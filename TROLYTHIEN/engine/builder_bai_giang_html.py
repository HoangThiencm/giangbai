# -*- coding: utf-8 -*-
"""
ENGINE CHUẨN HÓA DUY NHẤT: XUẤT BÀI GIẢNG ĐIỆN TỬ HTML 16:9 TRÌNH CHIẾU
Trợ lý Sư phạm Hoàng Thiên • Thư mục: TROLYTHIEN/engine/builder_bai_giang_html.py

CHỨC NĂNG:
- Nhận cấu trúc dữ liệu bài giảng (JSON hoặc Python dict) chứa các slide 16:9.
- Ghép vào Master Lecture Template: hỗ trợ Bảng viết đen/xanh/trắng đa năng, phấn màu,
  MathJax dynamic typeset, bước xuất hiện (slide steps), Laser pointer, phím tắt F / Space.
- Xuất file HTML trình chiếu độc lập 100% vào TROLYTHIEN/10_BAI_GIANG_HTML/.
"""

import os
import sys
import json
import re
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

MASTER_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    '10_BAI_GIANG_HTML', 'templates', 'master_lecture_template.html'
)

def build_bai_giang_html(lecture_data, output_html_path, template_path=None):
    """
    Hàm chuẩn hóa duy nhất để tạo bài giảng HTML trình chiếu 16:9.
    """
    if template_path is None:
        template_path = MASTER_TEMPLATE_PATH

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Không tìm thấy master lecture template tại: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    ten_bai = lecture_data.get("ten_bai", "BÀI GIẢNG ĐIỆN TỬ")
    mon_hoc = lecture_data.get("mon_hoc", "Toán học")
    lop = lecture_data.get("lop", "9")
    so_tiet = lecture_data.get("so_tiet", 2)
    giao_vien = lecture_data.get("giao_vien", "Trợ lý Sư phạm Hoàng Thiên")
    truong = lecture_data.get("truong", "Trường THCS Trần Phú")
    slides = lecture_data.get("slides", [])
    total_slides = len(slides)

    # Lắp ráp danh sách slides HTML
    slides_html_list = []
    for idx, s in enumerate(slides, 1):
        s_title = s.get("title", f"NỘI DUNG {idx}")
        tiet = s.get("tiet", 1)
        max_steps = s.get("max_steps", 1)
        body_html = s.get("body_html", "")
        active_class = " active" if idx == 1 else ""

        slide_item = f"""
    <!-- SLIDE {idx}: {s_title} -->
    <section class="slide-item{active_class}" data-slide-index="{idx}" data-tiet="{tiet}" data-max-steps="{max_steps}">
      <header class="slide-header">
        <span class="slide-lesson-title">{mon_hoc.upper()} {lop} &bull; BỘ SÁCH KẾT NỐI TRI THỨC</span>
        <span class="slide-heading-text">TIẾT {tiet} &bull; {ten_bai.upper()}</span>
        <span class="slide-index-badge">{idx} / {total_slides}</span>
      </header>
      <div class="slide-content-grid" style="min-height:68vh; padding:24px 20px;">
        {body_html}
      </div>
    </section>
"""
        slides_html_list.append(slide_item)

    all_slides_html = "\n".join(slides_html_list)

    # Thay thế phần slide-deck bên trong template
    deck_start_pat = r'(<div class="slide-deck" id="slideDeck">)'
    deck_end_pat = r'(</div>\s*<div id="blackboardOverlay")'

    m_start = re.search(deck_start_pat, template_content)
    m_end = re.search(deck_end_pat, template_content)

    if m_start and m_end:
        start_pos = m_start.end()
        end_pos = m_end.start()
        final_html = template_content[:start_pos] + "\n" + all_slides_html + "\n  " + template_content[end_pos:]
    else:
        # Fallback nếu không khớp cấu trúc: ghi đè thông qua placeholder
        final_html = template_content

    # Cập nhật title tag
    final_html = re.sub(r'<title>.*?</title>', f'<title>{ten_bai} — {mon_hoc} {lop} ({so_tiet} tiết)</title>', final_html, count=1)

    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"✔ XUẤT THÀNH CÔNG BÀI GIẢNG HTML: {output_html_path}")
    print(f"  - Tổng số slide: {total_slides}")
    print(f"  - Dung lượng: {os.path.getsize(output_html_path):,} bytes")
    return output_html_path

def main():
    parser = argparse.ArgumentParser(description="Universal Lecture Slides HTML Engine - Trợ lý Sư phạm Hoàng Thiên")
    parser.add_argument("--json", type=str, help="Đường dẫn file JSON chứa dữ liệu bài giảng")
    parser.add_argument("--out", type=str, help="Đường dẫn file HTML xuất ra")

    args = parser.parse_args()
    if args.json:
        with open(args.json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        out = args.out or data.get("output_path", "TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_Giang.html")
        build_bai_giang_html(data, out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
