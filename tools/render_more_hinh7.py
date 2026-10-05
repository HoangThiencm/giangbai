import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

for f in os.listdir(thao_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(thao_dir, f))
        if len(doc) == 30 and "Hình học 7" in doc[0].get_text():
            for p_no in [22, 23, 28, 29]:
                page = doc[p_no - 1]
                pix = page.get_pixmap(dpi=150)
                out_img = f"page_{p_no}_hinh7.png"
                pix.save(out_img)
                print(f"Saved {out_img}")
