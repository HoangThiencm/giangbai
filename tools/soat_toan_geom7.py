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
    if f.lower().endswith('.pdf'):
        clean = remove_accents(f).upper()
        if "HINH" in clean and "7" in clean:
            doc = fitz.open(os.path.join(thao_dir, f))
            print(f"=== SOÁT KÝ HIỆU TOÁN HỌC TRONG {f} ({len(doc)} trang) ===")
            for p_no in range(len(doc)):
                text = doc[p_no].get_text()
                lines = text.split('\n')
                for l in lines:
                    ls = l.strip()
                    if any(k in ls for k in ['°', '= 180', '= 90', '= 360', 'kề bù', 'đối đỉnh', 'so le', 'đồng vị']):
                        if any(c in ls for c in ['+', '-', '=']):
                            print(f"P.{p_no+1}: {ls}")
