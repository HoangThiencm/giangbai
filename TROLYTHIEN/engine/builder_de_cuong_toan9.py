# -*- coding: utf-8 -*-
"""
BIÊN SOẠN ĐỀ CƯƠNG ÔN TẬP GIỮA HỌC KỲ I - TOÁN 9 (PHIÊN BẢN CHUẨN THỰC CHIẾN MỞ RỘNG)
NĂM HỌC: 2026 - 2027 (Đã bỏ cấp Phòng GD&ĐT, chỉ dùng TRƯỜNG THCS TRẦN PHÚ / TỔ TOÁN - TIN)
TẬP TRUNG:
1. Ngân hàng bài tập rèn kỹ năng thực chiến cực kỳ dày dặn (20 dạng toán chuyên sâu cho học sinh yếu, trung bình đến khá giỏi).
2. Bộ 10 Đề ôn tập tự luận 100% (thời gian làm bài: 60 phút/đề) bám sát cấu trúc phân hóa chuẩn.
3. 100% Công thức toán là Microsoft Word Equation (OMML m:oMath), căn thức, hệ phương trình hiển thị chuẩn mực.
"""

import os
from de_cuong_docx_helper import (
    create_base_document, add_header_quoc_hieu, add_heading_1, add_heading_2,
    add_heading_3, add_body_paragraph, add_exercise, add_test_header, add_answer_header, add_answer_item
)

def build_de_cuong_toan_9(output_path):
    doc = create_base_document()
    add_header_quoc_hieu(doc, "9", school_year="2026 - 2027")
    
    # =========================================================================
    # PHẦN I: CÁC DẠNG BÀI TẬP RÈN KỸ NĂNG THỰC CHIẾN (20 DẠNG CHUYÊN SÂU)
    # =========================================================================
    add_heading_1(doc, "PHẦN I: CÁC DẠNG BÀI TẬP RÈN KỸ NĂNG THỰC CHIẾN (DÀNH CHO HỌC SINH YẾU, TRUNG BÌNH & KHÁ)")
    
    # ----------------------------- CHỦ ĐỀ 1 -----------------------------
    add_heading_2(doc, "A. HỆ HAI PHƯƠNG TRÌNH VÀ PHƯƠNG TRÌNH BẬC NHẤT")
    
    # DẠNG 1
    add_heading_3(doc, "Dạng 1: Giải hệ hai phương trình bậc nhất hai ẩn bằng phương pháp cộng đại số")
    add_body_paragraph(doc, "Kỹ năng cần nắm: \n- Trường hợp 1: Hệ số của cùng một ẩn đối nhau thì cộng hai vế của phương trình; bằng nhau thì trừ hai vế để triệt tiêu ẩn đó.\n- Trường hợp 2: Hệ số chưa bằng/đối nhau: Nhân hai vế của một (hoặc cả hai) phương trình với số thích hợp để đưa về Trường hợp 1.\n- Tìm được một ẩn rồi thay vào phương trình đơn giản để tìm ẩn còn lại. Kết luận cặp nghiệm (x; y).", "★")
    
    add_exercise(doc, "1.1", "Giải các hệ phương trình sau bằng phương pháp cộng đại số:", [
        "a) $\\begin{cases} x + y = 5 \\\\ x - y = 1 \\end{cases}$",
        "b) $\\begin{cases} 2x + y = 7 \\\\ x - y = 2 \\end{cases}$",
        "c) $\\begin{cases} 3x - 2y = 4 \\\\ x + 2y = 8 \\end{cases}$",
        "d) $\\begin{cases} 2x + 3y = 8 \\\\ 2x - y = 4 \\end{cases}$",
        "e) $\\begin{cases} 4x - 5y = 3 \\\\ 4x + y = 15 \\end{cases}$",
        "f) $\\begin{cases} -x + 3y = 5 \\\\ x + 2y = 5 \\end{cases}$"
    ])
    
    add_exercise(doc, "1.2", "Giải các hệ phương trình sau:", [
        "a) $\\begin{cases} 2x - y = 5 \\\\ 3x + 2y = 11 \\end{cases}$",
        "b) $\\begin{cases} 3x + 2y = 8 \\\\ 2x - y = 3 \\end{cases}$",
        "c) $\\begin{cases} x - 3y = -2 \\\\ 2x + 5y = 7 \\end{cases}$",
        "d) $\\begin{cases} 4x + y = 11 \\\\ 3x - 2y = 0 \\end{cases}$",
        "e) $\\begin{cases} 5x - 2y = 9 \\\\ x + 3y = 7 \\end{cases}$",
        "f) $\\begin{cases} 2x + 5y = 1 \\\\ 6x - y = 19 \\end{cases}$"
    ])
    
    add_exercise(doc, "1.3", "Giải các hệ phương trình sau:", [
        "a) $\\begin{cases} 2x + 3y = 7 \\\\ 3x + 2y = 8 \\end{cases}$",
        "b) $\\begin{cases} 3x + 5y = 1 \\\\ 2x - 3y = 7 \\end{cases}$",
        "c) $\\begin{cases} 4x + 3y = 6 \\\\ 3x - 2y = 13 \\end{cases}$",
        "d) $\\begin{cases} 5x + 3y = -1 \\\\ 3x - 2y = 7 \\end{cases}$",
        "e) $\\begin{cases} 7x - 2y = 1 \\\\ 3x + 4y = 10 \\end{cases}$",
        "f) $\\begin{cases} 2x + 5y = 9 \\\\ 3x - 4y = 2 \\end{cases}$"
    ])
    
    # DẠNG 2
    add_heading_3(doc, "Dạng 2: Giải hệ hai phương trình bậc nhất hai ẩn bằng phương pháp thế")
    add_body_paragraph(doc, "Kỹ năng cần nắm: Rút một ẩn có hệ số là 1 hoặc -1 từ một phương trình rồi thế biểu thức đó vào phương trình còn lại để thu được phương trình một ẩn. Giải tìm ẩn đó rồi thay ngược lại tìm nốt ẩn kia.", "★")
    
    add_exercise(doc, "2.1", "Giải các hệ phương trình sau bằng phương pháp thế:", [
        "a) $\\begin{cases} x - 2y = 1 \\\\ 2x + y = 7 \\end{cases}$",
        "b) $\\begin{cases} 3x - y = 7 \\\\ x + 2y = 7 \\end{cases}$",
        "c) $\\begin{cases} 2x + 3y = 12 \\\\ x - y = 1 \\end{cases}$",
        "d) $\\begin{cases} x + 4y = 9 \\\\ 3x - 2y = 13 \\end{cases}$",
        "e) $\\begin{cases} 4x - y = 5 \\\\ 2x + 3y = 13 \\end{cases}$",
        "f) $\\begin{cases} 5x + y = 11 \\\\ 3x - 2y = 4 \\end{cases}$"
    ])
    
    # DẠNG 3
    add_heading_3(doc, "Dạng 3: Hệ phương trình chứa dấu ngoặc hoặc chứa mẫu số cần quy đồng")
    add_body_paragraph(doc, "Kỹ năng cần nắm: Thực hiện nhân phá ngoặc, chuyển vế, thu gọn các hạng tử đồng dạng để đưa hệ về dạng chính tắc $\\begin{cases} ax + by = c \\\\ a'x + b'y = c' \\end{cases}$ rồi áp dụng phương pháp cộng đại số.", "★")
    
    add_exercise(doc, "3.1", "Biến đổi và giải các hệ phương trình sau:", [
        "a) $\\begin{cases} 2(x + y) + 3(x - y) = 4 \\\\ (x + y) - 2(x - y) = 9 \\end{cases}$",
        "b) $\\begin{cases} 3(x + 1) - 2(y - 2) = 7 \\\\ 2(x - 2) + 3(y + 1) = 9 \\end{cases}$",
        "c) $\\begin{cases} (x + 2)(y - 1) = xy + 1 \\\\ (x - 1)(y + 2) = xy + 5 \\end{cases}$",
        "d) $\\begin{cases} 2(2x + 3y) - 3(x - y) = 11 \\\\ 4(x - 2y) + 3(2x + y) = 7 \\end{cases}$"
    ])
    
    add_exercise(doc, "3.2", "Quy đồng mẫu số và giải các hệ phương trình sau:", [
        "a) $\\begin{cases} \\frac{x}{2} + \\frac{y}{3} = 4 \\\\ x - y = 3 \\end{cases}$",
        "b) $\\begin{cases} \\frac{x + 1}{3} - \\frac{y + 2}{4} = 0 \\\\ \\frac{x - 1}{2} + \\frac{y - 1}{3} = 2 \\end{cases}$",
        "c) $\\begin{cases} \\frac{2x - 1}{3} + \\frac{y + 1}{2} = 3 \\\\ \\frac{x + 2}{4} - \\frac{2y - 1}{3} = 1 \\end{cases}$",
        "d) $\\begin{cases} \\frac{x}{3} - \\frac{y}{4} = 1 \\\\ 2x + 3y = 28 \\end{cases}$"
    ])
    
    # DẠNG 4
    add_heading_3(doc, "Dạng 4: Giải hệ phương trình bằng phương pháp đặt ẩn phụ")
    add_body_paragraph(doc, "Kỹ năng cần nắm: Nhận diện biểu thức chung giống nhau ở cả hai phương trình $\\to$ Đặt ẩn phụ (chú ý đặt ĐKXĐ nếu có mẫu hoặc căn) $\\to$ Giải hệ bậc nhất đối với ẩn phụ $\\to$ Thay ngược lại để tìm $x, y$.", "★")
    
    add_exercise(doc, "4.1", "Giải các hệ phương trình sau:", [
        "a) $\\begin{cases} \\frac{1}{x} + \\frac{1}{y} = 5 \\\\ \\frac{2}{x} - \\frac{3}{y} = -5 \\end{cases}$",
        "b) $\\begin{cases} \\frac{2}{x} + \\frac{3}{y} = 7 \\\\ \\frac{3}{x} - \\frac{1}{y} = 5 \\end{cases}$",
        "c) $\\begin{cases} \\frac{1}{x - 1} + \\frac{1}{y + 1} = 3 \\\\ \\frac{2}{x - 1} - \\frac{3}{y + 1} = 1 \\end{cases}$",
        "d) $\\begin{cases} \\frac{3}{2x - 1} + \\frac{2}{y + 2} = 4 \\\\ \\frac{1}{2x - 1} - \\frac{1}{y + 2} = 3 \\end{cases}$"
    ])
    
    add_exercise(doc, "4.2", "Giải các hệ phương trình sau:", [
        "a) $\\begin{cases} 2\\sqrt{x} + 3\\sqrt{y} = 8 \\\\ 3\\sqrt{x} - \\sqrt{y} = 1 \\end{cases}$",
        "b) $\\begin{cases} 3\\sqrt{x - 1} + 2\\sqrt{y + 2} = 7 \\\\ \\sqrt{x - 1} - \\sqrt{y + 2} = -1 \\end{cases}$",
        "c) $\\begin{cases} 2(x + 1)^2 + 3(y - 2)^2 = 11 \\\\ (x + 1)^2 - 2(y - 2)^2 = -5 \\end{cases}$",
        "d) $\\begin{cases} |x - 2| + 2|y + 1| = 5 \\\\ 3|x - 2| - |y + 1| = 1 \\end{cases}$"
    ])
    
    # DẠNG 5
    add_heading_3(doc, "Dạng 5: Phương trình tích")
    add_body_paragraph(doc, "Kỹ năng cần nắm: $A(x) \\cdot B(x) = 0 \\Rightarrow A(x) = 0$ hoặc $B(x) = 0$.\nĐối với phương trình chưa có dạng tích: Chuyển toàn bộ các số hạng sang vế trái để vế phải bằng 0 $\\to$ Đặt nhân tử chung, dùng hằng đẳng thức hoặc tách hạng tử để đưa về dạng tích.", "★")
    
    add_exercise(doc, "5.1", "Giải các phương trình sau:", [
        "a) $(2x - 3)(x + 4) = 0$",
        "b) $(3x - 1)(2x + 5) = 0$",
        "c) $(4x + 1)(3 - x) = 0$",
        "d) $(x - 5)(2x + 7) = 0$",
        "e) $x(2x - 8) = 0$",
        "f) $(5x - 2)(3x - 9) = 0$"
    ])
    
    add_exercise(doc, "5.2", "Giải các phương trình sau:", [
        "a) $x^2 - 4x = 0$",
        "b) $2x^2 + 6x = 0$",
        "c) $x(x - 5) + 3(x - 5) = 0$",
        "d) $2x(x + 1) - (x + 1) = 0$",
        "e) $x^2 - 9 = 0$",
        "f) $4x^2 - 25 = 0$",
        "g) $(2x - 1)^2 - 9 = 0$",
        "h) $(x + 3)^2 - 16 = 0$"
    ])
    
    add_exercise(doc, "5.3", "Giải các phương trình sau:", [
        "a) $x^2 - 5x + 6 = 0$",
        "b) $x^2 - 7x + 12 = 0$",
        "c) $x^2 + 5x + 4 = 0$",
        "d) $x^2 - x - 6 = 0$",
        "e) $2x^2 - 5x + 2 = 0$",
        "f) $3x^2 + 5x - 2 = 0$"
    ])
    
    # DẠNG 6
    add_heading_3(doc, "Dạng 6: Phương trình chứa ẩn ở mẫu")
    add_body_paragraph(doc, "Kỹ năng thực chiến 4 bước: \n- Bước 1: Tìm ĐKXĐ (các mẫu số khác 0).\n- Bước 2: Quy đồng mẫu hai vế và khử mẫu.\n- Bước 3: Giải phương trình vừa nhận được.\n- Bước 4: Đối chiếu giá trị tìm được với ĐKXĐ để loại nghiệm ngoại lai và kết luận tập nghiệm $S$.", "★")
    
    add_exercise(doc, "6.1", "Giải các phương trình sau:", [
        "a) $\\frac{x + 2}{x - 2} = 3$",
        "b) $\\frac{2x - 1}{x + 1} = 1$",
        "c) $\\frac{3x + 1}{x - 3} = 2$",
        "d) $\\frac{x + 3}{x + 1} = 2$",
        "e) $\\frac{2x - 3}{x + 2} = \\frac{1}{2}$",
        "f) $\\frac{4x + 1}{2x - 1} = 3$"
    ])
    
    add_exercise(doc, "6.2", "Giải các phương trình sau:", [
        "a) $\\frac{1}{x - 1} + \\frac{2}{x + 1} = \\frac{4}{x^2 - 1}$",
        "b) $\\frac{x + 1}{x - 1} - \\frac{x - 1}{x + 1} = \\frac{4}{x^2 - 1}$",
        "c) $\\frac{3}{x - 2} + \\frac{2}{x + 2} = \\frac{8}{x^2 - 4}$",
        "d) $\\frac{x + 2}{x} - \\frac{x}{x + 2} = \\frac{4}{x(x + 2)}$",
        "e) $\\frac{2}{x - 3} - \\frac{1}{x} = \\frac{6}{x(x - 3)}$",
        "f) $\\frac{x - 3}{x - 1} = \\frac{x + 1}{x + 3}$"
    ])
    
    # ----------------------------- CHỦ ĐỀ 2 -----------------------------
    add_heading_2(doc, "B. BẤT ĐẲNG THỨC VÀ BẤT PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN")
    
    # DẠNG 7
    add_heading_3(doc, "Dạng 7: Chứng minh bất đẳng thức đơn giản")
    add_body_paragraph(doc, "Kỹ năng cần nắm: Để chứng minh $A \\ge B$, ta xét hiệu $A - B$ rồi biến đổi đưa về bình phương một tổng hoặc một hiệu: $A - B = (M)^2 \\ge 0$.", "★")
    
    add_exercise(doc, "7.1", "Chứng minh các bất đẳng thức sau với mọi số thực:", [
        "a) $x^2 + 2x + 2 > 0$",
        "b) $x^2 - 4x + 5 > 0$",
        "c) $(a + b)^2 \\ge 4ab$",
        "d) $a^2 + b^2 \\ge 2ab$",
        "e) Cho $a > b$, chứng minh $2a + 3 > 2b + 3$.",
        "f) Cho $a < b$, chứng minh $-3a + 5 > -3b + 5$."
    ])
    
    # DẠNG 8
    add_heading_3(doc, "Dạng 8: Giải bất phương trình bậc nhất một ẩn và biểu diễn tập nghiệm trên trục số")
    add_body_paragraph(doc, "Kỹ năng sống còn: \n- Quy tắc chuyển vế: Chuyển hạng tử từ vế này sang vế kia thì đổi dấu hạng tử đó.\n- Quy tắc nhân: Khi nhân hoặc chia hai vế với một số ÂM thì BẮT BUỘC ĐỔI CHIỀU bất phương trình.", "★")
    
    add_exercise(doc, "8.1", "Giải các bất phương trình sau và biểu diễn tập nghiệm trên trục số:", [
        "a) $2x - 5 > 3$",
        "b) $3x + 1 \\le 10$",
        "c) $4 - 2x \\ge 8$",
        "d) $-3x + 6 < 0$",
        "e) $5x - 7 \\ge 2x + 8$",
        "f) $3 - 4x > 11 - 2x$"
    ])
    
    add_exercise(doc, "8.2", "Giải các bất phương trình sau:", [
        "a) $3(x - 2) < 5x + 4$",
        "b) $2(3x + 1) - 4 \\ge 3(x - 2) + 1$",
        "c) $\\frac{2x - 1}{3} > \\frac{x + 2}{2}$",
        "d) $\\frac{x - 1}{4} - \\frac{2x + 1}{3} \\le 1$",
        "e) $\\frac{2x - 1}{3} - \\frac{x + 2}{2} > \\frac{3x - 5}{6}$",
        "f) $\\frac{3x + 5}{2} - 1 \\le \\frac{x + 2}{3} + x$"
    ])
    
    # ----------------------------- CHỦ ĐỀ 3 -----------------------------
    add_heading_2(doc, "C. CĂN THỨC BẬC HAI VÀ RÚT GỌN BIỂU THỨC")
    
    # DẠNG 9
    add_heading_3(doc, "Dạng 9: Điều kiện xác định (ĐKXĐ) của căn thức bậc hai")
    add_body_paragraph(doc, "Kỹ năng cần nắm: \n- Biểu thức $\\sqrt{A}$ có nghĩa khi $A \\ge 0$.\n- Biểu thức $\\frac{1}{\\sqrt{A}}$ có nghĩa khi $A > 0$.\n- Biểu thức chứa nhiều căn thức: Lập hệ các điều kiện cùng lớn hơn hoặc bằng 0.", "★")
    
    add_exercise(doc, "9.1", "Tìm điều kiện của $x$ để mỗi căn thức sau có nghĩa:", [
        "a) $\\sqrt{2x - 6}$",
        "b) $\\sqrt{5 - x}$",
        "c) $\\sqrt{3x + 12}$",
        "d) $\\sqrt{8 - 4x}$",
        "e) $\\sqrt{2x + 10}$",
        "f) $\\sqrt{15 - 5x}$",
        "g) $\\sqrt{4x - 16}$",
        "h) $\\sqrt{9 - 3x}$"
    ])
    
    add_exercise(doc, "9.2", "Tìm điều kiện của $x$ để mỗi biểu thức sau xác định:", [
        "a) $\\frac{1}{\\sqrt{x - 2}}$",
        "b) $\\frac{1}{\\sqrt{2x - 4}}$",
        "c) $\\frac{3}{\\sqrt{5 - 2x}}$",
        "d) $\\sqrt{x^2 + 1}$",
        "e) $\\sqrt{x^2 + 4}$",
        "f) $\\sqrt{x - 1} + \\frac{1}{x - 3}$"
    ])
    
    # DẠNG 10
    add_heading_3(doc, "Dạng 10: Rút gọn căn thức số bằng hằng đẳng thức $\\sqrt{A^2} = |A|$")
    add_body_paragraph(doc, "Kỹ năng cần nắm: \n- $\\sqrt{A^2} = |A| = A$ nếu $A \\ge 0$; $|A| = -A$ nếu $A < 0$.\n- Tách biểu thức dưới dấu căn dạng $a \\pm 2\\sqrt{b} = (\\sqrt{x} \\pm \\sqrt{y})^2$ để khử căn bậc hai bên ngoài.", "★")
    
    add_exercise(doc, "10.1", "Thực hiện phép tính và rút gọn:", [
        "a) $\\sqrt{(3 - \\sqrt{5})^2} + \\sqrt{5}$",
        "b) $\\sqrt{(2 - \\sqrt{7})^2} - \\sqrt{7}$",
        "c) $\\sqrt{(\\sqrt{3} - 2)^2} + \\sqrt{3}$",
        "d) $\\sqrt{(4 - \\sqrt{15})^2} + \\sqrt{15}$",
        "e) $\\sqrt{(\\sqrt{6} - 3)^2} + \\sqrt{6}$",
        "f) $\\sqrt{(5 - \\sqrt{21})^2} + \\sqrt{21}$"
    ])
    
    add_exercise(doc, "10.2", "Rút gọn các biểu thức sau:", [
        "a) $A = \\sqrt{7 - 4\\sqrt{3}} + \\sqrt{3}$",
        "b) $B = \\sqrt{9 - 4\\sqrt{5}} + \\sqrt{5}$",
        "c) $C = \\sqrt{14 - 6\\sqrt{5}} + \\sqrt{5}$",
        "d) $D = \\sqrt{11 - 6\\sqrt{2}} + \\sqrt{2}$",
        "e) $E = \\sqrt{8 - 2\\sqrt{7}} - \\sqrt{7}$",
        "f) $F = \\sqrt{12 - 2\\sqrt{35}} + \\sqrt{7} - \\sqrt{5}$"
    ])
    
    # DẠNG 11
    add_heading_3(doc, "Dạng 11: Rút gọn biểu thức chứa căn bậc hai và chữ số biến")
    add_body_paragraph(doc, "Kỹ năng cần nắm: Phân tích mẫu số thành nhân tử $\\to$ Quy đồng mẫu thức chung $\\to$ Nhân phối hợp và thu gọn tử $\\to$ Rút gọn nhân tử chung giữa tử và mẫu.", "★")
    
    add_exercise(doc, "11.1", "Cho biểu thức $P = \\left( \\frac{1}{\\sqrt{x} - 1} - \\frac{1}{\\sqrt{x} + 1} \\right) : \\frac{2}{x - 1}$ (với $x \\ge 0, x \\neq 1$).", [
        "a) Rút gọn biểu thức $P$.",
        "b) Tính giá trị của biểu thức $P$ khi $x = 4$."
    ])
    
    add_exercise(doc, "11.2", "Cho biểu thức $A = \\left( \\frac{\\sqrt{x}}{\\sqrt{x} + 2} + \\frac{2}{\\sqrt{x} - 2} \\right) : \\frac{x + 4}{x - 4}$ (với $x \\ge 0, x \\neq 4$).", [
        "a) Rút gọn biểu thức $A$.",
        "b) Tìm giá trị của $x$ để $A = 1$."
    ])
    
    add_exercise(doc, "11.3", "Cho biểu thức $B = \\left( \\frac{x - \\sqrt{x}}{\\sqrt{x} - 1} - \\frac{x + \\sqrt{x}}{\\sqrt{x} + 1} \\right) + 1$ (với $x \\ge 0, x \\neq 1$).", [
        "a) Rút gọn biểu thức $B$.",
        "b) Tìm $x$ để biểu thức $B < 0$."
    ])
    
    # ----------------------------- CHỦ ĐỀ 4 -----------------------------
    add_heading_2(doc, "D. GIẢI BÀI TOÁN BẰNG CÁCH LẬP HỆ PHƯƠNG TRÌNH (TOÁN THỰC TẾ)")
    
    # DẠNG 12
    add_heading_3(doc, "Dạng 12: Bài toán chuyển động")
    add_body_paragraph(doc, "Công thức then chốt: $s = v \\cdot t$; $v = \\frac{s}{t}$; $t = \\frac{s}{v}$.\nChuyển động dòng nước: $v_{\\text{xuôi}} = v_{\\text{riêng}} + v_{\\text{nước}}$; $v_{\\text{ngược}} = v_{\\text{riêng}} - v_{\\text{nước}}$.", "★")
    
    add_exercise(doc, "12.1", "Hai ô tô cùng khởi hành từ hai bến xe $A$ và $B$ cách nhau 180 km, đi ngược chiều và gặp nhau sau 2 giờ. Biết vận tốc xe đi từ $A$ lớn hơn vận tốc xe đi từ $B$ là 10 km/h. Tính vận tốc của mỗi xe.")
    
    add_exercise(doc, "12.2", "Hai người đi xe đạp cùng khởi hành từ hai địa điểm cách nhau 42 km và đi ngược chiều nhau. Sau 2 giờ họ gặp nhau. Tính vận tốc mỗi người biết vận tốc người thứ nhất lớn hơn người thứ hai là 3 km/h.")
    
    add_exercise(doc, "12.3", "Một ca nô xuôi dòng 45 km rồi ngược dòng 18 km hết tổng cộng 3 giờ. Biết vận tốc của dòng nước là 3 km/h. Tính vận tốc riêng của ca nô khi nước yên lặng.")
    
    # DẠNG 13
    add_heading_3(doc, "Dạng 13: Bài toán hình học (Chu vi và diện tích hình chữ nhật)")
    add_body_paragraph(doc, "Công thức: Nửa chu vi = Dài + Rộng. Diện tích = Dài $\\times$ Rộng.", "★")
    
    add_exercise(doc, "13.1", "Một khu vườn hình chữ nhật có chu vi là 140 m. Nếu giảm chiều dài 10 m và tăng chiều rộng 5 m thì diện tích không đổi. Tính chiều dài và chiều rộng ban đầu của khu vườn.")
    
    add_exercise(doc, "13.2", "Một mảnh đất hình chữ nhật có chu vi 72 m. Chiều dài hơn chiều rộng 12 m. Tính diện tích mảnh đất đó bằng cách lập hệ phương trình.")
    
    add_exercise(doc, "13.3", "Một hình chữ nhật có chu vi 100 m. Nếu tăng chiều rộng thêm 5 m và giảm chiều dài 5 m thì diện tích tăng thêm 50 $\\text{m}^2$. Tính diện tích hình chữ nhật ban đầu.")
    
    # DẠNG 14
    add_heading_3(doc, "Dạng 14: Bài toán năng suất, làm chung làm riêng và phần trăm")
    add_body_paragraph(doc, "Quy ước: Khối lượng toàn bộ công việc là 1 đơn vị. Trong 1 ngày (hoặc 1 giờ), năng suất bằng $\\frac{1}{\\text{thời gian hoàn thành}}$.", "★")
    
    add_exercise(doc, "14.1", "Hai đội công nhân cùng làm chung một đoạn đường thì sau 12 ngày hoàn thành. Nếu đội thứ nhất làm một mình 4 ngày rồi nghỉ, đội thứ hai làm tiếp một mình 9 ngày thì cả hai làm được $\\frac{7}{12}$ đoạn đường. Hỏi mỗi đội làm một mình thì sau bao nhiêu ngày hoàn thành?")
    
    add_exercise(doc, "14.2", "Hai tổ sản xuất được giao làm tổng cộng 800 sản phẩm. Do cải tiến kỹ thuật, tổ 1 vượt mức 15%, tổ 2 vượt mức 20% nên cả hai tổ làm được tất cả 945 sản phẩm. Hỏi theo kế hoạch ban đầu mỗi tổ được giao làm bao nhiêu sản phẩm?")
    
    add_exercise(doc, "14.3", "Đầu năm học, bác Nam mua một bộ SGK và một chiếc cặp sách giá niêm yết tổng cộng 600 000 đồng. Nhân dịp khai giảng, SGK được giảm giá 10% và cặp sách giảm giá 15% nên bác Nam chỉ phải trả 522 000 đồng. Tính giá niêm yết của mỗi loại sản phẩm.")
    
    add_exercise(doc, "14.4", "Một lớp học có 40 học sinh. Trong đợt quyên góp sách giáo khoa cũ ủng hộ các bạn học sinh vùng bão lũ, mỗi bạn nam đóng góp 3 quyển, mỗi bạn nữ đóng góp 2 quyển. Tổng số sách lớp quyên góp được là 105 quyển. Hỏi lớp có bao nhiêu bạn nam, bao nhiêu bạn nữ?")
    
    # ----------------------------- CHỦ ĐỀ 5 -----------------------------
    add_heading_2(doc, "E. HỆ THỨC LƯỢNG TRONG TAM GIÁC VUÔNG VÀ TOÁN THỰC TẾ")
    
    # DẠNG 15
    add_heading_3(doc, "Dạng 15: Tính cạnh và đường cao trong tam giác vuông bằng hệ thức lượng")
    add_body_paragraph(doc, "Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$:\n- $BC^2 = AB^2 + AC^2$ (Định lý Pythagoras).\n- $AB^2 = BH \\cdot BC; \\quad AC^2 = CH \\cdot BC$.\n- $AH^2 = BH \\cdot CH$.\n- $AB \\cdot AC = BC \\cdot AH$.\n- $\\frac{1}{AH^2} = \\frac{1}{AB^2} + \\frac{1}{AC^2}$.", "★")
    
    add_exercise(doc, "15.1", "Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$. Tính các độ dài còn lại trong mỗi trường hợp sau:", [
        "a) Cho $AB = 6\\text{ cm}, AC = 8\\text{ cm}$. Tính $BC, AH, BH, CH$.",
        "b) Cho $AB = 9\\text{ cm}, BC = 15\\text{ cm}$. Tính $AC, AH, BH, CH$.",
        "c) Cho $BH = 4\\text{ cm}, CH = 9\\text{ cm}$. Tính $AH, AB, AC$.",
        "d) Cho $BH = 2\\text{ cm}, BC = 8\\text{ cm}$. Tính $AB, AC, AH$."
    ])
    
    add_exercise(doc, "15.2", "Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$. Kẻ $HM \\perp AB$ tại $M, HN \\perp AC$ tại $N$.", [
        "a) Chứng minh tứ giác $AMHN$ là hình chữ nhật và $MN = AH$.",
        "b) Chứng minh $AM \\cdot AB = AN \\cdot AC = AH^2$."
    ])
    
    # DẠNG 16
    add_heading_3(doc, "Dạng 16: Tỉ số lượng giác và Giải tam giác vuông")
    add_body_paragraph(doc, "Tỉ số: $\\sin = \\frac{\\text{đối}}{\\text{huyền}}; \\cos = \\frac{\\text{kề}}{\\text{huyền}}; \\tan = \\frac{\\text{đối}}{\\text{kề}}; \\cot = \\frac{\\text{kề}}{\\text{đối}}$.\nCạnh góc vuông = Cạnh huyền $\\times \\sin$ góc đối = Cạnh huyền $\\times \\cos$ góc kề.", "★")
    
    add_exercise(doc, "16.1", "Cho tam giác $ABC$ vuông tại $A$ có $AB = 6\\text{ cm}, AC = 8\\text{ cm}$.", [
        "a) Tính độ dài cạnh huyền $BC$.",
        "b) Tính các tỉ số lượng giác của góc $B$: $\\sin B, \\cos B, \\tan B$.",
        "c) Từ đó suy ra tỉ số lượng giác của góc $C$."
    ])
    
    add_exercise(doc, "16.2", "Giải tam giác $ABC$ vuông tại $A$ trong các trường hợp sau (làm tròn số đo góc đến độ):", [
        "a) Biết cạnh huyền $BC = 12\\text{ cm}$ và $\\widehat{B} = 30^\\circ$.",
        "b) Biết cạnh góc vuông $AB = 7\\text{ cm}$ và $\\widehat{C} = 40^\\circ$."
    ])
    
    # DẠNG 17
    add_heading_3(doc, "Dạng 17: Toán thực tế ứng dụng tỉ số lượng giác (Đo bóng nắng, góc nghiêng)")
    add_body_paragraph(doc, "Mô hình hóa hình học: Biến bài toán thực tế thành tam giác vuông với chiều cao, khoảng cách và góc nghiêng cho trước $\\to$ Dùng $\\tan$ hoặc $\\sin$ để tính.", "★")
    
    add_exercise(doc, "17.1", "Một cột cờ thẳng đứng có bóng trên mặt đất dài 12 m. Góc tạo bởi tia nắng mặt trời và mặt đất bằng $35^\\circ$. Tính chiều cao cột cờ (làm tròn đến hàng phần mười).")
    
    add_exercise(doc, "17.2", "Một chiếc thang dài 4 m đặt dựa vào tường tạo với mặt đất một góc $65^\\circ$.", [
        "a) Tính chiều cao từ mặt đất đến đỉnh thang chạm tường (làm tròn đến hai chữ số thập phân).",
        "b) Chân thang cách tường bao nhiêu mét?",
        "c) Để đảm bảo an toàn, góc nghiêng lý tưởng là $60^\\circ$. Khi đó chân thang phải cách tường bao nhiêu mét?"
    ])
    
    add_exercise(doc, "17.3", "Một cột phát sóng cao 30 m được cố định bằng một dây cáp từ đỉnh cột xuống mặt đất. Góc tạo bởi dây cáp và mặt đất bằng $40^\\circ$.", [
        "a) Tính chiều dài dây cáp (làm tròn đến hàng phần mười mét).",
        "b) Điểm néo dây cáp trên mặt đất cách chân cột bao nhiêu mét?"
    ])
    
    # ----------------------------- CHỦ ĐỀ 6 -----------------------------
    add_heading_2(doc, "F. ĐƯỜNG TRÒN, DÂY CUNG VÀ TIẾP TUYẾN")
    
    # DẠNG 18
    add_heading_3(doc, "Dạng 18: Quan hệ vuông góc giữa đường kính và dây cung")
    add_body_paragraph(doc, "Định lý: Trong một đường tròn, đường kính vuông góc với một dây thì đi qua trung điểm của dây ấy.\nTam giác vuông Pythagoras: $R^2 = OH^2 + AH^2 = OH^2 + \\left(\\frac{AB}{2}\\right)^2$.", "★")
    
    add_exercise(doc, "18.1", "Cho đường tròn $(O; 10\\text{ cm})$ và dây $AB = 16\\text{ cm}$. Kẻ $OH \\perp AB$ tại $H$.", [
        "a) Tính độ dài đoạn thẳng $AH$.",
        "b) Tính khoảng cách $OH$ từ tâm $O$ đến dây $AB$."
    ])
    
    add_exercise(doc, "18.2", "Cho đường tròn $(O; 13\\text{ cm})$ và dây $CD = 24\\text{ cm}$. Kẻ $OH \\perp CD$ tại $H$.", [
        "a) Tính độ dài khoảng cách $OH$.",
        "b) Đường thẳng $OH$ cắt đường tròn $(O)$ tại điểm $M$ ($M$ thuộc cung nhỏ $CD$). Tính độ dài đoạn thẳng $MH$."
    ])
    
    add_exercise(doc, "18.3", "Cho đường tròn $(O; R)$ có dây $AB = 8\\text{ cm}$. Khoảng cách từ tâm $O$ đến dây $AB$ bằng 3 cm. Tính bán kính $R$ của đường tròn $(O)$.")
    
    # DẠNG 19
    add_heading_3(doc, "Dạng 19: Tiếp tuyến của đường tròn và tính chất hai tiếp tuyến cắt nhau")
    add_body_paragraph(doc, "Tính chất hai tiếp tuyến cắt nhau tại $M$ ($MA, MB$ là tiếp tuyến): \n- $MA = MB$.\n- $MO$ là tia phân giác của góc $\\widehat{AMB}$.\n- $OM$ là tia phân giác của góc $\\widehat{AOB}$.\n- $MO$ là đường trung trực của đoạn thẳng $AB$.", "★")
    
    add_exercise(doc, "19.1", "Cho đường tròn $(O; R)$ và một điểm $A$ nằm ngoài đường tròn. Kẻ hai tiếp tuyến $AB$ và $AC$ với đường tròn ($B, C$ là các tiếp điểm). Gọi $H$ là giao điểm của $OA$ và $BC$.", [
        "a) Chứng minh $OA \\perp BC$ tại $H$ và $H$ là trung điểm của $BC$.",
        "b) Cho $R = 6\\text{ cm}$ và $OA = 10\\text{ cm}$. Tính độ dài các tiếp tuyến $AB, AC$ và độ dài đoạn thẳng $BC$."
    ])
    
    add_exercise(doc, "19.2", "Cho nửa đường tròn tâm $O$ đường kính $AB$. Trên cùng một nửa mặt phẳng bờ $AB$, vẽ các tiếp tuyến $Ax, By$ với nửa đường tròn. Lấy điểm $M$ bất kỳ trên nửa đường tròn. Tiếp tuyến tại $M$ cắt $Ax$ tại $C$ và cắt $By$ tại $D$.", [
        "a) Chứng minh $CD = AC + BD$.",
        "b) Chứng minh tam giác $COD$ vuông tại $O$.",
        "c) Chứng minh tích $AC \\cdot BD = R^2$ (không đổi)."
    ])
    
    # ----------------------------- CHỦ ĐỀ 7 -----------------------------
    add_heading_2(doc, "G. BÀI TOÁN NÂNG CAO VẬN DỤNG TƯ DUY (LẤY ĐIỂM 10)")
    
    # DẠNG 20
    add_heading_3(doc, "Dạng 20: Tìm giá trị lớn nhất, giá trị nhỏ nhất của biểu thức chứa căn hoặc BĐT Cauchy")
    add_body_paragraph(doc, "Phương pháp biến đổi thêm bớt đưa về bình phương: \n- $A = x - 2k\\sqrt{x - a} + C = (x - a) - 2k\\sqrt{x - a} + k^2 + (C + a - k^2) = (\\sqrt{x - a} - k)^2 + M \\ge M$.\n- Áp dụng BĐT Cauchy: $a + b \\ge 2\\sqrt{ab}$ (với $a, b > 0$). Dấu bằng xảy ra khi $a = b$.", "★")
    
    add_exercise(doc, "20.1", "Tìm giá trị nhỏ nhất của các biểu thức sau:", [
        "a) $M = x - 4\\sqrt{x - 1} + 2028$ (với $x \\ge 1$).",
        "b) $N = x - 2\\sqrt{x - 3} + 5$ (với $x \\ge 3$).",
        "c) $Q = x - 6\\sqrt{x - 2} + 2035$ (với $x \\ge 2$).",
        "d) $T = x - 8\\sqrt{x - 4} + 2040$ (với $x \\ge 4$)."
    ])
    
    add_exercise(doc, "20.2", "Chứng minh bất đẳng thức và tìm cực trị:", [
        "a) Cho hai số dương $x, y$ thoả mãn $x + y = 2$. Tìm giá trị nhỏ nhất của $P = \\frac{1}{x} + \\frac{1}{y}$.",
        "b) Cho hai số dương $a, b$ thoả mãn $a + b = 4$. Chứng minh rằng $\\frac{1}{a} + \\frac{1}{b} \\ge 1$."
    ])
    
    # =========================================================================
    # PHẦN II: BỘ 10 ĐỀ ÔN TẬP TỰ LUẬN 100% (60 PHÚT/ĐỀ)
    # =========================================================================
    add_heading_1(doc, "PHẦN II: BỘ 10 ĐỀ ÔN TẬP TỰ LUẬN 100% (THỜI GIAN LÀM BÀI: 60 PHÚT/ĐỀ)")
    
    # --- ĐỀ 1 ---
    add_test_header(doc, 1, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 2x - y = 5 \\\\ 3x + 2y = 11 \\end{cases}$",
        "b) $(2x - 3)(x + 4) = 0$",
        "c) $\\frac{x + 2}{x - 2} = 3$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{2x - 8}$.",
        "b) Rút gọn biểu thức: $A = \\sqrt{(3 - \\sqrt{5})^2} + \\sqrt{5}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Hai ô tô cùng khởi hành từ hai bến xe $A$ và $B$ cách nhau 180 km, đi ngược chiều và gặp nhau sau 2 giờ. Biết vận tốc xe đi từ $A$ lớn hơn vận tốc xe đi từ $B$ là 10 km/h. Tính vận tốc của mỗi xe.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho đường tròn $(O; 5\\text{ cm})$ đường kính $AB$. Dây $CD \\perp AB$ tại $H$ ($H$ nằm giữa $O$ và $B$) sao cho $OH = 3\\text{ cm}$.", [
        "a) Chứng minh $H$ là trung điểm của dây $CD$ và tính độ dài dây $CD$.",
        "b) Kẻ tiếp tuyến tại $C$ của $(O)$ cắt tia $AB$ tại $E$. Tính độ dài đoạn thẳng $CE$.",
        "c) Chứng minh $ED$ là tiếp tuyến của đường tròn $(O)$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $M = x - 4\\sqrt{x - 1} + 2028$ (với $x \\ge 1$).")
    
    # --- ĐỀ 2 ---
    add_test_header(doc, 2, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 3x + y = 10 \\\\ 2x - 3y = 3 \\end{cases}$",
        "b) $(3x - 1)(x + 2) = 0$",
        "c) $\\frac{2x - 1}{x + 1} = 1$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{6 - 3x}$.",
        "b) Rút gọn biểu thức: $B = \\sqrt{7 - 4\\sqrt{3}} + \\sqrt{3}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Một khu vườn hình chữ nhật có chu vi là 140 m. Nếu giảm chiều dài 10 m và tăng chiều rộng 5 m thì diện tích không đổi. Tính chiều dài và chiều rộng ban đầu của khu vườn.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ vuông tại $A$ có $AB = 6\\text{ cm}, AC = 8\\text{ cm}$, đường cao $AH$.", [
        "a) Tính độ dài cạnh $BC$ và đường cao $AH$.",
        "b) Tính tỉ số lượng giác $\\sin B$ và $\\cos B$.",
        "c) Kẻ $HM \\perp AB$ tại $M, HN \\perp AC$ tại $N$. Chứng minh $AM \\cdot AB = AN \\cdot AC$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $N = x - 2\\sqrt{x - 3} + 5$ (với $x \\ge 3$).")
    
    # --- ĐỀ 3 ---
    add_test_header(doc, 3, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 4x + 3y = 6 \\\\ 2x - y = 8 \\end{cases}$",
        "b) $x^2 - 4x = 0$",
        "c) $\\frac{1}{x - 1} + \\frac{2}{x + 1} = \\frac{4}{x^2 - 1}$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{4x + 8}$.",
        "b) Rút gọn: $C = \\sqrt{(2 - \\sqrt{7})^2} - \\sqrt{7}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Đầu năm học, bác Nam mua một bộ SGK và một chiếc cặp sách giá niêm yết tổng cộng 600 000 đồng. Nhân dịp khai giảng, SGK được giảm giá 10% và cặp sách giảm giá 15% nên bác Nam chỉ trả 522 000 đồng. Tính giá niêm yết mỗi loại.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho đường tròn $(O; 10\\text{ cm})$ và dây $CD = 16\\text{ cm}$. Kẻ $OH \\perp CD$ tại $H$.", [
        "a) Tính độ dài đoạn thẳng $OH$.",
        "b) Kẻ đường kính $AB \\perp CD$ tại $H$ ($A$ thuộc cung lớn $CD$). Tính độ dài $AH$ và $BH$.",
        "c) Chứng minh tam giác $ACD$ cân tại $A$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Giải hệ phương trình khi $m = 2$: $\\begin{cases} (m - 1)x + y = 2 \\\\ mx + y = m + 1 \\end{cases}$.")
    
    # --- ĐỀ 4 ---
    add_test_header(doc, 4, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 3x + 5y = 1 \\\\ 2x - y = 5 \\end{cases}$",
        "b) $(x - 3)(2x + 1) = 0$",
        "c) $\\frac{x + 3}{x + 1} = 2$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{9 - 3x}$.",
        "b) Rút gọn: $D = \\sqrt{9 - 4\\sqrt{5}} + \\sqrt{5}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Hai đội công nhân cùng làm chung một đoạn đường thì sau 12 ngày xong. Nếu đội 1 làm một mình 4 ngày rồi nghỉ, đội 2 làm tiếp 9 ngày thì cả hai làm được $\\frac{7}{12}$ đoạn đường. Hỏi mỗi đội làm một mình thì bao nhiêu ngày xong?")
    add_exercise(doc, "4 (3,0 điểm)", "Một chiếc thang dài 4 m đặt dựa vào tường tạo với mặt đất góc $65^\\circ$.", [
        "a) Tính chiều cao từ mặt đất đến đỉnh thang (làm tròn đến hàng phần trăm).",
        "b) Chân thang cách tường bao nhiêu mét?",
        "c) Để thang tạo góc an toàn $60^\\circ$ thì chân thang phải cách tường bao nhiêu mét?"
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của $P = \\frac{1}{x} + \\frac{1}{y}$ với $x > 0, y > 0$ và $x + y = 2$.")
    
    # --- ĐỀ 5 ---
    add_test_header(doc, 5, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 5x + 2y = 9 \\\\ 2x - 3y = 11 \\end{cases}$",
        "b) $(2x - 1)^2 - 9 = 0$",
        "c) $\\frac{x + 1}{x - 1} - \\frac{x - 1}{x + 1} = \\frac{4}{x^2 - 1}$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\frac{1}{\\sqrt{2x - 4}}$.",
        "b) Rút gọn: $E = \\sqrt{(\\sqrt{3} - 2)^2} + \\sqrt{3}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Một ca nô xuôi dòng 45 km rồi ngược dòng 18 km hết tổng cộng 3 giờ. Biết vận tốc dòng nước là 3 km/h. Tính vận tốc riêng của ca nô.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho đường tròn $(O; R)$ có dây $AB = 8\\text{ cm}$. Khoảng cách từ tâm $O$ đến dây $AB$ bằng 3 cm.", [
        "a) Tính bán kính $R$ của đường tròn $(O)$.",
        "b) Gọi $C$ là điểm trên tia đối của tia $AB$ sao cho $BC = 1\\text{ cm}$. Kẻ $OD \\perp AC$ tại $D$. Tính độ dài $OD$.",
        "c) Kẻ tiếp tuyến $CE$ với đường tròn $(O)$ ($E$ là tiếp điểm). Tính độ dài đoạn thẳng $CE$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Giải bất phương trình: $\\frac{2x - 1}{3} - \\frac{x + 2}{2} > \\frac{3x - 5}{6}$.")
    
    # --- ĐỀ 6 ---
    add_test_header(doc, 6, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 3x - 2y = 12 \\\\ 4x + 5y = -7 \\end{cases}$",
        "b) $x^2 - 5x + 6 = 0$",
        "c) $\\frac{3}{x - 2} + \\frac{2}{x + 2} = \\frac{8}{x^2 - 4}$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{x^2 + 1}$.",
        "b) Rút gọn: $F = \\sqrt{14 - 6\\sqrt{5}} + \\sqrt{5}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Một hình chữ nhật có chu vi 100 m. Nếu tăng chiều rộng thêm 5 m và giảm chiều dài 5 m thì diện tích tăng thêm 50 $\\text{m}^2$. Tính diện tích hình chữ nhật ban đầu.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ vuông tại $A$ có $\\widehat{B} = 30^\\circ$ và $BC = 12\\text{ cm}$.", [
        "a) Tính độ dài các cạnh $AC$ và $AB$.",
        "b) Kẻ đường cao $AH$. Tính $AH$ và $BH$.",
        "c) Kẻ đường phân giác $AD$ của góc $A$ ($D \\in BC$). Tính độ dài đoạn thẳng $BD$ và $CD$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm $m$ để hệ phương trình có nghiệm duy nhất thoả mãn $x + y = 4$: $\\begin{cases} (m - 1)x + y = 2 \\\\ mx + y = m + 1 \\end{cases}$.")
    
    # --- ĐỀ 7 ---
    add_test_header(doc, 7, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 2x + 3y = -2 \\\\ 3x - 2y = -16 \\end{cases}$",
        "b) $(3x - 2)(x + 1) = 0$",
        "c) $\\frac{x - 3}{x - 1} = \\frac{x + 1}{x + 3}$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{8 - 4x}$.",
        "b) Rút gọn: $G = \\sqrt{(4 - \\sqrt{15})^2} + \\sqrt{15}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Hai tổ sản xuất được giao làm 800 sản phẩm. Do cải tiến kỹ thuật, tổ 1 vượt mức 15%, tổ 2 vượt mức 20% nên cả hai tổ làm được 945 sản phẩm. Hỏi kế hoạch ban đầu mỗi tổ được giao bao nhiêu sản phẩm?")
    add_exercise(doc, "4 (3,0 điểm)", "Cho đường tròn $(O; 13\\text{ cm})$ và dây $AB = 24\\text{ cm}$.", [
        "a) Kẻ $OH \\perp AB$ tại $H$. Tính độ dài đoạn thẳng $OH$.",
        "b) Gọi $M$ là điểm thuộc dây $AB$ sao cho $AM = 7\\text{ cm}$. Kẻ $OK \\perp AB$ tại $K$. Tính độ dài $OM$.",
        "c) Kẻ tiếp tuyến tại $A$ của $(O)$ cắt tia $OH$ tại $P$. Tính độ dài đoạn thẳng $AP$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $Q = x - 6\\sqrt{x - 2} + 2035$ (với $x \\ge 2$).")
    
    # --- ĐỀ 8 ---
    add_test_header(doc, 8, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 7x - 2y = 1 \\\\ 3x + y = 6 \\end{cases}$",
        "b) $2x(x - 4) + 3(x - 4) = 0$",
        "c) $\\frac{x + 2}{x} - \\frac{x}{x + 2} = \\frac{4}{x^2 + 2x}$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{2x + 10}$.",
        "b) Rút gọn: $H = \\sqrt{(\\sqrt{6} - 3)^2} + \\sqrt{6}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Một mảnh đất hình chữ nhật có chu vi 72 m. Chiều dài hơn chiều rộng 12 m. Tính diện tích mảnh đất đó bằng cách lập hệ phương trình.")
    add_exercise(doc, "4 (3,0 điểm)", "Một cột phát sóng cao 30 m được cố định bằng một dây cáp từ đỉnh cột xuống mặt đất. Góc tạo bởi dây cáp và mặt đất bằng $40^\\circ$.", [
        "a) Tính chiều dài dây cáp (làm tròn đến hàng phần mười).",
        "b) Điểm néo dây cáp trên mặt đất cách chân cột bao nhiêu mét?",
        "c) Nếu cắm thêm một dây cáp thứ hai tạo với mặt đất góc $50^\\circ$ thì dây cáp thứ hai dài bao nhiêu mét?"
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Giải hệ phương trình bằng cách đặt ẩn phụ: $\\begin{cases} \\frac{1}{x} + \\frac{1}{y} = 5 \\\\ \\frac{2}{x} - \\frac{3}{y} = -5 \\end{cases}$.")
    
    # --- ĐỀ 9 ---
    add_test_header(doc, 9, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 3x + 4y = 7 \\\\ 2x - y = 1 \\end{cases}$",
        "b) $(x + 5)^2 - 16 = 0$",
        "c) $\\frac{2}{x - 3} - \\frac{1}{x} = \\frac{6}{x^2 - 3x}$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{15 - 5x}$.",
        "b) Rút gọn: $K = \\sqrt{11 - 6\\sqrt{2}} + \\sqrt{2}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Hai người đi xe đạp cùng khởi hành từ hai địa điểm cách nhau 42 km và đi ngược chiều nhau. Sau 2 giờ họ gặp nhau. Tính vận tốc mỗi người biết vận tốc người thứ nhất lớn hơn người thứ hai là 3 km/h.")
    add_exercise(doc, "4 (3,0 điểm)", "Cho đường tròn $(O; R)$ có hai dây $AB$ và $CD$ bằng nhau và vuông góc với nhau tại $I$.", [
        "a) Kẻ $OH \\perp AB$ tại $H, OK \\perp CD$ tại $K$. Chứng minh tứ giác $OHIK$ là hình vuông.",
        "b) Biết $AB = CD = 14\\text{ cm}$ và khoảng cách từ tâm $O$ đến mỗi dây bằng 5 cm. Tính bán kính $R$.",
        "c) Tính độ dài đoạn thẳng $OI$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Tìm giá trị nhỏ nhất của biểu thức: $T = x - 8\\sqrt{x - 4} + 2040$ (với $x \\ge 4$).")
    
    # --- ĐỀ 10 ---
    add_test_header(doc, 10, "9")
    add_exercise(doc, "1 (2,5 điểm)", "Giải các phương trình và hệ phương trình sau:", [
        "a) $\\begin{cases} 5x - 3y = 1 \\\\ 2x + y = 7 \\end{cases}$",
        "b) $(2x - 5)(3x + 1) = 0$",
        "c) $\\frac{x + 1}{x - 2} = \\frac{x - 1}{x + 2}$"
    ])
    add_exercise(doc, "2 (1,5 điểm)", "Rút gọn các biểu thức sau:", [
        "a) Tìm điều kiện xác định của $\\sqrt{4x - 16}$.",
        "b) Rút gọn: $L = \\sqrt{(5 - \\sqrt{21})^2} + \\sqrt{21}$"
    ])
    add_exercise(doc, "3 (2,0 điểm)", "Một lớp học có 40 học sinh. Trong đợt quyên góp sách giáo khoa cũ ủng hộ vùng bão lũ, mỗi bạn nam đóng góp 3 quyển, mỗi bạn nữ đóng góp 2 quyển. Tổng số sách quyên góp được là 105 quyển. Hỏi lớp có bao nhiêu bạn nam, bao nhiêu bạn nữ?")
    add_exercise(doc, "4 (3,0 điểm)", "Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$.", [
        "a) Biết $BH = 4\\text{ cm}, CH = 9\\text{ cm}$. Tính độ dài đoạn thẳng $AH, AB$ và $AC$.",
        "b) Kẻ đường tròn tâm $A$ bán kính $AH$. Kẻ tiếp tuyến $BD$ và $CE$ với $(A)$ ($D, E$ là các tiếp điểm khác $H$). Chứng minh ba điểm $D, A, E$ thẳng hàng.",
        "c) Chứng minh tứ giác $BDEC$ là hình thang vuông và $DE = BD + CE$."
    ])
    add_exercise(doc, "5 (1,0 điểm)", "Cho hai số dương $a, b$ thoả mãn $a + b = 4$. Chứng minh rằng $\\frac{1}{a} + \\frac{1}{b} \\ge 1$.")
    
    # =========================================================================
    # PHẦN III: BẢNG ĐÁP SỐ VÀ HƯỚNG DẪN GIẢI 10 ĐỀ TỰ LUẬN
    # =========================================================================
    add_heading_1(doc, "PHẦN III: BẢNG ĐÁP SỐ VÀ HƯỚNG DẪN GIẢI 10 ĐỀ TỰ LUẬN")
    add_answer_header(doc, 1)
    for _ans in [
        "Bài 1: a) Nghiệm $(3; 1)$; b) $x \\in \\{3/2; -4\\}$; c) $x + 2 = 3(x - 2) \\Rightarrow 2x = 8 \\Rightarrow x = 4$ (thoả mãn ĐKXĐ $x \\neq 2$).",
        "Bài 2: a) $2x - 8 \\ge 0 \\Rightarrow x \\ge 4$; b) $A = |3 - \\sqrt{5}| + \\sqrt{5} = 3 - \\sqrt{5} + \\sqrt{5} = 3$.",
        "Bài 3: Gọi vận tốc xe đi từ $A$ là $x$ (km/h), xe đi từ $B$ là $y$ (km/h) ($x > y > 0$). Ta có hệ: $\\begin{cases} x - y = 10 \\\\ 2x + 2y = 180 \\end{cases} \\Rightarrow \\begin{cases} x = 50 \\\\ y = 40 \\end{cases}$. Vậy vận tốc xe đi từ $A$ là 50 km/h, xe đi từ $B$ là 40 km/h.",
        "Bài 4: a) $H$ là trung điểm của $CD$ vì đường kính $AB \\perp CD$. Trong tam giác vuông $OHC$: $CH = \\sqrt{OC^2 - OH^2} = \\sqrt{5^2 - 3^2} = 4\\text{ cm} \\Rightarrow CD = 2CH = 8\\text{ cm}$; b) $OC^2 = OH \\cdot OE \\Rightarrow OE = \\frac{25}{3}\\text{ cm} \\Rightarrow CE = \\sqrt{OE^2 - OC^2} = \\frac{20}{3}\\text{ cm}$; c) $\\Delta OCE = \\Delta ODE$ (c-g-c) $\\Rightarrow \\widehat{ODE} = \\widehat{OCE} = 90^\\circ \\Rightarrow ED$ là tiếp tuyến của $(O)$.",
        "Bài 5: $M = (\\sqrt{x - 1} - 2)^2 + 2024 \\ge 2024$. Dấu bằng xảy ra khi $\\sqrt{x - 1} = 2 \\Rightarrow x = 5$. Vậy GTNN của $M$ là 2024."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 2)
    for _ans in [
        "Bài 1: a) Nghiệm $(3; 1)$; b) $x \\in \\{1/3; -2\\}$; c) $2x - 1 = x + 1 \\Rightarrow x = 2$ (thoả mãn ĐKXĐ $x \\neq -1$).",
        "Bài 2: a) $6 - 3x \\ge 0 \\Rightarrow x \\le 2$; b) $B = \\sqrt{(2 - \\sqrt{3})^2} + \\sqrt{3} = |2 - \\sqrt{3}| + \\sqrt{3} = 2$.",
        "Bài 3: Gọi chiều dài ban đầu là $x$ (m), chiều rộng ban đầu là $y$ (m) ($x > y > 0$). Ta có hệ: $\\begin{cases} x + y = 70 \\\\ (x - 10)(y + 5) = xy \\end{cases} \\Rightarrow \\begin{cases} x = 50 \\\\ y = 20 \\end{cases}$. Chiều dài 50 m, chiều rộng 20 m.",
        "Bài 4: a) $BC = \\sqrt{6^2 + 8^2} = 10\\text{ cm}, AH = \\frac{AB \\cdot AC}{BC} = 4{,}8\\text{ cm}$; b) $\\sin B = \\frac{AC}{BC} = \\frac{4}{5}, \\cos B = \\frac{AB}{BC} = \\frac{3}{5}$; c) Áp dụng hệ thức lượng cho $\\Delta AHB$ và $\\Delta AHC$ vuông: $AM \\cdot AB = AH^2$ và $AN \\cdot AC = AH^2 \\Rightarrow AM \\cdot AB = AN \\cdot AC$.",
        "Bài 5: $N = (\\sqrt{x - 3} - 1)^2 + 4 \\ge 4$. Dấu bằng xảy ra khi $x = 4$. Vậy GTNN là 4."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 3)
    for _ans in [
        "Bài 1: a) Nghiệm $(3; -2)$; b) $x(x - 4) = 0 \\Rightarrow x \\in \\{0; 4\\}$; c) ĐKXĐ: $x \\neq \\pm 1$. Khử mẫu: $(x + 1) + 2(x - 1) = 4 \\Rightarrow 3x - 1 = 4 \\Rightarrow x = \\frac{5}{3}$ (thoả mãn).",
        "Bài 2: a) $4x + 8 \\ge 0 \\Rightarrow x \\ge -2$; b) $C = |2 - \\sqrt{7}| - \\sqrt{7} = \\sqrt{7} - 2 - \\sqrt{7} = -2$.",
        "Bài 3: Gọi giá niêm yết SGK là $x$ (đồng), cặp sách là $y$ (đồng). Ta có hệ: $\\begin{cases} x + y = 600000 \\\\ 0{,}9x + 0{,}85y = 522000 \\end{cases} \\Rightarrow \\begin{cases} x = 360000 \\\\ y = 240000 \\end{cases}$.",
        "Bài 4: a) $H$ là trung điểm của $CD \\Rightarrow CH = 8\\text{ cm}$. Trong $\\Delta OCH$ vuông: $OH = \\sqrt{10^2 - 8^2} = 6\\text{ cm}$; b) $AH = OA + OH = 10 + 6 = 16\\text{ cm}, BH = OB - OH = 10 - 6 = 4\\text{ cm}$; c) $AB$ là trung trực của đoạn $CD$ nên $AC = AD \\Rightarrow \\Delta ACD$ cân tại $A$.",
        "Bài 5: Khi $m = 2$: $\\begin{cases} x + y = 2 \\\\ 2x + y = 3 \\end{cases} \\Rightarrow x = 1, y = 1$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 4)
    for _ans in [
        "Bài 1: a) Nghiệm $(2; -1)$; b) $x \\in \\{3; -1/2\\}$; c) $x + 3 = 2(x + 1) \\Rightarrow x = 1$ (thoả mãn ĐKXĐ $x \\neq -1$).",
        "Bài 2: a) $9 - 3x \\ge 0 \\Rightarrow x \\le 3$; b) $D = \\sqrt{(\\sqrt{5} - 2)^2} + \\sqrt{5} = |\\sqrt{5} - 2| + \\sqrt{5} = 2\\sqrt{5} - 2$.",
        "Bài 3: Gọi thời gian đội 1, đội 2 làm một mình xong việc lần lượt là $x, y$ (ngày) ($x, y > 12$). Ta có hệ: $\\begin{cases} \\frac{1}{x} + \\frac{1}{y} = \\frac{1}{12} \\\\ \\frac{4}{x} + \\frac{9}{y} = \\frac{7}{12} \\end{cases} \\Rightarrow \\begin{cases} x = 20 \\\\ y = 30 \\end{cases}$. Đội 1 làm trong 20 ngày, đội 2 làm trong 30 ngày.",
        "Bài 4: a) Chiều cao: $h = 4 \\cdot \\sin 65^\\circ \\approx 3{,}63$ m; b) Khoảng cách chân thang: $d = 4 \\cdot \\cos 65^\\circ \\approx 1{,}69$ m; c) Khoảng cách mới: $d' = 4 \\cdot \\cos 60^\\circ = 2$ m.",
        "Bài 5: Áp dụng BĐT Cauchy: $P = \\frac{x + y}{xy} = \\frac{2}{xy} \\ge \\frac{2}{[(x+y)/2]^2} = 2$. GTNN là 2 khi $x = y = 1$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 5)
    for _ans in [
        "Bài 1: a) Nghiệm $(1; 2)$; b) $(2x - 1)^2 = 9 \\Rightarrow 2x - 1 = \\pm 3 \\Rightarrow x = 2$ hoặc $x = -1$; c) ĐKXĐ: $x \\neq \\pm 1$. Khử mẫu: $(x + 1)^2 - (x - 1)^2 = 4 \\Rightarrow 4x = 4 \\Rightarrow x = 1$ (loại vì vi phạm ĐKXĐ). Phương trình vô nghiệm.",
        "Bài 2: a) $2x - 4 > 0 \\Rightarrow x > 2$; b) $E = |\\sqrt{3} - 2| + \\sqrt{3} = 2 - \\sqrt{3} + \\sqrt{3} = 2$.",
        "Bài 3: Gọi vận tốc riêng ca nô là $v$ (km/h) ($v > 3$). Ta có: $\\frac{45}{v + 3} + \\frac{18}{v - 3} = 3 \\Rightarrow v = 21$ (km/h).",
        "Bài 4: a) Kẻ $OH \\perp AB \\Rightarrow H$ là trung điểm $AB \\Rightarrow AH = 4\\text{ cm}$. Bán kính $R = \\sqrt{OH^2 + AH^2} = \\sqrt{3^2 + 4^2} = 5\\text{ cm}$; b) $C$ thuộc tia đối của $AB \\Rightarrow AC = AB + BC = 9\\text{ cm}$. $D$ là trung điểm $AC \\Rightarrow AD = 4{,}5\\text{ cm} \\Rightarrow HD = 0{,}5\\text{ cm}$. Tính được $OD = \\sqrt{OH^2 + HD^2} = \\sqrt{3^2 + 0{,}5^2} = \\sqrt{9{,}25}\\text{ cm}$; c) Tiếp tuyến $CE = \\sqrt{OC^2 - R^2}$.",
        "Bài 5: Quy đồng mẫu chung là 6: $2(2x - 1) - 3(x + 2) > 3x - 5 \\Rightarrow x - 8 > 3x - 5 \\Rightarrow -2x > 3 \\Rightarrow x < -1{,}5$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 6)
    for _ans in [
        "Bài 1: a) Nghiệm $(2; -3)$; b) $(x - 2)(x - 3) = 0 \\Rightarrow x \\in \\{2; 3\\}$; c) ĐKXĐ: $x \\neq \\pm 2$. Khử mẫu: $3(x + 2) + 2(x - 2) = 8 \\Rightarrow 5x + 2 = 8 \\Rightarrow x = 1{,}2$ (thoả mãn).",
        "Bài 2: a) $x^2 + 1 > 0$ với mọi $x$, vậy biểu thức luôn xác định với mọi số thực $x$; b) $F = \\sqrt{(3 - \\sqrt{5})^2} + \\sqrt{5} = |3 - \\sqrt{5}| + \\sqrt{5} = 3$.",
        "Bài 3: Chiều dài ban đầu là 30 m, chiều rộng ban đầu là 20 m. Diện tích ban đầu là $30 \\times 20 = 600\\text{ m}^2$.",
        "Bài 4: a) $AC = BC \\cdot \\sin 30^\\circ = 6\\text{ cm}, AB = BC \\cdot \\cos 30^\\circ = 6\\sqrt{3}\\text{ cm}$; b) $AH = \\frac{AB \\cdot AC}{BC} = 3\\sqrt{3}\\text{ cm}, BH = \\frac{AB^2}{BC} = 9\\text{ cm}$; c) Tính theo tính chất đường phân giác trong tam giác: $\\frac{DB}{DC} = \\frac{AB}{AC} = \\sqrt{3} \\Rightarrow BD = 12(2\\sqrt{3} - 3)\\text{ cm}, CD = 12(4 - 2\\sqrt{3})\\text{ cm}$.",
        "Bài 5: Trừ vế với vế ta được $x = m - 1 \\Rightarrow y = 2 - (m - 1)^2$. Thay vào điều kiện $x + y = 4$ để tìm các giá trị của $m$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 7)
    for _ans in [
        "Bài 1: a) Nghiệm $(-4; 2)$; b) $x \\in \\{2/3; -1\\}$; c) ĐKXĐ: $x \\neq 1, x \\neq -3$. $(x - 3)(x + 3) = (x - 1)(x + 1) \\Rightarrow x^2 - 9 = x^2 - 1 \\Rightarrow -9 = -1$ (vô lý). Phương trình vô nghiệm.",
        "Bài 2: a) $8 - 4x \\ge 0 \\Rightarrow x \\le 2$; b) $G = |4 - \\sqrt{15}| + \\sqrt{15} = 4$.",
        "Bài 3: Gọi số sản phẩm tổ 1 và tổ 2 theo kế hoạch là $x, y$. Ta có: $\\begin{cases} x + y = 800 \\\\ 1{,}15x + 1{,}20y = 945 \\end{cases} \\Rightarrow \\begin{cases} x = 300 \\\\ y = 500 \\end{cases}$.",
        "Bài 4: a) $H$ là trung điểm $AB \\Rightarrow AH = 12\\text{ cm}$. $OH = \\sqrt{13^2 - 12^2} = 5\\text{ cm}$; b) $H$ cách $A$ là 12 cm, $M$ cách $A$ là 7 cm $\\Rightarrow HM = 5\\text{ cm} \\Rightarrow OM = \\sqrt{OH^2 + HM^2} = \\sqrt{5^2 + 5^2} = 5\\sqrt{2}\\text{ cm}$; c) Trong $\\Delta OAP$ vuông tại $A$, đường cao $AH$: $AP = \\frac{OA \\cdot AH}{OH} = \\frac{13 \\cdot 12}{5} = 31{,}2\\text{ cm}$.",
        "Bài 5: $Q = (\\sqrt{x - 2} - 3)^2 + 2024 \\ge 2024$. GTNN là 2024 khi $x = 11$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 8)
    for _ans in [
        "Bài 1: a) Nghiệm $(1; 3)$; b) $(x - 4)(2x + 3) = 0 \\Rightarrow x \\in \\{4; -1{,}5\\}$; c) ĐKXĐ: $x \\neq 0, x \\neq -2$. Quy đồng khử mẫu: $(x + 2)^2 - x^2 = 4 \\Rightarrow 4x + 4 = 4 \\Rightarrow x = 0$ (loại vì vi phạm ĐKXĐ). Phương trình vô nghiệm.",
        "Bài 2: a) $2x + 10 \\ge 0 \\Rightarrow x \\ge -5$; b) $H = |\\sqrt{6} - 3| + \\sqrt{6} = 3 - \\sqrt{6} + \\sqrt{6} = 3$.",
        "Bài 3: Nửa chu vi là 36 m. Hệ phương trình: $\\begin{cases} x + y = 36 \\\\ x - y = 12 \\end{cases} \\Rightarrow x = 24\\text{ m}, y = 12\\text{ m}$. Diện tích là $24 \\times 12 = 288\\text{ m}^2$.",
        "Bài 4: a) Chiều dài dây cáp: $L_1 = \\frac{30}{\\sin 40^\\circ} \\approx 46{,}7$ m; b) Khoảng cách chân cột: $d = \\frac{30}{\\tan 40^\\circ} \\approx 35{,}8$ m; c) Dây cáp thứ hai: $L_2 = \\frac{30}{\\sin 50^\\circ} \\approx 39{,}2$ m.",
        "Bài 5: Đặt $u = \\frac{1}{x}, v = \\frac{1}{y}$. Hệ trở thành $\\begin{cases} u + v = 5 \\\\ 2u - 3v = -5 \\end{cases} \\Rightarrow \\begin{cases} u = 2 \\\\ v = 3 \\end{cases} \\Rightarrow x = \\frac{1}{2}, y = \\frac{1}{3}$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 9)
    for _ans in [
        "Bài 1: a) Nghiệm $(1; 1)$; b) $(x + 5)^2 = 16 \\Rightarrow x + 5 = \\pm 4 \\Rightarrow x = -1$ hoặc $x = -9$; c) ĐKXĐ: $x \\neq 0, x \\neq 3$. Khử mẫu: $2x - (x - 3) = 6 \\Rightarrow x + 3 = 6 \\Rightarrow x = 3$ (loại vì vi phạm ĐKXĐ). Phương trình vô nghiệm.",
        "Bài 2: a) $15 - 5x \\ge 0 \\Rightarrow x \\le 3$; b) $K = \\sqrt{(3 - \\sqrt{2})^2} + \\sqrt{2} = |3 - \\sqrt{2}| + \\sqrt{2} = 3$.",
        "Bài 3: Hệ phương trình: $\\begin{cases} x - y = 3 \\\\ 2x + 2y = 42 \\end{cases} \\Rightarrow \\begin{cases} x = 12 \\\\ y = 9 \\end{cases}$. Vận tốc người thứ nhất là 12 km/h, người thứ hai là 9 km/h.",
        "Bài 4: a) Tứ giác $OHIK$ có $\\widehat{H} = \\widehat{K} = \\widehat{I} = 90^\\circ$ nên là hình chữ nhật. Lại có hai dây bằng nhau nên khoảng cách từ tâm đến hai dây bằng nhau: $OH = OK \\Rightarrow OHIK$ là hình vuông; b) Bán kính $R = \\sqrt{OH^2 + (AB/2)^2} = \\sqrt{5^2 + 7^2} = \\sqrt{74}\\text{ cm}$; c) $OI$ là đường chéo hình vuông cạnh 5 cm nên $OI = 5\\sqrt{2}\\text{ cm}$.",
        "Bài 5: $T = (\\sqrt{x - 4} - 4)^2 + 2024 \\ge 2024$. GTNN là 2024 khi $x = 20$."
    ]:
        add_answer_item(doc, _ans)
    add_answer_header(doc, 10)
    for _ans in [
        "Bài 1: a) Nghiệm $(2; 3)$; b) $x \\in \\{5/2; -1/3\\}$; c) ĐKXĐ: $x \\neq \\pm 2$. Khử mẫu: $(x + 1)(x + 2) = (x - 1)(x - 2) \\Rightarrow x^2 + 3x + 2 = x^2 - 3x + 2 \\Rightarrow 6x = 0 \\Rightarrow x = 0$ (thoả mãn).",
        "Bài 2: a) $4x - 16 \\ge 0 \\Rightarrow x \\ge 4$; b) $L = |5 - \\sqrt{21}| + \\sqrt{21} = 5$.",
        "Bài 3: Gọi số bạn nam là $x$, bạn nữ là $y$. Hệ phương trình: $\\begin{cases} x + y = 40 \\\\ 3x + 2y = 105 \\end{cases} \\Rightarrow \\begin{cases} x = 25 \\\\ y = 15 \\end{cases}$. Có 25 bạn nam và 15 bạn nữ.",
        "Bài 4: a) $AH = \\sqrt{BH \\cdot CH} = \\sqrt{4 \\cdot 9} = 6\\text{ cm}$. $AB = \\sqrt{AH^2 + BH^2} = \\sqrt{36 + 16} = 2\\sqrt{13}\\text{ cm}, AC = \\sqrt{AH^2 + CH^2} = \\sqrt{36 + 81} = 3\\sqrt{13}\\text{ cm}$; b) $AD \\perp BD$ và $AE \\perp CE$ với $AD = AE = AH$. Theo tính chất tiếp tuyến, $\\widehat{DAH} = 2\\widehat{BAH}, \\widehat{EAH} = 2\\widehat{CAH} \\Rightarrow \\widehat{DAE} = 2(\\widehat{BAH} + \\widehat{CAH}) = 2 \\cdot 90^\\circ = 180^\\circ$. Do đó $D, A, E$ thẳng hàng; c) $BD \\perp DE$ và $CE \\perp DE \\Rightarrow BDEC$ là hình thang vuông. Theo tính chất tiếp tuyến cắt nhau: $BD = BH, CE = CH \\Rightarrow DE = DA + AE = BH + CH = BD + CE$.",
        "Bài 5: Áp dụng BĐT Cauchy: $(a + b)\\left(\\frac{1}{a} + \\frac{1}{b}\\right) \\ge 2\\sqrt{ab} \\cdot 2\\sqrt{\\frac{1}{ab}} = 4 \\Rightarrow 4\\left(\\frac{1}{a} + \\frac{1}{b}\\right) \\ge 4 \\Rightarrow \\frac{1}{a} + \\frac{1}{b} \\ge 1$."
    ]:
        add_answer_item(doc, _ans)

    doc.save(output_path)
    print(f"[TOAN 9 - 2026-2027] Saved successfully to: {output_path}")

if __name__ == "__main__":
    import datetime
    today = datetime.datetime.now().strftime("%d.%m")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "2_TAO_BAI_TAP", "Ket_qua", today)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "De_Cuong_On_Tap_Giua_HK1_Toan_9.docx")
    build_de_cuong_toan_9(out_file)
