import os, sys, fitz

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG"
f_so6 = [f for f in os.listdir(folder) if '1791200844100' in f][0]
doc = fitz.open(os.path.join(folder, f_so6))
page = doc[43] # page 44
print("Page 44 spans for NLS:")
for b in page.get_text("dict")["blocks"]:
    if "lines" in b:
        for l in b["lines"]:
            for s in l["spans"]:
                txt = s["text"].strip()
                if any(k in txt.lower() for k in ["năng lực số", "5.3", "3.1", "nls"]):
                    b_val = bool(s["flags"] & 16 or "bold" in s["font"].lower())
                    it_val = bool(s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower())
                    print(f"  font={s['font']} B={b_val} I={it_val} | '{txt}'")

print("\nPage 47 spans for NLS:")
page47 = doc[46]
for b in page47.get_text("dict")["blocks"]:
    if "lines" in b:
        for l in b["lines"]:
            for s in l["spans"]:
                txt = s["text"].strip()
                if any(k in txt.lower() for k in ["nls", "2.1", "năng lực"]):
                    b_val = bool(s["flags"] & 16 or "bold" in s["font"].lower())
                    it_val = bool(s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower())
                    print(f"  font={s['font']} B={b_val} I={it_val} | '{txt}'")
