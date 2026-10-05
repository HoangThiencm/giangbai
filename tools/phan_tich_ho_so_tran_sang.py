import os
import sys
import fitz # PyMuPDF
import unicodedata
import re

sys.stdout.reconfigure(encoding='utf-8')

sang_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG")

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

pdf_files = [f for f in os.listdir(sang_dir) if f.lower().endswith('.pdf')]
print(f"Thư mục TRAN SANG có {len(pdf_files)} tệp PDF:")
for f in pdf_files:
    print(" -", f)

def analyze_pdf(f_name):
    path = os.path.join(sang_dir, f_name)
    doc = fitz.open(path)
    clean_name = remove_accents(f_name).upper()
    num_pages = len(doc)
    print(f"\n=======================================================")
    print(f"TỆP: {clean_name} ({num_pages} trang)")
    print(f"=======================================================")

    # 1. Header/Footer
    print("--- 1. Header / Footer ---")
    for p_no in range(min(3, num_pages)):
        lines = [l.strip() for l in doc[p_no].get_text().split('\n') if l.strip()]
        hdr = lines[:2] if len(lines) >= 2 else lines
        ftr = lines[-2:] if len(lines) >= 2 else lines
        print(f" P.{p_no+1} Top: {' | '.join(hdr)}")
        print(f" P.{p_no+1} Bot: {' | '.join(ftr)}")

    # 2. Danh sách bài học và Tiết
    print("\n--- 2. Danh sách Bài học / Tiết dạy ---")
    lessons = []
    full_text = ""
    for p_no in range(num_pages):
        page_text = doc[p_no].get_text()
        full_text += f"\n[PAGE {p_no+1}]\n" + page_text
        for line in page_text.split('\n'):
            line_s = line.strip()
            line_u = remove_accents(line_s).upper()
            if any(k in line_u for k in ['TIET ', 'BAI ', 'LUYEN TAP CHUNG', 'CHUONG ']):
                if any(term in line_u for term in [
                    'TIET 1', 'TIET 2', 'TIET 3', 'TIET 4', 'TIET 5', 'TIET 6', 'TIET 7', 'TIET 8', 'TIET 9', 'TIET 10', 'TIET 11', 'TIET 12', 'TIET 13', 'TIET 14',
                    'BAI 1', 'BAI 2', 'BAI 3', 'BAI 4', 'BAI 5', 'BAI 6', 'BAI 7', 'BAI 11', 'BAI 12', 'BAI 13', 'BAI 18', 'BAI 19',
                    'LUYEN TAP CHUNG', 'ON TAP CHUONG'
                ]):
                    if len(line_s) < 85 and not line_s.startswith('Bài 1.') and not line_s.startswith('Bài 2.') and not line_s.startswith('Bài 3.') and not line_s.startswith('Bài 4.') and not line_s.startswith('Bài 5.') and not line_s.startswith('Bài 6.') and not line_s.startswith('Bài 7.'):
                        lessons.append((p_no+1, line_s))
                        print(f" P.{p_no+1:02d}: {line_s}")

    # 3. Năng lực số / AI
    print("\n--- 3. Kiểm tra Năng lực số / AI ---")
    nls_lines = []
    for p_no in range(num_pages):
        page_text = doc[p_no].get_text()
        for l in page_text.split('\n'):
            ls = l.strip()
            if any(k in ls.lower() for k in ['năng lực số', 'nls', '5.3', '3.1', '9.b2', 'năng lực ai', 'trí tuệ nhân tạo']):
                nls_lines.append((p_no+1, ls))
    print(f" Số dòng đề cập NLS / AI: {len(nls_lines)}")
    for p_no, ls in nls_lines[:10]:
        print(f"   [P.{p_no}]: {ls}")

    # 4. Kiểm tra in đậm + nghiêng (bold italic) cho NLS
    bold_italic_nls = []
    for p_no in range(num_pages):
        blocks = doc[p_no].get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        flags = s["flags"]
                        font_name = s["font"].lower()
                        is_bi = (flags & 18 == 18) or ("bold" in font_name and ("italic" in font_name or "oblique" in font_name))
                        if is_bi:
                            t = s["text"].strip()
                            if len(t) > 3 and any(k in t.lower() for k in ['năng lực', 'số', 'ai', '5.3', '3.1', 'máy tính', 'phần mềm', 'casio']):
                                bold_italic_nls.append((p_no+1, t))
    print(f" Số đoạn NLS/AI in đậm + nghiêng: {len(bold_italic_nls)}")
    for p_no, t in bold_italic_nls[:10]:
        print(f"   [P.{p_no}]: {t}")

for f in pdf_files:
    analyze_pdf(f)
