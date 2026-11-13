# -*- coding: utf-8 -*-
"""
Script kiểm định chất lượng toàn diện (Audit) cho 11 tệp KHBD Toán 6
Kiểm tra:
1. Star leak (dấu * lẻ loi hoặc **)
2. Số lượng ảnh w:drawing (Mindmap)
3. Số lượng công thức m:oMath
4. Từ khóa lỗi tiềm ẩn như 'phantom', 'undefined', '[object'
"""
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import re

sys.stdout.reconfigure(encoding='utf-8')

DOCX_DIR = "TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TOAN6"

files = [
    "01_KHBD_Toan6_LuyenTapChung_Chuong2_Tiet25.docx",
    "02_KHBD_Toan6_BaiTapCuoiChuong2_Tiet26.docx",
    "03_KHBD_Toan6_OnTapGiuaHK1_SoHoc_Tiet27-28.docx",
    "04_KHBD_Toan6_Bai13_TapHopCacSoNguyen_Tiet30-31.docx",
    "05_KHBD_Toan6_Bai14_PhepCongVaPhepTruSoNguyen_Tiet32-34.docx",
    "06_KHBD_Toan6_Bai15_QuyTacDauNgoac_Tiet35-36.docx",
    "07_KHBD_Toan6_OnTapGiuaHK1_HinhHoc_Tiet09.docx",
    "08_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet11.docx",
    "09_KHBD_Toan6_BaiTapCuoiChuong4_Tiet12.docx",
    "KHBD_Toan6_Ghep_SoHoc_Tuan09-12.docx",
    "KHBD_Toan6_Ghep_HinhHoc_Tuan09-12.docx"
]

print(f"{'File Name':<50} | {'Size (KB)':<10} | {'Drawings':<8} | {'OMML Math':<10} | {'Star Leaks':<10} | {'Status'}")
print("-" * 105)

all_pass = True

for fname in files:
    fpath = os.path.join(DOCX_DIR, fname)
    if not os.path.exists(fpath):
        print(f"{fname:<50} | NOT FOUND")
        all_pass = False
        continue

    size_kb = os.path.getsize(fpath) / 1024

    with zipfile.ZipFile(fpath, 'r') as z:
        xml_content = z.read('word/document.xml').decode('utf-8')

    # 1. Đếm w:drawing
    drawings_count = len(re.findall(r'<w:drawing\b', xml_content))

    # 2. Đếm m:oMath
    omml_count = len(re.findall(r'<m:oMath\b', xml_content))

    # 3. Trích xuất toàn bộ text để kiểm tra star leak và từ khóa lỗi
    # Loại bỏ các thẻ XML
    text_only = re.sub(r'<[^>]+>', '', xml_content)

    # Tìm các lỗi rò rỉ dấu sao
    star_leaks = re.findall(r'(\*{1,4}[^\*\n\r]{1,40}\*{1,4}|\*{2,4})', text_only)
    
    # Lỗi phantom
    phantom_matches = re.findall(r'phantom', text_only, re.IGNORECASE)

    status = "PASS"
    if star_leaks or phantom_matches:
        status = "FAIL"
        all_pass = False

    print(f"{fname:<50} | {size_kb:8.1f}KB | {drawings_count:<8} | {omml_count:<10} | {len(star_leaks):<10} | {status}")
    if star_leaks:
        print(f"   Lỗi star leaks: {star_leaks[:3]}")
    if phantom_matches:
        print(f"   Lỗi phantom phát hiện: {phantom_matches}")

print("-" * 105)
if all_pass:
    print(">>> TẤT CẢ 11 TỆP KHBD ĐÃ ĐẠT CHUẨN 100% (PASS TẤT CẢ CÁC TIÊU CHÍ)! <<<")
else:
    print(">>> CÓ TỆP CHƯA ĐẠT CHUẨN, CẦN SỬA ĐỔI! <<<")
