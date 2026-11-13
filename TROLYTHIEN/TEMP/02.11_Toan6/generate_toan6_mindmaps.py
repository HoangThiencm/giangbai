# -*- coding: utf-8 -*-
"""
Script sinh hệ thống Sơ đồ tư duy (Mindmap) chất lượng cao 300 DPI cho môn Toán 6 (Tuần 9 - 12)
Phù hợp chuẩn CV 5512 V2.1 • Trợ lý Sư phạm Hoàng Thiên
"""

import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\TEMP\02.11_Toan6\mindmaps"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11

def draw_rounded_box(ax, x, y, w, h, text, title="", bg_color="#EBF5FB", edge_color="#2980B9", title_color="#1B4F72", text_color="#1A252C"):
    box = patches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.06",
        facecolor=bg_color,
        edgecolor=edge_color,
        linewidth=2,
        zorder=3
    )
    ax.add_patch(box)
    
    if title:
        ax.text(x, y + h/2 - 0.12, title,
                ha='center', va='center',
                fontsize=11.5, fontweight='bold',
                color=title_color, zorder=4)
        ax.plot([x - w/2 + 0.08, x + w/2 - 0.08], [y + h/2 - 0.22, y + h/2 - 0.22],
                color=edge_color, linewidth=1, linestyle='-', zorder=4)
        ax.text(x, y - 0.08, text,
                ha='center', va='center',
                fontsize=10, color=text_color,
                linespacing=1.35, zorder=4)
    else:
        ax.text(x, y, text,
                ha='center', va='center',
                fontsize=12.5, fontweight='bold',
                color=title_color, linespacing=1.3, zorder=4)

def draw_arrow(ax, start_pt, end_pt, color="#5D6D7E"):
    ax.annotate(
        "",
        xy=end_pt, xycoords='data',
        xytext=start_pt, textcoords='data',
        arrowprops=dict(
            arrowstyle="->,head_width=0.3,head_length=0.4",
            color=color,
            lw=2,
            connectionstyle="arc3,rad=0.08"
        ),
        zorder=2
    )

# 1. MINDMAP TIẾT 25: LUYỆN TẬP CHUNG CHƯƠNG II (ƯCLN & BCNN)
def create_mindmap_tiet25():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.6, 1.2,
                     "ƯCLN & BCNN\nỨNG DỤNG TOÁN 6",
                     bg_color="#D4EFDF", edge_color="#27AE60", title_color="#145A32")

    b1 = "• Tìm ƯCLN qua phân tích thừa số nguyên tố\n• Chọn thừa số chung với số mũ nhỏ nhất\n• Ứng dụng: Rút gọn phân số về tối giản"
    draw_rounded_box(ax, 2.0, 4.6, 3.6, 1.7, b1,
                     title="1. ƯỚC CHUNG LỚN NHẤT (ƯCLN)",
                     bg_color="#EBF5FB", edge_color="#3498DB", title_color="#1B4F72")
    draw_arrow(ax, (4.1, 3.5), (3.3, 4.0), color="#3498DB")

    b2 = "• Tìm BCNN qua phân tích thừa số nguyên tố\n• Chọn thừa số chung và riêng với số mũ lớn nhất\n• Ứng dụng: Quy đồng mẫu các phân số"
    draw_rounded_box(ax, 2.0, 1.4, 3.6, 1.7, b2,
                     title="2. BỘI CHUNG NHỎ NHẤT (BCNN)",
                     bg_color="#FEF9E7", edge_color="#F39C12", title_color="#7D6608")
    draw_arrow(ax, (4.1, 2.5), (3.3, 2.0), color="#F39C12")

    b3 = "• Chia tổ học tập, chia quà đều nhau (ƯCLN)\n• Bài toán chu kỳ lặp lại, cùng khởi hành (BCNN)\n• Lịch trực nhật cùng ngày, đèn nhấp nháy"
    draw_rounded_box(ax, 8.0, 3.0, 3.6, 2.1, b3,
                     title="3. BÀI TOÁN THỰC TẾ ĐỜI SỐNG",
                     bg_color="#FADBD8", edge_color="#E74C3C", title_color="#78281F")
    draw_arrow(ax, (6.3, 3.0), (6.7, 3.0), color="#E74C3C")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mindmap_01_luyen_tap_chung_chuong2_tiet25.png"), bbox_inches='tight', pad_inches=0.1)
    plt.close()

# 2. MINDMAP TIẾT 26: BÀI TẬP CUỐI CHƯƠNG II
def create_mindmap_tiet26():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.7, 1.3,
                     "TỔNG KẾT CHƯƠNG II\nTÍNH CHẤT CHIA HẾT",
                     bg_color="#FCF3CF", edge_color="#F1C40F", title_color="#7D6608")

    b1 = "• Quan hệ chia hết: a chia hết cho b (b ≠ 0)\n• Tính chất chia hết của một tổng/hiệu\n• Dấu hiệu chia hết cho 2, 3, 5, 9"
    draw_rounded_box(ax, 2.1, 4.6, 3.8, 1.7, b1,
                     title="1. QUAN HỆ & DẤU HIỆU CHIA HẾT",
                     bg_color="#E8F8F5", edge_color="#1ABC9C", title_color="#0E6251")
    draw_arrow(ax, (4.1, 3.5), (3.3, 4.1), color="#1ABC9C")

    b2 = "• Số nguyên tố: Chỉ có 2 ước là 1 và chính nó\n• Hợp số: Có nhiều hơn 2 ước\n• Phân tích số tự nhiên ra thừa số nguyên tố"
    draw_rounded_box(ax, 2.1, 1.4, 3.8, 1.7, b2,
                     title="2. SỐ NGUYÊN TỐ & HỢP SỐ",
                     bg_color="#EBF5FB", edge_color="#2980B9", title_color="#1B4F72")
    draw_arrow(ax, (4.1, 2.5), (3.3, 1.9), color="#2980B9")

    b3 = "• Tập hợp ƯC và BC của hai hay nhiều số\n• Cách tìm ƯCLN và BCNN bằng thuật toán chuẩn\n• Hai số nguyên tố cùng nhau có ƯCLN = 1"
    draw_rounded_box(ax, 7.9, 3.0, 3.8, 2.2, b3,
                     title="3. ƯỚC CHUNG & BỘI CHUNG",
                     bg_color="#F4ECF7", edge_color="#8E44AD", title_color="#4A235A")
    draw_arrow(ax, (6.35, 3.0), (6.65, 3.0), color="#8E44AD")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mindmap_02_bai_tap_cuoi_chuong2_tiet26.png"), bbox_inches='tight', pad_inches=0.1)
    plt.close()

# 3. MINDMAP TIẾT 27-28: ÔN TẬP GIỮA HỌC KÌ I (SỐ HỌC 6)
def create_mindmap_tiet27_28():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.7, 1.3,
                     "ÔN TẬP SỐ HỌC 6\nGIỮA HỌC KÌ I",
                     bg_color="#EAECEE", edge_color="#5D6D7E", title_color="#212F3D")

    b1 = "• Tập hợp N và N*, cách ghi số tự nhiên\n• Phép tính: +, -, ×, ÷ và Lũy thừa số mũ tự nhiên\n• Thứ tự thực hiện: Ngoặc tròn -> vuông -> nhọn"
    draw_rounded_box(ax, 2.1, 4.6, 3.8, 1.8, b1,
                     title="CHƯƠNG I: SỐ TỰ NHIÊN",
                     bg_color="#EAFAF1", edge_color="#2ECC71", title_color="#145A32")
    draw_arrow(ax, (4.1, 3.5), (3.4, 4.1), color="#2ECC71")

    b2 = "• Tính chất chia hết của một tổng\n• Dấu hiệu chia hết cho 2, 5 (chữ số tận cùng)\n• Dấu hiệu chia hết cho 3, 9 (tổng các chữ số)"
    draw_rounded_box(ax, 2.1, 1.4, 3.8, 1.7, b2,
                     title="CHƯƠNG II: CHIA HẾT & DẤU HIỆU",
                     bg_color="#FEF5E7", edge_color="#E67E22", title_color="#6E2C00")
    draw_arrow(ax, (4.1, 2.5), (3.4, 1.9), color="#E67E22")

    b3 = "• Số nguyên tố, hợp số, bảng số nguyên tố\n• Phân tích ra thừa số nguyên tố\n• Quy tắc tìm ƯCLN và BCNN\n• Rút gọn phân số & quy đồng mẫu"
    draw_rounded_box(ax, 7.9, 3.0, 3.8, 2.2, b3,
                     title="CHƯƠNG II: ƯCLN & BCNN",
                     bg_color="#EBF5FB", edge_color="#2980B9", title_color="#1B4F72")
    draw_arrow(ax, (6.35, 3.0), (6.65, 3.0), color="#2980B9")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mindmap_03_on_tap_giua_hk1_sohoc_tiet27_28.png"), bbox_inches='tight', pad_inches=0.1)
    plt.close()

# 4. MINDMAP TIẾT 09: ÔN TẬP GIỮA HỌC KÌ I (HÌNH HỌC TRỰC QUAN 6)
def create_mindmap_tiet09():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.7, 1.3,
                     "HÌNH HỌC TRỰC QUAN 6\nGIỮA HỌC KÌ I",
                     bg_color="#FDEDEC", edge_color="#E74C3C", title_color="#78281F")

    b1 = "• Tam giác đều: 3 cạnh bằng nhau, 3 góc bằng nhau\n• Hình vuông: 4 cạnh bằng nhau, 4 góc vuông\n• Lục giác đều: 6 cạnh bằng nhau, 6 đỉnh"
    draw_rounded_box(ax, 2.1, 4.6, 3.8, 1.8, b1,
                     title="1. TAM GIÁC ĐỀU, VUÔNG, LỤC GIÁC",
                     bg_color="#EBF5FB", edge_color="#3498DB", title_color="#1B4F72")
    draw_arrow(ax, (4.1, 3.5), (3.4, 4.1), color="#3498DB")

    b2 = "• Hình chữ nhật: 4 góc vuông, 2 đường chéo bằng\n• Hình thoi: 4 cạnh bằng nhau, 2 đường chéo vuông góc\n• Hình bình hành: Cặp cạnh đối // và bằng nhau\n• Hình thang cân: 2 cạnh bên bằng, 2 góc đáy bằng"
    draw_rounded_box(ax, 2.1, 1.4, 3.8, 1.9, b2,
                     title="2. CÁC TỨ GIÁC ĐẶC BIỆT",
                     bg_color="#FEF9E7", edge_color="#F39C12", title_color="#7D6608")
    draw_arrow(ax, (4.1, 2.5), (3.4, 1.9), color="#F39C12")

    b3 = "• Chu vi hình chữ nhật: C = 2(a + b)\n• Diện tích hình chữ nhật: S = a·b\n• Diện tích hình vuông: S = a²\n• Diện tích hình thoi: S = 1/2·m·n\n• Diện tích hình bình hành: S = a·h\n• Diện tích hình thang: S = 1/2(a + b)·h"
    draw_rounded_box(ax, 7.9, 3.0, 3.9, 2.5, b3,
                     title="3. BỘ CÔNG THỨC CHU VI & DIỆN TÍCH",
                     bg_color="#E8F8F5", edge_color="#16A085", title_color="#0E6251")
    draw_arrow(ax, (6.35, 3.0), (6.65, 3.0), color="#16A085")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mindmap_07_on_tap_giua_hk1_hinhhoc_tiet09.png"), bbox_inches='tight', pad_inches=0.1)
    plt.close()

# 5. MINDMAP TIẾT 11: LUYỆN TẬP CHUNG HÌNH HỌC (TRANG 94 - 95)
def create_mindmap_tiet11():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.7, 1.3,
                     "CHU VI & DIỆN TÍCH\nTRONG THỰC TIỄN",
                     bg_color="#E8F8F5", edge_color="#16A085", title_color="#0E6251")

    b1 = "• Công thức chu vi các hình: C = tổng các cạnh ngoài\n• Diện tích hình chữ nhật: S = a·b\n• Diện tích tam giác: S = 1/2·a·h\n• Diện tích hình thoi: S = 1/2·d₁·d₂"
    draw_rounded_box(ax, 2.1, 4.6, 3.8, 1.8, b1,
                     title="1. CÔNG THỨC NỀN TẢNG",
                     bg_color="#EBF5FB", edge_color="#3498DB", title_color="#1B4F72")
    draw_arrow(ax, (4.1, 3.5), (3.4, 4.1), color="#3498DB")

    b2 = "• Tính diện tích hình ghép: Chia nhỏ thành các hình đã biết\n• Tính diện tích phần còn lại: S = S_tổng - S_trống\n• Đổi đơn vị đo: m², cm², dm², ha chuẩn xác"
    draw_rounded_box(ax, 2.1, 1.4, 3.8, 1.8, b2,
                     title="2. PHƯƠNG PHÁP CHIA & GHÉP HÌNH",
                     bg_color="#FEF9E7", edge_color="#F39C12", title_color="#7D6608")
    draw_arrow(ax, (4.1, 2.5), (3.4, 1.9), color="#F39C12")

    b3 = "• Tính số viên gạch cần dùng lát nền nhà\n• Tính chi phí làm hàng rào quanh khu vườn\n• Tính sản lượng lúa, lượng phân bón trên thửa ruộng\n• Thiết kế khuôn viên sân trường, bồn hoa"
    draw_rounded_box(ax, 7.9, 3.0, 3.9, 2.3, b3,
                     title="3. BÀI TOÁN KINH TẾ & THỰC TẾ",
                     bg_color="#FADBD8", edge_color="#E74C3C", title_color="#78281F")
    draw_arrow(ax, (6.35, 3.0), (6.65, 3.0), color="#E74C3C")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mindmap_08_luyen_tap_chung_hinhhoc_tiet11.png"), bbox_inches='tight', pad_inches=0.1)
    plt.close()

# 6. MINDMAP TIẾT 12: BÀI TẬP CUỐI CHƯƠNG IV HÌNH HỌC
def create_mindmap_tiet12():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.7, 1.3,
                     "TỔNG KẾT CHƯƠNG IV\nHÌNH PHẲNG THỰC TIỄN",
                     bg_color="#F4ECF7", edge_color="#8E44AD", title_color="#4A235A")

    b1 = "• Tam giác đều: 3 cạnh =, 3 góc 60°\n• Hình vuông: 4 cạnh =, 4 góc vuông\n• Lục giác đều: 6 tam giác đều ghép lại"
    draw_rounded_box(ax, 2.1, 4.6, 3.8, 1.7, b1,
                     title="1. HÌNH ĐỀU",
                     bg_color="#E8F8F5", edge_color="#1ABC9C", title_color="#0E6251")
    draw_arrow(ax, (4.1, 3.5), (3.4, 4.1), color="#1ABC9C")

    b2 = "• Hình chữ nhật, hình thoi, hình bình hành, hình thang cân\n• Dấu hiệu nhận biết qua cạnh, góc và đường chéo\n• Vẽ hình bằng thước thẳng, compa, êke"
    draw_rounded_box(ax, 2.1, 1.4, 3.8, 1.8, b2,
                     title="2. CÁC TỨ GIÁC ĐÃ HỌC",
                     bg_color="#FEF5E7", edge_color="#E67E22", title_color="#6E2C00")
    draw_arrow(ax, (4.1, 2.5), (3.4, 1.9), color="#E67E22")

    b3 = "• Bảng tổng hợp công thức chu vi và diện tích 6 hình\n• Kỹ năng giải bài tập trắc nghiệm và tự luận\n• Gấp giấy, cắt dán trang trí mô hình hình học"
    draw_rounded_box(ax, 7.9, 3.0, 3.8, 2.2, b3,
                     title="3. CÔNG THỨC & THỰC HÀNH",
                     bg_color="#EBF5FB", edge_color="#2980B9", title_color="#1B4F72")
    draw_arrow(ax, (6.35, 3.0), (6.65, 3.0), color="#2980B9")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "mindmap_09_bai_tap_cuoi_chuong4_tiet12.png"), bbox_inches='tight', pad_inches=0.1)
    plt.close()

create_mindmap_tiet25()
create_mindmap_tiet26()
create_mindmap_tiet27_28()
create_mindmap_tiet09()
create_mindmap_tiet11()
create_mindmap_tiet12()
print(">>> TẤT CẢ 6 ẢNH SƠ ĐỒ TƯ DUY TOÁN 6 ĐÃ ĐƯỢC TẠO THÀNH CÔNG! <<<")
