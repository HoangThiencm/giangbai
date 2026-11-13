import os
import docx

base_dir = r'C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\3_DUYET_GIAO_AN\Dau_vao'

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.docx') and not f.startswith('~$') and not f.startswith('Phu-luc-3') and not f.startswith('PL3'):
            p = os.path.join(root, f)
            try:
                doc = docx.Document(p)
                text_sample = []
                for para in doc.paragraphs[:15]:
                    t = para.text.strip()
                    if t:
                        text_sample.append(t)
                for table in doc.tables[:2]:
                    for row in table.rows[:3]:
                        for cell in row.cells:
                            ct = cell.text.strip()
                            if any(k in ct for k in ['Lớp', 'lớp', 'GV', 'Giáo viên', 'Dạy']):
                                text_sample.append(ct)
                print(f"=== File: {f} ===")
                print("\n".join(text_sample[:8]))
            except Exception as e:
                pass
