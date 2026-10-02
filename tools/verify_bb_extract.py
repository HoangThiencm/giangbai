import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Blackboard CSS
c_start = text.find('/* BẢNG VIẾT PHẤN NÂNG CẤP: THANH CHỌN BỀ MẶT BẢNG VÀ MÀU PHẤN */')
c_end = text.find('/* Accordion Toggle Answer */', c_start)
bb_css = text[c_start:c_end].strip()

# 2. Blackboard HTML
h_start = text.find('<div id="blackboardOverlay"')
h_end = text.find('</div>\n\n<!-- THANH ĐIỀU KHIỂN', h_start)
if h_end == -1:
    h_end = text.find('</div>\n<!-- THANH ĐIỀU KHIỂN', h_start)
if h_end == -1:
    h_end = text.find('<!-- THANH ĐIỀU KHIỂN', h_start)
bb_html = text[h_start:h_end].strip()

# 3. Blackboard JS
j1_start = text.find('function resizeBlackboard')
if j1_start == -1:
    j1_start = text.find('function toggleBlackboard')
j1_end = text.find('function zoomableFigure', j1_start)
if j1_end == -1:
    j1_end = text.find('// 5. Nâng cấp Bảng viết phấn', j1_start)

j2_start = text.find('// 5. Nâng cấp Bảng viết phấn (Multi-surface Chalkboard)')
j2_end = text.find('function readCurrentSlideVi', j2_start)
if j2_end == -1:
    j2_end = text.find('/* MENU CHUỘT PHẢI SƯ PHẠM', j2_start)

print("CSS found:", bool(bb_css), len(bb_css))
print("HTML found:", bool(bb_html), len(bb_html))
print("JS1 start/end:", j1_start, j1_end)
print("JS2 start/end:", j2_start, j2_end)
