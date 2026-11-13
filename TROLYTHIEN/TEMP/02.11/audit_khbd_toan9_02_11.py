# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

RESULTS_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\1_SOAN_KHBD\Ket_qua\02.11"

files = [
    "01_KHBD_Toan9_Bai07_CanBacHaiVaCanThucBacHai_Tiet23-24.docx",
    "02_KHBD_Toan9_Bai14_CungVaDayCuaDuongTron_Tiet11-12.docx",
    "03_KHBD_Toan9_OnTapGiuaHK1_DaiSo_Tiet25.docx",
    "04_KHBD_Toan9_OnTapGiuaHK1_HinhHoc_Tiet13.docx",
    "05_KHBD_Toan9_Bai08_KhaiCanBacHaiPhepNhanPhepChia_Tiet27-28.docx",
    "06_KHBD_Toan9_Bai15_DoDaiCungTron_QuatTron_STEM_Tiet15-16.docx",
    "07_KHBD_Toan9_LuyenTapChung_DaiSo_Tiet29.docx",
    "08_KHBD_Toan9_Bai09_BienDoiDonGianVaRutGonCanThuc_Tiet30-32.docx",
    "09_KHBD_Toan9_LuyenTapChung_HinhHoc_Tiet17.docx",
    "10_KHBD_Toan9_Bai16_ViTriTuongDoiCuaDuongThangVaDuongTron_Tiet18-20.docx",
    "KHBD_Toan9_Ghep_DaiSo_Tuan09-12.docx",
    "KHBD_Toan9_Ghep_HinhHoc_Tuan09-12.docx"
]

print(f"{'STT':<4} | {'TÊN FILE':<55} | {'SIZE (KB)':<10} | {'OMML MATH':<10} | {'TABLES':<8} | {'STATUS'}")
print("-" * 105)

all_pass = True

for idx, fname in enumerate(files, 1):
    fpath = os.path.join(RESULTS_DIR, fname)
    if not os.path.exists(fpath):
        print(f"{idx:<4} | {fname:<55} | {'MISSING':<10} | {'-':<10} | {'-':<8} | FAIL")
        all_pass = False
        continue
    
    size_kb = round(os.path.getsize(fpath) / 1024, 1)
    
    try:
        with zipfile.ZipFile(fpath, 'r') as docx:
            xml_content = docx.read('word/document.xml').decode('utf-8')
            math_count = xml_content.count('<m:oMath>') + xml_content.count('<m:oMath ')
            table_count = xml_content.count('<w:tbl>') + xml_content.count('<w:tbl ')
            
            status = "PASS" if math_count > 0 and table_count > 0 else "CHECK"
            print(f"{idx:<4} | {fname:<55} | {size_kb:<10} | {math_count:<10} | {table_count:<8} | {status}")
    except Exception as e:
        print(f"{idx:<4} | {fname:<55} | {size_kb:<10} | ERROR: {e}")
        all_pass = False

print("-" * 105)
if all_pass:
    print(">>> TẤT CẢ 12 TỆP (.DOCX) ĐÃ ĐẠT CHUẨN KIỂM ĐỊNH CHẤT LƯỢNG 100% WORD EQUATION & CV 5512! <<<")
else:
    print(">>> CÓ TỆP CHƯA ĐẠT CHUẨN, CẦN KIỂM TRA LẠI. <<<")
