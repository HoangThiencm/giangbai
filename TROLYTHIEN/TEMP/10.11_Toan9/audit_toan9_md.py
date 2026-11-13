# -*- coding: utf-8 -*-
import os
import re
import glob

DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/10.11_Toan9"
files = sorted(glob.glob(os.path.join(DIR, "*.md")))

print(f"Kiểm tra {len(files)} tệp markdown Toán 9:")

passed = 0
for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    
    errors = []
    # 1. phantom
    if r"\phantom" in text:
        errors.append("Có chứa \\phantom")
    
    # 2. Leftrightarrow
    if r"\Leftrightarrow" in text:
        errors.append("Có chứa \\Leftrightarrow")
    
    # 3. S = {
    if re.search(r"S\s*=\s*\\?\{", text):
        errors.append("Có chứa tập nghiệm S = {...}")
        
    # 4. Heading III check
    lines = text.splitlines()
    for l in lines:
        if l.startswith("# III."):
            if l.strip() != "# III. TIẾN TRÌNH DẠY HỌC":
                errors.append(f"Tiêu đề mục III sai quy chuẩn: {l.strip()}")
                
    # 5. Check activity headings with "Tiết"
    for l in lines:
        if re.match(r"^#{2,4}\s+(Hoạt động|A\.|B\.|C\.|D\.).*Tiết\s+\d+", l, re.IGNORECASE):
            errors.append(f"Tiêu đề hoạt động chứa số tiết: {l.strip()}")
            
    # 6. Star leaks check
    star_triples = len(re.findall(r"\*\*\*", text))
    if star_triples % 2 != 0:
        errors.append(f"Lỗi rò rỉ dấu sao ***: số lượng lẻ ({star_triples})")
        
    # 7. Check mindmap references
    mm_refs = re.findall(r"!\[.*?\]\(khbd-ill:(.*?)\)", text)
    for ref in mm_refs:
        img_name = ref.replace("-", "_") + ".png"
        img_path = os.path.join(DIR, "mindmaps", img_name)
        if not os.path.exists(img_path):
            errors.append(f"Mindmap không tồn tại: {img_name}")
            
    if errors:
        print(f"[FAIL] {fname}:")
        for err in errors:
            print(f"   - {err}")
    else:
        passed += 1
        print(f"[PASS] {fname}")

print(f"\nTổng kết: {passed}/{len(files)} files đạt chuẩn markdown!")
