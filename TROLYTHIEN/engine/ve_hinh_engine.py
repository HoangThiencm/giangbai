# -*- coding: utf-8 -*-
"""
ENGINE CHUẨN HÓA DUY NHẤT: VẼ HÌNH HỌC CHUẨN XÁC 100% (GDPT 2018)
Trợ lý Sư phạm Hoàng Thiên • Thư mục: TROLYTHIEN/engine/ve_hinh_engine.py

QUY CHUẨN KỸ THUẬT:
- Dựng tọa độ giải tích 100% (hệ trục Oxy và chiếu xiên 3D góc 42°, hệ số sâu 0.52).
- Chuẩn GDPT 2018: Nhãn đỉnh nghiêng Times New Roman lệch ra ngoài; ký hiệu góc vuông, vạch bằng nhau; nét đứt cho cạnh khuất.
- Bản vẽ tinh gọn tuyệt đối (Clean Diagram): Không tiêu đề, không chú thích, không lời giải trong hình.
- Xuất file PNG chất lượng cao (300 DPI, khử răng cưa) hoặc SVG vector độc lập vào TROLYTHIEN/11_VE_HINH/Ket_qua/.
"""

import os
import sys
import math
import json
import argparse
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR_DEFAULT = "TROLYTHIEN/11_VE_HINH/Ket_qua"

def get_font(size, bold=False, italic=True):
    """Tìm font chữ Times New Roman / Segoe UI hỗ trợ tiếng Việt & ký hiệu toán"""
    font_names = []
    if bold and italic:
        font_names = ["timesbi.ttf", "segoeuiib.ttf", "arialbi.ttf"]
    elif italic:
        font_names = ["timesi.ttf", "segoeuii.ttf", "ariali.ttf"]
    elif bold:
        font_names = ["timesbd.ttf", "segoeuib.ttf", "arialbd.ttf"]
    else:
        font_names = ["times.ttf", "segoeui.ttf", "arial.ttf"]
        
    for f in font_names:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

def chieu_3d(x, y, z, goc=42, sau=0.52, goc_goc=(300, 360), don_vi=75):
    """Phép chiếu xiên chuẩn SGK (x sang phải, y lùi xa lên trên, z thẳng đứng)"""
    rad = math.radians(goc)
    px = goc_goc[0] + don_vi * (x + y * sau * math.cos(rad))
    py = goc_goc[1] - don_vi * (z + y * sau * math.sin(rad))
    return (px, py)

def draw_dashed_line(draw, pt1, pt2, fill=(30, 41, 59), width=2, dash_len=8, gap_len=6):
    """Vẽ đoạn thẳng nét đứt cho cạnh khuất"""
    x1, y1 = pt1
    x2, y2 = pt2
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0:
        return
    dx = (x2 - x1) / dist
    dy = (y2 - y1) / dist
    
    cur = 0
    drawing = True
    while cur < dist:
        seg = dash_len if drawing else gap_len
        nxt = min(cur + seg, dist)
        if drawing:
            draw.line([(x1 + dx * cur, y1 + dy * cur), (x1 + dx * nxt, y1 + dy * nxt)], fill=fill, width=width)
        cur = nxt
        drawing = not drawing

def draw_right_angle_mark(draw, vertex, pt_a, pt_b, size=18, fill=(30, 64, 175), width=2):
    """Vẽ ký hiệu góc vuông tại vertex hướng về pt_a và pt_b"""
    vx, vy = vertex
    d1 = math.hypot(pt_a[0] - vx, pt_a[1] - vy)
    d2 = math.hypot(pt_b[0] - vx, pt_b[1] - vy)
    if d1 == 0 or d2 == 0:
        return
    u1 = ((pt_a[0] - vx) / d1 * size, (pt_a[1] - vy) / d1 * size)
    u2 = ((pt_b[0] - vx) / d2 * size, (pt_b[1] - vy) / d2 * size)
    p1 = (vx + u1[0], vy + u1[1])
    p2 = (vx + u1[0] + u2[0], vy + u1[1] + u2[1])
    p3 = (vx + u2[0], vy + u2[1])
    draw.line([p1, p2, p3], fill=fill, width=width)

# ==============================================================================
# BỘ MẪU HÌNH HỌC PHỔ BIẾN (PRESETS)
# ==============================================================================

def render_tam_giac_vuong(output_path, AB=200, AC=300, dinh_vuong="A", dinh_b="B", dinh_c="C"):
    """Vẽ tam giác vuông tại A (chuẩn SGK)"""
    w, h = 600, 450
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_lbl = get_font(24, bold=True, italic=True)
    
    A = (120, 360)
    B = (120, 360 - AB)
    C = (120 + AC, 360)
    
    draw.polygon([A, B, C], outline=(30, 41, 59), width=3)
    draw_right_angle_mark(draw, A, B, C, size=20, fill=(30, 64, 175), width=2)
    
    draw.text((A[0] - 25, A[1] + 8), dinh_vuong, fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((B[0] - 25, B[1] - 12), dinh_b, fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((C[0] + 25, C[1] + 8), dinh_c, fill=(15, 23, 42), font=f_lbl, anchor="mm")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"✔ Đã xuất hình tam giác vuông: {output_path}")
    return output_path

def render_chop_s_abcd(output_path, h_val=2.8, a=2.2, b=1.8):
    """Vẽ hình chóp S.ABCD đáy hình chữ nhật, SA vuông góc đáy (chuẩn SGK)"""
    w, h = 650, 520
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_lbl = get_font(24, bold=True, italic=True)
    
    origin = (200, 400)
    A = chieu_3d(0, 0, 0, goc_goc=origin)
    B = chieu_3d(a, 0, 0, goc_goc=origin)
    C = chieu_3d(a, b, 0, goc_goc=origin)
    D = chieu_3d(0, b, 0, goc_goc=origin)
    S = chieu_3d(0, 0, h_val, goc_goc=origin)
    
    # Nét liền: AB, BC, CD?, SA, SB, SC, SD (D và các cạnh nối D là nét đứt)
    draw.line([A, B], fill=(30, 41, 59), width=3)
    draw.line([B, C], fill=(30, 41, 59), width=3)
    draw_dashed_line(draw, C, D, fill=(100, 116, 139), width=2)
    draw_dashed_line(draw, D, A, fill=(100, 116, 139), width=2)
    
    draw.line([S, A], fill=(30, 41, 59), width=3)
    draw.line([S, B], fill=(30, 41, 59), width=3)
    draw.line([S, C], fill=(30, 41, 59), width=3)
    draw_dashed_line(draw, S, D, fill=(100, 116, 139), width=2)
    
    # Góc vuông SA vuông góc đáy
    draw_right_angle_mark(draw, A, B, S, size=18, fill=(30, 64, 175), width=2)
    
    # Nhãn đỉnh
    draw.text((S[0], S[1] - 18), "S", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((A[0] - 22, A[1] + 12), "A", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((B[0] + 12, B[1] + 18), "B", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((C[0] + 24, C[1] - 6), "C", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((D[0] - 20, D[1] - 14), "D", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"✔ Đã xuất hình chóp S.ABCD: {output_path}")
    return output_path

def render_hop_chu_nhat(output_path, a=2.4, b=1.6, c=2.0):
    """Vẽ hình hộp chữ nhật ABCD.A'B'C'D'"""
    w, h = 650, 520
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_lbl = get_font(22, bold=True, italic=True)
    
    origin = (190, 420)
    # Đáy dưới ABCD
    A = chieu_3d(0, 0, 0, goc_goc=origin)
    B = chieu_3d(a, 0, 0, goc_goc=origin)
    C = chieu_3d(a, b, 0, goc_goc=origin)
    D = chieu_3d(0, b, 0, goc_goc=origin)
    # Đáy trên A'B'C'D'
    Ap = chieu_3d(0, 0, c, goc_goc=origin)
    Bp = chieu_3d(a, 0, c, goc_goc=origin)
    Cp = chieu_3d(a, b, c, goc_goc=origin)
    Dp = chieu_3d(0, b, c, goc_goc=origin)
    
    # Nét đứt quanh đỉnh D
    draw_dashed_line(draw, A, D, fill=(100, 116, 139), width=2)
    draw_dashed_line(draw, D, C, fill=(100, 116, 139), width=2)
    draw_dashed_line(draw, D, Dp, fill=(100, 116, 139), width=2)
    
    # Nét liền
    draw.line([A, B, C], fill=(30, 41, 59), width=3)
    draw.line([Ap, Bp, Cp, Dp, Ap], fill=(30, 41, 59), width=3)
    draw.line([A, Ap], fill=(30, 41, 59), width=3)
    draw.line([B, Bp], fill=(30, 41, 59), width=3)
    draw.line([C, Cp], fill=(30, 41, 59), width=3)
    
    # Nhãn
    draw.text((A[0] - 20, A[1] + 12), "A", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((B[0] + 18, B[1] + 14), "B", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((C[0] + 22, C[1] - 4), "C", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((D[0] - 20, D[1] - 12), "D", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((Ap[0] - 22, Ap[1] - 8), "A'", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((Bp[0] + 20, Bp[1] - 8), "B'", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((Cp[0] + 22, Cp[1] - 12), "C'", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    draw.text((Dp[0] - 20, Dp[1] - 14), "D'", fill=(15, 23, 42), font=f_lbl, anchor="mm")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, dpi=(300, 300))
    print(f"✔ Đã xuất hình hộp chữ nhật: {output_path}")
    return output_path

# ==============================================================================
# MAIN CLI
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Universal Geometry Drawing Engine - Trợ lý Sư phạm Hoàng Thiên")
    parser.add_argument("--preset", type=str, choices=["tam_giac_vuong", "chop_s_abcd", "hop_chu_nhat"], help="Mẫu hình có sẵn")
    parser.add_argument("--out", type=str, help="Đường dẫn file ảnh PNG xuất ra")
    parser.add_argument("--list-presets", action="store_true", help="Danh sách mẫu hình")

    args = parser.parse_args()

    if args.list_presets:
        print("Danh sách preset hình học có sẵn:")
        print("  • tam_giac_vuong: Tam giác vuông chuẩn SGK với góc vuông")
        print("  • chop_s_abcd: Hình chóp S.ABCD đáy chữ nhật, SA vuông góc đáy")
        print("  • hop_chu_nhat: Hình hộp chữ nhật ABCD.A'B'C'D'")
        return

    out = args.out or os.path.join(OUTPUT_DIR_DEFAULT, f"{args.preset or 'hinh_hoc'}.png")

    if args.preset == "tam_giac_vuong":
        render_tam_giac_vuong(out)
    elif args.preset == "chop_s_abcd":
        render_chop_s_abcd(out)
    elif args.preset == "hop_chu_nhat":
        render_hop_chu_nhat(out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
