# -*- coding: utf-8 -*-
"""
Script sinh 14 Sơ đồ tư duy Mindmap vector 300 DPI cho môn Toán 6 Học kì II (Tuần 19 - 35)
"""
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/HK2_Toan6/mindmaps"
os.makedirs(OUT_DIR, exist_ok=True)

def create_base_canvas(title, subtitle):
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.text(50, 96, title, ha='center', va='center', fontsize=15, fontweight='bold', color='#1E293B')
    ax.text(50, 92.5, subtitle, ha='center', va='center', fontsize=11, fontstyle='italic', color='#475569')
    return fig, ax

def draw_generic_mindmap(filename, title, subtitle, center_title, center_sub, nodes, c_ec="#2563EB", c_fc="#DBEAFE"):
    fig, ax = create_base_canvas(title, subtitle)
    c = patches.FancyBboxPatch((33, 43), 34, 14, boxstyle="round,pad=1.2,rounding_size=2", ec=c_ec, fc=c_fc, lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, center_title, ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, center_sub, ha='center', va='center', fontsize=11, fontweight='bold', color=c_ec)

    for node_title, lines, x, y, ec, fc in nodes:
        b = patches.FancyBboxPatch((x - 16, y - 11), 32, 22, boxstyle="round,pad=1,rounding_size=1.5", ec=ec, fc=fc, lw=2)
        ax.add_patch(b)
        ax.text(x, y + 8, node_title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=ec)
        ax.plot([x - 14, x + 14], [y + 5.5, y + 5.5], color=ec, lw=1)
        for idx, line in enumerate(lines):
            ax.text(x - 14, y + 2.5 - idx * 4.2, line, ha='left', va='center', fontsize=8.8, color="#1E293B")
        cx = 50 + (17 if x > 50 else -17)
        cy = 50 + (7 if y > 50 else -7)
        ax.annotate("", xy=(x + (-16 if x > 50 else 16), y), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=2, connectionstyle="arc3,rad=0.1"))

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, filename)
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

def generate_all():
    # 1. Tiet 55: Luyen tap chung Phan so
    draw_generic_mindmap("mindmap_toan6_tiet55.png",
        "SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: PHÂN SỐ",
        "(Môn Toán 6 - Số học - Tiết 55 - Tuần 20)",
        "PHÂN SỐ CƠ BẢN", "MỞ RỘNG & SO SÁNH",
        [
            ("KHÁI NIỆM PHÂN SỐ", ["• Dạng a/b với a, b thuộc Z, b != 0", "• a là tử số, b là mẫu số", "• Mọi số nguyên a = a/1", "• Số đối của a/b là -a/b"], 18, 70, "#2563EB", "#DBEAFE"),
            ("HAI PHÂN SỐ BẰNG NHAU", ["• Quy tắc: a/b = c/d <=> a . d = b . c", "• Tính chất cơ bản: a/b = (a . m)/(b . m)", "• Rút gọn phân số bằng cách chia ƯCLN", "• Phân số tối giản khi ƯCLN(|a|, |b|) = 1"], 82, 70, "#059669", "#D1FAE5"),
            ("SO SÁNH PHÂN SỐ", ["• Cùng mẫu dương: Tử lớn hơn thì lớn hơn", "• Khác mẫu: Quy đồng mẫu dương rồi so sánh", "• So sánh với số 0 (phân số âm, dương)", "• So sánh qua phân số trung gian (số 1)"], 18, 24, "#D97706", "#FEF3C7"),
            ("HỖN SỐ DƯƠNG", ["• Gồm phần nguyên và phân số nhỏ hơn 1", "• Viết phân số lớn hơn 1 thành hỗn số", "• Đổi hỗn số ra phân số: q r/b = (q.b + r)/b", "• Ứng dụng trong cân đo thực tế"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 2. Tiet 62, 63: 4 phep tinh & 2 bai toan phan so
    draw_generic_mindmap("mindmap_toan6_tiet62_63.png",
        "SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: CÁC PHÉP TÍNH PHÂN SỐ",
        "(Môn Toán 6 - Số học - Tiết 62, 63 - Tuần 22, 23)",
        "CÁC PHÉP TÍNH PHÂN SỐ", "CỘNG TRỪ NHÂN CHIA & ỨNG DỤNG",
        [
            ("PHÉP CỘNG VÀ TRỪ", ["• Cùng mẫu: Cộng/trừ tử, giữ nguyên mẫu", "• Khác mẫu: Quy đồng mẫu dương rồi tính", "• Số đối: a/b + (-a/b) = 0", "• Tính chất giao hoán, kết hợp cộng"], 18, 70, "#2563EB", "#DBEAFE"),
            ("PHÉP NHÂN VÀ CHIA", ["• Nhân: (a/b) . (c/d) = (a.c) / (b.d)", "• Phân số nghịch đảo của a/b là b/a", "• Chia: (a/b) : (c/d) = (a/b) . (d/c)", "• Phân phối của nhân đối với cộng"], 82, 70, "#059669", "#D1FAE5"),
            ("BÀI TOÁN 1: GIÁ TRỊ PHÂN SỐ", ["• Tìm m/n của số b cho trước", "• Quy tắc: Lấy b . (m/n)", "• Ví dụ: 2/3 của 18 là: 18 . 2/3 = 12", "• Áp dụng tính toán giảm giá, tỉ lệ"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("BÀI TOÁN 2: TÌM MỘT SỐ", ["• Tìm số biết m/n của nó bằng a", "• Quy tắc: Lấy a : (m/n)", "• Ví dụ: Tìm x biết 3/4 của x là 15: x = 15 : 3/4 = 20", "• Phân biệt rõ giữa bài toán 1 và bài toán 2"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 3. Tiet 64, 65: Bai tap cuoi chuong VI
    draw_generic_mindmap("mindmap_toan6_tiet64_65.png",
        "SƠ ĐỒ TƯ DUY TỔNG KẾT CHƯƠNG VI: PHÂN SỐ",
        "(Môn Toán 6 - Số học - Tiết 64, 65 - Tuần 23)",
        "TỔNG KẾT CHƯƠNG VI", "TOÀN BỘ KIẾN THỨC PHÂN SỐ",
        [
            ("ĐỊNH NGHĨA & SO SÁNH", ["• Khái niệm phân số, phân số bằng nhau", "• Rút gọn về phân số tối giản", "• Quy đồng mẫu số nhiều phân số", "• So sánh phân số, hỗn số dương"], 18, 70, "#2563EB", "#DBEAFE"),
            ("BỐN PHÉP TOÁN PHÂN SỐ", ["• Phép cộng, phép trừ hai phân số", "• Phép nhân, phép chia hai phân số", "• Thứ tự thực hiện các phép tính và ngoặc", "• Tính nhanh hợp lí dùng tính chất"], 82, 70, "#059669", "#D1FAE5"),
            ("HAI BÀI TOÁN VỀ PHÂN SỐ", ["• Tìm giá trị phân số của một số: b . (m/n)", "• Tìm một số biết giá trị phân số: a : (m/n)", "• Nhận diện đúng đề bài hỏi đại lượng nào", "• Giải toán chuyển động, tỉ lệ lao động"], 18, 24, "#D97706", "#FEF3C7"),
            ("ỨNG DỤNG THỰC TIỄN", ["• Tính toán chia phần trong đời sống", "• Đổi đơn vị đo (giờ sang phút, kg sang g)", "• Tính tỉ lệ nguyên liệu nấu ăn", "• Quản lí thời gian biểu khoa học"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 4. Tiet 71, 72: On tap giua HK2 (So hoc)
    draw_generic_mindmap("mindmap_toan6_tiet71_72.png",
        "SƠ ĐỒ TƯ DUY ÔN TẬP GIỮA HỌC KÌ II: SỐ HỌC 6",
        "(Môn Toán 6 - Số học - Tiết 71, 72 - Tuần 25, 26)",
        "ÔN TẬP GIỮA HKII", "PHÂN SỐ & SỐ THẬP PHÂN",
        [
            ("PHÂN SỐ & PHÉP TÍNH", ["• Khái niệm, so sánh, quy đồng phân số", "• 4 phép tính cộng, trừ, nhân, chia", "• Hai bài toán cơ bản về phân số", "• Tính giá trị biểu thức phân số phức tạp"], 18, 70, "#2563EB", "#DBEAFE"),
            ("SỐ THẬP PHÂN", ["• Định nghĩa số thập phân âm, dương", "• Số đối của số thập phân", "• So sánh hai số thập phân", "• Chuyển đổi giữa phân số và số thập phân"], 82, 70, "#059669", "#D1FAE5"),
            ("TÍNH TOÁN SỐ THẬP PHÂN", ["• Cộng, trừ số thập phân có dấu", "• Nhân, chia số thập phân có dấu", "• Quy tắc dấu ngoặc khi tính toán", "• Tính nhanh bằng tính chất phân phối"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("LÀM TRÒN & ƯỚC LƯỢNG", ["• Quy tắc làm tròn số thập phân", "• Làm tròn đến hàng đơn vị, chục, phần mười", "• Ước lượng kết quả phép tính khi mua sắm", "• Dùng máy tính cầm tay kiểm tra kết quả"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 5. Tiet 77, 78: Luyen tap chung Ti so va %
    draw_generic_mindmap("mindmap_toan6_tiet77_78.png",
        "SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: TỈ SỐ VÀ TỈ SỐ PHẦN TRĂM",
        "(Môn Toán 6 - Số học - Tiết 77, 78 - Tuần 27, 28)",
        "TỈ SỐ & PHẦN TRĂM", "BÀI TOÁN TỈ SỐ THỰC TẾ",
        [
            ("TỈ SỐ CỦA HAI ĐẠI LƯỢNG", ["• Tỉ số của a và b là thương a : b (b != 0)", "• Viết dưới dạng phân số a/b", "• Chú ý: Hai đại lượng phải cùng đơn vị đo", "• Tỉ lệ xích bản đồ: T = a/b"], 18, 70, "#2563EB", "#DBEAFE"),
            ("TỈ SỐ PHẦN TRĂM", ["• Tỉ số phần trăm của a và b: (a.100)/b %", "• Kí hiệu phần trăm %", "• Tính tỉ số phần trăm học sinh giỏi", "• Tính tỉ lệ tăng trưởng dân số, sản lượng"], 82, 70, "#059669", "#D1FAE5"),
            ("HAI BÀI TOÁN TỈ SỐ %", ["• Bài toán 1: Tìm m% của số a -> a . (m/100)", "• Bài toán 2: Tìm số biết m% của nó là b -> b : (m/100)", "• Tính tiền lãi tiết kiệm ngân hàng", "• Tính tiền giảm giá (Sale off) khi mua sắm"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("ỨNG DỤNG ĐỜI SỐNG", ["• Đọc nhãn mác thành phần dinh dưỡng (%)", "• Tính nồng độ phần trăm dung dịch muối", "• Đọc bản đồ địa lí qua tỉ lệ xích", "• Quản lí chi tiêu cá nhân hợp lí"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 6. Tiet 79, 80: Bai tap cuoi chuong VII So thap phan
    draw_generic_mindmap("mindmap_toan6_tiet79_80.png",
        "SƠ ĐỒ TƯ DUY TỔNG KẾT CHƯƠNG VII: SỐ THẬP PHÂN",
        "(Môn Toán 6 - Số học - Tiết 79, 80 - Tuần 28)",
        "TỔNG KẾT CHƯƠNG VII", "SỐ THẬP PHÂN VÀ TỈ SỐ",
        [
            ("SỐ THẬP PHÂN & SO SÁNH", ["• Cấu tạo số thập phân (phần nguyên, phần thập phân)", "• Số thập phân âm và số đối", "• So sánh hai số thập phân", "• Biểu diễn số thập phân trên trục số"], 18, 70, "#2563EB", "#DBEAFE"),
            ("CÁC PHÉP TOÁN", ["• Cộng, trừ số thập phân", "• Nhân, chia số thập phân với số nguyên/thập phân", "• Nhân chia nhẩm với 10, 100, 0.1, 0.01", "• Thứ tự thực hiện phép tính và dấu ngoặc"], 82, 70, "#059669", "#D1FAE5"),
            ("LÀM TRÒN & ƯỚC LƯỢNG", ["• Chữ số ngay sau hàng làm tròn >= 5: Cộng 1", "• Chữ số ngay sau hàng làm tròn < 5: Giữ nguyên", "• Ước lượng phép nhân, chia trong thực tế", "• Sai số khi làm tròn"], 18, 24, "#D97706", "#FEF3C7"),
            ("TỈ SỐ & PHẦN TRĂM", ["• Tỉ số và tỉ lệ xích bản đồ", "• Tỉ số phần trăm và các bài toán %", "• Bài toán tính lãi suất ngân hàng", "• Bài toán mua sắm khuyến mãi thực tế"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 7. Tiet 29 Hinh hoc: Luyen tap chung Diem, duong thang, doan thang
    draw_generic_mindmap("mindmap_toan6_hinh_tiet29.png",
        "SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: ĐIỂM, ĐƯỜNG THẲNG, ĐOẠN THẲNG",
        "(Môn Toán 6 - Hình học - Tiết 29 - Tuần 25)",
        "HÌNH HỌC CƠ BẢN", "ĐIỂM - ĐƯỜNG THẲNG - ĐOẠN THẲNG",
        [
            ("ĐIỂM & ĐƯỜNG THẲNG", ["• Điểm thuộc/không thuộc đường thẳng (A in d)", "• Ba điểm thẳng hàng / không thẳng hàng", "• Hai đường thẳng cắt nhau, song song, trùng nhau", "• Qua hai điểm phân biệt có duy nhất 1 đường thẳng"], 18, 70, "#2563EB", "#DBEAFE"),
            ("ĐIỂM NẰM GIỮA & TIA", ["• Điểm B nằm giữa hai điểm A và C", "• Khi đó: AB + BC = AC", "• Khái niệm tia: Gốc O và phần đường thẳng", "• Hai tia đối nhau (tạo thành đường thẳng)", "• Hai tia trùng nhau"], 82, 70, "#059669", "#D1FAE5"),
            ("ĐOẠN THẲNG & ĐỘ DÀI", ["• Đoạn thẳng AB gồm điểm A, B và các điểm ở giữa", "• Đo độ dài đoạn thẳng bằng thước kẻ chia mm", "• So sánh độ dài hai đoạn thẳng", "• Đơn vị đo độ dài chuẩn (mm, cm, m, km)"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("TRUNG ĐIỂM ĐOẠN THẲNG", ["• Định nghĩa: M nằm giữa A, B và MA = MB", "• Công thức: MA = MB = AB / 2", "• Cách xác định trung điểm bằng thước hoặc gấp giấy", "• Tính chất đối xứng qua trung điểm"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 8. Tiet 34 Hinh hoc: Luyen tap chung Goc
    draw_generic_mindmap("mindmap_toan6_hinh_tiet34.png",
        "SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: GÓC VÀ SỐ ĐO GÓC",
        "(Môn Toán 6 - Hình học - Tiết 34 - Tuần 30)",
        "HÌNH HỌC CƠ BẢN", "GÓC VÀ SỐ ĐO GÓC",
        [
            ("KHÁI NIỆM GÓC", ["• Góc là hình tạo bởi hai tia chung gốc", "• Gốc chung là đỉnh của góc", "• Hai tia là hai cạnh của góc", "• Kí hiệu: góc xOy hoặc góc AOB"], 18, 70, "#2563EB", "#DBEAFE"),
            ("ĐO GÓC & ĐƠN VỊ ĐO", ["• Dụng cụ: Thước đo góc (thước đo độ)", "• Đơn vị: Độ (kí hiệu là độ tròn)", "• Mỗi góc có 1 số đo, từ 0 độ đến 180 độ", "• Hai góc bằng nhau có số đo bằng nhau"], 82, 70, "#059669", "#D1FAE5"),
            ("CÁC LOẠI GÓC", ["• Góc nhọn: Lớn hơn 0 độ và nhỏ hơn 90 độ", "• Góc vuông: Bằng 90 độ (dùng êke kiểm tra)", "• Góc tù: Lớn hơn 90 độ và nhỏ hơn 180 độ", "• Góc bẹt: Bằng 180 độ (hai cạnh đối nhau)"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("ĐIỂM TRONG CỦA GÓC", ["• Khái niệm điểm nằm bên trong góc", "• Nhận diện góc trong các hình tam giác, tứ giác", "• Ứng dụng: Góc mở compa, góc sút bóng trong thể thao", "• Đo góc nghiêng mái nhà thực tế"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 9. Tiet 35 Hinh hoc: Bai tap cuoi chuong VIII
    draw_generic_mindmap("mindmap_toan6_hinh_tiet35.png",
        "SƠ ĐỒ TƯ DUY TỔNG KẾT CHƯƠNG VIII: HÌNH HỌC CƠ BẢN",
        "(Môn Toán 6 - Hình học - Tiết 35 - Tuần 31)",
        "TỔNG KẾT CHƯƠNG VIII", "ĐIỂM - ĐƯỜNG THẲNG - GÓC",
        [
            ("ĐIỂM & ĐƯỜNG THẲNG", ["• Điểm, đường thẳng, ba điểm thẳng hàng", "• Quan hệ thuộc / không thuộc", "• Vị trí tương đối hai đường thẳng", "• Điểm nằm giữa hai điểm"], 18, 70, "#2563EB", "#DBEAFE"),
            ("TIA & ĐOẠN THẲNG", ["• Khái niệm tia, hai tia đối nhau", "• Đoạn thẳng và độ dài đoạn thẳng", "• Hệ thức cộng đoạn thẳng: AB + BC = AC", "• Trung điểm của đoạn thẳng: MA = MB = AB/2"], 82, 70, "#059669", "#D1FAE5"),
            ("GÓC VÀ PHÂN LOẠI", ["• Định nghĩa góc, đỉnh và cạnh của góc", "• Thước đo góc và cách đo góc", "• Phân loại: Góc nhọn, vuông, tù, bẹt", "• Điểm nằm trong góc"], 18, 24, "#D97706", "#FEF3C7"),
            ("KỸ NĂNG VẼ HÌNH", ["• Dùng thước thẳng vẽ đường thẳng, đoạn thẳng", "• Dùng thước chia vạch xác định trung điểm", "• Dùng êke vẽ góc vuông", "• Dùng thước đo độ vẽ góc cho trước số đo"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 10. Tiet 37 Hinh hoc: On tap cuoi HKII Hinh hoc 6
    draw_generic_mindmap("mindmap_toan6_hinh_tiet37.png",
        "SƠ ĐỒ TƯ DUY ÔN TẬP CUỐI HỌC KÌ II: HÌNH HỌC 6",
        "(Môn Toán 6 - Hình học - Tiết 37 - Tuần 33)",
        "ÔN TẬP CUỐI HKII", "HÌNH HỌC 6 TOÀN DIỆN",
        [
            ("CÁC HÌNH PHẲNG (HKI)", ["• Tam giác đều, hình vuông, lục giác đều", "• Hình chữ nhật, hình thoi, hình bình hành, thang cân", "• Chu vi và diện tích các hình phẳng cơ bản", "• Tính đối xứng: Trục đối xứng và tâm đối xứng"], 18, 70, "#2563EB", "#DBEAFE"),
            ("HÌNH HỌC CƠ BẢN (HKII)", ["• Điểm, đường thẳng, tia, đoạn thẳng", "• Điểm nằm giữa, cộng độ dài đoạn thẳng", "• Trung điểm của đoạn thẳng", "• Góc, số đo góc, phân loại các loại góc"], 82, 70, "#059669", "#D1FAE5"),
            ("VẼ HÌNH VỚI GEOGEBRA", ["• Dựng điểm, đoạn thẳng, đường thẳng", "• Dựng trung điểm và đo độ dài", "• Dựng góc và đo số đo góc bằng phần mềm", "• Kiểm nghiệm tính chất hình học tương tác"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("BÀI TOÁN TÍNH TOÁN & THỰC TẾ", ["• Tính độ dài đoạn thẳng, chứng minh trung điểm", "• So sánh các góc trong tam giác", "• Đo góc nghiêng và khoảng cách thực tế", "• Rèn luyện kỹ năng trình bày lập luận chuẩn xác"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 11. Tiet 89: Luyen tap chung Bieu do cot & cot kep
    draw_generic_mindmap("mindmap_toan6_tiet89.png",
        "SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: BIỂU ĐỒ THỐNG KÊ",
        "(Môn Toán 6 - Thống kê - Tiết 89 - Tuần 31)",
        "THỐNG KÊ 6", "BẢNG BIỂU & BIỂU ĐỒ CỘT",
        [
            ("THU THẬP & PHÂN LOẠI", ["• Thu thập dữ liệu: Quan sát, phỏng vấn, khảo sát", "• Phân loại: Dữ liệu số (định lượng), không phải số", "• Bảng dữ liệu ban đầu", "• Bảng thống kê tần số"], 18, 70, "#2563EB", "#DBEAFE"),
            ("BIỂU ĐỒ TRANH", ["• Dùng biểu tượng hoặc hình ảnh biểu diễn số lượng", "• Mỗi biểu tượng ứng với một số lượng nhất định", "• Đọc và trích xuất dữ liệu từ biểu đồ tranh", "• Ưu điểm: Trực quan, hấp dẫn với trẻ em"], 82, 70, "#059669", "#D1FAE5"),
            ("BIỂU ĐỒ CỘT ĐƠN", ["• Các cột hình chữ nhật có cùng chiều rộng", "• Chiều cao cột thể hiện số lượng/giá trị", "• Gốc trục đứng từ số 0, vạch chia đều", "• So sánh độ lớn giữa các đối tượng"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("BIỂU ĐỒ CỘT KÉP", ["• Ghép hai cột cạnh nhau cho cùng một tiêu chí", "• Dùng phân biệt bằng màu sắc hoặc họa tiết khác nhau", "• So sánh hai nhóm đối tượng qua các thời điểm", "• Rút ra nhận xét xu thế biến động số liệu"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 12. Tiet 92: Luyen tap chung Xac suat thuc nghiem
    draw_generic_mindmap("mindmap_toan6_tiet92.png",
        "SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: XÁC SUẤT THỰC NGHIỆM",
        "(Môn Toán 6 - Xác suất - Tiết 92 - Tuần 32)",
        "XÁC SUẤT THỰC NGHIỆM", "TRÒ CHƠI & THÍ NGHIỆM",
        [
            ("KẾT QUẢ CÓ THỂ", ["• Các kết quả có thể xảy ra khi tung đồng xu (Sấp, Ngửa)", "• Các kết quả khi gieo xúc xắc (1, 2, 3, 4, 5, 6 chấm)", "• Tập hợp tất cả các kết quả có thể", "• Tính ngẫu nhiên, không dự đoán trước được"], 18, 70, "#2563EB", "#DBEAFE"),
            ("SỰ KIỆN TRONG THỰC TẾ", ["• Sự kiện chắc chắn xảy ra (xác suất = 1)", "• Sự kiện không thể xảy ra (xác suất = 0)", "• Sự kiện có thể xảy ra (ngẫu nhiên)", "• Kiểm tra sự kiện xảy ra hay không xảy ra"], 82, 70, "#059669", "#D1FAE5"),
            ("CÔNG THỨC XÁC SUẤT THỰC NGHIỆM", ["• P = (Số lần sự kiện xảy ra) / (Tổng số lần thử nghiệm)", "• Viết dưới dạng phân số hoặc phần trăm %", "• Khi số lần thử nghiệm càng lớn, P càng ổn định", "• Ví dụ: Tung đồng xu 50 lần, xuất hiện ngửa 26 lần -> P = 26/50 = 52%"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("ỨNG DỤNG THỰC TIỄN", ["• Dự đoán khả năng thắng thua trong trò chơi", "• Dự báo thời tiết (khả năng mưa)", "• Thống kê tỉ lệ nảy mầm của hạt giống", "• Đánh giá chất lượng sản phẩm trong sản xuất"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 13. Tiet 93-97: On tap cuoi HKII Toan dien Toan 6
    draw_generic_mindmap("mindmap_toan6_tiet93_97.png",
        "SƠ ĐỒ TƯ DUY ÔN TẬP TỔNG HỢP CUỐI HỌC KÌ II: TOÁN 6",
        "(Môn Toán 6 - Số học & Thống kê - Tiết 93-97 - Tuần 33, 34)",
        "ÔN TẬP CUỐI HKII", "SỐ HỌC - THỐNG KÊ - XÁC SUẤT",
        [
            ("PHÂN SỐ (CHƯƠNG VI)", ["• Khái niệm, rút gọn, quy đồng, so sánh phân số", "• 4 phép tính: cộng, trừ, nhân, chia phân số", "• Hai bài toán cơ bản về phân số", "• Hỗn số dương và tính toán hợp lí"], 18, 70, "#2563EB", "#DBEAFE"),
            ("SỐ THẬP PHÂN (CHƯƠNG VII)", ["• Khái niệm số thập phân âm, dương", "• 4 phép toán với số thập phân có dấu", "• Làm tròn và ước lượng kết quả", "• Tỉ số, tỉ số phần trăm và tỉ lệ xích"], 82, 70, "#059669", "#D1FAE5"),
            ("DỮ LIỆU & BIỂU ĐỒ (CHƯƠNG IX)", ["• Thu thập và phân loại dữ liệu", "• Đọc và vẽ biểu đồ tranh, biểu đồ cột đơn", "• Đọc và phân tích biểu đồ cột kép", "• Đánh giá tính hợp lí của dữ liệu thống kê"], 18, 24, "#7C3AED", "#EDE9FE"),
            ("XÁC SUẤT THỰC NGHIỆM", ["• Liệt kê các kết quả có thể", "• Nhận biết sự kiện xảy ra / không xảy ra", "• Tính xác suất thực nghiệm trong trò chơi", "• Rèn kỹ năng làm bài kiểm tra học kì đạt điểm 10"], 82, 24, "#DC2626", "#FEE2E2")
        ])

    # 14. Tiet 99: Bai tap cuoi chuong IX Du lieu va xac suat
    draw_generic_mindmap("mindmap_toan6_tiet99.png",
        "SƠ ĐỒ TƯ DUY TỔNG KẾT CHƯƠNG IX: DỮ LIỆU VÀ XÁC SUẤT",
        "(Môn Toán 6 - Tiết 99 - Tuần 35)",
        "TỔNG KẾT CHƯƠNG IX", "DỮ LIỆU & XÁC SUẤT THỰC NGHIỆM",
        [
            ("THU THẬP & BIỂU DIỄN", ["• Phương pháp thu thập dữ liệu khách quan", "• Lập bảng thống kê tần số", "• Chọn dạng biểu đồ phù hợp (tranh, cột đơn, cột kép)", "• Hoàn thiện các thành phần của biểu đồ"], 18, 70, "#2563EB", "#DBEAFE"),
            ("PHÂN TÍCH THỐNG KÊ", ["• Đọc số liệu cao nhất, thấp nhất", "• Tính tổng số lượng, tỉ lệ phần trăm", "• Nhận xét xu thế biến động tăng/giảm", "• Phát hiện số liệu bất thường không hợp lí"], 82, 70, "#059669", "#D1FAE5"),
            ("KẾT QUẢ & SỰ KIỆN", ["• Liệt kê không gian kết quả của phép thử", "• Xác định sự kiện cần quan tâm", "• Kiểm đếm số lần sự kiện xuất hiện", "• Phân biệt sự kiện ngẫu nhiên, chắc chắn, không thể"], 18, 24, "#D97706", "#FEF3C7"),
            ("XÁC SUẤT THỰC NGHIỆM", ["• Tính tỉ số: (Số lần thuận lợi) / (Tổng số lần lặp)", "• Biểu diễn xác suất bằng phân số tối giản hoặc %", "• Ý nghĩa thực tiễn trong đánh giá rủi ro", "• Ứng dụng trong trò chơi dân gian và thể thao"], 82, 24, "#DC2626", "#FEE2E2")
        ])

if __name__ == "__main__":
    generate_all()
    print("Hoàn tất tạo 14 ảnh Mindmap vector 300 DPI môn Toán 6 HK2!")
