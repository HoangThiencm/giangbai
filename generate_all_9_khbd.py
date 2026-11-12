# -*- coding: utf-8 -*-
"""Script sinh toàn bộ 09 Kế hoạch bài dạy (KHBD) tiết dạy Thư viện số
cho Tổ Toán - Tin học Trường THCS Trần Phú
Chuẩn Công văn 5512/BGDĐT-GDTrH, khai thác CSDL Thư viện số DlibK12 (Tivi + Laptop)
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from TROLYTHIEN.engine.word_math_helper import latex_to_omml

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
    tblPr = table._tbl.tblPr
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

def add_math(paragraph, latex_expr):
    """Chèn công thức Word Equation OMML chuẩn"""
    try:
        omml = latex_to_omml(latex_expr)
        paragraph._element.append(omml)
    except Exception:
        r = paragraph.add_run(latex_expr)
        format_run(r, italic=True)

out_dir = r"C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\1_SOAN_KHBD\Ket_qua\05.11"
os.makedirs(out_dir, exist_ok=True)

lessons_data = [
    {
        "filename": "KHBD_01_Hoang_Tan_Thien_Toan_9.docx",
        "gv": "Hoàng Tấn Thiên",
        "mon": "TOÁN 9",
        "lop": "9/2 (hoặc 9/1)",
        "tuan": "Tuần 11",
        "tiet": "Tiết 27",
        "bai": "BÀI 8: KHAI CĂN BẬC HAI VỚI PHÉP NHÂN VÀ PHÉP CHIA\n(TIẾT HỌC THƯ VIỆN SỐ — LUYỆN TẬP ỨNG DỤNG THỰC TẾ)",
        "muc_tieu_kien_thuc": "Vận dụng thành thạo quy tắc khai phương một tích và quy tắc nhân các căn bậc hai; khai phương một thương và quy tắc chia các căn bậc hai để rút gọn biểu thức, tính giá trị và giải quyết bài toán thực tế hình học.",
        "nls_ai": "NLS 1.1: Khai thác CSDL Thư viện số DlibK12 để xem video ứng dụng hình học của căn bậc hai; NLS 2.2: Hợp tác giải toán nhóm và trình bày kết quả qua Màn hình Tivi Thư viện; Khung AI: Ứng dụng công cụ kiểm chứng kết quả rút gọn đại số có sự hướng dẫn của giáo viên.",
        "hoc_lieu": "Màn hình Tivi tương tác phòng đọc Thư viện; Laptop giáo viên kết nối Internet; Tài khoản DlibK12; SGK Toán 9 Tập 1 (bộ Kết nối tri thức); Phiếu học tập nhóm.",
        "hoat_dong_1": "Khởi động: Xem video ngắn 3 phút trên DlibK12 về ứng dụng công thức tính vận tốc rơi tự do v = √(2gh) và diện tích tam giác theo công thức Heron.",
        "hoat_dong_2": "Khám phá & Tương tác DlibK12: GV trình chiếu trên Tivi Thư viện bài giảng số DlibK12. HS quan sát các bước khai phương tích và thương. Thảo luận nhóm 4 HS giải bài tập số 1, 2.",
        "hoat_dong_3": "Luyện tập: HS làm việc nhóm trên Phiếu học tập; GV gọi đại diện nhóm lên bảng tương tác Tivi Thư viện điền kết quả rút gọn căn thức.",
        "hoat_dong_4": "Vận dụng & Nộp sản phẩm: Giải bài toán thực tế tính bán kính đường ống dẫn nước; nộp Phiếu học tập nhóm về bàn Thư viện lưu hồ sơ."
    },
    {
        "filename": "KHBD_02_Duong_Quang_Tung_Tin_6.docx",
        "gv": "Dương Quang Tùng",
        "mon": "TIN HỌC 6",
        "lop": "6/3 (hoặc 6/2, 8/1)",
        "tuan": "Tuần 13",
        "tiet": "Tiết 13",
        "bai": "BÀI 7: THỰC HÀNH: TÌM KIẾM THÔNG TIN TRÊN INTERNET VÀ THƯ VIỆN SỐ\n(TIẾT HỌC THƯ VIỆN SỐ DLIBK12)",
        "muc_tieu_kien_thuc": "Biết sử dụng công cụ tìm kiếm trên Internet và hệ thống Thư viện số DlibK12; biết lựa chọn từ khóa thích hợp; đánh giá tính tin cậy của thông tin tìm được.",
        "nls_ai": "NLS 1.2: Đánh giá dữ liệu, thông tin và nội dung số; NLS 1.1: Tìm kiếm, lọc và phân loại tài liệu số trên DlibK12; Khung AI: Nhận diện cơ chế gợi ý tìm kiếm thông minh và thuật toán tìm kiếm từ khóa an toàn.",
        "hoc_lieu": "Màn hình Tivi Thư viện; Laptop GV; Hệ thống máy tính phòng đọc Thư viện có kết nối mạng; Tài khoản DlibK12 của học sinh; SGK Tin học 6.",
        "hoat_dong_1": "Khởi động: Đặt câu hỏi tình huống: 'Làm thế nào để tìm được quyển sách hoặc tài liệu học tập chính xác nhất trên hệ thống thư viện trực tuyến trong vòng 30 giây?'.",
        "hoat_dong_2": "Khám phá & Thao tác mẫu: GV dùng Laptop kết nối Tivi hướng dẫn trực tiếp giao diện CSDL DlibK12; cách tìm theo tác giả, tên sách, mã số ISBN và từ khóa chủ đề.",
        "hoat_dong_3": "Thực hành trên máy: HS đăng nhập tài khoản DlibK12 cá nhân/nhóm, thực hành tìm kiếm 03 tài liệu số về chủ đề 'Văn hóa đọc học đường' và 'Kỹ năng an toàn mạng'.",
        "hoat_dong_4": "Vận dụng & Nộp sản phẩm: Tổng hợp danh mục tài liệu tìm được thành tệp Word/PDF nhỏ gửi về tài khoản Thư viện số để lưu hồ sơ minh chứng."
    },
    {
        "filename": "KHBD_03_Nguyen_Thi_Thao_Toan_6.docx",
        "gv": "Nguyễn Thị Thảo",
        "mon": "TOÁN 6",
        "lop": "6/2 (hoặc 6/5, 7/5)",
        "tuan": "Tuần 11",
        "tiet": "Tiết 21",
        "bai": "BÀI 19: HÌNH CHỮ NHẬT, HÌNH THOI, HÌNH BÌNH HÀNH\n(TIẾT HỌC THƯ VIỆN SỐ — STEM TẤM THIỆP HÌNH HỌC TRANG TRÍ THƯ VIỆN)",
        "muc_tieu_kien_thuc": "Nhận biết và mô tả được các yếu tố cơ bản (cạnh, góc, đường chéo) của hình chữ nhật, hình thoi, hình bình hành. Ứng dụng tính đối xứng và hình dạng để thiết kế tấm thiệp hình học.",
        "nls_ai": "NLS 3.1: Phát triển nội dung số và sản phẩm sáng tạo từ hình học trực quan; NLS 2.1: Tương tác qua công nghệ số; Khung AI: Quan sát ứng dụng nhận diện mẫu hình học đối xứng trong thiết kế đồ họa.",
        "hoc_lieu": "Màn hình Tivi Thư viện; Laptop GV; Video mô phỏng hình học phẳng trên DlibK12; SGK Toán 6 Tập 1; Giấy màu, kéo, keo dán, thước kẻ, bút màu.",
        "hoat_dong_1": "Khởi động: Xem video 2 phút trên DlibK12 giới thiệu kiến trúc hoa văn và tranh trang trí góc đọc sách thư viện có sử dụng hình chữ nhật, hình thoi, hình bình hành.",
        "hoat_dong_2": "Hình thành kiến thức & Khám phá DlibK12: GV trình chiếu mô hình động các hình phẳng trên Tivi. HS quan sát tính chất đường chéo và các cạnh đối song song, bằng nhau.",
        "hoat_dong_3": "Luyện tập & Thực hành STEM: HS chia nhóm 4-6 em, dùng giấy màu cắt dán tấm thiệp trang trí có kết hợp tối thiểu 2 trong 3 hình đã học.",
        "hoat_dong_4": "Vận dụng & Trưng bày: Trưng bày tấm thiệp tại Góc đọc sách Thư viện; chụp ảnh sản phẩm lưu chiểu hồ sơ chuyên môn thư viện."
    },
    {
        "filename": "KHBD_04_Le_Thi_Binh_Toan_8.docx",
        "gv": "Lê Thị Bình",
        "mon": "TOÁN 8",
        "lop": "8/1 (hoặc 7/1, 8/2)",
        "tuan": "Tuần 12",
        "tiet": "Tiết 24",
        "bai": "BÀI 15: ĐỊNH LÍ THALÈS TRONG TAM GIÁC\n(TIẾT HỌC THƯ VIỆN SỐ — LUYỆN TẬP ỨNG DỤNG THỰC TẾ)",
        "muc_tieu_kien_thuc": "Nắm vững định lí Thalès thuận, định lí Thalès đảo và hệ quả. Vận dụng tính tỉ số đoạn thẳng và tính độ dài đoạn thẳng trong các bài toán thực tế.",
        "nls_ai": "NLS 1.1: Tra cứu mô phỏng hình học tương tác trên DlibK12; NLS 3.2: Tích hợp công nghệ mô phỏng GeoGebra số; Khung AI: Sử dụng công cụ số kiểm tra tính tỉ lệ đoạn thẳng tự động.",
        "hoc_lieu": "Màn hình Tivi Thư viện; Laptop GV kết nối DlibK12; Tệp mô phỏng Thalès nhúng trên DlibK12; SGK Toán 8 Tập 1; Phiếu học tập nhóm.",
        "hoat_dong_1": "Khởi động: Chiếu tư liệu lịch sử trên DlibK12: 'Nhà toán học Thalès đo chiều cao kim tự tháp Ai Cập bằng bóng nắng như thế nào?'.",
        "hoat_dong_2": "Khám phá mô phỏng DlibK12: GV thao tác trên Tivi di chuyển đường thẳng song song với cạnh tam giác, HS quan sát sự biến thiên của độ dài và tỉ số đoạn thẳng luôn không đổi.",
        "hoat_dong_3": "Luyện tập: Các nhóm làm bài tập tính khoảng cách hai điểm bị ngăn cách bởi hồ nước dựa trên tỉ lệ hình vẽ trên Tivi.",
        "hoat_dong_4": "Vận dụng & Nộp hồ sơ: Lập sơ đồ tư duy tóm tắt hệ quả định lí Thalès; nộp phiếu học tập nhóm về bộ phận Thư viện."
    },
    {
        "filename": "KHBD_05_Hoang_Xuan_Anh_Toan_7.docx",
        "gv": "Hoàng Xuân Ánh",
        "mon": "TOÁN 7",
        "lop": "7/2 (hoặc 7/3, 7/4)",
        "tuan": "Tuần 11",
        "tiet": "Tiết 29",
        "bai": "BÀI 10: TIÊN ĐỀ EUCLID VÀ TÍNH CHẤT HAI ĐƯỜNG THẲNG SONG SONG\n(TIẾT HỌC THƯ VIỆN SỐ — TRỰC QUAN HÓA TOÁN HỌC)",
        "muc_tieu_kien_thuc": "Hiểu nội dung tiên đề Euclid về đường thẳng song song; nhận biết và chứng minh các cặp góc so le trong bằng nhau, đồng vị bằng nhau khi một đường thẳng cắt hai đường thẳng song song.",
        "nls_ai": "NLS 1.1: Khai thác hình học 3D tương tác trên DlibK12; NLS 2.2: Chia sẻ và phản biện kết quả qua màn hình lớn Thư viện; Khung AI: Tiếp cận mô hình nhận diện góc thực tế trong kiến trúc xây dựng.",
        "hoc_lieu": "Màn hình Tivi Thư viện; Laptop GV; Trình mô phỏng góc song song trên DlibK12; SGK Toán 7 Tập 1; Phiếu học tập.",
        "hoat_dong_1": "Khởi động: Chiếu hình ảnh các thanh ray đường sắt và dây cáp cầu treo trên Tivi Thư viện; đặt câu hỏi: 'Vì sao các thanh ray tàu hỏa không bao giờ cắt nhau?'.",
        "hoat_dong_2": "Hình thành kiến thức trên DlibK12: GV mở tệp tương tác DlibK12, đo góc so le trong và đồng vị khi xoay đường thẳng cắt; HS ghi nhận quy luật.",
        "hoat_dong_3": "Luyện tập: Thực hiện phiếu bài tập trắc nghiệm số trên DlibK12; các nhóm giơ bảng đáp án và giải thích trên màn hình Tivi.",
        "hoat_dong_4": "Vận dụng: Vẽ sơ đồ ứng dụng đường thẳng song song trong thực tế đời sống; nộp bài thu hoạch nhóm lưu hồ sơ Thư viện."
    },
    {
        "filename": "KHBD_06_Tran_Long_Hai_Toan_8.docx",
        "gv": "Trần Long Hải",
        "mon": "TOÁN 8",
        "lop": "8/4 (hoặc 8/3, 8/5)",
        "tuan": "Tuần 10",
        "tiet": "Tiết 18",
        "bai": "BÀI 15: ĐỊNH LÍ THALÈS TRONG TAM GIÁC\n(TIẾT HỌC THƯ VIỆN SỐ — STEM ĐO BÓNG NẮNG VÀ CHIỀU CAO CỌC TIÊU)",
        "muc_tieu_kien_thuc": "Vận dụng kiến thức tam giác và định lí Thalès để đo gián tiếp chiều cao vật thể không tới được đỉnh (cột cờ, tòa nhà thư viện).",
        "nls_ai": "NLS 3.1: Xử lý số liệu thực nghiệm trên bảng tính số; NLS 1.1: Xem video hướng dẫn quy trình đo kỹ thuật trên DlibK12; Khung AI: Nhận diện sai số quang học và bóng đổ do ánh sáng mặt trời.",
        "hoc_lieu": "Màn hình Tivi Thư viện; Laptop GV; Video kỹ thuật đo đạc ngoài trời DlibK12; Thước cuộn 10m; Cọc tiêu 1.5m; SGK Toán 8.",
        "hoat_dong_1": "Khởi động: Xem clip 3 phút trên DlibK12 mô phỏng các kỹ sư đo đạc công trình bằng cọc ngắm và bóng nắng.",
        "hoat_dong_2": "Khám phá kỹ thuật đo: GV chiếu sơ đồ hình học trên Tivi Thư viện; phân tích tam giác đồng dạng và định lí Thalès ứng dụng cho bóng nắng.",
        "hoat_dong_3": "Thực hành đo mẫu: Đo chiều cao tủ sách Thư viện bằng cọc ngắm và bóng đèn trần; tính toán số liệu trên phiếu học tập nhóm.",
        "hoat_dong_4": "Vận dụng: Hoàn thiện bảng tường trình đo đạc thực nghiệm; nộp 01 bản cho Thư viện lưu minh chứng hồ sơ chuyên môn."
    },
    {
        "filename": "KHBD_07_Tran_Sang_Toan_9.docx",
        "gv": "Trần Sáng",
        "mon": "TOÁN 9",
        "lop": "9/5 (hoặc 9/6, 9/7)",
        "tuan": "Tuần 11",
        "tiet": "Tiết 15",
        "bai": "BÀI 15: ĐỘ DÀI CUNG TRÒN, DIỆN TÍCH HÌNH QUẠT TRÒN VÀ VÀNH KHUYÊN\n(TIẾT HỌC THƯ VIỆN SỐ — STEM QUẠT GIẤY NGHỆ THUẬT)",
        "muc_tieu_kien_thuc": "Hiểu và áp dụng chính xác công thức tính độ dài cung tròn C = πRn/180 và diện tích hình quạt tròn S = πR²n/360, diện tích hình vành khuyên.",
        "nls_ai": "NLS 1.1: Tra cứu học liệu hoạt hình mô phỏng quạt tròn trên DlibK12; NLS 3.1: Thiết kế mô hình số và bản vẽ kỹ thuật; Khung AI: Ứng dụng mô hình tính toán vật liệu tối ưu trong thiết kế công nghiệp.",
        "hoc_lieu": "Màn hình Tivi Thư viện; Laptop GV; Hoạt hình mô phỏng DlibK12; Compa kỹ thuật; Giấy thủ công, que nan; SGK Toán 9 Tập 1.",
        "hoat_dong_1": "Khởi động: Chiếu hình ảnh các công trình kiến trúc mái vòm, cầu xoay hình quạt trên Tivi Thư viện kết nối DlibK12.",
        "hoat_dong_2": "Hình thành kiến thức: Quan sát mô phỏng chuyển động góc n độ của bán kính R quét nên diện tích quạt tròn trên Tivi; thiết lập công thức toán học.",
        "hoat_dong_3": "Luyện tập: Tính độ dài cung tròn và diện tích quạt giấy với bán kính R = 20cm và góc mở n = 120°.",
        "hoat_dong_4": "Vận dụng STEM: Hoàn thiện mô hình quạt nghệ thuật kèm bảng tính diện tích giấy sử dụng; trưng bày tại Thư viện và bàn giao hồ sơ lưu."
    },
    {
        "filename": "KHBD_08_Ho_Dang_Danh_Toan_6.docx",
        "gv": "Hồ Đăng Danh",
        "mon": "TOÁN 6",
        "lop": "6/3 (hoặc 6/4, 9/3)",
        "tuan": "Tuần 13",
        "tiet": "Tiết 49",
        "bai": "HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM:\nSỬ DỤNG MÁY TÍNH CẦM TAY GIẢI TOÁN THỰC TẾ\n(TIẾT HỌC THƯ VIỆN SỐ DLIBK12)",
        "muc_tieu_kien_thuc": "Thành thạo các phím chức năng cơ bản, phím ngoặc, tính lũy thừa, tính căn bậc hai và phân số trên máy tính cầm tay; biết vận dụng giải nhanh bài toán thực tế.",
        "nls_ai": "NLS 1.1: Sử dụng phần mềm giả lập máy tính điện tử trên DlibK12; NLS 3.2: Tự động hóa quy trình tính toán số học; Khung AI: Hiểu nguyên lý xử lý phép tính của vi xử lý số.",
        "hoc_lieu": "Màn hình Tivi Thư viện; Laptop GV cài phần mềm giả lập máy tính Casio; Ngân hàng bài toán số học thực tế trên DlibK12; Máy tính cầm tay cá nhân của HS; SGK Toán 6.",
        "hoat_dong_1": "Khởi động: Trò chơi 'Ai nhanh hơn': GV chiếu phép tính phức tạp trên Tivi Thư viện, HS so tài bấm máy tính tìm kết quả.",
        "hoat_dong_2": "Khám phá quy trình: GV thao tác trên phần mềm giả lập chiếu màn hình Tivi phóng to bàn phím máy tính; hướng dẫn thứ tự thực hiện các phím nhớ và phím hàm.",
        "hoat_dong_3": "Thực hành nhóm: Giải các bài toán thực tế về tiền điện nước, tính lãi suất gửi tiết kiệm bằng máy tính; đối chiếu đáp án với hệ thống DlibK12.",
        "hoat_dong_4": "Vận dụng: Làm bài kiểm tra tính nhanh 5 câu trên DlibK12; in bảng điểm tổng hợp nộp lưu hồ sơ Thư viện."
    },
    {
        "filename": "KHBD_09_Nguyen_Van_Tinh_HDTN_6.docx",
        "gv": "Nguyễn Văn Tính",
        "mon": "HOẠT ĐỘNG TRẢI NGHIỆM 6",
        "lop": "6/2 (hoặc 6/5, 7/5)",
        "tuan": "Tuần 11",
        "tiet": "Tiết 32",
        "bai": "CHỦ ĐỀ 3: XÂY DỰNG NỀN NẾP TỰ HỌC VÀ RÈN LUYỆN KỸ NĂNG ĐỌC SÁCH\n(TIẾT TRẢI NGHIỆM TẠI THƯ VIỆN SỐ DLIBK12)",
        "muc_tieu_kien_thuc": "Rèn luyện kỹ năng tự học, hình thành thói quen đọc sách hàng ngày; biết cách quản lý thời gian và khai thác hiệu quả kho tài nguyên số DlibK12.",
        "nls_ai": "NLS 1.1: Khai thác sách điện tử (E-book) trên DlibK12; NLS 4.1: Xây dựng thói quen số lành mạnh, cân bằng giữa màn hình và đời sống; Khung AI: Tiếp cận công cụ trợ lý gợi ý sách đọc theo sở thích cá nhân.",
        "hoc_lieu": "Màn hình Tivi Thư viện; Laptop GV; Kho sách điện tử kỹ năng sống trên DlibK12; Sổ tay đọc sách cá nhân (mẫu KWL); SGK Hoạt động trải nghiệm 6.",
        "hoat_dong_1": "Khởi động: Chiếu video truyền cảm hứng 3 phút: 'Đọc sách để trưởng thành' từ kho tư liệu DlibK12 lên màn hình Tivi Thư viện.",
        "hoat_dong_2": "Khám phá Thư viện số: GV hướng dẫn HS cách đăng nhập DlibK12, chọn danh mục 'Sách kỹ năng - Phát triển bản thân'; HS chọn 1 mẩu chuyện ngắn để đọc lướt.",
        "hoat_dong_3": "Thực hành ghi chép: HS ghi vào Sổ tay đọc sách số theo mô hình KWL (Điều em đã biết - Điều em muốn biết - Điều em học được sau khi đọc).",
        "hoat_dong_4": "Vận dụng & Cam kết: Chia sẻ cảm nhận trước lớp qua micro Thư viện; ký bản Cam kết văn hóa đọc và nộp sổ tay lưu hồ sơ Thư viện."
    }
]

for idx, data in enumerate(lessons_data, 1):
    doc = Document()
    
    # Page setup A4
    for s in doc.sections:
        s.page_width = Mm(210)
        s.page_height = Mm(297)
        s.top_margin = Mm(20)
        s.bottom_margin = Mm(20)
        s.left_margin = Mm(30)
        s.right_margin = Mm(15)
        
    # Header Table
    tbl_h = doc.add_table(rows=1, cols=2)
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_h.autofit = False
    tbl_h.columns[0].width = Mm(65)
    tbl_h.columns[1].width = Mm(100)

    p1 = tbl_h.cell(0, 0).paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.line_spacing = 1.0
    r = p1.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    format_run(r, size_pt=12, bold=False)
    r = p1.add_run("TỔ TOÁN – TIN HỌC")
    format_run(r, size_pt=12, bold=True)

    p2 = tbl_h.cell(0, 1).paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.line_spacing = 1.0
    r = p2.add_run("KẾ HOẠCH BÀI DẠY (TIẾT HỌC THƯ VIỆN SỐ)\n")
    format_run(r, size_pt=12, bold=True)
    r = p2.add_run(f"Môn: {data['mon']} — Khối lớp: {data['lop']}\n")
    format_run(r, size_pt=11.5, bold=False)
    r = p2.add_run(f"Thời lượng: 01 tiết (45 phút) — {data['tuan']}")
    format_run(r, size_pt=11.5, italic=True)

    for row in tbl_h.rows:
        for cell in row.cells:
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>'
                f'</w:tcBorders>'
            )
            cell._tc.get_or_add_tcPr().append(tcBorders)

    # Line separator
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(4)
    p_sep.paragraph_format.space_after = Pt(6)

    # Lesson Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(2)
    r = p_title.add_run(f"{data['bai']}\n")
    format_run(r, size_pt=13.5, bold=True)
    r = p_title.add_run(f"Tiết PPCT: {data['tiet']} — Giáo viên thực hiện: {data['gv']}")
    format_run(r, size_pt=12.5, italic=True)

    # I. MỤC TIÊU
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
    r = p.add_run("I. MỤC TIÊU BÀI HỌC")
    format_run(r, size_pt=13, bold=True)

    p = add_p(doc, indent=0.5)
    r = p.add_run("1. Về kiến thức: ")
    format_run(r, size_pt=13, bold=True)
    r = p.add_run(data["muc_tieu_kien_thuc"])
    format_run(r, size_pt=13)

    p = add_p(doc, indent=0.5)
    r = p.add_run("2. Về năng lực:")
    format_run(r, size_pt=13, bold=True)

    p = add_p(doc, indent=0.5)
    r = p.add_run("- Năng lực chung: ")
    format_run(r, size_pt=13, italic=True)
    r = p.add_run("Năng lực tự chủ và tự học (tự giác khai thác tài nguyên số trên DlibK12); năng lực giao tiếp và hợp tác (thảo luận nhóm qua màn hình Tivi tương tác).")
    format_run(r, size_pt=13)

    p = add_p(doc, indent=0.5)
    r = p.add_run("- Năng lực đặc thù: ")
    format_run(r, size_pt=13, italic=True)
    r = p.add_run("Tư duy và lập luận toán học, mô hình hóa toán học, giải quyết vấn đề toán học và kỹ năng công nghệ thông tin.")
    format_run(r, size_pt=13)

    p = add_p(doc, indent=0.5)
    r = p.add_run("- Tích hợp Năng lực số (NLS) và Trí tuệ nhân tạo (AI): ")
    format_run(r, size_pt=13, bold=True, italic=True)
    r = p.add_run(data["nls_ai"])
    format_run(r, size_pt=13, bold=True, italic=True)

    p = add_p(doc, indent=0.5)
    r = p.add_run("3. Về phẩm chất: ")
    format_run(r, size_pt=13, bold=True)
    r = p.add_run("Chăm chỉ, trung thực trong học tập, có ý thức giữ gìn tài sản chung và xây dựng văn hóa đọc, tự học trong môi trường số.")
    format_run(r, size_pt=13)

    # II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
    r = p.add_run("II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU (KHAI THÁC DLIBK12)")
    format_run(r, size_pt=13, bold=True)

    p = add_p(doc, indent=0.5)
    r = p.add_run("1. Giáo viên: ")
    format_run(r, size_pt=13, bold=True)
    r = p.add_run(data["hoc_lieu"])
    format_run(r, size_pt=13)

    p = add_p(doc, indent=0.5)
    r = p.add_run("2. Học sinh: ")
    format_run(r, size_pt=13, bold=True)
    r = p.add_run("Sách giáo khoa Kết nối tri thức bản in, sổ tay ghi chép học tập, dụng cụ học tập (compa, ê-ke, máy tính cầm tay, bút màu).")
    format_run(r, size_pt=13)

    # III. TIẾN TRÌNH DẠY HỌC
    p = add_p(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
    r = p.add_run("III. TIẾN TRÌNH DẠY HỌC (CHUẨN CÔNG VĂN 5512)")
    format_run(r, size_pt=13, bold=True)

    # 4 Activities
    acts = [
        ("1. HOẠT ĐỘNG 1: MỞ ĐẦU / KHỞI ĐỘNG (5 - 7 phút)",
         "Kích hoạt hứng thú học tập và tạo mâu thuẫn nhận thức cho học sinh.",
         data["hoat_dong_1"],
         "Câu trả lời của học sinh, sự hào hứng tham gia vào vấn đề bài học.",
         "GV trình chiếu trên Tivi Thư viện. HS quan sát và trả lời. GV nhận xét dẫn dắt vào bài mới."),
        ("2. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC / TƯƠNG TÁC DLIBK12 (18 - 20 phút)",
         "Học sinh tự chiếm lĩnh kiến thức thông qua quan sát mô phỏng và bài giảng số trên CSDL DlibK12.",
         data["hoat_dong_2"],
         "Ghi chép các kết luận kiến thức trọng tâm vào vở, lời giải sơ bộ của bài toán trên phiếu.",
         "Bước 1 (Chuyển giao): GV nêu nhiệm vụ học tập trên Tivi.\nBước 2 (Thực hiện): Các nhóm HS làm việc tại bàn đọc Thư viện.\nBước 3 (Báo cáo): Đại diện 1 nhóm trình bày trên Tivi tương tác.\nBước 4 (Kết luận): GV chuẩn hóa kiến thức."),
        ("3. HOẠT ĐỘNG 3: LUYỆN TẬP / THỰC HÀNH TƯƠNG TÁC (10 - 12 phút)",
         "Củng cố và khắc sâu kiến thức thông qua hệ thống bài tập thực hành trên màn hình Tivi và phiếu học tập.",
         data["hoat_dong_3"],
         "Kết quả bài làm trên Phiếu học tập nhóm, đáp án trả lời trên màn hình Tivi Thư viện.",
         "GV điều khiển ngân hàng bài tập DlibK12 trên Tivi. HS thực hiện cá nhân kết hợp nhóm. GV chữa bài trực tiếp."),
        ("4. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (5 - 7 phút)",
         "Vận dụng kiến thức vào bài toán thực tiễn; bàn giao hồ sơ lưu chiểu Thư viện theo Kế hoạch 115.",
         data["hoat_dong_4"],
         "Sản phẩm học tập hoàn chỉnh (Phiếu học tập nhóm / Bản tường trình / Mô hình sản phẩm) nộp lại Thư viện.",
         "GV giao nhiệm vụ liên hệ thực tế. HS hoàn thiện sản phẩm và bàn giao cho cán bộ Thư viện lưu hồ sơ.")
    ]

    for a_title, a_obj, a_content, a_prod, a_org in acts:
        p = add_p(doc, space_before=4, space_after=1)
        r = p.add_run(a_title)
        format_run(r, size_pt=13, bold=True)

        p = add_p(doc, indent=0.5, space_before=1, space_after=1)
        r = p.add_run("a) Mục tiêu: ")
        format_run(r, size_pt=12.5, bold=True)
        r = p.add_run(a_obj)
        format_run(r, size_pt=12.5)

        p = add_p(doc, indent=0.5, space_before=1, space_after=1)
        r = p.add_run("b) Nội dung: ")
        format_run(r, size_pt=12.5, bold=True)
        r = p.add_run(a_content)
        format_run(r, size_pt=12.5)

        p = add_p(doc, indent=0.5, space_before=1, space_after=1)
        r = p.add_run("c) Sản phẩm: ")
        format_run(r, size_pt=12.5, bold=True)
        r = p.add_run(a_prod)
        format_run(r, size_pt=12.5)

        p = add_p(doc, indent=0.5, space_before=1, space_after=2)
        r = p.add_run("d) Tổ chức thực hiện: ")
        format_run(r, size_pt=12.5, bold=True)
        r = p.add_run(a_org)
        format_run(r, size_pt=12.5)

    # Signature Table
    p_sep3 = doc.add_paragraph()
    p_sep3.paragraph_format.space_before = Pt(8)
    p_sep3.paragraph_format.space_after = Pt(8)

    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig.autofit = False
    tbl_sig.columns[0].width = Mm(85)
    tbl_sig.columns[1].width = Mm(85)

    c_sig_l = tbl_sig.cell(0, 0)
    p_sl = c_sig_l.paragraphs[0]
    p_sl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sl.paragraph_format.line_spacing = 1.0
    r = p_sl.add_run("PHÊ DUYỆT CỦA TỔ TRƯỞNG\n\n\n\n\n")
    format_run(r, size_pt=13, bold=True)
    r = p_sl.add_run("Hoàng Tấn Thiên")
    format_run(r, size_pt=13, bold=True)

    c_sig_r = tbl_sig.cell(0, 1)
    p_sr = c_sig_r.paragraphs[0]
    p_sr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sr.paragraph_format.line_spacing = 1.0
    r = p_sr.add_run("GIÁO VIÊN BIÊN SOẠN\n\n\n\n\n")
    format_run(r, size_pt=13, bold=True)
    r = p_sr.add_run(data["gv"])
    format_run(r, size_pt=13, bold=True)

    for row in tbl_sig.rows:
        for cell in row.cells:
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>'
                f'</w:tcBorders>'
            )
            cell._tc.get_or_add_tcPr().append(tcBorders)

    file_path = os.path.join(out_dir, data["filename"])
    doc.save(file_path)
    print(f"[{idx}/9] Saved: {file_path}")

print("Successfully generated all 9 KHBD docx files!")
