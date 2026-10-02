import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all strong tags
strongs = re.findall(r'<strong>(.*?)</strong>', text)
pedagogy_keywords = ['SƯ PHẠM', 'GIÁO VIÊN', 'GV ', 'HỌC SINH ĐỌC', 'TƯ DUY SƯ PHẠM']
found = []
for s in strongs:
    for kw in pedagogy_keywords:
        if kw in s.upper():
            found.append(s)

print("Pedagogy strongs found:", set(found))
