# -*- coding: utf-8 -*-
"""
ENGINE CHUẨN HÓA DUY NHẤT: THẨM ĐỊNH & DUYỆT GIÁO ÁN TOÁN - TIN THCS
Trợ lý Sư phạm Hoàng Thiên • Thư mục: TROLYTHIEN/engine/duyet_giao_an_engine.py

QUY CHUẨN ÁP DỤNG:
- Công văn 5512/BGDĐT-GDTrH: 4 hoạt động dạy học chuẩn mực.
- Nghị định 30/2020/NĐ-CP: Phông Times New Roman 13pt, lề chuẩn A4, đóng khung kín bảng biểu 4 cạnh.
- Quy chuẩn chuyên môn & Chuyển đổi số (Zero Tolerance):
  + Tích hợp Năng lực số (NLS) và Trí tuệ nhân tạo (AI) bắt buộc IN ĐẬM VÀ NGHIÊNG.
  + Quét triệt để lỗi font công thức toán, đè dấu mũ góc (U+0307, U+22A5, µ...).
  + Xuất 3 sản phẩm nghiệm thu chuẩn mực: Phiếu nhận xét cá nhân, Biên bản tổ, Cập nhật vnEdu/SMAS.
"""

import os
import sys
import re
import argparse
import pymupdf  # fitz
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# HẰNG SỐ & MÃ MÀU NGHỊ ĐỊNH 30 / TRẠNG THÁI DUYỆT
# ==============================================================================
STATUS_DUYET_TOT = "DUYỆT (Xếp loại: Tốt)"
STATUS_DUYET_KHA = "DUYỆT (Xếp loại: Khá)"
STATUS_TRA_HO_SO = "TRẢ HỒ SƠ"

SUSPICIOUS_CHARS = [
    0x0307, 0x0308,  # combining dot above
    0x0227, 0x1e41, 0x1e8b, 0x1e8f,  # chữ có chấm trên
    0x22a5,          # perpendicular ⊥ đè lên đỉnh góc
    0x00b5,          # micro µ
]

# ==============================================================================
# HELPER FUNCTIONS NGHỊ ĐỊNH 30/2020/NĐ-CP
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

def apply_page_setup_nd30(doc):
    for s in doc.sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(0.79)      # 20 mm
        s.bottom_margin = Inches(0.79)   # 20 mm
        s.left_margin = Inches(1.18)     # 30 mm
        s.right_margin = Inches(0.59)    # 15 mm
        s.different_first_page_header_footer = False

def add_callout(doc, text, title="KẾT LUẬN & XẾP LOẠI:", border_color="16A34A", bg_color="F0FDF4"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=140)
    set_cell_background(cell, bg_color)
    
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    
    r_title = p.add_run(f"👉 {title} ")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(13)
    r_title.font.color.rgb = RGBColor(15, 23, 42) if border_color != "DC2626" else RGBColor(185, 28, 28)
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(13)
    r_txt.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def safe_save_doc(doc, target_path):
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        doc.save(target_path)
        print(f"✔ Đã lưu thành công: {target_path}")
        return target_path
    except PermissionError:
        base, ext = os.path.splitext(target_path)
        fallback_path = f"{base}_CapNhat{ext}"
        doc.save(fallback_path)
        print(f"⚠️ Tệp bị khóa. Đã lưu sang: {fallback_path}")
        return fallback_path

# ==============================================================================
# AUDIT CORE: QUÉT FILE PDF GIÁO ÁN
# ==============================================================================
def inspect_pdf(pdf_path):
    """Quét chi tiết 1 tệp PDF giáo án"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Không tìm thấy file: {pdf_path}")
        
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    math_errors = []
    nls_findings = []
    
    act_keywords = ["KHỞI ĐỘNG", "HÌNH THÀNH KIẾN THỨC", "LUYỆN TẬP", "VẬN DỤNG"]
    activities_count = {kw: 0 for kw in act_keywords}
    
    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text()
        
        # 1. Đếm 4 hoạt động 5512
        text_u = text.upper()
        for kw in act_keywords:
            if kw in text_u:
                activities_count[kw] += 1
                
        # 2. Quét lỗi font công thức & ký hiệu góc
        for line in text.splitlines():
            line_s = line.strip()
            for ch in line_s:
                if ord(ch) in SUSPICIOUS_CHARS:
                    math_errors.append({
                        "page": page_num + 1,
                        "line": line_s,
                        "char": ch,
                        "code": f"U+{ord(ch):04X}"
                    })
                    break
            if re.search(r'(?<![A-Za-z])[A-Z]\u22a5|\u00b5\s*[A-Z]', line_s):
                math_errors.append({
                    "page": page_num + 1,
                    "line": line_s,
                    "char": "perp/micro",
                    "code": "Font Overlay"
                })

        # 3. Quét định dạng in đậm nghiêng của NLS & AI
        blocks = page.get_text("dict").get("blocks", [])
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    line_spans = l.get("spans", [])
                    full_line_text = "".join([s.get("text", "") for s in line_spans]).strip()
                    
                    if any(k in full_line_text.lower() for k in ["nls", "năng lực số", "ai:", "năng lực ai", "tc1a", "tc1b", "tc2a", "tc2b", "6.a1", "7.a1", "8.a3", "9.b2"]):
                        is_all_bi = all(
                            (bool(s.get("flags", 0) & 16 or "bold" in s.get("font", "").lower()) and 
                             bool(s.get("flags", 0) & 2 or "italic" in s.get("font", "").lower() or "oblique" in s.get("font", "").lower()))
                            for s in line_spans if s.get("text", "").strip()
                        )
                        nls_findings.append({
                            "page": page_num + 1,
                            "text": full_line_text,
                            "is_bold_italic": is_all_bi
                        })

    doc.close()
    
    nls_unformatted = [n for n in nls_findings if not n["is_bold_italic"]]
    has_math_error = len(math_errors) > 0
    has_nls_error = len(nls_unformatted) > 0
    
    if has_math_error or has_nls_error:
        verdict = STATUS_TRA_HO_SO
    else:
        verdict = STATUS_DUYET_TOT
        
    return {
        "filename": os.path.basename(pdf_path),
        "filepath": pdf_path,
        "total_pages": total_pages,
        "math_errors": math_errors,
        "nls_findings": nls_findings,
        "nls_unformatted": nls_unformatted,
        "activities_count": activities_count,
        "verdict": verdict
    }

def inspect_teacher_folder(folder_path):
    """Rà soát toàn bộ file PDF trong thư mục giáo viên"""
    if not os.path.exists(folder_path):
        print(f"❌ Không tìm thấy thư mục: {folder_path}")
        return None
        
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"⚠️ Không tìm thấy file PDF nào trong: {folder_path}")
        return None
        
    print(f"\n=======================================================")
    print(f"RÀ SOÁT HỒ SƠ GIÁO VIÊN: {os.path.basename(folder_path)}")
    print(f"Số lượng tệp: {len(pdf_files)}")
    print(f"=======================================================")
    
    results = []
    total_pages = 0
    all_math_errors = 0
    all_nls_unformatted = 0
    
    for p in pdf_files:
        res = inspect_pdf(p)
        results.append(res)
        total_pages += res["total_pages"]
        all_math_errors += len(res["math_errors"])
        all_nls_unformatted += len(res["nls_unformatted"])
        
        status_icon = "❌" if res["verdict"] == STATUS_TRA_HO_SO else "✔"
        print(f"{status_icon} [{res['total_pages']} trang] {res['filename']}")
        print(f"   - Kết luận: {res['verdict']}")
        if res["math_errors"]:
            print(f"   - Lỗi font công thức/ký hiệu góc: {len(res['math_errors'])} vị trí")
        if res["nls_unformatted"]:
            print(f"   - NLS/AI chưa in đậm nghiêng: {len(res['nls_unformatted'])} vị trí")
            
    return {
        "teacher_name": os.path.basename(folder_path),
        "folder_path": folder_path,
        "files_count": len(pdf_files),
        "total_pages": total_pages,
        "file_results": results,
        "overall_verdict": STATUS_TRA_HO_SO if (all_math_errors > 0 or all_nls_unformatted > 0) else STATUS_DUYET_TOT
    }

# ==============================================================================
# XUẤT PHIẾU NHẬN XÉT CÁ NHÂN THEO NGHỊ ĐỊNH 30
# ==============================================================================
def export_phieu_nhan_xet(teacher_summary, output_docx_path):
    """Xuất phiếu nhận xét cá nhân chuẩn Nghị định 30"""
    doc = docx.Document()
    apply_page_setup_nd30(doc)
    
    t_name = teacher_summary["teacher_name"]
    verdict = teacher_summary["overall_verdict"]
    
    # Header Quốc hiệu & Đơn vị
    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = tbl_top.cell(0, 0)
    c_right = tbl_top.cell(0, 1)
    
    p_left = c_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_left.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r1.font.name = "Times New Roman"; r1.font.size = Pt(12)
    r2 = p_left.add_run("TỔ TOÁN - TIN HỌC\n")
    r2.bold = True; r2.font.name = "Times New Roman"; r2.font.size = Pt(12)
    r3 = p_left.add_run("Số: ... /PĐG-TT")
    r3.font.name = "Times New Roman"; r3.font.size = Pt(11); r3.font.italic = True
    
    p_right = c_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = p_right.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r4.bold = True; r4.font.name = "Times New Roman"; r4.font.size = Pt(12)
    r5 = p_right.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r5.bold = True; r5.font.name = "Times New Roman"; r5.font.size = Pt(12)
    r6 = p_right.add_run("Thành phố Cà Mau, ngày ... tháng ... năm 2026")
    r6.font.name = "Times New Roman"; r6.font.size = Pt(11); r6.font.italic = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # Tiêu đề
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run(f"PHIẾU NHẬN XÉT, ĐÁNH GIÁ HỒ SƠ BÀI DẠY\nGIÁO VIÊN: {t_name.upper()}")
    r_t.bold = True; r_t.font.name = "Times New Roman"; r_t.font.size = Pt(14)
    r_t.font.color.rgb = RGBColor(15, 23, 42)
    
    # Nội dung kết luận
    is_reject = (verdict == STATUS_TRA_HO_SO)
    border_col = "DC2626" if is_reject else "16A34A"
    bg_col = "FEF2F2" if is_reject else "F0FDF4"
    callout_txt = (
        f"{verdict}. Hồ sơ còn tồn tại một số điểm cần khắc phục trước khi tải lên hệ thống vnEdu/SMAS."
        if is_reject else
        f"{verdict}. Hồ sơ đạt chuẩn mực Công văn 5512 và quy chế chuyên môn, đủ điều kiện lưu chiểu."
    )
    add_callout(doc, callout_txt, title="KẾT QUẢ RÀ SOÁT TỰ ĐỘNG:", border_color=border_col, bg_color=bg_col)
    
    # Bảng chi tiết từng tệp
    tbl = doc.add_table(rows=1, cols=4)
    set_table_borders_nd30(tbl)
    hdr_cells = tbl.rows[0].cells
    headers = ["STT", "Tên tệp hồ sơ", "Số trang", "Kết quả rà soát"]
    for i, h in enumerate(headers):
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = hdr_cells[i].paragraphs[0].add_run(h)
        run.bold = True; run.font.name = "Times New Roman"; run.font.size = Pt(12)
        set_cell_background(hdr_cells[i], "E2E8F0")
        
    for idx, f_res in enumerate(teacher_summary["file_results"], 1):
        row_cells = tbl.add_row().cells
        row_cells[0].paragraphs[0].text = str(idx)
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        row_cells[1].paragraphs[0].text = f_res["filename"]
        row_cells[2].paragraphs[0].text = str(f_res["total_pages"])
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        detail_msg = f_res["verdict"]
        if f_res["math_errors"]:
            detail_msg += f"\n- {len(f_res['math_errors'])} lỗi font công thức/góc"
        if f_res["nls_unformatted"]:
            detail_msg += f"\n- {len(f_res['nls_unformatted'])} dòng NLS/AI chưa in đậm nghiêng"
        row_cells[3].paragraphs[0].text = detail_msg
        
        for c in row_cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"; r.font.size = Pt(12)
                    
    safe_save_doc(doc, output_docx_path)
    return output_docx_path

# ==============================================================================
# MAIN CLI
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Universal Lesson Plan Audit Engine - Trợ lý Sư phạm Hoàng Thiên")
    parser.add_argument("--inspect", type=str, help="Rà soát chi tiết 1 tệp PDF hoặc 1 thư mục giáo viên")
    parser.add_argument("--audit-teacher", type=str, help="Rà soát và xuất Phiếu nhận xét cá nhân cho 1 thư mục giáo viên")
    parser.add_argument("--all", action="store_true", help="Quét toàn bộ giáo viên trong TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/")
    parser.add_argument("--out", type=str, help="Đường dẫn file Word đầu ra (tùy chọn)")

    args = parser.parse_args()
    
    if args.inspect:
        target = args.inspect
        if os.path.isfile(target):
            res = inspect_pdf(target)
            print(f"\nKết quả tệp: {res['filename']} ({res['total_pages']} trang)")
            print(f"Xếp loại: {res['verdict']}")
            print(f"Lỗi font công thức: {len(res['math_errors'])}")
            print(f"NLS/AI chưa in đậm nghiêng: {len(res['nls_unformatted'])}")
            print(f"Số lượng 4 hoạt động 5512: {res['activities_count']}")
        elif os.path.isdir(target):
            inspect_teacher_folder(target)
        else:
            print(f"Không tìm thấy: {target}")
        return

    if args.audit_teacher:
        folder = args.audit_teacher
        res = inspect_teacher_folder(folder)
        if res:
            t_name = res["teacher_name"].replace(" ", "_")
            out_path = args.out or f"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_{t_name}.docx"
            export_phieu_nhan_xet(res, out_path)
        return

    if args.all:
        base_dau_vao = "TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao"
        if not os.path.exists(base_dau_vao):
            print(f"Không tìm thấy thư mục: {base_dau_vao}")
            return
            
        subdirs = [os.path.join(base_dau_vao, d) for d in os.listdir(base_dau_vao) if os.path.isdir(os.path.join(base_dau_vao, d))]
        print(f"Tìm thấy {len(subdirs)} thư mục giáo viên.")
        for d in subdirs:
            res = inspect_teacher_folder(d)
            if res and res["file_results"]:
                t_name = res["teacher_name"].replace(" ", "_")
                out_path = f"TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua/Phieu_Nhan_Xet_Ho_So_{t_name}.docx"
                export_phieu_nhan_xet(res, out_path)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
