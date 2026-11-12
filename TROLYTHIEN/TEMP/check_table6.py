import docx

doc = docx.Document('TROLYTHIEN/1_SOAN_KHBD/Ket_qua/TOAN9_STEM_Bai15_DoDaiCungTron_DienTichHinhQuatTron.docx')
t6 = doc.tables[6]
print('Table 6 total OMML count:', t6._element.xml.count('<m:oMath'))

for r in range(len(t6.rows)):
    row = t6.rows[r]
    row_xml = row._element.xml
    omml_in_row = row_xml.count('<m:oMath')
    cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
    print(f'Row {r} (OMML: {omml_in_row}): {cells}')
