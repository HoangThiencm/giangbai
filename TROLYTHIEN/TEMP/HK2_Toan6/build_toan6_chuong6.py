# -*- coding: utf-8 -*-
"""
Script sinh 8 KHBD Chương VI: Phân số (Tiết 51 - 65) - Toán 6 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan6"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    {
        "filename": "01_KHBD_Toan6_Bai23_MoRongPhanSo_Tiet51-52.md",
        "header": "TIẾT 51, 52 - BÀI 23: MỞ RỘNG PHÂN SỐ. PHÂN SỐ BẰNG NHAU\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 51, 52 - BÀI 23: MỞ RỘNG PHÂN SỐ. PHÂN SỐ BẰNG NHAU
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm phân số với tử số và mẫu số là các số nguyên, trong đó mẫu số phải khác $0$.
- Nắm vững khái niệm hai phân số bằng nhau: $\\frac{a}{b} = \\frac{c}{d}$ nếu $a \\cdot d = b \\cdot c$ ($a, b, c, d \\in \\mathbb{Z}; b, d \\neq 0$).
- Vận dụng tính chất cơ bản của phân số để rút gọn phân số và viết một phân số bất kì dưới dạng phân số có mẫu số dương.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác tìm hiểu khái niệm phân số có tử và mẫu là các số nguyên, phân biệt với phân số đã học ở Tiểu học.
- Giao tiếp và hợp tác: Tương tác, thảo luận nhóm để giải thích quy tắc hai phân số bằng nhau thông qua tích chéo.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh tích chéo $a \\cdot d$ và $b \\cdot c$ để kiểm tra tính bằng nhau của hai phân số.
- Năng lực giải quyết vấn đề toán học: Tìm số nguyên chưa biết $x$ trong đẳng thức hai phân số bằng nhau.

c) Năng lực số (NLS):
- ***5.3.TC1a: Học sinh sử dụng máy tính cầm tay để kiểm tra tích chéo $a \\cdot d$ và $b \\cdot c$ đối với các số nguyên có giá trị tuyệt đối lớn.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh tra cứu trợ lý AI để tìm hiểu lịch sử ra đời của phân số âm trong toán học thế giới.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi thực hiện phép nhân các số nguyên có dấu âm.
- Tinh thần trách nhiệm, chủ động hoàn thành các bài tập được giao.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, bài giảng điện tử, phiếu học tập nhóm.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, đồ dùng học tập, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Gợi lại khái niệm phân số đã học ở tiểu học và tạo tình huống có vấn đề xuất hiện tử số và mẫu số là số nguyên âm.
b) Nội dung: Trả lời câu hỏi phân chia số bánh, nhiệt độ trung bình dưới $0^\\circ\\text{C}$.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt vấn đề: Ở Tiểu học ta đã biết phân số $\\frac{1}{2}, \\frac{3}{4}$. Vậy nếu nhiệt độ giảm $3^\\circ\\text{C}$ trong $4$ giờ thì mức giảm trung bình mỗi giờ được biểu diễn bởi biểu thức nào? Có thể viết dưới dạng $\\frac{-3}{4}$ được không?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 1 HS phát biểu suy nghĩ cá nhân.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định toán học mở rộng phân số với tử và mẫu là các số nguyên, dẫn dắt vào bài mới. | Phân số mở rộng có tử và mẫu là các số nguyên, mẫu số khác $0$. Ví dụ: $\\frac{-3}{4}, \\frac{5}{-7}, \\frac{-2}{-9}$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Mở rộng khái niệm phân số (20 phút)
a) Mục tiêu: HS hiểu được dạng tổng quát của phân số $\\frac{a}{b}$ với $a, b \\in \\mathbb{Z}, b \\neq 0$.
b) Nội dung: Thực hiện HĐ1, HĐ2 và ví dụ 1 trong SGK.
c) Sản phẩm: Vở ghi bài và câu trả lời phiếu học tập.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho biết dạng tổng quát của phân số đã học ở Tiểu học. Khi mở rộng sang tập số nguyên $\\mathbb{Z}$, phân số được định nghĩa thế nào?<br>- **HS:** Tiếp nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc SGK, ghi nhớ định nghĩa: Người ta gọi $\\frac{a}{b}$ với $a, b \\in \\mathbb{Z}, b \\neq 0$ là một phân số, $a$ là tử số, $b$ là mẫu số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Yêu cầu HS lấy $3$ ví dụ về phân số và chỉ rõ tử số, mẫu số.<br>- **HS:** Phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và chốt lại điều kiện tiên quyết: Mẫu số bắt buộc phải khác $0$. | **1. Mở rộng khái niệm phân số:**<br>- Phân số có dạng $\\frac{a}{b}$ với $a, b \\in \\mathbb{Z}, b \\neq 0$.<br>- $a$ là tử số (tử), $b$ là mẫu số (mẫu).<br>- Ví dụ: $\\frac{-2}{3}$ (tử là $-2$, mẫu là $3$); $\\frac{4}{-5}$ (tử là $4$, mẫu là $-5$).<br>- Chú ý: Số nguyên $a$ cũng là một phân số với mẫu là $1$: $a = \\frac{a}{1}$. |

### Hoạt động 2.2: Phân số bằng nhau (25 phút)
a) Mục tiêu: Nắm vững quy tắc hai phân số bằng nhau thông qua tích chéo: $\\frac{a}{b} = \\frac{c}{d} \\iff a \\cdot d = b \\cdot c$.
b) Nội dung: Xét các cặp phân số bằng nhau ở tiểu học và mở rộng sang số nguyên.
c) Sản phẩm: Lời giải các bài luyện tập 1, 2.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho hai phân số $\\frac{1}{2}$ và $\\frac{2}{4}$. Hãy so sánh tích $1 \\cdot 4$ và $2 \\cdot 2$. Từ đó nêu quy tắc tổng quát cho hai phân số $\\frac{a}{b}$ và $\\frac{c}{d}$.<br>- **HS:** Quan sát và tính toán tích chéo.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi, phát biểu quy tắc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện cặp đôi giải thích: $\\frac{-3}{4} = \\frac{6}{-8}$ vì $(-3) \\cdot (-8) = 4 \\cdot 6 = 24$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt quy tắc hai phân số bằng nhau. Nhắc nhở HS không dùng dấu tương đương tùy tiện và chỉ kết luận giá trị rõ ràng. | **2. Hai phân số bằng nhau:**<br>- Hai phân số $\\frac{a}{b}$ và $\\frac{c}{d}$ gọi là bằng nhau nếu $a \\cdot d = b \\cdot c$. Ta viết: $\\frac{a}{b} = \\frac{c}{d}$.<br>- Ví dụ: $\\frac{-1}{3} = \\frac{2}{-6}$ vì $(-1) \\cdot (-6) = 3 \\cdot 2 = 6$.<br>- Ngược lại: $\\frac{-3}{5} \\neq \\frac{3}{5}$ vì $(-3) \\cdot 5 = -15 \\neq 5 \\cdot 3 = 15$. |

### Hoạt động 2.3: Tính chất cơ bản của phân số (20 phút)
a) Mục tiêu: Vận dụng nhân hoặc chia cả tử và mẫu với cùng một số nguyên khác $0$ để biến đổi phân số.
b) Nội dung: Tìm hiểu tính chất cơ bản và quy tắc đổi dấu mẫu âm.
c) Sản phẩm: Lời giải bài Luyện tập 3.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu tính chất cơ bản: Nhân/chia cả tử và mẫu với cùng số nguyên $m, n \\neq 0$. Hướng dẫn quy tắc đưa phân số về mẫu dương.<br>- **HS:** Tiếp thu kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng viết phân số $\\frac{3}{-5}$ thành phân số có mẫu dương.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Lên bảng trình bày: $\\frac{3}{-5} = \\frac{3 \\cdot (-1)}{(-5) \\cdot (-1)} = \\frac{-3}{5}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Mọi phân số có mẫu âm đều viết được thành phân số bằng nó và có mẫu dương bằng cách nhân cả tử và mẫu với $-1$. | **3. Tính chất cơ bản của phân số:**<br>- Nếu nhân cả tử và mẫu của một phân số với cùng một số nguyên khác $0$ thì ta được một phân số bằng phân số đã cho:<br>$$\\frac{a}{b} = \\frac{a \\cdot m}{b \\cdot m} \\quad (m \\in \\mathbb{Z}, m \\neq 0)$$<br>- Nếu chia cả tử và mẫu của một phân số cho một ước chung của chúng thì ta được một phân số bằng phân số đã cho:<br>$$\\frac{a}{b} = \\frac{a : n}{b : n} \\quad (n \\in \\text{ƯC}(a, b))$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Củng cố kỹ năng kiểm tra phân số bằng nhau và tìm số nguyên $x$ chưa biết.
b) Nội dung: Giải Bài 6.1, 6.2, 6.3 trong SGK.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tìm $x$: Tìm số nguyên $x$ biết $\\frac{x}{6} = \\frac{-2}{3}$.<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng định nghĩa phân số bằng nhau: $x \\cdot 3 = 6 \\cdot (-2) = -12$, từ đó tính ra $x = -4$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày, các HS khác kiểm tra chéo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa cách trình bày tìm $x$, tránh kết luận tập nghiệm không phù hợp. | **Bài tập tìm $x$:**<br>Ta có $\\frac{x}{6} = \\frac{-2}{3}$<br>Suy ra: $x \\cdot 3 = 6 \\cdot (-2)$<br>$3 \\cdot x = -12$<br>$x = -12 : 3$<br>$x = -4$.<br>Vậy giá trị của $x$ cần tìm là $-4$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng kiến thức phân số vào các tình huống thực tiễn đơn giản.
b) Nội dung: Bài toán đo lường lượng nước trong bình chứa có vạch chia âm và dương.
c) Sản phẩm: Bài làm trong phiếu bài tập cá nhân.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ về nhà: Viết các số đo thời gian sau dưới dạng phân số với đơn vị giờ: $15$ phút, $45$ phút, $50$ phút, và rút gọn về phân số tối giản.<br>- **HS:** Ghi chép yêu cầu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc độc lập tại nhà.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Nộp vở bài tập vào đầu tiết sau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò HS ôn lại quy tắc phân số bằng nhau và xem trước Bài 24. | **Hướng dẫn về nhà:**<br>- $15$ phút $= \\frac{15}{60} = \\frac{1}{4}$ giờ.<br>- $45$ phút $= \\frac{45}{60} = \\frac{3}{4}$ giờ.<br>- $50$ phút $= \\frac{50}{60} = \\frac{5}{6}$ giờ. |
"""
    },
    {
        "filename": "02_KHBD_Toan6_Bai24_SoSanhPhanSo_HonSoDuong_Tiet53-54.md",
        "header": "TIẾT 53, 54 - BÀI 24: SO SÁNH PHÂN SỐ. HỖN SỐ DƯƠNG\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 53, 54 - BÀI 24: SO SÁNH PHÂN SỐ. HỖN SỐ DƯƠNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- So sánh được hai phân số có cùng mẫu số hoặc khác mẫu số (bằng cách quy đồng mẫu số dương).
- Nhận biết phân số dương, phân số âm và áp dụng so sánh với số $0$.
- Hiểu và viết được một phân số lớn hơn $1$ dưới dạng hỗn số dương và ngược lại.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quy đồng mẫu số các phân số và thực hiện so sánh theo quy tắc.
- Giao tiếp và hợp tác: Thảo luận nhóm lựa chọn mẫu số chung nhỏ nhất để quy đồng thuận tiện nhất.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận so sánh hai phân số bằng cách so sánh với phân số trung gian hoặc so sánh với $0, 1$.
- Năng lực mô hình hoá toán học: Chuyển đổi hỗn số biểu thị số lượng vật phẩm trong đời sống thực tế thành phân số để tính toán.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng chức năng phân số trên máy tính cầm tay để kiểm tra thứ tự từ nhỏ đến lớn của dãy gồm nhiều phân số.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Ứng dụng AI tạo các câu đố so sánh phân số thú vị gắn liền với các kỳ quan địa lý trên thế giới.***

## 3. Về phẩm chất
- Trung thực, cẩn thận trong việc tính toán BCNN để tìm mẫu chung.
- Say mê học tập, yêu thích khám phá vẻ đẹp của toán học số học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, bảng phụ, phiếu bài tập.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập quy tắc so sánh hai phân số cùng mẫu ở tiểu học và tạo nhu cầu so sánh phân số có số âm.
b) Nội dung: So sánh $\\frac{2}{5}$ và $\\frac{4}{5}$; dự đoán so sánh $\\frac{-2}{5}$ và $\\frac{-4}{5}$.
c) Sản phẩm: Bảng nhóm của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu câu hỏi: So sánh $\\frac{2}{5}$ và $\\frac{4}{5}$. Nếu tử số là số nguyên âm: So sánh $\\frac{-2}{5}$ và $\\frac{-4}{5}$ thì phân số nào lớn hơn?<br>- **HS:** Lắng nghe câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhớ lại so sánh hai số nguyên âm $-2 > -4$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Vì $-2 > -4$ nên $\\frac{-2}{5} > \\frac{-4}{5}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Xác nhận và dẫn dắt vào quy tắc so sánh hai phân số có cùng mẫu dương. | Trong hai phân số có cùng một mẫu dương, phân số nào có tử lớn hơn thì phân số đó lớn hơn. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: So sánh hai phân số (35 phút)
a) Mục tiêu: Nắm vững quy tắc so sánh hai phân số cùng mẫu dương và khác mẫu số qua bước quy đồng.
b) Nội dung: Quy tắc quy đồng mẫu số và so sánh phân số.
c) Sản phẩm: Kết quả bài tập so sánh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc: Muốn so sánh hai phân số không cùng mẫu, ta viết chúng dưới dạng hai phân số có cùng một mẫu dương rồi so sánh các tử số với nhau.<br>- **HS:** Ghi nhận quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện so sánh $\\frac{-3}{4}$ và $\\frac{-4}{5}$. Viết mẫu chung là $20$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: $\\frac{-3}{4} = \\frac{-15}{20}$; $\\frac{-4}{5} = \\frac{-16}{20}$. Vì $-15 > -16$ nên $\\frac{-15}{20} > \\frac{-16}{20}$, tức là $\\frac{-3}{4} > \\frac{-4}{5}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy trình 3 bước: 1. Đưa về mẫu dương; 2. Quy đồng mẫu số; 3. So sánh tử số. | **1. So sánh hai phân số:**<br>- Quy tắc: Trong hai phân số có cùng một mẫu dương, phân số có tử lớn hơn thì lớn hơn.<br>- Với hai phân số khác mẫu: Quy đồng về cùng một mẫu dương rồi so sánh các tử số.<br>- Nhận xét: Phân số có tử và mẫu cùng dấu thì lớn hơn $0$ (phân số dương); Phân số có tử và mẫu khác dấu thì nhỏ hơn $0$ (phân số âm). |

### Hoạt động 2.2: Hỗn số dương (30 phút)
a) Mục tiêu: Nhận biết cấu tạo hỗn số dương gồm phần nguyên và phần phân số; cách chuyển đổi qua lại giữa phân số và hỗn số.
b) Nội dung: Ví dụ chia có dư để viết phân số lớn hơn $1$ thành hỗn số dương.
c) Sản phẩm: Bảng con và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khi chia $11$ cho $4$, ta được thương là $2$ và số dư là $3$. Ta viết $\\frac{11}{4} = 2 + \\frac{3}{4} = 2\\frac{3}{4}$. Giới thiệu cách gọi: $2\\frac{3}{4}$ là hỗn số dương.<br>- **HS:** Tiếp thu khái niệm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện chuyển đổi: $\\frac{17}{5}$ sang hỗn số và chuyển $3\\frac{2}{7}$ sang phân số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $\\frac{17}{5} = 3\\frac{2}{5}$; $3\\frac{2}{7} = \\frac{3 \\cdot 7 + 2}{7} = \\frac{23}{7}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và lưu ý phần phân số của hỗn số luôn nhỏ hơn $1$. | **2. Hỗn số dương:**<br>- Cho phân số $\\frac{a}{b}$ với $a > b > 0$. Nếu $a$ chia cho $b$ được thương là $q$ và số dư là $r$ ($0 < r < b$) thì ta viết:<br>$$\\frac{a}{b} = q\\frac{r}{b}$$<br>- $q$ là phần nguyên, $\\frac{r}{b}$ là phần phân số.<br>- Ngược lại: $q\\frac{r}{b} = \\frac{q \\cdot b + r}{b}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Luyện tập so sánh dãy phân số và sắp xếp theo thứ tự tăng dần.
b) Nội dung: Bài tập 6.8, 6.9 SGK.
c) Sản phẩm: Bài giải trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu sắp xếp các phân số sau theo thứ tự tăng dần: $\\frac{-5}{6}; \\frac{2}{3}; 0; \\frac{-7}{6}; \\frac{5}{6}$.<br>- **HS:** Nhận đề bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân loại nhóm số âm, số $0$, nhóm số dương rồi so sánh từng nhóm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trình bày thứ tự: $\\frac{-7}{6} < \\frac{-5}{6} < 0 < \\frac{2}{3} < \\frac{5}{6}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách làm nhanh dựa vào tính chất phân loại qua số $0$. | **Sắp xếp thứ tự phân số:**<br>- Nhóm phân số âm: $\\frac{-7}{6} < \\frac{-5}{6}$.<br>- Phân số trung gian: $0$.<br>- Nhóm phân số dương: $\\frac{2}{3} = \\frac{4}{6} < \\frac{5}{6}$.<br>- Kết luận thứ tự tăng dần:<br>$$\\frac{-7}{6} < \\frac{-5}{6} < 0 < \\frac{2}{3} < \\frac{5}{6}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng so sánh phân số vào so sánh số đo vận tốc, thời gian trong thực tế.
b) Nội dung: So sánh vận tốc chạy của hai bạn học sinh.
c) Sản phẩm: Lời giải ngắn gọn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ: Bạn An chạy $100\\text{ m}$ hết $\\frac{1}{4}$ phút, bạn Bình chạy hết $\\frac{3}{10}$ phút. Hỏi bạn nào chạy nhanh hơn?<br>- **HS:** Ghi bài tập về nhà.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quy đồng: $\\frac{1}{4} = \\frac{5}{20}$; $\\frac{3}{10} = \\frac{6}{20}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Báo cáo kết quả vào đầu giờ tiết luyện tập chung.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Lưu ý: Thời gian chạy ít hơn đồng nghĩa với vận tốc nhanh hơn. | **Giải toán thực tế:**<br>Ta có $\\frac{1}{4} = \\frac{5}{20}$ và $\\frac{3}{10} = \\frac{6}{20}$.<br>Vì $\\frac{5}{20} < \\frac{6}{20}$ nên bạn An mất ít thời gian hơn.<br>Do đó bạn An chạy nhanh hơn bạn Bình. |
"""
    },
    {
        "filename": "03_KHBD_Toan6_LuyenTapChung_Tiet55.md",
        "header": "TIẾT 55 - LUYỆN TẬP CHUNG (TRANG 13)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 55 - LUYỆN TẬP CHUNG (TRANG 13)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và khắc sâu các kiến thức về: Khái niệm phân số, hai phân số bằng nhau, tính chất cơ bản của phân số, so sánh phân số và hỗn số dương.
- Vận dụng thành thạo các tính chất để rút gọn về phân số tối giản và sắp xếp dãy phân số.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ sơ đồ tư duy hệ thống kiến thức Bài 23 và Bài 24; chủ động tìm phương pháp giải tối ưu.
- Giao tiếp và hợp tác: Trao đổi nhóm tự tin, phân tích rõ lý do khi kiểm tra kết quả chéo.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích căn cứ quy đồng và so sánh phân số bằng nhiều cách khác nhau.
- Năng lực giải quyết vấn đề toán học: Giải các bài toán tìm số nguyên thỏa mãn điều kiện phân số bằng nhau hoặc bất đẳng thức phân số.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay để rút gọn phân số có tử và mẫu số lớn bằng phím phân số tự động.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI gợi ý sơ đồ tư duy phân nhánh trực quan tóm tắt các tính chất cơ bản của phân số.***

## 3. Về phẩm chất
- Cẩn thận, chính xác trong các phép biến đổi dấu âm.
- Tinh thần kiên trì, say mê giải quyết các bài toán thử thách.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2, KHBD, Sơ đồ tư duy Mindmap Tiết 55 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tái hiện nhanh các công thức và quy tắc cốt lõi đã học.
b) Nội dung: Trả lời nhanh 2 câu hỏi trắc nghiệm kiểm tra lý thuyết.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: 1. Nêu điều kiện để $\\frac{a}{b} = \\frac{c}{d}$. 2. Viết $\\frac{7}{-4}$ thành phân số có mẫu dương.<br>- **HS:** Đọc kỹ câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết nhanh câu trả lời vào bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con đồng loạt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tinh thần học tập và dẫn dắt vào tiết luyện tập. | 1. $a \\cdot d = b \\cdot c$.<br>2. $\\frac{7}{-4} = \\frac{-7}{4}$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức phân số, phân số bằng nhau, so sánh phân số và hỗn số dương bằng Sơ đồ tư duy trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 55; thảo luận các nhánh kiến thức trọng tâm.

![Sơ đồ tư duy Luyện tập chung Tiết 55](khbd-ill:mindmap-toan6-tiet55)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở ghi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Tiết 55. Yêu cầu HS phân tích các nhánh chính: Khái niệm phân số, Phân số bằng nhau, Tính chất cơ bản, So sánh và Hỗn số.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoạt động nhóm 4, nhắc lại các định nghĩa và công thức tương ứng với từng nhánh sơ đồ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm đứng tại chỗ thuyết trình tóm tắt theo sơ đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá phần trình bày, nhấn mạnh mối liên hệ logic giữa tính chất cơ bản và việc quy đồng so sánh phân số. | **Hệ thống kiến thức trọng tâm:**<br>1. Phân số: $\\frac{a}{b}$ ($a, b \\in \\mathbb{Z}, b \\neq 0$).<br>2. Bằng nhau: $\\frac{a}{b} = \\frac{c}{d} \\iff a \\cdot d = b \\cdot c$.<br>3. Tính chất: Nhân/chia cùng số nguyên khác $0$. Đổi mẫu âm thành mẫu dương.<br>4. So sánh: Cùng mẫu dương (tử lớn hơn thì lớn hơn); Khác mẫu (quy đồng mẫu dương rồi so sánh tử).<br>5. Hỗn số dương: $q\\frac{r}{b} = \\frac{q \\cdot b + r}{b}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Rèn luyện kỹ năng giải các bài toán rút gọn, so sánh và tìm giá trị ẩn số.
b) Nội dung: Bài 6.11, 6.12, 6.13 SGK trang 13, 14.
c) Sản phẩm: Lời giải chi tiết trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài toán:<br>  Bài 1: Rút gọn các phân số: $\\frac{-18}{24}; \\frac{36}{-60}$.<br>  Bài 2: Tìm số nguyên $x$ biết: $\\frac{-3}{x} = \\frac{x}{-27}$.<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br>- Bài 1: $\\frac{-18}{24} = \\frac{-18:6}{24:6} = \\frac{-3}{4}$; $\\frac{36}{-60} = \\frac{36:(-12)}{-60:(-12)} = \\frac{-3}{5}$.<br>- Bài 2: $(-3) \\cdot (-27) = x \\cdot x \\Rightarrow x^2 = 81 \\Rightarrow x = 9$ hoặc $x = -9$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kiến thức: Khi giải $x^2 = 81$ cần lưu ý cả hai giá trị đối nhau $x = 9$ hoặc $x = -9$. Không kết luận tập nghiệm. | **Lời giải bài tập:**<br>**Bài 1:**<br>$$\\frac{-18}{24} = \\frac{-3}{4}; \\quad \\frac{36}{-60} = \\frac{-3}{5}$$<br>**Bài 2:**<br>Ta có $\\frac{-3}{x} = \\frac{x}{-27}$<br>Suy ra: $x^2 = (-3) \\cdot (-27) = 81$<br>Vì $9^2 = 81$ và $(-9)^2 = 81$ nên $x = 9$ hoặc $x = -9$.<br>Vậy $x = 9$ hoặc $x = -9$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng kiến thức hỗn số vào giải quyết bài toán chia phần bánh trong sinh hoạt gia đình.
b) Nội dung: Bài toán chia $9$ chiếc bánh pizza cho $4$ bạn sao cho mỗi bạn nhận phần bằng nhau.
c) Sản phẩm: Câu trả lời của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Có $9$ chiếc bánh pizza chia đều cho $4$ bạn. Viết số phần bánh mỗi bạn nhận được dưới dạng phân số và hỗn số.<br>- **HS:** Đọc đề và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính toán: $9 : 4 = \\frac{9}{4} = 2\\frac{1}{4}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Mỗi bạn nhận được $2$ chiếc bánh nguyên vẹn và $\\frac{1}{4}$ chiếc bánh nữa.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá tính thực tiễn của hỗn số trong việc hình dung số lượng đồ vật. | Mỗi bạn nhận được $\\frac{9}{4} = 2\\frac{1}{4}$ chiếc bánh pizza (nghĩa là $2$ chiếc nguyên và $\\frac{1}{4}$ chiếc nữa). |
"""
    },
    {
        "filename": "04_KHBD_Toan6_Bai25_PhepCongVaPhepTruPhanSo_Tiet56-57.md",
        "header": "TIẾT 56, 57 - BÀI 25: PHÉP CỘNG VÀ PHÉP TRỪ PHÂN SỐ\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 56, 57 - BÀI 25: PHÉP CỘNG VÀ PHÉP TRỪ PHÂN SỐ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Thực hiện được phép cộng và phép trừ hai phân số (cùng mẫu và khác mẫu).
- Nắm vững khái niệm hai phân số đối nhau và quy tắc chuyển phép trừ thành phép cộng với số đối: $\\frac{a}{b} - \\frac{c}{d} = \\frac{a}{b} + \\left(-\\frac{c}{d}\\right)$.
- Vận dụng tính chất giao hoán, kết hợp, cộng với số $0$ để tính toán một cách hợp lí.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quy đồng mẫu số và thực hiện các bước cộng, trừ phân số cẩn thận.
- Giao tiếp và hợp tác: Làm việc nhóm để tìm các cặp số đối nhau nhằm tính nhanh biểu thức gồm nhiều phân số.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích việc nhóm các phân số có cùng mẫu số hoặc có tổng bằng số nguyên để tính toán nhanh.
- Năng lực giải quyết vấn đề toán học: Áp dụng phép cộng, trừ phân số vào bài toán tính quãng đường, năng suất thực tế.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay để kiểm tra kết quả tính nhanh các biểu thức có nhiều phân số và dấu ngoặc.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Khai thác AI để kiểm tra lỗi sai thường gặp của học sinh trong việc quên đổi dấu tử số khi trừ phân số.***

## 3. Về phẩm chất
- Cẩn thận, kiên trì, không nhầm lẫn dấu khi cộng trừ số nguyên ở tử số.
- Có ý thức tự giác học tập và hỗ trợ bạn trong nhóm.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, máy chiếu, phiếu bài tập.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại quy tắc cộng hai phân số cùng mẫu ở tiểu học và đặt vấn đề với phân số có tử là số nguyên âm.
b) Nội dung: Tính: $\\frac{3}{7} + \\frac{2}{7}$ và dự đoán $\\frac{-3}{7} + \\frac{2}{7}$.
c) Sản phẩm: Kết quả miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu phép tính: $\\frac{3}{7} + \\frac{2}{7}$ và $\\frac{-3}{7} + \\frac{2}{7}$. Yêu cầu HS nêu cách thực hiện.<br>- **HS:** Đọc phép tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng cộng tử giữ nguyên mẫu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $\\frac{3}{7} + \\frac{2}{7} = \\frac{5}{7}$; $\\frac{-3}{7} + \\frac{2}{7} = \\frac{-3 + 2}{7} = \\frac{-1}{7}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định quy tắc cộng phân số cùng mẫu áp dụng hoàn toàn tương tự cho phân số có tử là số nguyên. | Muốn cộng hai phân số có cùng mẫu số, ta cộng các tử số và giữ nguyên mẫu số. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Phép cộng phân số và tính chất (35 phút)
a) Mục tiêu: HS nắm vững quy tắc cộng phân số cùng mẫu, khác mẫu và các tính chất giao hoán, kết hợp.
b) Nội dung: Xây dựng quy tắc cộng khác mẫu (quy đồng mẫu dương) và các tính chất.
c) Sản phẩm: Lời giải các ví dụ trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc: Muốn cộng hai phân số không cùng mẫu, ta viết chúng dưới dạng hai phân số có cùng một mẫu dương rồi cộng các tử và giữ nguyên mẫu chung.<br>- **HS:** Ghi nhận quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện tính: $\\frac{-5}{12} + \\frac{7}{18}$. Tìm MCNN của $12$ và $18$ là $36$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày: $\\frac{-5}{12} + \\frac{7}{18} = \\frac{-15}{36} + \\frac{14}{36} = \\frac{-1}{36}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại tính chất giao hoán $p + q = q + p$, tính chất kết hợp $(p + q) + r = p + (q + r)$ và cộng với $0$. | **1. Phép cộng phân số:**<br>- Cùng mẫu: $\\frac{a}{m} + \\frac{b}{m} = \\frac{a+b}{m}$ ($m > 0$).<br>- Khác mẫu: Quy đồng mẫu dương rồi cộng các tử, giữ nguyên mẫu chung.<br>- Tính chất: Giao hoán, kết hợp, cộng với số $0$:<br>$$A + B = B + A; \\quad (A + B) + C = A + (B + C); \\quad A + 0 = A$$ |

### Hoạt động 2.2: Số đối và phép trừ phân số (30 phút)
a) Mục tiêu: Nhận biết hai số đối nhau: tổng bằng $0$. Quy tắc phép trừ phân số.
b) Nội dung: Định nghĩa số đối $-\\frac{a}{b} = \\frac{-a}{b} = \\frac{a}{-b}$ và quy tắc trừ phân số.
c) Sản phẩm: Lời giải bài tập trừ phân số.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hai phân số gọi là đối nhau nếu tổng của chúng bằng $0$. Số đối của phân số $\\frac{a}{b}$ là gì? Muốn trừ phân số $\\frac{a}{b}$ cho $\\frac{c}{d}$ ta làm thế nào?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết số đối của $\\frac{2}{5}$ là $\\frac{-2}{5}$. Quy tắc: Ta cộng $\\frac{a}{b}$ với số đối của $\\frac{c}{d}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Thực hiện: $\\frac{1}{3} - \\frac{3}{4} = \\frac{1}{3} + \\left(\\frac{-3}{4}\\right) = \\frac{4}{12} + \\frac{-9}{12} = \\frac{-5}{12}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy tắc trừ phân số và quy tắc dấu ngoặc khi bỏ ngoặc. | **2. Phép trừ phân số:**<br>- Hai phân số đối nhau có tổng bằng $0$: $\\frac{a}{b} + \\left(-\\frac{a}{b}\\right) = 0$.<br>- Ta có: $-\\frac{a}{b} = \\frac{-a}{b} = \\frac{a}{-b}$.<br>- Quy tắc trừ: Muốn trừ phân số $\\frac{a}{b}$ cho phân số $\\frac{c}{d}$, ta cộng $\\frac{a}{b}$ với số đối của $\\frac{c}{d}$:<br>$$\\frac{a}{b} - \\frac{c}{d} = \\frac{a}{b} + \\left(-\\frac{c}{d}\\right)$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính hợp lí giá trị các biểu thức gồm nhiều phân số.
b) Nội dung: Bài 6.16, 6.17 SGK.
c) Sản phẩm: Lời giải trên bảng và vở ghi.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu tính giá trị biểu thức hợp lí:<br>$A = \\frac{-5}{9} + \\frac{8}{15} + \\frac{-4}{9} + \\frac{7}{15}$.<br>- **HS:** Nhận đề.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm các phân số cùng mẫu $9$ và cùng mẫu $15$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: $A = \\left(\\frac{-5}{9} + \\frac{-4}{9}\\right) + \\left(\\frac{8}{15} + \\frac{7}{15}\\right) = \\frac{-9}{9} + \\frac{15}{15} = (-1) + 1 = 0$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi việc vận dụng tính chất giao hoán, kết hợp một cách thông minh, chuẩn mực. | **Tính hợp lí:**<br>$$A = \\left(\\frac{-5}{9} + \\frac{-4}{9}\\right) + \\left(\\frac{8}{15} + \\frac{7}{15}\\right)$$<br>$$A = \\frac{-9}{9} + \\frac{15}{15} = (-1) + 1 = 0$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng phép cộng, trừ phân số vào bài toán phân chia công việc trong thực tế.
b) Nội dung: Bài toán hai vòi nước cùng chảy vào một bể.
c) Sản phẩm: Lời giải bài toán thực tế.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trong một giờ, vòi thứ nhất chảy được $\\frac{1}{3}$ bể, vòi thứ hai chảy được $\\frac{1}{4}$ bể. Hỏi trong một giờ cả hai vòi cùng chảy được bao nhiêu phần của bể?<br>- **HS:** Đọc đề và phân tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính tổng: $\\frac{1}{3} + \\frac{1}{4} = \\frac{4}{12} + \\frac{3}{12} = \\frac{7}{12}$ bể.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định kết quả và dặn dò HS làm bài tập về nhà trong SBT. | Trong một giờ cả hai vòi chảy được:<br>$$\\frac{1}{3} + \\frac{1}{4} = \\frac{7}{12} \\text{ (bể)}$$<br>Đáp số: $\\frac{7}{12}$ bể. |
"""
    },
    {
        "filename": "05_KHBD_Toan6_Bai26_PhepNhanVaPhepChiaPhanSo_Tiet58-59.md",
        "header": "TIẾT 58, 59 - BÀI 26: PHÉP NHÂN VÀ PHÉP CHIA PHÂN SỐ\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 58, 59 - BÀI 26: PHÉP NHÂN VÀ PHÉP CHIA PHÂN SỐ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Thực hiện được phép nhân hai phân số: Nhân các tử với nhau và nhân các mẫu với nhau.
- Nắm vững các tính chất của phép nhân phân số: Giao hoán, kết hợp, nhân với $1$, tính chất phân phối của phép nhân đối với phép cộng.
- Hiểu khái niệm phân số nghịch đảo và thực hiện phép chia phân số: Nhân với phân số nghịch đảo của số chia.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác tính toán rút gọn các thừa số chung trước khi nhân tử và mẫu để tối giản kết quả.
- Giao tiếp và hợp tác: Tương tác nhóm giải bài toán tính nhanh bằng tính chất phân phối.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phát hiện thừa số chung để áp dụng $a \\cdot b + a \\cdot c = a \\cdot (b + c)$.
- Năng lực giải quyết vấn đề toán học: Áp dụng phép nhân chia phân số tính diện tích hình học và chuyển đổi đơn vị thực tế.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay thực hiện tính phân số nghịch đảo bằng phím số mũ âm $x^{-1}$.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Sử dụng chatbot AI để tạo đề kiểm tra trắc nghiệm nhanh về phân số nghịch đảo và phép chia phân số.***

## 3. Về phẩm chất
- Cẩn thận, chính xác khi xác định dấu của tích (tích của chẵn các thừa số âm là dương, lẻ là âm).
- Trách nhiệm và tích cực đóng góp ý kiến trong hoạt động nhóm.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, bảng phụ, máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhớ lại quy tắc nhân hai phân số ở Tiểu học và đặt vấn đề nhân hai phân số có dấu âm.
b) Nội dung: Tính: $\\frac{2}{3} \\cdot \\frac{4}{5}$; dự đoán kết quả $\\frac{-2}{3} \\cdot \\frac{4}{5}$.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Nêu quy tắc nhân hai phân số đã học ở Tiểu học. Khi có số âm thì quy tắc có thay đổi không?<br>- **HS:** Đọc câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm: $\\frac{-2}{3} \\cdot \\frac{4}{5} = \\frac{(-2) \\cdot 4}{3 \\cdot 5} = \\frac{-8}{15}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định quy tắc nhân áp dụng hoàn toàn tương tự cho số nguyên. | Muốn nhân hai phân số, ta nhân các tử với nhau và nhân các mẫu với nhau. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Phép nhân phân số và tính chất (35 phút)
a) Mục tiêu: Nắm vững công thức nhân và các tính chất giao hoán, kết hợp, phân phối.
b) Nội dung: Công thức tổng quát $\\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}$ và các tính chất.
c) Sản phẩm: Lời giải các bài tập luyện tập trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc nhân phân số: $\\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}$ ($b, d \\neq 0$). Giới thiệu các tính chất tương tự như trong tập hợp số nguyên.<br>- **HS:** Tiếp thu kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng tính: $\\frac{-6}{35} \\cdot \\frac{-49}{54}$. Chú ý rút gọn trước khi nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: $\\frac{-6}{35} \\cdot \\frac{-49}{54} = \\frac{(-6) \\cdot (-49)}{35 \\cdot 54} = \\frac{(-1) \\cdot (-7)}{5 \\cdot 9} = \\frac{7}{45}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Cần rút gọn các thừa số chia hết ở tử và mẫu trước khi nhân để tránh tính toán cồng kềnh. | **1. Phép nhân phân số:**<br>- Quy tắc: $\\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}$ ($b, d \\neq 0$).<br>- Tính chất:<br>  + Giao hoán: $a \\cdot b = b \\cdot a$<br>  + Kết hợp: $(a \\cdot b) \\cdot c = a \\cdot (b \\cdot c)$<br>  + Nhân với số $1$: $a \\cdot 1 = a$<br>  + Phân phối đối với phép cộng: $a \\cdot (b + c) = a \\cdot b + a \\cdot c$ |

### Hoạt động 2.2: Phân số nghịch đảo và phép chia phân số (30 phút)
a) Mục tiêu: Hiểu khái niệm phân số nghịch đảo (tích bằng $1$) và quy tắc chia phân số.
b) Nội dung: Định nghĩa phân số nghịch đảo và quy tắc: $\\frac{a}{b} : \\frac{c}{d} = \\frac{a}{b} \\cdot \\frac{d}{c}$ ($c \\neq 0$).
c) Sản phẩm: Kết quả bài tập chia phân số trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hai phân số gọi là nghịch đảo của nhau nếu tích của chúng bằng $1$. Tìm phân số nghịch đảo của $\\frac{-3}{7}$ và của số nguyên $-5$. Nêu quy tắc chia hai phân số.<br>- **HS:** Đọc SGK và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân số nghịch đảo của $\\frac{-3}{7}$ là $\\frac{7}{-3} = \\frac{-7}{3}$. Nghịch đảo của $-5$ là $\\frac{-1}{5}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Thực hiện phép chia: $\\frac{-8}{15} : \\frac{4}{5} = \\frac{-8}{15} \\cdot \\frac{5}{4} = \\frac{-2}{3}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy tắc chia phân số: Nhân số bị chia với nghịch đảo của số chia. | **2. Phép chia phân số:**<br>- Phân số nghịch đảo: Hai phân số nghịch đảo nhau có tích bằng $1$. Phân số nghịch đảo của $\\frac{a}{b}$ ($a, b \\neq 0$) là $\\frac{b}{a}$.<br>- Quy tắc chia: Muốn chia một phân số cho một phân số khác $0$, ta nhân số bị chia với phân số nghịch đảo của số chia:<br>$$\\frac{a}{b} : \\frac{c}{d} = \\frac{a}{b} \\cdot \\frac{d}{c} = \\frac{a \\cdot d}{b \\cdot c} \\quad (b, c, d \\neq 0)$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính giá trị biểu thức phân số bằng cách áp dụng tính chất phân phối.
b) Nội dung: Bài tập tính nhanh giá trị biểu thức.
c) Sản phẩm: Bài giải chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Tính nhanh giá trị biểu thức:<br>$M = \\frac{7}{11} \\cdot \\frac{-3}{4} + \\frac{7}{11} \\cdot \\frac{-1}{4}$.<br>- **HS:** Quan sát thừa số chung.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt $\\frac{7}{11}$ ra ngoài làm thừa số chung.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày: $M = \\frac{7}{11} \\cdot \\left(\\frac{-3}{4} + \\frac{-1}{4}\\right) = \\frac{7}{11} \\cdot \\frac{-4}{4} = \\frac{7}{11} \\cdot (-1) = \\frac{-7}{11}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt phương pháp đặt thừa số chung để tính nhẩm nhanh chóng. | **Tính nhanh:**<br>$$M = \\frac{7}{11} \\cdot \\left(\\frac{-3}{4} + \\frac{-1}{4}\\right)$$<br>$$M = \\frac{7}{11} \\cdot (-1) = \\frac{-7}{11}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng phép nhân phân số tính diện tích hình chữ nhật trong thực tế.
b) Nội dung: Tính diện tích mảnh đất hình chữ nhật có chiều dài $\\frac{15}{2}\\text{ m}$ và chiều rộng $\\frac{16}{5}\\text{ m}$.
c) Sản phẩm: Lời giải bài toán thực tế trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu đề bài: Một mảnh đất hình chữ nhật có chiều dài $\\frac{15}{2}\\text{ m}$ và chiều rộng $\\frac{16}{5}\\text{ m}$. Tính diện tích mảnh đất.<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng công thức $S = a \\cdot b = \\frac{15}{2} \\cdot \\frac{16}{5}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $S = \\frac{15 \\cdot 16}{2 \\cdot 5} = 3 \\cdot 8 = 24\\text{ m}^2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi kết quả chính xác và giao bài tập về nhà. | Diện tích mảnh đất là:<br>$$S = \\frac{15}{2} \\cdot \\frac{16}{5} = 24\\text{ (m}^2\\text{)}$$<br>Đáp số: $24\\text{ m}^2$. |
"""
    },
    {
        "filename": "06_KHBD_Toan6_Bai27_HaiBaiToanVePhanSo_Tiet60-61.md",
        "header": "TIẾT 60, 61 - BÀI 27: HAI BÀI TOÁN VỀ PHÂN SỐ\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 60, 61 - BÀI 27: HAI BÀI TOÁN VỀ PHÂN SỐ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững quy tắc tìm giá trị phân số của một số cho trước: Muốn tìm $\\frac{m}{n}$ của số $a$, ta tính $a \\cdot \\frac{m}{n}$ ($m, n \\in \\mathbb{N}^*$).
- Nắm vững quy tắc tìm một số khi biết giá trị phân số của nó: Muốn tìm một số biết $\\frac{m}{n}$ của nó bằng $b$, ta tính $b : \\frac{m}{n}$.
- Phân biệt rõ hai bài toán thuận và nghịch để áp dụng đúng phép nhân hoặc phép chia.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Đọc hiểu và phân tích đề bài, xác định đúng đại lượng đã biết và đại lượng cần tìm.
- Giao tiếp và hợp tác: Tương tác nhóm phản biện lựa chọn phép tính nhân hay chia.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Thiết lập mối quan hệ giữa tổng thể và bộ phận thông qua tỉ số phân số.
- Năng lực mô hình hoá toán học: Chuyển các bài toán thực tế (giảm giá, lãi suất, tỉ lệ phần trăm dinh dưỡng) về bài toán tìm phân số.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay giải quyết các bài toán về tỉ số phân số với số liệu tiền tệ thực tế lớn.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Sử dụng công cụ AI mô phỏng bài toán kinh tế gia đình và tính toán số tiền tiết kiệm hàng tháng.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn thận trong việc tính toán tiền bạc, số lượng thực tế.
- Ý thức tiết kiệm và quản lý tài chính cá nhân phù hợp với lứa tuổi học sinh.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, bảng phụ tóm tắt hai bài toán, máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt tình huống thực tế về tìm phân số của một số để khơi gợi hứng thú học tập.
b) Nội dung: Một rổ cam có $24$ quả, mẹ lấy đi $\\frac{2}{3}$ số cam để vắt nước. Hỏi mẹ đã lấy bao nhiêu quả cam?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế về $24$ quả cam. Làm thế nào để tìm $\\frac{2}{3}$ của $24$ quả cam?<br>- **HS:** Đọc đề và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm: Chia $3$ phần bằng nhau mỗi phần $8$ quả, lấy $2$ phần là $16$ quả.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Ta tính $24 \\cdot \\frac{2}{3} = 16$ quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và giới thiệu: Đây chính là bài toán tìm giá trị phân số của một số cho trước. | Để tìm $\\frac{2}{3}$ của $24$, ta lấy $24 \\cdot \\frac{2}{3} = 16$ (quả). |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Bài toán 1 - Tìm giá trị phân số của một số cho trước (35 phút)
a) Mục tiêu: HS nắm vững quy tắc và công thức: Tìm $\\frac{m}{n}$ của số $a$ cho trước ta tính $a \\cdot \\frac{m}{n}$.
b) Nội dung: Phát biểu quy tắc và giải các ví dụ thực tế.
c) Sản phẩm: Lời giải bài Luyện tập 1 trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc: Muốn tìm $\\frac{m}{n}$ của số $a$ cho trước, ta tính $a \\cdot \\frac{m}{n}$ ($m \\in \\mathbb{Z}, n \\in \\mathbb{N}^*$). Yêu cầu HS tính $\\frac{3}{5}$ của $120\\text{ kg}$.<br>- **HS:** Tiếp nhận công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: $120 \\cdot \\frac{3}{5} = \\frac{360}{5} = 72\\text{ kg}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy tắc bài toán 1: "Biết số ban đầu, tìm giá trị phân số $\\rightarrow$ Dùng phép NHÂN". | **1. Tìm giá trị phân số của một số cho trước:**<br>- Quy tắc: Muốn tìm $\\frac{m}{n}$ của số $a$ cho trước, ta tính $a \\cdot \\frac{m}{n}$ ($m \\in \\mathbb{Z}, n \\in \\mathbb{N}^*$).<br>- Ví dụ: Tìm $\\frac{3}{5}$ của $120\\text{ kg}$:<br>$$120 \\cdot \\frac{3}{5} = 72\\text{ (kg)}$$ |

### Hoạt động 2.2: Bài toán 2 - Tìm một số khi biết giá trị phân số của nó (30 phút)
a) Mục tiêu: Nắm vững quy tắc và công thức: Tìm một số biết $\\frac{m}{n}$ của nó bằng $b$, ta tính $b : \\frac{m}{n}$.
b) Nội dung: Xây dựng quy tắc thông qua phép toán ngược lại của phép nhân.
c) Sản phẩm: Lời giải bài Luyện tập 2 trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt vấn đề: Tìm một số biết $\\frac{2}{3}$ của nó bằng $16$. Gọi số đó là $x$, ta có $x \\cdot \\frac{2}{3} = 16$. Vậy tìm $x$ như thế nào?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ta tính $x = 16 : \\frac{2}{3} = 16 \\cdot \\frac{3}{2} = 24$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát biểu quy tắc bài toán 2.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt quy tắc bài toán 2: "Biết giá trị của phân số, tìm số ban đầu $\\rightarrow$ Dùng phép CHIA". Phân biệt rành mạch giữa Nhân và Chia. | **2. Tìm một số khi biết giá trị phân số của nó:**<br>- Quy tắc: Muốn tìm một số biết $\\frac{m}{n}$ của nó bằng $b$, ta tính $b : \\frac{m}{n}$ ($m, n \\in \\mathbb{N}^*$).<br>- Ví dụ: Tìm một số biết $\\frac{2}{7}$ của nó bằng $14$:<br>$$14 : \\frac{2}{7} = 14 \\cdot \\frac{7}{2} = 49$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Luyện tập phân biệt và giải các bài toán thực tế áp dụng hai bài toán về phân số.
b) Nội dung: Bài 6.34, 6.35 SGK trang 21.
c) Sản phẩm: Bài làm chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đưa bài toán: Một bác nông dân thu hoạch được $1200\\text{ kg}$ thóc. Bác bán đi $\\frac{2}{5}$ số thóc, số còn lại đem ủng hộ quỹ khuyến học $\\frac{1}{3}$. Tính số thóc bác nông dân còn lại.<br>- **HS:** Đọc đề và phân tích từng bước.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính số thóc bán đi, số thóc còn lại sau khi bán, rồi tính số thóc ủng hộ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: Số thóc bán là $1200 \\cdot \\frac{2}{5} = 480\\text{ kg}$. Còn lại: $1200 - 480 = 720\\text{ kg}$. Số thóc ủng hộ: $720 \\cdot \\frac{1}{3} = 240\\text{ kg}$. Còn lại: $720 - 240 = 480\\text{ kg}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và chốt lời giải chuẩn xác. | **Bài giải:**<br>- Số thóc bán đi là:<br>$$1200 \\cdot \\frac{2}{5} = 480\\text{ (kg)}$$<br>- Số thóc còn lại sau khi bán là:<br>$$1200 - 480 = 720\\text{ (kg)}$$<br>- Số thóc ủng hộ là:<br>$$720 \\cdot \\frac{1}{3} = 240\\text{ (kg)}$$<br>- Bác nông dân còn lại là:<br>$$720 - 240 = 480\\text{ (kg)}$$<br>Đáp số: $480\\text{ kg}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng kiến thức tính chiều cao của một cái cây qua bóng nắng trên mặt đất.
b) Nội dung: Bài toán thực tế về tỉ lệ chiều dài bóng nắng và chiều cao vật thể.
c) Sản phẩm: Bài làm trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tại một thời điểm, bóng của một cột cờ dài $6\\text{ m}$, biết chiều dài bóng bằng $\\frac{3}{4}$ chiều cao cột cờ. Tính chiều cao cột cờ.<br>- **HS:** Xác định bài toán 2.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chiều cao cột cờ là: $6 : \\frac{3}{4} = 6 \\cdot \\frac{4}{3} = 8\\text{ m}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát biểu kết quả trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, củng cố ý nghĩa thực tiễn to lớn của phân số. | Chiều cao của cột cờ là:<br>$$6 : \\frac{3}{4} = 6 \\cdot \\frac{4}{3} = 8\\text{ (m)}$$<br>Đáp số: $8\\text{ m}$. |
"""
    },
    {
        "filename": "07_KHBD_Toan6_LuyenTapChung_Tiet62-63.md",
        "header": "TIẾT 62, 63 - LUYỆN TẬP CHUNG (TRANG 21)\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 62, 63 - LUYỆN TẬP CHUNG (TRANG 21)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Rèn luyện kỹ năng thực hiện thành thạo cả 4 phép tính: cộng, trừ, nhân, chia phân số.
- Vận dụng linh hoạt thứ tự thực hiện phép tính và các tính chất giao hoán, kết hợp, phân phối để tính giá trị biểu thức.
- Giải quyết thành thạo các bài toán thực tế liên quan đến hai bài toán về phân số.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức các phép tính và sơ đồ nhận biết hai bài toán về phân số.
- Giao tiếp và hợp tác: Hợp tác nhóm nhỏ cùng thảo luận lập kế hoạch giải bài toán thực tế có nhiều bước tính.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phân tích cấu trúc biểu thức để chọn thứ tự thực hiện hoặc nhóm hợp lí nhất.
- Năng lực giải quyết vấn đề toán học: Mô hình hóa các dữ kiện thực tế bằng sơ đồ đoạn thẳng hoặc phân số biểu thị.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay kiểm tra kết quả các biểu thức phức tạp có chứa phân số và lũy thừa.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Ứng dụng trợ lý AI giải thích các bước tính toán và phát hiện lỗi sai trong quá trình rút gọn biểu thức phân số.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, cẩn trọng khi thực hiện nhiều phép tính liên hoàn.
- Ý thức tự giác, vượt khó trong giải quyết các bài toán vận dụng cao.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 62-63 (vector 300 DPI), máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khởi động tinh thần học tập qua trò chơi tiếp sức tính nhanh các phép tính phân số.
b) Nội dung: 4 đội thi tiếp sức điền kết quả các phép tính phân số cơ bản lên bảng.
c) Sản phẩm: Bảng kết quả của các đội thi.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chia lớp thành 4 đội tiếp sức, mỗi đội điền kết quả của 3 phép tính phân số.<br>- **HS:** Đại diện các đội chuẩn bị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lần lượt từng thành viên lên điền đáp số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cả lớp đối chiếu kết quả chéo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương đội nhanh và chính xác nhất, dẫn dắt vào bài luyện tập chung. | Các phép tính cơ bản cộng, trừ, nhân, chia phân số được thực hiện chính xác và tối giản. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (20 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ các phép tính phân số và phân biệt rành mạch hai bài toán về phân số.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 62-63; hệ thống các công thức tính toán.

![Sơ đồ tư duy Luyện tập chung Tiết 62-63](khbd-ill:mindmap-toan6-tiet62-63)

c) Sản phẩm: Sơ đồ tư duy và bảng công thức trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy Tiết 62-63. Yêu cầu HS nêu rõ: Phép cộng trừ quy đồng mẫu; Phép nhân nhân tử nhân mẫu; Phép chia nhân nghịch đảo; Bài toán 1 lấy $a \\cdot \\frac{m}{n}$; Bài toán 2 lấy $b : \\frac{m}{n}$.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo cặp đôi nhắc lại các quy tắc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS xung phong lên bảng vẽ nhánh sơ đồ tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa kiến thức trên sơ đồ. | **Hệ thống 4 phép tính và 2 bài toán phân số:**<br>1. Cộng, trừ: Đưa về cùng mẫu dương rồi cộng/trừ tử số.<br>2. Nhân: $\\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{a \\cdot c}{b \\cdot d}$.<br>3. Chia: $\\frac{a}{b} : \\frac{c}{d} = \\frac{a}{b} \\cdot \\frac{d}{c}$.<br>4. Bài toán 1: Tìm $\\frac{m}{n}$ của $a \\Rightarrow$ Tính $a \\cdot \\frac{m}{n}$.<br>5. Bài toán 2: Tìm số biết $\\frac{m}{n}$ của nó bằng $b \\Rightarrow$ Tính $b : \\frac{m}{n}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Giải thành thạo các dạng bài toán tính biểu thức phức hợp và bài toán lời văn thực tế.
b) Nội dung: Bài tập tính giá trị biểu thức và bài toán phân chia công việc.
c) Sản phẩm: Lời giải chi tiết trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài tập:<br>  Bài 1: Tính giá trị biểu thức: $B = \\left(\\frac{3}{4} - \\frac{5}{6}\\right) : \\frac{7}{12} + \\frac{1}{7}$.<br>  Bài 2: Một lớp học có $40$ học sinh gồm 3 loại: giỏi, khá, trung bình. Số học sinh giỏi chiếm $\\frac{1}{4}$ số học sinh cả lớp. Số học sinh khá bằng $\\frac{3}{5}$ số học sinh còn lại. Tính số học sinh trung bình.<br>- **HS:** Nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br>- Bài 1: $\\frac{3}{4} - \\frac{5}{6} = \\frac{9-10}{12} = \\frac{-1}{12}$. Biểu thức $B = \\frac{-1}{12} \\cdot \\frac{12}{7} + \\frac{1}{7} = \\frac{-1}{7} + \\frac{1}{7} = 0$.<br>- Bài 2: Số HS giỏi là $40 \\cdot \\frac{1}{4} = 10$ (HS). Số HS còn lại là $40 - 10 = 30$ (HS). Số HS khá là $30 \\cdot \\frac{3}{5} = 18$ (HS). Số HS trung bình là $30 - 18 = 12$ (HS).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao cách giải rõ ràng, mạch lạc của học sinh. | **Lời giải chi tiết:**<br>**Bài 1:**<br>$$B = \\left(\\frac{9}{12} - \\frac{10}{12}\\right) : \\frac{7}{12} + \\frac{1}{7}$$<br>$$B = \\frac{-1}{12} \\cdot \\frac{12}{7} + \\frac{1}{7} = \\frac{-1}{7} + \\frac{1}{7} = 0$$<br>**Bài 2:**<br>- Số học sinh giỏi là: $40 \\cdot \\frac{1}{4} = 10$ (học sinh).<br>- Số học sinh còn lại là: $40 - 10 = 30$ (học sinh).<br>- Số học sinh khá là: $30 \\cdot \\frac{3}{5} = 18$ (học sinh).<br>- Số học sinh trung bình là: $30 - 18 = 12$ (học sinh).<br>Đáp số: $12$ học sinh trung bình. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Vận dụng phân số vào bài toán lập kế hoạch tài chính cá nhân.
b) Nội dung: Bài toán quản lý chi tiêu tiền mừng tuổi đầu năm của học sinh.
c) Sản phẩm: Bảng kế hoạch chi tiêu trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** An nhận được $1\\,200\\,000$ đồng tiền mừng tuổi. An dành $\\frac{1}{2}$ để mua sách vở, $\\frac{1}{4}$ để nuôi heo đất tiết kiệm và số còn lại để giúp đỡ các bạn có hoàn cảnh khó khăn. Hỏi số tiền An giúp đỡ bạn là bao nhiêu?<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính phân số chỉ số tiền giúp bạn: $1 - \\frac{1}{2} - \\frac{1}{4} = \\frac{1}{4}$. Số tiền là: $1\\,200\\,000 \\cdot \\frac{1}{4} = 300\\,000$ đồng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giáo dục phẩm chất nhân ái và kỹ năng quản lý tài chính cá nhân. | Số tiền An dành giúp đỡ bạn là:<br>$$1\\,200\\,000 \\cdot \\left(1 - \\frac{1}{2} - \\frac{1}{4}\\right) = 300\\,000\\text{ (đồng)}$$<br>Đáp số: $300\\,000$ đồng. |
"""
    },
    {
        "filename": "08_KHBD_Toan6_BaiTapCuoiChuong6_Tiet64-65.md",
        "header": "TIẾT 64, 65 - BÀI TẬP CUỐI CHƯƠNG VI (TRANG 24)\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 64, 65 - BÀI TẬP CUỐI CHƯƠNG VI (TRANG 24)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết và hệ thống hóa toàn bộ kiến thức Chương VI: Khái niệm phân số, phân số bằng nhau, so sánh phân số, các phép tính với phân số, hỗn số dương và hai bài toán về phân số.
- Vận dụng kiến thức toàn chương để giải quyết các bài tập tổng hợp và bài toán thực tế.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa toàn bộ kiến thức chương qua sơ đồ tư duy tổng hợp; phát hiện những phần kiến thức mình còn chưa vững để tự bổ sung.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải các bài toán tổng hợp trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa quy tắc, lựa chọn công thức giải toán chính xác và ngắn gọn nhất.
- Năng lực giải quyết vấn đề toán học: Phân tích và xử lý các bài toán phối hợp nhiều phép tính và chuyển đổi đơn vị đo lường.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay kiểm tra kết quả tính toán của toàn bộ đề bài tập ôn tập chương.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Khai thác AI tổng hợp các dạng lỗi sai kinh điển của học sinh THCS khi học chương phân số và đề xuất giải pháp khắc phục.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật và tác phong khoa học trong học tập.
- Nâng cao ý thức tự học và tự đánh giá năng lực của bản thân.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 64-65 (vector 300 DPI), tivi/máy chiếu, đề ôn tập.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập nhanh các công thức trọng tâm qua trò chơi trắc nghiệm "Vòng quay may mắn".
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm kiến thức cốt lõi chương VI.
c) Sản phẩm: Lựa chọn đáp án của học sinh trên bảng con.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu hỏi trắc nghiệm vòng quay may mắn.<br>- **HS:** Chuẩn bị bảng con ghi đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ đáp án sau hiệu lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giải thích ngắn gọn lý do chọn đáp án.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và dẫn vào bài ôn tập tổng kết chương VI. | Bảng đáp án trắc nghiệm chuẩn xác của học sinh. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (20 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ cấu trúc kiến thức Chương VI bằng Sơ đồ tư duy tổng hợp 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 64-65; hoàn thiện bức tranh tổng thể về phân số.

![Sơ đồ tư duy Bài tập cuối chương VI Tiết 64-65](khbd-ill:mindmap-toan6-tiet64-65)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy tổng thể Chương VI. Hướng dẫn HS hệ thống theo 4 nhánh lớn: 1. Khái niệm & Phân số bằng nhau; 2. So sánh & Hỗn số; 3. Bốn phép tính phân số; 4. Hai bài toán về phân số.<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành các chỗ trống trong phiếu tóm tắt lý thuyết.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS đứng tại chỗ trình bày tổng quan cấu trúc chương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại các lưu ý quan trọng: Điều kiện mẫu khác $0$, đổi mẫu âm thành mẫu dương, các tính chất phân phối giúp tính nhanh. | **Tổng kết lý thuyết Chương VI:**<br>- Phân số: $\\frac{a}{b}$ ($a, b \\in \\mathbb{Z}, b \\neq 0$).<br>- Bằng nhau: $a \\cdot d = b \\cdot c$.<br>- Tính chất: $\\frac{a}{b} = \\frac{a \\cdot m}{b \\cdot m} = \\frac{a : n}{b : n}$.<br>- So sánh: Đưa về cùng mẫu dương.<br>- Bốn phép tính: Cộng, Trừ, Nhân, Chia.<br>- Hai bài toán phân số: Tìm giá trị phân số (Nhân); Tìm số khi biết giá trị phân số (Chia). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Luyện tập toàn diện các bài tập trắc nghiệm và tự luận cuối chương trong SGK.
b) Nội dung: Giải Bài 6.36, 6.38, 6.40, 6.42 SGK trang 24, 25.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài toán tổng hợp:<br>  Bài 1: Tính hợp lí: $P = \\left(\\frac{-3}{8}\\right) \\cdot \\frac{1}{6} + \\left(\\frac{-3}{8}\\right) \\cdot \\frac{5}{6}$.<br>  Bài 2: Tìm $x$ biết: $\\frac{3}{5} \\cdot x + \\frac{1}{2} = \\frac{1}{5}$.<br>- **HS:** Nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện giải bài tập độc lập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng:<br>- Bài 1: $P = \\left(\\frac{-3}{8}\\right) \\cdot \\left(\\frac{1}{6} + \\frac{5}{6}\\right) = \\left(\\frac{-3}{8}\\right) \\cdot 1 = \\frac{-3}{8}$.<br>- Bài 2: $\\frac{3}{5} \\cdot x = \\frac{1}{5} - \\frac{1}{2} = \\frac{2-5}{10} = \\frac{-3}{10}$. Suy ra $x = \\frac{-3}{10} : \\frac{3}{5} = \\frac{-3}{10} \\cdot \\frac{5}{3} = \\frac{-1}{2}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa: Kết luận rõ $x = \\frac{-1}{2}$, tuyệt đối không kết luận tập nghiệm. | **Lời giải bài tập tổng hợp:**<br>**Bài 1:**<br>$$P = \\left(\\frac{-3}{8}\\right) \\cdot \\left(\\frac{1}{6} + \\frac{5}{6}\\right) = \\frac{-3}{8} \\cdot 1 = \\frac{-3}{8}$$<br>**Bài 2:**<br>$$\\frac{3}{5} \\cdot x + \\frac{1}{2} = \\frac{1}{5}$$<br>$$\\frac{3}{5} \\cdot x = \\frac{1}{5} - \\frac{1}{2} = \\frac{-3}{10}$$<br>$$x = \\frac{-3}{10} : \\frac{3}{5} = \\frac{-3}{10} \\cdot \\frac{5}{3} = \\frac{-1}{2}$$<br>Vậy giá trị của $x$ cần tìm là $\\frac{-1}{2}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Vận dụng kiến thức tổng hợp giải bài toán thực tế về thành phần dinh dưỡng của thực phẩm.
b) Nội dung: Bài 6.43 SGK: Trong $100\\text{ g}$ đậu đen nấu chín có chứa $8\\text{ g}$ protein. Tính tỉ lệ phần trăm protein trong đậu đen và lượng protein trong $250\\text{ g}$ đậu đen.
c) Sản phẩm: Lời giải hoàn thiện trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu đề bài 6.43. Yêu cầu tính lượng protein trong $250\\text{ g}$ đậu đen.<br>- **HS:** Đọc đề và phân tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tỉ lệ protein là $\\frac{8}{100} = \\frac{2}{25}$. Lượng protein trong $250\\text{ g}$ đậu đen là $250 \\cdot \\frac{2}{25} = 20\\text{ g}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá ý nghĩa thực tiễn của bài toán đối với chế độ ăn uống khoa học hàng ngày. Dặn dò ôn tập chuẩn bị bước sang Chương VII: Số thập phân. | Lượng protein trong $250\\text{ g}$ đậu đen là:<br>$$250 \\cdot \\frac{8}{100} = 20\\text{ (g)}$$<br>Đáp số: $20\\text{ g}$ protein. |
"""
    }
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print("Hoàn tất tạo 8 KHBD Chương VI: Phân số (Tiết 51 - 65)!")
