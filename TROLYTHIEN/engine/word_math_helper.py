# -*- coding: utf-8 -*-
"""
TROLYTHIEN — UNIVERSAL WORD EQUATION & MATH HELPER
Module chuẩn hóa tạo công thức toán học Microsoft Word Equation (OMML m:oMath)
Áp dụng cho TOÀN BỘ 14 PHÂN MỤC của Trợ lý Sư phạm Hoàng Thiên.

ĐẶC BIỆT LƯU Ý CHO TẤT CẢ AGENT:
- Tuyệt đối KHÔNG xuất công thức toán dạng text Unicode thô: cấm (x+y)/4, x⁴y², góc M = 100°!
- Bắt buộc dùng add_text_with_math() hoặc latex_to_omml() từ module này.
"""

import os
import sys
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.path.append(os.path.dirname(__file__))
from de_cuong_docx_helper import latex_to_omml, add_text_with_math

def format_run(run, font_name="Times New Roman", size_pt=11.5, bold=False, italic=False, color_rgb=(0, 0, 0)):
    """Định dạng phông chữ cho text run chuẩn sư phạm."""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_math_paragraph(container, text, bold_prefix=None, size_pt=11.5, bold=False, italic=False, space_after=3, line_spacing=1.15):
    """
    Tạo một paragraph Word mới, tự động nhận diện các công thức toán kẹp giữa $...$
    và chuyển hóa 100% sang Microsoft Word Equation (OMML m:oMath).
    """
    p = container.add_paragraph()
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(space_after)

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        format_run(r_pre, size_pt=size_pt, bold=True)

    add_text_with_math(p, text, default_size_pt=size_pt, bold=bold, italic=italic)
    return p

def add_multiline_math(container, text, bold_prefix=None, size_pt=11.5, space_after=3):
    """Xử lý văn bản nhiều dòng (\n), mỗi dòng tự động nhận diện Equation $...$."""
    lines = text.strip().split('\n')
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        prefix = bold_prefix if idx == 0 else ""
        add_math_paragraph(container, line, bold_prefix=prefix, size_pt=size_pt, space_after=2)

def set_cell_shading(cell, color_hex="F2F2F2"):
    """Đổ màu nền xám nhẹ trang trọng cho ô bảng Word (thường dùng cho header Cột A / Cột B)."""
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_table_no_borders(table):
    """Xóa toàn bộ viền bảng (thường dùng cho bảng chứa ảnh song song)."""
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)
