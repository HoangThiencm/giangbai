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

    titles = re.findall(r'data-title-vi="([^"]*)"', html)
    unique_titles = []
    for t in titles:
        if t not in unique_titles:
            unique_titles.append(t)
    print(f"Total blocks: {len(titles)}, Unique titles: {len(unique_titles)}")
    for t in unique_titles:
        print(" -", t)
