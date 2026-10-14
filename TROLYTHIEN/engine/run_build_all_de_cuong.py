# -*- coding: utf-8 -*-
"""
Script điều phối tạo trọn bộ 3 Đề cương ôn tập Giữa học kỳ 1 (Toán 6, 8, 9)
TÍCH HỢP VÒNG PHẢN BIỆN & HẬU KIỂM TỰ ĐỘNG (AUTO-AUDITOR & SELF-CORRECTION)
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(__file__))

from builder_de_cuong_toan6 import build_de_cuong_toan_6
from builder_de_cuong_toan7 import build_de_cuong_toan_7
from builder_de_cuong_toan8 import build_de_cuong_toan_8
from builder_de_cuong_toan9 import build_de_cuong_toan_9
from de_cuong_docx_auditor import audit_and_fix_document

import datetime

TODAY_FOLDER = datetime.datetime.now().strftime("%d.%m")
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "2_TAO_BAI_TAP", "Ket_qua", TODAY_FOLDER))

def run_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=================================================================")
    print(f"KHỞI TẠO ĐỀ CƯƠNG ÔN TẬP GIỮA HỌC KỲ I (TOÁN 6, 7, 8, 9) - THƯ MỤC: {TODAY_FOLDER}")
    print("NĂM HỌC 2026 - 2027 | TRƯỜNG THCS TRẦN PHÚ | TỔ: TOÁN - TIN")
    print("=================================================================\n")
    
    files = [
        ("Toán 6", os.path.join(OUTPUT_DIR, "De_Cuong_On_Tap_Giua_HK1_Toan_6.docx"), build_de_cuong_toan_6),
        ("Toán 7", os.path.join(OUTPUT_DIR, "De_Cuong_On_Tap_Giua_HK1_Toan_7.docx"), build_de_cuong_toan_7),
        ("Toán 8", os.path.join(OUTPUT_DIR, "De_Cuong_On_Tap_Giua_HK1_Toan_8.docx"), build_de_cuong_toan_8),
        ("Toán 9", os.path.join(OUTPUT_DIR, "De_Cuong_On_Tap_Giua_HK1_Toan_9.docx"), build_de_cuong_toan_9)
    ]
    
    audit_reports = []
    
    for idx, (label, fpath, builder_func) in enumerate(files, 1):
        print(f"[{idx}/4] Đang biên soạn Đề cương {label}...")
        builder_func(fpath)
        
        # VÒNG TỰ ĐỘNG PHẢN BIỆN & RÀ SOÁT CHẤT LƯỢNG (AUTO-AUDIT)
        print(f"      -> Chạy vòng phản biện tự động rà soát chất lượng {label}...")
        ok, report = audit_and_fix_document(fpath)
        audit_reports.append((label, fpath, report))
        
    print("\n" + "="*65)
    print("BẢNG BÁO CÁO PHẢN BIỆN & KIỂM ĐỊNH CHẤT LƯỢNG TỰ ĐỘNG (QUALITY AUDIT):")
    print("="*65)
    
    for label, fpath, report in audit_reports:
        print(f"📘 MÔN: {label.upper()} ({os.path.basename(fpath)})")
        print(f"   • Dung lượng file: {os.path.getsize(fpath):,} bytes")
        print(f"   • Số đoạn văn: {report.get('paragraphs', 0)}")
        print(f"   • Số công thức Word Equation chuẩn (OMML): {report.get('omath_count', 0)}")
        print(f"   • Vòng 1 (Phản biện Toán học & Số liệu): {report.get('round_1_math_logic', 'PASS')}")
        print(f"   • Vòng 2 (Phản biện Cấu trúc XML & Equation): {report.get('round_2_xml_omml', 'PASS')} (Sửa: {report.get('fixed_issues', 0)} lỗi, Ô rỗng: {report.get('empty_placeholders', 0)})")
        print(f"   • Vòng 3 (Cấp chứng nhận chất lượng): {report.get('status', 'OK')}")
        if report.get('unresolved_errors'):
            for err in report['unresolved_errors'][:3]:
                print(f"     ⚠️ {err}")
        print("-" * 65)
        
    print("\nHOÀN TẤT XUẤT TRỌN BỘ 4 KHỐI LỚP (TOÁN 6, 7, 8, 9) TẠI THƯ MỤC:")
    print(OUTPUT_DIR)
    print("="*65)

if __name__ == "__main__":
    run_all()
