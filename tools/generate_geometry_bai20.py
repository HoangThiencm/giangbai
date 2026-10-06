# -*- coding: utf-8 -*-
"""
Tạo các hình vẽ hình học vector SVG độ nét cao cho Bài 20 Toán 6:
Chu vi và diện tích của một số tứ giác đã học (SGK Kết nối tri thức với cuộc sống).
Render tự động ra PNG 300 DPI qua PyMuPDF.
"""

import os
import pymupdf

OUT_DIR = os.path.abspath(r"TROLYTHIEN\engine\hinh_ve_sgk")
os.makedirs(OUT_DIR, exist_ok=True)

def render_svg_to_png(svg_str, out_png_path, dpi=200):
    doc = pymupdf.open(stream=svg_str.encode('utf-8'), filetype='svg')
    pix = doc[0].get_pixmap(dpi=dpi)
    pix.save(out_png_path)
    print(f"Rendered: {os.path.basename(out_png_path)} ({pix.width}x{pix.height})")

# 1. Hình 1: Bộ 3 hình cơ bản (Hình vuông, Hình chữ nhật, Hình thang)
svg_hinh_01 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 260" width="850" height="260">
  <rect width="850" height="260" fill="#FFFFFF"/>
  
  <!-- Khung Hình vuông -->
  <g transform="translate(30, 20)">
    <rect x="30" y="25" width="110" height="110" fill="#F8FAFC" stroke="#1E293B" stroke-width="2.2" rx="2"/>
    <!-- Góc vuông -->
    <path d="M 30,37 L 42,37 L 42,25" fill="none" stroke="#64748B" stroke-width="1.5"/>
    <text x="15" y="85" font-family="Times New Roman" font-size="20" font-style="italic" fill="#0F172A">a</text>
    <text x="80" y="155" font-family="Times New Roman" font-size="20" font-style="italic" fill="#0F172A">a</text>
    <text x="85" y="185" font-family="Times New Roman" font-size="18" font-weight="bold" fill="#1E3A8A" text-anchor="middle">Hình vuông</text>
    <text x="85" y="210" font-family="Times New Roman" font-size="17" fill="#334155" text-anchor="middle">C = 4a</text>
    <text x="85" y="233" font-family="Times New Roman" font-size="17" fill="#334155" text-anchor="middle">S = a²</text>
  </g>

  <!-- Khung Hình chữ nhật -->
  <g transform="translate(260, 20)">
    <rect x="20" y="35" width="170" height="100" fill="#F8FAFC" stroke="#1E293B" stroke-width="2.2" rx="2"/>
    <!-- Góc vuông -->
    <path d="M 20,47 L 32,47 L 32,35" fill="none" stroke="#64748B" stroke-width="1.5"/>
    <text x="5" y="90" font-family="Times New Roman" font-size="20" font-style="italic" fill="#0F172A">a</text>
    <text x="100" y="155" font-family="Times New Roman" font-size="20" font-style="italic" fill="#0F172A">b</text>
    <text x="105" y="185" font-family="Times New Roman" font-size="18" font-weight="bold" fill="#1E3A8A" text-anchor="middle">Hình chữ nhật</text>
    <text x="105" y="210" font-family="Times New Roman" font-size="17" fill="#334155" text-anchor="middle">C = 2(a + b)</text>
    <text x="105" y="233" font-family="Times New Roman" font-size="17" fill="#334155" text-anchor="middle">S = ab</text>
  </g>

  <!-- Khung Hình thang -->
  <g transform="translate(530, 20)">
    <polygon points="50,35 170,35 220,135 10,135" fill="#F8FAFC" stroke="#1E293B" stroke-width="2.2"/>
    <!-- Đường cao h -->
    <line x1="50" y1="35" x2="50" y2="135" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <path d="M 50,123 L 62,123 L 62,135" fill="none" stroke="#DC2626" stroke-width="1.5"/>
    <text x="56" y="90" font-family="Times New Roman" font-size="19" font-style="italic" fill="#DC2626">h</text>
    <!-- Nhãn các cạnh -->
    <text x="105" y="27" font-family="Times New Roman" font-size="20" font-style="italic" fill="#0F172A">a</text>
    <text x="110" y="155" font-family="Times New Roman" font-size="20" font-style="italic" fill="#0F172A">b</text>
    <text x="18" y="80" font-family="Times New Roman" font-size="19" font-style="italic" fill="#0F172A">c</text>
    <text x="202" y="80" font-family="Times New Roman" font-size="19" font-style="italic" fill="#0F172A">d</text>
    <text x="115" y="185" font-family="Times New Roman" font-size="18" font-weight="bold" fill="#1E3A8A" text-anchor="middle">Hình thang</text>
    <text x="115" y="210" font-family="Times New Roman" font-size="17" fill="#334155" text-anchor="middle">C = a + b + c + d</text>
    <text x="115" y="233" font-family="Times New Roman" font-size="17" fill="#334155" text-anchor="middle">S = ½(a + b)h</text>
  </g>
</svg>"""

# 2. Hình 2: Luyện tập 1.3 - Thửa ruộng kết hợp hình thang và hình chữ nhật
svg_hinh_02 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 280" width="520" height="280">
  <rect width="520" height="280" fill="#FFFFFF"/>
  <g transform="translate(60, 20)">
    <!-- Hình thang phía trên -->
    <polygon points="70,20 270,20 330,120 10,120" fill="#ECFDF5" stroke="#059669" stroke-width="2.2"/>
    <!-- Đường cao hình thang -->
    <line x1="70" y1="20" x2="70" y2="120" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <path d="M 70,108 L 82,108 L 82,120" fill="none" stroke="#DC2626" stroke-width="1.5"/>
    <text x="76" y="75" font-family="Times New Roman" font-size="17" fill="#DC2626">10 m</text>
    <text x="155" y="14" font-family="Times New Roman" font-size="18" font-weight="bold" fill="#0F172A">30 m</text>
    
    <!-- Hình chữ nhật phía dưới -->
    <rect x="10" y="120" width="320" height="100" fill="#F0FDF4" stroke="#059669" stroke-width="2.2"/>
    <!-- Cạnh đáy và cạnh bên HCN -->
    <text x="150" y="245" font-family="Times New Roman" font-size="18" font-weight="bold" fill="#0F172A">50 m</text>
    <text x="-40" y="175" font-family="Times New Roman" font-size="17" fill="#0F172A">15 m</text>
    
    <!-- Mũi tên chỉ kích thước chiều rộng 15m -->
    <line x1="-5" y1="120" x2="-5" y2="220" stroke="#64748B" stroke-width="1.2"/>
    <path d="M -5,120 L -2,128 M -5,120 L -8,128" stroke="#64748B" stroke-width="1.2"/>
    <path d="M -5,220 L -2,212 M -5,220 L -8,212" stroke="#64748B" stroke-width="1.2"/>

    <text x="170" y="175" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#047857" text-anchor="middle">Hình chữ nhật</text>
    <text x="170" y="75" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#047857" text-anchor="middle">Hình thang</text>
  </g>
</svg>"""

# 3. Hình 3: Cắt ghép hình bình hành thành hình chữ nhật (HĐ1, HĐ2)
svg_hinh_03 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 230" width="760" height="230">
  <rect width="760" height="230" fill="#FFFFFF"/>
  
  <!-- Hình bình hành ban đầu -->
  <g transform="translate(30, 25)">
    <polygon points="50,20 220,20 170,140 0,140" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.2"/>
    <!-- Đường cao cắt tam giác -->
    <line x1="50" y1="20" x2="50" y2="140" stroke="#DC2626" stroke-width="2" stroke-dasharray="4,3"/>
    <path d="M 50,128 L 62,128 L 62,140" fill="none" stroke="#DC2626" stroke-width="1.5"/>
    <polygon points="50,20 50,140 0,140" fill="#DBEAFE" stroke="#2563EB" stroke-width="1.8"/>
    
    <text x="56" y="85" font-family="Times New Roman" font-size="19" font-style="italic" fill="#DC2626">h</text>
    <text x="100" y="165" font-family="Times New Roman" font-size="20" font-style="italic" fill="#0F172A">a</text>
    <text x="110" y="195" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#1E40AF" text-anchor="middle">Hình bình hành (S = ah)</text>
  </g>

  <!-- Mũi tên chuyển đổi -->
  <g transform="translate(310, 85)">
    <path d="M 10,25 L 80,25" stroke="#475569" stroke-width="3" stroke-linecap="round"/>
    <polygon points="80,18 95,25 80,32" fill="#475569"/>
    <text x="50" y="12" font-family="Times New Roman" font-size="15" fill="#475569" text-anchor="middle">Cắt &amp; Ghép</text>
  </g>

  <!-- Hình chữ nhật sau khi ghép -->
  <g transform="translate(450, 25)">
    <rect x="50" y="20" width="170" height="120" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.2"/>
    <!-- Tam giác ghép vào bên phải -->
    <polygon points="220,20 220,140 170,140" fill="#DBEAFE" stroke="#2563EB" stroke-width="1.8"/>
    <!-- Góc vuông -->
    <path d="M 50,32 L 62,32 L 62,20" fill="none" stroke="#64748B" stroke-width="1.5"/>
    
    <text x="32" y="85" font-family="Times New Roman" font-size="19" font-style="italic" fill="#DC2626">h</text>
    <text x="130" y="165" font-family="Times New Roman" font-size="20" font-style="italic" fill="#0F172A">a</text>
    <text x="135" y="195" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#1E40AF" text-anchor="middle">Hình chữ nhật (S = ah)</text>
  </g>
</svg>"""

# 4. Hình 4: Cắt ghép hình thoi thành hình chữ nhật (HĐ3, HĐ4)
svg_hinh_04 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 240" width="760" height="240">
  <rect width="760" height="240" fill="#FFFFFF"/>

  <!-- Hình thoi ban đầu -->
  <g transform="translate(40, 25)">
    <polygon points="120,10 230,85 120,160 10,85" fill="#FAF5FF" stroke="#7C3AED" stroke-width="2.2"/>
    <!-- 2 đường chéo -->
    <line x1="10" y1="85" x2="230" y2="85" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <line x1="120" y1="10" x2="120" y2="160" stroke="#2563EB" stroke-width="1.8" stroke-dasharray="4,3"/>
    
    <text x="125" y="75" font-family="Times New Roman" font-size="19" font-style="italic" fill="#DC2626">a</text>
    <text x="130" y="140" font-family="Times New Roman" font-size="19" font-style="italic" fill="#2563EB">b</text>
    <text x="120" y="195" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#6D28D9" text-anchor="middle">Hình thoi (S = ½ab)</text>
  </g>

  <!-- Mũi tên chuyển đổi -->
  <g transform="translate(320, 85)">
    <path d="M 10,25 L 80,25" stroke="#475569" stroke-width="3" stroke-linecap="round"/>
    <polygon points="80,18 95,25 80,32" fill="#475569"/>
    <text x="50" y="12" font-family="Times New Roman" font-size="15" fill="#475569" text-anchor="middle">Cắt &amp; Ghép</text>
  </g>

  <!-- Hình chữ nhật ghép từ các phần của hình thoi -->
  <g transform="translate(470, 25)">
    <rect x="20" y="45" width="220" height="75" fill="#FAF5FF" stroke="#7C3AED" stroke-width="2.2"/>
    <line x1="130" y1="45" x2="130" y2="120" stroke="#64748B" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="20" y1="45" x2="130" y2="120" stroke="#7C3AED" stroke-width="1.8"/>
    <line x1="130" y1="45" x2="240" y2="120" stroke="#7C3AED" stroke-width="1.8"/>

    <text x="125" y="35" font-family="Times New Roman" font-size="19" font-style="italic" fill="#DC2626">a</text>
    <text x="250" y="85" font-family="Times New Roman" font-size="19" font-style="italic" fill="#2563EB">b/2</text>
    <text x="130" y="195" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#6D28D9" text-anchor="middle">Hình chữ nhật (S = a · (b/2) = ½ab)</text>
  </g>
</svg>"""

# 5. Hình 5: Luyện tập 2 - Mảnh đất chia thành hoa AMCN và cỏ
svg_hinh_05 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 280" width="540" height="280">
  <rect width="540" height="280" fill="#FFFFFF"/>
  <g transform="translate(70, 30)">
    <!-- Hình chữ nhật ABCD -->
    <rect x="30" y="20" width="360" height="180" fill="#F8FAFC" stroke="#1E293B" stroke-width="2.2"/>
    
    <!-- Phần trồng hoa: Hình bình hành AMCN (tô màu tím pastel) -->
    <polygon points="30,200 210,20 390,20 210,200" fill="#FDF2F8" stroke="#DB2777" stroke-width="2.5"/>
    <!-- Phần trồng cỏ: Tam giác ABM và CDN (tô màu xanh lá nhạt) -->
    <polygon points="30,20 210,20 30,200" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.8"/>
    <polygon points="210,200 390,20 390,200" fill="#F0FDF4" stroke="#16A34A" stroke-width="1.8"/>

    <!-- Tên các đỉnh -->
    <text x="12" y="22" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">B</text>
    <text x="205" y="14" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">M</text>
    <text x="400" y="22" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">C</text>
    <text x="12" y="215" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">A</text>
    <text x="205" y="225" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">N</text>
    <text x="400" y="215" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">D</text>

    <!-- Số đo kích thước -->
    <text x="110" y="14" font-family="Times New Roman" font-size="17" fill="#0F172A">6 m</text>
    <text x="295" y="14" font-family="Times New Roman" font-size="17" fill="#0F172A">6 m</text>
    <text x="110" y="225" font-family="Times New Roman" font-size="17" fill="#0F172A">6 m</text>
    <text x="295" y="225" font-family="Times New Roman" font-size="17" fill="#0F172A">6 m</text>
    <text x="-15" y="115" font-family="Times New Roman" font-size="17" fill="#0F172A">10 m</text>

    <!-- Nhãn khu vực -->
    <text x="250" y="115" font-family="Times New Roman" font-size="16" font-weight="bold" fill="#BE185D" text-anchor="middle">Trồng hoa (AMCN)</text>
    <text x="90" y="75" font-family="Times New Roman" font-size="15" fill="#15803D">Cỏ</text>
    <text x="330" y="150" font-family="Times New Roman" font-size="15" fill="#15803D">Cỏ</text>
  </g>
</svg>"""

# 6. Hình 6: Luyện tập 3 - Mảnh vườn chữ nhật có luống hoa hình thoi
svg_hinh_06 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 260" width="520" height="260">
  <rect width="520" height="260" fill="#FFFFFF"/>
  <g transform="translate(60, 20)">
    <!-- Mảnh vườn hình chữ nhật -->
    <rect x="20" y="20" width="360" height="180" fill="#F8FAFC" stroke="#1E293B" stroke-width="2.2"/>
    <!-- Luống hoa hình thoi ở giữa -->
    <polygon points="200,20 380,110 200,200 20,110" fill="#FFF1F2" stroke="#E11D48" stroke-width="2.5"/>
    
    <!-- Kích thước -->
    <text x="195" y="225" font-family="Times New Roman" font-size="18" font-weight="bold" fill="#0F172A" text-anchor="middle">8 m</text>
    <text x="-12" y="115" font-family="Times New Roman" font-size="18" font-weight="bold" fill="#0F172A" text-anchor="middle">5 m</text>
    
    <text x="200" y="115" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#BE123C" text-anchor="middle">Luống hoa hình thoi</text>
  </g>
</svg>"""

# 7. Hình 7: Bài 4.20 - Mặt sàn nhà
svg_hinh_07 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 320" width="540" height="320">
  <rect width="540" height="320" fill="#FFFFFF"/>
  <g transform="translate(50, 25)">
    <!-- Phòng khách 6 x 8 -->
    <rect x="20" y="20" width="220" height="150" fill="#EFF6FF" stroke="#1E3A8A" stroke-width="2.2"/>
    <text x="130" y="85" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#1E3A8A" text-anchor="middle">Phòng khách</text>
    <text x="130" y="110" font-family="Times New Roman" font-size="16" fill="#3B82F6" text-anchor="middle">6 m × 8 m</text>

    <!-- Phòng ăn và bếp 6 x 6 -->
    <rect x="240" y="20" width="180" height="150" fill="#FEF3C7" stroke="#B45309" stroke-width="2.2"/>
    <text x="330" y="85" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#B45309" text-anchor="middle">Phòng ăn và bếp</text>
    <text x="330" y="110" font-family="Times New Roman" font-size="16" fill="#D97706" text-anchor="middle">6 m × 6 m</text>

    <!-- Hành lang 2 x 12 (trên bản vẽ: 2m x 12m) -->
    <rect x="20" y="170" width="340" height="60" fill="#F1F5F9" stroke="#475569" stroke-width="2.2"/>
    <text x="190" y="205" font-family="Times New Roman" font-size="16" font-weight="bold" fill="#334155" text-anchor="middle">Hành lang (2 m × 12 m)</text>

    <!-- WC 2 x 2 -->
    <rect x="360" y="170" width="60" height="60" fill="#E0F2FE" stroke="#0369A1" stroke-width="2.2"/>
    <text x="390" y="200" font-family="Times New Roman" font-size="14" font-weight="bold" fill="#0369A1" text-anchor="middle">WC</text>
    <text x="390" y="218" font-family="Times New Roman" font-size="13" fill="#0284C7" text-anchor="middle">2×2</text>
  </g>
</svg>"""

# 8. Hình 8: Bài 4.21 - Thửa đất hình thang vuông ABCD
svg_hinh_08 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 260" width="520" height="260">
  <rect width="520" height="260" fill="#FFFFFF"/>
  <g transform="translate(60, 20)">
    <!-- Hình thang ABCD vuông tại D: A(40,20), B(190,20), C(370,180), D(40,180) -->
    <!-- Điểm E là chân đường vuông góc từ B xuống DC: E(190, 180) -->
    <polygon points="40,20 190,20 370,180 40,180" fill="#F8FAFC" stroke="#1E293B" stroke-width="2.2"/>
    
    <!-- Đường thẳng BE chia hình chữ nhật ABED và tam giác BEC -->
    <line x1="190" y1="20" x2="190" y2="180" stroke="#2563EB" stroke-width="1.8" stroke-dasharray="4,3"/>
    
    <!-- Góc vuông tại D, E -->
    <path d="M 40,168 L 52,168 L 52,180" fill="none" stroke="#64748B" stroke-width="1.5"/>
    <path d="M 190,168 L 202,168 L 202,180" fill="none" stroke="#64748B" stroke-width="1.5"/>

    <!-- Tên các đỉnh -->
    <text x="25" y="18" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">A</text>
    <text x="195" y="18" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">B</text>
    <text x="380" y="190" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">C</text>
    <text x="22" y="195" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">D</text>
    <text x="185" y="202" font-family="Times New Roman" font-size="20" font-weight="bold" font-style="italic" fill="#0F172A">E</text>

    <!-- Kích thước -->
    <text x="115" y="14" font-family="Times New Roman" font-size="17" fill="#0F172A" text-anchor="middle">10 m</text>
    <text x="205" y="225" font-family="Times New Roman" font-size="17" font-weight="bold" fill="#0F172A" text-anchor="middle">DC = 25 m</text>

    <!-- Ghi chú diện tích ABED -->
    <text x="115" y="105" font-family="Times New Roman" font-size="16" font-weight="bold" fill="#1E40AF" text-anchor="middle">S(ABED) = 150 m²</text>
  </g>
</svg>"""

all_figures = [
    (svg_hinh_01, "hinh_01_cong_thuc_3_hinh.png"),
    (svg_hinh_02, "hinh_02_thua_ruong_luyentap1.png"),
    (svg_hinh_03, "hinh_03_cat_ghep_hinh_binh_hanh.png"),
    (svg_hinh_04, "hinh_04_cat_ghep_hinh_thoi.png"),
    (svg_hinh_05, "hinh_05_luyen_tap_2_manh_dat.png"),
    (svg_hinh_06, "hinh_06_luyen_tap_3_manh_vuon_hinh_thoi.png"),
    (svg_hinh_07, "hinh_07_bai_4_20_mat_san_nha.png"),
    (svg_hinh_08, "hinh_08_bai_4_21_thua_dat_hinh_thang.png"),
]

for svg_code, fname in all_figures:
    p = os.path.join(OUT_DIR, fname)
    render_svg_to_png(svg_code, p)

print("ĐÃ XUẤT THÀNH CÔNG TẤT CẢ HÌNH VẼ HÌNH HỌC BÀI 20!")
