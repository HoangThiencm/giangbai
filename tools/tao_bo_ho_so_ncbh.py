# -*- coding: utf-8 -*-
"""
TOOL TẠO TRỌN BỘ HỒ SƠ NGHIÊN CỨU BÀI HỌC (LESSON STUDY)
Chủ đề: Định lí Thalès trong tam giác - Toán 8 (Bài 15)
Đơn vị: Trường THCS Trần Phú - Tổ Toán – Tin
Tổ trưởng: Hoàng Tấn Thiên
Giáo viên dạy khối 8: Thầy Trần Long Hải, Cô Lê Thị Bình
Quy chuẩn: Công văn 5555/BGDĐT-GDTrH, Công văn 5512/BGDĐT-GDTrH, Nghị định 30/2020/NĐ-CP
"""

import os
import sys
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

OUTPUT_DIR = os.path.abspath("TROLYTHIEN/NCBH_DINH_LY_THALES_TOAN_8")
IMG_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_page_nd30(doc):
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

def make_header_block(doc, left_org, doc_num, right_title, date_str):
    """Tạo khối Quốc hiệu - Tiêu ngữ & Tên cơ quan ban hành chuẩn NĐ 30"""
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell_l = tbl.cell(0, 0)
    cell_r = tbl.cell(0, 1)
    cell_l.width = Inches(2.8)
    cell_r.width = Inches(3.7)
    
    set_cell_margins(cell_l, 0, 0, 0, 0)
    set_cell_margins(cell_r, 0, 0, 0, 0)
    
    # Left
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.1
    p_l.paragraph_format.space_after = Pt(2)
    for line in left_org:
        r = p_l.add_run(line + "\n")
        r.font.name = "Times New Roman"
        r.font.size = Pt(11.5)
        if "TRƯỜNG" in line or "TỔ" in line:
            r.bold = True
    r_num = p_l.add_run(doc_num)
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(11)
    
    # Right
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.1
    p_r.paragraph_format.space_after = Pt(2)
    r_qh1 = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r_qh1.bold = True
    r_qh1.font.name = "Times New Roman"
    r_qh1.font.size = Pt(11)
    r_qh2 = p_r.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r_qh2.bold = True
    r_qh2.font.name = "Times New Roman"
    r_qh2.font.size = Pt(12)
    r_date = p_r.add_run(date_str)
    r_date.italic = True
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_p(doc, text="", bold=False, italic=False, size=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3, line_spacing=1.2, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.name = "Times New Roman"
        r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor(*color)
    return p

def add_callout(doc, text, title="LƯU Ý TRỌNG TÂM:", border_color="16A34A", bg_color="F0FDF4"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=100)
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
    
    r_title = p.add_run(f"📌 {title} ")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(12.5)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    r_txt.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

print("Base helper initialized!")
