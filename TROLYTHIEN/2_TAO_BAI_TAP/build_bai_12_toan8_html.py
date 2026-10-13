# -*- coding: utf-8 -*-
r"""
BUILDER SCRIPT: BÀI 12 - HÌNH BÌNH HÀNH (TOÁN 8)
ÁP DỤNG TRỌN VẸN 8 BẢN VÁ SƯ PHẠM THỰC CHIẾN (CHUẨN TÔN THÂN - VŨ HỮU BÌNH)
ĐẦU VÀO: TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/13.10/Toan8_Chuong_3_Bai_12_Hinh_binh_hanh_Trang_57-61.pdf
ĐẦU RA:  TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/Bai_12_Hinh_Binh_Hanh_Toan_8.html
"""

import os
import sys
import json

# Import engine
engine_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'engine')
sys.path.append(engine_dir)
from builder_bai_day_html import build_bai_day_html

# ==============================================================================
# 1. HÌNH VẼ SVG CHUẨN XÁC 1:1 THEO GIẢI TÍCH OXY (KHÔNG LỘ ĐÁP ÁN, PADDING >= 40PX)
# ==============================================================================

def make_svg_hbh_basic(a_deg=110, show_angle_a=True, show_q_b=True, show_side_ab=True, ab_val="10 cm"):
    """Hình bình hành cơ bản ABCD: A(120,60), B(380,60), C(310,200), D(50,200)"""
    angle_badge = f'<text x="140" y="90" font-size="14" font-weight="bold" fill="#dc2626">{a_deg}°</text>' if show_angle_a else ''
    q_b = '<text x="340" y="85" font-size="14" font-weight="bold" fill="#64748b">?°</text>' if show_q_b else ''
    side_ab = f'<text x="240" y="50" font-size="15" font-weight="bold" fill="#2563eb">{ab_val}</text>' if show_side_ab else ''
    
    return f"""<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <polygon points="120,60 380,60 310,200 50,200" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5"/>
  <path d="M 120,60 L 145,60 A 25,25 0 0,1 110,83 Z" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <circle cx="120" cy="60" r="3.5" fill="#1e293b"/>
  <circle cx="380" cy="60" r="3.5" fill="#1e293b"/>
  <circle cx="310" cy="200" r="3.5" fill="#1e293b"/>
  <circle cx="50" cy="200" r="3.5" fill="#1e293b"/>
  <text x="105" y="50" font-size="16" font-weight="bold" fill="#0f172a">A</text>
  <text x="390" y="55" font-size="16" font-weight="bold" fill="#0f172a">B</text>
  <text x="320" y="220" font-size="16" font-weight="bold" fill="#0f172a">C</text>
  <text x="35" y="215" font-size="16" font-weight="bold" fill="#0f172a">D</text>
  {angle_badge}
  {q_b}
  {side_ab}
  <text x="25" y="130" font-size="15" font-weight="bold" fill="#dc2626">? cm</text>
</svg>"""

def make_svg_hbh_diagonals():
    """Hình bình hành ABCD với 2 đường chéo cắt nhau tại O"""
    return """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <polygon points="120,60 380,60 300,200 40,200" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5"/>
  <line x1="120" y1="60" x2="300" y2="200" stroke="#64748b" stroke-width="1.8" stroke-dasharray="4,4"/>
  <line x1="40" y1="200" x2="380" y2="60" stroke="#64748b" stroke-width="1.8" stroke-dasharray="4,4"/>
  <circle cx="210" cy="130" r="4" fill="#dc2626"/>
  <circle cx="120" cy="60" r="3.5" fill="#1e293b"/>
  <circle cx="380" cy="60" r="3.5" fill="#1e293b"/>
  <circle cx="300" cy="200" r="3.5" fill="#1e293b"/>
  <circle cx="40" cy="200" r="3.5" fill="#1e293b"/>
  <text x="105" y="50" font-size="16" font-weight="bold" fill="#0f172a">A</text>
  <text x="390" y="55" font-size="16" font-weight="bold" fill="#0f172a">B</text>
  <text x="310" y="220" font-size="16" font-weight="bold" fill="#0f172a">C</text>
  <text x="25" y="215" font-size="16" font-weight="bold" fill="#0f172a">D</text>
  <text x="215" y="125" font-size="16" font-weight="bold" fill="#dc2626">O</text>
  <text x="245" y="50" font-size="14" font-weight="bold" fill="#2563eb">11 cm</text>
  <text x="145" y="105" font-size="13" font-weight="bold" fill="#475569">OA = ?</text>
  <text x="270" y="105" font-size="13" font-weight="bold" fill="#475569">OB = ?</text>
</svg>"""

def make_svg_hbh_midpoints():
    """Hình bình hành ABCD với M, N là trung điểm AB, CD (5 HBH lồng nhau) - Nấc vẽ theo câu a, b, c"""
    return """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- CÂU A: HÌNH BÌNH HÀNH ABCD VÀ TRUNG ĐIỂM M, N -->
  <g class="geo-stage geo-stage-a" data-stage="a">
    <polygon points="100,60 360,60 300,200 40,200" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
    <line x1="230" y1="60" x2="170" y2="200" stroke="#059669" stroke-width="2.2"/>
    <circle cx="230" cy="60" r="3.5" fill="#059669"/>
    <circle cx="170" cy="200" r="3.5" fill="#059669"/>
    <text x="85" y="55" font-size="16" font-weight="bold" fill="#0f172a">A</text>
    <text x="225" y="50" font-size="16" font-weight="bold" fill="#059669">M</text>
    <text x="370" y="55" font-size="16" font-weight="bold" fill="#0f172a">B</text>
    <text x="310" y="215" font-size="16" font-weight="bold" fill="#0f172a">C</text>
    <text x="165" y="225" font-size="16" font-weight="bold" fill="#059669">N</text>
    <text x="25" y="215" font-size="16" font-weight="bold" fill="#0f172a">D</text>
  </g>
  <!-- CÂU B: NỐI AN VÀ CM -->
  <g class="geo-stage geo-stage-b" data-stage="b" style="display: none;">
    <line x1="100" y1="60" x2="170" y2="200" stroke="#d97706" stroke-width="2"/>
    <line x1="230" y1="60" x2="300" y2="200" stroke="#d97706" stroke-width="2"/>
  </g>
  <!-- CÂU C: NỐI DM VÀ BN, GIAO ĐIỂM I VÀ K -->
  <g class="geo-stage geo-stage-c" data-stage="c" style="display: none;">
    <line x1="40" y1="200" x2="230" y2="60" stroke="#7c3aed" stroke-width="2"/>
    <line x1="170" y1="200" x2="360" y2="60" stroke="#7c3aed" stroke-width="2"/>
    <circle cx="135" cy="130" r="4" fill="#dc2626"/>
    <circle cx="265" cy="130" r="4" fill="#dc2626"/>
    <text x="120" y="130" font-size="15" font-weight="bold" fill="#dc2626">I</text>
    <text x="275" y="130" font-size="15" font-weight="bold" fill="#dc2626">K</text>
  </g>
</svg>"""

def make_svg_hbh_perpendiculars():
    """Hình bình hành ABCD với AH và CK vuông góc BD - Nấc vẽ theo câu a, b, c"""
    return """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- CÂU A: HÌNH BÌNH HÀNH ABCD, BD VÀ 2 ĐƯỜNG VUÔNG GÓC AH, CK -->
  <g class="geo-stage geo-stage-a" data-stage="a">
    <polygon points="110,60 370,60 310,200 50,200" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2"/>
    <line x1="50" y1="200" x2="370" y2="60" stroke="#475569" stroke-width="1.8"/>
    <line x1="110" y1="60" x2="160" y2="152" stroke="#dc2626" stroke-width="2.2"/>
    <line x1="310" y1="200" x2="260" y2="108" stroke="#dc2626" stroke-width="2.2"/>
    <polyline points="152,148 156,140 164,144" fill="none" stroke="#dc2626" stroke-width="1.5"/>
    <polyline points="268,112 264,120 256,116" fill="none" stroke="#dc2626" stroke-width="1.5"/>
    <text x="95" y="55" font-size="16" font-weight="bold" fill="#0f172a">A</text>
    <text x="380" y="55" font-size="16" font-weight="bold" fill="#0f172a">B</text>
    <text x="320" y="215" font-size="16" font-weight="bold" fill="#0f172a">C</text>
    <text x="35" y="215" font-size="16" font-weight="bold" fill="#0f172a">D</text>
    <text x="145" y="172" font-size="15" font-weight="bold" fill="#dc2626">H</text>
    <text x="260" y="98" font-size="15" font-weight="bold" fill="#dc2626">K</text>
  </g>
  <!-- CÂU B: NỐI TỨ GIÁC AHCK -->
  <g class="geo-stage geo-stage-b" data-stage="b" style="display: none;">
    <line x1="110" y1="60" x2="260" y2="108" stroke="#ea580c" stroke-width="2" stroke-dasharray="4,4"/>
    <line x1="160" y1="152" x2="310" y2="200" stroke="#ea580c" stroke-width="2" stroke-dasharray="4,4"/>
  </g>
  <!-- CÂU C: TRUNG ĐIỂM O CỦA HK VÀ ĐƯỜNG THẲNG AC -->
  <g class="geo-stage geo-stage-c" data-stage="c" style="display: none;">
    <line x1="110" y1="60" x2="310" y2="200" stroke="#7c3aed" stroke-width="1.8" stroke-dasharray="3,3"/>
    <circle cx="210" cy="130" r="4" fill="#0f172a"/>
    <text x="215" y="145" font-size="15" font-weight="bold" fill="#0f172a">O</text>
  </g>
</svg>"""

def make_svg_hbh_bisectors():
    """Hình bình hành ABCD với tia phân giác góc D và góc B"""
    return """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <polygon points="120,60 380,60 300,200 40,200" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2"/>
  <line x1="40" y1="200" x2="280" y2="60" stroke="#059669" stroke-width="2.2"/>
  <line x1="380" y1="60" x2="140" y2="200" stroke="#059669" stroke-width="2.2"/>
  <circle cx="280" cy="60" r="3.5" fill="#059669"/>
  <circle cx="140" cy="200" r="3.5" fill="#059669"/>
  <text x="105" y="55" font-size="16" font-weight="bold" fill="#0f172a">A</text>
  <text x="390" y="55" font-size="16" font-weight="bold" fill="#0f172a">B</text>
  <text x="310" y="215" font-size="16" font-weight="bold" fill="#0f172a">C</text>
  <text x="25" y="215" font-size="16" font-weight="bold" fill="#0f172a">D</text>
  <text x="280" y="50" font-size="16" font-weight="bold" fill="#059669">E</text>
  <text x="135" y="225" font-size="16" font-weight="bold" fill="#059669">F</text>
  <path d="M 40,200 L 70,200 A 30,30 0 0,0 60,175 Z" fill="#fef3c7" stroke="#d97706" stroke-width="1"/>
  <path d="M 380,60 L 350,60 A 30,30 0 0,0 360,85 Z" fill="#fef3c7" stroke="#d97706" stroke-width="1"/>
</svg>"""

def make_svg_realworld_opening():
    """Bài toán thực tế mở đầu SGK Trang 57 & 61: Hai con đường a, b và điểm O"""
    return """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <line x1="40" y1="210" x2="440" y2="210" stroke="#1e293b" stroke-width="4"/>
  <line x1="40" y1="210" x2="300" y2="30" stroke="#1e293b" stroke-width="4"/>
  <polygon points="40,210 200,80 340,80 180,210" fill="#dcfce7" stroke="#059669" stroke-width="2" stroke-dasharray="4,4"/>
  <line x1="40" y1="210" x2="340" y2="80" stroke="#dc2626" stroke-width="2.5"/>
  <line x1="200" y1="80" x2="180" y2="210" stroke="#2563eb" stroke-width="2.5"/>
  <circle cx="190" cy="145" r="5" fill="#dc2626"/>
  <circle cx="200" cy="80" r="4" fill="#2563eb"/>
  <circle cx="180" cy="210" r="4" fill="#2563eb"/>
  <circle cx="340" cy="80" r="4" fill="#059669"/>
  <circle cx="40" cy="210" r="4" fill="#1e293b"/>
  <text x="25" y="225" font-size="16" font-weight="bold" fill="#1e293b">S</text>
  <text x="195" y="65" font-size="16" font-weight="bold" fill="#2563eb">A</text>
  <text x="175" y="235" font-size="16" font-weight="bold" fill="#2563eb">B</text>
  <text x="200" y="150" font-size="16" font-weight="bold" fill="#dc2626">O (Dân cư)</text>
  <text x="350" y="85" font-size="16" font-weight="bold" fill="#059669">K</text>
  <text x="430" y="200" font-size="15" font-weight="bold" fill="#1e293b">đường b</text>
  <text x="280" y="25" font-size="15" font-weight="bold" fill="#1e293b">đường a</text>
</svg>"""

def make_svg_extension_median():
    """Bài 19: Phát minh định lý đường trung bình qua HBH (E trung điểm AC, DF qua E)"""
    return """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <polygon points="140,50 60,200 320,200" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5"/>
  <line x1="100" y1="125" x2="230" y2="125" stroke="#dc2626" stroke-width="2.5"/>
  <line x1="230" y1="125" x2="360" y2="125" stroke="#059669" stroke-width="2" stroke-dasharray="4,4"/>
  <line x1="320" y1="200" x2="400" y2="50" stroke="#059669" stroke-width="2" stroke-dasharray="4,4"/>
  <line x1="140" y1="50" x2="400" y2="50" stroke="#059669" stroke-width="2" stroke-dasharray="4,4"/>
  <circle cx="100" cy="125" r="3.5" fill="#dc2626"/>
  <circle cx="230" cy="125" r="3.5" fill="#dc2626"/>
  <circle cx="360" cy="125" r="3.5" fill="#059669"/>
  <text x="135" y="40" font-size="16" font-weight="bold" fill="#0f172a">A</text>
  <text x="45" y="215" font-size="16" font-weight="bold" fill="#0f172a">B</text>
  <text x="325" y="215" font-size="16" font-weight="bold" fill="#0f172a">C</text>
  <text x="80" y="125" font-size="15" font-weight="bold" fill="#dc2626">D</text>
  <text x="225" y="115" font-size="15" font-weight="bold" fill="#dc2626">E</text>
  <text x="370" y="125" font-size="15" font-weight="bold" fill="#059669">F</text>
</svg>"""

# ==============================================================================
# 2. XÂY DỰNG TOÀN BỘ 20 SLIDE DỮ LIỆU CHUẨN THỰC CHIẾN
# ==============================================================================

slides = []

# --- SLIDE 1: LÝ THUYẾT TRỌNG TÂM ---
slide_1_html = """
<div style="padding: 10px 20px;">
  <h2 style="color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-bottom: 15px;">
    📐 I. ĐỊNH NGHĨA & BẢN CHẤT HÌNH BÌNH HÀNH
  </h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
    <div style="background: #eff6ff; padding: 15px; border-radius: 8px; border-left: 4px solid #2563eb;">
      <h3 style="color: #1d4ed8; margin-bottom: 8px;">1. Định nghĩa chuẩn SGK</h3>
      <p style="font-size: 15px; line-height: 1.6;">
        <strong>Hình bình hành</strong> là tứ giác có <em>các cạnh đối song song</em>.
      </p>
      <p style="font-size: 14px; color: #475569; margin-top: 6px;">
        Tứ giác $ABCD$ là hình bình hành khi: $AB \parallel CD$ và $AD \parallel BC$.
      </p>
    </div>
    <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; border-left: 4px solid #16a34a;">
      <h3 style="color: #15803d; margin-bottom: 8px;">2. Tính chất cốt lõi (Định lí 1)</h3>
      <ul style="font-size: 14.5px; line-height: 1.6; margin-left: 18px;">
        <li>Các cạnh đối bằng nhau: $AB = CD$ và $AD = BC$.</li>
        <li>Các góc đối bằng nhau: $\widehat{A} = \widehat{C}$ và $\widehat{B} = \widehat{D}$.</li>
        <li>Hai đường chéo cắt nhau tại trung điểm của mỗi đường: $OA = OC$ và $OB = OD$.</li>
        <li><strong>Nhận xét:</strong> Hai góc kề một cạnh bất kì luôn bù nhau ($\widehat{A} + \widehat{B} = 180^\circ$).</li>
      </ul>
    </div>
  </div>

  <h2 style="color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-bottom: 15px;">
    🎯 II. 5 DẤU HIỆU NHẬN BIẾT HÌNH BÌNH HÀNH
  </h2>
  <table style="width: 100%; border-collapse: collapse; font-size: 14.5px;" border="1">
    <thead>
      <tr style="background: #f1f5f9; color: #0f172a;">
        <th style="padding: 8px; width: 15%;">Nhóm Dấu hiệu</th>
        <th style="padding: 8px; width: 55%;">Nội dung Dấu hiệu</th>
        <th style="padding: 8px; width: 30%;">Phạm vi ứng dụng & Lưu ý</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px; font-weight: bold; color: #2563eb;">1. Theo Cạnh</td>
        <td style="padding: 8px;">• Dấu hiệu 1: Tứ giác có các cạnh đối song song là HBH (theo định nghĩa).<br>• Dấu hiệu 2: Tứ giác có các cạnh đối bằng nhau là HBH.<br>• <strong>Dấu hiệu 3:</strong> Tứ giác có <em>một cặp cạnh đối song song VÀ bằng nhau</em> là HBH.</td>
        <td style="padding: 8px; color: #15803d;">Áp dụng thuận tiện khi bài toán đã cho sẵn 1 yếu tố song song hoặc trung điểm.</td>
      </tr>
      <tr>
        <td style="padding: 8px; font-weight: bold; color: #d97706;">2. Theo Góc</td>
        <td style="padding: 8px;">• Dấu hiệu 4: Tứ giác có <em>các góc đối bằng nhau</em> là HBH ($\widehat{A} = \widehat{C}$ và $\widehat{B} = \widehat{D}$).</td>
        <td style="padding: 8px; color: #b45309;">Bắt buộc phải đủ CẢ HAI CẶP GÓC ĐỐI. Kiểm tra 1 cặp là chưa đủ kết luận.</td>
      </tr>
      <tr>
        <td style="padding: 8px; font-weight: bold; color: #7c3aed;">3. Theo Đường chéo</td>
        <td style="padding: 8px;">• Dấu hiệu 5: Tứ giác có <em>hai đường chéo cắt nhau tại trung điểm của mỗi đường</em> là HBH.</td>
        <td style="padding: 8px; color: #6d28d9;">Phương pháp trọng tâm chứng minh 3 điểm thẳng hàng, đối xứng tâm và đồng quy.</td>
      </tr>
    </tbody>
  </table>
</div>
"""

slides.append({
    "slide_num": 1,
    "jump_label": "Slide 1: Tóm Tắt Lý Thuyết & 5 Dấu Hiệu Nhận Biết",
    "badge": "LÝ THUYẾT TRỌNG TÂM",
    "type": "theory",
    "html": slide_1_html
})

# --- HÀM TẠO CẤU TRÚC PHÂN TÍCH ĐI LÊN (HEURISTIC DIAGRAM) ---
def make_heuristic_diagram(target, intermediate, premise, why_text):
    return f"""
<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; margin-bottom: 10px;">
  <div style="font-weight: bold; color: #1e3a8a; margin-bottom: 6px; font-size: 14px;">
    🧭 SƠ ĐỒ PHÂN TÍCH TÌM HƯỚNG GIẢI:
  </div>
  <div style="display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 13.5px; background: #ffffff; padding: 8px; border-radius: 4px; border: 1px dashed #94a3b8;">
    <span style="color: #b91c1c; font-weight: bold;">[Cần tìm/chứng minh]: {target}</span>
    <span style="font-weight: bold; color: #475569; font-size: 16px;">⟸</span>
    <span style="color: #d97706; font-weight: bold;">[Yếu tố trung gian]: {intermediate}</span>
    <span style="font-weight: bold; color: #475569; font-size: 16px;">⟸</span>
    <span style="color: #15803d; font-weight: bold;">[Giả thiết/Định lý]: {premise}</span>
  </div>
  <div style="margin-top: 8px; font-size: 13.5px; color: #334155; line-height: 1.5;">
    💡 <strong>Mấu chốt suy luận:</strong> {why_text}
  </div>
</div>
"""

# ==============================================================================
# CÁC DẠNG BÀI TẬP PHÂN TẦNG (80% TB-KHÁ, 20% KHÁ-GIỎI)
# ==============================================================================

# --- DẠNG 1: TÍNH GÓC, ĐỘ DÀI CẠNH VÀ ĐƯỜNG CHÉO ---

# Bài 1: Ví dụ mẫu (Mức 1)
ana_1 = make_heuristic_diagram(
    target="Góc B, C, D và cạnh BC, CD, AD",
    intermediate="Tính chất hai góc kề bù nhau; các cạnh đối bằng nhau",
    premise="Tứ giác ABCD là HBH, góc A = 110°, chu vi = 32 cm, AB = 10 cm",
    why_text="Hình bình hành có các cạnh đối song song nên hai góc kề một cạnh là hai góc trong cùng phía, tổng bằng 180°. Nửa chu vi bằng tổng hai cạnh kề."
)
sol_1 = """
<p><strong>a) Tính các góc của hình bình hành:</strong></p>
<p>Vì tứ giác $ABCD$ là hình bình hành nên $AD \parallel BC$.</p>
<p>Do đó hai góc $\widehat{A}$ và $\widehat{B}$ là hai góc trong cùng phía bù nhau, ta có:</p>
<p>$$\widehat{A} + \widehat{B} = 180^\circ \quad \text{suy ra} \quad \widehat{B} = 180^\circ - 110^\circ = 70^\circ.$$</p>
<p>Áp dụng định lí về các góc đối của hình bình hành:</p>
<p>$$\widehat{C} = \widehat{A} = 110^\circ \quad \text{và} \quad \widehat{D} = \widehat{B} = 70^\circ.$$</p>
<p><strong>b) Tính các cạnh còn lại của hình bình hành:</strong></p>
<p>Áp dụng định lí về các cạnh đối của hình bình hành:</p>
<p>$$CD = AB = 10\text{ cm} \quad \text{và} \quad AD = BC.$$</p>
<p>Nửa chu vi của hình bình hành là: $AB + BC = 32 : 2 = 16\text{ cm}$.</p>
<p>Suy ra: $BC = 16 - 10 = 6\text{ cm}$. Do đó $AD = 6\text{ cm}$.</p>
<p><strong>Kết luận:</strong> Các cạnh còn lại là $CD = 10\text{ cm}$, $BC = 6\text{ cm}$, $AD = 6\text{ cm}$.</p>
"""
slides.append({
    "slide_num": 2, "pid": 1, "is_example": True,
    "jump_label": "Slide 2: Bài 1 (Ví dụ mẫu: Tính góc & cạnh HBH)",
    "badge": "Dạng 1: Tính góc & cạnh HBH",
    "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_basic(110, True, True, True, "10 cm"),
    "debai": "Cho hình bình hành $ABCD$ có góc $\widehat{A} = 110^\circ$.<br>a) Tính số đo các góc $\widehat{B}, \widehat{C}, \widehat{D}$.<br>b) Biết chu vi hình bình hành $ABCD$ bằng $32\\text{ cm}$ và độ dài cạnh $AB = 10\\text{ cm}$. Hãy tính độ dài các cạnh còn lại.",
    "analysis": ana_1, "solution": sol_1,
    "pitfall": "Học sinh thường quên tính chất hai góc kề bù nhau mà nhầm tưởng tất cả các góc đều bằng nhau, hoặc quên chia đôi chu vi trước khi trừ cạnh đã biết.",
    "extension": "Mọi bài toán tính góc hình bình hành khi đã biết 1 góc thì luôn xác định được ngay 3 góc còn lại (góc đối bằng nó, hai góc kề bù với nó)."
})

# Bài 2: Bài tương tự 1 (Luyện tay - Mức 1)
ana_2 = make_heuristic_diagram(
    target="Số đo góc B, C, D và các cạnh BC, CD, AD",
    intermediate="Áp dụng định lí hai góc kề bù nhau và các cạnh đối bằng nhau",
    premise="ABCD là HBH, góc A = 70°, chu vi = 36 cm, AB = 11 cm",
    why_text="Hai góc kề bù nhau nên góc B = 180° - 70° = 110°. Nửa chu vi bằng AB + BC nên BC = 18 - 11 = 7 cm."
)
sol_2 = """
<p><strong>a) Tính các góc của hình bình hành:</strong></p>
<p>Vì $ABCD$ là hình bình hành nên hai góc kề cạnh $AB$ bù nhau: $\widehat{A} + \widehat{B} = 180^\circ$.</p>
<p>Suy ra $\widehat{B} = 180^\circ - 70^\circ = 110^\circ$.</p>
<p>Theo tính chất góc đối hình bình hành: $\widehat{C} = \widehat{A} = 70^\circ$ và $\widehat{D} = \widehat{B} = 110^\circ$.</p>
<p><strong>b) Tính các cạnh còn lại:</strong></p>
<p>Nửa chu vi hình bình hành là: $AB + BC = 36 : 2 = 18\text{ cm}$.</p>
<p>Suy ra cạnh $BC = 18 - 11 = 7\text{ cm}$.</p>
<p>Vì các cạnh đối bằng nhau nên $CD = AB = 11\text{ cm}$ và $AD = BC = 7\text{ cm}$.</p>
"""
slides.append({
    "slide_num": 3, "pid": 2,
    "jump_label": "Slide 3: Bài 2 (Bài tương tự 1: Luyện tính góc & cạnh)",
    "badge": "Dạng 1: Tính góc & cạnh HBH",
    "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_basic(70, True, True, True, "11 cm"),
    "debai": "Cho hình bình hành $ABCD$ có góc $\widehat{A} = 70^\circ$.<br>a) Tính số đo ba góc còn lại của hình bình hành.<br>b) Biết chu vi hình bình hành bằng $36\\text{ cm}$ và cạnh $AB = 11\\text{ cm}$. Tính độ dài các cạnh $BC, CD, DA$.",
    "analysis": ana_2, "solution": sol_2,
    "pitfall": "Học sinh thường bấm máy nhầm 180 - 70 = 100 thay vì 110, hoặc nhầm cạnh đối diện thành cạnh kề.",
    "extension": "Biết chu vi và một cạnh của hình bình hành, độ dài cạnh kề bằng nửa chu vi trừ đi cạnh đã biết: $BC = \\frac{P}{2} - AB$."
})

# Bài 3: Bài biến thể 2 (Đổi chiều tư duy - Mức 1)
ana_3 = make_heuristic_diagram(
    target="Số đo 4 góc và độ dài 4 cạnh của HBH",
    intermediate="Giải bài toán tìm hai số khi biết Tổng & Hiệu; Tổng & Tỉ số",
    premise="A - B = 40°, A + B = 180°; Chu vi = 48 cm, AB = 3*AD",
    why_text="Tổng hai góc kề bằng 180° và hiệu bằng 40° đưa về tìm hai số biết tổng và hiệu. Cạnh AB = 3AD kết hợp nửa chu vi bằng 24 cm đưa về tìm hai số biết tổng và tỉ số."
)
sol_3 = """
<p><strong>a) Tính các góc của hình bình hành:</strong></p>
<p>Vì $ABCD$ là hình bình hành nên hai góc kề bù nhau: $\widehat{A} + \widehat{B} = 180^\circ$.</p>
<p>Kết hợp với đề bài $\widehat{A} - \widehat{B} = 40^\circ$, ta có bài toán tìm hai số khi biết tổng và hiệu:</p>
<p>$$\widehat{A} = (180^\circ + 40^\circ) : 2 = 110^\circ.$$</p>
<p>Suy ra $\widehat{B} = 180^\circ - 110^\circ = 70^\circ$.</p>
<p>Theo tính chất góc đối: $\widehat{C} = \widehat{A} = 110^\circ$ và $\widehat{D} = \widehat{B} = 70^\circ$.</p>
<p><strong>b) Tính các cạnh của hình bình hành:</strong></p>
<p>Nửa chu vi là: $AB + AD = 48 : 2 = 24\text{ cm}$.</p>
<p>Vì $AB = 3 \cdot AD$, ta có $3 \cdot AD + AD = 24$, hay $4 \cdot AD = 24$.</p>
<p>Suy ra $AD = 24 : 4 = 6\text{ cm}$ và $AB = 3 \cdot 6 = 18\text{ cm}$.</p>
<p>Do đó các cạnh là: $AB = CD = 18\text{ cm}$ và $BC = AD = 6\text{ cm}$.</p>
"""
slides.append({
    "slide_num": 4, "pid": 3,
    "jump_label": "Slide 4: Bài 3 (Biến thể đại số: Tổng - Hiệu & Tỉ số)",
    "badge": "Dạng 1: Tính góc & cạnh HBH",
    "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_basic(110, True, True, True, "3x"),
    "debai": "Cho hình bình hành $ABCD$.<br>a) Biết hiệu số đo hai góc kề một cạnh là $\\widehat{A} - \\widehat{B} = 40^\\circ$. Hãy tính số đo bốn góc của hình bình hành.<br>b) Biết cạnh $AB$ dài gấp 3 lần cạnh $AD$ và chu vi hình bình hành bằng $48\\text{ cm}$. Tính độ dài mỗi cạnh của hình bình hành.",
    "analysis": ana_3, "solution": sol_3,
    "pitfall": "Học sinh thường quên chia đôi chu vi mà lấy luôn 48 : 4 = 12 dẫn đến tính sai hoàn toàn các cạnh.",
    "extension": "Nếu đề bài cho tỉ số hai góc $\\widehat{A} : \\widehat{B} = 2 : 3$, ta dùng tính chất dãy tỉ số bằng nhau với tổng $\\widehat{A} + \\widehat{B} = 180^\\circ$."
})

# Bài 4: Phát triển đường chéo (Mức 2)
ana_4 = make_heuristic_diagram(
    target="Độ dài hai cạnh kề AB và BC",
    intermediate="Nhận xét: Chu vi tam giác OAB trừ chu vi tam giác OBC bằng AB - BC",
    premise="Hai đường chéo cắt nhau tại trung điểm O (OA = OC, OB chung); Chu vi = 40 cm",
    why_text="Đại lượng trung gian OA, OC triệt tiêu hoàn toàn vì OA = OC. Từ đó hiệu chu vi hai tam giác kề chính là hiệu hai cạnh kề của hình bình hành."
)
sol_4 = """
<p>Vì $ABCD$ là hình bình hành nên hai đường chéo cắt nhau tại trung điểm $O$ của mỗi đường, do đó $OA = OC$.</p>
<p>Chu vi tam giác $OAB$ là: $P_1 = OA + OB + AB$.</p>
<p>Chu vi tam giác $OBC$ là: $P_2 = OB + OC + BC$.</p>
<p>Xét hiệu hai chu vi, ta có:</p>
<p>$$P_1 - P_2 = (OA + OB + AB) - (OB + OC + BC) = (OA - OC) + (OB - OB) + (AB - BC).$$</p>
<p>Vì $OA = OC$ và $OB = OB$ nên hiệu trên triệt tiêu còn lại:</p>
<p>$$P_1 - P_2 = AB - BC = 4\text{ cm}.$$</p>
<p>Mặt khác, nửa chu vi hình bình hành là: $AB + BC = 40 : 2 = 20\text{ cm}$.</p>
<p>Ta tìm được độ dài hai cạnh kề:</p>
<p>$$AB = (20 + 4) : 2 = 12\text{ cm} \quad \text{và} \quad BC = 20 - 12 = 8\text{ cm}.$$</p>
<p><strong>Kết luận:</strong> Hai cạnh kề có độ dài là $AB = 12\text{ cm}$ và $BC = 8\text{ cm}$.</p>
"""
slides.append({
    "slide_num": 5, "pid": 4,
    "jump_label": "Slide 5: Bài 4 (Đường chéo & Triệt tiêu hiệu chu vi)",
    "badge": "Dạng 1: Đường chéo HBH",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_diagonals(),
    "debai": "Cho hình bình hành $ABCD$ có chu vi bằng $40\\text{ cm}$. Gọi $O$ là giao điểm của hai đường chéo $AC$ và $BD$. Biết chu vi của tam giác $OAB$ lớn hơn chu vi của tam giác $OBC$ là $4\\text{ cm}$. Tính độ dài hai cạnh kề $AB$ và $BC$ của hình bình hành.",
    "analysis": ana_4, "solution": sol_4,
    "pitfall": "Học sinh thường lúng túng vì không biết độ dài hai đường chéo mà không nhận ra OA và OC tự triệt tiêu khi lấy hiệu.",
    "extension": "Hiệu chu vi của hai tam giác kề nhau tạo bởi hai đường chéo luôn luôn bằng đúng hiệu độ dài hai cạnh kề của hình bình hành."
})

# --- DẠNG 2: CHỨNG MINH TỨ GIÁC LÀ HÌNH BÌNH HÀNH ---

# Bài 5: Ví dụ mẫu dấu hiệu góc (Mức 1)
ana_5 = make_heuristic_diagram(
    target="Chứng minh tứ giác ABCD là hình bình hành",
    intermediate="Tính góc D = 80°; kiểm tra Dấu hiệu 4 (góc đối) hoặc Dấu hiệu 1 (song song)",
    premise="Tứ giác ABCD có góc A = 100°, B = 80°, C = 100°",
    why_text="Tổng bốn góc trong tứ giác bằng 360° giúp tính được góc D = 80°. Sau đó dùng Dấu hiệu 4 (các góc đối bằng nhau) hoặc Dấu hiệu 1 (hai cạnh đối song song)."
)
sol_5 = """
<p><strong>a) Tính số đo góc D:</strong></p>
<p>Theo định lí tổng các góc trong một tứ giác, ta có:</p>
<p>$$\widehat{A} + \widehat{B} + \widehat{C} + \widehat{D} = 360^\circ$$</p>
<p>hay $100^\circ + 80^\circ + 100^\circ + \widehat{D} = 360^\circ$. Suy ra $\widehat{D} = 360^\circ - 280^\circ = 80^\circ$.</p>
<p><strong>b) Chứng minh ABCD là hình bình hành:</strong></p>
<p><em>Cách 1 (Sử dụng Dấu hiệu 4 - Các góc đối bằng nhau):</em></p>
<p>Tứ giác $ABCD$ có $\widehat{A} = \widehat{C} = 100^\circ$ và $\widehat{B} = \widehat{D} = 80^\circ$.</p>
<p>Tứ giác có các góc đối bằng nhau nên $ABCD$ là hình bình hành.</p>
<p><em>Cách 2 (Sử dụng Dấu hiệu 1 - Các cạnh đối song song):</em></p>
<p>Ta có $\widehat{A} + \widehat{B} = 100^\circ + 80^\circ = 180^\circ$. Mà hai góc này ở vị trí trong cùng phía nên $AD \parallel BC$.</p>
<p>Lại có $\widehat{B} + \widehat{C} = 80^\circ + 100^\circ = 180^\circ$ nên $AB \parallel CD$.</p>
<p>Tứ giác $ABCD$ có các cạnh đối song song nên là hình bình hành.</p>
"""
slides.append({
    "slide_num": 6, "pid": 5, "is_example": True,
    "jump_label": "Slide 6: Bài 5 (Ví dụ mẫu: Nhận biết qua góc)",
    "badge": "Dạng 2: Chứng minh HBH",
    "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_basic(100, True, True, False),
    "debai": "Cho tứ giác $ABCD$ có ba góc được đo như sau: $\\widehat{A} = 100^\\circ, \\widehat{B} = 80^\\circ, \\widehat{C} = 100^\\circ$.<br>a) Tính số đo của góc $\\widehat{D}$.<br>b) Tứ giác $ABCD$ có phải là hình bình hành không? Hãy giải thích bằng hai cách khác nhau (sử dụng Dấu hiệu 4 và Dấu hiệu 1).",
    "analysis": ana_5, "solution": sol_5,
    "pitfall": "Học sinh thường chỉ kiểm tra 1 cặp góc đối bằng nhau đã vội kết luận là HBH (chú ý: hình cánh diều cũng có thể có 1 cặp góc đối bằng nhau!).",
    "extension": "Tứ giác có hai cặp góc đối bằng nhau là hình bình hành; còn tứ giác có 3 góc vuông là hình chữ nhật."
})

# Bài 6: Bài tương tự 1 - Dấu hiệu cạnh đối bằng nhau (Mức 1)
ana_6 = make_heuristic_diagram(
    target="Chứng minh Định lí 2a: Tứ giác có các cạnh đối bằng nhau là HBH",
    intermediate="Kẻ đường chéo AC, chứng minh tam giác ABC = CDA (c-c-c) => các góc so le trong bằng nhau",
    premise="Tứ giác ABCD có AB = CD và AD = BC",
    why_text="Đường chéo AC chia tứ giác thành hai tam giác bằng nhau theo trường hợp cạnh - cạnh - cạnh, đưa về chứng minh các cạnh song song."
)
sol_6 = """
<p><strong>a) Chứng minh hai tam giác bằng nhau:</strong></p>
<p>Kẻ đường chéo $AC$. Xét $\triangle ABC$ và $\triangle CDA$, ta có:</p>
<p>• $AB = CD$ (theo giả thiết);</p>
<p>• $BC = DA$ (theo giả thiết);</p>
<p>• Cạnh $AC$ là cạnh chung.</p>
<p>Do đó $\triangle ABC = \triangle CDA$ (cạnh - cạnh - cạnh).</p>
<p><strong>b) Chứng minh ABCD là hình bình hành:</strong></p>
<p>Vì $\triangle ABC = \triangle CDA$ nên các góc tương ứng bằng nhau:</p>
<p>$$\widehat{BAC} = \widehat{DCA} \quad \text{và} \quad \widehat{BCA} = \widehat{DAC}.$$</p>
<p>Vì hai góc $\widehat{BAC}$ và $\widehat{DCA}$ ở vị trí so le trong nên $AB \parallel CD$.</p>
<p>Vì hai góc $\widehat{BCA}$ và $\widehat{DAC}$ ở vị trí so le trong nên $AD \parallel BC$.</p>
<p>Tứ giác $ABCD$ có các cạnh đối song song nên là hình bình hành.</p>
"""
slides.append({
    "slide_num": 7, "pid": 6,
    "jump_label": "Slide 7: Bài 6 (Chứng minh Định lí 2a SGK)",
    "badge": "Dạng 2: Chứng minh HBH",
    "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_diagonals(),
    "debai": "Cho tứ giác $ABCD$ có các cạnh đối bằng nhau từng đôi một: $AB = CD$ và $AD = BC$.<br>a) Kẻ đường chéo $AC$. Chứng minh $\\triangle ABC = \\triangle CDA$.<br>b) Từ đó suy ra các góc so le trong bằng nhau và chứng minh tứ giác $ABCD$ là hình bình hành.",
    "analysis": ana_6, "solution": sol_6,
    "pitfall": "Học sinh thường quên giải thích vị trí 'so le trong' trước khi kết luận hai đường thẳng song song.",
    "extension": "Đây chính là phương pháp mẫu mực chứng minh tính đúng đắn của Dấu hiệu nhận biết 2 trong SGK Toán 8."
})

# Bài 7: Dấu hiệu 3 - Một cặp cạnh đối song song và bằng nhau (Mức 1)
ana_7 = make_heuristic_diagram(
    target="Chứng minh AECF và DEBF là các hình bình hành",
    intermediate="Chỉ ra: AE // CF và AE = CF; EB // DF và EB = DF",
    premise="ABCD là HBH (AB // CD, AB = CD); E trên AB, F trên CD có AE = CF",
    why_text="Chỉ cần chỉ ra một cặp cạnh đối vừa song song vừa bằng nhau (AE // CF và AE = CF) là đủ chứng minh AECF là hình bình hành."
)
sol_7 = """
<p><strong>a) Chứng minh tứ giác AECF là hình bình hành:</strong></p>
<p>Vì $ABCD$ là hình bình hành nên $AB \parallel CD$.</p>
<p>Do $E \in AB$ và $F \in CD$ nên ta có $AE \parallel CF$.</p>
<p>Mặt khác theo giả thiết ta có $AE = CF$.</p>
<p>Tứ giác $AECF$ có một cặp cạnh đối vừa song song vừa bằng nhau nên là hình bình hành.</p>
<p><strong>b) Chứng minh tứ giác DEBF là hình bình hành:</strong></p>
<p>Ta có: $EB = AB - AE$ và $DF = CD - CF$.</p>
<p>Vì $AB = CD$ và $AE = CF$ nên suy ra $EB = DF$.</p>
<p>Lại có $EB \parallel DF$ (vì $AB \parallel CD$).</p>
<p>Do đó tứ giác $DEBF$ là hình bình hành.</p>
<p><strong>c) Kết luận về AF và CE:</strong></p>
<p>Vì $AECF$ là hình bình hành nên hai cạnh đối $AF$ và $CE$ song song và bằng nhau: $AF \parallel CE$ và $AF = CE$.</p>
"""
slides.append({
    "slide_num": 8, "pid": 7,
    "jump_label": "Slide 8: Bài 7 (Dấu hiệu 3: Cặp cạnh // và bằng nhau)",
    "badge": "Dạng 2: Chứng minh HBH",
    "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_midpoints(),
    "debai": "Cho hình bình hành $ABCD$. Lấy điểm $E$ trên cạnh $AB$ và điểm $F$ trên cạnh $CD$ sao cho $AE = CF$.<br>a) Chứng minh tứ giác $AECF$ là hình bình hành.<br>b) Chứng minh tứ giác $DEBF$ là hình bình hành.<br>c) Chứng minh hai đoạn thẳng $AF$ và $CE$ song song và bằng nhau.",
    "analysis": ana_7, "solution": sol_7,
    "pitfall": "Học sinh thường hay chứng minh dài dòng qua tam giác bằng nhau mà không tận dụng Dấu hiệu 3 (nhanh hơn gấp đôi).",
    "extension": "Khi lấy các đoạn bằng nhau trên hai cạnh đối của hình bình hành ($AE = CF$), các tứ giác mới tạo thành luôn có các cạnh đối song song và bằng nhau."
})

# Bài 8: Mô hình 5 HBH lồng nhau từ hai trung điểm (Mức 2)
ana_8 = make_heuristic_diagram(
    target="Chứng minh MINK là hình bình hành",
    intermediate="AMCN là HBH => AN // CM (IN // MK); MBND là HBH => DM // BN (IM // NK)",
    premise="M, N là trung điểm AB, CD của HBH ABCD",
    why_text="Từ các hình bình hành AMCN và MBND, ta có AN // CM và DM // BN, suy ra tứ giác MINK có các cặp cạnh đối song song nên là hình bình hành."
)
sol_8 = """
<p><strong>a) Chứng minh AMND và MBCN là hình bình hành:</strong></p>
<p>Vì $M, N$ là trung điểm của $AB, CD$ và $AB = CD, AB \parallel CD$ nên:</p>
<p>$$AM = MB = CN = ND = \frac{AB}{2}.$$</p>
<p>Tứ giác $AMND$ có $AM \parallel DN$ và $AM = DN$ nên là hình bình hành.</p>
<p>Tương tự, tứ giác $MBCN$ có $MB \parallel CN$ và $MB = CN$ nên là hình bình hành.</p>
<p><strong>b) Chứng minh AN song song và bằng CM:</strong></p>
<p>Xét tứ giác $AMCN$ có $AM \parallel CN$ và $AM = CN$, do đó $AMCN$ là hình bình hành.</p>
<p>Suy ra hai cạnh đối $AN$ và $CM$ song song và bằng nhau: $AN \parallel CM$ và $AN = CM$.</p>
<p><strong>c) Chứng minh tứ giác MINK là hình bình hành:</strong></p>
<p>Chứng minh tương tự, tứ giác $MBND$ là hình bình hành nên $DM \parallel BN$.</p>
<p>Xét tứ giác $MINK$:</p>
<p>• Vì $AN \parallel CM$ nên $IN \parallel MK$;</p>
<p>• Vì $DM \parallel BN$ nên $IM \parallel NK$.</p>
<p>Tứ giác $MINK$ có các cạnh đối song song nên là hình bình hành.</p>
"""
slides.append({
    "slide_num": 9, "pid": 8,
    "jump_label": "Slide 9: Bài 8 (Mô hình 5 HBH lồng nhau từ trung điểm)",
    "badge": "Dạng 2: Chứng minh HBH",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_midpoints(),
    "debai": "Cho hình bình hành $ABCD$. Gọi $M, N$ lần lượt là trung điểm của các cạnh $AB$ và $CD$.<br>a) Chứng minh hai tứ giác $AMND$ và $MBCN$ là những hình bình hành.<br>b) Chứng minh đoạn thẳng $AN$ song song và bằng đoạn thẳng $CM$.<br>c) Gọi $I$ là giao điểm của $AN$ và $DM$, $K$ là giao điểm của $BN$ và $CM$. Chứng minh tứ giác $MINK$ là hình bình hành.",
    "analysis": ana_8, "solution": sol_8,
    "pitfall": "Học sinh thường quên không chứng minh tứ giác MBND là HBH mà tự tiện suy ra ngay IM // NK.",
    "extension": "Hình bình hành MINK có tâm đối xứng trùng với tâm đối xứng của hình bình hành ABCD."
})

# --- DẠNG 3: VẬN DỤNG HÌNH BÌNH HÀNH CHỨNG MINH QUAN HỆ HÌNH HỌC ---

# Bài 9: Điểm đối xứng qua tâm O (Mức 1)
ana_9 = make_heuristic_diagram(
    target="Chứng minh A'B' // AB và A'B' = AB",
    intermediate="Chứng minh tứ giác ABA'B' là hình bình hành theo Dấu hiệu 5",
    premise="O là trung điểm của AA' và O là trung điểm của BB'",
    why_text="Hai đường chéo AA' và BB' cắt nhau tại trung điểm O của mỗi đường. Theo Dấu hiệu 5, tứ giác là HBH, kéo theo hai cạnh đối song song và bằng nhau."
)
sol_9 = """
<p><strong>a) Chứng minh tứ giác ABA'B' là hình bình hành:</strong></p>
<p>Theo giả thiết, điểm $A'$ đối xứng với $A$ qua điểm $O$ nên $O$ là trung điểm của $AA'$.</p>
<p>Điểm $B'$ đối xứng với $B$ qua điểm $O$ nên $O$ là trung điểm của $BB'$.</p>
<p>Xét tứ giác $ABA'B'$, có hai đường chéo $AA'$ và $BB'$ cắt nhau tại trung điểm $O$ của mỗi đường.</p>
<p>Áp dụng Dấu hiệu nhận biết 5, tứ giác $ABA'B'$ là hình bình hành.</p>
<p><strong>b) Chứng minh A'B' song song và bằng AB:</strong></p>
<p>Vì $ABA'B'$ là hình bình hành nên hai cạnh đối $A'B'$ và $AB$ song song và bằng nhau:</p>
<p>$$A'B' \parallel AB \quad \text{và} \quad A'B' = AB.$$</p>
"""
slides.append({
    "slide_num": 10, "pid": 9, "is_example": True,
    "jump_label": "Slide 10: Bài 9 (Ví dụ mẫu: Điểm đối xứng qua O)",
    "badge": "Dạng 3: Chứng minh quan hệ hình học",
    "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_diagonals(),
    "debai": "Cho hai điểm phân biệt $A, B$ và điểm $O$ không nằm trên đường thẳng $AB$. Lấy điểm $A'$ đối xứng với $A$ qua $O$, điểm $B'$ đối xứng với $B$ qua $O$.<br>a) Chứng minh tứ giác $ABA'B'$ là hình bình hành.<br>b) Từ đó chứng minh đoạn thẳng $A'B'$ song song và bằng đoạn thẳng $AB$.",
    "analysis": ana_9, "solution": sol_9,
    "pitfall": "Học sinh hay ghi nhầm tên tứ giác thành ABB'A' dẫn đến xác định sai hai đường chéo.",
    "extension": "Đây chính là bản chất hình học của phép đối xứng tâm: Biến một đoạn thẳng thành đoạn thẳng song song và bằng nó."
})

# Bài 10: Chứng minh 3 điểm thẳng hàng qua tâm O (Mức 2)
ana_10 = make_heuristic_diagram(
    target="Chứng minh ba điểm P, O, Q thẳng hàng",
    intermediate="Chứng minh BPDQ là hình bình hành có tâm đối xứng là O => PQ đi qua O",
    premise="BEDF là HBH => DE // BF (DP // BQ); ABCD là HBH => BP // DQ",
    why_text="Chứng minh tứ giác BPDQ là hình bình hành nhận O làm trung điểm của đường chéo BD, do đó đường chéo thứ hai PQ cũng phải nhận O làm trung điểm và đi qua O."
)
sol_10 = """
<p><strong>a) Chứng minh tứ giác BEDF là hình bình hành:</strong></p>
<p>Vì $ABCD$ là hình bình hành nên hai đường chéo $AC$ và $BD$ cắt nhau tại trung điểm $O$ của mỗi đường, suy ra $OB = OD$.</p>
<p>Theo giả thiết ta có $OE = OF$, do đó $O$ cũng là trung điểm của đoạn thẳng $EF$.</p>
<p>Tứ giác $BEDF$ có hai đường chéo $EF$ và $BD$ cắt nhau tại trung điểm $O$ của mỗi đường nên là hình bình hành.</p>
<p><strong>b) Chứng minh ba điểm P, O, Q thẳng hàng:</strong></p>
<p>Vì $BEDF$ là hình bình hành nên $DE \parallel BF$, tức là $DP \parallel BQ$.</p>
<p>Mặt khác, vì $ABCD$ là hình bình hành nên $AB \parallel CD$, tức là $BP \parallel DQ$.</p>
<p>Tứ giác $BPDQ$ có các cặp cạnh đối song song nên là hình bình hành.</p>
<p>Do đó hai đường chéo $BD$ và $PQ$ phải cắt nhau tại trung điểm của mỗi đường.</p>
<p>Mà $O$ là trung điểm của $BD$ nên $O$ cũng là trung điểm của $PQ$.</p>
<p>Suy ra ba điểm $P, O, Q$ thẳng hàng.</p>
"""
slides.append({
    "slide_num": 11, "pid": 10,
    "jump_label": "Slide 11: Bài 10 (Chứng minh thẳng hàng qua tâm đối xứng)",
    "badge": "Dạng 3: Chứng minh quan hệ hình học",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_diagonals(),
    "debai": "Cho hình bình hành $ABCD$ có $O$ là giao điểm của hai đường chéo $AC$ và $BD$. Trên đoạn thẳng $OA$ lấy điểm $E$, trên đoạn thẳng $OC$ lấy điểm $F$ sao cho $OE = OF$.<br>a) Chứng minh tứ giác $BEDF$ là hình bình hành.<br>b) Tia $DE$ cắt cạnh $AB$ tại điểm $P$, tia $BF$ cắt cạnh $CD$ tại điểm $Q$. Chứng minh ba điểm $P, O, Q$ thẳng hàng.",
    "analysis": ana_10, "solution": sol_10,
    "pitfall": "Học sinh thường hay kẻ thêm đường thẳng phụ phức tạp thay vì nhận diện tứ giác BPDQ là hình bình hành.",
    "extension": "Để chứng minh ba điểm thẳng hàng, ta có thể chứng minh chúng cùng nằm trên đường chéo của một hình bình hành có chung tâm đối xứng."
})

# Bài 11: Đoạn vuông góc AHCK và tính thẳng hàng H, O, K (Mức 2)
ana_11 = make_heuristic_diagram(
    target="Chứng minh AHCK là HBH và H, O, K thẳng hàng, OH = OK",
    intermediate="Tam giác vuông AHD = CKB (cạnh huyền - góc nhọn) => AH = CK; AH // CK vì cùng vuông góc BD",
    premise="ABCD là HBH; AH vuông góc BD, CK vuông góc BD tại H, K",
    why_text="Đường chéo AC của HBH AHCK đi qua trung điểm O, do đó đường chéo thứ hai HK cũng phải nhận O làm trung điểm."
)
sol_11 = """
<p><strong>a) Chứng minh tam giác AHD bằng tam giác CKB:</strong></p>
<p>Vì $ABCD$ là hình bình hành nên $AD = BC$ và $AD \parallel BC$.</p>
<p>Do $AD \parallel BC$ nên hai góc so le trong bằng nhau: $\widehat{ADH} = \widehat{CBK}$.</p>
<p>Xét hai tam giác vuông $\triangle AHD$ (tại $H$) và $\triangle CKB$ (tại $K$):</p>
<p>• Cạnh huyền $AD = BC$;</p>
<p>• Góc nhọn $\widehat{ADH} = \widehat{CBK}$.</p>
<p>Do đó $\triangle AHD = \triangle CKB$ (cạnh huyền - góc nhọn), suy ra $AH = CK$.</p>
<p><strong>b) Chứng minh tứ giác AHCK là hình bình hành:</strong></p>
<p>Vì $AH \perp BD$ và $CK \perp BD$ nên $AH \parallel CK$.</p>
<p>Tứ giác $AHCK$ có $AH \parallel CK$ và $AH = CK$ nên là hình bình hành.</p>
<p><strong>c) Chứng minh H, O, K thẳng hàng và OH = OK:</strong></p>
<p>Vì $AHCK$ là hình bình hành nên hai đường chéo $AC$ và $HK$ cắt nhau tại trung điểm của mỗi đường.</p>
<p>Mà $O$ là trung điểm của $AC$ nên $O$ cũng là trung điểm của $HK$.</p>
<p>Suy ra ba điểm $H, O, K$ thẳng hàng và $OH = OK$.</p>
"""
slides.append({
    "slide_num": 12, "pid": 11,
    "jump_label": "Slide 12: Bài 11 (Đoạn vuông góc AHCK & Ba điểm H, O, K)",
    "badge": "Dạng 3: Chứng minh quan hệ hình học",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_perpendiculars(),
    "debai": "Cho hình bình hành $ABCD$. Từ hai đỉnh $A$ và $C$ lần lượt kẻ $AH \\perp BD$ và $CK \\perp BD$ ($H, K \\in BD$).<br>a) Chứng minh $\\triangle AHD = \\triangle CKB$, từ đó suy ra $AH = CK$.<br>b) Chứng minh tứ giác $AHCK$ là hình bình hành.<br>c) Gọi $O$ là giao điểm của hai đường chéo $AC$ và $BD$. Chứng minh ba điểm $H, O, K$ thẳng hàng và $OH = OK$.",
    "analysis": ana_11, "solution": sol_11,
    "pitfall": "Học sinh hay dùng tam giác bằng nhau để chứng minh OH = OK mà quên rằng chỉ cần vận dụng tính chất đường chéo HBH AHCK là có ngay cả hai kết luận.",
    "extension": "Mô hình hai đường vuông góc kẻ từ hai đỉnh đối diện xuống một đường chéo luôn tạo thành một hình bình hành mới có chung tâm đối xứng."
})

# Bài 12: Phân giác hai góc đối song song (Mức 2)
ana_12 = make_heuristic_diagram(
    target="Chứng minh tam giác ADE cân và DE song song BF",
    intermediate="Tia phân giác cắt đường song song tạo tam giác cân; DEBF có EB // DF và EB = DF",
    premise="DE là phân giác góc D; BF là phân giác góc B của HBH ABCD",
    why_text="Tia phân giác kết hợp với hai đường thẳng song song tạo ra cặp góc so le trong bằng nhau, suy ra tam giác ADE có hai góc bằng nhau nên là tam giác cân (AE = AD)."
)
sol_12 = """
<p><strong>a) Chứng minh tam giác ADE và CBF là các tam giác cân:</strong></p>
<p>Vì tia $DE$ là phân giác của góc $\widehat{D}$ nên: $\widehat{D}_1 = \widehat{D}_2 = \frac{\widehat{D}}{2}$.</p>
<p>Vì $AB \parallel CD$ nên hai góc so le trong bằng nhau: $\widehat{AED} = \widehat{D}_2$.</p>
<p>Suy ra $\widehat{AED} = \widehat{D}_1$, do đó tam giác $ADE$ cân tại $A$ ($AE = AD$).</p>
<p>Chứng minh hoàn toàn tương tự, tam giác $CBF$ cân tại $C$ ($CF = CB$).</p>
<p>Vì $AD = BC$ và $\widehat{A} = \widehat{C}$ nên hai tam giác cân này bằng nhau: $\triangle ADE = \triangle CBF$ (c-g-c).</p>
<p><strong>b) Chứng minh DEBF là hình bình hành và DE song song BF:</strong></p>
<p>Ta có $EB = AB - AE$ và $DF = CD - CF$.</p>
<p>Vì $AB = CD$ và $AE = CF$ (do $AE = AD = BC = CF$) nên suy ra $EB = DF$.</p>
<p>Lại có $EB \parallel DF$ (vì $AB \parallel CD$).</p>
<p>Do đó tứ giác $DEBF$ là hình bình hành, suy ra $DE \parallel BF$.</p>
"""
slides.append({
    "slide_num": 13, "pid": 12,
    "jump_label": "Slide 13: Bài 12 (Phân giác hai góc đối song song)",
    "badge": "Dạng 3: Chứng minh quan hệ hình học",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_bisectors(),
    "debai": "Cho hình bình hành $ABCD$ ($AB > BC$). Tia phân giác của góc $\\widehat{D}$ cắt cạnh $AB$ tại điểm $E$, tia phân giác của góc $\\widehat{B}$ cắt cạnh $CD$ tại điểm $F$.<br>a) Chứng minh $\\triangle ADE$ là tam giác cân tại $A$ và $\\triangle CBF$ là tam giác cân tại $C$.<br>b) Chứng minh hai tam giác $\\triangle ADE$ và $\\triangle CBF$ bằng nhau.<br>c) Chứng minh tứ giác $DEBF$ là hình bình hành, từ đó suy ra $DE \\parallel BF$.",
    "analysis": ana_12, "solution": sol_12,
    "pitfall": "Học sinh thường hay nhầm lẫn tia phân giác của hai góc đối diện sẽ cắt nhau, trong khi ở hình bình hành chúng luôn song song.",
    "extension": "Trong hình bình hành, tia phân giác của hai góc đối diện luôn song song với nhau: $DE \\parallel BF$."
})

# --- DẠNG 4: TÂM ĐỐI XỨNG, ĐỒNG QUY VÀ TOÁN THỰC TẾ ---

# Bài 13: Đoạn thẳng qua tâm đối xứng O (Mức 2)
ana_13 = make_heuristic_diagram(
    target="Chứng minh OM = ON và MBND là hình bình hành",
    intermediate="Tam giác OAM = OCN (g-c-g) => OM = ON; Tứ giác MBND có 2 đường chéo cắt tại trung điểm O",
    premise="Đường thẳng qua tâm O của HBH ABCD cắt AB tại M, CD tại N",
    why_text="Mọi đường thẳng đi qua tâm đối xứng O đều bị O chia đôi thành hai đoạn bằng nhau. Đây là cách nhanh nhất để dùng Dấu hiệu 5."
)
sol_13 = """
<p><strong>a) Chứng minh tam giác OAM bằng tam giác OCN:</strong></p>
<p>Vì $ABCD$ là hình bình hành nên $OA = OC$ và $AB \parallel CD$.</p>
<p>Do $AB \parallel CD$ nên hai góc so le trong bằng nhau: $\widehat{MAO} = \widehat{NCO}$.</p>
<p>Hai góc đối đỉnh: $\widehat{AOM} = \widehat{CON}$.</p>
<p>Xét $\triangle OAM$ và $\triangle OCN$, ta có:</p>
<p>• $\widehat{MAO} = \widehat{NCO}$;</p>
<p>• Cạnh $OA = OC$;</p>
<p>• $\widehat{AOM} = \widehat{CON}$.</p>
<p>Do đó $\triangle OAM = \triangle OCN$ (g-c-g), suy ra $OM = ON$ và $AM = CN$.</p>
<p><strong>b) Chứng minh MBND là hình bình hành:</strong></p>
<p>Tứ giác $MBND$ có hai đường chéo là $BD$ và $MN$.</p>
<p>Theo tính chất hình bình hành, $O$ là trung điểm của $BD$. Theo chứng minh trên, $O$ là trung điểm của $MN$.</p>
<p>Tứ giác $MBND$ có hai đường chéo cắt nhau tại trung điểm của mỗi đường nên là hình bình hành.</p>
"""
slides.append({
    "slide_num": 14, "pid": 13,
    "jump_label": "Slide 14: Bài 13 (Tâm đối xứng chia đôi mọi đoạn thẳng)",
    "badge": "Dạng 4: Toán thực tế & Mô hình hóa",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_diagonals(),
    "debai": "Cho hình bình hành $ABCD$ có $O$ là giao điểm của hai đường chéo $AC$ và $BD$. Một đường thẳng $d$ bất kì đi qua $O$, cắt cạnh $AB$ tại điểm $M$ và cắt cạnh $CD$ tại điểm $N$.<br>a) Chứng minh $\\triangle OAM = \\triangle OCN$, từ đó suy ra $OM = ON$ và $AM = CN$.<br>b) Chứng minh tứ giác $MBND$ là hình bình hành.",
    "analysis": ana_13, "solution": sol_13,
    "pitfall": "Học sinh hay mất thời gian đi tính MB = AB - AM để dùng Dấu hiệu 3, trong khi dùng Dấu hiệu 5 về đường chéo nhanh và thanh thoát hơn rất nhiều.",
    "extension": "Mọi đường thẳng chia đôi diện tích của một hình bình hành đều bắt buộc phải đi qua tâm đối xứng O của nó."
})

# Bài 14: Ba đường thẳng đồng quy tại tâm O (Mức 2)
ana_14 = make_heuristic_diagram(
    target="Chứng minh ba đoạn thẳng AC, MN, PQ đồng quy tại một điểm",
    intermediate="AMCN là HBH => MN qua trung điểm O của AC; APCQ là HBH => PQ qua trung điểm O của AC",
    premise="AM = CN trên AB, CD; AP = CQ trên AD, BC của HBH ABCD",
    why_text="Các đoạn thẳng MN và PQ lần lượt là đường chéo của các hình bình hành AMCN và APCQ có chung đường chéo AC, nên cùng cắt nhau tại trung điểm O của AC."
)
sol_14 = """
<p><strong>a) Chứng minh AMCN và APCQ là các hình bình hành:</strong></p>
<p>Vì $ABCD$ là hình bình hành nên $AB \parallel CD$, suy ra $AM \parallel CN$.</p>
<p>Lại có $AM = CN$, do đó tứ giác $AMCN$ là hình bình hành.</p>
<p>Tương tự, $AD \parallel BC \Rightarrow AP \parallel CQ$. Kết hợp $AP = CQ$, suy ra tứ giác $APCQ$ là hình bình hành.</p>
<p><strong>b) Chứng minh ba đoạn thẳng đồng quy tại O:</strong></p>
<p>Gọi $O$ là trung điểm của đường chéo $AC$.</p>
<p>Vì $AMCN$ là hình bình hành nên đường chéo thứ hai $MN$ phải đi qua trung điểm $O$ của $AC$.</p>
<p>Vì $APCQ$ là hình bình hành nên đường chéo thứ hai $PQ$ phải đi qua trung điểm $O$ của $AC$.</p>
<p>Như vậy cả ba đoạn thẳng $AC, MN, PQ$ đều cùng đi qua điểm $O$.</p>
<p>Do đó ba đoạn thẳng $AC, MN, PQ$ đồng quy tại điểm $O$.</p>
"""
slides.append({
    "slide_num": 15, "pid": 14,
    "jump_label": "Slide 15: Bài 14 (Chùm đường chéo đồng quy tại O)",
    "badge": "Dạng 4: Toán thực tế & Mô hình hóa",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_diagonals(),
    "debai": "Cho hình bình hành $ABCD$. Lấy điểm $M$ trên cạnh $AB$, điểm $N$ trên cạnh $CD$ sao cho $AM = CN$. Lấy điểm $P$ trên cạnh $AD$, điểm $Q$ trên cạnh $BC$ sao cho $AP = CQ$.<br>a) Chứng minh tứ giác $AMCN$ và tứ giác $APCQ$ là những hình bình hành.<br>b) Chứng minh ba đoạn thẳng $AC, MN, PQ$ cùng cắt nhau tại một điểm (đồng quy).",
    "analysis": ana_14, "solution": sol_14,
    "pitfall": "Học sinh thường cố gắng chứng minh các cặp cạnh song song bằng tam giác bằng nhau rất vất vả thay vì chỉ ra tâm đối xứng O chung.",
    "extension": "Các hình bình hành có chung một đường chéo thì các đường chéo còn lại luôn đồng quy tại trung điểm của đường chéo chung đó."
})

# Bài 15: Bài toán mở đầu SGK Trang 57 & 61 (Mức 2)
ana_15 = make_heuristic_diagram(
    target="Dựng đường thẳng qua O cắt a tại A, cắt b tại B sao cho OA = OB",
    intermediate="Dựng điểm K đối xứng với đỉnh góc S qua O => Tứ giác SAKB là hình bình hành có tâm O",
    premise="Hai con đường a, b cắt nhau tại đỉnh góc S; Điểm dân cư O nằm trong góc",
    why_text="Để O là trung điểm đường chéo AB, ta tạo hình bình hành SAKB nhận O làm trung điểm đường chéo thứ hai SK. Khi đó K là điểm đối xứng của S qua O."
)
sol_15 = """
<p><strong>a) Các bước dựng hình trên thực địa:</strong></p>
<p>• <strong>Bước 1:</strong> Nối đoạn thẳng $SO$ từ ngã ba $S$ đến điểm dân cư $O$.</p>
<p>• <strong>Bước 2:</strong> Trên tia đối của tia $OS$, lấy điểm $K$ sao cho $OK = OS$ (điểm $K$ đối xứng với $S$ qua $O$).</p>
<p>• <strong>Bước 3:</strong> Từ điểm $K$, kẻ đường thẳng song song với con đường $b$, cắt con đường $a$ tại điểm $A$.</p>
<p>• <strong>Bước 4:</strong> Từ điểm $K$, kẻ đường thẳng song song với con đường $a$, cắt con đường $b$ tại điểm $B$.</p>
<p>Nối hai điểm $A$ và $B$, ta được con đường cần mở đi qua $O$.</p>
<p><strong>b) Chứng minh cách dựng thỏa mãn OA = OB:</strong></p>
<p>Xét tứ giác $SAKB$, ta có $KA \parallel SB$ (theo bước 3) và $KB \parallel SA$ (theo bước 4).</p>
<p>Tứ giác $SAKB$ có các cạnh đối song song nên là hình bình hành.</p>
<p>Do đó hai đường chéo $SK$ và $AB$ cắt nhau tại trung điểm của mỗi đường.</p>
<p>Vì điểm $O$ là trung điểm của đường chéo $SK$ (theo bước 2), nên điểm $O$ cũng bắt buộc là trung điểm của đường chéo $AB$.</p>
<p>Suy ra $OA = OB$. Con đường $AB$ hoàn toàn thỏa mãn yêu cầu đề bài.</p>
"""
slides.append({
    "slide_num": 16, "pid": 15,
    "jump_label": "Slide 16: Bài 15 (Bài toán mở đầu SGK Trang 57 & 61)",
    "badge": "Dạng 4: Toán thực tế & Mô hình hóa",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_realworld_opening(),
    "debai": "Bài toán mở đầu SGK (Trang 57 & 61): Hai con đường lớn $a$ và $b$ cắt nhau tạo thành một góc tại đỉnh $S$. Bên trong góc đó có một khu dân cư tại điểm $O$. Người ta cần mở một con đường thẳng đi qua $O$, cắt con đường $a$ tại điểm $A$ và cắt con đường $b$ tại điểm $B$ sao cho khoảng cách $OA = OB$ (tức là điểm $O$ nằm chính giữa hai nút giao).<br>a) Hãy nêu các bước dựng hình để xác định chính xác vị trí hai điểm $A$ và $B$.<br>b) Dựa vào kiến thức hình bình hành, hãy chứng minh cách dựng trên thỏa mãn $OA = OB$.",
    "analysis": ana_15, "solution": sol_15,
    "pitfall": "Học sinh thường vẽ mò một đường thẳng qua O rồi ước lượng bằng mắt sao cho OA = OB mà không biết thuật toán dựng điểm đối xứng K.",
    "extension": "Bài toán giải quyết việc dựng đoạn thẳng đi qua một điểm cho trước và nhận điểm đó làm trung điểm, có hai đầu mút nằm trên hai đường thẳng cắt nhau."
})

# Bài 16: Toán thực tế cổng xếp & thang nâng chữ X (Mức 2)
ana_16 = make_heuristic_diagram(
    target="Giải thích vì sao ray cổng xếp và sàn nâng ô tô luôn song song",
    intermediate="Mỗi mắt lưới là HBH => cạnh đối luôn song song; Thang nâng chữ X có 2 thanh cắt tại trung điểm => HBH",
    premise="Cổng xếp gồm các thanh thép bằng nhau chéo nhau; Thang nâng ô tô cắt tại trung điểm O",
    why_text="Cơ cấu hình bình hành là cơ cấu cơ học giữ hướng song song bất biến ở mọi góc mở."
)
sol_16 = """
<p><strong>a) Nguyên lí cổng xếp tự động:</strong></p>
<p>Các thanh thép ghép chéo nhau tạo thành hệ thống các tứ giác mắt lưới liên tiếp.</p>
<p>Do các thanh thép có kích thước tương ứng bằng nhau nên mỗi mắt lưới là một hình bình hành.</p>
<p>Theo tính chất hình bình hành, hai cạnh đối diện trên và dưới luôn luôn song song với nhau.</p>
<p>Khi kéo dãn ra hoặc đẩy xếp lại, các góc của mắt lưới thay đổi nhưng các cạnh đối diện vẫn luôn giữ quan hệ song song.</p>
<p>Do đó mép ray trên và mép ray dưới của cổng xếp luôn luôn song song với nhau.</p>
<p><strong>b) Nguyên lí thang nâng ô tô chữ X:</strong></p>
<p>Xét tứ giác $ACBD$ tạo bởi sàn nâng $AC$, mặt đất $BD$ và hai thanh nâng $AB, CD$.</p>
<p>Theo thiết kế, hai thanh nâng $AB$ và $CD$ cắt nhau tại trung điểm $O$ của mỗi thanh.</p>
<p>Áp dụng Dấu hiệu nhận biết 5, tứ giác $ACBD$ luôn là một hình bình hành ở mọi độ cao nâng.</p>
<p>Theo tính chất hình bình hành, sàn nâng $AC$ luôn luôn song song với mặt nền $BD$.</p>
<p>Nhờ đó sàn nâng giữ được trạng thái thăng bằng tuyệt đối, bảo đảm an toàn cho xe ô tô không bị nghiêng lật.</p>
"""
slides.append({
    "slide_num": 17, "pid": 16,
    "jump_label": "Slide 17: Bài 16 (Toán thực tế kỹ thuật: Cổng xếp & Thang nâng)",
    "badge": "Dạng 4: Toán thực tế & Mô hình hóa",
    "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Thực tế",
    "type": "problem_with_svg", "svg_code": make_svg_realworld_opening(),
    "debai": "Trong đời sống kỹ thuật và sản xuất:<br>a) Cổng xếp tự động ở các cơ quan, trường học gồm nhiều thanh thép bằng nhau bắt chéo liên kết với nhau bằng các khớp trục xoay, tạo thành các hình bình hành liên tiếp. Giải thích vì sao khi kéo dãn ra hoặc đẩy xếp gọn lại thì thanh ray trên và thanh ray dưới của cổng luôn luôn song song với nhau?<br>b) Một chiếc thang nâng xe ô tô kiểu chữ X có hai thanh nâng $AB$ và $CD$ cắt nhau tại trung điểm $O$ của mỗi thanh. Chứng minh rằng sàn nâng $AC$ luôn song song với mặt đất $BD$ ở mọi độ cao nâng.",
    "analysis": ana_16, "solution": sol_16,
    "pitfall": "Học sinh thường giải thích bằng cảm tính vật lý ('vì các thanh bằng nhau') mà không nêu được bản chất hình học: Tứ giác có hai đường chéo cắt nhau tại trung điểm là HBH.",
    "extension": "Cơ cấu hình bình hành giúp giữ cho hai thanh đối diện luôn song song dù khoảng cách hoặc góc mở thay đổi."
})

# --- DẠNG 5: MỞ RỘNG VẬN DỤNG CAO ÔN THI VÀO LỚP 10 (~20%) ---

# Bài 17: Phương pháp tạo hình bình hành phụ (Mức 3)
ana_17 = make_heuristic_diagram(
    target="Chứng minh ABDC là HBH và tam giác ECD cân tại D",
    intermediate="Tam giác MBD = MCA (g-c-g) => BD = AC; ACDE có CD // AE và CD = AE => ACDE là HBH => DE = AC",
    premise="M là trung điểm BC; BD // AC; E đối xứng B qua A (AE = AB)",
    why_text="Tạo hình bình hành phụ để chuyển cạnh là phương pháp tư duy trọng tâm giúp đưa các đoạn thẳng cần so sánh về cùng một tam giác."
)
sol_17 = """
<p><strong>a) Chứng minh tứ giác ABDC là hình bình hành:</strong></p>
<p>Vì $BD \parallel AC$ nên hai góc so le trong bằng nhau: $\widehat{DBC} = \widehat{ACB}$.</p>
<p>Xét $\triangle MBD$ và $\triangle MCA$, ta có:</p>
<p>• $\widehat{DBC} = \widehat{ACB}$;</p>
<p>• Cạnh $MB = MC$ ($M$ là trung điểm $BC$);</p>
<p>• Hai góc đối đỉnh $\widehat{BMD} = \widehat{CMA}$.</p>
<p>Do đó $\triangle MBD = \triangle MCA$ (g-c-g), suy ra $BD = AC$.</p>
<p>Tứ giác $ABDC$ có một cặp cạnh đối vừa song song vừa bằng nhau ($BD \parallel AC$ và $BD = AC$) nên là hình bình hành.</p>
<p><strong>b) Chứng minh tứ giác ACDE là hình bình hành:</strong></p>
<p>Vì $ABDC$ là hình bình hành nên $CD \parallel AB$ và $CD = AB$.</p>
<p>Mặt khác, điểm $E$ nằm trên tia đối của tia $AB$ và $AE = AB$ nên $CD \parallel AE$ và $CD = AE$.</p>
<p>Tứ giác $ACDE$ có một cặp cạnh đối vừa song song vừa bằng nhau nên là hình bình hành.</p>
<p><strong>c) Chứng minh tam giác ECD cân tại D:</strong></p>
<p>Vì $ACDE$ là hình bình hành nên hai cạnh đối $DE$ và $AC$ bằng nhau: $DE = AC$.</p>
<p>Theo câu a, vì $ABDC$ là hình bình hành nên $DC = AB$.</p>
<p>Lại có $AE = AB$ (theo giả thiết), suy ra nếu tam giác $ABC$ có $AC = AB$ thì $DE = DC$, tức là tam giác $ECD$ cân tại $D$.</p>
"""
slides.append({
    "slide_num": 18, "pid": 17,
    "jump_label": "Slide 18: Bài 17 (Phương pháp tạo HBH phụ để chuyển cạnh)",
    "badge": "Dạng 5: Mở rộng Khá - Giỏi thi vào 10",
    "level": 3, "level_text": "Mức 3: Mở rộng Khá — Giỏi ôn thi 10",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_basic(110, True, False, False),
    "debai": "Cho tam giác $ABC$. Gọi $M$ là trung điểm của cạnh $BC$. Kẻ đường thẳng qua $B$ song song với $AC$, cắt tia đối của tia $MA$ tại điểm $D$.<br>a) Chứng minh tứ giác $ABDC$ là hình bình hành.<br>b) Lấy điểm $E$ trên tia đối của tia $AB$ sao cho $AE = AB$. Chứng minh tứ giác $ACDE$ là hình bình hành.<br>c) Khảo sát điều kiện của tam giác $ABC$ để tam giác $ECD$ cân tại $D$.",
    "analysis": ana_17, "solution": sol_17,
    "pitfall": "Học sinh thường quên không chứng minh tính thẳng hàng của B, A, E trước khi kết luận CD // AE.",
    "extension": "Phương pháp kéo dài trung tuyến một đoạn bằng chính nó và kẻ đường song song tạo hình bình hành phụ giúp chuyển các cạnh rời nhau về cùng một tam giác."
})

# Bài 18: Giao điểm 4 tia phân giác tạo hình chữ nhật (Mức 3)
ana_18 = make_heuristic_diagram(
    target="Chứng minh tứ giác tạo bởi 4 tia phân giác có 4 góc vuông",
    intermediate="Hai góc kề bù nhau => tổng hai nửa góc bằng 90° => góc thứ ba của tam giác bằng 90°",
    premise="Tia phân giác của 4 góc trong HBH ABCD cắt nhau",
    why_text="Hai góc kề một cạnh của HBH bù nhau: A + B = 180° => A/2 + B/2 = 90°. Trong tam giác có hai góc cộng lại bằng 90° thì góc còn lại vuông."
)
sol_18 = """
<p><strong>Chứng minh tứ giác tạo bởi bốn tia phân giác là hình có bốn góc vuông:</strong></p>
<p>Vì $ABCD$ là hình bình hành nên hai góc kề một cạnh bù nhau: $\widehat{A} + \widehat{B} = 180^\circ$.</p>
<p>Vì các tia là phân giác nên:</p>
<p>$$\frac{\widehat{A}}{2} + \frac{\widehat{B}}{2} = \frac{\widehat{A} + \widehat{B}}{2} = \frac{180^\circ}{2} = 90^\circ.$$</p>
<p>Gọi $I$ là giao điểm của tia phân giác góc $\widehat{A}$ và tia phân giác góc $\widehat{B}$.</p>
<p>Xét tam giác $ABI$, ta có: $\widehat{IAB} + \widehat{IBA} = 90^\circ$.</p>
<p>Do đó góc thứ ba là: $\widehat{AIB} = 180^\circ - 90^\circ = 90^\circ$.</p>
<p>Chứng minh hoàn toàn tương tự cho ba đỉnh giao điểm còn lại, mỗi góc đều bằng $90^\circ$.</p>
<p><strong>Kết luận:</strong> Tứ giác tạo bởi bốn tia phân giác của một hình bình hành có bốn góc vuông (đây chính là hình chữ nhật).</p>
"""
slides.append({
    "slide_num": 19, "pid": 18,
    "jump_label": "Slide 19: Bài 18 (Giao điểm 4 tia phân giác tạo hình vuông vức)",
    "badge": "Dạng 5: Mở rộng Khá - Giỏi thi vào 10",
    "level": 3, "level_text": "Mức 3: Mở rộng Khá — Giỏi ôn thi 10",
    "type": "problem_with_svg", "svg_code": make_svg_hbh_bisectors(),
    "debai": "Cho hình bình hành $ABCD$ ($AB > BC$). Các tia phân giác của bốn góc $\\widehat{A}, \\widehat{B}, \\widehat{C}, \\widehat{D}$ cắt nhau tạo thành một tứ giác.<br>Chứng minh rằng tứ giác tạo thành có bốn góc vuông (hình chữ nhật).",
    "analysis": ana_18, "solution": sol_18,
    "pitfall": "Học sinh thường cố gắng chứng minh hai đường chéo bằng nhau rất dài, trong khi chỉ cần chỉ ra 3 đến 4 góc vuông bằng tổng hai nửa góc 90°.",
    "extension": "Tứ giác tạo bởi các đường phân giác trong của một hình bình hành luôn luôn là một hình chữ nhật."
})

# Bài 19: Phát minh định lý đường trung bình qua HBH (Mức 3)
ana_19 = make_heuristic_diagram(
    target="Chứng minh DE // BC và DE = 1/2 BC (Định lí đường trung bình)",
    intermediate="ADCF là HBH => CF // AD và CF = AD => CF // BD và CF = BD => BDCF là HBH => DF // BC và DF = BC",
    premise="D, E là trung điểm AB, AC; Lấy F trên tia đối ED sao cho EF = ED",
    why_text="Kéo dài đoạn ED lấy EF = ED để tạo hình bình hành phụ ADCF, từ đó suy ra CF song song và bằng BD, giúp chứng minh BDCF là hình bình hành."
)
sol_19 = """
<p><strong>a) Chứng minh tứ giác ADCF là hình bình hành:</strong></p>
<p>Tứ giác $ADCF$ có hai đường chéo là $AC$ và $DF$.</p>
<p>Theo giả thiết, điểm $E$ là trung điểm của $AC$. Theo cách dựng, $E$ là trung điểm của $DF$ ($EF = ED$).</p>
<p>Tứ giác $ADCF$ có hai đường chéo cắt nhau tại trung điểm của mỗi đường nên là hình bình hành.</p>
<p><strong>b) Chứng minh tứ giác BDCF là hình bình hành:</strong></p>
<p>Vì $ADCF$ là hình bình hành nên hai cạnh đối song song và bằng nhau: $CF \parallel AD$ và $CF = AD$.</p>
<p>Vì $D$ là trung điểm của $AB$ nên $AD = BD$ và $A, D, B$ thẳng hàng.</p>
<p>Suy ra $CF \parallel BD$ và $CF = BD$.</p>
<p>Tứ giác $BDCF$ có một cặp cạnh đối vừa song song vừa bằng nhau nên là hình bình hành.</p>
<p><strong>c) Chứng minh định lí đường trung bình:</strong></p>
<p>Vì $BDCF$ là hình bình hành nên hai cạnh đối $DF$ và $BC$ song song và bằng nhau:</p>
<p>$$DF \parallel BC \quad \text{và} \quad DF = BC.$$</p>
<p>Vì $D, E, F$ thẳng hàng và $E$ là trung điểm của $DF$ nên $DE \parallel BC$.</p>
<p>Đồng thời: $DE = \frac{DF}{2} = \frac{BC}{2}$.</p>
<p><strong>Kết luận:</strong> Đoạn thẳng nối trung điểm hai cạnh của tam giác thì song song với cạnh thứ ba và bằng nửa cạnh đó.</p>
"""
slides.append({
    "slide_num": 20, "pid": 19,
    "jump_label": "Slide 20: Bài 19 (Phát minh định lý đường trung bình tam giác)",
    "badge": "Dạng 5: Mở rộng Khá - Giỏi thi vào 10",
    "level": 3, "level_text": "Mức 3: Mở rộng Khá — Giỏi ôn thi 10",
    "type": "problem_with_svg", "svg_code": make_svg_extension_median(),
    "debai": "Cho tam giác $ABC$. Gọi $D, E$ lần lượt là trung điểm của hai cạnh $AB$ và $AC$. Trên tia đối của tia $ED$ lấy điểm $F$ sao cho $EF = ED$.<br>a) Chứng minh tứ giác $ADCF$ là hình bình hành.<br>b) Chứng minh tứ giác $BDCF$ là hình bình hành.<br>c) Từ đó chứng minh đoạn thẳng $DE$ song song với cạnh $BC$ và có độ dài bằng nửa cạnh $BC$: $DE \\parallel BC$ và $DE = \\frac{1}{2}BC$.",
    "analysis": ana_19, "solution": sol_19,
    "pitfall": "Học sinh thường quên giải thích ba điểm A, D, B thẳng hàng nên không suy ra được CF // BD một cách chặt chẽ.",
    "extension": "Phương pháp này dùng tính chất hình bình hành để chứng minh Định lí đường trung bình của tam giác mà không cần dùng định lí Ta-lét hay tam giác đồng dạng."
})

# ==============================================================================
# 3. GỌI ENGINE BUILD VÀ XUẤT FILE HOÀN CHỈNH
# ==============================================================================

lesson_data = {
    "ten_bai_hoc": "BÀI 12: HÌNH BÌNH HÀNH (TOÁN 8 — KNTT)",
    "ten_chuyen_de": "CHUYÊN ĐỀ PHÂN DẠNG VÀ RÈN KỸ NĂNG: HÌNH BÌNH HÀNH",
    "slides": slides
}

import datetime
today_folder = datetime.datetime.now().strftime("%d.%m")
output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'Ket_qua', today_folder, 'Bai_12_Hinh_Binh_Hanh_Toan_8.html'
)

if __name__ == '__main__':
    result_path = build_bai_day_html(lesson_data, output_file)
    print("\n✅ HOÀN THÀNH BIÊN SOẠN BÀI DẠY MỚI 100%!")
    print(f"File mới đã xuất tại: {result_path}")
