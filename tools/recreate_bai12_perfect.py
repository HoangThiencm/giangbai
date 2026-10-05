import subprocess
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_path = 'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'
print(f"Recreating {target_path} completely fresh from git HEAD and applying all modern standards...")

# 1. Lấy nội dung gốc từ git HEAD
cmd = ['git', 'show', 'HEAD:TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html']
content = subprocess.check_output(cmd, encoding='utf-8')
print(f"Loaded {len(content)} characters from git HEAD.")

# 2. Sửa toàn bộ lỗi tab corrupt trong LaTeX
TAB_REPLACEMENTS = [
    ('\tan', r'\tan'),
    ('\text', r'\text'),
    ('\times', r'\times'),
    ('\theta', r'\theta'),
    ('\tau', r'\tau')
]
for bad, good in TAB_REPLACEMENTS:
    if bad in content:
        c = content.count(bad)
        content = content.replace(bad, good)
        print(f"  Fixed {c} corrupted tab escapes for {repr(good)}")

# 3. Đảm bảo CSS khóa cuộn khi vẽ bút
if 'body.pen-mode, body.pen-mode .slide-deck' not in content:
    target = '.pen-palette.active { display: flex; }'
    if target in content:
        content = content.replace(target, target + '\n    body.pen-mode, body.pen-mode .slide-deck { overflow: hidden !important; }\n')
        print("  Added pen-mode scroll lock CSS.")

# 4. Đảm bảo Bảng viết nằm trên thanh công cụ và gỡ khỏi chuột phải
# Thanh công cụ:
btn_board_html = '<button class="btn-ctrl" id="btnBoard" onclick="toggleBlackboard()" title="Bảng viết vẽ toàn màn hình & Chèn ảnh (Phím W)">📋 Bảng viết</button>'
if 'id="btnBoard"' not in content:
    if '<button class="btn-ctrl" id="btnTimer"' in content:
        content = content.replace(
            '<button class="btn-ctrl" id="btnTimer"',
            btn_board_html + '\n    <button class="btn-ctrl" id="btnTimer"'
        )
        print("  Added btnBoard to control bar.")

# Gỡ blackboard khỏi contextMenu
content = re.sub(
    r'<div class="ctx-item"\s+onclick="handleCtxAction\(\'blackboard\'\)">[\s\S]*?</div>',
    '',
    content
)
print("  Removed blackboard from contextMenu (screen-only tools retained).")

# 5. Đảm bảo giao diện bảng viết có đầy đủ chức năng chèn và kéo thả ảnh
if 'id="boardImageBox"' not in content:
    print("  [WARN] boardImageBox not in content, verifying...")

# 6. Đổi tiêu đề tinh gọn theo TITLE_MAPPINGS
TITLE_MAPPINGS = {
    # Hướng dẫn & lời giải
    "HƯỚNG DẪN GIẢI TỪNG BƯỚC": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (CHUẨN GDPT 2018)": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (CHUẨN SGK)": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT": "HƯỚNG DẪN",
    "HƯỚNG DẪN THỰC HIỆN CÂU A": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (2 CÁCH TÍNH CẠNH BC)": "HƯỚNG DẪN",

    # Đề bài & Hoạt động
    "HOẠT ĐỘNG 1 (SGK TR.74)": "HOẠT ĐỘNG 1",
    "HOẠT ĐỘNG 2 (SGK TR.75)": "HOẠT ĐỘNG 2",

    # Ví dụ & Luyện tập
    "LUYỆN TẬP 4 (SGK TR.77)": "LUYỆN TẬP 4",
    "BÀI TẬP VẬN DỤNG NHANH TẠI LỚP (30 GIÂY)": "VẬN DỤNG",

    # Câu hỏi & đáp án
    "CÂU HỎI TRẮC NGHIỆM 1": "TRẮC NGHIỆM 1",
    "CÂU HỎI TRẮC NGHIỆM 2": "TRẮC NGHIỆM 2",

    # Tình huống & hình
    "TÌNH HUỐNG MỞ ĐẦU (SGK TR.74)": "TÌNH HUỐNG",
    "HÌNH 4.11 — MÔ HÌNH QUAN SÁT THỰC ĐỊA": "HÌNH 4.11",
    "HÌNH 4.11 — MÔ HÌNH TOÁN HỌC": "HÌNH 4.11",
    "HÌNH 4.12 — TAM GIÁC VUÔNG ABC": "HÌNH 4.12",
    "HÌNH 4.13 — MÔ HÌNH HÌNH HỌC": "HÌNH 4.13",
    "HÌNH 4.14 — CHIẾC THANG GÓC 65°": "HÌNH 4.14",
    "HÌNH 4.15 — CON ĐÒ QUA KHÚC SÔNG": "HÌNH 4.15",
    "HÌNH 4.16 — TAM GIÁC VUÔNG VỚI HAI CẠNH GÓC VUÔNG": "HÌNH 4.16",
    "HÌNH 4.17 — TÒA THÁP VÀ BÓNG NẮNG 8,6 M": "HÌNH 4.17",
    "HÌNH 4.18 — BÓNG CÂY 25 M DƯỚI GÓC 40°": "HÌNH 4.18",
    "HÌNH 4.19 — TAM GIÁC ABC CÓ AB = 5, AC = 8": "HÌNH 4.19",
    "HÌNH 4.20 — TAM GIÁC ABC CÓ AB = 3 VÀ GÓC B = 42°": "HÌNH 4.20",
    "HÌNH 4.22 — XE CHỞ RÁC NÂNG THÙNG BEN": "HÌNH 4.22",
    "HÌNH 4.23 — MÔ HÌNH MÁI DỐC NHÀ KHO": "HÌNH 4.23",
    "HÌNH VẼ MINH HỌA CHO A = 10, B = 6": "HÌNH VẼ",
    "HÌNH VẼ MINH HỌA HÌNH THOI": "HÌNH VẼ",

    # Lý thuyết & phương pháp
    "MỤC TIÊU BÀI HỌC (3 TIẾT)": "MỤC TIÊU",
    "SƠ ĐỒ TƯ DUY PHÂN TÍCH ĐI LÊN": "PHÂN TÍCH",
    "NHẬN XÉT SƯ PHẠM VỀ VỊ TRÍ GÓC": "NHẬN XÉT",
    "ĐỊNH HƯỚNG CHUYỂN THÀNH ĐỊNH LÍ PHÁT BIỂU BẰNG LỜI": "KẾT LUẬN",
    "ĐỊNH HƯỚNG PHÁT BIỂU ĐỊNH LÍ 2": "KẾT LUẬN",
    "MẸO GHI NHỚ SƯ PHẠM ĐỘC QUYỀN": "GHI NHỚ",
    "BẢNG CHUYỂN ĐỔI KHI ĐỔI TÊN ĐỈNH TAM GIÁC": "BẢNG CHUYỂN ĐỔI",
    "TỈ SỐ TANG & CÔTANG TRONG TAM GIÁC ABC": "TỈ SỐ LƯỢNG GIÁC",
    "BIỂU DIỄN CẠNH GÓC VUÔNG QUA CẠNH GÓC VUÔNG KIA": "BIỂU DIỄN CẠNH",
    "PHÂN TÍCH VỊ TRÍ GÓC ĐỐI VÀ GÓC KỀ": "VỊ TRÍ GÓC",
    "CÔNG THỨC TÍNH CÔTANG TRÊN MÁY TÍNH CẦM TAY": "TÍNH CÔTANG",
    "BẢNG ĐỐI CHIẾU HỆ THỨC LƯỢNG": "BẢNG ĐỐI CHIẾU",
    "SƠ ĐỒ CÂY QUYẾT ĐỊNH CHỌN ĐỊNH LÍ": "SƠ ĐỒ QUYẾT ĐỊNH",
    "GIẢI TAM GIÁC VUÔNG LÀ GÌ? (SGK TR.77)": "ĐỊNH NGHĨA",
    "HAI TRƯỜNG HỢP CƠ BẢN": "HAI TRƯỜNG HỢP",
    "CÔNG CỤ TOÁN HỌC CẦN SỬ DỤNG KHI GIẢI": "CÔNG CỤ",
    "CÁC TRỤ CỘT KIẾN THỨC CỐT LÕI": "TRỌNG TÂM",

    # Casio
    "MẸO BẤM MÁY FX-580VN X & CẢNH BÁO": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & AN TOÀN LAO ĐỘNG": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & NGUYÊN LÝ ĐO BÓNG NẮNG": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO LÀM TRÒN": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & BỘ BA SỐ PYTHAGORE": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO DÂY CHUYỀN": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & LƯU Ý LÀM TRÒN .0": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO GIÁC KẾ": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & KỸ THUẬT XE BEN": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & NGUYÊN LÝ THOÁT NƯỚC": "HƯỚNG DẪN CASIO",
    "MẸO CASIO & CẢNH BÁO NHÂN ĐÔI GÓC": "HƯỚNG DẪN CASIO",

    # Bài tập & tổng kết
    "TỔNG KẾT TIẾT 1 & DẶN DÒ": "DẶN DÒ",
    "TỔNG KẾT TIẾT 2 & CHUẨN BỊ TIẾT 3": "DẶN DÒ",
    "NHIỆM VỤ TỰ HỌC TẠI NHÀ": "DẶN DÒ",
    "SƠ ĐỒ TƯ DUY HỆ THỨC LƯỢNG TRONG TAM GIÁC VUÔNG": "TỔNG KẾT",
    "GỢI Ý BÀI TẬP VỀ NHÀ 4.13 (SGK TR.78)": "GỢI Ý 4.13"
}

title_count = 0
for old_t, new_t in TITLE_MAPPINGS.items():
    old_attr = f'data-title-vi="{old_t}"'
    new_attr = f'data-title-vi="{new_t}"'
    if old_attr in content:
        title_count += content.count(old_attr)
        content = content.replace(old_attr, new_attr)

    old_strong = f'<strong>{old_t}</strong>'
    new_strong = f'<strong>{new_t}</strong>'
    if old_strong in content:
        content = content.replace(old_strong, new_strong)

    old_h4 = f'<h4 class="block-title">{old_t}</h4>'
    new_h4 = f'<h4 class="block-title">{new_t}</h4>'
    if old_h4 in content:
        content = content.replace(old_h4, new_h4)

print(f"  Replaced {title_count} verbose titles with clean titles.")

# 7. Sửa bước Slide 16 thành tuần tự dứt điểm (1: Định nghĩa, 2: Hai trường hợp, 3: Công cụ)
def update_block_step(txt, block_id, new_step):
    block_pattern = rf'(<div\s+class="content-block[^"]*"\s+id="{block_id}"[^>]*>)([\s\S]*?)(<button class="btn-block-speak")'
    m = re.search(block_pattern, txt)
    if not m:
        print(f"  [WARN] Block {block_id} not found!")
        return txt

    start_tag = m.group(1)
    overlay = m.group(2)
    rest = m.group(3)

    if 'data-step="' in start_tag:
        new_start_tag = re.sub(r'data-step="[^"]*"', f'data-step="{new_step}"', start_tag)
    else:
        new_start_tag = start_tag.replace('id="', f'data-step="{new_step}" id="')

    badge_pattern = rf'(<span\s+class="badge-step-num"\s+onclick="setBlockStepDirect\(\'{block_id}\'\)"[^>]*>)([^<]*)(</span>)'
    new_overlay = re.sub(badge_pattern, rf'\g<1>{new_step}\g<3>', overlay)

    new_full = new_start_tag + new_overlay + rest
    txt = txt[:m.start()] + new_full + txt[m.end():]
    return txt

content = update_block_step(content, 's16_b1', '1')
content = update_block_step(content, 's16_b2', '2')
content = update_block_step(content, 's16_t1', '3')

# Slide 16 max steps = 3
content = re.sub(
    r'(<section\s+class="slide-item[^"]*"[^>]*id="s16"[^>]*data-max-steps=")\d+(")',
    r'\g<1>3\g<2>',
    content
)
print("  Re-indexed Slide 16 steps: Left (1 -> 2) -> Right (3).")

# 8. Lưu file
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"SAVED RECREATED {target_path} SUCCESSFULLY!")
