# -*- coding: utf-8 -*-
"""
VẼ 10 HÌNH HỌC CHUẨN XÁC 100% ĐỀ CƯƠNG TOÁN 7 GIỮA KỲ I (BẢN TINH CHỈNH HOÀN HẢO)
Trợ lý Sư phạm Hoàng Thiên • Trường THCS Trần Phú
Độ phân giải cao (3x supersampling khử răng cưa), phông chữ Times New Roman nghiêng chuẩn SGK.
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = os.path.abspath("TROLYTHIEN/4_DUYET_DE/Ket_qua/hinh_ve")
os.makedirs(OUT_DIR, exist_ok=True)
SCALE = 3

def get_fonts():
    return {
        'reg': ImageFont.truetype('times.ttf', 16 * SCALE),
        'bold': ImageFont.truetype('timesbd.ttf', 16 * SCALE),
        'italic': ImageFont.truetype('timesi.ttf', 18 * SCALE),
        'bold_italic': ImageFont.truetype('timesbi.ttf', 18 * SCALE),
        'small': ImageFont.truetype('times.ttf', 14 * SCALE),
        'small_it': ImageFont.truetype('timesi.ttf', 15 * SCALE),
        'deg': ImageFont.truetype('times.ttf', 15 * SCALE),
        'deg_bold': ImageFont.truetype('timesbd.ttf', 15 * SCALE),
    }

def draw_point(draw, pt, r=3*SCALE, fill=(30, 41, 59)):
    draw.ellipse([pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r], fill=fill)

def draw_right_angle(draw, V, A, B, size=14*SCALE, color=(30, 41, 59), width=2*SCALE):
    vx, vy = V
    d1 = math.hypot(A[0]-vx, A[1]-vy)
    d2 = math.hypot(B[0]-vx, B[1]-vy)
    if d1 == 0 or d2 == 0: return
    u1 = ((A[0]-vx)/d1 * size, (A[1]-vy)/d1 * size)
    u2 = ((B[0]-vx)/d2 * size, (B[1]-vy)/d2 * size)
    p1 = (vx + u1[0], vy + u1[1])
    p2 = (vx + u1[0] + u2[0], vy + u1[1] + u2[1])
    p3 = (vx + u2[0], vy + u2[1])
    draw.line([p1, p2, p3], fill=color, width=width)

def draw_angle_arc(draw, V, start_deg, end_deg, radius=32*SCALE, color=(37, 99, 235), width=2*SCALE):
    bbox = [V[0]-radius, V[1]-radius, V[0]+radius, V[1]+radius]
    draw.arc(bbox, start=start_deg, end=end_deg, fill=color, width=width)

def draw_tick_mark(draw, p1, p2, count=1, size=7*SCALE, color=(220, 38, 38), width=2*SCALE):
    mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    L = math.hypot(dx, dy)
    if L == 0: return
    nx, ny = -dy/L, dx/L
    spacing = 4 * SCALE
    if count == 1:
        draw.line([(mx - nx*size, my - ny*size), (mx + nx*size, my + ny*size)], fill=color, width=width)
    elif count == 2:
        for offset in [-spacing, spacing]:
            cx = mx + (dx/L)*offset
            cy = my + (dy/L)*offset
            draw.line([(cx - nx*size, cy - ny*size), (cx + nx*size, cy + ny*size)], fill=color, width=width)

def save_resampled(img, filename):
    w, h = img.size
    out_w, out_h = w // SCALE, h // SCALE
    res = img.resize((out_w, out_h), Image.Resampling.LANCZOS)
    out_path = os.path.join(OUT_DIR, filename)
    res.save(out_path, dpi=(300, 300))
    print(f"Saved: {out_path} ({out_w}x{out_h})")
    return out_path

# ==============================================================================
# HÌNH 1: GÓC KỀ BÙ (xOz và zOy = 50 độ)
# ==============================================================================
def render_hinh_1():
    w, h = 550 * SCALE, 260 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    O = (275 * SCALE, 190 * SCALE)
    X = (60 * SCALE, 190 * SCALE)
    Y = (490 * SCALE, 190 * SCALE)
    
    rad50 = math.radians(50)
    L_z = 170 * SCALE
    Z = (O[0] + L_z * math.cos(rad50), O[1] - L_z * math.sin(rad50))
    
    draw.line([X, Y], fill=(30, 41, 59), width=2*SCALE)
    draw.line([O, Z], fill=(30, 41, 59), width=2*SCALE)
    draw_point(draw, O)
    
    draw_angle_arc(draw, O, 310, 360, radius=42*SCALE, color=(37, 99, 235), width=2*SCALE)
    draw_angle_arc(draw, O, 180, 310, radius=32*SCALE, color=(220, 38, 38), width=2*SCALE)
    
    draw.text((O[0] - 8*SCALE, O[1] + 8*SCALE), "O", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((X[0] - 25*SCALE, X[1] - 12*SCALE), "x", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((Y[0] + 12*SCALE, Y[1] - 12*SCALE), "y", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((Z[0] + 8*SCALE, Z[1] - 20*SCALE), "z", fill=(0, 0, 0), font=fonts['italic'])
    
    draw.text((O[0] + 50*SCALE, O[1] - 38*SCALE), "50°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((O[0] - 45*SCALE, O[1] - 50*SCALE), "?", fill=(220, 38, 38), font=fonts['deg_bold'])
    
    return save_resampled(img, "Hinh_1_Goc_Ke_Bu.png")

# ==============================================================================
# HÌNH 2: TIA PHÂN GIÁC (Oz là phân giác xOy, zOy = 32 độ)
# ==============================================================================
def render_hinh_2():
    w, h = 550 * SCALE, 280 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    O = (90 * SCALE, 220 * SCALE)
    L_y = 360 * SCALE
    L_z = 300 * SCALE
    L_x = 180 * SCALE
    
    Y = (O[0] + L_y, O[1])
    rad32 = math.radians(32)
    Z = (O[0] + L_z * math.cos(rad32), O[1] - L_z * math.sin(rad32))
    rad64 = math.radians(64)
    X = (O[0] + L_x * math.cos(rad64), O[1] - L_x * math.sin(rad64))
    
    draw.line([O, Y], fill=(30, 41, 59), width=2*SCALE)
    draw.line([O, Z], fill=(30, 41, 59), width=2*SCALE)
    draw.line([O, X], fill=(30, 41, 59), width=2*SCALE)
    draw_point(draw, O)
    
    draw_angle_arc(draw, O, 328, 360, radius=55*SCALE, color=(37, 99, 235), width=2*SCALE)
    draw_angle_arc(draw, O, 296, 328, radius=55*SCALE, color=(37, 99, 235), width=2*SCALE)
    
    a1_mid = math.radians(16)
    m1 = (O[0] + 55*SCALE * math.cos(a1_mid), O[1] - 55*SCALE * math.sin(a1_mid))
    draw.line([(m1[0] - 3*SCALE, m1[1] - 3*SCALE), (m1[0] + 3*SCALE, m1[1] + 3*SCALE)], fill=(37, 99, 235), width=2*SCALE)
    
    a2_mid = math.radians(48)
    m2 = (O[0] + 55*SCALE * math.cos(a2_mid), O[1] - 55*SCALE * math.sin(a2_mid))
    draw.line([(m2[0] - 4*SCALE, m2[1] + 2*SCALE), (m2[0] + 4*SCALE, m2[1] - 2*SCALE)], fill=(37, 99, 235), width=2*SCALE)
    
    draw.text((O[0] - 20*SCALE, O[1] + 5*SCALE), "O", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((Y[0] + 10*SCALE, Y[1] - 12*SCALE), "y", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((Z[0] + 10*SCALE, Z[1] - 12*SCALE), "z", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((X[0] + 6*SCALE, X[1] - 16*SCALE), "x", fill=(0, 0, 0), font=fonts['italic'])
    
    draw.text((O[0] + 75*SCALE, O[1] - 25*SCALE), "32°", fill=(37, 99, 235), font=fonts['deg_bold'])
    
    return save_resampled(img, "Hinh_2_Tia_Phan_Giac.png")

# ==============================================================================
# HÌNH 3: CHỨNG MINH SONG SONG - HÌNH 1 (Hai góc so le trong 71 độ)
# ==============================================================================
def render_hinh_3():
    w, h = 500 * SCALE, 270 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    y_a = 75 * SCALE
    y_b = 185 * SCALE
    
    B = (290 * SCALE, y_a)
    dx = (y_b - y_a) / math.tan(math.radians(71))
    C = (B[0] - dx, y_b)
    
    draw.line([(50*SCALE, y_a), (450*SCALE, y_a)], fill=(30, 41, 59), width=2*SCALE)
    draw.line([(50*SCALE, y_b), (450*SCALE, y_b)], fill=(30, 41, 59), width=2*SCALE)
    
    trans_dx = (C[0] - B[0])
    trans_dy = (C[1] - B[1])
    ext = 0.35
    T1 = (B[0] - trans_dx * ext, B[1] - trans_dy * ext)
    T2 = (C[0] + trans_dx * ext, C[1] + trans_dy * ext)
    draw.line([T1, T2], fill=(30, 41, 59), width=2*SCALE)
    
    draw_point(draw, B)
    draw_point(draw, C)
    
    # Arc at B: strictly between ray Ba (left: 180) and transversal BC (109 deg)
    draw_angle_arc(draw, B, 109, 180, radius=32*SCALE, color=(37, 99, 235), width=2*SCALE)
    # Arc at C: strictly between ray Cy (right: 360) and transversal CB (289 deg)
    draw_angle_arc(draw, C, 289, 360, radius=32*SCALE, color=(37, 99, 235), width=2*SCALE)
    
    draw.text((60*SCALE, y_a - 26*SCALE), "a", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((435*SCALE, y_a - 26*SCALE), "x", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((60*SCALE, y_b - 26*SCALE), "b", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((435*SCALE, y_b - 26*SCALE), "y", fill=(0, 0, 0), font=fonts['italic'])
    
    draw.text((B[0] - 5*SCALE, B[1] - 28*SCALE), "B", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((C[0] - 18*SCALE, C[1] + 8*SCALE), "C", fill=(0, 0, 0), font=fonts['bold_italic'])
    
    draw.text((B[0] - 45*SCALE, B[1] + 8*SCALE), "71°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((C[0] + 16*SCALE, C[1] - 25*SCALE), "71°", fill=(37, 99, 235), font=fonts['deg_bold'])
    
    draw.text((220*SCALE, 235*SCALE), "Hình 1", fill=(0, 0, 0), font=fonts['reg'])
    
    return save_resampled(img, "Hinh_3_Song_Song_71_Do.png")

# ==============================================================================
# HÌNH 4: CHỨNG MINH SONG SONG - HÌNH 2 (Góc 130 độ)
# ==============================================================================
def render_hinh_4():
    w, h = 500 * SCALE, 270 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    y_a = 75 * SCALE
    y_b = 185 * SCALE
    
    H = (220 * SCALE, y_a)
    dx = (y_b - y_a) / math.tan(math.radians(50))
    P = (H[0] + dx, y_b)
    
    draw.line([(50*SCALE, y_a), (450*SCALE, y_a)], fill=(30, 41, 59), width=2*SCALE)
    draw.line([(50*SCALE, y_b), (450*SCALE, y_b)], fill=(30, 41, 59), width=2*SCALE)
    
    trans_dx = P[0] - H[0]
    trans_dy = P[1] - H[1]
    ext = 0.35
    T1 = (H[0] - trans_dx * ext, H[1] - trans_dy * ext)
    T2 = (P[0] + trans_dx * ext, P[1] + trans_dy * ext)
    draw.line([T1, T2], fill=(30, 41, 59), width=2*SCALE)
    
    draw_point(draw, H)
    draw_point(draw, P)
    
    draw_angle_arc(draw, H, 230, 360, radius=32*SCALE, color=(37, 99, 235), width=2*SCALE)
    draw_angle_arc(draw, P, 50, 180, radius=32*SCALE, color=(37, 99, 235), width=2*SCALE)
    
    draw.text((60*SCALE, y_a - 26*SCALE), "a", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((435*SCALE, y_a - 26*SCALE), "x", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((60*SCALE, y_b - 26*SCALE), "b", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((435*SCALE, y_b - 26*SCALE), "y", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((T1[0] + 8*SCALE, T1[1] - 15*SCALE), "c", fill=(0, 0, 0), font=fonts['italic'])
    
    draw.text((H[0] - 22*SCALE, H[1] + 8*SCALE), "H", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((P[0] + 8*SCALE, P[1] - 28*SCALE), "P", fill=(0, 0, 0), font=fonts['bold_italic'])
    
    draw.text((H[0] + 32*SCALE, H[1] - 32*SCALE), "130°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((P[0] - 65*SCALE, P[1] + 12*SCALE), "130°", fill=(37, 99, 235), font=fonts['deg_bold'])
    
    draw.text((220*SCALE, 235*SCALE), "Hình 2", fill=(0, 0, 0), font=fonts['reg'])
    
    return save_resampled(img, "Hinh_4_Song_Song_130_Do.png")

# ==============================================================================
# HÌNH 5: TÍNH GÓC VỚI a // b (Góc 100 độ và ?)
# ==============================================================================
def render_hinh_5():
    w, h = 480 * SCALE, 280 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    y_a = 75 * SCALE
    y_b = 185 * SCALE
    
    J = (230 * SCALE, y_a)
    dx = (y_b - y_a) / math.tan(math.radians(80))
    K = (J[0] - dx, y_b)
    
    draw.line([(50*SCALE, y_a), (430*SCALE, y_a)], fill=(30, 41, 59), width=2*SCALE)
    draw.line([(50*SCALE, y_b), (430*SCALE, y_b)], fill=(30, 41, 59), width=2*SCALE)
    
    trans_dx = K[0] - J[0]
    trans_dy = K[1] - J[1]
    ext = 0.35
    H_pt = (J[0] - trans_dx * ext, J[1] - trans_dy * ext)
    I_pt = (K[0] + trans_dx * ext, K[1] + trans_dy * ext)
    draw.line([H_pt, I_pt], fill=(30, 41, 59), width=2*SCALE)
    
    draw_point(draw, J)
    draw_point(draw, K)
    
    # Arc at J: 100 deg obtuse angle
    draw_angle_arc(draw, J, 180, 280, radius=32*SCALE, color=(37, 99, 235), width=2*SCALE)
    # Arc at K: question mark at corresponding or interior angle
    draw_angle_arc(draw, K, 180, 280, radius=32*SCALE, color=(220, 38, 38), width=2*SCALE)
    
    draw.text((60*SCALE, y_a - 26*SCALE), "a", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((60*SCALE, y_b - 26*SCALE), "b", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((H_pt[0] - 10*SCALE, H_pt[1] - 22*SCALE), "H", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((I_pt[0] - 18*SCALE, I_pt[1] + 2*SCALE), "I", fill=(0, 0, 0), font=fonts['bold_italic'])
    
    draw.text((J[0] + 10*SCALE, J[1] + 6*SCALE), "J", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((K[0] + 10*SCALE, K[1] + 6*SCALE), "K", fill=(0, 0, 0), font=fonts['bold_italic'])
    
    draw.text((J[0] - 55*SCALE, J[1] - 32*SCALE), "100°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((K[0] - 40*SCALE, K[1] - 30*SCALE), "?", fill=(220, 38, 38), font=fonts['deg_bold'])
    
    draw.text((210*SCALE, 245*SCALE), "Hình 1", fill=(0, 0, 0), font=fonts['reg'])
    
    return save_resampled(img, "Hinh_5_Tinh_Goc_Song_Song_100_Do.png")

# ==============================================================================
# HÌNH 6: TỨ GIÁC VUÔNG ABCD (D = C = 90 độ, B = 135 độ, tìm x = DAB)
# ==============================================================================
def render_hinh_6():
    w, h = 480 * SCALE, 260 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    D = (110 * SCALE, 70 * SCALE)
    C = (110 * SCALE, 190 * SCALE)
    dy = C[1] - D[1]
    
    A = (D[0] + 240 * SCALE, D[1])
    B = (A[0] - dy, C[1])
    
    draw.line([D, A], fill=(30, 41, 59), width=2*SCALE)
    draw.line([A, B], fill=(30, 41, 59), width=2*SCALE)
    draw.line([B, C], fill=(30, 41, 59), width=2*SCALE)
    draw.line([C, D], fill=(30, 41, 59), width=2*SCALE)
    
    draw_point(draw, A)
    draw_point(draw, B)
    draw_point(draw, C)
    draw_point(draw, D)
    
    draw_right_angle(draw, D, A, C, size=14*SCALE)
    draw_right_angle(draw, C, B, D, size=14*SCALE)
    
    draw_angle_arc(draw, B, 180, 315, radius=30*SCALE, color=(37, 99, 235), width=2*SCALE)
    draw_angle_arc(draw, A, 135, 180, radius=35*SCALE, color=(220, 38, 38), width=2*SCALE)
    
    draw.text((D[0] - 25*SCALE, D[1] - 15*SCALE), "D", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((C[0] - 25*SCALE, C[1] - 5*SCALE), "C", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((A[0] + 8*SCALE, A[1] - 15*SCALE), "A", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((B[0] - 5*SCALE, B[1] + 8*SCALE), "B", fill=(0, 0, 0), font=fonts['bold_italic'])
    
    draw.text((B[0] - 45*SCALE, B[1] - 28*SCALE), "135°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((A[0] - 50*SCALE, A[1] + 8*SCALE), "x", fill=(220, 38, 38), font=fonts['deg_bold'])
    
    draw.text((210*SCALE, 225*SCALE), "Hình 1", fill=(0, 0, 0), font=fonts['reg'])
    
    return save_resampled(img, "Hinh_6_Tu_Giac_Vuong_135_Do.png")

# ==============================================================================
# HÌNH 7: TAM GIÁC ABC CÓ EF // BC (Góc 72 độ, 49 độ, tìm x = AEF)
# ==============================================================================
def render_hinh_7():
    w, h = 500 * SCALE, 260 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    A = (190 * SCALE, 50 * SCALE)
    B = (80 * SCALE, 200 * SCALE)
    C = (440 * SCALE, 200 * SCALE)
    
    t = 0.55
    E = (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)
    F = (A[0] + (C[0] - A[0]) * t, A[1] + (C[1] - A[1]) * t)
    
    draw.line([A, B], fill=(30, 41, 59), width=2*SCALE)
    draw.line([B, C], fill=(30, 41, 59), width=2*SCALE)
    draw.line([C, A], fill=(30, 41, 59), width=2*SCALE)
    draw.line([E, F], fill=(30, 41, 59), width=2*SCALE)
    
    # Extend EF slightly past F to show corresponding angle clearly
    F_ext = (F[0] + 35*SCALE, F[1])
    draw.line([F, F_ext], fill=(30, 41, 59), width=2*SCALE)
    
    draw_point(draw, A)
    draw_point(draw, B)
    draw_point(draw, C)
    draw_point(draw, E)
    draw_point(draw, F)
    
    # At B: 72 deg
    draw_angle_arc(draw, B, 305, 360, radius=28*SCALE, color=(37, 99, 235), width=2*SCALE)
    
    # At C: 49 deg
    draw_angle_arc(draw, C, 180, 215, radius=35*SCALE, color=(37, 99, 235), width=2*SCALE)
    
    # At F: corresponding angle 49 deg between F_ext (0 deg) and FC (35 deg down-right)
    draw_angle_arc(draw, F, 0, 35, radius=28*SCALE, color=(37, 99, 235), width=2*SCALE)
    
    # At E: angle x (between EF: 0 deg and EB: 55 deg down-left)
    draw_angle_arc(draw, E, 305, 360, radius=28*SCALE, color=(220, 38, 38), width=2*SCALE)
    
    draw.text((A[0] - 8*SCALE, A[1] - 25*SCALE), "A", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((B[0] - 22*SCALE, B[1] - 5*SCALE), "B", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((C[0] + 10*SCALE, C[1] - 5*SCALE), "C", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((E[0] - 25*SCALE, E[1] - 12*SCALE), "E", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((F[0] + 8*SCALE, F[1] - 22*SCALE), "F", fill=(0, 0, 0), font=fonts['bold_italic'])
    
    draw.text((B[0] + 32*SCALE, B[1] - 22*SCALE), "72°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((C[0] - 55*SCALE, C[1] - 18*SCALE), "49°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((F[0] + 32*SCALE, F[1] + 8*SCALE), "49°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((E[0] + 32*SCALE, E[1] - 18*SCALE), "x", fill=(220, 38, 38), font=fonts['deg_bold'])
    
    draw.text((220*SCALE, 225*SCALE), "Hình 2", fill=(0, 0, 0), font=fonts['reg'])
    
    return save_resampled(img, "Hinh_7_Tam_Giac_Dong_Vi_72_Do.png")

# ==============================================================================
# HÌNH 8: HÌNH TỔNG HỢP BÀI 9 (m vuông góc a, cát tuyến EF, tia phân giác Et, Fk cắt tại O)
# ==============================================================================
def render_hinh_8():
    w, h = 560 * SCALE, 300 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    y_a = 75 * SCALE
    y_b = 205 * SCALE
    x_m = 120 * SCALE
    
    H = (x_m, y_a)
    G = (x_m, y_b)
    
    # Transversal EF: angle aEF = 100 deg
    # E is on line a, F is on line b
    E = (340 * SCALE, y_a)
    # dx for 80 deg slope: (y_b - y_a) / tan(80) = 130 / 5.67 = 23
    # Transversal goes down-left from E to F:
    dx = (y_b - y_a) / math.tan(math.radians(80))
    F = (E[0] - dx, y_b) # F is to the left of E
    
    # Draw horizontal lines a and b
    draw.line([(70*SCALE, y_a), (510*SCALE, y_a)], fill=(30, 41, 59), width=2*SCALE)
    draw.line([(70*SCALE, y_b), (510*SCALE, y_b)], fill=(30, 41, 59), width=2*SCALE)
    # Line m vertical
    draw.line([(x_m, 35*SCALE), (x_m, 245*SCALE)], fill=(30, 41, 59), width=2*SCALE)
    
    # Transversal line extending beyond E and F
    trans_dx = F[0] - E[0]
    trans_dy = F[1] - E[1]
    ext = 0.25
    T1 = (E[0] - trans_dx * ext, E[1] - trans_dy * ext)
    T2 = (F[0] + trans_dx * ext, F[1] + trans_dy * ext)
    draw.line([T1, T2], fill=(30, 41, 59), width=2*SCALE)
    
    draw_point(draw, H)
    draw_point(draw, G)
    draw_point(draw, E)
    draw_point(draw, F)
    
    # Right angle at H
    draw_right_angle(draw, H, (x_m + 30*SCALE, y_a), (x_m, 35*SCALE), size=12*SCALE)
    
    # Arc at E: angle aEF = 100 deg (between ray Ea right: 0 deg and EF down-left: 100 deg)
    draw_angle_arc(draw, E, 0, 100, radius=32*SCALE, color=(37, 99, 235), width=2*SCALE)
    
    # Arc at F: angle EFG = 100 deg (between ray FG left: 180 deg and FE up-right: 280 deg)
    draw_angle_arc(draw, F, 180, 280, radius=32*SCALE, color=(37, 99, 235), width=2*SCALE)
    
    # Angle bisector Et of angle HEF (angle HEF = 80 deg, bisector is 40 deg from HE left)
    # Ray Et direction: 180 - 40 = 140 deg (down-left)
    rad_et = math.radians(140)
    L_et = 140 * SCALE
    Et_end = (E[0] - L_et * math.cos(math.radians(40)), E[1] + L_et * math.sin(math.radians(40)))
    
    # Ray Fk inside GFE: GFk = 40 deg (from FG left: 180, up by 40 deg => 180 - 40 = 140 deg up-left)
    rad_fk = math.radians(40)
    L_fk = 140 * SCALE
    Fk_end = (F[0] - L_fk * math.cos(rad_fk), F[1] - L_fk * math.sin(rad_fk))
    
    # Intersection O of Et and Fk:
    # Et: E + t*(-cos40, sin40)
    # Fk: F + s*(-cos40, -sin40)
    # Solve for O:
    # E_y + t*sin40 = F_y - s*sin40 => (t + s)*sin40 = F_y - E_y = 130*SCALE
    # Since slope magnitudes are symmetric (40 deg), intersection has:
    # O_y = (E_y + F_y) / 2 = (75 + 205)/2 * SCALE = 140 * SCALE!
    # t = (140 - 75) / sin40 = 65 / 0.6428 = 101.1 * SCALE
    # O_x = E_x - t * cos40 = 340*SCALE - 101.1*SCALE * 0.766 = 340 - 77.4 = 262.6 * SCALE
    O_pt = (E[0] - (65 * SCALE / math.sin(math.radians(40))) * math.cos(math.radians(40)), (y_a + y_b) / 2)
    
    # Draw Et through O
    draw.line([E, (O_pt[0] - 25*SCALE, O_pt[1] + 25*SCALE*math.tan(math.radians(40)))], fill=(16, 185, 129), width=2*SCALE)
    # Draw Fk through O
    draw.line([F, (O_pt[0] - 25*SCALE, O_pt[1] - 25*SCALE*math.tan(math.radians(40)))], fill=(217, 119, 6), width=2*SCALE)
    
    draw_point(draw, O_pt, r=3*SCALE, fill=(220, 38, 38))
    
    # Labels
    draw.text((x_m - 26*SCALE, 30*SCALE), "m", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((495*SCALE, y_a - 24*SCALE), "a", fill=(0, 0, 0), font=fonts['italic'])
    draw.text((495*SCALE, y_b - 24*SCALE), "b", fill=(0, 0, 0), font=fonts['italic'])
    
    draw.text((H[0] - 22*SCALE, H[1] - 26*SCALE), "H", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((G[0] - 22*SCALE, G[1] + 8*SCALE), "G", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((E[0] + 8*SCALE, E[1] - 26*SCALE), "E", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((F[0] + 8*SCALE, F[1] + 8*SCALE), "F", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((O_pt[0] - 22*SCALE, O_pt[1] - 12*SCALE), "O", fill=(220, 38, 38), font=fonts['bold_italic'])
    
    draw.text((O_pt[0] - 38*SCALE, O_pt[1] + 20*SCALE), "t", fill=(16, 185, 129), font=fonts['italic'])
    draw.text((O_pt[0] - 38*SCALE, O_pt[1] - 30*SCALE), "k", fill=(217, 119, 6), font=fonts['italic'])
    
    draw.text((E[0] + 16*SCALE, E[1] + 12*SCALE), "100°", fill=(37, 99, 235), font=fonts['deg_bold'])
    draw.text((F[0] - 65*SCALE, F[1] - 35*SCALE), "100°", fill=(37, 99, 235), font=fonts['deg_bold'])
    
    return save_resampled(img, "Hinh_8_Hinh_Tong_Hop_Bai_9.png")

# ==============================================================================
# HÌNH 9: BÀI 11 - HAI TAM GIÁC BẰNG NHAU (c-c-c: ABC và DBC)
# ==============================================================================
def render_hinh_9():
    w, h = 480 * SCALE, 260 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    B = (70 * SCALE, 130 * SCALE)
    C = (410 * SCALE, 130 * SCALE)
    A = (180 * SCALE, 50 * SCALE)
    D = (180 * SCALE, 210 * SCALE)
    
    draw.line([A, B], fill=(30, 41, 59), width=2*SCALE)
    draw.line([A, C], fill=(30, 41, 59), width=2*SCALE)
    draw.line([D, B], fill=(30, 41, 59), width=2*SCALE)
    draw.line([D, C], fill=(30, 41, 59), width=2*SCALE)
    draw.line([B, C], fill=(37, 99, 235), width=2*SCALE)
    
    draw_point(draw, A)
    draw_point(draw, B)
    draw_point(draw, C)
    draw_point(draw, D)
    
    draw_tick_mark(draw, A, B, count=1, size=8*SCALE, color=(220, 38, 38))
    draw_tick_mark(draw, D, B, count=1, size=8*SCALE, color=(220, 38, 38))
    draw_tick_mark(draw, A, C, count=2, size=8*SCALE, color=(220, 38, 38))
    draw_tick_mark(draw, D, C, count=2, size=8*SCALE, color=(220, 38, 38))
    
    draw.text((A[0] - 8*SCALE, A[1] - 26*SCALE), "A", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((D[0] - 8*SCALE, D[1] + 8*SCALE), "D", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((B[0] - 24*SCALE, B[1] - 10*SCALE), "B", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((C[0] + 10*SCALE, C[1] - 10*SCALE), "C", fill=(0, 0, 0), font=fonts['bold_italic'])
    
    return save_resampled(img, "Hinh_9_Tam_Giac_Bang_Nhau_CCC.png")

# ==============================================================================
# HÌNH 10: BÀI 12 - TAM GIÁC ĐỐI XỨNG QUA TRUNG ĐIỂM (c-g-c: AMB và CMD)
# ==============================================================================
def render_hinh_10():
    w, h = 500 * SCALE, 280 * SCALE
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    fonts = get_fonts()

    A = (160 * SCALE, 55 * SCALE)
    B = (70 * SCALE, 215 * SCALE)
    C = (380 * SCALE, 215 * SCALE)
    
    M = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
    D = (M[0] + (M[0] - B[0]), M[1] + (M[1] - B[1]))
    
    draw.line([A, B], fill=(30, 41, 59), width=2*SCALE)
    draw.line([B, C], fill=(30, 41, 59), width=2*SCALE)
    draw.line([A, C], fill=(30, 41, 59), width=2*SCALE)
    draw.line([B, D], fill=(37, 99, 235), width=2*SCALE)
    draw.line([C, D], fill=(16, 185, 129), width=2*SCALE)
    
    draw_point(draw, A)
    draw_point(draw, B)
    draw_point(draw, C)
    draw_point(draw, D)
    draw_point(draw, M, fill=(220, 38, 38))
    
    draw_tick_mark(draw, A, M, count=1, size=7*SCALE, color=(220, 38, 38))
    draw_tick_mark(draw, M, C, count=1, size=7*SCALE, color=(220, 38, 38))
    draw_tick_mark(draw, B, M, count=2, size=7*SCALE, color=(37, 99, 235))
    draw_tick_mark(draw, M, D, count=2, size=7*SCALE, color=(37, 99, 235))
    
    draw_angle_arc(draw, M, 145, 202, radius=24*SCALE, color=(16, 185, 129), width=2*SCALE)
    draw_angle_arc(draw, M, 325, 382, radius=24*SCALE, color=(16, 185, 129), width=2*SCALE)
    
    draw.text((A[0] - 15*SCALE, A[1] - 25*SCALE), "A", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((B[0] - 24*SCALE, B[1] - 5*SCALE), "B", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((C[0] + 5*SCALE, C[1] + 5*SCALE), "C", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((D[0] + 10*SCALE, D[1] - 22*SCALE), "D", fill=(0, 0, 0), font=fonts['bold_italic'])
    draw.text((M[0] - 5*SCALE, M[1] - 28*SCALE), "M", fill=(220, 38, 38), font=fonts['bold_italic'])
    
    return save_resampled(img, "Hinh_10_Tam_Giac_Doi_Xung_CGC.png")

if __name__ == "__main__":
    print("Vẽ lại 10 hình học chuẩn xác...")
    render_hinh_1()
    render_hinh_2()
    render_hinh_3()
    render_hinh_4()
    render_hinh_5()
    render_hinh_6()
    render_hinh_7()
    render_hinh_8()
    render_hinh_9()
    render_hinh_10()
    print("HOÀN TẤT VẼ 10 HÌNH HỌC!")
