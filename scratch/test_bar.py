# -*- coding: utf-8 -*-
import docx
from docx.oxml import parse_xml

doc = docx.Document()

def create_overbar_math(text):
    xml = f"""<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
  <m:bar>
    <m:barPr><m:pos m:val="top"/></m:barPr>
    <m:e><m:r><m:t>{text}</m:t></m:r></m:e>
  </m:bar>
</m:oMath>"""
    return parse_xml(xml)

p1 = doc.add_paragraph("Số có gạch trên đầu 1: ")
p1._p.append(create_overbar_math("3*5"))

p2 = doc.add_paragraph("Số có gạch trên đầu 2: ")
p2._p.append(create_overbar_math("17*"))

p3 = doc.add_paragraph("Số có gạch trên đầu 3: ")
p3._p.append(create_overbar_math("2x3y"))

doc.save(r"scratch\test_bar_output.docx")
print("SUCCESS SAVED!")
