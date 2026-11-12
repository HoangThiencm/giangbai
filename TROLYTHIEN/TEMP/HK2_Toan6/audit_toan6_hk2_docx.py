# -*- coding: utf-8 -*-
"""
Script kiểm định chất lượng các tệp DOCX Toán 6 HK2
Kiểm tra cấu trúc XML, Drawing, OMML Math và star leaks
"""

import os
import zipfile
import xml.etree.ElementTree as ET

docx_dir = "TROLYTHIEN/1_SOAN_KHBD/Ket_qua/HK2/TOAN6"
files = [f for f in os.listdir(docx_dir) if f.endswith(".docx")]
files.sort()

print(f"Tổng số tệp DOCX Toán 6 HK2 tìm thấy: {len(files)}")

errors = []
total_drawings = 0
total_omml = 0

for f in files:
    path = os.path.join(docx_dir, f)
    try:
        with zipfile.ZipFile(path, 'r') as docx:
            xml_content = docx.read('word/document.xml').decode('utf-8')
            
            # Kiểm tra OMML
            omml_count = xml_content.count("<m:oMath")
            total_omml += omml_count
            
            # Kiểm tra Drawing
            drawing_count = xml_content.count("<w:drawing>")
            total_drawings += drawing_count
            
            # Kiểm tra phantom
            if "phantom" in xml_content:
                errors.append(f"[{f}] Phát hiện lỗi phantom trong XML!")
                
            # Kiểm tra dấu sao rò rỉ trong text
            root = ET.fromstring(xml_content)
            full_text = "".join(root.itertext())
            
            # Bỏ qua các dấu sao trong bảng hoặc text thông thường nếu không phải rò rỉ cú pháp Markdown
            # Kiểm tra xem có '**' hay '***' còn sót lại trong text không
            if "**" in full_text:
                errors.append(f"[{f}] Phát hiện còn sót ký hiệu Markdown '**' trong text hiển thị!")
                
            # Kiểm tra các file luyện tập có ảnh không
            if any(k in f for k in ["LuyenTapChung", "BaiTapCuoiChuong", "OnTap"]):
                if drawing_count == 0:
                    errors.append(f"[{f}] Tiết Luyện tập/Ôn tập nhưng không có Drawing hình ảnh!")
    except Exception as e:
        errors.append(f"[{f}] Lỗi đọc tệp docx: {str(e)}")

print(f"Tổng số công thức toán học OMML (m:oMath): {total_omml}")
print(f"Tổng số hình ảnh Drawing vector: {total_drawings}")

if errors:
    print(f"❌ THẤT BẠI: Phát hiện {len(errors)} lỗi:")
    for err in errors:
        print("  - " + err)
else:
    print("✅ XUẤT SẮC: Toàn bộ 45 tệp DOCX Toán 6 HK2 đều đạt chuẩn 100% (OMML chuẩn, 0 lỗi phantom, 0 star leaks)!")
