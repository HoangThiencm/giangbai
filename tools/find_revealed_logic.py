import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('is-revealed')
while idx != -1:
    print(c[max(0, idx-100):min(len(c), idx+200)])
    print("-" * 50)
    idx = c.find('is-revealed', idx+1)
