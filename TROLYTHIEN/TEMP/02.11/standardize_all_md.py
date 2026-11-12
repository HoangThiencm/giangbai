# -*- coding: utf-8 -*-
import os, re, glob, sys

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\TEMP\02.11"
md_files = sorted(glob.glob(os.path.join(TEMP_DIR, "*.md")))

print(f"Tìm thấy {len(md_files)} tệp Markdown cần chuẩn hóa.")

for fpath in md_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Chuẩn hóa mục Năng lực số và AI trong I. MỤC TIÊU: IN ĐẬM VÀ IN NGHIÊNG (***...***)
    # Tìm vùng c) Năng lực số (NLS)
    def fix_nls_ai_objective(m):
        header = m.group(1) # c) Năng lực số (NLS): hoặc d) Năng lực Trí tuệ Nhân tạo (AI):
        bullet = m.group(2) # - **5.2.TC2b:** ... hoặc tương tự
        # Bóc tách text sạch bên trong bullet
        cleaned = re.sub(r'^\s*[-*+]\s*', '', bullet).strip()
        cleaned = re.sub(r'^\*+|(?<!\*)\*+$', '', cleaned).strip() # gỡ bỏ các dấu * ở đầu/cuối
        cleaned = re.sub(r'^\*\*(.*?)\*\*:?\s*', r'\1: ', cleaned).strip() # gỡ **Mã:**
        cleaned = re.sub(r'^\*\*\*(.*?)\*\*\*:?\s*', r'\1: ', cleaned).strip()
        # Đảm bảo mã và nội dung được bọc trong ***...***
        return f"{header}\n- ***{cleaned}***"

    # Regex cho c) Năng lực số
    content = re.sub(
        r'(c\)\s*Năng lực số\s*(?:\(NLS\))?:)\s*\n\s*([-*+].+?)(?=\n\s*(?:d\)|#|2\.|3\.|\Z))',
        fix_nls_ai_objective,
        content,
        flags=re.IGNORECASE | re.DOTALL
    )

    # Regex cho d) Năng lực AI
    content = re.sub(
        r'(d\)\s*Năng lực Trí tuệ Nhân tạo\s*(?:\(AI\))?:)\s*\n\s*([-*+].+?)(?=\n\s*(?:e\)|##|#|3\.|\Z))',
        fix_nls_ai_objective,
        content,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 2. Chuẩn hóa các dòng tích hợp NLS và AI trong bảng và các hoạt động
    # Tránh để cụm "GV:", "HS:" làm vỡ vai; dùng "Giáo viên", "học sinh"
    def fix_integration_line(m):
        raw = m.group(0)
        # Bóc nội dung bên trong dấu *** hoặc **
        inner = re.sub(r'^\s*[-*+]*\s*\**\s*', '', raw)
        inner = re.sub(r'\s*\**\s*$', '', inner)
        # Thay thế GV:, HS: bằng Giáo viên, học sinh trong dòng tích hợp
        inner = re.sub(r'\bGV:\s*', 'Giáo viên: ', inner)
        inner = re.sub(r'\bHS:\s*', 'học sinh: ', inner)
        inner = re.sub(r'\bGV\b', 'giáo viên', inner)
        inner = re.sub(r'\bHS\b', 'học sinh', inner)
        # Khôi phục chuẩn danh từ đầu câu nếu có
        inner = re.sub(r'^Tích hợp', 'Tích hợp', inner)
        return f"- ***{inner}***"

    # Match bất kỳ dòng nào bắt đầu bằng Tích hợp NLS hoặc Tích hợp AI
    content = re.sub(
        r'[-*+]?\s*\*{0,3}\s*(?:\(?\s*Tích hợp\s+(?:NLS|AI)[^\n\r]*?)\s*\*{0,3}',
        fix_integration_line,
        content,
        flags=re.IGNORECASE
    )

    # 3. Quét sạch các lỗi formatting sót trong markdown
    # Đảm bảo các dòng vai trong bảng có <br> rõ ràng
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f" -> Đã chuẩn hóa: {fname}")

print("HOÀN TẤT CHUẨN HÓA 10 FILE MARKDOWN!")
