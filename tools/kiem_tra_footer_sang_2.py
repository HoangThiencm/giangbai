import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

sang_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG")

for f in os.listdir(sang_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(sang_dir, f))
        has_footer = False
        for p in range(len(doc)):
            text = doc[p].get_text().lower()
            if "năm học: 2026-2027" in text or "năm học 2026-2027" in text or "trang " in text:
                has_footer = True
                break
        print(f"{f}: has footer = {has_footer}")
