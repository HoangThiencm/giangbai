import os, sys, fitz

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/TRAN SANG"

def check_hinh6():
    f_h6 = os.path.join(folder, "HÌNH HỌC 6 - THÁNG 9 - TRẦN SÁNG_1791200843581.pdf")
    doc = fitz.open(f_h6)
    print(f"=== HÌNH HỌC 6: {len(doc)} pages ===")
    for p_no in range(len(doc)):
        txt = doc[p_no].get_text()
        for l in txt.splitlines():
            ls = l.strip()
            if any(w in ls.lower() for w in ['tiết', 'tuần', 'bài 18', 'bài 19', 'hình bình hành', 'hình thang cân']):
                if len(ls) < 80:
                    print(f"  P{p_no+1}: {ls}")

def check_so6_tail():
    f_s6 = os.path.join(folder, "SỐ HỌC 6 - THANG 9 - TRẦN SÁNG_1791200844100.pdf")
    doc = fitz.open(f_s6)
    print(f"\n=== SỐ HỌC 6 (Pages 42-54): {len(doc)} pages ===")
    for p_no in range(41, len(doc)):
        print(f"\n--- PAGE {p_no+1} ---")
        lines = [l.strip() for l in doc[p_no].get_text().splitlines() if l.strip()]
        for l in lines[:15]:
            print("  ", l)

check_hinh6()
check_so6_tail()
