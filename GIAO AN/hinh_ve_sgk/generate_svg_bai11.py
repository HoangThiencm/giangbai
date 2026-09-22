import os
import sys
import math
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, QSize

app = QGuiApplication.instance() or QGuiApplication(sys.argv)
out_dir = os.path.join(os.path.dirname(__file__))
os.makedirs(out_dir, exist_ok=True)

def svg_to_png(svg_str, out_png_path, scale=2.5):
    renderer = QSvgRenderer(QByteArray(svg_str.encode('utf-8')))
    default_size = renderer.defaultSize()
    w = int(default_size.width() * scale)
    h = int(default_size.height() * scale)
    
    img = QImage(QSize(w, h), QImage.Format_ARGB32)
    img.fill(QColor(255, 255, 255, 255))
    
    painter = QPainter(img)
    renderer.render(painter)
    painter.end()
    
    img.save(out_png_path, "PNG")
    print(f"Rendered: {os.path.basename(out_png_path)} ({w}x{h})")

# 1. HÌNH 3.11: Bài toán mở đầu (Cắt ghép hình thang cân)
svg_3_11 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 210" width="460" height="210">
  <rect width="460" height="210" fill="#ffffff"/>
  <g transform="translate(10, 10)">
    <!-- Toàn bộ hình thang mới tạo thành: D(50,150) -> M'(310,150) -> N'(260,40) -> A(100,40) -->
    <polygon points="50,150 310,150 260,40 100,40" fill="#f0f9ff" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>
    
    <!-- Nhát cắt MN (nét liền màu đỏ hoặc xám đậm) -->
    <line x1="150" y1="40" x2="150" y2="150" stroke="#ef4444" stroke-width="1.8" stroke-dasharray="4,2"/>
    
    <!-- Mép ghép dọc theo cạnh bên BC: B(200,40) -> C(250,150) -->
    <line x1="200" y1="40" x2="250" y2="150" stroke="#111827" stroke-width="1.5" stroke-dasharray="3,3"/>

    <!-- Vòng cung nét đứt biểu thị lật mảnh giấy từ bên trái sang mép phải -->
    <path d="M 100,40 C 130,10 230,10 260,40" fill="none" stroke="#0ea5e9" stroke-width="1.4" stroke-dasharray="3,3"/>
    <path d="M 50,150 C 90,195 270,195 310,150" fill="none" stroke="#0ea5e9" stroke-width="1.4" stroke-dasharray="3,3"/>

    <!-- Điểm đỉnh tròn -->
    <circle cx="100" cy="40" r="2.5" fill="#111827"/>
    <circle cx="150" cy="40" r="2.5" fill="#111827"/>
    <circle cx="200" cy="40" r="2.5" fill="#111827"/>
    <circle cx="260" cy="40" r="2.5" fill="#111827"/>
    <circle cx="50" cy="150" r="2.5" fill="#111827"/>
    <circle cx="150" cy="150" r="2.5" fill="#111827"/>
    <circle cx="250" cy="150" r="2.5" fill="#111827"/>
    <circle cx="310" cy="150" r="2.5" fill="#111827"/>

    <!-- Nhãn chữ đỉnh chuẩn Times New Roman in nghiêng -->
    <text x="94" y="30" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="144" y="30" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">M</text>
    <text x="195" y="30" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="255" y="30" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">N'</text>
    
    <text x="32" y="155" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
    <text x="144" y="170" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">N</text>
    <text x="245" y="170" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="318" y="155" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">M'</text>
  </g>
</svg>"""

# 2. HÌNH 3.12: Khái niệm hình thang ABCD (AB // CD) và đường cao AH
svg_3_12 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200" width="380" height="200">
  <rect width="380" height="200" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Hình thang ABCD: A(90, 35), B(230, 35), C(310, 160), D(30, 160) -->
    <polygon points="90,35 230,35 310,160 30,160" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>
    
    <!-- Đường cao AH: H(90, 160) -->
    <line x1="90" y1="35" x2="90" y2="160" stroke="#111827" stroke-width="1.5" stroke-dasharray="4,3"/>
    
    <!-- Ký hiệu góc vuông tại H: (90, 160), kích thước 12x12 -->
    <polyline points="90,148 78,148 78,160" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Điểm đỉnh -->
    <circle cx="90" cy="35" r="2.5" fill="#111827"/>
    <circle cx="230" cy="35" r="2.5" fill="#111827"/>
    <circle cx="310" cy="160" r="2.5" fill="#111827"/>
    <circle cx="30" cy="160" r="2.5" fill="#111827"/>
    <circle cx="90" cy="160" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="85" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="235" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="320" y="165" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="14" y="165" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
    <text x="85" y="180" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">H</text>

    <!-- Nhãn các yếu tố hình học theo SGK: đáy nhỏ, đáy lớn, cạnh bên, đường cao -->
    <text x="145" y="26" font-family="'Times New Roman', serif" font-size="12" fill="#475569">đáy nhỏ</text>
    <text x="175" y="180" font-family="'Times New Roman', serif" font-size="12" fill="#475569">đáy lớn</text>
    <text x="35" y="95" font-family="'Times New Roman', serif" font-size="11" fill="#475569" transform="rotate(-64 45,95)">cạnh bên</text>
    <text x="280" y="95" font-family="'Times New Roman', serif" font-size="11" fill="#475569" transform="rotate(57 280,95)">cạnh bên</text>
    <text x="96" y="105" font-family="'Times New Roman', serif" font-size="11" fill="#475569">đường cao</text>
  </g>
</svg>"""

# 3. HÌNH 3.13: Khái niệm hình thang cân (hai góc kề đáy bằng nhau)
svg_3_13 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 190" width="360" height="190">
  <rect width="360" height="190" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Hình thang cân ABCD: A(80, 35), B(220, 35), C(270, 155), D(30, 155) -->
    <polygon points="80,35 220,35 270,155 30,155" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>
    
    <!-- Cung tròn góc D (1 cung đơn) -->
    <path d="M 54,155 A 24,24 0 0,0 43,124" fill="none" stroke="#111827" stroke-width="1.4"/>
    
    <!-- Cung tròn góc C (1 cung đơn) -->
    <path d="M 257,124 A 24,24 0 0,0 246,155" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Cung tròn góc A (cung đôi) -->
    <path d="M 68,64 A 22,22 0 0,0 102,35" fill="none" stroke="#111827" stroke-width="1.4"/>
    <path d="M 64,70 A 27,27 0 0,0 107,35" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Cung tròn góc B (cung đôi) -->
    <path d="M 198,35 A 22,22 0 0,0 232,64" fill="none" stroke="#111827" stroke-width="1.4"/>
    <path d="M 193,35 A 27,27 0 0,0 236,70" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Điểm đỉnh -->
    <circle cx="80" cy="35" r="2.5" fill="#111827"/>
    <circle cx="220" cy="35" r="2.5" fill="#111827"/>
    <circle cx="270" cy="155" r="2.5" fill="#111827"/>
    <circle cx="30" cy="155" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="75" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="225" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="280" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="14" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
  </g>
</svg>"""

# 4. HÌNH 3.14: Ví dụ 1 (Hai góc kề một cạnh bên bù nhau, góc đồng vị D = A1)
svg_3_14 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 210" width="360" height="210">
  <rect width="360" height="210" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- D(40, 180), A(90, 80), kéo dài qua A đến (115, 30) -->
    <line x1="40" y1="180" x2="115" y2="30" stroke="#111827" stroke-width="1.8"/>
    
    <!-- Hình thang ABCD: A(90, 80), B(230, 80), C(280, 180), D(40, 180) -->
    <polygon points="90,80 230,80 280,180 40,180" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Cung góc D (1 cung đơn) -->
    <path d="M 64,180 A 24,24 0 0,0 52,156" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Cung góc A1 (1 cung đơn, đồng vị với góc D) -->
    <path d="M 115,80 A 25,25 0 0,0 101.2,57.6" fill="none" stroke="#111827" stroke-width="1.4"/>
    <text x="114" y="66" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" fill="#111827">1</text>

    <!-- Điểm đỉnh -->
    <circle cx="90" cy="80" r="2.5" fill="#111827"/>
    <circle cx="230" cy="80" r="2.5" fill="#111827"/>
    <circle cx="280" cy="180" r="2.5" fill="#111827"/>
    <circle cx="40" cy="180" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="70" y="85" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="238" y="78" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="290" y="185" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="24" y="185" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
  </g>
</svg>"""

# 5. HÌNH 3.15: Luyện tập 1 (Tính các góc hình thang cân khi biết góc C = 40 độ)
svg_3_15 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 190" width="360" height="190">
  <rect width="360" height="190" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Hình thang cân ABCD: A(80, 35), B(220, 35), C(270, 155), D(30, 155) -->
    <polygon points="80,35 220,35 270,155 30,155" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Cung góc C với số đo 40 độ -->
    <path d="M 252,112 A 26,26 0 0,0 244,155" fill="none" stroke="#111827" stroke-width="1.4"/>
    <text x="220" y="150" font-family="'Times New Roman', serif" font-size="14" fill="#111827">40°</text>

    <!-- Điểm đỉnh -->
    <circle cx="80" cy="35" r="2.5" fill="#111827"/>
    <circle cx="220" cy="35" r="2.5" fill="#111827"/>
    <circle cx="270" cy="155" r="2.5" fill="#111827"/>
    <circle cx="30" cy="155" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="75" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="225" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="280" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="14" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
  </g>
</svg>"""

# 6. HÌNH 3.16: HĐ1 (Kẻ AH, BI vuông góc CD, chứng minh AD = BC)
svg_3_16 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200" width="380" height="200">
  <rect width="380" height="200" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Hình thang cân ABCD: A(90, 35), B(210, 35), C(270, 155), D(30, 155) -->
    <polygon points="90,35 210,35 270,155 30,155" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>
    
    <!-- Hai đường cao AH và BI -->
    <line x1="90" y1="35" x2="90" y2="155" stroke="#111827" stroke-width="1.6"/>
    <line x1="210" y1="35" x2="210" y2="155" stroke="#111827" stroke-width="1.6"/>

    <!-- Đường chéo phụ AI để chứng minh tam giác AHI = IBA -->
    <line x1="90" y1="35" x2="210" y2="155" stroke="#111827" stroke-width="1.4"/>

    <!-- Ký hiệu góc vuông tại H và I -->
    <polyline points="90,143 78,143 78,155" fill="none" stroke="#111827" stroke-width="1.3"/>
    <polyline points="210,143 222,143 222,155" fill="none" stroke="#111827" stroke-width="1.3"/>

    <!-- Điểm đỉnh -->
    <circle cx="90" cy="35" r="2.5" fill="#111827"/>
    <circle cx="210" cy="35" r="2.5" fill="#111827"/>
    <circle cx="270" cy="155" r="2.5" fill="#111827"/>
    <circle cx="30" cy="155" r="2.5" fill="#111827"/>
    <circle cx="90" cy="155" r="2.5" fill="#111827"/>
    <circle cx="210" cy="155" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="85" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="215" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="280" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="14" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
    <text x="85" y="176" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">H</text>
    <text x="207" y="176" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">I</text>
  </g>
</svg>"""

# 7. HÌNH 3.17: Định lí 1 (Trong hình thang cân, hai cạnh bên bằng nhau AD = BC)
svg_3_17 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 190" width="360" height="190">
  <rect width="360" height="190" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Hình thang cân ABCD: A(80, 35), B(220, 35), C(270, 155), D(30, 155) -->
    <polygon points="80,35 220,35 270,155 30,155" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Vạch bằng nhau trên AD: trung điểm (55, 95) -->
    <line x1="48" y1="92" x2="62" y2="98" stroke="#111827" stroke-width="1.6"/>

    <!-- Vạch bằng nhau trên BC: trung điểm (245, 95) -->
    <line x1="238" y1="98" x2="252" y2="92" stroke="#111827" stroke-width="1.6"/>

    <!-- Điểm đỉnh -->
    <circle cx="80" cy="35" r="2.5" fill="#111827"/>
    <circle cx="220" cy="35" r="2.5" fill="#111827"/>
    <circle cx="270" cy="155" r="2.5" fill="#111827"/>
    <circle cx="30" cy="155" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="75" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="225" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="280" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="14" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
  </g>
</svg>"""

# 8. HÌNH 3.18: Luyện tập 2 (Tứ giác ABCD có góc A = góc B = góc D1)
svg_3_18 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 200" width="360" height="200">
  <rect width="360" height="200" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Tứ giác ABCD: C(270, 150), D(90, 150), kéo dài CD qua D đến (30, 150) -->
    <!-- Đỉnh A(50, 45), B(210, 45) -->
    <line x1="30" y1="150" x2="270" y2="150" stroke="#111827" stroke-width="1.8"/>

    <!-- Các cạnh khác -->
    <polyline points="270,150 210,45 50,45 90,150" fill="none" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Cung góc A (1 cung) -->
    <path d="M 72,45 A 22,22 0 0,1 57.8,65.6" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Cung góc B (1 cung) -->
    <path d="M 188,45 A 22,22 0 0,0 220.9,64.1" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Cung góc D1 ngoài: đỉnh D(90, 150), tia Dx sang trái, tia DA lên (50, 45) -->
    <path d="M 65,150 A 25,25 0 0,1 81.1,126.6" fill="none" stroke="#111827" stroke-width="1.4"/>
    <text x="54" y="136" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" fill="#111827">1</text>

    <!-- Điểm đỉnh -->
    <circle cx="50" cy="45" r="2.5" fill="#111827"/>
    <circle cx="210" cy="45" r="2.5" fill="#111827"/>
    <circle cx="270" cy="150" r="2.5" fill="#111827"/>
    <circle cx="90" cy="150" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="35" y="40" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="215" y="40" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="280" y="155" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="96" y="168" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
  </g>
</svg>"""

# 9. HÌNH 3.19: HĐ2 (Hình thang cân có hai đường chéo AC = BD)
svg_3_19 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 190" width="360" height="190">
  <rect width="360" height="190" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Hình thang cân ABCD: A(80, 35), B(220, 35), C(270, 155), D(30, 155) -->
    <polygon points="80,35 220,35 270,155 30,155" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Hai đường chéo AC và BD -->
    <line x1="80" y1="35" x2="270" y2="155" stroke="#111827" stroke-width="1.6"/>
    <line x1="220" y1="35" x2="30" y2="155" stroke="#111827" stroke-width="1.6"/>

    <!-- Điểm đỉnh -->
    <circle cx="80" cy="35" r="2.5" fill="#111827"/>
    <circle cx="220" cy="35" r="2.5" fill="#111827"/>
    <circle cx="270" cy="155" r="2.5" fill="#111827"/>
    <circle cx="30" cy="155" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="75" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="225" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="280" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="14" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
  </g>
</svg>"""

# 10. HÌNH 3.20: Luyện tập 3 (Tam giác ABC cân tại A, d song song BC cắt AB tại D, AC tại E)
svg_3_20 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 210" width="380" height="210">
  <rect width="380" height="210" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Tam giác ABC cân tại A: A(180, 30), B(50, 175), C(310, 175) -->
    <polygon points="180,30 50,175 310,175" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Đường thẳng d song song BC -->
    <line x1="20" y1="115" x2="340" y2="115" stroke="#111827" stroke-width="1.5"/>

    <!-- Điểm đỉnh và giao điểm -->
    <circle cx="180" cy="30" r="2.5" fill="#111827"/>
    <circle cx="50" cy="175" r="2.5" fill="#111827"/>
    <circle cx="310" cy="175" r="2.5" fill="#111827"/>
    <circle cx="104" cy="115" r="2.5" fill="#111827"/>
    <circle cx="256" cy="115" r="2.5" fill="#111827"/>

    <!-- Nhãn chữ -->
    <text x="175" y="20" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="34" y="185" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="318" y="185" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="90" y="108" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
    <text x="262" y="108" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">E</text>
    <text x="330" y="108" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">d</text>
  </g>
</svg>"""

# 11. HÌNH 3.21: Ví dụ 2 (Hình thang ABCD có góc ACD = góc BDC là hình thang cân)
svg_3_21 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 190" width="360" height="190">
  <rect width="360" height="190" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Hình thang cân ABCD: A(80, 35), B(220, 35), C(270, 155), D(30, 155) -->
    <polygon points="80,35 220,35 270,155 30,155" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Hai đường chéo AC và BD cắt nhau tại I(150, 79.2) -->
    <line x1="80" y1="35" x2="270" y2="155" stroke="#111827" stroke-width="1.6"/>
    <line x1="220" y1="35" x2="30" y2="155" stroke="#111827" stroke-width="1.6"/>

    <!-- Cung góc ACD tại C (1 cung) -->
    <path d="M 235,155 A 35,35 0 0,0 240.4,136.3" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Cung góc BDC tại D (1 cung) -->
    <path d="M 65,155 A 35,35 0 0,1 59.6,136.3" fill="none" stroke="#111827" stroke-width="1.4"/>

    <!-- Điểm đỉnh và giao điểm I -->
    <circle cx="80" cy="35" r="2.5" fill="#111827"/>
    <circle cx="220" cy="35" r="2.5" fill="#111827"/>
    <circle cx="270" cy="155" r="2.5" fill="#111827"/>
    <circle cx="30" cy="155" r="2.5" fill="#111827"/>
    <circle cx="150" cy="79.2" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="75" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="225" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="280" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="14" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
    <text x="145" y="98" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">I</text>
  </g>
</svg>"""

# 12. HÌNH 3.22: Thực hành (Vẽ hình thang có hai đường chéo bằng nhau qua cung tròn)
svg_3_22 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200" width="380" height="200">
  <rect width="380" height="200" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Đường b ở trên: y=45; đường a ở dưới: y=145 -->
    <line x1="20" y1="45" x2="340" y2="45" stroke="#111827" stroke-width="1.4"/>
    <line x1="20" y1="145" x2="340" y2="145" stroke="#111827" stroke-width="1.4"/>

    <!-- A(110, 145), B(210, 145) trên đường a -->
    <!-- D(50, 45), C(270, 45) trên đường b -->
    <!-- Hình thang ABCD -->
    <polygon points="110,145 210,145 270,45 50,45" fill="none" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Đường chéo AC và BD -->
    <line x1="110" y1="145" x2="270" y2="45" stroke="#111827" stroke-width="1.6"/>
    <line x1="210" y1="145" x2="50" y2="45" stroke="#111827" stroke-width="1.6"/>

    <!-- Cung tròn tâm A bán kính AC qua C: nét đứt màu xanh -->
    <path d="M 265,35 A 190,190 0 0,1 280,65" fill="none" stroke="#0284c7" stroke-width="1.4" stroke-dasharray="3,3"/>

    <!-- Cung tròn tâm B bán kính BD qua D: nét đứt màu xanh -->
    <path d="M 55,35 A 190,190 0 0,0 40,65" fill="none" stroke="#0284c7" stroke-width="1.4" stroke-dasharray="3,3"/>

    <!-- Điểm đỉnh -->
    <circle cx="110" cy="145" r="2.5" fill="#111827"/>
    <circle cx="210" cy="145" r="2.5" fill="#111827"/>
    <circle cx="270" cy="45" r="2.5" fill="#111827"/>
    <circle cx="50" cy="45" r="2.5" fill="#111827"/>

    <!-- Nhãn chữ -->
    <text x="105" y="165" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="205" y="165" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="275" y="40" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="38" y="40" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
    <text x="160" y="162" font-family="'Times New Roman', serif" font-style="italic" font-size="15" fill="#111827">a</text>
    <text x="160" y="38" font-family="'Times New Roman', serif" font-style="italic" font-size="15" fill="#111827">b</text>
  </g>
</svg>"""

# 13. HÌNH 3.23: Bài 3.4 (Hình thang có góc A = 120 độ, góc C = 80 độ)
svg_3_23 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190" width="340" height="190">
  <rect width="340" height="190" fill="#ffffff"/>
  <g transform="translate(15, 10)">
    <!-- Tứ giác ABCD có đáy AB // CD: A(90, 45), B(210, 45), C(235, 155), D(45, 155) -->
    <polygon points="90,45 210,45 235,155 45,155" fill="#f8fafc" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/>

    <!-- Cung góc A (120 độ) -->
    <path d="M 118,45 A 28,28 0 0,1 79.4,70.9" fill="none" stroke="#111827" stroke-width="1.4"/>
    <text x="92" y="68" font-family="'Times New Roman', serif" font-size="13" fill="#111827">120°</text>

    <!-- Cung góc C (80 độ) -->
    <path d="M 210,155 A 25,25 0 0,1 229.5,130.6" fill="none" stroke="#111827" stroke-width="1.4"/>
    <text x="182" y="148" font-family="'Times New Roman', serif" font-size="13" fill="#111827">80°</text>

    <!-- Điểm đỉnh -->
    <circle cx="90" cy="45" r="2.5" fill="#111827"/>
    <circle cx="210" cy="45" r="2.5" fill="#111827"/>
    <circle cx="235" cy="155" r="2.5" fill="#111827"/>
    <circle cx="45" cy="155" r="2.5" fill="#111827"/>

    <!-- Nhãn đỉnh -->
    <text x="85" y="32" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">A</text>
    <text x="215" y="32" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">B</text>
    <text x="245" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">C</text>
    <text x="28" y="160" font-family="'Times New Roman', serif" font-style="italic" font-size="16" fill="#111827">D</text>
  </g>
</svg>"""

drawings = [
    ("hinh_3_11", svg_3_11),
    ("hinh_3_12", svg_3_12),
    ("hinh_3_13", svg_3_13),
    ("hinh_3_14", svg_3_14),
    ("hinh_3_15", svg_3_15),
    ("hinh_3_16", svg_3_16),
    ("hinh_3_17", svg_3_17),
    ("hinh_3_18", svg_3_18),
    ("hinh_3_19", svg_3_19),
    ("hinh_3_20", svg_3_20),
    ("hinh_3_21", svg_3_21),
    ("hinh_3_22", svg_3_22),
    ("hinh_3_23", svg_3_23),
]

for name, svg in drawings:
    svg_path = os.path.join(out_dir, f"{name}.svg")
    png_path = os.path.join(out_dir, f"{name}.png")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    svg_to_png(svg, png_path, scale=2.5)

print(f"Successfully generated all {len(drawings)} drawings!")
