import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

sang_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG")

for f in os.listdir(sang_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(sang_dir, f))
        print(f"\n=== KIỂM TRA FOOTER: {f} ===")
        for p_no in [1, 2, len(doc)//2, len(doc)]:
            page = doc[p_no - 1]
            lines = [l.strip() for l in page.get_text().split('\n') if l.strip()]
            print(f" Trang {p_no} Cuối trang: {' | '.join(lines[-3:])}")
