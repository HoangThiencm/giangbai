import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    c = f.read()

style = c[:c.find('</style>')]
for m in re.finditer(r'([^{}]*?\.slide-deck[^{}]*?\{[^}]*\})', style):
    print("Match:\n", m.group(1).strip())
