import subprocess
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

cmd = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless',
    '--disable-gpu',
    '--virtual-time-budget=10000',
    '--dump-dom',
    r'file:///c:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

errors = list(re.finditer(r'data-mjx-error="([^"]+)"', res.stdout))
print(f'Total data-mjx-error found: {len(errors)}')
for m in errors:
    idx = m.start()
    print('Error message:', m.group(1))
    print('Context:', res.stdout[max(0, idx-60):min(len(res.stdout), idx+140)])
    print('-'*50)

# Check for any inline errors or red text or [Math Input Error]
math_errs = list(re.finditer(r'Math (?:input|processing) error', res.stdout, re.IGNORECASE))
print(f'Total "Math input error" found: {len(math_errs)}')

# Also search for red brackets or red characters
red_chars = list(re.finditer(r'data-c="5C"|data-c="5B"|data-c="5D"', res.stdout))
print(f'Total data-c brackets: {len(red_chars)}')
