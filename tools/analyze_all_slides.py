import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def analyze_file(path):
    print(f"\n=======================================================")
    print(f"ANALYZE: {path}")
    print(f"=======================================================")
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all sections with slide-item
    sec_matches = list(re.finditer(r'<section\s+class="slide-item[^"]*"[^>]*id="([^"]+)"[^>]*data-slide-index="([^"]+)"[^>]*>([\s\S]*?)</section>', html))
    print(f"Found {len(sec_matches)} slides.")

    for m in sec_matches:
        sid = m.group(1)
        sidx = m.group(2)
        sbody = m.group(3)

        # Header title
        htitle_m = re.search(r'<span class="slide-heading-text">([^<]*)</span>', sbody)
        htitle = htitle_m.group(1).strip() if htitle_m else ""

        # Col board
        cb_m = re.search(r'<div class="col-board">([\s\S]*?)</div>\s*<div class="col-task">', sbody)
        # Col task
        ct_m = re.search(r'<div class="col-task">([\s\S]*?)</div>\s*</div>\s*(?:<!--|$)', sbody)

        print(f"\n[Slide {sidx} | {sid}] {htitle}")

        board_items = []
        if cb_m:
            for bm in re.finditer(r'<div class="content-block[^"]*"[^>]*id="([^"]+)"(?:[^>]*data-step="([^"]*)")?[^>]*data-title-vi="([^"]*)"', cb_m.group(1)):
                board_items.append((bm.group(1), bm.group(2) or 'none', bm.group(3)))

        task_items = []
        if ct_m:
            for tm in re.finditer(r'<div class="content-block[^"]*"[^>]*id="([^"]+)"(?:[^>]*data-step="([^"]*)")?[^>]*data-title-vi="([^"]*)"', ct_m.group(1)):
                task_items.append((tm.group(1), tm.group(2) or 'none', tm.group(3)))

        print("  LEFT (Ghi bảng) :", [(bid, f"step={st}", tit) for bid, st, tit in board_items])
        print("  RIGHT (Hoạt động):", [(tid, f"step={st}", tit) for tid, st, tit in task_items])

        # Check sequence
        all_steps = []
        for bid, st, tit in board_items:
            if st != 'none':
                all_steps.append((int(st), 'LEFT', bid, tit))
        for tid, st, tit in task_items:
            if st != 'none':
                all_steps.append((int(st), 'RIGHT', tid, tit))
        all_steps.sort(key=lambda x: x[0])
        flow = " -> ".join([f"{col}[s={st}:{tit[:15]}]" for st, col, bid, tit in all_steps])
        print("  FLOW:", flow)

analyze_file('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html')
analyze_file('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html')
