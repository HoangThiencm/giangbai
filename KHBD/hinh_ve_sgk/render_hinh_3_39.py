import sys
import math
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, QSize

app = QGuiApplication.instance() or QGuiApplication(sys.argv)

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 240" width="740" height="240">
  <rect width="740" height="240" fill="#ffffff"/>
  <defs>
    <style>
      .geom-line { stroke: #111827; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; fill: none; }
      .point-dot { fill: #111827; }
      .label-vertex { font-family: 'Times New Roman', serif; font-style: italic; font-size: 18px; font-weight: bold; fill: #111827; }
      .label-fig { font-family: 'Times New Roman', serif; font-style: italic; font-size: 19px; font-weight: bold; fill: #111827; }
      .label-deg { font-family: 'Times New Roman', serif; font-size: 14px; fill: #111827; }
      .arc-angle { stroke: #111827; stroke-width: 1.3; stroke-linecap: round; fill: none; }
      .tick-mark { stroke: #111827; stroke-width: 1.5; stroke-linecap: round; }
    </style>
  </defs>

  <!-- ================= Hình a: Tứ giác các góc đối bằng nhau (A=C, B=D) ================= -->
  <!-- A=(85, 60), B=(205, 60), C=(170, 165), D=(50, 165) -->
  <polygon points="85,60 205,60 170,165 50,165" class="geom-line"/>

  <!-- Góc A: Cung đơn bán kính 24 từ cạnh AB đến cạnh AD -->
  <path d="M 109 60 A 24 24 0 0 1 77.41 82.77" class="arc-angle"/>

  <!-- Góc C: Cung đơn bán kính 24 từ cạnh CD đến cạnh CB -->
  <path d="M 146 165 A 24 24 0 0 1 177.59 142.23" class="arc-angle"/>

  <!-- Góc D: Cung có gạch chéo vuông góc -->
  <path d="M 57.59 142.23 A 24 24 0 0 1 74 165" class="arc-angle"/>
  <line x1="65.4" y1="153.9" x2="73.5" y2="148.1" class="tick-mark"/>

  <!-- Góc B: Cung có gạch chéo vuông góc -->
  <path d="M 197.41 82.77 A 24 24 0 0 1 181 60" class="arc-angle"/>
  <line x1="189.6" y1="71.1" x2="181.5" y2="77.0" class="tick-mark"/>

  <!-- Đỉnh Hình a -->
  <circle cx="85" cy="60" r="2.2" class="point-dot"/>
  <circle cx="205" cy="60" r="2.2" class="point-dot"/>
  <circle cx="170" cy="165" r="2.2" class="point-dot"/>
  <circle cx="50" cy="165" r="2.2" class="point-dot"/>
  <text x="75" y="50" class="label-vertex">A</text>
  <text x="212" y="58" class="label-vertex">B</text>
  <text x="175" y="178" class="label-vertex">C</text>
  <text x="34" y="173" class="label-vertex">D</text>
  <text x="120" y="215" class="label-fig">a)</text>

  <!-- ================= Hình b: A=110°, B=70°, D=75° => Không phải HBH ================= -->
  <!-- D=(285, 165), C=(390, 165), A=(295, 60), B=(400, 50) -->
  <polygon points="295,60 400,50 390,165 285,165" class="geom-line"/>
  <circle cx="295" cy="60" r="2.2" class="point-dot"/>
  <circle cx="400" cy="50" r="2.2" class="point-dot"/>
  <circle cx="390" cy="165" r="2.2" class="point-dot"/>
  <circle cx="285" cy="165" r="2.2" class="point-dot"/>
  <text x="285" y="50" class="label-vertex">A</text>
  <text x="406" y="48" class="label-vertex">B</text>
  <text x="396" y="178" class="label-vertex">C</text>
  <text x="268" y="173" class="label-vertex">D</text>
  <text x="302" y="80" class="label-deg">110°</text>
  <text x="374" y="72" class="label-deg">70°</text>
  <text x="292" y="153" class="label-deg">75°</text>
  <text x="335" y="215" class="label-fig">b)</text>

  <!-- ================= Hình c: Hình thang cân AD=BC, D=80°, C=80° ================= -->
  <!-- D=(510, 165), C=(640, 165), A=(535, 60), B=(615, 60) -->
  <line x1="480" y1="165" x2="670" y2="165" class="geom-line"/>
  <polygon points="535,60 615,60 640,165 510,165" class="geom-line"/>
  
  <!-- Vạch bằng nhau AD = BC (vuông góc với cạnh) -->
  <line x1="516" y1="115" x2="528" y2="110" class="tick-mark"/>
  <line x1="622" y1="110" x2="634" y2="115" class="tick-mark"/>
  
  <!-- Số đo 80° tại D và C -->
  <text x="518" y="155" class="label-deg">80°</text>
  <text x="618" y="155" class="label-deg">80°</text>

  <circle cx="535" cy="60" r="2.2" class="point-dot"/>
  <circle cx="615" cy="60" r="2.2" class="point-dot"/>
  <circle cx="640" cy="165" r="2.2" class="point-dot"/>
  <circle cx="510" cy="165" r="2.2" class="point-dot"/>
  <text x="526" y="50" class="label-vertex">A</text>
  <text x="620" y="50" class="label-vertex">B</text>
  <text x="646" y="178" class="label-vertex">C</text>
  <text x="494" y="173" class="label-vertex">D</text>
  <text x="570" y="215" class="label-fig">c)</text>
</svg>"""

renderer = QSvgRenderer(QByteArray(svg.encode('utf-8')))
default_size = renderer.defaultSize()
scale = 2.5
w = int(default_size.width() * scale)
h = int(default_size.height() * scale)

img = QImage(QSize(w, h), QImage.Format_ARGB32)
img.fill(QColor(255, 255, 255, 255))

painter = QPainter(img)
renderer.render(painter)
painter.end()

out_paths = [
    'KHBD/hinh_ve_sgk/hinh_3_39.png',
    'GIAO AN/hinh_ve_sgk/hinh_3_39.png'
]

for out_path in out_paths:
    try:
        img.save(out_path, 'PNG')
        print(f"Rendered successfully: {out_path} ({w}x{h})")
    except Exception as e:
        print(f"Error saving {out_path}: {e}")
