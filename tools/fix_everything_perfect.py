import subprocess
import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

CASIO_WIDGET_OPEN = """<!-- ==========================================================================
       MÁY TÍNH CẦM TAY CASIO fx-580VN X CLASSWIZ MÔ PHỎNG
       ========================================================================== -->
  <div id="casioWidget" class="casio-widget" style="display:none;">
    <div class="casio-header" id="casioHeader">
      <div class="casio-brand">MÁY TÍNH <b>TRỢ GIẢNG</b><small>NATURAL DISPLAY</small></div>
      <div class="casio-ctrl-btns">
        <button type="button" class="casio-ctrl-btn" onclick="scaleCasio(0.9)" title="Thu nhỏ máy tính">−</button>
        <button type="button" class="casio-ctrl-btn" onclick="scaleCasio(1.1)" title="Phóng to máy tính">+</button>
        <button type="button" class="casio-ctrl-btn close" onclick="toggleCalculator(false)" title="Đóng máy tính">✕</button>
      </div>
    </div>
"""

COL_TAG_MAPPINGS = {
    "📌 MỤC TIÊU BÀI HỌC (3 TIẾT)": "📌 MỤC TIÊU",
    "🎯 TÌNH HUỐNG KHỞI ĐỘNG (SGK TR.74)": "🎯 TÌNH HUỐNG",
    "🎯 HOẠT ĐỘNG KHÁM PHÁ (HĐ1)": "🎯 HOẠT ĐỘNG 1",
    "🎯 HOẠT ĐỘNG KHÁM PHÁ (HĐ2)": "🎯 HOẠT ĐỘNG 2",
    "🎯 CỦNG CỐ KIẾN THỨC & TỔNG KẾT TIẾT 1": "🎯 CỦNG CỐ TIẾT 1",
    "🎯 CỦNG CỐ KIẾN THỨC & TỔNG KẾT TIẾT 2": "🎯 CỦNG CỐ TIẾT 2",
    "🎯 HƯỚNG DẪN TỰ HỌC & BÀI TẬP VỀ NHÀ": "🎯 DẶN DÒ",
    "🎯 BÀI TOÁN HÌNH HỌC — 4 TẦNG TƯ DUY": "🎯 BÀI TOÁN HÌNH HỌC",
    "🎯 BÀI TOÁN THỰC TIỄN — 4 TẦNG TƯ DUY": "🎯 BÀI TOÁN THỰC TIỄN",
    "🎯 GIẢI TAM GIÁC VUÔNG — 4 TẦNG TƯ DUY": "🎯 GIẢI TAM GIÁC VUÔNG",
    "🎯 BỘ 4 CÔNG CỤ TOÁN HỌC CẦN DÙNG": "🎯 CÔNG CỤ CẦN DÙNG",
    "🎯 CHIẾN THUẬT LỰA CHỌN CÔNG THỨC": "🎯 LỰA CHỌN CÔNG THỨC",
    "🎯 HỆ THỐNG HÓA KIẾN THỨC BÀI 12": "🎯 TỔNG KẾT BÀI HỌC",
    "🎯 KHẮC SÂU QUY TẮC & PHẢN XẠ NHANH": "🎯 GHI NHỚ QUY TẮC",
    "🎯 TỔNG QUÁT HÓA TỪ HOẠT ĐỘNG 1": "🎯 KẾT LUẬN TỪ HĐ1",
    "🎯 TỔNG QUÁT HÓA TỪ HOẠT ĐỘNG 2": "🎯 KẾT LUẬN TỪ HĐ2",
    "📌 BẢNG BÀI HỌC (GHI VỞ)": "📌 GHI BẢNG",
}

def fix_file(path):
    print(f"=== Processing {path} ===")
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Khôi phục thẻ mở casioWidget nếu bị thiếu
    if 'id="casioWidget"' not in c:
        if '<div class="casio-bezel">' in c:
            c = c.replace('<div class="casio-bezel">', CASIO_WIDGET_OPEN + '    <div class="casio-bezel">', 1)
            print("  Restored missing casioWidget opening tag!")
        else:
            print("  [WARN] casio-bezel not found!")
    else:
        # Đảm bảo style="display:none;" trên casioWidget
        c = re.sub(
            r'<div\s+id="casioWidget"\s+class="casio-widget"[^>]*>',
            '<div id="casioWidget" class="casio-widget" style="display:none;">',
            c
        )

    # 2. Cập nhật hàm toggleCalculator để set style.display
    c = c.replace(
        "widget.classList.toggle('active', on);\n    const btn",
        "widget.classList.toggle('active', on);\n    widget.style.display = on ? 'block' : 'none';\n    const btn"
    )
    c = c.replace(
        "widget.classList.toggle('active', on);\n      const btn",
        "widget.classList.toggle('active', on);\n      widget.style.display = on ? 'block' : 'none';\n      const btn"
    )

    # 3. Sửa toàn bộ lỗi ký tự điều khiển \a (ASCII 7) và \b (ASCII 8) trong LaTeX
    CONTROL_REPLACEMENTS = [
        ('\x07lpha', r'\alpha'),
        ('\x07pprox', r'\approx'),
        ('\x07rccos', r'\arccos'),
        ('\x08eta', r'\beta'),
        ('\x08egin', r'\begin'),
        ('\x07', ''),
        ('\x08', '')
    ]
    for bad, good in CONTROL_REPLACEMENTS:
        if bad in c:
            cnt = c.count(bad)
            c = c.replace(bad, good)
            print(f"  Fixed {cnt} occurrences of {repr(bad)} -> {repr(good)}")

    # 4. Thay thế col-tag rườm rà
    for old_tag, new_tag in COL_TAG_MAPPINGS.items():
        if old_tag in c:
            cnt = c.count(old_tag)
            c = c.replace(old_tag, new_tag)
            print(f"  Replaced {cnt} verbose col-tags: {old_tag} -> {new_tag}")

    # 5. Đảm bảo .col-board có overflow-y: auto !important để không bị cụt dòng
    col_board_css = """.col-board {
      background: var(--board-bg);
      border: 1.5px solid #cbd5e1;
      border-radius: 10px;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      border-left: 5px solid var(--primary);
      height: 100%;
      overflow-y: auto !important;
      overflow-x: hidden !important;
      scrollbar-width: thin;
      scrollbar-color: var(--primary) rgba(241, 245, 249, 0.6);
    }"""
    # Thay thế .col-board trong CSS
    c = re.sub(
        r'\.col-board\s*\{[^}]*border-left:\s*5px\s*solid\s*var\(--primary\);\s*height:\s*100%;\s*\}',
        lambda m: col_board_css,
        c
    )

    # 6. Sửa Slide 1 trong Bai_12:
    if 'Bai_12' in path:
        # Cập nhật badge-step-num của s1_b1 thành 0
        c = re.sub(
            r'(<div\s+class="content-block[^"]*"\s+id="s1_b1"[^>]*>[\s\S]*?<span class="badge-step-num"[^>]*>)\d+(</span>)',
            r'\g<1>0\g<2>',
            c
        )
        # Tinh chỉnh danh sách 3 tiết trong s1_b1 cho gọn đẹp vừa vặn
        old_ul_pat = r'<ul style="padding-left:18px;margin:4px 0;line-height:1\.6;font-size:0\.95em;">[\s\S]*?</ul>'
        new_ul = """<ul style="padding-left:18px;margin:3px 0;line-height:1.45;font-size:0.92em;">
                <li><b>Tiết 1:</b> Hệ thức giữa cạnh huyền và cạnh góc vuông (Định lí 1).</li>
                <li><b>Tiết 2:</b> Hệ thức giữa hai cạnh góc vuông (Định lí 2).</li>
                <li><b>Tiết 3:</b> Ứng dụng thực tế & giải tam giác vuông.</li>
              </ul>"""
        if re.search(old_ul_pat, c):
            c = re.sub(old_ul_pat, lambda m: new_ul, c)
            print("  Refined s1_b1 list layout in Bai 12.")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"DONE {path}!\n")

for p in [
    'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
]:
    fix_file(p)
