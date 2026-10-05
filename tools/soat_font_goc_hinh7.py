import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

for f in os.listdir(thao_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(thao_dir, f))
        if len(doc) == 30 and "Hình học 7" in doc[0].get_text():
            print(f"FOUND: {f}")
            for p_no in [8, 9, 21, 23]:
                page = doc[p_no - 1]
                print(f"\n=================== TRANG {p_no} ===================")
                blocks = page.get_text("dict")["blocks"]
                for b in blocks:
                    if "lines" in b:
                        for l in b["lines"]:
                            line_text = "".join([s["text"] for s in l["spans"]])
                            if any(k in line_text for k in ['Bài 3.4', 'Bài 3.5', 'Bài 3.13', 'Bài 3.15', 'Ta có', 'kề bù', 'đối đỉnh', 'so le', '·', '¶']):
                                print("LINE:", line_text)
                                for s in l["spans"]:
                                    print(f"   SPAN: text={repr(s['text'])}, font={s['font']}, size={s['size']:.1f}")
