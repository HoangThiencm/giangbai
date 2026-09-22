import os
import sys
import math
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, QSize

app = QGuiApplication.instance() or QGuiApplication(sys.argv)
out_dir = 'GIAO AN/hinh_ve_sgk'
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
    print(f"Rendered: {out_png_path} ({w}x{h})")

# 1. HÌNH 3.24: Ví dụ chứng minh hình thang có 2 đáy không bằng nhau, 2 cạnh bên bằng nhau là hình thang cân
# Hình thang ABCD, AB // CD, AB < CD, AD = BC. E nằm trên CD sao cho DE = AB.
# Vẽ sạch sẽ, chuẩn mực, hoàn toàn không có chú thích caption
svg_hinh_3_24 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 240" width="500" height="240">
  <rect width="500" height="240" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #0055aa; }
      .label-num { font-family: 'Times New Roman', serif; font-style: italic; font-size: 15px; font-weight: bold; fill: #0055aa; }
      .tick-mark { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; }
    </style>
  </defs>

  <!-- Đáy CD: D=(60, 190), C=(440, 190) -->
  <!-- Đáy AB: A=(160, 60), B=(340, 60) -->
  <!-- Điểm E trên CD: DE = AB = 180 => E=(240, 190) -->
  <!-- Tứ giác ABED là hình bình hành: AD // BE, AD = BE = 164.01 -->
  <!-- Tam giác BEC cân tại B: BE = BC = 164.01 -->

  <!-- Các cạnh hình thang -->
  <line x1="60" y1="190" x2="440" y2="190" class="geom-line"/>
  <line x1="160" y1="60" x2="340" y2="60" class="geom-line"/>
  <line x1="60" y1="190" x2="160" y2="60" class="geom-line"/>
  <line x1="440" y1="190" x2="340" y2="60" class="geom-line"/>

  <!-- Các đoạn nối AE và BE -->
  <line x1="160" y1="60" x2="240" y2="190" class="geom-line"/>
  <line x1="340" y1="60" x2="240" y2="190" class="geom-line"/>

  <!-- Vạch bằng nhau AD = BC (1 vạch xiên) -->
  <!-- AD midpoint: (110, 125). Vector normal: (130, 100) / 164 * 6 = (4.75, 3.65) -->
  <line x1="104" y1="130" x2="116" y2="120" class="tick-mark"/>
  <!-- BC midpoint: (390, 125) -->
  <line x1="384" y1="120" x2="396" y2="130" class="tick-mark"/>

  <!-- Điểm đỉnh -->
  <circle cx="160" cy="60" r="2.5" class="point-dot"/>
  <circle cx="340" cy="60" r="2.5" class="point-dot"/>
  <circle cx="440" cy="190" r="2.5" class="point-dot"/>
  <circle cx="60" cy="190" r="2.5" class="point-dot"/>
  <circle cx="240" cy="190" r="2.5" class="point-dot"/>

  <!-- Nhãn đỉnh -->
  <text x="155" y="44" class="label-vertex">A</text>
  <text x="345" y="44" class="label-vertex">B</text>
  <text x="448" y="202" class="label-vertex">C</text>
  <text x="45" y="202" class="label-vertex">D</text>
  <text x="236" y="215" class="label-vertex">E</text>

  <!-- Đánh số các góc -->
  <!-- Tại A: góc 1 (trong tam giác ADE), góc 2 (giữa AB và AE) -->
  <text x="150" y="85" class="label-num">1</text>
  <text x="180" y="78" class="label-num">2</text>

  <!-- Tại B: góc 1 (giữa AB và BE) -->
  <text x="320" y="80" class="label-num">1</text>

  <!-- Tại E: góc 1, góc 2, góc 3 -->
  <text x="215" y="180" class="label-num">1</text>
  <text x="238" y="165" class="label-num">2</text>
  <text x="260" y="180" class="label-num">3</text>
</svg>"""

# 2. HÌNH 3.25: Bài 3.9 SGK trang 56
# Tứ giác ABCD có góc A = 120 độ, góc D = 60 độ
svg_hinh_3_25 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 220" width="440" height="220">
  <rect width="440" height="220" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #0055aa; }
      .label-deg { font-family: 'Times New Roman', serif; font-size: 15px; font-weight: bold; fill: #0055aa; }
      .angle-arc { stroke: #0055aa; stroke-width: 1.5; fill: none; }
    </style>
  </defs>

  <!-- Cạnh đáy CD: D=(70, 175), C=(370, 175) -->
  <!-- Cạnh đáy AB: A=(135, 65), B=(320, 65) -->
  <!-- Góc D = 60 độ, Góc A = 120 độ => AD nghiêng 60 độ so với đáy -->
  <line x1="70" y1="175" x2="370" y2="175" class="geom-line"/>
  <line x1="135" y1="65" x2="320" y2="65" class="geom-line"/>
  <line x1="70" y1="175" x2="135" y2="65" class="geom-line"/>
  <line x1="370" y1="175" x2="320" y2="65" class="geom-line"/>

  <!-- Cung góc D (60 độ) tại (70, 175) -->
  <!-- Cung từ (100, 175) tới hướng AD (70 + 30*cos60, 175 - 30*sin60) = (85, 149) -->
  <path d="M 98 175 A 28 28 0 0 0 84 150" class="angle-arc"/>
  <text x="75" y="165" class="label-deg">60°</text>

  <!-- Cung góc A (120 độ) tại (135, 65) -->
  <!-- Cung từ AD (135 - 28*cos60, 65 + 28*sin60) = (121, 89) tới AB (163, 65) -->
  <path d="M 121 89 A 28 28 0 0 0 163 65" class="angle-arc"/>
  <text x="135" y="90" class="label-deg">120°</text>

  <!-- Điểm đỉnh -->
  <circle cx="135" cy="65" r="2.5" class="point-dot"/>
  <circle cx="320" cy="65" r="2.5" class="point-dot"/>
  <circle cx="370" cy="175" r="2.5" class="point-dot"/>
  <circle cx="70" cy="175" r="2.5" class="point-dot"/>

  <!-- Nhãn đỉnh -->
  <text x="126" y="50" class="label-vertex">A</text>
  <text x="325" y="50" class="label-vertex">B</text>
  <text x="375" y="188" class="label-vertex">C</text>
  <text x="52" y="188" class="label-vertex">D</text>
</svg>"""

# 3. HÌNH 3.26: Bài 3.11 SGK trang 56
# Tứ giác ABCD hình cánh diều: AB = AD (1 vạch), BC = CD (2 vạch). Đường chéo BD.
# Góc ABD = 40 độ, góc ADC = 120 độ.
svg_hinh_3_26 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 230" width="500" height="230">
  <rect width="500" height="230" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #0055aa; }
      .label-deg { font-family: 'Times New Roman', serif; font-size: 14px; font-weight: bold; fill: #0055aa; }
      .angle-arc { stroke: #0055aa; stroke-width: 1.5; fill: none; }
      .tick-mark { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; }
    </style>
  </defs>

  <!-- Đỉnh: A=(80, 115), B=(160, 40), D=(160, 190), C=(450, 115) -->
  <line x1="80" y1="115" x2="160" y2="40" class="geom-line"/>
  <line x1="160" y1="40" x2="450" y2="115" class="geom-line"/>
  <line x1="450" y1="115" x2="160" y2="190" class="geom-line"/>
  <line x1="160" y1="190" x2="80" y2="115" class="geom-line"/>
  <!-- Đường chéo BD -->
  <line x1="160" y1="40" x2="160" y2="190" class="geom-line"/>

  <!-- 1 vạch trên AB và AD -->
  <!-- AB midpoint: (120, 77.5) -->
  <line x1="114" y1="81" x2="126" y2="74" class="tick-mark"/>
  <!-- AD midpoint: (120, 152.5) -->
  <line x1="114" y1="149" x2="126" y2="156" class="tick-mark"/>

  <!-- 2 vạch trên BC và CD -->
  <!-- BC midpoint: (305, 77.5) -->
  <line x1="300" y1="72" x2="308" y2="82" class="tick-mark"/>
  <line x1="305" y1="73" x2="313" y2="83" class="tick-mark"/>
  <!-- CD midpoint: (305, 152.5) -->
  <line x1="300" y1="158" x2="308" y2="148" class="tick-mark"/>
  <line x1="305" y1="157" x2="313" y2="147" class="tick-mark"/>

  <!-- Góc ABD = 40 độ tại B(160, 40) -->
  <!-- Cung từ BD (160, 68) tới BA (160 - 28*sin47, 40 + 28*cos47) = (140, 59) -->
  <path d="M 140 59 A 28 28 0 0 0 160 68" class="angle-arc"/>
  <text x="142" y="78" class="label-deg">40°</text>

  <!-- Góc ADC = 120 độ tại D(160, 190) -->
  <!-- Cung từ DA (140, 171) tới DC (187, 183) -->
  <path d="M 140 171 A 28 28 0 0 1 187 183" class="angle-arc"/>
  <text x="165" y="172" class="label-deg">120°</text>

  <!-- Điểm đỉnh -->
  <circle cx="80" cy="115" r="2.5" class="point-dot"/>
  <circle cx="160" cy="40" r="2.5" class="point-dot"/>
  <circle cx="450" cy="115" r="2.5" class="point-dot"/>
  <circle cx="160" cy="190" r="2.5" class="point-dot"/>

  <!-- Nhãn đỉnh -->
  <text x="62" y="120" class="label-vertex">A</text>
  <text x="156" y="28" class="label-vertex">B</text>
  <text x="458" y="120" class="label-vertex">C</text>
  <text x="156" y="210" class="label-vertex">D</text>
</svg>"""

# 4. HÌNH BÀI 3.10: Bài tập 3.10 SGK trang 56
# Cho hình thang cân ABCD (AB // CD) có AB = AD, góc ABD = 30 độ
svg_hinh_bai_3_10 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 230" width="460" height="230">
  <rect width="460" height="230" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #0055aa; }
      .label-deg { font-family: 'Times New Roman', serif; font-size: 14px; font-weight: bold; fill: #0055aa; }
      .angle-arc { stroke: #0055aa; stroke-width: 1.5; fill: none; }
      .tick-mark { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; }
    </style>
  </defs>

  <!-- Đáy CD: D=(50, 185), C=(410, 185) -->
  <!-- Đáy AB: A=(140, 65), B=(320, 65). Độ dài AB = 180. AD = sqrt(90^2 + 120^2) = 150 -->
  <!-- Để AB = AD: nếu dy = 120, dx = sqrt(180^2 - 120^2) = 134 => A=(184, 65), B=(364, 65) thì hình thang mất cân đối -->
  <!-- Ta vẽ AB = 160, A=(150, 65), B=(310, 65), D=(70, 185), C=(390, 185) -->
  <!-- AD = sqrt(80^2 + 120^2) = 144, AB = 160 xấp xỉ bằng nhau trực quan rất đẹp -->
  <line x1="70" y1="185" x2="390" y2="185" class="geom-line"/>
  <line x1="150" y1="65" x2="310" y2="65" class="geom-line"/>
  <line x1="70" y1="185" x2="150" y2="65" class="geom-line"/>
  <line x1="390" y1="185" x2="310" y2="65" class="geom-line"/>
  <!-- Đường chéo BD -->
  <line x1="310" y1="65" x2="70" y2="185" class="geom-line"/>

  <!-- Vạch bằng nhau trên AB và AD -->
  <!-- AB midpoint: (230, 65) -->
  <line x1="230" y1="58" x2="230" y2="72" class="tick-mark"/>
  <!-- AD midpoint: (110, 125) -->
  <line x1="104" y1="129" x2="116" y2="121" class="tick-mark"/>

  <!-- Góc ABD = 30 độ tại B(310, 65) -->
  <!-- Cung giữa BA và BD -->
  <path d="M 280 65 A 30 30 0 0 1 285 78" class="angle-arc"/>
  <text x="250" y="88" class="label-deg">30°</text>

  <!-- Điểm đỉnh -->
  <circle cx="150" cy="65" r="2.5" class="point-dot"/>
  <circle cx="310" cy="65" r="2.5" class="point-dot"/>
  <circle cx="390" cy="185" r="2.5" class="point-dot"/>
  <circle cx="70" cy="185" r="2.5" class="point-dot"/>

  <!-- Nhãn đỉnh -->
  <text x="144" y="48" class="label-vertex">A</text>
  <text x="315" y="48" class="label-vertex">B</text>
  <text x="398" y="198" class="label-vertex">C</text>
  <text x="52" y="198" class="label-vertex">D</text>
</svg>"""

# 5. HÌNH BÀI 3.12: Bài tập 3.12 SGK trang 56
# Cho M trong tam giác đều ABC. Kẻ các đường song song với BC, CA, AB cắt các cạnh tại P, Q, R...
svg_hinh_bai_3_12 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 300" width="460" height="300">
  <rect width="460" height="300" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .geom-dashed { stroke: #4b5563; stroke-width: 1.5; stroke-dasharray: 4,4; fill: none; }
      .point-dot { fill: #111827; }
      .point-m { fill: #dc2626; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #0055aa; }
      .label-pt { font-family: 'Times New Roman', serif; font-style: italic; font-size: 16px; font-weight: bold; fill: #111827; }
      .poly-highlight { fill: #eff6ff; stroke: #2563eb; stroke-width: 1.8; }
    </style>
  </defs>

  <!-- Tam giác đều ABC: A=(230, 35), B=(70, 260), C=(390, 260) -->
  <!-- Điểm M bên trong: M=(210, 180) -->
  <!-- Qua M kẻ:
       1) // BC (nằm ngang y=180): cắt AB tại P, cắt AC tại P2
          Phương trình AB: y - 260 = -sqrt(3)*(x - 70) => y = -1.406*x + 358.4 => x_P = (260-180)/tan60 + 70 = 80/1.406 + 70 = 127
          => P=(127, 180) trên AB
       2) // AB: cắt AC tại R, cắt BC tại R2
          Qua M(210, 180) song song AB (nghiêng 60 độ về phía trước):
          Cắt AC tại R=(270, 91)
       3) // AC: cắt BC tại Q, cắt AB tại Q2
          Qua M(210, 180) song song AC:
          Cắt BC tại Q=(280, 260)
  -->

  <!-- Các cạnh tam giác đều ABC -->
  <polygon points="230,35 70,260 390,260" fill="none" stroke="#111827" stroke-width="2"/>

  <!-- Tứ giác APMR hình thang cân được tô nhẹ nổi bật -->
  <polygon points="230,35 127,180 210,180 270,91" fill="#f0f9ff" stroke="#2563eb" stroke-width="1.8"/>

  <!-- Các đường song song qua M -->
  <!-- Đoạn song song BC qua M: từ P(127, 180) đến AC (293, 180) -->
  <line x1="127" y1="180" x2="293" y2="180" class="geom-line"/>
  <!-- Đoạn song song AB qua M: từ BC(164, 260) qua M(210, 180) đến R(270, 91) -->
  <line x1="164" y1="260" x2="270" y2="91" class="geom-line"/>
  <!-- Đoạn song song AC qua M: từ AB(184, 99) qua M(210, 180) đến Q(256, 260) -->
  <line x1="184" y1="99" x2="256" y2="260" class="geom-line"/>

  <!-- Nối tam giác PQR để làm rõ câu b, c -->
  <polygon points="127,180 256,260 270,91" fill="none" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,3"/>

  <!-- Điểm đỉnh -->
  <circle cx="230" cy="35" r="2.5" class="point-dot"/>
  <circle cx="70" cy="260" r="2.5" class="point-dot"/>
  <circle cx="390" cy="260" r="2.5" class="point-dot"/>
  <circle cx="210" cy="180" r="3.5" class="point-m"/>
  <circle cx="127" cy="180" r="2.5" class="point-dot"/>
  <circle cx="256" cy="260" r="2.5" class="point-dot"/>
  <circle cx="270" cy="91" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="226" y="24" class="label-vertex">A</text>
  <text x="50" y="275" class="label-vertex">B</text>
  <text x="398" y="275" class="label-vertex">C</text>
  <text x="202" y="160" class="label-pt" fill="#dc2626">M</text>
  <text x="108" y="185" class="label-pt">P</text>
  <text x="252" y="280" class="label-pt">Q</text>
  <text x="280" y="94" class="label-pt">R</text>
</svg>"""

# 6. HÌNH NĂNG LỰC SỐ GEOGEBRA (NLS: 5.2.TC2b - Thực nghiệm 2 đường chéo bằng nhau của hình thang cân)
svg_hinh_geogebra = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 250" width="600" height="250">
  <rect width="600" height="250" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" rx="6"/>
  <defs>
    <style>
      .geom-line { stroke: #1e293b; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .diag-line-1 { stroke: #2563eb; stroke-width: 2; stroke-dasharray: 4,4; fill: none; }
      .diag-line-2 { stroke: #dc2626; stroke-width: 2; stroke-dasharray: 4,4; fill: none; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 17px; font-weight: bold; fill: #0f172a; }
      .ui-text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: bold; fill: #1e293b; }
      .ui-val { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: bold; }
    </style>
  </defs>

  <!-- Thanh công cụ GeoGebra giả lập phía trên -->
  <rect x="0" y="0" width="600" height="32" fill="#e2e8f0" rx="6 6 0 0"/>
  <text x="15" y="21" class="ui-text" fill="#475569">GeoGebra Geometry — [NLS: 5.2.TC2b] Khám phá tính chất 2 đường chéo</text>

  <!-- Bảng số liệu đo đạc bên trái -->
  <rect x="18" y="45" width="165" height="100" fill="#ffffff" stroke="#94a3b8" rx="4"/>
  <text x="28" y="72" class="ui-text" fill="#2563eb">AC = 6.42 cm</text>
  <text x="28" y="98" class="ui-text" fill="#dc2626">BD = 6.42 cm</text>
  <line x1="28" y1="108" x2="173" y2="108" stroke="#cbd5e1"/>
  <text x="28" y="130" class="ui-val" fill="#16a34a">AC = BD (Đúng)</text>

  <!-- Hình thang cân ABCD trong khu vực làm việc GeoGebra -->
  <!-- A=(290, 75), B=(460, 75), C=(515, 205), D=(235, 205) -->
  <polygon points="290,75 460,75 515,205 235,205" fill="#ffffff" stroke="#1e293b" stroke-width="2"/>
  <!-- Hai đường chéo AC và BD -->
  <line x1="290" y1="75" x2="515" y2="205" class="diag-line-1"/>
  <line x1="460" y1="75" x2="235" y2="205" class="diag-line-2"/>

  <!-- Các điểm kéo thả của GeoGebra -->
  <circle cx="290" cy="75" r="4.5" fill="#2563eb"/>
  <circle cx="460" cy="75" r="4.5" fill="#2563eb"/>
  <circle cx="515" cy="205" r="4.5" fill="#2563eb"/>
  <circle cx="235" cy="205" r="4.5" fill="#2563eb"/>

  <!-- Nhãn điểm -->
  <text x="282" y="62" class="label-vertex">A</text>
  <text x="464" y="62" class="label-vertex">B</text>
  <text x="524" y="215" class="label-vertex">C</text>
  <text x="220" y="215" class="label-vertex">D</text>

  <!-- Ghi chú thao tác kéo thả động -->
  <text x="210" y="238" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-style="italic" fill="#64748b">* Kéo thả các đỉnh A, B, C, D: độ dài AC và BD luôn bằng nhau.</text>
</svg>"""

drawings = [
    ("hinh_3_24.svg", "hinh_3_24.png", svg_hinh_3_24),
    ("hinh_3_25.svg", "hinh_3_25.png", svg_hinh_3_25),
    ("hinh_3_26.svg", "hinh_3_26.png", svg_hinh_3_26),
    ("hinh_bai_3_10.svg", "hinh_bai_3_10.png", svg_hinh_bai_3_10),
    ("hinh_bai_3_12.svg", "hinh_bai_3_12.png", svg_hinh_bai_3_12),
    ("hinh_geogebra.svg", "hinh_geogebra.png", svg_hinh_geogebra),
]

for svg_name, png_name, svg_content in drawings:
    svg_path = os.path.join(out_dir, svg_name)
    png_path = os.path.join(out_dir, png_name)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    svg_to_png(svg_content, png_path, scale=2.5)

print("ALL SVG AND PNG DRAWINGS GENERATED SUCCESSFULLY!")
