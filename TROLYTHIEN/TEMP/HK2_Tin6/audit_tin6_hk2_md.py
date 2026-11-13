# -*- coding: utf-8 -*-
import os
import re

MD_DIR = "TROLYTHIEN/TEMP/HK2_Tin6"
ILL_DIR = os.path.join(MD_DIR, "illustrations")

files = sorted([f for f in os.listdir(MD_DIR) if f.endswith(".md")])
print(f"=== BẮT ĐẦU AUDIT {len(files)} FILE MARKDOWN TIN HỌC 6 HK2 ===\n")

total_errors = 0

for filename in files:
    filepath = os.path.join(MD_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()

    file_errors = []

    # 1. Header chuẩn CV 5512 V2.1
    non_empty = [l.strip() for l in lines if l.strip()]
    if len(non_empty) < 3:
        file_errors.append("File quá ngắn.")
    else:
        line1, line2, line3 = non_empty[0], non_empty[1], non_empty[2]
        if not line1.startswith("**TIẾT"):
            file_errors.append(f"Dòng 1 sai chuẩn: '{line1[:40]}'")
        if not (line2.startswith("*Thời lượng thực hiện:") and line2.endswith("*")):
            file_errors.append(f"Dòng 2 sai chuẩn thời lượng: '{line2[:40]}'")
        if not line3.startswith("# I. MỤC TIÊU"):
            file_errors.append(f"Dòng 3 phải là '# I. MỤC TIÊU', thấy: '{line3[:40]}'")

    # 2. Kiểm tra Mục III không kèm phút
    for l in lines:
        if l.strip().startswith("# III. TIẾN TRÌNH DẠY HỌC"):
            if "(" in l or "phút" in l.lower():
                file_errors.append(f"Mục III chứa thời lượng: '{l.strip()}'")

    # 3. Kiểm tra Hoạt động con không chứa số tiết
    for l in lines:
        if l.strip().startswith("### Hoạt động"):
            if re.search(r"tiết\s*\d+", l, re.IGNORECASE):
                file_errors.append(f"Tiêu đề hoạt động chứa số tiết: '{l.strip()}'")

    # 4. Kiểm tra rò rỉ ****
    for idx, l in enumerate(lines, 1):
        if "****" in l:
            file_errors.append(f"Dòng {idx}: rò rỉ '****'")

    # 5. Kiểm tra lỗi cấm
    if "\\phantom" in content:
        file_errors.append("Chứa '\\phantom'")

    # 6. Kiểm tra tham chiếu ảnh minh họa
    ill_matches = re.findall(r"!\[(.*?)\]\((khbd-ill:.*?)\)", content)
    for alt, ref in ill_matches:
        img_id = ref.replace("khbd-ill:", "").strip()
        img_file = img_id.replace("-", "_") + ".png"
        img_path = os.path.join(ILL_DIR, img_file)
        if not os.path.exists(img_path):
            file_errors.append(f"Ảnh minh họa không tồn tại: id='{img_id}', file='{img_file}'")

    # 7. Đếm số từ
    word_count = len(content.split())

    if file_errors:
        print(f"[FAIL] {filename}:")
        for err in file_errors:
            print(f"   - {err}")
        total_errors += len(file_errors)
    else:
        print(f"[PASS] {filename} | Từ: {word_count} | Ảnh minh họa: {len(ill_matches)}")

print("\n" + "="*50)
if total_errors == 0:
    print(f"TẤT CẢ {len(files)} FILE MARKDOWN TIN HỌC 6 HK2 ĐẠT CHUẨN 100%!")
else:
    print(f"TỔNG SỐ LỖI CẦN SỬA: {total_errors}")
