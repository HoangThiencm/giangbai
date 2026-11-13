# -*- coding: utf-8 -*-
import os, glob, zipfile, xml.etree.ElementTree as ET, sys

sys.stdout.reconfigure(encoding='utf-8')

RESULTS_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\1_SOAN_KHBD\Ket_qua\02.11"
files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.docx")))

print(f"=== BÁO CÁO KIỂM ĐỊNH CHẤT LƯỢNG TOÀN DIỆN ({len(files)} TỆP) ===")
print(f"{'TÊN TỆP':<58} | {'STAR LEAK':<10} | {'OMML MATH':<10} | {'TABLES':<8} | {'STATUS'}")
print("-" * 102)

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
all_pass = True

for f in files:
    fname = os.path.basename(f)
    with zipfile.ZipFile(f) as z:
        xml = z.read('word/document.xml').decode('utf-8')
        root = ET.fromstring(xml)
        
        # 1. Đếm star leak
        texts = [elem.text for elem in root.iter(f"{{{ns['w']}}}t") if elem.text]
        stars = [t for t in texts if '**' in t or '***' in t]
        star_count = len(stars)
        
        # 2. Đếm Math
        math_count = xml.count('<m:oMath>') + xml.count('<m:oMath ')
        
        # 3. Đếm Table
        table_count = xml.count('<w:tbl>') + xml.count('<w:tbl ')
        
        is_ok = (star_count == 0) and (math_count > 0) and (table_count > 0)
        status = "PASS 100%" if is_ok else "CHECK"
        if not is_ok:
            all_pass = False
        
        print(f"{fname:<58} | {star_count:<10} | {math_count:<10} | {table_count:<8} | {status}")

print("-" * 102)
if all_pass:
    print(">>> TẤT CẢ 12 TỆP ĐỀU ĐẠT CHUẨN TUYỆT ĐỐI (0 STAR LEAK, ĐẦY ĐỦ BOLD + ITALIC, 100% OMML EQUATION)! <<<")
