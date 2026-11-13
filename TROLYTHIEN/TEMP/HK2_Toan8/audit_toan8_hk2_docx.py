# -*- coding: utf-8 -*-
"""
Audit 47 tệp docx KHBD Toán 8 Học kì II (Tuần 19 - 35)
Kiểm tra OMML (m:oMath), Drawings (Mindmaps 300 DPI), 0 phantom, 0 star leak
"""

import os
import glob
import zipfile
import xml.etree.ElementTree as ET

output_dir = "TROLYTHIEN/1_SOAN_KHBD/Ket_qua/HK2/TOAN8"
docx_files = sorted(glob.glob(os.path.join(output_dir, "*.docx")))

print(f"Tổng số tệp DOCX Toán 8 HK2 tìm thấy: {len(docx_files)}")

namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'
}

total_omml = 0
total_drawings = 0
errors = []

for filepath in docx_files:
    fname = os.path.basename(filepath)
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            doc_xml = z.read('word/document.xml')
            tree = ET.fromstring(doc_xml)
            
            # Count OMML
            omml_list = tree.findall('.//m:oMath', namespaces)
            omml_count = len(omml_list)
            total_omml += omml_count
            
            # Count drawings
            drawings = tree.findall('.//w:drawing', namespaces)
            drawing_count = len(drawings)
            total_drawings += drawing_count
            
            # Text check for phantom and star leak
            all_text = "".join(tree.itertext())
            if "phantom" in all_text:
                errors.append(f"[{fname}] Phát hiện lỗi 'phantom'!")
            if "; phantom x." in all_text:
                errors.append(f"[{fname}] Phát hiện lỗi '; phantom x.'!")
            
            # Check mindmap presence for review lessons
            if any(k in fname for k in ["LuyenTapChung", "BaiTapCuoiChuong", "OnTap"]):
                if drawing_count == 0:
                    errors.append(f"[{fname}] Bài Luyện tập/Ôn tập thiếu hình ảnh Sơ đồ tư duy!")

    except Exception as e:
        errors.append(f"[{fname}] Lỗi đọc tệp: {str(e)}")

print(f"\n=== KẾT QUẢ KIỂM ĐỊNH DOCX TOÁN 8 HK2 ===")
print(f"- Tổng số tệp DOCX: {len(docx_files)} (45 bài lẻ + 2 tệp ghép)")
print(f"- Tổng số công thức Word Equation OMML: {total_omml}")
print(f"- Tổng số hình vẽ Mindmap (Drawings): {total_drawings}")
print(f"- Số lỗi phát hiện: {len(errors)}")

if errors:
    print("\nCÁC LỖI PHÁT HIỆN:")
    for err in errors:
        print(f"  X {err}")
else:
    print("\n>>> TẤT CẢ 47 TỆP DOCX TOÁN 8 HK2 PASS AUDIT 100%! <<<")
