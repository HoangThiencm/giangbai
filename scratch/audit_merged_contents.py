import docx, os

check_list = [
    (r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TIN6/KHBD_Tin6_Ghep_Tuan09-12.docx', 'Tin 6 Ghep', ['Tiết 10', 'Câu 29', 'Câu 30', '1 024']),
    (r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TOAN6/KHBD_Toan6_Ghep_SoHoc_Tuan09-12.docx', 'Toan 6 So Hoc Ghep', ['Tiết 29', 'Bài 1', 'Bài 5', '9 380 000']),
    (r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TOAN6/KHBD_Toan6_Ghep_HinhHoc_Tuan09-12.docx', 'Toan 6 Hinh Hoc Ghep', ['Tiết 09', 'Tiết 11', 'Tiết 12']),
    (r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/KHBD_Toan9_Ghep_DaiSo_Tuan09-12.docx', 'Toan 9 Dai So Ghep', ['Tiết 26', 'Bài 1', 'Bài 4', 'bánh mì']),
    (r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/KHBD_Toan9_Ghep_HinhHoc_Tuan09-12.docx', 'Toan 9 Hinh Hoc Ghep', ['Tiết 11, 12', 'Tiết 13', 'Tiết 15, 16', 'STEM'])
]

for path, label, keywords in check_list:
    doc = docx.Document(path)
    full_text = ' '.join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])
    print(f'=== {label} ({os.path.basename(path)}) ===')
    for kw in keywords:
        found = kw in full_text
        print(f'  Contains "{kw}": {found}')
