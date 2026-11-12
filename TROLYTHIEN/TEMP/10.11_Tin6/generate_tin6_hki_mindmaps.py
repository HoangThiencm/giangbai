# -*- coding: utf-8 -*-
"""
Script sinh Sơ đồ tư duy Mindmap vector 300 DPI cho môn Tin học 6 (Tuần 13 - 18):
1. Tiết 17: Ôn tập cuối học kì I (Tổng kết toàn bộ HKI - Chủ đề 1, 2, 3)
2. Bài 7 & Bài 8: Tìm kiếm thông tin & Thư điện tử
"""
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Tin6/mindmaps"
os.makedirs(OUT_DIR, exist_ok=True)

def draw_mindmap_on_tap_cuoi_hk1_tin6():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor("#F8FAFC")
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 96, "SƠ ĐỒ HỆ THỐNG HÓA KIẾN THỨC ÔN TẬP CUỐI HỌC KÌ I - TIN HỌC 6", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1E293B')
    ax.text(50, 92.5, "(Tổng kết Chủ đề 1, 2 và Chủ đề 3 - Bộ sách Kết nối tri thức với cuộc sống)", 
            ha='center', va='center', fontsize=11, fontstyle='italic', color='#475569')

    # Central Box
    center_box = patches.FancyBboxPatch((35, 43), 30, 14, boxstyle="round,pad=1.2,rounding_size=2", 
                                        ec="#1E40AF", fc="#DBEAFE", lw=2.5)
    ax.add_patch(center_box)
    ax.text(50, 52, "ÔN TẬP CUỐI HỌC KÌ I", ha='center', va='center', fontsize=13, fontweight='bold', color="#1E3A8A")
    ax.text(50, 48, "TIN HỌC 6 (KNTT)", ha='center', va='center', fontsize=11, fontweight='bold', color="#2563EB")
    ax.text(50, 45, "(Tuần 13 - Tuần 18)", ha='center', va='center', fontsize=9.5, fontstyle='italic', color="#1E40AF")

    # Nhánh 1: Chủ đề 1 - Máy tính & Cộng đồng (Top Left)
    ax.annotate('', xy=(24, 76), xytext=(38, 57), 
                arrowprops=dict(arrowstyle="-|>", color="#0284C7", lw=2, connectionstyle="arc3,rad=0.15"))
    b1 = patches.FancyBboxPatch((4, 70), 32, 17, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#0284C7", fc="#E0F2FE", lw=1.8)
    ax.add_patch(b1)
    ax.text(20, 83.5, "1. MÁY TÍNH VÀ CỘNG ĐỒNG", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#0369A1")
    t1 = ("• Thông tin, Dữ liệu, Vật mang tin\n"
          "• 4 bước xử lí thông tin: Thu nhận -> Lưu trữ -> Xử lí -> Truyền\n"
          "• Biểu diễn dữ liệu bằng dãy bit (0 và 1)\n"
          "• Đơn vị đo: Byte, KB, MB, GB, TB (1 Byte = 8 bit; 1 KB = 1024 B)")
    ax.text(6, 75.5, t1, ha='left', va='center', fontsize=8.8, color="#0F172A", linespacing=1.3)

    # Nhánh 2: Chủ đề 2 - Mạng máy tính & Internet (Bottom Left)
    ax.annotate('', xy=(24, 25), xytext=(38, 43), 
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2, connectionstyle="arc3,rad=-0.15"))
    b2 = patches.FancyBboxPatch((4, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#D97706", fc="#FEF3C7", lw=1.8)
    ax.add_patch(b2)
    ax.text(20, 29.5, "2. MẠNG MÁY TÍNH VÀ INTERNET", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#B45309")
    t2 = ("• Mạng máy tính: Thiết bị đầu cuối, thiết bị kết nối, phần mềm\n"
          "• Thiết bị mạng: Cáp mạng, Switch (chuyển mạch), Access Point\n"
          "• Phân loại: Mạng có dây và mạng không dây (Wi-Fi)\n"
          "• Internet: Mạng kết nối toàn cầu, kho tàng tri thức khổng lồ")
    ax.text(6, 21, t2, ha='left', va='center', fontsize=8.8, color="#0F172A", linespacing=1.3)

    # Nhánh 3: Bài 6 & 7 - WWW & Tìm kiếm thông tin (Top Right)
    ax.annotate('', xy=(76, 76), xytext=(62, 57), 
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=2, connectionstyle="arc3,rad=-0.15"))
    b3 = patches.FancyBboxPatch((64, 69), 32, 19, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#7C3AED", fc="#F3E8FF", lw=1.8)
    ax.add_patch(b3)
    ax.text(80, 84.5, "3. WWW & TÌM KIẾM THÔNG TIN", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#6D28D9")
    t3 = ("• World Wide Web: Mạng lưới website chứa siêu văn bản\n"
          "• Trình duyệt: Chrome, Edge, Cốc Cốc, Firefox...\n"
          "• Máy tìm kiếm (Search Engine): Google, Bing, Yahoo...\n"
          "• Từ khóa tìm kiếm: Ngắn gọn, chính xác, dùng ngoặc kép \"...\"\n"
          "• Đánh giá và chọn lọc thông tin đáng tin cậy")
    ax.text(66, 75.5, t3, ha='left', va='center', fontsize=8.8, color="#0F172A", linespacing=1.3)

    # Nhánh 4: Bài 8 - Thư điện tử (Email) (Bottom Right)
    ax.annotate('', xy=(76, 25), xytext=(62, 43), 
                arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2, connectionstyle="arc3,rad=0.15"))
    b4 = patches.FancyBboxPatch((64, 15), 32, 18, boxstyle="round,pad=0.8,rounding_size=1.5", 
                                ec="#059669", fc="#D1FAE5", lw=1.8)
    ax.add_patch(b4)
    ax.text(80, 29.5, "4. THƯ ĐIỆN TỬ (EMAIL)", ha='center', va='center', fontsize=10.5, fontweight='bold', color="#047857")
    t4 = ("• Khái niệm: Dịch vụ gửi/nhận thư điện tử qua Internet\n"
          "• Cấu trúc địa chỉ: <tên người dùng>@<tên máy chủ thư>\n"
          "• Ưu điểm: Nhanh chóng, chi phí thấp, đính kèm tệp tin đa dạng\n"
          "• Quy tắc an toàn: Bảo mật mật khẩu, không mở tệp lạ")
    ax.text(66, 21, t4, ha='left', va='center', fontsize=8.8, color="#0F172A", linespacing=1.3)

    out_file = os.path.join(OUT_DIR, "mindmap_03_on_tap_cuoi_hk1_tin6_tiet17.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f" -> Đã tạo Mindmap: {out_file}")

if __name__ == "__main__":
    draw_mindmap_on_tap_cuoi_hk1_tin6()
    print(">>> HOÀN TẤT SINH MINDMAP TIN HỌC 6 CUỐI HKI! <<<")
