import os
import sys
import shutil
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
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

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

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

def add_callout(doc, text, title="GHI CHÚ / LƯU Ý:", border_color="0284C7", bg_color="F0F9FF"):
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

print("Starting generation of Le Thi Binh's review documents...")

# ==============================================================================
# 1. TẠO PHIẾU NHẬN XÉT CÁ NHÂN CÔ LÊ THỊ BÌNH
# ==============================================================================
def create_personal_review_binh():
    doc = docx.Document()
    
    # Page setup A4
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.59)
        section.bottom_margin = Inches(0.59)
        section.left_margin = Inches(0.79)
        section.right_margin = Inches(0.59)
        
        # Header / Footer
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("Trường THCS Trần Phú | Tổ Toán – Tin | Hồ sơ chuyên môn Tháng 9/2026")
        r_hdr.font.name = "Times New Roman"
        r_hdr.font.size = Pt(9)
        r_hdr.font.color.rgb = RGBColor(100, 116, 139)
        
        footer = section.footer
        p_ftr = footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ftr = p_ftr.add_run("Trang ")
        r_ftr.font.name = "Times New Roman"
        r_ftr.font.size = Pt(9)
        r_ftr.font.color.rgb = RGBColor(100, 116, 139)
        
    # National header
    tbl_h = doc.add_table(rows=1, cols=2)
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = tbl_h.cell(0, 0)
    c1 = tbl_h.cell(0, 1)
    set_cell_margins(c0, 0, 0, 0, 0)
    set_cell_margins(c1, 0, 0, 0, 0)
    
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p0.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.bold = True
    r = p0.add_run("TỔ TOÁN – TIN\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True
    r = p0.add_run("Số: 05/PĐG-TT")
    r.font.name = "Times New Roman"; r.font.size = Pt(10); r.italic = True
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p1.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(10.5); r.bold = True
    r = p1.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True
    r = p1.add_run("Xuân Đông, ngày 05 tháng 10 năm 2026")
    r.font.name = "Times New Roman"; r.font.size = Pt(10); r.italic = True
    
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run("PHIẾU NHẬN XÉT, THẨM ĐỊNH HỒ SƠ BÀI DẠY\n(DUYỆT GIÁO ÁN THÁNG 9/2026)")
    r_t.font.name = "Times New Roman"; r_t.font.size = Pt(14); r_t.bold = True
    r_t.font.color.rgb = RGBColor(15, 23, 42)
    
    # Info
    p_info = doc.add_paragraph()
    p_info.paragraph_format.space_before = Pt(4)
    p_info.paragraph_format.space_after = Pt(10)
    p_info.paragraph_format.line_spacing = 1.2
    
    def add_line(p, label, val):
        r1 = p.add_run(f"• {label}: ")
        r1.font.name = "Times New Roman"; r1.font.size = Pt(11); r1.bold = True
        r2 = p.add_run(f"{val}\n")
        r2.font.name = "Times New Roman"; r2.font.size = Pt(11)
        
    add_line(p_info, "Họ và tên giáo viên", "LÊ THỊ BÌNH")
    add_line(p_info, "Tổ chuyên môn", "Toán – Tin, Trường THCS Trần Phú")
    add_line(p_info, "Môn giảng dạy", "Toán 7, Toán 8, Hoạt động trải nghiệm, hướng nghiệp 7 (HĐTN 7)")
    add_line(p_info, "Tổng số hồ sơ nộp", "05 phân môn (178 trang PDF)")
    add_line(p_info, "Tổng số tiết nộp", "45 tiết (Đại số 7: 9 tiết; Hình học 7: 8 tiết; Đại số 8: 8 tiết; Hình học 8: 8 tiết; HĐTN 7: 12 tiết)")
    add_line(p_info, "Tiến độ thực hiện", "Đạt 100% kế hoạch 4 tuần Tháng 9/2026 (Đại số 7 vượt sang tuần 5)")

    # Section 1: Detailed Table
    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_before = Pt(6)
    p_s1.paragraph_format.space_after = Pt(4)
    r = p_s1.add_run("I. CHI TIẾT KẾT QUẢ THẨM ĐỊNH TỪNG PHÂN MÔN")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    tbl = doc.add_table(rows=6, cols=5)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)
    
    headers = ["Phân môn", "Số trang", "Số tiết", "Tiến độ & Tích hợp NLS / AI", "Đánh giá"]
    
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
        format_cell(cell, h, bold=True, font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=(15, 23, 42))
        
    data = [
        ("Đại số 7", "31 trang", "09 tiết", "Đạt 100% Tháng 9 & vượt tuần 5 (Bài 1, 2, LTC, Bài 3). 4 hoạt động rõ ràng, bài tập chuẩn.", "DUYỆT (Tốt)"),
        ("Hình học 7", "31 trang", "08 tiết", "Đạt 100% Tháng 9 (Bài 8, 9, LTC, Bài 10). Ký hiệu góc và song song chuẩn xác.", "DUYỆT (Tốt)"),
        ("Đại số 8", "51 trang", "08 tiết", "Đạt 100% Tháng 9 (Bài 1, 2, 3, LTC, Bài 4). Tích hợp NLS 5.3.TC2a in đậm, nghiêng chuẩn.", "DUYỆT (Tốt)"),
        ("Hình học 8", "52 trang", "08 tiết", "Đạt 100% Tháng 9 (Bài 10, 11, LTC, Bài 12, LTC). NLS 1.1 và 5.3 in đậm nghiêng; toán chuẩn.", "DUYỆT (Tốt)"),
        ("HĐTN 7", "13 trang", "12 tiết", "Đạt 100% Tháng 9 (Chủ đề 1). Tích hợp NLS & AI cực kỳ công phu, 100% in đậm nghiêng mẫu mực.", "DUYỆT (Xuất sắc)")
    ]
    
    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = tbl.cell(row_idx, col_idx)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [1, 2, 4] else WD_ALIGN_PARAGRAPH.LEFT
            format_cell(cell, text, bold=(col_idx==4), font_size=10, align=align, color_rgb=(15, 23, 42))
            
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # Section 2: Detailed observations
    p_s2 = doc.add_paragraph()
    p_s2.paragraph_format.space_before = Pt(6)
    p_s2.paragraph_format.space_after = Pt(4)
    r = p_s2.add_run("II. NHẬN XÉT CHUYÊN MÔN CHI TIẾT")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    p_obs = doc.add_paragraph()
    p_obs.paragraph_format.line_spacing = 1.25
    p_obs.paragraph_format.space_after = Pt(6)
    
    def add_p_run(p, title, content):
        r1 = p.add_run(f"1. {title}: ") if "Ưu điểm" in title else (p.add_run(f"2. {title}: ") if "Tồn tại" in title else p.add_run(f"3. {title}: "))
        r1.font.name = "Times New Roman"; r1.font.size = Pt(11); r1.bold = True
        r2 = p.add_run(f"{content}\n\n")
        r2.font.name = "Times New Roman"; r2.font.size = Pt(11)
        
    add_p_run(p_obs, "Ưu điểm nổi bật",
              "• Hồ sơ giáo án đồ sộ, được chuẩn bị vô cùng công phu, nghiêm túc và bài bản với tổng cộng 178 trang PDF qua 5 phân môn, đảm bảo 100% tiến độ 4 tuần của Tháng 9 và vượt tiến độ sang tuần 5 ở môn Đại số 7.\n"
              "• Tích hợp Năng lực số (NLS) và Trí tuệ nhân tạo (AI) rất xuất sắc, tiêu biểu là giáo án HĐTN 7 và Đại số 8. Toàn bộ các câu mô tả chỉ báo hành động NLS (1.1.TC2a, 3.1.TC2a, 2.5.TC1a, 4.2.TC1a, 3.1.TC1a, 3.3.TC1a, 5.3.TC2a) và AI (7.A1.1, 7.A1.2, 7.B3.1) đều được in đậm, nghiêng đúng 100% theo quy chế chuyên môn và khớp chuẩn xác với Phụ lục 3.\n"
              "• Kiến thức toán học chính xác, lập luận chặt chẽ; định lý tổng 4 góc tứ giác và bài toán tính góc trong Hình học 8 chuẩn mực; các bước thực hiện 4 hoạt động theo CV 5512 rõ ràng, mạch lạc.")
              
    add_p_run(p_obs, "Một số điểm lưu ý, hoàn thiện",
              "• Phân môn Hình học 8: Tại Mục tiêu (Trang 1), cần bổ sung định dạng in đậm, nghiêng cho 2 dòng chỉ báo NLS (1.1.TC2a và 5.3.TC2a) để đồng bộ tuyệt đối với các hoạt động bên dưới; tại Trang 51 lưu ý chỉnh lại ký hiệu góc bị hiển thị nhầm thành font micro (góc µ A) thành dấu mũ góc chuẩn xác.\n"
              "• Phân môn Đại số 7: Dòng gợi ý sử dụng Canva/Mindmap ở Trang 7 là hoạt động phát triển tốt, giáo viên có thể in đậm nghiêng để hồ sơ thêm hoàn thiện.")

    # Section 3: Conclusion
    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.space_before = Pt(6)
    p_s3.paragraph_format.space_after = Pt(4)
    r = p_s3.add_run("III. KẾT LUẬN VÀ XẾP LOẠI")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    add_callout(doc, 
                "Hồ sơ bài dạy môn Toán 7, Toán 8 và HĐTN 7 đợt Tháng 9/2026 của Cô Lê Thị Bình ĐẠT CHẤT LƯỢNG RẤT XUẤT SẮC. Tiến độ đảm bảo đủ và vượt kế hoạch; tích hợp NLS/AI mẫu mực, in đậm nghiêng đúng quy định. Tổ chuyên môn thống nhất DUYỆT TOÀN BỘ HỒ SƠ - XẾP LOẠI: TỐT.",
                title="KẾT LUẬN:", border_color="16A34A", bg_color="F0FDF4")
                
    # Signature table
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    cs0 = tbl_sig.cell(0, 0)
    cs1 = tbl_sig.cell(0, 1)
    set_cell_margins(cs0, 100, 0, 0, 0)
    set_cell_margins(cs1, 100, 0, 0, 0)
    
    ps0 = cs0.paragraphs[0]
    ps0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = ps0.add_run("GIÁO VIÊN BỘ MÔN\n\n\n\n\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True
    r = ps0.add_run("Lê Thị Bình")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True
    
    ps1 = cs1.paragraphs[0]
    ps1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = ps1.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n\n\n\n\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True
    r = ps1.add_run("Hoàng Tấn Thiên")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True

    p_doc = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_Le_Thi_Binh_Thang_9.docx"
    safe_save_doc(doc, p_doc)

create_personal_review_binh()

# ==============================================================================
# 2. CẬP NHẬT TỆP NHẬN XÉT HỆ THỐNG (Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9)
# ==============================================================================
def update_system_comments_file():
    doc_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.docx"
    doc = docx.Document(doc_path)
    
    # Check if section 5 already exists (to avoid duplicate)
    for p in doc.paragraphs:
        if "5. CÔ LÊ THỊ BÌNH" in p.text:
            print("Notice: Le Thi Binh already in Cap_Nhat_He_Thong docx, skipping duplicate.")
            return
            
    # Add Section 5 for Le Thi Binh
    p_sec = doc.add_paragraph()
    p_sec.paragraph_format.space_before = Pt(16)
    p_sec.paragraph_format.space_after = Pt(6)
    r = p_sec.add_run("5. CÔ LÊ THỊ BÌNH (MÔN TOÁN 7, TOÁN 8, HĐTN 7 — 45 TIẾT, 178 TRANG)")
    r.font.name = "Times New Roman"; r.font.size = Pt(13); r.bold = True
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    items = [
        ("Phân môn Hoạt động trải nghiệm, hướng nghiệp 7 (13 trang — 12 tiết: Chủ đề 1: Em với nhà trường)",
         "ĐẠT / DUYỆT (XUẤT SẮC)",
         "Kế hoạch bài dạy chuẩn bị rất công phu, đủ 12 tiết Chủ đề 1 đúng tiến độ tháng 9. Cấu trúc rõ ràng giữa hoạt động quy mô trường và hoạt động trên lớp. Tích hợp Năng lực số (1.1, 3.1, 2.5, 4.2, 3.3) và Năng lực AI (7.A1.1, 7.A1.2, 7.B3.1) cực kỳ mẫu mực, 100% chỉ báo và mô tả hành động đều được IN ĐẬM, NGHIÊNG rất chuẩn xác theo quy chế chuyên môn. Duyệt.",
         "16A34A", "F0FDF4"),
        
        ("Phân môn Đại số 7 (31 trang — 09 tiết: Bài 1, 2, LTC, Bài 3)",
         "ĐẠT / DUYỆT (TỐT)",
         "Kế hoạch bài dạy soạn tốt, đủ 09 tiết đảm bảo 100% tiến độ tháng 9 và vượt tuần 5. Thiết kế đủ 4 hoạt động CV 5512, các bước thực hiện phép tính số hữu tỉ và lũy thừa chính xác, bài tập củng cố phong phú. Duyệt.",
         "16A34A", "F0FDF4"),
        
        ("Phân môn Hình học 7 (31 trang — 08 tiết: Bài 8, 9, LTC, Bài 10)",
         "ĐẠT / DUYỆT (TỐT)",
         "Soạn đủ 08 tiết đảm bảo đúng tiến độ tháng 9. Kiến thức góc ở vị trí đặc biệt, tia phân giác, hai đường thẳng song song và tiên đề Euclid đầy đủ, logic. Ký hiệu góc và quan hệ hình học chuẩn xác. Duyệt.",
         "16A34A", "F0FDF4"),
        
        ("Phân môn Đại số 8 (51 trang — 08 tiết: Bài 1, 2, Bài 3, LTC, Bài 4)",
         "ĐẠT / DUYỆT (XUẤT SẮC)",
         "Soạn đủ 08 tiết đúng tiến độ 4 tuần tháng 9. Hệ thống bài tập đa dạng, phương pháp dẫn dắt trực quan. Tích hợp Năng lực số (5.3.TC2a) tại Bài 3 khớp Phụ lục 3 và đã IN ĐẬM, NGHIÊNG rất chuẩn mực theo quy định. Duyệt.",
         "16A34A", "F0FDF4"),
        
        ("Phân môn Hình học 8 (52 trang — 08 tiết: Bài 10, 11, LTC, Bài 12, LTC)",
         "ĐẠT / DUYỆT (TỐT)",
         "Kế hoạch bài dạy soạn rất kỹ lưỡng (52 trang), đủ 08 tiết đảm bảo 100% tiến độ tháng 9. Khắc phục hoàn toàn lỗi toán học (định lý tổng 4 góc tứ giác và phép tính góc E, H tại Bài 10 chuẩn xác). Tích hợp NLS 1.1 và 5.3 in đậm nghiêng ở hoạt động. Lưu ý: Chỉnh lại lỗi font hiển thị tia phân giác góc A ở trang 51 trước khi dạy. Duyệt.",
         "16A34A", "F0FDF4"),
         
        ("Nhận xét chung toàn bộ hồ sơ Cô Lê Thị Bình (Duyệt theo gói)",
         "DUYỆT - XẾP LOẠI TỐT",
         "DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại Tốt). Giáo án chuẩn bị rất công phu (178 trang PDF qua 5 phân môn), đảm bảo 100% tiến độ tháng 9 và vượt tuần 5 ở Đại 7. Tích hợp NLS/AI xuất sắc, tuân thủ tuyệt đối quy định in đậm, nghiêng. Toán học và thể thức chuẩn mực. Biểu dương tinh thần trách nhiệm chuyên môn của cô Bình.",
         "16A34A", "F0FDF4")
    ]
    
    for sub, status, comment, border_c, bg_c in items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(8)
        p_item.paragraph_format.space_after = Pt(2)
        r_sub = p_item.add_run(f"• {sub}: ")
        r_sub.font.name = "Times New Roman"; r_sub.font.size = Pt(11.5); r_sub.bold = True
        r_st = p_item.add_run(f"[{status}]")
        r_st.font.name = "Times New Roman"; r_st.font.size = Pt(11.5); r_st.bold = True
        r_st.font.color.rgb = RGBColor(22, 163, 74)
        
        add_callout(doc, comment, title="Nhận xét hệ thống (Copy & Paste):", border_color=border_c, bg_color=bg_c)

    safe_save_doc(doc, doc_path)

update_system_comments_file()

# ==============================================================================
# 3. CẬP NHẬT BIÊN BẢN KIỂM TRA TỔ (Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9)
# ==============================================================================
def update_bien_ban_to():
    doc_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.docx"
    doc = docx.Document(doc_path)
    
    # 1. Update table of all teachers: Add row 5 (Le Thi Binh)
    found_table = False
    for t in doc.tables:
        if len(t.rows) > 0 and len(t.columns) == 6 and "họ và tên" in t.rows[0].cells[1].text.lower():
            # Check if row 5 already exists
            already_added = any("lê thị bình" in r.cells[1].text.lower() for r in t.rows)
            if not already_added:
                row = t.add_row()
                cells = row.cells
                format_cell(cells[0], "5", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
                format_cell(cells[1], "LÊ THỊ BÌNH", bold=True, font_size=10)
                format_cell(cells[2], "Toán 7, Toán 8, HĐTN 7", font_size=10)
                format_cell(cells[3], "45 tiết (5 phân môn)", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
                format_cell(cells[4], "Đủ 100% Tháng 9 & vượt Tuần 5 (Đại 7); NLS/AI in đậm nghiêng chuẩn", font_size=10)
                format_cell(cells[5], "DUYỆT (Xếp loại: Tốt)", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=(22, 163, 74))
                for c in cells:
                    set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            found_table = True
            break
            
    if not found_table:
        print("WARNING: Table of teachers not found in Bien Ban!")

    # 2. Add detailed review section for Le Thi Binh if not present
    already_has_sec5 = any("5. Thẩm định hồ sơ giáo viên: LÊ THỊ BÌNH" in p.text for p in doc.paragraphs)
    if not already_has_sec5:
        p_sec = doc.add_paragraph()
        p_sec.paragraph_format.space_before = Pt(14)
        p_sec.paragraph_format.space_after = Pt(4)
        r = p_sec.add_run("5. Thẩm định hồ sơ giáo viên: LÊ THỊ BÌNH")
        r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138)
        
        p_txt = doc.add_paragraph()
        p_txt.paragraph_format.line_spacing = 1.25
        p_txt.paragraph_format.space_after = Pt(6)
        
        p_txt.add_run("• Phân công giảng dạy: ").bold = True
        p_txt.add_run("Toán 7, Toán 8 và Hoạt động trải nghiệm, hướng nghiệp 7 (HĐTN 7).\n")
        p_txt.add_run("• Tiến độ và khối lượng: ").bold = True
        p_txt.add_run("Nộp 05 tệp PDF gồm 178 trang, tổng cộng 45 tiết. Đảm bảo 100% tiến độ 4 tuần của Tháng 9 và vượt tiến độ sang tuần 5 ở phân môn Đại số 7 (Bài 3).\n")
        p_txt.add_run("• Ưu điểm: ").bold = True
        p_txt.add_run("Hồ sơ chuẩn bị đồ sộ, công phu, phương pháp tổ chức 4 hoạt động CV 5512 rõ nét. Tích hợp Năng lực số và AI trong HĐTN 7 và Đại số 8 cực kỳ xuất sắc; toàn bộ các câu chỉ báo hành động NLS và AI đều được in đậm, nghiêng rất chuẩn mực và khớp 100% với Phụ lục 3. Kiến thức toán học chính xác, công thức và ký hiệu góc trong Hình học 7 và Hình học 8 chuẩn mực; khắc phục hoàn toàn lỗi toán học thường gặp ở bài Tứ giác.\n")
        p_txt.add_run("• Tồn tại, lưu ý: ").bold = True
        p_txt.add_run("Tại Mục tiêu Trang 1 Hình học 8 cần bổ sung định dạng in đậm, nghiêng cho mã NLS 1.1 và 5.3; chú ý chỉnh sửa ký hiệu góc A bị lỗi font ở Trang 51 Hình học 8.\n")
        p_txt.add_run("• Kết luận thẩm định: ").bold = True
        r_res = p_txt.add_run("DUYỆT TOÀN BỘ HỒ SƠ - XẾP LOẠI: TỐT.\n")
        r_res.bold = True; r_res.font.color.rgb = RGBColor(22, 163, 74)

    safe_save_doc(doc, doc_path)

update_bien_ban_to()

# ==============================================================================
# 4. ĐỒNG BỘ NỘI DUNG VÀO CÁC FILE MARKDOWN (.md)
# ==============================================================================
def update_markdown_files():
    # 4.1 Update Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md
    md_system_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md"
    with open(md_system_path, "r", encoding="utf-8") as f:
        sys_md = f.read()
        
    if "## 5. CÔ LÊ THỊ BÌNH" not in sys_md:
        content_binh_md = """
---

## 5. CÔ LÊ THỊ BÌNH (MÔN TOÁN 7, TOÁN 8, HĐTN 7 — 45 TIẾT, 178 TRANG)

### • Phân môn Hoạt động trải nghiệm, hướng nghiệp 7 (13 trang — 12 tiết: Chủ đề 1: Em với nhà trường): [ĐẠT / DUYỆT (XUẤT SẮC)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy chuẩn bị rất công phu, đủ 12 tiết Chủ đề 1 đúng tiến độ tháng 9. Cấu trúc rõ ràng giữa hoạt động quy mô trường và hoạt động trên lớp. Tích hợp Năng lực số (1.1, 3.1, 2.5, 4.2, 3.3) và Năng lực AI (7.A1.1, 7.A1.2, 7.B3.1) cực kỳ mẫu mực, 100% chỉ báo và mô tả hành động đều được IN ĐẬM, NGHIÊNG rất chuẩn xác theo quy chế chuyên môn. Duyệt.`

### • Phân môn Đại số 7 (31 trang — 09 tiết: Bài 1, 2, LTC, Bài 3): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy soạn tốt, đủ 09 tiết đảm bảo 100% tiến độ tháng 9 và vượt tuần 5. Thiết kế đủ 4 hoạt động CV 5512, các bước thực hiện phép tính số hữu tỉ và lũy thừa chính xác, bài tập củng cố phong phú. Duyệt.`

### • Phân môn Hình học 7 (31 trang — 08 tiết: Bài 8, 9, LTC, Bài 10): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Soạn đủ 08 tiết đảm bảo đúng tiến độ tháng 9. Kiến thức góc ở vị trí đặc biệt, tia phân giác, hai đường thẳng song song và tiên đề Euclid đầy đủ, logic. Ký hiệu góc và quan hệ hình học chuẩn xác. Duyệt.`

### • Phân môn Đại số 8 (51 trang — 08 tiết: Bài 1, 2, Bài 3, LTC, Bài 4): [ĐẠT / DUYỆT (XUẤT SẮC)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Soạn đủ 08 tiết đúng tiến độ 4 tuần tháng 9. Hệ thống bài tập đa dạng, phương pháp dẫn dắt trực quan. Tích hợp Năng lực số (5.3.TC2a) tại Bài 3 khớp Phụ lục 3 và đã IN ĐẬM, NGHIÊNG rất chuẩn mực theo quy định. Duyệt.`

### • Phân môn Hình học 8 (52 trang — 08 tiết: Bài 10, 11, LTC, Bài 12, LTC): [ĐẠT / DUYỆT (TỐT)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy soạn rất kỹ lưỡng (52 trang), đủ 08 tiết đảm bảo 100% tiến độ tháng 9. Khắc phục hoàn toàn lỗi toán học (định lý tổng 4 góc tứ giác và phép tính góc E, H tại Bài 10 chuẩn xác). Tích hợp NLS 1.1 và 5.3 in đậm nghiêng ở hoạt động. Lưu ý: Chỉnh lại lỗi font hiển thị tia phân giác góc A ở trang 51 trước khi dạy. Duyệt.`

### • Nhận xét chung toàn bộ hồ sơ Cô Lê Thị Bình (Duyệt theo gói): [DUYỆT - XẾP LOẠI TỐT]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `DUYỆT TOÀN BỘ HỒ SƠ (Xếp loại Tốt). Giáo án chuẩn bị rất công phu (178 trang PDF qua 5 phân môn), đảm bảo 100% tiến độ tháng 9 và vượt tuần 5 ở Đại 7. Tích hợp NLS/AI xuất sắc, tuân thủ tuyệt đối quy định in đậm, nghiêng. Toán học và thể thức chuẩn mực. Biểu dương tinh thần trách nhiệm chuyên môn của cô Bình.`
"""
        with open(md_system_path, "a", encoding="utf-8") as f:
            f.write(content_binh_md)
        print("SUCCESS: Appended Le Thi Binh to Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md")

    # 4.2 Update Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md
    md_bb_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md"
    with open(md_bb_path, "r", encoding="utf-8") as f:
        bb_content = f.read()
        
    if "### 5. Thẩm định hồ sơ giáo viên: LÊ THỊ BÌNH" not in bb_content:
        # Add row to table in MD
        row_md = "| 5 | **Lê Thị Bình** | Toán 7, Toán 8, HĐTN 7 | 45 tiết (178 tr) | Đủ 100% Tháng 9 & vượt Tuần 5 | NLS/AI mẫu mực, in đậm nghiêng đúng quy định | **DUYỆT (TỐT)** |\n"
        if "| 4 | **Trần Sáng**" in bb_content:
            bb_content = bb_content.replace(
                "| 4 | **Trần Sáng** | Toán 6, Toán 9 | 28 tiết (144 tr) | Thiếu 04 tiết Tuần 4 môn Toán 6 | Đã tích hợp NLS/AI in đậm nghiêng chuẩn | **TRẢ HỒ SƠ** |\n",
                "| 4 | **Trần Sáng** | Toán 6, Toán 9 | 28 tiết (144 tr) | Thiếu 04 tiết Tuần 4 môn Toán 6 | Đã tích hợp NLS/AI in đậm nghiêng chuẩn | **TRẢ HỒ SƠ** |\n" + row_md
            )
            
        # Append section 5 in MD
        sec_binh_md = """
### 5. Thẩm định hồ sơ giáo viên: LÊ THỊ BÌNH
- **Phân công giảng dạy**: Môn Toán 7, Toán 8 và Hoạt động trải nghiệm, hướng nghiệp 7 (HĐTN 7).
- **Tiến độ và khối lượng**: Nộp 05 tệp PDF gồm 178 trang, tổng cộng 45 tiết. Đảm bảo 100% tiến độ 4 tuần của Tháng 9 và vượt tiến độ sang tuần 5 ở phân môn Đại số 7 (Bài 3).
- **Ưu điểm**:
  + Hồ sơ chuẩn bị đồ sộ, công phu, phương pháp tổ chức 4 hoạt động CV 5512 rõ nét.
  + Tích hợp Năng lực số và AI trong HĐTN 7 và Đại số 8 cực kỳ xuất sắc; toàn bộ các câu chỉ báo hành động NLS và AI đều được in đậm, nghiêng rất chuẩn mực và khớp 100% với Phụ lục 3.
  + Kiến thức toán học chính xác, công thức và ký hiệu góc trong Hình học 7 và Hình học 8 chuẩn mực; khắc phục hoàn toàn lỗi toán học thường gặp ở bài Tứ giác.
- **Tồn tại, lưu ý**:
  + Tại Mục tiêu Trang 1 Hình học 8 cần bổ sung định dạng in đậm, nghiêng cho mã NLS 1.1 và 5.3; chú ý chỉnh sửa ký hiệu góc A bị lỗi font ở Trang 51 Hình học 8.
- **Kết luận thẩm định**: **DUYỆT TOÀN BỘ HỒ SƠ - XẾP LOẠI: TỐT**.
"""
        bb_content += sec_binh_md
        
        with open(md_bb_path, "w", encoding="utf-8") as f:
            f.write(bb_content)
        print("SUCCESS: Updated Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md")

update_markdown_files()
print("ALL TASKS COMPLETED FOR LE THI BINH!")
