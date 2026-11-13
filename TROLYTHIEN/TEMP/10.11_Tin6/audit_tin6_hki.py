# -*- coding: utf-8 -*-
"""
Audit cho các file KHBD Tin học 6 Tuần 13 - 18
"""
import os
import sys
import zipfile
import re

sys.stdout.reconfigure(encoding='utf-8')

DOCX_DIR = "TROLYTHIEN/1_SOAN_KHBD/Ket_qua/10.11/TIN6"

files = [
    "01_KHBD_Tin6_Bai07_TimKiemThongTinTrenInternet_Tiet13-14.docx",
    "02_KHBD_Tin6_Bai08_ThuDienTu_Tiet15-16.docx",
    "03_KHBD_Tin6_OnTapCuoiHK1_Tiet17.docx",
    "04_KHBD_Tin6_KiemTraCuoiHK1_Tiet18.docx",
    "KHBD_Tin6_Ghep_Tuan13-18.docx"
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

    drawings_count = len(re.findall(r'<w:drawing\b', xml_content))
    omml_count = len(re.findall(r'<m:oMath\b', xml_content))
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
        print(f"   Lỗi phantom: {phantom_matches}")

print("-" * 110)
if all_pass:
    print(">>> 100% TỆP KHBD TIN HỌC 6 TUẦN 13 - 18 ĐÃ ĐẠT CHUẨN! <<<")
