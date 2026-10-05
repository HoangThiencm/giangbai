import os, sys, fitz, re

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"

files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]

def analyze_file(filename):
    path = os.path.join(folder, filename)
    doc = fitz.open(path)
    total_pages = len(doc)
    print(f"\n======================================================================")
    print(f"FILE: {filename}")
    print(f"TOTAL PAGES: {total_pages}")
    
    # Collect all headers/titles/weeks/periods
    week_period_lines = []
    nls_lines = []
    
    for p_no in range(total_pages):
        page = doc[p_no]
        text = page.get_text()
        
        # Check text lines for week / period / lesson
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        for l in lines:
            if re.search(r'(Tuần|Tiết|BÀI|Bài|CHỦ ĐỀ|Chủ đề)\s*[:\s]*\d+', l, re.IGNORECASE):
                if any(w in l.lower() for w in ['tuần', 'tiết', 'bài ', 'chủ đề ']):
                    week_period_lines.append((p_no + 1, l))
                    
        # Check spans for NLS / AI
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for line in b["lines"]:
                    spans = line["spans"]
                    line_text = "".join([s["text"] for s in spans]).strip()
                    # Check if line contains NLS or AI keywords
                    if any(k in line_text.lower() for k in ["năng lực số", "nls", "năng lực ai", "ai:", "tc1a", "tc1b", "tc2a", "tc2b", "7.a", "7.b", "7.c", "8.a", "8.b", "8.c", "1.1.", "1.2.", "1.3.", "2.4.", "2.5.", "3.1.", "3.2.", "4.3.", "5.3."]):
                        # evaluate bold / italic across the spans of this line
                        is_any_bold = any((s["flags"] & 16 or "bold" in s["font"].lower()) for s in spans)
                        is_any_italic = any((s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower()) for s in spans)
                        is_all_bi = all(((s["flags"] & 16 or "bold" in s["font"].lower()) and (s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower())) for s in spans if s["text"].strip())
                        
                        span_details = []
                        for s in spans:
                            b = bool(s["flags"] & 16 or "bold" in s["font"].lower())
                            it = bool(s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower())
                            span_details.append(f"[{s['text']} (B={b}, I={it})]")
                        nls_lines.append((p_no + 1, line_text, is_all_bi, " ".join(span_details)))

    print("\n--- ALL DETECTED WEEK / PERIOD / LESSON LINES ---")
    seen = set()
    for p, l in week_period_lines:
        if l not in seen:
            seen.add(l)
            print(f"  P{p}: {l}")

    print(f"\n--- ALL NLS / AI LINES ({len(nls_lines)}) ---")
    for p, txt, all_bi, span_dt in nls_lines:
        status = "ALL_BOLD_ITALIC" if all_bi else "NOT_ALL_BI"
        print(f"  P{p} [{status}]: {txt}")
        print(f"       Details: {span_dt[:160]}")

for f in sorted(files):
    analyze_file(f)
