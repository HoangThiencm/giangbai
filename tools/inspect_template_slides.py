import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    c = f.read()

slides = re.findall(r'<section[^>]*class=["\']slide-item[^"\']*["\'][^>]*>', c)
print(f"Total slides in template: {len(slides)}")
for s in slides:
    print(" ", s)
