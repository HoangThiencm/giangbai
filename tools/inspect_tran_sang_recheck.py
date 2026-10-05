import os, sys, fitz, docx, re

sys.stdout.reconfigure(encoding='utf-8')

ts_folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG"
files = os.listdir(ts_folder)
print("=== FILES IN TRAN SANG FOLDER ===")
for f in files:
    print(" -", f)

# 1. Check PL3 Toan 6 for Week 4 (Tiet 10, 11, 12 in So 6 and Tiet 4 in Hinh 6)
pl3_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/Phu-luc-3-Toan 6.docx"
if os.path.exists(pl3_path):
    print("\n=== CHECKING PL3 TOAN 6 FOR WEEK 4 ===")
    doc_pl3 = docx.Document(pl3_path)
    for t_idx, t in enumerate(doc_pl3.tables):
        for r_idx, r in enumerate(t.rows):
            line = " | ".join([c.text.strip().replace('\n', ' ') for c in r.cells])
            if any(k in line.lower() for k in ['tuần 4', 'tiết 10', 'tiết 11', 'tiết 12', 'tiết 4', 'bài 7', 'bài 19']):
                dedup = []
                for c in r.cells:
                    txt = c.text.strip().replace('\n', ' ')
                    if not dedup or txt != dedup[-1]:
                        dedup.append(txt)
                print(f"  [T{t_idx+1} R{r_idx}]", " | ".join(dedup))

# 2. Inspect the PDF files
def inspect_pdf(f_name):
    f_path = os.path.join(ts_folder, f_name)
    doc = fitz.open(f_path)
    total_pages = len(doc)
    print(f"\n=======================================================")
    print(f"FILE: {f_name}")
    print(f"TOTAL PAGES: {total_pages}")
    
    lessons = []
    periods = []
    nls_hits = []
    
    pattern = re.compile(r'(năng lực số|năng lực ai|\b\d\.[A-Z]\d\.\d\b|\b\d\.\d\.tc[12][ab]\b|\bnls\b)', re.IGNORECASE)
    
    for p_no in range(total_pages):
        page = doc[p_no]
        text = page.get_text()
        
        # Check lessons / periods
        for l in text.splitlines():
            ls = l.strip()
            if re.search(r'(Tuần|Tiết|BÀI|Bài)\s*[:\s]*\d+', ls, re.IGNORECASE) and len(ls) < 100:
                if any(w in ls.lower() for w in ['tuần', 'tiết', 'bài 7', 'bài 19', 'luyện tập chung']):
                    if ls not in lessons:
                        lessons.append(ls)
                        
        # Check NLS / AI
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for line in b["lines"]:
                    spans = line["spans"]
                    line_txt = "".join([s["text"] for s in spans]).strip()
                    if pattern.search(line_txt):
                        span_details = []
                        for s in spans:
                            txt = s["text"].strip()
                            if txt:
                                b_val = bool(s["flags"] & 16 or "bold" in s["font"].lower())
                                it_val = bool(s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower())
                                span_details.append((txt, b_val, it_val))
                        all_bi = all((b_val and it_val) for txt, b_val, it_val in span_details)
                        nls_hits.append((p_no + 1, line_txt, all_bi, span_details))
                        
    print("--- DETECTED LESSONS / PERIODS ---")
    for l in lessons[:25]:
        print("  ", l)
        
    print(f"--- NLS / AI MATCHES ({len(nls_hits)}) ---")
    for p, txt, all_bi, spans in nls_hits[:15]:
        status = "ALL_BOLD_ITALIC" if all_bi else "NOT_ALL_BI"
        print(f"  P{p} [{status}]: {txt}")
        for t, b, it in spans:
            if pattern.search(t) or any(k in t.lower() for k in ["nls", "năng lực", "tc1a", "tc2a", "3.1"]):
                print(f"       -> '{t}' | Bold={b}, Italic={it}")

for f in files:
    if f.endswith('.pdf'):
        inspect_pdf(f)
