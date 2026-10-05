import os, sys, fitz, re

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"

files = [f for f in os.listdir(folder) if f.endswith('.pdf')]

pattern = re.compile(r'(năng lực số|năng lực ai|\b\d\.[A-Z]\d\.\d\b|\b\d\.\d\.tc[12][ab]\b|\bnls\b)', re.IGNORECASE)

for f in files:
    doc = fitz.open(os.path.join(folder, f))
    print(f"\n=======================================================")
    print(f"FILE: {f} ({len(doc)} pages)")
    hits = []
    for p_no in range(len(doc)):
        page = doc[p_no]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    spans = l["spans"]
                    line_txt = "".join([s["text"] for s in spans]).strip()
                    if pattern.search(line_txt):
                        # check spans bold/italic
                        span_details = []
                        for s in spans:
                            txt = s["text"].strip()
                            if txt:
                                b_val = bool(s["flags"] & 16 or "bold" in s["font"].lower())
                                it_val = bool(s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower())
                                span_details.append((txt, b_val, it_val))
                        all_bi = all((b_val and it_val) for txt, b_val, it_val in span_details)
                        hits.append((p_no + 1, line_txt, all_bi, span_details))
    print(f"Total NLS/AI lines matched: {len(hits)}")
    for p_no, l_txt, all_bi, spans in hits:
        bi_label = "ALL_BOLD_ITALIC" if all_bi else "NOT_ALL_BI"
        print(f"  P{p_no} [{bi_label}]: {l_txt}")
        for t, b, it in spans:
            if pattern.search(t) or any(k in t.lower() for k in ["nls", "năng lực", "tc1a", "tc2a", "7.a", "5.3"]):
                print(f"       -> '{t}' | Bold={b}, Italic={it}")

