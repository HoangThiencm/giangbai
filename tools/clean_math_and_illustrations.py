# -*- coding: utf-8 -*-
import os, glob, re

base_dir = r"TROLYTHIEN/1_SOAN_KHBD/Ket_qua"
files = sorted(glob.glob(os.path.join(base_dir, "*.md")))

# Danh sách minh họa không cần thiết (chỉ giữ mindmap cho bài ôn tập / luyện tập chung)
unneeded_ills = [
    "hinh-01-hop-chu-nhat-152",
    "hinh-03-tinh-chat-chia-het",
    "hinh-04-dau-hieu-chia-het",
    "hinh-05-sang-eratosthenes",
    "hinh-07-quy-trinh-tim-ucln",
    "hinh-08-quy-trinh-tim-bcnn"
]

for fpath in files:
    with open(fpath, "r", encoding="utf-8") as fp:
        c = fp.read()

    # 1. Xóa toàn bộ ký tự điều khiển (control characters)
    c = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", c)

    # 2. Xóa các hình minh họa không cần thiết
    for ill in unneeded_ills:
        c = re.sub(r"!\[[^\]]*\]\(khbd-ill:" + re.escape(ill) + r"\)(?:<br\s*/?>)*", "", c)

    # 3. Chuẩn hóa công thức chia hết triệt để
    # Biến mọi dạng "\ dots \", "\vdots\", "\ \vdots \", "dots" trong ngữ cảnh chia hết thành "\vdots"
    # Dấu không chia hết:
    c = re.sub(r"\\+\s*not\s*\\+\s*(?:dots|vdots)", r"\\not\\vdots", c)
    c = re.sub(r"\\+\s*not\s*dots", r"\\not\\vdots", c)
    c = re.sub(r"\\+\s*not\s*\\+\s*mid", r"\\not\\vdots", c)
    c = re.sub(r"\\\s*not\\vdots\s*\\?", r"\\not\\vdots", c)

    # Dấu chia hết:
    c = re.sub(r"\\\s*dots\s*\\", r"\\vdots", c)
    # Dọn sạch triệt để các vết \v hoặc \v \vdots bị sót
    c = re.sub(r"\\+v+\s*\\*vdots", r"\\vdots", c)
    c = re.sub(r"(?<=[0-9a-zA-Z\)])\s*(?:\\dots|\bdots\b)\s*(?=[0-9a-zA-Z\(])", r" \\vdots ", c)

    # Các trường hợp cụ thể:
    c = c.replace("36 \\ dots \\ x", "36 \\vdots x")
    c = c.replace("48 \\ dots \\ x", "48 \\vdots x")
    c = c.replace("36 dots x", "36 \\vdots x")
    c = c.replace("48 dots x", "48 \\vdots x")
    c = c.replace("110 \\ dots \\ 55", "110 \\vdots 55")
    c = c.replace("24 \\ dots \\ 8", "24 \\vdots 8")

    # Dọn dẹp khoảng cách và thẻ <br> lặp
    c = re.sub(r"(?:<br\s*/?>\s*){3,}", "<br><br>", c)
    c = re.sub(r"\|\s*<br\s*/?>\s*", "| ", c)

    with open(fpath, "w", encoding="utf-8") as fp:
        fp.write(c)

    print("Processed:", os.path.basename(fpath))

print("ALL FILES CLEANED AND NORMALIZED!")
