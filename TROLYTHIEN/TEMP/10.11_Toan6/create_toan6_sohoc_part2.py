# -*- coding: utf-8 -*-
"""
Script sinh tiếp các tệp KHBD Số học 6 (Bài 03 đến Bài 08):
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Toan6"
os.makedirs(OUT_DIR, exist_ok=True)

# 03. Bài 17: Phép chia hết. Ước và bội của một số nguyên (Tiết 41)
md_03 = """Tiết 41 - BÀI 17: PHÉP CHIA HẾT. ƯỚC VÀ BỘI CỦA MỘT SỐ NGUYÊN
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được định nghĩa phép chia hết trong tập hợp số nguyên $\\mathbb{Z}$: Cho $a, b \\in \\mathbb{Z}$ ($b \\ne 0$). Nếu có số nguyên $q$ sao cho $a = b \\cdot q$ thì ta nói $a$ chia hết cho $b$, kí hiệu $a$ chia hết cho $b$.
- Nắm được quy tắc dấu của thương: Thương của hai số nguyên cùng dấu luôn mang dấu dương (+); thương của hai số nguyên khác dấu luôn mang dấu âm (-).
- Hiểu và xác định được ước và bội của một số nguyên: Nếu $a$ chia hết cho $b$ thì $a$ là bội của $b$, $b$ là ước của $a$.
- Nhận biết tính chất: Nếu $b$ là ước của $a$ thì $-b$ cũng là ước của $a$. Do đó, các ước của một số nguyên luôn đi theo từng cặp số đối nhau.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đọc hiểu SGK để rút ra định nghĩa ước và bội trong tập hợp $\\mathbb{Z}$, đối chiếu với tập hợp số tự nhiên $\\mathbb{N}$.
- Giao tiếp và hợp tác: Tự tin trao đổi cách liệt kê đầy đủ cả ước dương và ước âm của một số nguyên.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận xác định dấu của thương và tìm các ước nguyên của một số.
- Năng lực giải quyết vấn đề toán học: Vận dụng phép chia hết giải bài toán tìm số nguyên thỏa mãn điều kiện.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng máy tính cầm tay phím phân số và chia nguyên để kiểm tra quan hệ chia hết giữa hai số nguyên có dấu.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để tạo bảng đối chiếu tập ước của một số trong tập N và trong tập Z, từ đó khắc sâu tính chất số đối.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, không bỏ sót các ước nguyên âm.
- Tinh thần vượt khó, chủ động trong học tập.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, bảng phụ quy tắc dấu phép chia, máy chiếu.
2. Học sinh: SGK Toán 6, vở ghi bài, máy tính cầm tay, bảng con.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy về mối liên hệ giữa phép nhân và phép chia qua câu đố số nguyên.
b) Nội dung: Tìm số nguyên $x$ biết: $(-3) \\cdot x = 12$ và $5 \\cdot x = -35$.
c) Sản phẩm: Bảng kết quả của học sinh: $x = -4$ và $x = -7$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt câu hỏi: Số nguyên $x$ nào thỏa mãn $(-3) \\cdot x = 12$?<br>- **HS:** Nhẩm nhanh và ghi bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: $x = 12 : (-3) = -4$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ giải thích vì sao $x = -4$ (vì âm nhân âm ra dương).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định kết quả và dẫn dắt vào bài mới: Phép chia hết trong tập số nguyên. | **Khởi động:**<br>- Vì $(-3) \\cdot (-4) = 12$ nên $12 : (-3) = -4$.<br>- Phép chia trong $\\mathbb{Z}$ tuân theo quy tắc dấu tương tự phép nhân. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (25 phút)
### Hoạt động 2.1: Phép chia hết trong Z và Quy tắc dấu (13 phút)
a) Mục tiêu: Nắm vững định nghĩa phép chia hết và quy tắc dấu của thương.
b) Nội dung: Đọc mục 1 SGK trang 73; thực hiện Luyện tập 1.
c) Sản phẩm: Định nghĩa phép chia hết, bảng dấu thương và kết quả Luyện tập 1.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu định nghĩa phép chia hết trong $\\mathbb{Z}$ và bảng quy tắc dấu:<br>  $(+) : (+) = (+)$; $(-) : (-) = (+)$<br>  $(+) : (-) = (-)$; $(-) : (+) = (-)$<br>- **GV:** Yêu cầu HS tính Luyện tập 1:<br>  a) $(-48) : (-6)$;<br>  b) $56 : (-7)$;<br>  c) $(-125) : 5$.<br>- **HS:** Tiếp nhận quy tắc và làm bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS lên bảng tính: a) $8$; b) $-8$; c) $-25$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc: Cùng dấu ra dương, khác dấu ra âm. | **1. Phép chia hết trong Z:**<br>- Cho $a, b \\in \\mathbb{Z}$ ($b \\ne 0$). Nếu có $q \\in \\mathbb{Z}$ sao cho $a = b \\cdot q$ thì $a$ chia hết cho $b$ ($a : b = q$).<br>- Quy tắc dấu:<br>+ Cùng dấu: thương mang dấu (+).<br>+ Khác dấu: thương mang dấu (-).<br>Ví dụ:<br>$(-36) : (-9) = 4$.<br>$(-45) : 5 = -9$. |

### Hoạt động 2.2: Ước và Bội của một số nguyên (12 phút)
a) Mục tiêu: Biết tìm tập hợp các ước và các bội của một số nguyên bất kì.
b) Nội dung: Đọc mục 2 SGK trang 74; làm Luyện tập 2.
c) Sản phẩm: Tập hợp ước $\\text{Ư}(a)$ và bội $\\text{B}(b)$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa:<br>  Khi $a$ chia hết cho $b$, ta nói $a$ là bội của $b$ và $b$ là ước của $a$.<br>- **GV:** Hướng dẫn: Nếu $b$ là ước của $a$ thì $-b$ cũng là ước của $a$.<br>  Hãy tìm tất cả các ước của $6$ và tìm 4 bội của $-5$.<br>- **HS:** Làm bài vào vở nháp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Liệt kê các ước dương rồi lấy thêm các số đối.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng viết: $\\text{Ư}(6) = \\{1; -1; 2; -2; 3; -3; 6; -6\\}$.<br>- 1 HS viết: 4 bội của $-5$ là $0; -5; 5; 10$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Số $0$ là bội của mọi số nguyên khác $0$, nhưng số $0$ không là ước của bất kì số nào. | **2. Ước và bội của một số nguyên:**<br>- Khi $a$ chia hết cho $b$, $a$ là bội của $b$, $b$ là ước của $a$.<br>- Chú ý:<br>+ Các ước của số nguyên luôn tồn tại theo từng cặp số đối nhau.<br>+ $\\text{Ư}(6) = \\{\\pm 1; \\pm 2; \\pm 3; \\pm 6\\}$.<br>+ Các bội của $-5$ là: $0; \\pm 5; \\pm 10; \\pm 15; ...$ |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
a) Mục tiêu: Củng cố kĩ năng chia số nguyên và tìm ước của số nguyên âm.
b) Nội dung: Giải bài tập 3.39, 3.40 SGK trang 74.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS giải bài 3.39 và 3.40 SGK.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở ghi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa lời giải. | **Bài 3.39 (SGK tr.74):**<br>a) $(-63) : 9 = -7$.<br>b) $(-24) : (-8) = 3$.<br><br>**Bài 3.40 (SGK tr.74):**<br>Các ước của $-8$ là: $\\text{Ư}(-8) = \\{\\pm 1; \\pm 2; \\pm 4; \\pm 8\\}$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
a) Mục tiêu: Vận dụng ước của số nguyên để tìm số nguyên $x$ thỏa mãn điều kiện chia hết.
b) Nội dung: Tìm số nguyên $x$ sao cho $6$ chia hết cho $(x - 1)$.
c) Sản phẩm: Lời giải bài toán tìm $x$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán: Tìm $x \\in \\mathbb{Z}$ để $6$ chia hết cho $(x - 1)$.<br>- **HS:** Lập luận: $x - 1 \\in \\text{Ư}(6)$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lập bảng giá trị $x - 1 \\in \\{\\pm 1; \\pm 2; \\pm 3; \\pm 6\\}$ để tìm $x$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ nêu các giá trị $x = 2; 0; 3; -1; 4; -2; 7; -5$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương tư duy logic của học sinh, giao nhiệm vụ chuẩn bị tiết Luyện tập chung. | **Vận dụng:**<br>Vì $6$ chia hết cho $(x - 1)$ nên $x - 1 \\in \\text{Ư}(6) = \\{\\pm 1; \\pm 2; \\pm 3; \\pm 6\\}$.<br>Các giá trị $x$ thỏa mãn là:<br>$x \\in \\{-5; -2; -1; 0; 2; 3; 4; 7\\}$. |
"""

# 04. Luyện tập chung Tiết 42
md_04 = """Tiết 42 - LUYỆN TẬP CHUNG (TRANG 75)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và rèn luyện kĩ năng thực hiện phép nhân và phép chia số nguyên; vận dụng thành thạo quy tắc dấu của tích và thương.
- Vận dụng linh hoạt các tính chất giao hoán, kết hợp, phân phối của phép nhân để tính hợp lí giá trị các biểu thức phức hợp.
- Củng cố khái niệm ước và bội của một số nguyên; giải quyết thành thạo các bài toán tìm thành phần chưa biết $x$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát sơ đồ tư duy hệ thống hóa phép nhân chia và bội ước trong $\\mathbb{Z}$, chủ động hoàn thành các bài tập phân hóa.
- Giao tiếp và hợp tác: Tự tin phản biện cách nhóm các số hạng, thừa số thuận tiện nhất trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh quy tắc dấu của phép nhân và phép chia; lập luận tìm tập ước của số nguyên âm.
- Năng lực giải quyết vấn đề toán học: Biến đổi biểu thức đại số và giải các bài toán thực tế.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng máy tính cầm tay phím STO/Ans để gán giá trị và kiểm tra nhanh kết quả tính giá trị biểu thức nhiều biến.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng chatbot AI để tạo các bài toán vui đố mẹo về số nguyên âm và chia hết nhằm kích thích tư duy toán học.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, ngăn nắp, chính xác trong từng bước lập luận.
- Tinh thần trách nhiệm và trung thực trong học tập.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Luyện tập chung Tiết 42 (vector 300 DPI), tivi/máy chiếu, phiếu bài tập.
2. Học sinh: SGK Toán 6, vở bài tập, máy tính cầm tay, bảng con.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy và sự tập trung thông qua bảng quy tắc dấu nhanh của tích và thương.
b) Nội dung: Điền dấu thích hợp (+ hoặc -) vào các ô trống trên màn chiếu.
c) Sản phẩm: Bảng điền dấu của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu bảng quy tắc dấu:<br>  $(+) \\cdot (-) = [?]$; $(-) \\cdot (-) = [?]$; $(-) : (+) = [?]$; $(-) : (-) = [?]$.<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm nhanh và giơ bảng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cả lớp đồng thanh đọc: Âm, Dương, Âm, Dương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu: \"Cùng dấu thì dương, khác dấu thì âm\", bắt đầu vào tiết luyện tập. | **Đáp án khởi động:**<br>$(+) \\cdot (-) = (-)$<br>$(-) \\cdot (-) = (+)$<br>$(-) : (+) = (-)$<br>$(-) : (-) = (+)$ |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Tổng kết toàn diện các quy tắc phép nhân, phép chia hết và bội ước số nguyên qua Sơ đồ tư duy.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 42; nhắc lại các kiến thức trọng tâm.

![Sơ đồ tư duy Luyện tập chung Tiết 42](khbd-ill:mindmap-toan6-tiet42)

c) Sản phẩm: Bản ghi nhớ hệ thống kiến thức trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Tiết 42 lên màn hình. Yêu cầu HS nêu:<br>  + Các tính chất của phép nhân số nguyên.<br>  + Cách tìm tập hợp các ước của một số nguyên.<br>- **HS:** Quan sát sơ đồ tư duy và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trình bày tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa các bước giải bài toán tính nhanh. | **Kiến thức cốt lõi:**<br>1. Nhân chia số nguyên: Quy tắc cùng dấu, khác dấu.<br>2. Tính chất phân phối: $a \\cdot (b + c) = a \\cdot b + a \\cdot c$.<br>3. Bội và ước: Nếu $a$ chia hết cho $b$ thì $b$ là ước của $a$. |

### Hoạt động 2.2: Luyện giải bài tập SGK trang 75 (22 phút)
a) Mục tiêu: Vận dụng giải các bài tập 3.44, 3.45, 3.46, 3.48 SGK trang 75.
b) Nội dung: Thực hiện phép tính, tính hợp lí và bài toán có lời văn.
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao các bài tập:<br>  + Bài 3.44: Thực hiện phép tính nhân chia.<br>  + Bài 3.45: Tính giá trị biểu thức một cách hợp lí.<br>  + Bài 3.48: Tìm các ước chung của hai số nguyên.<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc cá nhân vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Sửa bài chi tiết, chốt phương pháp tính nhanh. | **Bài 3.44 (SGK tr.75):**<br>a) $(-3) \\cdot (-2) \\cdot (-5) = 6 \\cdot (-5) = -30$.<br>b) $(-8) \\cdot 12 : (-6) = -96 : (-6) = 16$.<br><br>**Bài 3.45 (SGK tr.75): Tính hợp lí:**<br>$B = (-4) \\cdot 125 \\cdot (-25) \\cdot (-8)$<br>$B = [(-4) \\cdot (-25)] \\cdot [125 \\cdot (-8)] = 100 \\cdot (-1000) = -100\\,000$.<br><br>**Bài 3.48 (SGK tr.75):**<br>Tìm các ước chung của $12$ và $-18$:<br>$\\text{ƯC}(12; -18) = \\{\\pm 1; \\pm 2; \\pm 3; \\pm 6\\}$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng phép nhân và chia số nguyên để giải bài toán tính tốc độ thay đổi nhiệt độ kho lạnh.
b) Nội dung: Nhiệt độ kho lạnh đang là $5^\\circ\\text{C}$, người ta giảm đều nhiệt độ mỗi giờ $2^\\circ\\text{C}$ ($-2^\\circ\\text{C}$). Hỏi sau 6 giờ nhiệt độ là bao nhiêu?
c) Sản phẩm: Lời giải của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế kho lạnh như trên.<br>- **HS:** Tiếp nhận đề bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính toán: $5 + 6 \\cdot (-2) = 5 - 12 = -7^\\circ\\text{C}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ nêu đáp án: $-7^\\circ\\text{C}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học. Dặn dò ôn tập chuẩn bị cho tiết Bài tập cuối chương III. | **Lời giải bài toán kho lạnh:**<br>Nhiệt độ giảm đi sau 6 giờ là:<br>$6 \\cdot (-2) = -12^\\circ\\text{C}$.<br>Nhiệt độ của kho lạnh sau 6 giờ là:<br>$5 + (-12) = -7^\\circ\\text{C}$.<br>Đáp số: $-7^\\circ\\text{C}$. |
"""

# 05. Bài tập cuối chương III (Tiết 43)
md_05 = """Tiết 43 - BÀI TẬP CUỐI CHƯƠNG III (SỐ NGUYÊN)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức của Chương III: Tập hợp các số nguyên $\\mathbb{Z}$, trục số, số đối, thứ tự trong $\\mathbb{Z}$; bốn phép tính cộng, trừ, nhân, chia số nguyên; quy tắc dấu ngoặc và quan hệ ước, bội trong $\\mathbb{Z}$.
- Rèn luyện kĩ năng tính toán chính xác, vận dụng linh hoạt các tính chất đại số để tính nhẩm, tính nhanh.
- Giải quyết thành thạo các bài tập tổng hợp cuối chương trong SGK trang 76.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đánh giá mức độ nắm vững các quy tắc dấu qua sơ đồ tư duy tổng kết toàn chương.
- Giao tiếp và hợp tác: Tự tin phản biện, trao đổi phương pháp giải các bài toán nâng cao trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa quy tắc dấu cho tích của nhiều thừa số nguyên âm.
- Năng lực giải quyết vấn đề toán học: Vận dụng toàn diện kiến thức số nguyên vào giải quyết các bài toán đời sống.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng máy tính cầm tay thực hiện kiểm tra kết quả các phép tính có chứa lũy thừa và dấu ngoặc phức tạp.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS sử dụng AI để tạo bản đồ tóm tắt ngắn gọn các công thức và quy tắc dấu của Chương III.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật và kiên nhẫn trong tính toán số học.
- Ý thức tự giác ôn tập chuẩn bị cho các tiết ôn tập cuối học kì I.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Tổng kết Chương III (vector 300 DPI), tivi/máy chiếu, bảng phụ trắc nghiệm.
2. Học sinh: SGK Toán 6, vở bài tập, máy tính cầm tay, bảng con.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (6 phút)
a) Mục tiêu: Khởi động tinh thần qua bài trắc nghiệm nhanh 4 câu hỏi củng cố toàn bộ quy tắc Chương III.
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm nhanh trên màn chiếu.
c) Sản phẩm: Bảng chọn đáp án của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu hỏi trắc nghiệm củng cố quy tắc dấu và số đối.<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ bảng đáp án.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ giải thích các câu hỏi.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá mức độ nắm bài toàn chương của lớp, bắt đầu tiết ôn tập cuối chương. | **Đáp án khởi động:**<br>Nắm vững quy tắc dấu của cộng, trừ, nhân, chia số nguyên. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (30 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Giúp học sinh nhìn thấy bức tranh toàn cảnh của toàn bộ Chương III qua Sơ đồ tư duy cô đọng, mạch lạc.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tổng kết Chương III; củng cố các nhánh kiến thức.

![Sơ đồ tư duy Tổng kết Chương III](khbd-ill:mindmap-toan6-tiet43)

c) Sản phẩm: Bản ghi nhớ toàn bộ Chương III trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Tổng kết Chương III lên màn chiếu. Nêu câu hỏi tóm tắt:<br>  1. Tập hợp số nguyên $\\mathbb{Z}$ gồm những thành phần nào?<br>  2. Nhắc lại quy tắc dấu của phép cộng và phép nhân.<br>  3. Nêu các ứng dụng thực tiễn của số nguyên.<br>- **HS:** Quan sát sơ đồ tư duy và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm 4 người trong 3 phút.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm trình bày tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa sơ đồ, khen ngợi học sinh nắm vững bản chất kiến thức. | **Tổng kết Chương III:**<br>- Tập hợp $\\mathbb{Z}$: Số âm, số $0$, số dương.<br>- Bốn phép tính: $+$, $-$, $\\times$, $:$.<br>- Tính chất đại số: Giao hoán, kết hợp, phân phối, quy tắc dấu ngoặc.<br>- Ứng dụng: Nhiệt độ, độ cao, tài chính, thời gian. |

### Hoạt động 2.2: Luyện giải bài tập tổng hợp SGK trang 76 (20 phút)
a) Mục tiêu: Vận dụng thành thạo giải các bài tập 3.49, 3.51, 3.52, 3.54 SGK trang 76.
b) Nội dung: Giải các bài toán tính giá trị biểu thức và tìm $x$.
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao các bài tập tổng hợp:<br>  + Bài 3.51: Tính giá trị biểu thức một cách hợp lí.<br>  + Bài 3.52: Liệt kê các phần tử và tính tổng các số nguyên $x$.<br>  + Bài 3.54: Tính giá trị biểu thức khi biết giá trị của biến.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự lực làm bài vào vở bài tập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt lại kĩ năng nhóm các cặp số đối nhau để tổng bằng $0$. | **Bài 3.51 (SGK tr.76): Tính hợp lí:**<br>$A = (-125) \\cdot 25 \\cdot (-8) \\cdot (-4)$<br>$A = [(-125) \\cdot (-8)] \\cdot [25 \\cdot (-4)] = 1000 \\cdot (-100) = -100\\,000$.<br><br>**Bài 3.52 (SGK tr.76):**<br>Liệt kê và tính tổng các số nguyên $x$ với $-5 < x < 5$:<br>$x \\in \\{-4; -3; -2; -1; 0; 1; 2; 3; 4\\}$.<br>Tổng $S = (-4 + 4) + (-3 + 3) + (-2 + 2) + (-1 + 1) + 0 = 0$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (9 phút)
a) Mục tiêu: Vận dụng tính chất lũy thừa và tích của các số nguyên để giải bài toán thực tế.
b) Nội dung: Giải bài toán về sự nhân đôi của một loại vi khuẩn trong phòng thí nghiệm.
c) Sản phẩm: Lời giải của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán: Một quần thể vi khuẩn ban đầu có 100 cá thể, cứ sau mỗi giờ số lượng vi khuẩn tăng gấp đôi. Hỏi sau 5 giờ có tất cả bao nhiêu cá thể vi khuẩn?<br>- **HS:** Tiếp nhận bài toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết biểu thức: $100 \\cdot 2^5 = 100 \\cdot 32 = 3200$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ nêu kết quả: $3200$ cá thể.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học. Dặn dò HS chuẩn bị chu đáo cho chùm 4 tiết Ôn tập cuối học kì I ở tuần sau. | **Lời giải thực tế:**<br>Số lượng vi khuẩn sau 5 giờ là:<br>$100 \\cdot 2^5 = 100 \\cdot 32 = 3200$ (cá thể).<br>Đáp số: $3200$ cá thể. |
"""

# 06. Ôn tập cuối học kì I Số học (Tiết 44 - 47)
md_06 = """Tiết 44, 45, 46, 47 - ÔN TẬP CUỐI HỌC KÌ I (SỐ HỌC)
*Thời lượng thực hiện: 04 tiết (180 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Số học của Học kì I gồm 3 chương:
  + **Chương I: Tập hợp các số tự nhiên:** Tập hợp $\\mathbb{N}$ và $\\mathbb{N}^*$, thứ tự trong $\\mathbb{N}$; bốn phép tính cộng, trừ, nhân, chia và lũy thừa với số mũ tự nhiên; thứ tự thực hiện các phép tính (ngoặc tròn $\\rightarrow$ vuông $\\rightarrow$ nhọn).
  + **Chương II: Tính chia hết trong tập hợp các số tự nhiên:** Quan hệ chia hết, tính chất chia hết của một tổng; dấu hiệu chia hết cho $2, 5, 3, 9$; số nguyên tố, hợp số, phân tích ra thừa số nguyên tố; Ước chung, Bội chung, ƯCLN và BCNN cùng các ứng dụng thực tế.
  + **Chương III: Số nguyên:** Tập hợp $\\mathbb{Z}$, biểu diễn trên trục số, số đối, so sánh số nguyên; bốn phép tính cộng, trừ, nhân, chia số nguyên; quy tắc dấu ngoặc và quan hệ ước, bội trong $\\mathbb{Z}$.
- Rèn luyện kĩ năng giải các dạng bài tập phân loại: Tính giá trị biểu thức hợp lý, tìm số chưa biết $x$, bài toán có lời văn thực tiễn và bài toán tìm giá trị lớn nhất/nhỏ nhất hoặc chia hết nâng cao.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ lại sơ đồ tư duy hệ thống kiến thức 3 chương, chủ động rà soát những phần kiến thức chưa vững.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải toán trong nhóm học tập, biết lắng nghe và phản biện ý kiến bạn bè.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận lựa chọn phương pháp tìm ƯCLN hay BCNN; giải thích quy tắc dấu.
- Năng lực giải quyết vấn đề toán học: Vận dụng linh hoạt các thuật toán số học vào giải toán thực tế đời sống.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng thành thạo máy tính cầm tay (các phím phân tích thừa số nguyên tố FACT, phím chia có dư, hàm GCD, LCM và phím số âm) để giải nhanh và kiểm tra kết quả bài toán số học.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để phân loại các dạng bài toán số học thường gặp trong đề thi cuối học kì I và tự luyện các câu hỏi trắc nghiệm.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn thận, tỉ mỉ và kiên trì trong tính toán.
- Ý thức tự giác, tự tin chuẩn bị tốt nhất cho bài kiểm tra cuối học kì I.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Ôn tập cuối HKI Số học 6 (vector 300 DPI), tivi/máy chiếu, đề cương ôn tập.
2. Học sinh: SGK Toán 6, vở bài tập, máy tính cầm tay, đề cương ôn tập đã làm trước ở nhà.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (10 phút)
a) Mục tiêu: Kích hoạt tư duy và sự hào hứng qua trò chơi tiếp sức giải toán số học.
b) Nội dung: Hai đội thi đấu giải nhanh 4 câu hỏi trắc nghiệm đại diện cho 3 chương học kì I.
c) Sản phẩm: Bảng kết quả của hai đội.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chia lớp thành 2 đội: Đội Số Tự Nhiên và Đội Số Nguyên. Giao 4 câu hỏi trắc nghiệm nhanh trên màn chiếu.<br>- **HS:** Cử đại diện tham gia.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mỗi thành viên lên bảng giải 1 câu rồi chuyền phấn cho bạn tiếp theo.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cả lớp đối chiếu kết quả, chấm điểm thi đua.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ chính xác và tốc độ, dẫn dắt vào chùm tiết ôn tập cuối học kì I. | **Khởi động:**<br>Củng cố phản xạ tính toán và quy tắc dấu, tạo tâm thế tích cực cho chuỗi tiết ôn tập. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (130 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (30 phút)
a) Mục tiêu: Giúp học sinh nắm vững mạng lưới kiến thức toàn diện 3 chương Số học qua Sơ đồ tư duy trực quan.
b) Nội dung: Quan sát và phân tích Sơ đồ tư duy Mindmap Ôn tập cuối HKI Số học 6; nhắc lại các kiến thức trọng tâm.

![Sơ đồ tư duy Ôn tập Cuối HK1 Số học](khbd-ill:mindmap-toan6-tiet44-47)

c) Sản phẩm: Bảng tổng kết kiến thức 3 chương trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Ôn tập cuối HKI Số học. Yêu cầu 3 nhóm thảo luận 3 nhánh lớn:<br>  + Nhóm 1: Chương I (Số tự nhiên, lũy thừa, thứ tự thực hiện phép tính).<br>  + Nhóm 2: Chương II (Tính chia hết, số nguyên tố, ƯCLN, BCNN).<br>  + Nhóm 3: Chương III (Tập hợp $\\mathbb{Z}$, các phép tính, quy tắc dấu ngoặc).<br>- **HS:** Đọc sơ đồ tư duy và chuẩn bị thuyết trình tóm tắt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm trong 5 phút.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 3 nhóm lần lượt trình bày tóm tắt từng nhánh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa toàn bộ kiến thức, chốt các dạng bài trọng tâm trong đề kiểm tra. | **Hệ thống kiến thức trọng tâm:**<br>1. **Chương I:** Lũy thừa $a^m \\cdot a^n = a^{m+n}$; thứ tự ngoặc: $( ) \\rightarrow [ ] \\rightarrow \\{ \\}$.<br>2. **Chương II:**<br>- $a$ chia hết cho $m$ và $b$ chia hết cho $m \\rightarrow (a + b)$ chia hết cho $m$.<br>- ƯCLN: Chọn thừa số nguyên tố chung với số mũ nhỏ nhất.<br>- BCNN: Chọn thừa số nguyên tố chung và riêng với số mũ lớn nhất.<br>3. **Chương III:** Quy tắc cộng, trừ, nhân, chia số nguyên và dấu ngoặc. |

### Hoạt động 2.2: Luyện giải hệ thống bài tập phân dạng (100 phút)
a) Mục tiêu: Rèn luyện thành thạo 4 dạng bài tập cốt lõi của học kì I.
b) Nội dung: Giải bài tập trong đề cương ôn tập: Dạng 1 (Thực hiện phép tính); Dạng 2 (Tìm $x$); Dạng 3 (Toán thực tế ƯCLN, BCNN); Dạng 4 (Bài toán nâng cao).
c) Sản phẩm: Lời giải chi tiết của học sinh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phân công bài tập theo 4 dạng:<br>  + **Dạng 1 (Tính hợp lí):**<br>    $A = 25 \\cdot 125 \\cdot (-4) \\cdot (-8)$<br>    $B = 17 \\cdot 85 + 15 \\cdot 17 - 120$<br>  + **Dạng 2 (Tìm $x$):**<br>    a) $2x - 15 = -25$; b) $125 - 5(x + 4) = 35$<br>  + **Dạng 3 (Toán thực tế BCNN):**<br>    Học sinh khối 6 khi xếp hàng 12, hàng 15, hàng 18 đều vừa đủ. Biết số học sinh trong khoảng từ 300 đến 400 em. Tính số học sinh.<br>- **HS:** Nhận nhiệm vụ và làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Độc lập giải bài. GV hướng dẫn HS dạng toán thực tế gọi $x$ là số học sinh, tìm $\\text{BCNN}(12, 15, 18)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 4 HS lên bảng trình bày 4 bài.<br>- Cả lớp nhận xét, chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt phương pháp trình bày chuẩn mực. | **Dạng 1: Tính hợp lí:**<br>$A = [25 \\cdot (-4)] \\cdot [125 \\cdot (-8)] = (-100) \\cdot (-1000) = 100\\,000$.<br>$B = 17 \\cdot (85 + 15) - 120 = 17 \\cdot 100 - 120 = 1700 - 120 = 1580$.<br><br>**Dạng 2: Tìm $x$:**<br>a) $2x = -25 + 15 = -10 \\rightarrow x = -5$.<br>b) $5(x + 4) = 125 - 35 = 90 \\rightarrow x + 4 = 18 \\rightarrow x = 14$.<br><br>**Dạng 3: Toán thực tế:**<br>- Gọi số học sinh khối 6 là $x$ ($x \\in \\mathbb{N}^*$, $300 \\le x \\le 400$).<br>- Vì $x$ chia hết cho $12, 15, 18$ nên $x \\in \\text{BC}(12, 15, 18)$.<br>- Ta có: $12 = 2^2 \\cdot 3$; $15 = 3 \\cdot 5$; $18 = 2 \\cdot 3^2$.<br>$\\text{BCNN}(12, 15, 18) = 2^2 \\cdot 3^2 \\cdot 5 = 180$.<br>$\\text{BC}(12, 15, 18) = \\{0; 180; 360; 540; ...\\}$.<br>- Vì $300 \\le x \\le 400$ nên $x = 360$.<br>Vậy số học sinh khối 6 là $360$ em. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (40 phút)
a) Mục tiêu: Vận dụng giải bài toán nâng cao về chia hết và tính tổng dãy số nguyên có quy luật.
b) Nội dung: Tính tổng $S = 1 - 2 + 3 - 4 + 5 - 6 + ... + 99 - 100$.
c) Sản phẩm: Lời giải bài toán tính tổng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đưa ra bài toán tính tổng dãy số quy luật:<br>  $S = 1 - 2 + 3 - 4 + 5 - 6 + ... + 99 - 100$.<br>- **HS:** Nhận đề bài và tìm quy luật nhóm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét: Cứ mỗi cặp $(1 - 2) = -1$; $(3 - 4) = -1$... Dãy có 100 số hạng, tương ứng có 50 cặp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày: $S = (-1) \\cdot 50 = -50$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi học sinh đã phát hiện quy luật rất nhanh. Dặn dò ôn tập kĩ để chuẩn bị cho tiết Kiểm tra cuối học kì I. | **Lời giải:**<br>Dãy số có 100 số hạng. Nhóm thành 50 cặp:<br>$S = (1 - 2) + (3 - 4) + ... + (99 - 100)$<br>$S = (-1) + (-1) + ... + (-1)$ (50 số hạng $-1$)<br>$S = (-1) \\cdot 50 = -50$.<br>Đáp số: $-50$. |
"""

# 07. Kiểm tra cuối học kì I Số học (Tiết 48)
md_07 = """Tiết 48 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (SỐ HỌC 6)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện kiến thức, kĩ năng của học sinh về phần Số học Học kì I gồm 3 chương: Chương I (Số tự nhiên), Chương II (Tính chia hết), Chương III (Số nguyên).
- Kiểm tra năng lực vận dụng các phép tính, thứ tự thực hiện phép tính, tìm $x$, thuật toán tìm ƯCLN/BCNN và giải toán thực tiễn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác làm bài thi độc lập, nghiêm túc, không quay cóp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học; Năng lực giải quyết vấn đề toán học.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng máy tính cầm tay đúng quy chế thi (dùng kiểm tra kết quả tính nhẩm, không dùng các thiết bị truyền tin số bị cấm trong phòng thi).***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.D1.1: HS có ý thức tự lực hoàn thành bài kiểm tra, trung thực học thuật, không gian lận.***

## 3. Về phẩm chất
- Rèn luyện phẩm chất trung thực, cẩn thận, kỷ luật và tự trọng.

# II. CẤU TRÚC ĐỀ KIỂM TRA

## 1. Hình thức kiểm tra
- Kết hợp Trắc nghiệm khách quan (50% - 5,0 điểm gồm 10 câu) và Tự luận (50% - 5,0 điểm gồm 3 câu).
- Thời gian làm bài: 45 phút.

---

## 2. ĐỀ KIỂM TRA MẪU CHUẨN

### PHẦN I. TRẮC NGHIỆM KHÁCH QUAN (5,0 điểm - Mỗi câu 0,5 điểm)
**Câu 1 (NB):** Cho tập hợp $A = \\{x \\in \\mathbb{N}^* \\mid x \\le 4\\}$. Tập hợp $A$ viết dưới dạng liệt kê là:
A. $\\{0; 1; 2; 3; 4\\}$.
B. $\\{1; 2; 3; 4\\}$.
C. $\\{1; 2; 3\\}$.
D. $\\{0; 1; 2; 3\\}$.

**Câu 2 (NB):** Kết quả của phép tính $3^2 \\cdot 3^3$ bằng:
A. $3^6$.
B. $3^5$.
C. $9^5$.
D. $6^5$.

**Câu 3 (NB):** Số nào sau đây là số nguyên tố?
A. $9$.
B. $15$.
C. $17$.
D. $21$.

**Câu 4 (TH):** Số nào sau đây chia hết cho cả $2$ và $5$?
A. $125$.
B. $230$.
C. $342$.
D. $555$.

**Câu 5 (TH):** Ước chung lớn nhất của $12$ và $18$ là:
A. $2$.
B. $3$.
C. $6$.
D. $36$.

**Câu 6 (NB):** Số đối của số $-15$ là:
A. $-15$.
B. $15$.
C. $0$.
D. $51$.

**Câu 7 (TH):** Kết quả của phép tính $(-12) + (-18)$ là:
A. $30$.
B. $-30$.
C. $-6$.
D. $6$.

**Câu 8 (TH):** Kết quả của phép tính $5 - (-8)$ là:
A. $-3$.
B. $3$.
C. $-13$.
D. $13$.

**Câu 9 (TH):** Tích của hai số nguyên âm luôn là:
A. Một số nguyên âm.
B. Một số nguyên dương.
C. Bằng số 0.
D. Không xác định được.

**Câu 10 (VD):** Tập hợp tất cả các ước nguyên của số $4$ là:
A. $\\{1; 2; 4\\}$.
B. $\\{-1; -2; -4\\}$.
C. $\\{\\pm 1; \\pm 2; \\pm 4\\}$.
D. $\\{0; \\pm 1; \\pm 2; \\pm 4\\}$.

---

### PHẦN II. TỰ LUẬN (5,0 điểm)

**Câu 1 (2,0 điểm):** Thực hiện phép tính (tính hợp lí nếu có thể):
a) $150 - [10^2 - (14 - 11)^2 \\cdot 2026^0]$
b) $(-25) \\cdot 68 + (-25) \\cdot 32$

**Câu 2 (1,5 điểm):** Tìm số nguyên $x$, biết:
a) $x - (-12) = 20$
b) $3(x - 2) + 15 = 0$

**Câu 3 (1,5 điểm):**
Một đội thiện nguyện có 48 hộp sữa và 72 gói bánh. Đội muốn chia số sữa và bánh này thành các phần quà đều nhau sao cho số hộp sữa và số gói bánh ở mỗi phần quà là như nhau. Hỏi có thể chia được nhiều nhất thành bao nhiêu phần quà? Khi đó, mỗi phần quà có bao nhiêu hộp sữa và bao nhiêu gói bánh?

---

# III. HƯỚNG DẪN CHẤM VÀ THANG ĐIỂM

## 1. Trắc nghiệm (5,0 điểm - Mỗi câu 0,5 điểm)
- Câu 1: **B** | Câu 2: **B** | Câu 3: **C** | Câu 4: **B** | Câu 5: **C**
- Câu 6: **B** | Câu 7: **B** | Câu 8: **D** | Câu 9: **B** | Câu 10: **C**

## 2. Tự luận (5,0 điểm)

| Câu | Nội dung đáp án chuẩn | Điểm |
| :---: | :--- | :---: |
| **Câu 1**<br>*(2,0 đ)* | **a)** $150 - [100 - 3^2 \\cdot 1] = 150 - [100 - 9] = 150 - 91 = 59$.<br><br>**b)** $= (-25) \\cdot (68 + 32) = (-25) \\cdot 100 = -2500$. | 1,0 đ<br><br>1,0 đ |
| **Câu 2**<br>*(1,5 đ)* | **a)** $x + 12 = 20 \\rightarrow x = 20 - 12 = 8$.<br><br>**b)** $3(x - 2) = -15 \\rightarrow x - 2 = -5 \\rightarrow x = -5 + 2 = -3$. | 0,75 đ<br><br>0,75 đ |
| **Câu 3**<br>*(1,5 đ)* | - Gọi số phần quà nhiều nhất có thể chia là $a$ ($a \\in \\mathbb{N}^*$).<br>- Vì số sữa và bánh chia đều vào $a$ phần quà nên $48$ chia hết cho $a$ và $72$ chia hết cho $a$, mà $a$ lớn nhất nên $a = \\text{ƯCLN}(48, 72)$.<br>- Ta có: $48 = 2^4 \\cdot 3$; $72 = 2^3 \\cdot 3^2$.<br>$\\text{ƯCLN}(48, 72) = 2^3 \\cdot 3 = 24$.<br>Vậy có thể chia được nhiều nhất 24 phần quà.<br>- Mỗi phần quà có: $48 : 24 = 2$ (hộp sữa) và $72 : 24 = 3$ (gói bánh). | 0,25 đ<br><br>0,5 đ<br><br>0,5 đ<br><br>0,25 đ |

---

# IV. TIẾN TRÌNH TỔ CHỨC KIỂM TRA (45 phút)
1. Ổn định và phát đề (3 phút).
2. Học sinh làm bài nghiêm túc (37 phút).
3. Thu bài và nhận xét (5 phút).
"""

# 08. HĐTN Sử dụng máy tính cầm tay (Tiết 49, 50)
md_08 = """Tiết 49, 50 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: SỬ DỤNG MÁY TÍNH CẦM TAY
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết các phím chức năng cơ bản trên máy tính cầm tay (Casio fx-580VN X, Vinacal...): Phím bật/tắt (ON/SHIFT OFF), phím số âm `(-)`, phím lũy thừa `x^■`, phím phân tích thừa số nguyên tố `FACT`, phím tìm ước chung lớn nhất `GCD` và bội chung nhỏ nhất `LCM`.
- Thực hành thành thạo sử dụng máy tính cầm tay để:
  + Tính giá trị biểu thức số có chứa nhiều lớp dấu ngoặc và số nguyên âm.
  + Phân tích một số tự nhiên ra thừa số nguyên tố một cách tức thời.
  + Tìm nhanh $\\text{ƯCLN}$ và $\\text{BCNN}$ của hai hay nhiều số lớn.
  + Kiểm tra tính đúng đắn của các bài toán tính toán đã giải bằng tay.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đọc bảng tra cứu phím chức năng trong SGK trang 119-121, chủ động thực hành bấm máy theo các ví dụ mẫu.
- Giao tiếp và hợp tác: Hướng dẫn bạn cùng bàn thao tác bấm các tổ hợp phím phức tạp (`SHIFT` + phím chức năng).

b) Năng lực đặc thù môn Toán:
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo máy tính cầm tay để hỗ trợ học toán, biết phối hợp giữa tư duy toán học và công nghệ hỗ trợ.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng thành thạo các tính năng nâng cao của máy tính cầm tay như hàm GCD, LCM, FACT để phân tích dữ liệu số và giải quyết các bài toán số học phức tạp.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS tìm hiểu cách máy tính cầm tay sử dụng các thuật toán Euclid để tính ƯCLN một cách siêu tốc tương tự thuật toán máy học.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi nhập dữ liệu vào máy tính.
- Ý thức không lạm dụng máy tính cầm tay trong các bài toán rèn luyện tư duy tính nhẩm cơ bản.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, máy chiếu hoặc phần mềm giả lập máy tính Casio fx-580VN X trên máy tính, phiếu thực hành.
2. Học sinh: SGK Toán 6, máy tính cầm tay (Casio fx-570VN Plus hoặc fx-580VN X), vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: Khơi gợi sự tò mò và hứng thú của học sinh về tốc độ xử lí của máy tính cầm tay.
b) Nội dung: So sánh thời gian phân tích số $12600$ ra thừa số nguyên tố giữa tính tay và bấm máy.
c) Sản phẩm: Kết quả phân tích $12600 = 2^3 \\cdot 3^2 \\cdot 5^2 \\cdot 7$ xuất hiện trên màn hình máy tính chỉ sau 1 giây.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho số $12600$. Đố các em phân tích được số này ra thừa số nguyên tố trong vòng 3 giây mà không cần đặt bút tính?<br>- **HS:** Lắng nghe và ngạc nhiên.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Thao tác trên phần mềm giả lập máy tính: Bấm `12600` $\\rightarrow$ `=` $\\rightarrow$ `SHIFT` $\\rightarrow$ `FACT`.<br>- **HS:** Quan sát kết quả hiển thị trên màn hình.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS reo vui và hào hứng muốn tự thực hiện trên máy của mình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu bài học thực hành: Khám phá các tính năng kì diệu của máy tính cầm tay. | **Khởi động:**<br>Máy tính cầm tay là công cụ hỗ trợ tính toán vô cùng mạnh mẽ giúp học sinh tiết kiệm thời gian và kiểm chứng kết quả nhanh chóng. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KĨ NĂNG THAO TÁC (50 phút)
### Hoạt động 2.1: Thao tác tính toán với số nguyên âm và lũy thừa (25 phút - Tiết 49)
a) Mục tiêu: Biết sử dụng phím dấu âm `(-)`, phím ngoặc và phím lũy thừa.
b) Nội dung: Tìm hiểu hướng dẫn mục 1, 2 SGK trang 119-120; thực hành tính các biểu thức có dấu âm.
c) Sản phẩm: Thao tác bấm phím chuẩn xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn:<br>  + Phím `(-)` dùng để nhập số nguyên âm (khác với phím trừ phép toán `-`).<br>  + Phím `x^■` để nhập lũy thừa.<br>  + Yêu cầu HS tính:<br>    1. $(-15) + (-28) \\cdot (-4)$<br>    2. $(-3)^4 - (-2)^5$<br>- **HS:** Quan sát mẫu và bấm máy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhập nguyên biểu thức vào máy tính rồi bấm phím `=`.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đối chiếu kết quả: Biểu thức 1 ra $97$; biểu thức 2 ra $81 - (-32) = 113$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Lưu ý: Khi tính lũy thừa của số âm bắt buộc phải cho số âm vào trong dấu ngoặc đơn: `((-3))^4`. | **1. Thao tác số âm và lũy thừa:**<br>- Nhập số âm: Bấm phím `(-)` rồi bấm số.<br>- Lũy thừa số âm: `(` $\\rightarrow$ `(-)` $\\rightarrow$ `a` $\\rightarrow$ `)` $\\rightarrow$ `x^■` $\\rightarrow$ `n`.<br>Ví dụ: $(-3)^4 = 81$. |

### Hoạt động 2.2: Phân tích thừa số nguyên tố, tìm ƯCLN và BCNN (25 phút - Tiết 50)
a) Mục tiêu: Sử dụng thành thạo phím `FACT`, hàm `GCD` và `LCM`.
b) Nội dung: Đọc mục 3 SGK trang 120-121; thực hành tìm ƯCLN và BCNN của các số lớn.
c) Sản phẩm: Kết quả thực hành của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn thao tác:<br>  + Phân tích ra TSNT: Nhập số $\\rightarrow$ `=` $\\rightarrow$ `SHIFT` $\\rightarrow$ `FACT` (`.,\'\'\'`).<br>  + Tìm ƯCLN (GCD): Bấm `ALPHA` $\\rightarrow$ `(` (GCD) $\\rightarrow$ Nhập số thứ nhất $\\rightarrow$ `SHIFT` $\\rightarrow$ `)` (dấu phẩy `,`) $\\rightarrow$ Nhập số thứ hai $\\rightarrow$ `)` $\\rightarrow$ `=`.<br>  + Tìm BCNN (LCM): Bấm `ALPHA` $\\rightarrow$ `)` (LCM)...<br>- **GV:** Yêu cầu HS tìm $\\text{ƯCLN}(144, 192)$ và $\\text{BCNN}(36, 48)$.<br>- **HS:** Quan sát và thực hành theo cặp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bấm máy và ghi lại kết quả.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS đọc kết quả: $\\text{ƯCLN} = 48$; $\\text{BCNN} = 144$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi học sinh đã làm chủ được công cụ máy tính cầm tay. | **2. Phân tích TSNT và tìm ƯCLN, BCNN:**<br>- Lệnh FACT: Phân tích thừa số nguyên tố tức thời.<br>- Lệnh GCD: Tìm Ước chung lớn nhất.<br>$\\text{GCD}(144, 192) = 48$.<br>- Lệnh LCM: Tìm Bội chung nhỏ nhất.<br>$\\text{LCM}(36, 48) = 144$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP VÀ THỰC HÀNH (23 phút)
a) Mục tiêu: Tự lực dùng máy tính cầm tay hoàn thành phiếu thực hành 5 bài toán tổng hợp.
b) Nội dung: Thực hành trên phiếu học tập do giáo viên phát.
c) Sản phẩm: Phiếu kết quả thực hành đã hoàn thành của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát phiếu thực hành gồm 5 câu kiểm tra kĩ năng bấm máy tổng hợp.<br>- **HS:** Nhận phiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự lực thao tác trên máy tính cầm tay của mình.<br>- **GV:** Đi quan sát, hỗ trợ học sinh bấm nhầm phím `AC` hoặc `DEL`.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đổi chéo phiếu học tập giữa hai bạn cùng bàn để chấm điểm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng kết điểm số, biểu dương các bạn thao tác nhanh và chính xác. | **Kết quả phiếu thực hành:**<br>100% học sinh biết cách bật/tắt, dùng phím âm, lũy thừa, FACT, GCD, LCM thành thạo. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
a) Mục tiêu: Hiểu rõ ranh giới giữa việc dùng máy tính để hỗ trợ kiểm tra và việc lạm dụng máy tính làm mòn tư duy.
b) Nội dung: Thảo luận về văn hóa sử dụng máy tính cầm tay trong học toán.
c) Sản phẩm: Quy tắc sử dụng máy tính văn minh của lớp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt câu hỏi: Theo em, khi nào ta nên dùng máy tính cầm tay và khi nào ta nên tự tính tay?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời: Với bài tập tính nhẩm cơ bản nên tự tính tay để rèn luyện trí não, máy tính chỉ dùng khi số quá lớn hoặc dùng để kiểm tra lại kết quả bài làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa thông điệp sư phạm: Máy tính là người bạn hỗ trợ đắc lực, nhưng bộ não của các em mới là người ra quyết định! | **Thông điệp sư phạm:**<br>- Máy tính cầm tay là công cụ hỗ trợ kiểm tra tính toán và giải quyết số liệu lớn.<br>- Luôn chủ động rèn luyện tư duy tính nhẩm để phát triển trí tuệ toán học. |
"""

tasks = [
    ("03_KHBD_Toan6_Bai17_PhepChiaHet_UocBoi_Tiet41.md", md_03),
    ("04_KHBD_Toan6_LuyenTapChung_Tiet42.md", md_04),
    ("05_KHBD_Toan6_BaiTapCuoiChuong3_Tiet43.md", md_05),
    ("06_KHBD_Toan6_OnTapCuoiHK1_SoHoc_Tiet44-47.md", md_06),
    ("07_KHBD_Toan6_KiemTraCuoiHK1_SoHoc_Tiet48.md", md_07),
    ("08_KHBD_Toan6_HDTN_SuDungMayTinhCamTay_Tiet49-50.md", md_08),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")

print(">>> HOÀN TẤT TẠO 8 TỆP SỐ HỌC 6! <<<")
