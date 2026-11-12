# -*- coding: utf-8 -*-
"""
Script sinh 11 KHBD Chương VII: Phương trình bậc nhất và Hàm số bậc nhất (Tiết 55 - 70) - Toán 8 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan8"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    {
        "filename": "08_KHBD_Toan8_Bai25_PhuongTrinhBacNhatMotAn_Tiet55-56.md",
        "header": "TIẾT 55, 56 - BÀI 25: PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 55, 56 - BÀI 25: PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa phương trình bậc nhất một ẩn: Phương trình có dạng $ax + b = 0$, trong đó $a$ và $b$ là hai số đã cho và $a \\neq 0$.
- Nắm vững hai quy tắc biến đổi tương đương: Quy tắc chuyển vế và quy tắc nhân với một số khác $0$.
- Biết cách giải phương trình bậc nhất một ẩn và các phương trình đưa được về dạng $ax + b = 0$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự áp dụng quy tắc chuyển vế đổi dấu và nhân chia hai vế để tìm giá trị ẩn số.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận phân tích các lỗi sai phổ biến khi chuyển vế mà quên đổi dấu.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận giải thích các bước biến đổi phương trình đưa về dạng $ax = -b$.
- Năng lực giải quyết vấn đề toán học: Tìm nghiệm duy nhất của phương trình bậc nhất $x = -\\frac{b}{a}$.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS lựa chọn phần mềm giải phương trình hoặc máy tính cầm tay để kiểm tra nghiệm bài làm; 1.3.TC2a: HS sắp xếp các phương trình vào bảng tính để giải hàng loạt.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS mô tả cách AI thực hiện chức năng đọc các ký hiệu toán học để chuyển đổi thành phương trình số; 8.D2.1: HS thực hành lập kế hoạch sử dụng app AI để kiểm tra nhanh nghiệm.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi thực hiện đổi dấu hạng tử.
- Trung thực, độc lập suy nghĩ trong quá trình giải toán.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, máy chiếu, bảng phụ ghi quy tắc biến đổi.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt tình huống bài toán cổ "Vừa gà vừa chó" để dẫn vào khái niệm phương trình.
b) Nội dung: Tìm số gà và số chó khi biết tổng số con là $36$ và tổng số chân là $100$.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đọc bài toán dân gian: "Vừa gà vừa chó, Bó lại cho tròn, Ba mươi sáu con, Một trăm chân chẵn". Nếu gọi số gà là $x$ thì phương trình tìm $x$ là gì?<br>- **HS:** Đọc đề và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Số chó là $36 - x$. Tổng số chân: $2x + 4(36 - x) = 100$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Biểu thức có dấu bằng chứa ẩn $x$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Đây là phương trình bậc nhất một ẩn. | Phương trình biểu thị số chân là: $2x + 4(36 - x) = 100$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Định nghĩa phương trình bậc nhất một ẩn (30 phút)
a) Mục tiêu: Nhận biết phương trình bậc nhất một ẩn dạng $ax + b = 0$ ($a \\neq 0$).
b) Nội dung: Định nghĩa, xác định hệ số $a, b$ và nghiệm của phương trình.
c) Sản phẩm: Vở ghi và các ví dụ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Phương trình dạng $ax + b = 0$, với $a$ và $b$ là hai số đã cho và $a \\neq 0$, được gọi là phương trình bậc nhất một ẩn (ẩn $x$). Cho ví dụ và chỉ rõ hệ số $a, b$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lấy ví dụ: $2x - 6 = 0$ ($a = 2, b = -6$); $-3x + 1 = 0$ ($a = -3, b = 1$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chỉ rõ hệ số $a, b$ của từng phương trình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại điều kiện bắt buộc: Hệ số $a$ phải khác $0$. | **1. Định nghĩa phương trình bậc nhất một ẩn:**<br>- Dạng tổng quát: $ax + b = 0$ ($a, b \\in \\mathbb{R}, a \\neq 0$).<br>- Nghiệm: Giá trị $x_0$ thỏa mãn đẳng thức khi thay vào phương trình. |

### Hoạt động 2.2: Hai quy tắc biến đổi và cách giải tổng quát (35 phút)
a) Mục tiêu: Nắm vững quy tắc chuyển vế và quy tắc nhân để giải phương trình $ax + b = 0$.
b) Nội dung: Quy tắc chuyển vế đổi dấu và quy tắc chia hai vế cho $a \\neq 0$.
c) Sản phẩm: Lời giải mẫu các phương trình trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu hai quy tắc biến đổi:<br>  + Quy tắc chuyển vế: Khi chuyển một hạng tử từ vế này sang vế kia của phương trình, ta phải đổi dấu hạng tử đó.<br>  + Quy tắc nhân: Ta có thể nhân (hoặc chia) cả hai vế của phương trình với cùng một số khác $0$.<br>- **HS:** Ghi nhận quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải phương trình: $3x - 12 = 0$. Chuyển $-12$ sang vế phải thành $+12$. Chia hai vế cho $3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: $3x = 12 \\Rightarrow x = 4$. Kết luận: Vậy phương trình có nghiệm duy nhất $x = 4$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Nghiệm duy nhất của phương trình $ax + b = 0$ là $x = -\\frac{b}{a}$. Tuyệt đối không kết luận tập nghiệm. | **2. Cách giải tổng quát phương trình bậc nhất:**<br>$$ax + b = 0$$<br>$$ax = -b$$<br>$$x = -\\frac{b}{a}$$<br>- Kết luận: Vậy phương trình có nghiệm duy nhất $x = -\\frac{b}{a}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Giải các phương trình đưa được về dạng $ax + b = 0$ bằng cách mở ngoặc và thu gọn.
b) Nội dung: Bài 7.1, 7.2 SGK trang 32.
c) Sản phẩm: Bài giải chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao phương trình: $5(x - 2) - 3(x + 1) = 9$.<br>- **HS:** Nhận đề và thực hiện mở ngoặc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $5x - 10 - 3x - 3 = 9 \\Rightarrow 2x - 13 = 9 \\Rightarrow 2x = 9 + 13 = 22 \\Rightarrow x = 11$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kết luận rõ: Vậy nghiệm của phương trình là $x = 11$. | **Lời giải:**<br>$$5(x - 2) - 3(x + 1) = 9$$<br>$$5x - 10 - 3x - 3 = 9$$<br>$$2x - 13 = 9$$<br>$$2x = 22$$<br>$$x = 11$$<br>Vậy nghiệm của phương trình là $x = 11$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Giải quyết bài toán dân gian "Vừa gà vừa chó" đã đặt ra ở phần khởi động.
b) Nội dung: Giải phương trình $2x + 4(36 - x) = 100$ để tìm số gà và số chó.
c) Sản phẩm: Lời giải hoàn thiện trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu giải phương trình $2x + 4(36 - x) = 100$ để tìm số gà.<br>- **HS:** Thực hiện giải phương trình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $2x + 144 - 4x = 100 \\Rightarrow -2x = 100 - 144 = -44 \\Rightarrow x = 22$. Số chó là $36 - 22 = 14$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Có 22 con gà và 14 con chó.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao cách ứng dụng phương trình đại số giải toán đố cổ Việt Nam. | Số gà là $22$ con, số chó là $14$ con. (Thử lại: $22 + 14 = 36$ con; $22 \\cdot 2 + 14 \\cdot 4 = 100$ chân, hoàn toàn chính xác). |
"""
    },
    {
        "filename": "09_KHBD_Toan8_OnTapGiuaHK2_DaiSo_Tiet58.md",
        "header": "TIẾT 58 - ÔN TẬP GIỮA HỌC KÌ II (ĐẠI SỐ)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 58 - ÔN TẬP GIỮA HỌC KÌ II (ĐẠI SỐ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức trọng tâm nửa đầu HKII môn Đại số 8: Phân thức đại số (khái niệm, tính chất, 4 phép tính, rút gọn biểu thức) và Phương trình bậc nhất một ẩn (định nghĩa, hai quy tắc biến đổi, cách giải phương trình).
- Rèn luyện kỹ năng giải các bài toán tổng hợp rút gọn phân thức và giải phương trình chứa dấu ngoặc hoặc mẫu số.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức qua sơ đồ tư duy; chủ động rà soát các dạng bài tập mình còn hay sai sót.
- Giao tiếp và hợp tác: Tích cực trao đổi, thảo luận nhóm chữa bài tập ôn tập giữa kì.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lựa chọn thứ tự biến đổi hợp lí nhất khi rút gọn phân thức và giải phương trình.
- Năng lực giải quyết vấn đề toán học: Giải quyết trọn vẹn các bài toán tìm $x$ và bài toán thực tế.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS lựa chọn máy tính cầm tay để kiểm tra nhanh kết quả toàn bộ đề cương ôn tập giữa kì II môn Đại số.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D2.1: HS sử dụng AI để tạo ngân hàng câu hỏi trắc nghiệm ôn tập giữa học kì II có chấm điểm tự động.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, tỉ mỉ, tác phong làm bài thi nghiêm túc.
- Tự tin, sẵn sàng tâm thế bước vào bài kiểm tra đánh giá giữa HKII.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 58 (vector 300 DPI), tivi/máy chiếu, đề cương ôn tập.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt tinh thần ôn tập qua trò chơi trắc nghiệm chọn đáp án đúng.
b) Nội dung: Trả lời 3 câu hỏi trắc nghiệm về điều kiện xác định và nghiệm của phương trình.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu nhanh 3 câu hỏi trắc nghiệm ôn tập lý thuyết.<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết nhanh đáp án lên bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con đồng loạt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và dẫn dắt vào bài ôn tập. | Bảng đáp án trắc nghiệm chuẩn xác. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn diện kiến thức Phân thức và Phương trình qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 58; đối chiếu các công thức và quy tắc biến đổi.

![Sơ đồ tư duy Ôn tập giữa HK2 Tiết 58](khbd-ill:mindmap-toan8-tiet58)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 58. Yêu cầu HS phân tích các nhánh: 1. Phân thức đại số & Rút gọn; 2. Phương trình bậc nhất một ẩn; 3. Giải bài toán bằng cách lập PT; 4. Kỹ năng trình bày bài giải.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo cặp đôi nhắc lại các quy tắc cốt lõi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Nhấn mạnh tuyệt đối không kết luận tập nghiệm $S = \\{...\\}$, không dùng dấu tương đương tùy tiện. | **Hệ thống lý thuyết giữa kì II:**<br>1. Phân thức: ĐKXĐ $B \\neq 0$, rút gọn, 4 phép tính.<br>2. Phương trình bậc nhất: $ax + b = 0$ ($a \\neq 0$), nghiệm $x = -\\frac{b}{a}$.<br>3. Quy tắc: Chuyển vế đổi dấu; Nhân chia hai vế cùng số khác $0$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải 2 bài toán điển hình trong đề cương: Rút gọn phân thức tổng hợp và Giải phương trình có mẫu số.
b) Nội dung: Bài tập tự luận ôn tập giữa kì.
c) Sản phẩm: Bài làm chi tiết trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài tập:<br>  Bài 1: Rút gọn biểu thức $A = \\left(\\frac{1}{x - 1} + \\frac{x}{x^2 - 1}\\right) \\cdot \\frac{x + 1}{2x + 1}$.<br>  Bài 2: Giải phương trình: $\\frac{x - 3}{2} + \\frac{2x + 1}{3} = 4$.<br>- **HS:** Nhận đề và giải bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br>- Bài 1: ĐKXĐ: $x \\neq \\pm 1, x \\neq -\\frac{1}{2}$. Biểu thức trong ngoặc: $\\frac{x + 1 + x}{(x - 1)(x + 1)} = \\frac{2x + 1}{(x - 1)(x + 1)}$. Nhân với $\\frac{x + 1}{2x + 1}$ rút gọn được $A = \\frac{1}{x - 1}$.<br>- Bài 2: Mẫu chung là $6$. Nhân hai vế với $6$: $3(x - 3) + 2(2x + 1) = 24 \\Rightarrow 3x - 9 + 4x + 2 = 24 \\Rightarrow 7x - 7 = 24 \\Rightarrow 7x = 31 \\Rightarrow x = \\frac{31}{7}$. Kết luận nghiệm rõ ràng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt chuẩn mực trình bày bài thi tự luận. | **Lời giải chi tiết:**<br>**Bài 1:**<br>$$A = \\frac{2x + 1}{(x - 1)(x + 1)} \\cdot \\frac{x + 1}{2x + 1} = \\frac{1}{x - 1}$$<br>**Bài 2:**<br>$$\\frac{x - 3}{2} + \\frac{2x + 1}{3} = 4$$<br>$$3(x - 3) + 2(2x + 1) = 24$$<br>$$3x - 9 + 4x + 2 = 24$$<br>$$7x - 7 = 24$$<br>$$7x = 31 \\Rightarrow x = \\frac{31}{7}$$<br>Vậy nghiệm của phương trình là $x = \\frac{31}{7}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Quán triệt quy chế phòng thi và chuẩn bị cho Tiết 59: Kiểm tra giữa học kì II.
b) Nội dung: Giáo viên dặn dò thời gian làm bài, dụng cụ mang vào phòng thi.
c) Sản phẩm: Kế hoạch làm bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò: Chuẩn bị máy tính cầm tay, bút mực, giấy thi; làm bài bình tĩnh, cẩn thận từng bước biến đổi.<br>- **HS:** Ghi nhớ lưu ý.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự rà soát lại kiến thức bản thân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đặt câu hỏi thắc mắc nếu có.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em đạt kết quả xuất sắc trong bài kiểm tra giữa kì. | Tâm thế tự tin, chuẩn bị đầy đủ dụng cụ cho bài kiểm tra giữa học kì II. |
"""
    },
    {
        "filename": "10_KHBD_Toan8_KiemTraGiuaHK2_DaiSo_Tiet59.md",
        "header": "TIẾT 59 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (ĐẠI SỐ)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 59 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (ĐẠI SỐ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ nắm vững chuẩn kiến thức, kỹ năng của học sinh về Chương VI (Phân thức đại số) và nửa đầu Chương VII (Phương trình bậc nhất một ẩn).
- Đánh giá kỹ năng biến đổi phân thức, tìm điều kiện xác định, giải phương trình và trình bày bài giải logic, có căn cứ khoa học.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác, nghiêm túc làm bài thi độc lập, tuân thủ đúng quy chế phòng kiểm tra.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày bài giải mạch lạc, lập luận chặt chẽ, chính xác.
- Năng lực giải quyết vấn đề toán học: Xử lý các bài toán đại số từ cơ bản đến vận dụng.

c) Năng lực số (NLS):
- ***5.2.TC2b: Sử dụng máy tính cầm tay đúng quy chế phòng thi để kiểm tra các phép biến đổi số học và tìm nghiệm.***

## 3. Về phẩm chất
- Trung thực, khách quan, tự trọng trong kiểm tra.
- Tác phong khoa học, cẩn trọng trong từng phép tính.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận và bản đặc tả chuẩn Bộ GD&ĐT (Trắc nghiệm 30% - Tự luận 70%), đáp án và biểu điểm.
2. Học sinh: Giấy thi, bút mực, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (3 phút)
a) Mục tiêu: Ổn định tổ chức, phát đề thi và nhắc nhở thời gian làm bài.
b) Nội dung: Phát đề kiểm tra.
c) Sản phẩm: Đề thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định trật tự phòng thi, phổ biến quy chế. Phát đề thi cho học sinh.<br>- **HS:** Nhận đề, kiểm tra số trang và độ rõ của đề.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Điền đầy đủ thông tin cá nhân vào giấy thi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo ngay nếu có đề bị lỗi mờ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Phát lệnh bắt đầu tính giờ làm bài. | 100% học sinh sẵn sàng bước vào bài làm. |

## B. THỰC HIỆN BÀI KIỂM TRA (HOẠT ĐỘNG 2) (40 phút)
a) Mục tiêu: Học sinh độc lập làm bài thi trắc nghiệm và tự luận.
b) Nội dung: Học sinh giải các câu hỏi trong đề kiểm tra.
c) Sản phẩm: Bài làm hoàn thiện trên giấy thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giám sát phòng thi nghiêm túc, bao quát đảm bảo tính công bằng, khách quan.<br>- **HS:** Độc lập làm bài, không trao đổi, không quay cóp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm phần Trắc nghiệm trước, sau đó làm phần Tự luận trình bày chi tiết.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Báo mốc thời gian còn lại 15 phút và 5 phút.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **HS:** Soát lại toàn bộ bài làm, đặc biệt là các bước biến đổi dấu âm và kết luận nghiệm. | Học sinh làm bài độc lập, nghiêm túc, đạt chất lượng cao. |

## C. THU BÀI VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (2 phút)
a) Mục tiêu: Thu bài đầy đủ theo danh sách lớp và nhận xét ý thức kiểm tra.
b) Nội dung: Thu bài thi theo dãy bàn.
c) Sản phẩm: Toàn bộ bài thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hết giờ làm bài, yêu cầu học sinh dừng bút, nộp bài theo dãy.<br>- **HS:** Dừng bút và chuyển bài lên đầu bàn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm đủ số bài thi theo sĩ số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp xác nhận sĩ số tham gia kiểm tra.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét thái độ làm bài của học sinh; dặn dò chuẩn bị cho Tiết 60 Luyện tập chung. | Thu đủ 100% bài kiểm tra theo sĩ số lớp. |
"""
    },
    {
        "filename": "11_KHBD_Toan8_LuyenTapChung_Tiet60.md",
        "header": "TIẾT 60 - LUYỆN TẬP CHUNG: PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN (TRANG 37)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 60 - LUYỆN TẬP CHUNG: PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN (TRANG 37)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Rèn luyện kỹ năng giải các phương trình đưa được về dạng $ax + b = 0$ bằng các phép biến đổi: Bỏ dấu ngoặc, quy đồng và khử mẫu số.
- Vận dụng thành thạo giải phương trình tích đơn giản: $A(x) \\cdot B(x) = 0 \\iff A(x) = 0$ hoặc $B(x) = 0$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát cấu trúc phương trình để lựa chọn phương pháp quy đồng hay đặt nhân tử chung đưa về phương trình tích.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận giải phương trình có chứa tham số đơn giản.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận chặt chẽ trong từng bước biến đổi tương đương; chỉ ra điều kiện để phương trình có nghiệm.
- Năng lực giải quyết vấn đề toán học: Tìm giá trị của ẩn số thỏa mãn đẳng thức toán học.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS lựa chọn phần mềm giải phương trình hoặc MTBT để kiểm tra nhanh các bước biến đổi phương trình.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D2.1: HS tìm hiểu cách AI nhận diện các phương trình viết tay trên màn hình cảm ứng để tự động giải và vẽ đồ thị.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, cẩn thận, không làm tắt dẫn đến sai dấu.
- Ý thức học tập tự giác, chủ động khám phá nhiều cách giải khác nhau.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 60 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại các quy tắc giải phương trình có mẫu số qua câu hỏi kiểm tra nhanh.
b) Nội dung: Khi giải phương trình có mẫu là các số thì bước đầu tiên ta nên làm gì?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Muốn giải phương trình có mẫu số là các hằng số, bước đầu tiên ta làm gì?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tìm mẫu chung và quy đồng khử mẫu hai vế.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài luyện tập chung. | Quy đồng mẫu số hai vế rồi khử mẫu để đưa về phương trình không chứa mẫu số. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức phương trình bậc nhất một ẩn qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 60; đối chiếu các dạng phương trình quy về bậc nhất.

![Sơ đồ tư duy Luyện tập chung Tiết 60](khbd-ill:mindmap-toan8-tiet60)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 60. Yêu cầu HS phân tích các nhánh: 1. Định nghĩa $ax + b = 0$; 2. Hai quy tắc biến đổi; 3. Cách giải tổng quát $x = -b/a$; 4. Các phương trình quy về bậc nhất (chứa ngoặc, chứa mẫu).<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo cặp đôi nhắc lại các quy tắc cốt lõi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa sơ đồ kiến thức. | **Hệ thống kiến thức phương trình bậc nhất:**<br>1. Định nghĩa: $ax + b = 0$ ($a \\neq 0$).<br>2. Hai quy tắc: Chuyển vế đổi dấu; Nhân chia hai vế cùng số khác $0$.<br>3. Nghiệm duy nhất: $x = -\\frac{b}{a}$.<br>4. Phương trình quy về: Mở ngoặc, quy đồng khử mẫu số. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải phương trình chứa mẫu số và phương trình tích.
b) Nội dung: Bài 7.4, 7.5 SGK trang 37.
c) Sản phẩm: Lời giải chi tiết trên bảng và trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 phương trình:<br>  Phương trình 1: $\\frac{x + 2}{4} - \\frac{2x - 1}{3} = \\frac{x - 3}{6}$.<br>  Phương trình 2: $(2x - 3)(x + 5) = 0$.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** PT 1: Mẫu chung $12$. Nhân hai vế với $12$: $3(x + 2) - 4(2x - 1) = 2(x - 3) \\Rightarrow 3x + 6 - 8x + 4 = 2x - 6 \\Rightarrow -5x + 10 = 2x - 6 \\Rightarrow -7x = -16 \\Rightarrow x = \\frac{16}{7}$. PT 2: $2x - 3 = 0$ hoặc $x + 5 = 0 \\Rightarrow x = \\frac{3}{2}$ hoặc $x = -5$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chốt chuẩn: Kết luận rõ các nghiệm, không dùng kí hiệu tập nghiệm. | **Lời giải chi tiết:**<br>**Phương trình 1:**<br>$$3(x + 2) - 4(2x - 1) = 2(x - 3)$$<br>$$3x + 6 - 8x + 4 = 2x - 6$$<br>$$-5x + 10 = 2x - 6$$<br>$$-7x = -16 \\Rightarrow x = \\frac{16}{7}$$<br>Vậy nghiệm của phương trình là $x = \\frac{16}{7}$.<br>**Phương trình 2:**<br>$$(2x - 3)(x + 5) = 0$$<br>Suy ra $2x - 3 = 0$ hoặc $x + 5 = 0$.<br>Do đó $x = \\frac{3}{2}$ hoặc $x = -5$.<br>Vậy phương trình có hai nghiệm là $x = \\frac{3}{2}$ và $x = -5$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Giải phương trình có chứa tham số $m$.
b) Nội dung: Tìm $m$ để phương trình $(m - 1)x + 2 = 0$ có nghiệm $x = 2$.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thay nghiệm $x = 2$ vào phương trình để tìm giá trị của tham số $m$.<br>- **HS:** Thực hiện thay số.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $(m - 1) \\cdot 2 + 2 = 0 \\Rightarrow 2m - 2 + 2 = 0 \\Rightarrow 2m = 0 \\Rightarrow m = 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng: $m = 0$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học. Dặn dò chuẩn bị cho Bài 26: Giải bài toán bằng cách lập phương trình. | Thay $x = 2$ vào phương trình ta được:<br>$$(m - 1) \\cdot 2 + 2 = 0 \\Rightarrow 2m = 0 \\Rightarrow m = 0$$<br>Vậy giá trị của $m$ cần tìm là $0$. |
"""
    },
    {
        "filename": "12_KHBD_Toan8_Bai26_GiaiBaiToanBangCachLapPT_Tiet57.md",
        "header": "TIẾT 57 - BÀI 26: GIẢI BÀI TOÁN BẰNG CÁCH LẬP PHƯƠNG TRÌNH\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 57 - BÀI 26: GIẢI BÀI TOÁN BẰNG CÁCH LẬP PHƯƠNG TRÌNH
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững quy trình 3 bước giải bài toán bằng cách lập phương trình:
  + Bước 1: Lập phương trình (Chọn ẩn số và đặt điều kiện thích hợp cho ẩn; Biểu diễn các đại lượng chưa biết theo ẩn và các đại lượng đã biết; Lập phương trình biểu thị mối quan hệ giữa các đại lượng).
  + Bước 2: Giải phương trình vừa lập.
  + Bước 3: Trả lời (Kiểm tra xem trong các nghiệm của phương trình, nghiệm nào thỏa mãn điều kiện của ẩn, nghiệm nào không, rồi kết luận).
- Vận dụng giải các bài toán về quan hệ số, bài toán hình học và bài toán thực tế đơn giản.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Đọc hiểu và phân tích đề bài, xác định rõ đại lượng đã biết và đại lượng cần tìm.
- Giao tiếp và hợp tác: Làm việc nhóm phân tích mối liên hệ giữa các đại lượng và thống nhất phương trình lập được.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Chuyển ngôn ngữ đời sống thực tế thành phương trình toán học bậc nhất một ẩn.
- Năng lực giải quyết vấn đề toán học: Giải phương trình và đối chiếu điều kiện để đưa ra câu trả lời thực tế.

c) Năng lực số (NLS):
- ***1.1.TC2a: HS tìm kiếm dữ liệu thực tế về khoảng cách các tuyến đường bộ để thiết kế bài toán chuyển động.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D1.1: HS tìm hiểu cách trợ lý AI phân tích ngôn ngữ tự nhiên (NLP) của đề bài để tự động thiết lập phương trình toán học.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác, không quên đặt điều kiện và đơn vị cho ẩn số.
- Tinh thần trách nhiệm, gắn kết bài học toán với giải quyết các vấn đề thực tiễn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, bảng phụ tóm tắt 3 bước giải bài toán bằng cách lập phương trình.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt bài toán tìm số học sinh của một lớp để dẫn vào quy trình giải bài toán bằng cách lập phương trình.
b) Nội dung: Một lớp có số bạn nam gấp đôi số bạn nữ. Nếu chuyển 3 bạn nam đi thì số nam chỉ còn hơn số nữ 5 bạn. Tìm số bạn nữ ban đầu.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán về số học sinh nam và nữ của lớp. Làm thế nào để giải bài toán này một cách khoa học nhất?<br>- **HS:** Đọc đề và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Gọi số bạn nữ là $x$, số bạn nam là $2x$. Phương trình: $2x - 3 = x + 5$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giải ra $x = 8$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Đây chính là phương pháp giải bài toán bằng cách lập phương trình. | Gọi ẩn và biểu diễn các đại lượng giúp giải quyết bài toán lời văn một cách hệ thống và chính xác. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Quy trình 3 bước giải bài toán bằng cách lập phương trình (20 phút)
a) Mục tiêu: Nắm vững chi tiết 3 bước giải bài toán bằng cách lập phương trình.
b) Nội dung: Các bước lập phương trình, giải phương trình và đối chiếu kết luận.
c) Sản phẩm: Vở ghi quy trình 3 bước và bài giải ví dụ mẫu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình bày chi tiết 3 bước:<br>  + Bước 1: Lập phương trình (chọn ẩn, đặt ĐK, biểu diễn đại lượng, lập PT).<br>  + Bước 2: Giải phương trình.<br>  + Bước 3: Kiểm tra ĐK và kết luận.<br>- **HS:** Ghi chép 3 bước vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng giải bài toán: Một mảnh vườn hình chữ nhật có chu vi $64\\text{ m}$. Chiều dài hơn chiều rộng $8\\text{ m}$. Tính diện tích mảnh vườn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết theo 3 bước.<br>- Nửa chu vi: $64 : 2 = 32\\text{ m}$. Gọi chiều rộng là $x$ ($0 < x < 32$, mét). Chiều dài là $x + 8$. Ta có: $x + (x + 8) = 32 \\Rightarrow 2x = 24 \\Rightarrow x = 12$ (thỏa mãn ĐK). Chiều dài: $12 + 8 = 20\\text{ m}$. Diện tích: $20 \\cdot 12 = 240\\text{ m}^2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy trình chuẩn mực và nhấn mạnh bước đối chiếu điều kiện. | **Quy trình 3 bước:**<br>- **Bước 1: Lập phương trình:**<br>  + Chọn ẩn số và đặt điều kiện thích hợp cho ẩn.<br>  + Biểu diễn các đại lượng chưa biết theo ẩn và các đại lượng đã biết.<br>  + Lập phương trình biểu thị mối quan hệ giữa các đại lượng.<br>- **Bước 2: Giải phương trình.**<br>- **Bước 3: Trả lời:** Kiểm tra điều kiện và kết luận. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Giải bài toán chuyển động đều trên quãng đường thẳng.
b) Nội dung: Bài 7.8 SGK trang 40: Một ô tô đi từ A đến B với vận tốc $50\\text{ km/h}$ rồi quay về A với vận tốc $40\\text{ km/h}$. Tổng thời gian cả đi và về là $4$ giờ $30$ phút. Tính quãng đường AB.
c) Sản phẩm: Bài giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đổi $4$ giờ $30$ phút $= 4{,}5$ giờ $= \\frac{9}{2}$ giờ. Gọi độ dài quãng đường AB là $x\\text{ (km, } x > 0)$. Thời gian đi là gì? Thời gian về là gì?<br>- **HS:** Đọc đề và lập phương trình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thời gian đi: $\\frac{x}{50}$. Thời gian về: $\\frac{x}{40}$. Phương trình: $\\frac{x}{50} + \\frac{x}{40} = \\frac{9}{2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: Mẫu chung là $200$. Nhân với $200$: $4x + 5x = 900 \\Rightarrow 9x = 900 \\Rightarrow x = 100$ (thỏa mãn ĐK).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi bài giải chuẩn mực và lưu ý bước đổi đơn vị thời gian. | **Bài giải:**<br>- Đổi $4$ giờ $30$ phút $= \\frac{9}{2}$ giờ.<br>- Gọi quãng đường AB là $x\\text{ (km, } x > 0)$.<br>- Thời gian đi từ A đến B là $\\frac{x}{50}$ (giờ).<br>- Thời gian về từ B về A là $\\frac{x}{40}$ (giờ).<br>- Theo đề bài ta có phương trình:<br>$$\\frac{x}{50} + \\frac{x}{40} = \\frac{9}{2}$$<br>$$4x + 5x = 900 \\Rightarrow 9x = 900 \\Rightarrow x = 100\\text{ (thỏa mãn ĐK)}$$<br>Vậy quãng đường AB dài $100\\text{ km}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng lập phương trình giải bài toán năng suất lao động.
b) Nội dung: Một xưởng may theo kế hoạch mỗi ngày phải may 30 bộ quần áo. Nhờ cải tiến kỹ thuật xưởng may được 40 bộ mỗi ngày nên hoàn thành trước 2 ngày. Tính số bộ quần áo xưởng phải may theo kế hoạch.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn chọn ẩn: Gọi số bộ quần áo kế hoạch là $x\\text{ (bộ, } x \\in \\mathbb{N}^*)$.<br>- **HS:** Lập phương trình thời gian: $\\frac{x}{30} - \\frac{x}{40} = 2$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải phương trình: Mẫu chung $120$. $4x - 3x = 240 \\Rightarrow x = 240$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời: Kế hoạch may 240 bộ quần áo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học thực tiễn. Dặn dò chuẩn bị cho Bài 27: Khái niệm hàm số và đồ thị. | Xưởng phải may $240$ bộ quần áo theo kế hoạch. |
"""
    },
    {
        "filename": "13_KHBD_Toan8_Bai27_KhaiNiemHamSoVaDoThi_Tiet61-63.md",
        "header": "TIẾT 61, 62, 63 - BÀI 27: KHÁI NIỆM HÀM SỐ VÀ ĐỒ THỊ CỦA HÀM SỐ\n*Thời lượng thực hiện: 03 tiết (135 phút)*",
        "md": """TIẾT 61, 62, 63 - BÀI 27: KHÁI NIỆM HÀM SỐ VÀ ĐỒ THỊ CỦA HÀM SỐ
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhắc lại và nâng cao khái niệm hàm số: Nếu đại lượng $y$ phụ thuộc vào đại lượng thay đổi $x$ sao cho với mỗi giá trị của $x$, ta luôn xác định được chỉ một giá trị tương ứng của $y$ thì $y$ được gọi là hàm số của $x$, và $x$ gọi là biến số. Kí hiệu $y = f(x)$.
- Biết các cách cho một hàm số: Bằng bảng, bằng công thức.
- Nắm vững khái niệm mặt phẳng tọa độ $Oxy$ và đồ thị của hàm số: Tập hợp tất cả các điểm biểu diễn các cặp giá trị tương ứng $(x; y)$ trên mặt phẳng tọa độ.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự lập bảng giá trị của hàm số cho bởi công thức và biểu diễn các điểm lên mặt phẳng tọa độ.
- Giao tiếp và hợp tác: Làm việc nhóm vẽ hệ trục tọa độ $Oxy$ và xác định tọa độ các điểm chuẩn xác.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Kiểm tra một điểm có thuộc đồ thị hàm số hay không bằng cách thay tọa độ điểm vào công thức hàm số.
- Năng lực sử dụng công cụ học toán: Sử dụng thước thẳng, êke vẽ hệ trục tọa độ $Oxy$ vuông góc chuẩn xác.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng phần mềm GeoGebra để vẽ điểm và quan sát quỹ tích các điểm tạo thành đồ thị hàm số.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu cách AI sử dụng khái niệm hàm số đa biến để dự báo giá nhà đất dựa trên diện tích và vị trí.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi xác định hoành độ và tung độ của điểm.
- Say mê, hào hứng khám phá sự gắn kết giữa đại số và hình học qua đồ thị.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, thước thẳng, máy chiếu, bảng phụ vẽ hệ trục $Oxy$.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, thước thẳng có chia vạch, giấy kẻ ô li.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề từ thực tế bảng giá cước taxi phụ thuộc vào quãng đường di chuyển.
b) Nội dung: Quan sát bảng giá cước taxi: Đi $1\\text{ km}$ giá $12\\,000$ đồng, đi $2\\text{ km}$ giá $24\\,000$ đồng,... Số tiền trả có phụ thuộc vào quãng đường không?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khi đi taxi, số tiền phải trả $y$ phụ thuộc vào quãng đường đi $x$. Với mỗi quãng đường $x$, ta có xác định được duy nhất một số tiền $y$ không?<br>- **HS:** Quan sát và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mỗi quãng đường chỉ có duy nhất một số tiền tương ứng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Đại lượng $y$ phụ thuộc vào $x$ như vậy gọi là hàm số. | Số tiền $y$ là hàm số của quãng đường $x$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (95 phút)
### Hoạt động 2.1: Khái niệm hàm số và các cách cho hàm số (45 phút)
a) Mục tiêu: Nắm vững định nghĩa hàm số và cách cho hàm số bằng bảng hoặc công thức.
b) Nội dung: Định nghĩa, biến số, hàm số, giá trị của hàm số $f(x_0)$.
c) Sản phẩm: Vở ghi bài và lời giải các ví dụ tính giá trị hàm số.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa hàm số: Nếu đại lượng $y$ phụ thuộc vào đại lượng thay đổi $x$ sao cho với mỗi giá trị của $x$ ta luôn xác định được chỉ một giá trị tương ứng của $y$ thì $y$ gọi là hàm số của $x$, $x$ gọi là biến số. Kí hiệu $y = f(x)$. Cho hàm số $y = f(x) = 2x - 3$. Tính $f(1), f(-2)$.<br>- **HS:** Tiếp nhận công thức và tính toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $f(1) = 2(1) - 3 = -1$. $f(-2) = 2(-2) - 3 = -7$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Hàm số có thể cho bằng bảng hoặc cho bằng công thức toán học. | **1. Khái niệm hàm số:**<br>- $y$ là hàm số của biến số $x$ nếu với mỗi giá trị của $x$, có duy nhất một giá trị tương ứng của $y$.<br>- Kí hiệu: $y = f(x)$.<br>- Các cách cho hàm số: Bằng bảng hoặc bằng công thức. |

### Hoạt động 2.2: Mặt phẳng tọa độ và Đồ thị của hàm số (50 phút)
a) Mục tiêu: Nắm vững hệ trục tọa độ $Oxy$, cách xác định tọa độ một điểm và định nghĩa đồ thị hàm số.
b) Nội dung: Hệ trục tọa độ $Oxy$ gồm 2 trục vuông góc tại gốc $O$, biểu diễn điểm $M(x_0; y_0)$ và tập hợp các điểm đồ thị.
c) Sản phẩm: Hình vẽ hệ trục $Oxy$ và các điểm biểu diễn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vẽ hệ trục tọa độ $Oxy$ trên bảng: Trục hoành $Ox$ nằm ngang, trục tung $Oy$ thẳng đứng vuông góc tại $O$. Điểm $M(x_0; y_0)$: $x_0$ là hoành độ, $y_0$ là tung độ. Định nghĩa: Đồ thị hàm số $y = f(x)$ là tập hợp tất cả các điểm $(x; f(x))$ trên mặt phẳng tọa độ.<br>- **HS:** Quan sát và vẽ vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Biểu diễn các điểm $A(1; 2), B(-2; 3), C(0; -1)$ lên mặt phẳng tọa độ $Oxy$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng biểu diễn 3 điểm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Kiểm tra quy tắc đọc tọa độ: Hoành độ đọc trước, tung độ đọc sau: $(x; y)$. | **2. Mặt phẳng tọa độ và Đồ thị hàm số:**<br>- Hệ trục $Oxy$: Trục hoành $Ox$, trục tung $Oy$, gốc tọa độ $O(0; 0)$.<br>- Tọa độ điểm $M(x; y)$: $x$ là hoành độ, $y$ là tung độ.<br>- Đồ thị của hàm số $y = f(x)$ là tập hợp tất cả các điểm biểu diễn các cặp giá trị tương ứng $(x; y)$ trên mặt phẳng tọa độ $Oxy$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (25 phút)
a) Mục tiêu: Kiểm tra xem các điểm cho trước có thuộc đồ thị hàm số $y = 3x - 1$ hay không.
b) Nội dung: Bài 7.12, 7.13 SGK trang 45.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho hàm số $y = f(x) = 3x - 1$. Các điểm sau có thuộc đồ thị hàm số không:<br>  a) $A(1; 2)$;<br>  b) $B(-1; -4)$;<br>  c) $C(2; 4)$?<br>- **HS:** Nhận đề và thay tọa độ vào công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thay $x = 1 \\Rightarrow y = 3(1) - 1 = 2$ (đúng tung độ điểm A) $\\Rightarrow A$ thuộc đồ thị. Thay $x = -1 \\Rightarrow y = 3(-1) - 1 = -4$ $\\Rightarrow B$ thuộc đồ thị. Thay $x = 2 \\Rightarrow y = 3(2) - 1 = 5 \\neq 4$ $\\Rightarrow C$ không thuộc đồ thị.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa phương pháp kiểm tra điểm thuộc đồ thị hàm số. | **Lời giải:**<br>- Điểm $A(1; 2)$: Thay $x = 1$ ta được $y = 3 \\cdot 1 - 1 = 2$. Vậy điểm $A$ thuộc đồ thị hàm số.<br>- Điểm $B(-1; -4)$: Thay $x = -1$ ta được $y = 3 \\cdot (-1) - 1 = -4$. Vậy điểm $B$ thuộc đồ thị hàm số.<br>- Điểm $C(2; 4)$: Thay $x = 2$ ta được $y = 3 \\cdot 2 - 1 = 5 \\neq 4$. Vậy điểm $C$ không thuộc đồ thị hàm số. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Vận dụng hàm số vào mô hình hóa mối quan hệ giữa nhiệt độ theo thang Celsius ($^\\circ\\text{C}$) và thang Fahrenheit ($^\\circ\\text{F}$).
b) Nội dung: Công thức chuyển đổi: $F = 1{,}8C + 32$. Tính nhiệt độ $F$ khi $C = 25^\\circ\\text{C}$ và khi nước đóng băng $C = 0^\\circ\\text{C}$.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu công thức hàm số chuyển đổi nhiệt độ $F = 1{,}8C + 32$. Yêu cầu tính $F$ tại $C = 0$ và $C = 25$.<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tại $C = 0 \\Rightarrow F = 32^\\circ\\text{F}$. Tại $C = 25 \\Rightarrow F = 1{,}8(25) + 32 = 45 + 32 = 77^\\circ\\text{F}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học thực tế. Dặn dò chuẩn bị cho Bài 28: Hàm số bậc nhất và đồ thị. | Khi $C = 0^\\circ\\text{C}$ thì $F = 32^\\circ\\text{F}$.<br>Khi $C = 25^\\circ\\text{C}$ thì $F = 77^\\circ\\text{F}$. |
"""
    },
    {
        "filename": "14_KHBD_Toan8_Bai28_HamSoBacNhatVaDoThi_Tiet64-65.md",
        "header": "TIẾT 64, 65 - BÀI 28: HÀM SỐ BẬC NHẤT VÀ ĐỒ THỊ CỦA HÀM SỐ BẬC NHẤT\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 64, 65 - BÀI 28: HÀM SỐ BẬC NHẤT VÀ ĐỒ THỊ CỦA HÀM SỐ BẬC NHẤT
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa hàm số bậc nhất: Hàm số được cho bởi công thức $y = ax + b$, trong đó $a, b$ là các số cho trước và $a \\neq 0$.
- Nắm vững tính chất đồng biến (khi $a > 0$) và nghịch biến (khi $a < 0$) của hàm số bậc nhất trên $\\mathbb{R}$.
- Hiểu và vẽ thành thạo đồ thị của hàm số bậc nhất $y = ax + b$ ($a \\neq 0$): Là một đường thẳng luôn cắt trục tung tại điểm $(0; b)$ và cắt trục hoành tại điểm $\\left(-\\frac{b}{a}; 0\\right)$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự lập bảng giá trị xác định 2 điểm đặc biệt thuộc đồ thị và dùng thước thẳng nối lại thành đường thẳng.
- Giao tiếp và hợp tác: Hợp tác nhóm nhận xét xu hướng đi lên hay đi xuống của đồ thị tương ứng với dấu của hệ số $a$.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận chứng minh tính đồng biến, nghịch biến thông qua việc so sánh giá trị $f(x_1)$ và $f(x_2)$.
- Năng lực sử dụng công cụ học toán: Vẽ đồ thị đường thẳng chuẩn xác, đẹp mắt trên hệ trục tọa độ $Oxy$.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng phần mềm GeoGebra để vẽ đồ thị hàm số bậc nhất và thay đổi thanh trượt hệ số a, b để quan sát chuyển động của đường thẳng.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu thuật toán hồi quy tuyến tính (Linear Regression) trong AI chính là việc tìm đường thẳng bậc nhất y = ax + b khớp nhất với tập dữ liệu thực nghiệm.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, đo vẽ chính xác từng điểm tọa độ trên mặt phẳng.
- Tinh thần say mê học hỏi, yêu thích vẻ đẹp hình học của các hàm số đại số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, thước thẳng, máy chiếu, GeoGebra mô phỏng chuyển động đường thẳng.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, thước thẳng có chia vạch, giấy kẻ ô li.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tạo tình huống bài toán nạp thẻ điện thoại để xuất hiện hàm số bậc nhất $y = ax + b$.
b) Nội dung: Một sim điện thoại có sẵn $20\\,000$ đồng, mỗi phút gọi tốn $1\\,500$ đồng. Biểu diễn số tiền còn lại $y$ theo số phút gọi $x$.
c) Sản phẩm: Công thức $y = 20\\,000 - 1\\,500x$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Viết công thức biểu thị số tiền còn lại $y$ trong tài khoản sau $x$ phút gọi, biết ban đầu có $20\\,000$ đồng và mỗi phút tốn $1\\,500$ đồng.<br>- **HS:** Đọc đề và viết công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $y = 20\\,000 - 1\\,500x$, hay $y = -1\\,500x + 20\\,000$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Biểu thức có dạng $ax + b$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu bài mới: Hàm số bậc nhất và đồ thị. | Công thức $y = -1500x + 20000$ là một hàm số bậc nhất với $a = -1500, b = 20000$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Định nghĩa và tính chất của hàm số bậc nhất (30 phút)
a) Mục tiêu: Nắm vững định nghĩa $y = ax + b$ ($a \\neq 0$) và tính đồng biến, nghịch biến.
b) Nội dung: Định nghĩa, hệ số $a, b$, tính đồng biến khi $a > 0$, nghịch biến khi $a < 0$.
c) Sản phẩm: Vở ghi bài và nhận xét của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Hàm số bậc nhất là hàm số được cho bởi công thức $y = ax + b$, trong đó $a, b$ là các số cho trước và $a \\neq 0$. Giới thiệu tính chất:<br>  + Đồng biến trên $\\mathbb{R}$ khi $a > 0$ (khi $x$ tăng thì $y$ tăng).<br>  + Nghịch biến trên $\\mathbb{R}$ khi $a < 0$ (khi $x$ tăng thì $y$ giảm).<br>- **HS:** Ghi nhận định nghĩa và tính chất.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xét tính đồng biến, nghịch biến của các hàm số: $y = 3x + 1$ và $y = -2x + 5$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $y = 3x + 1$ đồng biến vì $a = 3 > 0$; $y = -2x + 5$ nghịch biến vì $a = -2 < 0$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Dấu của hệ số $a$ quyết định chiều biến thiên của hàm số. | **1. Định nghĩa và tính chất:**<br>- Dạng: $y = ax + b$ ($a \\neq 0$).<br>- Tính chất biến thiên:<br>  + $a > 0$: Hàm số đồng biến trên $\\mathbb{R}$.<br>  + $a < 0$: Hàm số nghịch biến trên $\\mathbb{R}$. |

### Hoạt động 2.2: Đồ thị của hàm số bậc nhất (35 phút)
a) Mục tiêu: Nắm vững hình dạng đồ thị là một đường thẳng và quy trình 2 bước vẽ đồ thị qua 2 điểm đặc biệt.
b) Nội dung: Cách xác định giao điểm với trục tung $(0; b)$ và giao điểm với trục hoành $\\left(-\\frac{b}{a}; 0\\right)$.
c) Sản phẩm: Đồ thị hàm số vẽ chuẩn xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lý: Đồ thị của hàm số $y = ax + b$ ($a \\neq 0$) là một đường thẳng luôn cắt trục tung tại điểm $P(0; b)$ và cắt trục hoành tại điểm $Q\\left(-\\frac{b}{a}; 0\\right)$. Hướng dẫn cách vẽ qua 2 bước:<br>  + Bước 1: Cho $x = 0 \\Rightarrow y = b$, ta được điểm $P(0; b)$. Cho $y = 0 \\Rightarrow x = -\\frac{b}{a}$, ta được điểm $Q\\left(-\\frac{b}{a}; 0\\right)$.<br>  + Bước 2: Dùng thước thẳng vẽ đường thẳng đi qua hai điểm $P$ và $Q$.<br>- **HS:** Ghi nhớ 2 bước.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành vẽ đồ thị hàm số $y = 2x - 4$ vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: Cho $x = 0 \\Rightarrow y = -4$, điểm $P(0; -4)$. Cho $y = 0 \\Rightarrow x = 2$, điểm $Q(2; 0)$. Nối $P$ và $Q$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá đường thẳng vẽ chính xác, cắt đúng hai trục tọa độ. | **2. Đồ thị của hàm số $y = ax + b$ ($a \\neq 0$):**<br>- Đồ thị là một đường thẳng.<br>- Các bước vẽ:<br>  1. Xác định giao điểm với trục tung: $P(0; b)$.<br>  2. Xác định giao điểm với trục hoành: $Q\\left(-\\frac{b}{a}; 0\\right)$.<br>  3. Vẽ đường thẳng đi qua hai điểm $P$ và $Q$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vẽ đồ thị hàm số có hệ số âm và nhận xét chiều đi xuống của đồ thị.
b) Nội dung: Bài 7.17 SGK trang 49: Vẽ đồ thị hàm số $y = -x + 3$.
c) Sản phẩm: Hình vẽ đồ thị trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu vẽ đồ thị hàm số $y = -x + 3$ trên mặt phẳng tọa độ $Oxy$.<br>- **HS:** Xác định 2 điểm thuộc đồ thị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $x = 0 \\Rightarrow y = 3 \\Rightarrow (0; 3)$. $y = 0 \\Rightarrow x = 3 \\Rightarrow (3; 0)$. Dùng thước vẽ đường thẳng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ hình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét: Vì $a = -1 < 0$ nên đồ thị đi xuống từ trái sang phải (nghịch biến). | Cho $x = 0 \\Rightarrow y = 3$, ta có điểm $A(0; 3)$.<br>Cho $y = 0 \\Rightarrow x = 3$, ta có điểm $B(3; 0)$.<br>Đường thẳng đi qua hai điểm $A(0; 3)$ và $B(3; 0)$ chính là đồ thị của hàm số $y = -x + 3$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tìm tọa độ giao điểm của hai đường thẳng bằng phương pháp đại số.
b) Nội dung: Tìm tọa độ giao điểm của đồ thị hàm số $y = 2x - 1$ và $y = -x + 2$.
c) Sản phẩm: Tọa độ giao điểm $(1; 1)$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Để tìm giao điểm của hai đồ thị, ta lập phương trình hoành độ giao điểm: $2x - 1 = -x + 2$.<br>- **HS:** Đọc đề và giải phương trình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $2x + x = 2 + 1 \\Rightarrow 3x = 3 \\Rightarrow x = 1$. Thay vào tìm $y = 2(1) - 1 = 1$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Tọa độ giao điểm là điểm $(1; 1)$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò xem trước Bài 29: Hệ số góc của đường thẳng. | Tọa độ giao điểm của hai đường thẳng là điểm $(1; 1)$. |
"""
    },
    {
        "filename": "15_KHBD_Toan8_Bai29_HeSoGocCuaDuongThang_Tiet66.md",
        "header": "TIẾT 66 - BÀI 29: HỆ SỐ GÓC CỦA ĐƯỜNG THẲNG\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 66 - BÀI 29: HỆ SỐ GÓC CỦA ĐƯỜNG THẲNG
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết góc tạo bởi đường thẳng $y = ax + b$ ($a \\neq 0$) và trục $Ox$: Là góc tạo bởi tia $Ax$ (chiều dương trục hoành) và tia $AT$ (phần đường thẳng nằm phía trên trục hoành).
- Hiểu ý nghĩa hình học của hệ số $a$: Được gọi là hệ số góc của đường thẳng $y = ax + b$.
  + Khi $a > 0$: Góc tạo bởi đường thẳng và trục $Ox$ là góc nhọn; $a$ càng lớn thì góc càng lớn.
  + Khi $a < 0$: Góc tạo bởi đường thẳng và trục $Ox$ là góc tù; $a$ càng lớn thì góc càng lớn.
- Nắm vững điều kiện để hai đường thẳng song song, cắt nhau, trùng nhau:
  + Song song: $a = a'$ và $b \\neq b'$.
  + Trùng nhau: $a = a'$ và $b = b'$.
  + Cắt nhau: $a \\neq a'$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát độ nghiêng của đường thẳng khi hệ số góc $a$ thay đổi.
- Giao tiếp và hợp tác: Làm việc nhóm kiểm tra điều kiện song song và cắt nhau của các cặp đường thẳng.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích vì sao hai đường thẳng có cùng hệ số góc lại có độ nghiêng như nhau và song song với nhau.
- Năng lực giải quyết vấn đề toán học: Xác định hệ số $a, b$ của đường thẳng thỏa mãn điều kiện hình học cho trước.

c) Năng lực số (NLS):
- ***5.2.TC2b: Sử dụng GeoGebra tạo thanh trượt tham số a và đo góc tạo bởi đường thẳng với trục Ox theo thời gian thực.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: Tìm hiểu cách các thuật toán AI xe tự hành nhận diện độ dốc mặt đường dựa trên hệ số góc của các vạch kẻ đường.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi phân biệt điều kiện song song ($b \\neq b'$) và trùng nhau ($b = b'$).
- Ý thức học tập tự giác, say mê nghiên cứu khoa học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, máy chiếu, thước đo góc bảng lớn, mô phỏng GeoGebra.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, thước thẳng, thước đo độ.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề từ thực tế độ dốc của mái nhà hoặc dốc cầu để hiểu khái niệm độ nghiêng.
b) Nội dung: Hai con dốc có độ nghiêng khác nhau thì đại lượng toán học nào quyết định độ nghiêng đó?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh con dốc thoai thoải và con dốc đứng. Đại lượng nào trong công thức hàm số $y = ax + b$ quyết định độ dốc nghiêng của đường thẳng?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hệ số $a$ đứng trước biến $x$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Hệ số $a$ được gọi là hệ số góc của đường thẳng. | Hệ số $a$ quyết định độ nghiêng của đường thẳng đối với trục hoành $Ox$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Khái niệm hệ số góc của đường thẳng (10 phút)
a) Mục tiêu: Định nghĩa góc tạo bởi đường thẳng với trục $Ox$ và ý nghĩa hệ số góc $a$.
b) Nội dung: Góc $\\alpha$ nhọn khi $a > 0$, góc $\\alpha$ tù khi $a < 0$.
c) Sản phẩm: Vở ghi bài và hình vẽ góc $\\alpha$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình vẽ góc $\\alpha$ tạo bởi đường thẳng $d: y = ax + b$ và trục hoành $Ox$. Giới thiệu: $a$ là hệ số góc, $b$ là tung độ gốc. Khi $a > 0$ thì $\\alpha$ là góc nhọn; Khi $a < 0$ thì $\\alpha$ là góc tù.<br>- **HS:** Ghi nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chỉ rõ hệ số góc của các đường thẳng: $y = 3x - 2$; $y = -x + 4$; $y = 0{,}5x$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Hệ số góc lần lượt là $3, -1, 0{,}5$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Hệ số góc chính là hệ số của $x$ khi hàm số ở dạng $y = ax + b$. | **1. Khái niệm hệ số góc:**<br>- Cho đường thẳng $d: y = ax + b$ ($a \\neq 0$).<br>- $a$ gọi là hệ số góc của đường thẳng $d$.<br>- $b$ gọi là tung độ gốc của đường thẳng $d$.<br>- $a > 0$: Góc tạo bởi $d$ và $Ox$ là góc nhọn.<br>- $a < 0$: Góc tạo bởi $d$ và $Ox$ là góc tù. |

### Hoạt động 2.2: Đường thẳng song song và đường thẳng cắt nhau (10 phút)
a) Mục tiêu: Nắm vững điều kiện song song, trùng nhau và cắt nhau của hai đường thẳng.
b) Nội dung: Xét hai đường thẳng $d: y = ax + b$ và $d': y = a'x + b'$ ($a, a' \\neq 0$).
c) Sản phẩm: Bảng điều kiện vị trí tương đối trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu điều kiện:<br>  + $d \\parallel d' \\iff a = a'$ và $b \\neq b'$.<br>  + $d \\equiv d' \\iff a = a'$ và $b = b'$.<br>  + $d$ cắt $d' \\iff a \\neq a'$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tìm các cặp đường thẳng song song trong các đường thẳng sau: $d_1: y = 2x + 1$; $d_2: y = 2x - 3$; $d_3: y = -2x + 1$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $d_1 \\parallel d_2$ vì cùng có $a = 2$ và $1 \\neq -3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Muốn song song bắt buộc phải kiểm tra cả điều kiện $b \\neq b'$ để không bị trùng nhau. | **2. Vị trí tương đối của hai đường thẳng:**<br>- Song song: $a = a'$ và $b \\neq b'$.<br>- Trùng nhau: $a = a'$ và $b = b'$.<br>- Cắt nhau: $a \\neq a'$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Xác định hệ số $a, b$ để đường thẳng song song với một đường thẳng cho trước và đi qua một điểm.
b) Nội dung: Bài 7.22, 7.23 SGK trang 53.
c) Sản phẩm: Lời giải chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tìm giá trị của $a$ và $b$ để đường thẳng $d: y = ax + b$ song song với đường thẳng $y = 3x - 2$ và đi qua điểm $A(1; 5)$.<br>- **HS:** Nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vì $d \\parallel y = 3x - 2$ nên $a = 3$ và $b \\neq -2$. Khi đó phương trình đường thẳng có dạng $y = 3x + b$. Vì $d$ đi qua $A(1; 5)$ nên: $5 = 3(1) + b \\Rightarrow b = 5 - 3 = 2$ (thỏa mãn $b \\neq -2$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá bài làm hoàn hảo, có đối chiếu điều kiện $b \\neq -2$ đầy đủ. | **Bài giải:**<br>- Vì đường thẳng $d$ song song với đường thẳng $y = 3x - 2$ nên:<br>$$a = 3 \\quad \\text{và} \\quad b \\neq -2$$<br>Khi đó phương trình đường thẳng $d$ có dạng $y = 3x + b$.<br>- Vì đường thẳng $d$ đi qua điểm $A(1; 5)$ nên ta thay $x = 1, y = 5$ vào phương trình:<br>$$5 = 3 \\cdot 1 + b \\Rightarrow b = 5 - 3 = 2\\text{ (thỏa mãn } b \\neq -2\\text{)}$$<br>Vậy $a = 3$ và $b = 2$, phương trình đường thẳng cần tìm là $y = 3x + 2$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhận biết điều kiện để hai đường thẳng vuông góc với nhau: $a \\cdot a' = -1$.
b) Nội dung: Giới thiệu mở rộng tích hai hệ số góc bằng $-1$.
c) Sản phẩm: Ghi chú kiến thức mở rộng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu định lý mở rộng: Hai đường thẳng $y = ax + b$ và $y = a'x + b'$ vuông góc với nhau khi và chỉ khi tích hai hệ số góc bằng $-1$: $a \\cdot a' = -1$.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kiểm tra hai đường thẳng $y = 2x + 1$ và $y = -0{,}5x + 3$ có vuông góc không?<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Vì $2 \\cdot (-0{,}5) = -1$ nên hai đường thẳng vuông góc với nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò xem lại toàn bộ bài để chuẩn bị cho tiết Luyện tập chung. | Hai đường thẳng vuông góc với nhau khi và chỉ khi $a \\cdot a' = -1$. |
"""
    },
    {
        "filename": "16_KHBD_Toan8_LuyenTapChung_Tiet67.md",
        "header": "TIẾT 67 - LUYỆN TẬP CHUNG: HÀM SỐ BẬC NHẤT VÀ ĐỒ THỊ (TRANG 53)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 67 - LUYỆN TẬP CHUNG: HÀM SỐ BẬC NHẤT VÀ ĐỒ THỊ (TRANG 53)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và nâng cao kỹ năng: Nhận biết hàm số bậc nhất, tính đồng biến/nghịch biến, vẽ đồ thị đường thẳng, xác định hệ số góc và xét vị trí tương đối giữa hai đường thẳng.
- Rèn luyện kỹ năng xác định công thức hàm số bậc nhất $y = ax + b$ khi biết các yếu tố hình học (đi qua điểm, song song, cắt trục tọa độ).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa mối liên hệ giữa hệ số $a, b$ và vị trí đường thẳng qua sơ đồ tư duy.
- Giao tiếp và hợp tác: Hợp tác nhóm giải các bài toán tương giao đồ thị và tính diện tích tam giác giới hạn bởi đồ thị và các trục tọa độ.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa điều kiện hai đường thẳng cắt nhau tại một điểm trên trục tung (cùng có tung độ gốc $b = b'$).
- Năng lực giải quyết vấn đề toán học: Tính diện tích tam giác tạo bởi đường thẳng với hai trục tọa độ $S = \\frac{1}{2} |x_0| \\cdot |y_0|$.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng máy tính cầm tay hoặc GeoGebra để xác định chính xác tọa độ giao điểm của hai đường thẳng.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D1.1: HS tìm hiểu ứng dụng của hệ số góc trong việc huấn luyện mạng nơ-ron nhân tạo điều chỉnh trọng số (Weights & Biases).***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác trong vẽ đồ thị và biến đổi đại số.
- Ý thức tự giác, vượt khó trong giải quyết các bài toán vận dụng cao.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 67 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, thước thẳng, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tái hiện nhanh các điều kiện song song, cắt nhau, trùng nhau của hai đường thẳng.
b) Nội dung: Điền điều kiện tương ứng vào bảng quan hệ vị trí của hai đường thẳng.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Nêu điều kiện để đường thẳng $d: y = ax + b$ song song với đường thẳng $d': y = a'x + b'$.<br>- **HS:** Đọc câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết nhanh câu trả lời lên bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con: $a = a'$ và $b \\neq b'$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn dắt vào bài luyện tập chung. | Điều kiện song song: $a = a'$ và $b \\neq b'$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức Hàm số bậc nhất và đồ thị qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 67; đối chiếu các nhánh định nghĩa, đồ thị, hệ số góc và ứng dụng.

![Sơ đồ tư duy Luyện tập chung Tiết 67](khbd-ill:mindmap-toan8-tiet67)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 67. Yêu cầu HS phân tích các nhánh: 1. Định nghĩa $y = ax + b$; 2. Đồ thị đường thẳng qua 2 điểm $(0; b)$ và $(-b/a; 0)$; 3. Hệ số góc & Vị trí tương đối; 4. Ứng dụng thực tế.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoạt động nhóm đôi tóm tắt công thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ kiến thức chuẩn mực. | **Hệ thống kiến thức trọng tâm:**<br>1. Hàm số bậc nhất: $y = ax + b$ ($a \\neq 0$).<br>2. Đồ thị: Đường thẳng cắt $Oy$ tại $(0; b)$, cắt $Ox$ tại $(-b/a; 0)$.<br>3. Hệ số góc $a$: Quyết định độ nghiêng và chiều biến thiên (đồng biến khi $a > 0$, nghịch biến khi $a < 0$).<br>4. Vị trí: Song song ($a=a', b \\neq b'$); Cắt nhau ($a \\neq a'$). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tìm giao điểm và tính diện tích tam giác giới hạn bởi đường thẳng và hai trục tọa độ.
b) Nội dung: Cho đường thẳng $d: y = 2x - 4$.<br>  a) Vẽ đồ thị hàm số trên mặt phẳng tọa độ $Oxy$;<br>  b) Gọi $A, B$ lần lượt là giao điểm của $d$ với các trục $Ox, Oy$. Tính diện tích tam giác $OAB$.
c) Sản phẩm: Bài giải chi tiết trên bảng và trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập vẽ đồ thị và tính diện tích tam giác vuông $OAB$.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giao điểm $Ox$: Cho $y = 0 \\Rightarrow 2x - 4 = 0 \\Rightarrow x = 2 \\Rightarrow A(2; 0) \\Rightarrow OA = 2$. Giao điểm $Oy$: Cho $x = 0 \\Rightarrow y = -4 \\Rightarrow B(0; -4) \\Rightarrow OB = |-4| = 4$. Tam giác $OAB$ vuông tại $O$, diện tích: $S = \\frac{1}{2} OA \\cdot OB = \\frac{1}{2} \\cdot 2 \\cdot 4 = 4$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao việc lấy giá trị tuyệt đối khi tính độ dài đoạn thẳng $OB = |-4| = 4$. | **Lời giải:**<br>a) Cho $x = 0 \\Rightarrow y = -4$, ta được điểm $B(0; -4)$.<br>Cho $y = 0 \\Rightarrow 2x - 4 = 0 \\Rightarrow x = 2$, ta được điểm $A(2; 0)$.<br>Đường thẳng đi qua hai điểm $A(2; 0)$ và $B(0; -4)$ là đồ thị của hàm số $y = 2x - 4$.<br>b) Ta có $OA = 2$ và $OB = |-4| = 4$.<br>Tam giác $OAB$ vuông tại $O$, do đó diện tích tam giác $OAB$ là:<br>$$S_{OAB} = \\frac{1}{2} OA \\cdot OB = \\frac{1}{2} \\cdot 2 \\cdot 4 = 4\\text{ (đơn vị diện tích)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng hàm số bậc nhất tính giá cước dịch vụ Internet cáp quang.
b) Nội dung: Cước hòa mạng ban đầu là $300\\,000$ đồng, cước thuê bao hàng tháng là $220\\,000$ đồng. Viết công thức hàm số tính tổng chi phí $y$ sau $x$ tháng sử dụng.
c) Sản phẩm: Công thức $y = 220\\,000x + 300\\,000$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Viết công thức hàm số tính tổng số tiền $y$ (đồng) sau $x$ tháng sử dụng dịch vụ Internet.<br>- **HS:** Đọc đề và viết công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $y = 220\\,000x + 300\\,000$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và dặn dò ôn tập toàn bộ chương VII chuẩn bị cho tiết Bài tập cuối chương VII. | Tổng chi phí sau $x$ tháng sử dụng là:<br>$$y = 220\\,000x + 300\\,000\\text{ (đồng)}$$ |
"""
    },
    {
        "filename": "17_KHBD_Toan8_BaiTapCuoiChuong7_Tiet68.md",
        "header": "TIẾT 68 - BÀI TẬP CUỐI CHƯƠNG VII: PHƯƠNG TRÌNH VÀ HÀM SỐ BẬC NHẤT (TRANG 54)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 68 - BÀI TẬP CUỐI CHƯƠNG VII: PHƯƠNG TRÌNH VÀ HÀM SỐ BẬC NHẤT (TRANG 54)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết toàn bộ kiến thức Chương VII: Phương trình bậc nhất một ẩn, giải bài toán bằng cách lập phương trình, khái niệm hàm số và đồ thị, hàm số bậc nhất $y = ax + b$, hệ số góc và vị trí tương đối của hai đường thẳng.
- Vận dụng kiến thức toàn chương để giải quyết các bài tập tổng hợp và dự án toán học thực tiễn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng kết kiến thức toàn chương qua sơ đồ tư duy; chủ động rà soát và đánh giá các kỹ năng giải phương trình và vẽ đồ thị.
- Giao tiếp và hợp tác: Tự tin thuyết trình báo cáo phương pháp giải các bài toán thực tế trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa quy tắc, lựa chọn công thức giải toán chính xác và ngắn gọn nhất.
- Năng lực giải quyết vấn đề toán học: Xử lý các bài toán phối hợp đại số và đồ thị hình học.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng phần mềm GeoGebra hoặc máy tính cầm tay để kiểm tra kết quả tính toán của toàn bộ đề bài tập ôn tập cuối chương VII.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D1.1: HS tìm hiểu ứng dụng hàm số bậc nhất trong việc mô phỏng các xu hướng kinh tế vĩ mô thông qua các công cụ AI phân tích tài chính.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật và tác phong khoa học.
- Tự tin, sẵn sàng tâm thế bước vào các tiết Hoạt động thực hành trải nghiệm và Chương VIII: Xác suất.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 68 (vector 300 DPI), máy chiếu, phiếu ôn tập chương.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay, thước thẳng.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập nhanh các công thức trọng tâm qua trò chơi trắc nghiệm "Vòng tròn kỳ diệu".
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm kiểm tra lý thuyết chương VII.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu hỏi trắc nghiệm lý thuyết.<br>- **HS:** Chuẩn bị bảng con ghi đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ đáp án sau hiệu lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giải thích ngắn gọn lý do chọn đáp án.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và dẫn vào bài ôn tập tổng kết chương VII. | Bảng đáp án trắc nghiệm chuẩn xác của học sinh. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ cấu trúc kiến thức Chương VII bằng Sơ đồ tư duy tổng hợp 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 68; hoàn thiện bức tranh tổng thể về phương trình và hàm số bậc nhất.

![Sơ đồ tư duy Bài tập cuối chương VII Tiết 68](khbd-ill:mindmap-toan8-tiet68)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy tổng thể Chương VII. Hướng dẫn HS hệ thống theo 4 nhánh lớn: 1. Phương trình bậc nhất một ẩn & Giải bài toán bằng lập PT; 2. Khái niệm hàm số và đồ thị; 3. Hàm số bậc nhất $y = ax + b$; 4. Hệ số góc và vị trí tương đối.<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành các chỗ trống trong phiếu tóm tắt.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS lên bảng điền các công thức trọng tâm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại toàn bộ hệ thống lý thuyết chương VII chuẩn mực. | **Tổng kết lý thuyết Chương VII:**<br>- Phương trình: $ax + b = 0$ ($a \\neq 0$), nghiệm $x = -b/a$; 3 bước giải bài toán bằng cách lập phương trình.<br>- Hàm số: $y = f(x)$, đồ thị hàm số.<br>- Hàm bậc nhất: $y = ax + b$ ($a \\neq 0$), hệ số góc $a$, vẽ đồ thị qua 2 điểm.<br>- Vị trí: Song song ($a=a', b \\neq b'$); Cắt nhau ($a \\neq a'$). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tự luận tổng hợp: Giải phương trình và xác định đường thẳng.
b) Nội dung: Bài 7.25, 7.27 SGK trang 54, 55.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tổng hợp: Cho hai đường thẳng $d_1: y = 2x - 1$ và $d_2: y = (m - 1)x + 3$.<br>  a) Tìm giá trị của $m$ để $d_1$ song song với $d_2$;<br>  b) Với $m = 3$, tìm tọa độ giao điểm của $d_1$ và $d_2$.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** a) Để $d_1 \\parallel d_2$ thì $m - 1 = 2$ và $3 \\neq -1$ (luôn đúng) $\\Rightarrow m = 3$. b) Khi $m = 3$ thì hai đường thẳng song song nên chúng không có giao điểm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao việc học sinh phát hiện ra ngay với $m = 3$ thì hai đường thẳng song song nên không có điểm chung. | **Lời giải:**<br>a) Để $d_1$ song song với $d_2$ thì:<br>$$m - 1 = 2 \\quad \\text{và} \\quad 3 \\neq -1\\text{ (thỏa mãn)}$$<br>Suy ra $m = 3$.<br>b) Khi $m = 3$, theo câu a thì $d_1 \\parallel d_2$, do đó hai đường thẳng này song song và không có giao điểm. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Định hướng chuẩn bị cho các tiết Hoạt động thực hành trải nghiệm ứng dụng tài chính và phần mềm GeoGebra ở Tiết 69, 70.
b) Nội dung: Giáo viên phân công chuẩn bị máy tính và thu thập dữ liệu giá cước taxi.
c) Sản phẩm: Kế hoạch làm bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến nội dung 2 tiết trải nghiệm tiếp theo: Tìm hiểu cước taxi thực tế và vẽ đồ thị hàm số bằng GeoGebra.<br>- **HS:** Ghi chép yêu cầu chuẩn bị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tìm kiếm bảng giá cước của các hãng taxi phổ biến.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác nhận sẵn sàng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi kết quả học tập xuất sắc của cả lớp trong Chương VII. | Chuẩn bị đầy đủ số liệu thực tế và phần mềm cho 2 tiết trải nghiệm tiếp theo. |
"""
    },
    {
        "filename": "18_KHBD_Toan8_HDTN_TaiChinhVaGeoGebra_Tiet69-70.md",
        "header": "TIẾT 69, 70 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: ỨNG DỤNG CỦA HÀM SỐ BẬC NHẤT TRONG TÀI CHÍNH VÀ VẼ ĐỒ THỊ VỚI PHẦN MỀM GEOGEBRA\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 69, 70 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: ỨNG DỤNG CỦA HÀM SỐ BẬC NHẤT TRONG TÀI CHÍNH VÀ VẼ ĐỒ THỊ VỚI PHẦN MỀM GEOGEBRA
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng hàm số bậc nhất $y = ax + b$ để mô hình hóa và phân tích các bài toán tài chính đời sống: Giá cước vận chuyển, tính điểm hòa vốn (Break-even Point), phân tích doanh thu và chi phí sản xuất.
- Sử dụng thành thạo phần mềm hình học động GeoGebra để:
  + Nhập và tính toán các phép biến đổi trên phân thức đại số;
  + Vẽ đồ thị của hàm số bậc nhất và xác định trực quan tọa độ giao điểm của hai đường thẳng;
  + Tạo thanh trượt (Slider) để khảo sát sự biến thiên của đồ thị hàm số khi hệ số $a, b$ thay đổi.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác các lệnh trên GeoGebra, khám phá các tính năng đồ họa và bảng tính đại số.
- Giao tiếp và hợp tác: Làm việc nhóm thiết kế bảng tính so sánh chi phí đi taxi giữa các hãng khác nhau và thuyết trình đề xuất lựa chọn kinh tế nhất.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Chuyển đổi bảng giá dịch vụ thực tế thành hệ các hàm số bậc nhất trên cùng một mặt phẳng tọa độ.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng công nghệ thông tin giải quyết nhanh các bài toán toán học phức tạp.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS chọn mô phỏng đồ thị hàm số trên GeoGebra để xác định điểm hòa vốn; 1.3.TC2a: HS tổ chức số liệu chi phí vào bảng tính phân tích tự động.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu cách AI sử dụng mô hình tối ưu hóa đồ thị tuyến tính để phân bổ tài nguyên kinh tế thông minh.***

## 3. Về phẩm chất
- Rèn luyện tư duy thực tế, tính toán chi tiêu thông thái và tiết kiệm trong sinh hoạt.
- Tinh thần say mê ứng dụng toán học và công nghệ vào giải quyết các bài toán đời sống.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn phần mềm GeoGebra (hoặc bản GeoGebra Online), máy chiếu, bảng giá cước taxi thực tế của 3 hãng xe lớn.
2. Học sinh: Máy vi tính phòng máy, sổ tay ghi chép, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (10 phút)
a) Mục tiêu: Đặt bài toán lựa chọn hãng taxi kinh tế nhất cho chuyến đi tham quan của gia đình.
b) Nội dung: Hãng taxi A có giá mở cửa $10\\,000$ đồng và $14\\,000$ đồng$/\\text{km}$ tiếp theo. Hãng B không có giá mở cửa nhưng tính đồng giá $16\\,000$ đồng$/\\text{km}$. Đi bao nhiêu km thì giá tiền hai hãng bằng nhau? Đi xa thì nên chọn hãng nào?
c) Sản phẩm: Sự hào hứng tranh luận của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán so sánh chi phí của hai hãng taxi A và B. Hướng dẫn lập hai hàm số bậc nhất tương ứng: $y_A = 14x + 10$ và $y_B = 16x$ (đơn vị nghìn đồng).<br>- **HS:** Đọc đề và thảo luận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho hai hàm số bằng nhau: $14x + 10 = 16x \\Rightarrow 2x = 10 \\Rightarrow x = 5\\text{ km}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nếu đi đúng $5\\text{ km}$ thì giá hai hãng bằng nhau ($80\\,000$ đồng). Nếu đi trên $5\\text{ km}$ thì hãng A rẻ hơn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài thực hành: Hôm nay chúng ta sẽ dùng GeoGebra để vẽ đồ thị và trực quan hóa điểm cắt nhau này trong chớp mắt. | Điểm cắt nhau của hai đường thẳng chính là điểm hòa vốn để ra quyết định kinh tế tối ưu. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (35 phút)
### Hoạt động 2.1: Thực hành tính toán phân thức trên GeoGebra CAS (15 phút)
a) Mục tiêu: Sử dụng vùng tính toán biểu thức đại số (CAS) của GeoGebra để rút gọn phân thức tự động.
b) Nội dung: Nhập lệnh Simplify và Factor trên GeoGebra để rút gọn các phân thức cồng kềnh.
c) Sản phẩm: Thao tác thành thạo của học sinh trên máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn mở vùng CAS trong GeoGebra: Vào Menu View $\\rightarrow$ Chọn CAS. Nhập lệnh: `Simplify((x^2 - 4)/(x^2 + 2x))` và quan sát kết quả tự động xuất ra `(x - 2)/x`.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự thực hành nhập các phân thức của Bài tập cuối chương VI để kiểm tra kết quả tính tay.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác nhận kết quả máy tính khớp hoàn toàn với bài làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định: GeoGebra là công cụ kiểm tra đắc lực giúp học sinh tự học và tự soát lỗi hiệu quả. | Sử dụng thành thạo lệnh `Simplify` và `Factor` trong môi trường GeoGebra CAS để xử lý phân thức đại số. |

### Hoạt động 2.2: Vẽ đồ thị hàm số và xác định giao điểm bằng GeoGebra (20 phút)
a) Mục tiêu: Biết cách nhập hàm số vào thanh Input và dùng công cụ Intersect tìm giao điểm đồ thị.
b) Nội dung: Nhập hai hàm số cước taxi $f(x) = 14x + 10$ và $g(x) = 16x$.
c) Sản phẩm: Hình vẽ hai đường thẳng cắt nhau tại điểm $(5; 80)$ trên màn hình máy tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn:<br>  1. Nhập vào ô lệnh: `f(x) = 14x + 10` (nhấn Enter).<br>  2. Nhập tiếp: `g(x) = 16x` (nhấn Enter).<br>  3. Chọn công cụ Điểm $\\rightarrow$ "Intersect" (Giao điểm của hai đối tượng) $\\rightarrow$ Nhấp lần lượt vào hai đường thẳng. Quan sát tọa độ giao điểm $A(5; 80)$ xuất hiện trên Vùng đại số.<br>- **HS:** Thực hiện thao tác trên máy tính cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát đồ thị: Với $x < 5$, đường $g(x)$ nằm dưới đường $f(x)$ (hãng B rẻ hơn); với $x > 5$, đường $f(x)$ nằm dưới (hãng A rẻ hơn).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Thuyết minh sự so sánh trực quan qua màu sắc hai đường thẳng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương kỹ năng đọc đồ thị hình học xuất sắc của học sinh. | Tọa độ giao điểm $A(5; 80)$ thể hiện rõ tại $x = 5\\text{ km}$ thì chi phí hai hãng bằng nhau là $80\\,000$ đồng. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (35 phút)
a) Mục tiêu: Thực hành tạo thanh trượt (Slider) hệ số $a, b$ để khảo sát chuyển động của đường thẳng.
b) Nội dung: Tạo thanh trượt $a \\in [-5; 5]$, $b \\in [-5; 5]$ và vẽ đường thẳng $y = ax + b$.
c) Sản phẩm: Mô phỏng đồ thị động chuyển động theo thanh trượt của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn tạo Slider:<br>  1. Chọn công cụ Slider $\\rightarrow$ Nhấp chuột tạo thanh trượt $a$ và thanh trượt $b$.<br>  2. Nhập lệnh vẽ hàm số: `y = a*x + b`.<br>  3. Dùng chuột kéo rê thanh trượt $a$ để quan sát độ nghiêng thay đổi; kéo thanh trượt $b$ để quan sát đường thẳng tịnh tiến lên xuống song song với chính nó.<br>- **HS:** Thực hành tạo sản phẩm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hào hứng điều khiển các thanh trượt và quan sát đường thẳng xoay quanh điểm $(0; b)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Chiếu sản phẩm của các nhóm lên màn hình lớn phòng máy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá: Việc trực quan hóa giúp khắc sâu bản chất hình học của hệ số góc và tung độ gốc một cách tự nhiên, sâu sắc nhất. | Học sinh làm chủ công cụ Slider, hiểu sâu sắc ý nghĩa của hệ số góc $a$ và tung độ gốc $b$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Đóng gói và lưu sản phẩm thực hành trải nghiệm.
b) Nội dung: Học sinh lưu tệp `.ggb` và xuất ảnh poster phân tích tài chính cá nhân.
c) Sản phẩm: Tệp bài làm nộp lên hệ thống học tập của trường.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các nhóm lưu tệp: `Toan8_NhomX_TaiChinhGeoGebra.ggb` và xuất ảnh đồ thị nộp bài.<br>- **HS:** Thực hiện thao tác lưu tệp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thu dọn phòng máy, tắt máy vi tính gọn gàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp kiểm tra và báo cáo sĩ số nộp bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương tinh thần học tập sáng tạo, làm chủ công nghệ của cả lớp; dặn dò chuẩn bị bước sang Chương VIII: Xác suất biến cố ở tiết sau. | Hoàn thành xuất sắc 2 tiết thực hành trải nghiệm ứng dụng tài chính và phần mềm GeoGebra. |
"""
    }
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print("Hoàn tất tạo 11 KHBD Chương VII: Phương trình và Hàm số bậc nhất (Tiết 55 - 70)!")
