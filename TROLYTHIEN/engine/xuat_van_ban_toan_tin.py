# -*- coding: utf-8 -*-
"""
HỆ THỐNG XUẤT VĂN BẢN WORD (.DOCX) CHUẨN NGHỊ ĐỊNH 30/2020/NĐ-CP
CHO TỔ TOÁN - TIN HỌC - TRƯỜNG THCS TRẦN PHÚ
Chuyên dụng cho:
1. Biên bản họp tổ Toán - Tin (3 phần chuẩn: Triển khai văn bản, Đánh giá, Công tác tới).
2. Báo cáo & Kế hoạch hoạt động tổ theo tháng (Form chuẩn trường THCS Trần Phú).
Tính năng đặc biệt: Tự động in chữ MÀU ĐỎ cho mọi nội dung chưa chắc chắn hoặc đánh dấu [CHỮ ĐỎ: ...].
"""

import os
import re
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

COLOR_BLACK = RGBColor(0, 0, 0)
COLOR_RED = RGBColor(220, 20, 20)  # Đỏ nổi bật chuẩn văn bản


def create_nd30_document():
    """Khởi tạo tài liệu Word chuẩn thể thức Nghị định 30/2020/NĐ-CP."""
    doc = docx.Document()
    
    # Định lề trang A4: Trên 20mm, Dưới 20mm, Trái 30mm, Phải 15mm
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.79)     # ~20 mm
        section.bottom_margin = Inches(0.79)  # ~20 mm
        section.left_margin = Inches(1.18)    # ~30 mm
        section.right_margin = Inches(0.59)   # ~15 mm
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
    
    return doc


def set_cell_border(cell, **kwargs):
    """
    Thiết lập viền ô bảng theo chuẩn XML của Microsoft Word.
    Các thuộc tính: top, bottom, left, right: dict(val='single', sz='4', color='000000')
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn(f'w:{key}'), str(val))


def format_table_borders_closed(table):
    """
    Đóng khung kín 4 cạnh viền ngoài và các đường kẻ bên trong theo chuẩn NĐ 30.
    Chống xé dòng (cantSplit) và lặp lại dòng tiêu đề khi sang trang (tblHeader).
    """
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    border_spec = {
        'val': 'single',
        'sz': '4',         # 0.5 pt
        'space': '0',
        'color': '000000'   # Đen
    }
    
    # Thiết lập viền cho toàn bộ ô
    for row_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(r'<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
        
        if row_idx == 0:
            trPr.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
            
        for cell in row.cells:
            set_cell_border(
                cell,
                top=border_spec,
                bottom=border_spec,
                left=border_spec,
                right=border_spec
            )


def set_table_no_borders(table):
    """Bỏ toàn bộ viền bảng (dùng cho bảng Header và Chữ ký)."""
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


def add_run_parsed(paragraph, text, default_size=13, default_bold=False, default_italic=False, force_red=False):
    """
    Rà soát và thêm run văn bản.
    Tự động nhận diện cú pháp:
    - [CHỮ ĐỎ: ...] hoặc [ĐỎ: ...] hoặc <red>...</red> -> in màu ĐỎ (RGB 220, 20, 20)
    - **in đậm** -> run.bold = True
    - *in nghiêng* -> run.italic = True
    """
    if force_red:
        run = paragraph.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(default_size)
        run.bold = default_bold
        run.italic = default_italic
        run.font.color.rgb = COLOR_RED
        return

    pattern = r'(\[CHỮ ĐỎ:[^\]]+\]|\[ĐỎ:[^\]]+\]|<red>[^<]+</red>)'
    parts = re.split(pattern, text)
    
    for part in parts:
        if not part:
            continue
            
        is_red_chunk = False
        chunk_text = part
        
        m_tag1 = re.match(r'\[CHỮ ĐỎ:\s*(.+)\]$', part, re.DOTALL)
        m_tag2 = re.match(r'\[ĐỎ:\s*(.+)\]$', part, re.DOTALL)
        m_tag3 = re.match(r'<red>(.+)</red>$', part, re.DOTALL)
        
        if m_tag1:
            is_red_chunk = True
            chunk_text = m_tag1.group(1).strip()
        elif m_tag2:
            is_red_chunk = True
            chunk_text = m_tag2.group(1).strip()
        elif m_tag3:
            is_red_chunk = True
            chunk_text = m_tag3.group(1).strip()
            
        run = paragraph.add_run(chunk_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(default_size)
        run.bold = default_bold
        run.italic = default_italic
        if is_red_chunk:
            run.font.color.rgb = COLOR_RED
        else:
            run.font.color.rgb = COLOR_BLACK


def add_paragraph_styled(doc, text, bold_prefix="", indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=2, line_spacing=1.2, force_red=False):
    """Thêm một đoạn văn bản chuẩn thể thức Nghị định 30."""
    p = doc.add_paragraph()
    p.paragraph_format.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.5)  # 1.27 cm
        
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + (" " if not bold_prefix.endswith(" ") else ""))
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_RED if force_red else COLOR_BLACK
        
    add_run_parsed(p, text, default_size=13, default_bold=False, default_italic=False, force_red=force_red)
    return p


def add_header_thcs_tran_phu(doc, so_hieu="01/BC - TCM", ngay_thang_str="Xuân Đông, ngày 28 tháng 9 năm 2026"):
    """Thêm Header chuẩn trường THCS Trần Phú (Đã bỏ cấp Phòng GD&ĐT)."""
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_no_borders(table)
    
    cell_l, cell_r = table.rows[0].cells
    cell_l.width = Inches(2.9)
    cell_r.width = Inches(3.9)
    
    # Cột trái
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.15
    p_l.paragraph_format.space_before = Pt(0)
    p_l.paragraph_format.space_after = Pt(0)
    
    r1 = p_l.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.bold = True
    
    r2 = p_l.add_run("TỔ TOÁN - TIN HỌC\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.bold = True
    
    r_so = p_l.add_run(f"Số: {so_hieu}\n")
    r_so.font.name = 'Times New Roman'
    r_so.font.size = Pt(11)
    r_so.italic = True
    
    # Cột phải
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.15
    p_r.paragraph_format.space_before = Pt(0)
    p_r.paragraph_format.space_after = Pt(0)
    
    r3 = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(11.5)
    r3.bold = True
    
    r4 = p_r.add_run("Độc lập – Tự do – Hạnh phúc\n")
    r4.font.name = 'Times New Roman'
    r4.font.size = Pt(12)
    r4.bold = True
    
    r5 = p_r.add_run("──────────────────\n")
    r5.font.name = 'Times New Roman'
    r5.font.size = Pt(9)
    r5.bold = True
    
    r6 = p_r.add_run(f"{ngay_thang_str}")
    r6.font.name = 'Times New Roman'
    r6.font.size = Pt(12)
    r6.italic = True
    
    # Dãn cách sau header
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(6)
    p_sp.paragraph_format.space_after = Pt(2)


def add_doc_title(doc, main_title, sub_title=""):
    """Tiêu đề chính giữa, in hoa, đậm."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    
    r = p.add_run(f"{main_title}\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True
    
    if sub_title:
        r_sub = p.add_run(f"{sub_title}\n")
        r_sub.font.name = 'Times New Roman'
        r_sub.font.size = Pt(13)
        r_sub.bold = True


def add_can_cu(doc, can_cu_list):
    """Căn cứ ban hành: Chữ nghiêng 13pt, lùi đầu dòng 1.27cm."""
    for idx, cc in enumerate(can_cu_list):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.first_line_indent = Inches(0.5)
        
        # Dấu kết thúc: dấu phẩy nếu chưa hết, dấu chấm nếu là dòng cuối
        suffix = "." if idx == len(can_cu_list) - 1 else ";"
        text_full = cc.strip()
        if not text_full.endswith(('.', ';', ',')):
            text_full += suffix
            
        r = p.add_run(text_full)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.italic = True


def add_section_h1(doc, text):
    """Tiêu đề phần La Mã: I. , II. , III."""
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True


def add_section_h2(doc, text):
    """Tiêu đề mục số: 1. Chủ nhiệm, 2. Ngày giờ công..."""
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True


def add_signatures(doc, left_title="Ban giám hiệu", left_name="", right_title="Tổ trưởng", right_name="Hoàng Tấn Thiên"):
    """Thêm phần chữ ký 2 bên chuẩn form (không viền)."""
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(10)
    p_sp.paragraph_format.space_after = Pt(2)
    
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_no_borders(table)
    
    cell_l1, cell_r1 = table.rows[0].cells
    cell_l2, cell_r2 = table.rows[1].cells
    cell_l1.width = Inches(3.4)
    cell_r1.width = Inches(3.4)
    cell_l2.width = Inches(3.4)
    cell_r2.width = Inches(3.4)
    
    # Hàng chức vụ
    p_l1 = cell_l1.paragraphs[0]
    p_l1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_lt = p_l1.add_run(f"{left_title}\n")
    r_lt.font.name = 'Times New Roman'
    r_lt.font.size = Pt(13)
    r_lt.bold = True
    
    p_r1 = cell_r1.paragraphs[0]
    p_r1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rt = p_r1.add_run(f"{right_title}\n")
    r_rt.font.name = 'Times New Roman'
    r_rt.font.size = Pt(13)
    r_rt.bold = True
    
    # Hàng họ tên (cách 3-4 dòng để ký)
    p_l2 = cell_l2.paragraphs[0]
    p_l2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l2.paragraph_format.space_before = Pt(45)
    if left_name:
        r_ln = p_l2.add_run(left_name)
        r_ln.font.name = 'Times New Roman'
        r_ln.font.size = Pt(13)
        r_ln.bold = True
        
    p_r2 = cell_r2.paragraphs[0]
    p_r2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r2.paragraph_format.space_before = Pt(45)
    if right_name:
        r_rn = p_r2.add_run(right_name)
        r_rn.font.name = 'Times New Roman'
        r_rn.font.size = Pt(13)
        r_rn.bold = True


def add_thi_dua_table(doc, rows_data=None):
    """
    Thêm bảng III. Đánh giá thi đua trong tháng theo đúng 7 cột chuẩn form ảnh THCS Trần Phú.
    Khung viền kín 4 cạnh và các đường kẻ trong, cantSplit và tblHeader.
    Tự động in chữ MÀU ĐỎ cho mọi nội dung đánh dấu [CHỮ ĐỎ: ...].
    """
    headers = [
        "STT", "HỌ VÀ TÊN", "CHỨC VỤ", "TỰ XẾP LOẠI", "TỰ NHẬN XÉT", "TỔ XẾP LOẠI", "GHI CHÚ"
    ]
    # Độ rộng xấp xỉ cho khổ ngang 6.8 inch khả dụng (A4 lề trái 30mm, phải 15mm)
    col_widths = [Inches(0.45), Inches(1.15), Inches(0.75), Inches(0.65), Inches(1.6), Inches(0.65), Inches(1.55)]
    
    if not rows_data:
        rows_data = [
            (
                "1",
                "Hoàng Tấn Thiên",
                "Tổ trưởng",
                "A",
                "Lên kế hoạch kịp thời, đúng tiến độ. Hoàn thành tốt công tác soạn giảng, thực hiện tốt quy chế chuyên môn, nhà trường. Ngày giờ công đảm bảo, thông tin 2 chiều kịp thời và chính xác.",
                "A",
                "Lên kế hoạch kịp thời, đúng tiến độ. Hoàn thành tốt công tác soạn giảng, thực hiện tốt quy chế chuyên môn, nhà trường. Ngày giờ công đảm bảo, thông tin 2 chiều kịp thời và chính xác."
            ),
            (
                "2",
                "[CHỮ ĐỎ: Hồ Đăng Danh]",
                "[CHỮ ĐỎ: Giáo viên]",
                "[CHỮ ĐỎ: A]",
                "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ giảng dạy và công tác được giao.]",
                "[CHỮ ĐỎ: A]",
                "[CHỮ ĐỎ: ...]"
            ),
            (
                "3",
                "[CHỮ ĐỎ: Trần Long Hải]",
                "[CHỮ ĐỎ: Giáo viên]",
                "[CHỮ ĐỎ: A]",
                "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, tích cực tham gia dạy thay.]",
                "[CHỮ ĐỎ: A]",
                "[CHỮ ĐỎ: ...]"
            ),
            (
                "4",
                "[CHỮ ĐỎ: (Chờ Thầy cung cấp thêm danh sách GV trong tổ)]",
                "[CHỮ ĐỎ: ...]",
                "[CHỮ ĐỎ: ...]",
                "[CHỮ ĐỎ: ...]",
                "[CHỮ ĐỎ: ...]",
                "[CHỮ ĐỎ: ...]"
            )
        ]

    table = doc.add_table(rows=len(rows_data) + 1, cols=7)
    format_table_borders_closed(table)
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.bold = True
        
    # Data Rows
    for row_idx, data_tuple in enumerate(rows_data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(data_tuple):
            row_cells[col_idx].width = col_widths[col_idx]
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            # Cột STT, Chức vụ, Xếp loại căn giữa; Cột Họ tên, Nhận xét căn đều/trái
            if col_idx in (0, 2, 3, 5):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif col_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                
            add_run_parsed(p, str(cell_value), default_size=11.5)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(2)


def add_bien_ban_signatures(doc, chu_tri="Hoàng Tấn Thiên", thu_ky="Lê Thị Bình"):
    """Phần chữ ký của Biên bản họp tổ: Thư ký (trái) và Chủ trì (phải)."""
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(10)
    p_sp.paragraph_format.space_after = Pt(2)
    
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_no_borders(table)
    
    cell_l1, cell_r1 = table.rows[0].cells
    cell_l2, cell_r2 = table.rows[1].cells
    cell_l1.width = Inches(3.4)
    cell_r1.width = Inches(3.4)
    cell_l2.width = Inches(3.4)
    cell_r2.width = Inches(3.4)
    
    # Hàng chức danh
    p_l1 = cell_l1.paragraphs[0]
    p_l1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_lt = p_l1.add_run("THƯ KÝ\n")
    r_lt.font.name = 'Times New Roman'
    r_lt.font.size = Pt(13)
    r_lt.bold = True
    
    p_r1 = cell_r1.paragraphs[0]
    p_r1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rt = p_r1.add_run("CHỦ TRÌ CUỘC HỌP\n(TỔ TRƯỞNG)\n")
    r_rt.font.name = 'Times New Roman'
    r_rt.font.size = Pt(13)
    r_rt.bold = True
    
    # Hàng họ tên
    p_l2 = cell_l2.paragraphs[0]
    p_l2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l2.paragraph_format.space_before = Pt(45)
    r_ln = p_l2.add_run(thu_ky)
    r_ln.font.name = 'Times New Roman'
    r_ln.font.size = Pt(13)
    r_ln.bold = True
    
    p_r2 = cell_r2.paragraphs[0]
    p_r2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r2.paragraph_format.space_before = Pt(45)
    r_rn = p_r2.add_run(chu_tri)
    r_rn.font.name = 'Times New Roman'
    r_rn.font.size = Pt(13)
    r_rn.bold = True

