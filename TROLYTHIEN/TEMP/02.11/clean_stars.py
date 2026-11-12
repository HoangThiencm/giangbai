# -*- coding: utf-8 -*-
import os, re, glob, sys

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\TEMP\02.11"
md_files = sorted(glob.glob(os.path.join(TEMP_DIR, "*.md")))

for fpath in md_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Xóa bỏ các cặp ** bên trong ***...***
    def clean_nested_stars(m):
        full = m.group(0)
        inner = m.group(1)
        # Xóa mọi ** bên trong
        cleaned_inner = inner.replace('**', '')
        return f"***{cleaned_inner}***"

    text = re.sub(r'\*\*\*([\s\S]+?)\*\*\*', clean_nested_stars, text)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Đã làm sạch toàn bộ dấu sao lồng nhau!")
