# -*- coding: utf-8 -*-
"""
Module sinh tài liệu NCBH 1, 2, 3 (CẬP NHẬT CHUẨN XÁC TUẦN 8, 9 - CUỐI THÁNG 10 & ĐẦU THÁNG 11)
Theo đúng Phụ lục 3 Toán 8: Bài 15 gồm 3 tiết (Tiết 16, 17, 18 - Tuần 8, 9).
1. NCBH_01_Ke_Hoach_Sinh_Hoat_Chuyen_Mon.docx
2. NCBH_02_Bien_Ban_Buoc_1_Xay_Dung_Ke_Hoach_Bai_Day.docx
3. NCBH_03_Ke_Hoach_Bai_Day_Minh_Hoa_Dinh_Ly_Thales.docx
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

OUTPUT_DIR = os.path.abspath("TROLYTHIEN/NCBH_DINH_LY_THALES_TOAN_8")
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
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    r_txt.font.color.rgb = RGBColor(30, 41, 59)
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
    rl2.font.size = Pt(12.5)
    
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
    rr2.font.size = Pt(12.5)

# ==============================================================================
# 1. FILE 1: NCBH_01_Ke_Hoach_Sinh_Hoat_Chuyen_Mon.docx
# ==============================================================================
def create_doc_1():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(
        doc,
        ["PHÒNG GIÁO DỤC VÀ ĐÀO TẠO", "TRƯỜNG THCS TRẦN PHÚ", "TỔ TOÁN – TIN"],
        "Số: 08/KH-TTH",
        "Xuân Đông, ngày 20 tháng 10 năm 2026"
    )
    
    add_p(doc, "KẾ HOẠCH", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "TỔ CHỨC SINH HOẠT CHUYÊN MÔN THEO NGHIÊN CỨU BÀI HỌC", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "HỌC KỲ I - NĂM HỌC 2026 - 2027", bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Chuyên đề: Đổi mới phương pháp dạy học Hình học 8 thông qua chủ đề \"Bài 15. Định lí Thalès trong tam giác\" (3 tiết - Phụ lục 3) gắn với giáo dục STEM và Chuyển đổi số", italic=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    
    add_callout(
        doc,
        "CĂN CỨ THEO PHÂN PHỐI CHƯƠNG TRÌNH (PHỤ LỤC 3 MÔN TOÁN 8): Bài 15. Định lí Thalès trong tam giác (KHBD STEM) được bố trí 3 tiết (Tiết 16, 17, 18), thực hiện trong Tuần 8 và Tuần 9 (rơi vào thời điểm Cuối tháng 10 và Đầu tháng 11 năm 2026). Kế hoạch chuyên đề được xây dựng chuẩn xác khớp 100% với tiến độ kế hoạch giáo dục đã được Ban Giám hiệu phê duyệt.",
        title="ĐỒNG BỘ TIẾN ĐỘ PPCT PHỤ LỤC 3:",
        border_color="2563EB",
        bg_color="EFF6FF"
    )
    
    add_p(doc, "I. CĂN CỨ XÂY DỰNG KẾ HOẠCH", bold=True, size=13)
    add_p(doc, "- Căn cứ Thông tư số 32/2018/TT-BGDĐT ngày 26/12/2018 của Bộ Giáo dục và Đào tạo ban hành Chương trình Giáo dục phổ thông 2018;")
    add_p(doc, "- Căn cứ Công văn số 5555/BGDĐT-GDTrH ngày 08/10/2014 của Bộ Giáo dục và Đào tạo về việc hướng dẫn sinh hoạt chuyên môn về đổi mới phương pháp dạy học và kiểm tra, đánh giá;")
    add_p(doc, "- Căn cứ Công văn số 5512/BGDĐT-GDTrH ngày 18/12/2020 của Bộ Giáo dục và Đào tạo về việc xây dựng và tổ chức thực hiện kế hoạch giáo dục của nhà trường;")
    add_p(doc, "- Căn cứ Công văn số 3456/BGDĐT-GDTrH về Khung Năng lực số và Quyết định số 2422/QĐ-BGDĐT về Khung Năng lực Trí tuệ nhân tạo (AI);")
    add_p(doc, "- Căn cứ Kế hoạch giáo dục nhà trường năm học 2026 - 2027 của Trường THCS Trần Phú và Kế hoạch giáo dục môn Toán khối 8 (Phụ lục 3) của Tổ Toán – Tin đã được Hiệu trưởng phê duyệt.")
    
    add_p(doc, "II. MỤC ĐÍCH, YÊU CẦU", bold=True, size=13)
    add_p(doc, "1. Mục đích:", bold=True)
    add_p(doc, "- Chuyển biến căn bản nhận thức của giáo viên về sinh hoạt chuyên môn: chuyển từ đánh giá, xếp loại, soi xét giáo viên dạy sang tập trung quan sát, phân tích hoạt động học của học sinh theo tinh thần Công văn 5555/BGDĐT-GDTrH.")
    add_p(doc, "- Giúp nhóm giáo viên khối 8 (thầy Trần Long Hải, cô Lê Thị Bình) và toàn thể giáo viên trong tổ nâng cao năng lực sư phạm khi dạy chủ đề Hình học trực quan Chương IV: cách tổ chức chuỗi 3 tiết dạy học khám phá định lý, ứng dụng mô phỏng GeoGebra và thực hành giáo dục STEM.")
    add_p(doc, "- Tháo gỡ khó khăn kinh điển của học sinh lớp 8: nhầm lẫn tỉ số đoạn thẳng, viết sai thứ tự cặp đoạn thẳng tương ứng tỉ lệ hoặc nhầm định lí thuận với hệ quả.")
    add_p(doc, "- Xây dựng tinh thần đoàn kết, tương trợ chuyên môn giữa các đồng nghiệp trong tổ.")
    add_p(doc, "2. Yêu cầu:", bold=True)
    add_p(doc, "- 100% giáo viên trong tổ tham gia nghiêm túc, thực chất trong suốt quy trình 4 bước.")
    add_p(doc, "- Tuyệt đối không dạy trước bài, không luyện tập gà bài cho học sinh trước tiết dạy minh họa.")
    add_p(doc, "- Trong giờ dự giờ, giáo viên quan sát phải ghi chép minh chứng cụ thể về hành vi, biểu cảm, khó khăn của học sinh trên phiếu quan sát chuyên dụng.")
    
    add_p(doc, "III. NỘI DUNG VÀ TIẾN TRÌNH THỰC HIỆN THEO PPCT", bold=True, size=13)
    add_p(doc, "1. Nội dung chuyên đề nghiên cứu bài học:", bold=True)
    add_p(doc, "- Môn học: Toán - Khối lớp: 8 (Bộ sách Kết nối tri thức với cuộc sống).")
    add_p(doc, "- Chủ đề nghiên cứu: Bài 15. Định lí Thalès trong tam giác (Chương IV - KHBD STEM).")
    add_p(doc, "- Thời lượng thực hiện: 3 tiết (Tiết 16, 17, 18 theo Phân phối chương trình Phụ lục 3):")
    add_p(doc, "  + Tiết 1 (Tiết 16 - Tuần 8, Cuối tháng 10): Đoạn thẳng tỉ lệ & Định lí Thalès thuận trong tam giác (Tiết dạy minh họa NCBH).")
    add_p(doc, "  + Tiết 2 (Tiết 17 - Tuần 8/9): Định lí Thalès đảo trong tam giác.")
    add_p(doc, "  + Tiết 3 (Tiết 18 - Tuần 9, Đầu tháng 11): Luyện tập & Hoạt động thực hành STEM đo bóng nắng, khoảng cách thực tế.")
    add_p(doc, "- Địa điểm thực hiện: Lớp minh họa 8A1 (38 học sinh); Lớp vận dụng đối chứng 8A2, 8A3, 8A4.")
    
    add_p(doc, "2. Kế hoạch thời gian thực hiện theo 4 bước chuẩn (Khớp Tuần 8, 9 - Cuối tháng 10 & Đầu tháng 11):", bold=True)
    
    tbl_b = doc.add_table(rows=5, cols=5)
    tbl_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_b)
    headers = ["Bước", "Thời gian", "Nội dung công việc", "Địa điểm", "Người phụ trách"]
    widths = [Inches(0.8), Inches(1.3), Inches(2.5), Inches(1.1), Inches(1.3)]
    for i, h in enumerate(headers):
        cell = tbl_b.cell(0, i)
        cell.width = widths[i]
        set_cell_bg(cell, "F1F5F9")
        set_cell_margins(cell, 80, 80, 60, 60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    steps_data = [
        ("Bước 1", "22/10/2026 (Tuần 7)\n14h00", "Họp tổ chuyên môn: Thảo luận mục tiêu, thiết kế chuỗi 3 tiết Bài 15 (tiết 16, 17, 18), dự đoán rào cản nhận thức của HS; duyệt KHBD minh họa Tiết 16.", "Phòng SHCM Tổ Toán - Tin", "Tổ trưởng Hoàng Tấn Thiên\nThầy Hải, Cô Bình"),
        ("Bước 2", "28/10/2026 (Tuần 8)\nTiết 2, Cuối tháng 10", "Tổ chức dạy học minh họa Tiết 16 tại lớp 8A1; toàn thể GV trong tổ dự giờ, ghi hình, chụp ảnh, quan sát việc học của học sinh.", "Phòng học thông minh 8A1", "Thầy Trần Long Hải (Dạy)\nToàn thể GV tổ Toán"),
        ("Bước 3", "28/10/2026 (Tuần 8)\nTiết 4, Cuối tháng 10", "Họp tổ suy ngẫm, phân tích bài học: Người dạy chia sẻ cảm xúc, người dự giờ nêu minh chứng học tập của HS, thống nhất giải pháp điều chỉnh sư phạm.", "Phòng Hội đồng sư phạm", "Tổ trưởng Hoàng Tấn Thiên (Chủ trì)\nToàn thể GV tổ"),
        ("Bước 4", "02/11 - 07/11/2026\n(Tuần 9 - Đầu tháng 11)", "Vận dụng KHBD đã điều chỉnh dạy tại 8A2, 8A3 (Cô Bình) và 8A4 (Thầy Hải); thực hiện dạy tiếp Tiết 17, 18 hoàn thành 3 tiết; tổng kết và báo cáo BGH.", "Các lớp khối 8", "Cô Lê Thị Bình (8A2, 8A3)\nThầy Trần Long Hải (8A4)")
    ]
    
    for row_idx, data in enumerate(steps_data, start=1):
        for col_idx, text in enumerate(data):
            cell = tbl_b.cell(row_idx, col_idx)
            cell.width = widths[col_idx]
            set_cell_margins(cell, 60, 60, 60, 60)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if col_idx in [0, 1, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            if col_idx == 0:
                r.bold = True
                
    add_p(doc, "", space_after=4)
    add_p(doc, "IV. PHÂN CÔNG NHIỆM VỤ CỤ THỂ", bold=True, size=13)
    
    tbl_nv = doc.add_table(rows=8, cols=4)
    tbl_nv.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_nv)
    nv_headers = ["STT", "Họ và tên", "Nhiệm vụ được phân công", "Ghi chú"]
    nv_widths = [Inches(0.6), Inches(1.8), Inches(3.6), Inches(1.0)]
    for i, h in enumerate(nv_headers):
        cell = tbl_nv.cell(0, i)
        cell.width = nv_widths[i]
        set_cell_bg(cell, "F1F5F9")
        set_cell_margins(cell, 80, 80, 60, 60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    nv_data = [
        ("1", "Thầy Hoàng Tấn Thiên", "Tổ trưởng chuyên môn: Chỉ đạo chung; chủ trì các phiên họp Bước 1 và Bước 3; phê duyệt Kế hoạch bài dạy 3 tiết; tổng hợp báo cáo chuyên đề nộp BGH.", "Chủ trì"),
        ("2", "Thầy Trần Long Hải", "Giáo viên giảng dạy Toán 8: Trưởng nhóm xây dựng KHBD minh họa; trực tiếp thực hiện tiết dạy minh họa Tiết 16 tại lớp 8A1; thực hiện dạy Tiết 17, 18 tại lớp 8A4.", "Dạy minh họa"),
        ("3", "Cô Lê Thị Bình", "Giáo viên giảng dạy Toán 8: Đồng biên soạn KHBD; phụ trách thiết kế Phiếu học tập số 1, 2, 3 và mô hình bóng nắng STEM; thực hiện dạy vận dụng đối chứng trọn vẹn 3 tiết tại 8A2, 8A3.", "Đồng biên soạn & Vận dụng"),
        ("4", "Cô Nguyễn Thị Thảo", "Giáo viên Toán: Thư ký chuyên đề, ghi chép biên bản sinh hoạt chuyên môn các bước 1, 3 và tổng hợp phiếu quan sát của các thành viên.", "Thư ký"),
        ("5", "Thầy Dương Quang Tùng", "Giáo viên Tin học: Phụ trách kỹ thuật trình chiếu, hỗ trợ phần mềm mô phỏng GeoGebra; ghi hình video và chụp ảnh các góc học tập của học sinh làm minh chứng.", "Kỹ thuật & Tư liệu"),
        ("6", "Thầy Hồ Đăng Danh", "Giáo viên Toán: Dự giờ, quan sát chuyên sâu hoạt động học của học sinh Dãy 1 (Nhóm 1 và Nhóm 2); ghi phiếu quan sát theo tiêu chí CV 5555.", "Quan sát viên"),
        ("7", "Thầy Trần Sáng\nThầy Hoàng Xuân Ánh", "Giáo viên Toán: Dự giờ, quan sát hoạt động học của học sinh Dãy 2 và Dãy 3 (Nhóm 3 và Nhóm 4); ghi nhận các khó khăn, vướng mắc của học sinh.", "Quan sát viên")
    ]
    
    for row_idx, data in enumerate(nv_data, start=1):
        for col_idx, text in enumerate(data):
            cell = tbl_nv.cell(row_idx, col_idx)
            cell.width = nv_widths[col_idx]
            set_cell_margins(cell, 60, 60, 60, 60)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if col_idx in [0, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            if col_idx == 1:
                r.bold = True
                
    add_p(doc, "", space_after=4)
    add_p(doc, "V. ĐIỀU KIỆN CƠ SỞ VẬT CHẤT VÀ THIẾT BỊ DẠY HỌC", bold=True, size=13)
    add_p(doc, "- Phòng học: Phòng học thông minh lớp 8A1 trang bị màn hình tương tác, hệ thống âm thanh, camera ghi hình tiết dạy chuyên đề.")
    add_p(doc, "- Thiết bị & học liệu: 08 bộ bảng phụ nhóm A3, bút lông dạ nhiều màu, thước dây cuộn 10m, thước thẳng có vạch chia, mô hình cọc đo bóng nắng STEM ngoài trời.")
    add_p(doc, "- Phần mềm hỗ trợ: Tệp mô phỏng hình học động GeoGebra trực quan hóa định lí Thalès; bài giảng PowerPoint chuẩn hóa.")
    
    add_p(doc, "VI. TỔ CHỨC THỰC HIỆN", bold=True, size=13)
    add_p(doc, "- Nhóm Toán 8 (Thầy Hải, Cô Bình) hoàn thiện giáo án bản thảo nộp Tổ trưởng chuyên môn trước ngày 25/10/2026.")
    add_p(doc, "- Tổ trưởng chuyên môn kiểm tra, ký duyệt hồ sơ và báo cáo Ban Giám hiệu theo dõi chỉ đạo.")
    add_p(doc, "- Các thành viên tổ Toán – Tin sắp xếp công việc giảng dạy dự giờ nghiêm túc, đúng giờ, đúng vị trí phân công.")
    
    add_p(doc, "", space_after=10)
    add_signatures(
        doc,
        "HIỆU TRƯỞNG PHÊ DUYỆT",
        "Nguyễn Văn An",
        "TỔ TRƯỞNG CHUYÊN MÔN",
        "Hoàng Tấn Thiên",
        left_sub="(Ký, ghi rõ họ tên và đóng dấu)",
        right_sub="(Ký và ghi rõ họ tên)"
    )
    
    out_file = os.path.join(OUTPUT_DIR, "NCBH_01_Ke_Hoach_Sinh_Hoat_Chuyen_Mon.docx")
    doc.save(out_file)
    print("XUẤT THÀNH CÔNG:", out_file)

# ==============================================================================
# 2. FILE 2: NCBH_02_Bien_Ban_Buoc_1_Xay_Dung_Ke_Hoach_Bai_Day.docx
# ==============================================================================
def create_doc_2():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(
        doc,
        ["TRƯỜNG THCS TRẦN PHÚ", "TỔ TOÁN – TIN"],
        "Số: 02/BB-NCBH",
        "Xuân Đông, ngày 22 tháng 10 năm 2026"
    )
    
    add_p(doc, "BIÊN BẢN HỌP TỔ CHUYÊN MÔN", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "BƯỚC 1: XÂY DỰNG KẾ HOẠCH BÀI DẠY MINH HỌA", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Chuyên đề Nghiên cứu bài học môn Toán 8 - Tuần 8, 9 (Cuối tháng 10 và Đầu tháng 11/2026)", italic=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    
    add_p(doc, "I. THỜI GIAN, ĐỊA ĐIỂM VÀ THÀNH PHẦN", bold=True, size=13)
    add_p(doc, "1. Thời gian: Vào hồi 14 giờ 00 phút, ngày 22 tháng 10 năm 2026 (Tuần 7).")
    add_p(doc, "2. Địa điểm: Phòng Sinh hoạt chuyên môn Tổ Toán – Tin, Trường THCS Trần Phú.")
    add_p(doc, "3. Thành phần tham dự:")
    add_p(doc, "- Chủ trì: Thầy Hoàng Tấn Thiên – Tổ trưởng chuyên môn.")
    add_p(doc, "- Thư ký: Cô Nguyễn Thị Thảo – Giáo viên Toán.")
    add_p(doc, "- Thành viên dự họp: 07/07 giáo viên trong tổ, gồm:")
    add_p(doc, "  + Thầy Trần Long Hải (GV Toán 8 - Phụ trách dạy minh họa);")
    add_p(doc, "  + Cô Lê Thị Bình (GV Toán 8 - Phụ trách đồng biên soạn & thiết kế học liệu);")
    add_p(doc, "  + Thầy Hồ Đăng Danh (GV Toán);")
    add_p(doc, "  + Thầy Trần Sáng (GV Toán);")
    add_p(doc, "  + Thầy Hoàng Xuân Ánh (GV Toán);")
    add_p(doc, "  + Thầy Dương Quang Tùng (GV Tin học).")
    
    add_p(doc, "II. NỘI DUNG CUỘC HỌP", bold=True, size=13)
    add_p(doc, "1. Quán triệt tinh thần chỉ đạo của Tổ trưởng (Thầy Hoàng Tấn Thiên):", bold=True)
    add_p(doc, "Thầy Hoàng Tấn Thiên phát biểu khai mạc: Căn cứ theo Phân phối chương trình Phụ lục 3 môn Toán 8, chủ đề 'Bài 15. Định lí Thalès trong tam giác' được phân bổ 3 tiết (Tiết 16, 17, 18), thực hiện trong Tuần 8 và Tuần 9 (rơi vào thời điểm Cuối tháng 10 và Đầu tháng 11 năm 2026). Đây là chủ đề có đăng ký giáo án STEM. Tổ chuyên môn thống nhất chọn Bài 15 làm chuyên đề Nghiên cứu bài học học kỳ I. Nhóm giáo viên Toán 8 cần xây dựng bài bản kế hoạch dạy học cả 3 tiết, trong đó chọn Tiết 16 (Tiết 1 của bài - Đoạn thẳng tỉ lệ & Định lí Thalès thuận) để thực hiện dạy minh họa vào thứ Tư ngày 28/10/2026 (Tuần 8 - Cuối tháng 10).")
    
    add_p(doc, "2. Báo cáo đề xuất cấu trúc chuỗi 3 tiết của nhóm giáo viên Toán 8:", bold=True)
    add_p(doc, "- Thầy Trần Long Hải trình bày dự thảo Kế hoạch bài dạy 3 tiết:")
    add_p(doc, "  + Tiết 1 (Tiết 16 - Tuần 8, Cuối tháng 10): Đoạn thẳng tỉ lệ và Định lí Thalès thuận trong tam giác. Trọng tâm là dẫn dắt học sinh khám phá định lí qua lưới ô vuông và mô phỏng GeoGebra.")
    add_p(doc, "  + Tiết 2 (Tiết 17 - Tuần 8/9): Định lí Thalès đảo trong tam giác và cách chứng minh song song.")
    add_p(doc, "  + Tiết 3 (Tiết 18 - Tuần 9, Đầu tháng 11): Luyện tập & Hoạt động thực hành STEM đo chiều cao cây bàng, cột cờ ngoài sân trường.")
    add_p(doc, "- Cô Lê Thị Bình bổ sung phân tích khó khăn nhận thức của học sinh khối 8:")
    add_p(doc, "  + Học sinh lớp 8 rất dễ nhầm tỉ số đoạn thẳng khi các đoạn thẳng không cùng đơn vị đo (ví dụ AB = 3 cm, CD = 5 dm thì viết luôn tỉ số 3/5).")
    add_p(doc, "  + Khi đường thẳng song song cắt hai cạnh tam giác, học sinh thường mắc sai lầm kinh điển: viết tỉ lệ chéo hoặc nhầm đoạn trên đoạn dưới (viết AB'/B'B = AC'/AC thay vì AC'/C'C).")
    add_p(doc, "  + Học sinh hay bị lệ thuộc vào hình tam giác có đáy nằm ngang. Nếu hình vẽ bị quay nghiêng, học sinh lúng túng không nhận ra các đoạn thẳng tương ứng tỉ lệ.")
    
    add_p(doc, "3. Thảo luận, đóng góp ý kiến của các giáo viên trong tổ:", bold=True)
    add_p(doc, "- Ý kiến của Thầy Hồ Đăng Danh:")
    add_p(doc, "  + Nhất trí cao với việc chia 3 tiết hợp lý. Ở Tiết 16 dạy minh họa, thay vì cho học sinh đo bằng thước milimét dễ bị sai số, bắt buộc dùng lưới ô vuông để tỉ số 2/4 = 1/2 và 3/6 = 1/2 hiện ra tuyệt đối chính xác.")
    add_p(doc, "- Ý kiến của Thầy Trần Sáng:")
    add_p(doc, "  + Ở phần phát biểu định lí Thalès, cần dùng 3 màu phấn (hoặc 3 màu mực bảng nhóm) để phân biệt: màu đỏ cho đoạn trên, màu vàng cho đoạn dưới, màu trắng cho toàn bộ cạnh. Nhờ đó học sinh khắc sâu quy tắc 'tương ứng'.")
    add_p(doc, "- Ý kiến của Thầy Hoàng Xuân Ánh:")
    add_p(doc, "  + Sang Tiết 18 (Tuần 9 - Đầu tháng 11), hoạt động STEM ngoài sân trường cần chuẩn bị sẵn thước dây và giác kế. Cần chia lớp thành 4 nhóm nhỏ để mỗi nhóm thực hành đo bóng nắng một vật thể khác nhau (cột cờ, cây bàng, khung thành bóng đá).")
    add_p(doc, "- Ý kiến của Thầy Dương Quang Tùng:")
    add_p(doc, "  + Tệp GeoGebra đã sẵn sàng và được cài đặt trên Tivi phòng học thông minh 8A1, đáp ứng chuẩn Năng lực số 5.3.TC2a.")
    
    add_p(doc, "4. Kết luận và phân công của Tổ trưởng Hoàng Tấn Thiên:", bold=True)
    add_p(doc, "- Tổ chuyên môn thống nhất 100% cấu trúc 3 tiết và kế hoạch dạy minh họa:")
    add_p(doc, "  + Tiết dạy minh họa: Tiết 16 (Tiết 1) dạy vào Tiết 2, sáng thứ Tư ngày 28/10/2026 (Tuần 8 - Cuối tháng 10) tại lớp 8A1 do Thầy Trần Long Hải thực hiện.")
    add_p(doc, "  + Họp thảo luận Bước 3 ngay sau tiết dạy (Tiết 4, ngày 28/10/2026).")
    add_p(doc, "  + Tuần 9 (Đầu tháng 11 - Từ 02/11 đến 07/11/2026): Cô Lê Thị Bình và Thầy Hải thực hiện dạy vận dụng tại các lớp 8A2, 8A3, 8A4 và hoàn thành tiếp Tiết 17, Tiết 18.")
    
    add_p(doc, "III. KẾT THÚC CUỘC HỌP", bold=True, size=13)
    add_p(doc, "Biên bản được thông qua trước toàn thể cuộc họp, 100% thành viên nhất trí biểu quyết và ký tên xác nhận.")
    add_p(doc, "Cuộc họp kết thúc vào lúc 16 giờ 30 phút cùng ngày./.")
    
    add_p(doc, "", space_after=10)
    add_signatures(
        doc,
        "THƯ KÝ BIÊN BẢN",
        "Nguyễn Thị Thảo",
        "TỔ TRƯỞNG CHUYÊN MÔN",
        "Hoàng Tấn Thiên"
    )
    
    out_file = os.path.join(OUTPUT_DIR, "NCBH_02_Bien_Ban_Buoc_1_Xay_Dung_Ke_Hoach_Bai_Day.docx")
    doc.save(out_file)
    print("XUẤT THÀNH CÔNG:", out_file)

# ==============================================================================
# 3. FILE 3: NCBH_03_Ke_Hoach_Bai_Day_Minh_Hoa_Dinh_Ly_Thales.docx
# ==============================================================================
def create_doc_3():
    doc = docx.Document()
    setup_page(doc)
    
    add_p(doc, "BÀI 15: ĐỊNH LÍ THALÈS TRONG TAM GIÁC (KHBD STEM)", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Thời lượng thực hiện: 03 tiết (Tiết 16, 17, 18 - Tuần 8, 9 theo PPCT Phụ lục 3)", bold=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "(Tiết 16 dạy minh họa NCBH vào Tuần 8 - Cuối tháng 10; Tiết 17, 18 vận dụng vào Tuần 9 - Đầu tháng 11)", italic=True, size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    
    add_callout(
        doc,
        "HỒ SƠ KẾ HOẠCH BÀI DẠY CHUYÊN ĐỀ NGHIÊN CỨU BÀI HỌC CẤP TRƯỜNG: Thiết kế trọn vẹn chuỗi 3 tiết theo Phụ lục 3 môn Toán 8. Giáo viên dạy minh họa Tiết 16: Thầy Trần Long Hải; Giáo viên đồng thiết kế & dạy đối chứng Tiết 16, 17, 18: Cô Lê Thị Bình; Phê duyệt chuyên môn: Thầy Hoàng Tấn Thiên (Tổ trưởng Toán – Tin). Tích hợp Giáo dục STEM & Khung Năng lực số 5.3.TC2a.",
        title="THÔNG TIN CHUYÊN ĐỀ NCBH (3 TIẾT - TUẦN 8 & 9):",
        border_color="2563EB",
        bg_color="EFF6FF"
    )
    
    add_p(doc, "I. MỤC TIÊU DẠY HỌC CHỦ ĐỀ (3 TIẾT)", bold=True, size=13)
    add_p(doc, "1. Về kiến thức:", bold=True)
    add_p(doc, "- Nắm vững định nghĩa tỉ số của hai đoạn thẳng và các đoạn thẳng tỉ lệ;")
    add_p(doc, "- Hiểu, phát biểu chuẩn xác định lí Thalès thuận trong tam giác và viết được giả thiết, kết luận, 3 hệ thức tỉ số tương ứng (Tiết 16);")
    add_p(doc, "- Hiểu và phát biểu được định lí Thalès đảo trong tam giác, biết vận dụng để nhận biết và chứng minh hai đường thẳng song song (Tiết 17);")
    add_p(doc, "- Vận dụng định lí Thalès và tính chất hình học để giải quyết bài toán thực tế đo bóng nắng, xác định chiều cao vật thể ngoài trời theo phương pháp STEM (Tiết 18).")
    
    add_p(doc, "2. Về năng lực:", bold=True)
    add_p(doc, "a) Năng lực chung:")
    add_p(doc, "- Tự chủ và tự học: Tự giác thực hiện các nhiệm vụ khám phá trên phiếu học tập, chủ động nghiên cứu ví dụ trong SGK.")
    add_p(doc, "- Giao tiếp và hợp tác: Tương tác tích cực, phân vai hiệu quả trong nhóm 4 học sinh; biết lắng nghe, phản biện và thống nhất kết quả.")
    add_p(doc, "b) Năng lực đặc thù môn Toán:")
    add_p(doc, "- Năng lực tư duy và lập luận toán học: So sánh các tỉ số đoạn thẳng trên lưới ô vuông; phát hiện quy luật tỉ lệ bất biến khi đường thẳng song song di chuyển.")
    add_p(doc, "- Năng lực mô hình hóa toán học: Chuyển đổi bài toán thực tế đo chiều cao kim tự tháp, đo bóng nắng cây bàng sân trường thành mô hình tam giác có các đường thẳng song song.")
    add_p(doc, "- Năng lực giải quyết vấn đề toán học: Lập phương trình tỉ số để tìm độ dài x, y của các cạnh trong tam giác.")
    add_p(doc, "c) Năng lực số (NLS) & AI:")
    add_p(doc, "- ***(Tích hợp NLS 5.3.TC2a: Học sinh sử dụng và quan sát phần mềm hình học động GeoGebra để trực quan hóa việc thay đổi vị trí điểm, kiểm chứng các cặp đoạn thẳng tỉ lệ không đổi khi đường thẳng song song với cạnh đáy tam giác)***.")
    add_p(doc, "d) Năng lực STEM:")
    add_p(doc, "- Chế tạo mô hình đo đơn giản và thực hành đo gián tiếp chiều cao vật thể thông qua bóng nắng mặt trời.")
    
    add_p(doc, "3. Về phẩm chất:", bold=True)
    add_p(doc, "- Chăm chỉ: Cẩn thận, tỉ mỉ trong đo đạc và tính toán tỉ số.")
    add_p(doc, "- Trách nhiệm: Nghiêm túc hoàn thành nhiệm vụ được nhóm phân công, có tinh thần tương trợ bạn học còn thao tác chậm.")
    add_p(doc, "- Trung thực: Tôn trọng số liệu đo đạc thực tế ngoài trời, không gán ghép số liệu giả tạo.")
    
    add_p(doc, "II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU", bold=True, size=13)
    add_p(doc, "1. Giáo viên:")
    add_p(doc, "- Màn hình tương tác / Tivi thông minh kết nối máy tính;")
    add_p(doc, "- Phần mềm GeoGebra với tệp mô phỏng định lí Thalès động;")
    add_p(doc, "- 08 bộ Phiếu học tập số 1, số 2, số 3 in sẵn khổ A3, bút lông dạ nhiều màu;")
    add_p(doc, "- Thước dây cuộn 10m, mô hình cọc đo bóng nắng 1.4m và giác kế mini phục vụ tiết 18 STEM ngoài trời.")
    add_p(doc, "2. Học sinh:")
    add_p(doc, "- Sách giáo khoa Toán 8 Tập 1 (Kết nối tri thức với cuộc sống);")
    add_p(doc, "- Thước thẳng chia milimét, êke, compa, bút dạ, bảng phụ nhóm.")
    
    add_p(doc, "III. PHÂN BỔ NỘI DUNG 3 TIẾT THEO PHỤ LỤC 3", bold=True, size=13)
    add_p(doc, "- Tiết 1 (Tiết 16 - Tuần 8, Cuối tháng 10): Đoạn thẳng tỉ lệ & Định lí Thalès thuận trong tam giác (Tiết dạy minh họa Nghiên cứu bài học tại Lớp 8A1).")
    add_p(doc, "- Tiết 2 (Tiết 17 - Tuần 8/9): Định lí Thalès đảo trong tam giác.")
    add_p(doc, "- Tiết 3 (Tiết 18 - Tuần 9, Đầu tháng 11): Luyện tập & Hoạt động thực hành STEM đo chiều cao thực tế.")
    
    # Helper tạo bảng 2 cột cho hoạt động
    def add_activity_table(doc, act_title, gv_steps, hs_content):
        add_p(doc, act_title, bold=True, size=12.5, space_before=4, space_after=3)
        tbl = doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        set_table_borders(tbl)
        
        c_l = tbl.cell(0, 0)
        c_r = tbl.cell(0, 1)
        c_l.width = Inches(3.6)
        c_r.width = Inches(3.1)
        set_cell_margins(c_l, top=60, bottom=60, left=60, right=60)
        set_cell_margins(c_r, top=60, bottom=60, left=60, right=60)
        
        # Tiêu đề cột
        p_tl = c_l.paragraphs[0]
        p_tl.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_bg(c_l, "F8FAFC")
        r_tl = p_tl.add_run("HOẠT ĐỘNG CỦA GV VÀ HS")
        r_tl.bold = True
        r_tl.font.name = "Times New Roman"
        r_tl.font.size = Pt(11)
        
        p_tr = c_r.paragraphs[0]
        p_tr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_bg(c_r, "F8FAFC")
        r_tr = p_tr.add_run("SẢN PHẨM DỰ KIẾN")
        r_tr.bold = True
        r_tr.font.name = "Times New Roman"
        r_tr.font.size = Pt(11)
        
        row_content = tbl.add_row()
        cl_c = row_content.cells[0]
        cr_c = row_content.cells[1]
        cl_c.width = Inches(3.6)
        cr_c.width = Inches(3.1)
        set_cell_margins(cl_c, top=60, bottom=60, left=60, right=60)
        set_cell_margins(cr_c, top=60, bottom=60, left=60, right=60)
        
        for line in gv_steps:
            p_line = cl_c.add_paragraph()
            p_line.paragraph_format.line_spacing = 1.15
            p_line.paragraph_format.space_after = Pt(2)
            if "Tích hợp NLS" in line or "Tích hợp AI" in line:
                r = p_line.add_run(line)
                r.bold = True
                r.italic = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(180, 83, 9)
            elif line.startswith("+ Bước") or line.startswith("- **GV:**") or line.startswith("- **HS:**"):
                parts = line.split(":", 1)
                r_hd = p_line.add_run(parts[0] + ":")
                r_hd.bold = True
                r_hd.font.name = "Times New Roman"
                r_hd.font.size = Pt(11)
                if len(parts) > 1:
                    r_tx = p_line.add_run(parts[1])
                    r_tx.font.name = "Times New Roman"
                    r_tx.font.size = Pt(11)
            else:
                r = p_line.add_run(line)
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                
        for line in hs_content:
            p_line = cr_c.add_paragraph()
            p_line.paragraph_format.line_spacing = 1.15
            p_line.paragraph_format.space_after = Pt(2)
            if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("*") or line.startswith("Ví dụ") or line.startswith("Luyện tập") or line.startswith("Bài"):
                r = p_line.add_run(line)
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
            else:
                r = p_line.add_run(line)
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
                
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # CHI TIẾT TIẾT 16: TIẾT DẠY MINH HỌA NCBH
    add_p(doc, "TIẾN TRÌNH DẠY HỌC TIẾT 16 (TIẾT 1 - DẠY MINH HỌA NCBH - TUẦN 8, CUỐI THÁNG 10)", bold=True, size=13.5, space_before=6)
    
    # 1. Khởi động
    add_activity_table(
        doc,
        "A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (6 phút)",
        [
            "+ Bước 1: Chuyển giao nhiệm vụ:",
            "- **GV:** Chiếu hình ảnh Kim tự tháp Kheops Ai Cập và kể mẩu chuyện lịch sử: Cách đây hơn 2600 năm, nhà bác học Hy Lạp Thalès đã đo chính xác chiều cao kỳ vĩ của kim tự tháp mà không cần trèo lên đỉnh, chỉ bằng một chiếc cọc nhỏ cắm trên cát và bóng nắng mặt trời.",
            "- **GV:** Đặt câu hỏi kích thích tư duy: 'Làm thế nào chỉ với bóng nắng và một chiếc cọc, Thalès có thể tính ra chiều cao kim tự tháp? Nguyên lý toán học nào ẩn sau điều kỳ diệu đó?'",
            "+ Bước 2: Thực hiện nhiệm vụ:",
            "- **HS:** Quan sát tranh ảnh trên màn hình, suy nghĩ, trao đổi nhanh theo cặp đôi bàn.",
            "+ Bước 3: Báo cáo, thảo luận:",
            "- **GV:** Mời đại diện 2 học sinh chia sẻ phán đoán.",
            "- **HS:** Trả lời phỏng đoán: 'Em nghĩ Thalès đã so sánh bóng của chiếc cọc với bóng của kim tự tháp; khi bóng cọc bằng chiều cao cọc thì bóng kim tự tháp cũng bằng chiều cao kim tự tháp.'",
            "+ Bước 4: Kết luận, nhận định:",
            "- **GV:** Khen ngợi trực giác toán học xuất sắc của HS và dẫn dắt vào bài mới."
        ],
        [
            "1. Tình huống thực tế:",
            "- Đo chiều cao kim tự tháp thông qua bóng nắng mặt trời.",
            "2. Dự đoán của học sinh:",
            "- Có mối liên hệ tỉ lệ giữa chiều cao vật thể và chiều dài bóng của nó dưới ánh nắng mặt trời.",
            "- Tia nắng mặt trời chiếu song song tạo ra các đoạn thẳng tỉ lệ tương ứng.",
            "3. Tâm thế học tập:",
            "- Học sinh hào hứng, mong muốn tìm hiểu bản chất toán học của Định lí Thalès."
        ]
    )
    
    # 2. Hình thành kiến thức
    add_p(doc, "B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (22 phút)", bold=True, size=13)
    
    add_activity_table(
        doc,
        "2.1. Đoạn thẳng tỉ lệ (10 phút)",
        [
            "+ Bước 1: Chuyển giao nhiệm vụ:",
            "- **GV:** Phát Phiếu học tập số 1. Yêu cầu HS quan sát các đoạn thẳng trên lưới ô vuông và tính tỉ số: AB = 2 cm, CD = 4 cm; A'B' = 3 cm, C'D' = 6 cm.",
            "- **GV:** Yêu cầu so sánh tỉ số AB/CD và A'B'/C'D'.",
            "+ Bước 2: Thực hiện nhiệm vụ:",
            "- **HS:** Làm việc cá nhân 3 phút, sau đó kiểm tra chéo đáp án với bạn cùng bàn.",
            "- **GV:** Quan sát lớp, hướng dẫn học sinh còn lúng túng khi rút gọn phân số.",
            "+ Bước 3: Báo cáo, thảo luận:",
            "- **HS:** Đứng tại chỗ phát biểu: AB/CD = 2/4 = 1/2; A'B'/C'D' = 3/6 = 1/2. Suy ra AB/CD = A'B'/C'D'.",
            "+ Bước 4: Kết luận, nhận định:",
            "- **GV:** Chốt kiến thức: Tỉ số của hai đoạn thẳng là tỉ số độ dài của chúng theo cùng một đơn vị đo. Hai đoạn thẳng AB và CD gọi là tỉ lệ với A'B' và C'D' nếu có tỉ lệ thức AB/CD = A'B'/C'D'."
        ],
        [
            "1. Tỉ số của hai đoạn thẳng:",
            "- Tỉ số của hai đoạn thẳng AB và CD là tỉ số độ dài của chúng theo cùng một đơn vị đo, kí hiệu là AB/CD.",
            "- Chú ý: Tỉ số của hai đoạn thẳng không phụ thuộc vào đơn vị đo (miễn là cùng đơn vị).",
            "2. Đoạn thẳng tỉ lệ:",
            "- Hai đoạn thẳng AB và CD gọi là tỉ lệ với hai đoạn thẳng A'B' và C'D' nếu có tỉ lệ thức:",
            "  AB / CD = A'B' / C'D'",
            "  hay AB / A'B' = CD / C'D'."
        ]
    )
    
    img1_path = os.path.join(IMG_DIR, "hinh_1_tam_giac_thales_luoi.png")
    if os.path.exists(img1_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(img1_path, width=Inches(4.2))
        add_p(doc, "Hình 1: Hoạt động khám phá định lí Thalès trên lưới ô vuông", italic=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
        
    add_activity_table(
        doc,
        "2.2. Định lí Thalès trong tam giác (12 phút)",
        [
            "+ Bước 1: Chuyển giao nhiệm vụ:",
            "- **GV:** Chiếu Hình 1 lên màn hình và phát lệnh hoạt động nhóm 4 học sinh:",
            "  1) Đếm số ô để tính tỉ số AB'/AB và AC'/AC;",
            "  2) Tính tỉ số AB'/B'B và AC'/C'C;",
            "  3) So sánh các cặp tỉ số trên và rút ra nhận xét khi d // BC.",
            "- ***(Tích hợp NLS 5.3.TC2a: GV mở tệp GeoGebra, gọi 1 đại diện HS lên bảng chạm kéo di chuyển điểm A và điểm B' để cả lớp quan sát các giá trị tỉ số trên bảng dữ liệu tự động nhảy nhưng luôn giữ nguyên dấu bằng)***.",
            "+ Bước 2: Thực hiện nhiệm vụ:",
            "- **HS:** Thảo luận nhóm, ghi kết quả vào Phiếu học tập số 1.",
            "- **GV:** Theo dõi các nhóm, hỗ trợ Nhóm 3 khi học sinh viết nhầm thứ tự đoạn thẳng.",
            "+ Bước 3: Báo cáo, thảo luận:",
            "- **HS:** Đại diện Nhóm 1 dán bảng phụ và thuyết trình.",
            "- **HS:** Cả lớp quan sát GeoGebra và đồng thanh xác nhận định lý luôn đúng.",
            "+ Bước 4: Kết luận, nhận định:",
            "- **GV:** Chuẩn hóa và phát biểu Định lí Thalès thuận:",
            "  'Nếu một đường thẳng song song với một cạnh của tam giác và cắt hai cạnh còn lại thì nó định ra trên hai cạnh đó những đoạn thẳng tương ứng tỉ lệ.'"
        ],
        [
            "1. Định lí Thalès (thuận):",
            "Nếu một đường thẳng song song với một cạnh của tam giác và cắt hai cạnh còn lại thì nó định ra trên hai cạnh đó những đoạn thẳng tương ứng tỉ lệ.",
            "2. Giả thiết & Kết luận:",
            "- GT: Tam giác ABC, d // BC (B' ∈ AB, C' ∈ AC).",
            "- KL:",
            "  + AB' / AB = AC' / AC",
            "  + AB' / B'B = AC' / C'C",
            "  + B'B / AB = C'C / AC",
            "3. Lưu ý sư phạm cốt lõi:",
            "- Các cặp đoạn thẳng phải viết đúng vị trí TƯƠNG ỨNG."
        ]
    )
    
    img2_path = os.path.join(IMG_DIR, "hinh_2_dinh_ly_thales_tong_quat.png")
    if os.path.exists(img2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_after = Pt(2)
        doc.add_picture(img2_path, width=Inches(4.2))
        add_p(doc, "Hình 2: Các đoạn thẳng tương ứng tỉ lệ theo Định lí Thalès", italic=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
        
    # 3. Luyện tập
    add_activity_table(
        doc,
        "C. HOẠT ĐỘNG 3: LUYỆN TẬP (12 phút)",
        [
            "+ Bước 1: Chuyển giao nhiệm vụ:",
            "- **GV:** Giao nhiệm vụ Luyện tập trên Phiếu học tập số 2:",
            "  Bài 1: Cho tam giác ABC, MN // BC (M ∈ AB, N ∈ AC). Biết AM = 4 cm, MB = 2 cm, AN = 6 cm. Tính độ dài x = NC.",
            "  Bài 2: Cho tam giác DEF, HK // EF (H ∈ DE, K ∈ DF). Biết DH = 3 cm, DE = 7.5 cm, DF = 10 cm. Tính độ dài y = KF.",
            "+ Bước 2: Thực hiện nhiệm vụ:",
            "- **HS:** Làm việc cá nhân trong 5 phút. 2 học sinh lên bảng trình bày.",
            "- **GV:** Quan sát, phát hiện học sinh nhầm giữa DH/HE và DH/DE để gợi ý điều chỉnh.",
            "+ Bước 3: Báo cáo, thảo luận:",
            "- **HS:** Hai học sinh trên bảng giải chi tiết và giải thích căn cứ áp dụng định lí Thalès.",
            "- **HS:** Các học sinh dưới lớp nhận xét, đối chiếu bài làm.",
            "+ Bước 4: Kết luận, nhận định:",
            "- **GV:** Chốt lời giải chuẩn mực, nhấn mạnh cách trình bày hình học logic: 1) Nêu rõ đường thẳng song song; 2) Áp dụng định lí Thalès; 3) Thay số và tính toán ẩn x, y."
        ],
        [
            "Bài 1: Tính x = NC",
            "- Vì MN // BC, theo định lí Thalès ta có:",
            "  AM / MB = AN / NC",
            "  => 4 / 2 = 6 / x",
            "  => x = (2 . 6) / 4 = 3 (cm).",
            "Vậy NC = 3 cm.",
            "",
            "Bài 2: Tính y = KF",
            "- Ta có: HE = DE - DH = 7.5 - 3 = 4.5 (cm).",
            "- Vì HK // EF, theo định lí Thalès ta có:",
            "  DH / DE = DK / DF",
            "  => DK = (DH . DF) / DE = (3 . 10) / 7.5 = 4 (cm).",
            "  => y = KF = DF - DK = 10 - 4 = 6 (cm).",
            "Vậy y = 6 cm."
        ]
    )
    
    # 4. Vận dụng
    add_activity_table(
        doc,
        "D. HOẠT ĐỘNG 4: VẬN DỤNG & STEM (5 phút)",
        [
            "+ Bước 1: Chuyển giao nhiệm vụ:",
            "- **GV:** Chiếu Hình 3 bài toán STEM bóng nắng Thalès và giao bài tập thực tế:",
            "  'Để đo chiều cao cây bàng ở sân trường THCS Trần Phú, một bạn học sinh cắm một chiếc cọc A'B' cao 1.4 m vuông góc với mặt đất. Tại cùng thời điểm nắng, bóng của cọc trên mặt đất là B'C = 2 m, bóng của cây bàng là BC = 6 m. Hỏi cây bàng cao bao nhiêu mét?'",
            "+ Bước 2: Thực hiện nhiệm vụ:",
            "- **HS:** Hoạt động nhóm bàn nhanh, phác thảo tam giác ABC và cọc A'B' // AB.",
            "+ Bước 3: Báo cáo, thảo luận:",
            "- **HS:** Đại diện 1 học sinh giải miệng: 'Vì cọc và cây đều vuông góc mặt đất nên A'B' // AB. Theo định lí Thalès: AB/A'B' = BC/B'C => AB/1.4 = 6/2 = 3 => AB = 1.4 . 3 = 4.2 m!'",
            "+ Bước 4: Kết luận, nhận định & Dặn dò:",
            "- **GV:** Khẳng định lời giải chính xác, giải thích đó chính là cách Thalès đo kim tự tháp.",
            "- **Dặn dò về nhà chuẩn bị cho Tiết 17, 18:**",
            "  1) Học thuộc định lí Thalès thuận, làm bài tập 4.1, 4.2 SGK trang 79;",
            "  2) Chuẩn bị trước nội dung Định lí Thalès đảo cho Tiết 17;",
            "  3) Mỗi nhóm chuẩn bị 1 thước dây cuộn để Tiết 18 thực hành đo bóng nắng ngoài sân trường."
        ],
        [
            "1. Lời giải bài toán STEM bóng nắng:",
            "- Vì cây bàng AB và cọc A'B' cùng vuông góc với mặt đất nên A'B' // AB.",
            "- Xét tam giác ABC có A'B' // AB, theo định lí Thalès ta có:",
            "  AB / A'B' = BC / B'C",
            "  => AB / 1.4 = 6 / 2",
            "  => AB = (1.4 . 6) / 2 = 4.2 (m).",
            "Vậy cây bàng sân trường cao 4.2 mét.",
            "",
            "2. Hướng dẫn tự học:",
            "- Nắm vững điều kiện áp dụng: Bắt buộc phải có yếu tố SONG SONG."
        ]
    )
    
    img3_path = os.path.join(IMG_DIR, "hinh_3_ung_dung_thales_do_bong_nang.png")
    if os.path.exists(img3_path):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.paragraph_format.space_after = Pt(2)
        doc.add_picture(img3_path, width=Inches(4.5))
        add_p(doc, "Hình 3: Ứng dụng STEM đo chiều cao cây bóng mát thông qua bóng nắng mặt trời", italic=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
        
    # KHÁI QUÁT TIẾT 17 VÀ TIẾT 18 (VẬN DỤNG VÀO TUẦN 9 - ĐẦU THÁNG 11)
    add_p(doc, "TÓM TẮT TIẾN TRÌNH TIẾT 17 VÀ TIẾT 18 (VẬN DỤNG VÀO TUẦN 9 - ĐẦU THÁNG 11)", bold=True, size=13.5, space_before=8)
    
    add_p(doc, "1. TIẾT 17: ĐỊNH LÍ THALÈS ĐẢO TRONG TAM GIÁC", bold=True, size=13)
    add_p(doc, "- Mục tiêu: Học sinh phát biểu được định lí Thalès đảo; biết chứng minh hai đường thẳng song song dựa vào các đoạn thẳng tỉ lệ.")
    add_p(doc, "- Tiến trình tổ chức: Khởi động kiểm tra bài cũ (4 phút) -> Khám phá Định lí đảo qua hình vẽ đối chứng (15 phút) -> Luyện tập chứng minh song song và nhận biết hình thang (18 phút) -> Vận dụng củng cố (8 phút).")
    
    add_p(doc, "2. TIẾT 18: LUYỆN TẬP VÀ HOẠT ĐỘNG THỰC HÀNH STEM NGOÀI TRỜI (TUẦN 9 - ĐẦU THÁNG 11)", bold=True, size=13)
    add_p(doc, "- Mục tiêu: Học sinh vận dụng tổng hợp định lí Thalès thuận, đảo; sử dụng thước dây và cọc tiêu để đo chiều cao cột cờ, cây bàng sân trường THCS Trần Phú.")
    add_p(doc, "- Tiến trình tổ chức:")
    add_p(doc, "  + Hoạt động 1: Ôn tập hệ thống hóa kiến thức 2 định lí bằng Sơ đồ tư duy Mindmap (10 phút).")
    add_p(doc, "  + Hoạt động 2: Phân chia 4 nhóm ra sân trường thực hành đo bóng nắng và góc nghiêng (20 phút).")
    add_p(doc, "  + Hoạt động 3: Báo cáo số liệu đo đạc, tính toán chiều cao vật thể và đánh giá sai số giữa các nhóm (15 phút).")
    
    # Phụ lục phiếu học tập & Rubric
    add_p(doc, "IV. PHỤ LỤC HỌC LIỆU VÀ RUBRIC ĐÁNH GIÁ", bold=True, size=13, space_before=6)
    
    add_p(doc, "1. Phiếu học tập số 1 (Khám phá định lí Thalès thuận):", bold=True)
    add_p(doc, "- Nhiệm vụ 1: Đếm ô vuông trên Hình 1 và điền vào chỗ trống: AB' = ... ô; AB = ... ô; AC' = ... ô; AC = ... ô.")
    add_p(doc, "- Nhiệm vụ 2: Lập tỉ số: AB'/AB = ... ; AC'/AC = ... => So sánh: AB'/AB ... AC'/AC.")
    add_p(doc, "- Nhiệm vụ 3: Rút ra kết luận tổng quát khi một đường thẳng song song với cạnh tam giác.")
    
    add_p(doc, "2. Bảng Rubric đánh giá hoạt động học sinh trong chủ đề 3 tiết:", bold=True)
    tbl_rb = doc.add_table(rows=4, cols=4)
    tbl_rb.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_rb)
    rb_heads = ["Tiêu chí đánh giá", "Mức 1 (Chưa đạt)", "Mức 2 (Đạt)", "Mức 3 (Tốt)"]
    rb_w = [Inches(1.8), Inches(1.6), Inches(1.8), Inches(1.8)]
    for i, h in enumerate(rb_heads):
        c = tbl_rb.cell(0, i)
        c.width = rb_w[i]
        set_cell_bg(c, "F1F5F9")
        set_cell_margins(c, 70, 70, 60, 60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    rb_rows = [
        ("1. Khám phá & Phát biểu định lý (Tiết 16, 17)", "Chưa đếm đúng ô lưới, chưa lập được tỉ số tương ứng.", "Đếm đúng ô lưới, lập được tỉ số và phát biểu được định lý.", "Thao tác thành thạo, phát biểu chuẩn xác, tương tác tự tin với mô phỏng GeoGebra."),
        ("2. Kỹ năng tính toán & Chứng minh", "Viết sai tỉ lệ thức hoặc nhầm lẫn giữa các cạnh.", "Viết đúng tỉ lệ thức, thay số tính đúng ẩn số ở bài cơ bản.", "Giải nhanh, trình bày chuẩn mực hình học, giải quyết tốt bài toán có tam giác xoay hướng."),
        ("3. Tinh thần hợp tác & Thực hành STEM (Tiết 18)", "Thụ động, dựa dẫm vào các bạn trong nhóm.", "Tham gia thảo luận nhóm, ghi chép đầy đủ vào phiếu đo thực tế.", "Chủ động điều phối nhóm, thao tác đo bóng nắng chuẩn xác, báo cáo số liệu sáng tạo.")
    ]
    for row_idx, r_data in enumerate(rb_rows, start=1):
        for col_idx, text in enumerate(r_data):
            c = tbl_rb.cell(row_idx, col_idx)
            c.width = rb_w[col_idx]
            set_cell_margins(c, 60, 60, 60, 60)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if col_idx == 0:
                r = p.add_run(text)
                r.bold = True
            else:
                r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            
    add_p(doc, "", space_after=10)
    add_signatures(
        doc,
        "GIÁO VIÊN SOẠN BÀI",
        "Trần Long Hải - Lê Thị Bình",
        "TỔ TRƯỞNG CHUYÊN MÔN DUYỆT",
        "Hoàng Tấn Thiên",
        left_sub="(Ký và ghi rõ họ tên)",
        right_sub="(Ký và ghi rõ họ tên)"
    )
    
    out_file = os.path.join(OUTPUT_DIR, "NCBH_03_Ke_Hoach_Bai_Day_Minh_Hoa_Dinh_Ly_Thales.docx")
    doc.save(out_file)
    print("XUẤT THÀNH CÔNG:", out_file)

if __name__ == "__main__":
    create_doc_1()
    create_doc_2()
    create_doc_3()
    print("HOÀN THÀNH CẬP NHẬT 3 FILE ĐẦU TIÊN THEO TUẦN 8, 9!")
