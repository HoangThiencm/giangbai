import os, sys, fitz

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"
f_hh8 = [f for f in os.listdir(folder) if '1791212409278' in f][0]
doc = fitz.open(os.path.join(folder, f_hh8))
page5 = doc[4] # page 5

print("=== PAGE 5 TEXT OF HÌNH HỌC 8 ===")
print(page5.get_text())

print("\n=== PAGE 5 SPANS OF HÌNH HỌC 8 ===")
for b in page5.get_text("dict")["blocks"]:
    if "lines" in b:
        for l in b["lines"]:
            for s in l["spans"]:
                txt = s["text"]
                font = s["font"]
                if any(ord(c) > 127 for c in txt):
                    chars = [f"{c} (U+{ord(c):04X})" for c in txt if ord(c) > 127]
                    print(f"Font={font} | Text='{txt}' | Chars={chars[:5]}")
