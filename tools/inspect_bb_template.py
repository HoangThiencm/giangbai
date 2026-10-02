import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find CSS for blackboard
bb_css_m = re.search(r'/\* ==+ (?:BẢNG VIẾT|BLACKBOARD)[\s\S]*?(?=/\* ==+|$)', text)
if bb_css_m:
    print("Found Blackboard CSS, length:", len(bb_css_m.group(0)))
    print(bb_css_m.group(0)[:200])

# Find HTML for blackboard
bb_html_m = re.search(r'<!-- ==+ (?:BẢNG VIẾT|BLACKBOARD)[\s\S]*?</div>\s*</div>', text)
if not bb_html_m:
    bb_html_m = re.search(r'<div id="blackboardOverlay"[\s\S]*?</div>\s*</div>', text)
if bb_html_m:
    print("\nFound Blackboard HTML, length:", len(bb_html_m.group(0)))
    print(bb_html_m.group(0)[:200])

# Find JS for blackboard
bb_js_m = re.search(r'/\* ==+ BẢNG VIẾT PHẤN[\s\S]*?(?=/\* ==+|$)', text)
if not bb_js_m:
    bb_js_m = re.search(r'function toggleBlackboard[\s\S]*?(?=/\* ==+|function initContextMenu|$)', text)
if bb_js_m:
    print("\nFound Blackboard JS, length:", len(bb_js_m.group(0)))
    print(bb_js_m.group(0)[:200])
