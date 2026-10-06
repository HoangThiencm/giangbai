# -*- coding: utf-8 -*-
"""
Script vẽ Sơ đồ tư duy dạng PNG chuẩn sắc nét (300 DPI) cho Toán 9 - Chương II:
Tuân thủ 100% Quy chuẩn Sư phạm THCS (GDPT 2018):
- Tuyệt đối KHÔNG dùng dấu tương đương (<=>, ⇔) hay ký hiệu logic hình thức Cấp 3.
- Dùng cấu trúc tự nhiên: "Nếu ... thì ...", "chuyển vế được", "suy ra".
1. mindmap_toan9_chuong2_bai5.png (Bất đẳng thức & Tính chất - cho Bài 02)
2. mindmap_toan9_chuong2_tong_hop.png (Tổng hợp Chương II - cho Bài 04)
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.abspath(r"TROLYTHIEN\engine\hinh_ve_sgk")
os.makedirs(OUT_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_path = "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

def draw_rounded_box(draw, xy, fill, outline, width=2, radius=10):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# ==============================================================================
# 1. SƠ ĐỒ TƯ DUY CHO BÀI 02: BẤT ĐẲNG THỨC VÀ TÍNH CHẤT
# ==============================================================================
def draw_mindmap_toan9_bai5():
    w, h = 1050, 520
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_node = get_font(16, bold=True)
    f_sub = get_font(15, bold=True)
    f_text = get_font(13, bold=False)

    # Tiêu đề
    draw.text((w // 2, 25), "SƠ ĐỒ TƯ DUY: BẤT ĐẲNG THỨC VÀ CÁC TÍNH CHẤT CƠ BẢN", fill="#1E3A8A", font=f_title, anchor="mm")

    # Trung tâm
    draw_rounded_box(draw, [(360, 65), (690, 125)], fill="#DBEAFE", outline="#1D4ED8", width=3, radius=12)
    draw.text((525, 85), "BẤT ĐẲNG THỨC", fill="#1E3A8A", font=f_title, anchor="mm")
    draw.text((525, 108), "Khái niệm & Tính chất liên hệ phép toán", fill="#1D4ED8", font=f_text, anchor="mm")

    # 4 Cột / Nhánh
    # Nhánh 1: Khái niệm & Ký hiệu
    b1_x1, b1_y1, b1_x2, b1_y2 = 25, 170, 260, 485
    draw.line([(420, 125), (142, 170)], fill="#2563EB", width=2)
    draw_rounded_box(draw, [(b1_x1, b1_y1), (b1_x2, b1_y2)], fill="#F8FAFC", outline="#3B82F6", width=2, radius=10)
    draw_rounded_box(draw, [(b1_x1, b1_y1), (b1_x2, b1_y1 + 40)], fill="#EFF6FF", outline="#3B82F6", width=2, radius=10)
    draw.text(((b1_x1 + b1_x2) // 2, b1_y1 + 20), "1. KHÁI NIỆM", fill="#1D4ED8", font=f_sub, anchor="mm")

    draw.text((b1_x1 + 12, b1_y1 + 55), "• Dạng tổng quát:", fill="#1E293B", font=f_sub)
    draw.text((b1_x1 + 20, b1_y1 + 80), "a < b,  a > b", fill="#0F766E", font=f_node)
    draw.text((b1_x1 + 20, b1_y1 + 105), "a ≤ b,  a ≥ b", fill="#0F766E", font=f_node)
    draw.text((b1_x1 + 12, b1_y1 + 140), "• Vế trái (a), vế phải (b)", fill="#1E293B", font=f_text)
    draw.text((b1_x1 + 12, b1_y1 + 175), "• BĐT cùng chiều:", fill="#1E293B", font=f_sub)
    draw.text((b1_x1 + 20, b1_y1 + 200), "a < b và c < d", fill="#2563EB", font=f_text)
    draw.text((b1_x1 + 12, b1_y1 + 235), "• BĐT ngược chiều:", fill="#1E293B", font=f_sub)
    draw.text((b1_x1 + 20, b1_y1 + 260), "a < b và c > d", fill="#DC2626", font=f_text)

    # Nhánh 2: Tính chất bắc cầu
    b2_x1, b2_y1, b2_x2, b2_y2 = 280, 170, 515, 485
    draw.line([(480, 125), (397, 170)], fill="#16A34A", width=2)
    draw_rounded_box(draw, [(b2_x1, b2_y1), (b2_x2, b2_y2)], fill="#F0FDF4", outline="#16A34A", width=2, radius=10)
    draw_rounded_box(draw, [(b2_x1, b2_y1), (b2_x2, b2_y1 + 40)], fill="#DCFCE7", outline="#16A34A", width=2, radius=10)
    draw.text(((b2_x1 + b2_x2) // 2, b2_y1 + 20), "2. TÍNH CHẤT BẮC CẦU", fill="#15803D", font=f_sub, anchor="mm")

    draw.text((b2_x1 + 12, b2_y1 + 55), "• Quy tắc bắc cầu:", fill="#1E293B", font=f_sub)
    draw_rounded_box(draw, [(b2_x1 + 12, b2_y1 + 85), (b2_x2 - 12, b2_y1 + 155)], fill="#FFFFFF", outline="#16A34A", width=1, radius=6)
    draw.text(((b2_x1 + b2_x2) // 2, b2_y1 + 105), "Nếu a < b và b < c", fill="#15803D", font=f_node, anchor="mm")
    draw.text(((b2_x1 + b2_x2) // 2, b2_y1 + 135), "thì a < c", fill="#B91C1C", font=f_title, anchor="mm")
    draw.text((b2_x1 + 12, b2_y1 + 175), "• Tương tự với các thứ tự:", fill="#1E293B", font=f_text)
    draw.text((b2_x1 + 20, b2_y1 + 205), "a > b và b > c thì a > c", fill="#1E293B", font=f_text)
    draw.text((b2_x1 + 20, b2_y1 + 235), "a ≤ b và b ≤ c thì a ≤ c", fill="#1E293B", font=f_text)
    draw.text((b2_x1 + 12, b2_y1 + 270), "• Ứng dụng: So sánh qua", fill="#1E293B", font=f_text)
    draw.text((b2_x1 + 20, b2_y1 + 295), "số trung gian (0, 1, ...)", fill="#0284C7", font=f_sub)

    # Nhánh 3: Thứ tự & Phép cộng
    b3_x1, b3_y1, b3_x2, b3_y2 = 535, 170, 775, 485
    draw.line([(570, 125), (655, 170)], fill="#D97706", width=2)
    draw_rounded_box(draw, [(b3_x1, b3_y1), (b3_x2, b3_y2)], fill="#FFFBEB", outline="#D97706", width=2, radius=10)
    draw_rounded_box(draw, [(b3_x1, b3_y1), (b3_x2, b3_y1 + 40)], fill="#FEF3C7", outline="#D97706", width=2, radius=10)
    draw.text(((b3_x1 + b3_x2) // 2, b3_y1 + 20), "3. THỨ TỰ & PHÉP CỘNG", fill="#B45309", font=f_sub, anchor="mm")

    draw.text((b3_x1 + 12, b3_y1 + 55), "• Cộng cùng một số:", fill="#1E293B", font=f_sub)
    draw_rounded_box(draw, [(b3_x1 + 12, b3_y1 + 85), (b3_x2 - 12, b3_y1 + 155)], fill="#FFFFFF", outline="#D97706", width=1, radius=6)
    draw.text(((b3_x1 + b3_x2) // 2, b3_y1 + 105), "Nếu a < b", fill="#B45309", font=f_node, anchor="mm")
    draw.text(((b3_x1 + b3_x2) // 2, b3_y1 + 135), "thì a + c < b + c", fill="#DC2626", font=f_node, anchor="mm")
    draw.text((b3_x1 + 12, b3_y1 + 175), "• Kết luận quan trọng:", fill="#1E293B", font=f_sub)
    draw.text((b3_x1 + 16, b3_y1 + 205), "Bất đẳng thức MỚI", fill="#B45309", font=f_node)
    draw.text((b3_x1 + 16, b3_y1 + 235), "CÙNG CHIỀU với BĐT cũ", fill="#16A34A", font=f_node)
    draw.text((b3_x1 + 12, b3_y1 + 270), "• Tương tự với phép trừ:", fill="#1E293B", font=f_text)
    draw.text((b3_x1 + 20, b3_y1 + 295), "a < b thì a - c < b - c", fill="#1E293B", font=f_text)

    # Nhánh 4: Thứ tự & Phép nhân
    b4_x1, b4_y1, b4_x2, b4_y2 = 795, 170, 1030, 485
    draw.line([(630, 125), (912, 170)], fill="#7C3AED", width=2)
    draw_rounded_box(draw, [(b4_x1, b4_y1), (b4_x2, b4_y2)], fill="#FAF5FF", outline="#7C3AED", width=2, radius=10)
    draw_rounded_box(draw, [(b4_x1, b4_y1), (b4_x2, b4_y2 + 40)], fill="#F3E8FF", outline="#7C3AED", width=2, radius=10)
    draw.text(((b4_x1 + b4_x2) // 2, b4_y1 + 20), "4. THỨ TỰ & PHÉP NHÂN", fill="#6D28D9", font=f_sub, anchor="mm")

    draw.text((b4_x1 + 12, b4_y1 + 55), "• Nhân với SỐ DƯƠNG (c > 0):", fill="#15803D", font=f_sub)
    draw.text((b4_x1 + 20, b4_y1 + 80), "a < b thì ac < bc", fill="#15803D", font=f_node)
    draw.text((b4_x1 + 20, b4_y1 + 105), "→ CÙNG CHIỀU", fill="#15803D", font=f_sub)

    draw.line([(b4_x1 + 15, b4_y1 + 135), (b4_x2 - 15, b4_y1 + 135)], fill="#DDD6FE", width=1)

    draw.text((b4_x1 + 12, b4_y1 + 150), "• Nhân với SỐ ÂM (c < 0):", fill="#B91C1C", font=f_sub)
    draw.text((b4_x1 + 20, b4_y1 + 175), "a < b thì ac > bc", fill="#B91C1C", font=f_node)
    draw.text((b4_x1 + 20, b4_y1 + 200), "→ ĐỔI CHIỀU (ngược chiều)", fill="#B91C1C", font=f_sub)

    draw.line([(b4_x1 + 15, b4_y1 + 230), (b4_x2 - 15, b4_y1 + 230)], fill="#DDD6FE", width=1)
    draw.text((b4_x1 + 12, b4_y1 + 245), "• Lưu ý với phép chia:", fill="#1E293B", font=f_text)
    draw.text((b4_x1 + 16, b4_y1 + 270), "Chia tương đương nhân với 1/c", fill="#4B5563", font=f_text)

    out_file = os.path.join(OUT_DIR, "mindmap_toan9_chuong2_bai5.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Exported: {out_file}")

# ==============================================================================
# 2. SƠ ĐỒ TƯ DUY CHO BÀI 04: TỔNG HỢP TOÀN BỘ CHƯƠNG II
# ==============================================================================
def draw_mindmap_toan9_chuong2_tong_hop():
    w, h = 1050, 530
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(21, bold=True)
    f_node = get_font(16, bold=True)
    f_sub = get_font(14, bold=True)
    f_text = get_font(13, bold=False)

    # Tiêu đề
    draw.text((w // 2, 25), "SƠ ĐỒ TƯ DUY: TỔNG HỢP KIẾN THỨC CHƯƠNG II - ĐẠI SỐ 9", fill="#1E3A8A", font=f_title, anchor="mm")

    # Trung tâm
    draw_rounded_box(draw, [(300, 65), (750, 125)], fill="#DBEAFE", outline="#1D4ED8", width=3, radius=12)
    draw.text((525, 85), "CHƯƠNG II: BẤT ĐẲNG THỨC & BẤT PHƯƠNG TRÌNH", fill="#1E3A8A", font=f_node, anchor="mm")
    draw.text((525, 108), "Bất đẳng thức • Bất phương trình bậc nhất 1 ẩn • Ứng dụng thực tế", fill="#1D4ED8", font=f_text, anchor="mm")

    # 4 Nhánh
    # Nhánh 1: Bất đẳng thức & Tính chất
    b1_x1, b1_y1, b1_x2, b1_y2 = 25, 170, 260, 495
    draw.line([(410, 125), (142, 170)], fill="#2563EB", width=2)
    draw_rounded_box(draw, [(b1_x1, b1_y1), (b1_x2, b1_y2)], fill="#EFF6FF", outline="#2563EB", width=2, radius=10)
    draw_rounded_box(draw, [(b1_x1, b1_y1), (b1_x2, b1_y1 + 40)], fill="#DBEAFE", outline="#2563EB", width=2, radius=10)
    draw.text(((b1_x1 + b1_x2) // 2, b1_y1 + 20), "1. BẤT ĐẲNG THỨC", fill="#1D4ED8", font=f_sub, anchor="mm")

    draw.text((b1_x1 + 10, b1_y1 + 55), "• Khái niệm: a < b; a > b;", fill="#1E293B", font=f_text)
    draw.text((b1_x1 + 20, b1_y1 + 78), "a ≤ b; a ≥ b", fill="#0F766E", font=f_sub)
    draw.text((b1_x1 + 10, b1_y1 + 105), "• Tính chất bắc cầu:", fill="#1E293B", font=f_sub)
    draw.text((b1_x1 + 16, b1_y1 + 128), "a < b và b < c thì a < c", fill="#B91C1C", font=f_text)
    draw.text((b1_x1 + 10, b1_y1 + 155), "• Cộng cùng một số:", fill="#1E293B", font=f_sub)
    draw.text((b1_x1 + 16, b1_y1 + 178), "a < b thì a + c < b + c", fill="#15803D", font=f_text)
    draw.text((b1_x1 + 16, b1_y1 + 200), "(luôn CÙNG CHIỀU)", fill="#15803D", font=f_text)
    draw.text((b1_x1 + 10, b1_y1 + 230), "• Nhân với số dương (c > 0):", fill="#1E293B", font=f_sub)
    draw.text((b1_x1 + 16, b1_y1 + 253), "a < b thì ac < bc (cùng chiều)", fill="#2563EB", font=f_text)
    draw.text((b1_x1 + 10, b1_y1 + 280), "• Nhân với số âm (c < 0):", fill="#1E293B", font=f_sub)
    draw.text((b1_x1 + 16, b1_y1 + 303), "a < b thì ac > bc (ĐỔI CHIỀU)", fill="#DC2626", font=f_sub)

    # Nhánh 2: Khái niệm BPT bậc nhất 1 ẩn
    b2_x1, b2_y1, b2_x2, b2_y2 = 280, 170, 515, 495
    draw.line([(470, 125), (397, 170)], fill="#0D9488", width=2)
    draw_rounded_box(draw, [(b2_x1, b2_y1), (b2_x2, b2_y2)], fill="#F0FDFA", outline="#0D9488", width=2, radius=10)
    draw_rounded_box(draw, [(b2_x1, b2_y1), (b2_x2, b2_y1 + 40)], fill="#CCFBF1", outline="#0D9488", width=2, radius=10)
    draw.text(((b2_x1 + b2_x2) // 2, b2_y1 + 20), "2. BPT BẬC NHẤT 1 ẨN", fill="#0F766E", font=f_sub, anchor="mm")

    draw.text((b2_x1 + 10, b2_y1 + 55), "• Định nghĩa dạng chuẩn:", fill="#1E293B", font=f_sub)
    draw_rounded_box(draw, [(b2_x1 + 10, b2_y1 + 80), (b2_x2 - 10, b2_y1 + 145)], fill="#FFFFFF", outline="#0D9488", width=1, radius=6)
    draw.text(((b2_x1 + b2_x2) // 2, b2_y1 + 100), "ax + b < 0 (hoặc >, ≤, ≥)", fill="#0F766E", font=f_node, anchor="mm")
    draw.text(((b2_x1 + b2_x2) // 2, b2_y1 + 125), "với a, b cho trước (a ≠ 0)", fill="#DC2626", font=f_text, anchor="mm")
    draw.text((b2_x1 + 10, b2_y1 + 160), "• Nghiệm của BPT:", fill="#1E293B", font=f_sub)
    draw.text((b2_x1 + 16, b2_y1 + 185), "Giá trị x₀ làm cho khẳng", fill="#1F2937", font=f_text)
    draw.text((b2_x1 + 16, b2_y1 + 208), "định ax₀ + b < 0 là ĐÚNG.", fill="#15803D", font=f_text)
    draw.text((b2_x1 + 10, b2_y1 + 240), "• Giải một BPT:", fill="#1E293B", font=f_sub)
    draw.text((b2_x1 + 16, b2_y1 + 265), "Là tìm tất cả các nghiệm", fill="#1F2937", font=f_text)
    draw.text((b2_x1 + 16, b2_y1 + 288), "của bất phương trình đó.", fill="#1F2937", font=f_text)

    # Nhánh 3: Quy tắc giải BPT bậc nhất 1 ẩn
    b3_x1, b3_y1, b3_x2, b3_y2 = 535, 170, 775, 495
    draw.line([(580, 125), (655, 170)], fill="#D97706", width=2)
    draw_rounded_box(draw, [(b3_x1, b3_y1), (b3_x2, b3_y2)], fill="#FFFBEB", outline="#D97706", width=2, radius=10)
    draw_rounded_box(draw, [(b3_x1, b3_y1), (b3_x2, b3_y1 + 40)], fill="#FEF3C7", outline="#D97706", width=2, radius=10)
    draw.text(((b3_x1 + b3_x2) // 2, b3_y1 + 20), "3. QUY TẮC GIẢI BPT", fill="#B45309", font=f_sub, anchor="mm")

    draw.text((b3_x1 + 10, b3_y1 + 55), "• Quy tắc 1: CHUYỂN VẾ", fill="#B45309", font=f_sub)
    draw.text((b3_x1 + 16, b3_y1 + 80), "Chuyển hạng tử sang vế kia", fill="#1F2937", font=f_text)
    draw.text((b3_x1 + 16, b3_y1 + 102), "đồng thời ĐỔI DẤU hạng tử:", fill="#1F2937", font=f_text)
    draw.text((b3_x1 + 25, b3_y1 + 125), "ax + b < 0 chuyển vế ax < -b", fill="#DC2626", font=f_sub)

    draw.line([(b3_x1 + 12, b3_y1 + 155), (b3_x2 - 12, b3_y1 + 155)], fill="#FDE68A", width=1)

    draw.text((b3_x1 + 10, b3_y1 + 170), "• Quy tắc 2: NHÂN / CHIA", fill="#B45309", font=f_sub)
    draw.text((b3_x1 + 16, b3_y1 + 195), "1) Nếu a > 0: GIỮ NGUYÊN CHIỀU", fill="#15803D", font=f_sub)
    draw.text((b3_x1 + 25, b3_y1 + 218), "nghiệm: x < -b / a", fill="#15803D", font=f_node)
    draw.text((b3_x1 + 16, b3_y1 + 250), "2) Nếu a < 0: ĐỔI CHIỀU BPT", fill="#DC2626", font=f_sub)
    draw.text((b3_x1 + 25, b3_y1 + 273), "nghiệm: x > -b / a", fill="#DC2626", font=f_node)

    # Nhánh 4: Ứng dụng & Phương pháp
    b4_x1, b4_y1, b4_x2, b4_y2 = 795, 170, 1030, 495
    draw.line([(640, 125), (912, 170)], fill="#7C3AED", width=2)
    draw_rounded_box(draw, [(b4_x1, b4_y1), (b4_x2, b4_y2)], fill="#FAF5FF", outline="#7C3AED", width=2, radius=10)
    draw_rounded_box(draw, [(b4_x1, b4_y1), (b4_x2, b4_y2 + 40)], fill="#F3E8FF", outline="#7C3AED", width=2, radius=10)
    draw.text(((b4_x1 + b4_x2) // 2, b4_y1 + 20), "4. ỨNG DỤNG THỰC TIỄN", fill="#6D28D9", font=f_sub, anchor="mm")

    draw.text((b4_x1 + 10, b4_y1 + 55), "• Các bài toán thực tế:", fill="#6D28D9", font=f_sub)
    draw.text((b4_x1 + 16, b4_y1 + 80), "• Tốc độ giao thông (≤, ≥)", fill="#1F2937", font=f_text)
    draw.text((b4_x1 + 16, b4_y1 + 105), "• Chi phí, ngân sách tối đa", fill="#1F2937", font=f_text)
    draw.text((b4_x1 + 16, b4_y1 + 130), "• Lãi suất tiền gửi tiết kiệm", fill="#1F2937", font=f_text)
    draw.text((b4_x1 + 16, b4_y1 + 155), "• Điểm xét tuyển, chỉ tiêu", fill="#1F2937", font=f_text)

    draw.line([(b4_x1 + 12, b4_y1 + 185), (b4_x2 - 12, b4_y1 + 185)], fill="#DDD6FE", width=1)

    draw.text((b4_x1 + 10, b4_y1 + 200), "• Phương pháp 3 bước:", fill="#6D28D9", font=f_sub)
    draw.text((b4_x1 + 16, b4_y1 + 225), "B1: Chọn ẩn & lập BPT", fill="#1E293B", font=f_text)
    draw.text((b4_x1 + 16, b4_y1 + 250), "B2: Giải BPT tìm ẩn", fill="#1E293B", font=f_text)
    draw.text((b4_x1 + 16, b4_y1 + 275), "B3: Đối chiếu ĐK & kết luận", fill="#1E293B", font=f_text)

    out_file = os.path.join(OUT_DIR, "mindmap_toan9_chuong2_tong_hop.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Exported: {out_file}")

if __name__ == "__main__":
    draw_mindmap_toan9_bai5()
    draw_mindmap_toan9_chuong2_tong_hop()
    print("FINISHED UPDATING TOAN 9 MINDMAPS!")
