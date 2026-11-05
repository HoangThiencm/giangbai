# -*- coding: utf-8 -*-
import os, sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

sys.stdout.reconfigure(encoding='utf-8')

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

def add_section_h1(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    format_run(r, size_pt=14, bold=True, color_rgb=(30, 58, 138))
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)

def add_section_h2(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    format_run(r, size_pt=13, bold=True, color_rgb=(180, 83, 9))
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + " ")
        format_run(r_pre, size_pt=12.5, bold=True)
    r = p.add_run(text)
    format_run(r, size_pt=12.5)

def add_exercise(doc, num_str, content):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_num = p.add_run(f"Bài {num_str}: ")
    format_run(r_num, size_pt=12.5, bold=True, color_rgb=(15, 23, 42))
    r_cnt = p.add_run(content)
    format_run(r_cnt, size_pt=12.5)

print("Base helper loaded.")
