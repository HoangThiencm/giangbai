import os
import sys
import fitz # PyMuPDF
import re

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")
pdf_files = [f for f in os.listdir(thao_dir) if f.lower().endswith('.pdf')]

print(f"Danh sách tệp PDF của cô Nguyễn Thị Thảo ({len(pdf_files)} tệp):")
for f in pdf_files:
    print(" -", f)

def analyze_pdf(file_name):
    path = os.path.join(thao_dir, file_name)
    doc = fitz.open(path)
    num_pages = len(doc)
    print(f"\n=======================================================")
    print(f"TỆP: {file_name} ({num_pages} trang)")
    print(f"=======================================================")
    
    # 1. Kiểm tra Header / Footer ở trang 1, 2, 3
    print("--- 1. Kiểm tra Header / Footer ---")
    for p_no in range(min(3, num_pages)):
        text = doc[p_no].get_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        hdr = lines[:4] if len(lines) >= 4 else lines
        ftr = lines[-4:] if len(lines) >= 4 else lines
        print(f" Trang {p_no+1} Đầu trang: {' | '.join(hdr[:2])}")
        print(f" Trang {p_no+1} Cuối trang: {' | '.join(ftr[-2:])}")

    # 2. Tìm danh sách bài học / tiết PPCT
    print("\n--- 2. Danh sách Bài học / Tiết dạy ---")
    full_text = ""
    for p_no in range(num_pages):
        page_text = doc[p_no].get_text()
        full_text += f"\n[PAGE {p_no+1}]\n" + page_text
        for line in page_text.split('\n'):
            line_s = line.strip()
            if any(k in line_s.upper() for k in ['BÀI ', 'TIẾT ', 'LUYỆN TẬP CHUNG', 'CHƯƠNG ']):
                if len(line_s) < 80 and any(c.isdigit() for c in line_s):
                    # print lesson headings
                    if any(term in line_s.upper() for term in ['BÀI 1', 'BÀI 2', 'BÀI 3', 'BÀI 4', 'BÀI 5', 'BÀI 6', 'BÀI 7', 'BÀI 8', 'BÀI 9', 'BÀI 10', 'BÀI 11', 'BÀI 18', 'BÀI 19', 'LUYỆN TẬP']):
                        print(f" P.{p_no+1}: {line_s}")

    # 3. Kiểm tra Năng lực số / AI
    print("\n--- 3. Kiểm tra Năng lực số / AI ---")
    nls_matches = re.findall(r'(năng lực số[^\n]+|năng lực ai[^\n]+|NLS[^\n]+|5\.3[^\n]+|1\.1[^\n]+|3\.1[^\n]+|AI[^\n]+)', full_text, re.IGNORECASE)
    print(f" Số đoạn đề cập NLS / AI: {len(nls_matches)}")
    for m in nls_matches[:8]:
        print(f"   * {m.strip()}")

    # 4. Kiểm tra font chữ, in nghiêng đậm của NLS nếu có
    # Kiểm tra xem có text spans với bold+italic không
    bold_italic_spans = []
    for p_no in range(num_pages):
        blocks = doc[p_no].get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        flags = s["flags"]
                        # bit 1: italic (2), bit 4: bold (16) -> bold+italic = flags & 18 == 18
                        is_bold = bool(flags & 16) or "bold" in s["font"].lower()
                        is_italic = bool(flags & 2) or "italic" in s["font"].lower() or "oblique" in s["font"].lower()
                        if is_bold and is_italic:
                            txt = s["text"].strip()
                            if len(txt) > 5 and any(k in txt.lower() for k in ['năng lực', 'số', 'ai', 'tc', 'máy tính', 'công cụ']):
                                bold_italic_spans.append((p_no+1, txt))
    print(f" Số đoạn NLS/AI in đậm + nghiêng: {len(bold_italic_spans)}")
    for p_no, txt in bold_italic_spans[:5]:
        print(f"   * [P.{p_no}]: {txt}")

    # 5. Soát lỗi toán học cơ bản (ký hiệu góc, định lý, dấu)
    print("\n--- 5. Soát từ khóa toán học & ký hiệu ---")
    math_errors = []
    for p_no in range(num_pages):
        page_text = doc[p_no].get_text()
        # Tìm các dòng có A + B + C + D = 360 hoặc mất dấu góc hoặc lỗi tính toán
        lines = page_text.split('\n')
        for l in lines:
            l_str = l.strip()
            if any(err_pat in l_str for err_pat in ['360°', '360 độ', '180°', '180 độ', 'định lí', 'định lý']):
                if any(c in l_str for c in ['A +', 'B +', 'C +', 'H +', 'E +', 'F -', 'D =']):
                    math_errors.append((p_no+1, l_str))
    if math_errors:
        print(f" Đoạn cần lưu ý về công thức góc/tính toán ({len(math_errors)} dòng):")
        for p_no, l_str in math_errors[:10]:
            print(f"   * P.{p_no}: {l_str}")
    else:
        print(" Không phát hiện dấu hiệu sai định lý/công thức tứ giác dạng thô.")

for f in pdf_files:
    analyze_pdf(f)
