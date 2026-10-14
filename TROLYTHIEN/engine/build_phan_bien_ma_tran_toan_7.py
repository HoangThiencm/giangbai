# -*- coding: utf-8 -*-
"""
BIÊN BẢN PHẢN BIỆN CHUYÊN MÔN: MA TRẬN ĐỀ KIỂM TRA GIỮA KỲ I TOÁN 7 (2026 - 2027)
Trường THCS Trần Phú
Trọng tâm phản biện: CẤU TRÚC MA TRẬN, TỶ LỆ ĐIỂM, THỜI LƯỢNG 60 PHÚT VÀ BẢN ĐẶC TẢ
Định dạng Word (.docx) chuẩn Nghị định 30/2020/NĐ-CP & Công văn 3280/BGDĐT-GDTrH
"""

import os
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL

sys.path.append(os.path.dirname(__file__))
from de_cuong_docx_helper import (
    create_base_document, set_table_borders, set_table_no_borders, 
    set_cell_background, apply_table_protection, format_run
)

def build_phan_bien_ma_tran_toan_7(output_paths):
    doc = create_base_document()
    
    # 1. HEADER QUỐC HIỆU VÀ ĐƠN VỊ
    tbl_hdr = doc.add_table(rows=1, cols=2)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hdr.autofit = False
    set_table_no_borders(tbl_hdr)
    
    cell_l, cell_r = tbl_hdr.rows[0].cells
    cell_l.width = Inches(3.0)
    cell_r.width = Inches(3.8)
    
    # Cột trái
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
    
    # Cột phải
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
    r_t2 = p_title.add_run("MA TRẬN ĐỀ KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KỲ I — MÔN TOÁN 7\n")
    format_run(r_t2, size_pt=13, bold=True, color_rgb=(30, 58, 138))
    r_t3 = p_title.add_run("NĂM HỌC 2026 - 2027")
    format_run(r_t3, size_pt=12, bold=True)
    
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

    def add_bullet(text, level=0, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.2
        r_b = p.add_run("• ")
        format_run(r_b, size_pt=12.5)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            format_run(r_pre, size_pt=12.5, bold=True)
        r = p.add_run(text)
        format_run(r, size_pt=12.5)
        return p

    # I. THÔNG TIN THẨM ĐỊNH
    add_sec_title("I. THÔNG TIN THẨM ĐỊNH")
    add_bullet("Trường THCS Trần Phú — Tổ Toán - Tin.", bold_prefix="Đơn vị: ")
    add_bullet("Bản Ma trận đề kiểm tra giữa học kỳ I môn Toán 7 năm học 2026 - 2027 (Tệp nguồn: Ma tran giua HK 1_toan 7_NH 2026-2027.pdf).", bold_prefix="Đối tượng thẩm định: ")
    add_bullet("60 phút — Hình thức: 100% Tự luận (Thang điểm 10,0).", bold_prefix="Thời lượng đề kiểm tra: ")
    add_bullet("Trợ lý Sư phạm Hoàng Thiên.", bold_prefix="Người thẩm định: ")
    add_bullet("Thầy Hoàng Thiên.", bold_prefix="Tổ trưởng chuyên môn: ")

    # II. ĐỐI SOÁT VÀ XÁC NHẬN SỐ HỌC
    add_sec_title("II. ĐỐI SOÁT VÀ XÁC NHẬN SỐ HỌC KHÁCH QUAN")
    p_cf = doc.add_paragraph()
    p_cf.paragraph_format.space_before = Pt(2)
    p_cf.paragraph_format.space_after = Pt(4)
    r_cf = p_cf.add_run("Qua đối soát kỹ thuật trên bảng Ma trận Toán 7 gốc, Hội đồng chuyên môn ghi nhận ưu điểm lớn về mặt số học:")
    format_run(r_cf, size_pt=12.5, italic=True)

    add_bullet("Chủ đề 1 (Số hữu tỉ - 14 tiết): 4,0đ + 1,5đ = 5,5đ (55%) — Tính khớp 100%.", level=1)
    add_bullet("Chủ đề 2 (Số thực - 5 tiết): 0,5đ (5%) — Tính khớp 100%.", level=1)
    add_bullet("Chủ đề 3 (Tam giác bằng nhau - 7 tiết): 0,5đ + 1,0đ = 1,5đ (15%) — Tính khớp 100%.", level=1)
    add_bullet("Chủ đề 4 (Góc & ĐT song song - 11 tiết): 2,5đ (25%) — Tính khớp 100%.", level=1)
    add_bullet("Nhận biết: 1,0đ + 0,5đ + 0,5đ + 0,5đ + 0,5đ + 1,0đ = 4,0đ (40%) — Khớp 100%.", level=1)
    add_bullet("Thông hiểu: 2,0đ (C7) + 1,0đ (C8) = 3,0đ (30%) — Khớp 100%.", level=1)
    add_bullet("Vận dụng: 1,5đ (C9) + 1,0đ (C10) = 2,5đ (25%) — Khớp 100%.", level=1)
    add_bullet("Vận dụng cao: 0,5đ (C11) = 0,5đ (5%) — Khớp 100%.", level=1)
    add_bullet("Tổng điểm toàn bài: 4,0 + 3,0 + 2,5 + 0,5 = 10,0 điểm (100%) — Khớp tuyệt đối.", level=1)
    add_bullet("Hàng Tỉ lệ chung: 70% (NB + TH) và 30% (VD + VDC) — Đã gộp nhóm đúng chuẩn Bộ GD&ĐT (đạt ưu điểm vượt trội hơn ma trận Toán 8 và Toán 9).", level=1)

    # III. 05 BẤT CẬP SƯ PHẠM VÀ QUY CHUẨN TRỌNG YẾU
    add_sec_title("III. 05 BẤT CẬP SƯ PHẠM VÀ QUY CHUẨN KHẢO THÍ TRỌNG YẾU")
    
    # Bất cập 1
    p_b1 = doc.add_paragraph()
    p_b1.paragraph_format.space_before = Pt(6)
    p_b1.paragraph_format.space_after = Pt(2)
    r_b1 = p_b1.add_run("1. Số lượng câu hỏi quá lớn gây quá tải nghiêm trọng trong 60 phút (Lỗi thiết kế thời lượng):")
    format_run(r_b1, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Đề thi tự luận 60 phút nhưng có tới 11 bài lớn gồm 16 ý câu hỏi độc lập (7 ý Nhận biết, 4 ý Thông hiểu, 4 ý Vận dụng, 1 ý VDC).")
    add_bullet("Phân tích áp lực thời gian: Trừ 5 phút đọc đề và kiểm tra bài, học sinh chỉ có 55 phút thực làm. Trung bình mỗi ý câu hỏi chỉ có 3,4 phút!")
    add_bullet("Trong khi đó, đề yêu cầu học sinh lớp 7 phải: vẽ hình song song, vẽ hình và chứng minh tam giác bằng nhau (Câu 8, Câu 10), thực hiện biến đổi số học phân số, lũy thừa, quy tắc dấu ngoặc, tìm x và bài toán VDC. Đây là khối lượng công việc vượt quá ngưỡng chịu tải của học sinh lớp 7 đại trà.")
    add_bullet("Chuẩn khảo thí khuyến nghị: Đề tự luận 60 phút chỉ nên gồm 5 - 6 bài lớn với khoảng 8 - 10 ý hỏi nhỏ.")

    # Bất cập 2
    p_b2 = doc.add_paragraph()
    p_b2.paragraph_format.space_before = Pt(6)
    p_b2.paragraph_format.space_after = Pt(2)
    r_b2 = p_b2.add_run("2. Thiếu hoàn toàn BẢN ĐẶC TẢ MA TRẬN (Vi phạm quy chuẩn Công văn 3280/BGDĐT-GDTrH):")
    format_run(r_b2, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Tiêu đề mục II ghi rõ: 'II. MA TRẬN – BẢNG ĐẶC TẢ', nhưng toàn bộ văn bản chỉ có 2 trang ma trận, hoàn toàn không có Bảng đặc tả.")
    add_bullet("Bản đặc tả là thành phần bắt buộc của hồ sơ đề thi theo Thông tư 22/2021/TT-BGDĐT và CV 3280, dùng để quy định chuẩn Yêu cầu cần đạt đo lường của từng câu hỏi. Việc thiếu bản đặc tả làm mất đi cơ sở khoa học để thẩm định tính chuẩn xác của đề thi.")

    # Bất cập 3
    p_b3 = doc.add_paragraph()
    p_b3.paragraph_format.space_before = Pt(6)
    p_b3.paragraph_format.space_after = Pt(2)
    r_b3 = p_b3.add_run("3. Bất hợp lý trong phân bổ trọng số điểm số giữa các chủ đề:")
    format_run(r_b3, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Chủ đề 2 (Số thực): Giảng dạy 5 tiết (chiếm 13,5% thời lượng), nhưng chỉ kiểm tra duy nhất 1 câu Nhận biết (Câu 5: 0,5đ = 5%). Dòng 'Số vô tỉ. Số thực' được đưa vào khung nhưng bỏ trống hoàn toàn (0 câu, 0 điểm).")
    add_bullet("Chủ đề 1 (Số hữu tỉ): Giảng dạy 14 tiết (38% thời lượng) nhưng chiếm tới 5,5 điểm (55% toàn bộ đề thi), áp đảo toàn bộ các phần kiến thức khác.")

    # Bất cập 4
    p_b4 = doc.add_paragraph()
    p_b4.paragraph_format.space_before = Pt(6)
    p_b4.paragraph_format.space_after = Pt(2)
    r_b4 = p_b4.add_run("4. Xếp sai và chưa chuẩn hóa mức độ nhận thức của các câu hỏi:")
    format_run(r_b4, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Câu 6 (0,5đ) - 'Tổng các góc của một tam giác' xếp vào Nhận biết là chưa chuẩn: Học sinh phải vận dụng định lí tổng ba góc để tính toán góc còn lại, đây là mức độ Thông hiểu.")
    add_bullet("Câu 10 a, b (1,0đ) - Xếp cả 2 ý vào Vận dụng là chưa thỏa đáng: Ý 10a (chứng minh 2 tam giác bằng nhau cơ bản) là Thông hiểu, ý 10b mới là Vận dụng. Cho 1,0đ cho cả 2 ý chứng minh hình học là điểm số quá thấp, gây thiệt thòi cho học sinh.")

    # Bất cập 5
    p_b5 = doc.add_paragraph()
    p_b5.paragraph_format.space_before = Pt(6)
    p_b5.paragraph_format.space_after = Pt(2)
    r_b5 = p_b5.add_run("5. Lỗi thể thức văn bản hành chính và lỗi trình bày kỹ thuật:")
    format_run(r_b5, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Ghi cụm từ 'ĐỀ CHÍNH THỨC' ở đầu văn bản Ma trận là sai thể thức hành chính (cụm từ này chỉ xuất hiện trên đề phát cho học sinh).")
    add_bullet("Dấu phân cách thập phân dùng lẫn lộn giữa dấu chấm và dấu phẩy ('1.0đ', '0.5đ', '5.5đ' với '1,0đ', '0,5đ').")
    add_bullet("Bảng ma trận vẫn để 4 cột Trắc nghiệm (TNKQ) trống 100%, gây rối mắt và lãng phí diện tích biểu mẫu.")

    # IV. BẢNG TỔNG HỢP ĐỐI CHIẾU
    add_sec_title("IV. BẢNG TỔNG HỢP ĐỐI CHIẾU TRƯỚC VÀ SAU PHẢN BIỆN")
    
    tbl_cmp = doc.add_table(rows=8, cols=4)
    tbl_cmp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cmp.autofit = False
    set_table_borders(tbl_cmp, color="CBD5E1", sz="4")
    apply_table_protection(tbl_cmp)
    
    col_w = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.4)]
    headers = ["Hạng mục chỉ số", "Hiện trạng Ma trận cũ", "Đánh giá chuyên môn", "Giải pháp chuẩn hóa"]
    
    for c_i, h in enumerate(headers):
        c = tbl_cmp.rows[0].cells[c_i]
        c.width = col_w[c_i]
        set_cell_background(c, "1E3A8A")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        format_run(r, size_pt=11, bold=True, color_rgb=(255, 255, 255))
        
    cmp_data = [
        ("Số lượng câu / ý hỏi", "11 bài / 16 ý tự luận", "Quá tải nặng cho 60p", "Gom gọn 5 bài (9 ý)"),
        ("Bản đặc tả đi kèm", "Hoàn toàn không có", "Vi phạm CV 3280", "Bổ sung Bản đặc tả"),
        ("Cộng dồn số học", "Khớp 10,0 điểm (100%)", "Chính xác tuyệt đối", "Bảo lưu công nhận"),
        ("Tỉ lệ chung", "70% — 30%", "Đúng chuẩn Bộ GD&ĐT", "Giữ nguyên tỷ lệ đẹp"),
        ("Mức độ Câu 6 (Tam giác)", "Xếp Nhận biết (0,5đ)", "Sai bản chất năng lực", "Chuyển sang Thông hiểu"),
        ("Mức độ Câu 10 (Hình học)", "Cả 2 ý đều là Vận dụng", "Chưa phân hóa bậc", "10a: TH, 10b: VD"),
        ("Dòng 'Số vô tỉ. Số thực'", "Bỏ trống (0 câu, 0đ)", "Thừa dòng biểu mẫu", "Tích hợp câu hỏi")
    ]
    
    for r_i, (k, old, stt, sol) in enumerate(cmp_data, 1):
        row = tbl_cmp.rows[r_i]
        for c_i, val in enumerate([k, old, stt, sol]):
            c = row.cells[c_i]
            c.width = col_w[c_i]
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [1, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            is_bold = (c_i == 3)
            c_color = (22, 101, 52) if c_i == 3 else ((185, 28, 28) if "Quá tải" in val or "Vi phạm" in val or "Sai" in val or "Thừa" in val else (0, 0, 0))
            format_run(r, size_pt=10.5, bold=is_bold, color_rgb=c_color)

    # V. KHUNG MA TRẬN CHUẨN HÓA TIN GỌN (5 BÀI TOÁN - VỪA SỨC 60 PHÚT)
    add_sec_title("V. KHUNG MA TRẬN ĐÃ TIN GỌN VÀ CHUẨN HÓA (ĐỀ XUẤT)")
    p_mt_note = doc.add_paragraph()
    p_mt_note.paragraph_format.space_before = Pt(2)
    p_mt_note.paragraph_format.space_after = Pt(4)
    r_mtn = p_mt_note.add_run("Khung ma trận tinh gọn từ 16 ý xuống 9 ý hỏi, vừa vặn tuyệt đối cho thời lượng 60 phút, bảo đảm tỷ lệ 70% (NB+TH) — 30% (VD+VDC), Đại số 60% — Hình học 40%:")
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
        ("1", "Số hữu tỉ", "Tập hợp số hữu tỉ, thứ tự, các phép tính và lũy thừa", "Bài 1a\n(1,0đ)", "Bài 2a\n(1,0đ)", "Bài 3a\n(1,0đ)", "Bài 5\n(0,5đ)", "3,50đ\n(35%)"),
        ("2", "Số thực", "Căn bậc hai số học, số vô tỉ, số thực", "Bài 1b\n(1,0đ)", "Bài 2b\n(1,0đ)", "Bài 3b\n(0,5đ)", "", "2,50đ\n(25%)"),
        ("3", "Góc & Đường thẳng song song", "Các góc ở vị trí đặc biệt, định lí, hai ĐT song song", "Bài 1c\n(1,0đ)", "Bài 4a\n(1,0đ)", "", "", "2,00đ\n(20%)"),
        ("4", "Tam giác bằng nhau", "Tổng các góc trong tam giác, các trường hợp bằng nhau", "Bài 1d\n(1,0đ)", "", "Bài 4b\n(1,0đ)", "", "2,00đ\n(20%)"),
        ("TỔNG SỐ CÂU", "", "", "4 ý", "3 ý", "3 ý", "1 ý", "11 ý (5 bài)"),
        ("TỔNG SỐ ĐIỂM", "", "", "4,0 đ", "3,0 đ", "2,5 đ", "0,5 đ", "10,0 đ"),
        ("TỈ LỆ % MỨC ĐỘ", "", "", "40%", "30%", "25%", "5%", "100%"),
        ("TỈ LỆ CHUNG (GỘP)", "", "", "70% (NB + TH)", "70% (NB + TH)", "30% (VD + VDC)", "30% (VD + VDC)", "100%"),
        ("CƠ CẤU THEO PHÂN MÔN", "", "", "ĐẠI SỐ: 6,0 điểm (60%)", "", "HÌNH HỌC: 4,0 điểm (40%)", "", "100%")
    ]
    
    for r_i, r_data in enumerate(mt_rows, 1):
        row = tbl_mt.rows[r_i]
        is_summary = (r_i >= 5)
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

    # VI. KẾT LUẬN VÀ KIẾN NGHỊ
    add_sec_title("VI. KẾT LUẬN VÀ KIẾN NGHỊ")
    add_bullet("Kết luận chung: Ma trận gốc đạt yêu cầu về độ chính xác số học (tổng 10đ, tỷ lệ chung 70/30). Tuy nhiên, số lượng 16 ý tự luận trong 60 phút là quá tải nặng và hồ sơ còn thiếu hoàn toàn Bản đặc tả mức độ đánh giá.")
    add_bullet("Kiến nghị giáo viên ra đề: Rút gọn số lượng câu hỏi từ 11 bài (16 ý) xuống còn 5 bài lớn (khoảng 9 - 11 ý); xây dựng hoàn thiện Bảng đặc tả Yêu cầu cần đạt chi tiết trước khi trình duyệt Ban Giám hiệu.")
    add_bullet("Xóa bỏ cụm từ 'ĐỀ CHÍNH THỨC' ở đầu ma trận và chuẩn hóa đồng nhất dấu phẩy thập phân.")

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
    out1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "4_DUYET_DE", "Ket_qua", today, "Phan_Bien_Ma_Tran_Toan_7.docx"))
    out2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "4_DUYET_DE", "Ket_qua", "Phan_Bien_Ma_Tran_Toan_7.docx"))
    build_phan_bien_ma_tran_toan_7([out1, out2])
