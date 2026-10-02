import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Blackboard CSS
c_start = text.find('/* NÂNG CẤP: THANH CHỌN BỀ MẶT BẢNG VÀ MÀU PHẤN */')
if c_start == -1:
    c_start = text.find('.blackboard-top-bar')
c_end = text.find('/* MENU CHUỘT PHẢI SƯ PHẠM', c_start)
bb_css = text[c_start:c_end].strip()
print("BB CSS len:", len(bb_css))

# 2. Blackboard HTML
h_start = text.find('<div id="blackboardOverlay"')
h_end = text.find('</div>\n</div>', h_start) + 13
bb_html = text[h_start:h_end].strip()
print("BB HTML len:", len(bb_html))

# 3. Blackboard JS
j_start = text.find('// 5. Nâng cấp Bảng viết phấn (Multi-surface Chalkboard)')
if j_start == -1:
    j_start = text.find('function setBoardSurface')
j_end = text.find('/* MENU CHUỘT PHẢI SƯ PHẠM', j_start)
bb_js = text[j_start:j_end].strip()
print("BB JS len:", len(bb_js))

# Check for toggleBlackboard in JS
print("toggleBlackboard in text:", 'function toggleBlackboard' in text)
t_start = text.find('function toggleBlackboard')
t_end = text.find('function initContextMenu', t_start)
print("toggleBlackboard snippet:", text[t_start:t_start+300])
