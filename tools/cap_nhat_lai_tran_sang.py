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

print("Starting re-assessment update for Thầy Trần Sáng...")

# ==============================================================================
# 1. TÁI TẠO PHIẾU NHẬN XÉT CÁ NHÂN THẦY TRẦN SÁNG (XẾP LOẠI KHÁ / DUYỆT)
# ==============================================================================
def create_personal_review_sang():
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
    r = p0.add_run("Số: 04/PĐG-TT")
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
    r_t = p_title.add_run("PHIẾU NHẬN XÉT, THẨM ĐỊNH LẠI HỒ SƠ BÀI DẠY\n(DUYỆT GIÁO ÁN BỔ SUNG THÁNG 9/2026)")
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
        
    add_line(p_info, "Họ và tên giáo viên", "TRẦN SÁNG")
    add_line(p_info, "Tổ chuyên môn", "Toán – Tin, Trường THCS Trần Phú")
    add_line(p_info, "Môn giảng dạy", "Toán 6, Toán 9 (Sách Kết nối tri thức)")
    add_line(p_info, "Tổng số hồ sơ nộp", "04 phân môn (155 trang PDF: Số 6 - 54 tr, Hình 6 - 25 tr, Đại 9 - 59 tr, Hình 9 - 17 tr)")
    add_line(p_info, "Tổng số tiết đã nộp", "32 tiết / 32 tiết quy định (Đã nộp bổ sung đủ 04 tiết Tuần 4 môn Toán 6)")
    add_line(p_info, "Tiến độ thực hiện", "Đạt 100% kế hoạch 4 tuần Tháng 9/2026 (Đại số 9 vượt sang tuần 5)")

    # Section 1: Detailed Table
    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_before = Pt(6)
    p_s1.paragraph_format.space_after = Pt(4)
    r = p_s1.add_run("I. CHI TIẾT KẾT QUẢ THẨM ĐỊNH LẠI TỪNG PHÂN MÔN")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    tbl = doc.add_table(rows=5, cols=5)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)
    
    headers = ["Phân môn", "Số trang", "Số tiết", "Tiến độ & Tích hợp NLS / AI", "Đánh giá"]
    
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        set_cell_shading(cell, "F1F5F9")
        set_cell_margins(cell, top=120, bottom=120, left=100, right=100)
        format_cell(cell, h, bold=True, font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=(15, 23, 42))
        
    data = [
        ("Số học 6", "54 trang", "12 tiết", "ĐÃ BỔ SUNG ĐỦ: Tiết 10, 11 (Bài 7) & Tiết 12 (LTC). Đạt 100% tiến độ. Có mã NLS 5.3 & 3.1, lưu ý in đậm nghiêng.", "DUYỆT (Khá)"),
        ("Hình học 6", "25 trang", "04 tiết", "Đảm bảo đủ 4 tiết 4 tuần Tháng 9 (Bài 18 & Tiết 3, 4 Bài 19) theo đúng PPCT Phụ lục 3.", "DUYỆT (Đạt)"),
        ("Đại số 9", "59 trang", "12 tiết", "Đạt 100% Tháng 9 & vượt tuần 5 (Bài 1 đến 4). Tích hợp NLS (5.3) & AI (9.B2.1) in đậm nghiêng chuẩn.", "DUYỆT (Tốt)"),
        ("Hình học 9", "17 trang", "04 tiết", "Đạt 100% Tháng 9 (Bài 11 & Bài 12 Tiết 1). Định nghĩa và hệ thức lượng giác chuẩn xác.", "DUYỆT (Đạt)")
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
        
    add_p_run(p_obs, "Ưu điểm nổi bật và ghi nhận nộp bổ sung",
              "• Giáo viên có tinh thần cầu thị, tiếp thu nhanh chóng và kịp thời bổ sung hoàn chỉnh các tiết còn thiếu trong đợt kiểm tra đầu. Hiện tại toàn bộ hồ sơ đã đạt tổng cộng 155 trang PDF với đủ 32 tiết / 32 tiết quy định, đảm bảo 100% tiến độ PPCT 4 tuần của Tháng 9 và vượt tiến độ sang tuần 5 ở môn Đại số 9.\n"
              "• Phân môn Đại số 9 và Hình học 9 soạn rất công phu, chuẩn mực 4 hoạt động CV 5512. Tích hợp NLS (5.3.TC2a) và Năng lực AI (9.B2.1) tại Bài 1 Đại 9 đã được in đậm, nghiêng rất chuẩn mực.\n"
              "• Phân môn Số học 6 phần bổ sung (Bài 7: Thứ tự thực hiện các phép tính và Luyện tập chung) đã đưa đầy đủ mã năng lực số (5.3.TC1a và 3.1.TC1a) khớp chuẩn xác với Phụ lục 3. Các bài toán thực tiễn tính thời gian tiêu thụ hydrogen, tế bào hồng cầu, tiền lát sàn nhà được hướng dẫn giải chi tiết, chuẩn xác.")
              
    add_p_run(p_obs, "Một số điểm lưu ý, hoàn thiện",
              "• Tại Bài 7 Số học 6 (Trang 44): Nội dung mô tả chỉ báo NLS (5.3.TC1a và 3.1.TC1a) đã khớp Phụ lục 3 nhưng font chữ vẫn đang ở định dạng thường. Giáo viên cần chỉnh sửa in đậm, nghiêng đúng quy định chuyên môn trước khi lưu hành giảng dạy.")

    # Section 3: Conclusion
    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.space_before = Pt(6)
    p_s3.paragraph_format.space_after = Pt(4)
    r = p_s3.add_run("III. KẾT LUẬN VÀ XẾP LOẠI")
    r.font.name = "Times New Roman"; r.font.size = Pt(12); r.bold = True
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    add_callout(doc, 
                "Giáo viên đã nộp bổ sung đầy đủ 04 tiết còn thiếu của môn Toán 6, đạt 100% tiến độ PPCT Tháng 9/2026 với 32 tiết (155 trang). Tích hợp NLS và AI đầy đủ. Tổ chuyên môn thống nhất DUYỆT TOÀN BỘ HỒ SƠ - XẾP LOẠI: KHÁ (Nhắc nhở in đậm nghiêng NLS tại Bài 7 Số 6).",
                title="KẾT LUẬN:", border_color="2563EB", bg_color="EFF6FF")
                
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
    r = ps0.add_run("Trần Sáng")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True
    
    ps1 = cs1.paragraphs[0]
    ps1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = ps1.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n\n\n\n\n")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True
    r = ps1.add_run("Hoàng Tấn Thiên")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.bold = True

    p_doc = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_Tran_Sang_Thang_9.docx"
    safe_save_doc(doc, p_doc)

create_personal_review_sang()

# ==============================================================================
# 2. CẬP NHẬT BIÊN BẢN KIỂM TRA TỔ (Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.docx & .md)
# ==============================================================================
def update_bien_ban_to():
    doc_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.docx"
    doc = docx.Document(doc_path)
    
    # 1. Update row 4 (Tran Sang) in Table 2
    for t in doc.tables:
        if len(t.rows) > 0 and len(t.columns) == 6 and "họ và tên" in t.rows[0].cells[1].text.lower():
            for r in t.rows:
                if "trần sáng" in r.cells[1].text.lower():
                    format_cell(r.cells[3], "32 tiết (155 trang)", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
                    format_cell(r.cells[4], "Đã bổ sung đủ 100% Tháng 9; NLS khớp PL3", font_size=10)
                    format_cell(r.cells[5], "DUYỆT (Xếp loại: Khá)", bold=True, font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color_rgb=(37, 99, 235))
                    break
            break

    # 2. Update Section 4 text of Tran Sang in paragraphs
    for p in doc.paragraphs:
        if "4. Giáo viên: TRẦN SÁNG" in p.text or ("TRẦN SÁNG" in p.text and "Ưu điểm" in p.text):
            p.text = (
                "4. Giáo viên: TRẦN SÁNG (Môn Toán 6, Toán 9)\n"
                "• Tiến độ: Đã nộp bổ sung đủ 04 tiết của môn Toán 6, hoàn thành 100% tiến độ PPCT Tháng 9 với 32 tiết (155 trang PDF qua 4 phân môn).\n"
                "• Ưu điểm: Môn Toán 9 (Đại số và Hình học) soạn rất tốt, tích hợp NLS và AI in đậm nghiêng chuẩn mực. Môn Toán 6 phần bổ sung đã cập nhật đầy đủ mã NLS 5.3.TC1a và 3.1.TC1a khớp 100% Phụ lục 3. Toán học và phương pháp dạy học chuẩn mực.\n"
                "• Tồn tại, lưu ý: Tại Bài 7 Số học 6 (Trang 44), cần in đậm, nghiêng câu mô tả chỉ báo NLS theo đúng quy chế chuyên môn.\n"
                "• Kết luận: DUYỆT HỒ SƠ - XẾP LOẠI: KHÁ."
            )
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)
            break

    safe_save_doc(doc, doc_path)

update_bien_ban_to()

# ==============================================================================
# 3. CẬP NHẬT TỆP NHẬN XÉT HỆ THỐNG (Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.docx & .md)
# ==============================================================================
def update_system_comments_docx():
    doc_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.docx"
    doc = docx.Document(doc_path)
    
    # We will search and replace text for Tran Sang in paragraphs and table cells
    for p in doc.paragraphs:
        if "Phân môn Số học 6" in p.text and "TRẦN SÁNG" not in p.text:
            pass
            
    # In docx, the callouts are tables. Let's find tables that have Tran Sang's comments
    # Easier: rebuild or replace specific text in tables
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                # Replace So hoc 6 rejection
                if "HỒ SƠ CHƯA ĐẠT TIẾN ĐỘ THÁNG 9. Hiện tại mới nộp 09 tiết" in c.text:
                    p = c.paragraphs[0]
                    p.text = "👉 Nhận xét hệ thống (Copy & Paste): Kế hoạch bài dạy đã nộp bổ sung đầy đủ 03 tiết Tuần 4 (Tiết 10, 11 Bài 7 và Tiết 12 LTC), hoàn thành 100% tiến độ Tháng 9 (12 tiết). Kiến thức và các bước thực hiện phép tính chuẩn xác. Lưu ý: Cần in đậm, nghiêng câu mô tả Năng lực số (5.3.TC1a và 3.1.TC1a) tại Bài 7 theo đúng quy chế chuyên môn trước khi giảng dạy. Duyệt."
                    p.runs[0].font.name = "Times New Roman"
                    p.runs[0].font.size = Pt(11)
                # Replace Hinh hoc 6 rejection
                elif "HỒ SƠ CHƯA ĐẠT TIẾN ĐỘ THÁNG 9. Mới nộp 03 tiết" in c.text:
                    p = c.paragraphs[0]
                    p.text = "👉 Nhận xét hệ thống (Copy & Paste): Kế hoạch bài dạy đảm bảo đủ 04 tiết của 4 tuần tháng 9 theo đúng PPCT Phụ lục 3 (Bài 18 và Tiết 3, 4 Bài 19). Hình vẽ trực quan, phân chia hoạt động GV - HS rõ ràng. Duyệt."
                    p.runs[0].font.name = "Times New Roman"
                    p.runs[0].font.size = Pt(11)
                # Replace Overall package rejection
                elif "TRẢ HỒ SƠ. Môn Toán 9 (Đại số 9 và Hình học 9) soạn rất tốt" in c.text:
                    p = c.paragraphs[0]
                    p.text = "👉 Nhận xét hệ thống (Copy & Paste): DUYỆT HỒ SƠ (Xếp loại Khá). Giáo viên đã nộp bổ sung đầy đủ 04 tiết môn Toán 6, hoàn thành 100% tiến độ Tháng 9 với tổng cộng 32 tiết (155 trang). Tích hợp NLS và AI đầy đủ khớp Phụ lục 3. Nhắc nhở thầy Sáng in đậm, nghiêng nội dung NLS tại Bài 7 Số học 6 để hoàn thiện hồ sơ."
                    p.runs[0].font.name = "Times New Roman"
                    p.runs[0].font.size = Pt(11)

    # Also update paragraph status headers
    for p in doc.paragraphs:
        if "Phân môn Số học 6 (43 trang" in p.text:
            p.text = "• Phân môn Số học 6 (54 trang — 12 tiết: Bài 1 đến Bài 7 & LTC): [ĐẠT / DUYỆT (KHÁ)]"
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11.5); r.bold = True
        elif "Phân môn Hình học 6 (25 trang — 03 tiết" in p.text:
            p.text = "• Phân môn Hình học 6 (25 trang — 04 tiết: Bài 18 & Tiết 3, 4 Bài 19): [ĐẠT / DUYỆT]"
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11.5); r.bold = True
        elif "Nhận xét chung toàn bộ hồ sơ Thầy Trần Sáng (Duyệt theo gói): [TRẢ HỒ SƠ" in p.text:
            p.text = "• Nhận xét chung toàn bộ hồ sơ Thầy Trần Sáng (Duyệt theo gói): [DUYỆT - XẾP LOẠI KHÁ]"
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(11.5); r.bold = True

    safe_save_doc(doc, doc_path)

update_system_comments_docx()

# ==============================================================================
# 4. CẬP NHẬT CÁC FILE MARKDOWN (.md)
# ==============================================================================
def update_md_files():
    # 4.1 Update Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md
    md_sys_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md"
    with open(md_sys_path, "r", encoding="utf-8") as f:
        sys_txt = f.read()
        
    old_so6 = """### • Phân môn Số học 6 (43 trang — 09 tiết: Bài 1 đến Bài 6): [KHÔNG DUYỆT / TRẢ HỒ SƠ (THIẾU TUẦN 4)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `HỒ SƠ CHƯA ĐẠT TIẾN ĐỘ THÁNG 9. Hiện tại mới nộp 09 tiết (đến hết Bài 6), còn thiếu trọn vẹn Tuần 4 gồm 03 tiết: Tiết 10, 11 (Bài 7: Thứ tự thực hiện các phép tính) và Tiết 12 (Luyện tập chung) theo đúng PPCT Phụ lục 3. Đề nghị thầy soạn bổ sung đủ 03 tiết nộp lại tổ chuyên môn.`"""

    new_so6 = """### • Phân môn Số học 6 (54 trang — 12 tiết: Bài 1 đến Bài 7 & LTC): [ĐẠT / DUYỆT (KHÁ)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy đã nộp bổ sung đầy đủ 03 tiết Tuần 4 (Tiết 10, 11 Bài 7 và Tiết 12 LTC), hoàn thành 100% tiến độ Tháng 9 (12 tiết). Kiến thức và các bước thực hiện phép tính chuẩn xác. Lưu ý: Cần in đậm, nghiêng câu mô tả Năng lực số (5.3.TC1a và 3.1.TC1a) tại Bài 7 theo đúng quy chế chuyên môn trước khi giảng dạy. Duyệt.`"""

    old_hh6 = """### • Phân môn Hình học 6 (25 trang — 03 tiết: Bài 18 & Tiết 1 Bài 19): [KHÔNG DUYỆT / TRẢ HỒ SƠ (THIẾU TIẾT 4)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `HỒ SƠ CHƯA ĐẠT TIẾN ĐỘ THÁNG 9. Mới nộp 03 tiết (Bài 18 và hình chữ nhật, hình thoi), còn thiếu Tiết 4 của Tuần 4 (Tiết 2 Bài 19: Hình bình hành, hình thang cân) theo PPCT Phụ lục 3. Đề nghị thầy soạn bổ sung Tiết 4 nộp lại tổ chuyên môn.`"""

    new_hh6 = """### • Phân môn Hình học 6 (25 trang — 04 tiết: Bài 18 & Tiết 3, 4 Bài 19): [ĐẠT / DUYỆT]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `Kế hoạch bài dạy đảm bảo đủ 04 tiết của 4 tuần tháng 9 theo đúng PPCT Phụ lục 3 (Bài 18 và Tiết 3, 4 Bài 19). Hình vẽ trực quan, phân chia hoạt động GV - HS rõ ràng. Duyệt.`"""

    old_all_sang = """### • Nhận xét chung toàn bộ hồ sơ Thầy Trần Sáng (Duyệt theo gói): [TRẢ HỒ SƠ (BỔ SUNG 4 TIẾT TOÁN 6)]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `TRẢ HỒ SƠ. Môn Toán 9 (Đại số 9 và Hình học 9) soạn rất tốt, đủ và vượt tiến độ, tích hợp NLS/AI in đậm nghiêng chuẩn mực. Tuy nhiên môn Toán 6 chưa đảm bảo tiến độ tháng 9, còn thiếu tổng cộng 04 tiết của Tuần 4 (03 tiết Số học 6 và 01 tiết Hình học 6). Đề nghị thầy Trần Sáng bổ sung đủ 04 tiết nộp lại để phê duyệt hoàn thành hồ sơ tháng 9.`"""

    new_all_sang = """### • Nhận xét chung toàn bộ hồ sơ Thầy Trần Sáng (Duyệt theo gói): [DUYỆT - XẾP LOẠI KHÁ]
> **👉 Nhận xét hệ thống (Copy & Paste):**  
> `DUYỆT HỒ SƠ (Xếp loại Khá). Giáo viên đã nộp bổ sung đầy đủ 04 tiết môn Toán 6, hoàn thành 100% tiến độ Tháng 9 với tổng cộng 32 tiết (155 trang). Tích hợp NLS và AI đầy đủ khớp Phụ lục 3. Nhắc nhở thầy Sáng in đậm, nghiêng nội dung NLS tại Bài 7 Số học 6 để hoàn thiện hồ sơ.`"""

    sys_txt = sys_txt.replace("## 4. THẦY TRẦN SÁNG (MÔN TOÁN 6, TOÁN 9 — 28 TIẾT, 144 TRANG)", "## 4. THẦY TRẦN SÁNG (MÔN TOÁN 6, TOÁN 9 — 32 TIẾT, 155 TRANG)")
    sys_txt = sys_txt.replace(old_so6, new_so6)
    sys_txt = sys_txt.replace(old_hh6, new_hh6)
    sys_txt = sys_txt.replace(old_all_sang, new_all_sang)

    with open(md_sys_path, "w", encoding="utf-8") as f:
        f.write(sys_txt)
    print("SUCCESS: Updated Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_9.md")

    # 4.2 Update Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md
    md_bb_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md"
    with open(md_bb_path, "r", encoding="utf-8") as f:
        bb_txt = f.read()

    old_row_sang = "| 4 | **Trần Sáng** | Toán 6, Toán 9 | 28 tiết (144 tr) | Thiếu 04 tiết Tuần 4 môn Toán 6 | Đã tích hợp NLS/AI in đậm nghiêng chuẩn | **TRẢ HỒ SƠ** |"
    new_row_sang = "| 4 | **Trần Sáng** | Toán 6, Toán 9 | 32 tiết (155 tr) | Đã bổ sung đủ 100% Tháng 9; NLS khớp PL3 | Tích hợp NLS/AI đầy đủ | **DUYỆT (KHÁ)** |"
    bb_txt = bb_txt.replace(old_row_sang, new_row_sang)

    old_sec4 = """### 4. Thẩm định hồ sơ giáo viên: TRẦN SÁNG
- **Phân công giảng dạy**: Môn Toán 6 và Toán 9 (Sách Kết nối tri thức).
- **Tiến độ và khối lượng**: Nộp 04 tệp PDF gồm 144 trang, tổng cộng 28 tiết / 32 tiết quy định (Thiếu 04 tiết Tuần 4 môn Toán 6).
- **Ưu điểm**:
  + Môn Toán 9 (59 trang Đại số 9 và 17 trang Hình học 9) soạn rất công phu, chuẩn mực 4 hoạt động CV 5512, đủ 100% tiến độ tháng 9 và vượt tuần 5.
  + Tích hợp NLS (5.3.TC2a) và Năng lực AI (9.B2.1) tại Bài 1 Đại số 9 đúng địa chỉ và đã **_in đậm, nghiêng_** chuẩn mực.
  + Kiến thức toán học chính xác, ký hiệu góc chuẩn mực.
- **Tồn tại, hạn chế**:
  + Môn Toán 6 thiếu trọn vẹn Tuần 4 gồm 04 tiết: 03 tiết Số học 6 (Tiết 10, 11: Bài 7 và Tiết 12: Luyện tập chung); 01 tiết Hình học 6 (Tiết 4 của Tuần 4: Tiết 2 Bài 19: Hình bình hành, hình thang cân).
- **Kết luận thẩm định**: **TRẢ HỒ SƠ (Yêu cầu soạn bổ sung 04 tiết môn Toán 6 nộp lại tổ chuyên môn)**."""

    new_sec4 = """### 4. Thẩm định hồ sơ giáo viên: TRẦN SÁNG (THẨM ĐỊNH LẠI SAU BỔ SUNG)
- **Phân công giảng dạy**: Môn Toán 6 và Toán 9 (Sách Kết nối tri thức).
- **Tiến độ và khối lượng**: Nộp 04 tệp PDF gồm 155 trang, tổng cộng 32 tiết / 32 tiết quy định (Đã nộp bổ sung đủ 04 tiết Tuần 4 môn Toán 6, đạt 100% tiến độ PPCT Tháng 9).
- **Ưu điểm**:
  + Giáo viên tiếp thu ý kiến nhanh chóng, kịp thời bổ sung hoàn chỉnh các tiết còn thiếu. Môn Toán 9 (Đại số và Hình học) soạn rất tốt, tích hợp NLS và AI in đậm nghiêng chuẩn mực.
  + Môn Toán 6 phần bổ sung đã cập nhật đầy đủ mã NLS 5.3.TC1a và 3.1.TC1a khớp 100% Phụ lục 3. Toán học và phương pháp dạy học chuẩn mực.
- **Tồn tại, lưu ý**:
  + Tại Bài 7 Số học 6 (Trang 44), cần in đậm, nghiêng câu mô tả chỉ báo NLS theo đúng quy chế chuyên môn trước khi lưu hành giảng dạy.
- **Kết luận thẩm định**: **DUYỆT TOÀN BỘ HỒ SƠ - XẾP LOẠI: KHÁ**."""

    bb_txt = bb_txt.replace(old_sec4, new_sec4)

    with open(md_bb_path, "w", encoding="utf-8") as f:
        f.write(bb_txt)
    print("SUCCESS: Updated Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_9.md")

update_md_files()
print("RE-ASSESSMENT COMPLETED SUCCESSFULLY!")
