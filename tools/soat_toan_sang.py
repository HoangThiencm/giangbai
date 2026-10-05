import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

sang_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG")

for f in os.listdir(sang_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(sang_dir, f))
        first_page = doc[0].get_text()
        if "Hình học" in first_page:
            print(f"\n=== SOÁT KÝ HIỆU TOÁN HỌC: {f} ({len(doc)} trang) ===")
            for p_no in range(len(doc)):
                text = doc[p_no].get_text()
                for line in text.split('\n'):
                    ls = line.strip()
                    if any(k in ls for k in ['sin', 'cos', 'tan', 'cot', 'góc', 'Góc', '°', 'độ']):
                        if any(c in ls for c in ['=', '+', '-', '√', '𝛼', 'B =', 'C =', 'A =']):
                            if len(ls) < 80:
                                print(f" P.{p_no+1:02d}: {ls}")
