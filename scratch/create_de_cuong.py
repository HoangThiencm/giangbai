# -*- coding: utf-8 -*-
"""
TẠO ĐỀ CƯƠNG ÔN TẬP GIỮA HỌC KỲ I (TOÁN 6, 8, 9)
DỰA 100% VÀO PHÂN PHỐI CHƯƠNG TRÌNH (PHỤ LỤC 3) CỦA TRƯỜNG THCS TRẦN PHÚ
TUYỆT ĐỐI KHÔNG DÙNG MA TRẬN / BẢN ĐẶC TẢ CŨ
ÁP DỤNG QUY CHUẨN SƯ PHẠM TÔN THÂN - VŨ HỮU BÌNH
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_DIR = r"TROLYTHIEN\2_TAO_BAI_TAP\Ket_qua"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def format_run(run, font_name="Times New Roman", size_pt=13, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_header(doc, title, subtitle):
    # Header table 2 columns
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell_l, cell_r = table.rows[0].cells
    cell_l.width = Inches(3.2)
    cell_r.width = Inches(3.8)
    
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_l.add_run("PHÒNG GD&ĐT HUYỆN CẨM MỸ\nTRƯỜNG THCS TRẦN PHÚ\n")
    format_run(r1, size_pt=11, bold=True)
    r2 = p_l.add_run("TỔ TOÁN - TIN\n─────────")
    format_run(r2, size_pt=11, bold=True)
    
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n")
    format_run(r3, size_pt=11, bold=True)
    r4 = p_r.add_run("─────────────────")
    format_run(r4, size_pt=11, bold=True)
    
    doc.add_paragraph()
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run(title + "\n")
    format_run(r_t, size_pt=15, bold=True, color_rgb=(15, 23, 42))
    r_sub = p_title.add_run(subtitle)
    format_run(r_sub, size_pt=12, italic=True, color_rgb=(71, 85, 105))
    
    doc.add_paragraph()

print("Script template ready.")
