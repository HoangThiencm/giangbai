import sys
import re
import subprocess
import tempfile
import os

sys.stdout.reconfigure(encoding='utf-8')

targets = [
    'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'
]

all_ok = True
for t in targets:
    if not os.path.exists(t):
        continue
    with open(t, 'r', encoding='utf-8') as f:
        html = f.read()

    
    scripts = re.findall(r'<script(?:\s+[^>]*)?>([\s\S]*?)</script>', html, re.IGNORECASE)
    print(f"=== Checking {t} ({len(scripts)} scripts) ===")
    
    for i, s in enumerate(scripts):
        # Skip MathJax config if type is math/tex
        if 'window.MathJax' not in s and len(s.strip()) < 10:
            continue
        with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as tmp:
            tmp.write(s)
            tmp_path = tmp.name
        try:
            res = subprocess.run(['node', '--check', tmp_path], capture_output=True, text=True)
            if res.returncode != 0:
                print(f"  [X] Script {i+1} ERROR:")
                print(res.stderr)
                all_ok = False
            else:
                print(f"  [OK] Script {i+1} valid syntax ({len(s.strip())} chars)")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if all_ok:
    print("\nALL JAVASCRIPT SYNTAX CHECKS PASSED WITH 0 ERRORS!")
else:
    print("\nSOME SYNTAX CHECKS FAILED!")
    sys.exit(1)
