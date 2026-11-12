# -*- coding: utf-8 -*-
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_element(name):
    return OxmlElement(name)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    trPr.append(tblHeader)

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = OxmlElement('w:cantSplit')
    trPr.append(cantSplit)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def format_run(run, font_name="Times New Roman", size_pt=13, bold=False, italic=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), font_name)

def add_p(doc, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=2, line_spacing=1.2, indent=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if indent > 0:
        p.paragraph_format.first_line_indent = Inches(indent)
    if text:
        r = p.add_run(text)
        format_run(r, size_pt=13)
    return p

out_dir = r"C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\8_TAO_BAO_CAO\Ket_qua\05.11"
os.makedirs(out_dir, exist_ok=True)
docx_path = os.path.join(out_dir, "Ke_Hoach_Dang_Ky_Tiet_Hoc_Thu_Vien_To_Toan_Tin_HK1.docx")

doc = Document()

# Page setup A4
for s in doc.sections:
    s.page_width = Mm(210)
    s.page_height = Mm(297)
    s.top_margin = Mm(20)
    s.bottom_margin = Mm(20)
    s.left_margin = Mm(30)
    s.right_margin = Mm(15)

# 1. Header Table (2 columns)
tbl_h = doc.add_table(rows=1, cols=2)
tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_h.autofit = False
tbl_h.columns[0].width = Mm(65)
tbl_h.columns[1].width = Mm(100)

c_left = tbl_h.cell(0, 0)
p1 = c_left.paragraphs[0]
p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p1.paragraph_format.space_before = Pt(0)
p1.paragraph_format.space_after = Pt(1)
p1.paragraph_format.line_spacing = 1.0
r = p1.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
format_run(r, size_pt=12, bold=False)
r = p1.add_run("TỔ TOÁN – TIN HỌC\n")
format_run(r, size_pt=12, bold=True)
r = p1.add_run("Số: 09/KH-TTIN")
format_run(r, size_pt=12, italic=True)

c_right = tbl_h.cell(0, 1)
p2 = c_right.paragraphs[0]
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.paragraph_format.space_before = Pt(0)
p2.paragraph_format.space_after = Pt(1)
p2.paragraph_format.line_spacing = 1.0
r = p2.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
format_run(r, size_pt=12, bold=True)
r = p2.add_run("Độc lập – Tự do – Hạnh phúc\n")
format_run(r, size_pt=13, bold=True)
r = p2.add_run("Xuân Đông, ngày 05 tháng 11 năm 2026")
format_run(r, size_pt=12, italic=True)

for row in tbl_h.rows:
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)

p_sep = doc.add_paragraph()
p_sep.paragraph_format.space_before = Pt(4)
p_sep.paragraph_format.space_after = Pt(8)

# Title
p_t = doc.add_paragraph()
p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_t.paragraph_format.space_before = Pt(6)
p_t.paragraph_format.space_after = Pt(2)
r = p_t.add_run("KẾ HOẠCH\n")
format_run(r, size_pt=14, bold=True)
r = p_t.add_run("TRIỂN KHAI ĐĂNG KÝ VÀ TỔ CHỨC TIẾT HỌC THƯ VIỆN\n(KHAI THÁC CSDL THƯ VIỆN SỐ DLIBK12 KẾT HỢP TIVI VÀ LAPTOP)\nHỌC KỲ I — NĂM HỌC 2026 - 2027")
format_run(r, size_pt=13.5, bold=True)

cancu = [
    "Căn cứ Thông tư số 16/2022/TT-BGDĐT ngày 22/11/2022 của Bộ Giáo dục và Đào tạo ban hành quy định tiêu chuẩn thư viện cơ sở giáo dục mầm non và phổ thông;",
    "Căn cứ Công văn số 4200/SGDĐT-GDPT&GDTX ngày 22/8/2026 của Sở GD&ĐT tỉnh Đồng Nai về việc hướng dẫn thực hiện nhiệm vụ GD trung học cơ sở năm học 2026 - 2027;",
    "Căn cứ Kế hoạch số 85/KH-THCS.TP ngày 15/9/2026 của Trường THCS Trần Phú về Kế hoạch giáo dục nhà trường năm học 2026 - 2027;",
    "Căn cứ Kế hoạch số 115/KH-THCS.TP ngày 09/10/2026 của Trường THCS Trần Phú về Triển khai thực hiện tiết học và tiết đọc Thư viện trong nhà trường năm học 2026 - 2027;",
    "Căn cứ Kế hoạch giáo dục bộ môn (Phụ lục 3) môn Toán, Tin học và Hoạt động trải nghiệm năm học 2026 - 2027 của Tổ Toán – Tin học đã được Ban Giám hiệu phê duyệt;"
]
for cc in cancu:
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=1, space_after=1, indent=0.5)
    r = p.add_run(cc)
    format_run(r, size_pt=12.5, italic=True)

p_intro = add_p(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=4, indent=0.5)
r = p_intro.add_run("Thực hiện chỉ đạo của Ban Giám hiệu Trường THCS Trần Phú về việc triển khai Tiết học tại Thư viện theo Kế hoạch số 115/KH-THCS.TP; xuất phát từ điều kiện thực tế của nhà trường: nguồn sách in chủ yếu là Sách giáo khoa chương trình chuẩn dùng chung, Tổ Toán – Tin học (gồm 09 giáo viên) thống nhất phương án tập trung khai thác tối đa nguồn học liệu điện tử phong phú trên CSDL Thư viện số DlibK12 kết hợp thiết bị Màn hình Tivi tương tác và Laptop giáo viên. Tổ ban hành Kế hoạch tổ chức và Bảng phân công đăng ký tiết dạy theo Tuần thực hiện như sau:")
format_run(r, size_pt=13)

# I. MỤC ĐÍCH, YÊU CẦU
p_sec1 = add_p(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
r = p_sec1.add_run("I. MỤC ĐÍCH, YÊU CẦU")
format_run(r, size_pt=13, bold=True)

p = add_p(doc, indent=0.5)
r = p.add_run("1. Mục đích:")
format_run(r, size_pt=13, bold=True)
p = add_p(doc, indent=0.5)
r = p.add_run("- Đổi mới không gian và phương thức dạy học: Chuyển dịch từ việc đọc sách in truyền thống sang mô hình Thư viện số hiện đại; khai thác sâu kho học liệu số, video mô phỏng tương tác, bài tập số trên nền tảng DlibK12 qua màn hình Tivi lớn của Thư viện và Laptop.")
format_run(r, size_pt=13)
p = add_p(doc, indent=0.5)
r = p.add_run("- Nâng cao năng lực số (NLS) và tư duy công nghệ cho học sinh: Hướng dẫn học sinh kỹ năng đăng nhập tài khoản DlibK12 cá nhân, tra cứu tài liệu học tập chuẩn xác, xem video bài giảng số và làm bài tập tương tác trên môi trường số.")
format_run(r, size_pt=13)

p = add_p(doc, indent=0.5)
r = p.add_run("2. Yêu cầu:")
format_run(r, size_pt=13, bold=True)
p = add_p(doc, indent=0.5)
r = p.add_run("- Định mức: 100% giáo viên trong tổ hoàn thành tối thiểu 01 tiết dạy Thư viện trong Học kỳ I.")
format_run(r, size_pt=13)
p = add_p(doc, indent=0.5)
r = p.add_run("- Đăng ký theo Tuần linh hoạt: Giáo viên đăng ký theo Tuần thực hiện, Tiết PPCT, Tên bài học. Lịch dạy cụ thể trong tuần sẽ do giáo viên chủ động thống nhất trước 03 ngày với Bộ phận Thư viện để kiểm tra đường truyền mạng Internet, máy chiếu/Tivi và tài khoản DlibK12.")
format_run(r, size_pt=13)
p = add_p(doc, indent=0.5)
r = p.add_run("- Hồ sơ lưu chuyên môn Thư viện (01 bộ/tiết): Gồm Phiếu đăng ký + Kế hoạch bài dạy (KHBD) chuẩn CV 5512 đã có chữ ký duyệt của TTCM và BGH + Minh chứng sản phẩm học tập số của học sinh.")
format_run(r, size_pt=13)

# II. BẢNG PHÂN CÔNG ĐĂNG KÝ TIẾT HỌC THƯ VIỆN THEO TUẦN (KHAI THÁC DLIBK12)
p_sec2 = add_p(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
r = p_sec2.add_run("II. BẢNG PHÂN CÔNG ĐĂNG KÝ TIẾT HỌC THƯ VIỆN THEO TUẦN (KHAI THÁC DLIBK12)")
format_run(r, size_pt=13, bold=True)

# Table data with focus on DlibK12 + TV + Laptop + SGK
table_data = [
    [
        "STT", "Họ và tên GV", "Môn phụ trách", "Lớp thực hiện\n(Theo TKB số 9)", "Tuần thực hiện\n& Tiết PPCT",
        "Tên bài dạy / Chủ đề thực hiện\n(Bám sát SGK Kết nối tri thức)", "Học liệu số & Thiết bị khai thác\n(CSDL DlibK12 + Tivi + Laptop)", "Sản phẩm HS nộp\nlưu Thư viện"
    ],
    [
        "1", "Hoàng Tấn Thiên\n(Tổ trưởng)", "Toán", "Lớp 9/2\n(hoặc 9/1)", "Tuần 11\n(Tiết PPCT: 27)",
        "Bài 8. Khai căn bậc hai với phép nhân và phép chia (Luyện tập ứng dụng)",
        "• Học liệu số DlibK12: Video bài giảng ứng dụng khai căn, ngân hàng câu hỏi trắc nghiệm tương tác trên DlibK12.\n• Thiết bị: Laptop GV kết nối Màn hình Tivi Thư viện, SGK Toán 9 Tập 1.",
        "Phiếu học tập nhóm, kết quả làm trắc nghiệm tương tác trên DlibK12."
    ],
    [
        "2", "Dương Quang Tùng", "Tin học", "Lớp 6/3\n(hoặc 6/2, 8/1)", "Tuần 13\n(Tiết PPCT: 13)",
        "Bài 7. Thực hành: Tìm kiếm thông tin trên Internet và Thư viện số DlibK12",
        "• Học liệu số DlibK12: CSDL sách điện tử và bài giảng số DlibK12, tài liệu an toàn thông tin số.\n• Thiết bị: Laptop GV trình chiếu Tivi, laptop/máy tính HS thực hành đăng nhập và tra cứu DlibK12.",
        "Bài thu hoạch số: Danh mục tài liệu học tập tra cứu được từ DlibK12."
    ],
    [
        "3", "Nguyễn Thị Thảo", "Toán", "Lớp 6/2\n(hoặc 6/5, 7/5)", "Tuần 11\n(Tiết PPCT: 21)",
        "Bài 19. Hình chữ nhật, hình thoi, hình bình hành (STEM Tấm thiệp của em)",
        "• Học liệu số DlibK12: Video mô phỏng hình học phẳng trong tự nhiên và mỹ thuật, học liệu hướng dẫn STEM trên DlibK12.\n• Thiết bị: Laptop GV kết nối Tivi Thư viện, SGK Toán 6 Tập 1.",
        "Mô hình tấm thiệp hình học đối xứng của các nhóm HS."
    ],
    [
        "4", "Lê Thị Bình", "Toán", "Lớp 8/1\n(hoặc 7/1, 8/2)", "Tuần 12\n(Tiết PPCT: 24)",
        "Bài 15. Định lí Thalès trong tam giác (Luyện tập ứng dụng thực tế)",
        "• Học liệu số DlibK12: Tệp mô phỏng hình học động GeoGebra nhúng trên DlibK12; video tư liệu lịch sử đo kim tự tháp của Thalès.\n• Thiết bị: Laptop GV kết nối Tivi Thư viện, SGK Toán 8 Tập 1.",
        "Phiếu bài tập hình học số, sơ đồ tỉ số đoạn thẳng của nhóm."
    ],
    [
        "5", "Hoàng Xuân Ánh", "Toán", "Lớp 7/2\n(hoặc 7/3, 7/4)", "Tuần 11\n(Tiết PPCT: 29)",
        "Bài 10. Tiên đề Euclid và tính chất hai đường thẳng song song trong thực tế",
        "• Học liệu số DlibK12: Mô phỏng 3D góc so le trong, đồng vị trên DlibK12; gói bài tập trực tuyến hình học DlibK12.\n• Thiết bị: Laptop GV kết nối Tivi Thư viện, SGK Toán 7 Tập 1.",
        "Phiếu học tập giải thích hiện tượng quang học và kiến trúc song song."
    ],
    [
        "6", "Trần Long Hải", "Toán", "Lớp 8/4\n(hoặc 8/3, 8/5)", "Tuần 10\n(Tiết PPCT: 18)",
        "Bài 15. Định lí Thalès trong tam giác (STEM Đo đạc bóng nắng thực tế)",
        "• Học liệu số DlibK12: Video clip hướng dẫn kỹ thuật đo gián tiếp chiều cao bằng định lí Thalès trên DlibK12; bảng tính số liệu.\n• Thiết bị: Laptop GV kết nối Tivi Thư viện, thước dây, SGK Toán 8.",
        "Bản tường trình số đo bóng nắng thực tế và sai số thực nghiệm."
    ],
    [
        "7", "Trần Sáng", "Toán", "Lớp 9/5\n(hoặc 9/6, 9/7)", "Tuần 11\n(Tiết PPCT: 15)",
        "Bài 15. Độ dài cung tròn, diện tích hình quạt tròn và vành khuyên (STEM)",
        "• Học liệu số DlibK12: Hoạt hình mô phỏng chuyển động quét của bán kính tạo quạt tròn trên DlibK12; tư liệu kiến trúc vòm cung.\n• Thiết bị: Laptop GV kết nối Tivi Thư viện, compa kỹ thuật lớn, SGK Toán 9.",
        "Mô hình quạt nghệ thuật kèm bảng tính diện tích vật liệu thực tế."
    ],
    [
        "8", "Hồ Đăng Danh", "Toán", "Lớp 6/3\n(hoặc 6/4, 9/3)", "Tuần 13\n(Tiết PPCT: 49)",
        "Hoạt động thực hành & trải nghiệm: Sử dụng máy tính cầm tay giải toán thực tế",
        "• Học liệu số DlibK12: Phần mềm giả lập máy tính điện tử trên DlibK12 chiếu lên Tivi; ngân hàng bài toán số học thực tế DlibK12.\n• Thiết bị: Laptop GV kết nối Tivi Thư viện, máy tính cầm tay HS, SGK Toán 6.",
        "Phiếu thực hành bấm máy tính và quy trình giải nhanh bài toán."
    ],
    [
        "9", "Nguyễn Văn Tính", "HĐTN", "Lớp 6/2\n(hoặc 6/5, 7/5)", "Tuần 11\n(Tiết PPCT: 32)",
        "Chủ đề 3: Xây dựng nền nếp tự học và rèn luyện kỹ năng khai thác Thư viện số DlibK12",
        "• Học liệu số DlibK12: Sách điện tử (E-book) kỹ năng sống THCS trên DlibK12; video diễn đàn phương pháp tự học thời đại số.\n• Thiết bị: Laptop GV kết nối Tivi Thư viện, tài khoản DlibK12 học sinh.",
        "Sổ tay tự học số (mẫu KWL) và phiếu cam kết văn hóa đọc số."
    ]
]

tbl_data = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
tbl_data.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_data.autofit = False
set_table_borders(tbl_data)

col_widths = [Mm(10), Mm(26), Mm(14), Mm(20), Mm(18), Mm(32), Mm(34), Mm(24)]

for r_idx, row in enumerate(tbl_data.rows):
    make_row_cant_split(row)
    if r_idx == 0:
        make_row_header(row)
    for c_idx, cell in enumerate(row.cells):
        cell.width = col_widths[c_idx]
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.05
        
        text = table_data[r_idx][c_idx]
        if r_idx == 0:
            set_cell_shading(cell, "F2F2F2")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            format_run(r, size_pt=11.5, bold=True)
        else:
            if c_idx in [0, 2, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            if c_idx == 1:
                r = p.add_run(text)
                format_run(r, size_pt=11.5, bold=True)
            else:
                r = p.add_run(text)
                format_run(r, size_pt=11)

p_sep2 = doc.add_paragraph()
p_sep2.paragraph_format.space_before = Pt(4)
p_sep2.paragraph_format.space_after = Pt(4)

# III. QUY TRÌNH THỰC HIỆN VÀ HỒ SƠ LƯU THƯ VIỆN
p_sec3 = add_p(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
r = p_sec3.add_run("III. QUY TRÌNH THỰC HIỆN VÀ HỒ SƠ LƯU THƯ VIỆN")
format_run(r, size_pt=13, bold=True)

steps = [
    ("1. Bước 1: Đăng ký với Bộ phận Thư viện", "Giáo viên điền Phiếu đăng ký, gửi Thư viện trước ngày dạy tối thiểu 03 ngày để cán bộ thư viện chuẩn bị phòng đọc, bật màn hình Tivi, kiểm tra cổng HDMI kết nối Laptop và đường truyền cáp quang/Wifi truy cập DlibK12."),
    ("2. Bước 2: Soạn và Phê duyệt KHBD (Giáo án)", "Giáo viên xây dựng KHBD theo khung Công văn 5512/BGDĐT-GDTrH. Thiết kế rõ hoạt động của học sinh khi xem video bài giảng số, thao tác trên DlibK12, thảo luận nhóm; tích hợp Khung Năng lực số (NLS), Khung AI (in đậm, in nghiêng rõ nét). KHBD phải được Tổ trưởng chuyên môn ký duyệt và Ban Giám hiệu phê duyệt trước khi lên lớp."),
    ("3. Bước 3: Tổ chức tiết dạy", "Thực hiện đúng thời lượng và kế hoạch bài học tại phòng Thư viện. Quản lý việc truy cập mạng của học sinh đúng mục đích học tập."),
    ("4. Bước 4: Hoàn tất và bàn giao hồ sơ", "Sau khi hoàn thành tiết dạy, giáo viên tổng hợp và bàn giao 01 bộ hồ sơ chuyên môn hoàn chỉnh cho Cán bộ Thư viện gồm: (1) Phiếu đăng ký có xác nhận; (2) Bản in KHBD đã có đầy đủ chữ ký duyệt của TTCM và BGH; (3) Minh chứng sản phẩm học tập số hoặc phiếu học tập của học sinh.")
]

for title, desc in steps:
    p = add_p(doc, indent=0.5, space_before=2, space_after=2)
    r1 = p.add_run(title + ": ")
    format_run(r1, size_pt=13, bold=True)
    r2 = p.add_run(desc)
    format_run(r2, size_pt=13)

# IV. ĐIỀU KHOẢN THI ĐUA VÀ TỔ CHỨC THỰC HIỆN
p_sec4 = add_p(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
r = p_sec4.add_run("IV. ĐIỀU KHOẢN THI ĐUA VÀ TỔ CHỨC THỰC HIỆN")
format_run(r, size_pt=13, bold=True)

p = add_p(doc, indent=0.5)
r = p.add_run("- Việc hoàn thành đúng tiến độ tiết dạy Thư viện và nộp đầy đủ hồ sơ minh chứng là tiêu chí bắt buộc trong đánh giá xếp loại chuyên môn và bình xét thi đua tháng 11, tháng 12 năm 2026 của giáo viên trong tổ.")
format_run(r, size_pt=13)
p = add_p(doc, indent=0.5)
r = p.add_run("- Trong quá trình thực hiện, nếu có sự thay đổi đột xuất về thời khóa biểu hoặc sự cố kỹ thuật đường truyền, giáo viên chủ động báo trước với Tổ trưởng chuyên môn và Cán bộ Thư viện để sắp xếp lịch bù phù hợp.")
format_run(r, size_pt=13)

p_sep3 = doc.add_paragraph()
p_sep3.paragraph_format.space_before = Pt(8)
p_sep3.paragraph_format.space_after = Pt(8)

# Signatures (2 columns)
tbl_sig = doc.add_table(rows=1, cols=2)
tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_sig.autofit = False
tbl_sig.columns[0].width = Mm(85)
tbl_sig.columns[1].width = Mm(85)

c_sig_l = tbl_sig.cell(0, 0)
p_sl = c_sig_l.paragraphs[0]
p_sl.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sl.paragraph_format.space_before = Pt(0)
p_sl.paragraph_format.space_after = Pt(2)
p_sl.paragraph_format.line_spacing = 1.0
r = p_sl.add_run("BAN GIÁM HIỆU PHÊ DUYỆT\n")
format_run(r, size_pt=13, bold=True)
r = p_sl.add_run("HIỆU TRƯỞNG\n\n\n\n\n")
format_run(r, size_pt=12.5, italic=True)
r = p_sl.add_run("Bùi Ngọc Nam")
format_run(r, size_pt=13, bold=True)

c_sig_r = tbl_sig.cell(0, 1)
p_sr = c_sig_r.paragraphs[0]
p_sr.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sr.paragraph_format.space_before = Pt(0)
p_sr.paragraph_format.space_after = Pt(2)
p_sr.paragraph_format.line_spacing = 1.0
r = p_sr.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n\n\n\n\n\n")
format_run(r, size_pt=13, bold=True)
r = p_sr.add_run("Hoàng Tấn Thiên")
format_run(r, size_pt=13, bold=True)

for row in tbl_sig.rows:
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)

# Section break for Phụ lục Phiếu đăng ký (Trang 2)
doc.add_page_break()

p_app_title = doc.add_paragraph()
p_app_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_app_title.paragraph_format.space_before = Pt(6)
p_app_title.paragraph_format.space_after = Pt(2)
r = p_app_title.add_run("PHỤ LỤC: BIỂU MẪU ĐĂNG KÝ TIẾT HỌC THƯ VIỆN SỐ\n")
format_run(r, size_pt=13, bold=True)
r = p_app_title.add_run("(Ban hành kèm theo Kế hoạch số 09/KH-TTIN ngày 05/11/2026 của Tổ Toán – Tin học)")
format_run(r, size_pt=12, italic=True)

p_space = doc.add_paragraph()
p_space.paragraph_format.space_before = Pt(6)
p_space.paragraph_format.space_after = Pt(6)

# Header Phiếu
tbl_phieu_h = doc.add_table(rows=1, cols=2)
tbl_phieu_h.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_phieu_h.autofit = False
tbl_phieu_h.columns[0].width = Mm(65)
tbl_phieu_h.columns[1].width = Mm(100)

p1 = tbl_phieu_h.cell(0, 0).paragraphs[0]
p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p1.paragraph_format.space_before = Pt(0)
p1.paragraph_format.space_after = Pt(1)
p1.paragraph_format.line_spacing = 1.0
r = p1.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
format_run(r, size_pt=12, bold=False)
r = p1.add_run("TỔ TOÁN – TIN HỌC")
format_run(r, size_pt=12, bold=True)

p2 = tbl_phieu_h.cell(0, 1).paragraphs[0]
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p2.paragraph_format.space_before = Pt(0)
p2.paragraph_format.space_after = Pt(1)
p2.paragraph_format.line_spacing = 1.0
r = p2.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
format_run(r, size_pt=12, bold=True)
r = p2.add_run("Độc lập – Tự do – Hạnh phúc")
format_run(r, size_pt=13, bold=True)

for row in tbl_phieu_h.rows:
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)

p_phieu_name = doc.add_paragraph()
p_phieu_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_phieu_name.paragraph_format.space_before = Pt(12)
p_phieu_name.paragraph_format.space_after = Pt(4)
r = p_phieu_name.add_run("PHIẾU ĐĂNG KÝ TIẾT HỌC TẠI THƯ VIỆN\n")
format_run(r, size_pt=14, bold=True)
r = p_phieu_name.add_run("(Ứng dụng Thư viện số DlibK12 — Học kỳ I, Năm học 2026 - 2027)")
format_run(r, size_pt=12.5, italic=True)

fields = [
    "1. Họ và tên giáo viên đăng ký: ..........................................................................................................",
    "2. Giảng dạy bộ môn: ................................................ Lớp dạy: ................. Sĩ số học sinh: ........ em.",
    "3. Tuần thực hiện: Tuần ...........; Tiết PPCT: .........; Ngày dạy dự kiến: ..... / ..... / 2026 (Buổi: ...........).",
    "4. Tên bài dạy / Chủ đề: ......................................................................................................................",
    "...........................................................................................................................................................",
    "5. Nhu cầu hỗ trợ cơ sở vật chất & Thiết bị thư viện số:",
    "   [ X ] Màn hình Tivi tương tác kết nối Laptop giáo viên (Cổng HDMI / Dây nối)",
    "   [ X ] Đường truyền Internet cáp quang / Wifi Thư viện phục vụ truy cập CSDL DlibK12",
    "   [   ] Hệ thống máy tính/laptop phòng đọc cho học sinh thực hành",
    "   [   ] Khác (compa kỹ thuật lớn, thước cuộn, thiết bị STEM...): .............................................",
    "6. Tài nguyên số khai thác trên CSDL DlibK12:",
    "   - Học liệu bài giảng số / Video mô phỏng: .............................................................................",
    "   - Ngân hàng bài tập tương tác / E-book SGK: ........................................................................",
    "7. Kế hoạch bài dạy (KHBD) kèm theo: Đã được phê duyệt đầy đủ theo quy định."
]

for f_text in fields:
    p = add_p(doc, space_before=2, space_after=2, indent=0.25)
    r = p.add_run(f_text)
    format_run(r, size_pt=12.5)

p_sep4 = doc.add_paragraph()
p_sep4.paragraph_format.space_before = Pt(8)
p_sep4.paragraph_format.space_after = Pt(8)

# Signatures for Phiếu (3 columns)
tbl_p_sig = doc.add_table(rows=1, cols=3)
tbl_p_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_p_sig.autofit = False
tbl_p_sig.columns[0].width = Mm(55)
tbl_p_sig.columns[1].width = Mm(55)
tbl_p_sig.columns[2].width = Mm(55)

sig_titles = [
    ("BỘ PHẬN THƯ VIỆN\n(Bố trí Tivi, mạng & phòng)", "(Ký và ghi rõ họ tên)\n\n\n\n\n................................................"),
    ("TỔ TRƯỞNG CHUYÊN MÔN\n(Duyệt kế hoạch)", "(Ký và ghi rõ họ tên)\n\n\n\n\nHoàng Tấn Thiên"),
    ("GIÁO VIÊN ĐĂNG KÝ\n(Cam kết thực hiện)", "(Ký và ghi rõ họ tên)\n\n\n\n\n................................................")
]

for idx, (t1, t2) in enumerate(sig_titles):
    cell = tbl_p_sig.cell(0, idx)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0
    r1 = p.add_run(t1 + "\n")
    format_run(r1, size_pt=12, bold=True)
    r2 = p.add_run(t2)
    format_run(r2, size_pt=11.5, italic=True)

for row in tbl_p_sig.rows:
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)

doc.save(docx_path)
print(f"File updated with DlibK12 successfully: {docx_path}")
