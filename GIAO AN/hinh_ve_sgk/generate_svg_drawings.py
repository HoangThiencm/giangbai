import os
import sys
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, QSize

app = QGuiApplication.instance() or QGuiApplication(sys.argv)
os.makedirs('GIAO AN/hinh_ve_sgk', exist_ok=True)

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

# 1. HÌNH 3.1: Hoạt động mở đầu (Ghép 4 tứ giác quanh 1 điểm chung) - KHÔNG CÓ CHÚ THÍCH DƯỚI
svg_hinh_3_1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 230" width="540" height="230">
  <rect width="540" height="230" fill="#ffffff"/>
  
  <!-- Hình 3.1a: Một tứ giác ABCD -->
  <g transform="translate(15, 10)">
    <polygon points="120,40 50,170 170,170 150,90" fill="#fef08a" stroke="#000000" stroke-width="2" stroke-linejoin="round"/>
    <circle cx="170" cy="170" r="2.5" fill="#000000"/>
    <circle cx="50" cy="170" r="2.5" fill="#000000"/>
    <circle cx="120" cy="40" r="2.5" fill="#000000"/>
    <circle cx="150" cy="90" r="2.5" fill="#000000"/>
    
    <text x="182" y="180" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold" fill="#0055aa">A</text>
    <text x="35" y="180" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold" fill="#0055aa">B</text>
    <text x="120" y="25" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold" fill="#0055aa">D</text>
    <text x="165" y="95" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold" fill="#0055aa">C</text>
    
    <text x="155" y="160" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" fill="#000000">1</text>
    <text x="68" y="160" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" fill="#000000">2</text>
    <text x="140" y="105" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" fill="#000000">3</text>
    <text x="120" y="65" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" fill="#000000">4</text>
    
    <text x="110" y="205" font-family="'Times New Roman', serif" font-style="italic" font-size="15" fill="#000000">a)</text>
  </g>
  
  <!-- Hình 3.1b: Bốn tứ giác ghép khít quanh điểm chung -->
  <g transform="translate(360, 100)">
    <polygon points="0,0 80,0 60,-80 30,-50" fill="#fef08a" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/>
    <text x="15" y="-12" font-family="'Times New Roman', serif" font-size="13" font-weight="bold">1</text>
    <text x="65" y="-10" font-family="'Times New Roman', serif" font-size="12">2</text>
    <text x="50" y="-65" font-family="'Times New Roman', serif" font-size="12">3</text>
    <text x="25" y="-40" font-family="'Times New Roman', serif" font-size="12">4</text>
    
    <polygon points="0,0 -40,-70 -90,-40 -50,-10" fill="#bae6fd" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/>
    <text x="-8" y="-18" font-family="'Times New Roman', serif" font-size="13" font-weight="bold">4</text>
    <text x="-38" y="-55" font-family="'Times New Roman', serif" font-size="12">1</text>
    <text x="-75" y="-35" font-family="'Times New Roman', serif" font-size="12">2</text>
    <text x="-48" y="-18" font-family="'Times New Roman', serif" font-size="12">3</text>

    <polygon points="0,0 -80,10 -60,80 -20,60" fill="#fbcfe8" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/>
    <text x="-18" y="15" font-family="'Times New Roman', serif" font-size="13" font-weight="bold">2</text>
    <text x="-65" y="18" font-family="'Times New Roman', serif" font-size="12">3</text>
    <text x="-50" y="68" font-family="'Times New Roman', serif" font-size="12">4</text>
    <text x="-20" y="50" font-family="'Times New Roman', serif" font-size="12">1</text>
    
    <polygon points="0,0 20,70 70,50 60,10" fill="#bbf7d0" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/>
    <text x="12" y="18" font-family="'Times New Roman', serif" font-size="13" font-weight="bold">3</text>
    <text x="22" y="58" font-family="'Times New Roman', serif" font-size="12">4</text>
    <text x="60" y="42" font-family="'Times New Roman', serif" font-size="12">1</text>
    <text x="50" y="15" font-family="'Times New Roman', serif" font-size="12">2</text>
    
    <circle cx="0" cy="0" r="3.5" fill="#dc2626"/>
    
    <text x="0" y="115" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="15" fill="#000000">b)</text>
  </g>
</svg>"""

# 2. HÌNH 3.2: Các hình tứ giác (a, b, c, d) - THUẦN HÌNH HỌC KHÔNG CHÚ THÍCH ĐÁP ÁN
svg_hinh_3_2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 200" width="680" height="200">
  <rect width="680" height="200" fill="#ffffff"/>
  
  <!-- Hình a -->
  <g transform="translate(10, 10)">
    <polygon points="20,90 75,30 120,95 75,150" fill="#f8fafc" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/>
    <text x="7" y="95" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">A</text>
    <text x="75" y="20" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">D</text>
    <text x="128" y="100" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">C</text>
    <text x="75" y="168" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">B</text>
    <text x="75" y="190" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="15">a)</text>
  </g>
  
  <!-- Hình b -->
  <g transform="translate(170, 10)">
    <polygon points="20,95 110,25 75,95 110,155" fill="#f8fafc" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/>
    <text x="5" y="98" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">A</text>
    <text x="116" y="25" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">B</text>
    <text x="82" y="102" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">C</text>
    <text x="116" y="165" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">D</text>
    <text x="70" y="190" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="15">b)</text>
  </g>
  
  <!-- Hình c: Tự cắt nhau -->
  <g transform="translate(340, 10)">
    <line x1="20" y1="35" x2="100" y2="35" stroke="#000000" stroke-width="1.8"/>
    <line x1="100" y1="35" x2="20" y2="155" stroke="#000000" stroke-width="1.8"/>
    <line x1="20" y1="155" x2="100" y2="155" stroke="#000000" stroke-width="1.8"/>
    <line x1="100" y1="155" x2="20" y2="35" stroke="#000000" stroke-width="1.8"/>
    <text x="8" y="32" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">A</text>
    <text x="106" y="32" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">D</text>
    <text x="8" y="168" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">C</text>
    <text x="106" y="168" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">B</text>
    <text x="60" y="190" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="15">c)</text>
  </g>
  
  <!-- Hình d: Không phải tứ giác (3 điểm thẳng hàng) -->
  <g transform="translate(500, 10)">
    <polygon points="50,30 10,155 110,155" fill="#f8fafc" stroke="#000000" stroke-width="1.8" stroke-linejoin="round"/>
    <circle cx="60" cy="155" r="2.5" fill="#000000"/>
    <text x="50" y="20" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">A</text>
    <text x="-2" y="165" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">B</text>
    <text x="60" y="172" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">C</text>
    <text x="116" y="165" font-family="'Times New Roman', serif" font-style="italic" font-size="15" font-weight="bold">D</text>
    <text x="60" y="190" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="15">d)</text>
  </g>
</svg>"""

# 3. HÌNH 3.4: Tứ giác ABCD và hai đường chéo
svg_hinh_3_4 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 225" width="360" height="225">
  <rect width="360" height="225" fill="#ffffff"/>
  <polygon points="50,120 180,40 310,110 170,205" fill="#f8fafc" stroke="#000000" stroke-width="2" stroke-linejoin="round"/>
  <!-- Hai đường chéo AC và BD -->
  <line x1="50" y1="120" x2="310" y2="110" stroke="#0284c7" stroke-width="1.6" stroke-dasharray="6,4"/>
  <line x1="180" y1="40" x2="170" y2="205" stroke="#0284c7" stroke-width="1.6" stroke-dasharray="6,4"/>
  
  <circle cx="175" cy="115" r="2.5" fill="#000000"/>
  <text x="187" y="125" font-family="'Times New Roman', serif" font-style="italic" font-size="14" fill="#0284c7">O</text>
  
  <text x="32" y="125" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">A</text>
  <text x="180" y="26" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">D</text>
  <text x="322" y="115" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">C</text>
  <text x="170" y="222" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">B</text>
</svg>"""

# 4. HÌNH 3.5: Kẻ đường chéo BD chia 2 tam giác để chứng minh định lí
svg_hinh_3_5 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 215" width="380" height="215">
  <rect width="380" height="215" fill="#ffffff"/>
  <polygon points="50,110 210,35 340,110 190,195" fill="#f8fafc" stroke="#000000" stroke-width="2" stroke-linejoin="round"/>
  <line x1="50" y1="110" x2="340" y2="110" stroke="#000000" stroke-width="1.8"/>
  
  <path d="M 75,95 A 30,30 0 0,0 78,110" fill="none" stroke="#000000" stroke-width="1.3"/>
  <path d="M 78,110 A 30,30 0 0,0 72,125" fill="none" stroke="#000000" stroke-width="1.3"/>
  <text x="85" y="103" font-family="'Times New Roman', serif" font-size="13">1</text>
  <text x="85" y="125" font-family="'Times New Roman', serif" font-size="13">2</text>
  
  <path d="M 315,95 A 30,30 0 0,1 312,110" fill="none" stroke="#000000" stroke-width="1.3"/>
  <path d="M 312,110 A 30,30 0 0,1 318,125" fill="none" stroke="#000000" stroke-width="1.3"/>
  <text x="303" y="103" font-family="'Times New Roman', serif" font-size="13">1</text>
  <text x="303" y="125" font-family="'Times New Roman', serif" font-size="13">2</text>
  
  <text x="32" y="115" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">D</text>
  <text x="210" y="24" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">A</text>
  <text x="352" y="115" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">B</text>
  <text x="190" y="212" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">C</text>
</svg>"""

# 5. HÌNH 3.6: Ví dụ tính góc D
svg_hinh_3_6 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 230" width="320" height="230">
  <rect width="320" height="230" fill="#ffffff"/>
  <polygon points="60,130 150,45 270,60 190,205" fill="#f8fafc" stroke="#000000" stroke-width="2" stroke-linejoin="round"/>
  
  <text x="75" y="125" font-family="'Times New Roman', serif" font-size="13" fill="#0284c7">110°</text>
  <text x="155" y="75" font-family="'Times New Roman', serif" font-size="13" fill="#0284c7">120°</text>
  <text x="240" y="85" font-family="'Times New Roman', serif" font-size="13" fill="#0284c7">80°</text>
  <text x="180" y="195" font-family="'Times New Roman', serif" font-size="15" font-weight="bold" fill="#dc2626">?</text>
  
  <text x="42" y="135" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">A</text>
  <text x="150" y="32" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">B</text>
  <text x="282" y="65" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">C</text>
  <text x="195" y="222" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">D</text>
</svg>"""

# 6. HÌNH 3.7: Luyện tập 2 tính góc F trong tứ giác EFGH
svg_hinh_3_7 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 230" width="320" height="230">
  <rect width="320" height="230" fill="#ffffff"/>
  <polygon points="60,195 150,45 250,95 250,195" fill="#f8fafc" stroke="#000000" stroke-width="2" stroke-linejoin="round"/>
  
  <polyline points="142,59 155,67 163,53" fill="none" stroke="#000000" stroke-width="1.5"/>
  <polyline points="236,195 236,181 250,181" fill="none" stroke="#000000" stroke-width="1.5"/>
  
  <text x="85" y="190" font-family="'Times New Roman', serif" font-size="13" fill="#0284c7">55°</text>
  <text x="230" y="115" font-family="'Times New Roman', serif" font-size="15" font-weight="bold" fill="#dc2626">?</text>
  
  <text x="42" y="205" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">H</text>
  <text x="150" y="32" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">E</text>
  <text x="262" y="100" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">F</text>
  <text x="262" y="205" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">G</text>
</svg>"""

# 7. HÌNH 3.8: Bài tập 3.1 (Hình 3.8a và 3.8c)
svg_hinh_3_8 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 220" width="520" height="220">
  <rect width="520" height="220" fill="#ffffff"/>
  
  <!-- Hình 3.8a -->
  <g transform="translate(20, 15)">
    <polygon points="40,30 160,30 160,160 40,160" fill="#f8fafc" stroke="#000000" stroke-width="2" stroke-linejoin="round"/>
    <polyline points="40,44 54,44 54,30" fill="none" stroke="#000000" stroke-width="1.5"/>
    <polyline points="160,44 146,44 146,30" fill="none" stroke="#000000" stroke-width="1.5"/>
    <polyline points="40,146 54,146 54,160" fill="none" stroke="#000000" stroke-width="1.5"/>
    
    <text x="140" y="145" font-family="'Times New Roman', serif" font-size="16" font-weight="bold" fill="#dc2626">?</text>
    
    <text x="24" y="28" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">A</text>
    <text x="168" y="28" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">B</text>
    <text x="168" y="172" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">C</text>
    <text x="24" y="172" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">D</text>
    <text x="100" y="195" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="15">a)</text>
  </g>
  
  <!-- Hình 3.8c -->
  <g transform="translate(280, 15)">
    <polygon points="40,160 80,40 180,40 210,160" fill="#f8fafc" stroke="#000000" stroke-width="2" stroke-linejoin="round"/>
    <text x="50" y="145" font-family="'Times New Roman', serif" font-size="13" fill="#0284c7">50°</text>
    <text x="180" y="145" font-family="'Times New Roman', serif" font-size="13" fill="#0284c7">60°</text>
    
    <path d="M 75,55 A 18,18 0 0,0 95,45" fill="none" stroke="#dc2626" stroke-width="1.5"/>
    <text x="90" y="65" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" fill="#dc2626">?</text>
    
    <path d="M 165,45 A 18,18 0 0,0 185,55" fill="none" stroke="#dc2626" stroke-width="1.5"/>
    <text x="160" y="65" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" fill="#dc2626">?</text>
    
    <text x="25" y="172" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">G</text>
    <text x="75" y="28" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">H</text>
    <text x="185" y="28" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">E</text>
    <text x="218" y="172" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">F</text>
    <text x="130" y="195" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="15">c)</text>
  </g>
</svg>"""

# 8. HÌNH 3.10: Bài tập 3.3 (Hình cái diều)
svg_hinh_3_10 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 245" width="360" height="245">
  <rect width="360" height="245" fill="#ffffff"/>
  <polygon points="180,30 90,110 180,225 270,110" fill="#f8fafc" stroke="#000000" stroke-width="2" stroke-linejoin="round"/>
  <line x1="180" y1="30" x2="180" y2="225" stroke="#0284c7" stroke-width="1.8"/>
  <line x1="90" y1="110" x2="270" y2="110" stroke="#0284c7" stroke-width="1.8"/>
  
  <polyline points="180,98 168,98 168,110" fill="none" stroke="#000000" stroke-width="1.5"/>
  <text x="188" y="125" font-family="'Times New Roman', serif" font-style="italic" font-size="13" fill="#0284c7">I</text>
  
  <line x1="130" y1="67" x2="138" y2="75" stroke="#dc2626" stroke-width="1.8"/>
  <line x1="222" y1="75" x2="230" y2="67" stroke="#dc2626" stroke-width="1.8"/>
  
  <line x1="130" y1="165" x2="138" y2="173" stroke="#16a34a" stroke-width="1.8"/>
  <line x1="134" y1="161" x2="142" y2="169" stroke="#16a34a" stroke-width="1.8"/>
  <line x1="222" y1="173" x2="230" y2="165" stroke="#16a34a" stroke-width="1.8"/>
  <line x1="218" y1="169" x2="226" y2="161" stroke="#16a34a" stroke-width="1.8"/>
  
  <text x="180" y="20" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">D</text>
  <text x="70" y="115" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">A</text>
  <text x="180" y="240" text-anchor="middle" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">B</text>
  <text x="282" y="115" font-family="'Times New Roman', serif" font-style="italic" font-size="16" font-weight="bold">C</text>
</svg>"""

all_svgs = [
    ("hinh_3_1", svg_hinh_3_1),
    ("hinh_3_2", svg_hinh_3_2),
    ("hinh_3_4", svg_hinh_3_4),
    ("hinh_3_5", svg_hinh_3_5),
    ("hinh_3_6", svg_hinh_3_6),
    ("hinh_3_7", svg_hinh_3_7),
    ("hinh_3_8", svg_hinh_3_8),
    ("hinh_3_10", svg_hinh_3_10),
]

for name, svg in all_svgs:
    svg_path = f"GIAO AN/hinh_ve_sgk/{name}.svg"
    png_path = f"GIAO AN/hinh_ve_sgk/{name}.png"
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    svg_to_png(svg, png_path)

print("DONE: Rendered all 8 SVG and PNG files without captions!")

