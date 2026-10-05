import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Split slides
pattern = r'<section\s+class="slide-item[^"]*"[^>]*id="(s\d+)"[^>]*data-slide-index="(\d+)"[^>]*>([\s\S]*?)</section>'
for m in re.finditer(pattern, html):
    sid = m.group(1)
    sidx = int(m.group(2))
    body = m.group(3)

    # find blocks
    cb_m = re.search(r'<div class="col-board">([\s\S]*?)</div>\s*<!-- CỘT PHẢI', body)
    if not cb_m:
        cb_m = re.search(r'<div class="col-board">([\s\S]*?)</div>\s*<div class="col-task">', body)
    
    ct_m = re.search(r'<div class="col-task">([\s\S]*?)</div>\s*</div>', body)

    b_blocks = []
    if cb_m:
        for blk in re.finditer(r'<div class="content-block[^"]*"[^>]*id="([^"]+)"(?:[^>]*data-step="([^"]*)")?[^>]*data-title-vi="([^"]*)"', cb_m.group(1)):
            b_blocks.append((blk.group(1), blk.group(2) or 'fix', blk.group(3)))

    t_blocks = []
    if ct_m:
        for blk in re.finditer(r'<div class="content-block[^"]*"[^>]*id="([^"]+)"(?:[^>]*data-step="([^"]*)")?[^>]*data-title-vi="([^"]*)"', ct_m.group(1)):
            t_blocks.append((blk.group(1), blk.group(2) or 'fix', blk.group(3)))

    print(f"Slide {sidx:2d} ({sid}):")
    print(f"   LEFT ({len(b_blocks)}):", b_blocks)
    print(f"  RIGHT ({len(t_blocks)}):", t_blocks)
