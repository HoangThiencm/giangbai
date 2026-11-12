# -*- coding: utf-8 -*-
"""
Script sinh Sơ đồ tư duy Mindmap vector 300 DPI cho môn Tin học 6:
1. Tiết 09: Ôn tập kiểm tra đánh giá giữa HK1
2. Tiết 11, 12: Bài 6 - Mạng thông tin toàn cầu (World Wide Web)
"""
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình font tiếng Việt và độ phân giải
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = "TROLYTHIEN/TEMP/02.11_Tin6/mindmaps"
os.makedirs(OUT_DIR, exist_ok=True)

def draw_mindmap_tiet09():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header / Title
    ax.text(50, 96, "SƠ ĐỒ HỆ THỐNG HÓA KIẾN THỨC ÔN TẬP GIỮA HỌC KÌ I - TIN HỌC 6", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1E293B')
    ax.text(50, 92.5, "(Chủ đề 1: Máy tính và cộng đồng  |  Chủ đề 2: Mạng máy tính và Internet)", 
            ha='center', va='center', fontsize=11, fontstyle='italic', color='#475569')

    # Central Node
    center_box = patches.FancyBboxPatch((36, 44), 28, 12, boxstyle="round,pad=1.2,rounding_size=2", 
                                        ec="#1E40AF", fc="#DBEAFE", lw=2.5)
    ax.add_patch(center_box)
    ax.text(50, 51, "ÔN TẬP GIỮA HỌC KÌ I", ha='center', va='center', fontsize=13, fontweight='bold', color="#1E3A8A")
    ax.text(50, 47, "TIN HỌC 6 (KNTT)", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")

    # Nhánh 1: Thông tin & Dữ liệu (Top Left)
    ax.annotate('', xy=(24, 76), xytext=(40, 56), 
                arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=2, connectionstyle="arc3,rad=0.15"))
    b1 = patches.FancyBboxPatch((4, 71), 32, 16, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. THÔNG TIN VÀ DỮ LIỆU", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    t1 = ("• Thông tin: Hiểu biết của con người về thế giới\n"
          "• Dữ liệu: Thông tin dưới dạng chữ, số, hình ảnh, âm thanh\n"
          "• Vật mang tin: Phương tiện chứa/truyền dữ liệu (giấy, thẻ nhớ)")
    ax.text(6, 76.5, t1, ha='left', va='center', fontsize=9, color="#0F172A", linespacing=1.3)

    # Nhánh 2: Xử lí thông tin (Bottom Left)
    ax.annotate('', xy=(24, 25), xytext=(40, 44), 
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2, connectionstyle="arc3,rad=-0.15"))
    b2 = patches.FancyBboxPatch((4, 14), 32, 19, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. XỬ LÍ THÔNG TIN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    t2 = ("• Thu nhận thông tin: Nhờ giác quan và thiết bị vào\n"
          "• Lưu trữ thông tin: Ghi lại vào bộ nhớ trong/ngoài\n"
          "• Xử lí thông tin: Bộ não / CPU biến đổi thông tin\n"
          "• Truyền thông tin: Chia sẻ ra ngoài qua màn hình, loa, mạng")
    ax.text(6, 20.5, t2, ha='left', va='center', fontsize=9, color="#0F172A", linespacing=1.3)

    # Nhánh 3: Thông tin trong máy tính (Top Right)
    ax.annotate('', xy=(76, 76), xytext=(60, 56), 
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=2, connectionstyle="arc3,rad=-0.15"))
    b3 = patches.FancyBboxPatch((64, 70), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 84.5, "3. BIỂU DIỄN VÀ ĐO THÔNG TIN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    t3 = ("• Bit (Binary digit): Kí hiệu 0 và 1, đơn vị nhỏ nhất\n"
          "• Mọi thông tin trong máy tính đều biểu diễn bằng dãy bit\n"
          "• Đơn vị đo dung lượng nhớ: Byte (B)\n"
          "• Bội số: 1 Byte = 8 Bit; 1 KB = 1024 B;\n"
          "  1 MB = 1024 KB; 1 GB = 1024 MB; 1 TB = 1024 GB")
    ax.text(66, 76, t3, ha='left', va='center', fontsize=8.8, color="#0F172A", linespacing=1.3)

    # Nhánh 4: Mạng máy tính & Internet (Bottom Right)
    ax.annotate('', xy=(76, 25), xytext=(60, 44), 
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2, connectionstyle="arc3,rad=0.15"))
    b4 = patches.FancyBboxPatch((64, 14), 32, 20, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 30.5, "4. MẠNG MÁY TÍNH VÀ INTERNET", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    t4 = ("• Mạng máy tính: Tập hợp các máy tính kết nối với nhau\n"
          "• Thành phần: Thiết bị đầu cuối, thiết bị kết nối, phần mềm\n"
          "• Thiết bị mạng: Cáp mạng, Switch (bộ chuyển mạch), Access Point\n"
          "• Internet: Mạng toàn cầu kết nối hàng triệu máy tính\n"
          "• Lợi ích: Tra cứu thông tin, thư điện tử, học tập, giải trí")
    ax.text(66, 21, t4, ha='left', va='center', fontsize=8.8, color="#0F172A", linespacing=1.3)

    out_file = os.path.join(OUT_DIR, "mindmap_01_on_tap_giua_hk1_tin6_tiet09.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f" -> Đã tạo Mindmap: {out_file}")

def draw_mindmap_bai06():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header / Title
    ax.text(50, 96, "SƠ ĐỒ TƯ DUY BÀI 6: MẠNG THÔNG TIN TOÀN CẦU (WORLD WIDE WEB)", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1E293B')
    ax.text(50, 92.5, "(Môn Tin học 6 - Bộ sách Kết nối tri thức với cuộc sống - Tuần 11, 12)", 
            ha='center', va='center', fontsize=11, fontstyle='italic', color='#475569')

    # Central Node
    center_box = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", 
                                        ec="#2563EB", fc="#DBEAFE", lw=2.5)
    ax.add_patch(center_box)
    ax.text(50, 52, "MẠNG THÔNG TIN TOÀN CẦU", ha='center', va='center', fontsize=12.5, fontweight='bold', color="#1E3A8A")
    ax.text(50, 48, "WORLD WIDE WEB (WWW)", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")
    ax.text(50, 45, "(Hệ thống thông tin trên Internet)", ha='center', va='center', fontsize=9.5, fontstyle='italic', color="#1E40AF")

    # Nhánh 1: Thông tin trên Internet & WWW (Top Left)
    ax.annotate('', xy=(24, 76), xytext=(40, 57), 
                arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=2, connectionstyle="arc3,rad=0.15"))
    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. WORLD WIDE WEB (WWW)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    t1 = ("• WWW là hệ thống các website liên kết trên Internet\n"
          "• Do Tim Berners-Lee phát minh năm 1989\n"
          "• Là dịch vụ phổ biến nhất trên Internet hiện nay\n"
          "• Giúp tìm kiếm, đọc và chia sẻ thông tin đa phương tiện")
    ax.text(6, 75.5, t1, ha='left', va='center', fontsize=9, color="#0F172A", linespacing=1.3)

    # Nhánh 2: Siêu văn bản & Siêu liên kết (Bottom Left)
    ax.annotate('', xy=(24, 25), xytext=(40, 43), 
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2, connectionstyle="arc3,rad=-0.15"))
    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. SIÊU VĂN BẢN VÀ SIÊU LIÊN KẾT", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    t2 = ("• Siêu văn bản (Hypertext): Văn bản tích hợp chữ,\n"
          "  hình ảnh, âm thanh, video và các liên kết trỏ tới nơi khác\n"
          "• Siêu liên kết (Hyperlink): Đoạn chữ hoặc hình ảnh\n"
          "  cho phép mở sang trang web khác khi nhấp chuột vào\n"
          "• Con trỏ chuột chuyển thành hình bàn tay khi gặp liên kết")
    ax.text(6, 21, t2, ha='left', va='center', fontsize=9, color="#0F172A", linespacing=1.3)

    # Nhánh 3: Trang web, Website, Địa chỉ (Top Right)
    ax.annotate('', xy=(76, 76), xytext=(60, 57), 
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=2, connectionstyle="arc3,rad=-0.15"))
    b3 = patches.FancyBboxPatch((64, 69), 32, 19, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 84.5, "3. TRANG WEB VÀ WEBSITE", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    t3 = ("• Trang web (Webpage): Một siêu văn bản mở trên web\n"
          "• Website: Tập hợp các trang web liên quan, có chung địa chỉ\n"
          "• Trang chủ (Homepage): Trang đầu tiên xuất hiện khi vào website\n"
          "• Địa chỉ website (URL): Tên định danh duy nhất\n"
          "  Ví dụ: https://thieunientienphong.vn ; https://moet.gov.vn")
    ax.text(66, 75.5, t3, ha='left', va='center', fontsize=8.8, color="#0F172A", linespacing=1.3)

    # Nhánh 4: Trình duyệt web (Bottom Right)
    ax.annotate('', xy=(76, 25), xytext=(60, 43), 
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2, connectionstyle="arc3,rad=0.15"))
    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. TRÌNH DUYỆT WEB (WEB BROWSER)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    t4 = ("• Phần mềm giúp người dùng truy cập và xem trang web\n"
          "• Các trình duyệt phổ biến: Chrome, Edge, Firefox, Cốc Cốc, Safari\n"
          "• Cấu trúc cơ bản của trình duyệt:\n"
          "  + Thanh địa chỉ: Nhập tên miền website (URL)\n"
          "  + Nút điều hướng: Back (quay lại), Forward (tiếp tục), Reload\n"
          "  + Vùng hiển thị nội dung trang web")
    ax.text(66, 21, t4, ha='left', va='center', fontsize=8.8, color="#0F172A", linespacing=1.3)

    out_file = os.path.join(OUT_DIR, "mindmap_03_mang_thong_tin_toan_cau_tiet11_12.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f" -> Đã tạo Mindmap: {out_file}")

if __name__ == "__main__":
    draw_mindmap_tiet09()
    draw_mindmap_bai06()
    print(">>> HOÀN TẤT SINH 2 MINDMAP TIN HỌC 6 VECTOR 300 DPI! <<<")
