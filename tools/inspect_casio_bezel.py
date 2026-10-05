import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('class="casio-bezel"')
if idx != -1:
    print(c[idx-300:idx+100])
else:
    print("casio-bezel not found")
