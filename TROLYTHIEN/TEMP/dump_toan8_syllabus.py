import docx

doc = docx.Document('TROLYTHIEN/1_SOAN_KHBD/Dau_vao/PHỤ LỤC 3-TOÁN 8 (26-27) - Chỉnh.docx')
t1 = doc.tables[1] # Dai so & Xac suat
t2 = doc.tables[2] # Hinh hoc

with open('TROLYTHIEN/TEMP/toan8_hk2_syllabus.txt', 'w', encoding='utf-8') as f:
    f.write("=== TABLE 1: ĐẠI SỐ & THỐNG KÊ XÁC SUẤT (HK2 - TUẦN 19 ĐẾN 35) ===\n")
    for i, r in enumerate(t1.rows):
        cells = [c.text.strip().replace('\n', ' ') for c in r.cells]
        # check week
        tuan = cells[4] if len(cells) > 4 else ''
        f.write(f"Row {i:02d}: STT={cells[0]} | Bai={cells[1]} | SoTiet={cells[2]} | TietPPCT={cells[3]} | Tuan={tuan} | NLS={cells[7] if len(cells)>7 else ''} | AI={cells[8] if len(cells)>8 else ''}\n")

    f.write("\n=== TABLE 2: HÌNH HỌC VÀ ĐO LƯỜNG (HK2 - TUẦN 19 ĐẾN 35) ===\n")
    for i, r in enumerate(t2.rows):
        cells = [c.text.strip().replace('\n', ' ') for c in r.cells]
        tuan = cells[4] if len(cells) > 4 else ''
        f.write(f"Row {i:02d}: STT={cells[0]} | Bai={cells[1]} | SoTiet={cells[2]} | TietPPCT={cells[3]} | Tuan={tuan} | NLS={cells[7] if len(cells)>7 else ''} | AI={cells[8] if len(cells)>8 else ''}\n")

print("Done dumping Toán 8 syllabus.")
