# -*- coding: utf-8 -*-
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import lxml.etree as ET
from latex2mathml.converter import convert as latex2mathml_convert
import os

xslt_path = r'C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL'
xslt = ET.parse(xslt_path)
transform = ET.XSLT(xslt)

def latex_to_omml(latex_code):
    mml = latex2mathml_convert(latex_code)
    mml_tree = ET.fromstring(mml)
    omml_tree = transform(mml_tree)
    omml_str = ET.tostring(omml_tree, encoding='unicode')
    return parse_xml(omml_str)

def add_line_with_math(p, line, font_size=12, default_bold=False, default_italic=False, default_color=None):
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(0)
    
    parts = line.split('$')
    for idx, part in enumerate(parts):
        if not part:
            continue
        if idx % 2 == 1:
            try:
                omml_elem = latex_to_omml(part)
                p._p.append(omml_elem)
            except Exception as e:
                r = p.add_run(part)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_size)
        else:
            r = p.add_run(part)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            r.bold = default_bold
            r.italic = default_italic
            if default_color:
                r.font.color.rgb = default_color

def create_patched_syllabus():
    doc = Document()
    
    # Page setup A4
    for section in doc.sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(0.79)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # Header table
    tbl_header = doc.add_table(rows=1, cols=2)
    tbl_header.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_header.autofit = False
    cell_l, cell_r = tbl_header.rows[0].cells
    cell_l.width = Inches(3.2)
    cell_r.width = Inches(3.6)
    
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_l.add_run("TRƯỜNG THCS TRẦN PHÚ\nTỔ TOÁN - TIN\n")
    r.bold = True
    r.font.size = Pt(11)
    
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_r.add_run("ĐỀ CƯƠNG ÔN TẬP GIỮA KỲ I TOÁN 9\nNĂM HỌC: 2026 - 2027\n")
    r.bold = True
    r.font.size = Pt(11)
    r2 = p_r.add_run("(BẢN VÁ CHUẨN ĐÃ CHỈNH LÝ SƯ PHẠM)")
    r2.bold = True
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor(180, 40, 20)
    
    doc.add_paragraph()
    
    # I. DAI SO
    p_part1 = doc.add_paragraph()
    r = p_part1.add_run("I. ĐẠI SỐ")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    # Bai 1
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 1. Giải các phương trình sau:", default_bold=True)
    
    b1_items = [
        "a. $3x(2x - 5) = 0$",
        "b. $(x - 6)(3x + 4) = 0$",
        "c. $5x(x - 2) - 3x + 6 = 0$",
        "d. $(4x - 5)^2 - (x + 7)^2 = 0$",
        "e. $\\frac{2x - 3}{x - 1} + \\frac{3}{x} = 2$",
        "g. $\\frac{2x - 5}{x + 3} - \\frac{x + 1}{x - 3} = \\frac{x^2 + 9}{x^2 - 9}$",
        "h. $\\frac{x}{x + 3} - \\frac{2}{x - 1} = \\frac{x^2 + 9}{(x + 3)(x - 1)}$",
        "i. $\\frac{x - 1}{x - 3} - \\frac{x + 3}{x - 1} = \\frac{8x}{(x - 3)(x - 1)}$   [Lưu ý sư phạm: PT có nghiệm ngoại lai x = 1 vi phạm ĐKXĐ nên VÔ NGHIỆM]"
    ]
    for it in b1_items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        add_line_with_math(p, it)
        
    # Bai 2
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 2. Giải các bất phương trình sau:", default_bold=True)
    b2_items = [
        "a. $5x - 20 \\ge 0$",
        "b. $8x - 2 < 11x + 7$",
        "c. $5x - 7(2x - 5) < 2(x - 1)$"
    ]
    for it in b2_items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        add_line_with_math(p, it)
        
    # Bai 3 & 4
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 3. Trong các phương trình sau, phương trình nào là phương trình bậc nhất hai ẩn? Xác định hệ số a, b, c của các phương trình bậc nhất hai ẩn đó:", default_bold=True)
    b3_items = [
        "a. $3x + y = 5$",
        "b. $0x - 0y = 2$",
        "c. $4x + 0y = -3$",
        "d. $2x^2 + 3y = 1$"
    ]
    for it in b3_items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        add_line_with_math(p, it)
        
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 4. Trong các bất phương trình sau, bất phương trình nào là bất phương trình bậc nhất một ẩn (ẩn x)? Xác định hệ số a, b của các bất phương trình đó:", default_bold=True)
    b4_items = [
        "a. $3x^2 + 7 > 0$",
        "b. $0x + 1 \\ge 0$",
        "c. $4x + 3y < 0$",
        "d. $5x - 1 \\le 0$",
        "e. $-x \\ge 0$"
    ]
    for it in b4_items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        add_line_with_math(p, it)
        
    # Bai 5 & 6
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 5. Trong các cặp số sau, cặp số nào là nghiệm của hệ phương trình $\\begin{cases} 2x - 5y = -1 \\\\ 3x + y = 7 \\end{cases}$?", default_bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "A. $(3; -1)$                 B. $(2; 1)$")
    
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 6. Giải các hệ phương trình sau:", default_bold=True)
    b6_items = [
        "a. $\\begin{cases} 3x + y = 3 \\\\ 2x - y = 7 \\end{cases}$",
        "b. $\\begin{cases} 8x + 3y = 5 \\\\ 4x + y = 2 \\end{cases}$",
        "c. $\\begin{cases} 2x - y = 1 \\\\ 4x - 2y = 0 \\end{cases}$",
        "d. $\\begin{cases} 2x + 5y = 1 \\\\ 0,4x + y = 0,2 \\end{cases}$"
    ]
    for it in b6_items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        add_line_with_math(p, it)
        
    # Bai 7, 8, 9
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 7. Dùng các dấu $>, <, \\ge, \\le$ để diễn tả:", default_bold=True)
    b7_items = [
        "a. Giá bán thấp nhất T của một chiếc điện thoại là 6 triệu đồng.",
        "b. Nhiệt độ t ($^\\circ\\text{C}$) bảo quản của một loại sữa là dưới $4^\\circ\\text{C}$.",
        "c. Số người x của xe buýt chở được tối đa là 45 người."
    ]
    for it in b7_items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        add_line_with_math(p, it)
        
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 8. Hãy chỉ ra các bất đẳng thức diễn tả mỗi khẳng định sau:", default_bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "a. a nhỏ hơn 5           b. x không lớn hơn y           c. m nhỏ hơn hoặc bằng n")
    
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 9. Cho hai số a, b thỏa mãn $a > b$. Chứng minh:", default_bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "a. $2a + 1 > 2b + 1$           b. $5 - 3a < 5 - 3b$           c. $2a + 3 > 2b + 1$")
    
    # Bai 10
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 10. Giải các bài toán sau bằng cách lập hệ phương trình:", default_bold=True)
    b10_items = [
        "10.1. Hai xí nghiệp theo kế hoạch phải làm tổng cộng 360 công cụ. Nhờ sắp xếp hợp lý dây chuyền sản xuất nên xí nghiệp I đã vượt mức 12% kế hoạch, xí nghiệp II đã vượt mức 10% kế hoạch. Do đó cả xí nghiệp đã làm được 400 công cụ. Tính số công cụ mỗi xí nghiệp phải làm theo kế hoạch.",
        "10.2. Một mảnh vườn hình chữ nhật có chu vi là 64 m. Nếu tăng chiều rộng thêm 3 m và giảm chiều dài đi 2 m thì diện tích mảnh vườn tăng thêm $30\\text{ m}^2$. Tính diện tích ban đầu của mảnh vườn.",
        "10.3. Tại một quầy bán vé xem phim, ông An mua 5 vé người lớn và 3 vé trẻ em hết tất cả 840 000 đồng. Ông Nam mua 7 vé người lớn và 6 vé trẻ em hết 1 320 000 đồng. Tính giá tiền mỗi vé người lớn và mỗi vé trẻ em.",
        "10.4. Quãng đường AB dài 120 km. Một ô tô đi từ A đến B và một xe máy đi từ B đến A, xuất phát cùng lúc. Sau 2 giờ thì hai xe gặp nhau. Biết mỗi giờ ô tô đi nhanh hơn xe máy 10 km. Tính vận tốc của mỗi xe."
    ]
    for it in b10_items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        add_line_with_math(p, it)
        
    doc.add_paragraph()
    
    # II. HINH HOC
    p_part2 = doc.add_paragraph()
    r = p_part2.add_run("II. HÌNH HỌC")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 1.", default_bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "1. Hãy viết các tỉ số lượng giác sau thành tỉ số lượng giác của các góc nhỏ hơn $45^\\circ$:")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5)
    add_line_with_math(p, "a. $\\cos 69^\\circ$           b. $\\cot 83^\\circ$           c. $\\sin 77^\\circ$           d. $\\tan 51^\\circ$")
    
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "2. Không sử dụng máy tính cầm tay. Hãy tính giá trị biểu thức sau:")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5)
    add_line_with_math(p, "$A = 3\\cos 35^\\circ - 3\\sin 55^\\circ + \\frac{\\tan 70^\\circ}{\\cot 20^\\circ}$ ;       $B = \\tan 25^\\circ - \\cot 65^\\circ + 4\\frac{\\sin 80^\\circ}{\\cos 10^\\circ}$")
    
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "3. Tính giá trị các biểu thức sau [ĐÃ VÁ CHUẨN GÓC ĐẶC BIỆT]:")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5)
    add_line_with_math(p, "$A = \\cos 45^\\circ - \\sin 60^\\circ + \\frac{\\tan 30^\\circ}{\\cos 60^\\circ}$ ;       $B = \\tan 60^\\circ - \\sin 30^\\circ + \\frac{\\sin 45^\\circ \\cdot \\sin 60^\\circ}{\\tan 45^\\circ}$")
    
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 2. Tính các tỉ số lượng giác của góc nhọn C trong mỗi tam giác vuông ở Hình 1:", default_bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "a. $\\triangle ABC$ vuông tại B có $AB = 3, BC = 4, AC = 5$.")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "b. $\\triangle ABC$ vuông tại A có $AB = 2, AC = 3$.")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "c. $\\triangle ABC$ vuông tại B có $AB = \\sqrt{10}, BC = \\sqrt{6}$.")
    
    p = doc.add_paragraph()
    add_line_with_math(p, "Bài 3. Giải các tam giác vuông sau (kết quả làm tròn đến hàng phần trăm hoặc đến độ):", default_bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "a. $\\triangle ABC$ vuông tại A có $AB = 8, AC = 12$.")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "b. $\\triangle DEF$ vuông tại D có $DF = 14, \\widehat{E} = 34^\\circ$.")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    add_line_with_math(p, "c. $\\triangle PQR$ vuông tại P có $PQ = 14, PR = 15$.")
    
    # Bai 4 - 9
    geom_reals = [
        ("Bài 4.", "Các tia nắng mặt trời tạo với mặt đất một góc xấp xỉ bằng $34^\\circ$ và bóng của một tòa tháp trên mặt đất dài $8,6\\text{ m}$. Tính chiều cao của tòa tháp đó (kết quả làm tròn đến hàng đơn vị)."),
        ("Bài 5. [ĐÃ VÁ]", "Tính góc nghiêng $\\alpha$ của thùng xe chở rác biết cạnh thùng nâng dài $4\\text{ m}$ và khung xe nằm ngang dài $5\\text{ m}$ (tam giác tạo bởi thành thùng và gầm xe vuông tại hình chiếu của đỉnh thùng nâng)."),
        ("Bài 6.", "Một người đứng trên một tháp hải đăng ở vị trí cao $75\\text{ m}$ so với mặt nước biển đã quan sát hai lần thấy một chiếc thuyền đang hướng về phía tháp hải đăng với góc hạ lần lượt là $30^\\circ$ và $45^\\circ$. Hỏi thuyền đi được bao nhiêu mét giữa hai lần quan sát?"),
        ("Bài 7.", "Một người đứng cách chân tháp $13,65\\text{ m}$ nhìn lên đỉnh tháp với phương nhìn hợp với phương nằm ngang một góc bằng $58^\\circ$. Biết mắt của người đó cách chân của mình một khoảng $1,55\\text{ m}$. Hỏi tháp cao bao nhiêu mét (làm tròn đến chữ số thập phân thứ hai)?"),
        ("Bài 8. [ĐÃ VÁ ĐƠN VỊ VẬN TỐC]", "Lúc 6h sáng bạn An đi từ nhà (điểm A) đến trường (điểm B) phải leo lên và xuống dốc như hình vẽ. Cho biết đoạn $AB = 762\\text{ m}$, góc dốc $\\widehat{A} = 6^\\circ, \\widehat{B} = 4^\\circ$.\n  a) Tính chiều cao con dốc.\n  b) Hỏi An đến trường lúc mấy giờ? Biết rằng tốc độ lên dốc $4\\text{ km/h}$ và tốc độ xuống dốc $19\\text{ km/h}$."),
        ("Bài 9.", "Tính chiều cao của trụ cầu Cần Thơ so với mặt sông Hậu, cho biết tại hai điểm cách nhau $89\\text{ m}$ trên mặt sông người ta nhìn thấy đỉnh trụ cầu với góc nâng lần lượt là $40^\\circ$ và $30^\\circ$."),
        ("Bài 10.", "Cho đường tròn $(O)$, bán kính $5\\text{ cm}$ và bốn điểm A, B, C, D thỏa mãn $OA = 3\\text{ cm}, OB = 4\\text{ cm}, OC = 7\\text{ cm}, OD = 5\\text{ cm}$. Xác định vị trí tương đối của bốn điểm A, B, C, D so với đường tròn $(O; 5\\text{ cm})$."),
        ("Bài 11.", "Cho hình chữ nhật ABCD có $AB = 6\\text{ cm}, BC = 8\\text{ cm}$. Chứng minh rằng bốn điểm A, B, C, D cùng thuộc một đường tròn. Xác định tâm và bán kính của đường tròn đó.")
    ]
    for b_title, b_desc in geom_reals:
        p = doc.add_paragraph()
        add_line_with_math(p, b_title + " " + b_desc, default_bold=("Bài" in b_title and len(b_title) <= 10))

    # Save
    path_out = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\4_DUYET_DE\Ket_qua\14.10\De_Cuong_Toan_9_Ban_Va_Chinh_Thuc.docx"
    path_backup = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\4_DUYET_DE\Ket_qua\De_Cuong_Toan_9_Ban_Va_Chinh_Thuc.docx"
    
    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    doc.save(path_out)
    doc.save(path_backup)
    print("Saved Patched Syllabus successfully to:")
    print("1.", path_out)
    print("2.", path_backup)

if __name__ == "__main__":
    create_patched_syllabus()
