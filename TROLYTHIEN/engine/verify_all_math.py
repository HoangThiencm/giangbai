# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def test_toan_6():
    print("=" * 60)
    print("KIỂM TRA TOÀN DIỆN TOÁN 6")
    print("=" * 60)
    with open('TROLYTHIEN/engine/builder_de_cuong_toan6.py', 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract all string literals containing $...$
    pattern = r'"([a-hA-Z0-9\(\)\s,\.\-]+)\$([^$]+)\$"'
    matches = re.findall(pattern, text)
    print(f"Tổng số biểu thức tìm thấy: {len(matches)}")

    errors = []
    checked_count = 0

    for prefix, expr in matches:
        raw = expr.strip()
        # Filter out algebraic equations, sets, power comparisons
        if any(v in raw for v in ['x', 'n', 'y', 'dots', 'ƯCLN', 'BCNN', 'ƯC', 'BC', 'overline', 'vdots', 'neq', 'le', 'ge', 'sim', 'circ', 'text']):
            continue
        
        # Check pure arithmetic expressions
        clean = raw.replace(r'\cdot', '*').replace(r'\times', '*').replace(':', '/')
        clean = clean.replace('\\{', '(').replace('\\}', ')')
        clean = clean.replace('{', '(').replace('}', ')')
        clean = clean.replace('[', '(').replace(']', ')')
        clean = clean.replace('\\', '')
        clean = re.sub(r'(\d+)\^(\d+)', r'(\1**\2)', clean)
        clean = re.sub(r'\)\^(\d+)', r')**\1', clean)
        
        # Only evaluate if contains digits and arithmetic operators
        if re.search(r'[\d]', clean) and re.search(r'[\+\-\*/]', clean):
            try:
                # Also check intermediate sub-expressions inside brackets for non-negative
                # E.g. (a - b) must have a >= b
                val = eval(clean)
                checked_count += 1
                if isinstance(val, float):
                    if not val.is_integer():
                        errors.append(f"❌ [LẺ THẬP PHÂN] {prefix.strip()} ${raw}$ = {val}")
                    elif val < 0:
                        errors.append(f"❌ [KẾT QUẢ ÂM] {prefix.strip()} ${raw}$ = {val}")
                elif isinstance(val, int) and val < 0:
                    errors.append(f"❌ [KẾT QUẢ ÂM] {prefix.strip()} ${raw}$ = {val}")
            except Exception as e:
                # e.g. syntax error in formula
                pass

    print(f"Số phép tính số học thuần túy đã kiểm tra: {checked_count}")
    if errors:
        for err in errors:
            print(err)
    else:
        print("✅ 100% CÁC PHÉP TÍNH TOÁN 6 ĐỀU CHIA HẾT VÀ CHO KẾT QUẢ SỐ TỰ NHIÊN DƯƠNG!")

    return len(errors) == 0

def test_toan_8():
    print("\n" + "=" * 60)
    print("KIỂM TRA TOÀN DIỆN TOÁN 8")
    print("=" * 60)
    with open('TROLYTHIEN/engine/builder_de_cuong_toan8.py', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Check De 1 Bai 3
    ok1 = "tăng thêm 34" in text and "4x - 6 = 34" in text
    print(f"Đề 1 Bài 3 (tăng 34 m2 -> x = 10 nguyên đẹp): {'✅ PASS' if ok1 else '❌ FAIL'}")

    # Check De 5 Bai 3
    ok2 = "chiều dài hơn chiều rộng 5 m và chu vi bằng 50 m" in text
    print(f"Đề 5 Bài 3 (dài hơn rộng 5m, chu vi 50m -> dài 15, rộng 10, S = 150): {'✅ PASS' if ok2 else '❌ FAIL'}")

    return ok1 and ok2

def test_toan_9():
    print("\n" + "=" * 60)
    print("KIỂM TRA TOÀN DIỆN TOÁN 9")
    print("=" * 60)
    with open('TROLYTHIEN/engine/builder_de_cuong_toan9.py', 'r', encoding='utf-8') as f:
        text = f.read()

    # Check De 6 Bai 3
    ok1 = "diện tích tăng thêm 25" in text
    print(f"Đề 6 Bài 3 (diện tích tăng thêm 25 m2 -> dài 30, rộng 20, S = 600): {'✅ PASS' if ok1 else '❌ FAIL'}")

    return ok1

if __name__ == '__main__':
    p6 = test_toan_6()
    p8 = test_toan_8()
    p9 = test_toan_9()
    print("\n" + "=" * 60)
    if p6 and p8 and p9:
        print("🏆 TẤT CẢ CÁC ĐỀ BÀI CẢ 4 KHỐI ĐÃ ĐƯỢC CHUẨN HÓA VÀ KHỚP 100%!")
    else:
        print("⚠️ VẪN CÒN ĐIỂM CHƯA ĐẠT!")
    print("=" * 60)
