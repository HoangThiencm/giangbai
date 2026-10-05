import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html', 'r', encoding='utf-8') as f:
    html = f.read()

sec_matches = list(re.finditer(r'<section\s+class="slide-item[^"]*"[^>]*id="([^"]+)"[^>]*data-slide-index="([^"]+)"[^>]*>([\s\S]*?)</section>', html))
print(f"Found {len(sec_matches)} slides in Bai 4.")

for m in sec_matches:
    sid = m.group(1)
    sidx = m.group(2)
    sbody = m.group(3)
    
    cb_m = re.search(r'<div class="col-board">([\s\S]*?)</div>\s*<!-- CỘT PHẢI', sbody)
    if not cb_m:
        cb_m = re.search(r'<div class="col-board">([\s\S]*?)</div>\s*<div class="col-task">', sbody)
    
    ct_m = re.search(r'<div class="col-task">([\s\S]*?)</div>\s*</div>\s*</section>', sbody)
    if not ct_m:
        ct_m = re.search(r'<div class="col-task">([\s\S]*?)</div>\s*</div>', sbody)
    
    board_items = []
    if cb_m:
        for bm in re.finditer(r'<div class="content-block[^"]*"[^>]*id="([^"]+)"(?:[^>]*data-step="([^"]*)")?[^>]*data-title-vi="([^"]*)"', cb_m.group(1)):
            board_items.append((bm.group(1), bm.group(2) or 'fixed', bm.group(3)))
    
    task_items = []
    if ct_m:
        for tm in re.finditer(r'<div class="content-block[^"]*"[^>]*id="([^"]+)"(?:[^>]*data-step="([^"]*)")?[^>]*data-title-vi="([^"]*)"', ct_m.group(1)):
            task_items.append((tm.group(1), tm.group(2) or 'fixed', tm.group(3)))
    
    print(f"\n[Slide {sidx} ({sid})]")
    print("  LEFT :", board_items)
    print("  RIGHT:", task_items)
    
    all_steps = []
    for bid, st, tit in board_items:
        if st != 'fixed':
            all_steps.append((int(st), 'LEFT', bid, tit))
    for tid, st, tit in task_items:
        if st != 'fixed':
            all_steps.append((int(st), 'RIGHT', tid, tit))
    all_steps.sort(key=lambda x: x[0])
    flow = " -> ".join([f"{col}[s={st}:{tit[:15]}]" for st, col, bid, tit in all_steps])
    print("  FLOW:", flow)
