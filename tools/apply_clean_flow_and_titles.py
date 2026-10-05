import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# 1. BẢNG TIÊU ĐỀ TINH GỌN
TITLE_MAPPINGS = {
    # Hướng dẫn & lời giải
    "HƯỚNG DẪN GIẢI TỪNG BƯỚC": "HƯỚNG DẪN",
    "HĐ1: HƯỚNG DẪN GIẢI TỪNG BƯỚC": "HƯỚNG DẪN",
    "HĐ2: HƯỚNG DẪN GIẢI & KẾT LUẬN": "HƯỚNG DẪN",
    "VÍ DỤ MẪU 1 (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "VÍ DỤ MẪU 2 (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "VÍ DỤ MẪU 3 (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "VÍ DỤ MẪU 4 (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "BƯỚC GIẢI CHI TIẾT": "HƯỚNG DẪN",
    "BÀI TẬP TƯƠNG TỰ (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "LUYỆN TẬP 1A (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "LUYỆN TẬP 1B (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "GIẢI BÀI TOÁN MỞ ĐẦU (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "LUYỆN TẬP TẠI CHỖ (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "LUYỆN TẬP 2 (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "CÁC BƯỚC THỰC HIỆN THEO YÊU CẦU": "HƯỚNG DẪN",
    "LUYỆN TẬP 3 (PHÂN TÍCH MẪU THỨC)": "HƯỚNG DẪN",
    "HƯỚNG DẪN QUY ĐỒNG MẪU": "HƯỚNG DẪN",
    "LUYỆN TẬP 3 — BƯỚC 3 & 4 (HƯỚNG DẪN GIẢI CHI TIẾT)": "HƯỚNG DẪN",
    "HƯỚNG DẪN GIẢI CÂU A": "HƯỚNG DẪN a",
    "HƯỚNG DẪN GIẢI CÂU B": "HƯỚNG DẪN b",
    "HƯỚNG DẪN GIẢI 2.3A": "HƯỚNG DẪN 2.3a",
    "HƯỚNG DẪN GIẢI 2.3B": "HƯỚNG DẪN 2.3b",
    "LỜI GIẢI CHI TIẾT & BIỆN LUẬN": "HƯỚNG DẪN",
    "GIẢI PHƯƠNG TRÌNH NĂNG SUẤT (HƯỚNG DẪN GIẢI)": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (CHUẨN GDPT 2018)": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (CHUẨN SGK)": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT": "HƯỚNG DẪN",
    "HƯỚNG DẪN THỰC HIỆN CÂU A": "HƯỚNG DẪN",
    "LỜI GIẢI CHI TIẾT (2 CÁCH TÍNH CẠNH BC)": "HƯỚNG DẪN",

    # Đề bài & Hoạt động
    "HĐ1: PHÂN TÍCH ĐA THỨC (ĐỀ BÀI)": "HOẠT ĐỘNG 1",
    "HĐ2: GIẢI PHƯƠNG TRÌNH P(x) = 0 (ĐỀ BÀI)": "HOẠT ĐỘNG 2",
    "HĐ3: BIẾN ĐỔI CHUYỂN VẾ": "HOẠT ĐỘNG 3",
    "HĐ4: KIỂM TRA NGHIỆM": "HOẠT ĐỘNG 4",
    "HĐ5: XÉT PHƯƠNG TRÌNH (1) (SGK TR.29)": "HOẠT ĐỘNG 5",
    "HOẠT ĐỘNG 1 (SGK TR.74)": "HOẠT ĐỘNG 1",
    "HOẠT ĐỘNG 2 (SGK TR.75)": "HOẠT ĐỘNG 2",
    "XÉT PHƯƠNG TRÌNH (SGK TR.28)": "KHÁM PHÁ",

    # Ví dụ & Luyện tập
    "VÍ DỤ MẪU 1 (ĐỀ BÀI)": "VÍ DỤ 1",
    "VÍ DỤ MẪU 2 (ĐỀ BÀI)": "VÍ DỤ 2",
    "VÍ DỤ MẪU 3 (ĐỀ BÀI)": "VÍ DỤ 3",
    "VÍ DỤ MẪU 4 (ĐỀ BÀI)": "VÍ DỤ 4",
    "VÍ DỤ MINH HỌA NHANH": "VÍ DỤ MINH HỌA",
    "LUYỆN TẬP NHANH TẠI LỚP (ĐỀ BÀI)": "LUYỆN TẬP 1",
    "LUYỆN TẬP 1A (ĐỀ BÀI)": "LUYỆN TẬP 1a",
    "LUYỆN TẬP 1B (ĐỀ BÀI)": "LUYỆN TẬP 1b",
    "LUYỆN TẬP TẠI CHỖ (ĐỀ BÀI)": "LUYỆN TẬP 2",
    "LUYỆN TẬP 2 (ĐỀ BÀI)": "LUYỆN TẬP 2",
    "LUYỆN TẬP 3 (ĐỀ BÀI)": "LUYỆN TẬP 3",
    "LUYỆN TẬP 4 (SGK TR.77)": "LUYỆN TẬP 4",
    "BÀI TẬP TƯƠNG TỰ (ĐỀ BÀI)": "LUYỆN TẬP",
    "BÀI TẬP VẬN DỤNG NHANH TẠI LỚP (30 GIÂY)": "VẬN DỤNG",

    # Câu hỏi & đáp án
    "CÂU HỎI ĐẶT VẤN ĐỀ": "CÂU HỎI",
    "CÂU HỎI NHẬN BIẾT NHANH (ĐỀ BÀI)": "CÂU HỎI",
    "CÂU HỎI THẢO LUẬN TƯ DUY": "CÂU HỎI",
    "CÂU HỎI TƯ DUY": "CÂU HỎI",
    "CÂU HỎI TRẮC NGHIỆM 1": "TRẮC NGHIỆM 1",
    "CÂU HỎI TRẮC NGHIỆM 2": "TRẮC NGHIỆM 2",
    "TRÒ CHƠI TRẮC NGHIỆM ĐÁNH GIÁ NHANH": "TRẮC NGHIỆM",
    "ĐÁP ÁN & GIẢI THÍCH": "ĐÁP ÁN",
    "ĐÁP ÁN ĐÚNG & PHÂN TÍCH BẪY SAI LẦM": "ĐÁP ÁN",
    "GỢI Ý & ĐỐI CHIẾU NHANH": "GỢI Ý",

    # Tình huống & hình
    "TÌNH HUỐNG THỰC TẾ (SGK TR.26)": "TÌNH HUỐNG",
    "TÌNH HUỐNG MỞ ĐẦU (SGK TR.74)": "TÌNH HUỐNG",
    "HÌNH 2.1 — MINH HỌA KHU VƯỜN HÌNH VUÔNG": "HÌNH 2.1",
    "HÌNH 2.2 — MINH HỌA MẢNH ĐẤT VÀ NHÀ": "HÌNH 2.2",
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
    "TRỌNG TÂM KIẾN THỨC": "TRỌNG TÂM",
    "MỤC TIÊU BÀI HỌC (3 TIẾT)": "MỤC TIÊU",
    "CÁCH GIẢI PHƯƠNG TRÌNH TÍCH": "CÁCH GIẢI",
    "KỸ THUẬT BIẾN ĐỔI VỀ DẠNG TÍCH": "PHƯƠNG PHÁP",
    "CÁC KỸ THUẬT PHÂN TÍCH NHÂN TỬ THƯỜNG DÙNG": "PHƯƠNG PHÁP",
    "CHÚ Ý QUAN TRỌNG: CẤM CHIA CHO ẨN": "CHÚ Ý",
    "LƯU Ý DẤU PHÉP TÍNH": "LƯU Ý",
    "CHÚ Ý KHI TÌM ĐKXĐ": "CHÚ Ý",
    "LƯU Ý CỐT LÕI (BƯỚC 4)": "LƯU Ý",
    "CHÚ Ý QUAN TRỌNG VỀ NGHIỆM x = 0": "CHÚ Ý",
    "KỸ NĂNG XÉT TAM THỨC BẬC HAI LUÔN DƯƠNG": "KỸ NĂNG",
    "QUY TRÌNH 4 BƯỚC BẮT BUỘC": "QUY TRÌNH 4 BƯỚC",
    "TẠI SAO PHẢI TÌM ĐKXĐ TRƯỚC TIÊN?": "ĐIỀU KIỆN XÁC ĐỊNH",
    "PHÂN TÍCH HẰNG ĐẲNG THỨC": "PHÂN TÍCH",
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
    "GIẢI BÀI TOÁN MỞ ĐẦU (ĐỀ BÀI)": "BÀI TOÁN MỞ ĐẦU",
    "BÀI TOÁN THỰC TẾ 2.4 (ĐỀ BÀI & THIẾT LẬP)": "BÀI 2.4",
    "BÀI TOÁN LÀM CHUNG CÔNG VIỆC 2.5 (ĐỀ BÀI & PT)": "BÀI 2.5",
    "ĐỀ BÀI 2.1 (SGK TR.30)": "BÀI 2.1",
    "ĐỀ BÀI 2.2 (SGK TR.30)": "BÀI 2.2",
    "ĐỀ BÀI 2.3A (SGK TR.30)": "BÀI 2.3a",
    "ĐỀ BÀI 2.3B (SGK TR.30)": "BÀI 2.3b",
    "KẾT LUẬN THỰC TIỄN": "KẾT LUẬN",
    "HƯỚNG DẪN TỰ HỌC TIẾT 1": "DẶN DÒ",
    "HƯỚNG DẪN TỰ HỌC TIẾT 2": "DẶN DÒ",
    "HƯỚNG DẪN TỰ HỌC VỀ NHÀ": "DẶN DÒ",
    "TỔNG KẾT TIẾT 1 & DẶN DÒ": "DẶN DÒ",
    "TỔNG KẾT TIẾT 2 & CHUẨN BỊ TIẾT 3": "DẶN DÒ",
    "NHIỆM VỤ TỰ HỌC TẠI NHÀ": "DẶN DÒ",
    "TỔNG KẾT TIẾT 2": "TỔNG KẾT",
    "NỘI DUNG TRỌNG TÂM TIẾT 3": "TRỌNG TÂM",
    "HỆ THỐNG THỬ THÁCH HỌC TẬP": "BÀI TẬP",
    "BẢN ĐỒ TƯ DUY 2 PHƯƠNG PHÁP": "TỔNG KẾT",
    "SƠ ĐỒ TƯ DUY HỆ THỐNG KIẾN THỨC BÀI 4": "TỔNG KẾT",
    "SƠ ĐỒ TƯ DUY HỆ THỨC LƯỢNG TRONG TAM GIÁC VUÔNG": "TỔNG KẾT",
    "GỢI Ý BÀI TẬP VỀ NHÀ 4.13 (SGK TR.78)": "GỢI Ý 4.13"
}

def clean_titles(content):
    count = 0
    for old_t, new_t in TITLE_MAPPINGS.items():
        # replace data-title-vi="..."
        old_attr = f'data-title-vi="{old_t}"'
        new_attr = f'data-title-vi="{new_t}"'
        if old_attr in content:
            c = content.count(old_attr)
            content = content.replace(old_attr, new_attr)
            count += c

        # replace <strong>OLD_T</strong>
        old_strong = f'<strong>{old_t}</strong>'
        new_strong = f'<strong>{new_t}</strong>'
        if old_strong in content:
            content = content.replace(old_strong, new_strong)

        # replace <h4 class="block-title">OLD_T</h4>
        old_h4 = f'<h4 class="block-title">{old_t}</h4>'
        new_h4 = f'<h4 class="block-title">{new_t}</h4>'
        if old_h4 in content:
            content = content.replace(old_h4, new_h4)

    return content, count

def update_block_step(content, block_id, new_step):
    block_pattern = rf'(<div\s+class="content-block[^"]*"\s+id="{block_id}"[^>]*>)([\s\S]*?)(<button class="btn-block-speak")'
    m = re.search(block_pattern, content)
    if not m:
        print(f"  [WARN] Block {block_id} not found!")
        return content

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
    content = content[:m.start()] + new_full + content[m.end():]
    return content

def update_slide_max_steps(content, slide_id, max_steps):
    pattern = rf'(<section\s+class="slide-item[^"]*"[^>]*id="{slide_id}"[^>]*data-max-steps=")(\d+)(")'
    content = re.sub(pattern, rf'\g<1>{max_steps}\g<3>', content)
    # also if order of attributes differs
    pattern2 = rf'(<section\s+class="slide-item[^"]*"[^>]*data-max-steps=")(\d+)("[^>]*id="{slide_id}")'
    content = re.sub(pattern2, rf'\g<1>{max_steps}\g<3>', content)
    return content

# 3. REFACTOR BAI 4
def refactor_bai_4():
    fn = 'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
    print(f"\nProcessing {fn}...")
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    # Step re-indexing mappings: (block_id, new_step)
    BAI_4_STEPS = [
        # Slide 3
        ('s3_b2', '1'),
        ('s3_t1', '2'),
        ('s3_t2', '3'),

        # Slide 4: Left Ví dụ 1 xong (1->2), Right Luyện tập 1 xong (3->4)
        ('s4_b2', '1'),
        ('s4_b3', '2'),
        ('s4_t1', '3'),
        ('s4_t2', '4'),

        # Slide 5: Left Ví dụ 2 xong (1->2), Right Kỹ thuật & Luyện tập xong (3->4->5)
        ('s5_b2', '1'),
        ('s5_b3', '2'),
        ('s5_t1', '3'),
        ('s5_t2', '4'),
        ('s5_t3', '5'),

        # Slide 7: Left Luyện tập 1a xong (1->2), Right Lưu ý (3)
        ('s7_b2', '1'),
        ('s7_b3', '2'),
        ('s7_t2', '3'),

        # Slide 8: Left Luyện tập 1b xong (1->2), Right Thảo luận & Chú ý cấm chia (3->4)
        ('s8_b2', '1'),
        ('s8_b3', '2'),
        ('s8_t1', '3'),
        ('s8_t2', '4'),

        # Slide 9: Left Bài toán mở đầu xong (1->2), Right Kết luận & Dặn dò (3->4)
        ('s9_b2', '1'),
        ('s9_b3', '2'),
        ('s9_t1', '3'),
        ('s9_t2', '4'),

        # Slide 12: Left Ví dụ 3 xong (1->2), Right Luyện tập 2 xong (3->4) & Trắc nghiệm (5)
        ('s12_b2', '1'),
        ('s12_b3', '2'),
        ('s12_t1', '3'),
        ('s12_t2', '4'),
        ('s12_t3', '5'),

        # Slide 13: Left Luyện tập 2 xong (1->2), Right Chú ý ĐKXĐ (3)
        ('s13_b2', '1'),
        ('s13_b3', '2'),
        ('s13_t1', '3'),

        # Slide 15: Left Quy trình 4 bước (1), Right Lưu ý (2)
        ('s15_b2', '1'),
        ('s15_t1', '2'),

        # Slide 16: Left Ví dụ 4 xong (1->2), Right Câu hỏi tư duy (3)
        ('s16_b2', '1'),
        ('s16_b3', '2'),
        ('s16_t1', '3'),

        # Slide 17: Left Luyện tập 3 Đề (1) & Phân tích mẫu/ĐKXĐ (2), Right Quy đồng mẫu (3)
        ('s17_b2', '1'),
        ('s17_b3', '2'),
        ('s17_t1', '3'),

        # Slide 18: Left Luyện tập 3 Lời giải hoàn tất (1), Right Tổng kết (2) & Dặn dò (3)
        ('s18_b1', '1'),
        ('s18_t1', '2'),
        ('s18_t2', '3'),

        # Slide 19: Left Bản đồ tư duy (1), Right Trọng tâm tiết 3 (2) & Thử thách (3)
        ('s19_b1', '1'),
        ('s19_t1', '2'),
        ('s19_t2', '3'),

        # Slide 20: Right Đề 2.1 (1) & Gợi ý (2), Left Lời giải a (3) & Lời giải b (4)
        ('s20_t1', '1'),
        ('s20_t2', '2'),
        ('s20_b1', '3'),
        ('s20_b2', '4'),

        # Slide 21: Right Đề 2.2 (1) & Phân tích (2), Left Lời giải a (3) & Lời giải b (4)
        ('s21_t1', '1'),
        ('s21_t2', '2'),
        ('s21_b1', '3'),
        ('s21_b2', '4'),

        # Slide 22: Right Đề 2.3a (1) & Chú ý x=0 (2), Left Lời giải (3)
        ('s22_t1', '1'),
        ('s22_t2', '2'),
        ('s22_b1', '3'),

        # Slide 23: Right Đề 2.3b (1) & Kỹ năng tam thức (2), Left Lời giải (3)
        ('s23_t1', '1'),
        ('s23_t2', '2'),
        ('s23_b1', '3'),

        # Slide 24: Left Đề 2.4 (1), Right Hình 2.2 (2) & Lời giải (3)
        ('s24_b1', '1'),
        ('s24_t1', '2'),
        ('s24_t2', '3'),

        # Slide 25: Left Đề 2.5 (1), Right Lời giải (2)
        ('s25_b1', '1'),
        ('s25_t1', '2'),

        # Slide 26: Left Sơ đồ tư duy tổng kết (1), Right Dặn dò (2)
        ('s26_b1', '1'),
        ('s26_t1', '2')
    ]

    for bid, st in BAI_4_STEPS:
        html = update_block_step(html, bid, st)

    # Max steps per slide
    MAX_STEPS = {
        's3': 3,
        's4': 4,
        's5': 5,
        's7': 3,
        's8': 4,
        's9': 4,
        's12': 5,
        's13': 3,
        's15': 2,
        's16': 3,
        's17': 3,
        's18': 3,
        's19': 3,
        's20': 4,
        's21': 4,
        's22': 3,
        's23': 3,
        's24': 3,
        's25': 2,
        's26': 2
    }
    for sid, mx in MAX_STEPS.items():
        html = update_slide_max_steps(html, sid, mx)

    # Clean titles
    html, c_titles = clean_titles(html)
    print(f"  Cleaned {c_titles} titles in Bai 4.")

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Saved Bai 4 successfully.")

# 4. REFACTOR BAI 12
def refactor_bai_12():
    fn = 'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'
    print(f"\nProcessing {fn}...")
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    # Slide 16: Left Định nghĩa (1) & Hai trường hợp (2), Right Công cụ (3)
    BAI_12_STEPS = [
        ('s16_b1', '1'),
        ('s16_b2', '2'),
        ('s16_t1', '3')
    ]
    for bid, st in BAI_12_STEPS:
        html = update_block_step(html, bid, st)

    html = update_slide_max_steps(html, 's16', 3)

    # Clean titles
    html, c_titles = clean_titles(html)
    print(f"  Cleaned {c_titles} titles in Bai 12.")

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Saved Bai 12 successfully.")

# 5. REFACTOR MASTER TEMPLATE
def refactor_master_template():
    fn = 'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html'
    print(f"\nProcessing {fn}...")
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace Slide 4 CV 5512 text with proper student activity blocks
    old_s4_body = '''      <div class="slide-content-grid">
        <div class="col-board">
          <div class="col-board-tag">HOẠT ĐỘNG CỦA GIÁO VIÊN (4 BƯỚC CV 5512)</div>
          <div class="content-block highlight-def" data-step="1">
            <h4 class="block-title">Bước 1: Chuyển giao nhiệm vụ</h4>
            <p>GV chia lớp thành các nhóm 4 học sinh, giao phiếu học tập số 1 và yêu cầu thực hiện nhiệm vụ [Nội dung nhiệm vụ trích từ PDF].</p>
          </div>
          <div class="content-block highlight-def" data-step="3">
            <h4 class="block-title">Bước 2: Tổ chức thực hiện</h4>
            <p>GV quan sát các nhóm, kịp thời định hướng các nhóm gặp khó khăn; ghi nhận thái độ làm việc nhóm của học sinh.</p>
          </div>
        </div>
        <div class="col-board">
          <div class="col-board-tag">HOẠT ĐỘNG CỦA HỌC SINH & KẾT QUẢ</div>
          <div class="content-block highlight-proof" data-step="2">
            <h4 class="block-title">Học sinh tiếp nhận & Thảo luận</h4>
            <p>HS nhận phiếu học tập, phân công nhiệm vụ thành viên, tiến hành đo đạc / tính toán theo yêu cầu.</p>
          </div>
          <div class="content-block highlight-example" data-step="4">
            <h4 class="block-title">Bước 3 & 4: Báo cáo thảo luận & Kết luận</h4>
            <p>Đại diện nhóm 1 lên bảng trình bày, các nhóm khác lắng nghe phản biện. GV nhận xét chốt kiến thức.</p>
          </div>
        </div>
      </div>'''

    new_s4_body = '''      <div class="slide-content-grid">
        <!-- CỘT TRÁI: BẢNG GHI BÀI -->
        <div class="col-board">
          <div class="col-board-tag">📋 BẢNG GHI BÀI</div>
          <div class="content-block" data-step="1" data-title-vi="HOẠT ĐỘNG 1">
            <h4 class="block-title">HOẠT ĐỘNG 1</h4>
            <p>[Nhiệm vụ khám phá kiến thức mới trích xuất từ PDF]</p>
          </div>
          <div class="content-block highlight-def" data-step="2" data-title-vi="HƯỚNG DẪN">
            <h4 class="block-title">HƯỚNG DẪN</h4>
            <p>[Các bước thực hiện, phân tích và kết luận rút ra]</p>
          </div>
        </div>
        <!-- CỘT PHẢI: HOẠT ĐỘNG HỌC TẬP -->
        <div class="col-task">
          <div class="col-task-tag">✍️ HOẠT ĐỘNG HỌC TẬP</div>
          <div class="content-block" data-step="3" data-title-vi="CÂU HỎI">
            <h4 class="block-title">CÂU HỎI</h4>
            <p>[Câu hỏi nhận biết hoặc bài tập kiểm tra nhanh]</p>
          </div>
          <div class="content-block highlight-example" data-step="4" data-title-vi="ĐÁP ÁN">
            <h4 class="block-title">ĐÁP ÁN</h4>
            <p>[Đáp án chính xác và phân tích đối chiếu]</p>
          </div>
        </div>
      </div>'''

    if old_s4_body in html:
        html = html.replace(old_s4_body, new_s4_body)
        print("  Replaced Slide 4 in master template with clean student activity layout.")
    else:
        print("  [WARN] Old Slide 4 body not matched exactly in template.")

    # Clean titles
    html, c_titles = clean_titles(html)
    print(f"  Cleaned {c_titles} titles in master template.")

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Saved master template successfully.")

if __name__ == '__main__':
    refactor_bai_4()
    refactor_bai_12()
    refactor_master_template()
    print("\nALL REFACTORS COMPLETED SUCCESSFULLY!")
