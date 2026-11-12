# -*- coding: utf-8 -*-
"""
Script sinh 7 tệp DOCX chuẩn thể thức NĐ 30/2020/NĐ-CP và 100% Word Equation OMML
Giáo viên dạy minh họa: Cô Lê Thị Bình - Lớp 8/1 - Tiết 16 (28/10/2026)
Tổ trưởng chuyên môn: Thầy Hoàng Tấn Thiên
Thư mục xuất: TROLYTHIEN/1_SOAN_KHBD/Ket_qua/10.11/NCBH_DINH_LY_THALES_TOAN_8/
"""

import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("TROLYTHIEN/engine"))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from word_math_helper import add_text_with_math

OUTPUT_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\1_SOAN_KHBD\Ket_qua\10.11\NCBH_DINH_LY_THALES_TOAN_8"
IMG_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_page(doc):
    for s in doc.sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(0.79)
        s.bottom_margin = Inches(0.79)
        s.left_margin = Inches(1.18)
        s.right_margin = Inches(0.59)

def set_cell_margins(cell, top=70, bottom=70, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_bg(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="000000", sz="4", val="single"):
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

def make_header_block(doc, left_lines, doc_num, date_str):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell_l = tbl.cell(0, 0)
    cell_r = tbl.cell(0, 1)
    cell_l.width = Inches(3.0)
    cell_r.width = Inches(3.5)
    
    set_cell_margins(cell_l, 0, 0, 0, 0)
    set_cell_margins(cell_r, 0, 0, 0, 0)
    
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.15
    p_l.paragraph_format.space_after = Pt(2)
    for idx, line in enumerate(left_lines):
        r = p_l.add_run(line + "\n")
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        if idx >= 1:
            r.bold = True
    r_num = p_l.add_run(doc_num)
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(11)
    
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.15
    p_r.paragraph_format.space_after = Pt(2)
    r1 = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r1.bold = True
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r2 = p_r.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r2.bold = True
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(12)
    r_d = p_r.add_run(date_str)
    r_d.italic = True
    r_d.font.name = "Times New Roman"
    r_d.font.size = Pt(12)
    
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_after = Pt(6)

def add_p(doc, text="", bold=False, italic=False, size=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3, line_spacing=1.2, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        add_text_with_math(p, text, default_size_pt=size, default_font="Times New Roman", bold=bold, italic=italic, color_rgb=color if color else (0,0,0))
    return p

def add_callout(doc, text, title="LƯU Ý TRỌNG TÂM:", border_color="16A34A", bg_color="F0FDF4"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=100, bottom=100, left=140, right=100)
    set_cell_bg(cell, bg_color)
    
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
    
    add_text_with_math(p, text, default_size_pt=12, default_font="Times New Roman")
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_signatures(doc, left_title, left_name, right_title, right_name, left_sub="", right_sub=""):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cl = tbl.cell(0, 0)
    cr = tbl.cell(0, 1)
    cl.width = Inches(3.2)
    cr.width = Inches(3.3)
    set_cell_margins(cl, 0, 0, 0, 0)
    set_cell_margins(cr, 0, 0, 0, 0)
    
    pl = cl.paragraphs[0]
    pl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pl.paragraph_format.line_spacing = 1.15
    rl1 = pl.add_run(left_title + "\n")
    rl1.bold = True
    rl1.font.name = "Times New Roman"
    rl1.font.size = Pt(12)
    if left_sub:
        rls = pl.add_run(left_sub + "\n")
        rls.italic = True
        rls.font.name = "Times New Roman"
        rls.font.size = Pt(11)
    pl.add_run("\n\n\n\n")
    rl2 = pl.add_run(left_name)
    rl2.bold = True
    rl2.font.name = "Times New Roman"
    rl2.font.size = Pt(12)
    
    pr = cr.paragraphs[0]
    pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pr.paragraph_format.line_spacing = 1.15
    rr1 = pr.add_run(right_title + "\n")
    rr1.bold = True
    rr1.font.name = "Times New Roman"
    rr1.font.size = Pt(12)
    if right_sub:
        rrs = pr.add_run(right_sub + "\n")
        rrs.italic = True
        rrs.font.name = "Times New Roman"
        rrs.font.size = Pt(11)
    pr.add_run("\n\n\n\n")
    rr2 = pr.add_run(right_name)
    rr2.bold = True
    rr2.font.name = "Times New Roman"
    rr2.font.size = Pt(12)

# =============================================================
# DOC 1: KẾ HOẠCH TỔ CHỨC SHCM THEO NCBH
# =============================================================
def build_doc_1():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(doc, ["PHÒNG GIÁO DỤC VÀ ĐÀO TẠO", "TRƯỜNG THCS TRẦN PHÚ - TỔ TOÁN – TIN"], "Số: 10/KH-TTIN", "Xuân Đông, ngày 20 tháng 10 năm 2026")
    
    p = add_p(doc, "KẾ HOẠCH", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    p = add_p(doc, "TỔ CHỨC SINH HOẠT CHUYÊN MÔN THEO NGHIÊN CỨU BÀI HỌC", bold=True, size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    p = add_p(doc, "HỌC KỲ I - NĂM HỌC 2026 - 2027", bold=True, size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4)
    p = add_p(doc, "Chuyên đề: Đổi mới phương pháp dạy học Hình học 8 thông qua chủ đề \"Bài 15. Định lí Thalès trong tam giác\" - Trọng tâm Nghiên cứu bài học Tiết 1 (Tiết 16: Đoạn thẳng tỉ lệ và Định lí Thalès thuận) gắn với Giáo dục STEM và Chuyển đổi số", italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8)
    
    add_callout(doc, 
        "Bài 15: Định lí Thalès trong tam giác gồm 3 tiết (Tiết 16, 17, 18 - Tuần 8, 9). Tổ Toán – Tin học thống nhất phương án tập trung: NGHIÊN CỨU BÀI HỌC CHUYÊN SÂU TIẾT 1 (Tiết 16: Đoạn thẳng tỉ lệ & Định lí Thalès thuận trong tam giác). Giáo viên thực hiện dạy minh họa: Cô Lê Thị Bình tại Lớp 8/1 (Sĩ số: 42/43) vào Tiết 7 (13h45 – 14h30) ngày 28/10/2026. Các tiết 17, 18 sẽ kế thừa và vận dụng kết quả rút kinh nghiệm từ tiết dạy minh họa này.",
        title="ĐỒNG BỘ PPCT PHỤ LỤC 3 TOÁN 8 & PHÂN CÔNG GIẢNG DẠY:"
    )
    
    add_p(doc, "I. CĂN CỨ XÂY DỰNG KẾ HOẠCH", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "- Căn cứ Nghị định số 30/2020/NĐ-CP ngày 05/3/2020 của Chính phủ về công tác văn thư;")
    add_p(doc, "- Căn cứ Thông tư số 32/2018/TT-BGDĐT ngày 26/12/2018 của Bộ Giáo dục và Đào tạo ban hành Chương trình GDPT 2018 môn Toán;")
    add_p(doc, "- Căn cứ Công văn số 5555/BGDĐT-GDTrH ngày 08/10/2014 của Bộ Giáo dục và Đào tạo về hướng dẫn sinh hoạt chuyên môn đổi mới PPDH và kiểm tra đánh giá;")
    add_p(doc, "- Căn cứ Công văn số 5512/BGDĐT-GDTrH ngày 18/12/2020 của Bộ GD&ĐT về xây dựng và tổ chức thực hiện kế hoạch giáo dục;")
    add_p(doc, "- Căn cứ Kế hoạch giáo dục nhà trường và Phân phối chương trình Phụ lục 3 môn Toán 8 năm học 2026 - 2027.")
    
    add_p(doc, "II. MỤC ĐÍCH, YÊU CẦU", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Mục đích:", bold=True)
    add_p(doc, "• Đổi mới căn bản sinh hoạt tổ chuyên môn: Chuyển từ hình thức sinh hoạt hành chính sang sinh hoạt chuyên môn lấy người học làm trung tâm theo Công văn số 5555/BGDĐT-GDTrH.")
    add_p(doc, "• Tháo gỡ rào cản nhận thức của học sinh khối 8: Giúp học sinh nắm vững tỉ số đoạn thẳng, đoạn thẳng tỉ lệ, quy tắc đổi đơn vị đo và vận dụng định lí Thalès thuận.")
    add_p(doc, "• Đẩy mạnh ứng dụng công nghệ và chuyển đổi số: Tích hợp Năng lực số (NLS 5.3.TC2a) qua phần mềm hình học động GeoGebra trên Tivi tương tác thông minh.")
    add_p(doc, "2. Yêu cầu:", bold=True)
    add_p(doc, "• Nguyên tắc cốt tử: Tuyệt đối KHÔNG đánh giá, xếp loại giáo viên dạy minh họa. Toàn bộ quá trình dự giờ và thảo luận tập trung 100% vào việc quan sát hoạt động học của học sinh.")
    add_p(doc, "• 100% giáo viên trong Tổ Toán – Tin học (09 giáo viên) tham dự đầy đủ 4 bước.")
    
    add_p(doc, "III. TIẾN TRÌNH THỰC HIỆN (4 BƯỚC CHUẨN CÔNG VĂN 5555)", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "• Bước 1: Xây dựng Kế hoạch bài dạy minh họa Tiết 16 (14h00 Thứ Ba, ngày 20/10/2026). Chủ trì: Thầy Hoàng Tấn Thiên; Thư ký: Cô Nguyễn Thị Thảo; Báo cáo dự thảo: Cô Lê Thị Bình cùng nhóm giáo viên Toán 8.")
    add_p(doc, "• Bước 2: Tổ chức dạy minh họa và dự giờ quan sát (Tiết 7, 13h45 – 14h30 Thứ Tư ngày 28/10/2026 tại Lớp 8/1 do Cô Lê Thị Bình thực hiện). Toàn tổ dự giờ ghi chép Phiếu quan sát.")
    add_p(doc, "• Bước 3: Phân tích, suy ngẫm sau tiết dạy (15h00 Thứ Tư ngày 28/10/2026 tại Phòng học thông minh). Tập trung phân tích hoạt động học của học sinh.")
    add_p(doc, "• Bước 4: Vận dụng và nhân rộng kết quả vào giảng dạy đại trà tại các lớp 8/2, 8/3, 8/4 và các tiết tiếp theo (Tiết 17, 18).")
    
    add_p(doc, "IV. BẢNG PHÂN CÔNG NHIỆM VỤ CỤ THỂ TOÀN TỔ", bold=True, size=13, space_before=4, space_after=2)
    
    headers = ["STT", "Họ và tên", "Chức vụ / Bộ môn", "Nhiệm vụ cụ thể trong chuyên đề NCBH", "Thời gian", "Ghi chú"]
    rows = [
        ["1", "Hoàng Tấn Thiên", "Tổ trưởng chuyên môn\n(Toán 6)", "• Chỉ đạo chung, duyệt Kế hoạch và KHBD minh họa.\n• Chủ trì cuộc họp Bước 1 và điều hành thảo luận Bước 3.\n• Dự giờ quan sát nhóm học sinh.", "20/10 – 30/10", "Tổ trưởng"],
        ["2", "Trần Sáng", "Phó Tổ trưởng\n(Toán 9, Tin 9)", "• Cố vấn phương pháp dạy học hình học.\n• Dự giờ và tham gia đóng góp ý kiến phân tích ở Bước 3.", "20/10 – 28/10", "Phó Tổ trưởng"],
        ["3", "Lê Thị Bình", "Giáo viên môn Toán\n(Toán 8, Toán 7)", "• Trực tiếp xây dựng KHBD và dạy minh họa Tiết 16 tại Lớp 8/1.\n• Báo cáo dự thảo ở Bước 1 và chia sẻ cảm nhận ở Bước 3.", "20/10 – 28/10", "GV dạy minh họa"],
        ["4", "Trần Long Hải", "Giáo viên môn Toán\n(Toán 8, GVCN 8/3)", "• Nhóm cốt cán Toán 8: Góp ý xây dựng KHBD Bước 1.\n• Dự giờ ghi chép phiếu quan sát nhóm HS; phát biểu ở Bước 3.\n• Vận dụng dạy Tiết 16 tại lớp 8/3, 8/4.", "20/10 – 05/11", "Nhóm Toán 8"],
        ["5", "Hoàng Xuân Ánh", "Giáo viên Toán - Tin\n(Toán 8, Tin 6)", "• Nhóm cốt cán Toán 8: Góp ý Rubric và bài toán STEM.\n• Dự giờ quan sát nhóm 4, nhóm 6; phát biểu ở Bước 3.\n• Vận dụng dạy Tiết 16 tại lớp 8/2.", "20/10 – 05/11", "Nhóm Toán 8"],
        ["6", "Dương Quang Tùng", "Giáo viên Tin học\n(Tin 7, 8, 9)", "• Hỗ trợ CNTT: Cài đặt tệp mô phỏng GeoGebra trên Tivi cảm ứng lớp 8/1.\n• Dự giờ quan sát tương tác số của HS; phát biểu ở Bước 3.", "20/10 – 28/10", "Hỗ trợ CNTT"],
        ["7", "Nguyễn Thị Thảo", "Giáo viên Toán - Tin\n(Toán 6, 7, Tin 6, 7)", "• Thư ký ghi chép biên bản cuộc họp Bước 1 và Bước 3.\n• Dự giờ quan sát hoạt động nhóm; phát biểu ở Bước 3.", "20/10 – 28/10", "Thư ký"],
        ["8", "Hồ Đăng Danh", "Giáo viên môn Toán\n(Toán 9)", "• Dự giờ, quan sát học sinh tiếp nhận nhiệm vụ.\n• Tham gia đóng góp ý kiến phân tích sư phạm ở Bước 3.", "28/10/2026", "GV môn Toán"],
        ["9", "Nguyễn Văn Tính", "Giáo viên môn Toán\n(Toán 6, Toán 7)", "• Dự giờ, quan sát hoạt động luyện tập của học sinh.\n• Tham gia đóng góp ý kiến ở Bước 3.", "28/10/2026", "GV môn Toán"]
    ]
    
    col_w = [Inches(0.4), Inches(1.2), Inches(1.3), Inches(2.5), Inches(0.8), Inches(0.9)]
    tbl = doc.add_table(rows=len(rows)+1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl)
    
    # header row
    for i, h in enumerate(headers):
        c = tbl.cell(0, i)
        c.width = col_w[i]
        set_cell_bg(c, "F2F2F2")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            c = tbl.cell(r_idx+1, c_idx)
            c.width = col_w[c_idx]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 4, 5] else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            if c_idx == 1:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    add_p(doc, "V. TỔ CHỨC THỰC HIỆN VÀ HỒ SƠ LƯU TRỮ", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "Bộ hồ sơ minh chứng lưu tại Tổ chuyên môn gồm 6 tệp chuẩn (NCBH_01 đến NCBH_06) kèm theo Tệp Hướng dẫn trọng tâm NCBH_Chu_Y.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    add_signatures(doc, "PHÊ DUYỆT CỦA BAN GIÁM HIỆU\nHIỆU TRƯỞNG", "Đinh Văn Đông", "TỔ TRƯỞNG CHUYÊN MÔN", "Hoàng Tấn Thiên")
    
    doc.save(os.path.join(OUTPUT_DIR, "NCBH_01_Ke_Hoach_Sinh_Hoat_Chuyen_Mon.docx"))
    print("Created DOCX 1: NCBH_01_Ke_Hoach_Sinh_Hoat_Chuyen_Mon.docx")

# =============================================================
# DOC 2: BIÊN BẢN BƯỚC 1 XÂY DỰNG KHBD
# =============================================================
def build_doc_2():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(doc, ["PHÒNG GIÁO DỤC VÀ ĐÀO TẠO", "TRƯỜNG THCS TRẦN PHÚ - TỔ TOÁN – TIN"], "Số: .../BB-TTIN", "Xuân Đông, ngày 20 tháng 10 năm 2026")
    
    add_p(doc, "BIÊN BẢN HỌP TỔ CHUYÊN MÔN", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "BƯỚC 1: XÂY DỰNG KẾ HOẠCH BÀI DẠY MINH HỌA", bold=True, size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "Chuyên đề Nghiên cứu bài học môn Toán 8 - Học kỳ I năm học 2026 - 2027", italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "Bài dạy: Bài 15. Định lí Thalès trong tam giác (Tiết 1 - Tiết 16: Đoạn thẳng tỉ lệ và Định lí Thalès thuận)", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8)
    
    add_p(doc, "I. THỜI GIAN, ĐỊA ĐIỂM, THÀNH PHẦN", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Thời gian: 14 giờ 00 phút, ngày 20 tháng 10 năm 2026.")
    add_p(doc, "2. Địa điểm: Phòng học thông minh - Trường THCS Trần Phú.")
    add_p(doc, "3. Chủ trì cuộc họp: Thầy Hoàng Tấn Thiên – Tổ trưởng chuyên môn.")
    add_p(doc, "4. Thư ký cuộc họp: Cô Nguyễn Thị Thảo – Giáo viên môn Toán - Tin.")
    add_p(doc, "5. Thành phần tham dự: 09/09 giáo viên tổ Toán – Tin (Vắng: 0).")
    
    add_p(doc, "II. NỘI DUNG CUỘC HỌP", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Quán triệt tinh thần chuyên đề (Thầy Hoàng Tấn Thiên):", bold=True)
    add_p(doc, "Tổ chuyên môn thống nhất lựa chọn Tiết 16 (Tiết 1 của Bài 15: Đoạn thẳng tỉ lệ & Định lí Thalès thuận) để thực hiện NCBH. Phân công cô Lê Thị Bình trực tiếp dạy minh họa tại Lớp 8/1 vào Tiết 7 ngày 28/10/2026.")
    
    add_p(doc, "2. Báo cáo ý tưởng thiết kế bài dạy (Cô Lê Thị Bình):", bold=True)
    add_p(doc, "Cô Bình trình bày 4 hoạt động: Khởi động cây cầu qua sông (6p); Đoạn thẳng tỉ lệ (10p); Định lí Thalès thuận & GeoGebra NLS 5.3.TC2a (12p); Luyện tập 3 hình 4.6 (12p); Vận dụng STEM hố cát nhảy xa 3,75m (5p); Dặn dò và tóm tắt tiến trình Tiết 17, 18.")
    
    add_p(doc, "3. Ý kiến thảo luận đóng góp của các thành viên:", bold=True)
    add_p(doc, "• Thầy Trần Long Hải (Toán 8): Nhất trí cao với giáo án cô Bình. Nhấn mạnh lưu ý cốt tử: Không đưa tỉ số cạnh đáy vào Tiết 16 kẻo học sinh nhầm sang Hệ quả Thalès.")
    add_p(doc, "• Thầy Hoàng Xuân Ánh (Toán 8): Lưu ý học sinh hay quên đổi đơn vị đo ở Luyện tập 1b ($HK = 10\\text{ dm} = 100\\text{ cm}$). Bài toán hố cát nhảy xa rất thực tế và hay.")
    add_p(doc, "• Thầy Dương Quang Tùng (Tin học): Đã cài đặt tệp GeoGebra động trên Tivi tương tác lớp 8/1 sẵn sàng phục vụ tiết dạy.")
    add_p(doc, "• Thầy Hồ Đăng Danh & Thầy Trần Sáng: Thống nhất phiếu học tập số 1, phiếu số 2 và bảng Rubric 3 mức độ.")
    
    add_p(doc, "4. Kết luận của Chủ trì cuộc họp (Thầy Hoàng Tấn Thiên):", bold=True)
    add_p(doc, "Thông qua Kế hoạch bài dạy minh họa Tiết 16. Giao cô Lê Thị Bình hoàn thiện KHBD và thực hiện dạy minh họa vào Tiết 7 ngày 28/10/2026 tại Lớp 8/1.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    add_signatures(doc, "THƯ KÝ CUỘC HỌP", "Nguyễn Thị Thảo", "TỔ TRƯỞNG CHUYÊN MÔN", "Hoàng Tấn Thiên")
    
    doc.save(os.path.join(OUTPUT_DIR, "NCBH_02_Bien_Ban_Buoc_1_Xay_Dung_Ke_Hoach_Bai_Day.docx"))
    print("Created DOCX 2: NCBH_02_Bien_Ban_Buoc_1_Xay_Dung_Ke_Hoach_Bai_Day.docx")

build_doc_1()
build_doc_2()

# =============================================================
# DOC 3: KẾ HOẠCH BÀI DẠY MINH HỌA TIẾT 16 (CÔ LÊ THỊ BÌNH)
# =============================================================
def add_img(p, name, width=3.0):
    img_path = os.path.join(IMG_DIR, name)
    if os.path.exists(img_path):
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run()
        run.add_picture(img_path, width=Inches(width))

def make_2col_table(doc, left_text_list, right_text_list, left_w=3.4, right_w=3.4):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl)
    
    # header
    c0 = tbl.cell(0, 0)
    c1 = tbl.cell(0, 1)
    c0.width = Inches(left_w)
    c1.width = Inches(right_w)
    set_cell_bg(c0, "F2F2F2")
    set_cell_bg(c1, "F2F2F2")
    
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p0.add_run("HOẠT ĐỘNG CỦA GV VÀ HS")
    r0.bold = True
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(11)
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p1.add_run("SẢN PHẨM DỰ KIẾN")
    r1.bold = True
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    
    # content row
    row = tbl.add_row()
    cell_l = row.cells[0]
    cell_r = row.cells[1]
    cell_l.width = Inches(left_w)
    cell_r.width = Inches(right_w)
    set_cell_margins(cell_l, 60, 60, 70, 70)
    set_cell_margins(cell_r, 60, 60, 70, 70)
    
    # populate left
    for idx, item in enumerate(left_text_list):
        p = cell_l.paragraphs[0] if idx == 0 else cell_l.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        if isinstance(item, tuple) and item[0] == "IMG":
            add_img(p, item[1], item[2])
        else:
            add_text_with_math(p, str(item), default_size_pt=11, default_font="Times New Roman")
            
    # populate right
    for idx, item in enumerate(right_text_list):
        p = cell_r.paragraphs[0] if idx == 0 else cell_r.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        if isinstance(item, tuple) and item[0] == "IMG":
            add_img(p, item[1], item[2])
        else:
            add_text_with_math(p, str(item), default_size_pt=11, default_font="Times New Roman")
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_doc_3():
    doc = docx.Document()
    setup_page(doc)
    
    p = add_p(doc, "KHBD NGHIÊN CỨU BÀI HỌC", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    p = add_p(doc, "LỚP DẠY: 8/1 (sĩ số: 42/43)", bold=True, size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    p = add_p(doc, "NGÀY DẠY: Tiết 7 ngày 28/10/2026 (13h45 => 14h30)", italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    p = add_p(doc, "TIẾT DẠY: Tiết 16 (Tiết 1 của bài)", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    p = add_p(doc, "GIÁO VIÊN DẠY: LÊ THỊ BÌNH", bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
    
    add_p(doc, "CHƯƠNG IV: ĐỊNH LÍ THALÈS", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2)
    add_p(doc, "BÀI 15: ĐỊNH LÍ THALÈS TRONG TAM GIÁC", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "Thời lượng thực hiện: 03 tiết (Tiết 16, 17, 18 - Tuần 8, 9 theo PPCT Phụ lục 3)", italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
    
    add_p(doc, "I. MỤC TIÊU:", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Về kiến thức:", bold=True)
    add_p(doc, "- Nắm vững định nghĩa tỉ số của hai đoạn thẳng và các đoạn thẳng tỉ lệ;")
    add_p(doc, "- Hiểu, phát biểu chuẩn xác định lí Thalès thuận trong tam giác và viết được giả thiết, kết luận, 3 hệ thức tỉ số tương ứng (Tiết 16);")
    add_p(doc, "- Hiểu và phát biểu được định lí Thalès đảo trong tam giác, biết vận dụng để nhận biết và chứng minh hai đường thẳng song song (Tiết 17);")
    add_p(doc, "- Vận dụng định lí Thalès và tính chất hình học để giải quyết bài toán thực tế đo khoảng cách hai điểm ngoài trời theo phương pháp STEM (Tiết 18).")
    
    add_p(doc, "2. Về năng lực:", bold=True)
    add_p(doc, "a. Năng lực chung:")
    add_p(doc, "- Tự chủ và tự học: Tự giác thực hiện các nhiệm vụ khám phá trên phiếu học tập, chủ động nghiên cứu ví dụ trong SGK.")
    add_p(doc, "- Giao tiếp và hợp tác: Tương tác tích cực, phân vai hiệu quả trong nhóm 4 học sinh; biết lắng nghe, phản biện và thống nhất kết quả.")
    add_p(doc, "b. Năng lực đặc thù môn Toán:")
    add_p(doc, "- Năng lực tư duy và lập luận toán học: So sánh các tỉ số đoạn thẳng trên lưới ô vuông; phát hiện quy luật tỉ lệ bất biến khi đường thẳng song song di chuyển.")
    add_p(doc, "- Năng lực mô hình hóa toán học: Chuyển đổi bài toán thực tế đo khoảng cách hai điểm ở hai bờ sông, đo khoảng cách hai điểm ở hố cát nhảy ở sân trường thành mô hình tam giác có các đường thẳng song song.")
    add_p(doc, "- Năng lực giải quyết vấn đề toán học: Lập phương trình tỉ số để tìm độ dài x, y của các cạnh trong tam giác.")
    add_p(doc, "c. Năng lực số (NLS):")
    add_p(doc, "- Tích hợp NLS 5.3.TC2a: Học sinh sử dụng và quan sát phần mềm hình học động GeoGebra để trực quan hóa việc thay đổi vị trí điểm, kiểm chứng các cặp đoạn thẳng tỉ lệ không đổi khi đường thẳng song song với cạnh đáy tam giác.")
    add_p(doc, "d. Năng lực STEM:")
    add_p(doc, "- Chế tạo mô hình đo đơn giản và thực hành đo gián tiếp khoảng cách hai điểm ngoài thực tế.")
    
    add_p(doc, "3. Về phẩm chất:", bold=True)
    add_p(doc, "- Chăm chỉ: Cẩn thận, tỉ mỉ trong đo đạc và tính toán tỉ số.")
    add_p(doc, "- Trách nhiệm: Nghiêm túc hoàn thành nhiệm vụ được nhóm phân công, có tinh thần tương trợ bạn học còn thao tác chậm.")
    add_p(doc, "- Trung thực: Tôn trọng số liệu đo đạc thực tế ngoài trời, không gán ghép số liệu giả tạo.")
    
    add_p(doc, "II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Đối với GV:")
    add_p(doc, "- Màn hình tương tác / Tivi thông minh kết nối máy tính;")
    add_p(doc, "- Phần mềm GeoGebra với tệp mô phỏng định lí Thalès động;")
    add_p(doc, "- 08 bộ Phiếu học tập số 1, số 2 in sẵn khổ A3, bút lông dạ nhiều màu;")
    add_p(doc, "- Thước dây cuộn 10m, mô hình cọc đo bóng nắng 1.4m và giác kế mini phục vụ tiết 18 STEM ngoài trời.")
    add_p(doc, "2. Đối với HS:")
    add_p(doc, "- Sách giáo khoa Toán 8 Tập 1 (Kết nối tri thức với cuộc sống);")
    add_p(doc, "- Thước thẳng chia milimét, êke, compa, bút dạ, bảng phụ nhóm.")
    
    add_p(doc, "III. PHÂN BỔ NỘI DUNG 3 TIẾT THEO PHỤ LỤC 3", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "- Tiết 1 (Tiết 16 - Tuần 8, Cuối tháng 10): Đoạn thẳng tỉ lệ & Định lí Thalès thuận trong tam giác (Tiết dạy minh họa Nghiên cứu bài học tại Lớp 8/1).")
    add_p(doc, "- Tiết 2 (Tiết 17 - Tuần 8/9): Định lí Thalès đảo trong tam giác.")
    add_p(doc, "- Tiết 3 (Tiết 18 - Tuần 9, Đầu tháng 11): Luyện tập & Hoạt động thực hành STEM đo khoảng cách thực tế.")
    
    add_p(doc, "IV. TIẾN TRÌNH DẠY HỌC — TIẾT 16", bold=True, size=13, space_before=6, space_after=2)
    
    # ------------------ HOẠT ĐỘNG 1 ------------------
    add_p(doc, "A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (6 phút)", bold=True, size=12.5, space_before=2, space_after=1)
    add_p(doc, "a) Mục tiêu: Tạo hứng thú, thu hút HS tìm hiểu nội dung bài học.")
    add_p(doc, "b) Nội dung: HS dự đoán câu trả lời bài mở đầu, suy nghĩ trả lời câu hỏi.")
    add_p(doc, "c) Sản phẩm: HS đọc bài mở đầu, bước đầu hình dung về nội dung sẽ học: Định lí Thalès.")
    add_p(doc, "d) Tổ chức thực hiện:", space_after=2)
    
    h1_left = [
        "+ Bước 1: Chuyển giao nhiệm vụ:",
        "- GV: Chiếu đoạn video về hình ảnh Cây cầu $AB$ bắc qua một con sông có chiều rộng $300\\text{ m}$. Để đo khoảng cách giữa hai điểm $C$ và $D$ trên hai bờ con sông, người ta chọn một điểm $E$ trên đường thẳng $AB$ sao cho ba điểm $E, C, D$ thẳng hàng. Trên mặt đất, người ta đo được $AE = 400\\text{ m}, EC = 500\\text{ m}$. Theo em, người ta tính khoảng cách giữa $C$ và $D$ như thế nào?",
        "+ Bước 2: Thực hiện nhiệm vụ:",
        "- HS: Quan sát tranh ảnh trên màn hình, suy nghĩ, trao đổi nhanh theo cặp đôi bàn.",
        "+ Bước 3: Báo cáo, thảo luận:",
        "- GV: Mời đại diện 2 học sinh chia sẻ phán đoán.",
        "+ Bước 4: Kết luận, nhận định:",
        "- GV: Khen ngợi trực giác toán học xuất sắc của HS và dẫn dắt vào bài mới."
    ]
    h1_right = [
        ("IMG", "hinh_1_khoi_dong_cay_cau.png", 2.8),
        "Hình 4.1 SGK trang 76: Cây cầu AB qua sông.",
        "Dự đoán ban đầu của học sinh: Khoảng cách $CD$ có thể tính gián tiếp thông qua mối liên hệ tỉ lệ với các đoạn thẳng trên bờ sông ($AE = 400\\text{ m}$, $AB = 300\\text{ m}$, $EC = 500\\text{ m}$)."
    ]
    make_2col_table(doc, h1_left, h1_right)
    
    # ------------------ HOẠT ĐỘNG 2.1 ------------------
    add_p(doc, "B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (22 phút)", bold=True, size=12.5, space_before=4, space_after=1)
    add_p(doc, "2.1. Đoạn thẳng tỉ lệ (10 phút)", bold=True, size=12, space_before=2, space_after=1)
    add_p(doc, "a) Mục tiêu: HS nhận biết được khái niệm tỉ số của hai đoạn thẳng và định nghĩa đoạn thẳng tỉ lệ; sử dụng được định nghĩa để so sánh và tính toán.")
    add_p(doc, "b) Nội dung: HS đọc SGK, nghe giảng, thực hiện HĐ 1, 2, 3, Luyện tập 1, 2.")
    add_p(doc, "c) Sản phẩm: Phiếu học tập số 1; phát biểu được khái niệm tỉ số đoạn thẳng, đoạn thẳng tỉ lệ.")
    add_p(doc, "d) Tổ chức thực hiện:", space_after=2)
    
    h21_left = [
        "Nhiệm vụ 1: Tìm hiểu định nghĩa tỉ số của hai đoạn thẳng",
        "Bước 1: Chuyển giao nhiệm vụ:",
        "- GV: Phát Phiếu học tập số 1. Yêu cầu HS thảo luận nhóm đôi, hoàn thành HĐ 1, 2, 3.",
        "HĐ1: $AB = \\dots MN; CD = \\dots MN \\Rightarrow \\frac{AB}{CD} = \\dots$",
        "HĐ2: Đo cm: $AB = \\dots\\text{ cm}; CD = \\dots\\text{ cm} \\Rightarrow \\frac{AB}{CD} = \\dots$",
        "HĐ3: Nhận xét gì về hai tỉ số trên?",
        "- GV đưa ra Nhận xét và yêu cầu HS ghi nhớ.",
        "- GV dẫn dắt và ra kết luận trong hộp kiến thức.",
        "- GV yêu cầu 2 HS lên bảng thực hiện Luyện tập 1.",
        "→ GV chữa bài, chốt đáp án.",
        "Nhiệm vụ 2: Tìm hiểu định nghĩa hai đoạn thẳng tỉ lệ",
        "- GV chiếu Hình 4.3 lên bảng và giải thích về tỉ lệ của 4 đoạn thẳng.",
        "- GV dẫn dắt, ra kết luận trong hộp kiến thức.",
        "- GV yêu cầu HS hoàn thành Luyện tập 2 theo nhóm bàn bằng cách đếm ô vuông.",
        "→ GV chữa bài, chốt đáp án.",
        "Bước 2: Thực hiện nhiệm vụ:",
        "- HS theo dõi SGK, tiếp nhận kiến thức, thảo luận nhóm đôi, trả lời câu hỏi.",
        "Bước 3: Báo cáo, thảo luận:",
        "- HS giơ tay phát biểu, lên bảng trình bày, nhận xét.",
        "Bước 4: Kết luận, nhận định:",
        "+ Tỉ số của hai đoạn thẳng là tỉ số độ dài của chúng theo cùng một đơn vị đo.",
        "+ Nếu $AB$ và $CD$ tỉ lệ với $A'B'$ và $C'D'$ thì $\\frac{AB}{CD} = \\frac{A'B'}{C'D'}$ hay $\\frac{AB}{A'B'} = \\frac{CD}{C'D'}$."
    ]
    h21_right = [
        "1. Đoạn thẳng tỉ lệ",
        "a. Tỉ số của hai đoạn thẳng",
        ("IMG", "hinh_2_ti_so_doan_thang.png", 2.6),
        "HĐ1: $AB = 2\\text{ }MN$; $CD = 6\\text{ }MN$",
        "HĐ2: $AB = 3\\text{ cm}$; $CD = 9\\text{ cm}$",
        "HĐ3: $\\frac{AB}{CD} = \\frac{2}{6} = \\frac{3}{9} = \\frac{1}{3}$. Hai tỉ số bằng nhau.",
        "Nhận xét: Khi thay đổi đơn vị đo, tỉ số độ dài của hai đoạn thẳng $AB$ và $CD$ không thay đổi.",
        "Kết luận: Tỉ số của hai đoạn thẳng là tỉ số độ dài của chúng theo cùng một đơn vị đo.",
        "Luyện tập 1:",
        "a) Tỉ số của $MN = 3\\text{ cm}$ và $PQ = 9\\text{ cm}$ là: $\\frac{MN}{PQ} = \\frac{3}{9} = \\frac{1}{3}$",
        "b) $HK = 10\\text{ dm} = 100\\text{ cm}$. Tỉ số của $EF = 25\\text{ cm}$ và $HK$ là: $\\frac{EF}{HK} = \\frac{25}{100} = \\frac{1}{4}$",
        "b. Đoạn thẳng tỉ lệ",
        ("IMG", "hinh_3_doan_thang_ti_le.png", 2.4),
        "Kết luận: Hai đoạn thẳng $AB$ và $CD$ gọi là tỉ lệ với hai đoạn thẳng $A'B'$ và $C'D'$ nếu có tỉ lệ thức: $\\frac{AB}{CD} = \\frac{A'B'}{C'D'}$ hay $\\frac{AB}{A'B'} = \\frac{CD}{C'D'}$",
        "Luyện tập 2:",
        ("IMG", "hinh_4_luyen_tap_2_luoi_o_vuong.png", 2.6),
        "a) $AB' = 4; AB = 6; AC' = 4; AC = 6$. Ta có: $\\frac{AB'}{AB} = \\frac{AC'}{AC} = \\frac{4}{6} = \\frac{2}{3}$",
        "b) $B'B = 2; C'C = 2$. Ta có: $\\frac{B'B}{AB} = \\frac{C'C}{AC} = \\frac{2}{6} = \\frac{1}{3}$",
        "c) $\\frac{AB'}{B'B} = \\frac{4}{2} = 2; \\frac{AC'}{C'C} = \\frac{4}{2} = 2$. Ta có: $\\frac{AB'}{B'B} = \\frac{AC'}{C'C}$"
    ]
    make_2col_table(doc, h21_left, h21_right)
    
    # ------------------ HOẠT ĐỘNG 2.2 ------------------
    add_p(doc, "2.2. Định lí Thalès trong tam giác (12 phút)", bold=True, size=12, space_before=4, space_after=1)
    add_p(doc, "a) Mục tiêu: HS nhận biết, phát biểu, giải thích được định lí Thalès trong tam giác và sử dụng để tính độ dài đoạn thẳng.")
    add_p(doc, "b) Nội dung: HS quan sát LT2, tương tác GeoGebra, nghiên cứu Ví dụ 1.")
    add_p(doc, "c) Sản phẩm: Phát biểu định lí Thalès trong tam giác, lời giải Ví dụ 1.")
    add_p(doc, "d) Tổ chức thực hiện:", space_after=2)
    
    h22_left = [
        "Bước 1: Chuyển giao nhiệm vụ:",
        "Nhiệm vụ: Tìm hiểu định lí Thalès",
        "- GV yêu cầu HS quan sát lại bài Luyện tập 2 đưa ra các tỉ lệ thức.",
        "- GV dẫn dắt rút ra kết luận trong hộp kiến thức: Khi $B'C' \\parallel BC$ thì ta có các tỉ lệ thức.",
        "Tích hợp NLS 5.3.TC2a: GV mở tệp GeoGebra, gọi 1 đại diện HS lên bảng chạm kéo di chuyển điểm $A$ và điểm $B'$ để cả lớp quan sát các giá trị tỉ số trên bảng dữ liệu tự động nhảy nhưng luôn giữ nguyên dấu bằng.",
        "- GV hướng dẫn HS viết giả thiết, kết luận tóm tắt định lí Thalès.",
        "- GV yêu cầu HS thực hiện Ví dụ 1 (SGK tr.78).",
        "Bước 2: Thực hiện nhiệm vụ:",
        "- HS theo dõi SGK, chú ý nghe, tiếp nhận kiến thức, làm Ví dụ 1.",
        "Bước 3: Báo cáo, thảo luận:",
        "- HS giơ tay phát biểu, lên bảng trình bày.",
        "Bước 4: Kết luận, nhận định:",
        "+ Định lí Thalès thuận định ra trên hai cạnh những đoạn thẳng tương ứng tỉ lệ."
    ]
    h22_right = [
        "2. Định lí Thalès trong tam giác",
        "a. Định lí Thalès",
        "Kết luận: Nếu một đường thẳng song song với một cạnh của tam giác và cắt hai cạnh còn lại thì nó định ra trên hai cạnh đó những đoạn thẳng tương ứng tỉ lệ.",
        ("IMG", "hinh_5_dinh_ly_thales_tong_quat.png", 2.6),
        "GT: $\\Delta ABC, B'C' \\parallel BC$ ($B' \\in AB; C' \\in AC$)",
        "KL: $\\frac{AB'}{AB} = \\frac{AC'}{AC}$; $\\frac{AB'}{B'B} = \\frac{AC'}{C'C}$; $\\frac{B'B}{AB} = \\frac{C'C}{AC}$",
        "Ví dụ 1 (SGK tr.78):",
        "Xét tam giác $DEF$ có $MN \\parallel EF$, theo định lí Thalès ta có: $\\frac{DM}{ME} = \\frac{DN}{NF}$ hay $\\frac{2}{4} = \\frac{x}{5}$, suy ra $x = \\frac{2 \\cdot 5}{4} = 2,5$."
    ]
    make_2col_table(doc, h22_left, h22_right)
    
    # ------------------ HOẠT ĐỘNG 3 ------------------
    add_p(doc, "C. HOẠT ĐỘNG 3: LUYỆN TẬP (12 phút)", bold=True, size=12.5, space_before=4, space_after=1)
    h3_left = [
        "+ Bước 1: Chuyển giao nhiệm vụ:",
        "- GV: Giao nhiệm vụ Luyện tập 3 trên Phiếu học tập số 2: Tìm các độ dài $x, y$ trong Hình 4.6 (SGK tr.79).",
        "+ Bước 2: Thực hiện nhiệm vụ:",
        "- HS: Làm việc cá nhân trong 5 phút. 2 học sinh lên bảng trình bày.",
        "- GV: Quan sát, phát hiện học sinh nhầm giữa các tỉ số để gợi ý điều chỉnh.",
        "+ Bước 3: Báo cáo, thảo luận:",
        "- HS: Hai học sinh trên bảng giải chi tiết và giải thích căn cứ áp dụng định lí Thalès.",
        "- HS: Các học sinh dưới lớp nhận xét, đối chiếu bài làm.",
        "+ Bước 4: Kết luận, nhận định:",
        "- GV: Chốt lời giải chuẩn mực, nhấn mạnh cách trình bày hình học logic: 1) Nêu rõ đường thẳng song song; 2) Áp dụng định lí Thalès; 3) Thay số và tính toán ẩn $x, y$."
    ]
    h3_right = [
        "Luyện tập 3 (SGK tr.79):",
        "a) Tìm x:",
        ("IMG", "hinh_6_luyen_tap_3_hinh_a.png", 2.3),
        "Xét tam giác $ABC$ có $MN \\parallel BC$, theo định lí Thalès ta có: $\\frac{AM}{MB} = \\frac{AN}{NC}$ hay $\\frac{6,5}{x} = \\frac{4}{2}$. Suy ra $x = \\frac{6,5 \\cdot 2}{4} = 3,25$.",
        "b) Tìm y:",
        ("IMG", "hinh_7_luyen_tap_3_hinh_b.png", 1.8),
        "Ta có $EF \\perp PH$ và $HQ \\perp PH \\Rightarrow EF \\parallel HQ$.",
        "Xét tam giác $HPQ$ có $EF \\parallel HQ$, theo định lí Thalès ta có: $\\frac{PE}{EH} = \\frac{PF}{FQ}$ hay $\\frac{4}{EH} = \\frac{5}{3,5}$. Suy ra $EH = \\frac{4 \\cdot 3,5}{5} = 2,8$.",
        "Vậy $y = PH = PE + EH = 4 + 2,8 = 6,8$."
    ]
    make_2col_table(doc, h3_left, h3_right)
    
    # ------------------ HOẠT ĐỘNG 4 ------------------
    add_p(doc, "D. HOẠT ĐỘNG 4: VẬN DỤNG VÀ STEM (5 phút)", bold=True, size=12.5, space_before=4, space_after=1)
    h4_left = [
        "+ Bước 1: Chuyển giao nhiệm vụ:",
        "- GV: Chiếu Hình 3 bài toán STEM đo khoảng cách và giao bài tập thực tế:",
        "Khi chuẩn bị sân bãi cho môn Thể dục, các bạn học sinh cần xác định chiều dài đoạn thẳng $CD$ đi qua mặt hố cát nhảy xa. Do không thể đo trực tiếp trên mặt cát, các bạn đã chọn điểm ngắm $A$ trên sân gạch và đo được các số liệu: $AB = 4\\text{ m}, BE = 3\\text{ m}, AC = 5\\text{ m}$ (biết $BC \\perp AE$ và $ED \\perp AE$). Em hãy giúp các bạn tính xem khoảng cách $CD$ dài bao nhiêu mét?",
        "+ Bước 2: Thực hiện nhiệm vụ:",
        "- HS: Hoạt động nhóm bàn nhanh, phác thảo tam giác $AED$ có $BC \\parallel ED$.",
        "+ Bước 3: Báo cáo, thảo luận:",
        "- HS: Đại diện 1 học sinh giải miệng: tam giác $AED$ có $BC \\parallel ED$, theo định lí Thalès: $\\frac{AB}{BE} = \\frac{AC}{CD}$ hay $\\frac{4}{3} = \\frac{5}{CD}$.",
        "+ Bước 4: Kết luận, nhận định & Dặn dò:",
        "- GV: Khẳng định lời giải chính xác, giải thích đó chính là cách đo khoảng cách giữa 2 điểm mà không cần trực tiếp đi đến nơi."
    ]
    h4_right = [
        ("IMG", "hinh_8_stem_ho_cat_nhay_xa.png", 2.6),
        "Hình 3: Ứng dụng STEM đo khoảng cách 2 điểm ở 2 đầu hố cát nhảy xa.",
        "Lời giải bài toán STEM đo khoảng cách:",
        "- Xét tam giác $AED$ có $BC \\parallel ED$, theo định lí Thalès ta có: $\\frac{AB}{BE} = \\frac{AC}{CD}$ hay $\\frac{4}{3} = \\frac{5}{CD}$. Suy ra $CD = \\frac{3 \\cdot 5}{4} = 3,75\\text{ (m)}$.",
        "Vậy khoảng cách $CD$ dài $3,75\\text{ mét}$."
    ]
    make_2col_table(doc, h4_left, h4_right)
    
    # ------------------ DẶN DÒ & TÓM TẮT TIẾT 17, 18 ------------------
    add_p(doc, "* Dặn dò về nhà chuẩn bị cho Tiết 17, 18:", bold=True, size=12, space_before=4, space_after=1)
    add_p(doc, "1) Học thuộc định lí Thalès thuận, làm bài tập 4.1, 4.2 SGK trang 80;")
    add_p(doc, "2) Chuẩn bị trước nội dung Định lí Thalès đảo cho Tiết 17;")
    add_p(doc, "3) Mỗi nhóm chuẩn bị 1 thước dây cuộn để Tiết 18 thực hành đo khoảng cách 2 điểm ở 2 đầu hố cát nhảy xa.")
    
    add_p(doc, "TÓM TẮT TIẾN TRÌNH TIẾT 17 VÀ TIẾT 18", bold=True, size=12.5, space_before=4, space_after=2)
    add_p(doc, "1. TIẾT 17: ĐỊNH LÍ THALÈS ĐẢO TRONG TAM GIÁC", bold=True)
    add_p(doc, "- Mục tiêu: Học sinh phát biểu được định lí Thalès đảo; biết chứng minh hai đường thẳng song song dựa vào các đoạn thẳng tỉ lệ.")
    add_p(doc, "- Tiến trình: Khởi động kiểm tra bài cũ (4 phút) -> Khám phá Định lí đảo qua hình vẽ đối chứng (15 phút) -> Luyện tập chứng minh song song và nhận biết hình thang (18 phút) -> Vận dụng củng cố (8 phút).")
    
    add_p(doc, "2. TIẾT 18: LUYỆN TẬP VÀ HOẠT ĐỘNG THỰC HÀNH STEM NGOÀI TRỜI", bold=True)
    add_p(doc, "- Mục tiêu: Học sinh vận dụng tổng hợp định lí Thalès thuận, đảo; sử dụng thước dây và cọc tiêu để đo khoảng cách 2 điểm ở 2 đầu hố cát nhảy xa sân trường THCS Trần Phú.")
    add_p(doc, "- Tiến trình:")
    add_p(doc, "  + Hoạt động 1: Ôn tập hệ thống hóa kiến thức 2 định lí bằng Sơ đồ tư duy Mindmap (10 phút).")
    add_p(doc, "  + Hoạt động 2: Phân chia 4 nhóm ra sân trường thực hành đo bóng nắng và góc nghiêng (20 phút).")
    add_p(doc, "  + Hoạt động 3: Báo cáo số liệu đo đạc, tính toán khoảng cách và đánh giá sai số giữa các nhóm (15 phút).")
    
    # ------------------ PHỤ LỤC RUBRIC ------------------
    add_p(doc, "V. PHỤ LỤC HỌC LIỆU VÀ RUBRIC ĐÁNH GIÁ", bold=True, size=12.5, space_before=4, space_after=2)
    add_p(doc, "1. Phiếu học tập số 1 (Khám phá định lí Thalès thuận):", bold=True)
    add_p(doc, "- Nhiệm vụ 1: Đếm ô vuông trên Hình 1 và điền vào chỗ trống: $AB' = \\dots$ ô; $AB = \\dots$ ô; $AC' = \\dots$ ô; $AC = \\dots$ ô.")
    add_p(doc, "- Nhiệm vụ 2: Lập tỉ số: $\\frac{AB'}{AB} = \\dots; \\frac{AC'}{AC} = \\dots \\Rightarrow \\frac{AB'}{AB} = \\frac{AC'}{AC}$.")
    add_p(doc, "- Nhiệm vụ 3: Rút ra kết luận tổng quát khi một đường thẳng song song với cạnh tam giác.")
    
    add_p(doc, "2. Bảng Rubric đánh giá hoạt động học sinh trong chủ đề 3 tiết:", bold=True, space_before=2, space_after=2)
    
    rb_headers = ["Tiêu chí đánh giá", "Mức 1 (Chưa đạt)", "Mức 2 (Đạt)", "Mức 3 (Tốt)"]
    rb_rows = [
        ["1. Khám phá & Phát biểu định lý (Tiết 16, 17)", "Chưa đếm đúng ô lưới, chưa lập được tỉ số tương ứng.", "Đếm đúng ô lưới, lập được tỉ số và phát biểu được định lý.", "Thao tác thành thạo, phát biểu chuẩn xác, tương tác tự tin với mô phỏng GeoGebra."],
        ["2. Kỹ năng tính toán & Chứng minh", "Viết sai tỉ lệ thức hoặc nhầm lẫn giữa các cạnh.", "Viết đúng tỉ lệ thức, thay số tính đúng ẩn số ở bài cơ bản.", "Giải nhanh, trình bày chuẩn mực hình học, giải quyết tốt bài toán có tam giác xoay hướng."],
        ["3. Tinh thần hợp tác & Thực hành STEM (Tiết 18)", "Thụ động, dựa dẫm vào các bạn trong nhóm.", "Tham gia thảo luận nhóm, ghi chép đầy đủ vào phiếu đo thực tế.", "Chủ động điều phối nhóm, thao tác đo khoảng cách chuẩn xác, báo cáo số liệu sáng tạo."]
    ]
    
    tbl_rb = doc.add_table(rows=len(rb_rows)+1, cols=len(rb_headers))
    tbl_rb.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_rb.autofit = False
    set_table_borders(tbl_rb)
    
    col_rb_w = [Inches(1.8), Inches(1.7), Inches(1.7), Inches(1.8)]
    for i, h in enumerate(rb_headers):
        c = tbl_rb.cell(0, i)
        c.width = col_rb_w[i]
        set_cell_bg(c, "F2F2F2")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    for r_idx, r_data in enumerate(rb_rows):
        for c_idx, val in enumerate(r_data):
            c = tbl_rb.cell(r_idx+1, c_idx)
            c.width = col_rb_w[c_idx]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            if c_idx == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    add_signatures(doc, "TỔ TRƯỞNG CHUYÊN MÔN DUYỆT", "Hoàng Tấn Thiên", "GIÁO VIÊN SOẠN BÀI", "Lê Thị Bình")
    
    doc.save(os.path.join(OUTPUT_DIR, "NCBH_03_Ke_Hoach_Bai_Day_Minh_Hoa_Dinh_Ly_Thales.docx"))
    print("Created DOCX 3: NCBH_03_Ke_Hoach_Bai_Day_Minh_Hoa_Dinh_Ly_Thales.docx")

build_doc_3()

# =============================================================
# DOC 4: PHIẾU QUAN SÁT VÀ ĐÁNH GIÁ TIẾT DẠY (THẦY TRẦN LONG HẢI DỰ GIỜ)
# =============================================================
def build_doc_4():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(doc, ["PHÒNG GIÁO DỤC VÀ ĐÀO TẠO", "TRƯỜNG THCS TRẦN PHÚ - TỔ TOÁN – TIN"], "", "Xuân Đông, ngày 28 tháng 10 năm 2026")
    
    add_p(doc, "PHIẾU QUAN SÁT VÀ ĐÁNH GIÁ TIẾT DẠY MINH HỌA", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "SINH HOẠT CHUYÊN MÔN THEO NGHIÊN CỨU BÀI HỌC (CV 5555/BGDĐT-GDTrH)", bold=True, size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
    
    add_callout(doc,
        "Người dự giờ không ngồi một chỗ ghi chép lời giảng của giáo viên, mà chủ động di chuyển nhẹ nhàng, quan sát nét mặt, thái độ, cử chỉ, sản phẩm học tập và sự tương tác giữa các học sinh trong nhóm; ghi nhận minh chứng thực tế để chia sẻ tại buổi họp thảo luận suy ngẫm Bước 3. TUYỆT ĐỐI KHÔNG CHẤM ĐIỂM, KHÔNG XẾP LOẠI GIÁO VIÊN.",
        title="NGUYÊN TẮC QUAN SÁT THEO CÔNG VĂN 5555/BGDĐT-GDTrH:"
    )
    
    add_p(doc, "• Bài dạy: Bài 15. Định lí Thalès trong tam giác (Chương IV - Môn Toán 8)")
    add_p(doc, "• Tiết thực hiện: Tiết 16 (Tiết 1 của bài: Đoạn thẳng tỉ lệ & Định lí Thalès thuận)")
    add_p(doc, "• Lớp thực hiện: Lớp 8/1 (Sĩ số: 42/43) — Ngày dạy: Tiết 7 ngày 28/10/2026")
    add_p(doc, "• Giáo viên dạy minh họa: Lê Thị Bình")
    add_p(doc, "• Người quan sát (dự giờ): Trần Long Hải (GV môn Toán 8, GVCN 8/3)")
    
    add_p(doc, "I. NỘI DUNG QUAN SÁT THEO TIÊU CHÍ CÔNG VĂN 5555", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Kế hoạch và tài liệu dạy học: Tiến trình 4 hoạt động chặt chẽ, mạch lạc, bám sát CV 5512. Phiếu học tập số 1 và số 2 thiết kế khoa học, có chia sẵn lưới ô vuông giúp học sinh dễ dàng đo đếm và lập tỉ lệ thức.")
    add_p(doc, "2. Tổ chức hoạt động học cho học sinh: Cô Bình chuyển giao nhiệm vụ rõ ràng; bao quát lớp và phát hiện kịp thời khó khăn của học sinh. Phần mềm GeoGebra trên Tivi tương tác thông minh phát huy hiệu quả tối đa.")
    add_p(doc, "3. Hoạt động của học sinh (Trọng tâm quan sát): 100% học sinh chú ý lắng nghe, hào hứng khi xem video mở đầu. Các nhóm 4 học sinh hoạt động sôi nổi, có sự phân công hỗ trợ lẫn nhau. Đa số học sinh lập đúng 3 hệ thức tỉ lệ của định lí Thalès thuận.")
    
    add_p(doc, "II. NHẬT KÝ QUAN SÁT THEO DÒNG THỜI GIAN THỰC TẾ", bold=True, size=13, space_before=4, space_after=2)
    
    headers = ["Thời gian & Hoạt động", "Hành vi, phản ứng của học sinh được quan sát", "Nhận xét sư phạm & Phân tích nguyên nhân"]
    rows = [
        ["Phút 01 – 06\n(HĐ 1: Khởi động cây cầu)", "• Cả lớp chăm chú theo dõi video cây cầu bắc qua sông rộng 300m.\n• Khi cô Bình đặt câu hỏi: \"Làm sao đo khoảng cách CD giữa hai bờ sông?\", em Huy và em Vy giơ tay: \"Em nghĩ phải dùng tỉ lệ đoạn thẳng\".", "Tình huống mở đầu tạo động cơ học tập rất tốt, kích thích tư duy giải quyết vấn đề thực tế."],
        ["Phút 07 – 16\n(HĐ 2.1: Đoạn thẳng tỉ lệ)", "• HĐ1 và HĐ2: Các nhóm đếm ô vuông và đo thước rất nhanh.\n• Luyện tập 1b: Em Tuấn (nhóm 3) viết nhầm $\\frac{25}{10}$, bạn ngồi cạnh nhắc: \"HK là đề-xi-mét, phải đổi ra xăng-ti-mét!\". Tuấn sửa lại ngay $\\frac{25}{100} = \\frac{1}{4}$.\n• Luyện tập 2: Cả lớp đếm lưới ô vuông và so sánh $\\frac{4}{6} = \\frac{2}{3}$ rất chuẩn.", "Rào cản quên đổi đơn vị đo đã xuất hiện đúng dự báo. Hoạt động nhóm đôi phát huy hiệu quả giúp đỡ đồng đẳng kịp thời."],
        ["Phút 17 – 28\n(HĐ 2.2: Định lí Thalès & GeoGebra)", "• Cô Bình mời em Bảo Trâm lên Tivi chạm kéo điểm B' và điểm A trên GeoGebra.\n• Cả lớp ồ lên thích thú khi thấy tam giác méo đi nhưng bảng tỉ số vẫn luôn giữ nguyên dấu bằng.\n• Cả lớp ghi định lí và làm Ví dụ 1 rất nhanh ($x = 2,5$).", "Ứng dụng GeoGebra mang lại hiệu quả trực quan vượt bậc. Học sinh hiểu bản chất định lí bằng thị giác chứ không học vẹt công thức."],
        ["Phút 29 – 40\n(HĐ 3: Luyện tập 3)", "• Câu a (Hình 4.6a): Cả lớp giải đúng $x = 3,25$.\n• Câu b (Hình 4.6b - Tam giác vuông xoay hướng): Nhóm 4 có 2 em lúng túng. Cô Bình gợi ý: \"Hai đoạn thẳng EF và HQ cùng vuông góc với đoạn nào?\", hai em nhận ra ngay cùng vuông góc với PH nên song song, sau đó tính đúng $y = 6,8$.", "Tam giác xoay hướng là thử thách tư duy không gian. Sự gợi mở nhẹ nhàng của cô Bình đã giúp học sinh tự vượt qua khó khăn."],
        ["Phút 41 – 45\n(HĐ 4: STEM hố cát)", "• Khi chiếu hình hố cát nhảy xa của trường, học sinh cười hào hứng: \"Hố cát trường mình kìa!\".\n• Nhóm 1 tính nhẩm ra ngay $CD = 3,75\\text{ m}$. Em Minh đại diện trình bày miệng mạch lạc.", "Bài toán thực tế gần gũi tạo cảm xúc phấn khởi cuối tiết học, học sinh rời lớp trong tâm thế thích thú."]
    ]
    
    col_w = [Inches(1.8), Inches(2.7), Inches(2.5)]
    tbl = doc.add_table(rows=len(rows)+1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl)
    
    for i, h in enumerate(headers):
        c = tbl.cell(0, i)
        c.width = col_w[i]
        set_cell_bg(c, "F2F2F2")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            c = tbl.cell(r_idx+1, c_idx)
            c.width = col_w[c_idx]
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            add_text_with_math(p, val, default_size_pt=10.5, default_font="Times New Roman")
            if c_idx == 0:
                p.runs[0].bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_p(doc, "III. ĐÁNH GIÁ CHUNG VÀ BÀI HỌC KINH NGHIỆM", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Điểm sáng: Cô Bình làm chủ tiến trình sư phạm; GeoGebra trên Tivi tương tác trực quan xuất sắc; học sinh tự tin, tích cực.")
    add_p(doc, "2. Bài học rút ra: Cho học sinh đếm ô vuông và xem hình động trước khi chốt định lí giúp các em nhớ sâu sắc; tiếp tục đưa bài toán thực tế sân trường vào giảng dạy.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    p_sign = add_p(doc, "NGƯỜI QUAN SÁT (DỰ GIỜ)", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.RIGHT)
    p_sign2 = add_p(doc, "(Ký và ghi rõ họ tên)\n\n\n\nTrần Long Hải", italic=True, size=11, align=WD_ALIGN_PARAGRAPH.RIGHT)
    p_sign2.runs[-1].bold = True
    p_sign2.runs[-1].italic = False
    p_sign2.runs[-1].font.size = Pt(12)
    
    doc.save(os.path.join(OUTPUT_DIR, "NCBH_04_Phieu_Quan_Sat_Va_Danh_Gia_Tiet_Day.docx"))
    print("Created DOCX 4: NCBH_04_Phieu_Quan_Sat_Va_Danh_Gia_Tiet_Day.docx")

# =============================================================
# DOC 5: BIÊN BẢN BƯỚC 3 THẢO LUẬN SUY NGẪM
# =============================================================
def build_doc_5():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(doc, ["PHÒNG GIÁO DỤC VÀ ĐÀO TẠO", "TRƯỜNG THCS TRẦN PHÚ - TỔ TOÁN – TIN"], "Số: .../BB-TTIN", "Xuân Đông, ngày 28 tháng 10 năm 2026")
    
    add_p(doc, "BIÊN BẢN HỌP TỔ CHUYÊN MÔN", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "BƯỚC 3: THẢO LUẬN, SUY NGẪM VÀ PHÂN TÍCH TIẾT DẠY MINH HỌA", bold=True, size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "Chuyên đề Nghiên cứu bài học môn Toán 8 - Học kỳ I năm học 2026 - 2027", italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "Tiết dạy minh họa: Tiết 16 (Đoạn thẳng tỉ lệ & Định lí Thalès thuận) — Lớp 8/1 — GV: Lê Thị Bình", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8)
    
    add_p(doc, "I. THỜI GIAN, ĐỊA ĐIỂM, THÀNH PHẦN", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Thời gian: 15 giờ 00 phút đến 16 giờ 45 phút, ngày 28 tháng 10 năm 2026.")
    add_p(doc, "2. Địa điểm: Phòng học thông minh - Trường THCS Trần Phú.")
    add_p(doc, "3. Chủ trì cuộc họp: Thầy Hoàng Tấn Thiên – Tổ trưởng chuyên môn.")
    add_p(doc, "4. Thư ký cuộc họp: Cô Nguyễn Thị Thảo – Giáo viên môn Toán - Tin.")
    add_p(doc, "5. Thành phần tham dự: Toàn thể 09/09 giáo viên tổ Toán – Tin học (Vắng: 0).")
    
    add_p(doc, "II. DIỄN BIẾN VÀ NỘI DUNG CUỘC HỌP", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Quán triệt nguyên tắc điều hành Bước 3 (Thầy Hoàng Tấn Thiên):", bold=True)
    add_p(doc, "Nhấn mạnh tinh thần CV 5555: Tuyệt đối KHÔNG đánh giá, xếp loại giáo viên dạy. Mục tiêu duy nhất là phân tích hoạt động học của học sinh lớp 8/1 để cùng nhau rút kinh nghiệm.")
    
    add_p(doc, "2. Cô Lê Thị Bình (GV dạy minh họa) chia sẻ cảm nhận:", bold=True)
    add_p(doc, "Học sinh lớp 8/1 tương tác rất tích cực. Phần mềm GeoGebra giúp bài học nhẹ nhàng, trực quan. Điểm tiếc nuối là ở phần chuyển giao giữa HĐ 2.1 và 2.2 còn hơi gấp do học sinh đếm ô vuông kéo dài hơn dự kiến 1 phút.")
    
    add_p(doc, "3. Ý kiến chia sẻ minh chứng của giáo viên dự giờ:", bold=True)
    add_p(doc, "• Thầy Trần Long Hải: Nhóm 1 và nhóm 3 làm việc rất tốt. Minh chứng em Tuấn quên đổi đơn vị đo nhưng được bạn ngồi cạnh nhắc nhở tự sửa chữa ngay là biểu hiện rõ nét của học tập cộng tác.")
    add_p(doc, "• Thầy Hoàng Xuân Ánh: Nhóm 4 gặp khó khăn ở Luyện tập 3b vì tam giác bị xoay hướng. Sau khi cô Bình gợi ý quan hệ cùng vuông góc thì các em tự giải được $y = 6,8$. Đề xuất in sẵn hình cho học sinh tô màu hai đường song song.")
    add_p(doc, "• Thầy Dương Quang Tùng: GeoGebra trên Tivi tương tác đạt hiệu quả thị giác tuyệt vời, chứng minh Chuyển đổi số phục vụ chuyên môn thực chất.")
    add_p(doc, "• Thầy Hồ Đăng Danh: Bài toán STEM hố cát sân trường tạo cảm xúc phấn khởi cho học sinh.")
    add_p(doc, "• Thầy Trần Sáng: Phân bổ thời gian 4 hoạt động rất chuẩn xác trong 45 phút.")
    
    add_p(doc, "4. Kết luận của Chủ trì cuộc họp (Thầy Hoàng Tấn Thiên):", bold=True)
    add_p(doc, "Khẳng định tiết dạy minh họa Tiết 16 thành công xuất sắc. Rút ra 3 bài học sư phạm cốt lõi:")
    add_p(doc, "1) Trực quan hóa hình học bằng công nghệ số trước khi chốt công thức toán học.")
    add_p(doc, "2) Luôn rèn cho học sinh thói quen kiểm tra đơn vị đo và lập tỉ số thuận chiều.")
    add_p(doc, "3) Rèn kỹ năng nhận biết tính chất song song gián tiếp ở hình vẽ xoay hướng.")
    add_p(doc, "Giao Thầy Hải và Thầy Ánh áp dụng dạy Tiết 16 tại các lớp 8/2, 8/3, 8/4; nhóm Toán 8 tiếp tục chuẩn bị Tiết 17, 18.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    add_signatures(doc, "THƯ KÝ CUỘC HỌP", "Nguyễn Thị Thảo", "TỔ TRƯỞNG CHUYÊN MÔN", "Hoàng Tấn Thiên")
    
    doc.save(os.path.join(OUTPUT_DIR, "NCBH_05_Bien_Ban_Buoc_3_Thao_Luan_Suy_Ngam.docx"))
    print("Created DOCX 5: NCBH_05_Bien_Ban_Buoc_3_Thao_Luan_Suy_Ngam.docx")

# =============================================================
# DOC 6: BÁO CÁO TỔNG KẾT VÀ KẾ HOẠCH VẬN DỤNG BƯỚC 4
# =============================================================
def build_doc_6():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(doc, ["PHÒNG GIÁO DỤC VÀ ĐÀO TẠO", "TRƯỜNG THCS TRẦN PHÚ - TỔ TOÁN – TIN"], "Số: 11/BC-TTIN", "Xuân Đông, ngày 30 tháng 10 năm 2026")
    
    add_p(doc, "BÁO CÁO TỔNG KẾT CHUYÊN ĐỀ", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "SINH HOẠT CHUYÊN MÔN THEO NGHIÊN CỨU BÀI HỌC — HỌC KỲ I", bold=True, size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "(Áp dụng đối với Tiết 1 - Tiết 16: Định lí Thalès thuận trong tam giác - Môn Toán 8)", italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8)
    
    add_p(doc, "I. ĐÁNH GIÁ TỔNG QUÁT KẾT QUẢ THỰC HIỆN CHUYÊN ĐỀ", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Về phía học sinh: 100% học sinh lớp 8/1 tiếp thu tốt định nghĩa đoạn thẳng tỉ lệ và định lí Thalès thuận. Kỹ năng tính toán độ dài đạt yêu cầu. Năng lực số và tinh thần hợp tác nhóm phát triển rõ rệt.")
    add_p(doc, "2. Về phía giáo viên và tổ chuyên môn: Tổ chức sinh hoạt chuyên môn thực chất theo CV 5555, đoàn kết, học hỏi lẫn nhau, nâng cao năng lực sư phạm cho toàn thể giáo viên.")
    
    add_p(doc, "II. BÀI HỌC KINH NGHIỆM SƯ PHẠM RÚT RA", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "• Trực quan hóa hình học bằng phần mềm GeoGebra trên Tivi tương tác.")
    add_p(doc, "• Tổ chức nhóm đôi giúp đỡ đồng đẳng, tháo gỡ lỗi quên đổi đơn vị đo.")
    add_p(doc, "• Hướng dẫn học sinh nhận biết hai đường thẳng song song trong tam giác xoay hướng.")
    add_p(doc, "• Đưa bài toán thực tế gắn liền với sân trường vào giảng dạy tạo cảm xúc hứng khởi.")
    
    add_p(doc, "III. KẾ HOẠCH VẬN DỤNG VÀ NHÂN RỘNG KẾT QUẢ (BƯỚC 4)", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Dạy đại trà Tiết 16: Thầy Hoàng Xuân Ánh áp dụng tại Lớp 8/2; Thầy Trần Long Hải áp dụng tại Lớp 8/3 và 8/4.")
    add_p(doc, "2. Kế thừa cho Tiết 17, 18: Nhóm Toán 8 phối hợp xây dựng giáo án Tiết 17 (Thalès đảo) và Tiết 18 (Thực hành STEM đo đạc hố cát nhảy xa và bóng nắng cây bàng ngoài trời).")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    add_signatures(doc, "PHÊ DUYỆT CỦA HIỆU TRƯỞNG", "Đinh Văn Đông", "TỔ TRƯỞNG CHUYÊN MÔN", "Hoàng Tấn Thiên")
    
    doc.save(os.path.join(OUTPUT_DIR, "NCBH_06_Bao_Cao_Tong_Ket_Va_Van_Dung_Buoc_4.docx"))
    print("Created DOCX 6: NCBH_06_Bao_Cao_Tong_Ket_Va_Van_Dung_Buoc_4.docx")

# =============================================================
# DOC 7: TÀI LIỆU HƯỚNG DẪN TRỌNG TÂM (NCBH_CHU_Y)
# =============================================================
def build_doc_7():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(doc, ["TRƯỜNG THCS TRẦN PHÚ", "TỔ TOÁN – TIN HỌC"], "TÀI LIỆU LƯU HÀNH NỘI BỘ", "Tháng 10 năm 2026")
    
    add_p(doc, "TÀI LIỆU HƯỚNG DẪN TRỌNG TÂM & NHỮNG ĐIỂM CỐT TỬ CẦN CHÚ Ý", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "DÀNH RIÊNG CHO TỔ TRƯỞNG CHUYÊN MÔN HOÀNG TẤN THIÊN", bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p(doc, "(Bộ hồ sơ Sinh hoạt chuyên môn theo Nghiên cứu bài học - Tiết 1 Định lí Thalès - Toán 8)", italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8)
    
    add_callout(doc,
        "Thầy Hoàng Tấn Thiên thân mến! Đây là tệp tài liệu tổng hợp toàn bộ các lưu ý pháp lý, kỹ năng điều hành sư phạm, cốt tử chuyên môn và quy trình đóng gói hồ sơ chuẩn nhất. Tệp đã được đồng bộ chuẩn xác với Phân phối chương trình Phụ lục 3 môn Toán 8: Bài 15 gồm 3 tiết (Tiết 16, 17, 18), trong đó trọng tâm nghiên cứu bài học CHỈ TẬP TRUNG VÀO TIẾT 1 (Tiết 16: Đoạn thẳng tỉ lệ và Định lí Thalès thuận trong tam giác) do Cô Lê Thị Bình trực tiếp dạy minh họa tại Lớp 8/1 vào Tiết 7 ngày 28/10/2026. Thầy hãy đọc kỹ trước khi ký duyệt hoặc đón đoàn kiểm tra.",
        title="LỜI DẶN DÀNH CHO TỔ TRƯỞNG (ĐỒNG BỘ CHỈ DẠY TIẾT 1 & CÔ BÌNH DẠY MINH HỌA):"
    )
    
    add_p(doc, "I. CĂN CỨ PHÁP LÝ & HỒ SƠ KIỂM TRA CHUYÊN MÔN", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Bốn văn bản pháp quy bắt buộc: CV 5555/BGDĐT-GDTrH; CV 5512/BGDĐT-GDTrH; TT 32/2018/TT-BGDĐT; NĐ 30/2020/NĐ-CP.")
    add_p(doc, "2. Cấu trúc đóng tập hồ sơ (6 tệp chuẩn từ NCBH_01 đến NCBH_06).")
    
    add_p(doc, "II. BẢNG PHÂN CÔNG NHÂN SỰ TỔ TOÁN – TIN CHUẨN XÁC", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "• Thầy Hoàng Tấn Thiên (Tổ trưởng - Môn Toán 6): Chủ trì chỉ đạo, duyệt KHBD, chủ trì họp Bước 1 & Bước 3.")
    add_p(doc, "• Thầy Trần Sáng (Phó Tổ trưởng - Môn Toán 9, Tin 9): Cố vấn phương pháp, dự giờ, phản biện ở Bước 3.")
    add_p(doc, "• Cô Lê Thị Bình (Môn Toán 8): Giáo viên dạy minh họa Tiết 16 tại Lớp 8/1 (13h45 - 14h30 ngày 28/10/2026).")
    add_p(doc, "• Thầy Trần Long Hải (Môn Toán 8, GVCN 8/3): Nhóm cốt cán Toán 8, góp ý KHBD Bước 1, dự giờ ghi phiếu, vận dụng dạy 8/3, 8/4.")
    add_p(doc, "• Thầy Hoàng Xuân Ánh (Toán 8, Tin 6): Nhóm cốt cán Toán 8, góp ý Rubric và STEM, dự giờ, vận dụng dạy lớp 8/2.")
    add_p(doc, "• Thầy Dương Quang Tùng (Tin học 7, 8, 9): Hỗ trợ CNTT, cài đặt tệp GeoGebra trên Tivi tương tác, hỗ trợ trình chiếu.")
    add_p(doc, "• Cô Nguyễn Thị Thảo (Toán - Tin): Thư ký ghi chép biên bản cuộc họp Bước 1 và Bước 3 (thay cô Bình để cô Bình báo cáo).")
    add_p(doc, "• Thầy Hồ Đăng Danh (Toán 9) & Thầy Nguyễn Văn Tính (Toán 6, 7): Thành viên dự giờ và đóng góp ý kiến.")
    
    add_p(doc, "III. NGUYÊN TẮC VÀNG VỀ TÂM LÝ & NGHỆ THUẬT ĐIỀU HÀNH BƯỚC 3", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "1. Nguyên tắc sống còn: TUYỆT ĐỐI KHÔNG ĐÁNH GIÁ, KHÔNG XẾP LOẠI GIÁO VIÊN DẠY!")
    add_p(doc, "2. Kỹ năng \"Bẻ lái sư phạm\" dành cho Thầy Thiên: Nếu giáo viên nhận xét tác phong cô Bình, khéo léo bẻ lái sang: \"Vậy học sinh lúc đó phản ứng ra sao, tiếp thu thế nào?\" để bảo vệ người dạy minh họa.")
    
    add_p(doc, "IV. ĐIỂM CỐT TỬ VỀ CHUYÊN MÔN TOÁN 8 (TIẾT 16: ĐỊNH LÍ THALÈS THUẬN)", bold=True, size=13, space_before=4, space_after=2)
    add_p(doc, "• CẢNH BÁO ĐỎ: Tuyệt đối KHÔNG đưa tỉ số cạnh đáy song song $\\frac{B'C'}{BC}$ vào Tiết 16 này! Tỉ số này thuộc về Hệ quả Thalès (học ở bài sau).")
    add_p(doc, "• Ba lỗi học sinh hay mắc: Quên đổi đơn vị đo; Đảo chiều tỉ số; Lúng túng ở tam giác vuông xoay hướng.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    p_sign = add_p(doc, "TỔ TRƯỞNG CHUYÊN MÔN", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.RIGHT)
    p_sign2 = add_p(doc, "Hoàng Tấn Thiên", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.RIGHT)
    
    doc.save(os.path.join(OUTPUT_DIR, "NCBH_Chu_Y.docx"))
    print("Created DOCX 7: NCBH_Chu_Y.docx")

build_doc_4()
build_doc_5()
build_doc_6()
build_doc_7()
print("ALL 7 DOCX FILES GENERATED SUCCESSFULLY IN 10.11!")
