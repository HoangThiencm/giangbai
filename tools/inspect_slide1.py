import subprocess
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for name in [
    'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
]:
    print(f"================ {name} ================")
    with open(name, 'r', encoding='utf-8') as f:
        c = f.read()

    # Find slide 1
    m = re.search(r'(<section[^>]*id=["\']s1["\'][^>]*>[\s\S]*?</section>)', c)
    if m:
        slide1 = m.group(1)
        # Find all blocks and their data-step
        blocks = re.findall(r'<div[^>]*class=["\'][^"\']*content-block[^"\']*["\'][^>]*>', slide1)
        for b in blocks:
            print("  Block:", b)
    else:
        print("  Slide 1 not found!")
