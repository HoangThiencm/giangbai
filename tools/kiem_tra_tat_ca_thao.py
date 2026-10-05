import os
import sys
import fitz # PyMuPDF
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

for f in os.listdir(thao_dir):
    f_clean = remove_accents(f).upper()
    print(f"File found: {f_clean}")
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(thao_dir, f))
        print(f"\n=======================================================")
        print(f"TỆP: {f} (Số trang: {len(doc)})")
        print(f"=======================================================")
        
        # Header / Footer trang 1, 2
        for p in range(min(2, len(doc))):
            lines = [l.strip() for l in doc[p].get_text().split('\n') if l.strip()]
            print(f"Trang {p+1} Đầu: {' | '.join(lines[:2])}")
            print(f"Trang {p+1} Cuối: {' | '.join(lines[-2:])}")
            
        # Tìm bài và tiết
        print("--- Danh sách bài học / Tiết ---")
        for p_no in range(len(doc)):
            text = doc[p_no].get_text()
            for line in text.split('\n'):
                line_u = remove_accents(line).upper()
                if any(k in line_u for k in ['TIET ', 'BAI ', 'LUYEN TAP CHUNG', 'CHUONG ']):
                    # filter interesting lines
                    if any(term in line_u for term in ['TIET 1', 'TIET 2', 'TIET 3', 'TIET 4', 'TIET 5', 'TIET 6', 'TIET 7', 'TIET 8', 'TIET 9', 'TIET 10', 'TIET 11', 'TIET 12', 'BAI 1', 'BAI 2', 'BAI 3', 'BAI 4', 'BAI 5', 'BAI 6', 'BAI 7', 'BAI 8', 'BAI 9', 'BAI 10', 'BAI 11', 'BAI 18', 'BAI 19', 'LUYEN TAP CHUNG']):
                        if len(line.strip()) < 80:
                            print(f" P.{p_no+1}: {line.strip()}")
