import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx_s1 = c.find('id="s1"')
end_s1 = c.find('</section>', idx_s1)
s1 = c[idx_s1:end_s1]

print("=== Col tags in Slide 1 ===")
for m in re.finditer(r'<div class="col-[^"]*-tag">([\s\S]*?)</div>', s1):
    print("  tag:", repr(m.group(1).strip()))
