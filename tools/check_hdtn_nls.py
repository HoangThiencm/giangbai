import os, sys, fitz

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"

def inspect_hdtn():
    for f in os.listdir(folder):
        if 'HDTN' in f.upper():
            doc = fitz.open(os.path.join(folder, f))
            print(f"=== CHECKING HDTN 7: {f} ({len(doc)} pages) ===")
            for p_no in range(len(doc)):
                page = doc[p_no]
                blocks = page.get_text("dict")["blocks"]
                for b in blocks:
                    if "lines" in b:
                        for l in b["lines"]:
                            spans = l["spans"]
                            txt = "".join([s["text"] for s in spans]).strip()
                            if any(k in txt.lower() for k in ["nls", "năng lực số", "ai", "trí tuệ", "7.a", "7.b", "1.1.", "2.4.", "2.5.", "3.1.", "3.3.", "4.2."]):
                                is_b = all(bool(s["flags"] & 16 or "bold" in s["font"].lower()) for s in spans if s["text"].strip())
                                is_it = all(bool(s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower()) for s in spans if s["text"].strip())
                                print(f"P{p_no+1} [B={is_b}, IT={is_it}]: {txt}")

inspect_hdtn()
