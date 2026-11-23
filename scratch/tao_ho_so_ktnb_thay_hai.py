# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

COLOR_BLACK = RGBColor(0, 0, 0)
COLOR_RED = RGBColor(220, 20, 20)  # Đỏ nổi bật cho nội dung cần lưu ý / chờ rà soát

def create_base_document():
    doc = docx.Document()
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.79)     # 20 mm
        section.bottom_margin = Inches(0.79)  # 20 mm
        section.left_margin = Inches(1.18)    # 30 mm
        section.right_margin = Inches(0.59)   # 15 mm
        section.header_distance = Inches(0.5)
        section.footer_distance = Inches(0.5)
        
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = COLOR_BLACK
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_before = Pt(2)
    normal_style.paragraph_format.space_after = Pt(2)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal_style.paragraph_format.first_line_indent = Inches(0)
    return doc

def set_table_no_borders(table):
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.first_line_indent = Inches(0)
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def set_cell_margins_zero(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m in ['top', 'bottom', 'left', 'right']:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), '0')
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_p(doc, runs_data, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=2, line_spacing=1.2):
    """
    Thêm đoạn văn hoàn chỉnh. TUYỆT ĐỐI KHÔNG DÙNG \\n TRONG RUN ĐỂ TRÁNH LỖI KÉO DÃN TỪ CỦA WORD!
    runs_data: list of tuples (text, is_bold, is_italic, color, font_size)
    """
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.first_line_indent = Inches(indent)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    
    for item in runs_data:
        text = item[0]
        bold = item[1] if len(item) > 1 else False
        italic = item[2] if len(item) > 2 else False
        color = item[3] if len(item) > 3 else COLOR_BLACK
        size = item[4] if len(item) > 4 else Pt(13)
        
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = size
        run.font.color.rgb = color
    return p

def create_mau_04():
    doc = create_base_document()
    
    # 1. Tiêu ngữ mẫu phía trên cùng (Căn giữa đúng chuẩn CV 4794)
    add_p(doc, [("Mẫu số 04", True, True, COLOR_BLACK, Pt(12))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=1, line_spacing=1.1)
    add_p(doc, [("(Kèm theo Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026", False, True, COLOR_BLACK, Pt(11.5))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=0, line_spacing=1.1)
    add_p(doc, [("của Sở Giáo dục và Đào tạo thành phố Đồng Nai)", False, True, COLOR_BLACK, Pt(11.5))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=6, line_spacing=1.1)
    
    # 2. Header 2 cột không viền
    tbl_hdr = doc.add_table(rows=1, cols=2)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(tbl_hdr)
    
    c_left = tbl_hdr.cell(0, 0)
    c_right = tbl_hdr.cell(0, 1)
    c_left.width = Inches(2.4)
    c_right.width = Inches(4.1)
    set_cell_margins_zero(c_left)
    set_cell_margins_zero(c_right)
    
    # Cột trái (Đúng mẫu 04: TRƯỜNG THCS TRẦN PHÚ / gạch ngang / Tổ kiểm tra theo Quyết định số...)
    p_l1 = c_left.paragraphs[0]
    p_l1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l1.paragraph_format.first_line_indent = Inches(0)
    p_l1.paragraph_format.line_spacing = 1.15
    p_l1.paragraph_format.space_before = Pt(0)
    p_l1.paragraph_format.space_after = Pt(2)
    r = p_l1.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12.0)
    r_line = p_l1.add_run("──────────\n")
    r_line.font.name = 'Times New Roman'
    r_line.font.size = Pt(8.0)
    r2 = p_l1.add_run("Tổ kiểm tra theo Quyết định\nsố ")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12.0)
    r3 = p_l1.add_run("18/QĐ-THCS.TP")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(12.0)
    r3.font.color.rgb = COLOR_RED
    
    # Cột phải
    p_r1 = c_right.paragraphs[0]
    p_r1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r1.paragraph_format.first_line_indent = Inches(0)
    p_r1.paragraph_format.line_spacing = 1.15
    p_r1.paragraph_format.space_before = Pt(0)
    p_r1.paragraph_format.space_after = Pt(2)
    
    run_qh = p_r1.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    run_qh.bold = True
    run_qh.font.name = 'Times New Roman'
    run_qh.font.size = Pt(11.5)
    
    run_tn = p_r1.add_run("Độc lập - Tự do - Hạnh phúc\n")
    run_tn.bold = True
    run_tn.font.name = 'Times New Roman'
    run_tn.font.size = Pt(12.0)
    
    run_ln = p_r1.add_run("──────────────\n")
    run_ln.font.name = 'Times New Roman'
    run_ln.font.size = Pt(8.0)
    
    run_ng = p_r1.add_run("Xuân Đông, ngày 23 tháng 11 năm 2026")
    run_ng.italic = True
    run_ng.font.name = 'Times New Roman'
    run_ng.font.size = Pt(12.0)
    
    # 3. Tiêu đề chính
    add_p(doc, [("BIÊN BẢN KIỂM TRA", True, False, COLOR_BLACK, Pt(14))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=8, space_after=2, line_spacing=1.15)
    add_p(doc, [("Về việc kiểm tra chuyên đề đối với giáo viên môn Toán lớp 8", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=2, line_spacing=1.15)
    add_p(doc, [("──────────────", False, False, COLOR_BLACK, Pt(9))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=6, line_spacing=1.0)
    
    # 4. Căn cứ & mở đầu (Đúng cấu trúc Mẫu 04)
    add_p(doc, [
        ("Căn cứ Quyết định số ", False, False, COLOR_BLACK, Pt(13)),
        ("18/QĐ-THCS.TP", False, False, COLOR_RED, Pt(13)),
        (" ngày ", False, False, COLOR_BLACK, Pt(13)),
        ("15/11/2026", False, False, COLOR_RED, Pt(13)),
        (" của Hiệu trưởng Trường THCS Trần Phú về việc kiểm tra chuyên đề chuyên môn năm học 2026 - 2027; vào ngày 23 tháng 11 năm 2026,", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=2)
    
    add_p(doc, [
        ("Tổ kiểm tra đã tiến hành thu thập thông tin, tài liệu, minh chứng và kiểm tra trực tiếp tại Tổ Toán – Tin học về việc đổi mới phương pháp dạy học, xây dựng Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH và ứng dụng công nghệ thông tin trong môn Toán lớp 8.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=2)
    
    add_p(doc, [
        ("Sau đây là kết quả kiểm tra:", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=4)
    
    # 5. I. THÀNH PHẦN LÀM VIỆC (Đúng nguyên văn Mẫu 04)
    add_p(doc, [("I. THÀNH PHẦN LÀM VIỆC", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    
    add_p(doc, [("1. Đại diện Tổ kiểm tra", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [
        ("- Ông: ", False, False, COLOR_BLACK, Pt(13)),
        ("Hoàng Tấn Thiên", True, False, COLOR_BLACK, Pt(13)),
        (" – chức vụ: Tổ trưởng chuyên môn Tổ Toán – Tin học (Tổ trưởng Tổ kiểm tra).", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [
        ("- Ông: ", False, False, COLOR_BLACK, Pt(13)),
        ("Hồ Đăng Danh", True, False, COLOR_BLACK, Pt(13)),
        (" – chức vụ: Giáo viên môn Tin học (Thành viên).", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [
        ("- Bà: ", False, False, COLOR_BLACK, Pt(13)),
        ("Lê Thị Bình", True, False, COLOR_BLACK, Pt(13)),
        (" – chức vụ: Giáo viên môn Toán (Người ghi biên bản).", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=3)
    
    add_p(doc, [("2. Đã tiến hành kiểm tra đối với: ", True, False, COLOR_BLACK, Pt(13)),
                ("Ông Trần Long Hải, gồm:", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [
        ("- Ông: ", False, False, COLOR_BLACK, Pt(13)),
        ("Trần Long Hải", True, False, COLOR_BLACK, Pt(13)),
        (" – chức vụ: Giáo viên giảng dạy môn Toán khối 8, Tổ Toán – Tin học Trường THCS Trần Phú.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=3)
    
    add_p(doc, [("3. Người chứng kiến (nếu có):", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [
        ("- Ông: ", False, False, COLOR_BLACK, Pt(13)),
        ("Đinh Văn Đông", True, False, COLOR_BLACK, Pt(13)),
        (" – chức vụ: Phó Hiệu trưởng Trường THCS Trần Phú.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [
        ("- Ông: ", False, False, COLOR_BLACK, Pt(13)),
        ("Hoàng Xuân Ánh", True, False, COLOR_BLACK, Pt(13)),
        (" – chức vụ: Giáo viên môn Toán.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 6. II. NỘI DUNG KIỂM TRA (Đúng nguyên văn Mẫu 04)
    add_p(doc, [("II. NỘI DUNG KIỂM TRA", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    
    add_p(doc, [("1. Kiểm tra cấu trúc Kế hoạch bài dạy (KHBD) theo quy định tại Công văn 5512/BGDĐT-GDTrH đối với Bài 9: Phân tích đa thức thành nhân tử (3 tiết) – Tiết 24, Tuần 12, Toán 8 (Bộ sách Kết nối tri thức với cuộc sống).", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("2. Kiểm tra chuỗi 4 hoạt động học tập (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng): Việc chuyển giao nhiệm vụ học tập, tổ chức cho học sinh hoạt động nhóm bảng phụ, hệ thống bài tập thực hành và câu hỏi củng cố.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("3. Kiểm tra việc thực hiện tích hợp Khung Năng lực số (đối chiếu Phụ lục 3 môn Toán 8; không áp dụng Khung AI do không bắt buộc), đánh giá mức độ ứng dụng CNTT, học liệu số và tiến độ đưa bài, ký số trên CSDL ngành (truong.dongnai.edu.vn).", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 7. III. ĐÁNH GIÁ CHUNG (Đúng nguyên văn Mẫu 04)
    add_p(doc, [("III. ĐÁNH GIÁ CHUNG", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    
    # 1. Ưu điểm
    add_p(doc, [("1. Ưu điểm", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [
        ("- Về cấu trúc và mục tiêu bài dạy: ", True, False, COLOR_BLACK, Pt(13)),
        ("Kế hoạch bài dạy Bài 9 (Tiết 24, Tuần 12) được xây dựng đúng quy chuẩn cấu trúc Công văn 5512/BGDĐT-GDTrH. Mục tiêu bài học xác định rõ ràng yêu cầu cần đạt: Học sinh nhận biết và vận dụng thành thạo 3 phương pháp phân tích đa thức thành nhân tử (đặt nhân tử chung, dùng hằng đẳng thức, nhóm hạng tử). Chú trọng phát triển các năng lực toán học cốt lõi: năng lực tư duy và lập luận toán học, mô hình hóa toán học, giao tiếp toán học và giải quyết vấn đề toán học.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("- Về thiết bị và học liệu dạy học: ", True, False, COLOR_BLACK, Pt(13)),
        ("Chuẩn bị công phu, chu đáo; kết hợp hài hòa giữa SGK, giáo án điện tử PPT, phiếu học tập, bảng phụ nhóm và video âm nhạc sinh động.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("- Về đổi mới phương pháp tổ chức hoạt động và ứng dụng CNTT: ", True, False, COLOR_BLACK, Pt(13)),
        ("Hoạt động khởi động sáng tạo, hấp dẫn khi lồng ghép video bài hát “Hello Song” vận động đầu giờ (3 phút) giúp học sinh giải tỏa áp lực, sau đó khéo léo kết nối với tình huống bài toán thực tế của nhân vật Vuông và Tròn (4 phút) để gợi mở kiến thức mới. Hoạt động hình thành kiến thức (Tiết 1: Đặt nhân tử chung) được bố cục theo bảng 2 cột đối chiếu rõ nét giữa Hoạt động của GV và Sản phẩm của HS; tổ chức hiệu quả hoạt động nhóm với bảng phụ ở phần Luyện tập 1. Hoạt động luyện tập được số hóa sinh động qua trò chơi tương tác “Ai là triệu phú” với 5 câu hỏi trắc nghiệm có quyền trợ giúp, kích thích tối đa sự hứng thú và thi đua học tập của học sinh.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("- Về việc tích hợp và tiến độ chuyên môn: ", True, False, COLOR_BLACK, Pt(13)),
        ("Bài 9 trong Phụ lục 3 môn Toán 8 không thuộc diện bắt buộc tích hợp Khung năng lực số; giáo viên đã chủ động khai thác hiệu quả công nghệ thông tin (video, slide trình chiếu, trò chơi tương tác số hóa) phục vụ đắc lực cho bài học. Tiến độ giảng dạy đảm bảo khớp 100% phân phối chương trình môn Toán 8 học kỳ I năm học 2026 - 2027.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 2. Tồn tại (Góp ý nhẹ nhàng)
    add_p(doc, [("2. Tồn tại", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=3, space_after=2)
    add_p(doc, [
        ("- Về cách trình bày bảng 2 cột: ", True, False, COLOR_BLACK, Pt(13)),
        ("Ở phần tổ chức thực hiện của Hoạt động hình thành kiến thức, các hoạt động nhỏ (HĐ1, Ví dụ 1, Bài tập phụ, Luyện tập 1, Vận dụng 1) nếu được phân tách thành từng dòng riêng biệt trong bảng và ghi chú thêm thời lượng dự kiến thì tiến trình bài soạn sẽ càng trực quan, rõ ràng và thuận tiện hơn khi theo dõi.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("- Về rà soát kỹ thuật văn bản: ", True, False, COLOR_BLACK, Pt(13)),
        ("Trong lời dẫn tình huống mở đầu, giáo viên rà soát bổ sung biểu thức toán học còn khuyết (đoạn ", False, False, COLOR_BLACK, Pt(13)),
        ("“...tìm được tất cả số x để biểu thức . Vuông nghe vậy...”", False, True, COLOR_RED, Pt(13)),
        (") để bài soạn được hoàn chỉnh và chuẩn mực hơn.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("- Về hồ sơ CSDL ngành: ", True, False, COLOR_BLACK, Pt(13)),
        ("Tiếp tục duy trì và hoàn tất việc ký số điện tử trên hệ thống truong.dongnai.edu.vn đúng tuần quy định.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 3. Nguyên nhân
    add_p(doc, [("3. Nguyên nhân", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=3, space_after=2)
    add_p(doc, [
        ("- Khách quan: ", True, False, COLOR_BLACK, Pt(13)),
        ("Nội dung bài học có nhiều dạng bài tập biến đổi đại số; giáo viên đã dành nhiều tâm huyết và thời gian để đầu tư thiết kế bài giảng điện tử và trò chơi tương tác sinh động cho học sinh.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("- Chủ quan: ", True, False, COLOR_BLACK, Pt(13)),
        ("Trong quá trình biên tập và chuyển đổi tệp văn bản, còn một vài sơ suất nhỏ về khâu định dạng chưa kịp hoàn thiện trước buổi kiểm tra.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 8. IV. Kiến nghị của Tổ kiểm tra (Đúng nguyên văn Mẫu 04)
    add_p(doc, [("IV. Kiến nghị của Tổ kiểm tra ", True, False, COLOR_BLACK, Pt(13)),
                ("(Đối với cá nhân, tổ chuyên môn, nhà trường, cấp trên)", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    add_p(doc, [("1. Đối với giáo viên Trần Long Hải:", True, True, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [("- Tiếp tục phát huy thế mạnh về phương pháp dạy học tích cực, tổ chức trò chơi học tập tạo không khí hào hứng cho học sinh trong các tiết dạy tiếp theo.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [("- Rà soát, chỉnh sửa nhẹ nhàng các điểm định dạng như đã góp ý để bài soạn thêm hoàn chỉnh; hoàn thành cập nhật ký số trên CSDL ngành trước ngày ", False, False, COLOR_BLACK, Pt(13)),
                ("28/11/2026", True, False, COLOR_RED, Pt(13)), (".", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    
    add_p(doc, [("2. Đối với Tổ chuyên môn Toán – Tin học:", True, True, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [("- Tổ chức trao đổi, nhân rộng kinh nghiệm thiết kế hoạt động khởi động sinh động và trò chơi học tập tương tác của Thầy Hải trong buổi sinh hoạt chuyên môn toàn tổ.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [("- Hỗ trợ, theo dõi việc cập nhật ký số bài giảng của giáo viên trên hệ thống quản lý.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 9. V. Ý kiến của bộ phận (người) được kiểm tra: (Đúng nguyên văn Mẫu 04)
    add_p(doc, [("V. Ý kiến của bộ phận (người) được kiểm tra:", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    add_p(doc, [
        ("Tôi hoàn toàn nhất trí với toàn bộ nhận xét, đánh giá khách quan của Tổ kiểm tra. Tôi xin tiếp thu các ý kiến góp ý mang tính xây dựng để bài soạn được hoàn thiện hơn, cam kết sẽ rà soát lại công thức toán học, căn chỉnh bảng 2 cột và hoàn thành ký số đúng thời hạn được giao.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=4)
    
    # 10. Đoạn kết (Đúng nguyên văn Mẫu 04 - có Biên bản gồm ... trang)
    add_p(doc, [
        ("Việc kiểm tra kết thúc vào lúc ", False, False, COLOR_BLACK, Pt(13)),
        ("10 giờ 30 phút", False, False, COLOR_RED, Pt(13)),
        (" ngày 23 tháng 11 năm 2026 và được lập thành biên bản. Biên bản gồm ", False, False, COLOR_BLACK, Pt(13)),
        ("02", False, False, COLOR_RED, Pt(13)),
        (" trang.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=4, space_after=2)
    
    add_p(doc, [
        ("Biên bản này đã được đọc lại cho những người có tên nêu trên cùng nghe và đồng ý ký xác nhận; biên bản được lập thành 02 bản có giá trị như nhau, mỗi bên giữ 01 bản./.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=10)
    
    # 11. Bảng Chữ ký 3 bên (Đúng chữ thường in đậm như Mẫu 04)
    tbl_sig = doc.add_table(rows=1, cols=3)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(tbl_sig)
    
    c1 = tbl_sig.cell(0, 0)
    c2 = tbl_sig.cell(0, 1)
    c3 = tbl_sig.cell(0, 2)
    c1.width = Inches(2.1)
    c2.width = Inches(2.3)
    c3.width = Inches(2.1)
    set_cell_margins_zero(c1)
    set_cell_margins_zero(c2)
    set_cell_margins_zero(c3)
    
    def fill_sig_cell(cell, title, role, name):
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        
        r1 = p.add_run(f"{title}\n")
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12.0)
        
        r2 = p.add_run(f"{role}\n\n\n\n\n")
        r2.italic = True
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11.5)
        
        r3 = p.add_run(name)
        r3.bold = True
        r3.font.name = 'Times New Roman'
        r3.font.size = Pt(12.5)
        
    fill_sig_cell(c1, "Người được kiểm tra", "(Ký và ghi rõ họ tên)", "Trần Long Hải")
    fill_sig_cell(c2, "Tổ trưởng Tổ kiểm tra", "(Ký và ghi rõ họ tên)", "Hoàng Tấn Thiên")
    fill_sig_cell(c3, "Người ghi biên bản", "(Ký và ghi rõ họ tên)", "Lê Thị Bình")
    
    return doc

def create_mau_05():
    doc = create_base_document()
    
    # 1. Tiêu ngữ mẫu phía trên cùng (Căn giữa đúng nguyên văn Mẫu số 05)
    add_p(doc, [("Mẫu số 05", True, True, COLOR_BLACK, Pt(12))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=1, line_spacing=1.1)
    add_p(doc, [("(Kèm theo Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026", False, True, COLOR_BLACK, Pt(11.5))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=0, line_spacing=1.1)
    add_p(doc, [("của Sở Giáo dục và Đào tạo thành phố Đồng Nai)", False, True, COLOR_BLACK, Pt(11.5))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=6, line_spacing=1.1)
    
    # 2. Header 2 cột không viền
    tbl_hdr = doc.add_table(rows=1, cols=2)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(tbl_hdr)
    
    c_left = tbl_hdr.cell(0, 0)
    c_right = tbl_hdr.cell(0, 1)
    c_left.width = Inches(2.4)
    c_right.width = Inches(4.1)
    set_cell_margins_zero(c_left)
    set_cell_margins_zero(c_right)
    
    # Cột trái (Đúng mẫu: TRƯỜNG THCS TRẦN PHÚ / Tổ kiểm tra theo Quyết định số...)
    p_l1 = c_left.paragraphs[0]
    p_l1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l1.paragraph_format.first_line_indent = Inches(0)
    p_l1.paragraph_format.line_spacing = 1.15
    p_l1.paragraph_format.space_before = Pt(0)
    p_l1.paragraph_format.space_after = Pt(2)
    r = p_l1.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r.bold = True
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12.0)
    r_line = p_l1.add_run("──────────\n")
    r_line.font.name = 'Times New Roman'
    r_line.font.size = Pt(8.0)
    r2 = p_l1.add_run("Tổ kiểm tra theo Quyết định\nsố ")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12.0)
    r3 = p_l1.add_run("18/QĐ-THCS.TP")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(12.0)
    r3.font.color.rgb = COLOR_RED
    
    # Cột phải
    p_r1 = c_right.paragraphs[0]
    p_r1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r1.paragraph_format.first_line_indent = Inches(0)
    p_r1.paragraph_format.line_spacing = 1.15
    p_r1.paragraph_format.space_before = Pt(0)
    p_r1.paragraph_format.space_after = Pt(2)
    
    run_qh = p_r1.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    run_qh.bold = True
    run_qh.font.name = 'Times New Roman'
    run_qh.font.size = Pt(11.5)
    
    run_tn = p_r1.add_run("Độc lập - Tự do - Hạnh phúc\n")
    run_tn.bold = True
    run_tn.font.name = 'Times New Roman'
    run_tn.font.size = Pt(12.0)
    
    run_ln = p_r1.add_run("──────────────\n")
    run_ln.font.name = 'Times New Roman'
    run_ln.font.size = Pt(8.0)
    
    run_ng = p_r1.add_run("Xuân Đông, ngày 23 tháng 11 năm 2026")
    run_ng.italic = True
    run_ng.font.name = 'Times New Roman'
    run_ng.font.size = Pt(12.0)
    
    # 3. Tiêu đề chính (Đúng nguyên văn Mẫu số 05 - Không có dòng Kính gửi)
    add_p(doc, [("BÁO CÁO", True, False, COLOR_BLACK, Pt(14))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=8, space_after=2, line_spacing=1.15)
    add_p(doc, [("Kết quả kiểm tra chuyên đề về việc đổi mới phương pháp dạy học,", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=1, line_spacing=1.15)
    add_p(doc, [("xây dựng Kế hoạch bài dạy và ứng dụng công nghệ thông tin môn Toán 8", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=1, line_spacing=1.15)
    add_p(doc, [("đối với giáo viên Trần Long Hải", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=2, line_spacing=1.15)
    add_p(doc, [("──────────────", False, False, COLOR_BLACK, Pt(9))], 
          align=WD_ALIGN_PARAGRAPH.CENTER, indent=0, space_before=0, space_after=6, line_spacing=1.0)
    
    # 4. Căn cứ & mở đầu (Đúng cấu trúc mẫu 05)
    add_p(doc, [
        ("Thực hiện Quyết định kiểm tra số ", False, False, COLOR_BLACK, Pt(13)),
        ("18/QĐ-THCS.TP", False, False, COLOR_RED, Pt(13)),
        (" ngày ", False, False, COLOR_BLACK, Pt(13)),
        ("15/11/2026", False, False, COLOR_RED, Pt(13)),
        (" của Hiệu trưởng Trường THCS Trần Phú về việc kiểm tra chuyên đề chuyên môn năm học 2026 - 2027; Tổ kiểm tra đã tiến hành kiểm tra tại Tổ Toán – Tin học đối với ông ", False, False, COLOR_BLACK, Pt(13)),
        ("Trần Long Hải", True, False, COLOR_BLACK, Pt(13)),
        (" – Giáo viên giảng dạy môn Toán khối 8.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=2)
    
    add_p(doc, [
        ("Quá trình kiểm tra, Tổ kiểm tra đã làm việc với ông Trần Long Hải (cùng sự chứng kiến của Phó Hiệu trưởng Đinh Văn Đông và giáo viên Hoàng Xuân Ánh) vào ngày 23 tháng 11 năm 2026 và tiến hành kiểm tra, xác minh trực tiếp các nội dung kiểm tra.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=2)
    
    add_p(doc, [("Sau đây là kết quả kiểm tra:", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=4)
    
    # 5. I. KHÁI QUÁT CHUNG
    add_p(doc, [("I. KHÁI QUÁT CHUNG", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    add_p(doc, [
        ("- Họ và tên giáo viên được kiểm tra: ", False, False, COLOR_BLACK, Pt(13)),
        ("Trần Long Hải", True, False, COLOR_BLACK, Pt(13)),
        (".", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Chức vụ chuyên môn: Giáo viên môn Toán; Tổ chuyên môn: Toán – Tin học.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Trình độ đào tạo: Đại học Sư phạm Toán học.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Phân công nhiệm vụ năm học 2026 - 2027: Giảng dạy môn Toán khối 8, tham gia đầy đủ các hoạt động chuyên môn, sinh hoạt tổ và các phong trào thi đua của nhà trường.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Ý thức tổ chức kỷ luật và nề nếp chuyên môn: Chấp hành tốt chủ trương, đường lối chính sách của Đảng và pháp luật của Nhà nước; thực hiện nghiêm túc quy chế chuyên môn, ngày giờ công đảm bảo, có tinh thần trách nhiệm và tích cực đổi mới phương pháp dạy học.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 6. II. KẾT QUẢ KIỂM TRA, XÁC MINH (Đúng nguyên văn tiêu đề Mẫu 05)
    add_p(doc, [("II. KẾT QUẢ KIỂM TRA, XÁC MINH", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    
    add_p(doc, [("1. Về tiến độ và tính pháp lý của hồ sơ bài dạy:", True, True, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [("- Giáo viên cung cấp đầy đủ Kế hoạch bài dạy theo phân phối chương trình: Bài 9: Phân tích đa thức thành nhân tử (3 tiết) – Tiết 24, Tuần 12, môn Toán 8 (Bộ sách Kết nối tri thức với cuộc sống).", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Tiến độ soạn giảng khớp hoàn toàn với Kế hoạch giáo dục môn học của Tổ chuyên môn và Phụ lục 3 của nhà trường.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=3)
    
    add_p(doc, [("2. Về chất lượng sư phạm và đổi mới phương pháp dạy học (Công văn 5512/BGDĐT-GDTrH):", True, True, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [("- Kế hoạch bài dạy được thiết kế chặt chẽ theo cấu trúc 3 phần chuẩn; mục tiêu phân định rõ ràng giữa yêu cầu cần đạt về kiến thức, các năng lực toán học đặc thù (tư duy lập luận, giao tiếp toán học, mô hình hóa toán học, giải quyết vấn đề) và phẩm chất học sinh.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Hoạt động Khởi động có sự đổi mới sáng tạo nổi bật: Sử dụng video âm nhạc “Hello Song” giải tỏa căng thẳng (3 phút) kết hợp đưa ra bài toán thực tế của Vuông và Tròn (4 phút) tạo tình huống có vấn đề dẫn dắt học sinh tiếp cận kiến thức phân tích đa thức thành nhân tử rất tự nhiên.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Hoạt động Hình thành kiến thức mới (Tiết 1: Đặt nhân tử chung) thể hiện theo bảng 2 cột rõ ràng; chú trọng hoạt động của học sinh, tổ chức thảo luận nhóm bảng phụ ở Luyện tập 1.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Hoạt động Luyện tập được thiết kế sáng tạo thông qua trò chơi trắc nghiệm tương tác “Ai là triệu phú” (5 câu hỏi phân hóa có quyền trợ giúp), giúp học sinh khắc sâu kiến thức trong không khí thi đua sôi nổi.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=3)
    
    add_p(doc, [("3. Về việc tích hợp Khung Năng lực số và ứng dụng CNTT:", True, True, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [("- Thực hiện đúng định hướng chuyên môn: Đối chiếu Phụ lục 3 môn Toán 8, Bài 9 không thuộc danh mục các tiết bắt buộc tích hợp Khung Năng lực số (và Khung AI không bắt buộc).", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Giáo viên đã thể hiện tinh thần chủ động ứng dụng công nghệ thông tin rất hiệu quả: khai thác video âm nhạc khởi động, trình chiếu Slide PowerPoint và số hóa trò chơi học tập trắc nghiệm, tạo sự hứng khởi lớn cho học sinh.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=1)
    add_p(doc, [("- Về góp ý hoàn thiện: Góp ý giáo viên phân tách các hoạt động nhỏ trong bảng 2 cột thành từng dòng riêng có ghi chú thời lượng dự kiến để bài dạy thêm trực quan; rà soát bổ sung biểu thức toán học còn khuyết trong tình huống mở đầu; tiếp tục duy trì ký số điện tử đều đặn trên hệ thống truong.dongnai.edu.vn.", False, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 7. III. KẾT LUẬN VỀ NHỮNG NỘI DUNG ĐÃ TIẾN HÀNH KIỂM TRA (Đúng nguyên văn Mẫu 05)
    add_p(doc, [("III. KẾT LUẬN VỀ NHỮNG NỘI DUNG ĐÃ TIẾN HÀNH KIỂM TRA", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    add_p(doc, [
        ("1. Đánh giá chung: ", True, False, COLOR_BLACK, Pt(13)),
        ("Kế hoạch bài dạy chuyên đề của Thầy Trần Long Hải được chuẩn bị chu đáo, có sự đầu tư công phu về đổi mới phương pháp dạy học, ứng dụng trò chơi tương tác và học liệu số sinh động, kích thích tinh thần tự học và hợp tác của học sinh, đáp ứng rất tốt tinh thần Chương trình GDPT 2018.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("2. Xếp loại hồ sơ Kế hoạch bài dạy chuyên đề: ", True, False, COLOR_BLACK, Pt(13)),
        ("LOẠI TỐT", True, False, COLOR_RED, Pt(13)),
        (".", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("3. Trách nhiệm: ", True, False, COLOR_BLACK, Pt(13)),
        ("Cá nhân giáo viên Trần Long Hải tiếp tục phát huy các ưu điểm về phương pháp dạy học và hoàn thiện các lưu ý kỹ thuật về bảng biểu và ký số theo quy định.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 8. IV. CÁC BIỆN PHÁP XỬ LÝ THEO THẨM QUYỀN ĐÃ ÁP DỤNG (NẾU CÓ) (Đúng nguyên văn Mẫu 05)
    add_p(doc, [("IV. CÁC BIỆN PHÁP XỬ LÝ THEO THẨM QUYỀN ĐÃ ÁP DỤNG (NẾU CÓ)", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    add_p(doc, [
        ("Không (Tổ kiểm tra chỉ trao đổi, góp ý nhẹ nhàng trực tiếp về kỹ thuật trình bày bảng 2 cột và nhắc nhở duy trì tiến độ ký số trên hệ thống CSDL ngành).", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=4)
    
    # 9. V. NHỮNG Ý KIẾN KHÁC NHAU GIỮA CÁC THÀNH VIÊN ĐOÀN KIỂM TRA (NẾU CÓ) (Đúng nguyên văn Mẫu 05)
    add_p(doc, [("V. NHỮNG Ý KIẾN KHÁC NHAU GIỮA CÁC THÀNH VIÊN ĐOÀN KIỂM TRA (NẾU CÓ)", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    add_p(doc, [
        ("Không (100% thành viên Tổ kiểm tra và đại diện Ban giám hiệu chứng kiến thống nhất với toàn bộ nội dung đánh giá và kết luận).", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=2, space_after=4)
    
    # 10. VI. KIẾN NGHỊ VÀ BIỆN PHÁP XỬ LÝ (Đúng nguyên văn Mẫu 05)
    add_p(doc, [("VI. KIẾN NGHỊ VÀ BIỆN PHÁP XỬ LÝ", True, False, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=6, space_after=2)
    add_p(doc, [("1. Đối với Hiệu trưởng Trường THCS Trần Phú:", True, True, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [
        ("- Đề nghị Hiệu trưởng xem xét ghi nhận kết quả kiểm tra chuyên đề đối với giáo viên Trần Long Hải; công nhận xếp loại hồ sơ Kế hoạch bài dạy chuyên đề: ", False, False, COLOR_BLACK, Pt(13)),
        ("Loại Tốt", True, False, COLOR_RED, Pt(13)),
        (".", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    add_p(doc, [
        ("- Biểu dương tinh thần tích cực đổi mới phương pháp dạy học, tổ chức trò chơi học tập tương tác của giáo viên để khích lệ phong trào chuyên môn chung trong nhà trường.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    
    add_p(doc, [("2. Đối với cá nhân giáo viên Trần Long Hải:", True, True, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [
        ("- Rà soát, căn chỉnh lại bảng 2 cột và hoàn tất việc ký số điện tử trên hệ thống CSDL ngành trước ngày ", False, False, COLOR_BLACK, Pt(13)),
        ("28/11/2026", True, False, COLOR_RED, Pt(13)),
        (".", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=2)
    
    add_p(doc, [("3. Đối với Tổ chuyên môn Toán – Tin học:", True, True, COLOR_BLACK, Pt(13))], 
          align=WD_ALIGN_PARAGRAPH.LEFT, indent=0.5, space_before=2, space_after=2)
    add_p(doc, [
        ("- Nhân rộng kinh nghiệm thiết kế hoạt động khởi động và trò chơi học tập tương tác của Thầy Hải trong toàn tổ; theo dõi việc hoàn thiện ký số của giáo viên.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=1, space_after=4)
    
    # 11. Đoạn kết (Đúng nguyên văn Mẫu 05)
    add_p(doc, [
        ("Trên đây là Báo cáo kết quả kiểm tra về chuyên đề đổi mới phương pháp dạy học, xây dựng Kế hoạch bài dạy và ứng dụng công nghệ thông tin môn Toán 8 đối với giáo viên Trần Long Hải, Tổ kiểm tra xin ý kiến chỉ đạo của Hiệu trưởng./.", False, False, COLOR_BLACK, Pt(13))
    ], align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=0.5, space_before=4, space_after=10)
    
    # 12. Bảng Chữ ký & Nơi nhận (1 hàng 2 cột không viền)
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(tbl_sig)
    
    c1 = tbl_sig.cell(0, 0)
    c2 = tbl_sig.cell(0, 1)
    c1.width = Inches(3.2)
    c2.width = Inches(3.3)
    set_cell_margins_zero(c1)
    set_cell_margins_zero(c2)
    
    # Cột trái: Nơi nhận
    p_c1 = c1.paragraphs[0]
    p_c1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_c1.paragraph_format.first_line_indent = Inches(0)
    p_c1.paragraph_format.space_before = Pt(0)
    p_c1.paragraph_format.space_after = Pt(0)
    p_c1.paragraph_format.line_spacing = 1.15
    
    r_nn = p_c1.add_run("Nơi nhận:\n")
    r_nn.bold = True
    r_nn.italic = True
    r_nn.font.name = 'Times New Roman'
    r_nn.font.size = Pt(11.0)
    
    lines_nn = [
        "- Hiệu trưởng (để b/c);\n",
        "- Phó Hiệu trưởng Đinh Văn Đông (để b/c);\n",
        "- Thầy Trần Long Hải (để th/h);\n",
        "- Lưu: Hồ sơ KTNB."
    ]
    for l in lines_nn:
        r_item = p_c1.add_run(l)
        r_item.font.name = 'Times New Roman'
        r_item.font.size = Pt(10.0)
        
    # Cột phải: Tổ trưởng
    p_c2 = c2.paragraphs[0]
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.first_line_indent = Inches(0)
    p_c2.paragraph_format.space_before = Pt(0)
    p_c2.paragraph_format.space_after = Pt(0)
    p_c2.paragraph_format.line_spacing = 1.15
    
    r_tt = p_c2.add_run("TỔ TRƯỞNG TỔ KIỂM TRA\n")
    r_tt.bold = True
    r_tt.font.name = 'Times New Roman'
    r_tt.font.size = Pt(12.0)
    
    r_ky = p_c2.add_run("(Ký và ghi rõ họ tên)\n\n\n\n\n")
    r_ky.italic = True
    r_ky.font.name = 'Times New Roman'
    r_ky.font.size = Pt(11.0)
    
    r_ten = p_c2.add_run("Hoàng Tấn Thiên")
    r_ten.bold = True
    r_ten.font.name = 'Times New Roman'
    r_ten.font.size = Pt(12.5)
    
    return doc

def save_docx_robust(doc, out_docx_path):
    p = Path(out_docx_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        doc.save(str(p))
        print(f"Saved: {p}")
        return str(p)
    except PermissionError:
        fallback = p.with_name(p.stem + "_Cap_Nhat" + p.suffix)
        doc.save(str(fallback))
        print(f"[THONG BAO] Tep {p.name} dang mo trong Word nen da luu vao: {fallback.name}")
        return str(fallback)

def main():
    out_dir = Path("TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/23.11")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    doc4 = create_mau_04()
    p4 = out_dir / "Bien_Ban_Kiem_Tra_Chuyen_De_Thay_Hai_Mau_04.docx"
    save_docx_robust(doc4, p4)
    
    doc5 = create_mau_05()
    p5 = out_dir / "Bao_Cao_Ket_Qua_Kiem_Tra_Chuyen_De_Thay_Hai_Mau_05.docx"
    save_docx_robust(doc5, p5)

if __name__ == "__main__":
    main()
