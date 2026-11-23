# -*- coding: utf-8 -*-
r"""
TẠO DỮ LIỆU BÀI DẠY: TOÁN 6 - BÀI 21: HÌNH CÓ TRỤC ĐỐI XỨNG
Bám sát SGK Kết nối tri thức với cuộc sống (Trang 98 - 102) & 8 bản vá Sư phạm thực chiến
CHUẨN HOÁ VÙNG KIẾN THỨC TOÁN 6:
TUYỆT ĐỐI KHÔNG DÙNG THUẬT NGỮ "ĐƯỜNG TRUNG TRỰC" (vì Lớp 6 chưa học, Lớp 7 mới học).
Dùng đúng cách diễn đạt SGK Toán 6:
"Đường thẳng đi qua trung điểm của đoạn thẳng và vuông góc với đoạn thẳng đó".
"""

import json
import os

def create_lesson_bai_21():
    # Helper heuristic diagram
    def make_heuristic(target, intermediate, premise, key_point):
        return f"""
<div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; margin-bottom: 10px;">
  <div style="font-weight: bold; color: #1e3a8a; margin-bottom: 6px; font-size: 14px;">
    🧭 SƠ ĐỒ PHÂN TÍCH TÌM HƯỚNG GIẢI:
  </div>
  <div style="display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 13.5px; background: #ffffff; padding: 8px; border-radius: 4px; border: 1px dashed #94a3b8; flex-wrap: wrap;">
    <span style="color: #b91c1c; font-weight: bold;">[Cần tìm/kết luận]: {target}</span>
    <span style="font-weight: bold; color: #475569; font-size: 16px;">⟸</span>
    <span style="color: #d97706; font-weight: bold;">[Tính chất đối xứng]: {intermediate}</span>
    <span style="font-weight: bold; color: #475569; font-size: 16px;">⟸</span>
    <span style="color: #15803d; font-weight: bold;">[Giả thiết hình học]: {premise}</span>
  </div>
  <div style="margin-top: 8px; font-size: 13.5px; color: #334155; line-height: 1.5;">
    💡 <strong>Mấu chốt bản chất:</strong> {key_point}
  </div>
</div>"""

    slides = []

    # =========================================================================
    # SLIDE 1: TÓM TẮT LÝ THUYẾT CỐT LÕI & BẢNG ĐỐI CHIẾU SỐ TRỤC ĐỐI XỨNG
    # =========================================================================
    slide_1_html = """
<div style="padding: 10px 15px;">
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 15px;">
    <!-- Khối 1: Định nghĩa bản chất -->
    <div style="background: #eff6ff; border: 1.5px solid #3b82f6; border-radius: 8px; padding: 14px;">
      <h3 style="margin-top: 0; color: #1d4ed8; font-size: 16px; border-bottom: 1.5px solid #93c5fd; padding-bottom: 6px;">
        📌 1. Định nghĩa Hình có trục đối xứng (Toán 6)
      </h3>
      <p style="font-size: 14px; line-height: 1.6; color: #1e293b; margin-bottom: 8px;">
        • Một đường thẳng $d$ được gọi là <strong>trục đối xứng</strong> của một hình nếu khi <em>gấp</em> hình theo đường thẳng $d$, hai phần của hình đó <strong>chồng khít lên nhau</strong>.
      </p>
      <p style="font-size: 14px; line-height: 1.6; color: #1e293b; margin-bottom: 8px;">
        • Hình có tính chất trên được gọi là <strong>hình có trục đối xứng</strong>.
      </p>
      <div style="background: #ffffff; border-left: 4px solid #2563eb; padding: 8px 12px; font-size: 13.5px; color: #1e40af;">
        <strong>Bản chất hình học:</strong> Mỗi điểm $M$ thuộc hình thì điểm $M'$ đối xứng với $M$ qua đường thẳng $d$ cũng thuộc hình đó (đoạn thẳng $MM' \\perp d$ tại trung điểm $I$ của $MM'$).
      </div>
    </div>

    <!-- Khối 2: Phương pháp xác định -->
    <div style="background: #f0fdf4; border: 1.5px solid #22c55e; border-radius: 8px; padding: 14px;">
      <h3 style="margin-top: 0; color: #15803d; font-size: 16px; border-bottom: 1.5px solid #86efac; padding-bottom: 6px;">
        🔍 2. Phương pháp xác định trục đối xứng
      </h3>
      <p style="font-size: 14px; line-height: 1.6; color: #1e293b; margin-bottom: 6px;">
        <strong>Cách 1 (Gấp giấy thực nghiệm):</strong> Gấp đôi tờ giấy sao cho hai nửa hình khít nhau. Nếp gấp thẳng chính là trục đối xứng.
      </p>
      <p style="font-size: 14px; line-height: 1.6; color: #1e293b; margin-bottom: 6px;">
        <strong>Cách 2 (Sử dụng đường phân chia đặc biệt theo chuẩn SGK Toán 6):</strong>
      </p>
      <ul style="font-size: 13.5px; line-height: 1.5; color: #334155; margin: 0; padding-left: 20px;">
        <li>Đoạn thẳng: Đường thẳng đi qua trung điểm và vuông góc với đoạn thẳng.</li>
        <li>Góc: Đường thẳng chứa tia phân giác của góc.</li>
        <li>Hình đa giác đều $n$ cạnh: Có đúng $n$ trục đối xứng.</li>
      </ul>
    </div>
  </div>

  <!-- Khối 3: Bảng tra cứu số trục đối xứng của 9 hình học phẳng kinh điển -->
  <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #0f172a; font-size: 16px; margin-bottom: 10px;">
      📊 3. Bảng chuẩn hóa: Số trục đối xứng của các hình học phẳng quen thuộc
    </h3>
    <table style="width: 100%; border-collapse: collapse; font-size: 13.5px; text-align: center;">
      <thead>
        <tr style="background: #f1f5f9; color: #0f172a; border-bottom: 2px solid #cbd5e1;">
          <th style="padding: 8px; border: 1px solid #cbd5e1;">Tên hình</th>
          <th style="padding: 8px; border: 1px solid #cbd5e1;">Số trục đối xứng</th>
          <th style="padding: 8px; border: 1px solid #cbd5e1; text-align: left;">Vị trí cụ thể của trục đối xứng</th>
          <th style="padding: 8px; border: 1px solid #cbd5e1; color: #dc2626;">Cạm bẫy học sinh hay mắc</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Đoạn thẳng</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #2563eb;">1 (hoặc 2)</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">Đường thẳng đi qua trung điểm và vuông góc với đoạn thẳng (và đường thẳng chứa đoạn thẳng)</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Hay quên đường vuông góc tại trung điểm</td>
        </tr>
        <tr style="background: #f8fafc;">
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Tam giác cân</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #2563eb;">1</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">Đường thẳng đi qua đỉnh cân và trung điểm cạnh đáy</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Nhầm với đường kẻ từ các đỉnh ở đáy</td>
        </tr>
        <tr>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Tam giác đều</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #2563eb;">3</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">3 đường thẳng đi qua mỗi đỉnh và trung điểm cạnh đối diện</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Nghĩ tam giác chỉ có 1 trục</td>
        </tr>
        <tr style="background: #f8fafc;">
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Hình thang cân</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #2563eb;">1</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">Đường thẳng nối trung điểm của hai cạnh đáy</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Nghĩ nối trung điểm 2 cạnh bên</td>
        </tr>
        <tr>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Hình bình hành tổng quát</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #dc2626;">0</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">Không có trục đối xứng nào</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Nhầm lẫn đường chéo là trục!</td>
        </tr>
        <tr style="background: #f8fafc;">
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Hình chữ nhật</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #2563eb;">2</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">2 đường thẳng đi qua trung điểm các cặp cạnh đối diện</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Cực kỳ hay nhầm 2 đường chéo!</td>
        </tr>
        <tr>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Hình thoi</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #2563eb;">2</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">2 đường thẳng chứa hai đường chéo</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Nghĩ nối trung điểm các cạnh</td>
        </tr>
        <tr style="background: #f8fafc;">
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Hình vuông</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #2563eb;">4</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">2 đường chéo + 2 đường đi qua trung điểm các cạnh đối</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Đếm thiếu còn 2 trục</td>
        </tr>
        <tr>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Hình lục giác đều</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #2563eb;">6</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">3 đường chéo chính + 3 đường nối trung điểm các cạnh đối</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Chỉ đếm 3 đường chéo chính</td>
        </tr>
        <tr style="background: #f8fafc;">
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold;">Hình tròn</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; font-weight: bold; color: #16a34a;">VÔ SỐ</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left;">Mọi đường thẳng đi qua tâm đường tròn</td>
          <td style="padding: 7px; border: 1px solid #e2e8f0; text-align: left; color: #b91c1c;">Nói đường kính (đường kính là đoạn)</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""
    slides.append({
        "slide_num": 1,
        "jump_label": "Slide 1: Lý Thuyết Trọng Tâm & Bảng Đối Chiếu 9 Hình",
        "badge": "LÝ THUYẾT TRỌNG TÂM",
        "type": "theory",
        "html": slide_1_html
    })

    # =========================================================================
    # DẠNG 1: NHẬN DIỆN & ĐẾM SỐ TRỤC ĐỐI XỨNG CỦA CÁC HÌNH HỌC PHẲNG
    # =========================================================================

    # --- BÀI 1 (SLIDE 2): Đoạn thẳng & Tam giác cân, Tam giác đều ---
    svg_1 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Đoạn thẳng AB và đường thẳng vuông góc tại trung điểm -->
  <g transform="translate(10, 20)">
    <line x1="20" y1="100" x2="160" y2="100" stroke="#2563eb" stroke-width="2.5"/>
    <circle cx="20" cy="100" r="4" fill="#1e293b"/>
    <circle cx="160" cy="100" r="4" fill="#1e293b"/>
    <circle cx="90" cy="100" r="3" fill="#dc2626"/>
    <text x="10" y="95" font-size="14" font-weight="bold" fill="#0f172a">A</text>
    <text x="165" y="95" font-size="14" font-weight="bold" fill="#0f172a">B</text>
    <text x="95" y="118" font-size="13" font-weight="bold" fill="#dc2626">M</text>
    <!-- Trục d: đường thẳng đi qua trung điểm M và vuông góc AB -->
    <line x1="90" y1="20" x2="90" y2="180" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
    <text x="96" y="35" font-size="14" font-weight="bold" fill="#dc2626">d</text>
    <!-- Ký hiệu vuông góc -->
    <path d="M 90,90 L 100,90 L 100,100" fill="none" stroke="#dc2626" stroke-width="1.5"/>
    <text x="35" y="210" font-size="13" font-weight="bold" fill="#2563eb">Đoạn thẳng (Trục d qua M, d ⊥ AB)</text>
  </g>

  <!-- Tam giác cân ABC -->
  <g transform="translate(230, 20)">
    <polygon points="120,30 40,170 200,170" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2"/>
    <circle cx="120" cy="30" r="4" fill="#1e293b"/>
    <circle cx="40" cy="170" r="4" fill="#1e293b"/>
    <circle cx="200" cy="170" r="4" fill="#1e293b"/>
    <circle cx="120" cy="170" r="3" fill="#dc2626"/>
    <text x="115" y="22" font-size="14" font-weight="bold" fill="#0f172a">A</text>
    <text x="25" y="180" font-size="14" font-weight="bold" fill="#0f172a">B</text>
    <text x="208" y="180" font-size="14" font-weight="bold" fill="#0f172a">C</text>
    <text x="125" y="190" font-size="13" font-weight="bold" fill="#dc2626">H</text>
    <!-- Trục AH -->
    <line x1="120" y1="15" x2="120" y2="195" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
    <!-- Ký hiệu vuông góc tại H -->
    <path d="M 120,160 L 130,160 L 130,170" fill="none" stroke="#dc2626" stroke-width="1.5"/>
    <!-- Ký hiệu 2 cạnh bên bằng nhau -->
    <line x1="75" y1="96" x2="85" y2="104" stroke="#2563eb" stroke-width="2"/>
    <line x1="155" y1="104" x2="165" y2="96" stroke="#2563eb" stroke-width="2"/>
    <text x="60" y="210" font-size="13" font-weight="bold" fill="#2563eb">Tam giác cân (1 trục AH)</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 2, "pid": 1, "is_example": True,
        "jump_label": "Slide 2: Bài 1 (Ví dụ mẫu: Đoạn thẳng & Tam giác cân)",
        "badge": "Dạng 1: Nhận diện & Số trục đối xứng",
        "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
        "type": "problem_with_svg", "svg_code": svg_1,
        "debai": "Cho đoạn thẳng $AB = 6\\text{ cm}$ và tam giác cân $ABC$ tại $A$ ($AB = AC = 5\\text{ cm}, BC = 6\\text{ cm}$).<br>a) Bằng cách gấp giấy hoặc quan sát hình học, hãy chỉ ra trục đối xứng của đoạn thẳng $AB$. Đường thẳng đó đi qua điểm nào và có quan hệ vuông góc như thế nào với $AB$?<br>b) Hãy chỉ ra trục đối xứng của tam giác cân $ABC$. Tam giác cân có bao nhiêu trục đối xứng?<br>c) Nếu tam giác $ABC$ là tam giác đều thì nó có bao nhiêu trục đối xứng?",
        "analysis": make_heuristic(
            target="Xác định trục đối xứng của đoạn thẳng và tam giác",
            intermediate="Gấp hình sao cho $A$ trùng $B$; cạnh $AB$ trùng $AC$",
            premise="Đường thẳng đi qua trung điểm và vuông góc với đoạn thẳng; đường thẳng đi qua đỉnh và trung điểm đáy",
            key_point="Trục đối xứng của đoạn thẳng là đường thẳng đi qua trung điểm và vuông góc với đoạn thẳng đó. Tam giác cân chỉ có duy nhất 1 trục đối xứng đi qua đỉnh cân và trung điểm cạnh đáy, còn tam giác đều có 3 trục đối xứng đi qua mỗi đỉnh và trung điểm cạnh đối diện."
        ),
        "solution": """<p><strong>a) Trục đối xứng của đoạn thẳng $AB$:</strong></p>
<p>Gọi $M$ là trung điểm của đoạn thẳng $AB$ ($AM = MB = 3\\text{ cm}$).</p>
<p>Đường thẳng $d$ đi qua trung điểm $M$ và vuông góc với đoạn thẳng $AB$ chính là trục đối xứng của đoạn thẳng $AB$.</p>
<p>Khi gấp tờ giấy theo đường thẳng $d$, điểm $A$ trùng khít lên điểm $B$, nửa đoạn thẳng $MA$ trùng khít lên nửa đoạn thẳng $MB$. Ngoài ra, đường thẳng chứa đoạn thẳng $AB$ cũng là một trục đối xứng biến đoạn thẳng $AB$ thành chính nó.</p>
<p><strong>b) Trục đối xứng của tam giác cân $ABC$:</strong></p>
<p>Gọi $H$ là trung điểm của cạnh đáy $BC$. Do tam giác $ABC$ cân tại $A$ nên đường thẳng $AH$ vuông góc với cạnh đáy $BC$.</p>
<p>Đường thẳng $AH$ là trục đối xứng của tam giác $ABC$. Khi gấp tam giác theo đường thẳng $AH$, cạnh $AB$ trùng khít lên cạnh $AC$, đỉnh $B$ trùng khít lên đỉnh $C$.</p>
<p>Do đó, tam giác cân $ABC$ (không đều) có đúng <strong>1 trục đối xứng</strong>.</p>
<p><strong>c) Trường hợp tam giác $ABC$ là tam giác đều:</strong></p>
<p>Do tam giác đều có ba cạnh bằng nhau nên tam giác đều cân tại cả ba đỉnh $A, B, C$.</p>
<p>Do đó, tam giác đều có đúng <strong>3 trục đối xứng</strong>, mỗi trục là đường thẳng đi qua một đỉnh và trung điểm của cạnh đối diện.</p>
<p><strong>Kết luận:</strong> Đoạn thẳng có trục đối xứng là đường thẳng đi qua trung điểm và vuông góc với đoạn thẳng đó; tam giác cân có 1 trục đối xứng; tam giác đều có 3 trục đối xứng.</p>""",
        "pitfall": "Học sinh thường nhầm lẫn cho rằng mọi tam giác đều có trục đối xứng. Cần ghi nhớ: Tam giác thường (không cân) KHÔNG CÓ trục đối xứng nào!",
        "extension": "Số trục đối xứng của tam giác phụ thuộc vào tính chất cân/đều: Tam giác thường có 0 trục, tam giác cân có 1 trục, tam giác đều có 3 trục."
    })

    # --- BÀI 2 (SLIDE 3): Hình thang cân & Hình bình hành & Hình thoi ---
    svg_2 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Hình thang cân ABCD -->
  <g transform="translate(10, 20)">
    <polygon points="60,40 140,40 180,160 20,160" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2"/>
    <line x1="100" y1="20" x2="100" y2="180" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
    <circle cx="100" cy="40" r="3.5" fill="#dc2626"/>
    <circle cx="100" cy="160" r="3.5" fill="#dc2626"/>
    <text x="50" y="35" font-size="14" font-weight="bold" fill="#0f172a">A</text>
    <text x="145" y="35" font-size="14" font-weight="bold" fill="#0f172a">B</text>
    <text x="185" y="175" font-size="14" font-weight="bold" fill="#0f172a">C</text>
    <text x="10" y="175" font-size="14" font-weight="bold" fill="#0f172a">D</text>
    <text x="105" y="35" font-size="12" font-weight="bold" fill="#dc2626">M</text>
    <text x="105" y="175" font-size="12" font-weight="bold" fill="#dc2626">N</text>
    <text x="40" y="210" font-size="13" font-weight="bold" fill="#2563eb">Hình thang cân (1 trục MN)</text>
  </g>

  <!-- Hình thoi (2 trục) -->
  <g transform="translate(230, 20)">
    <polygon points="120,30 200,100 120,170 40,100" fill="#f0fdf4" stroke="#16a34a" stroke-width="2.2"/>
    <line x1="120" y1="15" x2="120" y2="185" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
    <line x1="25" y1="100" x2="215" y2="100" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
    <circle cx="120" cy="30" r="3.5" fill="#1e293b"/>
    <circle cx="200" cy="100" r="3.5" fill="#1e293b"/>
    <circle cx="120" cy="170" r="3.5" fill="#1e293b"/>
    <circle cx="40" cy="100" r="3.5" fill="#1e293b"/>
    <text x="115" y="22" font-size="14" font-weight="bold" fill="#0f172a">P</text>
    <text x="205" y="105" font-size="14" font-weight="bold" fill="#0f172a">Q</text>
    <text x="115" y="190" font-size="14" font-weight="bold" fill="#0f172a">R</text>
    <text x="22" y="105" font-size="14" font-weight="bold" fill="#0f172a">S</text>
    <text x="50" y="210" font-size="13" font-weight="bold" fill="#16a34a">Hình thoi (2 trục chéo)</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 3, "pid": 2,
        "jump_label": "Slide 3: Bài 2 (Hình thang cân, Hình thoi & Hình bình hành)",
        "badge": "Dạng 1: Nhận diện & Số trục đối xứng",
        "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
        "type": "problem_with_svg", "svg_code": svg_2,
        "debai": "Cho ba hình: Hình thang cân $ABCD$ ($AB \\parallel CD$), Hình thoi $PQRS$ và Hình bình hành tổng quát $EFGH$.<br>a) Chỉ ra trục đối xứng của hình thang cân $ABCD$. Hình thang cân có mấy trục đối xứng?<br>b) Hình thoi $PQRS$ có mấy trục đối xứng? Đó là những đường thẳng nào?<br>c) Hình bình hành tổng quát $EFGH$ có trục đối xứng hay không? Giải thích vì sao khi gấp theo đường chéo thì hai nửa không chồng khít.",
        "analysis": make_heuristic(
            target="Xác định số trục đối xứng của hình thang cân, hình thoi, hình bình hành",
            intermediate="Đối chiếu phép gấp qua đường nối trung điểm hai đáy và đường chéo",
            premise="Đặc điểm các cạnh, góc của tứ giác đặc biệt",
            key_point="Hình thang cân có 1 trục đối xứng nối trung điểm 2 đáy. Hình thoi có 2 trục đối xứng là 2 đường thẳng chứa 2 đường chéo. Hình bình hành tổng quát KHÔNG CÓ trục đối xứng nào."
        ),
        "solution": """<p><strong>a) Xét hình thang cân $ABCD$ ($AB \\parallel CD$):</strong></p>
<p>Gọi $M$ là trung điểm đáy nhỏ $AB$, $N$ là trung điểm đáy lớn $CD$.</p>
<p>Đường thẳng $MN$ vuông góc với cả hai đáy $AB$ và $CD$. Khi gấp hình thang theo đường thẳng $MN$, điểm $A$ trùng $B$, điểm $D$ trùng $C$, cạnh bên $AD$ chồng khít lên cạnh bên $BC$.</p>
<p>Do đó, hình thang cân có đúng <strong>1 trục đối xứng</strong> (đường thẳng nối trung điểm hai đáy).</p>
<p><strong>b) Xét hình thoi $PQRS$:</strong></p>
<p>Hình thoi có bốn cạnh bằng nhau và hai đường chéo $PR, QS$ vuông góc với nhau tại trung điểm mỗi đường.</p>
<p>Khi gấp theo đường thẳng chứa đường chéo $PR$, đỉnh $Q$ trùng khít đỉnh $S$. Tương tự khi gấp theo đường thẳng chứa đường chéo $QS$, đỉnh $P$ trùng khít đỉnh $R$.</p>
<p>Do đó, hình thoi có đúng <strong>2 trục đối xứng</strong>, chính là 2 đường thẳng chứa hai đường chéo.</p>
<p><strong>c) Xét hình bình hành tổng quát $EFGH$:</strong></p>
<p>Nếu gấp hình bình hành theo đường chéo $EG$, do các góc kề một cạnh không bằng nhau và các cạnh kề không bằng nhau, cạnh $EF$ không thể trùng với cạnh $EH$, hai nửa hình không chồng khít lên nhau.</p>
<p>Nếu gấp theo đường thẳng nối trung điểm các cạnh đối diện, hai nửa hình cũng không chồng khít.</p>
<p><strong>Kết luận:</strong> Hình thang cân có 1 trục đối xứng; hình thoi có 2 trục đối xứng; hình bình hành tổng quát <strong>không có trục đối xứng nào</strong>.</p>""",
        "pitfall": "Học sinh lớp 6 rất hay trả lời 'hình bình hành có 2 trục đối xứng là 2 đường chéo'. Cần nhấn mạnh: Chỉ khi hình bình hành là hình thoi hoặc hình vuông thì mới có trục đối xứng!",
        "extension": "Hình bình hành không có trục đối xứng nhưng có tâm đối xứng (giao điểm hai đường chéo - sẽ học ở bài sau)."
    })

    # --- BÀI 3 (SLIDE 4): Hình chữ nhật vs Hình vuông ---
    svg_3 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Hình chữ nhật ABCD (2 trục đối xứng) -->
  <g transform="translate(20, 20)">
    <polygon points="20,40 180,40 180,160 20,160" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2"/>
    <!-- 2 trục đối xứng chính thức -->
    <line x1="100" y1="20" x2="100" y2="180" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
    <line x1="5" y1="100" x2="195" y2="100" stroke="#dc2626" stroke-width="2" stroke-dasharray="6,4"/>
    <!-- Đường chéo KHÔNG PHẢI TRỤC (nét chấm mờ kèm dấu gạch chéo) -->
    <line x1="20" y1="40" x2="180" y2="160" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>
    <text x="140" y="130" font-size="16" font-weight="bold" fill="#dc2626">✕</text>
    <text x="10" y="35" font-size="14" font-weight="bold" fill="#0f172a">A</text>
    <text x="185" y="35" font-size="14" font-weight="bold" fill="#0f172a">B</text>
    <text x="185" y="175" font-size="14" font-weight="bold" fill="#0f172a">C</text>
    <text x="10" y="175" font-size="14" font-weight="bold" fill="#0f172a">D</text>
    <text x="105" y="35" font-size="12" font-weight="bold" fill="#dc2626">d₁</text>
    <text x="185" y="95" font-size="12" font-weight="bold" fill="#dc2626">d₂</text>
    <text x="25" y="210" font-size="13" font-weight="bold" fill="#2563eb">Hình chữ nhật (ĐÚNG 2 TRỤC)</text>
  </g>

  <!-- Hình vuông MNPQ (4 trục đối xứng) -->
  <g transform="translate(250, 20)">
    <polygon points="40,30 170,30 170,160 40,160" fill="#fef2f2" stroke="#dc2626" stroke-width="2.2"/>
    <!-- 2 trục nối trung điểm cạnh đối -->
    <line x1="105" y1="15" x2="105" y2="175" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="25" y1="95" x2="185" y2="95" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5,3"/>
    <!-- 2 trục đường chéo -->
    <line x1="30" y1="20" x2="180" y2="170" stroke="#ea580c" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="30" y1="170" x2="180" y2="20" stroke="#ea580c" stroke-width="1.8" stroke-dasharray="5,3"/>
    <text x="25" y="30" font-size="14" font-weight="bold" fill="#0f172a">M</text>
    <text x="175" y="30" font-size="14" font-weight="bold" fill="#0f172a">N</text>
    <text x="175" y="175" font-size="14" font-weight="bold" fill="#0f172a">P</text>
    <text x="25" y="175" font-size="14" font-weight="bold" fill="#0f172a">Q</text>
    <text x="35" y="210" font-size="13" font-weight="bold" fill="#dc2626">Hình vuông (ĐÚNG 4 TRỤC)</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 4, "pid": 3,
        "jump_label": "Slide 4: Bài 3 (So sánh Hình chữ nhật vs Hình vuông)",
        "badge": "Dạng 1: Nhận diện & Số trục đối xứng",
        "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
        "type": "problem_with_svg", "svg_code": svg_3,
        "debai": "Cho một hình chữ nhật $ABCD$ có chiều dài $8\\text{ cm}$, chiều rộng $5\\text{ cm}$ và một hình vuông $MNPQ$ có cạnh $6\\text{ cm}$.<br>a) Hình chữ nhật $ABCD$ có bao nhiêu trục đối xứng? Hãy nêu rõ vị trí của từng trục.<br>b) Đường chéo $AC$ của hình chữ nhật có phải là trục đối xứng của hình chữ nhật không? Giải thích bằng thực nghiệm gấp giấy.<br>c) Hình vuông $MNPQ$ có bao nhiêu trục đối xứng? Vì sao số trục đối xứng của hình vuông nhiều hơn hình chữ nhật?",
        "analysis": make_heuristic(
            target="Phân biệt số trục đối xứng của hình chữ nhật (2) và hình vuông (4)",
            intermediate="Gấp theo đường nối trung điểm các cạnh đối và theo đường chéo",
            premise="Độ dài các cạnh kề: HCN khác nhau ($a \\neq b$), HV bằng nhau ($a = b$)",
            key_point="Hình chữ nhật chỉ có 2 trục đối xứng nối trung điểm các cạnh đối diện, đường chéo KHÔNG là trục đối xứng. Hình vuông có 4 trục đối xứng vì 4 cạnh bằng nhau nên hai đường chéo cũng trở thành trục đối xứng."
        ),
        "solution": """<p><strong>a) Số trục đối xứng của hình chữ nhật $ABCD$:</strong></p>
<p>Hình chữ nhật $ABCD$ có đúng <strong>2 trục đối xứng</strong>, gồm:</p>
<p>• Trục $d_1$: Đường thẳng đi qua trung điểm của hai cạnh đối diện $AB$ và $CD$.</p>
<p>• Trục $d_2$: Đường thẳng đi qua trung điểm của hai cạnh đối diện $AD$ và $BC$.</p>
<p><strong>b) Đường chéo $AC$ KHÔNG PHẢI là trục đối xứng của hình chữ nhật:</strong></p>
<p>Khi gấp tờ giấy hình chữ nhật theo đường chéo $AC$, đỉnh $B$ sẽ gập sang phía bên kia nhưng không trùng với đỉnh $D$ (cạnh $BC$ ngắn hơn cạnh $CD$ nên cạnh $BC$ không khớp lên cạnh $CD$).</p>
<p>Do đó hai nửa tam giác sau khi gấp bị lệch góc, không chồng khít lên nhau. Vậy đường chéo không phải là trục đối xứng của hình chữ nhật.</p>
<p><strong>c) Số trục đối xứng của hình vuông $MNPQ$:</strong></p>
<p>Hình vuông $MNPQ$ có đúng <strong>4 trục đối xứng</strong>, gồm:</p>
<p>• 2 đường thẳng đi qua trung điểm các cặp cạnh đối diện.</p>
<p>• 2 đường thẳng chứa hai đường chéo $MP$ và $NQ$.</p>
<p><em>Giải thích:</em> Do hình vuông vừa là hình chữ nhật vừa là hình thoi (có 4 cạnh bằng nhau và 4 góc vuông), nên hình vuông kế thừa trọn vẹn 2 trục đối xứng của hình chữ nhật và 2 trục đối xứng của hình thoi, tạo thành 4 trục đối xứng.</p>
<p><strong>Kết luận:</strong> Hình chữ nhật có 2 trục đối xứng; Hình vuông có 4 trục đối xứng.</p>""",
        "pitfall": "Đây là cạm bẫy kinh điển số 1 trong các đề kiểm tra Toán 6: Học sinh khoanh bừa 'hình chữ nhật có 4 trục đối xứng' vì tưởng 2 đường chéo cũng là trục đối xứng!",
        "extension": "Mọi hình chữ nhật có 2 trục đối xứng vuông góc với nhau; khi chiều dài bằng chiều rộng (trở thành hình vuông) thì xuất hiện thêm 2 trục đối xứng theo phương đường chéo."
    })

    # --- BÀI 4 (SLIDE 5): Đa giác đều (Lục giác đều) vs Hình tròn ---
    svg_4 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Lục giác đều ABCDEF (6 trục đối xứng) -->
  <g transform="translate(20, 20)">
    <polygon points="100,20 170,60 170,140 100,180 30,140 30,60" fill="#f0fdf4" stroke="#16a34a" stroke-width="2.2"/>
    <!-- 3 đường chéo chính -->
    <line x1="100" y1="10" x2="100" y2="190" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="20" y1="55" x2="180" y2="145" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="20" y1="145" x2="180" y2="55" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5,3"/>
    <!-- 3 đường nối trung điểm cạnh đối -->
    <line x1="15" y1="100" x2="185" y2="100" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="60" y1="20" x2="140" y2="180" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="3,3"/>
    <line x1="140" y1="20" x2="60" y2="180" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="3,3"/>
    <circle cx="100" cy="100" r="3.5" fill="#0f172a"/>
    <text x="105" y="105" font-size="12" font-weight="bold" fill="#0f172a">O</text>
    <text x="25" y="210" font-size="13" font-weight="bold" fill="#16a34a">Lục giác đều (6 TRỤC ĐỐI XỨNG)</text>
  </g>

  <!-- Hình tròn tâm O (Vô số trục đối xứng) -->
  <g transform="translate(250, 20)">
    <circle cx="110" cy="100" r="75" fill="#eff6ff" stroke="#2563eb" stroke-width="2.2"/>
    <circle cx="110" cy="100" r="4" fill="#dc2626"/>
    <!-- Các đường thẳng đi qua tâm O -->
    <line x1="110" y1="15" x2="110" y2="185" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="25" y1="100" x2="195" y2="100" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="50" y1="40" x2="170" y2="160" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4,3"/>
    <line x1="50" y1="160" x2="170" y2="40" stroke="#059669" stroke-width="1.5" stroke-dasharray="4,3"/>
    <text x="115" y="95" font-size="13" font-weight="bold" fill="#dc2626">O</text>
    <text x="45" y="210" font-size="13" font-weight="bold" fill="#2563eb">Hình tròn (VÔ SỐ TRỤC ĐỐI XỨNG)</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 5, "pid": 4,
        "jump_label": "Slide 5: Bài 4 (Lục giác đều vs Hình tròn)",
        "badge": "Dạng 1: Nhận diện & Số trục đối xứng",
        "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
        "type": "problem_with_svg", "svg_code": svg_4,
        "debai": "Cho một hình lục giác đều $ABCDEF$ tâm $O$ và một hình tròn tâm $O$ bán kính $R = 4\\text{ cm}$.<br>a) Hình lục giác đều có bao nhiêu trục đối xứng? Hãy phân loại các trục đối xứng đó.<br>b) Hình tròn tâm $O$ có bao nhiêu trục đối xứng? Đó là những đường thẳng như thế nào?<br>c) Có bạn phát biểu: 'Đường kính của hình tròn là trục đối xứng của hình tròn'. Phát biểu này chính xác hay chưa chính xác? Hãy giải thích.",
        "analysis": make_heuristic(
            target="Xác định số trục đối xứng của lục giác đều và hình tròn",
            intermediate="Tính chất đối xứng qua tâm và các cặp đỉnh, cạnh đối diện",
            premise="Đa giác đều n cạnh có n trục; mọi đường thẳng qua tâm hình tròn chia đôi đường tròn",
            key_point="Lục giác đều có 6 trục đối xứng (3 đường chéo chính + 3 đường nối trung điểm các cặp cạnh đối diện). Hình tròn có vô số trục đối xứng. Trục đối xứng phải là ĐƯỜNG THẲNG đi qua tâm, còn đường kính là ĐOẠN THẲNG."
        ),
        "solution": """<p><strong>a) Số trục đối xứng của hình lục giác đều $ABCDEF$:</strong></p>
<p>Hình lục giác đều $ABCDEF$ có đúng <strong>6 trục đối xứng</strong>, được chia làm hai nhóm:</p>
<p>• Nhóm 1 (3 trục): 3 đường thẳng chứa ba đường chéo chính đi qua tâm $O$ ($AD, BE, CF$).</p>
<p>• Nhóm 2 (3 trục): 3 đường thẳng đi qua trung điểm các cặp cạnh đối diện ($AB$ và $DE$; $BC$ và $EF$; $CD$ và $FA$).</p>
<p><strong>b) Số trục đối xứng của hình tròn tâm $O$:</strong></p>
<p>Hình tròn tâm $O$ có <strong>vô số trục đối xứng</strong>.</p>
<p>Mỗi đường thẳng đi qua tâm $O$ đều chia hình tròn thành hai nửa đường tròn bằng nhau. Khi gấp theo đường thẳng đó, hai nửa hình tròn chồng khít hoàn toàn lên nhau.</p>
<p><strong>c) Nhận xét về phát biểu:</strong></p>
<p>Phát biểu trên là <strong>chưa chính xác về mặt thuật ngữ toán học</strong>.</p>
<p>• <em>Đường kính</em> là một <strong>đoạn thẳng</strong> có hai đầu mút nằm trên đường tròn.</p>
<p>• Trong khi đó, <em>trục đối xứng</em> theo định nghĩa bắt buộc phải là một <strong>đường thẳng</strong> (kéo dài vô tận về hai phía).</p>
<p>Phát biểu chuẩn xác phải là: <em>'Mỗi đường thẳng đi qua tâm (hay đường thẳng chứa đường kính) là một trục đối xứng của hình tròn'</em>.</p>
<p><strong>Kết luận:</strong> Lục giác đều có 6 trục đối xứng; hình tròn có vô số trục đối xứng.</p>""",
        "pitfall": "Học sinh hay nhầm lẫn giữa khái niệm 'đường kính' (đoạn thẳng) và 'đường thẳng chứa đường kính' (trục đối xứng). Trong bài kiểm tra tự luận, nếu viết 'đường kính là trục đối xứng' sẽ bị trừ điểm thuật ngữ.",
        "extension": "Tổng quát: Đa giác đều có $n$ cạnh thì luôn có đúng $n$ trục đối xứng. Khi số cạnh $n$ tiến ra vô cực, đa giác đều tiệm cận hình tròn, số trục đối xứng trở thành vô số."
    })

    # =========================================================================
    # DẠNG 2: CHỮ CÁI, CHỮ SỐ & BIỂU TƯỢNG ĐỜI SỐNG
    # =========================================================================

    # --- BÀI 5 (SLIDE 6): Chữ cái in hoa ---
    svg_5 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Nhóm 1 trục đứng: A, M -->
  <g transform="translate(10, 20)">
    <rect x="10" y="10" width="130" height="90" rx="8" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
    <text x="40" y="70" font-size="52" font-family="Arial, sans-serif" font-weight="bold" fill="#1e40af">A</text>
    <line x1="56" y1="18" x2="56" y2="92" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,3"/>
    <text x="85" y="70" font-size="52" font-family="Arial, sans-serif" font-weight="bold" fill="#1e40af">M</text>
    <line x1="108" y1="18" x2="108" y2="92" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,3"/>
    <text x="25" y="125" font-size="13" font-weight="bold" fill="#1e40af">1 Trục thẳng đứng</text>
  </g>

  <!-- Nhóm 1 trục ngang: B, E -->
  <g transform="translate(165, 20)">
    <rect x="10" y="10" width="130" height="90" rx="8" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
    <text x="35" y="70" font-size="52" font-family="Arial, sans-serif" font-weight="bold" fill="#15803d">B</text>
    <line x1="20" y1="52" x2="75" y2="52" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,3"/>
    <text x="85" y="70" font-size="52" font-family="Arial, sans-serif" font-weight="bold" fill="#15803d">E</text>
    <line x1="80" y1="52" x2="125" y2="52" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,3"/>
    <text x="30" y="125" font-size="13" font-weight="bold" fill="#15803d">1 Trục nằm ngang</text>
  </g>

  <!-- Nhóm 2 trục đối xứng: H, O, X -->
  <g transform="translate(320, 20)">
    <rect x="5" y="10" width="145" height="90" rx="8" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.5"/>
    <text x="20" y="70" font-size="52" font-family="Arial, sans-serif" font-weight="bold" fill="#b91c1c">H</text>
    <line x1="39" y1="18" x2="39" y2="92" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <line x1="15" y1="52" x2="63" y2="52" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <text x="75" y="70" font-size="52" font-family="Arial, sans-serif" font-weight="bold" fill="#b91c1c">O</text>
    <line x1="95" y1="18" x2="95" y2="92" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <line x1="70" y1="52" x2="120" y2="52" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <text x="25" y="125" font-size="13" font-weight="bold" fill="#b91c1c">2 Trục (Đứng & Ngang)</text>
  </g>

  <!-- Nhóm không có trục: F, G, N -->
  <g transform="translate(50, 150)">
    <rect x="10" y="10" width="370" height="75" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="50" y="60" font-size="44" font-family="Arial, sans-serif" font-weight="bold" fill="#64748b">F</text>
    <text x="140" y="60" font-size="44" font-family="Arial, sans-serif" font-weight="bold" fill="#64748b">G</text>
    <text x="230" y="60" font-size="44" font-family="Arial, sans-serif" font-weight="bold" fill="#64748b">N</text>
    <text x="310" y="60" font-size="44" font-family="Arial, sans-serif" font-weight="bold" fill="#64748b">P</text>
    <text x="100" y="78" font-size="13" font-weight="bold" fill="#64748b">KHÔNG CÓ TRỤC ĐỐI XỨNG</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 6, "pid": 5, "is_example": True,
        "jump_label": "Slide 6: Bài 5 (Ví dụ mẫu: Phân loại chữ cái in hoa)",
        "badge": "Dạng 2: Chữ cái & Biểu tượng",
        "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
        "type": "problem_with_svg", "svg_code": svg_5,
        "debai": "Cho danh sách các chữ cái in hoa tiếng Anh sau:<br>$$\\text{A, B, C, D, E, F, G, H, I, K, M, N, O, P, T, U, V, X, Y}$$<br>a) Những chữ cái nào có đúng <strong>1 trục đối xứng thẳng đứng</strong>?<br>b) Những chữ cái nào có đúng <strong>1 trục đối xứng nằm ngang</strong>?<br>c) Những chữ cái nào có từ <strong>2 trục đối xứng trở lên</strong>?<br>d) Những chữ cái nào <strong>không có trục đối xứng</strong>?",
        "analysis": make_heuristic(
            target="Phân loại chữ cái theo số lượng và hướng của trục đối xứng",
            intermediate="Kiểm tra phép gấp dọc và gấp ngang từng nét chữ",
            premise="Hình dáng hình học in hoa chuẩn phông không chân",
            key_point="Chữ đối xứng đứng có nửa trái trùng nửa phải. Chữ đối xứng ngang có nửa trên trùng nửa dưới. Chữ N hay bị nhầm có trục đối xứng nhưng thực tế N chỉ có tâm đối xứng, không có trục đối xứng!"
        ),
        "solution": """<p>Xét các chữ cái in hoa theo phông chữ in hoa chuẩn:</p>
<p><strong>a) Các chữ cái có đúng 1 trục đối xứng thẳng đứng:</strong></p>
<p>Gồm các chữ cái: <strong>A, M, T, U, V, Y</strong>.</p>
<p><em>(Khi vẽ đường thẳng đứng chính giữa chữ, nửa bên trái gấp sang trùng khít lên nửa bên phải).</em></p>
<p><strong>b) Các chữ cái có đúng 1 trục đối xứng nằm ngang:</strong></p>
<p>Gồm các chữ cái: <strong>B, C, D, E, K</strong>.</p>
<p><em>(Khi vẽ đường thẳng nằm ngang ở giữa, nửa trên gấp xuống trùng khít lên nửa dưới).</em></p>
<p><strong>c) Các chữ cái có từ 2 trục đối xứng trở lên:</strong></p>
<p>Gồm các chữ cái: <strong>H, I, X, O</strong>.</p>
<p>• Chữ H, I, X có đúng <strong>2 trục đối xứng</strong> (1 trục đứng và 1 trục ngang).</p>
<p>• Chữ O (nếu vẽ theo hình tròn) có <strong>vô số trục đối xứng</strong>; nếu vẽ theo hình elip chuẩn thì có <strong>2 trục đối xứng</strong>.</p>
<p><strong>d) Các chữ cái không có trục đối xứng:</strong></p>
<p>Gồm các chữ: <strong>F, G, N, P</strong>.</p>
<p><strong>Kết luận:</strong> Đã phân loại đầy đủ các chữ cái vào 4 nhóm đối xứng chuẩn xác.</p>""",
        "pitfall": "Chữ N là cạm bẫy rất lớn! Học sinh hay nhầm chữ N có trục đối xứng chéo. Thực tế khi gấp theo đường chéo của chữ N, hai thanh dọc sẽ lệch nhau 90 độ, không bao giờ trùng khít!",
        "extension": "Hiện tượng đối xứng trục của chữ cái được ứng dụng rộng rãi trong thiết kế biển báo cứu hộ, xe cứu thương (chữ AMBULANCE in ngược để nhìn qua gương chiếu hậu) và logo thương hiệu."
    })

    # --- BÀI 6 (SLIDE 7): Các từ ngữ & Tên riêng đối xứng ---
    svg_6 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Từ WOW (đối xứng đứng) -->
  <g transform="translate(20, 20)">
    <rect x="10" y="10" width="200" height="90" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.8"/>
    <text x="35" y="75" font-size="52" font-family="Arial, sans-serif" font-weight="bold" fill="#1d4ed8" letter-spacing="8">WOW</text>
    <line x1="110" y1="15" x2="110" y2="95" stroke="#dc2626" stroke-width="2.2" stroke-dasharray="5,3"/>
    <text x="30" y="125" font-size="13" font-weight="bold" fill="#1d4ed8">Từ WOW (1 trục đứng chính giữa)</text>
  </g>

  <!-- Từ CHOICE (đối xứng ngang) -->
  <g transform="translate(250, 20)">
    <rect x="10" y="10" width="200" height="90" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.8"/>
    <text x="25" y="75" font-size="46" font-family="Arial, sans-serif" font-weight="bold" fill="#15803d" letter-spacing="6">CHOICE</text>
    <line x1="20" y1="52" x2="200" y2="52" stroke="#dc2626" stroke-width="2.2" stroke-dasharray="5,3"/>
    <text x="20" y="125" font-size="13" font-weight="bold" fill="#15803d">Từ CHOICE (1 trục ngang xuyên suốt)</text>
  </g>

  <!-- Các từ khảo sát -->
  <g transform="translate(20, 145)">
    <rect x="10" y="10" width="430" height="80" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.8"/>
    <text x="30" y="60" font-size="34" font-family="Arial, sans-serif" font-weight="bold" fill="#b45309">HAI</text>
    <text x="130" y="60" font-size="34" font-family="Arial, sans-serif" font-weight="bold" fill="#b45309">TOOT</text>
    <text x="260" y="60" font-size="34" font-family="Arial, sans-serif" font-weight="bold" fill="#b45309">AHA</text>
    <text x="350" y="60" font-size="34" font-family="Arial, sans-serif" font-weight="bold" fill="#b45309">NOON</text>
    <text x="30" y="82" font-size="12" font-weight="bold" fill="#78350f">Khảo sát tính đối xứng trục của cả từ khi viết in hoa liền mạch</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 7, "pid": 6,
        "jump_label": "Slide 7: Bài 6 (Khảo sát các từ ngữ đối xứng)",
        "badge": "Dạng 2: Chữ cái & Biểu tượng",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_6,
        "debai": "Quan sát các từ tiếng Anh và tiếng Việt được viết hoa không chân sau đây:<br>$$\\text{WOW, AHA, TOOT, CHOICE, BED, NOON}$$<br>a) Những từ nào có <strong>trục đối xứng thẳng đứng</strong> (nghĩa là soi từ đó qua gương phẳng đặt vuông góc thì hình ảnh phản chiếu vẫn đọc được đúng từ đó)?<br>b) Những từ nào có <strong>trục đối xứng nằm ngang</strong> (nghĩa là soi từ đó qua mặt nước phẳng lặng bên dưới thì bóng ảnh vẫn đọc được đúng từ đó)?<br>c) Từ $\\text{NOON}$ có trục đối xứng hay không? Hãy phân tích sự khác nhau giữa đối xứng trục và đối xứng tâm ở từ này.",
        "analysis": make_heuristic(
            target="Xác định tính đối xứng trục của toàn bộ một từ ngữ",
            intermediate="Xét điều kiện cần: từng chữ cái phải đối xứng; điều kiện đủ: thứ tự chữ cái đối xứng từ 2 đầu",
            premise="Tính chất đối xứng gương (đứng) và đối xứng mặt nước (ngang)",
            key_point="Để cả từ có trục đối xứng đứng: Từng chữ cái phải có trục đối xứng đứng VÀ từ đó phải đọc xuôi ngược như nhau (chữ đầu bằng chữ cuối). Để cả từ có trục đối xứng ngang: MỌI chữ cái trong từ đều phải có trục đối xứng ngang."
        ),
        "solution": """<p><strong>a) Xét các từ có trục đối xứng thẳng đứng:</strong></p>
<p>Điều kiện để cả từ có trục đối xứng thẳng đứng:</p>
<p>1. Từng chữ cái trong từ phải có trục đối xứng đứng.</p>
<p>2. Cụm chữ phải đối xứng từ hai đầu vào giữa (chữ đầu trùng chữ cuối khi lật).</p>
<p>• Xét $\\text{WOW}$: Các chữ $W, O, W$ đều có trục đứng, chữ $W$ đầu trùng chữ $W$ cuối $\\rightarrow$ <strong>Có trục đối xứng thẳng đứng</strong> đi qua tâm chữ $O$.</p>
<p>• Xét $\\text{AHA}$: Các chữ $A, H, A$ đều có trục đứng, hai chữ $A$ đối xứng qua $H$ $\\rightarrow$ <strong>Có trục đối xứng thẳng đứng</strong> đi qua tâm chữ $H$.</p>
<p>• Xét $\\text{TOOT}$: Các chữ $T, O, O, T$ đều có trục đứng, thứ tự chữ đối xứng $\\rightarrow$ <strong>Có trục đối xứng thẳng đứng</strong> đi qua khe giữa hai chữ $O$.</p>
<p><strong>b) Xét các từ có trục đối xứng nằm ngang:</strong></p>
<p>Điều kiện để cả từ có trục đối xứng nằm ngang: TẤT CẢ các chữ cái cấu thành phải có trục đối xứng nằm ngang.</p>
<p>• Xét $\\text{CHOICE}$: Các chữ $C, H, O, I, C, E$ đều có trục đối xứng nằm ngang $\\rightarrow$ Toàn bộ từ $\\text{CHOICE}$ <strong>có trục đối xứng nằm ngang</strong> chạy dọc suốt chiều dài của từ!</p>
<p>• Xét $\\text{BED}$: Các chữ $B, E, D$ đều có trục đối xứng nằm ngang $\\rightarrow$ Từ $\\text{BED}$ <strong>có trục đối xứng nằm ngang</strong>.</p>
<p><strong>c) Phân tích từ $\\text{NOON}$:'</strong></p>
<p>• Khi soi gương thẳng đứng, chữ $N$ bị lật ngược nét chéo thành chữ không đọc được. Khi soi mặt nước ngang, chữ $N$ cũng bị đảo ngược.</p>
<p>• Do đó, từ $\\text{NOON}$ <strong>KHÔNG CÓ trục đối xứng</strong> nào (cả đứng lẫn ngang).</p>
<p>• Tuy nhiên, nếu quay ngược từ $\\text{NOON}$ $180^\\circ$ (lộn ngược đầu đuôi), từ này vẫn đọc là $\\text{NOON}$. Đây là tính chất <em>đối xứng tâm</em>, không phải đối xứng trục.</p>
<p><strong>Kết luận:</strong> Các từ đối xứng đứng là $\\text{WOW, AHA, TOOT}$; từ đối xứng ngang là $\\text{CHOICE, BED}$; từ $\\text{NOON}$ không có trục đối xứng.</p>""",
        "pitfall": "Học sinh rất hay nhầm lẫn từ 'NOON' có trục đối xứng vì thấy đọc xuôi ngược đều là N-O-O-N. Nhưng trục đối xứng đòi hỏi lật hình (soi gương), trong khi chữ N lật gương bị đổi chiều nét chéo!",
        "extension": "Các từ đọc xuôi ngược như nhau gọi là từ Palindrome trong ngôn ngữ học. Chỉ những từ Palindrome cấu tạo hoàn toàn bởi các chữ cái đối xứng đứng mới có trục đối xứng hình học."
    })

    # --- BÀI 7 (SLIDE 8): Biển báo giao thông ---
    svg_7 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Biển a: Cấm đi ngược chiều (2 trục đối xứng) -->
  <g transform="translate(10, 20)">
    <circle cx="55" cy="60" r="45" fill="#dc2626"/>
    <rect x="25" y="50" width="60" height="20" fill="#ffffff" rx="2"/>
    <line x1="55" y1="10" x2="55" y2="110" stroke="#2563eb" stroke-width="1.8" stroke-dasharray="4,3"/>
    <line x1="5" y1="60" x2="105" y2="60" stroke="#2563eb" stroke-width="1.8" stroke-dasharray="4,3"/>
    <text x="25" y="130" font-size="12" font-weight="bold" fill="#0f172a">Hình a: Cấm ngược chiều</text>
    <text x="35" y="148" font-size="12" font-weight="bold" fill="#dc2626">(2 TRỤC: ĐỨNG & NGANG)</text>
  </g>

  <!-- Biển b: Hướng đi thẳng (1 trục đối xứng) -->
  <g transform="translate(130, 20)">
    <circle cx="55" cy="60" r="45" fill="#2563eb"/>
    <polygon points="55,25 72,50 62,50 62,90 48,90 48,50 38,50" fill="#ffffff"/>
    <line x1="55" y1="10" x2="55" y2="110" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <text x="20" y="130" font-size="12" font-weight="bold" fill="#0f172a">Hình b: Đi thẳng</text>
    <text x="35" y="148" font-size="12" font-weight="bold" fill="#2563eb">(1 TRỤC ĐỨNG DỌC)</text>
  </g>

  <!-- Biển c: Cấm người đi bộ (0 trục) -->
  <g transform="translate(245, 20)">
    <circle cx="55" cy="60" r="45" fill="#ffffff" stroke="#dc2626" stroke-width="8"/>
    <!-- Người đi bộ cách điệu -->
    <circle cx="58" cy="42" r="5" fill="#0f172a"/>
    <path d="M 58,48 L 52,65 L 42,72 M 52,65 L 62,75 L 62,88 M 55,54 L 46,62 M 55,54 L 66,58" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/>
    <!-- Vạch chéo đỏ cấm -->
    <line x1="25" y1="30" x2="85" y2="90" stroke="#dc2626" stroke-width="7"/>
    <text x="15" y="130" font-size="12" font-weight="bold" fill="#0f172a">Hình c: Cấm người đi bộ</text>
    <text x="30" y="148" font-size="12" font-weight="bold" fill="#64748b">(0 TRỤC ĐỐI XỨNG)</text>
  </g>

  <!-- Biển d: Giao nhau đường cùng cấp (1 trục) -->
  <g transform="translate(360, 20)">
    <polygon points="55,15 105,100 5,100" fill="#fef08a" stroke="#dc2626" stroke-width="6" stroke-linejoin="round"/>
    <!-- Dấu cộng đen chữ thập -->
    <rect x="49" y="45" width="12" height="36" fill="#0f172a"/>
    <rect x="37" y="57" width="36" height="12" fill="#0f172a"/>
    <line x1="55" y1="10" x2="55" y2="105" stroke="#2563eb" stroke-width="1.8" stroke-dasharray="4,3"/>
    <text x="10" y="130" font-size="12" font-weight="bold" fill="#0f172a">Hình d: Đường cùng cấp</text>
    <text x="35" y="148" font-size="12" font-weight="bold" fill="#b45309">(1 TRỤC ĐỨNG)</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 8, "pid": 7,
        "jump_label": "Slide 8: Bài 7 (Nhận diện trục đối xứng Biển báo giao thông)",
        "badge": "Dạng 2: Chữ cái & Biểu tượng",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_7,
        "debai": "Quan sát bốn biển báo giao thông trong hình vẽ (Hình a, Hình b, Hình c, Hình d):<br>a) Biển báo nào có <strong>nhiều hơn 1 trục đối xứng</strong>? Hãy chỉ rõ các trục đó.<br>b) Biển báo nào có đúng <strong>1 trục đối xứng</strong>?<br>c) Biển báo nào <strong>không có trục đối xứng</strong>? Vì sao dải băng chéo màu đỏ trên biển báo cấm thường làm mất tính đối xứng của hình?",
        "analysis": make_heuristic(
            target="Xác định số trục đối xứng của từng biển báo giao thông",
            intermediate="Kết hợp hình dạng viền ngoài và hình vẽ biểu tượng bên trong",
            premise="Hình đối xứng đòi hỏi cả hình viền lẫn biểu tượng bên trong đều phải chồng khít",
            key_point="Muốn biển báo có trục đối xứng thì trục đó phải đồng thời là trục đối xứng của hình viền ngoài VÀ của hình vẽ biểu hiện bên trong. Dải gạch chéo nghiêng làm mất tính đối xứng đứng và ngang."
        ),
        "solution": """<p><strong>a) Biển báo có nhiều hơn 1 trục đối xứng:</strong></p>
<p>Đó là <strong>Hình a: Biển cấm đi ngược chiều</strong>.</p>
<p>• Viền ngoài là hình tròn đỏ (vô số trục).</p>
<p>• Hình bên trong là thanh chữ nhật ngang màu trắng đặt chính giữa tâm (có 2 trục đối xứng: 1 đứng, 1 ngang).</p>
<p>Do đó, biển báo này có đúng <strong>2 trục đối xứng</strong>: 1 trục thẳng đứng và 1 trục nằm ngang đi qua tâm biển.</p>
<p><strong>b) Biển báo có đúng 1 trục đối xứng:</strong></p>
<p>• <strong>Hình b: Biển hiệu lệnh hướng đi thẳng:</strong> Mũi tên thẳng đứng đặt giữa hình tròn chỉ có <strong>1 trục đối xứng thẳng đứng</strong> đi dọc theo thân mũi tên.</p>
<p>• <strong>Hình d: Biển cảnh báo giao nhau tuyến đường cùng cấp:</strong> Khung viền là tam giác đều, dấu chữ thập ở giữa có 4 trục đối xứng; nhưng vì đặt trong khung tam giác đều có đỉnh hướng lên nên toàn bộ biển chỉ có đúng <strong>1 trục đối xứng thẳng đứng</strong> đi qua đỉnh tam giác.</p>
<p><strong>c) Biển báo không có trục đối xứng:</strong></p>
<p>Đó là <strong>Hình c: Biển cấm người đi bộ</strong>.</p>
<p><em>Giải thích:</em> Biểu tượng người đi bộ đang sải bước sang một bên (không đối xứng). Hơn nữa, dải băng chéo đỏ đi từ góc trên bên trái xuống góc dưới bên phải là một đường xiên đơn độc, khi gấp hình theo bất kỳ trục nào dải băng này cũng không thể chồng khít lên chính nó.</p>
<p><strong>Kết luận:</strong> Hình a có 2 trục; Hình b và Hình d có 1 trục; Hình c không có trục đối xứng.</p>""",
        "pitfall": "Học sinh hay nhìn vào khung viền tròn của Hình c rồi kết luận có vô số trục đối xứng mà quên xét hình vẽ người và vạch chéo đỏ bên trong!",
        "extension": "Hầu hết các biển báo chỉ dẫn và biển cấm cơ bản được thiết kế có trục đối xứng để tài xế có thể nhận diện tín hiệu từ xa trong tích tắc."
    })

    # --- BÀI 8 (SLIDE 9): Biểu tượng (Ngôi sao 5 cánh, Trái tim, Cỏ 4 lá) ---
    svg_8 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Ngôi sao 5 cánh (5 trục) -->
  <g transform="translate(10, 20)">
    <polygon points="75,20 90,62 135,62 98,90 112,132 75,106 38,132 52,90 15,62 60,62" fill="#fef08a" stroke="#ca8a04" stroke-width="2"/>
    <!-- 5 trục đối xứng đi qua 5 đỉnh -->
    <line x1="75" y1="10" x2="75" y2="140" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <line x1="15" y1="62" x2="130" y2="120" stroke="#ea580c" stroke-width="1.2" stroke-dasharray="3,2"/>
    <line x1="135" y1="62" x2="20" y2="120" stroke="#ea580c" stroke-width="1.2" stroke-dasharray="3,2"/>
    <text x="35" y="165" font-size="13" font-weight="bold" fill="#854d0e">Ngôi sao 5 cánh</text>
    <text x="45" y="183" font-size="12" font-weight="bold" fill="#dc2626">(5 TRỤC ĐỐI XỨNG)</text>
  </g>

  <!-- Hình trái tim (1 trục) -->
  <g transform="translate(170, 20)">
    <path d="M 75,45 C 75,25 45,15 25,35 C 5,55 25,95 75,130 C 125,95 145,55 125,35 C 105,15 75,25 75,45 Z" fill="#fee2e2" stroke="#dc2626" stroke-width="2.2"/>
    <line x1="75" y1="15" x2="75" y2="145" stroke="#2563eb" stroke-width="2" stroke-dasharray="5,3"/>
    <text x="40" y="165" font-size="13" font-weight="bold" fill="#b91c1c">Hình trái tim</text>
    <text x="40" y="183" font-size="12" font-weight="bold" fill="#2563eb">(1 TRỤC ĐỨNG DỌC)</text>
  </g>

  <!-- Cỏ bốn lá (4 trục) -->
  <g transform="translate(320, 20)">
    <circle cx="55" cy="55" r="22" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <circle cx="95" cy="55" r="22" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <circle cx="55" cy="95" r="22" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <circle cx="95" cy="95" r="22" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <circle cx="75" cy="75" r="8" fill="#15803d"/>
    <!-- 4 trục đối xứng -->
    <line x1="75" y1="15" x2="75" y2="135" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <line x1="15" y1="75" x2="135" y2="75" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,3"/>
    <line x1="30" y1="30" x2="120" y2="120" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="4,3"/>
    <line x1="30" y1="120" x2="120" y2="30" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="4,3"/>
    <text x="45" y="165" font-size="13" font-weight="bold" fill="#15803d">Cỏ bốn lá</text>
    <text x="45" y="183" font-size="12" font-weight="bold" fill="#dc2626">(4 TRỤC ĐỐI XỨNG)</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 9, "pid": 8,
        "jump_label": "Slide 9: Bài 8 (Biểu tượng: Ngôi sao, Trái tim & Cỏ 4 lá)",
        "badge": "Dạng 2: Chữ cái & Biểu tượng",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_8,
        "debai": "Quan sát ba biểu tượng quen thuộc trong cuộc sống:<br>1. Ngôi sao 5 cánh đều đặn.<br>2. Biểu tượng hình trái tim chuẩn.<br>3. Biểu tượng cỏ bốn lá cách điệu đối xứng.<br>a) Biểu tượng hình trái tim có bao nhiêu trục đối xứng? Trục đó nằm ở đâu?<br>b) Ngôi sao 5 cánh có bao nhiêu trục đối xứng? Các trục đó đi qua những điểm đặc biệt nào?<br>c) Biểu tượng cỏ bốn lá có bao nhiêu trục đối xứng?",
        "analysis": make_heuristic(
            target="Xác định số lượng trục đối xứng của các biểu tượng tự nhiên và văn hóa",
            intermediate="Đếm số tia đối xứng chia hình thành các phần giống hệt nhau",
            premise="Đặc điểm hình học của từng biểu tượng",
            key_point="Hình trái tim có 1 trục đối xứng dọc nối vết lõm trên và chóp nhọn dưới. Ngôi sao 5 cánh đều có 5 trục đi qua mỗi đỉnh và điểm lõm đối diện. Cỏ 4 lá có 4 trục (2 trục dọc-ngang và 2 trục chéo)."
        ),
        "solution": """<p><strong>a) Xét biểu tượng hình trái tim:</strong></p>
<p>Biểu tượng hình trái tim có đúng <strong>1 trục đối xứng</strong>.</p>
<p>Đó là đường thẳng thẳng đứng đi qua điểm lõm trên đỉnh của trái tim và chóp nhọn dưới đáy. Khi gấp đôi theo đường này, nửa bên trái và nửa bên phải chồng khít hoàn toàn lên nhau.</p>
<p><strong>b) Xét hình ngôi sao 5 cánh:</strong></p>
<p>Ngôi sao 5 cánh đều có đúng <strong>5 trục đối xứng</strong>.</p>
<p>Mỗi trục đối xứng là một đường thẳng đi qua một đỉnh của ngôi sao và đi qua đáy lõm nằm giữa hai cánh đối diện.</p>
<p><strong>c) Xét biểu tượng cỏ bốn lá:</strong></p>
<p>Biểu tượng cỏ bốn lá cách điệu cân đối có đúng <strong>4 trục đối xứng</strong>, gồm:</p>
<p>• 2 trục thẳng đứng và nằm ngang đi qua khe phân chia giữa các cặp lá đối diện.</p>
<p>• 2 trục nằm trên hai đường chéo đi qua tâm và chia đôi từng chiếc lá.</p>
<p><strong>Kết luận:</strong> Hình trái tim có 1 trục; ngôi sao 5 cánh có 5 trục; cỏ bốn lá có 4 trục đối xứng.</p>""",
        "pitfall": "Học sinh thường đếm thiếu trục của ngôi sao 5 cánh (chỉ đếm 1 trục đứng) hoặc nhầm cỏ bốn lá có vô số trục vì tưởng giống hình tròn.",
        "extension": "Số trục đối xứng thể hiện tính cân đối hài hòa cao trong nghệ thuật thị giác và sinh học tiến hóa (tính đối xứng tỏa tròn của hoa, sao biển)."
    })

    # =========================================================================
    # DẠNG 3: VẼ ĐIỂM, ĐOẠN THẲNG & HÌNH ĐỐI XỨNG TRÊN LƯỚI Ô VUÔNG
    # =========================================================================

    # --- BÀI 9 (SLIDE 10): Điểm & Đoạn thẳng trên lưới ô vuông ---
    svg_9 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Lưới ô vuông 14x7 ô, kích thước 30px mỗi ô -->
  <g transform="translate(30, 20)">
    <defs>
      <pattern id="grid9" width="30" height="30" patternUnits="userSpaceOnUse">
        <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#e2e8f0" stroke-width="1"/>
      </pattern>
    </defs>
    <rect width="420" height="210" fill="url(#grid9)" stroke="#94a3b8" stroke-width="1.5"/>
    
    <!-- Trục đối xứng d tại x = 210 (cột thứ 7) -->
    <line x1="210" y1="0" x2="210" y2="210" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,4"/>
    <text x="215" y="20" font-size="14" font-weight="bold" fill="#dc2626">d</text>

    <!-- Điểm A tại (90, 60) cách d là 120px = 4 ô -->
    <circle cx="90" cy="60" r="5" fill="#2563eb"/>
    <text x="75" y="55" font-size="14" font-weight="bold" fill="#2563eb">A</text>
    <!-- Điểm A' đối xứng tại (330, 60) cách d là 120px = 4 ô -->
    <circle cx="330" cy="60" r="5" fill="#dc2626"/>
    <text x="340" y="55" font-size="14" font-weight="bold" fill="#dc2626">A'</text>
    <line x1="90" y1="60" x2="330" y2="60" stroke="#dc2626" stroke-width="1.2" stroke-dasharray="3,3"/>

    <!-- Điểm B tại (150, 150) cách d là 60px = 2 ô -->
    <circle cx="150" cy="150" r="5" fill="#2563eb"/>
    <text x="135" y="145" font-size="14" font-weight="bold" fill="#2563eb">B</text>
    <!-- Điểm B' đối xứng tại (270, 150) cách d là 60px = 2 ô -->
    <circle cx="270" cy="150" r="5" fill="#dc2626"/>
    <text x="280" y="145" font-size="14" font-weight="bold" fill="#dc2626">B'</text>
    <line x1="150" y1="150" x2="270" y2="150" stroke="#dc2626" stroke-width="1.2" stroke-dasharray="3,3"/>

    <!-- Đoạn thẳng AB và đoạn thẳng A'B' -->
    <line x1="90" y1="60" x2="150" y2="150" stroke="#2563eb" stroke-width="2.5"/>
    <line x1="330" y1="60" x2="270" y2="150" stroke="#dc2626" stroke-width="2.5"/>
  </g>
</svg>"""

    slides.append({
        "slide_num": 10, "pid": 9, "is_example": True,
        "jump_label": "Slide 10: Bài 9 (Ví dụ mẫu: Điểm & Đoạn thẳng đối xứng)",
        "badge": "Dạng 3: Vẽ trên lưới ô vuông",
        "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
        "type": "problem_with_svg", "svg_code": svg_9,
        "debai": "Trên lưới ô vuông, cho đường thẳng $d$ đi dọc theo một đường lưới. Cho đoạn thẳng $AB$ nằm về phía bên trái đường thẳng $d$ như hình vẽ.<br>Biết điểm $A$ cách đường thẳng $d$ đúng $4$ ô vuông, điểm $B$ cách đường thẳng $d$ đúng $2$ ô vuông.<br>a) Nêu quy tắc xác định điểm $A'$ đối xứng với điểm $A$ qua trục $d$ trên lưới ô vuông.<br>b) Xác định vị trí các điểm $A'$ và $B'$ đối xứng với $A, B$ qua trục $d$.<br>c) Đoạn thẳng $A'B'$ có độ dài như thế nào so với đoạn thẳng $AB$?",
        "analysis": make_heuristic(
            target="Dựng điểm và đoạn thẳng đối xứng qua trục trên lưới ô vuông",
            intermediate="Kẻ đường vuông góc với trục d, đếm số ô vuông bằng nhau sang phía đối diện",
            premise="Định nghĩa: Trục d đi qua trung điểm và vuông góc với đoạn thẳng nối hai điểm đối xứng",
            key_point="Từ điểm A, đếm theo hàng ngang vuông góc với trục d bao nhiêu ô vuông thì từ trục d đếm tiếp theo hàng ngang sang phải bấy nhiêu ô vuông để chấm điểm A'. Đoạn thẳng A'B' luôn bằng đoạn thẳng AB."
        ),
        "solution": """<p><strong>a) Quy tắc xác định điểm đối xứng trên lưới ô vuông:</strong></p>
<p>• Từ điểm $A$, kẻ một đường thẳng nằm ngang (vuông góc với trục thẳng đứng $d$), cắt trục $d$ tại điểm $H$.</p>
<p>• Đếm khoảng cách từ $A$ đến $H$ trên lưới ô vuông (ở đây $AH = 4$ ô vuông).</p>
<p>• Kéo dài tia đối của tia $HA$ sang phía bên phải trục $d$ và lấy điểm $A'$ sao cho $HA' = AH = 4$ ô vuông.</p>
<p>Khi đó, đường thẳng $d$ đi qua trung điểm của đoạn thẳng $AA'$ và vuông góc với $AA'$, nghĩa là điểm $A'$ đối xứng với điểm $A$ qua đường thẳng $d$.</p>
<p><strong>b) Xác định các điểm đối xứng:</strong></p>
<p>• Điểm $A'$ nằm trên cùng hàng ngang với $A$, cách trục $d$ đúng $4$ ô vuông về phía bên phải.</p>
<p>• Điểm $B'$ nằm trên cùng hàng ngang với $B$, cách trục $d$ đúng $2$ ô vuông về phía bên phải.</p>
<p>Nối $A'$ với $B'$, ta được đoạn thẳng $A'B'$ đối xứng với đoạn thẳng $AB$ qua trục $d$.</p>
<p><strong>c) So sánh độ dài:</strong></p>
<p>Do phép đối xứng trục bảo toàn khoảng cách giữa hai điểm bất kỳ, nên độ dài đoạn thẳng $A'B'$ <strong>bằng đúng độ dài đoạn thẳng $AB$</strong> ($A'B' = AB$).</p>
<p><strong>Kết luận:</strong> Đoạn thẳng $A'B'$ đối xứng với $AB$ qua $d$ và $A'B' = AB$.</p>""",
        "pitfall": "Học sinh thường đếm chéo ô thay vì đếm vuông góc với trục d, dẫn đến điểm đối xứng bị lệch hàng.",
        "extension": "Quy tắc 'vuông góc và cách đều' là thuật toán nền tảng của đồ họa máy tính để thực hiện phép lật ảnh (Flip Horizontal/Vertical)."
    })

    # --- BÀI 10 (SLIDE 11): Tam giác đối xứng trên lưới ô vuông ---
    svg_10 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(30, 20)">
    <defs>
      <pattern id="grid10" width="30" height="30" patternUnits="userSpaceOnUse">
        <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#e2e8f0" stroke-width="1"/>
      </pattern>
    </defs>
    <rect width="420" height="210" fill="url(#grid10)" stroke="#94a3b8" stroke-width="1.5"/>
    <line x1="210" y1="0" x2="210" y2="210" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,4"/>
    <text x="215" y="20" font-size="14" font-weight="bold" fill="#dc2626">d</text>

    <!-- Tam giác ABC bên trái -->
    <polygon points="150,30 60,150 180,180" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5"/>
    <circle cx="150" cy="30" r="4.5" fill="#2563eb"/>
    <circle cx="60" cy="150" r="4.5" fill="#2563eb"/>
    <circle cx="180" cy="180" r="4.5" fill="#2563eb"/>
    <text x="140" y="25" font-size="13" font-weight="bold" fill="#2563eb">A</text>
    <text x="45" y="155" font-size="13" font-weight="bold" fill="#2563eb">B</text>
    <text x="165" y="195" font-size="13" font-weight="bold" fill="#2563eb">C</text>

    <!-- Tam giác A'B'C' đối xứng bên phải -->
    <polygon points="270,30 360,150 240,180" fill="#fef2f2" stroke="#dc2626" stroke-width="2.5"/>
    <circle cx="270" cy="30" r="4.5" fill="#dc2626"/>
    <circle cx="360" cy="150" r="4.5" fill="#dc2626"/>
    <circle cx="240" cy="180" r="4.5" fill="#dc2626"/>
    <text x="275" y="25" font-size="13" font-weight="bold" fill="#dc2626">A'</text>
    <text x="370" y="155" font-size="13" font-weight="bold" fill="#dc2626">B'</text>
    <text x="245" y="195" font-size="13" font-weight="bold" fill="#dc2626">C'</text>

    <!-- Đường gióng ngang -->
    <line x1="150" y1="30" x2="270" y2="30" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,3"/>
    <line x1="60" y1="150" x2="360" y2="150" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,3"/>
    <line x1="180" y1="180" x2="240" y2="180" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3,3"/>
  </g>
</svg>"""

    slides.append({
        "slide_num": 11, "pid": 10,
        "jump_label": "Slide 11: Bài 10 (Dựng tam giác đối xứng trên lưới ô vuông)",
        "badge": "Dạng 3: Vẽ trên lưới ô vuông",
        "level": 1, "level_text": "Mức 1: Thông hiểu — Rèn kỹ thuật giải",
        "type": "problem_with_svg", "svg_code": svg_10,
        "debai": "Cho tam giác $ABC$ trên lưới ô vuông như hình vẽ. Trục đối xứng $d$ là đường kẻ dọc của lưới.<br>a) Đếm khoảng cách từ từng đỉnh $A, B, C$ đến trục $d$.<br>b) Xác định vị trí 3 đỉnh $A', B', C'$ đối xứng với $A, B, C$ qua trục $d$ và vẽ tam giác $A'B'C'$.<br>c) Hãy so sánh diện tích của hai tam giác $ABC$ và $A'B'C'$.",
        "analysis": make_heuristic(
            target="Dựng toàn bộ hình tam giác đối xứng qua trục",
            intermediate="Dựng từng đỉnh đối xứng rồi nối các đỉnh lại với nhau",
            premise="Định nghĩa phép đối xứng trục bảo toàn hình dạng và kích thước",
            key_point="Để vẽ một đa giác đối xứng qua trục, ta chỉ cần tìm các điểm đối xứng của từng đỉnh rồi nối chúng lại theo đúng thứ tự. Tam giác ảnh bằng đúng tam giác gốc cả về cạnh, góc và diện tích."
        ),
        "solution": """<p><strong>a) Khoảng cách từ các đỉnh đến trục đối xứng $d$:</strong></p>
<p>• Đỉnh $A$ cách trục $d$ là $2$ ô vuông về phía bên trái.</p>
<p>• Đỉnh $B$ cách trục $d$ là $5$ ô vuông về phía bên trái.</p>
<p>• Đỉnh $C$ cách trục $d$ là $1$ ô vuông về phía bên trái.</p>
<p><strong>b) Xác định 3 đỉnh đối xứng $A', B', C'$:</strong></p>
<p>• Lấy điểm $A'$ trên cùng hàng ngang với $A$, cách trục $d$ đúng $2$ ô vuông về phía bên phải.</p>
<p>• Lấy điểm $B'$ trên cùng hàng ngang với $B$, cách trục $d$ đúng $5$ ô vuông về phía bên phải.</p>
<p>• Lấy điểm $C'$ trên cùng hàng ngang với $C$, cách trục $d$ đúng $1$ ô vuông về phía bên phải.</p>
<p>Nối $A'$ với $B'$, $B'$ với $C'$, $C'$ với $A'$, ta được tam giác $A'B'C'$ đối xứng với tam giác $ABC$ qua trục $d$.</p>
<p><strong>c) So sánh diện tích:</strong></p>
<p>Do phép đối xứng trục biến tam giác $ABC$ thành tam giác $A'B'C'$ bằng nó ($AB = A'B', BC = B'C', CA = C'A'$), nên diện tích hai tam giác này bằng nhau:</p>
<p>$$S_{A'B'C'} = S_{ABC}$$</p>
<p><strong>Kết luận:</strong> Hai tam giác đối xứng qua trục có hình dạng và diện tích hoàn toàn bằng nhau.</p>""",
        "pitfall": "Học sinh nối nhầm thứ tự các đỉnh (ví dụ nối A' với C' thành đường chéo sai lệch) làm biến dạng tam giác.",
        "extension": "Nguyên lý 'dựng từng điểm chốt' này được mở rộng cho mọi hình đa giác phức tạp (tứ giác, ngũ giác, hoa văn trang trí)."
    })

    # --- BÀI 11 (SLIDE 12): Hoàn thiện hình con bướm ---
    svg_11 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(30, 20)">
    <defs>
      <pattern id="grid11" width="30" height="30" patternUnits="userSpaceOnUse">
        <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#e2e8f0" stroke-width="1"/>
      </pattern>
    </defs>
    <rect width="420" height="210" fill="url(#grid11)" stroke="#94a3b8" stroke-width="1.5"/>
    <line x1="210" y1="0" x2="210" y2="210" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,4"/>
    <text x="215" y="20" font-size="14" font-weight="bold" fill="#dc2626">d</text>

    <!-- Nửa cánh bướm bên trái (gốc) -->
    <path d="M 210,30 Q 120,20 90,60 T 120,120 Q 90,150 120,180 T 210,180 Z" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5"/>
    <circle cx="210" cy="30" r="4" fill="#0f172a"/>
    <circle cx="210" cy="180" r="4" fill="#0f172a"/>
    <text x="120" y="80" font-size="13" font-weight="bold" fill="#2563eb">Nửa bên trái (đã cho)</text>

    <!-- Nửa cánh bướm đối xứng bên phải -->
    <path d="M 210,30 Q 300,20 330,60 T 300,120 Q 330,150 300,180 T 210,180 Z" fill="#fef2f2" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="5,3"/>
    <text x="240" y="80" font-size="13" font-weight="bold" fill="#dc2626">Nửa cần vẽ hoàn thiện</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 12, "pid": 11,
        "jump_label": "Slide 12: Bài 11 (Hoàn thiện hình con bướm đối xứng)",
        "badge": "Dạng 3: Vẽ trên lưới ô vuông",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_11,
        "debai": "Hình vẽ cho biết một nửa cánh bướm bên trái trục đối xứng $d$ trên lưới kẻ ô vuông.<br>a) Hai điểm đầu và đuôi của thân con bướm có vị trí đặc biệt gì đối với trục $d$?<br>b) Hãy chọn 4 điểm mấu chốt trên đường viền cánh bướm bên trái, nêu cách lấy 4 điểm đối xứng tương ứng sang bên phải trục $d$.<br>c) Vẽ tiếp nửa bên phải để được một hình con bướm hoàn chỉnh nhận đường thẳng $d$ làm trục đối xứng.",
        "analysis": make_heuristic(
            target="Hoàn thiện hình vẽ tự nhiên có trục đối xứng trên giấy kẻ ô",
            intermediate="Xác định các điểm mấu chốt (điểm uốn, điểm nhọn) rồi lấy đối xứng",
            premise="Các điểm nằm ngay trên trục d có điểm đối xứng là chính nó",
            key_point="Hai điểm nằm trên trục d giữ nguyên. Với các đường cong phức tạp, ta chấm các điểm mấu chốt (đỉnh cánh trên, hõm cánh giữa, đỉnh cánh dưới), lấy đối xứng các điểm đó rồi vẽ đường cong mềm mại nối qua chúng."
        ),
        "solution": """<p><strong>a) Vị trí hai điểm đầu và đuôi con bướm:</strong></p>
<p>Hai điểm đầu và đuôi nằm <strong>trực tiếp trên trục đối xứng $d$</strong>.</p>
<p>Do đó, điểm đối xứng của chúng qua trục $d$ là chính nó, không cần phải dịch chuyển.</p>
<p><strong>b) Xác định 4 điểm mấu chốt trên cánh bướm:</strong></p>
<p>1. <em>Đỉnh nhọn cánh trên:</em> Cách trục $d$ là $4$ ô về bên trái $\\rightarrow$ Lấy điểm đối xứng cách $d$ đúng $4$ ô về bên phải.</p>
<p>2. <em>Điểm uốn mép ngoài:</em> Cách trục $d$ là $3$ ô về bên trái $\\rightarrow$ Lấy điểm đối xứng cách $d$ đúng $3$ ô về bên phải.</p>
<p>3. <em>Điểm hõm giữa hai cánh:</em> Cách trục $d$ là $2$ ô về bên trái $\\rightarrow$ Lấy điểm đối xứng cách $d$ đúng $2$ ô về bên phải.</p>
<p>4. <em>Đỉnh nhọn cánh dưới:</em> Cách trục $d$ là $3$ ô về bên trái $\\rightarrow$ Lấy điểm đối xứng cách $d$ đúng $3$ ô về bên phải.</p>
<p><strong>c) Vẽ hoàn thiện hình:</strong></p>
<p>Nối các điểm vừa xác định bằng đường lượn mềm mại sao cho đối xứng với nửa bên trái, ta thu được hình con bướm cân đối hoàn hảo.</p>
<p><strong>Kết luận:</strong> Hình sau khi vẽ nhận đường thẳng $d$ làm trục đối xứng.</p>""",
        "pitfall": "Học sinh thường vẽ ước lượng bằng mắt mà không đếm số ô của các điểm mấu chốt, khiến cánh bướm bên to bên nhỏ không cân xứng.",
        "extension": "Đây là bài toán thực hành chuẩn trong SGK Kết nối tri thức (HĐ1 trang 99) rèn luyện năng lực thẩm mỹ và tư duy hình học trực quan."
    })

    # --- BÀI 12 (SLIDE 13): Hoàn thiện hình mũi tên qua trục ngang ---
    svg_12 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(30, 20)">
    <defs>
      <pattern id="grid12" width="30" height="30" patternUnits="userSpaceOnUse">
        <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#e2e8f0" stroke-width="1"/>
      </pattern>
    </defs>
    <rect width="420" height="210" fill="url(#grid12)" stroke="#94a3b8" stroke-width="1.5"/>
    <line x1="0" y1="105" x2="420" y2="105" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="6,4"/>
    <text x="400" y="100" font-size="14" font-weight="bold" fill="#dc2626">d</text>

    <!-- Nửa trên của mũi tên hướng sang phải -->
    <polygon points="60,105 60,60 240,60 240,30 360,105" fill="#dcfce7" stroke="#16a34a" stroke-width="2.5"/>
    <text x="140" y="85" font-size="13" font-weight="bold" fill="#15803d">Nửa trên đã cho</text>

    <!-- Nửa dưới cần vẽ hoàn thiện -->
    <polygon points="60,105 60,150 240,150 240,180 360,105" fill="#fef2f2" stroke="#dc2626" stroke-width="2" stroke-dasharray="5,3"/>
    <text x="140" y="140" font-size="13" font-weight="bold" fill="#dc2626">Nửa dưới cần vẽ</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 13, "pid": 12,
        "jump_label": "Slide 13: Bài 12 (Hoàn thiện mũi tên đối xứng qua trục ngang)",
        "badge": "Dạng 3: Vẽ trên lưới ô vuông",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_12,
        "debai": "Trên giấy kẻ ô vuông, cho trục đối xứng $d$ là một đường nằm ngang. Nửa phía trên của một hình mũi tên chỉ hướng được cho như hình vẽ.<br>a) Đỉnh nhọn của mũi tên nằm ở đâu so với trục $d$?<br>b) Hãy xác định các điểm đối xứng qua trục ngang $d$ của thân mũi tên và cánh mũi tên.<br>c) Hoàn thiện hình vẽ mũi tên bên dưới trục $d$. Hình hoàn chỉnh có phải là hình có trục đối xứng không?",
        "analysis": make_heuristic(
            target="Vẽ hình đối xứng qua trục nằm ngang",
            intermediate="Đếm số ô vuông theo phương thẳng đứng (vuông góc với trục ngang d)",
            premise="Khoảng cách từ điểm phía trên đến trục ngang bằng khoảng cách từ trục đến điểm phía dưới",
            key_point="Khi trục đối xứng nằm ngang, ta đếm số ô theo chiều thẳng đứng từ trên xuống dưới. Điểm thuộc trục ngang giữ nguyên vị trí."
        ),
        "solution": """<p><strong>a) Vị trí đỉnh nhọn của mũi tên:</strong></p>
<p>Đỉnh nhọn ngoài cùng của mũi tên nằm <strong>ngay trên trục đối xứng nằm ngang $d$</strong>.</p>
<p>Do đó, đỉnh nhọn này là điểm chung của cả nửa trên và nửa dưới mũi tên.</p>
<p><strong>b) Xác định các điểm đối xứng qua trục ngang $d$:</strong></p>
<p>• Điểm đuôi mũi tên phía trên cách trục $d$ là $1.5$ ô vuông hướng lên $\\rightarrow$ Lấy điểm đối xứng cách $d$ đúng $1.5$ ô vuông hướng xuống.</p>
<p>• Điểm gãy ở cổ mũi tên cách trục $d$ là $1.5$ ô vuông hướng lên $\\rightarrow$ Lấy điểm đối xứng tương ứng ở phía dưới.</p>
<p>• Đỉnh cánh mở rộng của mũi tên cách trục $d$ là $2.5$ ô vuông hướng lên $\\rightarrow$ Lấy điểm đối xứng cách $d$ đúng $2.5$ ô vuông hướng xuống.</p>
<p><strong>c) Hoàn thiện hình vẽ:</strong></p>
<p>Nối các điểm phía dưới theo đúng thứ tự tương ứng với nửa phía trên, ta thu được một mũi tên hoàn chỉnh chỉ sang bên phải.</p>
<p>Hình hoàn chỉnh nhận đường thẳng $d$ làm trục đối xứng duy nhất.</p>
<p><strong>Kết luận:</strong> Đã hoàn thiện hình mũi tên đối xứng chuẩn xác qua trục ngang.</p>""",
        "pitfall": "Học sinh quen đếm ô ngang khi gặp trục dọc, đến khi gặp trục ngang thì vẫn đếm ngang thay vì đếm dọc vuông góc với trục!",
        "extension": "Biển báo giao thông chỉ hướng rẽ hoặc lối thoát hiểm luôn dùng các mũi tên có trục đối xứng nằm ngang như thế này."
    })

    # =========================================================================
    # DẠNG 4: GẤP GIẤY, CẮT HÌNH & BÀI TOÁN THỰC TẾ
    # =========================================================================

    # --- BÀI 13 (SLIDE 14): Gấp giấy cắt chữ cái ---
    svg_13 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Bước 1: Mảnh giấy chữ nhật và nếp gấp đôi -->
  <g transform="translate(15, 20)">
    <rect x="10" y="20" width="90" height="130" fill="#f8fafc" stroke="#64748b" stroke-width="1.8"/>
    <line x1="55" y1="10" x2="55" y2="160" stroke="#dc2626" stroke-width="2" stroke-dasharray="5,3"/>
    <text x="25" y="175" font-size="12" font-weight="bold" fill="#0f172a">Bước 1: Gấp đôi</text>
  </g>

  <!-- Bước 2: Tờ giấy đã gấp và vẽ nửa nét chữ A -->
  <g transform="translate(130, 20)">
    <rect x="15" y="20" width="55" height="130" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
    <line x1="15" y1="10" x2="15" y2="160" stroke="#dc2626" stroke-width="3"/>
    <path d="M 15,30 L 55,140 L 40,140 L 32,110 L 15,110 Z" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <path d="M 15,55 L 25,95 L 15,95 Z" fill="#ffffff" stroke="#dc2626" stroke-width="1.2"/>
    <text x="10" y="175" font-size="12" font-weight="bold" fill="#0f172a">Bước 2: Vẽ nửa nét</text>
    <text x="5" y="192" font-size="11" font-weight="bold" fill="#dc2626">(Mép gấp là trục)</text>
  </g>

  <!-- Bước 3: Mở ra thành chữ A hoàn chỉnh -->
  <g transform="translate(260, 20)">
    <polygon points="100,25 40,150 70,150 82,120 118,120 130,150 160,150" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2.5"/>
    <polygon points="100,55 88,95 112,95" fill="#ffffff" stroke="#1d4ed8" stroke-width="2"/>
    <line x1="100" y1="15" x2="100" y2="165" stroke="#dc2626" stroke-width="2" stroke-dasharray="5,3"/>
    <text x="45" y="175" font-size="12" font-weight="bold" fill="#1d4ed8">Bước 3: Mở ra chữ A</text>
    <text x="50" y="192" font-size="11" font-weight="bold" fill="#dc2626">(Trục đối xứng d)</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 14, "pid": 13, "is_example": True,
        "jump_label": "Slide 14: Bài 13 (Ví dụ mẫu: Gấp giấy cắt chữ cái A, H)",
        "badge": "Dạng 4: Gấp giấy & Thực tế",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_13,
        "debai": "Để cắt chữ cái in hoa bằng giấy thủ công theo phương pháp gấp giấy:<br>a) Vì sao ta chỉ cần vẽ một nửa chữ cái lên tờ giấy đã gấp đôi mà khi mở ra vẫn được chữ cái hoàn chỉnh?<br>b) Khi gấp đôi tờ giấy để cắt chữ $\\text{A}$, mép gấp của tờ giấy phải trùng với yếu tố nào của chữ $\\text{A}$?<br>c) Em hãy nêu các bước gấp giấy và cắt để tạo thành chữ $\\text{H}$ và hình trái tim.",
        "analysis": make_heuristic(
            target="Giải thích nguyên lý và quy trình gấp giấy cắt hình có trục đối xứng",
            intermediate="Nếp gấp đóng vai trò là trục đối xứng của hình",
            premise="Định nghĩa hai phần chồng khít khi gấp theo trục",
            key_point="Nếp gấp chính là trục đối xứng. Do đó vẽ và cắt một bên thì nửa bên kia tự động được sao chép chuẩn xác khi mở giấy ra. Mép gấp phải là trục đối xứng của chữ cái."
        ),
        "solution": """<p><strong>a) Giải thích nguyên lý:</strong></p>
<p>Chữ cái in hoa $\\text{A}$ là một hình có trục đối xứng thẳng đứng.</p>
<p>Khi gấp đôi tờ giấy, nếp gấp đóng vai trò là <strong>trục đối xứng</strong>. Nếu ta vẽ và cắt theo đường nét của một nửa chữ cái, đường kéo cắt sẽ xuyên qua đồng thời cả hai lớp giấy.</p>
<p>Khi mở tờ giấy ra, hai nửa hình liên kết với nhau qua nếp gấp và hoàn toàn đối xứng, tạo thành chữ cái hoàn chỉnh.</p>
<p><strong>b) Yêu cầu đối với mép gấp khi cắt chữ $\\text{A}$:</strong></p>
<p>Mép gấp của tờ giấy bắt buộc phải <strong>trùng với trục đối xứng thẳng đứng của chữ $\\text{A}$</strong> (đường đi qua đỉnh nhọn trên cùng và chính giữa thanh ngang).</p>
<p><em>Nếu vẽ lộn ngược mép gấp sang phía cạnh ngoài thì khi cắt xong mở ra, chữ sẽ bị đứt đôi thành hai mảnh rời nhau!</em></p>
<p><strong>c) Các bước gấp cắt chữ $\\text{H}$ và hình trái tim:</strong></p>
<p>• <em>Cắt chữ $\\text{H}$ (có 2 trục đối xứng):</em> Ta có thể gấp đôi tờ giấy theo chiều dọc, sau đó gấp đôi tiếp theo chiều ngang (gấp tư). Vẽ một góc của chữ $\\text{H}$ rồi cắt bỏ phần khuyết, mở ra ta được chữ $\\text{H}$ hoàn hảo.</p>
<p>• <em>Cắt hình trái tim:</em> Gấp đôi tờ giấy theo chiều dọc. Vẽ nửa hình trái tim tựa lưng vào mép gấp (chỗ nếp gấp là đường nối đỉnh lõm và chóp nhọn). Cắt theo đường vẽ và mở ra.</p>
<p><strong>Kết luận:</strong> Phương pháp gấp giấy cắt hình dựa trên tính chất bảo toàn hình học của trục đối xứng.</p>""",
        "pitfall": "Học sinh rất hay cắt nhầm vào mép gấp (cắt đứt trục đối xứng), khiến hình bị rách làm hai nửa rời rạc.",
        "extension": "Nghệ thuật cắt giấy Kirigami của Nhật Bản và cắt chữ trang trí khẩu hiệu của Việt Nam đều vận dụng triệt để nguyên lý trục đối xứng."
    })

    # --- BÀI 14 (SLIDE 15): Gấp giấy hình chữ nhật & so sánh 3 nếp gấp ---
    svg_14 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Gấp dọc: Chồng khít -->
  <g transform="translate(15, 20)">
    <rect x="10" y="20" width="120" height="80" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
    <line x1="70" y1="10" x2="70" y2="110" stroke="#16a34a" stroke-width="2.5" stroke-dasharray="5,3"/>
    <text x="15" y="130" font-size="12" font-weight="bold" fill="#0f172a">1. Gấp dọc (Trục d₁)</text>
    <text x="25" y="148" font-size="12" font-weight="bold" fill="#16a34a">✔ CHỒNG KHÍT</text>
  </g>

  <!-- Gấp ngang: Chồng khít -->
  <g transform="translate(160, 20)">
    <rect x="10" y="20" width="120" height="80" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
    <line x1="0" y1="60" x2="140" y2="60" stroke="#16a34a" stroke-width="2.5" stroke-dasharray="5,3"/>
    <text x="15" y="130" font-size="12" font-weight="bold" fill="#0f172a">2. Gấp ngang (Trục d₂)</text>
    <text x="25" y="148" font-size="12" font-weight="bold" fill="#16a34a">✔ CHỒNG KHÍT</text>
  </g>

  <!-- Gấp theo đường chéo: Bị lệch, không chồng khít -->
  <g transform="translate(305, 20)">
    <polygon points="10,20 130,20 130,100" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
    <line x1="10" y1="20" x2="130" y2="100" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,3"/>
    <polygon points="10,20 130,100 50,140" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
    <text x="15" y="165" font-size="12" font-weight="bold" fill="#0f172a">3. Gấp theo đường chéo</text>
    <text x="20" y="183" font-size="12" font-weight="bold" fill="#dc2626">✘ LỆCH, KHÔNG KHÍT!</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 15, "pid": 14,
        "jump_label": "Slide 15: Bài 14 (Thực nghiệm 3 nếp gấp tờ giấy hình chữ nhật)",
        "badge": "Dạng 4: Gấp giấy & Thực tế",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_14,
        "debai": "Cho một tờ giấy hình chữ nhật có kích thước $12\\text{ cm} \\times 8\\text{ cm}$. Ta thực hiện 3 nếp gấp khác nhau:<br>• Nếp gấp 1: Gấp đôi tờ giấy theo chiều dọc nối trung điểm hai cạnh dài.<br>• Nếp gấp 2: Gấp đôi tờ giấy theo chiều ngang nối trung điểm hai cạnh ngắn.<br>• Nếp gấp 3: Gấp tờ giấy theo đường chéo.<br>a) Trong 3 nếp gấp trên, những nếp gấp nào làm cho hai phần của tờ giấy chồng khít hoàn toàn lên nhau?<br>b) Tại sao khi gấp theo đường chéo, hai nửa tam giác dù có diện tích bằng nhau nhưng lại không chồng khít lên nhau?<br>c) Cần thay đổi kích thước tờ giấy như thế nào để nếp gấp theo đường chéo cũng làm hai phần chồng khít lên nhau?",
        "analysis": make_heuristic(
            target="Chứng minh điều kiện chồng khít của phép gấp giấy và bản chất trục đối xứng",
            intermediate="Phân biệt diện tích bằng nhau và chồng khít hình học",
            premise="Định nghĩa hình có trục đối xứng: Mọi điểm phải gập trùng khít tương ứng",
            key_point="Hai hình có cùng diện tích chưa chắc chồng khít khi gấp theo đường biên chung. Đường chéo hình chữ nhật chia đôi diện tích nhưng KHÔNG chia đôi theo phép đối xứng trục trừ khi hình chữ nhật đó là hình vuông (chiều dài bằng chiều rộng)."
        ),
        "solution": """<p><strong>a) Nếp gấp làm hai phần chồng khít hoàn toàn:</strong></p>
<p>Đó là <strong>Nếp gấp 1</strong> (gấp dọc) và <strong>Nếp gấp 2</strong> (gấp ngang).</p>
<p>Hai nếp gấp này chính là 2 trục đối xứng của hình chữ nhật.</p>
<p><strong>b) Giải thích vì sao nếp gấp đường chéo không chồng khít:</strong></p>
<p>Đường chéo chia hình chữ nhật thành hai tam giác vuông có diện tích bằng nhau.</p>
<p>Tuy nhiên, phép đối xứng trục qua đường chéo $AC$ sẽ biến cạnh $AB$ (dài $12\\text{ cm}$) thành một đoạn thẳng vuông góc với cạnh $AD$ (dài $8\\text{ cm}$). Do $12\\text{ cm} \\neq 8\\text{ cm}$ nên đỉnh $B$ gập sang không thể trùng với đỉnh $D$, mép giấy bị chìa ra ngoài như hình vẽ.</p>
<p>Do đó, hai phần không chồng khít lên nhau.</p>
<p><strong>c) Điều kiện để nếp gấp đường chéo chồng khít:</strong></p>
<p>Để nếp gấp theo đường chéo làm hai phần chồng khít, chiều dài phải bằng chiều rộng:</p>
<p>$$\\text{Chiều dài} = \\text{Chiều rộng} = 8\\text{ cm} \\text{ (hoặc } 12\\text{ cm)}$$</p>
<p>Khi đó tờ giấy trở thành <strong>hình vuông</strong>. Lúc này đường chéo vừa là đường phân giác, góc vuông bị chia đôi thành hai góc $45^\\circ$ nên khi gấp lại hai cạnh kề sẽ chồng khít hoàn toàn lên nhau.</p>
<p><strong>Kết luận:</strong> Chỉ có nếp gấp dọc và ngang là trục đối xứng của hình chữ nhật; đường chéo chỉ là trục đối xứng khi hình chữ nhật là hình vuông.</p>""",
        "pitfall": "Học sinh hay lý luận: 'Hai tam giác tạo bởi đường chéo có diện tích bằng nhau nên chúng phải chồng khít khi gấp'. Đây là sự nhầm lẫn giữa khái niệm 'bằng nhau về diện tích' và 'chồng khít theo phép đối xứng trục'.",
        "extension": "Bài toán giúp học sinh phân biệt sâu sắc giữa Phép đối xứng trục (phép lật gương) và Phép đối xứng tâm (phép quay $180^\\circ$)."
    })

    # --- BÀI 15 (SLIDE 16): Tổ hợp tô màu ô vuông bảng 4x4 ---
    svg_15 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(60, 20)">
    <rect x="0" y="0" width="180" height="180" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
    <line x1="45" y1="0" x2="45" y2="180" stroke="#cbd5e1" stroke-width="1.5"/>
    <line x1="90" y1="0" x2="90" y2="180" stroke="#dc2626" stroke-width="2.5" stroke-dasharray="5,3"/>
    <line x1="135" y1="0" x2="135" y2="180" stroke="#cbd5e1" stroke-width="1.5"/>
    <line x1="0" y1="45" x2="180" y2="45" stroke="#cbd5e1" stroke-width="1.5"/>
    <line x1="0" y1="90" x2="180" y2="90" stroke="#cbd5e1" stroke-width="1.5"/>
    <line x1="0" y1="135" x2="180" y2="135" stroke="#cbd5e1" stroke-width="1.5"/>
    
    <!-- 3 ô xanh ban đầu -->
    <rect x="0" y="0" width="45" height="45" fill="#2563eb"/>
    <rect x="45" y="45" width="45" height="45" fill="#2563eb"/>
    <rect x="0" y="90" width="45" height="45" fill="#2563eb"/>

    <!-- Các ô cần tô thêm -->
    <rect x="135" y="0" width="45" height="45" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
    <text x="150" y="28" font-size="16" font-weight="bold" fill="#dc2626">?</text>
    <rect x="90" y="45" width="45" height="45" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
    <text x="105" y="73" font-size="16" font-weight="bold" fill="#dc2626">?</text>
    <rect x="135" y="90" width="45" height="45" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
    <text x="150" y="118" font-size="16" font-weight="bold" fill="#dc2626">?</text>
    <text x="95" y="195" font-size="13" font-weight="bold" fill="#dc2626">Trục d</text>
  </g>

  <g transform="translate(280, 40)">
    <rect x="0" y="0" width="180" height="150" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#0f172a">QUY ƯỚC BẢNG:</text>
    <rect x="15" y="40" width="18" height="18" fill="#2563eb"/>
    <text x="40" y="55" font-size="12" fill="#334155">: 3 ô đã tô ban đầu</text>
    <rect x="15" y="70" width="18" height="18" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <text x="40" y="85" font-size="12" fill="#dc2626">: Ô cần tô thêm</text>
    <text x="15" y="115" font-size="12" font-style="italic" fill="#64748b">• Trục d chia đôi bảng</text>
    <text x="15" y="133" font-size="12" font-style="italic" fill="#64748b">• Yêu cầu: Số ô ít nhất</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 16, "pid": 15,
        "jump_label": "Slide 16: Bài 15 (Tô thêm ô vuông ít nhất để tạo trục đối xứng)",
        "badge": "Dạng 4: Gấp giấy & Thực tế",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_15,
        "debai": "Cho một bảng ô vuông kích thước $4 \\times 4$ gồm 16 ô vuông nhỏ. Hiện tại đã có 3 ô vuông được tô màu xanh như hình vẽ (tại vị trí hàng 1 cột 1, hàng 2 cột 2, và hàng 3 cột 1).<br>a) Cần tô thêm <strong>ít nhất bao nhiêu ô vuông nữa</strong> để hình nhận đường thẳng $d$ (đường kẻ dọc chia đôi bảng thành hai nửa $2 \\times 4$) làm trục đối xứng?<br>b) Hãy chỉ rõ vị trí (hàng, cột) của các ô vuông cần tô thêm đó.<br>c) Nếu chọn trục đối xứng là đường chéo chính từ góc trên bên trái xuống góc dưới bên phải của bảng, thì cần tô thêm ít nhất bao nhiêu ô vuông?",
        "analysis": make_heuristic(
            target="Tìm số ô vuông tối thiểu cần tô thêm để bảng có trục đối xứng",
            intermediate="Xác định ô đối xứng của từng ô đã tô qua trục quy định",
            premise="Mỗi ô đã tô mà ô đối xứng chưa tô thì bắt buộc phải tô thêm ô đối xứng đó",
            key_point="Để đối xứng qua trục d: Mỗi ô ở cột 1 đối xứng với ô cùng hàng ở cột 4. Mỗi ô ở cột 2 đối xứng với ô cùng hàng ở cột 3. Đếm số ô đối xứng chưa được tô."
        ),
        "solution": """<p><strong>a) & b) Xét trục đối xứng thẳng đứng $d$ chia đôi bảng:</strong></p>
<p>Trục $d$ nằm giữa cột 2 và cột 3. Ta tìm các ô đối xứng với 3 ô màu xanh đã tô:</p>
<p>1. Ô tại <em>hàng 1, cột 1</em> cách trục $d$ là $2$ ô về bên trái $\\rightarrow$ Ô đối xứng tương ứng là ô tại <strong>hàng 1, cột 4</strong>.</p>
<p>2. Ô tại <em>hàng 2, cột 2</em> cách trục $d$ là $1$ ô về bên trái $\\rightarrow$ Ô đối xứng tương ứng là ô tại <strong>hàng 2, cột 3</strong>.</p>
<p>3. Ô tại <em>hàng 3, cột 1</em> cách trục $d$ là $2$ ô về bên trái $\\rightarrow$ Ô đối xứng tương ứng là ô tại <strong>hàng 3, cột 4</strong>.</p>
<p>Cả 3 ô đối xứng này hiện đều chưa được tô màu.</p>
<p>Do đó, cần tô thêm ít nhất <strong>3 ô vuông nữa</strong> tại các vị trí: (hàng 1, cột 4), (hàng 2, cột 3), (hàng 3, cột 4).</p>
<p><strong>c) Xét trục đối xứng là đường chéo chính:</strong></p>
<p>Đường chéo chính đi qua các ô: (hàng 1, cột 1), (hàng 2, cột 2), (hàng 3, cột 3), (hàng 4, cột 4).</p>
<p>• Hai ô (hàng 1, cột 1) và (hàng 2, cột 2) nằm ngay trên đường chéo chính nên chúng tự đối xứng với chính mình!</p>
<p>• Ô tại (hàng 3, cột 1) nằm lệch khỏi đường chéo chính $\\rightarrow$ Ô đối xứng với nó qua đường chéo chính là ô tại <strong>hàng 1, cột 3</strong>.</p>
<p>Như vậy, trong trường hợp này ta chỉ cần tô thêm đúng <strong>1 ô vuông duy nhất</strong> tại vị trí (hàng 1, cột 3)!</p>
<p><strong>Kết luận:</strong> Đối xứng qua trục dọc cần tô thêm 3 ô; đối xứng qua đường chéo chỉ cần tô thêm 1 ô.</p>""",
        "pitfall": "Học sinh thường đếm cả các ô nằm trên trục đối xứng cần tô thêm, hoặc nhầm vị trí đối xứng qua đường chéo (nhầm thành hàng 3 cột 4 thay vì hàng 1 cột 3).",
        "extension": "Dạng toán tô màu đối xứng thường xuyên xuất hiện trong các bài toán tư duy tổ hợp và đề thi học sinh giỏi THCS cấp trường."
    })

    # --- BÀI 16 (SLIDE 17): Quốc kỳ Việt Nam ---
    svg_16 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(40, 20)">
    <rect x="0" y="10" width="240" height="160" fill="#da251d" stroke="#b91c1c" stroke-width="2"/>
    <polygon points="120,40 129,68 158,68 135,86 144,114 120,97 96,114 105,86 82,68 111,68" fill="#ffff00"/>
    <line x1="120" y1="0" x2="120" y2="180" stroke="#ffffff" stroke-width="2.5" stroke-dasharray="6,4"/>
    <text x="125" y="25" font-size="13" font-weight="bold" fill="#ffffff">Trục đứng d</text>
    <line x1="-10" y1="90" x2="250" y2="90" stroke="#fcd34d" stroke-width="1.8" stroke-dasharray="4,4"/>
    <text x="210" y="85" font-size="16" font-weight="bold" fill="#fcd34d">✕</text>
  </g>

  <g transform="translate(310, 30)">
    <rect x="0" y="0" width="155" height="150" rx="6" fill="#fef2f2" stroke="#f87171" stroke-width="1.5"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#991b1b">QUỐC KỲ VIỆT NAM:</text>
    <text x="15" y="55" font-size="12" fill="#1e293b">• Lá cờ hình chữ nhật</text>
    <text x="15" y="75" font-size="12" fill="#1e293b">• Sao vàng 5 cánh ở tâm</text>
    <text x="15" y="95" font-size="12" fill="#1e293b">• Đỉnh sao hướng lên</text>
    <text x="15" y="125" font-size="13" font-weight="bold" fill="#dc2626">CẢ LÁ CỜ CÓ:</text>
    <text x="15" y="142" font-size="13" font-weight="bold" fill="#dc2626">ĐÚNG 1 TRỤC ĐỐI XỨNG</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 17, "pid": 16,
        "jump_label": "Slide 17: Bài 16 (Khảo sát tính đối xứng của Quốc kỳ Việt Nam)",
        "badge": "Dạng 4: Gấp giấy & Thực tế",
        "level": 2, "level_text": "Mức 2: Vận dụng vừa sức & Biến thể",
        "type": "problem_with_svg", "svg_code": svg_16,
        "debai": "Quốc kỳ nước Cộng hòa Xã hội Chủ nghĩa Việt Nam có dạng hình chữ nhật màu đỏ, chiều rộng bằng $\\frac{2}{3}$ chiều dài, ở chính giữa có một ngôi sao vàng năm cánh với đỉnh của một cánh hướng thẳng đứng lên trên.<br>a) Riêng nền cờ hình chữ nhật có bao nhiêu trục đối xứng?<br>b) Riêng ngôi sao vàng năm cánh có bao nhiêu trục đối xứng?<br>c) Khi kết hợp cả lá cờ (gồm nền cờ màu đỏ và ngôi sao vàng năm cánh ở chính giữa), lá cờ có tất cả bao nhiêu trục đối xứng? Giải thích vì sao đường nằm ngang qua tâm không phải là trục đối xứng.",
        "analysis": make_heuristic(
            target="Xác định chính xác số trục đối xứng của Quốc kỳ Việt Nam",
            intermediate="Giao các trục đối xứng của nền chữ nhật với trục đối xứng của ngôi sao 5 cánh",
            premise="Đỉnh của ngôi sao hướng thẳng lên trên nên chỉ có trục đứng trùng với trục đứng của hình chữ nhật",
            key_point="Hình chữ nhật có 2 trục (đứng và ngang). Ngôi sao có 5 trục. Nhưng vì đỉnh sao hướng lên trên nên ngôi sao không đối xứng qua trục ngang (trên 1 đỉnh, dưới 2 chân). Do đó, trục đối xứng chung của cả lá cờ CHỈ CÓ DUY NHẤT 1 TRỤC THẲNG ĐỨNG."
        ),
        "solution": """<p><strong>a) Xét riêng nền cờ hình chữ nhật:</strong></p>
<p>Hình chữ nhật có đúng <strong>2 trục đối xứng</strong>: 1 trục thẳng đứng và 1 trục nằm ngang nối trung điểm các cạnh đối diện.</p>
<p><strong>b) Xét riêng ngôi sao năm cánh:</strong></p>
<p>Ngôi sao năm cánh đều có đúng <strong>5 trục đối xứng</strong>, mỗi trục đi qua một đỉnh cánh sao.</p>
<p><strong>c) Xét toàn bộ lá cờ (nền đỏ và sao vàng):</strong></p>
<p>Trục đối xứng của toàn bộ lá cờ phải đồng thời là trục đối xứng của nền cờ hình chữ nhật VÀ là trục đối xứng của ngôi sao vàng năm cánh.</p>
<p>• Đường thẳng đứng đi qua trung điểm hai cạnh dài của lá cờ cũng chính là đường thẳng đi qua đỉnh hướng thẳng đứng của ngôi sao năm cánh. Khi gấp cờ theo đường này, nửa bên trái và nửa bên phải chồng khít hoàn toàn lên nhau. Vậy đây là 1 trục đối xứng.</p>
<p>• Đường thẳng nằm ngang đi qua trung điểm hai cạnh ngắn của lá cờ chia hình chữ nhật làm hai nửa bằng nhau. Tuy nhiên, đối với ngôi sao năm cánh: phía trên đường ngang chỉ có 1 cánh thẳng đứng, trong khi phía dưới đường ngang lại có 2 cánh sao hướng xuống. Khi gấp cờ theo đường ngang, cánh sao phía trên không có cánh sao đối ứng ở phía dưới!</p>
<p>Do đó, đường nằm ngang <em>không phải</em> là trục đối xứng của lá cờ.</p>
<p><strong>Kết luận:</strong> Toàn bộ lá cờ Quốc kỳ Việt Nam có <strong>duy nhất 1 trục đối xứng thẳng đứng</strong>.</p>""",
        "pitfall": "Đây là câu hỏi phân loại tư duy thực tế rất sâu sắc: Học sinh rất hay vội vàng trả lời 'lá cờ có 2 trục đối xứng' vì thấy lá cờ là hình chữ nhật!",
        "extension": "Cách xác định trục đối xứng giao thoa này áp dụng cho mọi bài toán thiết kế quốc kỳ, logo công ty và phù hiệu trường học."
    })

    # =========================================================================
    # DẠNG 5: MỞ RỘNG TƯ DUY KHÁ — GIỎI (ĐỊNH HƯỚNG ÔN THI VÀO 10)
    # =========================================================================

    # --- BÀI 17 (SLIDE 18): Hoa văn hoa tuyết / Lục giác lồng sao 6 cánh ---
    svg_17 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(60, 20)">
    <polygon points="120,10 205,60 205,160 120,210 35,160 35,60" fill="#f8fafc" stroke="#0284c7" stroke-width="2"/>
    <polygon points="120,10 205,160 35,160" fill="none" stroke="#dc2626" stroke-width="2.2"/>
    <polygon points="120,210 205,60 35,60" fill="none" stroke="#2563eb" stroke-width="2.2"/>
    <circle cx="120" cy="110" r="4" fill="#0f172a"/>
    <text x="125" y="105" font-size="13" font-weight="bold" fill="#0f172a">O</text>

    <!-- 6 trục đối xứng -->
    <line x1="120" y1="0" x2="120" y2="220" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="25" y1="55" x2="215" y2="165" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="25" y1="165" x2="215" y2="55" stroke="#16a34a" stroke-width="1.8" stroke-dasharray="5,3"/>
    <line x1="20" y1="110" x2="220" y2="110" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4,3"/>
    <line x1="75" y1="15" x2="165" y2="205" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4,3"/>
    <line x1="165" y1="15" x2="75" y2="205" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4,3"/>
  </g>

  <g transform="translate(300, 40)">
    <rect x="0" y="0" width="165" height="150" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#15803d">HOA VĂN ĐỐI XỨNG:</text>
    <text x="15" y="55" font-size="12" fill="#1e293b">• Ghép từ 2 tam giác đều</text>
    <text x="15" y="75" font-size="12" fill="#1e293b">• Tạo thành sao 6 cánh</text>
    <text x="15" y="95" font-size="12" fill="#1e293b">• Khung lục giác đều</text>
    <text x="15" y="125" font-size="13" font-weight="bold" fill="#15803d">SỐ TRỤC ĐỐI XỨNG:</text>
    <text x="15" y="142" font-size="13" font-weight="bold" fill="#dc2626">ĐÚNG 6 TRỤC ĐỐI XỨNG</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 18, "pid": 17, "is_example": True,
        "jump_label": "Slide 18: Bài 17 (Ví dụ mẫu: Hoa văn hoa tuyết & Ngôi sao 6 cánh)",
        "badge": "Dạng 5: Mở rộng Khá — Giỏi",
        "level": 3, "level_text": "Mức 3: Mở rộng Khá — Giỏi ôn thi 10",
        "type": "problem_with_svg", "svg_code": svg_17,
        "debai": "Một viên gạch trang trí hình lục giác đều có hoa văn được tạo bởi hai tam giác đều bằng nhau lồng vào nhau có chung tâm $O$ (tạo thành một ngôi sao 6 cánh như hình vẽ).<br>a) Mỗi tam giác đều riêng lẻ có bao nhiêu trục đối xứng?<br>b) Khi ghép hai tam giác đều ngược chiều nhau để tạo thành ngôi sao sáu cánh, hình thu được có tất cả bao nhiêu trục đối xứng?<br>c) So sánh số trục đối xứng của ngôi sao 5 cánh và ngôi sao 6 cánh.",
        "analysis": make_heuristic(
            target="Xác định số trục đối xứng của hình ghép tổ hợp đa giác đều",
            intermediate="Tìm các trục đối xứng chung của hai tam giác đều lồng nhau",
            premise="Tam giác đều có 3 trục; phép quay 60 độ bảo toàn hình hoa tuyết",
            key_point="Tam giác 1 có 3 trục. Tam giác 2 có 3 trục. Khi lồng nhau lệch 60 độ, 3 trục của tam giác 1 trở thành 3 đường đi qua trung điểm các cạnh của tam giác 2 và ngược lại, tạo thành tổng cộng 6 trục đối xứng."
        ),
        "solution": """<p><strong>a) Xét mỗi tam giác đều riêng lẻ:</strong></p>
<p>Mỗi tam giác đều có đúng <strong>3 trục đối xứng</strong>, là 3 đường thẳng đi qua mỗi đỉnh và trung điểm của cạnh đối diện.</p>
<p><strong>b) Xét hình ngôi sao 6 cánh (lồng ghép 2 tam giác đều):</strong></p>
<p>Hình ngôi sao 6 cánh có đúng <strong>6 trục đối xứng</strong>, gồm:</p>
<p>• 3 trục đối xứng đi qua các cặp đỉnh đối diện của ngôi sao 6 cánh (chính là 3 trục đối xứng của từng tam giác đều kéo dài).</p>
<p>• 3 trục đối xứng đi qua các đáy lõm đối diện giữa các cánh sao (chính là các đường đi qua trung điểm các cạnh đối diện của ngôi sao).</p>
<p>Do hình này khít hoàn toàn vào một hình lục giác đều bao quanh, nên nó mang trọn vẹn <strong>6 trục đối xứng</strong> của hình lục giác đều.</p>
<p><strong>c) So sánh ngôi sao 5 cánh và ngôi sao 6 cánh:</strong></p>
<p>• Ngôi sao 5 cánh có đúng <strong>5 trục đối xứng</strong> (số trục bằng số cánh, là số lẻ; chỉ đối xứng trục, không có tâm đối xứng).</p>
<p>• Ngôi sao 6 cánh có đúng <strong>6 trục đối xứng</strong> (số trục bằng số cánh, là số chẵn; vừa có đối xứng trục vừa có tâm đối xứng tại tâm $O$).</p>
<p><strong>Kết luận:</strong> Ngôi sao 6 cánh có 6 trục đối xứng, nhiều hơn ngôi sao 5 cánh 1 trục.</p>""",
        "pitfall": "Học sinh thường nghĩ rằng khi ghép 2 hình có 3 trục thì kết quả chỉ có 3 trục (hoặc $3+3=6$ nhưng không chỉ rõ vị trí hình học).",
        "extension": "Các tinh thể bông tuyết trong tự nhiên đều kết tinh theo mạng tinh thể lục giác của phân tử nước, do đó mọi bông tuyết chuẩn đều có đúng 6 trục đối xứng."
    })

    # --- BÀI 18 (SLIDE 19): Bài toán đường đi ngắn nhất của Heron ---
    svg_18 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(20, 10)">
    <!-- Đường thẳng d tại y = 120 -->
    <line x1="20" y1="120" x2="420" y2="120" stroke="#0284c7" stroke-width="3"/>
    <text x="360" y="112" font-size="13" font-weight="bold" fill="#0284c7">Bờ sông d</text>

    <!-- Điểm A tại (70, 40) cách d là 80px -->
    <circle cx="70" cy="40" r="5" fill="#1e40af"/>
    <text x="55" y="38" font-size="15" font-weight="bold" fill="#1e40af">A</text>

    <!-- Điểm B tại (350, 70) cách d là 50px -->
    <circle cx="350" cy="70" r="5" fill="#1e40af"/>
    <text x="360" y="68" font-size="15" font-weight="bold" fill="#1e40af">B</text>

    <!-- Điểm A' đối xứng với A qua d tại (70, 200) cách d đúng 80px -->
    <circle cx="70" cy="200" r="5" fill="#dc2626"/>
    <text x="50" y="210" font-size="15" font-weight="bold" fill="#dc2626">A'</text>
    <line x1="70" y1="40" x2="70" y2="200" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="4,3"/>
    <circle cx="70" cy="120" r="3" fill="#dc2626"/>
    <text x="75" y="135" font-size="12" fill="#dc2626">H</text>

    <!-- Nối thẳng A' với B cắt d tại M tối ưu (230, 120) -->
    <line x1="70" y1="200" x2="350" y2="70" stroke="#16a34a" stroke-width="2.5"/>
    <circle cx="230" cy="120" r="5" fill="#16a34a"/>
    <text x="225" y="140" font-size="14" font-weight="bold" fill="#16a34a">M (Trạm bơm)</text>

    <!-- Đường ống thực tế AM + MB -->
    <line x1="70" y1="40" x2="230" y2="120" stroke="#2563eb" stroke-width="2.2"/>
    <line x1="230" y1="120" x2="350" y2="70" stroke="#2563eb" stroke-width="2.2"/>
  </g>
</svg>"""

    slides.append({
        "slide_num": 19, "pid": 18,
        "jump_label": "Slide 19: Bài 18 (Ứng dụng trục đối xứng: Bài toán đường đi ngắn nhất)",
        "badge": "Dạng 5: Mở rộng Khá — Giỏi",
        "level": 3, "level_text": "Mức 3: Mở rộng Khá — Giỏi ôn thi 10",
        "type": "problem_with_svg", "svg_code": svg_18,
        "debai": "Hai ngôi làng $A$ và $B$ nằm ở cùng một phía đối với con sông thẳng $d$. Người ta cần xây dựng một trạm bơm nước $M$ đặt trên bờ sông $d$ để dẫn nước về cả hai làng bằng hai đường ống $MA$ và $MB$.<br>a) Giả sử $A'$ là điểm đối xứng với làng $A$ qua con sông $d$. Hãy so sánh độ dài đoạn thẳng $MA$ và đoạn thẳng $MA'$ với điểm $M$ bất kỳ trên bờ sông.<br>b) Khi trạm bơm $M$ thay đổi trên bờ sông, tổng độ dài đường ống $MA + MB$ bằng đoạn thẳng nào nối $A'$ và $B$?<br>c) Để tổng chi phí đặt đường ống $MA + MB$ là <strong>ngắn nhất</strong>, trạm bơm $M$ phải nằm ở vị trí nào trên bờ sông $d$?",
        "analysis": make_heuristic(
            target="Tìm vị trí điểm M trên trục d để tổng khoảng cách MA + MB đạt giá trị nhỏ nhất",
            intermediate="Chuyển tổng MA + MB thành MA' + MB nhờ tính chất đối xứng trục",
            premise="Đoạn thẳng nối hai điểm A', B luôn là đường ngắn nhất (Bất đẳng thức tam giác)",
            key_point="Vì d là trục đối xứng của đoạn thẳng AA' nên MA = MA'. Do đó MA + MB = MA' + MB. Để MA' + MB nhỏ nhất thì ba điểm A', M, B phải thẳng hàng, tức là M chính là giao điểm của đoạn thẳng A'B với bờ sông d."
        ),
        "solution": """<p><strong>a) So sánh $MA$ và $MA'$:</strong></p>
<p>Do $A'$ là điểm đối xứng với điểm $A$ qua đường thẳng $d$, nên đường thẳng $d$ <strong>đi qua trung điểm của đoạn thẳng $AA'$ và vuông góc với $AA'$</strong>.</p>
<p>Mọi điểm $M$ nằm trên bờ sông $d$ khi gập theo đường thẳng $d$ thì đoạn thẳng $MA$ sẽ trùng khít lên đoạn thẳng $MA'$.</p>
<p>Do đó, ta luôn có:</p>
<p>$$MA = MA'$$</p>
<p><strong>b) Chuyển đổi tổng độ dài đường ống:</strong></p>
<p>Tổng độ dài hai đường ống dẫn nước từ trạm bơm $M$ về hai làng là:</p>
<p>$$\\text{Tổng độ dài} = MA + MB = MA' + MB$$</p>
<p>Ta thấy $M, A', B$ tạo thành ba đỉnh của một tam giác (nếu không thẳng hàng).</p>
<p>Theo tính chất đường đi giữa hai điểm: Đoạn thẳng luôn là đường ngắn nhất nối hai điểm $A'$ và $B$. Ta có:</p>
<p>$$MA' + MB \\ge A'B$$</p>
<p><strong>c) Xác định vị trí tối ưu của trạm bơm $M$:</strong></p>
<p>Dấu đẳng thức xảy ra khi và chỉ khi điểm $M$ nằm giữa hai điểm $A'$ và $B$, nghĩa là <strong>ba điểm $A', M, B$ thẳng hàng</strong>.</p>
<p><em>Cách xác định vị trí:</em></p>
<p>1. Lấy điểm $A'$ đối xứng với điểm $A$ qua bờ sông $d$.</p>
<p>2. Nối đoạn thẳng $A'B$, đoạn thẳng này cắt bờ sông $d$ tại điểm nào thì đó chính là vị trí trạm bơm $M$ cần xây dựng.</p>
<p>Khi đó, tổng chiều dài đường ống dẫn nước đạt giá trị nhỏ nhất bằng đúng độ dài đoạn thẳng $A'B$.</p>
<p><strong>Kết luận:</strong> Trạm bơm $M$ đặt tại giao điểm của đoạn thẳng $A'B$ với con sông $d$.</p>""",
        "pitfall": "Học sinh lớp 6 thường nghĩ rằng đặt trạm bơm ở vị trí chính giữa khoảng cách giữa A và B trên bờ sông. Cách đó chỉ đúng khi hai làng cách đều bờ sông, còn trường hợp tổng quát bắt buộc phải dùng phép lấy điểm đối xứng qua bờ sông.",
        "extension": "Đây chính là bài toán cực trị hình học kinh điển của nhà toán học cổ đại Heron xứ Alexandria, được ứng dụng rộng rãi từ lắp đặt hạ tầng mạng cáp quang đến định luật phản xạ ánh sáng (tia sáng đi theo đường ngắn nhất)."
    })

    # --- BÀI 19 (SLIDE 20): Tổ hợp Pentomino đối xứng ---
    svg_19 = """<svg viewBox="0 0 480 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <!-- Hình 1: Chữ thập (4 trục đối xứng) -->
  <g transform="translate(20, 20)">
    <rect x="25" y="0" width="25" height="75" fill="#eff6ff" stroke="#2563eb" stroke-width="1.8"/>
    <rect x="0" y="25" width="75" height="25" fill="#eff6ff" stroke="#2563eb" stroke-width="1.8"/>
    <line x1="37.5" y1="-5" x2="37.5" y2="80" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,2"/>
    <line x1="-5" y1="37.5" x2="80" y2="37.5" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,2"/>
    <text x="5" y="100" font-size="12" font-weight="bold" fill="#1e40af">Hình Chữ Thập (+)</text>
    <text x="12" y="116" font-size="11" font-weight="bold" fill="#dc2626">(4 TRỤC ĐỐI XỨNG)</text>
  </g>

  <!-- Hình 2: Chữ T (1 trục đối xứng) -->
  <g transform="translate(130, 20)">
    <rect x="0" y="0" width="75" height="25" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8"/>
    <rect x="25" y="25" width="25" height="50" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8"/>
    <line x1="37.5" y1="-5" x2="37.5" y2="80" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="3,2"/>
    <text x="15" y="100" font-size="12" font-weight="bold" fill="#15803d">Hình Chữ T</text>
    <text x="12" y="116" font-size="11" font-weight="bold" fill="#dc2626">(1 TRỤC ĐỨNG)</text>
  </g>

  <!-- Hình 3: Chữ U (1 trục đối xứng) -->
  <g transform="translate(240, 20)">
    <rect x="0" y="0" width="25" height="50" fill="#fef2f2" stroke="#dc2626" stroke-width="1.8"/>
    <rect x="50" y="0" width="25" height="50" fill="#fef2f2" stroke="#dc2626" stroke-width="1.8"/>
    <rect x="0" y="50" width="75" height="25" fill="#fef2f2" stroke="#dc2626" stroke-width="1.8"/>
    <line x1="37.5" y1="-5" x2="37.5" y2="80" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="3,2"/>
    <text x="15" y="100" font-size="12" font-weight="bold" fill="#b91c1c">Hình Chữ U</text>
    <text x="12" y="116" font-size="11" font-weight="bold" fill="#2563eb">(1 TRỤC ĐỨNG)</text>
  </g>

  <!-- Hình 4: Chữ Z (0 trục đối xứng) -->
  <g transform="translate(350, 20)">
    <rect x="0" y="0" width="50" height="25" fill="#f8fafc" stroke="#64748b" stroke-width="1.8"/>
    <rect x="25" y="25" width="25" height="25" fill="#f8fafc" stroke="#64748b" stroke-width="1.8"/>
    <rect x="25" y="50" width="50" height="25" fill="#f8fafc" stroke="#64748b" stroke-width="1.8"/>
    <text x="15" y="100" font-size="12" font-weight="bold" fill="#475569">Hình Chữ Z</text>
    <text x="12" y="116" font-size="11" font-weight="bold" fill="#64748b">(0 TRỤC ĐỐI XỨNG)</text>
  </g>

  <g transform="translate(20, 155)">
    <rect x="0" y="0" width="440" height="70" rx="8" fill="#fffbeb" stroke="#fcd34d" stroke-width="1.5"/>
    <text x="15" y="25" font-size="13" font-weight="bold" fill="#b45309">BỘ GHÉP HÌNH PENTOMINO (5 Ô VUÔNG ĐƠN VỊ):</text>
    <text x="15" y="45" font-size="12" fill="#1e293b">• Tổng cộng có 12 hình dạng Pentomino khác nhau tạo từ 5 ô vuông.</text>
    <text x="15" y="62" font-size="12" fill="#1e293b">• Phân loại theo tính chất đối xứng giúp phát triển tư duy hình học không gian.</text>
  </g>
</svg>"""

    slides.append({
        "slide_num": 20, "pid": 19,
        "jump_label": "Slide 20: Bài 19 (Phân loại tính đối xứng trục trong các hình Pentomino)",
        "badge": "Dạng 5: Mở rộng Khá — Giỏi",
        "level": 3, "level_text": "Mức 3: Mở rộng Khá — Giỏi ôn thi 10",
        "type": "problem_with_svg", "svg_code": svg_19,
        "debai": "Một hình Pentomino được tạo thành bằng cách ghép $5$ ô vuông đơn vị cạnh $1\\text{ cm}$ lại với nhau sao cho mỗi ô vuông chung nhau ít nhất một cạnh hoàn chỉnh.<br>Quan sát 4 hình Pentomino đặc trưng: Hình chữ thập $(+)$, Hình chữ $\\text{T}$, Hình chữ $\\text{U}$ và Hình chữ $\\text{Z}$.<br>a) Trong 4 hình trên, những hình nào là hình có trục đối xứng? Nêu rõ số trục đối xứng của từng hình.<br>b) Hình chữ thập $(+)$ có bao nhiêu trục đối xứng? Hãy vẽ và chỉ rõ các trục đó.<br>c) Tại sao hình chữ $\\text{Z}$ không có trục đối xứng dù nó trông rất cân đối?",
        "analysis": make_heuristic(
            target="Phân loại tính đối xứng trục của các dạng đa giác ghép ô vuông",
            intermediate="Kiểm tra phép gấp hình qua các đường trục khả dĩ",
            premise="Hình chữ Z có tâm đối xứng nhưng không có trục đối xứng",
            key_point="Hình chữ thập (+) có 4 trục đối xứng (2 trục thẳng đứng/ngang và 2 trục chéo). Hình chữ T và chữ U có 1 trục đối xứng. Hình chữ Z không có trục đối xứng vì khi gấp theo bất kỳ đường nào thì hai nhánh cũng chìa ra hai hướng ngược nhau."
        ),
        "solution": """<p><strong>a) Xác định các hình có trục đối xứng:</strong></p>
<p>• <strong>Hình chữ thập $(+)$:</strong> Là hình có trục đối xứng. Có tất cả <strong>4 trục đối xứng</strong>.</p>
<p>• <strong>Hình chữ $\\text{T}$:</strong> Là hình có trục đối xứng. Có đúng <strong>1 trục đối xứng</strong> thẳng đứng đi qua giữa thanh dọc.</p>
<p>• <strong>Hình chữ $\\text{U}$:</strong> Là hình có trục đối xứng. Có đúng <strong>1 trục đối xứng</strong> thẳng đứng đi qua khe giữa hai nhánh.</p>
<p>• <strong>Hình chữ $\\text{Z}$:</strong> <strong>KHÔNG CÓ trục đối xứng nào</strong>.</p>
<p><strong>b) Bốn trục đối xứng của hình chữ thập $(+)$:</strong></p>
<p>Hình chữ thập gồm 1 ô ở tâm và 4 ô nhô ra 4 phía bằng nhau. Bốn trục đối xứng gồm:</p>
<p>1. Trục thẳng đứng đi qua tâm của 3 ô dọc.</p>
<p>2. Trục nằm ngang đi qua tâm của 3 ô ngang.</p>
<p>3. Trục đường chéo thứ nhất nghiêng $45^\\circ$ đi qua tâm hình.</p>
<p>4. Trục đường chéo thứ hai nghiêng $135^\\circ$ đi qua tâm hình.</p>
<p><strong>c) Giải thích vì sao hình chữ $\\text{Z}$ không có trục đối xứng:</strong></p>
<p>Hình chữ $\\text{Z}$ có hai cánh hướng về hai phía đối nghịch nhau (một cánh sang trái ở phía trên, một cánh sang phải ở phía dưới).</p>
<p>• Nếu gấp theo trục dọc hay trục ngang, cánh trên và cánh dưới nằm lệch phía nhau nên không bao giờ chồng khít.</p>
<p>• Nếu gấp theo đường chéo, mép các ô vuông sẽ vuông góc với nếp gấp và không thể khớp khít vào nhau.</p>
<p>Hình chữ $\\text{Z}$ chỉ có <em>tâm đối xứng</em> (nằm tại tâm của ô vuông chính giữa), không có trục đối xứng.</p>
<p><strong>Kết luận:</strong> Hình chữ thập có 4 trục; hình chữ T và U có 1 trục; hình chữ Z không có trục đối xứng.</p>""",
        "pitfall": "Học sinh rất dễ nhầm lẫn hình chữ Z có trục đối xứng theo đường chéo vì trực giác thấy hai đầu của chữ Z cân bằng nhau.",
        "extension": "Trò chơi xếp hình Tetris kinh điển trên toàn thế giới sử dụng 7 mảnh gạch hình học (Tetromino), trong đó việc nhận biết trục đối xứng giúp người chơi phản xạ nhanh để xoay ghép hình kín kẽ."
    })

    # =========================================================================
    # BẢNG RUBRIC TỰ ĐÁNH GIÁ NĂNG LỰC HỌC TẬP
    # =========================================================================
    rubric_html = """
    <div class="print-section-title" style="margin-top: 30px;">PHẦN IV: BẢNG MA TRẬN TỰ ĐÁNH GIÁ NĂNG LỰC (SELF-ASSESSMENT RUBRIC)</div>
    <div style="font-size: 13px; color: #475569; margin-top: 4px; margin-bottom: 8px; font-style: italic;">
      * Ma trận phân bổ chuẩn mực sư phạm THCS: 80% Dành cho Trung bình — Khá (rèn luyện kỹ thuật & vận dụng vừa sức) — 20% Mở rộng Khá — Giỏi (phát triển tư duy thi vào 10).
    </div>
    <table style="width: 100%; border-collapse: collapse; margin-top: 6px; font-size: 13px;" border="1">
      <thead>
        <tr style="background: #f1f5f9; text-align: center;">
          <th style="padding: 8px;">Tiêu chí Đánh giá Năng lực</th>
          <th style="padding: 8px; width: 30%;">Mức 1: Thông hiểu — Rèn kỹ thuật giải (~50%)</th>
          <th style="padding: 8px; width: 30%;">Mức 2: Vận dụng vừa sức & Thực tế (~30%)</th>
          <th style="padding: 8px; width: 25%;">Mức 3: Mở rộng Khá — Giỏi (~20%)</th>
          <th style="padding: 8px; width: 15%;">Tự đánh giá</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="padding: 8px;"><strong>1. Nhận biết hình có trục đối xứng</strong></td>
          <td style="padding: 8px;">• Nhận biết trục đối xứng của đoạn thẳng, tam giác cân, tam giác đều.<br>• Phân biệt hình có trục và không có trục.</td>
          <td style="padding: 8px;">• Nhận diện trục đối xứng trong chữ cái in hoa, chữ số, biển báo giao thông.<br>• Khảo sát tính đối xứng của từ ngữ.</td>
          <td style="padding: 8px;">• Phân tích tính đối xứng của các hình tổ hợp đa giác đều (hoa tuyết, sao 6 cánh).</td>
          <td style="padding: 8px; text-align: center;">☐ Đạt<br>☐ Cần rèn</td>
        </tr>
        <tr>
          <td style="padding: 8px;"><strong>2. Đếm số trục đối xứng của hình phẳng</strong></td>
          <td style="padding: 8px;">• Xác định đúng số trục của hình thang cân (1), hình thoi (2), hình chữ nhật (2), hình vuông (4).</td>
          <td style="padding: 8px;">• Đếm số trục của biểu tượng thực tế (ngôi sao 5 cánh, trái tim, quốc kỳ).</td>
          <td style="padding: 8px;">• Đếm số trục đối xứng của các hình Pentomino ghép ô vuông.</td>
          <td style="padding: 8px; text-align: center;">☐ Đạt<br>☐ Cần rèn</td>
        </tr>
        <tr>
          <td style="padding: 8px;"><strong>3. Kỹ năng vẽ đối xứng trên lưới ô vuông</strong></td>
          <td style="padding: 8px;">• Dựng điểm và đoạn thẳng đối xứng qua trục dọc hoặc trục ngang.<br>• Dựng tam giác đối xứng.</td>
          <td style="padding: 8px;">• Hoàn thiện nửa hình còn lại của hình chiếc lá, cánh bướm, mũi tên.<br>• Xác định số ô cần tô thêm.</td>
          <td style="padding: 8px;">• Giải bài toán đường đi ngắn nhất (Heron) bằng phép đối xứng trục qua bờ sông.</td>
          <td style="padding: 8px; text-align: center;">☐ Đạt<br>☐ Cần rèn</td>
        </tr>
      </tbody>
    </table>
"""

    lesson_data = {
        "ten_bai_hoc": "TOÁN 6 - BÀI 21: HÌNH CÓ TRỤC ĐỐI XỨNG",
        "ten_chuyen_de": "CHUYÊN ĐỀ DẠY THÊM & RÈN KỸ NĂNG: HÌNH CÓ TRỤC ĐỐI XỨNG",
        "slides": slides,
        "rubric_html": rubric_html
    }

    return lesson_data

if __name__ == "__main__":
    data = create_lesson_bai_21()
    out_dir = r"TROLYTHIEN/TEMP/16.11"
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, "lesson_toan_6_bai_21.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✔ Đã tạo file JSON bài học tại: {json_path}")
    print(f"  - Số slide: {len(data['slides'])}")
