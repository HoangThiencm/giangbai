import os, sys, fitz, docx, re

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"

def get_file(substring):
    for f in os.listdir(folder):
        if substring.lower() in f.lower() and f.lower().endswith('.pdf'):
            return os.path.join(folder, f)
    return None

print("=== CHECKING PHỤ LỤC 3 FOR TOÁN 7, TOÁN 8, HĐTN 7 ===")

# 1. Check PL3 Toan 7
pl3_t7_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/Phu-luc-3-Toan 7.docx"
doc_t7 = docx.Document(pl3_t7_path)
print("\n--- PL3 TOÁN 7 (Tháng 9: Tuần 1 - 4) ---")
for t in doc_t7.tables:
    for r in t.rows:
        row_txt = " | ".join([c.text.strip().replace('\n', ' ') for c in r.cells])
        if any(w in row_txt.lower() for w in ['tuần 1', 'tuần 2', 'tuần 3', 'tuần 4', 'tiết 1', 'tiết 8', 'tiết 9']):
            dedup = []
            for c in r.cells:
                ct = c.text.strip().replace('\n', ' ')
                if not dedup or ct != dedup[-1]:
                    dedup.append(ct)
            print("  ", " | ".join(dedup))

# 2. Check PL3 Toan 8
pl3_t8_path = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/Phu-luc-3-Toan 8.docx"
doc_t8 = docx.Document(pl3_t8_path)
print("\n--- PL3 TOÁN 8 (Tháng 9: Tuần 1 - 4) ---")
for t in doc_t8.tables:
    for r in t.rows:
        row_txt = " | ".join([c.text.strip().replace('\n', ' ') for c in r.cells])
        if any(w in row_txt.lower() for w in ['tuần 1', 'tuần 2', 'tuần 3', 'tuần 4', 'tiết 8', 'tiết 9', 'tiết 10']):
            dedup = []
            for c in r.cells:
                ct = c.text.strip().replace('\n', ' ')
                if not dedup or ct != dedup[-1]:
                    dedup.append(ct)
            print("  ", " | ".join(dedup))

print("\n=== CHECKING SPECIFIC ISSUES IN LE THI BINH'S FILES ===")

# 3. Check Hinh Hoc 8: Math in Tu Giac (Page 4, 5)
f_hh8 = get_file("HÌNH HỌC 8")
if f_hh8:
    doc = fitz.open(f_hh8)
    print(f"\n--- HÌNH HỌC 8: Pages 1-8 (Tu Giac) Math & NLS ---")
    for p in range(min(8, len(doc))):
        print(f"--- PAGE {p+1} ---")
        print(doc[p].get_text()[:600])

# 4. Check Hinh Hoc 8: Pages 40-52 (End of file, periods)
if f_hh8:
    doc = fitz.open(f_hh8)
    print(f"\n--- HÌNH HỌC 8: Pages 45-52 (Periods & Lessons) ---")
    for p in range(44, len(doc)):
        print(f"--- PAGE {p+1} ---")
        lines = [l.strip() for l in doc[p].get_text().splitlines() if l.strip()]
        for l in lines[:10]:
            print("  ", l)

