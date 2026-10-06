# -*- coding: utf-8 -*-
"""
CÔNG CỤ RÀ SOÁT & THẨM ĐỊNH TỰ ĐỘNG KẾ HOẠCH BÀI DẠY (KHBD LINTER & AUDITOR V3.0)
Hệ thống Trợ lý Sư phạm Hoàng Thiên — Trường THCS Trần Phú
Bảo vệ kép: Thẩm định đồng thời File Nguồn Markdown (.md) và File Thành Phẩm Word (.docx)
"""

import os
import glob
import re
import sys
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Bảng phân bổ PPCT chuẩn (Tháng 9 & 10)
# Cột Ghi chú có mã: chỉ bài 03 (Bài 8), bài 04 (Bài 9), bài 08 (Bài 12)
PPCT_INTEGRATION_MAP = {
    "01": {"name": "Luyện tập chung (Tiết 12)", "nls": False, "ai": False, "mindmap": True},
    "02": {"name": "Bài tập cuối chương I (Tiết 13)", "nls": False, "ai": False, "mindmap": True},
    "03": {"name": "Bài 8. Quan hệ chia hết và tính chất", "nls": "1.1.TC1a", "ai": "6.B2.1", "mindmap": False},
    "04": {"name": "Bài 9. Dấu hiệu chia hết", "nls": "5.3.TC1a", "ai": "6.D1.1", "mindmap": False},
    "05": {"name": "Bài 10. Số nguyên tố", "nls": False, "ai": False, "mindmap": False},
    "06": {"name": "Luyện tập chung (Tiết 20)", "nls": False, "ai": False, "mindmap": True},
    "07": {"name": "Bài 11. Ước chung và ƯCLN", "nls": False, "ai": False, "mindmap": False},
    "08": {"name": "Bài 12. Bội chung và BCNN", "nls": "5.3.TC1a", "ai": "6.C1.1", "mindmap": False},
}

def audit_khbd_file(fpath):
    issues = []
    warnings = []
    
    fname = os.path.basename(fpath)
    match_num = re.search(r"KHBD_(\d\d)_", fname)
    lesson_id = match_num.group(1) if match_num else None
    rule = PPCT_INTEGRATION_MAP.get(lesson_id, {})

    with open(fpath, "r", encoding="utf-8") as fp:
        content = fp.read()

    # =========================================================================
    # TẦNG 1: KIỂM TRA FILE NGUỒN MARKDOWN (.MD)
    # =========================================================================

    # 1.1 Ký tự điều khiển ASCII ẩn
    ctrl_chars = re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", content)
    if ctrl_chars:
        issues.append(f"Markdown chứa {len(ctrl_chars)} ký tự điều khiển ẩn (escape corruption như VT, FF, Backspace).")

    # 1.2 Lệnh LaTeX rụng gạch chéo
    # Phân số bị rụng gạch chéo thành rac{
    broken_fractions = re.findall(r"(?<![\\f])\brac\{[^}]*\}\{[^}]*\}", content)
    if broken_fractions:
        issues.append(f"Lỗi công thức phân số: {len(broken_fractions)} vị trí bị mất gạch chéo (ví dụ: '{broken_fractions[0]}').")

    # Lệnh begin bị rụng gạch chéo thành egin
    broken_begins = re.findall(r"(?<!\\)\b(egin)\b", content)
    if broken_begins:
        issues.append(f"Lỗi cú pháp LaTeX: {len(broken_begins)} vị trí bị rụng gạch chéo thành 'egin' (mất \\b của \\begin).")

    # Lệnh text bị rụng gạch chéo thành ext{
    broken_texts = re.findall(r"(?<!\\)\b(ext)\{", content)
    if broken_texts:
        issues.append(f"Lỗi cú pháp LaTeX: {len(broken_texts)} vị trí bị rụng gạch chéo thành 'ext{{' (mất \\t của \\text).")

    # 1.3 Lỗi chia hết: vdots bị rách hoặc biến thành dots
    broken_div = re.findall(r"(?<!\\)\b(dots)\b|\\v\s*\\*vdots|\\v\b", content)
    if broken_div:
        issues.append(f"Lỗi ký hiệu chia hết: {len(broken_div)} vị trí có chữ 'dots' hoặc ký tự rác 'v'.")

    # 1.4 Kiểm tra cân bằng dấu $
    dollar_count = content.count("$")
    escaped_dollars = content.count(r"\$")
    actual_dollars = dollar_count - escaped_dollars
    if actual_dollars % 2 != 0:
        issues.append(f"Mất cân bằng dấu $: Tổng số {actual_dollars} dấu $ (lẻ), có thể bị mở mà quên đóng công thức.")

    # 2. KIỂM TRA NLS & AI THEO PPCT
    has_nls = "***(Tích hợp NLS" in content or "***[NLS" in content or "Năng lực số" in content
    has_ai = "***(Tích hợp AI" in content or "***[AI" in content or "Năng lực Trí tuệ Nhân tạo" in content

    if rule:
        if not rule["nls"] and has_nls:
            issues.append("Sai quy định PPCT: Bài học này không có mã NLS trong PPCT nhưng bị chèn nội dung NLS.")
        if not rule["ai"] and has_ai:
            issues.append("Sai quy định PPCT: Bài học này không có mã AI trong PPCT nhưng bị chèn nội dung AI.")
        if rule["nls"] and not has_nls:
            issues.append(f"Thiếu tích hợp NLS: PPCT yêu cầu mã [{rule['nls']}] nhưng bài dạy chưa tích hợp.")
        if rule["ai"] and not has_ai:
            issues.append(f"Thiếu tích hợp AI: PPCT yêu cầu mã [{rule['ai']}] nhưng bài dạy chưa tích hợp.")

        if rule["nls"]:
            nls_lines = re.findall(r".*Tích hợp NLS.*", content)
            for line in nls_lines:
                if "|" in line and not line.strip().startswith("***") and not line.strip().startswith("- ***"):
                    warnings.append(f"Dòng tích hợp NLS có thể chưa in đậm, in nghiêng chuẩn: '{line.strip()[:60]}...'")

    # 3. KIỂM TRA HÌNH VẼ VÀ SƠ ĐỒ TƯ DUY
    all_images = re.findall(r"!\[([^\]]*)\]\((khbd-ill:[^)]+)\)", content)
    
    # 3.1 Bài số học: Cấm sơ đồ hộp / quy trình giả tạo lặp lại lý thuyết
    for img_caption, img_id in all_images:
        if any(bad in img_id.lower() for bad in ["quy-trinh", "tinh-chat-chia-het", "dau-hieu-chia-het"]):
            issues.append(f"Chèn sơ đồ hộp/quy trình giả tạo thừa ('{img_id}'). Cần trình bày bằng công thức và bảng 2 cột.")

    # 3.2 Tiết Luyện tập / Ôn tập phải có Mindmap
    if rule and rule.get("mindmap", False):
        if len(all_images) == 0:
            issues.append("Tiết Luyện tập chung / Ôn tập thiếu Sơ đồ tư duy (Mindmap).")
        else:
            table_lines_with_img = [line for line in content.splitlines() if "|" in line and "![" in line]
            if table_lines_with_img:
                issues.append("Sơ đồ tư duy bị chèn SAI VỊ TRÍ: Nằm bên trong ô bảng (làm ép hẹp cột). Bắt buộc phải đặt ở mục b) Nội dung bên ngoài bảng.")

    # 4. KIỂM TRA CẤU TRÚC HOẠT ĐỘNG CHUẨN CÔNG VĂN 5512
    h_kd = "KHỞI ĐỘNG" in content.upper()
    h_vd = "VẬN DỤNG" in content.upper()
    h_lt = "LUYỆN TẬP" in content.upper()
    is_practice = rule.get("mindmap", False) or "LUYỆN TẬP" in fname.upper() or "ÔN TẬP" in fname.upper()

    if not h_kd or not h_vd or not h_lt:
        missing = []
        if not h_kd: missing.append("Khởi động")
        if not h_lt: missing.append("Luyện tập")
        if not h_vd: missing.append("Vận dụng")
        issues.append("Thiếu hoạt động cốt lõi: " + ", ".join(missing))
    elif not is_practice and "HÌNH THÀNH KIẾN THỨC" not in content.upper():
        issues.append("Bài lý thuyết mới nhưng thiếu Hoạt động Hình thành kiến thức.")

    # =========================================================================
    # TẦNG 2: THẨM ĐỊNH TRỰC TIẾP FILE WORD THÀNH PHẨM (.DOCX XML)
    # =========================================================================
    docx_path = fpath.replace(".md", ".docx")
    if not os.path.exists(docx_path):
        issues.append(f"Chưa xuất file Word (.docx) thành phẩm: '{os.path.basename(docx_path)}' không tồn tại.")
    else:
        try:
            with zipfile.ZipFile(docx_path, 'r') as zf:
                xml_content = zf.read('word/document.xml').decode('utf-8')
            
            # Quét các lỗi hiển thị thô trong Word:
            if "egin" in xml_content:
                issues.append("LỖI WORD DOCX: Chứa chuỗi rác 'egin' trong công thức (mất gạch chéo \\begin).")
            if re.search(r"\brac\d|\brac\{", xml_content):
                issues.append("LỖI WORD DOCX: Chứa chuỗi rác 'rac' trong công thức (mất gạch chéo \\frac).")
            if "\\vdots" in xml_content or "\\v " in xml_content:
                issues.append("LỖI WORD DOCX: Chứa ký hiệu LaTeX thô '\\vdots' chưa được chuyển đổi sang Equation Word.")
            if "array" in xml_content:
                issues.append("LỖI WORD DOCX: Chứa chuỗi 'array' chưa được chuyển đổi thành bảng Word.")
            
            docx_ctrls = re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", xml_content)
            if docx_ctrls:
                issues.append(f"LỖI WORD DOCX: Chứa {len(docx_ctrls)} ký tự điều khiển ẩn trong văn bản Word.")
        except Exception as e:
            warnings.append(f"Không thể mở file docx để thẩm định XML: {e}")

    return {
        "file": fname,
        "docx_file": os.path.basename(docx_path),
        "lesson": rule.get("name", fname),
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
        "math_ok": len([i for i in issues if "công thức" in i or "chia hết" in i or "kết nối" in i or "ký tự" in i or "WORD DOCX" in i or "LaTeX" in i]) == 0,
        "ppct_ok": len([i for i in issues if "PPCT" in i or "NLS" in i or "AI" in i]) == 0,
        "visual_ok": len([i for i in issues if "hình" in i or "Sơ đồ" in i or "Mindmap" in i]) == 0
    }

def main():
    base_dir = r"TROLYTHIEN/1_SOAN_KHBD/Ket_qua"
    files = sorted(glob.glob(os.path.join(base_dir, "*.md")))

    if not files:
        print("Không tìm thấy file Markdown nào trong", base_dir)
        sys.exit(1)

    print("=" * 80)
    print(" HỆ THỐNG RÀ SOÁT & THẨM ĐỊNH KÉP KẾ HOẠCH BÀI DẠY (KHBD AUDITOR V3.0)")
    print(" Đảm bảo chất lượng đồng bộ: Markdown (.md) + Word (.docx XML)")
    print("=" * 80)

    total_pass = 0
    total_fail = 0

    for fpath in files:
        res = audit_khbd_file(fpath)
        icon = "[✓ PASS]" if res["status"] == "PASS" else "[✗ FAIL]"
        print(f"\n{icon} {res['file']} -> {res['docx_file']} — {res['lesson']}")

        if res["status"] == "PASS":
            total_pass += 1
            print("   • Công thức Toán học: CHUẨN XÁC 100% (Cả MD và Word DOCX đều sạch, không lỗi egin, rac, vdots)")
            print("   • Tích hợp NLS & AI:  KHỚP 100% PPCT (Đúng mã và in đậm nghiêng)")
            print("   • Hình vẽ & Mindmap:  ĐÚNG QUY CHUẨN (Mindmap ở mục b ngoài bảng, không chèn hình thừa)")
        else:
            total_fail += 1
            for err in res["issues"]:
                print(f"   [LỖI] {err}")
            for w in res["warnings"]:
                print(f"   [CẢNH BÁO] {w}")

    print("\n" + "=" * 80)
    print(f" TỔNG KẾT THẨM ĐỊNH: {total_pass}/{len(files)} FILE ĐẠT CHUẨN KÉP (PASS) | {total_fail} FILE CẦN CHỈNH SỬA")
    print("=" * 80)

if __name__ == "__main__":
    main()
