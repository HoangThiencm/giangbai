import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for path in [
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
]:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"=== {path} ===")
    tags = re.findall(r'<div class="col-[^"]*-tag">([\s\S]*?)</div>', c)
    unique_tags = list(set([t.strip() for t in tags]))
    for ut in sorted(unique_tags):
        print(" ", ut)
