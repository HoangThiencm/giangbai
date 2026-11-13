# -*- coding: utf-8 -*-
"""
Script sinh 8 Sơ đồ tư duy Mindmap vector 300 DPI cho môn Toán 8 (Tuần 13 - 18)
"""
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Toan8/mindmaps"
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

def draw_tiet26():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: PHÂN TÍCH ĐA THỨC THÀNH NHÂN TỬ",
                                "(Môn Toán 8 - Đại số - Tiết 26 - Tuần 13)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#2563EB", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "PHÂN TÍCH ĐA THỨC", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "THÀNH NHÂN TỬ", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. ĐẶT NHÂN TỬ CHUNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Công thức: A.B + A.C = A.(B + C)\n• Tìm nhân tử chung về hệ số (ƯCLN)\n• Tìm nhân tử chung về biến (lũy thừa nhỏ nhất)\n  Ví dụ: 6x^2.y - 9x.y^2 = 3xy(2x - 3y)", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. DÙNG HẰNG ĐẲNG THỨC", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Hiệu hai bình phương: A^2 - B^2 = (A-B)(A+B)\n• Bình phương tổng/hiệu: (A +/- B)^2\n• Tổng/hiệu hai lập phương: A^3 +/- B^3\n  Ví dụ: x^2 - 4 = (x - 2)(x + 2)", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. NHÓM HẠNG TỬ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Nhóm các hạng tử có nhân tử chung\n• Nhóm các hạng tử tạo thành hằng đẳng thức\n  Ví dụ: x^2 - y^2 + 2x + 2y\n  = (x - y)(x + y) + 2(x + y) = (x + y)(x - y + 2)", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. PHỐI HỢP NHIỀU PHƯƠNG PHÁP", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(66, 21, "• Thứ tự ưu tiên:\n  1. Đặt nhân tử chung (nếu có)\n  2. Dùng hằng đẳng thức hoặc nhóm\n  3. Tách hạng tử hoặc thêm bớt hạng tử\n• Ứng dụng: Rút gọn phân thức, tìm x, tính nhanh", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan8_tiet26.png"), dpi=300)
    plt.close()

def draw_tiet27():
    fig, ax = create_base_canvas("SƠ ĐỒ TỔNG KẾT BÀI TẬP CUỐI CHƯƠNG II: HẰNG ĐẲNG THỨC & ỨNG DỤNG",
                                "(Môn Toán 8 - Đại số - Tiết 27 - Tuần 13)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#7C3AED", fc="#F3E8FF", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TỔNG KẾT CHƯƠNG II", ha='center', va='center', fontsize=12, fontweight='bold', color="#6D28D9")
    ax.text(50, 47, "HẰNG ĐẲNG THỨC ĐÁNG NHỚ", ha='center', va='center', fontsize=11, fontweight='bold', color="#7C3AED")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. BẢY HẰNG ĐẲNG THỨC ĐÁNG NHỚ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• (A + B)^2 = A^2 + 2AB + B^2\n• (A - B)^2 = A^2 - 2AB + B^2\n• A^2 - B^2 = (A - B)(A + B)\n• (A +/- B)^3 = A^3 +/- 3A^2B + 3AB^2 +/- B^3\n• A^3 +/- B^3 = (A +/- B)(A^2 -/+ AB + B^2)", fontsize=8.5, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. PHÂN TÍCH ĐA THỨC THÀNH NHÂN TỬ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Phương pháp đặt nhân tử chung\n• Phương pháp dùng hằng đẳng thức\n• Phương pháp nhóm hạng tử\n• Phương pháp tách/thêm bớt hạng tử bậc hai", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. CÁC DẠNG BÀI TẬP TRỌNG TÂM", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(66, 75.5, "• Khai triển và rút gọn biểu thức\n• Tính nhanh giá trị biểu thức tại x = x0\n• Tìm x (đưa về phương trình tích A.B = 0)\n• Chứng minh biểu thức luôn dương/âm", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. ỨNG DỤNG THỰC TẾ & CÔNG NGHỆ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Tính nhẩm bình phương số tận cùng là 5\n• Bài toán diện tích, thể tích hình học đại số\n• Sử dụng lệnh Factor, Expand trong phần mềm GeoGebra", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan8_tiet27.png"), dpi=300)
    plt.close()

def draw_tiet34():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: DỮ LIỆU VÀ BIỂU ĐỒ THỐNG KÊ",
                                "(Môn Toán 8 - Thống kê - Tiết 34 - Tuần 16)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#059669", fc="#D1FAE5", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "DỮ LIỆU & BIỂU ĐỒ", ha='center', va='center', fontsize=12, fontweight='bold', color="#047857")
    ax.text(50, 47, "THỐNG KÊ TOÁN 8", ha='center', va='center', fontsize=11, fontweight='bold', color="#059669")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. THU THẬP & PHÂN LOẠI DỮ LIỆU", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Thu thập trực tiếp (quan sát, phỏng vấn, khảo sát)\n• Thu thập gián tiếp (sách báo, Internet, CSDL)\n• Dữ liệu định tính (chữ, không đo bằng số)\n• Dữ liệu định lượng (số liệu đo đếm được)", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. CÁC DẠNG BIỂU ĐỒ BIỂU DIỄN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Biểu đồ cột đơn/cột kép: So sánh số liệu các nhóm\n• Biểu đồ đoạn thẳng: Thể hiện xu hướng biến động\n• Biểu đồ hình quạt tròn: Thể hiện cơ cấu, tỉ lệ phần trăm", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. PHÂN TÍCH SỐ LIỆU DỰA VÀO BIỂU ĐỒ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Đọc giá trị lớn nhất, nhỏ nhất, trung bình\n• Nhận xét xu hướng tăng, giảm theo thời gian\n• Rút ra kết luận hoặc dự đoán xu thế tương lai", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. CÔNG CỤ SỐ HỖ TRỢ (NLS)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Google Forms: Tạo phiếu khảo sát số trực tuyến\n• Excel / Google Sheets: Lập bảng số liệu và tự động vẽ\n  biểu đồ cột, quạt tròn, đường biểu diễn", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan8_tiet34.png"), dpi=300)
    plt.close()

def draw_tiet35():
    fig, ax = create_base_canvas("SƠ ĐỒ TỔNG KẾT BÀI TẬP CUỐI CHƯƠNG V: DỮ LIỆU VÀ BIỂU ĐỒ",
                                "(Môn Toán 8 - Thống kê - Tiết 35 - Tuần 16)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#0284C7", fc="#E0F2FE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TỔNG KẾT CHƯƠNG V", ha='center', va='center', fontsize=12, fontweight='bold', color="#0369A1")
    ax.text(50, 47, "DỮ LIỆU VÀ BIỂU ĐỒ", ha='center', va='center', fontsize=11, fontweight='bold', color="#0284C7")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. DỮ LIỆU THỐNG KÊ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(6, 75.5, "• Dữ liệu định tính (danh mục, thứ bậc)\n• Dữ liệu định lượng (rời rạc, liên tục)\n• Tính đại diện và độ tin cậy của dữ liệu", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. LỰA CHỌN BIỂU ĐỒ PHÙ HỢP", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• Biểu đồ cột: So sánh đại lượng rời rạc\n• Biểu đồ đoạn thẳng: Theo dõi biến đổi liên tục\n• Biểu đồ quạt tròn: Thể hiện cơ cấu tỉ lệ phần trăm", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. ĐỌC VÀ DIỄN GIẢI SỐ LIỆU", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Phát hiện các điểm bất thường hoặc sai lệch\n• Tính tỉ số, phần trăm tăng trưởng\n• Trả lời các câu hỏi thực tế dựa trên đồ thị", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. VẬN DỤNG THỰC TIỄN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Phân tích số liệu thời tiết, khí hậu Việt Nam\n• Thống kê kết quả rèn luyện học tập của học sinh\n• Phân tích doanh số kinh doanh và thị phần", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan8_tiet35.png"), dpi=300)
    plt.close()

def draw_tiet37_39():
    fig, ax = create_base_canvas("SƠ ĐỒ HỆ THỐNG HÓA ÔN TẬP CUỐI HỌC KÌ I - ĐẠI SỐ & THỐNG KÊ 8",
                                "(Tổng kết Chương I: Đa thức - Chương II: Hằng đẳng thức - Chương V: Dữ liệu & Biểu đồ)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#1E40AF", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "ÔN TẬP CUỐI HỌC KÌ I", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "ĐẠI SỐ & THỐNG KÊ 8", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. ĐA THỨC NHIỀU BIẾN (CHƯƠNG I)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Đơn thức, đơn thức thu gọn, bậc của đơn thức\n• Cộng, trừ đa thức nhiều biến\n• Nhân đơn thức với đa thức, đa thức với đa thức\n• Chia đa thức cho đơn thức", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. HẰNG ĐẲNG THỨC (CHƯƠNG II)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(6, 21, "• 7 Hằng đẳng thức đáng nhớ\n• 4 Phương pháp phân tích đa thức thành nhân tử\n• Tính nhanh giá trị biểu thức và giải phương trình tích", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. THỐNG KÊ & DỮ LIỆU (CHƯƠNG V)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Thu thập và phân loại dữ liệu định tính, định lượng\n• Biểu diễn dữ liệu bằng biểu đồ cột, đoạn thẳng, quạt tròn\n• Phân tích số liệu và giải thích ý nghĩa thực tiễn", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. NĂNG LỰC SỐ & CÔNG NGHỆ (NLS)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(66, 21, "• Sử dụng GeoGebra tính toán đa thức (Expand, Factor)\n• Sử dụng bảng tính Excel lập bảng và vẽ biểu đồ\n• Máy tính cầm tay tính giá trị đa thức nhanh", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan8_tiet37_39.png"), dpi=300)
    plt.close()

def draw_hinh_tiet25():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: ĐỊNH LÍ THALÈS & TÍNH CHẤT PHÂN GIÁC",
                                "(Môn Toán 8 - Hình học - Tiết 25 - Tuần 13)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#D97706", fc="#FEF3C7", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "ĐỊNH LÍ THALÈS", ha='center', va='center', fontsize=12, fontweight='bold', color="#B45309")
    ax.text(50, 47, "TRUNG BÌNH & PHÂN GIÁC", ha='center', va='center', fontsize=11, fontweight='bold', color="#D97706")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. ĐỊNH LÍ THALÈS TRONG TAM GIÁC", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Thuận: Nếu MN // BC thì AM/AB = AN/AC = MN/BC\n• Đảo: Nếu AM/AB = AN/AC thì MN // BC\n• Hệ quả: MN // BC tạo thành tam giác mới\n  có 3 cạnh tương ứng tỉ lệ với 3 cạnh tam giác đã cho", fontsize=8.5, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. ĐƯỜNG TRUNG BÌNH TAM GIÁC", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(6, 21, "• Định nghĩa: Đoạn thẳng nối trung điểm hai cạnh tam giác\n• Tính chất: Đường trung bình song song với cạnh thứ ba\n  và bằng nửa độ dài cạnh ấy: MN // BC và MN = 1/2 BC", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. TÍNH CHẤT ĐƯỜNG PHÂN GIÁC", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    ax.text(66, 75.5, "• Trong tam giác, đường phân giác của một góc\n  chia cạnh đối diện thành hai đoạn thẳng tỉ lệ\n  với hai cạnh kề hai đoạn ấy:\n  AD là phân giác góc A -> DB/DC = AB/AC", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. ỨNG DỤNG TÍNH TOÁN & THỰC TẾ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Tính độ dài đoạn thẳng chưa biết\n• Chứng minh hai đường thẳng song song\n• Đo gián tiếp khoảng cách giữa hai điểm qua vật cản", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan8_hinh_tiet25.png"), dpi=300)
    plt.close()

def draw_hinh_tiet26_27():
    fig, ax = create_base_canvas("SƠ ĐỒ TỔNG KẾT BÀI TẬP CUỐI CHƯƠNG IV: ĐỊNH LÍ THALÈS",
                                "(Môn Toán 8 - Hình học - Tiết 26, 27 - Tuần 14, 15)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#7C3AED", fc="#F3E8FF", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TỔNG KẾT CHƯƠNG IV", ha='center', va='center', fontsize=12, fontweight='bold', color="#6D28D9")
    ax.text(50, 47, "ĐỊNH LÍ THALÈS TRONG TAM GIÁC", ha='center', va='center', fontsize=11, fontweight='bold', color="#7C3AED")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. ĐOẠN THẲNG TỈ LỆ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Tỉ số hai đoạn thẳng: AB/CD\n• Đoạn thẳng tỉ lệ: AB/CD = A'B'/C'D'\n• Tính chất của tỉ lệ thức", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. ĐỊNH LÍ THALÈS & HỆ QUẢ", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(6, 21, "• Định lí thuận: MN // BC -> AM/AB = AN/AC\n• Định lí đảo: AM/AB = AN/AC -> MN // BC\n• Hệ quả: MN // BC -> AM/AB = AN/AC = MN/BC", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. ĐƯỜNG TRUNG BÌNH & PHÂN GIÁC", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(66, 75.5, "• Đường trung bình: MN // BC và MN = 1/2 BC\n• Tính chất phân giác: DB/DC = AB/AC\n• Áp dụng cho cả phân giác ngoài", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. GIẢI QUYẾT BÀI TOÁN THỰC TIỄN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Đo chiều cao cây cối, tòa nhà qua bóng nắng\n• Đo bề rộng khúc sông bằng giác kế và cọc tiêu\n• Mô phỏng hình học bằng phần mềm GeoGebra", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan8_hinh_tiet26_27.png"), dpi=300)
    plt.close()

def draw_hinh_tiet29():
    fig, ax = create_base_canvas("SƠ ĐỒ HỆ THỐNG HÓA ÔN TẬP CUỐI HỌC KÌ I - HÌNH HỌC 8",
                                "(Tổng kết Chương III: Tứ giác & Chương IV: Định lí Thalès)")
    c = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#1E40AF", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "ÔN TẬP CUỐI HỌC KÌ I", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "PHẦN HÌNH HỌC 8", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. CÁC TỨ GIÁC ĐẶC BIỆT (CHƯƠNG III)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    ax.text(6, 75.5, "• Hình thang, hình thang cân\n• Hình bình hành, hình thoi\n• Hình chữ nhật, hình vuông\n• Dấu hiệu nhận biết và tính chất đường chéo", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. ĐỊNH LÍ THALÈS (CHƯƠNG IV)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    ax.text(6, 21, "• Định lí thuận, định lí đảo và hệ quả\n• Đoạn thẳng tỉ lệ trong tam giác\n• Phương pháp chứng minh hai đường thẳng song song", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b3 = patches.FancyBboxPatch((64, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 83.5, "3. ĐƯỜNG TRUNG BÌNH & PHÂN GIÁC", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    ax.text(66, 75.5, "• Đường trung bình của tam giác (MN // BC, MN = 1/2 BC)\n• Tính chất đường phân giác trong và ngoài tam giác\n• Kĩ năng tính độ dài đoạn thẳng", fontsize=8.8, color="#0F172A", linespacing=1.3)

    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", ec="#DC2626", fc="#FEE2E2", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. PHƯƠNG PHÁP CHỨNG MINH HÌNH HỌC", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B91C1C")
    ax.text(66, 21, "• Chứng minh tứ giác là hình đặc biệt\n• Chứng minh đẳng thức tích a.b = c.d qua tỉ số Thalès\n• Chứng minh 3 điểm thẳng hàng, 3 đường đồng quy", fontsize=8.8, color="#0F172A", linespacing=1.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "mindmap_toan8_hinh_tiet29.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    draw_tiet26()
    draw_tiet27()
    draw_tiet34()
    draw_tiet35()
    draw_tiet37_39()
    draw_hinh_tiet25()
    draw_hinh_tiet26_27()
    draw_hinh_tiet29()
    print(">>> HOÀN TẤT SINH 8 MINDMAP TOÁN 8 VECTOR 300 DPI! <<<")
