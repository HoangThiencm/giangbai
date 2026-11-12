import os
import sys
import pymupdf

base_dir = r'C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\3_DUYET_GIAO_AN\Dau_vao'
sys.stdout.reconfigure(encoding='utf-8')

for item in os.listdir(base_dir):
    p = os.path.join(base_dir, item)
    if os.path.isdir(p):
        print(f"\n==================== {item} ====================")
        for f in os.listdir(p):
            if f.endswith('.pdf'):
                pdf_path = os.path.join(p, f)
                doc = pymupdf.open(pdf_path)
                p1 = doc[0].get_text('text')
                lines = [l.strip() for l in p1.split('\n') if l.strip()]
                # find lines with Lớp, Tiết, Bài
                info = [l for l in lines if any(k in l for k in ['Lớp', 'lớp', 'Tiết', 'tiết', 'Tuần', 'tuần', 'Bài', 'Kế hoạch bài dạy', 'Trường'])]
                print(f"--- {f[:30]} ---")
                print(" | ".join(info[:6]))
