import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Blackboard CSS
css_start = text.find('/* ==========================================================================\n       BẢNG VIẾT TOÀN MÀN HÌNH')
css_end = text.find('/* ==========================================================================\n       CÔNG CỤ TOÁN HỌC: MÁY TÍNH', css_start)
bb_css = text[css_start:css_end].strip()
print(f"BB CSS length: {len(bb_css)}")

# 2. Blackboard DOM
dom_start = text.find('<div id="blackboardOverlay"')
dom_end = text.find('<!-- MODAL MÁY TÍNH CASIO FX-580VN X', dom_start)
bb_dom = text[dom_start:dom_end].strip()
print(f"BB DOM length: {len(bb_dom)}")

# 3. Blackboard JS
js_start = text.find('/* === BẢNG VIẾT PHẤN TOÀN MÀN HÌNH VỚI ẢNH TỰ DO KÉO THẢ')
js_end = text.find('/* ==========================================================================\n     MÁY TÍNH KHOA HỌC CASIO FX-580VN X', js_start)
bb_js = text[js_start:js_end].strip()
print(f"BB JS length: {len(bb_js)}")

# 4. Context Menu
ctx_start = text.find('<!-- MENU CHUỘT PHẢI SƯ PHẠM')
ctx_end = text.find('<!-- ĐỒNG HỒ ĐẾM NGƯỢC SƯ PHẠM', ctx_start)
ctx_html = text[ctx_start:ctx_end].strip()
print(f"Context menu length: {len(ctx_html)}")

# 5. Toolbar Pedagogy group
ctrl_pedagogy = re.search(r'(<div class="ctrl-group ctrl-group-pedagogy">[\s\S]*?</div>)', text).group(1)
print(f"Toolbar pedagogy group length: {len(ctrl_pedagogy)}")
