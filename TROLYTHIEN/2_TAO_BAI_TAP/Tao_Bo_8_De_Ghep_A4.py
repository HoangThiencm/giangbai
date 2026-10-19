# -*- coding: utf-8 -*-
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

import latex2mathml.commands
from latex2mathml.converter import convert as latex2mathml_convert
from lxml import etree
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT, WD_SECTION_START
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
import pymupdf

import sys
_engine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'engine'))
if _engine_dir not in sys.path:
    sys.path.insert(0, _engine_dir)
from de_cuong_docx_helper import latex_to_omml

def add_math_to_paragraph(p, latex_str):
    try:
        el = latex_to_omml(latex_str)
        if el is not None:
            p._element.append(el)
        else:
            p.add_run(f'${latex_str}$')
    except Exception as e:
        print(f"Error converting latex '{latex_str}': {e}")
        p.add_run(f'${latex_str}$')
def add_text_with_math(p, text, bold_prefix="", font_size=9.0, default_italic=False, line_spacing=1.05):
    p.paragraph_format.line_spacing = line_spacing
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.bold = True
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(font_size)
    
    pattern = re.compile(r'(\$[^$]+\$)')
    tokens = pattern.split(text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('$') and token.endswith('$') and len(token) > 1:
            latex = token[1:-1].strip()
            add_math_to_paragraph(p, latex)
        else:
            r = p.add_run(token)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            if default_italic:
                r.font.italic = True

def set_cell_margins(cell, top=20, bottom=20, left=40, right=40):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            </w:tblBorders>
        ''')
        tblPr[0].append(borders)

def render_exam(doc, exam, is_last_in_column=True, break_type=None):
    """
    Renders 1 complete exam into the current column.
    break_type: None, 'column', or 'page'
    """
    # 1. Header Table
    ht = doc.add_table(rows=1, cols=2)
    ht.alignment = WD_TABLE_ALIGNMENT.CENTER
    ht.autofit = False
    
    c_left = ht.cell(0, 0)
    c_right = ht.cell(0, 1)
    c_left.width = Inches(2.3)
    c_right.width = Inches(2.9)
    set_cell_margins(c_left, top=10, bottom=10, left=5, right=5)
    set_cell_margins(c_right, top=10, bottom=10, left=5, right=5)
    
    # Left Header
    p_hl = c_left.paragraphs[0]
    p_hl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hl.paragraph_format.line_spacing = 1.05
    p_hl.paragraph_format.space_before = Pt(0)
    p_hl.paragraph_format.space_after = Pt(0)
    r1 = p_hl.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r1.font.bold = True
    r1.font.size = Pt(8.5)
    r1.font.name = 'Times New Roman'
    r2 = p_hl.add_run("TỔ TOÁN - TIN HỌC")
    r2.font.bold = True
    r2.font.size = Pt(8.5)
    r2.font.name = 'Times New Roman'
    
    # Right Header
    p_hr = c_right.paragraphs[0]
    p_hr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hr.paragraph_format.line_spacing = 1.05
    p_hr.paragraph_format.space_before = Pt(0)
    p_hr.paragraph_format.space_after = Pt(0)
    r3 = p_hr.add_run(f"ĐỀ KIỂM TRA 15 PHÚT — {exam['title'].upper()}\n")
    r3.font.bold = True
    r3.font.size = Pt(9.5)
    r3.font.name = 'Times New Roman'
    r3.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    r4 = p_hr.add_run("Môn: Toán 9 — Năm học 2024-2025")
    r4.font.bold = True
    r4.font.size = Pt(8.5)
    r4.font.name = 'Times New Roman'
    
    # Student Info
    p_stu = doc.add_paragraph()
    p_stu.paragraph_format.line_spacing = 1.05
    p_stu.paragraph_format.space_before = Pt(2)
    p_stu.paragraph_format.space_after = Pt(2)
    r_s = p_stu.add_run("Họ và tên: ........................................... Lớp: 9.....  Điểm: ..........")
    r_s.font.size = Pt(9.0)
    r_s.font.name = 'Times New Roman'
    r_s.font.italic = True
    
    # PHẦN I
    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.line_spacing = 1.05
    p_s1.paragraph_format.space_before = Pt(2)
    p_s1.paragraph_format.space_after = Pt(1)
    r_p1 = p_s1.add_run("PHẦN I. CÂU HỎI TRẮC NGHIỆM (4,0 điểm)")
    r_p1.font.bold = True
    r_p1.font.size = Pt(9.5)
    r_p1.font.name = 'Times New Roman'
    r_p1.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    
    for q_idx, q in enumerate(exam['p1_questions']):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(1)
        p_q.paragraph_format.space_after = Pt(1)
        add_text_with_math(p_q, q['text'], bold_prefix=f"Câu {q_idx + 1}. ", font_size=9.0)
        
        opts = q['options']
        if q.get('layout') == 'grid2x2':
            t_opt = doc.add_table(rows=2, cols=2)
            t_opt.alignment = WD_TABLE_ALIGNMENT.CENTER
            t_opt.autofit = False
            for idx, (label, text) in enumerate(opts):
                cell = t_opt.cell(idx // 2, idx % 2)
                cell.width = Inches(2.6)
                set_cell_margins(cell, top=4, bottom=4, left=5, right=5)
                p_c = cell.paragraphs[0]
                p_c.paragraph_format.space_after = Pt(0)
                p_c.paragraph_format.space_before = Pt(0)
                add_text_with_math(p_c, text, bold_prefix=f"{label.strip()} ", font_size=9.0)
        else:
            t_opt = doc.add_table(rows=1, cols=4)
            t_opt.alignment = WD_TABLE_ALIGNMENT.CENTER
            t_opt.autofit = False
            for idx, (label, text) in enumerate(opts):
                cell = t_opt.cell(0, idx)
                cell.width = Inches(1.3)
                set_cell_margins(cell, top=4, bottom=4, left=5, right=5)
                p_c = cell.paragraphs[0]
                p_c.paragraph_format.space_after = Pt(0)
                p_c.paragraph_format.space_before = Pt(0)
                add_text_with_math(p_c, text, bold_prefix=f"{label.strip()}. ", font_size=9.0)
    
    # PHẦN II
    p_s2 = doc.add_paragraph()
    p_s2.paragraph_format.line_spacing = 1.05
    p_s2.paragraph_format.space_before = Pt(2)
    p_s2.paragraph_format.space_after = Pt(1)
    r_p2 = p_s2.add_run("PHẦN II. CÂU TRẮC NGHIỆM ĐÚNG SAI (3,0 điểm)")
    r_p2.font.bold = True
    r_p2.font.size = Pt(9.5)
    r_p2.font.name = 'Times New Roman'
    r_p2.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    
    p_p2 = doc.add_paragraph()
    p_p2.paragraph_format.space_before = Pt(0)
    p_p2.paragraph_format.space_after = Pt(1)
    add_text_with_math(p_p2, exam['p2_intro'], bold_prefix="Câu 1. ", font_size=9.0)
    
    for label, text in exam['p2_items']:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.left_indent = Inches(0.12)
        p_it.paragraph_format.space_before = Pt(0)
        p_it.paragraph_format.space_after = Pt(1)
        add_text_with_math(p_it, text, bold_prefix=f"{label.strip()} ", font_size=9.0)
        
    # PHẦN III
    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.line_spacing = 1.05
    p_s3.paragraph_format.space_before = Pt(2)
    p_s3.paragraph_format.space_after = Pt(1)
    r_p3 = p_s3.add_run("PHẦN III. CÂU TRẢ LỜI NGẮN (3,0 điểm)")
    r_p3.font.bold = True
    r_p3.font.size = Pt(9.5)
    r_p3.font.name = 'Times New Roman'
    r_p3.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    
    # Q3.1
    p31 = doc.add_paragraph()
    p31.paragraph_format.space_before = Pt(0)
    p31.paragraph_format.space_after = Pt(1)
    add_text_with_math(p31, exam['p3_q1_text'] + "\nTrả lời: ........................................................................................", bold_prefix="Câu 1. ", font_size=9.0)
    
    # Q3.2
    p32 = doc.add_paragraph()
    p32.paragraph_format.space_before = Pt(0)
    p32.paragraph_format.space_after = Pt(1)
    add_text_with_math(p32, exam['p3_q2_text'] + "\nTrả lời: ........................................................................................", bold_prefix="Câu 2. ", font_size=9.0)
    
    # Footer end
    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_end.paragraph_format.space_before = Pt(1)
    p_end.paragraph_format.space_after = Pt(0)
    r_end = p_end.add_run("---------- HẾT ----------")
    r_end.font.size = Pt(8.0)
    r_end.font.italic = True
    r_end.font.color.rgb = RGBColor(0x6b, 0x72, 0x80)
    
    if break_type == 'column':
        r_end.add_break(WD_BREAK.COLUMN)
    elif break_type == 'page':
        r_end.add_break(WD_BREAK.PAGE)

# Define e1
e1 = {
    'title': 'Đề số 01',
    'p1_questions': [
        {
            'text': 'Cặp số nào sau đây là nghiệm của hệ phương trình $\\begin{cases} 2x - y = 3 \\\\ x + y = 6 \\end{cases}$?',
            'options': [('A', '$(3; 3)$'), ('B', '$(2; 1)$'), ('C', '$(4; 2)$'), ('D', '$(1; 5)$')],
            'layout': '1x4'
        },
        {
            'text': 'Nghiệm của hệ phương trình $\\begin{cases} 3x + 2y = 8 \\\\ 2x - y = 3 \\end{cases}$ là:',
            'options': [('A', '$(x; y) = (2; 1)$'), ('B', '$(x; y) = (1; 2)$'), ('C', '$(x; y) = (0; 4)$'), ('D', '$(x; y) = (3; 3)$')],
            'layout': '1x4'
        },
        {
            'text': 'Nghiệm của hệ phương trình $\\begin{cases} x - 2y = -5 \\\\ 2x + y = 5 \\end{cases}$ là:',
            'options': [('A', '$(x; y) = (1; 3)$'), ('B', '$(x; y) = (3; 1)$'), ('C', '$(x; y) = (-1; 2)$'), ('D', '$(x; y) = (2; 1)$')],
            'layout': '1x4'
        },
        {
            'text': 'Cặp số $(-1; 2)$ là nghiệm của hệ phương trình nào sau đây?',
            'options': [
                ('A. ', '$\\begin{cases} 2x + 3y = 4 \\\\ x - y = -3 \\end{cases}$'),
                ('B. ', '$\\begin{cases} x + y = 3 \\\\ 2x - y = 0 \\end{cases}$'),
                ('C. ', '$\\begin{cases} 3x - y = 1 \\\\ x + 2y = 5 \\end{cases}$'),
                ('D. ', '$\\begin{cases} 2x - y = 4 \\\\ x + y = 1 \\end{cases}$')
            ],
            'layout': 'grid2x2'
        }
    ],
    'p1_answers': ['A', 'A', 'A', 'A'],
    'p2_intro': 'Cho hệ phương trình: $\\begin{cases} 2x - y = 1 \\quad (1) \\\\ x + 2y = 8 \\quad (2) \\end{cases}$.',
    'p2_items': [
        ('a) ', 'Từ phương trình (1), biểu diễn $y$ theo $x$ ta được hệ thức $y = 2x - 1$.'),
        ('b) ', 'Nghiệm duy nhất của hệ phương trình đã cho là cặp số $(x_0; y_0) = (2; 3)$.'),
        ('c) ', 'Giá trị của biểu thức $P = x_0^2 + y_0^2$ bằng $15$.'),
        ('d) ', 'Giá trị của tham số $m$ để phương trình $mx + 3y = 13$ nhận cặp số $(x_0; y_0)$ làm nghiệm là $m = 2$.')
    ],
    'p2_answers': ['ĐÚNG', 'ĐÚNG', 'SAI', 'ĐÚNG'],
    'p3_q1_text': 'Cho hệ phương trình: $\\begin{cases} 2x + y = 5m - 1 \\\\ x - 2y = 2 \\end{cases}$ (với $m$ là tham số). Tìm giá trị của $m$ để hệ phương trình có nghiệm duy nhất $(x_0; y_0)$ thỏa mãn đẳng thức $x_0 + 3y_0 = 12$.',
    'p3_q2_text': 'Cho hệ phương trình: $\\begin{cases} \\frac{1}{x} + \\frac{1}{y} = \\frac{3}{2} \\\\ \\frac{2}{x} - \\frac{1}{y} = 0 \\end{cases}$. Biết cặp số $(x_0; y_0)$ là nghiệm duy nhất của hệ phương trình đã cho. Giá trị của tổng $x_0 + y_0$ bằng bao nhiêu?',
    'p3_answers': [3, 3]
}

# Load other exams from scratch_all_exams
from scratch_all_exams import e2, e3, e4, e5, e6, e7, e8

exams = [e1, e2, e3, e4, e5, e6, e7, e8]
pairs = [
    (exams[0], exams[1]), # Tờ 1: Đề 1 & Đề 2
    (exams[2], exams[3]), # Tờ 2: Đề 3 & Đề 4
    (exams[4], exams[5]), # Tờ 3: Đề 5 & Đề 6
    (exams[6], exams[7]), # Tờ 4: Đề 7 & Đề 8
]

doc = docx.Document()

# Section 1: 2-column Landscape for the 4 paired exam sheets
sec1 = doc.sections[0]
sec1.orientation = WD_ORIENT.LANDSCAPE
sec1.page_width = Inches(11.69)
sec1.page_height = Inches(8.27)
sec1.top_margin = Inches(0.35)
sec1.bottom_margin = Inches(0.35)
sec1.left_margin = Inches(0.4)
sec1.right_margin = Inches(0.4)

sectPr = sec1._sectPr
cols = sectPr.xpath('./w:cols')
if cols:
    cols[0].set(qn('w:num'), '2')
    cols[0].set(qn('w:space'), '576') # 0.4 in gap
    cols[0].set(qn('w:sep'), '1')     # Vertical cut line
else:
    cols_xml = parse_xml(f'<w:cols {nsdecls("w")} w:num="2" w:space="576" w:sep="1"/>')
    sectPr.append(cols_xml)

for p_idx, (ex_left, ex_right) in enumerate(pairs):
    # Left column: Column break at end
    render_exam(doc, ex_left, is_last_in_column=True, break_type='column')
    
    # Right column: Page break at end if not last pair
    if p_idx < len(pairs) - 1:
        render_exam(doc, ex_right, is_last_in_column=True, break_type='page')
    else:
        render_exam(doc, ex_right, is_last_in_column=True, break_type=None)

# ==============================================================================
# Section 2: Answer Key Page for Teacher (Full width 1-column Landscape)
# ==============================================================================
sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
sec2.orientation = WD_ORIENT.LANDSCAPE
sec2.page_width = Inches(11.69)
sec2.page_height = Inches(8.27)
sec2.top_margin = Inches(0.5)
sec2.bottom_margin = Inches(0.5)
sec2.left_margin = Inches(0.6)
sec2.right_margin = Inches(0.6)

# Set 1 column for section 2
sectPr2 = sec2._sectPr
cols2 = sectPr2.xpath('./w:cols')
if cols2:
    cols2[0].set(qn('w:num'), '1')
    cols2[0].set(qn('w:sep'), '0')
else:
    cols_xml2 = parse_xml(f'<w:cols {nsdecls("w")} w:num="1" w:sep="0"/>')
    sectPr2.append(cols_xml2)

p_ak = doc.add_paragraph()
p_ak.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ak.paragraph_format.space_before = Pt(4)
p_ak.paragraph_format.space_after = Pt(2)
r_title = p_ak.add_run("BẢNG ĐÁP ÁN TỔNG HỢP VÀ THANG ĐIỂM CHẤM THI — 8 MÃ ĐỀ\n")
r_title.font.bold = True
r_title.font.size = Pt(13)
r_title.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
r_sub = p_ak.add_run("MÔN: TOÁN 9 — BÀI 2: GIẢI HỆ HAI PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN (THỜI GIAN: 15 PHÚT)")
r_sub.font.bold = True
r_sub.font.size = Pt(10.5)

p_desc = doc.add_paragraph()
p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_desc.paragraph_format.space_after = Pt(8)
r_d = p_desc.add_run("(Dành riêng cho Giáo viên — Quy cách in: In 5 bản của 4 trang đề A4, cắt đôi theo đường kẻ dọc giữa để phát cho 40 học sinh)")
r_d.font.italic = True
r_d.font.size = Pt(9.5)
r_d.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)

# Master Table: Rows = Questions, Cols = Exams (Col 0: Question Name, Cols 1..8: Exam 1..8)
rows_data = [
    # Header
    ["Phần thi / Câu hỏi", "Đề 01", "Đề 02", "Đề 03", "Đề 04", "Đề 05", "Đề 06", "Đề 07", "Đề 08"],
    # Phần I (4 câu)
    ["Phần I - Câu 1 (1,0đ)", exams[0]['p1_answers'][0], exams[1]['p1_answers'][0], exams[2]['p1_answers'][0], exams[3]['p1_answers'][0], exams[4]['p1_answers'][0], exams[5]['p1_answers'][0], exams[6]['p1_answers'][0], exams[7]['p1_answers'][0]],
    ["Phần I - Câu 2 (1,0đ)", exams[0]['p1_answers'][1], exams[1]['p1_answers'][1], exams[2]['p1_answers'][1], exams[3]['p1_answers'][1], exams[4]['p1_answers'][1], exams[5]['p1_answers'][1], exams[6]['p1_answers'][1], exams[7]['p1_answers'][1]],
    ["Phần I - Câu 3 (1,0đ)", exams[0]['p1_answers'][2], exams[1]['p1_answers'][2], exams[2]['p1_answers'][2], exams[3]['p1_answers'][2], exams[4]['p1_answers'][2], exams[5]['p1_answers'][2], exams[6]['p1_answers'][2], exams[7]['p1_answers'][2]],
    ["Phần I - Câu 4 (1,0đ)", exams[0]['p1_answers'][3], exams[1]['p1_answers'][3], exams[2]['p1_answers'][3], exams[3]['p1_answers'][3], exams[4]['p1_answers'][3], exams[5]['p1_answers'][3], exams[6]['p1_answers'][3], exams[7]['p1_answers'][3]],
    # Phần II (4 ý)
    ["Phần II - Ý a (0,3đ)", exams[0]['p2_answers'][0], exams[1]['p2_answers'][0], exams[2]['p2_answers'][0], exams[3]['p2_answers'][0], exams[4]['p2_answers'][0], exams[5]['p2_answers'][0], exams[6]['p2_answers'][0], exams[7]['p2_answers'][0]],
    ["Phần II - Ý b (0,75đ)", exams[0]['p2_answers'][1], exams[1]['p2_answers'][1], exams[2]['p2_answers'][1], exams[3]['p2_answers'][1], exams[4]['p2_answers'][1], exams[5]['p2_answers'][1], exams[6]['p2_answers'][1], exams[7]['p2_answers'][1]],
    ["Phần II - Ý c (1,5đ)", exams[0]['p2_answers'][2], exams[1]['p2_answers'][2], exams[2]['p2_answers'][2], exams[3]['p2_answers'][2], exams[4]['p2_answers'][2], exams[5]['p2_answers'][2], exams[6]['p2_answers'][2], exams[7]['p2_answers'][2]],
    ["Phần II - Ý d (3,0đ)", exams[0]['p2_answers'][3], exams[1]['p2_answers'][3], exams[2]['p2_answers'][3], exams[3]['p2_answers'][3], exams[4]['p2_answers'][3], exams[5]['p2_answers'][3], exams[6]['p2_answers'][3], exams[7]['p2_answers'][3]],
    # Phần III (2 câu)
    ["Phần III - Câu 1 (1,5đ)", str(exams[0]['p3_answers'][0]), str(exams[1]['p3_answers'][0]), str(exams[2]['p3_answers'][0]), str(exams[3]['p3_answers'][0]), str(exams[4]['p3_answers'][0]), str(exams[5]['p3_answers'][0]), str(exams[6]['p3_answers'][0]), str(exams[7]['p3_answers'][0])],
    ["Phần III - Câu 2 (1,5đ)", str(exams[0]['p3_answers'][1]), str(exams[1]['p3_answers'][1]), str(exams[2]['p3_answers'][1]), str(exams[3]['p3_answers'][1]), str(exams[4]['p3_answers'][1]), str(exams[5]['p3_answers'][1]), str(exams[6]['p3_answers'][1]), str(exams[7]['p3_answers'][1])]
]

t_ak = doc.add_table(rows=len(rows_data), cols=9)
t_ak.alignment = WD_TABLE_ALIGNMENT.CENTER
t_ak.autofit = False
set_table_borders(t_ak, color="9CA3AF", sz="6")

col_widths = [Inches(2.5)] + [Inches(1.0)] * 8

for r_idx, row_values in enumerate(rows_data):
    row = t_ak.rows[r_idx]
    is_header = (r_idx == 0)
    bg_color = "1E3A8A" if is_header else ("F3F4F6" if r_idx % 2 == 1 else "FFFFFF")
    
    for c_idx, val in enumerate(row_values):
        cell = row.cells[c_idx]
        cell.width = col_widths[c_idx]
        set_cell_margins(cell, top=30, bottom=30, left=40, right=40)
        set_cell_background(cell, bg_color)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        if c_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
        r = p.add_run(val)
        r.font.name = 'Times New Roman'
        if is_header:
            r.font.bold = True
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)
        else:
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.font.bold = True
            else:
                if val in ['A', 'B', 'C', 'D']:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0x1d, 0x4e, 0xd8)
                elif val == 'ĐÚNG':
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0x15, 0x80, 0x3d)
                elif val == 'SAI':
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0xb9, 0x1c, 0x1c)
                else:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0x7c, 0x2d, 0x12)

# Guide note
p_note = doc.add_paragraph()
p_note.paragraph_format.space_before = Pt(8)
r_n1 = p_note.add_run("Quy định tính điểm Phần II (Câu trắc nghiệm Đúng/Sai - Tối đa 3,0 điểm):\n")
r_n1.font.bold = True
r_n1.font.size = Pt(9.0)
r_n2 = p_note.add_run("- Đúng 1 ý: 0,3 điểm   |   - Đúng 2 ý: 0,75 điểm   |   - Đúng 3 ý: 1,5 điểm   |   - Đúng cả 4 ý: 3,0 điểm.")
r_n2.font.italic = True
r_n2.font.size = Pt(9.0)

# Save document
out_docx = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\2_TAO_BAI_TAP\Ket_qua\Bo_8_De_Toan9_Ghep_A4_In_Tiet_Kiem.docx"
doc.save(out_docx)
print("Saved Master Paired Word Document:", out_docx)
