# -*- coding: utf-8 -*-
import os, glob, re, sys

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\TEMP\02.11"
md_files = sorted(glob.glob(os.path.join(TEMP_DIR, "*.md")))

for fpath in md_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_nls_section = False
    in_ai_section = False

    for line in lines:
        stripped = line.strip()

        # Phát hiện mục NLS và AI trong Mục tiêu
        if re.search(r'c\)\s*Năng lực số', stripped, re.I):
            in_nls_section = True
            in_ai_section = False
            new_lines.append(line)
            continue
        elif re.search(r'd\)\s*Năng lực Trí tuệ Nhân tạo', stripped, re.I):
            in_nls_section = False
            in_ai_section = True
            new_lines.append(line)
            continue
        elif re.search(r'^(?:##|\d+\.|\b[a-z]\))\s+', stripped) and not stripped.startswith(('c)', 'd)')):
            in_nls_section = False
            in_ai_section = False

        # Xử lý dòng chỉ báo trong mục NLS
        if in_nls_section and stripped.startswith(('-', '*', '+')):
            # Làm sạch mọi dấu sao cũ
            clean_text = re.sub(r'^\s*[-*+]\s*', '', stripped)
            clean_text = clean_text.replace('***', '').replace('**', '').replace('*', '').strip()
            # Bọc lại thành - ***[Mã]: [Nội dung]***
            new_lines.append(f"- ***{clean_text}***\n")
            continue

        # Xử lý dòng chỉ báo trong mục AI
        if in_ai_section and stripped.startswith(('-', '*', '+')):
            clean_text = re.sub(r'^\s*[-*+]\s*', '', stripped)
            clean_text = clean_text.replace('***', '').replace('**', '').replace('*', '').strip()
            new_lines.append(f"- ***{clean_text}***\n")
            continue

        # Xử lý các dòng trong bảng hoặc hoạt động
        # Tìm và chuẩn hóa các bước dạy học trong bảng: + Bước 1, + Bước 2...
        line_processed = line
        line_processed = re.sub(r'(?<!\*\*)\+\s*Bước\s*(\d)[:：]?(?!\*\*)', r'**+ Bước \1:**', line_processed)

        # Chuẩn hóa các đoạn tích hợp NLS và AI
        # Tìm các chuỗi có dạng Tích hợp NLS hoặc Tích hợp AI
        def clean_integration_inline(m):
            snippet = m.group(0)
            # Gỡ bỏ các dấu ngoặc hoặc sao thừa
            clean = re.sub(r'^\s*[-*+]*\s*\(?\s*\**\s*', '', snippet)
            clean = re.sub(r'\s*\**\s*\)?\s*$', '', clean)
            clean = clean.replace('***', '').replace('**', '').strip()
            # Bọc lại chuẩn: ***Tích hợp NLS/AI...***
            return f"***{clean}***"

        line_processed = re.sub(
            r'[-*+]?\s*\*{0,3}\s*\(?\s*Tích hợp\s+(?:NLS|AI)[^\n\r<|]*?\)?\s*\*{0,3}',
            clean_integration_inline,
            line_processed,
            flags=re.IGNORECASE
        )

        # Sửa các từ dính dạng ***(Tích hợp NLS***
        line_processed = re.sub(r'\*\*\*\s*\(?\s*Tích hợp\s+(NLS|AI)\s*\*\*\*', r'***Tích hợp \1:', line_processed)
        # Sửa đóng ngoặc thừa: ).*** thành .***
        line_processed = re.sub(r'\)\.\*\*\*', r'.***', line_processed)
        line_processed = re.sub(r'\)\*\*\*', r'***', line_processed)

        new_lines.append(line_processed)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f" -> Đã làm sạch: {fname}")

print("HOÀN TẤT LÀM SẠCH 10 FILE!")
