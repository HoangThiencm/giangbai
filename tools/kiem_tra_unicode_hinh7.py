import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")

for f in os.listdir(thao_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(thao_dir, f))
        if len(doc) == 30 and "Hình học 7" in doc[0].get_text():
            page = doc[7] # Trang 8
            for b in page.get_text("dict")["blocks"]:
                if "lines" in b:
                    for l in b["lines"]:
                        for s in l["spans"]:
                            t = s["text"]
                            if any(c in t for c in ['·', '¶']) or s["size"] > 14:
                                print(f"Text: {repr(t)} | Font: {s['font']} | Size: {s['size']} | Unicodes: {[ord(c) for c in t]}")
