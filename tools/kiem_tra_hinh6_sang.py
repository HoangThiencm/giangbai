import os
import sys
import fitz
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

sang_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG")

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

for f in os.listdir(sang_dir):
    clean = remove_accents(f).upper()
    if "HINH" in clean and "6" in clean and f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(sang_dir, f))
        print(f"=== {clean} ({len(doc)} trang) ===")
        for p in range(min(2, len(doc))):
            lines = [l.strip() for l in doc[p].get_text().split('\n') if l.strip()]
            print(f"P.{p+1} Top: {' | '.join(lines[:2])}")
            print(f"P.{p+1} Bot: {' | '.join(lines[-2:])}")
        print("--- Lessons ---")
        for p_no in range(len(doc)):
            text = doc[p_no].get_text()
            for line in text.split('\n'):
                line_u = remove_accents(line).strip().upper()
                if any(k in line_u for k in ['TIET ', 'BAI 18', 'BAI 19', 'CHUONG IV']):
                    if len(line.strip()) < 80 and not line.strip().startswith('Bài 18.') and not line.strip().startswith('Bài 19.'):
                        print(f" P.{p_no+1:02d}: {line.strip()}")
