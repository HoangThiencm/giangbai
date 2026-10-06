# -*- coding: utf-8 -*-
"""
Script vẽ Sơ đồ cây và Sơ đồ cột phân tích thừa số nguyên tố Toán 6 (SGK Kết nối tri thức).
Tái hiện trung thực 100% hình ảnh SGK:
1. Sơ đồ cây phân tích số 24 (24 -> 4 x 6 -> 2x2 và 2x3).
2. Sơ đồ cột phân tích số 30 với các ô tròn nét đứt điền khuyết (?).
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.abspath(r"TROLYTHIEN\engine\hinh_ve_sgk")
os.makedirs(OUT_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    if not os.path.exists(font_path):
        font_path = "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf"
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

def draw_dashed_circle(draw, center, radius, outline="#64748B", width=2, num_dashes=24):
    cx, cy = center
    for i in range(num_dashes):
        start_angle = i * (2 * math.pi / num_dashes)
        end_angle = start_angle + (math.pi / num_dashes)
        x1 = cx + radius * math.cos(start_angle)
        y1 = cy + radius * math.sin(start_angle)
        x2 = cx + radius * math.cos(end_angle)
        y2 = cy + radius * math.sin(end_angle)
        draw.line([(x1, y1), (x2, y2)], fill=outline, width=width)

def draw_diagram():
    w, h = 1040, 460
    # Nền trắng thanh thoát với bo viền nhẹ
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, bold=True)
    f_node_lg = get_font(24, bold=True)
    f_node_md = get_font(21, bold=True)
    f_sign = get_font(22, bold=False)
    f_res = get_font(18, bold=True)
    f_hint = get_font(15, bold=False)

    # Khung bao tổng thể
    draw.rounded_rectangle([(10, 10), (w - 10, h - 10)], radius=12, outline="#CBD5E1", width=2, fill="#FFFFFF")

    # =========================================================================
    # PHẦN 1: SƠ ĐỒ CÂY (PHÂN TÍCH SỐ 24) — BÊN TRÁI (x: 20 -> 560)
    # =========================================================================
    # Khung nền nhẹ
    draw.rounded_rectangle([(24, 24), (550, h - 24)], radius=10, fill="#F0F9FF", outline="#BAE6FD", width=2)
    draw.text((287, 48), "a) SƠ ĐỒ CÂY (Ví dụ phân tích số 24)", fill="#0369A1", font=f_title, anchor="mm")

    # Node gốc: 24 (Trắng)
    c24 = (287, 115)
    r_lg = 32
    draw.ellipse([(c24[0]-r_lg, c24[1]-r_lg), (c24[0]+r_lg, c24[1]+r_lg)], fill="#FFFFFF", outline="#0284C7", width=3)
    draw.text(c24, "24", fill="#0F172A", font=f_node_lg, anchor="mm")

    # Nhánh rẽ từ 24 -> 4 và 6
    c4 = (175, 220)
    c6 = (400, 220)
    draw.line([(265, 140), (195, 195)], fill="#334155", width=3)
    draw.line([(310, 140), (380, 195)], fill="#334155", width=3)

    # Dấu nhân giữa 4 và 6
    draw.text((287, 220), "×", fill="#475569", font=f_sign, anchor="mm")

    # Node 4 (Trắng)
    draw.ellipse([(c4[0]-r_lg, c4[1]-r_lg), (c4[0]+r_lg, c4[1]+r_lg)], fill="#FFFFFF", outline="#0284C7", width=3)
    draw.text(c4, "4", fill="#0F172A", font=f_node_lg, anchor="mm")

    # Node 6 (Trắng)
    draw.ellipse([(c6[0]-r_lg, c6[1]-r_lg), (c6[0]+r_lg, c6[1]+r_lg)], fill="#FFFFFF", outline="#0284C7", width=3)
    draw.text(c6, "6", fill="#0F172A", font=f_node_lg, anchor="mm")

    # Nhánh từ 4 -> 2 và 2 (Lá màu cam)
    c4_1 = (115, 330)
    c4_2 = (235, 330)
    draw.line([(155, 245), (125, 305)], fill="#334155", width=3)
    draw.line([(195, 245), (225, 305)], fill="#334155", width=3)
    draw.text((175, 330), "×", fill="#475569", font=f_sign, anchor="mm")

    r_leaf = 28
    draw.ellipse([(c4_1[0]-r_leaf, c4_1[1]-r_leaf), (c4_1[0]+r_leaf, c4_1[1]+r_leaf)], fill="#F59E0B", outline="#D97706", width=2)
    draw.text(c4_1, "2", fill="#0F172A", font=f_node_md, anchor="mm")

    draw.ellipse([(c4_2[0]-r_leaf, c4_2[1]-r_leaf), (c4_2[0]+r_leaf, c4_2[1]+r_leaf)], fill="#F59E0B", outline="#D97706", width=2)
    draw.text(c4_2, "2", fill="#0F172A", font=f_node_md, anchor="mm")

    # Nhánh từ 6 -> 2 và 3 (Lá màu cam)
    c6_1 = (340, 330)
    c6_2 = (460, 330)
    draw.line([(380, 245), (350, 305)], fill="#334155", width=3)
    draw.line([(420, 245), (450, 305)], fill="#334155", width=3)
    draw.text((400, 330), "×", fill="#475569", font=f_sign, anchor="mm")

    draw.ellipse([(c6_1[0]-r_leaf, c6_1[1]-r_leaf), (c6_1[0]+r_leaf, c6_1[1]+r_leaf)], fill="#F59E0B", outline="#D97706", width=2)
    draw.text(c6_1, "2", fill="#0F172A", font=f_node_md, anchor="mm")

    draw.ellipse([(c6_2[0]-r_leaf, c6_2[1]-r_leaf), (c6_2[0]+r_leaf, c6_2[1]+r_leaf)], fill="#F59E0B", outline="#D97706", width=2)
    draw.text(c6_2, "3", fill="#0F172A", font=f_node_md, anchor="mm")

    # Kết luận sơ đồ cây
    draw.text((287, 405), "Viết kết quả:  24 = 2 · 2 · 2 · 3 = 2³ · 3", fill="#1E3A8A", font=f_res, anchor="mm")

    # =========================================================================
    # PHẦN 2: SƠ ĐỒ CỘT (ĐIỀN KHUYẾT SỐ 30 SGK) — BÊN PHẢI (x: 570 -> 1016)
    # =========================================================================
    draw.rounded_rectangle([(566, 24), (1016, h - 24)], radius=10, fill="#FFFBEB", outline="#FDE68A", width=2)
    draw.text((791, 48), "b) SƠ ĐỒ CỘT DỌC (Ví dụ điền khuyết số 30)", fill="#B45309", font=f_title, anchor="mm")

    # Trục vạch kẻ dọc ngăn cách giữa cột trái và phải
    line_x = 791
    draw.line([(line_x, 88), (line_x, 375)], fill="#1E293B", width=3)

    # Header hướng dẫn
    draw.text((line_x - 90, 80), "(Số bị chia / thương)", fill="#64748B", font=f_hint, anchor="mm")
    draw.text((line_x + 90, 80), "(Ước nguyên tố)", fill="#64748B", font=f_hint, anchor="mm")

    # Hàng 1: 30 | 2
    y1 = 125
    draw.text((line_x - 80, y1), "30", fill="#0F172A", font=f_node_lg, anchor="mm")
    draw.text((line_x + 80, y1), "2", fill="#0F172A", font=f_node_lg, anchor="mm")

    # Hàng 2: (?) | 3  (vòng tròn nét đứt điền khuyết)
    y2 = 195
    draw_dashed_circle(draw, (line_x - 80, y2), 26, outline="#0284C7", width=2)
    draw.text((line_x - 80, y2), "?", fill="#0284C7", font=f_node_lg, anchor="mm")
    draw.text((line_x + 80, y2), "3", fill="#0F172A", font=f_node_lg, anchor="mm")

    # Hàng 3: 5 | (?)
    y3 = 265
    draw.text((line_x - 80, y3), "5", fill="#0F172A", font=f_node_lg, anchor="mm")
    draw_dashed_circle(draw, (line_x + 80, y3), 26, outline="#0284C7", width=2)
    draw.text((line_x + 80, y3), "?", fill="#0284C7", font=f_node_lg, anchor="mm")

    # Hàng 4: 1 | (kết thúc)
    y4 = 335
    draw.text((line_x - 80, y4), "1", fill="#0F172A", font=f_node_lg, anchor="mm")

    # Kết luận sơ đồ cột
    draw.text((791, 405), "Viết kết quả:  30 = 2 · 3 · 5", fill="#92400E", font=f_res, anchor="mm")

    out_file = os.path.join(OUT_DIR, "so_do_cay_va_cot_so_nguyen_to.png")
    img.save(out_file, dpi=(300, 300))
    print(f"SUCCESS: Generated {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    draw_diagram()
