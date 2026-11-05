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

def create_master_report():
    doc = Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.59)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.2
    style.paragraph_format.space_after = Pt(3)
    style.paragraph_format.space_before = Pt(0)
    
    # Header
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
    r2 = p_l.add_run("Số: ... /BC-TT")
    r2.italic = True
    r2.font.size = Pt(11)
    
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n")
    r.bold = True
    r.font.size = Pt(11)
    r2 = p_r.add_run("-------------------\nThành phố Cần Thơ, ngày 14 tháng 10 năm 2026")
    r2.italic = True
    r2.font.size = Pt(11)
    
    doc.add_paragraph()
    
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("BÁO CÁO THẨM ĐỊNH VÀ PHẢN BIỆN CHUYÊN MÔN TOÁN 9\n")
    r_t1.bold = True
    r_t1.font.size = Pt(15)
    r_t1.font.color.rgb = RGBColor(27, 54, 93)
    
    r_t2 = p_title.add_run("TỔNG HỢP: MA TRẬN & ĐỀ CƯƠNG ÔN TẬP GIỮA HỌC KỲ I (2026 - 2027)\n")
    r_t2.bold = True
    r_t2.font.size = Pt(13)
    
    r_t3 = p_title.add_run("(Chuẩn hóa 100% công thức Word Equation OMML - Căn thức & Phân số)")
    r_t3.italic = True
    r_t3.font.size = Pt(12)
    
    doc.add_paragraph()
    
    # Section 1: Thẩm định ma trận
    p_h1 = doc.add_paragraph()
    r = p_h1.add_run("PHẦN I: KẾT QUẢ THẨM ĐỊNH MA TRẬN ĐỀ KIỂM TRA GIỮA HỌC KỲ I")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    doc.add_paragraph(
        "1. Cơ sở pháp lý: Tệp gốc 'MT_Toan 9_ Kiemtra GK_1.docx'.\n"
        "2. Kết quả đối soát số học trên bảng ma trận:\n"
        "   • Lỗi 1 (Cột Thông hiểu TNKQ): Ghi tổng 2 câu = 0,5 điểm, nhưng tổng cột tính nhầm thành 0,75 điểm.\n"
        "   • Lỗi 2 (Tỷ lệ % Vận dụng cao): Cột VDC gồm Bài 1.3 (0,5đ) + Bài 4 (0,5đ) = 1,0 điểm. Nhưng bảng tổng kết cuối ghi 0% (đúng chuẩn phải là 10%).\n"
        "   • Lỗi 3 (Dòng Tổng hợp điểm & số câu): Tính lệch 0,25 điểm giữa tổng số điểm hàng ngang và hàng dọc.\n"
        "   • Cấu trúc câu hỏi: Phân bổ Bài 1.1, 1.2, 1.3; Bài 2.1, 2.2; Bài 3.1 - 3.4; Bài 4 là hoàn toàn bình thường, đúng chuẩn cấu trúc trường THCS Trần Phú."
    )
    
    doc.add_paragraph()
    
    # Section 2: Thẩm định đề cương (BẢNG EQUATION)
    p_h2 = doc.add_paragraph()
    r = p_h2.add_run("PHẦN II: THẨM ĐỊNH VÀ PHẢN BIỆN CHI TIẾT ĐỀ CƯƠNG ÔN TẬP (CHUẨN EQUATION)")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    doc.add_paragraph(
        "Giải tích độc lập toàn bộ 10 bài Đại số và 11 bài Hình học từ bản PDF gốc 'De_cuong_Giua_HKI_Toan_9_(2026_2027).pdf'.\n"
        "Tất cả căn thức, phân số, hệ phương trình dưới đây đã được cập nhật bản vá thành Word Equation (OMML):"
    )
    
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="D3D3D3")
    
    col_widths = [Inches(0.9), Inches(2.2), Inches(2.4), Inches(1.7)]
    headers = ["Bài số", "Nội dung vắn tắt", "Kết quả giải tích (Equation)", "Đánh giá & Khuyến nghị"]
    
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
                "LƯU Ý CÂU 1.i: Bẫy nghiệm ngoại lai kinh điển. GV cần lưu ý đáp án PT vô nghiệm."
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
                "Chuẩn mực. Rèn tốt quy tắc chia cho số âm đổi chiều."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 3, 4",
            [
                "Nhận biết PT, BPT bậc nhất hai ẩn & một ẩn."
            ],
            [
                "• Bài 3: (a, c) là PT bậc nhất 2 ẩn; (b, d) không phải.",
                "• Bài 4: (d, e) là BPT bậc nhất 1 ẩn; (a, b, c) không phải."
            ],
            [
                "Chuẩn mực theo khung GDPT 2018."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 5, 6",
            [
                "Nghiệm và giải hệ phương trình bậc nhất hai ẩn."
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
                "Đầy đủ 3 dạng: nghiệm duy nhất, vô nghiệm, vô số nghiệm."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 7, 8, 9",
            [
                "Biểu diễn BĐT thực tế; tính chất BĐT."
            ],
            [
                "• Bài 7: $T \\ge 6$; $t \\le 4^\\circ\\text{C}$; $x \\le 45$",
                "• Bài 8: $a < 5$; $x \\le y$; $m \\le n$",
                "• Bài 9: Áp dụng tính chất cộng/nhân với số dương/âm."
            ],
            [
                "Tốt, rèn tư duy toán học hóa đời sống."
            ]
        ),
        (
            "[ĐẠI SỐ]\nBài 10",
            [
                "Toán thực tế HPT:",
                "• 10.1: 360 công cụ",
                "• 10.2: Mảnh vườn 64m",
                "• 10.3: Vé xem phim",
                "• 10.4: Quãng đường 120km"
            ],
            [
                "• 10.1: $\\begin{cases} x + y = 360 \\\\ 1,12x + 1,1y = 400 \\end{cases} \\Leftrightarrow \\begin{cases} x = 200 \\\\ y = 160 \\end{cases}$",
                "• 10.2: $\\begin{cases} x + y = 32 \\\\ 3x - 2y = 36 \\end{cases} \\Rightarrow x = 20, y = 12, S = 240\\text{ m}^2$",
                "• 10.3: $\\begin{cases} 5x + 3y = 840000 \\\\ 7x + 6y = 1320000 \\end{cases} \\Leftrightarrow \\begin{cases} x = 120000 \\\\ y = 80000 \\end{cases}$",
                "• 10.4: $\\begin{cases} x - y = 10 \\\\ 2(x + y) = 120 \\end{cases} \\Leftrightarrow \\begin{cases} x = 35 \\\\ y = 25 \\end{cases}$"
            ],
            [
                "Nghiệm nguyên cực đẹp, số liệu rất thực tế."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 1",
            [
                "Tỉ số lượng giác góc phụ nhau; tính giá trị biểu thức."
            ],
            [
                "• 1.1: $\\cos 69^\\circ = \\sin 21^\\circ$; $\\cot 83^\\circ = \\tan 7^\\circ$; $\\sin 77^\\circ = \\cos 13^\\circ$; $\\tan 51^\\circ = \\cot 39^\\circ$",
                "• 1.2: $A = 1$; $B = 4$",
                "• 1.3: $A = \\frac{\\sqrt{2}}{2} + \\frac{\\sqrt{3}}{6}$ ; $B$ xuất hiện $\\tan 65^\\circ$."
            ],
            [
                "LƯU Ý CÂU 1.3: $\\tan 65^\\circ$ không phải góc đặc biệt. Đã vá thành $\\tan 60^\\circ$."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 2",
            [
                "Tính TSLG góc nhọn C trong tam giác vuông (Hình 1):",
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
                "Căn thức chuẩn xác 100%. Trục căn thức ở mẫu chuẩn mực."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 3",
            [
                "Giải các tam giác vuông trong Hình 2:"
            ],
            [
                "• a) $BC = 4\\sqrt{13} \\approx 14,42$; $\\widehat{C} \\approx 34^\\circ$; $\\widehat{B} \\approx 56^\\circ$",
                "• b) $\\widehat{F} = 56^\\circ$; $EF = \\frac{14}{\\sin 34^\\circ} \\approx 25,04$; $DE = \\frac{14}{\\tan 34^\\circ} \\approx 20,76$",
                "• c) $QR = \\sqrt{421} \\approx 20,52$; $\\widehat{Q} \\approx 47^\\circ$; $\\widehat{R} \\approx 43^\\circ$"
            ],
            [
                "Chuẩn xác 100%."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 4 - 9",
            [
                "Toán thực tế:",
                "• Bài 4: Tháp bóng 8,6m",
                "• Bài 5: Xe chở rác",
                "• Bài 6: Hải đăng 75m",
                "• Bài 7: Tháp cao qua giác kế",
                "• Bài 8: Con dốc 762m",
                "• Bài 9: Trụ cầu Cần Thơ"
            ],
            [
                "• Bài 4: $h = 8,6 \\cdot \\tan 34^\\circ \\approx 5,8\\text{ m} \\approx 6\\text{ m}$",
                "• Bài 5: $\\cos \\alpha = \\frac{4}{5} = 0,8 \\Rightarrow \\alpha \\approx 36^\\circ 52'$",
                "• Bài 6: $d = 75(\\cot 30^\\circ - \\cot 45^\\circ) = 75(\\sqrt{3} - 1) \\approx 54,9\\text{ m}$",
                "• Bài 7: $h = 1,55 + 13,65 \\cdot \\tan 58^\\circ \\approx 23,39\\text{ m}$",
                "• Bài 8: $h = \\frac{762}{\\cot 6^\\circ + \\cot 4^\\circ} \\approx 32\\text{ m}$; Lên dốc 306m, xuống dốc 459m",
                "• Bài 9: $h = \\frac{89}{\\cot 30^\\circ - \\cot 40^\\circ} = \\frac{89}{\\sqrt{3} - \\cot 40^\\circ} \\approx 164,7\\text{ m}$"
            ],
            [
                "LƯU Ý BÀI 8: Đơn vị '4hm/h' đã được vá thành $4\\text{ km/h}$.",
                "BÀI 9: Cầu Cần Thơ số liệu cực kỳ sát với thực tế (~171m)."
            ]
        ),
        (
            "[HÌNH HỌC]\nBài 10, 11",
            [
                "Đường tròn:",
                "• Vị trí điểm với $(O; 5\\text{ cm})$",
                "• 4 đỉnh hình chữ nhật"
            ],
            [
                "• Bài 10: $OA=3, OB=4$ (trong); $OC=7$ (ngoài); $OD=5=R$ (thuộc đường tròn).",
                "• Bài 11: Tâm $O$ là giao điểm 2 đường chéo, $R = \\frac{AC}{2} = 5\\text{ cm}$."
            ],
            [
                "Chuẩn xác 100%."
            ]
        )
    ]
    
    for row_idx, item in enumerate(data):
        row = table.add_row()
        bg_color = "FFFFFF" if row_idx % 2 == 0 else "F9FBFD"
        
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
        
        for col_idx in [1, 2, 3]:
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
            
            lines = item[col_idx]
            for l_idx, line in enumerate(lines):
                p = cell.paragraphs[0] if l_idx == 0 else cell.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                is_alert = "LƯU Ý" in line
                alert_color = RGBColor(180, 40, 20) if is_alert else None
                add_line_with_math(p, line, font_size=10.5, default_bold=is_alert, default_color=alert_color)

    doc.add_paragraph()
    
    # Section 3: 4 Trọng tâm sư phạm
    p_h3 = doc.add_paragraph()
    r = p_h3.add_run("PHẦN III: BỐN (04) TRỌNG TÂM SƯ PHẠM ĐÃ CẬP NHẬT BẢN VÁ EQUATION")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(180, 40, 20)
    
    recs = [
        ("1. Bẫy nghiệm ngoại lai Bài 1.i:", [
            "Phương trình: $\\frac{x - 1}{x - 3} - \\frac{x + 3}{x - 1} = \\frac{8x}{(x - 3)(x - 1)}$.",
            "ĐKXĐ: $x \\ne 3, x \\ne 1$. Quy đồng rút gọn ra $10x = 10 \\Leftrightarrow x = 1$ (LOẠI).",
            "⇒ Kết luận: Phương trình VÔ NGHIỆM ($S = \\emptyset$)."
        ]),
        ("2. Góc đặc biệt Bài 1.3 Biểu thức B:", [
            "Đề bài ghi: $B = \\tan 65^\\circ - \\sin 30^\\circ + \\frac{\\sin 45^\\circ \\cdot \\sin 60^\\circ}{\\tan 45^\\circ}$.",
            "⇒ Đã vá: Đổi $\\tan 65^\\circ$ thành $\\tan 60^\\circ$ để biểu thức tính toán được bằng góc đặc biệt."
        ]),
        ("3. Mô hình hình học Bài 5 (Thùng xe chở rác):", [
            "Hình 4 thùng xe nâng 4m, đáy 5m. Đã bổ sung giả thiết tam giác vuông tại chân thùng nâng để tính $\\cos \\alpha = \\frac{4}{5} = 0,8 \\Rightarrow \\alpha \\approx 36^\\circ 52'$."
        ]),
        ("4. Đơn vị vận tốc thực tế Bài 8.b (Con dốc):", [
            "Đề ghi: 'vận tốc lên dốc $4\\text{ hm/h}$' ($= 0,4\\text{ km/h}$). Đã vá thành $4\\text{ km/h}$ để sát với đời sống."
        ])
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
            
    doc.add_paragraph()
    
    # Signature
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
    
    # Save both to Phan_Bien_Toan_9.docx and Phan_Bien_De_Cuong_Toan_9.docx
    paths = [
        r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\4_DUYET_DE\Ket_qua\14.10\Phan_Bien_Toan_9.docx",
        r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\4_DUYET_DE\Ket_qua\Phan_Bien_Toan_9.docx",
        r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\4_DUYET_DE\Ket_qua\14.10\Phan_Bien_De_Cuong_Toan_9.docx",
        r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\4_DUYET_DE\Ket_qua\Phan_Bien_De_Cuong_Toan_9.docx"
    ]
    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        doc.save(p)
        print("Saved Master Equation doc to:", p)

if __name__ == "__main__":
    create_master_report()
