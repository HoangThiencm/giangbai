# -*- coding: utf-8 -*-
"""
Audit 45 tệp Markdown KHBD Toán 8 HK2 (Tuần 19 - 35)
Kiểm định hợp đồng hệ thống, chuẩn CV 5512 V2.1, 0 star leak, 0 phantom, 0 \Leftrightarrow, 0 S={...}
"""

import os
import re
import glob

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan8"
md_files = sorted(glob.glob(os.path.join(temp_dir, "*.md")))

print(f"Tổng số tệp Markdown cần kiểm tra: {len(md_files)}")

errors = []
mindmap_count = 0

for filepath in md_files:
    fname = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Header check
    lines = [line.strip() for line in content.split("\n") if line.strip()]
    if len(lines) < 3:
        errors.append(f"[{fname}] Tệp quá ngắn.")
        continue
    
    if not (lines[0].startswith("**TIẾT") or lines[0].startswith("TIẾT")):
        errors.append(f"[{fname}] Dòng 1 không phải TIẾT: {lines[0][:50]}")
    
    if not ("Thời lượng thực hiện:" in lines[1] or "Thời lượng thực hiện:" in lines[0]):
        errors.append(f"[{fname}] Thiếu Thời lượng thực hiện: {lines[1][:50]}")
        
    # 2. Mục III check
    if "# III. TIẾN TRÌNH DẠY HỌC" not in content:
        errors.append(f"[{fname}] Sai tiêu đề Mục III: Không khớp '# III. TIẾN TRÌNH DẠY HỌC'")
        
    # 3. Tiêu đề hoạt động con không được chứa "Tiết"
    act_matches = re.findall(r"^###\s+Hoạt động\s+.*$", content, re.MULTILINE)
    for act in act_matches:
        if "Tiết" in act or "tiết" in act:
            errors.append(f"[{fname}] Tiêu đề hoạt động con chứa từ 'Tiết': {act}")

    # 4. Forbidden patterns
    if r"\phantom" in content:
        errors.append(f"[{fname}] Chứa lệnh cấm \\phantom!")
    
    if r"\Leftrightarrow" in content or "⇔" in content:
        errors.append(f"[{fname}] Chứa dấu tương đương cấm \\Leftrightarrow!")
        
    if re.search(r"S\s*=\s*\\?\{", content):
        errors.append(f"[{fname}] Chứa kết luận tập nghiệm cấm S = {{...}}!")

    # 5. Star leak check
    clean = re.sub(r"\*\*\*.*?\*\*\*", "", content)
    clean = re.sub(r"\*\*.*?\*\*", "", clean)
    clean = re.sub(r"\*.*?\*", "", clean)
    if "*" in clean:
        leak_lines = [l for l in clean.split("\n") if "*" in l]
        # Ignore bullet points or markdown tables if any bare star
        # check if bare star
        real_leaks = [l for l in leak_lines if not l.strip().startswith("* ") and not l.strip().startswith("- ")]
        if real_leaks:
            errors.append(f"[{fname}] Rò rỉ dấu sao (*): {real_leaks[:2]}")

    # 6. Mindmaps
    mm_matches = re.findall(r"!\[Sơ đồ tư duy.*?\]\((khbd-ill:.*?)\)", content)
    if mm_matches:
        mindmap_count += len(mm_matches)

print(f"\nKiểm tra hoàn tất:")
print(f"- Số Mindmaps phát hiện: {mindmap_count}")
print(f"- Số lỗi phát hiện: {len(errors)}")

if errors:
    print("\nCÁC LỖI CẦN SỬA:")
    for err in errors:
        print(f"  X {err}")
else:
    print("\n>>> TẤT CẢ 45 TỆP MARKDOWN TOÁN 8 HK2 ĐẠT CHUẨN 100% (PASS AUDIT) <<<")
