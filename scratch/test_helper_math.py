# -*- coding: utf-8 -*-
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import parse_xml
import latex2mathml.commands
from latex2mathml.converter import convert
import lxml.etree as ET

XSLT_PATH = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"
_xslt_doc = ET.parse(XSLT_PATH)
_transform = ET.XSLT(_xslt_doc)

def latex_to_omml(latex_code):
    try:
        mathml = convert(latex_code)
        tree = ET.fromstring(mathml)
        omml = _transform(tree)
        omml_str = ET.tostring(omml, encoding='unicode')
        return parse_xml(omml_str)
    except Exception as e:
        print(f"Lỗi convert latex: {latex_code} -> {e}")
        return None

def add_text_with_math(paragraph, text, default_size_pt=13, default_font="Times New Roman", bold=False, italic=False, color_rgb=(0,0,0)):
    # Phân tách văn bản và công thức $...$
    pattern = r'\$([^\$]+)\$'
    pos = 0
    for match in re.finditer(pattern, text):
        start, end = match.span()
        # Đoạn văn bản thường trước match
        if start > pos:
            run = paragraph.add_run(text[pos:start])
            run.font.name = default_font
            run.font.size = Pt(default_size_pt)
            run.bold = bold
            run.italic = italic
            run.font.color.rgb = RGBColor(*color_rgb)
        
        # Đoạn công thức math
        latex_str = match.group(1).strip()
        omml_elm = latex_to_omml(latex_str)
        if omml_elm is not None:
            paragraph._p.append(omml_elm)
        else:
            # Fallback
            run_fb = paragraph.add_run(latex_str)
            run_fb.font.name = default_font
            run_fb.font.size = Pt(default_size_pt)
            run_fb.italic = True
            
        pos = end
        
    # Đoạn văn bản còn lại sau cùng
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        run.font.name = default_font
        run.font.size = Pt(default_size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

doc = Document()
p = doc.add_paragraph()
add_text_with_math(p, r"Bài 1. Cho biểu thức $P = \frac{x + 2\sqrt{x}}{x - 4} - \frac{1}{\sqrt{x} - 2}$ với $x \ge 0, x \neq 4$.")
doc.save(r"scratch\test_output_math.docx")
print("SUCCESS!")
