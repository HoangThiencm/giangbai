# -*- coding: utf-8 -*-
"""
MODULE TEMPLATE & ENGINE DUYỆT GIÁO ÁN — TRỢ LÝ SƯ PHẠM HOÀNG THIÊN
Phiên bản: VERSION 2.0.0 (BẢN VÁ KỶ LUẬT CHUYÊN MÔN & ZERO TOLERANCE)
Quy chuẩn: Công văn 5512/BGDĐT-GDTrH & Nghị định 30/2020/NĐ-CP & Quy chế THCS Trần Phú

QUY TẮC THÉP TRẢ HỒ SƠ (ZERO TOLERANCE):
1. SAI QUY CHẾ CHUYÊN MÔN: NLS/AI không in đậm, nghiêng; thiếu tiết; sai PL3 -> TRẢ HỒ SƠ 100%.
2. SAI CÔNG THỨC KÝ HIỆU: Lỗi font góc, mất dấu mũ góc, đè ký tự rác -> TRẢ HỒ SƠ 100%.
3. SAI VỀ NỘI DUNG: Sai định lý, nhầm dấu, sai chuyển vế, sai toán học -> TRẢ HỒ SƠ 100%.
TUYỆT ĐỐI KHÔNG DUYỆT NƯƠNG TAY (KỂ CẢ XẾP LOẠI KHÁ)!
"""

import os
import sys
import re
import pymupdf as fitz
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

VERSION = "2.0.0"

# ==============================================================================
# 1. HỆ THỐNG TRẠNG THÁI & MÃ MÀU CHUẨN MỰC
# ==============================================================================

STATUS_DUYET_TOT = "DUYỆT (Xếp loại: Tốt)"
STATUS_DUYET_KHA = "DUYỆT (Xếp loại: Khá)"
STATUS_TRA_HO_SO = "TRẢ HỒ SƠ"

# Mã màu nhận diện chuẩn
COLOR_SUCCESS = (22, 163, 74)   # Xanh lá cây (Đạt / Duyệt)
COLOR_WARNING = (217, 119, 6)   # Vàng cam (Lưu ý nhỏ thể thức)
COLOR_DANGER = (220, 38, 38)    # Đỏ tươi (Trả hồ sơ)

HEX_SUCCESS_BG = "F0FDF4"
HEX_SUCCESS_BORDER = "16A34A"
HEX_DANGER_BG = "FEF2F2"
HEX_DANGER_BORDER = "DC2626"

# Ký tự rác font toán học MathType / Word Equation cần quét phát hiện
SUSPICIOUS_CHARS = [
    0x0307, 0x0308, # combining dot above (tạo lỗi dấu chấm đè: ẋ, ẏ, ṁ, Ṁ...)
    0x0227, 0x1e41, 0x1e8b, 0x1e8f, # chữ có chấm trên
    0x22a5,         # dấu perpendicular ⊥ đè lên đỉnh góc
    0x00b5,         # ký tự micro µ (lỗi font µ A)
]

# ==============================================================================
# 2. CÔNG CỤ RÀ SOÁT TỰ ĐỘNG (AUDIT ENGINE V2.0 - ZERO TOLERANCE)
# ==============================================================================

def scan_pdf_deep(pdf_path, required_nls_codes=None):
    """
    Quét tự động tệp PDF giáo án theo tiêu chuẩn Version 2.0:
    1. Quét lỗi font công thức & ký hiệu góc biến dạng.
    2. Quét định dạng in đậm, nghiêng (bold italic) của NLS/AI.
    3. Đánh giá và trả về quyết định tự động: PASS hoặc REJECT.
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    math_errors = []
    nls_findings = []
    
    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text()
        
        # 1. Quét lỗi font ký hiệu góc và công thức
        for line in text.splitlines():
            line_s = line.strip()
            # Bắt dấu chấm trên đầu chữ cái
            for ch in line_s:
                if ord(ch) in SUSPICIOUS_CHARS:
                    math_errors.append({
                        "page": page_num + 1,
                        "line": line_s,
                        "type": "LỖI FONT CÔNG THỨC / KÝ HIỆU GÓC",
                        "detail": f"Ký tự bất thường '{ch}' (U+{ord(ch):04X}) gây biến dạng ký hiệu."
                    })
                    break
            # Bắt lỗi font đè ký tự perpendicular lên đỉnh góc: [A-Z]⊥ hoặc micro µ A
            if re.search(r'(?<![A-Za-z])[A-Z]\u22a5|\u00b5\s*[A-Z]', line_s):
                bad_matches = re.findall(r'(?<![A-Za-z])[A-Z]\u22a5|\u00b5\s*[A-Z]', line_s)
                if bad_matches:
                    math_errors.append({
                        "page": page_num + 1,
                        "line": line_s,
                        "type": "LỖI FONT CÔNG THỨC / KÝ HIỆU GÓC",
                        "detail": f"Ký hiệu góc bị đè ký tự rác: {bad_matches}"
                    })
                    
        # 2. Quét spans để kiểm tra font style NLS / AI
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    line_spans = l["spans"]
                    full_line_text = "".join([s["text"] for s in line_spans]).strip()
                    
                    if any(k in full_line_text.lower() for k in ["nls", "năng lực số", "ai:", "năng lực ai", "tc1a", "tc1b", "tc2a", "tc2b"]):
                        is_all_bi = all(
                            (bool(s["flags"] & 16 or "bold" in s["font"].lower()) and 
                             bool(s["flags"] & 2 or "italic" in s["font"].lower() or "oblique" in s["font"].lower()))
                            for s in line_spans if s["text"].strip()
                        )
                        nls_findings.append({
                            "page": page_num + 1,
                            "text": full_line_text,
                            "is_bold_italic": is_all_bi
                        })
                        
    # 3. Đánh giá Zero Tolerance
    nls_unformatted = [n for n in nls_findings if not n["is_bold_italic"]]
    
    has_math_error = len(math_errors) > 0
    has_nls_format_error = len(nls_unformatted) > 0
    
    if has_math_error or has_nls_format_error:
        final_verdict = STATUS_TRA_HO_SO
    else:
        final_verdict = STATUS_DUYET_TOT
        
    return {
        "pages": total_pages,
        "math_errors": math_errors,
        "nls_findings": nls_findings,
        "nls_unformatted": nls_unformatted,
        "has_math_error": has_math_error,
        "has_nls_format_error": has_nls_format_error,
        "final_verdict": final_verdict
    }

# ==============================================================================
# 3. HELPER ĐỊNH DẠNG THEO NGHỊ ĐỊNH 30/2020/NĐ-CP
# ==============================================================================

def apply_page_setup_nd30(doc):
    """Thiết lập lề trang A4 chuẩn Nghị định 30/2020/NĐ-CP"""
    for s in doc.sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(0.79)      # 20 mm
        s.bottom_margin = Inches(0.79)   # 20 mm
        s.left_margin = Inches(1.18)     # 30 mm
        s.right_margin = Inches(0.59)    # 15 mm
        s.different_first_page_header_footer = False

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders_nd30(table, color="000000", sz="4", val="single"):
    """Đóng khung kín 4 cạnh viền ngoài và các đường chia ô chuẩn NĐ 30"""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout(doc, text, title="KẾT LUẬN & XẾP LOẠI:", border_color="16A34A", bg_color="F0FDF4"):
    """Tạo ô callout kết luận có viền trái nổi bật"""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=140)
    set_cell_background(cell, bg_color)
    
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    
    r_title = p.add_run(f"👉 {title} ")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(13)
    r_title.font.color.rgb = RGBColor(15, 23, 42) if border_color != "DC2626" else RGBColor(185, 28, 28)
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(13)
    r_txt.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def safe_save_doc(doc, target_path):
    """Lưu tệp an toàn, tránh lỗi PermissionError khi Word đang mở"""
    try:
        doc.save(target_path)
        print("Đã lưu thành công:", target_path)
        return target_path
    except PermissionError:
        base, ext = os.path.splitext(target_path)
        fallback_path = f"{base}_CapNhat{ext}"
        doc.save(fallback_path)
        print(f"Tệp bị khóa. Đã lưu sang: {fallback_path}")
        return fallback_path

print(f"Module template_duyet_giao_an v{VERSION} (Zero Tolerance) loaded successfully!")
