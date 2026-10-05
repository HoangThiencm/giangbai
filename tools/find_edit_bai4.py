import re

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("Finding edit in Bai 4:")
for m in re.finditer(r'<div[^>]*id=["\'][^"\']*edit[^"\']*["\'][^>]*>', c, re.I):
    print(" ", m.group(0))
