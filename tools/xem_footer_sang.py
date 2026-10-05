import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

sang_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG")

for f in os.listdir(sang_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(sang_dir, f))
        print(f"\n--- {f} ---")
        for p in range(min(3, len(doc))):
            text = doc[p].get_text()
            for l in text.split('\n'):
                if any(k in l.lower() for k in ['năm học', 'môn', 'trang ']):
                    print(f" P.{p+1}: {l.strip()}")
