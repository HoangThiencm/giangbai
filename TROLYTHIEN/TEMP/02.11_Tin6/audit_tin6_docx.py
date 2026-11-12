# -*- coding: utf-8 -*-
"""
Script kiểm định chất lượng toàn diện (Audit) cho 4 tệp KHBD Tin học 6
"""
import os
import sys
import zipfile
import re

sys.stdout.reconfigure(encoding='utf-8')

DOCX_DIR = "TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TIN6"

files = [
    "01_KHBD_Tin6_OnTapGiuaHK1_Tiet09.docx",
    "02_KHBD_Tin6_KiemTraGiuaHK1_Tiet10.docx",
    "03_KHBD_Tin6_Bai06_MangThongTinToanCau_Tiet11-12.docx",
    "KHBD_Tin6_Ghep_Tuan09-12.docx"
]

print(f"{'File Name':<55} | {'Size (KB)':<10} | {'Drawings':<8} | {'OMML Math':<10} | {'Star Leaks':<10} | {'Status'}")
print("-" * 110)

all_pass = True

for fname in files:
    fpath = os.path.join(DOCX_DIR, fname)
    if not os.path.exists(fpath):
        print(f"{fname:<55} | NOT FOUND")
        all_pass = False
        continue

    size_kb = os.path.getsize(fpath) / 1024

    with zipfile.ZipFile(fpath, 'r') as z:
        xml_content = z.read('word/document.xml').decode('utf-8')

    # 1. Đếm w:drawing
    drawings_count = len(re.findall(r'<w:drawing\b', xml_content))

    # 2. Đếm m:oMath
    omml_count = len(re.findall(r'<m:oMath\b', xml_content))

    # 3. Trích xuất text để kiểm tra rò rỉ dấu sao
    text_only = re.sub(r'<[^>]+>', '', xml_content)
    star_leaks = re.findall(r'(\*{1,4}[^\*\n\r]{1,40}\*{1,4}|\*{2,4})', text_only)
    phantom_matches = re.findall(r'phantom', text_only, re.IGNORECASE)

    status = "PASS"
    if star_leaks or phantom_matches:
        status = "FAIL"
        all_pass = False

    print(f"{fname:<55} | {size_kb:8.1f}KB | {drawings_count:<8} | {omml_count:<10} | {len(star_leaks):<10} | {status}")
    if star_leaks:
        print(f"   Lỗi star leaks: {star_leaks[:3]}")
    if phantom_matches:
        print(f"   Lỗi phantom phát hiện: {phantom_matches}")

print("-" * 110)
if all_pass:
    print(">>> TẤT CẢ 4 TỆP KHBD TIN HỌC 6 ĐÃ ĐẠT CHUẨN 100% (PASS TẤT CẢ CÁC TIÊU CHÍ)! <<<")
else:
    print(">>> CÓ TỆP CHƯA ĐẠT CHUẨN, CẦN SỬA ĐỔI! <<<")
