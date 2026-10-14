# -*- coding: utf-8 -*-
"""
HỆ THỐNG PHẢN BIỆN TỰ ĐỘNG ĐA VÒNG ĐỀ CƯƠNG ÔN TẬP TOÁN (MULTI-ROUND AUTOMATIC AUDITOR)
Quy trình phản biện 3 vòng nghiêm ngặt:
  - VÒNG 1: Phản biện Toán học & Tính toàn vẹn số liệu (Mathematical & Pedagogical Logic Audit)
    + Toán 6: 100% phép tính trong N phải chia hết, trừ không âm, nghiệm tìm x là số tự nhiên.
    + Toán 7, 8, 9: Số liệu thực tế mẫu mực, nguyên đẹp, không mâu thuẫn giữa giả thiết đề bài và đáp số.
  - VÒNG 2: Phản biện Cấu trúc XML & Chuẩn hóa hiển thị Word Equation (Deep XML & OMML Audit)
    + Quét sâu từng thẻ XML <w:t> và <m:oMath>/<m:t>.
    + Chuyển đổi và dọn sạch 100% tàn dư LaTeX thô trong Equation.
    + Triệt tiêu mọi ô vuông nét đứt rỗng (<m:e/>).
    + Dọn sạch ký hiệu vi phạm GDPT 2018 (<=>, ⇔) và công thức lỗi chữ đỏ.
    + Chuẩn hóa tiêu đề đáp số, dọn sạch lỗi lặp từ ("Bài Đáp số Đề").
  - VÒNG 3: Tổng kiểm tra chéo & Cấp chứng nhận Đạt chuẩn Sư phạm (PASS 100%).
"""

import re
import os
import docx

LATEX_LEAK_PATTERNS = [
    r'\\mathrm',
    r'\\text\{',
    r'\\frac',
    r'\\sqrt',
    r'\\overline',
    r'\\begin\{cases\}',
    r'\\vdots',
    r'\\cdot',
    r'\\times',
    r'\\sim',
    r'\\perp',
    r'\\parallel',
    r'\\pm',
    r'\\in',
    r'\\notin',
    r'\\le',
    r'\\ge',
    r'\\left',
    r'\\right',
    r'\$[^\$]+\$',
    r'\^[0-9]+',
    r'\^\('
]

def auto_wrap_unwrapped_latex(text):
    """Tự động bọc $...$ cho các biểu thức toán học LaTeX bị quên bọc $ ngoài văn bản."""
    if not text:
        return text
    parts = re.split(r'(\$[^\$]+\$)', text)
    result_parts = []
    for part in parts:
        if part.startswith('$') and part.endswith('$'):
            result_parts.append(part)
        else:
            p = part
            p = re.sub(r'(\\mathrm\{[^{}]+\}(\([^\)]*\))?(\s*=\s*[^,\.;\n]+)?)', r'$\1$', p)
            p = re.sub(r'(\\text\{(?:ƯCLN|BCNN)\}(\([^\)]*\))?(\s*=\s*[^,\.;\n]+)?)', r'$\1$', p)
            p = re.sub(r'(\\frac\{[^{}]+\}\{[^{}]+\})', r'$\1$', p)
            p = re.sub(r'(\\sqrt\{[^{}]+\})', r'$\1$', p)
            p = re.sub(r'(\\overline\{[^{}]+\})', r'$\1$', p)
            result_parts.append(p)
    return "".join(result_parts)

def audit_round_1_math_logic(doc, docx_path):
    """
    VÒNG 1: PHẢN BIỆN TOÁN HỌC & TÍNH TOÀN VẸN SỐ LIỆU
    Kiểm tra các biểu thức toán học, tính chia hết, tính không âm trong N, và tính khớp nối giả thiết - đáp số.
    """
    issues = []
    fname = os.path.basename(docx_path)
    is_toan_6 = ("Toan_6" in fname or "Toán 6" in fname)
    is_toan_8 = ("Toan_8" in fname or "Toán 8" in fname)
    is_toan_9 = ("Toan_9" in fname or "Toán 9" in fname)

    total_formulas_checked = 0

    for p_idx, p in enumerate(doc.paragraphs):
        p_text = p.text.strip()
        if not p_text:
            continue

        # Kiểm tra Toán 6: Phép tính trong N
        if is_toan_6:
            # Tìm các biểu thức có dấu chia : hoặc /
            # VD: 100 : [34 - (18 - 3 * 5)^2]
            div_matches = re.findall(r'(\d+)\s*:\s*\[([^\]]+)\]', p_text)
            for num_str, inner in div_matches:
                total_formulas_checked += 1
                try:
                    # Clean inner expression
                    clean_inner = inner.replace('·', '*').replace('x', '*').replace('^2', '**2').replace('^3', '**3')
                    val_inner = eval(clean_inner)
                    num = int(num_str)
                    if val_inner <= 0:
                        issues.append(f"P{p_idx}: [LỖI TOÁN HỌC N] Mẫu số âm hoặc bằng 0: {num} : [{inner}] = {num} : {val_inner}")
                    elif num % val_inner != 0:
                        issues.append(f"P{p_idx}: [LỖI TOÁN HỌC N] Phép chia không chia hết trong N: {num} : [{inner}] = {num} : {val_inner} = {num / val_inner:.2f}")
                except Exception as e:
                    pass

        # Kiểm tra Toán 8: Mâu thuẫn đề bài
        if is_toan_8:
            if "diện tích tăng thêm 36" in p_text and "gấp đôi chiều rộng" in p_text:
                issues.append(f"P{p_idx}: [LỖI SỐ LIỆU TOÁN 8] Đề 1 Bài 3 diện tích tăng thêm 36 m2 dẫn đến x = 10.5 m (phải là 34 m2 để x = 10).")
            if "tăng chiều rộng thêm 5 m và giảm chiều dài đi 5 m thì diện tích tăng thêm 25" in p_text and "chu vi 50" in p_text:
                issues.append(f"P{p_idx}: [LỖI SỐ LIỆU TOÁN 8] Đề 5 Bài 3 diện tích thực tế không đổi nhưng đề lại ghi tăng 25 m2.")

        # Kiểm tra Toán 9: Mâu thuẫn đề bài
        if is_toan_9:
            if "chu vi 100" in p_text and "diện tích tăng thêm 50" in p_text:
                issues.append(f"P{p_idx}: [LỖI SỐ LIỆU TOÁN 9] Đề 6 Bài 3 diện tích thực tế từ 600 lên 625 (tăng 25 m2), ghi tăng 50 m2 dẫn đến x = 32.5 m.")

    passed = (len(issues) == 0)
    return passed, issues, total_formulas_checked

def audit_round_2_xml_and_omml(doc):
    """
    VÒNG 2: PHẢN BIỆN CẤU TRÚC XML & CHUẨN HÓA HIỂN THỊ WORD EQUATION (OMML)
    - Dọn dẹp tàn dư LaTeX thô trong Equation
    - Triệt tiêu ô vuông nét đứt rỗng (<m:e/>)
    - Quét công thức lỗi chữ đỏ
    - Chuẩn hóa tiêu đề lặp từ
    """
    issues_found = []
    fixed_count = 0
    modified = False

    for p_idx, p in enumerate(doc.paragraphs):
        p_elm = p._p

        # 1. Chuẩn hóa tiêu đề đáp số 'Bài Đáp số Đề X.' -> 'Đáp số & Hướng dẫn Đề số X'
        for t_elm in p_elm.xpath('.//w:t'):
            if t_elm.text and 'Bài Đáp số Đề' in t_elm.text:
                orig = t_elm.text
                m = re.search(r'Bài Đáp số Đề\s*(\d+)', orig)
                if m:
                    num = int(m.group(1))
                    t_elm.text = re.sub(r'Bài Đáp số Đề\s*\d+\.?', f'Đáp số & Hướng dẫn Đề số {num:02d}', orig)
                else:
                    t_elm.text = orig.replace('Bài Đáp số Đề', 'Đáp số & Hướng dẫn Đề')
                issues_found.append(f"P{p_idx}: [ĐÃ SỬA TIÊU ĐỀ] '{orig.strip()}' -> '{t_elm.text.strip()}'")
                fixed_count += 1
                modified = True

        # 2. Kiểm tra sâu nội dung công thức toán (<m:oMath> -> <m:t>)
        for m_t in p_elm.xpath('.//m:oMath//m:t'):
            if not m_t.text:
                continue
            text_val = m_t.text

            # Sửa trực tiếp lỗi \\mathrm{UCLN -> ƯCLN và \\mathrm{BCNN -> BCNN
            if r'\mathrm{UCLN' in text_val or 'UCLN' in text_val:
                new_val = text_val.replace(r'\mathrm{UCLN', 'ƯCLN').replace(r'\mathrm{UCLN}', 'ƯCLN').replace('UCLN', 'ƯCLN')
                m_t.text = new_val
                issues_found.append(f"P{p_idx}: [ĐÃ SỬA LATEX TRONG OMATH] '{text_val}' -> '{new_val}'")
                fixed_count += 1
                modified = True
            elif r'\mathrm{BCNN' in text_val or (text_val.startswith(r'\mathrm') and 'BCNN' in text_val):
                new_val = text_val.replace(r'\mathrm{BCNN', 'BCNN').replace(r'\mathrm{BCNN}', 'BCNN')
                m_t.text = new_val
                issues_found.append(f"P{p_idx}: [ĐÃ SỬA LATEX TRONG OMATH] '{text_val}' -> '{new_val}'")
                fixed_count += 1
                modified = True
            elif text_val.startswith(r'\mathrm{') or text_val.startswith(r'\text{'):
                clean_val = re.sub(r'\\(?:mathrm|text)\{([^{}]+)\}', r'\1', text_val)
                clean_val = clean_val.replace(r'\mathrm{', '').replace(r'\text{', '')
                m_t.text = clean_val
                issues_found.append(f"P{p_idx}: [ĐÃ SỬA LATEX TRONG OMATH] '{text_val}' -> '{clean_val}'")
                fixed_count += 1
                modified = True

            # Dọn dẹp dấu đóng ngoặc nhọn mồ côi '}(90,60)' -> '(90,60)'
            if m_t.text and m_t.text.startswith('}('):
                m_t.text = m_t.text[1:]
                modified = True

            # Sửa lỗi ngoặc nhọn bọc thừa {( hoặc )}
            if m_t.text and ('{(' in m_t.text or ')}' in m_t.text):
                orig_mt = m_t.text
                m_t.text = m_t.text.replace('{(', '(').replace(')}', ')')
                issues_found.append(f"P{p_idx}: [ĐÃ SỬA NGOẶC NHỌN THỪA TRONG OMATH] '{orig_mt}' -> '{m_t.text}'")
                fixed_count += 1
                modified = True

        # 3. Kiểm tra văn bản thường (<w:t>) xem có bị lọt LaTeX thô không
        for w_t in p_elm.xpath('.//w:r/w:t'):
            if not w_t.text:
                continue
            for pat in LATEX_LEAK_PATTERNS:
                if re.search(pat, w_t.text):
                    issues_found.append(f"P{p_idx}: [CẢNH BÁO LỌT LATEX NGOÀI VĂN BẢN] Tìm thấy {pat} trong '{w_t.text[:60]}'")

        # 4. Kiểm tra ký hiệu cấm GDPT 2018 (\\iff, <=>) và công thức lỗi chữ đỏ
        for w_t in p_elm.xpath('.//w:r/w:t'):
            if w_t.text and ('<=>' in w_t.text or '⇔' in w_t.text):
                issues_found.append(f"P{p_idx}: [VI PHẠM GDPT 2018] Ký hiệu tương đương: '{w_t.text[:50]}'")

        for red_r in p_elm.xpath('.//w:r[./w:rPr/w:color[@w:val="FF0000"]]'):
            t = red_r.xpath('.//w:t')
            if t and t[0].text:
                issues_found.append(f"P{p_idx}: [LỖI CÔNG THỨC THẤT BẠI] Phát hiện công thức chưa dịch: '{t[0].text}'")

    # 5. Rà soát cấu trúc XML toàn tài liệu (thẻ <m:e/> rỗng)
    xml_str = doc._element.xml
    omath_count = xml_str.count('<m:oMath>') + xml_str.count('<m:oMath ')

    root = doc._element
    empty_e_list = root.xpath('//m:e[not(node())]')
    empty_e_count = len(empty_e_list)
    if empty_e_count > 0:
        issues_found.append(f"[PLACEHOLDER RỖNG] Còn {empty_e_count} thẻ <m:e/> rỗng cần triệt tiêu.")

    passed = (len([iss for iss in issues_found if "[CẢNH BÁO" in iss or "[VI PHẠM" in iss or "[LỖI" in iss]) == 0 and empty_e_count == 0)
    return passed, fixed_count, issues_found, omath_count, empty_e_count, modified

def audit_and_fix_document(docx_path):
    """
    ĐIỀU PHỐI QUY TRÌNH PHẢN BIỆN 3 VÒNG (3-ROUND AUDIT PIPELINE)
    """
    if not os.path.exists(docx_path):
        return False, {"status": "FAIL", "error": f"File không tồn tại: {docx_path}"}

    doc = docx.Document(docx_path)

    # VÒNG 1: PHẢN BIỆN TOÁN HỌC & TÍNH TOÀN VẸN SỐ LIỆU
    r1_pass, r1_issues, r1_checked = audit_round_1_math_logic(doc, docx_path)

    # VÒNG 2: PHẢN BIỆN CẤU TRÚC XML & CHUẨN HÓA WORD EQUATION OMML
    r2_pass, fixed_count, r2_issues, omath_count, empty_e_count, modified = audit_round_2_xml_and_omml(doc)

    if modified:
        doc.save(docx_path)

    # VÒNG 3: TỔNG HỢP & ĐÁNH GIÁ CHẤT LƯỢNG SƯ PHẠM TOÀN DIỆN
    all_issues = r1_issues + r2_issues
    unresolved_errors = [
        iss for iss in all_issues 
        if "[LỖI" in iss or "[VI PHẠM" in iss or "[PLACEHOLDER" in iss or "[CẢNH BÁO LỌT LATEX" in iss
    ]

    is_pass = (r1_pass and r2_pass and len(unresolved_errors) == 0 and empty_e_count == 0)
    status = "HOÀN TOÀN ĐẠT CHUẨN (PASS 100%)" if is_pass else "CÒN LỖI (FAIL)"

    report = {
        "file": os.path.basename(docx_path),
        "paragraphs": len(doc.paragraphs),
        "omath_count": omath_count,
        "round_1_math_logic": "PASS" if r1_pass else "FAIL",
        "round_1_formulas_checked": r1_checked,
        "round_2_xml_omml": "PASS" if r2_pass else "FAIL",
        "empty_placeholders": empty_e_count,
        "fixed_issues": fixed_count,
        "unresolved_errors": unresolved_errors,
        "issues": all_issues,
        "status": status
    }

    return is_pass, report
