# -*- coding: utf-8 -*-
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from lxml import etree
import latex2mathml.converter as latex2mathml

# Load Microsoft Office Math XSLT
xslt_path = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"
if not os.path.exists(xslt_path):
    xslt_path = r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL"
xslt_doc = etree.parse(xslt_path)
transform = etree.XSLT(xslt_doc)

MATH_RE = re.compile(r"(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$)")

def normalize_latex_formula(s):
    s = re.sub(r"\\+widehat\{([A-Za-z0-9]+)\}", r"\\hat{\1}", s)
    s = re.sub(r"\\+widehat\s+([A-Za-z0-9])", r"\\hat{\1}", s)
    return s

def safe_save_doc(doc, target_path):
    try:
        doc.save(target_path)
        return target_path
    except PermissionError:
        p = Path(target_path)
        alt_path = str(p.parent / f"{p.stem}_Cap_Nhat{p.suffix}")
        doc.save(alt_path)
        print(f"Lưu ý: Tệp {target_path} đang mở trong Word nên bản mới nhất được lưu vào {alt_path}")
        return alt_path

def latex_to_omml(latex_str):
    latex_str = normalize_latex_formula(latex_str)
    mathml_str = latex2mathml.convert(latex_str)
    tree = etree.fromstring(mathml_str.encode("utf-8"))
    res = transform(tree)
    return etree.tostring(res, encoding="utf-8")

def add_math_to_paragraph(p, latex_str):
    try:
        omml_bytes = latex_to_omml(latex_str)
        el = parse_xml(omml_bytes)
        p._element.append(el)
    except Exception as e:
        print(f"Lỗi chuyển latex '{latex_str}': {e}")
        r = p.add_run(f"${latex_str}$")
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

def add_text_with_math(p, text, font_size=12, bold=False, italic=False, color_rgb=None):
    text = re.sub(r"\\+widehat\{([A-Za-z0-9]+)\}", r"\\hat{\1}", text)
    text = re.sub(r"(?<!\$)\((\\hat\{[A-Za-z0-9]+\}\s*=\s*\\hat\{[A-Za-z0-9]+\})\)(?!\$)", r"($\1$)", text)
    tokens = MATH_RE.split(text)
    for token in tokens:
        if not token:
            continue
        if token.startswith("$$") and token.endswith("$$"):
            add_math_to_paragraph(p, token[2:-2].strip())
        elif token.startswith("$") and token.endswith("$"):
            add_math_to_paragraph(p, token[1:-1].strip())
        else:
            r = p.add_run(token)
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
            r.font.bold = bold
            r.font.italic = italic
            if color_rgb:
                r.font.color.rgb = color_rgb

def add_p(doc, text="", font_size=12, bold=False, italic=False, color_rgb=None, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=3):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    
    if text:
        add_text_with_math(p, text, font_size=font_size, bold=bold, italic=italic, color_rgb=color_rgb)
    return p

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="4B5563", sz="4", val="single"):
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

def add_header(doc, lop_str, time_str="90 phút"):
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    c_left = table.cell(0, 0)
    c_right = table.cell(0, 1)
    c_left.width = Inches(3.2)
    c_right.width = Inches(3.8)
    set_cell_margins(c_left, 40, 40, 60, 60)
    set_cell_margins(c_right, 40, 40, 60, 60)
    
    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.15
    r = p_l.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    r = p_l.add_run("TỔ TOÁN - TIN HỌC\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    r = p_l.add_run("--------------------")
    r.font.name = "Times New Roman"; r.font.size = Pt(10)
    
    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.15
    r = p_r.add_run("ĐỀ KIỂM TRA GIỮA HỌC KỲ I\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)
    r = p_r.add_run(f"NĂM HỌC 2026 – 2027\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    r = p_r.add_run(f"MÔN: TOÁN – LỚP {lop_str}\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    r = p_r.add_run(f"Thời gian làm bài: {time_str} (không kể thời gian giao đề)")
    r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.font.italic = True
    
    # Student info box
    doc.add_paragraph()
    box = doc.add_table(rows=2, cols=2)
    box.alignment = WD_TABLE_ALIGNMENT.CENTER
    box.autofit = False
    box.cell(0, 0).width = Inches(5.0)
    box.cell(0, 1).width = Inches(2.0)
    box.cell(1, 0).width = Inches(5.0)
    box.cell(1, 1).width = Inches(2.0)
    set_table_borders(box, color="9CA3AF", sz="4")
    
    p00 = box.cell(0, 0).paragraphs[0]
    r = p00.add_run("Họ và tên học sinh: ........................................................................\nLớp: ........  Trường: ................................................................")
    r.font.name = "Times New Roman"; r.font.size = Pt(11)
    
    p01 = box.cell(0, 1).paragraphs[0]
    p01.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p01.add_run("ĐIỂM SỐ\n\n....................")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
    
    p10 = box.cell(1, 0).paragraphs[0]
    r = p10.add_run("Lời nhận xét của giáo viên:\n.......................................................................................................")
    r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.font.italic = True
    
    p11 = box.cell(1, 1).paragraphs[0]
    p11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p11.add_run("Chữ ký GK\n\n....................")
    r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.font.italic = True
    
    doc.add_paragraph()

# ==============================================================================
# TẠO ĐỀ TOÁN 8
# ==============================================================================
def tao_de_toan_8(out_docx, out_md):
    doc = Document()
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.6)
        
    add_header(doc, "8", "90 phút")
    
    add_p(doc, "A. ĐỀ KIỂM TRA", font_size=13, bold=True, color_rgb=RGBColor(0x1e, 0x3a, 0x8a))
    add_p(doc, "PHẦN I. TRẮC NGHIỆM KHÁCH QUAN (3,0 điểm)", font_size=12, bold=True)
    add_p(doc, "Khoanh tròn vào chữ cái đứng trước phương án trả lời đúng nhất (từ Câu 1 đến Câu 12):", font_size=11.5, italic=True)
    
    tn_8 = [
        ("Câu 1. (NB)", "Biểu thức nào sau đây là đơn thức nhiều biến?",
         ["A. $3x^2y$", "B. $\\frac{2x}{y}$", "C. $x^2 + y$", "D. $\\frac{1}{x} + y^2$"], "A"),
        ("Câu 2. (NB)", "Bậc của đơn thức $-5x^3y^2z$ là:",
         ["A. 3", "B. 5", "C. 6", "D. 7"], "C"),
        ("Câu 3. (NB)", "Đơn thức nào sau đây đồng dạng với đơn thức $2xy^2$?",
         ["A. $-3x^2y$", "B. $5xy^2$", "C. $2x^2y^2$", "D. $3xy$"], "B"),
        ("Câu 4. (NB)", "Thu gọn đa thức $P = 2x^2y + 3xy - 2x^2y + 5$ ta được kết quả là:",
         ["A. $3xy + 5$", "B. $4x^2y + 3xy + 5$", "C. $3xy - 5$", "D. $5$"], "A"),
        ("Câu 5. (NB)", "Hằng đẳng thức hiệu hai bình phương là:",
         ["A. $A^2 - B^2 = (A - B)(A + B)$", "B. $A^2 - B^2 = (A - B)^2$",
          "C. $A^2 - B^2 = A^2 - 2AB + B^2$", "D. $A^2 - B^2 = (A + B)^2$"], "A"),
        ("Câu 6. (NB)", "Khai triển của hằng đẳng thức $(x + 2)^2$ là:",
         ["A. $x^2 + 4$", "B. $x^2 + 2x + 4$", "C. $x^2 + 4x + 4$", "D. $x^2 + 4x + 2$"], "C"),
        ("Câu 7. (NB)", "Khai triển hằng đẳng thức $(x - 3y)^2$ ta được:",
         ["A. $x^2 - 6xy + 9y^2$", "B. $x^2 - 3xy + 9y^2$", "C. $x^2 - 9y^2$", "D. $x^2 + 6xy + 9y^2$"], "A"),
        ("Câu 8. (TH)", "Biểu thức $x^3 - 6x^2y + 12xy^2 - 8y^3$ viết dưới dạng lập phương của một hiệu là:",
         ["A. $(x - 8y)^3$", "B. $(x - 2y)^3$", "C. $(x + 2y)^3$", "D. $(x - 4y)^3$"], "B"),
        ("Câu 9. (NB)", "Tứ giác lồi là tứ giác luôn nằm trong:",
         ["A. Một nửa mặt phẳng có bờ là đường thẳng chứa bất kì cạnh nào của tứ giác.",
          "B. Hai nửa mặt phẳng khác nhau.",
          "C. Cùng một góc phần tư của mặt phẳng tọa độ.",
          "D. Đường tròn ngoại tiếp tứ giác."], "A"),
        ("Câu 10. (TH)", "Cho tứ giác $ABCD$ có $\\hat{A} = 70^\\circ$, $\\hat{B} = 80^\\circ$, $\\hat{C} = 100^\\circ$. Số đo góc $D$ là:",
         ["A. $110^\\circ$", "B. $100^\\circ$", "C. $90^\\circ$", "D. $120^\\circ$"], "A"),
        ("Câu 11. (NB)", "Hình thang cân là hình thang có:",
         ["A. Hai góc kề một đáy bằng nhau.", "B. Hai cạnh bên song song.",
          "C. Hai góc đối bù nhau và hai đáy bằng nhau.", "D. Hai cạnh đáy bằng nhau."], "A"),
        ("Câu 12. (NB)", "Khẳng định nào sau đây là sai đối với hình thang cân $ABCD$ ($AB \\parallel CD$)?",
         ["A. Hai cạnh bên bằng nhau ($AD = BC$).", "B. Hai đường chéo bằng nhau ($AC = BD$).",
          "C. Hai góc kề đáy $AB$ bằng nhau ($\\hat{A} = \\hat{B}$).", "D. Hai đường chéo vuông góc với nhau."], "D"),
    ]
    
    for tag, qtext, opts, _ in tn_8:
        add_p(doc, f"{tag} {qtext}", bold=True)
        # options table 2x2
        t = doc.add_table(rows=2, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        t.cell(0, 0).width = Inches(3.5); t.cell(0, 1).width = Inches(3.5)
        t.cell(1, 0).width = Inches(3.5); t.cell(1, 1).width = Inches(3.5)
        set_cell_margins(t.cell(0, 0), 20, 20, 40, 40); set_cell_margins(t.cell(0, 1), 20, 20, 40, 40)
        set_cell_margins(t.cell(1, 0), 20, 20, 40, 40); set_cell_margins(t.cell(1, 1), 20, 20, 40, 40)
        
        p00 = t.cell(0, 0).paragraphs[0]; p00.paragraph_format.line_spacing = 1.15; add_text_with_math(p00, opts[0])
        p01 = t.cell(0, 1).paragraphs[0]; p01.paragraph_format.line_spacing = 1.15; add_text_with_math(p01, opts[1])
        p10 = t.cell(1, 0).paragraphs[0]; p10.paragraph_format.line_spacing = 1.15; add_text_with_math(p10, opts[2])
        p11 = t.cell(1, 1).paragraphs[0]; p11.paragraph_format.line_spacing = 1.15; add_text_with_math(p11, opts[3])
        doc.add_paragraph()
        
    add_p(doc, "PHẦN II. TỰ LUẬN (7,0 điểm)", font_size=12, bold=True)
    
    add_p(doc, "Bài 13. (1,5 điểm) (NB)", bold=True)
    add_p(doc, "a) (0,75 điểm) Thu gọn và xác định bậc của đa thức sau:")
    add_p(doc, "$A = 3x^2y - 2xy^2 + 5x^2y + 4xy^2 - 7$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "b) (0,75 điểm) Cho hai đa thức $M = 2x^2 - 3xy + y^2$ và $N = x^2 + 2xy - 3y^2$. Tính $M + N$ và $M - N$.")
    
    add_p(doc, "Bài 14. (1,5 điểm)", bold=True)
    add_p(doc, "a) (0,75 điểm) (TH) Tính giá trị của biểu thức $P = 2x^2y - 3xy + 1$ tại $x = 1$, $y = -2$.")
    add_p(doc, "b) (0,75 điểm) (VD) Rút gọn biểu thức:")
    add_p(doc, "$Q = (2x - 1)(x + 3) - 2x(x + 2) + 5$", align=WD_ALIGN_PARAGRAPH.CENTER)
    
    add_p(doc, "Bài 15. (1,5 điểm)", bold=True)
    add_p(doc, "a) (0,75 điểm) (TH) Phân tích đa thức sau thành nhân tử: $x^2 - 4y^2 + 3x - 6y$.")
    add_p(doc, "b) (0,75 điểm) (VD) Phân tích đa thức sau thành nhân tử: $x^2 - 6x + 9 - y^2$.")
    
    add_p(doc, "Bài 16. (1,0 điểm) (TH)", bold=True)
    t16 = doc.add_table(rows=1, cols=2)
    t16.alignment = WD_TABLE_ALIGNMENT.CENTER
    t16.autofit = False
    c_text = t16.cell(0, 0)
    c_img = t16.cell(0, 1)
    c_text.width = Inches(4.3)
    c_img.width = Inches(2.7)
    set_cell_margins(c_text, 10, 10, 10, 20)
    set_cell_margins(c_img, 10, 10, 20, 10)
    
    p_t = c_text.paragraphs[0]
    p_t.paragraph_format.line_spacing = 1.2
    add_text_with_math(p_t, "Cho hình thang cân $ABCD$ ($AB \\parallel CD$, $AB < CD$). Kẻ các đường cao $AH, BK$ xuống đáy $CD$ ($H, K \\in CD$).")
    p_a = c_text.add_paragraph()
    p_a.paragraph_format.line_spacing = 1.2
    add_text_with_math(p_a, "a) (0,5 điểm) Chứng minh tam giác $AHD$ bằng tam giác $BKC$.")
    p_b = c_text.add_paragraph()
    p_b.paragraph_format.line_spacing = 1.2
    add_text_with_math(p_b, "b) (0,5 điểm) Chứng minh $DH = CK = \\frac{CD - AB}{2}$.")
    
    p_i = c_img.paragraphs[0]
    p_i.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_16 = str(Path("TROLYTHIEN/11_VE_HINH/Ket_qua/Bai_16_Hinh_Thang_Can_ABCD.png").resolve())
    if os.path.exists(img_16):
        p_i.add_run().add_picture(img_16, width=Inches(2.5))
    doc.add_paragraph()
    
    add_p(doc, "Bài 17. (1,5 điểm)", bold=True)
    add_p(doc, "a) (0,75 điểm) (VD) Tìm số thực $x$ thỏa mãn đẳng thức:")
    add_p(doc, "$(2x + 1)^2 - (2x - 1)(2x + 1) = 10$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "b) (0,75 điểm) (VDC) Cho các số thực $x, y$ thỏa mãn:")
    add_p(doc, "$x^2 + 2y^2 + 2xy - 2x - 6y + 5 = 0$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Tính giá trị của biểu thức $T = (x + y - 1)^{2026} + (x - 1)^{2027}$.")
    
    # --------------------------------------------------------------------------
    # ĐÁP ÁN & HƯỚNG DẪN CHẤM
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_p(doc, "B. ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM CHI TIẾT", font_size=13, bold=True, color_rgb=RGBColor(0x1e, 0x3a, 0x8a))
    
    add_p(doc, "I. BẢNG ĐÁP ÁN TRẮC NGHIỆM (3,0 điểm - Mỗi câu đúng được 0,25 điểm)", font_size=12, bold=True)
    ans_table = doc.add_table(rows=2, cols=12)
    ans_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ans_table, color="1E3A8A", sz="6")
    
    keys_8 = ["A", "C", "B", "A", "A", "C", "A", "B", "A", "A", "A", "D"]
    for i in range(12):
        c0 = ans_table.cell(0, i)
        c0.width = Inches(0.55)
        set_cell_background(c0, "DBEAFE")
        p = c0.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"C{i+1}"); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
        
        c1 = ans_table.cell(1, i)
        c1.width = Inches(0.55)
        p = c1.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(keys_8[i]); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
        
    doc.add_paragraph()
    add_p(doc, "II. HƯỚNG DẪN CHẤM TỰ LUẬN (7,0 điểm)", font_size=12, bold=True)
    
    rubric_8 = [
        ("Bài 13a\n(0,75đ)", [
            ("Ta có: $A = (3x^2y + 5x^2y) + (-2xy^2 + 4xy^2) - 7$", "0,25"),
            ("$A = 8x^2y + 2xy^2 - 7$", "0,25"),
            ("Hạng tử $8x^2y$ có bậc là $2 + 1 = 3$; hạng tử $2xy^2$ có bậc $3$. Vậy đa thức $A$ có bậc là 3.", "0,25"),
        ]),
        ("Bài 13b\n(0,75đ)", [
            ("$M + N = (2x^2 - 3xy + y^2) + (x^2 + 2xy - 3y^2) = 3x^2 - xy - 2y^2$", "0,50"),
            ("$M - N = (2x^2 - 3xy + y^2) - (x^2 + 2xy - 3y^2) = x^2 - 5xy + 4y^2$", "0,25"),
        ]),
        ("Bài 14a\n(0,75đ)", [
            ("Thay $x = 1$ và $y = -2$ vào biểu thức $P$, ta được:", "0,25"),
            ("$P = 2 \\cdot (1)^2 \\cdot (-2) - 3 \\cdot (1) \\cdot (-2) + 1$", "0,25"),
            ("$P = -4 + 6 + 1 = 3$. Vậy với $x = 1, y = -2$ thì $P = 3$.", "0,25"),
        ]),
        ("Bài 14b\n(0,75đ)", [
            ("Khai triển tích: $(2x - 1)(x + 3) = 2x^2 + 6x - x - 3 = 2x^2 + 5x - 3$", "0,25"),
            ("Nhân đơn thức với đa thức: $-2x(x + 2) = -2x^2 - 4x$", "0,25"),
            ("Thu gọn: $Q = 2x^2 + 5x - 3 - 2x^2 - 4x + 5 = x + 2$.", "0,25"),
        ]),
        ("Bài 15a\n(0,75đ)", [
            ("Nhóm hạng tử: $x^2 - 4y^2 + 3x - 6y = (x^2 - 4y^2) + (3x - 6y)$", "0,25"),
            ("Áp dụng HĐT và đặt nhân tử chung: $= (x - 2y)(x + 2y) + 3(x - 2y)$", "0,25"),
            ("Đặt nhân tử chung: $= (x - 2y)(x + 2y + 3)$.", "0,25"),
        ]),
        ("Bài 15b\n(0,75đ)", [
            ("Nhóm 3 hạng tử đầu tạo bình phương của một hiệu: $(x^2 - 6x + 9) - y^2$", "0,25"),
            ("Viết thành: $(x - 3)^2 - y^2$", "0,25"),
            ("Áp dụng HĐT hiệu hai bình phương: $(x - 3 - y)(x - 3 + y)$.", "0,25"),
        ]),
        ("Bài 16\n(1,0đ)", [
            ("a) Vì $ABCD$ là hình thang cân nên $AD = BC$ và $\\widehat{D} = \\widehat{C}$. Xét hai tam giác vuông $AHD$ (vuông tại $H$) và $BKC$ (vuông tại $K$): có cạnh huyền $AD = BC$, góc nhọn $\\widehat{D} = \\widehat{C}$. Do đó $\\Delta AHD = \\Delta BKC$ (cạnh huyền - góc nhọn).", "0,50"),
            ("b) Từ $\\Delta AHD = \\Delta BKC$ suy ra $DH = CK$. Mặt khác $ABKH$ là hình chữ nhật (vì $AB \\parallel HK$ và $AH \\parallel BK$ cùng vuông góc $CD$) nên $HK = AB$. Ta có $CD = DH + HK + KC = 2DH + AB \\Rightarrow 2DH = CD - AB \\Rightarrow DH = CK = \\frac{CD - AB}{2}$.", "0,50"),
        ]),
        ("Bài 17a\n(0,75đ)", [
            ("Khai triển: $(2x + 1)^2 = 4x^2 + 4x + 1$ và $(2x - 1)(2x + 1) = 4x^2 - 1$", "0,25"),
            ("Phương trình trở thành: $(4x^2 + 4x + 1) - (4x^2 - 1) = 10 \\Rightarrow 4x + 2 = 10$", "0,25"),
            ("$4x = 8 \\Rightarrow x = 2$. Vậy $x = 2$.", "0,25"),
        ]),
        ("Bài 17b\n(0,75đ)", [
            ("Biến đổi phương trình đã cho: $(x^2 + 2xy + y^2 - 2x - 2y + 1) + (y^2 - 4y + 4) = 0$", "0,25"),
            ("Tương đương: $[(x + y)^2 - 2(x + y) + 1] + (y - 2)^2 = 0 \\Rightarrow (x + y - 1)^2 + (y - 2)^2 = 0$", "0,25"),
            ("Vì $(x + y - 1)^2 \\ge 0$ và $(y - 2)^2 \\ge 0$ với mọi $x, y$ nên dấu bằng xảy ra khi: $\\begin{cases} x + y - 1 = 0 \\\\ y - 2 = 0 \\end{cases} \\Rightarrow \\begin{cases} y = 2 \\\\ x = -1 \\end{cases}$. Khi đó $x - 1 = -2$. Thay vào $T$: $T = 0^{2026} + (-2)^{2027} = -2^{2027}$.", "0,25"),
        ]),
    ]
    
    rt = doc.add_table(rows=1, cols=3)
    rt.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(rt, color="4B5563", sz="4")
    rt.cell(0, 0).width = Inches(1.2); rt.cell(0, 1).width = Inches(5.0); rt.cell(0, 2).width = Inches(0.8)
    for i, title in enumerate(["Câu", "Nội dung đáp án và các bước giải", "Điểm"]):
        c = rt.cell(0, i); set_cell_background(c, "F3F4F6")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title); r.font.name = "Times New Roman"; r.font.bold = True
        
    for cau, steps in rubric_8:
        for idx, (content, pt) in enumerate(steps):
            row = rt.add_row()
            c_cau = row.cells[0]; c_cont = row.cells[1]; c_pt = row.cells[2]
            c_cau.width = Inches(1.2); c_cont.width = Inches(5.0); c_pt.width = Inches(0.8)
            set_cell_margins(c_cau, 30, 30, 40, 40); set_cell_margins(c_cont, 30, 30, 40, 40); set_cell_margins(c_pt, 30, 30, 40, 40)
            
            if idx == 0:
                p = c_cau.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(cau); r.font.name = "Times New Roman"; r.font.bold = True
            p2 = c_cont.paragraphs[0]; add_text_with_math(p2, content)
            p3 = c_pt.paragraphs[0]; p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p3.add_run(pt); r.font.name = "Times New Roman"; r.font.bold = True
            
    saved_path = safe_save_doc(doc, out_docx)
    print("Đã tạo xong Word Toán 8:", saved_path)

# ==============================================================================
# TẠO ĐỀ TOÁN 9
# ==============================================================================
def tao_de_toan_9(out_docx, out_md):
    doc = Document()
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.6)
        
    add_header(doc, "9", "90 phút")
    
    add_p(doc, "A. ĐỀ KIỂM TRA", font_size=13, bold=True, color_rgb=RGBColor(0x1e, 0x3a, 0x8a))
    add_p(doc, "PHẦN I. TRẮC NGHIỆM KHÁCH QUAN (3,0 điểm)", font_size=12, bold=True)
    add_p(doc, "Khoanh tròn vào chữ cái đứng trước phương án trả lời đúng nhất (từ Câu 1 đến Câu 12):", font_size=11.5, italic=True)
    
    tn_9 = [
        ("Câu 1. (NB)", "Phương trình nào sau đây là phương trình bậc nhất hai ẩn $x$ và $y$?",
         ["A. $2x - 3y = 5$", "B. $2x^2 + y = 3$", "C. $xy + 2x = 1$", "D. $0x + 0y = 4$"], "A"),
        ("Câu 2. (NB)", "Cặp số nào sau đây là một nghiệm của phương trình $3x - 2y = 1$?",
         ["A. $(1; 1)$", "B. $(1; -1)$", "C. $(0; 1)$", "D. $(2; 3)$"], "A"),
        ("Câu 3. (NB)", "Hệ phương trình $\\begin{cases} x + y = 3 \\\\ 2x - y = 0 \\end{cases}$ có nghiệm duy nhất là:",
         ["A. $(1; 2)$", "B. $(2; 1)$", "C. $(0; 3)$", "D. $(3; 0)$"], "A"),
        ("Câu 4. (NB)", "Trong các hệ phương trình sau, hệ phương trình nào là hệ hai phương trình bậc nhất hai ẩn?",
         ["A. $\\begin{cases} 2x + 3y = 5 \\\\ x - y = 1 \\end{cases}$",
          "B. $\\begin{cases} x^2 + y = 3 \\\\ 2x - y = 1 \\end{cases}$",
          "C. $\\begin{cases} \\frac{1}{x} + y = 2 \\\\ x - 2y = 3 \\end{cases}$",
          "D. $\\begin{cases} xy = 1 \\\\ x + y = 2 \\end{cases}$"], "A"),
        ("Câu 5. (TH)", "Nghiệm của hệ phương trình $\\begin{cases} 3x + y = 5 \\\\ 2x - y = 5 \\end{cases}$ là:",
         ["A. $(2; -1)$", "B. $(1; 2)$", "C. $(-2; 1)$", "D. $(3; -4)$"], "A"),
        ("Câu 6. (NB)", "Nghiệm của phương trình tích $(2x - 4)(x + 3) = 0$ là:",
         ["A. $x = 2$ hoặc $x = -3$", "B. $x = -2$ hoặc $x = 3$", "C. $x = 2$ hoặc $x = 3$", "D. $x = -2$ hoặc $x = -3$"], "A"),
        ("Câu 7. (NB)", "Điều kiện xác định của căn thức bậc hai $\\sqrt{x - 3}$ là:",
         ["A. $x \\ge 3$", "B. $x > 3$", "C. $x \\le 3$", "D. $x < 3$"], "A"),
        ("Câu 8. (NB)", "Căn bậc hai số học của số thực $16$ là:",
         ["A. $4$", "B. $-4$", "C. $\\pm 4$", "D. $256$"], "A"),
        ("Câu 9. (VD)", "Giá trị của biểu thức $\\sqrt{(3 - \\sqrt{10})^2}$ bằng:",
         ["A. $\\sqrt{10} - 3$", "B. $3 - \\sqrt{10}$", "C. $9 - 10$", "D. $3 + \\sqrt{10}$"], "A"),
        ("Câu 10. (TH)", "Nghiệm của bất phương trình $2x - 4 > 0$ là:",
         ["A. $x > 2$", "B. $x < 2$", "C. $x \\ge 2$", "D. $x > -2$"], "A"),
        ("Câu 11. (NB)", "Giá trị $x = 2$ là một nghiệm của bất phương trình nào sau đây?",
         ["A. $3x - 1 > 4$", "B. $2x + 1 < 3$", "C. $-x + 3 < 0$", "D. $5 - 2x < 0$"], "A"),
        ("Câu 12. (TH)", "Cho hệ phương trình $\\begin{cases} ax + y = 3 \\\\ 2x - y = 1 \\end{cases}$. Biết hệ có nghiệm $(1; 1)$, giá trị của $a$ là:",
         ["A. $a = 2$", "B. $a = 1$", "C. $a = -2$", "D. $a = 3$"], "A"),
    ]
    
    for tag, qtext, opts, _ in tn_9:
        add_p(doc, f"{tag} {qtext}", bold=True)
        t = doc.add_table(rows=2, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        t.cell(0, 0).width = Inches(3.5); t.cell(0, 1).width = Inches(3.5)
        t.cell(1, 0).width = Inches(3.5); t.cell(1, 1).width = Inches(3.5)
        set_cell_margins(t.cell(0, 0), 20, 20, 40, 40); set_cell_margins(t.cell(0, 1), 20, 20, 40, 40)
        set_cell_margins(t.cell(1, 0), 20, 20, 40, 40); set_cell_margins(t.cell(1, 1), 20, 20, 40, 40)
        
        p00 = t.cell(0, 0).paragraphs[0]; p00.paragraph_format.line_spacing = 1.15; add_text_with_math(p00, opts[0])
        p01 = t.cell(0, 1).paragraphs[0]; p01.paragraph_format.line_spacing = 1.15; add_text_with_math(p01, opts[1])
        p10 = t.cell(1, 0).paragraphs[0]; p10.paragraph_format.line_spacing = 1.15; add_text_with_math(p10, opts[2])
        p11 = t.cell(1, 1).paragraphs[0]; p11.paragraph_format.line_spacing = 1.15; add_text_with_math(p11, opts[3])
        doc.add_paragraph()
        
    add_p(doc, "PHẦN II. TỰ LUẬN (7,0 điểm)", font_size=12, bold=True)
    
    add_p(doc, "Bài 10. (1,0 điểm) (TH)", bold=True)
    add_p(doc, "Giải các hệ phương trình sau:")
    add_p(doc, "a) (0,5 điểm) $\\begin{cases} 2x + 3y = 7 \\\\ 3x - y = 5 \\end{cases}$")
    add_p(doc, "b) (0,5 điểm) $\\begin{cases} x - 2y = 1 \\\\ 3x + 2y = 11 \\end{cases}$")
    
    add_p(doc, "Bài 11. (2,25 điểm)", bold=True)
    add_p(doc, "a) (0,75 điểm) (NB) Giải phương trình tích: $(3x - 2)(x + 4) = 0$.")
    add_p(doc, "b) (0,75 điểm) (TH) Giải phương trình chứa ẩn ở mẫu:")
    add_p(doc, "$\\frac{x + 2}{x - 2} - \\frac{x - 2}{x + 2} = \\frac{16}{x^2 - 4}$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "c) (0,75 điểm) (TH) Giải bất phương trình sau và biểu diễn nghiệm trên trục số:")
    add_p(doc, "$\\frac{2x - 1}{3} - \\frac{x - 2}{2} \\le 1$", align=WD_ALIGN_PARAGRAPH.CENTER)
    
    add_p(doc, "Bài 12. (1,75 điểm)", bold=True)
    add_p(doc, "a) (1,0 điểm) (VD) Thực hiện phép tính:")
    add_p(doc, "$A = \\sqrt{48} - 2\\sqrt{75} + \\sqrt{108} - \\frac{1}{3}\\sqrt{27}$", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "b) (0,75 điểm) (VD) Rút gọn biểu thức:")
    add_p(doc, "$B = \\left(\\frac{\\sqrt{x}}{\\sqrt{x} - 2} - \\frac{4}{x - 2\\sqrt{x}}\\right) : \\frac{\\sqrt{x} + 2}{\\sqrt{x}}$  với $x > 0$ và $x \\ne 4$", align=WD_ALIGN_PARAGRAPH.CENTER)
    
    add_p(doc, "Bài 13. (1,0 điểm) (VD - Bài toán thực tế)", bold=True)
    add_p(doc, "Hai tổ công nhân cùng may một loại áo khoác mùa đông cho học sinh vùng cao. Nếu cả hai tổ cùng làm thì trong 4 ngày sẽ hoàn thành kế hoạch. Nhưng thực tế, tổ I làm trong 3 ngày rồi chuyển sang công việc khác, tổ II làm tiếp một mình trong 6 ngày nữa thì hoàn thành công việc. Hỏi nếu làm riêng thì mỗi tổ phải mất bao nhiêu ngày để may xong số áo khoác theo kế hoạch?")
    
    add_p(doc, "Bài 14. (1,0 điểm) (VDC)", bold=True)
    add_p(doc, "Cho các số thực dương $x, y$ thỏa mãn $x + y \\le 2$. Tìm giá trị nhỏ nhất của biểu thức:")
    add_p(doc, "$P = \\frac{1}{x^2 + y^2} + \\frac{2}{xy} + 3xy$", align=WD_ALIGN_PARAGRAPH.CENTER)
    
    # --------------------------------------------------------------------------
    # ĐÁP ÁN & HƯỚNG DẪN CHẤM TOÁN 9
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_p(doc, "B. ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM CHI TIẾT", font_size=13, bold=True, color_rgb=RGBColor(0x1e, 0x3a, 0x8a))
    
    add_p(doc, "I. BẢNG ĐÁP ÁN TRẮC NGHIỆM (3,0 điểm - Mỗi câu đúng được 0,25 điểm)", font_size=12, bold=True)
    ans_table = doc.add_table(rows=2, cols=12)
    ans_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ans_table, color="1E3A8A", sz="6")
    
    keys_9 = ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"]
    for i in range(12):
        c0 = ans_table.cell(0, i)
        c0.width = Inches(0.55)
        set_cell_background(c0, "DBEAFE")
        p = c0.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"C{i+1}"); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
        
        c1 = ans_table.cell(1, i)
        c1.width = Inches(0.55)
        p = c1.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(keys_9[i]); r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True
        
    doc.add_paragraph()
    add_p(doc, "II. HƯỚNG DẪN CHẤM TỰ LUẬN (7,0 điểm)", font_size=12, bold=True)
    
    rubric_9 = [
        ("Bài 10a\n(0,5đ)", [
            ("Từ phương trình thứ hai rút ra: $y = 3x - 5$.", "0,25"),
            ("Thế vào phương trình thứ nhất: $2x + 3(3x - 5) = 7 \\Rightarrow 11x - 15 = 7 \\Rightarrow 11x = 22 \\Rightarrow x = 2$. Suy ra $y = 3(2) - 5 = 1$. Vậy hệ phương trình có nghiệm duy nhất là $(2; 1)$.", "0,25"),
        ]),
        ("Bài 10b\n(0,5đ)", [
            ("Cộng từng vế hai phương trình: $(x - 2y) + (3x + 2y) = 1 + 11 \\Rightarrow 4x = 12 \\Rightarrow x = 3$.", "0,25"),
            ("Thay $x = 3$ vào $x - 2y = 1 \\Rightarrow 3 - 2y = 1 \\Rightarrow 2y = 2 \\Rightarrow y = 1$. Vậy hệ phương trình có nghiệm duy nhất là $(3; 1)$.", "0,25"),
        ]),
        ("Bài 11a\n(0,75đ)", [
            ("Ta có: $(3x - 2)(x + 4) = 0 \\Rightarrow 3x - 2 = 0$ hoặc $x + 4 = 0$", "0,25"),
            ("Trường hợp 1: $3x - 2 = 0 \\Rightarrow 3x = 2 \\Rightarrow x = \\frac{2}{3}$.", "0,25"),
            ("Trường hợp 2: $x + 4 = 0 \\Rightarrow x = -4$. Vậy phương trình đã cho có hai nghiệm là $x = \\frac{2}{3}$ và $x = -4$.", "0,25"),
        ]),
        ("Bài 11b\n(0,75đ)", [
            ("Điều kiện xác định: $x \\ne 2$ và $x \\ne -2$. Quy đồng mẫu thức hai vế: Mẫu thức chung là $(x - 2)(x + 2) = x^2 - 4$.", "0,25"),
            ("Phương trình suy ra: $(x + 2)^2 - (x - 2)^2 = 16 \\Rightarrow (x^2 + 4x + 4) - (x^2 - 4x + 4) = 16 \\Rightarrow 8x = 16 \\Rightarrow x = 2$.", "0,25"),
            ("So sánh với điều kiện xác định: $x = 2$ không thỏa mãn điều kiện (loại). Vậy phương trình vô nghiệm.", "0,25"),
        ]),
        ("Bài 11c\n(0,75đ)", [
            ("Quy đồng mẫu số hai vế với mẫu chung là 6: $2(2x - 1) - 3(x - 2) \\le 6$.", "0,25"),
            ("Khai triển và thu gọn: $4x - 2 - 3x + 6 \\le 6 \\Rightarrow x + 4 \\le 6 \\Rightarrow x \\le 2$.", "0,25"),
            ("Kết luận: Nghiệm của bất phương trình là $x \\le 2$. Học sinh biểu diễn đúng trên trục số (điểm 2 có ngoặc vuông quay về bên trái, gạch bỏ phần lớn hơn 2).", "0,25"),
        ]),
        ("Bài 12a\n(1,0đ)", [
            ("Đưa thừa số ra ngoài dấu căn: $\\sqrt{48} = \\sqrt{16 \\cdot 3} = 4\\sqrt{3}$", "0,25"),
            ("$2\\sqrt{75} = 2\\sqrt{25 \\cdot 3} = 10\\sqrt{3}$; $\\sqrt{108} = \\sqrt{36 \\cdot 3} = 6\\sqrt{3}$", "0,25"),
            ("$\\frac{1}{3}\\sqrt{27} = \\frac{1}{3} \\cdot 3\\sqrt{3} = \\sqrt{3}$", "0,25"),
            ("Thu gọn: $A = 4\\sqrt{3} - 10\\sqrt{3} + 6\\sqrt{3} - \\sqrt{3} = (4 - 10 + 6 - 1)\\sqrt{3} = -\\sqrt{3}$.", "0,25"),
        ]),
        ("Bài 12b\n(0,75đ)", [
            ("Ta có $x - 2\\sqrt{x} = \\sqrt{x}(\\sqrt{x} - 2)$. Trong ngoặc thứ nhất: $\\frac{\\sqrt{x} \\cdot \\sqrt{x} - 4}{\\sqrt{x}(\\sqrt{x} - 2)} = \\frac{x - 4}{\\sqrt{x}(\\sqrt{x} - 2)}$.", "0,25"),
            ("Phân tích $x - 4 = (\\sqrt{x} - 2)(\\sqrt{x} + 2)$, rút gọn được: $\\frac{\\sqrt{x} + 2}{\\sqrt{x}}$.", "0,25"),
            ("Thực hiện phép chia: $B = \\frac{\\sqrt{x} + 2}{\\sqrt{x}} : \\frac{\\sqrt{x} + 2}{\\sqrt{x}} = 1$. Vậy $B = 1$ với $x > 0, x \\ne 4$.", "0,25"),
        ]),
        ("Bài 13\n(1,0đ)", [
            ("Gọi thời gian để tổ I làm một mình hoàn thành kế hoạch là $x$ (ngày, $x > 4$). Gọi thời gian để tổ II làm một mình hoàn thành kế hoạch là $y$ (ngày, $y > 4$). Trong 1 ngày, tổ I làm được $\\frac{1}{x}$ công việc, tổ II làm được $\\frac{1}{y}$ công việc.", "0,25"),
            ("Vì hai tổ cùng làm trong 4 ngày xong công việc nên trong 1 ngày hai tổ làm được $\\frac{1}{4}$ công việc, ta có phương trình: $\\frac{1}{x} + \\frac{1}{y} = \\frac{1}{4}$ (1).", "0,25"),
            ("Thực tế, tổ I làm 3 ngày được $\\frac{3}{x}$ công việc, tổ II làm 6 ngày được $\\frac{6}{y}$ công việc và hoàn thành kế hoạch, ta có: $\\frac{3}{x} + \\frac{6}{y} = 1$ (2).", "0,25"),
            ("Từ (1) và (2) ta có hệ phương trình: đặt $u = \\frac{1}{x}, v = \\frac{1}{y}$ ta được: $\\begin{cases} u + v = \\frac{1}{4} \\\\ 3u + 6v = 1 \\end{cases} \\Rightarrow \\begin{cases} u = \\frac{1}{6} \\\\ v = \\frac{1}{12} \\end{cases} \\Rightarrow \\begin{cases} x = 6 \\\\ y = 12 \\end{cases}$ (thỏa mãn điều kiện). Vậy tổ I làm riêng mất 6 ngày, tổ II làm riêng mất 12 ngày.", "0,25"),
        ]),
        ("Bài 14\n(1,0đ)", [
            ("Biến đổi biểu thức $P$: $P = \\left(\\frac{1}{x^2 + y^2} + \\frac{1}{2xy}\\right) + \\left(\\frac{3}{2xy} + \\frac{3xy}{8}\\right) + \\frac{21}{8}xy$.", "0,25"),
            ("Áp dụng bất đẳng thức Cauchy-Schwarz dạng phân thức: $\\frac{1}{x^2 + y^2} + \\frac{1}{2xy} \\ge \\frac{4}{x^2 + y^2 + 2xy} = \\frac{4}{(x+y)^2} \\ge \\frac{4}{2^2} = 1$.", "0,25"),
            ("Áp dụng BĐT AM-GM cho hai số dương: $\\frac{3}{2xy} + \\frac{3xy}{8} \\ge 2\\sqrt{\\frac{3}{2xy} \\cdot \\frac{3xy}{8}} = 2 \\cdot \\frac{3}{4} = \\frac{3}{2}$. Lại có $xy \\le \\frac{(x+y)^2}{4} \\le \\frac{4}{4} = 1$. Nhưng ta cần chặn dưới cho số hạng cuối, ta ghép lại: $P = \\frac{1}{x^2+y^2} + \\frac{1}{2xy} + \\frac{3}{2xy} + 3xy \\ge \\frac{4}{(x+y)^2} + 2\\sqrt{\\frac{3}{2xy} \\cdot 3xy \\cdot ...}$ Cách đơn giản: $P = \\left(\\frac{1}{x^2+y^2} + \\frac{1}{2xy}\\right) + \\left(\\frac{1}{2xy} + 2xy\\right) + \\left(\\frac{1}{xy} + xy\\right) \\ge 1 + 2 + 2 = 5$.", "0,25"),
            ("Dấu bằng xảy ra khi và chỉ khi $x^2 + y^2 = 2xy$ và $x + y = 2 \\Rightarrow x = y = 1$. Vậy giá trị nhỏ nhất của $P$ là $5$ khi $x = y = 1$.", "0,25"),
        ]),
    ]
    
    rt = doc.add_table(rows=1, cols=3)
    rt.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(rt, color="4B5563", sz="4")
    rt.cell(0, 0).width = Inches(1.2); rt.cell(0, 1).width = Inches(5.0); rt.cell(0, 2).width = Inches(0.8)
    for i, title in enumerate(["Câu", "Nội dung đáp án và các bước giải", "Điểm"]):
        c = rt.cell(0, i); set_cell_background(c, "F3F4F6")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title); r.font.name = "Times New Roman"; r.font.bold = True
        
    for cau, steps in rubric_9:
        for idx, (content, pt) in enumerate(steps):
            row = rt.add_row()
            c_cau = row.cells[0]; c_cont = row.cells[1]; c_pt = row.cells[2]
            c_cau.width = Inches(1.2); c_cont.width = Inches(5.0); c_pt.width = Inches(0.8)
            set_cell_margins(c_cau, 30, 30, 40, 40); set_cell_margins(c_cont, 30, 30, 40, 40); set_cell_margins(c_pt, 30, 30, 40, 40)
            
            if idx == 0:
                p = c_cau.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(cau); r.font.name = "Times New Roman"; r.font.bold = True
            p2 = c_cont.paragraphs[0]; add_text_with_math(p2, content)
            if "Bài 11c" in cau and idx == 2:
                img_ts = str(Path("TROLYTHIEN/11_VE_HINH/Ket_qua/Bai_11c_Truc_So_Toan_9.png").resolve())
                if os.path.exists(img_ts):
                    p_img = c_cont.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_img.paragraph_format.space_before = Pt(4)
                    p_img.add_run().add_picture(img_ts, width=Inches(4.2))
            p3 = c_pt.paragraphs[0]; p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p3.add_run(pt); r.font.name = "Times New Roman"; r.font.bold = True
            
    saved_path = safe_save_doc(doc, out_docx)
    print("Đã tạo xong Word Toán 9:", saved_path)

if __name__ == "__main__":
    out_dir = Path("TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    t8_docx = str(out_dir / "De_Kiem_Tra_Toan_8_Giua_HK1.docx")
    t8_md = str(out_dir / "De_Kiem_Tra_Toan_8_Giua_HK1.md")
    tao_de_toan_8(t8_docx, t8_md)
    
    t9_docx = str(out_dir / "De_Kiem_Tra_Toan_9_Giua_HK1.docx")
    t9_md = str(out_dir / "De_Kiem_Tra_Toan_9_Giua_HK1.md")
    tao_de_toan_9(t9_docx, t9_md)
    print("ALL EXAMS GENERATED SUCCESSFULLY!")
