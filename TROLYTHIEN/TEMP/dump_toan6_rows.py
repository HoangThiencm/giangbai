import docx

doc = docx.Document('TROLYTHIEN/1_SOAN_KHBD/Dau_vao/PL3_TOAN6_HOANGTANTHIEN.docx')
t = doc.tables[2]
with open('TROLYTHIEN/TEMP/toan6_all_hk2_rows.txt', 'w', encoding='utf-8') as f:
    for i in range(55, len(t.rows)):
        row = t.rows[i]
        vals = [c.text.strip().replace('\n', ' ') for c in row.cells]
        stt = vals[0] if len(vals) > 0 else ''
        bai = vals[1] if len(vals) > 1 else ''
        sotiet = vals[2] if len(vals) > 2 else ''
        tietct = vals[3] if len(vals) > 3 else ''
        tuan = vals[4] if len(vals) > 4 else ''
        note = vals[7] if len(vals) > 7 else ''
        f.write(f'Row {i}: STT={stt} | Bai={bai} | SoTiet={sotiet} | TietCT={tietct} | Tuan={tuan} | Note={note}\n')
print('Done dumping all rows.')
