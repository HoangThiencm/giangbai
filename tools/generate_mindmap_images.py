# -*- coding: utf-8 -*-
"""
Script vẽ Sơ đồ tư duy dạng PNG chuẩn sắc nét (300 DPI) cho các bài ôn tập / luyện tập chung Toán 6.
Sử dụng PIL để vẽ vector shape và render text tiếng Việt bằng font Times New Roman / Arial.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.abspath(r"TROLYTHIEN\engine\hinh_ve_sgk")
os.makedirs(OUT_DIR, exist_ok=True)

# Lựa chọn font
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

def draw_arrow(draw, start, end, color="#2563EB", width=2):
    draw.line([start, end], fill=color, width=width)

# ==============================================================================
# 1. SƠ ĐỒ TƯ DUY BÀI 1: LUYỆN TẬP CHUNG - THỨ TỰ THỰC HIỆN CÁC PHÉP TÍNH (TIẾT 12)
# ==============================================================================
def draw_mindmap_01():
    w, h = 1000, 480
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_node = get_font(18, bold=True)
    f_text = get_font(15, bold=False)
    f_sub = get_font(14, bold=False)

    # Tiêu đề trên cùng
    draw.text((w//2, 25), "SƠ ĐỒ TƯ DUY: THỨ TỰ THỰC HIỆN CÁC PHÉP TÍNH", fill="#1E3A8A", font=f_title, anchor="mm")

    # Nút trung tâm
    c_x, c_y = 500, 100
    draw_rounded_box(draw, [(360, 75), (640, 130)], fill="#DBEAFE", outline="#1D4ED8", width=3, radius=12)
    draw.text((c_x, c_y), "BIỂU THỨC SỐ", fill="#1E3A8A", font=f_node, anchor="mm")

    # Nhánh 1: Biểu thức không có dấu ngoặc
    b1_x1, b1_y1, b1_x2, b1_y2 = 60, 200, 470, 440
    draw.line([(430, 130), (265, 200)], fill="#2563EB", width=3)
    draw_rounded_box(draw, [(b1_x1, b1_y1), (b1_x2, b1_y2)], fill="#F8FAFC", outline="#3B82F6", width=2, radius=10)
    
    # Header Nhánh 1
    draw_rounded_box(draw, [(b1_x1, b1_y1), (b1_x2, b1_y1 + 45)], fill="#EFF6FF", outline="#3B82F6", width=2, radius=10)
    draw.text(((b1_x1+b1_x2)//2, b1_y1 + 22), "1. BIỂU THỨC KHÔNG CÓ NGOẶC", fill="#1D4ED8", font=f_node, anchor="mm")
    
    draw.text((b1_x1 + 20, b1_y1 + 65), "• Chỉ có phép cộng, trừ (hoặc nhân, chia):", fill="#1E293B", font=f_node)
    draw.text((b1_x1 + 40, b1_y1 + 95), "→ Thực hiện từ TRÁI sang PHẢI.", fill="#0F766E", font=f_text)
    
    draw.text((b1_x1 + 20, b1_y1 + 135), "• Có đầy đủ các phép tính:", fill="#1E293B", font=f_node)
    draw.text((b1_x1 + 40, b1_y1 + 165), "1. Lũy thừa trước", fill="#B91C1C", font=f_text)
    draw.text((b1_x1 + 40, b1_y1 + 195), "2. Nhân và chia", fill="#B91C1C", font=f_text)
    draw.text((b1_x1 + 40, b1_y1 + 225), "3. Cộng và trừ cuối cùng", fill="#B91C1C", font=f_text)

    # Nhánh 2: Biểu thức có dấu ngoặc
    b2_x1, b2_y1, b2_x2, b2_y2 = 530, 200, 940, 440
    draw.line([(570, 130), (735, 200)], fill="#D97706", width=3)
    draw_rounded_box(draw, [(b2_x1, b2_y1), (b2_x2, b2_y2)], fill="#FFFBEB", outline="#D97706", width=2, radius=10)
    
    # Header Nhánh 2
    draw_rounded_box(draw, [(b2_x1, b2_y1), (b2_x2, b2_y1 + 45)], fill="#FEF3C7", outline="#D97706", width=2, radius=10)
    draw.text(((b2_x1+b2_x2)//2, b2_y1 + 22), "2. BIỂU THỨC CÓ DẤU NGOẶC", fill="#B45309", font=f_node, anchor="mm")

    draw.text((b2_x1 + 20, b2_y1 + 65), "• Thứ tự ưu tiên giải các dấu ngoặc:", fill="#1E293B", font=f_node)
    
    draw_rounded_box(draw, [(b2_x1 + 40, b2_y1 + 105), (b2_x2 - 40, b2_y1 + 145)], fill="#FFFFFF", outline="#F59E0B", width=1, radius=6)
    draw.text(((b2_x1+b2_x2)//2, b2_y1 + 125), "Bước 1: Ngoặc tròn ( )", fill="#B45309", font=f_node, anchor="mm")

    draw.line([((b2_x1+b2_x2)//2, b2_y1 + 145), ((b2_x1+b2_x2)//2, b2_y1 + 165)], fill="#D97706", width=2)

    draw_rounded_box(draw, [(b2_x1 + 40, b2_y1 + 165), (b2_x2 - 40, b2_y1 + 205)], fill="#FFFFFF", outline="#F59E0B", width=1, radius=6)
    draw.text(((b2_x1+b2_x2)//2, b2_y1 + 185), "Bước 2: Ngoặc vuông [ ]", fill="#B45309", font=f_node, anchor="mm")

    draw.line([((b2_x1+b2_x2)//2, b2_y1 + 205), ((b2_x1+b2_x2)//2, b2_y1 + 225)], fill="#D97706", width=2)

    draw_rounded_box(draw, [(b2_x1 + 40, b2_y1 + 225), (b2_x2 - 40, b2_y1 + 265)], fill="#FFFFFF", outline="#F59E0B", width=1, radius=6)
    draw.text(((b2_x1+b2_x2)//2, b2_y1 + 245), "Bước 3: Ngoặc nhọn { }", fill="#B45309", font=f_node, anchor="mm")

    out_file = os.path.join(OUT_DIR, "mindmap_01_thu_tu_phep_tinh.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Exported: {out_file}")

# ==============================================================================
# 2. SƠ ĐỒ TƯ DUY BÀI 2: BÀI TẬP CUỐI CHƯƠNG I - TỔNG HỢP KIẾN THỨC CHƯƠNG I
# ==============================================================================
def draw_mindmap_02():
    w, h = 1000, 500
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_node = get_font(17, bold=True)
    f_text = get_font(14, bold=False)

    # Tiêu đề
    draw.text((w//2, 25), "SƠ ĐỒ TƯ DUY: HỆ THỐNG KIẾN THỨC CHƯƠNG I - SỐ TỰ NHIÊN", fill="#1E3A8A", font=f_title, anchor="mm")

    # Trung tâm
    draw_rounded_box(draw, [(370, 65), (630, 120)], fill="#DBEAFE", outline="#1D4ED8", width=3, radius=12)
    draw.text((500, 92), "CHƯƠNG I: TẬP HỢP SỐ TỰ NHIÊN", fill="#1E3A8A", font=f_node, anchor="mm")

    # 3 Nhánh lớn
    # Nhánh A: Tập hợp & Biểu diễn số
    draw.line([(420, 120), (180, 175)], fill="#2563EB", width=3)
    draw_rounded_box(draw, [(30, 175), (330, 460)], fill="#F0FDF4", outline="#16A34A", width=2, radius=10)
    draw_rounded_box(draw, [(30, 175), (330, 215)], fill="#DCFCE7", outline="#16A34A", width=2, radius=10)
    draw.text((180, 195), "1. TẬP HỢP & GHI SỐ", fill="#15803D", font=f_node, anchor="mm")
    draw.text((45, 230), "• Ký hiệu tập hợp: A = {a, b, c}", fill="#1F2937", font=f_text)
    draw.text((45, 260), "• Phần tử: a ∈ A, d ∉ A", fill="#1F2937", font=f_text)
    draw.text((45, 290), "• Tập số tự nhiên: ℕ = {0; 1; 2; ...}", fill="#1F2937", font=f_text)
    draw.text((45, 320), "• Tập số khác 0: ℕ* = {1; 2; 3; ...}", fill="#1F2937", font=f_text)
    draw.text((45, 350), "• Hệ thập phân: Các lớp, hàng", fill="#1F2937", font=f_text)
    draw.text((45, 380), "• Chữ số La Mã: I, V, X, L, C...", fill="#1F2937", font=f_text)
    draw.text((45, 410), "• Biểu diễn trên tia số", fill="#1F2937", font=f_text)

    # Nhánh B: Các phép toán trên ℕ
    draw.line([(500, 120), (500, 175)], fill="#2563EB", width=3)
    draw_rounded_box(draw, [(350, 175), (650, 460)], fill="#EFF6FF", outline="#2563EB", width=2, radius=10)
    draw_rounded_box(draw, [(350, 175), (650, 215)], fill="#DBEAFE", outline="#2563EB", width=2, radius=10)
    draw.text((500, 195), "2. CÁC PHÉP TOÁN TRÊN ℕ", fill="#1D4ED8", font=f_node, anchor="mm")
    draw.text((365, 230), "• Cộng & Trừ: Giao hoán, kết hợp", fill="#1F2937", font=f_text)
    draw.text((365, 260), "• Nhân & Chia hết: a = b · q", fill="#1F2937", font=f_text)
    draw.text((365, 290), "• Phép chia có dư: a = b · q + r", fill="#1F2937", font=f_text)
    draw.text((385, 315), "(với 0 < r < b)", fill="#4B5563", font=f_text)
    draw.text((365, 345), "• Lũy thừa với số mũ tự nhiên:", fill="#1F2937", font=f_text)
    draw.text((385, 370), "aⁿ = a · a · ... · a (n thừa số)", fill="#0369A1", font=f_text)
    draw.text((365, 400), "• Nhân 2 lũy thừa: aᵐ · aⁿ = aᵐ⁺ⁿ", fill="#1F2937", font=f_text)
    draw.text((365, 430), "• Chia 2 lũy thừa: aᵐ : aⁿ = aᵐ⁻ⁿ", fill="#1F2937", font=f_text)

    # Nhánh C: Thứ tự thực hiện phép tính
    draw.line([(580, 120), (820, 175)], fill="#2563EB", width=3)
    draw_rounded_box(draw, [(670, 175), (970, 460)], fill="#FFFBEB", outline="#D97706", width=2, radius=10)
    draw_rounded_box(draw, [(670, 175), (970, 215)], fill="#FEF3C7", outline="#D97706", width=2, radius=10)
    draw.text((820, 195), "3. THỨ TỰ PHÉP TÍNH", fill="#B45309", font=f_node, anchor="mm")
    draw.text((685, 230), "• Biểu thức không ngoặc:", fill="#1F2937", font=f_text)
    draw.text((705, 260), "1. Lũy thừa", fill="#DC2626", font=f_text)
    draw.text((705, 290), "2. Nhân, chia", fill="#DC2626", font=f_text)
    draw.text((705, 320), "3. Cộng, trừ", fill="#DC2626", font=f_text)
    draw.text((685, 360), "• Biểu thức có dấu ngoặc:", fill="#1F2937", font=f_text)
    draw.text((705, 390), "1. Ngoặc tròn ( )", fill="#B45309", font=f_text)
    draw.text((705, 415), "2. Ngoặc vuông [ ]", fill="#B45309", font=f_text)
    draw.text((705, 440), "3. Ngoặc nhọn { }", fill="#B45309", font=f_text)

    out_file = os.path.join(OUT_DIR, "mindmap_02_tong_hop_chuong_1.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Exported: {out_file}")

# ==============================================================================
# 3. SƠ ĐỒ TƯ DUY BÀI 6: LUYỆN TẬP CHUNG - SỐ NGUYÊN TỐ & THỪA SỐ NGUYÊN TỐ (TIẾT 20)
# ==============================================================================
def draw_mindmap_06():
    w, h = 1000, 480
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_node = get_font(17, bold=True)
    f_text = get_font(14, bold=False)

    # Tiêu đề
    draw.text((w//2, 25), "SƠ ĐỒ TƯ DUY: SỐ NGUYÊN TỐ - HỢP SỐ & PHÂN TÍCH RA THỪA SỐ NGUYÊN TỐ", fill="#1E3A8A", font=f_title, anchor="mm")

    # Trung tâm
    draw_rounded_box(draw, [(360, 65), (640, 120)], fill="#DBEAFE", outline="#1D4ED8", width=3, radius=12)
    draw.text((500, 92), "SỐ TỰ NHIÊN (LỚN HƠN 1)", fill="#1E3A8A", font=f_node, anchor="mm")

    # Nhánh Trái: Phân loại số
    draw.line([(430, 120), (250, 175)], fill="#2563EB", width=3)
    draw_rounded_box(draw, [(50, 175), (460, 440)], fill="#F8FAFC", outline="#3B82F6", width=2, radius=10)
    draw_rounded_box(draw, [(50, 175), (460, 215)], fill="#EFF6FF", outline="#3B82F6", width=2, radius=10)
    draw.text((255, 195), "1. PHÂN LOẠI SỐ TỰ NHIÊN > 1", fill="#1D4ED8", font=f_node, anchor="mm")

    # Số nguyên tố
    draw_rounded_box(draw, [(70, 230), (440, 310)], fill="#FEF2F2", outline="#EF4444", width=2, radius=8)
    draw.text((85, 245), "• SỐ NGUYÊN TỐ:", fill="#B91C1C", font=f_node)
    draw.text((85, 275), "Chỉ có 2 ước là 1 và chính nó (ví dụ: 2, 3, 5, 7, 11...).", fill="#1F2937", font=f_text)

    # Hợp số
    draw_rounded_box(draw, [(70, 325), (440, 405)], fill="#F0FDF4", outline="#22C55E", width=2, radius=8)
    draw.text((85, 340), "• HỢP SỐ:", fill="#15803D", font=f_node)
    draw.text((85, 370), "Có nhiều hơn 2 ước (ví dụ: 4, 6, 8, 9, 10...).", fill="#1F2937", font=f_text)
    
    draw.text((70, 415), "* Chú ý: Số 0 và số 1 không là số nguyên tố, không là hợp số.", fill="#64748B", font=f_text)

    # Nhánh Phải: Phân tích ra thừa số nguyên tố
    draw.line([(570, 120), (740, 175)], fill="#2563EB", width=3)
    draw_rounded_box(draw, [(520, 175), (950, 440)], fill="#FFFBEB", outline="#D97706", width=2, radius=10)
    draw_rounded_box(draw, [(520, 175), (950, 215)], fill="#FEF3C7", outline="#D97706", width=2, radius=10)
    draw.text((735, 195), "2. PHÂN TÍCH RA THỪA SỐ NGUYÊN TỐ", fill="#B45309", font=f_node, anchor="mm")

    # Cách 1: Sơ đồ cột
    draw.text((540, 230), "• Cách 1: Theo sơ đồ cột (dọc):", fill="#1E293B", font=f_node)
    draw.text((560, 255), "Chia số đã cho lần lượt cho các số nguyên tố", fill="#4B5563", font=f_text)
    draw.text((560, 275), "từ nhỏ đến lớn (2, 3, 5, 7...) đến khi thương bằng 1.", fill="#4B5563", font=f_text)

    # Cách 2: Sơ đồ cây
    draw.text((540, 310), "• Cách 2: Theo sơ đồ cây (nhánh):", fill="#1E293B", font=f_node)
    draw.text((560, 335), "Tách số thành tích hai thừa số bất kỳ,", fill="#4B5563", font=f_text)
    draw.text((560, 355), "tiếp tục tách cho đến khi tất cả các nhánh đều là số nguyên tố.", fill="#4B5563", font=f_text)

    # Kết quả
    draw_rounded_box(draw, [(540, 385), (930, 425)], fill="#FFFFFF", outline="#D97706", width=1, radius=6)
    draw.text((735, 405), "Viết tích các thừa số nguyên tố dưới dạng LŨY THỪA", fill="#B45309", font=f_node, anchor="mm")

    out_file = os.path.join(OUT_DIR, "mindmap_06_so_nguyen_to.png")
    img.save(out_file, "PNG", dpi=(300, 300))
    print(f"Exported: {out_file}")

if __name__ == "__main__":
    draw_mindmap_01()
    draw_mindmap_02()
    draw_mindmap_06()
    print("ALL MINDMAP IMAGES CREATED SUCCESSFULLY!")
