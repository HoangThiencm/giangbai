import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

cb_start = text.find('<nav class="control-bar"')
cb_end = text.find('</nav>', cb_start)
cb_text = text[cb_start:cb_end+6]

print("=== CONTROL BAR IN TEMPLATE ===")
print(cb_text)

print("\n=== BLACKBOARD & DRAWING IN TEMPLATE ===")
print("blackboardOverlay:", "blackboardOverlay" in text)
print("toggleBlackboard:", "toggleBlackboard" in text)
print("drawCanvas:", "drawCanvas" in text)
print("penPalette:", "penPalette" in text)
