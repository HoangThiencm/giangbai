# -*- coding: utf-8 -*-
import os
import re
import glob
import docx

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/1_SOAN_KHBD/Ket_qua/10.11/TOAN9"
files = sorted(glob.glob(os.path.join(OUT_DIR, "*.docx")))

print(f"Kiểm tra chất lượng {len(files)} tệp docx Toán 9:")

passed = 0
for fpath in files:
    fname = os.path.basename(fpath)
    doc = docx.Document(fpath)
    
    full_text = []
    for p in doc.paragraphs:
        full_text.append(p.text)
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                full_text.append(c.text)
    
    joined_text = "\n".join(full_text)
    star_matches = re.findall(r"(\*{1,4}[^\*\n\r]{1,40}\*{1,4}|\*{2,4})", joined_text)
    
    xml = doc._body._element.xml
    num_drawings = xml.count("<w:drawing")
    num_omml = xml.count("<m:oMath")
    has_phantom = "phantom" in xml
    
    errors = []
    if star_matches:
        errors.append(f"Có dấu sao thừa (star leaks): {star_matches[:3]}")
    if has_phantom:
        errors.append("Có chứa chữ 'phantom'")
        
    has_mindmap = any(k in fname for k in ["Tiet35", "Tiet36-37", "Tiet38-39", "Hinh_Tiet23", "Hinh_Tiet24-25", "Hinh_Tiet26-27", "Ghep"])
    if has_mindmap and num_drawings == 0:
        errors.append("Bài luyện tập/ôn tập nhưng không tìm thấy hình ảnh sơ đồ tư duy (0 drawing)")
        
    if errors:
        print(f"[FAIL] {fname}: {', '.join(errors)}")
    else:
        passed += 1
        print(f"[PASS] {fname} (drawings: {num_drawings}, OMML math: {num_omml})")

print(f"\nTổng kết chất lượng Docx Toán 9: {passed}/{len(files)} files ĐẠT CHUẨN HOÀN TOÀN!")
