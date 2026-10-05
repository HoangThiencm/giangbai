import fitz
import os
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

for f in os.listdir(thao_dir):
    clean = remove_accents(f).upper()
    if "HINH" in clean and "7" in clean and f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(thao_dir, f))
        print(f"=== CHI TIẾT CÁC BÀI TẬP VÀ CÔNG THỨC TRONG {f} ===")
        for p_no in [4, 5, 6, 7, 8, 9, 21, 22, 23, 28, 29]:
            text = doc[p_no - 1].get_text()
            print(f"\n--- TRANG {p_no} ---")
            for line in text.split('\n'):
                l = line.strip()
                if any(c in l for c in ['Bài', 'Ta có', '+', '=', '180', 'xOy', 'x\'Oy', 'tOz', '·', '̂', 'xOy', 'yOz', 'A1', 'B1', 'mOn']):
                    print("  ", l)
