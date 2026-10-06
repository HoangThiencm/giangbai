import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

INPUT_PATH = r"TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/Ke-hoach-THCS-Tan-Phong-2026-2027-the-thuc-ND30.docx"
OUTPUT_PATH = r"TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/Ke_Hoach_GDNT_THCS_Tan_Phong_2026_2027_Chuan_ND30.docx"

doc = Document(INPUT_PATH)

def set_font_run(run, name='Times New Roman', size_pt=13, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color_rgb:
        run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._r.get_or_add_rPr()
    # Ensure correct font name in w:rFonts
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is not None:
        rPr.remove(rFonts)
    new_rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{name}" w:hAnsi="{name}" w:cs="{name}" w:eastAsia="{name}"/>')
    rPr.append(new_rFonts)

def remove_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    new_borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(new_borders)

def set_table_borders(table, color="000000", sz="4"):
    tblPr = table._tbl.tblPr
    tblBorders = tblPr.find(qn('w:tblBorders'))
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    new_borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(new_borders)

def set_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn('w:cantSplit')) is None:
        cantSplit = parse_xml(f'<w:cantSplit {nsdecls("w")}/>')
        trPr.append(cantSplit)

def set_tbl_header(row):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn('w:tblHeader')) is None:
        tblHeader = parse_xml(f'<w:tblHeader {nsdecls("w")}/>')
        trPr.append(tblHeader)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = tcPr.find(qn('w:tcMar'))
    if tcMar is not None:
        tcPr.remove(tcMar)
    new_tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>\n'
        f'  <w:top w:w="{top}" w:type="dxa"/>\n'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>\n'
        f'  <w:left w:w="{left}" w:type="dxa"/>\n'
        f'  <w:right w:w="{right}" w:type="dxa"/>\n'
        f'</w:tcMar>'
    )
    tcPr.append(new_tcMar)

def add_vector_line_to_p(paragraph, length_mm, space_before=1, space_after=3):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(space_before)
    paragraph.paragraph_format.space_after = Pt(space_after)
    paragraph.paragraph_format.line_spacing = 1.0
    paragraph.paragraph_format.first_line_indent = Inches(0)
    # Clear existing runs
    p_elem = paragraph._p
    for child in list(p_elem):
        if child.tag.endswith('r'):
            p_elem.remove(child)
    length_pt = round(length_mm * 72 / 25.4, 2)
    run_xml = (
        f'<w:r {nsdecls("w")} xmlns:v="urn:schemas-microsoft-com:vml" '
        f'xmlns:o="urn:schemas-microsoft-com:office:office">'
        f'<w:pict><v:line style="position:relative" from="0pt,0pt" to="{length_pt}pt,0pt" '
        f'strokecolor="#000000" strokeweight="0.75pt"/></w:pict></w:r>'
    )
    p_elem.append(parse_xml(run_xml))

print("1. Standardizing Margins for all Sections...")
for idx, section in enumerate(doc.sections):
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    print(f"   Section {idx}: T=20mm, B=20mm, L=30mm, R=15mm (Orientation: {section.orientation})")

print("2. Standardizing Header Table (Table 0)...")
t0 = doc.tables[0]
remove_table_borders(t0)
t0.alignment = WD_TABLE_ALIGNMENT.CENTER
t0.autofit = False

# Set column widths: Left = 65mm (3685 dxa), Right = 100mm (5669 dxa)
col_widths_t0 = [Mm(65), Mm(100)]
for row in t0.rows:
    for c_idx, width in enumerate(col_widths_t0):
        cell = row.cells[c_idx]
        cell.width = width
        set_cell_margins(cell, top=0, bottom=0, left=0, right=0)

# Cell (0,0): UBND & TRƯỜNG THCS
c00 = t0.rows[0].cells[0]
p_ubnd = c00.paragraphs[0]
p_ubnd.text = "UBND PHƯỜNG TÂN TRIỀU"
p_ubnd.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ubnd.paragraph_format.line_spacing = 1.0
p_ubnd.paragraph_format.space_before = Pt(0)
p_ubnd.paragraph_format.space_after = Pt(2)
p_ubnd.paragraph_format.first_line_indent = Inches(0)
set_font_run(p_ubnd.runs[0], size_pt=12, bold=False)

p_truong = c00.paragraphs[1]
p_truong.text = "TRƯỜNG THCS TÂN PHONG"
p_truong.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_truong.paragraph_format.line_spacing = 1.0
p_truong.paragraph_format.space_before = Pt(0)
p_truong.paragraph_format.space_after = Pt(1)
p_truong.paragraph_format.first_line_indent = Inches(0)
set_font_run(p_truong.runs[0], size_pt=12, bold=True)

if len(c00.paragraphs) > 2:
    p_line_left = c00.paragraphs[2]
else:
    p_line_left = c00.add_paragraph()
add_vector_line_to_p(p_line_left, length_mm=38, space_before=1, space_after=3)

# Cell (0,1): QUỐC HIỆU & TIÊU NGỮ
c01 = t0.rows[0].cells[1]
p_qh = c01.paragraphs[0]
p_qh.text = "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"
p_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_qh.paragraph_format.line_spacing = 1.0
p_qh.paragraph_format.space_before = Pt(0)
p_qh.paragraph_format.space_after = Pt(2)
p_qh.paragraph_format.first_line_indent = Inches(0)
set_font_run(p_qh.runs[0], size_pt=12, bold=True)

p_tn = c01.paragraphs[1]
p_tn.text = "Độc lập - Tự do - Hạnh phúc"
p_tn.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_tn.paragraph_format.line_spacing = 1.0
p_tn.paragraph_format.space_before = Pt(0)
p_tn.paragraph_format.space_after = Pt(1)
p_tn.paragraph_format.first_line_indent = Inches(0)
set_font_run(p_tn.runs[0], size_pt=13, bold=True)

if len(c01.paragraphs) > 2:
    p_line_right = c01.paragraphs[2]
else:
    p_line_right = c01.add_paragraph()
add_vector_line_to_p(p_line_right, length_mm=75, space_before=1, space_after=3)

# Row 1: Số hiệu & Địa danh ngày tháng
c10 = t0.rows[1].cells[0]
p_so = c10.paragraphs[0]
p_so.text = "Số: 01/KH-THCS"
p_so.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_so.paragraph_format.line_spacing = 1.0
p_so.paragraph_format.space_before = Pt(2)
p_so.paragraph_format.space_after = Pt(0)
p_so.paragraph_format.first_line_indent = Inches(0)
set_font_run(p_so.runs[0], size_pt=13, bold=False)

c11 = t0.rows[1].cells[1]
p_ngay = c11.paragraphs[0]
p_ngay.text = "Tân Triều, ngày 14 tháng 9 năm 2026"
p_ngay.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ngay.paragraph_format.line_spacing = 1.0
p_ngay.paragraph_format.space_before = Pt(2)
p_ngay.paragraph_format.space_after = Pt(0)
p_ngay.paragraph_format.first_line_indent = Inches(0)
set_font_run(p_ngay.runs[0], size_pt=13, bold=False, italic=True)

print("3. Standardizing Titles & Legal Bases (Căn cứ)...")
# P0: DỰ THẢO
p0 = doc.paragraphs[0]
p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
p0.paragraph_format.first_line_indent = Inches(0)
p0.paragraph_format.line_spacing = 1.0
p0.paragraph_format.space_before = Pt(8)
p0.paragraph_format.space_after = Pt(2)
for r in p0.runs:
    set_font_run(r, size_pt=13, bold=True)

# P1: KẾ HOẠCH
p1 = doc.paragraphs[1]
p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p1.paragraph_format.first_line_indent = Inches(0)
p1.paragraph_format.line_spacing = 1.2
p1.paragraph_format.space_before = Pt(6)
p1.paragraph_format.space_after = Pt(3)
for r in p1.runs:
    set_font_run(r, size_pt=14.5, bold=True)

# P2: Giáo dục nhà trường năm học 2026 - 2027
p2 = doc.paragraphs[2]
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.paragraph_format.first_line_indent = Inches(0)
p2.paragraph_format.line_spacing = 1.2
p2.paragraph_format.space_before = Pt(2)
p2.paragraph_format.space_after = Pt(12)
for r in p2.runs:
    set_font_run(r, size_pt=13, bold=True)

# P3: I. Căn cứ xây dựng kế hoạch
p3 = doc.paragraphs[3]
p3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p3.paragraph_format.first_line_indent = Inches(0)
p3.paragraph_format.line_spacing = 1.2
p3.paragraph_format.space_before = Pt(8)
p3.paragraph_format.space_after = Pt(4)
for r in p3.runs:
    set_font_run(r, size_pt=13, bold=True)

# Legal bases standardized text (P4 to P18)
cancu_texts = [
    "Căn cứ Quyết định số 2308/QĐ-BGDĐT ngày 06/08/2026 của Bộ Giáo dục và Đào tạo về việc Ban hành Khung kế hoạch thời gian năm học đối với giáo dục mầm non, giáo dục phổ thông và giáo dục thường xuyên;",
    "Căn cứ Công văn số 7288/UBND-KGVX ngày 12/08/2026 của Ủy ban nhân dân Thành phố Đồng Nai về việc thực hiện Quyết định số 2308/QĐ-BGDĐT ngày 06/08/2026 của Bộ Giáo dục và Đào tạo;",
    "Căn cứ Thông tư số 32/2018/TT-BGDĐT ngày 26/12/2018 của Bộ Giáo dục và Đào tạo ban hành Chương trình giáo dục phổ thông 2018 (được sửa đổi, bổ sung bởi Thông tư 20/2021/TT-BGDĐT, Thông tư 13/2022/TT-BGDĐT và Thông tư 17/2025/TT-BGDĐT);",
    "Căn cứ Thông tư số 22/2021/TT-BGDĐT ngày 20/7/2021 của Bộ Giáo dục và Đào tạo quy định về đánh giá học sinh trung học cơ sở và trung học phổ thông;",
    "Căn cứ Thông tư số 15/2026/TT-BGDĐT ngày 24/3/2026 của Bộ Giáo dục và Đào tạo ban hành Điều lệ trường tiểu học, trường trung học cơ sở, trường trung học phổ thông và trường phổ thông có nhiều cấp học;",
    "Căn cứ Quyết định số 2422/QĐ-BGDĐT ngày 18/8/2026 của Bộ Giáo dục và Đào tạo ban hành Khung nội dung giáo dục Trí tuệ nhân tạo (AI) cho học sinh phổ thông và Công văn số 5588/BGDĐT-GDPT ngày 19/8/2026 về việc hướng dẫn triển khai;",
    "Căn cứ Thông tư số 02/2025/TT-BGDĐT ngày 24/01/2025 của Bộ Giáo dục và Đào tạo quy định Khung năng lực số cho người học và Kế hoạch triển khai Khung năng lực số cho học sinh phổ thông của Sở Giáo dục và Đào tạo tỉnh Đồng Nai;",
    "Căn cứ Quyết định số 2371/QĐ-TTg ngày 27/10/2025 của Thủ tướng Chính phủ phê duyệt Đề án “Đưa tiếng Anh thành ngôn ngữ thứ hai trong trường học giai đoạn 2025-2035, tầm nhìn đến năm 2045”;",
    "Căn cứ Công văn số 6020/BGDĐT-KHCNTT ngày 08/9/2026 của Bộ Giáo dục và Đào tạo về việc triển khai một số nhiệm vụ trọng tâm về chuyển đổi số năm học 2026-2027;",
    "Căn cứ Công văn số 4567/BGDĐT-GDPT ngày 05/8/2025 của Bộ Giáo dục và Đào tạo về việc hướng dẫn tổ chức dạy học 2 buổi/ngày đối với giáo dục phổ thông;",
    "Căn cứ Công văn số 5512/BGDĐT-GDTrH ngày 18/12/2020 về xây dựng và tổ chức thực hiện kế hoạch giáo dục của nhà trường; Công văn số 5636/BGDĐT-GDTrH ngày 10/10/2023 về xây dựng kế hoạch dạy học các môn học, hoạt động giáo dục; Công văn số 3175/BGDĐT-GDTrH ngày 21/7/2022 về đổi mới phương pháp dạy học và kiểm tra, đánh giá môn Ngữ văn ở trường phổ thông của Bộ Giáo dục và Đào tạo;",
    "Căn cứ Công văn hướng dẫn thực hiện nhiệm vụ giáo dục phổ thông năm học 2026-2027 của Sở Giáo dục và Đào tạo tỉnh Đồng Nai;",
    "Căn cứ Quyết định số 2322/QĐ-UBND ngày 19/8/2026 của Ủy ban nhân dân thành phố Đồng Nai ban hành Kế hoạch thời gian năm học 2026–2027; các văn bản chỉ đạo của Ủy ban nhân dân phường Tân Triều về thực hiện nhiệm vụ giáo dục năm học 2026–2027;",
    "Căn cứ Thông tư số 03/2018/TT-BGDĐT ngày 29/01/2018 của Bộ Giáo dục và Đào tạo quy định về giáo dục hòa nhập đối với người khuyết tật;",
    "Căn cứ Quy chế chuyên môn, Quy chế làm việc, các quy định nội bộ của nhà trường và điều kiện thực tế về học sinh, đội ngũ, cơ sở vật chất, thiết bị dạy học, hạ tầng công nghệ của Trường THCS Tân Phong,"
]

for idx, ctext in enumerate(cancu_texts):
    p_cc = doc.paragraphs[4 + idx]
    p_cc.text = ctext
    p_cc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cc.paragraph_format.first_line_indent = Inches(0.5)
    p_cc.paragraph_format.line_spacing = 1.2
    p_cc.paragraph_format.space_before = Pt(2)
    p_cc.paragraph_format.space_after = Pt(3)
    set_font_run(p_cc.runs[0], size_pt=13, bold=False, italic=True)

# P19: Trường THCS Tân Phong xây dựng kế hoạch giáo dục nhà trường năm học 2026 – 2027 như sau:
p19 = doc.paragraphs[19]
p19.text = "Trường THCS Tân Phong xây dựng kế hoạch giáo dục nhà trường năm học 2026 – 2027 như sau:"
p19.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p19.paragraph_format.first_line_indent = Inches(0.5)
p19.paragraph_format.line_spacing = 1.2
p19.paragraph_format.space_before = Pt(3)
p19.paragraph_format.space_after = Pt(4)
set_font_run(p19.runs[0], size_pt=13, bold=False, italic=False)

print("4. Standardizing all remaining Body Paragraphs (P20 to P436)...")
for p_idx in range(20, len(doc.paragraphs)):
    p = doc.paragraphs[p_idx]
    txt = p.text.strip()
    if not txt:
        continue
    
    # Check if heading
    is_major_heading = txt.startswith(('II.', 'III.', 'IV.', 'V.', 'VI.', 'VII.', 'VIII.'))
    is_sub_heading = any(txt.startswith(f"{num}. ") for num in range(1, 20)) or any(txt.startswith(f"{num}.{sub}") for num in range(1, 10) for sub in range(1, 10))
    is_all_bold = all(r.bold for r in p.runs if r.text.strip()) if p.runs else False
    
    p.paragraph_format.line_spacing = 1.2
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if is_major_heading:
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        for r in p.runs:
            set_font_run(r, size_pt=13, bold=True)
    elif is_sub_heading and is_all_bold:
        p.paragraph_format.first_line_indent = Inches(0.5)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            set_font_run(r, size_pt=13, bold=True)
    else:
        # Standard paragraph or bullet line
        p.paragraph_format.first_line_indent = Inches(0.5)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        for r in p.runs:
            # Preserve bold and italic within text, set 13pt Times New Roman
            r_bold = r.bold if r.bold is not None else False
            r_italic = r.italic if r.italic is not None else False
            set_font_run(r, size_pt=13, bold=r_bold, italic=r_italic)

print("5. Standardizing Tables 1 to 10 (Data Tables)...")
for t_idx in range(1, 11):
    table = doc.tables[t_idx]
    set_table_borders(table, color="000000", sz="4")
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    num_cols = len(table.columns)
    table_font_size = 10.0 if num_cols >= 10 else 11.0
    
    for r_idx, row in enumerate(table.rows):
        set_cant_split(row)
        if r_idx == 0:
            set_tbl_header(row)
            
        for cell in row.cells:
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            for p in cell.paragraphs:
                p.paragraph_format.first_line_indent = Inches(0)
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                for r in p.runs:
                    r_bold = r.bold if r.bold is not None else (r_idx == 0)
                    r_italic = r.italic if r.italic is not None else False
                    set_font_run(r, size_pt=table_font_size, bold=r_bold, italic=r_italic)

print("6. Standardizing Signature Table (Table 11)...")
t11 = doc.tables[11]
remove_table_borders(t11)
t11.alignment = WD_TABLE_ALIGNMENT.CENTER
t11.autofit = False

col_widths_t11 = [Mm(70), Mm(95)]
for row in t11.rows:
    for c_idx, width in enumerate(col_widths_t11):
        cell = row.cells[c_idx]
        cell.width = width
        set_cell_margins(cell, top=0, bottom=0, left=0, right=0)

# Cell (0,0): Nơi nhận
c_nn = t11.rows[0].cells[0]
for p_idx, p in enumerate(c_nn.paragraphs):
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.first_line_indent = Inches(0)
    if p_idx == 0:
        p.text = "Nơi nhận:"
        set_font_run(p.runs[0], size_pt=12, bold=True, italic=True)
    elif p_idx == 1:
        p.text = "- Phòng Văn hóa - Xã hội phường Tân Triều;"
        set_font_run(p.runs[0], size_pt=11, bold=False, italic=False)
    elif p_idx == 2:
        p.text = "- Phó HT, Tổ CM, Tổ VP;"
        set_font_run(p.runs[0], size_pt=11, bold=False, italic=False)
    elif p_idx == 3:
        p.text = "- Lưu: VT."
        set_font_run(p.runs[0], size_pt=11, bold=False, italic=False)

# Cell (0,1): HIỆU TRƯỞNG & Chữ ký
c_sign = t11.rows[0].cells[1]
# Clear paragraphs and build cleanly
for p in c_sign.paragraphs:
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Inches(0)

p_ht = c_sign.paragraphs[0]
p_ht.text = "HIỆU TRƯỞNG"
p_ht.paragraph_format.space_before = Pt(0)
p_ht.paragraph_format.space_after = Pt(0)
set_font_run(p_ht.runs[0], size_pt=13, bold=True, italic=False)

p_space = c_sign.paragraphs[1] if len(c_sign.paragraphs) > 1 else c_sign.add_paragraph()
p_space.text = ""
p_space.paragraph_format.space_before = Pt(36)
p_space.paragraph_format.space_after = Pt(0)

p_name = c_sign.paragraphs[2] if len(c_sign.paragraphs) > 2 else c_sign.add_paragraph()
p_name.text = "Phạm Thị Hồng Nghĩa"
p_name.paragraph_format.space_before = Pt(0)
p_name.paragraph_format.space_after = Pt(0)
set_font_run(p_name.runs[0], size_pt=13, bold=True, italic=False)

print(f"7. Saving standardized document to {OUTPUT_PATH}...")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
doc.save(OUTPUT_PATH)
print("SUCCESS: File saved successfully!")
