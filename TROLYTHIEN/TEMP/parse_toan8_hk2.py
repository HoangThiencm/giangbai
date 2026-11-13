import docx
import re

doc = docx.Document('TROLYTHIEN/1_SOAN_KHBD/Dau_vao/PHỤ LỤC 3-TOÁN 8 (26-27) - Chỉnh.docx')
t1 = doc.tables[1]
t2 = doc.tables[2]

def extract_hk2(table, name):
    rows = []
    for i, r in enumerate(table.rows[1:], 1):
        cells = [c.text.strip().replace('\n', ' ') for c in r.cells]
        tuan_str = cells[4] if len(cells) > 4 else ''
        # extract numbers from tuan_str
        nums = [int(n) for n in re.findall(r'\d+', tuan_str)]
        if any(w >= 19 for w in nums) or 'Học kì II' in cells[1] or 'HỌC KÌ II' in cells[1]:
            rows.append({
                'row_idx': i,
                'stt': cells[0],
                'bai': cells[1],
                'so_tiet': cells[2],
                'tiet_ppct': cells[3],
                'tuan': tuan_str,
                'nls': cells[7] if len(cells) > 7 else '',
                'ai': cells[8] if len(cells) > 8 else ''
            })
    return rows

r1 = extract_hk2(t1, "Đại số & Thống kê Xác suất")
r2 = extract_hk2(t2, "Hình học & Đo lường")

print(f"Toán 8 Table 1 (Đại số & Thống kê) HK2 rows: {len(r1)}")
for r in r1:
    print(f"  Row {r['row_idx']}: {r['bai']} | Tiết PPCT: {r['tiet_ppct']} | {r['tuan']} | NLS: {'YES' if r['nls'] else 'NO'} | AI: {'YES' if r['ai'] else 'NO'}")

print(f"\nToán 8 Table 2 (Hình học) HK2 rows: {len(r2)}")
for r in r2:
    print(f"  Row {r['row_idx']}: {r['bai']} | Tiết PPCT: {r['tiet_ppct']} | {r['tuan']} | NLS: {'YES' if r['nls'] else 'NO'} | AI: {'YES' if r['ai'] else 'NO'}")
