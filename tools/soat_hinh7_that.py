import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

for f in os.listdir(thao_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(thao_dir, f))
        # Find Hình học 7 (contains 30 pages and 'HINH HỌC 7' in title)
        p0 = doc[0].get_text()
        if "Hình học 7" in p0:
            print(f"=== CHI TIẾT CÁC BÀI TẬP VÀ CÔNG THỨC TRONG {f} ({len(doc)} trang) ===")
            for p_no in range(1, len(doc) + 1):
                text = doc[p_no - 1].get_text()
                lines = text.split('\n')
                for line in lines:
                    l = line.strip()
                    if any(c in l for c in ['Bài 3.', 'Ta có', '= 180', 'kề bù', 'đối đỉnh', 'so le', 'đồng vị', '̂', '෣', 'መ', '෡', '·']):
                        if any(c in l for c in ['=', '+', '-', '°', 'o', 'Bài 3']):
                            print(f"P.{p_no:02d}: {l}")
