import os
import re

MD_DIR = "TROLYTHIEN/TEMP/HK2_Toan9"
files = sorted([f for f in os.listdir(MD_DIR) if f.endswith(".md")])

print(f"Bắt đầu chuẩn hóa 39 file Markdown Toán 9 HK2...")

for filename in files:
    filepath = os.path.join(MD_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    new_lines = []
    first_non_empty_done = False

    for l in lines:
        stripped = l.strip()
        if not first_non_empty_done and stripped:
            first_non_empty_done = True
            # Chuẩn hóa dòng 1: bắt buộc **TIẾT ...**
            if not stripped.startswith("**"):
                # tìm xem có kết thúc bằng ** không
                text = stripped.strip("*")
                l = f"**{text}**"
        new_lines.append(l)

    content = "\n".join(new_lines)

    # 1. Khắc phục \Leftrightarrow
    # Thay \Leftrightarrow bằng \Rightarrow hoặc suy ra
    content = content.replace(r"\Leftrightarrow", r"\Rightarrow")

    # 2. Khắc phục cấm $S = \{...\}$
    content = re.sub(r"\$S\s*=\s*\\\{([^}]+)\\\}\$", r"nghiệm $x = \1$", content)
    content = re.sub(r"S\s*=\s*\{([^}]+)\}", r"nghiệm $x = \1$", content)

    # 3. Khắc phục phantom nếu có
    content = content.replace(r"\phantom{x}", "")
    content = content.replace(r"; phantom x.", "")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Đã hoàn tất chuẩn hóa 39 file Markdown Toán 9 HK2.")
