import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def audit_file(filepath):
    print(f"\n==================== AUDITING: {filepath} ====================")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all math expressions: $$...$$ and $...$
    math_blocks = []
    for m in re.finditer(r'\$\$(.*?)\$\$', content, re.DOTALL):
        math_blocks.append(('display', m.group(1), m.start()))
    
    # Inline math (skip display math)
    clean_content = re.sub(r'\$\$.*?\$\$', lambda m: ' ' * len(m.group(0)), content, flags=re.DOTALL)
    for m in re.finditer(r'\$([^\$\n]+?)\$', clean_content):
        math_blocks.append(('inline', m.group(1), m.start()))

    print(f"Total math blocks: {len(math_blocks)}")

    errors = []
    for kind, math_text, pos in math_blocks:
        # Check 1: single backslash followed by [Xpt]
        if re.search(r'(?<!\\)\\\[\d+pt\]', math_text):
            errors.append((pos, kind, "Single backslash \\[Xpt\\]", math_text))
        
        # Check 2: unknown or malformed LaTeX command
        # Valid mathjax commands usually start with \[a-zA-Z]+ or special symbols
        # Check for unescaped control characters or weird characters
        for ch in ['\x07', '\x08', '\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x0b', '\x0c', '\x0e', '\x0f']:
            if ch in math_text:
                errors.append((pos, kind, f"Control character {ord(ch)}", math_text))

        # Check 3: begin without matching end
        begins = re.findall(r'\\begin\{([a-zA-Z0-9*]+)\}', math_text)
        ends = re.findall(r'\\end\{([a-zA-Z0-9*]+)\}', math_text)
        if begins != ends:
            errors.append((pos, kind, f"Mismatched environments: {begins} vs {ends}", math_text))

        # Check 4: single backslash line break before \mathbf or other commands in environments like cases/aligned
        # In LaTeX cases, newline MUST be \\
        # Check if someone wrote something like `... \ \mathbf` or similar
        if re.search(r'\\begin\{(?:cases|aligned|matrix|bmatrix|array)\}', math_text):
            # check if there's no \\ in the environment
            if r'\\' not in math_text and r'\cr' not in math_text:
                errors.append((pos, kind, "Environment has multiple rows but NO \\\\ line break!", math_text))

    print(f"Total errors found: {len(errors)}")
    for pos, kind, err_type, math_text in errors:
        snippet = math_text.strip().replace('\n', ' ')
        if len(snippet) > 80: snippet = snippet[:80] + '...'
        print(f"  [Pos {pos}] ({kind}) {err_type} -> {snippet}")

audit_file(r'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_12_Mot_so_he_thuc_giua_canh_va_goc_trong_tam_giac_vuong_va_ung_dung.html')
audit_file(r'TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/Bai_4_Phuong_trinh_quy_ve_phuong_trinh_bac_nhat_mot_an.html')
audit_file(r'TROLYTHIEN/10_BAI_GIANG_HTML/templates/master_lecture_template.html')
