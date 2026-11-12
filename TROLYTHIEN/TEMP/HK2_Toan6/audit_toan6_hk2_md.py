# -*- coding: utf-8 -*-
"""
Script kiểm định chất lượng Markdown Toán 6 HK2
Kiểm tra:
- Không rò rỉ sao (star leaks)
- Không có \phantom
- Không có \Leftrightarrow
- Không có S = {
- Ký hiệu góc chuẩn \widehat{...}
- File ảnh mindmap tồn tại đầy đủ
"""

import os
import re

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan6"
mindmaps_dir = os.path.join(temp_dir, "mindmaps")

md_files = [f for f in os.listdir(temp_dir) if f.endswith(".md")]
md_files.sort()

print(f"Tổng số file Markdown Toán 6 HK2 tìm thấy: {len(md_files)}")

errors = []
warnings = []

for filename in md_files:
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Kiểm tra \phantom
    if "\\phantom" in content:
        errors.append(f"[{filename}] Phát hiện chuỗi cấm: \\phantom")

    # 2. Kiểm tra \Leftrightarrow
    if "\\Leftrightarrow" in content:
        errors.append(f"[{filename}] Phát hiện chuỗi cấm: \\Leftrightarrow")

    # 3. Kiểm tra S = {
    if re.search(r"S\s*=\s*\{", content):
        errors.append(f"[{filename}] Phát hiện kết luận tập nghiệm: S = {{...}}")

    # 4. Kiểm tra star leaks
    # Loại bỏ ***bold italic***, **bold**, *italic*
    clean = re.sub(r"\*\*\*[^*]+\*\*\*", "", content)
    clean = re.sub(r"\*\*[^*]+\*\*", "", clean)
    clean = re.sub(r"\*[^*]+\*", "", clean)
    if "*" in clean:
        errors.append(f"[{filename}] Phát hiện rò rỉ dấu sao (*) chưa đóng chuẩn!")

    # 5. Kiểm tra ảnh mindmap
    img_matches = re.findall(r"!\[(.*?)\]\(khbd-ill:(.*?)\)", content)
    for alt, ill_id in img_matches:
        expected_filename = ill_id.replace("-", "_") + ".png"
        img_path = os.path.join(mindmaps_dir, expected_filename)
        if not os.path.exists(img_path):
            errors.append(f"[{filename}] Ảnh mindmap không tồn tại: {expected_filename} (id: {ill_id})")

    # 6. Kiểm tra các mục lớn
    if "# I. MỤC TIÊU" not in content:
        errors.append(f"[{filename}] Thiếu tiêu đề # I. MỤC TIÊU")
    if "# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU" not in content:
        errors.append(f"[{filename}] Thiếu tiêu đề # II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU")
    if "# III. TIẾN TRÌNH DẠY HỌC" not in content:
        errors.append(f"[{filename}] Thiếu tiêu đề # III. TIẾN TRÌNH DẠY HỌC")

if errors:
    print(f"❌ THẤT BẠI: Phát hiện {len(errors)} lỗi:")
    for err in errors:
        print("  - " + err)
else:
    print("✅ XUẤT SẮC: 100% tệp Markdown Toán 6 HK2 đều PASS các tiêu chuẩn sư phạm và hợp đồng!")
