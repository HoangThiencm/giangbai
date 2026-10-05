import os, sys, fitz

sys.stdout.reconfigure(encoding='utf-8')
folder = r"TROLYTHIEN/3_DUYET_GIAO_AN/Dau_vao/LE THI BINH"

f_hh8 = [f for f in os.listdir(folder) if 'HÌNH HỌC 8' in f.upper() or '1791212409278' in f][0]
f_hh7 = [f for f in os.listdir(folder) if 'HÌNH HỌC 7' in f.upper() or '1791212408808' in f][0]

print(f"=== RE-CHECKING LE THI BINH ===")
print("File HH8:", f_hh8)
print("File HH7:", f_hh7)

SUSPICIOUS_CHARS = [
    0x0307, 0x0308, 0x0227, 0x1e41, 0x1e8b, 0x1e8f,
    0x22a5, 0x00b5
]

def check_file(f_name):
    doc = fitz.open(os.path.join(folder, f_name))
    print(f"\n=======================================================")
    print(f"ANALYZING: {f_name} ({len(doc)} pages)")
    
    suspicious_hits = []
    
    for p_no in range(len(doc)):
        page = doc[p_no]
        txt = page.get_text()
        
        # Check text lines for suspicious chars
        for line in txt.splitlines():
            ls = line.strip()
            for ch in ls:
                if ord(ch) in SUSPICIOUS_CHARS:
                    suspicious_hits.append((p_no + 1, ls, ch, hex(ord(ch))))
                    break
                    
        # Check for Luyện tập 2 in HH8
        if "Luyện tập 2" in txt or "Theo định lí về tổng các góc" in txt:
            print(f"\n--- FOUND Luyện tập 2 at Page {p_no+1} ---")
            lines = [l.strip() for l in txt.splitlines() if l.strip()]
            for l in lines:
                if any(k in l for k in ["360°", "Luyện tập 2", "Theo định lí", "Do đó", "125°", "50°", "110°"]):
                    print("  ", l)

        # Check for góc micro in HH8 (trang 51 cũ)
        if "phân giác của góc" in txt:
            print(f"\n--- FOUND Phân giác at Page {p_no+1} ---")
            lines = [l.strip() for l in txt.splitlines() if l.strip()]
            for l in lines:
                if "phân giác" in l:
                    print("  ", l)

    print(f"\n--- SUSPICIOUS CHARACTERS FOUND: {len(suspicious_hits)} ---")
    for p, l, ch, code in suspicious_hits:
        print(f"  P{p} [{code}]: {l}")

check_file(f_hh8)
check_file(f_hh7)
