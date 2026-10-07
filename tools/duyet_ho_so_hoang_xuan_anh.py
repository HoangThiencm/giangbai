# -*- coding: utf-8 -*-
"""
THẨM ĐỊNH VÀ DUYỆT HỒ SƠ BÀI DẠY — THẦY HOÀNG XUÂN ÁNH (TOÁN 7, HĐTN 6)
Chuẩn hóa 100% thể thức văn bản hành chính theo Nghị định 30/2020/NĐ-CP
- Phông chữ: Times New Roman
- Cỡ chữ nội dung: Đồng nhất 13pt
- Thụt đầu dòng: 1.27 cm (0.5 inch)
- Căn lề: JUSTIFY
- Dãn dòng: 1.2 line
- Lề trang A4: Top 20mm, Bottom 20mm, Left 30mm, Right 15mm
- Bảng biểu: Đóng khung kín 4 cạnh
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# HELPER FUNCTIONS ĐỊNH DẠNG NGHỊ ĐỊNH 30/2020/NĐ-CP
# ==============================================================================

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_table_borders_nd30(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_callout_border(cell, border_color="16A34A", bg_color="F0FDF4"):
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=140)
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

def apply_page_setup_nd30(doc):
    for s in doc.sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(0.79)      # 20 mm
        s.bottom_margin = Inches(0.79)   # 20 mm
        s.left_margin = Inches(1.18)     # 30 mm
        s.right_margin = Inches(0.59)    # 15 mm
        s.different_first_page_header_footer = False

def safe_save_doc(doc, target_path):
    try:
        doc.save(target_path)
        print("Đã lưu thành công:", target_path)
        return target_path
    except PermissionError:
        base, ext = os.path.splitext(target_path)
        fallback_path = f"{base}_CapNhat{ext}"
        doc.save(fallback_path)
        print(f"Tệp đang mở. Đã lưu sang: {fallback_path}")
        return fallback_path

# ==============================================================================
# 1. TẠO PHIẾU NHẬN XÉT CÁ NHÂN: HOÀNG XUÂN ÁNH (07/PĐG-TT)
# ==============================================================================
def create_phieu_nhan_xet_anh():
    print("\n--- BẮT ĐẦU TẠO PHIẾU NHẬN XÉT THẦY HOÀNG XUÂN ÁNH ---")
    doc = docx.Document()
    apply_page_setup_nd30(doc)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)

    # 1. Quốc hiệu tiêu ngữ (Table 0)
    tbl_h = doc.add_table(rows=1, cols=2)
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl_h.cell(0, 0)
    c1 = tbl_h.cell(0, 1)
    set_cell_margins(c0, 0, 0, 0, 0)
    set_cell_margins(c1, 0, 0, 0, 0)

    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0); p0.paragraph_format.space_after = Pt(0)
    p0.paragraph_format.line_spacing = 1.15
    r = p0.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12)
    r = p0.add_run("TỔ TOÁN – TIN\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
    r = p0.add_run("———————\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(10)
    r = p0.add_run("Số: 07/PĐG-TT")
    r.font.name = "Times New Roman"; r.font.size = Pt(12)

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(0); p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.line_spacing = 1.15
    r = p1.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
    r = p1.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(13); r.bold = True
    r = p1.add_run("—————————————\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(10)
    r = p1.add_run("Xuân Đông, ngày 30 tháng 9 năm 2026")
    r.font.name = "Times New Roman"; r.font.size = Pt(13); r.italic = True

    # 2. Tiêu đề phiếu
    p_t0 = doc.add_paragraph()
    p_t0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t0.paragraph_format.space_before = Pt(14); p_t0.paragraph_format.space_after = Pt(2)
    r_t0 = p_t0.add_run("PHIẾU NHẬN XÉT, ĐÁNH GIÁ HỒ SƠ BÀI DẠY")
    r_t0.font.name = "Times New Roman"; r_t0.font.size = Pt(14); r_t0.bold = True

    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(0); p_t1.paragraph_format.space_after = Pt(12)
    r_t1 = p_t1.add_run("(ĐỢT THÁNG 9/2026 — NĂM HỌC 2026 - 2027)")
    r_t1.font.name = "Times New Roman"; r_t1.font.size = Pt(13); r_t1.italic = True

    # 3. Thông tin giáo viên
    info_items = [
        ("Họ và tên giáo viên: ", "HOÀNG XUÂN ÁNH", True),
        ("Tổ chuyên môn: ", "Toán – Tin, Trường THCS Trần Phú", False),
        ("Nhiệm vụ giảng dạy: ", "Toán 7 (Đại số 7, Hình học 7) và HĐTN 6", False),
        ("Tổng số hồ sơ nộp: ", "03 phân môn (80 trang PDF, 29 tiết)", False),
    ]

    for label, val, is_val_bold in info_items:
        p_i = doc.add_paragraph()
        p_i.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_i.paragraph_format.first_line_indent = Inches(0.5)
        p_i.paragraph_format.space_before = Pt(2)
        p_i.paragraph_format.space_after = Pt(2 if label != "Tổng số hồ sơ nộp: " else 6)
        p_i.paragraph_format.line_spacing = 1.2
        r_lbl = p_i.add_run(label)
        r_lbl.font.name = "Times New Roman"; r_lbl.font.size = Pt(13); r_lbl.bold = True
        r_val = p_i.add_run(val)
        r_val.font.name = "Times New Roman"; r_val.font.size = Pt(13); r_val.bold = is_val_bold

    # 4. Mục I. KẾT QUẢ THẨM ĐỊNH CHI TIẾT THEO TỪNG PHÂN MÔN
    p_sec1 = doc.add_paragraph()
    p_sec1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sec1.paragraph_format.space_before = Pt(8); p_sec1.paragraph_format.space_after = Pt(4)
    p_sec1.paragraph_format.line_spacing = 1.2
    r_s1 = p_sec1.add_run("I. KẾT QUẢ THẨM ĐỊNH CHI TIẾT THEO TỪNG PHÂN MÔN")
    r_s1.font.name = "Times New Roman"; r_s1.font.size = Pt(13); r_s1.bold = True

    t_data = doc.add_table(rows=4, cols=5)
    t_data.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders_nd30(t_data, color="000000", sz="4")

    headers = ["Phân môn", "Số trang", "Số tiết", "Tiến độ & Tích hợp NLS / AI", "Đánh giá"]
    col_widths = [Inches(1.2), Inches(0.9), Inches(0.8), Inches(2.7), Inches(1.1)]

    for c_idx, h in enumerate(headers):
        cell = t_data.cell(0, c_idx)
        cell.width = col_widths[c_idx]
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.bold = True

    rows_anh = [
        ("Đại số 7", "31 trang", "09 tiết",
         "Đạt 100% Tháng 9 & vượt tuần 5 (Bài 1, 2, LTC, Bài 3). Phép tính số hữu tỉ và lũy thừa chuẩn xác, 4 hoạt động CV 5512 rõ ràng.",
         "DUYỆT (Tốt)"),
        ("Hình học 7", "31 trang", "08 tiết",
         "Đạt 100% Tháng 9 (Bài 8, 9, LTC, Bài 10). Ký hiệu góc và song song hiển thị dấu mũ góc rõ nét, chuẩn mực, không lỗi font.",
         "DUYỆT (Tốt)"),
        ("HĐTN 6", "18 trang", "12 tiết",
         "Đạt 100% Tháng 9 (Chủ đề 1). Tích hợp NLS (2.2.TC1a) và AI (6.C2.2) đầy đủ, có phiếu học tập số; lưu ý in đậm nghiêng mục tiêu.",
         "DUYỆT (Khá/Tốt)"),
    ]

    for r_idx, row_val in enumerate(rows_anh, start=1):
        for c_idx, val in enumerate(row_val):
            cell = t_data.cell(r_idx, c_idx)
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [1, 2, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"; r.font.size = Pt(10.5)
            if c_idx in [0, 4]:
                r.bold = True

    # 5. Mục II. NHẬN XÉT CHUYÊN MÔN CHI TIẾT
    p_sec2 = doc.add_paragraph()
    p_sec2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sec2.paragraph_format.space_before = Pt(12); p_sec2.paragraph_format.space_after = Pt(4)
    p_sec2.paragraph_format.line_spacing = 1.2
    r_s2 = p_sec2.add_run("II. NHẬN XÉT CHUYÊN MÔN CHI TIẾT")
    r_s2.font.name = "Times New Roman"; r_s2.font.size = Pt(13); r_s2.bold = True

    # Ưu điểm nổi bật
    p_u = doc.add_paragraph()
    p_u.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_u.paragraph_format.first_line_indent = Inches(0.5)
    p_u.paragraph_format.space_before = Pt(2); p_u.paragraph_format.space_after = Pt(3)
    p_u.paragraph_format.line_spacing = 1.2
    r_ulbl = p_u.add_run("1. Ưu điểm nổi bật: ")
    r_ulbl.font.name = "Times New Roman"; r_ulbl.font.size = Pt(13); r_ulbl.bold = True
    r_utxt = p_u.add_run(
        "Hồ sơ bài dạy chuẩn bị chu đáo, nộp đầy đủ 03 phân môn với 29 tiết (80 trang PDF), đảm bảo 100% tiến độ 4 tuần của Tháng 9/2026 và vượt tiến độ sang tuần 5 ở phân môn Đại số 7 (đến hết Bài 3). Cấu trúc giáo án bám sát Công văn số 5512/BGDĐT-GDTrH với đầy đủ 4 hoạt động dạy học rõ ràng. Thể thức văn bản, Header và Footer đúng chuẩn quy định của trường THCS Trần Phú. Kiến thức bộ môn Toán 7 chính xác, logic; đặc biệt tại phân môn Hình học 7, các ký hiệu toán học như dấu mũ góc, hai đường thẳng vuông góc, song song được trình bày rất chuẩn mực, sắc nét, không có hiện tượng lỗi font hay biến dạng ký hiệu. Môn HĐTN 6 thiết kế hoạt động sinh động, có bảng tự đánh giá đồng đẳng và rubric đánh giá sản phẩm số rất khoa học."
    )
    r_utxt.font.name = "Times New Roman"; r_utxt.font.size = Pt(13)

    # Điểm lưu ý
    p_l = doc.add_paragraph()
    p_l.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_l.paragraph_format.first_line_indent = Inches(0.5)
    p_l.paragraph_format.space_before = Pt(2); p_l.paragraph_format.space_after = Pt(3)
    p_l.paragraph_format.line_spacing = 1.2
    r_llbl = p_l.add_run("2. Điểm lưu ý khi lưu hành giảng dạy: ")
    r_llbl.font.name = "Times New Roman"; r_llbl.font.size = Pt(13); r_llbl.bold = True
    r_ltxt = p_l.add_run(
        "Tại phân môn HĐTN 6 (Chủ đề 1), giáo viên đã tích hợp Năng lực số (2.2.TC1a) và Trí tuệ nhân tạo (6.C2.2) rất đúng địa chỉ và có tô màu đỏ nổi bật, tuy nhiên cần bổ sung thêm định dạng in đậm, nghiêng (bold italic) cho các câu mô tả chỉ báo này theo đúng quy chế chuyên môn của nhà trường trước khi lưu hành giảng dạy."
    )
    r_ltxt.font.name = "Times New Roman"; r_ltxt.font.size = Pt(13)

    # Khoảng đệm trước Table 2
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0); p_sp.paragraph_format.space_after = Pt(4)

    # Table 2: Callout kết luận và xếp loại
    tbl_callout = doc.add_table(rows=1, cols=1)
    tbl_callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_call = tbl_callout.cell(0, 0)
    set_callout_border(c_call, border_color="16A34A", bg_color="F0FDF4")

    p_call = c_call.paragraphs[0]
    p_call.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_call.paragraph_format.space_before = Pt(2); p_call.paragraph_format.space_after = Pt(2)
    p_call.paragraph_format.line_spacing = 1.2
    r_clbl = p_call.add_run("👉 KẾT LUẬN & XẾP LOẠI: ")
    r_clbl.font.name = "Times New Roman"; r_clbl.font.size = Pt(13); r_clbl.bold = True
    r_clbl.font.color.rgb = RGBColor(15, 23, 42)
    r_ctxt = p_call.add_run(
        "Hồ sơ bài dạy môn Toán 7 và HĐTN 6 nộp đầy đủ 29 tiết (80 trang PDF), đảm bảo 100% tiến độ Tháng 9 và vượt tuần 5 ở Đại 7. Cấu trúc 4 hoạt động CV 5512 rõ ràng, kiến thức và ký hiệu toán học chuẩn mực. Tích hợp NLS/AI bám sát Phụ lục 3. Tổ chuyên môn thống nhất DUYỆT TOÀN BỘ HỒ SƠ — XẾP LOẠI: TỐT."
    )
    r_ctxt.font.name = "Times New Roman"; r_ctxt.font.size = Pt(13)
    r_ctxt.font.color.rgb = RGBColor(15, 23, 42)

    # Khoảng đệm trước Table 3
    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(4); p_sp2.paragraph_format.space_after = Pt(6)

    # Table 3: Chữ ký 2 bên
    tbl_sign = doc.add_table(rows=1, cols=2)
    tbl_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    cs0 = tbl_sign.cell(0, 0)
    cs1 = tbl_sign.cell(0, 1)
    set_cell_margins(cs0, 60, 0, 0, 0)
    set_cell_margins(cs1, 60, 0, 0, 0)

    ps0 = cs0.paragraphs[0]
    ps0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ps0.paragraph_format.line_spacing = 1.15
    r_s0 = ps0.add_run("GIÁO VIÊN BỘ MÔN\n\n\n\n\n")
    r_s0.font.name = "Times New Roman"; r_s0.font.size = Pt(13); r_s0.bold = True
    r_n0 = ps0.add_run("Hoàng Xuân Ánh")
    r_n0.font.name = "Times New Roman"; r_n0.font.size = Pt(13); r_n0.bold = True

    ps1 = cs1.paragraphs[0]
    ps1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ps1.paragraph_format.line_spacing = 1.15
    r_s1 = ps1.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n\n\n\n\n")
    r_s1.font.name = "Times New Roman"; r_s1.font.size = Pt(13); r_s1.bold = True
    r_n1 = ps1.add_run("Hoàng Tấn Thiên")
    r_n1.font.name = "Times New Roman"; r_n1.font.size = Pt(13); r_n1.bold = True

    out_phieu = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_Hoang_Xuan_Anh_Thang_9.docx"
    safe_save_doc(doc, out_phieu)
    print("HOÀN THÀNH TẠO PHIẾU NHẬN XÉT THẦY HOÀNG XUÂN ÁNH!")

# ==============================================================================
# 2. CẬP NHẬT BIÊN BẢN KIỂM TRA TỔ (Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9)
# ==============================================================================
def update_bien_ban_to():
    print("\n--- BẮT ĐẦU CẬP NHẬT BIÊN BẢN TỔ CHUYÊN MÔN ---")
    docx_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.docx"
    doc = docx.Document(docx_path)

    # 1. Thêm dòng STT 7 vào Bảng III (Table 1)
    t = doc.tables[1]
    has_row7 = any("hoàng xuân ánh" in r.cells[1].text.lower() for r in t.rows)
    if not has_row7:
        row7 = t.add_row()
        cells = row7.cells
        cells[0].text = "7"
        cells[1].text = "HOÀNG XUÂN ÁNH"
        cells[2].text = "Toán 7, HĐTN 6"
        cells[3].text = "29 tiết\n(80 trang)"
        cells[4].text = "Đủ 100% Tháng 9 & vượt Tuần 5 (Đại 7); NLS HĐTN 6 cần in đậm nghiêng"
        cells[5].text = "DUYỆT\n(Xếp loại: Tốt)"

        for ci, c in enumerate(cells):
            set_cell_margins(c, top=80, bottom=80, left=80, right=80)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in [0, 3, 5] else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10.5)
                if ci in [1, 5]:
                    run.bold = True
                if ci == 5:
                    run.font.color.rgb = RGBColor(22, 163, 74)

    # 2. Cập nhật Mục IV: Thêm mục IV.7
    has_sec7 = any("7. Thầy Hoàng Xuân Ánh" in p.text for p in doc.paragraphs)
    if not has_sec7:
        p_v_idx = -1
        for idx, p in enumerate(doc.paragraphs):
            if "V. KẾT LUẬN VÀ KIẾN NGHỊ" in p.text:
                p_v_idx = idx
                break

        if p_v_idx != -1:
            p_v = doc.paragraphs[p_v_idx]

            # Header mục 7
            p_h7 = p_v.insert_paragraph_before()
            p_h7.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_h7.paragraph_format.first_line_indent = Inches(0.5)
            p_h7.paragraph_format.space_before = Pt(4); p_h7.paragraph_format.space_after = Pt(2)
            p_h7.paragraph_format.line_spacing = 1.2
            r = p_h7.add_run("7. Thầy Hoàng Xuân Ánh (Môn Toán 7, HĐTN 6)")
            r.font.name = "Times New Roman"; r.font.size = Pt(13); r.bold = True

            # Đoạn 1: Tiến độ và khối lượng
            p_td = p_v.insert_paragraph_before()
            p_td.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_td.paragraph_format.first_line_indent = Inches(0.5)
            p_td.paragraph_format.space_before = Pt(2); p_td.paragraph_format.space_after = Pt(2)
            p_td.paragraph_format.line_spacing = 1.2
            r1 = p_td.add_run("- Tiến độ và khối lượng: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p_td.add_run("Nộp đầy đủ 03 tệp PDF gồm 80 trang qua 3 phân môn với tổng số 29 tiết dạy: Đại số 7 (9 tiết, 31 tr), Hình học 7 (8 tiết, 31 tr) và HĐTN 6 (12 tiết, 18 tr). Đảm bảo 100% tiến độ 4 tuần Tháng 9/2026 và vượt tiến độ sang tuần 5 ở phân môn Đại số 7 (hết Bài 3).")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

            # Đoạn 2: Ưu điểm nổi bật
            p_ud = p_v.insert_paragraph_before()
            p_ud.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_ud.paragraph_format.first_line_indent = Inches(0.5)
            p_ud.paragraph_format.space_before = Pt(2); p_ud.paragraph_format.space_after = Pt(2)
            p_ud.paragraph_format.line_spacing = 1.2
            r1 = p_ud.add_run("- Ưu điểm nổi bật: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p_ud.add_run("Hồ sơ bài dạy soạn chu đáo, cấu trúc đầy đủ 4 hoạt động theo Công văn số 5512/BGDĐT-GDTrH. Thể thức văn bản, Header/Footer đúng chuẩn quy định của trường THCS Trần Phú. Ký hiệu góc và công thức hình học trong Hình học 7 hiển thị chuẩn mực, rõ nét, không lỗi font. Môn HĐTN 6 tích hợp NLS 2.2.TC1a và AI 6.C2.2 đầy đủ, có phiếu học tập và bảng rubric tự đánh giá rất bài bản.")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

            # Đoạn 3: Tồn tại, lưu ý
            p_lu = p_v.insert_paragraph_before()
            p_lu.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_lu.paragraph_format.first_line_indent = Inches(0.5)
            p_lu.paragraph_format.space_before = Pt(2); p_lu.paragraph_format.space_after = Pt(2)
            p_lu.paragraph_format.line_spacing = 1.2
            r1 = p_lu.add_run("- Điểm cần lưu ý: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p_lu.add_run("Các câu mô tả mục tiêu chỉ báo NLS và AI trong tệp HĐTN 6 cần bổ sung định dạng in đậm, nghiêng theo đúng quy chế chuyên môn trước khi lưu hành giảng dạy.")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

            # Đoạn 4: Kết luận và xếp loại
            p_kl = p_v.insert_paragraph_before()
            p_kl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_kl.paragraph_format.first_line_indent = Inches(0.5)
            p_kl.paragraph_format.space_before = Pt(2); p_kl.paragraph_format.space_after = Pt(6)
            p_kl.paragraph_format.line_spacing = 1.2
            r1 = p_kl.add_run("- Kết luận và xếp loại: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p_kl.add_run("Duyệt hồ sơ (Xếp loại: Tốt). ")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13); r2.bold = True
            r3 = p_kl.add_run("Đề nghị thầy Ánh hoàn thiện in đậm nghiêng mục tiêu NLS/AI HĐTN 6.")
            r3.font.name = "Times New Roman"; r3.font.size = Pt(13)

    # 3. Cập nhật Mục V.1: Cả tổ 07 giáo viên
    for p in doc.paragraphs:
        if "1. Đánh giá chung: Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định" in p.text:
            p.text = ""
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Inches(0.5)
            p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2); p.paragraph_format.line_spacing = 1.2
            r1 = p.add_run("1. Đánh giá chung: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p.add_run("Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 07 giáo viên trong tổ. Kết quả: 100% giáo viên (07/07 đồng chí) đạt chuẩn được phê duyệt chính thức (trong đó 06 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá). Toàn bộ hồ sơ trong tổ đảm bảo chất lượng, đúng tiến độ và chuẩn mực sư phạm.")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)
            break

    safe_save_doc(doc, docx_path)
    print("HOÀN THÀNH CẬP NHẬT BIÊN BẢN TỔ DOCX!")

    # Cập nhật Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md
    md_bb_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md"
    with open(md_bb_path, "r", encoding="utf-8") as f:
        bb_md = f.read()

    row7_md = "| **7** | **HOÀNG XUÂN ÁNH** | Toán 7, HĐTN 6 | 29 tiết (80 trang) | Đủ 100% Tháng 9 & vượt Tuần 5; NLS HĐTN 6 lưu ý in đậm nghiêng | **DUYỆT**<br>*(Xếp loại: Tốt)* |\n"
    if "| **7** | **HOÀNG XUÂN ÁNH**" not in bb_md:
        bb_md = bb_md.replace(
            "| **6** | **DƯƠNG QUANG TÙNG** | Tin học 6, 7, 8, 9 | 17 tiết (115 trang) | Đủ 100% Tháng 9 & vượt Tuần 5; NLS/AI mẫu mực | **DUYỆT**<br>*(Xếp loại: Tốt)* |\n",
            "| **6** | **DƯƠNG QUANG TÙNG** | Tin học 6, 7, 8, 9 | 17 tiết (115 trang) | Đủ 100% Tháng 9 & vượt Tuần 5; NLS/AI mẫu mực | **DUYỆT**<br>*(Xếp loại: Tốt)* |\n" + row7_md
        )

    sec7_md = """
### 7. Thầy Hoàng Xuân Ánh (Môn Toán 7, HĐTN 6)
- **Tiến độ và khối lượng**: Nộp đầy đủ 03 tệp PDF gồm 80 trang qua 3 phân môn với tổng số 29 tiết dạy: Đại số 7 (9 tiết, 31 tr), Hình học 7 (8 tiết, 31 tr) và HĐTN 6 (12 tiết, 18 tr). Đảm bảo 100% tiến độ 4 tuần Tháng 9/2026 và vượt tiến độ sang tuần 5 ở phân môn Đại số 7 (hết Bài 3).
- **Ưu điểm nổi bật**: Hồ sơ bài dạy soạn chu đáo, cấu trúc đầy đủ 4 hoạt động theo Công văn số 5512/BGDĐT-GDTrH. Thể thức văn bản, Header/Footer đúng chuẩn quy định của trường THCS Trần Phú. Ký hiệu góc và công thức hình học trong Hình học 7 hiển thị chuẩn mực, rõ nét, không lỗi font. Môn HĐTN 6 tích hợp NLS 2.2.TC1a và AI 6.C2.2 đầy đủ, có phiếu học tập và bảng rubric tự đánh giá rất bài bản.
- **Điểm cần lưu ý**: Các câu mô tả mục tiêu chỉ báo NLS và AI trong tệp HĐTN 6 cần bổ sung định dạng in đậm, nghiêng theo đúng quy chế chuyên môn trước khi lưu hành giảng dạy.
- **Kết luận và xếp loại**: **Duyệt hồ sơ (Xếp loại: Tốt)**. Đề nghị thầy Ánh hoàn thiện in đậm nghiêng mục tiêu NLS/AI HĐTN 6.
"""
    if "### 7. Thầy Hoàng Xuân Ánh" not in bb_md:
        bb_md = bb_md.replace("## V. KẾT LUẬN VÀ KIẾN NGHỊ", sec7_md + "\n---\n\n## V. KẾT LUẬN VÀ KIẾN NGHỊ")

    # Đổi câu đánh giá chung sang 07 giáo viên
    bb_md = bb_md.replace(
        "Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 06 giáo viên trong tổ. Kết quả: 100% giáo viên (06/06 đồng chí) đạt chuẩn được phê duyệt chính thức (trong đó 05 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá). Không còn giáo viên nào bị trả hồ sơ.",
        "Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 07 giáo viên trong tổ. Kết quả: 100% giáo viên (07/07 đồng chí) đạt chuẩn được phê duyệt chính thức (trong đó 06 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá). Không còn giáo viên nào bị trả hồ sơ."
    )

    with open(md_bb_path, "w", encoding="utf-8") as f:
        f.write(bb_md)
    print("HOÀN THÀNH CẬP NHẬT BIÊN BẢN TỔ MARKDOWN!")

# ==============================================================================
# 3. CẬP NHẬT TÀI LIỆU NỘP HỆ THỐNG (Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9)
# ==============================================================================
def update_cap_nhat_he_thong():
    print("\n--- BẮT ĐẦU CẬP NHẬT TÀI LIỆU NỘP HỆ THỐNG ---")
    docx_sys_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.docx"
    doc = docx.Document(docx_sys_path)

    has_sec7 = any("7. THẦY HOÀNG XUÂN ÁNH" in p.text for p in doc.paragraphs)
    if not has_sec7:
        p_h7 = doc.add_paragraph()
        p_h7.paragraph_format.space_before = Pt(16); p_h7.paragraph_format.space_after = Pt(6)
        r = p_h7.add_run("7. THẦY HOÀNG XUÂN ÁNH (MÔN TOÁN 7, HĐTN 6 — 29 TIẾT, 80 TRANG)")
        r.font.name = "Times New Roman"; r.font.size = Pt(13); r.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138)

        items_anh = [
            ("Phân môn Đại số 7 (31 trang — 09 tiết: Bài 1, 2, LTC, Bài 3)",
             "ĐẠT / DUYỆT (TỐT)",
             "Kế hoạch bài dạy soạn tốt, đủ 09 tiết đảm bảo 100% tiến độ tháng 9 và vượt tuần 5. Cấu trúc 4 hoạt động CV 5512 rõ ràng, các bước thực hiện phép tính số hữu tỉ và lũy thừa chính xác, bài tập củng cố phong phú. Duyệt.",
             "16A34A", "F0FDF4"),

            ("Phân môn Hình học 7 (31 trang — 08 tiết: Bài 8, 9, LTC, Bài 10)",
             "ĐẠT / DUYỆT (TỐT)",
             "Soạn đủ 08 tiết đảm bảo đúng tiến độ tháng 9. Kiến thức góc ở vị trí đặc biệt, tia phân giác, hai đường thẳng song song và tiên đề Euclid đầy đủ, logic. Ký hiệu góc và quan hệ hình học hiển thị dấu mũ góc chuẩn xác, không lỗi font. Duyệt.",
             "16A34A", "F0FDF4"),

            ("Phân môn Hoạt động trải nghiệm, hướng nghiệp 6 (18 trang — 12 tiết: Chủ đề 1: Em với nhà trường)",
             "ĐẠT / DUYỆT (KHÁ/TỐT)",
             "Soạn đủ 12 tiết Chủ đề 1 đúng PPCT tháng 9. Cấu trúc phân chia hoạt động chung và hoạt động lớp rõ ràng, có phiếu học tập số và bảng rubric tự đánh giá. Tích hợp NLS (2.2.TC1a) và AI (6.C2.2) đúng địa chỉ. Lưu ý: Cần bổ sung in đậm, nghiêng câu mô tả NLS và AI theo đúng quy định chuyên môn trước khi giảng dạy. Duyệt.",
             "16A34A", "F0FDF4"),

            ("Nhận xét chung toàn bộ hồ sơ Thầy Hoàng Xuân Ánh (Duyệt theo gói)",
             "DUYỆT - XẾP LOẠI TỐT",
             "DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại: Tốt). Hồ sơ giáo án nộp đầy đủ 29 tiết (80 trang) thuộc 3 phân môn Toán 7, HĐTN 6. Đảm bảo 100% tiến độ Tháng 9 và vượt tuần 5 ở Đại 7. Ký hiệu toán học và thể thức chuẩn mực. Nhắc nhở giáo viên in đậm, nghiêng nội dung tích hợp NLS và AI trong HĐTN 6.",
             "16A34A", "F0FDF4"),
        ]

        for sub, status, comment, border_c, bg_c in items_anh:
            p_item = doc.add_paragraph()
            p_item.paragraph_format.space_before = Pt(8); p_item.paragraph_format.space_after = Pt(2)
            r_sub = p_item.add_run(f"• {sub}: ")
            r_sub.font.name = "Times New Roman"; r_sub.font.size = Pt(13); r_sub.bold = True

            r_st = p_item.add_run(f"[{status}]")
            r_st.font.name = "Times New Roman"; r_st.font.size = Pt(13); r_st.bold = True
            r_st.font.color.rgb = RGBColor(22, 163, 74)

            tbl_c = doc.add_table(rows=1, cols=1)
            tbl_c.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell_c = tbl_c.cell(0, 0)
            set_callout_border(cell_c, border_color=border_c, bg_color=bg_c)

            p_c = cell_c.paragraphs[0]
            p_c.paragraph_format.space_before = Pt(2); p_c.paragraph_format.space_after = Pt(2)
            p_c.paragraph_format.line_spacing = 1.15
            r_lbl = p_c.add_run("👉 Nhận xét hệ thống (Copy & Paste): ")
            r_lbl.font.name = "Times New Roman"; r_lbl.font.size = Pt(11); r_lbl.bold = True
            r_lbl.font.color.rgb = RGBColor(15, 23, 42)

            r_txt = p_c.add_run(comment)
            r_txt.font.name = "Times New Roman"; r_txt.font.size = Pt(11)
            r_txt.font.color.rgb = RGBColor(30, 41, 59)

            p_sp = doc.add_paragraph()
            p_sp.paragraph_format.space_before = Pt(0); p_sp.paragraph_format.space_after = Pt(4)

        safe_save_doc(doc, docx_sys_path)
        print("HOÀN THÀNH CẬP NHẬT TÀI LIỆU NỘP HỆ THỐNG DOCX!")

    # Cập nhật Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md
    md_sys_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md"
    with open(md_sys_path, "r", encoding="utf-8") as f:
        sys_md = f.read()

    if "## 7. THẦY HOÀNG XUÂN ÁNH" not in sys_md:
        content_anh_md = """
---

## 7. THẦY HOÀNG XUÂN ÁNH (MÔN TOÁN 7, HĐTN 6 — 29 TIẾT, 80 TRANG)

### • Phân môn Đại số 7 (31 trang — 09 tiết: Bài 1, 2, LTC, Bài 3): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy soạn tốt, đủ 09 tiết đảm bảo 100% tiến độ tháng 9 và vượt tuần 5. Cấu trúc 4 hoạt động CV 5512 rõ ràng, các bước thực hiện phép tính số hữu tỉ và lũy thừa chính xác, bài tập củng cố phong phú. Duyệt.`

### • Phân môn Hình học 7 (31 trang — 08 tiết: Bài 8, 9, LTC, Bài 10): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Soạn đủ 08 tiết đảm bảo đúng tiến độ tháng 9. Kiến thức góc ở vị trí đặc biệt, tia phân giác, hai đường thẳng song song và tiên đề Euclid đầy đủ, logic. Ký hiệu góc và quan hệ hình học hiển thị dấu mũ góc chuẩn xác, không lỗi font. Duyệt.`

### • Phân môn Hoạt động trải nghiệm, hướng nghiệp 6 (18 trang — 12 tiết: Chủ đề 1: Em với nhà trường): [ĐẠT / DUYỆT (KHÁ/TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Soạn đủ 12 tiết Chủ đề 1 đúng PPCT tháng 9. Cấu trúc phân chia hoạt động chung và hoạt động lớp rõ ràng, có phiếu học tập số và bảng rubric tự đánh giá. Tích hợp NLS (2.2.TC1a) và AI (6.C2.2) đúng địa chỉ. Lưu ý: Cần bổ sung in đậm, nghiêng câu mô tả NLS và AI theo đúng quy định chuyên môn trước khi giảng dạy. Duyệt.`

### • Nhận xét chung toàn bộ hồ sơ Thầy Hoàng Xuân Ánh (Duyệt theo gói): [DUYỆT - XẾP LOẠI TỐT]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại: Tốt). Hồ sơ giáo án nộp đầy đủ 29 tiết (80 trang) thuộc 3 phân môn Toán 7, HĐTN 6. Đảm bảo 100% tiến độ Tháng 9 và vượt tuần 5 ở Đại 7. Ký hiệu toán học và thể thức chuẩn mực. Nhắc nhở giáo viên in đậm, nghiêng nội dung tích hợp NLS và AI trong HĐTN 6.`
"""
        with open(md_sys_path, "a", encoding="utf-8") as f:
            f.write(content_anh_md)
        print("HOÀN THÀNH CẬP NHẬT TÀI LIỆU NỘP HỆ THỐNG MARKDOWN!")

if __name__ == "__main__":
    create_phieu_nhan_xet_anh()
    update_bien_ban_to()
    update_cap_nhat_he_thong()
    print("\n>>> TẤT CẢ TÁC VỤ DUYỆT HỒ SƠ THẦY HOÀNG XUÂN ÁNH ĐÃ XONG! <<<")
