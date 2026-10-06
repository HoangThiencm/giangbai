# -*- coding: utf-8 -*-
"""
Tạo các hình vẽ hình học chuẩn xác và Sơ đồ tư duy (Mindmap) chất lượng cao
cho Kế hoạch bài dạy Toán 9 (Chương IV & Chương V).
Được render ở độ phân giải cao và khử răng cưa bằng LANCZOS.
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

OUTPUT_DIR = "TROLYTHIEN/engine/hinh_ve_sgk"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(size, bold=False):
    # Ưu tiên Segoe UI vì hỗ trợ tiếng Việt và ký hiệu toán học đẹp nhất trên Windows
    font_names = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "timesbd.ttf" if bold else "times.ttf"
    ]
    for f in font_names:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, box, radius, fill, outline, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# ==============================================================================
# 1. HÌNH BÀI 12: TAM GIÁC VUÔNG VÀ HỆ THỨC LƯỢNG
# ==============================================================================
def create_hinh_bai12_tam_giac_vuong():
    w, h = 1300, 750
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)

    f_title = get_font(34, bold=True)
    f_label = get_font(28, bold=True)
    f_sub = get_font(22, bold=False)
    f_math = get_font(25, bold=True)

    # Khung nền
    draw_rounded_rect(d, [20, 20, w - 20, h - 20], 16, (248, 250, 252), (203, 213, 225), 3)

    # Tiêu đề
    d.text((w // 2, 55), "HỆ THỨC GIỮA CẠNH VÀ GÓC TRONG TAM GIÁC VUÔNG", fill=(30, 58, 138), font=f_title, anchor="mm")

    # Điểm tam giác ABC vuông tại A
    Ax, Ay = 220, 580
    Bx, By = 220, 210
    Cx, Cy = 750, 580

    # Vẽ tam giác
    d.polygon([(Ax, Ay), (Bx, By), (Cx, Cy)], fill=(238, 242, 255))
    d.line([(Ax, Ay), (Bx, By)], fill=(30, 64, 175), width=4)
    d.line([(Ax, Ay), (Cx, Cy)], fill=(30, 64, 175), width=4)
    d.line([(Bx, By), (Cx, Cy)], fill=(220, 38, 38), width=5) # Cạnh huyền màu đỏ

    # Góc vuông tại A
    sq = 32
    d.line([(Ax, Ay - sq), (Ax + sq, Ay - sq), (Ax + sq, Ay)], fill=(30, 64, 175), width=3)

    # Tên đỉnh
    d.text((Ax - 35, Ay + 15), "A", fill=(15, 23, 42), font=f_label, anchor="mm")
    d.text((Bx - 35, By - 15), "B", fill=(15, 23, 42), font=f_label, anchor="mm")
    d.text((Cx + 35, Cy + 15), "C", fill=(15, 23, 42), font=f_label, anchor="mm")

    # Tên cạnh: c = AB, b = AC, a = BC
    d.text((Ax - 25, (Ay + By) // 2), "c", fill=(30, 64, 175), font=f_math, anchor="mm")
    d.text(((Ax + Cx) // 2, Ay + 35), "b", fill=(30, 64, 175), font=f_math, anchor="mm")
    d.text(((Bx + Cx) // 2 + 35, (By + Cy) // 2 - 25), "a (cạnh huyền)", fill=(220, 38, 38), font=f_math, anchor="mm")

    # Cung góc B và C
    d.arc([Bx - 45, By - 45, Bx + 45, By + 45], start=40, end=90, fill=(16, 185, 129), width=3)
    d.arc([Cx - 65, Cy - 65, Cx + 65, Cy + 65], start=180, end=215, fill=(16, 185, 129), width=3)

    # Bảng công thức bên phải
    bx1, by1, bx2, by2 = 800, 130, 1260, 690
    draw_rounded_rect(d, [bx1, by1, bx2, by2], 14, (255, 255, 255), (148, 163, 184), 2)
    d.text((bx1 + (bx2 - bx1)//2, by1 + 35), "CÁC HỆ THỨC CƠ BẢN", fill=(180, 83, 9), font=get_font(24, bold=True), anchor="mm")
    d.line([(bx1 + 25, by1 + 65), (bx2 - 25, by1 + 65)], fill=(226, 232, 240), width=2)

    lines = [
        ("• Theo cạnh huyền và góc:", (30, 58, 138), True),
        ("   b = a · sin B = a · cos C", (15, 23, 42), True),
        ("   c = a · sin C = a · cos B", (15, 23, 42), True),
        ("", (0,0,0), False),
        ("• Theo cạnh góc vuông kia:", (30, 58, 138), True),
        ("   b = c · tan B = c · cot C", (15, 23, 42), True),
        ("   c = b · tan C = b · cot B", (15, 23, 42), True),
        ("", (0,0,0), False),
        ("• Định lí Pythagore:", (30, 58, 138), True),
        ("   a² = b² + c²", (220, 38, 38), True),
        ("", (0,0,0), False),
        ("• Tổng hai góc nhọn:", (30, 58, 138), True),
        ("   Góc B + Góc C = 90°", (16, 185, 129), True),
    ]

    cur_y = by1 + 85
    for txt, col, is_b in lines:
        if txt:
            d.text((bx1 + 25, cur_y), txt, fill=col, font=get_font(21, bold=is_b))
        cur_y += 38

    out_path = os.path.join(OUTPUT_DIR, "hinh_bai12_tam_giac_vuong_he_thuc.png")
    img_res = img.resize((650, 375), Image.Resampling.LANCZOS)
    img_res.save(out_path, dpi=(300, 300))
    print(f"Saved: {out_path}")

# ==============================================================================
# 2. HÌNH BÀI 12: GÓC NÂNG VÀ GÓC HẠ
# ==============================================================================
def create_hinh_bai12_goc_nang_ha():
    w, h = 1200, 600
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_text = get_font(24, bold=True)
    f_sub = get_font(22, bold=False)

    draw_rounded_rect(d, [20, 20, w - 20, h - 20], 16, (248, 250, 252), (203, 213, 225), 3)
    d.text((w // 2, 50), "KHÁI NIỆM GÓC NÂNG VÀ GÓC HẠ TRONG ĐO ĐẠC", fill=(30, 58, 138), font=f_title, anchor="mm")

    # Mắt người quan sát O
    Ox, Oy = 250, 310
    d.ellipse([Ox - 10, Oy - 10, Ox + 10, Oy + 10], fill=(220, 38, 38))
    d.text((Ox - 25, Oy), "O (Mắt nhìn)", fill=(220, 38, 38), font=f_text, anchor="rm")

    # Đường nằm ngang chuẩn
    d.line([(Ox, Oy), (Ox + 620, Oy)], fill=(71, 85, 105), width=3)
    d.text((Ox + 640, Oy), "Đường nằm ngang", fill=(71, 85, 105), font=f_sub, anchor="lm")

    # Điểm nhìn trên cao A (Góc nâng)
    Ax, Ay = Ox + 480, Oy - 170
    d.line([(Ox, Oy), (Ax, Ay)], fill=(30, 64, 175), width=4)
    d.ellipse([Ax - 8, Ay - 8, Ax + 8, Ay + 8], fill=(30, 64, 175))
    d.text((Ax + 15, Ay), "Vật thể ở trên (A)", fill=(30, 64, 175), font=f_text, anchor="lm")

    # Vòng cung góc nâng
    d.arc([Ox - 90, Oy - 90, Ox + 90, Oy + 90], start=-25, end=0, fill=(30, 64, 175), width=3)
    d.text((Ox + 120, Oy - 40), "GÓC NÂNG (α)", fill=(30, 64, 175), font=f_text)

    # Điểm nhìn dưới thấp B (Góc hạ)
    Bx, By = Ox + 480, Oy + 170
    d.line([(Ox, Oy), (Bx, By)], fill=(16, 185, 129), width=4)
    d.ellipse([Bx - 8, By - 8, Bx + 8, By + 8], fill=(16, 185, 129))
    d.text((Bx + 15, By), "Vật thể ở dưới (B)", fill=(16, 185, 129), font=f_text, anchor="lm")

    # Vòng cung góc hạ
    d.arc([Ox - 90, Oy - 90, Ox + 90, Oy + 90], start=0, end=25, fill=(16, 185, 129), width=3)
    d.text((Ox + 120, Oy + 30), "GÓC HẠ (β)", fill=(16, 185, 129), font=f_text)

    # Chú thích cuối hình
    d.text((w // 2, 540), "Góc nâng: tia ngắm hướng lên so với phương ngang | Góc hạ: tia ngắm hướng xuống so với phương ngang", fill=(100, 116, 139), font=f_sub, anchor="mm")

    out_path = os.path.join(OUTPUT_DIR, "hinh_bai12_goc_nang_goc_ha.png")
    img_res = img.resize((600, 300), Image.Resampling.LANCZOS)
    img_res.save(out_path, dpi=(300, 300))
    print(f"Saved: {out_path}")

# ==============================================================================
# 3. HÌNH BÀI 12: ĐO CHIỀU CAO THỰC TẾ
# ==============================================================================
def create_hinh_bai12_do_chieu_cao():
    w, h = 1200, 700
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_text = get_font(24, bold=True)
    f_sub = get_font(22, bold=False)
    f_math = get_font(26, bold=True)

    draw_rounded_rect(d, [20, 20, w - 20, h - 20], 16, (248, 250, 252), (203, 213, 225), 3)
    d.text((w // 2, 50), "MÔ HÌNH TOÁN HỌC: ĐO CHIỀU CAO TÒA THÁP / LÂU ĐÀI", fill=(30, 58, 138), font=f_title, anchor="mm")

    # Mặt đất
    gy = 580
    d.line([(80, gy), (1120, gy)], fill=(34, 197, 94), width=6)
    d.text((100, gy + 30), "Mặt đất bằng phẳng", fill=(22, 101, 52), font=f_sub)

    # Giác kế tại A
    Ax = 250
    h_gk = 140
    Oy = gy - h_gk
    # Cọc giác kế
    d.line([(Ax, gy), (Ax, Oy)], fill=(15, 23, 42), width=5)
    d.ellipse([Ax - 10, Oy - 10, Ax + 10, Oy + 10], fill=(220, 38, 38))
    d.text((Ax - 20, gy - h_gk // 2), "h = 1,2 m", fill=(15, 23, 42), font=f_text, anchor="rm")
    d.text((Ax, Oy - 25), "Mắt nhìn C", fill=(220, 38, 38), font=f_text, anchor="mm")

    # Tòa tháp / lâu đài tại chân B
    Bx = 900
    top_y = 160
    d.rectangle([Bx - 30, top_y, Bx + 30, gy], fill=(226, 232, 240), outline=(71, 85, 105), width=3)
    d.polygon([(Bx - 45, top_y), (Bx + 45, top_y), (Bx, top_y - 40)], fill=(239, 68, 68)) # chóp
    d.text((Bx, top_y - 55), "Đỉnh tháp (A')", fill=(220, 38, 38), font=f_text, anchor="mm")
    d.text((Bx, gy + 30), "Chân tháp (B')", fill=(15, 23, 42), font=f_text, anchor="mm")

    # Đường ngắm nằm ngang từ C sang H trên tháp
    Hx = Bx - 30
    Hy = Oy
    d.line([(Ax, Oy), (Hx, Hy)], fill=(71, 85, 105), width=3)
    d.line([(Ax, Oy), (Bx, top_y)], fill=(30, 64, 175), width=4) # Đường ngắm đỉnh tháp

    # Góc nâng alpha
    d.arc([Ax - 80, Oy - 80, Ax + 80, Oy + 80], start=-35, end=0, fill=(30, 64, 175), width=3)
    d.text((Ax + 100, Oy - 30), "α = 38°", fill=(30, 64, 175), font=f_math)

    # Đoạn CH = a (khoảng cách)
    d.text(((Ax + Hx)//2, Oy + 25), "a = 25 m", fill=(15, 23, 42), font=f_math, anchor="mm")

    # Chiều cao tháp H = h + A'H
    d.line([(Bx + 60, top_y), (Bx + 60, gy)], fill=(220, 38, 38), width=3)
    d.line([(Bx + 50, top_y), (Bx + 70, top_y)], fill=(220, 38, 38), width=2)
    d.line([(Bx + 50, gy), (Bx + 70, gy)], fill=(220, 38, 38), width=2)
    d.text((Bx + 80, (top_y + gy)//2), "H = ?", fill=(220, 38, 38), font=f_text, anchor="lm")

    # Công thức tính
    box_math = [380, 200, 780, 330]
    draw_rounded_rect(d, box_math, 12, (255, 255, 255), (148, 163, 184), 2)
    d.text((580, 230), "CÔNG THỨC TÍNH CHIỀU CAO:", fill=(30, 58, 138), font=f_text, anchor="mm")
    d.text((580, 265), "A'H = a · tan α = 25 · tan 38° ≈ 19,53 m", fill=(15, 23, 42), font=get_font(22, bold=False), anchor="mm")
    d.text((580, 300), "H = h + A'H ≈ 1,2 + 19,53 = 20,73 m", fill=(220, 38, 38), font=f_math, anchor="mm")

    out_path = os.path.join(OUTPUT_DIR, "hinh_bai12_do_chieu_cao_thuc_te.png")
    img_res = img.resize((600, 350), Image.Resampling.LANCZOS)
    img_res.save(out_path, dpi=(300, 300))
    print(f"Saved: {out_path}")

# ==============================================================================
# 4. HÌNH BÀI 13: ĐƯỜNG TRÒN VÀ VỊ TRÍ TƯƠNG ĐỐI CỦA ĐIỂM
# ==============================================================================
def create_hinh_bai13_duong_tron_vi_tri():
    w, h = 1300, 760
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)

    f_title = get_font(34, bold=True)
    f_text = get_font(24, bold=True)
    f_sub = get_font(21, bold=False)
    f_math = get_font(23, bold=True)

    draw_rounded_rect(d, [20, 20, w - 20, h - 20], 16, (248, 250, 252), (203, 213, 225), 3)
    d.text((w // 2, 55), "ĐƯỜNG TRÒN VÀ VỊ TRÍ TƯƠNG ĐỐI CỦA MỘT ĐIỂM", fill=(30, 58, 138), font=f_title, anchor="mm")

    # Đường tròn tâm O, bán kính R = 180, dịch sang trái
    Ox, Oy = 290, 420
    R = 180
    d.ellipse([Ox - R, Oy - R, Ox + R, Oy + R], outline=(30, 64, 175), width=4, fill=(241, 245, 249))

    # Tâm O
    d.ellipse([Ox - 6, Oy - 6, Ox + 6, Oy + 6], fill=(220, 38, 38))
    d.text((Ox - 20, Oy + 15), "O", fill=(220, 38, 38), font=f_text, anchor="mm")

    # Bán kính OA: điểm A nằm trên đường tròn (góc 45 độ)
    angA = math.radians(45)
    Ax = int(Ox + R * math.cos(angA))
    Ay = int(Oy - R * math.sin(angA))
    d.line([(Ox, Oy), (Ax, Ay)], fill=(30, 64, 175), width=3)
    d.ellipse([Ax - 6, Ay - 6, Ax + 6, Ay + 6], fill=(30, 64, 175))
    d.text((Ax + 20, Ay - 15), "A thuộc (O)", fill=(30, 64, 175), font=f_text, anchor="mm")
    d.text(((Ox + Ax)//2 - 15, (Oy + Ay)//2 - 15), "R", fill=(30, 64, 175), font=f_math, anchor="mm")

    # Điểm C nằm trong đường tròn (OC < R)
    angC = math.radians(160)
    Cx = int(Ox + (R * 0.55) * math.cos(angC))
    Cy = int(Oy - (R * 0.55) * math.sin(angC))
    d.line([(Ox, Oy), (Cx, Cy)], fill=(16, 185, 129), width=2)
    d.ellipse([Cx - 6, Cy - 6, Cx + 6, Cy + 6], fill=(16, 185, 129))
    d.text((Cx - 20, Cy - 20), "C (nằm trong)", fill=(16, 185, 129), font=f_text, anchor="mm")

    # Điểm B nằm ngoài đường tròn (OB > R) - hướng chéo xuống
    angB = math.radians(-55)
    Bx = int(Ox + (R * 1.45) * math.cos(angB))
    By = int(Oy - (R * 1.45) * math.sin(angB))
    d.line([(Ox, Oy), (Bx, By)], fill=(220, 38, 38), width=2)
    d.ellipse([Bx - 6, By - 6, Bx + 6, By + 6], fill=(220, 38, 38))
    d.text((Bx, By + 22), "B (nằm ngoài)", fill=(220, 38, 38), font=f_text, anchor="mt")

    # Bảng kết luận bên phải
    bx1, by1, bx2, by2 = 620, 120, 1260, 710
    draw_rounded_rect(d, [bx1, by1, bx2, by2], 14, (255, 255, 255), (148, 163, 184), 2)
    d.text((bx1 + (bx2 - bx1)//2, by1 + 35), "VỊ TRÍ CỦA ĐIỂM M VỚI (O; R)", fill=(30, 58, 138), font=get_font(24, bold=True), anchor="mm")
    d.line([(bx1 + 25, by1 + 65), (bx2 - 25, by1 + 65)], fill=(226, 232, 240), width=2)

    conclusions = [
        ("1. Điểm M nằm TRÊN đường tròn:", (30, 64, 175), True),
        ("   OM = R   (kí hiệu M thuộc (O; R))", (15, 23, 42), True),
        ("", (0,0,0), False),
        ("2. Điểm M nằm TRONG đường tròn:", (16, 185, 129), True),
        ("   OM < R", (15, 23, 42), True),
        ("", (0,0,0), False),
        ("3. Điểm M nằm NGOÀI đường tròn:", (220, 38, 38), True),
        ("   OM > R", (15, 23, 42), True),
        ("", (0,0,0), False),
        ("GHI CHÚ QUAN TRỌNG:", (180, 83, 9), True),
        ("• Hình tròn gồm các điểm nằm trên", (71, 85, 105), False),
        ("   và các điểm nằm trong đường tròn.", (71, 85, 105), False),
        ("• Dây đi qua tâm gọi là ĐƯỜNG KÍNH.", (30, 64, 175), True),
        ("• Đường kính có độ dài d = 2R.", (15, 23, 42), True)
    ]
    cur_y = by1 + 80
    for txt, col, is_b in conclusions:
        if txt:
            d.text((bx1 + 25, cur_y), txt, fill=col, font=get_font(21, bold=is_b))
        cur_y += 36

    out_path = os.path.join(OUTPUT_DIR, "hinh_bai13_duong_tron_vi_tri_diem.png")
    img_res = img.resize((650, 380), Image.Resampling.LANCZOS)
    img_res.save(out_path, dpi=(300, 300))
    print(f"Saved: {out_path}")

# ==============================================================================
# 5. HÌNH BÀI 13: TÍNH ĐỐI XỨNG CỦA ĐƯỜNG TRÒN
# ==============================================================================
def create_hinh_bai13_tam_va_truc_doi_xung():
    w, h = 1300, 760
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)

    f_title = get_font(34, bold=True)
    f_text = get_font(24, bold=True)
    f_sub = get_font(21, bold=False)

    draw_rounded_rect(d, [20, 20, w - 20, h - 20], 16, (248, 250, 252), (203, 213, 225), 3)
    d.text((w // 2, 55), "TÍNH ĐỐI XỨNG CỦA ĐƯỜNG TRÒN: TÂM VÀ TRỤC ĐỐI XỨNG", fill=(30, 58, 138), font=f_title, anchor="mm")

    # Đường tròn tâm O dịch sang trái
    Ox, Oy = 290, 420
    R = 180
    d.ellipse([Ox - R, Oy - R, Ox + R, Oy + R], outline=(30, 64, 175), width=4, fill=(241, 245, 249))

    # Đường kính AB nằm ngang (làm trục đối xứng)
    Ax, Ay = Ox - R, Oy
    Bx, By = Ox + R, Oy
    d.line([(Ax - 50, Ay), (Bx + 60, By)], fill=(220, 38, 38), width=3) # Trục đối xứng d (chứa AB)
    d.text((Bx + 20, By - 30), "Trục d", fill=(220, 38, 38), font=get_font(22, bold=True), anchor="lm")
    d.text((Ax - 15, Ay - 20), "A", fill=(15, 23, 42), font=f_text, anchor="mm")
    d.text((Bx + 15, By + 25), "B", fill=(15, 23, 42), font=f_text, anchor="mm")

    # Tâm O
    d.ellipse([Ox - 6, Oy - 6, Ox + 6, Oy + 6], fill=(220, 38, 38))
    d.text((Ox, Oy + 25), "O (Tâm đối xứng)", fill=(220, 38, 38), font=f_text, anchor="mm")

    # Điểm M trên đường tròn (góc 55 độ)
    angM = math.radians(55)
    Mx = int(Ox + R * math.cos(angM))
    My = int(Oy - R * math.sin(angM))
    d.ellipse([Mx - 6, My - 6, Mx + 6, My + 6], fill=(30, 64, 175))
    d.text((Mx + 20, My - 15), "M", fill=(30, 64, 175), font=f_text, anchor="mm")

    # Điểm N đối xứng với M qua tâm O: N = 2O - M
    Nx = 2 * Ox - Mx
    Ny = 2 * Oy - My
    d.line([(Mx, My), (Nx, Ny)], fill=(16, 185, 129), width=3)
    d.ellipse([Nx - 6, Ny - 6, Nx + 6, Ny + 6], fill=(16, 185, 129))
    d.text((Nx - 20, Ny + 15), "N", fill=(16, 185, 129), font=f_text, anchor="mm")
    d.text(((Ox + Nx)//2 - 25, (Oy + Ny)//2), "OM = ON", fill=(16, 185, 129), font=get_font(18, bold=True), anchor="mm")

    # Điểm P đối xứng với M qua trục d (đường thẳng AB)
    Px = Mx
    Py = 2 * Oy - My
    d.line([(Mx, My), (Px, Py)], fill=(147, 51, 234), width=3)
    d.ellipse([Px - 6, Py - 6, Px + 6, Py + 6], fill=(147, 51, 234))
    d.text((Px + 20, Py + 15), "P", fill=(147, 51, 234), font=f_text, anchor="mm")

    # Chân vuông góc H
    d.ellipse([Mx - 4, Oy - 4, Mx + 4, Oy + 4], fill=(15, 23, 42))
    d.text((Mx - 15, Oy - 15), "H", fill=(15, 23, 42), font=get_font(20, bold=True), anchor="mm")
    sq = 15
    d.line([(Mx - sq, Oy), (Mx - sq, Oy - sq), (Mx, Oy - sq)], fill=(147, 51, 234), width=2)

    # Bảng phân tích bên phải
    bx1, by1, bx2, by2 = 600, 120, 1260, 710
    draw_rounded_rect(d, [bx1, by1, bx2, by2], 14, (255, 255, 255), (148, 163, 184), 2)
    d.text((bx1 + (bx2 - bx1)//2, by1 + 35), "TÍNH CHẤT ĐỐI XỨNG CỦA (O)", fill=(30, 58, 138), font=get_font(24, bold=True), anchor="mm")
    d.line([(bx1 + 25, by1 + 65), (bx2 - 25, by1 + 65)], fill=(226, 232, 240), width=2)

    prop_lines = [
        ("1. TÂM ĐỐI XỨNG:", (220, 38, 38), True),
        ("• Đường tròn là hình CÓ TÂM ĐỐI XỨNG.", (15, 23, 42), True),
        ("• Tâm O chính là tâm đối xứng của (O).", (71, 85, 105), False),
        ("• Với mọi M thuộc (O), điểm N đối xứng", (15, 23, 42), False),
        ("   với M qua O cũng thuộc (O) (MN là đường kính).", (16, 185, 129), True),
        ("", (0,0,0), False),
        ("2. TRỤC ĐỐI XỨNG:", (147, 51, 234), True),
        ("• Đường tròn là hình CÓ TRỤC ĐỐI XỨNG.", (15, 23, 42), True),
        ("• MỖI ĐƯỜNG THẲNG ĐI QUA TÂM O là một", (71, 85, 105), False),
        ("   trục đối xứng của đường tròn.", (71, 85, 105), False),
        ("• Đường tròn có VÔ SỐ trục đối xứng.", (220, 38, 38), True),
        ("• Nếu d đi qua O và M thuộc (O) thì điểm P", (15, 23, 42), False),
        ("   đối xứng với M qua d cũng thuộc (O).", (147, 51, 234), True)
    ]
    cur_y = by1 + 80
    for txt, col, is_b in prop_lines:
        if txt:
            d.text((bx1 + 25, cur_y), txt, fill=col, font=get_font(20, bold=is_b))
        cur_y += 36

    out_path = os.path.join(OUTPUT_DIR, "hinh_bai13_tam_va_truc_doi_xung.png")
    img_res = img.resize((650, 380), Image.Resampling.LANCZOS)
    img_res.save(out_path, dpi=(300, 300))
    print(f"Saved: {out_path}")

# ==============================================================================
# 6. SƠ ĐỒ TƯ DUY 1: LUYỆN TẬP CHUNG CHƯƠNG IV (BÀI 02)
# ==============================================================================
def create_mindmap_luyen_tap_chung():
    w, h = 1500, 880
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)

    f_title = get_font(36, bold=True)
    f_center = get_font(26, bold=True)
    f_branch = get_font(22, bold=True)
    f_sub = get_font(19, bold=False)

    # Nền
    draw_rounded_rect(d, [20, 20, w - 20, h - 20], 20, (248, 250, 252), (203, 213, 225), 3)
    d.text((w // 2, 55), "SƠ ĐỒ TƯ DUY: HỆ THỐNG KIẾN THỨC BÀI 11 & BÀI 12", fill=(30, 58, 138), font=f_title, anchor="mm")

    # Tọa độ tâm
    cx, cy = w // 2, h // 2 + 25
    cw, ch = 340, 140

    # 4 Nhánh chính
    branches = [
        # 1. Tây Bắc: Tỉ số lượng giác góc nhọn
        {
            "bx": 320, "by": 210, "bw": 420, "bh": 200,
            "title": "1. TỈ SỐ LƯỢNG GIÁC GÓC NHỌN", "color": (16, 185, 129),
            "items": [
                "• sin α = đối / huyền ; cos α = kề / huyền",
                "• tan α = đối / kề ; cot α = kề / đối",
                "• Hai góc phụ nhau: sin α = cos(90° - α)",
                "• tan α = cot(90° - α) ; sin²α + cos²α = 1",
                "• Bảng góc đặc biệt: 30°, 45°, 60°"
            ]
        },
        # 2. Đông Bắc: Hệ thức cạnh và góc
        {
            "bx": 1180, "by": 210, "bw": 420, "bh": 200,
            "title": "2. HỆ THỨC CẠNH VÀ GÓC", "color": (220, 38, 38),
            "items": [
                "• b = a · sin B = a · cos C",
                "• c = a · sin C = a · cos B",
                "• b = c · tan B = c · cot C",
                "• c = b · tan C = b · cot B",
                "• Định lí Pythagore: a² = b² + c²"
            ]
        },
        # 3. Tây Nam: Giải tam giác vuông
        {
            "bx": 320, "by": 660, "bw": 420, "bh": 200,
            "title": "3. GIẢI TAM GIÁC VUÔNG", "color": (147, 51, 234),
            "items": [
                "• Tìm tất cả các cạnh và góc chưa biết",
                "• Dạng 1: Biết 1 cạnh và 1 góc nhọn",
                "• Dạng 2: Biết độ dài 2 cạnh",
                "• Luôn nhớ: Tổng hai góc nhọn bằng 90°",
                "• Sử dụng máy tính cầm tay tính tỉ số góc"
            ]
        },
        # 4. Đông Nam: Ứng dụng thực tế
        {
            "bx": 1180, "by": 660, "bw": 420, "bh": 200,
            "title": "4. ỨNG DỤNG THỰC TẾ", "color": (217, 119, 6),
            "items": [
                "• Đo chiều cao cây cối, lâu đài, tòa tháp",
                "• Đo khoảng cách giữa 2 bờ sông",
                "• Xác định góc nâng (hướng lên phương ngang)",
                "• Xác định góc hạ (hướng xuống phương ngang)",
                "• Mô hình hóa hình thang, tam giác phụ"
            ]
        }
    ]

    # BƯỚC 1: VẼ ĐƯỜNG NỐI TRƯỚC (để đường nối nằm dưới các hộp)
    for b in branches:
        d.line([(cx, cy), (b["bx"], b["by"])], fill=b["color"], width=5)

    # BƯỚC 2: VẼ HỘP TRUNG TÂM ĐÈ LÊN ĐƯỜNG NỐI
    draw_rounded_rect(d, [cx - cw//2, cy - ch//2, cx + cw//2, cy + ch//2], 25, (30, 58, 138), (30, 64, 175), 4)
    d.text((cx, cy - 25), "HỆ THỨC LƯỢNG", fill=(255, 255, 255), font=f_center, anchor="mm")
    d.text((cx, cy + 22), "TRONG TAM GIÁC VUÔNG", fill=(254, 240, 138), font=f_center, anchor="mm")

    # BƯỚC 3: VẼ CÁC HỘP NHÁNH
    for b in branches:
        bx1 = b["bx"] - b["bw"]//2
        by1 = b["by"] - b["bh"]//2
        bx2 = b["bx"] + b["bw"]//2
        by2 = b["by"] + b["bh"]//2
        draw_rounded_rect(d, [bx1, by1, bx2, by2], 16, (255, 255, 255), b["color"], 3)

        # Tiêu đề nhánh
        d.text((b["bx"], by1 + 28), b["title"], fill=b["color"], font=f_branch, anchor="mm")
        d.line([(bx1 + 20, by1 + 52), (bx2 - 20, by1 + 52)], fill=(226, 232, 240), width=2)

        # Các dòng nội dung
        cur_y = by1 + 68
        for it in b["items"]:
            d.text((bx1 + 22, cur_y), it, fill=(30, 41, 59), font=f_sub)
            cur_y += 26

    out_path = os.path.join(OUTPUT_DIR, "mindmap_toan9_chuong4_he_thuc_luong.png")
    img_res = img.resize((750, 440), Image.Resampling.LANCZOS)
    img_res.save(out_path, dpi=(300, 300))
    print(f"Saved: {out_path}")

# ==============================================================================
# 7. SƠ ĐỒ TƯ DUY 2: TỔNG HỢP CHƯƠNG IV (BÀI 03)
# ==============================================================================
def create_mindmap_tong_hop_chuong4():
    w, h = 1500, 900
    img = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(img)

    f_title = get_font(36, bold=True)
    f_center = get_font(26, bold=True)
    f_branch = get_font(22, bold=True)
    f_sub = get_font(19, bold=False)

    # Nền
    draw_rounded_rect(d, [20, 20, w - 20, h - 20], 20, (248, 250, 252), (203, 213, 225), 3)
    d.text((w // 2, 55), "SƠ ĐỒ TƯ DUY: TỔNG HỢP TOÀN BỘ CHƯƠNG IV (TOÁN 9)", fill=(30, 58, 138), font=f_title, anchor="mm")

    # Tọa độ tâm
    cx, cy = w // 2, h // 2 + 25
    cw, ch = 350, 150

    # 4 Nhánh tổng hợp
    branches = [
        # Nhánh 1: Tỉ số lượng giác góc nhọn
        {
            "bx": 320, "by": 210, "bw": 420, "bh": 210,
            "title": "I. TỈ SỐ LƯỢNG GIÁC", "color": (16, 185, 129),
            "items": [
                "• Định nghĩa: sin, cos, tan, cot góc nhọn",
                "• Tỉ số góc phụ nhau: sin α = cos(90° - α)",
                "• Bảng góc đặc biệt: 30°, 45°, 60°",
                "• Công thức vàng: sin²α + cos²α = 1",
                "• tan α · cot α = 1 ; tan α = sin α / cos α"
            ]
        },
        # Nhánh 2: Các hệ thức giữa cạnh và góc
        {
            "bx": 1180, "by": 210, "bw": 420, "bh": 210,
            "title": "II. HỆ THỨC CẠNH VÀ GÓC", "color": (220, 38, 38),
            "items": [
                "• b = a · sin B = a · cos C",
                "• c = a · sin C = a · cos B",
                "• b = c · tan B = c · cot C",
                "• c = b · tan C = b · cot B",
                "• Định lí Pythagore: a² = b² + c²"
            ]
        },
        # Nhánh 3: Kĩ năng giải tam giác vuông
        {
            "bx": 320, "by": 670, "bw": 420, "bh": 210,
            "title": "III. GIẢI TAM GIÁC VUÔNG", "color": (147, 51, 234),
            "items": [
                "• Tính cạnh & góc khi biết đủ 2 yếu tố",
                "• Trường hợp 1 cạnh huyền + 1 góc nhọn",
                "• Trường hợp 1 cạnh góc vuông + 1 góc nhọn",
                "• Trường hợp biết 2 cạnh (tìm góc qua shift)",
                "• AI 9.D1.1: Định hướng kẻ thêm đường phụ"
            ]
        },
        # Nhánh 4: Vận dụng thực tế & Mô hình hóa
        {
            "bx": 1180, "by": 670, "bw": 420, "bh": 210,
            "title": "IV. VẬN DỤNG THỰC TẾ", "color": (217, 119, 6),
            "items": [
                "• Xác định góc nâng (hướng lên) & góc hạ",
                "• Đo chiều cao vật thể không tới chân được",
                "• Tính khoảng cách qua sông / khúc cua",
                "• Bài toán lịch sử: Đo chu vi Trái Đất",
                "• Bài toán cây gãy, con tàu lặn biển"
            ]
        }
    ]

    # BƯỚC 1: VẼ ĐƯỜNG NỐI TRƯỚC
    for b in branches:
        d.line([(cx, cy), (b["bx"], b["by"])], fill=b["color"], width=5)

    # BƯỚC 2: VẼ HỘP TRUNG TÂM ĐÈ LÊN ĐƯỜNG NỐI
    draw_rounded_rect(d, [cx - cw//2, cy - ch//2, cx + cw//2, cy + ch//2], 25, (30, 58, 138), (30, 64, 175), 4)
    d.text((cx, cy - 35), "CHƯƠNG IV", fill=(254, 240, 138), font=f_center, anchor="mm")
    d.text((cx, cy - 2), "HỆ THỨC LƯỢNG", fill=(255, 255, 255), font=f_center, anchor="mm")
    d.text((cx, cy + 32), "TRONG TAM GIÁC VUÔNG", fill=(255, 255, 255), font=get_font(21, bold=True), anchor="mm")

    # BƯỚC 3: VẼ CÁC HỘP NHÁNH
    for b in branches:
        bx1 = b["bx"] - b["bw"]//2
        by1 = b["by"] - b["bh"]//2
        bx2 = b["bx"] + b["bw"]//2
        by2 = b["by"] + b["bh"]//2
        draw_rounded_rect(d, [bx1, by1, bx2, by2], 16, (255, 255, 255), b["color"], 3)

        d.text((b["bx"], by1 + 28), b["title"], fill=b["color"], font=f_branch, anchor="mm")
        d.line([(bx1 + 20, by1 + 52), (bx2 - 20, by1 + 52)], fill=(226, 232, 240), width=2)

        cur_y = by1 + 68
        for it in b["items"]:
            d.text((bx1 + 22, cur_y), it, fill=(30, 41, 59), font=f_sub)
            cur_y += 26

    out_path = os.path.join(OUTPUT_DIR, "mindmap_toan9_chuong4_tong_hop.png")
    img_res = img.resize((750, 450), Image.Resampling.LANCZOS)
    img_res.save(out_path, dpi=(300, 300))
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    print("Bắt đầu khởi tạo các hình vẽ và Mindmap hoàn thiện...")
    create_hinh_bai12_tam_giac_vuong()
    create_hinh_bai12_goc_nang_ha()
    create_hinh_bai12_do_chieu_cao()
    create_hinh_bai13_duong_tron_vi_tri()
    create_hinh_bai13_tam_va_truc_doi_xung()
    create_mindmap_luyen_tap_chung()
    create_mindmap_tong_hop_chuong4()
    print("Hoàn tất tạo trọn bộ hình ảnh chuẩn mực!")
