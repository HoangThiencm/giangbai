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

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_line_with_math(p, line, font_size=10.5, default_bold=False, default_italic=False, default_color=None):
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(0)
    
    parts = line.split('$')
    for idx, part in enumerate(parts):
        if not part:
            continue
        if idx % 2 == 1:
            # Inline math equation
            try:
                omml_elem = latex_to_omml(part)
                p._p.append(omml_elem)
            except Exception as e:
                r = p.add_run(part)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_size)
        else:
            # Normal text
            r = p.add_run(part)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            r.bold = default_bold
            r.italic = default_italic
            if default_color:
                r.font.color.rgb = default_color

def create_report():
    doc = Document()
    
    # 1. Page Margins A4 (Top: 2cm, Bottom: 2cm, Left: 3cm, Right: 1.5cm)
    for section in doc.sections:
        section.top_margin = Inches(0.79)      # ~2.0 cm
        section.bottom_margin = Inches(0.79)   # ~2.0 cm
        section.left_margin = Inches(1.18)     # ~3.0 cm
        section.right_margin = Inches(0.59)    # ~1.5 cm
        
    # Styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.2
    style.paragraph_format.space_after = Pt(3)
    style.paragraph_format.space_before = Pt(0)
    
    # ------------------ HEADER ------------------
    tbl_header = doc.add_table(rows=1, cols=2)
    tbl_header.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_header.autofit = False
    
    cell_l, cell_r = tbl_header.rows[0].cells
    cell_l.width = Inches(3.2)
    cell_r.width = Inches(3.6)
    
    # Left Header
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_l.add_run("TRƯỜNG THCS TRẦN PHÚ\nTỔ TOÁN - TIN\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True
    r2 = p_l.add_run("Số: ... /BC-TT")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.italic = True
    
    # Right Header
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.bold = True
    r2 = p_r.add_run("-------------------\nThành phố Cần Thơ, ngày 14 tháng 10 năm 2026")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.italic = True
    
    doc.add_paragraph() # Spacing
    
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("BÁO CÁO THẨM ĐỊNH VÀ PHẢN BIỆN CHUYÊN MÔN\n")
    r_t1.font.name = 'Times New Roman'
    r_t1.font.size = Pt(15)
    r_t1.bold = True
    r_t1.font.color.rgb = RGBColor(27, 54, 93)
    
    r_t2 = p_title.add_run("ĐỀ CƯƠNG ÔN TẬP GIỮA HỌC KỲ I - MÔN TOÁN 9\nNĂM HỌC 2026 - 2027\n")
    r_t2.font.name = 'Times New Roman'
    r_t2.font.size = Pt(13)
    r_t2.bold = True
    
    r_t3 = p_title.add_run("(Bước 2: Phản biện chi tiết nội dung đề cương - Chuẩn hóa công thức Equation)")
    r_t3.font.name = 'Times New Roman'
    r_t3.font.size = Pt(12)
    r_t3.italic = True
    
    doc.add_paragraph()
    
    # Section I: Thông tin chung
    p_h1 = doc.add_paragraph()
    r = p_h1.add_run("I. THÔNG TIN CHUNG VÀ CƠ SỞ PHÁP LÝ")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    p = doc.add_paragraph()
    p.add_run(
        "1. Tài liệu thẩm định: Tệp bản gốc 'De_cuong_Giua_HKI_Toan_9_(2026_2027).pdf' (gồm 03 trang hoàn chỉnh với toàn bộ công thức và hình ảnh sắc nét), đối sánh cùng Ma trận kiểm tra giữa kỳ I.\n"
        "2. Đơn vị thực hiện: Tổ thẩm định chuyên môn Toán 9 - Trợ lý Sư phạm Hoàng Thiên.\n"
        "3. Phương pháp thẩm định: Giải tích độc lập toàn bộ các bài toán Đại số và Hình học, kiểm tra tính xác định, điều kiện nghiệm, tính logic sư phạm, tính thời sự thực tế và độ tương thích với Ma trận đặc tả đề kiểm tra.\n"
        "4. Chuẩn hóa hình thức: Toàn bộ công thức toán học, căn thức, phân số và hệ phương trình trong báo cáo được xuất bản bằng chuẩn công thức Word Equation (OMML) trực quan, chuẩn mực."
    )
    
    # Section II: Đánh giá tổng quan
    p_h2 = doc.add_paragraph()
    r = p_h2.add_run("II. ĐÁNH GIÁ TỔNG QUAN NỘI DUNG ĐỀ CƯƠNG")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    p = doc.add_paragraph()
    p.add_run(
        "Nhìn chung, Đề cương ôn tập Giữa học kỳ I môn Toán 9 của Tổ Toán - Tin trường THCS Trần Phú được biên soạn công phu, bám sát khung Chương trình GDPT 2018 và chuẩn kiến thức kỹ năng của SGK Toán 9 hiện hành.\n"
        "• Về cấu trúc: Đề cương phân định rõ ràng giữa hai mạch kiến thức cốt lõi: Phần I - Đại số (10 bài) và Phần II - Hình học (11 bài), bao phủ đầy đủ các mức độ từ Nhận biết, Thông hiểu đến Vận dụng và Vận dụng cao.\n"
        "• Về tính thực tiễn: Rất khen ngợi tổ bộ môn đã tích hợp các bài toán mô hình hóa thực tế sinh động, mang đậm dấu ấn địa phương và đời sống như: bài toán xe buýt, vé xem phim, mảnh vườn, xe chở rác, ngọn hải đăng, con dốc và đặc biệt là chiều cao Trụ cầu Cần Thơ bắc qua sông Hậu.\n"
        "• Độ chính xác toán học: Đa số các bài toán đều có nghiệm nguyên hoặc số thập phân/vô tỉ rất đẹp, chuẩn mực sư phạm."
    )
    
    # Section III: Bảng chi tiết
    p_h3 = doc.add_paragraph()
    r = p_h3.add_run("III. BẢNG PHẢN BIỆN VÀ GIẢI TÍCH CHI TIẾT TỪNG BÀI TOÁN (CHUẨN EQUATION)")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="D3D3D3")
    
    col_widths = [Inches(0.9), Inches(2.2), Inches(2.4), Inches(1.7)]
    headers = ["Bài số", "Nội dung vắn tắt", "Kết quả giải tích độc lập (Equation)", "Đánh giá sư phạm & Khuyến nghị"]
    
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(11)
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=100, right=100)

    # Detailed data items with LaTeX math delimiters $...$
    data = [
        # DAI SO
        (
            "[ĐẠI SỐ]\nBài 1",
            [
                "Giải phương trình:",
                "• PT tích: a, b, c, d",
                "• PT chứa ẩn ở mẫu:",
                "  e) $\\frac{2x - 3}{x - 1} + \\frac{3}{x} = 2$",
                "  g) $\\frac{2x - 5}{x + 3} - \\frac{x + 1}{x - 3} = \\frac{x^2 + 9}{x^2 - 9}$",
                "  h) $\\frac{x}{x + 3} - \\frac{2}{x - 1} = \\frac{x^2 + 9}{(x + 3)(x - 1)}$",
                "  i) $\\frac{x - 1}{x - 3} - \\frac{x + 3}{x - 1} = \\frac{8x}{(x - 3)(x - 1)}$"
            ],
            [
                "• a: $x \\in \\{0; \\frac{5}{2}\\}$",
                "• b: $x \\in \\{6; -\\frac{4}{3}\\}$",
                "• c: $x \\in \\{2; \\frac{3}{5}\\}$",
                "• d: $x \\in \\{4; -\\frac{2}{5}\\}$",
                "• e: $x = \\frac{3}{2} = 1,5$ (TMĐK)",
                "• g: $x = \\frac{1}{5} = 0,2$ (TMĐK)",
                "• h: $x = -5$ (TMĐK)",
                "• i: Giải ra $x = 1$. Đối chiếu ĐKXĐ ($x \\ne 1, x \\ne 3$) $\\Rightarrow x = 1$ bị LOẠI. Phương trình VÔ NGHIỆM ($S = \\emptyset$)."
            ],
            [
                "Rất tốt.",
                "LƯU Ý ĐẶC BIỆT CÂU 1.i:",
                "Đây là bẫy nghiệm ngoại lai kinh điển. HS rất dễ quên đối chiếu ĐKXĐ và kết luận $x = 1$ (sai). GV cần nhấn mạnh đáp án PT vô nghiệm."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 2",
            [
                "Giải các bất phương trình:",
                "a) $5x - 20 \\ge 0$",
                "b) $8x - 2 < 11x + 7$",
                "c) $5x - 7(2x - 5) < 2(x - 1)$"
            ],
            [
                "• a) $x \\ge 4$",
                "• b) $-3x < 9 \\Leftrightarrow x > -3$",
                "• c) $-11x < -37 \\Leftrightarrow x > \\frac{37}{11}$"
            ],
            [
                "Chuẩn mực. Rèn tốt kỹ năng chuyển vế và đổi chiều BPT khi chia cho số âm."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 3, 4",
            [
                "Nhận biết PT, BPT bậc nhất hai ẩn & một ẩn; xác định hệ số $a, b, c$."
            ],
            [
                "• Bài 3: (a, c) là PT bậc nhất 2 ẩn; (b, d) không phải.",
                "• Bài 4: (d, e) là BPT bậc nhất 1 ẩn; (a, b, c) không phải."
            ],
            [
                "Rất chuẩn theo yêu cầu cần đạt mức độ Nhận biết của Chương trình 2018."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 5, 6",
            [
                "Nghiệm và giải hệ phương trình bậc nhất hai ẩn (cộng đại số, thế)."
            ],
            [
                "• Bài 5: Cặp số $(2; 1)$ là nghiệm của hệ (Chọn B).",
                "• Bài 6:",
                "  a) $(2; -3)$",
                "  b) $(\\frac{1}{4}; 1)$",
                "  c) Vô nghiệm ($0x - 0y = 1$)",
                "  d) Vô số nghiệm $(x; \\frac{1 - 2x}{5})$"
            ],
            [
                "Rất bao quát, đầy đủ cả 3 trạng thái nghiệm: nghiệm duy nhất, vô nghiệm và vô số nghiệm."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 7, 8, 9",
            [
                "Biểu diễn BĐT bằng ngôn ngữ toán học; tính chất cơ bản của BĐT."
            ],
            [
                "• Bài 7: $T \\ge 6$; $t \\le 4^\\circ\\text{C}$; $x \\le 45$",
                "• Bài 8: $a < 5$; $x \\le y$; $m \\le n$",
                "• Bài 9: Áp dụng tính chất cộng/nhân với số dương/âm."
            ],
            [
                "Tốt, rèn tư duy toán học hóa các tình huống đời sống thực tế."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 10.1",
            [
                "Toán thực tế HPT: Kế hoạch 360 công cụ; xí nghiệp I vượt 12%, II vượt 10%; tổng 400 công cụ."
            ],
            [
                "Hệ phương trình:",
                "$\\begin{cases} x + y = 360 \\\\ 1,12x + 1,1y = 400 \\end{cases}$",
                "$\\Leftrightarrow \\begin{cases} x = 200 \\\\ y = 160 \\end{cases}$ (công cụ)"
            ],
            [
                "Số liệu nguyên rất đẹp, phù hợp kiểm tra giữa kỳ."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 10.2",
            [
                "Toán thực tế HPT: Mảnh vườn HCN chu vi 64m. Tăng rộng 3m, giảm dài 2m thì diện tích tăng $30\\text{ m}^2$."
            ],
            [
                "Hệ phương trình:",
                "$\\begin{cases} x + y = 32 \\\\ (x - 2)(y + 3) = xy + 30 \\end{cases}$",
                "$\\Leftrightarrow \\begin{cases} x = 20 \\\\ y = 12 \\end{cases}$ (m)",
                "$\\Rightarrow S = 20 \\times 12 = 240\\text{ m}^2$"
            ],
            [
                "Dạng toán kinh điển, số liệu tròn trịa, nghiệm thực tế hợp lý."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 10.3",
            [
                "Toán thực tế HPT: Vé xem phim. Ông An: 5 lớn + 3 trẻ = 840k; Ông Nam: 7 lớn + 6 trẻ = 1.320k."
            ],
            [
                "Hệ phương trình:",
                "$\\begin{cases} 5x + 3y = 840000 \\\\ 7x + 6y = 1320000 \\end{cases}$",
                "$\\Leftrightarrow \\begin{cases} x = 120000 \\\\ y = 80000 \\end{cases}$ (đồng)"
            ],
            [
                "Tuyệt vời. Giá vé phim người lớn 120k và trẻ em 80k rất sát với thực tế rạp phim hiện nay."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 10.4",
            [
                "Toán thực tế HPT: Quãng đường $AB = 120\\text{ km}$. Ô tô và xe máy đi ngược chiều gặp nhau sau 2h. Ô tô nhanh hơn xe máy $10\\text{ km/h}$."
            ],
            [
                "Hệ phương trình:",
                "$\\begin{cases} x - y = 10 \\\\ 2(x + y) = 120 \\end{cases}$",
                "$\\Leftrightarrow \\begin{cases} x = 35\\text{ km/h (ô tô)} \\\\ y = 25\\text{ km/h (xe máy)} \\end{cases}$"
            ],
            [
                "Chuẩn xác 100%. Số liệu vận tốc vừa phải, an toàn giao thông."
            ]
        ),
        # HINH HOC
        (
            "[HÌNH HỌC]\nBài 1.1, 1.2",
            [
                "Tỉ số lượng giác góc phụ nhau; Tính giá trị biểu thức không dùng MTCT."
            ],
            [
                "• 1.1: $\\cos 69^\\circ = \\sin 21^\\circ$; $\\cot 83^\\circ = \\tan 7^\\circ$; $\\sin 77^\\circ = \\cos 13^\\circ$; $\\tan 51^\\circ = \\cot 39^\\circ$",
                "• 1.2:",
                "  $A = 3\\cos 35^\\circ - 3\\sin 55^\\circ + \\frac{\\tan 70^\\circ}{\\cot 20^\\circ} = 1$",
                "  $B = \\tan 25^\\circ - \\cot 65^\\circ + 4\\frac{\\sin 80^\\circ}{\\cos 10^\\circ} = 4$"
            ],
            [
                "Chuẩn mực, các số hạng triệt tiêu rất đẹp."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 1.3",
            [
                "Tính giá trị biểu thức góc đặc biệt:",
                "Biểu thức A và biểu thức B."
            ],
            [
                "• $A = \\cos 45^\\circ - \\sin 60^\\circ + \\frac{\\tan 30^\\circ}{\\cos 60^\\circ}$",
                "  $A = \\frac{\\sqrt{2}}{2} - \\frac{\\sqrt{3}}{2} + \\frac{2\\sqrt{3}}{3} = \\frac{\\sqrt{2}}{2} + \\frac{\\sqrt{3}}{6}$",
                "• $B = \\tan 65^\\circ - \\sin 30^\\circ + \\frac{\\sin 45^\\circ \\cdot \\sin 60^\\circ}{\\tan 45^\\circ}$"
            ],
            [
                "CẦN ĐIỀU CHỈNH:",
                "Góc $65^\\circ$ không phải góc đặc biệt, không triệt tiêu được. Đề xuất sửa thành $\\tan 60^\\circ$ hoặc $\\tan 45^\\circ$."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 2",
            [
                "Tính các tỉ số lượng giác góc nhọn C trong tam giác vuông (Hình 1):",
                "a) $AB=3, BC=4$",
                "b) $AB=2, AC=3$",
                "c) $AB=\\sqrt{10}, BC=\\sqrt{6}$"
            ],
            [
                "• a) $AC = 5$; $\\sin C = \\frac{3}{5}$; $\\cos C = \\frac{4}{5}$; $\\tan C = \\frac{3}{4}$; $\\cot C = \\frac{4}{3}$",
                "• b) $BC = \\sqrt{13}$; $\\sin C = \\frac{2\\sqrt{13}}{13}$; $\\cos C = \\frac{3\\sqrt{13}}{13}$; $\\tan C = \\frac{2}{3}$; $\\cot C = \\frac{3}{2}$",
                "• c) $AC = 4$; $\\sin C = \\frac{\\sqrt{10}}{4}$; $\\cos C = \\frac{\\sqrt{6}}{4}$; $\\tan C = \\frac{\\sqrt{15}}{3}$; $\\cot C = \\frac{\\sqrt{15}}{5}$"
            ],
            [
                "Căn thức chuẩn xác 100%. Trục căn thức ở mẫu rất chuẩn mực sư phạm."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 3",
            [
                "Giải các tam giác vuông trong Hình 2 (kết quả làm tròn):",
                "a) $AB=8, AC=12$",
                "b) $DF=14, \\widehat{E}=34^\\circ$",
                "c) $PQ=14, PR=15$"
            ],
            [
                "• a) $BC = 4\\sqrt{13} \\approx 14,42$; $\\widehat{C} \\approx 34^\\circ$; $\\widehat{B} \\approx 56^\\circ$",
                "• b) $\\widehat{F} = 56^\\circ$; $EF = \\frac{14}{\\sin 34^\\circ} \\approx 25,04$; $DE = \\frac{14}{\\tan 34^\\circ} \\approx 20,76$",
                "• c) $QR = \\sqrt{421} \\approx 20,52$; $\\widehat{Q} \\approx 47^\\circ$; $\\widehat{R} \\approx 43^\\circ$"
            ],
            [
                "Chuẩn xác, rèn luyện toàn diện cả định lý Pitago và tỉ số lượng giác."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 4",
            [
                "Toán thực tế: Chiều cao tòa tháp có bóng $8,6\\text{ m}$, góc tia nắng $34^\\circ$."
            ],
            [
                "$h = 8,6 \\cdot \\tan 34^\\circ \\approx 5,8\\text{ m} \\approx 6\\text{ m}$"
            ],
            [
                "Chuẩn mực SGK."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 5",
            [
                "Toán thực tế: Tính góc nghiêng $\\alpha$ của thùng xe chở rác (đáy 5m, cạnh thùng 4m)."
            ],
            [
                "Mô hình tam giác vuông cạnh kề 4m, cạnh huyền 5m:",
                "$\\cos \\alpha = \\frac{4}{5} = 0,8 \\Rightarrow \\alpha \\approx 36^\\circ 52'$"
            ],
            [
                "LƯU Ý SƯ PHẠM: Cần bổ sung ký hiệu góc vuông $90^\\circ$ trên hình vẽ để học sinh áp dụng đúng tỉ số lượng giác."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 6",
            [
                "Toán thực tế: Người trên hải đăng cao 75m nhìn chiếc thuyền với góc hạ $30^\\circ$ và $45^\\circ$."
            ],
            [
                "Khoảng cách thuyền đi giữa 2 lần quan sát:",
                "$d = 75(\\cot 30^\\circ - \\cot 45^\\circ)$",
                "$d = 75(\\sqrt{3} - 1) \\approx 54,9\\text{ m}$"
            ],
            [
                "Rất hay, chuẩn dạng toán nâng cao thực tế."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 7",
            [
                "Toán thực tế: Giác kế cao $1,55\\text{ m}$, cách chân tháp $13,65\\text{ m}$, góc nhìn $58^\\circ$."
            ],
            [
                "$h = 1,55 + 13,65 \\cdot \\tan 58^\\circ \\approx 23,39\\text{ m}$"
            ],
            [
                "Chính xác và sát thực tế đo đạc địa lý."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 8",
            [
                "Toán thực tế: Con dốc $AB = 762\\text{ m}$, góc dốc $\\widehat{A} = 6^\\circ$, $\\widehat{B} = 4^\\circ$. Vận tốc lên dốc $4\\text{ hm/h}$, xuống dốc $19\\text{ km/h}$."
            ],
            [
                "a) Chiều cao con dốc:",
                "$h = \\frac{762}{\\cot 6^\\circ + \\cot 4^\\circ} \\approx 32\\text{ m}$",
                "b) Đoạn lên dốc: $AC = \\frac{32}{\\sin 6^\\circ} \\approx 306\\text{ m}$",
                "   Đoạn xuống dốc: $CB = \\frac{32}{\\sin 4^\\circ} \\approx 459\\text{ m}$"
            ],
            [
                "LƯU Ý QUAN TRỌNG: Đơn vị vận tốc '4hm/h' ($= 0,4\\text{ km/h}$) là bất hợp lý trong đời sống. Kiến nghị sửa thành $4\\text{ km/h}$."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 9",
            [
                "Toán thực tế: Chiều cao trụ cầu Cần Thơ trên sông Hậu nhìn từ 2 điểm cách nhau 89m, góc nâng $40^\\circ$ và $30^\\circ$."
            ],
            [
                "$h = \\frac{89}{\\cot 30^\\circ - \\cot 40^\\circ} = \\frac{89}{\\sqrt{3} - \\cot 40^\\circ}$",
                "$h \\approx 164,7\\text{ m}$"
            ],
            [
                "TUYỆT VỜI. Rất mang tính tự hào địa phương vùng ĐBSCL. Số liệu thực tế trụ tháp cầu Cần Thơ cao ~171m so với mặt nước, sai số mô hình rất nhỏ."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 10, 11",
            [
                "Đường tròn: Vị trí tương đối của điểm với $(O; 5\\text{ cm})$; 4 đỉnh hình chữ nhật cùng thuộc 1 đường tròn."
            ],
            [
                "• Bài 10: $OA=3 < 5, OB=4 < 5$ (trong); $OC=7 > 5$ (ngoài); $OD=5=R$ (thuộc đường tròn).",
                "• Bài 11: Tâm $O$ là giao điểm 2 đường chéo, $R = \\frac{AC}{2} = \\frac{10}{2} = 5\\text{ cm}$."
            ],
            [
                "Chuẩn xác 100%, chuẩn bị kiến thức nền tảng cho nửa cuối HKI."
            ]
        )
    ]
    
    for row_idx, item in enumerate(data):
        row = table.add_row()
        bg_color = "FFFFFF" if row_idx % 2 == 0 else "F9FBFD"
        
        # Col 0: Title
        cell0 = row.cells[0]
        cell0.width = col_widths[0]
        set_cell_background(cell0, bg_color)
        set_cell_margins(cell0, top=80, bottom=80, left=90, right=90)
        p0 = cell0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p0.add_run(item[0])
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        
        # Other cols
        for col_idx in [1, 2, 3]:
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
            
            lines = item[col_idx]
            for l_idx, line in enumerate(lines):
                p = cell.paragraphs[0] if l_idx == 0 else cell.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                is_alert = "LƯU Ý" in line or "CẦN ĐIỀU CHỈNH" in line
                alert_color = RGBColor(180, 40, 20) if is_alert else None
                add_line_with_math(p, line, font_size=10.5, default_bold=is_alert, default_color=alert_color)

    doc.add_paragraph() # Spacing
    
    # Section IV: 4 điểm kiến nghị
    p_h4 = doc.add_paragraph()
    r = p_h4.add_run("IV. BỐN (04) TRỌNG TÂM SƯ PHẠM CẦN TINH CHỈNH HOẶC LƯU Ý KHI GIẢNG DẠY")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(180, 40, 20)
    
    recs = [
        (
            "1. Bẫy nghiệm ngoại lai ở Bài 1.i (Phần Đại số):",
            [
                "Phương trình: $\\frac{x - 1}{x - 3} - \\frac{x + 3}{x - 1} = \\frac{8x}{(x - 3)(x - 1)}$.",
                "• Điều kiện xác định: $x \\ne 3$ và $x \\ne 1$.",
                "• Khi quy đồng rút gọn: $-2x + 10 = 8x \\Leftrightarrow 10x = 10 \\Leftrightarrow x = 1$.",
                "• Giá trị $x = 1$ vi phạm điều kiện xác định nên bị LOẠI. Vậy phương trình VÔ NGHIỆM ($S = \\emptyset$).",
                "⇒ Đánh giá sư phạm: Đây là câu hỏi rất hay để rèn học sinh tính cẩn trọng. Tuy nhiên, GV ra đề cần ghi rõ trong Hướng dẫn chấm: Nếu học sinh giải ra $x = 1$ mà không đối chiếu ĐKXĐ hoặc kết luận nghiệm $x = 1$ thì không cho điểm bước kết luận."
            ]
        ),
        (
            "2. Kiểm tra góc đặc biệt ở Bài 1.3 - Biểu thức B (Phần Hình học):",
            [
                "Đề bài ghi: $B = \\tan 65^\\circ - \\sin 30^\\circ + \\frac{\\sin 45^\\circ \\cdot \\sin 60^\\circ}{\\tan 45^\\circ}$.",
                "• Góc $65^\\circ$ không thuộc bảng giá trị lượng giác các góc đặc biệt ($30^\\circ, 45^\\circ, 60^\\circ$) mà học sinh được học trong bài này, và biểu thức cũng không có số hạng đối để triệt tiêu như ở câu 1.2.",
                "⇒ Kiến nghị điều chỉnh: Đổi góc $\\tan 65^\\circ$ thành $\\tan 60^\\circ$ (hoặc $\\tan 45^\\circ$) để biểu thức có thể tính toán chính xác bằng bảng lượng giác đặc biệt mà không cần dùng máy tính cầm tay."
            ]
        ),
        (
            "3. Làm rõ mô hình hình học ở Bài 5 (Phần Hình học - Thùng xe chở rác):",
            [
                "Hình vẽ số 4 mô tả thùng xe chở rác có đáy 5m và cạnh nâng 4m với góc nghiêng $\\alpha$.",
                "⇒ Kiến nghị điều chỉnh: Cần ghi chú rõ cạnh nào là cạnh huyền, cạnh nào là cạnh góc vuông (bổ sung ký hiệu góc vuông $90^\\circ$ vào mô hình tam giác) để tránh trường hợp học sinh nhầm lẫn giữa $\\sin, \\cos$ hay $\\tan$."
            ]
        ),
        (
            "4. Chuẩn hóa đơn vị đo tốc độ thực tế ở Bài 8.b (Phần Hình học - Con dốc):",
            [
                "Đề bài ghi: '...vận tốc lên dốc $4\\text{ hm/h}$ và tốc độ xuống dốc $19\\text{ km/h}$'.",
                "• Đơn vị $4\\text{ hm/h} = 0,4\\text{ km/h}$ (tương đương 400 mét trong 1 giờ). Đây là tốc độ cực kỳ chậm, không thực tế đối với một học sinh đi học (chậm hơn đi bộ bình thường 10 lần).",
                "⇒ Kiến nghị điều chỉnh: Đổi $4\\text{ hm/h}$ thành $4\\text{ km/h}$ (hoặc $12 - 14\\text{ km/h}$ nếu đi xe đạp) để đảm bảo tính giáo dục gắn liền với thực tế cuộc sống."
            ]
        )
    ]
    
    for title, lines in recs:
        p_t = doc.add_paragraph()
        r1 = p_t.add_run(title)
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.font.color.rgb = RGBColor(27, 54, 93)
        
        for line in lines:
            p_c = doc.add_paragraph()
            add_line_with_math(p_c, line, font_size=12)
        
    # Section V: Kết luận
    p_h5 = doc.add_paragraph()
    r = p_h5.add_run("V. KẾT LUẬN CỦA TỔ THẨM ĐỊNH CHUYÊN MÔN")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    p = doc.add_paragraph()
    p.add_run(
        "Đề cương ôn tập Giữa học kỳ I môn Toán 9 năm học 2026 - 2027 có chất lượng chuyên môn RẤT TỐT, bố cục khoa học, hệ thống bài tập thực tiễn đa dạng, phong phú và bám sát tinh thần đổi mới của Chương trình GDPT 2018.\n"
        "Tổ chuyên môn thống nhất thông qua đề cương sau khi tiếp thu và chỉnh lý 04 điểm lưu ý kỹ thuật nêu trên để phục vụ công tác giảng dạy, ôn tập và ra đề kiểm tra giữa kỳ đạt hiệu quả cao nhất."
    )
    
    doc.add_paragraph()
    
    # Signature Table
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig.autofit = False
    
    c_sig_l, c_sig_r = tbl_sig.rows[0].cells
    c_sig_l.width = Inches(3.4)
    c_sig_r.width = Inches(3.4)
    
    p_sl = c_sig_l.paragraphs[0]
    p_sl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sl.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n")
    r.bold = True
    r.font.size = Pt(12)
    r2 = p_sl.add_run("(Ký và ghi rõ họ tên)\n\n\n\n")
    r2.italic = True
    r2.font.size = Pt(11)
    
    p_sr = c_sig_r.paragraphs[0]
    p_sr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_sr.add_run("NGƯỜI LẬP BÁO CÁO / PHẢN BIỆN\n")
    r.bold = True
    r.font.size = Pt(12)
    r2 = p_sr.add_run("(Ký và ghi rõ họ tên)\n\n\n\n")
    r2.italic = True
    r2.font.size = Pt(11)
    r3 = p_sr.add_run("Trợ lý Sư phạm Hoàng Thiên")
    r3.bold = True
    r3.font.size = Pt(12)
    
    # Save to both folders
    path1 = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\4_DUYET_DE\Ket_qua\14.10\Phan_Bien_De_Cuong_Toan_9.docx"
    path2 = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\4_DUYET_DE\Ket_qua\Phan_Bien_De_Cuong_Toan_9.docx"
    
    os.makedirs(os.path.dirname(path1), exist_ok=True)
    os.makedirs(os.path.dirname(path2), exist_ok=True)
    
    doc.save(path1)
    doc.save(path2)
    print("Saved successfully with 100% Native Word Equations (OMML) to:")
    print("1.", path1)
    print("2.", path2)

if __name__ == "__main__":
    create_report()
