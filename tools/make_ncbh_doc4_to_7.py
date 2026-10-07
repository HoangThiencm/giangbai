# -*- coding: utf-8 -*-
"""
Module sinh tài liệu NCBH 4, 5, 6, 7 (CẬP NHẬT CHUẨN XÁC TUẦN 8, 9 - CUỐI THÁNG 10 & ĐẦU THÁNG 11)
4. NCBH_04_Phieu_Quan_Sat_Va_Danh_Gia_Tiet_Day.docx
5. NCBH_05_Bien_Ban_Buoc_3_Thao_Luan_Suy_Ngam.docx
6. NCBH_06_Bao_Cao_Tong_Ket_Va_Van_Dung_Buoc_4.docx
7. NCBH_Chu_Y.docx
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
# 4. FILE 4: NCBH_04_Phieu_Quan_Sat_Va_Danh_Gia_Tiet_Day.docx
# ==============================================================================
def create_doc_4():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(
        doc,
        ["TRƯỜNG THCS TRẦN PHÚ", "TỔ TOÁN – TIN"],
        "Mẫu số: 01/PQS-NCBH",
        "Xuân Đông, ngày 28 tháng 10 năm 2026"
    )
    
    add_p(doc, "PHIẾU QUAN SÁT VÀ GHI CHÉP TIẾT DẠY", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "SINH HOẠT CHUYÊN MÔN THEO NGHIÊN CỨU BÀI HỌC", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "(Thực hiện theo định hướng Công văn số 5555/BGDĐT-GDTrH của Bộ Giáo dục và Đào tạo)", italic=True, size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    
    add_callout(
        doc,
        "TIẾT DẠY MINH HỌA: Tiết 16 (Tiết 1 trong chuỗi 3 tiết Bài 15) - Thực hiện tại lớp 8A1 vào sáng thứ Tư ngày 28/10/2026 (Tuần 8 - Cuối tháng 10). MỤC ĐÍCH QUAN SÁT: Tập trung ghi nhận thực tế HOẠT ĐỘNG HỌC CỦA HỌC SINH (sự tiếp nhận, thái độ, khó khăn nhận diện và mức độ hiểu bài). TUYỆT ĐỐI KHÔNG đánh giá xếp loại giáo viên dạy.",
        title="THỜI ĐIỂM QUAN SÁT (TUẦN 8 - CUỐI THÁNG 10):",
        border_color="DC2626",
        bg_color="FEF2F2"
    )
    
    add_p(doc, "I. THÔNG TIN CHUNG TIẾT DẠY MINH HỌA", bold=True, size=13)
    add_p(doc, "- Bài dạy: Bài 15. Định lí Thalès trong tam giác (Tiết 1 - Tiết 16 theo PPCT Phụ lục 3).")
    add_p(doc, "- Môn học: Toán - Khối lớp: 8 (Lớp: 8A1 - Sĩ số: 38 học sinh).")
    add_p(doc, "- Họ và tên giáo viên dạy minh họa: Thầy Trần Long Hải.")
    add_p(doc, "- Thời gian: Tiết 2, sáng thứ Tư ngày 28 tháng 10 năm 2026 (Tuần 8 - Cuối tháng 10).")
    add_p(doc, "- Họ và tên người quan sát (dự giờ): Thầy Hồ Đăng Danh (GV môn Toán).")
    add_p(doc, "- Vị trí quan sát được phân công: Dãy 1 (Theo dõi chuyên sâu Nhóm 1 và Nhóm 2).")
    
    add_p(doc, "II. TIÊU CHÍ QUAN SÁT HOẠT ĐỘNG HỌC CỦA HỌC SINH (CV 5555/BGDĐT)", bold=True, size=13)
    
    tbl_tc = doc.add_table(rows=5, cols=3)
    tbl_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_tc)
    tc_h = ["Tiêu chí quan sát", "Biểu hiện cụ thể cần theo dõi", "Mức độ quan sát được"]
    tc_w = [Inches(1.8), Inches(3.6), Inches(1.3)]
    for i, h in enumerate(tc_h):
        c = tbl_tc.cell(0, i)
        c.width = tc_w[i]
        set_cell_bg(c, "F1F5F9")
        set_cell_margins(c, 70, 70, 60, 60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    tc_data = [
        ("1. Khả năng tiếp nhận nhiệm vụ học tập", "- Học sinh có chú ý lắng nghe, hiểu rõ yêu cầu trong phiếu học tập không?\n- Có học sinh nào ngơ ngác, không biết bắt đầu làm gì không?", "Tốt (95% HS hiểu ngay yêu cầu, 2 em cần GV nhắc lại lệnh)."),
        ("2. Sự chủ động, tích cực và hợp tác", "- Học sinh làm việc cá nhân có tập trung không? Khi hoạt động nhóm có chia sẻ, hỗ trợ nhau hay chỉ có 1-2 em làm còn lại ngồi chơi?", "Tích cực (Nhóm 1 phân công rõ: 1 em đếm ô, 1 em ghi tỉ số, 2 em phản biện)."),
        ("3. Khả năng trình bày và phản biện", "- Học sinh có tự tin phát biểu, dán bảng phụ, giải thích cách làm không? Ngôn ngữ toán học có mạch lạc không?", "Khá tốt (Đại diện nhóm trình bày tự tin, chỉ rõ căn cứ trên lưới ô vuông)."),
        ("4. Mức độ đạt được chuẩn kiến thức", "- Học sinh có phát biểu đúng định lý không? Tính toán độ dài x, y có chính xác không? Có bị nhầm lẫn cặp tỉ số không?", "Rất tốt (88% làm đúng hoàn toàn bài luyện tập ngay tại lớp).")
    ]
    for row_idx, r_data in enumerate(tc_data, start=1):
        for col_idx, text in enumerate(r_data):
            c = tbl_tc.cell(row_idx, col_idx)
            c.width = tc_w[col_idx]
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
            
    add_p(doc, "", space_after=4)
    add_p(doc, "III. NHẬT KÝ QUAN SÁT TIẾN TRÌNH TIẾT DẠY (GHI CHÉP MINH CHỨNG THỰC TẾ)", bold=True, size=13)
    
    tbl_nk = doc.add_table(rows=6, cols=5)
    tbl_nk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_nk)
    nk_h = ["Thời gian", "Hoạt động dạy học", "Hành vi của học sinh (Minh chứng cụ thể)", "Khó khăn / Rào cản nhận diện", "Biện pháp hỗ trợ đã diễn ra"]
    nk_w = [Inches(1.0), Inches(1.5), Inches(1.8), Inches(1.3), Inches(1.3)]
    for i, h in enumerate(nk_h):
        c = tbl_nk.cell(0, i)
        c.width = nk_w[i]
        set_cell_bg(c, "F1F5F9")
        set_cell_margins(c, 70, 70, 60, 60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        
    nk_data = [
        ("00 - 06'\n(6 phút)", "HĐ 1: Khởi động (STEM Thales đo kim tự tháp)", "100% học sinh hướng mắt lên màn hình khi thấy video kim tự tháp. Em Minh (bàn 2) thì thầm với bạn bên cạnh: 'Chắc là đo bóng nắng rồi!'. Khi GV hỏi, 5 cánh tay giơ lên xin phát biểu.", "Một số học sinh chưa rõ tại sao tia nắng mặt trời lại xem là những đường thẳng song song.", "GV chiếu mô phỏng tia sáng song song từ mặt trời ở rất xa, HS gật gù hiểu ngay."),
        ("06 - 16'\n(10 phút)", "HĐ 2.1: Đoạn thẳng tỉ lệ", "HS nhận Phiếu học tập số 1. Em Trang (Nhóm 1) dùng bút chì đo từng vạch rất cẩn thận. Em Huy (Nhóm 2) tính nhầm 2/4 = 2, nhưng được bạn ngồi cạnh nhắc 'lấy tử chia mẫu chứ' nên sửa lại thành 1/2.", "Học sinh thao tác chậm mất 1-2 phút ở khâu rút gọn phân số tỉ số.", "GV đi xuống cuối dãy 1, chạm vai động viên em Huy tự tin làm tiếp."),
        ("16 - 28'\n(12 phút)", "HĐ 2.2: Định lí Thalès trong tam giác", "Khi GV mở GeoGebra, em Tuấn được mời lên chạm màn hình kéo điểm B'. Cả lớp ồ lên thích thú vì thấy bảng số liệu tự nhảy nhưng 2 tỉ số luôn bằng 0.5. Các nhóm thảo luận rôm rả, tự rút ra kết luận.", "Ở Nhóm 2, em Nam viết hệ thức AB'/B'B = AC'/AC (nhầm mẫu số bên phải AC thay vì C'C).", "Bạn cùng nhóm chỉ vào hình: 'Đoạn trên chia đoạn dưới thì bên này cũng phải AC' chia C'C chứ!'. Em Nam tự gạch đi sửa lại."),
        ("28 - 40'\n(12 phút)", "HĐ 3: Luyện tập (Phiếu học tập 2)", "Cả lớp im lặng làm bài cá nhân. 2 học sinh lên bảng giải Bài 1 và Bài 2. Ở dưới lớp, 34/38 em làm xong trước thời gian 4 phút và bắt đầu so sánh kết quả với nhau.", "Em Linh (bàn 4) gặp khó khăn ở Bài 2 vì phải tính HE = DE - DH trước rồi mới áp dụng định lý.", "GV gợi ý chung cho cả lớp: 'Quan sát kỹ xem đoạn thẳng trong công thức đã có sẵn độ dài chưa, hay phải làm phép trừ?'. Em Linh làm được ngay."),
        ("40 - 45'\n(5 phút)", "HĐ 4: Vận dụng & Dặn dò", "Học sinh hào hứng giải bài toán cây bàng sân trường. Đại diện 1 học sinh trả lời miệng nhanh và chính xác 4.2 mét. Cả lớp vỗ tay.", "Thời gian gần hết nên chưa gọi được nhiều học sinh phát biểu.", "GV chuyển câu hỏi mở rộng chuẩn bị cho Tiết 17, 18 vào nhiệm vụ tự học ở nhà.")
    ]
    for row_idx, r_data in enumerate(nk_data, start=1):
        for col_idx, text in enumerate(r_data):
            c = tbl_nk.cell(row_idx, col_idx)
            c.width = nk_w[col_idx]
            set_cell_margins(c, 50, 50, 50, 50)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(text)
                r.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            
    add_p(doc, "", space_after=4)
    add_p(doc, "IV. ĐÁNH GIÁ CHUNG VÀ BÀI HỌC KINH NGHIỆM CHO BẢN THÂN", bold=True, size=13)
    add_p(doc, "1. Điều tâm đắc nhất về việc học của học sinh:")
    add_p(doc, "- Học sinh lớp 8A1 học tập rất tự nhiên, chủ động, không có biểu hiện gượng ép hay học trước. Việc kết hợp phần mềm GeoGebra với lưới ô vuông đã xóa tan sự khô khan trừu tượng của môn Hình học, giúp các em 'nhìn thấy' định lý trước khi phải ghi nhớ công thức.")
    add_p(doc, "2. Điểm cần điều chỉnh để học sinh học tốt hơn:")
    add_p(doc, "- Cần dành thêm khoảng 1-2 phút ở bước hướng dẫn viết các cặp tỉ số tương ứng, có thể dùng 3 màu phấn khác nhau trên bảng (màu đỏ cho đoạn trên, màu vàng cho đoạn dưới, màu trắng cho toàn bộ cạnh) để học sinh thị giác yếu dễ dàng phân biệt.")
    add_p(doc, "3. Kế hoạch tiếp nối cho Tiết 17, Tiết 18 (Tuần 9 - Đầu tháng 11):")
    add_p(doc, "- Phát huy tinh thần học tập tích cực này sang Tiết 17 (Định lí đảo) và Tiết 18 (thực hành STEM đo bóng nắng ngoài sân trường) để học sinh vận dụng nhuần nhuyễn kiến thức vào thực tế đời sống.")
    
    add_p(doc, "", space_after=10)
    add_signatures(
        doc,
        "XÁC NHẬN CỦA TỔ TRƯỞNG",
        "Hoàng Tấn Thiên",
        "GIÁO VIÊN QUAN SÁT (DỰ GIỜ)",
        "Hồ Đăng Danh",
        left_sub="(Ký và ghi rõ họ tên)",
        right_sub="(Ký và ghi rõ họ tên)"
    )
    
    out_file = os.path.join(OUTPUT_DIR, "NCBH_04_Phieu_Quan_Sat_Va_Danh_Gia_Tiet_Day.docx")
    doc.save(out_file)
    print("XUẤT THÀNH CÔNG:", out_file)

# ==============================================================================
# 5. FILE 5: NCBH_05_Bien_Ban_Buoc_3_Thao_Luan_Suy_Ngam.docx
# ==============================================================================
def create_doc_5():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(
        doc,
        ["TRƯỜNG THCS TRẦN PHÚ", "TỔ TOÁN – TIN"],
        "Số: 03/BB-NCBH",
        "Xuân Đông, ngày 28 tháng 10 năm 2026"
    )
    
    add_p(doc, "BIÊN BẢN HỌP TỔ CHUYÊN MÔN", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "BƯỚC 3: PHÂN TÍCH, SUY NGẪM BÀI HỌC SAU KHI DỰ GIỜ", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Chuyên đề Nghiên cứu bài học môn Toán 8 - Bài 15: Định lí Thalès trong tam giác (Tiết 16 - Tuần 8, Cuối tháng 10/2026)", italic=True, size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    
    add_p(doc, "I. THỜI GIAN, ĐỊA ĐIỂM VÀ THÀNH PHẦN", bold=True, size=13)
    add_p(doc, "1. Thời gian: Vào hồi 09 giờ 40 phút (Tiết 4), ngày 28 tháng 10 năm 2026 (ngay sau tiết 2 dạy minh họa tại 8A1).")
    add_p(doc, "2. Địa điểm: Phòng Hội đồng sư phạm Trường THCS Trần Phú.")
    add_p(doc, "3. Thành phần tham dự:")
    add_p(doc, "- Chủ trì: Thầy Hoàng Tấn Thiên – Tổ trưởng chuyên môn.")
    add_p(doc, "- Thư ký: Cô Nguyễn Thị Thảo – Giáo viên Toán.")
    add_p(doc, "- Toàn thể 07/07 giáo viên trong tổ Toán – Tin tham gia dự giờ có mặt đầy đủ.")
    
    add_p(doc, "II. TIẾN TRÌNH THẢO LUẬN, SUY NGẪM BÀI HỌC", bold=True, size=13)
    add_p(doc, "1. Quán triệt của Chủ trì (Thầy Hoàng Tấn Thiên):", bold=True)
    add_p(doc, "Thầy Hoàng Tấn Thiên phát biểu định hướng: 'Chúc mừng thầy Trần Long Hải và nhóm Toán 8 đã hoàn thành xuất sắc tiết dạy minh họa Tiết 16 (Tiết 1 của chủ đề Bài 15) vào thời điểm Tuần 8 - Cuối tháng 10. Tôi xin nhắc lại nguyên tắc cốt lõi của Bước 3 trong sinh hoạt chuyên môn theo nghiên cứu bài học: Mục đích hôm nay KHÔNG PHẢI là đánh giá, xếp loại giáo viên, không soi xét cá nhân người dạy. Chúng ta ngồi lại đây để cùng nhau phân tích VIỆC HỌC CỦA HỌC SINH: các em đã học như thế nào? Em nào tiếp thu tốt, em nào gặp khó khăn, nguyên nhân tại sao và chúng ta có giải pháp sư phạm gì để hoàn thiện giáo án, chuẩn bị cho việc dạy nhân rộng và dạy tiếp Tiết 17, 18 ở Tuần 9 (Đầu tháng 11). Đề nghị thầy Hải chia sẻ trước cảm xúc và suy nghĩ của mình.'")
    
    add_p(doc, "2. Ý kiến tự bộc bạch, chia sẻ của Giáo viên dạy minh họa (Thầy Trần Long Hải):", bold=True)
    add_p(doc, "- Cảm xúc chung: Tôi cảm thấy rất nhẹ nhõm và vui vì các em học sinh lớp 8A1 hôm nay rất tự nhiên, hào hứng, không bị áp lực dù có nhiều thầy cô ngồi dự xung quanh.")
    add_p(doc, "- Điều tâm đắc nhất:")
    add_p(doc, "  + Phần khởi động lịch sử kim tự tháp đã kích thích được tò mò của học sinh ngay từ phút đầu tiên.")
    add_p(doc, "  + Việc đưa GeoGebra lên màn hình tương tác thực sự phát huy tác dụng. Khi em Tuấn lên kéo thả điểm A, tôi quan sát thấy ánh mắt học sinh cả lớp sáng lên vì các em tận mắt chứng kiến các tỉ số nhảy số nhưng luôn bằng nhau.")
    add_p(doc, "- Điều còn trăn trở, băn khoăn:")
    add_p(doc, "  + Ở Hoạt động 2.2, khi làm việc nhóm, tôi quan sát thấy ở Nhóm 3 có em Nam và em Huy còn lúng túng khi lập tỉ số, em Nam viết nhầm mẫu số bên phải. Do thời gian có hạn nên tôi chỉ kịp nhắc bạn cùng nhóm hỗ trợ mà chưa trực tiếp giảng giải sâu cho em.")
    add_p(doc, "  + Ở Hoạt động 3, tôi hơi tham chi tiết nên phần Luyện tập bị kéo dài sang phút thứ 39, làm cho phần vận dụng STEM ngoài sân trường chỉ kịp chốt trên slide mà chưa cho học sinh thảo luận sâu về sai số khi đo nắng.")
    
    add_p(doc, "3. Ý kiến chia sẻ của Giáo viên đồng hành xây dựng bài dạy (Cô Lê Thị Bình):", bold=True)
    add_p(doc, "- Tôi phụ trách quan sát góc bàn phía trong của lớp: Tôi thấy Phiếu học tập số 1 thiết kế lưới ô vuông rất thành công. Học sinh trung bình như em Mai, em Khoa đếm ô vuông 2/4 = 1/2 rất nhanh, không bị sợ toán như mọi khi.")
    add_p(doc, "- Tuy nhiên, phiếu học tập số 2 ở Bài tập 2, đề bài cho DE = 7.5 cm là số thập phân, một số học sinh nhân chia số thập phân hơi chậm làm ảnh hưởng đến tiến độ của nhóm. Tuần sau (Tuần 9 - Đầu tháng 11) khi tôi dạy tại 8A2, tôi sẽ điều chỉnh số liệu thành số nguyên đẹp hơn (ví dụ DE = 8 cm) để học sinh tập trung trọn vẹn vào bản chất hình học.")
    
    add_p(doc, "4. Ý kiến phân tích minh chứng của các Giáo viên dự giờ quan sát:", bold=True)
    add_p(doc, "- Thầy Hồ Đăng Danh (quan sát Dãy 1): Nhóm 1 hoạt động rất tự giác, em Trang đã nhắc bạn Hùng sửa lỗi nghịch đảo tỉ số; chứng tỏ sự hợp tác nhóm rất hiệu quả.")
    add_p(doc, "- Thầy Trần Sáng (quan sát Dãy 2): Em Nam ở Nhóm 3 lúng túng khi nhìn hình vẽ nghiêng, cần chuẩn bị sẵn thước kẻ trong suốt hoặc hiệu ứng nhấp nháy trên slide để hỗ trợ học sinh có tư duy thị giác yếu.")
    add_p(doc, "- Thầy Hoàng Xuân Ánh (quan sát Dãy 3): Học sinh rất hào hứng với bài toán STEM đo bóng nắng cây bàng, cần chuẩn bị tốt dụng cụ để Tiết 18 (Tuần 9) ra sân trường thực hành đạt hiệu quả cao nhất.")
    add_p(doc, "- Thầy Dương Quang Tùng: Đánh giá cao hiệu ứng tương tác của GeoGebra trên Tivi thông minh, học sinh được trực tiếp chạm kéo tạo sự khắc sâu kiến thức tuyệt đối.")
    
    add_p(doc, "5. Thảo luận thống nhất giải pháp điều chỉnh Kế hoạch bài dạy:", bold=True)
    add_p(doc, "Toàn tổ thảo luận sôi nổi và thống nhất 3 giải pháp cải tiến sư phạm cụ thể:")
    add_p(doc, "1) Về hình vẽ & Bảng: Dùng màu phấn phân biệt (màu đỏ cho đoạn trên, màu vàng cho đoạn dưới) để khắc sâu quy tắc 'tương ứng tỉ lệ'.")
    add_p(doc, "2) Về số liệu bài tập: Chỉnh sửa số liệu Bài 2 trong Phiếu học tập số 2 cho chẵn đẹp, tránh để phép tính thập phân cản trở tư duy hình học của học sinh trung bình.")
    add_p(doc, "3) Kế hoạch triển khai Tuần 9 (Đầu tháng 11): Hoàn thiện giáo án để cô Lê Thị Bình dạy tại lớp 8A2, 8A3 và thầy Hải dạy tại 8A4; đồng thời triển khai trọn vẹn Tiết 17 (Định lí đảo) và Tiết 18 (thực hành STEM đo bóng nắng ngoài sân trường).")
    
    add_p(doc, "6. Kết luận chỉ đạo của Tổ trưởng chuyên môn (Thầy Hoàng Tấn Thiên):", bold=True)
    add_p(doc, "- Đánh giá tổng kết: Buổi sinh hoạt chuyên môn theo nghiên cứu bài học Bước 3 diễn ra đúng quy trình, thực chất, mang lại giá trị học hỏi to lớn cho toàn thể giáo viên trong tổ.")
    add_p(doc, "- Tiết dạy minh họa của thầy Trần Long Hải đạt hiệu quả cao, học sinh chủ động, nắm vững kiến thức trọng tâm.")
    add_p(doc, "- Giao nhiệm vụ cho Cô Lê Thị Bình tiếp thu toàn bộ các giải pháp điều chỉnh, hoàn thiện bản Kế hoạch bài dạy chuẩn mực để triển khai dạy thực nghiệm tại các lớp 8A2, 8A3 vào Tuần 9 (Đầu tháng 11/2026).")
    
    add_p(doc, "III. KẾT THÚC CUỘC HỌP", bold=True, size=13)
    add_p(doc, "Biên bản được thông qua và nhất trí 100% bởi các thành viên dự họp.")
    add_p(doc, "Cuộc họp kết thúc vào lúc 11 giờ 30 phút cùng ngày./.")
    
    add_p(doc, "", space_after=10)
    add_signatures(
        doc,
        "THƯ KÝ BIÊN BẢN",
        "Nguyễn Thị Thảo",
        "TỔ TRƯỞNG CHUYÊN MÔN",
        "Hoàng Tấn Thiên"
    )
    
    out_file = os.path.join(OUTPUT_DIR, "NCBH_05_Bien_Ban_Buoc_3_Thao_Luan_Suy_Ngam.docx")
    doc.save(out_file)
    print("XUẤT THÀNH CÔNG:", out_file)

# ==============================================================================
# 6. FILE 6: NCBH_06_Bao_Cao_Tong_Ket_Va_Van_Dung_Buoc_4.docx
# ==============================================================================
def create_doc_6():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(
        doc,
        ["PHÒNG GIÁO DỤC VÀ ĐÀO TẠO", "TRƯỜNG THCS TRẦN PHÚ", "TỔ TOÁN – TIN"],
        "Số: 09/BC-TTH",
        "Xuân Đông, ngày 09 tháng 11 năm 2026"
    )
    
    add_p(doc, "BÁO CÁO TỔNG KẾT CHUYÊN ĐỀ", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "SINH HOẠT CHUYÊN MÔN THEO NGHIÊN CỨU BÀI HỌC VÀ KẾ HOẠCH VẬN DỤNG (BƯỚC 4)", bold=True, size=13.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Môn: Toán - Khối 8 - Học kỳ I năm học 2026 - 2027", italic=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Chủ đề nghiên cứu: Bài 15. Định lí Thalès trong tam giác (3 tiết - Tuần 8, 9 theo PPCT Phụ lục 3)", italic=True, size=12.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    
    add_callout(
        doc,
        "BÁO CÁO TỔNG KẾT BƯỚC 4: Được lập vào ngày 09/11/2026 (Tuần 10) sau khi đã hoàn thành trọn vẹn chuỗi 3 tiết (Tiết 16, 17, 18) của Bài 15 trong suốt Tuần 8 (Cuối tháng 10) và Tuần 9 (Đầu tháng 11/2026) tại tất cả các lớp khối 8 Trường THCS Trần Phú.",
        title="ĐỒNG BỘ TIẾN ĐỘ THỰC TẾ TUẦN 8 & TUẦN 9:",
        border_color="16A34A",
        bg_color="F0FDF4"
    )
    
    add_p(doc, "I. ĐÁNH GIÁ TỔNG QUAN QUÁ TRÌNH TRIỂN KHAI CHUYÊN ĐỀ", bold=True, size=13)
    add_p(doc, "Thực hiện Kế hoạch số 08/KH-TTH ngày 20/10/2026 của Tổ Toán – Tin Trường THCS Trần Phú, tổ chuyên môn đã tiến hành thực hiện nghiêm túc chuyên đề Sinh hoạt chuyên môn theo nghiên cứu bài học theo đúng 4 bước chuẩn của Bộ Giáo dục và Đào tạo (Công văn số 5555/BGDĐT-GDTrH), bám sát tiến độ Phụ lục 3 môn Toán 8:")
    add_p(doc, "- Bước 1 (Xây dựng KHBD): Tổ chức ngày 22/10/2026 (Tuần 7) với sự tham gia của 7/7 giáo viên. Nhóm Toán 8 (thầy Hải, cô Bình) đã biên soạn giáo án 3 tiết công phu, tích hợp STEM và năng lực số.")
    add_p(doc, "- Bước 2 (Dạy minh họa & Dự giờ): Thực hiện ngày 28/10/2026 (Tuần 8 - Cuối tháng 10) tại lớp 8A1 (Tiết 16) do thầy Trần Long Hải giảng dạy. 100% giáo viên trong tổ tham gia dự giờ, bố trí các góc quan sát khoa học.")
    add_p(doc, "- Bước 3 (Phân tích, suy ngẫm bài học): Tổ chức ngay sau tiết dạy ngày 28/10/2026. Không khí thảo luận cởi mở, chân thành, tập trung 100% vào hoạt động học của học sinh, rút ra được các giải pháp sư phạm điều chỉnh thiết thực.")
    add_p(doc, "- Bước 4 (Vận dụng vào thực tiễn): Triển khai trong suốt Tuần 9 (Đầu tháng 11 - Từ 02/11 đến 07/11/2026) tại các lớp 8A2, 8A3, 8A4; thực hiện dạy trọn vẹn cả 3 tiết (Tiết 16, 17, 18) gắn với hoạt động thực hành STEM đo bóng nắng ngoài sân trường.")
    
    add_p(doc, "II. KẾT QUẢ ĐẠT ĐƯỢC VỀ HOẠT ĐỘNG HỌC CỦA HỌC SINH", bold=True, size=13)
    add_p(doc, "Tổ chuyên môn đã tiến hành khảo sát và đánh giá học sinh trên toàn bộ 4 lớp khối 8 sau khi hoàn thành chuỗi 3 tiết:")
    
    tbl_kq = doc.add_table(rows=5, cols=4)
    tbl_kq.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_kq)
    kq_h = ["Nội dung khảo sát đánh giá", "Khi chưa áp dụng NCBH (Năm trước)", "Sau khi áp dụng NCBH (Khối 8)", "Mức độ cải thiện"]
    kq_w = [Inches(2.5), Inches(1.5), Inches(1.5), Inches(1.2)]
    for i, h in enumerate(kq_h):
        c = tbl_kq.cell(0, i)
        c.width = kq_w[i]
        set_cell_bg(c, "F1F5F9")
        set_cell_margins(c, 70, 70, 60, 60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    kq_data = [
        ("Tỉ lệ HS hiểu bản chất & phát biểu đúng định lý", "65.5%", "94.7%", "Tăng 29.2%"),
        ("Tỉ lệ HS lập đúng các cặp đoạn thẳng tương ứng tỉ lệ", "58.0%", "89.5%", "Tăng 31.5%"),
        ("Tỉ lệ HS mắc lỗi nhầm lẫn thứ tự đoạn thẳng", "34.5%", "5.3%", "Giảm 29.2%"),
        ("Tỉ lệ HS đạt điểm Khá, Giỏi bài kiểm tra chuyên đề", "62.0%", "92.1%", "Tăng 30.1%")
    ]
    for row_idx, r_data in enumerate(kq_data, start=1):
        for col_idx, text in enumerate(r_data):
            c = tbl_kq.cell(row_idx, col_idx)
            c.width = kq_w[col_idx]
            set_cell_margins(c, 60, 60, 60, 60)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            if col_idx in [1, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            if col_idx == 3:
                r.bold = True
                
    add_p(doc, "", space_after=4)
    add_p(doc, "III. NHỮNG BÀI HỌC KINH NGHIỆM SƯ PHẠM RÚT RA", bold=True, size=13)
    add_p(doc, "1. Về phương pháp dạy học hình học trực quan:")
    add_p(doc, "- Sử dụng lưới ô vuông kết hợp phần mềm hình học động GeoGebra giúp biến các khái niệm tỉ số trừu tượng thành hình ảnh trực quan sinh động. Học sinh được tự tay thao tác đo đạc, kéo thả điểm thì nhớ sâu và hiểu bản chất gấp nhiều lần so với việc nghe giảng thụ động.")
    add_p(doc, "2. Về tổ chức giáo dục STEM thực tế (Tiết 18):")
    add_p(doc, "- Đưa học sinh ra sân trường thực hành đo bóng nắng mặt trời tạo ra sự gắn kết tuyệt vời giữa lý thuyết sách vở và ứng dụng thực tiễn. Học sinh hiểu được tại sao các nhà toán học cổ đại lại sáng tạo ra định lý.")
    add_p(doc, "3. Về kỹ thuật quản lý hoạt động nhóm thực chất:")
    add_p(doc, "- Phân vai rõ ràng cho từng thành viên trong nhóm 4 người (nhóm trưởng điều phối, thư ký ghi chép, thành viên phản biện và kiểm tra số liệu) giúp triệt tiêu hoàn toàn tình trạng học sinh ngồi chơi ỷ lại.")
    
    add_p(doc, "IV. KẾ HOẠCH DUY TRÌ VÀ LAN TỎA SAU BƯỚC 4", bold=True, size=13)
    add_p(doc, "- Tiếp tục áp dụng quy trình thiết kế bài dạy trực quan gắn với chuyển đổi số cho các bài học tiếp theo của Chương IV:")
    add_p(doc, "  + Bài 16: Đường trung bình của tam giác (Tiết 21, 22 - Tuần 11, 12);")
    add_p(doc, "  + Bài 17: Tính chất đường phân giác của tam giác (Tiết 23 - Tuần 13).")
    add_p(doc, "- Đưa toàn bộ sản phẩm hồ sơ NCBH lên kho học liệu số của trường để toàn thể giáo viên tham khảo, nhân rộng.")
    
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
    
    out_file = os.path.join(OUTPUT_DIR, "NCBH_06_Bao_Cao_Tong_Ket_Va_Van_Dung_Buoc_4.docx")
    doc.save(out_file)
    print("XUẤT THÀNH CÔNG:", out_file)

# ==============================================================================
# 7. FILE 7: NCBH_Chu_Y.docx
# ==============================================================================
def create_doc_7():
    doc = docx.Document()
    setup_page(doc)
    
    make_header_block(
        doc,
        ["TRƯỜNG THCS TRẦN PHÚ", "TỔ TOÁN – TIN"],
        "Lưu hành nội bộ",
        "Xuân Đông, ngày 22 tháng 10 năm 2026"
    )
    
    add_p(doc, "TÀI LIỆU HƯỚNG DẪN TRỌNG TÂM & NHỮNG ĐIỂM CỐT TỬ CẦN CHÚ Ý", bold=True, size=15, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "DÀNH RIÊNG CHO TỔ TRƯỞNG CHUYÊN MÔN HOÀNG TẤN THIÊN", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "(Bộ hồ sơ Sinh hoạt chuyên môn theo Nghiên cứu bài học - Môn Toán 8)", italic=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    
    add_callout(
        doc,
        "Thầy Hoàng Tấn Thiên thân mến! Đây là tệp tài liệu tổng hợp toàn bộ các lưu ý pháp lý, kỹ năng điều hành sư phạm, cốt tử chuyên môn và quy trình đóng gói hồ sơ chuẩn nhất. Tệp đã được đồng bộ chuẩn xác với Phân phối chương trình Phụ lục 3 môn Toán 8: Bài 15 gồm 3 tiết (Tiết 16, 17, 18), thực hiện trong Tuần 8 và Tuần 9 (rơi vào thời điểm Cuối tháng 10 và Đầu tháng 11 năm 2026). Thầy hãy đọc kỹ trước khi ký duyệt hoặc đón đoàn kiểm tra.",
        title="LỜI DẶN DÀNH CHO TỔ TRƯỞNG (ĐỒNG BỘ TUẦN 8, 9):",
        border_color="2563EB",
        bg_color="EFF6FF"
    )
    
    add_p(doc, "I. CĂN CỨ PHÁP LÝ & HỒ SƠ KIỂM TRA CHUYÊN MÔN CỦA ĐOÀN THANH TRA", bold=True, size=13)
    add_p(doc, "1. Bốn văn bản pháp quy bắt buộc phải trích dẫn chính xác:")
    add_p(doc, "- Công văn số 5555/BGDĐT-GDTrH ngày 08/10/2014 của Bộ GD&ĐT: Văn bản gốc quy định chuẩn mực về Sinh hoạt chuyên môn theo nghiên cứu bài học và 4 tiêu chí đánh giá hoạt động học của học sinh.")
    add_p(doc, "- Công văn số 5512/BGDĐT-GDTrH ngày 18/12/2020 của Bộ GD&ĐT: Hướng dẫn xây dựng Kế hoạch bài dạy chuẩn 4 hoạt động, bảng 2 cột GV-HS và phụ lục kế hoạch giáo dục.")
    add_p(doc, "- Thông tư số 32/2018/TT-BGDĐT ngày 26/12/2018 của Bộ GD&ĐT: Chương trình giáo dục phổ thông 2018 môn Toán.")
    add_p(doc, "- Thông tư số 20/2018/TT-BGDĐT: Quy định chuẩn nghề nghiệp giáo viên cơ sở giáo dục phổ thông (Tiêu chí 4: Phát triển chuyên môn bản thân và hỗ trợ đồng nghiệp).")
    add_p(doc, "2. Cấu trúc đóng tập hồ sơ lưu trữ tại Tổ chuyên môn:")
    add_p(doc, "Một bộ hồ sơ NCBH hoàn chỉnh khi đón đoàn kiểm tra của Phòng GD&ĐT hoặc Sở GD&ĐT bắt buộc phải có đủ 6 tệp thành phần kẹp chung trong 1 cặp hồ sơ chuyên đề (được đánh số thứ tự từ NCBH_01 đến NCBH_06):")
    add_p(doc, "  + Tệp 1: Kế hoạch tổ chức chuyên đề (có chữ ký duyệt của Hiệu trưởng, đóng dấu tròn nhà trường).")
    add_p(doc, "  + Tệp 2: Biên bản họp tổ Bước 1 (xây dựng bài dạy, phân tích rào cản nhận thức).")
    add_p(doc, "  + Tệp 3: Kế hoạch bài dạy minh họa hoàn chỉnh 3 tiết (có chữ ký của Thầy Hải, Cô Bình và Thầy Thiên).")
    add_p(doc, "  + Tệp 4: Các Phiếu quan sát tiết dạy của tất cả các giáo viên tham gia dự giờ (tối thiểu 5 phiếu có bút tích ghi chép thực tế).")
    add_p(doc, "  + Tệp 5: Biên bản họp tổ Bước 3 (thảo luận, suy ngẫm, chia sẻ minh chứng sau dự giờ).")
    add_p(doc, "  + Tệp 6: Báo cáo tổng kết và kế hoạch vận dụng Bước 4 (có phê duyệt của Ban Giám hiệu).")
    
    add_p(doc, "II. NGUYÊN TẮC VÀNG VỀ TÂM LÝ & NGHỆ THUẬT ĐIỀU HÀNH BƯỚC 3", bold=True, size=13)
    add_p(doc, "1. Nguyên tắc sống còn: TUYỆT ĐỐI KHÔNG ĐÁNH GIÁ, KHÔNG XẾP LOẠI GIÁO VIÊN DẠY!")
    add_p(doc, "- Nhiều trường học thất bại khi làm Nghiên cứu bài học vì biến buổi họp Bước 3 thành cuộc 'mổ xẻ, đấu tố' hoặc soi mói tác phong giáo viên. Điều này khiến giáo viên dạy minh họa sợ hãi, e dè, dẫn đến việc dạy 'diễn' hoặc từ chối dạy minh họa.")
    add_p(doc, "- Mục tiêu duy nhất của nghiên cứu bài học là: 'Cùng nhau tìm hiểu xem HỌC SINH HỌC NHƯ THẾ NÀO để cùng nhau dạy tốt hơn'.")
    add_p(doc, "2. Kỹ năng 'Bẻ lái sư phạm' dành cho Tổ trưởng Hoàng Tấn Thiên:")
    add_p(doc, "- Nếu trong buổi họp, có giáo viên quen lối mòn nhận xét: 'Thầy Hải đứng che bảng làm học sinh không thấy', 'Thầy Hải phân bố thời gian chưa chuẩn', Thầy Thiên cần mỉm cười và khéo léo bẻ lái sang học sinh:")
    add_p(doc, "  -> 'Cảm ơn ý kiến của thầy Danh. Vậy khi thầy Hải đứng ở vị trí đó, học sinh ở nhóm góc bàn có phản ứng thế nào? Các em có nhìn thấy hình không và chúng ta có cách nào bố trí máy chiếu hay bảng phụ để hỗ trợ các em tốt hơn?'.")
    add_p(doc, "- Luôn luôn khích lệ, bảo vệ và ghi nhận sự dũng cảm cống hiến của người dạy minh họa (thầy Trần Long Hải).")
    
    add_p(doc, "III. ĐIỂM CỐT TỬ VỀ CHUYÊN MÔN TOÁN 8 (BÀI 15: ĐỊNH LÍ THALÈS - 3 TIẾT)", bold=True, size=13)
    add_p(doc, "1. Phân bổ mạch kiến thức chuẩn xác theo Phụ lục 3:")
    add_p(doc, "- Tiết 16 (Tuần 8, Cuối tháng 10): Định lí Thalès thuận trong tam giác. Chỉ có các tỉ số trên hai cạnh bị cắt: AB'/AB = AC'/AC; AB'/B'B = AC'/C'C; B'B/AB = C'C/AC.")
    add_p(doc, "- CẢNH BÁO ĐỎ: Tuyệt đối KHÔNG đưa tỉ số cạnh đáy song song B'C'/BC vào Tiết 16 này! Tỉ số B'C'/BC thuộc về 'HỆ QUẢ CỦA ĐỊNH LÍ THALÈS' (học ở bài tiếp theo).")
    add_p(doc, "- Tiết 17 (Tuần 8/9): Định lí Thalès đảo trong tam giác. Nhận biết và chứng minh hai đường thẳng song song.")
    add_p(doc, "- Tiết 18 (Tuần 9, Đầu tháng 11): Luyện tập & Hoạt động thực hành STEM đo bóng nắng ngoài trời.")
    add_p(doc, "2. Lỗi học sinh lớp 8 hay mắc phải nhất cần dặn dò giáo viên dự giờ quan sát:")
    add_p(doc, "- Lỗi quên đổi đơn vị đo: Đoạn thẳng AB tính bằng cm, đoạn thẳng CD tính bằng dm mà lập ngay tỉ số.")
    add_p(doc, "- Lỗi đảo chiều tỉ số: Viết đoạn trên chia đoạn dưới bằng đoạn dưới chia đoạn trên (AB'/B'B = C'C/AC').")
    
    add_p(doc, "IV. HƯỚNG DẪN IN ẤN, KÝ DUYỆT VÀ ĐÓNG TẬP HỒ SƠ", bold=True, size=13)
    add_p(doc, "- Định dạng in ấn: Toàn bộ 6 tệp văn bản đã được thiết lập đúng chuẩn phông Times New Roman 13pt đứng, khổ giấy A4, căn lề chuẩn Nghị định 30/2020/NĐ-CP (Trái 30mm, Phải 15mm, Trên 20mm, Dưới 20mm), bảng biểu đóng khung 4 cạnh kín đáo.")
    add_p(doc, "- Thứ tự đóng tập:")
    add_p(doc, "  1. Trang bìa chuyên đề;")
    add_p(doc, "  2. Tệp NCBH_01 (Kế hoạch chuyên đề);")
    add_p(doc, "  3. Tệp NCBH_02 (Biên bản Bước 1);")
    add_p(doc, "  4. Tệp NCBH_03 (Kế hoạch bài dạy minh họa 3 tiết);")
    add_p(doc, "  5. Tệp NCBH_04 (Các Phiếu quan sát tiết dạy);")
    add_p(doc, "  6. Tệp NCBH_05 (Biên bản Bước 3);")
    add_p(doc, "  7. Tệp NCBH_06 (Báo cáo tổng kết Bước 4).")
    add_p(doc, "- Đóng gáy xoắn lò xo hoặc kẹp bìa còng xanh lưu tại tủ hồ sơ Tổ chuyên môn.")
    
    add_p(doc, "V. HƯỚNG DẪN ĐÓNG GÓI, GỬI EMAIL VÀ AN TOÀN HỆ THỐNG", bold=True, size=13)
    add_p(doc, "1. Tệp đóng gói ZIP:")
    add_p(doc, "- Toàn bộ 7 file hồ sơ Word (.docx), các file Markdown (.md) và hình ảnh đồ họa độ nét cao đã được tự động nén gọn trong tệp: Bo_Ho_So_NCBH_Dinh_Ly_Thales_Lop_8.zip đặt tại thư mục gốc.")
    add_p(doc, "2. Gửi thư điện tử qua email hoangthiencm@gmail.com:")
    add_p(doc, "- Thầy mở trình duyệt hoặc ứng dụng thư điện tử, đính kèm tệp Bo_Ho_So_NCBH_Dinh_Ly_Thales_Lop_8.zip và gửi đến địa chỉ hoangthiencm@gmail.com để lưu trữ đám mây an toàn.")
    add_p(doc, "3. Lưu ý an toàn về việc tắt máy tính:")
    add_p(doc, "- Để đảm bảo an toàn tuyệt đối, tránh làm mất dữ liệu chưa lưu của các ứng dụng khác đang mở trên máy tính và bảo toàn phiên kết nối làm việc, hệ thống không tự ý ép buộc tắt máy đột ngột.")
    add_p(doc, "- Hệ thống đã tạo sẵn tệp thực thi Tat_May.bat tại thư mục làm việc. Khi Thầy đã kiểm tra xong toàn bộ hồ sơ và muốn tắt máy, Thầy chỉ cần nhấp đúp chuột vào tệp Tat_May.bat để máy tính tự động hẹn giờ tắt an toàn!")
    
    add_p(doc, "", space_after=10)
    add_signatures(
        doc,
        "TỔ TRƯỞNG CHUYÊN MÔN",
        "Hoàng Tấn Thiên",
        "TRỢ LÝ SƯ PHẠM HOÀNG THIÊN",
        "Antigravity AI Assistant",
        left_sub="(Ký và lưu hành nội bộ)",
        right_sub="(Đồng hành & Hỗ trợ chuyên môn)"
    )
    
    out_file = os.path.join(OUTPUT_DIR, "NCBH_Chu_Y.docx")
    doc.save(out_file)
    print("XUẤT THÀNH CÔNG:", out_file)

if __name__ == "__main__":
    create_doc_4()
    create_doc_5()
    create_doc_6()
    create_doc_7()
    print("HOÀN THÀNH CẬP NHẬT 4 FILE CÒN LẠI THEO TUẦN 8, 9!")
