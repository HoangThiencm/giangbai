import os
import re

MD_DIR = "TROLYTHIEN/TEMP/HK2_Toan9"
MINDMAP_DIR = os.path.join(MD_DIR, "mindmaps")

files = sorted([f for f in os.listdir(MD_DIR) if f.endswith(".md")])
print(f"Bắt đầu Audit Markdown Toán 9 HK2: {len(files)} tệp\n")

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
        file_errors.append("File quá ngắn hoặc thiếu nội dung header.")
    else:
        line1 = non_empty[0]
        line2 = non_empty[1]
        line3 = non_empty[2]

        if not (line1.startswith("**TIẾT") or line1.startswith("**CHỦ ĐỀ") or line1.startswith("**BÀI")):
            file_errors.append(f"Header dòng 1 sai format CV 5512: '{line1[:40]}'")
        if not (line2.startswith("*Thời lượng thực hiện:") and line2.endswith("*")):
            file_errors.append(f"Header dòng 2 sai format thời lượng: '{line2[:40]}'")
        if not line3.startswith("# I. MỤC TIÊU"):
            file_errors.append(f"Header dòng 3 phải là '# I. MỤC TIÊU', thấy: '{line3[:40]}'")

    # 2. Kiểm tra Mục III: # III. TIẾN TRÌNH DẠY HỌC (tuyệt đối không kèm phút)
    for l in lines:
        if l.strip().startswith("# III. TIẾN TRÌNH DẠY HỌC"):
            if "(" in l or "phút" in l.lower():
                file_errors.append(f"Mục III chứa thời lượng: '{l.strip()}'")

    # 3. Kiểm tra Hoạt động con không chứa số tiết
    for l in lines:
        if l.strip().startswith("### Hoạt động"):
            if re.search(r"tiết\s*\d+", l, re.IGNORECASE):
                file_errors.append(f"Tiêu đề hoạt động chứa số tiết: '{l.strip()}'")

    # 4. Kiểm tra cấm: phantom, \Leftrightarrow, S = \{...\}
    if "\\phantom" in content:
        file_errors.append("Chứa lỗi cấm '\\phantom'")
    if "\\Leftrightarrow" in content:
        file_errors.append("Chứa lỗi cấm '\\Leftrightarrow'")
    if re.search(r"\$S\s*=\s*\\\{", content) or re.search(r"S\s*=\s*\{", content):
        file_errors.append("Chứa kết luận tập nghiệm dạng cấm 'S = {...}'")

    # 5. Kiểm tra rò rỉ dấu sao Markdown
    for idx, l in enumerate(lines, 1):
        clean_l = re.sub(r"\$[^$]+\$", "", l)
        if "****" in clean_l:
            file_errors.append(f"Dòng {idx}: có 4 dấu sao liên tiếp '****': '{l.strip()[:50]}'")

    # 6. Kiểm tra tham chiếu Mindmap hình ảnh
    mm_matches = re.findall(r"!\[(.*?)\]\((khbd-ill:.*?)\)", content)
    for alt, ref in mm_matches:
        raw_id = ref.replace("khbd-ill:", "").strip()
        # Ánh xạ id sang tên file: thay '-' thành '_' và thêm '.png' nếu chưa có
        mapped_name = raw_id.replace("-", "_")
        if not mapped_name.endswith(".png"):
            mapped_name += ".png"
        img_path = os.path.join(MINDMAP_DIR, mapped_name)
        if not os.path.exists(img_path):
            file_errors.append(f"Mindmap ảnh không tồn tại: raw='{raw_id}', mapped='{mapped_name}'")

    if file_errors:
        print(f"[FAIL] {filename}:")
        for err in file_errors:
            print(f"   - {err}")
        total_errors += len(file_errors)
    else:
        print(f"[PASS] {filename} (Mindmaps: {len(mm_matches)})")

print("\n" + "="*50)
if total_errors == 0:
    print(f"TẤT CẢ {len(files)} FILE MARKDOWN TOÁN 9 HK2 ĐẠT CHUẨN 100%!")
else:
    print(f"TỔNG SỐ LỖI CẦN SỬA: {total_errors}")
