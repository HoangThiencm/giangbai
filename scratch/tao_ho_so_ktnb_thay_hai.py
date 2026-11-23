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
    normal_style.paragraph_format.first_line_indent = Inches(0.5)  # 1.27 cm
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

def add_paragraph_runs(p, runs_data):
    """
    runs_data: list of tuples: (text, is_bold, is_italic, color, font_size)
    """
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

def create_mau_04():
    doc = create_base_document()
    
    # 1. Tiêu ngữ mẫu phía trên cùng
    p_mau = doc.add_paragraph()
    p_mau.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mau.paragraph_format.first_line_indent = Inches(0)
    p_mau.paragraph_format.space_after = Pt(4)
    run1 = p_mau.add_run("Mẫu số 04\n")
    run1.bold = True
    run1.font.name = 'Times New Roman'
    run1.font.size = Pt(11.5)
    run2 = p_mau.add_run("(Kèm theo Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026 của Sở Giáo dục và Đào tạo thành phố Đồng Nai)")
    run2.italic = True
    run2.font.name = 'Times New Roman'
    run2.font.size = Pt(11)
    
    # 2. Header 2 cột không viền
    tbl_hdr = doc.add_table(rows=1, cols=2)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(tbl_hdr)
    
    cell_left = tbl_hdr.cell(0, 0)
    cell_right = tbl_hdr.cell(0, 1)
    cell_left.width = Inches(3.2)
    cell_right.width = Inches(3.8)
    
    # Cột trái
    p_l = cell_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.first_line_indent = Inches(0)
    p_l.paragraph_format.line_spacing = 1.15
    add_paragraph_runs(p_l, [
        ("TRƯỜNG THCS TRẦN PHÚ\n", True, False, COLOR_BLACK, Pt(12)),
        ("TỔ KIỂM TRA THEO QĐ SỐ ", True, False, COLOR_BLACK, Pt(11.5)),
        ("18", True, False, COLOR_RED, Pt(11.5)),
    ])
    
    # Cột phải
    p_r = cell_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.first_line_indent = Inches(0)
    p_r.paragraph_format.line_spacing = 1.15
    add_paragraph_runs(p_r, [
        ("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n", True, False, COLOR_BLACK, Pt(12)),
        ("Độc lập - Tự do - Hạnh phúc\n", True, False, COLOR_BLACK, Pt(12.5)),
        ("Xuân Đông, ngày 23 tháng 11 năm 2026", False, True, COLOR_BLACK, Pt(12)),
    ])
    
    # Khoảng cách
    p_space = doc.add_paragraph()
    p_space.paragraph_format.first_line_indent = Inches(0)
    p_space.paragraph_format.space_before = Pt(4)
    p_space.paragraph_format.space_after = Pt(2)
    
    # 3. Tiêu đề chính
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.first_line_indent = Inches(0)
    p_title.paragraph_format.space_after = Pt(2)
    add_paragraph_runs(p_title, [
        ("BIÊN BẢN KIỂM TRA\n", True, False, COLOR_BLACK, Pt(14)),
        ("Về việc kiểm tra chuyên đề đối với giáo viên môn Toán lớp 8", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 4. Căn cứ & mở đầu
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.first_line_indent = Inches(0.5)
    p_intro.paragraph_format.space_before = Pt(4)
    add_paragraph_runs(p_intro, [
        ("Căn cứ Quyết định số ", False, False, COLOR_BLACK, Pt(13)),
        ("18/QĐ-THCS.TP", False, False, COLOR_RED, Pt(13)),
        (" ngày ", False, False, COLOR_BLACK, Pt(13)),
        ("15 tháng 11 năm 2026", False, False, COLOR_RED, Pt(13)),
        (" của Hiệu trưởng Trường THCS Trần Phú về việc thành lập Tổ kiểm tra nội bộ chuyên đề chuyên môn năm học 2026 - 2027;\n", False, False, COLOR_BLACK, Pt(13)),
        ("Vào hồi 08 giờ 00 phút, ngày 23 tháng 11 năm 2026, tại Văn phòng Trường THCS Trần Phú, Tổ kiểm tra đã tiến hành thu thập thông tin, hồ sơ minh chứng và làm việc trực tiếp để kiểm tra chuyên đề đối với giáo viên môn Toán lớp 8.\n", False, False, COLOR_BLACK, Pt(13)),
        ("Sau đây là kết quả kiểm tra:", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 5. I. THÀNH PHẦN LÀM VIỆC
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.first_line_indent = Inches(0)
    p_sec1.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec1, [
        ("I. THÀNH PHẦN LÀM VIỆC", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_tp1 = doc.add_paragraph()
    p_tp1.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_tp1, [
        ("1. Đại diện Tổ kiểm tra chuyên đề:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Ông: ", False, False, COLOR_BLACK, Pt(13)),
        ("Hoàng Tấn Thiên", True, False, COLOR_BLACK, Pt(13)),
        (" – Chức vụ: Tổ trưởng chuyên môn Tổ Toán – Tin học (Tổ trưởng Tổ kiểm tra).\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Ông: ", False, False, COLOR_BLACK, Pt(13)),
        ("Trần Sáng", True, False, COLOR_BLACK, Pt(13)),
        (" – Chức vụ: Tổ phó chuyên môn Tổ Toán – Tin học (Thành viên).\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Bà: ", False, False, COLOR_BLACK, Pt(13)),
        ("Lê Thị Bình", True, False, COLOR_BLACK, Pt(13)),
        (" – Chức vụ: Giáo viên môn Toán (Thư ký ghi biên bản / Thành viên).", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_tp2 = doc.add_paragraph()
    p_tp2.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_tp2, [
        ("2. Đối tượng được kiểm tra chuyên đề:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Ông: ", False, False, COLOR_BLACK, Pt(13)),
        ("Trần Long Hải", True, False, COLOR_BLACK, Pt(13)),
        (" – Chức vụ: Giáo viên giảng dạy môn Toán khối 8, Tổ Toán – Tin học Trường THCS Trần Phú.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_tp3 = doc.add_paragraph()
    p_tp3.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_tp3, [
        ("3. Người chứng kiến (nếu có): ", True, True, COLOR_BLACK, Pt(13)),
        ("Không.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 6. II. NỘI DUNG VÀ TRỌNG TÂM KIỂM TRA CHUYÊN ĐỀ
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.first_line_indent = Inches(0)
    p_sec2.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec2, [
        ("II. NỘI DUNG VÀ TRỌNG TÂM KIỂM TRA CHUYÊN ĐỀ", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_nd = doc.add_paragraph()
    p_nd.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_nd, [
        ("Tổ kiểm tra tiến hành kiểm tra chuyên sâu chuyên đề: ", False, False, COLOR_BLACK, Pt(13)),
        ("“Đổi mới phương pháp dạy học, xây dựng Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH và tích hợp Khung Năng lực số, Khung AI trong môn Toán lớp 8”", True, False, COLOR_BLACK, Pt(13)),
        (" thông qua hồ sơ kế hoạch bài dạy và tiết dạy minh họa trên lớp. Cụ thể gồm các nội dung:", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_nd_sub = doc.add_paragraph()
    p_nd_sub.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_nd_sub, [
        ("1. Kiểm tra cấu trúc Kế hoạch bài dạy (KHBD) theo quy định tại Công văn 5512/BGDĐT-GDTrH đối với Bài 9: Phân tích đa thức thành nhân tử (3 tiết) – Tiết 24, Tuần 12, Toán 8 (Bộ sách Kết nối tri thức với cuộc sống).\n", False, False, COLOR_BLACK, Pt(13)),
        ("2. Kiểm tra chuỗi 4 hoạt động học tập (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng): Việc chuyển giao nhiệm vụ học tập, tổ chức cho học sinh hoạt động nhóm bảng phụ, hệ thống bài tập thực hành và câu hỏi củng cố.\n", False, False, COLOR_BLACK, Pt(13)),
        ("3. Kiểm tra việc tích hợp Khung Năng lực số (NLS 20%) và 12 tiết Khung AI: Việc lựa chọn học liệu số, trình chiếu tương tác, phần mềm trò chơi học tập và hình thức thể hiện (in đậm, in nghiêng mục tiêu/hoạt động tích hợp) trong KHBD.\n", False, False, COLOR_BLACK, Pt(13)),
        ("4. Kiểm tra việc tuân thủ phân phối chương trình môn học, tiến độ đưa bài lên hệ thống CSDL ngành (truong.dongnai.edu.vn) và thực hiện ký số điện tử theo quy định của nhà trường.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 7. III. KẾT QUẢ KIỂM TRA VÀ ĐÁNH GIÁ CHUYÊN MÔN
    p_sec3 = doc.add_paragraph()
    p_sec3.paragraph_format.first_line_indent = Inches(0)
    p_sec3.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec3, [
        ("III. KẾT QUẢ KIỂM TRA VÀ ĐÁNH GIÁ CHUYÊN MÔN", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_ud = doc.add_paragraph()
    p_ud.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_ud, [
        ("1. Ưu điểm nổi bật:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Về cấu trúc và mục tiêu bài dạy: ", True, False, COLOR_BLACK, Pt(13)),
        ("Kế hoạch bài dạy Bài 9 (Tiết 24, Tuần 12) được xây dựng đúng quy chuẩn cấu trúc Công văn 5512/BGDĐT-GDTrH. Mục tiêu bài học xác định rõ ràng yêu cầu cần đạt: Học sinh nhận biết và vận dụng thành thạo 3 phương pháp phân tích đa thức thành nhân tử (đặt nhân tử chung, dùng hằng đẳng thức, nhóm hạng tử). Chú trọng phát triển các năng lực toán học cốt lõi: năng lực tư duy và lập luận toán học, mô hình hóa toán học, giao tiếp toán học và giải quyết vấn đề toán học.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Về thiết bị và học liệu dạy học: ", True, False, COLOR_BLACK, Pt(13)),
        ("Chuẩn bị công phu, hiện đại; kết hợp hài hòa giữa SGK, giáo án điện tử PPT, phiếu học tập, bảng phụ nhóm và video âm nhạc sinh động.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Về đổi mới phương pháp tổ chức hoạt động: ", True, False, COLOR_BLACK, Pt(13)),
        ("Hoạt động khởi động sáng tạo, hấp dẫn khi lồng ghép video bài hát “Hello Song” vận động đầu giờ (3 phút) giúp học sinh giải tỏa áp lực, sau đó khéo léo kết nối với tình huống bài toán thực tế của nhân vật Vuông và Tròn (4 phút) để gợi mở kiến thức mới. Hoạt động hình thành kiến thức (Tiết 1: Đặt nhân tử chung) được bố cục theo bảng 2 cột đối chiếu rõ nét giữa Hoạt động của GV và Sản phẩm của HS; tổ chức hiệu quả hoạt động nhóm với bảng phụ ở phần Luyện tập 1. Hoạt động luyện tập được số hóa sinh động qua trò chơi tương tác “Ai là triệu phú” với 5 câu hỏi trắc nghiệm có quyền trợ giúp, kích thích tối đa sự hứng thú và thi đua học tập của học sinh.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Về tiến độ chuyên môn: ", True, False, COLOR_BLACK, Pt(13)),
        ("Đảm bảo khớp 100% phân phối chương trình môn Toán 8 học kỳ I năm học 2026 - 2027.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_tt = doc.add_paragraph()
    p_tt.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_tt, [
        ("2. Tồn tại, hạn chế cần khắc phục:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Về thể thức tích hợp Năng lực số và Khung AI: ", True, False, COLOR_BLACK, Pt(13)),
        ("Giáo viên đã có ý thức ứng dụng CNTT (PowerPoint, video, trò chơi trắc nghiệm số hóa), tuy nhiên trong KHBD ", False, False, COLOR_BLACK, Pt(13)),
        ("chưa thể hiện tường minh mục tiêu và hoạt động tích hợp Khung Năng lực số (chỉ tiêu 20% số tiết) và Khung AI (12 tiết); chưa in đậm, in nghiêng nội dung tích hợp", True, False, COLOR_RED, Pt(13)),
        (" theo đúng quy định chuyên môn nghiêm ngặt của Tổ và Nhà trường.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Về kỹ thuật trình bày bảng 2 cột: ", True, False, COLOR_BLACK, Pt(13)),
        ("Tại mục d) Tổ chức thực hiện của Hoạt động hình thành kiến thức, toàn bộ các nội dung (HĐ1, Ví dụ 1, Bài tập phụ, Luyện tập 1, Vận dụng 1) đang gộp chung trong 1 ô bảng duy nhất, thiếu sự phân tách rành mạch các dòng và chưa thể hiện thời lượng ước tính cụ thể cho từng bước nhỏ.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Về ký hiệu toán học: ", True, False, COLOR_BLACK, Pt(13)),
        ("Trong lời dẫn tình huống khởi động có câu bị khuyết biểu thức: ", False, False, COLOR_BLACK, Pt(13)),
        ("“...tìm được tất cả số x để biểu thức . Vuông nghe vậy...”", False, True, COLOR_RED, Pt(13)),
        ("; cần kiểm tra rà soát hiển thị công thức Word Equation (OMML) chuẩn xác, tránh lỗi khuyết dữ liệu.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Về ký số CSDL ngành: ", True, False, COLOR_BLACK, Pt(13)),
        ("Cần rà soát hoàn tất thao tác ký số điện tử bài soạn trên CSDL ngành đúng tuần quy định.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_nn = doc.add_paragraph()
    p_nn.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_nn, [
        ("3. Nguyên nhân của tồn tại:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Khách quan: ", True, False, COLOR_BLACK, Pt(13)),
        ("Chương Đa thức Toán 8 có lượng bài tập và kiến thức biến đổi đại số tương đối nặng, giáo viên dành nhiều thời gian xây dựng hệ thống câu hỏi tương tác trò chơi cho học sinh.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- ", False, False, COLOR_BLACK, Pt(13)),
        ("Chủ quan: ", True, False, COLOR_BLACK, Pt(13)),
        ("Giáo viên chưa cập nhật triệt để quy định kỹ thuật về việc in đậm, in nghiêng mục tiêu và địa chỉ tích hợp NLS/AI vào giáo án Word trước khi tải lên hệ thống.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 8. IV. KIẾN NGHỊ CỦA TỔ KIỂM TRA
    p_sec4 = doc.add_paragraph()
    p_sec4.paragraph_format.first_line_indent = Inches(0)
    p_sec4.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec4, [
        ("IV. KIẾN NGHỊ CỦA TỔ KIỂM TRA", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_kn = doc.add_paragraph()
    p_kn.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_kn, [
        ("1. Đối với giáo viên Trần Long Hải:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Tiếp tục phát huy thế mạnh về phương pháp dạy học tích cực, tổ chức trò chơi học tập tạo không khí hào hứng cho học sinh trong các tiết dạy tiếp theo.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Khẩn trương rà soát, chỉnh sửa kỹ thuật soạn bài: ", False, False, COLOR_BLACK, Pt(13)),
        ("bổ sung mục tiêu NLS/AI, in đậm và in nghiêng phần tích hợp", True, False, COLOR_RED, Pt(13)),
        ("; hoàn thiện công thức toán bị khuyết và căn chỉnh lại bảng 2 cột rõ ràng từng hoạt động.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Hoàn thành việc cập nhật ký số bài giảng trên cổng CSDL ngành trước ngày ", False, False, COLOR_BLACK, Pt(13)),
        ("28/11/2026", True, False, COLOR_RED, Pt(13)),
        (".\n", False, False, COLOR_BLACK, Pt(13)),
        ("2. Đối với Tổ chuyên môn Toán – Tin học:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Tổ chức trao đổi, nhân rộng kinh nghiệm thiết kế hoạt động khởi động sinh động và trò chơi học tập tương tác của Thầy Hải trong buổi sinh hoạt chuyên môn toàn tổ.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Hỗ trợ, theo dõi và kiểm tra lại việc khắc phục các tồn tại về thể thức bài soạn của giáo viên.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 9. V. Ý KIẾN CỦA GIÁO VIÊN ĐƯỢC KIỂM TRA
    p_sec5 = doc.add_paragraph()
    p_sec5.paragraph_format.first_line_indent = Inches(0)
    p_sec5.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec5, [
        ("V. Ý KIẾN CỦA GIÁO VIÊN ĐƯỢC KIỂM TRA (ÔNG TRẦN LONG HẢI)", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_yk = doc.add_paragraph()
    p_yk.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_yk, [
        ("Tôi hoàn toàn nhất trí với toàn bộ nhận xét, đánh giá khách quan của Tổ kiểm tra. Tôi xin tiếp thu các ý kiến đóng góp về kỹ thuật trình bày, cam kết sẽ bổ sung đầy đủ phần in đậm nghiêng tích hợp Năng lực số / AI, rà soát lại công thức toán học và hoàn thành ký số đúng thời hạn được giao.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 10. Đoạn kết
    p_end = doc.add_paragraph()
    p_end.paragraph_format.first_line_indent = Inches(0.5)
    p_end.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_end, [
        ("Việc kiểm tra chuyên đề kết thúc vào hồi ", False, False, COLOR_BLACK, Pt(13)),
        ("10 giờ 30 phút", False, False, COLOR_RED, Pt(13)),
        (" cùng ngày và được lập thành biên bản. Biên bản đã được đọc lại cho tất cả các thành viên tham dự cùng nghe, thống nhất ký tên xác nhận; biên bản được lập thành 02 bản có giá trị pháp lý như nhau, mỗi bên giữ 01 bản để thực hiện./.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 11. Bảng Chữ ký 3 bên (không viền)
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.first_line_indent = Inches(0)
    p_sp.paragraph_format.space_before = Pt(8)
    
    tbl_sig = doc.add_table(rows=1, cols=3)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(tbl_sig)
    
    c1 = tbl_sig.cell(0, 0)
    c2 = tbl_sig.cell(0, 1)
    c3 = tbl_sig.cell(0, 2)
    c1.width = Inches(2.3)
    c2.width = Inches(2.4)
    c3.width = Inches(2.3)
    
    p_c1 = c1.paragraphs[0]
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.first_line_indent = Inches(0)
    add_paragraph_runs(p_c1, [
        ("NGƯỜI ĐƯỢC KIỂM TRA\n", True, False, COLOR_BLACK, Pt(12)),
        ("(Ký và ghi rõ họ tên)\n\n\n\n\n", False, True, COLOR_BLACK, Pt(11)),
        ("Trần Long Hải", True, False, COLOR_BLACK, Pt(12)),
    ])
    
    p_c2 = c2.paragraphs[0]
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.first_line_indent = Inches(0)
    add_paragraph_runs(p_c2, [
        ("TỔ TRƯỞNG TỔ KIỂM TRA\n", True, False, COLOR_BLACK, Pt(12)),
        ("(Ký và ghi rõ họ tên)\n\n\n\n\n", False, True, COLOR_BLACK, Pt(11)),
        ("Hoàng Tấn Thiên", True, False, COLOR_BLACK, Pt(12)),
    ])
    
    p_c3 = c3.paragraphs[0]
    p_c3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c3.paragraph_format.first_line_indent = Inches(0)
    add_paragraph_runs(p_c3, [
        ("NGƯỜI GHI BIÊN BẢN\n", True, False, COLOR_BLACK, Pt(12)),
        ("(Ký và ghi rõ họ tên)\n\n\n\n\n", False, True, COLOR_BLACK, Pt(11)),
        ("Lê Thị Bình", True, False, COLOR_BLACK, Pt(12)),
    ])
    
    return doc

def create_mau_05():
    doc = create_base_document()
    
    # 1. Tiêu ngữ mẫu phía trên cùng
    p_mau = doc.add_paragraph()
    p_mau.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mau.paragraph_format.first_line_indent = Inches(0)
    p_mau.paragraph_format.space_after = Pt(4)
    run1 = p_mau.add_run("Mẫu số 05\n")
    run1.bold = True
    run1.font.name = 'Times New Roman'
    run1.font.size = Pt(11.5)
    run2 = p_mau.add_run("(Kèm theo Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026 của Sở Giáo dục và Đào tạo thành phố Đồng Nai)")
    run2.italic = True
    run2.font.name = 'Times New Roman'
    run2.font.size = Pt(11)
    
    # 2. Header 2 cột không viền
    tbl_hdr = doc.add_table(rows=1, cols=2)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(tbl_hdr)
    
    cell_left = tbl_hdr.cell(0, 0)
    cell_right = tbl_hdr.cell(0, 1)
    cell_left.width = Inches(3.2)
    cell_right.width = Inches(3.8)
    
    # Cột trái
    p_l = cell_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.first_line_indent = Inches(0)
    p_l.paragraph_format.line_spacing = 1.15
    add_paragraph_runs(p_l, [
        ("TRƯỜNG THCS TRẦN PHÚ\n", True, False, COLOR_BLACK, Pt(12)),
        ("TỔ KIỂM TRA THEO QĐ SỐ ", True, False, COLOR_BLACK, Pt(11.5)),
        ("18", True, False, COLOR_RED, Pt(11.5)),
    ])
    
    # Cột phải
    p_r = cell_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.first_line_indent = Inches(0)
    p_r.paragraph_format.line_spacing = 1.15
    add_paragraph_runs(p_r, [
        ("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n", True, False, COLOR_BLACK, Pt(12)),
        ("Độc lập - Tự do - Hạnh phúc\n", True, False, COLOR_BLACK, Pt(12.5)),
        ("Xuân Đông, ngày 23 tháng 11 năm 2026", False, True, COLOR_BLACK, Pt(12)),
    ])
    
    # Khoảng cách
    p_space = doc.add_paragraph()
    p_space.paragraph_format.first_line_indent = Inches(0)
    p_space.paragraph_format.space_before = Pt(4)
    p_space.paragraph_format.space_after = Pt(2)
    
    # 3. Tiêu đề chính
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.first_line_indent = Inches(0)
    p_title.paragraph_format.space_after = Pt(2)
    add_paragraph_runs(p_title, [
        ("BÁO CÁO\n", True, False, COLOR_BLACK, Pt(14)),
        ("Kết quả kiểm tra chuyên đề về việc đổi mới phương pháp dạy học,\n", True, False, COLOR_BLACK, Pt(13)),
        ("xây dựng Kế hoạch bài dạy và tích hợp Khung Năng lực số, AI môn Toán 8\n", True, False, COLOR_BLACK, Pt(13)),
        ("đối với giáo viên Trần Long Hải", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    # Kính gửi
    p_kg = doc.add_paragraph()
    p_kg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_kg.paragraph_format.first_line_indent = Inches(0)
    p_kg.paragraph_format.space_after = Pt(6)
    add_paragraph_runs(p_kg, [
        ("Kính gửi: ", True, True, COLOR_BLACK, Pt(13)),
        ("Hiệu trưởng Trường THCS Trần Phú.", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 4. Căn cứ & mở đầu
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_intro, [
        ("Thực hiện Quyết định số ", False, False, COLOR_BLACK, Pt(13)),
        ("18/QĐ-THCS.TP", False, False, COLOR_RED, Pt(13)),
        (" ngày ", False, False, COLOR_BLACK, Pt(13)),
        ("15 tháng 11 năm 2026", False, False, COLOR_RED, Pt(13)),
        (" của Hiệu trưởng Trường THCS Trần Phú về việc thành lập Tổ kiểm tra nội bộ chuyên môn năm học 2026 - 2027;\n", False, False, COLOR_BLACK, Pt(13)),
        ("Tổ kiểm tra đã tiến hành kiểm tra chuyên đề chuyên môn đối với ông ", False, False, COLOR_BLACK, Pt(13)),
        ("Trần Long Hải", True, False, COLOR_BLACK, Pt(13)),
        (" – Giáo viên giảng dạy môn Toán khối 8, Tổ Toán – Tin học.\n", False, False, COLOR_BLACK, Pt(13)),
        ("Quá trình kiểm tra, Tổ kiểm tra đã làm việc, thu thập hồ sơ minh chứng, thẩm định Kế hoạch bài dạy và trao đổi trực tiếp với giáo viên vào ngày 23 tháng 11 năm 2026.\n", False, False, COLOR_BLACK, Pt(13)),
        ("Sau đây là kết quả kiểm tra:", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 5. I. KHÁI QUÁT CHUNG
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.first_line_indent = Inches(0)
    p_sec1.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec1, [
        ("I. KHÁI QUÁT CHUNG", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_kq = doc.add_paragraph()
    p_kq.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_kq, [
        ("- Họ và tên giáo viên được kiểm tra: ", False, False, COLOR_BLACK, Pt(13)),
        ("Trần Long Hải", True, False, COLOR_BLACK, Pt(13)),
        (".\n- Chức vụ chuyên môn: Giáo viên môn Toán; Tổ chuyên môn: Toán – Tin học.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Trình độ đào tạo: Đại học Sư phạm Toán học.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Phân công nhiệm vụ năm học 2026 - 2027: Giảng dạy môn Toán khối 8, tham gia đầy đủ các hoạt động chuyên môn, sinh hoạt tổ và các phong trào thi đua của nhà trường.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Ý thức tổ chức kỷ luật và nề nếp chuyên môn: Chấp hành tốt chủ trương, đường lối chính sách của Đảng và pháp luật của Nhà nước; thực hiện nghiêm túc quy chế chuyên môn, ngày giờ công đảm bảo, có tinh thần trách nhiệm và tích cực đổi mới phương pháp dạy học.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 6. II. KẾT QUẢ KIỂM TRA, XÁC MINH THEO CHUYÊN ĐỀ
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.first_line_indent = Inches(0)
    p_sec2.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec2, [
        ("II. KẾT QUẢ KIỂM TRA, XÁC MINH THEO CHUYÊN ĐỀ", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_xm1 = doc.add_paragraph()
    p_xm1.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_xm1, [
        ("1. Về tiến độ và tính pháp lý của hồ sơ bài dạy:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Giáo viên cung cấp đầy đủ Kế hoạch bài dạy theo phân phối chương trình: Bài 9: Phân tích đa thức thành nhân tử (3 tiết) – Tiết 24, Tuần 12, môn Toán 8 (Bộ sách Kết nối tri thức với cuộc sống).\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Tiến độ soạn giảng khớp hoàn toàn với Kế hoạch giáo dục môn học của Tổ chuyên môn và Phụ lục 3 của nhà trường.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_xm2 = doc.add_paragraph()
    p_xm2.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_xm2, [
        ("2. Về chất lượng sư phạm và đổi mới phương pháp dạy học (Công văn 5512/BGDĐT-GDTrH):\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Kế hoạch bài dạy được thiết kế chặt chẽ theo cấu trúc 3 phần chuẩn; mục tiêu phân định rõ ràng giữa yêu cầu cần đạt về kiến thức, các năng lực toán học đặc thù (tư duy lập luận, giao tiếp toán học, mô hình hóa toán học, giải quyết vấn đề) và phẩm chất học sinh.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Hoạt động Khởi động có sự đổi mới sáng tạo nổi bật: Sử dụng video âm nhạc “Hello Song” giải tỏa căng thẳng (3 phút) kết hợp đưa ra bài toán thực tế của Vuông và Tròn (4 phút) tạo tình huống có vấn đề dẫn dắt học sinh tiếp cận kiến thức phân tích đa thức thành nhân tử rất tự nhiên.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Hoạt động Hình thành kiến thức mới (Tiết 1: Đặt nhân tử chung) thể hiện theo bảng 2 cột rõ ràng; chú trọng hoạt động của học sinh, tổ chức thảo luận nhóm bảng phụ ở Luyện tập 1.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Hoạt động Luyện tập được thiết kế sáng tạo thông qua trò chơi trắc nghiệm tương tác “Ai là triệu phú” (5 câu hỏi phân hóa có quyền trợ giúp), giúp học sinh khắc sâu kiến thức trong không khí thi đua sôi nổi.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_xm3 = doc.add_paragraph()
    p_xm3.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_xm3, [
        ("3. Về việc tích hợp Khung Năng lực số (NLS), AI và ký số CSDL ngành:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Đã chủ động ứng dụng công nghệ thông tin trong thiết kế bài giảng (slide PowerPoint, video ca nhạc, trò chơi trắc nghiệm).\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Tuy nhiên, phần chỉ tiêu tích hợp Khung Năng lực số (20% số tiết) và Khung AI (12 tiết) ", False, False, COLOR_BLACK, Pt(13)),
        ("chưa được ghi rõ mã năng lực, chưa in đậm, in nghiêng mục tiêu và hoạt động tích hợp", True, False, COLOR_RED, Pt(13)),
        (" trong KHBD theo quy định bắt buộc của Tổ chuyên môn.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Bảng tiến trình tổ chức hoạt động ở mục d cần được tách dòng các hoạt động nhỏ và bổ sung thời lượng ước tính; rà soát biểu thức toán học trong tình huống khởi động để đảm bảo 100% hiển thị chuẩn Word Equation.\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Cần hoàn tất ký số điện tử trên hệ thống truong.dongnai.edu.vn đúng tuần chuyên môn.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 7. III. KẾT LUẬN VỀ NỘI DUNG KIỂM TRA CHUYÊN ĐỀ
    p_sec3 = doc.add_paragraph()
    p_sec3.paragraph_format.first_line_indent = Inches(0)
    p_sec3.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec3, [
        ("III. KẾT LUẬN VỀ NỘI DUNG KIỂM TRA CHUYÊN ĐỀ", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_kl = doc.add_paragraph()
    p_kl.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_kl, [
        ("1. Đánh giá chung: ", True, False, COLOR_BLACK, Pt(13)),
        ("Kế hoạch bài dạy chuyên đề của Thầy Trần Long Hải được đầu tư nghiêm túc, có nhiều điểm sáng tạo trong đổi mới phương pháp dạy học, ứng dụng trò chơi tương tác và học liệu số sinh động, kích thích tinh thần tự học và hợp tác của học sinh, đáp ứng tốt tinh thần Chương trình GDPT 2018.\n", False, False, COLOR_BLACK, Pt(13)),
        ("2. Xếp loại hồ sơ Kế hoạch bài dạy chuyên đề: ", True, False, COLOR_BLACK, Pt(13)),
        ("LOẠI TỐT", True, False, COLOR_RED, Pt(13)),
        (".\n", False, False, COLOR_BLACK, Pt(13)),
        ("3. Trách nhiệm: ", True, False, COLOR_BLACK, Pt(13)),
        ("Thuộc về cá nhân giáo viên Trần Long Hải trong việc nhanh chóng hoàn thiện thể thức in đậm nghiêng tích hợp NLS/AI và ký số theo quy chuẩn chuyên môn của đơn vị.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 8. IV. CÁC BIỆN PHÁP XỬ LÝ THEO THẨM QUYỀN ĐÃ ÁP DỤNG
    p_sec4 = doc.add_paragraph()
    p_sec4.paragraph_format.first_line_indent = Inches(0)
    p_sec4.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec4, [
        ("IV. CÁC BIỆN PHÁP XỬ LÝ THEO THẨM QUYỀN ĐÃ ÁP DỤNG", True, False, COLOR_BLACK, Pt(13)),
    ])
    p_bp = doc.add_paragraph()
    p_bp.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_bp, [
        ("Tổ kiểm tra đã tiến hành hướng dẫn trực tiếp cho giáo viên kỹ thuật thể hiện chữ in đậm, in nghiêng đối với các mục tiêu tích hợp Năng lực số / AI và cách căn chỉnh bảng 2 cột đúng thể thức hành chính tại buổi làm việc.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 9. V. NHỮNG Ý KIẾN KHÁC NHAU GIỮA CÁC THÀNH VIÊN TỔ KIỂM TRA
    p_sec5 = doc.add_paragraph()
    p_sec5.paragraph_format.first_line_indent = Inches(0)
    p_sec5.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec5, [
        ("V. NHỮNG Ý KIẾN KHÁC NHAU GIỮA CÁC THÀNH VIÊN TỔ KIỂM TRA", True, False, COLOR_BLACK, Pt(13)),
    ])
    p_yk = doc.add_paragraph()
    p_yk.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_yk, [
        ("Không (100% thành viên Tổ kiểm tra thống nhất với toàn bộ nội dung đánh giá và kết luận).", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 10. VI. KIẾN NGHỊ VÀ ĐỀ XUẤT
    p_sec6 = doc.add_paragraph()
    p_sec6.paragraph_format.first_line_indent = Inches(0)
    p_sec6.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_sec6, [
        ("VI. KIẾN NGHỊ VÀ ĐỀ XUẤT", True, False, COLOR_BLACK, Pt(13)),
    ])
    
    p_kn_full = doc.add_paragraph()
    p_kn_full.paragraph_format.first_line_indent = Inches(0.5)
    add_paragraph_runs(p_kn_full, [
        ("1. Đối với Hiệu trưởng Trường THCS Trần Phú:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Đề nghị Hiệu trưởng xem xét ghi nhận kết quả kiểm tra chuyên đề đối với giáo viên Trần Long Hải; công nhận xếp loại hồ sơ Kế hoạch bài dạy chuyên đề: ", False, False, COLOR_BLACK, Pt(13)),
        ("Loại Tốt", True, False, COLOR_RED, Pt(13)),
        (".\n", False, False, COLOR_BLACK, Pt(13)),
        ("- Biểu dương tinh thần tích cực đổi mới phương pháp dạy học, tổ chức trò chơi học tập tương tác của giáo viên để khích lệ phong trào chuyên môn chung trong nhà trường.\n", False, False, COLOR_BLACK, Pt(13)),
        ("2. Đối với cá nhân giáo viên Trần Long Hải:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Bổ sung nội dung in đậm nghiêng tích hợp NLS và AI vào KHBD Bài 9 và toàn bộ các bài dạy tiếp theo; hoàn tất việc ký số điện tử trên hệ thống CSDL ngành trước ngày ", False, False, COLOR_BLACK, Pt(13)),
        ("28/11/2026", True, False, COLOR_RED, Pt(13)),
        (".\n", False, False, COLOR_BLACK, Pt(13)),
        ("3. Đối với Tổ chuyên môn Toán – Tin học:\n", True, True, COLOR_BLACK, Pt(13)),
        ("- Đôn đốc, giám sát việc hoàn thiện hồ sơ của giáo viên theo đúng thời hạn quy định.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 11. Đoạn kết
    p_end = doc.add_paragraph()
    p_end.paragraph_format.first_line_indent = Inches(0.5)
    p_end.paragraph_format.space_before = Pt(6)
    add_paragraph_runs(p_end, [
        ("Trên đây là Báo cáo kết quả kiểm tra chuyên đề về việc đổi mới phương pháp dạy học, xây dựng Kế hoạch bài dạy và tích hợp Khung Năng lực số, AI môn Toán 8 đối với giáo viên Trần Long Hải. Tổ kiểm tra kính trình Hiệu trưởng xem xét và cho ý kiến chỉ đạo./.", False, False, COLOR_BLACK, Pt(13)),
    ])
    
    # 12. Bảng Chữ ký & Nơi nhận (1 hàng 2 cột không viền)
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.first_line_indent = Inches(0)
    p_sp.paragraph_format.space_before = Pt(8)
    
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_no_borders(tbl_sig)
    
    c1 = tbl_sig.cell(0, 0)
    c2 = tbl_sig.cell(0, 1)
    c1.width = Inches(3.5)
    c2.width = Inches(3.5)
    
    p_c1 = c1.paragraphs[0]
    p_c1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_c1.paragraph_format.first_line_indent = Inches(0)
    p_c1.paragraph_format.line_spacing = 1.15
    add_paragraph_runs(p_c1, [
        ("Nơi nhận:\n", True, True, COLOR_BLACK, Pt(11)),
        ("- Hiệu trưởng (để b/c);\n", False, False, COLOR_BLACK, Pt(10)),
        ("- Thầy Trần Long Hải (để th/h);\n", False, False, COLOR_BLACK, Pt(10)),
        ("- Lưu: Hồ sơ KTNB.", False, False, COLOR_BLACK, Pt(10)),
    ])
    
    p_c2 = c2.paragraphs[0]
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.first_line_indent = Inches(0)
    p_c2.paragraph_format.line_spacing = 1.15
    add_paragraph_runs(p_c2, [
        ("TỔ TRƯỞNG TỔ KIỂM TRA\n", True, False, COLOR_BLACK, Pt(12)),
        ("(Ký và ghi rõ họ tên)\n\n\n\n\n", False, True, COLOR_BLACK, Pt(11)),
        ("Hoàng Tấn Thiên", True, False, COLOR_BLACK, Pt(12)),
    ])
    
    return doc

def main():
    out_dir = Path("TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/23.11")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    doc4 = create_mau_04()
    p4 = out_dir / "Bien_Ban_Kiem_Tra_Chuyen_De_Thay_Hai_Mau_04.docx"
    doc4.save(str(p4))
    print(f"Saved: {p4}")
    
    doc5 = create_mau_05()
    p5 = out_dir / "Bao_Cao_Ket_Qua_Kiem_Tra_Chuyen_De_Thay_Hai_Mau_05.docx"
    doc5.save(str(p5))
    print(f"Saved: {p5}")

if __name__ == "__main__":
    main()
