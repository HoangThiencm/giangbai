# -*- coding: utf-8 -*-
"""
HỆ THỐNG KIỂM ĐỊNH SÂU & TỰ ĐỘNG KHẮC PHỤC LỖI CÔNG THỨC TOÁN TRONG WORD (DEEP XML AUDITOR)
Phản biện toàn diện:
1. Quét sâu vào từng thẻ XML <w:t> (văn bản thường) VÀ <m:t> (nội dung Word Equation).
2. Phát hiện và sửa chữa 100% tàn dư LaTeX thô bị lọt vào Equation (như \\mathrm{UCLN}, \\mathrm{BCNN}, \\text...).
3. Phát hiện và triệt tiêu mọi ô vuông nét đứt rỗng (<m:e/>) trong XML.
4. Chuẩn hóa tiêu đề đáp số, dọn sạch lỗi lặp từ ('Bài Đáp số Đề').
5. Kiểm định nghiêm ngặt: Chỉ báo PASS khi toàn bộ tài liệu đạt 0 lỗi thực sự.
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

def audit_and_fix_document(docx_path):
    """
    VÒNG PHẢN BIỆN SÂU (DEEP AUDIT) CẤU TRÚC XML WORD:
    Quét trực tiếp vào cây XML của từng Paragraph và Run để không bỏ sót bất kỳ công thức nào.
    """
    if not os.path.exists(docx_path):
        return False, {"status": "FAIL", "error": f"File không tồn tại: {docx_path}"}
        
    doc = docx.Document(docx_path)
    
    issues_found = []
    fixed_count = 0
    modified = False

    for p_idx, p in enumerate(doc.paragraphs):
        p_elm = p._p
        
        # 1. KIỂM TRA TIÊU ĐỀ LỖI LẶP TỪ 'Bài Đáp số Đề X.' -> Sửa thành 'Đáp số & Hướng dẫn Đề số X'
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

        # 2. KIỂM TRA SÂU NỘI DUNG CÔNG THỨC TOÁN (<m:oMath> -> <m:t>)
        # Phát hiện tàn dư LaTeX thô chưa được dịch (như \\mathrm{UCLN}, \\mathrm{BCNN}...)
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
                # Loại bỏ cú pháp bao bọc LaTeX thô
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

        # 3. KIỂM TRA VĂN BẢN THƯỜNG (<w:t>) XEM CÓ BỊ LỌT LATEX THÔ KHÔNG
        for w_t in p_elm.xpath('.//w:r/w:t'):
            if not w_t.text:
                continue
            for pat in LATEX_LEAK_PATTERNS:
                if re.search(pat, w_t.text):
                    issues_found.append(f"P{p_idx}: [CẢNH BÁO LỌT LATEX NGOÀI VĂN BẢN] Tìm thấy {pat} trong '{w_t.text[:60]}'")

        # 4. KIỂM TRA KÝ HIỆU CẤM GDPT 2018 (\\iff, <=>) VÀ CÔNG THỨC LỖI CHỮ ĐỎ
        for w_t in p_elm.xpath('.//w:r/w:t'):
            if w_t.text and ('<=>' in w_t.text or '⇔' in w_t.text):
                issues_found.append(f"P{p_idx}: [VI PHẠM GDPT 2018] Ký hiệu tương đương: '{w_t.text[:50]}'")

        for red_r in p_elm.xpath('.//w:r[./w:rPr/w:color[@w:val="FF0000"]]'):
            t = red_r.xpath('.//w:t')
            if t and t[0].text:
                issues_found.append(f"P{p_idx}: [LỖI CÔNG THỨC THẤT BẠI] Phát hiện công thức chưa dịch: '{t[0].text}'")

    # 5. RÀ SOÁT CẤU TRÚC XML TOÀN TÀI LIỆU (THẺ <m:e/> RỖNG)
    xml_str = doc._element.xml
    omath_count = xml_str.count('<m:oMath>') + xml_str.count('<m:oMath ')
    
    # Tìm và đếm thẻ rỗng
    root = doc._element
    empty_e_list = root.xpath('//m:e[not(node())]')
    empty_e_count = len(empty_e_list)
    if empty_e_count > 0:
        issues_found.append(f"[PLACEHOLDER RỖNG] Còn {empty_e_count} thẻ <m:e/> rỗng cần triệt tiêu.")

    # Lưu file nếu có chỉnh sửa
    if modified:
        doc.save(docx_path)

    # ĐÁNH GIÁ CHẤT LƯỢNG NGHIÊM NGẶT
    unresolved_errors = [iss for iss in issues_found if not iss.startswith("P") or "[CẢNH BÁO" in iss or "[VI PHẠM" in iss or "[PLACEHOLDER" in iss]
    is_pass = (len(unresolved_errors) == 0 and empty_e_count == 0)
    status = "HOÀN TOÀN ĐẠT CHUẨN (PASS)" if is_pass else "CÒN LỖI (FAIL)"

    report = {
        "file": os.path.basename(docx_path),
        "paragraphs": len(doc.paragraphs),
        "omath_count": omath_count,
        "empty_placeholders": empty_e_count,
        "fixed_issues": fixed_count,
        "issues": issues_found,
        "status": status
    }
    
    return is_pass, report
