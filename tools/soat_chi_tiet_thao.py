import os
import sys
import fitz
import re
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def check_file_detail(f_name):
    path = os.path.join(thao_dir, f_name)
    doc = fitz.open(path)
    clean_name = remove_accents(f_name).upper()
    print(f"\n=======================================================")
    print(f"KIỂM TRA CHI TIẾT: {clean_name} ({len(doc)} trang)")
    print(f"=======================================================")

    # 1. Soát NLS / AI
    print("--- 1. Rà soát Năng lực số / AI ---")
    found_nls = False
    for p_no in range(len(doc)):
        page = doc[p_no]
        text = page.get_text()
        for line in text.split('\n'):
            line_s = line.strip()
            if any(k in line_s.lower() for k in ['năng lực số', 'nls', '5.3', '3.1', '1.1', '1.2', 'trí tuệ nhân tạo', 'năng lực ai']):
                found_nls = True
                print(f" [P.{p_no+1}]: {line_s}")
    if not found_nls:
        print(" Không có đoạn văn nào đề cập rõ NLS / AI.")

    # 2. Soát các đoạn text in đậm + nghiêng (bold + italic)
    print("\n--- 2. Rà soát các đoạn in đậm + nghiêng (bold italic) ---")
    bold_italic_list = []
    for p_no in range(len(doc)):
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
                            if len(t) > 3:
                                bold_italic_list.append((p_no+1, t))
    print(f" Tổng số đoạn bold+italic: {len(bold_italic_list)}")
    for p_no, t in bold_italic_list[:10]:
        print(f"   [P.{p_no}]: {t}")

    # 3. Soát ký hiệu góc (đối với Hình học)
    if "HINH" in clean_name:
        print("\n--- 3. Soát ký hiệu góc trong Hình học ---")
        angles = []
        for p_no in range(len(doc)):
            text = doc[p_no].get_text()
            lines = text.split('\n')
            for l in lines:
                l_s = l.strip()
                # Kiểm tra ký hiệu góc: mũ góc hoặc ký hiệu góc lạ
                if any(k in l_s for k in ['xOy', 'yOz', 'AOB', 'BOC', 'góc', 'Góc', 'kề bù', 'đối đỉnh', 'đồng vị', 'so le trong']):
                    # kiểm tra xem có góc không mũ không
                    angles.append((p_no+1, l_s))
        print(f" Số dòng liên quan đến góc: {len(angles)}")
        for p_no, l_s in angles[:15]:
            print(f"   [P.{p_no}]: {l_s}")

for f in os.listdir(thao_dir):
    if f.lower().endswith('.pdf'):
        check_file_detail(f)
