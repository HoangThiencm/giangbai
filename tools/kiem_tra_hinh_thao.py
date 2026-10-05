import os
import sys
import fitz # PyMuPDF
import re

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

def inspect_geom(f_name):
    path = os.path.join(thao_dir, f_name)
    doc = fitz.open(path)
    print(f"\n=======================================================")
    print(f"TỆP: {f_name} (Số trang: {len(doc)})")
    print(f"=======================================================")
    
    # 1. Header/Footer trang 1, 2
    for p in range(min(2, len(doc))):
        lines = [l.strip() for l in doc[p].get_text().split('\n') if l.strip()]
        print(f"Trang {p+1} Header: {' | '.join(lines[:3])}")
        print(f"Trang {p+1} Footer: {' | '.join(lines[-3:])}")

    # 2. Danh sách bài học / Tiết
    print("--- Danh sách bài học / Tiết ---")
    for p_no in range(len(doc)):
        text = doc[p_no].get_text()
        for line in text.split('\n'):
            line_u = line.strip().upper()
            if any(k in line_u for k in ['TIẾT ', 'BÀI 1', 'BÀI 2', 'BÀI 8', 'BÀI 9', 'BÀI 10', 'BÀI 18', 'BÀI 19', 'LUYỆN TẬP CHUNG']):
                if len(line.strip()) < 80 and not line.strip().startswith('Bài 1.') and not line.strip().startswith('Bài 8.'):
                    print(f" P.{p_no+1}: {line.strip()}")

for f in os.listdir(thao_dir):
    if "HINH" in f.upper():
        inspect_geom(f)
