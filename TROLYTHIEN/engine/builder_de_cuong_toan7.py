# -*- coding: utf-8 -*-
"""
BIÊN SOẠN ĐỀ CƯƠNG ÔN TẬP GIỮA HỌC KỲ I - TOÁN 7 (PHIÊN BẢN CHUẨN THỰC CHIẾN)
NĂM HỌC: 2026 - 2027 (Đã bỏ cấp Phòng GD&ĐT, chuẩn TRƯỜNG THCS TRẦN PHÚ / TỔ: TOÁN - TIN)
CHƯƠNG TRÌNH: GDPT 2018 - MÔN TOÁN 7 (BỘ KẾT NỐI TRI THỨC VỚI CUỘC SỐNG)

CẤU TRÚC 3 PHẦN:
1. PHẦN I: CÁC DẠNG BÀI TẬP RÈN KỸ NĂNG THỰC CHIẾN (17 DẠNG CHUYÊN SÂU CHO HỌC SINH YẾU, TRUNG BÌNH & KHÁ)
2. PHẦN II: BỘ 10 ĐỀ ÔN TẬP TỰ LUẬN 100% (THỜI GIAN LÀM BÀI: 60 PHÚT/ĐỀ)
3. PHẦN III: BẢNG ĐÁP SỐ VÀ HƯỚNG DẪN GIẢI CHI TIẾT 10 ĐỀ TỰ LUẬN
"""

import os
from de_cuong_docx_helper import (
    create_base_document, add_header_quoc_hieu, add_heading_1, add_heading_2,
    add_heading_3, add_body_paragraph, add_exercise, add_test_header,
    add_answer_header, add_answer_item
)

def build_de_cuong_toan_7(output_path):
    doc = create_base_document()
    add_header_quoc_hieu(doc, "7", school_year="2026 - 2027")
    
    # =========================================================================
    # PHẦN I: CÁC DẠNG BÀI TẬP RÈN KỸ NĂNG THỰC CHIẾN (17 DẠNG CHUYÊN SÂU)
    # =========================================================================
    add_heading_1(doc, "PHẦN I: CÁC DẠNG BÀI TẬP RÈN KỸ NĂNG THỰC CHIẾN (DÀNH CHO HỌC SINH YẾU, TRUNG BÌNH & KHÁ)")
    
    # ----------------------------- CHỦ ĐỀ 1 -----------------------------
    add_heading_2(doc, "A. SỐ HỮU TỈ VÀ CÁC PHÉP TÍNH VỚI SỐ HỮU TỈ")
    
    # DẠNG 1
    add_heading_3(doc, "Dạng 1: Tập hợp số hữu tỉ, số đối và so sánh số hữu tỉ")
    add_body_paragraph(doc, "Kỹ năng cần nắm: \n- Số hữu tỉ là số viết được dưới dạng phân số $\\frac{a}{b}$ với $a, b \\in \\mathbb{Z}, b \\neq 0$. Tập hợp các số hữu tỉ kí hiệu là $\\mathbb{Q}$.\n- Số đối của số hữu tỉ $\\frac{a}{b}$ là $-\\frac{a}{b}$.\n- Để so sánh hai số hữu tỉ: Đưa về phân số có cùng mẫu số dương rồi so sánh các tử số (hoặc so sánh với số 0, số 1, số đối).", "★")
    
    add_exercise(doc, "1.1", "Điền kí hiệu thích hợp ($\\in, \\notin, \\subset$) vào ô trống:", [
        "a) $-5 \\dots \\mathbb{N}$",
        "b) $-5 \\dots \\mathbb{Z}$",
        "c) $-5 \\dots \\mathbb{Q}$",
        "d) $-\\frac{3}{7} \\dots \\mathbb{Z}$",
        "e) $-\\frac{3}{7} \\dots \\mathbb{Q}$",
        "f) $0{,}25 \\dots \\mathbb{Q}$",
        "g) $\\mathbb{N} \\dots \\mathbb{Z}$",
        "h) $\\mathbb{Z} \\dots \\mathbb{Q}$"
    ])
    
    add_exercise(doc, "1.2", "Tìm số đối của mỗi số hữu tỉ sau:", [
        "a) $\\frac{4}{7}$",
        "b) $-\\frac{5}{9}$",
        "c) $-1{,}5$",
        "d) $0$",
        "e) $2\\frac{1}{3}$",
        "f) $-\\frac{-3}{8}$"
    ])
    
    add_exercise(doc, "1.3", "So sánh các cặp số hữu tỉ sau:", [
        "a) $\\frac{-3}{5}$ và $\\frac{-4}{5}$",
        "b) $\\frac{2}{3}$ và $\\frac{3}{4}$",
        "c) $\\frac{-5}{7}$ và $\\frac{-3}{4}$",
        "d) $-0{,}6$ và $\\frac{-7}{10}$",
        "e) $\\frac{-13}{20}$ và $\\frac{7}{-10}$",
        "f) $\\frac{-1}{100}$ và $0{,}001$"
    ])
    
    # DẠNG 2
    add_heading_3(doc, "Dạng 2: Thực hiện phép tính cộng, trừ số hữu tỉ")
    add_body_paragraph(doc, "Kỹ năng cần nắm: \n- Viết các số hữu tỉ dưới dạng phân số có mẫu số dương $\\to$ Quy đồng mẫu số $\\to$ Cộng hoặc trừ các tử số và giữ nguyên mẫu số chung.\n- Với số thập phân: Đổi về phân số hoặc cộng trừ trực tiếp phần thập phân nếu thuận tiện.", "★")
    
    add_exercise(doc, "2.1", "Thực hiện phép tính:", [
        "a) $\\frac{-3}{7} + \\frac{5}{7}$",
        "b) $\\frac{-4}{9} - \\frac{2}{9}$",
        "c) $\\frac{1}{6} + \\frac{-5}{12}$",
        "d) $\\frac{-2}{3} - \\frac{1}{4}$",
        "e) $\\frac{5}{8} + \\frac{-3}{5}$",
        "f) $\\frac{-7}{10} - \\frac{-2}{5}$",
        "g) $-0{,}75 + \\frac{3}{4}$",
        "h) $1\\frac{1}{2} - 0{,}75$"
    ])
    
    add_exercise(doc, "2.2", "Thực hiện phép tính (kết hợp phân số và số thập phân):", [
        "a) $\\frac{-5}{6} + 0{,}25$",
        "b) $-1{,}2 - \\frac{3}{5}$",
        "c) $\\frac{7}{4} - \\left(-\\frac{1}{2}\\right) + \\frac{3}{8}$",
        "d) $-\\frac{5}{12} - \\left(\\frac{1}{3} - \\frac{1}{4}\\right)$",
        "e) $\\left(-\\frac{2}{5} + \\frac{1}{2}\\right) - \\left(\\frac{3}{4} - \\frac{1}{10}\\right)$",
        "f) $\\frac{2}{3} - \\left[-0{,}4 + \\left(\\frac{1}{3} - \\frac{4}{5}\\right)\\right]$"
    ])
    
    # DẠNG 3
    add_heading_3(doc, "Dạng 3: Thực hiện phép tính nhân, chia số hữu tỉ")
    add_body_paragraph(doc, "Kỹ năng cần nắm: \n- Nhân: $\\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}$ (rút gọn thừa số chung giữa tử và mẫu trước khi nhân).\n- Chia: $\\frac{a}{b} : \\frac{c}{d} = \\frac{a}{b} \\cdot \\frac{d}{c}$ (nhân với phân số nghịch đảo).", "★")
    
    add_exercise(doc, "3.1", "Thực hiện phép tính:", [
        "a) $\\frac{-3}{7} \\cdot \\frac{14}{9}$",
        "b) $\\frac{-5}{8} \\cdot \\frac{-16}{25}$",
        "c) $1\\frac{1}{3} \\cdot \\frac{-9}{8}$",
        "d) $\\frac{-12}{25} : \\frac{4}{5}$",
        "e) $\\frac{-8}{15} : \\frac{-4}{5}$",
        "f) $-2{,}4 : \\frac{6}{5}$",
        "g) $\\frac{3}{4} : (-1{,}5)$",
        "h) $0{,}75 \\cdot \\frac{-8}{9}$"
    ])
    
    # DẠNG 4
    add_heading_3(doc, "Dạng 4: Tính nhanh, tính hợp lý giá trị biểu thức số hữu tỉ")
    add_body_paragraph(doc, "Kỹ năng cần nắm: \n- Giao hoán và kết hợp: Nhóm các phân số có cùng mẫu số hoặc có tổng/hiệu là số nguyên.\n- Phân phối giữa phép nhân và phép cộng: $a \\cdot b + a \\cdot c = a \\cdot (b + c)$; $a \\cdot b - a \\cdot c = a \\cdot (b - c)$.\n- Chia cho cùng một số: $\\frac{a}{c} + \\frac{b}{c} = (a + b) : c$.", "★")
    
    add_exercise(doc, "4.1", "Tính hợp lý bằng cách nhóm các số hạng thích hợp:", [
        "a) $A = \\frac{5}{11} + \\frac{-3}{7} + \\frac{6}{11} + \\frac{-4}{7}$",
        "b) $B = \\frac{7}{15} + \\frac{-4}{9} + \\frac{8}{15} + \\frac{-5}{9}$",
        "c) $C = \\frac{-2}{17} + \\frac{15}{23} + \\frac{-15}{17} + \\frac{8}{23}$",
        "d) $D = \\frac{3}{5} + \\left(\\frac{-1}{4}\\right) + \\frac{2}{5} + \\left(-\\frac{3}{4}\\right) + 2026$",
        "e) $E = \\left(\\frac{1}{3} - \\frac{5}{7}\\right) + \\left(\\frac{2}{3} + \\frac{12}{7}\\right)$",
        "f) $F = \\frac{3}{8} - \\left(\\frac{-5}{6}\\right) - \\frac{11}{8} + \\frac{1}{6}$"
    ])
    
    add_exercise(doc, "4.2", "Tính hợp lý bằng cách đặt thừa số chung:", [
        "a) $M = \\frac{4}{9} \\cdot \\frac{13}{15} + \\frac{4}{9} \\cdot \\frac{2}{15}$",
        "b) $N = \\frac{5}{7} \\cdot \\frac{-3}{11} + \\frac{5}{7} \\cdot \\frac{-8}{11}$",
        "c) $P = \\frac{7}{19} \\cdot \\frac{8}{11} + \\frac{7}{19} \\cdot \\frac{3}{11} - \\frac{7}{19}$",
        "d) $Q = \\frac{-3}{8} \\cdot 2\\frac{1}{3} + \\frac{-3}{8} \\cdot 3\\frac{2}{3}$",
        "e) $R = \\frac{5}{13} \\cdot \\frac{-7}{9} + \\frac{5}{13} \\cdot \\frac{-2}{9} + 1\\frac{8}{13}$",
        "f) $S = \\left(\\frac{-5}{9} + \\frac{4}{11}\\right) : \\frac{7}{15} + \\left(\\frac{-4}{9} + \\frac{7}{11}\\right) : \\frac{7}{15}$"
    ])
    
    # ----------------------------- CHỦ ĐỀ 2 -----------------------------
    add_heading_2(doc, "B. LUỸ THỪA VỚI SỐ MŨ TỰ NHIÊN CỦA SỐ HỮU TỈ")
    
    # DẠNG 5
    add_heading_3(doc, "Dạng 5: Các phép tính về luỹ thừa của số hữu tỉ")
    add_body_paragraph(doc, "Công thức sống còn: \n- $x^m \\cdot x^n = x^{m + n}$; $x^m : x^n = x^{m - n}$ ($x \\neq 0, m \\ge n$).\n- $(x^m)^n = x^{m \\cdot n}$.\n- $(x \\cdot y)^n = x^n \\cdot y^n$; $\\left(\\frac{x}{y}\\right)^n = \\frac{x^n}{y^n}$ ($y \\neq 0$).\n- Quy ước: $x^0 = 1$ ($x \\neq 0$), $x^1 = x$.", "★")
    
    add_exercise(doc, "5.1", "Tính giá trị của mỗi luỹ thừa sau:", [
        "a) $\\left(-\\frac{1}{2}\\right)^2$",
        "b) $\\left(-\\frac{1}{2}\\right)^3$",
        "c) $\\left(-\\frac{2}{3}\\right)^4$",
        "d) $\\left(-1\\frac{1}{4}\\right)^2$",
        "e) $(-0{,}1)^3$",
        "f) $(-0{,}2)^4$",
        "g) $\\left(-\\frac{3}{5}\\right)^0$",
        "h) $\\left(\\frac{4}{7}\\right)^1$"
    ])
    
    add_exercise(doc, "5.2", "Áp dụng các quy tắc nhân, chia luỹ thừa để viết kết quả dưới dạng một luỹ thừa:", [
        "a) $\\left(-\\frac{2}{3}\\right)^3 \\cdot \\left(-\\frac{2}{3}\\right)^4$",
        "b) $(0{,}5)^6 : (0{,}5)^2$",
        "c) $\\left[\\left(-\\frac{3}{4}\\right)^2\\right]^3$",
        "d) $\\left(-\\frac{1}{5}\\right)^5 : \\left(-\\frac{1}{5}\\right)^3$",
        "e) $8^4 : 2^3$",
        "f) $27^3 : 9^2$"
    ])
    
    add_exercise(doc, "5.3", "Rút gọn các biểu thức chứa luỹ thừa bằng cách đưa về các thừa số nguyên tố:", [
        "a) $A = \\frac{4^3 \\cdot 9^7}{27^5 \\cdot 8^2}$",
        "b) $B = \\frac{2^{15} \\cdot 9^4}{6^6 \\cdot 8^3}$",
        "c) $C = \\frac{10^3 + 2 \\cdot 5^3 + 5^3}{55}$",
        "d) $D = \\frac{4^5 \\cdot 9^4 - 2 \\cdot 6^9}{2^{10} \\cdot 3^8 + 6^8 \\cdot 20}$"
    ])
    
    # DẠNG 6
    add_heading_3(doc, "Dạng 6: So sánh hai luỹ thừa")
    add_body_paragraph(doc, "Phương pháp: \n- Cách 1: Đưa về cùng cơ số $a^m$ và $a^n$ (với $a > 1$, nếu $m > n$ thì $a^m > a^n$).\n- Cách 2: Đưa về cùng số mũ $a^n$ và $b^n$ (với $a > b > 0$ thì $a^n > b^n$).\n- Cách 3: So sánh qua số trung gian.", "★")
    
    add_exercise(doc, "6.1", "So sánh các cặp luỹ thừa sau:", [
        "a) $2^{300}$ và $3^{200}$",
        "b) $2^{24}$ và $3^{16}$",
        "c) $5^{300}$ và $3^{500}$",
        "d) $99^{20}$ và $9999^{10}$",
        "e) $3^{39}$ và $11^{21}$",
        "f) $(-0{,}1)^4$ và $(-0{,}1)^2$"
    ])
    
    # ----------------------------- CHỦ ĐỀ 3 -----------------------------
    add_heading_2(doc, "C. QUY TẮC DẤU NGOẶC, QUY TẮC CHUYỂN VẾ VÀ TÌM X")
    
    # DẠNG 7
    add_heading_3(doc, "Dạng 7: Tìm x cơ bản áp dụng quy tắc chuyển vế đổi dấu")
    add_body_paragraph(doc, "Quy tắc: Khi chuyển một số hạng từ vế này sang vế kia của một đẳng thức, ta phải đổi dấu số hạng đó: dấu '+' đổi thành dấu '-' và dấu '-' đổi thành dấu '+'.", "★")
    
    add_exercise(doc, "7.1", "Tìm số hữu tỉ $x$, biết:", [
        "a) $x + \\frac{1}{3} = \\frac{4}{5}$",
        "b) $x - \\frac{2}{7} = -\\frac{5}{14}$",
        "c) $\\frac{3}{4} - x = \\frac{1}{2}$",
        "d) $\\frac{-5}{6} + x = -\\frac{2}{3}$",
        "e) $x + 0{,}25 = -\\frac{3}{4}$",
        "f) $1{,}5 - x = -\\frac{1}{2}$",
        "g) $x - \\left(-\\frac{3}{5}\\right) = \\frac{1}{2}$",
        "h) $-\\frac{4}{7} - x = \\frac{3}{14}$"
    ])
    
    # DẠNG 8
    add_heading_3(doc, "Dạng 8: Tìm x chứa phép nhân, phép chia và dấu ngoặc")
    add_body_paragraph(doc, "Thứ tự: Tìm cụm chứa $x$ trước (coi cụm trong ngoặc hoặc cụm nhân/chia là một ẩn phụ) $\\to$ Sau đó mới tìm $x$.", "★")
    
    add_exercise(doc, "8.1", "Tìm số hữu tỉ $x$, biết:", [
        "a) $\\frac{2}{3}x - \\frac{1}{2} = \\frac{5}{6}$",
        "b) $\\frac{3}{5}x + \\frac{1}{4} = -\\frac{7}{20}$",
        "c) $\\frac{1}{2} - \\frac{3}{4}x = \\frac{5}{8}$",
        "d) $\\left(x - \\frac{1}{2}\\right) : \\frac{3}{4} = -\\frac{2}{3}$",
        "e) $\\frac{4}{7} : x + \\frac{2}{3} = \\frac{5}{6}$",
        "f) $\\frac{1}{3} + \\frac{2}{3} : x = -1$",
        "g) $2\\left(x - \\frac{1}{3}\\right) + \\frac{1}{4} = \\frac{3}{2}$",
        "h) $\\frac{3}{4} - 2\\left(x + \\frac{1}{2}\\right) = -\\frac{1}{4}$"
    ])
    
    # DẠNG 9
    add_heading_3(doc, "Dạng 9: Tìm x ở số mũ hoặc cơ số luỹ thừa")
    add_body_paragraph(doc, "Phương pháp: \n- Tìm $x$ ở số mũ: Đưa hai vế về cùng cơ số $a^{f(x)} = a^n \\Rightarrow f(x) = n$ ($a \\neq 0, a \\neq \\pm 1$).\n- Tìm $x$ ở cơ số mũ chẵn: $x^2 = a^2 \\Rightarrow x = a$ hoặc $x = -a$.\n- Tìm $x$ ở cơ số mũ lẻ: $x^3 = a^3 \\Rightarrow x = a$.", "★")
    
    add_exercise(doc, "9.1 (Tìm x ở số mũ)", "Tìm số tự nhiên $x$, biết:", [
        "a) $2^x = 16$",
        "b) $3^{x + 1} = 27$",
        "c) $5^{2x - 1} = 125$",
        "d) $\\left(\\frac{1}{2}\\right)^x = \\frac{1}{32}$",
        "e) $\\left(-\\frac{2}{3}\\right)^x = \\frac{4}{9}$",
        "f) $\\left(-\\frac{3}{4}\\right)^{x + 2} = -\\frac{27}{64}$",
        "g) $2^{x + 1} + 2^x = 24$",
        "h) $3^{x + 2} - 3^x = 72$"
    ])
    
    add_exercise(doc, "9.2 (Tìm x ở cơ số)", "Tìm số hữu tỉ $x$, biết:", [
        "a) $x^2 = \\frac{4}{9}$",
        "b) $x^3 = -\\frac{8}{27}$",
        "c) $\\left(x - \\frac{1}{2}\\right)^2 = \\frac{1}{4}$",
        "d) $\\left(x + \\frac{2}{3}\\right)^2 = \\frac{25}{36}$",
        "e) $\\left(2x - \\frac{1}{3}\\right)^3 = -\\frac{1}{27}$",
        "f) $(x - 1)^4 = 16$"
    ])
    
    # DẠNG 10
    add_heading_3(doc, "Dạng 10: Tìm x trong biểu thức chứa giá trị tuyệt đối")
    add_body_paragraph(doc, "Công thức: Với $a > 0$:\n- $|A| = a \\Rightarrow A = a$ hoặc $A = -a$.\n- $|A| = 0 \\Rightarrow A = 0$.\n- $|A| < 0 \\Rightarrow$ Không có giá trị nào của $x$ thoả mãn (vô nghiệm).", "★")
    
    add_exercise(doc, "10.1", "Tìm số hữu tỉ $x$, biết:", [
        "a) $|x| = \\frac{3}{5}$",
        "b) $|x| = 1{,}25$",
        "c) $\\left|x - \\frac{1}{2}\\right| = \\frac{3}{4}$",
        "d) $\\left|x + \\frac{2}{3}\\right| = \\frac{1}{6}$",
        "e) $\\left|2x - \\frac{1}{3}\\right| = \\frac{5}{6}$",
        "f) $2|x - 1| - \\frac{1}{2} = \\frac{3}{2}$",
        "g) $|x + 2| + \\frac{3}{4} = \\frac{1}{2}$",
        "h) $\\left|x - \\frac{3}{4}\\right| = 0$"
    ])
    
    # DẠNG 11
    add_heading_3(doc, "Dạng 11: Căn bậc hai số học và số thực")
    add_body_paragraph(doc, "Kỹ năng cần nắm: \n- Căn bậc hai số học của số $a$ không âm là số $x$ không âm sao cho $x^2 = a$, kí hiệu là $\\sqrt{a}$.\n- Chú ý: $\\sqrt{a} \\ge 0$ với mọi $a \\ge 0$. Ví dụ $\\sqrt{25} = 5$ (không lấy $-5$).", "★")
    
    add_exercise(doc, "11.1", "Tính giá trị của các căn bậc hai số học sau:", [
        "a) $\\sqrt{16}$",
        "b) $\\sqrt{49}$",
        "c) $\\sqrt{81}$",
        "d) $\\sqrt{121}$",
        "e) $\\sqrt{\\frac{4}{25}}$",
        "f) $\\sqrt{\\frac{9}{64}}$",
        "g) $\\sqrt{0{,}36}$",
        "h) $\\sqrt{1{,}44}$"
    ])
    
    add_exercise(doc, "11.2", "Tìm $x$ biết:", [
        "a) $\\sqrt{x} = 4$",
        "b) $\\sqrt{x} = 9$",
        "c) $\\sqrt{x} = \\frac{2}{3}$",
        "d) $\\sqrt{x + 1} = 3$",
        "e) $\\sqrt{2x - 1} = 5$",
        "f) $2\\sqrt{x} - 6 = 0$"
    ])
    
    # ----------------------------- CHỦ ĐỀ 4 -----------------------------
    add_heading_2(doc, "D. HÌNH HỌC: GÓC Ở VỊ TRÍ ĐẶC BIỆT, TIA PHÂN GIÁC VÀ ĐƯỜNG THẲNG SONG SONG")
    
    # DẠNG 12
    add_heading_3(doc, "Dạng 12: Hai góc kề bù, hai góc đối đỉnh")
    add_body_paragraph(doc, "Định lý: \n- Hai góc đối đỉnh thì bằng nhau: $\\widehat{O}_1 = \\widehat{O}_3, \\widehat{O}_2 = \\widehat{O}_4$.\n- Hai góc kề bù có tổng số đo bằng $180^\\circ$: $\\widehat{A} + \\widehat{B} = 180^\\circ$.", "★")
    
    add_exercise(doc, "12.1", "Cho hai đường thẳng $xy$ và $zt$ cắt nhau tại $O$. Biết $\\widehat{xOz} = 50^\\circ$.", [
        "a) Tính số đo góc $\\widehat{yOt}$.",
        "b) Tính số đo góc $\\widehat{xOt}$ và $\\widehat{yOz}$."
    ])
    
    add_exercise(doc, "12.2", "Cho hai đường thẳng $AB$ và $CD$ cắt nhau tại $O$. Biết rằng $\\widehat{AOC} + \\widehat{BOD} = 140^\\circ$.", [
        "a) Tính số đo mỗi góc $\\widehat{AOC}$ và $\\widehat{BOD}$.",
        "b) Tính số đo góc $\\widehat{AOD}$ và $\\widehat{BOC}$."
    ])
    
    # DẠNG 13
    add_heading_3(doc, "Dạng 13: Tia phân giác của một góc")
    add_body_paragraph(doc, "Định nghĩa: Tia phân giác của một góc là tia nằm trong góc và tạo với hai cạnh của góc đó hai góc bằng nhau: $\\widehat{xOz} = \\widehat{yOz} = \\frac{\\widehat{xOy}}{2}$.", "★")
    
    add_exercise(doc, "13.1", "Cho góc $\\widehat{xOy} = 80^\\circ$. Vẽ tia $Oz$ là tia phân giác của góc $\\widehat{xOy}$.", [
        "a) Tính số đo các góc $\\widehat{xOz}$ và $\\widehat{yOz}$.",
        "b) Vẽ tia $Ot$ là tia đối của tia $Ox$. Tính số đo góc $\\widehat{zOt}$."
    ])
    
    add_exercise(doc, "13.2", "Cho hai góc kề bù $\\widehat{xOy}$ và $\\widehat{yOz}$, biết $\\widehat{xOy} = 120^\\circ$. Kẻ tia $Om$ là tia phân giác của góc $\\widehat{xOy}$, tia $On$ là tia phân giác của góc $\\widehat{yOz}$.", [
        "a) Tính số đo góc $\\widehat{yOz}$.",
        "b) Tính số đo góc $\\widehat{xOm}$ và $\\widehat{zOn}$.",
        "c) Chứng minh rằng tia $Om \\perp On$ (tức là $\\widehat{mOn} = 90^\\circ$)."
    ])
    
    # DẠNG 14
    add_heading_3(doc, "Dạng 14: Dấu hiệu nhận biết hai đường thẳng song song")
    add_body_paragraph(doc, "Dấu hiệu: Nếu đường thẳng $c$ cắt hai đường thẳng $a, b$ và trong các góc tạo thành có: \n- Một cặp góc so le trong bằng nhau; HOẶC\n- Một cặp góc đồng vị bằng nhau; HOẶC\n- Một cặp góc trong cùng phía bù nhau (tổng bằng $180^\\circ$)\nthì $a \\parallel b$.", "★")
    
    add_exercise(doc, "14.1", "Cho hình vẽ có đường thẳng $c$ cắt hai đường thẳng $a, b$ lần lượt tại $A$ và $B$. Biết $\\widehat{A}_1 = 60^\\circ$ và $\\widehat{B}_1 = 60^\\circ$ ở vị trí so le trong.", [
        "a) Chứng minh rằng $a \\parallel b$.",
        "b) Tính số đo các góc còn lại tại đỉnh $A$ và đỉnh $B$."
    ])
    
    add_exercise(doc, "14.2", "Cho góc nhọn $\\widehat{xOy}$. Trên tia $Ox$ lấy điểm $A$, trên tia $Oy$ lấy điểm $B$. Qua $A$ vẽ đường thẳng $d_1 \\perp Oy$. Qua $B$ vẽ đường thẳng $d_2 \\perp Oy$.", [
        "a) Chứng minh rằng $d_1 \\parallel d_2$.",
        "b) Nêu định lý (quan hệ từ vuông góc đến song song) được áp dụng ở câu a."
    ])
    
    # DẠNG 15
    add_heading_3(doc, "Dạng 15: Tính số đo góc dựa vào tính chất hai đường thẳng song song")
    add_body_paragraph(doc, "Tính chất: Cho $a \\parallel b$ và đường thẳng $c$ cắt $a, b$: \n- Hai góc so le trong bằng nhau.\n- Hai góc đồng vị bằng nhau.\n- Hai góc trong cùng phía bù nhau.", "★")
    
    add_exercise(doc, "15.1", "Cho $a \\parallel b$. Một đường thẳng $c$ cắt $a$ tại $A$ và cắt $b$ tại $B$ sao cho $\\widehat{A}_4 = 110^\\circ$.", [
        "a) Tính số đo góc $\\widehat{B}_2$ (so le trong với $\\widehat{A}_4$).",
        "b) Tính số đo góc $\\widehat{B}_4$ (đồng vị với $\\widehat{A}_4$).",
        "c) Tính số đo góc $\\widehat{B}_1$ (trong cùng phía với $\\widehat{A}_4$)."
    ])
    
    add_exercise(doc, "15.2 (Bài toán kẻ thêm đường song song)", "Cho hình vẽ có $Ax \\parallel By$. Điểm $O$ nằm giữa hai đường thẳng $Ax$ và $By$ sao cho $\\widehat{xAO} = 40^\\circ$ và $\\widehat{yBO} = 50^\\circ$ (tia $Ax, By$ cùng hướng).", [
        "a) Kẻ qua $O$ đường thẳng $Ot \\parallel Ax$. Chứng minh $Ot \\parallel By$.",
        "b) Tính số đo góc $\\widehat{AOB}$."
    ])
    
    # ----------------------------- CHỦ ĐỀ 5 -----------------------------
    add_heading_2(doc, "E. TOÁN THỰC TẾ HÌNH KHỐI VÀ BÀI TOÁN LẤY ĐIỂM 10")
    
    # DẠNG 16
    add_heading_3(doc, "Dạng 16: Bài toán thực tế diện tích xung quanh và thể tích hình khối")
    add_body_paragraph(doc, "Công thức: \n- Hình hộp chữ nhật: $S_{xq} = 2(a + b) \\cdot h$; $V = a \\cdot b \\cdot h$.\n- Hình lập phương cạnh $a$: $S_{xq} = 4a^2$; $V = a^3$.\n- Lăng trụ đứng: $S_{xq} = C_{đáy} \\cdot h$; $V = S_{đáy} \\cdot h$.", "★")
    
    add_exercise(doc, "16.1", "Một hồ bơi dạng hình hộp chữ nhật có chiều dài 25 m, chiều rộng 10 m và sâu 2 m.", [
        "a) Tính thể tích nước chứa đầy hồ bơi đó.",
        "b) Người ta lát gạch men xung quanh thành hồ và đáy hồ. Biết diện tích các mạch vữa không đáng kể, tính diện tích cần lát gạch men.",
        "c) Nếu chi phí lát gạch là 150 000 đồng/$\\text{m}^2$ thì tổng chi phí lát gạch là bao nhiêu?"
    ])
    
    add_exercise(doc, "16.2", "Một chiếc hộp quà hình lập phương có cạnh bằng 15 cm.", [
        "a) Tính thể tích của chiếc hộp quà đó.",
        "b) Người ta dùng giấy gói quà bọc kín toàn bộ 6 mặt của chiếc hộp. Tính diện tích giấy gói quà tối thiểu cần dùng (bỏ qua mép dán)."
    ])
    
    # DẠNG 17
    add_heading_3(doc, "Dạng 17: Bài toán vận dụng cao tìm GTLN, GTNN và dãy số phân số quy luật")
    add_body_paragraph(doc, "Phương pháp: \n- Vì $|A| \\ge 0$ nên $-|A| \\le 0$. Do đó $M = a + |A| \\ge a$ (GTNN là $a$ khi $A = 0$); $N = b - |A| \\le b$ (GTLN là $b$ khi $A = 0$).\n- Dãy phân số quy luật: $\\frac{1}{n(n + 1)} = \\frac{1}{n} - \\frac{1}{n + 1}$.", "★")
    
    add_exercise(doc, "17.1", "Tìm giá trị nhỏ nhất của các biểu thức sau:", [
        "a) $A = |x - 2| + 2026$",
        "b) $B = \\left|x + \\frac{3}{4}\\right| - 5$",
        "c) $C = (x - 3)^2 + |y + 1| + 10$"
    ])
    
    add_exercise(doc, "17.2", "Tìm giá trị lớn nhất của các biểu thức sau:", [
        "a) $P = 2027 - |x + 5|$",
        "b) $Q = 10 - \\left|2x - \\frac{1}{3}\\right|$"
    ])
    
    add_exercise(doc, "17.3", "Tính tổng các dãy phân số có quy luật sau:", [
        "a) $S_1 = \\frac{1}{1 \\cdot 2} + \\frac{1}{2 \\cdot 3} + \\frac{1}{3 \\cdot 4} + \\dots + \\frac{1}{99 \\cdot 100}$",
        "b) $S_2 = \\frac{1}{1 \\cdot 3} + \\frac{1}{3 \\cdot 5} + \\frac{1}{5 \\cdot 7} + \\dots + \\frac{1}{97 \\cdot 99}$"
    ])
    
    # =========================================================================
    # PHẦN II: BỘ 10 ĐỀ ÔN TẬP TỰ LUẬN 100% (60 PHÚT/ĐỀ)
    # =========================================================================
    add_heading_1(doc, "PHẦN II: BỘ 10 ĐỀ ÔN TẬP TỰ LUẬN 100% (THỜI GIAN LÀM BÀI: 60 PHÚT/ĐỀ)")
    
    # --- ĐỀ 1 ---
    add_test_header(doc, 1, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính (tính hợp lý nếu có thể):", [
        "a) $\\frac{-3}{7} + \\frac{5}{14} - \\frac{1}{2}$",
        "b) $\\frac{5}{9} \\cdot \\frac{7}{13} + \\frac{5}{9} \\cdot \\frac{6}{13}$",
        "c) $\\left(-\\frac{1}{2}\\right)^3 : \\frac{1}{4} + \\sqrt{25} - | -3 |$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số hữu tỉ $x$, biết:", [
        "a) $x + \\frac{3}{5} = \\frac{1}{10}$",
        "b) $\\frac{2}{3}x - \\frac{1}{2} = -\\frac{5}{6}$",
        "c) $\\left|x - \\frac{1}{3}\\right| = \\frac{2}{3}$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một căn phòng dạng hình hộp chữ nhật có chiều dài 6 m, chiều rộng 4 m và chiều cao 3 m. Người ta muốn sơn bốn bức tường bên trong căn phòng. Biết tổng diện tích các cửa là 8 $\\text{m}^2$. Tính diện tích cần sơn.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho góc nhọn $\\widehat{xOy} = 70^\\circ$. Trên tia $Ox$ lấy điểm $A$ ($A \\neq O$). Kẻ tia $Az$ nằm trong góc $\\widehat{xOy}$ sao cho $\\widehat{OAz} = 110^\\circ$.", [
        "a) Chứng minh rằng $Az \\parallel Oy$.",
        "b) Kẻ tia phân giác $Om$ của góc $\\widehat{xOy}$ và tia phân giác $An$ của góc $\\widehat{xAz}$. Chứng minh $Om \\parallel An$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $A = \\left|x - \\frac{2}{3}\\right| + 2026$.")
    
    # --- ĐỀ 2 ---
    add_test_header(doc, 2, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính (tính hợp lý nếu có thể):", [
        "a) $\\frac{2}{3} - \\frac{5}{6} + \\frac{1}{4}$",
        "b) $\\frac{-7}{15} \\cdot \\frac{8}{11} + \\frac{-7}{15} \\cdot \\frac{3}{11}$",
        "c) $\\left(-\\frac{2}{3}\\right)^2 - \\sqrt{\\frac{16}{81}} + |-0{,}5|$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số hữu tỉ $x$, biết:", [
        "a) $x - \\frac{1}{4} = -\\frac{5}{8}$",
        "b) $\\frac{3}{4} + \\frac{1}{4} : x = \\frac{1}{2}$",
        "c) $2^{x + 1} = 32$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một bể nước hình hộp chữ nhật có kích thước đáy là 2 m và 1{,}5 m; chiều cao bể là 1{,}2 m. Hiện bể đang chứa lượng nước bằng $\\frac{3}{4}$ thể tích bể. Tính số lít nước đang có trong bể (biết $1\\text{ m}^3 = 1000$ lít).")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hai đường thẳng $xx'$ và $yy'$ cắt nhau tại $O$. Biết góc $\\widehat{xOy} = 60^\\circ$.", [
        "a) Tính số đo các góc $\\widehat{x'Oy'}, \\widehat{xOy'}$ và $\\widehat{x'Oy}$.",
        "b) Vẽ tia phân giác $Ot$ của góc $\\widehat{xOy}$ và tia phân giác $Ot'$ của góc $\\widehat{x'Oy'}$. Chứng minh hai tia $Ot$ và $Ot'$ là hai tia đối nhau."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị lớn nhất của biểu thức: $B = 2027 - |2x + 1|$.")
    
    # --- ĐỀ 3 ---
    add_test_header(doc, 3, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $\\frac{-5}{12} + \\frac{4}{9} - \\frac{1}{4}$",
        "b) $\\frac{4}{7} \\cdot \\left(\\frac{-2}{5}\\right) + \\frac{4}{7} \\cdot \\left(-\\frac{3}{5}\\right)$",
        "c) $\\frac{2^7 \\cdot 9^3}{4^3 \\cdot 3^5}$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm $x$ biết:", [
        "a) $\\frac{2}{3} - x = \\frac{1}{6}$",
        "b) $\\left(x + \\frac{1}{2}\\right)^2 = \\frac{9}{16}$",
        "c) $\\left|x - \\frac{3}{5}\\right| = 0$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Bác Nam mua một chiếc tủ lạnh giá niêm yết là 8 000 000 đồng. Nhân dịp khuyến mãi, cửa hàng giảm giá 15%. Bác Nam có thẻ thành viên nên được giảm thêm 5% trên giá đã giảm. Hỏi bác Nam phải trả bao nhiêu tiền?")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hình vẽ có $a \\parallel b$. Đường thẳng $c$ cắt $a$ tại $A$ và cắt $b$ tại $B$. Cho biết $\\widehat{A}_1 = 75^\\circ$.", [
        "a) Tính số đo các góc còn lại tại đỉnh $A$.",
        "b) Tính số đo các góc tại đỉnh $B$ (nêu rõ các cặp góc so le trong, đồng vị, trong cùng phía)."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tính tổng: $S = \\frac{1}{1 \\cdot 2} + \\frac{1}{2 \\cdot 3} + \\frac{1}{3 \\cdot 4} + \\dots + \\frac{1}{99 \\cdot 100}$.")
    
    # --- ĐỀ 4 ---
    add_test_header(doc, 4, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $\\frac{-3}{8} \\cdot \\frac{4}{9} + \\frac{5}{6}$",
        "b) $\\frac{11}{19} \\cdot \\frac{-5}{7} + \\frac{11}{19} \\cdot \\frac{-2}{7} + \\frac{8}{19}$",
        "c) $\\sqrt{49} - \\left(-\\frac{1}{3}\\right)^2 \\cdot 9 + |-2{,}5|$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm $x$ biết:", [
        "a) $x + \\frac{4}{7} = -\\frac{3}{14}$",
        "b) $\\frac{3}{5}x + \\frac{1}{2} = -\\frac{1}{10}$",
        "c) $\\left|2x - \\frac{1}{4}\\right| = \\frac{3}{4}$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một khối bê tông hình lăng trụ đứng tam giác có chiều cao 2 m. Đáy là tam giác vuông có hai cạnh góc vuông lần lượt là 1{,}5 m và 2 m. Tính thể tích khối bê tông đó.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho góc $\\widehat{xOy} = 80^\\circ$. Lấy điểm $A$ trên tia $Ox$ ($A \\neq O$). Vẽ tia $Am$ sao cho $\\widehat{OAm} = 80^\\circ$ ($Am$ và $Oy$ cùng nằm trên một nửa mặt phẳng bờ chứa tia $Ox$).", [
        "a) Chứng minh rằng $Am \\parallel Oy$.",
        "b) Vẽ tia $An$ là tia đối của tia $Am$. Tính số đo góc $\\widehat{xAn}$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "So sánh: $2^{300}$ và $3^{200}$.")
    
    # --- ĐỀ 5 ---
    add_test_header(doc, 5, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính một cách hợp lý:", [
        "a) $\\frac{3}{7} + \\left(-\\frac{5}{2}\\right) + \\left(-\\frac{3}{5}\\right) + \\frac{4}{7}$",
        "b) $\\frac{5}{13} \\cdot \\frac{-8}{15} + \\frac{5}{13} \\cdot \\frac{-7}{15}$",
        "c) $\\left(\\frac{1}{3}\\right)^2 : \\left(\\frac{1}{3}\\right)^4 + \\sqrt{64} \\cdot \\frac{1}{2}$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm $x$ biết:", [
        "a) $x - \\frac{2}{3} = -\\frac{5}{6}$",
        "b) $3^{x - 1} = 81$",
        "c) $\\sqrt{x - 2} = 3$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một thùng đựng rác hình lập phương có cạnh 40 cm. Tính diện tích tôn cần dùng để làm chiếc thùng đó (thùng không có nắp đậy).")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hình vẽ có $AB \\parallel CD$. Biết $\\widehat{A} = 50^\\circ, \\widehat{C} = 60^\\circ$ và tia $AO, CO$ cắt nhau tại $O$ nằm giữa hai đường thẳng.", [
        "a) Kẻ đường thẳng qua $O$ song song với $AB$.",
        "b) Tính số đo góc $\\widehat{AOC}$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $M = |x - 1| + |x - 4|$.")
    
    # --- ĐỀ 6 ---
    add_test_header(doc, 6, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $\\frac{-2}{5} + \\frac{1}{4} - \\frac{3}{10}$",
        "b) $\\frac{3}{17} \\cdot \\frac{6}{11} + \\frac{3}{17} \\cdot \\frac{5}{11} - \\frac{3}{17}$",
        "c) $\\left(-\\frac{3}{4}\\right)^0 + \\sqrt{0{,}25} - \\left(-\\frac{1}{2}\\right)^2$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm $x$ biết:", [
        "a) $x + \\frac{1}{2} = -\\frac{3}{4}$",
        "b) $\\frac{2}{5}x - \\frac{1}{3} = \\frac{7}{15}$",
        "c) $\\left|x + \\frac{1}{2}\\right| = \\frac{3}{4}$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một bể cá cảnh bằng kính dạng hình hộp chữ nhật có chiều dài 80 cm, chiều rộng 50 cm và chiều cao 45 cm. Người ta đổ nước vào bể sao cho mực nước cao 35 cm. Tính thể tích nước trong bể theo đơn vị lít.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hai đường thẳng song song $a$ và $b$. Đường thẳng $c$ cắt $a$ tại $M$ và cắt $b$ tại $N$ sao cho $\\widehat{M}_1 = 120^\\circ$.", [
        "a) Tính số đo góc $\\widehat{N}_1$ (đồng vị với $\\widehat{M}_1$).",
        "b) Kẻ đường thẳng $d \\perp a$ tại $P$. Chứng minh rằng $d \\perp b$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "So sánh: $5^{300}$ và $3^{500}$.")
    
    # --- ĐỀ 7 ---
    add_test_header(doc, 7, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $\\frac{-5}{8} - \\frac{3}{4} + \\frac{7}{16}$",
        "b) $\\frac{8}{15} \\cdot \\frac{-4}{9} + \\frac{8}{15} \\cdot \\frac{-5}{9}$",
        "c) $\\frac{3^5 \\cdot 4^3}{12^3 \\cdot 2^2}$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm $x$ biết:", [
        "a) $\\frac{4}{7} - x = \\frac{1}{3}$",
        "b) $\\left(x - \\frac{2}{5}\\right)^2 = \\frac{9}{25}$",
        "c) $5^{x + 1} - 5^x = 100$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Bác Ba muốn rào xung quanh một khu đất hình chữ nhật có chiều dài 18 m và chiều rộng 12 m. Bác để lại một lối đi rộng 2 m không rào. Hỏi chiều dài hàng rào bác Ba cần làm là bao nhiêu mét?")
    add_exercise(doc, "4 (3,0 điểm)", "Cho góc $\\widehat{xOy} = 100^\\circ$. Vẽ tia $Oz$ nằm giữa hai tia $Ox, Oy$ sao cho $\\widehat{xOz} = 40^\\circ$.", [
        "a) Tính số đo góc $\\widehat{yOz}$.",
        "b) Vẽ tia $Ot$ là tia phân giác của góc $\\widehat{yOz}$. Tính số đo góc $\\widehat{xOt}$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị lớn nhất của: $P = 15 - \\left|x - \\frac{1}{2}\\right| - |y + 2|$.")
    
    # --- ĐỀ 8 ---
    add_test_header(doc, 8, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $\\frac{1}{4} + \\frac{-5}{6} - \\frac{-1}{3}$",
        "b) $\\frac{-2}{11} \\cdot \\frac{5}{7} + \\frac{-2}{11} \\cdot \\frac{9}{7} - \\frac{-2}{11}$",
        "c) $\\sqrt{100} - \\left(-\\frac{1}{2}\\right)^3 : \\frac{1}{8} + |-3{,}2|$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm $x$ biết:", [
        "a) $x - \\frac{3}{4} = -\\frac{1}{8}$",
        "b) $\\frac{1}{2} - \\frac{2}{3}x = \\frac{5}{6}$",
        "c) $\\left|x - \\frac{1}{4}\\right| = 0$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một chiếc lều cắm trại dạng hình lăng trụ đứng tam giác có chiều dài lều 3 m. Mặt trước lều là tam giác cân có cạnh đáy 2 m và chiều cao tương ứng 1{,}5 m. Tính thể tích không gian bên trong chiếc lều.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hai đường thẳng $a$ và $b$ song song với nhau. Đường thẳng $c$ cắt $a, b$ lần lượt tại $A$ và $B$. Biết $\\widehat{A}_2 = 50^\\circ$ (góc nhọn).", [
        "a) Tính số đo các góc còn lại tại đỉnh $A$.",
        "b) Tính số đo các góc tại đỉnh $B$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm $x, y$ biết: $(x - 1)^2 + |y + 2| = 0$.")
    
    # --- ĐỀ 9 ---
    add_test_header(doc, 9, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $\\frac{-3}{10} + \\frac{7}{15} - \\frac{1}{6}$",
        "b) $\\frac{7}{12} \\cdot \\frac{-3}{8} + \\frac{7}{12} \\cdot \\frac{-5}{8}$",
        "c) $\\left(-\\frac{2}{5}\\right)^2 : \\frac{4}{25} + \\sqrt{81} - 10$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm $x$ biết:", [
        "a) $x + \\frac{2}{5} = -\\frac{3}{10}$",
        "b) $\\left(x - \\frac{1}{3}\\right)^3 = -\\frac{8}{27}$",
        "c) $\\sqrt{2x + 1} = 5$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một khối gỗ hình hộp chữ nhật có chiều dài 12 cm, chiều rộng 8 cm và chiều cao 5 cm. Người ta sơn tất cả các mặt của khối gỗ đó. Tính diện tích cần sơn.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho góc $\\widehat{xOy} = 120^\\circ$. Vẽ tia $Ot$ là tia phân giác của góc $\\widehat{xOy}$.", [
        "a) Tính số đo góc $\\widehat{xOt}$ và $\\widehat{yOt}$.",
        "b) Trên nửa mặt phẳng bờ chứa tia $Ox$ có chứa tia $Oy$, vẽ tia $Om \\perp Ox$. Chứng minh $Om$ là tia phân giác của góc $\\widehat{yOt}$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tính giá trị biểu thức: $A = \\frac{1}{1 \\cdot 3} + \\frac{1}{3 \\cdot 5} + \\frac{1}{5 \\cdot 7} + \\dots + \\frac{1}{99 \\cdot 101}$.")
    
    # --- ĐỀ 10 ---
    add_test_header(doc, 10, "7")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính một cách hợp lý:", [
        "a) $\\frac{4}{13} + \\frac{-5}{11} + \\frac{9}{13} + \\frac{-6}{11}$",
        "b) $\\frac{5}{8} \\cdot \\frac{-3}{7} + \\frac{5}{8} \\cdot \\frac{-4}{7}$",
        "c) $\\sqrt{144} - \\left(-\\frac{1}{2}\\right)^4 \\cdot 16 + | -5 |$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số hữu tỉ $x$, biết:", [
        "a) $x - \\frac{5}{6} = \\frac{1}{3}$",
        "b) $\\frac{3}{4}x + \\frac{1}{2} = -\\frac{1}{4}$",
        "c) $\\left|x - \\frac{2}{5}\\right| = \\frac{3}{5}$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một lớp học có 40 học sinh. Trong đợt kiểm tra giữa học kỳ 1, số học sinh đạt điểm Giỏi chiếm $\\frac{2}{5}$ số học sinh cả lớp. Số học sinh đạt điểm Khá bằng $\\frac{3}{4}$ số học sinh còn lại. Tính số học sinh đạt điểm Khá và số học sinh còn lại (Đạt).")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hai đường thẳng $a$ và $b$ cùng vuông góc với đường thẳng $c$ lần lượt tại $A$ và $B$.", [
        "a) Chứng minh rằng $a \\parallel b$.",
        "b) Một đường thẳng $d$ cắt $a, b$ lần lượt tại $C$ và $D$ sao cho $\\widehat{C}_1 = 70^\\circ$ (góc nhọn). Tính các góc còn lại tại đỉnh $C$ và $D$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Cho hai số thực $x, y$ thoả mãn $|x - 2026| + |y - 2027| \\le 0$. Tính giá trị của biểu thức $P = x + y$.")
    
    # =========================================================================
    # PHẦN III: BẢNG ĐÁP SỐ VÀ HƯỚNG DẪN GIẢI 10 ĐỀ TỰ LUẬN
    # =========================================================================
    add_heading_1(doc, "PHẦN III: BẢNG ĐÁP SỐ VÀ HƯỚNG DẪN GIẢI 10 ĐỀ TỰ LUẬN")
    
    # Đề 1
    add_answer_header(doc, 1)
    for _ans in [
        "Bài 1: a) Mẫu chung 14: $\\frac{-6 + 5 - 7}{14} = \\frac{-8}{14} = -\\frac{4}{7}$; b) $\\frac{5}{9} \\left(\\frac{7}{13} + \\frac{6}{13}\\right) = \\frac{5}{9} \\cdot 1 = \\frac{5}{9}$; c) $-\\frac{1}{8} \\cdot 4 + 5 - 3 = -\\frac{1}{2} + 2 = \\frac{3}{2}$.",
        "Bài 2: a) $x = \\frac{1}{10} - \\frac{3}{5} = -\\frac{1}{2}$; b) $\\frac{2}{3}x = -\\frac{5}{6} + \\frac{1}{2} = -\\frac{1}{3} \\Rightarrow x = -\\frac{1}{2}$; c) $x - \\frac{1}{3} = \\frac{2}{3} \\Rightarrow x = 1$ hoặc $x - \\frac{1}{3} = -\\frac{2}{3} \\Rightarrow x = -\\frac{1}{3}$.",
        "Bài 3: Diện tích xung quanh: $S_{xq} = 2(6 + 4) \\cdot 3 = 60\\text{ m}^2$. Diện tích cần sơn là $60 - 8 = 52\\text{ m}^2$.",
        "Bài 4: a) Hai góc $\\widehat{xOy} = 70^\\circ$ và $\\widehat{OAz} = 110^\\circ$ ở vị trí trong cùng phía có tổng bằng $180^\\circ$ nên $Az \\parallel Oy$; b) $\\widehat{xOm} = 35^\\circ, \\widehat{xAn} = 35^\\circ$ ở vị trí đồng vị nên $Om \\parallel An$.",
        "Bài 5: Vì $\\left|x - \\frac{2}{3}\\right| \\ge 0$ nên $A \\ge 2026$. Dấu bằng xảy ra khi $x = \\frac{2}{3}$. Vậy GTNN là 2026."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 2
    add_answer_header(doc, 2)
    for _ans in [
        "Bài 1: a) Mẫu chung 12: $\\frac{8 - 10 + 3}{12} = \\frac{1}{12}$; b) $\\frac{-7}{15} \\left(\\frac{8}{11} + \\frac{3}{11}\\right) = -\\frac{7}{15} \\cdot 1 = -\\frac{7}{15}$; c) $\\frac{4}{9} - \\frac{4}{9} + 0{,}5 = 0{,}5 = \\frac{1}{2}$.",
        "Bài 2: a) $x = -\\frac{5}{8} + \\frac{1}{4} = -\\frac{3}{8}$; b) $\\frac{1}{4} : x = \\frac{1}{2} - \\frac{3}{4} = -\\frac{1}{4} \\Rightarrow x = -1$; c) $2^{x + 1} = 2^5 \\Rightarrow x + 1 = 5 \\Rightarrow x = 4$.",
        "Bài 3: Thể tích bể: $V = 2 \\cdot 1{,}5 \\cdot 1{,}2 = 3{,}6\\text{ m}^3 = 3600$ lít. Số lít nước hiện có: $3600 \\cdot \\frac{3}{4} = 2700$ lít.",
        "Bài 4: a) $\\widehat{x'Oy'} = 60^\\circ$ (đối đỉnh); $\\widehat{xOy'} = \\widehat{x'Oy} = 180^\\circ - 60^\\circ = 120^\\circ$ (kề bù); b) $\\widehat{tOy} + \\widehat{yOx'} + \\widehat{x'Ot'} = 30^\\circ + 120^\\circ + 30^\\circ = 180^\\circ$ nên $Ot, Ot'$ là hai tia đối nhau.",
        "Bài 5: Vì $|2x + 1| \\ge 0$ nên $B \\le 2027$. GTLN là 2027 khi $x = -0{,}5$."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 3
    add_answer_header(doc, 3)
    for _ans in [
        "Bài 1: a) Mẫu chung 36: $\\frac{-15 + 16 - 9}{36} = -\\frac{8}{36} = -\\frac{2}{9}$; b) $\\frac{4}{7} \\left(-\\frac{2}{5} - \\frac{3}{5}\\right) = \\frac{4}{7} (-1) = -\\frac{4}{7}$; c) $\\frac{2^7 \\cdot 3^6}{2^6 \\cdot 3^5} = 2 \\cdot 3 = 6$.",
        "Bài 2: a) $x = \\frac{2}{3} - \\frac{1}{6} = \\frac{1}{2}$; b) $x + \\frac{1}{2} = \\pm \\frac{3}{4} \\Rightarrow x = \\frac{1}{4}$ hoặc $x = -\\frac{5}{4}$; c) $x = \\frac{3}{5}$.",
        "Bài 3: Giá sau lần giảm 1: $8000000 \\cdot 0{,}85 = 6800000$ đồng. Giá phải trả sau giảm lần 2: $6800000 \\cdot 0{,}95 = 6460000$ đồng.",
        "Bài 4: a) $\\widehat{A}_3 = 75^\\circ$ (đối đỉnh), $\\widehat{A}_2 = \\widehat{A}_4 = 180^\\circ - 75^\\circ = 105^\\circ$ (kề bù); b) Vì $a \\parallel b$ nên góc so le trong $\\widehat{B}_3 = \\widehat{A}_1 = 75^\\circ$; đồng vị $\\widehat{B}_1 = \\widehat{A}_1 = 75^\\circ$; trong cùng phía $\\widehat{B}_2 = 180^\\circ - 75^\\circ = 105^\\circ$.",
        "Bài 5: $S = 1 - \\frac{1}{2} + \\frac{1}{2} - \\frac{1}{3} + \\dots + \\frac{1}{99} - \\frac{1}{100} = 1 - \\frac{1}{100} = \\frac{99}{100}$."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 4
    add_answer_header(doc, 4)
    for _ans in [
        "Bài 1: a) $-\\frac{1}{6} + \\frac{5}{6} = \\frac{4}{6} = \\frac{2}{3}$; b) $\\frac{11}{19} \\left(-\\frac{5}{7} - \\frac{2}{7}\\right) + \\frac{8}{19} = -\\frac{11}{19} + \\frac{8}{19} = -\\frac{3}{19}$; c) $7 - 1 + 2{,}5 = 8{,}5$.",
        "Bài 2: a) $x = -\\frac{3}{14} - \\frac{4}{7} = -\\frac{11}{14}$; b) $\\frac{3}{5}x = -\\frac{1}{10} - \\frac{1}{2} = -\\frac{3}{5} \\Rightarrow x = -1$; c) $2x - \\frac{1}{4} = \\pm \\frac{3}{4} \\Rightarrow x = \\frac{1}{2}$ hoặc $x = -\\frac{1}{4}$.",
        "Bài 3: Diện tích đáy: $S_{đáy} = \\frac{1}{2} \\cdot 1{,}5 \\cdot 2 = 1{,}5\\text{ m}^2$. Thể tích: $V = S_{đáy} \\cdot h = 1{,}5 \\cdot 2 = 3\\text{ m}^3$.",
        "Bài 4: a) Hai góc $\\widehat{xOy} = 80^\\circ$ và $\\widehat{OAm} = 80^\\circ$ ở vị trí so le trong bằng nhau nên $Am \\parallel Oy$; b) $\\widehat{xAn} = 180^\\circ - 80^\\circ = 100^\\circ$ (kề bù).",
        "Bài 5: $2^{300} = (2^3)^{100} = 8^{100}$; $3^{200} = (3^2)^{100} = 9^{100}$. Vì $8 < 9$ nên $2^{300} < 3^{200}$."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 5
    add_answer_header(doc, 5)
    for _ans in [
        "Bài 1: a) Nhóm $\\left(\\frac{3}{7} + \\frac{4}{7}\\right) + \\left(-\\frac{5}{2} - \\frac{3}{5}\\right) = 1 - \\frac{31}{10} = -\\frac{21}{10}$; b) $\\frac{5}{13} \\left(-\\frac{8}{15} - \\frac{7}{15}\\right) = -\\frac{5}{13}$; c) $3^2 + 8 \\cdot 0{,}5 = 9 + 4 = 13$.",
        "Bài 2: a) $x = -\\frac{5}{6} + \\frac{2}{3} = -\\frac{1}{6}$; b) $3^{x - 1} = 3^4 \\Rightarrow x - 1 = 4 \\Rightarrow x = 5$; c) $x - 2 = 9 \\Rightarrow x = 11$.",
        "Bài 3: Thùng không nắp có 5 mặt. Diện tích 1 mặt: $40^2 = 1600\\text{ cm}^2$. Diện tích tôn cần dùng: $1600 \\times 5 = 8000\\text{ cm}^2 = 0{,}8\\text{ m}^2$.",
        "Bài 4: a) Kẻ $Ot \\parallel AB \\Rightarrow Ot \\parallel CD$; b) $\\widehat{AOt} = \\widehat{A} = 50^\\circ$ (so le trong), $\\widehat{COt} = \\widehat{C} = 60^\\circ$ (so le trong) $\\Rightarrow \\widehat{AOC} = 50^\\circ + 60^\\circ = 110^\\circ$.",
        "Bài 5: $M = |x - 1| + |4 - x| \\ge |x - 1 + 4 - x| = 3$. Dấu bằng khi $1 \\le x \\le 4$. Vậy GTNN là 3."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 6
    add_answer_header(doc, 6)
    for _ans in [
        "Bài 1: a) Mẫu chung 20: $\\frac{-8 + 5 - 6}{20} = -\\frac{9}{20}$; b) $\\frac{3}{17} \\left(\\frac{6}{11} + \\frac{5}{11} - 1\\right) = \\frac{3}{17} \\cdot 0 = 0$; c) $1 + 0{,}5 - 0{,}25 = 1{,}25 = \\frac{5}{4}$.",
        "Bài 2: a) $x = -\\frac{3}{4} - \\frac{1}{2} = -\\frac{5}{4}$; b) $\\frac{2}{5}x = \\frac{7}{15} + \\frac{1}{3} = \\frac{12}{15} = \\frac{4}{5} \\Rightarrow x = 2$; c) $x + \\frac{1}{2} = \\pm \\frac{3}{4} \\Rightarrow x = \\frac{1}{4}$ hoặc $x = -\\frac{5}{4}$.",
        "Bài 3: Thể tích nước: $V = 80 \\times 50 \\times 35 = 140000\\text{ cm}^3 = 140$ lít.",
        "Bài 4: a) Hai góc đồng vị bằng nhau nên $\\widehat{N}_1 = 120^\\circ$; b) Vì $a \\parallel b$ mà $d \\perp a$ nên $d \\perp b$ (quan hệ từ vuông góc đến song song).",
        "Bài 5: $5^{300} = (5^3)^{100} = 125^{100}$; $3^{500} = (3^5)^{100} = 243^{100}$. Vì $125 < 243$ nên $5^{300} < 3^{500}$."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 7
    add_answer_header(doc, 7)
    for _ans in [
        "Bài 1: a) Mẫu chung 16: $\\frac{-10 - 12 + 7}{16} = -\\frac{15}{16}$; b) $\\frac{8}{15} \\left(-\\frac{4}{9} - \\frac{5}{9}\\right) = -\\frac{8}{15}$; c) $\\frac{3^5 \\cdot 2^6}{3^3 \\cdot 2^6 \\cdot 2^2} = \\frac{3^2}{4} = \\frac{9}{4}$.",
        "Bài 2: a) $x = \\frac{4}{7} - \\frac{1}{3} = \\frac{5}{21}$; b) $x - \\frac{2}{5} = \\pm \\frac{3}{5} \\Rightarrow x = 1$ hoặc $x = -\\frac{1}{5}$; c) $5^x(5 - 1) = 100 \\Rightarrow 5^x \\cdot 4 = 100 \\Rightarrow 5^x = 25 \\Rightarrow x = 2$.",
        "Bài 3: Chu vi khu đất: $2(18 + 12) = 60$ m. Chiều dài hàng rào: $60 - 2 = 58$ m.",
        "Bài 4: a) $\\widehat{yOz} = 100^\\circ - 40^\\circ = 60^\\circ$; b) $\\widehat{zOt} = 30^\\circ \\Rightarrow \\widehat{xOt} = 40^\\circ + 30^\\circ = 70^\\circ$.",
        "Bài 5: Vì $\\left|x - \\frac{1}{2}\\right| \\ge 0$ và $|y + 2| \\ge 0$ nên $P \\le 15$. GTLN là 15 khi $x = 0{,}5, y = -2$."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 8
    add_answer_header(doc, 8)
    for _ans in [
        "Bài 1: a) Mẫu chung 12: $\\frac{3 - 10 + 4}{12} = -\\frac{3}{12} = -\\frac{1}{4}$; b) $-\\frac{2}{11} \\left(\\frac{5}{7} + \\frac{9}{7} - 1\\right) = -\\frac{2}{11} \\cdot 1 = -\\frac{2}{11}$; c) $10 - (-1) + 3{,}2 = 14{,}2$.",
        "Bài 2: a) $x = -\\frac{1}{8} + \\frac{3}{4} = \\frac{5}{8}$; b) $\\frac{2}{3}x = \\frac{1}{2} - \\frac{5}{6} = -\\frac{1}{3} \\Rightarrow x = -\\frac{1}{2}$; c) $x = \\frac{1}{4}$.",
        "Bài 3: Diện tích mặt đáy: $S = \\frac{1}{2} \\cdot 2 \\cdot 1{,}5 = 1{,}5\\text{ m}^2$. Thể tích chiếc lều: $V = S \\cdot h = 1{,}5 \\cdot 3 = 4{,}5\\text{ m}^3$.",
        "Bài 4: a) $\\widehat{A}_4 = 50^\\circ$ (đối đỉnh), $\\widehat{A}_1 = \\widehat{A}_3 = 130^\\circ$ (kề bù); b) Các góc so le trong bằng $50^\\circ$, đồng vị bằng $50^\\circ$ và các góc bù bằng $130^\\circ$.",
        "Bài 5: Tổng hai biểu thức không âm bằng 0 khi và chỉ khi cả hai cùng bằng 0: $x = 1, y = -2$."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 9
    add_answer_header(doc, 9)
    for _ans in [
        "Bài 1: a) Mẫu chung 30: $\\frac{-9 + 14 - 5}{30} = 0$; b) $\\frac{7}{12} \\left(-\\frac{3}{8} - \\frac{5}{8}\\right) = -\\frac{7}{12}$; c) $1 + 9 - 10 = 0$.",
        "Bài 2: a) $x = -\\frac{3}{10} - \\frac{2}{5} = -\\frac{7}{10}$; b) $x - \\frac{1}{3} = -\\frac{2}{3} \\Rightarrow x = -\\frac{1}{3}$; c) $2x + 1 = 25 \\Rightarrow 2x = 24 \\Rightarrow x = 12$.",
        "Bài 3: Diện tích toàn phần khối gỗ: $2(12 \\cdot 8 + 12 \\cdot 5 + 8 \\cdot 5) = 2(96 + 60 + 40) = 392\\text{ cm}^2$.",
        "Bài 4: a) $\\widehat{xOt} = \\widehat{yOt} = 60^\\circ$; b) $\\widehat{xOm} = 90^\\circ \\Rightarrow \\widehat{tOm} = 90^\\circ - 60^\\circ = 30^\\circ$, $\\widehat{yOm} = 120^\\circ - 90^\\circ = 30^\\circ$. Vì $\\widehat{tOm} = \\widehat{yOm} = 30^\\circ$ nên $Om$ là tia phân giác của $\\widehat{yOt}$.",
        "Bài 5: $2A = \\frac{2}{1 \\cdot 3} + \\frac{2}{3 \\cdot 5} + \\dots + \\frac{2}{99 \\cdot 101} = 1 - \\frac{1}{101} = \\frac{100}{101} \\Rightarrow A = \\frac{50}{101}$."
    ]:
        add_answer_item(doc, _ans)
        
    # Đề 10
    add_answer_header(doc, 10)
    for _ans in [
        "Bài 1: a) $\\left(\\frac{4}{13} + \\frac{9}{13}\\right) + \\left(-\\frac{5}{11} - \\frac{6}{11}\\right) = 1 - 1 = 0$; b) $\\frac{5}{8} \\left(-\\frac{3}{7} - \\frac{4}{7}\\right) = -\\frac{5}{8}$; c) $12 - 1 + 5 = 16$.",
        "Bài 2: a) $x = \\frac{1}{3} + \\frac{5}{6} = \\frac{7}{6}$; b) $\\frac{3}{4}x = -\\frac{1}{4} - \\frac{1}{2} = -\\frac{3}{4} \\Rightarrow x = -1$; c) $x - \\frac{2}{5} = \\pm \\frac{3}{5} \\Rightarrow x = 1$ hoặc $x = -\\frac{1}{5}$.",
        "Bài 3: Số học sinh Giỏi: $40 \\cdot \\frac{2}{5} = 16$ học sinh. Số học sinh còn lại: $40 - 16 = 24$ học sinh. Số học sinh Khá: $24 \\cdot \\frac{3}{4} = 18$ học sinh. Số học sinh Đạt: $24 - 18 = 6$ học sinh.",
        "Bài 4: a) Hai đường thẳng $a$ và $b$ cùng vuông góc với $c$ nên $a \\parallel b$; b) Các cặp góc so le trong bằng $70^\\circ$, đồng vị bằng $70^\\circ$, các góc kề bù bằng $180^\\circ - 70^\\circ = 110^\\circ$.",
        "Bài 5: Vì tổng hai giá trị tuyệt đối không âm mà nhỏ hơn hoặc bằng 0 nên bắt buộc phải bằng 0 $\\Rightarrow x = 2026$ và $y = 2027$. Vậy $P = 2026 + 2027 = 4053$."
    ]:
        add_answer_item(doc, _ans)

    doc.save(output_path)
    print(f"[TOAN 7 - 2026-2027] Saved successfully to: {output_path}")

if __name__ == "__main__":
    import datetime
    today = datetime.datetime.now().strftime("%d.%m")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "2_TAO_BAI_TAP", "Ket_qua", today)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "De_Cuong_On_Tap_Giua_HK1_Toan_7.docx")
    build_de_cuong_toan_7(out_file)
