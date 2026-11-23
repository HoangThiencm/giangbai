import docx, os

merged_files = [
    ('Toan 6 So Hoc (Tiet 25-36)', r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TOAN6/KHBD_Toan6_Ghep_SoHoc_Tuan09-12.docx', ['Tiết 25', 'Tiết 26', 'Tiết 27', 'Tiết 29', 'Tiết 30', 'Tiết 32', 'Tiết 35']),
    ('Toan 6 Hinh Hoc (Tiet 09-12)', r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TOAN6/KHBD_Toan6_Ghep_HinhHoc_Tuan09-12.docx', ['Tiết 09', 'Tiết 10', 'Tiết 11', 'Tiết 12']),
    ('Toan 9 Dai So (Tiet 23-32)', r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/KHBD_Toan9_Ghep_DaiSo_Tuan09-12.docx', ['Tiết 23', 'Tiết 25', 'Tiết 26', 'Tiết 27', 'Tiết 29', 'Tiết 30']),
    ('Toan 9 Hinh Hoc (Tiet 11-20)', r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/KHBD_Toan9_Ghep_HinhHoc_Tuan09-12.docx', ['Tiết 11', 'Tiết 13', 'Tiết 14', 'Tiết 15', 'Tiết 17', 'Tiết 18']),
    ('Tin 6 (Tiet 09-12)', r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TIN6/KHBD_Tin6_Ghep_Tuan09-12.docx', ['Tiết 09', 'Tiết 10', 'Tiết 11'])
]

for label, p, keywords in merged_files:
    print('========================================')
    print(f'AUDIT: {label}')
    doc = docx.Document(p)
    full_text = ' '.join([para.text for para in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])
    sz = os.path.getsize(p)
    print(f'  Size: {sz:,} bytes')
    
    # Check all required lesson tokens
    for kw in keywords:
        found = kw in full_text
        print(f'  -> Check "{kw}": {"PASS" if found else "MISSING"}')
