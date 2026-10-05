import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for path in [
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'
]:
    print(f"\n==================== {path} ====================")
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    slides = re.findall(r'<section class="slide-item"[^>]*id="([^"]+)"[^>]*>([\s\S]*?)</section>', html)
    for sid, scontent in slides:
        print(f"\n--- Slide: {sid} ---")
        # Find all content-blocks
        blocks = re.findall(r'<div class="content-block[^"]*"[^>]*data-step="([^"]*)"[^>]*data-title-vi="([^"]*)"', scontent)
        # Check if in col-board or col-task
        col_board_m = re.search(r'<div class="col-board">([\s\S]*?)</div>\s*<div class="col-task">', scontent)
        col_task_m = re.search(r'<div class="col-task">([\s\S]*?)</div>\s*</div>\s*</section>', scontent)
        
        board_blocks = []
        task_blocks = []
        if col_board_m:
            board_blocks = re.findall(r'data-step="([^"]*)"[^>]*data-title-vi="([^"]*)"', col_board_m.group(1))
        if col_task_m:
            task_blocks = re.findall(r'data-step="([^"]*)"[^>]*data-title-vi="([^"]*)"', col_task_m.group(1))
        
        print("  [Col Left  / Board]:", board_blocks)
        print("  [Col Right / Task ]:", task_blocks)
