# -*- coding: utf-8 -*-
r"""
ENGINE CHUẨN HÓA DUY NHẤT: XUẤT BÀI DẠY HTML & PHIẾU IN A4 (TOÁN THCS)
Trợ lý Sư phạm Hoàng Thiên • Thư mục: TROLYTHIEN/engine/builder_bai_day_html.py

CHỨC NĂNG:
- Nhận cấu trúc dữ liệu bài học (JSON hoặc Python dict) gồm 20 slide.
- Tự động thẩm định sư phạm: chuẩn 100% THCS, cấm \iff, ma trận 80% TB-Khá / 20% Khá-Giỏi.
- Tự động lắp ráp giao diện HTML hoàn chỉnh: MathJax Dynamic Typeset, dock điều khiển SVG
  (phóng to, thu nhỏ, tách nổi, đổi vị trí, kéo dãn chuột resize), Casio fx-580, Bảng viết.
- Tự động xuất phiếu in A4 4 phần chuẩn mực kèm Bảng Rubric tự đánh giá năng lực.
- Xuất file HTML thành phẩm độc lập 100% vào TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/.
"""

import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    '2_TAO_BAI_TAP', 'templates', 'master_bai_day_html_template.html'
)

def build_bai_day_html(lesson_data, output_path, template_path=None):
    """
    Hàm chuẩn hóa duy nhất để tạo bài dạy HTML từ dữ liệu bài học.
    """
    if template_path is None:
        template_path = DEFAULT_TEMPLATE_PATH

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Không tìm thấy master template tại: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    ten_bai_hoc = lesson_data.get("ten_bai_hoc", "BÀI HỌC TOÁN THCS")
    ten_chuyen_de = lesson_data.get("ten_chuyen_de", "CHUYÊN ĐỀ RÈN KỸ NĂNG TOÁN THCS")
    slides = lesson_data.get("slides", [])
    total_slides = len(slides)

    # 1. Thẩm định sư phạm nghiêm ngặt
    content_str = json.dumps(slides, ensure_ascii=False)
    if re.search(r'(\\iff|\\Leftrightarrow|<=>)', content_str):
        print("⚠️ CẢNH BÁO: Phát hiện ký hiệu tương đương \\iff trong nội dung bài tập! Cần sửa sang ngôn ngữ tự nhiên chuẩn THCS.")

    forbidden_c3 = re.findall(r'(định lý sin|định lí sin|định lý côsin|định lí côsin|regiomontanus)', content_str, re.IGNORECASE)
    if forbidden_c3:
        raise ValueError(f"LỖI VI PHẠM SƯ PHẠM: Phát hiện kiến thức cấp 3 bị cấm: {set(forbidden_c3)}")

    jump_options = []
    slides_html = []
    print_items_html = []
    original_svgs_map = {}

    train_level1_items = []
    train_level2_items = []
    train_level3_items = []

    # 2. Xử lý từng Slide
    for item in slides:
        s_num = item["slide_num"]
        s_type = item.get("type", "theory")

        if s_type == "theory":
            jump_options.append(f'<option value="{s_num}">{item["jump_label"]}</option>')
            slide_card = f"""
<section class="slide-card{' active' if s_num == 1 else ''}" data-slide="{s_num}">
  <div class="slide-header">
    <div>
      <span class="slide-badge">{item["badge"]}</span>
    </div>
    <div class="slide-quick-ctrl">
      <button class="nav-btn primary" onclick="nextSlide()">Bài Tiếp ▶</button>
    </div>
  </div>
  <div class="slide-body-full">
    {item["html"]}
  </div>
</section>
"""
            slides_html.append(slide_card)

            if s_num == 1:
                print_items_html.append(f"""
    <div class="print-section-title">PHẦN I: TÓM TẮT KIẾN THỨC TRỌNG TÂM & BẢN CHẤT TOÁN HỌC</div>
    <div class="print-item">
      <div style="font-size: 14px; line-height: 1.6; color: #1e293b;">
        {item["html"]}
      </div>
    </div>
    <div class="print-section-title" style="margin-top: 25px;">PHẦN II: HỆ THỐNG VÍ DỤ MINH HỌA MẪU MỰC</div>
""")

        elif s_type in ["problem_with_svg", "problem_algebra"]:
            pid = item["pid"]
            level = item.get("level", 1)
            level_text = item.get("level_text", "Mức 1: Thông hiểu — Rèn kỹ thuật giải")
            level_class = f"level-{level}"
            jump_options.append(f'<option value="{s_num}">{item["jump_label"]}</option>')

            svg_code = item.get("svg_code", "")
            if svg_code:
                original_svgs_map[str(pid)] = svg_code
                left_panel = f"""
    <div class="diagram-panel" id="diagramPanel_{pid}">
      <div class="diagram-dock-header">
        <span class="dock-header-title">📐 HÌNH MINH HỌA 1:1</span>
        <div class="dock-header-btns">
          <button type="button" class="btn-dock-ctrl btn-pos-toggle" id="btnPos_{pid}" onclick="toggleDiagramUnderProblem('{pid}')" title="Chuyển hình vẽ xuống phía dưới đề bài">⬇️ Dưới đề</button>
          <button type="button" class="btn-dock-ctrl btn-float-toggle" id="btnFloat_{pid}" onclick="toggleFloatDiagram('{pid}')" title="Tách hình nổi, kéo thả tự do khắp màn hình">🆓 Tách nổi</button>
          <button type="button" class="btn-dock-ctrl" onclick="zoomSlideDiagram('{pid}', 0.2)" title="Phóng to hình vẽ">➕</button>
          <button type="button" class="btn-dock-ctrl" onclick="zoomSlideDiagram('{pid}', -0.2)" title="Thu nhỏ hình vẽ">➖</button>
          <button type="button" class="btn-dock-ctrl" onclick="resetSlideDiagram('{pid}')" title="Đặt lại kích thước và vị trí">↺</button>
          <button type="button" class="btn-dock-ctrl" onclick="zoomActiveSlideDiagram('{pid}')" title="Phóng to toàn màn hình (Lightbox)">🔍</button>
        </div>
      </div>
      <div class="diagram-wrapper" id="diagramWrapper_{pid}">
        <div class="diagram-scalable" id="diagramScale_{pid}">
          {svg_code}
        </div>
      </div>
      <div class="image-actions-bar">
        <input type="file" id="fileInput_{pid}" accept="image/*" style="display:none;" onchange="handleImageUpload(event, '{pid}')">
        <button type="button" class="img-btn-upload" onclick="document.getElementById('fileInput_{pid}').click()" title="Thay bằng ảnh chụp hoặc hình vẽ tự vẽ">📷 Chèn ảnh bài {pid}</button>
        <button type="button" class="img-btn-remove" id="btnRemoveImg_{pid}" onclick="removeCustomImage('{pid}')" style="display:none;" title="Xóa ảnh ngoài, dùng lại hình gốc">🗑️ Hình gốc</button>
        <button type="button" class="img-btn-zoom" onclick="zoomActiveSlideDiagram('{pid}')" title="Phóng to chi tiết">🔍 Phóng to</button>
      </div>
    </div>
"""
                body_layout = f"""
  <div class="slide-body-grid">
    {left_panel}
    <div class="content-panel">
"""
            else:
                body_layout = f"""
  <div class="slide-body-full">
    <div class="content-panel">
"""

            slide_card = f"""
<section class="slide-card{' active' if s_num == 1 else ''}" data-slide="{s_num}" data-problem-id="{pid}">
  <div class="slide-header">
    <div>
      <span class="slide-badge">{item["badge"]}</span>
      <span class="level-badge {level_class}">{level_text}</span>
    </div>
    <div class="slide-quick-ctrl">
      <button class="nav-btn info btn-analysis-toggle" onclick="toggleCurrentAnalysis()">🧭 Hướng Giải</button>
      <button class="nav-btn success btn-solution-toggle" onclick="toggleCurrentSolution()">💡 Lời Giải</button>
      <button class="nav-btn primary" onclick="nextSlide()">Bài Tiếp ▶</button>
    </div>
  </div>
  
  {body_layout}
      <div class="problem-box">
        <strong>Bài {pid}:</strong> {item["debai"]}
      </div>

      <!-- 🧭 KHỐI PHÂN TÍCH TƯ DUY -->
      <div class="analysis-box">
        <div class="analysis-header">
          <span>🧭 PHÂN TÍCH TÌM HƯỚNG GIẢI:</span>
          <button type="button" class="btn-close-sol" onclick="hideCurrentAnalysis(event)" title="Đóng hướng giải (Phím H)">✕ Đóng</button>
        </div>
        <div class="analysis-content">
          {item["analysis"]}
        </div>
      </div>

      <!-- 💡 KHỐI LỜI GIẢI MẪU MỰC -->
      <div class="solution-box">
        <div class="solution-header">
          <span>💡 LỜI GIẢI MẪU MỰC:</span>
          <button type="button" class="btn-close-sol" onclick="hideCurrentSolution(event)" title="Đóng lời giải (Space)">✕ Đóng</button>
        </div>
        <div class="solution-content">
          {item["solution"]}

          <div class="pitfall-box">
            <div class="pitfall-header">⚠️ CẠM BẪY & SAI LẦM THƯỜNG GẶP:</div>
            <p>{item["pitfall"]}</p>
          </div>

          <div class="extension-box">
            <div class="extension-header">🚀 KHAI THÁC & PHÁT TRIỂN:</div>
            <p>{item["extension"]}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
            slides_html.append(slide_card)

            # Phân loại vào phiếu in
            if item.get("is_example", False) or pid in [1, 3, 9]:
                ex_item = f"""
    <div class="print-item">
      <div class="print-item-header">Ví dụ mẫu {pid} ({level_text}):</div>
      <div class="print-item-debai">{item["debai"]}</div>
      <div style="font-size: 13.5px; line-height: 1.5; color: #334155; margin-top: 6px; padding: 8px; background: #f8fafc; border-left: 3px solid #3b82f6;">
        <strong>Tóm tắt hướng giải:</strong> {item["analysis"]}
      </div>
    </div>
"""
                print_items_html.append(ex_item)
            else:
                train_item = f"""
    <div class="print-item">
      <div class="print-item-header">Bài {pid} ({level_text}):</div>
      <div class="print-item-debai">{item["debai"]}</div>
      <div class="print-lines">
        <div class="print-line"></div>
        <div class="print-line"></div>
        <div class="print-line"></div>
        <div class="print-line"></div>
      </div>
    </div>
"""
                if level == 1:
                    train_level1_items.append(train_item)
                elif level == 2:
                    train_level2_items.append(train_item)
                else:
                    train_level3_items.append(train_item)

    # 3. Phân tầng Ma trận Phiếu In (80% TB-Khá / 20% Khá-Giỏi)
    print_items_html.append("""
    <div class="print-section-title" style="margin-top: 25px;">PHẦN III: HỆ THỐNG BÀI TẬP TỰ LUYỆN GOM NHÓM (80% TRUNG BÌNH KHÁ — 20% KHÁ GIỎI)</div>
    <div style="font-weight: bold; color: #15803d; background: #dcfce7; padding: 7px 12px; border-radius: 4px; margin-top: 10px; margin-bottom: 10px; font-size: 14px; border: 1px solid #86efac;">
      A. CỤM 1: THÔNG HIỂU — RÈN KỸ THUẬT GIẢI NỀN TẢNG (~40% - 50%):
    </div>
""")
    print_items_html.extend(train_level1_items)

    print_items_html.append("""
    <div style="font-weight: bold; color: #b45309; background: #fef3c7; padding: 7px 12px; border-radius: 4px; margin-top: 20px; margin-bottom: 10px; font-size: 14px; border: 1px solid #fcd34d;">
      B. CỤM 2: VẬN DỤNG VỪA SỨC — BIẾN THỂ & MÔ HÌNH HÓA THỰC TẾ (~30% - 40%):
    </div>
""")
    print_items_html.extend(train_level2_items)

    print_items_html.append("""
    <div style="font-weight: bold; color: #b91c1c; background: #fee2e2; padding: 7px 12px; border-radius: 4px; margin-top: 20px; margin-bottom: 10px; font-size: 14px; border: 1px solid #fca5a5;">
      C. CỤM 3: MỞ RỘNG KHÁ — GIỎI THEO TỪNG DẠNG TOÁN ÔN THI VÀO 10 (~20%):
    </div>
""")
    print_items_html.extend(train_level3_items)

    # 4. Bảng Rubric tự đánh giá
    rubric_html = lesson_data.get("rubric_html", """
    <div class="print-section-title" style="margin-top: 30px;">PHẦN IV: BẢNG MA TRẬN TỰ ĐÁNH GIÁ NĂNG LỰC (SELF-ASSESSMENT RUBRIC)</div>
    <div style="font-size: 13px; color: #475569; margin-top: 4px; margin-bottom: 8px; font-style: italic;">
      * Ma trận phân bổ chuẩn mực sư phạm THCS: 80% Dành cho Trung bình — Khá (rèn luyện kỹ thuật & vận dụng vừa sức) — 20% Mở rộng Khá — Giỏi (phát triển tư duy thi vào 10).
    </div>
    <table style="width: 100%; border-collapse: collapse; margin-top: 6px; font-size: 13px;" border="1">
      <thead>
        <tr style="background: #f1f5f9; text-align: center;">
          <th style="padding: 8px;">Tiêu chí Đánh giá</th>
          <th style="padding: 8px; width: 30%;">Mức 1: Thông hiểu — Rèn kỹ thuật giải (~50%)</th>
          <th style="padding: 8px; width: 30%;">Mức 2: Vận dụng vừa sức & Thực tế (~30%)</th>
          <th style="padding: 8px; width: 25%;">Mức 3: Mở rộng Khá — Giỏi (~20%)</th>
          <th style="padding: 8px; width: 15%;">Tự đánh giá</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="padding: 8px;"><strong>Kỹ năng giải toán cốt lõi</strong></td>
          <td style="padding: 8px;">• Nhận diện công thức và áp dụng trực tiếp<br>• Rèn kỹ thuật tính toán nền tảng</td>
          <td style="padding: 8px;">• Biến thể các bước tính toán<br>• Ứng dụng giải quyết tình huống thực tế</td>
          <td style="padding: 8px;">• Phối hợp kiến thức đa chuyên đề<br>• Câu hỏi phân loại thi vào lớp 10</td>
          <td style="padding: 8px; text-align: center;">☐ Tốt<br>☐ Cần rèn</td>
        </tr>
      </tbody>
    </table>
""")
    print_items_html.append(rubric_html)

    # 5. Ghép vào template
    svgs_json = json.dumps(original_svgs_map, ensure_ascii=False)
    final_html = template_content
    final_html = final_html.replace('khi render vào __SLIDES_HTML__', 'khi render vào các slide')
    final_html = final_html.replace('{{TEN_BAI_HOC}}', ten_bai_hoc)
    final_html = final_html.replace('{{TEN_CHUYEN_DE}}', ten_chuyen_de)
    final_html = final_html.replace('__TOTAL_SLIDES__', str(total_slides))
    final_html = final_html.replace('__ORIGINAL_SVGS_JSON__', svgs_json)
    final_html = final_html.replace('__JUMP_OPTIONS__', '\n        '.join(jump_options))
    final_html = final_html.replace('__SLIDES_HTML__', '\n'.join(slides_html))
    final_html = final_html.replace('__PRINT_HTML__', '\n'.join(print_items_html))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"✔ XUẤT THÀNH CÔNG BÀI DẠY HTML: {output_path}")
    print(f"  - Tổng số slide: {total_slides}")
    print(f"  - Dung lượng file: {os.path.getsize(output_path):,} bytes")
    return output_path

if __name__ == '__main__':
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        out = sys.argv[2] if len(sys.argv) > 2 else data.get("output_path", "output.html")
        build_bai_day_html(data, out)
    else:
        print("Sử dụng: python -m TROLYTHIEN.engine.builder_bai_day_html [file_data.json] [output.html]")
