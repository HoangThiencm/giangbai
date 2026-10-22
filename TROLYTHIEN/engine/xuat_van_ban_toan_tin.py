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


def add_table_phan_cong_thang_8(doc):
    """Bảng dự kiến phân công chuyên môn HKI năm học 2026 - 2027 (chuẩn 6 cột)."""
    headers = ["STT", "Họ và tên giáo viên", "Môn và lớp phụ trách giảng dạy", "Nhiệm vụ kiêm nhiệm / khác", "Số tiết/tuần", "Ghi chú"]
    data = [
        ["1", "Hoàng Tấn Thiên", "Toán 6 (3 lớp - 12 tiết)", "Tổ trưởng chuyên môn (3t), Phụ trách Chuyển đổi số (3t)", "18", "Tổ trưởng"],
        ["2", "Trần Sáng", "Toán 9 (3 lớp - 12 tiết), Tin học 9 (1 lớp - 1 tiết)", "Phó Tổ trưởng (1t), Chủ nhiệm lớp 9/7 (4t)", "18", "Phó Tổ trưởng"],
        ["3", "Đinh Văn Đông", "Hoạt động TN, HN (3 tiết)", "Hiệu trưởng nhà trường", "3", "BGH sinh hoạt tổ"],
        ["4", "Hồ Đăng Danh", "Toán 9 (4 lớp - 16 tiết)", "Thành viên ban CNTT & CSDL ngành", "16", "GV môn Toán"],
        ["5", "Hoàng Xuân Ánh", "Toán 8 (3 lớp - 12 tiết), Tin học 6 (4 lớp - 4 tiết)", "Ủy viên tổ chuyên môn", "16", "GV Toán - Tin"],
        ["6", "Trần Long Hải", "Toán 8 (3 lớp - 12 tiết), HĐTN, HN (3 tiết)", "Chủ nhiệm lớp 8/3 (4t)", "19", "GV môn Toán"],
        ["7", "Lê Thị Bình", "Toán 7 (3 lớp - 12 tiết), HĐTN, HN (3 tiết)", "Chủ nhiệm lớp 7/1 (4t), Thư ký tổ", "19", "GV môn Toán"],
        ["8", "Nguyễn Thị Thảo", "Toán 6 (1 lớp - 4t), Toán 7 (1 lớp - 4t)\nTin 6 (2 lớp - 2t), Tin 7 (2 lớp - 2t), HĐTN (3t)", "Chủ nhiệm lớp 6/2 (4t)", "19", "GV Toán - Tin"],
        ["9", "Nguyễn Văn Tính", "Toán 6 (2 lớp - 8 tiết), Toán 7 (2 lớp - 8 tiết)", "Ủy viên tổ chuyên môn", "16", "GV môn Toán"],
        ["10", "Dương Quang Tùng", "Tin 7 (4 lớp - 4t), Tin 8 (6 lớp - 6t), Tin 9 (6 lớp - 6t)", "Phụ trách phòng máy vi tính bộ môn (3t)", "19", "GV Tin học"]
    ]
    
    col_widths = [Inches(0.5), Inches(1.5), Inches(2.3), Inches(2.0), Inches(0.8), Inches(0.9)]
    
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    format_table_borders_closed(table)
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        shading = parse_xml(r'<w:shd {} w:fill="F2F2F2"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)
        
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.bold = True
        
    # Data rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].width = col_widths[col_idx]
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            if col_idx in (0, 4, 5):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            add_run_parsed(p, str(cell_value), default_size=11.5)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(2)

def tao_bien_ban_hop_to_lan_1_thang_8(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 1 Tháng 8/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # 1. Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="01/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 26 tháng 8 năm 2026"
    )
    
    # 2. Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1",
        "SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 8/2026\n(Chuẩn bị năm học mới 2026 – 2027)"
    )
    
    # 3. Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 10 giờ 00 phút, ngày 26 tháng 8 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 8 chuẩn bị cho năm học mới 2026 – 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # 4. NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt các văn bản chỉ đạo trọng tâm của Bộ Giáo dục và Đào tạo, UBND thành phố Đồng Nai và Sở Giáo dục và Đào tạo; đồng thời tóm tắt các vấn đề cốt lõi tác động trực tiếp đến kế hoạch thực hiện của nhà trường và Tổ chuyên môn Toán – Tin học như sau:", indent=True)
    
    # 1. Kế hoạch thời gian năm học (QĐ 2308/QĐ-BGDĐT & QĐ 2322/QĐ-UBND)
    add_paragraph_styled(doc, "**1. Kế hoạch thời gian năm học 2026 – 2027 (Quyết định số 2308/QĐ-BGDĐT ngày 06/8/2026 của Bộ GD&ĐT và Quyết định số 2322/QĐ-UBND ngày 19/8/2026 của UBND thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Toàn quốc và thành phố thống nhất tổ chức Khai giảng năm học mới vào ngày 05/9/2026. Khung kế hoạch bảo đảm đủ 35 tuần thực học (Học kỳ I: 18 tuần, từ ngày 07/9/2026 đến ngày 16/01/2027; Học kỳ II: 17 tuần, từ ngày 18/01/2027 đến ngày 24/5/2027; kết thúc năm học trước ngày 31/5/2027). Tựu trường sớm nhất đối với học sinh lớp 9 từ ngày 21/8/2026 và học sinh lớp 6 từ ngày 28/8/2026.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phải xây dựng Kế hoạch dạy học (phân phối chương trình môn Toán và môn Tin học) khớp đúng khung 35 tuần, tuyệt đối không cắt xén hoặc dồn ghép cơ học; tính toán tuần đệm kiểm tra giữa kỳ (tuần 9) và cuối kỳ (tuần 17-18) khoa học, tránh dồn ép điểm số; giáo viên chủ nhiệm khối 6 và khối 9 chủ động ổn định sĩ số, nề nếp học tập ngay từ những ngày tựu trường sớm.", indent=True)
    
    # 2. Hướng dẫn nhiệm vụ năm học GDPT (Công văn 4200/SGDĐT-GDPT&GDTX)
    add_paragraph_styled(doc, "**2. Hướng dẫn thực hiện nhiệm vụ giáo dục phổ thông năm học 2026 – 2027 (Công văn số 4200/SGDĐT-GDPT&GDTX ngày 21/8/2026 của Sở GD&ĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Năm học 2026 – 2027 thực hiện toàn diện Chương trình GDPT 2018 cho cả 4 khối lớp (6, 7, 8, 9). Nhiệm vụ trọng tâm gồm: Đổi mới phương pháp dạy học chuyển từ truyền thụ kiến thức sang phát triển năng lực, phẩm chất học sinh; đẩy mạnh giáo dục STEM/STEAM và tăng cường bài học gắn với giải quyết vấn đề thực tiễn; đổi mới kiểm tra, đánh giá thường xuyên và định kỳ theo Thông tư 22/2021/TT-BGDĐT; đẩy mạnh ứng dụng công nghệ thông tin và chuyển đổi số trong quản lý, dạy học.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ Toán – Tin học giữ vai trò nòng cốt trong nhà trường, cần tiên phong thiết kế Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH gắn với thực tế đời sống; rà soát chuẩn hóa ngân hàng câu hỏi, ma trận và bản đặc tả đề kiểm tra định kỳ (không ra đề đánh đố, vượt cấp); xây dựng Kế hoạch giáo dục STEM với tối thiểu 02 chủ đề STEM/học kỳ cho bộ môn Toán và Tin học.", indent=True)
    
    # 3. Quy định về Học bạ số (Thông tư số 70/2026/TT-BGDĐT)
    add_paragraph_styled(doc, "**3. Quy định về quản lý và sử dụng Học bạ số (Thông tư số 70/2026/TT-BGDĐT ngày 22/8/2026 của Bộ GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Bãi bỏ học bạ giấy truyền thống, áp dụng Học bạ số 100% trong toàn bộ các cơ sở giáo dục phổ thông trên nền tảng Cơ sở dữ liệu ngành; Học bạ số có đầy đủ giá trị pháp lý chính thức tương đương học bạ giấy, được ký số điện tử bởi giáo viên bộ môn, giáo viên chủ nhiệm và người đứng đầu cơ sở giáo dục (Hiệu trưởng); liên thông dữ liệu phục vụ tuyển sinh đầu cấp và thi vào lớp 10.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** 100% giáo viên trong tổ (kể cả giáo viên bộ môn và GVCN) bắt buộc phải có chứng thư số cá nhân hợp lệ và thành thạo thao tác ký số; giáo viên có trách nhiệm cập nhật điểm kiểm tra, nhận xét học sinh định kỳ chính xác, đúng hạn trên phần mềm; bảo mật tuyệt đối tài khoản chữ ký số cá nhân, tuyệt đối không nhờ người khác ký hộ; hoàn thành ký số đúng tiến độ quy định, không để chậm trễ làm ảnh hưởng đến tiến độ đồng bộ dữ liệu của toàn trường.", indent=True)
    
    # 4. Hướng dẫn giáo dục Trí tuệ nhân tạo - AI (Công văn 5588/BGDĐT-GDPT)
    add_paragraph_styled(doc, "**4. Hướng dẫn triển khai nội dung giáo dục Trí tuệ nhân tạo (AI) cấp phổ thông từ năm học 2026 – 2027 (Công văn số 5588/BGDĐT-GDPT ngày 19/8/2026 của Bộ GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Cấu trúc Khung giáo dục AI cốt lõi gồm 12 tiết/lớp/năm học, áp dụng 3 hình thức triển khai linh hoạt: (1) Thực hiện chuyên đề giáo dục AI trong kế hoạch 2 buổi/ngày; (2) Lồng ghép tích hợp vào môn Tin học và các môn học khác (Toán, KHTN...); (3) Tổ chức qua câu lạc bộ, hoạt động ngoại khóa tự nguyện; bảo đảm không gây quá tải học tập, không làm biến đổi yêu cầu cần đạt của môn học.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Môn Tin học là lực lượng chủ công triển khai các nội dung cốt lõi về hiểu biết AI, kỹ năng sử dụng AI an toàn; môn Toán chủ động lựa chọn các bài học phù hợp để tích hợp công cụ AI và mô phỏng số hỗ trợ giải toán; tổ chuyên môn ghi rõ địa chỉ bài học tích hợp trong Kế hoạch giáo dục của tổ (Phụ lục 3) và Kế hoạch bài dạy (Phụ lục 4); chuẩn bị xây dựng bài dạy minh họa chuyên đề AI cấp trường và cấp cụm trường.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ CÔNG TÁC CHUẨN BỊ NĂM HỌC MỚI TRONG THÁNG 8/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm các khối lớp đã nhận lớp, nhanh chóng ổn định tổ chức nề nếp lớp học, lập nhóm Zalo kết nối thường xuyên với phụ huynh học sinh.", indent=True)
    add_paragraph_styled(doc, "- Đã hoàn thành thông báo danh mục sách giáo khoa bộ sách Cánh Diều cho cha mẹ học sinh chuẩn bị đầy đủ cho con em; rà soát, hoàn thành danh sách học sinh có hoàn cảnh khó khăn đề nghị nhà trường và địa phương hỗ trợ học bổng, sách giáo khoa đầu năm.", indent=True)
    
    add_section_h2(doc, "2. Kỷ luật lao động và ngày giờ công:")
    add_paragraph_styled(doc, "- Toàn thể 10/10 giáo viên trong tổ chấp hành nghiêm túc quy định ngày giờ công, tham gia đầy đủ các buổi tập trung chuẩn bị năm học của nhà trường và các đợt học tập chính trị hè 2026; đeo thẻ công chức/viên chức theo quy chế.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- Các nhóm bộ môn đã tham gia đầy đủ, nghiêm túc các đợt tập huấn chuyên môn do Sở GD&ĐT tổ chức: Tập huấn SGK lớp 9 mới, chuỗi tập huấn Năng lực số, Giáo dục Trí tuệ nhân tạo (AI), Giáo dục STEM và phương pháp dạy học trên nền tảng trực tuyến OLM theo đúng tiến độ.", indent=True)
    add_paragraph_styled(doc, "- Quy mô biên chế trường năm học 2026 – 2027 gồm **25 lớp** (Khối 6: 6 lớp; Khối 7: 6 lớp; Khối 8: 6 lớp; Khối 9: 7 lớp).", indent=True)
    add_paragraph_styled(doc, "- Tổ chuyên môn đã dự kiến phân công nhiệm vụ giảng dạy và công tác kiêm nhiệm Học kỳ I năm học 2026 – 2027 cho 10 giáo viên như sau:", indent=True)
    
    # Chèn bảng phân công chuyên môn
    add_table_phan_cong_thang_8(doc)
    
    add_paragraph_styled(doc, "- Các nhóm chuyên môn theo khối lớp đã thống nhất chương trình làm việc, thiết lập nhóm Zalo chuyên môn để trao đổi tài liệu, rà soát phân phối chương trình môn học.", indent=True)
    add_paragraph_styled(doc, "- Các đồng chí nhận lớp chủ nhiệm đã hoàn thành phiếu điều tra cơ bản đầu năm đúng hạn (Cô Nguyễn Thị Thảo lớp 6/2, Cô Lê Thị Bình lớp 7/1, Thầy Trần Long Hải lớp 8/3, Thầy Trần Sáng lớp 9/7).", indent=True)
    
    add_section_h2(doc, "4. Đánh giá thi đua tháng 8/2026:")
    add_paragraph_styled(doc, "- **Đánh giá chung:** Toàn thể thành viên trong tổ nêu cao tinh thần trách nhiệm, thực hiện nghiêm túc, kịp thời mọi kế hoạch của nhà trường, chuẩn bị chu đáo điều kiện cơ sở vật chất và chuyên môn cho ngày khai giảng.", indent=True)
    add_paragraph_styled(doc, "- **Xếp loại thi đua:** 10/10 đồng chí xếp loại A (Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng).", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. KẾ HOẠCH TRỌNG TÂM THÁNG 9/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Ổn định nề nếp lớp chủ nhiệm ngay từ tuần học đầu tiên; tích cực duy trì sinh hoạt 15 phút đầu giờ trước buổi học; hướng dẫn học sinh học tập nội quy, bình bầu ban cán sự lớp.", indent=True)
    add_paragraph_styled(doc, "- Tham gia lao động vệ sinh phong quang trường lớp, tập dượt nghi thức chuẩn bị lễ khai giảng năm học mới vào ngày 05/9/2026; quản lý tốt học sinh trong ngày khai giảng.", indent=True)
    
    add_section_h2(doc, "2. Kỷ luật ngày giờ công:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ phấn đấu bảo đảm ngày giờ công, chấp hành nghiêm túc thời khóa biểu chính thức bắt đầu từ ngày 07/9/2026.", indent=True)
    add_paragraph_styled(doc, "- Thực hiện đúng quy định dạy thay, dạy bù khi đồng nghiệp đi công tác hoặc ốm đau; không tự ý đổi giờ khi chưa báo cáo Ban Giám hiệu và Tổ trưởng.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- Nhóm bộ môn họp thống nhất kế hoạch dạy học, hoàn thiện các phụ lục theo Công văn 5512/BGDĐT-GDTrH (Phụ lục 1, Phụ lục 2, Phụ lục 3) và Kế hoạch kiểm tra đánh giá nộp về nhà trường phê duyệt chậm nhất ngày 10/9/2026.", indent=True)
    add_paragraph_styled(doc, "- Toàn thể giáo viên bộ môn: Cập nhật địa chỉ lồng ghép **Khung Năng lực số (20%)** và **12 tiết Khung AI** vào Kế hoạch bài dạy (Phụ lục 4); chuẩn bị giáo án đầy đủ trước khi lên lớp, đồng bộ lên Cơ sở dữ liệu ngành để ký số tuần đúng hạn.", indent=True)
    add_paragraph_styled(doc, "- Giáo viên đăng ký mượn đồ dùng dạy học, thiết bị thực hành, sách giáo khoa và sách tham khảo phục vụ giảng dạy tại phòng thiết bị - thư viện.", indent=True)
    add_paragraph_styled(doc, "- Khai thác có hiệu quả phòng máy vi tính và phòng học chức năng, bảo đảm an toàn điện và phòng cháy chữa cháy trong quá trình sử dụng.", indent=True)
    
    add_section_h2(doc, "4. Ngoại khóa và các hoạt động khác:")
    add_paragraph_styled(doc, "- Tập trung chuẩn bị cho lễ khai giảng ngày 05/9/2026 (phân công đọc quyết tâm thư, quản lý học sinh theo phân công của nhà trường).", indent=True)
    add_paragraph_styled(doc, "- Tham gia tuyên truyền học sinh chấp hành tốt luật An toàn giao thông (đặc biệt đội mũ bảo hiểm khi ngồi trên xe máy, xe đạp điện), phòng chống bạo lực học đường; tham gia các phong trào thi đua do Nhà trường và Đội TNTP phát động.", indent=True)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. THẢO LUẬN CHUYÊN MÔN VÀ Ý KIẾN CỦA CÁC THÀNH VIÊN TRONG TỔ")
    add_paragraph_styled(doc, "Cuộc họp đã dành phần lớn thời gian để các thầy cô đi thẳng vào các vấn đề chuyên môn cốt lõi, trao đổi thẳng thắn về các khó khăn thực tế khi đứng lớp và thống nhất phương án giải quyết cho năm học mới 2026 – 2027:", indent=True)
    
    # Ý kiến 1: Thảo luận về Chương trình Toán 9 mới và đề thi tuyển sinh 10
    add_paragraph_styled(doc, "**1. Thảo luận về Chương trình môn Toán 9 mới (năm đầu áp dụng GDPT 2018) và định hướng thi vào lớp 10:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Trần Sáng (Tổ phó chuyên môn, phụ trách Toán 9):** Năm học này là năm bản lề khi khối 9 bắt đầu học SGK mới theo Chương trình GDPT 2018. Khung kiến thức có sự thay đổi rất lớn: hệ thức lượng trong tam giác vuông, đường tròn, hàm số bậc nhất, bậc hai và đặc biệt là các bài toán thống kê - xác suất thực tế chiếm tỉ trọng điểm số đáng kể. Kỳ thi tuyển sinh vào lớp 10 tới đây chắc chắn sẽ ra đề theo cấu trúc ma trận mới 100%. Nếu giáo viên chỉ dạy lý thuyết sách giáo khoa theo lối mòn cũ thì học sinh sẽ rất lúng túng khi gặp bài toán thực tế (bài toán thực tế về đo đạc hình học, bài toán kinh tế, bài toán tối ưu...). Đề nghị nhóm Toán 9 ngay trong tháng 9 phải ngồi lại biên soạn một bộ chuyên đề bài tập thực tế chuẩn hóa theo từng chương để giáo viên dùng chung cho cả 7 lớp khối 9, bảo đảm tính đồng bộ và chất lượng đại trà.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hồ Đăng Danh (GV môn Toán 9):** Hoàn toàn nhất trí với ý kiến của thầy Sáng. Cần đặc biệt lưu ý về độ phân hóa giữa 7 lớp khối 9: lớp 9/7 học sinh tiếp thu rất nhanh, nhưng một số lớp khác học sinh còn hổng nhiều kiến thức đại số lớp 8. Do đó, trong Kế hoạch bài dạy, phần bài tập luyện tập phải thiết kế phân tầng rõ rệt: từ mức độ nhận biết, thông hiểu đến vận dụng thực tế; không nên áp dụng bài tập quá sức ngay từ đầu khiến học sinh có học lực trung bình, yếu bị nản chí.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Tấn Thiên (Chủ trì / Tổ trưởng):** Kết luận và thống nhất: Giao Thầy Trần Sáng làm trưởng nhóm Toán 9, chủ trì cùng Thầy Hồ Đăng Danh rà soát khung ma trận đề kiểm tra định kỳ và biên soạn ngân hàng bài tập thực tế khối 9. Tổ chuyên môn sẽ bố trí một buổi sinh hoạt chuyên môn chuyên đề vào tuần 3 tháng 9 để toàn tổ thẩm định và đóng góp ý kiến trước khi đưa vào giảng dạy chính thức.", indent=True)
    
    # Ý kiến 2: Thảo luận về tích hợp 12 tiết AI và Khung NLS (20%)
    add_paragraph_styled(doc, "**2. Thảo luận về phương pháp tích hợp 12 tiết Khung AI và Khung Năng lực số (20%) vào KHBD:**", indent=True)
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (GV môn Toán khối 7):** Giáo viên trong tổ đều ủng hộ chủ trương tích hợp AI và Năng lực số, nhưng băn khoăn lớn nhất là việc tích hợp cụ thể như thế nào trong tiến trình 4 hoạt động của Công văn 5512/BGDĐT-GDTrH để không làm loãng kiến thức trọng tâm bài Toán. Thời lượng 1 tiết chỉ có 45 phút, nếu đưa quá nhiều thuật ngữ AI hay công nghệ vào bài giảng thì học sinh sẽ không còn thời gian để rèn kỹ năng tính toán và lập luận hình học.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (GV môn Tin học):** Về phía môn Tin học, việc tích hợp 12 tiết AI rất thuận lợi vì chương trình Tin học có sẵn các mạch kiến thức về dữ liệu, thuật toán và đạo đức số. Nhóm Tin học (thầy Tùng, thầy Danh, cô Thảo) sẽ chủ động gánh vác phần lớn các bài học AI lý thuyết và kỹ năng sử dụng công cụ AI an toàn. Đối với môn Toán, việc tích hợp chỉ nên dừng lại ở mức độ công cụ trực quan (ví dụ: dùng phần mềm GeoGebra để vẽ hình động, dùng AI gợi ý hướng giải hoặc kiểm tra nghiệm), tuyệt đối không dạy kỹ thuật AI chuyên sâu trong giờ Toán làm quá tải học sinh.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Tấn Thiên (Tổ trưởng):** Thống nhất quan điểm: Tích hợp AI vào môn Toán phải thực chất, nhẹ nhàng và tự nhiên. Trong Kế hoạch bài dạy (Phụ lục 4), giáo viên chỉ cần in đậm, in nghiêng mục tiêu AI/NLS tại Hoạt động Luyện tập hoặc Vận dụng. Giao nhóm Tin học phối hợp cùng Thầy Sáng và Cô Bình soạn 01 giáo án mẫu tích hợp AI môn Toán lớp 8 và lớp 9 để gửi vào nhóm Zalo tổ cho cả tổ tham khảo trước ngày 10/9.", indent=True)
    
    # Ý kiến 3: Thảo luận về Cơ sở vật chất phòng máy vi tính môn Tin học
    add_paragraph_styled(doc, "**3. Thảo luận về cơ sở vật chất phòng máy vi tính và thiết bị thực hành môn Tin học:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (Phụ trách phòng máy vi tính):** Báo cáo hiện trạng: Nhà trường có 02 phòng máy vi tính (phòng 1 có 32 máy, phòng 2 có 30 máy). Qua rà soát kỹ thuật đầu năm, hiện có 6 máy tính bị hỏng chuột, 4 máy nguồn chập chờn và đường truyền mạng internet ở phòng 2 đôi lúc bị nghẽn khi học sinh cùng đăng nhập. Trong khi năm học này môn Tin học có tổng cộng 25 lớp, tần suất sử dụng phòng máy là liên tục cả sáng và chiều.", indent=True)
    add_paragraph_styled(doc, "- **Cô Nguyễn Thị Thảo (GV môn Tin học):** Nếu phòng máy thiếu máy tính hoạt động tốt thì học sinh phải ngồi ghép 2 đến 3 em một máy, rất khó quản lý nề nếp và hiệu quả thực hành lập trình Scratch (khối 6, 7) và Python (khối 8, 9) sẽ giảm sút rõ rệt. Đề nghị Tổ trưởng kiến nghị Ban Giám hiệu mua bổ sung chuột, bàn phím dự phòng và cấu hình lại mạng nội bộ trước ngày 05/9.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Đinh Văn Đông (Hiệu trưởng):** Tiếp thu ý kiến xác đáng của thầy Tùng và cô Thảo. Nhà trường đã phê duyệt kinh phí bảo dưỡng thiết bị dạy học đầu năm. Giao bộ phận thiết bị phối hợp với thầy Tùng hoàn thành việc kiểm tra, thay thế linh kiện hư hỏng và sửa chữa dứt điểm đường truyền internet phòng máy xong trước ngày 02/9 để đảm bảo ngày 07/9 học sinh vào học thực hành thuận lợi.", indent=True)
    
    # Ý kiến 4: Thảo luận về Triển khai Học bạ số và chữ ký số giáo viên (Thông tư 70)
    add_paragraph_styled(doc, "**4. Thảo luận về triển khai Học bạ số và chữ ký số giáo viên (Thông tư số 70/2026/TT-BGDĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh (GV môn Toán):** Việc triển khai Học bạ số thay cho học bạ giấy là bước tiến lớn, giúp giảm bớt áp lực ghi chép thủ công. Tuy nhiên, một số thầy cô còn lúng túng trong thao tác cài đặt chứng thư số trên điện thoại thông minh (SmartCA / VNPT CA), việc xác thực ký số điện tử và quy trình kiểm tra dữ liệu điểm số trước khi ký để tránh sai lệch.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hồ Đăng Danh (GV Tin học, CSDL ngành):** Đề xuất nhóm Tin học sẽ hỗ trợ kỹ thuật trực tiếp cho từng thầy cô trong tổ, hướng dẫn cài đặt app, kích hoạt chứng thư số và tổ chức một buổi thao tác ký số thử nghiệm trên hệ thống Cơ sở dữ liệu ngành vào đầu tháng 9.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Đinh Văn Đông (Hiệu trưởng):** Quán triệt nghiêm túc: Học bạ số là hồ sơ pháp lý liên thông quốc gia, giáo viên phải quản lý tài khoản ký số cá nhân như con dấu của mình, tuyệt đối không chia sẻ mật khẩu hay nhờ người khác ký hộ. Điểm số khi đã ký số sẽ khóa dữ liệu, sửa chữa rất phức tạp. Yêu cầu toàn thể giáo viên trong tổ nêu cao tinh thần trách nhiệm, vào điểm đúng hạn và kiểm tra thật kỹ trước khi ký số.", indent=True)
    
    # Ý kiến 5: Thảo luận về Giải pháp phụ đạo học sinh yếu kém và công tác chủ nhiệm đầu năm
    add_paragraph_styled(doc, "**5. Thảo luận về giải pháp phụ đạo học sinh yếu kém môn Toán và nề nếp chủ nhiệm:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Nguyễn Văn Tính (GV môn Toán khối 6 & 7):** Học sinh lớp 6 mới chuyển cấp từ tiểu học lên còn bỡ ngỡ về phương pháp học THCS; kỹ năng trình bày bài toán có lời văn và kỹ năng tính toán phân số, số thập phân còn nhiều hạn chế. Giáo viên dạy khối 6 cần kiên nhẫn, rèn phương pháp ghi chép và cách lập luận chuẩn mực ngay từ những tuần đầu tiên.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Trần Long Hải (GV môn Toán, GVCN lớp 8/3):** Đồng ý với thầy Tính. Đối với học sinh khối 8 và khối 9, ngay trong tháng 9 giáo viên bộ môn cần phối hợp chặt chẽ với giáo viên chủ nhiệm rà soát, lập danh sách học sinh có nguy cơ mất gốc kiến thức để có kế hoạch kèm cặp, phân công bạn học khá giúp đỡ bạn yếu trong 15 phút đầu giờ hoặc giao thêm bài tập vừa sức.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh (GV môn Toán):** Lưu ý thêm về công tác an toàn giao thông đầu năm: Đề nghị các giáo viên chủ nhiệm (đặc biệt khối 8, khối 9) phối hợp chặt chẽ với Tổng phụ trách Đội và phụ huynh nhắc nhở học sinh nghiêm túc đội mũ bảo hiểm khi đi xe đạp điện, xe máy điện tới trường.", indent=True)
    
    # ==================== PHẦN V ====================
    add_section_h1(doc, "V. KẾT LUẬN VÀ BIỂU QUYẾT")
    add_paragraph_styled(doc, "- Thầy Tổ trưởng Hoàng Tấn Thiên tổng hợp các ý kiến thảo luận và kết luận: Toàn thể giáo viên trong tổ phát huy tinh thần đoàn kết, trách nhiệm, tập trung hoàn thiện Kế hoạch bài dạy theo chuẩn CV 5512, tích hợp hiệu quả Khung AI và Năng lực số, chủ động hỗ trợ học sinh và chuẩn bị tốt nhất cho năm học mới 2026 – 2027.", indent=True)
    add_paragraph_styled(doc, "- **Biểu quyết:** 10/10 thành viên có mặt tán thành 100% với các nội dung đánh giá công tác tháng 8/2026, kế hoạch hoạt động tháng 9/2026 và các giải pháp chuyên môn đã thống nhất.", indent=True)
    add_paragraph_styled(doc, "Biên bản cuộc họp kết thúc vào lúc 11 giờ 30 phút cùng ngày, đã được đọc lại cho toàn thể các thành viên cùng nghe, nhất trí thông qua và ký xác nhận dưới đây; biên bản được lập thành 02 bản có giá trị như nhau, lưu hồ sơ tổ chuyên môn và gửi Ban Giám hiệu nhà trường./.", indent=True)
    
    # 5. Khung chữ ký chuẩn
    add_bien_ban_signatures(doc, chu_tri="Hoàng Tấn Thiên", thu_ky="Lê Thị Bình")
    
    # 6. Danh sách các thành viên khác của tổ ký xác nhận
    p_tv = doc.add_paragraph()
    p_tv.paragraph_format.space_before = Pt(12)
    p_tv.paragraph_format.space_after = Pt(4)
    r_tv = p_tv.add_run("CÁC THÀNH VIÊN KHÁC CỦA TỔ CHUYÊN MÔN KÝ XÁC NHẬN:\n")
    r_tv.font.name = 'Times New Roman'
    r_tv.font.size = Pt(13)
    r_tv.bold = True
    
    # Bảng 4 cột thành viên ký xác nhận
    table_tv = doc.add_table(rows=2, cols=4)
    table_tv.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_tv.autofit = False
    
    # Bỏ viền bảng chữ ký
    for r in table_tv.rows:
        for c in r.cells:
            tcPr = c._tc.get_or_add_tcPr()
            tcBorders = parse_xml(r'<w:tcBorders {}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>'.format(nsdecls('w')))
            tcPr.append(tcBorders)
            
    members_r1 = ["Đinh Văn Đông", "Trần Sáng", "Hồ Đăng Danh", "Hoàng Xuân Ánh"]
    members_r2 = ["Trần Long Hải", "Nguyễn Thị Thảo", "Nguyễn Văn Tính", "Dương Quang Tùng"]
    
    for i, name in enumerate(members_r1):
        cell = table_tv.rows[0].cells[i]
        cell.width = Inches(1.7)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(25)
        r = p.add_run(f"(Ký tên)\n\n\n**{name}**")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    for i, name in enumerate(members_r2):
        cell = table_tv.rows[1].cells[i]
        cell.width = Inches(1.7)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(25)
        r = p.add_run(f"(Ký tên)\n\n\n**{name}**")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    save_docx_robust(doc, out_docx_path)
    print(f"Da xuat thanh cong file Word: {out_docx_path}")
    
    if out_md_path:
        os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
        tao_bien_ban_hop_to_lan_1_thang_8_md(out_md_path)
        print(f"Da xuat thanh cong file Markdown: {out_md_path}")

def tao_bien_ban_hop_to_lan_1_thang_8_md(out_md_path):
    """Xuất phiên bản Markdown cho Biên bản họp tổ Lần 1 Tháng 8/2026."""
    md_content = """<div align="center">

| **TRƯỜNG THCS TRẦN PHÚ**<br>**TỔ TOÁN - TIN HỌC**<br>Số: 01/BB-TCM | **CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM**<br>**Độc lập – Tự do – Hạnh phúc**<br>──────────────────<br>*Xuân Đông, ngày 26 tháng 8 năm 2026* |
|:---:|:---:|

---

# BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1
### SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 8/2026
*(Chuẩn bị năm học mới 2026 – 2027)*
──────────────────

</div>

Hôm nay, vào lúc 10 giờ 00 phút, ngày 26 tháng 8 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 8 chuẩn bị cho năm học mới 2026 – 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.  
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.  
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).  
  + *Danh sách thành viên:* Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

<div align="center">

### NỘI DUNG CUỘC HỌP

</div>

## I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN

Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt các văn bản chỉ đạo trọng tâm của Bộ Giáo dục và Đào tạo, UBND thành phố Đồng Nai và Sở Giáo dục và Đào tạo; đồng thời tóm tắt các vấn đề cốt lõi tác động trực tiếp đến kế hoạch thực hiện của nhà trường và Tổ chuyên môn Toán – Tin học như sau:

**1. Kế hoạch thời gian năm học 2026 – 2027 (Quyết định số 2308/QĐ-BGDĐT ngày 06/8/2026 của Bộ GD&ĐT và Quyết định số 2322/QĐ-UBND ngày 19/8/2026 của UBND thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Toàn quốc và thành phố thống nhất tổ chức Khai giảng năm học mới vào ngày 05/9/2026. Khung kế hoạch bảo đảm đủ 35 tuần thực học (Học kỳ I: 18 tuần, từ ngày 07/9/2026 đến ngày 16/01/2027; Học kỳ II: 17 tuần, từ ngày 18/01/2027 đến ngày 24/5/2027; kết thúc năm học trước ngày 31/5/2027). Tựu trường sớm nhất đối với học sinh lớp 9 từ ngày 21/8/2026 và học sinh lớp 6 từ ngày 28/8/2026.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phải xây dựng Kế hoạch dạy học (phân phối chương trình môn Toán và môn Tin học) khớp đúng khung 35 tuần, tuyệt đối không cắt xén hoặc dồn ghép cơ học; tính toán tuần đệm kiểm tra giữa kỳ (tuần 9) và cuối kỳ (tuần 17-18) khoa học, tránh dồn ép điểm số; giáo viên chủ nhiệm khối 6 và khối 9 chủ động ổn định sĩ số, nề nếp học tập ngay từ những ngày tựu trường sớm.

**2. Hướng dẫn thực hiện nhiệm vụ giáo dục phổ thông năm học 2026 – 2027 (Công văn số 4200/SGDĐT-GDPT&GDTX ngày 21/8/2026 của Sở GD&ĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Năm học 2026 – 2027 thực hiện toàn diện Chương trình GDPT 2018 cho cả 4 khối lớp (6, 7, 8, 9). Nhiệm vụ trọng tâm gồm: Đổi mới phương pháp dạy học chuyển từ truyền thụ kiến thức sang phát triển năng lực, phẩm chất học sinh; đẩy mạnh giáo dục STEM/STEAM và tăng cường bài học gắn với giải quyết vấn đề thực tiễn; đổi mới kiểm tra, đánh giá thường xuyên và định kỳ theo Thông tư 22/2021/TT-BGDĐT; đẩy mạnh ứng dụng công nghệ thông tin và chuyển đổi số trong quản lý, dạy học.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ Toán – Tin học giữ vai trò nòng cốt trong nhà trường, cần tiên phong thiết kế Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH gắn với thực tế đời sống; rà soát chuẩn hóa ngân hàng câu hỏi, ma trận và bản đặc tả đề kiểm tra định kỳ (không ra đề đánh đố, vượt cấp); xây dựng Kế hoạch giáo dục STEM với tối thiểu 02 chủ đề STEM/học kỳ cho bộ môn Toán và Tin học.

**3. Quy định về quản lý và sử dụng Học bạ số (Thông tư số 70/2026/TT-BGDĐT ngày 22/8/2026 của Bộ GD&ĐT):**
- **Ý chính cốt lõi:** Bãi bỏ học bạ giấy truyền thống, áp dụng Học bạ số 100% trong toàn bộ các cơ sở giáo dục phổ thông trên nền tảng Cơ sở dữ liệu ngành; Học bạ số có đầy đủ giá trị pháp lý chính thức tương đương học bạ giấy, được ký số điện tử bởi giáo viên bộ môn, giáo viên chủ nhiệm và người đứng đầu cơ sở giáo dục (Hiệu trưởng); liên thông dữ liệu phục vụ tuyển sinh đầu cấp và thi vào lớp 10.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** 100% giáo viên trong tổ (kể cả giáo viên bộ môn và GVCN) bắt buộc phải có chứng thư số cá nhân hợp lệ và thành thạo thao tác ký số; giáo viên có trách nhiệm cập nhật điểm kiểm tra, nhận xét học sinh định kỳ chính xác, đúng hạn trên phần mềm; bảo mật tuyệt đối tài khoản chữ ký số cá nhân, tuyệt đối không nhờ người khác ký hộ; hoàn thành ký số đúng tiến độ quy định, không để chậm trễ làm ảnh hưởng đến tiến độ đồng bộ dữ liệu của toàn trường.

**4. Hướng dẫn triển khai nội dung giáo dục Trí tuệ nhân tạo (AI) cấp phổ thông từ năm học 2026 – 2027 (Công văn số 5588/BGDĐT-GDPT ngày 19/8/2026 của Bộ GD&ĐT):**
- **Ý chính cốt lõi:** Cấu trúc Khung giáo dục AI cốt lõi gồm 12 tiết/lớp/năm học, áp dụng 3 hình thức triển khai linh hoạt: (1) Thực hiện chuyên đề giáo dục AI trong kế hoạch 2 buổi/ngày; (2) Lồng ghép tích hợp vào môn Tin học và các môn học khác (Toán, KHTN...); (3) Tổ chức qua câu lạc bộ, hoạt động ngoại khóa tự nguyện; bảo đảm không gây quá tải học tập, không làm biến đổi yêu cầu cần đạt của môn học.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Môn Tin học là lực lượng chủ công triển khai các nội dung cốt lõi về hiểu biết AI, kỹ năng sử dụng AI an toàn; môn Toán chủ động lựa chọn các bài học phù hợp để tích hợp công cụ AI và mô phỏng số hỗ trợ giải toán; tổ chuyên môn ghi rõ địa chỉ bài học tích hợp trong Kế hoạch giáo dục của tổ (Phụ lục 3) và Kế hoạch bài dạy (Phụ lục 4); chuẩn bị xây dựng bài dạy minh họa chuyên đề AI cấp trường và cấp cụm trường.

## II. ĐÁNH GIÁ CÔNG TÁC CHUẨN BỊ NĂM HỌC MỚI TRONG THÁNG 8/2026

### **1. Công tác chủ nhiệm:**
- Giáo viên chủ nhiệm các khối lớp đã nhận lớp, nhanh chóng ổn định tổ chức nề nếp lớp học, lập nhóm Zalo kết nối thường xuyên với phụ huynh học sinh.
- Đã hoàn thành thông báo danh mục sách giáo khoa bộ sách Cánh Diều cho cha mẹ học sinh chuẩn bị đầy đủ cho con em; rà soát, hoàn thành danh sách học sinh có hoàn cảnh khó khăn đề nghị nhà trường và địa phương hỗ trợ học bổng, sách giáo khoa đầu năm.

### **2. Kỷ luật lao động và ngày giờ công:**
- Toàn thể 10/10 giáo viên trong tổ chấp hành nghiêm túc quy định ngày giờ công, tham gia đầy đủ các buổi tập trung chuẩn bị năm học của nhà trường và các đợt học tập chính trị hè 2026; đeo thẻ công chức/viên chức theo quy chế.

### **3. Công tác chuyên môn:**
- Các nhóm bộ môn đã tham gia đầy đủ, nghiêm túc các đợt tập huấn chuyên môn do Sở GD&ĐT tổ chức: Tập huấn SGK lớp 9 mới, chuỗi tập huấn Năng lực số, Giáo dục Trí tuệ nhân tạo (AI), Giáo dục STEM và phương pháp dạy học trên nền tảng trực tuyến OLM theo đúng tiến độ.
- Quy mô biên chế trường năm học 2026 – 2027 gồm **25 lớp** (Khối 6: 6 lớp; Khối 7: 6 lớp; Khối 8: 6 lớp; Khối 9: 7 lớp).
- Tổ chuyên môn đã dự kiến phân công nhiệm vụ giảng dạy và công tác kiêm nhiệm Học kỳ I năm học 2026 – 2027 cho 10 giáo viên như sau:

| STT | Họ và tên giáo viên | Môn và lớp phụ trách giảng dạy | Nhiệm vụ kiêm nhiệm / khác | Số tiết/tuần | Ghi chú |
|:---:|:---|:---|:---|:---:|:---:|
| 1 | Hoàng Tấn Thiên | Toán 6 (3 lớp - 12 tiết) | Tổ trưởng chuyên môn (3t), Phụ trách Chuyển đổi số (3t) | 18 | Tổ trưởng |
| 2 | Trần Sáng | Toán 9 (3 lớp - 12 tiết), Tin học 9 (1 lớp - 1 tiết) | Phó Tổ trưởng (1t), Chủ nhiệm lớp 9/7 (4t) | 18 | Phó Tổ trưởng |
| 3 | Đinh Văn Đông | Hoạt động TN, HN (3 tiết) | Hiệu trưởng nhà trường | 3 | BGH sinh hoạt tổ |
| 4 | Hồ Đăng Danh | Toán 9 (4 lớp - 16 tiết) | Thành viên ban CNTT & CSDL ngành | 16 | GV môn Toán |
| 5 | Hoàng Xuân Ánh | Toán 8 (3 lớp - 12 tiết), Tin học 6 (4 lớp - 4 tiết) | Ủy viên tổ chuyên môn | 16 | GV Toán - Tin |
| 6 | Trần Long Hải | Toán 8 (3 lớp - 12 tiết), HĐTN, HN (3 tiết) | Chủ nhiệm lớp 8/3 (4t) | 19 | GV môn Toán |
| 7 | Lê Thị Bình | Toán 7 (3 lớp - 12 tiết), HĐTN, HN (3 tiết) | Chủ nhiệm lớp 7/1 (4t), Thư ký tổ | 19 | GV môn Toán |
| 8 | Nguyễn Thị Thảo | Toán 6 (1 lớp - 4t), Toán 7 (1 lớp - 4t)<br>Tin 6 (2 lớp - 2t), Tin 7 (2 lớp - 2t), HĐTN (3t) | Chủ nhiệm lớp 6/2 (4t) | 19 | GV Toán - Tin |
| 9 | Nguyễn Văn Tính | Toán 6 (2 lớp - 8 tiết), Toán 7 (2 lớp - 8 tiết) | Ủy viên tổ chuyên môn | 16 | GV môn Toán |
| 10 | Dương Quang Tùng | Tin 7 (4 lớp - 4t), Tin 8 (6 lớp - 6t), Tin 9 (6 lớp - 6t) | Phụ trách phòng máy vi tính bộ môn (3t) | 19 | GV Tin học |

- Các nhóm chuyên môn theo khối lớp đã thống nhất chương trình làm việc, thiết lập nhóm Zalo chuyên môn để trao đổi tài liệu, rà soát phân phối chương trình môn học.
- Các đồng chí nhận lớp chủ nhiệm đã hoàn thành phiếu điều tra cơ bản đầu năm đúng hạn (Cô Nguyễn Thị Thảo lớp 6/2, Cô Lê Thị Bình lớp 7/1, Thầy Trần Long Hải lớp 8/3, Thầy Trần Sáng lớp 9/7).

### **4. Đánh giá thi đua tháng 8/2026:**
- **Đánh giá chung:** Toàn thể thành viên trong tổ nêu cao tinh thần trách nhiệm, thực hiện nghiêm túc, kịp thời mọi kế hoạch của nhà trường, chuẩn bị chu đáo điều kiện cơ sở vật chất và chuyên môn cho ngày khai giảng.
- **Xếp loại thi đua:** 10/10 đồng chí xếp loại A (Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng).

## III. KẾ HOẠCH TRỌNG TÂM THÁNG 9/2026

### **1. Công tác chủ nhiệm:**
- Ổn định nề nếp lớp chủ nhiệm ngay từ tuần học đầu tiên; tích cực duy trì sinh hoạt 15 phút đầu giờ trước buổi học; hướng dẫn học sinh học tập nội quy, bình bầu ban cán sự lớp.
- Tham gia lao động vệ sinh phong quang trường lớp, tập dượt nghi thức chuẩn bị lễ khai giảng năm học mới vào ngày 05/9/2026; quản lý tốt học sinh trong ngày khai giảng.

### **2. Kỷ luật ngày giờ công:**
- Giáo viên trong tổ phấn đấu bảo đảm ngày giờ công, chấp hành nghiêm túc thời khóa biểu chính thức bắt đầu từ ngày 07/9/2026.
- Thực hiện đúng quy định dạy thay, dạy bù khi đồng nghiệp đi công tác hoặc ốm đau; không tự ý đổi giờ khi chưa báo cáo Ban Giám hiệu và Tổ trưởng.

### **3. Công tác chuyên môn:**
- Nhóm bộ môn họp thống nhất kế hoạch dạy học, hoàn thiện các phụ lục theo Công văn 5512/BGDĐT-GDTrH (Phụ lục 1, Phụ lục 2, Phụ lục 3) và Kế hoạch kiểm tra đánh giá nộp về nhà trường phê duyệt chậm nhất ngày 10/9/2026.
- Toàn thể giáo viên bộ môn: Cập nhật địa chỉ lồng ghép **Khung Năng lực số (20%)** và **12 tiết Khung AI** vào Kế hoạch bài dạy (Phụ lục 4); chuẩn bị giáo án đầy đủ trước khi lên lớp, đồng bộ lên Cơ sở dữ liệu ngành để ký số tuần đúng hạn.
- Giáo viên đăng ký mượn đồ dùng dạy học, thiết bị thực hành, sách giáo khoa và sách tham khảo phục vụ giảng dạy tại phòng thiết bị - thư viện.
- Khai thác có hiệu quả phòng máy vi tính và phòng học chức năng, bảo đảm an toàn điện và phòng cháy chữa cháy trong quá trình sử dụng.

### **4. Ngoại khóa và các hoạt động khác:**
- Tập trung chuẩn bị cho lễ khai giảng ngày 05/9/2026 (phân công đọc quyết tâm thư, quản lý học sinh theo phân công của nhà trường).
- Tham gia tuyên truyền học sinh chấp hành tốt luật An toàn giao thông (đặc biệt đội mũ bảo hiểm khi ngồi trên xe máy, xe đạp điện), phòng chống bạo lực học đường; tham gia các phong trào thi đua do Nhà trường và Đội TNTP phát động.

## IV. THẢO LUẬN CHUYÊN MÔN VÀ Ý KIẾN CỦA CÁC THÀNH VIÊN TRONG TỔ

Cuộc họp đã dành phần lớn thời gian để các thầy cô đi thẳng vào các vấn đề chuyên môn cốt lõi, trao đổi thẳng thắn về các khó khăn thực tế khi đứng lớp và thống nhất phương án giải quyết cho năm học mới 2026 – 2027:

**1. Thảo luận về Chương trình môn Toán 9 mới (năm đầu áp dụng GDPT 2018) và định hướng thi vào lớp 10:**
- **Thầy Trần Sáng (Tổ phó chuyên môn, phụ trách Toán 9):** Năm học này là năm bản lề khi khối 9 bắt đầu học SGK mới theo Chương trình GDPT 2018. Khung kiến thức có sự thay đổi rất lớn: hệ thức lượng trong tam giác vuông, đường tròn, hàm số bậc nhất, bậc hai và đặc biệt là các bài toán thống kê - xác suất thực tế chiếm tỉ trọng điểm số đáng kể. Kỳ thi tuyển sinh vào lớp 10 tới đây chắc chắn sẽ ra đề theo cấu trúc ma trận mới 100%. Nếu giáo viên chỉ dạy lý thuyết sách giáo khoa theo lối mòn cũ thì học sinh sẽ rất lúng túng khi gặp bài toán thực tế (bài toán thực tế về đo đạc hình học, bài toán kinh tế, bài toán tối ưu...). Đề nghị nhóm Toán 9 ngay trong tháng 9 phải ngồi lại biên soạn một bộ chuyên đề bài tập thực tế chuẩn hóa theo từng chương để giáo viên dùng chung cho cả 7 lớp khối 9, bảo đảm tính đồng bộ và chất lượng đại trà.
- **Thầy Hồ Đăng Danh (GV môn Toán 9):** Hoàn toàn nhất trí với ý kiến của thầy Sáng. Cần đặc biệt lưu ý về độ phân hóa giữa 7 lớp khối 9: lớp 9/7 học sinh tiếp thu rất nhanh, nhưng một số lớp khác học sinh còn hổng nhiều kiến thức đại số lớp 8. Do đó, trong Kế hoạch bài dạy, phần bài tập luyện tập phải thiết kế phân tầng rõ rệt: từ mức độ nhận biết, thông hiểu đến vận dụng thực tế; không nên áp dụng bài tập quá sức ngay từ đầu khiến học sinh có học lực trung bình, yếu bị nản chí.
- **Thầy Hoàng Tấn Thiên (Chủ trì / Tổ trưởng):** Kết luận và thống nhất: Giao Thầy Trần Sáng làm trưởng nhóm Toán 9, chủ trì cùng Thầy Hồ Đăng Danh rà soát khung ma trận đề kiểm tra định kỳ và biên soạn ngân hàng bài tập thực tế khối 9. Tổ chuyên môn sẽ bố trí một buổi sinh hoạt chuyên môn chuyên đề vào tuần 3 tháng 9 để toàn tổ thẩm định và đóng góp ý kiến trước khi đưa vào giảng dạy chính thức.

**2. Thảo luận về phương pháp tích hợp 12 tiết Khung AI và Khung Năng lực số (20%) vào KHBD:**
- **Cô Lê Thị Bình (GV môn Toán khối 7):** Giáo viên trong tổ đều ủng hộ chủ trương tích hợp AI và Năng lực số, nhưng băn khoăn lớn nhất là việc tích hợp cụ thể như thế nào trong tiến trình 4 hoạt động của Công văn 5512/BGDĐT-GDTrH để không làm loãng kiến thức trọng tâm bài Toán. Thời lượng 1 tiết chỉ có 45 phút, nếu đưa quá nhiều thuật ngữ AI hay công nghệ vào bài giảng thì học sinh sẽ không còn thời gian để rèn kỹ năng tính toán và lập luận hình học.
- **Thầy Dương Quang Tùng (GV môn Tin học):** Về phía môn Tin học, việc tích hợp 12 tiết AI rất thuận lợi vì chương trình Tin học có sẵn các mạch kiến thức về dữ liệu, thuật toán và đạo đức số. Nhóm Tin học (thầy Tùng, thầy Danh, cô Thảo) sẽ chủ động gánh vác phần lớn các bài học AI lý thuyết và kỹ năng sử dụng công cụ AI an toàn. Đối với môn Toán, việc tích hợp chỉ nên dừng lại ở mức độ công cụ trực quan (ví dụ: dùng phần mềm GeoGebra để vẽ hình động, dùng AI gợi ý hướng giải hoặc kiểm tra nghiệm), tuyệt đối không dạy kỹ thuật AI chuyên sâu trong giờ Toán làm quá tải học sinh.
- **Thầy Hoàng Tấn Thiên (Tổ trưởng):** Thống nhất quan điểm: Tích hợp AI vào môn Toán phải thực chất, nhẹ nhàng và tự nhiên. Trong Kế hoạch bài dạy (Phụ lục 4), giáo viên chỉ cần in đậm, in nghiêng mục tiêu AI/NLS tại Hoạt động Luyện tập hoặc Vận dụng. Giao nhóm Tin học phối hợp cùng Thầy Sáng và Cô Bình soạn 01 giáo án mẫu tích hợp AI môn Toán lớp 8 và lớp 9 để gửi vào nhóm Zalo tổ cho cả tổ tham khảo trước ngày 10/9.

**3. Thảo luận về cơ sở vật chất phòng máy vi tính và thiết bị thực hành môn Tin học:**
- **Thầy Dương Quang Tùng (Phụ trách phòng máy vi tính):** Báo cáo hiện trạng: Nhà trường có 02 phòng máy vi tính (phòng 1 có 32 máy, phòng 2 có 30 máy). Qua rà soát kỹ thuật đầu năm, hiện có 6 máy tính bị hỏng chuột, 4 máy nguồn chập chờn và đường truyền mạng internet ở phòng 2 đôi lúc bị nghẽn khi học sinh cùng đăng nhập. Trong khi năm học này môn Tin học có tổng cộng 25 lớp, tần suất sử dụng phòng máy là liên tục cả sáng và chiều.
- **Cô Nguyễn Thị Thảo (GV môn Tin học):** Nếu phòng máy thiếu máy tính hoạt động tốt thì học sinh phải ngồi ghép 2 đến 3 em một máy, rất khó quản lý nề nếp và hiệu quả thực hành lập trình Scratch (khối 6, 7) và Python (khối 8, 9) sẽ giảm sút rõ rệt. Đề nghị Tổ trưởng kiến nghị Ban Giám hiệu mua bổ sung chuột, bàn phím dự phòng và cấu hình lại mạng nội bộ trước ngày 05/9.
- **Thầy Đinh Văn Đông (Hiệu trưởng):** Tiếp thu ý kiến xác đáng của thầy Tùng và cô Thảo. Nhà trường đã phê duyệt kinh phí bảo dưỡng thiết bị dạy học đầu năm. Giao bộ phận thiết bị phối hợp với thầy Tùng hoàn thành việc kiểm tra, thay thế linh kiện hư hỏng và sửa chữa dứt điểm đường truyền internet phòng máy xong trước ngày 02/9 để đảm bảo ngày 07/9 học sinh vào học thực hành thuận lợi.

**4. Thảo luận về triển khai Học bạ số và chữ ký số giáo viên (Thông tư số 70/2026/TT-BGDĐT):**
- **Thầy Hoàng Xuân Ánh (GV môn Toán):** Việc triển khai Học bạ số thay cho học bạ giấy là bước tiến lớn, giúp giảm bớt áp lực ghi chép thủ công. Tuy nhiên, một số thầy cô còn lúng túng trong thao tác cài đặt chứng thư số trên điện thoại thông minh (SmartCA / VNPT CA), việc xác thực ký số điện tử và quy trình kiểm tra dữ liệu điểm số trước khi ký để tránh sai lệch.
- **Thầy Hồ Đăng Danh (GV Tin học, CSDL ngành):** Đề xuất nhóm Tin học sẽ hỗ trợ kỹ thuật trực tiếp cho từng thầy cô trong tổ, hướng dẫn cài đặt app, kích hoạt chứng thư số và tổ chức một buổi thao tác ký số thử nghiệm trên hệ thống Cơ sở dữ liệu ngành vào đầu tháng 9.
- **Thầy Đinh Văn Đông (Hiệu trưởng):** Quán triệt nghiêm túc: Học bạ số là hồ sơ pháp lý liên thông quốc gia, giáo viên phải quản lý tài khoản ký số cá nhân như con dấu của mình, tuyệt đối không chia sẻ mật khẩu hay nhờ người khác ký hộ. Điểm số khi đã ký số sẽ khóa dữ liệu, sửa chữa rất phức tạp. Yêu cầu toàn thể giáo viên trong tổ nêu cao tinh thần trách nhiệm, vào điểm đúng hạn và kiểm tra thật kỹ trước khi ký số.

**5. Thảo luận về giải pháp phụ đạo học sinh yếu kém môn Toán và nề nếp chủ nhiệm:**
- **Thầy Nguyễn Văn Tính (GV môn Toán khối 6 & 7):** Học sinh lớp 6 mới chuyển cấp từ tiểu học lên còn bỡ ngỡ về phương pháp học THCS; kỹ năng trình bày bài toán có lời văn và kỹ năng tính toán phân số, số thập phân còn nhiều hạn chế. Giáo viên dạy khối 6 cần kiên nhẫn, rèn phương pháp ghi chép và cách lập luận chuẩn mực ngay từ những tuần đầu tiên.
- **Thầy Trần Long Hải (GV môn Toán, GVCN lớp 8/3):** Đồng ý với thầy Tính. Đối với học sinh khối 8 và khối 9, ngay trong tháng 9 giáo viên bộ môn cần phối hợp chặt chẽ với giáo viên chủ nhiệm rà soát, lập danh sách học sinh có nguy cơ mất gốc kiến thức để có kế hoạch kèm cặp, phân công bạn học khá giúp đỡ bạn yếu trong 15 phút đầu giờ hoặc giao thêm bài tập vừa sức.
- **Thầy Hoàng Xuân Ánh (GV môn Toán):** Lưu ý thêm về công tác an toàn giao thông đầu năm: Đề nghị các giáo viên chủ nhiệm (đặc biệt khối 8, khối 9) phối hợp chặt chẽ với Tổng phụ trách Đội và phụ huynh nhắc nhở học sinh nghiêm túc đội mũ bảo hiểm khi đi xe đạp điện, xe máy điện tới trường.

## V. KẾT LUẬN VÀ BIỂU QUYẾT

- Thầy Tổ trưởng Hoàng Tấn Thiên tổng hợp các ý kiến thảo luận và kết luận: Toàn thể giáo viên trong tổ phát huy tinh thần đoàn kết, trách nhiệm, tập trung hoàn thiện Kế hoạch bài dạy theo chuẩn CV 5512, tích hợp hiệu quả Khung AI và Năng lực số, chủ động hỗ trợ học sinh và chuẩn bị tốt nhất cho năm học mới 2026 – 2027.
- **Biểu quyết:** 10/10 thành viên có mặt tán thành 100% với các nội dung đánh giá công tác tháng 8/2026, kế hoạch hoạt động tháng 9/2026 và các giải pháp chuyên môn đã thống nhất.

Biên bản cuộc họp kết thúc vào lúc 11 giờ 30 phút cùng ngày, đã được đọc lại cho toàn thể các thành viên cùng nghe, nhất trí thông qua và ký xác nhận dưới đây; biên bản được lập thành 02 bản có giá trị như nhau, lưu hồ sơ tổ chuyên môn và gửi Ban Giám hiệu nhà trường./.

---

| **THƯ KÝ CUỘC HỌP**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Lê Thị Bình** | **TỔ TRƯỞNG CHUYÊN MÔN**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Hoàng Tấn Thiên** |
|:---:|:---:|

**CÁC THÀNH VIÊN KHÁC CỦA TỔ CHUYÊN MÔN KÝ XÁC NHẬN:**

| Đinh Văn Đông | Trần Sáng | Hồ Đăng Danh | Hoàng Xuân Ánh |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |

| Trần Long Hải | Nguyễn Thị Thảo | Nguyễn Văn Tính | Dương Quang Tùng |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


def tao_bien_ban_hop_to_lan_1_thang_9(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 1 Tháng 9/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # 1. Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="02/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 12 tháng 9 năm 2026"
    )
    
    # 2. Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1",
        "SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 9/2026 (LẦN 1)\nNăm học: 2026 - 2027"
    )
    
    # 3. Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 07 giờ 30 phút, ngày 12 tháng 9 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 9 năm học 2026 – 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # 4. NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt các văn bản chỉ đạo trọng tâm của Bộ Giáo dục và Đào tạo, Sở Giáo dục và Đào tạo và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:", indent=True)
    
    # 1. Công văn 5512/BGDĐT-GDTrH
    add_paragraph_styled(doc, "**1. Hướng dẫn xây dựng và tổ chức thực hiện kế hoạch giáo dục của nhà trường (Công văn số 5512/BGDĐT-GDTrH ngày 18/12/2020 của Bộ GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Quy định chuẩn hóa hệ thống hồ sơ kế hoạch giáo dục của tổ chuyên môn và giáo viên bao gồm: (1) **Phụ lục 1** – Khung kế hoạch dạy học môn học của tổ chuyên môn (phân phối chương trình 35 tuần, yêu cầu cần đạt, thiết bị dạy học, phòng học bộ môn); (2) **Phụ lục 2** – Khung kế hoạch tổ chức các hoạt động giáo dục của tổ chuyên môn (chuyên đề, chủ đề liên môn, bài học STEM); (3) **Phụ lục 3** – Khung kế hoạch giáo dục của giáo viên trong năm học (kế hoạch cá nhân theo phân công chuyên môn, chỉ tiêu, bồi dưỡng học sinh); (4) **Phụ lục 4** – Khung kế hoạch bài dạy (KHBD) cấu trúc 4 hoạt động: Mở đầu/Khởi động, Hình thành kiến thức mới, Luyện tập, Vận dụng.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Các nhóm bộ môn (Toán 6, 7, 8, 9; Tin học 6, 7, 8, 9) hoàn thiện Phụ lục 1, Phụ lục 2 và từng cá nhân hoàn thiện Phụ lục 3 nộp phê duyệt trên Cơ sở dữ liệu ngành chậm nhất ngày 30/9/2026; đặc biệt, bắt buộc tích hợp **Khung Năng lực số (20% số tiết)** và **12 tiết Khung AI** vào Phụ lục 1, Phụ lục 3 và thể hiện in đậm, in nghiêng rõ nét trong Kế hoạch bài dạy (Phụ lục 4) để phục vụ kiểm tra, duyệt giáo án ký số.", indent=True)
    
    # 2. Hội thi giáo dục phòng chống ma túy
    add_paragraph_styled(doc, "**2. Kế hoạch tham gia Hội thi giáo dục phòng, chống ma túy năm học 2026 – 2027 (Kế hoạch số 81/KH-THCS.TP ngày 11/9/2026 của Trường THCS Trần Phú và Kế hoạch số 4777/KH-SGDĐT của Sở GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Mỗi sản phẩm dự thi gồm 01 Kế hoạch bài dạy (hoặc Kế hoạch tổ chức hoạt động giáo dục) + 01 Bài giảng điện tử tương ứng bám sát chủ đề phòng, chống ma túy trong học đường; toàn bộ sản phẩm được số hóa, đóng gói dưới dung lượng 1GB; sản phẩm có tính nguyên gốc do chính giáo viên xây dựng; được phép sử dụng công cụ số/AI hỗ trợ thiết kế nhưng không dùng AI thay thế phần sáng tạo và chuyên môn của tác giả; hạn nộp cấp trường ngày 20/9/2026 và nộp về Sở GD&ĐT trước ngày 25/9/2026.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phân công **Thầy Trần Sáng** và **Cô Lê Thị Bình** trực tiếp biên soạn 02 sản phẩm đại diện tổ tham gia dự thi; Thầy Tổ trưởng theo dõi tiến độ, chủ trì phiên họp tổ góp ý chuyên môn và thẩm định sản phẩm trước khi nộp Ban Giám hiệu; các thành viên trong tổ hỗ trợ tư liệu, video học liệu và kỹ thuật công nghệ thông tin phục vụ đóng gói bài giảng điện tử.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ CÔNG TÁC GIAI ĐOẠN ĐẦU THÁNG 9/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm các khối lớp đã nhanh chóng ổn định tổ chức nề nếp lớp chủ nhiệm ngay từ ngày tựu trường; duy trì nghiêm túc sinh hoạt 15 phút đầu giờ trước buổi học; hoàn thành phổ biến nội quy trường lớp, kiện toàn ban cán sự lớp.", indent=True)
    add_paragraph_styled(doc, "- Đã lập danh sách học sinh có hoàn cảnh khó khăn đề nghị nhà trường trao quà, học bổng trong lễ khai giảng ngày 05/9/2026; cùng học sinh tham gia vệ sinh phong quang trường lớp chuẩn bị chu đáo cho ngày hội khai trường.", indent=True)
    
    add_section_h2(doc, "2. Kỷ luật lao động và ngày giờ công:")
    add_paragraph_styled(doc, "- 100% giáo viên trong tổ chấp hành nghiêm túc quy định ngày giờ công, tham gia đầy đủ lễ khai giảng năm học mới ngày 05/9/2026 và các buổi hội họp của nhà trường; giảng dạy đúng thời khóa biểu chính thức bắt đầu từ ngày 07/9/2026.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- Các nhóm bộ môn đã thống nhất cấu trúc soạn Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH; bắt đầu đưa giáo án lên Cơ sở dữ liệu ngành để ký số tuần.", indent=True)
    add_paragraph_styled(doc, "- Tổ chức dạy và học ổn định theo thời khóa biểu áp dụng từ 07/9/2026; thực hiện tốt kế hoạch dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT.", indent=True)
    add_paragraph_styled(doc, "- Tham gia đầy đủ các buổi tập huấn chuyên môn trực tuyến về chuyển đổi số, tập huấn dạy học và kiểm tra đánh giá trên nền tảng OLM.", indent=True)
    
    add_section_h2(doc, "4. Phòng bộ môn và thiết bị dạy học:")
    add_paragraph_styled(doc, "- Đã kiểm tra nề nếp ra vào lớp học, phòng máy vi tính bộ môn; rà soát thiết bị dạy học và cơ sở vật chất 02 phòng máy sau đợt bảo dưỡng đầu năm của nhà trường.", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. KẾ HOẠCH TRỌNG TÂM THỜI GIAN TỚI (THÁNG 9 & ĐẦU THÁNG 10/2026)")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Ổn định vững chắc nề nếp lớp chủ nhiệm, củng cố đội ngũ cán bộ lớp, tham gia họp GVCN; xây dựng Kế hoạch chủ nhiệm năm học 2026 – 2027.", indent=True)
    add_paragraph_styled(doc, "- Đẩy mạnh tuyên truyền thực hiện Tháng An toàn giao thông, tổ chức cho 100% học sinh ký cam kết đội mũ bảo hiểm khi đi xe máy điện, xe đạp điện; tuyên truyền phòng chống tệ nạn xã hội và dịch bệnh.", indent=True)
    add_paragraph_styled(doc, "- Cập nhật, rà soát hoàn thiện 100% thông tin học sinh lớp chủ nhiệm trên hệ thống Cơ sở dữ liệu ngành.", indent=True)
    add_paragraph_styled(doc, "- Chuẩn bị chu đáo nội dung họp cha mẹ học sinh đầu năm; giữ gìn sổ đầu bài cẩn thận, nhắc nhở giáo viên bộ môn ghi chép đầy đủ các cột mục và GVCN tổng hợp ký tuần.", indent=True)
    
    add_section_h2(doc, "2. Kỷ luật ngày giờ công:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ phấn đấu bảo đảm ngày giờ công, chấp hành nghiêm túc thời khóa biểu, không đi trễ về sớm; thực hiện nghiêm túc quy định dạy thay, dạy bù khi có giáo viên đi công tác hoặc ốm đau.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- **Hoàn thành các Phụ lục theo Công văn 5512:** Các nhóm bộ môn Toán, Tin học hoàn thiện Kế hoạch dạy học của tổ (Phụ lục 1), Kế hoạch tổ chức các hoạt động giáo dục (Phụ lục 2) và Kế hoạch giáo dục của giáo viên (Phụ lục 3), nộp phê duyệt trên CSDL ngành chậm nhất ngày 30/9/2026.", indent=True)
    add_paragraph_styled(doc, "- **Tham gia Hội thi giáo dục phòng, chống ma túy:** Thầy Sáng, Cô Bình hoàn thành KHBD và bài giảng điện tử trước 20/9 để tổ góp ý hoàn thiện, nộp Ban Giám hiệu xét chọn gửi Sở GD&ĐT trước 25/9.", indent=True)
    add_paragraph_styled(doc, "- **Phát động các phong trào thi trực tuyến:**", indent=True)
    add_paragraph_styled(doc, "  + *Đấu trường VioEdu môn Toán:* Phân công giáo viên phụ trách hướng dẫn học sinh đăng nhập và luyện tập: Khối 6 (Cô Thảo), Khối 7 (Thầy Ánh), Khối 8 (Cô Bình), Khối 9 (Thầy Sáng).", indent=True)
    add_paragraph_styled(doc, "  + *Cuộc thi IOE Tiếng Anh:* Phối hợp tổ Ngoại ngữ đôn đốc học sinh tham gia tự luyện các vòng điều kiện.", indent=True)
    add_paragraph_styled(doc, "- **Góp ý SGK Toán – Tin theo GDPT 2018 (Khó khăn & Biện pháp khắc phục):**", indent=True)
    add_paragraph_styled(doc, "  + *SGK Toán 8 (Bài 10: Tứ giác lồi & tổng các góc bằng 360°):* Khó khăn học sinh khó hình dung khái niệm hai đỉnh cùng phía đối với đường thẳng chứa cạnh còn lại; dễ nhầm lẫn các góc nhỏ bị chia cắt bởi đường chéo. Biện pháp: Cho học sinh dùng phần mềm GeoGebra kéo thả đỉnh tứ giác, đánh số góc 1, 2 trước khi cộng góc.", indent=True)
    add_paragraph_styled(doc, "  + *SGK Toán 9 (Bài 11, 12: Tỉ số lượng giác & Hệ thức cạnh – góc trong tam giác vuông):* Khó khăn học sinh nhầm lẫn cạnh đối/kề, khó mô hình hóa bài toán thực tế. Biện pháp: Dùng câu vè quen thuộc \"Sao Đi Học, Cứ Khóc Hoài, Thôi Đi Tắm, Cùng Đi Tắm\", áp dụng phương pháp \"Xác định góc nhìn\" và tăng cường vẽ sơ đồ tam giác vuông từ tình huống thực tế (chiều cao cây, tòa nhà, bóng nắng).", indent=True)
    
    add_section_h2(doc, "4. Ngoại khóa và các hoạt động khác:")
    add_paragraph_styled(doc, "- Thực hiện hoạt động ngoài giờ lên lớp theo chủ điểm \"Truyền thống nhà trường\"; tham gia tổ chức Tết Trung thu cho học sinh toàn trường.", indent=True)
    add_paragraph_styled(doc, "- Chuẩn bị tốt hồ sơ sổ sách, kế hoạch bài dạy phục vụ công tác Kiểm tra nội bộ của nhà trường trong tháng 10/2026.", indent=True)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. THẢO LUẬN CHUYÊN MÔN VÀ Ý KIẾN CỦA CÁC THÀNH VIÊN TRONG TỔ")
    add_paragraph_styled(doc, "Cuộc họp đã dành phần lớn thời gian để thảo luận chuyên sâu vào trọng tâm: **Phương pháp và giải pháp kỹ thuật tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI vào Kế hoạch bài dạy 5512**, đồng thời tháo gỡ các vướng mắc thực tế khi triển khai tại trường THCS Trần Phú:", indent=True)
    
    # Thảo luận 1: Kỹ thuật tích hợp NLS và AI vào tiến trình 4 hoạt động của CV 5512
    add_paragraph_styled(doc, "**1. Thảo luận về kỹ thuật tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI vào KHBD theo CV 5512:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Tấn Thiên (Tổ trưởng chuyên môn / Chủ trì):** Đặt vấn đề thảo luận: Theo hướng dẫn của Sở GD&ĐT tại Công văn 4200 và Công văn 5588 của Bộ GD&ĐT, năm học 2026 – 2027 bắt buộc phải thể hiện rõ việc tích hợp Khung Năng lực số (NLS) tối thiểu 20% tổng số tiết và 12 tiết Khung AI vào Kế hoạch bài dạy. Tuy nhiên, qua rà soát bước đầu, nhiều giáo viên còn lúng túng: Ghi mục tiêu NLS và AI ở vị trí nào trong giáo án 5512? Thiết kế hoạt động của học sinh ra sao để không biến tiết Toán thành tiết Tin học và không làm quá tải thời lượng 45 phút? Đề nghị các thầy cô đi thẳng vào giải pháp kỹ thuật cụ thể.", indent=True)
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (GV môn Toán khối 7 & 8):** Phân tích quy trình biên soạn cụ thể: Trong giáo án 5512, tại mục I. MỤC TIÊU (phần Năng lực), giáo viên bổ sung thêm chỉ báo: `*Năng lực số (NLS)*` và `*Năng lực Trí tuệ nhân tạo (AI)*`. Trong tiến trình 4 hoạt động dạy học, vị trí thích hợp nhất để tích hợp là **Hoạt động 3 (Luyện tập)** hoặc **Hoạt động 4 (Vận dụng)**. Ví dụ: Trong bài Thống kê biểu đồ (Toán 7) hoặc bài Hàm số và đồ thị (Toán 8), giáo viên giao nhiệm vụ cho học sinh dùng máy tính hoặc điện thoại thông minh tra cứu bảng số liệu thực tế tại địa phương, hoặc dùng phần mềm vẽ đồ thị kiểm tra nghiệm. Phần mô tả hoạt động của giáo viên và học sinh có yếu tố số/AI bắt buộc phải **in đậm, in nghiêng** để làm căn cứ đánh giá duyệt giáo án ký số.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Trần Sáng (Phó Tổ trưởng, GV môn Toán 9):** Bổ sung kinh nghiệm môn Toán 9: Môn Toán 9 kiến thức rất nặng để ôn thi vào lớp 10, giáo viên không nên gượng ép tiết nào cũng đưa AI vào. Nhóm Toán 9 đã họp sơ bộ và thống nhất: Trong 12 tiết Khung AI, môn Toán 9 chỉ đăng ký tích hợp 03 tiết trọng điểm: (1) Tiết Luyện tập Tỉ số lượng giác (sử dụng công cụ mô phỏng AI / phần mềm đo đạc gián tiếp); (2) Tiết Đồ thị hàm số bậc nhất $y = ax + b$ (sử dụng phần mềm GeoGebra mô phỏng sự biến thiên của hệ số góc); (3) Tiết Bảng tần số và Biểu đồ tần số (sử dụng AI phân tích dữ liệu lớn). Các tiết còn lại, tích hợp NLS ở mức độ rèn luyện kỹ năng bấm máy tính cầm tay Casio FX-580VN/880BTG và làm bài tập trắc nghiệm số trên nền tảng OLM.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Tấn Thiên (Tổ trưởng):** Kết luận thống nhất: Cách tiếp cận của cô Bình và thầy Sáng là rất thực tế. Tuyệt đối không \"khoác áo AI\" một cách hình thức. Giao Thầy Sáng và Cô Bình hoàn thành 02 bài soạn mẫu có tích hợp NLS và AI (01 bài Toán 8, 01 bài Toán 9) đưa lên nhóm Zalo tổ trước ngày 18/9 để toàn tổ cùng áp dụng đồng bộ.", indent=True)
    
    # Thảo luận 2: Môn Tin học chủ lực gánh vác 12 tiết AI
    add_paragraph_styled(doc, "**2. Thảo luận về vai trò chủ lực của môn Tin học trong việc triển khai 12 tiết Khung AI cốt lõi:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (GV môn Tin học):** Khẳng định: Môn Tin học là môn học nòng cốt gánh vác 12 tiết AI cốt lõi theo hướng dẫn của Bộ GD&ĐT. Nhóm Tin học (thầy Tùng, thầy Danh, cô Thảo) đã đối chiếu chương trình SGK Tin học Cánh Diều cả 4 khối và xác định địa chỉ 12 tiết AI cụ thể: Khối 6 (Chủ đề E – Tìm kiếm thông tin và ứng dụng trợ lý số); Khối 7 (Chủ đề E – Thu thập, xử lý và trực quan hóa bảng tính); Khối 8 (Chủ đề F – Bước đầu làm quen với thuật toán học máy và phân loại dữ liệu); Khối 9 (Chủ đề D & F – Sử dụng AI tạo sinh có trách nhiệm, bảo mật dữ liệu và đạo đức số). Nhóm Tin học sẽ đưa toàn bộ 12 tiết này vào Kế hoạch dạy học (Phụ lục 1) môn Tin học nộp về nhà trường.", indent=True)
    add_paragraph_styled(doc, "- **Cô Nguyễn Thị Thảo (GV môn Tin học):** Để học sinh thực hành tốt 12 tiết AI, phòng máy vi tính cần được cài đặt sẵn các tiện ích mô phỏng và bảo đảm đường truyền internet ổn định. Đề nghị trong các tiết học AI, giáo viên cho học sinh thực hành nhóm đôi, có sản phẩm cụ thể (bài trình chiếu, poster số, đoạn mã lập trình Scratch đơn giản ứng dụng nhận dạng hình ảnh) để học sinh hứng thú học tập.", indent=True)
    
    # Thảo luận 3: Quy trình hoàn thiện Phụ lục 1, 2, 3 và đưa lên CSDL ngành
    add_paragraph_styled(doc, "**3. Thảo luận về quy trình hoàn thiện Phụ lục 1, 2, 3 theo Công văn 5512 và đưa lên CSDL ngành:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hồ Đăng Danh (GV Tin học, phụ trách kỹ thuật CSDL ngành):** Lưu ý các thầy cô trong tổ: Năm học này Sở GD&ĐT kiểm tra hồ sơ giáo án hoàn toàn trên môi trường số. Khi các nhóm bộ môn hoàn thành Phụ lục 1 (Kế hoạch dạy học theo 35 tuần) và Phụ lục 2 (Kế hoạch hoạt động giáo dục), trưởng nhóm phải rà soát thật kỹ số tiết, tên bài học khớp 100% với thời khóa biểu và PPCT. Riêng Phụ lục 3 của từng giáo viên, phần \"Kế hoạch thực hiện chương trình\" phải thể hiện rõ các tuần kiểm tra giữa kỳ, cuối kỳ và các tiết tích hợp NLS/AI. Thầy Danh sẽ trực tiếp hỗ trợ các thầy cô tải tệp lên hệ thống và ký số phê duyệt đúng hạn trước ngày 30/9.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Đinh Văn Đông (Hiệu trưởng):** Quán triệt: Phụ lục 1, 2, 3 theo CV 5512 là \"xương sống\" pháp lý của toàn bộ hoạt động chuyên môn trong năm học. Sau khi Hiệu trưởng phê duyệt trên CSDL ngành, giáo viên phải thực hiện nghiêm túc theo đúng tiến độ, không tự ý đảo tiết hay cắt xén chương trình. Ban Giám hiệu sẽ kiểm tra ngẫu nhiên hồ sơ sổ sách và việc ký số hàng tuần của từng giáo viên.", indent=True)
    
    # Thảo luận 4: Phối hợp phát động VioEdu và kiểm tra thường xuyên qua OLM
    add_paragraph_styled(doc, "**4. Thảo luận về phối hợp phát động Đấu trường VioEdu Toán và kiểm tra thường xuyên qua OLM:**", indent=True)
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (GV môn Toán khối 7):** Đề nghị giáo viên dạy Toán các khối 6, 7, 8, 9 lập danh sách từ 5 đến 10 học sinh có học lực khá, giỏi môn Toán mỗi lớp chuyển cho quản trị trường để kích hoạt tài khoản VioEdu thi đấu vòng trường. Đồng thời, đề nghị Ban Giám hiệu và Tổng phụ trách Đội đưa phong trào VioEdu vào tiêu chí chấm điểm thi đua tuần giữa các lớp để tạo động lực cho học sinh tham gia đông đảo.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Trần Long Hải (GV môn Toán, GVCN lớp 8/3):** Cần nhắc nhở giáo viên bộ môn khi giao bài tập rèn luyện trên VioEdu hoặc OLM phải hướng dẫn cụ thể cách đăng nhập cho học sinh, đặc biệt học sinh lớp 6 mới vào trường, tránh để phụ huynh phải phản ánh vì không biết cách thao tác.", indent=True)
    
    # Thảo luận 5: Chuẩn bị hồ sơ chuyên môn cho công tác Kiểm tra nội bộ tháng 10
    add_paragraph_styled(doc, "**5. Thảo luận về chuẩn bị hồ sơ chuyên môn cho công tác Kiểm tra nội bộ tháng 10/2026:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh & Thầy Nguyễn Văn Tính:** Tháng 10 tới nhà trường sẽ triển khai kiểm tra toàn diện và kiểm tra chuyên môn định kỳ theo kế hoạch kiểm tra nội bộ. Giáo viên trong tổ cần chủ động rà soát Kế hoạch bài dạy 4 hoạt động, sổ đầu bài, việc ghi nhận xét và vào điểm thường xuyên đợt 1 trên hệ thống SMAS/CSDL ngành, bảo đảm khớp tiến độ từng ngày, không để dồn việc vào cuối đợt kiểm tra.", indent=True)
    
    # ==================== PHẦN V ====================
    add_section_h1(doc, "V. KẾT LUẬN VÀ BIỂU QUYẾT")
    add_paragraph_styled(doc, "- Thầy Tổ trưởng Hoàng Tấn Thiên tổng hợp các ý kiến thảo luận và kết luận: Toàn thể giáo viên trong tổ phát huy tinh thần đoàn kết, trách nhiệm, tập trung hoàn thiện hệ thống hồ sơ Phụ lục 1, 2, 3 theo Công văn 5512 trước ngày 30/9; thực hiện nghiêm túc việc tích hợp Năng lực số và 12 tiết Khung AI vào KHBD; chuẩn bị tốt nhất các điều kiện chuyên môn phục vụ giảng dạy và kiểm tra nội bộ tháng 10.", indent=True)
    add_paragraph_styled(doc, "- **Biểu quyết:** 10/10 thành viên có mặt tán thành 100% với các nội dung đánh giá công tác đầu tháng 9, kế hoạch trọng tâm và các giải pháp chuyên môn đã thống nhất.", indent=True)
    add_paragraph_styled(doc, "Biên bản cuộc họp kết thúc vào lúc 10 giờ 00 phút cùng ngày, đã được đọc lại cho toàn thể các thành viên cùng nghe, nhất trí thông qua và ký xác nhận dưới đây; biên bản được lập thành 02 bản có giá trị như nhau, lưu hồ sơ tổ chuyên môn và gửi Ban Giám hiệu nhà trường./.", indent=True)
    
    # 5. Khung chữ ký chuẩn
    add_bien_ban_signatures(
        doc,
        chu_tri="Hoàng Tấn Thiên",
        thu_ky="Lê Thị Bình"
    )
    
    # 6. Danh sách các thành viên khác của tổ ký xác nhận
    p_tv = doc.add_paragraph()
    p_tv.paragraph_format.space_before = Pt(12)
    p_tv.paragraph_format.space_after = Pt(4)
    r_tv = p_tv.add_run("CÁC THÀNH VIÊN KHÁC CỦA TỔ CHUYÊN MÔN KÝ XÁC NHẬN:\n")
    r_tv.font.name = 'Times New Roman'
    r_tv.font.size = Pt(13)
    r_tv.bold = True
    
    table_tv = doc.add_table(rows=2, cols=4)
    table_tv.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_tv.autofit = False
    
    for r in table_tv.rows:
        for c in r.cells:
            tcPr = c._tc.get_or_add_tcPr()
            tcBorders = parse_xml(r'<w:tcBorders {}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>'.format(nsdecls('w')))
            tcPr.append(tcBorders)
            
    members_r1 = ["Đinh Văn Đông", "Trần Sáng", "Hồ Đăng Danh", "Hoàng Xuân Ánh"]
    members_r2 = ["Trần Long Hải", "Nguyễn Thị Thảo", "Nguyễn Văn Tính", "Dương Quang Tùng"]
    
    for i, name in enumerate(members_r1):
        cell = table_tv.rows[0].cells[i]
        cell.width = Inches(1.7)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(25)
        r = p.add_run(f"(Ký tên)\n\n\n**{name}**")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    for i, name in enumerate(members_r2):
        cell = table_tv.rows[1].cells[i]
        cell.width = Inches(1.7)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(25)
        r = p.add_run(f"(Ký tên)\n\n\n**{name}**")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    save_docx_robust(doc, out_docx_path)
    print(f"Da xuat thanh cong file Word: {out_docx_path}")
    
    if out_md_path:
        os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
        tao_bien_ban_hop_to_lan_1_thang_9_md(out_md_path)
        print(f"Da xuat thanh cong file Markdown: {out_md_path}")

def tao_bien_ban_hop_to_lan_1_thang_9_md(out_md_path):
    """Xuất phiên bản Markdown cho Biên bản họp tổ Lần 1 Tháng 9/2026."""
    md_content = """<div align="center">

| **TRƯỜNG THCS TRẦN PHÚ**<br>**TỔ TOÁN - TIN HỌC**<br>Số: 02/BB-TCM | **CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM**<br>**Độc lập – Tự do – Hạnh phúc**<br>──────────────────<br>*Xuân Đông, ngày 12 tháng 9 năm 2026* |
|:---:|:---:|

---

# BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1
### SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 9/2026 (LẦN 1)
*(Năm học: 2026 – 2027)*
──────────────────

</div>

Hôm nay, vào lúc 07 giờ 30 phút, ngày 12 tháng 9 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 9 năm học 2026 – 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.  
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.  
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).  
  + *Danh sách thành viên:* Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

<div align="center">

### NỘI DUNG CUỘC HỌP

</div>

## I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN

Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt các văn bản chỉ đạo trọng tâm của Bộ Giáo dục và Đào tạo, Sở Giáo dục và Đào tạo và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:

**1. Hướng dẫn xây dựng và tổ chức thực hiện kế hoạch giáo dục của nhà trường (Công văn số 5512/BGDĐT-GDTrH ngày 18/12/2020 của Bộ GD&ĐT):**
- **Ý chính cốt lõi:** Quy định chuẩn hóa hệ thống hồ sơ kế hoạch giáo dục của tổ chuyên môn và giáo viên bao gồm: (1) **Phụ lục 1** – Khung kế hoạch dạy học môn học của tổ chuyên môn (phân phối chương trình 35 tuần, yêu cầu cần đạt, thiết bị dạy học, phòng học bộ môn); (2) **Phụ lục 2** – Khung kế hoạch tổ chức các hoạt động giáo dục của tổ chuyên môn (chuyên đề, chủ đề liên môn, bài học STEM); (3) **Phụ lục 3** – Khung kế hoạch giáo dục của giáo viên trong năm học (kế hoạch cá nhân theo phân công chuyên môn, chỉ tiêu, bồi dưỡng học sinh); (4) **Phụ lục 4** – Khung kế hoạch bài dạy (KHBD) cấu trúc 4 hoạt động: Mở đầu/Khởi động, Hình thành kiến thức mới, Luyện tập, Vận dụng.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Các nhóm bộ môn (Toán 6, 7, 8, 9; Tin học 6, 7, 8, 9) hoàn thiện Phụ lục 1, Phụ lục 2 và từng cá nhân hoàn thiện Phụ lục 3 nộp phê duyệt trên Cơ sở dữ liệu ngành chậm nhất ngày 30/9/2026; đặc biệt, bắt buộc tích hợp **Khung Năng lực số (20% số tiết)** và **12 tiết Khung AI** vào Phụ lục 1, Phụ lục 3 và thể hiện in đậm, in nghiêng rõ nét trong Kế hoạch bài dạy (Phụ lục 4) để phục vụ kiểm tra, duyệt giáo án ký số.

**2. Kế hoạch tham gia Hội thi giáo dục phòng, chống ma túy năm học 2026 – 2027 (Kế hoạch số 81/KH-THCS.TP ngày 11/9/2026 của Trường THCS Trần Phú và Kế hoạch số 4777/KH-SGDĐT của Sở GD&ĐT):**
- **Ý chính cốt lõi:** Mỗi sản phẩm dự thi gồm 01 Kế hoạch bài dạy (hoặc Kế hoạch tổ chức hoạt động giáo dục) + 01 Bài giảng điện tử tương ứng bám sát chủ đề phòng, chống ma túy trong học đường; toàn bộ sản phẩm được số hóa, đóng gói dưới dung lượng 1GB; sản phẩm có tính nguyên gốc do chính giáo viên xây dựng; được phép sử dụng công cụ số/AI hỗ trợ thiết kế nhưng không dùng AI thay thế phần sáng tạo và chuyên môn của tác giả; hạn nộp cấp trường ngày 20/9/2026 và nộp về Sở GD&ĐT trước ngày 25/9/2026.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phân công **Thầy Trần Sáng** và **Cô Lê Thị Bình** trực tiếp biên soạn 02 sản phẩm đại diện tổ tham gia dự thi; Thầy Tổ trưởng theo dõi tiến độ, chủ trì phiên họp tổ góp ý chuyên môn và thẩm định sản phẩm trước khi nộp Ban Giám hiệu; các thành viên trong tổ hỗ trợ tư liệu, video học liệu và kỹ thuật công nghệ thông tin phục vụ đóng gói bài giảng điện tử.

## II. ĐÁNH GIÁ CÔNG TÁC GIAI ĐOẠN ĐẦU THÁNG 9/2026

### **1. Công tác chủ nhiệm:**
- Giáo viên chủ nhiệm các khối lớp đã nhanh chóng ổn định tổ chức nề nếp lớp chủ nhiệm ngay từ ngày tựu trường; duy trì nghiêm túc sinh hoạt 15 phút đầu giờ trước buổi học; hoàn thành phổ biến nội quy trường lớp, kiện toàn ban cán sự lớp.
- Đã lập danh sách học sinh có hoàn cảnh khó khăn đề nghị nhà trường trao quà, học bổng trong lễ khai giảng ngày 05/9/2026; cùng học sinh tham gia vệ sinh phong quang trường lớp chuẩn bị chu đáo cho ngày hội khai trường.

### **2. Kỷ luật lao động và ngày giờ công:**
- 100% giáo viên trong tổ chấp hành nghiêm túc quy định ngày giờ công, tham gia đầy đủ lễ khai giảng năm học mới ngày 05/9/2026 và các buổi hội họp của nhà trường; giảng dạy đúng thời khóa biểu chính thức bắt đầu từ ngày 07/9/2026.

### **3. Công tác chuyên môn:**
- Các nhóm bộ môn đã thống nhất cấu trúc soạn Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH; bắt đầu đưa giáo án lên Cơ sở dữ liệu ngành để ký số tuần.
- Tổ chức dạy và học ổn định theo thời khóa biểu áp dụng từ 07/9/2026; thực hiện tốt kế hoạch dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT.
- Tham gia đầy đủ các buổi tập huấn chuyên môn trực tuyến về chuyển đổi số, tập huấn dạy học và kiểm tra đánh giá trên nền tảng OLM.

### **4. Phòng bộ môn và thiết bị dạy học:**
- Đã kiểm tra nề nếp ra vào lớp học, phòng máy vi tính bộ môn; rà soát thiết bị dạy học và cơ sở vật chất 02 phòng máy sau đợt bảo dưỡng đầu năm của nhà trường.

## III. KẾ HOẠCH TRỌNG TÂM THỜI GIAN TỚI (THÁNG 9 & ĐẦU THÁNG 10/2026)

### **1. Công tác chủ nhiệm:**
- Ổn định vững chắc nề nếp lớp chủ nhiệm, củng cố đội ngũ cán bộ lớp, tham gia họp GVCN; xây dựng Kế hoạch chủ nhiệm năm học 2026 – 2027.
- Đẩy mạnh tuyên truyền thực hiện Tháng An toàn giao thông, tổ chức cho 100% học sinh ký cam kết đội mũ bảo hiểm khi đi xe máy điện, xe đạp điện; tuyên truyền phòng chống tệ nạn xã hội và dịch bệnh.
- Cập nhật, rà soát hoàn thiện 100% thông tin học sinh lớp chủ nhiệm trên hệ thống Cơ sở dữ liệu ngành.
- Chuẩn bị chu đáo nội dung họp cha mẹ học sinh đầu năm; giữ gìn sổ đầu bài cẩn thận, nhắc nhở giáo viên bộ môn ghi chép đầy đủ các cột mục và GVCN tổng hợp ký tuần.

### **2. Kỷ luật ngày giờ công:**
- Giáo viên trong tổ phấn đấu bảo đảm ngày giờ công, chấp hành nghiêm túc thời khóa biểu, không đi trễ về sớm; thực hiện nghiêm túc quy định dạy thay, dạy bù khi có giáo viên đi công tác hoặc ốm đau.

### **3. Công tác chuyên môn:**
- **Hoàn thành các Phụ lục theo Công văn 5512:** Các nhóm bộ môn Toán, Tin học hoàn thiện Kế hoạch dạy học của tổ (Phụ lục 1), Kế hoạch tổ chức các hoạt động giáo dục (Phụ lục 2) và Kế hoạch giáo dục của giáo viên (Phụ lục 3), nộp phê duyệt trên CSDL ngành chậm nhất ngày 30/9/2026.
- **Tham gia Hội thi giáo dục phòng, chống ma túy:** Thầy Sáng, Cô Bình hoàn thành KHBD và bài giảng điện tử trước 20/9 để tổ góp ý hoàn thiện, nộp Ban Giám hiệu xét chọn gửi Sở GD&ĐT trước 25/9.
- **Phát động các phong trào thi trực tuyến:**
  + *Đấu trường VioEdu môn Toán:* Phân công giáo viên phụ trách hướng dẫn học sinh đăng nhập và luyện tập: Khối 6 (Cô Thảo), Khối 7 (Thầy Ánh), Khối 8 (Cô Bình), Khối 9 (Thầy Sáng).
  + *Cuộc thi IOE Tiếng Anh:* Phối hợp tổ Ngoại ngữ đôn đốc học sinh tham gia tự luyện các vòng điều kiện.
- **Góp ý SGK Toán – Tin theo GDPT 2018 (Khó khăn & Biện pháp khắc phục):**
  + *SGK Toán 8 (Bài 10: Tứ giác lồi & tổng các góc bằng 360°):* Khó khăn học sinh khó hình dung khái niệm hai đỉnh cùng phía đối với đường thẳng chứa cạnh còn lại; dễ nhầm lẫn các góc nhỏ bị chia cắt bởi đường chéo. Biện pháp: Cho học sinh dùng phần mềm GeoGebra kéo thả đỉnh tứ giác, đánh số góc 1, 2 trước khi cộng góc.
  + *SGK Toán 9 (Bài 11, 12: Tỉ số lượng giác & Hệ thức cạnh – góc trong tam giác vuông):* Khó khăn học sinh nhầm lẫn cạnh đối/kề, khó mô hình hóa bài toán thực tế. Biện pháp: Dùng câu vè quen thuộc "Sao Đi Học, Cứ Khóc Hoài, Thôi Đi Tắm, Cùng Đi Tắm", áp dụng phương pháp "Xác định góc nhìn" và tăng cường vẽ sơ đồ tam giác vuông từ tình huống thực tế (chiều cao cây, tòa nhà, bóng nắng).

### **4. Ngoại khóa và các hoạt động khác:**
- Thực hiện hoạt động ngoài giờ lên lớp theo chủ điểm "Truyền thống nhà trường"; tham gia tổ chức Tết Trung thu cho học sinh toàn trường.
- Chuẩn bị tốt hồ sơ sổ sách, kế hoạch bài dạy phục vụ công tác Kiểm tra nội bộ của nhà trường trong tháng 10/2026.

## IV. THẢO LUẬN CHUYÊN MÔN VÀ Ý KIẾN CỦA CÁC THÀNH VIÊN TRONG TỔ

Cuộc họp đã dành phần lớn thời gian để thảo luận chuyên sâu vào trọng tâm: **Phương pháp và giải pháp kỹ thuật tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI vào Kế hoạch bài dạy 5512**, đồng thời tháo gỡ các vướng mắc thực tế khi triển khai tại trường THCS Trần Phú:

**1. Thảo luận về kỹ thuật tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI vào KHBD theo CV 5512:**
- **Thầy Hoàng Tấn Thiên (Tổ trưởng chuyên môn / Chủ trì):** Đặt vấn đề thảo luận: Theo hướng dẫn của Sở GD&ĐT tại Công văn 4200 và Công văn 5588 của Bộ GD&ĐT, năm học 2026 – 2027 bắt buộc phải thể hiện rõ việc tích hợp Khung Năng lực số (NLS) tối thiểu 20% tổng số tiết và 12 tiết Khung AI vào Kế hoạch bài dạy. Tuy nhiên, qua rà soát bước đầu, nhiều giáo viên còn lúng túng: Ghi mục tiêu NLS và AI ở vị trí nào trong giáo án 5512? Thiết kế hoạt động của học sinh ra sao để không biến tiết Toán thành tiết Tin học và không làm quá tải thời lượng 45 phút? Đề nghị các thầy cô đi thẳng vào giải pháp kỹ thuật cụ thể.
- **Cô Lê Thị Bình (GV môn Toán khối 7 & 8):** Phân tích quy trình biên soạn cụ thể: Trong giáo án 5512, tại mục I. MỤC TIÊU (phần Năng lực), giáo viên bổ sung thêm chỉ báo: `*Năng lực số (NLS)*` và `*Năng lực Trí tuệ nhân tạo (AI)*`. Trong tiến trình 4 hoạt động dạy học, vị trí thích hợp nhất để tích hợp là **Hoạt động 3 (Luyện tập)** hoặc **Hoạt động 4 (Vận dụng)**. Ví dụ: Trong bài Thống kê biểu đồ (Toán 7) hoặc bài Hàm số và đồ thị (Toán 8), giáo viên giao nhiệm vụ cho học sinh dùng máy tính hoặc điện thoại thông minh tra cứu bảng số liệu thực tế tại địa phương, hoặc dùng phần mềm vẽ đồ thị kiểm tra nghiệm. Phần mô tả hoạt động của giáo viên và học sinh có yếu tố số/AI bắt buộc phải **in đậm, in nghiêng** để làm căn cứ đánh giá duyệt giáo án ký số.
- **Thầy Trần Sáng (Phó Tổ trưởng, GV môn Toán 9):** Bổ sung kinh nghiệm môn Toán 9: Môn Toán 9 kiến thức rất nặng để ôn thi vào lớp 10, giáo viên không nên gượng ép tiết nào cũng đưa AI vào. Nhóm Toán 9 đã họp sơ bộ và thống nhất: Trong 12 tiết Khung AI, môn Toán 9 chỉ đăng ký tích hợp 03 tiết trọng điểm: (1) Tiết Luyện tập Tỉ số lượng giác (sử dụng công cụ mô phỏng AI / phần mềm đo đạc gián tiếp); (2) Tiết Đồ thị hàm số bậc nhất $y = ax + b$ (sử dụng phần mềm GeoGebra mô phỏng sự biến thiên của hệ số góc); (3) Tiết Bảng tần số và Biểu đồ tần số (sử dụng AI phân tích dữ liệu lớn). Các tiết còn lại, tích hợp NLS ở mức độ rèn luyện kỹ năng bấm máy tính cầm tay Casio FX-580VN/880BTG và làm bài tập trắc nghiệm số trên nền tảng OLM.
- **Thầy Hoàng Tấn Thiên (Tổ trưởng):** Kết luận thống nhất: Cách tiếp cận của cô Bình và thầy Sáng là rất thực tế. Tuyệt đối không "khoác áo AI" một cách hình thức. Giao Thầy Sáng và Cô Bình hoàn thành 02 bài soạn mẫu có tích hợp NLS và AI (01 bài Toán 8, 01 bài Toán 9) đưa lên nhóm Zalo tổ trước ngày 18/9 để toàn tổ cùng áp dụng đồng bộ.

**2. Thảo luận về vai trò chủ lực của môn Tin học trong việc triển khai 12 tiết Khung AI cốt lõi:**
- **Thầy Dương Quang Tùng (GV môn Tin học):** Khẳng định: Môn Tin học là môn học nòng cốt gánh vác 12 tiết AI cốt lõi theo hướng dẫn của Bộ GD&ĐT. Nhóm Tin học (thầy Tùng, thầy Danh, cô Thảo) đã đối chiếu chương trình SGK Tin học Cánh Diều cả 4 khối và xác định địa chỉ 12 tiết AI cụ thể: Khối 6 (Chủ đề E – Tìm kiếm thông tin và ứng dụng trợ lý số); Khối 7 (Chủ đề E – Thu thập, xử lý và trực quan hóa bảng tính); Khối 8 (Chủ đề F – Bước đầu làm quen với thuật toán học máy và phân loại dữ liệu); Khối 9 (Chủ đề D & F – Sử dụng AI tạo sinh có trách nhiệm, bảo mật dữ liệu và đạo đức số). Nhóm Tin học sẽ đưa toàn bộ 12 tiết này vào Kế hoạch dạy học (Phụ lục 1) môn Tin học nộp về nhà trường.
- **Cô Nguyễn Thị Thảo (GV môn Tin học):** Để học sinh thực hành tốt 12 tiết AI, phòng máy vi tính cần được cài đặt sẵn các tiện ích mô phỏng và bảo đảm đường truyền internet ổn định. Đề nghị trong các tiết học AI, giáo viên cho học sinh thực hành nhóm đôi, có sản phẩm cụ thể (bài trình chiếu, poster số, đoạn mã lập trình Scratch đơn giản ứng dụng nhận dạng hình ảnh) để học sinh hứng thú học tập.

**3. Thảo luận về quy trình hoàn thiện Phụ lục 1, 2, 3 theo Công văn 5512 và đưa lên CSDL ngành:**
- **Thầy Hồ Đăng Danh (GV Tin học, phụ trách kỹ thuật CSDL ngành):** Lưu ý các thầy cô trong tổ: Năm học này Sở GD&ĐT kiểm tra hồ sơ giáo án hoàn toàn trên môi trường số. Khi các nhóm bộ môn hoàn thành Phụ lục 1 (Kế hoạch dạy học theo 35 tuần) và Phụ lục 2 (Kế hoạch hoạt động giáo dục), trưởng nhóm phải rà soát thật kỹ số tiết, tên bài học khớp 100% với thời khóa biểu và PPCT. Riêng Phụ lục 3 của từng giáo viên, phần "Kế hoạch thực hiện chương trình" phải thể hiện rõ các tuần kiểm tra giữa kỳ, cuối kỳ và các tiết tích hợp NLS/AI. Thầy Danh sẽ trực tiếp hỗ trợ các thầy cô tải tệp lên hệ thống và ký số phê duyệt đúng hạn trước ngày 30/9.
- **Thầy Đinh Văn Đông (Hiệu trưởng):** Quán triệt: Phụ lục 1, 2, 3 theo CV 5512 là "xương sống" pháp lý của toàn bộ hoạt động chuyên môn trong năm học. Sau khi Hiệu trưởng phê duyệt trên CSDL ngành, giáo viên phải thực hiện nghiêm túc theo đúng tiến độ, không tự ý đảo tiết hay cắt xén chương trình. Ban Giám hiệu sẽ kiểm tra ngẫu nhiên hồ sơ sổ sách và việc ký số hàng tuần của từng giáo viên.

**4. Thảo luận về phối hợp phát động Đấu trường VioEdu Toán và kiểm tra thường xuyên qua OLM:**
- **Cô Lê Thị Bình (GV môn Toán khối 7):** Đề nghị giáo viên dạy Toán các khối 6, 7, 8, 9 lập danh sách từ 5 đến 10 học sinh có học lực khá, giỏi môn Toán mỗi lớp chuyển cho quản trị trường để kích hoạt tài khoản VioEdu thi đấu vòng trường. Đồng thời, đề nghị Ban Giám hiệu và Tổng phụ trách Đội đưa phong trào VioEdu vào tiêu chí chấm điểm thi đua tuần giữa các lớp để tạo động lực cho học sinh tham gia đông đảo.
- **Thầy Trần Long Hải (GV môn Toán, GVCN lớp 8/3):** Cần nhắc nhở giáo viên bộ môn khi giao bài tập rèn luyện trên VioEdu hoặc OLM phải hướng dẫn cụ thể cách đăng nhập cho học sinh, đặc biệt học sinh lớp 6 mới vào trường, tránh để phụ huynh phải phản ánh vì không biết cách thao tác.

**5. Thảo luận về chuẩn bị hồ sơ chuyên môn cho công tác Kiểm tra nội bộ tháng 10/2026:**
- **Thầy Hoàng Xuân Ánh & Thầy Nguyễn Văn Tính:** Tháng 10 tới nhà trường sẽ triển khai kiểm tra toàn diện và kiểm tra chuyên môn định kỳ theo kế hoạch kiểm tra nội bộ. Giáo viên trong tổ cần chủ động rà soát Kế hoạch bài dạy 4 hoạt động, sổ đầu bài, việc ghi nhận xét và vào điểm thường xuyên đợt 1 trên hệ thống SMAS/CSDL ngành, bảo đảm khớp tiến độ từng ngày, không để dồn việc vào cuối đợt kiểm tra.

## V. KẾT LUẬN VÀ BIỂU QUYẾT

- Thầy Tổ trưởng Hoàng Tấn Thiên tổng hợp các ý kiến thảo luận và kết luận: Toàn thể giáo viên trong tổ phát huy tinh thần đoàn kết, trách nhiệm, tập trung hoàn thiện hệ thống hồ sơ Phụ lục 1, 2, 3 theo Công văn 5512 trước ngày 30/9; thực hiện nghiêm túc việc tích hợp Năng lực số và 12 tiết Khung AI vào KHBD; chuẩn bị tốt nhất các điều kiện chuyên môn phục vụ giảng dạy và kiểm tra nội bộ tháng 10.
- **Biểu quyết:** 10/10 thành viên có mặt tán thành 100% với các nội dung đánh giá công tác đầu tháng 9, kế hoạch trọng tâm và các giải pháp chuyên môn đã thống nhất.

Biên bản cuộc họp kết thúc vào lúc 10 giờ 00 phút cùng ngày, đã được đọc lại cho toàn thể các thành viên cùng nghe, nhất trí thông qua và ký xác nhận dưới đây; biên bản được lập thành 02 bản có giá trị như nhau, lưu hồ sơ tổ chuyên môn và gửi Ban Giám hiệu nhà trường./.

---

| **THƯ KÝ CUỘC HỌP**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Lê Thị Bình** | **TỔ TRƯỞNG CHUYÊN MÔN**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Hoàng Tấn Thiên** |
|:---:|:---:|

**CÁC THÀNH VIÊN KHÁC CỦA TỔ CHUYÊN MÔN KÝ XÁC NHẬN:**

| Đinh Văn Đông | Trần Sáng | Hồ Đăng Danh | Hoàng Xuân Ánh |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |

| Trần Long Hải | Nguyễn Thị Thảo | Nguyễn Văn Tính | Dương Quang Tùng |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


def tao_bien_ban_hop_to_lan_2_thang_9(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 2 Tháng 9/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="03/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 18 tháng 9 năm 2026"
    )
    
    # Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 2",
        "SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 9/2026 (LẦN 2)\nNăm học: 2026 - 2027"
    )
    
    # Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 13 giờ 30 phút, ngày 18 tháng 9 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 2 tháng 9 năm học 2026 - 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt sâu sắc các văn bản chỉ đạo của Sở Giáo dục và Đào tạo thành phố Đồng Nai, các cấp quản lý và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:", indent=True)
    
    # 1. Hướng dẫn 5351
    add_paragraph_styled(doc, "**1. Hướng dẫn một số giải pháp hạn chế việc sử dụng điện thoại di động, thiết bị thông minh, mạng xã hội của học sinh trong trường học (Hướng dẫn số 5351/HD-SGDĐT ngày 15/9/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Căn cứ Thông tư 15/2026/TT-BGDĐT và Công văn 3147/BGDĐT-HSSV của Bộ GD&ĐT. Nhằm giảm thiểu sự phụ thuộc quá mức vào thiết bị công nghệ, tạo không gian học tập tập trung, cải thiện khả năng tư duy độc lập và bảo vệ sức khỏe học đường (thị lực, cột sống, sức khỏe tâm thần) cho học sinh. Học sinh phấn đấu thực hiện bốn tiêu chuẩn “Tự”: *Tự giác* (tắt thiết bị hoặc để chế độ im lặng và cất vào nơi quy định ngay khi bước vào trường/lớp); *Tự quản* (thành lập tổ tự quản nhắc nhở nhau); *Tự rèn* (làm chủ hành vi, không để bị cuốn vào mạng xã hội); *Tự chủ* (sử dụng công nghệ đúng lúc, đúng chỗ phục vụ học tập). Triển khai đồng bộ 03 mô hình vận dụng linh hoạt: (1) Mô hình *“Hộp lưu trữ niềm tin”* (bố trí tủ/khay/túi chuyên dụng tại lớp, học sinh cất thiết bị đầu buổi và nhận lại sau buổi học); (2) Mô hình *“Giờ ra chơi không màn hình”* (tổ chức cờ vua, trò chơi dân gian, góc đọc sách xanh); (3) Mô hình *“Tích hợp giáo dục kỹ năng số”* (hướng dẫn lọc thông tin, bảo mật cá nhân, ứng xử văn minh trên không gian mạng).", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Giáo viên bộ môn Toán và Tin học làm gương, tuyệt đối không sử dụng điện thoại làm việc riêng trong giờ lên lớp. Phân định rõ ràng: Trong giờ học lý thuyết Toán và Tin học, học sinh tuyệt đối không dùng điện thoại; chỉ khi có yêu cầu nghiệp vụ bài dạy rõ ràng (tra cứu phần mềm GeoGebra, làm bài kiểm tra trực tuyến OLM/VioEdu tại phòng máy hoặc theo nhóm có kiểm soát) thì giáo viên mới cho phép mở thiết bị. Giáo viên chủ nhiệm phối hợp chặt chẽ với cha mẹ học sinh để thống nhất quản lý, phòng ngừa bắt nạt mạng và xao nhãng học tập.", indent=True)
    
    # 2. Kế hoạch 5264
    add_paragraph_styled(doc, "**2. Kế hoạch thực hiện nhiệm vụ ứng dụng công nghệ thông tin, chuyển đổi số và thống kê giáo dục năm học 2026 – 2027 (Kế hoạch số 5264/KH-SGDĐT ngày 22/9/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Bám sát Công văn 6020/BGDĐT-KHCNTT của Bộ GD&ĐT, Nghị quyết 57-NQ/TW của Bộ Chính trị, Luật Chuyển đổi số số 148/2025/QH15, Luật Dữ liệu số 60/2024/QH15, Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 và Luật Trí tuệ nhân tạo số 134/2025/QH15. Chỉ đạo xuyên suốt theo tinh thần **“6 rõ”** (*rõ người, rõ việc, rõ thời gian, rõ trách nhiệm, rõ sản phẩm, rõ thẩm quyền*). Dữ liệu giáo dục phải bảo đảm *“đúng, đủ, sạch, sống, thống nhất, dùng chung”*; thực hiện nghiêm nguyên tắc *“dữ liệu cập nhật một lần, sử dụng nhiều lần”*, cắt giảm thủ tục hành chính. Đẩy mạnh phong trào *“Bình dân học vụ số”* và hưởng ứng Ngày Chuyển đổi số Quốc gia (10/10). Định hướng rõ việc thúc đẩy ứng dụng Trí tuệ nhân tạo (AI) an toàn, có kiểm soát và có trách nhiệm: Khuyến khích ứng dụng AI hỗ trợ soạn bài, xây dựng học liệu, thiết kế đề kiểm tra; tuy nhiên *kết quả do AI tạo ra phải được giáo viên kiểm chứng về tính chính xác và phù hợp sư phạm; AI tuyệt đối không thay thế trách nhiệm chuyên môn và quyền ra quyết định của nhà giáo*.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ Toán - Tin là đơn vị nòng cốt triển khai chuyển đổi số trong nhà trường; 100% giáo viên hoàn thành phê duyệt Kế hoạch bài dạy (KHBD) trên hệ thống số CSDL ngành đúng thời hạn; đảm bảo an toàn dữ liệu học bạ số và thông tin cá nhân học sinh; giáo viên Tin học chủ động tham mưu nâng cấp đường truyền và bảo đảm an ninh mạng cho hệ thống phòng máy.", indent=True)
    
    # 3. Công văn 946
    add_paragraph_styled(doc, "**3. Hướng dẫn việc trả và lưu trữ đề, bài kiểm tra, đánh giá định kỳ của học sinh (Công văn số 946/SGDĐT-GDPT&GDTX ngày 06/02/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Hướng dẫn thực hiện thống nhất quy trình trả bài và lưu trữ hồ sơ, ma trận, đặc tả, đề kiểm tra cùng bài kiểm tra, đánh giá định kỳ của học sinh bảo đảm tính chính xác, công bằng, minh bạch và đúng quy định quản lý hồ sơ chuyên môn trong nhà trường.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn thẩm định kỹ lưỡng ma trận và đề kiểm tra định kỳ các khối 6, 7, 8, 9; giáo viên thực hiện nghiêm túc quy trình chấm, trả bài có lời nhận xét cụ thể, vào điểm đúng tiến độ trên hệ thống quản lý điểm số và lưu trữ hồ sơ kiểm tra đầy đủ phục vụ kiểm tra chuyên môn.", indent=True)
    
    # 4. Công văn 4794
    add_paragraph_styled(doc, "**4. Hướng dẫn công tác kiểm tra nội bộ trường học năm học 2026 - 2027 (Công văn số 4794/SGD ngày 09/9/2026 của Sở GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Xác định mục đích, yêu cầu và quy trình tổ chức kiểm tra nhằm nâng cao hiệu quả quản trị, phòng ngừa và chấn chỉnh kịp thời các sai phạm; triển khai 06 cuộc kiểm tra chuyên đề định kỳ cùng các đợt kiểm tra đột xuất đối với toàn thể cán bộ, giáo viên, nhân viên; tập trung quy chế chuyên môn, hoạt động sư phạm, quản lý dạy thêm - học thêm, thu chi tài chính, an toàn trường học và đánh giá xếp loại học sinh.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Giáo viên trong tổ chấp hành nghiêm chỉnh quy định về dạy thêm - học thêm (tuyệt đối không dạy thêm sai quy định); thực hiện đúng kế hoạch kiểm tra nội bộ của trường; Thầy Trần Sáng tham gia tổ kiểm tra nội bộ thực hiện đúng nhiệm vụ được giao.", indent=True)
    
    # 5. Kế hoạch VioEdu
    add_paragraph_styled(doc, "**5. Kế hoạch tổ chức sân chơi “Đấu trường VioEdu” năm học 2026 - 2027 (Kế hoạch số 01/KH-TCM ngày 15/9/2026 của Tổ Toán - Tin học Trường THCS Trần Phú):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi & Quy chế thi:** Mục tiêu thúc đẩy chuyển đổi số, ứng dụng AI và khơi dậy đam mê Toán học, Toán tiếng Anh cho học sinh từ khối 6 đến khối 9 trên tinh thần tự nguyện 100%, hoàn toàn miễn phí. Học sinh thi trực tuyến trên website vio.edu.vn hoặc app VioEdu bằng 01 tài khoản định danh do nhà trường cấp. Mỗi vòng thi gồm 30 câu hỏi (20 câu Toán + 10 câu Toán tiếng Anh), thời gian làm bài cố định 20 phút.", indent=True)
    add_paragraph_styled(doc, "- **Lộ trình thời gian thực hiện:** (1) Ngày 15/9 – 20/9/2026: Khởi tạo và cấp tài khoản đồng loạt; (2) Ngày 28/9 – 13/12/2026: Vòng sơ loại trực tuyến (8 vòng sơ loại và 2 vòng định kỳ, mở từ 00h00 thứ Hai đến 23h59 Chủ nhật hàng tuần); (3) Ngày 11/01 – 15/01/2027: Vòng cấp Trường (thi tập trung tại phòng máy); (4) Ngày 23/02 – 24/02/2027: Vòng cấp Xã; (5) Ngày 30/03 – 31/03/2027: Vòng cấp Tỉnh (dành cho thí sinh đạt từ 20 điểm trở lên và nằm trong Top 30% cấp Xã).", indent=True)
    add_paragraph_styled(doc, "- **Phân công phụ trách khối:** Cô Nguyễn Thị Thảo (Khối 6), Thầy Hoàng Xuân Ánh (Khối 7), Cô Lê Thị Bình (Khối 8), Thầy Trần Sáng (Khối 9), Thầy Dương Quang Tùng (Phụ trách phòng máy và đường truyền mạng). Giáo viên phụ trách khối định kỳ báo cáo kết quả tham gia cho Tổ trưởng chuyên môn vào ngày 25 hàng tháng.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ TÌNH HÌNH CÔNG TÁC THỜI GIAN QUA")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Các giáo viên chủ nhiệm trong tổ đã nhanh chóng ổn định nề nếp lớp chủ nhiệm, tích cực duy trì sinh hoạt 15 phút đầu giờ trước buổi học, hướng dẫn học sinh học tập nội quy, củng cố đội ngũ cán bộ lớp, tham gia họp GVCN và xây dựng kế hoạch chủ nhiệm năm học 2026 - 2027.", indent=True)
    add_paragraph_styled(doc, "- Phát động sôi nổi các phong trào thi đua chào mừng ngày Quốc khánh 2/9, Tháng An toàn giao thông; cho học sinh và cha mẹ học sinh ký cam kết: Không thử, không tàng trữ, không sử dụng và buôn bán các chất ma túy, thuốc lá điện tử và chấp hành nghiêm chỉnh luật giao thông.", indent=True)
    add_paragraph_styled(doc, "- GVCN tăng cường bám sát lớp, theo dõi chuyên cần, quản lý sổ đầu bài cẩn thận, yêu cầu GVBM ghi chép đầy đủ các cột mục và GVCN tổng hợp ký duyệt hàng tuần. Hoàn thành điều tra thông tin học sinh lớp chủ nhiệm trên hệ thống CSDL ngành. Tổ chức họp cha mẹ học sinh đầu năm học vào ngày 13/9/2026 đạt kết quả tốt, thông báo các khoản thu BHYT, BHTN và triển khai đăng ký môn Tiếng Anh tăng cường.", indent=True)
    
    add_section_h2(doc, "2. Ngày giờ công và kỷ luật lao động:")
    add_paragraph_styled(doc, "- 100% giáo viên trong tổ đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ các hoạt động của nhà trường, dạy đủ các tiết theo phân công chuyên môn, thực hiện nghiêm túc việc dạy bù, dạy thay khi có giáo viên đi công tác hoặc nghỉ ốm.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- Duy trì nền nếp dạy và học ổn định theo thời khóa biểu. Thực hiện chương trình theo kế hoạch nhà trường, thực hiện dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT, thực hiện giáo dục địa phương và hoạt động trải nghiệm hướng nghiệp đúng định hướng. Giáo viên trong tổ khai thác tốt trang thiết bị dạy học và phòng bộ môn.", indent=True)
    add_paragraph_styled(doc, "- Tổ đã phân công phụ trách khối, đóng góp ý kiến xây dựng Kế hoạch giáo dục của tổ và nhà trường. Thực hiện nghiêm túc các quy chế chuyên môn.", indent=True)
    add_paragraph_styled(doc, "- 100% giáo viên trong tổ hoàn thành đợt tập huấn chuyển đổi số ngày 11/9/2026 về CSDL ngành, eNetViet, OLM, phương pháp tích hợp Năng lực số (NLS 20%) và Khung 12 tiết AI vào bài giảng.", indent=True)
    
    add_section_h2(doc, "4. Công tác chuyên đề, thao giảng:")
    add_paragraph_styled(doc, "- Tham gia đầy đủ các buổi tập huấn chuyên đề do các cấp tổ chức và phổ biến lại các nội dung thống nhất để thực hiện. Giáo viên trong tổ đã tiến hành đăng ký chuyên đề nghiên cứu bài học cho năm học.", indent=True)
    
    add_section_h2(doc, "5. Công tác kiểm tra nội bộ:")
    add_paragraph_styled(doc, "- Thường xuyên kiểm tra việc giáo viên thực hiện quy chế chuyên môn, nền nếp ra vào lớp, chất lượng soạn giảng Kế hoạch bài dạy theo đúng khung hướng dẫn.", indent=True)
    
    add_section_h2(doc, "6. Sử dụng đồ dùng dạy học và phòng chức năng:")
    add_paragraph_styled(doc, "- Khai thác có hiệu quả phòng máy tính, phòng học bộ môn. Giáo viên tiếp tục rà soát, đề xuất mua sắm bổ sung thiết bị dạy học, sách tham khảo phục vụ nhu cầu giảng dạy.", indent=True)
    
    add_section_h2(doc, "7. Công tác khác:")
    add_paragraph_styled(doc, "- Phối hợp tốt trong công tác phòng chống các loại tội phạm, phòng chống đuối nước; tham gia tích cực các hoạt động Đoàn – Đội và hoàn thành tốt nhiệm vụ điều tra phổ cập giáo dục theo phân công.", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. KẾ HOẠCH TRỌNG TÂM TRONG THỜI GIAN TỚI")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Tiếp tục ổn định nền nếp lớp chủ nhiệm, tích cực sinh hoạt 15 phút đầu giờ. Phát động đợt thi đua cao điểm chào mừng các ngày lễ lớn trong tháng 10: Ngày Quốc tế Người cao tuổi (01/10), Ngày Khuyến học Việt Nam (02/10), Ngày Bác Hồ gửi bức thư cuối cùng cho ngành Giáo dục (15/10) và Ngày Phụ nữ Việt Nam (20/10). Đẩy mạnh tuyên truyền phòng chống ma túy, ATGT, PCCC và phòng tránh tai nạn thương tích.", indent=True)
    add_paragraph_styled(doc, "- Thực hiện hiệu quả Tuần lễ hưởng ứng học tập suốt đời năm 2026. Hoàn thành hồ sơ sổ sách GVCN đúng quy định; tiếp tục rà soát, thống kê học sinh có hoàn cảnh khó khăn để kịp thời hỗ trợ; đôn đốc thu nộp BHYT, BHTN; thông tin thường xuyên với phụ huynh qua Zalo lớp và sổ liên lạc điện tử.", indent=True)
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm vận động 100% học sinh đăng ký tham gia Đấu trường VioEdu theo kế hoạch; triển khai khai thác thư viện số của trường và đăng ký học Tiếng Anh tăng cường theo chủ trương.", indent=True)
    
    add_section_h2(doc, "2. Đảm bảo ngày giờ công và nền nếp chuyên môn:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ phấn đấu đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ các hoạt động của trường, dạy đúng, dạy đủ các tiết theo phân công; thực hiện nghiêm túc việc dạy bù, dạy thay kịp thời.", indent=True)
    
    add_section_h2(doc, "3. Hoạt động chuyên môn trọng tâm:")
    add_paragraph_styled(doc, "- Thực hiện nghiêm túc việc soạn Kế hoạch bài dạy (KHBD) từ tuần 1 đến tuần 4 và hoàn thành phê duyệt, đẩy lên hệ thống CSDL ngành trong khoảng thời gian từ ngày 20/9 đến ngày 24/9/2026. Lưu ý thể hiện rõ nét nội dung giáo dục học sinh hòa nhập, tích hợp Năng lực số (NLS 20%), ứng dụng AI có kiểm soát và bài học STEM.", indent=True)
    add_paragraph_styled(doc, "- Phân công nhiệm vụ cụ thể hướng dẫn học sinh tham gia các vòng thi VioEdu đạt hiệu quả: Cô Nguyễn Thị Thảo (Khối 6), Thầy Hoàng Xuân Ánh (Khối 7), Cô Lê Thị Bình (Khối 8), Thầy Trần Sáng (Khối 9), Thầy Dương Quang Tùng (Phòng máy & đường truyền).", indent=True)
    add_paragraph_styled(doc, "- Thầy Trần Sáng tiếp tục hoàn thành bài dự thi về Chuyên môn, nghiệp vụ giáo dục phòng, chống ma túy đạt chất lượng cao.", indent=True)
    add_paragraph_styled(doc, "- **Tập trung góp ý chuyên sâu chương trình Sách giáo khoa GDPT 2018 môn Toán - Tin, nhận diện các khó khăn sư phạm và thống nhất hướng khắc phục:**", indent=True)
    add_paragraph_styled(doc, "  + *Đối với sách giáo khoa Toán lớp 8 (Bài 12: Hình thang cân):*", indent=True)
    add_paragraph_styled(doc, "    • Khó khăn thực tế: Học sinh rất dễ ngụy biện và mặc định sai lầm rằng “Hình thang có 2 cạnh bên bằng nhau là hình thang cân” (trong khi nếu 2 cạnh bên bằng nhau và song song thì đó lại là hình bình hành). Việc chứng minh Định lý 3 (Ví dụ 2 trang 54) đòi hỏi kẻ thêm đường phụ khá phức tạp so với trình độ đầu năm lớp 8.", indent=True)
    add_paragraph_styled(doc, "    • Hướng khắc phục: Khai thác triệt để phần “Tranh luận” (trang 59) và “Luyện tập chung” (trang 56) để cho học sinh vẽ cả 2 trường hợp (hai cạnh bên không song song -> hình thang cân; hai cạnh bên song song -> hình bình hành). Chuẩn hóa quy trình kẻ đường song song phụ qua một đỉnh để đưa bài toán về tam giác cân quen thuộc.", indent=True)
    add_paragraph_styled(doc, "  + *Đối với sách giáo khoa Toán lớp 6 (Bài 18 và Bài 19 về các hình phẳng trong thực tiễn):*", indent=True)
    add_paragraph_styled(doc, "    • Khó khăn thực tế: Học sinh gặp khó khăn lớn khi sử dụng compa và êke để vẽ các hình đòi hỏi kỹ thuật cao như hình lục giác đều hay hình thoi. Bên cạnh đó, học sinh rất dễ nhầm lẫn thuộc tính đường chéo giữa các hình (ví dụ: nhầm đường chéo bằng nhau của hình chữ nhật/hình thang cân với đường chéo vuông góc của hình thoi/hình vuông).", indent=True)
    add_paragraph_styled(doc, "    • Hướng khắc phục: Xây dựng Quy trình vẽ hình từng bước: Chuẩn bị phiếu học tập có hình ảnh minh họa rõ ràng các bước đặt thước, quay compa để vẽ hình thoi và hình lục giác đều. Cho học sinh lập Bảng so sánh các yếu tố Cạnh - Góc - Đường chéo của 7 hình phẳng đã học để rèn luyện tư duy phân loại thị giác.", indent=True)
    add_paragraph_styled(doc, "- Hoàn thành toàn bộ hồ sơ tổ chuyên môn theo kế hoạch năm học của nhà trường.", indent=True)
    
    add_section_h2(doc, "4. Công tác chuyên đề và nghiên cứu bài học:")
    add_paragraph_styled(doc, "- Các nhóm bộ môn lên kế hoạch thực hiện chuyên đề theo nghiên cứu bài học. Tổ thống nhất và đăng ký phổ biến chuyên đề cấp trường/tổ: Học kỳ I do Thầy Hoàng Tấn Thiên chủ trì (môn Toán); Học kỳ II do Thầy Hoàng Tấn Thiên và Thầy Trần Sáng phối hợp triển khai (môn Toán). Tham gia đầy đủ các buổi tập huấn chuyên đề do các cấp tổ chức.", indent=True)
    
    add_section_h2(doc, "5. Công tác ngoại khóa và phong trào:")
    add_paragraph_styled(doc, "- Tuyên truyền học sinh chấp hành tốt nội quy trường, lớp, tích cực tham gia các cuộc thi do Nhà trường, Đoàn, Đội tổ chức; duy trì phong trào vệ sinh “Sạch trường, đẹp lớp”.", indent=True)
    
    add_section_h2(doc, "6. Công tác kiểm tra:")
    add_paragraph_styled(doc, "- Kiểm tra nền nếp ra vào lớp, duyệt ma trận và đề kiểm tra định kỳ của tổ; kiểm tra việc soạn giảng, ra đề theo chuẩn KT-KN chương trình GDPT 2018 và kiểm tra việc thực hiện quy chế chuyên môn, sử dụng phòng CNTT.", indent=True)
    
    add_section_h2(doc, "7. Sử dụng đồ dùng dạy học và phòng CNTT:")
    add_paragraph_styled(doc, "- Sử dụng có hiệu quả phòng chức năng, phòng CNTT, khai thác triệt để các phần mềm trong giảng dạy; khuyến khích giáo viên và học sinh ươm mầm các ý tưởng sản phẩm dự thi KHKT.", indent=True)
    
    add_section_h2(doc, "8. Công tác khác:")
    add_paragraph_styled(doc, "- Vệ sinh trường lớp, trang trí lớp Xanh – Sạch – Đẹp; tham gia hoạt động Đoàn – Đội và các hoạt động do nhà trường, công đoàn phát động chào mừng các ngày lễ lớn trong tháng.", indent=True)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. Ý KIẾN THẢO LUẬN VÀ GIẢI PHÁP CHUYÊN MÔN THỰC CHIẾN")
    add_paragraph_styled(doc, "Phiên họp diễn ra thẳng thắn, dân chủ, tập trung sâu sắc vào các vấn đề chuyên môn, phản ánh đúng thực tế lớp học và đề xuất các giải pháp kỹ thuật cụ thể:", indent=True)
    
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (Giáo viên môn Toán 8, Thư ký):** Đánh giá cao tính cấp thiết của Hướng dẫn số 5351/HD-SGDĐT về hạn chế điện thoại trong trường học. Thực tế học sinh lớp 8 rất tò mò và dễ bị phân tâm bởi tin nhắn, mạng xã hội nếu mang điện thoại vào lớp. Đề xuất giải pháp: Mỗi lớp học bố trí 01 khay/túi vải có đánh số thứ tự treo tại góc bảng lớp (Mô hình Hộp lưu trữ niềm tin). Đầu buổi học, ban cán sự lớp đôn đốc học sinh tự giác tắt nguồn hoặc bật chế độ im lặng rồi cất điện thoại vào đúng ô số của mình. Trong giờ học Toán, giáo viên yêu cầu học sinh sử dụng máy tính cầm tay Casio khoa học, tuyệt đối cấm dùng phần mềm giả lập trên điện thoại để tránh việc lén lút chuyển sang ứng dụng mạng xã hội. Giáo viên chủ nhiệm cần thống nhất chặt chẽ với cha mẹ học sinh ngay từ đầu năm.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh (Giáo viên môn Toán 7, Phụ trách VioEdu Khối 7):** Đề nghị Liên đội tăng cường kiểm tra và ghi tên những học sinh không đội nón bảo hiểm khi tham gia giao thông bằng xe đạp điện, xe máy điện ở cổng trường lúc tan học. Về chuyên môn hình học: Đồng tình với giải pháp khắc phục khó khăn vẽ hình lớp 6 và hình thang cân lớp 8. Đối với thao tác vẽ hình phức tạp như lục giác đều, giáo viên nên chiếu video mô phỏng thao tác dựng hình chuẩn bằng phần mềm GeoGebra trước 2 phút, sau đó yêu cầu học sinh thực hành trên phiếu in sẵn lưới ô vuông để định hình tỷ lệ chuẩn trước khi vẽ vào vở.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (Giáo viên Tin học, Phụ trách phòng máy & hạ tầng CNTT):** Báo cáo hạ tầng CNTT: 2 phòng máy tính (45 máy) hiện hoạt động ổn định. Để triển khai tốt Kế hoạch số 5264/KH-SGDĐT và sân chơi VioEdu, Thầy Tùng đề xuất mở cửa phòng máy từ 16h30 đến 17h15 vào các ngày thứ Ba và thứ Năm hàng tuần để tạo điều kiện cho các em học sinh có hoàn cảnh khó khăn (không có máy tính/điện thoại ở nhà) được tham gia thi đấu vòng sơ loại VioEdu miễn phí dưới sự hướng dẫn của giáo viên trực phòng máy. Về việc ứng dụng AI có kiểm soát: Khuyến nghị các thầy cô trong tổ có thể sử dụng các trợ lý AI (như ChatGPT, Claude) để gợi ý các bài toán thực tế, tạo câu hỏi trắc nghiệm khách quan; tuy nhiên phải tuân thủ nghiêm ngặt nguyên tắc kiểm chứng: Giáo viên phải tự tay giải lại, thẩm định lời giải và ma trận đề, tuyệt đối không sao chép nguyên văn sản phẩm của AI đưa vào đề thi hay giáo án.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Hồ Đăng Danh (Giáo viên môn Toán):** Thống nhất bài làm kiểm tra thường xuyên (KTTX) cần thực hiện nhiều hình thức phong phú: vấn đáp, bài viết phiếu học tập, sản phẩm STEM (mô hình tam giác, hình thang cân bằng giấy carton) và đánh giá hoạt động nhóm... nhằm tạo động lực và khích lệ học sinh yếu kém tiến bộ, tránh gây áp lực điểm số đơn thuần bằng bài kiểm tra giấy truyền thống.", indent=True)
    
    add_paragraph_styled(doc, "- **Cô Nguyễn Thị Thảo (Giáo viên môn Toán 6, Phụ trách VioEdu Khối 6):** Phản ánh ý kiến của phụ huynh học sinh về môn Tiếng Anh tăng cường: Cần khảo sát phân loại học sinh theo trình độ để xếp lớp phù hợp, tránh để học sinh trung bình bị quá tải. Đối với 10 câu hỏi Toán tiếng Anh trong mỗi vòng thi VioEdu, Cô Thảo đề xuất giáo viên giảng dạy khối 6 và khối 7 dành 5 phút cuối tiết luyện tập để hướng dẫn học sinh làm quen với các thuật ngữ Toán học tiếng Anh cốt lõi (như *prime number, common divisor, right triangle, angle, perimeter, area*) giúp học sinh tự tin làm bài mà không bị rào cản ngôn ngữ.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Trần Sáng (Giáo viên môn Toán 9, KTNB):** Đề nghị thiết thực về cơ sở vật chất: Nhà trường cần sớm làm khung giá đỡ hoặc hạ thấp ti vi tại các lớp học ở cơ sở 2. Lý do ti vi hiện nay treo quá cao sát trần nhà khiến học sinh ngồi các dãy giữa và cuối phải ngửa cổ liên tục gây mỏi mắt, không quan sát rõ nét chữ và hình vẽ. Về xử lý sai lầm Hình thang cân lớp 8: Thống nhất giáo viên phải đưa ra phản ví dụ cụ thể ngay trên bảng (vẽ một hình thang có 2 cạnh bên bằng nhau và song song để học sinh tự kết luận đó là hình bình hành, từ đó khắc cốt ghi tâm điều kiện 2 cạnh bên phải *không song song* mới là hình thang cân).", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Đinh Văn Đông & Thầy Trần Long Hải:** Đề xuất nhà trường trang cấp bổ sung cho tổ bộ môn 02 bộ compa bảng compozit khổ lớn và thước đo góc có tay cầm chuyên dụng để phục vụ trực quan cho giáo viên dạy hình học các khối 6, 7. Thống nhất mốc thời gian hoàn thành Kế hoạch bài dạy (KHBD) tuần 1 đến tuần 4: 100% giáo viên nộp bài lên hệ thống CSDL ngành trước 17h00 ngày 23/9/2026 để Tổ trưởng chuyên môn kịp thời thẩm định và phê duyệt trước hạn chót 24/9/2026.", indent=True)
    
    # ==================== PHẦN V ====================
    add_section_h1(doc, "V. KẾT LUẬN CỦA CHỦ TỌA VÀ NGHỊ QUYẾT CUỘC HỌP")
    add_paragraph_styled(doc, "Thầy Tổ trưởng chuyên môn Hoàng Tấn Thiên kết luận toàn diện phiên họp và chỉ đạo thực hiện các nhiệm vụ trọng tâm sau:", indent=True)
    add_paragraph_styled(doc, "1. Toàn thể giáo viên quán triệt và thực hiện nghiêm túc Hướng dẫn số 5351/HD-SGDĐT: Triển khai hiệu quả Mô hình “Hộp lưu trữ niềm tin” tại lớp chủ nhiệm và phòng bộ môn; tuyệt đối không để học sinh lạm dụng điện thoại trong giờ học; giáo viên làm gương không sử dụng thiết bị cá nhân làm việc riêng trong tiết giảng.", indent=True)
    add_paragraph_styled(doc, "2. Bám sát tinh thần Kế hoạch số 5264/KH-SGDĐT: Thực hiện nghiêm túc nguyên tắc “6 rõ”, chuẩn hóa dữ liệu CSDL ngành theo phương châm “đúng, đủ, sạch, sống”; hoàn thành việc phê duyệt và nộp KHBD tuần 1 đến tuần 4 lên CSDL ngành đúng thời hạn (hạn chót hoàn thành của giáo viên là ngày 23/9/2026); ứng dụng AI một cách thông minh, có trách nhiệm và luôn kiểm chứng tính chính xác chuyên môn.", indent=True)
    add_paragraph_styled(doc, "3. Triển khai sâu rộng và đồng bộ sân chơi Đấu trường VioEdu theo Kế hoạch 01/KH-TCM; giáo viên phụ trách khối chủ động cấp tài khoản, đôn đốc học sinh tham gia vòng sơ loại từ ngày 28/9/2026; Thầy Dương Quang Tùng quản lý tốt phòng máy mở cửa ngoài giờ hỗ trợ học sinh có hoàn cảnh khó khăn.", indent=True)
    add_paragraph_styled(doc, "4. Áp dụng đồng bộ giải pháp tháo gỡ điểm nghẽn SGK Toán 6 và Toán 8 đã được tổ thống nhất (phiếu hướng dẫn vẽ hình từng bước, bảng so sánh 7 hình phẳng, khai thác phản ví dụ tránh ngụy biện hình thang cân).", indent=True)
    add_paragraph_styled(doc, "5. Tổ trưởng chuyên môn tổng hợp các kiến nghị chính đáng của tổ (hạ thấp tivi cơ sở 2, mua sắm compa bảng, rà soát phân lớp tiếng Anh tăng cường) để trực tiếp đề xuất với Ban Giám hiệu nhà trường trong cuộc họp giao ban đầu tuần tới.", indent=True)
    
    add_paragraph_styled(doc, "**Biểu quyết:** 10/10 thành viên trong tổ (100%) giáo viên nhất trí hoàn toàn với nội dung cuộc họp.", indent=True)
    add_paragraph_styled(doc, "Biên bản được thông qua trước tập thể và kết thúc vào lúc 16 giờ 00 phút cùng ngày./.", indent=True)
    
    # Chữ ký 2 bên
    add_signatures(
        doc,
        left_title="THƯ KÝ CUỘC HỌP",
        left_name="Lê Thị Bình",
        right_title="TỔ TRƯỞNG CHUYÊN MÔN",
        right_name="Hoàng Tấn Thiên"
    )
    
    # Bảng ký xác nhận của các thành viên khác
    p_mem_head = doc.add_paragraph()
    p_mem_head.paragraph_format.space_before = Pt(12)
    p_mem_head.paragraph_format.space_after = Pt(4)
    r_mh = p_mem_head.add_run("CÁC THÀNH VIÊN TRONG TỔ KÝ TÊN XÁC NHẬN")
    r_mh.font.name = 'Times New Roman'
    r_mh.font.size = Pt(13)
    r_mh.bold = True
    p_mem_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    tbl_ack = doc.add_table(rows=3, cols=4)
    tbl_ack.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_borders_closed(tbl_ack)
    
    ack_names = [
        ["Đinh Văn Đông", "Hồ Đăng Danh", "Hoàng Xuân Ánh", "Trần Long Hải"],
        ["Nguyễn Văn Tính", "Dương Quang Tùng", "Trần Sáng", "Nguyễn Thị Thảo"]
    ]
    
    # Hàng 1
    for c_idx in range(4):
        cell = tbl_ack.cell(0, c_idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"**{ack_names[0][c_idx]}**\n\n*(Ký tên)*")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    # Hàng 2
    for c_idx in range(4):
        cell = tbl_ack.cell(1, c_idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"**{ack_names[1][c_idx]}**\n\n*(Ký tên)*")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    save_docx_robust(doc, out_docx_path)
    
    if out_md_path:
        tao_bien_ban_hop_to_lan_2_thang_9_md(out_md_path)


def tao_bien_ban_hop_to_lan_2_thang_9_md(out_md_path):
    md_content = """# BIÊN BẢN SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 9/2026 (LẦN 2)
**Trường THCS Trần Phú – Tổ Toán - Tin**  
**Số: 03/BB-TCM**  
*Xuân Đông, ngày 18 tháng 9 năm 2026*

---

Hôm nay, vào lúc 13 giờ 30 phút, ngày 18 tháng 9 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 2 tháng 9 năm học 2026 - 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).
  + *Danh sách thành viên:* Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

### NỘI DUNG CUỘC HỌP

## I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN

Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt sâu sắc các văn bản chỉ đạo của Sở Giáo dục và Đào tạo thành phố Đồng Nai, các cấp quản lý và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:

**1. Hướng dẫn một số giải pháp hạn chế việc sử dụng điện thoại di động, thiết bị thông minh, mạng xã hội của học sinh trong trường học (Hướng dẫn số 5351/HD-SGDĐT ngày 15/9/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Căn cứ Thông tư 15/2026/TT-BGDĐT và Công văn 3147/BGDĐT-HSSV của Bộ GD&ĐT. Nhằm giảm thiểu sự phụ thuộc quá mức vào thiết bị công nghệ, tạo không gian học tập tập trung, cải thiện khả năng tư duy độc lập và bảo vệ sức khỏe học đường (thị lực, cột sống, sức khỏe tâm thần) cho học sinh. Học sinh phấn đấu thực hiện bốn tiêu chuẩn “Tự”: *Tự giác* (tắt thiết bị hoặc để chế độ im lặng và cất vào nơi quy định ngay khi bước vào trường/lớp); *Tự quản* (thành lập tổ tự quản nhắc nhở nhau); *Tự rèn* (làm chủ hành vi, không để bị cuốn vào mạng xã hội); *Tự chủ* (sử dụng công nghệ đúng lúc, đúng chỗ phục vụ học tập). Triển khai đồng bộ 03 mô hình vận dụng linh hoạt: (1) Mô hình *“Hộp lưu trữ niềm tin”* (bố trí tủ/khay/túi chuyên dụng tại lớp, học sinh cất thiết bị đầu buổi và nhận lại sau buổi học); (2) Mô hình *“Giờ ra chơi không màn hình”* (tổ chức cờ vua, trò chơi dân gian, góc đọc sách xanh); (3) Mô hình *“Tích hợp giáo dục kỹ năng số”* (hướng dẫn lọc thông tin, bảo mật cá nhân, ứng xử văn minh trên không gian mạng).
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Giáo viên bộ môn Toán và Tin học làm gương, tuyệt đối không sử dụng điện thoại làm việc riêng trong giờ lên lớp. Phân định rõ ràng: Trong giờ học lý thuyết Toán và Tin học, học sinh tuyệt đối không dùng điện thoại; chỉ khi có yêu cầu nghiệp vụ bài dạy rõ ràng (tra cứu phần mềm GeoGebra, làm bài kiểm tra trực tuyến OLM/VioEdu tại phòng máy hoặc theo nhóm có kiểm soát) thì giáo viên mới cho phép mở thiết bị. Giáo viên chủ nhiệm phối hợp chặt chẽ với cha mẹ học sinh để thống nhất quản lý, phòng ngừa bắt nạt mạng và xao nhãng học tập.

**2. Kế hoạch thực hiện nhiệm vụ ứng dụng công nghệ thông tin, chuyển đổi số và thống kê giáo dục năm học 2026 – 2027 (Kế hoạch số 5264/KH-SGDĐT ngày 22/9/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Bám sát Công văn 6020/BGDĐT-KHCNTT của Bộ GD&ĐT, Nghị quyết 57-NQ/TW của Bộ Chính trị, Luật Chuyển đổi số số 148/2025/QH15, Luật Dữ liệu số 60/2024/QH15, Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 và Luật Trí tuệ nhân tạo số 134/2025/QH15. Chỉ đạo xuyên suốt theo tinh thần **“6 rõ”** (*rõ người, rõ việc, rõ thời gian, rõ trách nhiệm, rõ sản phẩm, rõ thẩm quyền*). Dữ liệu giáo dục phải bảo đảm *“đúng, đủ, sạch, sống, thống nhất, dùng chung”*; thực hiện nghiêm nguyên tắc *“dữ liệu cập nhật một lần, sử dụng nhiều lần”*, cắt giảm thủ tục hành chính. Đẩy mạnh phong trào *“Bình dân học vụ số”* và hưởng ứng Ngày Chuyển đổi số Quốc gia (10/10). Định hướng rõ việc thúc đẩy ứng dụng Trí tuệ nhân tạo (AI) an toàn, có kiểm soát và có trách nhiệm: Khuyến khích ứng dụng AI hỗ trợ soạn bài, xây dựng học liệu, thiết kế đề kiểm tra; tuy nhiên *kết quả do AI tạo ra phải được giáo viên kiểm chứng về tính chính xác và phù hợp sư phạm; AI tuyệt đối không thay thế trách nhiệm chuyên môn và quyền ra quyết định của nhà giáo*.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ Toán - Tin là đơn vị nòng cốt triển khai chuyển đổi số trong nhà trường; 100% giáo viên hoàn thành phê duyệt Kế hoạch bài dạy (KHBD) trên hệ thống số CSDL ngành đúng thời hạn; đảm bảo an toàn dữ liệu học bạ số và thông tin cá nhân học sinh; giáo viên Tin học chủ động tham mưu nâng cấp đường truyền và bảo đảm an ninh mạng cho hệ thống phòng máy.

**3. Hướng dẫn việc trả và lưu trữ đề, bài kiểm tra, đánh giá định kỳ của học sinh (Công văn số 946/SGDĐT-GDPT&GDTX ngày 06/02/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Hướng dẫn thực hiện thống nhất quy trình trả bài và lưu trữ hồ sơ, ma trận, đặc tả, đề kiểm tra cùng bài kiểm tra, đánh giá định kỳ của học sinh bảo đảm tính chính xác, công bằng, minh bạch và đúng quy định quản lý hồ sơ chuyên môn trong nhà trường.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn thẩm định kỹ lưỡng ma trận và đề kiểm tra định kỳ các khối 6, 7, 8, 9; giáo viên thực hiện nghiêm túc quy trình chấm, trả bài có lời nhận xét cụ thể, vào điểm đúng tiến độ trên hệ thống quản lý điểm số và lưu trữ hồ sơ kiểm tra đầy đủ phục vụ kiểm tra chuyên môn.

**4. Hướng dẫn công tác kiểm tra nội bộ trường học năm học 2026 - 2027 (Công văn số 4794/SGD ngày 09/9/2026 của Sở GD&ĐT):**
- **Ý chính cốt lõi:** Xác định mục đích, yêu cầu và quy trình tổ chức kiểm tra nhằm nâng cao hiệu quả quản trị, phòng ngừa và chấn chỉnh kịp thời các sai phạm; triển khai 06 cuộc kiểm tra chuyên đề định kỳ cùng các đợt kiểm tra đột xuất đối với toàn thể cán bộ, giáo viên, nhân viên; tập trung quy chế chuyên môn, hoạt động sư phạm, quản lý dạy thêm - học thêm, thu chi tài chính, an toàn trường học và đánh giá xếp loại học sinh.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Giáo viên trong tổ chấp hành nghiêm chỉnh quy định về dạy thêm - học thêm (tuyệt đối không dạy thêm sai quy định); thực hiện đúng kế hoạch kiểm tra nội bộ của trường; Thầy Trần Sáng tham gia tổ kiểm tra nội bộ thực hiện đúng nhiệm vụ được giao.

**5. Kế hoạch tổ chức sân chơi “Đấu trường VioEdu” năm học 2026 - 2027 (Kế hoạch số 01/KH-TCM ngày 15/9/2026 của Tổ Toán - Tin học Trường THCS Trần Phú):**
- **Ý chính cốt lõi & Quy chế thi:** Mục tiêu thúc đẩy chuyển đổi số, ứng dụng AI và khơi dậy đam mê Toán học, Toán tiếng Anh cho học sinh từ khối 6 đến khối 9 trên tinh thần tự nguyện 100%, hoàn toàn miễn phí. Học sinh thi trực tuyến trên website vio.edu.vn hoặc app VioEdu bằng 01 tài khoản định danh do nhà trường cấp. Mỗi vòng thi gồm 30 câu hỏi (20 câu Toán + 10 câu Toán tiếng Anh), thời gian làm bài cố định 20 phút.
- **Lộ trình thời gian thực hiện:** (1) Ngày 15/9 – 20/9/2026: Khởi tạo và cấp tài khoản đồng loạt; (2) Ngày 28/9 – 13/12/2026: Vòng sơ loại trực tuyến (8 vòng sơ loại và 2 vòng định kỳ, mở từ 00h00 thứ Hai đến 23h59 Chủ nhật hàng tuần); (3) Ngày 11/01 – 15/01/2027: Vòng cấp Trường (thi tập trung tại phòng máy); (4) Ngày 23/02 – 24/02/2027: Vòng cấp Xã; (5) Ngày 30/03 – 31/03/2027: Vòng cấp Tỉnh (dành cho thí sinh đạt từ 20 điểm trở lên và nằm trong Top 30% cấp Xã).
- **Phân công phụ trách khối:** Cô Nguyễn Thị Thảo (Khối 6), Thầy Hoàng Xuân Ánh (Khối 7), Cô Lê Thị Bình (Khối 8), Thầy Trần Sáng (Khối 9), Thầy Dương Quang Tùng (Phụ trách phòng máy và đường truyền mạng). Giáo viên phụ trách khối định kỳ báo cáo kết quả tham gia cho Tổ trưởng chuyên môn vào ngày 25 hàng tháng.

## II. ĐÁNH GIÁ TÌNH HÌNH CÔNG TÁC THỜI GIAN QUA

### **1. Công tác chủ nhiệm:**
- Các giáo viên chủ nhiệm trong tổ đã nhanh chóng ổn định nề nếp lớp chủ nhiệm, tích cực duy trì sinh hoạt 15 phút đầu giờ trước buổi học, hướng dẫn học sinh học tập nội quy, củng cố đội ngũ cán bộ lớp, tham gia họp GVCN và xây dựng kế hoạch chủ nhiệm năm học 2026 - 2027.
- Phát động sôi nổi các phong trào thi đua chào mừng ngày Quốc khánh 2/9, Tháng An toàn giao thông; cho học sinh và cha mẹ học sinh ký cam kết: Không thử, không tàng trữ, không sử dụng và buôn bán các chất ma túy, thuốc lá điện tử và chấp hành nghiêm chỉnh luật giao thông.
- GVCN tăng cường bám sát lớp, theo dõi chuyên cần, quản lý sổ đầu bài cẩn thận, yêu cầu GVBM ghi chép đầy đủ các cột mục và GVCN tổng hợp ký duyệt hàng tuần. Hoàn thành điều tra thông tin học sinh lớp chủ nhiệm trên hệ thống CSDL ngành. Tổ chức họp cha mẹ học sinh đầu năm học vào ngày 13/9/2026 đạt kết quả tốt, thông báo các khoản thu BHYT, BHTN và triển khai đăng ký môn Tiếng Anh tăng cường.

### **2. Ngày giờ công và kỷ luật lao động:**
- 100% giáo viên trong tổ đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ các hoạt động của nhà trường, dạy đủ các tiết theo phân công chuyên môn, thực hiện nghiêm túc việc dạy bù, dạy thay khi có giáo viên đi công tác hoặc nghỉ ốm.

### **3. Công tác chuyên môn:**
- Duy trì nền nếp dạy và học ổn định theo thời khóa biểu. Thực hiện chương trình theo kế hoạch nhà trường, thực hiện dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT, thực hiện giáo dục địa phương và hoạt động trải nghiệm hướng nghiệp đúng định hướng. Giáo viên trong tổ khai thác tốt trang thiết bị dạy học và phòng bộ môn.
- Tổ đã phân công phụ trách khối, đóng góp ý kiến xây dựng Kế hoạch giáo dục của tổ và nhà trường. Thực hiện nghiêm túc các quy chế chuyên môn.
- 100% giáo viên trong tổ hoàn thành đợt tập huấn chuyển đổi số ngày 11/9/2026 về CSDL ngành, eNetViet, OLM, phương pháp tích hợp Năng lực số (NLS 20%) và Khung 12 tiết AI vào bài giảng.

### **4. Công tác chuyên đề, thao giảng:**
- Tham gia đầy đủ các buổi tập huấn chuyên đề do các cấp tổ chức và phổ biến lại các nội dung thống nhất để thực hiện. Giáo viên trong tổ đã tiến hành đăng ký chuyên đề nghiên cứu bài học cho năm học.

### **5. Công tác kiểm tra nội bộ:**
- Thường xuyên kiểm tra việc giáo viên thực hiện quy chế chuyên môn, nền nếp ra vào lớp, chất lượng soạn giảng Kế hoạch bài dạy theo đúng khung hướng dẫn.

### **6. Sử dụng đồ dùng dạy học và phòng chức năng:**
- Khai thác có hiệu quả phòng máy tính, phòng học bộ môn. Giáo viên tiếp tục rà soát, đề xuất mua sắm bổ sung thiết bị dạy học, sách tham khảo phục vụ nhu cầu giảng dạy.

### **7. Công tác khác:**
- Phối hợp tốt trong công tác phòng chống các loại tội phạm, phòng chống đuối nước; tham gia tích cực các hoạt động Đoàn – Đội và hoàn thành tốt nhiệm vụ điều tra phổ cập giáo dục theo phân công.

## III. KẾ HOẠCH TRỌNG TÂM TRONG THỜI GIAN TỚI

### **1. Công tác chủ nhiệm:**
- Tiếp tục ổn định nền nếp lớp chủ nhiệm, tích cực sinh hoạt 15 phút đầu giờ. Phát động đợt thi đua cao điểm chào mừng các ngày lễ lớn trong tháng 10: Ngày Quốc tế Người cao tuổi (01/10), Ngày Khuyến học Việt Nam (02/10), Ngày Bác Hồ gửi bức thư cuối cùng cho ngành Giáo dục (15/10) và Ngày Phụ nữ Việt Nam (20/10). Đẩy mạnh tuyên truyền phòng chống ma túy, ATGT, PCCC và phòng tránh tai nạn thương tích.
- Thực hiện hiệu quả Tuần lễ hưởng ứng học tập suốt đời năm 2026. Hoàn thành hồ sơ sổ sách GVCN đúng quy định; tiếp tục rà soát, thống kê học sinh có hoàn cảnh khó khăn để kịp thời hỗ trợ; đôn đốc thu nộp BHYT, BHTN; thông tin thường xuyên với phụ huynh qua Zalo lớp và sổ liên lạc điện tử.
- Giáo viên chủ nhiệm vận động 100% học sinh đăng ký tham gia Đấu trường VioEdu theo kế hoạch; triển khai khai thác thư viện số của trường và đăng ký học Tiếng Anh tăng cường theo chủ trương.

### **2. Đảm bảo ngày giờ công và nền nếp chuyên môn:**
- Giáo viên trong tổ phấn đấu đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ các hoạt động của trường, dạy đúng, dạy đủ các tiết theo phân công; thực hiện nghiêm túc việc dạy bù, dạy thay kịp thời.

### **3. Hoạt động chuyên môn trọng tâm:**
- Thực hiện nghiêm túc việc soạn Kế hoạch bài dạy (KHBD) từ tuần 1 đến tuần 4 và hoàn thành phê duyệt, đẩy lên hệ thống CSDL ngành trong khoảng thời gian từ ngày 20/9 đến ngày 24/9/2026. Lưu ý thể hiện rõ nét nội dung giáo dục học sinh hòa nhập, tích hợp Năng lực số (NLS 20%), ứng dụng AI có kiểm soát và bài học STEM.
- Phân công nhiệm vụ cụ thể hướng dẫn học sinh tham gia các vòng thi VioEdu đạt hiệu quả: Cô Nguyễn Thị Thảo (Khối 6), Thầy Hoàng Xuân Ánh (Khối 7), Cô Lê Thị Bình (Khối 8), Thầy Trần Sáng (Khối 9), Thầy Dương Quang Tùng (Phòng máy & đường truyền).
- Thầy Trần Sáng tiếp tục hoàn thành bài dự thi về Chuyên môn, nghiệp vụ giáo dục phòng, chống ma túy đạt chất lượng cao.
- **Tập trung góp ý chuyên sâu chương trình Sách giáo khoa GDPT 2018 môn Toán - Tin, nhận diện các khó khăn sư phạm và thống nhất hướng khắc phục:**
  - *Đối với sách giáo khoa Toán lớp 8 (Bài 12: Hình thang cân):*
    - **Khó khăn thực tế:** Học sinh rất dễ ngụy biện và mặc định sai lầm rằng “Hình thang có 2 cạnh bên bằng nhau là hình thang cân” (trong khi nếu 2 cạnh bên bằng nhau và song song thì đó lại là hình bình hành). Việc chứng minh Định lý 3 (Ví dụ 2 trang 54) đòi hỏi kẻ thêm đường phụ khá phức tạp so với trình độ đầu năm lớp 8.
    - **Hướng khắc phục:** Khai thác triệt để phần “Tranh luận” (trang 59) và “Luyện tập chung” (trang 56) để cho học sinh vẽ cả 2 trường hợp (hai cạnh bên không song song -> hình thang cân; hai cạnh bên song song -> hình bình hành). Chuẩn hóa quy trình kẻ đường song song phụ qua một đỉnh để đưa bài toán về tam giác cân quen thuộc.
  - *Đối với sách giáo khoa Toán lớp 6 (Bài 18 và Bài 19 về các hình phẳng trong thực tiễn):*
    - **Khó khăn thực tế:** Học sinh gặp khó khăn lớn khi sử dụng compa và êke để vẽ các hình đòi hỏi kỹ thuật cao như hình lục giác đều hay hình thoi. Bên cạnh đó, học sinh rất dễ nhầm lẫn thuộc tính đường chéo giữa các hình (ví dụ: nhầm đường chéo bằng nhau của hình chữ nhật/hình thang cân với đường chéo vuông góc của hình thoi/hình vuông).
    - **Hướng khắc phục:** Xây dựng Quy trình vẽ hình từng bước: Chuẩn bị phiếu học tập có hình ảnh minh họa rõ ràng các bước đặt thước, quay compa để vẽ hình thoi và hình lục giác đều. Cho học sinh lập Bảng so sánh các yếu tố Cạnh - Góc - Đường chéo của 7 hình phẳng đã học để rèn luyện tư duy phân loại thị giác.
- Hoàn thành toàn bộ hồ sơ tổ chuyên môn theo kế hoạch năm học của nhà trường.

### **4. Công tác chuyên đề và nghiên cứu bài học:**
- Các nhóm bộ môn lên kế hoạch thực hiện chuyên đề theo nghiên cứu bài học. Tổ thống nhất và đăng ký phổ biến chuyên đề cấp trường/tổ: Học kỳ I do Thầy Hoàng Tấn Thiên chủ trì (môn Toán); Học kỳ II do Thầy Hoàng Tấn Thiên và Thầy Trần Sáng phối hợp triển khai (môn Toán). Tham gia đầy đủ các buổi tập huấn chuyên đề do các cấp tổ chức.

### **5. Công tác ngoại khóa và phong trào:**
- Tuyên truyền học sinh chấp hành tốt nội quy trường, lớp, tích cực tham gia các cuộc thi do Nhà trường, Đoàn, Đội tổ chức; duy trì phong trào vệ sinh “Sạch trường, đẹp lớp”.

### **6. Công tác kiểm tra:**
- Kiểm tra nền nếp ra vào lớp, duyệt ma trận và đề kiểm tra định kỳ của tổ; kiểm tra việc soạn giảng, ra đề theo chuẩn KT-KN chương trình GDPT 2018 và kiểm tra việc thực hiện quy chế chuyên môn, sử dụng phòng CNTT.

### **7. Sử dụng đồ dùng dạy học và phòng CNTT:**
- Sử dụng có hiệu quả phòng chức năng, phòng CNTT, khai thác triệt để các phần mềm trong giảng dạy; khuyến khích giáo viên và học sinh ươm mầm các ý tưởng sản phẩm dự thi KHKT.

### **8. Công tác khác:**
- Vệ sinh trường lớp, trang trí lớp Xanh – Sạch – Đẹp; tham gia hoạt động Đoàn – Đội và các hoạt động do nhà trường, công đoàn phát động chào mừng các ngày lễ lớn trong tháng.

## IV. Ý KIẾN THẢO LUẬN VÀ GIẢI PHÁP CHUYÊN MÔN THỰC CHIẾN

Phiên họp diễn ra thẳng thắn, dân chủ, tập trung sâu sắc vào các vấn đề chuyên môn, phản ánh đúng thực tế lớp học và đề xuất các giải pháp kỹ thuật cụ thể:

- **Cô Lê Thị Bình (Giáo viên môn Toán 8, Thư ký):** Đánh giá cao tính cấp thiết của Hướng dẫn số 5351/HD-SGDĐT về hạn chế điện thoại trong trường học. Thực tế học sinh lớp 8 rất tò mò và dễ bị phân tâm bởi tin nhắn, mạng xã hội nếu mang điện thoại vào lớp. Đề xuất giải pháp: Mỗi lớp học bố trí 01 khay/túi vải có đánh số thứ tự treo tại góc bảng lớp (Mô hình Hộp lưu trữ niềm tin). Đầu buổi học, ban cán sự lớp đôn đốc học sinh tự giác tắt nguồn hoặc bật chế độ im lặng rồi cất điện thoại vào đúng ô số của mình. Trong giờ học Toán, giáo viên yêu cầu học sinh sử dụng máy tính cầm tay Casio khoa học, tuyệt đối cấm dùng phần mềm giả lập trên điện thoại để tránh việc lén lút chuyển sang ứng dụng mạng xã hội. Giáo viên chủ nhiệm cần thống nhất chặt chẽ với cha mẹ học sinh ngay từ đầu năm.

- **Thầy Hoàng Xuân Ánh (Giáo viên môn Toán 7, Phụ trách VioEdu Khối 7):** Đề nghị Liên đội tăng cường kiểm tra và ghi tên những học sinh không đội nón bảo hiểm khi tham gia giao thông bằng xe đạp điện, xe máy điện ở cổng trường lúc tan học. Về chuyên môn hình học: Đồng tình với giải pháp khắc phục khó khăn vẽ hình lớp 6 và hình thang cân lớp 8. Đối với thao tác vẽ hình phức tạp như lục giác đều, giáo viên nên chiếu video mô phỏng thao tác dựng hình chuẩn bằng phần mềm GeoGebra trước 2 phút, sau đó yêu cầu học sinh thực hành trên phiếu in sẵn lưới ô vuông để định hình tỷ lệ chuẩn trước khi vẽ vào vở.

- **Thầy Dương Quang Tùng (Giáo viên Tin học, Phụ trách phòng máy & hạ tầng CNTT):** Báo cáo hạ tầng CNTT: 2 phòng máy tính (45 máy) hiện hoạt động ổn định. Để triển khai tốt Kế hoạch số 5264/KH-SGDĐT và sân chơi VioEdu, Thầy Tùng đề xuất mở cửa phòng máy từ 16h30 đến 17h15 vào các ngày thứ Ba và thứ Năm hàng tuần để tạo điều kiện cho các em học sinh có hoàn cảnh khó khăn (không có máy tính/điện thoại ở nhà) được tham gia thi đấu vòng sơ loại VioEdu miễn phí dưới sự hướng dẫn của giáo viên trực phòng máy. Về việc ứng dụng AI có kiểm soát: Khuyến nghị các thầy cô trong tổ có thể sử dụng các trợ lý AI (như ChatGPT, Claude) để gợi ý các bài toán thực tế, tạo câu hỏi trắc nghiệm khách quan; tuy nhiên phải tuân thủ nghiêm ngặt nguyên tắc kiểm chứng: Giáo viên phải tự tay giải lại, thẩm định lời giải và ma trận đề, tuyệt đối không sao chép nguyên văn sản phẩm của AI đưa vào đề thi hay giáo án.

- **Thầy Hồ Đăng Danh (Giáo viên môn Toán):** Thống nhất bài làm kiểm tra thường xuyên (KTTX) cần thực hiện nhiều hình thức phong phú: vấn đáp, bài viết phiếu học tập, sản phẩm STEM (mô hình tam giác, hình thang cân bằng giấy carton) và đánh giá hoạt động nhóm... nhằm tạo động lực và khích lệ học sinh yếu kém tiến bộ, tránh gây áp lực điểm số đơn thuần bằng bài kiểm tra giấy truyền thống.

- **Cô Nguyễn Thị Thảo (Giáo viên môn Toán 6, Phụ trách VioEdu Khối 6):** Phản ánh ý kiến của phụ huynh học sinh về môn Tiếng Anh tăng cường: Cần khảo sát phân loại học sinh theo trình độ để xếp lớp phù hợp, tránh để học sinh trung bình bị quá tải. Đối với 10 câu hỏi Toán tiếng Anh trong mỗi vòng thi VioEdu, Cô Thảo đề xuất giáo viên giảng dạy khối 6 và khối 7 dành 5 phút cuối tiết luyện tập để hướng dẫn học sinh làm quen với các thuật ngữ Toán học tiếng Anh cốt lõi (như *prime number, common divisor, right triangle, angle, perimeter, area*) giúp học sinh tự tin làm bài mà không bị rào cản ngôn ngữ.

- **Thầy Trần Sáng (Giáo viên môn Toán 9, KTNB):** Đề nghị thiết thực về cơ sở vật chất: Nhà trường cần sớm làm khung giá đỡ hoặc hạ thấp ti vi tại các lớp học ở cơ sở 2. Lý do ti vi hiện nay treo quá cao sát trần nhà khiến học sinh ngồi các dãy giữa và cuối phải ngửa cổ liên tục gây mỏi mắt, không quan sát rõ nét chữ và hình vẽ. Về xử lý sai lầm Hình thang cân lớp 8: Thống nhất giáo viên phải đưa ra phản ví dụ cụ thể ngay trên bảng (vẽ một hình thang có 2 cạnh bên bằng nhau và song song để học sinh tự kết luận đó là hình bình hành, từ đó khắc cốt ghi tâm điều kiện 2 cạnh bên phải *không song song* mới là hình thang cân).

- **Thầy Đinh Văn Đông & Thầy Trần Long Hải:** Đề xuất nhà trường trang cấp bổ sung cho tổ bộ môn 02 bộ compa bảng compozit khổ lớn và thước đo góc có tay cầm chuyên dụng để phục vụ trực quan cho giáo viên dạy hình học các khối 6, 7. Thống nhất mốc thời gian hoàn thành Kế hoạch bài dạy (KHBD) tuần 1 đến tuần 4: 100% giáo viên nộp bài lên hệ thống CSDL ngành trước 17h00 ngày 23/9/2026 để Tổ trưởng chuyên môn kịp thời thẩm định và phê duyệt trước hạn chót 24/9/2026.

## V. KẾT LUẬN CỦA CHỦ TỌA VÀ NGHỊ QUYẾT CUỘC HỌP

Thầy Tổ trưởng chuyên môn Hoàng Tấn Thiên kết luận toàn diện phiên họp và chỉ đạo thực hiện các nhiệm vụ trọng tâm sau:

1. Toàn thể giáo viên quán triệt và thực hiện nghiêm túc Hướng dẫn số 5351/HD-SGDĐT: Triển khai hiệu quả Mô hình “Hộp lưu trữ niềm tin” tại lớp chủ nhiệm và phòng bộ môn; tuyệt đối không để học sinh lạm dụng điện thoại trong giờ học; giáo viên làm gương không sử dụng thiết bị cá nhân làm việc riêng trong tiết giảng.
2. Bám sát tinh thần Kế hoạch số 5264/KH-SGDĐT: Thực hiện nghiêm túc nguyên tắc “6 rõ”, chuẩn hóa dữ liệu CSDL ngành theo phương châm “đúng, đủ, sạch, sống”; hoàn thành việc phê duyệt và nộp KHBD tuần 1 đến tuần 4 lên CSDL ngành đúng thời hạn (hạn chót hoàn thành của giáo viên là ngày 23/9/2026); ứng dụng AI một cách thông minh, có trách nhiệm và luôn kiểm chứng tính chính xác chuyên môn.
3. Triển khai sâu rộng và đồng bộ sân chơi Đấu trường VioEdu theo Kế hoạch 01/KH-TCM; giáo viên phụ trách khối chủ động cấp tài khoản, đôn đốc học sinh tham gia vòng sơ loại từ ngày 28/9/2026; Thầy Dương Quang Tùng quản lý tốt phòng máy mở cửa ngoài giờ hỗ trợ học sinh có hoàn cảnh khó khăn.
4. Áp dụng đồng bộ giải pháp tháo gỡ điểm nghẽn SGK Toán 6 và Toán 8 đã được tổ thống nhất (phiếu hướng dẫn vẽ hình từng bước, bảng so sánh 7 hình phẳng, khai thác phản ví dụ tránh ngụy biện hình thang cân).
5. Tổ trưởng chuyên môn tổng hợp các kiến nghị chính đáng của tổ (hạ thấp tivi cơ sở 2, mua sắm compa bảng, rà soát phân lớp tiếng Anh tăng cường) để trực tiếp đề xuất với Ban Giám hiệu nhà trường trong cuộc họp giao ban đầu tuần tới.

- **Biểu quyết:** 10/10 thành viên trong tổ (100%) giáo viên nhất trí hoàn toàn với nội dung cuộc họp.
- Biên bản được thông qua trước tập thể và kết thúc vào lúc 16 giờ 00 phút cùng ngày./.

---

<table style="width: 100%; border: none;">
<tr>
<td style="width: 50%; text-align: center; vertical-align: top;">
<strong>THƯ KÝ CUỘC HỌP</strong><br>
<em>(Ký và ghi rõ họ tên)</em><br><br><br><br>
<strong>Lê Thị Bình</strong>
</td>
<td style="width: 50%; text-align: center; vertical-align: top;">
<strong>TỔ TRƯỞNG CHUYÊN MÔN</strong><br>
<em>(Ký và ghi rõ họ tên)</em><br><br><br><br>
<strong>Hoàng Tấn Thiên</strong>
</td>
</tr>
</table>

<div align="center">

### CÁC THÀNH VIÊN TRONG TỔ KÝ TÊN XÁC NHẬN

</div>

| Đinh Văn Đông | Hồ Đăng Danh | Hoàng Xuân Ánh | Trần Long Hải |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |

| Nguyễn Văn Tính | Dương Quang Tùng | Trần Sáng | Nguyễn Thị Thảo |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Da xuat thanh cong file Markdown: {out_md_path}")


def tao_bien_ban_hop_to_lan_1_thang_10(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 1 Tháng 10/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # 1. Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="04/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 03 tháng 10 năm 2026"
    )
    
    # 2. Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1",
        "SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 10/2026 (LẦN 1)\nNăm học: 2026 - 2027"
    )
    
    # 3. Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 07 giờ 30 phút, ngày 03 tháng 10 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 10 năm học 2026 - 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # 4. NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt sâu sắc các văn bản chỉ đạo của Sở Giáo dục và Đào tạo thành phố Đồng Nai, các cấp quản lý và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:", indent=True)
    
    # 1. Công văn 5529
    add_paragraph_styled(doc, "**1. Hướng dẫn tổ chức kiểm tra, đánh giá học sinh phổ thông và học viên giáo dục thường xuyên năm học 2026 - 2027 (Công văn số 5529/SGDĐT-GDPT&GDTX ngày 28/9/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Quán triệt thực hiện nghiêm túc quy định đổi mới phương pháp kiểm tra, đánh giá định kỳ và thường xuyên theo định hướng phát triển phẩm chất, năng lực học sinh. Xây dựng ma trận, bản đặc tả chi tiết bảo đảm đúng tỷ lệ 4 mức độ nhận thức (Nhận biết 40%, Thông hiểu 30%, Vận dụng 20%, Vận dụng cao 10%); đề kiểm tra bám sát chuẩn kiến thức, kỹ năng chương trình GDPT 2018, bảo đảm tính khách quan, công bằng và phân hóa tốt đối tượng học sinh; đa dạng hóa hình thức đánh giá (trên giấy kết hợp trực tuyến).", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phân công cụ thể giáo viên ra đề cương, ma trận, bản đặc tả và đề kiểm tra giữa kỳ 1 môn Toán (khối 6, 7, 8, 9) và môn Tin học; thực hiện nghiêm túc quy trình phản biện chéo và nộp đề đúng hạn quy định.", indent=True)
    
    # 2. Công văn 3939
    add_paragraph_styled(doc, "**2. Thực hiện Đề án “Tăng cường giảng dạy Tiếng Anh trong các trường phổ thông trên địa bàn tỉnh Đồng Nai” (Công văn số 3939/SGDĐT-NV1 ngày 26/9/2023 của Sở GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Tăng cường lồng ghép các thuật ngữ Tiếng Anh chuyên ngành vào bài giảng chính khóa môn Toán và môn Tin học; khích lệ giáo viên tổ chức các hoạt động ngoại khóa, câu lạc bộ học thuật và sân chơi trí tuệ có yếu tố Tiếng Anh.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tích hợp các câu hỏi Tiếng Anh Toán học vào Chuyên đề Ngoại khóa “Rung chuông vàng” khối 6; hướng dẫn học sinh tiếp cận phần thi Toán Tiếng Anh trong Đấu trường VioEdu; phối hợp quản lý tốt các lớp Tiếng Anh giao tiếp do giáo viên nước ngoài trực tiếp giảng dạy 2 tiết/tuần.", indent=True)
    
    # 3. Quy định dạy thêm, học thêm
    add_paragraph_styled(doc, "**3. Quy định về quản lý dạy thêm, học thêm (Quyết định số 25/2025/QĐ-UBND ngày 14/8/2025; Quyết định sửa đổi số 59/2026/QĐ-UBND ngày 16/7/2026 của UBND thành phố Đồng Nai; Văn bản hợp nhất số 01/2026/VBHN-QĐ-UBND ngày 22/8/2026 và Công văn số 5473/SGDĐT-GDPT&GDTX ngày 25/9/2026 của Sở GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Quán triệt tinh thần chấn chỉnh, tăng cường kỷ cương quản lý dạy thêm, học thêm trên địa bàn thành phố. Tuyệt đối không tổ chức dạy thêm, học thêm trái quy định dưới bất kỳ hình thức nào; không ép buộc, gợi ý phụ huynh và học sinh tham gia học thêm; nghiêm cấm việc cắt giảm nội dung bài học chính khóa để đưa vào dạy thêm; toàn thể giáo viên ký cam kết chấp hành nghiêm túc quy định pháp luật và giữ gìn đạo đức nhà giáo.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** 100% giáo viên trong tổ Toán – Tin ký cam kết không vi phạm quy định dạy thêm, học thêm; tập trung nâng cao chất lượng từng giờ dạy chính khóa trên lớp và phụ đạo học sinh còn hổng kiến thức miễn phí theo kế hoạch giáo dục của nhà trường.", indent=True)
    
    # 4. Kế hoạch thi HSG
    add_paragraph_styled(doc, "**4. Kế hoạch Tổ chức Kỳ thi chọn học sinh giỏi cấp thành phố năm học 2026 - 2027 (Kế hoạch số 4706/KH-SGDĐT ngày 08/9/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Kế hoạch tuyển chọn và tổ chức kỳ thi học sinh giỏi THCS cấp thành phố nhằm phát hiện, bồi dưỡng các tài năng trẻ môn Toán và Tin học.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn chủ động rà soát, tuyển chọn các nhân tố xuất sắc khối 8 và khối 9, phân công giáo viên có kinh nghiệm phụ trách bồi dưỡng đội tuyển Toán 9 và Tin học 9 nhằm nâng cao chất lượng mũi nhọn của trường.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ CÔNG TÁC CHUYÊN MÔN CUỐI THÁNG 9/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm đã ổn định vững chắc nề nếp lớp, duy trì nghiêm túc sinh hoạt 15 phút đầu giờ trước buổi học, quản lý tốt chuyên cần và nền nếp trật tự.", indent=True)
    add_paragraph_styled(doc, "- Bám sát lớp, thực hiện các loại báo cáo kịp thời; hoàn thành thu nộp BHYT, BHTN đợt 1; triển khai chương trình Tiếng Anh tăng cường đến phụ huynh; hoàn thành 100% cập nhật thông tin học sinh lớp chủ nhiệm trên hệ thống CSDL ngành.", indent=True)
    add_paragraph_styled(doc, "- Tích cực vận động học sinh tham gia Đấu trường VioEdu, triển khai thư viện số; phối hợp trợ giảng trong các tiết Tiếng Anh giao tiếp với giáo viên nước ngoài (2 tiết/tuần theo năng lực) bảo đảm hiệu quả.", indent=True)
    
    add_section_h2(doc, "2. Ngày giờ công và kỷ luật lao động:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ đảm bảo ngày giờ công nghiêm túc, tham gia đầy đủ các hoạt động hội họp của nhà trường, dạy đủ số tiết theo phân công chuyên môn; thực hiện chu đáo việc dạy bù, dạy thay khi có giáo viên đi công tác hoặc nghỉ ốm.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn và thực hiện quy chế:")
    add_paragraph_styled(doc, "- Ổn định nền nếp dạy và học theo đúng thời khóa biểu; thực hiện chương trình theo kế hoạch giáo dục nhà trường, dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT, dạy học giáo dục địa phương, GDNGLL và HĐTN đúng định hướng.", indent=True)
    add_paragraph_styled(doc, "- **Về hồ sơ sổ sách và Kế hoạch bài dạy (KHBD):**", indent=True)
    add_paragraph_styled(doc, "  + *Ưu điểm:* Đa số giáo viên trong tổ đã có ý thức chuẩn bị hồ sơ bài dạy đầy đủ theo phân phối chương trình, bảo đảm cấu trúc 4 hoạt động theo tinh thần Công văn 5512/BGDĐT-GDTrH.", indent=True)
    add_paragraph_styled(doc, "  + *Tồn tại, hạn chế cần khắc phục ngay:* Qua đợt kiểm tra hồ sơ bài dạy tháng 9, một số giáo viên thực hiện chưa đúng biểu mẫu quy định. Cụ thể: Kế hoạch bài dạy còn mắc lỗi định dạng công thức toán học, biến dạng ký hiệu góc hình học; các chỉ báo năng lực số (NLS) và trí tuệ nhân tạo (AI) chưa được định dạng in đậm, in nghiêng theo quy định; một số bài soạn chưa đồng bộ Header/Footer theo mẫu chung của nhà trường. Yêu cầu các thầy cô khẩn trương rà soát, chỉnh sửa hoàn thiện trước đợt kiểm tra tiếp theo.", indent=True)
    add_paragraph_styled(doc, "- **Về nền nếp giảng dạy và thực hiện quy chế chuyên môn:**", indent=True)
    add_paragraph_styled(doc, "  + Chấp hành nghiêm túc quy chế chuyên môn, lên lớp đúng giờ, quản lý học sinh tốt trong các tiết học; tuyệt đối không tự ý đổi tiết, bỏ tiết khi chưa có sự phê duyệt của Tổ trưởng và Ban Giám hiệu.", indent=True)
    add_paragraph_styled(doc, "  + Thực hiện ghi chép Sổ đầu bài đầy đủ, sạch sẽ, khớp 100% với tiến độ phân phối chương trình và Kế hoạch giáo dục của tổ (Phụ lục 3).", indent=True)
    add_paragraph_styled(doc, "  + Công tác kiểm tra đánh giá thường xuyên: Giáo viên các bộ môn đã chủ động kiểm tra theo tiến độ, vào điểm và cập nhật kịp thời trên phần mềm quản lý điểm của trường.", indent=True)
    add_paragraph_styled(doc, "  + Nền nếp phòng học bộ môn: Giáo viên Tin học duy trì nền nếp phòng máy vi tính nghiêm túc, hướng dẫn học sinh thực hiện đúng nội quy phòng máy, bảo đảm an toàn thiết bị điện và bảo quản máy móc phục vụ giảng dạy.", indent=True)
    
    # Bảng xếp loại hồ sơ chuyên môn tháng 9
    add_paragraph_styled(doc, "- **Kết quả xếp loại hồ sơ chuyên môn tháng 9/2026:**", indent=True)
    
    ratings_data = [
        ("STT", "Họ và tên giáo viên", "Môn giảng dạy", "Số tiết nộp", "Xếp loại tháng 9"),
        ("1", "Hoàng Tấn Thiên", "Toán 9, Tin học 6", "Đầy đủ", "Tốt"),
        ("2", "Hồ Đăng Danh", "Toán 6, Toán 9", "Đầy đủ", "Tốt"),
        ("3", "Trần Sáng", "Toán 6, Toán 9", "Đầy đủ", "Tốt"),
        ("4", "Trần Long Hải", "Toán 8", "Đầy đủ", "Khá"),
        ("5", "Nguyễn Thị Thảo", "Toán 6, Toán 7", "Đầy đủ", "Khá"),
        ("6", "Lê Thị Bình", "Toán 7, Toán 8, HĐTN", "Đầy đủ", "Khá"),
        ("7", "Hoàng Xuân Ánh", "Toán 7, HĐTN 6", "Đầy đủ", "Khá"),
        ("8", "Nguyễn Văn Tính", "HĐTN 7", "Đầy đủ", "Khá"),
        ("9", "Đinh Văn Đông", "Toán 8", "Đầy đủ", "Khá"),
        ("10", "Dương Quang Tùng", "Tin học 6, 7, 8, 9", "Đầy đủ", "Tốt")
    ]
    
    tbl_rate = doc.add_table(rows=len(ratings_data), cols=5)
    tbl_rate.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_borders_closed(tbl_rate)
    r_widths = [Inches(0.6), Inches(2.2), Inches(2.0), Inches(1.1), Inches(1.19)]
    
    for r_idx, row in enumerate(tbl_rate.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.width = r_widths[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Inches(0)
            
            val = ratings_data[r_idx][c_idx]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.size = Pt(13)
                run.font.bold = True
            else:
                run.font.size = Pt(13)
                if c_idx in (0, 3, 4):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    
    # Kết quả VioEdu vòng 1
    add_paragraph_styled(doc, "- **Tổng hợp số lượng học sinh tham gia thi Đấu trường VioEdu vòng sơ loại 1:** Toàn trường có **107 học sinh** tham gia dự thi. Cụ thể từng khối: Khối 6 đạt 30 học sinh; Khối 7 đạt 24 học sinh; Khối 8 đạt 31 học sinh; Khối 9 đạt 22 học sinh.", indent=True)
    
    add_section_h2(doc, "4. Công tác chuyên đề, thao giảng:")
    add_paragraph_styled(doc, "- Tham gia đầy đủ các buổi tập huấn chuyên môn, chuyên đề do Sở GD&ĐT tổ chức; phổ biến lại trong nhóm bộ môn để triển khai thống nhất.", indent=True)
    
    add_section_h2(doc, "5. Công tác ngoại khóa và phong trào:")
    add_paragraph_styled(doc, "- Đã thực hiện tốt hoạt động GDNGLL theo chủ điểm: Tổ chức Tết Trung thu vui tươi, an toàn cho học sinh; tuyên truyền học sinh chấp hành tốt nội quy trường lớp, tham gia các cuộc thi do Nhà trường và Đoàn - Đội phát động.", indent=True)
    
    add_section_h2(doc, "6. Công tác kiểm tra nội bộ:")
    add_paragraph_styled(doc, "- Kiểm tra nền nếp ra vào lớp, việc thực hiện quy chế chuyên môn, chất lượng soạn giảng và tiến độ thực hiện chương trình.", indent=True)
    
    add_section_h2(doc, "7. Sử dụng thiết bị dạy học và phòng bộ môn:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ sử dụng có hiệu quả phòng thực hành Tin học, phòng học chức năng, khai thác triệt để các phần mềm dạy học phục vụ bài giảng.", indent=True)
    
    add_section_h2(doc, "8. Công tác khác:")
    add_paragraph_styled(doc, "- Tích cực tham gia các phong trào thi đua của Đoàn – Đội, tham gia đầy đủ công tác điều tra phổ cập giáo dục theo phân công của xã.", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. KẾ HOẠCH HOẠT ĐỘNG CHUYÊN MÔN THÁNG 10/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Ổn định nền nếp lớp chủ nhiệm, tích cực sinh hoạt 15 phút đầu giờ. Phát động đợt thi đua cao điểm chào mừng các ngày lễ lớn trong tháng: Ngày Quốc tế Người cao tuổi (01/10), Ngày Khuyến học Việt Nam (02/10), Ngày Bác Hồ gửi bức thư cuối cùng cho ngành Giáo dục (15/10) và Ngày Phụ nữ Việt Nam (20/10). Tuyên truyền phòng chống ma túy, tội phạm, ATGT, PCCC và phòng tránh tai nạn thương tích.", indent=True)
    add_paragraph_styled(doc, "- Thực hiện hiệu quả Tuần lễ học tập suốt đời năm 2026; hoàn thành hồ sơ sổ sách GVCN đúng quy định; tiếp tục rà soát học sinh khó khăn; đôn đốc thu nộp BHYT, BHTN; thông tin thường xuyên qua Zalo lớp.", indent=True)
    add_paragraph_styled(doc, "- Vận động học sinh đăng ký thi VioEdu các vòng tiếp theo; triển khai thư viện số và tiết học thư viện theo thời khóa biểu. Giáo viên bộ môn tích hợp bài dạy STEM (Phụ lục 2) vào Kế hoạch bài dạy theo thời điểm, hướng dẫn học sinh nộp sản phẩm tại phòng STEM.", indent=True)
    
    add_section_h2(doc, "2. Đảm bảo ngày giờ công và nền nếp chuyên môn:")
    add_paragraph_styled(doc, "- Giáo viên phấn đấu đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ hoạt động của trường; dạy đúng, dạy đủ số tiết theo phân công chuyên môn; thực hiện kịp thời việc dạy bù, dạy thay khi có phân công.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn trọng tâm:")
    
    # 3.1. Chuẩn bị kiểm tra nội bộ
    add_paragraph_styled(doc, "*- Chuẩn bị công tác kiểm tra nội bộ nhà trường (Thanh tra toàn diện):*", indent=True)
    add_paragraph_styled(doc, "  + Đối tượng kiểm tra: Thầy **Trần Sáng** (thực hiện theo Kế hoạch kiểm tra nội bộ năm học 2026 - 2027 của Trường THCS Trần Phú).", indent=True)
    add_paragraph_styled(doc, "  + Yêu cầu chuẩn bị: Thầy Sáng chuẩn bị chu đáo toàn bộ hồ sơ chuyên môn cá nhân (Kế hoạch bài dạy chuẩn CV 5512, sổ theo dõi và đánh giá học sinh, kế hoạch dạy học cá nhân, thiết bị và đồ dùng dạy học).", indent=True)
    add_paragraph_styled(doc, "  + Phân công phối hợp: Thầy Sáng chủ động gửi Thời khóa biểu và lịch dạy trong tuần cho Tổ trưởng để tổ sắp xếp báo cáo Ban Giám hiệu, đồng thời phân công giáo viên trong tổ bố trí dự giờ, đóng góp ý kiến mang tính xây dựng chuyên môn.", indent=True)
    
    # 3.2. Kế hoạch Rung chuông vàng
    add_paragraph_styled(doc, "*- Kế hoạch Chuyên đề Ngoại khóa “Rung chuông vàng” môn Toán khối 6:*", indent=True)
    add_paragraph_styled(doc, "Nhằm tạo sân chơi học tập bổ ích, khơi dậy niềm đam mê học Toán và nâng cao kỹ năng vận dụng kiến thức thực tế cho học sinh khối 6, Tổ Toán – Tin thống nhất thành lập Ban Tổ chức và xây dựng tiến độ triển khai chuyên đề ngoại khóa như sau:", indent=True)
    add_paragraph_styled(doc, "• **Thành lập Ban Tổ chức chuyên đề:**", indent=True)
    add_paragraph_styled(doc, "  + Nhóm biên soạn nội dung và ngân hàng đề: Cô Nguyễn Thị Thảo (Chủ đạo, phụ trách khối 6); Cô Lê Thị Bình (Hỗ trợ xây dựng và rà soát câu hỏi).", indent=True)
    add_paragraph_styled(doc, "  + Nhóm tư vấn và thẩm định chuyên môn: Thầy Hoàng Tấn Thiên (Trưởng ban), Thầy Hồ Đăng Danh, Thầy Nguyễn Văn Tính, Thầy Đinh Văn Đông.", indent=True)
    add_paragraph_styled(doc, "  + Nhóm hỗ trợ tổ chức và kỹ thuật - hậu cần: Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Thầy Dương Quang Tùng, Thầy Trần Sáng (chuẩn bị âm thanh, máy chiếu, bảng con, sân bãi).", indent=True)
    add_paragraph_styled(doc, "  + Phân công Cô Nguyễn Thị Thảo rà soát, xây dựng kịch bản chi tiết phù hợp với thực tế nhà trường.", indent=True)
    
    # Bảng tiến độ Rung chuông vàng
    add_paragraph_styled(doc, "• **Lịch trình và tiến độ thực hiện chi tiết (Thực hiện trong tháng 11/2026):**", indent=True)
    
    rcv_data = [
        ("Thời gian", "Nội dung công việc", "Người phụ trách", "Ghi chú / Sản phẩm"),
        ("08/10 – 15/10/2026", "Xây dựng khung thể lệ; biên soạn bộ ngân hàng 35 câu hỏi Toán 6 (30 câu chính, 5 câu phụ; tích hợp câu hỏi thực tiễn và Tiếng Anh Toán học).", "Cô Thảo, Cô Bình", "Bản thảo đề & đáp án"),
        ("16/10 – 22/10/2026", "Họp nhóm tư vấn thẩm định câu hỏi; Tổ trưởng hoàn thiện kế hoạch chi tiết trình BGH phê duyệt; Cô Thảo xem lịch chọn ngày cụ thể.", "Thầy Thiên, Thầy Danh, Thầy Tính, Thầy Đông, Cô Thảo", "Kế hoạch được BGH duyệt"),
        ("23/10 – 31/10/2026", "Thông báo thể lệ đến các lớp khối 6; các lớp lập danh sách học sinh tham gia (15 HS/lớp); nhóm hỗ trợ chuẩn bị bảng con, phấn, chuông, sân bãi.", "Cô Thảo, Thầy Ánh, Thầy Hải, Thầy Tùng, Thầy Sáng", "Danh sách thí sinh & CSVC"),
        ("01/11 – 07/11/2026", "Chạy thử chương trình, kiểm tra hệ thống âm thanh, máy chiếu trình chiếu câu hỏi; phân công dẫn chương trình (MC) và cứu trợ.", "Toàn thể thành viên Ban Tổ chức", "Hoàn tất chuẩn bị"),
        ("Tuần 2 Tháng 11/2026\n(Dự kiến 14/11/2026)", "Tổ chức chính thức Chuyên đề Ngoại khóa “Rung chuông vàng môn Toán khối 6” chào mừng kỷ niệm Ngày Nhà giáo Việt Nam 20/11.", "Tổ Toán – Tin phối hợp Đoàn - Đội", "Tổng kết, trao thưởng")
    ]
    
    tbl_rcv = doc.add_table(rows=len(rcv_data), cols=4)
    tbl_rcv.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_borders_closed(tbl_rcv)
    rcv_widths = [Inches(1.8), Inches(2.6), Inches(1.5), Inches(1.19)]
    
    for r_idx, row in enumerate(tbl_rcv.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.width = rcv_widths[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Inches(0)
            
            val = rcv_data[r_idx][c_idx]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.size = Pt(13)
                run.font.bold = True
            else:
                run.font.size = Pt(12)
                if c_idx in (0, 2, 3):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    
    # 3.3. Ma trận, bản đặc tả, đề kiểm tra Giữa HKI
    add_paragraph_styled(doc, "*- Công tác xây dựng Ma trận, Bản đặc tả, Đề cương và Đề kiểm tra giữa học kỳ 1:*", indent=True)
    add_paragraph_styled(doc, "  + Toàn tổ thực hiện nghiêm túc Công văn số 5529/SGDĐT-GDPT&GDTX của Sở GD&ĐT thành phố Đồng Nai về tổ chức kiểm tra, đánh giá định kỳ.", indent=True)
    add_paragraph_styled(doc, "  + **Yêu cầu chuyên môn:** Ma trận và bản đặc tả phải bám sát nội dung chương trình GDPT 2018, bảo đảm đúng tỉ lệ 4 mức độ nhận thức (Nhận biết 40%, Thông hiểu 30%, Vận dụng 20%, Vận dụng cao 10%). Đề kiểm tra phải bám sát ma trận và đề cương ôn tập, có tính phân hóa phù hợp với đối tượng học sinh.", indent=True)
    add_paragraph_styled(doc, "  + **Phân công phụ trách xây dựng đề cương, ma trận và đề kiểm tra:** Môn Toán khối 6 do Cô Nguyễn Thị Thảo phụ trách; Môn Toán khối 7 do Thầy Hoàng Xuân Ánh phụ trách; Môn Toán khối 8 do Cô Lê Thị Bình phụ trách; Môn Toán khối 9 do Thầy Trần Sáng phụ trách; Môn Tin học (Khối 6, 7, 8, 9) do Thầy Dương Quang Tùng phụ trách.", indent=True)
    add_paragraph_styled(doc, "  + **Hình thức và thời lượng kiểm tra thống nhất toàn tổ:**", indent=True)
    add_paragraph_styled(doc, "    • Môn Toán (Khối 6, 7, 8, 9): Thời gian làm bài 60 phút; hình thức: 100% Tự luận làm trên giấy thi theo đúng hướng dẫn kiểm tra định kỳ.", indent=True)
    add_paragraph_styled(doc, "    • Môn Tin học (Khối 6, 7, 8, 9): Thời gian làm bài 45 phút; hình thức: Kiểm tra trực tuyến trên phòng máy vi tính thông qua nền tảng OLM (đảm bảo tính khách quan, tự động trộn đề và chấm điểm).", indent=True)
    add_paragraph_styled(doc, "  + **Tiến độ và các mốc thời gian thực hiện bắt buộc:**", indent=True)
    add_paragraph_styled(doc, "    • **Ngày 15/10/2026:** Hạn chót nộp Ma trận, Bản đặc tả và Đề cương ôn tập về Tổ trưởng chuyên môn thẩm định và duyệt.", indent=True)
    add_paragraph_styled(doc, "    • **Ngày 24/10/2026:** Hạn chót nộp Đề kiểm tra giữa kỳ (kèm hướng dẫn chấm/thang điểm) và hoàn thành công tác phản biện chéo giữa các giáo viên trong nhóm bộ môn.", indent=True)
    add_paragraph_styled(doc, "    • **Ngày 28/10/2026:** Tổ trưởng chuyên môn tổng hợp, thẩm định lần cuối và chính thức nộp toàn bộ Đề thi giữa kỳ về bộ phận Chuyên môn nhà trường (Ban Giám hiệu) để chuẩn bị công tác in sao và tổ chức kiểm tra theo kế hoạch.", indent=True)
    
    # 3.4. Nghiên cứu bài học
    add_paragraph_styled(doc, "*- Kế hoạch Sinh hoạt chuyên môn theo Nghiên cứu bài học (NCBH) trong tháng 11/2026:*", indent=True)
    add_paragraph_styled(doc, "Nhằm bảo đảm tính liên tục và nâng cao chất lượng dạy học ở các khối lớp trọng tâm, Tổ chuyên môn thống nhất không tổ chức nghiên cứu bài học ở khối 6 (do khối 6 đang tập trung cho Chuyên đề Ngoại khóa Rung chuông vàng) mà chuyển trọng tâm sang khối 8 và khối 9 trong tháng 11/2026 (sau kỳ kiểm tra giữa học kỳ 1) với định hướng chi tiết như sau:", indent=True)
    add_paragraph_styled(doc, "  + **Bài học trọng tâm được lựa chọn:** Môn Toán lớp 8 – Bài “Định lí Thalès trong tam giác” (Chương Định lí Thalès, bộ sách GDPT 2018; phân phối chương trình dạy vào trung tuần tháng 11).", indent=True)
    add_paragraph_styled(doc, "  + **Chuyên đề định hướng nâng cao lớp 9:** Nhóm giáo viên dạy Toán 9 (Thầy Thiên, Thầy Danh, Thầy Sáng) đồng thời chuẩn bị chuyên đề sinh hoạt chuyên môn “Đổi mới phương pháp dạy học Hàm số bậc nhất và Rèn kỹ năng giải toán thực tế cho học sinh lớp 9 ôn thi Tuyển sinh 10”.", indent=True)
    add_paragraph_styled(doc, "  + **Lý do lựa chọn bài “Định lí Thalès trong tam giác” (Lớp 8):** (1) Bài học mang tính nền tảng và bước ngoặt của hình học lớp 8, giúp học sinh chuyển từ hình học trực quan sang tư duy suy luận tỉ số đoạn thẳng tỉ lệ; (2) Khả năng ứng dụng thực tế và giáo dục STEM rất cao (học sinh thực hành đo bóng mặt trời để xác định chiều cao cột cờ, cây xanh; đo khoảng cách giữa hai điểm qua chướng ngại vật); (3) Rất thuận lợi ứng dụng Năng lực số (sử dụng phần mềm hình học động GeoGebra để trực quan quan sát các tỉ số đoạn thẳng tỉ lệ không đổi).", indent=True)
    add_paragraph_styled(doc, "  + **Tiến độ và phân công thực hiện:** Cô Lê Thị Bình (phụ trách chính khối 8) chủ trì xây dựng Kế hoạch bài dạy minh họa; Thầy Trần Long Hải và Thầy Nguyễn Văn Tính phối hợp hỗ trợ thiết kế phiếu học tập, chuẩn bị dụng cụ đo đạc thực hành (thước dây, giác kế mini). Thời gian dạy thể nghiệm dự kiến vào Tuần 1 hoặc Tuần 2 Tháng 11/2026.", indent=True)
    
    # 3.5. Góp ý SGK
    add_paragraph_styled(doc, "*- Góp ý chuyên sâu chương trình Sách giáo khoa GDPT 2018 môn Toán - Tin:*", indent=True)
    add_paragraph_styled(doc, "  + **Đại số 9:** Trong bài kiểm tra, phần giải bài toán bằng cách lập hệ phương trình, trong quá trình làm bài học sinh được phép sử dụng máy tính cầm tay để bấm nghiệm kiểm tra kết quả và ghi bước kết luận theo đúng tinh thần giảm tải tính toán cơ học.", indent=True)
    add_paragraph_styled(doc, "  + **Hình học 9:** Các hệ thức lượng trong tam giác vuông (như trong SGK cũ) không được áp dụng trực tiếp như định lý sẵn có để làm bài tập; nếu học sinh sử dụng trong bài thi thì bắt buộc phải chứng minh lại bằng tam giác đồng dạng, tuân thủ đúng kết luận thống nhất của Hội đồng bộ môn cấp tỉnh.", indent=True)
    
    add_section_h2(doc, "4. Công tác chuyên đề và bồi dưỡng:")
    add_paragraph_styled(doc, "- Phát động phong trào thi đua chào mừng ngày Phụ nữ Việt Nam 20/10: Mỗi giáo viên trong tổ đăng ký ít nhất 01 tiết dạy tốt, tăng cường ứng dụng công nghệ thông tin và chuyển đổi số trong giảng dạy.", indent=True)
    add_paragraph_styled(doc, "- Chuẩn bị chu đáo công tác bồi dưỡng học sinh giỏi khối 8, 9 theo đúng tinh thần Kế hoạch số 4706/KH-SGDĐT của Sở GD&ĐT; lập danh sách học sinh cần hỗ trợ để phụ đạo kịp thời.", indent=True)
    add_paragraph_styled(doc, "- Tiếp tục quán triệt thực hiện nghiêm túc quy định về dạy thêm, học thêm (Quyết định số 25/2025/QĐ-UBND, Quyết định số 59/2026/QĐ-UBND, Văn bản hợp nhất số 01/2026/VBHN-QĐ-UBND và Công văn 5473/SGDĐT-GDPT&GDTX); tuyệt đối không vi phạm đạo đức nhà giáo.", indent=True)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. Ý KIẾN THẢO LUẬN VÀ GIẢI PHÁP CHUYÊN MÔN THỰC CHIẾN")
    add_paragraph_styled(doc, "Phiên họp diễn ra sôi nổi, thẳng thắn, phản ánh đúng thực tế lớp học và đề xuất các giải pháp kỹ thuật cụ thể:", indent=True)
    
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (Giáo viên môn Toán 8, Thư ký):** Qua theo dõi vòng 1 Đấu trường VioEdu, còn một số học sinh ở các lớp bỏ thi hoặc điểm đạt được chưa cao. Đề nghị các thầy cô giáo viên phụ trách khối cần chủ động phối hợp chặt chẽ với giáo viên chủ nhiệm để nhắc nhở các em vào thi trước khi hệ thống tự động khóa vòng vào 23h59 Chủ nhật hàng tuần. Về nhiệm vụ dạy minh họa Nghiên cứu bài học bài “Định lí Thalès trong tam giác”, tôi nhất trí nhận nhiệm vụ và sẽ kết hợp hoạt động đo đạc thực tế ngoài sân trường với mô phỏng GeoGebra; cam kết nộp đề cương Toán 8 giữa kỳ đúng hạn 15/10/2026.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Trần Long Hải (Giáo viên môn Toán 8):** Đề nghị Ban Thi đua nhà trường phổ biến rõ ràng, cụ thể tiêu chí chấm điểm thi đua cho đội cờ đỏ/sao đỏ các lớp để bảo đảm chấm điểm đồng đều, khách quan giữa các lớp (hiện nay đang có sự chênh lệch cách chấm giữa học sinh học ở Cơ sở 1 và Cơ sở 2). Đồng thời, Thầy Hải cam kết sẽ phối hợp cùng Thầy Tính hỗ trợ cô Bình thiết kế phiếu học tập và chuẩn bị dụng cụ đo đạc thực hành cho tiết dạy minh họa Thalès.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh (Giáo viên môn Toán 7, Phụ trách VioEdu K7):** Hoàn toàn nhất trí với phần đánh giá và kế hoạch hoạt động của tổ chuyên môn. Nhóm Toán 7 sẽ tập trung bám sát chuẩn kiến thức kỹ năng để xây dựng ma trận và đề cương kiểm tra giữa kỳ 1 có tính phân hóa phù hợp với học sinh khối 7, bảo đảm nộp đúng hạn 15/10/2026.", indent=True)
    
    add_paragraph_styled(doc, "- **Cô Nguyễn Thị Thảo (Giáo viên môn Toán 6, Phụ trách VioEdu K6):** Cảm ơn tổ chuyên môn đã đồng thuận chuyển nhiệm vụ Nghiên cứu bài học sang khối 8, tạo điều kiện thuận lợi cho nhóm Toán 6 tập trung toàn lực xây dựng bộ ngân hàng 35 câu hỏi và kịch bản chi tiết cho Chuyên đề Ngoại khóa “Rung chuông vàng môn Toán khối 6” chào mừng ngày 20/11; cam kết hoàn thành dự thảo ngân hàng câu hỏi trước ngày 15/10/2026.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Trần Sáng (Giáo viên môn Toán 9, KTNB):** Tiếp thu toàn diện kế hoạch kiểm tra nội bộ của nhà trường; Thầy Sáng cam kết hoàn thiện hồ sơ Kế hoạch bài dạy chuẩn Công văn 5512, tích hợp chỉ báo Năng lực số và AI in đậm, in nghiêng rõ nét theo đúng kết luận rút kinh nghiệm của tổ; chủ động gửi lịch dạy trong tuần cho Tổ trưởng để tổ sắp xếp dự giờ. Về ma trận và đề kiểm tra Toán 9, Thầy Sáng đảm bảo bám sát cấu trúc đề thi tuyển sinh 10, nộp đúng tiến độ (ma trận ngày 15/10, đề kiểm tra ngày 24/10) để tổ phản biện chéo.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (Giáo viên Tin học, Phụ trách phòng máy):** Báo cáo tình hình chuẩn bị cho kỳ kiểm tra giữa kỳ môn Tin học: 2 phòng máy tính (45 máy) đã được kiểm tra đường truyền và cài đặt ổn định; sẵn sàng tổ chức cho học sinh làm bài kiểm tra trực tuyến 100% trên nền tảng OLM theo đúng thời lượng 45 phút. Thầy Tùng cũng sẽ hỗ trợ kỹ thuật âm thanh, máy chiếu và trình chiếu câu hỏi cho sân chơi Rung chuông vàng khối 6.", indent=True)
    
    # ==================== PHẦN V ====================
    add_section_h1(doc, "V. KẾT LUẬN CỦA CHỦ TỌA VÀ NGHỊ QUYẾT CUỘC HỌP")
    add_paragraph_styled(doc, "Thầy Tổ trưởng chuyên môn Hoàng Tấn Thiên kết luận toàn diện phiên họp và chỉ đạo thực hiện các nhiệm vụ trọng tâm sau:", indent=True)
    add_paragraph_styled(doc, "1. Toàn thể giáo viên trong tổ thực hiện chuẩn xác 03 mốc thời gian kiểm tra giữa kỳ 1: (1) Ngày 15/10/2026: Nộp Ma trận, Bản đặc tả và Đề cương ôn tập về Tổ trưởng duyệt; (2) Ngày 24/10/2026: Nộp Đề kiểm tra giữa kỳ và hoàn tất phản biện chéo trong nhóm; (3) Ngày 28/10/2026: Tổ trưởng chính thức nộp toàn bộ đề thi về Ban Giám hiệu để in sao.", indent=True)
    add_paragraph_styled(doc, "2. Yêu cầu 100% giáo viên khẩn trương rà soát, chỉnh sửa ngay các tồn tại về hồ sơ bài dạy: Khắc phục lỗi công thức toán, sửa ký hiệu góc hình học, định dạng in đậm và in nghiêng các chỉ báo Năng lực số (NLS), AI, đồng bộ Header/Footer theo mẫu chung.", indent=True)
    add_paragraph_styled(doc, "3. Phối hợp chuẩn bị chu đáo công tác kiểm tra nội bộ toàn diện đối với Thầy Trần Sáng; đẩy mạnh xây dựng ngân hàng đề Rung chuông vàng khối 6; nhóm Toán 8 khẩn trương hoàn thiện Kế hoạch bài dạy minh họa bài “Định lí Thalès trong tam giác” tích hợp GeoGebra và thực hành STEM.", indent=True)
    add_paragraph_styled(doc, "4. Giáo viên phụ trách các khối tiếp tục đôn đốc học sinh tham gia đầy đủ các vòng thi Đấu trường VioEdu; GVCN phối hợp quản lý tốt các tiết Tiếng Anh giao tiếp với giáo viên nước ngoài.", indent=True)
    add_paragraph_styled(doc, "5. Chấp hành nghiêm túc quy định pháp luật về dạy thêm, học thêm; tuyệt đối không vi phạm đạo đức nhà giáo.", indent=True)
    
    add_paragraph_styled(doc, "**Biểu quyết:** 10/10 thành viên trong tổ (100% giáo viên) nhất trí hoàn toàn với nội dung cuộc họp.", indent=True)
    add_paragraph_styled(doc, "Biên bản kết thúc vào lúc 10 giờ 00 phút cùng ngày./.", indent=True)
    
    # Chữ ký 2 bên
    add_signatures(
        doc,
        left_title="THƯ KÝ CUỘC HỌP",
        left_name="Lê Thị Bình",
        right_title="TỔ TRƯỞNG CHUYÊN MÔN",
        right_name="Hoàng Tấn Thiên"
    )
    
    # Bảng ký xác nhận của các thành viên khác
    p_mem_head = doc.add_paragraph()
    p_mem_head.paragraph_format.space_before = Pt(12)
    p_mem_head.paragraph_format.space_after = Pt(4)
    r_mh = p_mem_head.add_run("CÁC THÀNH VIÊN TRONG TỔ KÝ TÊN XÁC NHẬN")
    r_mh.font.name = 'Times New Roman'
    r_mh.font.size = Pt(13)
    r_mh.bold = True
    p_mem_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    tbl_ack = doc.add_table(rows=3, cols=4)
    tbl_ack.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_borders_closed(tbl_ack)
    
    ack_names = [
        ["Đinh Văn Đông", "Hồ Đăng Danh", "Hoàng Xuân Ánh", "Trần Long Hải"],
        ["Nguyễn Văn Tính", "Dương Quang Tùng", "Trần Sáng", "Nguyễn Thị Thảo"]
    ]
    
    # Hàng 1
    for c_idx in range(4):
        cell = tbl_ack.cell(0, c_idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"**{ack_names[0][c_idx]}**\n\n*(Ký tên)*")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    # Hàng 2
    for c_idx in range(4):
        cell = tbl_ack.cell(1, c_idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"**{ack_names[1][c_idx]}**\n\n*(Ký tên)*")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    save_docx_robust(doc, out_docx_path)
    
    if out_md_path:
        tao_bien_ban_hop_to_lan_1_thang_10_md(out_md_path)


def tao_bien_ban_hop_to_lan_1_thang_10_md(out_md_path):
    md_content = """# BIÊN BẢN SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 10/2026 (LẦN 1)
**Trường THCS Trần Phú – Tổ Toán - Tin**  
**Số: 04/BB-TCM**  
*Xuân Đông, ngày 03 tháng 10 năm 2026*

---

Hôm nay, vào lúc 07 giờ 30 phút, ngày 03 tháng 10 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 10 năm học 2026 - 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).
  + *Danh sách thành viên:* Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

### NỘI DUNG CUỘC HỌP

## I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN

Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt sâu sắc các văn bản chỉ đạo của Sở Giáo dục và Đào tạo thành phố Đồng Nai, các cấp quản lý và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:

**1. Hướng dẫn tổ chức kiểm tra, đánh giá học sinh phổ thông và học viên giáo dục thường xuyên năm học 2026 - 2027 (Công văn số 5529/SGDĐT-GDPT&GDTX ngày 28/9/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Quán triệt thực hiện nghiêm túc quy định đổi mới phương pháp kiểm tra, đánh giá định kỳ và thường xuyên theo định hướng phát triển phẩm chất, năng lực học sinh. Xây dựng ma trận, bản đặc tả chi tiết bảo đảm đúng tỷ lệ 4 mức độ nhận thức (Nhận biết 40%, Thông hiểu 30%, Vận dụng 20%, Vận dụng cao 10%); đề kiểm tra bám sát chuẩn kiến thức, kỹ năng chương trình GDPT 2018, bảo đảm tính khách quan, công bằng và phân hóa tốt đối tượng học sinh; đa dạng hóa hình thức đánh giá (trên giấy kết hợp trực tuyến).
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phân công cụ thể giáo viên ra đề cương, ma trận, bản đặc tả và đề kiểm tra giữa kỳ 1 môn Toán (khối 6, 7, 8, 9) và môn Tin học; thực hiện nghiêm túc quy trình phản biện chéo và nộp đề đúng hạn quy định.

**2. Thực hiện Đề án “Tăng cường giảng dạy Tiếng Anh trong các trường phổ thông trên địa bàn tỉnh Đồng Nai” (Công văn số 3939/SGDĐT-NV1 ngày 26/9/2023 của Sở GD&ĐT):**
- **Ý chính cốt lõi:** Tăng cường lồng ghép các thuật ngữ Tiếng Anh chuyên ngành vào bài giảng chính khóa môn Toán và môn Tin học; khích lệ giáo viên tổ chức các hoạt động ngoại khóa, câu lạc bộ học thuật và sân chơi trí tuệ có yếu tố Tiếng Anh.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tích hợp các câu hỏi Tiếng Anh Toán học vào Chuyên đề Ngoại khóa “Rung chuông vàng” khối 6; hướng dẫn học sinh tiếp cận phần thi Toán Tiếng Anh trong Đấu trường VioEdu; phối hợp quản lý tốt các lớp Tiếng Anh giao tiếp do giáo viên nước ngoài trực tiếp giảng dạy 2 tiết/tuần.

**3. Quy định về quản lý dạy thêm, học thêm (Quyết định số 25/2025/QĐ-UBND ngày 14/8/2025; Quyết định sửa đổi số 59/2026/QĐ-UBND ngày 16/7/2026 của UBND thành phố Đồng Nai; Văn bản hợp nhất số 01/2026/VBHN-QĐ-UBND ngày 22/8/2026 và Công văn số 5473/SGDĐT-GDPT&GDTX ngày 25/9/2026 của Sở GD&ĐT):**
- **Ý chính cốt lõi:** Quán triệt tinh thần chấn chỉnh, tăng cường kỷ cương quản lý dạy thêm, học thêm trên địa bàn thành phố. Tuyệt đối không tổ chức dạy thêm, học thêm trái quy định dưới bất kỳ hình thức nào; không ép buộc, gợi ý phụ huynh và học sinh tham gia học thêm; nghiêm cấm việc cắt giảm nội dung bài học chính khóa để đưa vào dạy thêm; toàn thể giáo viên ký cam kết chấp hành nghiêm túc quy định pháp luật và giữ gìn đạo đức nhà giáo.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** 100% giáo viên trong tổ Toán – Tin ký cam kết không vi phạm quy định dạy thêm, học thêm; tập trung nâng cao chất lượng từng giờ dạy chính khóa trên lớp và phụ đạo học sinh còn hổng kiến thức miễn phí theo kế hoạch giáo dục của nhà trường.

**4. Kế hoạch Tổ chức Kỳ thi chọn học sinh giỏi cấp thành phố năm học 2026 - 2027 (Kế hoạch số 4706/KH-SGDĐT ngày 08/9/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Kế hoạch tuyển chọn và tổ chức kỳ thi học sinh giỏi THCS cấp thành phố nhằm phát hiện, bồi dưỡng các tài năng trẻ môn Toán và Tin học.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn chủ động rà soát, tuyển chọn các nhân tố xuất sắc khối 8 và khối 9, phân công giáo viên có kinh nghiệm phụ trách bồi dưỡng đội tuyển Toán 9 và Tin học 9 nhằm nâng cao chất lượng mũi nhọn của trường.

---

## II. ĐÁNH GIÁ CÔNG TÁC CHUYÊN MÔN CUỐI THÁNG 9/2026

### **1. Công tác chủ nhiệm:**
- Giáo viên chủ nhiệm đã ổn định vững chắc nề nếp lớp, duy trì nghiêm túc sinh hoạt 15 phút đầu giờ trước buổi học, quản lý tốt chuyên cần và nền nếp trật tự.
- Bám sát lớp, thực hiện các loại báo cáo kịp thời; hoàn thành thu nộp BHYT, BHTN đợt 1; triển khai chương trình Tiếng Anh tăng cường đến phụ huynh; hoàn thành 100% cập nhật thông tin học sinh lớp chủ nhiệm trên hệ thống CSDL ngành.
- Tích cực vận động học sinh tham gia Đấu trường VioEdu, triển khai thư viện số; phối hợp trợ giảng trong các tiết Tiếng Anh giao tiếp với giáo viên nước ngoài (2 tiết/tuần theo năng lực) bảo đảm hiệu quả.

### **2. Ngày giờ công và kỷ luật lao động:**
- Giáo viên trong tổ đảm bảo ngày giờ công nghiêm túc, tham gia đầy đủ các hoạt động hội họp của nhà trường, dạy đủ số tiết theo phân công chuyên môn; thực hiện chu đáo việc dạy bù, dạy thay khi có giáo viên đi công tác hoặc nghỉ ốm.

### **3. Công tác chuyên môn và thực hiện quy chế:**
- Ổn định nền nếp dạy và học theo đúng thời khóa biểu; thực hiện chương trình theo kế hoạch giáo dục nhà trường, dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT, dạy học giáo dục địa phương, GDNGLL và HĐTN đúng định hướng.
- **Về hồ sơ sổ sách và Kế hoạch bài dạy (KHBD):**
  - *Ưu điểm:* Đa số giáo viên trong tổ đã có ý thức chuẩn bị hồ sơ bài dạy đầy đủ theo phân phối chương trình, bảo đảm cấu trúc 4 hoạt động theo tinh thần Công văn 5512/BGDĐT-GDTrH.
  - *Tồn tại, hạn chế cần khắc phục ngay:* Qua đợt kiểm tra hồ sơ bài dạy tháng 9, một số giáo viên thực hiện chưa đúng biểu mẫu quy định. Cụ thể: Kế hoạch bài dạy còn mắc lỗi định dạng công thức toán học, biến dạng ký hiệu góc hình học; các chỉ báo năng lực số (NLS) và trí tuệ nhân tạo (AI) chưa được định dạng in đậm, in nghiêng theo quy định; một số bài soạn chưa đồng bộ Header/Footer theo mẫu chung của nhà trường. Yêu cầu các thầy cô khẩn trương rà soát, chỉnh sửa hoàn thiện trước đợt kiểm tra tiếp theo.
- **Về nền nếp giảng dạy và thực hiện quy chế chuyên môn:**
  - Chấp hành nghiêm túc quy chế chuyên môn, lên lớp đúng giờ, quản lý học sinh tốt trong các tiết học; tuyệt đối không tự ý đổi tiết, bỏ tiết khi chưa có sự phê duyệt của Tổ trưởng và Ban Giám hiệu.
  - Thực hiện ghi chép Sổ đầu bài đầy đủ, sạch sẽ, khớp 100% với tiến độ phân phối chương trình và Kế hoạch giáo dục của tổ (Phụ lục 3).
  - Công tác kiểm tra đánh giá thường xuyên: Giáo viên các bộ môn đã chủ động kiểm tra theo tiến độ, vào điểm và cập nhật kịp thời trên phần mềm quản lý điểm của trường.
  - Nề nếp phòng học bộ môn: Giáo viên Tin học duy trì nền nếp phòng máy vi tính nghiêm túc, hướng dẫn học sinh thực hiện đúng nội quy phòng máy, bảo đảm an toàn thiết bị điện và bảo quản máy móc phục vụ giảng dạy.

### **Kết quả xếp loại hồ sơ chuyên môn tháng 9/2026:**
| STT | Họ và tên giáo viên | Môn giảng dạy | Số tiết nộp | Xếp loại tháng 9 |
|:---:|:---|:---|:---:|:---:|
| 1 | Hoàng Tấn Thiên | Toán 9, Tin học 6 | Đầy đủ | **Tốt** |
| 2 | Hồ Đăng Danh | Toán 6, Toán 9 | Đầy đủ | **Tốt** |
| 3 | Trần Sáng | Toán 6, Toán 9 | Đầy đủ | **Tốt** |
| 4 | Trần Long Hải | Toán 8 | Đầy đủ | **Khá** |
| 5 | Nguyễn Thị Thảo | Toán 6, Toán 7 | Đầy đủ | **Khá** |
| 6 | Lê Thị Bình | Toán 7, Toán 8, HĐTN | Đầy đủ | **Khá** |
| 7 | Hoàng Xuân Ánh | Toán 7, HĐTN 6 | Đầy đủ | **Khá** |
| 8 | Nguyễn Văn Tính | HĐTN 7 | Đầy đủ | **Khá** |
| 9 | Đinh Văn Đông | Toán 8 | Đầy đủ | **Khá** |
| 10 | Dương Quang Tùng | Tin học 6, 7, 8, 9 | Đầy đủ | **Tốt** |

- **Tổng hợp số lượng học sinh tham gia thi Đấu trường VioEdu vòng sơ loại 1:** Toàn trường có **107 học sinh** tham gia dự thi. Cụ thể từng khối: Khối 6: 30 học sinh; Khối 7: 24 học sinh; Khối 8: 31 học sinh; Khối 9: 22 học sinh.

### **4. Công tác chuyên đề, thao giảng:**
- Tham gia đầy đủ các buổi tập huấn chuyên môn, chuyên đề do Sở GD&ĐT tổ chức; phổ biến lại trong nhóm bộ môn để triển khai thống nhất.

### **5. Công tác ngoại khóa và phong trào:**
- Đã thực hiện tốt hoạt động GDNGLL theo chủ điểm: Tổ chức Tết Trung thu vui tươi, an toàn cho học sinh; tuyên truyền học sinh chấp hành tốt nội quy trường lớp, tham gia các cuộc thi do Nhà trường và Đoàn - Đội phát động.

### **6. Công tác kiểm tra nội bộ:**
- Kiểm tra nền nếp ra vào lớp, việc thực hiện quy chế chuyên môn, chất lượng soạn giảng và tiến độ thực hiện chương trình.

### **7. Sử dụng thiết bị dạy học và phòng bộ môn:**
- Giáo viên trong tổ sử dụng có hiệu quả phòng thực hành Tin học, phòng học chức năng, khai thác triệt để các phần mềm dạy học phục vụ bài giảng.

### **8. Công tác khác:**
- Tích cực tham gia các phong trào thi đua của Đoàn – Đội, tham gia đầy đủ công tác điều tra phổ cập giáo dục theo phân công của xã.

---

## III. KẾ HOẠCH HOẠT ĐỘNG CHUYÊN MÔN THÁNG 10/2026

### **1. Công tác chủ nhiệm:**
- Ổn định nền nếp lớp chủ nhiệm, tích cực sinh hoạt 15 phút đầu giờ. Phát động đợt thi đua cao điểm chào mừng các ngày lễ lớn trong tháng: Ngày Quốc tế Người cao tuổi (01/10), Ngày Khuyến học Việt Nam (02/10), Ngày Bác Hồ gửi bức thư cuối cùng cho ngành Giáo dục (15/10) và Ngày Phụ nữ Việt Nam (20/10). Tuyên truyền phòng chống ma túy, tội phạm, ATGT, PCCC và phòng tránh tai nạn thương tích.
- Thực hiện hiệu quả Tuần lễ học tập suốt đời năm 2026; hoàn thành hồ sơ sổ sách GVCN đúng quy định; tiếp tục rà soát học sinh khó khăn; đôn đốc thu nộp BHYT, BHTN; thông tin thường xuyên qua Zalo lớp.
- Vận động học sinh đăng ký thi VioEdu các vòng tiếp theo; triển khai thư viện số và tiết học thư viện theo thời khóa biểu. Giáo viên bộ môn tích hợp bài dạy STEM (Phụ lục 2) vào Kế hoạch bài dạy theo thời điểm, hướng dẫn học sinh nộp sản phẩm tại phòng STEM.

### **2. Đảm bảo ngày giờ công và nền nếp chuyên môn:**
- Giáo viên phấn đấu đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ hoạt động của trường; dạy đúng, dạy đủ số tiết theo phân công chuyên môn; thực hiện kịp thời việc dạy bù, dạy thay khi có phân công.

### **3. Công tác chuyên môn trọng tâm:**

**a) Chuẩn bị công tác kiểm tra nội bộ nhà trường (Thanh tra toàn diện):**
- Đối tượng kiểm tra: Thầy **Trần Sáng** (thực hiện theo Kế hoạch kiểm tra nội bộ năm học 2026 - 2027 của Trường THCS Trần Phú).
- Yêu cầu chuẩn bị: Thầy Sáng chuẩn bị chu đáo toàn bộ hồ sơ chuyên môn cá nhân (Kế hoạch bài dạy chuẩn CV 5512, sổ theo dõi và đánh giá học sinh, kế hoạch dạy học cá nhân, thiết bị và đồ dùng dạy học).
- Phân công phối hợp: Thầy Sáng chủ động gửi Thời khóa biểu và lịch dạy trong tuần cho Tổ trưởng để tổ sắp xếp báo cáo Ban Giám hiệu, đồng thời phân công giáo viên trong tổ bố trí dự giờ, đóng góp ý kiến mang tính xây dựng chuyên môn.

**b) Kế hoạch Chuyên đề Ngoại khóa “Rung chuông vàng” môn Toán khối 6:**
- Nhằm tạo sân chơi học tập bổ ích, khơi dậy niềm đam mê học Toán và nâng cao kỹ năng vận dụng kiến thức thực tế cho học sinh khối 6, Tổ Toán – Tin thống nhất thành lập Ban Tổ chức và xây dựng tiến độ triển khai:
  - *Nhóm biên soạn nội dung và ngân hàng đề:* Cô Nguyễn Thị Thảo (Chủ đạo, phụ trách khối 6); Cô Lê Thị Bình (Hỗ trợ xây dựng và rà soát câu hỏi).
  - *Nhóm tư vấn và thẩm định chuyên môn:* Thầy Hoàng Tấn Thiên (Trưởng ban), Thầy Hồ Đăng Danh, Thầy Nguyễn Văn Tính, Thầy Đinh Văn Đông.
  - *Nhóm hỗ trợ tổ chức và kỹ thuật - hậu cần:* Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Thầy Dương Quang Tùng, Thầy Trần Sáng (chuẩn bị âm thanh, máy chiếu, bảng con, sân bãi).
- **Lịch trình và tiến độ thực hiện chi tiết (Thực hiện trong tháng 11/2026):**

| Thời gian | Nội dung công việc | Người phụ trách | Ghi chú / Sản phẩm |
|:---|:---|:---|:---|
| **08/10 – 15/10/2026** | Xây dựng khung thể lệ; biên soạn bộ ngân hàng 35 câu hỏi Toán 6 (30 câu chính, 5 câu phụ; tích hợp câu hỏi thực tiễn và Tiếng Anh Toán học). | Cô Thảo, Cô Bình | Bản thảo đề & đáp án |
| **16/10 – 22/10/2026** | Họp nhóm tư vấn thẩm định câu hỏi; Tổ trưởng hoàn thiện kế hoạch chi tiết trình BGH phê duyệt; Cô Thảo xem lịch chọn ngày cụ thể. | Thầy Thiên, Thầy Danh, Thầy Tính, Thầy Đông, Cô Thảo | Kế hoạch được BGH duyệt |
| **23/10 – 31/10/2026** | Thông báo thể lệ đến các lớp khối 6; các lớp lập danh sách học sinh tham gia (15 HS/lớp); nhóm hỗ trợ chuẩn bị bảng con, phấn, chuông, sân bãi. | Cô Thảo, Thầy Ánh, Thầy Hải, Thầy Tùng, Thầy Sáng | Danh sách thí sinh & CSVC |
| **01/11 – 07/11/2026** | Chạy thử chương trình, kiểm tra hệ thống âm thanh, máy chiếu trình chiếu câu hỏi; phân công dẫn chương trình (MC) và cứu trợ. | Toàn thể thành viên Ban Tổ chức | Hoàn tất chuẩn bị |
| **Tuần 2 Tháng 11/2026**<br>*(Dự kiến 14/11/2026)* | Tổ chức chính thức Chuyên đề Ngoại khóa “Rung chuông vàng môn Toán khối 6” chào mừng kỷ niệm Ngày Nhà giáo Việt Nam 20/11. | Tổ Toán – Tin phối hợp Đoàn - Đội | Tổng kết, trao thưởng |

**c) Công tác xây dựng Ma trận, Bản đặc tả, Đề cương và Đề kiểm tra giữa học kỳ 1:**
- Toàn tổ thực hiện nghiêm túc Công văn số 5529/SGDĐT-GDPT&GDTX của Sở GD&ĐT thành phố Đồng Nai về tổ chức kiểm tra, đánh giá định kỳ.
- **Yêu cầu chuyên môn:** Ma trận và bản đặc tả phải bám sát nội dung chương trình GDPT 2018, bảo đảm đúng tỉ lệ 4 mức độ nhận thức (Nhận biết 40%, Thông hiểu 30%, Vận dụng 20%, Vận dụng cao 10%). Đề kiểm tra phải bám sát ma trận và đề cương ôn tập, có tính phân hóa phù hợp với đối tượng học sinh.
- **Phân công phụ trách:** Môn Toán khối 6 do Cô Nguyễn Thị Thảo phụ trách; Môn Toán khối 7 do Thầy Hoàng Xuân Ánh phụ trách; Môn Toán khối 8 do Cô Lê Thị Bình phụ trách; Môn Toán khối 9 do Thầy Trần Sáng phụ trách; Môn Tin học (Khối 6, 7, 8, 9) do Thầy Dương Quang Tùng phụ trách.
- **Hình thức và thời lượng:**
  - Môn Toán (Khối 6, 7, 8, 9): Thời gian làm bài 60 phút; hình thức: 100% Tự luận làm trên giấy thi theo đúng hướng dẫn kiểm tra định kỳ.
  - Môn Tin học (Khối 6, 7, 8, 9): Thời gian làm bài 45 phút; hình thức: Kiểm tra trực tuyến trên phòng máy vi tính thông qua nền tảng OLM (đảm bảo tính khách quan, tự động trộn đề và chấm điểm).
- **Tiến độ và các mốc thời gian thực hiện bắt buộc:**
  - **Ngày 15/10/2026:** Hạn chót nộp Ma trận, Bản đặc tả và Đề cương ôn tập về Tổ trưởng chuyên môn thẩm định và duyệt.
  - **Ngày 24/10/2026:** Hạn chót nộp Đề kiểm tra giữa kỳ (kèm hướng dẫn chấm/thang điểm) và hoàn thành công tác phản biện chéo giữa các giáo viên trong nhóm bộ môn.
  - **Ngày 28/10/2026:** Tổ trưởng chuyên môn tổng hợp, thẩm định lần cuối và chính thức nộp toàn bộ Đề thi giữa kỳ về bộ phận Chuyên môn nhà trường (Ban Giám hiệu) để chuẩn bị công tác in sao và tổ chức kiểm tra theo kế hoạch.

**d) Kế hoạch Sinh hoạt chuyên môn theo Nghiên cứu bài học (NCBH) trong tháng 11/2026:**
- Thống nhất chuyển trọng tâm NCBH từ khối 6 sang khối 8 và khối 9 trong tháng 11/2026 (sau kỳ kiểm tra giữa kỳ 1):
  - *Bài học trọng tâm lựa chọn:* Môn Toán lớp 8 – Bài “Định lí Thalès trong tam giác” (Chương Định lí Thalès, bộ sách GDPT 2018).
  - *Chuyên đề định hướng nâng cao lớp 9:* Nhóm giáo viên dạy Toán 9 (Thầy Thiên, Thầy Danh, Thầy Sáng) chuẩn bị chuyên đề “Đổi mới phương pháp dạy học Hàm số bậc nhất và Rèn kỹ năng giải toán thực tế cho học sinh lớp 9 ôn thi Tuyển sinh 10”.
  - *Lý do lựa chọn bài Định lí Thalès (Lớp 8):* Bài học nền tảng hình học 8; khả năng ứng dụng thực tế và giáo dục STEM rất cao (đo bóng mặt trời xác định chiều cao cột cờ, cây xanh); rất thuận lợi ứng dụng Năng lực số với phần mềm hình học động GeoGebra.
  - *Phân công thực hiện:* Cô Lê Thị Bình (phụ trách chính khối 8) chủ trì xây dựng Kế hoạch bài dạy minh họa; Thầy Trần Long Hải và Thầy Nguyễn Văn Tính phối hợp hỗ trợ thiết kế phiếu học tập, chuẩn bị dụng cụ đo đạc thực hành (thước dây, giác kế mini). Thời gian dạy thể nghiệm dự kiến vào Tuần 1 hoặc Tuần 2 Tháng 11/2026.

**e) Góp ý chuyên sâu chương trình Sách giáo khoa GDPT 2018 môn Toán - Tin:**
- **Đại số 9:** Trong bài kiểm tra, phần giải bài toán bằng cách lập hệ phương trình, trong quá trình làm bài học sinh được phép sử dụng máy tính cầm tay để bấm nghiệm kiểm tra kết quả và ghi bước kết luận theo đúng tinh thần giảm tải tính toán cơ học.
- **Hình học 9:** Các hệ thức lượng trong tam giác vuông (như trong SGK cũ) không được áp dụng trực tiếp như định lý sẵn có để làm bài tập; nếu học sinh sử dụng trong bài thi thì bắt buộc phải chứng minh lại bằng tam giác đồng dạng, tuân thủ đúng kết luận thống nhất của Hội đồng bộ môn cấp tỉnh.

### **4. Công tác chuyên đề và bồi dưỡng:**
- Phát động phong trào thi đua chào mừng ngày Phụ nữ Việt Nam 20/10: Mỗi giáo viên trong tổ đăng ký ít nhất 01 tiết dạy tốt, tăng cường ứng dụng công nghệ thông tin và chuyển đổi số trong giảng dạy.
- Chuẩn bị chu đáo công tác bồi dưỡng học sinh giỏi khối 8, 9 theo đúng tinh thần Kế hoạch số 4706/KH-SGDĐT của Sở GD&ĐT; lập danh sách học sinh cần hỗ trợ để phụ đạo kịp thời.
- Tiếp tục quán triệt thực hiện nghiêm túc quy định về dạy thêm, học thêm (Quyết định số 25/2025/QĐ-UBND, Quyết định số 59/2026/QĐ-UBND, Văn bản hợp nhất số 01/2026/VBHN-QĐ-UBND và Công văn 5473/SGDĐT-GDPT&GDTX); tuyệt đối không vi phạm đạo đức nhà giáo.

---

## IV. Ý KIẾN THẢO LUẬN VÀ GIẢI PHÁP CHUYÊN MÔN THỰC CHIẾN

Phiên họp diễn ra sôi nổi, thẳng thắn, phản ánh đúng thực tế lớp học và đề xuất các giải pháp kỹ thuật cụ thể:

- **Cô Lê Thị Bình (Giáo viên môn Toán 8, Thư ký):** Qua theo dõi vòng 1 Đấu trường VioEdu, còn một số học sinh ở các lớp bỏ thi hoặc điểm đạt được chưa cao. Đề nghị các thầy cô giáo viên phụ trách khối cần chủ động phối hợp chặt chẽ với giáo viên chủ nhiệm để nhắc nhở các em vào thi trước khi hệ thống tự động khóa vòng vào 23h59 Chủ nhật hàng tuần. Về nhiệm vụ dạy minh họa Nghiên cứu bài học bài “Định lí Thalès trong tam giác”, tôi nhất trí nhận nhiệm vụ và sẽ kết hợp hoạt động đo đạc thực tế ngoài sân trường với mô phỏng GeoGebra; cam kết nộp đề cương Toán 8 giữa kỳ đúng hạn 15/10/2026.

- **Thầy Trần Long Hải (Giáo viên môn Toán 8):** Đề nghị Ban Thi đua nhà trường phổ biến rõ ràng, cụ thể tiêu chí chấm điểm thi đua cho đội cờ đỏ/sao đỏ các lớp để bảo đảm chấm điểm đồng đều, khách quan giữa các lớp (hiện nay đang có sự chênh lệch cách chấm giữa học sinh học ở Cơ sở 1 và Cơ sở 2). Đồng thời, Thầy Hải cam kết sẽ phối hợp cùng Thầy Tính hỗ trợ cô Bình thiết kế phiếu học tập và chuẩn bị dụng cụ đo đạc thực hành cho tiết dạy minh họa Thalès.

- **Thầy Hoàng Xuân Ánh (Giáo viên môn Toán 7, Phụ trách VioEdu K7):** Hoàn toàn nhất trí với phần đánh giá và kế hoạch hoạt động của tổ chuyên môn. Nhóm Toán 7 sẽ tập trung bám sát chuẩn kiến thức kỹ năng để xây dựng ma trận và đề cương kiểm tra giữa kỳ 1 có tính phân hóa phù hợp với học sinh khối 7, bảo đảm nộp đúng hạn 15/10/2026.

- **Cô Nguyễn Thị Thảo (Giáo viên môn Toán 6, Phụ trách VioEdu K6):** Cảm ơn tổ chuyên môn đã đồng thuận chuyển nhiệm vụ Nghiên cứu bài học sang khối 8, tạo điều kiện thuận lợi cho nhóm Toán 6 tập trung toàn lực xây dựng bộ ngân hàng 35 câu hỏi và kịch bản chi tiết cho Chuyên đề Ngoại khóa “Rung chuông vàng môn Toán khối 6” chào mừng ngày 20/11; cam kết hoàn thành dự thảo ngân hàng câu hỏi trước ngày 15/10/2026.

- **Thầy Trần Sáng (Giáo viên môn Toán 9, KTNB):** Tiếp thu toàn diện kế hoạch kiểm tra nội bộ của nhà trường; Thầy Sáng cam kết hoàn thiện hồ sơ Kế hoạch bài dạy chuẩn Công văn 5512, tích hợp chỉ báo Năng lực số và AI in đậm, in nghiêng rõ nét theo đúng kết luận rút kinh nghiệm của tổ; chủ động gửi lịch dạy trong tuần cho Tổ trưởng để tổ sắp xếp dự giờ. Về ma trận và đề kiểm tra Toán 9, Thầy Sáng đảm bảo bám sát cấu trúc đề thi tuyển sinh 10, nộp đúng tiến độ (ma trận ngày 15/10, đề kiểm tra ngày 24/10) để tổ phản biện chéo.

- **Thầy Dương Quang Tùng (Giáo viên Tin học, Phụ trách phòng máy):** Báo cáo tình hình chuẩn bị cho kỳ kiểm tra giữa kỳ môn Tin học: 2 phòng máy tính (45 máy) đã được kiểm tra đường truyền và cài đặt ổn định; sẵn sàng tổ chức cho học sinh làm bài kiểm tra trực tuyến 100% trên nền tảng OLM theo đúng thời lượng 45 phút. Thầy Tùng cũng sẽ hỗ trợ kỹ thuật âm thanh, máy chiếu và trình chiếu câu hỏi cho sân chơi Rung chuông vàng khối 6.

---

## V. KẾT LUẬN CỦA CHỦ TỌA VÀ NGHỊ QUYẾT CUỘC HỌP

Thầy Tổ trưởng chuyên môn Hoàng Tấn Thiên kết luận toàn diện phiên họp và chỉ đạo thực hiện các nhiệm vụ trọng tâm sau:

1. Toàn thể giáo viên trong tổ thực hiện chuẩn xác 03 mốc thời gian kiểm tra giữa kỳ 1:
   - **Ngày 15/10/2026:** Nộp Ma trận, Bản đặc tả và Đề cương ôn tập về Tổ trưởng duyệt.
   - **Ngày 24/10/2026:** Nộp Đề kiểm tra giữa kỳ và hoàn tất phản biện chéo trong nhóm.
   - **Ngày 28/10/2026:** Tổ trưởng chính thức nộp toàn bộ đề thi về Ban Giám hiệu để in sao.
2. Yêu cầu 100% giáo viên khẩn trương rà soát, chỉnh sửa ngay các tồn tại về hồ sơ bài dạy: Khắc phục lỗi công thức toán, sửa ký hiệu góc hình học, định dạng in đậm và in nghiêng các chỉ báo Năng lực số (NLS), AI, đồng bộ Header/Footer theo mẫu chung.
3. Phối hợp chuẩn bị chu đáo công tác kiểm tra nội bộ toàn diện đối với Thầy Trần Sáng; đẩy mạnh xây dựng ngân hàng đề Rung chuông vàng khối 6; nhóm Toán 8 khẩn trương hoàn thiện Kế hoạch bài dạy minh họa bài “Định lí Thalès trong tam giác” tích hợp GeoGebra và thực hành STEM.
4. Giáo viên phụ trách các khối tiếp tục đôn đốc học sinh tham gia đầy đủ các vòng thi Đấu trường VioEdu; GVCN phối hợp quản lý tốt các tiết Tiếng Anh giao tiếp với giáo viên nước ngoài.
5. Chấp hành nghiêm túc quy định pháp luật về dạy thêm, học thêm; tuyệt đối không vi phạm đạo đức nhà giáo.

- **Biểu quyết:** 10/10 thành viên trong tổ (100% giáo viên) nhất trí hoàn toàn với nội dung cuộc họp.
- Biên bản kết thúc vào lúc 10 giờ 00 phút cùng ngày./.

---

<table style="width: 100%; border: none;">
<tr>
<td style="width: 50%; text-align: center; vertical-align: top;">
<strong>THƯ KÝ CUỘC HỌP</strong><br>
<em>(Ký và ghi rõ họ tên)</em><br><br><br><br>
<strong>Lê Thị Bình</strong>
</td>
<td style="width: 50%; text-align: center; vertical-align: top;">
<strong>TỔ TRƯỞNG CHUYÊN MÔN</strong><br>
<em>(Ký và ghi rõ họ tên)</em><br><br><br><br>
<strong>Hoàng Tấn Thiên</strong>
</td>
</tr>
</table>

<div align="center">

### CÁC THÀNH VIÊN TRONG TỔ KÝ TÊN XÁC NHẬN

</div>

| Đinh Văn Đông | Hồ Đăng Danh | Hoàng Xuân Ánh | Trần Long Hải |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |

| Nguyễn Văn Tính | Dương Quang Tùng | Trần Sáng | Nguyễn Thị Thảo |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Da xuat thanh cong file Markdown: {out_md_path}")


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


def add_table_phan_cong_thang_8(doc):
    """Bảng dự kiến phân công chuyên môn HKI năm học 2026 - 2027 (chuẩn 6 cột)."""
    headers = ["STT", "Họ và tên giáo viên", "Môn và lớp phụ trách giảng dạy", "Nhiệm vụ kiêm nhiệm / khác", "Số tiết/tuần", "Ghi chú"]
    data = [
        ["1", "Hoàng Tấn Thiên", "Toán 6 (3 lớp - 12 tiết)", "Tổ trưởng chuyên môn (3t), Phụ trách Chuyển đổi số (3t)", "18", "Tổ trưởng"],
        ["2", "Trần Sáng", "Toán 9 (3 lớp - 12 tiết), Tin học 9 (1 lớp - 1 tiết)", "Phó Tổ trưởng (1t), Chủ nhiệm lớp 9/7 (4t)", "18", "Phó Tổ trưởng"],
        ["3", "Đinh Văn Đông", "Hoạt động TN, HN (3 tiết)", "Hiệu trưởng nhà trường", "3", "BGH sinh hoạt tổ"],
        ["4", "Hồ Đăng Danh", "Toán 9 (4 lớp - 16 tiết)", "Thành viên ban CNTT & CSDL ngành", "16", "GV môn Toán"],
        ["5", "Hoàng Xuân Ánh", "Toán 8 (3 lớp - 12 tiết), Tin học 6 (4 lớp - 4 tiết)", "Ủy viên tổ chuyên môn", "16", "GV Toán - Tin"],
        ["6", "Trần Long Hải", "Toán 8 (3 lớp - 12 tiết), HĐTN, HN (3 tiết)", "Chủ nhiệm lớp 8/3 (4t)", "19", "GV môn Toán"],
        ["7", "Lê Thị Bình", "Toán 7 (3 lớp - 12 tiết), HĐTN, HN (3 tiết)", "Chủ nhiệm lớp 7/1 (4t), Thư ký tổ", "19", "GV môn Toán"],
        ["8", "Nguyễn Thị Thảo", "Toán 6 (1 lớp - 4t), Toán 7 (1 lớp - 4t)\nTin 6 (2 lớp - 2t), Tin 7 (2 lớp - 2t), HĐTN (3t)", "Chủ nhiệm lớp 6/2 (4t)", "19", "GV Toán - Tin"],
        ["9", "Nguyễn Văn Tính", "Toán 6 (2 lớp - 8 tiết), Toán 7 (2 lớp - 8 tiết)", "Ủy viên tổ chuyên môn", "16", "GV môn Toán"],
        ["10", "Dương Quang Tùng", "Tin 7 (4 lớp - 4t), Tin 8 (6 lớp - 6t), Tin 9 (6 lớp - 6t)", "Phụ trách phòng máy vi tính bộ môn (3t)", "19", "GV Tin học"]
    ]
    
    col_widths = [Inches(0.5), Inches(1.5), Inches(2.3), Inches(2.0), Inches(0.8), Inches(0.9)]
    
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    format_table_borders_closed(table)
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        shading = parse_xml(r'<w:shd {} w:fill="F2F2F2"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)
        
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.bold = True
        
    # Data rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].width = col_widths[col_idx]
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            if col_idx in (0, 4, 5):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            add_run_parsed(p, str(cell_value), default_size=11.5)
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(2)

def tao_bien_ban_hop_to_lan_1_thang_8(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 1 Tháng 8/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # 1. Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="01/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 26 tháng 8 năm 2026"
    )
    
    # 2. Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1",
        "SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 8/2026\n(Chuẩn bị năm học mới 2026 – 2027)"
    )
    
    # 3. Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 10 giờ 00 phút, ngày 26 tháng 8 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 8 chuẩn bị cho năm học mới 2026 – 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # 4. NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt các văn bản chỉ đạo trọng tâm của Bộ Giáo dục và Đào tạo, UBND thành phố Đồng Nai và Sở Giáo dục và Đào tạo; đồng thời tóm tắt các vấn đề cốt lõi tác động trực tiếp đến kế hoạch thực hiện của nhà trường và Tổ chuyên môn Toán – Tin học như sau:", indent=True)
    
    # 1. Kế hoạch thời gian năm học (QĐ 2308/QĐ-BGDĐT & QĐ 2322/QĐ-UBND)
    add_paragraph_styled(doc, "**1. Kế hoạch thời gian năm học 2026 – 2027 (Quyết định số 2308/QĐ-BGDĐT ngày 06/8/2026 của Bộ GD&ĐT và Quyết định số 2322/QĐ-UBND ngày 19/8/2026 của UBND thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Toàn quốc và thành phố thống nhất tổ chức Khai giảng năm học mới vào ngày 05/9/2026. Khung kế hoạch bảo đảm đủ 35 tuần thực học (Học kỳ I: 18 tuần, từ ngày 07/9/2026 đến ngày 16/01/2027; Học kỳ II: 17 tuần, từ ngày 18/01/2027 đến ngày 24/5/2027; kết thúc năm học trước ngày 31/5/2027). Tựu trường sớm nhất đối với học sinh lớp 9 từ ngày 21/8/2026 và học sinh lớp 6 từ ngày 28/8/2026.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phải xây dựng Kế hoạch dạy học (phân phối chương trình môn Toán và môn Tin học) khớp đúng khung 35 tuần, tuyệt đối không cắt xén hoặc dồn ghép cơ học; tính toán tuần đệm kiểm tra giữa kỳ (tuần 9) và cuối kỳ (tuần 17-18) khoa học, tránh dồn ép điểm số; giáo viên chủ nhiệm khối 6 và khối 9 chủ động ổn định sĩ số, nề nếp học tập ngay từ những ngày tựu trường sớm.", indent=True)
    
    # 2. Hướng dẫn nhiệm vụ năm học GDPT (Công văn 4200/SGDĐT-GDPT&GDTX)
    add_paragraph_styled(doc, "**2. Hướng dẫn thực hiện nhiệm vụ giáo dục phổ thông năm học 2026 – 2027 (Công văn số 4200/SGDĐT-GDPT&GDTX ngày 21/8/2026 của Sở GD&ĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Năm học 2026 – 2027 thực hiện toàn diện Chương trình GDPT 2018 cho cả 4 khối lớp (6, 7, 8, 9). Nhiệm vụ trọng tâm gồm: Đổi mới phương pháp dạy học chuyển từ truyền thụ kiến thức sang phát triển năng lực, phẩm chất học sinh; đẩy mạnh giáo dục STEM/STEAM và tăng cường bài học gắn với giải quyết vấn đề thực tiễn; đổi mới kiểm tra, đánh giá thường xuyên và định kỳ theo Thông tư 22/2021/TT-BGDĐT; đẩy mạnh ứng dụng công nghệ thông tin và chuyển đổi số trong quản lý, dạy học.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ Toán – Tin học giữ vai trò nòng cốt trong nhà trường, cần tiên phong thiết kế Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH gắn với thực tế đời sống; rà soát chuẩn hóa ngân hàng câu hỏi, ma trận và bản đặc tả đề kiểm tra định kỳ (không ra đề đánh đố, vượt cấp); xây dựng Kế hoạch giáo dục STEM với tối thiểu 02 chủ đề STEM/học kỳ cho bộ môn Toán và Tin học.", indent=True)
    
    # 3. Quy định về Học bạ số (Thông tư số 70/2026/TT-BGDĐT)
    add_paragraph_styled(doc, "**3. Quy định về quản lý và sử dụng Học bạ số (Thông tư số 70/2026/TT-BGDĐT ngày 22/8/2026 của Bộ GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Bãi bỏ học bạ giấy truyền thống, áp dụng Học bạ số 100% trong toàn bộ các cơ sở giáo dục phổ thông trên nền tảng Cơ sở dữ liệu ngành; Học bạ số có đầy đủ giá trị pháp lý chính thức tương đương học bạ giấy, được ký số điện tử bởi giáo viên bộ môn, giáo viên chủ nhiệm và người đứng đầu cơ sở giáo dục (Hiệu trưởng); liên thông dữ liệu phục vụ tuyển sinh đầu cấp và thi vào lớp 10.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** 100% giáo viên trong tổ (kể cả giáo viên bộ môn và GVCN) bắt buộc phải có chứng thư số cá nhân hợp lệ và thành thạo thao tác ký số; giáo viên có trách nhiệm cập nhật điểm kiểm tra, nhận xét học sinh định kỳ chính xác, đúng hạn trên phần mềm; bảo mật tuyệt đối tài khoản chữ ký số cá nhân, tuyệt đối không nhờ người khác ký hộ; hoàn thành ký số đúng tiến độ quy định, không để chậm trễ làm ảnh hưởng đến tiến độ đồng bộ dữ liệu của toàn trường.", indent=True)
    
    # 4. Hướng dẫn giáo dục Trí tuệ nhân tạo - AI (Công văn 5588/BGDĐT-GDPT)
    add_paragraph_styled(doc, "**4. Hướng dẫn triển khai nội dung giáo dục Trí tuệ nhân tạo (AI) cấp phổ thông từ năm học 2026 – 2027 (Công văn số 5588/BGDĐT-GDPT ngày 19/8/2026 của Bộ GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Cấu trúc Khung giáo dục AI cốt lõi gồm 12 tiết/lớp/năm học, áp dụng 3 hình thức triển khai linh hoạt: (1) Thực hiện chuyên đề giáo dục AI trong kế hoạch 2 buổi/ngày; (2) Lồng ghép tích hợp vào môn Tin học và các môn học khác (Toán, KHTN...); (3) Tổ chức qua câu lạc bộ, hoạt động ngoại khóa tự nguyện; bảo đảm không gây quá tải học tập, không làm biến đổi yêu cầu cần đạt của môn học.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Môn Tin học là lực lượng chủ công triển khai các nội dung cốt lõi về hiểu biết AI, kỹ năng sử dụng AI an toàn; môn Toán chủ động lựa chọn các bài học phù hợp để tích hợp công cụ AI và mô phỏng số hỗ trợ giải toán; tổ chuyên môn ghi rõ địa chỉ bài học tích hợp trong Kế hoạch giáo dục của tổ (Phụ lục 3) và Kế hoạch bài dạy (Phụ lục 4); chuẩn bị xây dựng bài dạy minh họa chuyên đề AI cấp trường và cấp cụm trường.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ CÔNG TÁC CHUẨN BỊ NĂM HỌC MỚI TRONG THÁNG 8/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm các khối lớp đã nhận lớp, nhanh chóng ổn định tổ chức nề nếp lớp học, lập nhóm Zalo kết nối thường xuyên với phụ huynh học sinh.", indent=True)
    add_paragraph_styled(doc, "- Đã hoàn thành thông báo danh mục sách giáo khoa bộ sách Cánh Diều cho cha mẹ học sinh chuẩn bị đầy đủ cho con em; rà soát, hoàn thành danh sách học sinh có hoàn cảnh khó khăn đề nghị nhà trường và địa phương hỗ trợ học bổng, sách giáo khoa đầu năm.", indent=True)
    
    add_section_h2(doc, "2. Kỷ luật lao động và ngày giờ công:")
    add_paragraph_styled(doc, "- Toàn thể 10/10 giáo viên trong tổ chấp hành nghiêm túc quy định ngày giờ công, tham gia đầy đủ các buổi tập trung chuẩn bị năm học của nhà trường và các đợt học tập chính trị hè 2026; đeo thẻ công chức/viên chức theo quy chế.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- Các nhóm bộ môn đã tham gia đầy đủ, nghiêm túc các đợt tập huấn chuyên môn do Sở GD&ĐT tổ chức: Tập huấn SGK lớp 9 mới, chuỗi tập huấn Năng lực số, Giáo dục Trí tuệ nhân tạo (AI), Giáo dục STEM và phương pháp dạy học trên nền tảng trực tuyến OLM theo đúng tiến độ.", indent=True)
    add_paragraph_styled(doc, "- Quy mô biên chế trường năm học 2026 – 2027 gồm **25 lớp** (Khối 6: 6 lớp; Khối 7: 6 lớp; Khối 8: 6 lớp; Khối 9: 7 lớp).", indent=True)
    add_paragraph_styled(doc, "- Tổ chuyên môn đã dự kiến phân công nhiệm vụ giảng dạy và công tác kiêm nhiệm Học kỳ I năm học 2026 – 2027 cho 10 giáo viên như sau:", indent=True)
    
    # Chèn bảng phân công chuyên môn
    add_table_phan_cong_thang_8(doc)
    
    add_paragraph_styled(doc, "- Các nhóm chuyên môn theo khối lớp đã thống nhất chương trình làm việc, thiết lập nhóm Zalo chuyên môn để trao đổi tài liệu, rà soát phân phối chương trình môn học.", indent=True)
    add_paragraph_styled(doc, "- Các đồng chí nhận lớp chủ nhiệm đã hoàn thành phiếu điều tra cơ bản đầu năm đúng hạn (Cô Nguyễn Thị Thảo lớp 6/2, Cô Lê Thị Bình lớp 7/1, Thầy Trần Long Hải lớp 8/3, Thầy Trần Sáng lớp 9/7).", indent=True)
    
    add_section_h2(doc, "4. Đánh giá thi đua tháng 8/2026:")
    add_paragraph_styled(doc, "- **Đánh giá chung:** Toàn thể thành viên trong tổ nêu cao tinh thần trách nhiệm, thực hiện nghiêm túc, kịp thời mọi kế hoạch của nhà trường, chuẩn bị chu đáo điều kiện cơ sở vật chất và chuyên môn cho ngày khai giảng.", indent=True)
    add_paragraph_styled(doc, "- **Xếp loại thi đua:** 10/10 đồng chí xếp loại A (Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng).", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. KẾ HOẠCH TRỌNG TÂM THÁNG 9/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Ổn định nề nếp lớp chủ nhiệm ngay từ tuần học đầu tiên; tích cực duy trì sinh hoạt 15 phút đầu giờ trước buổi học; hướng dẫn học sinh học tập nội quy, bình bầu ban cán sự lớp.", indent=True)
    add_paragraph_styled(doc, "- Tham gia lao động vệ sinh phong quang trường lớp, tập dượt nghi thức chuẩn bị lễ khai giảng năm học mới vào ngày 05/9/2026; quản lý tốt học sinh trong ngày khai giảng.", indent=True)
    
    add_section_h2(doc, "2. Kỷ luật ngày giờ công:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ phấn đấu bảo đảm ngày giờ công, chấp hành nghiêm túc thời khóa biểu chính thức bắt đầu từ ngày 07/9/2026.", indent=True)
    add_paragraph_styled(doc, "- Thực hiện đúng quy định dạy thay, dạy bù khi đồng nghiệp đi công tác hoặc ốm đau; không tự ý đổi giờ khi chưa báo cáo Ban Giám hiệu và Tổ trưởng.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- Nhóm bộ môn họp thống nhất kế hoạch dạy học, hoàn thiện các phụ lục theo Công văn 5512/BGDĐT-GDTrH (Phụ lục 1, Phụ lục 2, Phụ lục 3) và Kế hoạch kiểm tra đánh giá nộp về nhà trường phê duyệt chậm nhất ngày 10/9/2026.", indent=True)
    add_paragraph_styled(doc, "- Toàn thể giáo viên bộ môn: Cập nhật địa chỉ lồng ghép **Khung Năng lực số (20%)** và **12 tiết Khung AI** vào Kế hoạch bài dạy (Phụ lục 4); chuẩn bị giáo án đầy đủ trước khi lên lớp, đồng bộ lên Cơ sở dữ liệu ngành để ký số tuần đúng hạn.", indent=True)
    add_paragraph_styled(doc, "- Giáo viên đăng ký mượn đồ dùng dạy học, thiết bị thực hành, sách giáo khoa và sách tham khảo phục vụ giảng dạy tại phòng thiết bị - thư viện.", indent=True)
    add_paragraph_styled(doc, "- Khai thác có hiệu quả phòng máy vi tính và phòng học chức năng, bảo đảm an toàn điện và phòng cháy chữa cháy trong quá trình sử dụng.", indent=True)
    
    add_section_h2(doc, "4. Ngoại khóa và các hoạt động khác:")
    add_paragraph_styled(doc, "- Tập trung chuẩn bị cho lễ khai giảng ngày 05/9/2026 (phân công đọc quyết tâm thư, quản lý học sinh theo phân công của nhà trường).", indent=True)
    add_paragraph_styled(doc, "- Tham gia tuyên truyền học sinh chấp hành tốt luật An toàn giao thông (đặc biệt đội mũ bảo hiểm khi ngồi trên xe máy, xe đạp điện), phòng chống bạo lực học đường; tham gia các phong trào thi đua do Nhà trường và Đội TNTP phát động.", indent=True)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. THẢO LUẬN CHUYÊN MÔN VÀ Ý KIẾN CỦA CÁC THÀNH VIÊN TRONG TỔ")
    add_paragraph_styled(doc, "Cuộc họp đã dành phần lớn thời gian để các thầy cô đi thẳng vào các vấn đề chuyên môn cốt lõi, trao đổi thẳng thắn về các khó khăn thực tế khi đứng lớp và thống nhất phương án giải quyết cho năm học mới 2026 – 2027:", indent=True)
    
    # Ý kiến 1: Thảo luận về Chương trình Toán 9 mới và đề thi tuyển sinh 10
    add_paragraph_styled(doc, "**1. Thảo luận về Chương trình môn Toán 9 mới (năm đầu áp dụng GDPT 2018) và định hướng thi vào lớp 10:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Trần Sáng (Tổ phó chuyên môn, phụ trách Toán 9):** Năm học này là năm bản lề khi khối 9 bắt đầu học SGK mới theo Chương trình GDPT 2018. Khung kiến thức có sự thay đổi rất lớn: hệ thức lượng trong tam giác vuông, đường tròn, hàm số bậc nhất, bậc hai và đặc biệt là các bài toán thống kê - xác suất thực tế chiếm tỉ trọng điểm số đáng kể. Kỳ thi tuyển sinh vào lớp 10 tới đây chắc chắn sẽ ra đề theo cấu trúc ma trận mới 100%. Nếu giáo viên chỉ dạy lý thuyết sách giáo khoa theo lối mòn cũ thì học sinh sẽ rất lúng túng khi gặp bài toán thực tế (bài toán thực tế về đo đạc hình học, bài toán kinh tế, bài toán tối ưu...). Đề nghị nhóm Toán 9 ngay trong tháng 9 phải ngồi lại biên soạn một bộ chuyên đề bài tập thực tế chuẩn hóa theo từng chương để giáo viên dùng chung cho cả 7 lớp khối 9, bảo đảm tính đồng bộ và chất lượng đại trà.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hồ Đăng Danh (GV môn Toán 9):** Hoàn toàn nhất trí với ý kiến của thầy Sáng. Cần đặc biệt lưu ý về độ phân hóa giữa 7 lớp khối 9: lớp 9/7 học sinh tiếp thu rất nhanh, nhưng một số lớp khác học sinh còn hổng nhiều kiến thức đại số lớp 8. Do đó, trong Kế hoạch bài dạy, phần bài tập luyện tập phải thiết kế phân tầng rõ rệt: từ mức độ nhận biết, thông hiểu đến vận dụng thực tế; không nên áp dụng bài tập quá sức ngay từ đầu khiến học sinh có học lực trung bình, yếu bị nản chí.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Tấn Thiên (Chủ trì / Tổ trưởng):** Kết luận và thống nhất: Giao Thầy Trần Sáng làm trưởng nhóm Toán 9, chủ trì cùng Thầy Hồ Đăng Danh rà soát khung ma trận đề kiểm tra định kỳ và biên soạn ngân hàng bài tập thực tế khối 9. Tổ chuyên môn sẽ bố trí một buổi sinh hoạt chuyên môn chuyên đề vào tuần 3 tháng 9 để toàn tổ thẩm định và đóng góp ý kiến trước khi đưa vào giảng dạy chính thức.", indent=True)
    
    # Ý kiến 2: Thảo luận về tích hợp 12 tiết AI và Khung NLS (20%)
    add_paragraph_styled(doc, "**2. Thảo luận về phương pháp tích hợp 12 tiết Khung AI và Khung Năng lực số (20%) vào KHBD:**", indent=True)
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (GV môn Toán khối 7):** Giáo viên trong tổ đều ủng hộ chủ trương tích hợp AI và Năng lực số, nhưng băn khoăn lớn nhất là việc tích hợp cụ thể như thế nào trong tiến trình 4 hoạt động của Công văn 5512/BGDĐT-GDTrH để không làm loãng kiến thức trọng tâm bài Toán. Thời lượng 1 tiết chỉ có 45 phút, nếu đưa quá nhiều thuật ngữ AI hay công nghệ vào bài giảng thì học sinh sẽ không còn thời gian để rèn kỹ năng tính toán và lập luận hình học.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (GV môn Tin học):** Về phía môn Tin học, việc tích hợp 12 tiết AI rất thuận lợi vì chương trình Tin học có sẵn các mạch kiến thức về dữ liệu, thuật toán và đạo đức số. Nhóm Tin học (thầy Tùng, thầy Danh, cô Thảo) sẽ chủ động gánh vác phần lớn các bài học AI lý thuyết và kỹ năng sử dụng công cụ AI an toàn. Đối với môn Toán, việc tích hợp chỉ nên dừng lại ở mức độ công cụ trực quan (ví dụ: dùng phần mềm GeoGebra để vẽ hình động, dùng AI gợi ý hướng giải hoặc kiểm tra nghiệm), tuyệt đối không dạy kỹ thuật AI chuyên sâu trong giờ Toán làm quá tải học sinh.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Tấn Thiên (Tổ trưởng):** Thống nhất quan điểm: Tích hợp AI vào môn Toán phải thực chất, nhẹ nhàng và tự nhiên. Trong Kế hoạch bài dạy (Phụ lục 4), giáo viên chỉ cần in đậm, in nghiêng mục tiêu AI/NLS tại Hoạt động Luyện tập hoặc Vận dụng. Giao nhóm Tin học phối hợp cùng Thầy Sáng và Cô Bình soạn 01 giáo án mẫu tích hợp AI môn Toán lớp 8 và lớp 9 để gửi vào nhóm Zalo tổ cho cả tổ tham khảo trước ngày 10/9.", indent=True)
    
    # Ý kiến 3: Thảo luận về Cơ sở vật chất phòng máy vi tính môn Tin học
    add_paragraph_styled(doc, "**3. Thảo luận về cơ sở vật chất phòng máy vi tính và thiết bị thực hành môn Tin học:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (Phụ trách phòng máy vi tính):** Báo cáo hiện trạng: Nhà trường có 02 phòng máy vi tính (phòng 1 có 32 máy, phòng 2 có 30 máy). Qua rà soát kỹ thuật đầu năm, hiện có 6 máy tính bị hỏng chuột, 4 máy nguồn chập chờn và đường truyền mạng internet ở phòng 2 đôi lúc bị nghẽn khi học sinh cùng đăng nhập. Trong khi năm học này môn Tin học có tổng cộng 25 lớp, tần suất sử dụng phòng máy là liên tục cả sáng và chiều.", indent=True)
    add_paragraph_styled(doc, "- **Cô Nguyễn Thị Thảo (GV môn Tin học):** Nếu phòng máy thiếu máy tính hoạt động tốt thì học sinh phải ngồi ghép 2 đến 3 em một máy, rất khó quản lý nề nếp và hiệu quả thực hành lập trình Scratch (khối 6, 7) và Python (khối 8, 9) sẽ giảm sút rõ rệt. Đề nghị Tổ trưởng kiến nghị Ban Giám hiệu mua bổ sung chuột, bàn phím dự phòng và cấu hình lại mạng nội bộ trước ngày 05/9.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Đinh Văn Đông (Hiệu trưởng):** Tiếp thu ý kiến xác đáng của thầy Tùng và cô Thảo. Nhà trường đã phê duyệt kinh phí bảo dưỡng thiết bị dạy học đầu năm. Giao bộ phận thiết bị phối hợp với thầy Tùng hoàn thành việc kiểm tra, thay thế linh kiện hư hỏng và sửa chữa dứt điểm đường truyền internet phòng máy xong trước ngày 02/9 để đảm bảo ngày 07/9 học sinh vào học thực hành thuận lợi.", indent=True)
    
    # Ý kiến 4: Thảo luận về Triển khai Học bạ số và chữ ký số giáo viên (Thông tư 70)
    add_paragraph_styled(doc, "**4. Thảo luận về triển khai Học bạ số và chữ ký số giáo viên (Thông tư số 70/2026/TT-BGDĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh (GV môn Toán):** Việc triển khai Học bạ số thay cho học bạ giấy là bước tiến lớn, giúp giảm bớt áp lực ghi chép thủ công. Tuy nhiên, một số thầy cô còn lúng túng trong thao tác cài đặt chứng thư số trên điện thoại thông minh (SmartCA / VNPT CA), việc xác thực ký số điện tử và quy trình kiểm tra dữ liệu điểm số trước khi ký để tránh sai lệch.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hồ Đăng Danh (GV Tin học, CSDL ngành):** Đề xuất nhóm Tin học sẽ hỗ trợ kỹ thuật trực tiếp cho từng thầy cô trong tổ, hướng dẫn cài đặt app, kích hoạt chứng thư số và tổ chức một buổi thao tác ký số thử nghiệm trên hệ thống Cơ sở dữ liệu ngành vào đầu tháng 9.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Đinh Văn Đông (Hiệu trưởng):** Quán triệt nghiêm túc: Học bạ số là hồ sơ pháp lý liên thông quốc gia, giáo viên phải quản lý tài khoản ký số cá nhân như con dấu của mình, tuyệt đối không chia sẻ mật khẩu hay nhờ người khác ký hộ. Điểm số khi đã ký số sẽ khóa dữ liệu, sửa chữa rất phức tạp. Yêu cầu toàn thể giáo viên trong tổ nêu cao tinh thần trách nhiệm, vào điểm đúng hạn và kiểm tra thật kỹ trước khi ký số.", indent=True)
    
    # Ý kiến 5: Thảo luận về Giải pháp phụ đạo học sinh yếu kém và công tác chủ nhiệm đầu năm
    add_paragraph_styled(doc, "**5. Thảo luận về giải pháp phụ đạo học sinh yếu kém môn Toán và nề nếp chủ nhiệm:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Nguyễn Văn Tính (GV môn Toán khối 6 & 7):** Học sinh lớp 6 mới chuyển cấp từ tiểu học lên còn bỡ ngỡ về phương pháp học THCS; kỹ năng trình bày bài toán có lời văn và kỹ năng tính toán phân số, số thập phân còn nhiều hạn chế. Giáo viên dạy khối 6 cần kiên nhẫn, rèn phương pháp ghi chép và cách lập luận chuẩn mực ngay từ những tuần đầu tiên.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Trần Long Hải (GV môn Toán, GVCN lớp 8/3):** Đồng ý với thầy Tính. Đối với học sinh khối 8 và khối 9, ngay trong tháng 9 giáo viên bộ môn cần phối hợp chặt chẽ với giáo viên chủ nhiệm rà soát, lập danh sách học sinh có nguy cơ mất gốc kiến thức để có kế hoạch kèm cặp, phân công bạn học khá giúp đỡ bạn yếu trong 15 phút đầu giờ hoặc giao thêm bài tập vừa sức.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh (GV môn Toán):** Lưu ý thêm về công tác an toàn giao thông đầu năm: Đề nghị các giáo viên chủ nhiệm (đặc biệt khối 8, khối 9) phối hợp chặt chẽ với Tổng phụ trách Đội và phụ huynh nhắc nhở học sinh nghiêm túc đội mũ bảo hiểm khi đi xe đạp điện, xe máy điện tới trường.", indent=True)
    
    # ==================== PHẦN V ====================
    add_section_h1(doc, "V. KẾT LUẬN VÀ BIỂU QUYẾT")
    add_paragraph_styled(doc, "- Thầy Tổ trưởng Hoàng Tấn Thiên tổng hợp các ý kiến thảo luận và kết luận: Toàn thể giáo viên trong tổ phát huy tinh thần đoàn kết, trách nhiệm, tập trung hoàn thiện Kế hoạch bài dạy theo chuẩn CV 5512, tích hợp hiệu quả Khung AI và Năng lực số, chủ động hỗ trợ học sinh và chuẩn bị tốt nhất cho năm học mới 2026 – 2027.", indent=True)
    add_paragraph_styled(doc, "- **Biểu quyết:** 10/10 thành viên có mặt tán thành 100% với các nội dung đánh giá công tác tháng 8/2026, kế hoạch hoạt động tháng 9/2026 và các giải pháp chuyên môn đã thống nhất.", indent=True)
    add_paragraph_styled(doc, "Biên bản cuộc họp kết thúc vào lúc 11 giờ 30 phút cùng ngày, đã được đọc lại cho toàn thể các thành viên cùng nghe, nhất trí thông qua và ký xác nhận dưới đây; biên bản được lập thành 02 bản có giá trị như nhau, lưu hồ sơ tổ chuyên môn và gửi Ban Giám hiệu nhà trường./.", indent=True)
    
    # 5. Khung chữ ký chuẩn
    add_bien_ban_signatures(doc, chu_tri="Hoàng Tấn Thiên", thu_ky="Lê Thị Bình")
    
    # 6. Danh sách các thành viên khác của tổ ký xác nhận
    p_tv = doc.add_paragraph()
    p_tv.paragraph_format.space_before = Pt(12)
    p_tv.paragraph_format.space_after = Pt(4)
    r_tv = p_tv.add_run("CÁC THÀNH VIÊN KHÁC CỦA TỔ CHUYÊN MÔN KÝ XÁC NHẬN:\n")
    r_tv.font.name = 'Times New Roman'
    r_tv.font.size = Pt(13)
    r_tv.bold = True
    
    # Bảng 4 cột thành viên ký xác nhận
    table_tv = doc.add_table(rows=2, cols=4)
    table_tv.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_tv.autofit = False
    
    # Bỏ viền bảng chữ ký
    for r in table_tv.rows:
        for c in r.cells:
            tcPr = c._tc.get_or_add_tcPr()
            tcBorders = parse_xml(r'<w:tcBorders {}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>'.format(nsdecls('w')))
            tcPr.append(tcBorders)
            
    members_r1 = ["Đinh Văn Đông", "Trần Sáng", "Hồ Đăng Danh", "Hoàng Xuân Ánh"]
    members_r2 = ["Trần Long Hải", "Nguyễn Thị Thảo", "Nguyễn Văn Tính", "Dương Quang Tùng"]
    
    for i, name in enumerate(members_r1):
        cell = table_tv.rows[0].cells[i]
        cell.width = Inches(1.7)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(25)
        r = p.add_run(f"(Ký tên)\n\n\n**{name}**")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    for i, name in enumerate(members_r2):
        cell = table_tv.rows[1].cells[i]
        cell.width = Inches(1.7)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(25)
        r = p.add_run(f"(Ký tên)\n\n\n**{name}**")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    save_docx_robust(doc, out_docx_path)
    print(f"Da xuat thanh cong file Word: {out_docx_path}")
    
    if out_md_path:
        os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
        tao_bien_ban_hop_to_lan_1_thang_8_md(out_md_path)
        print(f"Da xuat thanh cong file Markdown: {out_md_path}")

def tao_bien_ban_hop_to_lan_1_thang_8_md(out_md_path):
    """Xuất phiên bản Markdown cho Biên bản họp tổ Lần 1 Tháng 8/2026."""
    md_content = """<div align="center">

| **TRƯỜNG THCS TRẦN PHÚ**<br>**TỔ TOÁN - TIN HỌC**<br>Số: 01/BB-TCM | **CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM**<br>**Độc lập – Tự do – Hạnh phúc**<br>──────────────────<br>*Xuân Đông, ngày 26 tháng 8 năm 2026* |
|:---:|:---:|

---

# BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1
### SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 8/2026
*(Chuẩn bị năm học mới 2026 – 2027)*
──────────────────

</div>

Hôm nay, vào lúc 10 giờ 00 phút, ngày 26 tháng 8 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 8 chuẩn bị cho năm học mới 2026 – 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.  
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.  
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).  
  + *Danh sách thành viên:* Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

<div align="center">

### NỘI DUNG CUỘC HỌP

</div>

## I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN

Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt các văn bản chỉ đạo trọng tâm của Bộ Giáo dục và Đào tạo, UBND thành phố Đồng Nai và Sở Giáo dục và Đào tạo; đồng thời tóm tắt các vấn đề cốt lõi tác động trực tiếp đến kế hoạch thực hiện của nhà trường và Tổ chuyên môn Toán – Tin học như sau:

**1. Kế hoạch thời gian năm học 2026 – 2027 (Quyết định số 2308/QĐ-BGDĐT ngày 06/8/2026 của Bộ GD&ĐT và Quyết định số 2322/QĐ-UBND ngày 19/8/2026 của UBND thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Toàn quốc và thành phố thống nhất tổ chức Khai giảng năm học mới vào ngày 05/9/2026. Khung kế hoạch bảo đảm đủ 35 tuần thực học (Học kỳ I: 18 tuần, từ ngày 07/9/2026 đến ngày 16/01/2027; Học kỳ II: 17 tuần, từ ngày 18/01/2027 đến ngày 24/5/2027; kết thúc năm học trước ngày 31/5/2027). Tựu trường sớm nhất đối với học sinh lớp 9 từ ngày 21/8/2026 và học sinh lớp 6 từ ngày 28/8/2026.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phải xây dựng Kế hoạch dạy học (phân phối chương trình môn Toán và môn Tin học) khớp đúng khung 35 tuần, tuyệt đối không cắt xén hoặc dồn ghép cơ học; tính toán tuần đệm kiểm tra giữa kỳ (tuần 9) và cuối kỳ (tuần 17-18) khoa học, tránh dồn ép điểm số; giáo viên chủ nhiệm khối 6 và khối 9 chủ động ổn định sĩ số, nề nếp học tập ngay từ những ngày tựu trường sớm.

**2. Hướng dẫn thực hiện nhiệm vụ giáo dục phổ thông năm học 2026 – 2027 (Công văn số 4200/SGDĐT-GDPT&GDTX ngày 21/8/2026 của Sở GD&ĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Năm học 2026 – 2027 thực hiện toàn diện Chương trình GDPT 2018 cho cả 4 khối lớp (6, 7, 8, 9). Nhiệm vụ trọng tâm gồm: Đổi mới phương pháp dạy học chuyển từ truyền thụ kiến thức sang phát triển năng lực, phẩm chất học sinh; đẩy mạnh giáo dục STEM/STEAM và tăng cường bài học gắn với giải quyết vấn đề thực tiễn; đổi mới kiểm tra, đánh giá thường xuyên và định kỳ theo Thông tư 22/2021/TT-BGDĐT; đẩy mạnh ứng dụng công nghệ thông tin và chuyển đổi số trong quản lý, dạy học.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ Toán – Tin học giữ vai trò nòng cốt trong nhà trường, cần tiên phong thiết kế Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH gắn với thực tế đời sống; rà soát chuẩn hóa ngân hàng câu hỏi, ma trận và bản đặc tả đề kiểm tra định kỳ (không ra đề đánh đố, vượt cấp); xây dựng Kế hoạch giáo dục STEM với tối thiểu 02 chủ đề STEM/học kỳ cho bộ môn Toán và Tin học.

**3. Quy định về quản lý và sử dụng Học bạ số (Thông tư số 70/2026/TT-BGDĐT ngày 22/8/2026 của Bộ GD&ĐT):**
- **Ý chính cốt lõi:** Bãi bỏ học bạ giấy truyền thống, áp dụng Học bạ số 100% trong toàn bộ các cơ sở giáo dục phổ thông trên nền tảng Cơ sở dữ liệu ngành; Học bạ số có đầy đủ giá trị pháp lý chính thức tương đương học bạ giấy, được ký số điện tử bởi giáo viên bộ môn, giáo viên chủ nhiệm và người đứng đầu cơ sở giáo dục (Hiệu trưởng); liên thông dữ liệu phục vụ tuyển sinh đầu cấp và thi vào lớp 10.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** 100% giáo viên trong tổ (kể cả giáo viên bộ môn và GVCN) bắt buộc phải có chứng thư số cá nhân hợp lệ và thành thạo thao tác ký số; giáo viên có trách nhiệm cập nhật điểm kiểm tra, nhận xét học sinh định kỳ chính xác, đúng hạn trên phần mềm; bảo mật tuyệt đối tài khoản chữ ký số cá nhân, tuyệt đối không nhờ người khác ký hộ; hoàn thành ký số đúng tiến độ quy định, không để chậm trễ làm ảnh hưởng đến tiến độ đồng bộ dữ liệu của toàn trường.

**4. Hướng dẫn triển khai nội dung giáo dục Trí tuệ nhân tạo (AI) cấp phổ thông từ năm học 2026 – 2027 (Công văn số 5588/BGDĐT-GDPT ngày 19/8/2026 của Bộ GD&ĐT):**
- **Ý chính cốt lõi:** Cấu trúc Khung giáo dục AI cốt lõi gồm 12 tiết/lớp/năm học, áp dụng 3 hình thức triển khai linh hoạt: (1) Thực hiện chuyên đề giáo dục AI trong kế hoạch 2 buổi/ngày; (2) Lồng ghép tích hợp vào môn Tin học và các môn học khác (Toán, KHTN...); (3) Tổ chức qua câu lạc bộ, hoạt động ngoại khóa tự nguyện; bảo đảm không gây quá tải học tập, không làm biến đổi yêu cầu cần đạt của môn học.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Môn Tin học là lực lượng chủ công triển khai các nội dung cốt lõi về hiểu biết AI, kỹ năng sử dụng AI an toàn; môn Toán chủ động lựa chọn các bài học phù hợp để tích hợp công cụ AI và mô phỏng số hỗ trợ giải toán; tổ chuyên môn ghi rõ địa chỉ bài học tích hợp trong Kế hoạch giáo dục của tổ (Phụ lục 3) và Kế hoạch bài dạy (Phụ lục 4); chuẩn bị xây dựng bài dạy minh họa chuyên đề AI cấp trường và cấp cụm trường.

## II. ĐÁNH GIÁ CÔNG TÁC CHUẨN BỊ NĂM HỌC MỚI TRONG THÁNG 8/2026

### **1. Công tác chủ nhiệm:**
- Giáo viên chủ nhiệm các khối lớp đã nhận lớp, nhanh chóng ổn định tổ chức nề nếp lớp học, lập nhóm Zalo kết nối thường xuyên với phụ huynh học sinh.
- Đã hoàn thành thông báo danh mục sách giáo khoa bộ sách Cánh Diều cho cha mẹ học sinh chuẩn bị đầy đủ cho con em; rà soát, hoàn thành danh sách học sinh có hoàn cảnh khó khăn đề nghị nhà trường và địa phương hỗ trợ học bổng, sách giáo khoa đầu năm.

### **2. Kỷ luật lao động và ngày giờ công:**
- Toàn thể 10/10 giáo viên trong tổ chấp hành nghiêm túc quy định ngày giờ công, tham gia đầy đủ các buổi tập trung chuẩn bị năm học của nhà trường và các đợt học tập chính trị hè 2026; đeo thẻ công chức/viên chức theo quy chế.

### **3. Công tác chuyên môn:**
- Các nhóm bộ môn đã tham gia đầy đủ, nghiêm túc các đợt tập huấn chuyên môn do Sở GD&ĐT tổ chức: Tập huấn SGK lớp 9 mới, chuỗi tập huấn Năng lực số, Giáo dục Trí tuệ nhân tạo (AI), Giáo dục STEM và phương pháp dạy học trên nền tảng trực tuyến OLM theo đúng tiến độ.
- Quy mô biên chế trường năm học 2026 – 2027 gồm **25 lớp** (Khối 6: 6 lớp; Khối 7: 6 lớp; Khối 8: 6 lớp; Khối 9: 7 lớp).
- Tổ chuyên môn đã dự kiến phân công nhiệm vụ giảng dạy và công tác kiêm nhiệm Học kỳ I năm học 2026 – 2027 cho 10 giáo viên như sau:

| STT | Họ và tên giáo viên | Môn và lớp phụ trách giảng dạy | Nhiệm vụ kiêm nhiệm / khác | Số tiết/tuần | Ghi chú |
|:---:|:---|:---|:---|:---:|:---:|
| 1 | Hoàng Tấn Thiên | Toán 6 (3 lớp - 12 tiết) | Tổ trưởng chuyên môn (3t), Phụ trách Chuyển đổi số (3t) | 18 | Tổ trưởng |
| 2 | Trần Sáng | Toán 9 (3 lớp - 12 tiết), Tin học 9 (1 lớp - 1 tiết) | Phó Tổ trưởng (1t), Chủ nhiệm lớp 9/7 (4t) | 18 | Phó Tổ trưởng |
| 3 | Đinh Văn Đông | Hoạt động TN, HN (3 tiết) | Hiệu trưởng nhà trường | 3 | BGH sinh hoạt tổ |
| 4 | Hồ Đăng Danh | Toán 9 (4 lớp - 16 tiết) | Thành viên ban CNTT & CSDL ngành | 16 | GV môn Toán |
| 5 | Hoàng Xuân Ánh | Toán 8 (3 lớp - 12 tiết), Tin học 6 (4 lớp - 4 tiết) | Ủy viên tổ chuyên môn | 16 | GV Toán - Tin |
| 6 | Trần Long Hải | Toán 8 (3 lớp - 12 tiết), HĐTN, HN (3 tiết) | Chủ nhiệm lớp 8/3 (4t) | 19 | GV môn Toán |
| 7 | Lê Thị Bình | Toán 7 (3 lớp - 12 tiết), HĐTN, HN (3 tiết) | Chủ nhiệm lớp 7/1 (4t), Thư ký tổ | 19 | GV môn Toán |
| 8 | Nguyễn Thị Thảo | Toán 6 (1 lớp - 4t), Toán 7 (1 lớp - 4t)<br>Tin 6 (2 lớp - 2t), Tin 7 (2 lớp - 2t), HĐTN (3t) | Chủ nhiệm lớp 6/2 (4t) | 19 | GV Toán - Tin |
| 9 | Nguyễn Văn Tính | Toán 6 (2 lớp - 8 tiết), Toán 7 (2 lớp - 8 tiết) | Ủy viên tổ chuyên môn | 16 | GV môn Toán |
| 10 | Dương Quang Tùng | Tin 7 (4 lớp - 4t), Tin 8 (6 lớp - 6t), Tin 9 (6 lớp - 6t) | Phụ trách phòng máy vi tính bộ môn (3t) | 19 | GV Tin học |

- Các nhóm chuyên môn theo khối lớp đã thống nhất chương trình làm việc, thiết lập nhóm Zalo chuyên môn để trao đổi tài liệu, rà soát phân phối chương trình môn học.
- Các đồng chí nhận lớp chủ nhiệm đã hoàn thành phiếu điều tra cơ bản đầu năm đúng hạn (Cô Nguyễn Thị Thảo lớp 6/2, Cô Lê Thị Bình lớp 7/1, Thầy Trần Long Hải lớp 8/3, Thầy Trần Sáng lớp 9/7).

### **4. Đánh giá thi đua tháng 8/2026:**
- **Đánh giá chung:** Toàn thể thành viên trong tổ nêu cao tinh thần trách nhiệm, thực hiện nghiêm túc, kịp thời mọi kế hoạch của nhà trường, chuẩn bị chu đáo điều kiện cơ sở vật chất và chuyên môn cho ngày khai giảng.
- **Xếp loại thi đua:** 10/10 đồng chí xếp loại A (Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng).

## III. KẾ HOẠCH TRỌNG TÂM THÁNG 9/2026

### **1. Công tác chủ nhiệm:**
- Ổn định nề nếp lớp chủ nhiệm ngay từ tuần học đầu tiên; tích cực duy trì sinh hoạt 15 phút đầu giờ trước buổi học; hướng dẫn học sinh học tập nội quy, bình bầu ban cán sự lớp.
- Tham gia lao động vệ sinh phong quang trường lớp, tập dượt nghi thức chuẩn bị lễ khai giảng năm học mới vào ngày 05/9/2026; quản lý tốt học sinh trong ngày khai giảng.

### **2. Kỷ luật ngày giờ công:**
- Giáo viên trong tổ phấn đấu bảo đảm ngày giờ công, chấp hành nghiêm túc thời khóa biểu chính thức bắt đầu từ ngày 07/9/2026.
- Thực hiện đúng quy định dạy thay, dạy bù khi đồng nghiệp đi công tác hoặc ốm đau; không tự ý đổi giờ khi chưa báo cáo Ban Giám hiệu và Tổ trưởng.

### **3. Công tác chuyên môn:**
- Nhóm bộ môn họp thống nhất kế hoạch dạy học, hoàn thiện các phụ lục theo Công văn 5512/BGDĐT-GDTrH (Phụ lục 1, Phụ lục 2, Phụ lục 3) và Kế hoạch kiểm tra đánh giá nộp về nhà trường phê duyệt chậm nhất ngày 10/9/2026.
- Toàn thể giáo viên bộ môn: Cập nhật địa chỉ lồng ghép **Khung Năng lực số (20%)** và **12 tiết Khung AI** vào Kế hoạch bài dạy (Phụ lục 4); chuẩn bị giáo án đầy đủ trước khi lên lớp, đồng bộ lên Cơ sở dữ liệu ngành để ký số tuần đúng hạn.
- Giáo viên đăng ký mượn đồ dùng dạy học, thiết bị thực hành, sách giáo khoa và sách tham khảo phục vụ giảng dạy tại phòng thiết bị - thư viện.
- Khai thác có hiệu quả phòng máy vi tính và phòng học chức năng, bảo đảm an toàn điện và phòng cháy chữa cháy trong quá trình sử dụng.

### **4. Ngoại khóa và các hoạt động khác:**
- Tập trung chuẩn bị cho lễ khai giảng ngày 05/9/2026 (phân công đọc quyết tâm thư, quản lý học sinh theo phân công của nhà trường).
- Tham gia tuyên truyền học sinh chấp hành tốt luật An toàn giao thông (đặc biệt đội mũ bảo hiểm khi ngồi trên xe máy, xe đạp điện), phòng chống bạo lực học đường; tham gia các phong trào thi đua do Nhà trường và Đội TNTP phát động.

## IV. THẢO LUẬN CHUYÊN MÔN VÀ Ý KIẾN CỦA CÁC THÀNH VIÊN TRONG TỔ

Cuộc họp đã dành phần lớn thời gian để các thầy cô đi thẳng vào các vấn đề chuyên môn cốt lõi, trao đổi thẳng thắn về các khó khăn thực tế khi đứng lớp và thống nhất phương án giải quyết cho năm học mới 2026 – 2027:

**1. Thảo luận về Chương trình môn Toán 9 mới (năm đầu áp dụng GDPT 2018) và định hướng thi vào lớp 10:**
- **Thầy Trần Sáng (Tổ phó chuyên môn, phụ trách Toán 9):** Năm học này là năm bản lề khi khối 9 bắt đầu học SGK mới theo Chương trình GDPT 2018. Khung kiến thức có sự thay đổi rất lớn: hệ thức lượng trong tam giác vuông, đường tròn, hàm số bậc nhất, bậc hai và đặc biệt là các bài toán thống kê - xác suất thực tế chiếm tỉ trọng điểm số đáng kể. Kỳ thi tuyển sinh vào lớp 10 tới đây chắc chắn sẽ ra đề theo cấu trúc ma trận mới 100%. Nếu giáo viên chỉ dạy lý thuyết sách giáo khoa theo lối mòn cũ thì học sinh sẽ rất lúng túng khi gặp bài toán thực tế (bài toán thực tế về đo đạc hình học, bài toán kinh tế, bài toán tối ưu...). Đề nghị nhóm Toán 9 ngay trong tháng 9 phải ngồi lại biên soạn một bộ chuyên đề bài tập thực tế chuẩn hóa theo từng chương để giáo viên dùng chung cho cả 7 lớp khối 9, bảo đảm tính đồng bộ và chất lượng đại trà.
- **Thầy Hồ Đăng Danh (GV môn Toán 9):** Hoàn toàn nhất trí với ý kiến của thầy Sáng. Cần đặc biệt lưu ý về độ phân hóa giữa 7 lớp khối 9: lớp 9/7 học sinh tiếp thu rất nhanh, nhưng một số lớp khác học sinh còn hổng nhiều kiến thức đại số lớp 8. Do đó, trong Kế hoạch bài dạy, phần bài tập luyện tập phải thiết kế phân tầng rõ rệt: từ mức độ nhận biết, thông hiểu đến vận dụng thực tế; không nên áp dụng bài tập quá sức ngay từ đầu khiến học sinh có học lực trung bình, yếu bị nản chí.
- **Thầy Hoàng Tấn Thiên (Chủ trì / Tổ trưởng):** Kết luận và thống nhất: Giao Thầy Trần Sáng làm trưởng nhóm Toán 9, chủ trì cùng Thầy Hồ Đăng Danh rà soát khung ma trận đề kiểm tra định kỳ và biên soạn ngân hàng bài tập thực tế khối 9. Tổ chuyên môn sẽ bố trí một buổi sinh hoạt chuyên môn chuyên đề vào tuần 3 tháng 9 để toàn tổ thẩm định và đóng góp ý kiến trước khi đưa vào giảng dạy chính thức.

**2. Thảo luận về phương pháp tích hợp 12 tiết Khung AI và Khung Năng lực số (20%) vào KHBD:**
- **Cô Lê Thị Bình (GV môn Toán khối 7):** Giáo viên trong tổ đều ủng hộ chủ trương tích hợp AI và Năng lực số, nhưng băn khoăn lớn nhất là việc tích hợp cụ thể như thế nào trong tiến trình 4 hoạt động của Công văn 5512/BGDĐT-GDTrH để không làm loãng kiến thức trọng tâm bài Toán. Thời lượng 1 tiết chỉ có 45 phút, nếu đưa quá nhiều thuật ngữ AI hay công nghệ vào bài giảng thì học sinh sẽ không còn thời gian để rèn kỹ năng tính toán và lập luận hình học.
- **Thầy Dương Quang Tùng (GV môn Tin học):** Về phía môn Tin học, việc tích hợp 12 tiết AI rất thuận lợi vì chương trình Tin học có sẵn các mạch kiến thức về dữ liệu, thuật toán và đạo đức số. Nhóm Tin học (thầy Tùng, thầy Danh, cô Thảo) sẽ chủ động gánh vác phần lớn các bài học AI lý thuyết và kỹ năng sử dụng công cụ AI an toàn. Đối với môn Toán, việc tích hợp chỉ nên dừng lại ở mức độ công cụ trực quan (ví dụ: dùng phần mềm GeoGebra để vẽ hình động, dùng AI gợi ý hướng giải hoặc kiểm tra nghiệm), tuyệt đối không dạy kỹ thuật AI chuyên sâu trong giờ Toán làm quá tải học sinh.
- **Thầy Hoàng Tấn Thiên (Tổ trưởng):** Thống nhất quan điểm: Tích hợp AI vào môn Toán phải thực chất, nhẹ nhàng và tự nhiên. Trong Kế hoạch bài dạy (Phụ lục 4), giáo viên chỉ cần in đậm, in nghiêng mục tiêu AI/NLS tại Hoạt động Luyện tập hoặc Vận dụng. Giao nhóm Tin học phối hợp cùng Thầy Sáng và Cô Bình soạn 01 giáo án mẫu tích hợp AI môn Toán lớp 8 và lớp 9 để gửi vào nhóm Zalo tổ cho cả tổ tham khảo trước ngày 10/9.

**3. Thảo luận về cơ sở vật chất phòng máy vi tính và thiết bị thực hành môn Tin học:**
- **Thầy Dương Quang Tùng (Phụ trách phòng máy vi tính):** Báo cáo hiện trạng: Nhà trường có 02 phòng máy vi tính (phòng 1 có 32 máy, phòng 2 có 30 máy). Qua rà soát kỹ thuật đầu năm, hiện có 6 máy tính bị hỏng chuột, 4 máy nguồn chập chờn và đường truyền mạng internet ở phòng 2 đôi lúc bị nghẽn khi học sinh cùng đăng nhập. Trong khi năm học này môn Tin học có tổng cộng 25 lớp, tần suất sử dụng phòng máy là liên tục cả sáng và chiều.
- **Cô Nguyễn Thị Thảo (GV môn Tin học):** Nếu phòng máy thiếu máy tính hoạt động tốt thì học sinh phải ngồi ghép 2 đến 3 em một máy, rất khó quản lý nề nếp và hiệu quả thực hành lập trình Scratch (khối 6, 7) và Python (khối 8, 9) sẽ giảm sút rõ rệt. Đề nghị Tổ trưởng kiến nghị Ban Giám hiệu mua bổ sung chuột, bàn phím dự phòng và cấu hình lại mạng nội bộ trước ngày 05/9.
- **Thầy Đinh Văn Đông (Hiệu trưởng):** Tiếp thu ý kiến xác đáng của thầy Tùng và cô Thảo. Nhà trường đã phê duyệt kinh phí bảo dưỡng thiết bị dạy học đầu năm. Giao bộ phận thiết bị phối hợp với thầy Tùng hoàn thành việc kiểm tra, thay thế linh kiện hư hỏng và sửa chữa dứt điểm đường truyền internet phòng máy xong trước ngày 02/9 để đảm bảo ngày 07/9 học sinh vào học thực hành thuận lợi.

**4. Thảo luận về triển khai Học bạ số và chữ ký số giáo viên (Thông tư số 70/2026/TT-BGDĐT):**
- **Thầy Hoàng Xuân Ánh (GV môn Toán):** Việc triển khai Học bạ số thay cho học bạ giấy là bước tiến lớn, giúp giảm bớt áp lực ghi chép thủ công. Tuy nhiên, một số thầy cô còn lúng túng trong thao tác cài đặt chứng thư số trên điện thoại thông minh (SmartCA / VNPT CA), việc xác thực ký số điện tử và quy trình kiểm tra dữ liệu điểm số trước khi ký để tránh sai lệch.
- **Thầy Hồ Đăng Danh (GV Tin học, CSDL ngành):** Đề xuất nhóm Tin học sẽ hỗ trợ kỹ thuật trực tiếp cho từng thầy cô trong tổ, hướng dẫn cài đặt app, kích hoạt chứng thư số và tổ chức một buổi thao tác ký số thử nghiệm trên hệ thống Cơ sở dữ liệu ngành vào đầu tháng 9.
- **Thầy Đinh Văn Đông (Hiệu trưởng):** Quán triệt nghiêm túc: Học bạ số là hồ sơ pháp lý liên thông quốc gia, giáo viên phải quản lý tài khoản ký số cá nhân như con dấu của mình, tuyệt đối không chia sẻ mật khẩu hay nhờ người khác ký hộ. Điểm số khi đã ký số sẽ khóa dữ liệu, sửa chữa rất phức tạp. Yêu cầu toàn thể giáo viên trong tổ nêu cao tinh thần trách nhiệm, vào điểm đúng hạn và kiểm tra thật kỹ trước khi ký số.

**5. Thảo luận về giải pháp phụ đạo học sinh yếu kém môn Toán và nề nếp chủ nhiệm:**
- **Thầy Nguyễn Văn Tính (GV môn Toán khối 6 & 7):** Học sinh lớp 6 mới chuyển cấp từ tiểu học lên còn bỡ ngỡ về phương pháp học THCS; kỹ năng trình bày bài toán có lời văn và kỹ năng tính toán phân số, số thập phân còn nhiều hạn chế. Giáo viên dạy khối 6 cần kiên nhẫn, rèn phương pháp ghi chép và cách lập luận chuẩn mực ngay từ những tuần đầu tiên.
- **Thầy Trần Long Hải (GV môn Toán, GVCN lớp 8/3):** Đồng ý với thầy Tính. Đối với học sinh khối 8 và khối 9, ngay trong tháng 9 giáo viên bộ môn cần phối hợp chặt chẽ với giáo viên chủ nhiệm rà soát, lập danh sách học sinh có nguy cơ mất gốc kiến thức để có kế hoạch kèm cặp, phân công bạn học khá giúp đỡ bạn yếu trong 15 phút đầu giờ hoặc giao thêm bài tập vừa sức.
- **Thầy Hoàng Xuân Ánh (GV môn Toán):** Lưu ý thêm về công tác an toàn giao thông đầu năm: Đề nghị các giáo viên chủ nhiệm (đặc biệt khối 8, khối 9) phối hợp chặt chẽ với Tổng phụ trách Đội và phụ huynh nhắc nhở học sinh nghiêm túc đội mũ bảo hiểm khi đi xe đạp điện, xe máy điện tới trường.

## V. KẾT LUẬN VÀ BIỂU QUYẾT

- Thầy Tổ trưởng Hoàng Tấn Thiên tổng hợp các ý kiến thảo luận và kết luận: Toàn thể giáo viên trong tổ phát huy tinh thần đoàn kết, trách nhiệm, tập trung hoàn thiện Kế hoạch bài dạy theo chuẩn CV 5512, tích hợp hiệu quả Khung AI và Năng lực số, chủ động hỗ trợ học sinh và chuẩn bị tốt nhất cho năm học mới 2026 – 2027.
- **Biểu quyết:** 10/10 thành viên có mặt tán thành 100% với các nội dung đánh giá công tác tháng 8/2026, kế hoạch hoạt động tháng 9/2026 và các giải pháp chuyên môn đã thống nhất.

Biên bản cuộc họp kết thúc vào lúc 11 giờ 30 phút cùng ngày, đã được đọc lại cho toàn thể các thành viên cùng nghe, nhất trí thông qua và ký xác nhận dưới đây; biên bản được lập thành 02 bản có giá trị như nhau, lưu hồ sơ tổ chuyên môn và gửi Ban Giám hiệu nhà trường./.

---

| **THƯ KÝ CUỘC HỌP**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Lê Thị Bình** | **TỔ TRƯỞNG CHUYÊN MÔN**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Hoàng Tấn Thiên** |
|:---:|:---:|

**CÁC THÀNH VIÊN KHÁC CỦA TỔ CHUYÊN MÔN KÝ XÁC NHẬN:**

| Đinh Văn Đông | Trần Sáng | Hồ Đăng Danh | Hoàng Xuân Ánh |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |

| Trần Long Hải | Nguyễn Thị Thảo | Nguyễn Văn Tính | Dương Quang Tùng |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


def tao_bien_ban_hop_to_lan_1_thang_9(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 1 Tháng 9/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # 1. Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="02/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 12 tháng 9 năm 2026"
    )
    
    # 2. Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1",
        "SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 9/2026 (LẦN 1)\nNăm học: 2026 - 2027"
    )
    
    # 3. Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 07 giờ 30 phút, ngày 12 tháng 9 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 9 năm học 2026 – 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # 4. NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt các văn bản chỉ đạo trọng tâm của Bộ Giáo dục và Đào tạo, Sở Giáo dục và Đào tạo và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:", indent=True)
    
    # 1. Công văn 5512/BGDĐT-GDTrH
    add_paragraph_styled(doc, "**1. Hướng dẫn xây dựng và tổ chức thực hiện kế hoạch giáo dục của nhà trường (Công văn số 5512/BGDĐT-GDTrH ngày 18/12/2020 của Bộ GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Quy định chuẩn hóa hệ thống hồ sơ kế hoạch giáo dục của tổ chuyên môn và giáo viên bao gồm: (1) **Phụ lục 1** – Khung kế hoạch dạy học môn học của tổ chuyên môn (phân phối chương trình 35 tuần, yêu cầu cần đạt, thiết bị dạy học, phòng học bộ môn); (2) **Phụ lục 2** – Khung kế hoạch tổ chức các hoạt động giáo dục của tổ chuyên môn (chuyên đề, chủ đề liên môn, bài học STEM); (3) **Phụ lục 3** – Khung kế hoạch giáo dục của giáo viên trong năm học (kế hoạch cá nhân theo phân công chuyên môn, chỉ tiêu, bồi dưỡng học sinh); (4) **Phụ lục 4** – Khung kế hoạch bài dạy (KHBD) cấu trúc 4 hoạt động: Mở đầu/Khởi động, Hình thành kiến thức mới, Luyện tập, Vận dụng.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Các nhóm bộ môn (Toán 6, 7, 8, 9; Tin học 6, 7, 8, 9) hoàn thiện Phụ lục 1, Phụ lục 2 và từng cá nhân hoàn thiện Phụ lục 3 nộp phê duyệt trên Cơ sở dữ liệu ngành chậm nhất ngày 30/9/2026; đặc biệt, bắt buộc tích hợp **Khung Năng lực số (20% số tiết)** và **12 tiết Khung AI** vào Phụ lục 1, Phụ lục 3 và thể hiện in đậm, in nghiêng rõ nét trong Kế hoạch bài dạy (Phụ lục 4) để phục vụ kiểm tra, duyệt giáo án ký số.", indent=True)
    
    # 2. Hội thi giáo dục phòng chống ma túy
    add_paragraph_styled(doc, "**2. Kế hoạch tham gia Hội thi giáo dục phòng, chống ma túy năm học 2026 – 2027 (Kế hoạch số 81/KH-THCS.TP ngày 11/9/2026 của Trường THCS Trần Phú và Kế hoạch số 4777/KH-SGDĐT của Sở GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Mỗi sản phẩm dự thi gồm 01 Kế hoạch bài dạy (hoặc Kế hoạch tổ chức hoạt động giáo dục) + 01 Bài giảng điện tử tương ứng bám sát chủ đề phòng, chống ma túy trong học đường; toàn bộ sản phẩm được số hóa, đóng gói dưới dung lượng 1GB; sản phẩm có tính nguyên gốc do chính giáo viên xây dựng; được phép sử dụng công cụ số/AI hỗ trợ thiết kế nhưng không dùng AI thay thế phần sáng tạo và chuyên môn của tác giả; hạn nộp cấp trường ngày 20/9/2026 và nộp về Sở GD&ĐT trước ngày 25/9/2026.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phân công **Thầy Trần Sáng** và **Cô Lê Thị Bình** trực tiếp biên soạn 02 sản phẩm đại diện tổ tham gia dự thi; Thầy Tổ trưởng theo dõi tiến độ, chủ trì phiên họp tổ góp ý chuyên môn và thẩm định sản phẩm trước khi nộp Ban Giám hiệu; các thành viên trong tổ hỗ trợ tư liệu, video học liệu và kỹ thuật công nghệ thông tin phục vụ đóng gói bài giảng điện tử.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ CÔNG TÁC GIAI ĐOẠN ĐẦU THÁNG 9/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm các khối lớp đã nhanh chóng ổn định tổ chức nề nếp lớp chủ nhiệm ngay từ ngày tựu trường; duy trì nghiêm túc sinh hoạt 15 phút đầu giờ trước buổi học; hoàn thành phổ biến nội quy trường lớp, kiện toàn ban cán sự lớp.", indent=True)
    add_paragraph_styled(doc, "- Đã lập danh sách học sinh có hoàn cảnh khó khăn đề nghị nhà trường trao quà, học bổng trong lễ khai giảng ngày 05/9/2026; cùng học sinh tham gia vệ sinh phong quang trường lớp chuẩn bị chu đáo cho ngày hội khai trường.", indent=True)
    
    add_section_h2(doc, "2. Kỷ luật lao động và ngày giờ công:")
    add_paragraph_styled(doc, "- 100% giáo viên trong tổ chấp hành nghiêm túc quy định ngày giờ công, tham gia đầy đủ lễ khai giảng năm học mới ngày 05/9/2026 và các buổi hội họp của nhà trường; giảng dạy đúng thời khóa biểu chính thức bắt đầu từ ngày 07/9/2026.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- Các nhóm bộ môn đã thống nhất cấu trúc soạn Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH; bắt đầu đưa giáo án lên Cơ sở dữ liệu ngành để ký số tuần.", indent=True)
    add_paragraph_styled(doc, "- Tổ chức dạy và học ổn định theo thời khóa biểu áp dụng từ 07/9/2026; thực hiện tốt kế hoạch dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT.", indent=True)
    add_paragraph_styled(doc, "- Tham gia đầy đủ các buổi tập huấn chuyên môn trực tuyến về chuyển đổi số, tập huấn dạy học và kiểm tra đánh giá trên nền tảng OLM.", indent=True)
    
    add_section_h2(doc, "4. Phòng bộ môn và thiết bị dạy học:")
    add_paragraph_styled(doc, "- Đã kiểm tra nề nếp ra vào lớp học, phòng máy vi tính bộ môn; rà soát thiết bị dạy học và cơ sở vật chất 02 phòng máy sau đợt bảo dưỡng đầu năm của nhà trường.", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. KẾ HOẠCH TRỌNG TÂM THỜI GIAN TỚI (THÁNG 9 & ĐẦU THÁNG 10/2026)")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Ổn định vững chắc nề nếp lớp chủ nhiệm, củng cố đội ngũ cán bộ lớp, tham gia họp GVCN; xây dựng Kế hoạch chủ nhiệm năm học 2026 – 2027.", indent=True)
    add_paragraph_styled(doc, "- Đẩy mạnh tuyên truyền thực hiện Tháng An toàn giao thông, tổ chức cho 100% học sinh ký cam kết đội mũ bảo hiểm khi đi xe máy điện, xe đạp điện; tuyên truyền phòng chống tệ nạn xã hội và dịch bệnh.", indent=True)
    add_paragraph_styled(doc, "- Cập nhật, rà soát hoàn thiện 100% thông tin học sinh lớp chủ nhiệm trên hệ thống Cơ sở dữ liệu ngành.", indent=True)
    add_paragraph_styled(doc, "- Chuẩn bị chu đáo nội dung họp cha mẹ học sinh đầu năm; giữ gìn sổ đầu bài cẩn thận, nhắc nhở giáo viên bộ môn ghi chép đầy đủ các cột mục và GVCN tổng hợp ký tuần.", indent=True)
    
    add_section_h2(doc, "2. Kỷ luật ngày giờ công:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ phấn đấu bảo đảm ngày giờ công, chấp hành nghiêm túc thời khóa biểu, không đi trễ về sớm; thực hiện nghiêm túc quy định dạy thay, dạy bù khi có giáo viên đi công tác hoặc ốm đau.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- **Hoàn thành các Phụ lục theo Công văn 5512:** Các nhóm bộ môn Toán, Tin học hoàn thiện Kế hoạch dạy học của tổ (Phụ lục 1), Kế hoạch tổ chức các hoạt động giáo dục (Phụ lục 2) và Kế hoạch giáo dục của giáo viên (Phụ lục 3), nộp phê duyệt trên CSDL ngành chậm nhất ngày 30/9/2026.", indent=True)
    add_paragraph_styled(doc, "- **Tham gia Hội thi giáo dục phòng, chống ma túy:** Thầy Sáng, Cô Bình hoàn thành KHBD và bài giảng điện tử trước 20/9 để tổ góp ý hoàn thiện, nộp Ban Giám hiệu xét chọn gửi Sở GD&ĐT trước 25/9.", indent=True)
    add_paragraph_styled(doc, "- **Phát động các phong trào thi trực tuyến:**", indent=True)
    add_paragraph_styled(doc, "  + *Đấu trường VioEdu môn Toán:* Phân công giáo viên phụ trách hướng dẫn học sinh đăng nhập và luyện tập: Khối 6 (Cô Thảo), Khối 7 (Thầy Ánh), Khối 8 (Cô Bình), Khối 9 (Thầy Sáng).", indent=True)
    add_paragraph_styled(doc, "  + *Cuộc thi IOE Tiếng Anh:* Phối hợp tổ Ngoại ngữ đôn đốc học sinh tham gia tự luyện các vòng điều kiện.", indent=True)
    add_paragraph_styled(doc, "- **Góp ý SGK Toán – Tin theo GDPT 2018 (Khó khăn & Biện pháp khắc phục):**", indent=True)
    add_paragraph_styled(doc, "  + *SGK Toán 8 (Bài 10: Tứ giác lồi & tổng các góc bằng 360°):* Khó khăn học sinh khó hình dung khái niệm hai đỉnh cùng phía đối với đường thẳng chứa cạnh còn lại; dễ nhầm lẫn các góc nhỏ bị chia cắt bởi đường chéo. Biện pháp: Cho học sinh dùng phần mềm GeoGebra kéo thả đỉnh tứ giác, đánh số góc 1, 2 trước khi cộng góc.", indent=True)
    add_paragraph_styled(doc, "  + *SGK Toán 9 (Bài 11, 12: Tỉ số lượng giác & Hệ thức cạnh – góc trong tam giác vuông):* Khó khăn học sinh nhầm lẫn cạnh đối/kề, khó mô hình hóa bài toán thực tế. Biện pháp: Dùng câu vè quen thuộc \"Sao Đi Học, Cứ Khóc Hoài, Thôi Đi Tắm, Cùng Đi Tắm\", áp dụng phương pháp \"Xác định góc nhìn\" và tăng cường vẽ sơ đồ tam giác vuông từ tình huống thực tế (chiều cao cây, tòa nhà, bóng nắng).", indent=True)
    
    add_section_h2(doc, "4. Ngoại khóa và các hoạt động khác:")
    add_paragraph_styled(doc, "- Thực hiện hoạt động ngoài giờ lên lớp theo chủ điểm \"Truyền thống nhà trường\"; tham gia tổ chức Tết Trung thu cho học sinh toàn trường.", indent=True)
    add_paragraph_styled(doc, "- Chuẩn bị tốt hồ sơ sổ sách, kế hoạch bài dạy phục vụ công tác Kiểm tra nội bộ của nhà trường trong tháng 10/2026.", indent=True)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. THẢO LUẬN CHUYÊN MÔN VÀ Ý KIẾN CỦA CÁC THÀNH VIÊN TRONG TỔ")
    add_paragraph_styled(doc, "Cuộc họp đã dành phần lớn thời gian để thảo luận chuyên sâu vào trọng tâm: **Phương pháp và giải pháp kỹ thuật tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI vào Kế hoạch bài dạy 5512**, đồng thời tháo gỡ các vướng mắc thực tế khi triển khai tại trường THCS Trần Phú:", indent=True)
    
    # Thảo luận 1: Kỹ thuật tích hợp NLS và AI vào tiến trình 4 hoạt động của CV 5512
    add_paragraph_styled(doc, "**1. Thảo luận về kỹ thuật tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI vào KHBD theo CV 5512:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Tấn Thiên (Tổ trưởng chuyên môn / Chủ trì):** Đặt vấn đề thảo luận: Theo hướng dẫn của Sở GD&ĐT tại Công văn 4200 và Công văn 5588 của Bộ GD&ĐT, năm học 2026 – 2027 bắt buộc phải thể hiện rõ việc tích hợp Khung Năng lực số (NLS) tối thiểu 20% tổng số tiết và 12 tiết Khung AI vào Kế hoạch bài dạy. Tuy nhiên, qua rà soát bước đầu, nhiều giáo viên còn lúng túng: Ghi mục tiêu NLS và AI ở vị trí nào trong giáo án 5512? Thiết kế hoạt động của học sinh ra sao để không biến tiết Toán thành tiết Tin học và không làm quá tải thời lượng 45 phút? Đề nghị các thầy cô đi thẳng vào giải pháp kỹ thuật cụ thể.", indent=True)
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (GV môn Toán khối 7 & 8):** Phân tích quy trình biên soạn cụ thể: Trong giáo án 5512, tại mục I. MỤC TIÊU (phần Năng lực), giáo viên bổ sung thêm chỉ báo: `*Năng lực số (NLS)*` và `*Năng lực Trí tuệ nhân tạo (AI)*`. Trong tiến trình 4 hoạt động dạy học, vị trí thích hợp nhất để tích hợp là **Hoạt động 3 (Luyện tập)** hoặc **Hoạt động 4 (Vận dụng)**. Ví dụ: Trong bài Thống kê biểu đồ (Toán 7) hoặc bài Hàm số và đồ thị (Toán 8), giáo viên giao nhiệm vụ cho học sinh dùng máy tính hoặc điện thoại thông minh tra cứu bảng số liệu thực tế tại địa phương, hoặc dùng phần mềm vẽ đồ thị kiểm tra nghiệm. Phần mô tả hoạt động của giáo viên và học sinh có yếu tố số/AI bắt buộc phải **in đậm, in nghiêng** để làm căn cứ đánh giá duyệt giáo án ký số.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Trần Sáng (Phó Tổ trưởng, GV môn Toán 9):** Bổ sung kinh nghiệm môn Toán 9: Môn Toán 9 kiến thức rất nặng để ôn thi vào lớp 10, giáo viên không nên gượng ép tiết nào cũng đưa AI vào. Nhóm Toán 9 đã họp sơ bộ và thống nhất: Trong 12 tiết Khung AI, môn Toán 9 chỉ đăng ký tích hợp 03 tiết trọng điểm: (1) Tiết Luyện tập Tỉ số lượng giác (sử dụng công cụ mô phỏng AI / phần mềm đo đạc gián tiếp); (2) Tiết Đồ thị hàm số bậc nhất $y = ax + b$ (sử dụng phần mềm GeoGebra mô phỏng sự biến thiên của hệ số góc); (3) Tiết Bảng tần số và Biểu đồ tần số (sử dụng AI phân tích dữ liệu lớn). Các tiết còn lại, tích hợp NLS ở mức độ rèn luyện kỹ năng bấm máy tính cầm tay Casio FX-580VN/880BTG và làm bài tập trắc nghiệm số trên nền tảng OLM.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Tấn Thiên (Tổ trưởng):** Kết luận thống nhất: Cách tiếp cận của cô Bình và thầy Sáng là rất thực tế. Tuyệt đối không \"khoác áo AI\" một cách hình thức. Giao Thầy Sáng và Cô Bình hoàn thành 02 bài soạn mẫu có tích hợp NLS và AI (01 bài Toán 8, 01 bài Toán 9) đưa lên nhóm Zalo tổ trước ngày 18/9 để toàn tổ cùng áp dụng đồng bộ.", indent=True)
    
    # Thảo luận 2: Môn Tin học chủ lực gánh vác 12 tiết AI
    add_paragraph_styled(doc, "**2. Thảo luận về vai trò chủ lực của môn Tin học trong việc triển khai 12 tiết Khung AI cốt lõi:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (GV môn Tin học):** Khẳng định: Môn Tin học là môn học nòng cốt gánh vác 12 tiết AI cốt lõi theo hướng dẫn của Bộ GD&ĐT. Nhóm Tin học (thầy Tùng, thầy Danh, cô Thảo) đã đối chiếu chương trình SGK Tin học Cánh Diều cả 4 khối và xác định địa chỉ 12 tiết AI cụ thể: Khối 6 (Chủ đề E – Tìm kiếm thông tin và ứng dụng trợ lý số); Khối 7 (Chủ đề E – Thu thập, xử lý và trực quan hóa bảng tính); Khối 8 (Chủ đề F – Bước đầu làm quen với thuật toán học máy và phân loại dữ liệu); Khối 9 (Chủ đề D & F – Sử dụng AI tạo sinh có trách nhiệm, bảo mật dữ liệu và đạo đức số). Nhóm Tin học sẽ đưa toàn bộ 12 tiết này vào Kế hoạch dạy học (Phụ lục 1) môn Tin học nộp về nhà trường.", indent=True)
    add_paragraph_styled(doc, "- **Cô Nguyễn Thị Thảo (GV môn Tin học):** Để học sinh thực hành tốt 12 tiết AI, phòng máy vi tính cần được cài đặt sẵn các tiện ích mô phỏng và bảo đảm đường truyền internet ổn định. Đề nghị trong các tiết học AI, giáo viên cho học sinh thực hành nhóm đôi, có sản phẩm cụ thể (bài trình chiếu, poster số, đoạn mã lập trình Scratch đơn giản ứng dụng nhận dạng hình ảnh) để học sinh hứng thú học tập.", indent=True)
    
    # Thảo luận 3: Quy trình hoàn thiện Phụ lục 1, 2, 3 và đưa lên CSDL ngành
    add_paragraph_styled(doc, "**3. Thảo luận về quy trình hoàn thiện Phụ lục 1, 2, 3 theo Công văn 5512 và đưa lên CSDL ngành:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hồ Đăng Danh (GV Tin học, phụ trách kỹ thuật CSDL ngành):** Lưu ý các thầy cô trong tổ: Năm học này Sở GD&ĐT kiểm tra hồ sơ giáo án hoàn toàn trên môi trường số. Khi các nhóm bộ môn hoàn thành Phụ lục 1 (Kế hoạch dạy học theo 35 tuần) và Phụ lục 2 (Kế hoạch hoạt động giáo dục), trưởng nhóm phải rà soát thật kỹ số tiết, tên bài học khớp 100% với thời khóa biểu và PPCT. Riêng Phụ lục 3 của từng giáo viên, phần \"Kế hoạch thực hiện chương trình\" phải thể hiện rõ các tuần kiểm tra giữa kỳ, cuối kỳ và các tiết tích hợp NLS/AI. Thầy Danh sẽ trực tiếp hỗ trợ các thầy cô tải tệp lên hệ thống và ký số phê duyệt đúng hạn trước ngày 30/9.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Đinh Văn Đông (Hiệu trưởng):** Quán triệt: Phụ lục 1, 2, 3 theo CV 5512 là \"xương sống\" pháp lý của toàn bộ hoạt động chuyên môn trong năm học. Sau khi Hiệu trưởng phê duyệt trên CSDL ngành, giáo viên phải thực hiện nghiêm túc theo đúng tiến độ, không tự ý đảo tiết hay cắt xén chương trình. Ban Giám hiệu sẽ kiểm tra ngẫu nhiên hồ sơ sổ sách và việc ký số hàng tuần của từng giáo viên.", indent=True)
    
    # Thảo luận 4: Phối hợp phát động VioEdu và kiểm tra thường xuyên qua OLM
    add_paragraph_styled(doc, "**4. Thảo luận về phối hợp phát động Đấu trường VioEdu Toán và kiểm tra thường xuyên qua OLM:**", indent=True)
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (GV môn Toán khối 7):** Đề nghị giáo viên dạy Toán các khối 6, 7, 8, 9 lập danh sách từ 5 đến 10 học sinh có học lực khá, giỏi môn Toán mỗi lớp chuyển cho quản trị trường để kích hoạt tài khoản VioEdu thi đấu vòng trường. Đồng thời, đề nghị Ban Giám hiệu và Tổng phụ trách Đội đưa phong trào VioEdu vào tiêu chí chấm điểm thi đua tuần giữa các lớp để tạo động lực cho học sinh tham gia đông đảo.", indent=True)
    add_paragraph_styled(doc, "- **Thầy Trần Long Hải (GV môn Toán, GVCN lớp 8/3):** Cần nhắc nhở giáo viên bộ môn khi giao bài tập rèn luyện trên VioEdu hoặc OLM phải hướng dẫn cụ thể cách đăng nhập cho học sinh, đặc biệt học sinh lớp 6 mới vào trường, tránh để phụ huynh phải phản ánh vì không biết cách thao tác.", indent=True)
    
    # Thảo luận 5: Chuẩn bị hồ sơ chuyên môn cho công tác Kiểm tra nội bộ tháng 10
    add_paragraph_styled(doc, "**5. Thảo luận về chuẩn bị hồ sơ chuyên môn cho công tác Kiểm tra nội bộ tháng 10/2026:**", indent=True)
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh & Thầy Nguyễn Văn Tính:** Tháng 10 tới nhà trường sẽ triển khai kiểm tra toàn diện và kiểm tra chuyên môn định kỳ theo kế hoạch kiểm tra nội bộ. Giáo viên trong tổ cần chủ động rà soát Kế hoạch bài dạy 4 hoạt động, sổ đầu bài, việc ghi nhận xét và vào điểm thường xuyên đợt 1 trên hệ thống SMAS/CSDL ngành, bảo đảm khớp tiến độ từng ngày, không để dồn việc vào cuối đợt kiểm tra.", indent=True)
    
    # ==================== PHẦN V ====================
    add_section_h1(doc, "V. KẾT LUẬN VÀ BIỂU QUYẾT")
    add_paragraph_styled(doc, "- Thầy Tổ trưởng Hoàng Tấn Thiên tổng hợp các ý kiến thảo luận và kết luận: Toàn thể giáo viên trong tổ phát huy tinh thần đoàn kết, trách nhiệm, tập trung hoàn thiện hệ thống hồ sơ Phụ lục 1, 2, 3 theo Công văn 5512 trước ngày 30/9; thực hiện nghiêm túc việc tích hợp Năng lực số và 12 tiết Khung AI vào KHBD; chuẩn bị tốt nhất các điều kiện chuyên môn phục vụ giảng dạy và kiểm tra nội bộ tháng 10.", indent=True)
    add_paragraph_styled(doc, "- **Biểu quyết:** 10/10 thành viên có mặt tán thành 100% với các nội dung đánh giá công tác đầu tháng 9, kế hoạch trọng tâm và các giải pháp chuyên môn đã thống nhất.", indent=True)
    add_paragraph_styled(doc, "Biên bản cuộc họp kết thúc vào lúc 10 giờ 00 phút cùng ngày, đã được đọc lại cho toàn thể các thành viên cùng nghe, nhất trí thông qua và ký xác nhận dưới đây; biên bản được lập thành 02 bản có giá trị như nhau, lưu hồ sơ tổ chuyên môn và gửi Ban Giám hiệu nhà trường./.", indent=True)
    
    # 5. Khung chữ ký chuẩn
    add_bien_ban_signatures(
        doc,
        chu_tri="Hoàng Tấn Thiên",
        thu_ky="Lê Thị Bình"
    )
    
    # 6. Danh sách các thành viên khác của tổ ký xác nhận
    p_tv = doc.add_paragraph()
    p_tv.paragraph_format.space_before = Pt(12)
    p_tv.paragraph_format.space_after = Pt(4)
    r_tv = p_tv.add_run("CÁC THÀNH VIÊN KHÁC CỦA TỔ CHUYÊN MÔN KÝ XÁC NHẬN:\n")
    r_tv.font.name = 'Times New Roman'
    r_tv.font.size = Pt(13)
    r_tv.bold = True
    
    table_tv = doc.add_table(rows=2, cols=4)
    table_tv.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_tv.autofit = False
    
    for r in table_tv.rows:
        for c in r.cells:
            tcPr = c._tc.get_or_add_tcPr()
            tcBorders = parse_xml(r'<w:tcBorders {}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>'.format(nsdecls('w')))
            tcPr.append(tcBorders)
            
    members_r1 = ["Đinh Văn Đông", "Trần Sáng", "Hồ Đăng Danh", "Hoàng Xuân Ánh"]
    members_r2 = ["Trần Long Hải", "Nguyễn Thị Thảo", "Nguyễn Văn Tính", "Dương Quang Tùng"]
    
    for i, name in enumerate(members_r1):
        cell = table_tv.rows[0].cells[i]
        cell.width = Inches(1.7)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(25)
        r = p.add_run(f"(Ký tên)\n\n\n**{name}**")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    for i, name in enumerate(members_r2):
        cell = table_tv.rows[1].cells[i]
        cell.width = Inches(1.7)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(25)
        r = p.add_run(f"(Ký tên)\n\n\n**{name}**")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        
    os.makedirs(os.path.dirname(out_docx_path), exist_ok=True)
    save_docx_robust(doc, out_docx_path)
    print(f"Da xuat thanh cong file Word: {out_docx_path}")
    
    if out_md_path:
        os.makedirs(os.path.dirname(out_md_path), exist_ok=True)
        tao_bien_ban_hop_to_lan_1_thang_9_md(out_md_path)
        print(f"Da xuat thanh cong file Markdown: {out_md_path}")

def tao_bien_ban_hop_to_lan_1_thang_9_md(out_md_path):
    """Xuất phiên bản Markdown cho Biên bản họp tổ Lần 1 Tháng 9/2026."""
    md_content = """<div align="center">

| **TRƯỜNG THCS TRẦN PHÚ**<br>**TỔ TOÁN - TIN HỌC**<br>Số: 02/BB-TCM | **CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM**<br>**Độc lập – Tự do – Hạnh phúc**<br>──────────────────<br>*Xuân Đông, ngày 12 tháng 9 năm 2026* |
|:---:|:---:|

---

# BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1
### SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 9/2026 (LẦN 1)
*(Năm học: 2026 – 2027)*
──────────────────

</div>

Hôm nay, vào lúc 07 giờ 30 phút, ngày 12 tháng 9 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 9 năm học 2026 – 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.  
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.  
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).  
  + *Danh sách thành viên:* Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

<div align="center">

### NỘI DUNG CUỘC HỌP

</div>

## I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN

Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt các văn bản chỉ đạo trọng tâm của Bộ Giáo dục và Đào tạo, Sở Giáo dục và Đào tạo và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:

**1. Hướng dẫn xây dựng và tổ chức thực hiện kế hoạch giáo dục của nhà trường (Công văn số 5512/BGDĐT-GDTrH ngày 18/12/2020 của Bộ GD&ĐT):**
- **Ý chính cốt lõi:** Quy định chuẩn hóa hệ thống hồ sơ kế hoạch giáo dục của tổ chuyên môn và giáo viên bao gồm: (1) **Phụ lục 1** – Khung kế hoạch dạy học môn học của tổ chuyên môn (phân phối chương trình 35 tuần, yêu cầu cần đạt, thiết bị dạy học, phòng học bộ môn); (2) **Phụ lục 2** – Khung kế hoạch tổ chức các hoạt động giáo dục của tổ chuyên môn (chuyên đề, chủ đề liên môn, bài học STEM); (3) **Phụ lục 3** – Khung kế hoạch giáo dục của giáo viên trong năm học (kế hoạch cá nhân theo phân công chuyên môn, chỉ tiêu, bồi dưỡng học sinh); (4) **Phụ lục 4** – Khung kế hoạch bài dạy (KHBD) cấu trúc 4 hoạt động: Mở đầu/Khởi động, Hình thành kiến thức mới, Luyện tập, Vận dụng.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Các nhóm bộ môn (Toán 6, 7, 8, 9; Tin học 6, 7, 8, 9) hoàn thiện Phụ lục 1, Phụ lục 2 và từng cá nhân hoàn thiện Phụ lục 3 nộp phê duyệt trên Cơ sở dữ liệu ngành chậm nhất ngày 30/9/2026; đặc biệt, bắt buộc tích hợp **Khung Năng lực số (20% số tiết)** và **12 tiết Khung AI** vào Phụ lục 1, Phụ lục 3 và thể hiện in đậm, in nghiêng rõ nét trong Kế hoạch bài dạy (Phụ lục 4) để phục vụ kiểm tra, duyệt giáo án ký số.

**2. Kế hoạch tham gia Hội thi giáo dục phòng, chống ma túy năm học 2026 – 2027 (Kế hoạch số 81/KH-THCS.TP ngày 11/9/2026 của Trường THCS Trần Phú và Kế hoạch số 4777/KH-SGDĐT của Sở GD&ĐT):**
- **Ý chính cốt lõi:** Mỗi sản phẩm dự thi gồm 01 Kế hoạch bài dạy (hoặc Kế hoạch tổ chức hoạt động giáo dục) + 01 Bài giảng điện tử tương ứng bám sát chủ đề phòng, chống ma túy trong học đường; toàn bộ sản phẩm được số hóa, đóng gói dưới dung lượng 1GB; sản phẩm có tính nguyên gốc do chính giáo viên xây dựng; được phép sử dụng công cụ số/AI hỗ trợ thiết kế nhưng không dùng AI thay thế phần sáng tạo và chuyên môn của tác giả; hạn nộp cấp trường ngày 20/9/2026 và nộp về Sở GD&ĐT trước ngày 25/9/2026.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phân công **Thầy Trần Sáng** và **Cô Lê Thị Bình** trực tiếp biên soạn 02 sản phẩm đại diện tổ tham gia dự thi; Thầy Tổ trưởng theo dõi tiến độ, chủ trì phiên họp tổ góp ý chuyên môn và thẩm định sản phẩm trước khi nộp Ban Giám hiệu; các thành viên trong tổ hỗ trợ tư liệu, video học liệu và kỹ thuật công nghệ thông tin phục vụ đóng gói bài giảng điện tử.

## II. ĐÁNH GIÁ CÔNG TÁC GIAI ĐOẠN ĐẦU THÁNG 9/2026

### **1. Công tác chủ nhiệm:**
- Giáo viên chủ nhiệm các khối lớp đã nhanh chóng ổn định tổ chức nề nếp lớp chủ nhiệm ngay từ ngày tựu trường; duy trì nghiêm túc sinh hoạt 15 phút đầu giờ trước buổi học; hoàn thành phổ biến nội quy trường lớp, kiện toàn ban cán sự lớp.
- Đã lập danh sách học sinh có hoàn cảnh khó khăn đề nghị nhà trường trao quà, học bổng trong lễ khai giảng ngày 05/9/2026; cùng học sinh tham gia vệ sinh phong quang trường lớp chuẩn bị chu đáo cho ngày hội khai trường.

### **2. Kỷ luật lao động và ngày giờ công:**
- 100% giáo viên trong tổ chấp hành nghiêm túc quy định ngày giờ công, tham gia đầy đủ lễ khai giảng năm học mới ngày 05/9/2026 và các buổi hội họp của nhà trường; giảng dạy đúng thời khóa biểu chính thức bắt đầu từ ngày 07/9/2026.

### **3. Công tác chuyên môn:**
- Các nhóm bộ môn đã thống nhất cấu trúc soạn Kế hoạch bài dạy theo Công văn 5512/BGDĐT-GDTrH; bắt đầu đưa giáo án lên Cơ sở dữ liệu ngành để ký số tuần.
- Tổ chức dạy và học ổn định theo thời khóa biểu áp dụng từ 07/9/2026; thực hiện tốt kế hoạch dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT.
- Tham gia đầy đủ các buổi tập huấn chuyên môn trực tuyến về chuyển đổi số, tập huấn dạy học và kiểm tra đánh giá trên nền tảng OLM.

### **4. Phòng bộ môn và thiết bị dạy học:**
- Đã kiểm tra nề nếp ra vào lớp học, phòng máy vi tính bộ môn; rà soát thiết bị dạy học và cơ sở vật chất 02 phòng máy sau đợt bảo dưỡng đầu năm của nhà trường.

## III. KẾ HOẠCH TRỌNG TÂM THỜI GIAN TỚI (THÁNG 9 & ĐẦU THÁNG 10/2026)

### **1. Công tác chủ nhiệm:**
- Ổn định vững chắc nề nếp lớp chủ nhiệm, củng cố đội ngũ cán bộ lớp, tham gia họp GVCN; xây dựng Kế hoạch chủ nhiệm năm học 2026 – 2027.
- Đẩy mạnh tuyên truyền thực hiện Tháng An toàn giao thông, tổ chức cho 100% học sinh ký cam kết đội mũ bảo hiểm khi đi xe máy điện, xe đạp điện; tuyên truyền phòng chống tệ nạn xã hội và dịch bệnh.
- Cập nhật, rà soát hoàn thiện 100% thông tin học sinh lớp chủ nhiệm trên hệ thống Cơ sở dữ liệu ngành.
- Chuẩn bị chu đáo nội dung họp cha mẹ học sinh đầu năm; giữ gìn sổ đầu bài cẩn thận, nhắc nhở giáo viên bộ môn ghi chép đầy đủ các cột mục và GVCN tổng hợp ký tuần.

### **2. Kỷ luật ngày giờ công:**
- Giáo viên trong tổ phấn đấu bảo đảm ngày giờ công, chấp hành nghiêm túc thời khóa biểu, không đi trễ về sớm; thực hiện nghiêm túc quy định dạy thay, dạy bù khi có giáo viên đi công tác hoặc ốm đau.

### **3. Công tác chuyên môn:**
- **Hoàn thành các Phụ lục theo Công văn 5512:** Các nhóm bộ môn Toán, Tin học hoàn thiện Kế hoạch dạy học của tổ (Phụ lục 1), Kế hoạch tổ chức các hoạt động giáo dục (Phụ lục 2) và Kế hoạch giáo dục của giáo viên (Phụ lục 3), nộp phê duyệt trên CSDL ngành chậm nhất ngày 30/9/2026.
- **Tham gia Hội thi giáo dục phòng, chống ma túy:** Thầy Sáng, Cô Bình hoàn thành KHBD và bài giảng điện tử trước 20/9 để tổ góp ý hoàn thiện, nộp Ban Giám hiệu xét chọn gửi Sở GD&ĐT trước 25/9.
- **Phát động các phong trào thi trực tuyến:**
  + *Đấu trường VioEdu môn Toán:* Phân công giáo viên phụ trách hướng dẫn học sinh đăng nhập và luyện tập: Khối 6 (Cô Thảo), Khối 7 (Thầy Ánh), Khối 8 (Cô Bình), Khối 9 (Thầy Sáng).
  + *Cuộc thi IOE Tiếng Anh:* Phối hợp tổ Ngoại ngữ đôn đốc học sinh tham gia tự luyện các vòng điều kiện.
- **Góp ý SGK Toán – Tin theo GDPT 2018 (Khó khăn & Biện pháp khắc phục):**
  + *SGK Toán 8 (Bài 10: Tứ giác lồi & tổng các góc bằng 360°):* Khó khăn học sinh khó hình dung khái niệm hai đỉnh cùng phía đối với đường thẳng chứa cạnh còn lại; dễ nhầm lẫn các góc nhỏ bị chia cắt bởi đường chéo. Biện pháp: Cho học sinh dùng phần mềm GeoGebra kéo thả đỉnh tứ giác, đánh số góc 1, 2 trước khi cộng góc.
  + *SGK Toán 9 (Bài 11, 12: Tỉ số lượng giác & Hệ thức cạnh – góc trong tam giác vuông):* Khó khăn học sinh nhầm lẫn cạnh đối/kề, khó mô hình hóa bài toán thực tế. Biện pháp: Dùng câu vè quen thuộc "Sao Đi Học, Cứ Khóc Hoài, Thôi Đi Tắm, Cùng Đi Tắm", áp dụng phương pháp "Xác định góc nhìn" và tăng cường vẽ sơ đồ tam giác vuông từ tình huống thực tế (chiều cao cây, tòa nhà, bóng nắng).

### **4. Ngoại khóa và các hoạt động khác:**
- Thực hiện hoạt động ngoài giờ lên lớp theo chủ điểm "Truyền thống nhà trường"; tham gia tổ chức Tết Trung thu cho học sinh toàn trường.
- Chuẩn bị tốt hồ sơ sổ sách, kế hoạch bài dạy phục vụ công tác Kiểm tra nội bộ của nhà trường trong tháng 10/2026.

## IV. THẢO LUẬN CHUYÊN MÔN VÀ Ý KIẾN CỦA CÁC THÀNH VIÊN TRONG TỔ

Cuộc họp đã dành phần lớn thời gian để thảo luận chuyên sâu vào trọng tâm: **Phương pháp và giải pháp kỹ thuật tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI vào Kế hoạch bài dạy 5512**, đồng thời tháo gỡ các vướng mắc thực tế khi triển khai tại trường THCS Trần Phú:

**1. Thảo luận về kỹ thuật tích hợp Khung Năng lực số (20%) và 12 tiết Khung AI vào KHBD theo CV 5512:**
- **Thầy Hoàng Tấn Thiên (Tổ trưởng chuyên môn / Chủ trì):** Đặt vấn đề thảo luận: Theo hướng dẫn của Sở GD&ĐT tại Công văn 4200 và Công văn 5588 của Bộ GD&ĐT, năm học 2026 – 2027 bắt buộc phải thể hiện rõ việc tích hợp Khung Năng lực số (NLS) tối thiểu 20% tổng số tiết và 12 tiết Khung AI vào Kế hoạch bài dạy. Tuy nhiên, qua rà soát bước đầu, nhiều giáo viên còn lúng túng: Ghi mục tiêu NLS và AI ở vị trí nào trong giáo án 5512? Thiết kế hoạt động của học sinh ra sao để không biến tiết Toán thành tiết Tin học và không làm quá tải thời lượng 45 phút? Đề nghị các thầy cô đi thẳng vào giải pháp kỹ thuật cụ thể.
- **Cô Lê Thị Bình (GV môn Toán khối 7 & 8):** Phân tích quy trình biên soạn cụ thể: Trong giáo án 5512, tại mục I. MỤC TIÊU (phần Năng lực), giáo viên bổ sung thêm chỉ báo: `*Năng lực số (NLS)*` và `*Năng lực Trí tuệ nhân tạo (AI)*`. Trong tiến trình 4 hoạt động dạy học, vị trí thích hợp nhất để tích hợp là **Hoạt động 3 (Luyện tập)** hoặc **Hoạt động 4 (Vận dụng)**. Ví dụ: Trong bài Thống kê biểu đồ (Toán 7) hoặc bài Hàm số và đồ thị (Toán 8), giáo viên giao nhiệm vụ cho học sinh dùng máy tính hoặc điện thoại thông minh tra cứu bảng số liệu thực tế tại địa phương, hoặc dùng phần mềm vẽ đồ thị kiểm tra nghiệm. Phần mô tả hoạt động của giáo viên và học sinh có yếu tố số/AI bắt buộc phải **in đậm, in nghiêng** để làm căn cứ đánh giá duyệt giáo án ký số.
- **Thầy Trần Sáng (Phó Tổ trưởng, GV môn Toán 9):** Bổ sung kinh nghiệm môn Toán 9: Môn Toán 9 kiến thức rất nặng để ôn thi vào lớp 10, giáo viên không nên gượng ép tiết nào cũng đưa AI vào. Nhóm Toán 9 đã họp sơ bộ và thống nhất: Trong 12 tiết Khung AI, môn Toán 9 chỉ đăng ký tích hợp 03 tiết trọng điểm: (1) Tiết Luyện tập Tỉ số lượng giác (sử dụng công cụ mô phỏng AI / phần mềm đo đạc gián tiếp); (2) Tiết Đồ thị hàm số bậc nhất $y = ax + b$ (sử dụng phần mềm GeoGebra mô phỏng sự biến thiên của hệ số góc); (3) Tiết Bảng tần số và Biểu đồ tần số (sử dụng AI phân tích dữ liệu lớn). Các tiết còn lại, tích hợp NLS ở mức độ rèn luyện kỹ năng bấm máy tính cầm tay Casio FX-580VN/880BTG và làm bài tập trắc nghiệm số trên nền tảng OLM.
- **Thầy Hoàng Tấn Thiên (Tổ trưởng):** Kết luận thống nhất: Cách tiếp cận của cô Bình và thầy Sáng là rất thực tế. Tuyệt đối không "khoác áo AI" một cách hình thức. Giao Thầy Sáng và Cô Bình hoàn thành 02 bài soạn mẫu có tích hợp NLS và AI (01 bài Toán 8, 01 bài Toán 9) đưa lên nhóm Zalo tổ trước ngày 18/9 để toàn tổ cùng áp dụng đồng bộ.

**2. Thảo luận về vai trò chủ lực của môn Tin học trong việc triển khai 12 tiết Khung AI cốt lõi:**
- **Thầy Dương Quang Tùng (GV môn Tin học):** Khẳng định: Môn Tin học là môn học nòng cốt gánh vác 12 tiết AI cốt lõi theo hướng dẫn của Bộ GD&ĐT. Nhóm Tin học (thầy Tùng, thầy Danh, cô Thảo) đã đối chiếu chương trình SGK Tin học Cánh Diều cả 4 khối và xác định địa chỉ 12 tiết AI cụ thể: Khối 6 (Chủ đề E – Tìm kiếm thông tin và ứng dụng trợ lý số); Khối 7 (Chủ đề E – Thu thập, xử lý và trực quan hóa bảng tính); Khối 8 (Chủ đề F – Bước đầu làm quen với thuật toán học máy và phân loại dữ liệu); Khối 9 (Chủ đề D & F – Sử dụng AI tạo sinh có trách nhiệm, bảo mật dữ liệu và đạo đức số). Nhóm Tin học sẽ đưa toàn bộ 12 tiết này vào Kế hoạch dạy học (Phụ lục 1) môn Tin học nộp về nhà trường.
- **Cô Nguyễn Thị Thảo (GV môn Tin học):** Để học sinh thực hành tốt 12 tiết AI, phòng máy vi tính cần được cài đặt sẵn các tiện ích mô phỏng và bảo đảm đường truyền internet ổn định. Đề nghị trong các tiết học AI, giáo viên cho học sinh thực hành nhóm đôi, có sản phẩm cụ thể (bài trình chiếu, poster số, đoạn mã lập trình Scratch đơn giản ứng dụng nhận dạng hình ảnh) để học sinh hứng thú học tập.

**3. Thảo luận về quy trình hoàn thiện Phụ lục 1, 2, 3 theo Công văn 5512 và đưa lên CSDL ngành:**
- **Thầy Hồ Đăng Danh (GV Tin học, phụ trách kỹ thuật CSDL ngành):** Lưu ý các thầy cô trong tổ: Năm học này Sở GD&ĐT kiểm tra hồ sơ giáo án hoàn toàn trên môi trường số. Khi các nhóm bộ môn hoàn thành Phụ lục 1 (Kế hoạch dạy học theo 35 tuần) và Phụ lục 2 (Kế hoạch hoạt động giáo dục), trưởng nhóm phải rà soát thật kỹ số tiết, tên bài học khớp 100% với thời khóa biểu và PPCT. Riêng Phụ lục 3 của từng giáo viên, phần "Kế hoạch thực hiện chương trình" phải thể hiện rõ các tuần kiểm tra giữa kỳ, cuối kỳ và các tiết tích hợp NLS/AI. Thầy Danh sẽ trực tiếp hỗ trợ các thầy cô tải tệp lên hệ thống và ký số phê duyệt đúng hạn trước ngày 30/9.
- **Thầy Đinh Văn Đông (Hiệu trưởng):** Quán triệt: Phụ lục 1, 2, 3 theo CV 5512 là "xương sống" pháp lý của toàn bộ hoạt động chuyên môn trong năm học. Sau khi Hiệu trưởng phê duyệt trên CSDL ngành, giáo viên phải thực hiện nghiêm túc theo đúng tiến độ, không tự ý đảo tiết hay cắt xén chương trình. Ban Giám hiệu sẽ kiểm tra ngẫu nhiên hồ sơ sổ sách và việc ký số hàng tuần của từng giáo viên.

**4. Thảo luận về phối hợp phát động Đấu trường VioEdu Toán và kiểm tra thường xuyên qua OLM:**
- **Cô Lê Thị Bình (GV môn Toán khối 7):** Đề nghị giáo viên dạy Toán các khối 6, 7, 8, 9 lập danh sách từ 5 đến 10 học sinh có học lực khá, giỏi môn Toán mỗi lớp chuyển cho quản trị trường để kích hoạt tài khoản VioEdu thi đấu vòng trường. Đồng thời, đề nghị Ban Giám hiệu và Tổng phụ trách Đội đưa phong trào VioEdu vào tiêu chí chấm điểm thi đua tuần giữa các lớp để tạo động lực cho học sinh tham gia đông đảo.
- **Thầy Trần Long Hải (GV môn Toán, GVCN lớp 8/3):** Cần nhắc nhở giáo viên bộ môn khi giao bài tập rèn luyện trên VioEdu hoặc OLM phải hướng dẫn cụ thể cách đăng nhập cho học sinh, đặc biệt học sinh lớp 6 mới vào trường, tránh để phụ huynh phải phản ánh vì không biết cách thao tác.

**5. Thảo luận về chuẩn bị hồ sơ chuyên môn cho công tác Kiểm tra nội bộ tháng 10/2026:**
- **Thầy Hoàng Xuân Ánh & Thầy Nguyễn Văn Tính:** Tháng 10 tới nhà trường sẽ triển khai kiểm tra toàn diện và kiểm tra chuyên môn định kỳ theo kế hoạch kiểm tra nội bộ. Giáo viên trong tổ cần chủ động rà soát Kế hoạch bài dạy 4 hoạt động, sổ đầu bài, việc ghi nhận xét và vào điểm thường xuyên đợt 1 trên hệ thống SMAS/CSDL ngành, bảo đảm khớp tiến độ từng ngày, không để dồn việc vào cuối đợt kiểm tra.

## V. KẾT LUẬN VÀ BIỂU QUYẾT

- Thầy Tổ trưởng Hoàng Tấn Thiên tổng hợp các ý kiến thảo luận và kết luận: Toàn thể giáo viên trong tổ phát huy tinh thần đoàn kết, trách nhiệm, tập trung hoàn thiện hệ thống hồ sơ Phụ lục 1, 2, 3 theo Công văn 5512 trước ngày 30/9; thực hiện nghiêm túc việc tích hợp Năng lực số và 12 tiết Khung AI vào KHBD; chuẩn bị tốt nhất các điều kiện chuyên môn phục vụ giảng dạy và kiểm tra nội bộ tháng 10.
- **Biểu quyết:** 10/10 thành viên có mặt tán thành 100% với các nội dung đánh giá công tác đầu tháng 9, kế hoạch trọng tâm và các giải pháp chuyên môn đã thống nhất.

Biên bản cuộc họp kết thúc vào lúc 10 giờ 00 phút cùng ngày, đã được đọc lại cho toàn thể các thành viên cùng nghe, nhất trí thông qua và ký xác nhận dưới đây; biên bản được lập thành 02 bản có giá trị như nhau, lưu hồ sơ tổ chuyên môn và gửi Ban Giám hiệu nhà trường./.

---

| **THƯ KÝ CUỘC HỌP**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Lê Thị Bình** | **TỔ TRƯỞNG CHUYÊN MÔN**<br>*(Ký, ghi rõ họ tên)*<br><br><br><br>**Hoàng Tấn Thiên** |
|:---:|:---:|

**CÁC THÀNH VIÊN KHÁC CỦA TỔ CHUYÊN MÔN KÝ XÁC NHẬN:**

| Đinh Văn Đông | Trần Sáng | Hồ Đăng Danh | Hoàng Xuân Ánh |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |

| Trần Long Hải | Nguyễn Thị Thảo | Nguyễn Văn Tính | Dương Quang Tùng |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


def tao_bien_ban_hop_to_lan_2_thang_9(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 2 Tháng 9/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="03/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 18 tháng 9 năm 2026"
    )
    
    # Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 2",
        "SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 9/2026 (LẦN 2)\nNăm học: 2026 - 2027"
    )
    
    # Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 13 giờ 30 phút, ngày 18 tháng 9 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 2 tháng 9 năm học 2026 - 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt sâu sắc các văn bản chỉ đạo của Sở Giáo dục và Đào tạo thành phố Đồng Nai, các cấp quản lý và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:", indent=True)
    
    # 1. Hướng dẫn 5351
    add_paragraph_styled(doc, "**1. Hướng dẫn một số giải pháp hạn chế việc sử dụng điện thoại di động, thiết bị thông minh, mạng xã hội của học sinh trong trường học (Hướng dẫn số 5351/HD-SGDĐT ngày 15/9/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Căn cứ Thông tư 15/2026/TT-BGDĐT và Công văn 3147/BGDĐT-HSSV của Bộ GD&ĐT. Nhằm giảm thiểu sự phụ thuộc quá mức vào thiết bị công nghệ, tạo không gian học tập tập trung, cải thiện khả năng tư duy độc lập và bảo vệ sức khỏe học đường (thị lực, cột sống, sức khỏe tâm thần) cho học sinh. Học sinh phấn đấu thực hiện bốn tiêu chuẩn “Tự”: *Tự giác* (tắt thiết bị hoặc để chế độ im lặng và cất vào nơi quy định ngay khi bước vào trường/lớp); *Tự quản* (thành lập tổ tự quản nhắc nhở nhau); *Tự rèn* (làm chủ hành vi, không để bị cuốn vào mạng xã hội); *Tự chủ* (sử dụng công nghệ đúng lúc, đúng chỗ phục vụ học tập). Triển khai đồng bộ 03 mô hình vận dụng linh hoạt: (1) Mô hình *“Hộp lưu trữ niềm tin”* (bố trí tủ/khay/túi chuyên dụng tại lớp, học sinh cất thiết bị đầu buổi và nhận lại sau buổi học); (2) Mô hình *“Giờ ra chơi không màn hình”* (tổ chức cờ vua, trò chơi dân gian, góc đọc sách xanh); (3) Mô hình *“Tích hợp giáo dục kỹ năng số”* (hướng dẫn lọc thông tin, bảo mật cá nhân, ứng xử văn minh trên không gian mạng).", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Giáo viên bộ môn Toán và Tin học làm gương, tuyệt đối không sử dụng điện thoại làm việc riêng trong giờ lên lớp. Phân định rõ ràng: Trong giờ học lý thuyết Toán và Tin học, học sinh tuyệt đối không dùng điện thoại; chỉ khi có yêu cầu nghiệp vụ bài dạy rõ ràng (tra cứu phần mềm GeoGebra, làm bài kiểm tra trực tuyến OLM/VioEdu tại phòng máy hoặc theo nhóm có kiểm soát) thì giáo viên mới cho phép mở thiết bị. Giáo viên chủ nhiệm phối hợp chặt chẽ với cha mẹ học sinh để thống nhất quản lý, phòng ngừa bắt nạt mạng và xao nhãng học tập.", indent=True)
    
    # 2. Kế hoạch 5264
    add_paragraph_styled(doc, "**2. Kế hoạch thực hiện nhiệm vụ ứng dụng công nghệ thông tin, chuyển đổi số và thống kê giáo dục năm học 2026 – 2027 (Kế hoạch số 5264/KH-SGDĐT ngày 22/9/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Bám sát Công văn 6020/BGDĐT-KHCNTT của Bộ GD&ĐT, Nghị quyết 57-NQ/TW của Bộ Chính trị, Luật Chuyển đổi số số 148/2025/QH15, Luật Dữ liệu số 60/2024/QH15, Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 và Luật Trí tuệ nhân tạo số 134/2025/QH15. Chỉ đạo xuyên suốt theo tinh thần **“6 rõ”** (*rõ người, rõ việc, rõ thời gian, rõ trách nhiệm, rõ sản phẩm, rõ thẩm quyền*). Dữ liệu giáo dục phải bảo đảm *“đúng, đủ, sạch, sống, thống nhất, dùng chung”*; thực hiện nghiêm nguyên tắc *“dữ liệu cập nhật một lần, sử dụng nhiều lần”*, cắt giảm thủ tục hành chính. Đẩy mạnh phong trào *“Bình dân học vụ số”* và hưởng ứng Ngày Chuyển đổi số Quốc gia (10/10). Định hướng rõ việc thúc đẩy ứng dụng Trí tuệ nhân tạo (AI) an toàn, có kiểm soát và có trách nhiệm: Khuyến khích ứng dụng AI hỗ trợ soạn bài, xây dựng học liệu, thiết kế đề kiểm tra; tuy nhiên *kết quả do AI tạo ra phải được giáo viên kiểm chứng về tính chính xác và phù hợp sư phạm; AI tuyệt đối không thay thế trách nhiệm chuyên môn và quyền ra quyết định của nhà giáo*.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ Toán - Tin là đơn vị nòng cốt triển khai chuyển đổi số trong nhà trường; 100% giáo viên hoàn thành phê duyệt Kế hoạch bài dạy (KHBD) trên hệ thống số CSDL ngành đúng thời hạn; đảm bảo an toàn dữ liệu học bạ số và thông tin cá nhân học sinh; giáo viên Tin học chủ động tham mưu nâng cấp đường truyền và bảo đảm an ninh mạng cho hệ thống phòng máy.", indent=True)
    
    # 3. Công văn 946
    add_paragraph_styled(doc, "**3. Hướng dẫn việc trả và lưu trữ đề, bài kiểm tra, đánh giá định kỳ của học sinh (Công văn số 946/SGDĐT-GDPT&GDTX ngày 06/02/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Hướng dẫn thực hiện thống nhất quy trình trả bài và lưu trữ hồ sơ, ma trận, đặc tả, đề kiểm tra cùng bài kiểm tra, đánh giá định kỳ của học sinh bảo đảm tính chính xác, công bằng, minh bạch và đúng quy định quản lý hồ sơ chuyên môn trong nhà trường.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn thẩm định kỹ lưỡng ma trận và đề kiểm tra định kỳ các khối 6, 7, 8, 9; giáo viên thực hiện nghiêm túc quy trình chấm, trả bài có lời nhận xét cụ thể, vào điểm đúng tiến độ trên hệ thống quản lý điểm số và lưu trữ hồ sơ kiểm tra đầy đủ phục vụ kiểm tra chuyên môn.", indent=True)
    
    # 4. Công văn 4794
    add_paragraph_styled(doc, "**4. Hướng dẫn công tác kiểm tra nội bộ trường học năm học 2026 - 2027 (Công văn số 4794/SGD ngày 09/9/2026 của Sở GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Xác định mục đích, yêu cầu và quy trình tổ chức kiểm tra nhằm nâng cao hiệu quả quản trị, phòng ngừa và chấn chỉnh kịp thời các sai phạm; triển khai 06 cuộc kiểm tra chuyên đề định kỳ cùng các đợt kiểm tra đột xuất đối với toàn thể cán bộ, giáo viên, nhân viên; tập trung quy chế chuyên môn, hoạt động sư phạm, quản lý dạy thêm - học thêm, thu chi tài chính, an toàn trường học và đánh giá xếp loại học sinh.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Giáo viên trong tổ chấp hành nghiêm chỉnh quy định về dạy thêm - học thêm (tuyệt đối không dạy thêm sai quy định); thực hiện đúng kế hoạch kiểm tra nội bộ của trường; Thầy Trần Sáng tham gia tổ kiểm tra nội bộ thực hiện đúng nhiệm vụ được giao.", indent=True)
    
    # 5. Kế hoạch VioEdu
    add_paragraph_styled(doc, "**5. Kế hoạch tổ chức sân chơi “Đấu trường VioEdu” năm học 2026 - 2027 (Kế hoạch số 01/KH-TCM ngày 15/9/2026 của Tổ Toán - Tin học Trường THCS Trần Phú):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi & Quy chế thi:** Mục tiêu thúc đẩy chuyển đổi số, ứng dụng AI và khơi dậy đam mê Toán học, Toán tiếng Anh cho học sinh từ khối 6 đến khối 9 trên tinh thần tự nguyện 100%, hoàn toàn miễn phí. Học sinh thi trực tuyến trên website vio.edu.vn hoặc app VioEdu bằng 01 tài khoản định danh do nhà trường cấp. Mỗi vòng thi gồm 30 câu hỏi (20 câu Toán + 10 câu Toán tiếng Anh), thời gian làm bài cố định 20 phút.", indent=True)
    add_paragraph_styled(doc, "- **Lộ trình thời gian thực hiện:** (1) Ngày 15/9 – 20/9/2026: Khởi tạo và cấp tài khoản đồng loạt; (2) Ngày 28/9 – 13/12/2026: Vòng sơ loại trực tuyến (8 vòng sơ loại và 2 vòng định kỳ, mở từ 00h00 thứ Hai đến 23h59 Chủ nhật hàng tuần); (3) Ngày 11/01 – 15/01/2027: Vòng cấp Trường (thi tập trung tại phòng máy); (4) Ngày 23/02 – 24/02/2027: Vòng cấp Xã; (5) Ngày 30/03 – 31/03/2027: Vòng cấp Tỉnh (dành cho thí sinh đạt từ 20 điểm trở lên và nằm trong Top 30% cấp Xã).", indent=True)
    add_paragraph_styled(doc, "- **Phân công phụ trách khối:** Cô Nguyễn Thị Thảo (Khối 6), Thầy Hoàng Xuân Ánh (Khối 7), Cô Lê Thị Bình (Khối 8), Thầy Trần Sáng (Khối 9), Thầy Dương Quang Tùng (Phụ trách phòng máy và đường truyền mạng). Giáo viên phụ trách khối định kỳ báo cáo kết quả tham gia cho Tổ trưởng chuyên môn vào ngày 25 hàng tháng.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ TÌNH HÌNH CÔNG TÁC THỜI GIAN QUA")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Các giáo viên chủ nhiệm trong tổ đã nhanh chóng ổn định nề nếp lớp chủ nhiệm, tích cực duy trì sinh hoạt 15 phút đầu giờ trước buổi học, hướng dẫn học sinh học tập nội quy, củng cố đội ngũ cán bộ lớp, tham gia họp GVCN và xây dựng kế hoạch chủ nhiệm năm học 2026 - 2027.", indent=True)
    add_paragraph_styled(doc, "- Phát động sôi nổi các phong trào thi đua chào mừng ngày Quốc khánh 2/9, Tháng An toàn giao thông; cho học sinh và cha mẹ học sinh ký cam kết: Không thử, không tàng trữ, không sử dụng và buôn bán các chất ma túy, thuốc lá điện tử và chấp hành nghiêm chỉnh luật giao thông.", indent=True)
    add_paragraph_styled(doc, "- GVCN tăng cường bám sát lớp, theo dõi chuyên cần, quản lý sổ đầu bài cẩn thận, yêu cầu GVBM ghi chép đầy đủ các cột mục và GVCN tổng hợp ký duyệt hàng tuần. Hoàn thành điều tra thông tin học sinh lớp chủ nhiệm trên hệ thống CSDL ngành. Tổ chức họp cha mẹ học sinh đầu năm học vào ngày 13/9/2026 đạt kết quả tốt, thông báo các khoản thu BHYT, BHTN và triển khai đăng ký môn Tiếng Anh tăng cường.", indent=True)
    
    add_section_h2(doc, "2. Ngày giờ công và kỷ luật lao động:")
    add_paragraph_styled(doc, "- 100% giáo viên trong tổ đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ các hoạt động của nhà trường, dạy đủ các tiết theo phân công chuyên môn, thực hiện nghiêm túc việc dạy bù, dạy thay khi có giáo viên đi công tác hoặc nghỉ ốm.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn:")
    add_paragraph_styled(doc, "- Duy trì nền nếp dạy và học ổn định theo thời khóa biểu. Thực hiện chương trình theo kế hoạch nhà trường, thực hiện dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT, thực hiện giáo dục địa phương và hoạt động trải nghiệm hướng nghiệp đúng định hướng. Giáo viên trong tổ khai thác tốt trang thiết bị dạy học và phòng bộ môn.", indent=True)
    add_paragraph_styled(doc, "- Tổ đã phân công phụ trách khối, đóng góp ý kiến xây dựng Kế hoạch giáo dục của tổ và nhà trường. Thực hiện nghiêm túc các quy chế chuyên môn.", indent=True)
    add_paragraph_styled(doc, "- 100% giáo viên trong tổ hoàn thành đợt tập huấn chuyển đổi số ngày 11/9/2026 về CSDL ngành, eNetViet, OLM, phương pháp tích hợp Năng lực số (NLS 20%) và Khung 12 tiết AI vào bài giảng.", indent=True)
    
    add_section_h2(doc, "4. Công tác chuyên đề, thao giảng:")
    add_paragraph_styled(doc, "- Tham gia đầy đủ các buổi tập huấn chuyên đề do các cấp tổ chức và phổ biến lại các nội dung thống nhất để thực hiện. Giáo viên trong tổ đã tiến hành đăng ký chuyên đề nghiên cứu bài học cho năm học.", indent=True)
    
    add_section_h2(doc, "5. Công tác kiểm tra nội bộ:")
    add_paragraph_styled(doc, "- Thường xuyên kiểm tra việc giáo viên thực hiện quy chế chuyên môn, nền nếp ra vào lớp, chất lượng soạn giảng Kế hoạch bài dạy theo đúng khung hướng dẫn.", indent=True)
    
    add_section_h2(doc, "6. Sử dụng đồ dùng dạy học và phòng chức năng:")
    add_paragraph_styled(doc, "- Khai thác có hiệu quả phòng máy tính, phòng học bộ môn. Giáo viên tiếp tục rà soát, đề xuất mua sắm bổ sung thiết bị dạy học, sách tham khảo phục vụ nhu cầu giảng dạy.", indent=True)
    
    add_section_h2(doc, "7. Công tác khác:")
    add_paragraph_styled(doc, "- Phối hợp tốt trong công tác phòng chống các loại tội phạm, phòng chống đuối nước; tham gia tích cực các hoạt động Đoàn – Đội và hoàn thành tốt nhiệm vụ điều tra phổ cập giáo dục theo phân công.", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. KẾ HOẠCH TRỌNG TÂM TRONG THỜI GIAN TỚI")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Tiếp tục ổn định nền nếp lớp chủ nhiệm, tích cực sinh hoạt 15 phút đầu giờ. Phát động đợt thi đua cao điểm chào mừng các ngày lễ lớn trong tháng 10: Ngày Quốc tế Người cao tuổi (01/10), Ngày Khuyến học Việt Nam (02/10), Ngày Bác Hồ gửi bức thư cuối cùng cho ngành Giáo dục (15/10) và Ngày Phụ nữ Việt Nam (20/10). Đẩy mạnh tuyên truyền phòng chống ma túy, ATGT, PCCC và phòng tránh tai nạn thương tích.", indent=True)
    add_paragraph_styled(doc, "- Thực hiện hiệu quả Tuần lễ hưởng ứng học tập suốt đời năm 2026. Hoàn thành hồ sơ sổ sách GVCN đúng quy định; tiếp tục rà soát, thống kê học sinh có hoàn cảnh khó khăn để kịp thời hỗ trợ; đôn đốc thu nộp BHYT, BHTN; thông tin thường xuyên với phụ huynh qua Zalo lớp và sổ liên lạc điện tử.", indent=True)
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm vận động 100% học sinh đăng ký tham gia Đấu trường VioEdu theo kế hoạch; triển khai khai thác thư viện số của trường và đăng ký học Tiếng Anh tăng cường theo chủ trương.", indent=True)
    
    add_section_h2(doc, "2. Đảm bảo ngày giờ công và nền nếp chuyên môn:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ phấn đấu đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ các hoạt động của trường, dạy đúng, dạy đủ các tiết theo phân công; thực hiện nghiêm túc việc dạy bù, dạy thay kịp thời.", indent=True)
    
    add_section_h2(doc, "3. Hoạt động chuyên môn trọng tâm:")
    add_paragraph_styled(doc, "- Thực hiện nghiêm túc việc soạn Kế hoạch bài dạy (KHBD) từ tuần 1 đến tuần 4 và hoàn thành phê duyệt, đẩy lên hệ thống CSDL ngành trong khoảng thời gian từ ngày 20/9 đến ngày 24/9/2026. Lưu ý thể hiện rõ nét nội dung giáo dục học sinh hòa nhập, tích hợp Năng lực số (NLS 20%), ứng dụng AI có kiểm soát và bài học STEM.", indent=True)
    add_paragraph_styled(doc, "- Phân công nhiệm vụ cụ thể hướng dẫn học sinh tham gia các vòng thi VioEdu đạt hiệu quả: Cô Nguyễn Thị Thảo (Khối 6), Thầy Hoàng Xuân Ánh (Khối 7), Cô Lê Thị Bình (Khối 8), Thầy Trần Sáng (Khối 9), Thầy Dương Quang Tùng (Phòng máy & đường truyền).", indent=True)
    add_paragraph_styled(doc, "- Thầy Trần Sáng tiếp tục hoàn thành bài dự thi về Chuyên môn, nghiệp vụ giáo dục phòng, chống ma túy đạt chất lượng cao.", indent=True)
    add_paragraph_styled(doc, "- **Tập trung góp ý chuyên sâu chương trình Sách giáo khoa GDPT 2018 môn Toán - Tin, nhận diện các khó khăn sư phạm và thống nhất hướng khắc phục:**", indent=True)
    add_paragraph_styled(doc, "  + *Đối với sách giáo khoa Toán lớp 8 (Bài 12: Hình thang cân):*", indent=True)
    add_paragraph_styled(doc, "    • Khó khăn thực tế: Học sinh rất dễ ngụy biện và mặc định sai lầm rằng “Hình thang có 2 cạnh bên bằng nhau là hình thang cân” (trong khi nếu 2 cạnh bên bằng nhau và song song thì đó lại là hình bình hành). Việc chứng minh Định lý 3 (Ví dụ 2 trang 54) đòi hỏi kẻ thêm đường phụ khá phức tạp so với trình độ đầu năm lớp 8.", indent=True)
    add_paragraph_styled(doc, "    • Hướng khắc phục: Khai thác triệt để phần “Tranh luận” (trang 59) và “Luyện tập chung” (trang 56) để cho học sinh vẽ cả 2 trường hợp (hai cạnh bên không song song -> hình thang cân; hai cạnh bên song song -> hình bình hành). Chuẩn hóa quy trình kẻ đường song song phụ qua một đỉnh để đưa bài toán về tam giác cân quen thuộc.", indent=True)
    add_paragraph_styled(doc, "  + *Đối với sách giáo khoa Toán lớp 6 (Bài 18 và Bài 19 về các hình phẳng trong thực tiễn):*", indent=True)
    add_paragraph_styled(doc, "    • Khó khăn thực tế: Học sinh gặp khó khăn lớn khi sử dụng compa và êke để vẽ các hình đòi hỏi kỹ thuật cao như hình lục giác đều hay hình thoi. Bên cạnh đó, học sinh rất dễ nhầm lẫn thuộc tính đường chéo giữa các hình (ví dụ: nhầm đường chéo bằng nhau của hình chữ nhật/hình thang cân với đường chéo vuông góc của hình thoi/hình vuông).", indent=True)
    add_paragraph_styled(doc, "    • Hướng khắc phục: Xây dựng Quy trình vẽ hình từng bước: Chuẩn bị phiếu học tập có hình ảnh minh họa rõ ràng các bước đặt thước, quay compa để vẽ hình thoi và hình lục giác đều. Cho học sinh lập Bảng so sánh các yếu tố Cạnh - Góc - Đường chéo của 7 hình phẳng đã học để rèn luyện tư duy phân loại thị giác.", indent=True)
    add_paragraph_styled(doc, "- Hoàn thành toàn bộ hồ sơ tổ chuyên môn theo kế hoạch năm học của nhà trường.", indent=True)
    
    add_section_h2(doc, "4. Công tác chuyên đề và nghiên cứu bài học:")
    add_paragraph_styled(doc, "- Các nhóm bộ môn lên kế hoạch thực hiện chuyên đề theo nghiên cứu bài học. Tổ thống nhất và đăng ký phổ biến chuyên đề cấp trường/tổ: Học kỳ I do Thầy Hoàng Tấn Thiên chủ trì (môn Toán); Học kỳ II do Thầy Hoàng Tấn Thiên và Thầy Trần Sáng phối hợp triển khai (môn Toán). Tham gia đầy đủ các buổi tập huấn chuyên đề do các cấp tổ chức.", indent=True)
    
    add_section_h2(doc, "5. Công tác ngoại khóa và phong trào:")
    add_paragraph_styled(doc, "- Tuyên truyền học sinh chấp hành tốt nội quy trường, lớp, tích cực tham gia các cuộc thi do Nhà trường, Đoàn, Đội tổ chức; duy trì phong trào vệ sinh “Sạch trường, đẹp lớp”.", indent=True)
    
    add_section_h2(doc, "6. Công tác kiểm tra:")
    add_paragraph_styled(doc, "- Kiểm tra nền nếp ra vào lớp, duyệt ma trận và đề kiểm tra định kỳ của tổ; kiểm tra việc soạn giảng, ra đề theo chuẩn KT-KN chương trình GDPT 2018 và kiểm tra việc thực hiện quy chế chuyên môn, sử dụng phòng CNTT.", indent=True)
    
    add_section_h2(doc, "7. Sử dụng đồ dùng dạy học và phòng CNTT:")
    add_paragraph_styled(doc, "- Sử dụng có hiệu quả phòng chức năng, phòng CNTT, khai thác triệt để các phần mềm trong giảng dạy; khuyến khích giáo viên và học sinh ươm mầm các ý tưởng sản phẩm dự thi KHKT.", indent=True)
    
    add_section_h2(doc, "8. Công tác khác:")
    add_paragraph_styled(doc, "- Vệ sinh trường lớp, trang trí lớp Xanh – Sạch – Đẹp; tham gia hoạt động Đoàn – Đội và các hoạt động do nhà trường, công đoàn phát động chào mừng các ngày lễ lớn trong tháng.", indent=True)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. Ý KIẾN THẢO LUẬN VÀ GIẢI PHÁP CHUYÊN MÔN THỰC CHIẾN")
    add_paragraph_styled(doc, "Phiên họp diễn ra thẳng thắn, dân chủ, tập trung sâu sắc vào các vấn đề chuyên môn, phản ánh đúng thực tế lớp học và đề xuất các giải pháp kỹ thuật cụ thể:", indent=True)
    
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (Giáo viên môn Toán 8, Thư ký):** Đánh giá cao tính cấp thiết của Hướng dẫn số 5351/HD-SGDĐT về hạn chế điện thoại trong trường học. Thực tế học sinh lớp 8 rất tò mò và dễ bị phân tâm bởi tin nhắn, mạng xã hội nếu mang điện thoại vào lớp. Đề xuất giải pháp: Mỗi lớp học bố trí 01 khay/túi vải có đánh số thứ tự treo tại góc bảng lớp (Mô hình Hộp lưu trữ niềm tin). Đầu buổi học, ban cán sự lớp đôn đốc học sinh tự giác tắt nguồn hoặc bật chế độ im lặng rồi cất điện thoại vào đúng ô số của mình. Trong giờ học Toán, giáo viên yêu cầu học sinh sử dụng máy tính cầm tay Casio khoa học, tuyệt đối cấm dùng phần mềm giả lập trên điện thoại để tránh việc lén lút chuyển sang ứng dụng mạng xã hội. Giáo viên chủ nhiệm cần thống nhất chặt chẽ với cha mẹ học sinh ngay từ đầu năm.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh (Giáo viên môn Toán 7, Phụ trách VioEdu Khối 7):** Đề nghị Liên đội tăng cường kiểm tra và ghi tên những học sinh không đội nón bảo hiểm khi tham gia giao thông bằng xe đạp điện, xe máy điện ở cổng trường lúc tan học. Về chuyên môn hình học: Đồng tình với giải pháp khắc phục khó khăn vẽ hình lớp 6 và hình thang cân lớp 8. Đối với thao tác vẽ hình phức tạp như lục giác đều, giáo viên nên chiếu video mô phỏng thao tác dựng hình chuẩn bằng phần mềm GeoGebra trước 2 phút, sau đó yêu cầu học sinh thực hành trên phiếu in sẵn lưới ô vuông để định hình tỷ lệ chuẩn trước khi vẽ vào vở.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (Giáo viên Tin học, Phụ trách phòng máy & hạ tầng CNTT):** Báo cáo hạ tầng CNTT: 2 phòng máy tính (45 máy) hiện hoạt động ổn định. Để triển khai tốt Kế hoạch số 5264/KH-SGDĐT và sân chơi VioEdu, Thầy Tùng đề xuất mở cửa phòng máy từ 16h30 đến 17h15 vào các ngày thứ Ba và thứ Năm hàng tuần để tạo điều kiện cho các em học sinh có hoàn cảnh khó khăn (không có máy tính/điện thoại ở nhà) được tham gia thi đấu vòng sơ loại VioEdu miễn phí dưới sự hướng dẫn của giáo viên trực phòng máy. Về việc ứng dụng AI có kiểm soát: Khuyến nghị các thầy cô trong tổ có thể sử dụng các trợ lý AI (như ChatGPT, Claude) để gợi ý các bài toán thực tế, tạo câu hỏi trắc nghiệm khách quan; tuy nhiên phải tuân thủ nghiêm ngặt nguyên tắc kiểm chứng: Giáo viên phải tự tay giải lại, thẩm định lời giải và ma trận đề, tuyệt đối không sao chép nguyên văn sản phẩm của AI đưa vào đề thi hay giáo án.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Hồ Đăng Danh (Giáo viên môn Toán):** Thống nhất bài làm kiểm tra thường xuyên (KTTX) cần thực hiện nhiều hình thức phong phú: vấn đáp, bài viết phiếu học tập, sản phẩm STEM (mô hình tam giác, hình thang cân bằng giấy carton) và đánh giá hoạt động nhóm... nhằm tạo động lực và khích lệ học sinh yếu kém tiến bộ, tránh gây áp lực điểm số đơn thuần bằng bài kiểm tra giấy truyền thống.", indent=True)
    
    add_paragraph_styled(doc, "- **Cô Nguyễn Thị Thảo (Giáo viên môn Toán 6, Phụ trách VioEdu Khối 6):** Phản ánh ý kiến của phụ huynh học sinh về môn Tiếng Anh tăng cường: Cần khảo sát phân loại học sinh theo trình độ để xếp lớp phù hợp, tránh để học sinh trung bình bị quá tải. Đối với 10 câu hỏi Toán tiếng Anh trong mỗi vòng thi VioEdu, Cô Thảo đề xuất giáo viên giảng dạy khối 6 và khối 7 dành 5 phút cuối tiết luyện tập để hướng dẫn học sinh làm quen với các thuật ngữ Toán học tiếng Anh cốt lõi (như *prime number, common divisor, right triangle, angle, perimeter, area*) giúp học sinh tự tin làm bài mà không bị rào cản ngôn ngữ.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Trần Sáng (Giáo viên môn Toán 9, KTNB):** Đề nghị thiết thực về cơ sở vật chất: Nhà trường cần sớm làm khung giá đỡ hoặc hạ thấp ti vi tại các lớp học ở cơ sở 2. Lý do ti vi hiện nay treo quá cao sát trần nhà khiến học sinh ngồi các dãy giữa và cuối phải ngửa cổ liên tục gây mỏi mắt, không quan sát rõ nét chữ và hình vẽ. Về xử lý sai lầm Hình thang cân lớp 8: Thống nhất giáo viên phải đưa ra phản ví dụ cụ thể ngay trên bảng (vẽ một hình thang có 2 cạnh bên bằng nhau và song song để học sinh tự kết luận đó là hình bình hành, từ đó khắc cốt ghi tâm điều kiện 2 cạnh bên phải *không song song* mới là hình thang cân).", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Đinh Văn Đông & Thầy Trần Long Hải:** Đề xuất nhà trường trang cấp bổ sung cho tổ bộ môn 02 bộ compa bảng compozit khổ lớn và thước đo góc có tay cầm chuyên dụng để phục vụ trực quan cho giáo viên dạy hình học các khối 6, 7. Thống nhất mốc thời gian hoàn thành Kế hoạch bài dạy (KHBD) tuần 1 đến tuần 4: 100% giáo viên nộp bài lên hệ thống CSDL ngành trước 17h00 ngày 23/9/2026 để Tổ trưởng chuyên môn kịp thời thẩm định và phê duyệt trước hạn chót 24/9/2026.", indent=True)
    
    # ==================== PHẦN V ====================
    add_section_h1(doc, "V. KẾT LUẬN CỦA CHỦ TỌA VÀ NGHỊ QUYẾT CUỘC HỌP")
    add_paragraph_styled(doc, "Thầy Tổ trưởng chuyên môn Hoàng Tấn Thiên kết luận toàn diện phiên họp và chỉ đạo thực hiện các nhiệm vụ trọng tâm sau:", indent=True)
    add_paragraph_styled(doc, "1. Toàn thể giáo viên quán triệt và thực hiện nghiêm túc Hướng dẫn số 5351/HD-SGDĐT: Triển khai hiệu quả Mô hình “Hộp lưu trữ niềm tin” tại lớp chủ nhiệm và phòng bộ môn; tuyệt đối không để học sinh lạm dụng điện thoại trong giờ học; giáo viên làm gương không sử dụng thiết bị cá nhân làm việc riêng trong tiết giảng.", indent=True)
    add_paragraph_styled(doc, "2. Bám sát tinh thần Kế hoạch số 5264/KH-SGDĐT: Thực hiện nghiêm túc nguyên tắc “6 rõ”, chuẩn hóa dữ liệu CSDL ngành theo phương châm “đúng, đủ, sạch, sống”; hoàn thành việc phê duyệt và nộp KHBD tuần 1 đến tuần 4 lên CSDL ngành đúng thời hạn (hạn chót hoàn thành của giáo viên là ngày 23/9/2026); ứng dụng AI một cách thông minh, có trách nhiệm và luôn kiểm chứng tính chính xác chuyên môn.", indent=True)
    add_paragraph_styled(doc, "3. Triển khai sâu rộng và đồng bộ sân chơi Đấu trường VioEdu theo Kế hoạch 01/KH-TCM; giáo viên phụ trách khối chủ động cấp tài khoản, đôn đốc học sinh tham gia vòng sơ loại từ ngày 28/9/2026; Thầy Dương Quang Tùng quản lý tốt phòng máy mở cửa ngoài giờ hỗ trợ học sinh có hoàn cảnh khó khăn.", indent=True)
    add_paragraph_styled(doc, "4. Áp dụng đồng bộ giải pháp tháo gỡ điểm nghẽn SGK Toán 6 và Toán 8 đã được tổ thống nhất (phiếu hướng dẫn vẽ hình từng bước, bảng so sánh 7 hình phẳng, khai thác phản ví dụ tránh ngụy biện hình thang cân).", indent=True)
    add_paragraph_styled(doc, "5. Tổ trưởng chuyên môn tổng hợp các kiến nghị chính đáng của tổ (hạ thấp tivi cơ sở 2, mua sắm compa bảng, rà soát phân lớp tiếng Anh tăng cường) để trực tiếp đề xuất với Ban Giám hiệu nhà trường trong cuộc họp giao ban đầu tuần tới.", indent=True)
    
    add_paragraph_styled(doc, "**Biểu quyết:** 10/10 thành viên trong tổ (100%) giáo viên nhất trí hoàn toàn với nội dung cuộc họp.", indent=True)
    add_paragraph_styled(doc, "Biên bản được thông qua trước tập thể và kết thúc vào lúc 16 giờ 00 phút cùng ngày./.", indent=True)
    
    # Chữ ký 2 bên
    add_signatures(
        doc,
        left_title="THƯ KÝ CUỘC HỌP",
        left_name="Lê Thị Bình",
        right_title="TỔ TRƯỞNG CHUYÊN MÔN",
        right_name="Hoàng Tấn Thiên"
    )
    
    # Bảng ký xác nhận của các thành viên khác
    p_mem_head = doc.add_paragraph()
    p_mem_head.paragraph_format.space_before = Pt(12)
    p_mem_head.paragraph_format.space_after = Pt(4)
    r_mh = p_mem_head.add_run("CÁC THÀNH VIÊN TRONG TỔ KÝ TÊN XÁC NHẬN")
    r_mh.font.name = 'Times New Roman'
    r_mh.font.size = Pt(13)
    r_mh.bold = True
    p_mem_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    tbl_ack = doc.add_table(rows=3, cols=4)
    tbl_ack.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_borders_closed(tbl_ack)
    
    ack_names = [
        ["Đinh Văn Đông", "Hồ Đăng Danh", "Hoàng Xuân Ánh", "Trần Long Hải"],
        ["Nguyễn Văn Tính", "Dương Quang Tùng", "Trần Sáng", "Nguyễn Thị Thảo"]
    ]
    
    # Hàng 1
    for c_idx in range(4):
        cell = tbl_ack.cell(0, c_idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"**{ack_names[0][c_idx]}**\n\n*(Ký tên)*")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    # Hàng 2
    for c_idx in range(4):
        cell = tbl_ack.cell(1, c_idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"**{ack_names[1][c_idx]}**\n\n*(Ký tên)*")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    save_docx_robust(doc, out_docx_path)
    
    if out_md_path:
        tao_bien_ban_hop_to_lan_2_thang_9_md(out_md_path)


def tao_bien_ban_hop_to_lan_2_thang_9_md(out_md_path):
    md_content = """# BIÊN BẢN SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 9/2026 (LẦN 2)
**Trường THCS Trần Phú – Tổ Toán - Tin**  
**Số: 03/BB-TCM**  
*Xuân Đông, ngày 18 tháng 9 năm 2026*

---

Hôm nay, vào lúc 13 giờ 30 phút, ngày 18 tháng 9 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 2 tháng 9 năm học 2026 - 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).
  + *Danh sách thành viên:* Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

### NỘI DUNG CUỘC HỌP

## I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN

Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt sâu sắc các văn bản chỉ đạo của Sở Giáo dục và Đào tạo thành phố Đồng Nai, các cấp quản lý và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:

**1. Hướng dẫn một số giải pháp hạn chế việc sử dụng điện thoại di động, thiết bị thông minh, mạng xã hội của học sinh trong trường học (Hướng dẫn số 5351/HD-SGDĐT ngày 15/9/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Căn cứ Thông tư 15/2026/TT-BGDĐT và Công văn 3147/BGDĐT-HSSV của Bộ GD&ĐT. Nhằm giảm thiểu sự phụ thuộc quá mức vào thiết bị công nghệ, tạo không gian học tập tập trung, cải thiện khả năng tư duy độc lập và bảo vệ sức khỏe học đường (thị lực, cột sống, sức khỏe tâm thần) cho học sinh. Học sinh phấn đấu thực hiện bốn tiêu chuẩn “Tự”: *Tự giác* (tắt thiết bị hoặc để chế độ im lặng và cất vào nơi quy định ngay khi bước vào trường/lớp); *Tự quản* (thành lập tổ tự quản nhắc nhở nhau); *Tự rèn* (làm chủ hành vi, không để bị cuốn vào mạng xã hội); *Tự chủ* (sử dụng công nghệ đúng lúc, đúng chỗ phục vụ học tập). Triển khai đồng bộ 03 mô hình vận dụng linh hoạt: (1) Mô hình *“Hộp lưu trữ niềm tin”* (bố trí tủ/khay/túi chuyên dụng tại lớp, học sinh cất thiết bị đầu buổi và nhận lại sau buổi học); (2) Mô hình *“Giờ ra chơi không màn hình”* (tổ chức cờ vua, trò chơi dân gian, góc đọc sách xanh); (3) Mô hình *“Tích hợp giáo dục kỹ năng số”* (hướng dẫn lọc thông tin, bảo mật cá nhân, ứng xử văn minh trên không gian mạng).
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Giáo viên bộ môn Toán và Tin học làm gương, tuyệt đối không sử dụng điện thoại làm việc riêng trong giờ lên lớp. Phân định rõ ràng: Trong giờ học lý thuyết Toán và Tin học, học sinh tuyệt đối không dùng điện thoại; chỉ khi có yêu cầu nghiệp vụ bài dạy rõ ràng (tra cứu phần mềm GeoGebra, làm bài kiểm tra trực tuyến OLM/VioEdu tại phòng máy hoặc theo nhóm có kiểm soát) thì giáo viên mới cho phép mở thiết bị. Giáo viên chủ nhiệm phối hợp chặt chẽ với cha mẹ học sinh để thống nhất quản lý, phòng ngừa bắt nạt mạng và xao nhãng học tập.

**2. Kế hoạch thực hiện nhiệm vụ ứng dụng công nghệ thông tin, chuyển đổi số và thống kê giáo dục năm học 2026 – 2027 (Kế hoạch số 5264/KH-SGDĐT ngày 22/9/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Bám sát Công văn 6020/BGDĐT-KHCNTT của Bộ GD&ĐT, Nghị quyết 57-NQ/TW của Bộ Chính trị, Luật Chuyển đổi số số 148/2025/QH15, Luật Dữ liệu số 60/2024/QH15, Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 và Luật Trí tuệ nhân tạo số 134/2025/QH15. Chỉ đạo xuyên suốt theo tinh thần **“6 rõ”** (*rõ người, rõ việc, rõ thời gian, rõ trách nhiệm, rõ sản phẩm, rõ thẩm quyền*). Dữ liệu giáo dục phải bảo đảm *“đúng, đủ, sạch, sống, thống nhất, dùng chung”*; thực hiện nghiêm nguyên tắc *“dữ liệu cập nhật một lần, sử dụng nhiều lần”*, cắt giảm thủ tục hành chính. Đẩy mạnh phong trào *“Bình dân học vụ số”* và hưởng ứng Ngày Chuyển đổi số Quốc gia (10/10). Định hướng rõ việc thúc đẩy ứng dụng Trí tuệ nhân tạo (AI) an toàn, có kiểm soát và có trách nhiệm: Khuyến khích ứng dụng AI hỗ trợ soạn bài, xây dựng học liệu, thiết kế đề kiểm tra; tuy nhiên *kết quả do AI tạo ra phải được giáo viên kiểm chứng về tính chính xác và phù hợp sư phạm; AI tuyệt đối không thay thế trách nhiệm chuyên môn và quyền ra quyết định của nhà giáo*.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ Toán - Tin là đơn vị nòng cốt triển khai chuyển đổi số trong nhà trường; 100% giáo viên hoàn thành phê duyệt Kế hoạch bài dạy (KHBD) trên hệ thống số CSDL ngành đúng thời hạn; đảm bảo an toàn dữ liệu học bạ số và thông tin cá nhân học sinh; giáo viên Tin học chủ động tham mưu nâng cấp đường truyền và bảo đảm an ninh mạng cho hệ thống phòng máy.

**3. Hướng dẫn việc trả và lưu trữ đề, bài kiểm tra, đánh giá định kỳ của học sinh (Công văn số 946/SGDĐT-GDPT&GDTX ngày 06/02/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Hướng dẫn thực hiện thống nhất quy trình trả bài và lưu trữ hồ sơ, ma trận, đặc tả, đề kiểm tra cùng bài kiểm tra, đánh giá định kỳ của học sinh bảo đảm tính chính xác, công bằng, minh bạch và đúng quy định quản lý hồ sơ chuyên môn trong nhà trường.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn thẩm định kỹ lưỡng ma trận và đề kiểm tra định kỳ các khối 6, 7, 8, 9; giáo viên thực hiện nghiêm túc quy trình chấm, trả bài có lời nhận xét cụ thể, vào điểm đúng tiến độ trên hệ thống quản lý điểm số và lưu trữ hồ sơ kiểm tra đầy đủ phục vụ kiểm tra chuyên môn.

**4. Hướng dẫn công tác kiểm tra nội bộ trường học năm học 2026 - 2027 (Công văn số 4794/SGD ngày 09/9/2026 của Sở GD&ĐT):**
- **Ý chính cốt lõi:** Xác định mục đích, yêu cầu và quy trình tổ chức kiểm tra nhằm nâng cao hiệu quả quản trị, phòng ngừa và chấn chỉnh kịp thời các sai phạm; triển khai 06 cuộc kiểm tra chuyên đề định kỳ cùng các đợt kiểm tra đột xuất đối với toàn thể cán bộ, giáo viên, nhân viên; tập trung quy chế chuyên môn, hoạt động sư phạm, quản lý dạy thêm - học thêm, thu chi tài chính, an toàn trường học và đánh giá xếp loại học sinh.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Giáo viên trong tổ chấp hành nghiêm chỉnh quy định về dạy thêm - học thêm (tuyệt đối không dạy thêm sai quy định); thực hiện đúng kế hoạch kiểm tra nội bộ của trường; Thầy Trần Sáng tham gia tổ kiểm tra nội bộ thực hiện đúng nhiệm vụ được giao.

**5. Kế hoạch tổ chức sân chơi “Đấu trường VioEdu” năm học 2026 - 2027 (Kế hoạch số 01/KH-TCM ngày 15/9/2026 của Tổ Toán - Tin học Trường THCS Trần Phú):**
- **Ý chính cốt lõi & Quy chế thi:** Mục tiêu thúc đẩy chuyển đổi số, ứng dụng AI và khơi dậy đam mê Toán học, Toán tiếng Anh cho học sinh từ khối 6 đến khối 9 trên tinh thần tự nguyện 100%, hoàn toàn miễn phí. Học sinh thi trực tuyến trên website vio.edu.vn hoặc app VioEdu bằng 01 tài khoản định danh do nhà trường cấp. Mỗi vòng thi gồm 30 câu hỏi (20 câu Toán + 10 câu Toán tiếng Anh), thời gian làm bài cố định 20 phút.
- **Lộ trình thời gian thực hiện:** (1) Ngày 15/9 – 20/9/2026: Khởi tạo và cấp tài khoản đồng loạt; (2) Ngày 28/9 – 13/12/2026: Vòng sơ loại trực tuyến (8 vòng sơ loại và 2 vòng định kỳ, mở từ 00h00 thứ Hai đến 23h59 Chủ nhật hàng tuần); (3) Ngày 11/01 – 15/01/2027: Vòng cấp Trường (thi tập trung tại phòng máy); (4) Ngày 23/02 – 24/02/2027: Vòng cấp Xã; (5) Ngày 30/03 – 31/03/2027: Vòng cấp Tỉnh (dành cho thí sinh đạt từ 20 điểm trở lên và nằm trong Top 30% cấp Xã).
- **Phân công phụ trách khối:** Cô Nguyễn Thị Thảo (Khối 6), Thầy Hoàng Xuân Ánh (Khối 7), Cô Lê Thị Bình (Khối 8), Thầy Trần Sáng (Khối 9), Thầy Dương Quang Tùng (Phụ trách phòng máy và đường truyền mạng). Giáo viên phụ trách khối định kỳ báo cáo kết quả tham gia cho Tổ trưởng chuyên môn vào ngày 25 hàng tháng.

## II. ĐÁNH GIÁ TÌNH HÌNH CÔNG TÁC THỜI GIAN QUA

### **1. Công tác chủ nhiệm:**
- Các giáo viên chủ nhiệm trong tổ đã nhanh chóng ổn định nề nếp lớp chủ nhiệm, tích cực duy trì sinh hoạt 15 phút đầu giờ trước buổi học, hướng dẫn học sinh học tập nội quy, củng cố đội ngũ cán bộ lớp, tham gia họp GVCN và xây dựng kế hoạch chủ nhiệm năm học 2026 - 2027.
- Phát động sôi nổi các phong trào thi đua chào mừng ngày Quốc khánh 2/9, Tháng An toàn giao thông; cho học sinh và cha mẹ học sinh ký cam kết: Không thử, không tàng trữ, không sử dụng và buôn bán các chất ma túy, thuốc lá điện tử và chấp hành nghiêm chỉnh luật giao thông.
- GVCN tăng cường bám sát lớp, theo dõi chuyên cần, quản lý sổ đầu bài cẩn thận, yêu cầu GVBM ghi chép đầy đủ các cột mục và GVCN tổng hợp ký duyệt hàng tuần. Hoàn thành điều tra thông tin học sinh lớp chủ nhiệm trên hệ thống CSDL ngành. Tổ chức họp cha mẹ học sinh đầu năm học vào ngày 13/9/2026 đạt kết quả tốt, thông báo các khoản thu BHYT, BHTN và triển khai đăng ký môn Tiếng Anh tăng cường.

### **2. Ngày giờ công và kỷ luật lao động:**
- 100% giáo viên trong tổ đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ các hoạt động của nhà trường, dạy đủ các tiết theo phân công chuyên môn, thực hiện nghiêm túc việc dạy bù, dạy thay khi có giáo viên đi công tác hoặc nghỉ ốm.

### **3. Công tác chuyên môn:**
- Duy trì nền nếp dạy và học ổn định theo thời khóa biểu. Thực hiện chương trình theo kế hoạch nhà trường, thực hiện dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT, thực hiện giáo dục địa phương và hoạt động trải nghiệm hướng nghiệp đúng định hướng. Giáo viên trong tổ khai thác tốt trang thiết bị dạy học và phòng bộ môn.
- Tổ đã phân công phụ trách khối, đóng góp ý kiến xây dựng Kế hoạch giáo dục của tổ và nhà trường. Thực hiện nghiêm túc các quy chế chuyên môn.
- 100% giáo viên trong tổ hoàn thành đợt tập huấn chuyển đổi số ngày 11/9/2026 về CSDL ngành, eNetViet, OLM, phương pháp tích hợp Năng lực số (NLS 20%) và Khung 12 tiết AI vào bài giảng.

### **4. Công tác chuyên đề, thao giảng:**
- Tham gia đầy đủ các buổi tập huấn chuyên đề do các cấp tổ chức và phổ biến lại các nội dung thống nhất để thực hiện. Giáo viên trong tổ đã tiến hành đăng ký chuyên đề nghiên cứu bài học cho năm học.

### **5. Công tác kiểm tra nội bộ:**
- Thường xuyên kiểm tra việc giáo viên thực hiện quy chế chuyên môn, nền nếp ra vào lớp, chất lượng soạn giảng Kế hoạch bài dạy theo đúng khung hướng dẫn.

### **6. Sử dụng đồ dùng dạy học và phòng chức năng:**
- Khai thác có hiệu quả phòng máy tính, phòng học bộ môn. Giáo viên tiếp tục rà soát, đề xuất mua sắm bổ sung thiết bị dạy học, sách tham khảo phục vụ nhu cầu giảng dạy.

### **7. Công tác khác:**
- Phối hợp tốt trong công tác phòng chống các loại tội phạm, phòng chống đuối nước; tham gia tích cực các hoạt động Đoàn – Đội và hoàn thành tốt nhiệm vụ điều tra phổ cập giáo dục theo phân công.

## III. KẾ HOẠCH TRỌNG TÂM TRONG THỜI GIAN TỚI

### **1. Công tác chủ nhiệm:**
- Tiếp tục ổn định nền nếp lớp chủ nhiệm, tích cực sinh hoạt 15 phút đầu giờ. Phát động đợt thi đua cao điểm chào mừng các ngày lễ lớn trong tháng 10: Ngày Quốc tế Người cao tuổi (01/10), Ngày Khuyến học Việt Nam (02/10), Ngày Bác Hồ gửi bức thư cuối cùng cho ngành Giáo dục (15/10) và Ngày Phụ nữ Việt Nam (20/10). Đẩy mạnh tuyên truyền phòng chống ma túy, ATGT, PCCC và phòng tránh tai nạn thương tích.
- Thực hiện hiệu quả Tuần lễ hưởng ứng học tập suốt đời năm 2026. Hoàn thành hồ sơ sổ sách GVCN đúng quy định; tiếp tục rà soát, thống kê học sinh có hoàn cảnh khó khăn để kịp thời hỗ trợ; đôn đốc thu nộp BHYT, BHTN; thông tin thường xuyên với phụ huynh qua Zalo lớp và sổ liên lạc điện tử.
- Giáo viên chủ nhiệm vận động 100% học sinh đăng ký tham gia Đấu trường VioEdu theo kế hoạch; triển khai khai thác thư viện số của trường và đăng ký học Tiếng Anh tăng cường theo chủ trương.

### **2. Đảm bảo ngày giờ công và nền nếp chuyên môn:**
- Giáo viên trong tổ phấn đấu đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ các hoạt động của trường, dạy đúng, dạy đủ các tiết theo phân công; thực hiện nghiêm túc việc dạy bù, dạy thay kịp thời.

### **3. Hoạt động chuyên môn trọng tâm:**
- Thực hiện nghiêm túc việc soạn Kế hoạch bài dạy (KHBD) từ tuần 1 đến tuần 4 và hoàn thành phê duyệt, đẩy lên hệ thống CSDL ngành trong khoảng thời gian từ ngày 20/9 đến ngày 24/9/2026. Lưu ý thể hiện rõ nét nội dung giáo dục học sinh hòa nhập, tích hợp Năng lực số (NLS 20%), ứng dụng AI có kiểm soát và bài học STEM.
- Phân công nhiệm vụ cụ thể hướng dẫn học sinh tham gia các vòng thi VioEdu đạt hiệu quả: Cô Nguyễn Thị Thảo (Khối 6), Thầy Hoàng Xuân Ánh (Khối 7), Cô Lê Thị Bình (Khối 8), Thầy Trần Sáng (Khối 9), Thầy Dương Quang Tùng (Phòng máy & đường truyền).
- Thầy Trần Sáng tiếp tục hoàn thành bài dự thi về Chuyên môn, nghiệp vụ giáo dục phòng, chống ma túy đạt chất lượng cao.
- **Tập trung góp ý chuyên sâu chương trình Sách giáo khoa GDPT 2018 môn Toán - Tin, nhận diện các khó khăn sư phạm và thống nhất hướng khắc phục:**
  - *Đối với sách giáo khoa Toán lớp 8 (Bài 12: Hình thang cân):*
    - **Khó khăn thực tế:** Học sinh rất dễ ngụy biện và mặc định sai lầm rằng “Hình thang có 2 cạnh bên bằng nhau là hình thang cân” (trong khi nếu 2 cạnh bên bằng nhau và song song thì đó lại là hình bình hành). Việc chứng minh Định lý 3 (Ví dụ 2 trang 54) đòi hỏi kẻ thêm đường phụ khá phức tạp so với trình độ đầu năm lớp 8.
    - **Hướng khắc phục:** Khai thác triệt để phần “Tranh luận” (trang 59) và “Luyện tập chung” (trang 56) để cho học sinh vẽ cả 2 trường hợp (hai cạnh bên không song song -> hình thang cân; hai cạnh bên song song -> hình bình hành). Chuẩn hóa quy trình kẻ đường song song phụ qua một đỉnh để đưa bài toán về tam giác cân quen thuộc.
  - *Đối với sách giáo khoa Toán lớp 6 (Bài 18 và Bài 19 về các hình phẳng trong thực tiễn):*
    - **Khó khăn thực tế:** Học sinh gặp khó khăn lớn khi sử dụng compa và êke để vẽ các hình đòi hỏi kỹ thuật cao như hình lục giác đều hay hình thoi. Bên cạnh đó, học sinh rất dễ nhầm lẫn thuộc tính đường chéo giữa các hình (ví dụ: nhầm đường chéo bằng nhau của hình chữ nhật/hình thang cân với đường chéo vuông góc của hình thoi/hình vuông).
    - **Hướng khắc phục:** Xây dựng Quy trình vẽ hình từng bước: Chuẩn bị phiếu học tập có hình ảnh minh họa rõ ràng các bước đặt thước, quay compa để vẽ hình thoi và hình lục giác đều. Cho học sinh lập Bảng so sánh các yếu tố Cạnh - Góc - Đường chéo của 7 hình phẳng đã học để rèn luyện tư duy phân loại thị giác.
- Hoàn thành toàn bộ hồ sơ tổ chuyên môn theo kế hoạch năm học của nhà trường.

### **4. Công tác chuyên đề và nghiên cứu bài học:**
- Các nhóm bộ môn lên kế hoạch thực hiện chuyên đề theo nghiên cứu bài học. Tổ thống nhất và đăng ký phổ biến chuyên đề cấp trường/tổ: Học kỳ I do Thầy Hoàng Tấn Thiên chủ trì (môn Toán); Học kỳ II do Thầy Hoàng Tấn Thiên và Thầy Trần Sáng phối hợp triển khai (môn Toán). Tham gia đầy đủ các buổi tập huấn chuyên đề do các cấp tổ chức.

### **5. Công tác ngoại khóa và phong trào:**
- Tuyên truyền học sinh chấp hành tốt nội quy trường, lớp, tích cực tham gia các cuộc thi do Nhà trường, Đoàn, Đội tổ chức; duy trì phong trào vệ sinh “Sạch trường, đẹp lớp”.

### **6. Công tác kiểm tra:**
- Kiểm tra nền nếp ra vào lớp, duyệt ma trận và đề kiểm tra định kỳ của tổ; kiểm tra việc soạn giảng, ra đề theo chuẩn KT-KN chương trình GDPT 2018 và kiểm tra việc thực hiện quy chế chuyên môn, sử dụng phòng CNTT.

### **7. Sử dụng đồ dùng dạy học và phòng CNTT:**
- Sử dụng có hiệu quả phòng chức năng, phòng CNTT, khai thác triệt để các phần mềm trong giảng dạy; khuyến khích giáo viên và học sinh ươm mầm các ý tưởng sản phẩm dự thi KHKT.

### **8. Công tác khác:**
- Vệ sinh trường lớp, trang trí lớp Xanh – Sạch – Đẹp; tham gia hoạt động Đoàn – Đội và các hoạt động do nhà trường, công đoàn phát động chào mừng các ngày lễ lớn trong tháng.

## IV. Ý KIẾN THẢO LUẬN VÀ GIẢI PHÁP CHUYÊN MÔN THỰC CHIẾN

Phiên họp diễn ra thẳng thắn, dân chủ, tập trung sâu sắc vào các vấn đề chuyên môn, phản ánh đúng thực tế lớp học và đề xuất các giải pháp kỹ thuật cụ thể:

- **Cô Lê Thị Bình (Giáo viên môn Toán 8, Thư ký):** Đánh giá cao tính cấp thiết của Hướng dẫn số 5351/HD-SGDĐT về hạn chế điện thoại trong trường học. Thực tế học sinh lớp 8 rất tò mò và dễ bị phân tâm bởi tin nhắn, mạng xã hội nếu mang điện thoại vào lớp. Đề xuất giải pháp: Mỗi lớp học bố trí 01 khay/túi vải có đánh số thứ tự treo tại góc bảng lớp (Mô hình Hộp lưu trữ niềm tin). Đầu buổi học, ban cán sự lớp đôn đốc học sinh tự giác tắt nguồn hoặc bật chế độ im lặng rồi cất điện thoại vào đúng ô số của mình. Trong giờ học Toán, giáo viên yêu cầu học sinh sử dụng máy tính cầm tay Casio khoa học, tuyệt đối cấm dùng phần mềm giả lập trên điện thoại để tránh việc lén lút chuyển sang ứng dụng mạng xã hội. Giáo viên chủ nhiệm cần thống nhất chặt chẽ với cha mẹ học sinh ngay từ đầu năm.

- **Thầy Hoàng Xuân Ánh (Giáo viên môn Toán 7, Phụ trách VioEdu Khối 7):** Đề nghị Liên đội tăng cường kiểm tra và ghi tên những học sinh không đội nón bảo hiểm khi tham gia giao thông bằng xe đạp điện, xe máy điện ở cổng trường lúc tan học. Về chuyên môn hình học: Đồng tình với giải pháp khắc phục khó khăn vẽ hình lớp 6 và hình thang cân lớp 8. Đối với thao tác vẽ hình phức tạp như lục giác đều, giáo viên nên chiếu video mô phỏng thao tác dựng hình chuẩn bằng phần mềm GeoGebra trước 2 phút, sau đó yêu cầu học sinh thực hành trên phiếu in sẵn lưới ô vuông để định hình tỷ lệ chuẩn trước khi vẽ vào vở.

- **Thầy Dương Quang Tùng (Giáo viên Tin học, Phụ trách phòng máy & hạ tầng CNTT):** Báo cáo hạ tầng CNTT: 2 phòng máy tính (45 máy) hiện hoạt động ổn định. Để triển khai tốt Kế hoạch số 5264/KH-SGDĐT và sân chơi VioEdu, Thầy Tùng đề xuất mở cửa phòng máy từ 16h30 đến 17h15 vào các ngày thứ Ba và thứ Năm hàng tuần để tạo điều kiện cho các em học sinh có hoàn cảnh khó khăn (không có máy tính/điện thoại ở nhà) được tham gia thi đấu vòng sơ loại VioEdu miễn phí dưới sự hướng dẫn của giáo viên trực phòng máy. Về việc ứng dụng AI có kiểm soát: Khuyến nghị các thầy cô trong tổ có thể sử dụng các trợ lý AI (như ChatGPT, Claude) để gợi ý các bài toán thực tế, tạo câu hỏi trắc nghiệm khách quan; tuy nhiên phải tuân thủ nghiêm ngặt nguyên tắc kiểm chứng: Giáo viên phải tự tay giải lại, thẩm định lời giải và ma trận đề, tuyệt đối không sao chép nguyên văn sản phẩm của AI đưa vào đề thi hay giáo án.

- **Thầy Hồ Đăng Danh (Giáo viên môn Toán):** Thống nhất bài làm kiểm tra thường xuyên (KTTX) cần thực hiện nhiều hình thức phong phú: vấn đáp, bài viết phiếu học tập, sản phẩm STEM (mô hình tam giác, hình thang cân bằng giấy carton) và đánh giá hoạt động nhóm... nhằm tạo động lực và khích lệ học sinh yếu kém tiến bộ, tránh gây áp lực điểm số đơn thuần bằng bài kiểm tra giấy truyền thống.

- **Cô Nguyễn Thị Thảo (Giáo viên môn Toán 6, Phụ trách VioEdu Khối 6):** Phản ánh ý kiến của phụ huynh học sinh về môn Tiếng Anh tăng cường: Cần khảo sát phân loại học sinh theo trình độ để xếp lớp phù hợp, tránh để học sinh trung bình bị quá tải. Đối với 10 câu hỏi Toán tiếng Anh trong mỗi vòng thi VioEdu, Cô Thảo đề xuất giáo viên giảng dạy khối 6 và khối 7 dành 5 phút cuối tiết luyện tập để hướng dẫn học sinh làm quen với các thuật ngữ Toán học tiếng Anh cốt lõi (như *prime number, common divisor, right triangle, angle, perimeter, area*) giúp học sinh tự tin làm bài mà không bị rào cản ngôn ngữ.

- **Thầy Trần Sáng (Giáo viên môn Toán 9, KTNB):** Đề nghị thiết thực về cơ sở vật chất: Nhà trường cần sớm làm khung giá đỡ hoặc hạ thấp ti vi tại các lớp học ở cơ sở 2. Lý do ti vi hiện nay treo quá cao sát trần nhà khiến học sinh ngồi các dãy giữa và cuối phải ngửa cổ liên tục gây mỏi mắt, không quan sát rõ nét chữ và hình vẽ. Về xử lý sai lầm Hình thang cân lớp 8: Thống nhất giáo viên phải đưa ra phản ví dụ cụ thể ngay trên bảng (vẽ một hình thang có 2 cạnh bên bằng nhau và song song để học sinh tự kết luận đó là hình bình hành, từ đó khắc cốt ghi tâm điều kiện 2 cạnh bên phải *không song song* mới là hình thang cân).

- **Thầy Đinh Văn Đông & Thầy Trần Long Hải:** Đề xuất nhà trường trang cấp bổ sung cho tổ bộ môn 02 bộ compa bảng compozit khổ lớn và thước đo góc có tay cầm chuyên dụng để phục vụ trực quan cho giáo viên dạy hình học các khối 6, 7. Thống nhất mốc thời gian hoàn thành Kế hoạch bài dạy (KHBD) tuần 1 đến tuần 4: 100% giáo viên nộp bài lên hệ thống CSDL ngành trước 17h00 ngày 23/9/2026 để Tổ trưởng chuyên môn kịp thời thẩm định và phê duyệt trước hạn chót 24/9/2026.

## V. KẾT LUẬN CỦA CHỦ TỌA VÀ NGHỊ QUYẾT CUỘC HỌP

Thầy Tổ trưởng chuyên môn Hoàng Tấn Thiên kết luận toàn diện phiên họp và chỉ đạo thực hiện các nhiệm vụ trọng tâm sau:

1. Toàn thể giáo viên quán triệt và thực hiện nghiêm túc Hướng dẫn số 5351/HD-SGDĐT: Triển khai hiệu quả Mô hình “Hộp lưu trữ niềm tin” tại lớp chủ nhiệm và phòng bộ môn; tuyệt đối không để học sinh lạm dụng điện thoại trong giờ học; giáo viên làm gương không sử dụng thiết bị cá nhân làm việc riêng trong tiết giảng.
2. Bám sát tinh thần Kế hoạch số 5264/KH-SGDĐT: Thực hiện nghiêm túc nguyên tắc “6 rõ”, chuẩn hóa dữ liệu CSDL ngành theo phương châm “đúng, đủ, sạch, sống”; hoàn thành việc phê duyệt và nộp KHBD tuần 1 đến tuần 4 lên CSDL ngành đúng thời hạn (hạn chót hoàn thành của giáo viên là ngày 23/9/2026); ứng dụng AI một cách thông minh, có trách nhiệm và luôn kiểm chứng tính chính xác chuyên môn.
3. Triển khai sâu rộng và đồng bộ sân chơi Đấu trường VioEdu theo Kế hoạch 01/KH-TCM; giáo viên phụ trách khối chủ động cấp tài khoản, đôn đốc học sinh tham gia vòng sơ loại từ ngày 28/9/2026; Thầy Dương Quang Tùng quản lý tốt phòng máy mở cửa ngoài giờ hỗ trợ học sinh có hoàn cảnh khó khăn.
4. Áp dụng đồng bộ giải pháp tháo gỡ điểm nghẽn SGK Toán 6 và Toán 8 đã được tổ thống nhất (phiếu hướng dẫn vẽ hình từng bước, bảng so sánh 7 hình phẳng, khai thác phản ví dụ tránh ngụy biện hình thang cân).
5. Tổ trưởng chuyên môn tổng hợp các kiến nghị chính đáng của tổ (hạ thấp tivi cơ sở 2, mua sắm compa bảng, rà soát phân lớp tiếng Anh tăng cường) để trực tiếp đề xuất với Ban Giám hiệu nhà trường trong cuộc họp giao ban đầu tuần tới.

- **Biểu quyết:** 10/10 thành viên trong tổ (100%) giáo viên nhất trí hoàn toàn với nội dung cuộc họp.
- Biên bản được thông qua trước tập thể và kết thúc vào lúc 16 giờ 00 phút cùng ngày./.

---

<table style="width: 100%; border: none;">
<tr>
<td style="width: 50%; text-align: center; vertical-align: top;">
<strong>THƯ KÝ CUỘC HỌP</strong><br>
<em>(Ký và ghi rõ họ tên)</em><br><br><br><br>
<strong>Lê Thị Bình</strong>
</td>
<td style="width: 50%; text-align: center; vertical-align: top;">
<strong>TỔ TRƯỞNG CHUYÊN MÔN</strong><br>
<em>(Ký và ghi rõ họ tên)</em><br><br><br><br>
<strong>Hoàng Tấn Thiên</strong>
</td>
</tr>
</table>

<div align="center">

### CÁC THÀNH VIÊN TRONG TỔ KÝ TÊN XÁC NHẬN

</div>

| Đinh Văn Đông | Hồ Đăng Danh | Hoàng Xuân Ánh | Trần Long Hải |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |

| Nguyễn Văn Tính | Dương Quang Tùng | Trần Sáng | Nguyễn Thị Thảo |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Da xuat thanh cong file Markdown: {out_md_path}")


def tao_bien_ban_hop_to_lan_1_thang_10(out_docx_path, out_md_path=None):
    """
    Soạn thảo hoàn chỉnh Biên bản họp Tổ chuyên môn Lần 1 Tháng 10/2026.
    Chuẩn Nghị định 30/2020/NĐ-CP và đặc thù Trường THCS Trần Phú.
    """
    doc = create_nd30_document()
    
    # 1. Header chuẩn
    add_header_thcs_tran_phu(
        doc,
        so_hieu="04/BB-TCM",
        ngay_thang_str="Xuân Đông, ngày 03 tháng 10 năm 2026"
    )
    
    # 2. Tiêu đề
    add_doc_title(
        doc,
        "BIÊN BẢN HỌP TỔ CHUYÊN MÔN LẦN 1",
        "SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 10/2026 (LẦN 1)\nNăm học: 2026 - 2027"
    )
    
    # 3. Thời gian, địa điểm, thành phần
    add_paragraph_styled(doc, "Hôm nay, vào lúc 07 giờ 30 phút, ngày 03 tháng 10 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 10 năm học 2026 - 2027.", indent=True)
    add_paragraph_styled(doc, "Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.", bold_prefix="- Chủ trì cuộc họp:", indent=True)
    add_paragraph_styled(doc, "Cô **Lê Thị Bình** – Giáo viên môn Toán.", bold_prefix="- Thư ký cuộc họp:", indent=True)
    add_paragraph_styled(doc, "10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).", bold_prefix="- Thành viên tham dự:", indent=True)
    add_paragraph_styled(doc, "Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.", bold_prefix="  + Danh sách thành viên:", indent=True)
    
    # 4. NỘI DUNG CUỘC HỌP
    add_doc_title(doc, "NỘI DUNG CUỘC HỌP", "")
    
    # ==================== PHẦN I ====================
    add_section_h1(doc, "I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN")
    add_paragraph_styled(doc, "Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt sâu sắc các văn bản chỉ đạo của Sở Giáo dục và Đào tạo thành phố Đồng Nai, các cấp quản lý và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:", indent=True)
    
    # 1. Công văn 5529
    add_paragraph_styled(doc, "**1. Hướng dẫn tổ chức kiểm tra, đánh giá học sinh phổ thông và học viên giáo dục thường xuyên năm học 2026 - 2027 (Công văn số 5529/SGDĐT-GDPT&GDTX ngày 28/9/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Quán triệt thực hiện nghiêm túc quy định đổi mới phương pháp kiểm tra, đánh giá định kỳ và thường xuyên theo định hướng phát triển phẩm chất, năng lực học sinh. Xây dựng ma trận, bản đặc tả chi tiết bảo đảm đúng tỷ lệ 4 mức độ nhận thức (Nhận biết 40%, Thông hiểu 30%, Vận dụng 20%, Vận dụng cao 10%); đề kiểm tra bám sát chuẩn kiến thức, kỹ năng chương trình GDPT 2018, bảo đảm tính khách quan, công bằng và phân hóa tốt đối tượng học sinh; đa dạng hóa hình thức đánh giá (trên giấy kết hợp trực tuyến).", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phân công cụ thể giáo viên ra đề cương, ma trận, bản đặc tả và đề kiểm tra giữa kỳ 1 môn Toán (khối 6, 7, 8, 9) và môn Tin học; thực hiện nghiêm túc quy trình phản biện chéo và nộp đề đúng hạn quy định.", indent=True)
    
    # 2. Công văn 3939
    add_paragraph_styled(doc, "**2. Thực hiện Đề án “Tăng cường giảng dạy Tiếng Anh trong các trường phổ thông trên địa bàn tỉnh Đồng Nai” (Công văn số 3939/SGDĐT-NV1 ngày 26/9/2023 của Sở GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Tăng cường lồng ghép các thuật ngữ Tiếng Anh chuyên ngành vào bài giảng chính khóa môn Toán và môn Tin học; khích lệ giáo viên tổ chức các hoạt động ngoại khóa, câu lạc bộ học thuật và sân chơi trí tuệ có yếu tố Tiếng Anh.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tích hợp các câu hỏi Tiếng Anh Toán học vào Chuyên đề Ngoại khóa “Rung chuông vàng” khối 6; hướng dẫn học sinh tiếp cận phần thi Toán Tiếng Anh trong Đấu trường VioEdu; phối hợp quản lý tốt các lớp Tiếng Anh giao tiếp do giáo viên nước ngoài trực tiếp giảng dạy 2 tiết/tuần.", indent=True)
    
    # 3. Quy định dạy thêm, học thêm
    add_paragraph_styled(doc, "**3. Quy định về quản lý dạy thêm, học thêm (Quyết định số 25/2025/QĐ-UBND ngày 14/8/2025; Quyết định sửa đổi số 59/2026/QĐ-UBND ngày 16/7/2026 của UBND thành phố Đồng Nai; Văn bản hợp nhất số 01/2026/VBHN-QĐ-UBND ngày 22/8/2026 và Công văn số 5473/SGDĐT-GDPT&GDTX ngày 25/9/2026 của Sở GD&ĐT):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Quán triệt tinh thần chấn chỉnh, tăng cường kỷ cương quản lý dạy thêm, học thêm trên địa bàn thành phố. Tuyệt đối không tổ chức dạy thêm, học thêm trái quy định dưới bất kỳ hình thức nào; không ép buộc, gợi ý phụ huynh và học sinh tham gia học thêm; nghiêm cấm việc cắt giảm nội dung bài học chính khóa để đưa vào dạy thêm; toàn thể giáo viên ký cam kết chấp hành nghiêm túc quy định pháp luật và giữ gìn đạo đức nhà giáo.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** 100% giáo viên trong tổ Toán – Tin ký cam kết không vi phạm quy định dạy thêm, học thêm; tập trung nâng cao chất lượng từng giờ dạy chính khóa trên lớp và phụ đạo học sinh còn hổng kiến thức miễn phí theo kế hoạch giáo dục của nhà trường.", indent=True)
    
    # 4. Kế hoạch thi HSG
    add_paragraph_styled(doc, "**4. Kế hoạch Tổ chức Kỳ thi chọn học sinh giỏi cấp thành phố năm học 2026 - 2027 (Kế hoạch số 4706/KH-SGDĐT ngày 08/9/2026 của Sở GDĐT thành phố Đồng Nai):**", indent=True)
    add_paragraph_styled(doc, "- **Ý chính cốt lõi:** Kế hoạch tuyển chọn và tổ chức kỳ thi học sinh giỏi THCS cấp thành phố nhằm phát hiện, bồi dưỡng các tài năng trẻ môn Toán và Tin học.", indent=True)
    add_paragraph_styled(doc, "- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn chủ động rà soát, tuyển chọn các nhân tố xuất sắc khối 8 và khối 9, phân công giáo viên có kinh nghiệm phụ trách bồi dưỡng đội tuyển Toán 9 và Tin học 9 nhằm nâng cao chất lượng mũi nhọn của trường.", indent=True)
    
    # ==================== PHẦN II ====================
    add_section_h1(doc, "II. ĐÁNH GIÁ CÔNG TÁC CHUYÊN MÔN CUỐI THÁNG 9/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Giáo viên chủ nhiệm đã ổn định vững chắc nề nếp lớp, duy trì nghiêm túc sinh hoạt 15 phút đầu giờ trước buổi học, quản lý tốt chuyên cần và nền nếp trật tự.", indent=True)
    add_paragraph_styled(doc, "- Bám sát lớp, thực hiện các loại báo cáo kịp thời; hoàn thành thu nộp BHYT, BHTN đợt 1; triển khai chương trình Tiếng Anh tăng cường đến phụ huynh; hoàn thành 100% cập nhật thông tin học sinh lớp chủ nhiệm trên hệ thống CSDL ngành.", indent=True)
    add_paragraph_styled(doc, "- Tích cực vận động học sinh tham gia Đấu trường VioEdu, triển khai thư viện số; phối hợp trợ giảng trong các tiết Tiếng Anh giao tiếp với giáo viên nước ngoài (2 tiết/tuần theo năng lực) bảo đảm hiệu quả.", indent=True)
    
    add_section_h2(doc, "2. Ngày giờ công và kỷ luật lao động:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ đảm bảo ngày giờ công nghiêm túc, tham gia đầy đủ các hoạt động hội họp của nhà trường, dạy đủ số tiết theo phân công chuyên môn; thực hiện chu đáo việc dạy bù, dạy thay khi có giáo viên đi công tác hoặc nghỉ ốm.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn và thực hiện quy chế:")
    add_paragraph_styled(doc, "- Ổn định nền nếp dạy và học theo đúng thời khóa biểu; thực hiện chương trình theo kế hoạch giáo dục nhà trường, dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT, dạy học giáo dục địa phương, GDNGLL và HĐTN đúng định hướng.", indent=True)
    add_paragraph_styled(doc, "- **Về hồ sơ sổ sách và Kế hoạch bài dạy (KHBD):**", indent=True)
    add_paragraph_styled(doc, "  + *Ưu điểm:* Đa số giáo viên trong tổ đã có ý thức chuẩn bị hồ sơ bài dạy đầy đủ theo phân phối chương trình, bảo đảm cấu trúc 4 hoạt động theo tinh thần Công văn 5512/BGDĐT-GDTrH.", indent=True)
    add_paragraph_styled(doc, "  + *Tồn tại, hạn chế cần khắc phục ngay:* Qua đợt kiểm tra hồ sơ bài dạy tháng 9, một số giáo viên thực hiện chưa đúng biểu mẫu quy định. Cụ thể: Kế hoạch bài dạy còn mắc lỗi định dạng công thức toán học, biến dạng ký hiệu góc hình học; các chỉ báo năng lực số (NLS) và trí tuệ nhân tạo (AI) chưa được định dạng in đậm, in nghiêng theo quy định; một số bài soạn chưa đồng bộ Header/Footer theo mẫu chung của nhà trường. Yêu cầu các thầy cô khẩn trương rà soát, chỉnh sửa hoàn thiện trước đợt kiểm tra tiếp theo.", indent=True)
    add_paragraph_styled(doc, "- **Về nền nếp giảng dạy và thực hiện quy chế chuyên môn:**", indent=True)
    add_paragraph_styled(doc, "  + Chấp hành nghiêm túc quy chế chuyên môn, lên lớp đúng giờ, quản lý học sinh tốt trong các tiết học; tuyệt đối không tự ý đổi tiết, bỏ tiết khi chưa có sự phê duyệt của Tổ trưởng và Ban Giám hiệu.", indent=True)
    add_paragraph_styled(doc, "  + Thực hiện ghi chép Sổ đầu bài đầy đủ, sạch sẽ, khớp 100% với tiến độ phân phối chương trình và Kế hoạch giáo dục của tổ (Phụ lục 3).", indent=True)
    add_paragraph_styled(doc, "  + Công tác kiểm tra đánh giá thường xuyên: Giáo viên các bộ môn đã chủ động kiểm tra theo tiến độ, vào điểm và cập nhật kịp thời trên phần mềm quản lý điểm của trường.", indent=True)
    add_paragraph_styled(doc, "  + Nền nếp phòng học bộ môn: Giáo viên Tin học duy trì nền nếp phòng máy vi tính nghiêm túc, hướng dẫn học sinh thực hiện đúng nội quy phòng máy, bảo đảm an toàn thiết bị điện và bảo quản máy móc phục vụ giảng dạy.", indent=True)
    
    # Bảng xếp loại hồ sơ chuyên môn tháng 9
    add_paragraph_styled(doc, "- **Kết quả xếp loại hồ sơ chuyên môn tháng 9/2026:**", indent=True)
    
    ratings_data = [
        ("STT", "Họ và tên giáo viên", "Môn giảng dạy", "Số tiết nộp", "Xếp loại tháng 9"),
        ("1", "Hoàng Tấn Thiên", "Toán 9, Tin học 6", "Đầy đủ", "Tốt"),
        ("2", "Hồ Đăng Danh", "Toán 6, Toán 9", "Đầy đủ", "Tốt"),
        ("3", "Trần Sáng", "Toán 6, Toán 9", "Đầy đủ", "Tốt"),
        ("4", "Trần Long Hải", "Toán 8", "Đầy đủ", "Khá"),
        ("5", "Nguyễn Thị Thảo", "Toán 6, Toán 7", "Đầy đủ", "Khá"),
        ("6", "Lê Thị Bình", "Toán 7, Toán 8, HĐTN", "Đầy đủ", "Khá"),
        ("7", "Hoàng Xuân Ánh", "Toán 7, HĐTN 6", "Đầy đủ", "Khá"),
        ("8", "Nguyễn Văn Tính", "HĐTN 7", "Đầy đủ", "Khá"),
        ("9", "Đinh Văn Đông", "Toán 8", "Đầy đủ", "Khá"),
        ("10", "Dương Quang Tùng", "Tin học 6, 7, 8, 9", "Đầy đủ", "Tốt")
    ]
    
    tbl_rate = doc.add_table(rows=len(ratings_data), cols=5)
    tbl_rate.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_borders_closed(tbl_rate)
    r_widths = [Inches(0.6), Inches(2.2), Inches(2.0), Inches(1.1), Inches(1.19)]
    
    for r_idx, row in enumerate(tbl_rate.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.width = r_widths[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Inches(0)
            
            val = ratings_data[r_idx][c_idx]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.size = Pt(13)
                run.font.bold = True
            else:
                run.font.size = Pt(13)
                if c_idx in (0, 3, 4):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    
    # Kết quả VioEdu vòng 1
    add_paragraph_styled(doc, "- **Tổng hợp số lượng học sinh tham gia thi Đấu trường VioEdu vòng sơ loại 1:** Toàn trường có **107 học sinh** tham gia dự thi. Cụ thể từng khối: Khối 6 đạt 30 học sinh; Khối 7 đạt 24 học sinh; Khối 8 đạt 31 học sinh; Khối 9 đạt 22 học sinh.", indent=True)
    
    add_section_h2(doc, "4. Công tác chuyên đề, thao giảng:")
    add_paragraph_styled(doc, "- Tham gia đầy đủ các buổi tập huấn chuyên môn, chuyên đề do Sở GD&ĐT tổ chức; phổ biến lại trong nhóm bộ môn để triển khai thống nhất.", indent=True)
    
    add_section_h2(doc, "5. Công tác ngoại khóa và phong trào:")
    add_paragraph_styled(doc, "- Đã thực hiện tốt hoạt động GDNGLL theo chủ điểm: Tổ chức Tết Trung thu vui tươi, an toàn cho học sinh; tuyên truyền học sinh chấp hành tốt nội quy trường lớp, tham gia các cuộc thi do Nhà trường và Đoàn - Đội phát động.", indent=True)
    
    add_section_h2(doc, "6. Công tác kiểm tra nội bộ:")
    add_paragraph_styled(doc, "- Kiểm tra nền nếp ra vào lớp, việc thực hiện quy chế chuyên môn, chất lượng soạn giảng và tiến độ thực hiện chương trình.", indent=True)
    
    add_section_h2(doc, "7. Sử dụng thiết bị dạy học và phòng bộ môn:")
    add_paragraph_styled(doc, "- Giáo viên trong tổ sử dụng có hiệu quả phòng thực hành Tin học, phòng học chức năng, khai thác triệt để các phần mềm dạy học phục vụ bài giảng.", indent=True)
    
    add_section_h2(doc, "8. Công tác khác:")
    add_paragraph_styled(doc, "- Tích cực tham gia các phong trào thi đua của Đoàn – Đội, tham gia đầy đủ công tác điều tra phổ cập giáo dục theo phân công của xã.", indent=True)
    
    # ==================== PHẦN III ====================
    add_section_h1(doc, "III. KẾ HOẠCH HOẠT ĐỘNG CHUYÊN MÔN THÁNG 10/2026")
    
    add_section_h2(doc, "1. Công tác chủ nhiệm:")
    add_paragraph_styled(doc, "- Ổn định nền nếp lớp chủ nhiệm, tích cực sinh hoạt 15 phút đầu giờ. Phát động đợt thi đua cao điểm chào mừng các ngày lễ lớn trong tháng: Ngày Quốc tế Người cao tuổi (01/10), Ngày Khuyến học Việt Nam (02/10), Ngày Bác Hồ gửi bức thư cuối cùng cho ngành Giáo dục (15/10) và Ngày Phụ nữ Việt Nam (20/10). Tuyên truyền phòng chống ma túy, tội phạm, ATGT, PCCC và phòng tránh tai nạn thương tích.", indent=True)
    add_paragraph_styled(doc, "- Thực hiện hiệu quả Tuần lễ học tập suốt đời năm 2026; hoàn thành hồ sơ sổ sách GVCN đúng quy định; tiếp tục rà soát học sinh khó khăn; đôn đốc thu nộp BHYT, BHTN; thông tin thường xuyên qua Zalo lớp.", indent=True)
    add_paragraph_styled(doc, "- Vận động học sinh đăng ký thi VioEdu các vòng tiếp theo; triển khai thư viện số và tiết học thư viện theo thời khóa biểu. Giáo viên bộ môn tích hợp bài dạy STEM (Phụ lục 2) vào Kế hoạch bài dạy theo thời điểm, hướng dẫn học sinh nộp sản phẩm tại phòng STEM.", indent=True)
    
    add_section_h2(doc, "2. Đảm bảo ngày giờ công và nền nếp chuyên môn:")
    add_paragraph_styled(doc, "- Giáo viên phấn đấu đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ hoạt động của trường; dạy đúng, dạy đủ số tiết theo phân công chuyên môn; thực hiện kịp thời việc dạy bù, dạy thay khi có phân công.", indent=True)
    
    add_section_h2(doc, "3. Công tác chuyên môn trọng tâm:")
    
    # 3.1. Chuẩn bị kiểm tra nội bộ
    add_paragraph_styled(doc, "*- Chuẩn bị công tác kiểm tra nội bộ nhà trường (Thanh tra toàn diện):*", indent=True)
    add_paragraph_styled(doc, "  + Đối tượng kiểm tra: Thầy **Trần Sáng** (thực hiện theo Kế hoạch kiểm tra nội bộ năm học 2026 - 2027 của Trường THCS Trần Phú).", indent=True)
    add_paragraph_styled(doc, "  + Yêu cầu chuẩn bị: Thầy Sáng chuẩn bị chu đáo toàn bộ hồ sơ chuyên môn cá nhân (Kế hoạch bài dạy chuẩn CV 5512, sổ theo dõi và đánh giá học sinh, kế hoạch dạy học cá nhân, thiết bị và đồ dùng dạy học).", indent=True)
    add_paragraph_styled(doc, "  + Phân công phối hợp: Thầy Sáng chủ động gửi Thời khóa biểu và lịch dạy trong tuần cho Tổ trưởng để tổ sắp xếp báo cáo Ban Giám hiệu, đồng thời phân công giáo viên trong tổ bố trí dự giờ, đóng góp ý kiến mang tính xây dựng chuyên môn.", indent=True)
    
    # 3.2. Kế hoạch Rung chuông vàng
    add_paragraph_styled(doc, "*- Kế hoạch Chuyên đề Ngoại khóa “Rung chuông vàng” môn Toán khối 6:*", indent=True)
    add_paragraph_styled(doc, "Nhằm tạo sân chơi học tập bổ ích, khơi dậy niềm đam mê học Toán và nâng cao kỹ năng vận dụng kiến thức thực tế cho học sinh khối 6, Tổ Toán – Tin thống nhất thành lập Ban Tổ chức và xây dựng tiến độ triển khai chuyên đề ngoại khóa như sau:", indent=True)
    add_paragraph_styled(doc, "• **Thành lập Ban Tổ chức chuyên đề:**", indent=True)
    add_paragraph_styled(doc, "  + Nhóm biên soạn nội dung và ngân hàng đề: Cô Nguyễn Thị Thảo (Chủ đạo, phụ trách khối 6); Cô Lê Thị Bình (Hỗ trợ xây dựng và rà soát câu hỏi).", indent=True)
    add_paragraph_styled(doc, "  + Nhóm tư vấn và thẩm định chuyên môn: Thầy Hoàng Tấn Thiên (Trưởng ban), Thầy Hồ Đăng Danh, Thầy Nguyễn Văn Tính, Thầy Đinh Văn Đông.", indent=True)
    add_paragraph_styled(doc, "  + Nhóm hỗ trợ tổ chức và kỹ thuật - hậu cần: Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Thầy Dương Quang Tùng, Thầy Trần Sáng (chuẩn bị âm thanh, máy chiếu, bảng con, sân bãi).", indent=True)
    add_paragraph_styled(doc, "  + Phân công Cô Nguyễn Thị Thảo rà soát, xây dựng kịch bản chi tiết phù hợp với thực tế nhà trường.", indent=True)
    
    # Bảng tiến độ Rung chuông vàng
    add_paragraph_styled(doc, "• **Lịch trình và tiến độ thực hiện chi tiết (Thực hiện trong tháng 11/2026):**", indent=True)
    
    rcv_data = [
        ("Thời gian", "Nội dung công việc", "Người phụ trách", "Ghi chú / Sản phẩm"),
        ("08/10 – 15/10/2026", "Xây dựng khung thể lệ; biên soạn bộ ngân hàng 35 câu hỏi Toán 6 (30 câu chính, 5 câu phụ; tích hợp câu hỏi thực tiễn và Tiếng Anh Toán học).", "Cô Thảo, Cô Bình", "Bản thảo đề & đáp án"),
        ("16/10 – 22/10/2026", "Họp nhóm tư vấn thẩm định câu hỏi; Tổ trưởng hoàn thiện kế hoạch chi tiết trình BGH phê duyệt; Cô Thảo xem lịch chọn ngày cụ thể.", "Thầy Thiên, Thầy Danh, Thầy Tính, Thầy Đông, Cô Thảo", "Kế hoạch được BGH duyệt"),
        ("23/10 – 31/10/2026", "Thông báo thể lệ đến các lớp khối 6; các lớp lập danh sách học sinh tham gia (15 HS/lớp); nhóm hỗ trợ chuẩn bị bảng con, phấn, chuông, sân bãi.", "Cô Thảo, Thầy Ánh, Thầy Hải, Thầy Tùng, Thầy Sáng", "Danh sách thí sinh & CSVC"),
        ("01/11 – 07/11/2026", "Chạy thử chương trình, kiểm tra hệ thống âm thanh, máy chiếu trình chiếu câu hỏi; phân công dẫn chương trình (MC) và cứu trợ.", "Toàn thể thành viên Ban Tổ chức", "Hoàn tất chuẩn bị"),
        ("Tuần 2 Tháng 11/2026\n(Dự kiến 14/11/2026)", "Tổ chức chính thức Chuyên đề Ngoại khóa “Rung chuông vàng môn Toán khối 6” chào mừng kỷ niệm Ngày Nhà giáo Việt Nam 20/11.", "Tổ Toán – Tin phối hợp Đoàn - Đội", "Tổng kết, trao thưởng")
    ]
    
    tbl_rcv = doc.add_table(rows=len(rcv_data), cols=4)
    tbl_rcv.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_borders_closed(tbl_rcv)
    rcv_widths = [Inches(1.8), Inches(2.6), Inches(1.5), Inches(1.19)]
    
    for r_idx, row in enumerate(tbl_rcv.rows):
        for c_idx, cell in enumerate(row.cells):
            cell.width = rcv_widths[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Inches(0)
            
            val = rcv_data[r_idx][c_idx]
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.size = Pt(13)
                run.font.bold = True
            else:
                run.font.size = Pt(12)
                if c_idx in (0, 2, 3):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    
    # 3.3. Ma trận, bản đặc tả, đề kiểm tra Giữa HKI
    add_paragraph_styled(doc, "*- Công tác xây dựng Ma trận, Bản đặc tả, Đề cương và Đề kiểm tra giữa học kỳ 1:*", indent=True)
    add_paragraph_styled(doc, "  + Toàn tổ thực hiện nghiêm túc Công văn số 5529/SGDĐT-GDPT&GDTX của Sở GD&ĐT thành phố Đồng Nai về tổ chức kiểm tra, đánh giá định kỳ.", indent=True)
    add_paragraph_styled(doc, "  + **Yêu cầu chuyên môn:** Ma trận và bản đặc tả phải bám sát nội dung chương trình GDPT 2018, bảo đảm đúng tỉ lệ 4 mức độ nhận thức (Nhận biết 40%, Thông hiểu 30%, Vận dụng 20%, Vận dụng cao 10%). Đề kiểm tra phải bám sát ma trận và đề cương ôn tập, có tính phân hóa phù hợp với đối tượng học sinh.", indent=True)
    add_paragraph_styled(doc, "  + **Phân công phụ trách xây dựng đề cương, ma trận và đề kiểm tra:** Môn Toán khối 6 do Cô Nguyễn Thị Thảo phụ trách; Môn Toán khối 7 do Thầy Hoàng Xuân Ánh phụ trách; Môn Toán khối 8 do Cô Lê Thị Bình phụ trách; Môn Toán khối 9 do Thầy Trần Sáng phụ trách; Môn Tin học (Khối 6, 7, 8, 9) do Thầy Dương Quang Tùng phụ trách.", indent=True)
    add_paragraph_styled(doc, "  + **Hình thức và thời lượng kiểm tra thống nhất toàn tổ:**", indent=True)
    add_paragraph_styled(doc, "    • Môn Toán (Khối 6, 7, 8, 9): Thời gian làm bài 60 phút; hình thức: 100% Tự luận làm trên giấy thi theo đúng hướng dẫn kiểm tra định kỳ.", indent=True)
    add_paragraph_styled(doc, "    • Môn Tin học (Khối 6, 7, 8, 9): Thời gian làm bài 45 phút; hình thức: Kiểm tra trực tuyến trên phòng máy vi tính thông qua nền tảng OLM (đảm bảo tính khách quan, tự động trộn đề và chấm điểm).", indent=True)
    add_paragraph_styled(doc, "  + **Tiến độ và các mốc thời gian thực hiện bắt buộc:**", indent=True)
    add_paragraph_styled(doc, "    • **Ngày 15/10/2026:** Hạn chót nộp Ma trận, Bản đặc tả và Đề cương ôn tập về Tổ trưởng chuyên môn thẩm định và duyệt.", indent=True)
    add_paragraph_styled(doc, "    • **Ngày 24/10/2026:** Hạn chót nộp Đề kiểm tra giữa kỳ (kèm hướng dẫn chấm/thang điểm) và hoàn thành công tác phản biện chéo giữa các giáo viên trong nhóm bộ môn.", indent=True)
    add_paragraph_styled(doc, "    • **Ngày 28/10/2026:** Tổ trưởng chuyên môn tổng hợp, thẩm định lần cuối và chính thức nộp toàn bộ Đề thi giữa kỳ về bộ phận Chuyên môn nhà trường (Ban Giám hiệu) để chuẩn bị công tác in sao và tổ chức kiểm tra theo kế hoạch.", indent=True)
    
    # 3.4. Nghiên cứu bài học
    add_paragraph_styled(doc, "*- Kế hoạch Sinh hoạt chuyên môn theo Nghiên cứu bài học (NCBH) trong tháng 11/2026:*", indent=True)
    add_paragraph_styled(doc, "Nhằm bảo đảm tính liên tục và nâng cao chất lượng dạy học ở các khối lớp trọng tâm, Tổ chuyên môn thống nhất không tổ chức nghiên cứu bài học ở khối 6 (do khối 6 đang tập trung cho Chuyên đề Ngoại khóa Rung chuông vàng) mà chuyển trọng tâm sang khối 8 và khối 9 trong tháng 11/2026 (sau kỳ kiểm tra giữa học kỳ 1) với định hướng chi tiết như sau:", indent=True)
    add_paragraph_styled(doc, "  + **Bài học trọng tâm được lựa chọn:** Môn Toán lớp 8 – Bài “Định lí Thalès trong tam giác” (Chương Định lí Thalès, bộ sách GDPT 2018; phân phối chương trình dạy vào trung tuần tháng 11).", indent=True)
    add_paragraph_styled(doc, "  + **Chuyên đề định hướng nâng cao lớp 9:** Nhóm giáo viên dạy Toán 9 (Thầy Thiên, Thầy Danh, Thầy Sáng) đồng thời chuẩn bị chuyên đề sinh hoạt chuyên môn “Đổi mới phương pháp dạy học Hàm số bậc nhất và Rèn kỹ năng giải toán thực tế cho học sinh lớp 9 ôn thi Tuyển sinh 10”.", indent=True)
    add_paragraph_styled(doc, "  + **Lý do lựa chọn bài “Định lí Thalès trong tam giác” (Lớp 8):** (1) Bài học mang tính nền tảng và bước ngoặt của hình học lớp 8, giúp học sinh chuyển từ hình học trực quan sang tư duy suy luận tỉ số đoạn thẳng tỉ lệ; (2) Khả năng ứng dụng thực tế và giáo dục STEM rất cao (học sinh thực hành đo bóng mặt trời để xác định chiều cao cột cờ, cây xanh; đo khoảng cách giữa hai điểm qua chướng ngại vật); (3) Rất thuận lợi ứng dụng Năng lực số (sử dụng phần mềm hình học động GeoGebra để trực quan quan sát các tỉ số đoạn thẳng tỉ lệ không đổi).", indent=True)
    add_paragraph_styled(doc, "  + **Tiến độ và phân công thực hiện:** Cô Lê Thị Bình (phụ trách chính khối 8) chủ trì xây dựng Kế hoạch bài dạy minh họa; Thầy Trần Long Hải và Thầy Nguyễn Văn Tính phối hợp hỗ trợ thiết kế phiếu học tập, chuẩn bị dụng cụ đo đạc thực hành (thước dây, giác kế mini). Thời gian dạy thể nghiệm dự kiến vào Tuần 1 hoặc Tuần 2 Tháng 11/2026.", indent=True)
    
    # 3.5. Góp ý SGK
    add_paragraph_styled(doc, "*- Góp ý chuyên sâu chương trình Sách giáo khoa GDPT 2018 môn Toán - Tin:*", indent=True)
    add_paragraph_styled(doc, "  + **Đại số 9:** Trong bài kiểm tra, phần giải bài toán bằng cách lập hệ phương trình, trong quá trình làm bài học sinh được phép sử dụng máy tính cầm tay để bấm nghiệm kiểm tra kết quả và ghi bước kết luận theo đúng tinh thần giảm tải tính toán cơ học.", indent=True)
    add_paragraph_styled(doc, "  + **Hình học 9:** Các hệ thức lượng trong tam giác vuông (như trong SGK cũ) không được áp dụng trực tiếp như định lý sẵn có để làm bài tập; nếu học sinh sử dụng trong bài thi thì bắt buộc phải chứng minh lại bằng tam giác đồng dạng, tuân thủ đúng kết luận thống nhất của Hội đồng bộ môn cấp tỉnh.", indent=True)
    
    add_section_h2(doc, "4. Công tác chuyên đề và bồi dưỡng:")
    add_paragraph_styled(doc, "- Phát động phong trào thi đua chào mừng ngày Phụ nữ Việt Nam 20/10: Mỗi giáo viên trong tổ đăng ký ít nhất 01 tiết dạy tốt, tăng cường ứng dụng công nghệ thông tin và chuyển đổi số trong giảng dạy.", indent=True)
    add_paragraph_styled(doc, "- Chuẩn bị chu đáo công tác bồi dưỡng học sinh giỏi khối 8, 9 theo đúng tinh thần Kế hoạch số 4706/KH-SGDĐT của Sở GD&ĐT; lập danh sách học sinh cần hỗ trợ để phụ đạo kịp thời.", indent=True)
    add_paragraph_styled(doc, "- Tiếp tục quán triệt thực hiện nghiêm túc quy định về dạy thêm, học thêm (Quyết định số 25/2025/QĐ-UBND, Quyết định số 59/2026/QĐ-UBND, Văn bản hợp nhất số 01/2026/VBHN-QĐ-UBND và Công văn 5473/SGDĐT-GDPT&GDTX); tuyệt đối không vi phạm đạo đức nhà giáo.", indent=True)
    
    # ==================== PHẦN IV ====================
    add_section_h1(doc, "IV. Ý KIẾN THẢO LUẬN VÀ GIẢI PHÁP CHUYÊN MÔN THỰC CHIẾN")
    add_paragraph_styled(doc, "Phiên họp diễn ra sôi nổi, thẳng thắn, phản ánh đúng thực tế lớp học và đề xuất các giải pháp kỹ thuật cụ thể:", indent=True)
    
    add_paragraph_styled(doc, "- **Cô Lê Thị Bình (Giáo viên môn Toán 8, Thư ký):** Qua theo dõi vòng 1 Đấu trường VioEdu, còn một số học sinh ở các lớp bỏ thi hoặc điểm đạt được chưa cao. Đề nghị các thầy cô giáo viên phụ trách khối cần chủ động phối hợp chặt chẽ với giáo viên chủ nhiệm để nhắc nhở các em vào thi trước khi hệ thống tự động khóa vòng vào 23h59 Chủ nhật hàng tuần. Về nhiệm vụ dạy minh họa Nghiên cứu bài học bài “Định lí Thalès trong tam giác”, tôi nhất trí nhận nhiệm vụ và sẽ kết hợp hoạt động đo đạc thực tế ngoài sân trường với mô phỏng GeoGebra; cam kết nộp đề cương Toán 8 giữa kỳ đúng hạn 15/10/2026.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Trần Long Hải (Giáo viên môn Toán 8):** Đề nghị Ban Thi đua nhà trường phổ biến rõ ràng, cụ thể tiêu chí chấm điểm thi đua cho đội cờ đỏ/sao đỏ các lớp để bảo đảm chấm điểm đồng đều, khách quan giữa các lớp (hiện nay đang có sự chênh lệch cách chấm giữa học sinh học ở Cơ sở 1 và Cơ sở 2). Đồng thời, Thầy Hải cam kết sẽ phối hợp cùng Thầy Tính hỗ trợ cô Bình thiết kế phiếu học tập và chuẩn bị dụng cụ đo đạc thực hành cho tiết dạy minh họa Thalès.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Hoàng Xuân Ánh (Giáo viên môn Toán 7, Phụ trách VioEdu K7):** Hoàn toàn nhất trí với phần đánh giá và kế hoạch hoạt động của tổ chuyên môn. Nhóm Toán 7 sẽ tập trung bám sát chuẩn kiến thức kỹ năng để xây dựng ma trận và đề cương kiểm tra giữa kỳ 1 có tính phân hóa phù hợp với học sinh khối 7, bảo đảm nộp đúng hạn 15/10/2026.", indent=True)
    
    add_paragraph_styled(doc, "- **Cô Nguyễn Thị Thảo (Giáo viên môn Toán 6, Phụ trách VioEdu K6):** Cảm ơn tổ chuyên môn đã đồng thuận chuyển nhiệm vụ Nghiên cứu bài học sang khối 8, tạo điều kiện thuận lợi cho nhóm Toán 6 tập trung toàn lực xây dựng bộ ngân hàng 35 câu hỏi và kịch bản chi tiết cho Chuyên đề Ngoại khóa “Rung chuông vàng môn Toán khối 6” chào mừng ngày 20/11; cam kết hoàn thành dự thảo ngân hàng câu hỏi trước ngày 15/10/2026.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Trần Sáng (Giáo viên môn Toán 9, KTNB):** Tiếp thu toàn diện kế hoạch kiểm tra nội bộ của nhà trường; Thầy Sáng cam kết hoàn thiện hồ sơ Kế hoạch bài dạy chuẩn Công văn 5512, tích hợp chỉ báo Năng lực số và AI in đậm, in nghiêng rõ nét theo đúng kết luận rút kinh nghiệm của tổ; chủ động gửi lịch dạy trong tuần cho Tổ trưởng để tổ sắp xếp dự giờ. Về ma trận và đề kiểm tra Toán 9, Thầy Sáng đảm bảo bám sát cấu trúc đề thi tuyển sinh 10, nộp đúng tiến độ (ma trận ngày 15/10, đề kiểm tra ngày 24/10) để tổ phản biện chéo.", indent=True)
    
    add_paragraph_styled(doc, "- **Thầy Dương Quang Tùng (Giáo viên Tin học, Phụ trách phòng máy):** Báo cáo tình hình chuẩn bị cho kỳ kiểm tra giữa kỳ môn Tin học: 2 phòng máy tính (45 máy) đã được kiểm tra đường truyền và cài đặt ổn định; sẵn sàng tổ chức cho học sinh làm bài kiểm tra trực tuyến 100% trên nền tảng OLM theo đúng thời lượng 45 phút. Thầy Tùng cũng sẽ hỗ trợ kỹ thuật âm thanh, máy chiếu và trình chiếu câu hỏi cho sân chơi Rung chuông vàng khối 6.", indent=True)
    
    # ==================== PHẦN V ====================
    add_section_h1(doc, "V. KẾT LUẬN CỦA CHỦ TỌA VÀ NGHỊ QUYẾT CUỘC HỌP")
    add_paragraph_styled(doc, "Thầy Tổ trưởng chuyên môn Hoàng Tấn Thiên kết luận toàn diện phiên họp và chỉ đạo thực hiện các nhiệm vụ trọng tâm sau:", indent=True)
    add_paragraph_styled(doc, "1. Toàn thể giáo viên trong tổ thực hiện chuẩn xác 03 mốc thời gian kiểm tra giữa kỳ 1: (1) Ngày 15/10/2026: Nộp Ma trận, Bản đặc tả và Đề cương ôn tập về Tổ trưởng duyệt; (2) Ngày 24/10/2026: Nộp Đề kiểm tra giữa kỳ và hoàn tất phản biện chéo trong nhóm; (3) Ngày 28/10/2026: Tổ trưởng chính thức nộp toàn bộ đề thi về Ban Giám hiệu để in sao.", indent=True)
    add_paragraph_styled(doc, "2. Yêu cầu 100% giáo viên khẩn trương rà soát, chỉnh sửa ngay các tồn tại về hồ sơ bài dạy: Khắc phục lỗi công thức toán, sửa ký hiệu góc hình học, định dạng in đậm và in nghiêng các chỉ báo Năng lực số (NLS), AI, đồng bộ Header/Footer theo mẫu chung.", indent=True)
    add_paragraph_styled(doc, "3. Phối hợp chuẩn bị chu đáo công tác kiểm tra nội bộ toàn diện đối với Thầy Trần Sáng; đẩy mạnh xây dựng ngân hàng đề Rung chuông vàng khối 6; nhóm Toán 8 khẩn trương hoàn thiện Kế hoạch bài dạy minh họa bài “Định lí Thalès trong tam giác” tích hợp GeoGebra và thực hành STEM.", indent=True)
    add_paragraph_styled(doc, "4. Giáo viên phụ trách các khối tiếp tục đôn đốc học sinh tham gia đầy đủ các vòng thi Đấu trường VioEdu; GVCN phối hợp quản lý tốt các tiết Tiếng Anh giao tiếp với giáo viên nước ngoài.", indent=True)
    add_paragraph_styled(doc, "5. Chấp hành nghiêm túc quy định pháp luật về dạy thêm, học thêm; tuyệt đối không vi phạm đạo đức nhà giáo.", indent=True)
    
    add_paragraph_styled(doc, "**Biểu quyết:** 10/10 thành viên trong tổ (100% giáo viên) nhất trí hoàn toàn với nội dung cuộc họp.", indent=True)
    add_paragraph_styled(doc, "Biên bản kết thúc vào lúc 10 giờ 00 phút cùng ngày./.", indent=True)
    
    # Chữ ký 2 bên
    add_signatures(
        doc,
        left_title="THƯ KÝ CUỘC HỌP",
        left_name="Lê Thị Bình",
        right_title="TỔ TRƯỞNG CHUYÊN MÔN",
        right_name="Hoàng Tấn Thiên"
    )
    
    # Bảng ký xác nhận của các thành viên khác
    p_mem_head = doc.add_paragraph()
    p_mem_head.paragraph_format.space_before = Pt(12)
    p_mem_head.paragraph_format.space_after = Pt(4)
    r_mh = p_mem_head.add_run("CÁC THÀNH VIÊN TRONG TỔ KÝ TÊN XÁC NHẬN")
    r_mh.font.name = 'Times New Roman'
    r_mh.font.size = Pt(13)
    r_mh.bold = True
    p_mem_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    tbl_ack = doc.add_table(rows=3, cols=4)
    tbl_ack.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_table_borders_closed(tbl_ack)
    
    ack_names = [
        ["Đinh Văn Đông", "Hồ Đăng Danh", "Hoàng Xuân Ánh", "Trần Long Hải"],
        ["Nguyễn Văn Tính", "Dương Quang Tùng", "Trần Sáng", "Nguyễn Thị Thảo"]
    ]
    
    # Hàng 1
    for c_idx in range(4):
        cell = tbl_ack.cell(0, c_idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"**{ack_names[0][c_idx]}**\n\n*(Ký tên)*")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    # Hàng 2
    for c_idx in range(4):
        cell = tbl_ack.cell(1, c_idx)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"**{ack_names[1][c_idx]}**\n\n*(Ký tên)*")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
        
    save_docx_robust(doc, out_docx_path)
    
    if out_md_path:
        tao_bien_ban_hop_to_lan_1_thang_10_md(out_md_path)


def tao_bien_ban_hop_to_lan_1_thang_10_md(out_md_path):
    md_content = """# BIÊN BẢN SINH HOẠT CHUYÊN MÔN TỔ TOÁN – TIN THÁNG 10/2026 (LẦN 1)
**Trường THCS Trần Phú – Tổ Toán - Tin**  
**Số: 04/BB-TCM**  
*Xuân Đông, ngày 03 tháng 10 năm 2026*

---

Hôm nay, vào lúc 07 giờ 30 phút, ngày 03 tháng 10 năm 2026, tại Phòng sinh hoạt chuyên môn Trường THCS Trần Phú, Tổ Toán – Tin học đã tiến hành phiên họp chuyên môn định kỳ lần 1 tháng 10 năm học 2026 - 2027.

- **Chủ trì cuộc họp:** Thầy **Hoàng Tấn Thiên** – Tổ trưởng chuyên môn.
- **Thư ký cuộc họp:** Cô **Lê Thị Bình** – Giáo viên môn Toán.
- **Thành viên tham dự:** 10/10 thành viên trong tổ (Có mặt: 10/10, Vắng: 0).
  + *Danh sách thành viên:* Thầy Hoàng Tấn Thiên, Thầy Trần Sáng, Thầy Đinh Văn Đông, Thầy Hồ Đăng Danh, Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Cô Lê Thị Bình, Cô Nguyễn Thị Thảo, Thầy Nguyễn Văn Tính, Thầy Dương Quang Tùng.

### NỘI DUNG CUỘC HỌP

## I. TRIỂN KHAI VĂN BẢN CHỈ ĐẠO CỦA CẤP TRÊN

Thầy Tổ trưởng Hoàng Tấn Thiên phổ biến, quán triệt sâu sắc các văn bản chỉ đạo của Sở Giáo dục và Đào tạo thành phố Đồng Nai, các cấp quản lý và kế hoạch của nhà trường; nêu rõ các nội dung cốt lõi và tóm tắt tác động trực tiếp đến nhiệm vụ của tổ chuyên môn như sau:

**1. Hướng dẫn tổ chức kiểm tra, đánh giá học sinh phổ thông và học viên giáo dục thường xuyên năm học 2026 - 2027 (Công văn số 5529/SGDĐT-GDPT&GDTX ngày 28/9/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Quán triệt thực hiện nghiêm túc quy định đổi mới phương pháp kiểm tra, đánh giá định kỳ và thường xuyên theo định hướng phát triển phẩm chất, năng lực học sinh. Xây dựng ma trận, bản đặc tả chi tiết bảo đảm đúng tỷ lệ 4 mức độ nhận thức (Nhận biết 40%, Thông hiểu 30%, Vận dụng 20%, Vận dụng cao 10%); đề kiểm tra bám sát chuẩn kiến thức, kỹ năng chương trình GDPT 2018, bảo đảm tính khách quan, công bằng và phân hóa tốt đối tượng học sinh; đa dạng hóa hình thức đánh giá (trên giấy kết hợp trực tuyến).
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn phân công cụ thể giáo viên ra đề cương, ma trận, bản đặc tả và đề kiểm tra giữa kỳ 1 môn Toán (khối 6, 7, 8, 9) và môn Tin học; thực hiện nghiêm túc quy trình phản biện chéo và nộp đề đúng hạn quy định.

**2. Thực hiện Đề án “Tăng cường giảng dạy Tiếng Anh trong các trường phổ thông trên địa bàn tỉnh Đồng Nai” (Công văn số 3939/SGDĐT-NV1 ngày 26/9/2023 của Sở GD&ĐT):**
- **Ý chính cốt lõi:** Tăng cường lồng ghép các thuật ngữ Tiếng Anh chuyên ngành vào bài giảng chính khóa môn Toán và môn Tin học; khích lệ giáo viên tổ chức các hoạt động ngoại khóa, câu lạc bộ học thuật và sân chơi trí tuệ có yếu tố Tiếng Anh.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tích hợp các câu hỏi Tiếng Anh Toán học vào Chuyên đề Ngoại khóa “Rung chuông vàng” khối 6; hướng dẫn học sinh tiếp cận phần thi Toán Tiếng Anh trong Đấu trường VioEdu; phối hợp quản lý tốt các lớp Tiếng Anh giao tiếp do giáo viên nước ngoài trực tiếp giảng dạy 2 tiết/tuần.

**3. Quy định về quản lý dạy thêm, học thêm (Quyết định số 25/2025/QĐ-UBND ngày 14/8/2025; Quyết định sửa đổi số 59/2026/QĐ-UBND ngày 16/7/2026 của UBND thành phố Đồng Nai; Văn bản hợp nhất số 01/2026/VBHN-QĐ-UBND ngày 22/8/2026 và Công văn số 5473/SGDĐT-GDPT&GDTX ngày 25/9/2026 của Sở GD&ĐT):**
- **Ý chính cốt lõi:** Quán triệt tinh thần chấn chỉnh, tăng cường kỷ cương quản lý dạy thêm, học thêm trên địa bàn thành phố. Tuyệt đối không tổ chức dạy thêm, học thêm trái quy định dưới bất kỳ hình thức nào; không ép buộc, gợi ý phụ huynh và học sinh tham gia học thêm; nghiêm cấm việc cắt giảm nội dung bài học chính khóa để đưa vào dạy thêm; toàn thể giáo viên ký cam kết chấp hành nghiêm túc quy định pháp luật và giữ gìn đạo đức nhà giáo.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** 100% giáo viên trong tổ Toán – Tin ký cam kết không vi phạm quy định dạy thêm, học thêm; tập trung nâng cao chất lượng từng giờ dạy chính khóa trên lớp và phụ đạo học sinh còn hổng kiến thức miễn phí theo kế hoạch giáo dục của nhà trường.

**4. Kế hoạch Tổ chức Kỳ thi chọn học sinh giỏi cấp thành phố năm học 2026 - 2027 (Kế hoạch số 4706/KH-SGDĐT ngày 08/9/2026 của Sở GDĐT thành phố Đồng Nai):**
- **Ý chính cốt lõi:** Kế hoạch tuyển chọn và tổ chức kỳ thi học sinh giỏi THCS cấp thành phố nhằm phát hiện, bồi dưỡng các tài năng trẻ môn Toán và Tin học.
- **Vấn đề liên quan trực tiếp đến nhà trường và tổ chuyên môn khi thực hiện:** Tổ chuyên môn chủ động rà soát, tuyển chọn các nhân tố xuất sắc khối 8 và khối 9, phân công giáo viên có kinh nghiệm phụ trách bồi dưỡng đội tuyển Toán 9 và Tin học 9 nhằm nâng cao chất lượng mũi nhọn của trường.

---

## II. ĐÁNH GIÁ CÔNG TÁC CHUYÊN MÔN CUỐI THÁNG 9/2026

### **1. Công tác chủ nhiệm:**
- Giáo viên chủ nhiệm đã ổn định vững chắc nề nếp lớp, duy trì nghiêm túc sinh hoạt 15 phút đầu giờ trước buổi học, quản lý tốt chuyên cần và nền nếp trật tự.
- Bám sát lớp, thực hiện các loại báo cáo kịp thời; hoàn thành thu nộp BHYT, BHTN đợt 1; triển khai chương trình Tiếng Anh tăng cường đến phụ huynh; hoàn thành 100% cập nhật thông tin học sinh lớp chủ nhiệm trên hệ thống CSDL ngành.
- Tích cực vận động học sinh tham gia Đấu trường VioEdu, triển khai thư viện số; phối hợp trợ giảng trong các tiết Tiếng Anh giao tiếp với giáo viên nước ngoài (2 tiết/tuần theo năng lực) bảo đảm hiệu quả.

### **2. Ngày giờ công và kỷ luật lao động:**
- Giáo viên trong tổ đảm bảo ngày giờ công nghiêm túc, tham gia đầy đủ các hoạt động hội họp của nhà trường, dạy đủ số tiết theo phân công chuyên môn; thực hiện chu đáo việc dạy bù, dạy thay khi có giáo viên đi công tác hoặc nghỉ ốm.

### **3. Công tác chuyên môn và thực hiện quy chế:**
- Ổn định nền nếp dạy và học theo đúng thời khóa biểu; thực hiện chương trình theo kế hoạch giáo dục nhà trường, dạy học 2 buổi/ngày theo Công văn 4567 của Bộ GD&ĐT, dạy học giáo dục địa phương, GDNGLL và HĐTN đúng định hướng.
- **Về hồ sơ sổ sách và Kế hoạch bài dạy (KHBD):**
  - *Ưu điểm:* Đa số giáo viên trong tổ đã có ý thức chuẩn bị hồ sơ bài dạy đầy đủ theo phân phối chương trình, bảo đảm cấu trúc 4 hoạt động theo tinh thần Công văn 5512/BGDĐT-GDTrH.
  - *Tồn tại, hạn chế cần khắc phục ngay:* Qua đợt kiểm tra hồ sơ bài dạy tháng 9, một số giáo viên thực hiện chưa đúng biểu mẫu quy định. Cụ thể: Kế hoạch bài dạy còn mắc lỗi định dạng công thức toán học, biến dạng ký hiệu góc hình học; các chỉ báo năng lực số (NLS) và trí tuệ nhân tạo (AI) chưa được định dạng in đậm, in nghiêng theo quy định; một số bài soạn chưa đồng bộ Header/Footer theo mẫu chung của nhà trường. Yêu cầu các thầy cô khẩn trương rà soát, chỉnh sửa hoàn thiện trước đợt kiểm tra tiếp theo.
- **Về nền nếp giảng dạy và thực hiện quy chế chuyên môn:**
  - Chấp hành nghiêm túc quy chế chuyên môn, lên lớp đúng giờ, quản lý học sinh tốt trong các tiết học; tuyệt đối không tự ý đổi tiết, bỏ tiết khi chưa có sự phê duyệt của Tổ trưởng và Ban Giám hiệu.
  - Thực hiện ghi chép Sổ đầu bài đầy đủ, sạch sẽ, khớp 100% với tiến độ phân phối chương trình và Kế hoạch giáo dục của tổ (Phụ lục 3).
  - Công tác kiểm tra đánh giá thường xuyên: Giáo viên các bộ môn đã chủ động kiểm tra theo tiến độ, vào điểm và cập nhật kịp thời trên phần mềm quản lý điểm của trường.
  - Nề nếp phòng học bộ môn: Giáo viên Tin học duy trì nền nếp phòng máy vi tính nghiêm túc, hướng dẫn học sinh thực hiện đúng nội quy phòng máy, bảo đảm an toàn thiết bị điện và bảo quản máy móc phục vụ giảng dạy.

### **Kết quả xếp loại hồ sơ chuyên môn tháng 9/2026:**
| STT | Họ và tên giáo viên | Môn giảng dạy | Số tiết nộp | Xếp loại tháng 9 |
|:---:|:---|:---|:---:|:---:|
| 1 | Hoàng Tấn Thiên | Toán 9, Tin học 6 | Đầy đủ | **Tốt** |
| 2 | Hồ Đăng Danh | Toán 6, Toán 9 | Đầy đủ | **Tốt** |
| 3 | Trần Sáng | Toán 6, Toán 9 | Đầy đủ | **Tốt** |
| 4 | Trần Long Hải | Toán 8 | Đầy đủ | **Khá** |
| 5 | Nguyễn Thị Thảo | Toán 6, Toán 7 | Đầy đủ | **Khá** |
| 6 | Lê Thị Bình | Toán 7, Toán 8, HĐTN | Đầy đủ | **Khá** |
| 7 | Hoàng Xuân Ánh | Toán 7, HĐTN 6 | Đầy đủ | **Khá** |
| 8 | Nguyễn Văn Tính | HĐTN 7 | Đầy đủ | **Khá** |
| 9 | Đinh Văn Đông | Toán 8 | Đầy đủ | **Khá** |
| 10 | Dương Quang Tùng | Tin học 6, 7, 8, 9 | Đầy đủ | **Tốt** |

- **Tổng hợp số lượng học sinh tham gia thi Đấu trường VioEdu vòng sơ loại 1:** Toàn trường có **107 học sinh** tham gia dự thi. Cụ thể từng khối: Khối 6: 30 học sinh; Khối 7: 24 học sinh; Khối 8: 31 học sinh; Khối 9: 22 học sinh.

### **4. Công tác chuyên đề, thao giảng:**
- Tham gia đầy đủ các buổi tập huấn chuyên môn, chuyên đề do Sở GD&ĐT tổ chức; phổ biến lại trong nhóm bộ môn để triển khai thống nhất.

### **5. Công tác ngoại khóa và phong trào:**
- Đã thực hiện tốt hoạt động GDNGLL theo chủ điểm: Tổ chức Tết Trung thu vui tươi, an toàn cho học sinh; tuyên truyền học sinh chấp hành tốt nội quy trường lớp, tham gia các cuộc thi do Nhà trường và Đoàn - Đội phát động.

### **6. Công tác kiểm tra nội bộ:**
- Kiểm tra nền nếp ra vào lớp, việc thực hiện quy chế chuyên môn, chất lượng soạn giảng và tiến độ thực hiện chương trình.

### **7. Sử dụng thiết bị dạy học và phòng bộ môn:**
- Giáo viên trong tổ sử dụng có hiệu quả phòng thực hành Tin học, phòng học chức năng, khai thác triệt để các phần mềm dạy học phục vụ bài giảng.

### **8. Công tác khác:**
- Tích cực tham gia các phong trào thi đua của Đoàn – Đội, tham gia đầy đủ công tác điều tra phổ cập giáo dục theo phân công của xã.

---

## III. KẾ HOẠCH HOẠT ĐỘNG CHUYÊN MÔN THÁNG 10/2026

### **1. Công tác chủ nhiệm:**
- Ổn định nền nếp lớp chủ nhiệm, tích cực sinh hoạt 15 phút đầu giờ. Phát động đợt thi đua cao điểm chào mừng các ngày lễ lớn trong tháng: Ngày Quốc tế Người cao tuổi (01/10), Ngày Khuyến học Việt Nam (02/10), Ngày Bác Hồ gửi bức thư cuối cùng cho ngành Giáo dục (15/10) và Ngày Phụ nữ Việt Nam (20/10). Tuyên truyền phòng chống ma túy, tội phạm, ATGT, PCCC và phòng tránh tai nạn thương tích.
- Thực hiện hiệu quả Tuần lễ học tập suốt đời năm 2026; hoàn thành hồ sơ sổ sách GVCN đúng quy định; tiếp tục rà soát học sinh khó khăn; đôn đốc thu nộp BHYT, BHTN; thông tin thường xuyên qua Zalo lớp.
- Vận động học sinh đăng ký thi VioEdu các vòng tiếp theo; triển khai thư viện số và tiết học thư viện theo thời khóa biểu. Giáo viên bộ môn tích hợp bài dạy STEM (Phụ lục 2) vào Kế hoạch bài dạy theo thời điểm, hướng dẫn học sinh nộp sản phẩm tại phòng STEM.

### **2. Đảm bảo ngày giờ công và nền nếp chuyên môn:**
- Giáo viên phấn đấu đảm bảo nghiêm túc ngày giờ công, tham gia đầy đủ hoạt động của trường; dạy đúng, dạy đủ số tiết theo phân công chuyên môn; thực hiện kịp thời việc dạy bù, dạy thay khi có phân công.

### **3. Công tác chuyên môn trọng tâm:**

**a) Chuẩn bị công tác kiểm tra nội bộ nhà trường (Thanh tra toàn diện):**
- Đối tượng kiểm tra: Thầy **Trần Sáng** (thực hiện theo Kế hoạch kiểm tra nội bộ năm học 2026 - 2027 của Trường THCS Trần Phú).
- Yêu cầu chuẩn bị: Thầy Sáng chuẩn bị chu đáo toàn bộ hồ sơ chuyên môn cá nhân (Kế hoạch bài dạy chuẩn CV 5512, sổ theo dõi và đánh giá học sinh, kế hoạch dạy học cá nhân, thiết bị và đồ dùng dạy học).
- Phân công phối hợp: Thầy Sáng chủ động gửi Thời khóa biểu và lịch dạy trong tuần cho Tổ trưởng để tổ sắp xếp báo cáo Ban Giám hiệu, đồng thời phân công giáo viên trong tổ bố trí dự giờ, đóng góp ý kiến mang tính xây dựng chuyên môn.

**b) Kế hoạch Chuyên đề Ngoại khóa “Rung chuông vàng” môn Toán khối 6:**
- Nhằm tạo sân chơi học tập bổ ích, khơi dậy niềm đam mê học Toán và nâng cao kỹ năng vận dụng kiến thức thực tế cho học sinh khối 6, Tổ Toán – Tin thống nhất thành lập Ban Tổ chức và xây dựng tiến độ triển khai:
  - *Nhóm biên soạn nội dung và ngân hàng đề:* Cô Nguyễn Thị Thảo (Chủ đạo, phụ trách khối 6); Cô Lê Thị Bình (Hỗ trợ xây dựng và rà soát câu hỏi).
  - *Nhóm tư vấn và thẩm định chuyên môn:* Thầy Hoàng Tấn Thiên (Trưởng ban), Thầy Hồ Đăng Danh, Thầy Nguyễn Văn Tính, Thầy Đinh Văn Đông.
  - *Nhóm hỗ trợ tổ chức và kỹ thuật - hậu cần:* Thầy Hoàng Xuân Ánh, Thầy Trần Long Hải, Thầy Dương Quang Tùng, Thầy Trần Sáng (chuẩn bị âm thanh, máy chiếu, bảng con, sân bãi).
- **Lịch trình và tiến độ thực hiện chi tiết (Thực hiện trong tháng 11/2026):**

| Thời gian | Nội dung công việc | Người phụ trách | Ghi chú / Sản phẩm |
|:---|:---|:---|:---|
| **08/10 – 15/10/2026** | Xây dựng khung thể lệ; biên soạn bộ ngân hàng 35 câu hỏi Toán 6 (30 câu chính, 5 câu phụ; tích hợp câu hỏi thực tiễn và Tiếng Anh Toán học). | Cô Thảo, Cô Bình | Bản thảo đề & đáp án |
| **16/10 – 22/10/2026** | Họp nhóm tư vấn thẩm định câu hỏi; Tổ trưởng hoàn thiện kế hoạch chi tiết trình BGH phê duyệt; Cô Thảo xem lịch chọn ngày cụ thể. | Thầy Thiên, Thầy Danh, Thầy Tính, Thầy Đông, Cô Thảo | Kế hoạch được BGH duyệt |
| **23/10 – 31/10/2026** | Thông báo thể lệ đến các lớp khối 6; các lớp lập danh sách học sinh tham gia (15 HS/lớp); nhóm hỗ trợ chuẩn bị bảng con, phấn, chuông, sân bãi. | Cô Thảo, Thầy Ánh, Thầy Hải, Thầy Tùng, Thầy Sáng | Danh sách thí sinh & CSVC |
| **01/11 – 07/11/2026** | Chạy thử chương trình, kiểm tra hệ thống âm thanh, máy chiếu trình chiếu câu hỏi; phân công dẫn chương trình (MC) và cứu trợ. | Toàn thể thành viên Ban Tổ chức | Hoàn tất chuẩn bị |
| **Tuần 2 Tháng 11/2026**<br>*(Dự kiến 14/11/2026)* | Tổ chức chính thức Chuyên đề Ngoại khóa “Rung chuông vàng môn Toán khối 6” chào mừng kỷ niệm Ngày Nhà giáo Việt Nam 20/11. | Tổ Toán – Tin phối hợp Đoàn - Đội | Tổng kết, trao thưởng |

**c) Công tác xây dựng Ma trận, Bản đặc tả, Đề cương và Đề kiểm tra giữa học kỳ 1:**
- Toàn tổ thực hiện nghiêm túc Công văn số 5529/SGDĐT-GDPT&GDTX của Sở GD&ĐT thành phố Đồng Nai về tổ chức kiểm tra, đánh giá định kỳ.
- **Yêu cầu chuyên môn:** Ma trận và bản đặc tả phải bám sát nội dung chương trình GDPT 2018, bảo đảm đúng tỉ lệ 4 mức độ nhận thức (Nhận biết 40%, Thông hiểu 30%, Vận dụng 20%, Vận dụng cao 10%). Đề kiểm tra phải bám sát ma trận và đề cương ôn tập, có tính phân hóa phù hợp với đối tượng học sinh.
- **Phân công phụ trách:** Môn Toán khối 6 do Cô Nguyễn Thị Thảo phụ trách; Môn Toán khối 7 do Thầy Hoàng Xuân Ánh phụ trách; Môn Toán khối 8 do Cô Lê Thị Bình phụ trách; Môn Toán khối 9 do Thầy Trần Sáng phụ trách; Môn Tin học (Khối 6, 7, 8, 9) do Thầy Dương Quang Tùng phụ trách.
- **Hình thức và thời lượng:**
  - Môn Toán (Khối 6, 7, 8, 9): Thời gian làm bài 60 phút; hình thức: 100% Tự luận làm trên giấy thi theo đúng hướng dẫn kiểm tra định kỳ.
  - Môn Tin học (Khối 6, 7, 8, 9): Thời gian làm bài 45 phút; hình thức: Kiểm tra trực tuyến trên phòng máy vi tính thông qua nền tảng OLM (đảm bảo tính khách quan, tự động trộn đề và chấm điểm).
- **Tiến độ và các mốc thời gian thực hiện bắt buộc:**
  - **Ngày 15/10/2026:** Hạn chót nộp Ma trận, Bản đặc tả và Đề cương ôn tập về Tổ trưởng chuyên môn thẩm định và duyệt.
  - **Ngày 24/10/2026:** Hạn chót nộp Đề kiểm tra giữa kỳ (kèm hướng dẫn chấm/thang điểm) và hoàn thành công tác phản biện chéo giữa các giáo viên trong nhóm bộ môn.
  - **Ngày 28/10/2026:** Tổ trưởng chuyên môn tổng hợp, thẩm định lần cuối và chính thức nộp toàn bộ Đề thi giữa kỳ về bộ phận Chuyên môn nhà trường (Ban Giám hiệu) để chuẩn bị công tác in sao và tổ chức kiểm tra theo kế hoạch.

**d) Kế hoạch Sinh hoạt chuyên môn theo Nghiên cứu bài học (NCBH) trong tháng 11/2026:**
- Thống nhất chuyển trọng tâm NCBH từ khối 6 sang khối 8 và khối 9 trong tháng 11/2026 (sau kỳ kiểm tra giữa kỳ 1):
  - *Bài học trọng tâm lựa chọn:* Môn Toán lớp 8 – Bài “Định lí Thalès trong tam giác” (Chương Định lí Thalès, bộ sách GDPT 2018).
  - *Chuyên đề định hướng nâng cao lớp 9:* Nhóm giáo viên dạy Toán 9 (Thầy Thiên, Thầy Danh, Thầy Sáng) chuẩn bị chuyên đề “Đổi mới phương pháp dạy học Hàm số bậc nhất và Rèn kỹ năng giải toán thực tế cho học sinh lớp 9 ôn thi Tuyển sinh 10”.
  - *Lý do lựa chọn bài Định lí Thalès (Lớp 8):* Bài học nền tảng hình học 8; khả năng ứng dụng thực tế và giáo dục STEM rất cao (đo bóng mặt trời xác định chiều cao cột cờ, cây xanh); rất thuận lợi ứng dụng Năng lực số với phần mềm hình học động GeoGebra.
  - *Phân công thực hiện:* Cô Lê Thị Bình (phụ trách chính khối 8) chủ trì xây dựng Kế hoạch bài dạy minh họa; Thầy Trần Long Hải và Thầy Nguyễn Văn Tính phối hợp hỗ trợ thiết kế phiếu học tập, chuẩn bị dụng cụ đo đạc thực hành (thước dây, giác kế mini). Thời gian dạy thể nghiệm dự kiến vào Tuần 1 hoặc Tuần 2 Tháng 11/2026.

**e) Góp ý chuyên sâu chương trình Sách giáo khoa GDPT 2018 môn Toán - Tin:**
- **Đại số 9:** Trong bài kiểm tra, phần giải bài toán bằng cách lập hệ phương trình, trong quá trình làm bài học sinh được phép sử dụng máy tính cầm tay để bấm nghiệm kiểm tra kết quả và ghi bước kết luận theo đúng tinh thần giảm tải tính toán cơ học.
- **Hình học 9:** Các hệ thức lượng trong tam giác vuông (như trong SGK cũ) không được áp dụng trực tiếp như định lý sẵn có để làm bài tập; nếu học sinh sử dụng trong bài thi thì bắt buộc phải chứng minh lại bằng tam giác đồng dạng, tuân thủ đúng kết luận thống nhất của Hội đồng bộ môn cấp tỉnh.

### **4. Công tác chuyên đề và bồi dưỡng:**
- Phát động phong trào thi đua chào mừng ngày Phụ nữ Việt Nam 20/10: Mỗi giáo viên trong tổ đăng ký ít nhất 01 tiết dạy tốt, tăng cường ứng dụng công nghệ thông tin và chuyển đổi số trong giảng dạy.
- Chuẩn bị chu đáo công tác bồi dưỡng học sinh giỏi khối 8, 9 theo đúng tinh thần Kế hoạch số 4706/KH-SGDĐT của Sở GD&ĐT; lập danh sách học sinh cần hỗ trợ để phụ đạo kịp thời.
- Tiếp tục quán triệt thực hiện nghiêm túc quy định về dạy thêm, học thêm (Quyết định số 25/2025/QĐ-UBND, Quyết định số 59/2026/QĐ-UBND, Văn bản hợp nhất số 01/2026/VBHN-QĐ-UBND và Công văn 5473/SGDĐT-GDPT&GDTX); tuyệt đối không vi phạm đạo đức nhà giáo.

---

## IV. Ý KIẾN THẢO LUẬN VÀ GIẢI PHÁP CHUYÊN MÔN THỰC CHIẾN

Phiên họp diễn ra sôi nổi, thẳng thắn, phản ánh đúng thực tế lớp học và đề xuất các giải pháp kỹ thuật cụ thể:

- **Cô Lê Thị Bình (Giáo viên môn Toán 8, Thư ký):** Qua theo dõi vòng 1 Đấu trường VioEdu, còn một số học sinh ở các lớp bỏ thi hoặc điểm đạt được chưa cao. Đề nghị các thầy cô giáo viên phụ trách khối cần chủ động phối hợp chặt chẽ với giáo viên chủ nhiệm để nhắc nhở các em vào thi trước khi hệ thống tự động khóa vòng vào 23h59 Chủ nhật hàng tuần. Về nhiệm vụ dạy minh họa Nghiên cứu bài học bài “Định lí Thalès trong tam giác”, tôi nhất trí nhận nhiệm vụ và sẽ kết hợp hoạt động đo đạc thực tế ngoài sân trường với mô phỏng GeoGebra; cam kết nộp đề cương Toán 8 giữa kỳ đúng hạn 15/10/2026.

- **Thầy Trần Long Hải (Giáo viên môn Toán 8):** Đề nghị Ban Thi đua nhà trường phổ biến rõ ràng, cụ thể tiêu chí chấm điểm thi đua cho đội cờ đỏ/sao đỏ các lớp để bảo đảm chấm điểm đồng đều, khách quan giữa các lớp (hiện nay đang có sự chênh lệch cách chấm giữa học sinh học ở Cơ sở 1 và Cơ sở 2). Đồng thời, Thầy Hải cam kết sẽ phối hợp cùng Thầy Tính hỗ trợ cô Bình thiết kế phiếu học tập và chuẩn bị dụng cụ đo đạc thực hành cho tiết dạy minh họa Thalès.

- **Thầy Hoàng Xuân Ánh (Giáo viên môn Toán 7, Phụ trách VioEdu K7):** Hoàn toàn nhất trí với phần đánh giá và kế hoạch hoạt động của tổ chuyên môn. Nhóm Toán 7 sẽ tập trung bám sát chuẩn kiến thức kỹ năng để xây dựng ma trận và đề cương kiểm tra giữa kỳ 1 có tính phân hóa phù hợp với học sinh khối 7, bảo đảm nộp đúng hạn 15/10/2026.

- **Cô Nguyễn Thị Thảo (Giáo viên môn Toán 6, Phụ trách VioEdu K6):** Cảm ơn tổ chuyên môn đã đồng thuận chuyển nhiệm vụ Nghiên cứu bài học sang khối 8, tạo điều kiện thuận lợi cho nhóm Toán 6 tập trung toàn lực xây dựng bộ ngân hàng 35 câu hỏi và kịch bản chi tiết cho Chuyên đề Ngoại khóa “Rung chuông vàng môn Toán khối 6” chào mừng ngày 20/11; cam kết hoàn thành dự thảo ngân hàng câu hỏi trước ngày 15/10/2026.

- **Thầy Trần Sáng (Giáo viên môn Toán 9, KTNB):** Tiếp thu toàn diện kế hoạch kiểm tra nội bộ của nhà trường; Thầy Sáng cam kết hoàn thiện hồ sơ Kế hoạch bài dạy chuẩn Công văn 5512, tích hợp chỉ báo Năng lực số và AI in đậm, in nghiêng rõ nét theo đúng kết luận rút kinh nghiệm của tổ; chủ động gửi lịch dạy trong tuần cho Tổ trưởng để tổ sắp xếp dự giờ. Về ma trận và đề kiểm tra Toán 9, Thầy Sáng đảm bảo bám sát cấu trúc đề thi tuyển sinh 10, nộp đúng tiến độ (ma trận ngày 15/10, đề kiểm tra ngày 24/10) để tổ phản biện chéo.

- **Thầy Dương Quang Tùng (Giáo viên Tin học, Phụ trách phòng máy):** Báo cáo tình hình chuẩn bị cho kỳ kiểm tra giữa kỳ môn Tin học: 2 phòng máy tính (45 máy) đã được kiểm tra đường truyền và cài đặt ổn định; sẵn sàng tổ chức cho học sinh làm bài kiểm tra trực tuyến 100% trên nền tảng OLM theo đúng thời lượng 45 phút. Thầy Tùng cũng sẽ hỗ trợ kỹ thuật âm thanh, máy chiếu và trình chiếu câu hỏi cho sân chơi Rung chuông vàng khối 6.

---

## V. KẾT LUẬN CỦA CHỦ TỌA VÀ NGHỊ QUYẾT CUỘC HỌP

Thầy Tổ trưởng chuyên môn Hoàng Tấn Thiên kết luận toàn diện phiên họp và chỉ đạo thực hiện các nhiệm vụ trọng tâm sau:

1. Toàn thể giáo viên trong tổ thực hiện chuẩn xác 03 mốc thời gian kiểm tra giữa kỳ 1:
   - **Ngày 15/10/2026:** Nộp Ma trận, Bản đặc tả và Đề cương ôn tập về Tổ trưởng duyệt.
   - **Ngày 24/10/2026:** Nộp Đề kiểm tra giữa kỳ và hoàn tất phản biện chéo trong nhóm.
   - **Ngày 28/10/2026:** Tổ trưởng chính thức nộp toàn bộ đề thi về Ban Giám hiệu để in sao.
2. Yêu cầu 100% giáo viên khẩn trương rà soát, chỉnh sửa ngay các tồn tại về hồ sơ bài dạy: Khắc phục lỗi công thức toán, sửa ký hiệu góc hình học, định dạng in đậm và in nghiêng các chỉ báo Năng lực số (NLS), AI, đồng bộ Header/Footer theo mẫu chung.
3. Phối hợp chuẩn bị chu đáo công tác kiểm tra nội bộ toàn diện đối với Thầy Trần Sáng; đẩy mạnh xây dựng ngân hàng đề Rung chuông vàng khối 6; nhóm Toán 8 khẩn trương hoàn thiện Kế hoạch bài dạy minh họa bài “Định lí Thalès trong tam giác” tích hợp GeoGebra và thực hành STEM.
4. Giáo viên phụ trách các khối tiếp tục đôn đốc học sinh tham gia đầy đủ các vòng thi Đấu trường VioEdu; GVCN phối hợp quản lý tốt các tiết Tiếng Anh giao tiếp với giáo viên nước ngoài.
5. Chấp hành nghiêm túc quy định pháp luật về dạy thêm, học thêm; tuyệt đối không vi phạm đạo đức nhà giáo.

- **Biểu quyết:** 10/10 thành viên trong tổ (100% giáo viên) nhất trí hoàn toàn với nội dung cuộc họp.
- Biên bản kết thúc vào lúc 10 giờ 00 phút cùng ngày./.

---

<table style="width: 100%; border: none;">
<tr>
<td style="width: 50%; text-align: center; vertical-align: top;">
<strong>THƯ KÝ CUỘC HỌP</strong><br>
<em>(Ký và ghi rõ họ tên)</em><br><br><br><br>
<strong>Lê Thị Bình</strong>
</td>
<td style="width: 50%; text-align: center; vertical-align: top;">
<strong>TỔ TRƯỞNG CHUYÊN MÔN</strong><br>
<em>(Ký và ghi rõ họ tên)</em><br><br><br><br>
<strong>Hoàng Tấn Thiên</strong>
</td>
</tr>
</table>

<div align="center">

### CÁC THÀNH VIÊN TRONG TỔ KÝ TÊN XÁC NHẬN

</div>

| Đinh Văn Đông | Hồ Đăng Danh | Hoàng Xuân Ánh | Trần Long Hải |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |

| Nguyễn Văn Tính | Dương Quang Tùng | Trần Sáng | Nguyễn Thị Thảo |
|:---:|:---:|:---:|:---:|
| *(Ký tên)* | *(Ký tên)* | *(Ký tên)* | *(Ký tên)* |
"""
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
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
    parser.add_argument("--loai", type=str, default="tat_ca", choices=["bien_ban_1_8", "bien_ban_1_9", "bien_ban_2_9", "bien_ban_1_10", "bien_ban_2_10", "bao_cao_thang_10", "ktnb_bien_ban", "ktnb_bao_cao", "ktnb", "tat_ca"], help="Loại văn bản cần xuất")
    parser.add_argument("--out-dir", type=str, default="c:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/22.10", help="Thư mục kết quả")
    args = parser.parse_args()
    
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    root_ket_qua = Path("c:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua")
    root_ket_qua.mkdir(parents=True, exist_ok=True)
    import shutil
    
    # Chức năng 1: Biên bản họp tổ lần 1 tháng 8 (Đầu năm học 2026 - 2027)
    if args.loai in ("bien_ban_1_8", "tat_ca"):
        docx_file_bb1 = out_dir / "Bien_Ban_Hop_To_Lan_1_Thang_8_2026.docx"
        md_file_bb1 = out_dir / "Bien_Ban_Hop_To_Lan_1_Thang_8_2026.md"
        tao_bien_ban_hop_to_lan_1_thang_8(str(docx_file_bb1), str(md_file_bb1))
        safe_copy2(docx_file_bb1, root_ket_qua / "Bien_Ban_Hop_To_Lan_1_Thang_8_2026.docx")
        safe_copy2(md_file_bb1, root_ket_qua / "Bien_Ban_Hop_To_Lan_1_Thang_8_2026.md")
        print(f"Da dong bo Bien ban hop to thang 8 vao: {root_ket_qua / 'Bien_Ban_Hop_To_Lan_1_Thang_8_2026.docx'}")

    # Chức năng 1B: Biên bản họp tổ lần 1 tháng 9 (Công văn 5512 & Tích hợp NLS, AI)
    if args.loai in ("bien_ban_1_9", "tat_ca"):
        docx_file_bb9 = out_dir / "Bien_Ban_Hop_To_Lan_1_Thang_9_2026.docx"
        md_file_bb9 = out_dir / "Bien_Ban_Hop_To_Lan_1_Thang_9_2026.md"
        tao_bien_ban_hop_to_lan_1_thang_9(str(docx_file_bb9), str(md_file_bb9))
        safe_copy2(docx_file_bb9, root_ket_qua / "Bien_Ban_Hop_To_Lan_1_Thang_9_2026.docx")
        safe_copy2(md_file_bb9, root_ket_qua / "Bien_Ban_Hop_To_Lan_1_Thang_9_2026.md")
        print(f"Da dong bo Bien ban hop to thang 9 vao: {root_ket_qua / 'Bien_Ban_Hop_To_Lan_1_Thang_9_2026.docx'}")

    # Chức năng 1C: Biên bản họp tổ lần 2 tháng 9 (HD 5351 Quản lý ĐT & KH 5264 CĐS, AI)
    if args.loai in ("bien_ban_2_9", "tat_ca"):
        docx_file_bb9_2 = out_dir / "Bien_Ban_Hop_To_Lan_2_Thang_9_2026.docx"
        md_file_bb9_2 = out_dir / "Bien_Ban_Hop_To_Lan_2_Thang_9_2026.md"
        tao_bien_ban_hop_to_lan_2_thang_9(str(docx_file_bb9_2), str(md_file_bb9_2))
        safe_copy2(docx_file_bb9_2, root_ket_qua / "Bien_Ban_Hop_To_Lan_2_Thang_9_2026.docx")
        safe_copy2(md_file_bb9_2, root_ket_qua / "Bien_Ban_Hop_To_Lan_2_Thang_9_2026.md")
        print(f"Da dong bo Bien ban hop to thang 9 lan 2 vao: {root_ket_qua / 'Bien_Ban_Hop_To_Lan_2_Thang_9_2026.docx'}")

    # Chức năng 1D: Biên bản họp tổ lần 1 tháng 10 (Kiểm tra giữa kỳ, Rung chuông vàng K6, Đề án TA)
    if args.loai in ("bien_ban_1_10", "tat_ca"):
        docx_file_bb10_1 = out_dir / "Bien_Ban_Hop_To_Lan_1_Thang_10_2026.docx"
        md_file_bb10_1 = out_dir / "Bien_Ban_Hop_To_Lan_1_Thang_10_2026.md"
        tao_bien_ban_hop_to_lan_1_thang_10(str(docx_file_bb10_1), str(md_file_bb10_1))
        safe_copy2(docx_file_bb10_1, root_ket_qua / "Bien_Ban_Hop_To_Lan_1_Thang_10_2026.docx")
        safe_copy2(md_file_bb10_1, root_ket_qua / "Bien_Ban_Hop_To_Lan_1_Thang_10_2026.md")
        safe_copy2(docx_file_bb10_1, root_ket_qua / "Noi_Dung_Hop_To_Lan_1_Thang_10_2026.docx")
        safe_copy2(md_file_bb10_1, root_ket_qua / "Noi_Dung_Hop_To_Lan_1_Thang_10_2026.md")
        print(f"Da dong bo Bien ban hop to thang 10 lan 1 vao: {root_ket_qua / 'Bien_Ban_Hop_To_Lan_1_Thang_10_2026.docx'}")

    # Chức năng 1E: Biên bản họp tổ lần 2 tháng 10
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




