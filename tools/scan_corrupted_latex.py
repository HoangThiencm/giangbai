import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for path in [
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html',
    'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html'
]:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    print(f"=== Scanning {path} ===")
    
    # Check for control characters
    bad_chars = [('\x07', 'BELL \\a'), ('\x08', 'BACKSPACE \\b'), ('\x0c', 'FORMFEED \\f'), ('\t', 'TAB \\t'), ('\r', 'CR \\r')]
    for ch, name in bad_chars:
        cnt = c.count(ch)
        if cnt > 0:
            print(f"  Found {cnt} occurrences of {name}")

    # Check for "lpha" or "eta" in math
    for m in re.finditer(r'\$[^\$]*?(?:lpha|eta|irc)[^\$]*?\$', c):
        print("  Suspicious math:", m.group(0))
