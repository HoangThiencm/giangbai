import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

sang_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG")

for f in os.listdir(sang_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(sang_dir, f))
        # Dai so 9
        if "DAI SO 9" in f.upper() or "D?I S? 9" in f.upper() or len(doc) == 59:
            print(f"=== SOÁT NLS/AI ĐẠI SỐ 9 ({f}) ===")
            page1 = doc[0]
            for b in page1.get_text("dict")["blocks"]:
                if "lines" in b:
                    for l in b["lines"]:
                        txt = "".join([s["text"] for s in l["spans"]])
                        if any(k in txt for k in ['NLS', 'AI', '5.3', '9.B2', 'máy tính', 'trợ lý']):
                            spans = [f"'{s['text']}' [b={bool(s['flags']&16)}, i={bool(s['flags']&2)}, font={s['font']}]" for s in l["spans"]]
                            print("L:", txt)
                            print("  S:", " | ".join(spans[:3]))
        
        # So hoc 6
        if "SO HOC 6" in f.upper() or "S? H?C 6" in f.upper() or len(doc) == 43:
            print(f"\n=== SOÁT NLS SỐ HỌC 6 ({f}) ===")
            page35 = doc[34]
            for b in page35.get_text("dict")["blocks"]:
                if "lines" in b:
                    for l in b["lines"]:
                        txt = "".join([s["text"] for s in l["spans"]])
                        if any(k in txt for k in ['NLS', '5.3', '3.1', 'máy tính', 'lũy thừa']):
                            spans = [f"'{s['text']}' [b={bool(s['flags']&16)}, i={bool(s['flags']&2)}, font={s['font']}]" for s in l["spans"]]
                            print("L:", txt)
                            print("  S:", " | ".join(spans[:3]))
