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


def save_docx_robust(doc, out_docx_path):
    """Lưu tệp docx an toàn, nếu tệp đang bị khóa (ví dụ do mở trong Word), lưu dự phòng có hậu tố _Cap_Nhat."""
    p = Path(out_docx_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        doc.save(str(p))
        return str(p)
    except PermissionError:
        fallback = p.with_name(p.stem + "_Cap_Nhat" + p.suffix)
        doc.save(str(fallback))
        print(f"[THONG BAO] Tep {p.name} dang mo trong Word nen da luu vao: {fallback.name}")
        return str(fallback)


def safe_copy2(src, dst):
    """Sao chép tệp an toàn, tự động xử lý khi có tệp _Cap_Nhat hoặc tệp đích bị khóa."""
    src_p = Path(src)
    if not src_p.exists():
        fallback_src = src_p.with_name(src_p.stem + "_Cap_Nhat" + src_p.suffix)
        if fallback_src.exists():
            src_p = fallback_src
            
    dst_p = Path(dst)
    dst_p.parent.mkdir(parents=True, exist_ok=True)
    
    # Thử copy trực tiếp
    try:
        with open(src_p, 'rb') as fsrc:
            content = fsrc.read()
        with open(dst_p, 'wb') as fdst:
            fdst.write(content)
    except PermissionError:
        fallback_dst = dst_p.with_name(dst_p.stem + "_Cap_Nhat" + dst_p.suffix)
        with open(fallback_dst, 'wb') as fdst:
            fdst.write(content)
        print(f"[THONG BAO] Tep {dst_p.name} dang mo trong Word nen da sao chep vao: {fallback_dst.name}")


def create_nd30_document():
    """Khởi tạo tài liệu Word chuẩn thể thức Nghị định 30/2020/NĐ-CP (Cỡ 14, Firstline 1.27cm)."""
    doc = docx.Document()
    
    # Định lề trang A4 chuẩn: Trên 20mm, Dưới 20mm, Trái 30mm, Phải 15mm
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
    normal_style.font.size = Pt(14)
    normal_style.font.color.rgb = COLOR_BLACK
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_before = Pt(2)
    normal_style.paragraph_format.space_after = Pt(2)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal_style.paragraph_format.first_line_indent = Inches(0.5)  # 1.27 cm
    
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


def add_run_parsed(paragraph, text, default_size=14, default_bold=False, default_italic=False, force_red=False):
    """
    Rà soát và thêm run văn bản chuẩn NĐ 30 cỡ 14.
    Tự động nhận diện cú pháp:
    - [CHỮ ĐỎ: ...] hoặc [ĐỎ: ...] hoặc <red>...</red> -> in màu ĐỎ (RGB 220, 20, 20)
    - **in đậm** -> run.bold = True (loại bỏ dấu **)
    - **in nghiêng:** -> run.italic = True (loại bỏ dấu *)
    """
    pattern_red = r'(\[CHỮ ĐỎ:[^\]]+\]|\[ĐỎ:[^\]]+\]|<red>[^<]+</red>)'
    parts = re.split(pattern_red, text)
    
    for part in parts:
        if not part:
            continue
            
        is_red_chunk = force_red
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
            
        token_pattern = r'(\*\*[^*]+\*\*|\*[^\s*][^*]*\*)'
        sub_tokens = re.split(token_pattern, chunk_text)
        
        for tok in sub_tokens:
            if not tok:
                continue
            run_bold = default_bold
            run_italic = default_italic
            run_text = tok
            
            if tok.startswith('**') and tok.endswith('**') and len(tok) >= 4:
                run_bold = True
                run_italic = False  # Đề mục in đậm TUYỆT ĐỐI KHÔNG IN NGHIÊNG
                run_text = tok[2:-2]
            elif tok.startswith('*') and tok.endswith('*') and len(tok) >= 2 and not tok.startswith('* '):
                run_italic = True
                run_text = tok[1:-1]
                
            run = paragraph.add_run(run_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(default_size)
            run.bold = run_bold
            run.italic = run_italic
            if is_red_chunk:
                run.font.color.rgb = COLOR_RED
            else:
                run.font.color.rgb = COLOR_BLACK


def add_paragraph_styled(doc, text, bold_prefix="", indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=2, line_spacing=1.2, force_red=False, size=14):
    """Thêm một đoạn văn bản chuẩn thể thức Nghị định 30 (cỡ 14, thụt đầu dòng 1.27cm)."""
    text_clean = text.strip()
    # Tự động chuẩn hóa: nếu văn bản bắt đầu bằng số thứ tự rồi mới đến bold (ví dụ: "1. **Tiêu đề**" hoặc "1.1. **Tiêu đề**"),
    # gộp số thứ tự vào bên trong cặp dấu ** để số thứ tự cũng được in đậm đồng nhất theo NĐ 30, không bị số in thường / chữ in đậm.
    text_clean = re.sub(r'^([0-9IVXLCDM]+(?:\.[0-9]+)*\.)\s*\*\*([^*]+)\*\*', r'**\1 \2**', text_clean)

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
        r_pre.font.size = Pt(size)
        r_pre.bold = True
        r_pre.italic = False  # Đề mục in đậm không in nghiêng
        r_pre.font.color.rgb = COLOR_RED if force_red else COLOR_BLACK
        
    add_run_parsed(p, text_clean, default_size=size, default_bold=False, default_italic=False, force_red=force_red)
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
        r_sub.font.size = Pt(14)
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


def add_section_h1(doc, text, size=14):
    """Tiêu đề phần La Mã: I. , II. , III. theo NĐ 30: Cỡ 14, In đậm, ĐỨNG (không nghiêng), Thụt đầu dòng 1.27cm."""
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.first_line_indent = Inches(0.5)  # 1.27 cm
    p.paragraph_format.keep_with_next = True
    
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(size)
    r.bold = True
    r.italic = False  # In đậm không nghiêng


def add_section_h2(doc, text, size=14):
    """Tiêu đề mục số: 1., 2., 3. theo NĐ 30: Cỡ 14, In đậm, ĐỨNG (không nghiêng), Thụt đầu dòng 1.27cm."""
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.first_line_indent = Inches(0.5)  # 1.27 cm
    p.paragraph_format.keep_with_next = True
    
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(size)
    r.bold = True
    r.italic = False  # In đậm không nghiêng


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


def add_day_thay_table(doc, rows_data):
    """Bảng chi tiết tình hình dạy thay trong tháng (NĐ 30: viền kín, cantSplit, tblHeader)."""
    headers = ["STT", "Ngày & Buổi", "Tiết & Lớp", "Số tiết", "GV thực dạy", "Thay cho GV", "Lý do"]
    col_widths = [Inches(0.4), Inches(1.0), Inches(1.4), Inches(0.6), Inches(1.0), Inches(1.0), Inches(1.4)]
    
    table = doc.add_table(rows=len(rows_data) + 1, cols=7)
    format_table_borders_closed(table)
    
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
        
    for row_idx, data_tuple in enumerate(rows_data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(data_tuple):
            row_cells[col_idx].width = col_widths[col_idx]
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            if col_idx in (0, 1, 3, 4, 5):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            add_run_parsed(p, str(cell_value), default_size=11.5)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(2)


def add_phan_cong_ra_de_table(doc, rows_data):
    """Bảng phân công ra đề, phản biện kiểm tra giữa kỳ I (NĐ 30: viền kín, cantSplit, tblHeader)."""
    headers = ["STT", "Khối & Môn", "Người biên soạn", "Người phản biện", "Hình thức & Lịch kiểm tra", "Hạn nộp BGH"]
    col_widths = [Inches(0.4), Inches(1.0), Inches(1.3), Inches(1.2), Inches(1.9), Inches(1.0)]
    
    table = doc.add_table(rows=len(rows_data) + 1, cols=6)
    format_table_borders_closed(table)
    
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
        
    for row_idx, data_tuple in enumerate(rows_data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(data_tuple):
            row_cells[col_idx].width = col_widths[col_idx]
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            if col_idx in (0, 1, 5):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            add_run_parsed(p, str(cell_value), default_size=11.5)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(2)


def tao_bien_ban_hop_to_lan_2_thang_10(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 2 Tháng 10/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="03/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 23 tháng 10 năm 2026"
    )
    
    # Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 2",
        "NỘI DUNG SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 10/2026\nNăm học: 2026 - 2027"
    )
    
    # Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 14 giờ 00 phút, ngày 23 tháng 10 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 2 tháng 10 năm học 2026 - 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên quán triệt, phổ biến và cụ thể hóa các văn bản chỉ đạo của cấp trên và nhà trường gắn với nhiệm vụ chuyên môn của Tổ Toán – Tin học như sau:", indent=True)
    
    # 1. Văn bản STEM (Thông tư 86 & CV Sở GD&ĐT Đồng Nai)
    add_paragraph_styled(doc, "Thông tư số 86/2026/TT-BGDĐT ngày 30/9/2026 của Bộ Giáo dục và Đào tạo quy định về tổ chức hoạt động giáo dục tích hợp khoa học, công nghệ, kĩ thuật và toán học (giáo dục STEM) trong giáo dục phổ thông và Công văn hướng dẫn ngày 19/10/2026 của Sở Giáo dục và Đào tạo Đồng Nai về triển khai thực hiện Thông tư số 86/2026/TT-BGDĐT (kết hợp Công văn số 7206/BGDĐT-GDPT và Bộ Tài liệu giáo dục STEM cấp THCS: Tập 1 Phần chung, Tập 2B THCS).", bold_prefix="1. Triển khai Thông tư số 86/2026/TT-BGDĐT và chỉ đạo của Sở GD&ĐT về Giáo dục STEM:", indent=True)
    add_paragraph_styled(doc, "- Quán triệt 3 nguyên tắc chỉ đạo trọng tâm của Sở GD&ĐT:", indent=True)
    add_paragraph_styled(doc, "  + Không yêu cầu xây dựng, phê duyệt kế hoạch riêng về giáo dục STEM; không làm phát sinh môn học, thời lượng học tập bắt buộc, đầu điểm, hồ sơ sổ sách riêng ngoài quy định.", indent=True)
    add_paragraph_styled(doc, "  + Bài học STEM được tổ chức tích hợp trực tiếp trong quá trình dạy học môn Toán và môn Tin học; bám sát mục tiêu, yêu cầu cần đạt của Chương trình GDPT 2018 và giải quyết các vấn đề thực tiễn gắn với đời sống, nghề nghiệp.", indent=True)
    add_paragraph_styled(doc, "  + Đánh giá kết quả học tập qua bài học STEM theo quy định hiện hành áp dụng đối với từng môn học (Thông tư 22/2021/TT-BGDĐT); kết hợp tự đánh giá và đánh giá sản phẩm của học sinh, tuyệt đối không đánh giá, xếp loại riêng ngoài quy định.", indent=True)
    
    # 2. GDQP&AN (Thông báo Sở GD&ĐT Đồng Nai 20/10/2026)
    add_paragraph_styled(doc, "Thông báo ngày 20/10/2026 của Sở Giáo dục và Đào tạo Đồng Nai về Kết luận sau tập huấn cán bộ quản lý, giáo viên về lồng ghép nội dung Giáo dục quốc phòng và an ninh (GDQP&AN) trong trường tiểu học, trung học cơ sở năm 2026 (thực hiện Thông tư số 08/2024/TT-BGDĐT ngày 15/5/2024 của Bộ GD&ĐT).", bold_prefix="2. Triển khai lồng ghép Giáo dục quốc phòng và an ninh (GDQP&AN):", indent=True)
    add_paragraph_styled(doc, "- Định hướng chuyên môn lồng ghép trong Tổ Toán – Tin học:", indent=True)
    add_paragraph_styled(doc, "  + Nguyên tắc: Vận dụng linh hoạt, nhẹ nhàng, tự nhiên, phù hợp với tâm lý lứa tuổi học sinh THCS, không gây quá tải hoặc làm ảnh hưởng đến mục tiêu và thời lượng của môn học; lựa chọn học liệu từ nguồn chính thống, chính xác.", indent=True)
    add_paragraph_styled(doc, "  + Đối với môn Toán: Lồng ghép qua các bài toán thực tiễn về tính toán khoảng cách, cự ly, hình học đo đạc, số liệu biểu đồ thống kê gắn với truyền thống lịch sử dựng nước, giữ nước và sức mạnh quốc phòng toàn dân.", indent=True)
    add_paragraph_styled(doc, "  + Đối với môn Tin học: Tích hợp giáo dục ý thức bảo đảm an toàn thông tin, an ninh mạng, giữ gìn dữ liệu cá nhân và bảo mật thông tin số; nâng cao tinh thần cảnh giác trước thông tin xấu độc, lừa đảo trực tuyến và tội phạm công nghệ cao theo Luật An ninh mạng.", indent=True)
    
    # 3. GD Liêm chính
    add_paragraph_styled(doc, "Kế hoạch số 116/KH-THCS.TP ngày 21/10/2026 của Trường THCS Trần Phú về chỉ đạo thực hiện nội dung giáo dục liêm chính, phòng chống tham nhũng, tiêu cực và tiết kiệm, chống lãng phí năm học 2026 - 2027 (căn cứ Quyết định số 2907/QĐ-BGDĐT ngày 05/10/2026 của Bộ GD&ĐT).", bold_prefix="3. Kế hoạch Giáo dục Liêm chính, phòng chống tham nhũng, lãng phí:", indent=True)
    add_paragraph_styled(doc, "- Tổ Toán – Tin học xác định địa chỉ tích hợp tự nhiên, không gượng ép: Rèn luyện cho học sinh đức tính trung thực, tính chính xác khoa học, công bằng, tuyệt đối không gian lận trong kiểm tra thi cử và học tập; thực hành tiết kiệm thời gian, tiết kiệm giấy mực, có ý thức giữ gìn tài sản chung của nhà trường và bảo vệ tài nguyên số.", indent=True)
    
    # 4. Học tập tư tưởng Bác
    add_paragraph_styled(doc, "Kế hoạch số 121/KH-THCS.TP ngày 19/10/2026 của Trường THCS Trần Phú về tích hợp học tập, làm theo tư tưởng, đạo đức, phong cách Hồ Chí Minh năm học 2026 - 2027 (căn cứ Quyết định số 2995/QĐ-BGDĐT ngày 13/10/2026 của Bộ GD&ĐT).", bold_prefix="4. Kế hoạch Tích hợp học tập làm theo tư tưởng, đạo đức, phong cách Hồ Chí Minh:", indent=True)
    add_paragraph_styled(doc, "- Lồng ghép vào môn Khoa học Tự nhiên và Toán học: Rèn luyện phương pháp làm việc khoa học, tác phong cẩn thận, tư duy độc lập và sáng tạo.", indent=True)
    add_paragraph_styled(doc, "- Đặc biệt, giáo viên lồng ghép các chỉ báo Khung Năng lực số (NLS) và Khung Trí tuệ nhân tạo (AI) vào bài giảng, hướng dẫn học sinh ứng dụng công cụ AI một cách hợp lý, đúng mực và có trách nhiệm trong học tập.", indent=True)
    
    # 5. Kế hoạch nhiệm vụ & Quy chế làm việc
    add_paragraph_styled(doc, "Kế hoạch số 124/KH-THCS.TP ngày 19/10/2026 về Thực hiện nhiệm vụ năm học 2026 - 2027 và Quyết định số 183/QĐ-THCS.TP ngày 19/10/2026 của Hiệu trưởng Trường THCS Trần Phú ban hành Quy chế làm việc năm học 2026 - 2027.", bold_prefix="5. Kế hoạch nhiệm vụ năm học và Quy chế làm việc của cơ quan:", indent=True)
    add_paragraph_styled(doc, "- Quán triệt 100% cán bộ, giáo viên trong tổ thực hiện nghiêm túc ngày giờ công, giờ lên lớp, tác phong sư phạm mẫu mực, không vi phạm quy chế chuyên môn, hoàn thành các loại hồ sơ sổ sách đúng tiến độ.", indent=True)
    
    # 6. Cuộc thi Đồng Nai vươn mình
    add_paragraph_styled(doc, "Kế hoạch số 125/KH-THCS.TP ngày 20/10/2026 của Trường THCS Trần Phú triển khai Cuộc thi trực tuyến “Đồng Nai vươn mình trong kỷ nguyên mới” (tìm hiểu Nghị quyết số 16-NQ/TW ngày 21/7/2026 của Bộ Chính trị theo Kế hoạch 05-KH/BTGTU của Ban Tuyên giáo Thành ủy Đồng Nai).", bold_prefix="6. Cuộc thi trực tuyến “Đồng Nai vươn mình trong kỷ nguyên mới”:", indent=True)
    add_paragraph_styled(doc, "- Yêu cầu 100% giáo viên trong tổ tham gia thi trực tuyến nghiêm túc, đạt chất lượng cao; báo cáo tiến độ và kết quả về Tổ trưởng theo dõi.", indent=True)
    
    # 7. Đôn đốc an ninh mạng PA05
    add_paragraph_styled(doc, "Công văn số 3791/CATP-PA05 của Công an thành phố Đồng Nai về việc triển khai khóa học an ninh mạng, dữ liệu cá nhân, AI trên nền tảng Bình dân học vụ số (https://huanluyenanninhmang.mobifone.vn): Đôn đốc các giáo viên đã đăng ký khẩn trương hoàn thành các bài học và bài kiểm tra trực tuyến để nhận chứng nhận hoàn thành khóa học.", bold_prefix="7. Khóa học an ninh mạng, dữ liệu cá nhân và AI trên nền tảng số:", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ CÔNG TÁC GIAI ĐOẠN QUA")
    
    # 1. KHBD
    add_section_h2(doc, "1. Hồ sơ chuyên môn và Kế hoạch bài dạy (KHBD)")
    add_paragraph_styled(doc, "- Công tác soạn bài theo Công văn 5512/BGDĐT-GDTrH: Toàn thể giáo viên trong tổ thực hiện nghiêm túc, soạn bài đầy đủ trước khi lên lớp, bám sát yêu cầu cần đạt của Chương trình GDPT 2018.", indent=True)
    add_paragraph_styled(doc, "- Tích hợp Khung Năng lực số (NLS 20%) và Khung AI (12 tiết): Giáo viên chủ động đưa mục tiêu và chỉ báo năng lực vào tiến trình hoạt động dạy học, thể hiện in đậm nghiêng rõ nét trong KHBD.", indent=True)
    add_paragraph_styled(doc, "- Đưa KHBD lên Cơ sở dữ liệu ngành và ký số: Các đồng chí hoàn thành cơ bản đáp ứng yêu cầu tiến độ theo quy định của nhà trường, đảm bảo hồ sơ số phê duyệt kịp thời.", indent=True)
    
    # 2. Ngày giờ công
    add_section_h2(doc, "2. Nề nếp giảng dạy và thực hiện ngày giờ công")
    add_paragraph_styled(doc, "- Giáo viên chấp hành tốt kỷ luật lao động, đảm bảo ngày giờ công, không đi trễ về sớm, không cắt xén chương trình.", indent=True)
    add_paragraph_styled(doc, "- Thực hiện đúng quy định kiểm tra đánh giá thường xuyên theo Thông tư 22/2021/TT-BGDĐT, ghi sổ đầu bài khớp lịch trình giảng dạy.", indent=True)
    
    # 3. Dạy thay
    add_section_h2(doc, "3. Tình hình dạy thay giáo viên đi công tác / tập huấn")
    add_paragraph_styled(doc, "Trong giai đoạn qua của tháng 10, do phân công công tác đột xuất của cấp trên và địa phương, tổ đã chủ động sắp xếp dạy thay 05 lượt (tổng số 12 tiết dạy thay), đảm bảo đầy đủ quyền lợi học tập của học sinh, không để trống tiết. Chi tiết cụ thể như sau:", indent=True)
    
    day_thay_data = [
        ("1", "08/10/2026\n(Sáng)", "Tiết 1: 91 - Toán\nTiết 2: 91 - Toán\nTiết 4: 92 - Toán", "3", "Trần Sáng", "Hoàng Tấn Thiên", "Đi nộp hồ sơ an ninh mạng tại PA05 – Công an TP Đồng Nai"),
        ("2", "15/10/2026\n(Chiều)", "Tiết 8: 86 - HĐTN\nTiết 9: 86 - HĐTN", "2", "Nguyễn Văn Tính", "Đinh Văn Đông", "Đi họp tại UBND xã Xuân Đông"),
        ("3", "19/10/2026\n(Sáng)", "Tiết 2: 66 - Toán\nTiết 4: 95 - Toán", "2", "Đinh Văn Đông", "Trần Sáng", "Tham gia Hội thi Khuyến học"),
        ("4", "19/10/2026\n(Chiều)", "Tiết 7: 97 - Toán\nTiết 8: 96 - Toán", "2", "Hồ Đăng Danh", "Trần Sáng", "Tham gia Hội thi Khuyến học"),
        ("5", "21/10/2026\n(Sáng)", "Tiết 1: 61 - Toán\nTiết 2: 92 - Toán\nTiết 3: 91 - Toán", "3", "Lê Thị Bình", "Hoàng Tấn Thiên", "Đi kiểm tra hồ sơ đảng viên tại Đảng uỷ xã Xuân Đông")
    ]
    add_day_thay_table(doc, day_thay_data)
    add_paragraph_styled(doc, "Tổ tuyên dương tinh thần đoàn kết, sẵn sàng nhận nhiệm vụ và hỗ trợ đồng nghiệp kịp thời của các Thầy/Cô: Trần Sáng, Lê Thị Bình, Đinh Văn Đông, Hồ Đăng Danh, Nguyễn Văn Tính.", indent=True)
    
    # 4. Phòng máy
    add_section_h2(doc, "4. Quản lý phòng bộ môn và cơ sở vật chất")
    add_paragraph_styled(doc, "- Thầy Dương Quang Tùng duy trì bảo quản tốt hệ thống phòng máy vi tính, kiểm tra đường truyền mạng ổn định, chuẩn bị sẵn sàng cho kỳ kiểm tra giữa kỳ môn Tin học trên OLM.", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. CÔNG TÁC TỚI (KẾ HOẠCH TRỌNG TÂM THỜI GIAN TỚI)")
    
    # 1. Kiểm tra giữa kỳ I
    add_section_h2(doc, "1. Công tác Kiểm tra đánh giá Giữa học kỳ I năm học 2026 - 2027")
    add_paragraph_styled(doc, "Thực hiện Kế hoạch số 122/KH-THCS.TP ngày 19/10/2026 của Trường THCS Trần Phú về việc tổ chức kiểm tra, đánh giá giữa kỳ I, Tổ Toán – Tin học thống nhất triển khai kế hoạch cụ thể như sau:", indent=True)
    add_paragraph_styled(doc, "- Hình thức và lịch kiểm tra:", indent=True)
    add_paragraph_styled(doc, "  + Môn Tin học: Kiểm tra trực tuyến trên nền tảng OLM theo Thời khóa biểu trong Tuần 9 (từ ngày 02/11 đến ngày 06/11/2026).", indent=True)
    add_paragraph_styled(doc, "  + Môn Toán (khối 6, 7, 8, 9): Kiểm tra tập trung đồng loạt vào Sáng Thứ Sáu, ngày 13/11/2026 (Thời lượng 60 phút, từ 7 giờ 00 phút đến 8 giờ 00 phút).", indent=True)
    add_paragraph_styled(doc, "- Yêu cầu chuyên môn về đề kiểm tra: Bám sát chuẩn kiến thức, kỹ năng và yêu cầu cần đạt của Chương trình GDPT 2018 theo định dạng Công văn 7991/BGDĐT-GDTrH và hướng dẫn số 4096/SGDĐT-GDPT&GDTX Đồng Nai. Mỗi bộ môn/khối biên soạn 02 đề (01 đề chính thức, 01 đề dự phòng) kèm Ma trận, Bản đặc tả và Hướng dẫn chấm chi tiết.", indent=True)
    add_paragraph_styled(doc, "- Hạn chót nộp sản phẩm: Tổ chuyên môn thẩm định, ký duyệt và nộp toàn bộ đề, ma trận về Ban Giám hiệu duyệt in sao chậm nhất ngày **29/10/2026** (trước ngày 30/10/2026).", indent=True)
    add_paragraph_styled(doc, "- Phân công nhiệm vụ biên soạn và phản biện đề kiểm tra Giữa kỳ I:", indent=True)
    
    ra_de_data = [
        ("1", "Toán 6", "Hoàng Tấn Thiên\nNguyễn Thị Thảo", "Hồ Đăng Danh", "Tập trung (60 phút)\nSáng Thứ Sáu 13/11/2026", "29/10/2026"),
        ("2", "Toán 7", "Lê Thị Bình", "Hoàng Xuân Ánh", "Tập trung (60 phút)\nSáng Thứ Sáu 13/11/2026", "29/10/2026"),
        ("3", "Toán 8", "Trần Long Hải", "Lê Thị Bình", "Tập trung (60 phút)\nSáng Thứ Sáu 13/11/2026", "29/10/2026"),
        ("4", "Toán 9", "Trần Sáng", "Hoàng Tấn Thiên", "Tập trung (60 phút)\nSáng Thứ Sáu 13/11/2026", "29/10/2026"),
        ("5", "Tin học 6, 7, 8, 9", "Dương Quang Tùng", "Hoàng Tấn Thiên", "Trực tuyến OLM theo TKB\nTuần 9 (02/11 – 06/11/2026)", "29/10/2026")
    ]
    add_phan_cong_ra_de_table(doc, ra_de_data)
    add_paragraph_styled(doc, "- Nhập điểm kết quả kiểm tra lên Cơ sở dữ liệu ngành: Hoàn thành chậm nhất ngày **20/11/2026**.", indent=True)
    
    # 2. Rung chuông vàng 20/11
    add_section_h2(doc, "2. Phong trào thi đua chào mừng Ngày Nhà giáo Việt Nam 20/11 — Hội thi “Rung chuông vàng” môn Toán 6")
    add_paragraph_styled(doc, "Thực hiện Kế hoạch số 02/KH-TT ngày 15/10/2026 của Tổ Toán – Tin học về việc tổ chức Chuyên đề ngoại khóa “Rung chuông vàng” môn Toán khối 6 chào mừng kỷ niệm 44 năm Ngày Nhà giáo Việt Nam (20/11/1982 – 20/11/2026):", indent=True)
    add_paragraph_styled(doc, "- Thời gian tổ chức: Từ 14 giờ 00 phút đến 16 giờ 00 phút, chiều Thứ Sáu, ngày 13 tháng 11 năm 2026.", indent=True)
    add_paragraph_styled(doc, "- Địa điểm: Sân trường THCS Trần Phú.", indent=True)
    add_paragraph_styled(doc, "- Đối tượng: Toàn thể học sinh khối 6 (06 lớp). Mỗi lớp cử 05 học sinh xuất sắc tham gia thi đấu trên sàn đấu (tổng số 30 thí sinh); số học sinh còn lại là lực lượng cổ động viên và tham gia phần thi giao lưu khán giả.", indent=True)
    add_paragraph_styled(doc, "- Phân công trách nhiệm tổ chức:", indent=True)
    add_paragraph_styled(doc, "  + Trưởng ban tổ chức: Thầy **Hoàng Tấn Thiên** (chỉ đạo chung, phê duyệt thể lệ và thẩm định đề thi).", indent=True)
    add_paragraph_styled(doc, "  + Phó ban tổ chức: Thầy **Đinh Văn Đông** (chỉ đạo chuyên môn), Thầy **Trần Sáng** (phụ trách điều hành kịch bản, kiêm MC sàn đấu).", indent=True)
    add_paragraph_styled(doc, "  + Ban biên soạn ngân hàng câu hỏi: Cô **Nguyễn Thị Thảo** và Cô **Lê Thị Bình** biên soạn bộ 40 câu hỏi (30 câu chính thức, 05 câu phụ phân loại, 05 câu giao lưu khán giả; có tích hợp câu hỏi thực tiễn và thuật ngữ tiếng Anh toán học). Thẩm định hoàn tất trước ngày 22/10/2026.", indent=True)
    add_paragraph_styled(doc, "  + Ban Giám khảo, cứu trợ và hỗ trợ sân bãi: Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng chịu trách nhiệm chuẩn bị bảng con, bút viết, chuông, âm thanh, nước uống và điều phối cứu trợ thí sinh.", indent=True)
    
    # 3. NCBH
    add_section_h2(doc, "3. Sinh hoạt chuyên môn theo Nghiên cứu bài học (NCBH)")
    add_paragraph_styled(doc, "- Môn học và khối lớp: Môn **Toán khối 8**.", indent=True)
    add_paragraph_styled(doc, "- Người thực hiện dạy minh họa: Cô **Lê Thị Bình** chịu trách nhiệm thiết kế bài dạy nghiên cứu và tổ chức dạy thể nghiệm trên lớp.", indent=True)
    add_paragraph_styled(doc, "- Tiến trình thực hiện: Cả tổ tham gia đóng góp ý kiến thiết kế bài dạy, dự giờ tập trung quan sát hoạt động học của học sinh, tổ chức họp phân tích bài học và rút kinh nghiệm nhằm nâng cao phương pháp giảng dạy hình học/đại số 8.", indent=True)
    
    # 4. Điều chỉnh chuyên đề AI
    add_section_h2(doc, "4. Điều chỉnh Kế hoạch Chuyên đề Ứng dụng Trí tuệ nhân tạo (AI) trong dạy học (Chuyên đề Cụm)")
    add_paragraph_styled(doc, "- Điều chỉnh thời gian: Nhằm đáp ứng yêu cầu chuyển đổi số và nâng cao năng lực ứng dụng công nghệ của giáo viên trong toàn cụm, tổ thống nhất **điều chỉnh thời gian tổ chức Chuyên đề AI từ tháng 3/2027 chuyển sang tháng 12/2026**.", indent=True)
    add_paragraph_styled(doc, "- Phân công phụ trách chuyên đề cụm: Giao Cô **Lê Thị Bình** và Thầy **Trần Sáng** chịu trách nhiệm xây dựng báo cáo chuyên đề, thiết kế giáo án điện tử ứng dụng các công cụ AI hỗ trợ dạy học và trực tiếp dạy minh họa.", indent=True)
    add_paragraph_styled(doc, "- Toàn tổ tham gia hỗ trợ tư liệu, chạy thử phần mềm và chuẩn bị các điều kiện cơ sở vật chất tốt nhất cho chuyên đề cấp cụm.", indent=True)
    
    # 5. HSG, VioEdu, IOE
    add_section_h2(doc, "5. Công tác bồi dưỡng học sinh giỏi và các phong trào học tập trực tuyến")
    add_paragraph_styled(doc, "- Tiếp tục duy trì công tác bồi dưỡng đội tuyển học sinh giỏi Toán, Tin học theo kế hoạch của nhà trường.", indent=True)
    add_paragraph_styled(doc, "- Tiếp tục đẩy mạnh phong trào Đấu trường Toán học VioEdu và Olympic tiếng Anh (IOE) ở tất cả các khối lớp 6, 7, 8, 9, động viên học sinh tích cực tham gia các vòng tự luyện và vòng thi các cấp.", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: * Danh sách phân công giáo viên phụ trách bồi dưỡng HSG và các phong trào thi (chờ rà soát và cập nhật):]", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: + Khối 6: Giáo viên phụ trách: ........................................, Danh sách học sinh: ........................................]", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: + Khối 7: Giáo viên phụ trách: ........................................, Danh sách học sinh: ........................................]", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: + Khối 8: Giáo viên phụ trách: ........................................, Danh sách học sinh: ........................................]", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: + Khối 9: Giáo viên phụ trách: ........................................, Danh sách học sinh: ........................................]", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: + Phụ trách Đấu trường Toán học VioEdu: ........................................]", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: + Phụ trách Olympic tiếng Anh (IOE): ........................................]", indent=True)
    
    # 6. Công tác khác (Đọc sách)
    add_section_h2(doc, "6. Các công tác khác: Nâng cao văn hóa đọc và nề nếp chủ nhiệm")
    add_paragraph_styled(doc, "- Giáo viên bộ môn (Toán, Tin học): Chủ động phối hợp với Thư viện nhà trường bố trí và tiến hành các tiết đọc sách chuyên môn, hướng dẫn học sinh đọc sách tham khảo, tài liệu toán vui, lịch sử toán học và kiến thức khoa học công nghệ.", indent=True)
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm (Cô Thảo - 62, Cô Bình - 71, Thầy Hải - 83, Thầy Sáng - 97): Tích cực triển khai phong trào đọc sách tại lớp trong các tiết sinh hoạt lớp, duy trì nề nếp bảo quản tủ sách lớp học; tiếp tục bám sát nề nếp học tập, chuyên cần và đôn đốc các khoản thu theo quy định.", indent=True)
    
    # 7. Thi đua tổ
    add_section_h2(doc, "7. Đánh giá, xếp loại thi đua Tổ chuyên môn tháng 10/2026")
    add_paragraph_styled(doc, "Căn cứ kết quả thực hiện nhiệm vụ, ngày giờ công và tinh thần trách nhiệm trong công tác của các thành viên, Tổ Toán – Tin học thống nhất bảng xếp loại thi đua tháng 10/2026 như sau (các nội dung dự kiến in chữ màu đỏ để Thầy Tổ trưởng rà soát trước khi phê duyệt chính thức):", indent=True)
    
    thi_dua_data = [
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
            "Trần Sáng",
            "Tổ phó",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Thực hiện tốt giảng dạy môn Toán 6, 9; chủ nhiệm lớp 97 nghiêm túc; tích cực tham gia dạy thay 03 tiết Toán và chuẩn bị tốt kịch bản MC Rung chuông vàng.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, tích cực dạy thay.]"
        ),
        (
            "3",
            "Đinh Văn Đông",
            "Phó Hiệu trưởng",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Tham gia giảng dạy HĐTN 86 đầy đủ, đúng quy chế; tích cực chỉ đạo chuyên môn tổ và tham gia dạy thay 02 tiết Toán cho giáo viên trong tổ.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ giảng dạy và chỉ đạo chuyên môn.]"
        ),
        (
            "4",
            "Hồ Đăng Danh",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Thực hiện nghiêm túc tiến độ giảng dạy Toán 6, 9; hồ sơ sổ sách đầy đủ; tích cực tham gia dạy thay 02 tiết Toán 9 cho đồng nghiệp.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, hỗ trợ dạy thay kịp thời.]"
        ),
        (
            "5",
            "Hoàng Xuân Ánh",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Toán 7, HĐTN khối 6 đúng phân phối chương trình; nề nếp ngày giờ công đảm bảo, hồ sơ giáo án đầy đủ.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ được giao.]"
        ),
        (
            "6",
            "Trần Long Hải",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Toán khối 8 đúng tiến độ; chủ nhiệm lớp 83 trách nhiệm, sâu sát nề nếp học sinh; chuẩn bị tốt đề kiểm tra Toán 8.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ chuyên môn và chủ nhiệm.]"
        ),
        (
            "7",
            "Lê Thị Bình",
            "Giáo viên (Thư ký)",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Toán 7, 8; chủ nhiệm lớp 71 tốt; ghi chép biên bản tổ chu đáo; tham gia dạy thay 03 tiết Toán; chuẩn bị chu đáo NCBH Toán 8 và ngân hàng câu hỏi RCV.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, nhiệt tình dạy thay.]"
        ),
        (
            "8",
            "Nguyễn Thị Thảo",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Toán 6, 7; chủ nhiệm lớp 62 tận tụy, quản lý học sinh tốt; tích cực xây dựng ngân hàng câu hỏi Rung chuông vàng và đề kiểm tra Toán 6.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ chuyên môn và phong trào.]"
        ),
        (
            "9",
            "Nguyễn Văn Tính",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy Toán 65, HĐTN khối 6, 7 đúng tiến độ; chấp hành tốt ngày giờ công; tích cực tham gia dạy thay 02 tiết HĐTN 86.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, hỗ trợ dạy thay kịp thời.]"
        ),
        (
            "10",
            "Dương Quang Tùng",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Tin học các khối 6, 7, 8, 9 nghiêm túc; quản lý phòng máy vi tính chu đáo, bảo đảm kỹ thuật đường truyền phục vụ kiểm tra giữa kỳ trên OLM.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ chuyên môn và quản lý thiết bị.]"
        )
    ]
    add_thi_dua_table(doc, thi_dua_data)
    
    # Kết thúc cuộc họp
    add_paragraph_styled(doc, "Cuộc họp kết thúc vào lúc 16 giờ 30 phút cùng ngày. Biên bản đã được thông qua trước toàn thể thành viên trong tổ và 100% các thành viên đều nhất trí với các nội dung trên, không có ý kiến bổ sung hay thắc mắc nào khác.", indent=True)
    
    # Chữ ký
    add_bien_ban_signatures(doc, chu_tri="Hoàng Tấn Thiên", thu_ky="Lê Thị Bình")
    
    # Lưu file Word
    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    save_docx_robust(doc, out_docx_path)
    print(f"Da xuat thanh cong file Word: {out_docx_path}")
    
    # Nếu có yêu cầu xuất markdown
    if out_md_path:
        os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
        # Tạo nội dung markdown tương đương
        tao_bien_ban_hop_to_lan_2_thang_10_md(out_md_path)
        print(f"Da xuat thanh cong file Markdown: {out_md_path}")


def tao_bien_ban_hop_to_lan_2_thang_10_md(out_md_path):
    """Xuất bản sao lưu Markdown đồng bộ cho Biên bản họp tổ lần 2 tháng 10/2026."""
    md_content = """# TRƯỜNG THCS TRẦN PHÚ
## TỔ TOÁN – TIN HỌC
**Số: 03/BB-TCM**

---

# CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
### Độc lập – Tự do – Hạnh phúc
*Xuân Đông, ngày 23 tháng 10 năm 2026*

---

# BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 2
### NỘI DUNG SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 10/2026
**Năm học: 2026 - 2027**

Hôm nay, vào lúc 14 giờ 00 phút, ngày 23 tháng 10 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 2 tháng 10 năm học 2026 - 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).
  + Danh sách thành viên: Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

---

## NỘI DUNG CUỘC HỌP

### I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO
Thầy Tổ trưởng Hoàng Tấn Thiên quán triệt, phổ biến và cụ thể hóa các văn bản chỉ đạo của cấp trên và nhà trường gắn liền với nhiệm vụ chuyên môn của Tổ Toán – Tin học như sau:

1. **Triển khai Thông tư số 86/2026/TT-BGDĐT và chỉ đạo của Sở GD&ĐT về Giáo dục STEM:**
   - Thông tư số 86/2026/TT-BGDĐT ngày 30/9/2026 của Bộ Giáo dục và Đào tạo quy định về tổ chức hoạt động giáo dục tích hợp khoa học, công nghệ, kĩ thuật và toán học (giáo dục STEM) trong giáo dục phổ thông và Công văn hướng dẫn ngày 19/10/2026 của Sở Giáo dục và Đào tạo Đồng Nai về triển khai thực hiện Thông tư số 86/2026/TT-BGDĐT (kết hợp Công văn số 7206/BGDĐT-GDPT và Bộ Tài liệu giáo dục STEM cấp THCS: Tập 1 Phần chung, Tập 2B THCS).
   - Quán triệt 3 nguyên tắc chỉ đạo trọng tâm của Sở GD&ĐT:
     + Không yêu cầu xây dựng, phê duyệt kế hoạch riêng về giáo dục STEM; không làm phát sinh môn học, thời lượng học tập bắt buộc, đầu điểm, hồ sơ sổ sách riêng ngoài quy định.
     + Bài học STEM được tổ chức tích hợp trực tiếp trong quá trình dạy học môn Toán và môn Tin học; bám sát mục tiêu, yêu cầu cần đạt của Chương trình GDPT 2018 và giải quyết các vấn đề thực tiễn gắn với đời sống, nghề nghiệp.
     + Đánh giá kết quả học tập qua bài học STEM theo quy định hiện hành áp dụng đối với từng môn học (Thông tư 22/2021/TT-BGDĐT); kết hợp tự đánh giá và đánh giá sản phẩm của học sinh, tuyệt đối không đánh giá, xếp loại riêng ngoài quy định.

2. **Triển khai lồng ghép Giáo dục quốc phòng và an ninh (GDQP&AN):**
   - Thông báo ngày 20/10/2026 của Sở Giáo dục và Đào tạo Đồng Nai về Kết luận sau tập huấn cán bộ quản lý, giáo viên về lồng ghép nội dung Giáo dục quốc phòng và an ninh (GDQP&AN) trong trường tiểu học, trung học cơ sở năm 2026 (thực hiện Thông tư số 08/2024/TT-BGDĐT ngày 15/5/2024 của Bộ GD&ĐT).
   - Định hướng chuyên môn lồng ghép trong Tổ Toán – Tin học:
     + Nguyên tắc: Vận dụng linh hoạt, nhẹ nhàng, tự nhiên, phù hợp với tâm lý lứa tuổi học sinh THCS, không gây quá tải hoặc làm ảnh hưởng đến mục tiêu và thời lượng của môn học; lựa chọn học liệu từ nguồn chính thống, chính xác.
     + Đối với môn Toán: Lồng ghép qua các bài toán thực tiễn về tính toán khoảng cách, cự ly, hình học đo đạc, số liệu biểu đồ thống kê gắn với truyền thống lịch sử dựng nước, giữ nước và sức mạnh quốc phòng toàn dân.
     + Đối với môn Tin học: Tích hợp giáo dục ý thức bảo đảm an toàn thông tin, an ninh mạng, giữ gìn dữ liệu cá nhân và bảo mật thông tin số; nâng cao tinh thần cảnh giác trước thông tin xấu độc, lừa đảo trực tuyến và tội phạm công nghệ cao theo Luật An ninh mạng.

3. **Kế hoạch Giáo dục Liêm chính, phòng chống tham nhũng, lãng phí:**
   - Kế hoạch số 116/KH-THCS.TP ngày 21/10/2026 của Trường THCS Trần Phú về chỉ đạo thực hiện nội dung giáo dục liêm chính, phòng chống tham nhũng, tiêu cực và tiết kiệm, chống lãng phí năm học 2026 - 2027 (căn cứ Quyết định số 2907/QĐ-BGDĐT ngày 05/10/2026 của Bộ GD&ĐT).
   - Tổ Toán – Tin học xác định địa chỉ tích hợp tự nhiên, không gượng ép: Rèn luyện cho học sinh đức tính trung thực, tính chính xác khoa học, công bằng, tuyệt đối không gian lận trong kiểm tra thi cử và học tập; thực hành tiết kiệm thời gian, tiết kiệm giấy mực, có ý thức giữ gìn tài sản chung của nhà trường và bảo vệ tài nguyên số.

4. **Kế hoạch Tích hợp học tập làm theo tư tưởng, đạo đức, phong cách Hồ Chí Minh:**
   - Kế hoạch số 121/KH-THCS.TP ngày 19/10/2026 của Trường THCS Trần Phú về tích hợp học tập, làm theo tư tưởng, đạo đức, phong cách Hồ Chí Minh năm học 2026 - 2027 (căn cứ Quyết định số 2995/QĐ-BGDĐT ngày 13/10/2026 của Bộ GD&ĐT).
   - Lồng ghép vào môn Khoa học Tự nhiên và Toán học: Rèn luyện phương pháp làm việc khoa học, tác phong cẩn thận, tư duy độc lập và sáng tạo.
   - Đặc biệt, giáo viên lồng ghép các chỉ báo Khung Năng lực số (NLS) và Khung Trí tuệ nhân tạo (AI) vào bài giảng, hướng dẫn học sinh ứng dụng công cụ AI một cách hợp lý, đúng mực và có trách nhiệm trong học tập.

5. **Kế hoạch nhiệm vụ năm học và Quy chế làm việc của cơ quan:**
   - Kế hoạch số 124/KH-THCS.TP ngày 19/10/2026 về Thực hiện nhiệm vụ năm học 2026 - 2027 và Quyết định số 183/QĐ-THCS.TP ngày 19/10/2026 của Hiệu trưởng Trường THCS Trần Phú ban hành Quy chế làm việc năm học 2026 - 2027.
   - Quán triệt 100% cán bộ, giáo viên trong tổ thực hiện nghiêm túc ngày giờ công, giờ lên lớp, tác phong sư phạm mẫu mực, không vi phạm quy chế chuyên môn, hoàn thành các loại hồ sơ sổ sách đúng tiến độ.

6. **Cuộc thi trực tuyến “Đồng Nai vươn mình trong kỷ nguyên mới”:**
   - Kế hoạch số 125/KH-THCS.TP ngày 20/10/2026 của Trường THCS Trần Phú triển khai Cuộc thi trực tuyến “Đồng Nai vươn mình trong kỷ nguyên mới” (tìm hiểu Nghị quyết số 16-NQ/TW ngày 21/7/2026 của Bộ Chính trị theo Kế hoạch 05-KH/BTGTU của Ban Tuyên giáo Thành ủy Đồng Nai).
   - Yêu cầu 100% giáo viên trong tổ tham gia thi trực tuyến nghiêm túc, đạt chất lượng cao; báo cáo tiến độ và kết quả về Tổ trưởng theo dõi.

7. **Khóa học an ninh mạng, dữ liệu cá nhân và AI trên nền tảng số:**
   - Công văn số 3791/CATP-PA05 của Công an thành phố Đồng Nai về việc triển khai khóa học an ninh mạng, dữ liệu cá nhân, AI trên nền tảng Bình dân học vụ số (https://huanluyenanninhmang.mobifone.vn): Đôn đốc các giáo viên đã đăng ký khẩn trương hoàn thành các bài học và bài kiểm tra trực tuyến để nhận chứng nhận hoàn thành khóa học.

---

### II. ĐÁNH GIÁ CÔNG TÁC GIAI ĐOẠN QUA

#### 1. Hồ sơ chuyên môn và Kế hoạch bài dạy (KHBD)
- Công tác soạn bài theo Công văn 5512/BGDĐT-GDTrH: Toàn thể giáo viên trong tổ thực hiện nghiêm túc, soạn bài đầy đủ trước khi lên lớp, bám sát yêu cầu cần đạt của Chương trình GDPT 2018.
- Tích hợp Khung Năng lực số (NLS 20%) và Khung AI (12 tiết): Giáo viên chủ động đưa mục tiêu và chỉ báo năng lực vào tiến trình hoạt động dạy học, thể hiện in đậm nghiêng rõ nét trong KHBD.
- Đưa KHBD lên Cơ sở dữ liệu ngành và ký số: Các đồng chí hoàn thành cơ bản đáp ứng yêu cầu tiến độ theo quy định của nhà trường, đảm bảo hồ sơ số phê duyệt kịp thời.

#### 2. Nề nếp giảng dạy và thực hiện ngày giờ công
- Giáo viên chấp hành tốt kỷ luật lao động, đảm bảo ngày giờ công, không đi trễ về sớm, không cắt xén chương trình.
- Thực hiện đúng quy định kiểm tra đánh giá thường xuyên theo Thông tư 22/2021/TT-BGDĐT, ghi sổ đầu bài khớp lịch trình giảng dạy.

#### 3. Tình hình dạy thay giáo viên đi công tác / tập huấn
Trong giai đoạn qua của tháng 10, do phân công công tác đột xuất của cấp trên và địa phương, tổ đã chủ động sắp xếp dạy thay 05 lượt (tổng số 12 tiết dạy thay), đảm bảo đầy đủ quyền lợi học tập của học sinh, không để trống tiết. Chi tiết cụ thể như sau:

| STT | Ngày & Buổi | Tiết & Lớp | Số tiết | GV thực dạy | Thay cho GV | Lý do |
|:---:|:---:|:---|:---:|:---:|:---:|:---|
| 1 | 08/10/2026 (Sáng) | Tiết 1: 91 - Toán<br>Tiết 2: 91 - Toán<br>Tiết 4: 92 - Toán | 3 | Trần Sáng | Hoàng Tấn Thiên | Đi nộp hồ sơ an ninh mạng tại PA05 – Công an TP Đồng Nai |
| 2 | 15/10/2026 (Chiều) | Tiết 8: 86 - HĐTN<br>Tiết 9: 86 - HĐTN | 2 | Nguyễn Văn Tính | Đinh Văn Đông | Đi họp tại UBND xã Xuân Đông |
| 3 | 19/10/2026 (Sáng) | Tiết 2: 66 - Toán<br>Tiết 4: 95 - Toán | 2 | Đinh Văn Đông | Trần Sáng | Tham gia Hội thi Khuyến học |
| 4 | 19/10/2026 (Chiều) | Tiết 7: 97 - Toán<br>Tiết 8: 96 - Toán | 2 | Hồ Đăng Danh | Trần Sáng | Tham gia Hội thi Khuyến học |
| 5 | 21/10/2026 (Sáng) | Tiết 1: 61 - Toán<br>Tiết 2: 92 - Toán<br>Tiết 3: 91 - Toán | 3 | Lê Thị Bình | Hoàng Tấn Thiên | Đi kiểm tra hồ sơ đảng viên tại Đảng uỷ xã Xuân Đông |

Tổ tuyên dương tinh thần đoàn kết, sẵn sàng nhận nhiệm vụ và hỗ trợ đồng nghiệp kịp thời của các Thầy/Cô: Trần Sáng, Lê Thị Bình, Đinh Văn Đông, Hồ Đăng Danh, Nguyễn Văn Tính.

#### 4. Quản lý phòng bộ môn và cơ sở vật chất
- Thầy Dương Quang Tùng duy trì bảo quản tốt hệ thống phòng máy vi tính, kiểm tra đường truyền mạng ổn định, chuẩn bị sẵn sàng cho kỳ kiểm tra giữa kỳ môn Tin học trên OLM.

---

### III. CÔNG TÁC TỚI (KẾ HOẠCH TRỌNG TÂM THỜI GIAN TỚI)

#### 1. Công tác Kiểm tra đánh giá Giữa học kỳ I năm học 2026 - 2027
Thực hiện Kế hoạch số 122/KH-THCS.TP ngày 19/10/2026 của Trường THCS Trần Phú về việc tổ chức kiểm tra, đánh giá giữa kỳ I, Tổ Toán – Tin học thống nhất triển khai kế hoạch cụ thể như sau:
- **Hình thức và lịch kiểm tra:**
  + Môn Tin học: Kiểm tra trực tuyến trên nền tảng OLM theo Thời khóa biểu trong Tuần 9 (từ ngày 02/11 đến ngày 06/11/2026).
  + Môn Toán (khối 6, 7, 8, 9): Kiểm tra tập trung đồng loạt vào Sáng Thứ Sáu, ngày 13/11/2026 (Thời lượng 60 phút, từ 7 giờ 00 phút đến 8 giờ 00 phút).
- **Yêu cầu chuyên môn về đề kiểm tra:** Bám sát chuẩn kiến thức, kỹ năng và yêu cầu cần đạt của Chương trình GDPT 2018 theo định dạng Công văn 7991/BGDĐT-GDTrH và hướng dẫn số 4096/SGDĐT-GDPT&GDTX Đồng Nai. Mỗi bộ môn/khối biên soạn 02 đề (01 đề chính thức, 01 đề dự phòng) kèm Ma trận, Bản đặc tả và Hướng dẫn chấm chi tiết.
- **Hạn chót nộp sản phẩm:** Tổ chuyên môn thẩm định, ký duyệt và nộp toàn bộ đề, ma trận về Ban Giám hiệu duyệt in sao chậm nhất ngày **29/10/2026** (trước ngày 30/10/2026).
- **Phân công nhiệm vụ biên soạn và phản biện đề kiểm tra Giữa kỳ I:**

| STT | Khối & Môn | Người biên soạn | Người phản biện | Hình thức & Lịch kiểm tra | Hạn nộp BGH |
|:---:|:---:|:---|:---|:---|:---:|
| 1 | Toán 6 | Hoàng Tấn Thiên<br>Nguyễn Thị Thảo | Hồ Đăng Danh | Tập trung (60 phút)<br>Sáng Thứ Sáu 13/11/2026 | 29/10/2026 |
| 2 | Toán 7 | Lê Thị Bình | Hoàng Xuân Ánh | Tập trung (60 phút)<br>Sáng Thứ Sáu 13/11/2026 | 29/10/2026 |
| 3 | Toán 8 | Trần Long Hải | Lê Thị Bình | Tập trung (60 phút)<br>Sáng Thứ Sáu 13/11/2026 | 29/10/2026 |
| 4 | Toán 9 | Trần Sáng | Hoàng Tấn Thiên | Tập trung (60 phút)<br>Sáng Thứ Sáu 13/11/2026 | 29/10/2026 |
| 5 | Tin học 6, 7, 8, 9 | Dương Quang Tùng | Hoàng Tấn Thiên | Trực tuyến OLM theo TKB<br>Tuần 9 (02/11 – 06/11/2026) | 29/10/2026 |

- **Nhập điểm kết quả kiểm tra lên Cơ sở dữ liệu ngành:** Hoàn thành chậm nhất ngày **20/11/2026**.

#### 2. Phong trào thi đua chào mừng Ngày Nhà giáo Việt Nam 20/11 — Hội thi “Rung chuông vàng” môn Toán 6
Thực hiện Kế hoạch số 02/KH-TT ngày 15/10/2026 của Tổ Toán – Tin học về việc tổ chức Chuyên đề ngoại khóa “Rung chuông vàng” môn Toán khối 6 chào mừng kỷ niệm 44 năm Ngày Nhà giáo Việt Nam (20/11/1982 – 20/11/2026):
- **Thời gian tổ chức:** Từ 14 giờ 00 phút đến 16 giờ 00 phút, chiều Thứ Sáu, ngày 13 tháng 11 năm 2026.
- **Địa điểm:** Sân trường THCS Trần Phú.
- **Đối tượng:** Toàn thể học sinh khối 6 (06 lớp). Mỗi lớp cử 05 học sinh xuất sắc tham gia thi đấu trên sàn đấu (tổng số 30 thí sinh); số học sinh còn lại là lực lượng cổ động viên và tham gia phần thi giao lưu khán giả.
- **Phân công trách nhiệm tổ chức:**
  + Trưởng ban tổ chức: Thầy **Hoàng Tấn Thiên** (chỉ đạo chung, phê duyệt thể lệ và thẩm định đề thi).
  + Phó ban tổ chức: Thầy **Đinh Văn Đông** (chỉ đạo chuyên môn), Thầy **Trần Sáng** (phụ trách điều hành kịch bản, kiêm MC sàn đấu).
  + Ban biên soạn ngân hàng câu hỏi: Cô **Nguyễn Thị Thảo** và Cô **Lê Thị Bình** biên soạn bộ 40 câu hỏi (30 câu chính thức, 05 câu phụ phân loại, 05 câu giao lưu khán giả; có tích hợp câu hỏi thực tiễn và thuật ngữ tiếng Anh toán học). Thẩm định hoàn tất trước ngày 22/10/2026.
  + Ban Giám khảo, cứu trợ và hỗ trợ sân bãi: Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng chịu trách nhiệm chuẩn bị bảng con, bút viết, chuông, âm thanh, nước uống và điều phối cứu trợ thí sinh.

#### 3. Sinh hoạt chuyên môn theo Nghiên cứu bài học (NCBH)
- Môn học và khối lớp: Môn **Toán khối 8**.
- Người thực hiện dạy minh họa: Cô **Lê Thị Bình** chịu trách nhiệm thiết kế bài dạy nghiên cứu và tổ chức dạy thể nghiệm trên lớp.
- Tiến trình thực hiện: Cả tổ tham gia đóng góp ý kiến thiết kế bài dạy, dự giờ tập trung quan sát hoạt động học của học sinh, tổ chức họp phân tích bài học và rút kinh nghiệm nhằm nâng cao phương pháp giảng dạy hình học/đại số 8.

#### 4. Điều chỉnh Kế hoạch Chuyên đề Ứng dụng Trí tuệ nhân tạo (AI) trong dạy học (Chuyên đề Cụm)
- **Điều chỉnh thời gian:** Nhằm đáp ứng yêu cầu chuyển đổi số và nâng cao năng lực ứng dụng công nghệ của giáo viên trong toàn cụm, tổ thống nhất **điều chỉnh thời gian tổ chức Chuyên đề AI từ tháng 3/2027 chuyển sang tháng 12/2026**.
- **Phân công phụ trách chuyên đề cụm:** Giao Cô **Lê Thị Bình** và Thầy **Trần Sáng** chịu trách nhiệm xây dựng báo cáo chuyên đề, thiết kế giáo án điện tử ứng dụng các công cụ AI hỗ trợ dạy học và trực tiếp dạy minh họa.
- Toàn tổ tham gia hỗ trợ tư liệu, chạy thử phần mềm và chuẩn bị các điều kiện cơ sở vật chất tốt nhất cho chuyên đề cấp cụm.

#### 5. Công tác bồi dưỡng học sinh giỏi và các phong trào học tập trực tuyến
- Tiếp tục duy trì công tác bồi dưỡng đội tuyển học sinh giỏi Toán, Tin học theo kế hoạch của nhà trường.
- Tiếp tục đẩy mạnh phong trào Đấu trường Toán học VioEdu và Olympic tiếng Anh (IOE) ở tất cả các khối lớp 6, 7, 8, 9, động viên học sinh tích cực tham gia các vòng tự luyện và vòng thi các cấp.
- *<span style="color:red">Danh sách phân công giáo viên phụ trách bồi dưỡng HSG và các phong trào thi (chờ rà soát và cập nhật):</span>*
  + <span style="color:red">Khối 6: Giáo viên phụ trách: ........................................, Danh sách học sinh: ........................................</span>
  + <span style="color:red">Khối 7: Giáo viên phụ trách: ........................................, Danh sách học sinh: ........................................</span>
  + <span style="color:red">Khối 8: Giáo viên phụ trách: ........................................, Danh sách học sinh: ........................................</span>
  + <span style="color:red">Khối 9: Giáo viên phụ trách: ........................................, Danh sách học sinh: ........................................</span>
  + <span style="color:red">Phụ trách Đấu trường Toán học VioEdu: ........................................</span>
  + <span style="color:red">Phụ trách Olympic tiếng Anh (IOE): ........................................</span>

#### 6. Các công tác khác: Nâng cao văn hóa đọc và nề nếp chủ nhiệm
- Giáo viên bộ môn (Toán, Tin học): Chủ động phối hợp với Thư viện nhà trường bố trí và tiến hành các tiết đọc sách chuyên môn, hướng dẫn học sinh đọc sách tham khảo, tài liệu toán vui, lịch sử toán học và kiến thức khoa học công nghệ.
- Giáo viên chủ nhiệm (Cô Thảo - 62, Cô Bình - 71, Thầy Hải - 83, Thầy Sáng - 97): Tích cực triển khai phong trào đọc sách tại lớp trong các tiết sinh hoạt lớp, duy trì nề nếp bảo quản tủ sách lớp học; tiếp tục bám sát nề nếp học tập, chuyên cần và đôn đốc các khoản thu theo quy định.

#### 7. Đánh giá, xếp loại thi đua Tổ chuyên môn tháng 10/2026
Căn cứ kết quả thực hiện nhiệm vụ, ngày giờ công và tinh thần trách nhiệm trong công tác của các thành viên, Tổ Toán – Tin học thống nhất bảng xếp loại thi đua tháng 10/2026 như sau (các nội dung dự kiến in chữ màu đỏ để Thầy Tổ trưởng rà soát trước khi phê duyệt chính thức):

| STT | HỌ VÀ TÊN | CHỨC VỤ | TỰ XẾP LOẠI | TỰ NHẬN XÉT | TỔ XẾP LOẠI | GHI CHÚ |
|:---:|:---|:---:|:---:|:---|:---:|:---|
| 1 | **Hoàng Tấn Thiên** | Tổ trưởng | **A** | Lên kế hoạch kịp thời, đúng tiến độ. Hoàn thành tốt công tác soạn giảng, thực hiện tốt quy chế chuyên môn, nhà trường. Ngày giờ công đảm bảo, thông tin 2 chiều kịp thời và chính xác. | **A** | Lên kế hoạch kịp thời, đúng tiến độ. Hoàn thành tốt công tác soạn giảng, thực hiện tốt quy chế chuyên môn, nhà trường. Ngày giờ công đảm bảo, thông tin 2 chiều kịp thời và chính xác. |
| 2 | Trần Sáng | Tổ phó | <span style="color:red">A</span> | <span style="color:red">Thực hiện tốt giảng dạy môn Toán 6, 9; chủ nhiệm lớp 97 nghiêm túc; tích cực tham gia dạy thay 03 tiết Toán và chuẩn bị tốt kịch bản MC Rung chuông vàng.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ, tích cực dạy thay.</span> |
| 3 | Đinh Văn Đông | Phó Hiệu trưởng | <span style="color:red">A</span> | <span style="color:red">Tham gia giảng dạy HĐTN 86 đầy đủ, đúng quy chế; tích cực chỉ đạo chuyên môn tổ và tham gia dạy thay 02 tiết Toán cho giáo viên trong tổ.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ giảng dạy và chỉ đạo chuyên môn.</span> |
| 4 | Hồ Đăng Danh | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Thực hiện nghiêm túc tiến độ giảng dạy Toán 6, 9; hồ sơ sổ sách đầy đủ; tích cực tham gia dạy thay 02 tiết Toán 9 cho đồng nghiệp.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ, hỗ trợ dạy thay kịp thời.</span> |
| 5 | Hoàng Xuân Ánh | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Toán 7, HĐTN khối 6 đúng phân phối chương trình; nề nếp ngày giờ công đảm bảo, hồ sơ giáo án đầy đủ.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ được giao.</span> |
| 6 | Trần Long Hải | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Toán khối 8 đúng tiến độ; chủ nhiệm lớp 83 trách nhiệm, sâu sát nề nếp học sinh; chuẩn bị tốt đề kiểm tra Toán 8.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ chuyên môn và chủ nhiệm.</span> |
| 7 | Lê Thị Bình | Giáo viên (Thư ký) | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Toán 7, 8; chủ nhiệm lớp 71 tốt; ghi chép biên bản tổ chu đáo; tham gia dạy thay 03 tiết Toán; chuẩn bị chu đáo NCBH Toán 8 và ngân hàng câu hỏi RCV.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ, nhiệt tình dạy thay.</span> |
| 8 | Nguyễn Thị Thảo | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Toán 6, 7; chủ nhiệm lớp 62 tận tụy, quản lý học sinh tốt; tích cực xây dựng ngân hàng câu hỏi Rung chuông vàng và đề kiểm tra Toán 6.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ chuyên môn và phong trào.</span> |
| 9 | Nguyễn Văn Tính | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy Toán 65, HĐTN khối 6, 7 đúng tiến độ; chấp hành tốt ngày giờ công; tích cực tham gia dạy thay 02 tiết HĐTN 86.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ, hỗ trợ dạy thay kịp thời.</span> |
| 10 | Dương Quang Tùng | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Tin học các khối 6, 7, 8, 9 nghiêm túc; quản lý phòng máy vi tính chu đáo, bảo đảm kỹ thuật đường truyền phục vụ kiểm tra giữa kỳ trên OLM.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ chuyên môn và quản lý thiết bị.</span> |

Cuộc họp kết thúc vào lúc 16 giờ 30 phút cùng ngày. Biên bản đã được thông qua trước toàn thể thành viên trong tổ và 100% các thành viên đều nhất trí với các nội dung trên, không có ý kiến bổ sung hay thắc mắc nào khác.

---

| **THƯ KÝ** | **CHỦ TRÌ CUỘC HỌP (TỔ TRƯỞNG)** |
|:---:|:---:|
| *(Ký và ghi rõ họ tên)* | *(Ký và ghi rõ họ tên)* |
| <br><br><br>**Lê Thị Bình** | <br><br><br>**Hoàng Tấn Thiên** |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


def tao_bao_cao_thang_10(out_docx_path, out_md_path=None):
    """
    Soạn thảo Báo cáo Hoạt động tháng 10/2026 của Tổ Toán - Tin học gửi Ban Giám hiệu nhà trường.
    Chuẩn Form mẫu thực tế Trường THCS Trần Phú và Thể thức Nghị định 30/2020/NĐ-CP.
    """
    doc = create_nd30_document()
    
    # 1. Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="02/BC - TCM",
        ngay_thang_str="Xuân Đông, ngày 28 tháng 10 năm 2026"
    )
    
    # 2. Tiêu đề
    add_doc_title(
        doc,
        "BÁO CÁO",
        "HOẠT ĐỘNG TỔ TOÁN – TIN HỌC THÁNG 10/2026\nNăm học: 2026 - 2027"
    )
    
    # 3. Căn cứ ban hành
    can_cu_list = [
        "Căn cứ chỉ đạo, định hướng công tác chuyên môn trường THCS Trần Phú tháng 10 năm học 2026 - 2027",
        "Căn cứ tình hình thực tế hoạt động chuyên môn của tổ Toán – Tin học báo cáo hoạt động chuyên môn tháng 10 cụ thể như sau"
    ]
    add_can_cu(doc, can_cu_list)
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. ĐÁNH GIÁ CÔNG TÁC QUA:")
    
    # 1. Chủ nhiệm
    add_section_h2(doc, "1. Chủ nhiệm:")
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm trong tổ (Cô Thảo - 62, Cô Bình - 71, Thầy Hải - 83, Thầy Sáng - 97) đã chủ động điều tra, nắm bắt hoàn cảnh học sinh diện khó khăn, đề xuất hỗ trợ học bổng và bảo hiểm y tế kịp thời.", indent=True)
    add_paragraph_styled(doc, "- Ổn định nề nếp học tập, duy trì kiểm tra việc chấp hành nội quy, đồng phục, bảo quản sách giáo khoa; duy trì công tác vệ sinh trường lớp và lao động tự quản.", indent=True)
    add_paragraph_styled(doc, "- Cập nhật đầy đủ thông tin học sinh và đồng bộ chính xác trên hệ thống Cơ sở dữ liệu ngành; rà soát hồ sơ phục vụ công tác ký học bạ số.", indent=True)
    add_paragraph_styled(doc, "- Tổ chức cho học sinh ký cam kết giáo dục pháp luật (GDPL), phòng chống tai nạn thương tích (PCTNTT), chấp hành nghiêm luật an toàn giao thông (ATGT).", indent=True)
    add_paragraph_styled(doc, "- Tích cực đôn đốc phụ huynh và học sinh hoàn thành các khoản đóng góp về bộ phận tài vụ theo đúng quy định.", indent=True)
    add_paragraph_styled(doc, "- Phối hợp với Thư viện nhà trường hướng dẫn học sinh đọc sách trong giờ sinh hoạt lớp, duy trì tốt phong trào đọc sách và nề nếp tủ sách lớp học.", indent=True)
    
    # 2. Ngày giờ công
    add_section_h2(doc, "2. Ngày giờ công:")
    add_paragraph_styled(doc, "- Toàn thể giáo viên trong tổ chấp hành nghiêm túc ngày giờ công, không đi trễ về sớm, đảm bảo quy chế chuyên môn và Quy chế làm việc ban hành theo Quyết định số 183/QĐ-THCS.TP ngày 19/10/2026 của Hiệu trưởng nhà trường.", indent=True)
    add_paragraph_styled(doc, "- Công tác dạy thay: Trong tháng 10, do phân công công tác đột xuất của cấp trên và địa phương, tổ đã linh hoạt bố trí dạy thay 05 lượt (tổng số 12 tiết dạy thay), đảm bảo học sinh không bị trống tiết, đúng tiến độ chương trình giảng dạy. Cụ thể như sau:", indent=True)
    
    day_thay_data = [
        ("1", "08/10/2026\n(Sáng)", "Tiết 1: 91 - Toán\nTiết 2: 91 - Toán\nTiết 4: 92 - Toán", "3", "Trần Sáng", "Hoàng Tấn Thiên", "Đi nộp hồ sơ an ninh mạng tại PA05 – Công an TP Đồng Nai"),
        ("2", "15/10/2026\n(Chiều)", "Tiết 8: 86 - HĐTN\nTiết 9: 86 - HĐTN", "2", "Nguyễn Văn Tính", "Đinh Văn Đông", "Đi họp tại UBND xã Xuân Đông"),
        ("3", "19/10/2026\n(Sáng)", "Tiết 2: 66 - Toán\nTiết 4: 95 - Toán", "2", "Đinh Văn Đông", "Trần Sáng", "Tham gia Hội thi Khuyến học"),
        ("4", "19/10/2026\n(Chiều)", "Tiết 7: 97 - Toán\nTiết 8: 96 - Toán", "2", "Hồ Đăng Danh", "Trần Sáng", "Tham gia Hội thi Khuyến học"),
        ("5", "21/10/2026\n(Sáng)", "Tiết 1: 61 - Toán\nTiết 2: 92 - Toán\nTiết 3: 91 - Toán", "3", "Lê Thị Bình", "Hoàng Tấn Thiên", "Đi kiểm tra hồ sơ đảng viên tại Đảng uỷ xã Xuân Đông")
    ]
    add_day_thay_table(doc, day_thay_data)
    
    # 3. Hoạt động tổ chuyên môn
    add_section_h2(doc, "3. Hoạt động tổ chuyên môn:")
    add_paragraph_styled(doc, "- Kịp thời triển khai, cụ thể hóa các văn bản chỉ đạo trọng tâm của cấp trên và nhà trường:", indent=True)
    add_paragraph_styled(doc, "  + Triển khai Thông tư số 86/2026/TT-BGDĐT ngày 30/9/2026 của Bộ GD&ĐT và Công văn hướng dẫn ngày 19/10/2026 của Sở GD&ĐT Đồng Nai về Giáo dục STEM (kết hợp CV 7206/BGDĐT-GDPT và Bộ Tài liệu STEM Tập 1, Tập 2B THCS): Quán triệt không xây dựng kế hoạch riêng về STEM, không phát sinh đầu điểm/sổ sách; tổ chức dạy học bài học STEM tích hợp trực tiếp trong môn Toán và Tin học; đánh giá qua quá trình và sản phẩm học tập theo quy định hiện hành.", indent=True)
    add_paragraph_styled(doc, "  + Triển khai Thông báo ngày 20/10/2026 của Sở GD&ĐT Đồng Nai về lồng ghép Giáo dục quốc phòng và an ninh (GDQP&AN) theo Thông tư số 08/2024/TT-BGDĐT: Vận dụng linh hoạt, nhẹ nhàng trong môn Toán (bài toán khoảng cách, cự ly, số liệu thống kê) và môn Tin học (bảo đảm an toàn, an ninh thông tin, an ninh mạng, bảo vệ dữ liệu cá nhân theo Luật An ninh mạng).", indent=True)
    add_paragraph_styled(doc, "  + Triển khai đầy đủ các văn bản: Kế hoạch số 116/KH-THCS.TP về Giáo dục liêm chính, PCTN, chống lãng phí; Kế hoạch số 121/KH-THCS.TP về Tích hợp học tập làm theo tư tưởng đạo đức Hồ Chí Minh; Kế hoạch số 124/KH-THCS.TP về Thực hiện nhiệm vụ năm học; Quyết định số 183/QĐ-THCS.TP ban hành Quy chế làm việc; Kế hoạch số 125/KH-THCS.TP về Cuộc thi trực tuyến 'Đồng Nai vươn mình trong kỷ nguyên mới'; Công văn số 3791/CATP-PA05 về khóa học an ninh mạng, AI trên Bình dân học vụ số.", indent=True)
    add_paragraph_styled(doc, "- Công tác soạn giảng và hồ sơ sổ sách: Toàn thể giáo viên thực hiện nghiêm túc Công văn 5512/BGDĐT-GDTrH; tích hợp Khung Năng lực số (20% tổng số tiết) và 12 tiết Khung AI vào KHBD thể hiện in đậm nghiêng rõ nét; tiến độ đưa KHBD lên CSDL ngành và ký số cơ bản đáp ứng tốt yêu cầu.", indent=True)
    add_paragraph_styled(doc, "- Sinh hoạt chuyên môn tổ: Duy trì nền nếp sinh hoạt định kỳ 02 lần/tháng (Lần 1 ngày 06/10/2026, Lần 2 ngày 23/10/2026), giải quyết vướng mắc về chuyên môn, thống nhất tiến độ bài học.", indent=True)
    add_paragraph_styled(doc, "- Chuẩn bị Kiểm tra Giữa kỳ I (Kế hoạch số 122/KH-THCS.TP): Hoàn thành xây dựng ma trận, bản đặc tả, đề cương và biên soạn 02 bộ đề (chính thức, dự phòng) các khối 6, 7, 8, 9 môn Toán và môn Tin học theo đúng hướng dẫn Công văn 7991 của Bộ GD&ĐT và Công văn 4096 của Sở GD&ĐT Đồng Nai; thẩm định hoàn tất gửi BGH duyệt trước ngày 30/10/2026.", indent=True)
    add_paragraph_styled(doc, "- Phong trào thi đua chào mừng 20/11: Xây dựng hoàn chỉnh Kế hoạch số 02/KH-TT ngày 15/10/2026 về Hội thi 'Rung chuông vàng' môn Toán khối 6; biên soạn bộ ngân hàng 40 câu hỏi bảo đảm chất lượng, tính thực tiễn và hội nhập.", indent=True)
    add_paragraph_styled(doc, "- Sinh hoạt chuyên môn theo Nghiên cứu bài học: Đã đăng ký và chuẩn bị bài dạy minh họa môn Toán 8 do Cô Lê Thị Bình phụ trách.", indent=True)
    add_paragraph_styled(doc, "- Chuyên đề Cụm về AI: Tổ đã thống nhất điều chỉnh thời gian tổ chức Chuyên đề Ứng dụng Trí tuệ nhân tạo (AI) trong dạy học Toán - Tin cấp cụm từ tháng 3/2027 sang tháng 12/2026, phân công Cô Lê Thị Bình và Thầy Trần Sáng phụ trách thực hiện.", indent=True)
    add_paragraph_styled(doc, "- Tiếp tục duy trì công tác bồi dưỡng học sinh giỏi Toán, Tin học; đôn đốc học sinh tham gia tự luyện Đấu trường Toán học VioEdu và Olympic tiếng Anh (IOE).", indent=True)
    
    # 4. Công tác khác
    add_section_h2(doc, "4. Công tác khác:")
    add_paragraph_styled(doc, "- Giáo viên bộ môn phối hợp với Thư viện nhà trường tổ chức các tiết đọc sách chuyên môn, giới thiệu tài liệu toán học, công nghệ thông tin cho học sinh.", indent=True)
    add_paragraph_styled(doc, "- Tích cực tham gia các phong trào thi đua, lao động vệ sinh môi trường cơ sở 1 và cơ sở 2 theo phân công của Ban Giám hiệu.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. KẾ HOẠCH TRỌNG TÂM TRONG THỜI GIAN TỚI (THÁNG 11/2026):")
    
    # 1. Chủ nhiệm
    add_section_h2(doc, "1. Chủ nhiệm:")
    add_paragraph_styled(doc, "- Tiếp tục duy trì nề nếp kỷ cương lớp học, theo dõi sát sao chuyên cần và đạo đức học sinh; kịp thời uốn nắn học sinh có biểu hiện lơ là học tập.", indent=True)
    add_paragraph_styled(doc, "- Tiếp tục đôn đốc học sinh tham gia học tiếng Anh với giáo viên nước ngoài; hoàn thành việc thu nộp các khoản đóng góp về bộ phận tài vụ.", indent=True)
    add_paragraph_styled(doc, "- Duy trì và phát huy hiệu quả phong trào đọc sách tại lớp, hướng dẫn học sinh khai thác tài liệu tại thư viện nhà trường.", indent=True)
    add_paragraph_styled(doc, "- Hướng dẫn học sinh tích cực thi đua lập thành tích chào mừng Ngày Nhà giáo Việt Nam 20/11.", indent=True)
    
    # 2. Ngày giờ công
    add_section_h2(doc, "2. Ngày giờ công:")
    add_paragraph_styled(doc, "- Toàn thể cán bộ, giáo viên trong tổ đảm bảo nghiêm túc ngày giờ công, giờ lên lớp; tham gia đầy đủ, nhiệt tình các hoạt động kỷ niệm 44 năm Ngày Nhà giáo Việt Nam 20/11 do nhà trường và ngành phát động.", indent=True)
    
    # 3. Hoạt động tổ chuyên môn
    add_section_h2(doc, "3. Hoạt động tổ chuyên môn:")
    add_paragraph_styled(doc, "- Tổ chức Kiểm tra đánh giá Giữa học kỳ I năm học 2026 - 2027 theo đúng Kế hoạch 122/KH-THCS.TP của Trường THCS Trần Phú:", indent=True)
    add_paragraph_styled(doc, "  + Tuần 9 (02/11 – 06/11/2026): Kiểm tra trực tuyến môn Tin học trên nền tảng OLM theo TKB.", indent=True)
    add_paragraph_styled(doc, "  + Tuần 10: Sáng Thứ Sáu 13/11/2026 kiểm tra tập trung đồng loạt môn Toán 6, 7, 8, 9 (60 phút, 7h00 – 8h00).", indent=True)
    add_paragraph_styled(doc, "  + Tổ chức chấm bài nghiêm túc, công bằng, trả bài và sửa bài cho học sinh; hoàn thành nhập điểm lên CSDL ngành chậm nhất ngày **20/11/2026**.", indent=True)
    
    ra_de_data = [
        ("1", "Toán 6", "Hoàng Tấn Thiên\nNguyễn Thị Thảo", "Hồ Đăng Danh", "Tập trung (60 phút)\nSáng Thứ Sáu 13/11/2026", "29/10/2026"),
        ("2", "Toán 7", "Lê Thị Bình", "Hoàng Xuân Ánh", "Tập trung (60 phút)\nSáng Thứ Sáu 13/11/2026", "29/10/2026"),
        ("3", "Toán 8", "Trần Long Hải", "Lê Thị Bình", "Tập trung (60 phút)\nSáng Thứ Sáu 13/11/2026", "29/10/2026"),
        ("4", "Toán 9", "Trần Sáng", "Hoàng Tấn Thiên", "Tập trung (60 phút)\nSáng Thứ Sáu 13/11/2026", "29/10/2026"),
        ("5", "Tin học 6, 7, 8, 9", "Dương Quang Tùng", "Hoàng Tấn Thiên", "Trực tuyến OLM theo TKB\nTuần 9 (02/11 – 06/11/2026)", "29/10/2026")
    ]
    add_phan_cong_ra_de_table(doc, ra_de_data)
    
    add_paragraph_styled(doc, "- Tổ chức thành công Chuyên đề ngoại khóa 'Rung chuông vàng' môn Toán khối 6 chào mừng 44 năm Ngày Nhà giáo Việt Nam vào chiều Thứ Sáu ngày 13/11/2026 (từ 14h00 đến 16h00) tại sân trường THCS Trần Phú.", indent=True)
    add_paragraph_styled(doc, "- Triển khai tiết dạy minh họa Nghiên cứu bài học môn Toán 8 do Cô Lê Thị Bình thực hiện; tổ chức sinh hoạt chuyên môn đánh giá, phân tích hoạt động học của học sinh.", indent=True)
    add_paragraph_styled(doc, "- Hoàn thiện công tác chuẩn bị cho Chuyên đề Cụm về AI (tổ chức trong tháng 12/2026): Cô Bình và Thầy Sáng hoàn tất giáo án điện tử và bài dạy thể nghiệm.", indent=True)
    add_paragraph_styled(doc, "- Tiếp tục đẩy mạnh bồi dưỡng học sinh giỏi; theo dõi và hướng dẫn học sinh tham gia các vòng thi Đấu trường Toán học VioEdu và Olympic tiếng Anh (IOE).", indent=True)
    add_paragraph_styled(doc, "- Duy trì nghiêm nếp soạn KHBD tích hợp NLS và AI; phê duyệt ký số hàng tuần trên hệ thống CSDL ngành đúng tiến độ.", indent=True)
    
    # 4. Công tác khác
    add_section_h2(doc, "4. Công tác khác:")
    add_paragraph_styled(doc, "- Thực hiện tốt các nhiệm vụ đột xuất khác theo sự phân công và điều hành của Ban Giám hiệu.", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. ĐÁNH GIÁ THI ĐUA TRONG THÁNG 10/2026:")
    add_paragraph_styled(doc, "Căn cứ kết quả thực hiện nhiệm vụ chuyên môn, ngày giờ công và tinh thần trách nhiệm trong công tác của các thành viên, Tổ Toán – Tin học thống nhất bảng xếp loại thi đua tháng 10/2026 như sau (các nội dung dự kiến in chữ màu đỏ để Ban Giám hiệu theo dõi và rà soát):", indent=True)
    
    thi_dua_data = [
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
            "Trần Sáng",
            "Tổ phó",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Thực hiện tốt giảng dạy môn Toán 6, 9; chủ nhiệm lớp 97 nghiêm túc; tích cực tham gia dạy thay 03 tiết Toán và chuẩn bị tốt kịch bản MC Rung chuông vàng.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, tích cực dạy thay.]"
        ),
        (
            "3",
            "Đinh Văn Đông",
            "Phó Hiệu trưởng",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Tham gia giảng dạy HĐTN 86 đầy đủ, đúng quy chế; tích cực chỉ đạo chuyên môn tổ và tham gia dạy thay 02 tiết Toán cho giáo viên trong tổ.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ giảng dạy và chỉ đạo chuyên môn.]"
        ),
        (
            "4",
            "Hồ Đăng Danh",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Thực hiện nghiêm túc tiến độ giảng dạy Toán 6, 9; hồ sơ sổ sách đầy đủ; tích cực tham gia dạy thay 02 tiết Toán 9 cho đồng nghiệp.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, hỗ trợ dạy thay kịp thời.]"
        ),
        (
            "5",
            "Hoàng Xuân Ánh",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Toán 7, HĐTN khối 6 đúng phân phối chương trình; nề nếp ngày giờ công đảm bảo, hồ sơ giáo án đầy đủ.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ được giao.]"
        ),
        (
            "6",
            "Trần Long Hải",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Toán khối 8 đúng tiến độ; chủ nhiệm lớp 83 trách nhiệm, sâu sát nề nếp học sinh; chuẩn bị tốt đề kiểm tra Toán 8.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ chuyên môn và chủ nhiệm.]"
        ),
        (
            "7",
            "Lê Thị Bình",
            "Giáo viên (Thư ký)",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Toán 7, 8; chủ nhiệm lớp 71 tốt; ghi chép biên bản tổ chu đáo; tham gia dạy thay 03 tiết Toán; chuẩn bị chu đáo NCBH Toán 8 và ngân hàng câu hỏi RCV.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, nhiệt tình dạy thay.]"
        ),
        (
            "8",
            "Nguyễn Thị Thảo",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Toán 6, 7; chủ nhiệm lớp 62 tận tụy, quản lý học sinh tốt; tích cực xây dựng ngân hàng câu hỏi Rung chuông vàng và đề kiểm tra Toán 6.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ chuyên môn và phong trào.]"
        ),
        (
            "9",
            "Nguyễn Văn Tính",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy Toán 65, HĐTN khối 6, 7 đúng tiến độ; chấp hành tốt ngày giờ công; tích cực tham gia dạy thay 02 tiết HĐTN 86.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ, hỗ trợ dạy thay kịp thời.]"
        ),
        (
            "10",
            "Dương Quang Tùng",
            "Giáo viên",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Giảng dạy môn Tin học các khối 6, 7, 8, 9 nghiêm túc; quản lý phòng máy vi tính chu đáo, bảo đảm kỹ thuật đường truyền phục vụ kiểm tra giữa kỳ trên OLM.]",
            "[CHỮ ĐỎ: A]",
            "[CHỮ ĐỎ: Hoàn thành tốt nhiệm vụ chuyên môn và quản lý thiết bị.]"
        )
    ]
    add_thi_dua_table(doc, thi_dua_data)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. ĐỀ XUẤT, KIẾN NGHỊ TRONG THỜI GIAN TỚI:")
    add_paragraph_styled(doc, "Kính đề nghị Ban Giám hiệu và bộ phận Thiết bị – Đoàn Đội tạo điều kiện hỗ trợ về hệ thống âm thanh, loa mic, sân bãi và các điều kiện cơ sở vật chất cần thiết để Tổ Toán – Tin học tổ chức thành công Chuyên đề ngoại khóa 'Rung chuông vàng' môn Toán khối 6 vào chiều Thứ Sáu, ngày 13/11/2026 tại sân trường.", indent=True)
    
    # Chữ ký 2 bên (BGH trái, Tổ trưởng phải)
    add_signatures(
        doc,
        left_title="Ban giám hiệu\n(Ký, ghi rõ họ tên và đóng dấu)",
        left_name="",
        right_title="Tổ trưởng\n(Ký và ghi rõ họ tên)",
        right_name="Hoàng Tấn Thiên"
    )
    
    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    save_docx_robust(doc, out_docx_path)
    print(f"Da xuat thanh cong file Word: {out_docx_path}")
    
    if out_md_path:
        os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
        tao_bao_cao_thang_10_md(out_md_path)
        print(f"Da xuat thanh cong file Markdown: {out_md_path}")


def tao_bao_cao_thang_10_md(out_md_path):
    """Xuất bản sao lưu Markdown đồng bộ cho Báo cáo hoạt động tháng 10/2026."""
    md_content = """# TRƯỜNG THCS TRẦN PHÚ
## TỔ TOÁN - TIN HỌC
**Số: 02/BC - TCM**

---

# CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
### Độc lập – Tự do – Hạnh phúc
*Xuân Đông, ngày 28 tháng 10 năm 2026*

---

# BÁO CÁO
### HOẠT ĐỘNG TỔ TOÁN – TIN HỌC THÁNG 10/2026
**Năm học: 2026 - 2027**

*Căn cứ chỉ đạo, định hướng công tác chuyên môn trường THCS Trần Phú tháng 10 năm học 2026 - 2027;*
*Căn cứ tình hình thực tế hoạt động chuyên môn của tổ Toán – Tin học báo cáo hoạt động chuyên môn tháng 10 cụ thể như sau:*

---

## I. ĐÁNH GIÁ CÔNG TÁC QUA:

### 1. Chủ nhiệm:
- Giáo viên chủ nhiệm trong tổ (Cô Thảo - 62, Cô Bình - 71, Thầy Hải - 83, Thầy Sáng - 97) đã chủ động điều tra, nắm bắt hoàn cảnh học sinh diện khó khăn, đề xuất hỗ trợ học bổng và bảo hiểm y tế kịp thời.
- Ổn định nề nếp học tập, duy trì kiểm tra việc chấp hành nội quy, đồng phục, bảo quản sách giáo khoa; duy trì công tác vệ sinh trường lớp và lao động tự quản.
- Cập nhật đầy đủ thông tin học sinh và đồng bộ chính xác trên hệ thống Cơ sở dữ liệu ngành; rà soát hồ sơ phục vụ công tác ký học bạ số.
- Tổ chức cho học sinh ký cam kết giáo dục pháp luật (GDPL), phòng chống tai nạn thương tích (PCTNTT), chấp hành nghiêm luật an toàn giao thông (ATGT).
- Tích cực đôn đốc phụ huynh và học sinh hoàn thành các khoản đóng góp về bộ phận tài vụ theo đúng quy định.
- Phối hợp với Thư viện nhà trường hướng dẫn học sinh đọc sách trong giờ sinh hoạt lớp, duy trì tốt phong trào đọc sách và nề nếp tủ sách lớp học.

### 2. Ngày giờ công:
- Toàn thể giáo viên trong tổ chấp hành nghiêm túc ngày giờ công, không đi trễ về sớm, đảm bảo quy chế chuyên môn và Quy chế làm việc ban hành theo Quyết định số 183/QĐ-THCS.TP ngày 19/10/2026 của Hiệu trưởng nhà trường.
- **Công tác dạy thay:** Trong tháng 10, do phân công công tác đột xuất của cấp trên và địa phương, tổ đã linh hoạt bố trí dạy thay 05 lượt (tổng số 12 tiết dạy thay), đảm bảo học sinh không bị trống tiết, đúng tiến độ chương trình giảng dạy. Cụ thể như sau:

| STT | Ngày & Buổi | Tiết & Lớp | Số tiết | GV thực dạy | Thay cho GV | Lý do |
|:---:|:---:|:---|:---:|:---:|:---:|:---|
| 1 | 08/10/2026 (Sáng) | Tiết 1: 91 - Toán<br>Tiết 2: 91 - Toán<br>Tiết 4: 92 - Toán | 3 | Trần Sáng | Hoàng Tấn Thiên | Đi nộp hồ sơ an ninh mạng tại PA05 – Công an TP Đồng Nai |
| 2 | 15/10/2026 (Chiều) | Tiết 8: 86 - HĐTN<br>Tiết 9: 86 - HĐTN | 2 | Nguyễn Văn Tính | Đinh Văn Đông | Đi họp tại UBND xã Xuân Đông |
| 3 | 19/10/2026 (Sáng) | Tiết 2: 66 - Toán<br>Tiết 4: 95 - Toán | 2 | Đinh Văn Đông | Trần Sáng | Tham gia Hội thi Khuyến học |
| 4 | 19/10/2026 (Chiều) | Tiết 7: 97 - Toán<br>Tiết 8: 96 - Toán | 2 | Hồ Đăng Danh | Trần Sáng | Tham gia Hội thi Khuyến học |
| 5 | 21/10/2026 (Sáng) | Tiết 1: 61 - Toán<br>Tiết 2: 92 - Toán<br>Tiết 3: 91 - Toán | 3 | Lê Thị Bình | Hoàng Tấn Thiên | Đi kiểm tra hồ sơ đảng viên tại Đảng uỷ xã Xuân Đông |

### 3. Hoạt động tổ chuyên môn:
- Kịp thời triển khai, cụ thể hóa các văn bản chỉ đạo trọng tâm của cấp trên và nhà trường:
  + **Triển khai Thông tư số 86/2026/TT-BGDĐT ngày 30/9/2026 của Bộ GD&ĐT và Công văn hướng dẫn ngày 19/10/2026 của Sở GD&ĐT Đồng Nai về Giáo dục STEM** (kết hợp CV 7206/BGDĐT-GDPT và Bộ Tài liệu STEM Tập 1, Tập 2B THCS): Quán triệt không xây dựng kế hoạch riêng về STEM, không phát sinh đầu điểm/sổ sách; tổ chức dạy học bài học STEM tích hợp trực tiếp trong môn Toán và Tin học; đánh giá qua quá trình và sản phẩm học tập theo quy định hiện hành.
  + **Triển khai Thông báo ngày 20/10/2026 của Sở GD&ĐT Đồng Nai về lồng ghép Giáo dục quốc phòng và an ninh (GDQP&AN)** theo Thông tư số 08/2024/TT-BGDĐT: Vận dụng linh hoạt, nhẹ nhàng trong môn Toán (bài toán khoảng cách, cự ly, số liệu thống kê) và môn Tin học (bảo đảm an toàn, an ninh thông tin, an ninh mạng, bảo vệ dữ liệu cá nhân theo Luật An ninh mạng).
  + **Triển khai đầy đủ các văn bản:** Kế hoạch số 116/KH-THCS.TP về Giáo dục liêm chính, PCTN, chống lãng phí; Kế hoạch số 121/KH-THCS.TP về Tích hợp học tập làm theo tư tưởng đạo đức Hồ Chí Minh; Kế hoạch số 124/KH-THCS.TP về Thực hiện nhiệm vụ năm học; Quyết định số 183/QĐ-THCS.TP ban hành Quy chế làm việc; Kế hoạch số 125/KH-THCS.TP về Cuộc thi trực tuyến "Đồng Nai vươn mình trong kỷ nguyên mới"; Công văn số 3791/CATP-PA05 về khóa học an ninh mạng, AI trên Bình dân học vụ số.
- Công tác soạn giảng và hồ sơ sổ sách: Toàn thể giáo viên thực hiện nghiêm túc Công văn 5512/BGDĐT-GDTrH; tích hợp Khung Năng lực số (20% tổng số tiết) và 12 tiết Khung AI vào KHBD thể hiện in đậm nghiêng rõ nét; tiến độ đưa KHBD lên CSDL ngành và ký số cơ bản đáp ứng tốt yêu cầu.
- Sinh hoạt chuyên môn tổ: Duy trì nền nếp sinh hoạt định kỳ 02 lần/tháng (Lần 1 ngày 06/10/2026, Lần 2 ngày 23/10/2026), giải quyết vướng mắc về chuyên môn, thống nhất tiến độ bài học.
- Chuẩn bị Kiểm tra Giữa kỳ I (Kế hoạch số 122/KH-THCS.TP): Hoàn thành xây dựng ma trận, bản đặc tả, đề cương và biên soạn 02 bộ đề (chính thức, dự phòng) các khối 6, 7, 8, 9 môn Toán và môn Tin học theo đúng hướng dẫn Công văn 7991 của Bộ GD&ĐT và Công văn 4096 của Sở GD&ĐT Đồng Nai; thẩm định hoàn tất gửi BGH duyệt trước ngày 30/10/2026.
- Phong trào thi đua chào mừng 20/11: Xây dựng hoàn chỉnh Kế hoạch số 02/KH-TT ngày 15/10/2026 về Hội thi "Rung chuông vàng" môn Toán khối 6; biên soạn bộ ngân hàng 40 câu hỏi bảo đảm chất lượng, tính thực tiễn và hội nhập.
- Sinh hoạt chuyên môn theo Nghiên cứu bài học: Đã đăng ký và chuẩn bị bài dạy minh họa môn Toán 8 do Cô Lê Thị Bình phụ trách.
- Chuyên đề Cụm về AI: Tổ đã thống nhất điều chỉnh thời gian tổ chức Chuyên đề Ứng dụng Trí tuệ nhân tạo (AI) trong dạy học Toán - Tin cấp cụm từ tháng 3/2027 sang tháng 12/2026, phân công Cô Lê Thị Bình và Thầy Trần Sáng phụ trách thực hiện.
- Tiếp tục duy trì công tác bồi dưỡng học sinh giỏi Toán, Tin học; đôn đốc học sinh tham gia tự luyện Đấu trường Toán học VioEdu và Olympic tiếng Anh (IOE).

### 4. Công tác khác:
- Giáo viên bộ môn phối hợp với Thư viện nhà trường tổ chức các tiết đọc sách chuyên môn, giới thiệu tài liệu toán học, công nghệ thông tin cho học sinh.
- Tích cực tham gia các phong trào thi đua, lao động vệ sinh môi trường cơ sở 1 và cơ sở 2 theo phân công của Ban Giám hiệu.

---

## II. KẾ HOẠCH TRỌNG TÂM TRONG THỜI GIAN TỚI (THÁNG 11/2026):

### 1. Chủ nhiệm:
- Tiếp tục duy trì nề nếp kỷ cương lớp học, theo dõi sát sao chuyên cần và đạo đức học sinh; kịp thời uốn nắn học sinh có biểu hiện lơ là học tập.
- Tiếp tục đôn đốc học sinh tham gia học tiếng Anh với giáo viên nước ngoài; hoàn thành việc thu nộp các khoản đóng góp về bộ phận tài vụ.
- Duy trì và phát huy hiệu quả phong trào đọc sách tại lớp, hướng dẫn học sinh khai thác tài liệu tại thư viện nhà trường.
- Hướng dẫn học sinh tích cực thi đua lập thành tích chào mừng Ngày Nhà giáo Việt Nam 20/11.

### 2. Ngày giờ công:
- Toàn thể cán bộ, giáo viên trong tổ đảm bảo nghiêm túc ngày giờ công, giờ lên lớp; tham gia đầy đủ, nhiệt tình các hoạt động kỷ niệm 44 năm Ngày Nhà giáo Việt Nam 20/11 do nhà trường và ngành phát động.

### 3. Hoạt động tổ chuyên môn:
- **Tổ chức Kiểm tra đánh giá Giữa học kỳ I năm học 2026 - 2027 theo đúng Kế hoạch 122/KH-THCS.TP của Trường THCS Trần Phú:**
  + Tuần 9 (02/11 – 06/11/2026): Kiểm tra trực tuyến môn Tin học trên nền tảng OLM theo TKB.
  + Tuần 10: Sáng Thứ Sáu 13/11/2026 kiểm tra tập trung đồng loạt môn Toán 6, 7, 8, 9 (60 phút, 7h00 – 8h00).
  + Tổ chức chấm bài nghiêm túc, công bằng, trả bài và sửa bài cho học sinh; hoàn thành nhập điểm lên CSDL ngành chậm nhất ngày **20/11/2026**.

| STT | Khối & Môn | Người biên soạn | Người phản biện | Hình thức & Lịch kiểm tra | Hạn nộp BGH |
|:---:|:---:|:---|:---|:---|:---:|
| 1 | Toán 6 | Hoàng Tấn Thiên<br>Nguyễn Thị Thảo | Hồ Đăng Danh | Tập trung (60 phút)<br>Sáng Thứ Sáu 13/11/2026 | 29/10/2026 |
| 2 | Toán 7 | Lê Thị Bình | Hoàng Xuân Ánh | Tập trung (60 phút)<br>Sáng Thứ Sáu 13/11/2026 | 29/10/2026 |
| 3 | Toán 8 | Trần Long Hải | Lê Thị Bình | Tập trung (60 phút)<br>Sáng Thứ Sáu 13/11/2026 | 29/10/2026 |
| 4 | Toán 9 | Trần Sáng | Hoàng Tấn Thiên | Tập trung (60 phút)<br>Sáng Thứ Sáu 13/11/2026 | 29/10/2026 |
| 5 | Tin học 6, 7, 8, 9 | Dương Quang Tùng | Hoàng Tấn Thiên | Trực tuyến OLM theo TKB<br>Tuần 9 (02/11 – 06/11/2026) | 29/10/2026 |

- Tổ chức thành công Chuyên đề ngoại khóa "Rung chuông vàng" môn Toán khối 6 chào mừng 44 năm Ngày Nhà giáo Việt Nam vào chiều Thứ Sáu ngày 13/11/2026 (từ 14h00 đến 16h00) tại sân trường THCS Trần Phú.
- Triển khai tiết dạy minh họa Nghiên cứu bài học môn Toán 8 do Cô Lê Thị Bình thực hiện; tổ chức sinh hoạt chuyên môn đánh giá, phân tích hoạt động học của học sinh.
- Hoàn thiện công tác chuẩn bị cho Chuyên đề Cụm về AI (tổ chức trong tháng 12/2026): Cô Bình và Thầy Sáng hoàn tất giáo án điện tử và bài dạy thể nghiệm.
- Tiếp tục đẩy mạnh bồi dưỡng học sinh giỏi; theo dõi và hướng dẫn học sinh tham gia các vòng thi Đấu trường Toán học VioEdu và Olympic tiếng Anh (IOE).
- Duy trì nghiêm nếp soạn KHBD tích hợp NLS và AI; phê duyệt ký số hàng tuần trên hệ thống CSDL ngành đúng tiến độ.

### 4. Công tác khác:
- Thực hiện tốt các nhiệm vụ đột xuất khác theo sự phân công và điều hành của Ban Giám hiệu.

---

## III. ĐÁNH GIÁ THI ĐUA TRONG THÁNG 10/2026:
Căn cứ kết quả thực hiện nhiệm vụ chuyên môn, ngày giờ công và tinh thần trách nhiệm trong công tác của các thành viên, Tổ Toán – Tin học thống nhất bảng xếp loại thi đua tháng 10/2026 như sau (các nội dung dự kiến in chữ màu đỏ để Ban Giám hiệu theo dõi và rà soát):

| STT | HỌ VÀ TÊN | CHỨC VỤ | TỰ XẾP LOẠI | TỰ NHẬN XÉT | TỔ XẾP LOẠI | GHI CHÚ |
|:---:|:---|:---:|:---:|:---|:---:|:---|
| 1 | **Hoàng Tấn Thiên** | Tổ trưởng | **A** | Lên kế hoạch kịp thời, đúng tiến độ. Hoàn thành tốt công tác soạn giảng, thực hiện tốt quy chế chuyên môn, nhà trường. Ngày giờ công đảm bảo, thông tin 2 chiều kịp thời và chính xác. | **A** | Lên kế hoạch kịp thời, đúng tiến độ. Hoàn thành tốt công tác soạn giảng, thực hiện tốt quy chế chuyên môn, nhà trường. Ngày giờ công đảm bảo, thông tin 2 chiều kịp thời và chính xác. |
| 2 | Trần Sáng | Tổ phó | <span style="color:red">A</span> | <span style="color:red">Thực hiện tốt giảng dạy môn Toán 6, 9; chủ nhiệm lớp 97 nghiêm túc; tích cực tham gia dạy thay 03 tiết Toán và chuẩn bị tốt kịch bản MC Rung chuông vàng.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ, tích cực dạy thay.</span> |
| 3 | Đinh Văn Đông | Phó Hiệu trưởng | <span style="color:red">A</span> | <span style="color:red">Tham gia giảng dạy HĐTN 86 đầy đủ, đúng quy chế; tích cực chỉ đạo chuyên môn tổ và tham gia dạy thay 02 tiết Toán cho giáo viên trong tổ.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ giảng dạy và chỉ đạo chuyên môn.</span> |
| 4 | Hồ Đăng Danh | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Thực hiện nghiêm túc tiến độ giảng dạy Toán 6, 9; hồ sơ sổ sách đầy đủ; tích cực tham gia dạy thay 02 tiết Toán 9 cho đồng nghiệp.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ, hỗ trợ dạy thay kịp thời.</span> |
| 5 | Hoàng Xuân Ánh | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Toán 7, HĐTN khối 6 đúng phân phối chương trình; nề nếp ngày giờ công đảm bảo, hồ sơ giáo án đầy đủ.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ được giao.</span> |
| 6 | Trần Long Hải | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Toán khối 8 đúng tiến độ; chủ nhiệm lớp 83 trách nhiệm, sâu sát nề nếp học sinh; chuẩn bị tốt đề kiểm tra Toán 8.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ chuyên môn và chủ nhiệm.</span> |
| 7 | Lê Thị Bình | Giáo viên (Thư ký) | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Toán 7, 8; chủ nhiệm lớp 71 tốt; ghi chép biên bản tổ chu đáo; tham gia dạy thay 03 tiết Toán; chuẩn bị chu đáo NCBH Toán 8 và ngân hàng câu hỏi RCV.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ, nhiệt tình dạy thay.</span> |
| 8 | Nguyễn Thị Thảo | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Toán 6, 7; chủ nhiệm lớp 62 tận tụy, quản lý học sinh tốt; tích cực xây dựng ngân hàng câu hỏi Rung chuông vàng và đề kiểm tra Toán 6.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ chuyên môn và phong trào.</span> |
| 9 | Nguyễn Văn Tính | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy Toán 65, HĐTN khối 6, 7 đúng tiến độ; chấp hành tốt ngày giờ công; tích cực tham gia dạy thay 02 tiết HĐTN 86.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ, hỗ trợ dạy thay kịp thời.</span> |
| 10 | Dương Quang Tùng | Giáo viên | <span style="color:red">A</span> | <span style="color:red">Giảng dạy môn Tin học các khối 6, 7, 8, 9 nghiêm túc; quản lý phòng máy vi tính chu đáo, bảo đảm kỹ thuật đường truyền phục vụ kiểm tra giữa kỳ trên OLM.</span> | <span style="color:red">A</span> | <span style="color:red">Hoàn thành tốt nhiệm vụ chuyên môn và quản lý thiết bị.</span> |

---

## IV. ĐỀ XUẤT, KIẾN NGHỊ TRONG THỜI GIAN TỚI:
Kính đề nghị Ban Giám hiệu và bộ phận Thiết bị – Đoàn Đội tạo điều kiện hỗ trợ về hệ thống âm thanh, loa mic, sân bãi và các điều kiện cơ sở vật chất cần thiết để Tổ Toán – Tin học tổ chức thành công Chuyên đề ngoại khóa "Rung chuông vàng" môn Toán khối 6 vào chiều Thứ Sáu, ngày 13/11/2026 tại sân trường.

---

| **Ban giám hiệu**<br>*(Ký, ghi rõ họ tên và đóng dấu)* | **Tổ trưởng**<br>*(Ký và ghi rõ họ tên)* |
|:---:|:---:|
| <br><br><br> | <br><br><br>**Hoàng Tấn Thiên** |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)




def add_header_ktnb(doc, mau_so="04", so_qd="169/QĐ-THCS.TP", ngay_thang_str="[CHỮ ĐỎ: Xuân Đông, ngày 23 tháng 10 năm 2026]"):
    """Thêm Header chuẩn Mẫu 04 hoặc Mẫu 05 ban hành kèm CV 4794/SGDĐT-VP của Sở GD&ĐT TP Đồng Nai."""
    p_mau = doc.add_paragraph()
    p_mau.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mau.paragraph_format.space_before = Pt(0)
    p_mau.paragraph_format.space_after = Pt(1)
    p_mau.paragraph_format.line_spacing = 1.15
    
    r_mau1 = p_mau.add_run(f"Mẫu số {mau_so}\n")
    r_mau1.font.name = 'Times New Roman'
    r_mau1.font.size = Pt(11.5)
    r_mau1.bold = True
    
    r_mau2 = p_mau.add_run("(Kèm theo Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026\ncủa Sở Giáo dục và Đào tạo thành phố Đồng Nai)")
    r_mau2.font.name = 'Times New Roman'
    r_mau2.font.size = Pt(11)
    r_mau2.italic = True
    
    # Bảng 2 cột: Đơn vị (trái) và Quốc hiệu (phải)
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_no_borders(table)
    
    cell_l, cell_r = table.rows[0].cells
    cell_l.width = Inches(3.1)
    cell_r.width = Inches(3.7)
    
    # Cột trái
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.15
    p_l.paragraph_format.space_before = Pt(4)
    p_l.paragraph_format.space_after = Pt(0)
    
    r1 = p_l.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.bold = True
    
    r2 = p_l.add_run("Tổ kiểm tra theo Quyết định\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    
    add_run_parsed(p_l, f"số: {so_qd}", default_size=11.5, default_italic=True)
    
    # Cột phải
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.15
    p_r.paragraph_format.space_before = Pt(4)
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
    
    add_run_parsed(p_r, f"{ngay_thang_str}", default_size=12, default_italic=True)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(6)
    p_sp.paragraph_format.space_after = Pt(2)


def add_ktnb_bien_ban_signatures(doc, nguoi_duoc_kt="Trần Sáng", to_truong="Hoàng Tấn Thiên", nguoi_ghi="Lê Thị Bình"):
    """Khung chữ ký 3 bên của Mẫu số 04 (Biên bản kiểm tra)."""
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(10)
    p_sp.paragraph_format.space_after = Pt(2)
    
    table = doc.add_table(rows=2, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_no_borders(table)
    
    widths = [Inches(2.25), Inches(2.3), Inches(2.25)]
    for r in table.rows:
        for i, c in enumerate(r.cells):
            c.width = widths[i]
            
    # Tiêu đề ký
    p0 = table.rows[0].cells[0].paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.line_spacing = 1.15
    r0_1 = p0.add_run("NGƯỜI ĐƯỢC KIỂM TRA\n")
    r0_1.font.name = 'Times New Roman'
    r0_1.font.size = Pt(12)
    r0_1.bold = True
    r0_2 = p0.add_run("(Ký, ghi rõ họ tên)")
    r0_2.font.name = 'Times New Roman'
    r0_2.font.size = Pt(11)
    r0_2.italic = True
    
    p1 = table.rows[0].cells[1].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.line_spacing = 1.15
    r1_1 = p1.add_run("TỔ TRƯỞNG TỔ KIỂM TRA\n")
    r1_1.font.name = 'Times New Roman'
    r1_1.font.size = Pt(12)
    r1_1.bold = True
    r1_2 = p1.add_run("(Ký, ghi rõ họ tên)")
    r1_2.font.name = 'Times New Roman'
    r1_2.font.size = Pt(11)
    r1_2.italic = True
    
    p2 = table.rows[0].cells[2].paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.line_spacing = 1.15
    r2_1 = p2.add_run("NGƯỜI GHI BIÊN BẢN\n")
    r2_1.font.name = 'Times New Roman'
    r2_1.font.size = Pt(12)
    r2_1.bold = True
    r2_2 = p2.add_run("(Ký, ghi rõ họ tên)")
    r2_2.font.name = 'Times New Roman'
    r2_2.font.size = Pt(11)
    r2_2.italic = True
    
    # Dòng tên người ký
    p_b0 = table.rows[1].cells[0].paragraphs[0]
    p_b0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b0.paragraph_format.space_before = Pt(45)
    r_b0 = p_b0.add_run(nguoi_duoc_kt)
    r_b0.font.name = 'Times New Roman'
    r_b0.font.size = Pt(12)
    r_b0.bold = True
    
    p_b1 = table.rows[1].cells[1].paragraphs[0]
    p_b1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b1.paragraph_format.space_before = Pt(45)
    add_run_parsed(p_b1, to_truong, default_size=12, default_bold=True)
    
    p_b2 = table.rows[1].cells[2].paragraphs[0]
    p_b2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b2.paragraph_format.space_before = Pt(45)
    add_run_parsed(p_b2, nguoi_ghi, default_size=12, default_bold=True)


def add_ktnb_bao_cao_signatures(doc, to_truong="Hoàng Tấn Thiên"):
    """Khung chữ ký và Nơi nhận của Mẫu số 05 (Báo cáo kết quả kiểm tra)."""
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(10)
    p_sp.paragraph_format.space_after = Pt(2)
    
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_no_borders(table)
    
    cell_l, cell_r = table.rows[0].cells
    cell_l.width = Inches(3.2)
    cell_r.width = Inches(3.6)
    table.rows[1].cells[0].width = Inches(3.2)
    table.rows[1].cells[1].width = Inches(3.6)
    
    # Nơi nhận (trái)
    p_nn = cell_l.paragraphs[0]
    p_nn.paragraph_format.line_spacing = 1.15
    r_nn0 = p_nn.add_run("Nơi nhận:\n")
    r_nn0.font.name = 'Times New Roman'
    r_nn0.font.size = Pt(11)
    r_nn0.bold = True
    r_nn0.italic = True
    
    r_nn1 = p_nn.add_run("- Hiệu trưởng (để b/c);\n")
    r_nn1.font.name = 'Times New Roman'
    r_nn1.font.size = Pt(10.5)
    r_nn1.italic = True
    
    r_nn2 = p_nn.add_run("- Ông Trần Sáng (để t/h);\n")
    r_nn2.font.name = 'Times New Roman'
    r_nn2.font.size = Pt(10.5)
    r_nn2.italic = True
    
    r_nn3 = p_nn.add_run("- Lưu: Hồ sơ KTNB.")
    r_nn3.font.name = 'Times New Roman'
    r_nn3.font.size = Pt(10.5)
    r_nn3.italic = True
    
    # Tiêu đề ký (phải)
    p_ky = cell_r.paragraphs[0]
    p_ky.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ky.paragraph_format.line_spacing = 1.15
    r_ky1 = p_ky.add_run("TỔ TRƯỞNG TỔ KIỂM TRA\n")
    r_ky1.font.name = 'Times New Roman'
    r_ky1.font.size = Pt(12)
    r_ky1.bold = True
    r_ky2 = p_ky.add_run("(Ký, ghi rõ họ tên)")
    r_ky2.font.name = 'Times New Roman'
    r_ky2.font.size = Pt(11)
    r_ky2.italic = True
    
    # Tên người ký
    p_ten = table.rows[1].cells[1].paragraphs[0]
    p_ten.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ten.paragraph_format.space_before = Pt(45)
    add_run_parsed(p_ten, to_truong, default_size=12, default_bold=True)


def tao_bien_ban_kiem_tra_noi_bo(out_docx_path, out_md_path=None, **kwargs):
    """
    Soạn thảo hoàn chỉnh BIÊN BẢN KIỂM TRA (Mẫu số 04 kèm Công văn số 4794/SGDĐT-VP
    ngày 09/9/2026 của Sở GD&ĐT TP Đồng Nai).
    Chuẩn Nghị định 30/2020/NĐ-CP và Quyết định 169/QĐ-THCS.TP của Trường THCS Trần Phú.
    Kiểm tra toàn diện hoạt động sư phạm đối với Thầy Trần Sáng (Toán 9/5, 9/6, 9/7, 6/5; CN 9/7).
    """
    doc = create_nd30_document()
    
    so_qd = kwargs.get("so_qd", "169/QĐ-THCS.TP")
    ngay_qd = kwargs.get("ngay_qd", "05 tháng 10 năm 2026")
    ngay_kt_str = kwargs.get("ngay_kt_str", "Xuân Đông, ngày 23 tháng 10 năm 2026")
    ten_cuoc_kt = kwargs.get("ten_cuoc_kt", "kiểm tra toàn diện hoạt động sư phạm của nhà giáo")
    nguoi_duoc_kt_ten = kwargs.get("nguoi_duoc_kt_ten", "Trần Sáng")
    nguoi_duoc_kt_chuc_vu = kwargs.get("nguoi_duoc_kt_chuc_vu", "Phó Tổ trưởng Tổ Toán – Tin học, Giáo viên môn Toán")
    lop_phu_trach = kwargs.get("lop_phu_trach", "môn Toán các lớp 9/5, 9/6, 9/7, 6/5 và kiêm nhiệm Giáo viên chủ nhiệm lớp 9/7")
    dia_diem = kwargs.get("dia_diem", "Văn phòng Tổ Toán – Tin học và Phòng học lớp 9/7, 6/5 Trường THCS Trần Phú")
    
    # 1. Header chuẩn Mẫu 04
    add_header_ktnb(doc, mau_so="04", so_qd=so_qd, ngay_thang_str=ngay_kt_str)
    
    # 2. Tiêu đề chính
    add_doc_title(doc, "BIÊN BẢN KIỂM TRA", f"Về việc {ten_cuoc_kt}\n──────────────────")
    
    # 3. Căn cứ và dẫn nhập
    add_paragraph_styled(doc, f"Căn cứ Nghị định số 217/2025/NĐ-CP ngày 05 tháng 8 năm 2025 của Chính phủ về hoạt động kiểm tra chuyên ngành;", indent=True)
    add_paragraph_styled(doc, f"Căn cứ Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026 của Sở Giáo dục và Đào tạo thành phố Đồng Nai về việc hướng dẫn công tác kiểm tra nội bộ năm học 2026 - 2027;", indent=True)
    add_paragraph_styled(doc, f"Căn cứ Quyết định số {so_qd} ngày {ngay_qd} của Hiệu trưởng Trường THCS Trần Phú về việc {ten_cuoc_kt};", indent=True)
    add_paragraph_styled(doc, f"Trong tháng 10 năm 2026 (từ ngày 12 tháng 10 năm 2026 đến ngày 23 tháng 10 năm 2026), Tổ kiểm tra đã tiến hành thu thập thông tin, hồ sơ sổ sách chuyên môn, dự giờ thao giảng trực tiếp và kiểm tra thực tế tại {dia_diem} về việc {ten_cuoc_kt}.", indent=True)
    add_paragraph_styled(doc, "Sau đây là kết quả kiểm tra:", indent=True)
    
    # 4. Phần I: Thành phần làm việc
    add_section_h1(doc, "I. THÀNH PHẦN LÀM VIỆC")
    add_paragraph_styled(doc, "**1. Đại diện Tổ kiểm tra:**", indent=True)
    add_paragraph_styled(doc, "- Ông: **Hoàng Tấn Thiên** – chức vụ: Tổ trưởng chuyên môn (Tổ trưởng tổ kiểm tra).", indent=True)
    add_paragraph_styled(doc, "- Ông: **Hồ Đăng Danh** – chức vụ: Giáo viên môn Tin học (Thành viên).", indent=True)
    add_paragraph_styled(doc, "- Bà: **Lê Thị Bình** – chức vụ: Giáo viên môn Toán (Người ghi biên bản).", indent=True)
    
    add_paragraph_styled(doc, f"**2. Đã tiến hành kiểm tra đối với:** Thầy **{nguoi_duoc_kt_ten}**, gồm:", indent=True)
    add_paragraph_styled(doc, f"- Thầy: **{nguoi_duoc_kt_ten}** – chức vụ: {nguoi_duoc_kt_chuc_vu}; phụ trách giảng dạy {lop_phu_trach}.", indent=True)
    
    add_paragraph_styled(doc, "**3. Người chứng kiến:**", indent=True)
    add_paragraph_styled(doc, "- Ông: **Đinh Văn Đông** – chức vụ: Hiệu trưởng Trường THCS Trần Phú.", indent=True)
    add_paragraph_styled(doc, "- Ông: **Hoàng Xuân Ánh** – chức vụ: Giáo viên môn Toán.", indent=True)
    
    # 5. Phần II: Nội dung kiểm tra (Chuẩn form sư phạm THCS Trần Phú)
    add_section_h1(doc, "II. NỘI DUNG KIỂM TRA")
    
    # 1. Trình độ nghiệp vụ sư phạm
    add_paragraph_styled(doc, "**1. Trình độ nghiệp vụ sư phạm:**", indent=True)
    add_paragraph_styled(doc, "**1.1. Nắm vững mục đích, yêu cầu, chương trình và nội dung giảng dạy:**", indent=True)
    add_paragraph_styled(doc, "- Giáo viên nắm vững chương trình môn Toán (Toán 6 và Toán 9 theo Chương trình GDPT 2018); xác định đúng chuẩn kiến thức, kỹ năng và yêu cầu cần đạt (YCCĐ) của từng bài học; xác định chuẩn xác trọng tâm bài dạy.", indent=True)
    add_paragraph_styled(doc, "- Xây dựng kế hoạch dạy học bộ môn khoa học, cấu trúc bài dạy hợp lý, thể hiện rõ năng lực chuyên môn và nghiệp vụ sư phạm vững vàng khi đứng lớp. Tích cực liên hệ kiến thức toán học với đời sống thực tế tạo ham thích, hưng phấn, giáo dục toàn diện học sinh.", indent=True)
    add_paragraph_styled(doc, "=> **Xếp loại:** **Tốt**.", indent=True)
    
    add_paragraph_styled(doc, "**1.2. Trình độ vận dụng phương pháp dạy học:**", indent=True)
    add_paragraph_styled(doc, "- Lựa chọn phương pháp khá hợp lý trong giảng dạy, xử lý linh hoạt các phương pháp trong tiết dạy, đúng đặc trưng bộ môn Toán; tổ chức tốt các chuỗi hoạt động học tập (khởi động, hình thành kiến thức, luyện tập, vận dụng).", indent=True)
    add_paragraph_styled(doc, "- Ứng dụng công nghệ thông tin và công cụ trực quan hiệu quả vào dạy học; chuẩn bị chu đáo đồ dùng dạy học, phiếu học tập phục vụ tiết dạy. Định lượng thời gian các hoạt động khá cân đối.", indent=True)
    add_paragraph_styled(doc, "- Tác phong sư phạm nhẹ nhàng, chuẩn mực, làm chủ tiết dạy, nhiệt tình, hòa nhã với học sinh khi đứng lớp.", indent=True)
    add_paragraph_styled(doc, "=> **Xếp loại:** **Tốt**.", indent=True)
    
    add_paragraph_styled(doc, "**1.3. Hiệu quả tiết dạy (Dự giờ thao giảng 02 tiết):**", indent=True)
    add_paragraph_styled(doc, "- Học sinh bước đầu nắm vững kiến thức và vận dụng linh hoạt trong giải bài tập; tham gia xây dựng bài khá tốt; sử dụng sách giáo khoa và đồ dùng học tập hợp lý.", indent=True)
    add_paragraph_styled(doc, "- Kết quả đánh giá xếp loại sau dự giờ:", indent=True)
    add_paragraph_styled(doc, "  + **Tiết dạy 1:** Tiết 18 – *Luyện tập (Hệ thức lượng cạnh và góc trong tam giác vuông)* (Môn Toán 9, Lớp 9/7, Ngày dạy: 13/10/2026).", indent=True)
    add_paragraph_styled(doc, "    * Người dự giờ: Thầy **Đinh Văn Đông**, Thầy **Hoàng Tấn Thiên**, Thầy **Hồ Đăng Danh**, Thầy **Hoàng Xuân Ánh**.", indent=True)
    add_paragraph_styled(doc, "    * Nhận xét: Giáo viên chuẩn bị bài chu đáo, hệ thống bài tập logic, rèn luyện tốt kỹ năng tính toán và vận dụng hệ thức lượng cho học sinh; quản lý lớp tốt, tương tác tích cực. Xếp loại: **Giỏi**.", indent=True)
    add_paragraph_styled(doc, "  + **Tiết dạy 2:** Tiết 21 – *Bài 11: Ước chung, ước chung lớn nhất* (Môn Toán 6, Lớp 6/5, Ngày dạy: 22/10/2026).", indent=True)
    add_paragraph_styled(doc, "    * Người dự giờ: Thầy **Hoàng Tấn Thiên**, Cô **Lê Thị Bình**.", indent=True)
    add_paragraph_styled(doc, "    * Nhận xét: Phương pháp đúng đặc trưng bộ môn, tổ chức hoạt động hình thành kiến thức sôi nổi; ứng dụng tốt CNTT và mô phỏng trực quan giúp học sinh nắm vững cách tìm ƯCLN. Xếp loại: **Giỏi**.", indent=True)
    add_paragraph_styled(doc, "=> **Đánh giá chung về trình độ nghiệp vụ sư phạm:** **Tốt**.", indent=True)
    
    # 2. Thực hiện quy chế, quy định về chuyên môn
    add_paragraph_styled(doc, "**2. Thực hiện quy chế, quy định về chuyên môn:**", indent=True)
    add_paragraph_styled(doc, "**2.1. Thực hiện tiến độ chương trình và nề nếp chuyên môn:** Giảng dạy đúng chương trình theo quy định, dạy đủ các tiết theo kế hoạch môn Toán 6 và Toán 9, không cắt xén, không dạy dồn ghép; chấp hành nghiêm túc quy định về ngày giờ công và thực hiện nghiêm túc quy định dạy thêm, học thêm. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**2.2. Chuẩn bị Kế hoạch bài dạy (KHBD):** Soạn giảng kế hoạch dạy học đầy đủ theo kế hoạch dạy học, đúng với PPCT; đảm bảo đủ kiến thức, kỹ năng, có liên hệ thực tế; đầy đủ các bước lên lớp theo Công văn số 5512/BGDĐT-GDTrH, thể hiện rõ các hoạt động thầy và trò; chủ động tích hợp hiệu quả Khung Năng lực số (20%) và 12 tiết Khung AI (được in đậm, in nghiêng rõ nét theo đúng quy chuẩn); đồng bộ lên CSDL ngành và hoàn thành phê duyệt ký số tuần 100%. Soạn đủ các tiết thực hành trải nghiệm theo KHBD. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**2.3. Thực hiện kiểm tra, đánh giá học sinh:** Hoàn thành cơ số điểm theo quy định tới thời điểm kiểm tra; nội dung và hình thức kiểm tra thống nhất chung theo kế hoạch kiểm tra đánh giá đã phê duyệt đầu năm học; có chấm, chữa bài cẩn thận cho học sinh và có nhận xét rõ ràng; cập nhật điểm trên hệ thống và ghi sổ đầu bài khớp tiến độ; chú trọng ra đề kiểm tra bám sát các dạng toán thực tế. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**2.4. Đánh giá việc thực hành, thí nghiệm, sử dụng ĐDDH & STEM:** Dạy đủ các tiết thực hành, trải nghiệm theo quy định; có sử dụng ĐDDH chu đáo để phục vụ cho tiết dạy; bản thân tích cực tìm tòi có ý tưởng về sản phẩm STEM môn Toán. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**2.5. Bồi dưỡng, tự bồi dưỡng và sinh hoạt tổ chuyên môn:** Tham gia đầy đủ các buổi tập huấn theo quy định; tham gia họp tổ, chuyên môn đầy đủ; tham gia sinh hoạt chuyên đề của tổ; tích cực dự giờ khi được phân công; giữ vai trò nòng cốt Phó Tổ trưởng chuyên môn và chuẩn bị bài dạy minh họa Chuyên đề AI cấp cụm trường vào tháng 12/2026. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "=> **Đánh giá chung về thực hiện quy chế chuyên môn:** **Tốt**.", indent=True)
    
    # 3. Hoạt động chủ nhiệm lớp (Lớp 9/7)
    add_paragraph_styled(doc, "**3. Hoạt động chủ nhiệm lớp (Lớp 9/7):**", indent=True)
    add_paragraph_styled(doc, "- Xây dựng Kế hoạch chủ nhiệm năm học 2026 – 2027 đầy đủ, khoa học, bám sát phương hướng năm học của nhà trường và tình hình thực tế của học sinh khối 9 cuối cấp.", indent=True)
    add_paragraph_styled(doc, "- Quản lý nề nếp lớp 9/7 rất tốt; duy trì sĩ số chuyên cần cao; sâu sát nắm bắt hoàn cảnh từng học sinh; kịp thời uốn nắn, động viên các em học sinh có biểu hiện chểnh mảng; xây dựng tập thể lớp 9/7 đoàn kết, có ý thức tự quản và thi đua học tập tốt.", indent=True)
    add_paragraph_styled(doc, "- Thực hiện sổ sách chủ nhiệm sạch đẹp, cập nhật thông tin kịp thời; duy trì kênh phối hợp thường xuyên, hiệu quả giữa GVCN, Ban Giám hiệu, giáo viên bộ môn và Ban đại diện cha mẹ học sinh lớp 9/7; định hướng tốt cho học sinh về phân luồng và ôn thi tuyển sinh lớp 10.", indent=True)
    add_paragraph_styled(doc, "=> **Đánh giá chung về công tác chủ nhiệm:** **Tốt**.", indent=True)
    
    # 4. Thực hiện các nhiệm vụ khác
    add_paragraph_styled(doc, "**4. Thực hiện các nhiệm vụ khác và phong trào thi đua:**", indent=True)
    add_paragraph_styled(doc, "Hoàn thành mọi phong trào của nhà trường, tham gia tích cực trong các cuộc vận động, đóng góp; gương mẫu hoàn thành các nhiệm vụ đột xuất do Ban Giám hiệu phân công. => **Xếp loại:** **Tốt**.", indent=True)
    
    # 6. Phần III: Đánh giá chung (Ưu điểm, Tồn tại, Nguyên nhân)
    add_section_h1(doc, "III. ĐÁNH GIÁ CHUNG")
    add_paragraph_styled(doc, "**1. Ưu điểm:**", indent=True)
    add_paragraph_styled(doc, "- **Về chuyên môn giảng dạy môn Toán:** Thực hiện đúng phân công chuyên môn, phân phối chương trình môn Toán (các lớp 9/5, 9/6, 9/7, 6/5) và thời khóa biểu các môn phụ trách giảng dạy; chấp hành nghiêm túc quy định về dạy thêm, học thêm. Thực hiện việc kiểm tra, đánh giá đúng theo quy định, đảm bảo cơ số điểm đến thời điểm kiểm tra. Tổ chức giảng dạy đảm bảo yêu cầu cần đạt về năng lực và phẩm chất cho học sinh, thực hiện đúng quy chế chuyên môn, kết quả giảng dạy giỏi (cả 02 tiết dự giờ thao giảng của Ban Giám hiệu và tổ chuyên môn đều đạt loại Giỏi). Hồ sơ Kế hoạch bài dạy chuẩn bị chu đáo theo CV 5512, tích hợp hiệu quả Khung NLS và AI, ký số CSDL ngành đạt 100% đúng hạn. Có ý tưởng tốt trong hoàn thành sản phẩm STEM và đồ dùng dạy học trực quan.", indent=True)
    add_paragraph_styled(doc, "- **Về công tác chủ nhiệm lớp 9/7:** Có tinh thần trách nhiệm rất cao với lớp chủ nhiệm cuối cấp; xây dựng kế hoạch chủ nhiệm chu đáo; quản lý nề nếp lớp 9/7 chặt chẽ, tạo sự đồng thuận cao với phụ huynh học sinh; sâu sát uốn nắn học sinh và định hướng thi vào lớp 10 đạt hiệu quả rõ nét.", indent=True)
    add_paragraph_styled(doc, "- **Về vai trò nòng cốt và phong trào:** Luôn gương mẫu, hoàn thành xuất sắc trọng trách Phó Tổ trưởng chuyên môn; tích cực hỗ trợ đồng nghiệp và đang chuẩn bị tốt bài dạy minh họa chuyên đề AI cấp cụm vào tháng 12/2026; tích cực tham gia mọi hoạt động, phong trào của nhà trường.", indent=True)
    
    add_paragraph_styled(doc, "**2. Tồn tại:**", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: - Về chuyên môn: Quan tâm nhiều hơn cho học sinh yếu kém của lớp; định lượng thời gian các hoạt động trong tiết dạy đôi chỗ cần hợp lý hơn; hoạt động thực hành lưu ý việc phân công nhiệm vụ của từng thành viên trong nhóm và bài tập về nhà. Cần hướng dẫn học sinh hệ thống kiến thức qua bản đồ tư duy để học sinh dễ nắm vững kiến thức; trong soạn đề kiểm tra cần có ý tưởng sáng tạo hơn, hạn chế rập khuôn các dạng toán thực tế, cẩn trọng hơn trong soạn thảo chuẩn hóa Word Equation (OMML). Tiếp tục tìm tòi, nghiên cứu tham khảo từ đồng nghiệp, tài liệu và nguồn internet.]", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: - Về công tác chủ nhiệm: Tiếp tục theo dõi sát sao hơn nữa nhóm học sinh có nguy cơ đuối sức trong giai đoạn ôn thi tuyển sinh vào lớp 10, phân hóa biện pháp động viên phù hợp với từng đối tượng học sinh cá biệt; đa dạng hóa thêm hình thức sinh hoạt lớp cuối tuần để tạo không khí sôi nổi hơn.]", indent=True)
    
    add_paragraph_styled(doc, "**3. Nguyên nhân:**", indent=True)
    add_paragraph_styled(doc, "- Ưu điểm: Do giáo viên có trình độ chuyên môn vững vàng, nhiệt tình, hòa nhã với học sinh, tinh thần trách nhiệm cao và luôn tâm huyết với nghề nghiệp.", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: - Tồn tại: Do khối lượng công việc chuyên môn phụ trách 4 lớp (9/5, 9/6, 9/7, 6/5) kèm công tác chủ nhiệm lớp 9 cuối cấp nhiều áp lực về mặt thời gian, việc bao quát tỉ mỉ từng đối tượng học sinh cá biệt đôi lúc còn gặp khó khăn.]", indent=True)
    
    # 7. Phần IV: Kiến nghị của Tổ kiểm tra
    add_section_h1(doc, "IV. KIẾN NGHỊ CỦA TỔ KIỂM TRA")
    add_paragraph_styled(doc, "- **Đối với cá nhân (Thầy Trần Sáng):** Cần phát huy mặt mạnh và khắc phục các mặt tồn tại nêu trên; hoàn thành tốt bài dạy minh họa chuyên đề AI cấp cụm trường vào tháng 12/2026.", indent=True)
    add_paragraph_styled(doc, "- **Đối với Tổ chuyên môn:** Tiếp tục quan tâm và giúp đỡ về chuyên môn, nghiệp vụ; tạo điều kiện để Thầy Trần Sáng chia sẻ kinh nghiệm ứng dụng công nghệ, tích hợp AI và bài học STEM cho giáo viên trong tổ cùng học tập, nhân rộng.", indent=True)
    add_paragraph_styled(doc, "- **Đối với Nhà trường:** Cần quan tâm và giúp đỡ về tinh thần, tạo điều kiện thuận lợi về cơ sở vật chất, trang thiết bị dạy học bộ môn và phòng học lớp 9/7.", indent=True)
    
    # 8. Phần V: Ý kiến của bộ phận (người) được kiểm tra
    add_section_h1(doc, "V. Ý KIẾN CỦA BỘ PHẬN (NGƯỜI) ĐƯỢC KIỂM TRA")
    add_paragraph_styled(doc, "Đồng ý hoàn toàn với nội dung nhận xét, đánh giá của Tổ kiểm tra; nghiêm túc tiếp thu các ý kiến đóng góp và cam kết hoàn thành xuất sắc mọi nhiệm vụ được giao trong năm học 2026 – 2027.", indent=True)
    
    # Đoạn kết
    add_paragraph_styled(doc, "Việc kiểm tra kết thúc vào lúc [CHỮ ĐỎ: 11 giờ 30 phút, ngày 23 tháng 10 năm 2026] và được lập thành biên bản. Biên bản gồm [CHỮ ĐỎ: 04] trang.", indent=True)
    add_paragraph_styled(doc, "Biên bản này đã được đọc lại cho những người có tên nêu trên cùng nghe và đồng ý ký xác nhận; biên bản được lập thành 02 bản có giá trị như nhau, mỗi bên giữ 01 bản./.", indent=True)
    
    # Chữ ký 3 bên
    add_ktnb_bien_ban_signatures(doc, nguoi_duoc_kt=nguoi_duoc_kt_ten, to_truong="Hoàng Tấn Thiên", nguoi_ghi="Lê Thị Bình")
    
    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    save_docx_robust(doc, out_docx_path)
    print(f"Da xuat thanh cong Bien ban KTNB (Mau 04): {out_docx_path}")
    
    if out_md_path:
        os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
        tao_bien_ban_kiem_tra_noi_bo_md(out_md_path, **kwargs)
        print(f"Da xuat thanh cong Bien ban KTNB Markdown: {out_md_path}")


def tao_bien_ban_kiem_tra_noi_bo_md(out_md_path, **kwargs):
    """Xuất Markdown cho Mẫu 04 (Biên bản kiểm tra)."""
    so_qd = kwargs.get("so_qd", "169/QĐ-THCS.TP")
    ngay_qd = kwargs.get("ngay_qd", "05 tháng 10 năm 2026")
    ngay_kt_str = kwargs.get("ngay_kt_str", "Xuân Đông, ngày 23 tháng 10 năm 2026")
    ten_cuoc_kt = kwargs.get("ten_cuoc_kt", "kiểm tra toàn diện hoạt động sư phạm của nhà giáo")
    nguoi_duoc_kt_ten = kwargs.get("nguoi_duoc_kt_ten", "Trần Sáng")
    nguoi_duoc_kt_chuc_vu = kwargs.get("nguoi_duoc_kt_chuc_vu", "Phó Tổ trưởng Tổ Toán – Tin học, Giáo viên môn Toán")
    lop_phu_trach = kwargs.get("lop_phu_trach", "môn Toán các lớp 9/5, 9/6, 9/7, 6/5 và kiêm nhiệm Giáo viên chủ nhiệm lớp 9/7")
    dia_diem = kwargs.get("dia_diem", "Văn phòng Tổ Toán – Tin học và Phòng học lớp 9/7, 6/5 Trường THCS Trần Phú")
    
    md_content = f"""<div align="center">

**Mẫu số 04**  
*(Kèm theo Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026 của Sở Giáo dục và Đào tạo thành phố Đồng Nai)*

</div>

| **TRƯỜNG THCS TRẦN PHÚ**<br>Tổ kiểm tra theo Quyết định<br>số: {so_qd} | **CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM**<br>**Độc lập – Tự do – Hạnh phúc**<br>──────────────────<br>*{ngay_kt_str}* |
|:---:|:---:|

---

# BIÊN BẢN KIỂM TRA
### Về việc {ten_cuoc_kt}
──────────────────

Căn cứ Nghị định số 217/2025/NĐ-CP ngày 05 tháng 8 năm 2025 của Chính phủ về hoạt động kiểm tra chuyên ngành;  
Căn cứ Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026 của Sở Giáo dục và Đào tạo thành phố Đồng Nai về việc hướng dẫn công tác kiểm tra nội bộ năm học 2026 - 2027;  
Căn cứ Quyết định số {so_qd} ngày {ngay_qd} của Hiệu trưởng Trường THCS Trần Phú về việc {ten_cuoc_kt};  
Trong tháng 10 năm 2026 (từ ngày 12 tháng 10 năm 2026 đến ngày 23 tháng 10 năm 2026), Tổ kiểm tra đã tiến hành thu thập thông tin, hồ sơ sổ sách chuyên môn, dự giờ thao giảng trực tiếp và kiểm tra thực tế tại {dia_diem} về việc {ten_cuoc_kt}.  
Sau đây là kết quả kiểm tra:

## I. THÀNH PHẦN LÀM VIỆC
1. **Đại diện Tổ kiểm tra:**
   - Ông: **Hoàng Tấn Thiên** – chức vụ: Tổ trưởng chuyên môn (Tổ trưởng tổ kiểm tra).
   - Ông: **Hồ Đăng Danh** – chức vụ: Giáo viên môn Tin học (Thành viên).
   - Bà: **Lê Thị Bình** – chức vụ: Giáo viên môn Toán (Người ghi biên bản).
2. **Đã tiến hành kiểm tra đối với:** Thầy **{nguoi_duoc_kt_ten}**, gồm:
   - Thầy: **{nguoi_duoc_kt_ten}** – chức vụ: {nguoi_duoc_kt_chuc_vu}; phụ trách giảng dạy {lop_phu_trach}.
3. **Người chứng kiến:**
   - Ông: **Đinh Văn Đông** – chức vụ: Hiệu trưởng Trường THCS Trần Phú.
   - Ông: **Hoàng Xuân Ánh** – chức vụ: Giáo viên môn Toán.

## II. NỘI DUNG KIỂM TRA
### **1. Trình độ nghiệp vụ sư phạm:**
**1.1. Nắm vững mục đích, yêu cầu, chương trình và nội dung giảng dạy:**  
- Giáo viên nắm vững chương trình môn Toán (Toán 6 và Toán 9 theo Chương trình GDPT 2018); xác định đúng chuẩn kiến thức, kỹ năng và yêu cầu cần đạt (YCCĐ) của từng bài học; xác định chuẩn xác trọng tâm bài dạy.  
- Xây dựng kế hoạch dạy học bộ môn khoa học, cấu trúc bài dạy hợp lý, thể hiện rõ năng lực chuyên môn và nghiệp vụ sư phạm vững vàng khi đứng lớp. Tích cực liên hệ kiến thức toán học với đời sống thực tế tạo ham thích, hưng phấn, giáo dục toàn diện học sinh.  
=> **Xếp loại:** **Tốt**.

**1.2. Trình độ vận dụng phương pháp dạy học:**  
- Lựa chọn phương pháp khá hợp lý trong giảng dạy, xử lý linh hoạt các phương pháp trong tiết dạy, đúng đặc trưng bộ môn Toán; tổ chức tốt các chuỗi hoạt động học tập (khởi động, hình thành kiến thức, luyện tập, vận dụng).  
- Ứng dụng công nghệ thông tin và công cụ trực quan hiệu quả vào dạy học; chuẩn bị chu đáo đồ dùng dạy học, phiếu học tập phục vụ tiết dạy. Định lượng thời gian các hoạt động khá cân đối.  
- Tác phong sư phạm nhẹ nhàng, chuẩn mực, làm chủ tiết dạy, nhiệt tình, hòa nhã với học sinh khi đứng lớp.  
=> **Xếp loại:** **Tốt**.

**1.3. Hiệu quả tiết dạy (Dự giờ thao giảng 02 tiết):**  
- Học sinh bước đầu nắm vững kiến thức và vận dụng linh hoạt trong giải bài tập; tham gia xây dựng bài khá tốt; sử dụng sách giáo khoa và đồ dùng học tập hợp lý.  
- **Kết quả đánh giá xếp loại sau dự giờ:**  
  + **Tiết dạy 1:** Tiết 18 – *Luyện tập (Hệ thức lượng cạnh và góc trong tam giác vuông)* (Môn Toán 9, Lớp 9/7, Ngày dạy: 13/10/2026).  
    * Người dự giờ: Thầy **Đinh Văn Đông**, Thầy **Hoàng Tấn Thiên**, Thầy **Hồ Đăng Danh**, Thầy **Hoàng Xuân Ánh**.  
    * Nhận xét: Giáo viên chuẩn bị bài chu đáo, hệ thống bài tập logic, rèn luyện tốt kỹ năng tính toán và vận dụng hệ thức lượng cho học sinh; quản lý lớp tốt, tương tác tích cực. Xếp loại: **Giỏi**.  
  + **Tiết dạy 2:** Tiết 21 – *Bài 11: Ước chung, ước chung lớn nhất* (Môn Toán 6, Lớp 6/5, Ngày dạy: 22/10/2026).  
    * Người dự giờ: Thầy **Hoàng Tấn Thiên**, Cô **Lê Thị Bình**.  
    * Nhận xét: Phương pháp đúng đặc trưng bộ môn, tổ chức hoạt động hình thành kiến thức sôi nổi; ứng dụng tốt CNTT và mô phỏng trực quan giúp học sinh nắm vững cách tìm ƯCLN. Xếp loại: **Giỏi**.  
=> **Đánh giá chung về trình độ nghiệp vụ sư phạm:** **Tốt**.

### **2. Thực hiện quy chế, quy định về chuyên môn:**
**2.1. Thực hiện tiến độ chương trình và nề nếp chuyên môn:** Giảng dạy đúng chương trình theo quy định, dạy đủ các tiết theo kế hoạch môn Toán 6 và Toán 9, không cắt xén, không dạy dồn ghép; chấp hành nghiêm túc quy định về ngày giờ công và thực hiện nghiêm túc quy định dạy thêm, học thêm. => **Xếp loại:** **Tốt**.  
**2.2. Chuẩn bị Kế hoạch bài dạy (KHBD):** Soạn giảng kế hoạch dạy học đầy đủ theo kế hoạch dạy học, đúng với PPCT; đảm bảo đủ kiến thức, kỹ năng, có liên hệ thực tế; đầy đủ các bước lên lớp theo Công văn số 5512/BGDĐT-GDTrH, thể hiện rõ các hoạt động thầy và trò; chủ động tích hợp hiệu quả Khung Năng lực số (20%) và 12 tiết Khung AI (được in đậm, in nghiêng rõ nét theo đúng quy chuẩn); đồng bộ lên CSDL ngành và hoàn thành phê duyệt ký số tuần 100%. Soạn đủ các tiết thực hành trải nghiệm theo KHBD. => **Xếp loại:** **Tốt**.  
**2.3. Thực hiện kiểm tra, đánh giá học sinh:** Hoàn thành cơ số điểm theo quy định tới thời điểm kiểm tra; nội dung và hình thức kiểm tra thống nhất chung theo kế hoạch kiểm tra đánh giá đã phê duyệt đầu năm học; có chấm, chữa bài cẩn thận cho học sinh và có nhận xét rõ ràng; cập nhật điểm trên hệ thống và ghi sổ đầu bài khớp tiến độ; chú trọng ra đề kiểm tra bám sát các dạng toán thực tế. => **Xếp loại:** **Tốt**.  
**2.4. Đánh giá việc thực hành, thí nghiệm, sử dụng ĐDDH & STEM:** Dạy đủ các tiết thực hành, trải nghiệm theo quy định; có sử dụng ĐDDH chu đáo để phục vụ cho tiết dạy; bản thân tích cực tìm tòi có ý tưởng về sản phẩm STEM môn Toán. => **Xếp loại:** **Tốt**.  
**2.5. Bồi dưỡng, tự bồi dưỡng và sinh hoạt tổ chuyên môn:** Tham gia đầy đủ các buổi tập huấn theo quy định; tham gia họp tổ, chuyên môn đầy đủ; tham gia sinh hoạt chuyên đề của tổ; tích cực dự giờ khi được phân công; giữ vai trò nòng cốt Phó Tổ trưởng chuyên môn và chuẩn bị bài dạy minh họa Chuyên đề AI cấp cụm trường vào tháng 12/2026. => **Xếp loại:** **Tốt**.  
=> **Đánh giá chung về thực hiện quy chế chuyên môn:** **Tốt**.

### **3. Hoạt động chủ nhiệm lớp (Lớp 9/7):**
- Xây dựng Kế hoạch chủ nhiệm năm học 2026 – 2027 đầy đủ, khoa học, bám sát phương hướng năm học của nhà trường và tình hình thực tế của học sinh khối 9 cuối cấp.  
- Quản lý nề nếp lớp 9/7 rất tốt; duy trì sĩ số chuyên cần cao; sâu sát nắm bắt hoàn cảnh từng học sinh; kịp thời uốn nắn, động viên các em học sinh có biểu hiện chểnh mảng; xây dựng tập thể lớp 9/7 đoàn kết, có ý thức tự quản và thi đua học tập tốt.  
- Thực hiện sổ sách chủ nhiệm sạch đẹp, cập nhật thông tin kịp thời; duy trì kênh phối hợp thường xuyên, hiệu quả giữa GVCN, Ban Giám hiệu, giáo viên bộ môn và Ban đại diện cha mẹ học sinh lớp 9/7; định hướng tốt cho học sinh về phân luồng và ôn thi tuyển sinh lớp 10.  
=> **Đánh giá chung về công tác chủ nhiệm:** **Tốt**.

### **4. Thực hiện các nhiệm vụ khác và phong trào thi đua:**
Hoàn thành mọi phong trào của nhà trường, tham gia tích cực trong các cuộc vận động, đóng góp; gương mẫu hoàn thành các nhiệm vụ đột xuất do Ban Giám hiệu phân công. => **Xếp loại:** **Tốt**.

## III. ĐÁNH GIÁ CHUNG
1. **Ưu điểm:**
   - **Về chuyên môn giảng dạy môn Toán:** Thực hiện đúng phân công chuyên môn, phân phối chương trình môn Toán (các lớp 9/5, 9/6, 9/7, 6/5) và thời khóa biểu các môn phụ trách giảng dạy; chấp hành nghiêm túc quy định về dạy thêm, học thêm. Thực hiện việc kiểm tra, đánh giá đúng theo quy định, đảm bảo cơ số điểm đến thời điểm kiểm tra. Tổ chức giảng dạy đảm bảo yêu cầu cần đạt về năng lực và phẩm chất cho học sinh, thực hiện đúng quy chế chuyên môn, kết quả giảng dạy giỏi (cả 02 tiết dự giờ thao giảng của Ban Giám hiệu và tổ chuyên môn đều đạt loại Giỏi). Hồ sơ Kế hoạch bài dạy chuẩn bị chu đáo theo CV 5512, tích hợp hiệu quả Khung NLS và AI, ký số CSDL ngành đạt 100% đúng hạn. Có ý tưởng tốt trong hoàn thành sản phẩm STEM và đồ dùng dạy học trực quan.
   - **Về công tác chủ nhiệm lớp 9/7:** Có tinh thần trách nhiệm rất cao với lớp chủ nhiệm cuối cấp; xây dựng kế hoạch chủ nhiệm chu đáo; quản lý nề nếp lớp 9/7 chặt chẽ, tạo sự đồng thuận cao với phụ huynh học sinh; sâu sát uốn nắn học sinh và định hướng thi vào lớp 10 đạt hiệu quả rõ nét.
   - **Về vai trò nòng cốt và phong trào:** Luôn gương mẫu, hoàn thành xuất sắc trọng trách Phó Tổ trưởng chuyên môn; tích cực hỗ trợ đồng nghiệp và đang chuẩn bị tốt bài dạy minh họa chuyên đề AI cấp cụm vào tháng 12/2026; tích cực tham gia mọi hoạt động, phong trào của nhà trường.
2. **Tồn tại:**
   - <span style="color:red">Về chuyên môn: Quan tâm nhiều hơn cho học sinh yếu kém của lớp; định lượng thời gian các hoạt động trong tiết dạy đôi chỗ cần hợp lý hơn; hoạt động thực hành lưu ý việc phân công nhiệm vụ của từng thành viên trong nhóm và bài tập về nhà. Cần hướng dẫn học sinh hệ thống kiến thức qua bản đồ tư duy để học sinh dễ nắm vững kiến thức; trong soạn đề kiểm tra cần có ý tưởng sáng tạo hơn, hạn chế rập khuôn các dạng toán thực tế, cẩn trọng hơn trong soạn thảo chuẩn hóa Word Equation (OMML). Tiếp tục tìm tòi, nghiên cứu tham khảo từ đồng nghiệp, tài liệu và nguồn internet.</span>
   - <span style="color:red">Về công tác chủ nhiệm: Tiếp tục theo dõi sát sao hơn nữa nhóm học sinh có nguy cơ đuối sức trong giai đoạn ôn thi tuyển sinh vào lớp 10, phân hóa biện pháp động viên phù hợp với từng đối tượng học sinh cá biệt; đa dạng hóa thêm hình thức sinh hoạt lớp cuối tuần để tạo không khí sôi nổi hơn.</span>
3. **Nguyên nhân:**
   - **Ưu điểm:** Do giáo viên có trình độ chuyên môn vững vàng, nhiệt tình, hòa nhã với học sinh, tinh thần trách nhiệm cao và luôn tâm huyết với nghề nghiệp.
   - **Tồn tại:** <span style="color:red">Do khối lượng công việc chuyên môn phụ trách 4 lớp (9/5, 9/6, 9/7, 6/5) kèm công tác chủ nhiệm lớp 9 cuối cấp nhiều áp lực về mặt thời gian, việc bao quát tỉ mỉ từng đối tượng học sinh cá biệt đôi lúc còn gặp khó khăn.</span>

## IV. KIẾN NGHỊ CỦA TỔ KIỂM TRA
- **Đối với cá nhân (Thầy Trần Sáng):** Cần phát huy mặt mạnh và khắc phục các mặt tồn tại nêu trên; hoàn thành tốt bài dạy minh họa chuyên đề AI cấp cụm trường vào tháng 12/2026.
- **Đối với Tổ chuyên môn:** Tiếp tục quan tâm và giúp đỡ về chuyên môn, nghiệp vụ; tạo điều kiện để Thầy Trần Sáng chia sẻ kinh nghiệm ứng dụng công nghệ, tích hợp AI và bài học STEM cho giáo viên trong tổ cùng học tập, nhân rộng.
- **Đối với Nhà trường:** Cần quan tâm và giúp đỡ về tinh thần, tạo điều kiện thuận lợi về cơ sở vật chất, trang thiết bị dạy học bộ môn và phòng học lớp 9/7.

## V. Ý KIẾN CỦA BỘ PHẬN (NGƯỜI) ĐƯỢC KIỂM TRA
Đồng ý hoàn toàn với nội dung nhận xét, đánh giá của Tổ kiểm tra; nghiêm túc tiếp thu các ý kiến đóng góp và cam kết hoàn thành xuất sắc mọi nhiệm vụ được giao trong năm học 2026 – 2027.

Việc kiểm tra kết thúc vào lúc [CHỮ ĐỎ: 11 giờ 30 phút, ngày 23 tháng 10 năm 2026] và được lập thành biên bản. Biên bản gồm [CHỮ ĐỎ: 04] trang.  
Biên bản này đã được đọc lại cho những người có tên nêu trên cùng nghe và đồng ý ký xác nhận; biên bản được lập thành 02 bản có giá trị như nhau, mỗi bên giữ 01 bản./.

---

| **NGƯỜI ĐƯỢC KIỂM TRA**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**{nguoi_duoc_kt_ten}** | **TỔ TRƯỞNG TỔ KIỂM TRA**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Hoàng Tấn Thiên** | **NGƯỜI GHI BIÊN BẢN**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Lê Thị Bình** |
|:---:|:---:|:---:|
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


def tao_bao_cao_kiem_tra_noi_bo(out_docx_path, out_md_path=None, **kwargs):
    """
    Soạn thảo hoàn chỉnh BÁO CÁO KẾT QUẢ KIỂM TRA (Mẫu số 05 kèm Công văn số 4794/SGDĐT-VP
    ngày 09/9/2026 của Sở GD&ĐT TP Đồng Nai).
    Chuẩn Nghị định 30/2020/NĐ-CP và Quyết định 169/QĐ-THCS.TP của Trường THCS Trần Phú.
    Báo cáo kết quả kiểm tra toàn diện hoạt động sư phạm đối với Thầy Trần Sáng.
    """
    doc = create_nd30_document()
    
    so_qd = kwargs.get("so_qd", "169/QĐ-THCS.TP")
    ngay_qd = kwargs.get("ngay_qd", "05 tháng 10 năm 2026")
    ngay_bc_str = kwargs.get("ngay_bc_str", "Xuân Đông, ngày 23 tháng 10 năm 2026")
    ten_cuoc_kt = kwargs.get("ten_cuoc_kt", "kiểm tra toàn diện hoạt động sư phạm của nhà giáo")
    nguoi_duoc_kt_ten = kwargs.get("nguoi_duoc_kt_ten", "Trần Sáng")
    nguoi_duoc_kt_chuc_vu = kwargs.get("nguoi_duoc_kt_chuc_vu", "Phó Tổ trưởng Tổ Toán – Tin học, Giáo viên môn Toán")
    lop_phu_trach = kwargs.get("lop_phu_trach", "môn Toán các lớp 9/5, 9/6, 9/7, 6/5 và kiêm nhiệm Giáo viên chủ nhiệm lớp 9/7")
    dia_diem = kwargs.get("dia_diem", "Văn phòng Tổ Toán – Tin học và Phòng học lớp 9/7, 6/5 Trường THCS Trần Phú")
    
    # 1. Header chuẩn Mẫu 05
    add_header_ktnb(doc, mau_so="05", so_qd=so_qd, ngay_thang_str=ngay_bc_str)
    
    # 2. Tiêu đề chính
    add_doc_title(doc, "BÁO CÁO", f"Kết quả {ten_cuoc_kt}\n──────────────────")
    
    # 3. Dẫn nhập
    add_paragraph_styled(doc, f"Thực hiện Quyết định kiểm tra số {so_qd} ngày {ngay_qd} của Hiệu trưởng Trường THCS Trần Phú về việc {ten_cuoc_kt};", indent=True)
    add_paragraph_styled(doc, f"Căn cứ Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026 của Sở Giáo dục và Đào tạo thành phố Đồng Nai về việc hướng dẫn công tác kiểm tra nội bộ năm học 2026 - 2027;", indent=True)
    add_paragraph_styled(doc, f"Tổ kiểm tra đã tiến hành kiểm tra thực tế tại {dia_diem}.", indent=True)
    add_paragraph_styled(doc, f"Quá trình kiểm tra, Tổ kiểm tra đã làm việc với Thầy: **{nguoi_duoc_kt_ten}** – chức vụ: {nguoi_duoc_kt_chuc_vu} từ ngày 12 tháng 10 năm 2026 đến ngày 23 tháng 10 năm 2026 và tiến hành kiểm tra, xác minh, dự giờ trực tiếp các nội dung theo quyết định kiểm tra.", indent=True)
    add_paragraph_styled(doc, "Sau đây là kết quả kiểm tra:", indent=True)
    
    # 4. Phần I: Khái quát chung
    add_section_h1(doc, "I. KHÁI QUÁT CHUNG")
    add_paragraph_styled(doc, f"- **Về nhân sự và trình độ đào tạo:** Thầy **{nguoi_duoc_kt_ten}** có trình độ chuyên môn [CHỮ ĐỎ: Đại học Sư phạm Toán], hiện giữ chức vụ Phó Tổ trưởng Tổ Toán – Tin học; năm học 2026 – 2027 được phân công giảng dạy {lop_phu_trach}.", indent=True)
    add_paragraph_styled(doc, "- **Về phẩm chất chính trị và nề nếp:** Giáo viên có lập trường tư tưởng vững vàng, luôn chấp hành nghiêm túc đường lối, chủ trương của Đảng, chính sách pháp luật của Nhà nước và các quy chế chuyên môn của ngành, của nhà trường. Có tinh thần trách nhiệm rất cao, nề nếp ngày giờ công gương mẫu, chan hòa và uy tín đối với đồng nghiệp, phụ huynh và học sinh.", indent=True)
    
    # 5. Phần II: Kết quả kiểm tra, xác minh
    add_section_h1(doc, "II. KẾT QUẢ KIỂM TRA, XÁC MINH")
    
    # 1. Trình độ nghiệp vụ sư phạm
    add_paragraph_styled(doc, "**1. Trình độ nghiệp vụ sư phạm:**", indent=True)
    add_paragraph_styled(doc, "**1.1. Nắm vững mục đích, yêu cầu, chương trình và nội dung giảng dạy:** Nắm vững chương trình môn Toán (Toán 6, 9 Chương trình GDPT 2018), xác định chuẩn xác yêu cầu cần đạt và trọng tâm bài dạy; kế hoạch bài dạy hợp lý, thể hiện rõ năng lực chuyên môn khi đứng lớp. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**1.2. Vận dụng phương pháp dạy học:** Lựa chọn phương pháp dạy học tích cực phù hợp đặc trưng bộ môn Toán; tổ chức tốt các hoạt động học tập; ứng dụng CNTT và mô phỏng trực quan hiệu quả; tác phong sư phạm chuẩn mực, nhiệt tình, hòa nhã, làm chủ lớp học. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**1.3. Hiệu quả tiết dạy (Dự giờ thao giảng):** Học sinh tích cực học tập, vận dụng linh hoạt kiến thức giải bài tập. Kết quả dự giờ 02 tiết của giáo viên:", indent=True)
    add_paragraph_styled(doc, "- **Tiết dạy 1:** Tiết 18 – *Luyện tập (Hệ thức lượng cạnh và góc trong tam giác vuông)* (Môn Toán 9, Lớp 9/7, Ngày dạy: 13/10/2026). Người dự: Thầy Đinh Văn Đông, Thầy Hoàng Tấn Thiên, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh. Xếp loại: **Giỏi**.", indent=True)
    add_paragraph_styled(doc, "- **Tiết dạy 2:** Tiết 21 – *Bài 11: Ước chung, ước chung lớn nhất* (Môn Toán 6, Lớp 6/5, Ngày dạy: 22/10/2026). Người dự: Thầy Hoàng Tấn Thiên, Cô Lê Thị Bình. Xếp loại: **Giỏi**.", indent=True)
    add_paragraph_styled(doc, "=> **Xếp loại chung nghiệp vụ sư phạm:** **Tốt**.", indent=True)
    
    # 2. Thực hiện quy chế, quy định về chuyên môn
    add_paragraph_styled(doc, "**2. Thực hiện quy chế, quy định về chuyên môn:**", indent=True)
    add_paragraph_styled(doc, "**2.1. Tiến độ chương trình và ngày giờ công:** Thực hiện đúng phân phối chương trình môn Toán, dạy đủ số tiết theo kế hoạch, không cắt xén, không dạy dồn ghép; chấp hành nghiêm túc quy định dạy thêm, học thêm. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**2.2. Chuẩn bị Kế hoạch bài dạy (KHBD):** Soạn bài đầy đủ theo CV 5512 cấu trúc 4 hoạt động; tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI in đậm nghiêng đúng chuẩn; đồng bộ và ký số CSDL ngành đạt 100% đúng hạn. Soạn đủ các tiết thực hành trải nghiệm. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**2.3. Kiểm tra, đánh giá học sinh:** Đảm bảo cơ số điểm kiểm tra thường xuyên theo Thông tư 22/2021/TT-BGDĐT; chấm chữa bài cẩn thận, nhận xét rõ ràng, vào điểm và ghi sổ đầu bài khớp tiến độ; chú trọng đưa toán thực tế vào đánh giá. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**2.4. Thực hành, thí nghiệm, ĐDDH & STEM:** Dạy đủ tiết thực hành trải nghiệm; sử dụng hiệu quả đồ dùng dạy học; bản thân có ý tưởng tốt về sản phẩm STEM môn Toán. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "**2.5. Bồi dưỡng và sinh hoạt chuyên môn:** Tham gia đầy đủ các lớp tập huấn; dự giờ đồng nghiệp đúng quy định; nòng cốt tham gia chỉ đạo chuyên môn tổ và tích cực chuẩn bị bài dạy minh họa chuyên đề AI cấp cụm vào tháng 12/2026. => **Xếp loại:** **Tốt**.", indent=True)
    add_paragraph_styled(doc, "=> **Xếp loại chung thực hiện quy chế chuyên môn:** **Tốt**.", indent=True)
    
    # 3. Hoạt động chủ nhiệm lớp (Lớp 9/7)
    add_paragraph_styled(doc, "**3. Hoạt động chủ nhiệm lớp (Lớp 9/7):**", indent=True)
    add_paragraph_styled(doc, "- Kế hoạch chủ nhiệm lớp 9/7 được xây dựng đầy đủ, bám sát phương hướng năm học của nhà trường và tình hình học sinh cuối cấp.", indent=True)
    add_paragraph_styled(doc, "- Quản lý nề nếp lớp 9/7 chặt chẽ, duy trì sĩ số tốt; kịp thời uốn nắn học sinh có biểu hiện sa sút, xây dựng tập thể lớp tự quản tốt.", indent=True)
    add_paragraph_styled(doc, "- Sổ sách chủ nhiệm ghi chép cẩn thận, khoa học; duy trì mối liên hệ thường xuyên, hiệu quả giữa gia đình và nhà trường; định hướng phân luồng và ôn thi tuyển sinh lớp 10 tích cực. => **Xếp loại:** **Tốt**.", indent=True)
    
    # 4. Thực hiện các nhiệm vụ khác
    add_paragraph_styled(doc, "**4. Thực hiện các nhiệm vụ khác và phong trào thi đua:**", indent=True)
    add_paragraph_styled(doc, "Hoàn thành mọi phong trào thi đua của nhà trường; tích cực tham gia các cuộc vận động, đóng góp; gương mẫu hoàn thành các nhiệm vụ đột xuất được phân công. => **Xếp loại:** **Tốt**.", indent=True)
    
    # 6. Phần III: Kết luận về những nội dung đã tiến hành kiểm tra
    add_section_h1(doc, "III. KẾT LUẬN VỀ NHỮNG NỘI DUNG ĐÃ TIẾN HÀNH KIỂM TRA")
    add_paragraph_styled(doc, "**1. Kết quả đạt được (Ưu điểm):**", indent=True)
    add_paragraph_styled(doc, "- **Về chuyên môn môn Toán:** Thực hiện đúng phân công chuyên môn, phân phối chương trình các lớp 9/5, 9/6, 9/7, 6/5 và thời khóa biểu; chấp hành nghiêm quy định dạy thêm, học thêm. Thực hiện việc kiểm tra, đánh giá đúng theo quy định, đảm bảo cơ số điểm đến thời điểm kiểm tra. Tổ chức giảng dạy đảm bảo yêu cầu cần đạt về năng lực và phẩm chất cho học sinh, thực hiện đúng quy chế chuyên môn, kết quả giảng dạy giỏi (cả 02 tiết dự giờ thao giảng của Ban Giám hiệu và tổ chuyên môn đều đạt loại Giỏi). Hồ sơ Kế hoạch bài dạy chuẩn bị rất công phu, đúng cấu trúc 4 hoạt động theo Công văn 5512/BGDĐT-GDTrH; xác định chuẩn xác yêu cầu cần đạt và trọng tâm bài dạy; tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI sáng tạo, in đậm nghiêng đúng chuẩn; đồng bộ và ký số CSDL ngành đạt 100% đúng hạn. Có ý tưởng tốt trong hoàn thành sản phẩm STEM và khai thác ĐDDH trực quan.", indent=True)
    add_paragraph_styled(doc, "- **Về công tác chủ nhiệm lớp 9/7:** Tinh thần trách nhiệm rất cao với lớp cuối cấp; quản lý nề nếp lớp 9/7 chặt chẽ, tạo sự đồng thuận cao với phụ huynh học sinh; sâu sát uốn nắn học sinh và định hướng thi vào lớp 10 đạt hiệu quả rõ nét.", indent=True)
    add_paragraph_styled(doc, "- **Về vai trò nòng cốt:** Hoàn thành xuất sắc nhiệm vụ Phó Tổ trưởng chuyên môn; nòng cốt tham gia chỉ đạo ra đề kiểm tra giữa kỳ I và tích cực chuẩn bị bài dạy minh họa chuyên đề AI cấp cụm vào tháng 12/2026.", indent=True)
    
    add_paragraph_styled(doc, "**2. Hạn chế (Tồn tại):**", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: - Về chuyên môn: Quan tâm nhiều hơn cho học sinh yếu kém của lớp; định lượng thời gian các hoạt động trong tiết dạy đôi chỗ cần hợp lý hơn; hoạt động thực hành lưu ý việc phân công nhiệm vụ của từng thành viên trong nhóm và bài tập về nhà. Cần hướng dẫn học sinh hệ thống kiến thức qua bản đồ tư duy để học sinh dễ nắm vững kiến thức; trong soạn đề kiểm tra cần có ý tưởng sáng tạo hơn, hạn chế rập khuôn các dạng toán thực tế, cẩn trọng hơn trong soạn thảo chuẩn hóa Word Equation (OMML). Tiếp tục tìm tòi, nghiên cứu tham khảo từ đồng nghiệp, tài liệu và nguồn internet.]", indent=True)
    add_paragraph_styled(doc, "[CHỮ ĐỎ: - Về công tác chủ nhiệm: Tiếp tục theo dõi sát sao hơn nữa nhóm học sinh có nguy cơ đuối sức trong giai đoạn ôn thi tuyển sinh vào lớp 10, phân hóa biện pháp động viên phù hợp với từng đối tượng học sinh cá biệt; đa dạng hóa thêm hình thức sinh hoạt lớp cuối tuần để tạo không khí sôi nổi hơn.]", indent=True)
    
    add_paragraph_styled(doc, "**3. Đánh giá, xếp loại chung:** Toàn bộ hoạt động sư phạm của nhà giáo được Tổ kiểm tra thống nhất xếp loại: **TỐT**.", indent=True)
    
    # 7. Phần IV: Các biện pháp xử lý theo thẩm quyền đã áp dụng (nếu có)
    add_section_h1(doc, "IV. CÁC BIỆN PHÁP XỬ LÝ THEO THẨM QUYỀN ĐÃ ÁP DỤNG (NẾU CÓ)")
    add_paragraph_styled(doc, "Không (Giáo viên không có sai phạm phải áp dụng biện pháp xử lý).", indent=True)
    
    # 8. Phần V: Những ý kiến khác nhau giữa các thành viên đoàn kiểm tra (nếu có)
    add_section_h1(doc, "V. NHỮNG Ý KIẾN KHÁC NHAU GIỮA CÁC THÀNH VIÊN ĐOÀN KIỂM TRA (NẾU CÓ)")
    add_paragraph_styled(doc, "Không (100% thành viên Tổ kiểm tra thống nhất với toàn bộ kết quả, biên bản và báo cáo đánh giá).", indent=True)
    
    # 9. Phần VI: Kiến nghị và biện pháp xử lý
    add_section_h1(doc, "VI. KIẾN NGHỊ VÀ BIỆN PHÁP XỬ LÝ")
    add_paragraph_styled(doc, "**1.** Đề nghị Ban Giám hiệu nhà trường ghi nhận, biểu dương kết quả kiểm tra xếp loại Tốt của Thầy Trần Sáng; xem xét khen thưởng trong các đợt thi đua chào mừng Ngày Nhà giáo Việt Nam 20/11.", indent=True)
    add_paragraph_styled(doc, "**2.** Đề nghị Hiệu trưởng tạo điều kiện thuận lợi và phê duyệt kế hoạch để Thầy Trần Sáng và Cô Lê Thị Bình đại diện tổ triển khai thành công bài dạy minh họa Chuyên đề AI cấp cụm trường vào tháng 12/2026.", indent=True)
    add_paragraph_styled(doc, "**3.** Giao Tổ chuyên môn Toán – Tin học tổ chức sinh hoạt nhân rộng mô hình tích hợp Khung AI, Năng lực số và ứng dụng STEM của Thầy Sáng cho toàn thể giáo viên trong tổ học tập, chia sẻ.", indent=True)
    
    # Đoạn kết
    add_paragraph_styled(doc, f"Trên đây là Báo cáo kết quả {ten_cuoc_kt} đối với Thầy Trần Sáng, Tổ kiểm tra kính xin ý kiến chỉ đạo của Hiệu trưởng nhà trường./.", indent=True)
    
    # Khung chữ ký và nơi nhận
    add_ktnb_bao_cao_signatures(doc, to_truong="Hoàng Tấn Thiên")
    
    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    save_docx_robust(doc, out_docx_path)
    print(f"Da xuat thanh cong Bao cao KTNB (Mau 05): {out_docx_path}")
    
    if out_md_path:
        os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
        tao_bao_cao_kiem_tra_noi_bo_md(out_md_path, **kwargs)
        print(f"Da xuat thanh cong Bao cao KTNB Markdown: {out_md_path}")


def tao_bao_cao_kiem_tra_noi_bo_md(out_md_path, **kwargs):
    """Xuất Markdown cho Mẫu 05 (Báo cáo kết quả kiểm tra)."""
    so_qd = kwargs.get("so_qd", "169/QĐ-THCS.TP")
    ngay_qd = kwargs.get("ngay_qd", "05 tháng 10 năm 2026")
    ngay_bc_str = kwargs.get("ngay_bc_str", "Xuân Đông, ngày 23 tháng 10 năm 2026")
    ten_cuoc_kt = kwargs.get("ten_cuoc_kt", "kiểm tra toàn diện hoạt động sư phạm của nhà giáo")
    nguoi_duoc_kt_ten = kwargs.get("nguoi_duoc_kt_ten", "Trần Sáng")
    nguoi_duoc_kt_chuc_vu = kwargs.get("nguoi_duoc_kt_chuc_vu", "Phó Tổ trưởng Tổ Toán – Tin học, Giáo viên môn Toán")
    lop_phu_trach = kwargs.get("lop_phu_trach", "môn Toán các lớp 9/5, 9/6, 9/7, 6/5 và kiêm nhiệm Giáo viên chủ nhiệm lớp 9/7")
    dia_diem = kwargs.get("dia_diem", "Văn phòng Tổ Toán – Tin học và Phòng học lớp 9/7, 6/5 Trường THCS Trần Phú")
    
    md_content = f"""<div align="center">

**Mẫu số 05**  
*(Kèm theo Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026 của Sở Giáo dục và Đào tạo thành phố Đồng Nai)*

</div>

| **TRƯỜNG THCS TRẦN PHÚ**<br>Tổ kiểm tra theo Quyết định<br>số: {so_qd} | **CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM**<br>**Độc lập – Tự do – Hạnh phúc**<br>──────────────────<br>*{ngay_bc_str}* |
|:---:|:---:|

---

# BÁO CÁO
### Kết quả {ten_cuoc_kt}
──────────────────

Thực hiện Quyết định kiểm tra số {so_qd} ngày {ngay_qd} của Hiệu trưởng Trường THCS Trần Phú về việc {ten_cuoc_kt};  
Căn cứ Công văn số 4794/SGDĐT-VP ngày 09 tháng 9 năm 2026 của Sở Giáo dục và Đào tạo thành phố Đồng Nai về việc hướng dẫn công tác kiểm tra nội bộ năm học 2026 - 2027;  
Tổ kiểm tra đã tiến hành kiểm tra thực tế tại {dia_diem}.  
Quá trình kiểm tra, Tổ kiểm tra đã làm việc với Thầy: **{nguoi_duoc_kt_ten}** – chức vụ: {nguoi_duoc_kt_chuc_vu} từ ngày 12 tháng 10 năm 2026 đến ngày 23 tháng 10 năm 2026 và tiến hành kiểm tra, xác minh, dự giờ trực tiếp các nội dung theo quyết định kiểm tra.  
Sau đây là kết quả kiểm tra:

## I. KHÁI QUÁT CHUNG
- **Về nhân sự và trình độ đào tạo:** Thầy **{nguoi_duoc_kt_ten}** có trình độ chuyên môn [CHỮ ĐỎ: Đại học Sư phạm Toán], hiện giữ chức vụ Phó Tổ trưởng Tổ Toán – Tin học; năm học 2026 – 2027 được phân công giảng dạy {lop_phu_trach}.
- **Về phẩm chất chính trị và nề nếp:** Giáo viên có lập trường tư tưởng vững vàng, luôn chấp hành nghiêm túc đường lối, chủ trương của Đảng, chính sách pháp luật của Nhà nước và các quy chế chuyên môn của ngành, của nhà trường. Có tinh thần trách nhiệm rất cao, nề nếp ngày giờ công gương mẫu, chan hòa và uy tín đối với đồng nghiệp, phụ huynh và học sinh.

## II. KẾT QUẢ KIỂM TRA, XÁC MINH
### **1. Trình độ nghiệp vụ sư phạm:**
**1.1. Nắm vững mục đích, yêu cầu, chương trình và nội dung giảng dạy:** Nắm vững chương trình môn Toán (Toán 6, 9 Chương trình GDPT 2018), xác định chuẩn xác yêu cầu cần đạt và trọng tâm bài dạy; kế hoạch bài dạy hợp lý, thể hiện rõ năng lực chuyên môn khi đứng lớp. => **Xếp loại:** **Tốt**.  
**1.2. Vận dụng phương pháp dạy học:** Lựa chọn phương pháp dạy học tích cực phù hợp đặc trưng bộ môn Toán; tổ chức tốt các hoạt động học tập; ứng dụng CNTT và mô phỏng trực quan hiệu quả; tác phong sư phạm chuẩn mực, nhiệt tình, hòa nhã, làm chủ lớp học. => **Xếp loại:** **Tốt**.  
**1.3. Hiệu quả tiết dạy (Dự giờ thao giảng):** Học sinh tích cực học tập, vận dụng linh hoạt kiến thức giải bài tập. Kết quả dự giờ 02 tiết của giáo viên:  
- **Tiết dạy 1:** Tiết 18 – *Luyện tập (Hệ thức lượng cạnh và góc trong tam giác vuông)* (Môn Toán 9, Lớp 9/7, Ngày dạy: 13/10/2026). Người dự: Thầy Đinh Văn Đông, Thầy Hoàng Tấn Thiên, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh. Xếp loại: **Giỏi**.  
- **Tiết dạy 2:** Tiết 21 – *Bài 11: Ước chung, ước chung lớn nhất* (Môn Toán 6, Lớp 6/5, Ngày dạy: 22/10/2026). Người dự: Thầy Hoàng Tấn Thiên, Cô Lê Thị Bình. Xếp loại: **Giỏi**.  
=> **Xếp loại chung nghiệp vụ sư phạm:** **Tốt**.

### **2. Thực hiện quy chế, quy định về chuyên môn:**
**2.1. Tiến độ chương trình và ngày giờ công:** Thực hiện đúng phân phối chương trình môn Toán, dạy đủ số tiết theo kế hoạch, không cắt xén, không dạy dồn ghép; chấp hành nghiêm túc quy định dạy thêm, học thêm. => **Xếp loại:** **Tốt**.  
**2.2. Chuẩn bị Kế hoạch bài dạy (KHBD):** Soạn bài đầy đủ theo CV 5512 cấu trúc 4 hoạt động; tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI in đậm nghiêng đúng chuẩn; đồng bộ và ký số CSDL ngành đạt 100% đúng hạn. Soạn đủ các tiết thực hành trải nghiệm. => **Xếp loại:** **Tốt**.  
**2.3. Kiểm tra, đánh giá học sinh:** Đảm bảo cơ số điểm kiểm tra thường xuyên theo Thông tư 22/2021/TT-BGDĐT; chấm chữa bài cẩn thận, nhận xét rõ ràng, vào điểm và ghi sổ đầu bài khớp tiến độ; chú trọng đưa toán thực tế vào đánh giá. => **Xếp loại:** **Tốt**.  
**2.4. Thực hành, thí nghiệm, ĐDDH & STEM:** Dạy đủ tiết thực hành trải nghiệm; sử dụng hiệu quả đồ dùng dạy học; bản thân có ý tưởng tốt về sản phẩm STEM môn Toán. => **Xếp loại:** **Tốt**.  
**2.5. Bồi dưỡng và sinh hoạt chuyên môn:** Tham gia đầy đủ các lớp tập huấn; dự giờ đồng nghiệp đúng quy định; nòng cốt tham gia chỉ đạo chuyên môn tổ và tích cực chuẩn bị bài dạy minh họa chuyên đề AI cấp cụm vào tháng 12/2026. => **Xếp loại:** **Tốt**.  
=> **Xếp loại chung thực hiện quy chế chuyên môn:** **Tốt**.

### **3. Hoạt động chủ nhiệm lớp (Lớp 9/7):**
- Kế hoạch chủ nhiệm lớp 9/7 được xây dựng đầy đủ, bám sát phương hướng năm học của nhà trường và tình hình học sinh cuối cấp.  
- Quản lý nề nếp lớp 9/7 chặt chẽ, duy trì sĩ số tốt; kịp thời uốn nắn học sinh có biểu hiện sa sút, xây dựng tập thể lớp tự quản tốt.  
- Sổ sách chủ nhiệm ghi chép cẩn thận, khoa học; duy trì mối liên hệ thường xuyên, hiệu quả giữa gia đình và nhà trường; định hướng phân luồng và ôn thi tuyển sinh lớp 10 tích cực. => **Xếp loại:** **Tốt**.

### **4. Thực hiện các nhiệm vụ khác và phong trào thi đua:**
Hoàn thành mọi phong trào thi đua của nhà trường; tích cực tham gia các cuộc vận động, đóng góp; gương mẫu hoàn thành các nhiệm vụ đột xuất được phân công. => **Xếp loại:** **Tốt**.

## III. KẾT LUẬN VỀ NHỮNG NỘI DUNG ĐÃ TIẾN HÀNH KIỂM TRA
1. **Kết quả đạt được (Ưu điểm):**
   - **Về chuyên môn môn Toán:** Thực hiện đúng phân công chuyên môn, phân phối chương trình các lớp 9/5, 9/6, 9/7, 6/5 và thời khóa biểu; chấp hành nghiêm quy định dạy thêm, học thêm. Thực hiện việc kiểm tra, đánh giá đúng theo quy định, đảm bảo cơ số điểm đến thời điểm kiểm tra. Tổ chức giảng dạy đảm bảo yêu cầu cần đạt về năng lực và phẩm chất cho học sinh, thực hiện đúng quy chế chuyên môn, kết quả giảng dạy giỏi (cả 02 tiết dự giờ thao giảng của Ban Giám hiệu và tổ chuyên môn đều đạt loại Giỏi). Hồ sơ Kế hoạch bài dạy chuẩn bị rất công phu, đúng cấu trúc 4 hoạt động theo Công văn 5512/BGDĐT-GDTrH; xác định chuẩn xác yêu cầu cần đạt và trọng tâm bài dạy; tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI sáng tạo, in đậm nghiêng đúng chuẩn; đồng bộ và ký số CSDL ngành đạt 100% đúng hạn. Có ý tưởng tốt trong hoàn thành sản phẩm STEM và khai thác ĐDDH trực quan.
   - **Về công tác chủ nhiệm lớp 9/7:** Tinh thần trách nhiệm rất cao với lớp cuối cấp; quản lý nề nếp lớp 9/7 chặt chẽ, tạo sự đồng thuận cao với phụ huynh học sinh; sâu sát uốn nắn học sinh và định hướng thi vào lớp 10 đạt hiệu quả rõ nét.
   - **Về vai trò nòng cốt:** Hoàn thành xuất sắc nhiệm vụ Phó Tổ trưởng chuyên môn; nòng cốt tham gia chỉ đạo ra đề kiểm tra giữa kỳ I và tích cực chuẩn bị bài dạy minh họa chuyên đề AI cấp cụm vào tháng 12/2026.
2. **Hạn chế (Tồn tại):**
   - <span style="color:red">Về chuyên môn: Quan tâm nhiều hơn cho học sinh yếu kém của lớp; định lượng thời gian các hoạt động trong tiết dạy đôi chỗ cần hợp lý hơn; hoạt động thực hành lưu ý việc phân công nhiệm vụ của từng thành viên trong nhóm và bài tập về nhà. Cần hướng dẫn học sinh hệ thống kiến thức qua bản đồ tư duy để học sinh dễ nắm vững kiến thức; trong soạn đề kiểm tra cần có ý tưởng sáng tạo hơn, hạn chế rập khuôn các dạng toán thực tế, cẩn trọng hơn trong soạn thảo chuẩn hóa Word Equation (OMML). Tiếp tục tìm tòi, nghiên cứu tham khảo từ đồng nghiệp, tài liệu và nguồn internet.</span>
   - <span style="color:red">Về công tác chủ nhiệm: Tiếp tục theo dõi sát sao hơn nữa nhóm học sinh có nguy cơ đuối sức trong giai đoạn ôn thi tuyển sinh vào lớp 10, phân hóa biện pháp động viên phù hợp với từng đối tượng học sinh cá biệt; đa dạng hóa thêm hình thức sinh hoạt lớp cuối tuần để tạo không khí sôi nổi hơn.</span>
3. **Đánh giá, xếp loại chung:** Toàn bộ hoạt động sư phạm của nhà giáo được Tổ kiểm tra thống nhất xếp loại: **TỐT**.

## IV. CÁC BIỆN PHÁP XỬ LÝ THEO THẨM QUYỀN ĐÃ ÁP DỤNG (NẾU CÓ)
Không (Giáo viên không có sai phạm phải áp dụng biện pháp xử lý).

## V. NHỮNG Ý KIẾN KHÁC NHAU GIỮA CÁC THÀNH VIÊN ĐOÀN KIỂM TRA (NẾU CÓ)
Không (100% thành viên Tổ kiểm tra thống nhất với toàn bộ kết quả, biên bản và báo cáo đánh giá).

## VI. KIẾN NGHỊ VÀ BIỆN PHÁP XỬ LÝ
1. Đề nghị Ban Giám hiệu nhà trường ghi nhận, biểu dương kết quả kiểm tra xếp loại Tốt của Thầy Trần Sáng; xem xét khen thưởng trong các đợt thi đua chào mừng Ngày Nhà giáo Việt Nam 20/11.
2. Đề nghị Hiệu trưởng tạo điều kiện thuận lợi và phê duyệt kế hoạch để Thầy Trần Sáng và Cô Lê Thị Bình đại diện tổ triển khai thành công bài dạy minh họa Chuyên đề AI cấp cụm trường vào tháng 12/2026.
3. Giao Tổ chuyên môn Toán – Tin học tổ chức sinh hoạt nhân rộng mô hình tích hợp Khung AI, Năng lực số và ứng dụng STEM của Thầy Sáng cho toàn thể giáo viên trong tổ học tập, chia sẻ.

Trên đây là Báo cáo kết quả {ten_cuoc_kt} đối với Thầy Trần Sáng, Tổ kiểm tra kính xin ý kiến chỉ đạo của Hiệu trưởng nhà trường./.

---

| **Nơi nhận:**<br>*- Hiệu trưởng (để b/c);*<br>*- Ông Trần Sáng (để t/h);*<br>*- Lưu: Hồ sơ KTNB.* | **TỔ TRƯỞNG TỔ KIỂM TRA**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Hoàng Tấn Thiên** |
|:---|:---:|
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Hệ thống xuất văn bản Word chuẩn NĐ 30 Tổ Toán - Tin THCS Trần Phú")
    parser.add_argument("--loai", type=str, default="tat_ca", choices=["bien_ban_2_10", "bao_cao_thang_10", "ktnb_bien_ban", "ktnb_bao_cao", "ktnb", "tat_ca"], help="Loại văn bản cần xuất")
    parser.add_argument("--out-dir", type=str, default="c:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/22.10", help="Thư mục kết quả")
    args = parser.parse_args()
    
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    root_ket_qua = Path("c:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua")
    root_ket_qua.mkdir(parents=True, exist_ok=True)
    import shutil
    
    # Chức năng 1: Biên bản họp tổ
    if args.loai in ("bien_ban_2_10", "tat_ca"):
        docx_file = out_dir / "Bien_Ban_Hop_To_Lan_2_Thang_10_2026.docx"
        md_file = out_dir / "Bien_Ban_Hop_To_Lan_2_Thang_10_2026.md"
        tao_bien_ban_hop_to_lan_2_thang_10(str(docx_file), str(md_file))
        safe_copy2(docx_file, root_ket_qua / "Bien_Ban_Hop_To_Lan_2_Thang_10_2026.docx")
        safe_copy2(md_file, root_ket_qua / "Bien_Ban_Hop_To_Lan_2_Thang_10_2026.md")
        print(f"Da dong bo Bien ban hop to vao: {root_ket_qua / 'Bien_Ban_Hop_To_Lan_2_Thang_10_2026.docx'}")
        
    # Chức năng 2: Báo cáo hoạt động tháng
    if args.loai in ("bao_cao_thang_10", "tat_ca"):
        docx_file_bc = out_dir / "Bao_Cao_Hoat_Dong_To_Toan_Tin_Thang_10_2026.docx"
        md_file_bc = out_dir / "Bao_Cao_Hoat_Dong_To_Toan_Tin_Thang_10_2026.md"
        tao_bao_cao_thang_10(str(docx_file_bc), str(md_file_bc))
        safe_copy2(docx_file_bc, root_ket_qua / "Bao_Cao_Hoat_Dong_To_Toan_Tin_Thang_10_2026.docx")
        safe_copy2(md_file_bc, root_ket_qua / "Bao_Cao_Hoat_Dong_To_Toan_Tin_Thang_10_2026.md")
        print(f"Da dong bo Bao cao thang 10 vao: {root_ket_qua / 'Bao_Cao_Hoat_Dong_To_Toan_Tin_Thang_10_2026.docx'}")

    # Chức năng 3: Kiểm tra nội bộ (KTNB - Mẫu 04 & Mẫu 05)
    if args.loai in ("ktnb_bien_ban", "ktnb", "tat_ca"):
        docx_file_bb_ktnb = out_dir / "KTNB_Mau_04_Bien_Ban_Kiem_Tra.docx"
        md_file_bb_ktnb = out_dir / "KTNB_Mau_04_Bien_Ban_Kiem_Tra.md"
        tao_bien_ban_kiem_tra_noi_bo(str(docx_file_bb_ktnb), str(md_file_bb_ktnb))
        safe_copy2(docx_file_bb_ktnb, root_ket_qua / "KTNB_Mau_04_Bien_Ban_Kiem_Tra.docx")
        safe_copy2(md_file_bb_ktnb, root_ket_qua / "KTNB_Mau_04_Bien_Ban_Kiem_Tra.md")
        print(f"Da dong bo Bien ban KTNB Mau 04 vao: {root_ket_qua / 'KTNB_Mau_04_Bien_Ban_Kiem_Tra.docx'}")

    if args.loai in ("ktnb_bao_cao", "ktnb", "tat_ca"):
        docx_file_bc_ktnb = out_dir / "KTNB_Mau_05_Bao_Cao_Ket_Qua_Kiem_Tra.docx"
        md_file_bc_ktnb = out_dir / "KTNB_Mau_05_Bao_Cao_Ket_Qua_Kiem_Tra.md"
        tao_bao_cao_kiem_tra_noi_bo(str(docx_file_bc_ktnb), str(md_file_bc_ktnb))
        safe_copy2(docx_file_bc_ktnb, root_ket_qua / "KTNB_Mau_05_Bao_Cao_Ket_Qua_Kiem_Tra.docx")
        safe_copy2(md_file_bc_ktnb, root_ket_qua / "KTNB_Mau_05_Bao_Cao_Ket_Qua_Kiem_Tra.md")
        print(f"Da dong bo Bao cao KTNB Mau 05 vao: {root_ket_qua / 'KTNB_Mau_05_Bao_Cao_Ket_Qua_Kiem_Tra.docx'}")




