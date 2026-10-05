import docx
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def print_month_9(path, title):
    print(f"\n==========================================")
    print(f"CHI TIẾT THÁNG 9 (TUẦN 1-5): {title}")
    print(f"==========================================")
    doc = docx.Document(path)
    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
            unique_cells = []
            for c in cells:
                if not unique_cells or c != unique_cells[-1]:
                    unique_cells.append(c)
            line = " | ".join(unique_cells)
            # check if week 1, 2, 3, 4, 5 or tiết 1-16
            for w in ['Tuần 1', 'Tuần 2', 'Tuần 3', 'Tuần 4', 'Tuần 5', 'tuần 1', 'tuần 2', 'tuần 3', 'tuần 4', 'tuần 5']:
                if f'| {w[5:]} |' in f'| {line} |' or w in line:
                    print(f"T{t_idx}-R{r_idx:02d}: {line}")
                    break

print_month_9('TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/Phu-luc-3-Toan 6.docx', 'TOÁN 6')
print_month_9('TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/Phu-luc-3-Toan 7.docx', 'TOÁN 7')
