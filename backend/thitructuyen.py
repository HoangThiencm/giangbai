import json
import uuid
import io
import os
import re
import time
import random
import shutil
import base64
import fitz  # PyMuPDF
import asyncio
import cv2
import numpy as np
import difflib # Thư viện so sánh chuỗi
from datetime import datetime
from typing import Dict, Optional, List, Any, Union
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Body
from pydantic import BaseModel
import google.generativeai as genai
from supabase import create_client, Client
from concurrent.futures import ThreadPoolExecutor

# Import module Google Sheet
try:
    from google_utils import gsheet_client
except ImportError:
    gsheet_client = None
    print("⚠️ Warning: google_utils not found. GSheet feature disabled.")

# --- TẮT OCR ĐỂ TĂNG TỐC KHỞI ĐỘNG VÀ XỬ LÝ ---
ocr_engine = None 

router = APIRouter(prefix="/api/exam", tags=["Thitructuyen"])
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# === KẾT NỐI SUPABASE ===
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ [Thitructuyen] Đã kết nối Supabase thành công!")
    except Exception as e:
        print(f"❌ [Thitructuyen] Lỗi kết nối Supabase: {e}")

# === MODELS ===
class SaveExamRequest(BaseModel):
    id: Optional[str] = None
    title: str
    school: str
    subject: str = ""
    grade: str = ""
    duration: Union[int, str]
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    api_keys: List[str]
    teacher_email: str
    questions: List[Dict[str, Any]]
    google_sheet_id: Optional[str] = None

class Submission(BaseModel):
    exam_id: str
    student_name: str
    sbd: str
    student_class: str
    answers: Dict[str, int]

class NormalizeRequest(BaseModel):
    raw_text: str = ""
    image_data: str    # Ảnh full page
    api_keys: List[str]
    model: str = "gemini-2.5-flash" # Nhận model từ frontend

class ImportAnswerRequest(BaseModel):
    image_data: str
    api_keys: List[str]
    model: str = "gemini-2.5-flash" # Nhận model từ frontend

# [NEW] Model cho request nhận diện vùng thủ công
class NormalizeManualRequest(BaseModel):
    cropped_data: str
    api_keys: List[str]
    model: str = "gemini-2.5-flash"

# === UTILS ===

def clean_text(text):
    """Làm sạch văn bản: xóa xuống dòng thừa, khoảng trắng thừa"""
    if not text: return ""
    # Xóa ký tự đầu dòng kiểu A. B. nếu AI lỡ đưa vào
    text = re.sub(r'^[A-D]\.\s*', '', text.strip())
    # Xóa xuống dòng
    text = text.replace('\n', ' ').replace('\r', '')
    return " ".join(text.split())

def extract_gemini_text(resp):
    """Trích xuất text an toàn từ phản hồi Gemini"""
    if hasattr(resp, "text") and resp.text:
        return resp.text.strip()
    try:
        if hasattr(resp, "candidates") and resp.candidates:
            parts = resp.candidates[0].content.parts
            txt = ""
            for p in parts:
                if hasattr(p, "text") and p.text:
                    txt += p.text + "\n"
            return txt.strip()
    except:
        pass
    return ""

def slice_image_smart_overlap(img_bytes, slices=2, overlap_ratio=0.15):
    """
    Cắt ảnh thành nhiều phần với độ chồng lấn (overlap) để xử lý đa luồng.
    overlap_ratio: Tỷ lệ chồng lấn (15% chiều cao)
    slices: 2 là đủ cho trang A4 thông thường để tránh lặp nhiều.
    """
    try:
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None: return [img_bytes] 

        h, w = img.shape[:2]
        if h < 1000: return [img_bytes] # Ảnh nhỏ không cần cắt

        # Resize chiều ngang nếu quá lớn để giảm dung lượng
        if w > 1600:
            scale = 1600 / w
            img = cv2.resize(img, (1600, int(h * scale)), interpolation=cv2.INTER_AREA)
            h, w = img.shape[:2]

        chunk_h = h // slices
        overlap_px = int(h * overlap_ratio)
        parts = []

        for i in range(slices):
            # Tính toán tọa độ cắt
            y_start = i * chunk_h
            y_end = (i + 1) * chunk_h
            
            # Thêm overlap
            if i > 0: y_start = max(0, y_start - overlap_px)
            if i < slices - 1: y_end = min(h, y_end + overlap_px)
            else: y_end = h # Chunk cuối lấy hết

            crop = img[y_start:y_end, :]
            
            # Nén nhẹ để gửi nhanh hơn
            _, buf = cv2.imencode(".jpg", crop, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            parts.append(buf.tobytes())

        return parts
    except Exception as e:
        print(f"Slicing Error: {e}")
        return [img_bytes]

# Hàm khử trùng lặp thông minh
def is_duplicate(q1, q2_list):
    """
    Kiểm tra xem câu hỏi q1 có bị trùng với bất kỳ câu nào trong danh sách q2_list không.
    Sử dụng so sánh chuỗi tương đối (difflib).
    """
    def normalize(text):
        # Xóa khoảng trắng, lowercase để so sánh
        return re.sub(r'\s+', '', str(text)).lower()

    text1 = normalize(q1.get('question', ''))
    # Nếu câu hỏi quá ngắn (ví dụ: "Câu 1:"), so sánh thêm đáp án
    if len(text1) < 20:
        text1 += normalize("".join(q1.get('options', [])))

    for q2 in q2_list:
        text2 = normalize(q2.get('question', ''))
        if len(text2) < 20:
            text2 += normalize("".join(q2.get('options', [])))
            
        # Tính tỷ lệ giống nhau
        ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
        
        # Nếu giống > 85% -> Coi là trùng
        if ratio > 0.85:
            return True
            
        # Hoặc kiểm tra nếu nội dung câu này chứa câu kia (cho trường hợp cắt bị dư/thiếu chút ít)
        if len(text1) > 50 and len(text2) > 50:
            if text1 in text2 or text2 in text1:
                return True
                
    return False

# === API ENDPOINTS ===

@router.post("/process_paper")
async def process_paper(file: UploadFile = File(...)):
    """ONE-SHOT MODE: Chuyển PDF thành danh sách ảnh Full Page."""
    try:
        file_id = str(uuid.uuid4())
        ext = os.path.splitext(file.filename)[1].lower()
        temp_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        doc = fitz.open(temp_path)
        pages = []
        
        for i, page in enumerate(doc):
            # [OPTIMIZE] Giữ Zoom 2.0 (200 DPI) để cân bằng giữa độ nét và dung lượng
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            img_data = pix.tobytes("jpg")
            b64_str = base64.b64decode(img_data).decode("utf-8") if isinstance(img_data, str) else base64.b64encode(img_data).decode("utf-8")
            
            pages.append({
                "id": str(uuid.uuid4()),
                "page_index": i + 1,
                "image_data": f"data:image/jpeg;base64,{b64_str}",
                "status": "pending",
                "q_count": 0 
            })

        doc.close()
        try: os.remove(temp_path)
        except: pass

        return { "status": "ok", "pages": pages }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Lỗi xử lý PDF: {str(e)}")


async def call_gemini_vision_robust(api_keys, prompt, img_bytes, model_name="gemini-2.5-flash", retries=3):
    """
    Gọi Gemini với cơ chế tự động xoay key và retry khi lỗi.
    Sử dụng model_name được truyền vào.
    """
    # Xáo trộn danh sách key để cân bằng tải
    shuffled_keys = list(api_keys)
    random.shuffle(shuffled_keys)
    
    last_error = None
    
    for i in range(min(len(shuffled_keys), retries)):
        key = shuffled_keys[i]
        genai.configure(api_key=key)
        # Sử dụng model được chỉ định
        model = genai.GenerativeModel(model_name)
        
        try:
            loop = asyncio.get_running_loop()
            resp = await loop.run_in_executor(
                None, 
                lambda: model.generate_content([
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_bytes}}
                ])
            )
            
            txt = extract_gemini_text(resp)
            
            # Xử lý JSON sạch
            if "```json" in txt:
                txt = txt.split("```json")[1].split("```")[0].strip()
            elif "```" in txt:
                txt = txt.replace("```","").strip()
                
            if txt.startswith("[") or txt.startswith("{"):
                data = json.loads(txt)
                if isinstance(data, dict): data = [data]
                return data
            return txt # Trả về text nếu không phải JSON (cho trường hợp feedback)
            
        except Exception as e:
            last_error = e
            # print(f"Key ...{key[-4:]} failed: {e}. Switching key...")
            continue
            
    # print(f"All retries failed. Last error: {last_error}")
    return []


# ==== NEW: STREAM PROGRESS FOR A PAGE ====

progress_store = {}

@router.get("/progress/{page_id}")
async def get_progress(page_id: str):
    from fastapi.responses import StreamingResponse

    async def event_stream():
        last_value = -1
        while True:
            await asyncio.sleep(0.2)
            value = progress_store.get(page_id, 0)

            if value != last_value:
                last_value = value
                yield f"data: {value}\n\n"

            if value >= 100:
                break

    return StreamingResponse(event_stream(), media_type="text/event-stream")



@router.post("/normalize_segment")
async def normalize_segment(req: NormalizeRequest):
    if not req.api_keys:
        raise HTTPException(400, "Missing API Keys")
    
    # --- GIẢI MÃ ẢNH ---
    try:
        if "base64," in req.image_data:
            img_base64 = req.image_data.split("base64,")[1]
        else:
            img_base64 = req.image_data
        img_bytes = base64.b64decode(img_base64)
    except:
        return {"status": "error", "message": "Invalid Image Data", "data": []}

    # 🌟 BƯỚC 2 — Reset progress (0%)
    progress_store[req.model] = 0

    # --- PROMPT LATEX CHUẨN HÓA ---
    BASE_PROMPT = """
    Trích xuất câu hỏi trắc nghiệm từ phần ảnh này.
    
    YÊU CẦU QUAN TRỌNG:
    1. ĐỌC KỸ: Tìm đủ các câu có đánh số (Câu X, Bài X...).
    2. CHUẨN HÓA NGHIÊM NGẶT TOÁN HỌC (LATEX):
       - Bắt buộc dùng LaTeX cho TẤT CẢ công thức, ký hiệu toán học (biến x, y, tập hợp R, N, độ C, độ F...).
       - Inline Math: $...$ (TUYỆT ĐỐI KHÔNG có khoảng trắng sau $ mở và trước $ đóng. Ví dụ: $x^2$ là ĐÚNG, $x^2$ là SAI).
       - Display Math: $$...$$ (căn giữa).
       - Ký hiệu chia hết: dùng \\vdots (ba chấm dọc).
       - Tam giác: dùng \\Delta (không dùng Triangle).
       - Góc: dùng \\widehat{ABC}.
       - In đậm: dùng \\textbf{Nội dung}.
       - In nghiêng: dùng \\textit{Nội dung}. (Lưu ý: dùng textit cho nghiêng, textbf cho đậm).
       - Ví dụ chuẩn: $AB \\perp CD$, $\\widehat{A} = 90^\\circ$, $d_1 \\parallel d_2$, $S = \\pi r^2$.
    3. ĐÁP ÁN: Tách riêng 4 lựa chọn A, B, C, D vào mảng "options". Chỉ lấy nội dung, bỏ ký tự A., B. đầu dòng.
    4. KHÔNG BỊA ĐẶT: Nếu câu hỏi bị cắt ngang và bạn KHÔNG thấy đủ các lựa chọn (ví dụ chỉ thấy A, B mà mất C, D), HÃY CHỈ GHI NHẬN NHỮNG GÌ BẠN THẤY. TUYỆT ĐỐI KHÔNG TỰ BỊA RA NỘI DUNG CÒN THIẾU.
    5. CẮT TRANG:
       - Nếu thấy các đáp án (A, B...) ở ĐẦU ảnh mà không có câu hỏi đi kèm -> Tạo câu hỏi có nội dung "[[Tiếp nối]]".
    
    OUTPUT JSON (Mảng): [{"question": "...", "options": ["...",...], "correct_index": -1}, ...]
    """

    # --- CẮT ẢNH THÀNH NHIỀU PHẦN ---
    image_parts = slice_image_smart_overlap(img_bytes, slices=1, overlap_ratio=0.10)

    tasks = []
    total_parts = len(image_parts)

    # 🌟 BƯỚC 3 — cập nhật tiến trình theo từng phần ảnh
    for i, part in enumerate(image_parts):
        progress_store[req.model] = int((i / total_parts) * 100)

        part_context = f"Lưu ý: Đây là phần {i+1}/{total_parts} của trang."
        full_prompt = f"{part_context}\n{BASE_PROMPT}"

        tasks.append(
            call_gemini_vision_robust(req.api_keys, full_prompt, part, req.model)
        )

    # --- CHỜ AI XỬ LÝ SONG SONG ---
    results_list = await asyncio.gather(*tasks)

    # --- GHÉP DỮ LIỆU ---
    merged_questions = {}

    for i, res in enumerate(results_list):
        if not res or not isinstance(res, list):
            continue

        base_id = i * 1000

        for q in res:
            q_text = q.get("question", "")

            if "options" in q and isinstance(q["options"], list):
                q["options"] = [clean_text(opt) for opt in q["options"]]

            # Tìm số câu
            match = re.search(r"(Câu|Question|Bài)\s*(\d+)", q_text, re.IGNORECASE)

            if match:
                q_num = int(match.group(2))
                merged_questions[q_num] = q
            else:
                fake_id = base_id + 0.01 + len(merged_questions)
                merged_questions[fake_id] = q

    # --- CHUYỂN THÀNH DANH SÁCH ---
    raw_questions = []
    for k in sorted(merged_questions.keys()):
        q = merged_questions[k]
        if "options" not in q:
            q["options"] = ["", "", "", ""]
        q["status"] = "done"
        if "id" not in q:
            q["id"] = str(uuid.uuid4())
        raw_questions.append(q)

    # --- KHỬ TRÙNG LẶP ---
    unique_questions = []
    for q in raw_questions:
        if not is_duplicate(q, unique_questions):
            unique_questions.append(q)

    # 🌟 HOÀN THÀNH — TIẾN TRÌNH = 100%
    progress_store[req.model] = 100

    return {"status": "ok", "data": unique_questions}

# [NEW] API Xử lý vùng cắt thủ công
@router.post("/normalize_manual")
async def normalize_manual(req: NormalizeManualRequest):
    if not req.api_keys: raise HTTPException(400, "Missing API Keys")
    try:
        # Xử lý chuỗi base64 ảnh
        if "base64," in req.cropped_data:
            img_str = req.cropped_data.split("base64,")[1]
        else:
            img_str = req.cropped_data
        img_bytes = base64.b64decode(img_str)
    except:
        raise HTTPException(400, "Invalid Crop Image")

    PROMPT = """
    Bạn là một trợ lý AI chuyên trích xuất câu hỏi từ hình ảnh.
    
    NHIỆM VỤ:
    - Trích xuất các câu hỏi trắc nghiệm từ VÙNG ẢNH ĐƯỢC CUNG CẤP.
    - Đây là một phần cắt từ trang lớn, hãy đọc chính xác nội dung hiển thị.
    - KHÔNG được suy diễn câu hỏi bị cắt. Chỉ trích xuất những gì nhìn thấy rõ.
    
    YÊU CẦU ĐỊNH DẠNG (LATEX):
    - Toán học bắt buộc dùng LaTeX chuẩn: $x^2$, $\\frac{a}{b}$, $\\Delta$.
    - Không dùng unicode cho toán học (ví dụ: không dùng ², dùng ^2).
    
    OUTPUT JSON (Mảng): 
    [{"question": "Nội dung câu hỏi...", "options": ["A", "B", "C", "D"], "correct_index": -1}, ...]
    Nếu không có câu hỏi nào, trả về danh sách rỗng [].
    """

    res = await call_gemini_vision_robust(req.api_keys, PROMPT, img_bytes, req.model)
    
    # Gán ID cho các câu hỏi mới để đảm bảo frontend merge được
    final_questions = []
    if res and isinstance(res, list):
        for q in res:
            q["id"] = str(uuid.uuid4())
            q["status"] = "manual"
            if "options" not in q: q["options"] = ["","","",""]
            final_questions.append(q)
            
    return {"status": "ok", "data": final_questions}

@router.post("/import_answer_sheet")
async def import_answer_sheet(req: ImportAnswerRequest):
    if not req.api_keys: raise HTTPException(400, "Missing API Keys")
    try:
        img_str = req.image_data.split("base64,")[1] if "base64," in req.image_data else req.image_data
        img_bytes = base64.b64decode(img_str)
    except: raise HTTPException(400, "Invalid Image")

    PROMPT = """
    Trích xuất danh sách đáp án từ ảnh bảng đáp án này.
    Output JSON: [{"index": 1, "answer": "A"}, {"index": 2, "answer": "C"}...]
    """
    # Truyền req.model vào hàm gọi AI
    res = await call_gemini_vision_robust(req.api_keys, PROMPT, img_bytes, req.model)
    return {"status": "ok", "data": res} if res and isinstance(res, list) else {"status": "error"}

@router.post("/save")
async def save_exam_to_db(data: SaveExamRequest):
    if not supabase: raise HTTPException(500, "DB Disconnected")
    exam_id = data.id if data.id else str(uuid.uuid4())[:8]
    variants = [{"exam_code": "ROOT", "questions": data.questions, "meta": {"google_sheet_id": data.google_sheet_id}}]
    payload = {
        "teacher_email": data.teacher_email, "title": data.title, "school": data.school, 
        "duration_mins": int(data.duration), "variants_json": json.dumps(variants), 
        "api_keys_backup": json.dumps(data.api_keys), "start_time": data.start_time, "end_time": data.end_time
    }
    if data.id: supabase.table("exams").update(payload).eq("id", exam_id).execute()
    else: payload["id"] = exam_id; supabase.table("exams").insert(payload).execute()
    return {"status": "ok", "exam_id": exam_id}

@router.get("/get/{exam_id}")
def get_exam(exam_id: str):
    if not supabase: raise HTTPException(500, "DB Error")
    res = supabase.table("exams").select("*").eq("id", exam_id).execute()
    if not res.data: raise HTTPException(404, "Not Found")
    d = res.data[0]
    
    now_iso = datetime.utcnow().isoformat()
    start, end = d.get("start_time"), d.get("end_time")
    exam_status = "open"
    if start and now_iso < start: exam_status = "not_started"
    elif end and now_iso > end: exam_status = "expired"

    v = json.loads(d["variants_json"])
    return { 
        "info": { 
            "title": d["title"], "school": d["school"], "duration_mins": d["duration_mins"], 
            "id": d["id"], "start_time": start, "end_time": end, "status": exam_status 
        }, 
        "questions": v[0]["questions"] 
    }

@router.get("/my-exams")
def get_my_exams(email: str):
    if not supabase: raise HTTPException(500, "DB Error")
    return supabase.table("exams").select("*").eq("teacher_email", email).order("created_at", desc=True).execute().data

@router.delete("/delete/{exam_id}")
def delete_exam(exam_id: str):
    if not supabase: raise HTTPException(500, "DB Error")
    supabase.table("submissions").delete().eq("exam_id", exam_id).execute()
    supabase.table("exams").delete().eq("id", exam_id).execute()
    return {"message": "Deleted"}

@router.post("/duplicate/{exam_id}")
def duplicate_exam(exam_id: str):
    if not supabase: raise HTTPException(500, "DB Error")
    res = supabase.table("exams").select("*").eq("id", exam_id).execute()
    if not res.data: raise HTTPException(404, "Exam not found")
    new_data = {k: v for k, v in res.data[0].items() if k not in ['id', 'created_at']}
    new_data['id'] = str(uuid.uuid4())[:8]
    new_data['title'] += " (Copy)"
    supabase.table("exams").insert(new_data).execute()
    return {"status": "ok", "new_id": new_data['id']}

@router.put("/rename/{exam_id}")
def rename_exam(exam_id: str, body: Dict[str, str]):
    if not supabase: raise HTTPException(500, "DB Error")
    supabase.table("exams").update({"title": body['new_title']}).eq("id", exam_id).execute()
    return {"status": "ok"}

@router.post("/submit")
async def submit_exam(data: Submission):
    if not supabase: raise HTTPException(500, "DB Error")
    res = supabase.table("exams").select("variants_json, api_keys_backup").eq("id", data.exam_id).execute()
    if not res.data: raise HTTPException(404, "Not Found")
    
    variants = json.loads(res.data[0]["variants_json"])
    questions = variants[0]["questions"]
    correct = 0; wrong = []
    for i, q in enumerate(questions):
        user_ans = data.answers.get(str(i))
        true_ans = q.get("correct_index", -1)
        if user_ans == true_ans: correct += 1
        else: wrong.append({"q": q["question"], "ans": q["options"][true_ans] if true_ans != -1 else "?"})
            
    score = round((correct/len(questions))*10, 2) if questions else 0
    
    # --- [NEW] AI FEEDBACK GENERATION ---
    fb = f"Bạn làm đúng {correct}/{len(questions)} câu."
    try:
        api_keys = json.loads(res.data[0]["api_keys_backup"])
        if api_keys and wrong:
            # Tạo prompt ngắn gọn cho AI
            wrong_summary = "\n".join([f"- Câu: {w['q'][:100]}..." for w in wrong[:5]]) # Lấy tối đa 5 câu sai để tiết kiệm token
            prompt = f"""
            Học sinh làm bài thi được {score}/10 điểm. Đúng {correct}/{len(questions)} câu.
            Một số câu làm sai:
            {wrong_summary}
            
            Hãy viết một đoạn nhận xét ngắn (dưới 100 từ) bằng tiếng Việt.
            Động viên học sinh và chỉ ra cần ôn tập lại kiến thức liên quan đến các câu sai (nếu nhận diện được chủ đề).
            Giọng điệu: Thân thiện, giống giáo viên.
            """
            
            # Sử dụng hàm call_gemini_vision_robust để tận dụng cơ chế xoay key và retry
            # Lưu ý: Hàm này thiết kế cho vision nhưng vẫn dùng được cho text nếu img_bytes rỗng
            ai_comment_res = await call_gemini_vision_robust(api_keys, prompt, b"", model_name="gemini-2.5-flash")
            
            if isinstance(ai_comment_res, str):
                fb = ai_comment_res
            elif isinstance(ai_comment_res, list) and ai_comment_res:
                 # Nếu trả về JSON list
                 fb = ai_comment_res[0].get("feedback", ai_comment_res[0].get("message", str(ai_comment_res)))

    except Exception as e:
        print(f"AI Feedback Error: {e}")
        pass
    # ------------------------------------

    supabase.table("submissions").insert({
        "exam_id": data.exam_id, "student_name": data.student_name, "sbd": data.sbd, 
        "student_class": data.student_class, "score": score, "correct_count": correct, 
        "total_questions": len(questions), "details_json": json.dumps(wrong), "ai_feedback": fb
    }).execute()
    return {"score": score, "total": len(questions), "feedback": fb}

@router.get("/results/{exam_id}")
def get_results(exam_id: str):
    if not supabase: raise HTTPException(500, "DB Error")
    return supabase.table("submissions").select("*").eq("exam_id", exam_id).order("score", desc=True).execute().data


class DeleteResultsBatchRequest(BaseModel):
    ids: List[int]


@router.delete("/result/{result_id}")
def delete_result(result_id: int):
    if not supabase:
        raise HTTPException(500, "DB Error")
    check = supabase.table("submissions").select("id").eq("id", result_id).execute()
    if not check.data:
        raise HTTPException(404, "Không tìm thấy kết quả")
    supabase.table("submissions").delete().eq("id", result_id).execute()
    return {"status": "ok", "message": "Đã xóa kết quả", "id": result_id}


@router.post("/results/delete-batch")
def delete_results_batch(body: DeleteResultsBatchRequest):
    if not supabase:
        raise HTTPException(500, "DB Error")
    ids = [int(i) for i in (body.ids or []) if i is not None]
    if not ids:
        raise HTTPException(400, "Thiếu danh sách id")
    supabase.table("submissions").delete().in_("id", ids).execute()
    return {"status": "ok", "deleted": len(ids)}