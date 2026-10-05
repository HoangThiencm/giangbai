import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# Bảng chuyển đổi tiêu đề tinh gọn
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

def clean_titles_in_html(content):
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

    print(f"  Cleaned {count} titles.")
    return content

print("Title mapping dictionary ready.")
