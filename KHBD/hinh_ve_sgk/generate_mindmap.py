import os
import sys
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, QSize

out_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(out_dir, exist_ok=True)

svg_mindmap = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 460" width="840" height="460">
  <rect width="840" height="460" fill="#ffffff" rx="8"/>
  <defs>
    <style>
      .node-core { fill: #1e3a8a; stroke: #172554; stroke-width: 2.5; rx: 12; }
      .text-core { font-family: 'Times New Roman', serif; font-size: 22px; font-weight: bold; fill: #ffffff; text-anchor: middle; }
      
      .node-branch { fill: #eff6ff; stroke: #2563eb; stroke-width: 2; rx: 8; }
      .title-branch { font-family: 'Times New Roman', serif; font-size: 16px; font-weight: bold; fill: #1e40af; }
      .text-content { font-family: 'Times New Roman', serif; font-size: 14.5px; fill: #0f172a; }
      .math-italic { font-family: 'Times New Roman', serif; font-style: italic; font-weight: bold; }
      
      .conn-line { stroke: #3b82f6; stroke-width: 2; fill: none; }
      .tag-num { fill: #2563eb; rx: 3; }
      .tag-text { font-family: sans-serif; font-size: 11px; font-weight: bold; fill: #ffffff; text-anchor: middle; }
    </style>
  </defs>

  <!-- ĐƯỜNG KẾT NỐI TỪ TRUNG TÂM -->
  <path d="M 420 180 C 420 80, 240 70, 240 70" class="conn-line"/>
  <path d="M 420 220 C 420 310, 250 310, 250 310" class="conn-line"/>
  <path d="M 420 200 C 520 200, 520 200, 560 200" class="conn-line"/>

  <!-- KHỐI TRUNG TÂM -->
  <rect x="290" y="175" width="260" height="70" class="node-core"/>
  <text x="420" y="218" class="text-core">HÌNH BÌNH HÀNH</text>

  <!-- NHÁNH 1: ĐỊNH NGHĨA -->
  <rect x="20" y="20" width="360" height="95" class="node-branch"/>
  <text x="35" y="46" class="title-branch">I. ĐỊNH NGHĨA</text>
  <text x="35" y="72" class="text-content">• Là tứ giác có các cạnh đối song song:</text>
  <text x="55" y="96" class="text-content"><tspan class="math-italic">AB // CD</tspan>  và  <tspan class="math-italic">AD // BC</tspan></text>

  <!-- NHÁNH 2: TÍNH CHẤT TRỌNG TÂM -->
  <rect x="20" y="145" width="360" height="295" class="node-branch"/>
  <text x="35" y="172" class="title-branch">II. TÍNH CHẤT TRỌNG TÂM</text>
  
  <text x="35" y="202" class="text-content">1. <tspan font-weight="bold">Cạnh đối bằng nhau:</tspan></text>
  <text x="55" y="224" class="text-content"><tspan class="math-italic">AB = CD</tspan>,  <tspan class="math-italic">AD = BC</tspan></text>
  
  <text x="35" y="254" class="text-content">2. <tspan font-weight="bold">Góc đối bằng nhau:</tspan></text>
  <text x="55" y="276" class="text-content"><tspan class="math-italic">∠A = ∠C</tspan>,  <tspan class="math-italic">∠B = ∠D</tspan></text>
  
  <text x="35" y="306" class="text-content">3. <tspan font-weight="bold">Hai đường chéo cắt nhau tại trung điểm:</tspan></text>
  <text x="55" y="328" class="text-content"><tspan class="math-italic">OA = OC</tspan>,  <tspan class="math-italic">OB = OD</tspan> (<tspan class="math-italic">O</tspan> là giao điểm)</text>
  
  <text x="35" y="358" class="text-content">4. <tspan font-weight="bold">Hai góc kề một cạnh bù nhau:</tspan></text>
  <text x="55" y="380" class="text-content"><tspan class="math-italic">∠A + ∠B = 180°</tspan>,  <tspan class="math-italic">∠B + ∠C = 180°</tspan></text>

  <!-- NHÁNH 3: 5 DẤU HIỆU NHẬN BIẾT -->
  <rect x="470" y="20" width="350" height="420" class="node-branch" stroke="#16a34a" fill="#f0fdf4"/>
  <text x="485" y="46" class="title-branch" fill="#15803d">III. 5 DẤU HIỆU NHẬN BIẾT</text>

  <!-- Dấu hiệu 1 -->
  <rect x="485" y="65" width="22" height="16" class="tag-num" fill="#16a34a"/>
  <text x="496" y="77" class="tag-text">1</text>
  <text x="515" y="78" class="text-content" font-weight="bold">Theo định nghĩa:</text>
  <text x="515" y="100" class="text-content">Tứ giác có các cạnh đối song song.</text>

  <!-- Dấu hiệu 2 -->
  <rect x="485" y="130" width="22" height="16" class="tag-num" fill="#16a34a"/>
  <text x="496" y="142" class="tag-text">2</text>
  <text x="515" y="143" class="text-content" font-weight="bold">Theo cạnh đối (ĐL 2a):</text>
  <text x="515" y="165" class="text-content">Tứ giác có các cạnh đối bằng nhau.</text>

  <!-- Dấu hiệu 3 -->
  <rect x="485" y="195" width="22" height="16" class="tag-num" fill="#16a34a"/>
  <text x="496" y="207" class="tag-text">3</text>
  <text x="515" y="208" class="text-content" font-weight="bold">Một cặp cạnh đối (ĐL 2b):</text>
  <text x="515" y="230" class="text-content">Có 1 cặp cạnh đối song song và bằng nhau</text>
  <text x="515" y="250" class="text-content">(<tspan class="math-italic">AB // CD</tspan> và <tspan class="math-italic">AB = CD</tspan>).</text>

  <!-- Dấu hiệu 4 -->
  <rect x="485" y="280" width="22" height="16" class="tag-num" fill="#16a34a"/>
  <text x="496" y="292" class="tag-text">4</text>
  <text x="515" y="293" class="text-content" font-weight="bold">Theo góc đối (ĐL 3a):</text>
  <text x="515" y="315" class="text-content">Tứ giác có các góc đối bằng nhau.</text>

  <!-- Dấu hiệu 5 -->
  <rect x="485" y="345" width="22" height="16" class="tag-num" fill="#16a34a"/>
  <text x="496" y="357" class="tag-text">5</text>
  <text x="515" y="358" class="text-content" font-weight="bold">Theo đường chéo (ĐL 3b):</text>
  <text x="515" y="380" class="text-content">Có 2 đường chéo cắt nhau tại trung điểm</text>
  <text x="515" y="400" class="text-content">của mỗi đường.</text>
</svg>"""

renderer = QSvgRenderer(QByteArray(svg_mindmap.encode('utf-8')))
size = renderer.defaultSize()
scale = 2.5
w, h = int(size.width() * scale), int(size.height() * scale)
img = QImage(QSize(w, h), QImage.Format_ARGB32)
img.fill(QColor(255, 255, 255, 255))
painter = QPainter(img)
renderer.render(painter)
painter.end()

out_path = os.path.join(out_dir, 'so_do_tu_duy_hinh_binh_hanh.png')
img.save(out_path, 'PNG')
print('Rendered:', out_path, f'({w}x{h})')
