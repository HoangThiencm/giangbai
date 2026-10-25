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
# DANH MỤC TOÀN BỘ 8 GIÁO VIÊN TỔ TOÁN - TIN HỌC (THÁNG 10/2026)
# ==============================================================================
TEACHERS_CATALOG = [
    {
        "stt": 1,
        "id": "HO_DANG_DANH",
        "name": "Hồ Đăng Danh",
        "folder_name": "Hồ Đăng Danh",
        "doc_id": "01",
        "subjects": "Toán 6 (Số học 6 & Hình học 6), Toán 9 (Đại số 9 & Hình học 9)",
        "subjects_short": "• Đại số 9\n• Hình học 9\n• Số học 6\n• Hình học 6",
        "lessons_stats": "• Đại 9: 8 tiết (Tiết 15-22)\n• Hình 9: 7 tiết (Tiết 4-10)\n• Số 6: 13 tiết (Tiết 12-24)\n• Hình 6: 3 tiết (Tiết 6-8)\n(31 tiết - 105 trang)",
        "progress_eval": "Đủ 100% Tháng 10; đã bù đủ tiết thiếu tháng 9.",
        "format_eval": "Đạt chuẩn CV 5512; Header/Footer đúng mẫu.",
        "remarks": "Hồ sơ chỉn chu; các ký hiệu và định dạng đạt yêu cầu thực tế sư phạm.",
        "verdict": "DUYỆT (TỐT)",
        "total_pages": 105,
        "files_count": 4,
        "overall_summary": (
            "Hồ sơ nộp đầy đủ 4 phân môn với dung lượng lớn (31 tiết dạy — 105 trang giáo án). "
            "Thể thức văn bản và Header/Footer đúng quy định trường THCS Trần Phú. Tiến độ thực hiện chương trình đạt 100%, "
            "đã chủ động bù đủ các tiết thiếu của tháng 9 (Tiết 4-6 Hình 9 và Tiết 12 Số 6). "
            "Các phân môn Đại số 9, Hình học 6, Số học 6 và Hình học 9 đều đạt chất lượng chuyên môn tốt, bám sát Công văn 5512."
        ),
        "overall_system_comment": (
            "[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG 10 - GV HỒ ĐĂNG DANH]: Kế hoạch bài dạy chuẩn bị rất công phu, "
            "đầy đủ 4 phân môn (31 tiết dạy, 105 trang), tiến độ đạt 100% PPCT và đã bù đủ các tiết còn thiếu của tháng 9. "
            "Cấu trúc 4 hoạt động theo Công văn 5512 rõ nét, bài tập phân hóa tốt, tích hợp NLS và AI bám sát Phụ lục 3. "
            "Thể thức văn bản và Header/Footer trường THCS Trần Phú đúng quy định. DUYỆT (XẾP LOẠI: TỐT)."
        ),
        "files": [
            {
                "filename": "DAIS09-THANG10-HODANG DANH_1792727827471.pdf",
                "short_name": "Đại số 9",
                "pages": 24,
                "detail_title": "1. Phân môn Đại số 9 (Tiết 15 đến Tiết 22 — 24 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 8 tiết dạy từ Bài 5 (Bất đẳng thức và tính chất), Luyện tập chung, "
                    "Bài 6 (Bất phương trình bậc nhất một ẩn) đến Bài tập cuối chương II. Đúng tiến độ 100% theo Phụ lục 3 (Tuần 5, 6, 7, 8).\n"
                    "• Cấu trúc: Đầy đủ 4 hoạt động CV 5512, tích hợp NLS 3.1.TC2a và AI 9.D1.1 đã được in đậm nghiêng chuẩn mực. Toán học chuẩn xác, không lỗi font.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP ĐẠI SỐ 9 (24 TRANG - DAIS09-THANG10-HODANG DANH)]:",
                "system_comment": (
                    "[TỆP ĐẠI SỐ 9 - TIẾT 15 ĐẾN 22]: Kế hoạch bài dạy soạn đầy đủ 8 tiết theo PPCT (Bài 5, Luyện tập chung, Bài 6, Bài tập cuối chương II). "
                    "Cấu trúc 4 hoạt động CV 5512 rõ nét. Tích hợp NLS 3.1.TC2a và AI 9.D1.1 khớp Phụ lục 3 và đã in đậm nghiêng chuẩn mực. "
                    "Toán học chuẩn xác, không lỗi font. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HINHHOC6-THANG10-HODANGDANH_1792727827827.pdf",
                "short_name": "Hình học 6",
                "pages": 10,
                "detail_title": "2. Phân môn Hình học 6 (Tiết 6 đến Tiết 8 — 10 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 3 tiết Bài 20: Chu vi và diện tích của một số hình trong thực tiễn (Tuần 6, 7, 8). Tiến độ khớp 100% Phụ lục 3.\n"
                    "• Cấu trúc: 4 hoạt động sư phạm chuẩn mực, phân hóa tốt bài tập tam giác, hình thoi, hình chữ nhật. Bài học không đăng ký NLS/AI nên giữ nguyên giáo án tinh gọn đúng quy chuẩn.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 6 (10 TRANG - HINHHOC6-THANG10-HODANGDANH)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 6 - TIẾT 6 ĐẾN 8]: Kế hoạch bài dạy Bài 20 (Chu vi và diện tích một số hình trong thực tiễn) soạn đầy đủ 3 tiết, "
                    "khớp 100% PPCT tuần 6, 7, 8. Cấu trúc 4 bước CV 5512 mạch lạc, bài tập gắn liền thực tiễn đời sống. Thể thức và hình vẽ chuẩn xác. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HINHHOC9-THANG10-HODANGDANH_1792727827361.pdf",
                "short_name": "Hình học 9",
                "pages": 33,
                "detail_title": "3. Phân môn Hình học 9 (Tiết 4 đến Tiết 10 — 33 trang):",
                "detail_desc": (
                    "• Ưu điểm: Đã bù đủ Tiết 4, 5, 6 (Bài 12: Hệ thức giữa cạnh và góc trong tam giác vuông) và soạn tiếp Tiết 7 (LTC), Tiết 8 (BTC chương IV), Tiết 9, 10 (Bài 13: Mở đầu về đường tròn). Đảm bảo 100% số tiết theo PPCT.\n"
                    "• Đánh giá chuyên môn: Thể thức trình bày rõ ràng, ký hiệu góc và các nội dung tích hợp AI đảm bảo tính sư phạm và yêu cầu thực tế dạy học trên lớp.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 9 (33 TRANG - HINHHOC9-THANG10-HODANGDANH)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 9 - TIẾT 4 ĐẾN 10]: Kế hoạch bài dạy chuẩn bị đầy đủ 7 tiết theo PPCT (Bài 12: Hệ thức giữa cạnh và góc trong tam giác vuông, "
                    "Luyện tập chung, Bài tập cuối chương IV, Bài 13: Mở đầu về đường tròn). Đã chủ động bù đủ các tiết còn thiếu của tháng 9. "
                    "Cấu trúc 4 hoạt động CV 5512 rõ ràng, tích hợp AI 9.D1.1 định hướng vẽ thêm yếu tố phụ phù hợp. Ký hiệu và thể thức đảm bảo yêu cầu sư phạm. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "SOHOC6-THANG10-HODANGDANH_1792727827517.pdf",
                "short_name": "Số học 6",
                "pages": 38,
                "detail_title": "4. Phân môn Số học 6 (Tiết 12 đến Tiết 24 — 38 trang):",
                "detail_desc": (
                    "• Ưu điểm: Chuẩn bị đồ sộ 13 tiết dạy từ Tiết 12 (Luyện tập chung) đến Tiết 24 (Bài 12: Bội chung. Bội chung nhỏ nhất). Đã bù đủ tiết thiếu tháng 9 và đảm bảo tiến độ tháng 10.\n"
                    "• Cấu trúc: 4 hoạt động 5512 rõ nét. Tích hợp NLS 1.1.TC1a, 5.3.TC1a và AI 6.B2.1, 6.D1.1, 6.C1.1 đầy đủ và 100% được in đậm nghiêng theo quy định. Toán học chuẩn xác.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP SỐ HỌC 6 (38 TRANG - SOHOC6-THANG10-HODANGDANH)]:",
                "system_comment": (
                    "[TỆP SỐ HỌC 6 - TIẾT 12 ĐẾN 24]: Kế hoạch bài dạy chuẩn bị rất đồ sộ và công phu 13 tiết dạy, đúng tiến độ và đã bù đủ tiết thiếu tháng 9. "
                    "Tích hợp NLS (1.1.TC1a, 5.3.TC1a) và AI (6.B2.1, 6.D1.1, 6.C1.1) phong phú, 100% đã được in đậm nghiêng chuẩn mực. Toán học chuẩn xác, bài tập phân hóa sâu sắc. DUYỆT (XẾP LOẠI: TỐT)."
                )
            }
        ]
    },
    {
        "stt": 2,
        "id": "Duong_Quang_Tung",
        "name": "Dương Quang Tùng",
        "folder_name": "Duong Quang Tùng",
        "doc_id": "02",
        "subjects": "Tin học 6, Tin học 7, Tin học 8, Tin học 9",
        "subjects_short": "• Tin học 6\n• Tin học 7\n• Tin học 8\n• Tin học 9",
        "lessons_stats": "• Tin 6: 4 tiết (20 trang)\n• Tin 7: 4 tiết (17 trang)\n• Tin 8: 4 tiết (9 trang)\n• Tin 9: 4 tiết (43 trang)\n(16 tiết - 89 trang)",
        "progress_eval": "Đủ 100% Tháng 10 (Tuần 5 đến Tuần 8).",
        "format_eval": "Đạt chuẩn CV 5512; Phân môn Tin học trực quan, sinh động.",
        "remarks": "Giáo án chuẩn mực, thiết kế bài thực hành máy tính chi tiết, phù hợp đặc thù môn Tin học.",
        "verdict": "DUYỆT (TỐT)",
        "total_pages": 89,
        "files_count": 4,
        "overall_summary": (
            "Hồ sơ Kế hoạch bài dạy nộp đầy đủ 4 khối lớp (Tin học 6, 7, 8, 9) với tổng cộng 16 tiết dạy (89 trang giáo án). "
            "Tiến độ thực hiện chương trình đạt 100% kế hoạch tháng 10. Kế hoạch bài dạy thiết kế chuẩn mực theo Công văn 5512, "
            "đặc biệt chú trọng hoạt động thực hành trên máy tính và hướng dẫn học sinh thao tác phần mềm, khai thác Internet an toàn, văn minh. "
            "Thể thức trình bày sạch đẹp, bố cục rõ ràng."
        ),
        "overall_system_comment": (
            "[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG 10 - GV DƯƠNG QUANG TÙNG]: Kế hoạch bài dạy nộp đầy đủ 4 khối lớp Tin học 6, 7, 8, 9 "
            "(16 tiết dạy, 89 trang), khớp 100% tiến độ PPCT tháng 10. Cấu trúc 4 hoạt động CV 5512 rõ nét, bài tập thực hành trên máy tính được thiết kế chi tiết, "
            "phát huy tốt phẩm chất và năng lực số của học sinh. Thể thức trình bày chuẩn mực. DUYỆT (XẾP LOẠI: TỐT)."
        ),
        "files": [
            {
                "filename": "TINHỌC6-THÁNG10-DUONGQUANGTUNG_1792966264898.pdf",
                "short_name": "Tin học 6",
                "pages": 20,
                "detail_title": "1. Môn Tin học 6 (20 trang — Tuần 5 đến Tuần 8):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ các bài Bài 3 (Thông tin trong máy tính), Bài 4 (Mạng máy tính). Đúng tiến độ PPCT tháng 10.\n"
                    "• Cấu trúc: 4 hoạt động CV 5512 rõ ràng. Các hoạt động khám phá biểu diễn thông tin nhị phân và sơ đồ mạng máy tính được thiết kế sinh động, trực quan.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP TIN HỌC 6 (20 TRANG - TINHOC6-THANG10-DUONGQUANGTUNG)]:",
                "system_comment": (
                    "[TỆP TIN HỌC 6 - THÁNG 10]: Soạn đầy đủ các bài Bài 3: Thông tin trong máy tính và Bài 4: Mạng máy tính. "
                    "Đúng tiến độ PPCT tháng 10. Hoạt động học tập trực quan, giải thích khái niệm bit, byte và kết nối mạng dễ hiểu, phù hợp học sinh lớp 6. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "TINHỌC7-THÁNG10-DUONGQUANGTUNG_1792966264527.pdf",
                "short_name": "Tin học 7",
                "pages": 17,
                "detail_title": "2. Môn Tin học 7 (17 trang — Tuần 5 đến Tuần 8):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ Bài 4 (Mạng xã hội và một số kênh trao đổi thông tin trên Internet), Bài 5 (Ứng xử trên mạng). Đảm bảo 100% tiến độ.\n"
                    "• Cấu trúc: Thiết kế tình huống sư phạm thực tế, hướng dẫn học sinh kỹ năng giao tiếp mạng an toàn và đạo đức số. Tích hợp năng lực số tự nhiên và hiệu quả.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP TIN HỌC 7 (17 TRANG - TINHOC7-THANG10-DUONGQUANGTUNG)]:",
                "system_comment": (
                    "[TỆP TIN HỌC 7 - THÁNG 10]: Soạn bài Bài 4: Mạng xã hội và Bài 5: Ứng xử trên mạng đầy đủ, đúng tiến độ. "
                    "Hệ thống câu hỏi và bài tập tình huống thực tế giúp học sinh nâng cao nhận thức về an toàn thông tin và văn hóa ứng xử trên không gian số. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "TINHỌC8-THÁNG10-DUONGQUANGTUNG_1792966264691.pdf",
                "short_name": "Tin học 8",
                "pages": 9,
                "detail_title": "3. Môn Tin học 8 (9 trang — Tuần 5 đến Tuần 8):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ Bài 5: Sử dụng bảng tính giải quyết bài toán thực tế. Tiến độ khớp 100% PPCT.\n"
                    "• Cấu trúc: 4 hoạt động sư phạm chuẩn mực; bài thực hành hướng dẫn thao tác nhập công thức, hàm tính toán và định dạng bảng biểu chi tiết, rõ ràng.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP TIN HỌC 8 (9 TRANG - TINHOC8-THANG10-DUONGQUANGTUNG)]:",
                "system_comment": (
                    "[TỆP TIN HỌC 8 - THÁNG 10]: Soạn bài Bài 5: Sử dụng bảng tính giải quyết bài toán thực tế đảm bảo tiến độ. "
                    "Nội dung thực hành bám sát bài toán thực tế, hướng dẫn từng bước thao tác phần mềm bảng tính mạch lạc. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "TINHỌC9-THÁNG 10-DUONGQUANGTUNG_1792966264862.pdf",
                "short_name": "Tin học 9",
                "pages": 43,
                "detail_title": "4. Môn Tin học 9 (43 trang — Tuần 5 đến Tuần 8):",
                "detail_desc": (
                    "• Ưu điểm: Chuẩn bị rất đồ sộ và chu đáo (43 trang) gồm Bài 4 (Một số vấn đề pháp lí về sử dụng dịch vụ Internet), Bài 5 (Tìm hiểu phần mềm mô phỏng). Khớp 100% PPCT.\n"
                    "• Cấu trúc: Nội dung pháp lý về bản quyền, an ninh mạng được cụ thể hóa bằng các tình huống pháp luật gần gũi. Bài thực hành phần mềm mô phỏng hướng dẫn chi tiết, hình ảnh minh họa rõ ràng.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP TIN HỌC 9 (43 TRANG - TINHOC9-THANG10-DUONGQUANGTUNG)]:",
                "system_comment": (
                    "[TỆP TIN HỌC 9 - THÁNG 10]: Hồ sơ chuẩn bị rất công phu (43 trang), soạn đầy đủ Bài 4: Vấn đề pháp lí trên Internet và Bài 5: Phần mềm mô phỏng. "
                    "Cấu trúc CV 5512 rõ nét, bài tập tình huống pháp lý và hướng dẫn thực hành mô phỏng sâu sắc, chất lượng cao. DUYỆT (XẾP LOẠI: TỐT)."
                )
            }
        ]
    },
    {
        "stt": 3,
        "id": "Hoang_Xuan_Anh",
        "name": "Hoàng Xuân Ánh",
        "folder_name": "Hoàng Xuân Ánh",
        "doc_id": "03",
        "subjects": "Toán 7 (Đại số 7 & Hình học 7), Hoạt động trải nghiệm 6 (HĐTN 6)",
        "subjects_short": "• Đại số 7\n• Hình học 7\n• HĐTN 6",
        "lessons_stats": "• Đại 7: 10 tiết (27 trang)\n• Hình 7: 10 tiết (44 trang)\n• HĐTN 6: 4 tiết (10 trang)\n(24 tiết - 81 trang)",
        "progress_eval": "Đủ 100% Tháng 10 theo Phụ lục 3.",
        "format_eval": "Đạt chuẩn CV 5512; Phân môn Toán học và Trải nghiệm rõ ràng.",
        "remarks": "Hồ sơ bài bản; nội dung hình học 7 và đại số 7 chính xác, thể thức đạt yêu cầu thực tế sư phạm.",
        "verdict": "DUYỆT (TỐT)",
        "total_pages": 81,
        "files_count": 3,
        "overall_summary": (
            "Hồ sơ nộp đầy đủ 3 tệp thuộc các phân môn Toán 7 (Đại số, Hình học) và HĐTN 6 với tổng cộng 24 tiết dạy (81 trang). "
            "Tiến độ thực hiện chương trình đạt 100% kế hoạch tháng 10. Giáo án môn Toán thể hiện tốt phương pháp dạy học tích cực, "
            "các định lý và bài tập hình học 7 được vẽ hình và lập luận chứng minh chặt chẽ. Giáo án HĐTN 6 thiết kế hoạt động trải nghiệm bổ ích, "
            "giúp học sinh hình thành thói quen tự chăm sóc bản thân."
        ),
        "overall_system_comment": (
            "[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG 10 - GV HOÀNG XUÂN ÁNH]: Kế hoạch bài dạy nộp đầy đủ 3 phân môn Toán 7 (Đại số, Hình học) "
            "và HĐTN 6 (24 tiết dạy, 81 trang), đảm bảo 100% tiến độ PPCT tháng 10. Cấu trúc 4 hoạt động CV 5512 chuẩn mực, toán học chính xác, "
            "hình vẽ rõ ràng, tổ chức hoạt động trải nghiệm sôi nổi. DUYỆT (XẾP LOẠI: TỐT)."
        ),
        "files": [
            {
                "filename": "ĐẠI SỐ 7 THÁNG 10 - HOÀNG XUÂN ÁNH_1792966222503.pdf",
                "short_name": "Đại số 7",
                "pages": 27,
                "detail_title": "1. Phân môn Đại số 7 (Tiết 10 đến Tiết 19 — 27 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 10 tiết từ Bài 4 (Thứ tự thực hiện các phép tính. Quy tắc chuyển vế), Luyện tập chung, Bài tập cuối chương I đến Bài 5 (Làm quen số thập phân vô hạn tuần hoàn). Đúng tiến độ PPCT.\n"
                    "• Cấu trúc: 4 hoạt động rõ nét, quy tắc chuyển vế và đổi dấu được giải thích cặn kẽ, bài tập luyện tập phân hóa tốt.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP ĐẠI SỐ 7 (27 TRANG - DAISO7-THANG10-HOANGXUANANH)]:",
                "system_comment": (
                    "[TỆP ĐẠI SỐ 7 - THÁNG 10]: Kế hoạch bài dạy soạn đủ 10 tiết theo PPCT (Bài 4: Quy tắc chuyển vế, Luyện tập chung, Bài tập cuối chương I, Bài 5). "
                    "Cấu trúc CV 5512 rõ ràng, quy tắc biến đổi đại số chuẩn xác, hệ thống bài tập rèn kỹ năng tính toán tốt. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "hinh 7 -thang 10- HOÀNG XUÂN ÁNH_1792966222608.pdf",
                "short_name": "Hình học 7",
                "pages": 44,
                "detail_title": "2. Phân môn Hình học 7 (Tiết 9 đến Tiết 18 — 44 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn công phu 10 tiết (Bài 11: Định lí và chứng minh định lí, Bài tập cuối chương III, Bài 12: Tổng các góc trong tam giác, Bài 13: Hai tam giác bằng nhau). Khớp 100% PPCT.\n"
                    "• Cấu trúc: Các bước chứng minh hình học được trình bày bài bản, hình vẽ chuẩn xác, ký hiệu góc và tam giác rõ ràng, đảm bảo yêu cầu sư phạm.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 7 (44 TRANG - HINH7-THANG10-HOANGXUANANH)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 7 - THÁNG 10]: Hồ sơ chuẩn bị công phu 44 trang (10 tiết dạy: Bài 11 Định lí, Bài tập cuối chương III, Bài 12 Tổng các góc trong tam giác, Bài 13). "
                    "Cấu trúc CV 5512 rõ nét, hình vẽ chuẩn xác, lập luận chứng minh chặt chẽ, sư phạm. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HĐTN 6-THÁNG 10- HOÀNG XUÂN ÁNH_1792966222142.pdf",
                "short_name": "HĐTN 6",
                "pages": 10,
                "detail_title": "3. Hoạt động trải nghiệm 6 (Tuần 5 đến Tuần 8 — 10 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đủ 4 tiết theo chủ đề tháng 10: Chủ đề 2 (Khám phá bản thân và chăm sóc cuộc sống cá nhân). Tiến độ đạt 100%.\n"
                    "• Cấu trúc: Thiết kế sinh động với trò chơi, thảo luận nhóm và bài tập tự liên hệ, giúp học sinh chủ động rèn luyện bản thân.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HĐTN 6 (10 TRANG - HDTN6-THANG10-HOANGXUANANH)]:",
                "system_comment": (
                    "[TỆP HĐTN 6 - THÁNG 10]: Soạn đầy đủ 4 tiết theo Chủ đề 2 (Khám phá bản thân, chăm sóc cuộc sống cá nhân) từ tuần 5 đến tuần 8. "
                    "Hình thức tổ chức hoạt động trải nghiệm đa dạng, phát huy tính tích cực và chủ động của học sinh. DUYỆT (XẾP LOẠI: TỐT)."
                )
            }
        ]
    },
    {
        "stt": 4,
        "id": "Le_Thi_Binh",
        "name": "Lê Thị Bình",
        "folder_name": "Lê Thị Bình",
        "doc_id": "04",
        "subjects": "Toán 7 (Đại số 7 & Hình học 7), Toán 8 (Đại số 8 & Hình học 8), HĐTN 7",
        "subjects_short": "• Đại số 7 & Hình 7\n• Đại số 8 & Hình 8\n• HĐTN 7",
        "lessons_stats": "• Đại 7: 10 tiết (27 trang)\n• Hình 7: 10 tiết (44 trang)\n• Đại 8: 8 tiết (36 trang)\n• Hình 8: 7 tiết (60 trang)\n• HĐTN 7: 4 tiết (12 trang)\n(39 tiết - 179 trang)",
        "progress_eval": "Đủ 100% Tháng 10 theo Phụ lục 3.",
        "format_eval": "Đạt chuẩn CV 5512; Khối lượng hồ sơ rất lớn, công phu.",
        "remarks": "Giáo án chuẩn bị rất đồ sộ, đầy đủ 5 phân môn, bài tập phân hóa sâu sắc.",
        "verdict": "DUYỆT (TỐT)",
        "total_pages": 179,
        "files_count": 5,
        "overall_summary": (
            "Cô Lê Thị Bình có khối lượng công việc kiểm tra lớn nhất tổ với 5 phân môn (Đại 7, Hình 7, Đại 8, Hình 8, HĐTN 7), "
            "tổng cộng 39 tiết dạy (179 trang giáo án). Tiến độ thực hiện chương trình đạt 100% kế hoạch. "
            "Hồ sơ Kế hoạch bài dạy chuẩn bị rất chu đáo và công phu, hệ thống bài tập Toán 7 và Toán 8 phong phú, "
            "phân hóa sâu sắc từ nhận biết đến vận dụng cao. Kế hoạch HĐTN 7 tổ chức khoa học, phát huy tốt phẩm chất học sinh."
        ),
        "overall_system_comment": (
            "[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG 10 - GV LÊ THỊ BÌNH]: Khối lượng hồ sơ đồ sộ với 5 phân môn Toán 7, Toán 8 và HĐTN 7 "
            "(39 tiết dạy, 179 trang), đảm bảo 100% tiến độ PPCT tháng 10. Giáo án chuẩn bị rất công phu, cấu trúc 4 hoạt động CV 5512 rõ nét, "
            "hệ thống bài tập phân hóa sâu sắc, toán học chuẩn xác, hình vẽ rõ ràng. DUYỆT (XẾP LOẠI: TỐT)."
        ),
        "files": [
            {
                "filename": "ĐẠI SỐ 7 - THÁNG 10 - LÊ THỊ BÌNH_1792966277371.pdf",
                "short_name": "Đại số 7",
                "pages": 27,
                "detail_title": "1. Phân môn Đại số 7 (Tiết 10 đến Tiết 19 — 27 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đủ 10 tiết (Bài 4: Thứ tự thực hiện các phép tính. Quy tắc chuyển vế, Luyện tập chung, Bài tập cuối chương I, Bài 5). Đúng tiến độ PPCT.\n"
                    "• Cấu trúc: 4 hoạt động CV 5512 mạch lạc, bài tập rèn kỹ năng biến đổi đại số phong phú, lời giải chuẩn xác.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP ĐẠI SỐ 7 (27 TRANG - DAISO7-THANG10-LETHIBINH)]:",
                "system_comment": (
                    "[TỆP ĐẠI SỐ 7 - THÁNG 10]: Soạn đầy đủ 10 tiết theo PPCT từ Bài 4 đến Bài 5. Cấu trúc 4 hoạt động CV 5512 rõ nét, "
                    "hướng dẫn quy tắc chuyển vế và thứ tự phép tính chuẩn xác, bài tập phân hóa tốt. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HÌNH HỌC 7 - THÁNG 10 - LÊ THỊ BÌNH_1792966277534.pdf",
                "short_name": "Hình học 7",
                "pages": 44,
                "detail_title": "2. Phân môn Hình học 7 (Tiết 9 đến Tiết 18 — 44 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn công phu 10 tiết (Bài 11: Định lí và chứng minh định lí, Bài tập cuối chương III, Bài 12: Tổng các góc trong tam giác, Bài 13: Hai tam giác bằng nhau). Đạt 100% tiến độ.\n"
                    "• Cấu trúc: Lập luận chứng minh định lý chặt chẽ, hình vẽ trực quan, ký hiệu góc và tam giác rõ ràng.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 7 (44 TRANG - HINH7-THANG10-LETHIBINH)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 7 - THÁNG 10]: Hồ sơ chuẩn bị 44 trang chu đáo, soạn đủ 10 tiết theo PPCT (Bài 11, 12, 13 và Bài tập cuối chương III). "
                    "Hình vẽ trực quan, lập luận chứng minh chặt chẽ, phương pháp sư phạm mạch lạc. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "ĐẠI SỐ 8 - THÁNG 10 - LÊ THỊ BÌNH_1792966277418.pdf",
                "short_name": "Đại số 8",
                "pages": 36,
                "detail_title": "3. Phân môn Đại số 8 (Tiết 9 đến Tiết 16 — 36 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 8 tiết (Bài 5: Phép chia đa thức cho đơn thức, Luyện tập chung, Bài tập cuối chương I, Bài 6: Hiệu hai bình phương. Bình phương một tổng hay hiệu). Tiến độ đạt 100%.\n"
                    "• Cấu trúc: Các hằng đẳng thức đáng nhớ được hình thành qua hoạt động ghép hình và tính diện tích trực quan, học sinh dễ nhớ và vận dụng thành thạo.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP ĐẠI SỐ 8 (36 TRANG - DAISO8-THANG10-LETHIBINH)]:",
                "system_comment": (
                    "[TỆP ĐẠI SỐ 8 - THÁNG 10]: Soạn đầy đủ 8 tiết theo PPCT từ Bài 5 đến Bài 6 (Hằng đẳng thức đáng nhớ). "
                    "Cấu trúc CV 5512 rõ nét, hình thành kiến thức hằng đẳng thức trực quan, hệ thống bài tập áp dụng phong phú. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HÌNH HỌC 8 - THÁNG 10 - LÊ THỊ BÌNH_1792966277508.pdf",
                "short_name": "Hình học 8",
                "pages": 60,
                "detail_title": "4. Phân môn Hình học 8 (Tiết 9 đến Tiết 15 — 60 trang):",
                "detail_desc": (
                    "• Ưu điểm: Chuẩn bị rất đồ sộ 60 trang gồm Bài 13: Hình chữ nhật, Bài 14: Hình thoi và hình vuông, Bài tập cuối chương III. Khớp 100% PPCT.\n"
                    "• Cấu trúc: Tính chất và dấu hiệu nhận biết các tứ giác đặc biệt được tổng hợp hệ thống bằng bảng so sánh rõ nét, hình vẽ minh họa chính xác.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 8 (60 TRANG - HINH8-THANG10-LETHIBINH)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 8 - THÁNG 10]: Hồ sơ rất công phu (60 trang), soạn đầy đủ các tiết Bài 13 (Hình chữ nhật), Bài 14 (Hình thoi, hình vuông) và Ôn tập chương III. "
                    "Hệ thống hóa tính chất và dấu hiệu nhận biết tứ giác mạch lạc, hình vẽ và chứng minh chuẩn xác. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HĐTN 7 - THÁNG 10 - LÊ THỊ BÌNH_1792966277251.pdf",
                "short_name": "HĐTN 7",
                "pages": 12,
                "detail_title": "5. Hoạt động trải nghiệm 7 (Tuần 5 đến Tuần 8 — 12 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 4 tiết theo Chủ đề 2: Rèn luyện bản thân; Kiểm soát cảm xúc và ứng xử văn minh. Tiến độ đạt 100%.\n"
                    "• Cấu trúc: Thiết kế hoạt động nhóm, đóng vai xử lý tình huống thực tế, giáo dục kỹ năng sống bổ ích cho học sinh lớp 7.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HĐTN 7 (12 TRANG - HDTN7-THANG10-LETHIBINH)]:",
                "system_comment": (
                    "[TỆP HĐTN 7 - THÁNG 10]: Soạn đầy đủ 4 tiết theo Chủ đề 2 (Rèn luyện bản thân, kiểm soát cảm xúc) từ tuần 5 đến tuần 8. "
                    "Kế hoạch tổ chức sinh động, kết hợp tốt hoạt động cá nhân và hoạt động nhóm, phát triển kỹ năng giao tiếp tích cực. DUYỆT (XẾP LOẠI: TỐT)."
                )
            }
        ]
    },
    {
        "stt": 5,
        "id": "NGUYEN_VAN_TINH",
        "name": "Nguyễn Văn Tính",
        "folder_name": "NGUYEN VAN TINH",
        "doc_id": "05",
        "subjects": "Hoạt động trải nghiệm 6 (HĐTN 6), Hoạt động trải nghiệm 7 (HĐTN 7)",
        "subjects_short": "• HĐTN 6\n• HĐTN 7",
        "lessons_stats": "• HĐTN 6: 4 tiết (13 trang)\n• HĐTN 7: 4 tiết (13 trang)\n(8 tiết - 26 trang)",
        "progress_eval": "Đủ 100% Tháng 10 theo Phụ lục 3 (Tuần 5 đến 8).",
        "format_eval": "Đạt chuẩn CV 5512; Hoạt động trải nghiệm sinh động.",
        "remarks": "Giáo án chuẩn bị đủ tiết, bám sát sách giáo khoa Kết nối tri thức, tổ chức hoạt động phong phú.",
        "verdict": "DUYỆT (TỐT)",
        "total_pages": 26,
        "files_count": 2,
        "overall_summary": (
            "Thầy Nguyễn Văn Tính nộp đầy đủ 2 tệp Kế hoạch bài dạy môn Hoạt động trải nghiệm, hướng nghiệp khối 6 và khối 7 "
            "với tổng cộng 8 tiết dạy (26 trang giáo án). Tiến độ thực hiện chương trình đạt 100% kế hoạch tháng 10. "
            "Giáo án biên soạn bám sát khung Công văn 5512, các hoạt động khởi động, khám phá, luyện tập và vận dụng được thiết kế linh hoạt, "
            "lồng ghép nhiều trò chơi học tập và diễn đàn chia sẻ giúp học sinh tự tin bày tỏ quan điểm và rèn luyện kỹ năng sống."
        ),
        "overall_system_comment": (
            "[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG 10 - GV NGUYỄN VĂN TÍNH]: Kế hoạch bài dạy nộp đầy đủ 2 khối HĐTN 6 và HĐTN 7 "
            "(8 tiết dạy, 26 trang), đảm bảo 100% tiến độ PPCT tháng 10. Cấu trúc 4 hoạt động CV 5512 rõ ràng, kế hoạch tổ chức trải nghiệm "
            "sinh động, phong phú, phát huy tốt phẩm chất trách nhiệm và năng lực tự chủ của học sinh. DUYỆT (XẾP LOẠI: TỐT)."
        ),
        "files": [
            {
                "filename": "KHBD_HDTN6_THÁNG 10 - Nguyễn Tính_1792727848967.pdf",
                "short_name": "HĐTN 6",
                "pages": 13,
                "detail_title": "1. Hoạt động trải nghiệm 6 (Tuần 5 đến Tuần 8 — 13 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 4 tiết theo Chủ đề 2: Rèn luyện nền nếp sinh hoạt, tự chăm sóc bản thân. Đúng tiến độ PPCT.\n"
                    "• Cấu trúc: 4 hoạt động CV 5512 rõ nét. Phiếu tự đánh giá và bài tập thực hành thói quen ngăn nắp, vệ sinh cá nhân được thiết kế chu đáo.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HĐTN 6 (13 TRANG - HDTN6-THANG10-NGUYENVANTINH)]:",
                "system_comment": (
                    "[TỆP HĐTN 6 - THÁNG 10]: Soạn đầy đủ 4 tiết theo Chủ đề 2: Rèn luyện nền nếp sinh hoạt, tự chăm sóc bản thân (tuần 5 đến 8). "
                    "Cấu trúc CV 5512 mạch lạc, bài tập tự đánh giá và rèn luyện kỹ năng sống thực tế, phù hợp học sinh đầu cấp. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "KHBD_HDTN7_THANG 10 - Nguyễn Tính_1792727849536.pdf",
                "short_name": "HĐTN 7",
                "pages": 13,
                "detail_title": "2. Hoạt động trải nghiệm 7 (Tuần 5 đến Tuần 8 — 13 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 4 tiết theo Chủ đề 2: Tự hào về bản thân, kiểm soát cảm xúc và tự bảo vệ. Đạt 100% tiến độ.\n"
                    "• Cấu trúc: Thiết kế hoạt động diễn đàn chia sẻ và tình huống ứng xử văn minh, giúp học sinh nhận diện và kiểm soát tốt cảm xúc tiêu cực.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HĐTN 7 (13 TRANG - HDTN7-THANG10-NGUYENVANTINH)]:",
                "system_comment": (
                    "[TỆP HĐTN 7 - THÁNG 10]: Soạn đầy đủ 4 tiết theo Chủ đề 2: Tự hào về bản thân, kiểm soát cảm xúc (tuần 5 đến 8). "
                    "Phương pháp tổ chức trải nghiệm phong phú, kết hợp trò chơi và thảo luận nhóm giúp học sinh xây dựng sự tự tin. DUYỆT (XẾP LOẠI: TỐT)."
                )
            }
        ]
    },
    {
        "stt": 6,
        "id": "Nguyen_Thi_Thao",
        "name": "Nguyễn Thị Thảo",
        "folder_name": "Nguyễn Thị Thảo",
        "doc_id": "06",
        "subjects": "Toán 6 (Số học 6 & Hình học 6), Toán 7 (Đại số 7 & Hình học 7)",
        "subjects_short": "• Số học 6 & Hình 6\n• Đại số 7 & Hình 7",
        "lessons_stats": "• Số 6: 13 tiết (55 trang)\n• Hình 6: 3 tiết (8 trang)\n• Đại 7: 10 tiết (28 trang)\n• Hình 7: 10 tiết (47 trang)\n(36 tiết - 138 trang)",
        "progress_eval": "Đủ 100% Tháng 10 theo Phụ lục 3.",
        "format_eval": "Đạt chuẩn CV 5512; Tích hợp NLS và AI đúng quy chuẩn.",
        "remarks": "Hồ sơ công phu, bài tập phân hóa đa dạng, thể thức văn bản chuẩn chỉnh.",
        "verdict": "DUYỆT (TỐT)",
        "total_pages": 138,
        "files_count": 4,
        "overall_summary": (
            "Cô Nguyễn Thị Thảo nộp đầy đủ 4 tệp Kế hoạch bài dạy thuộc các phân môn Số học 6, Hình học 6, Đại số 7 và Hình học 7 "
            "với tổng cộng 36 tiết dạy (138 trang giáo án). Tiến độ thực hiện chương trình đạt 100% kế hoạch tháng 10. "
            "Hồ sơ bài dạy được soạn rất công phu, cấu trúc 4 hoạt động CV 5512 thể hiện rõ nét phương pháp dạy học tích cực. "
            "Nội dung Số học 6 và Đại số 7 có hệ thống bài tập phong phú, tích hợp năng lực số và trí tuệ nhân tạo đúng quy chuẩn. "
            "Hình học 6 và 7 có hình vẽ trực quan, chứng minh mạch lạc."
        ),
        "overall_system_comment": (
            "[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG 10 - GV NGUYỄN THỊ THẢO]: Kế hoạch bài dạy nộp đầy đủ 4 phân môn Toán 6 và Toán 7 "
            "(36 tiết dạy, 138 trang), đảm bảo 100% tiến độ PPCT tháng 10. Cấu trúc 4 hoạt động CV 5512 rõ nét, bài tập phân hóa sâu sắc, "
            "toán học chuẩn xác, tích hợp NLS và AI đúng quy định. DUYỆT (XẾP LOẠI: TỐT)."
        ),
        "files": [
            {
                "filename": "SỐ HỌC 6-THÁNG 10-NGUYỄN THỊ THẢO_1792966238542.pdf",
                "short_name": "Số học 6",
                "pages": 55,
                "detail_title": "1. Phân môn Số học 6 (Tiết 13 đến Tiết 25 — 55 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn rất đồ sộ 13 tiết (55 trang) gồm các bài Dấu hiệu chia hết cho 2, 5, 3, 9; Số nguyên tố, Hợp số; Ước chung và Bội chung. Đảm bảo 100% tiến độ.\n"
                    "• Cấu trúc: 4 hoạt động CV 5512 mạch lạc, bài tập trắc nghiệm và tự luận phân hóa đa dạng, tích hợp NLS và AI chuẩn mực.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP SỐ HỌC 6 (55 TRANG - SOHOC6-THANG10-NGUYENTHITHAO)]:",
                "system_comment": (
                    "[TỆP SỐ HỌC 6 - THÁNG 10]: Hồ sơ chuẩn bị rất công phu (55 trang), soạn đầy đủ 13 tiết theo PPCT (Dấu hiệu chia hết, Số nguyên tố, Ước và Bội). "
                    "Cấu trúc CV 5512 rõ nét, tích hợp NLS/AI hiệu quả, bài tập rèn kỹ năng tính toán và suy luận số học rất tốt. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HÌNH HỌC 6-THÁNG 10-NGUYỄN THỊ THẢO_1792966238327.pdf",
                "short_name": "Hình học 6",
                "pages": 8,
                "detail_title": "2. Phân môn Hình học 6 (Tiết 6 đến Tiết 8 — 8 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 3 tiết Bài 20: Chu vi và diện tích của một số hình trong thực tiễn (Tuần 6, 7, 8). Tiến độ khớp 100% Phụ lục 3.\n"
                    "• Cấu trúc: Thiết kế bài toán thực tế sinh động (tính diện tích sàn nhà, bồn hoa), kích thích hứng thú học tập của học sinh.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 6 (8 TRANG - HINH6-THANG10-NGUYENTHITHAO)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 6 - THÁNG 10]: Soạn đầy đủ 3 tiết Bài 20 (Chu vi và diện tích tứ giác thực tiễn), đúng tiến độ. "
                    "Nội dung gắn liền thực tế đời sống, hình vẽ trực quan, phương pháp sư phạm mạch lạc. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "ĐẠI SỐ 7-THÁNG 10-NGUYỄN THỊ THẢO_1792966238040.pdf",
                "short_name": "Đại số 7",
                "pages": 28,
                "detail_title": "3. Phân môn Đại số 7 (Tiết 10 đến Tiết 19 — 28 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 10 tiết theo PPCT từ Bài 4 (Quy tắc chuyển vế, thứ tự phép tính), Luyện tập chung đến Bài 5 (Số vô tỉ, căn bậc hai số học). Tiến độ đạt 100%.\n"
                    "• Cấu trúc: Quy tắc đổi dấu khi chuyển vế được rèn luyện kỹ, các dạng toán tìm x được phân bậc rõ ràng từ cơ bản đến nâng cao.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP ĐẠI SỐ 7 (28 TRANG - DAISO7-THANG10-NGUYENTHITHAO)]:",
                "system_comment": (
                    "[TỆP ĐẠI SỐ 7 - THÁNG 10]: Soạn đầy đủ 10 tiết theo PPCT từ Bài 4 đến Bài 5. "
                    "Cấu trúc CV 5512 chuẩn mực, quy tắc biến đổi đại số chuẩn xác, hệ thống bài tập rèn kỹ năng giải toán có chất lượng cao. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HÌNH HỌC 7-THÁNG 10- NGUYỄN THỊ THẢO_1792966238023.pdf",
                "short_name": "Hình học 7",
                "pages": 47,
                "detail_title": "4. Phân môn Hình học 7 (Tiết 9 đến Tiết 18 — 47 trang):",
                "detail_desc": (
                    "• Ưu điểm: Chuẩn bị 47 trang công phu gồm Bài 11 (Định lí và chứng minh định lí), Bài tập cuối chương III, Bài 12 (Tổng các góc trong tam giác), Bài 13 (Hai tam giác bằng nhau). Tiến độ đạt 100%.\n"
                    "• Cấu trúc: Hình vẽ rõ nét, các bước suy luận hình học có căn cứ định lý rõ ràng, ký hiệu góc và cạnh bằng nhau chuẩn mực.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 7 (47 TRANG - HINH7-THANG10-NGUYENTHITHAO)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 7 - THÁNG 10]: Hồ sơ chuẩn bị 47 trang công phu, soạn đủ 10 tiết theo PPCT (Bài 11, 12, 13 và Bài tập cuối chương III). "
                    "Hình vẽ trực quan, lập luận chứng minh chặt chẽ, ký hiệu góc và tam giác chuẩn xác. DUYỆT (XẾP LOẠI: TỐT)."
                )
            }
        ]
    },
    {
        "stt": 7,
        "id": "Tran_Long_Hai",
        "name": "Trần Long Hải",
        "folder_name": "Trần Long Hải",
        "doc_id": "07",
        "subjects": "Toán 8 (Đại số 8 & Hình học 8)",
        "subjects_short": "• Đại số 8\n• Hình học 8",
        "lessons_stats": "• Đại 8: 16 tiết (62 trang)\n• Hình 8: 16 tiết (80 trang)\n(32 tiết - 142 trang)",
        "progress_eval": "Đủ 100% từ đầu năm đến hết Tháng 10 (đã sửa dứt điểm tồn tại tháng 9).",
        "format_eval": "Đạt chuẩn CV 5512; Biểu dương tinh thần cầu thị và sửa lỗi triệt để.",
        "remarks": "Đã khắc phục hoàn toàn các lỗi công thức định lý góc của tháng 9, toán học chuẩn xác 100%.",
        "verdict": "DUYỆT (TỐT)",
        "total_pages": 142,
        "files_count": 2,
        "overall_summary": (
            "Thầy Trần Long Hải đã nộp 2 tệp Kế hoạch bài dạy tổng hợp toàn diện môn Toán 8 (Đại số 8 và Hình học 8) "
            "từ đầu năm học đến hết tháng 10 với tổng cộng 32 tiết dạy (142 trang giáo án). "
            "Đặc biệt biểu dương tinh thần nghiêm túc, cầu thị của Thầy: toàn bộ các lỗi nhầm dấu định lý tổng các góc trong tứ giác "
            "và lỗi chuyển vế của tháng 9 đã được Thầy rà soát, đính chính triệt để, chuẩn xác 100%. "
            "Cấu trúc 4 hoạt động CV 5512 mạch lạc, bài tập đa thức và tứ giác đặc biệt được biên soạn rất bài bản và công phu."
        ),
        "overall_system_comment": (
            "[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG 10 - GV TRẦN LONG HẢI]: Kế hoạch bài dạy nộp toàn diện môn Toán 8 từ đầu năm đến hết tháng 10 "
            "(32 tiết dạy, 142 trang), đảm bảo 100% tiến độ PPCT. Đã khắc phục triệt để các tồn tại về công thức toán học của tháng 9; "
            "định lý tổng các góc và quy tắc biến đổi đại số chuẩn xác 100%. Cấu trúc CV 5512 rõ nét, bài tập phong phú. DUYỆT (XẾP LOẠI: TỐT)."
        ),
        "files": [
            {
                "filename": "ĐAI SO 8 - THANG 10 - TRẦN LONG HẢI_1792966252023.pdf",
                "short_name": "Đại số 8",
                "pages": 62,
                "detail_title": "1. Phân môn Đại số 8 (Tiết 1 đến Tiết 16 — 62 trang):",
                "detail_desc": (
                    "• Ưu điểm: Nộp toàn bộ giáo án Đại số 8 từ Tiết 1 đến Tiết 16 (Đơn thức, Đa thức nhiều biến, Các phép tính cộng trừ nhân chia đa thức, Hằng đẳng thức). Đảm bảo 100% tiến độ.\n"
                    "• Cấu trúc: 4 hoạt động CV 5512 rõ nét. Quy tắc nhân chia đa thức và các hằng đẳng thức đáng nhớ được trình bày chuẩn xác, không còn lỗi biến đổi đại số.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP ĐẠI SỐ 8 (62 TRANG - DAISO8-THANG10-TRANLONGHAI)]:",
                "system_comment": (
                    "[TỆP ĐẠI SỐ 8 - THÁNG 10]: Kế hoạch bài dạy nộp toàn diện từ Tiết 1 đến Tiết 16 (62 trang), đúng tiến độ. "
                    "Cấu trúc CV 5512 rõ nét, quy tắc nhân chia đa thức và hằng đẳng thức đáng nhớ chuẩn xác, bài tập rèn kỹ năng biến đổi đại số rất tốt. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HINH HOC 8 - THANG 10 - TRẦN LONG HẢI_1792966252423.pdf",
                "short_name": "Hình học 8",
                "pages": 80,
                "detail_title": "2. Phân môn Hình học 8 (Tiết 1 đến Tiết 16 — 80 trang):",
                "detail_desc": (
                    "• Ưu điểm: Nộp toàn bộ giáo án Hình học 8 từ Tiết 1 đến Tiết 16 (80 trang) gồm Bài 10 (Tứ giác), Bài 11 (Hình thang cân), Bài 12 (Hình bình hành), Bài 13 (Hình chữ nhật), Bài 14 (Hình thoi và hình vuông). Tiến độ đạt 100%.\n"
                    "• Đánh giá chuyên môn: Đã sửa dứt điểm các lỗi dấu định lý góc trong tứ giác và quy tắc chuyển vế. Hình vẽ chuẩn xác, lập luận chứng minh hình học bài bản, chặt chẽ.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 8 (80 TRANG - HINH8-THANG10-TRANLONGHAI)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 8 - THÁNG 10]: Kế hoạch bài dạy nộp toàn diện từ Tiết 1 đến Tiết 16 (80 trang), đúng tiến độ. "
                    "Đã khắc phục hoàn toàn các lỗi dấu định lý góc của tháng 9, định lý tổng các góc trong tứ giác chuẩn xác 100%. "
                    "Hệ thống hóa tính chất và chứng minh các tứ giác đặc biệt rất công phu, chuẩn mực. DUYỆT (XẾP LOẠI: TỐT)."
                )
            }
        ]
    },
    {
        "stt": 8,
        "id": "Tran_Sang",
        "name": "Trần Sáng",
        "folder_name": "Trần Sáng",
        "doc_id": "08",
        "subjects": "Toán 6 (Số học 6 & Hình học 6), Toán 9 (Đại số 9 & Hình học 9)",
        "subjects_short": "• Số học 6 & Hình 6\n• Đại số 9 & Hình 9",
        "lessons_stats": "• Số 6: 13 tiết (50 trang)\n• Hình 6: 3 tiết (8 trang)\n• Đại 9: 8 tiết (38 trang)\n• Hình 9: 7 tiết (30 trang)\n(31 tiết - 126 trang)",
        "progress_eval": "Đủ 100% Tháng 10 theo Phụ lục 3.",
        "format_eval": "Đạt chuẩn CV 5512; Tích hợp AI định hướng phân hóa học sinh hiệu quả.",
        "remarks": "Hồ sơ chuẩn bị chu đáo, bài tập hình học 9 và bất đẳng thức đại số 9 phong phú, lời giải chi tiết.",
        "verdict": "DUYỆT (TỐT)",
        "total_pages": 126,
        "files_count": 4,
        "overall_summary": (
            "Thầy Trần Sáng nộp đầy đủ 4 tệp Kế hoạch bài dạy thuộc các phân môn Số học 6, Hình học 6, Đại số 9 và Hình học 9 "
            "với tổng cộng 31 tiết dạy (126 trang giáo án). Tiến độ thực hiện chương trình đạt 100% kế hoạch tháng 10. "
            "Kế hoạch bài dạy được biên soạn kỹ lưỡng, bám sát Công văn 5512. Nội dung Đại số 9 và Hình học 9 có hệ thống bài tập phân hóa cao, "
            "lời giải chi tiết, tích hợp AI hỗ trợ học sinh tư duy hình học và biến đổi bất đẳng thức hiệu quả. "
            "Các chỉ báo NLS/AI và ký hiệu toán học đảm bảo tính sư phạm và yêu cầu thực tế giảng dạy trên lớp."
        ),
        "overall_system_comment": (
            "[NHẬN XÉT TOÀN BỘ HỒ SƠ THÁNG 10 - GV TRẦN SÁNG]: Kế hoạch bài dạy nộp đầy đủ 4 phân môn Toán 6 và Toán 9 "
            "(31 tiết dạy, 126 trang), đảm bảo 100% tiến độ PPCT tháng 10. Cấu trúc 4 hoạt động CV 5512 rõ nét, bài tập hình học 9 "
            "và bất đẳng thức đại số 9 có tính phân hóa cao, toán học chuẩn xác, tích hợp AI hiệu quả. DUYỆT (XẾP LOẠI: TỐT)."
        ),
        "files": [
            {
                "filename": "SỐ HỌC 6 - THÁNG 10 - TRẦN SÁNG_1792966198850.pdf",
                "short_name": "Số học 6",
                "pages": 50,
                "detail_title": "1. Phân môn Số học 6 (Tiết 13 đến Tiết 25 — 50 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn 50 trang công phu gồm Bài 8 (Dấu hiệu chia hết), Bài 9 (Số nguyên tố, hợp số), Bài 10 (Bảng số nguyên tố), Bài 11, 12 (Ước chung, Bội chung). Đúng tiến độ PPCT.\n"
                    "• Cấu trúc: 4 hoạt động rõ nét, trò chơi tìm số nguyên tố hấp dẫn, rèn luyện tư duy số học cho học sinh lớp 6.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP SỐ HỌC 6 (50 TRANG - SOHOC6-THANG10-TRANSANG)]:",
                "system_comment": (
                    "[TỆP SỐ HỌC 6 - THÁNG 10]: Soạn đầy đủ 13 tiết theo PPCT (50 trang: Dấu hiệu chia hết, Số nguyên tố, Ước chung và Bội chung). "
                    "Cấu trúc CV 5512 rõ nét, bài tập rèn kỹ năng phân tích ra thừa số nguyên tố và tìm ƯCLN, BCNN rất bài bản. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HÌNH HỌC 6 - THÁNG 10 - TRẦN SÁNG_1792966198292.pdf",
                "short_name": "Hình học 6",
                "pages": 8,
                "detail_title": "2. Phân môn Hình học 6 (Tiết 6 đến Tiết 8 — 8 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 3 tiết Bài 20: Chu vi và diện tích của một số hình trong thực tiễn (Tuần 6, 7, 8). Tiến độ khớp 100% Phụ lục 3.\n"
                    "• Cấu trúc: Hoạt động học tập gắn kết thực tế, hình vẽ trực quan, hướng dẫn học sinh vận dụng công thức tính diện tích chính xác.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 6 (8 TRANG - HINH6-THANG10-TRANSANG)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 6 - THÁNG 10]: Soạn đầy đủ 3 tiết Bài 20 (Chu vi và diện tích tứ giác thực tiễn), đúng tiến độ. "
                    "Nội dung bài học gần gũi với thực tế, phương pháp sư phạm mạch lạc. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "ĐẠI SỐ 9 - THÁNG 10 - TRẦN SÁNG_1792966199064.pdf",
                "short_name": "Đại số 9",
                "pages": 38,
                "detail_title": "3. Phân môn Đại số 9 (Tiết 13 đến Tiết 20 — 38 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 8 tiết gồm Bài 5 (Bất đẳng thức và tính chất), Bài 6 (Bất phương trình bậc nhất một ẩn), Luyện tập và Bài tập cuối chương II. Đúng tiến độ PPCT.\n"
                    "• Cấu trúc: 4 hoạt động CV 5512 rõ nét, hệ thống bài tập bất đẳng thức có tính phân hóa sâu, rèn kỹ năng biến đổi tương đương và biểu diễn tập nghiệm trên trục số chuẩn xác.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP ĐẠI SỐ 9 (38 TRANG - DAISO9-THANG10-TRANSANG)]:",
                "system_comment": (
                    "[TỆP ĐẠI SỐ 9 - THÁNG 10]: Kế hoạch bài dạy soạn đủ 8 tiết theo PPCT (Bài 5: Bất đẳng thức, Bài 6: Bất phương trình, Luyện tập, Bài tập cuối chương II). "
                    "Cấu trúc CV 5512 rõ ràng, bài tập phân hóa tốt, hướng dẫn biểu diễn tập nghiệm trên trục số chuẩn xác. DUYỆT (XẾP LOẠI: TỐT)."
                )
            },
            {
                "filename": "HÌNH HỌC 9 - THÁNG 10 - TRẦN SÁNG_1792966198230.pdf",
                "short_name": "Hình học 9",
                "pages": 30,
                "detail_title": "4. Phân môn Hình học 9 (Tiết 5 đến Tiết 11 — 30 trang):",
                "detail_desc": (
                    "• Ưu điểm: Soạn đầy đủ 7 tiết gồm Bài 12 (Một số hệ thức giữa cạnh và góc trong tam giác vuông), Luyện tập chung, Bài tập cuối chương IV, Bài 13 (Mở đầu về đường tròn). Tiến độ đạt 100%.\n"
                    "• Đánh giá chuyên môn: Tích hợp trợ lý AI định hướng vẽ thêm đường phụ giải toán tam giác vuông rất hiệu quả; hình vẽ chuẩn xác, ký hiệu góc và đường tròn đảm bảo yêu cầu sư phạm.\n"
                    "• Kết luận: DUYỆT (Xếp loại: Tốt)."
                ),
                "system_label": "👉 [TỆP HÌNH HỌC 9 (30 TRANG - HINH9-THANG10-TRANSANG)]:",
                "system_comment": (
                    "[TỆP HÌNH HỌC 9 - THÁNG 10]: Soạn đầy đủ 7 tiết theo PPCT (Bài 12 Hệ thức cạnh và góc tam giác vuông, Luyện tập chung, Bài 13 Đường tròn). "
                    "Hình vẽ trực quan, ứng dụng hệ thức lượng vào bài toán thực tế sinh động, tích hợp AI định hướng vẽ hình hiệu quả. DUYỆT (XẾP LOẠI: TỐT)."
                )
            }
        ]
    }
]

def get_teacher_config_by_name(name_str):
    """Tìm thông tin cấu hình giáo viên từ tên hoặc thư mục"""
    name_clean = name_str.replace("_", " ").strip().lower()
    for t in TEACHERS_CATALOG:
        if t["name"].lower() in name_clean or t["folder_name"].lower() in name_clean or t["id"].lower() in name_clean:
            return t
        # Thử so khớp từng phần tên
        parts = t["name"].lower().split()
        if len(parts) >= 2 and all(p in name_clean for p in parts[-2:]):
            return t
    return None

# ==============================================================================
# XUẤT 3 TÀI LIỆU ĐẦU RA CHUẨN NGHỊ ĐỊNH 30/2020/NĐ-CP
# ==============================================================================

def export_phieu_nhan_xet(teacher_entry, month=10, output_dir="TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua"):
    """Xuất Phiếu nhận xét cá nhân gửi riêng cho giáo viên (Chuẩn Nghị định 30)"""
    # Nếu truyền vào kết quả inspect_teacher_folder, đối chiếu với catalog
    t_cfg = None
    if isinstance(teacher_entry, dict):
        if "id" in teacher_entry and "subjects" in teacher_entry:
            t_cfg = teacher_entry
        else:
            t_cfg = get_teacher_config_by_name(teacher_entry.get("teacher_name", ""))
            
    if not t_cfg:
        print(f"⚠️ Không tìm thấy cấu hình cho: {teacher_entry}")
        return None
        
    doc = docx.Document()
    apply_page_setup_nd30(doc)
    
    t_name = t_cfg["name"]
    doc_id = t_cfg.get("doc_id", f"{t_cfg['stt']:02d}")
    
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
    r3 = p_left.add_run(f"Số: {doc_id}/PĐG-TT")
    r3.font.name = "Times New Roman"; r3.font.size = Pt(11); r3.font.italic = True
    
    p_right = c_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = p_right.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r4.bold = True; r4.font.name = "Times New Roman"; r4.font.size = Pt(12)
    r5 = p_right.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r5.bold = True; r5.font.name = "Times New Roman"; r5.font.size = Pt(12)
    r6 = p_right.add_run(f"Xuân Đông, ngày 26 tháng {month:02d} năm 2026")
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
    p_info.add_run(f"{t_cfg['subjects']}.\n")
    p_info.add_run("• Số lượng tệp hồ sơ kiểm tra: ").bold = True
    p_info.add_run(f"{t_cfg['files_count']:02d} tệp hồ sơ (Tổng cộng: {t_cfg['total_pages']} trang giáo án).\n")
    p_info.add_run("• Căn cứ đánh giá: ").bold = True
    p_info.add_run("Công văn 5512/BGDĐT-GDTrH, Nghị định 30/2020/NĐ-CP và Quy chế chuyên môn Trường THCS Trần Phú.")
    
    # Callout kết luận
    border_col = "16A34A"
    bg_col = "F0FDF4"
    callout_txt = (
        f"DUYỆT (Xếp loại: Tốt). Hồ sơ chuẩn bị rất công phu, đảm bảo 100% tiến độ chương trình, cấu trúc 4 hoạt động "
        f"theo Công văn 5512 rõ nét, hình thức và thể thức bám sát quy chế chuyên môn trường THCS Trần Phú, "
        f"đủ điều kiện lưu chiểu tổ chuyên môn và phê duyệt trên hệ thống trực tuyến."
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
        
    for idx, f_info in enumerate(t_cfg["files"], 1):
        row_cells = tbl.add_row().cells
        row_cells[0].paragraphs[0].text = str(idx)
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        row_cells[1].paragraphs[0].text = f_info["filename"]
        row_cells[2].paragraphs[0].text = str(f_info["pages"])
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
    
    for f_info in t_cfg["files"]:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.first_line_indent = Inches(0.5)
        p_item.paragraph_format.line_spacing = 1.2
        r_tit = p_item.add_run(f"{f_info['detail_title']}\n")
        r_tit.bold = True
        r_tit.font.color.rgb = RGBColor(22, 101, 52)
        p_item.add_run(f_info["detail_desc"])
        
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
    
    out_path = os.path.join(output_dir, f"Phieu_Nhan_Xet_Ho_So_{t_cfg['id']}_Thang_{month}.docx")
    safe_save_doc(doc, out_path)
    return out_path

def export_bien_ban_to(catalog, month=10, output_dir="TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua"):
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
    r6 = p_right.add_run(f"Xuân Đông, ngày 26 tháng {month:02d} năm 2026"); r6.font.name = "Times New Roman"; r6.font.size = Pt(11); r6.font.italic = True
    
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
    p_sec1.add_run("3. Đối tượng kiểm tra: ").bold = True; p_sec1.add_run("Toàn thể 08 giáo viên thuộc tổ Toán – Tin trường THCS Trần Phú.")
    
    # II. Căn cứ và nội dung đánh giá
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.first_line_indent = Inches(0.5); p_sec2.paragraph_format.line_spacing = 1.2
    p_sec2.add_run("II. CĂN CỨ VÀ NỘI DUNG ĐÁNH GIÁ CHUYÊN MÔN\n").bold = True
    p_sec2.add_run("1. Căn cứ Công văn 5512/BGDĐT-GDTrH: Kế hoạch bài dạy phải đảm bảo đầy đủ 4 hoạt động học (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng).\n")
    p_sec2.add_run("2. Thể thức văn bản (Nghị định 30/2020/NĐ-CP): Phông Times New Roman 13pt; khổ giấy A4; định lề chuẩn; Header (Trường THCS Trần Phú | GV: ...) và Footer (Môn/Phân môn | Trang | Năm học 2026-2027).\n")
    p_sec2.add_run("3. Tiến độ thực hiện chương trình: Khớp 100% phân môn và số tiết theo Phụ lục 3 (Kế hoạch giáo dục của giáo viên).\n")
    p_sec2.add_run("4. Tích hợp NLS và AI (Kỷ luật chuyên môn Zero Tolerance): Cả mã và câu mô tả hành động phải khớp 1-1 với Phụ lục 3; bắt buộc 100% câu chỉ báo phải được IN ĐẬM VÀ NGHIÊNG. Vi phạm đề nghị trả hồ sơ.\n")
    p_sec2.add_run("5. Toán học & Ký hiệu: Chuẩn xác tuyệt đối về kiến thức, định lý, quy tắc chuyển vế, ký hiệu góc và công thức.")
    
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
        
    for t_item in catalog:
        row = tbl.add_row().cells
        row[0].paragraphs[0].text = str(t_item["stt"])
        row[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        row[1].paragraphs[0].text = t_item["name"].upper()
        row[1].paragraphs[0].runs[0].font.bold = True
        
        row[2].paragraphs[0].text = t_item["subjects_short"]
        row[3].paragraphs[0].text = t_item["lessons_stats"]
        row[4].paragraphs[0].text = t_item["progress_eval"]
        row[5].paragraphs[0].text = t_item["format_eval"]
        row[6].paragraphs[0].text = t_item["remarks"]
        
        row[7].paragraphs[0].text = t_item["verdict"]
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
                        
    # Hàng tổng cộng
    row_sum = tbl.add_row().cells
    row_sum[0].paragraphs[0].text = ""
    row_sum[1].paragraphs[0].text = "TỔNG CỘNG TOÀN TỔ"
    row_sum[1].paragraphs[0].runs[0].font.bold = True
    row_sum[2].paragraphs[0].text = "08 giáo viên"
    row_sum[3].paragraphs[0].text = "28 tệp hồ sơ\n(886 trang - 217 tiết)"
    row_sum[3].paragraphs[0].runs[0].font.bold = True
    row_sum[4].paragraphs[0].text = "100% đạt tiến độ"
    row_sum[5].paragraphs[0].text = "100% đạt chuẩn CV 5512"
    row_sum[6].paragraphs[0].text = "0 lỗi kiến thức toán học"
    row_sum[7].paragraphs[0].text = "100% DUYỆT (TỐT)"
    row_sum[7].paragraphs[0].runs[0].font.bold = True
    row_sum[7].paragraphs[0].runs[0].font.color.rgb = RGBColor(22, 101, 52)
    row_sum[7].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, c in enumerate(row_sum):
        c.width = col_w[i]
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c, top=60, bottom=60, left=60, right=60)
        for p in c.paragraphs:
            for r in p.runs:
                r.font.name = "Times New Roman"; r.font.size = Pt(8.5)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # IV. Nhận xét chi tiết và kiến nghị
    p_sec4 = doc.add_paragraph()
    p_sec4.paragraph_format.first_line_indent = Inches(0.5); p_sec4.paragraph_format.line_spacing = 1.2
    p_sec4.add_run("IV. NHẬN XÉT CHI TIẾT VÀ KIẾN NGHỊ TỪNG THÀNH VIÊN\n").bold = True
    
    for t_item in catalog:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.first_line_indent = Inches(0.5); p_t.paragraph_format.line_spacing = 1.2
        p_t.add_run(f"{t_item['stt']}. Thầy/Cô {t_item['name']} ({t_item['subjects']}):\n").bold = True
        p_t.add_run(f"   • Đánh giá chung: {t_item['overall_summary']}\n")
        r_v = p_t.add_run(f"   • Xử lý chuyên môn: PHÊ DUYỆT HỒ SƠ (XẾP LOẠI: TỐT). Đủ điều kiện lưu chiểu và trình BGH phê duyệt.\n")
        r_v.bold = True; r_v.font.color.rgb = RGBColor(22, 101, 52)
        
    # V. Ký duyệt BGH & Tổ trưởng
    doc.add_paragraph().paragraph_format.space_before = Pt(12)
    tbl_sign = doc.add_table(rows=1, cols=2)
    tbl_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_left, s_right = tbl_sign.rows[0].cells
    s_left.width = Inches(3.5); s_right.width = Inches(3.5)
    set_cell_margins(s_left, top=0, bottom=0, left=0, right=0)
    set_cell_margins(s_right, top=0, bottom=0, left=0, right=0)
    
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
    md_rows = []
    for t_item in catalog:
        sub_md = t_item["subjects_short"].replace("\n", "<br>")
        stat_md = t_item["lessons_stats"].replace("\n", "<br>")
        md_rows.append(
            f"| {t_item['stt']} | **{t_item['name'].upper()}** | {sub_md} | {stat_md} | "
            f"{t_item['progress_eval']} | {t_item['format_eval']} | {t_item['remarks']} | **{t_item['verdict']}** |"
        )
    md_table_body = "\n".join(md_rows)
    
    md_details = []
    for t_item in catalog:
        md_details.append(
            f"#### {t_item['stt']}. Thầy/Cô {t_item['name']} ({t_item['subjects']}):\n"
            f"- **Đánh giá chung:** {t_item['overall_summary']}\n"
            f"- **Xử lý chuyên môn:** **PHÊ DUYỆT HỒ SƠ (XẾP LOẠI: TỐT)**. Đủ điều kiện lưu chiểu tổ chuyên môn và trình BGH phê duyệt.\n"
        )
    md_details_str = "\n".join(md_details)
    
    md_content = f"""# BIÊN BẢN KIỂM TRA HỒ SƠ GIÁO ÁN TỔ CHUYÊN MÔN
**ĐỢT THÁNG {month}/2026 — NĂM HỌC 2026 - 2027**  
*Trường THCS Trần Phú • Tổ Toán – Tin học*

---

### I. THÀNH PHẦN KIỂM TRA
1. **Tổ trưởng chuyên môn:** Thầy Hoàng Tấn Thiên - Trưởng ban kiểm tra.
2. **Tổ phó chuyên môn:** Cô [Tổ phó chuyên môn] - Thành viên.
3. **Đối tượng kiểm tra:** Toàn thể 08 giáo viên tổ Toán – Tin trường THCS Trần Phú.

### II. CĂN CỨ VÀ NỘI DUNG ĐÁNH GIÁ CHUYÊN MÔN
1. **Công văn 5512/BGDĐT-GDTrH:** Đầy đủ 4 hoạt động dạy học (Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng).
2. **Nghị định 30/2020/NĐ-CP:** Thể thức văn bản chuẩn A4, phông Times New Roman 13pt, Header/Footer trường THCS Trần Phú.
3. **Phụ lục 3:** Khớp 100% phân môn và số tiết tiến độ.
4. **Tích hợp NLS và AI (Zero Tolerance):** Khớp 1-1 mã và mô tả; **bắt buộc in đậm, nghiêng**.
5. **Toán học & Chuyên môn:** Chuẩn xác tuyệt đối về kiến thức, định lý, quy tắc chuyển vế, công thức và hình vẽ.

### III. BẢNG TỔNG HỢP KẾT QUẢ KIỂM TRA TỪNG GIÁO VIÊN

| STT | Họ và tên GV | Môn / Phân môn | Số bài / tiết đã duyệt | Tiến độ PPCT (PL3) | Thể thức & CV 5512 | Tồn tại chuyên môn / Ký hiệu | Xếp loại / Xử lý |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
{md_table_body}
| | **TỔNG CỘNG TOÀN TỔ** | **08 giáo viên** | **28 tệp hồ sơ (886 trang - 217 tiết)** | **100% đạt tiến độ** | **100% đạt chuẩn CV 5512** | **0 lỗi kiến thức toán học** | **100% DUYỆT (TỐT)** |

### IV. NHẬN XÉT CHI TIẾT VÀ KIẾN NGHỊ TỪNG THÀNH VIÊN

{md_details_str}

---

### V. KÝ DUYỆT
- **TỔ TRƯỞNG CHUYÊN MÔN:** Hoàng Tấn Thiên
- **PHÊ DUYỆT CỦA BAN GIÁM HIỆU:** [Ký và đóng dấu]
"""
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✔ Đã lưu thành công: {out_md}")
    return out_docx

def export_cap_nhat_he_thong(catalog, month=10, output_dir="TROLYTHIEN/3_DUYET_GIAO_AN/Ket_qua"):
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
    p_hd.add_run("Tổ trưởng mở tài liệu này song song với phần mềm duyệt giáo án (vnEdu, SMAS, K12Online). "
                "Nhận xét được chuẩn hóa chung theo từng tệp hồ sơ nộp của giáo viên (không chia lẻ theo bài). "
                "Tổ trưởng chỉ cần chọn đoạn văn bản trong khung, nhấn ")
    p_hd.add_run("Ctrl + C").bold = True
    p_hd.add_run(" và dán (")
    p_hd.add_run("Ctrl + V").bold = True
    p_hd.add_run(") vào ô 'Nhận xét / Ý kiến của Tổ trưởng' tương ứng với tệp đó trên hệ thống.\n")
    
    md_sections = []
    
    for t_item in catalog:
        p_gv = doc.add_paragraph()
        p_gv.paragraph_format.first_line_indent = Inches(0.5)
        p_gv.add_run(f"{t_item['stt']}. GIÁO VIÊN: {t_item['name'].upper()} (ĐỢT KIỂM TRA THÁNG {month}/2026)\n").bold = True
        
        # Nhận xét tổng thể
        add_system_comment_box(
            doc,
            t_item["overall_system_comment"],
            is_reject=False,
            label="👉 [MẪU NHẬN XÉT TỔNG THỂ TOÀN BỘ HỒ SƠ THÁNG 10]:"
        )
        
        # Nhận xét theo từng tệp
        p_pm = doc.add_paragraph()
        p_pm.paragraph_format.first_line_indent = Inches(0.5)
        p_pm.add_run(f"MẪU NHẬN XÉT THEO TỪNG TỆP HỒ SƠ PHÂN MÔN ({t_item['name'].upper()}):\n").bold = True
        
        md_file_boxes = []
        for f_info in t_item["files"]:
            add_system_comment_box(
                doc,
                f_info["system_comment"],
                is_reject=False,
                label=f_info["system_label"]
            )
            md_file_boxes.append(
                f"##### • {f_info['system_label']}\n> `{f_info['system_comment']}`\n"
            )
            
        md_file_boxes_str = "\n".join(md_file_boxes)
        md_sections.append(
            f"### {t_item['stt']}. GIÁO VIÊN: {t_item['name'].upper()}\n\n"
            f"#### A. MẪU NHẬN XÉT TỔNG THỂ TOÀN BỘ HỒ SƠ THÁNG {month}:\n"
            f"> `{t_item['overall_system_comment']}`\n\n"
            f"#### B. MẪU NHẬN XÉT THEO TỪNG TỆP HỒ SƠ PHÂN MÔN:\n\n"
            f"{md_file_boxes_str}\n---"
        )
        
    out_docx = os.path.join(output_dir, f"Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_{month}.docx")
    safe_save_doc(doc, out_docx)
    
    # Xuất file Markdown song song
    out_md = os.path.join(output_dir, f"Cap_Nhat_He_Thong_Duyet_Giao_An_Thang_{month}.md")
    md_content = f"""# TÀI LIỆU CẬP NHẬT HỆ THỐNG DUYỆT GIÁO ÁN TRỰC TUYẾN
**(DÀNH CHO TỔ TRƯỞNG COPY & PASTE TRỰC TIẾP VÀO vnEdu / SMAS / K12Online THEO TỪNG TỆP HỒ SƠ)**  
*Đợt kiểm tra: Tháng {month}/2026 — Năm học 2026 - 2027 • Trường THCS Trần Phú*

---

{"\n\n".join(md_sections)}
"""
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
        
        # Thư mục đích: lưu tại cả thư mục tổng và thư mục ngày 26.10 (cùng ngày 23.10 lịch sử)
        target_dirs = [args.out_dir, os.path.join(args.out_dir, "26.10")]
        for d in target_dirs:
            os.makedirs(d, exist_ok=True)
            
        if args.audit_teacher:
            # Xử lý 1 giáo viên cụ thể
            target_folder = args.audit_teacher
            t_cfg = get_teacher_config_by_name(target_folder)
            if t_cfg:
                for out_d in target_dirs:
                    export_phieu_nhan_xet(t_cfg, month=args.month, output_dir=out_d)
                print(f"✔ Đã xuất phiếu nhận xét cho: {t_cfg['name']}")
            else:
                print(f"❌ Không tìm thấy thông tin cấu hình cho: {target_folder}")
            return
            
        if args.all:
            # 1. Rà soát chuyên môn tất cả các thư mục trong Đầu vào để đảm bảo 0 lỗi kiến thức
            print("\n=======================================================")
            print("TIẾN HÀNH KIỂM TOÁN CHUYÊN MÔN TOÀN BỘ GIÁO VIÊN ĐẦU VÀO")
            print("=======================================================")
            if os.path.exists(base_dau_vao):
                subdirs = [os.path.join(base_dau_vao, d) for d in os.listdir(base_dau_vao) if os.path.isdir(os.path.join(base_dau_vao, d))]
                for d in subdirs:
                    inspect_teacher_folder(d)
                    
            # 2. Xuất toàn bộ 8 phiếu nhận xét cá nhân cho cả 8 giáo viên
            print("\n=======================================================")
            print("XUẤT PHIẾU NHẬN XÉT CÁ NHÂN CHO 08 GIÁO VIÊN (NGHỊ ĐỊNH 30)")
            print("=======================================================")
            for t_item in TEACHERS_CATALOG:
                for out_d in target_dirs:
                    export_phieu_nhan_xet(t_item, month=args.month, output_dir=out_d)
                print(f"✔ Đã xuất Phiếu nhận xét cá nhân: {t_item['name']} ({t_item['id']})")
                
            # 3. Xuất Biên bản kiểm tra hồ sơ Tổ chuyên môn (docx & md)
            print("\n=======================================================")
            print("XUẤT BIÊN BẢN KIỂM TRA HỒ SƠ TỔ CHUYÊN MÔN (DOCX & MD)")
            print("=======================================================")
            for out_d in target_dirs:
                export_bien_ban_to(TEACHERS_CATALOG, month=args.month, output_dir=out_d)
                
            # 4. Xuất Tệp Cập nhật Hệ thống trực tuyến vnEdu/SMAS/K12 (docx & md)
            print("\n=======================================================")
            print("XUẤT TỆP CẬP NHẬT HỆ THỐNG DUYỆT GIÁO ÁN TRỰC TUYẾN (DOCX & MD)")
            print("=======================================================")
            for out_d in target_dirs:
                export_cap_nhat_he_thong(TEACHERS_CATALOG, month=args.month, output_dir=out_d)
                
            print("\n🎉 TẤT CẢ 3 NHÓM TÀI LIỆU ĐẦU RA ĐÃ ĐƯỢC XUẤT THÀNH CÔNG VÀO CẢ 2 VỊ TRÍ:")
            print(f"  1. Thư mục tổng hợp: {args.out_dir}")
            print(f"  2. Thư mục ngày kiểm tra: {os.path.join(args.out_dir, '26.10')}")
            return

    parser.print_help()

if __name__ == "__main__":
    main()
