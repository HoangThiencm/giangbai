# -*- coding: utf-8 -*-
"""
BIÊN BẢN PHẢN BIỆN CHUYÊN MÔN: MA TRẬN ĐỀ KIỂM TRA GIỮA KỲ I TOÁN 8 (2026 - 2027)
Trường THCS Trần Phú - Người soạn: Cô Lê Thị Bình
Trọng tâm phản biện: TỔNG ĐIỂM VÀ TỶ LỆ PHẦN TRĂM
Chuẩn hóa theo Nghị định 30/2020/NĐ-CP & Công văn 3280/BGDĐT-GDTrH
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

def build_phan_bien_ma_tran_toan_8(output_paths):
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
    r_t2 = p_title.add_run("VỀ TỔNG ĐIỂM VÀ TỶ LỆ MA TRẬN ĐỀ KIỂM TRA GIỮA HỌC KỲ I — TOÁN 8\n")
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
    add_bullet("Bản Ma trận và Bản đặc tả đề kiểm tra giữa học kỳ I môn Toán 8 năm học 2026 - 2027 (Tệp nguồn: MT_TOAN8_KiemtraGK_1-2026-2027.pdf; Người soạn: Cô Lê Thị Bình).", bold_prefix="Đối tượng thẩm định: ")
    add_bullet("60 phút — Hình thức: 100% Tự luận (Thang điểm 10,0).", bold_prefix="Thời lượng đề kiểm tra: ")
    add_bullet("Đánh giá toàn diện, chính xác khoa học về cấu trúc tổng điểm, tính toán tỷ lệ phần trăm theo hàng ngang (chủ đề), hàng dọc (mức độ nhận thức) và hàng tỷ lệ chung theo Công văn 3280/BGDĐT-GDTrH.", bold_prefix="Trọng tâm phản biện: ")

    # II. ĐỐI SOÁT VÀ XÁC NHẬN SỐ HỌC
    add_sec_title("II. ĐỐI SOÁT VÀ XÁC NHẬN SỐ HỌC KHÁCH QUAN CỦA MA TRẬN GỐC")
    p_cf = doc.add_paragraph()
    p_cf.paragraph_format.space_before = Pt(2)
    p_cf.paragraph_format.space_after = Pt(4)
    r_cf = p_cf.add_run("Qua đối soát kỹ thuật từng ô dữ liệu trên tệp gốc MT_TOAN8_KiemtraGK_1-2026-2027.pdf, Tổ chuyên môn ghi nhận kết quả số học khách quan như sau:")
    format_run(r_cf, size_pt=12.5, italic=True)

    add_bullet(" Chủ đề 1 (Đa thức): 1,5đ (NB) + 1,5đ (TH) + 0,75đ (VDC) = 3,75đ (37,5%). Tác giả ghi 3,75đ (37,5%) — Hoàn toàn chính xác.", bold_prefix="1. Về tính toán theo từng chủ đề (Cộng hàng ngang):")
    add_bullet("Chủ đề 2 (Hằng đẳng thức đáng nhớ): 1,5đ (NB) + 1,0đ (VD) = 2,5đ (25%). Tác giả ghi 2,5đ 25%) — Đúng số học (chỉ có lỗi gõ phím thiếu ngoặc đơn).", level=1)
    add_bullet("Chủ đề 3.1 (Tứ giác): 0,5đ (TH) = 0,5đ (5%). Tác giả ghi 0,5đ (5%) — Hoàn toàn chính xác.", level=1)
    add_bullet("Chủ đề 3.2 (Tứ giác đặc biệt): 1,0đ (NB) + 0,25đ (TH hình vẽ) + 1,25đ (VD) = 2,5đ (25%). Tác giả ghi 2,5đ (25%) — Hoàn toàn chính xác.", level=1)
    add_bullet("Chủ đề 4 (Định lí Thalès): 0,75đ (TH) = 0,75đ (7,5%). Tác giả ghi 0,75đ (7,5%) — Hoàn toàn chính xác.", level=1)
    add_bullet(" Nhận biết: 1,5 + 1,5 + 1,0 = 4,0đ (40%). Tác giả ghi 4,0 đ | 40% — Đúng 100%.", bold_prefix="2. Về tính toán theo các mức độ nhận thức (Cộng hàng dọc):")
    add_bullet("Thông hiểu: 1,5 + 0,5 + 0,25 + 0,75 = 3,0đ (30%). Tác giả ghi 3,0 đ | 30% — Đúng 100%.", level=1)
    add_bullet("Vận dụng: 1,0 + 1,25 = 2,25đ (22,5%). Tác giả ghi 2,25 đ | 22,5% — Đúng 100%.", level=1)
    add_bullet("Vận dụng cao: 0,75đ (7,5%). Tác giả ghi 0,75 đ | 7,5% — Đúng 100%.", level=1)
    add_bullet("Tổng điểm toàn bài: 4,0 + 3,0 + 2,25 + 0,75 = 10,0 điểm (100%). Tác giả ghi 10 đ | 100% — Đúng 100%.", level=1)

    p_note_audit = doc.add_paragraph()
    p_note_audit.paragraph_format.space_before = Pt(4)
    p_note_audit.paragraph_format.space_after = Pt(4)
    r_na = p_note_audit.add_run("=> KẾT LUẬN ĐỐI SOÁT: Bản ma trận gốc của cô Lê Thị Bình hoàn toàn chính xác về mặt cộng dồn số học đại số thuần túy (không hề có lỗi tính sai 2,5đ thành 20,5% hay 0,75đ thành 7,25% như hiểu nhầm từ lỗi bóc tách văn bản trước đó).")
    format_run(r_na, size_pt=12.5, bold=True, color_rgb=(22, 101, 52))

    # III. 04 BẤT CẬP SƯ PHẠM VÀ QUY CHUẨN TRỌNG YẾU Ở PHẦN TỔNG ĐIỂM VÀ TỶ LỆ
    add_sec_title("III. 04 BẤT CẬP SƯ PHẠM VÀ QUY CHUẨN TRỌNG YẾU Ở PHẦN TỔNG ĐIỂM VÀ TỶ LỆ")
    
    # Bất cập 1
    p_b1 = doc.add_paragraph()
    p_b1.paragraph_format.space_before = Pt(6)
    p_b1.paragraph_format.space_after = Pt(2)
    r_b1 = p_b1.add_run("1. Sai lệch quy cách ở hàng 'Tỉ lệ chung' (Lỗi kỹ thuật văn bản ma trận theo CV 3280):")
    format_run(r_b1, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Theo hướng dẫn xây dựng ma trận chuẩn của Bộ GD&ĐT (Công văn 3280/BGDĐT-GDTrH), hàng 'Tỉ lệ %' đã thể hiện tỷ lệ độc lập của 4 mức độ: 40% (NB) — 30% (TH) — 22,5% (VD) — 7,5% (VDC).")
    add_bullet("Hàng 'Tỉ lệ chung' ở dòng cuối cùng bắt buộc phải GỘP NHÓM THEO 2 KHỐI NĂNG LỰC để phục vụ thống kê đối chiếu:")
    add_bullet("Khối Đạt chuẩn tối thiểu (Nhận biết + Thông hiểu): Bắt buộc gộp ô và thể hiện: 40% + 30% = 70%.", level=1)
    add_bullet("Khối Phân hóa - Nâng cao (Vận dụng + Vận dụng cao): Bắt buộc gộp ô và thể hiện: 22,5% + 7,5% = 30%.", level=1)
    add_bullet("Thực tế trong ma trận gốc: Tác giả lại chép y nguyên 4 ô riêng rẽ của dòng trên: '40% | 30% | 22,5% | 7,5%'. Điều này làm hàng Tỉ lệ chung bị thừa thãi và mất đi ý nghĩa giám sát tỷ lệ phân hóa (70/30) của tổ chuyên môn.")

    # Bất cập 2
    p_b2 = doc.add_paragraph()
    p_b2.paragraph_format.space_before = Pt(6)
    p_b2.paragraph_format.space_after = Pt(2)
    r_b2 = p_b2.add_run("2. Sự 'gượng ép' số học khi đưa 'Hình vẽ bài 4 (0,25đ)' vào ma trận để ép tròn Thông hiểu 30%:")
    format_run(r_b2, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Nếu chỉ tính các bài tập lý thuyết: Bài 2.2 (1,5đ) + Bài 3a (0,5đ) + Bài 3b (0,75đ) = 2,75 điểm (tương ứng 27,5%).")
    add_bullet("Để có con số tròn 3,0 điểm (30%) ở cột Thông hiểu, tác giả đã 'cắt' riêng 0,25đ của 'Hình vẽ bài 4' xếp vào một ô Thông hiểu độc lập trong ma trận.")
    add_bullet("Bất cập đo lường: Kỹ năng vẽ hình là thao tác thực hành đi kèm khi làm bài toán hình học (Bài 4), không phải là một câu hỏi hay Yêu cầu cần đạt chuẩn trong chương trình GDPT 2018. Việc xuất hiện dòng 'Hình vẽ bài 4 (0,25đ)' nằm ngang hàng với câu hỏi chính thức là không đúng bản chất ma trận kiểm tra. Điểm vẽ hình nên được quy định trong Hướng dẫn chấm (vẽ đúng hình câu a được điểm) hoặc tính gộp vào Bài 4a (1,25đ).")

    # Bất cập 3
    p_b3 = doc.add_paragraph()
    p_b3.paragraph_format.space_before = Pt(6)
    p_b3.paragraph_format.space_after = Pt(2)
    r_b3 = p_b3.add_run("3. Tỷ lệ phân hóa bị bẻ lẻ (22,5% - 7,5%) do các bước điểm 0,75đ và 1,25đ:")
    format_run(r_b3, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Đề phân bổ câu Vận dụng cao (Bài 5) là 0,75 điểm (7,5%) và câu Vận dụng là 2,25 điểm (22,5%).")
    add_bullet("Hệ quả sư phạm: Khung tỷ lệ 22,5% - 7,5% là tỷ lệ lẻ thập phân. Mức điểm 0,75đ cho câu VDC là thang điểm tương đối 'lửng lơ' trong đề Toán tự luận THCS (thường là 0,5đ hoặc 1,0đ). Điểm 0,75đ chỉ có đúng 3 bước chia 0,25đ trong barem chấm, quá hẹp để phân loại đa tầng đối với các học sinh khá, giỏi, xuất sắc.")

    # Bất cập 4
    p_b4 = doc.add_paragraph()
    p_b4.paragraph_format.space_before = Pt(6)
    p_b4.paragraph_format.space_after = Pt(2)
    r_b4 = p_b4.add_run("4. Tỷ lệ phân môn Đại số (62,5%) — Hình học (37,5%) bị lẻ và thiếu cân đối giữa các chủ đề hình:")
    format_run(r_b4, size_pt=12.5, bold=True, color_rgb=(185, 28, 28))
    add_bullet("Tổng điểm phân môn: Đại số chiếm 6,25 điểm (62,5%) — Hình học chiếm 3,75 điểm (37,5%). Tỷ lệ 62,5% - 37,5% khiến hệ số điểm thi có đuôi phẩy lẻ.")
    add_bullet("Mất cân đối giữa 2 chương hình học: Chủ đề Tứ giác chiếm tới 3,0 điểm (30%), trong khi toàn bộ Chương III (Định lí Thalès trong tam giác) chỉ có duy nhất 1 câu hỏi Bài 3b với 0,75 điểm (7,5%). Trọng số 7,5% là quá mỏng so với dung lượng giảng dạy của một chương kiến thức trọng tâm.")
    add_bullet("Lỗi chính tả/định dạng: Ô tổng Chủ đề 2 ghi '2,5đ 25%)' thiếu dấu mở ngoặc đơn; ô Bài 2.2 ghi 'Bài 2.2 (1,5)' thiếu chữ 'đ'; phần chân trang bị ngắt bảng ngẫu nhiên làm lặp lại dòng tổng của Chủ đề 1.")

    # IV. BẢNG TỔNG HỢP SO SÁNH & ĐỐI CHIẾU
    add_sec_title("IV. BẢNG TỔNG HỢP ĐỐI CHIẾU VỀ TỔNG ĐIỂM VÀ TỶ LỆ %")
    
    tbl_cmp = doc.add_table(rows=8, cols=4)
    tbl_cmp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cmp.autofit = False
    set_table_borders(tbl_cmp, color="CBD5E1", sz="4")
    apply_table_protection(tbl_cmp)
    
    col_w = [Inches(2.0), Inches(1.8), Inches(1.8), Inches(1.2)]
    headers = ["Hạng mục chỉ số", "Số liệu Ma trận gốc", "Hiện trạng chuyên môn", "Giải pháp chuẩn hóa"]
    
    for c_i, h in enumerate(headers):
        c = tbl_cmp.rows[0].cells[c_i]
        c.width = col_w[c_i]
        set_cell_background(c, "1E3A8A")
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        format_run(r, size_pt=11, bold=True, color_rgb=(255, 255, 255))
        
    cmp_data = [
        ("Cộng dồn điểm số học", "10,0 điểm (100%)", "Khớp số học 100%", "Bảo lưu công nhận"),
        ("Tỉ lệ chung (NB + TH)", "40% | 30% (rời rạc)", "Chưa gộp nhóm theo mẫu", "Gộp thành 70%"),
        ("Tỉ lệ chung (VD + VDC)", "22,5% | 7,5% (rời rạc)", "Chưa gộp nhóm theo mẫu", "Gộp thành 30%"),
        ("Mục Hình vẽ bài 4", "0,25đ (Thông hiểu)", "Gượng ép để đủ 30%", "Gộp vào Bài 4a (1,25đ)"),
        ("Tỉ lệ VD và VDC", "22,5% và 7,5%", "Tỷ lệ lẻ thập phân", "Khuyến nghị 20% - 10%"),
        ("Tỉ lệ Đại số / Hình học", "6,25đ (62,5%) / 3,75đ (37,5%)", "Bị lẻ điểm và tỷ lệ", "Khuyến nghị 6,0đ / 4,0đ"),
        ("Định dạng ô Chủ đề 2", "2,5đ 25%)", "Thiếu mở ngoặc đơn", "Sửa thành '2,5đ (25%)'")
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
            c_color = (22, 101, 52) if c_i == 3 else ((185, 28, 28) if "Chưa" in val or "Thiếu" in val or "Gượng" in val else (0, 0, 0))
            format_run(r, size_pt=10.5, bold=is_bold, color_rgb=c_color)

    # V. BẢNG MA TRẬN CHUẨN HÓA KHỚP 100%
    add_sec_title("V. BẢNG KHUNG MA TRẬN ĐÃ CHUẨN HÓA VỀ TỔNG ĐIỂM VÀ TỶ LỆ")
    p_mt_note = doc.add_paragraph()
    p_mt_note.paragraph_format.space_before = Pt(2)
    p_mt_note.paragraph_format.space_after = Pt(4)
    r_mtn = p_mt_note.add_run("Phương án tối ưu bảo lưu nguyên vẹn 100% đề bài của cô Bình, gộp điểm hình vẽ vào Bài 4a và chuẩn hóa hàng Tỉ lệ chung 70% — 30%:")
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
        ("1", "Đa thức", "Đơn thức, đa thức nhiều biến. Các phép toán cộng, trừ, nhân, chia", "Bài 1.1, 1.2\n(1,5đ)", "Bài 2.2\n(1,5đ)", "", "Bài 5\n(0,75đ)", "3,75đ\n(37,5%)"),
        ("2", "Hằng đẳng thức đáng nhớ", "Hằng đẳng thức đáng nhớ và ứng dụng", "Bài 1.3, 2.1\n(1,5đ)", "", "Bài 2.3\n(1,0đ)", "", "2,50đ\n(25,0%)"),
        ("3", "Tứ giác", "Tổng các góc của một tứ giác", "", "Bài 3a\n(0,5đ)", "", "", "0,50đ\n(5,0%)"),
        ("", "Tứ giác", "Tính chất và dấu hiệu nhận biết các tứ giác đặc biệt", "Bài 4a\n(1,25đ)", "", "Bài 4b, 4c\n(1,25đ)", "", "2,50đ\n(25,0%)"),
        ("4", "Định lí Thalès", "Định lí Thalès và tính độ dài đoạn thẳng", "", "Bài 3b\n(0,75đ)", "", "", "0,75đ\n(7,5%)"),
        ("TỔNG SỐ ĐIỂM", "", "", "4,25 đ", "2,75 đ", "2,25 đ", "0,75 đ", "10,0 đ"),
        ("TỈ LỆ % THEO MỨC ĐỘ", "", "", "42,5%", "27,5%", "22,5%", "7,5%", "100%"),
        ("TỈ LỆ CHUNG (GỘP THEO CV 3280)", "", "", "70,0% (NB + TH)", "70,0% (NB + TH)", "30,0% (VD + VDC)", "30,0% (VD + VDC)", "100%"),
        ("CƠ CẤU THEO PHÂN MÔN", "", "", "ĐẠI SỐ: 6,25 điểm (62,5%)", "", "HÌNH HỌC: 3,75 điểm (37,5%)", "", "100%")
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

    # VI. KIẾN NGHỊ VÀ ĐỀ XUẤT ĐIỀU CHỈNH ĐIỂM
    add_sec_title("VI. KIẾN NGHỊ VÀ ĐỀ XUẤT CỦA HỘI ĐỒNG THẨM ĐỊNH")
    add_bullet("Về mặt số học thuần túy: Ghi nhận sự cẩn trọng của cô Lê Thị Bình, toàn bộ các phép cộng ngang và dọc đã khớp chính xác 10,0 điểm (100%).")
    add_bullet("Về thể thức và quy chuẩn Bộ GD&ĐT: Bắt buộc gộp ô tại hàng Tỉ lệ chung thành 70% (Nhận biết + Thông hiểu) và 30% (Vận dụng + Vận dụng cao); sửa lỗi chính tả '2,5đ (25%)' và đơn vị 'Bài 2.2 (1,5đ)'.")
    add_bullet("Về tính sư phạm đo lường: Loại bỏ dòng 'Hình vẽ bài 4 (0,25đ)' trong bảng ma trận, chuyển toàn bộ 0,25đ này vào Bài 4a (hoặc quy định vào Bareme chấm thi).")
    add_bullet("Đề xuất cơ cấu điểm tối ưu cho kỳ kiểm tra tới: Nên phân bổ Đại số 6,0đ (60%) — Hình học 4,0đ (40%); các mức nhận thức đạt tỷ lệ chẵn 40% (4,0đ) — 30% (3,0đ) — 20% (2,0đ) — 10% (1,0đ) để đề thi đạt chuẩn mực cao nhất, tránh các mức điểm lẻ 0,75đ và 1,25đ gây khó khăn cho việc chấm thi.")

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
    out1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "4_DUYET_DE", "Ket_qua", today, "Phan_Bien_Ma_Tran_Toan_8.docx"))
    out2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "4_DUYET_DE", "Ket_qua", "Phan_Bien_Ma_Tran_Toan_8.docx"))
    build_phan_bien_ma_tran_toan_8([out1, out2])
