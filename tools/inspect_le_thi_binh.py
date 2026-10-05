import os
import sys
import fitz # PyMuPDF
import re

sys.stdout.reconfigure(encoding='utf-8')

folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"
files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]

print(f"Found {len(files)} PDF files for Cô Lê Thị Bình:")
for f in files:
    print(" -", f)

def analyze_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"\n=======================================================")
    print(f"FILE: {os.path.basename(pdf_path)}")
    print(f"TOTAL PAGES: {total_pages}")
    
    # Track lessons, periods, NLS/AI occurrences
    lessons = []
    periods = []
    nls_ai_hits = []
    math_issues = []
    
    full_text = []
    
    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text()
        full_text.append(text)
        
        # Check text blocks/spans for NLS / AI
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        span_text = s["text"]
                        font_name = s["font"]
                        flags = s["flags"]
                        is_bold = bool(flags & 16) or ("bold" in font_name.lower())
                        is_italic = bool(flags & 2) or ("italic" in font_name.lower()) or ("oblique" in font_name.lower())
                        
                        # Check NLS / AI indicators
                        if any(k in span_text.lower() for k in ["nls", "năng lực số", "ai", "trí tuệ nhân tạo", "1.1.", "1.2.", "1.3.", "2.4.", "2.5.", "3.1.", "3.2.", "4.3.", "5.3.", "7.a", "7.b", "7.c", "8.a", "8.b", "8.c", "tc1a", "tc1b", "tc2a", "tc2b"]):
                            nls_ai_hits.append({
                                "page": page_num + 1,
                                "text": span_text,
                                "font": font_name,
                                "is_bold": is_bold,
                                "is_italic": is_italic,
                                "flags": flags
                            })
        
        # Detect lesson titles
        for line in text.splitlines():
            line_str = line.strip()
            # Lesson match
            if re.match(r'^(BÀI|Bài|CHỦ ĐỀ|Chủ đề)\s+\d+', line_str, re.IGNORECASE):
                if line_str not in lessons:
                    lessons.append((page_num + 1, line_str))
            # Period match
            if re.search(r'(Tiết|TIẾT)\s*[:\d\-–]+', line_str):
                # match specific lines like "Tiết 1:", "Tiết 1, 2", "Tiết: 10"
                m = re.findall(r'(?:Tiết|TIẾT)\s*[:\s]*(\d+(?:\s*[,–\-]\s*\d+)?)', line_str)
                for p in m:
                    if (page_num + 1, p) not in periods:
                        periods.append((page_num + 1, p, line_str[:60]))
                        
        # Check potential math issues (especially in geometry)
        # e.g., missing hat on angle, weird dots on top of letters, incorrect formulas
        # Check for dots above letters like \u0227, \u1e41, etc.
        for char in text:
            if ord(char) in [0x0307, 0x0308, 0x0227, 0x1e41]: # dot above
                math_issues.append((page_num + 1, f"Ký hiệu lạ có dấu chấm: {char} (code {hex(ord(char))})"))

    print("\n--- DETECTED LESSONS ---")
    for p, l in lessons[:20]:
        print(f"  Page {p}: {l}")
        
    print("\n--- DETECTED PERIODS (sample) ---")
    for p, per, l_str in periods[:20]:
        print(f"  Page {p}: Tiết {per} -> {l_str}")
        
    print(f"\n--- NLS / AI HITS: {len(nls_ai_hits)} ---")
    for hit in nls_ai_hits[:15]:
        b_it_str = f"Bold: {hit['is_bold']}, Italic: {hit['is_italic']}"
        print(f"  Page {hit['page']}: [{b_it_str}] Font={hit['font']} | Text='{hit['text']}'")
        
    if math_issues:
        print(f"\n--- MATH / ENCODING ISSUES: {len(math_issues)} ---")
        for m in math_issues[:10]:
            print(f"  Page {m[0]}: {m[1]}")

for f in files:
    analyze_pdf(os.path.join(folder, f))
