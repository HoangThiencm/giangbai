import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'blackboard|surface-green|\.btn-bb', text, re.I)]
for m in matches[:10]:
    start = max(0, m - 50)
    end = min(len(text), m + 150)
    print(text[start:end])
    print('='*50)
