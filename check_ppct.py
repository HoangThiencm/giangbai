import os
import sys
import docx

base_dir = r'C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\3_DUYET_GIAO_AN\Dau_vao'
sys.stdout.reconfigure(encoding='utf-8')

for f in ['Phu-luc-3-Toan 6.docx', 'Phu-luc-3-Toan 7.docx', 'Phu-luc-3-Toan 8.docx', 'Phu-luc-3-Toan 9.docx',
          'Phu-luc-3-Tin 6 (Tich hop AI).docx', 'Phu-luc-3-Tin 7 (Tich hop AI).docx', 'Phu-luc-3-Tin 8 (Tich hop AI).docx', 'Phu-luc-3-Tin 9 (Tich hop AI).docx']:
    p = os.path.join(base_dir, f)
    if os.path.exists(p):
        d = docx.Document(p)
        print(f"\n=================== {f} ===================")
        # Search table for Tuần 9 - 14
        for tbl in d.tables:
            for row in tbl.rows:
                cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
                # look for week 9 to 14 or lessons around tiết 30-50
                row_str = " | ".join(cells)
                if any(w in row_str for w in ['Tuần 9', 'Tuần 10', 'Tuần 11', 'Tuần 12', 'Tuần 13', 'Tuần 14', 'Tuần 15', 'T9', 'T10', 'T11', 'T12']):
                    print(row_str[:120])
                elif any(k in row_str for k in ['Thư viện', 'trải nghiệm', 'Thực hành']):
                    print(">>> " + row_str[:120])
