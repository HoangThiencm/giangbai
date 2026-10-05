import os
import sys
import fitz

sys.stdout.reconfigure(encoding='utf-8')

sang_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG")

for f in os.listdir(sang_dir):
    if f.lower().endswith('.pdf') and "1791188882357" in f:
        doc = fitz.open(os.path.join(sang_dir, f))
        print(f"=== HINH HOC 9 ({len(doc)} trang) ===")
        for p in range(13, len(doc)):
            text = doc[p].get_text()
            print(f"\n--- Page {p+1} ---")
            for l in text.split('\n'):
                if any(k in l.upper() for k in ['TIẾT ', 'BÀI 12', 'BÀI 13', 'HỆ THỨC', 'BẢNG LƯỢNG GIÁC']):
                    print("  ", l.strip())
