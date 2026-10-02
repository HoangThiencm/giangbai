import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'TƯ DUY SƯ PHẠM' in line or 'HƯỚNG DẪN TƯ DUY' in line or 'SƯ PHẠM' in line:
        if 'MÁY TÍNH' not in line and 'MENU' not in line and 'ctrl-group' not in line:
            print(f"Line {idx+1}: {line.strip()[:120]}")
