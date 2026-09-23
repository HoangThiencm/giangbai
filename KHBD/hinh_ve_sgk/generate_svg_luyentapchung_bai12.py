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
# 1. HÌNH 3.37: Ví dụ 1 - Trung điểm các cạnh hình bình hành ABCD tạo thành HBH EFGH
# ==============================================================================
svg_hinh_3_37 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 250" width="520" height="250">
  <rect width="520" height="250" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .inner-line { stroke: #111827; stroke-width: 2.0; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .tick-mark { stroke: #111827; stroke-width: 1.6; stroke-linecap: round; }
    </style>
  </defs>

  <!-- ABCD: D=(60, 200), C=(420, 200), A=(160, 60), B=(500, 60) (đáy 340, xiên (100, -140)) -->
  <polygon points="160,60 500,60 420,200 60,200" class="geom-line"/>

  <!-- Trung điểm: E=(330, 60) trên AB; F=(460, 130) trên BC; G=(240, 200) trên CD; H=(110, 130) trên DA -->
  <polygon points="330,60 460,130 240,200 110,130" class="inner-line"/>

  <!-- Vạch bằng nhau: AE = EB = DG = GC (1 vạch dọc) -->
  <line x1="245" y1="54" x2="245" y2="66" class="tick-mark"/>
  <line x1="415" y1="54" x2="415" y2="66" class="tick-mark"/>
  <line x1="150" y1="194" x2="150" y2="206" class="tick-mark"/>
  <line x1="330" y1="194" x2="330" y2="206" class="tick-mark"/>

  <!-- Vạch bằng nhau: AH = HD = BF = FC (2 vạch xiên) -->
  <!-- AH: mid=(135, 95), HD: mid=(85, 165) -->
  <line x1="131" y1="99" x2="139" y2="91" class="tick-mark"/>
  <line x1="135" y1="103" x2="143" y2="95" class="tick-mark"/>

  <line x1="81" y1="169" x2="89" y2="161" class="tick-mark"/>
  <line x1="85" y1="173" x2="93" y2="165" class="tick-mark"/>

  <!-- BF: mid=(480, 95), FC: mid=(440, 165) -->
  <line x1="476" y1="99" x2="484" y2="91" class="tick-mark"/>
  <line x1="480" y1="103" x2="488" y2="95" class="tick-mark"/>

  <line x1="436" y1="169" x2="444" y2="161" class="tick-mark"/>
  <line x1="440" y1="173" x2="448" y2="165" class="tick-mark"/>

  <!-- Các điểm -->
  <circle cx="160" cy="60" r="2.5" class="point-dot"/>
  <circle cx="500" cy="60" r="2.5" class="point-dot"/>
  <circle cx="420" cy="200" r="2.5" class="point-dot"/>
  <circle cx="60" cy="200" r="2.5" class="point-dot"/>
  <circle cx="330" cy="60" r="2.5" class="point-dot"/>
  <circle cx="460" cy="130" r="2.5" class="point-dot"/>
  <circle cx="240" cy="200" r="2.5" class="point-dot"/>
  <circle cx="110" cy="130" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="150" y="50" class="label-vertex">A</text>
  <text x="506" y="58" class="label-vertex">B</text>
  <text x="426" y="214" class="label-vertex">C</text>
  <text x="46" y="210" class="label-vertex">D</text>

  <text x="326" y="50" class="label-vertex">E</text>
  <text x="472" y="136" class="label-vertex">F</text>
  <text x="236" y="222" class="label-vertex">G</text>
  <text x="86" y="135" class="label-vertex">H</text>
</svg>"""

# ==============================================================================
# 2. HÌNH 3.38: Ví dụ 2 - Hình bình hành ABCD có AC vuông góc AD (AC=4, AD=3)
# ==============================================================================
svg_hinh_3_38 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 240" width="500" height="240">
  <rect width="500" height="240" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .label-num { font-family: 'Times New Roman', serif; font-size: 16px; font-weight: bold; fill: #111827; }
      .right-angle { stroke: #111827; stroke-width: 1.4; fill: none; }
    </style>
  </defs>

  <!-- Tam giác ADC vuông tại A: AD=3, AC=4. Giả sử A=(170, 70). Vector AC=(160, 120) độ dài 200 (tỷ lệ 4: 50px/đơn vị). -->
  <!-- Vector AD vuông góc AC: chiều (-120, 90) độ dài 150 (tỷ lệ 3). -->
  <!-- D = A + (-120, 90) = (50, 160) -->
  <!-- C = A + (160, 120) = (330, 190) -->
  <!-- Vector DC = C - D = (280, 30). B = A + DC = (170+280, 70+30) = (450, 100) -->
  <polygon points="170,70 450,100 330,190 50,160" class="geom-line"/>
  <line x1="170" y1="70" x2="330" y2="190" class="geom-line"/>

  <!-- Ký hiệu góc vuông tại A (giữa AD và AC) -->
  <!-- AD vector: (-0.8, 0.6) * 12 = (-9.6, 7.2). AC vector: (0.8, 0.6) * 12 = (9.6, 7.2) -->
  <polyline points="160,77 170,84 180,77" class="right-angle"/>

  <!-- Ký hiệu góc vuông tại C (giữa CB và CA) -->
  <!-- CB vector: (0.8, -0.6) * 12 = (9.6, -7.2). CA vector: (-0.8, -0.6) * 12 = (-9.6, -7.2) -->
  <polyline points="340,183 330,176 320,183" class="right-angle"/>

  <!-- Số đo độ dài: AD = 3, AC = 4 -->
  <text x="96" y="110" class="label-num">3</text>
  <text x="260" y="125" class="label-num">4</text>

  <!-- Điểm -->
  <circle cx="170" cy="70" r="2.5" class="point-dot"/>
  <circle cx="450" cy="100" r="2.5" class="point-dot"/>
  <circle cx="330" cy="190" r="2.5" class="point-dot"/>
  <circle cx="50" cy="160" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="162" y="58" class="label-vertex">A</text>
  <text x="458" y="105" class="label-vertex">B</text>
  <text x="338" y="206" class="label-vertex">C</text>
  <text x="32" y="166" class="label-vertex">D</text>
</svg>"""

# ==============================================================================
# 3. HÌNH 3.39: Bài 3.19 - Ba hình a, b, c nhận biết hình bình hành
# ==============================================================================
svg_hinh_3_39 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 230" width="720" height="230">
  <rect width="720" height="230" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 17px; font-weight: bold; fill: #111827; }
      .label-fig { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .label-deg { font-family: 'Times New Roman', serif; font-size: 14px; fill: #111827; }
      .arc-angle { stroke: #111827; stroke-width: 1.3; fill: none; }
      .tick-mark { stroke: #111827; stroke-width: 1.6; stroke-linecap: round; }
    </style>
  </defs>

  <!-- ================= Hình a: Tứ giác các góc đối bằng nhau (A=C, B=D) ================= -->
  <!-- A=(80, 50), B=(200, 50), C=(170, 160), D=(50, 160) -->
  <polygon points="80,50 200,50 170,160 50,160" class="geom-line"/>
  <!-- Cung góc A và C (1 vòng cung) -->
  <path d="M 68 64 A 20 20 0 0 0 98 50" class="arc-angle"/>
  <path d="M 182 146 A 20 20 0 0 0 152 160" class="arc-angle"/>
  <!-- Cung góc B và D (2 vòng cung hoặc cung có gạch) -->
  <path d="M 183 50 A 20 20 0 0 1 192 69" class="arc-angle"/>
  <line x1="184" y1="57" x2="191" y2="64" class="tick-mark"/>
  <path d="M 67 160 A 20 20 0 0 1 58 141" class="arc-angle"/>
  <line x1="60" y1="153" x2="67" y2="146" class="tick-mark"/>

  <circle cx="80" cy="50" r="2.5" class="point-dot"/>
  <circle cx="200" cy="50" r="2.5" class="point-dot"/>
  <circle cx="170" cy="160" r="2.5" class="point-dot"/>
  <circle cx="50" cy="160" r="2.5" class="point-dot"/>
  <text x="72" y="42" class="label-vertex">A</text>
  <text x="206" y="48" class="label-vertex">B</text>
  <text x="176" y="172" class="label-vertex">C</text>
  <text x="36" y="168" class="label-vertex">D</text>
  <text x="120" y="205" class="label-fig">a)</text>

  <!-- ================= Hình b: A=110°, B=70°, D=75° => Không phải HBH ================= -->
  <!-- D=(280, 160), C=(380, 160), A=(295, 55), B=(390, 45) -->
  <polygon points="295,55 390,45 380,160 280,160" class="geom-line"/>
  <circle cx="295" cy="55" r="2.5" class="point-dot"/>
  <circle cx="390" cy="45" r="2.5" class="point-dot"/>
  <circle cx="380" cy="160" r="2.5" class="point-dot"/>
  <circle cx="280" cy="160" r="2.5" class="point-dot"/>
  <text x="286" y="48" class="label-vertex">A</text>
  <text x="396" y="45" class="label-vertex">B</text>
  <text x="386" y="172" class="label-vertex">C</text>
  <text x="265" y="168" class="label-vertex">D</text>
  <text x="300" y="75" class="label-deg">110°</text>
  <text x="366" y="68" class="label-deg">70°</text>
  <text x="286" y="150" class="label-deg">75°</text>
  <text x="330" y="205" class="label-fig">b)</text>

  <!-- ================= Hình c: Hình thang cân AD=BC, D=80°, C=80° (kéo dài đáy CD) ================= -->
  <!-- D=(500, 160), C=(640, 160), A=(525, 55), B=(615, 55). Kéo dài CD sang hai bên -->
  <line x1="470" y1="160" x2="670" y2="160" class="geom-line"/>
  <polygon points="525,55 615,55 640,160 500,160" class="geom-line"/>
  <!-- Vạch AD = BC -->
  <line x1="508" y1="104" x2="518" y2="110" class="tick-mark"/>
  <line x1="622" y1="110" x2="632" y2="104" class="tick-mark"/>
  <!-- Góc 80° tại D và C -->
  <text x="508" y="152" class="label-deg">80°</text>
  <text x="618" y="152" class="label-deg">80°</text>

  <circle cx="525" cy="55" r="2.5" class="point-dot"/>
  <circle cx="615" cy="55" r="2.5" class="point-dot"/>
  <circle cx="640" cy="160" r="2.5" class="point-dot"/>
  <circle cx="500" cy="160" r="2.5" class="point-dot"/>
  <text x="518" y="46" class="label-vertex">A</text>
  <text x="620" y="46" class="label-vertex">B</text>
  <text x="646" y="172" class="label-vertex">C</text>
  <text x="486" y="168" class="label-vertex">D</text>
  <text x="565" y="205" class="label-fig">c)</text>
</svg>"""

# ==============================================================================
# 4. HÌNH BÀI 3.20: Hình bình hành ABCD, AM = CN
# ==============================================================================
svg_hinh_bai_3_20 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 230" width="500" height="230">
  <rect width="500" height="230" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .dash-line { stroke: #2563eb; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .tick-mark { stroke: #111827; stroke-width: 1.6; stroke-linecap: round; }
    </style>
  </defs>

  <!-- ABCD: D=(60, 180), C=(420, 180), A=(150, 50), B=(510, 50). Đáy 360 -->
  <polygon points="150,50 510,50 420,180 60,180" class="geom-line"/>

  <!-- AM = CN: Giả sử AM = 110 => M=(260, 50). CN = 110 => N=(310, 180) -->
  <line x1="260" y1="50" x2="420" y2="180" class="dash-line"/>
  <line x1="150" y1="50" x2="310" y2="180" class="dash-line"/>

  <!-- Vạch bằng nhau AM = CN (1 vạch) -->
  <line x1="205" y1="44" x2="205" y2="56" class="tick-mark"/>
  <line x1="365" y1="174" x2="365" y2="186" class="tick-mark"/>

  <!-- Điểm -->
  <circle cx="150" cy="50" r="2.5" class="point-dot"/>
  <circle cx="510" cy="50" r="2.5" class="point-dot"/>
  <circle cx="420" cy="180" r="2.5" class="point-dot"/>
  <circle cx="60" cy="180" r="2.5" class="point-dot"/>
  <circle cx="260" cy="50" r="2.5" class="point-dot"/>
  <circle cx="310" cy="180" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="140" y="42" class="label-vertex">A</text>
  <text x="516" y="52" class="label-vertex">B</text>
  <text x="426" y="194" class="label-vertex">C</text>
  <text x="45" y="190" class="label-vertex">D</text>
  <text x="256" y="40" class="label-vertex">M</text>
  <text x="306" y="202" class="label-vertex">N</text>
</svg>"""

# ==============================================================================
# 5. HÌNH BÀI 3.22: Phân giác góc A trong hình bình hành ABCD cắt CD tại K
# ==============================================================================
svg_hinh_bai_3_22 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 240" width="500" height="240">
  <rect width="500" height="240" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .arc-angle { stroke: #111827; stroke-width: 1.3; fill: none; }
      .label-num { font-family: 'Times New Roman', serif; font-size: 15px; font-weight: bold; fill: #111827; }
      .tick-mark { stroke: #111827; stroke-width: 1.6; stroke-linecap: round; }
    </style>
  </defs>

  <!-- ABCD: AB=3, AD=5. Tỷ lệ: 1cm = 40px => AB=120, AD=200 -->
  <!-- D=(60, 190), C=(420, 190) (đáy CD=9cm=360px) -->
  <!-- A=(180, 50), B=(540, 50)? Không, đề bài: AB = 3 cm, AD = 5 cm => AB < AD. -->
  <!-- D=(60, 190), C=(180, 190) (CD=3cm=120px). AD=5cm: (120, -140), A=(180, 50), B=(300, 50). -->
  <!-- Nhận xét: Trong hình bình hành ABCD có AB = 3 cm, AD = 5 cm. -->
  <!-- Phân giác góc A cắt cạnh CD hay cạnh BC? -->
  <!-- Vì AD = 5 cm > AB = 3 cm, tam giác cân nếu cắt CD thì DK = AD = 5 cm > CD (3 cm) => K nằm ngoài đoạn CD! -->
  <!-- Do đó tia phân giác của góc A phải cắt cạnh BC chứ không cắt đoạn CD! -->
  <!-- Hãy vẽ chuẩn: A=(100, 60), B=(240, 60) (AB=3.5). D=(40, 200), C=(180, 200). AD=5. Tia phân giác góc A cắt BC tại K! -->
  <!-- Vector AD = (-60, 140) độ dài ~152. Vector AB = (140, 0) độ dài 140. -->
  <!-- Phân giác góc A: tam giác ABK cân tại B => BK = AB = 3.5 => K nằm trên cạnh BC! -->
  <!-- Nối BC: B=(240, 60), C=(180, 200). K trên đoạn BC sao cho BK = BA = 140px! -->
  <polygon points="100,60 250,60 190,200 40,200" class="geom-line"/>

  <!-- K trên cạnh BC: B=(250, 60), C=(190, 200). Vector BC = (-60, 140). -->
  <!-- Tỷ lệ BK / BC = AB / AD = 3 / 5 = 0.6. K = B + 0.6*(-60, 140) = (214, 144) -->
  <line x1="100" y1="60" x2="214" y2="144" class="geom-line"/>

  <!-- Cung góc phân giác tại A -->
  <path d="M 125 60 A 25 25 0 0 1 120 75" class="arc-angle"/>
  <path d="M 120 75 A 25 25 0 0 1 110 88" class="arc-angle"/>

  <!-- Ký hiệu bằng nhau AB = BK -->
  <line x1="175" y1="54" x2="175" y2="66" class="tick-mark"/>
  <line x1="230" y1="105" x2="238" y2="99" class="tick-mark"/>

  <!-- Độ dài nhãn -->
  <text x="165" y="48" class="label-num">3 cm</text>
  <text x="45" y="125" class="label-num">5 cm</text>

  <!-- Điểm -->
  <circle cx="100" cy="60" r="2.5" class="point-dot"/>
  <circle cx="250" cy="60" r="2.5" class="point-dot"/>
  <circle cx="190" cy="200" r="2.5" class="point-dot"/>
  <circle cx="40" cy="200" r="2.5" class="point-dot"/>
  <circle cx="214" cy="144" r="2.5" class="point-dot"/>

  <!-- Nhãn điểm -->
  <text x="90" y="52" class="label-vertex">A</text>
  <text x="258" y="58" class="label-vertex">B</text>
  <text x="196" y="214" class="label-vertex">C</text>
  <text x="26" y="210" class="label-vertex">D</text>
  <text x="222" y="148" class="label-vertex">K</text>
</svg>"""

# ==============================================================================
# 6. HÌNH BÀI 3.24: Ba điểm không thẳng hàng tạo thành 3 hình bình hành
# ==============================================================================
svg_hinh_bai_3_24 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="540" height="260">
  <rect width="540" height="260" fill="#ffffff"/>
  <defs>
    <style>
      .base-triangle { stroke: #111827; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; fill: rgba(17, 24, 39, 0.04); }
      .hbh-line1 { stroke: #2563eb; stroke-width: 1.6; stroke-dasharray: 5 4; fill: none; }
      .hbh-line2 { stroke: #16a34a; stroke-width: 1.6; stroke-dasharray: 5 4; fill: none; }
      .hbh-line3 { stroke: #dc2626; stroke-width: 1.6; stroke-dasharray: 5 4; fill: none; }
      .point-dot { fill: #111827; }
      .point-new { fill: #dc2626; stroke: #ffffff; stroke-width: 1.5; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 19px; font-weight: bold; fill: #111827; }
      .label-new { font-family: 'Times New Roman', serif; font-style: italic; font-size: 17px; font-weight: bold; fill: #dc2626; }
    </style>
  </defs>

  <!-- Tam giác cơ sở ABC: A=(260, 70), B=(150, 190), C=(370, 190) -->
  <polygon points="260,70 150,190 370,190" class="base-triangle"/>

  <!-- Điểm D1: ABD1C là hình bình hành => D1 = B + C - A = (150+370-260, 190+190-70) = (260, 310) -> hơi sâu xuống -->
  <!-- Hãy chỉnh tọa độ ABC: A=(270, 110), B=(170, 190), C=(370, 190) -->
  <!-- D1 (đối diện A qua BC): D1 = (270, 270) -->
  <!-- D2 (đối diện B qua AC): D2 = A + C - B = (270+370-170, 110+190-190) = (470, 110) -->
  <!-- D3 (đối diện C qua AB): D3 = A + B - C = (270+170-370, 110+190-190) = (70, 110) -->

  <!-- HBH 1: AD2CB (xanh lam) qua D2(470, 110) -->
  <line x1="270" y1="110" x2="470" y2="110" class="hbh-line1"/>
  <line x1="370" y1="190" x2="470" y2="110" class="hbh-line1"/>

  <!-- HBH 2: D3ACB (xanh lá) qua D3(70, 110) -->
  <line x1="270" y1="110" x2="70" y2="110" class="hbh-line2"/>
  <line x1="170" y1="190" x2="70" y2="110" class="hbh-line2"/>

  <!-- HBH 3: ABD1C (đỏ) qua D1(270, 270) -> trong khung (270, 240) với A=(270, 90), B=(180, 165), C=(360, 165) -->
  <!-- Hãy dùng: A=(270, 80), B=(190, 160), C=(350, 160) -->
  <!-- D1 = (270, 240); D2 = (430, 80); D3 = (110, 80) -->
  <line x1="190" y1="160" x2="270" y2="240" class="hbh-line3"/>
  <line x1="350" y1="160" x2="270" y2="240" class="hbh-line3"/>

  <!-- Cạnh D2 -->
  <line x1="270" y1="80" x2="430" y2="80" class="hbh-line1"/>
  <line x1="350" y1="160" x2="430" y2="80" class="hbh-line1"/>

  <!-- Cạnh D3 -->
  <line x1="270" y1="80" x2="110" y2="80" class="hbh-line2"/>
  <line x1="190" y1="160" x2="110" y2="80" class="hbh-line2"/>

  <!-- Các điểm đỉnh A, B, C -->
  <circle cx="270" cy="80" r="3.5" class="point-dot"/>
  <circle cx="190" cy="160" r="3.5" class="point-dot"/>
  <circle cx="350" cy="160" r="3.5" class="point-dot"/>

  <!-- Ba điểm D1, D2, D3 -->
  <circle cx="270" cy="240" r="3.5" class="point-new"/>
  <circle cx="430" cy="80" r="3.5" class="point-new"/>
  <circle cx="110" cy="80" r="3.5" class="point-new"/>

  <!-- Nhãn điểm -->
  <text x="264" y="65" class="label-vertex">A</text>
  <text x="170" y="168" class="label-vertex">B</text>
  <text x="358" y="168" class="label-vertex">C</text>

  <text x="264" y="258" class="label-new">D₁</text>
  <text x="438" y="86" class="label-new">D₂</text>
  <text x="82" y="86" class="label-new">D₃</text>
</svg>"""

# ==============================================================================
# 7. HÌNH GEOGEBRA: Thực nghiệm số các dấu hiệu nhận biết HBH (NLS 5.2.TC2b)
# ==============================================================================
svg_hinh_geogebra_ltc_bai12 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 270" width="620" height="270">
  <rect width="620" height="270" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" rx="6"/>
  <defs>
    <style>
      .app-bar { fill: #1e293b; }
      .app-title { font-family: sans-serif; font-size: 13px; font-weight: bold; fill: #ffffff; }
      .canvas-area { fill: #ffffff; stroke: #e2e8f0; stroke-width: 1; }
      .geom-hbh { stroke: #2563eb; stroke-width: 2.2; fill: rgba(37, 99, 235, 0.08); }
      .diag-line { stroke: #dc2626; stroke-width: 1.6; stroke-dasharray: 4 3; fill: none; }
      .point-ctrl { fill: #dc2626; stroke: #ffffff; stroke-width: 2; }
      .point-fixed { fill: #2563eb; stroke: #ffffff; stroke-width: 1.5; }
      .label-pt { font-family: 'Times New Roman', serif; font-style: italic; font-size: 16px; font-weight: bold; fill: #1e293b; }
      .status-text { font-family: 'Segoe UI', sans-serif; font-size: 13px; font-weight: bold; fill: #15803d; }
    </style>
  </defs>

  <!-- Thanh tiêu đề GeoGebra -->
  <rect x="0" y="0" width="620" height="32" class="app-bar" rx="6"/>
  <text x="14" y="21" class="app-title">GeoGebra — Thực nghiệm kiểm chứng 5 dấu hiệu nhận biết hình bình hành [NLS: 5.2.TC2b]</text>

  <!-- Vùng làm việc đồ họa -->
  <rect x="10" y="38" width="600" height="222" class="canvas-area" rx="4"/>

  <!-- Hình bình hành ABCD và hai đường chéo cắt nhau tại O -->
  <polygon points="140,75 380,75 310,195 70,195" class="geom-hbh"/>
  <line x1="140" y1="75" x2="310" y2="195" class="diag-line"/>
  <line x1="70" y1="195" x2="380" y2="75" class="diag-line"/>

  <!-- Các điểm điều khiển -->
  <circle cx="140" cy="75" r="4.5" class="point-ctrl"/>
  <circle cx="380" cy="75" r="4.5" class="point-ctrl"/>
  <circle cx="310" cy="195" r="4" class="point-fixed"/>
  <circle cx="70" cy="195" r="4" class="point-fixed"/>
  <circle cx="225" cy="135" r="3.5" fill="#dc2626"/>

  <!-- Nhãn điểm -->
  <text x="130" y="65" class="label-pt">A</text>
  <text x="388" y="72" class="label-pt">B</text>
  <text x="318" y="210" class="label-pt">C</text>
  <text x="52" y="205" class="label-pt">D</text>
  <text x="232" y="140" class="label-pt" fill="#dc2626">O</text>

  <!-- Bảng kiểm chứng thực nghiệm số bên phải -->
  <rect x="420" y="48" width="180" height="155" fill="#f1f5f9" stroke="#cbd5e1" rx="4"/>
  <text x="430" y="70" font-family="sans-serif" font-size="12px" font-weight="bold" fill="#334155">Kết quả kiểm chứng số:</text>
  <text x="430" y="92" font-family="sans-serif" font-size="12px" fill="#0f172a">• Đo cạnh: AB = CD = 6.00</text>
  <text x="430" y="112" font-family="sans-serif" font-size="12px" fill="#0f172a">• Đo cạnh: AD = BC = 3.61</text>
  <text x="430" y="132" font-family="sans-serif" font-size="12px" fill="#0f172a">• Đo góc: ∠A = ∠C = 120°</text>
  <text x="430" y="152" font-family="sans-serif" font-size="12px" fill="#0f172a">• Trung điểm: OA = OC = 3.0</text>
  <text x="430" y="180" class="status-text">✓ Thỏa mãn 5 dấu hiệu HBH</text>
</svg>"""

all_figures = [
    ("hinh_3_37.png", svg_hinh_3_37),
    ("hinh_3_38.png", svg_hinh_3_38),
    ("hinh_3_39.png", svg_hinh_3_39),
    ("hinh_bai_3_20.png", svg_hinh_bai_3_20),
    ("hinh_bai_3_22.png", svg_hinh_bai_3_22),
    ("hinh_bai_3_24.png", svg_hinh_bai_3_24),
    ("hinh_geogebra_ltc_bai12.png", svg_hinh_geogebra_ltc_bai12)
]

for filename, svg_str in all_figures:
    out_path = os.path.join(out_dir, filename)
    svg_to_png(svg_str, out_path, scale=2.5)

print("\n--- ALL 7 FIGURES FOR LUYEN TAP CHUNG TIET 7 RENDERED SUCCESSFULLY ---")
