# -*- coding: utf-8 -*-
"""
Script sinh 4 sơ đồ tư duy (Mindmap) chất lượng cao 300 DPI cho các tiết Ôn tập & Luyện tập Toán 9
Phù hợp chuẩn CV 5512 V2.1 • Trợ lý Sư phạm Hoàng Thiên
"""

import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\TEMP\02.11\mindmaps"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Thiết lập font Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11

def draw_rounded_box(ax, x, y, w, h, text, title="", bg_color="#EBF5FB", edge_color="#2980B9", title_color="#1B4F72", text_color="#1A252C"):
    """Vẽ một khối hộp bo tròn chứa tiêu đề và danh sách nội dung"""
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
                fontsize=12, fontweight='bold',
                color=title_color, zorder=4)
        ax.plot([x - w/2 + 0.08, x + w/2 - 0.08], [y + h/2 - 0.22, y + h/2 - 0.22],
                color=edge_color, linewidth=1, linestyle='-', zorder=4)
        ax.text(x, y - 0.08, text,
                ha='center', va='center',
                fontsize=10.5, color=text_color,
                linespacing=1.35, zorder=4)
    else:
        ax.text(x, y, text,
                ha='center', va='center',
                fontsize=13, fontweight='bold',
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

# 1. SƠ ĐỒ TƯ DUY 1: ÔN TẬP ĐẠI SỐ GIỮA HỌC KÌ I (TIẾT 25)
def create_mindmap_daiso_giuahk1():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.6, 1.2,
                     "ÔN TẬP ĐẠI SỐ 9\nGIỮA HỌC KÌ I",
                     bg_color="#D4EFDF", edge_color="#229954", title_color="#145A32")

    b1_text = "• PT quy về bậc nhất (tích, ẩn ở mẫu)\n• Hệ 2 PT bậc nhất 2 ẩn (Thế, Cộng)\n• Giải bài toán bằng cách lập hệ PT"
    draw_rounded_box(ax, 2.0, 4.6, 3.6, 1.7, b1_text,
                     title="1. PHƯƠNG TRÌNH & HỆ PT",
                     bg_color="#EBF5FB", edge_color="#3498DB", title_color="#1B4F72")
    draw_arrow(ax, (4.1, 3.5), (3.3, 4.0), color="#3498DB")

    b2_text = "• Liên hệ giữa thứ tự và phép cộng, nhân\n• BPT bậc nhất 1 ẩn (Đổi chiều khi chia số âm)\n• Biểu diễn tập nghiệm trên trục số"
    draw_rounded_box(ax, 2.0, 1.4, 3.6, 1.7, b2_text,
                     title="2. BẤT ĐẲNG THỨC & BPT",
                     bg_color="#FEF9E7", edge_color="#F39C12", title_color="#7D6608")
    draw_arrow(ax, (4.1, 2.5), (3.3, 2.0), color="#F39C12")

    b3_text = "• Căn bậc hai số học: a ≥ 0 thì √a ≥ 0\n• ĐKXĐ căn thức: √A có nghĩa khi A ≥ 0\n• Hằng đẳng thức: √(A²) = |A|\n• Phép nhân và chia căn bậc hai"
    draw_rounded_box(ax, 8.0, 3.0, 3.6, 2.1, b3_text,
                     title="3. CĂN BẬC HAI & CĂN THỨC",
                     bg_color="#FADBD8", edge_color="#E74C3C", title_color="#78281F")
    draw_arrow(ax, (6.3, 3.0), (6.7, 3.0), color="#E74C3C")

    out_path = os.path.join(OUTPUT_DIR, "mindmap_03_on_tap_dai_so_giua_hk1.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(" -> Tạo thành công:", os.path.basename(out_path))

# 2. SƠ ĐỒ TƯ DUY 2: ÔN TẬP HÌNH HỌC GIỮA HỌC KÌ I (TIẾT 13)
def create_mindmap_hinhhoc_giuahk1():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.6, 1.2,
                     "ÔN TẬP HÌNH HỌC 9\nGIỮA HỌC KÌ I",
                     bg_color="#FCF3CF", edge_color="#F1C40F", title_color="#7D6608")

    b1_text = "• Tỉ số lượng giác: sin, cos, tan, cot\n• Hệ thức cạnh & góc: b = a·sin B = c·tan B\n• Ứng dụng thực tế: Đo chiều cao, khoảng cách"
    draw_rounded_box(ax, 2.1, 4.6, 3.8, 1.7, b1_text,
                     title="1. HỆ THỨC LƯỢNG TRONG Δ VUÔNG",
                     bg_color="#E8F8F5", edge_color="#1ABC9C", title_color="#0E6251")
    draw_arrow(ax, (4.1, 3.5), (3.3, 4.1), color="#1ABC9C")

    b2_text = "• Định nghĩa đường tròn (O; R)\n• Tính chất đối xứng: Tâm O, vô số trục đối xứng\n• Vị trí điểm & đường tròn: OM < R, OM = R, OM > R"
    draw_rounded_box(ax, 2.1, 1.4, 3.8, 1.7, b2_text,
                     title="2. ĐƯỜNG TRÒN (CHƯƠNG V)",
                     bg_color="#EBF5FB", edge_color="#2980B9", title_color="#1B4F72")
    draw_arrow(ax, (4.1, 2.5), (3.3, 1.9), color="#2980B9")

    b3_text = "• Góc ở tâm & Số đo cung: sđ AB = góc AOB\n• Cung bằng nhau căng hai dây bằng nhau\n• Dây lớn hơn căng cung lớn hơn\n• Đường kính vuông góc dây đi qua trung điểm dây"
    draw_rounded_box(ax, 7.9, 3.0, 3.8, 2.2, b3_text,
                     title="3. CUNG VÀ DÂY CỦA ĐƯỜNG TRÒN",
                     bg_color="#F4ECF7", edge_color="#8E44AD", title_color="#4A235A")
    draw_arrow(ax, (6.3, 3.0), (6.6, 3.0), color="#8E44AD")

    out_path = os.path.join(OUTPUT_DIR, "mindmap_04_on_tap_hinh_hoc_giua_hk1.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(" -> Tạo thành công:", os.path.basename(out_path))

# 3. SƠ ĐỒ TƯ DUY 3: CĂN BẬC HAI & BIẾN ĐỔI CĂN THỨC (TIẾT 29)
def create_mindmap_daiso_tiet29():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.7, 1.3,
                     "CĂN BẬC HAI &\nCĂN THỨC BẬC HAI",
                     bg_color="#EAECEE", edge_color="#5D6D7E", title_color="#212F3D")

    b1_text = "• Điều kiện xác định: √A có nghĩa khi A ≥ 0\n• Hằng đẳng thức: √(A²) = |A|\n• Phá dấu |A|: A nếu A ≥ 0; -A nếu A < 0"
    draw_rounded_box(ax, 2.1, 4.6, 3.8, 1.7, b1_text,
                     title="1. ĐIỀU KIỆN & HẰNG ĐẲNG THỨC",
                     bg_color="#EAFAF1", edge_color="#2ECC71", title_color="#145A32")
    draw_arrow(ax, (4.1, 3.5), (3.4, 4.1), color="#2ECC71")

    b2_text = "• Khai phương tích: √(a·b) = √a·√b (a, b ≥ 0)\n• Khai phương thương: √(a/b) = √a/√b (a ≥ 0, b > 0)\n• Đưa thừa số ra ngoài/vào trong dấu căn"
    draw_rounded_box(ax, 2.1, 1.4, 3.8, 1.7, b2_text,
                     title="2. NHÂN & CHIA CĂN BẬC HAI",
                     bg_color="#FEF5E7", edge_color="#E67E22", title_color="#6E2C00")
    draw_arrow(ax, (4.1, 2.5), (3.4, 1.9), color="#E67E22")

    b3_text = "• Cộng trừ các căn thức đồng dạng\n• Trục căn thức ở mẫu (nhân lượng liên hợp)\n• Rút gọn biểu thức chứa biến tổng hợp\n• Vận dụng: Tầm nhìn chân trời d ≈ 3,57√h"
    draw_rounded_box(ax, 7.9, 3.0, 3.8, 2.2, b3_text,
                     title="3. RÚT GỌN & VẬN DỤNG THỰC TẾ",
                     bg_color="#EBF5FB", edge_color="#2980B9", title_color="#1B4F72")
    draw_arrow(ax, (6.35, 3.0), (6.65, 3.0), color="#2980B9")

    out_path = os.path.join(OUTPUT_DIR, "mindmap_07_luyen_tap_chung_dai_so_tiet29.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(" -> Tạo thành công:", os.path.basename(out_path))

# 4. SƠ ĐỒ TƯ DUY 4: CHƯƠNG V ĐƯỜNG TRÒN (TIẾT 17 - NLS 3.1.TC2a)
def create_mindmap_hinhhoc_tiet17():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    draw_rounded_box(ax, 5.0, 3.0, 2.6, 1.3,
                     "CHƯƠNG V:\nĐƯỜNG TRÒN (9)",
                     bg_color="#FDEDEC", edge_color="#E74C3C", title_color="#78281F")

    b1_text = "• Góc ở tâm: Đỉnh tại O; sđ AB = góc AOB\n• Hai cung bằng nhau căng hai dây bằng nhau\n• Đường kính vuông góc với dây đi qua\ntrung điểm dây và điểm chính giữa của cung"
    draw_rounded_box(ax, 2.1, 4.6, 3.8, 1.8, b1_text,
                     title="1. GÓC Ở TÂM - CUNG VÀ DÂY",
                     bg_color="#EBF5FB", edge_color="#3498DB", title_color="#1B4F72")
    draw_arrow(ax, (4.1, 3.5), (3.4, 4.1), color="#3498DB")

    b2_text = "• Chế tạo quạt giấy xòe truyền thống (STEM)\n• Tính chi phí trải đường chạy sân vận động\n• Xác định tầm với quét vật liệu của cần cẩu"
    draw_rounded_box(ax, 2.1, 1.4, 3.8, 1.7, b2_text,
                     title="2. ỨNG DỤNG THỰC TẾ & STEM",
                     bg_color="#FEF9E7", edge_color="#F39C12", title_color="#7D6608")
    draw_arrow(ax, (4.1, 2.5), (3.4, 1.9), color="#F39C12")

    b3_text = "• Chu vi đường tròn: C = 2πR = πd\n• Độ dài cung n°: l = (π·R·n) / 180\n• Diện tích hình tròn: S = π·R²\n• Diện tích hình quạt tròn: Sq = (π·R²·n)/360 = (l·R)/2\n• Diện tích hình vành khuyên: Svk = π(R₁² - R₂²)"
    draw_rounded_box(ax, 7.9, 3.0, 3.9, 2.4, b3_text,
                     title="3. BỘ CÔNG THỨC CHƯƠNG V",
                     bg_color="#E8F8F5", edge_color="#16A085", title_color="#0E6251")
    draw_arrow(ax, (6.3, 3.0), (6.6, 3.0), color="#16A085")

    out_path = os.path.join(OUTPUT_DIR, "mindmap_09_luyen_tap_chung_hinh_hoc_tiet17.png")
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(" -> Tạo thành công:", os.path.basename(out_path))

create_mindmap_daiso_giuahk1()
create_mindmap_hinhhoc_giuahk1()
create_mindmap_daiso_tiet29()
create_mindmap_hinhhoc_tiet17()
print(">>> TẤT CẢ 4 ẢNH SƠ ĐỒ TƯ DUY ĐÃ ĐƯỢC TẠO HOÀN HẢO! <<<")
