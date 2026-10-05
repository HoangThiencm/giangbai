import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Check for \n[a-z] inside $...$ or $$...$$
def check_math_escapes(content):
    all_math = []
    for m in re.finditer(r'(\${1,2})(.*?)\1', content, re.DOTALL):
        all_math.append((m.group(0), m.start()))

    print(f"Total math blocks: {len(all_math)}")
    for block, start_idx in all_math:
        # Check for unescaped python escapes like \night, \tan -> \t, etc.
        # Notice \night is literal \n followed by ight
        if '\night' in block or '\right' in block:
            pass # we know about this
        if '\n' in block:
            # check if newline is right after backslash or in place of backslash
            lines = block.split('\n')
            for line_idx, line in enumerate(lines):
                # if a line starts with a common command suffix without backslash
                m_suspicious = re.match(r'^(ight|rac|ext|begin|end|cdot|circ|approx|sqrt|alpha|beta)\b', line.strip())
                if m_suspicious:
                    print(f"Suspicious word at line start in math at {start_idx}: {m_suspicious.group(0)}")
                    print(f"  Context: {repr(block[:100])}")

check_math_escapes(text)
