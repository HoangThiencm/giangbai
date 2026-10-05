import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx_s1 = c.find('id="s1"')
end_s1 = c.find('</section>', idx_s1)
s1 = c[idx_s1:end_s1]

print("=== Titles in Slide 1 ===")
for m in re.finditer(r'<h4[^>]*>([\s\S]*?)</h4>', s1):
    print("  h4:", repr(m.group(1).strip()))
for m in re.finditer(r'<strong[^>]*>([\s\S]*?)</strong>', s1):
    print("  strong:", repr(m.group(1).strip()))
for m in re.finditer(r'data-title-vi=["\']([^"\']*)["\']', s1):
    print("  data-title-vi:", repr(m.group(1)))
for m in re.finditer(r'<div class="col-board-tag">([\s\S]*?)</div>', s1):
    print("  col-board-tag:", repr(m.group(1).strip()))
