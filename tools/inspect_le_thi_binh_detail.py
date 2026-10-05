import os, sys, fitz, re

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"

def inspect_file(filename):
    path = os.path.join(folder, filename)
    doc = fitz.open(path)
    print(f"\n======================================================================")
    print(f"FILE: {filename}")
    print(f"PAGES: {len(doc)}")
    
    # 1. Lessons and Periods
    lessons_and_periods = []
    
    # 2. Check NLS & AI
    nls_ai_details = []
    
    # 3. Check math notation / encoding issues
    math_issues = []
    
    # Let's inspect page by page
    for p_no in range(len(doc)):
        page = doc[p_no]
        text = page.get_text()
        
        # Check lines for lesson / period
        for line in text.splitlines():
            line_str = line.strip()
            if re.search(r'(Tuần|Tiết|BÀI|Bài|CHỦ ĐỀ|Chủ đề)\s*[:\s]*\d+', line_str, re.IGNORECASE):
                if any(k in line_str.lower() for k in ['tuần', 'tiết', 'bài', 'chủ đề']) and len(line_str) < 100:
                    lessons_and_periods.append((p_no + 1, line_str))
                    
        # Check dict for NLS/AI
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    line_spans = l["spans"]
                    full_line_text = "".join([s["text"] for s in line_spans])
                    if any(k in full_line_text.lower() for k in ["năng lực số", "nls", "năng lực ai", "7.a", "7.b", "7.c", "8.a", "8.b", "8.c", "1.1.", "1.2.", "1.3.", "2.4.", "2.5.", "3.1.", "3.2.", "4.3.", "5.3."]):
                        # record this line and spans
                        span_info = []
                        for s in line_spans:
                            is_b = bool(s["flags"] & 16) or ("bold" in s["font"].lower())
                            is_it = bool(s["flags"] & 2) or ("italic" in s["font"].lower()) or ("oblique" in s["font"].lower())
                            span_info.append(f"['{s['text']}' font={s['font']} B={is_b} I={is_it}]")
                        nls_ai_details.append((p_no + 1, full_line_text, " ".join(span_info)))
                        
        # Check math symbols: angle symbol, weird dots above letters
        # Search for pattern like \u0227, \u1e41, or missing angle notation
        for line in text.splitlines():
            line_str = line.strip()
            # check weird letters like ṁ, ẋ, ẏ
            for ch in line_str:
                if ord(ch) in [0x0307, 0x0308, 0x0227, 0x1e41, 0x1e8b, 0x1e8f]:
                    math_issues.append((p_no + 1, f"Lỗi font góc thành dấu chấm: '{line_str}' (ký tự {ch} u+{ord(ch):04x})"))
                    break
            # check formula / geometry lines for questionable formulas
            if any(k in line_str for k in ['360°', '180°', 'Góc', 'góc', 'tứ giác', 'tam giác']):
                if any(bad in line_str for bad in ['H + E + F - G', '+ 360', '360 -']):
                    math_issues.append((p_no + 1, f"Nghi vấn toán học: {line_str}"))

    print("\n--- LESSONS & PERIODS DETECTED (Unique sample) ---")
    seen_lp = set()
    for p, lp in lessons_and_periods:
        if lp not in seen_lp and len(seen_lp) < 30:
            seen_lp.add(lp)
            print(f"  P{p}: {lp}")
            
    print(f"\n--- NLS / AI DETECTED: {len(nls_ai_details)} lines ---")
    for p, txt, span_str in nls_ai_details[:10]:
        print(f"  P{p}: {txt}")
        print(f"       -> {span_str[:160]}...")
        
    print(f"\n--- MATH / ENCODING ISSUES: {len(math_issues)} ---")
    for p, issue in math_issues[:15]:
        print(f"  P{p}: {issue}")

# Run for all files
files = [
    "HÌNH HỌC 7 - THÁNG 9 - LÊ THỊ BÌNH_1791190453648.pdf",
    "HÌNH HỌC 8 - THÁNG 9 - LÊ THỊ BÌNH_1791190454088.pdf",
    "HDTN 7 - THÁNG 9 - LÊ THỊ BÌNH_1791190454116.pdf",
    "ĐẠI SỐ 7 - THÁNG 9 - LÊ THỊ BÌNH_1791190453819.pdf",
    "ĐẠI SỐ 8 - THÁNG 9 - LÊ THỊ BÌNH_1791190453387.pdf"
]

for f in files:
    inspect_file(f)
