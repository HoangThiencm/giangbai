import docx, zipfile, os, re

files = [
    r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TIN6/02_KiemTraGiuaHK1_Tin6_Tiet10.docx',
    r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/TOAN6/04_KHBD_Toan6_KiemTraGiuaHK1_Tiet29.docx',
    r'TROLYTHIEN/1_SOAN_KHBD/Ket_qua/02.11/04b_KHBD_Toan9_KiemTraGiuaHK1_Tiet26.docx'
]

for p in files:
    print('==============================================')
    print('AUDITING:', os.path.basename(p))
    if not os.path.exists(p):
        print('  File NOT found!')
        continue
    
    size = os.path.getsize(p)
    print(f'  Size: {size:,} bytes')
    
    with zipfile.ZipFile(p, 'r') as z:
        xml = z.read('word/document.xml').decode('utf-8', errors='ignore')
        
        omml_count = xml.count('<m:oMath>') + xml.count('<m:oMath ')
        print(f'  Word Equation (m:oMath) count: {omml_count}')
        
        media = [f for f in z.namelist() if f.startswith('word/media/')]
        print(f'  Embedded images count: {len(media)} ({media})')
        
        doc = docx.Document(p)
        raw_text = '\n'.join([para.text for para in doc.paragraphs] + [cell.text for tbl in doc.tables for r in tbl.rows for cell in r.cells])
        
        star_leaks = re.findall(r'\*{2,3}[^*]+\*{2,3}', raw_text)
        straight_quotes = raw_text.count('"')
        admin_quotes = raw_text.count('“') + raw_text.count('”')
        
        print(f'  Star leaks (** or ***): {len(star_leaks)}')
        if star_leaks:
            print('    Examples:', star_leaks[:3])
        print(f'  Straight quotes (\"): {straight_quotes}')
        print(f'  Administrative quotes (“...”): {admin_quotes}')
        if straight_quotes == 0 and len(star_leaks) == 0:
            print('  -> PASS 100% QUALITY STANDARDS!')
        else:
            print('  -> NEEDS ATTENTION!')
