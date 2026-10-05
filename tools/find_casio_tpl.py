import sys
sys.stdout.reconfigure(encoding='utf-8')

for path in [
    'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
]:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"=== {path} ===")
    print("  id='casioWidget':", 'id="casioWidget"' in c)
    print("  casio-header:", 'class="casio-header"' in c)
    print("  casio-bezel:", 'class="casio-bezel"' in c)
    print("  \\a count:", c.count('\x07'))
    print("  \\b count:", c.count('\x08'))
