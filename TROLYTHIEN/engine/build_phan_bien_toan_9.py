# -*- coding: utf-8 -*-
"""
XUẤT BIÊN BẢN PHẢN BIỆN MA TRẬN TOÁN 9 - GIỮA HỌC KỲ I (NĂM HỌC 2026 - 2027)
Trường THCS Trần Phú - Tổ Toán - Tin
Định dạng Word (.docx) chuẩn Nghị định 30/2020/NĐ-CP & GDPT 2018
"""

import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.path.append(os.path.dirname(__file__))
from de_cuong_docx_helper import (
    create_base_document, set_table_borders, set_table_no_borders, 
    set_cell_background, apply_table_protection, format_run
)

def build_phan_bien_toan_9(output_paths):
    doc = create_base_document()
    
    # 1. HEADER QUỐC HIỆU VÀ ĐƠN VỊ
    tbl_hdr = doc.add_table(rows=1, cols=2)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hdr.autofit = False
    set_table_no_borders(tbl_hdr)
    
    cell_l, cell_r = tbl_hdr.rows[0].cells
    cell_l.width = Inches(2.9)
    cell_r.width = Inches(3.9)
    
    # Cột trái: Đơn vị
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.15
    p_l.paragraph_format.space_before = Pt(0)
    p_l.paragraph_format.space_after = Pt(0)
    r_l1 = p_l.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    format_run(r_l1, size_pt=12, bold=True)
    r_l2 = p_l.add_run("TỔ TOÁN - TIN\n")
    format_run(r_l2, size_pt=12, bold=True)
    r_l3 = p_l.add_run("──────────")
    format_run(r_l3, size_pt=10, bold=True)
    
    # Cột phải: Quốc hiệu
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.15
    p_r.paragraph_format.space_before = Pt(0)
    p_r.paragraph_format.space_after = Pt(0)
    r_r1 = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    format_run(r_r1, size_pt=12, bold=True)
    r_r2 = p_r.add_run("Độc lập - Tự do - Hạnh phúc\n")
    format_run(r_r2, size_pt=12, bold=True)
    r_r3 = p_r.add_run("──────────────────")
    format_run(r_r3, size_pt=10, bold=True)
    
    # Ngày tháng
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_date.paragraph_format.space_before = Pt(8)
    p_date.paragraph_format.space_after = Pt(12)
    r_date = p_date.add_run("Phú Thạnh, ngày 14 tháng 10 năm 2026")
    format_run(r_date, size_pt=12, italic=True)
    
    # TIÊU ĐỀ BIÊN BẢN
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(4)
    r_t1 = p_title.add_run("BIÊN BẢN THẨM ĐỊNH VÀ PHẢN BIỆN CHUYÊN MÔN\n")
    format_run(r_t1, size_pt=14, bold=True, color_rgb=(15, 23, 42))
    r_t2 = p_title.add_run("MA TRẬN ĐỀ KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KỲ I — MÔN TOÁN 9\n")
    format_run(r_t2, size_pt=13, bold=True, color_rgb=(30, 58, 138))
    r_t3 = p_title.add_run("NĂM HỌC 2026 - 2027")
    format_run(r_t3, size_pt=12, bold=True)
    
    # Dải phân cách
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(12)
    r_div = p_div.add_run("◆ ◆ ◆")
    format_run(r_div, size_pt=10, color_rgb=(100, 116, 139))
    
    def add_sec_title(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title_text)
        format_run(r, size_pt=13, bold=True, color_rgb=(30, 58, 138))
        return p

    def add_bullet(text, level=0):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.2
        r = p.add_run("• " + text)
        format_run(r, size_pt=12.5)
        return p

    # PHẦN I: THÔNG TIN CHUNG
    add_sec_title("I. THÔNG TIN CHUNG")
    add_bullet("Thời gian thực hiện: Ngày 14 tháng 10 năm 2026.")
    add_bullet("Địa điểm: Văn phòng Tổ chuyên môn Toán - Tin, Trường THCS Trần Phú.")
    add_bullet("Đối tượng thẩm định: Bản Ma trận đề kiểm tra giữa học kỳ I môn Toán 9 (tệp nguồn: MT_Toan 9_ Kiemtra GK_1.doc).")
    add_bullet("Mục đích thẩm định: Đánh giá tính chính xác khoa học, tính nhất quán về mặt số liệu, tỷ lệ ma trận, sự cân đối các mức độ nhận thức và tính tương thích với định hướng Chương trình GDPT 2018 trước khi ban hành đề kiểm tra chính thức.")

    # PHẦN II: KẾT QUẢ PHẢN BIỆN CHI TIẾT
    add_sec_title("II. KẾT QUẢ THẨM ĐỊNH & PHẢN BIỆN CHI TIẾT (04 LỖI SAI VỀ SỐ LIỆU VÀ TÍNH TOÁN)")
    
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_before = Pt(2)
    p_intro.paragraph_format.space_after = Pt(4)
    r_intro = p_intro.add_run("Qua quá trình thẩm định kỹ thuật và đối soát chéo số học trên bảng Ma trận, Hội đồng thẩm định phát hiện 04 sai sót trọng yếu về mặt tính toán số liệu và tỷ lệ phần trăm cần phải điều chỉnh ngay:")
    format_run(r_intro, size_pt=12.5, italic=True)

    # Lỗi 1
    p_err1 = doc.add_paragraph()
    p_err1.paragraph_format.space_before = Pt(4)
    p_err1.paragraph_format.space_after = Pt(2)
    r_err1 = p_err1.add_run("1. Lỗi vênh điểm và bất khớp số học tại từng chủ đề (Cộng điểm ngang không khớp):")
    format_run(r_err1, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Tại Chủ đề 1.2 (Phương trình & HPT bậc nhất 2 ẩn): Các câu hỏi chi tiết gồm Bài 1.1 (1,0đ - Nhận biết) và Bài 1.3 (1,25đ - Vận dụng). Tổng điểm thực tế là 2,25 điểm (22,5%). Tuy nhiên, ô 'Tổng % điểm' ở cuối hàng lại ghi: '3đ (30%)'. Độ lệch sai số là 0,75 điểm.")
    add_bullet("Tại Chủ đề 3 (Hệ thức lượng trong tam giác vuông): Các câu hỏi chi tiết gồm Bài 3.1 (1,0đ) + Bài 3.2 (1,0đ) + Bài 3.3 (1,0đ) + Bài 4 (0,75đ). Tổng điểm thực tế là 3,75 điểm (37,5%). Tuy nhiên, ô 'Tổng % điểm' cuối hàng lại ghi: '3đ (30%)'. Độ lệch sai số là 0,75 điểm.")

    # Lỗi 2
    p_err2 = doc.add_paragraph()
    p_err2.paragraph_format.space_before = Pt(4)
    p_err2.paragraph_format.space_after = Pt(2)
    r_err2 = p_err2.add_run("2. Lỗi đánh máy sai số học ở hàng Tỉ lệ % (Row 10):")
    format_run(r_err2, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Mức độ Vận dụng có tổng điểm là 2,25 điểm trên thang điểm 10,0. Do đó, tỉ lệ phần trăm chính xác bắt buộc phải là 22,5%.")
    add_bullet("Trong bảng ma trận, tác giả đã gõ nhầm dấu phẩy thành: '2,25%' (hai phẩy hai mươi lăm phần trăm).")
    add_bullet("Hệ quả: Khi cộng tổng hàng phần trăm: 40% (NB) + 30% (TH) + 2,25% (VD) + 7,5% (VDC) = 79,75%, hoàn toàn mâu thuẫn với con số 100% được ghi ở ô tổng cộng cuối bảng.")

    # Lỗi 3
    p_err3 = doc.add_paragraph()
    p_err3.paragraph_format.space_before = Pt(4)
    p_err3.paragraph_format.space_after = Pt(2)
    r_err3 = p_err3.add_run("3. Lỗi mâu thuẫn toán học tại hàng Tỉ lệ chung (Row 11):")
    format_run(r_err3, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Cột gộp mức độ (Nhận biết + Thông hiểu): Bảng ghi '65%', trong khi số liệu cộng thực tế từ trên xuống là 40% + 30% = 70% (Sai lệch 5%).")
    add_bullet("Cột gộp mức độ (Vận dụng + Vận dụng cao): Bảng ghi '35%', trong khi số liệu cộng thực tế là 22,5% + 7,5% = 30% (Sai lệch 5%).")
    add_bullet("Nguyên nhân: Người soạn thảo sao chép khung tỷ lệ 65% - 35% từ biểu mẫu khác nhưng lại không tính toán lại theo số điểm phân bổ thực tế của đề thi.")

    # Lỗi 4
    p_err4 = doc.add_paragraph()
    p_err4.paragraph_format.space_before = Pt(4)
    p_err4.paragraph_format.space_after = Pt(2)
    r_err4 = p_err4.add_run("4. Lỗi đếm số câu ở hàng Tổng số câu (Row 8):")
    format_run(r_err4, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Tại cột Vận dụng (VD): Cả bảng chỉ có 02 câu là Bài 1.3 và Bài 3.3, nhưng ô tổng kết lại ghi là '3 câu'.")
    add_bullet("Khi cộng tổng số câu theo hàng ngang: 4 (NB) + 3 (TH) + 3 (VD) + 1 (VDC) = 11 câu, nhưng ô tổng cuối hàng lại ghi '10 câu' (mâu thuẫn 11 ≠ 10).")

    # Ghi nhận về cấu trúc
    p_str = doc.add_paragraph()
    p_str.paragraph_format.space_before = Pt(6)
    p_str.paragraph_format.space_after = Pt(2)
    r_str = p_str.add_run("(*) Về cấu trúc phân bổ câu hỏi và cách đánh số bài tập:")
    format_run(r_str, size_pt=12.5, bold=True, color_rgb=(15, 23, 42))
    add_bullet("Cách phân bổ câu hỏi thành Bài 1 (1.1, 1.2 a,c; 1.2 b; 1.3), Bài 2 (2.1, 2.2), Bài 3 (3.1, 3.2, 3.3, 3.4) và Bài 4 là hoàn toàn bình thường, phù hợp với thói quen ra đề kiểm tra thực tế tại các trường THCS (gom nhóm biến đổi đại số và hình học liên hoàn). Do đó, cách bố trí và mã hóa câu hỏi này được giữ nguyên vẹn 100%, chỉ chuẩn hóa lại điểm số và tỷ lệ phần trăm tương ứng.")

    # PHẦN III: BẢNG ĐỐI CHIẾU
    add_sec_title("III. BẢNG TỔNG HỢP ĐỐI CHIẾU TRƯỚC VÀ SAU PHẢN BIỆN")
    
    tbl_cmp = doc.add_table(rows=8, cols=4)
    tbl_cmp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cmp.autofit = False
    set_table_borders(tbl_cmp, color="CBD5E1", sz="4")
    apply_table_protection(tbl_cmp)
    
    col_w = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.4)]
    headers = ["Nội dung / Chỉ số kiểm tra", "Số liệu trong Ma trận cũ", "Số liệu sau Phản biện", "Đánh giá"]
    
    for c_i, h in enumerate(headers):
        c = tbl_cmp.rows[0].cells[c_i]
        c.width = col_w[c_i]
        set_cell_background(c, "1E3A8A")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        format_run(r, size_pt=11.5, bold=True, color_rgb=(255, 255, 255))
        
    cmp_data = [
        ("Tổng điểm Chủ đề 1.2", "3,0đ (30%)", "2,25đ (22,5%)", "Đã khớp 100%"),
        ("Tổng điểm Chủ đề 3", "3,0đ (30%)", "3,75đ (37,5%)", "Đã khớp 100%"),
        ("Tỉ lệ % Vận dụng", "2,25% (gõ sai)", "22,5%", "Đã sửa chuẩn"),
        ("Tổng % cả bảng", "79,75% (mâu thuẫn)", "100%", "Đã khớp chuẩn"),
        ("Tỉ lệ chung (NB + TH)", "65% (tính sai)", "70%", "Khớp chuẩn GDPT"),
        ("Tỉ lệ chung (VD + VDC)", "35% (tính sai)", "30%", "Khớp chuẩn GDPT"),
        ("Số câu hỏi Vận dụng", "3 câu (đếm sai)", "2 câu", "Đã đếm đúng")
    ]
    
    for r_i, (k, old, new, stt) in enumerate(cmp_data, 1):
        row = tbl_cmp.rows[r_i]
        for c_i, val in enumerate([k, old, new, stt]):
            c = row.cells[c_i]
            c.width = col_w[c_i]
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if c_i in [1, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            is_bold = (c_i == 2 or c_i == 3)
            c_color = (22, 101, 52) if c_i == 3 else ((185, 28, 28) if c_i == 1 and 'sai' in val else (0, 0, 0))
            format_run(r, size_pt=11, bold=is_bold, color_rgb=c_color)

    # PHẦN IV: BẢNG MA TRẬN CHUẨN HÓA HOÀN CHỈNH
    add_sec_title("IV. BẢNG MA TRẬN ĐỀ KIỂM TRA ĐÃ CHUẨN HÓA KHỚP 100%")
    p_mt_note = doc.add_paragraph()
    p_mt_note.paragraph_format.space_before = Pt(2)
    p_mt_note.paragraph_format.space_after = Pt(6)
    r_mtn = p_mt_note.add_run("Ma trận dưới đây giữ nguyên vẹn 100% cấu trúc câu hỏi của tác giả, đã khắc phục triệt để mọi lỗi số học và chuẩn hóa tỷ lệ 70% (NB+TH) — 30% (VD+VDC):")
    format_run(r_mtn, size_pt=12, italic=True)

    tbl_mt = doc.add_table(rows=10, cols=8)
    tbl_mt.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_mt.autofit = False
    set_table_borders(tbl_mt, color="CBD5E1", sz="4")
    apply_table_protection(tbl_mt)
    
    mt_w = [Inches(0.4), Inches(1.8), Inches(1.8), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.8)]
    mt_headers = ["TT", "Chương / Chủ đề", "Nội dung / Đơn vị kiến thức", "Nhận biết", "Thông hiểu", "Vận dụng", "VDC", "Tổng điểm"]
    
    for c_i, h in enumerate(mt_headers):
        c = tbl_mt.rows[0].cells[c_i]
        c.width = mt_w[c_i]
        set_cell_background(c, "0F172A")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        format_run(r, size_pt=11, bold=True, color_rgb=(255, 255, 255))
        
    mt_rows = [
        ("1", "Phương trình & Hệ phương trình", "Phương trình quy về PT bậc nhất một ẩn", "", "Bài 1.2 a, c\n(1,0đ)", "", "", "1,0đ\n(10%)"),
        ("", "Phương trình & Hệ phương trình", "Phương trình & Hệ PT bậc nhất hai ẩn", "Bài 1.1\n(1,0đ)", "", "Bài 1.3\n(1,25đ)", "", "2,25đ\n(22,5%)"),
        ("2", "Bất đẳng thức & Bất phương trình", "Bất đẳng thức & Bất phương trình bậc nhất 1 ẩn", "Bài 2.1\n(1,0đ)", "Bài 1.2 b (0,5đ)\nBài 2.2 (0,5đ)", "", "", "2,0đ\n(20%)"),
        ("3", "Hệ thức lượng trong tam giác vuông", "Tỉ số lượng giác góc nhọn & Hệ thức cạnh - góc", "Bài 3.1\n(1,0đ)", "Bài 3.2\n(1,0đ)", "Bài 3.3\n(1,0đ)", "Bài 4\n(0,75đ)", "3,75đ\n(37,5%)"),
        ("4", "Đường tròn", "Đường tròn, cung và dây của đường tròn", "Bài 3.4\n(1,0đ)", "", "", "", "1,0đ\n(10%)"),
        ("TỔNG SỐ CÂU", "", "", "4 câu", "3 câu", "2 câu", "1 câu", "10 câu"),
        ("TỔNG SỐ ĐIỂM", "", "", "4,0 đ", "3,0 đ", "2,25 đ", "0,75 đ", "10,0 đ"),
        ("TỈ LỆ % TỪNG MỨC ĐỘ", "", "", "40%", "30%", "22,5%", "7,5%", "100%"),
        ("TỈ LỆ CHUNG (GỘP)", "", "", "70% (NB + TH)", "70% (NB + TH)", "30% (VD + VDC)", "30% (VD + VDC)", "100%")
    ]
    
    for r_i, r_data in enumerate(mt_rows, 1):
        row = tbl_mt.rows[r_i]
        is_summary = (r_i >= 6)
        for c_i, val in enumerate(r_data):
            c = row.cells[c_i]
            c.width = mt_w[c_i]
            if is_summary:
                set_cell_background(c, "F1F5F9" if r_i % 2 == 0 else "E2E8F0")
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_i != 1 and c_i != 2) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            format_run(r, size_pt=10.5 if not is_summary else 11, bold=is_summary)

    # PHẦN V: KIẾN NGHỊ & KẾT LUẬN
    add_sec_title("V. KẾT LUẬN VÀ KIẾN NGHỊ CỦA TỔ CHUYÊN MÔN")
    add_bullet("Kết luận: Ma trận đề kiểm tra Giữa học kỳ I môn Toán 9 trong tệp gốc chưa đạt yêu cầu do còn 04 lỗi sai về số học, vênh điểm và tỷ lệ phần trăm. Bắt buộc phải điều chỉnh số liệu theo đúng Bảng Ma trận đã chuẩn hóa tại Mục IV của Biên bản này.")
    add_bullet("Kiến nghị giáo viên ra đề: Cập nhật lại Bảng đặc tả chi tiết đảm bảo ăn khớp 1-1 với ma trận chuẩn về số điểm và tỷ lệ phần trăm; giữ nguyên vẹn cấu trúc đánh số và phân bổ các câu hỏi quen thuộc của giáo viên.")
    add_bullet("Thời lượng đề thi: Đề nghị giáo viên rà soát độ dài của 10 câu tự luận để đảm bảo học sinh có đủ thời gian hoàn thành bài kiểm tra trong thời lượng 60 phút.")

    # CHỮ KÝ XÁC NHẬN
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig.autofit = False
    set_table_no_borders(tbl_sig)
    
    s_l, s_r = tbl_sig.rows[0].cells
    s_l.width = Inches(3.4)
    s_r.width = Inches(3.4)
    
    p_sl = s_l.paragraphs[0]
    p_sl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sl1 = p_sl.add_run("NGƯỜI THẨM ĐỊNH\n")
    format_run(r_sl1, size_pt=12, bold=True)
    r_sl2 = p_sl.add_run("(Ký và ghi rõ họ tên)\n\n\n\n")
    format_run(r_sl2, size_pt=11, italic=True)
    r_sl3 = p_sl.add_run("Trợ lý Sư phạm Hoàng Thiên")
    format_run(r_sl3, size_pt=12, bold=True)
    
    p_sr = s_r.paragraphs[0]
    p_sr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sr1 = p_sr.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n")
    format_run(r_sr1, size_pt=12, bold=True)
    r_sr2 = p_sr.add_run("(Ký và ghi rõ họ tên)\n\n\n\n")
    format_run(r_sr2, size_pt=11, italic=True)
    r_sr3 = p_sr.add_run("Thầy Hoàng Thiên")
    format_run(r_sr3, size_pt=12, bold=True)

    for out_p in output_paths:
        os.makedirs(os.path.dirname(out_p), exist_ok=True)
        doc.save(out_p)
        print(f"Đã lưu thành công tệp: {out_p}")

if __name__ == "__main__":
    today = datetime.datetime.now().strftime("%d.%m")
    out1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "4_DUYET_DE", "Ket_qua", today, "Phan_Bien_Toan_9.docx"))
    out2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "4_DUYET_DE", "Ket_qua", "Phan_Bien_Toan_9.docx"))
    build_phan_bien_toan_9([out1, out2])
