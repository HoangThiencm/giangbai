import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

for f in os.listdir(thao_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(thao_dir, f))
        if len(doc) == 30 and "Đại Số 7" in doc[0].get_text():
            print(f"=== SOÁT ĐẠI SỐ 7: {f} ===")
            for p_no in range(len(doc)):
                text = doc[p_no].get_text()
                lines = text.split('\n')
                for l in lines:
                    ls = l.strip()
                    if any(k in ls for k in ['Bài 1.', 'Bài 1.1', 'Bài 1.2', 'Bài 1.7', 'Bài 1.8', 'Bài 1.12', 'Bài 1.16', 'Bài 1.18', 'Bài 1.24']):
                        print(f"P.{p_no+1:02d}: {ls}")
