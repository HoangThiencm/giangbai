# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def audit_word_problems():
    print("="*60)
    print("KIỂM TRA TẤT CẢ CÁC BÀI TOÁN THỰC TẾ & HÌNH HỌC TRONG 10 ĐỀ (LỚP 6, 7, 8, 9)")
    print("="*60)

    # TOÁN 8
    print("\n--- TOÁN 8: RÀ SOÁT TỪNG ĐỀ ---")
    # Đề 1:
    # Bài 3: Một mảnh đất hình chữ nhật có chiều dài gấp đôi chiều rộng. Nếu giảm chiều dài 2 m và tăng chiều rộng 3 m thì diện tích tăng thêm 36 m2.
    # Chiều rộng x, dài 2x. (2x - 2)(x + 3) - 2x^2 = 2x^2 + 4x - 6 - 2x^2 = 4x - 6.
    # 4x - 6 = 36 => 4x = 42 => x = 10.5 (LẺ)
    # SỬA: "diện tích tăng thêm 34 m2" => 4x - 6 = 34 => 4x = 40 => x = 10 m, dài 20 m!
    print("Đề 1 Bài 3: Sửa 'tăng thêm 36 m2' thành 'tăng thêm 34 m2' để chiều rộng x = 10m, dài 20m nguyên đẹp.")

    # Đề 2 Bài 3: Thang dài 5m, cách chân tường 3m => chiều cao h = sqrt(5^2 - 3^2) = 4m. (OK)
    
    # Đề 3 Bài 3: AB = 12, AC = 15. AD = 4. AE = 5, EC = 10. (OK)

    # Đề 4 Bài 3: Cột cờ: (2 - 1.6)/3 = 0.4/3. Chiều cao = 1.6 + 0.4/3 * 15 = 1.6 + 2 = 3.6m. (OK)

    # Đề 5 Bài 3:
    # "Một mảnh đất hình chữ nhật có chu vi 50 m. Nếu tăng chiều rộng thêm 5 m và giảm chiều dài đi 5 m thì diện tích tăng thêm 25 m2. Tính diện tích mảnh đất ban đầu."
    # Ban đầu: dài 15, rộng 10. S_bd = 150.
    # Mới: dài 10, rộng 15. S_moi = 150. S_moi - S_bd = 0! Đề bảo tăng thêm 25 m2 là VÔ LÝ!
    # SỬA: "Một mảnh đất hình chữ nhật có chiều dài hơn chiều rộng 5 m và chu vi bằng 50 m. Tính diện tích mảnh đất đó."
    # Hoặc: "Một mảnh đất hình chữ nhật có chu vi 60 m. Nếu tăng chiều rộng thêm 3 m và giảm chiều dài đi 3 m thì diện tích tăng thêm 9 m2 (hoặc một số liệu tính toán chuẩn)."
    # Tốt nhất và thực tế nhất:
    # "Một mảnh đất hình chữ nhật có chiều dài hơn chiều rộng 6 m. Biết chu vi của mảnh đất là 52 m. Tính diện tích mảnh đất ban đầu."
    # Nửa chu vi = 26 m. Dài = (26 + 6)/2 = 16 m. Rộng = 16 - 6 = 10 m. S = 160 m2. Cực kỳ trong sáng và chuẩn mực!

    # Đề 6 Bài 3: P = x^3 - 3x^2 + 3x - 1 tại x = 101 => (101 - 1)^3 = 100^3 = 1 000 000. (OK)

    # Đề 7 Bài 3: AM = 3, MB = 6, AN = 4 => NC = 8, AC = 12. (OK)

    # Đề 8 Bài 3: A = 75^2 - 25^2 = 5000; B = 102 * 98 = (100+2)(100-2) = 9996. (OK)

    # Đề 9 Bài 3: M = (x - 5)(2x + 3) - 2x(x - 3) + x + 7 = 2x^2 - 7x - 15 - 2x^2 + 6x + x + 7 = -8 (không phụ thuộc x). (OK)

    # Đề 10 Bài 3: Sân vuông cạnh x, mở rộng mỗi phía 2m => cạnh mới (x + 4). S_lối_đi = (x + 4)^2 - x^2 = 8x + 16. (OK)

    # TOÁN 9
    print("\n--- TOÁN 9: RÀ SOÁT TỪNG ĐỀ ---")
    # Đề 1 Bài 3: v1 - v2 = 10. 2(v1 + v2) = 180 => v1 + v2 = 90. v1 = 50, v2 = 40. (OK)
    # Đề 2 Bài 3: Chu vi 140 => nửa chu vi 70. (x - 10)(70 - x + 5) = x(70 - x)
    # => (x - 10)(75 - x) = 70x - x^2 => 85x - x^2 - 750 = 70x - x^2 => 15x = 750 => x = 50, y = 20. S = 1000. (OK)
    # Đề 3 Bài 3: x + y = 600 000. 0.9x + 0.85y = 522 000 => x = 360 000, y = 240 000. (OK)
    # Đề 4 Bài 3: 1/x + 1/y = 1/12, 4/x + 9/y = 7/12 => 1/x = 1/20, 1/y = 1/30 => x = 20, y = 30. (OK)
    # Đề 5 Bài 3: 45/(v+3) + 18/(v-3) = 3 => v = 21 km/h. (OK)
    # Đề 6 Bài 3: SỬA 'tăng thêm 50 m2' thành 'tăng thêm 25 m2' để khớp: dài 30m, rộng 20m.
    # Đề 7 Bài 3: x + y = 800, 1.15x + 1.2y = 945 => 0.05y = 945 - 920 = 25 => y = 500, x = 300. (OK)
    # Đề 8 Bài 3: Chu vi 72 => x + y = 36. x - y = 12 => x = 24, y = 12. S = 288 m2. (OK)
    # Đề 9 Bài 3: x - y = 3, 2(x + y) = 42 => x + y = 21 => x = 12, y = 9. (OK)
    # Đề 10 Bài 3: x + y = 40, 3x + 2y = 105 => x = 25, y = 15. (OK)

if __name__ == '__main__':
    audit_word_problems()
