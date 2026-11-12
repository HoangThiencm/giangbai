# -*- coding: utf-8 -*-
"""
Script tạo 9 tệp Markdown Kế hoạch bài dạy Toán 6 (Tuần 9 - 12)
Chuẩn CV 5512 V2.1 • Trợ lý Sư phạm Hoàng Thiên
"""

import os, sys

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\TEMP\02.11_Toan6"
os.makedirs(TEMP_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. BÀI 01: LUYỆN TẬP CHUNG CHƯƠNG II (TIẾT 25)
# ------------------------------------------------------------------------------
f01 = """Tiết 25 - LUYỆN TẬP CHUNG (TRANG 54 - 55)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và khắc sâu các khái niệm: Ước chung, Ước chung lớn nhất (ƯCLN), Bội chung, Bội chung nhỏ nhất (BCNN) của hai hay nhiều số tự nhiên.
- Vận dụng thành thạo thuật toán tìm ƯCLN và BCNN bằng cách phân tích các số ra thừa số nguyên tố.
- Vận dụng ƯCLN để rút gọn phân số về phân số tối giản; vận dụng BCNN để quy đồng mẫu các phân số.
- Vận dụng ƯCLN và BCNN vào giải các bài toán thực tiễn đời sống (chia tổ, chia phần thưởng, bài toán chu kỳ lặp lại).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác hệ thống kiến thức ƯCLN và BCNN qua sơ đồ tư duy, chủ động hoàn thành các bài tập phân hóa.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải trong nhóm, biết lắng nghe và phản biện ý kiến của bạn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận lựa chọn tìm ƯCLN hay BCNN dựa trên dữ kiện đề bài toán thực tế.
- Năng lực giải quyết vấn đề toán học: Vận dụng linh hoạt thuật toán phân tích thừa số nguyên tố để giải các bài toán số học.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng máy tính cầm tay phím FACT để phân tích số ra thừa số nguyên tố và dùng hàm GCD, LCM để kiểm tra nhanh kết quả ƯCLN, BCNN.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***9.D1.1: HS ứng dụng trợ lý học tập AI để tra cứu các tình huống thực tiễn ứng dụng của BCNN trong thiên văn và đời sống.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác trong tính toán số học.
- Ý thức tự giác, vượt khó trong giải toán có lời văn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, hình ảnh Sơ đồ tư duy Mindmap ƯCLN & BCNN, máy chiếu, bảng phụ.
2. Học sinh: SGK Toán 6, vở bài tập, máy tính cầm tay, bút dạ bảng nhóm.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy và phản xạ nhanh về cách phân biệt ƯCLN và BCNN qua câu hỏi trắc nghiệm nhanh.
b) Nội dung: Trả lời 3 câu hỏi trắc nghiệm ngắn trên màn chiếu.
c) Sản phẩm: Bảng chọn đáp án của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 3 câu hỏi nhanh:<br>  1. Muốn rút gọn phân số về phân số tối giản, ta chia cả tử và mẫu cho số nào?<br>  2. Muốn tìm mẫu số chung để quy đồng mẫu các phân số, ta thường tìm số nào của các mẫu?<br>  3. Cho $a = 2^2 \\cdot 3$ và $b = 2 \\cdot 3^2$, hãy tính ƯCLN($a, b$) và BCNN($a, b$).<br>- **HS:** Chuẩn bị bảng con trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ bảng kết quả.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ giải thích cách chọn thừa số chung với số mũ nhỏ nhất/lớn nhất.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ phản xạ và dẫn dắt vào bài luyện tập. | **Câu hỏi khởi động:**<br>1. Chia cho ƯCLN của tử và mẫu.<br>2. Tìm BCNN của các mẫu số.<br>3. ƯCLN($a, b$) = $2 \\cdot 3 = 6$; BCNN($a, b$) = $2^2 \\cdot 3^2 = 36$. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức bằng Sơ đồ tư duy (10 phút)
a) Mục tiêu: Hệ thống hóa quy tắc tìm ƯCLN, BCNN và các ứng dụng cốt lõi thông qua sơ đồ tư duy trực quan; tích hợp chỉ báo AI 9.D1.1.
b) Nội dung: GV trình chiếu và hướng dẫn HS phân tích Sơ đồ tư duy Mindmap Luyện tập chung Chương II.

![Sơ đồ tư duy Luyện tập chung Chương II](khbd-ill:mindmap-tiet25)

c) Sản phẩm: Bảng so sánh ƯCLN và BCNN trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy Mindmap Luyện tập chung Chương II gồm 3 nhánh lớn:<br>  1. Ước chung lớn nhất (ƯCLN) & Rút gọn phân số.<br>  2. Bội chung nhỏ nhất (BCNN) & Quy đồng mẫu số.<br>  3. Ứng dụng thực tế đời sống (chia tổ, chu kỳ lặp lại).<br>- Yêu cầu HS quan sát sơ đồ và so sánh điểm giống/khác nhau giữa quy tắc tìm ƯCLN và BCNN.<br>- ***Tích hợp AI (9.D1.1): GV cho học sinh xem gợi ý của trợ lý AI giải thích thuật toán Euclid tìm ƯCLN của hai số lớn cực nhanh bằng phép chia có dư liên tiếp.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát sơ đồ tư duy, thảo luận cặp đôi và ghi chép vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết minh lại 3 nhánh chính của sơ đồ tư duy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại bảng so sánh và chuyển sang phần giải bài tập rèn kỹ năng. | **So sánh quy tắc tìm ƯCLN và BCNN:**<br>- **Bước 1:** Phân tích các số ra thừa số nguyên tố.<br>- **Bước 2 (Chọn thừa số):**<br>  + ƯCLN: Chỉ chọn các thừa số nguyên tố *chung*.<br>  + BCNN: Chọn các thừa số nguyên tố *chung và riêng*.<br>- **Bước 3 (Lập tích):**<br>  + ƯCLN: Mỗi thừa số lấy với số mũ *nhỏ nhất*.<br>  + BCNN: Mỗi thừa số lấy với số mũ *lớn nhất*. |

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)
a) Mục tiêu: Rèn kỹ năng rút gọn phân số, quy đồng mẫu số và giải bài toán thực tế; tích hợp chỉ báo NLS 5.3.TC1a.
b) Nội dung: Giải Bài 2.53, Bài 2.54 và Bài 2.56 (SGK trang 55).
c) Sản phẩm: Lời giải chi tiết các bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 3 bài tập lên bảng:<br>  **Bài 2.53:** Rút gọn các phân số sau về phân số tối giản: $\\frac{90}{126}; \\frac{144}{360}$.<br>  **Bài 2.54:** Quy đồng mẫu các phân số sau: $\\frac{5}{12}$ và $\\frac{7}{30}$.<br>  **Bài 2.56:** Hai bạn An và Bình cùng học một trường nhưng ở hai lớp khác nhau. An cứ 10 ngày lại trực nhật một lần, Bình cứ 12 ngày lại trực nhật một lần. Lần đầu tiên cả hai bạn cùng trực nhật vào một ngày. Hỏi sau ít nhất bao nhiêu ngày thì hai bạn lại cùng trực nhật?<br>- ***Tích hợp NLS (5.3.TC1a): HS sử dụng máy tính cầm tay bấm phím FACT để kiểm tra phân tích thừa số nguyên tố của 90, 126, 144, 360.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cá nhân giải bài vào vở. 3 HS đại diện lên bảng.<br>- **GV:** Quan sát, hướng dẫn học sinh nhận diện bài 2.56 là bài toán tìm BCNN(10, 12).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS trên bảng trình bày. Lớp nhận xét đối chiếu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa lời giải từng bài toán. | **Bài 2.53 (SGK trang 55):**<br>- Ta có: $90 = 2 \\cdot 3^2 \\cdot 5$; $126 = 2 \\cdot 3^2 \\cdot 7$.<br>  $\\Rightarrow$ ƯCLN(90, 126) = $2 \\cdot 3^2 = 18$.<br>  Do đó: $\\frac{90}{126} = \\frac{90 : 18}{126 : 18} = \\frac{5}{7}$.<br>- Ta có: $144 = 2^4 \\cdot 3^2$; $360 = 2^3 \\cdot 3^2 \\cdot 5$.<br>  $\\Rightarrow$ ƯCLN(144, 360) = $2^3 \\cdot 3^2 = 72$.<br>  Do đó: $\\frac{144}{360} = \\frac{144 : 72}{360 : 72} = \\frac{2}{5}$.<br><br>**Bài 2.54 (SGK trang 55):**<br>- Tìm mẫu chung: BCNN(12, 30).<br>  $12 = 2^2 \\cdot 3$; $30 = 2 \\cdot 3 \\cdot 5 \\Rightarrow$ BCNN(12, 30) = $2^2 \\cdot 3 \\cdot 5 = 60$.<br>- Quy đồng:<br>  $\\frac{5}{12} = \\frac{5 \\cdot 5}{12 \\cdot 5} = \\frac{25}{60}$; $\\frac{7}{30} = \\frac{7 \\cdot 2}{30 \\cdot 2} = \\frac{14}{60}$.<br><br>**Bài 2.56 (SGK trang 55):**<br>- Gọi số ngày ít nhất để hai bạn lại cùng trực nhật là $a$ (ngày, $a \\in \\mathbb{N}^*$).<br>- Vì $a$ chia hết cho 10 và $a$ chia hết cho 12, mà $a$ nhỏ nhất nên $a = \\text{BCNN}(10, 12)$.<br>- Ta có: $10 = 2 \\cdot 5$; $12 = 2^2 \\cdot 3$.<br>  $\\Rightarrow a = \\text{BCNN}(10, 12) = 2^2 \\cdot 3 \\cdot 5 = 60$.<br>Vậy sau ít nhất 60 ngày thì hai bạn lại cùng trực nhật. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng ƯCLN vào bài toán thực tế chia tổ học sinh trong chuyến dã ngoại.
b) Nội dung: Giải bài toán chia 24 bạn nam và 30 bạn nữ thành các tổ đều nhau. Hướng dẫn tự học.
c) Sản phẩm: Lời giải bài toán thực tế trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán: Lớp 6A có 24 bạn nam và 30 bạn nữ. Trong buổi sinh hoạt ngoài trời, cô giáo muốn chia lớp thành các tổ sao cho số nam và số nữ ở mỗi tổ đều bằng nhau. Hỏi cô giáo có thể chia được nhiều nhất thành bao nhiêu tổ? Khi đó mỗi tổ có bao nhiêu bạn nam, bao nhiêu bạn nữ?<br>- **HS:** Nhận nhiệm vụ, nhận diện bài toán tìm ƯCLN.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Số tổ nhiều nhất là ƯCLN(24, 30) = 6 tổ.<br>  Mỗi tổ có: $24 : 6 = 4$ nam và $30 : 6 = 5$ nữ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ nêu đáp số, lớp nhận xét.<br><br>**+ Bước 4: Kết luận, nhận định & Dặn dò**<br>- **GV:** Khen ngợi tinh thần học tập tích cực của lớp. | **Bài toán chia tổ:**<br>- Số tổ nhiều nhất là $x = \\text{ƯCLN}(24, 30)$.<br>- Ta có: $24 = 2^3 \\cdot 3$; $30 = 2 \\cdot 3 \\cdot 5 \\Rightarrow \\text{ƯCLN}(24, 30) = 2 \\cdot 3 = 6$.<br>Vậy có thể chia nhiều nhất thành 6 tổ.<br>Khi đó mỗi tổ có: $24 : 6 = 4$ bạn nam và $30 : 6 = 5$ bạn nữ.<br><br>**Dặn dò tự học tại nhà:**<br>1. Ôn lại quy tắc tìm ƯCLN và BCNN theo Sơ đồ tư duy.<br>2. Làm Bài 2.55 SGK trang 55.<br>3. Chuẩn bị cho Tiết 26: Bài tập cuối chương II. |
"""

with open(os.path.join(TEMP_DIR, "01_LuyenTapChung_Chuong2_Tiet25.md"), 'w', encoding='utf-8') as f:
    f.write(f01)
print(" -> Đã tạo: 01_LuyenTapChung_Chuong2_Tiet25.md")

# ------------------------------------------------------------------------------
# 2. BÀI 02: BÀI TẬP CUỐI CHƯƠNG II (TIẾT 26)
# ------------------------------------------------------------------------------
f02 = """Tiết 26 - BÀI TẬP CUỐI CHƯƠNG II (TRANG 56)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập và hệ thống hóa toàn bộ các mạch kiến thức cốt lõi của Chương II: Tính chất chia hết trong tập hợp số tự nhiên:
  + Quan hệ chia hết và tính chất chia hết của một tổng.
  + Dấu hiệu chia hết cho 2, cho 5, cho 3, cho 9.
  + Khái niệm số nguyên tố, hợp số và phân tích một số ra thừa số nguyên tố.
  + Khái niệm, cách tìm ƯCLN và BCNN của hai hay nhiều số tự nhiên.
- Rèn luyện kỹ năng giải các câu hỏi trắc nghiệm khách quan và giải các bài tập tự luận tổng hợp cuối chương.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác hệ thống hóa kiến thức toàn chương qua sơ đồ tư duy Mindmap, nhận diện các dạng toán trọng tâm.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp lập luận loại trừ phương án sai trong bài tập trắc nghiệm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Vận dụng tính chất chia hết và dấu hiệu chia hết để giải thích tính chia hết mà không cần tính giá trị biểu thức.
- Năng lực giải quyết vấn đề toán học: Phối hợp linh hoạt phân tích thừa số nguyên tố để giải quyết bài toán số học tổng hợp.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng máy tính cầm tay phím phân tích thừa số nguyên tố FACT và phím chia hết để kiểm tra nhanh kết quả bài toán trắc nghiệm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***9.D1.1: HS ứng dụng trợ lý học tập AI để tạo ngân hàng câu hỏi trắc nghiệm rèn luyện phản xạ về số nguyên tố và dấu hiệu chia hết.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng trong làm bài kiểm tra trắc nghiệm và tự luận.
- Tự giác chuẩn bị bài trước khi đến lớp.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, hình ảnh Sơ đồ tư duy Mindmap Tổng kết Chương II, máy chiếu, phiếu học tập trắc nghiệm.
2. Học sinh: SGK Toán 6, vở bài tập, máy tính cầm tay, bút dạ.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt không khí học tập sôi nổi và rèn luyện kỹ năng làm bài trắc nghiệm khách quan.
b) Nội dung: Giải 3 câu hỏi trắc nghiệm trong SGK trang 56 (Bài 2.57, 2.58, 2.59).
c) Sản phẩm: Bảng chọn đáp án của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 3 câu hỏi trắc nghiệm SGK trang 56:<br>  **Câu 2.57:** Khẳng định nào sau đây là sai?<br>  A. 15 chia hết cho 5; B. 24 chia hết cho 8; C. 36 chia hết cho 9; D. 42 không chia hết cho 7.<br>  **Câu 2.58:** Khẳng định nào sau đây là đúng?<br>  A. Tổng $12 + 15$ chia hết cho 2; B. Hiệu $45 - 18$ chia hết cho 9; C. Tổng $21 + 35$ chia hết cho 5; D. Hiệu $60 - 25$ chia hết cho 6.<br>  **Câu 2.59:** Số nào sau đây là số nguyên tố: 15; 29; 33; 49?<br>- **HS:** Chuẩn bị bảng con trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ bảng đáp án ngay khi có hiệu lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ giải thích vì sao chọn đáp án D (câu 2.57), B (câu 2.58), 29 (câu 2.59).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ phản xạ và dẫn dắt vào bài ôn tập tổng kết chương. | **Đáp án trắc nghiệm:**<br>- **Câu 2.57: Chọn D** (vì $42 : 7 = 6$ chia hết nên khẳng định 42 không chia hết cho 7 là sai).<br>- **Câu 2.58: Chọn B** (vì 45 và 18 đều chia hết cho 9 nên $45 - 18$ chia hết cho 9).<br>- **Câu 2.59: Chọn 29** (vì 29 chỉ có đúng 2 ước là 1 và 29). |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức bằng Sơ đồ tư duy (10 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức Chương II bằng sơ đồ tư duy trực quan, giúp học sinh nắm chắc mạch logic của chương; tích hợp chỉ báo AI 9.D1.1.
b) Nội dung: GV trình chiếu và hướng dẫn HS phân tích Sơ đồ tư duy Mindmap Tổng kết Chương II.

![Sơ đồ tư duy Tổng kết Chương II](khbd-ill:mindmap-tiet26)

c) Sản phẩm: Sơ đồ tư duy và bảng tóm tắt kiến thức Chương II trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tổng kết Chương II gồm 3 nhánh lớn:<br>  1. Quan hệ & Dấu hiệu chia hết.<br>  2. Số nguyên tố & Hợp số.<br>  3. Ước chung & Bội chung (ƯCLN, BCNN).<br>- Yêu cầu HS đọc sơ đồ và nhắc lại các dấu hiệu chia hết cho 2, 3, 5, 9.<br>- ***Tích hợp AI (9.D1.1): GV cho học sinh xem gợi ý của trợ lý AI phân tích mẹo ghi nhớ: chia hết cho 2 và 5 nhìn vào chữ số tận cùng; chia hết cho 3 và 9 nhìn vào tổng các chữ số.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát sơ đồ tư duy, hệ thống lại kiến thức và ghi chép vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết minh lại 3 nhánh chính của sơ đồ tư duy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại mạch kiến thức và chuyển sang luyện giải bài tập tự luận. | **Hệ thống kiến thức Chương II (Mindmap):**<br>1. **Chia hết & Dấu hiệu:**<br>  - $a$ chia hết cho $m$ và $b$ chia hết cho $m \\Rightarrow a + b$ chia hết cho $m$.<br>  - Tận cùng là 0, 2, 4, 6, 8 thì chia hết cho 2.<br>  - Tận cùng là 0 hoặc 5 thì chia hết cho 5.<br>  - Tổng các chữ số chia hết cho 3 (hoặc 9) thì chia hết cho 3 (hoặc 9).<br>2. **Số nguyên tố & Hợp số:**<br>  - Số nguyên tố nhỏ nhất và chẵn duy nhất là 2.<br>  - Phân tích số tự nhiên ra thừa số nguyên tố.<br>3. **ƯCLN & BCNN:**<br>  - ƯCLN lấy thừa số chung với số mũ nhỏ nhất.<br>  - BCNN lấy thừa số chung và riêng với số mũ lớn nhất. |

### 2. Hoạt động 2.2: Giải quyết bài tập tự luận trọng tâm (22 phút)
a) Mục tiêu: Rèn luyện kỹ năng phân tích thừa số nguyên tố, tìm ƯCLN, BCNN và xét tính chia hết; tích hợp chỉ báo NLS 5.3.TC1a.
b) Nội dung: Giải Bài 2.60, Bài 2.61 và Bài 2.62 (SGK trang 56).
c) Sản phẩm: Lời giải hoàn chỉnh các bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 3 bài tập tự luận lên bảng:<br>  **Bài 2.60:** Biết số $123*$ chia hết cho 2 và 5. Hãy tìm chữ số thay cho $*$.<br>  **Bài 2.61:** Phân tích các số sau ra thừa số nguyên tố rồi tìm ƯCLN và BCNN của chúng: $a = 60$ và $b = 140$.<br>  **Bài 2.62:** Bác Lan có một số quả cam khoảng từ 100 đến 150 quả. Nếu bác xếp vào các đĩa, mỗi đĩa 6 quả, 8 quả hoặc 10 quả thì đều vừa đủ. Hỏi bác Lan có bao nhiêu quả cam?<br>- ***Tích hợp NLS (5.3.TC1a): HS sử dụng máy tính cầm tay bấm phím FACT để kiểm tra phân tích của 60 và 140.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cá nhân giải bài vào vở. Ba HS lên bảng thực hiện.<br>- **GV:** Theo dõi, hướng dẫn học sinh nhận diện Bài 2.62 là bài toán tìm bội chung trong một khoảng giá trị.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS trên bảng trình bày. Lớp nhận xét từng bước giải.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa phương pháp giải bài toán tìm bội chung có điều kiện kèm theo. | **Bài 2.60 (SGK trang 56):**<br>- Vì số $123*$ chia hết cho cả 2 và 5 nên chữ số tận cùng phải là 0.<br>- Vậy $* = 0$ và số đó là $1230$.<br><br>**Bài 2.61 (SGK trang 56):**<br>- Ta có: $60 = 2^2 \\cdot 3 \\cdot 5$; $140 = 2^2 \\cdot 5 \\cdot 7$.<br>- Thừa số chung là 2 và 5 $\\Rightarrow$ ƯCLN(60, 140) = $2^2 \\cdot 5 = 20$.<br>- Thừa số chung và riêng là 2, 3, 5, 7 $\\Rightarrow$ BCNN(60, 140) = $2^2 \\cdot 3 \\cdot 5 \\cdot 7 = 420$.<br><br>**Bài 2.62 (SGK trang 56):**<br>- Gọi số quả cam bác Lan có là $x$ (quả, $100 \\le x \\le 150, x \\in \\mathbb{N}^*$).<br>- Vì xếp mỗi đĩa 6 quả, 8 quả hoặc 10 quả đều vừa đủ nên $x$ chia hết cho 6, 8 và 10.<br>- Suy ra $x \\in \\text{BC}(6, 8, 10)$.<br>- Ta có: $6 = 2 \\cdot 3$; $8 = 2^3$; $10 = 2 \\cdot 5$.<br>  $\\Rightarrow \\text{BCNN}(6, 8, 10) = 2^3 \\cdot 3 \\cdot 5 = 120$.<br>- Các bội chung của 6, 8, 10 là bội của 120: $\\text{BC}(6, 8, 10) = \\{0; 120; 240; \\dots\\}$.<br>- Vì $100 \\le x \\le 150$ nên $x = 120$ (thỏa mãn).<br>Vậy bác Lan có 120 quả cam. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức chia hết vào bài toán mật mã số học đơn giản.
b) Nội dung: Trò chơi tìm số may mắn chia hết cho cả 3 và 5 nhưng không chia hết cho 2. Dặn dò tự học.
c) Sản phẩm: Câu trả lời của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu đố: Tôi là một số tự nhiên có hai chữ số, chia hết cho cả 3 và 5 nhưng lại không chia hết cho 2. Chữ số hàng chục của tôi lớn hơn 5. Tôi là số nào?<br>- **HS:** Tiếp nhận câu đố, suy luận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chia hết cho 5 nhưng không chia hết cho 2 nên chữ số tận cùng là 5. Chữ số hàng chục lớn hơn 5 (có thể là 6, 7, 8, 9).<br>  Các số có thể: 65, 75, 85, 95.<br>  Số chia hết cho 3: $7 + 5 = 12$ chia hết cho 3. Vậy số đó là 75.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ trả lời là 75.<br><br>**+ Bước 4: Kết luận, nhận định & Dặn dò**<br>- **GV:** Khen ngợi học sinh có tư duy lập luận số học sắc bén. | **Đáp án câu đố:**<br>- Số đó là 75.<br><br>**Dặn dò tự học tại nhà:**<br>1. Ôn tập toàn bộ lý thuyết Chương I và Chương II theo Sơ đồ tư duy.<br>2. Chuẩn bị cho Tiết 27, 28: Ôn tập kiểm tra đánh giá giữa Học kì I (Số học). |
"""

with open(os.path.join(TEMP_DIR, "02_BaiTapCuoiChuong2_Tiet26.md"), 'w', encoding='utf-8') as f:
    f.write(f02)
print(" -> Đã tạo: 02_BaiTapCuoiChuong2_Tiet26.md")

# ------------------------------------------------------------------------------
# 3. BÀI 03: ÔN TẬP GIỮA HỌC KÌ I - SỐ HỌC (TIẾT 27, 28)
# ------------------------------------------------------------------------------
f03 = """Tiết 27, 28 - ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (SỐ HỌC)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức trọng tâm phần Số học nửa đầu Học kì I:
  + Chương I (Số tự nhiên): Tập hợp $\\mathbb{N}$ và $\\mathbb{N}^*$; Các phép tính cộng, trừ, nhân, chia, nâng lên lũy thừa; Thứ tự thực hiện các phép tính trong biểu thức chứa dấu ngoặc.
  + Chương II (Tính chất chia hết): Quan hệ chia hết; Tính chất chia hết của một tổng; Dấu hiệu chia hết cho 2, 5, 3, 9; Số nguyên tố, hợp số; Phân tích ra thừa số nguyên tố; Ước chung, Bội chung, ƯCLN và BCNN.
- Rèn luyện kỹ năng tính toán thành thạo, tìm $x$, giải bài toán thực tế và chuẩn bị tâm thế vững vàng cho bài kiểm tra giữa kì I.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác hệ thống hóa kiến thức số học giữa kì I qua sơ đồ tư duy Mindmap, nhận diện các dạng bài hay nhầm lẫn.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải ngắn gọn, mạch lạc trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phân tích biểu thức để áp dụng tính chất giao hoán, kết hợp, phân phối tính nhanh một cách hợp lý.
- Năng lực giải quyết vấn đề toán học: Chuyển đổi các bài toán thực tiễn chia tổ, xếp hàng, lịch chu kỳ thành bài toán tìm ƯCLN và BCNN.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng thành thạo máy tính cầm tay phím phân tích thừa số nguyên tố FACT, phím tính lũy thừa và hàm GCD, LCM để kiểm tra kết quả tính toán.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***9.D1.1: HS phối hợp sử dụng trợ lý học tập AI để tra cứu bảng tổng hợp các lỗi sai trừ điểm phổ biến khi làm bài thi giữa kì môn Toán 6.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, kỷ luật, tự kiểm tra lại bài làm bằng máy tính cầm tay trước khi nộp bài.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, hình ảnh Sơ đồ tư duy Mindmap Ôn tập Số học giữa HKI, máy chiếu, đề cương ôn tập.
2. Học sinh: SGK Toán 6, vở ghi, máy tính cầm tay, bút dạ bảng nhóm.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (10 phút)
a) Mục tiêu: Kích hoạt tư duy và ôn lại thứ tự thực hiện phép tính qua trò chơi tiếp sức nhanh.
b) Nội dung: Hai đội thi đua tính nhanh giá trị của 2 biểu thức trên bảng.
c) Sản phẩm: Lời giải trên bảng của hai đội.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chia lớp làm 2 đội thi tiếp sức tính giá trị biểu thức:<br>  Đội 1: $A = 3^2 \\cdot 5 - 2^3 \\cdot 4 + 10^0$.<br>  Đội 2: $B = 120 : [54 - (50 - 2^3)]$.<br>- **HS:** Mỗi đội cử 4 bạn tham gia tiếp sức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lần lượt từng bạn lên bảng thực hiện một phép tính.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cả lớp đối chiếu thứ tự thực hiện phép tính: tính lũy thừa trước, rồi nhân chia, rồi cộng trừ; trong ngoặc tròn trước, rồi ngoặc vuông.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, tuyên dương đội nhanh và chính xác. | **Lời giải khởi động:**<br>- Đội 1: $A = 9 \\cdot 5 - 8 \\cdot 4 + 1 = 45 - 32 + 1 = 14$.<br>- Đội 2: $B = 120 : [54 - (50 - 8)] = 120 : [54 - 42] = 120 : 12 = 10$. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (65 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức bằng Sơ đồ tư duy (Tiết 27) (20 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức Chương I và Chương II bằng Sơ đồ tư duy trực quan; tích hợp chỉ báo AI 9.D1.1.
b) Nội dung: GV trình chiếu và hướng dẫn HS phân tích Sơ đồ tư duy Mindmap Ôn tập Số học giữa HKI.

![Sơ đồ tư duy Ôn tập Số học giữa Học kì I](khbd-ill:mindmap-tiet27-28)

c) Sản phẩm: Bảng công thức và sơ đồ tư duy được khắc sâu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Ôn tập Số học giữa HKI gồm 3 nhánh lớn:<br>  1. Chương I: Số tự nhiên (Phép tính, lũy thừa, thứ tự thực hiện).<br>  2. Chương II: Chia hết & Dấu hiệu chia hết.<br>  3. Chương II: Số nguyên tố, ƯCLN & BCNN.<br>- Yêu cầu HS đọc sơ đồ và nhắc lại các công thức nhân, chia hai lũy thừa cùng cơ số.<br>- ***Tích hợp AI (9.D1.1): GV chiếu bảng cảnh báo do AI tổng hợp về các lỗi sai học sinh hay mắc phải: (1) Tính $a^m \\cdot a^n = a^{m \\cdot n}$ (sai, đúng phải là cộng số mũ); (2) Quên tính lũy thừa trước khi nhân chia; (3) Nhầm lẫn giữa tìm ƯCLN và BCNN.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát sơ đồ tư duy, hệ thống lại kiến thức và ghi chép vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ nêu rõ từng quy tắc lũy thừa và thứ tự thực hiện phép tính.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc và chuyển sang luyện giải các dạng bài tập trọng tâm. | **Hệ thống kiến thức cốt lõi (Mindmap):**<br>1. **Công thức lũy thừa:**<br>  $a^m \\cdot a^n = a^{m+n}$; $a^m : a^n = a^{m-n}$ ($a \\ne 0, m \\ge n$); $a^0 = 1$ ($a \\ne 0$).<br>2. **Thứ tự thực hiện phép tính:**<br>  - Biểu thức không có ngoặc: Lũy thừa $\\rightarrow$ Nhân, chia $\\rightarrow$ Cộng, trừ.<br>  - Biểu thức có dấu ngoặc: $( ) \\rightarrow [ ] \\rightarrow \\{ \\}$.<br>3. **Tính chất chia hết & Dấu hiệu:**<br>  - Chia hết cho 2 (tận cùng chẵn), cho 5 (tận cùng 0 hoặc 5).<br>  - Chia hết cho 3, cho 9 (tổng chữ số chia hết cho 3, cho 9).<br>4. **ƯCLN và BCNN:**<br>  - ƯCLN: Thừa số chung với số mũ nhỏ nhất.<br>  - BCNN: Thừa số chung và riêng với số mũ lớn nhất. |

### 2. Hoạt động 2.2: Luyện giải các dạng bài tập trọng tâm (Tiết 28) (45 phút)
a) Mục tiêu: Rèn luyện kỹ năng thực hiện phép tính hợp lý, tìm số tự nhiên $x$ và giải bài toán thực tế; tích hợp chỉ báo NLS 5.3.TC1a.
b) Nội dung: Giải 4 dạng bài tập điển hình bám sát ma trận đề kiểm tra giữa kì I.
c) Sản phẩm: Lời giải hoàn chỉnh các bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 4 bài tập lên bảng:<br>  **Dạng 1 (Tính hợp lý):**<br>  a) $A = 27 \\cdot 36 + 27 \\cdot 64 - 700$;<br>  b) $B = 35 \\cdot 48 + 35 \\cdot 53 - 35$.<br>  **Dạng 2 (Thứ tự phép tính):**<br>  $C = 2026 - [100 - (7 - 4)^2] \\cdot 10$.<br>  **Dạng 3 (Tìm $x$):**<br>  a) $2x - 138 = 2^3 \\cdot 3^2$;<br>  b) $120 : (x - 3) = 24$.<br>  **Dạng 4 (Bài toán thực tế):**<br>  Học sinh khối 6 của một trường khi xếp hàng 12, hàng 15, hàng 18 đều vừa đủ. Biết số học sinh trong khoảng từ 300 đến 400 em. Tính số học sinh khối 6 của trường đó.<br>- ***Tích hợp NLS (5.3.TC1a): HS sử dụng máy tính cầm tay bấm phím FACT để tìm BCNN(12, 15, 18) và bấm kiểm tra lại các phép tính hợp lý.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cá nhân làm bài vào vở. 4 HS đại diện lên bảng thực hiện.<br>- **GV:** Theo dõi, hướng dẫn học sinh còn yếu trong việc đặt thừa số chung ở Dạng 1.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS trên bảng trình bày chi tiết từng bước. Cả lớp đổi vở chấm chéo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa lời giải và thang điểm từng bài. | **Dạng 1 (Tính hợp lý):**<br>a) $A = 27 \\cdot (36 + 64) - 700 = 27 \\cdot 100 - 700 = 2700 - 700 = 2000$.<br>b) $B = 35 \\cdot (48 + 53 - 1) = 35 \\cdot 100 = 3500$.<br><br>**Dạng 2 (Thứ tự phép tính):**<br>$C = 2026 - [100 - 3^2] \\cdot 10 = 2026 - [100 - 9] \\cdot 10$<br>$C = 2026 - 91 \\cdot 10 = 2026 - 910 = 1116$.<br><br>**Dạng 3 (Tìm $x$):**<br>a) $2x - 138 = 8 \\cdot 9 = 72 \\Rightarrow 2x = 72 + 138 = 210 \\Rightarrow x = 105$.<br>Vậy $x = 105$.<br>b) $120 : (x - 3) = 24 \\Rightarrow x - 3 = 120 : 24 = 5 \\Rightarrow x = 8$.<br>Vậy $x = 8$.<br><br>**Dạng 4 (Bài toán thực tế):**<br>- Gọi số học sinh khối 6 là $a$ (học sinh, $300 \\le a \\le 400, a \\in \\mathbb{N}^*$).<br>- Vì xếp hàng 12, 15, 18 đều vừa đủ nên $a$ chia hết cho 12, 15 và 18.<br>- Suy ra $a \\in \\text{BC}(12, 15, 18)$.<br>- Ta có: $12 = 2^2 \\cdot 3$; $15 = 3 \\cdot 5$; $18 = 2 \\cdot 3^2$.<br>  $\\Rightarrow \\text{BCNN}(12, 15, 18) = 2^2 \\cdot 3^2 \\cdot 5 = 180$.<br>- Do đó $a \\in \\text{BC}(12, 15, 18) = \\{0; 180; 360; 540; \\dots\\}$.<br>- Vì $300 \\le a \\le 400$ nên $a = 360$ (thỏa mãn).<br>Vậy khối 6 có 360 học sinh. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (15 phút)
a) Mục tiêu: Hướng dẫn học sinh kỹ thuật phân bổ thời gian và chiến lược làm bài kiểm tra đánh giá giữa kì I.
b) Nội dung: Phân tích ma trận đề thi và dặn dò tự học.
c) Sản phẩm: Kế hoạch tự ôn tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chiến lược làm bài thi giữa HKI môn Toán 6:<br>  1. Phân bổ thời gian: 15 phút cho trắc nghiệm (12 câu), 75 phút cho tự luận.<br>  2. Làm bài tự luận theo thứ tự: Thực hiện phép tính $\\rightarrow$ Tìm $x \\rightarrow$ Bài toán thực tế $\\rightarrow$ Câu nâng cao.<br>  3. Luôn thử lại nghiệm $x$ và phép tính bằng máy tính cầm tay.<br>- **HS:** Lắng nghe, ghi chú vào sổ tay.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt các câu hỏi còn băn khoăn về quy cách trình bày bài thi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- GV giải đáp thắc mắc của học sinh.<br><br>**+ Bước 4: Kết luận, nhận định & Dặn dò**<br>- **GV:** Dặn dò HS chuẩn bị đầy đủ máy tính, bút mực, thước kẻ cho Tiết 29 (Kiểm tra đánh giá giữa HKI). | **Chiến lược làm bài thi giữa HKI:**<br>1. Đọc kỹ đề bài, gạch chân các từ khóa quan trọng.<br>2. Trình bày bài tự luận rõ ràng, viết các bước tính toán liền mạch từng dòng.<br>3. Ở bài toán tìm $x$: Luôn kết luận "Vậy $x = ...$".<br><br>**Dặn dò tự học tại nhà:**<br>- Ôn tập kỹ theo Sơ đồ tư duy Mindmap.<br>- Tự giải đề cương ôn tập giữa kì I. |
"""

with open(os.path.join(TEMP_DIR, "03_OnTapGiuaHK1_SoHoc_Tiet27-28.md"), 'w', encoding='utf-8') as f:
    f.write(f03)
print(" -> Đã tạo: 03_OnTapGiuaHK1_SoHoc_Tiet27-28.md")

print(">>> ĐÃ TẠO XONG 3 FILE ĐẦU TIÊN! <<<")
