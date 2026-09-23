import os
import sys
import math
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, QSize

out_dir = os.path.dirname(os.path.abspath(__file__))
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

# ==============================================================================
# 1. HÌNH 3.27: Bài toán mở đầu - Hai con đường a, b cắt nhau và điểm dân cư O
# ==============================================================================
svg_hinh_3_27 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 280" width="520" height="280">
  <rect width="520" height="280" fill="#ffffff"/>
  <defs>
    <style>
      .road-base { stroke: #374151; stroke-width: 24; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .road-line { stroke: #f9fafb; stroke-width: 2; stroke-dasharray: 8 6; fill: none; }
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; fill: none; }
      .dash-line { stroke: #dc2626; stroke-width: 1.8; stroke-dasharray: 5 4; stroke-linecap: round; fill: none; }
      .point-dot { fill: #111827; }
      .point-red { fill: #dc2626; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 19px; font-weight: bold; fill: #111827; }
      .label-red { font-family: 'Times New Roman', serif; font-style: italic; font-size: 19px; font-weight: bold; fill: #dc2626; }
      .label-street { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #ffffff; }
      .tick-mark { stroke: #dc2626; stroke-width: 1.6; stroke-linecap: round; }
    </style>
  </defs>

  <!-- Đỉnh giao hai con đường: V = (60, 230) -->
  <!-- Đường b: ngang từ (60, 230) đến (480, 230) -->
  <!-- Đường a: xiên lên từ (60, 230) đến (340, 30) (góc khoảng 55 độ) -->

  <!-- Con đường b (ngang) -->
  <line x1="50" y1="230" x2="490" y2="230" class="road-base"/>
  <line x1="70" y1="230" x2="470" y2="230" class="road-line"/>

  <!-- Con đường a (xiên) -->
  <line x1="50" y1="230" x2="345" y2="20" class="road-base"/>
  <line x1="70" y1="216" x2="335" y2="27" class="road-line"/>

  <!-- Tên đường a và b -->
  <text x="210" y="105" class="label-street">a</text>
  <text x="220" y="236" class="label-street">b</text>

  <!-- Điểm dân cư O: (310, 150) -->
  <!-- Đường thẳng qua O cắt a tại A(260, 80) và cắt b tại B(360, 220) -->
  <!-- Vector AB: (100, 140), O chính là trung điểm (260+360)/2=310, (80+220)/2=150 -->
  <line x1="240" y1="52" x2="380" y2="248" class="dash-line"/>

  <!-- Vạch bằng nhau OA = OB -->
  <!-- Mid OA: (285, 115) -->
  <line x1="280" y1="119" x2="290" y2="111" class="tick-mark"/>
  <!-- Mid OB: (335, 185) -->
  <line x1="330" y1="189" x2="340" y2="181" class="tick-mark"/>

  <!-- Biểu tượng ngôi nhà nhỏ tại điểm O -->
  <polygon points="360,110 395,85 430,110" fill="#dc2626"/>
  <rect x="370" y="110" width="50" height="35" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
  <rect x="388" y="125" width="14" height="20" fill="#b45309"/>
  <rect x="375" y="116" width="10" height="10" fill="#60a5fa"/>
  <rect x="405" y="116" width="10" height="10" fill="#60a5fa"/>

  <!-- Các điểm A, B, O -->
  <circle cx="260" cy="80" r="3.5" class="point-dot"/>
  <circle cx="360" cy="220" r="3.5" class="point-dot"/>
  <circle cx="310" cy="150" r="4" class="point-red"/>

  <!-- Nhãn điểm -->
  <text x="270" y="75" class="label-vertex">A</text>
  <text x="372" y="215" class="label-vertex">B</text>
  <text x="320" y="156" class="label-red">O</text>
</svg>"""

# ==============================================================================
# 2. HÌNH 3.28: HĐ1 - Nhận biết hình bình hành trên lưới ô vuông
# ==============================================================================
svg_hinh_3_28 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 250" width="720" height="250">
  <rect width="720" height="250" fill="#ffffff"/>
  <defs>
    <style>
      .grid-line { stroke: #e5e7eb; stroke-width: 1; }
      .geom-line { stroke: #111827; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 17px; font-weight: bold; fill: #111827; }
      .label-fig { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
    </style>
    <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
      <path d="M 22 0 L 0 0 0 22" fill="none" stroke="#e5e7eb" stroke-width="1"/>
    </pattern>
  </defs>

  <!-- Lưới ô vuông phủ nền -->
  <rect x="20" y="15" width="680" height="198" fill="url(#grid)" stroke="#d1d5db" stroke-width="1"/>

  <!-- ================= Hình a: Tứ giác không song song ================= -->
  <!-- A=(86, 59), B=(196, 59), C=(174, 191), D=(42, 147) -->
  <polygon points="86,59 196,59 174,191 42,147" class="geom-line"/>
  <circle cx="86" cy="59" r="2.5" class="point-dot"/>
  <circle cx="196" cy="59" r="2.5" class="point-dot"/>
  <circle cx="174" cy="191" r="2.5" class="point-dot"/>
  <circle cx="42" cy="147" r="2.5" class="point-dot"/>
  <text x="78" y="52" class="label-vertex">A</text>
  <text x="202" y="55" class="label-vertex">B</text>
  <text x="180" y="202" class="label-vertex">C</text>
  <text x="28" y="152" class="label-vertex">D</text>
  <text x="115" y="235" class="label-fig">a)</text>

  <!-- ================= Hình b: Tứ giác dạng thoi/cánh diều ================= -->
  <!-- A=(338, 37), B=(382, 103), C=(338, 213), D=(294, 103) -->
  <polygon points="338,37 382,103 338,213 294,103" class="geom-line"/>
  <circle cx="338" cy="37" r="2.5" class="point-dot"/>
  <circle cx="382" cy="103" r="2.5" class="point-dot"/>
  <circle cx="338" cy="213" r="2.5" class="point-dot"/>
  <circle cx="294" cy="103" r="2.5" class="point-dot"/>
  <text x="333" y="30" class="label-vertex">A</text>
  <text x="390" y="108" class="label-vertex">B</text>
  <text x="333" y="226" class="label-vertex">C</text>
  <text x="278" y="108" class="label-vertex">D</text>
  <text x="335" y="235" class="label-fig">b)</text>

  <!-- ================= Hình c: Hình bình hành chuẩn ================= -->
  <!-- A=(524, 59), B=(656, 59), C=(612, 169), D=(480, 169) -->
  <!-- AB = 132 ngang; CD = 132 ngang; AD = BC = vector (-44, 110) -->
  <polygon points="524,59 656,59 612,169 480,169" class="geom-line"/>
  <circle cx="524" cy="59" r="2.5" class="point-dot"/>
  <circle cx="656" cy="59" r="2.5" class="point-dot"/>
  <circle cx="612" cy="169" r="2.5" class="point-dot"/>
  <circle cx="480" cy="169" r="2.5" class="point-dot"/>
  <text x="518" y="52" class="label-vertex">A</text>
  <text x="662" y="55" class="label-vertex">B</text>
  <text x="618" y="177" class="label-vertex">C</text>
  <text x="466" y="174" class="label-vertex">D</text>
  <text x="560" y="235" class="label-fig">c)</text>
</svg>"""

# ==============================================================================
# 3. HÌNH 3.29: Ví dụ 1 - Tứ giác ABCD có 3 góc bằng nhau
# ==============================================================================
svg_hinh_3_29 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 230" width="460" height="230">
  <rect width="460" height="230" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .label-ray { font-family: 'Times New Roman', serif; font-style: italic; font-size: 16px; font-weight: bold; fill: #111827; }
      .arc-angle { stroke: #111827; stroke-width: 1.4; fill: none; }
    </style>
  </defs>

  <!-- Đáy CD trên tia Dx: D=(100, 180), C=(340, 180). Tia Dx kéo dài sang trái tới (40, 180) -->
  <line x1="40" y1="180" x2="340" y2="180" class="geom-line"/>
  <text x="45" y="202" class="label-ray">x</text>

  <!-- Đỉnh A: (160, 70), B: (400, 70) -->
  <line x1="160" y1="70" x2="400" y2="70" class="geom-line"/>
  <line x1="100" y1="180" x2="160" y2="70" class="geom-line"/>

  <!-- Cạnh BC kéo dài thành tia By: C=(340, 180), B=(400, 70), kéo lên (420, 33) -->
  <line x1="340" y1="180" x2="422" y2="30" class="geom-line"/>
  <text x="424" y="32" class="label-ray">y</text>

  <!-- Các cung góc bằng nhau: xDA, DAB, yBC -->
  <!-- Góc xDA tại D: từ tia Dx (180 độ) lên DA (vectơ (60, -110), góc ~118.6 độ). Cung r=26 -->
  <path d="M 74 180 A 26 26 0 0 1 87 157" class="arc-angle"/>

  <!-- Góc DAB tại A: từ AD xuống AB. Cung r=26 -->
  <path d="M 147 93 A 26 26 0 0 0 186 70" class="arc-angle"/>

  <!-- Góc yBC tại B: từ tia By xuống BA. Cung r=26 -->
  <path d="M 409 54 A 26 26 0 0 0 374 70" class="arc-angle"/>

  <!-- Các đỉnh -->
  <circle cx="160" cy="70" r="2.5" class="point-dot"/>
  <circle cx="400" cy="70" r="2.5" class="point-dot"/>
  <circle cx="340" cy="180" r="2.5" class="point-dot"/>
  <circle cx="100" cy="180" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="145" y="60" class="label-vertex">A</text>
  <text x="408" y="75" class="label-vertex">B</text>
  <text x="345" y="196" class="label-vertex">C</text>
  <text x="100" y="202" class="label-vertex">D</text>
</svg>"""

# ==============================================================================
# 4. HÌNH 3.30: HĐ3 - Hình bình hành ABCD và hai đường chéo cắt nhau tại O
# ==============================================================================
svg_hinh_3_30 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 240" width="460" height="240">
  <rect width="460" height="240" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
    </style>
  </defs>

  <!-- Đỉnh: A=(140, 50), B=(380, 50), C=(320, 190), D=(80, 190) -->
  <!-- AB = 240, CD = 240, Giao O = ((140+320)/2, (50+190)/2) = (230, 120) -->
  <polygon points="140,50 380,50 320,190 80,190" class="geom-line"/>
  
  <!-- Hai đường chéo AC và BD -->
  <line x1="140" y1="50" x2="320" y2="190" class="geom-line"/>
  <line x1="80" y1="190" x2="380" y2="50" class="geom-line"/>

  <!-- Điểm đỉnh và giao điểm O -->
  <circle cx="140" cy="50" r="2.5" class="point-dot"/>
  <circle cx="380" cy="50" r="2.5" class="point-dot"/>
  <circle cx="320" cy="190" r="2.5" class="point-dot"/>
  <circle cx="80" cy="190" r="2.5" class="point-dot"/>
  <circle cx="230" cy="120" r="2.5" class="point-dot"/>

  <!-- Nhãn đỉnh -->
  <text x="132" y="42" class="label-vertex">A</text>
  <text x="388" y="48" class="label-vertex">B</text>
  <text x="326" y="204" class="label-vertex">C</text>
  <text x="65" y="200" class="label-vertex">D</text>
  <text x="238" y="125" class="label-vertex">O</text>
</svg>"""

# ==============================================================================
# 5. HÌNH 3.31: Ví dụ 2 - Hình bình hành ABCD, AH vuông góc BD, CK vuông góc BD
# ==============================================================================
svg_hinh_3_31 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 250" width="500" height="250">
  <rect width="500" height="250" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .label-num { font-family: 'Times New Roman', serif; font-style: italic; font-size: 15px; font-weight: bold; fill: #111827; }
      .right-angle { stroke: #111827; stroke-width: 1.4; fill: none; }
      .arc-angle { stroke: #111827; stroke-width: 1.3; fill: none; }
    </style>
  </defs>

  <!-- D=(60, 190), B=(420, 60). Vector DB: (360, -130). Độ dài ~382.75. Chiều u=(0.9405, -0.3396) -->
  <!-- A=(180, 60), C=(300, 190) -->
  <!-- Cạnh hình bình hành -->
  <polygon points="180,60 420,60 300,190 60,190" class="geom-line"/>
  <line x1="60" y1="190" x2="420" y2="60" class="geom-line"/>

  <!-- H là hình chiếu của A(180, 60) lên BD: -->
  <!-- D=(60, 190), DA=(120, -130). DA.u = 120*0.9405 + (-130)*(-0.3396) = 112.86 + 44.15 = 157.0 -->
  <!-- H = (60, 190) + 157.0*(0.9405, -0.3396) = (207.6, 136.7) -->
  <line x1="180" y1="60" x2="208" y2="137" class="geom-line"/>

  <!-- K là hình chiếu của C(300, 190) lên BD: đối xứng với H qua tâm O=(240, 125) -->
  <!-- K = (480 - 207.6, 250 - 136.7) = (272.4, 113.3) -->
  <line x1="300" y1="190" x2="272" y2="113" class="geom-line"/>

  <!-- Ký hiệu vuông góc tại H: vector HA = (-28, -77), norm HA: (-0.34, -0.94); u=(0.94, -0.34) -->
  <!-- Vuông góc H: l=10 -->
  <polyline points="217,133 213,124 204,127" class="right-angle"/>
  <!-- Vuông góc K: l=10 -->
  <polyline points="263,117 267,126 276,123" class="right-angle"/>

  <!-- Góc D1 và B1 (so le trong) -->
  <path d="M 85 181 A 26 26 0 0 0 86 160" class="arc-angle"/>
  <text x="96" y="174" class="label-num">1</text>

  <path d="M 395 69 A 26 26 0 0 0 394 90" class="arc-angle"/>
  <text x="382" y="86" class="label-num">1</text>

  <!-- Các đỉnh -->
  <circle cx="180" cy="60" r="2.5" class="point-dot"/>
  <circle cx="420" cy="60" r="2.5" class="point-dot"/>
  <circle cx="300" cy="190" r="2.5" class="point-dot"/>
  <circle cx="60" cy="190" r="2.5" class="point-dot"/>
  <circle cx="208" cy="137" r="2.5" class="point-dot"/>
  <circle cx="272" cy="113" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="175" y="48" class="label-vertex">A</text>
  <text x="428" y="65" class="label-vertex">B</text>
  <text x="306" y="206" class="label-vertex">C</text>
  <text x="45" y="196" class="label-vertex">D</text>
  <text x="195" y="156" class="label-vertex">H</text>
  <text x="272" y="103" class="label-vertex">K</text>
</svg>"""

# ==============================================================================
# 6. HÌNH 3.32: Luyện tập 2 - Phân giác D và B trong hình bình hành ABCD
# ==============================================================================
svg_hinh_3_32 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 240" width="500" height="240">
  <rect width="500" height="240" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .arc-angle { stroke: #111827; stroke-width: 1.3; fill: none; }
    </style>
  </defs>

  <!-- ABCD: D=(60, 190), C=(400, 190), A=(160, 60), B=(500, 60) (dài 340) -->
  <!-- AD = sqrt(100^2 + 130^2) = 164.0 -->
  <!-- Phân giác góc D: tam giác ADE cân tại A => AE = AD = 164.0 => E = (160 + 164, 60) = (324, 60) -->
  <!-- Phân giác góc B: tam giác CBF cân tại C => CF = CB = 164.0 => F = (400 - 164, 190) = (236, 190) -->
  <polygon points="160,60 490,60 390,190 60,190" class="geom-line"/>

  <!-- Đường DE và BF -->
  <line x1="60" y1="190" x2="310" y2="60" class="geom-line"/>
  <line x1="490" y1="60" x2="240" y2="190" class="geom-line"/>

  <!-- Cung góc phân giác tại D -->
  <path d="M 85 190 A 25 25 0 0 0 81 179" class="arc-angle"/>
  <path d="M 81 179 A 25 25 0 0 0 76 170" class="arc-angle"/>

  <!-- Cung góc phân giác tại B -->
  <path d="M 465 60 A 25 25 0 0 0 469 71" class="arc-angle"/>
  <path d="M 469 71 A 25 25 0 0 0 474 80" class="arc-angle"/>

  <!-- Điểm đỉnh -->
  <circle cx="160" cy="60" r="2.5" class="point-dot"/>
  <circle cx="490" cy="60" r="2.5" class="point-dot"/>
  <circle cx="390" cy="190" r="2.5" class="point-dot"/>
  <circle cx="60" cy="190" r="2.5" class="point-dot"/>
  <circle cx="310" cy="60" r="2.5" class="point-dot"/>
  <circle cx="240" cy="190" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="152" y="50" class="label-vertex">A</text>
  <text x="498" y="58" class="label-vertex">B</text>
  <text x="396" y="204" class="label-vertex">C</text>
  <text x="46" y="200" class="label-vertex">D</text>
  <text x="306" y="50" class="label-vertex">E</text>
  <text x="234" y="210" class="label-vertex">F</text>
</svg>"""

# ==============================================================================
# 7. HÌNH 3.33: Thực hành 2 - Sợi dây xích chia 4 đoạn móc thành tứ giác ABCD
# ==============================================================================
svg_hinh_3_33 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 230" width="480" height="230">
  <rect width="480" height="230" fill="#ffffff"/>
  <defs>
    <style>
      .chain-link { stroke: #4b5563; stroke-width: 2.2; stroke-dasharray: 6 3; stroke-linecap: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .tick-mark { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; }
    </style>
  </defs>

  <!-- Tứ giác ABCD hình thành từ dây xích: A=(150, 50), B=(410, 50), C=(340, 180), D=(80, 180) -->
  <line x1="150" y1="50" x2="410" y2="50" class="chain-link"/>
  <line x1="410" y1="50" x2="340" y2="180" class="chain-link"/>
  <line x1="340" y1="180" x2="80" y2="180" class="chain-link"/>
  <line x1="80" y1="180" x2="150" y2="50" class="chain-link"/>

  <!-- Vạch bằng nhau: AB = CD (1 vạch), AD = BC (2 vạch) -->
  <line x1="280" y1="44" x2="280" y2="56" class="tick-mark"/>
  <line x1="210" y1="174" x2="210" y2="186" class="tick-mark"/>

  <line x1="112" y1="118" x2="120" y2="112" class="tick-mark"/>
  <line x1="116" y1="123" x2="124" y2="117" class="tick-mark"/>

  <line x1="372" y1="118" x2="380" y2="112" class="tick-mark"/>
  <line x1="376" y1="123" x2="384" y2="117" class="tick-mark"/>

  <!-- Móc nối tại 4 đỉnh -->
  <circle cx="150" cy="50" r="4" fill="#ffffff" stroke="#111827" stroke-width="2"/>
  <circle cx="410" cy="50" r="4" fill="#ffffff" stroke="#111827" stroke-width="2"/>
  <circle cx="340" cy="180" r="4" fill="#ffffff" stroke="#111827" stroke-width="2"/>
  <circle cx="80" cy="180" r="4" fill="#ffffff" stroke="#111827" stroke-width="2"/>

  <!-- Nhãn điểm -->
  <text x="142" y="40" class="label-vertex">A</text>
  <text x="418" y="48" class="label-vertex">B</text>
  <text x="348" y="194" class="label-vertex">C</text>
  <text x="64" y="190" class="label-vertex">D</text>
</svg>"""

# ==============================================================================
# 8. HÌNH 3.34: Ví dụ 3 - Ba tứ giác nhận biết hình bình hành (a, b, c)
# ==============================================================================
svg_hinh_3_34 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 240" width="720" height="240">
  <rect width="720" height="240" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 17px; font-weight: bold; fill: #111827; }
      .label-fig { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .label-deg { font-family: 'Times New Roman', serif; font-size: 15px; fill: #111827; }
      .tick-mark { stroke: #111827; stroke-width: 1.6; stroke-linecap: round; }
    </style>
  </defs>

  <!-- ================= Hình a: Tứ giác các cạnh đối bằng nhau ================= -->
  <!-- A=(80, 60), B=(200, 60), C=(160, 170), D=(40, 170) -->
  <polygon points="80,60 200,60 160,170 40,170" class="geom-line"/>
  <!-- Vạch 1: AB và CD -->
  <line x1="140" y1="54" x2="140" y2="66" class="tick-mark"/>
  <line x1="100" y1="164" x2="100" y2="176" class="tick-mark"/>
  <!-- Vạch 2: AD và BC -->
  <line x1="57" y1="117" x2="65" y2="111" class="tick-mark"/>
  <line x1="61" y1="122" x2="69" y2="116" class="tick-mark"/>
  <line x1="177" y1="117" x2="185" y2="111" class="tick-mark"/>
  <line x1="181" y1="122" x2="189" y2="116" class="tick-mark"/>
  <!-- Đỉnh a -->
  <circle cx="80" cy="60" r="2.5" class="point-dot"/>
  <circle cx="200" cy="60" r="2.5" class="point-dot"/>
  <circle cx="160" cy="170" r="2.5" class="point-dot"/>
  <circle cx="40" cy="170" r="2.5" class="point-dot"/>
  <text x="72" y="52" class="label-vertex">A</text>
  <text x="206" y="58" class="label-vertex">B</text>
  <text x="166" y="180" class="label-vertex">C</text>
  <text x="26" y="176" class="label-vertex">D</text>
  <text x="115" y="215" class="label-fig">a)</text>

  <!-- ================= Hình b: Tứ giác không phải HBH (góc A=110, D=80, C=100) ================= -->
  <!-- D=(280, 170), C=(390, 170), A=(295, 75), B=(410, 50) -->
  <polygon points="295,75 410,50 390,170 280,170" class="geom-line"/>
  <circle cx="295" cy="75" r="2.5" class="point-dot"/>
  <circle cx="410" cy="50" r="2.5" class="point-dot"/>
  <circle cx="390" cy="170" r="2.5" class="point-dot"/>
  <circle cx="280" cy="170" r="2.5" class="point-dot"/>
  <text x="290" y="65" class="label-vertex">A</text>
  <text x="416" y="48" class="label-vertex">B</text>
  <text x="396" y="182" class="label-vertex">C</text>
  <text x="265" y="176" class="label-vertex">D</text>
  <!-- Số đo các góc -->
  <text x="300" y="94" class="label-deg">110°</text>
  <text x="286" y="162" class="label-deg">80°</text>
  <text x="345" y="162" class="label-deg">100°</text>
  <text x="340" y="215" class="label-fig">b)</text>

  <!-- ================= Hình c: Tứ giác hai đường chéo cắt nhau tại trung điểm ================= -->
  <!-- A=(540, 60), B=(660, 60), C=(610, 170), D=(490, 170). O=(575, 115) -->
  <polygon points="540,60 660,60 610,170 490,170" class="geom-line"/>
  <line x1="540" y1="60" x2="610" y2="170" class="geom-line"/>
  <line x1="490" y1="170" x2="660" y2="60" class="geom-line"/>
  <!-- Vạch chéo AC: OA = OC (2 vạch chéo) -->
  <line x1="552" y1="91" x2="560" y2="85" class="tick-mark"/>
  <line x1="556" y1="95" x2="564" y2="89" class="tick-mark"/>
  <line x1="586" y1="145" x2="594" y2="139" class="tick-mark"/>
  <line x1="590" y1="149" x2="598" y2="143" class="tick-mark"/>
  <!-- Vạch BD: OB = OD (1 vạch) -->
  <line x1="530" y1="144" x2="538" y2="138" class="tick-mark"/>
  <line x1="614" y1="89" x2="622" y2="83" class="tick-mark"/>
  <!-- Đỉnh c -->
  <circle cx="540" cy="60" r="2.5" class="point-dot"/>
  <circle cx="660" cy="60" r="2.5" class="point-dot"/>
  <circle cx="610" cy="170" r="2.5" class="point-dot"/>
  <circle cx="490" cy="170" r="2.5" class="point-dot"/>
  <text x="532" y="52" class="label-vertex">A</text>
  <text x="668" y="58" class="label-vertex">B</text>
  <text x="618" y="180" class="label-vertex">C</text>
  <text x="475" y="176" class="label-vertex">D</text>
  <text x="570" y="215" class="label-fig">c)</text>
</svg>"""

# ==============================================================================
# 9. HÌNH 3.35: Bài 3.14 - Tính các góc còn lại của hình bình hành ABCD (A=100°)
# ==============================================================================
svg_hinh_3_35 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 220" width="460" height="220">
  <rect width="460" height="220" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .label-deg { font-family: 'Times New Roman', serif; font-size: 16px; font-weight: bold; fill: #111827; }
      .label-quest { font-family: 'Times New Roman', serif; font-size: 18px; font-weight: bold; fill: #dc2626; }
      .arc-angle { stroke: #111827; stroke-width: 1.3; fill: none; }
    </style>
  </defs>

  <!-- Hình bình hành ABCD có góc A = 100 độ (góc tù) -->
  <!-- A=(180, 50), B=(410, 50), C=(330, 180), D=(100, 180) -->
  <polygon points="180,50 410,50 330,180 100,180" class="geom-line"/>

  <!-- Cung góc tại A = 100° -->
  <path d="M 160 83 A 28 28 0 0 0 208 50" class="arc-angle"/>
  <text x="188" y="75" class="label-deg">100°</text>

  <!-- Dấu hỏi tại B, C, D -->
  <text x="382" y="75" class="label-quest">?</text>
  <text x="306" y="168" class="label-quest">?</text>
  <text x="122" y="168" class="label-quest">?</text>

  <!-- Đỉnh -->
  <circle cx="180" cy="50" r="2.5" class="point-dot"/>
  <circle cx="410" cy="50" r="2.5" class="point-dot"/>
  <circle cx="330" cy="180" r="2.5" class="point-dot"/>
  <circle cx="100" cy="180" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="172" y="40" class="label-vertex">A</text>
  <text x="418" y="48" class="label-vertex">B</text>
  <text x="336" y="196" class="label-vertex">C</text>
  <text x="84" y="190" class="label-vertex">D</text>
</svg>"""

# ==============================================================================
# 10. HÌNH 3.36: Bài 3.16 - Ba hình a, b, c nhận biết hình bình hành
# ==============================================================================
svg_hinh_3_36 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 230" width="720" height="230">
  <rect width="720" height="230" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 17px; font-weight: bold; fill: #111827; }
      .label-fig { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .label-deg { font-family: 'Times New Roman', serif; font-size: 14px; fill: #111827; }
      .right-angle { stroke: #111827; stroke-width: 1.3; fill: none; }
    </style>
  </defs>

  <!-- ================= Hình a: A=100°, B=80°, C=100° => HBH ================= -->
  <!-- A=(80, 50), B=(200, 50), C=(180, 160), D=(60, 160) -->
  <polygon points="80,50 200,50 180,160 60,160" class="geom-line"/>
  <circle cx="80" cy="50" r="2.5" class="point-dot"/>
  <circle cx="200" cy="50" r="2.5" class="point-dot"/>
  <circle cx="180" cy="160" r="2.5" class="point-dot"/>
  <circle cx="60" cy="160" r="2.5" class="point-dot"/>
  <text x="70" y="42" class="label-vertex">A</text>
  <text x="206" y="48" class="label-vertex">B</text>
  <text x="186" y="172" class="label-vertex">C</text>
  <text x="46" y="168" class="label-vertex">D</text>
  <text x="86" y="70" class="label-deg">100°</text>
  <text x="168" y="70" class="label-deg">80°</text>
  <text x="144" y="150" class="label-deg">100°</text>
  <text x="120" y="205" class="label-fig">a)</text>

  <!-- ================= Hình b: A=75°, D=90°, C=75° => Không phải HBH ================= -->
  <!-- D=(280, 160), C=(380, 160), A=(295, 60), B=(380, 110) -->
  <polygon points="295,60 380,110 380,160 280,160" class="geom-line"/>
  <polyline points="280,148 292,148 292,160" class="right-angle"/>
  <circle cx="295" cy="60" r="2.5" class="point-dot"/>
  <circle cx="380" cy="110" r="2.5" class="point-dot"/>
  <circle cx="380" cy="160" r="2.5" class="point-dot"/>
  <circle cx="280" cy="160" r="2.5" class="point-dot"/>
  <text x="286" y="52" class="label-vertex">A</text>
  <text x="388" y="112" class="label-vertex">B</text>
  <text x="386" y="172" class="label-vertex">C</text>
  <text x="265" y="168" class="label-vertex">D</text>
  <text x="296" y="80" class="label-deg">75°</text>
  <text x="350" y="152" class="label-deg">75°</text>
  <text x="330" y="205" class="label-fig">b)</text>

  <!-- ================= Hình c: A=70°, B=110°, D=110° => HBH ================= -->
  <!-- A=(480, 50), B=(590, 50), C=(620, 160), D=(510, 160) -->
  <polygon points="480,50 590,50 620,160 510,160" class="geom-line"/>
  <circle cx="480" cy="50" r="2.5" class="point-dot"/>
  <circle cx="590" cy="50" r="2.5" class="point-dot"/>
  <circle cx="620" cy="160" r="2.5" class="point-dot"/>
  <circle cx="510" cy="160" r="2.5" class="point-dot"/>
  <text x="470" y="42" class="label-vertex">A</text>
  <text x="596" y="48" class="label-vertex">B</text>
  <text x="626" y="172" class="label-vertex">C</text>
  <text x="496" y="168" class="label-vertex">D</text>
  <text x="492" y="70" class="label-deg">70°</text>
  <text x="562" y="70" class="label-deg">110°</text>
  <text x="515" y="148" class="label-deg">110°</text>
  <text x="550" y="205" class="label-fig">c)</text>
</svg>"""

# ==============================================================================
# 11. HÌNH GEOGEBRA: Mô phỏng biến đổi tứ giác thành hình bình hành (NLS 5.3.TC2a)
# ==============================================================================
svg_hinh_geogebra_bai12 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 270" width="620" height="270">
  <rect width="620" height="270" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" rx="6"/>
  <defs>
    <style>
      .app-bar { fill: #1e293b; }
      .app-title { font-family: sans-serif; font-size: 13px; font-weight: bold; fill: #ffffff; }
      .tool-btn { fill: #334155; rx: 3; }
      .canvas-area { fill: #ffffff; stroke: #e2e8f0; stroke-width: 1; }
      .grid-dot { fill: #cbd5e1; }
      .geom-orig { stroke: #94a3b8; stroke-width: 1.5; stroke-dasharray: 4 3; fill: none; }
      .geom-hbh { stroke: #2563eb; stroke-width: 2.2; fill: rgba(37, 99, 235, 0.08); }
      .vector-arrow { stroke: #16a34a; stroke-width: 1.8; fill: none; marker-end: url(#arrow-green); }
      .point-ctrl { fill: #dc2626; stroke: #ffffff; stroke-width: 2; }
      .point-fixed { fill: #2563eb; stroke: #ffffff; stroke-width: 1.5; }
      .label-pt { font-family: 'Times New Roman', serif; font-style: italic; font-size: 16px; font-weight: bold; fill: #1e293b; }
      .status-text { font-family: 'Segoe UI', sans-serif; font-size: 13px; font-weight: bold; fill: #15803d; }
    </style>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a"/>
    </marker>
  </defs>

  <!-- Thanh tiêu đề GeoGebra -->
  <rect x="0" y="0" width="620" height="32" class="app-bar" rx="6"/>
  <text x="14" y="21" class="app-title">GeoGebra Geometry — Mô phỏng biến đổi tứ giác thành hình bình hành [NLS: 5.3.TC2a]</text>

  <!-- Vùng làm việc đồ họa -->
  <rect x="10" y="38" width="600" height="222" class="canvas-area" rx="4"/>

  <!-- Tứ giác ban đầu trước khi kéo song song (nét đứt xám) -->
  <polygon points="120,80 320,60 380,200 90,210" class="geom-orig"/>
  <text x="80" y="75" class="label-pt" fill="#94a3b8">A₀</text>
  <text x="325" y="55" class="label-pt" fill="#94a3b8">B₀</text>

  <!-- Mũi tên vector kéo đỉnh điều chỉnh song song -->
  <line x1="120" y1="80" x2="160" y2="70" class="vector-arrow"/>
  <line x1="320" y1="60" x2="400" y2="70" class="vector-arrow"/>

  <!-- Hình bình hành hoàn chỉnh sau khi ràng buộc song song (xanh lam) -->
  <!-- A=(160, 70), B=(400, 70), C=(330, 200), D=(90, 200) -->
  <polygon points="160,70 400,70 330,200 90,200" class="geom-hbh"/>

  <!-- Các điểm điều khiển -->
  <circle cx="160" cy="70" r="5" class="point-ctrl"/>
  <circle cx="400" cy="70" r="5" class="point-ctrl"/>
  <circle cx="330" cy="200" r="4" class="point-fixed"/>
  <circle cx="90" cy="200" r="4" class="point-fixed"/>

  <!-- Nhãn điểm -->
  <text x="150" y="60" class="label-pt">A</text>
  <text x="408" y="68" class="label-pt">B</text>
  <text x="338" y="214" class="label-pt">C</text>
  <text x="72" y="210" class="label-pt">D</text>

  <!-- Bảng thông số đo đạc tự động bên phải -->
  <rect x="445" y="48" width="155" height="150" fill="#f1f5f9" stroke="#cbd5e1" rx="4"/>
  <text x="455" y="70" font-family="sans-serif" font-size="12px" font-weight="bold" fill="#334155">Quan hệ hình học:</text>
  <text x="455" y="92" font-family="sans-serif" font-size="12px" fill="#0f172a">• AB // CD: Đúng</text>
  <text x="455" y="112" font-family="sans-serif" font-size="12px" fill="#0f172a">• AD // BC: Đúng</text>
  <text x="455" y="132" font-family="sans-serif" font-size="12px" fill="#0f172a">• AB = CD = 6.0 cm</text>
  <text x="455" y="152" font-family="sans-serif" font-size="12px" fill="#0f172a">• AD = BC = 3.6 cm</text>
  <text x="455" y="180" class="status-text">✓ Hình bình hành</text>
</svg>"""

all_figures = [
    ("hinh_3_27.png", svg_hinh_3_27),
    ("hinh_3_28.png", svg_hinh_3_28),
    ("hinh_3_29.png", svg_hinh_3_29),
    ("hinh_3_30.png", svg_hinh_3_30),
    ("hinh_3_31.png", svg_hinh_3_31),
    ("hinh_3_32.png", svg_hinh_3_32),
    ("hinh_3_33.png", svg_hinh_3_33),
    ("hinh_3_34.png", svg_hinh_3_34),
    ("hinh_3_35.png", svg_hinh_3_35),
    ("hinh_3_36.png", svg_hinh_3_36),
    ("hinh_geogebra_bai12.png", svg_hinh_geogebra_bai12)
]

for filename, svg_str in all_figures:
    out_path = os.path.join(out_dir, filename)
    svg_to_png(svg_str, out_path, scale=2.5)

print("\n--- ALL 11 FIGURES FOR BAI 12 RENDERED SUCCESSFULLY ---")
