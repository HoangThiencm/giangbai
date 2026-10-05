import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'<section\s+class="slide-item[^"]*"[^>]*data-slide-index="(\d+)"[^>]*>([\s\S]*?)</section>'
for m in re.finditer(pattern, text):
    sidx = m.group(1)
    content = m.group(2)
    # find all block titles and tags
    print(f"=== SLIDE {sidx} ===")
    tags = re.findall(r'<div class="col-(?:board|task)-tag">([\s\S]*?)</div>', content)
    print("  TAGS:", [t.strip() for t in tags])
    blocks = re.findall(r'<div class="content-block[^"]*"(?:[^>]*data-step="([^"]*)")?[^>]*>([\s\S]*?)(?:</div>\s*</div>|<div class="content-block|$)', content)
    for b in re.finditer(r'<div class="content-block[^"]*"[^>]*data-step="([^"]*)"[^>]*>([\s\S]*?)(?=<div class="content-block|</div>\s*</div>|\s*<button)', content):
        st = b.group(1)
        blk_body = b.group(2)
        btitle = re.search(r'<(?:h4|strong|div)\s+class="block-title"[^>]*>([\s\S]*?)</(?:h4|strong|div)>|<strong>([\s\S]*?)</strong>', blk_body)
        title_str = btitle.group(1) or btitle.group(2) if btitle else 'NO TITLE'
        print(f"    step={st}: {title_str.strip()[:60]}")
