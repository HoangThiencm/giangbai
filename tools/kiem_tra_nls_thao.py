import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

thao_dir = os.path.abspath("TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/NGUYEN THI THAO")
for f in os.listdir(thao_dir):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(os.path.join(thao_dir, f))
        if len(doc) == 45: # Số học 6
            print(f"Checking {f}...")
            for p_no in [30, 33, 34, 35, 36, 38, 39]:
                page = doc[p_no - 1]
                blocks = page.get_text("dict")["blocks"]
                print(f"\n--- TRANG {p_no} ---")
                for b in blocks:
                    if "lines" in b:
                        for l in b["lines"]:
                            line_text = "".join([s["text"] for s in l["spans"]])
                            if any(k in line_text for k in ['5.3', '3.1', 'NLS', 'Năng lực số', 'máy tính', 'Sơ đồ hóa']):
                                span_details = []
                                for s in l["spans"]:
                                    flags = s["flags"]
                                    font = s["font"]
                                    is_b = bool(flags & 16) or "bold" in font.lower()
                                    is_i = bool(flags & 2) or "italic" in font.lower() or "oblique" in font.lower()
                                    span_details.append(f"'{s['text']}' [bold={is_b}, italic={is_i}]")
                                print(" LINE:", line_text[:100])
                                print("   SPANS:", " | ".join(span_details[:4]))
