import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    c = f.read()

for selector in ['.slide-deck', '.slide-item', '.slide-content-grid', '.col-board', '.col-task']:
    m = re.search(rf'({re.escape(selector)}\s*\{{[^}}]*\}})', c)
    if m:
        print(m.group(1))
    else:
        print(f"NOT FOUND: {selector}")
