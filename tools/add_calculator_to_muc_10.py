import os
import glob
import re

# 1. Đọc Casio CSS, HTML, JS từ master_bai_day_html_template.html
source_template = r'TROLYTHIEN\2_TAO_BAI_TAP\templates\master_bai_day_html_template.html'
with open(source_template, 'r', encoding='utf-8') as f:
    source_content = f.read()

# Trích xuất CSS
css_start = source_content.find('/* ==========================================================================\n       4. MÁY TÍNH CẦM TAY CASIO')
css_end = source_content.find('/* ==========================================================================\n       MODAL PHÓNG TO HÌNH ẢNH (LIGHTBOX)')
casio_css = source_content[css_start:css_end].strip()

# Trích xuất HTML
html_start = source_content.find('<!-- ==========================================================================\n       MÁY TÍNH CẦM TAY CASIO fx-580VN X')
html_end = source_content.find('<!-- ==========================================================================\n       MODAL SỬA BÀI')
casio_html = source_content[html_start:html_end].strip()

# Trích xuất JS
js_start = source_content.find('function solveFmt(n) {')
js_end = source_content.find('// 5. CƠ CHẾ SỬA BÀI "SAI ĐÂU SỬA ĐÓ"')
casio_js = source_content[js_start:js_end].strip()

target_files = [
    r'TROLYTHIEN\10_BAI_GIANG_HTML\templates\master_lecture_template.html',
    r'TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html',
    r'TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\Bai_1_Lop_Hoc_Moi_Cua_Em.html',
    r'TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\Bai_2_Truyen_Thong_Truong_Em.html',
    r'TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\Bai_3_Dieu_Chinh_Ban_Than.html',
    r'TROLYTHIEN\10_BAI_GIANG_HTML\Ket_qua\Bai_4_Em_Va_Cac_Ban.html',
]

for file_path in target_files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Thêm CSS vào trước </style>
    if '.casio-widget' not in content:
        content = content.replace('</style>', f"\n{casio_css}\n</style>", 1)
        
    # 2. Thêm HTML vào trước <nav class="control-bar" hoặc trước </body>
    if 'id="casioWidget"' not in content:
        if '<nav class="control-bar"' in content:
            content = content.replace('<nav class="control-bar"', f"{casio_html}\n\n<nav class=\"control-bar\"", 1)
        else:
            content = content.replace('</body>', f"{casio_html}\n</body>", 1)

    # 3. Thêm nút Máy tính vào ctrl-group-pedagogy
    if 'toggleCalculator()' not in content:
        # Tìm trong ctrl-group-pedagogy
        m_ped = re.search(r'(<div class="ctrl-group ctrl-group-pedagogy">[\s\S]*?)(</div>)', content)
        if m_ped:
            old_ped = m_ped.group(0)
            if 'btnCalc' not in old_ped:
                calc_btn = '\n    <button class="btn-ctrl" id="btnCalc" onclick="toggleCalculator()" title="Máy tính Casio fx-580VN X (phím C)">🔢 Máy tính</button>\n  '
                new_ped = m_ped.group(1) + calc_btn + m_ped.group(2)
                content = content.replace(old_ped, new_ped, 1)

    # 4. Thêm JS vào trước </script>
    if 'function toggleCalculator' not in content:
        # Thêm phím tắt C và Escape trong keydown nếu cần
        casio_hook = """
  // Phím tắt C mở máy tính Casio
  document.addEventListener('keydown', function(e) {
    if (e.target.closest && e.target.closest('input, textarea, [contenteditable="true"]')) return;
    if (e.key === 'c' || e.key === 'C') {
      e.preventDefault();
      toggleCalculator();
    } else if (e.key === 'Escape') {
      toggleCalculator(false);
    }
  });
"""
        full_js = f"\n\n/* === CASIO fx-580VN X SIMULATOR === */\n{casio_js}\n{casio_hook}\n"
        # Chèn trước thẻ </script> cuối cùng
        last_script = content.rfind('</script>')
        if last_script != -1:
            content = content[:last_script] + full_js + content[last_script:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Added Casio to: {os.path.basename(file_path)}")
