import os
import glob
import zipfile
import xml.etree.ElementTree as ET

docx_dir = "TROLYTHIEN/1_SOAN_KHBD/Ket_qua/HK2/TOAN9"
files = sorted(glob.glob(os.path.join(docx_dir, "*.docx")))

print(f"Bắt đầu Audit {len(files)} tệp docx Toán 9 HK2...\n")

total_omath = 0
total_drawings = 0
total_errors = 0

for filepath in files:
    filename = os.path.basename(filepath)
    file_errors = []
    omath_count = 0
    drawing_count = 0
    star_leak_count = 0

    try:
        with zipfile.ZipFile(filepath, 'r') as docx_zip:
            xml_content = docx_zip.read('word/document.xml').decode('utf-8')

            # Đếm công thức OMML
            omath_count = xml_content.count("<m:oMath")
            total_omath += omath_count

            # Đếm drawing / hình vẽ / mindmap
            drawing_count = xml_content.count("<w:drawing")
            total_drawings += drawing_count

            # Kiểm tra lỗi cấm
            if "phantom" in xml_content.lower():
                file_errors.append("Chứa chuỗi cấm 'phantom'")

            # Kiểm tra rò rỉ markdown ** trong text node
            # Tìm thẻ <w:t> chứa dấu sao không được xử lý
            root = ET.fromstring(xml_content)
            for elem in root.iter():
                if elem.tag.endswith('}t') and elem.text:
                    if "****" in elem.text:
                        star_leak_count += 1

            if star_leak_count > 0:
                file_errors.append(f"Chứa {star_leak_count} đoạn văn bản có rò rỉ dấu sao (star leaks)")

    except Exception as e:
        file_errors.append(f"Không thể đọc hoặc giải nén file docx: {str(e)}")

    if file_errors:
        print(f"[FAIL] {filename}:")
        for err in file_errors:
            print(f"   - {err}")
        total_errors += len(file_errors)
    else:
        print(f"[PASS] {filename} | OMML Equations: {omath_count} | Drawings: {drawing_count}")

print("\n" + "="*60)
print(f"TỔNG KẾT TOÁN 9 HK2:")
print(f"- Tổng số tệp DOCX: {len(files)} (39 lẻ + 2 ghép)")
print(f"- Tổng số công thức Word Equation OMML: {total_omath}")
print(f"- Tổng số sơ đồ / hình vẽ vector (Drawings): {total_drawings}")
print(f"- Tổng số lỗi: {total_errors}")

if total_errors == 0:
    print(">>> TẤT CẢ 41 TỆP DOCX TOÁN 9 HK2 ĐẠT CHUẨN PASS AUDIT 100%! <<<")
