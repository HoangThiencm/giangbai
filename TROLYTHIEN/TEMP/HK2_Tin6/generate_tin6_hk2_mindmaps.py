# -*- coding: utf-8 -*-
"""
Script sinh 2 Sơ đồ tư duy Mindmap vector 300 DPI cho môn Tin học 6 (Học kì II - Tuần 19 đến 35):
- mindmap_tin6_tiet27_giuahk2.png
- mindmap_tin6_tiet34_cuoihk2.png
"""
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/HK2_Tin6/mindmaps"
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

def draw_tiet27():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY ÔN TẬP GIỮA HỌC KÌ II: ỨNG DỤNG TIN HỌC",
                                "(Môn Tin học 6 - Tiết 27 - Tuần 27)")
    c = patches.FancyBboxPatch((34, 43), 32, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#2563EB", fc="#DBEAFE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "ỨNG DỤNG TIN HỌC", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "ÔN TẬP GIỮA HKII", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    nodes = [
        ("SƠ ĐỒ TƯ DUY", [
            "• Khái niệm: Công cụ tổ chức và biểu diễn thông tin trực quan",
            "• Thành phần: Chủ đề chính, chủ đề nhánh, từ khóa, hình ảnh",
            "• Phần mềm tạo: XMind, Mindomo, GitMind hoặc vẽ tay",
            "• Lợi ích: Ghi nhớ nhanh, sáng tạo, liên kết kiến thức"
        ], 18, 70, "#059669", "#D1FAE5"),
        ("ĐỊNH DẠNG VĂN BẢN", [
            "• Định dạng ký tự: Phông chữ, cỡ chữ, kiểu chữ, màu sắc",
            "• Định dạng đoạn: Căn lề (trái, phải, giữa, đều), giãn dòng",
            "• Định dạng trang: Hướng giấy (dọc, ngang), lề trang",
            "• Chèn hình ảnh minh họa và điều chỉnh bố cục"
        ], 82, 70, "#D97706", "#FEF3C7"),
        ("TRÌNH BÀY BẢNG BIỂU", [
            "• Tạo bảng: Chọn số hàng và số cột (Insert Table)",
            "• Thao tác: Chèn thêm hàng/cột, xóa hàng/cột, gộp ô (Merge)",
            "• Căn lề nội dung trong ô và định dạng đường viền bảng",
            "• Lợi ích: Trình bày số liệu khoa học, dễ so sánh"
        ], 18, 24, "#7C3AED", "#EDE9FE"),
        ("TÌM KIẾM VÀ THAY THẾ", [
            "• Công cụ Find (Ctrl + F): Tìm nhanh từ/cụm từ trong văn bản",
            "• Công cụ Replace (Ctrl + H): Thay thế từ cũ bằng từ mới",
            "• Chế độ: Thay thế từng từ (Replace) hoặc tất cả (Replace All)",
            "• Tác dụng: Nhanh chóng, chính xác, tiết kiệm thời gian"
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
    out_path = os.path.join(OUT_DIR, "mindmap_tin6_tiet27_giuahk2.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

def draw_tiet34():
    fig, ax = create_base_canvas("SƠ ĐỒ TƯ DUY TỔNG KẾT HỌC KÌ II: TIN HỌC 6",
                                "(Môn Tin học 6 - Tiết 34 - Tuần 34)")
    c = patches.FancyBboxPatch((33, 43), 34, 14, boxstyle="round,pad=1.2,rounding_size=2", ec="#7C3AED", fc="#EDE9FE", lw=2.5)
    ax.add_patch(c)
    ax.text(50, 51.5, "TỔNG KẾT HỌC KÌ II", ha='center', va='center', fontsize=12, fontweight='bold', color="#4C1D95")
    ax.text(50, 47, "TIN HỌC 6 TOÀN DIỆN", ha='center', va='center', fontsize=11, fontweight='bold', color="#7C3AED")

    nodes = [
        ("AN TOÀN THÔNG TIN", [
            "• Tác hại: Rò rỉ thông tin cá nhân, bị lừa đảo, mã độc",
            "• Quy tắc an toàn: Đặt mật khẩu mạnh, không chia sẻ MK",
            "• Ứng xử trên mạng: Tôn trọng người khác, không lan truyền tin giả",
            "• Bản quyền nội dung và quyền tác giả số"
        ], 18, 70, "#2563EB", "#DBEAFE"),
        ("SOẠN THẢO VĂN BẢN", [
            "• Định dạng văn bản hoàn chỉnh (ký tự, đoạn, trang, ảnh)",
            "• Trình bày dữ liệu khoa học bằng bảng biểu (Table)",
            "• Công cụ tìm kiếm và thay thế tự động (Find & Replace)",
            "• Hoàn thiện hồ sơ lưu niệm, báo tường, tập san số"
        ], 82, 70, "#059669", "#D1FAE5"),
        ("THUẬT TOÁN", [
            "• Khái niệm: Dãy các thao tác rõ ràng để giải quyết vấn đề",
            "• Ba đặc trưng: Xác định, hữu hạn, đúng đắn",
            "• Hai cách mô tả: Liệt kê các bước hoặc Sơ đồ khối",
            "• Các khối: Bắt đầu/Kết thúc (oval), Thao tác (chữ nhật), Điều kiện (thoi)"
        ], 18, 24, "#D97706", "#FEF3C7"),
        ("CẤU TRÚC & CHƯƠNG TRÌNH", [
            "• Ba cấu trúc điều khiển: Tuần tự, Rẽ nhánh (Nếu...thì), Lặp",
            "• Chương trình máy tính: Dãy các lệnh viết bằng ngôn ngữ lập trình",
            "• Làm quen môi trường lập trình trực quan (Scratch)",
            "• Ghép khối lệnh điều khiển nhân vật chuyển động, tính toán"
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
    out_path = os.path.join(OUT_DIR, "mindmap_tin6_tiet34_cuoihk2.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(" -> Đã tạo:", out_path)

if __name__ == "__main__":
    draw_tiet27()
    draw_tiet34()
    print("Hoàn tất tạo 2 ảnh Mindmap vector 300 DPI môn Tin học 6 HK2!")
