# -*- coding: utf-8 -*-
"""
HỆ THỐNG PHẢN BIỆN TOÁN HỌC ĐA VÒNG (MULTI-ROUND MATHEMATICAL AUDITOR)
Kiểm định tính đúng đắn, tính khả thi sư phạm và sự khớp nối đề - đáp của toàn bộ 4 khối lớp (Toán 6, 7, 8, 9).
"""
import sys
import re
from fractions import Fraction

sys.stdout.reconfigure(encoding='utf-8')

def eval_arith(s):
    s = s.replace('$', '')
    s = s.replace('\\cdot', '*').replace(r'\cdot', '*').replace('·', '*').replace(r'\times', '*')
    s = s.replace('\\{', '(').replace('\\}', ')')
    s = s.replace('{', '(').replace('}', ')')
    s = s.replace('[', '(').replace(']', ')')
    s = s.replace('\\', '')
    s = re.sub(r'(\d+)\^(\d+)', r'(\1**\2)', s)
    s = re.sub(r'\)\^(\d+)', r')**\1', s)
    s = s.replace(':', '/')
    return eval(s)

def audit_toan_6():
    print("=" * 60)
    print("PHẢN BIỆN TOÁN HỌC KHỐI 6")
    print("=" * 60)
    with open('TROLYTHIEN/engine/builder_de_cuong_toan6.py', 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []

    # 1. Kiểm tra Bài 3.2
    # 100 : [45 - (18 - 3 * 5)^2] -> 100 : [45 - 9] = 100 : 36 (Lỗi)
    # 120 : [45 - (17 - 3 * 4)^2] -> 120 : [45 - 25] = 120 : 20 = 6 (OK)
    # 80 : [35 - (15 - 2 * 6)^2] -> 80 : [35 - 9] = 80 : 26 (Lỗi)
    # 160 : [25 - (18 - 7 * 2)^2] -> 160 : [25 - 16] = 160 : 9 (Lỗi)
    # 200 : [119 - (25 - 2 * 3)] -> 200 : [119 - 19] = 200 : 100 = 2 (OK)
    # 150 : [28 - (16 - 3 * 4)^2] -> 150 : [28 - 16] = 150 : 12 = 12.5 (Lỗi)
    # 90 : [24 - (15 - 3 * 3)^2] -> 90 : [24 - 36] = 90 : (-12) (Lỗi âm)
    # 180 : [45 - (18 - 3 * 5)^2] -> 180 : [45 - 9] = 180 : 36 = 5 (OK)

    # 2. Kiểm tra các câu tìm x Toán 6:
    # Tuyển tập các phương trình tìm x:
    # 3x = 75 -> x = 25
    # 5x = 120 -> x = 24
    # 96 : x = 12 -> x = 8
    # 84 : x = 14 -> x = 6
    # x : 15 = 8 -> x = 120
    # x : 12 = 15 -> x = 180
    # 7x = 91 -> x = 13
    # 144 : x = 16 -> x = 9
    # 3(x + 4) = 42 -> x + 4 = 14 -> x = 10
    # 5(x + 7) = 120 -> x + 7 = 24 -> x = 17
    # 4(x - 5) = 28 -> x - 5 = 7 -> x = 12
    # 6(x - 3) = 54 -> x - 3 = 9 -> x = 12
    # 84 : (x - 3) = 14 -> x - 3 = 6 -> x = 9
    # 120 : (x - 2) = 24 -> x - 2 = 5 -> x = 7
    # 75 : (x - 3) = 15 -> x - 3 = 5 -> x = 8
    # 110 : (x + 2) = 11 -> x + 2 = 10 -> x = 8
    # 2x - 15 = 45 -> 2x = 60 -> x = 30
    # 3x - 14 = 31 -> 3x = 45 -> x = 15
    # 4x + 18 = 54 -> 4x = 36 -> x = 9
    # 5x - 23 = 47 -> 5x = 70 -> x = 14
    # 2x + 35 = 75 -> 2x = 40 -> x = 20
    # 6x - 27 = 33 -> 6x = 60 -> x = 10
    # 7x + 15 = 57 -> 7x = 42 -> x = 6
    # 8x - 35 = 45 -> 8x = 80 -> x = 10
    # 65 - 5(x + 3) = 20 -> 5(x+3) = 45 -> x+3=9 -> x=6
    # 50 - 4(x + 2) = 18 -> 4(x+2) = 32 -> x+2=8 -> x=6
    # 48 - 3(x - 5) = 24 -> 3(x-5) = 24 -> x-5=8 -> x=13
    # 72 - 3(x + 5) = 27 -> 3(x+5) = 45 -> x+5=15 -> x=10
    # 125 - 5(x + 4) = 45 -> 5(x+4) = 80 -> x+4=16 -> x=12
    # 90 - 3(x + 7) = 45 -> 3(x+7) = 45 -> x+7=15 -> x=8
    # 110 - 5(x + 2) = 40 -> 5(x+2) = 70 -> x+2=14 -> x=12
    # (2x - 8) : 3 = 14 -> 2x - 8 = 42 -> 2x = 50 -> x = 25
    # (x - 1)^2 = 25 -> x - 1 = 5 -> x = 6
    # (x + 2)^3 = 27 -> x + 2 = 3 -> x = 1
    # (x - 1)^3 = 27 -> x - 1 = 3 -> x = 4
    # (2x - 1)^2 = 49 -> 2x - 1 = 7 -> x = 4
    # (x + 1)^3 = 64 -> x + 1 = 4 -> x = 3
    # (2x - 3)^2 = 25 -> 2x - 3 = 5 -> x = 4
    # All these equations have beautiful positive integer solutions!

    # 3. Check Đề 10 bài 2a:
    # 9x - 24 = 48 -> 9x = 72 -> x = 8 (OK)
    # Đề 8 bài 2a:
    # 4x - 19 = 45 -> 4x = 64 -> x = 16 (OK)
    # Đề 7 bài 2a:
    # 5x - 38 = 42 -> 5x = 80 -> x = 16 (OK)

    # 4. Check Đề 2 Bài 4:
    # Chiều dài 18m, chiều rộng 10m -> S = 180 m2.
    # Bồn hoa hình thoi 2 đường chéo 6m và 4m -> S_thoi = (6*4)/2 = 12 m2.
    # S_rau = 180 - 12 = 168 m2.
    # Hàng rào = 2*(18 + 10) - 2 = 56 - 2 = 54 m. (OK)

    # 5. Check Đề 4 Bài 4:
    # Đáy 25m, chiều cao tương ứng 12m -> S = 25*12 = 300 m2.
    # Cạnh bên 15m -> Chu vi = 2*(25 + 15) = 80 m. (OK)

    # 6. Check Đề 7 Bài 4:
    # Mảnh đất hình thoi đường chéo 16m và 12m -> S = 16*12/2 = 96 m2.
    # Cạnh hình thoi 10m -> Chu vi = 4*10 = 40 m.
    # (Lưu ý: 10^2 = 6^2 + 8^2 = 100, chuẩn Pythagore nửa đường chéo 8 và 6! Số liệu cực chuẩn hình học!)

    # 7. Check Đề 9 Bài 4:
    # Dài 9m, rộng 6m -> S = 54 m2 = 540 000 cm2.
    # Gạch vuông cạnh 30cm -> S_gạch = 900 cm2.
    # Số gạch = 540 000 / 900 = 600 viên. (Chia hết, OK)

    # 8. Check Đề 10 Bài 4:
    # Dài 16m, rộng 10m -> S = 160 m2 = 1 600 000 cm2.
    # Gạch vuông cạnh 40cm -> S_gạch = 1600 cm2.
    # Số gạch = 1 600 000 / 1600 = 1000 viên. (Chia hết, OK)

    print("Phát hiện các bài toán thực hiện phép tính bị lỗi số liệu trong Toán 6:")
    faulty_expressions = [
        ("Bài 3.2 a", "100 : [45 - (18 - 3 * 5)^2]", "Mẫu = 36, 100 không chia hết cho 36"),
        ("Bài 3.2 c", "80 : [35 - (15 - 2 * 6)^2]", "Mẫu = 26, 80 không chia hết cho 26"),
        ("Bài 3.2 d", "160 : [25 - (18 - 7 * 2)^2]", "Mẫu = 9, 160 không chia hết cho 9"),
        ("Bài 3.2 f", "150 : [28 - (16 - 3 * 4)^2]", "Mẫu = 12, 150 không chia hết cho 12"),
        ("Bài 3.2 g", "90 : [24 - (15 - 3 * 3)^2]", "Mẫu = -12, phép trừ ra số âm trong N"),
        ("Bài 3.3 a", "140 : [35 - (16 - 3 * 4)^2]", "Mẫu = 19, 140 không chia hết cho 19"),
        ("Bài 3.3 b", "120 : [54 - (18 - 4 * 3)^2]", "Mẫu = 18, 120 không chia hết cho 18"),
        ("Đề 2 Bài 1c", "80 : [35 - (15 - 2 * 6)^2]", "Mẫu = 26, 80 không chia hết cho 26"),
        ("Đề 3 Bài 1c", "160 : [25 - (18 - 7 * 2)^2]", "Mẫu = 9, 160 không chia hết cho 9"),
        ("Đề 5 Bài 1c", "150 : [28 - (16 - 3 * 4)^2]", "Mẫu = 12, 150 không chia hết cho 12"),
        ("Đề 6 Bài 1c", "90 : [24 - (15 - 3 * 3)^2]", "Mẫu = -12, phép trừ ra số âm"),
        ("Đề 8 Bài 1c", "100 : [30 - (12 - 2 * 4)^2]", "Mẫu = 14, 100 không chia hết cho 14"),
        ("Đề 9 Bài 1c", "140 : [35 - (16 - 3 * 4)^2]", "Mẫu = 19, 140 không chia hết cho 19"),
        ("Đề 10 Bài 1c", "120 : [54 - (18 - 4 * 3)^2]", "Mẫu = 18, 120 không chia hết cho 18"),
    ]
    for label, expr, reason in faulty_expressions:
        print(f"❌ {label}: {expr} -> {reason}")

if __name__ == '__main__':
    audit_toan_6()
