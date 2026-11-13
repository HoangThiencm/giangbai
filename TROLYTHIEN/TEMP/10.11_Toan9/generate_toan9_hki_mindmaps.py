# -*- coding: utf-8 -*-
"""
Script sinh 6 Sơ đồ tư duy Mindmap vector 300 DPI cho môn Toán 9 (Tuần 13 - 18)
- mindmap_toan9_tiet35.png
- mindmap_toan9_tiet36_37.png
- mindmap_toan9_tiet38_39.png
- mindmap_toan9_hinh_tiet23.png
- mindmap_toan9_hinh_tiet24_25.png
- mindmap_toan9_hinh_tiet26_27.png
"""
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/10.11_Toan9/mindmaps"
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

def draw_tiet35():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: CĂN BẬC HAI VÀ CĂN BẬC BA",
                                "(Môn Toán 9 - Đại số - Tiết 35 - Tuần 15)")
    c = patches.FancyBboxPatch((34, 43), 32, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#2563EB", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "CĂN BẬC HAI & CĂN BẬC BA", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "LUYỆN TẬP BIẾN ĐỔI", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    nodes = [
        ("KHÁI NIỆM & ĐIỀU KIỆN", [
            "• Căn bậc hai số học: x = sqrt(a) (x >= 0, x^2 = a)",
            "• Điều kiện có nghĩa sqrt(A): A >= 0",
            "• Căn bậc ba: x = cbrt(a) <=> x^3 = a (với mọi a)",
            "• Khai căn số học bằng máy tính cầm tay"
        ], 18, 70, "#059669", "#D1FAE5"),
        ("KHAI PHƯƠNG TÍCH & THƯƠNG", [
            "• sqrt(A . B) = sqrt(A) . sqrt(B) (A >= 0, B >= 0)",
            "• sqrt(A / B) = sqrt(A) / sqrt(B) (A >= 0, B > 0)",
            "• Hằng đẳng thức: sqrt(A^2) = |A|",
            "• Chú ý bỏ dấu trị tuyệt đối theo dấu của A"
        ], 82, 70, "#D97706", "#FEF3C7"),
        ("ĐƯA THỪA SỐ RA / VÀO CĂN", [
            "• sqrt(A^2 . B) = |A| . sqrt(B) (B >= 0)",
            "• Nếu A >= 0: A . sqrt(B) = sqrt(A^2 . B)",
            "• Nếu A < 0: A . sqrt(B) = -sqrt(A^2 . B)",
            "• Rút gọn các đơn thức đồng dạng chứa căn"
        ], 18, 24, "#7C3AED", "#EDE9FE"),
        ("TRỤC CĂN THỨC Ở MẪU", [
            "• Dạng căn đơn: A / sqrt(B) = (A . sqrt(B)) / B",
            "• Nhân liên hợp: C / (sqrt(A) +- B)",
            "  = C(sqrt(A) -+ B) / (A - B^2)",
            "• Nhân liên hợp hai căn: sqrt(A) - sqrt(B)"
        ], 82, 24, "#DC2626", "#FEE2E2")
    ]

    for title, lines, x, y, ec, fc in nodes:
        b = patches.FancyBboxPatch((x - 16, y - 11), 32, 22, boxstyle="round,pad=1,rounding_size=1.5", ec=ec, fc=fc, lw=2)
        ax.add_patch(b)
        ax.text(x, y + 8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=ec)
        ax.plot([x - 14, x + 14], [y + 5.5, y + 5.5], color=ec, lw=1)
        for idx, line in enumerate(lines):
            ax.text(x - 14, y + 2.5 - idx * 4.2, line, ha='left', va='center', fontsize=8.8, color="#1E293B")
        cx = 50 + (16 if x > 50 else -16)
        cy = 50 + (7 if y > 50 else -7)
        ax.annotate("", xy=(x + (-16 if x > 50 else 16), y), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=2, connectionstyle="arc3,rad=0.1"))

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "mindmap_toan9_tiet35.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

def draw_tiet36_37():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY BÀI TẬP CUỐI CHƯƠNG III: CĂN BẬC HAI VÀ CĂN BẬC BA",
                                "(Môn Toán 9 - Đại số - Tiết 36, 37 - Tuần 15, 16)")
    c = patches.FancyBboxPatch((33, 43), 34, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#7C3AED", fc="#EDE9FE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TỔNG KẾT CHƯƠNG III", ha='center', va='center', fontsize=12, fontweight='bold', color="#4C1D95")
    ax.text(50, 47, "CĂN BẬC HAI & BẬC BA", ha='center', va='center', fontsize=11, fontweight='bold', color="#7C3AED")

    nodes = [
        ("CĂN BẬC HAI & BẬC BA", [
            "• sqrt(A) xác định <=> A >= 0; cbrt(A) xác định với mọi A",
            "• sqrt(A^2) = |A|; (sqrt(A))^2 = A (A >= 0)",
            "• (cbrt(A))^3 = cbrt(A^3) = A",
            "• So sánh: a < b <=> sqrt(a) < sqrt(b) <=> cbrt(a) < cbrt(b)"
        ], 18, 70, "#2563EB", "#DBEAFE"),
        ("CÁC PHÉP BIẾN ĐỔI", [
            "• Khai phương tích và thương",
            "• Đưa thừa số ra ngoài / vào trong dấu căn",
            "• Khử mẫu của biểu thức lấy căn",
            "• Trục căn thức ở mẫu bằng nhân liên hợp"
        ], 82, 70, "#059669", "#D1FAE5"),
        ("RÚT GỌN BIỂU THỨC", [
            "• Bước 1: Tìm điều kiện xác định (ĐKXĐ)",
            "• Bước 2: Phân tích mẫu thành nhân tử, quy đồng",
            "• Bước 3: Rút gọn tử và mẫu bằng hằng đẳng thức",
            "• Bước 4: Đối chiếu ĐKXĐ và kết luận"
        ], 18, 24, "#D97706", "#FEF3C7"),
        ("ỨNG DỤNG BÀI TOÁN", [
            "• Tính giá trị biểu thức tại x = x0 (thỏa ĐKXĐ)",
            "• Giải phương trình vô tỉ: sqrt(A) = B (B >= 0, A = B^2)",
            "• Tìm x để biểu thức nhận giá trị nguyên",
            "• Tìm giá trị lớn nhất / nhỏ nhất của biểu thức chứa căn"
        ], 82, 24, "#DC2626", "#FEE2E2")
    ]

    for title, lines, x, y, ec, fc in nodes:
        b = patches.FancyBboxPatch((x - 16, y - 11), 32, 22, boxstyle="round,pad=1,rounding_size=1.5", ec=ec, fc=fc, lw=2)
        ax.add_patch(b)
        ax.text(x, y + 8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=ec)
        ax.plot([x - 14, x + 14], [y + 5.5, y + 5.5], color=ec, lw=1)
        for idx, line in enumerate(lines):
            ax.text(x - 14, y + 2.5 - idx * 4.2, line, ha='left', va='center', fontsize=8.8, color="#1E293B")
        cx = 50 + (17 if x > 50 else -17)
        cy = 50 + (7 if y > 50 else -7)
        ax.annotate("", xy=(x + (-16 if x > 50 else 16), y), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=2, connectionstyle="arc3,rad=0.1"))

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "mindmap_toan9_tiet36_37.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

def draw_tiet38_39():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY ÔN TẬP HỌC KÌ I: ĐẠI SỐ 9",
                                "(Môn Toán 9 - Đại số - Tiết 38, 39 - Tuần 16, 17)")
    c = patches.FancyBboxPatch((33, 43), 34, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#DC2626", fc="#FEE2E2", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "ÔN TẬP HỌC KÌ I", ha='center', va='center', fontsize=12, fontweight='bold', color="#991B1B")
    ax.text(50, 47, "ĐẠI SỐ 9 TOÀN DIỆN", ha='center', va='center', fontsize=11, fontweight='bold', color="#DC2626")

    nodes = [
        ("CHƯƠNG I: PHƯƠNG TRÌNH & HỆ PT", [
            "• Phương trình bậc nhất hai ẩn: ax + by = c",
            "• Hệ hai phương trình bậc nhất hai ẩn: {ax+by=c; a'x+b'y=c'}",
            "• Phương pháp giải: Thế hoặc Cộng đại số",
            "• Giải toán bằng cách lập hệ phương trình (toán chuyển động, năng suất)"
        ], 18, 70, "#2563EB", "#DBEAFE"),
        ("CHƯƠNG II: BẤT ĐẲNG THỨC & BPT", [
            "• Tính chất BĐT: Cộng cùng số; Nhân số dương/âm",
            "• Bất phương trình bậc nhất 1 ẩn: ax + b > 0 (hoặc <, >=, <=)",
            "• Quy tắc đổi dấu chiều BPT khi nhân/chia số âm",
            "• Biểu diễn tập nghiệm trên trục số"
        ], 82, 70, "#059669", "#D1FAE5"),
        ("CHƯƠNG III: CĂN THỨC", [
            "• Hằng đẳng thức: sqrt(A^2) = |A|",
            "• Khai phương tích và thương; Đưa thừa số ra/vào căn",
            "• Trục căn thức ở mẫu bằng biểu thức liên hợp",
            "• Căn bậc ba: Tính chất và khai căn"
        ], 18, 24, "#7C3AED", "#EDE9FE"),
        ("KĨ NĂNG LÀM BÀI THI HKI", [
            "• Luôn đặt ĐKXĐ đầu tiên cho căn và mẫu",
            "• Rút gọn biểu thức cẩn thận từng phân thức",
            "• Không kết luận tập nghiệm S = {...} hình thức",
            "• Đối chiếu điều kiện và trả lời rõ ràng"
        ], 82, 24, "#D97706", "#FEF3C7")
    ]

    for title, lines, x, y, ec, fc in nodes:
        b = patches.FancyBboxPatch((x - 16, y - 11), 32, 22, boxstyle="round,pad=1,rounding_size=1.5", ec=ec, fc=fc, lw=2)
        ax.add_patch(b)
        ax.text(x, y + 8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=ec)
        ax.plot([x - 14, x + 14], [y + 5.5, y + 5.5], color=ec, lw=1)
        for idx, line in enumerate(lines):
            ax.text(x - 14, y + 2.5 - idx * 4.2, line, ha='left', va='center', fontsize=8.8, color="#1E293B")
        cx = 50 + (17 if x > 50 else -17)
        cy = 50 + (7 if y > 50 else -7)
        ax.annotate("", xy=(x + (-16 if x > 50 else 16), y), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=2, connectionstyle="arc3,rad=0.1"))

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "mindmap_toan9_tiet38_39.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

def draw_hinh_tiet23():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: VỊ TRÍ TƯƠNG ĐỐI ĐƯỜNG THẲNG & ĐƯỜNG TRÒN",
                                "(Môn Toán 9 - Hình học - Tiết 23 - Tuần 15)")
    c = patches.FancyBboxPatch((32, 43), 36, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#059669", fc="#D1FAE5", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "VỊ TRÍ TƯƠNG ĐỐI", ha='center', va='center', fontsize=12, fontweight='bold', color="#065F46")
    ax.text(50, 47, "ĐƯỜNG THẲNG & ĐƯỜNG TRÒN", ha='center', va='center', fontsize=11, fontweight='bold', color="#059669")

    nodes = [
        ("ĐƯỜNG THẲNG & ĐƯỜNG TRÒN", [
            "• Cắt nhau: d < R (2 điểm chung, cát tuyến)",
            "• Tiếp xúc: d = R (1 điểm chung duy nhất, tiếp tuyến)",
            "• Không giao nhau: d > R (0 điểm chung)",
            "• d: Khoảng cách từ tâm O đến đường thẳng delta"
        ], 18, 70, "#2563EB", "#DBEAFE"),
        ("TÍNH CHẤT TIẾP TUYẾN", [
            "• Định lí: Tiếp tuyến vuông góc bán kính tại tiếp điểm",
            "• Dấu hiệu: Đi qua 1 điểm thuộc (O) và vuông góc bán kính",
            "• Tính chất 2 tiếp tuyến cắt nhau tại M:",
            "  MA = MB; MO là phân giác góc AMB và AOB"
        ], 82, 70, "#D97706", "#FEF3C7"),
        ("VỊ TRÍ HAI ĐƯỜNG TRÒN", [
            "• Ngoài nhau: d > R + r (0 điểm chung)",
            "• Tiếp xúc ngoài: d = R + r; Tiếp xúc trong: d = R - r",
            "• Cắt nhau: R - r < d < R + r (2 điểm chung A, B)",
            "• Đựng nhau: d < R - r (O' nằm trong (O))"
        ], 18, 24, "#7C3AED", "#EDE9FE"),
        ("TÍNH CHẤT ĐƯỜNG NỐI TÂM", [
            "• Đường nối tâm OO' là trục đối xứng của hình",
            "• Tiếp xúc nhau: Tiếp điểm nằm trên đường nối tâm",
            "• Cắt nhau tại A, B: OO' là trung trực của dây chung AB",
            "• Vận dụng hệ thức lượng chứng minh vuông góc, đồng dạng"
        ], 82, 24, "#DC2626", "#FEE2E2")
    ]

    for title, lines, x, y, ec, fc in nodes:
        b = patches.FancyBboxPatch((x - 16, y - 11), 32, 22, boxstyle="round,pad=1,rounding_size=1.5", ec=ec, fc=fc, lw=2)
        ax.add_patch(b)
        ax.text(x, y + 8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=ec)
        ax.plot([x - 14, x + 14], [y + 5.5, y + 5.5], color=ec, lw=1)
        for idx, line in enumerate(lines):
            ax.text(x - 14, y + 2.5 - idx * 4.2, line, ha='left', va='center', fontsize=8.8, color="#1E293B")
        cx = 50 + (18 if x > 50 else -18)
        cy = 50 + (7 if y > 50 else -7)
        ax.annotate("", xy=(x + (-16 if x > 50 else 16), y), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=2, connectionstyle="arc3,rad=0.1"))

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "mindmap_toan9_hinh_tiet23.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

def draw_hinh_tiet24_25():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY BÀI TẬP CUỐI CHƯƠNG V: ĐƯỜNG TRÒN",
                                "(Môn Toán 9 - Hình học - Tiết 24, 25 - Tuần 15, 16)")
    c = patches.FancyBboxPatch((34, 43), 32, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#2563EB", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TỔNG KẾT CHƯƠNG V", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "HÌNH HỌC ĐƯỜNG TRÒN", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    nodes = [
        ("SỰ XÁC ĐỊNH ĐƯỜNG TRÒN", [
            "• Tập hợp điểm cách O khoảng R: (O; R)",
            "• Qua 3 điểm không thẳng hàng có 1 đường tròn duy nhất",
            "• Tâm là giao điểm các đường trung trực của tam giác",
            "• Tâm đối xứng là O; Trục đối xứng là mọi đường kính"
        ], 18, 70, "#059669", "#D1FAE5"),
        ("ĐƯỜNG KÍNH VÀ DÂY CUNG", [
            "• Đường kính là dây lớn nhất của đường tròn",
            "• Đường kính vuông góc với dây thì đi qua trung điểm",
            "• Đường kính qua trung điểm dây không qua tâm thì vuông góc",
            "• Dây bằng nhau <=> Cách đều tâm (OH = OK <=> AB = CD)"
        ], 82, 70, "#D97706", "#FEF3C7"),
        ("TIẾP TUYẾN CỦA ĐƯỜNG TRÒN", [
            "• Định nghĩa: Đường thẳng có 1 điểm chung với đường tròn",
            "• Tiếp tuyến vuông góc bán kính tại tiếp điểm",
            "• Tính chất 2 tiếp tuyến cắt nhau: MA = MB; MO là trung trực AB",
            "• Đường tròn nội tiếp tam giác: Tâm là giao các phân giác"
        ], 18, 24, "#7C3AED", "#EDE9FE"),
        ("CUNG VÀ HÌNH QUẠT TRÒN", [
            "• Độ dài cung n độ: l = (pi . R . n) / 180",
            "• Diện tích hình tròn: S = pi . R^2",
            "• Diện tích hình quạt tròn: S = (pi . R^2 . n) / 360",
            "• Diện tích hình vành khuyên: S = pi(R^2 - r^2)"
        ], 82, 24, "#DC2626", "#FEE2E2")
    ]

    for title, lines, x, y, ec, fc in nodes:
        b = patches.FancyBboxPatch((x - 16, y - 11), 32, 22, boxstyle="round,pad=1,rounding_size=1.5", ec=ec, fc=fc, lw=2)
        ax.add_patch(b)
        ax.text(x, y + 8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=ec)
        ax.plot([x - 14, x + 14], [y + 5.5, y + 5.5], color=ec, lw=1)
        for idx, line in enumerate(lines):
            ax.text(x - 14, y + 2.5 - idx * 4.2, line, ha='left', va='center', fontsize=8.8, color="#1E293B")
        cx = 50 + (16 if x > 50 else -16)
        cy = 50 + (7 if y > 50 else -7)
        ax.annotate("", xy=(x + (-16 if x > 50 else 16), y), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=2, connectionstyle="arc3,rad=0.1"))

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "mindmap_toan9_hinh_tiet24_25.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

def draw_hinh_tiet26_27():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY ÔN TẬP HỌC KÌ I: HÌNH HỌC 9",
                                "(Môn Toán 9 - Hình học - Tiết 26, 27 - Tuần 16, 17)")
    c = patches.FancyBboxPatch((33, 43), 34, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#D97706", fc="#FEF3C7", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "ÔN TẬP HỌC KÌ I", ha='center', va='center', fontsize=12, fontweight='bold', color="#92400E")
    ax.text(50, 47, "HÌNH HỌC 9 TOÀN DIỆN", ha='center', va='center', fontsize=11, fontweight='bold', color="#D97706")

    nodes = [
        ("CHƯƠNG IV: HỆ THỨC LƯỢNG", [
            "• b^2 = a . b'; c^2 = a . c'; a^2 = b^2 + c^2 (Pythagore)",
            "• h^2 = b' . c'; b . c = a . h",
            "• 1/h^2 = 1/b^2 + 1/c^2",
            "• Tỉ số lượng giác: sin = đ/h, cos = k/h, tan = đ/k, cot = k/đ"
        ], 18, 70, "#2563EB", "#DBEAFE"),
        ("GIẢI TAM GIÁC VUÔNG", [
            "• Cạnh góc vuông = Cạnh huyền . sin(góc đối) = Cạnh huyền . cos(góc kề)",
            "• Cạnh góc vuông = Cạnh kề . tan(góc đối) = Cạnh kề . cot(góc kề)",
            "• Ứng dụng thực tiễn: Đo chiều cao vật cản, góc nâng, góc hạ",
            "• Tính khoảng cách hai vị trí không tới được"
        ], 82, 70, "#059669", "#D1FAE5"),
        ("CHƯƠNG V: ĐƯỜNG TRÒN", [
            "• Quan hệ vuông góc đường kính và dây cung",
            "• Liên hệ khoảng cách từ tâm đến dây",
            "• Vị trí tương đối của đường thẳng và đường tròn",
            "• Tính chất 2 tiếp tuyến cắt nhau và đường tròn nội tiếp"
        ], 18, 24, "#7C3AED", "#EDE9FE"),
        ("CHỨNG MINH HÌNH HỌC", [
            "• Chứng minh tiếp tuyến: Khoảng cách d = R hoặc Ax vuông góc OA",
            "• Chứng minh 4 điểm cùng thuộc một đường tròn",
            "• Vận dụng tam giác đồng dạng và hệ thức lượng",
            "• Kẻ đường phụ: Đường kính, tiếp tuyến chung, dây chung"
        ], 82, 24, "#DC2626", "#FEE2E2")
    ]

    for title, lines, x, y, ec, fc in nodes:
        b = patches.FancyBboxPatch((x - 16, y - 11), 32, 22, boxstyle="round,pad=1,rounding_size=1.5", ec=ec, fc=fc, lw=2)
        ax.add_patch(b)
        ax.text(x, y + 8, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color=ec)
        ax.plot([x - 14, x + 14], [y + 5.5, y + 5.5], color=ec, lw=1)
        for idx, line in enumerate(lines):
            ax.text(x - 14, y + 2.5 - idx * 4.2, line, ha='left', va='center', fontsize=8.8, color="#1E293B")
        cx = 50 + (17 if x > 50 else -17)
        cy = 50 + (7 if y > 50 else -7)
        ax.annotate("", xy=(x + (-16 if x > 50 else 16), y), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=2, connectionstyle="arc3,rad=0.1"))

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "mindmap_toan9_hinh_tiet26_27.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

if __name__ == "__main__":
    draw_tiet35()
    draw_tiet36_37()
    draw_tiet38_39()
    draw_hinh_tiet23()
    draw_hinh_tiet24_25()
    draw_hinh_tiet26_27()
    print("Hoàn tất tạo 6 ảnh Mindmap vector 300 DPI môn Toán 9!")
