# -*- coding: utf-8 -*-
"""
Script vẽ lại 100% hình học và mô hình toán học chuẩn SGK Kết nối tri thức Toán 8
Bám sát 100% hình gốc SGK từ các file PDF đầu vào.
Đảm bảo:
1. KHÔNG THIẾU NÉT: Canvas rộng rãi, margin an toàn, toàn bộ nét thấy/khuất nguyên vẹn.
2. CHỮ KHÔNG CHE HÌNH: Tên điểm, nhãn kích thước được định vị bên ngoài hình với khoảng cách hợp lý.
3. Độ phân giải cao 300 DPI, nền trắng tinh khôi, nét vẽ mực đen sắc sảo, đúng ký hiệu toán học SGK.
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc, Polygon, Rectangle, Circle, FancyBboxPatch

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../TROLYTHIEN/engine/hinh_ve_sgk'))
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Times New Roman']
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

def setup_canvas(figsize=(6, 4), xlim=(-1, 10), ylim=(-1, 7)):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.set_aspect('equal')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    return fig, ax

def save_fig(fig, filename):
    out_path = os.path.join(OUT_DIR, filename)
    fig.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.25, facecolor='white')
    plt.close(fig)
    print(f"Đã vẽ thành công: {filename}")

def right_angle(ax, p, v1, v2, size=0.25, color='black', lw=1.2):
    """Vẽ ký hiệu góc vuông tại điểm p với 2 hướng v1, v2"""
    v1 = np.array(v1, dtype=float)
    v2 = np.array(v2, dtype=float)
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 == 0 or n2 == 0: return
    v1 = v1 / n1 * size
    v2 = v2 / n2 * size
    p = np.array(p, dtype=float)
    pts = [p + v1, p + v1 + v2, p + v2]
    ax.plot([pts[0][0], pts[1][0], pts[2][0]], [pts[0][1], pts[1][1], pts[2][1]], color=color, lw=lw)

def equality_tick(ax, p1, p2, count=1, size=0.16, color='black', lw=1.2):
    """Vẽ vạch ký hiệu bằng nhau trên đoạn p1-p2"""
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    mid = (p1 + p2) / 2.0
    d = p2 - p1
    length = np.linalg.norm(d)
    if length == 0: return
    u = d / length
    n = np.array([-u[1], u[0]])
    spacing = 0.08
    for i in range(count):
        offset = (i - (count - 1) / 2.0) * spacing * u
        pt1 = mid + offset + n * size
        pt2 = mid + offset - n * size
        ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], color=color, lw=lw)

def tick_cross(ax, p1, p2, size=0.14, color='black', lw=1.2):
    """Vẽ vạch gạch chéo chữ x trên đoạn p1-p2 (ký hiệu đường chéo bằng nhau)"""
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    mid = (p1 + p2) / 2.0
    d = p2 - p1
    length = np.linalg.norm(d)
    if length == 0: return
    u = d / length
    n = np.array([-u[1], u[0]])
    pt1 = mid + (u + n) * size * 0.7
    pt2 = mid - (u + n) * size * 0.7
    pt3 = mid + (u - n) * size * 0.7
    pt4 = mid - (u - n) * size * 0.7
    ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], color=color, lw=lw)
    ax.plot([pt3[0], pt4[0]], [pt3[1], pt4[1]], color=color, lw=lw)

# ==========================================
# 1. HÌNH KHỐI HỘP CHỮ NHẬT (BÀI 5 SGK TRANG 22)
# ==========================================
def draw_hinh_01():
    # Khối 1: màu đen, kích thước 3y (đứng), 2x (ngang), x (sâu)
    # Khối 2: viền hồng sen #E11D48, đáy tô màu hồng cam #FECDD3, mũi tên chỉ vào đáy S = 2xy
    fig, ax = setup_canvas(figsize=(6.5, 3.8), xlim=(-1.0, 9.5), ylim=(-1.0, 5.5))

    # Kích thước khối 1: rộng 2.2, cao 3.0, sâu (xiên 45 độ): dx=0.9, dy=0.9
    w = 2.0; h = 2.8; dx = 0.8; dy = 0.8
    # Đáy trước khối 1: (0.5, 0.5) đến (0.5+w, 0.5)
    A = np.array([0.5, 0.5])
    B = np.array([0.5 + w, 0.5])
    C = np.array([0.5 + w + dx, 0.5 + dy])
    D = np.array([0.5 + dx, 0.5 + dy]) # đỉnh khuất

    A1 = A + np.array([0, h])
    B1 = B + np.array([0, h])
    C1 = C + np.array([0, h])
    D1 = D + np.array([0, h])

    # Nét đứt khuất khối 1 (từ D)
    ax.plot([D[0], A[0]], [D[1], A[1]], 'k--', lw=1.2)
    ax.plot([D[0], C[0]], [D[1], C[1]], 'k--', lw=1.2)
    ax.plot([D[0], D1[0]], [D[1], D1[1]], 'k--', lw=1.2)

    # Nét thấy khối 1
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', lw=1.8)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', lw=1.8)
    ax.plot([A[0], A1[0]], [A[1], A1[1]], 'k-', lw=1.8)
    ax.plot([B[0], B1[0]], [B[1], B1[1]], 'k-', lw=1.8)
    ax.plot([C[0], C1[0]], [C[1], C1[1]], 'k-', lw=1.8)
    ax.plot([A1[0], B1[0]], [A1[1], B1[1]], 'k-', lw=1.8)
    ax.plot([B1[0], C1[0]], [B1[1], C1[1]], 'k-', lw=1.8)
    ax.plot([C1[0], D1[0]], [C1[1], D1[1]], 'k-', lw=1.8)
    ax.plot([D1[0], A1[0]], [D1[1], A1[1]], 'k-', lw=1.8)

    # Nhãn kích thước khối 1 (đặt hoàn toàn bên ngoài)
    ax.text(A[0] - 0.45, A[1] + h/2, '$3y$', fontsize=13, va='center', ha='right', style='italic')
    ax.text(A[0] + w/2, A[1] - 0.35, '$2x$', fontsize=13, ha='center', va='top', style='italic')
    ax.text(B[0] + dx/2 + 0.25, B[1] + dy/2 - 0.1, '$x$', fontsize=13, ha='left', va='center', style='italic')

    # Khối 2: viền hồng sen #E11D48
    shift_x = 4.8
    P = A + np.array([shift_x, 0])
    Q = B + np.array([shift_x, 0])
    R = C + np.array([shift_x, 0])
    S = D + np.array([shift_x, 0])

    P1 = A1 + np.array([shift_x, 0])
    Q1 = B1 + np.array([shift_x, 0])
    R1 = C1 + np.array([shift_x, 0])
    S1 = D1 + np.array([shift_x, 0])

    pink_color = '#E11D48'
    bg_pink = '#FECDD3'

    # Tô màu đáy khối 2
    poly_bot = Polygon([P, Q, R, S], closed=True, facecolor=bg_pink, edgecolor='none')
    ax.add_patch(poly_bot)

    # Nét đứt khối 2
    ax.plot([S[0], P[0]], [S[1], P[1]], color=pink_color, linestyle='--', lw=1.4)
    ax.plot([S[0], R[0]], [S[1], R[1]], color=pink_color, linestyle='--', lw=1.4)
    ax.plot([S[0], S1[0]], [S[1], S1[1]], color=pink_color, linestyle='--', lw=1.4)

    # Nét thấy khối 2
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=pink_color, lw=2.0)
    ax.plot([Q[0], R[0]], [Q[1], R[1]], color=pink_color, lw=2.0)
    ax.plot([P[0], P1[0]], [P[1], P1[1]], color=pink_color, lw=2.0)
    ax.plot([Q[0], Q1[0]], [Q[1], Q1[1]], color=pink_color, lw=2.0)
    ax.plot([R[0], R1[0]], [R[1], R1[1]], color=pink_color, lw=2.0)
    ax.plot([P1[0], Q1[0]], [P1[1], Q1[1]], color=pink_color, lw=2.0)
    ax.plot([Q1[0], R1[0]], [Q1[1], R1[1]], color=pink_color, lw=2.0)
    ax.plot([R1[0], S1[0]], [R1[1], S1[1]], color=pink_color, lw=2.0)
    ax.plot([S1[0], P1[0]], [S1[1], P1[1]], color=pink_color, lw=2.0)

    # Mũi tên chỉ vào đáy khối 2
    arrow_start = np.array([P[0] + w/2 - 0.3, P[1] - 0.45])
    arrow_target = (P + Q + R + S) / 4.0
    ax.annotate('', xy=(arrow_target[0], arrow_target[1]), xytext=(arrow_start[0], arrow_start[1]),
                arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', lw=1.2))
    ax.text(arrow_start[0], arrow_start[1] - 0.15, '$S = 2xy$', fontsize=13, ha='center', va='top', style='italic')

    save_fig(fig, 'hinh_01_khoi_hop_chu_nhat.png')

# ==========================================
# 2. HÌNH 1.3: GẤP HỘP CHỮ NHẬT (BÀI 1.46 SGK TRANG 28)
# ==========================================
def draw_hinh_sgk_1_3():
    fig, ax = setup_canvas(figsize=(7.5, 3.6), xlim=(-0.8, 11.5), ylim=(-0.8, 4.5))

    # Bên trái: Tấm bìa chữ nhật kích thước w=3.4, h=2.2
    x0 = 0.5; y0 = 0.8
    bw = 3.6; bh = 2.4; c = 0.65
    # Tô nền nhẹ tấm bìa
    ax.add_patch(Rectangle((x0, y0), bw, bh, facecolor='#FFF1F2', edgecolor='black', lw=1.6))

    # Nếp gấp nét đứt hình chữ nhật bên trong
    ax.plot([x0+c, x0+bw-c, x0+bw-c, x0+c, x0+c], [y0+c, y0+c, y0+bh-c, y0+bh-c, y0+c], 'k--', lw=1.2)

    # 4 góc cắt nhỏ ghi chữ x
    ax.text(x0 + c/2, y0 + c/2, '$x$', fontsize=11, ha='center', va='center', style='italic')
    ax.text(x0 + bw - c/2, y0 + c/2, '$x$', fontsize=11, ha='center', va='center', style='italic')
    ax.text(x0 + c/2, y0 + bh - c/2, '$x$', fontsize=11, ha='center', va='center', style='italic')
    ax.text(x0 + bw - c/2, y0 + bh - c/2, '$x$', fontsize=11, ha='center', va='center', style='italic')

    # Nhãn y (chiều dài) và z (chiều rộng)
    ax.text(x0 + bw/2, y0 - 0.35, '$y$', fontsize=13, ha='center', va='top', style='italic')
    ax.text(x0 - 0.35, y0 + bh/2, '$z$', fontsize=13, ha='right', va='center', style='italic')

    # Bên phải: Chiếc hộp mở không nắp (3D)
    # Hộp có đáy: (6.5, 1.2), chiều dài 3.0, chiều sâu dx=0.8, dy=0.6, chiều cao c=0.65
    hx0 = 6.0; hy0 = 1.0
    hw = 2.8; hh = 0.75; hdx = 0.8; hdy = 0.7
    pink = '#E11D48'; bg_p = '#FECDD3'

    P = np.array([hx0, hy0])
    Q = np.array([hx0 + hw, hy0])
    R = np.array([hx0 + hw + hdx, hy0 + hdy])
    S = np.array([hx0 + hdx, hy0 + hdy])

    P1 = P + np.array([0, hh])
    Q1 = Q + np.array([0, hh])
    R1 = R + np.array([0, hh])
    S1 = S + np.array([0, hh])

    # Tô màu đáy hộp
    poly_bot = Polygon([P, Q, R, S], closed=True, facecolor=bg_p, edgecolor='none')
    ax.add_patch(poly_bot)

    # Nét đứt khuất đáy
    ax.plot([S[0], P[0]], [S[1], P[1]], color=pink, linestyle='--', lw=1.3)
    ax.plot([S[0], R[0]], [S[1], R[1]], color=pink, linestyle='--', lw=1.3)
    ax.plot([S[0], S1[0]], [S[1], S1[1]], color=pink, linestyle='--', lw=1.3)

    # Nét thấy
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=pink, lw=1.8)
    ax.plot([Q[0], R[0]], [Q[1], R[1]], color=pink, lw=1.8)
    ax.plot([P[0], P1[0]], [P[1], P1[1]], color=pink, lw=1.8)
    ax.plot([Q[0], Q1[0]], [Q[1], Q1[1]], color=pink, lw=1.8)
    ax.plot([R[0], R1[0]], [R[1], R1[1]], color=pink, lw=1.8)
    ax.plot([P1[0], Q1[0]], [P1[1], Q1[1]], color=pink, lw=1.8)
    ax.plot([Q1[0], R1[0]], [Q1[1], R1[1]], color=pink, lw=1.8)
    ax.plot([R1[0], S1[0]], [R1[1], S1[1]], color=pink, lw=1.8)
    ax.plot([S1[0], P1[0]], [S1[1], P1[1]], color=pink, lw=1.8)

    # Chú thích Hình 1.3
    ax.text((x0 + bw/2 + hx0 + hw/2)/2, -0.4, 'Hình 1.3', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_1_3_gap_hop.png')

# ==========================================
# 3. HÌNH HĐTN: CÔNG THỨC LÃI KÉP
# ==========================================
def draw_hinh_hdtn_lai_kep():
    # Thiết lập canvas rộng rãi, cân đối hoàn hảo
    fig, ax = setup_canvas(figsize=(10.5, 4.6), xlim=(-0.6, 14.5), ylim=(-0.8, 5.3))

    # ==================== PHẦN 1: BIỂU ĐỒ CỘT TĂNG TRƯỞNG LÃI KÉP ====================
    # Tiêu đề phần 1
    ax.text(2.6, 4.9, 'MÔ HÌNH TĂNG TRƯỞNG LŨY THỪA', fontsize=10.5, ha='center', va='center', fontweight='bold', color='#0369A1')

    # Trục hoành thời gian
    ax.annotate('', xy=(5.9, 0.45), xytext=(0.2, 0.45),
                arrowprops=dict(facecolor='#1E293B', edgecolor='#1E293B', width=1.4, headwidth=6, headlength=7))
    ax.text(6.05, 0.45, r'$n$', fontsize=11, ha='left', va='center', fontweight='bold', fontstyle='italic', color='#1E293B')

    years = ['Ban đầu\n(n = 0)', 'Kỳ 1\n(n = 1)', 'Kỳ 2\n(n = 2)', 'Kỳ 3\n(n = 3)', 'Kỳ n\n(n kỳ)']
    vals = [1.15, 1.55, 2.1, 2.8, 3.75]
    xs = [0.8, 1.8, 2.8, 3.8, 4.9]
    colors = ['#BAE6FD', '#7DD3FC', '#38BDF8', '#0284C7', '#0369A1']

    for i in range(5):
        rect = Rectangle((xs[i]-0.35, 0.45), 0.7, vals[i], facecolor=colors[i], edgecolor='#0F172A', lw=1.2)
        ax.add_patch(rect)
        ax.text(xs[i], 0.2, years[i], fontsize=8, ha='center', va='top', fontweight='bold', color='#0F172A')

    # Đường tăng trưởng đứt nét màu đỏ
    pts_x = xs
    pts_y = [0.45 + v for v in vals]
    ax.plot(pts_x, pts_y, 'ro--', lw=1.8, markersize=5)

    # Nhãn giá trị trên mỗi cột
    labels = [r'$P$', r'$P(1+r)$', r'$P(1+r)^2$', r'$P(1+r)^3$', r'$A = P(1+r)^n$']
    y_offsets = [0.15, 0.15, 0.15, 0.15, 0.20]
    for i in range(5):
        is_last = (i == 4)
        col = '#DC2626' if is_last else '#0F172A'
        fs = 11.0 if is_last else 9.5
        fw = 'bold'
        ax.text(xs[i], pts_y[i] + y_offsets[i], labels[i], fontsize=fs, ha='center', va='bottom', fontweight=fw, color=col)

    # Đường phân cách dọc thanh lịch giữa 2 phần
    ax.plot([6.4, 6.4], [0.1, 4.9], color='#CBD5E1', lw=1.2, ls='--')

    # ==================== PHẦN 2: GIAO DIỆN MÔ PHỎNG EXCEL CHUẨN ĐỒ HỌA ====================
    t0 = (6.7, 0.2)
    tw = 7.4
    th = 4.7

    # 1. Khung cửa sổ ứng dụng
    ax.add_patch(FancyBboxPatch(t0, tw, th, boxstyle='round,pad=0.06,rounding_size=0.12',
                                facecolor='#FFFFFF', edgecolor='#059669', lw=1.6))

    # 2. Thanh tiêu đề xanh lá Excel
    ax.add_patch(FancyBboxPatch((t0[0], t0[1] + th - 0.65), tw, 0.65, boxstyle='round,pad=0.04,rounding_size=0.08',
                            facecolor='#107C41', edgecolor='none'))
    ax.text(t0[0] + tw/2, t0[1] + th - 0.35, 'MÔ PHỎNG BẢNG TÍNH EXCEL - TÍNH LÃI KÉP', fontsize=10,
            color='white', ha='center', va='center', fontweight='bold')

    # 3. Thanh công thức (Formula Bar)
    fbar_y = t0[1] + th - 1.15
    ax.add_patch(Rectangle((t0[0]+0.15, fbar_y), tw-0.3, 0.4, facecolor='#F1F5F9', edgecolor='#CBD5E1', lw=0.8))
    ax.text(t0[0] + 0.35, fbar_y + 0.2, 'fx', fontsize=9.5, fontweight='bold', fontstyle='italic', color='#64748B', va='center')
    ax.plot([t0[0]+0.7, t0[0]+0.7], [fbar_y+0.05, fbar_y+0.35], color='#CBD5E1', lw=1.0)
    ax.text(t0[0] + 0.9, fbar_y + 0.2, '= B1 * (1 + B2) ^ B3', fontsize=9, fontweight='bold', color='#0F172A', va='center')

    # 4. Tiêu đề các cột bảng tính
    th_y = fbar_y - 0.45
    cols_excel = ['Kỳ (n)', 'Vốn gốc (P)', 'Tiền lãi (r = 6%)', 'Tổng tiền (A)']
    col_w = [1.25, 1.95, 1.95, 1.95]
    col_xs = [t0[0] + 0.15]
    for w in col_w[:-1]:
        col_xs.append(col_xs[-1] + w)

    # Nền thanh tiêu đề cột
    ax.add_patch(Rectangle((t0[0]+0.15, th_y), tw-0.3, 0.38, facecolor='#E2E8F0', edgecolor='#CBD5E1', lw=0.8))
    for i, (cx, w, cname) in enumerate(zip(col_xs, col_w, cols_excel)):
        ax.text(cx + w/2, th_y + 0.19, cname, fontsize=8, ha='center', va='center', fontweight='bold', color='#1E293B')

    # 5. Các dòng dữ liệu
    rows_data = [
        ('Năm 1', '100.000.000 đ', '6.000.000 đ', '106.000.000 đ'),
        ('Năm 2', '106.000.000 đ', '6.360.000 đ', '112.360.000 đ'),
        ('Năm 3', '112.360.000 đ', '6.741.600 đ', '119.101.600 đ'),
        ('...', '...', '...', '...'),
        ('Năm n', r'$P \cdot (1+r)^{n-1}$', r'$r \cdot A_{n-1}$', r'$P \cdot (1+r)^n$')
    ]

    cur_y = th_y - 0.4
    for r_idx, rdata in enumerate(rows_data):
        bg_col = '#F8FAFC' if r_idx % 2 == 1 else '#FFFFFF'
        ax.add_patch(Rectangle((t0[0]+0.15, cur_y), tw-0.3, 0.38, facecolor=bg_col, edgecolor='#E2E8F0', lw=0.5))
        
        is_last = (r_idx == 4)
        for c_idx, (cx, w, val) in enumerate(zip(col_xs, col_w, rdata)):
            fw = 'bold' if (is_last or c_idx == 3) else 'normal'
            col = '#DC2626' if (is_last and c_idx == 3) else ('#059669' if is_last else '#1E293B')
            fs = 8.5 if not is_last else 8.0
            ax.text(cx + w/2, cur_y + 0.19, val, fontsize=fs, ha='center', va='center', fontweight=fw, color=col)
        cur_y -= 0.4

    # 6. Hộp ghi chú sư phạm ở đáy
    note_y = t0[1] + 0.10
    ax.add_patch(Rectangle((t0[0]+0.3, note_y), tw-0.6, 0.52, facecolor='#FEF3C7', edgecolor='#F59E0B', lw=0.9))
    ax.text(t0[0] + tw/2, note_y + 0.34, '• Cơ chế: Tiền lãi kỳ trước tự động gộp vào vốn gốc kỳ sau',
            fontsize=7.0, ha='center', va='center', fontweight='bold', color='#92400E')
    ax.text(t0[0] + tw/2, note_y + 0.16, '• Tăng trưởng theo cấp số nhân (hàm mũ):  A = P · (1 + r)ⁿ',
            fontsize=7.0, ha='center', va='center', fontweight='bold', color='#B45309')

    save_fig(fig, 'hinh_hdtn_cong_thuc_lai_kep.png')

# ==========================================
# 4. HÌNH 3.46: GẤP GIẤY HÌNH THOI VÀ HÌNH VUÔNG (SGK TRANG 67)
# ==========================================
def draw_hinh_sgk_3_46():
    fig, ax = setup_canvas(figsize=(7.5, 3.2), xlim=(-0.8, 9.5), ylim=(-0.8, 3.8))

    # Hình a: Cắt xiên AB
    O1 = np.array([0.8, 0.6])
    A1 = O1 + np.array([0, 2.2])
    B1 = O1 + np.array([2.0, 0])
    right_angle(ax, O1, [1, 0], [0, 1], size=0.22)
    # Đường gấp đôi
    ax.plot([O1[0], A1[0]], [O1[1], A1[1]], 'k-', lw=1.8)
    ax.plot([O1[0], B1[0]], [O1[1], B1[1]], 'k-', lw=1.8)
    # Vết cắt AB
    ax.plot([A1[0], B1[0]], [A1[1], B1[1]], 'k-', lw=1.8)
    # Viền giấy lượn sóng tượng trưng
    ax.plot([A1[0], A1[0]+0.8, B1[0]+0.4, B1[0]], [A1[1], A1[1]+0.3, B1[1]+0.8, B1[1]], 'k--', lw=1.0)

    ax.text(O1[0]-0.25, O1[1]-0.15, '$O$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(A1[0]-0.25, A1[1], '$A$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(B1[0], B1[1]-0.3, '$B$', fontsize=12, fontweight='bold', color='#0284C7')
    # Biểu tượng cây kéo cắt
    ax.text((A1[0]+B1[0])/2 + 0.15, (A1[1]+B1[1])/2 + 0.15, '✂', fontsize=14, rotation=45)
    ax.text(1.8, -0.4, 'a)', fontsize=11, ha='center', style='italic')

    # Hình b: OA = OB (tạo hình vuông)
    shift_x = 4.8
    O2 = O1 + np.array([shift_x, 0])
    A2 = O2 + np.array([0, 2.0])
    B2 = O2 + np.array([2.0, 0])
    right_angle(ax, O2, [1, 0], [0, 1], size=0.22)
    equality_tick(ax, O2, A2, 1)
    equality_tick(ax, O2, B2, 1)

    ax.plot([O2[0], A2[0]], [O2[1], A2[1]], 'k-', lw=1.8)
    ax.plot([O2[0], B2[0]], [O2[1], B2[1]], 'k-', lw=1.8)
    ax.plot([A2[0], B2[0]], [A2[1], B2[1]], 'k-', lw=1.8)
    ax.plot([A2[0], A2[0]+0.8, B2[0]+0.4, B2[0]], [A2[1], A2[1]+0.3, B2[1]+0.8, B2[1]], 'k--', lw=1.0)

    ax.text(O2[0]-0.25, O2[1]-0.15, '$O$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(A2[0]-0.25, A2[1], '$A$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(B2[0], B2[1]-0.3, '$B$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text((A2[0]+B2[0])/2 + 0.15, (A2[1]+B2[1])/2 + 0.15, '✂', fontsize=14, rotation=45)
    ax.text(6.6, -0.4, 'b)', fontsize=11, ha='center', style='italic')

    ax.text(4.2, -0.65, 'Hình 3.46', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_46_gap_giay.png')

# ==========================================
# 5. HÌNH 3.47: HÌNH THOI ABCD (SGK TRANG 67)
# ==========================================
def draw_hinh_sgk_3_47():
    fig, ax = setup_canvas(figsize=(5.5, 3.5), xlim=(-0.8, 6.0), ylim=(-0.8, 4.2))
    # 4 đỉnh: A (trái), B (trên), C (phải), D (dưới)
    A = np.array([0.8, 1.8])
    B = np.array([2.8, 3.2])
    C = np.array([4.8, 1.8])
    D = np.array([2.8, 0.4])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.0)

    # 4 vạch bằng nhau
    equality_tick(ax, A, B, 1)
    equality_tick(ax, B, C, 1)
    equality_tick(ax, C, D, 1)
    equality_tick(ax, D, A, 1)

    ax.text(A[0]-0.25, A[1], '$A$', fontsize=13, ha='right', va='center', fontweight='bold', color='#0284C7')
    ax.text(B[0], B[1]+0.2, '$B$', fontsize=13, ha='center', va='bottom', fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.25, C[1], '$C$', fontsize=13, ha='left', va='center', fontweight='bold', color='#0284C7')
    ax.text(D[0], D[1]-0.25, '$D$', fontsize=13, ha='center', va='top', fontweight='bold', color='#0284C7')

    ax.text(2.8, -0.45, 'Hình 3.47', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_47_hinh_thoi.png')

# ==========================================
# 6. HÌNH 3.48: ĐƯỜNG CHÉO HÌNH THOI (SGK TRANG 68)
# ==========================================
def draw_hinh_sgk_3_48():
    fig, ax = setup_canvas(figsize=(5.5, 4.0), xlim=(-0.8, 6.0), ylim=(-0.8, 4.8))
    # Đỉnh: A (trên), B (trái), C (dưới), D (phải)
    A = np.array([2.8, 3.8])
    B = np.array([0.8, 2.0])
    C = np.array([2.8, 0.2])
    D = np.array([4.8, 2.0])
    O = np.array([2.8, 2.0])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.0)
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k-', lw=1.5)
    ax.plot([B[0], D[0]], [B[1], D[1]], 'k-', lw=1.5)

    right_angle(ax, O, [1, 0], [0, 1], size=0.22)

    # Đánh số góc 1, 2 tại mỗi đỉnh
    ax.text(A[0]-0.15, A[1]-0.45, '1', fontsize=10)
    ax.text(A[0]+0.1, A[1]-0.45, '2', fontsize=10)

    ax.text(B[0]+0.45, B[1]+0.1, '1', fontsize=10)
    ax.text(B[0]+0.45, B[1]-0.25, '2', fontsize=10)

    ax.text(C[0]-0.15, C[1]+0.35, '1', fontsize=10)
    ax.text(C[0]+0.1, C[1]+0.35, '2', fontsize=10)

    ax.text(D[0]-0.55, D[1]+0.1, '2', fontsize=10)
    ax.text(D[0]-0.55, D[1]-0.25, '1', fontsize=10)

    ax.text(A[0], A[1]+0.2, '$A$', fontsize=13, ha='center', va='bottom', fontweight='bold', color='#0284C7')
    ax.text(B[0]-0.25, B[1], '$B$', fontsize=13, ha='right', va='center', fontweight='bold', color='#0284C7')
    ax.text(C[0], C[1]-0.25, '$C$', fontsize=13, ha='center', va='top', fontweight='bold', color='#0284C7')
    ax.text(D[0]+0.25, D[1], '$D$', fontsize=13, ha='left', va='center', fontweight='bold', color='#0284C7')
    ax.text(O[0]-0.2, O[1]-0.2, '$O$', fontsize=12, fontweight='bold', color='#0284C7')

    ax.text(2.8, -0.45, 'Hình 3.48', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_48_duong_cheo_hinh_thoi.png')

# ==========================================
# 7. HÌNH 3.49: HAI ĐƯỜNG TRÒN DỰNG HÌNH THOI (SGK TRANG 68)
# ==========================================
def draw_hinh_sgk_3_49():
    fig, ax = setup_canvas(figsize=(6.5, 4.2), xlim=(-0.8, 7.5), ylim=(-0.8, 5.0))
    A = np.array([2.0, 2.2])
    C = np.array([4.8, 2.2])
    R = 2.0
    h = np.sqrt(R**2 - 1.4**2)
    B = np.array([3.4, 2.2 + h])
    D = np.array([3.4, 2.2 - h])

    circA = Circle(A, R, edgecolor='black', facecolor='none', lw=1.3)
    circC = Circle(C, R, edgecolor='black', facecolor='none', lw=1.3)
    ax.add_patch(circA)
    ax.add_patch(circC)

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.0)
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k-', lw=1.2)
    ax.plot([B[0], D[0]], [B[1], D[1]], 'k-', lw=1.2)

    equality_tick(ax, A, B, 1)
    equality_tick(ax, B, C, 1)
    equality_tick(ax, C, D, 1)
    equality_tick(ax, D, A, 1)

    right_angle(ax, np.array([3.4, 2.2]), [1, 0], [0, 1], size=0.2)

    ax.text(A[0]-0.25, A[1], '$A$', fontsize=13, ha='right', va='center', fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.25, C[1], '$C$', fontsize=13, ha='left', va='center', fontweight='bold', color='#0284C7')
    ax.text(B[0], B[1]+0.2, '$B$', fontsize=13, ha='center', va='bottom', fontweight='bold', color='#0284C7')
    ax.text(D[0], D[1]-0.25, '$D$', fontsize=13, ha='center', va='top', fontweight='bold', color='#0284C7')

    save_fig(fig, 'hinh_sgk_3_49_hai_duong_tron.png')

# ==========================================
# 8. HÌNH 3.50: VÍ DỤ 2 NHẬN BIẾT HÌNH THOI (SGK TRANG 69)
# ==========================================
def draw_hinh_sgk_3_50():
    fig, ax = setup_canvas(figsize=(8.0, 3.5), xlim=(-0.8, 10.5), ylim=(-0.8, 4.5))

    # Hình a: Hình bình hành ABCD
    A = np.array([1.5, 3.2]); B = np.array([4.2, 3.2])
    D = np.array([0.5, 0.8]); C = np.array([3.2, 0.8])
    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.0)
    equality_tick(ax, A, B, 1)
    equality_tick(ax, B, C, 1)
    # Cung góc A và C
    ax.add_patch(Arc(A, 0.6, 0.6, angle=0, theta1=240, theta2=360, color='black', lw=1.2))
    ax.add_patch(Arc(C, 0.6, 0.6, angle=0, theta1=60, theta2=180, color='black', lw=1.2))
    # Cung góc B và D
    ax.add_patch(Arc(D, 0.6, 0.6, angle=0, theta1=0, theta2=65, color='black', lw=1.2))
    ax.add_patch(Arc(B, 0.6, 0.6, angle=0, theta1=180, theta2=245, color='black', lw=1.2))

    ax.text(A[0], A[1]+0.15, '$A$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(B[0]+0.15, B[1], '$B$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.15, C[1]-0.2, '$C$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(D[0]-0.25, D[1], '$D$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(2.35, -0.4, 'a)', fontsize=11, ha='center', style='italic')

    # Hình b: Tứ giác MNPQ
    M = np.array([5.5, 2.0]); N = np.array([7.2, 3.0]); P = np.array([9.8, 2.0]); Q = np.array([7.2, 1.0])
    ax.plot([M[0], N[0], P[0], Q[0], M[0]], [M[1], N[1], P[1], Q[1], M[1]], 'k-', lw=2.0)
    ax.plot([M[0], P[0]], [M[1], P[1]], 'k-', lw=1.2)
    equality_tick(ax, M, N, 1)
    equality_tick(ax, M, Q, 1)
    equality_tick(ax, N, P, 2)
    equality_tick(ax, Q, P, 2)

    ax.text(M[0]-0.25, M[1], '$M$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(N[0], N[1]+0.15, '$N$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(P[0]+0.2, P[1], '$P$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(Q[0], Q[1]-0.25, '$Q$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(7.6, -0.4, 'b)', fontsize=11, ha='center', style='italic')

    ax.text(5.0, -0.65, 'Hình 3.50', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_50_nhan_biet_hinh_thoi.png')

# ==========================================
# 9. HÌNH 3.51: LUYỆN TẬP 1 NHẬN BIẾT HÌNH THOI (SGK TRANG 69)
# ==========================================
def draw_hinh_sgk_3_51():
    fig, ax = setup_canvas(figsize=(8.5, 3.2), xlim=(-0.8, 11.5), ylim=(-0.8, 3.8))

    # a) Tứ giác 2 đường chéo vuông góc tại trung điểm
    A1 = np.array([0.5, 1.8]); B1 = np.array([1.8, 3.0]); C1 = np.array([3.1, 1.8]); D1 = np.array([1.8, 0.6])
    O1 = np.array([1.8, 1.8])
    ax.plot([A1[0], B1[0], C1[0], D1[0], A1[0]], [A1[1], B1[1], C1[1], D1[1], A1[1]], 'k-', lw=1.8)
    ax.plot([A1[0], C1[0]], [A1[1], C1[1]], 'k-', lw=1.2)
    ax.plot([B1[0], D1[0]], [B1[1], D1[1]], 'k-', lw=1.2)
    right_angle(ax, O1, [1, 0], [0, 1], size=0.2)
    equality_tick(ax, A1, O1, 2)
    equality_tick(ax, O1, C1, 2)
    equality_tick(ax, B1, O1, 1)
    equality_tick(ax, O1, D1, 1)
    ax.text(1.8, -0.4, 'a)', fontsize=11, ha='center', style='italic')

    # b) Tứ giác 4 cạnh bằng nhau
    shift2 = 3.8
    A2 = A1 + np.array([shift2, 0]); B2 = B1 + np.array([shift2, 0])
    C2 = C1 + np.array([shift2, 0]); D2 = D1 + np.array([shift2, 0])
    ax.plot([A2[0], B2[0], C2[0], D2[0], A2[0]], [A2[1], B2[1], C2[1], D2[1], A2[1]], 'k-', lw=1.8)
    equality_tick(ax, A2, B2, 1)
    equality_tick(ax, B2, C2, 1)
    equality_tick(ax, C2, D2, 1)
    equality_tick(ax, D2, A2, 1)
    ax.text(1.8+shift2, -0.4, 'b)', fontsize=11, ha='center', style='italic')

    # c) Tứ giác diều (2 đường chéo vuông góc nhưng chỉ 1 đường bị chia đôi)
    shift3 = 7.6
    A3 = np.array([0.5+shift3, 1.8]); B3 = np.array([1.8+shift3, 2.8])
    C3 = np.array([3.4+shift3, 1.8]); D3 = np.array([1.8+shift3, 0.8])
    O3 = np.array([1.8+shift3, 1.8])
    ax.plot([A3[0], B3[0], C3[0], D3[0], A3[0]], [A3[1], B3[1], C3[1], D3[1], A3[1]], 'k-', lw=1.8)
    ax.plot([A3[0], C3[0]], [A3[1], C3[1]], 'k-', lw=1.2)
    ax.plot([B3[0], D3[0]], [B3[1], D3[1]], 'k-', lw=1.2)
    right_angle(ax, O3, [1, 0], [0, 1], size=0.2)
    ax.add_patch(Arc(A3, 0.5, 0.5, angle=0, theta1=-35, theta2=35, color='black', lw=1.0))
    ax.text(1.8+shift3, -0.4, 'c)', fontsize=11, ha='center', style='italic')

    ax.text(5.6, -0.65, 'Hình 3.51', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_51_luyen_tap_1.png')

# ==========================================
# 10. HÌNH 3.52: HÌNH VUÔNG ABCD (SGK TRANG 69)
# ==========================================
def draw_hinh_sgk_3_52():
    fig, ax = setup_canvas(figsize=(4.8, 4.2), xlim=(-0.8, 5.0), ylim=(-0.8, 5.0))
    A = np.array([0.8, 3.8])
    B = np.array([3.8, 3.8])
    C = np.array([3.8, 0.8])
    D = np.array([0.8, 0.8])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.2)

    right_angle(ax, A, [1, 0], [0, -1], size=0.25)
    right_angle(ax, B, [-1, 0], [0, -1], size=0.25)
    right_angle(ax, C, [-1, 0], [0, 1], size=0.25)
    right_angle(ax, D, [1, 0], [0, 1], size=0.25)

    equality_tick(ax, A, B, 1)
    equality_tick(ax, B, C, 1)
    equality_tick(ax, C, D, 1)
    equality_tick(ax, D, A, 1)

    ax.text(A[0]-0.25, A[1]+0.15, '$A$', fontsize=13, ha='right', fontweight='bold', color='#0284C7')
    ax.text(B[0]+0.2, B[1]+0.15, '$B$', fontsize=13, ha='left', fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.2, C[1]-0.25, '$C$', fontsize=13, ha='left', fontweight='bold', color='#0284C7')
    ax.text(D[0]-0.25, D[1]-0.25, '$D$', fontsize=13, ha='right', fontweight='bold', color='#0284C7')

    ax.text(2.3, -0.45, 'Hình 3.52', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_52_hinh_vuong.png')

# ==========================================
# 11. HÌNH 3.53: VÍ DỤ 3 NHẬN BIẾT HÌNH VUÔNG (SGK TRANG 70)
# ==========================================
def draw_hinh_sgk_3_53():
    fig, ax = setup_canvas(figsize=(7.5, 4.0), xlim=(-0.8, 9.5), ylim=(-0.8, 4.5))

    # a) Hình chữ nhật nghiêng ABCD có AD = DC
    A = np.array([2.0, 3.8]); B = np.array([3.4, 2.4])
    C = np.array([2.0, 1.0]); D = np.array([0.6, 2.4])
    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.0)
    right_angle(ax, A, [B[0]-A[0], B[1]-A[1]], [D[0]-A[0], D[1]-A[1]], size=0.22)
    right_angle(ax, D, [A[0]-D[0], A[1]-D[1]], [C[0]-D[0], C[1]-D[1]], size=0.22)
    right_angle(ax, C, [D[0]-C[0], D[1]-C[1]], [B[0]-C[0], B[1]-C[1]], size=0.22)
    equality_tick(ax, A, D, 1)
    equality_tick(ax, D, C, 1)

    ax.text(A[0], A[1]+0.2, '$A$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(B[0]+0.2, B[1], '$B$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(C[0], C[1]-0.25, '$C$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(D[0]-0.25, D[1], '$D$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(2.0, -0.4, 'a)', fontsize=11, ha='center', style='italic')

    # b) Tứ giác MNPQ có MP vuông góc NQ
    M = np.array([6.5, 3.8]); N = np.array([7.8, 2.4])
    P = np.array([6.5, 1.0]); Q = np.array([5.2, 2.4])
    O = np.array([6.5, 2.4])
    ax.plot([M[0], N[0], P[0], Q[0], M[0]], [M[1], N[1], P[1], Q[1], M[1]], 'k-', lw=2.0)
    ax.plot([M[0], P[0]], [M[1], P[1]], 'k-', lw=1.2)
    ax.plot([Q[0], N[0]], [Q[1], N[1]], 'k-', lw=1.2)
    right_angle(ax, O, [1, 0], [0, 1], size=0.2)
    equality_tick(ax, Q, O, 1)
    equality_tick(ax, O, N, 1)
    equality_tick(ax, M, O, 2)
    equality_tick(ax, O, P, 2)

    ax.text(M[0], M[1]+0.2, '$M$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(N[0]+0.2, N[1], '$N$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(P[0], P[1]-0.25, '$P$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(Q[0]-0.25, Q[1], '$Q$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(6.5, -0.4, 'b)', fontsize=11, ha='center', style='italic')

    ax.text(4.25, -0.65, 'Hình 3.53', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_53_nhan_biet_hinh_vuong.png')

# ==========================================
# 12. HÌNH 3.54: LUYỆN TẬP 2 NHẬN BIẾT HÌNH VUÔNG (SGK TRANG 71)
# ==========================================
def draw_hinh_sgk_3_54():
    fig, ax = setup_canvas(figsize=(8.5, 3.6), xlim=(-0.8, 11.5), ylim=(-0.8, 4.2))

    # a) Tứ giác ABCD
    A = np.array([0.5, 2.0]); B = np.array([1.8, 3.3]); C = np.array([3.1, 2.0]); D = np.array([1.8, 0.7])
    O = np.array([1.8, 2.0])
    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=1.8)
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k-', lw=1.2)
    ax.plot([B[0], D[0]], [B[1], D[1]], 'k-', lw=1.2)
    equality_tick(ax, A, B, 2)
    equality_tick(ax, B, C, 2)
    equality_tick(ax, A, O, 1)
    equality_tick(ax, O, C, 1)
    equality_tick(ax, B, O, 1)
    equality_tick(ax, O, D, 1)
    ax.text(A[0]-0.2, A[1], '$A$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(B[0], B[1]+0.15, '$B$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.15, C[1], '$C$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(D[0], D[1]-0.2, '$D$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(1.8, -0.4, 'a)', fontsize=11, ha='center', style='italic')

    # b) Tứ giác EFGH
    shift2 = 3.8
    E = A + np.array([shift2, 0]); F = B + np.array([shift2, 0])
    G = C + np.array([shift2, 0]); H = D + np.array([shift2, 0])
    P = O + np.array([shift2, 0])
    ax.plot([E[0], F[0], G[0], H[0], E[0]], [E[1], F[1], G[1], H[1], E[1]], 'k-', lw=1.8)
    ax.plot([E[0], G[0]], [E[1], G[1]], 'k-', lw=1.2)
    ax.plot([F[0], H[0]], [F[1], H[1]], 'k-', lw=1.2)
    equality_tick(ax, E, P, 1)
    equality_tick(ax, P, G, 1)
    equality_tick(ax, F, P, 2)
    equality_tick(ax, P, H, 2)
    ax.text(F[0]-0.35, F[1]-0.45, '$45^\\circ$', fontsize=9)
    ax.text(F[0]+0.1, F[1]-0.45, '$45^\\circ$', fontsize=9)
    ax.text(E[0]-0.2, E[1], '$E$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(F[0], F[1]+0.15, '$F$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(G[0]+0.15, G[1], '$G$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(H[0], H[1]-0.2, '$H$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(P[0]-0.2, P[1]-0.2, '$P$', fontsize=10, fontweight='bold', color='#0284C7')
    ax.text(1.8+shift2, -0.4, 'b)', fontsize=11, ha='center', style='italic')

    # c) Tứ giác IJKL
    shift3 = 7.6
    I = A + np.array([shift3, 0]); J = B + np.array([shift3, 0])
    K = C + np.array([shift3, 0]); L = D + np.array([shift3, 0])
    Q = O + np.array([shift3, 0])
    ax.plot([I[0], J[0], K[0], L[0], I[0]], [I[1], J[1], K[1], L[1], I[1]], 'k-', lw=1.8)
    ax.plot([I[0], K[0]], [I[1], K[1]], 'k-', lw=1.2)
    ax.plot([J[0], L[0]], [J[1], L[1]], 'k-', lw=1.2)
    right_angle(ax, Q, [0, 1], [-1, 0], size=0.18)
    equality_tick(ax, I, Q, 1)
    equality_tick(ax, Q, K, 1)
    equality_tick(ax, J, Q, 1)
    equality_tick(ax, Q, L, 1)
    ax.text(I[0]-0.2, I[1], '$I$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(J[0], J[1]+0.15, '$J$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(K[0]+0.15, K[1], '$K$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(L[0], L[1]-0.2, '$L$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(Q[0]-0.2, Q[1]-0.2, '$Q$', fontsize=10, fontweight='bold', color='#0284C7')
    ax.text(1.8+shift3, -0.4, 'c)', fontsize=11, ha='center', style='italic')

    ax.text(5.6, -0.65, 'Hình 3.54', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_54_luyen_tap_2.png')

# ==========================================
# 13. HÌNH 3.55: BÀI TẬP 3.29 (SGK TRANG 71)
# ==========================================
def draw_hinh_sgk_3_55():
    fig, ax = setup_canvas(figsize=(8.5, 4.5), xlim=(-0.8, 10.5), ylim=(-0.8, 5.5))

    # a) Hình bình hành ABCD
    A = np.array([1.2, 4.8]); B = np.array([3.8, 4.8])
    D = np.array([0.5, 3.2]); C = np.array([3.1, 3.2])
    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=1.8)
    equality_tick(ax, A, B, 2)
    equality_tick(ax, D, C, 2)
    equality_tick(ax, A, D, 1)
    equality_tick(ax, B, C, 1)
    ax.text(A[0], A[1]+0.15, '$A$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(B[0]+0.15, B[1], '$B$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.15, C[1]-0.2, '$C$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(D[0]-0.2, D[1], '$D$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(2.15, 2.7, 'a)', fontsize=11, ha='center', style='italic')

    # b) Tứ giác EFGH
    E = np.array([5.5, 4.0]); F = np.array([7.0, 5.0]); G = np.array([8.5, 4.0]); H = np.array([7.0, 3.0])
    O = np.array([7.0, 4.0])
    ax.plot([E[0], F[0], G[0], H[0], E[0]], [E[1], F[1], G[1], H[1], E[1]], 'k-', lw=1.8)
    ax.plot([E[0], G[0]], [E[1], G[1]], 'k-', lw=1.2)
    ax.plot([F[0], H[0]], [F[1], H[1]], 'k-', lw=1.2)
    right_angle(ax, O, [1, 0], [0, -1], size=0.18)
    equality_tick(ax, E, O, 2)
    equality_tick(ax, O, G, 2)
    equality_tick(ax, F, O, 1)
    equality_tick(ax, O, H, 1)
    ax.text(E[0]-0.2, E[1], '$E$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(F[0], F[1]+0.15, '$F$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(G[0]+0.15, G[1], '$G$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(H[0], H[1]-0.25, '$H$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(7.0, 2.5, 'b)', fontsize=11, ha='center', style='italic')

    # c) Tứ giác MNPQ
    M = np.array([0.8, 1.2]); N = np.array([2.0, 2.4]); P = np.array([3.2, 1.2]); Q = np.array([2.0, 0.0])
    Om = np.array([2.0, 1.2])
    ax.plot([M[0], N[0], P[0], Q[0], M[0]], [M[1], N[1], P[1], Q[1], M[1]], 'k-', lw=1.8)
    ax.plot([M[0], P[0]], [M[1], P[1]], 'k-', lw=1.2)
    ax.plot([N[0], Q[0]], [N[1], Q[1]], 'k-', lw=1.2)
    right_angle(ax, Om, [1, 0], [0, -1], size=0.18)
    ax.text(M[0]+0.25, M[1]+0.15, '$45^\\circ$', fontsize=9)
    ax.text(M[0]-0.2, M[1], '$M$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(N[0], N[1]+0.15, '$N$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(P[0]+0.15, P[1], '$P$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(Q[0], Q[1]-0.25, '$Q$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(2.0, -0.4, 'c)', fontsize=11, ha='center', style='italic')

    # d) Tứ giác RSTU
    R = np.array([5.5, 1.2]); S = np.array([7.0, 2.0]); U = np.array([9.2, 1.2]); T = np.array([7.0, 0.4])
    ax.plot([R[0], S[0], U[0], T[0], R[0]], [R[1], S[1], U[1], T[1], R[1]], 'k-', lw=1.8)
    ax.plot([R[0], U[0]], [R[1], U[1]], 'k-', lw=1.2)
    equality_tick(ax, R, S, 2)
    equality_tick(ax, R, T, 2)
    equality_tick(ax, S, U, 1)
    equality_tick(ax, T, U, 1)
    ax.add_patch(Arc(R, 0.5, 0.5, angle=0, theta1=-25, theta2=25, color='black', lw=1.0))
    ax.text(R[0]-0.2, R[1], '$R$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(S[0], S[1]+0.15, '$S$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(U[0]+0.15, U[1], '$U$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(T[0], T[1]-0.25, '$T$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(7.35, -0.4, 'd)', fontsize=11, ha='center', style='italic')

    ax.text(4.75, -0.65, 'Hình 3.55', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_55_bai_3_29.png')

# ==========================================
# 14. HÌNH 3.56: BÀI TẬP 3.33 (SGK TRANG 72)
# ==========================================
def draw_hinh_sgk_3_56():
    fig, ax = setup_canvas(figsize=(5.5, 4.0), xlim=(-0.8, 6.0), ylim=(-0.8, 4.8))
    # Hình chữ nhật ABCD (A, D ở trên, B, C ở dưới)
    A = np.array([1.2, 3.8]); D = np.array([4.2, 3.8])
    B = np.array([1.2, 1.2]); C = np.array([4.2, 1.2])
    M = np.array([2.7, 1.2]) # M là trung điểm BC (ở đây cạnh đáy là BC)

    ax.plot([A[0], D[0], C[0], B[0], A[0]], [A[1], D[1], C[1], B[1], A[1]], 'k-', lw=2.0)
    ax.plot([A[0], M[0]], [A[1], M[1]], 'k-', lw=1.8)
    ax.plot([D[0], M[0]], [D[1], M[1]], 'k-', lw=1.8)

    # MA vuông góc MD tại M
    right_angle(ax, M, [A[0]-M[0], A[1]-M[1]], [D[0]-M[0], D[1]-M[1]], size=0.25)
    equality_tick(ax, B, M, 1)
    equality_tick(ax, M, C, 1)

    ax.text(A[0], A[1]+0.2, '$A$', fontsize=13, ha='center', fontweight='bold', color='#0284C7')
    ax.text(D[0], D[1]+0.2, '$D$', fontsize=13, ha='center', fontweight='bold', color='#0284C7')
    ax.text(B[0]-0.25, B[1]-0.15, '$B$', fontsize=13, ha='right', fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.25, C[1]-0.15, '$C$', fontsize=13, ha='left', fontweight='bold', color='#0284C7')
    ax.text(M[0], M[1]-0.3, '$M$', fontsize=13, ha='center', fontweight='bold', color='#0284C7')

    ax.text(2.7, -0.45, 'Hình 3.56', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_56_bai_3_33.png')

# ==========================================
# 15. HÌNH 3.57: VÍ DỤ DỰNG HÌNH VUÔNG (SGK TRANG 73)
# ==========================================
def draw_hinh_sgk_3_57():
    fig, ax = setup_canvas(figsize=(5.5, 4.2), xlim=(-0.8, 6.0), ylim=(-0.8, 5.0))
    # A vuông góc dưới trái, B dưới phải, D trên trái, C trên phải
    A = np.array([1.2, 1.2]); B = np.array([4.0, 1.2]); D = np.array([1.2, 4.0]); C = np.array([4.0, 4.0])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.0)
    right_angle(ax, A, [1, 0], [0, 1], size=0.25)
    equality_tick(ax, A, B, 1)
    equality_tick(ax, A, D, 1)

    # Hai cung tròn nét đứt màu đỏ/hồng tâm B và D bán kính AB=2.8
    arcB = Arc(B, 5.6, 5.6, angle=0, theta1=60, theta2=150, color='#E11D48', lw=1.4, linestyle='--')
    arcD = Arc(D, 5.6, 5.6, angle=0, theta1=240, theta2=330, color='#E11D48', lw=1.4, linestyle='--')
    ax.add_patch(arcB)
    ax.add_patch(arcD)

    ax.text(A[0]-0.25, A[1]-0.2, '$A$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(B[0]+0.2, B[1]-0.2, '$B$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(D[0]-0.25, D[1]+0.15, '$D$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.2, C[1]+0.15, '$C$', fontsize=13, fontweight='bold', color='#0284C7')

    ax.text(2.6, -0.45, 'Hình 3.57', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_57_vi_du.png')

# ==========================================
# 16. HÌNH 3.58: BÀI TẬP 3.35 (SGK TRANG 73)
# ==========================================
def draw_hinh_sgk_3_58():
    fig, ax = setup_canvas(figsize=(6.5, 4.0), xlim=(-0.8, 7.5), ylim=(-0.8, 4.5))
    # Hình bình hành ABCD: A (trên trái), B (trên phải), C (dưới phải), D (dưới trái)
    A = np.array([2.0, 3.5]); B = np.array([6.5, 3.5])
    D = np.array([0.5, 0.8]); C = np.array([5.0, 0.8])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.0)

    # 4 tia phân giác cắt nhau tạo hình chữ nhật EFGH
    # E trên, F phải, G dưới, H trái
    E = np.array([3.7, 2.7])
    F = np.array([4.7, 2.2])
    G = np.array([4.2, 1.4])
    H = np.array([3.2, 1.9])

    # Kẻ các tia
    ax.plot([A[0], G[0]], [A[1], G[1]], 'k-', lw=1.2)
    ax.plot([B[0], H[0]], [B[1], H[1]], 'k-', lw=1.2)
    ax.plot([C[0], E[0]], [C[1], E[1]], 'k-', lw=1.2)
    ax.plot([D[0], F[0]], [D[1], F[1]], 'k-', lw=1.2)

    # Cung góc phân giác
    ax.add_patch(Arc(A, 0.6, 0.6, angle=0, theta1=240, theta2=300, color='black', lw=1.0))
    ax.add_patch(Arc(A, 0.75, 0.75, angle=0, theta1=300, theta2=360, color='black', lw=1.0))

    ax.add_patch(Arc(B, 0.6, 0.6, angle=0, theta1=180, theta2=215, color='black', lw=1.0))
    ax.add_patch(Arc(B, 0.75, 0.75, angle=0, theta1=215, theta2=250, color='black', lw=1.0))

    ax.add_patch(Arc(D, 0.6, 0.6, angle=0, theta1=0, theta2=35, color='black', lw=1.0))
    ax.add_patch(Arc(D, 0.75, 0.75, angle=0, theta1=35, theta2=70, color='black', lw=1.0))

    ax.add_patch(Arc(C, 0.6, 0.6, angle=0, theta1=65, theta2=125, color='black', lw=1.0))
    ax.add_patch(Arc(C, 0.75, 0.75, angle=0, theta1=125, theta2=185, color='black', lw=1.0))

    ax.text(A[0], A[1]+0.2, '$A$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(B[0]+0.15, B[1]+0.15, '$B$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.2, C[1]-0.25, '$C$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(D[0]-0.25, D[1]-0.15, '$D$', fontsize=13, fontweight='bold', color='#0284C7')

    ax.text(E[0]-0.1, E[1]+0.15, '$E$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(F[0]+0.15, F[1], '$F$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(G[0]+0.1, G[1]-0.2, '$G$', fontsize=11, fontweight='bold', color='#0284C7')
    ax.text(H[0]-0.25, H[1], '$H$', fontsize=11, fontweight='bold', color='#0284C7')

    ax.text(3.5, -0.45, 'Hình 3.58', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_58_bai_3_35.png')

# ==========================================
# 17. HÌNH 3.59: BÀI TẬP 3.42 (SGK TRANG 74)
# ==========================================
def draw_hinh_sgk_3_59():
    fig, ax = setup_canvas(figsize=(6.0, 3.8), xlim=(-0.8, 6.5), ylim=(-0.8, 4.2))
    # Tứ giác ABCD có AD = BC, AC = BD
    A = np.array([1.8, 3.2]); B = np.array([4.2, 3.2])
    D = np.array([0.5, 0.8]); C = np.array([5.5, 0.8])

    ax.plot([A[0], B[0], C[0], D[0], A[0]], [A[1], B[1], C[1], D[1], A[1]], 'k-', lw=2.0)
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k-', lw=1.4)
    ax.plot([B[0], D[0]], [B[1], D[1]], 'k-', lw=1.4)

    # AD = BC (1 vạch)
    equality_tick(ax, A, D, 1)
    equality_tick(ax, B, C, 1)

    # AC = BD (vạch gạch chéo chữ x)
    tick_cross(ax, A, C)
    tick_cross(ax, B, D)

    ax.text(A[0], A[1]+0.2, '$A$', fontsize=13, ha='center', fontweight='bold', color='#0284C7')
    ax.text(B[0], B[1]+0.2, '$B$', fontsize=13, ha='center', fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.2, C[1]-0.2, '$C$', fontsize=13, ha='left', fontweight='bold', color='#0284C7')
    ax.text(D[0]-0.2, D[1]-0.2, '$D$', fontsize=13, ha='right', fontweight='bold', color='#0284C7')

    ax.text(3.0, -0.45, 'Hình 3.59', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_59_bai_3_42.png')

# ==========================================
# 18. HÌNH 3.60: BÀI TẬP 3.44 (SGK TRANG 75)
# ==========================================
def draw_hinh_sgk_3_60():
    fig, ax = setup_canvas(figsize=(7.0, 4.2), xlim=(-0.8, 8.5), ylim=(-0.8, 4.8))
    # Tam giác ABC vuông tại A: A (dưới trái), B (dưới phải), C (trên)
    A = np.array([3.2, 0.8]); B = np.array([7.5, 0.8]); C = np.array([3.2, 3.8])
    M = (B + C) / 2.0 # (5.35, 2.3)
    P = np.array([A[0], M[1]]) # (3.2, 2.3)
    N = np.array([M[0], A[1]]) # (5.35, 0.8)
    Q = P + (P - M) # (1.05, 2.3)

    # Tam giác ABC
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', lw=2.0)
    right_angle(ax, A, [1, 0], [0, 1], size=0.25)

    # Đường vuông góc MP, MN và AM
    ax.plot([P[0], M[0]], [P[1], M[1]], 'k-', lw=1.4)
    ax.plot([N[0], M[0]], [N[1], M[1]], 'k-', lw=1.4)
    ax.plot([A[0], M[0]], [A[1], M[1]], 'k-', lw=1.4)

    right_angle(ax, P, [0, 1], [1, 0], size=0.2)
    right_angle(ax, N, [0, 1], [-1, 0], size=0.2)

    # Kéo dài MP lấy Q
    ax.plot([Q[0], P[0]], [Q[1], P[1]], 'k-', lw=1.4)
    ax.plot([Q[0], C[0]], [Q[1], C[1]], 'k-', lw=1.6)
    ax.plot([Q[0], A[0]], [Q[1], A[1]], 'k-', lw=1.6)

    equality_tick(ax, B, M, 1)
    equality_tick(ax, M, C, 1)
    equality_tick(ax, Q, P, 2)
    equality_tick(ax, P, M, 2)

    ax.text(A[0]-0.15, A[1]-0.25, '$A$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(B[0]+0.2, B[1]-0.15, '$B$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(C[0], C[1]+0.2, '$C$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(M[0]+0.15, M[1]+0.15, '$M$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(P[0]-0.25, P[1]-0.25, '$P$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(N[0], N[1]-0.25, '$N$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(Q[0]-0.25, Q[1], '$Q$', fontsize=13, fontweight='bold', color='#0284C7')

    ax.text(4.2, -0.45, 'Hình 3.60', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_60_bai_3_44.png')

# ==========================================
# 19. HÌNH 3.61: BÀI TẬP 3.45 (SGK TRANG 75)
# ==========================================
def draw_hinh_sgk_3_61():
    fig, ax = setup_canvas(figsize=(6.5, 4.5), xlim=(-0.8, 7.5), ylim=(-0.8, 5.0))
    # Tam giác cân ABC: A (trên), B (dưới trái), C (dưới phải)
    A = np.array([4.0, 4.2])
    B = np.array([2.5, 1.2])
    C = np.array([5.5, 1.2])

    # Kéo dài CB về phía B lấy M
    M = np.array([0.8, 1.2])

    ax.plot([M[0], C[0]], [M[1], C[1]], 'k-', lw=1.8)
    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', lw=1.8)
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k-', lw=1.8)

    # ME vuông góc AC tại E
    vAC = C - A; uAC = vAC / np.linalg.norm(vAC)
    projE = np.dot(M - A, uAC)
    E = A + projE * uAC
    ax.plot([M[0], E[0]], [M[1], E[1]], 'k-', lw=1.4)
    right_angle(ax, E, [M[0]-E[0], M[1]-E[1]], [A[0]-E[0], A[1]-E[1]], size=0.2)

    # BK vuông góc AC tại K
    projK = np.dot(B - A, uAC)
    K = A + projK * uAC
    ax.plot([B[0], K[0]], [B[1], K[1]], 'k-', lw=1.4)
    right_angle(ax, K, [B[0]-K[0], B[1]-K[1]], [C[0]-K[0], C[1]-K[1]], size=0.2)

    # MD vuông góc AB kéo dài tại D
    vAB = B - A; uAB = vAB / np.linalg.norm(vAB)
    projD = np.dot(M - A, uAB)
    D = A + projD * uAB
    ax.plot([B[0], D[0]], [B[1], D[1]], 'k--', lw=1.2)
    ax.plot([M[0], D[0]], [M[1], D[1]], 'k-', lw=1.4)
    right_angle(ax, D, [M[0]-D[0], M[1]-D[1]], [A[0]-D[0], A[1]-D[1]], size=0.2)

    # BN vuông góc ME tại N
    vME = E - M; uME = vME / np.linalg.norm(vME)
    projN = np.dot(B - M, uME)
    N = M + projN * uME
    ax.plot([B[0], N[0]], [B[1], N[1]], 'k-', lw=1.4)
    right_angle(ax, N, [B[0]-N[0], B[1]-N[1]], [E[0]-N[0], E[1]-N[1]], size=0.2)

    ax.text(A[0], A[1]+0.2, '$A$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(B[0]+0.15, B[1]-0.25, '$B$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(C[0]+0.2, C[1]-0.15, '$C$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(M[0]-0.25, M[1]+0.1, '$M$', fontsize=13, fontweight='bold', color='#0284C7')
    ax.text(E[0]+0.2, E[1]+0.15, '$E$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(K[0]+0.25, K[1], '$K$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(D[0]+0.15, D[1]-0.25, '$D$', fontsize=12, fontweight='bold', color='#0284C7')
    ax.text(N[0]-0.15, N[1]+0.15, '$N$', fontsize=12, fontweight='bold', color='#0284C7')

    ax.text(3.5, -0.45, 'Hình 3.61', fontsize=11, ha='center', color='#475569', style='italic')

    save_fig(fig, 'hinh_sgk_3_61_bai_3_45.png')

def main():
    print("=== BẮT ĐẦU VẼ LẠI 100% HÌNH HỌC SGK TOÁN 8 CHUẨN MỰC ===")
    draw_hinh_01()
    draw_hinh_sgk_1_3()
    draw_hinh_hdtn_lai_kep()
    draw_hinh_sgk_3_46()
    draw_hinh_sgk_3_47()
    draw_hinh_sgk_3_48()
    draw_hinh_sgk_3_49()
    draw_hinh_sgk_3_50()
    draw_hinh_sgk_3_51()
    draw_hinh_sgk_3_52()
    draw_hinh_sgk_3_53()
    draw_hinh_sgk_3_54()
    draw_hinh_sgk_3_55()
    draw_hinh_sgk_3_56()
    draw_hinh_sgk_3_57()
    draw_hinh_sgk_3_58()
    draw_hinh_sgk_3_59()
    draw_hinh_sgk_3_60()
    draw_hinh_sgk_3_61()
    print("=== HOÀN THÀNH VẼ LẠI TOÀN BỘ 19 HÌNH HỌC CHUẨN XÁC! ===")

if __name__ == '__main__':
    main()
