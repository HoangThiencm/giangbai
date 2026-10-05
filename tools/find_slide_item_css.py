import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('min-height: 560px')
if idx != -1:
    print(c[idx-200:idx+300])
