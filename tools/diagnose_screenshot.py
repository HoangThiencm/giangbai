import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("=== 1. CASIO WIDGET ===")
m_casio = re.search(r'<div[^>]*id=["\']casioWidget["\'][^>]*>', c)
if m_casio:
    print("Tag:", m_casio.group(0))
else:
    print("casioWidget tag not found")

idx_css = c.find('.casio-widget {')
if idx_css != -1:
    print("CSS:\n", c[idx_css:idx_css+350])
else:
    print(".casio-widget CSS not found")

print("\n=== 2. SLIDE 1 RIGHT COLUMN (s1_t1) ===")
idx_t1 = c.find('id="s1_t1"')
if idx_t1 != -1:
    print(c[idx_t1-50:idx_t1+800])
else:
    print("s1_t1 not found")

print("\n=== 3. SEARCHING FOR ALL LATEX IN s1_t1 ===")
if idx_t1 != -1:
    end_t1 = c.find('</div>', idx_t1)
    chunk = c[idx_t1:end_t1+200]
    math_expressions = re.findall(r'\$[^\$]+\$', chunk)
    for me in math_expressions:
        print("  Math:", repr(me))

print("\n=== 4. TITLE IN SLIDE 1 ===")
for m in re.finditer(r'<h4[^>]*class=["\']block-title["\'][^>]*>[\s\S]*?</h4>', c[:idx_t1+1500]):
    print("  Block title:", m.group(0))
for m in re.finditer(r'<strong[^>]*>[\s\S]*?</strong>', c[:idx_t1+1500]):
    print("  Strong title:", m.group(0))
