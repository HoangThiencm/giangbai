# -*- coding: utf-8 -*-
"""
DUYỆT HỒ SƠ THẦY TRẦN LONG HẢI SAU KHI ĐÃ KHẮC PHỤC TOÀN BỘ SAI SÓT
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
# 1. TẠO LẠI PHIẾU NHẬN XÉT CÁ NHÂN: TRẦN LONG HẢI (02/PĐG-TT) — DUYỆT (TỐT)
# ==============================================================================
def create_phieu_nhan_xet_hai():
    print("\n--- BẮT ĐẦU TẠO LẠI PHIẾU NHẬN XÉT THẦY TRẦN LONG HẢI ---")
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
    r = p0.add_run("Số: 02/PĐG-TT")
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
    r = p1.add_run("Xuân Đông, ngày 07 tháng 10 năm 2026")
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
        ("Họ và tên giáo viên: ", "TRẦN LONG HẢI", True),
        ("Tổ chuyên môn: ", "Toán – Tin, Trường THCS Trần Phú", False),
        ("Nhiệm vụ giảng dạy: ", "Toán 8 (Đại số 8 và Hình học 8 — Sách Kết nối tri thức)", False),
        ("Tổng số hồ sơ nộp: ", "02 phân môn (89 trang PDF, 20 tiết)", False),
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

    t_data = doc.add_table(rows=3, cols=5)
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

    rows_hai = [
        ("Đại số 8", "40 trang", "10 tiết",
         "Đạt 100% Tháng 9 & vượt tuần 5 (Bài 1, 2, LTC, Bài 3, Bài 4, Bài 5). Tích hợp NLS (5.3.TC2a) tại Bài 3 đã IN ĐẬM, NGHIÊNG chuẩn.",
         "DUYỆT (Tốt)"),
        ("Hình học 8", "49 trang", "10 tiết",
         "ĐÃ KHẮC PHỤC TRIỆT ĐỂ: Trang 5 Bài 10 (Tứ giác) dấu mũ góc chuẩn xác, định lý và phép tính chuyển vế đúng 100%. NLS 1.1 và 5.3 in đậm nghiêng. Đạt 100% PPCT & vượt tuần 5.",
         "DUYỆT (Tốt)"),
    ]

    for r_idx, row_val in enumerate(rows_hai, start=1):
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

    # Ưu điểm nổi bật và ghi nhận kết quả khắc phục
    p_u = doc.add_paragraph()
    p_u.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_u.paragraph_format.first_line_indent = Inches(0.5)
    p_u.paragraph_format.space_before = Pt(2); p_u.paragraph_format.space_after = Pt(3)
    p_u.paragraph_format.line_spacing = 1.2
    r_ulbl = p_u.add_run("1. Ưu điểm nổi bật và ghi nhận kết quả khắc phục: ")
    r_ulbl.font.name = "Times New Roman"; r_ulbl.font.size = Pt(13); r_ulbl.bold = True
    r_utxt = p_u.add_run(
        "Giáo viên có tinh thần trách nhiệm nghề nghiệp và ý thức cầu thị rất cao. Ngay sau khi tổ chuyên môn chỉ ra các lỗi kiến thức toán học và ký hiệu góc tại Bài 10 Hình học 8, thầy Trần Long Hải đã nhanh chóng rà soát lại toàn bộ tệp giáo án, sửa lại chuẩn xác 100% định lý tổng các góc trong tứ giác và các phép tính chuyển vế tìm góc ở phần Ví dụ và Luyện tập 2 tại Trang 5; toàn bộ ký hiệu góc hiển thị dấu mũ góc rõ nét, thẩm mỹ, đúng quy chuẩn toán học. Khối lượng bài soạn đồ sộ với 89 trang PDF qua 20 tiết dạy, đảm bảo 100% tiến độ Tháng 9 và vượt tiến độ sang tuần 5 ở cả hai phân môn Đại số 8 và Hình học 8. Các bài dạy sau (Bài 11, 12, 13 Hình học 8 và các bài Đại số 8) soạn rất công phu, chuẩn mực. Các câu mô tả chỉ báo Năng lực số tại Bài 10 Hình 8 (1.1.TC2a, 5.3.TC2a) và Bài 3 Đại 8 (5.3.TC2a) đã được định dạng in đậm, nghiêng rất chuẩn mực theo đúng quy chế chuyên môn."
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
        "Giáo viên đã khắc phục triệt để và hoàn hảo toàn bộ sai sót, hồ sơ đạt chuẩn mực cao. Đề nghị thầy Hải tiếp tục duy trì tính cẩn trọng, tính chính xác khoa học về kiến thức và ký hiệu toán học trong các kế hoạch bài dạy tiếp theo."
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
        "Hồ sơ bài dạy môn Toán 8 (Đại số và Hình học) nộp đầy đủ 20 tiết (89 trang PDF), đảm bảo 100% tiến độ Tháng 9 và vượt tuần 5. Giáo viên đã khắc phục triệt để và hoàn hảo toàn bộ sai sót toán học và ký hiệu góc; tích hợp NLS in đậm nghiêng đúng quy định. Tổ chuyên môn thống nhất DUYỆT TOÀN BỘ HỒ SƠ — XẾP LOẠI: TỐT."
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
    r_n0 = ps0.add_run("Trần Long Hải")
    r_n0.font.name = "Times New Roman"; r_n0.font.size = Pt(13); r_n0.bold = True

    ps1 = cs1.paragraphs[0]
    ps1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ps1.paragraph_format.line_spacing = 1.15
    r_s1 = ps1.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n\n\n\n\n")
    r_s1.font.name = "Times New Roman"; r_s1.font.size = Pt(13); r_s1.bold = True
    r_n1 = ps1.add_run("Hoàng Tấn Thiên")
    r_n1.font.name = "Times New Roman"; r_n1.font.size = Pt(13); r_n1.bold = True

    out_phieu = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_Tran_Long_Hai_Thang_9.docx"
    safe_save_doc(doc, out_phieu)
    print("HOÀN THÀNH TẠO LẠI PHIẾU NHẬN XÉT THẦY HẢI (DUYỆT - TỐT)!")

# ==============================================================================
# 2. CẬP NHẬT BIÊN BẢN KIỂM TRA TỔ (Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9)
# ==============================================================================
def update_bien_ban_to():
    print("\n--- BẮT ĐẦU CẬP NHẬT BIÊN BẢN TỔ CHUYÊN MÔN ---")
    docx_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.docx"
    doc = docx.Document(docx_path)

    # 1. Cập nhật Bảng III (Table 1) - dòng STT 2 (Row index 2)
    t = doc.tables[1]
    row2 = t.rows[2]
    cells = row2.cells

    cells[0].text = "2"
    cells[1].text = "TRẦN LONG HẢI"
    cells[2].text = "Toán 8"
    cells[3].text = "20 tiết\n(89 trang)"
    cells[4].text = "Đủ 100% Tháng 9 & vượt Tuần 5; Đã sửa sạch 100% lỗi toán & NLS chuẩn"
    cells[5].text = "DUYỆT\n(Xếp loại: Tốt)"

    for ci, c in enumerate(cells):
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in [0, 3, 5] else WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            if ci in [1, 5]:
                run.bold = True
            if ci == 5:
                run.font.color.rgb = RGBColor(22, 163, 74) # Xanh lá DUYỆT

    # 2. Cập nhật Mục IV.2 cho Thầy Trần Long Hải
    # Tìm paragraph bắt đầu bằng "2. Thầy Trần Long Hải"
    idx_p2 = -1
    for i, p in enumerate(doc.paragraphs):
        if "2. Thầy Trần Long Hải" in p.text:
            idx_p2 = i
            break

    if idx_p2 != -1:
        # Cập nhật nội dung các đoạn văn của Thầy Hải (thay thế hoặc viết lại các đoạn tiếp theo)
        # Các đoạn sau idx_p2 là Ưu điểm, Tồn tại, Kết luận
        p_u = doc.paragraphs[idx_p2 + 1]
        p_u.text = ""
        p_u.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_u.paragraph_format.first_line_indent = Inches(0.5)
        p_u.paragraph_format.space_before = Pt(2); p_u.paragraph_format.space_after = Pt(2); p_u.paragraph_format.line_spacing = 1.2
        r1 = p_u.add_run("- Tiến độ và khối lượng: ")
        r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
        r2 = p_u.add_run("Hồ sơ giáo án chuẩn bị khối lượng lớn (20 tiết — 89 trang qua 2 phân môn Đại số 8 và Hình học 8), tiến độ đảm bảo 100% tháng 9 và vượt tuần 5 ở cả hai phân môn. Thể thức văn bản, Header/Footer đúng chuẩn quy định của trường THCS Trần Phú.")
        r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

        p_k = doc.paragraphs[idx_p2 + 2]
        p_k.text = ""
        p_k.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_k.paragraph_format.first_line_indent = Inches(0.5)
        p_k.paragraph_format.space_before = Pt(2); p_k.paragraph_format.space_after = Pt(2); p_k.paragraph_format.line_spacing = 1.2
        r1 = p_k.add_run("- Ưu điểm nổi bật và kết quả khắc phục: ")
        r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
        r2 = p_k.add_run("Giáo viên có tinh thần cầu thị và trách nhiệm nghề nghiệp rất cao. Sau khi tổ chuyên môn chỉ ra các lỗi toán học ở bản nộp đầu, thầy Trần Long Hải đã nhanh chóng rà soát và khắc phục triệt để 100% sai sót: định lý tổng các góc tứ giác và các phép tính chuyển vế tìm góc ở Trang 5 Bài 10 (Hình 8) đã chuẩn xác hoàn toàn; toàn bộ ký hiệu góc hiển thị dấu mũ góc rõ nét, chuẩn mực; các câu mô tả chỉ báo Năng lực số tại Bài 10 Hình 8 và Bài 3 Đại 8 đã được in đậm, nghiêng đúng quy định. Các bài dạy sau (Bài 11, 12, 13 Hình học 8 và các bài Đại số 8) soạn rất công phu, chuẩn mực.")
        r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

        p_kl = doc.paragraphs[idx_p2 + 3]
        p_kl.text = ""
        p_kl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_kl.paragraph_format.first_line_indent = Inches(0.5)
        p_kl.paragraph_format.space_before = Pt(2); p_kl.paragraph_format.space_after = Pt(4); p_kl.paragraph_format.line_spacing = 1.2
        r1 = p_kl.add_run("- Kết luận và xếp loại: ")
        r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
        r2 = p_kl.add_run("Duyệt hồ sơ (Xếp loại: Tốt). ")
        r2.font.name = "Times New Roman"; r2.font.size = Pt(13); r2.bold = True
        r3 = p_kl.add_run("Biểu dung tinh thần trách nhiệm và chất lượng hồ sơ sau khi khắc phục của thầy Trần Long Hải.")
        r3.font.name = "Times New Roman"; r3.font.size = Pt(13)

    # 3. Cập nhật Mục V.1 và V.3
    for p in doc.paragraphs:
        if "1. Đánh giá chung: Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định" in p.text:
            p.text = ""
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Inches(0.5)
            p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2); p.paragraph_format.line_spacing = 1.2
            r1 = p.add_run("1. Đánh giá chung: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p.add_run("Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 06 giáo viên trong tổ. Kết quả: 100% giáo viên (06/06 đồng chí) đạt chuẩn được phê duyệt chính thức (trong đó 05 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá). Không còn giáo viên nào bị trả hồ sơ.")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

        if "3. Yêu cầu đối với giáo viên trả hồ sơ:" in p.text:
            p.text = ""
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Inches(0.5)
            p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2); p.paragraph_format.line_spacing = 1.2
            r1 = p.add_run("3. Ghi nhận khắc phục: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p.add_run("Các giáo viên có nội dung đính chính bổ sung (cô Thảo, thầy Sáng, cô Bình, thầy Hải) đều đã hoàn thành xuất sắc việc chỉnh sửa, nộp lại hồ sơ đạt chất lượng cao đúng thời hạn quy định.")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

    safe_save_doc(doc, docx_path)
    print("HOÀN THÀNH CẬP NHẬT BIÊN BẢN TỔ DOCX!")

    # Cập nhật Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md
    md_bb_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md"
    with open(md_bb_path, "r", encoding="utf-8") as f:
        bb_md = f.read()

    # Thay hàng 2 trong markdown
    old_row_hai = "| **2** | **TRẦN LONG HẢI** | Toán 8 | 20 tiết (89 trang) | Đủ 100% Tháng 9 & vượt Tuần 5 | **TRẢ HỒ SƠ**<br>*(Sửa lỗi toán)* |"
    new_row_hai = "| **2** | **TRẦN LONG HẢI** | Toán 8 | 20 tiết (89 trang) | Đủ 100% Tháng 9 & vượt Tuần 5; Đã sửa sạch 100% lỗi toán & NLS chuẩn | **DUYỆT**<br>*(Xếp loại: Tốt)* |"
    if old_row_hai in bb_md:
        bb_md = bb_md.replace(old_row_hai, new_row_hai)

    # Thay mục IV.2 trong markdown
    old_sec2_md = """### 2. Thầy Trần Long Hải (Môn Toán 8)
- **Ưu điểm**: Hồ sơ giáo án chuẩn bị với khối lượng lớn (20 tiết — 89 trang), tiến độ đảm bảo 100% tháng 9 và vượt tuần 5. Thể thức văn bản, Header/Footer đúng chuẩn quy định của trường THCS Trần Phú. Các bài dạy sau (Bài 11, 12, 13 Hình học 8 và các bài Đại số 8) soạn rất công phu, chuẩn mực.
- **Tồn tại sai sót chuyên môn toán học nghiêm trọng (tại Trang 5 Bài 10 Hình học 8)**: (1) Vi phạm ký hiệu góc: Toàn bộ các góc viết trần bằng chữ cái in hoa (A, B, C, D và H, E, F, G), không có dấu mũ góc; (2) Sai bản chất định lý tổng các góc trong tứ giác: viết thành $H + E + F - G = 360^\\circ$ (nhầm dấu trừ); (3) Sai quy tắc chuyển vế và thứ tự phép tính: viết $D = 360^\\circ - A + B + C = 50^\\circ$ và $F = 360^\\circ - H - E + G = 125^\\circ$; (4) Chưa in đậm nghiêng câu mô tả năng lực số tại Bài 10 (Hình 8) và Bài 3 (Đại 8).
- **Kết luận và xếp loại**: **Đề nghị trả hồ sơ**. Yêu cầu thầy Trần Long Hải đính chính chuẩn xác toàn bộ lỗi toán học và ký hiệu góc tại Trang 5 Bài 10, in đậm nghiêng các phần NLS trước khi trình duyệt lại."""

    new_sec2_md = """### 2. Thầy Trần Long Hải (Môn Toán 8)
- **Tiến độ và khối lượng**: Hồ sơ giáo án chuẩn bị khối lượng lớn (20 tiết — 89 trang qua 2 phân môn Đại số 8 và Hình học 8), tiến độ đảm bảo 100% tháng 9 và vượt tuần 5 ở cả hai phân môn. Thể thức văn bản, Header/Footer đúng chuẩn quy định của trường THCS Trần Phú.
- **Ưu điểm nổi bật và kết quả khắc phục**: Giáo viên có tinh thần cầu thị và trách nhiệm nghề nghiệp rất cao. Sau khi tổ chuyên môn chỉ ra các lỗi toán học ở bản nộp đầu, thầy Trần Long Hải đã nhanh chóng rà soát và khắc phục triệt để 100% sai sót: định lý tổng các góc tứ giác và các phép tính chuyển vế tìm góc ở Trang 5 Bài 10 (Hình 8) đã chuẩn xác hoàn toàn; toàn bộ ký hiệu góc hiển thị dấu mũ góc rõ nét, chuẩn mực; các câu mô tả chỉ báo Năng lực số tại Bài 10 Hình 8 và Bài 3 Đại 8 đã được in đậm, nghiêng đúng quy định. Các bài dạy sau (Bài 11, 12, 13 Hình học 8 và các bài Đại số 8) soạn rất công phu, chuẩn mực.
- **Kết luận và xếp loại**: **Duyệt hồ sơ (Xếp loại: Tốt)**. Biểu dương tinh thần trách nhiệm và chất lượng hồ sơ sau khi khắc phục của thầy Trần Long Hải."""

    if old_sec2_md in bb_md:
        bb_md = bb_md.replace(old_sec2_md, new_sec2_md)

    # Thay đổi đánh giá chung Mục V trong MD
    old_v_md = """1. **Đánh giá chung**: Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 06 giáo viên trong tổ. Kết quả: 05 giáo viên đạt chuẩn được phê duyệt (trong đó 04 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá); 01 giáo viên tạm thời trả hồ sơ để chỉnh sửa sai sót toán học (thầy Trần Long Hải).
2. **Yêu cầu đối với giáo viên được phê duyệt**: Tiếp tục duy trì tính nghiêm túc, chuẩn mực trong soạn giảng; hoàn thiện việc in đậm, nghiêng các chỉ báo NLS/AI trước khi giảng dạy trên lớp.
3. **Yêu cầu đối với giáo viên trả hồ sơ**: Thầy Trần Long Hải khẩn trương đính chính dứt điểm toàn bộ lỗi kiến thức và ký hiệu góc tại Trang 5 Bài 10 Hình học 8, in đậm nghiêng mục tiêu NLS và nộp lại hồ sơ trước ngày 08 tháng 10 năm 2026."""

    new_v_md = """1. **Đánh giá chung**: Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 06 giáo viên trong tổ. Kết quả: 100% giáo viên (06/06 đồng chí) đạt chuẩn được phê duyệt chính thức (trong đó 05 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá). Không còn giáo viên nào bị trả hồ sơ.
2. **Yêu cầu đối với giáo viên được phê duyệt**: Tiếp tục duy trì tính nghiêm túc, chuẩn mực trong soạn giảng; phát huy tinh thần ứng dụng công nghệ và tích hợp Năng lực số, Trí tuệ nhân tạo hiệu quả trong giảng dạy.
3. **Ghi nhận khắc phục**: Các giáo viên có nội dung đính chính bổ sung (cô Thảo, thầy Sáng, cô Bình, thầy Hải) đều đã hoàn thành xuất sắc việc chỉnh sửa, nộp lại hồ sơ đạt chất lượng cao đúng thời hạn quy định."""

    if old_v_md in bb_md:
        bb_md = bb_md.replace(old_v_md, new_v_md)

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

    # Cập nhật Mục 2 Thầy Trần Long Hải trong docx:
    # Tìm đoạn Bài 10 và sửa callout
    for i, p in enumerate(doc.paragraphs):
        if "Bài 10: Tứ giác" in p.text and "[KHÔNG DUYỆT" in p.text:
            p.text = "• Bài 10: Tứ giác (Tiết 1, 2 — Trang 1-8): [ĐẠT / DUYỆT (TỐT)]"
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(13)
                r.bold = True
                if "[ĐẠT / DUYỆT" in r.text:
                    r.font.color.rgb = RGBColor(22, 163, 74)

        if "Nhận xét chung gói nộp Hình học 8" in p.text and "[KHÔNG DUYỆT" in p.text:
            p.text = "• Nhận xét chung gói nộp Hình học 8: [ĐẠT / DUYỆT (TỐT)]"
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(13)
                r.bold = True
                if "[ĐẠT / DUYỆT" in r.text:
                    r.font.color.rgb = RGBColor(22, 163, 74)

        if "Nhận xét chung toàn bộ hồ sơ Thầy Trần Long Hải" in p.text:
            p.text = "• Nhận xét chung toàn bộ hồ sơ Thầy Trần Long Hải (Duyệt theo gói): [DUYỆT - XẾP LOẠI TỐT]"
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(13)
                r.bold = True
                if "[DUYỆT" in r.text:
                    r.font.color.rgb = RGBColor(22, 163, 74)

    # Cập nhật nội dung trong các bảng callout của Thầy Hải
    for t in doc.tables:
        c = t.rows[0].cells[0]
        txt = c.text
        if "TRẢ HỒ SƠ do có sai sót nghiêm trọng về kiến thức" in txt:
            set_callout_border(c, border_color="16A34A", bg_color="F0FDF4")
            p = c.paragraphs[0]
            p.text = ""
            r1 = p.add_run("👉 Nhận xét hệ thống (Copy & Paste): ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(11); r1.bold = True
            r1.font.color.rgb = RGBColor(15, 23, 42)
            r2 = p.add_run("Kế hoạch bài dạy Bài 10 đã sửa lại hoàn hảo: định lý tổng các góc tứ giác và các phép tính góc tại Ví dụ, Luyện tập 2 chuẩn xác 100%; ký hiệu góc hiển thị dấu mũ góc rõ nét, chuẩn mực; chỉ báo NLS (1.1 và 5.3) đã được in đậm, nghiêng đúng quy định. Đảm bảo tiến độ và 4 hoạt động CV 5512. Duyệt.")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(11)
            r2.font.color.rgb = RGBColor(30, 41, 59)

        elif "TRẢ LẠI HỒ SƠ. Yêu cầu thầy Trần Long Hải đính chính" in txt:
            set_callout_border(c, border_color="16A34A", bg_color="F0FDF4")
            p = c.paragraphs[0]
            p.text = ""
            r1 = p.add_run("👉 Nhận xét hệ thống (Copy & Paste): ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(11); r1.bold = True
            r1.font.color.rgb = RGBColor(15, 23, 42)
            r2 = p.add_run("DUYỆT GÓI HÌNH HỌC 8. Hồ sơ gồm 10 tiết (49 trang), đảm bảo tiến độ tháng 9 và vượt tuần 5. Giáo viên đã khắc phục triệt để và hoàn hảo toàn bộ lỗi toán học và ký hiệu góc tại Bài 10; tích hợp NLS in đậm nghiêng đúng quy định. Cấu trúc bài soạn công phu, chuẩn mực.")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(11)
            r2.font.color.rgb = RGBColor(30, 41, 59)

    # Thêm callout nhận xét chung gói nếu chưa có
    has_hai_pkg_callout = any("DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại Tốt). Hồ sơ giáo án môn Toán 8 của thầy Trần Long Hải" in t.rows[0].cells[0].text for t in doc.tables)
    if not has_hai_pkg_callout:
        # Tìm vị trí sau "Nhận xét chung toàn bộ hồ sơ Thầy Trần Long Hải"
        idx_p_pkg = -1
        for i, p in enumerate(doc.paragraphs):
            if "Nhận xét chung toàn bộ hồ sơ Thầy Trần Long Hải" in p.text:
                idx_p_pkg = i
                break

    safe_save_doc(doc, docx_sys_path)
    print("HOÀN THÀNH CẬP NHẬT TÀI LIỆU NỘP HỆ THỐNG DOCX!")

    # Cập nhật Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md
    md_sys_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md"
    with open(md_sys_path, "r", encoding="utf-8") as f:
        sys_md = f.read()

    old_hai_md = """## 2. THẦY TRẦN LONG HẢI (MÔN TOÁN 8)

### A. PHÂN MÔN HÌNH HỌC 8 (49 TRANG — 6 BÀI):

* **Bài 10: Tứ giác (Tiết 1, 2 — Trang 1-8)**: [KHÔNG DUYỆT / TRẢ HỒ SƠ]
  > **👉 Nhận xét hệ thống (Copy & Paste):**  
  > `TRẢ HỒ SƠ do có sai sót nghiêm trọng về kiến thức và ký hiệu toán học tại Trang 5: (1) Mất dấu mũ góc ở toàn bộ các công thức (viết trần A, B, C, D); (2) Sai bản chất định lý tổng các góc: viết H + E + F - G = 360° (nhầm dấu trừ); (3) Sai quy tắc chuyển vế và thứ tự phép tính: viết D = 360° - A + B + C = 50° và F = 360° - H - E + G = 125°. Đề nghị đính chính chuẩn xác ký hiệu góc và biểu thức toán học, in đậm nghiêng NLS 1.1, 5.3 trước khi duyệt.`

* **Bài 11: Hình thang cân (Tiết 3, 4 — Trang 9-18)**: [ĐẠT / DUYỆT]
  > `Soạn tốt, đủ 4 hoạt động theo CV 5512. Ký hiệu góc và các bước chứng minh tính chất hình thang cân chuẩn xác. Tiến độ đúng PPCT. Duyệt.`

* **Luyện tập chung (Tiết 5 — Trang 19-24)**: [ĐẠT / DUYỆT]
  > `Hệ thống bài tập củng cố tính chất góc và cạnh của tứ giác, hình thang cân bám sát SGK. Ký hiệu toán học chuẩn. Duyệt.`

* **Bài 12: Hình bình hành (Tiết 6, 7 — Trang 25-36)**: [ĐẠT / DUYỆT]
  > `Kế hoạch bài dạy chi tiết (12 trang), phân hóa đối tượng học sinh tốt, ứng dụng đồ dùng dạy học trực quan. Ký hiệu góc chuẩn xác. Duyệt.`

* **Luyện tập chung (Tiết 8 — Trang 37-40)**: [ĐẠT / DUYỆT]
  > `Bài tập rèn luyện kỹ năng chứng minh hình bình hành chuẩn mực, các bước suy luận logic. Duyệt.`

* **Bài 13: Hình chữ nhật (Tiết 9, 10 — Trang 41-49)**: [ĐẠT / DUYỆT]
  > `Soạn vượt tiến độ tuần 5, nội dung định nghĩa, tính chất và dấu hiệu nhận biết hình chữ nhật rất chuẩn xác, khoa học. Duyệt.`

* **Nhận xét chung gói nộp Hình học 8 (Nếu duyệt theo gói/tệp)**: [KHÔNG DUYỆT / TRẢ HỒ SƠ]
  > `TRẢ LẠI HỒ SƠ. Yêu cầu thầy Trần Long Hải đính chính dứt điểm toàn bộ lỗi kiến thức định lý và ký hiệu góc tại Trang 5 Bài 10, in đậm nghiêng NLS trước khi phê duyệt toàn tệp.`

### B. PHÂN MÔN ĐẠI SỐ 8 (40 TRANG — 6 BÀI):

* **Bài 1, 2, LTC 6, Bài 4, Bài 5**: [ĐẠT / DUYỆT]
* **Bài 3: Phép cộng và phép trừ đa thức (Tiết 5)**: [DUYỆT CÓ LƯU Ý]
  > `Phương pháp rèn kỹ năng quy tắc dấu ngoặc khi trừ đa thức chặt chẽ. Có tích hợp NLS (5.3.TC2a) khớp Phụ lục 3. Lưu ý: Cần in đậm, nghiêng câu mô tả năng lực số theo đúng quy định chuyên môn.`
* **Nhận xét chung gói nộp Đại số 8**: [ĐẠT YÊU CẦU]
  > `ĐẠT YÊU CẦU. Kế hoạch bài dạy soạn đầy đủ 10 tiết, đúng PPCT và vượt tiến độ. Nhắc nhở giáo viên in đậm, nghiêng câu mô tả năng lực số tại Bài 3 theo đúng quy định.`"""

    new_hai_md = """## 2. THẦY TRẦN LONG HẢI (MÔN TOÁN 8 — 20 TIẾT, 89 TRANG)

### A. PHÂN MÔN HÌNH HỌC 8 (49 TRANG — 6 BÀI):

* **Bài 10: Tứ giác (Tiết 1, 2 — Trang 1-8)**: [ĐẠT / DUYỆT (TỐT)]
  > **👉 Nhận xét hệ thống (Copy & Paste):**  
  > `Kế hoạch bài dạy Bài 10 đã sửa lại hoàn hảo: định lý tổng các góc tứ giác và các phép tính góc tại Ví dụ, Luyện tập 2 chuẩn xác 100%; ký hiệu góc hiển thị dấu mũ góc rõ nét, chuẩn mực; chỉ báo NLS (1.1 và 5.3) đã được in đậm, nghiêng đúng quy định. Đảm bảo tiến độ và 4 hoạt động CV 5512. Duyệt.`

* **Bài 11: Hình thang cân (Tiết 3, 4 — Trang 9-18)**: [ĐẠT / DUYỆT]
  > `Soạn tốt, đủ 4 hoạt động theo CV 5512. Ký hiệu góc và các bước chứng minh tính chất hình thang cân chuẩn xác. Tiến độ đúng PPCT. Duyệt.`

* **Luyện tập chung (Tiết 5 — Trang 19-24)**: [ĐẠT / DUYỆT]
  > `Hệ thống bài tập củng cố tính chất góc và cạnh của tứ giác, hình thang cân bám sát SGK. Ký hiệu toán học chuẩn. Duyệt.`

* **Bài 12: Hình bình hành (Tiết 6, 7 — Trang 25-36)**: [ĐẠT / DUYỆT]
  > `Kế hoạch bài dạy chi tiết (12 trang), phân hóa đối tượng học sinh tốt, ứng dụng đồ dùng dạy học trực quan. Ký hiệu góc chuẩn xác. Duyệt.`

* **Luyện tập chung (Tiết 8 — Trang 37-40)**: [ĐẠT / DUYỆT]
  > `Bài tập rèn luyện kỹ năng chứng minh hình bình hành chuẩn mực, các bước suy luận logic. Duyệt.`

* **Bài 13: Hình chữ nhật (Tiết 9, 10 — Trang 41-49)**: [ĐẠT / DUYỆT]
  > `Soạn vượt tiến độ tuần 5, nội dung định nghĩa, tính chất và dấu hiệu nhận biết hình chữ nhật rất chuẩn xác, khoa học. Duyệt.`

* **Nhận xét chung gói nộp Hình học 8 (Nếu duyệt theo gói/tệp)**: [ĐẠT / DUYỆT (TỐT)]
  > **👉 Nhận xét hệ thống (Copy & Paste):**  
  > `DUYỆT GÓI HÌNH HỌC 8. Hồ sơ gồm 10 tiết (49 trang), đảm bảo tiến độ tháng 9 và vượt tuần 5. Giáo viên đã khắc phục triệt để và hoàn hảo toàn bộ lỗi toán học và ký hiệu góc tại Bài 10; tích hợp NLS in đậm nghiêng đúng quy định. Cấu trúc bài soạn công phu, chuẩn mực.`

### B. PHÂN MÔN ĐẠI SỐ 8 (40 TRANG — 6 BÀI):

* **Bài 1, 2, LTC 6, Bài 4, Bài 5**: [ĐẠT / DUYỆT]
* **Bài 3: Phép cộng và phép trừ đa thức (Tiết 5)**: [ĐẠT / DUYỆT (TỐT)]
  > `Phương pháp rèn kỹ năng quy tắc dấu ngoặc khi trừ đa thức chặt chẽ. Đã tích hợp NLS (5.3.TC2a) khớp Phụ lục 3 và IN ĐẬM, NGHIÊNG đúng quy định chuyên môn. Duyệt.`
* **Nhận xét chung gói nộp Đại số 8**: [ĐẠT YÊU CẦU / DUYỆT]
  > `ĐẠT YÊU CẦU. Kế hoạch bài dạy soạn đầy đủ 10 tiết, đúng PPCT và vượt tiến độ. Tích hợp NLS in đậm, nghiêng chuẩn mực. Duyệt.`

### • Nhận xét chung toàn bộ hồ sơ Thầy Trần Long Hải (Duyệt theo gói): [DUYỆT - XẾP LOẠI TỐT]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại Tốt). Hồ sơ giáo án nộp đầy đủ 20 tiết (89 trang) môn Toán 8 (Đại số và Hình học). Đảm bảo 100% tiến độ Tháng 9 và vượt tuần 5 ở cả hai phân môn. Giáo viên đã khắc phục triệt để và hoàn hảo toàn bộ sai sót toán học và ký hiệu góc tại Bài 10 Hình 8; tích hợp NLS in đậm nghiêng đúng quy định. Biểu dương tinh thần cầu thị và trách nhiệm nghề nghiệp của thầy Hải.`"""

    if old_hai_md in sys_md:
        sys_md = sys_md.replace(old_hai_md, new_hai_md)

    with open(md_sys_path, "w", encoding="utf-8") as f:
        f.write(sys_md)
    print("HOÀN THÀNH CẬP NHẬT TÀI LIỆU NỘP HỆ THỐNG MARKDOWN!")

if __name__ == "__main__":
    create_phieu_nhan_xet_hai()
    update_bien_ban_to()
    update_cap_nhat_he_thong()
    print("\n>>> TẤT CẢ TÁC VỤ DUYỆT HỒ SƠ THẦY TRẦN LONG HẢI ĐÃ XONG! <<<")
