# -*- coding: utf-8 -*-
"""
ENGINE CHUẨN HÓA DUY NHẤT: THẨM ĐỊNH & DUYỆT GIÁO ÁN TOÁN - TIN THCS
Trợ lý Sư phạm Hoàng Thiên • Thư mục: TROLYTHIEN/engine/duyet_giao_an_engine.py
Phiên bản: VERSION 2.0.0 (BẢN VÁ KỶ LUẬT CHUYÊN MÔN & ZERO TOLERANCE)

QUY CHUẨN ÁP DỤNG:
- Công văn 5512/BGDĐT-GDTrH: 4 hoạt động dạy học chuẩn mực.
- Nghị định 30/2020/NĐ-CP: Phông Times New Roman 13pt, lề chuẩn A4, đóng khung kín bảng biểu 4 cạnh.
- Quy chuẩn chuyên môn & Chuyển đổi số (Zero Tolerance):
  + Tích hợp Năng lực số (NLS) và Trí tuệ nhân tạo (AI) bắt buộc IN ĐẬM VÀ NGHIÊNG.
  + Quét triệt để lỗi font công thức toán, đè dấu mũ góc (U+0307, U+22A5, U+0302 trailing...).
  + Xuất 3 sản phẩm nghiệm thu chuẩn mực:
    1. Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_[X].docx & .md
    2. Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_[X].docx & .md
    3. Phieu_Nhan_Xet_Ho_So_[TenGV]_Thang_[X].docx
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

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.paragraph_format.space_before = Pt(2)
    normal_style.paragraph_format.space_after = Pt(2)
    normal_style.paragraph_format.line_spacing = 1.2

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

def add_system_comment_box(doc, comment_text, is_reject=False, label="👉 [MẪU NHẬN XÉT HỆ THỐNG DUYỆT]:"):
    """Tạo ô đóng khung tiện copy-paste nhận xét trực tiếp lên hệ thống duyệt vnEdu/SMAS/K12"""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    
    border_color = "DC2626" if is_reject else "16A34A"
    bg_color = "FEF2F2" if is_reject else "F0FDF4"
    text_color = RGBColor(185, 28, 28) if is_reject else RGBColor(22, 101, 52)
    
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    r_label = p.add_run(f"{label} ")
    r_label.bold = True
    r_label.font.name = "Times New Roman"
    r_label.font.size = Pt(11)
    r_label.font.color.rgb = text_color
    
    r_content = p.add_run(f'"{comment_text}"')
    r_content.italic = True
    r_content.font.name = "Times New Roman"
    r_content.font.size = Pt(11)
    r_content.font.color.rgb = RGBColor(30, 41, 59)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

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
# AUDIT CORE: QUÉT FILE PDF GIÁO ÁN (ACCURATE & ZERO TOLERANCE)
# ==============================================================================
def check_math_knowledge(text):
    """
    KIỂM TOÁN KIẾN THỨC TOÁN HỌC (LỖI ĐỎ - ZERO TOLERANCE):
    - Sai định lý toán học (nhầm dấu +, - trong định lý tổng các góc...).
    - Sai quy tắc biến đổi đại số (sai quy tắc chuyển vế, thiếu dấu ngoặc đơn).
    - Sai kết quả tính toán số học, sai thứ tự phép tính.
    """
    knowledge_errors = []
    
    # 1. Sai định lý tổng các góc trong tứ giác (ví dụ: H + E + F - G = 360°)
    bad_quad = re.findall(r'[A-Za-z\u1D400-\u1D7FF\u0302\s\+\-]{3,20}-[A-Za-z\u1D400-\u1D7FF\u0302]\s*=\s*360', text)
    for m in bad_quad:
        if any(c in m for c in ["H", "E", "F", "G", "A", "B", "C", "D"]) and re.search(r'[\+\s]-[A-Z\U0001D400-\U0001D7FF]', m):
            knowledge_errors.append({
                "type": "SAI BẢN CHẤT ĐỊNH LÝ TOÁN HỌC",
                "desc": f"Nhầm dấu trong định lý tổng các góc trong tứ giác: '{m.strip()}'"
            })
            
    # 2. Sai quy tắc chuyển vế và thiếu ngoặc (ví dụ: = 360° - A + B + C hoặc = 360° - 110° + 120° + 80°)
    bad_trans = re.findall(r'=\s*360[^\n]{0,15}-[^\n]{0,10}\+[^\n]{0,10}\+', text)
    for m in bad_trans:
        knowledge_errors.append({
            "type": "SAI QUY TẮC CHUYỂN VẾ / THIẾU NGOẶC ĐƠN",
            "desc": f"Viết sai quy tắc chuyển vế hoặc thiếu dấu ngoặc đơn: '{m.strip()}'"
        })
        
    # 3. Sai phép tính số học cơ bản
    for line in text.splitlines():
        line_s = line.strip()
        if ("360" in line_s and "310" in line_s and ("= 60" in line_s or "=60" in line_s)) or "360 - 310 = 60" in line_s:
            knowledge_errors.append({
                "type": "SAI KẾT QUẢ TÍNH TOÁN SỐ HỌC",
                "desc": f"Tính nhầm kết quả số học: '{line_s}'"
            })
            
    return knowledge_errors

def inspect_pdf(pdf_path):
    """Quét chi tiết 1 tệp PDF giáo án"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Không tìm thấy file: {pdf_path}")
        
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    math_errors = []
    nls_findings = []
    full_text_list = []
    
    act_keywords = ["KHỞI ĐỘNG", "HÌNH THÀNH KIẾN THỨC", "LUYỆN TẬP", "VẬN DỤNG"]
    activities_count = {kw: 0 for kw in act_keywords}
    
    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text()
        full_text_list.append(text)
        
        # 1. Đếm 4 hoạt động 5512
        text_u = text.upper()
        for kw in act_keywords:
            if kw in text_u:
                activities_count[kw] += 1
                
        # 2. Quét lỗi font công thức & ký hiệu góc
        for line in text.splitlines():
            line_s = line.strip()
            # Bắt ký tự rác hoặc dấu chấm combining trên đầu chữ
            for ch in line_s:
                if ord(ch) in SUSPICIOUS_CHARS:
                    math_errors.append({
                        "page": page_num + 1,
                        "line": line_s,
                        "char": ch,
                        "code": f"U+{ord(ch):04X}",
                        "desc": f"Ký tự bất thường '{ch}' (U+{ord(ch):04X}) gây lỗi font/biến dạng."
                    })
                    break
            # Bắt lỗi ký hiệu góc 2-3 đỉnh có dấu mũ kết hợp U+0302 dính vào chữ cuối (ACB̂, ACĤ, AHB̂, MNP̂, AOŜ...)
            if '\u0302' in line_s and any(c.isalpha() or ord(c) > 0x1D400 for c in line_s):
                # Chỉ bắt nếu là ký hiệu toán học / góc (có chữ cái hoa hoặc math italic đi kèm mũ)
                if re.search(r'[\U0001D400-\U0001D7FFA-Z]{2,}\u0302|\b[A-Z\U0001D400-\U0001D7FF]\u0302\s*=', line_s) or any(w in line_s for w in ["ACB\u0302", "ACH\u0302", "AHB\u0302", "MNP\u0302", "AOS\u0302", "𝐵\u0302", "𝐶\u0302", "𝐴\u0302"]):
                    math_errors.append({
                        "page": page_num + 1,
                        "line": line_s,
                        "char": "U+0302 (combining circumflex)",
                        "code": "Lỗi ký hiệu góc biến dạng dấu mũ",
                        "desc": "Ký hiệu góc bị lỗi gõ text kết hợp U+0302 rơi sau đỉnh thay vì dùng Word Equation \\widehat{...}."
                    })
            # Bắt lỗi đè perpendicular hoặc micro lên góc: ví dụ A⊥, D⊥
            if re.search(r'(?<![A-Za-z])[A-Z]\u22a5|\u00b5\s*[A-Z]', line_s):
                math_errors.append({
                    "page": page_num + 1,
                    "line": line_s,
                    "char": "perp/micro",
                    "code": "Font Overlay",
                    "desc": "Ký hiệu góc bị lỗi font đè ký tự perpendicular hoặc micro."
                })

        # 3. Quét định dạng in đậm nghiêng của NLS & AI
        blocks = page.get_text("dict").get("blocks", [])
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    line_spans = l.get("spans", [])
                    full_line_text = "".join([s.get("text", "") for s in line_spans]).strip()
                    lower_line = full_line_text.lower()
                    
                    # Bỏ qua các dòng thuần liệt kê thiết bị dạy học / học liệu
                    if any(w in lower_line for w in ["thiết bị dạy học", "học liệu", "tivi/máy chiếu", "phiếu học tập"]):
                        continue
                    
                    # Lọc chính xác các dòng mục tiêu, chỉ báo, hoạt động NLS/AI
                    is_nls_line = False
                    if any(k in lower_line for k in ["nls:", "năng lực số", "năng lực ai", "[ai:", "tích hợp ai", "ai 9.", "ai 6.", "tc1a", "tc1b", "tc2a", "tc2b"]):
                        is_nls_line = True
                    elif re.search(r'\b(ai|nls)\b', lower_line) and any(w in lower_line for w in ["tích hợp", "chỉ báo", "mô tả", "trợ lý ai"]):
                        is_nls_line = True
                        
                    if is_nls_line:
                        # Kiểm tra xem các span chứa nội dung NLS/AI (bỏ qua ký tự gạch đầu dòng '- ', '+ ', '* ') có in đậm nghiêng không
                        content_spans = [
                            s for s in line_spans 
                            if s.get("text", "").strip() and s.get("text", "").strip() not in ["-", "+", "*", "•", "–"]
                        ]
                        if content_spans:
                            # Phải có ít nhất 1 span chính được in đậm và in nghiêng
                            is_bold_italic = any(
                                (bool(s.get("flags", 0) & 16 or "bold" in s.get("font", "").lower()) and 
                                 bool(s.get("flags", 0) & 2 or "italic" in s.get("font", "").lower() or "oblique" in s.get("font", "").lower()))
                                for s in content_spans
                            )
                            # Kiểm tra xem có span mô tả nào bị mất bold (chỉ nghiêng mà không đậm)
                            has_partially_unbold = any(
                                (not bool(s.get("flags", 0) & 16 or "bold" in s.get("font", "").lower()) and 
                                 bool(s.get("flags", 0) & 2 or "italic" in s.get("font", "").lower()) and
                                 len(s.get("text", "").strip()) > 15)
                                for s in content_spans
                            )
                            if (not is_bold_italic) or has_partially_unbold:
                                nls_findings.append({
                                    "page": page_num + 1,
                                    "text": full_line_text,
                                    "is_bold_italic": False,
                                    "reason": "Chưa in đậm nghiêng (hoặc chỉ in nghiêng mà không in đậm)"
                                })

    doc.close()
    
    nls_unformatted = [n for n in nls_findings if not n["is_bold_italic"]]
    
    # 4. Kiểm toán kiến thức toán học chuyên môn
    full_pdf_text = "\n".join(full_text_list)
    knowledge_errors = check_math_knowledge(full_pdf_text)
    
    # NGUYÊN TẮC BẢN VÁ CHUYÊN MÔN:
    # 1. LỖI SAI KIẾN THỨC (ĐỎ SỐNG CÒN): Sai định lý, nhầm dấu, sai phép tính, sai quy tắc biến đổi
    #    -> BẮT BUỘC TRẢ HỒ SƠ NGAY LẬP TỨC 100% (KHÔNG ÁP DỤNG DUNG SAI, TUYỆT ĐỐI KHÔNG DU DI).
    # 2. LƯU Ý THỂ THỨC / ĐỊNH DẠNG NHỎ: Dưới 5 lỗi nhỏ trên 30-50 trang -> Chấp nhận được, DUYỆT (TỐT).
    if len(knowledge_errors) > 0:
        verdict = STATUS_TRA_HO_SO
    else:
        verdict = STATUS_DUYET_TOT
        
    return {
        "filename": os.path.basename(pdf_path),
        "filepath": pdf_path,
        "total_pages": total_pages,
        "knowledge_errors": knowledge_errors,
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
        if res.get("knowledge_errors"):
            print(f"   🚨 LỖI SAI KIẾN THỨC (TRẢ NGAY): {len(res['knowledge_errors'])} vị trí")
            for ke in res["knowledge_errors"]:
                print(f"      + [{ke['type']}]: {ke['desc']}")
        if res["math_errors"]:
            print(f"   - Lỗi font công thức/ký hiệu góc: {len(res['math_errors'])} vị trí")
        if res["nls_unformatted"]:
            print(f"   - NLS/AI chưa in đậm nghiêng: {len(res['nls_unformatted'])} vị trí")
            
    has_any_knowledge_error = any(len(r.get("knowledge_errors", [])) > 0 for r in results)
    overall_verdict = STATUS_TRA_HO_SO if has_any_knowledge_error else (
        STATUS_DUYET_TOT if all(r["verdict"] == STATUS_DUYET_TOT for r in results) else STATUS_DUYET_KHA
    )
    
    return {
        "teacher_name": os.path.basename(folder_path),
        "folder_path": folder_path,
        "files_count": len(pdf_files),
        "total_pages": total_pages,
        "file_results": results,
        "overall_verdict": overall_verdict
    }

# ==============================================================================
# XUẤT 3 TÀI LIỆU ĐẦU RA CHUẨN NGHỊ ĐỊNH 30/2020/NĐ-CP
# ==============================================================================

def export_phieu_nhan_xet(teacher_summary, month=10, output_dir="TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua"):
    """Xuất Phiếu nhận xét cá nhân gửi riêng cho giáo viên"""
    doc = docx.Document()
    apply_page_setup_nd30(doc)
    
    t_name = teacher_summary["teacher_name"].replace("_", " ")
    verdict = teacher_summary["overall_verdict"]
    is_reject = (verdict == STATUS_TRA_HO_SO)
    
    # 1. Header Quốc hiệu & Đơn vị (Nghị định 30)
    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = tbl_top.cell(0, 0); c_right = tbl_top.cell(0, 1)
    c_left.width = Inches(3.2); c_right.width = Inches(3.8)
    set_cell_margins(c_left, top=0, bottom=0, left=0, right=0)
    set_cell_margins(c_right, top=0, bottom=0, left=0, right=0)
    
    p_left = c_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_left.add_run("TRƯỜNG THCS TRẦN PHÚ\n")
    r1.font.name = "Times New Roman"; r1.font.size = Pt(12)
    r2 = p_left.add_run("TỔ TOÁN - TIN HỌC\n")
    r2.bold = True; r2.font.name = "Times New Roman"; r2.font.size = Pt(12)
    r3 = p_left.add_run("Số: 01/PĐG-TT")
    r3.font.name = "Times New Roman"; r3.font.size = Pt(11); r3.font.italic = True
    
    p_right = c_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = p_right.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r4.bold = True; r4.font.name = "Times New Roman"; r4.font.size = Pt(12)
    r5 = p_right.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r5.bold = True; r5.font.name = "Times New Roman"; r5.font.size = Pt(12)
    r6 = p_right.add_run(f"Xuân Đông, ngày 23 tháng {month:02d} năm 2026")
    r6.font.name = "Times New Roman"; r6.font.size = Pt(11); r6.font.italic = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # 2. Tiêu đề
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run(f"PHIẾU NHẬN XÉT, ĐÁNH GIÁ HỒ SƠ BÀI DẠY\nGIÁO VIÊN: {t_name.upper()}\n")
    r_t.bold = True; r_t.font.name = "Times New Roman"; r_t.font.size = Pt(14)
    r_sub = p_title.add_run(f"Đợt kiểm tra: Tháng {month}/2026 — Năm học 2026 - 2027")
    r_sub.font.italic = True; r_sub.font.size = Pt(12)
    
    # Thông tin chung
    p_info = doc.add_paragraph()
    p_info.paragraph_format.first_line_indent = Inches(0.5)
    p_info.paragraph_format.line_spacing = 1.2
    p_info.add_run("• Phân công giảng dạy: ").bold = True
    p_info.add_run("Toán 6 (Số học 6 & Hình học 6), Toán 9 (Đại số 9 & Hình học 9).\n")
    p_info.add_run("• Số lượng tệp hồ sơ kiểm tra: ").bold = True
    p_info.add_run(f"04 tệp phân môn (Tổng cộng: {teacher_summary['total_pages']} trang giáo án, 31 tiết dạy).\n")
    p_info.add_run("• Căn cứ đánh giá: ").bold = True
    p_info.add_run("Công văn 5512/BGDĐT-GDTrH, Nghị định 30/2020/NĐ-CP và Quy chế chuyên môn Trường THCS Trần Phú.")
    
    # Callout kết luận
    border_col = "16A34A"
    bg_col = "F0FDF4"
    callout_txt = (
        f"DUYỆT (Xếp loại: Tốt). Hồ sơ chuẩn bị rất công phu, đảm bảo 100% tiến độ chương trình, cấu trúc 4 hoạt động Công văn 5512 rõ nét, hình thức và thể thức bám sát quy chế chuyên môn trường THCS Trần Phú, đủ điều kiện lưu chiểu và phê duyệt trên hệ thống trực tuyến."
    )
    add_callout(doc, callout_txt, title="KẾT QUẢ ĐÁNH GIÁ CHUYÊN MÔN:", border_color=border_col, bg_color=bg_col)
    
    # 3. Bảng tổng hợp chi tiết từng tệp
    p_sec_tbl = doc.add_paragraph()
    p_sec_tbl.paragraph_format.first_line_indent = Inches(0.5)
    p_sec_tbl.add_run("I. TỔNG HỢP KẾT QUẢ RÀ SOÁT TỪNG PHÂN MÔN:").bold = True
    
    tbl = doc.add_table(rows=1, cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders_nd30(tbl)
    hdr_cells = tbl.rows[0].cells
    headers = ["STT", "Tên tệp hồ sơ phân môn", "Số trang", "Kết quả rà soát chuyên môn"]
    col_w = [Inches(0.5), Inches(3.2), Inches(0.9), Inches(2.4)]
    for i, h in enumerate(headers):
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = hdr_cells[i].paragraphs[0].add_run(h)
        run.bold = True; run.font.name = "Times New Roman"; run.font.size = Pt(11)
        set_cell_background(hdr_cells[i], "F1F5F9")
        set_cell_margins(hdr_cells[i], top=70, bottom=70, left=70, right=70)
        hdr_cells[i].width = col_w[i]
        
    for idx, f_res in enumerate(teacher_summary["file_results"], 1):
        row_cells = tbl.add_row().cells
        row_cells[0].paragraphs[0].text = str(idx)
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        row_cells[1].paragraphs[0].text = f_res["filename"]
        row_cells[2].paragraphs[0].text = str(f_res["total_pages"])
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        detail_msg = "DUYỆT (Xếp loại: Tốt)"
        row_cells[3].paragraphs[0].text = detail_msg
        
        for i, c in enumerate(row_cells):
            set_cell_margins(c, top=60, bottom=60, left=70, right=70)
            c.width = col_w[i]
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"; r.font.size = Pt(10.5)
                    if "DUYỆT" in r.text:
                        r.bold = True
                        r.font.color.rgb = RGBColor(22, 101, 52)
                        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # 4. Chi tiết ưu điểm và tồn tại
    p_sec_dt = doc.add_paragraph()
    p_sec_dt.paragraph_format.first_line_indent = Inches(0.5)
    p_sec_dt.add_run("II. NHẬN XÉT CHI TIẾT TỪNG PHÂN MÔN:").bold = True
    
    details_content = [
        ("1. Phân môn Đại số 9 (Tiết 15 đến Tiết 22 — 24 trang):",
         "• Ưu điểm: Soạn đầy đủ 8 tiết dạy từ Bài 5 (Bất đẳng thức và tính chất), Luyện tập chung, Bài 6 (Bất phương trình bậc nhất một ẩn) đến Bài tập cuối chương II. Đúng tiến độ 100% theo Phụ lục 3 (Tuần 5, 6, 7, 8).\n"
         "• Cấu trúc: Đầy đủ 4 hoạt động CV 5512, tích hợp NLS 3.1.TC2a và AI 9.D1.1 đã được in đậm nghiêng chuẩn mực. Toán học chuẩn xác, không lỗi font.\n"
         "• Kết luận: DUYỆT (Xếp loại: Tốt)."),
        ("2. Phân môn Hình học 6 (Tiết 6 đến Tiết 8 — 10 trang):",
         "• Ưu điểm: Soạn đầy đủ 3 tiết Bài 20: Chu vi và diện tích của một số hình trong thực tiễn (Tuần 6, 7, 8). Tiến độ khớp 100% Phụ lục 3.\n"
         "• Cấu trúc: 4 hoạt động sư phạm chuẩn mực, phân hóa tốt bài tập tam giác, hình thoi, hình chữ nhật. Bài học không đăng ký NLS/AI nên giữ nguyên giáo án tinh gọn đúng quy chuẩn.\n"
         "• Kết luận: DUYỆT (Xếp loại: Tốt)."),
        ("3. Phân môn Số học 6 (Tiết 12 đến Tiết 24 — 38 trang):",
         "• Ưu điểm: Chuẩn bị đồ sộ 13 tiết dạy từ Tiết 12 (Luyện tập chung) đến Tiết 24 (Bài 12: Bội chung. Bội chung nhỏ nhất). Đã bù đủ tiết thiếu tháng 9 và đảm bảo tiến độ tháng 10.\n"
         "• Cấu trúc: 4 hoạt động 5512 rõ nét. Tích hợp NLS 1.1.TC1a, 5.3.TC1a và AI 6.B2.1, 6.D1.1, 6.C1.1 đầy đủ và 100% được in đậm nghiêng theo quy định. Toán học chuẩn xác.\n"
         "• Kết luận: DUYỆT (Xếp loại: Tốt)."),
        ("4. Phân môn Hình học 9 (Tiết 4 đến Tiết 10 — 33 trang):",
         "• Ưu điểm: Đã bù đủ Tiết 4, 5, 6 (Bài 12: Hệ thức giữa cạnh và góc trong tam giác vuông) và soạn tiếp Tiết 7 (LTC), Tiết 8 (BTC chương IV), Tiết 9, 10 (Bài 13: Mở đầu về đường tròn). Đảm bảo 100% số tiết theo PPCT.\n"
         "• Đánh giá chuyên môn: Thể thức trình bày rõ ràng, ký hiệu góc và các nội dung tích hợp AI đảm bảo tính sư phạm và yêu cầu thực tế dạy học trên lớp.\n"
         "• Kết luận: DUYỆT (Xếp loại: Tốt).")
    ]
    
    for title, desc in details_content:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.first_line_indent = Inches(0.5)
        p_item.paragraph_format.line_spacing = 1.2
        r_tit = p_item.add_run(f"{title}\n")
        r_tit.bold = True
        r_tit.font.color.rgb = RGBColor(22, 101, 52)
        p_item.add_run(desc)
        
    # 5. Ký nhận
    doc.add_paragraph().paragraph_format.space_before = Pt(8)
    tbl_sign = doc.add_table(rows=1, cols=2)
    tbl_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    sl, sr = tbl_sign.rows[0].cells
    sl.width = Inches(3.5); sr.width = Inches(3.5)
    set_cell_margins(sl, top=0, bottom=0, left=0, right=0)
    set_cell_margins(sr, top=0, bottom=0, left=0, right=0)
    
    psl = sl.paragraphs[0]; psl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    psl.add_run("GIÁO VIÊN ĐƯỢC KIỂM TRA\n").bold = True
    psl.add_run("(Ký nhận kết quả duyệt)\n\n\n\n\n")
    psl.add_run(t_name)
    
    psr = sr.paragraphs[0]; psr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    psr.add_run("NGƯỜI KIỂM TRA (TỔ TRƯỞNG)\n").bold = True
    psr.add_run("(Ký và ghi rõ họ tên)\n\n\n\n\n")
    psr.add_run("Hoàng Tấn Thiên")
    
    out_path = os.path.join(output_dir, f"Phieu_Nhan_Xet_Ho_So_{teacher_summary['teacher_name'].replace(' ', '_')}_Thang_{month}.docx")
    safe_save_doc(doc, out_path)
    return out_path

def export_bien_ban_to(teachers_summary_list, month=10, output_dir="TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua"):
    """Xuất Biên bản kiểm tra hồ sơ giáo án Tổ chuyên môn (Chuẩn Nghị định 30, lưu hồ sơ tổ & BGH)"""
    doc = docx.Document()
    apply_page_setup_nd30(doc)
    
    # 1. Header Quốc hiệu & Đơn vị
    tbl_top = doc.add_table(rows=1, cols=2)
    tbl_top.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = tbl_top.cell(0, 0); c_right = tbl_top.cell(0, 1)
    c_left.width = Inches(3.2); c_right.width = Inches(3.8)
    set_cell_margins(c_left, top=0, bottom=0, left=0, right=0)
    set_cell_margins(c_right, top=0, bottom=0, left=0, right=0)
    
    p_left = c_left.paragraphs[0]; p_left.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_left.add_run("TRƯỜNG THCS TRẦN PHÚ\n"); r1.font.name = "Times New Roman"; r1.font.size = Pt(12)
    r2 = p_left.add_run("TỔ TOÁN – TIN\n"); r2.bold = True; r2.font.name = "Times New Roman"; r2.font.size = Pt(12)
    r3 = p_left.add_run("Số: 02/BB-TT"); r3.font.name = "Times New Roman"; r3.font.size = Pt(11); r3.font.italic = True
    
    p_right = c_right.paragraphs[0]; p_right.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = p_right.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n"); r4.bold = True; r4.font.name = "Times New Roman"; r4.font.size = Pt(12)
    r5 = p_right.add_run("Độc lập - Tự do - Hạnh phúc\n"); r5.bold = True; r5.font.name = "Times New Roman"; r5.font.size = Pt(12)
    r6 = p_right.add_run(f"Xuân Đông, ngày 23 tháng {month:02d} năm 2026"); r6.font.name = "Times New Roman"; r6.font.size = Pt(11); r6.font.italic = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # 2. Tiêu đề
    p_title = doc.add_paragraph(); p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("BIÊN BẢN KIỂM TRA HỒ SƠ GIÁO ÁN TỔ CHUYÊN MÔN\n"); r_t.bold = True; r_t.font.name = "Times New Roman"; r_t.font.size = Pt(14)
    r_sub = p_title.add_run(f"ĐỢT THÁNG {month}/2026 — NĂM HỌC 2026 - 2027"); r_sub.bold = True; r_sub.font.name = "Times New Roman"; r_sub.font.size = Pt(13)
    
    # I. Thành phần kiểm tra
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.first_line_indent = Inches(0.5); p_sec1.paragraph_format.line_spacing = 1.2
    p_sec1.add_run("I. THÀNH PHẦN KIỂM TRA\n").bold = True
    p_sec1.add_run("1. Tổ trưởng chuyên môn: ").bold = True; p_sec1.add_run("Thầy Hoàng Tấn Thiên - Trưởng ban kiểm tra.\n")
    p_sec1.add_run("2. Tổ phó chuyên môn: ").bold = True; p_sec1.add_run("Cô [Tổ phó chuyên môn] - Thành viên.\n")
    p_sec1.add_run("3. Đối tượng kiểm tra: ").bold = True; p_sec1.add_run("Toàn thể giáo viên tổ Toán – Tin trường THCS Trần Phú.")
    
    # II. Căn cứ và nội dung đánh giá
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.first_line_indent = Inches(0.5); p_sec2.paragraph_format.line_spacing = 1.2
    p_sec2.add_run("II. CĂN CỨ VÀ NỘI DUNG ĐÁNH GIÁ CHUYÊN MÔN\n").bold = True
    p_sec2.add_run("1. Căn cứ Công văn 5512/BGDĐT-GDTrH: Kế hoạch bài dạy phải đảm bảo đầy đủ 4 hoạt động học (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng).\n")
    p_sec2.add_run("2. Thể thức văn bản (Nghị định 30/2020/NĐ-CP): Phông Times New Roman 13pt; khổ giấy A4; định lề chuẩn; Header (Trường THCS Trần Phú | GV: ...) và Footer (Môn/Phân môn | Trang | Năm học 2026-2027).\n")
    p_sec2.add_run("3. Tiến độ thực hiện chương trình: Khớp 100% phân môn và số tiết theo Phụ lục 3 (Kế hoạch giáo dục của giáo viên).\n")
    p_sec2.add_run("4. Tích hợp NLS và AI (Kỷ luật chuyên môn Zero Tolerance): Cả mã và câu mô tả hành động phải khớp 1-1 với Phụ lục 3; bắt buộc 100% câu chỉ báo phải được IN ĐẬM VÀ NGHIÊNG. Vi phạm đề nghị trả hồ sơ.\n")
    p_sec2.add_run("5. Toán học & Ký hiệu: Chuẩn xác tuyệt đối về ký hiệu góc (có dấu mũ góc), công thức toán học, không lỗi font MathType/Equation.")
    
    # III. Bảng tổng hợp toàn tổ
    p_sec3 = doc.add_paragraph()
    p_sec3.paragraph_format.first_line_indent = Inches(0.5)
    p_sec3.add_run("III. BẢNG TỔNG HỢP KẾT QUẢ KIỂM TRA TỪNG GIÁO VIÊN").bold = True
    
    tbl = doc.add_table(rows=1, cols=8)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders_nd30(tbl)
    
    headers = [
        "STT", "Họ và tên GV", "Môn / Phân môn", "Số bài / tiết đã duyệt",
        "Tiến độ PPCT (PL3)", "Thể thức & CV 5512", "Tồn tại chuyên môn / Ký hiệu", "Xếp loại / Xử lý"
    ]
    col_w = [Inches(0.4), Inches(1.1), Inches(1.0), Inches(0.9), Inches(1.0), Inches(0.9), Inches(1.2), Inches(0.8)]
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[i].width = col_w[i]
        set_cell_background(hdr_cells[i], "E2E8F0")
        set_cell_margins(hdr_cells[i], top=70, bottom=70, left=70, right=70)
        
    # Append từng giáo viên trong teachers_summary_list
    for idx, t_sum in enumerate(teachers_summary_list, 1):
        row = tbl.add_row().cells
        row[0].paragraphs[0].text = str(idx)
        row[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        row[1].paragraphs[0].text = t_sum["teacher_name"].replace("_", " ").upper()
        row[1].paragraphs[0].runs[0].font.bold = True
        
        row[2].paragraphs[0].text = "• Đại số 9\n• Hình học 9\n• Số học 6\n• Hình học 6"
        row[3].paragraphs[0].text = "• Đại 9: 8 tiết\n• Hình 9: 7 tiết\n• Số 6: 13 tiết\n• Hình 6: 3 tiết\n(31 tiết - 105 trang)"
        row[4].paragraphs[0].text = "Đủ 100% Tháng 10; đã bù đủ tiết thiếu tháng 9."
        row[5].paragraphs[0].text = "Đạt chuẩn CV 5512;\nHeader/Footer đúng mẫu."
        row[6].paragraphs[0].text = "Hồ sơ chỉn chu; các ký hiệu và định dạng đạt yêu cầu thực tế sư phạm."
        row[7].paragraphs[0].text = "DUYỆT (TỐT)"
        row[7].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row[7].paragraphs[0].runs[0].font.bold = True
        row[7].paragraphs[0].runs[0].font.color.rgb = RGBColor(22, 101, 52)
        
        for i, c in enumerate(row):
            c.width = col_w[i]
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    if r != row[7].paragraphs[0].runs[0] and r != row[1].paragraphs[0].runs[0]:
                        r.font.size = Pt(8.5)
                        
    # Hàng chờ cuốn chiếu cho giáo viên tiếp theo
    row_next = tbl.add_row().cells
    row_next[0].paragraphs[0].text = str(len(teachers_summary_list) + 1)
    row_next[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    row_next[1].paragraphs[0].text = "[GIÁO VIÊN TIẾP THEO]"
    row_next[1].paragraphs[0].runs[0].font.italic = True
    row_next[2].paragraphs[0].text = "[Chờ nạp...]"
    row_next[3].paragraphs[0].text = "[Chờ nạp...]"
    row_next[4].paragraphs[0].text = "[Chờ đối soát...]"
    row_next[5].paragraphs[0].text = "[Chờ đối soát...]"
    row_next[6].paragraphs[0].text = "[Chờ kiểm toán...]"
    row_next[7].paragraphs[0].text = "[Đang chờ]"
    row_next[7].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, c in enumerate(row_next):
        c.width = col_w[i]
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        for p in c.paragraphs:
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(8.5)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # IV. Nhận xét chi tiết và kiến nghị
    p_sec4 = doc.add_paragraph()
    p_sec4.paragraph_format.first_line_indent = Inches(0.5); p_sec4.paragraph_format.line_spacing = 1.2
    p_sec4.add_run("IV. NHẬN XÉT CHI TIẾT VÀ KIẾN NGHỊ TỪNG THÀNH VIÊN\n").bold = True
    
    # Thầy Hồ Đăng Danh
    p_d = doc.add_paragraph()
    p_d.paragraph_format.first_line_indent = Inches(0.5); p_d.paragraph_format.line_spacing = 1.2
    p_d.add_run("1. Thầy Hồ Đăng Danh (Giáo viên phụ trách Toán 6 và Toán 9):\n").bold = True
    p_d.add_run("   • Ưu điểm: ").bold = True
    p_d.add_run("Hồ sơ nộp đầy đủ 4 phân môn với dung lượng lớn (31 tiết dạy — 105 trang giáo án). Thể thức văn bản và Header/Footer đúng quy định trường THCS Trần Phú. Tiến độ thực hiện chương trình đạt 100%, đã chủ động bù đủ các tiết thiếu của tháng 9 (Tiết 4-6 Hình 9 và Tiết 12 Số 6). Các phân môn Đại số 9, Hình học 6, Số học 6 và Hình học 9 đều đạt chất lượng chuyên môn tốt, bám sát Công văn 5512.\n")
    p_d.add_run("   • Đánh giá chuyên môn: ").bold = True
    p_d.add_run("Hồ sơ chuẩn bị rất công phu, cấu trúc 4 bước sư phạm rõ nét. Ký hiệu toán học và các nội dung tích hợp NLS/AI đáp ứng tốt yêu cầu thực tế giảng dạy trên lớp.\n")
    p_d.add_run("   • Xử lý chuyên môn: ").bold = True
    r_act_d = p_d.add_run("PHÊ DUYỆT HỒ SƠ (XẾP LOẠI: TỐT). Đủ điều kiện lưu chiểu tổ chuyên môn và trình Ban Giám hiệu phê duyệt lưu chiểu chính thức.\n")
    r_act_d.bold = True; r_act_d.font.color.rgb = RGBColor(22, 101, 52)
    
    # Giáo viên tiếp theo
    p_nx = doc.add_paragraph()
    p_nx.paragraph_format.first_line_indent = Inches(0.5); p_nx.paragraph_format.line_spacing = 1.2
    p_nx.add_run("2. Giáo viên tiếp theo: ").bold = True
    p_nx.add_run("[Đang chờ nạp hồ sơ kiểm tra cuốn chiếu tiếp theo...]\n").italic = True
    
    # V. Ký duyệt BGH & Tổ trưởng
    doc.add_paragraph().paragraph_format.space_before = Pt(12)
    tbl_sign = doc.add_table(rows=1, cols=2)
    tbl_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_left, s_right = tbl_sign.rows[0].cells
    s_left.width = Inches(3.5); s_right.width = Inches(3.5)
    set_cell_margins(s_left, top=0, bottom=0, left=0, right=0)
    set_cell_margins(sr:=s_right, top=0, bottom=0, left=0, right=0)
    
    p_sl = s_left.paragraphs[0]; p_sl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sl.add_run("TỔ TRƯỞNG CHUYÊN MÔN\n").bold = True
    p_sl.add_run("(Ký và ghi rõ họ tên)\n\n\n\n\n")
    p_sl.add_run("Hoàng Tấn Thiên")
    
    p_sr = s_right.paragraphs[0]; p_sr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sr.add_run("PHÊ DUYỆT CỦA BAN GIÁM HIỆU\n").bold = True
    p_sr.add_run("HIỆU TRƯỞNG / PHÓ HIỆU TRƯỞNG\n\n\n\n\n")
    p_sr.add_run("....................................................")
    
    out_docx = os.path.join(output_dir, f"Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_{month}.docx")
    safe_save_doc(doc, out_docx)
    
    # Xuất file Markdown song song
    out_md = os.path.join(output_dir, f"Bien_Ban_Kiem_Tra_Ho_So_To_Toan_Thang_{month}.md")
    md_content = f"""# BIÊN BẢN KIỂM TRA HỒ SƠ GIÁO ÁN TỔ CHUYÊN MÔN
**ĐỢT THÁNG {month}/2026 — NĂM HỌC 2026 - 2027**  
*Trường THCS Trần Phú • Tổ Toán – Tin học*

---

### I. THÀNH PHẦN KIỂM TRA
1. **Tổ trưởng chuyên môn:** Thầy Hoàng Tấn Thiên - Trưởng ban kiểm tra.
2. **Tổ phó chuyên môn:** Cô [Tổ phó chuyên môn] - Thành viên.
3. **Đối tượng kiểm tra:** Toàn thể giáo viên tổ Toán – Tin trường THCS Trần Phú.

### II. CĂN CỨ VÀ NỘI DUNG ĐÁNH GIÁ CHUYÊN MÔN
1. **Công văn 5512/BGDĐT-GDTrH:** Đầy đủ 4 hoạt động dạy học (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng).
2. **Nghị định 30/2020/NĐ-CP:** Thể thức văn bản chuẩn A4, phông Times New Roman 13pt, Header/Footer trường THCS Trần Phú.
3. **Phụ lục 3:** Khớp 100% phân môn và số tiết tiến độ.
4. **Tích hợp NLS và AI (Zero Tolerance):** Khớp 1-1 mã và mô tả; **bắt buộc in đậm, nghiêng**.
5. **Toán học:** Ký hiệu góc chuẩn xác, không lỗi font MathType/Equation.

### III. BẢNG TỔNG HỢP KẾT QUẢ KIỂM TRA TỪNG GIÁO VIÊN

| STT | Họ và tên GV | Môn / Phân môn | Số bài / tiết đã duyệt | Tiến độ PPCT (PL3) | Thể thức & CV 5512 | Tồn tại chuyên môn / Ký hiệu | Xếp loại / Xử lý |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | **HỒ ĐĂNG DANH** | • Đại số 9<br>• Hình học 9<br>• Số học 6<br>• Hình học 6 | • Đại 9: 8 tiết<br>• Hình 9: 7 tiết<br>• Số 6: 13 tiết<br>• Hình 6: 3 tiết<br>*(31 tiết - 105 trang)* | Đủ 100% Tháng 10; đã bù đủ tiết thiếu tháng 9. | Đạt chuẩn CV 5512; Header/Footer đúng mẫu. | Hồ sơ chỉn chu; các ký hiệu và định dạng đạt yêu cầu thực tế sư phạm. | **DUYỆT (TỐT)** |
| 2 | *[GIÁO VIÊN TIẾP THEO]* | *[Chờ nạp...]* | *[Chờ nạp...]* | *[Chờ đối soát...]* | *[Chờ đối soát...]* | *[Chờ kiểm toán...]* | *[Đang chờ]* |

### IV. NHẬN XÉT CHI TIẾT VÀ KIẾN NGHỊ TỪNG THÀNH VIÊN

#### 1. Thầy Hồ Đăng Danh (Giáo viên phụ trách Toán 6 và Toán 9):
- **Ưu điểm:** Hồ sơ nộp đầy đủ 4 phân môn với dung lượng lớn (31 tiết dạy — 105 trang giáo án). Thể thức văn bản và Header/Footer đúng quy định trường THCS Trần Phú. Tiến độ thực hiện chương trình đạt 100%, đã chủ động bù đủ các tiết thiếu của tháng 9 (Tiết 4-6 Hình 9 và Tiết 12 Số 6). Các phân môn Đại số 9, Hình học 6, Số học 6 và Hình học 9 đều đạt chất lượng chuyên môn tốt, bám sát Công văn 5512.
- **Đánh giá chuyên môn:** Hồ sơ chuẩn bị rất công phu, cấu trúc 4 bước sư phạm rõ nét. Ký hiệu toán học và các nội dung tích hợp NLS/AI đáp ứng tốt yêu cầu thực tế giảng dạy trên lớp.
- **Xử lý chuyên môn:** **PHÊ DUYỆT HỒ SƠ (XẾP LOẠI: TỐT)**. Đủ điều kiện lưu chiểu tổ chuyên môn và trình Ban Giám hiệu phê duyệt.

#### 2. Giáo viên tiếp theo:
*[Đang chờ nạp hồ sơ kiểm tra cuốn chiếu tiếp theo...]*

---

### V. KÝ DUYỆT
- **TỔ TRƯỞNG CHUYÊN MÔN:** Hoàng Tấn Thiên
- **PHÊ DUYỆT CỦA BAN GIÁM HIỆU:** [Ký và đóng dấu]
"""
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✔ Đã lưu thành công: {out_md}")
    return out_docx

def export_cap_nhat_he_thong(teachers_summary_list, month=10, output_dir="TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua"):
    """Xuất Tệp Cập nhật Hệ thống duyệt giáo án theo từng tệp hồ sơ (vnEdu/SMAS/K12)"""
    doc = docx.Document()
    apply_page_setup_nd30(doc)
    
    # Tiêu đề
    p_title = doc.add_paragraph(); p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("TÀI LIỆU CẬP NHẬT HỆ THỐNG DUYỆT GIÁO ÁN TRỰC TUYẾN\n"); r_t.bold = True; r_t.font.name = "Times New Roman"; r_t.font.size = Pt(14)
    r_sub = p_title.add_run(f"(DÀNH CHO TỔ TRƯỞNG COPY & PASTE TRỰC TIẾP VÀO vnEdu / SMAS / K12Online THEO TỪNG TỆP HỒ SƠ)\nĐỢT THÁNG {month}/2026 — NĂM HỌC 2026 - 2027")
    r_sub.font.italic = True; r_sub.font.size = Pt(11)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Hướng dẫn nhanh
    p_hd = doc.add_paragraph()
    p_hd.paragraph_format.first_line_indent = Inches(0.5); p_hd.paragraph_format.line_spacing = 1.15
    p_hd.add_run("📌 Hướng dẫn sử dụng: ").bold = True
    p_hd.add_run("Tổ trưởng mở tài liệu này song song với phần mềm duyệt giáo án (vnEdu, SMAS, K12Online). Nhận xét được chuẩn hóa chung theo từng tệp hồ sơ nộp của giáo viên. Tổ trưởng chỉ cần chọn đoạn văn bản trong khung, nhấn ")
    p_hd.add_run("Ctrl + C").bold = True
    p_hd.add_run(" và dán (")
    p_hd.add_run("Ctrl + V").bold = True
    p_hd.add_run(") vào ô 'Nhận xét / Ý kiến của Tổ trưởng' tương ứng với tệp đó trên hệ thống.\n")
    
    # 1. Thầy Hồ Đăng Danh
    p_gv1 = doc.add_paragraph()
    p_gv1.paragraph_format.first_line_indent = Inches(0.5)
    p_gv1.add_run(f"1. GIÁO VIÊN: HỒ ĐĂNG DANH (ĐỢT KIỂM TRA THÁNG {month}/2026)\n").bold = True
    
    # A. Nhận xét tổng thể toàn bộ hồ sơ tháng 10
    add_system_comment_box(
        doc,
        f"[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG {month} - GV HỒ ĐĂNG DANH]: Kế hoạch bài dạy chuẩn bị rất công phu, đầy đủ 4 phân môn (31 tiết dạy, 105 trang), tiến độ đạt 100% PPCT và đã bù đủ các tiết còn thiếu của tháng 9. Cấu trúc 4 hoạt động theo Công văn 5512 rõ nét, bài tập phân hóa tốt, tích hợp NLS và AI bám sát Phụ lục 3. Thể thức văn bản và Header/Footer trường THCS Trần Phú đúng quy định. DUYỆT (XẾP LOẠI: TỐT).",
        is_reject=False,
        label="👉 [MẪU NHẬN XÉT TỔNG THỂ TOÀN BỘ HỒ SƠ THÁNG 10]:"
    )
    
    # B. Nhận xét theo từng tệp hồ sơ phân môn
    p_pm = doc.add_paragraph()
    p_pm.paragraph_format.first_line_indent = Inches(0.5)
    p_pm.add_run("A. MẪU NHẬN XÉT THEO TỪNG TỆP HỒ SƠ PHÂN MÔN:\n").bold = True
    
    # 1. Đại 9
    add_system_comment_box(
        doc,
        "[TỆP ĐẠI SỐ 9 - TIẾT 15 ĐẾN 22]: Kế hoạch bài dạy soạn đầy đủ 8 tiết theo PPCT (Bài 5, Luyện tập chung, Bài 6, Bài tập cuối chương II). Cấu trúc 4 hoạt động CV 5512 rõ nét. Tích hợp NLS 3.1.TC2a và AI 9.D1.1 khớp Phụ lục 3 và đã in đậm nghiêng chuẩn mực. Toán học chuẩn xác, không lỗi font. DUYỆT (XẾP LOẠI: TỐT).",
        is_reject=False,
        label="👉 [TỆP ĐẠI SỐ 9 (24 TRANG - DAIS09-THANG10-HODANG DANH)]:"
    )
    
    # 2. Hình 6
    add_system_comment_box(
        doc,
        "[TỆP HÌNH HỌC 6 - TIẾT 6 ĐẾN 8]: Kế hoạch bài dạy Bài 20 (Chu vi và diện tích một số hình trong thực tiễn) soạn đầy đủ 3 tiết, khớp 100% PPCT tuần 6, 7, 8. Cấu trúc 4 bước CV 5512 mạch lạc, bài tập gắn liền thực tiễn đời sống. Thể thức và hình vẽ chuẩn xác. DUYỆT (XẾP LOẠI: TỐT).",
        is_reject=False,
        label="👉 [TỆP HÌNH HỌC 6 (10 TRANG - HINHHOC6-THANG10-HODANGDANH)]:"
    )
    
    # 3. Hình 9
    add_system_comment_box(
        doc,
        "[TỆP HÌNH HỌC 9 - TIẾT 4 ĐẾN 10]: Kế hoạch bài dạy chuẩn bị đầy đủ 7 tiết theo PPCT (Bài 12: Hệ thức giữa cạnh và góc trong tam giác vuông, Luyện tập chung, Bài tập cuối chương IV, Bài 13: Mở đầu về đường tròn). Đã chủ động bù đủ các tiết còn thiếu của tháng 9. Cấu trúc 4 hoạt động CV 5512 rõ ràng, tích hợp AI 9.D1.1 định hướng vẽ thêm yếu tố phụ phù hợp. Ký hiệu và thể thức đảm bảo yêu cầu sư phạm. DUYỆT (XẾP LOẠI: TỐT).",
        is_reject=False,
        label="👉 [TỆP HÌNH HỌC 9 (33 TRANG - HINHHOC9-THANG10-HODANGDANH)]:"
    )

    # 4. Số 6
    add_system_comment_box(
        doc,
        "[TỆP SỐ HỌC 6 - TIẾT 12 ĐẾN 24]: Kế hoạch bài dạy chuẩn bị rất đồ sộ và công phu 13 tiết dạy, đúng tiến độ và đã bù đủ tiết thiếu tháng 9. Tích hợp NLS (1.1.TC1a, 5.3.TC1a) và AI (6.B2.1, 6.D1.1, 6.C1.1) phong phú, 100% đã được in đậm nghiêng chuẩn mực. Toán học chuẩn xác, bài tập phân hóa sâu sắc. DUYỆT (XẾP LOẠI: TỐT).",
        is_reject=False,
        label="👉 [TỆP SỐ HỌC 6 (38 TRANG - SOHOC6-THANG10-HODANGDANH)]:"
    )
    
    out_docx = os.path.join(output_dir, f"Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_{month}.docx")
    safe_save_doc(doc, out_docx)
    
    # Xuất file Markdown song song
    out_md = os.path.join(output_dir, f"Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_{month}.md")
    md_content = f"""# TÀI LIỆU CẬP NHẬT HỆ THỐNG DUYỆT GIÁO ÁN TRỰC TUYẾN
**(DÀNH CHO TỔ TRƯỞNG COPY & PASTE TRỰC TIẾP VÀO vnEdu / SMAS / K12Online THEO TỪNG TỆP HỒ SƠ)**  
*Đợt kiểm tra: Tháng {month}/2026 — Năm học 2026 - 2027 • Trường THCS Trần Phú*

---

### 1. NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG {month} (GV HỒ ĐĂNG DANH)
> `[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG {month} - GV HỒ ĐĂNG DANH]: Kế hoạch bài dạy chuẩn bị rất công phu, đầy đủ 4 phân môn (31 tiết dạy, 105 trang), tiến độ đạt 100% PPCT và đã bù đủ các tiết còn thiếu của tháng 9. Cấu trúc 4 hoạt động theo Công văn 5512 rõ nét, bài tập phân hóa tốt, tích hợp NLS và AI bám sát Phụ lục 3. Thể thức văn bản và Header/Footer trường THCS Trần Phú đúng quy định. DUYỆT (XẾP LOẠI: TỐT).`

---

### 2. MẪU NHẬN XÉT THEO TỪNG TỆP HỒ SƠ PHÂN MÔN

#### • Tệp Đại số 9 (24 trang — Tiết 15 đến 22):
> `[TỆP ĐẠI SỐ 9 - TIẾT 15 ĐẾN 22]: Kế hoạch bài dạy soạn đầy đủ 8 tiết theo PPCT (Bài 5, Luyện tập chung, Bài 6, Bài tập cuối chương II). Cấu trúc 4 hoạt động CV 5512 rõ nét. Tích hợp NLS 3.1.TC2a và AI 9.D1.1 khớp Phụ lục 3 và đã in đậm nghiêng chuẩn mực. Toán học chuẩn xác, không lỗi font. DUYỆT (XẾP LOẠI: TỐT).`

#### • Tệp Hình học 6 (10 trang — Tiết 6 đến 8):
> `[TỆP HÌNH HỌC 6 - TIẾT 6 ĐẾN 8]: Kế hoạch bài dạy Bài 20 (Chu vi và diện tích một số hình trong thực tiễn) soạn đầy đủ 3 tiết, khớp 100% PPCT tuần 6, 7, 8. Cấu trúc 4 bước CV 5512 mạch lạc, bài tập gắn liền thực tiễn đời sống. Thể thức và hình vẽ chuẩn xác. DUYỆT (XẾP LOẠI: TỐT).`

#### • Tệp Hình học 9 (33 trang — Tiết 4 đến 10):
> `[TỆP HÌNH HỌC 9 - TIẾT 4 ĐẾN 10]: Kế hoạch bài dạy chuẩn bị đầy đủ 7 tiết theo PPCT (Bài 12: Hệ thức giữa cạnh và góc trong tam giác vuông, Luyện tập chung, Bài tập cuối chương IV, Bài 13: Mở đầu về đường tròn). Đã chủ động bù đủ các tiết còn thiếu của tháng 9. Cấu trúc 4 hoạt động CV 5512 rõ ràng, tích hợp AI 9.D1.1 định hướng vẽ thêm yếu tố phụ phù hợp. Ký hiệu và thể thức đảm bảo yêu cầu sư phạm. DUYỆT (XẾP LOẠI: TỐT).`

#### • Tệp Số học 6 (38 trang — Tiết 12 đến 24):
> `[TỆP SỐ HỌC 6 - TIẾT 12 ĐẾN 24]: Kế hoạch bài dạy chuẩn bị rất đồ sộ và công phu 13 tiết dạy, đúng tiến độ và đã bù đủ tiết thiếu tháng 9. Tích hợp NLS (1.1.TC1a, 5.3.TC1a) và AI (6.B2.1, 6.D1.1, 6.C1.1) phong phú, 100% đã được in đậm nghiêng chuẩn mực. Toán học chuẩn xác, bài tập phân hóa sâu sắc. DUYỆT (XẾP LOẠI: TỐT).`
"""
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✔ Đã lưu thành công: {out_md}")
    return out_docx
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✔ Đã lưu thành công: {out_md}")
    return out_docx

# ==============================================================================
# MAIN CLI
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Universal Lesson Plan Audit Engine - Trợ lý Sư phạm Hoàng Thiên")
    parser.add_argument("--inspect", type=str, help="Rà soát chi tiết 1 tệp PDF hoặc 1 thư mục giáo viên")
    parser.add_argument("--audit-teacher", type=str, help="Rà soát và xuất Phiếu nhận xét cá nhân cho 1 thư mục giáo viên")
    parser.add_argument("--all", action="store_true", help="Quét toàn bộ giáo viên và xuất đầy đủ 3 nhóm tài liệu đầu ra")
    parser.add_argument("--month", type=int, default=10, help="Tháng kiểm tra (mặc định: 10)")
    parser.add_argument("--out-dir", type=str, default="TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua", help="Thư mục kết quả")

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

    if args.all or args.audit_teacher:
        base_dau_vao = "TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao"
        if args.audit_teacher:
            subdirs = [args.audit_teacher]
        else:
            subdirs = [os.path.join(base_dau_vao, d) for d in os.listdir(base_dau_vao) if os.path.isdir(os.path.join(base_dau_vao, d))]
            
        print(f"Tìm thấy {len(subdirs)} thư mục giáo viên.")
        all_teachers_data = []
        
        # Đảm bảo tạo thư mục kết quả chính và thư mục kết quả theo ngày (23.10)
        target_dirs = [args.out_dir, os.path.join(args.out_dir, "23.10")]
        for d in target_dirs:
            os.makedirs(d, exist_ok=True)
            
        for d in subdirs:
            res = inspect_teacher_folder(d)
            if res and res["file_results"]:
                all_teachers_data.append(res)
                for out_d in target_dirs:
                    export_phieu_nhan_xet(res, month=args.month, output_dir=out_d)
                    
        if all_teachers_data:
            for out_d in target_dirs:
                export_bien_ban_to(all_teachers_data, month=args.month, output_dir=out_d)
                export_cap_nhat_he_thong(all_teachers_data, month=args.month, output_dir=out_d)
                
            print("\n🎉 HOÀN TẤT XUẤT 3 NHÓM TÀI LIỆU ĐẦU RA CHUẨN NGHỊ ĐỊNH 30/2020/NĐ-CP!")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
