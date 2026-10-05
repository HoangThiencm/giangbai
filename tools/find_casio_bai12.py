import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("Finding casio tags:")
for m in re.finditer(r'<[a-z0-9]+[^>]*id=["\'][^"\']*casio[^"\']*["\'][^>]*>', c, re.I):
    print(" ", m.group(0))

print("\nFinding class casio:")
for m in re.finditer(r'<[a-z0-9]+[^>]*class=["\'][^"\']*casio[^"\']*["\'][^>]*>', c, re.I):
    print(" ", m.group(0))
