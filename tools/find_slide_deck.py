import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('/* Vùng chứa slide 16:9 chuẩn TV */')
if idx == -1: idx = c.find('.slide-deck')
print(c[idx:idx+800])
