# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

OUT_DIR = Path("TROLYTHIEN/11_VE_HINH/Ket_qua")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. HÌNH THANG CÂN ABCD (Bài 16 - Toán 8)
# ------------------------------------------------------------------------------
svg_hinh_thang = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 460" width="760" height="460" style="background-color: #ffffff; font-family: 'Times New Roman', serif;">
  <!-- Nền trắng toàn phần -->
  <rect width="760" height="460" fill="#ffffff" />

  <!-- Vùng tô màu nhẹ cho tam giác vuông AHD và BKC -->
  <polygon points="120,350 240,350 240,150" fill="#2563eb" fill-opacity="0.05" stroke="none" />
  <polygon points="640,350 520,350 520,150" fill="#2563eb" fill-opacity="0.05" stroke="none" />

  <!-- 4 cạnh hình thang cân ABCD -->
  <!-- Đáy AB: (240, 150) -> (520, 150) -->
  <!-- Đáy CD: (120, 350) -> (640, 350) -->
  <!-- Cạnh bên AD: (240, 150) -> (120, 350) -->
  <!-- Cạnh bên BC: (520, 150) -> (640, 350) -->
  <polygon points="240,150 520,150 640,350 120,350" stroke="#000000" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none" />

  <!-- Hai đường cao AH và BK (nét liền sắc nét hoặc xanh sư phạm) -->
  <line x1="240" y1="150" x2="240" y2="350" stroke="#2563eb" stroke-width="2" stroke-linecap="round" fill="none" />
  <line x1="520" y1="150" x2="520" y2="350" stroke="#2563eb" stroke-width="2" stroke-linecap="round" fill="none" />

  <!-- Ký hiệu góc vuông tại H (240, 350) -->
  <!-- Vuông góc hướng về phía D: góc (215, 350) -> (215, 325) -> (240, 325) -->
  <path d="M 215,350 L 215,325 L 240,325" stroke="#000000" stroke-width="1.6" fill="none" />
  <!-- Vuông góc hướng về phía K: góc (265, 350) -> (265, 325) -> (240, 325) -->
  <path d="M 265,350 L 265,325 L 240,325" stroke="#000000" stroke-width="1.6" fill="none" />

  <!-- Ký hiệu góc vuông tại K (520, 350) -->
  <!-- Vuông góc hướng về phía H: góc (495, 350) -> (495, 325) -> (520, 325) -->
  <path d="M 495,350 L 495,325 L 520,325" stroke="#000000" stroke-width="1.6" fill="none" />
  <!-- Vuông góc hướng về phía C: góc (545, 350) -> (545, 325) -> (520, 325) -->
  <path d="M 545,350 L 545,325 L 520,325" stroke="#000000" stroke-width="1.6" fill="none" />

  <!-- Ký hiệu bằng nhau trên cạnh bên AD và BC (1 vạch nghiêng) -->
  <!-- Trung điểm AD = (180, 250); góc AD khoảng -59 độ; vạch vuông góc -->
  <line x1="172" y1="244" x2="188" y2="256" stroke="#000000" stroke-width="2" stroke-linecap="round" fill="none" />
  <!-- Trung điểm BC = (580, 250); vạch vuông góc -->
  <line x1="572" y1="256" x2="588" y2="244" stroke="#000000" stroke-width="2" stroke-linecap="round" fill="none" />

  <!-- Ký hiệu cung góc bằng nhau tại D và C -->
  <!-- Góc D tại (120, 350): tia DC sang phải, tia DA lên trên-phải (dx=120, dy=-200) -->
  <path d="M 160,350 A 40 40 0 0 0 140,317" stroke="#dc2626" stroke-width="1.8" fill="none" />
  <!-- Góc C tại (640, 350): tia CD sang trái, tia CB lên trên-trái (dx=-120, dy=-200) -->
  <path d="M 600,350 A 40 40 0 0 1 620,317" stroke="#dc2626" stroke-width="1.8" fill="none" />

  <!-- Các điểm tròn đỉnh -->
  <circle cx="240" cy="150" r="3.5" fill="#000000" />
  <circle cx="520" cy="150" r="3.5" fill="#000000" />
  <circle cx="120" cy="350" r="3.5" fill="#000000" />
  <circle cx="640" cy="350" r="3.5" fill="#000000" />
  <circle cx="240" cy="350" r="3.5" fill="#2563eb" />
  <circle cx="520" cy="350" r="3.5" fill="#2563eb" />

  <!-- Nhãn đỉnh chữ in nghiêng chuẩn GDPT 2018 (Times New Roman Bold Italic) -->
  <text x="235" y="125" font-family="'Times New Roman', serif" font-size="26" font-weight="bold" font-style="italic" fill="#000000" text-anchor="middle">A</text>
  <text x="525" y="125" font-family="'Times New Roman', serif" font-size="26" font-weight="bold" font-style="italic" fill="#000000" text-anchor="middle">B</text>
  <text x="90" y="365" font-family="'Times New Roman', serif" font-size="26" font-weight="bold" font-style="italic" fill="#000000" text-anchor="middle">D</text>
  <text x="670" y="365" font-family="'Times New Roman', serif" font-size="26" font-weight="bold" font-style="italic" fill="#000000" text-anchor="middle">C</text>
  <text x="240" y="385" font-family="'Times New Roman', serif" font-size="26" font-weight="bold" font-style="italic" fill="#2563eb" text-anchor="middle">H</text>
  <text x="520" y="385" font-family="'Times New Roman', serif" font-size="26" font-weight="bold" font-style="italic" fill="#2563eb" text-anchor="middle">K</text>
</svg>"""

svg_hinh_thang_path = OUT_DIR / "Bai_16_Hinh_Thang_Can_ABCD.svg"
svg_hinh_thang_path.write_text(svg_hinh_thang, encoding="utf-8")
doc_ht = pymupdf.open(str(svg_hinh_thang_path))
pix_ht = doc_ht[0].get_pixmap(dpi=300)
png_hinh_thang_path = OUT_DIR / "Bai_16_Hinh_Thang_Can_ABCD.png"
pix_ht.save(str(png_hinh_thang_path))
print("Đã tạo ảnh Bài 16 Toán 8:", png_hinh_thang_path)

# ------------------------------------------------------------------------------
# 2. TRỤC SỐ BIỂU DIỄN NGHIỆM x <= 2 (Bài 11c - Toán 9)
# ------------------------------------------------------------------------------
svg_truc_so = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 180" width="760" height="180" style="background-color: #ffffff; font-family: 'Times New Roman', serif;">
  <rect width="760" height="180" fill="#ffffff" />

  <!-- Trục số chính: đường thẳng có mũi tên ở bên phải -->
  <line x1="60" y1="90" x2="680" y2="90" stroke="#000000" stroke-width="2.5" />
  <!-- Mũi tên đầu trục số -->
  <polygon points="680,90 660,82 665,90 660,98" fill="#000000" />

  <!-- Vạch chia điểm 0 tại x = 250 -->
  <line x1="250" y1="80" x2="250" y2="100" stroke="#000000" stroke-width="2" />
  <text x="250" y="130" font-family="'Times New Roman', serif" font-size="24" font-weight="bold" fill="#000000" text-anchor="middle">0</text>

  <!-- Điểm 2 tại x = 430 -->
  <!-- Dấu ngoặc vuông ']' quay về bên trái biểu thị tập nghiệm x <= 2 -->
  <path d="M 418,65 L 430,65 L 430,115 L 418,115" stroke="#1d4ed8" stroke-width="3.5" fill="none" stroke-linecap="square" />
  <text x="430" y="145" font-family="'Times New Roman', serif" font-size="26" font-weight="bold" fill="#1d4ed8" text-anchor="middle">2</text>

  <!-- Phần bị gạch bỏ (x > 2): các đường chéo nghiêng từ x=435 đến x=660 -->
  <g stroke="#9ca3af" stroke-width="1.8" stroke-linecap="round">
    <line x1="445" y1="75" x2="465" y2="105" />
    <line x1="465" y1="75" x2="485" y2="105" />
    <line x1="485" y1="75" x2="505" y2="105" />
    <line x1="505" y1="75" x2="525" y2="105" />
    <line x1="525" y1="75" x2="545" y2="105" />
    <line x1="545" y1="75" x2="565" y2="105" />
    <line x1="565" y1="75" x2="585" y2="105" />
    <line x1="585" y1="75" x2="605" y2="105" />
    <line x1="605" y1="75" x2="625" y2="105" />
    <line x1="625" y1="75" x2="645" y2="105" />
    <line x1="645" y1="75" x2="660" y2="100" />
  </g>
</svg>"""

svg_truc_so_path = OUT_DIR / "Bai_11c_Truc_So_Toan_9.svg"
svg_truc_so_path.write_text(svg_truc_so, encoding="utf-8")
doc_ts = pymupdf.open(str(svg_truc_so_path))
pix_ts = doc_ts[0].get_pixmap(dpi=300)
png_truc_so_path = OUT_DIR / "Bai_11c_Truc_So_Toan_9.png"
pix_ts.save(str(png_truc_so_path))
print("Đã tạo ảnh Bài 11c Toán 9:", png_truc_so_path)
