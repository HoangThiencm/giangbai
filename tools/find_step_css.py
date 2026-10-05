import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('/* Ẩn hiện theo bước */')
if idx == -1: idx = c.find('[data-step]')
print(c[idx-50:idx+600])
