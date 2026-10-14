# -*- coding: utf-8 -*-
"""
BIÊN SOẠN ĐỀ CƯƠNG ÔN TẬP GIỮA HỌC KỲ I - TOÁN 8 (PHIÊN BẢN ĐẠI BẢNG RÈN LUYỆN)
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

def build_de_cuong_toan_8(output_path):
    doc = create_base_document()
    add_header_quoc_hieu(doc, "8", school_year="2026 - 2027")
    
    # ==================== PHẦN I ====================
    add_heading_1(doc, "PHẦN I: HỆ THỐNG BÀI TẬP RÈN KỸ NĂNG CƠ BẢN (DÀNH CHO HỌC SINH YẾU & TRUNG BÌNH)")
    
    # DẠNG 1
    add_heading_2(doc, "Dạng 1: Đơn thức nhiều biến (Thu gọn, bậc, hệ số, đơn thức đồng dạng)")
    add_body_paragraph(doc, "Quy tắc: Nhân hệ số với hệ số, biến với biến (cộng số mũ). Bậc của đơn thức là tổng số mũ của tất cả các biến. Hai đơn thức đồng dạng có hệ số khác 0 và có cùng phần biến.", "★")
    
    add_exercise(doc, "1.1", "Thu gọn các đơn thức sau, chỉ rõ phần hệ số, phần biến và bậc của mỗi đơn thức:", [
        "a) $A = 2x^2y \\cdot (-3xy^2)$",
        "b) $B = -\\frac{1}{2}x^3y \\cdot (4xy^3)$",
        "c) $C = 5x^2y \\cdot 2xy \\cdot (-y^2)$",
        "d) $D = -4x^3y^2z \\cdot \\left(-\\frac{1}{2}xyz\\right)$",
        "e) $E = \\frac{3}{4}xy^2 \\cdot (-8x^2y)$",
        "f) $F = -2x^2y \\cdot (-5x^3y^4)$"
    ])
    
    add_exercise(doc, "1.2", "Xếp các đơn thức sau thành từng nhóm các đơn thức đồng dạng:", [
        "$-3x^2y; \\ 2xy^2; \\ 5x^2y; \\ -\\frac{1}{2}xy^2; \\ 4x^2y; \\ 7xy^2; \\ -x^2y$"
    ])
    
    add_exercise(doc, "1.3", "Thực hiện phép tính:", [
        "a) $3x^2y + 5x^2y - 2x^2y$",
        "b) $4xy^2 - 7xy^2 + 8xy^2$",
        "c) $\\frac{1}{2}x^3y^2 + \\frac{3}{2}x^3y^2 - 5x^3y^2$",
        "d) $5x^2y^3 - 8x^2y^3 + 12x^2y^3$"
    ])

    # DẠNG 2
    add_heading_2(doc, "Dạng 2: Đa thức nhiều biến (Thu gọn, tìm bậc, tính giá trị)")
    add_body_paragraph(doc, "Quy tắc: Gom các đơn thức đồng dạng lại rồi cộng trừ hệ số. Bậc của đa thức là bậc của hạng tử có bậc cao nhất trong dạng thu gọn. Tính giá trị: thu gọn trước rồi thay số.", "★")
    
    add_exercise(doc, "2.1", "Thu gọn các đa thức sau và xác định bậc của mỗi đa thức:", [
        "a) $M = 3x^2y - 5xy^2 + 7 - 2x^2y + 5xy^2 - 3$",
        "b) $N = 2x^3 - 4x^2y + 3xy^2 - 2x^3 + 5x^2y - 2$",
        "c) $P = x^2y - 3xy + 5x^2y + 3xy - 7$",
        "d) $Q = 4x^2y - 3xy + 5 - 2x^2y + 3xy$",
        "e) $R = x^3 + 4x^2y - 3xy^2 - x^3 - 4x^2y + 5xy^2 - y^3$",
        "f) $S = 2x^4 - 3x^2y^2 + y^4 - 2x^4 + 5x^2y^2 - 2y^4 + 1$"
    ])
    
    add_exercise(doc, "2.2", "Tính giá trị của mỗi đa thức sau:", [
        "a) Tính giá trị của $M = x^2y - 3xy + 2$ tại $x = 1, y = -1$",
        "b) Tính giá trị của $N = 2x^2 - 5xy + y^2$ tại $x = -1, y = 2$",
        "c) Tính giá trị của $P = 3x^2y - 5xy^2 + 7 - 2x^2y + 5xy^2 - 3$ tại $x = -2, y = 1$"
    ])

    # DẠNG 3
    add_heading_2(doc, "Dạng 3: Phép cộng và trừ đa thức nhiều biến")
    add_body_paragraph(doc, "Quy tắc: Đặt phép tính trong ngoặc. Phá ngoặc chú ý đổi dấu khi trước ngoặc có dấu trừ. Nhóm các hạng tử đồng dạng để thu gọn.", "★")
    
    add_exercise(doc, "3.1", "Cho hai đa thức: $A = 4x^2 - 5xy + 3y^2$ và $B = 3x^2 + 2xy - y^2$.", [
        "a) Tính $C = A + B$",
        "b) Tính $D = A - B$",
        "c) Tính giá trị của $D$ tại $x = -1, y = 2$"
    ])
    
    add_exercise(doc, "3.2", "Cho hai đa thức: $P = 5x^2y - 3xy^2 + 4xy - 1$ và $Q = 2x^2y + 3xy^2 - 5xy + 6$.", [
        "a) Tính $P + Q$",
        "b) Tính $P - Q$"
    ])

    # DẠNG 4
    add_heading_2(doc, "Dạng 4: Phép nhân đa thức (Đơn với đa, đa với đa)")
    add_body_paragraph(doc, "Quy tắc: $A(B + C) = AB + AC$. $(A + B)(C + D) = AC + AD + BC + BD$. Cẩn thận quy tắc dấu: $(-a) \\cdot (-b) = ab$; $(-a) \\cdot b = -ab$.", "★")
    
    add_exercise(doc, "4.1", "Thực hiện phép tính:", [
        "a) $2x(3x^2 - 5x + 1)$",
        "b) $-3xy(2x^2 - 3xy + y^2)$",
        "c) $2xy(3x^2 - 4xy + 5y^2)$",
        "d) $-2x^2y(3xy - 4x + 2y)$",
        "e) $5x(x^2 - 2x + 3)$",
        "f) $-4x(x^2 - 3x + 2)$"
    ])
    
    add_exercise(doc, "4.2", "Thực hiện phép tính:", [
        "a) $(x + 3)(2x - 1)$",
        "b) $(2x - 3)(x^2 - 2x + 1)$",
        "c) $(2x - 3)(x + 2)$",
        "d) $(3x - 1)(x + 2)$",
        "e) $(x + 4)(x - 2)$",
        "f) $(2x - 1)(x + 3)$",
        "g) $(x - 3)(2x + 1)$",
        "h) $(2x - 5)(x + 2)$"
    ])

    # DẠNG 5
    add_heading_2(doc, "Dạng 5: Phép chia đa thức cho đơn thức")
    add_body_paragraph(doc, "Quy tắc: Chia từng hạng tử của đa thức cho đơn thức: $(A + B) : M = A : M + B : M$. Lũy thừa: $x^m : x^n = x^{m-n}$ ($m \\ge n$).", "★")
    
    add_exercise(doc, "5.1", "Thực hiện phép tính chia:", [
        "a) $(12x^3y^2 - 8x^2y) : (4x^2y)$",
        "b) $(15x^4y^3 - 20x^3y^2 + 25x^2y) : (5x^2y)$",
        "c) $(18x^4y^3 - 12x^3y^2 + 6x^2y) : (6x^2y)$",
        "d) $(6x^3y^2 - 9x^2y^3 + 12x^2y^2) : (-3x^2y)$",
        "e) $(24x^5y^3 - 16x^4y^2) : (8x^3y^2)$",
        "f) $(20x^3y^4 - 15x^2y^3 + 10xy^2) : (5xy^2)$",
        "g) $(25x^4y^3 - 15x^3y^2) : (5x^2y^2)$",
        "h) $(16x^4y^3 - 12x^3y^2 + 8x^2y) : (4x^2y)$"
    ])

    # DẠNG 6
    add_heading_2(doc, "Dạng 6: Năm hằng đẳng thức đáng nhớ — Khai triển")
    add_body_paragraph(doc, "Công thức: \n1) $A^2 - B^2 = (A - B)(A + B)$. \n2) $(A + B)^2 = A^2 + 2AB + B^2$. \n3) $(A - B)^2 = A^2 - 2AB + B^2$. \n4) $(A + B)^3 = A^3 + 3A^2B + 3AB^2 + B^3$. \n5) $(A - B)^3 = A^3 - 3A^2B + 3AB^2 - B^3$.", "★")
    
    add_exercise(doc, "6.1", "Khai triển các biểu thức sau:", [
        "a) $(x + 3)^2$",
        "b) $(2x - 1)^2$",
        "c) $(3x - 2y)^2$",
        "d) $(2x + 3y)^2$",
        "e) $(x - 5)^2$",
        "f) $(3x + 1)^2$",
        "g) $(2x - 3)^2$",
        "h) $(x + 4)^2$"
    ])
    
    add_exercise(doc, "6.2", "Khai triển các biểu thức sau:", [
        "a) $(x - 3)(x + 3)$",
        "b) $(x - 4)(x + 4)$",
        "c) $(2x - 3)(2x + 3)$",
        "d) $(3x - 1)(3x + 1)$",
        "e) $(4x - 5)(4x + 5)$",
        "f) $(2x - 5)(2x + 5)$"
    ])
    
    add_exercise(doc, "6.3", "Khai triển các biểu thức sau:", [
        "a) $(x + 2)^3$",
        "b) $(x - 1)^3$",
        "c) $(2x - 1)^3$",
        "d) $(x + 2y)^3$"
    ])

    # DẠNG 7
    add_heading_2(doc, "Dạng 7: Viết biểu thức về dạng bình phương hoặc lập phương")
    add_body_paragraph(doc, "Quy tắc: Nhận diện $a^2 \\pm 2ab + b^2 = (a \\pm b)^2$. Kiểm tra hạng tử ở giữa $2ab$.", "★")
    
    add_exercise(doc, "7.1", "Viết các biểu thức sau dưới dạng bình phương hoặc lập phương:", [
        "a) $x^2 + 6x + 9$",
        "b) $4x^2 - 4x + 1$",
        "c) $9x^2 - 12xy + 4y^2$",
        "d) $4x^2 + 12x + 9$",
        "e) $25x^2 - 20xy + 4y^2$",
        "f) $x^3 - 3x^2 + 3x - 1$",
        "g) $x^3 - 6x^2 + 12x - 8$",
        "h) $8x^3 + 36x^2y + 54xy^2 + 27y^3$"
    ])

    # DẠNG 8
    add_heading_2(doc, "Dạng 8: Tính nhanh giá trị số dùng hằng đẳng thức")
    add_body_paragraph(doc, "Quy tắc: $101^2 = (100 + 1)^2$; $99^2 = (100 - 1)^2$; $a^2 - b^2 = (a - b)(a + b)$.", "★")
    
    add_exercise(doc, "8.1", "Tính nhanh giá trị các biểu thức:", [
        "a) $101^2$",
        "b) $99^2$",
        "c) $75^2 - 25^2$",
        "d) $52 \\cdot 48$",
        "e) $102 \\cdot 98$",
        "f) $53^2 + 47^2 + 2 \\cdot 53 \\cdot 47$"
    ])

    # DẠNG 9
    add_heading_2(doc, "Dạng 9: Rút gọn biểu thức và chứng minh không phụ thuộc biến")
    add_body_paragraph(doc, "Quy tắc: Khai triển HĐT, nhân phá ngoặc, đổi dấu cẩn thận, thu gọn đồng dạng. Không phụ thuộc biến khi kết quả rút gọn là một hằng số.", "★")
    
    add_exercise(doc, "9.1", "Rút gọn các biểu thức sau:", [
        "a) $A = (x + 2)^2 - (x - 2)^2$",
        "b) $B = (x + 3)^2 - (x - 2)(x + 2) - 6x$",
        "c) $C = (2x - 1)^2 - (2x + 3)(2x - 3)$",
        "d) $D = (x - 2)^2 + (x + 2)^2 - 2x^2$",
        "e) $E = (x + 1)^2 - 2(x + 1)(x - 2) + (x - 2)^2$",
        "f) $F = (3x - 1)(3x + 1) - (3x - 2)^2$",
        "g) $G = (2x + 3)^2 - (2x - 3)^2$",
        "h) $H = (x + 2)^3 - (x - 2)^3 - 12x^2$"
    ])
    
    add_exercise(doc, "9.2", "Chứng minh rằng giá trị của các biểu thức sau không phụ thuộc vào $x$:", [
        "a) $M = (x - 5)(2x + 3) - 2x(x - 3) + x + 7$",
        "b) $N = (3x - 2)^2 - (3x + 1)(3x - 1) + 12x$",
        "c) $P = (x + 3)^2 - (x - 2)(x + 2) - 6x$"
    ])

    # DẠNG 10
    add_heading_2(doc, "Dạng 10: Tìm x triệt tiêu bậc hai")
    add_body_paragraph(doc, "Quy tắc: Khai triển hai vế, chuyển vế làm triệt tiêu số hạng $x^2$, đưa về dạng $ax = b \\Rightarrow x = b/a$.", "★")
    
    add_exercise(doc, "10.1", "Tìm $x$, biết:", [
        "a) $(x + 3)^2 - (x - 1)(x + 1) = 16$",
        "b) $(2x - 1)^2 - 4x(x - 2) = 9$",
        "c) $(x + 4)^2 - (x - 2)(x + 2) = 28$",
        "d) $(3x - 1)^2 - 9x(x - 2) = 17$",
        "e) $(2x - 3)^2 - 4x(x - 1) = 21$",
        "f) $(x + 2)^2 - (x - 3)(x + 3) = 13$",
        "g) $(2x + 1)^2 - 4x(x - 3) = 25$",
        "h) $(x - 4)^2 - (x + 2)(x - 2) = 12$"
    ])
    
    add_exercise(doc, "10.2", "Tìm $x$, biết:", [
        "a) $(3x - 2)^2 - (3x + 1)(3x - 1) = 9$",
        "b) $(x - 1)^2 - (x + 3)(x - 3) = 6$",
        "c) $(2x + 3)^2 - 4(x - 1)(x + 1) = 25$",
        "d) $4x(x - 5) - (2x + 1)^2 = 11$"
    ])

    # DẠNG 11
    add_heading_2(doc, "Dạng 11: Tìm x đưa về phương trình tích")
    add_body_paragraph(doc, "Quy tắc: Đưa về dạng $A(x) \\cdot B(x) = 0 \\Rightarrow A(x) = 0$ hoặc $B(x) = 0$.", "★")
    
    add_exercise(doc, "11.1", "Tìm $x$, biết:", [
        "a) $x^2 - 9 = 0$",
        "b) $4x^2 - 25 = 0$",
        "c) $x(x - 4) + 2(x - 4) = 0$",
        "d) $(2x - 3)^2 - (x + 1)^2 = 0$",
        "e) $x^2 - 6x + 9 = 0$",
        "f) $4x^2 - 12x + 9 = 0$",
        "g) $x^3 - 4x = 0$",
        "h) $2x(x - 3) - 5(x - 3) = 0$"
    ])

    # DẠNG 12
    add_heading_2(doc, "Dạng 12: Hình học — Tứ giác, tính số đo góc")
    add_body_paragraph(doc, "Định lý: Tổng bốn góc của một tứ giác luôn bằng $360^\\circ$: $\\widehat{A} + \\widehat{B} + \\widehat{C} + \\widehat{D} = 360^\\circ$.", "★")
    
    add_exercise(doc, "12.1", "Cho tứ giác $ABCD$ có $\\widehat{A} = 100^\\circ, \\widehat{B} = 80^\\circ, \\widehat{C} = 110^\\circ$. Tính số đo góc $\\widehat{D}$.")
    
    add_exercise(doc, "12.2", "Cho tứ giác $ABCD$ có $\\widehat{A} = 60^\\circ, \\widehat{B} = 100^\\circ, \\widehat{C} = 80^\\circ$. Tính số đo góc $\\widehat{D}$.")
    
    add_exercise(doc, "12.3", "Cho tứ giác $ABCD$ có $\\widehat{A} = 110^\\circ, \\widehat{B} = 80^\\circ, \\widehat{D} = 70^\\circ$. Tính số đo góc $\\widehat{C}$.")

    # DẠNG 13
    add_heading_2(doc, "Dạng 13: Hình học — Hình thang cân")
    add_body_paragraph(doc, "Tính chất: Hình thang có hai góc kề một đáy bằng nhau, hai đường chéo bằng nhau. Đường cao hạ từ hai đáy nhỏ tạo hai tam giác vuông bằng nhau: $DH = CK = \\frac{CD - AB}{2}$.", "★")
    
    add_exercise(doc, "13.1", "Cho hình thang cân $ABCD$ ($AB \\parallel CD$) có $\\widehat{C} = 60^\\circ$. Tính các góc còn lại của hình thang cân.")
    
    add_exercise(doc, "13.2", "Cho hình thang cân $ABCD$ ($AB \\parallel CD$, $AB < CD$). Kẻ các đường cao $AH, BK$ xuống đáy $CD$.", [
        "a) Chứng minh $\\Delta AHD = \\Delta BKC$",
        "b) Chứng minh $DH = CK = \\frac{CD - AB}{2}$",
        "c) Biết $AB = 6\\text{ cm}, CD = 14\\text{ cm}, AD = 5\\text{ cm}$. Tính độ dài đường cao $AH$ và diện tích hình thang cân $ABCD$."
    ])

    # DẠNG 14
    add_heading_2(doc, "Dạng 14: Hình học — Hình bình hành, Hình chữ nhật, Hình thoi, Hình vuông")
    add_body_paragraph(doc, "Dấu hiệu nhận biết: \n- HBH: các cạnh đối song song hoặc bằng nhau; 2 đường chéo cắt nhau tại trung điểm.\n- HCN: HBH có 1 góc vuông hoặc 2 đường chéo bằng nhau.\n- Hình thoi: HBH có 2 cạnh kề bằng nhau hoặc 2 đường chéo vuông góc.\n- Hình vuông: vừa là HCN vừa là hình thoi.", "★")
    
    add_exercise(doc, "14.1", "Cho hình bình hành $ABCD$. Gọi $E$ là trung điểm của $AB$, $F$ là trung điểm của $CD$.", [
        "a) Chứng minh tứ giác $AECF$ là hình bình hành.",
        "b) Đoạn thẳng $AC$ cắt $EF$ tại $O$. Chứng minh $O$ là trung điểm của $AC$ và $EF$.",
        "c) Gọi $M$ là giao điểm của $AF$ và $DE$, $N$ là giao điểm của $BF$ và $CE$. Chứng minh tứ giác $EMFN$ là hình bình hành."
    ])
    
    add_exercise(doc, "14.2", "Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường trung tuyến $AM$. Gọi $D$ là điểm đối xứng với $A$ qua $M$.", [
        "a) Chứng minh tứ giác $ABDC$ là hình chữ nhật.",
        "b) Gọi $I$ là trung điểm của $AC$. Kẻ $IK \\parallel BC$ ($K \\in AB$). Chứng minh $K$ là trung điểm của $AB$.",
        "c) Gọi $E$ là điểm đối xứng với $M$ qua $I$. Chứng minh tứ giác $AMCE$ là hình thoi."
    ])
    
    add_exercise(doc, "14.3", "Cho hình thoi $ABCD$ có hai đường chéo $AC$ và $BD$ cắt nhau tại $O$.", [
        "a) Chứng minh các đường chéo của hình thoi vuông góc với nhau tại trung điểm.",
        "b) Gọi $E, F, G, H$ lần lượt là trung điểm của các cạnh $AB, BC, CD, DA$. Chứng minh tứ giác $EFGH$ là hình chữ nhật.",
        "c) Hình thoi $ABCD$ cần có thêm điều kiện gì để $EFGH$ là hình vuông?"
    ])

    # DẠNG 15
    add_heading_2(doc, "Dạng 15: Hình học — Định lí Thalès trong tam giác")
    add_body_paragraph(doc, "Định lí: Nếu $DE \\parallel BC$ ($D \\in AB, E \\in AC$) thì $\\frac{AD}{AB} = \\frac{AE}{AC}$ hoặc $\\frac{AD}{DB} = \\frac{AE}{EC}$.", "★")
    
    add_exercise(doc, "15.1", "Cho tam giác $ABC$ có $AB = 12\\text{ cm}, AC = 15\\text{ cm}$. Trên $AB$ lấy điểm $D$ sao cho $AD = 4\\text{ cm}$. Qua $D$ kẻ đường thẳng song song với $BC$ cắt $AC$ tại $E$.", [
        "a) Tính độ dài đoạn thẳng $AE$ và $EC$.",
        "b) Qua $E$ kẻ đường thẳng song song với $AB$ cắt $BC$ tại $F$. Tứ giác $BDEF$ là hình gì?"
    ])
    
    add_exercise(doc, "15.2", "Để đo chiều cao cột cờ, người ta cắm cọc cao 2 m cách cột cờ 12 m. Người quan sát cách cọc 3 m nhìn thấy đỉnh cọc và đỉnh cột cờ thẳng hàng. Mắt người cách mặt đất 1,6 m. Tính chiều cao cột cờ.")

    # DẠNG 16
    add_heading_2(doc, "Dạng 16: Bài toán vận dụng cao — Tìm GTNN và GTLN")
    add_body_paragraph(doc, "Quy tắc: Biến đổi về dạng $A = [f(x)]^2 + k \\ge k \\Rightarrow \\text{Min } A = k$. Biến đổi $B = k - [f(x)]^2 \\le k \\Rightarrow \\text{Max } B = k$.", "★")
    
    add_exercise(doc, "16.1", "Tìm giá trị nhỏ nhất của các biểu thức sau:", [
        "a) $A = x^2 - 6x + 14$",
        "b) $B = 4x^2 + 4x + 5$",
        "c) $C = x^2 - 8x + 20$",
        "d) $D = 2x^2 + 4x + 7$",
        "e) $P = x^2 - 4xy + 5y^2 - 6y + 19$"
    ])
    
    add_exercise(doc, "16.2", "Tìm giá trị lớn nhất của các biểu thức sau:", [
        "a) $M = 5 - 4x - x^2$",
        "b) $N = 7 - 6x - x^2$",
        "c) $E = -x^2 + 2x + 4$"
    ])

    # ==================== PHẦN II ====================
    add_heading_1(doc, "PHẦN II: BỘ 10 ĐỀ ÔN TẬP TỰ LUẬN 100% (THỜI GIAN LÀM BÀI: 60 PHÚT/ĐỀ)")
    
    # --- ĐỀ 1 ---
    add_test_header(doc, 1, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $2x(3x^2 - 4x + 1)$",
        "b) $(2x - 3)(x + 2) - 2x^2$",
        "c) $(12x^3y^2 - 8x^2y) : (4x^2y)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $A = (x + 3)^2 - (x - 2)(x + 2) - 6x$",
        "b) Tìm $x$, biết: $(2x - 1)^2 - 4x(x - 2) = 9$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một khu vườn hình chữ nhật có chiều dài gấp đôi chiều rộng. Nếu tăng chiều rộng thêm 3 m và giảm chiều dài đi 2 m thì diện tích tăng thêm 34 $\\text{m}^2$. Tính kích thước ban đầu của khu vườn.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường trung tuyến $AM$. Gọi $D$ là điểm đối xứng với $A$ qua $M$.", [
        "a) Chứng minh tứ giác $ABDC$ là hình chữ nhật.",
        "b) Gọi $I$ là trung điểm của $AC$. Kẻ $IK \\parallel BC$ ($K \\in AB$). Chứng minh $K$ là trung điểm của $AB$.",
        "c) Gọi $E$ là điểm đối xứng với $M$ qua $I$. Chứng minh tứ giác $AMCE$ là hình thoi."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $P = x^2 - 6x + 14$.")
    
    # --- ĐỀ 2 ---
    add_test_header(doc, 2, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $-3xy(2x^2 - xy + 3y^2)$",
        "b) $(3x - 1)(x + 2) - 3x(x - 1)$",
        "c) $(15x^4y^3 - 20x^3y^2) : (5x^3y^2)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $B = (2x - 1)^2 - (2x + 3)(2x - 3)$",
        "b) Tìm $x$, biết: $(x + 4)^2 - (x - 2)(x + 2) = 28$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một chiếc thang dài 5 m đặt dựa vào tường, chân thang cách tường 3 m. Tính chiều cao bức tường từ mặt đất đến đỉnh thang.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hình bình hành $ABCD$. Gọi $E$ là trung điểm của $AB$, $F$ là trung điểm của $CD$.", [
        "a) Chứng minh tứ giác $AECF$ là hình bình hành.",
        "b) Đường chéo $AC$ cắt $EF$ tại $O$. Chứng minh $O$ là trung điểm của $AC$ và $EF$.",
        "c) Gọi $M$ là giao điểm của $AF$ và $DE$, $N$ là giao điểm của $BF$ và $CE$. Chứng minh tứ giác $EMFN$ là hình bình hành."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $Q = 4x^2 + 4x + 5$.")
    
    # --- ĐỀ 3 ---
    add_test_header(doc, 3, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $4x^2(2x - 3y + 1)$",
        "b) $\\left(2x - 1\\right)\\left(2x + 1\\right) - {\\left(x + 3\\right)}^2$",
        "c) $(18x^3y^4 - 12x^2y^3 + 6xy^2) : (6xy^2)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $C = (x - 2)^2 + (x + 2)^2 - 2x^2$",
        "b) Tìm $x$, biết: $(3x - 1)^2 - 9x(x - 2) = 17$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Cho tam giác $ABC$ có $AB = 12\\text{ cm}, AC = 15\\text{ cm}$. Trên $AB$ lấy điểm $D$ sao cho $AD = 4\\text{ cm}$. Qua $D$ kẻ đường thẳng song song với $BC$ cắt $AC$ tại $E$. Tính độ dài đoạn thẳng $AE$ và $EC$.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ cân tại $A$. Gọi $M, N$ lần lượt là trung điểm của $AB$ và $AC$.", [
        "a) Chứng minh tứ giác $BMNC$ là hình thang cân.",
        "b) Lấy điểm $P$ đối xứng với $M$ qua $N$. Chứng minh tứ giác $AMCP$ là hình bình hành.",
        "c) Tam giác cân $ABC$ cần có thêm điều kiện gì để tứ giác $BMNC$ có hai đáy bằng nhau (tức là hình bình hành)?"
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị lớn nhất của biểu thức: $M = 5 - 4x - x^2$.")
    
    # --- ĐỀ 4 ---
    add_test_header(doc, 4, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $3x(2x^2 - 5x + 4)$",
        "b) $(x + 4)(x - 2) - x(x + 1)$",
        "c) $(14x^4y^2 - 21x^3y^3 + 28x^2y^4) : (7x^2y^2)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $D = (x + 1)^2 - 2(x + 1)(x - 2) + (x - 2)^2$",
        "b) Tìm $x$, biết: $(2x - 3)^2 - 4x(x - 1) = 21$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Để đo chiều cao của một cột cờ, người ta cắm một chiếc cọc cao 2 m cách cột cờ 12 m. Người quan sát cách cọc 3 m nhìn thấy đỉnh cọc và đỉnh cột cờ thẳng hàng. Mắt người cách mặt đất 1,6 m. Tính chiều cao cột cờ.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ vuông tại $A$. Gọi $D$ là trung điểm của $BC$. Từ $D$ kẻ $DH \\perp AB$ tại $H$ và $DK \\perp AC$ tại $K$.", [
        "a) Chứng minh tứ giác $AHDK$ là hình chữ nhật.",
        "b) Chứng minh $H$ là trung điểm của $AB$ và $K$ là trung điểm của $AC$.",
        "c) Lấy điểm $E$ đối xứng với $D$ qua $H$. Chứng minh tứ giác $ADBE$ là hình thoi."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $P = x^2 - 4xy + 5y^2 - 6y + 19$.")
    
    # --- ĐỀ 5 ---
    add_test_header(doc, 5, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $-2x^2y(3xy - 4x + 2y)$",
        "b) $(2x - 1)(x + 3) - 2x(x + 2)$",
        "c) $(24x^5y^3 - 16x^4y^2) : (8x^3y^2)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $E = (3x - 1)(3x + 1) - (3x - 2)^2$",
        "b) Tìm $x$, biết: $(x + 2)^2 - (x - 3)(x + 3) = 13$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một mảnh đất hình chữ nhật có chiều dài hơn chiều rộng 5 m và chu vi bằng 50 m. Tính diện tích mảnh đất ban đầu.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hình thoi $ABCD$ có hai đường chéo $AC$ và $BD$ cắt nhau tại $O$. Qua $O$ kẻ các đường thẳng song song với các cạnh của hình thoi.", [
        "a) Chứng minh các đường chéo của hình thoi vuông góc với nhau.",
        "b) Gọi $E, F, G, H$ lần lượt là trung điểm của các cạnh $AB, BC, CD, DA$. Chứng minh tứ giác $EFGH$ là hình chữ nhật.",
        "c) Hình thoi $ABCD$ cần có thêm điều kiện gì thì tứ giác $EFGH$ là hình vuông?"
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $A = x^2 - 8x + 20$.")
    
    # --- ĐỀ 6 ---
    add_test_header(doc, 6, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $5x(x^2 - 2x + 3)$",
        "b) $(x - 3)(2x + 1) - x(2x - 5)$",
        "c) $(18x^4y^3 - 12x^3y^2 + 6x^2y) : (6x^2y)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $M = (x - 3)^2 - (x - 1)(x + 1) + 6x$",
        "b) Tìm $x$, biết: $(2x + 1)^2 - 4x(x - 3) = 25$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Tính giá trị của biểu thức $P = x^3 - 3x^2 + 3x - 1$ tại $x = 101$.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ nhọn. Các đường cao $BD$ và $CE$ cắt nhau tại $H$. Gọi $M$ là trung điểm của $BC$. Điểm $K$ đối xứng với $H$ qua $M$.", [
        "a) Chứng minh tứ giác $BHCK$ là hình bình hành.",
        "b) Chứng minh $BK \\perp AB$ và $CK \\perp AC$.",
        "c) Gọi $I$ là trung điểm của $AK$. Chứng minh $I$ cách đều ba điểm $A, B, C$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị lớn nhất của biểu thức: $B = 7 - 6x - x^2$.")
    
    # --- ĐỀ 7 ---
    add_test_header(doc, 7, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $2xy(3x^2 - xy + 4y^2)$",
        "b) $(3x - 2)(2x + 1) - 6x^2$",
        "c) $(20x^3y^4 - 15x^2y^3 + 10xy^2) : (5xy^2)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $N = (2x + 3)^2 - (2x - 3)^2$",
        "b) Tìm $x$, biết: $(x - 4)^2 - (x + 2)(x - 2) = 12$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Cho tam giác $ABC$, đường thẳng $d \\parallel BC$ cắt $AB$ tại $M$ và $AC$ tại $N$. Biết $AM = 3\\text{ cm}, MB = 6\\text{ cm}, AN = 4\\text{ cm}$. Tính độ dài $NC$ và $AC$.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$. Gọi $D$ là điểm đối xứng với $H$ qua $AB$, $E$ là điểm đối xứng với $H$ qua $AC$. Gọi giao điểm của $DH$ và $AB$ là $M$, của $HE$ và $AC$ là $N$.", [
        "a) Chứng minh tứ giác $AMHN$ là hình chữ nhật.",
        "b) Chứng minh ba điểm $D, A, E$ thẳng hàng.",
        "c) Chứng minh tứ giác $BDEC$ là hình thang vuông."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $C = x^2 + 2x + 10$.")
    
    # --- ĐỀ 8 ---
    add_test_header(doc, 8, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $-4x(x^2 - 3x + 2)$",
        "b) $(2x - 5)(x + 2) - 2x(x - 1)$",
        "c) $(25x^4y^3 - 15x^3y^2) : (5x^2y^2)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $P = (x + 2)^3 - (x - 2)^3 - 12x^2$",
        "b) Tìm $x$, biết: $(3x - 2)^2 - (3x + 1)(3x - 1) = 9$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Tính nhanh giá trị của biểu thức: $A = 75^2 - 25^2$ và $B = 102 \\cdot 98$.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hình thang cân $ABCD$ ($AB \\parallel CD$, $AB < CD$). Kẻ các đường cao $AH, BK$ xuống đáy $CD$.", [
        "a) Chứng minh $\\Delta AHD = \\Delta BKC$.",
        "b) Chứng minh $DH = CK = \\frac{CD - AB}{2}$.",
        "c) Biết $AB = 6\\text{ cm}, CD = 14\\text{ cm}, AD = 5\\text{ cm}$. Tính độ dài đường cao $AH$ và diện tích hình thang cân $ABCD$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $D = 2x^2 + 4x + 7$.")
    
    # --- ĐỀ 9 ---
    add_test_header(doc, 9, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $3x^2(2x^2 - 4x + 5)$",
        "b) $(x - 1)(x^2 + x + 1) - x^3$",
        "c) $(30x^5y^4 - 24x^4y^3 + 18x^3y^2) : (6x^3y^2)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $Q = (2x - 3)^2 + 2(2x - 3)(x + 3) + (x + 3)^2$",
        "b) Tìm $x$, biết: $(x - 1)^2 - (x + 3)(x - 3) = 6$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Chứng minh rằng biểu thức sau không phụ thuộc vào biến $x$: $M = (x - 5)(2x + 3) - 2x(x - 3) + x + 7$.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho hình bình hành $ABCD$. Trên cạnh $AB$ lấy điểm $E$, trên cạnh $CD$ lấy điểm $F$ sao cho $AE = CF$.", [
        "a) Chứng minh tứ giác $AECF$ là hình bình hành.",
        "b) Chứng minh tứ giác $EBFD$ là hình bình hành.",
        "c) Gọi $O$ là giao điểm của $AC$ và $BD$. Chứng minh ba điểm $E, O, F$ thẳng hàng."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị lớn nhất của biểu thức: $E = -x^2 + 2x + 4$.")
    
    # --- ĐỀ 10 ---
    add_test_header(doc, 10, "8")
    add_exercise(doc, "1 (2,5 điểm)", "Thực hiện phép tính:", [
        "a) $2x(x^2 - 3xy + 4y^2)$",
        "b) $(2x - 3)(3x + 1) - (x - 2)(6x - 1)$",
        "c) $(16x^4y^3 - 12x^3y^2 + 8x^2y) : (4x^2y)$"
    ])
    add_exercise(doc, "2 (2,0 điểm)", "Rút gọn biểu thức và tìm $x$:", [
        "a) Rút gọn biểu thức: $R = (x + 4)^2 - (x - 4)^2 - 16x$",
        "b) Tìm $x$, biết: $(2x + 3)^2 - 4(x - 1)(x + 1) = 25$"
    ])
    add_exercise(doc, "3 (1,5 điểm)", "Một khu vườn hình vuông có cạnh $x$ mét. Người ta mở rộng về mỗi phía thêm 2 m để làm lối đi. Viết biểu thức tính diện tích phần lối đi mở rộng theo $x$.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường trung tuyến $AM$. Gọi $D$ là điểm đối xứng với $A$ qua $M$.", [
        "a) Chứng minh tứ giác $ABDC$ là hình chữ nhật.",
        "b) Lấy điểm $E$ đối xứng với $M$ qua $AB$, gọi $H$ là giao điểm của $EM$ và $AB$. Chứng minh tứ giác $AHME$ là hình chữ nhật.",
        "c) Chứng minh tứ giác $AEBM$ là hình thoi."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $S = x^2 - 4xy + 5y^2 - 2y + 10$.")
    
    # ==================== PHẦN III ====================
    add_heading_1(doc, "PHẦN III: BẢNG ĐÁP SỐ VÀ HƯỚNG DẪN GIẢI 10 ĐỀ TỰ LUẬN")
    add_answer_header(doc, 1)
    for _ans in [
        "Bài 1: a) $6x^3 - 8x^2 + 2x$; b) $x - 6$; c) $3xy - 2$.",
        "Bài 2: a) $A = 13$ (không phụ thuộc vào $x$); b) $-4x + 1 + 8x = 9 \\Rightarrow 4x = 8 \\Rightarrow x = 2$.",
        "Bài 3: Gọi chiều rộng ban đầu là $x$ (m), chiều dài là $2x$ (m). Ta có $(2x - 2)(x + 3) - 2x^2 = 34 \\Rightarrow 4x - 6 = 34 \\Rightarrow x = 10$. Chiều rộng 10 m, chiều dài 20 m.",
        "Bài 4: a) Tứ giác có 2 đường chéo cắt nhau tại trung điểm và có 1 góc vuông; b) Đường trung bình; c) Hình bình hành có $AM = MC = BC/2$ nên là hình thoi.",
        "Bài 5: $P = (x - 3)^2 + 5 \\ge 5$. GTNN là 5 khi $x = 3$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 2)
    for _ans in [
        "Bài 1: a) $-6x^3y + 3x^2y^2 - 9xy^3$; b) $8x - 2$; c) $3x - 4$.",
        "Bài 2: a) $B = -4x + 10$; b) $8x + 20 = 28 \\Rightarrow x = 1$.",
        "Bài 3: Theo định lý Pythagoras: $h = \\sqrt{5^2 - 3^2} = 4$ m.",
        "Bài 4: a) $AE = CF = AB/2$ và $AE \\parallel CF$; b) Giao điểm 2 đường chéo hình bình hành; c) Tứ giác có các cạnh đối song song.",
        "Bài 5: $Q = (2x + 1)^2 + 4 \\ge 4$. GTNN là 4 khi $x = -1/2$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 3)
    for _ans in [
        "Bài 1: a) $8x^3 - 12x^2y + 4x^2$; b) $3x^2 - 6x - 10$; c) $3x^2y^2 - 2xy + 1$.",
        "Bài 2: a) $C = 8$; b) $18x + 1 - 9x^2 + 18x \\dots \\Rightarrow 12x = 16 \\Rightarrow x = 4/3$.",
        "Bài 3: $AE = 5\\text{ cm}, EC = 10\\text{ cm}$.",
        "Bài 4: a) Hình thang có 2 góc kề đáy bằng nhau; b) Các cạnh đối song song và bằng nhau; c) Không thể xảy ra vì $MN = BC/2 < BC$.",
        "Bài 5: $M = 9 - (x + 2)^2 \\le 9$. GTLN là 9 khi $x = -2$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 4)
    for _ans in [
        "Bài 1: a) $6x^3 - 15x^2 + 12x$; b) $x - 8$; c) $2x^2 - 3xy + 4y^2$.",
        "Bài 2: a) $D = [(x+1) - (x-2)]^2 = 3^2 = 9$; b) $-8x + 9 = 21 \\Rightarrow -8x = 12 \\Rightarrow x = -1{,}5$.",
        "Bài 3: Chiều cao cột cờ: $1{,}6 + (2 - 1{,}6) \\cdot \\frac{15}{3} = 1{,}6 + 2 = 3{,}6$ m.",
        "Bài 4: a) Tứ giác có 3 góc vuông; b) Tính chất đường trung bình; c) Hình bình hành có 2 đường chéo vuông góc.",
        "Bài 5: $P = (x - 2y)^2 + (y - 3)^2 + 10 \\ge 10$. GTNN là 10 khi $y = 3, x = 6$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 5)
    for _ans in [
        "Bài 1: a) $-6x^3y^2 + 8x^3y - 4x^2y^2$; b) $x - 3$; c) $3x^2y - 2x$.",
        "Bài 2: a) $E = 12x - 5$; b) $4x + 13 = 13 \\Rightarrow x = 0$.",
        "Bài 3: Nửa chu vi là 25 m. Chiều dài 15 m, chiều rộng 10 m. Diện tích 150 $\\text{m}^2$.",
        "Bài 4: a) Tính chất hình thoi; b) Đường trung bình chứng minh cạnh đối song song và góc vuông; c) Hình vuông khi $ABCD$ là hình vuông.",
        "Bài 5: $A = (x - 4)^2 + 4 \\ge 4$. GTNN là 4 khi $x = 4$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 6)
    for _ans in [
        "Bài 1: a) $5x^3 - 10x^2 + 15x$; b) 0; c) $3x^2y^2 - 2xy + 1$.",
        "Bài 2: a) $M = 10$; b) $16x + 1 = 25 \\Rightarrow x = 1{,}5$.",
        "Bài 3: $P = (x - 1)^3 = (101 - 1)^3 = 100^3 = 1\\ 000\\ 000$.",
        "Bài 4: a) Các cạnh đối song song; b) $BK \\parallel CH \\perp AB \\Rightarrow BK \\perp AB$; c) $I$ là tâm đường tròn ngoại tiếp.",
        "Bài 5: $B = 16 - (x + 3)^2 \\le 16$. GTLN là 16 khi $x = -3$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 7)
    for _ans in [
        "Bài 1: a) $6x^3y - 2x^2y^2 + 8xy^3$; b) $-x - 2$; c) $4x^2y^2 - 3xy + 2$.",
        "Bài 2: a) $N = 24x$; b) $-8x + 20 = 12 \\Rightarrow x = 1$.",
        "Bài 3: $NC = 8\\text{ cm}, AC = 12\\text{ cm}$.",
        "Bài 4: a) Tứ giác có 3 góc vuông; b) $\\widehat{DAE} = \\widehat{DAB} + \\widehat{BAC} + \\widehat{CAE} = 180^\\circ$; c) $BD \\parallel CE$ và vuông góc với $DE$.",
        "Bài 5: $C = (x + 1)^2 + 9 \\ge 9$. GTNN là 9 khi $x = -1$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 8)
    for _ans in [
        "Bài 1: a) $-4x^3 + 12x^2 - 8x$; b) $x - 10$; c) $5x^2y - 3x$.",
        "Bài 2: a) $P = 16$; b) $-12x + 5 = 9 \\Rightarrow x = -1/3$.",
        "Bài 3: $A = (75 - 25)(75 + 25) = 5000$; $B = (100 + 2)(100 - 2) = 10000 - 4 = 9996$.",
        "Bài 4: a) Cạnh huyền - góc nhọn; b) $DH = CK = 4\\text{ cm}$; c) $AH = 3\\text{ cm}$, diện tích 30 $\\text{m}^2$.",
        "Bài 5: $D = 2(x + 1)^2 + 5 \\ge 5$. GTNN là 5 khi $x = -1$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 9)
    for _ans in [
        "Bài 1: a) $6x^4 - 12x^3 + 15x^2$; b) $-1$; c) $5x^2y^2 - 4xy + 3$.",
        "Bài 2: a) $Q = [(2x - 3) + (x + 3)]^2 = 9x^2$; b) $-2x + 10 = 6 \\Rightarrow x = 2$.",
        "Bài 3: $M = 2x^2 - 7x - 15 - 2x^2 + 6x + x + 7 = -8$ (hằng số).",
        "Bài 4: a) $AE = CF$ và $AE \\parallel CF$; b) $BE = DF$ và $BE \\parallel DF$; c) $EF$ đi qua trung điểm $O$ của $AC$.",
        "Bài 5: $E = 5 - (x - 1)^2 \\le 5$. GTLN là 5 khi $x = 1$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 10)
    for _ans in [
        "Bài 1: a) $2x^3 - 6x^2y + 8xy^2$; b) $6x - 5$; c) $4x^2y^2 - 3xy + 2$.",
        "Bài 2: a) $R = 0$; b) $12x + 13 = 25 \\Rightarrow x = 1$.",
        "Bài 3: Diện tích ban đầu $x^2$, diện tích sau $(x + 4)^2$. Diện tích lối đi: $(x + 4)^2 - x^2 = 8x + 16$ ($\\text{m}^2$).",
        "Bài 4: a) Tứ giác có 2 đường chéo cắt nhau tại trung điểm và có 1 góc vuông; b) 3 góc vuông; c) Hình bình hành có 2 đường chéo vuông góc.",
        "Bài 5: $S = (x - 2y)^2 + (y - 1)^2 + 9 \\ge 9$. GTNN là 9 khi $y = 1, x = 2$."
    ]:
        add_answer_item(doc, _ans)

    doc.save(output_path)
    print(f"[TOAN 8 - 2026-2027] Saved successfully to: {output_path}")

if __name__ == "__main__":
    import datetime
    today = datetime.datetime.now().strftime("%d.%m")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "2_TAO_BAI_TAP", "Ket_qua", today)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "De_Cuong_On_Tap_Giua_HK1_Toan_8.docx")
    build_de_cuong_toan_8(out_file)
