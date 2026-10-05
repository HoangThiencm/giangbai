import os
import sys
import fitz
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

for f in os.listdir(thao_dir):
    f_clean = remove_accents(f).upper()
    if "HINH" in f_clean and "6" in f_clean:
        print(f"\n=======================================================")
        print(f"TỆP: {f}")
        print(f"=======================================================")
        doc = fitz.open(os.path.join(thao_dir, f))
        print("Tổng số trang:", len(doc))
        for p in range(min(2, len(doc))):
            lines = [l.strip() for l in doc[p].get_text().split('\n') if l.strip()]
            print(f"Trang {p+1} Đầu: {' | '.join(lines[:2])}")
            print(f"Trang {p+1} Cuối: {' | '.join(lines[-2:])}")
        print("--- Danh sách bài học / Tiết ---")
        for p_no in range(len(doc)):
            text = doc[p_no].get_text()
            for line in text.split('\n'):
                line_u = remove_accents(line).upper()
                if any(k in line_u for k in ['TIET ', 'BAI ', 'CHƯƠNG ', 'CHUONG ']):
                    if any(term in line_u for term in ['TIET 1', 'TIET 2', 'TIET 3', 'TIET 4', 'TIET 5', 'BAI 18', 'BAI 19']):
                        if len(line.strip()) < 80:
                            print(f" P.{p_no+1}: {line.strip()}")
