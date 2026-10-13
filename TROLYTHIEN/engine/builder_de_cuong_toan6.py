# -*- coding: utf-8 -*-
"""
BIÊN SOẠN ĐỀ CƯƠNG ÔN TẬP GIỮA HỌC KỲ I - TOÁN 6 (PHIÊN BẢN ĐẠI BẢNG RÈN LUYỆN)
NĂM HỌC: 2026 - 2027 (Trường THCS Trần Phú - Tổ Toán - Tin)
TẬP TRUNG TỐI ĐA:
1. Ngân hàng bài tập rèn kỹ năng thực chiến đồ sộ cho học sinh yếu, trung bình.
2. Bộ 10 Đề ôn tập tự luận 100% (thời gian làm bài: 60 phút/đề).
3. 100% Công thức toán là Microsoft Word Equation (OMML m:oMath, chuẩn Overbar m:bar).
"""

import os
from docx.shared import Inches, Pt, RGBColor
from de_cuong_docx_helper import (
    create_base_document, add_header_quoc_hieu, add_heading_1, add_heading_2,
    add_heading_3, add_body_paragraph, add_exercise, add_test_header, add_answer_header, add_answer_item
)

def build_de_cuong_toan_6(output_path):
    doc = create_base_document()
    add_header_quoc_hieu(doc, "6", school_year="2026 - 2027")
    
    # ==================== PHẦN I ====================
    add_heading_1(doc, "PHẦN I: HỆ THỐNG BÀI TẬP RÈN KỸ NĂNG CƠ BẢN (DÀNH CHO HỌC SINH YẾU & TRUNG BÌNH)")
    
    # DẠNG 1
    add_heading_2(doc, "Dạng 1: Tập hợp, phần tử và đếm số phần tử của tập hợp")
    add_body_paragraph(doc, "Quy tắc: Liệt kê phần tử trong ngoặc nhọn { }, cách nhau bởi dấu chấm phẩy (;). Kí hiệu thuộc $\\in$, không thuộc $\\notin$. Số phần tử dãy cách đều = (Số cuối - Số đầu) : khoảng cách + 1. Tổng dãy = (Số đầu + Số cuối) · (Số phần tử) : 2.", "★")
    
    add_exercise(doc, "1.1", "Viết các tập hợp sau bằng cách liệt kê các phần tử:", [
        "a) $A = \\{x \\in \\mathbb{N} \\mid 5 < x < 12\\}$",
        "b) $B = \\{x \\in \\mathbb{N} \\mid 18 \\le x \\le 25\\}$",
        "c) $C = \\{x \\in \\mathbb{N}^* \\mid x < 8\\}$",
        "d) $D = \\{x \\in \\mathbb{N} \\mid 30 < x \\le 36\\}$"
    ])
    
    add_exercise(doc, "1.2", "Cho tập hợp $M = \\{3; 7; 11; 15; 19\\}$. Điền kí hiệu thích hợp ($\\in$ hoặc $\\notin$) vào chỗ chấm:", [
        "a) $3 \\dots M$",
        "b) $5 \\dots M$",
        "c) $15 \\dots M$",
        "d) $21 \\dots M$"
    ])
    
    add_exercise(doc, "1.3", "Tính số phần tử của mỗi tập hợp sau:", [
        "a) $A = \\{12; 14; 16; 18; \\dots; 98\\}$",
        "b) $B = \\{21; 23; 25; 27; \\dots; 105\\}$",
        "c) $C = \\{10; 15; 20; 25; \\dots; 250\\}$",
        "d) $D = \\{1; 2; 3; 4; \\dots; 2026\\}$",
        "e) $E = \\{x \\in \\mathbb{N}^* \\mid x \\le 150\\}$"
    ])
    
    add_exercise(doc, "1.4", "Tính tổng các phần tử của các tập hợp sau:", [
        "a) Tổng các số tự nhiên liên tiếp từ 1 đến 100: $S_1 = 1 + 2 + 3 + \\dots + 100$",
        "b) Tổng các số tự nhiên chẵn từ 2 đến 80: $S_2 = 2 + 4 + 6 + \\dots + 80$",
        "c) Tổng các số tự nhiên lẻ từ 1 đến 99: $S_3 = 1 + 3 + 5 + \\dots + 99$"
    ])

    # DẠNG 2
    add_heading_2(doc, "Dạng 2: Phép tính số tự nhiên — Tính nhanh, tính hợp lý")
    add_body_paragraph(doc, "Quy tắc: Ghép cặp tạo số tròn chục, tròn trăm: $a + b = b + a$. Phân phối: $a \\cdot b + a \\cdot c = a \\cdot (b + c)$; $a \\cdot b - a \\cdot c = a \\cdot (b - c)$. Các tích đẹp cần nhớ: $4 \\cdot 25 = 100$; $8 \\cdot 125 = 1000$; $2 \\cdot 50 = 100$; $5 \\cdot 20 = 100$.", "★")
    
    add_exercise(doc, "2.1", "Tính một cách hợp lý nhất:", [
        "a) $46 + 128 + 54 + 72$",
        "b) $135 + 79 + 65 + 121$",
        "c) $38 + 145 + 62 + 55$",
        "d) $74 + 185 + 26 + 115$",
        "e) $58 + 247 + 42 + 153$",
        "f) $83 + 365 + 17 + 135$",
        "g) $67 + 158 + 33 + 42$",
        "h) $142 + 258 + 58 + 42$"
    ])
    
    add_exercise(doc, "2.2", "Tính nhanh:", [
        "a) $4 \\cdot 37 \\cdot 25$",
        "b) $125 \\cdot 19 \\cdot 8$",
        "c) $25 \\cdot 49 \\cdot 4$",
        "d) $8 \\cdot 27 \\cdot 125$",
        "e) $50 \\cdot 18 \\cdot 2$",
        "f) $5 \\cdot 36 \\cdot 20$"
    ])
    
    add_exercise(doc, "2.3", "Tính hợp lý bằng cách đặt thừa số chung:", [
        "a) $28 \\cdot 76 + 28 \\cdot 24$",
        "b) $45 \\cdot 63 + 45 \\cdot 37$",
        "c) $36 \\cdot 85 + 15 \\cdot 36$",
        "d) $64 \\cdot 35 + 65 \\cdot 64$",
        "e) $52 \\cdot 84 + 16 \\cdot 52$",
        "f) $43 \\cdot 76 + 43 \\cdot 24$",
        "g) $128 \\cdot 67 + 33 \\cdot 128$",
        "h) $84 \\cdot 45 + 55 \\cdot 84$"
    ])
    
    add_exercise(doc, "2.4", "Tính hợp lý:", [
        "a) $135 \\cdot 84 - 135 \\cdot 74 + 350$",
        "b) $27 \\cdot 64 + 27 \\cdot 36 - 500$",
        "c) $45 \\cdot 78 + 45 \\cdot 22 - 350$",
        "d) $17 \\cdot 85 + 15 \\cdot 17 - 200$",
        "e) $35 \\cdot 118 - 35 \\cdot 18 + 500$",
        "f) $67 \\cdot 54 + 46 \\cdot 67 - 700$"
    ])

    # DẠNG 3
    add_heading_2(doc, "Dạng 3: Thực hiện phép tính có lũy thừa và thứ tự dấu ngoặc")
    add_body_paragraph(doc, "Quy tắc: Các giá trị lũy thừa cần thuộc làu: $2^2 = 4, 2^3 = 8, 2^4 = 16, 2^5 = 32$; $3^2 = 9, 3^3 = 27, 3^4 = 81$; $4^2 = 16, 4^3 = 64$; $5^2 = 25, 5^3 = 125$. Quy ước: $a^0 = 1$ ($a \\neq 0$). Thứ tự: tính lũy thừa trước $\\to$ nhân chia $\\to$ cộng trừ; trong ngoặc tròn ( ) $\\to$ ngoặc vuông [ ] $\\to$ ngoặc nhọn { }.", "★")
    
    add_exercise(doc, "3.1", "Thực hiện phép tính:", [
        "a) $3 \\cdot 5^2 - 16 : 2^2$",
        "b) $2^3 \\cdot 17 - 2^3 \\cdot 14$",
        "c) $4^2 \\cdot 5 - 3 \\cdot 2^3$",
        "d) $5 \\cdot 2^3 + 3 \\cdot 4^2$",
        "e) $6^2 : 9 + 50 : 5^2$",
        "f) $75 - (3 \\cdot 5^2 - 4 \\cdot 2^3)$",
        "g) $3^3 \\cdot 2 - 2^4 : 4$",
        "h) $10^2 - 3 \\cdot 2^4 + 2026^0$"
    ])
    
    add_exercise(doc, "3.2", "Thực hiện phép tính:", [
        "a) $100 : [45 - (18 - 3 \\cdot 5)^2]$",
        "b) $120 : [45 - (17 - 3 \\cdot 4)^2]$",
        "c) $80 : [35 - (15 - 2 \\cdot 6)^2]$",
        "d) $160 : [25 - (18 - 7 \\cdot 2)^2]$",
        "e) $200 : [119 - (25 - 2 \\cdot 3)]$",
        "f) $150 : [28 - (16 - 3 \\cdot 4)^2]$",
        "g) $90 : [24 - (15 - 3 \\cdot 3)^2]$",
        "h) $180 : [45 - (18 - 3 \\cdot 5)^2]$"
    ])
    
    add_exercise(doc, "3.3", "Thực hiện phép tính:", [
        "a) $140 : [35 - (16 - 3 \\cdot 4)^2]$",
        "b) $120 : [54 - (18 - 4 \\cdot 3)^2]$",
        "c) $80 - [130 - (12 - 4)^2]$",
        "d) $150 - [10^2 - (14 - 11)^2 \\cdot 2026^0]$",
        "e) $480 : [75 + (7^2 - 8 \\cdot 3) : 5]$",
        "f) $500 - \\{5 \\cdot [409 - (2^3 \\cdot 3 - 21)^2] + 10\\} : 15$"
    ])

    # DẠNG 4
    add_heading_2(doc, "Dạng 4: Tìm số tự nhiên x cơ bản (Bốn phép tính)")
    add_body_paragraph(doc, "Quy tắc: \n- Tìm số hạng: $x + a = b \\Rightarrow x = b - a$.\n- Tìm số bị trừ: $x - a = b \\Rightarrow x = b + a$. Tìm số trừ: $a - x = b \\Rightarrow x = a - b$.\n- Tìm thừa số: $a \\cdot x = b \\Rightarrow x = b : a$.\n- Tìm số bị chia: $x : a = b \\Rightarrow x = b \\cdot a$. Tìm số chia: $a : x = b \\Rightarrow x = a : b$.", "★")
    
    add_exercise(doc, "4.1", "Tìm số tự nhiên $x$, biết:", [
        "a) $x + 25 = 68$",
        "b) $x + 48 = 125$",
        "c) $84 - x = 39$",
        "d) $135 - x = 89$",
        "e) $x - 36 = 74$",
        "f) $x - 52 = 48$",
        "g) $120 - x = 45$",
        "h) $x + 115 = 200$"
    ])
    
    add_exercise(doc, "4.2", "Tìm số tự nhiên $x$, biết:", [
        "a) $3x = 75$",
        "b) $5x = 120$",
        "c) $96 : x = 12$",
        "d) $84 : x = 14$",
        "e) $x : 15 = 8$",
        "f) $x : 12 = 15$",
        "g) $7x = 91$",
        "h) $144 : x = 16$"
    ])

    # DẠNG 5
    add_heading_2(doc, "Dạng 5: Tìm số tự nhiên x trong biểu thức có ngoặc")
    add_body_paragraph(doc, "Quy tắc: Coi cả cụm trong ngoặc là một ẩn phụ. Tính toán từ ngoài vào trong: xử lý phép cộng trừ ngoài trước, sau đó chia nhân ngoài, cuối cùng mới tìm $x$ trong ngoặc.", "★")
    
    add_exercise(doc, "5.1", "Tìm số tự nhiên $x$, biết:", [
        "a) $3 \\cdot (x + 4) = 42$",
        "b) $5 \\cdot (x + 7) = 120$",
        "c) $4 \\cdot (x - 5) = 28$",
        "d) $6 \\cdot (x - 3) = 54$",
        "e) $84 : (x - 3) = 14$",
        "f) $120 : (x - 2) = 24$",
        "g) $75 : (x - 3) = 15$",
        "h) $110 : (x + 2) = 11$"
    ])
    
    add_exercise(doc, "5.2", "Tìm số tự nhiên $x$, biết:", [
        "a) $2x - 15 = 45$",
        "b) $3x - 14 = 31$",
        "c) $4x + 18 = 54$",
        "d) $5x - 23 = 47$",
        "e) $2x + 35 = 75$",
        "f) $6x - 27 = 33$",
        "g) $7x + 15 = 57$",
        "h) $8x - 35 = 45$"
    ])
    
    add_exercise(doc, "5.3", "Tìm số tự nhiên $x$, biết:", [
        "a) $65 - 5 \\cdot (x + 3) = 20$",
        "b) $50 - 4 \\cdot (x + 2) = 18$",
        "c) $48 - 3 \\cdot (x - 5) = 24$",
        "d) $72 - 3 \\cdot (x + 5) = 27$",
        "e) $125 - 5 \\cdot (x + 4) = 45$",
        "f) $90 - 3 \\cdot (x + 7) = 45$",
        "g) $110 - 5 \\cdot (x + 2) = 40$",
        "h) $(2x - 8) : 3 = 14$"
    ])

    # DẠNG 6
    add_heading_2(doc, "Dạng 6: Tìm số tự nhiên x liên quan đến lũy thừa")
    add_body_paragraph(doc, "Quy tắc: \n- Ẩn ở số mũ ($a^x = a^n$): Đưa hai vế về cùng cơ số $a$ rồi cho hai số mũ bằng nhau.\n- Ẩn ở cơ số ($x^n = a^n$): Đưa hai vế về cùng số mũ rồi cho hai cơ số bằng nhau.", "★")
    
    add_exercise(doc, "6.1", "Tìm số tự nhiên $x$, biết:", [
        "a) $2^x = 16$",
        "b) $2^x = 32$",
        "c) $3^x = 81$",
        "d) $5^x = 125$",
        "e) $2^{x + 1} = 32$",
        "f) $3^{x + 2} = 81$",
        "g) $5^{x - 1} = 125$",
        "h) $2^{x + 3} = 128$",
        "i) $2^{x + 2} + 2^x = 40$",
        "k) $3^{x + 1} + 3^x = 36$"
    ])
    
    add_exercise(doc, "6.2", "Tìm số tự nhiên $x$, biết:", [
        "a) $(x - 1)^2 = 25$",
        "b) $(x + 2)^3 = 27$",
        "c) $(x - 1)^3 = 27$",
        "d) $(2x - 1)^2 = 49$",
        "e) $(x + 1)^3 = 64$",
        "f) $(2x - 3)^2 = 25$"
    ])

    # DẠNG 7
    add_heading_2(doc, "Dạng 7: Dấu hiệu chia hết và tính chất chia hết")
    add_body_paragraph(doc, "Quy tắc: Chia hết cho 2: tận cùng là chữ số chẵn $0, 2, 4, 6, 8$. Chia hết cho 5: tận cùng là $0$ hoặc $5$. Chia hết cho cả 2 và 5: tận cùng bằng $0$. Chia hết cho 3: tổng chữ số chia hết cho 3. Chia hết cho 9: tổng chữ số chia hết cho 9.", "★")
    
    add_exercise(doc, "7.1", "Trong các số: $120; 245; 348; 510; 621; 735; 846; 900$.", [
        "a) Những số nào chia hết cho 2?",
        "b) Những số nào chia hết cho 5?",
        "c) Những số nào chia hết cho cả 2 và 5?",
        "d) Những số nào chia hết cho 3? Những số nào chia hết cho 9?"
    ])
    
    add_exercise(doc, "7.2", "Không tính giá trị cụ thể, giải thích vì sao:", [
        "a) $A = 120 + 48 + 36$ chia hết cho 6.",
        "b) $B = 54 + 360 + 17$ không chia hết cho 9.",
        "c) $C = 1 \\cdot 2 \\cdot 3 \\cdot 4 \\cdot 5 - 35$ chia hết cho 5.",
        "d) $D = 2 \\cdot 3 \\cdot 4 \\cdot 5 \\cdot 6 + 42$ chia hết cho cả 2 và 3."
    ])
    
    add_exercise(doc, "7.3", "Tìm chữ số thích hợp điền vào dấu $*$ để:", [
        "a) Số $\\overline{3*5}$ chia hết cho 9.",
        "b) Số $\\overline{17*}$ chia hết cho cả 2 và 5.",
        "c) Số $\\overline{2*4}$ chia hết cho 3.",
        "d) Số $\\overline{5*8}$ chia hết cho 9.",
        "e) Số $\\overline{1*2}$ chia hết cho 3 nhưng không chia hết cho 9.",
        "f) Tìm các chữ số $x, y$ để số $\\overline{2x3y}$ chia hết cho cả 2; 5 và 9.",
        "g) Tìm các chữ số $x, y$ để số $\\overline{x45y}$ chia hết cho cả 2; 3; 5 và 9."
    ])

    # DẠNG 8
    add_heading_2(doc, "Dạng 8: Số nguyên tố, hợp số và phân tích ra thừa số nguyên tố")
    add_body_paragraph(doc, "Quy tắc: Số nguyên tố là số tự nhiên lớn hơn 1, chỉ có 2 ước là 1 và chính nó: $2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, \\dots$ Hợp số là số tự nhiên lớn hơn 1 có nhiều hơn 2 ước. Phân tích ra TSNT theo cột dọc hoặc sơ đồ cây.", "★")
    
    add_exercise(doc, "8.1", "Trong các số sau: $11; 12; 15; 17; 23; 27; 31; 35; 37; 49; 53$.", [
        "a) Số nào là số nguyên tố? Vì sao?",
        "b) Số nào là hợp số? Vì sao?"
    ])
    
    add_exercise(doc, "8.2", "Phân tích các số sau ra thừa số nguyên tố:", [
        "a) 60 và 72",
        "b) 84 và 90",
        "c) 120 và 144",
        "d) 150 và 180"
    ])

    # DẠNG 9
    add_heading_2(doc, "Dạng 9: Tìm ƯCLN, BCNN và rút gọn phân số")
    add_body_paragraph(doc, "Quy tắc: \n- ƯCLN: Tích các thừa số nguyên tố CHUNG với số mũ NHỎ NHẤT.\n- BCNN: Tích các thừa số nguyên tố CHUNG và RIÊNG với số mũ LỚN NHẤT.\n- ƯC của các số là ước của ƯCLN; BC của các số là bội của BCNN.", "★")
    
    add_exercise(doc, "9.1", "Tìm ƯCLN của các số sau:", [
        "a) ƯCLN(24, 36)",
        "b) ƯCLN(30, 45)",
        "c) ƯCLN(48, 72)",
        "d) ƯCLN(60, 90, 120)"
    ])
    
    add_exercise(doc, "9.2", "Tìm BCNN của các số sau:", [
        "a) BCNN(12, 18)",
        "b) BCNN(15, 20)",
        "c) BCNN(24, 36)",
        "d) BCNN(10, 12, 15)",
        "e) BCNN(12, 15, 18)"
    ])
    
    add_exercise(doc, "9.3", "Rút gọn các phân số sau về phân số tối giản bằng cách chia cả tử và mẫu cho ƯCLN:", [
        "a) $\\frac{24}{36}$",
        "b) $\\frac{48}{72}$",
        "c) $\\frac{60}{140}$",
        "d) $\\frac{135}{225}$"
    ])

    # DẠNG 10
    add_heading_2(doc, "Dạng 10: Bài toán thực tế tìm ƯCLN (Chia đều đồ vật nhiều nhất)")
    add_body_paragraph(doc, "Quy tắc: Nhận diện từ khóa 'nhiều nhất', 'chia đều thành các phần bằng nhau' $\\to$ Quy về tìm ƯCLN của các số lượng đồ vật.", "★")
    
    add_exercise(doc, "10.1", "Cô giáo chủ nhiệm muốn chia 60 quyển vở và 40 chiếc bút bi thành các phần thưởng sao cho số vở và bút ở mỗi phần là như nhau. Hỏi cô giáo có thể chia được nhiều nhất bao nhiêu phần thưởng? Khi đó mỗi phần thưởng có bao nhiêu quyển vở và bao nhiêu chiếc bút bi?")
    
    add_exercise(doc, "10.2", "Một lớp học có 24 bạn nam và 20 bạn nữ. Cô giáo muốn chia lớp thành các tổ học tập sao cho số nam và số nữ ở mỗi tổ đều bằng nhau. Hỏi cô có thể chia được nhiều nhất bao nhiêu tổ? Mỗi tổ có bao nhiêu nam và bao nhiêu nữ?")
    
    add_exercise(doc, "10.3", "Đoàn thanh niên có 72 chiếc áo ấm và 96 đôi tất muốn chia đều vào các túi quà tặng học sinh nghèo vùng cao. Hỏi có thể chia được nhiều nhất bao nhiêu túi quà? Khi đó mỗi túi có bao nhiêu áo ấm và bao nhiêu đôi tất?")
    
    add_exercise(doc, "10.4", "Một cửa hàng có 90 kg gạo tẻ và 60 kg gạo nếp muốn đóng vào các bao nhỏ sao cho khối lượng mỗi loại gạo ở các bao là như nhau. Hỏi chia được nhiều nhất bao nhiêu bao? Mỗi bao có bao nhiêu kg gạo mỗi loại?")

    # DẠNG 11
    add_heading_2(doc, "Dạng 11: Bài toán thực tế tìm BCNN (Xếp hàng vừa đủ, chu kỳ gặp nhau)")
    add_body_paragraph(doc, "Quy tắc: Nhận diện từ khóa 'xếp hàng ... vừa đủ', 'cùng lúc', 'sau ít nhất bao nhiêu ngày lặp lại' $\\to$ Quy về tìm BCNN, sau đó nhân lên tìm Bội chung thỏa mãn khoảng cho trước.", "★")
    
    add_exercise(doc, "11.1", "Số học sinh khối 6 của một trường khi xếp hàng 12, hàng 15, hàng 18 đều vừa vặn không thừa học sinh nào. Biết số học sinh trong khoảng từ 300 đến 400 em. Tính số học sinh khối 6 của trường đó.")
    
    add_exercise(doc, "11.2", "Học sinh khối 6 khi xếp hàng 10, hàng 12, hàng 15 đều vừa đủ hàng. Biết số học sinh trong khoảng từ 200 đến 250 em. Tính số học sinh khối 6.")
    
    add_exercise(doc, "11.3", "Ba bạn An, Bình, Chi cùng tham gia câu lạc bộ bơi lội. An cứ 4 ngày đến hồ bơi một lần, Bình cứ 6 ngày một lần, Chi cứ 8 ngày một lần. Hôm nay cả ba bạn cùng gặp nhau tại hồ bơi. Hỏi sau ít nhất bao nhiêu ngày nữa thì cả ba bạn lại cùng gặp nhau tại hồ bơi?")
    
    add_exercise(doc, "11.4", "Hai hồi chuông reo cùng lúc. Chuông thứ nhất cứ 15 phút reo một lần, chuông thứ hai cứ 20 phút reo một lần. Hỏi sau ít nhất bao nhiêu phút thì hai chuông lại cùng reo?")

    # DẠNG 12
    add_heading_2(doc, "Dạng 12: Hình học trực quan — Chu vi và diện tích các hình phẳng")
    add_body_paragraph(doc, "Công thức: \n- Hình vuông: $C = 4a; S = a^2$.\n- Hình chữ nhật: $C = 2(a + b); S = a \\cdot b$.\n- Hình thoi: $C = 4a; S = \\frac{m \\cdot n}{2}$.\n- Hình bình hành: $C = 2(a + b); S = a \\cdot h$.\n- Hình thang cân: $C = a + b + 2c; S = \\frac{(a + b) \\cdot h}{2}$.", "★")
    
    add_exercise(doc, "12.1", "Tính chu vi và diện tích của các hình phẳng sau:", [
        "a) Hình vuông có cạnh $a = 8\\text{ cm}$.",
        "b) Hình chữ nhật có chiều dài $15\\text{ cm}$ và chiều rộng $8\\text{ cm}$.",
        "c) Hình thoi có hai đường chéo dài $12\\text{ cm}$ và $16\\text{ cm}$.",
        "d) Hình bình hành có cạnh đáy $20\\text{ cm}$ và chiều cao tương ứng $12\\text{ cm}$."
    ])
    
    add_exercise(doc, "12.2", "Một mảnh sân hình chữ nhật có chiều dài 15 m và chiều rộng 8 m.", [
        "a) Tính chu vi và diện tích mảnh sân.",
        "b) Người ta lát sân bằng các viên gạch men hình vuông cạnh 50 cm. Tính số viên gạch cần dùng (coi mép vữa không đáng kể).",
        "c) Biết tiền công lát sân là 60 000 đồng/$\\text{m}^2$. Tính tổng số tiền công lát sân."
    ])
    
    add_exercise(doc, "12.3", "Một nền phòng học hình chữ nhật có chiều dài 9 m và chiều rộng 6 m.", [
        "a) Tính diện tích nền phòng học.",
        "b) Người ta lát nền bằng gạch men vuông cạnh 30 cm. Hỏi cần bao nhiêu viên gạch?",
        "c) Biết mỗi viên gạch giá 18 000 đồng. Tính tiền mua gạch để lát kín nền phòng."
    ])
    
    add_exercise(doc, "12.4", "Một mảnh vườn hình chữ nhật có chiều dài 24 m và chiều rộng 15 m.", [
        "a) Tính chu vi và diện tích mảnh vườn.",
        "b) Người ta làm lối đi xung quanh vườn rộng 1 m, phần còn lại trồng hoa. Tính diện tích phần đất trồng hoa.",
        "c) Người ta làm hàng rào bao quanh mảnh vườn ban đầu, chừa cổng ra vào rộng 2 m. Tính chiều dài hàng rào."
    ])

    # DẠNG 13
    add_heading_2(doc, "Dạng 13: Bài toán vận dụng cao lấy điểm 10")
    add_body_paragraph(doc, "Phương pháp: Nhân thêm cơ số để thu gọn tổng lũy thừa (tính $2S$ hoặc $3S$). Tách phần nguyên để tìm điều kiện chia hết: $(2n + 9) = 2(n + 1) + 7 \\ \\vdots \\ (n + 1) \\Rightarrow 7 \\ \\vdots \\ (n + 1)$.", "★")
    
    add_exercise(doc, "13.1", "Cho tổng $A = 2 + 2^2 + 2^3 + \\dots + 2^{60}$.", [
        "a) Thu gọn tổng $A$.",
        "b) Chứng minh rằng $A$ chia hết cho 3.",
        "c) Chứng minh rằng $A$ chia hết cho 7."
    ])
    
    add_exercise(doc, "13.2", "Cho tổng $B = 3 + 3^2 + 3^3 + \\dots + 3^{60}$.", [
        "a) Chứng minh rằng $2B + 3$ là một lũy thừa của 3.",
        "b) Chứng minh rằng $B$ chia hết cho 13."
    ])
    
    add_exercise(doc, "13.3", "Tìm số tự nhiên $n$ sao cho:", [
        "a) $(n + 7) \\ \\vdots \\ (n + 2)$",
        "b) $(2n + 9) \\ \\vdots \\ (n + 1)$",
        "c) $(3n + 14) \\ \\vdots \\ (n + 3)$"
    ])
    
    add_exercise(doc, "13.4", "So sánh các lũy thừa sau:", [
        "a) $2^{300}$ và $3^{200}$",
        "b) $5^{28}$ và $26^{14}$"
    ])

    # ==================== PHẦN II ====================
    add_heading_1(doc, "PHẦN II: BỘ 10 ĐỀ ÔN TẬP TỰ LUẬN 100% (THỜI GIAN LÀM BÀI: 60 PHÚT/ĐỀ)")
    
    # --- ĐỀ 1 ---
    add_test_header(doc, 1, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính (tính hợp lý nếu có thể):", [
        "a) $38 + 145 + 62 + 55$",
        "b) $27 \\cdot 64 + 27 \\cdot 36 - 500$",
        "c) $120 : [45 - (17 - 3 \\cdot 4)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $3x - 14 = 31$",
        "b) $50 - 4 \\cdot (x + 2) = 18$",
        "c) $2^{x + 1} = 32$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Cô giáo chủ nhiệm muốn chia 60 quyển vở và 40 chiếc bút bi thành các phần thưởng sao cho số vở và bút ở mỗi phần là như nhau. Hỏi có thể chia được nhiều nhất bao nhiêu phần thưởng? Khi đó mỗi phần có bao nhiêu quyển vở và bao nhiêu bút bi?")
    add_exercise(doc, "4 (3,0 điểm)", "Một mảnh sân hình chữ nhật có chiều dài 15 m và chiều rộng 8 m.", [
        "a) Tính chu vi và diện tích của mảnh sân.",
        "b) Người ta lát sân bằng các viên gạch vuông cạnh 50 cm. Tính số viên gạch cần dùng.",
        "c) Biết tiền công lát sân là 60 000 đồng/$\\text{m}^2$. Tính tổng số tiền công lát sân."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Cho $A = 2 + 2^2 + 2^3 + \\dots + 2^{60}$. Chứng minh rằng $A$ chia hết cho 3.")
    
    # --- ĐỀ 2 ---
    add_test_header(doc, 2, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $74 + 185 + 26 + 115$",
        "b) $45 \\cdot 78 + 45 \\cdot 22 - 350$",
        "c) $80 : [35 - (15 - 2 \\cdot 6)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $4x + 18 = 54$",
        "b) $65 - 5 \\cdot (x - 3) = 25$",
        "c) $3^{x + 2} = 81$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Số học sinh khối 6 khi xếp hàng 12, hàng 15, hàng 18 đều vừa vặn không thừa em nào. Biết số học sinh trong khoảng từ 300 đến 400 em. Tính số học sinh khối 6.")
    add_exercise(doc, "4 (3,0 điểm)", "Một khu vườn hình chữ nhật có chiều dài 18 m, chiều rộng 10 m.", [
        "a) Tính chu vi và diện tích khu vườn.",
        "b) Ở giữa khu vườn người ta xây bồn hoa hình thoi có hai đường chéo dài 6 m và 4 m. Tính diện tích đất còn lại để trồng rau.",
        "c) Người ta làm hàng rào quanh khu vườn, để cửa ra vào rộng 2 m. Tính chiều dài hàng rào."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm số tự nhiên $n$ sao cho $(n + 7)$ chia hết cho $(n + 2)$.")
    
    # --- ĐỀ 3 ---
    add_test_header(doc, 3, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $125 \\cdot 27 \\cdot 8$",
        "b) $36 \\cdot 85 + 15 \\cdot 36 - 600$",
        "c) $160 : [25 - (18 - 7 \\cdot 2)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $5x - 23 = 47$",
        "b) $72 - 3 \\cdot (x + 5) = 27$",
        "c) $(x - 1)^3 = 27$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Ba bạn An, Bình, Chi cùng trực nhật. An cứ 6 ngày trực một lần, Bình cứ 8 ngày, Chi cứ 12 ngày. Hôm nay ba bạn cùng trực nhật. Hỏi sau ít nhất bao nhiêu ngày nữa ba bạn lại cùng trực nhật?")
    add_exercise(doc, "4 (3,0 điểm)", "Một phòng họp hình chữ nhật có chiều dài 12 m và chiều rộng 6 m.", [
        "a) Tính diện tích nền phòng họp.",
        "b) Người ta dùng các viên gạch men hình vuông cạnh 40 cm để lát kín phòng họp. Hỏi cần bao nhiêu viên gạch?",
        "c) Mỗi viên gạch giá 25 000 đồng. Tính tiền mua gạch."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Chứng minh rằng tổng $B = 3 + 3^2 + 3^3 + \\dots + 3^{60}$ chia hết cho 13.")
    
    # --- ĐỀ 4 ---
    add_test_header(doc, 4, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $58 + 247 + 42 + 153$",
        "b) $64 \\cdot 35 + 65 \\cdot 64 - 1400$",
        "c) $200 : [119 - (25 - 2 \\cdot 3)]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $2x + 35 = 75$",
        "b) $84 : (x - 3) = 14$",
        "c) $5^{x - 1} = 125$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một lớp học có 24 nam và 20 nữ. Cô giáo muốn chia lớp thành các tổ sao cho số nam và số nữ ở mỗi tổ đều bằng nhau. Hỏi có thể chia được nhiều nhất bao nhiêu tổ? Khi đó mỗi tổ có bao nhiêu nam, bao nhiêu nữ?")
    add_exercise(doc, "4 (3,0 điểm)", "Một mảnh đất hình bình hành có độ dài đáy là 25 m, chiều cao tương ứng là 12 m.", [
        "a) Tính diện tích mảnh đất hình bình hành.",
        "b) Biết cạnh bên của mảnh đất dài 15 m. Tính chu vi mảnh đất.",
        "c) Người ta trồng cỏ trên toàn bộ mảnh đất với chi phí 40 000 đồng/$\\text{m}^2$. Tính tổng chi phí trồng cỏ."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm số tự nhiên $x$ biết $120$ chia hết cho $x$, $180$ chia hết cho $x$ và $x > 20$.")
    
    # --- ĐỀ 5 ---
    add_test_header(doc, 5, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $83 + 365 + 17 + 135$",
        "b) $52 \\cdot 84 + 16 \\cdot 52 - 200$",
        "c) $150 : [28 - (16 - 3 \\cdot 4)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $6x - 27 = 33$",
        "b) $125 - 5 \\cdot (x + 4) = 45$",
        "c) $2^{x + 3} = 64$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Số học sinh một trường khi xếp hàng 8, hàng 10, hàng 12 đều vừa đủ. Biết số học sinh trong khoảng từ 350 đến 450 em. Tính số học sinh trường đó.")
    add_exercise(doc, "4 (3,0 điểm)", "Một nền nhà hình chữ nhật có chiều dài 10 m, chiều rộng 6 m.", [
        "a) Tính chu vi và diện tích nền nhà.",
        "b) Người ta lát nền bằng gạch hình vuông cạnh 50 cm. Tính số viên gạch cần dùng.",
        "c) Biết mỗi viên gạch giá 35 000 đồng và công lát là 50 000 đồng/$\\text{m}^2$. Tính tổng chi phí lát nền."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm chữ số $x, y$ để số $\\overline{2x3y}$ chia hết cho cả 2; 5 và 9.")
    
    # --- ĐỀ 6 ---
    add_test_header(doc, 6, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $67 + 158 + 33 + 42$",
        "b) $43 \\cdot 76 + 43 \\cdot 24 - 300$",
        "c) $90 : [24 - (15 - 3 \\cdot 3)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $7x + 15 = 57$",
        "b) $48 - 4 \\cdot (x - 2) = 24$",
        "c) $(2x - 1)^2 = 49$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Đoàn thanh niên có 72 áo ấm và 96 đôi tất muốn chia đều vào các túi quà tặng người nghèo. Hỏi có thể chia được nhiều nhất bao nhiêu túi quà? Mỗi túi quà có bao nhiêu áo ấm và bao nhiêu đôi tất?")
    add_exercise(doc, "4 (3,0 điểm)", "Một mảnh vườn hình chữ nhật có chiều dài 24 m và chiều rộng 15 m.", [
        "a) Tính chu vi và diện tích mảnh vườn.",
        "b) Người ta bớt lối đi xung quanh vườn rộng 1 m, phần còn lại trồng hoa. Tính diện tích phần trồng hoa.",
        "c) Rào xung quanh vườn chừa cổng 2 m. Tính chiều dài hàng rào."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Chứng minh rằng $S = 5 + 5^2 + 5^3 + \\dots + 5^{100}$ chia hết cho 6.")
    
    # --- ĐỀ 7 ---
    add_test_header(doc, 7, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $4 \\cdot 49 \\cdot 25$",
        "b) $128 \\cdot 67 + 33 \\cdot 128 - 2800$",
        "c) $180 : [45 - (18 - 3 \\cdot 5)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $5x - 38 = 42$",
        "b) $90 - 3 \\cdot (x + 7) = 45$",
        "c) $2^{x + 2} + 2^x = 40$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Hai hồi chuông reo cùng lúc. Chuông thứ nhất cứ 15 phút reo một lần, chuông thứ hai cứ 20 phút reo một lần. Hỏi sau ít nhất bao nhiêu phút hai chuông lại cùng reo?")
    add_exercise(doc, "4 (3,0 điểm)", "Một mảnh đất hình thoi có hai đường chéo dài 16 m và 12 m. Cạnh của hình thoi dài 10 m.", [
        "a) Tính chu vi và diện tích mảnh đất hình thoi.",
        "b) Người ta trồng rau trên mảnh đất, mỗi mét vuông thu hoạch được 5 kg rau. Tính khối lượng rau thu hoạch được.",
        "c) Giá bán mỗi kg rau là 15 000 đồng. Tính tổng số tiền bán rau."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm số tự nhiên $n$ sao cho $(2n + 9)$ chia hết cho $(n + 1)$.")
    
    # --- ĐỀ 8 ---
    add_test_header(doc, 8, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $142 + 258 + 58 + 42$",
        "b) $35 \\cdot 118 - 35 \\cdot 18 + 500$",
        "c) $100 : [30 - (12 - 2 \\cdot 4)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $4x - 19 = 45$",
        "b) $120 : (x - 5) = 15$",
        "c) $3^{x + 1} = 243$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Khối 6 có khoảng từ 200 đến 250 học sinh. Khi xếp hàng 10, hàng 12, hàng 15 đều vừa đủ. Tính số học sinh khối 6.")
    add_exercise(doc, "4 (3,0 điểm)", "Một khu vườn hình chữ nhật có chiều dài 20 m và chiều rộng 14 m.", [
        "a) Tính diện tích và chu vi khu vườn.",
        "b) Ở giữa vườn đào một ao cá hình vuông cạnh 6 m. Tính diện tích đất còn lại của khu vườn.",
        "c) Làm hàng rào quanh khu vườn chừa cổng ra vào rộng 3 m. Tính chiều dài hàng rào."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "So sánh $2^{300}$ và $3^{200}$.")
    
    # --- ĐỀ 9 ---
    add_test_header(doc, 9, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $25 \\cdot 37 \\cdot 4$",
        "b) $84 \\cdot 45 + 55 \\cdot 84 - 400$",
        "c) $140 : [35 - (16 - 3 \\cdot 4)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $8x - 35 = 45$",
        "b) $110 - 5 \\cdot (x + 2) = 40$",
        "c) $(x + 1)^3 = 64$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một cửa hàng có 90 kg gạo tẻ và 60 kg gạo nếp. Người ta muốn chia đều vào các bao sao cho số gạo tẻ và nếp ở mỗi bao là như nhau. Hỏi có thể chia được nhiều nhất bao nhiêu bao? Mỗi bao có bao nhiêu kg mỗi loại?")
    add_exercise(doc, "4 (3,0 điểm)", "Một căn phòng hình chữ nhật dài 9 m, rộng 6 m.", [
        "a) Tính diện tích căn phòng.",
        "b) Lát nền bằng các viên gạch vuông cạnh 30 cm. Hỏi cần bao nhiêu viên gạch?",
        "c) Mỗi viên gạch giá 18 000 đồng. Tính tiền mua gạch lát căn phòng."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Chứng minh rằng $(10^{30} + 2)$ chia hết cho 3.")
    
    # --- ĐỀ 10 ---
    add_test_header(doc, 10, "6")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $63 + 175 + 37 + 125$",
        "b) $67 \\cdot 54 + 46 \\cdot 67 - 700$",
        "c) $120 : [54 - (18 - 4 \\cdot 3)^2]$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Tìm số tự nhiên $x$, biết:", [
        "a) $9x - 24 = 48$",
        "b) $75 : (x - 3) = 15$",
        "c) $2^{x + 3} = 128$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Ba hồi chuông báo giờ của ba xưởng sản xuất: hồi thứ nhất cứ 20 phút reo, hồi thứ hai cứ 30 phút, hồi thứ ba cứ 45 phút. Lúc 7 giờ sáng cả ba chuông cùng reo. Hỏi lần tiếp theo cả ba chuông cùng reo lúc mấy giờ?")
    add_exercise(doc, "4 (3,0 điểm)", "Một mảnh sân hình chữ nhật dài 16 m, rộng 10 m.", [
        "a) Tính chu vi và diện tích mảnh sân.",
        "b) Người ta lát sân bằng gạch vuông cạnh 40 cm. Cần bao nhiêu viên gạch?",
        "c) Giá mỗi viên gạch là 22 000 đồng, tiền công là 50 000 đồng/$\\text{m}^2$. Tính tổng chi phí lát sân."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Cho $M = 4 + 4^2 + 4^3 + \\dots + 4^{2024}$. Chứng minh rằng $M$ chia hết cho 5.")
    
    # ==================== PHẦN III ====================
    add_heading_1(doc, "PHẦN III: BẢNG ĐÁP SỐ VÀ HƯỚNG DẪN GIẢI 10 ĐỀ TỰ LUẬN")
    add_answer_header(doc, 1)
    for _ans in [
        "Bài 1: a) 300; b) 2200; c) 6.",
        "Bài 2: a) $x = 15$; b) $x = 6$; c) $x = 4$.",
        "Bài 3: Chia được nhiều nhất 20 phần. Mỗi phần có 3 quyển vở và 2 chiếc bút bi.",
        "Bài 4: a) Chu vi: 46 m; Diện tích: 120 $\\text{m}^2$; b) 480 viên gạch; c) 7 200 000 đồng.",
        "Bài 5: Ghép nhóm: $A = 2(1 + 2) + 2^3(1 + 2) + \\dots = 3 \\cdot (2 + 2^3 + \\dots) \\ \\vdots \\ 3$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 2)
    for _ans in [
        "Bài 1: a) 400; b) 4150; c) 4.",
        "Bài 2: a) $x = 9$; b) $x = 11$; c) $x = 2$.",
        "Bài 3: Số học sinh là $\\text{BCNN}(12, 15, 18) = 180$. Bội chung trong khoảng 300 đến 400 là 360 em.",
        "Bài 4: a) Chu vi: 56 m; Diện tích: 180 $\\text{m}^2$; b) Diện tích bồn hoa 12 $\\text{m}^2$, diện tích trồng rau 168 $\\text{m}^2$; c) Hàng rào dài 54 m.",
        "Bài 5: $(n + 7) = (n + 2) + 5 \\ \\vdots \\ (n + 2) \\Rightarrow 5 \\ \\vdots \\ (n + 2) \\Rightarrow n + 2 = 5 \\Rightarrow n = 3$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 3)
    for _ans in [
        "Bài 1: a) 27000; b) 3000; c) 16.",
        "Bài 2: a) $x = 14$; b) $x = 10$; c) $x = 4$.",
        "Bài 3: Sau ít nhất $\\text{BCNN}(6, 8, 12) = 24$ ngày.",
        "Bài 4: a) 72 $\\text{m}^2$; b) 450 viên gạch; c) 11 250 000 đồng.",
        "Bài 5: Ghép 3 số hạng: $B = 3(1 + 3 + 9) + \\dots = 13 \\cdot (3 + \\dots) \\ \\vdots \\ 13$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 4)
    for _ans in [
        "Bài 1: a) 500; b) 5000; c) 2.",
        "Bài 2: a) $x = 20$; b) $x = 9$; c) $x = 4$.",
        "Bài 3: Chia được nhiều nhất $\\text{ƯCLN}(24, 20) = 4$ tổ. Mỗi tổ 6 nam và 5 nữ.",
        "Bài 4: a) 300 $\\text{m}^2$; b) 80 m; c) 12 000 000 đồng.",
        "Bài 5: $x \\in \\text{ƯC}(120, 180) = \\text{Ư}(60)$. Vì $x > 20$ nên $x \\in \\{30; 60\\}$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 5)
    for _ans in [
        "Bài 1: a) 600; b) 5000; c) 12.",
        "Bài 2: a) $x = 10$; b) $x = 12$; c) $x = 3$.",
        "Bài 3: $\\text{BCNN}(8, 10, 12) = 120$. Bội chung trong khoảng 350 đến 450 là 360 em.",
        "Bài 4: a) Chu vi 32 m, diện tích 60 $\\text{m}^2$; b) 240 viên gạch; c) Tiền gạch: 8 400 000 đ, tiền công: 3 000 000 đ, tổng: 11 400 000 đồng.",
        "Bài 5: Để chia hết cho 2 và 5 thì $y = 0$. Số $2x30$ chia hết cho 9 khi $2 + x + 3 + 0 = 5 + x \\ \\vdots \\ 9 \\Rightarrow x = 4$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 6)
    for _ans in [
        "Bài 1: a) 300; b) 4000; c) 6.",
        "Bài 2: a) $x = 6$; b) $x = 8$; c) $2x - 1 = 7 \\Rightarrow x = 4$.",
        "Bài 3: $\\text{ƯCLN}(72, 96) = 24$ túi quà. Mỗi túi 3 áo ấm và 4 đôi tất.",
        "Bài 4: a) Chu vi 78 m, diện tích 360 $\\text{m}^2$; b) Kích thước trong: $22 \\times 13 = 286\\text{ m}^2$; c) Hàng rào 76 m.",
        "Bài 5: Ghép cặp: $S = 5(1 + 5) + 5^3(1 + 5) + \\dots = 6 \\cdot (5 + 5^3 + \\dots) \\ \\vdots \\ 6$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 7)
    for _ans in [
        "Bài 1: a) 4900; b) 10000; c) 5.",
        "Bài 2: a) $x = 16$; b) $x = 8$; c) $2^x(4 + 1) = 40 \\Rightarrow 2^x = 8 \\Rightarrow x = 3$.",
        "Bài 3: $\\text{BCNN}(15, 20) = 60$ phút (1 giờ).",
        "Bài 4: a) Chu vi 40 m, diện tích 96 $\\text{m}^2$; b) 480 kg rau; c) 7 200 000 đồng.",
        "Bài 5: $2n + 9 = 2(n + 1) + 7 \\ \\vdots \\ (n + 1) \\Rightarrow 7 \\ \\vdots \\ (n + 1) \\Rightarrow n + 1 = 7 \\Rightarrow n = 6$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 8)
    for _ans in [
        "Bài 1: a) 500; b) 4000; c) 7.",
        "Bài 2: a) $x = 16$; b) $x = 13$; c) $x = 4$.",
        "Bài 3: $\\text{BCNN}(10, 12, 15) = 60$. Bội chung trong khoảng 200 đến 250 là 240 em.",
        "Bài 4: a) Chu vi 68 m, diện tích 280 $\\text{m}^2$; b) Diện tích ao 36 $\\text{m}^2$, diện tích còn lại 244 $\\text{m}^2$; c) Hàng rào 65 m.",
        "Bài 5: $2^{300} = (2^3)^{100} = 8^{100}$; $3^{200} = (3^2)^{100} = 9^{100}$. Vì $8 < 9$ nên $2^{300} < 3^{200}$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 9)
    for _ans in [
        "Bài 1: a) 3700; b) 8000; c) 7.",
        "Bài 2: a) $x = 10$; b) $x = 12$; c) $x + 1 = 4 \\Rightarrow x = 3$.",
        "Bài 3: $\\text{ƯCLN}(90, 60) = 30$ bao. Mỗi bao 3 kg gạo tẻ và 2 kg gạo nếp.",
        "Bài 4: a) 54 $\\text{m}^2$; b) 600 viên gạch; c) 10 800 000 đồng.",
        "Bài 5: Số $10^{30} + 2 = 100\\dots002$ có tổng các chữ số là $1 + 2 = 3 \\ \\vdots \\ 3$ nên chia hết cho 3."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 10)
    for _ans in [
        "Bài 1: a) 400; b) 6000; c) 6.",
        "Bài 2: a) $x = 8$; b) $x = 8$; c) $x = 4$.",
        "Bài 3: $\\text{BCNN}(20, 30, 45) = 180$ phút = 3 giờ. Cùng reo lại lúc $7 + 3 = 10$ giờ sáng.",
        "Bài 4: a) Chu vi 52 m, diện tích 160 $\\text{m}^2$; b) 1000 viên gạch; c) Tiền gạch: 22 000 000 đ, công: 8 000 000 đ, tổng: 30 000 000 đồng.",
        "Bài 5: Ghép cặp: $M = 4(1 + 4) + 4^3(1 + 4) + \\dots = 5 \\cdot (4 + 4^3 + \\dots) \\ \\vdots \\ 5$."
    ]:
        add_answer_item(doc, _ans)

    doc.save(output_path)
    print(f"[TOAN 6 - 2026-2027] Saved successfully to: {output_path}")

if __name__ == "__main__":
    import datetime
    today = datetime.datetime.now().strftime("%d.%m")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "2_TAO_BAI_TAP", "Ket_qua", today)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "De_Cuong_On_Tap_Giua_HK1_Toan_6.docx")
    build_de_cuong_toan_6(out_file)
