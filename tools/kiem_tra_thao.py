import docx
import os
import sys

# Force utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

def parse_pl3(path):
    print(f"\n==================================================")
    print(f"PHỤ LỤC 3: {os.path.basename(path)}")
    print(f"==================================================")
    doc = docx.Document(path)
    for t_idx, table in enumerate(doc.tables):
        print(f"--- Table {t_idx} (rows: {len(table.rows)}, cols: {len(table.columns)}) ---")
        for r_idx, row in enumerate(table.rows[:35]):
            cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
            # eliminate duplicates if merged
            unique_cells = []
            for c in cells:
                if not unique_cells or c != unique_cells[-1]:
                    unique_cells.append(c)
            line = " | ".join(unique_cells)
            if any(k in line for k in ['Tuần', 'Bài', 'tiết', 'Tiết', 'NLS', 'AI', 'Số', 'Hình']):
                print(f"R{r_idx:02d}: {line}")

parse_pl3('TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/Phu-luc-3-Toan 6.docx')
parse_pl3('TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/Phu-luc-3-Toan 7.docx')
