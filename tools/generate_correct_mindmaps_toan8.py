# -*- coding: utf-8 -*-
"""
Script vẽ lại 2 sơ đồ tư duy chuẩn 100% chương trình Toán 8 KNTT:
1. mindmap_toan8_chuong1_ontap.png: Chỉ gói gọn trong Chương I (Đa thức), KHÔNG có hằng đẳng thức hay phân tích nhân tử.
2. mindmap_toan8_chuong3_ontap.png: Chỉ gói gọn trong Chương III (Tứ giác), KHÔNG có đường trung bình tam giác hay Pythagore.
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../TROLYTHIEN/engine/hinh_ve_sgk'))
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Times New Roman']

def draw_mindmap_chuong1_ontap():
    fig, ax = plt.subplots(figsize=(11.5, 6.0), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Tiêu đề lớn
    ax.text(50, 95, 'SƠ ĐỒ TƯ DUY: ÔN TẬP GIỮA HỌC KÌ I - ĐẠI SỐ 8',
            fontsize=15, ha='center', va='center', fontweight='bold', color='#1E3A8A')

    # Hộp trung tâm
    c_box = FancyBboxPatch((30, 80), 40, 10, boxstyle='round,pad=1,rounding_size=2',
                           facecolor='#DBEAFE', edgecolor='#2563EB', lw=2)
    ax.add_patch(c_box)
    ax.text(50, 86, 'TRỌNG TÂM ĐẠI SỐ GIỮA HK I',
            fontsize=12.5, ha='center', va='center', fontweight='bold', color='#1E3A8A')
    ax.text(50, 82.5, 'Hệ thống hóa toàn diện kiến thức Chương I: Đa thức',
            fontsize=9.5, ha='center', va='center', fontstyle='italic', color='#1E40AF')

    # Đường nối từ hộp trung tâm tới 3 nhánh
    ax.plot([50, 18], [80, 72], color='#2563EB', lw=1.6)
    ax.plot([50, 50], [80, 72], color='#059669', lw=1.6)
    ax.plot([50, 82], [80, 72], color='#7C3AED', lw=1.6)

    # ==================== CỘT 1: ĐƠN THỨC & ĐA THỨC ====================
    b1 = FancyBboxPatch((3, 5), 30, 67, boxstyle='round,pad=1,rounding_size=2',
                        facecolor='#F8FAFC', edgecolor='#3B82F6', lw=1.8)
    ax.add_patch(b1)
    # Header cột 1
    h1 = FancyBboxPatch((3, 64), 30, 8, boxstyle='round,pad=0.5,rounding_size=1.5',
                        facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.2)
    ax.add_patch(h1)
    ax.text(18, 68, '1. ĐƠN THỨC & ĐA THỨC',
            fontsize=10.5, ha='center', va='center', fontweight='bold', color='#1D4ED8')

    lines1 = [
        ('• Đơn thức nhiều biến:', True, '#0F172A', 9.2),
        ('  - Gồm số và biến liên kết bằng tích', False, '#334155', 8.2),
        ('  - Bậc: tổng số mũ các biến trong đơn thức', True, '#047857', 8.2),
        ('', False, '#334155', 4),
        ('• Đơn thức đồng dạng:', True, '#0F172A', 9.2),
        ('  - Cùng phần biến, hệ số khác 0', False, '#334155', 8.2),
        ('  - Cộng trừ: cộng trừ hệ số, giữ nguyên biến', True, '#047857', 8.2),
        ('', False, '#334155', 4),
        ('• Đa thức nhiều biến:', True, '#0F172A', 9.2),
        ('  - Tổng của những đơn thức', False, '#334155', 8.2),
        ('  - Thu gọn: cộng các hạng tử đồng dạng', False, '#334155', 8.2),
        ('  - Bậc đa thức: bậc của hạng tử có', True, '#047857', 8.2),
        ('    bậc cao nhất sau khi đã thu gọn', True, '#047857', 8.2),
        ('', False, '#334155', 4),
        ('• Giá trị của đa thức:', True, '#0F172A', 9.2),
        ('  - Thay giá trị của biến vào đa thức thu gọn', False, '#334155', 8.2)
    ]
    y_text = 60.5
    for txt, is_b, col, fs in lines1:
        if txt:
            ax.text(5.5, y_text, txt, fontsize=fs, ha='left', va='center',
                    fontweight='bold' if is_b else 'normal', color=col)
        y_text -= 3.3

    # ==================== CỘT 2: CÁC PHÉP TOÁN ĐẠI SỐ ====================
    b2 = FancyBboxPatch((35, 5), 30, 67, boxstyle='round,pad=1,rounding_size=2',
                        facecolor='#F8FAFC', edgecolor='#059669', lw=1.8)
    ax.add_patch(b2)
    # Header cột 2
    h2 = FancyBboxPatch((35, 64), 30, 8, boxstyle='round,pad=0.5,rounding_size=1.5',
                        facecolor='#ECFDF5', edgecolor='#059669', lw=1.2)
    ax.add_patch(h2)
    ax.text(50, 68, '2. CÁC PHÉP TOÁN ĐẠI SỐ',
            fontsize=10.5, ha='center', va='center', fontweight='bold', color='#047857')

    lines2 = [
        ('• Phép cộng và trừ đa thức:', True, '#0F172A', 9.2),
        ('  - Bỏ dấu ngoặc đúng quy tắc:', False, '#334155', 8.2),
        ('    -(A + B - C) = -A - B + C', True, '#DC2626', 8.5),
        ('  - Nhóm các hạng tử đồng dạng rồi cộng trừ', False, '#334155', 8.2),
        ('', False, '#334155', 4),
        ('• Phép nhân đa thức:', True, '#0F172A', 9.2),
        ('  - Đơn thức · Đa thức: A(B + C) = AB + AC', True, '#047857', 8.2),
        ('  - Đa thức · Đa thức:', False, '#334155', 8.2),
        ('    (A + B)(C + D) = AC + AD + BC + BD', True, '#047857', 8.2),
        ('', False, '#334155', 4),
        ('• Phép chia hết:', True, '#0F172A', 9.2),
        ('  - Đơn thức : Đơn thức (chia hệ số, trừ số mũ)', False, '#334155', 8.2),
        ('    x^m : x^n = x^(m-n)  (m >= n)', True, '#047857', 8.2),
        ('  - Đa thức : Đơn thức: chia từng hạng tử', True, '#047857', 8.2),
        ('    của đa thức cho đơn thức rồi cộng lại', False, '#334155', 8.2)
    ]
    y_text = 60.5
    for txt, is_b, col, fs in lines2:
        if txt:
            ax.text(37.5, y_text, txt, fontsize=fs, ha='left', va='center',
                    fontweight='bold' if is_b else 'normal', color=col)
        y_text -= 3.3

    # ==================== CỘT 3: CÁC DẠNG BÀI TẬP TRỌNG TÂM ====================
    b3 = FancyBboxPatch((67, 5), 30, 67, boxstyle='round,pad=1,rounding_size=2',
                        facecolor='#F8FAFC', edgecolor='#7C3AED', lw=1.8)
    ax.add_patch(b3)
    # Header cột 3
    h3 = FancyBboxPatch((67, 64), 30, 8, boxstyle='round,pad=0.5,rounding_size=1.5',
                        facecolor='#F5F3FF', edgecolor='#7C3AED', lw=1.2)
    ax.add_patch(h3)
    ax.text(82, 68, '3. BÀI TẬP TRỌNG TÂM GIỮA KÌ',
            fontsize=10.5, ha='center', va='center', fontweight='bold', color='#6D28D9')

    lines3 = [
        ('• Dạng 1: Thu gọn & Tính giá trị:', True, '#0F172A', 9.2),
        ('  - Rút gọn biểu thức trước khi thay số', False, '#334155', 8.2),
        ('  - Tránh thay số trực tiếp gây phức tạp', True, '#DC2626', 8.2),
        ('', False, '#334155', 4),
        ('• Dạng 2: Thực hiện phép tính:', True, '#0F172A', 9.2),
        ('  - Phối hợp phép nhân và cộng/trừ đa thức', False, '#334155', 8.2),
        ('  - Chia đa thức cho đơn thức nhiều biến', False, '#334155', 8.2),
        ('', False, '#334155', 4),
        ('• Dạng 3: Tìm x (Rút gọn rồi giải):', True, '#0F172A', 9.2),
        ('  - Khai triển tích, triệt tiêu số hạng x^2', True, '#6D28D9', 8.2),
        ('  - Đưa về dạng ax = b để tìm x', False, '#334155', 8.2),
        ('', False, '#334155', 4),
        ('• Dạng 4: Ứng dụng thực tế & Chia hết:', True, '#0F172A', 9.2),
        ('  - Tính diện tích, thể tích khối hộp chữ nhật', True, '#047857', 8.2),
        ('  - Tìm số tự nhiên n để phép chia là chia hết', True, '#047857', 8.2)
    ]
    y_text = 60.5
    for txt, is_b, col, fs in lines3:
        if txt:
            ax.text(69.5, y_text, txt, fontsize=fs, ha='left', va='center',
                    fontweight='bold' if is_b else 'normal', color=col)
        y_text -= 3.3

    out_file = os.path.join(OUT_DIR, 'mindmap_toan8_chuong1_ontap.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Đã vẽ thành công: {out_file}')


def draw_mindmap_chuong3_ontap():
    fig, ax = plt.subplots(figsize=(11.5, 6.0), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Tiêu đề lớn
    ax.text(50, 95, 'SƠ ĐỒ TƯ DUY: ÔN TẬP GIỮA HỌC KÌ I - HÌNH HỌC 8',
            fontsize=15, ha='center', va='center', fontweight='bold', color='#1E3A8A')

    # Hộp trung tâm
    c_box = FancyBboxPatch((28, 80), 44, 10, boxstyle='round,pad=1,rounding_size=2',
                           facecolor='#DBEAFE', edgecolor='#2563EB', lw=2)
    ax.add_patch(c_box)
    ax.text(50, 86, 'TRỌNG TÂM HÌNH HỌC GIỮA HK I',
            fontsize=12.5, ha='center', va='center', fontweight='bold', color='#1E3A8A')
    ax.text(50, 82.5, 'Hệ thống hóa toàn diện kiến thức Chương III: Tứ giác',
            fontsize=9.5, ha='center', va='center', fontstyle='italic', color='#1E40AF')

    # Đường nối
    ax.plot([50, 18], [80, 72], color='#D97706', lw=1.6)
    ax.plot([50, 50], [80, 72], color='#2563EB', lw=1.6)
    ax.plot([50, 82], [80, 72], color='#DC2626', lw=1.6)

    # ==================== CỘT 1: TỨ GIÁC & HÌNH THANG CÂN ====================
    b1 = FancyBboxPatch((3, 5), 30, 67, boxstyle='round,pad=1,rounding_size=2',
                        facecolor='#F8FAFC', edgecolor='#D97706', lw=1.8)
    ax.add_patch(b1)
    h1 = FancyBboxPatch((3, 64), 30, 8, boxstyle='round,pad=0.5,rounding_size=1.5',
                        facecolor='#FEF3C7', edgecolor='#D97706', lw=1.2)
    ax.add_patch(h1)
    ax.text(18, 68, '1. TỨ GIÁC & HÌNH THANG CÂN',
            fontsize=10.0, ha='center', va='center', fontweight='bold', color='#B45309')

    lines1 = [
        ('• Định lý Tứ giác:', True, '#0F172A', 9.2),
        ('  - Tổng 4 góc của một tứ giác luôn bằng 360°', True, '#B45309', 8.2),
        ('  - Áp dụng tính góc còn lại khi biết 3 góc', False, '#334155', 8.2),
        ('', False, '#334155', 4),
        ('• Hình thang:', True, '#0F172A', 9.2),
        ('  - Tứ giác có 2 cạnh đối song song', False, '#334155', 8.2),
        ('  - Hai góc kề một cạnh bên bù nhau (180°)', False, '#334155', 8.2),
        ('', False, '#334155', 4),
        ('• Hình thang cân (Dấu hiệu nhận biết):', True, '#0F172A', 9.2),
        ('  - Hình thang có 2 góc kề một đáy bằng nhau', True, '#047857', 8.2),
        ('  - Hình thang có 2 đường chéo bằng nhau', True, '#047857', 8.2),
        ('  - Tính chất: Hai cạnh bên bằng nhau;', False, '#334155', 8.2),
        ('    hai đường chéo bằng nhau', False, '#334155', 8.2),
        ('  - Trục đối xứng: đường trung trực 2 đáy', False, '#334155', 8.2)
    ]
    y_text = 60.5
    for txt, is_b, col, fs in lines1:
        if txt:
            ax.text(5.5, y_text, txt, fontsize=fs, ha='left', va='center',
                    fontweight='bold' if is_b else 'normal', color=col)
        y_text -= 3.3

    # ==================== CỘT 2: HÌNH BÌNH HÀNH & CHỮ NHẬT ====================
    b2 = FancyBboxPatch((35, 5), 30, 67, boxstyle='round,pad=1,rounding_size=2',
                        facecolor='#F8FAFC', edgecolor='#2563EB', lw=1.8)
    ax.add_patch(b2)
    h2 = FancyBboxPatch((35, 64), 30, 8, boxstyle='round,pad=0.5,rounding_size=1.5',
                        facecolor='#EFF6FF', edgecolor='#2563EB', lw=1.2)
    ax.add_patch(h2)
    ax.text(50, 68, '2. HÌNH BÌNH HÀNH & CHỮ NHẬT',
            fontsize=10.0, ha='center', va='center', fontweight='bold', color='#1D4ED8')

    lines2 = [
        ('• Hình bình hành (HBH) - Dấu hiệu:', True, '#0F172A', 9.2),
        ('  1. Các cạnh đối song song (hoặc bằng nhau)', False, '#334155', 8.2),
        ('  2. Một cặp cạnh đối song song & bằng nhau', True, '#047857', 8.2),
        ('  3. Các góc đối bằng nhau', False, '#334155', 8.2),
        ('  4. Hai đường chéo cắt nhau tại trung điểm', True, '#047857', 8.2),
        ('', False, '#334155', 4),
        ('• Hình chữ nhật (HCN) - Dấu hiệu:', True, '#0F172A', 9.2),
        ('  1. Tứ giác có 3 góc vuông (90°)', True, '#DC2626', 8.2),
        ('  2. Hình thang cân có một góc vuông', False, '#334155', 8.2),
        ('  3. HBH có một góc vuông', True, '#047857', 8.2),
        ('  4. HBH có 2 đường chéo bằng nhau', True, '#047857', 8.2),
        ('  - Tính chất: Hai đường chéo bằng nhau', False, '#334155', 8.2),
        ('    và cắt nhau tại trung điểm mỗi đường', False, '#334155', 8.2)
    ]
    y_text = 60.5
    for txt, is_b, col, fs in lines2:
        if txt:
            ax.text(37.5, y_text, txt, fontsize=fs, ha='left', va='center',
                    fontweight='bold' if is_b else 'normal', color=col)
        y_text -= 3.3

    # ==================== CỘT 3: HÌNH THOI & HÌNH VUÔNG ====================
    b3 = FancyBboxPatch((67, 5), 30, 67, boxstyle='round,pad=1,rounding_size=2',
                        facecolor='#F8FAFC', edgecolor='#DC2626', lw=1.8)
    ax.add_patch(b3)
    h3 = FancyBboxPatch((67, 64), 30, 8, boxstyle='round,pad=0.5,rounding_size=1.5',
                        facecolor='#FEE2E2', edgecolor='#DC2626', lw=1.2)
    ax.add_patch(h3)
    ax.text(82, 68, '3. HÌNH THOI & HÌNH VUÔNG',
            fontsize=10.0, ha='center', va='center', fontweight='bold', color='#B91C1C')

    lines3 = [
        ('• Hình thoi - Dấu hiệu nhận biết:', True, '#0F172A', 9.2),
        ('  1. Tứ giác có 4 cạnh bằng nhau', False, '#334155', 8.2),
        ('  2. HBH có 2 cạnh kề bằng nhau', True, '#047857', 8.2),
        ('  3. HBH có 2 đường chéo vuông góc', True, '#DC2626', 8.2),
        ('  4. HBH có 1 đường chéo là phân giác', True, '#047857', 8.2),
        ('', False, '#334155', 4),
        ('• Hình vuông - Dấu hiệu nhận biết:', True, '#0F172A', 9.2),
        ('  (Vừa là Hình chữ nhật, vừa là Hình thoi)', True, '#B91C1C', 8.2),
        ('  1. HCN có 2 cạnh kề bằng nhau', False, '#334155', 8.2),
        ('  2. HCN có 2 đường chéo vuông góc', True, '#047857', 8.2),
        ('  3. HCN có 1 đường chéo là phân giác', False, '#334155', 8.2),
        ('  4. Hình thoi có một góc vuông (90°)', True, '#DC2626', 8.2),
        ('  5. Hình thoi có 2 đường chéo bằng nhau', True, '#047857', 8.2)
    ]
    y_text = 60.5
    for txt, is_b, col, fs in lines3:
        if txt:
            ax.text(69.5, y_text, txt, fontsize=fs, ha='left', va='center',
                    fontweight='bold' if is_b else 'normal', color=col)
        y_text -= 3.3

    out_file = os.path.join(OUT_DIR, 'mindmap_toan8_chuong3_ontap.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Đã vẽ thành công: {out_file}')

if __name__ == '__main__':
    draw_mindmap_chuong1_ontap()
    draw_mindmap_chuong3_ontap()
