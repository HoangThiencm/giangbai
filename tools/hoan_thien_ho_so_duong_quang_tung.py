# -*- coding: utf-8 -*-
"""
CẬP NHẬT HOÀN THIỆN HỒ SƠ THẨM ĐỊNH THẦY DƯƠNG QUANG TÙNG (MÔN TIN HỌC 6, 7, 8, 9)
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
# HELPER FUNCTIONS CHO ĐỊNH DẠNG THEO NGHỊ ĐỊNH 30/2020/NĐ-CP
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
# 1. TẠO PHIẾU NHẬN XÉT CÁ NHÂN: DƯƠNG QUANG TÙNG (06/PĐG-TT)
# ==============================================================================
def create_phieu_nhan_xet_tung():
    print("\n--- BẮT ĐẦU TẠO PHIẾU NHẬN XÉT DƯƠNG QUANG TÙNG ---")
    doc = docx.Document()
    apply_page_setup_nd30(doc)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)

    # 1. Quốc hiệu tiêu ngữ (Table 0 - không viền)
    tbl_h = doc.add_table(rows=1, cols=2)
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl_h.cell(0, 0)
    c1 = tbl_h.cell(0, 1)
    set_cell_margins(c0, 0, 0, 0, 0)
    set_cell_margins(c1, 0, 0, 0, 0)

    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    p0.paragraph_format.line_spacing = 1.15
    r = p0.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12)
    r = p0.add_run("TỔ TOÁN – TIN\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
    r = p0.add_run("———————\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(10)
    r = p0.add_run("Số: 06/PĐG-TT")
    r.font.name = "Times New Roman"; r.font.size = Pt(12)

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
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
    p_t0.paragraph_format.space_before = Pt(14)
    p_t0.paragraph_format.space_after = Pt(2)
    r_t0 = p_t0.add_run("PHIẾU NHẬN XÉT, ĐÁNH GIÁ HỒ SƠ BÀI DẠY")
    r_t0.font.name = "Times New Roman"; r_t0.font.size = Pt(14); r_t0.bold = True

    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(0)
    p_t1.paragraph_format.space_after = Pt(12)
    r_t1 = p_t1.add_run("(ĐỢT THÁNG 9/2026 — NĂM HỌC 2026 - 2027)")
    r_t1.font.name = "Times New Roman"; r_t1.font.size = Pt(13); r_t1.italic = True

    # 3. Thông tin giáo viên (Đồng nhất 13pt, thụt lề 0.5 inch, Justify, line spacing 1.2)
    info_items = [
        ("Họ và tên giáo viên: ", "DƯƠNG QUANG TÙNG", True),
        ("Tổ chuyên môn: ", "Toán – Tin, Trường THCS Trần Phú", False),
        ("Nhiệm vụ giảng dạy: ", "Tin học 6, Tin học 7, Tin học 8, Tin học 9", False),
        ("Tổng số hồ sơ nộp: ", "04 khối lớp (115 trang PDF, 17 tiết)", False),
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
    p_sec1.paragraph_format.space_before = Pt(8)
    p_sec1.paragraph_format.space_after = Pt(4)
    p_sec1.paragraph_format.line_spacing = 1.2
    r_s1 = p_sec1.add_run("I. KẾT QUẢ THẨM ĐỊNH CHI TIẾT THEO TỪNG PHÂN MÔN")
    r_s1.font.name = "Times New Roman"; r_s1.font.size = Pt(13); r_s1.bold = True

    # Table 1: Bảng dữ liệu 4 khối lớp Tin học
    t_data = doc.add_table(rows=5, cols=5)
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

    rows_tin = [
        ("Tin học 6", "19 trang", "04 tiết",
         "Đạt 100% Tháng 9 (Bài 1, Bài 2). Tích hợp NLS (1.2.TC1a, 5.3.TC1a) và AI (6.A1.1) khớp Phụ lục 3 và đã IN ĐẬM, NGHIÊNG, MÀU TÍM rất chuẩn mực.",
         "DUYỆT (Tốt)"),
        ("Tin học 7", "23 trang", "04 tiết",
         "Đạt 100% Tháng 9 (Bài 1, 2, 3). Tích hợp AI (7.A1.1) và NLS (5.3.TC1a, 1.2.TC1a, 3.1.TC1a) khớp Phụ lục 3 và đã IN ĐẬM, NGHIÊNG, MÀU TÍM rất chuẩn mực.",
         "DUYỆT (Tốt)"),
        ("Tin học 8", "24 trang", "04 tiết",
         "Đạt 100% Tháng 9 (Bài 1, 2, 3, 4). Tích hợp AI (8.A3.3) tại Bài 1 và NLS (1.2.TC2a) tại Bài 2 đã IN ĐẬM, NGHIÊNG, MÀU TÍM đúng quy định.",
         "DUYỆT (Tốt)"),
        ("Tin học 9", "49 trang", "05 tiết",
         "Đạt 100% Tháng 9 & vượt tuần 5 (Bài 1 đến 4). Tích hợp NLS (3.1.TC2a, 1.2.TC2a) và AI (9.B2.1, 9.D1.1) in đậm, nghiêng, màu tím; ứng dụng AI sáng tạo.",
         "DUYỆT (Xuất sắc)"),
    ]

    for r_idx, row_val in enumerate(rows_tin, start=1):
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
    p_sec2.paragraph_format.space_before = Pt(12)
    p_sec2.paragraph_format.space_after = Pt(4)
    p_sec2.paragraph_format.line_spacing = 1.2
    r_s2 = p_sec2.add_run("II. NHẬN XÉT CHUYÊN MÔN CHI TIẾT")
    r_s2.font.name = "Times New Roman"; r_s2.font.size = Pt(13); r_s2.bold = True

    # Nhận xét 1: Ưu điểm nổi bật
    p_u = doc.add_paragraph()
    p_u.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_u.paragraph_format.first_line_indent = Inches(0.5)
    p_u.paragraph_format.space_before = Pt(2)
    p_u.paragraph_format.space_after = Pt(3)
    p_u.paragraph_format.line_spacing = 1.2
    r_ulbl = p_u.add_run("1. Ưu điểm nổi bật: ")
    r_ulbl.font.name = "Times New Roman"; r_ulbl.font.size = Pt(13); r_ulbl.bold = True
    r_utxt = p_u.add_run(
        "Hồ sơ bài dạy môn Tin học các khối 6, 7, 8, 9 được chuẩn bị vô cùng bài bản, mẫu mực bậc nhất trong tổ với tổng số 115 trang PDF qua 17 tiết dạy. Tiến độ đảm bảo 100% chương trình 4 tuần Tháng 9/2026 và vượt tiến độ sang tuần 5 ở khối 9 (đến hết Bài 4). Thể thức văn bản, Header và Footer đúng chuẩn quy định của trường THCS Trần Phú. Thiết kế tiến trình dạy học đảm bảo đầy đủ 4 hoạt động theo Công văn số 5512/BGDĐT-GDTrH. Đặc biệt, nội dung tích hợp Năng lực số (NLS) và Trí tuệ nhân tạo (AI) được triển khai cực kỳ xuất sắc: 100% các câu mô tả chỉ báo hành động trong cả 4 khối lớp đều khớp hoàn toàn với Phụ lục 3 và được định dạng in đậm, nghiêng, màu tím rất nổi bật và chuyên nghiệp. Thầy Tùng đã rất sáng tạo khi tích hợp việc hướng dẫn học sinh ứng dụng các công cụ AI (ChatGPT, Gemini, Copilot) làm trợ lý tìm kiếm thông tin và học tập an toàn."
    )
    r_utxt.font.name = "Times New Roman"; r_utxt.font.size = Pt(13)

    # Nhận xét 2: Điểm lưu ý
    p_l = doc.add_paragraph()
    p_l.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_l.paragraph_format.first_line_indent = Inches(0.5)
    p_l.paragraph_format.space_before = Pt(2)
    p_l.paragraph_format.space_after = Pt(3)
    p_l.paragraph_format.line_spacing = 1.2
    r_llbl = p_l.add_run("2. Điểm lưu ý khi lưu hành giảng dạy: ")
    r_llbl.font.name = "Times New Roman"; r_llbl.font.size = Pt(13); r_llbl.bold = True
    r_ltxt = p_l.add_run(
        "Hồ sơ chuẩn bị hoàn chỉnh, không có bất kỳ lỗi font chữ hay vi phạm chuyên môn. Đề nghị thầy Tùng tiếp tục phát huy tinh thần tiên phong ứng dụng công nghệ và lan tỏa kinh nghiệm xây dựng kế hoạch bài dạy tích hợp AI cho các đồng nghiệp trong tổ chuyên môn ở các đợt sinh hoạt chuyên đề sắp tới."
    )
    r_ltxt.font.name = "Times New Roman"; r_ltxt.font.size = Pt(13)

    # Khoảng đệm trước Table 2
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

    # Table 2: Callout kết luận và xếp loại
    tbl_callout = doc.add_table(rows=1, cols=1)
    tbl_callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_call = tbl_callout.cell(0, 0)
    set_callout_border(c_call, border_color="16A34A", bg_color="F0FDF4")

    p_call = c_call.paragraphs[0]
    p_call.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_call.paragraph_format.space_before = Pt(2)
    p_call.paragraph_format.space_after = Pt(2)
    p_call.paragraph_format.line_spacing = 1.2
    r_clbl = p_call.add_run("👉 KẾT LUẬN & XẾP LOẠI: ")
    r_clbl.font.name = "Times New Roman"; r_clbl.font.size = Pt(13); r_clbl.bold = True
    r_clbl.font.color.rgb = RGBColor(15, 23, 42)
    r_ctxt = p_call.add_run(
        "Hồ sơ bài dạy nộp đầy đủ 17 tiết (115 trang PDF) thuộc 4 khối lớp Tin học 6, 7, 8, 9; đảm bảo 100% tiến độ Tháng 9 và vượt tuần 5 ở khối 9. Tích hợp Năng lực số và AI kiểu mẫu, 100% câu mô tả đều in đậm, nghiêng, màu tím nổi bật và khớp chuẩn Phụ lục 3. Thể thức và tiến trình 4 hoạt động CV 5512 bài bản, chuẩn mực. Tổ chuyên môn thống nhất DUYỆT TOÀN BỘ HỒ SƠ — XẾP LOẠI: TỐT."
    )
    r_ctxt.font.name = "Times New Roman"; r_ctxt.font.size = Pt(13)
    r_ctxt.font.color.rgb = RGBColor(15, 23, 42)

    # Khoảng đệm trước Table 3
    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(4)
    p_sp2.paragraph_format.space_after = Pt(6)

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
    r_n0 = ps0.add_run("Dương Quang Tùng")
    r_n0.font.name = "Times New Roman"; r_n0.font.size = Pt(13); r_n0.bold = True

    ps1 = cs1.paragraphs[0]
    ps1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ps1.paragraph_format.line_spacing = 1.15
    r_s1 = ps1.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n\n\n\n\n")
    r_s1.font.name = "Times New Roman"; r_s1.font.size = Pt(13); r_s1.bold = True
    r_n1 = ps1.add_run("Hoàng Tấn Thiên")
    r_n1.font.name = "Times New Roman"; r_n1.font.size = Pt(13); r_n1.bold = True

    out_phieu = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_Duong_Quang_Tung_Thang_9.docx"
    safe_save_doc(doc, out_phieu)
    print("HOÀN THÀNH TẠO PHIẾU NHẬN XÉT THẦY TÙNG!")

# ==============================================================================
# 2. CẬP NHẬT BIÊN BẢN KIỂM TRA TỔ (Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9)
# ==============================================================================
def update_bien_ban_to():
    print("\n--- BẮT ĐẦU CẬP NHẬN BIÊN BẢN TỔ CHUYÊN MÔN ---")
    docx_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.docx"
    doc = docx.Document(docx_path)

    # 1. Cập nhật Bảng III (Table 1) - dòng STT 6
    t = doc.tables[1]
    row6 = t.rows[6]
    cells = row6.cells

    cells[0].text = "6"
    cells[1].text = "DƯƠNG QUANG TÙNG"
    cells[2].text = "Tin học 6, 7, 8, 9"
    cells[3].text = "17 tiết\n(115 trang)"
    cells[4].text = "Đủ 100% Tháng 9 & vượt Tuần 5; NLS/AI mẫu mực"
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

    # 2. Cập nhật Mục IV: Thêm mục IV.6 nếu chưa có
    has_sec6 = any("6. Thầy Dương Quang Tùng" in p.text for p in doc.paragraphs)
    if not has_sec6:
        # Tìm vị trí đoạn V. KẾT LUẬN VÀ KIẾN NGHỊ để chèn trước đó
        p_v_idx = -1
        for idx, p in enumerate(doc.paragraphs):
            if "V. KẾT LUẬN VÀ KIẾN NGHỊ" in p.text:
                p_v_idx = idx
                break

        if p_v_idx != -1:
            # Chèn các đoạn của Thầy Tùng trước đoạn V
            p_v = doc.paragraphs[p_v_idx]

            # Header mục 6
            p_h6 = p_v.insert_paragraph_before()
            p_h6.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_h6.paragraph_format.first_line_indent = Inches(0.5)
            p_h6.paragraph_format.space_before = Pt(4)
            p_h6.paragraph_format.space_after = Pt(2)
            p_h6.paragraph_format.line_spacing = 1.2
            r = p_h6.add_run("6. Thầy Dương Quang Tùng (Môn Tin học 6, 7, 8, 9)")
            r.font.name = "Times New Roman"; r.font.size = Pt(13); r.bold = True

            # Đoạn 1: Tiến độ và khối lượng
            p_td = p_v.insert_paragraph_before()
            p_td.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_td.paragraph_format.first_line_indent = Inches(0.5)
            p_td.paragraph_format.space_before = Pt(2)
            p_td.paragraph_format.space_after = Pt(2)
            p_td.paragraph_format.line_spacing = 1.2
            r1 = p_td.add_run("- Tiến độ và khối lượng: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p_td.add_run("Nộp đầy đủ 04 tệp PDF gồm 115 trang qua 4 khối lớp, tổng cộng 17 tiết dạy: Tin học 6 (4 tiết, 19 tr), Tin học 7 (4 tiết, 23 tr), Tin học 8 (4 tiết, 24 tr) và Tin học 9 (5 tiết, 49 tr). Đảm bảo 100% tiến độ 4 tuần Tháng 9/2026 và vượt tiến độ sang tuần 5 ở khối 9 (đến hết Bài 4).")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

            # Đoạn 2: Ưu điểm nổi bật
            p_ud = p_v.insert_paragraph_before()
            p_ud.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_ud.paragraph_format.first_line_indent = Inches(0.5)
            p_ud.paragraph_format.space_before = Pt(2)
            p_ud.paragraph_format.space_after = Pt(2)
            p_ud.paragraph_format.line_spacing = 1.2
            r1 = p_ud.add_run("- Ưu điểm nổi bật: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p_ud.add_run("Hồ sơ bài dạy chuẩn bị cực kỳ đồ sộ, bài bản, mẫu mực bậc nhất trong tổ. Thể thức văn bản, Header/Footer đúng chuẩn quy định của trường THCS Trần Phú. Thiết kế tiến trình dạy học đảm bảo đầy đủ 4 hoạt động theo Công văn số 5512/BGDĐT-GDTrH. Đặc biệt, việc tích hợp Năng lực số (NLS) và Trí tuệ nhân tạo (AI) được thực hiện xuất sắc: 100% các câu mô tả chỉ báo hành động trong cả 4 khối lớp đều được đưa đúng địa chỉ theo Phụ lục 3 và được định dạng in đậm, nghiêng, màu tím rất nổi bật (Tin 6: 1.2.TC1a, 5.3.TC1a, AI 6.A1.1; Tin 7: AI 7.A1.1, NLS 5.3.TC1a, 1.2.TC1a, 3.1.TC1a; Tin 8: AI 8.A3.3, NLS 1.2.TC2a; Tin 9: NLS 3.1.TC2a, 1.2.TC2a, AI 9.B2.1, 9.D1.1). Kế hoạch bài dạy có ứng dụng các công cụ AI (ChatGPT, Gemini, Copilot) hỗ trợ học tập rất hiện đại, sáng tạo.")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)

            # Đoạn 3: Kết luận và xếp loại
            p_kl = p_v.insert_paragraph_before()
            p_kl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_kl.paragraph_format.first_line_indent = Inches(0.5)
            p_kl.paragraph_format.space_before = Pt(2)
            p_kl.paragraph_format.space_after = Pt(6)
            p_kl.paragraph_format.line_spacing = 1.2
            r1 = p_kl.add_run("- Kết luận và xếp loại: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p_kl.add_run("Duyệt hồ sơ (Xếp loại: Tốt). ")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13); r2.bold = True
            r3 = p_kl.add_run("Biểu dương sự đầu tư công phu và tính gương mẫu của thầy Dương Quang Tùng.")
            r3.font.name = "Times New Roman"; r3.font.size = Pt(13)

    # 3. Cập nhật Mục V.1: Cả tổ 06 giáo viên (05 Duyệt, 01 Trả)
    for p in doc.paragraphs:
        if "1. Đánh giá chung: Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định" in p.text:
            p.text = ""
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Inches(0.5)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.2
            r1 = p.add_run("1. Đánh giá chung: ")
            r1.font.name = "Times New Roman"; r1.font.size = Pt(13); r1.bold = True
            r2 = p.add_run("Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 06 giáo viên trong tổ. Kết quả: 05 giáo viên đạt chuẩn được phê duyệt (trong đó 04 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá); 01 giáo viên tạm thời trả hồ sơ để chỉnh sửa sai sót toán học (thầy Trần Long Hải).")
            r2.font.name = "Times New Roman"; r2.font.size = Pt(13)
            break

    safe_save_doc(doc, docx_path)
    print("HOÀN THÀNH CẬP NHẬT BIÊN BẢN TỔ DOCX!")

    # Cập nhật Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md
    md_bb_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md"
    with open(md_bb_path, "r", encoding="utf-8") as f:
        bb_md = f.read()

    # Thay hàng 6 trong markdown
    old_row = "| *6* | *[Đang chờ nạp...]* | *—* | *—* | *—* | *—* |"
    new_row = "| **6** | **DƯƠNG QUANG TÙNG** | Tin học 6, 7, 8, 9 | 17 tiết (115 trang) | Đủ 100% Tháng 9 & vượt Tuần 5; NLS/AI mẫu mực | **DUYỆT**<br>*(Xếp loại: Tốt)* |"
    if old_row in bb_md:
        bb_md = bb_md.replace(old_row, new_row)

    # Thêm mục 6 vào markdown
    sec6_md = """
### 6. Thầy Dương Quang Tùng (Môn Tin học 6, 7, 8, 9)
- **Tiến độ và khối lượng**: Nộp đầy đủ 04 tệp PDF gồm 115 trang qua 4 khối lớp, tổng cộng 17 tiết dạy: Tin học 6 (4 tiết, 19 tr), Tin học 7 (4 tiết, 23 tr), Tin học 8 (4 tiết, 24 tr) và Tin học 9 (5 tiết, 49 tr). Đảm bảo 100% tiến độ 4 tuần Tháng 9/2026 và vượt tiến độ sang tuần 5 ở khối 9 (đến hết Bài 4).
- **Ưu điểm nổi bật**: Hồ sơ bài dạy chuẩn bị cực kỳ đồ sộ, bài bản, mẫu mực bậc nhất trong tổ. Thể thức văn bản, Header/Footer đúng chuẩn quy định của trường THCS Trần Phú. Thiết kế tiến trình dạy học đảm bảo đầy đủ 4 hoạt động theo Công văn số 5512/BGDĐT-GDTrH. Đặc biệt, việc tích hợp Năng lực số (NLS) và Trí tuệ nhân tạo (AI) được thực hiện xuất sắc: 100% các câu mô tả chỉ báo hành động trong cả 4 khối lớp đều được đưa đúng địa chỉ theo Phụ lục 3 và được định dạng in đậm, nghiêng, màu tím rất nổi bật (Tin 6: 1.2.TC1a, 5.3.TC1a, AI 6.A1.1; Tin 7: AI 7.A1.1, NLS 5.3.TC1a, 1.2.TC1a, 3.1.TC1a; Tin 8: AI 8.A3.3, NLS 1.2.TC2a; Tin 9: NLS 3.1.TC2a, 1.2.TC2a, AI 9.B2.1, 9.D1.1). Kế hoạch bài dạy có ứng dụng các công cụ AI (ChatGPT, Gemini, Copilot) hỗ trợ học tập rất hiện đại, sáng tạo.
- **Kết luận và xếp loại**: **Duyệt hồ sơ (Xếp loại: Tốt)**. Biểu dương sự đầu tư công phu và tính gương mẫu của thầy Dương Quang Tùng.
"""
    if "### 6. Thầy Dương Quang Tùng" not in bb_md:
        bb_md = bb_md.replace("## V. KẾT LUẬN VÀ KIẾN NGHỊ", sec6_md + "\n---\n\n## V. KẾT LUẬN VÀ KIẾN NGHỊ")

    # Cập nhật Mục V.1 trong MD
    old_v1 = "1. **Đánh giá chung**: Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 05 giáo viên trong tổ. Kết quả: 04 giáo viên đạt chuẩn được phê duyệt (trong đó 03 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá); 01 giáo viên tạm thời trả hồ sơ để chỉnh sửa sai sót toán học (thầy Trần Long Hải)."
    new_v1 = "1. **Đánh giá chung**: Đợt kiểm tra hồ sơ tháng 9/2026 đã tiến hành thẩm định 06 giáo viên trong tổ. Kết quả: 05 giáo viên đạt chuẩn được phê duyệt (trong đó 04 giáo viên xếp loại Tốt, 01 giáo viên xếp loại Khá); 01 giáo viên tạm thời trả hồ sơ để chỉnh sửa sai sót toán học (thầy Trần Long Hải)."
    bb_md = bb_md.replace(old_v1, new_v1)

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

    has_sec6 = any("6. THẦY DƯƠNG QUANG TÙNG" in p.text for p in doc.paragraphs)
    if not has_sec6:
        # Tiêu đề giáo viên 6
        p_h6 = doc.add_paragraph()
        p_h6.paragraph_format.space_before = Pt(16)
        p_h6.paragraph_format.space_after = Pt(6)
        r = p_h6.add_run("6. THẦY DƯƠNG QUANG TÙNG (MÔN TIN HỌC 6, 7, 8, 9 — 17 TIẾT, 115 TRANG)")
        r.font.name = "Times New Roman"; r.font.size = Pt(13); r.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138)

        items_tung = [
            ("Phân môn Tin học 6 (19 trang — 04 tiết: Bài 1, Bài 2)",
             "ĐẠT / DUYỆT (TỐT)",
             "Kế hoạch bài dạy chuẩn bị chu đáo, đủ 04 tiết đảm bảo 100% tiến độ 4 tuần tháng 9 theo đúng PPCT (Bài 1: 2 tiết, Bài 2: 2 tiết). Cấu trúc 4 hoạt động CV 5512 rõ ràng. Tích hợp Năng lực số (1.2.TC1a, 5.3.TC1a) và Năng lực AI (6.A1.1) khớp chuẩn Phụ lục 3 và đã IN ĐẬM, NGHIÊNG, MÀU TÍM rất nổi bật theo quy chế chuyên môn. Duyệt.",
             "16A34A", "F0FDF4"),

            ("Phân môn Tin học 7 (23 trang — 04 tiết: Bài 1, Bài 2, Bài 3)",
             "ĐẠT / DUYỆT (TỐT)",
             "Soạn đủ 04 tiết đúng tiến độ tháng 9 theo PPCT (Bài 1: 1 tiết, Bài 2: 1 tiết, Bài 3: 2 tiết). Tiến trình dạy học mạch lạc, phiếu học tập rõ ràng. Tích hợp Năng lực AI (7.A1.1) và Năng lực số (5.3.TC1a, 1.2.TC1a, 3.1.TC1a) khớp Phụ lục 3 và đã IN ĐẬM, NGHIÊNG, MÀU TÍM chuẩn mực. Duyệt.",
             "16A34A", "F0FDF4"),

            ("Phân môn Tin học 8 (24 trang — 04 tiết: Bài 1, Bài 2, Bài 3, Bài 4)",
             "ĐẠT / DUYỆT (TỐT)",
             "Kế hoạch bài dạy chuẩn bị tốt, đủ 04 tiết đảm bảo 100% tiến độ tháng 9 (Bài 1 đến Bài 4). Thiết kế hoạt động học tập phong phú, kết hợp công cụ số sinh động. Tích hợp Năng lực AI (8.A3.3) tại Bài 1 và Năng lực số (1.2.TC2a) tại Bài 2 đã IN ĐẬM, NGHIÊNG, MÀU TÍM đúng quy định. Duyệt.",
             "16A34A", "F0FDF4"),

            ("Phân môn Tin học 9 (49 trang — 05 tiết: Bài 1, Bài 2, Bài 3, Bài 4)",
             "ĐẠT / DUYỆT (XUẤT SẮC)",
             "Kế hoạch bài dạy soạn rất công phu (49 trang), đạt 05 tiết (đảm bảo 100% tháng 9 và vượt tuần 5 đến hết Bài 4). Ứng dụng công cụ AI (ChatGPT, Gemini, Copilot) làm trợ lý học tập rất sáng tạo, hiện đại. Tích hợp Năng lực số (3.1.TC2a, 1.2.TC2a) và Năng lực AI (9.B2.1, 9.D1.1) khớp Phụ lục 3 và đã IN ĐẬM, NGHIÊNG, MÀU TÍM cực kỳ chuẩn mực. Duyệt.",
             "16A34A", "F0FDF4"),

            ("Nhận xét chung toàn bộ hồ sơ Thầy Dương Quang Tùng (Duyệt theo gói)",
             "DUYỆT - XẾP LOẠI TỐT",
             "DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại Tốt). Hồ sơ giáo án nộp đầy đủ 17 tiết (115 trang PDF) thuộc 4 khối lớp Tin học 6, 7, 8, 9. Đảm bảo 100% tiến độ Tháng 9 và vượt tuần 5 ở khối 9. Tích hợp Năng lực số và AI trong cả 4 khối lớp rất mẫu mực, 100% câu mô tả đều in đậm, nghiêng, màu tím nổi bật và khớp Phụ lục 3. Thể thức và tiến trình CV 5512 chuẩn mực. Biểu dương tinh thần tiên phong ứng dụng công nghệ của thầy Tùng.",
             "16A34A", "F0FDF4"),
        ]

        for sub, status, comment, border_c, bg_c in items_tung:
            p_item = doc.add_paragraph()
            p_item.paragraph_format.space_before = Pt(8)
            p_item.paragraph_format.space_after = Pt(2)
            r_sub = p_item.add_run(f"• {sub}: ")
            r_sub.font.name = "Times New Roman"; r_sub.font.size = Pt(13); r_sub.bold = True

            r_st = p_item.add_run(f"[{status}]")
            r_st.font.name = "Times New Roman"; r_st.font.size = Pt(13); r_st.bold = True
            r_st.font.color.rgb = RGBColor(22, 163, 74)

            # Bảng callout copy-paste
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

    if "## 6. THẦY DƯƠNG QUANG TÙNG" not in sys_md:
        content_tung_md = """
---

## 6. THẦY DƯƠNG QUANG TÙNG (MÔN TIN HỌC 6, 7, 8, 9 — 17 TIẾT, 115 TRANG)

### • Phân môn Tin học 6 (19 trang — 04 tiết: Bài 1, Bài 2): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy chuẩn bị chu đáo, đủ 04 tiết đảm bảo 100% tiến độ 4 tuần tháng 9 theo đúng PPCT (Bài 1: 2 tiết, Bài 2: 2 tiết). Cấu trúc 4 hoạt động CV 5512 rõ ràng. Tích hợp Năng lực số (1.2.TC1a, 5.3.TC1a) và Năng lực AI (6.A1.1) khớp chuẩn Phụ lục 3 và đã IN ĐẬM, NGHIÊNG, MÀU TÍM rất nổi bật theo quy chế chuyên môn. Duyệt.`

### • Phân môn Tin học 7 (23 trang — 04 tiết: Bài 1, Bài 2, Bài 3): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Soạn đủ 04 tiết đúng tiến độ tháng 9 theo PPCT (Bài 1: 1 tiết, Bài 2: 1 tiết, Bài 3: 2 tiết). Tiến trình dạy học mạch lạc, phiếu học tập rõ ràng. Tích hợp Năng lực AI (7.A1.1) và Năng lực số (5.3.TC1a, 1.2.TC1a, 3.1.TC1a) khớp Phụ lục 3 và đã IN ĐẬM, NGHIÊNG, MÀU TÍM chuẩn mực. Duyệt.`

### • Phân môn Tin học 8 (24 trang — 04 tiết: Bài 1, Bài 2, Bài 3, Bài 4): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy chuẩn bị tốt, đủ 04 tiết đảm bảo 100% tiến độ tháng 9 (Bài 1 đến Bài 4). Thiết kế hoạt động học tập phong phú, kết hợp công cụ số sinh động. Tích hợp Năng lực AI (8.A3.3) tại Bài 1 và Năng lực số (1.2.TC2a) tại Bài 2 đã IN ĐẬM, NGHIÊNG, MÀU TÍM đúng quy định. Duyệt.`

### • Phân môn Tin học 9 (49 trang — 05 tiết: Bài 1, Bài 2, Bài 3, Bài 4): [ĐẠT / DUYỆT (XUẤT SẮC)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy soạn rất công phu (49 trang), đạt 05 tiết (đảm bảo 100% tháng 9 và vượt tuần 5 đến hết Bài 4). Ứng dụng công cụ AI (ChatGPT, Gemini, Copilot) làm trợ lý học tập rất sáng tạo, hiện đại. Tích hợp Năng lực số (3.1.TC2a, 1.2.TC2a) và Năng lực AI (9.B2.1, 9.D1.1) khớp Phụ lục 3 và đã IN ĐẬM, NGHIÊNG, MÀU TÍM cực kỳ chuẩn mực. Duyệt.`

### • Nhận xét chung toàn bộ hồ sơ Thầy Dương Quang Tùng (Duyệt theo gói): [DUYỆT - XẾP LOẠI TỐT]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại Tốt). Hồ sơ giáo án nộp đầy đủ 17 tiết (115 trang PDF) thuộc 4 khối lớp Tin học 6, 7, 8, 9. Đảm bảo 100% tiến độ Tháng 9 và vượt tuần 5 ở khối 9. Tích hợp Năng lực số và AI trong cả 4 khối lớp rất mẫu mực, 100% câu mô tả đều in đậm, nghiêng, màu tím nổi bật và khớp Phụ lục 3. Thể thức và tiến trình CV 5512 chuẩn mực. Biểu dương tinh thần tiên phong ứng dụng công nghệ của thầy Tùng.`
"""
        with open(md_sys_path, "a", encoding="utf-8") as f:
            f.write(content_tung_md)
        print("HOÀN THÀNH CẬP NHẬT TÀI LIỆU NỘP HỆ THỐNG MARKDOWN!")

if __name__ == "__main__":
    create_phieu_nhan_xet_tung()
    update_bien_ban_to()
    update_cap_nhat_he_thong()
    print("\n>>> TẤT CẢ TÁC VỤ HOÀN THIỆN HỒ SƠ THẦY DƯƠNG QUANG TÙNG ĐÃ XONG! <<<")
