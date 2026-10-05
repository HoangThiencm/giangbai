import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("All occurrences of \\x07:")
for m in re.finditer(r'\x07\w*', c):
    print(" ", repr(m.group(0)))

print("\nAll occurrences of \\x08:")
for m in re.finditer(r'\x08\w*', c):
    print(" ", repr(m.group(0)))
