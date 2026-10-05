import os
import sys
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

sys.stdout.reconfigure(encoding='utf-8')

# --- XML Helper Functions ---
def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def format_cell(cell, text, bold=False, italic=False, font_size=11, align=WD_ALIGN_PARAGRAPH.LEFT, color_rgb=(0,0,0)):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    for run in p.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

def add_callout(doc, text, title="GHI CHÚ / LƯU Ý:", border_color="DC2626", bg_color="FEF2F2"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=150)
    set_cell_shading(cell, bg_color)
    
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(f"👉 {title} ")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(11)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(11)
    r_txt.font.color.rgb = RGBColor(51, 65, 85)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def safe_save_doc(doc, target_path):
    try:
        doc.save(target_path)
        print(f"SUCCESS: Saved {os.path.basename(target_path)}")
        return target_path
    except PermissionError:
        base, ext = os.path.splitext(target_path)
        fallback_path = f"{base}_CapNhat{ext}"
        doc.save(fallback_path)
        print(f"WARNING: File locked! Saved to fallback: {os.path.basename(fallback_path)}")
        return fallback_path

print("Starting status update to TRẢ HỒ SƠ for Cô Thảo and Cô Bình...")

# ==============================================================================
# 1. CẬP NHẬT BIÊN BẢN KIỂM TRA TỔ (Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.docx)
# ==============================================================================
def update_bien_ban():
    path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.docx"
    doc = docx.Document(path)
    
    # Update table
    for t in doc.tables:
        if len(t.rows) > 0 and len(t.columns) == 6 and "họ và tên" in t.rows[0].cells[1].text.lower():
            for r in t.rows:
                name = r.cells[1].text.lower()
                if "nguyễn thị thảo" in name:
                    format_cell(r.cells[4], "Đủ 34 tiết; Lỗi font ký hiệu góc nặng ở Hình 7", font_size=10)
                    format_cell(r.cells[5], "TRẢ HỒ SƠ (Sửa lỗi ký hiệu)", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=(220, 38, 38))
                elif "lê thị bình" in name:
                    format_cell(r.cells[4], "Đủ 45 tiết; Lỗi font công thức góc ở Hình 8, 7", font_size=10)
                    format_cell(r.cells[5], "TRẢ HỒ SƠ (Sửa lỗi ký hiệu)", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=(220, 38, 38))

    # Update paragraph descriptions
    for p in doc.paragraphs:
        if "3. Giáo viên: NGUYỄN THỊ THẢO" in p.text:
            p.text = (
                "3. Giáo viên: NGUYỄN THỊ THẢO (Môn Toán 6, Toán 7)\n"
                "• Ưu điểm: Hồ sơ giáo án chuẩn bị đủ 34 tiết (123 trang), tiến độ đạt 100% tháng 9 và vượt tuần 5. Số học 6 tích hợp NLS in đậm nghiêng rất chuẩn.\n"
                "• Tồn tại, hạn chế: Phân môn Hình học 7 bị lỗi font ký hiệu góc rất nặng và phản cảm: các góc hiển thị thành dấu chấm trên đầu chữ cái (ẋOz, ẏOz, ṁBy, ẋAB...) và ký hiệu góc O1, O2, M1, M2 bị chèn ký tự rác vuông/perpendicular đè lên đỉnh, không đạt chuẩn mực sư phạm.\n"
                "• Kết luận thẩm định: TRẢ HỒ SƠ (Yêu cầu chỉnh sửa chuẩn hóa toàn bộ ký hiệu góc trong Hình học 7 nộp lại tổ chuyên môn)."
            )
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11)
        elif "5. Thẩm định hồ sơ giáo viên: LÊ THỊ BÌNH" in p.text:
            p.text = (
                "5. Thẩm định hồ sơ giáo viên: LÊ THỊ BÌNH (Môn Toán 7, Toán 8, HĐTN 7)\n"
                "• Ưu điểm: Khối lượng giáo án rất lớn (178 trang, 45 tiết), đủ 100% tiến độ tháng 9. HĐTN 7 và Đại số 8 tích hợp NLS/AI in đậm nghiêng rất xuất sắc.\n"
                "• Tồn tại, hạn chế: Phân môn Hình học 8 (Bài 10: Tứ giác, Luyện tập 2) và Hình học 7 bị lỗi font công thức toán học nghiêm trọng: toàn bộ dấu mũ góc bị hiển thị thành các ký tự rác đè lên đỉnh chữ (D┴, A┴, B┴, C┴, H┴, E┴, F┴, G┴...), sai chuẩn mực trình bày toán học, không thể lưu hành phục vụ giảng dạy.\n"
                "• Kết luận thẩm định: TRẢ HỒ SƠ (Yêu cầu sửa lại triệt để font công thức và ký hiệu góc trong Hình học 8, Hình học 7 nộp lại tổ chuyên môn)."
            )
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11)

    safe_save_doc(doc, path)

update_bien_ban()

# ==============================================================================
# 2. CẬP NHẬT TỆP NHẬN XÉT HỆ THỐNG (Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.docx)
# ==============================================================================
def update_system_comments_docx():
    path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.docx"
    doc = docx.Document(path)
    
    # Update headers
    for p in doc.paragraphs:
        if "Phân môn Hình học 7 (30 trang" in p.text and "THẢO" in p.text or "Phân môn Hình học 7 (30 trang — 08 tiết: Bài 8, 9, LTC, Bài 10):" in p.text:
            p.text = "• Phân môn Hình học 7 (30 trang — 08 tiết: Bài 8, 9, LTC, Bài 10): [KHÔNG DUYỆT / TRẢ HỒ SƠ (LỖI FONT GÓC)]"
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11.5); r.bold = True
        elif "Nhận xét chung toàn bộ hồ sơ Cô Nguyễn Thị Thảo (Duyệt theo gói):" in p.text:
            p.text = "• Nhận xét chung toàn bộ hồ sơ Cô Nguyễn Thị Thảo (Duyệt theo gói): [TRẢ HỒ SƠ (LỖI KÝ HIỆU GÓC HÌNH 7)]"
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11.5); r.bold = True
        elif "Phân môn Hình học 8 (52 trang — 08 tiết" in p.text:
            p.text = "• Phân môn Hình học 8 (52 trang — 08 tiết: Bài 10, 11, LTC, Bài 12, LTC): [KHÔNG DUYỆT / TRẢ HỒ SƠ (LỖI FONT CÔNG THỨC)]"
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11.5); r.bold = True
        elif "Nhận xét chung toàn bộ hồ sơ Cô Lê Thị Bình (Duyệt theo gói):" in p.text:
            p.text = "• Nhận xét chung toàn bộ hồ sơ Cô Lê Thị Bình (Duyệt theo gói): [TRẢ HỒ SƠ (LỖI FONT CÔNG THỨC HÌNH HỌC)]"
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11.5); r.bold = True

    # Update callout contents
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                # Thao Hinh 7
                if "ĐÍNH CHÍNH KÝ HIỆU GÓC" in c.text or "hiển thị thành dấu chấm trên đầu chữ cái như ṁBy" in c.text:
                    p = c.paragraphs[0]
                    p.text = "👉 Nhận xét hệ thống (Copy & Paste): TRẢ HỒ SƠ. Kế hoạch bài dạy Hình học 7 bị lỗi font ký hiệu góc rất nặng và biến dạng toán học: các góc bị hiển thị thành dấu chấm trên đầu chữ cái (ẋOz, ẏOz, ṁBy, ẋAB...) và góc O1, O2, M1, M2 bị ký tự rác chèn đè lên đỉnh chữ. Đề nghị cô Thảo chuẩn hóa toàn bộ công thức và ký hiệu dấu mũ góc chuẩn xác trước khi trình duyệt lại."
                    p.runs[0].font.name = "Times New Roman"; p.runs[0].font.size = Pt(11)
                # Thao overall
                elif "DUYỆT HỒ SƠ (Xếp loại Khá). Hồ sơ nộp đầy đủ 34 tiết" in c.text:
                    p = c.paragraphs[0]
                    p.text = "👉 Nhận xét hệ thống (Copy & Paste): TRẢ HỒ SƠ. Số học 6 và Đại số 7 soạn tốt, nhưng phân môn Hình học 7 bị lỗi font ký hiệu góc rất phản cảm và sai chuẩn mực toán học (dấu chấm trên đầu đỉnh góc và ký tự lạ đè lên chữ). Đề nghị cô Thảo khắc phục triệt để lỗi ký hiệu góc trong Hình học 7 và nộp lại để tổ chuyên môn phê duyệt."
                    p.runs[0].font.name = "Times New Roman"; p.runs[0].font.size = Pt(11)
                # Binh Hinh 8
                elif "Khắc phục hoàn toàn lỗi toán học" in c.text and "Lê Thị Bình" not in c.text:
                    p = c.paragraphs[0]
                    p.text = "👉 Nhận xét hệ thống (Copy & Paste): TRẢ HỒ SƠ. Kế hoạch bài dạy Hình học 8 bị lỗi font công thức toán học nghiêm trọng tại Bài 10 (Tứ giác) và Luyện tập 2: toàn bộ dấu mũ góc bị biến dạng thành các ký tự vuông/rác đè lên đỉnh chữ cái (D┴, A┴, B┴, C┴, H┴, E┴, F┴, G┴...), sai chuẩn mực sư phạm. Đề nghị cô Bình chuẩn hóa lại toàn bộ MathType/Equation ký hiệu góc chuẩn xác rồi nộp lại."
                    p.runs[0].font.name = "Times New Roman"; p.runs[0].font.size = Pt(11)
                # Binh overall
                elif "DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại Tốt). Giáo án chuẩn bị rất công phu (178 trang" in c.text:
                    p = c.paragraphs[0]
                    p.text = "👉 Nhận xét hệ thống (Copy & Paste): TRẢ HỒ SƠ. Môn HĐTN 7 và Đại số 7, Đại số 8 chuẩn bị rất công phu, NLS/AI mẫu mực. Tuy nhiên phân môn Hình học 8 và Hình học 7 bị lỗi font công thức toán học nghiêm trọng (dấu mũ góc biến dạng thành ký tự rác đè lên mặt chữ cái tại phần tính góc tứ giác). Đề nghị cô Bình sửa lại toàn bộ công thức toán học bị lỗi font và nộp lại tổ chuyên môn."
                    p.runs[0].font.name = "Times New Roman"; p.runs[0].font.size = Pt(11)

    safe_save_doc(doc, path)

update_system_comments_docx()

# ==============================================================================
# 3. TẠO LẠI PHIẾU NHẬN XÉT CÁ NHÂN CÔ THẢO (TRẢ HỒ SƠ)
# ==============================================================================
def create_personal_thao_tra_ho_so():
    doc = docx.Document()
    for s in doc.sections:
        s.page_width = Inches(8.27); s.page_height = Inches(11.69)
        s.top_margin = Inches(0.59); s.bottom_margin = Inches(0.59)
        s.left_margin = Inches(0.79); s.right_margin = Inches(0.59)
        
    # National header
    tbl_h = doc.add_table(rows=1, cols=2); tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl_h.cell(0, 0); c1 = tbl_h.cell(0, 1)
    set_cell_margins(c0, 0, 0, 0, 0); set_cell_margins(c1, 0, 0, 0, 0)
    
    p0 = c0.paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p0.add_run("TRƯỜNG THCS TRẦN PHÚ\nTỔ TOÁN – TIN\n"); r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.bold = True
    r = p0.add_run("Số: 03/PĐG-TT"); r.font.name = "Times New Roman"; r.font.size = Pt(10); r.italic = True
    
    p1 = c1.paragraphs[0]; p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p1.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n"); r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.bold = True
    r = p1.add_run("Xuân Đông, ngày 05 tháng 10 năm 2026"); r.font.name = "Times New Roman"; r.font.size = Pt(10); r.italic = True
    
    p_title = doc.add_paragraph(); p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14); p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run("PHIẾU NHẬN XÉT, THẨM ĐỊNH HỒ SƠ BÀI DẠY\n(DUYỆT GIÁO ÁN THÁNG 9/2026)")
    r_t.font.name = "Times New Roman"; r_t.font.size = Pt(14); r_t.bold = True; r_t.font.color.rgb = RGBColor(185, 28, 28)
    
    p_info = doc.add_paragraph(); p_info.paragraph_format.line_spacing = 1.2
    p_info.add_run("• Họ và tên giáo viên: ").bold = True; p_info.add_run("NGUYỄN THỊ THẢO\n")
    p_info.add_run("• Môn giảng dạy: ").bold = True; p_info.add_run("Toán 6, Toán 7 (123 trang PDF, 34 tiết)\n")
    p_info.add_run("• Kết luận kiểm tra: ").bold = True
    r = p_info.add_run("TRẢ HỒ SƠ (Yêu cầu sửa lỗi ký hiệu góc Hình học 7)\n"); r.bold = True; r.font.color.rgb = RGBColor(220, 38, 38)

    p_s2 = doc.add_paragraph(); p_s2.paragraph_format.space_before = Pt(6)
    r = p_s2.add_run("CHI TIẾT LỖI SAI SÓT YÊU CẦU KHẮC PHỤC:"); r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True; r.font.color.rgb = RGBColor(185, 28, 28)
    
    p_obs = doc.add_paragraph(); p_obs.paragraph_format.line_spacing = 1.25
    p_obs.add_run("1. Ưu điểm: ").bold = True
    p_obs.add_run("Đảm bảo đủ 34 tiết đúng tiến độ 4 tuần tháng 9; phân môn Số học 6 và Đại số 7 chuẩn bị công phu, có tích hợp NLS in đậm nghiêng đúng quy định.\n\n")
    p_obs.add_run("2. Lỗi nghiêm trọng cần khắc phục: ").bold = True
    p_obs.add_run(
        "• Phân môn Hình học 7 (Bài 8: Góc ở vị trí đặc biệt, tia phân giác) bị lỗi font ký hiệu góc nghiêm trọng trên toàn bộ bài dạy.\n"
        "• Ký hiệu góc bị lỗi thành dấu chấm trên đầu chữ cái: ẋOz = 135°, ẏOz = 45°, ṁBy, ẋAB...\n"
        "• Các góc O1, O2, M1, M2 bị lỗi font chèn ký tự lạ/rác đè lên mặt chữ cái, gây biến dạng công thức toán học và phản cảm về mặt sư phạm.\n"
    )
    
    add_callout(doc, 
                "Tổ chuyên môn quyết định TRẢ HỒ SƠ. Đề nghị cô Nguyễn Thị Thảo rà soát lại toàn bộ công thức và ký hiệu góc trong phân môn Hình học 7, sử dụng MathType hoặc công cụ Equation chuẩn của Word để hiển thị đúng dấu mũ góc trước khi nộp lại phê duyệt.",
                title="KẾT LUẬN & YÊU CẦU:", border_color="DC2626", bg_color="FEF2F2")

    # Signature
    tbl_sig = doc.add_table(rows=1, cols=2); tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl_sig.cell(0, 0); c1 = tbl_sig.cell(0, 1)
    set_cell_margins(c0, 100, 0, 0, 0); set_cell_margins(c1, 100, 0, 0, 0)
    p0 = c0.paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p0.add_run("GIÁO VIÊN BỘ MÔN\n\n\n\n\nNguyễn Thị Thảo"); r.bold = True
    p1 = c1.paragraphs[0]; p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p1.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n\n\n\n\nHoàng Tấn Thiên"); r.bold = True

    p_doc = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_Nguyen_Thi_Thao_Thang_9.docx"
    safe_save_doc(doc, p_doc)

create_personal_thao_tra_ho_so()

# ==============================================================================
# 4. TẠO LẠI PHIẾU NHẬN XÉT CÁ NHÂN CÔ BÌNH (TRẢ HỒ SƠ)
# ==============================================================================
def create_personal_binh_tra_ho_so():
    doc = docx.Document()
    for s in doc.sections:
        s.page_width = Inches(8.27); s.page_height = Inches(11.69)
        s.top_margin = Inches(0.59); s.bottom_margin = Inches(0.59)
        s.left_margin = Inches(0.79); s.right_margin = Inches(0.59)
        
    # National header
    tbl_h = doc.add_table(rows=1, cols=2); tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl_h.cell(0, 0); c1 = tbl_h.cell(0, 1)
    set_cell_margins(c0, 0, 0, 0, 0); set_cell_margins(c1, 0, 0, 0, 0)
    
    p0 = c0.paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p0.add_run("TRƯỜNG THCS TRẦN PHÚ\nTỔ TOÁN – TIN\n"); r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.bold = True
    r = p0.add_run("Số: 05/PĐG-TT"); r.font.name = "Times New Roman"; r.font.size = Pt(10); r.italic = True
    
    p1 = c1.paragraphs[0]; p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p1.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n"); r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.bold = True
    r = p1.add_run("Xuân Đông, ngày 05 tháng 10 năm 2026"); r.font.name = "Times New Roman"; r.font.size = Pt(10); r.italic = True
    
    p_title = doc.add_paragraph(); p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14); p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run("PHIẾU NHẬN XÉT, THẨM ĐỊNH HỒ SƠ BÀI DẠY\n(DUYỆT GIÁO ÁN THÁNG 9/2026)")
    r_t.font.name = "Times New Roman"; r_t.font.size = Pt(14); r_t.bold = True; r_t.font.color.rgb = RGBColor(185, 28, 28)
    
    p_info = doc.add_paragraph(); p_info.paragraph_format.line_spacing = 1.2
    p_info.add_run("• Họ và tên giáo viên: ").bold = True; p_info.add_run("LÊ THỊ BÌNH\n")
    p_info.add_run("• Môn giảng dạy: ").bold = True; p_info.add_run("Toán 7, Toán 8, HĐTN 7 (178 trang PDF, 45 tiết)\n")
    p_info.add_run("• Kết luận kiểm tra: ").bold = True
    r = p_info.add_run("TRẢ HỒ SƠ (Yêu cầu sửa lỗi ký hiệu góc Hình học 8, Hình học 7)\n"); r.bold = True; r.font.color.rgb = RGBColor(220, 38, 38)

    p_s2 = doc.add_paragraph(); p_s2.paragraph_format.space_before = Pt(6)
    r = p_s2.add_run("CHI TIẾT LỖI SAI SÓT YÊU CẦU KHẮC PHỤC:"); r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True; r.font.color.rgb = RGBColor(185, 28, 28)
    
    p_obs = doc.add_paragraph(); p_obs.paragraph_format.line_spacing = 1.25
    p_obs.add_run("1. Ưu điểm: ").bold = True
    p_obs.add_run("Khối lượng hồ sơ rất lớn, đảm bảo tiến độ đủ và vượt tháng 9; môn HĐTN 7 và Đại số 8 tích hợp NLS/AI in đậm nghiêng rất chuẩn mực.\n\n")
    p_obs.add_run("2. Lỗi nghiêm trọng cần khắc phục: ").bold = True
    p_obs.add_run(
        "• Phân môn Hình học 8 (Bài 10: Tứ giác, Luyện tập 2 và các bài tập tính góc) bị lỗi font công thức toán học nghiêm trọng.\n"
        "• Toàn bộ các công thức tính góc tứ giác bị biến dạng: D = 360° - (A + B + C) và H + E + F + G = 360° hiển thị các ký tự rác vuông/perpendicular đè lên đầu các chữ cái đỉnh (D┴, A┴, B┴, C┴, H┴, E┴, F┴, G┴...).\n"
        "• Ký hiệu góc A ở trang 51 bị lỗi font micro (góc µ A). Các lỗi font này gây mất thẩm mỹ chuyên môn và sai chuẩn toán học.\n"
    )
    
    add_callout(doc, 
                "Tổ chuyên môn quyết định TRẢ HỒ SƠ. Đề nghị cô Lê Thị Bình kiểm tra lại bộ font MathType/Equation trên máy, chỉnh sửa lại toàn bộ công thức và ký hiệu góc trong phân môn Hình học 8 và Hình học 7 để hiển thị dấu mũ góc chuẩn xác trước khi nộp lại phê duyệt.",
                title="KẾT LUẬN & YÊU CẦU:", border_color="DC2626", bg_color="FEF2F2")

    # Signature
    tbl_sig = doc.add_table(rows=1, cols=2); tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl_sig.cell(0, 0); c1 = tbl_sig.cell(0, 1)
    set_cell_margins(c0, 100, 0, 0, 0); set_cell_margins(c1, 100, 0, 0, 0)
    p0 = c0.paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p0.add_run("GIÁO VIÊN BỘ MÔN\n\n\n\n\nLê Thị Bình"); r.bold = True
    p1 = c1.paragraphs[0]; p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p1.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n\n\n\n\nHoàng Tấn Thiên"); r.bold = True

    p_doc = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_Le_Thi_Binh_Thang_9.docx"
    safe_save_doc(doc, p_doc)

create_personal_binh_tra_ho_so()

# ==============================================================================
# 5. CẬP NHẬT CÁC FILE MARKDOWN (.md)
# ==============================================================================
def update_markdown_files():
    # 5.1 Update Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md
    bb_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md"
    with open(bb_path, "r", encoding="utf-8") as f:
        bb_txt = f.read()

    old_row_thao = "| 3 | **Nguyễn Thị Thảo** | Toán 6, Toán 7 | 34 tiết (123 tr) | Đủ 100% Tháng 9 (12t Số 6) & vượt Tuần 5 | NLS Số 6 in đậm nghiêng chuẩn; nhắc lỗi font góc Hình 7 | **DUYỆT (KHÁ)** |"
    new_row_thao = "| 3 | **Nguyễn Thị Thảo** | Toán 6, Toán 7 | 34 tiết (123 tr) | Đủ 100% Tháng 9 & vượt Tuần 5 | Lỗi font ký hiệu góc nặng ở Hình 7 (ẋOz, O1┴...) | **TRẢ HỒ SƠ** |"

    old_row_binh = "| 5 | **Lê Thị Bình** | Toán 7, Toán 8, HĐTN 7 | 45 tiết (178 tr) | Đủ 100% Tháng 9 & vượt Tuần 5 | NLS/AI mẫu mực, in đậm nghiêng đúng quy định | **DUYỆT (TỐT)** |"
    new_row_binh = "| 5 | **Lê Thị Bình** | Toán 7, Toán 8, HĐTN 7 | 45 tiết (178 tr) | Đủ 100% Tháng 9 & vượt Tuần 5 | Lỗi font công thức góc nặng ở Hình 8 (D┴, A┴, H┴...) | **TRẢ HỒ SƠ** |"

    bb_txt = bb_txt.replace(old_row_thao, new_row_thao)
    bb_txt = bb_txt.replace(old_row_binh, new_row_binh)

    # Replace section 3 Thao
    old_sec3 = """### 3. Thẩm định hồ sơ giáo viên: NGUYỄN THỊ THẢO
- **Phân công giảng dạy**: Môn Toán 6 và Toán 7 (Sách Kết nối tri thức).
- **Tiến độ và khối lượng**: Nộp 04 tệp PDF gồm 123 trang, tổng cộng 34 tiết (Đại số 7: 9 tiết; Hình học 7: 8 tiết; Số học 6: 12 tiết; Hình học 6: 5 tiết). Đảm bảo 100% tiến độ 4 tuần của Tháng 9 và vượt tiến độ sang tuần 5 ở phân môn Đại số 7 và Hình học 6.
- **Ưu điểm**:
  + Hồ sơ chuẩn bị rất công phu, đầy đủ 4 hoạt động CV 5512, có nội dung giao việc chu đáo cho học sinh hòa nhập (HSHN).
  + Tích hợp Năng lực số (NLS 5.3 và 3.1) tại Bài 6 và Bài 7 Số học 6 đúng địa chỉ và đã **_in đậm, nghiêng_** rất chuẩn xác theo quy chế chuyên môn.
- **Tồn tại, hạn chế**:
  + Phân môn Hình học 7 bị lỗi font/ký hiệu góc (hiển thị thành dấu chấm trên đầu chữ cái như `ṁBy`, `ẋAB`... và lỗi font ở trang 8, 9).
- **Kết luận thẩm định**: **DUYỆT TOÀN BỘ HỒ SƠ - XẾP LOẠI: KHÁ** (Yêu cầu chỉnh sửa lại ký hiệu dấu mũ góc trước khi giảng dạy)."""

    new_sec3 = """### 3. Thẩm định hồ sơ giáo viên: NGUYỄN THỊ THẢO
- **Phân công giảng dạy**: Môn Toán 6 và Toán 7 (Sách Kết nối tri thức).
- **Tiến độ và khối lượng**: Nộp 04 tệp PDF gồm 123 trang, tổng cộng 34 tiết. Đảm bảo 100% tiến độ 4 tuần của Tháng 9 và vượt tiến độ sang tuần 5.
- **Ưu điểm**:
  + Số học 6 và Đại số 7 soạn tốt, tích hợp Năng lực số in đậm nghiêng đúng quy định.
- **Tồn tại, hạn chế (Nghiêm trọng)**:
  + Phân môn Hình học 7 bị lỗi font ký hiệu góc nghiêm trọng: các góc bị hiển thị thành dấu chấm trên đầu chữ cái (`ẋOz = 135°`, `ẏOz = 45°`, `ṁBy`, `ẋAB`...) và các góc `O1`, `O2`, `M1`, `M2` bị chèn ký tự rác vuông/perpendicular đè lên chữ.
- **Kết luận thẩm định**: **TRẢ HỒ SƠ (Yêu cầu chỉnh sửa chuẩn hóa toàn bộ ký hiệu góc trong Hình học 7 nộp lại tổ chuyên môn)**."""

    # Replace section 5 Binh
    old_sec5 = """### 5. Thẩm định hồ sơ giáo viên: LÊ THỊ BÌNH
- **Phân công giảng dạy**: Môn Toán 7, Toán 8 và Hoạt động trải nghiệm, hướng nghiệp 7 (HĐTN 7).
- **Tiến độ và khối lượng**: Nộp 05 tệp PDF gồm 178 trang, tổng cộng 45 tiết. Đảm bảo 100% tiến độ 4 tuần của Tháng 9 và vượt tiến độ sang tuần 5 ở phân môn Đại số 7 (Bài 3).
- **Ưu điểm**:
  + Hồ sơ chuẩn bị đồ sộ, công phu, phương pháp tổ chức 4 hoạt động CV 5512 rõ nét.
  + Tích hợp Năng lực số và AI trong HĐTN 7 và Đại số 8 cực kỳ xuất sắc; toàn bộ các câu chỉ báo hành động NLS và AI đều được in đậm, nghiêng rất chuẩn mực và khớp 100% với Phụ lục 3.
  + Kiến thức toán học chính xác, công thức và ký hiệu góc trong Hình học 7 và Hình học 8 chuẩn mực; khắc phục hoàn toàn lỗi toán học thường gặp ở bài Tứ giác.
- **Tồn tại, lưu ý**:
  + Tại Mục tiêu Trang 1 Hình học 8 cần bổ sung định dạng in đậm, nghiêng cho mã NLS 1.1 và 5.3; chú ý chỉnh sửa ký hiệu góc A bị lỗi font ở Trang 51 Hình học 8.
- **Kết luận thẩm định**: **DUYỆT TOÀN BỘ HỒ SƠ - XẾP LOẠI: TỐT**."""

    new_sec5 = """### 5. Thẩm định hồ sơ giáo viên: LÊ THỊ BÌNH
- **Phân công giảng dạy**: Môn Toán 7, Toán 8 và Hoạt động trải nghiệm, hướng nghiệp 7 (HĐTN 7).
- **Tiến độ và khối lượng**: Nộp 05 tệp PDF gồm 178 trang, tổng cộng 45 tiết. Đảm bảo 100% tiến độ 4 tuần của Tháng 9 và vượt tiến độ sang tuần 5 ở phân môn Đại số 7.
- **Ưu điểm**:
  + Khối lượng giáo án rất lớn, HĐTN 7 và Đại số 8 tích hợp NLS/AI in đậm nghiêng rất chuẩn mực.
- **Tồn tại, hạn chế (Nghiêm trọng)**:
  + Phân môn Hình học 8 (Bài 10: Tứ giác, Luyện tập 2) bị lỗi font công thức toán học nghiêm trọng: toàn bộ dấu mũ góc bị hiển thị thành các ký tự rác vuông/perpendicular đè lên đỉnh chữ (`D┴, A┴, B┴, C┴, H┴, E┴, F┴, G┴...`). Lỗi font hiển thị góc A ở trang 51 (`góc µ A`).
- **Kết luận thẩm định**: **TRẢ HỒ SƠ (Yêu cầu sửa lại triệt để font công thức và ký hiệu góc trong Hình học 8, Hình học 7 nộp lại tổ chuyên môn)**."""

    bb_txt = bb_txt.replace(old_sec3, new_sec3)
    bb_txt = bb_txt.replace(old_sec5, new_sec5)

    with open(bb_path, "w", encoding="utf-8") as f:
        f.write(bb_txt)
    print("SUCCESS: Updated Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md")

    # 5.2 Update Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md
    sys_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md"
    with open(sys_path, "r", encoding="utf-8") as f:
        sys_txt = f.read()

    # Thao Hinh 7
    old_thao_h7 = """### • Phân môn Hình học 7 (30 trang — 08 tiết: Bài 8, 9, LTC, Bài 10): [DUYỆT CÓ LƯU Ý (ĐÍNH CHÍNH KÝ HIỆU GÓC)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy đảm bảo đủ 08 tiết đúng tiến độ tháng 9. Nội dung kiến thức hai góc kề bù, đối đỉnh, hai đường thẳng song song và tiên đề Euclid đầy đủ. Lưu ý: Cần chỉnh sửa lại lỗi kỹ thuật hiển thị ký hiệu góc (các góc bị hiển thị thành dấu chấm trên đầu chữ cái như ṁBy, ẋAB... và lỗi font ở trang 8, 9) thành dấu mũ góc chuẩn xác trước khi giảng dạy.`"""

    new_thao_h7 = """### • Phân môn Hình học 7 (30 trang — 08 tiết: Bài 8, 9, LTC, Bài 10): [KHÔNG DUYỆT / TRẢ HỒ SƠ (LỖI FONT GÓC)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `TRẢ HỒ SƠ. Kế hoạch bài dạy Hình học 7 bị lỗi font ký hiệu góc rất nặng và biến dạng toán học: các góc bị hiển thị thành dấu chấm trên đầu chữ cái (ẋOz, ẏOz, ṁBy, ẋAB...) và góc O1, O2, M1, M2 bị ký tự rác chèn đè lên đỉnh chữ. Đề nghị cô Thảo chuẩn hóa toàn bộ công thức và ký hiệu dấu mũ góc chuẩn xác trước khi trình duyệt lại.`"""

    # Thao package
    old_thao_all = """### • Nhận xét chung toàn bộ hồ sơ Cô Nguyễn Thị Thảo (Duyệt theo gói): [DUYỆT - XẾP LOẠI KHÁ]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `DUYỆT HỒ SƠ (Xếp loại Khá). Hồ sơ nộp đầy đủ 34 tiết (123 trang), tiến độ đạt 100% tháng 9 và vượt tuần 5. Tích hợp NLS Số học 6 in đậm nghiêng rất chuẩn mực. Đề nghị cô Thảo chuẩn hóa lại ký hiệu dấu mũ góc trong phân môn Hình học 7 để nâng xếp loại Tốt trong đợt sau.`"""

    new_thao_all = """### • Nhận xét chung toàn bộ hồ sơ Cô Nguyễn Thị Thảo (Duyệt theo gói): [TRẢ HỒ SƠ (LỖI KÝ HIỆU GÓC HÌNH 7)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `TRẢ HỒ SƠ. Số học 6 và Đại số 7 soạn tốt, nhưng phân môn Hình học 7 bị lỗi font ký hiệu góc rất phản cảm và sai chuẩn mực toán học (dấu chấm trên đầu đỉnh góc và ký tự lạ đè lên chữ). Đề nghị cô Thảo khắc phục triệt để lỗi ký hiệu góc trong Hình học 7 và nộp lại để tổ chuyên môn phê duyệt.`"""

    # Binh Hinh 8
    old_binh_h8 = """### • Phân môn Hình học 8 (52 trang — 08 tiết: Bài 10, 11, LTC, Bài 12, LTC): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy soạn rất kỹ lưỡng (52 trang), đủ 08 tiết đảm bảo 100% tiến độ tháng 9. Khắc phục hoàn toàn lỗi toán học (định lý tổng 4 góc tứ giác và phép tính góc E, H tại Bài 10 chuẩn xác). Tích hợp NLS 1.1 và 5.3 in đậm nghiêng ở hoạt động. Lưu ý: Chỉnh lại lỗi font hiển thị tia phân giác góc A ở trang 51 trước khi dạy. Duyệt.`"""

    new_binh_h8 = """### • Phân môn Hình học 8 (52 trang — 08 tiết: Bài 10, 11, LTC, Bài 12, LTC): [KHÔNG DUYỆT / TRẢ HỒ SƠ (LỖI FONT CÔNG THỨC)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `TRẢ HỒ SƠ. Kế hoạch bài dạy Hình học 8 bị lỗi font công thức toán học nghiêm trọng tại Bài 10 (Tứ giác) và Luyện tập 2: toàn bộ dấu mũ góc bị biến dạng thành các ký tự vuông/rác đè lên đỉnh chữ cái (D┴, A┴, B┴, C┴, H┴, E┴, F┴, G┴...), sai chuẩn mực sư phạm. Đề nghị cô Bình chuẩn hóa lại toàn bộ MathType/Equation ký hiệu góc chuẩn xác rồi nộp lại.`"""

    # Binh package
    old_binh_all = """### • Nhận xét chung toàn bộ hồ sơ Cô Lê Thị Bình (Duyệt theo gói): [DUYỆT - XẾP LOẠI TỐT]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại Tốt). Giáo án chuẩn bị rất công phu (178 trang PDF qua 5 phân môn), đảm bảo 100% tiến độ tháng 9 và vượt tuần 5 ở Đại 7. Tích hợp NLS/AI xuất sắc, tuân thủ tuyệt đối quy định in đậm, nghiêng. Toán học và thể thức chuẩn mực. Biểu dương tinh thần trách nhiệm chuyên môn của cô Bình.`"""

    new_binh_all = """### • Nhận xét chung toàn bộ hồ sơ Cô Lê Thị Bình (Duyệt theo gói): [TRẢ HỒ SƠ (LỖI FONT CÔNG THỨC HÌNH HỌC)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `TRẢ HỒ SƠ. Môn HĐTN 7 và Đại số 7, Đại số 8 chuẩn bị rất công phu, NLS/AI mẫu mực. Tuy nhiên phân môn Hình học 8 và Hình học 7 bị lỗi font công thức toán học nghiêm trọng (dấu mũ góc biến dạng thành ký tự rác đè lên mặt chữ cái tại phần tính góc tứ giác). Đề nghị cô Bình sửa lại toàn bộ công thức toán học bị lỗi font và nộp lại tổ chuyên môn.`"""

    sys_txt = sys_txt.replace(old_thao_h7, new_thao_h7)
    sys_txt = sys_txt.replace(old_thao_all, new_thao_all)
    sys_txt = sys_txt.replace(old_binh_h8, new_binh_h8)
    sys_txt = sys_txt.replace(old_binh_all, new_binh_all)

    with open(sys_path, "w", encoding="utf-8") as f:
        f.write(sys_txt)
    print("SUCCESS: Updated Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md")

update_markdown_files()
print("ALL UPDATES FOR 2 TEACHERS COMPLETED!")
