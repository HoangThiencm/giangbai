# -*- coding: utf-8 -*-
"""
Script sinh 8 KHBD Chương VII: Số thập phân (Tiết 66 - 80) - Toán 6 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan6"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    {
        "filename": "09_KHBD_Toan6_Bai28_SoThapPhan_Tiet66-67.md",
        "header": "TIẾT 66, 67 - BÀI 28: SỐ THẬP PHÂN\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 66, 67 - BÀI 28: SỐ THẬP PHÂN
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết phân số thập phân và cách viết phân số thập phân dưới dạng số thập phân (gồm phần số nguyên và phần thập phân).
- Nhận biết số thập phân âm là số đối của số thập phân dương: $-a$ đối với $a$.
- Nắm vững quy tắc so sánh hai số thập phân bất kì (dương, âm).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác tìm hiểu mối quan hệ giữa phân số thập phân và số thập phân; phân biệt các hàng thập phân (phần mười, phần trăm, phần nghìn,...).
- Giao tiếp và hợp tác: Thảo luận nhóm về cách so sánh hai số thập phân âm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh hai số thập phân âm bằng cách so sánh hai số đối của chúng.
- Năng lực giải quyết vấn đề toán học: Sử dụng số thập phân âm để biểu diễn số đo nhiệt độ âm, độ sâu dưới mực nước biển, độ cận thị.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay thực hiện chuyển đổi qua lại giữa phân số và số thập phân bằng phím S-D.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh ứng dụng AI để tìm kiếm số liệu nhiệt độ kỷ lục đo được tại Nam Cực và so sánh các giá trị âm.***

## 3. Về phẩm chất
- Cẩn thận, chính xác khi xác định vị trí dấu phẩy và các hàng chữ số sau dấu phẩy.
- Ý thức liên hệ toán học với đời sống thực tế xung quanh.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, bảng phụ, tivi/máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Gợi lại kiến thức số thập phân dương ở Tiểu học và đặt vấn đề về số thập phân âm trong thực tế.
b) Nội dung: Quan sát bảng dự báo thời tiết tại Sa Pa vào mùa đông có nhiệt độ $-1{,}5^\\circ\\text{C}$.
c) Sản phẩm: Ý kiến phát biểu của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh nhiệt kế đo nhiệt độ $-1{,}5^\\circ\\text{C}$. Hỏi HS: Ở Tiểu học ta đã học số thập phân $1{,}5$. Vậy $-1{,}5$ là số gì và có ý nghĩa như thế nào?<br>- **HS:** Quan sát nhiệt kế.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và liên hệ với số nguyên âm đã học.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $-1{,}5$ là số đối của $1{,}5$, biểu thị nhiệt độ dưới $0^\\circ\\text{C}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu bài mới: Số thập phân mở rộng (bao gồm cả số thập phân âm). | Số $-1{,}5$ là số thập phân âm, biểu diễn nhiệt độ dưới $0^\\circ\\text{C}$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Phân số thập phân và số thập phân (35 phút)
a) Mục tiêu: Nhận biết phân số thập phân có mẫu là lũy thừa của $10$ và cách viết thành số thập phân.
b) Nội dung: Định nghĩa phân số thập phân, số thập phân âm, phần nguyên và phần thập phân.
c) Sản phẩm: Vở ghi và bài tập viết số thập phân.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phân số thập phân là phân số mà mẫu là lũy thừa của $10$ (như $10, 100, 1000,...$). Viết $\\frac{-15}{10}; \\frac{27}{100}; \\frac{-125}{1000}$ dưới dạng số thập phân.<br>- **HS:** Tiếp nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết: $\\frac{-15}{10} = -1{,}5$; $\\frac{27}{100} = 0{,}27$; $\\frac{-125}{1000} = -0{,}125$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu cấu tạo: Gồm phần số nguyên (trước dấu phẩy) và phần thập phân (sau dấu phẩy).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa khái niệm số thập phân âm và số đối. | **1. Phân số thập phân và số thập phân:**<br>- Phân số thập phân có mẫu là lũy thừa của $10$.<br>- Số thập phân gồm phần nguyên và phần thập phân ngăn cách bởi dấu phẩy.<br>- Số thập phân âm là số đối của số thập phân dương:<br>  Số đối của $1{,}5$ là $-1{,}5$.<br>  Số đối của $-0{,}27$ là $0{,}27$. |

### Hoạt động 2.2: So sánh hai số thập phân (30 phút)
a) Mục tiêu: Nắm vững quy tắc so sánh hai số thập phân dương, so sánh với $0$ và so sánh hai số thập phân âm.
b) Nội dung: Quy tắc so sánh hai số thập phân bất kì.
c) Sản phẩm: Lời giải bài tập so sánh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc: So sánh hai số thập phân dương như ở Tiểu học. Mọi số âm đều nhỏ hơn $0$ và nhỏ hơn mọi số dương. Để so sánh hai số thập phân âm $-a$ và $-b$ ($a, b > 0$), nếu $a > b$ thì $-a < -b$.<br>- **HS:** Ghi nhận quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** So sánh: $-2{,}15$ và $-2{,}17$; $-0{,}5$ và $0{,}2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Vì $2{,}15 < 2{,}17$ nên $-2{,}15 > -2{,}17$. Vì $-0{,}5$ âm còn $0{,}2$ dương nên $-0{,}5 < 0{,}2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định quy tắc so sánh tương tự như so sánh hai số nguyên. | **2. So sánh hai số thập phân:**<br>- Số thập phân âm luôn nhỏ hơn $0$ và nhỏ hơn số thập phân dương.<br>- Với hai số thập phân âm: Số nào có số đối lớn hơn thì số đó nhỏ hơn:<br>$$\\text{Nếu } a > b > 0 \\text{ thì } -a < -b$$<br>- Ví dụ: $-2{,}15 > -2{,}17$ vì $2{,}15 < 2{,}17$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Rèn luyện kỹ năng sắp xếp các số thập phân theo thứ tự tăng dần hoặc giảm dần.
b) Nội dung: Bài 7.1, 7.2 SGK trang 28.
c) Sản phẩm: Bài làm trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu sắp xếp các số sau theo thứ tự từ bé đến lớn: $-3{,}15; 0{,}4; -3{,}2; 1{,}75; 0$.<br>- **HS:** Đọc kỹ các số.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tách nhóm số âm: $-3{,}2 < -3{,}15$. Số $0$. Nhóm dương: $0{,}4 < 1{,}75$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng viết thứ tự hoàn chỉnh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kết quả chính xác. | **Sắp xếp thứ tự tăng dần:**<br>$$-3{,}2 < -3{,}15 < 0 < 0{,}4 < 1{,}75$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng số thập phân âm so sánh nhiệt độ sôi của các chất hóa học.
b) Nội dung: So sánh nhiệt độ sôi của Khí Ô-xi ($-183^\\circ\\text{C}$) và Khí Ni-tơ ($-196^\\circ\\text{C}$).
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khí Ô-xi sôi ở $-183^\\circ\\text{C}$, Khí Ni-tơ sôi ở $-196^\\circ\\text{C}$. Khí nào có nhiệt độ sôi cao hơn?<br>- **HS:** Đọc đề và so sánh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** So sánh $-183$ và $-196$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Vì $-183 > -196$ nên nhiệt độ sôi của khí Ô-xi cao hơn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại tính thực tế của việc so sánh số âm. | Ta có: $-183 > -196$.<br>Do đó, nhiệt độ sôi của khí Ô-xi cao hơn nhiệt độ sôi của khí Ni-tơ. |
"""
    },
    {
        "filename": "10_KHBD_Toan6_Bai29_TinhToanVoiSoThapPhan_Tiet68-69.md",
        "header": "TIẾT 68, 69 - BÀI 29: TÍNH TOÁN VỚI SỐ THẬP PHÂN\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 68, 69 - BÀI 29: TÍNH TOÁN VỚI SỐ THẬP PHÂN
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Thực hiện thành thạo các phép tính cộng, trừ, nhân, chia đối với số thập phân (cả số thập phân âm và dương).
- Vận dụng các tính chất giao hoán, kết hợp, phân phối và quy tắc dấu ngoặc để tính toán hợp lí.
- Giải quyết các bài toán tính chu vi, diện tích và tính toán chi tiêu đời sống.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đặt tính và thực hiện cẩn thận từng phép tính; kiểm tra lại kết quả bằng tính nhẩm hoặc máy tính.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận chiến lược nhóm số hạng để tính nhanh nhất.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Nhận diện thừa số chung hoặc các cặp số có tổng là số nguyên tròn chục để tính nhanh.
- Năng lực giải quyết vấn đề toán học: Tính toán hóa đơn mua sắm hàng hóa tại siêu thị.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay để kiểm tra chuỗi phép tính số thập phân nhiều chữ số.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI lập bảng so sánh mức tiêu thụ điện nước giữa các tháng trong gia đình dựa trên đơn giá số thập phân.***

## 3. Về phẩm chất
- Cẩn thận, chính xác khi đặt tính thẳng cột dấu phẩy và đếm số chữ số thập phân khi nhân, chia.
- Tinh thần trách nhiệm trong chi tiêu sinh hoạt hàng ngày.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, bảng phụ quy tắc dấu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại quy tắc nhân, chia số nguyên cùng dấu và khác dấu để vận dụng sang số thập phân.
b) Nội dung: Xác định dấu của: $(-2) \\cdot (-3)$; $(-4) \\cdot 5$. Dự đoán dấu của $(-2{,}5) \\cdot (-4)$ và $(-1{,}2) \\cdot 3$.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc nhân hai số nguyên cùng dấu và khác dấu. Dự đoán kết quả khi áp dụng cho số thập phân.<br>- **HS:** Nhớ lại quy tắc dấu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết nhanh dấu của tích lên bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Tích hai số cùng dấu mang dấu dương, tích hai số khác dấu mang dấu âm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định quy tắc dấu của các phép tính số thập phân hoàn toàn giống quy tắc dấu trong tập hợp số nguyên $\\mathbb{Z}$. | Quy tắc dấu đối với số thập phân hoàn toàn giống với số nguyên. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Phép cộng và phép trừ số thập phân (35 phút)
a) Mục tiêu: Thực hiện đúng quy tắc cộng trừ số thập phân cùng dấu và khác dấu.
b) Nội dung: Quy tắc cộng hai số thập phân âm: Cộng hai số đối rồi đặt dấu trừ trước kết quả; Cộng hai số thập phân khác dấu.
c) Sản phẩm: Bài làm các ví dụ trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc: Cộng hai số cùng dấu âm: $(-a) + (-b) = -(a + b)$. Cộng khác dấu: Lấy số có số đối lớn hơn trừ số có số đối nhỏ hơn rồi đặt dấu của số có số đối lớn hơn. Phép trừ chuyển thành cộng với số đối: $a - b = a + (-b)$.<br>- **HS:** Ghi nhận quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: $(-3{,}5) + (-2{,}7)$ và $(-4{,}2) + 1{,}5$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $(-3{,}5) + (-2{,}7) = -(3{,}5 + 2{,}7) = -6{,}2$. $(-4{,}2) + 1{,}5 = -(4{,}2 - 1{,}5) = -2{,}7$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy tắc tính cộng trừ số thập phân. | **1. Phép cộng và trừ số thập phân:**<br>- Cộng cùng dấu âm: $(-a) + (-b) = -(a + b)$.<br>- Cộng khác dấu: Lấy hiệu hai số đối, mang dấu của số có số đối lớn hơn.<br>- Trừ số thập phân: $a - b = a + (-b)$.<br>- Tính chất: Giao hoán, kết hợp, cộng với số $0$. |

### Hoạt động 2.2: Phép nhân và phép chia số thập phân (30 phút)
a) Mục tiêu: Thực hiện thành thạo phép nhân, phép chia số thập phân dương và âm; áp dụng tính chất phân phối.
b) Nội dung: Quy tắc nhân và chia số thập phân.
c) Sản phẩm: Lời giải bài tập nhân, chia trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc: Nhân/chia hai số cùng dấu kết quả dương; Nhân/chia hai số khác dấu kết quả âm. Thực hiện tính độ lớn như ở Tiểu học.<br>- **HS:** Tiếp thu kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: $(-1{,}5) \\cdot (-0{,}4)$ và $(-4{,}5) : 1{,}5$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $(-1{,}5) \\cdot (-0{,}4) = 1{,}5 \\cdot 0{,}4 = 0{,}6$. $(-4{,}5) : 1{,}5 = -(4{,}5 : 1{,}5) = -3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc và các tính chất phân phối giúp tính nhanh. | **2. Phép nhân và chia số thập phân:**<br>- Nhân/chia cùng dấu: Kết quả mang dấu dương ($+$).<br>- Nhân/chia khác dấu: Kết quả mang dấu âm ($-$).<br>- Tính chất: Giao hoán, kết hợp, nhân với $1$, phân phối của phép nhân đối với phép cộng: $a \\cdot (b + c) = a \\cdot b + a \\cdot c$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính giá trị biểu thức hợp lí bằng cách vận dụng tính chất phân phối.
b) Nội dung: Bài 7.8, 7.9 SGK trang 32.
c) Sản phẩm: Lời giải trên bảng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Tính hợp lí giá trị biểu thức:<br>$E = (-2{,}5) \\cdot 4{,}38 + (-2{,}5) \\cdot 5{,}62$.<br>- **HS:** Quan sát biểu thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt thừa số chung $(-2{,}5)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: $E = (-2{,}5) \\cdot (4{,}38 + 5{,}62) = (-2{,}5) \\cdot 10 = -25$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi học sinh nhận diện nhanh tổng $4{,}38 + 5{,}62 = 10$. | **Tính hợp lí:**<br>$$E = (-2{,}5) \\cdot (4{,}38 + 5{,}62)$$<br>$$E = (-2{,}5) \\cdot 10 = -25$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng tính tiền hóa đơn mua sắm thực tế.
b) Nội dung: Mẹ mua $2{,}5\\text{ kg}$ thịt lợn với giá $130\\,000$ đồng$/\\text{kg}$ và $3{,}2\\text{ kg}$ cam với giá $25\\,000$ đồng$/\\text{kg}$. Tính tổng số tiền mẹ phải trả.
c) Sản phẩm: Lời giải hoàn thiện trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu đề bài toán thực tế mua sắm.<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tổng tiền: $2{,}5 \\cdot 130\\,000 + 3{,}2 \\cdot 25\\,000 = 325\\,000 + 80\\,000 = 405\\,000$ đồng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học thực tiễn. | Tổng số tiền mẹ phải trả là:<br>$$2{,}5 \\cdot 130\\,000 + 3{,}2 \\cdot 25\\,000 = 405\\,000\\text{ (đồng)}$$<br>Đáp số: $405\\,000$ đồng. |
"""
    },
    {
        "filename": "11_KHBD_Toan6_Bai30_LamTronVaUocLuong_Tiet70.md",
        "header": "TIẾT 70 - BÀI 30: LÀM TRÒN VÀ ƯỚC LƯỢNG\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 70 - BÀI 30: LÀM TRÒN VÀ ƯỚC LƯỢNG
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững quy tắc làm tròn số thập phân đến một hàng cho trước (hàng đơn vị, phần mười, phần trăm, phần nghìn,...).
- Biết cách ước lượng kết quả các phép tính số học để nhanh chóng đánh giá tính hợp lí của đáp số.
- Vận dụng làm tròn và ước lượng trong các tình huống thực tiễn như tính tiền, đo đạc, thống kê dân số.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát chữ số ngay sau hàng làm tròn để quyết định cộng thêm $1$ hay giữ nguyên.
- Giao tiếp và hợp tác: Trao đổi nhóm về tính hợp lí của việc làm tròn số trong đời sống hàng ngày.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích căn cứ làm tròn (chữ số sau hàng làm tròn nhỏ hơn $5$ hay lớn hơn hoặc bằng $5$).
- Năng lực giải quyết vấn đề toán học: Ước lượng chi phí đi chợ hoặc chi phí cho một chuyến dã ngoại.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng chức năng làm tròn số (Fix) trên máy tính cầm tay để làm tròn tự động kết quả phép tính.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI mô phỏng sai số tích lũy khi làm tròn số liệu trong các dự án khoa học dữ liệu.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, trung thực và linh hoạt trong tư duy thực tế.
- Ý thức tôn trọng các quy chuẩn quy ước chung trong đo lường xã hội.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, máy chiếu, bảng phụ quy tắc làm tròn.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề từ thực tế mua xăng hoặc thanh toán tiền lẻ không thể trả đúng từng đồng.
b) Nội dung: Trả lời câu hỏi: Đi đổ xăng hết $31\\,640$ đồng thì người bán xăng thường lấy bao nhiêu tiền?
c) Sản phẩm: Ý kiến của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt tình huống: Khi đi đổ xăng hết $31\\,640$ đồng, thực tế người bán thường thu $32\\,000$ đồng hoặc $31\\,500$ đồng. Vì sao lại có việc đó?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Do không có tiền lẻ có mệnh giá $40$ đồng hoặc $640$ đồng nên cần làm tròn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Làm tròn số và ước lượng là kỹ năng thiết yếu trong đời sống. | Trong thực tế ta thường làm tròn số để thuận tiện cho việc thanh toán và ghi nhớ. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Quy tắc làm tròn số (12 phút)
a) Mục tiêu: HS nắm vững quy tắc làm tròn số đến hàng chỉ định.
b) Nội dung: Quy tắc so sánh chữ số đầu tiên bị bỏ đi với số $5$.
c) Sản phẩm: Vở ghi quy tắc và bài tập áp dụng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc làm tròn: Để làm tròn số thập phân đến một hàng nào đó (gọi là hàng làm tròn), ta nhìn chữ số ngay sau hàng làm tròn:<br>  + Nếu chữ số đó nhỏ hơn $5$ thì giữ nguyên hàng làm tròn.<br>  + Nếu chữ số đó lớn hơn hoặc bằng $5$ thì cộng thêm $1$ vào chữ số hàng làm tròn.<br>  + Bỏ các chữ số ở phần thập phân sau hàng làm tròn; thay bằng chữ số $0$ nếu ở phần nguyên.<br>- **HS:** Ghi nhận quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm tròn số $76{,}428$ đến hàng phần mười và hàng đơn vị.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Làm tròn đến phần mười: $76{,}428 \\approx 76{,}4$ (vì chữ số sau là $2 < 5$). Đến hàng đơn vị: $76{,}428 \\approx 76$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc chuẩn mực. | **1. Quy tắc làm tròn số:**<br>- Nhìn chữ số ngay sau hàng làm tròn:<br>  + Nhỏ hơn $5$: Giữ nguyên hàng làm tròn.<br>  + Lớn hơn hoặc bằng $5$: Cộng thêm $1$ vào hàng làm tròn.<br>- Ví dụ: $15{,}372$ làm tròn đến hàng phần mười là $15{,}4$; làm tròn đến hàng đơn vị là $15$. |

### Hoạt động 2.2: Ước lượng kết quả phép tính (8 phút)
a) Mục tiêu: Biết cách làm tròn các số hạng/thừa số trước khi tính để ước lượng kết quả.
b) Nội dung: Ước lượng tích $4{,}9 \\cdot 10{,}2$.
c) Sản phẩm: Kết quả ước lượng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn: Muốn ước lượng kết quả phép tính, ta làm tròn các số trong phép tính đến hàng cao nhất rồi thực hiện tính nhẩm.<br>- **HS:** Tiếp thu phương pháp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ước lượng $4{,}9 \\cdot 10{,}2 \\approx 5 \\cdot 10 = 50$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** So sánh với tích đúng $4{,}9 \\cdot 10{,}2 = 49{,}98$ để thấy sự sát sao của kết quả ước lượng. | **2. Ước lượng kết quả:**<br>- Làm tròn các số đến hàng thích hợp rồi tính nhẩm.<br>- Ví dụ: $4{,}9 \\cdot 10{,}2 \\approx 5 \\cdot 10 = 50$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Thực hành làm tròn số thập phân đến hàng phần mười, phần trăm, phần nghìn.
b) Nội dung: Bài 7.12, 7.13 SGK trang 35.
c) Sản phẩm: Bảng kết quả làm tròn của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu làm tròn số $-3{,}14159$ đến:<br>  a) Hàng phần mười;<br>  b) Hàng phần trăm;<br>  c) Hàng phần nghìn.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng quy tắc dấu và làm tròn số đối.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: a) $-3{,}1$; b) $-3{,}14$; c) $-3{,}142$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Khi làm tròn số âm, ta làm tròn số đối của nó rồi đặt dấu trừ đằng trước. | **Kết quả làm tròn số $-3{,}14159$:**<br>a) Đến hàng phần mười: $\\approx -3{,}1$.<br>b) Đến hàng phần trăm: $\\approx -3{,}14$.<br>c) Đến hàng phần nghìn: $\\approx -3{,}142$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Ước lượng chi phí mua sắm vật dụng trước khi đến quầy thanh toán.
b) Nội dung: Bạn Nam mua 3 cuốn sách giá $29\\,500$ đồng$/$cuốn và một hộp bút giá $41\\,000$ đồng. Ước lượng số tiền Nam cần mang theo.
c) Sản phẩm: Câu trả lời trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán ước lượng tiền mua sách vở của Nam.<br>- **HS:** Đọc đề và nhẩm tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm tròn: $29\\,500 \\approx 30\\,000$; $41\\,000 \\approx 40\\,000$. Tổng tiền ước lượng: $3 \\cdot 30\\,000 + 40\\,000 = 130\\,000$ đồng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng: Nam cần mang khoảng $130\\,000$ đồng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và chốt lại kỹ năng ước lượng trong cuộc sống. | Số tiền ước lượng Nam cần mang là:<br>$$3 \\cdot 30\\,000 + 40\\,000 = 130\\,000\\text{ (đồng)}$$<br>Nam cần mang khoảng $130\\,000$ đồng. |
"""
    },
    {
        "filename": "12_KHBD_Toan6_OnTapGiuaHK2_Tiet71-72.md",
        "header": "TIẾT 71, 72 - ÔN TẬP GIỮA HỌC KÌ II (SỐ HỌC)\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 71, 72 - ÔN TẬP GIỮA HỌC KÌ II (SỐ HỌC)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức trọng tâm từ đầu HKII đến giữa HKII: Phân số (định nghĩa, so sánh, 4 phép tính, hỗn số, hai bài toán về phân số) và Số thập phân (định nghĩa, so sánh, tính toán, làm tròn).
- Rèn luyện kỹ năng giải các bài toán tổng hợp phối hợp cả phân số và số thập phân.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ sơ đồ tư duy hệ thống kiến thức ôn tập giữa kì; tự rà soát các dạng bài tập mình còn hay sai sót.
- Giao tiếp và hợp tác: Tích cực thảo luận nhóm, chữa bài và hỗ trợ bạn cùng tiến bộ.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lựa chọn linh hoạt chuyển đổi giữa phân số và số thập phân để thực hiện phép tính hợp lí nhất.
- Năng lực giải quyết vấn đề toán học: Giải các bài toán thực tế có nhiều bước tính toán trung gian.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay để kiểm tra nhanh kết quả toàn bộ đề cương ôn tập giữa kì II.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Sử dụng AI để tổng hợp ngân hàng đề trắc nghiệm ôn tập giữa học kì II môn Toán lớp 6.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, tỉ mỉ, tác phong làm bài thi nghiêm túc.
- Tự tin, sẵn sàng tâm thế bước vào bài kiểm tra định kì giữa HKII.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 71-72 (vector 300 DPI), tivi/máy chiếu, đề cương ôn tập.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt tinh thần ôn tập qua trò chơi trắc nghiệm "Rung chuông vàng".
b) Nội dung: Trả lời nhanh 5 câu hỏi trắc nghiệm lý thuyết trọng tâm.
c) Sản phẩm: Bảng chọn đáp án của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến luật chơi "Rung chuông vàng" với 5 câu hỏi nhanh.<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi đáp án sau mỗi câu hỏi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cả lớp cùng đối chiếu đáp án đúng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương các học sinh xuất sắc và dẫn vào bài ôn tập. | Bảng đáp án trắc nghiệm chuẩn xác. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (20 phút)
a) Mục tiêu: Hệ thống hóa toàn diện các kiến thức trọng tâm nửa đầu HKII qua Sơ đồ tư duy vector 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 71-72; nhắc lại các nhánh kiến thức và công thức.

![Sơ đồ tư duy Ôn tập giữa HK2 Tiết 71-72](khbd-ill:mindmap-toan6-tiet71-72)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Ôn tập giữa kì II. Yêu cầu HS phân tích hai khối kiến thức lớn: 1. Phân số; 2. Số thập phân.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm 4 hoàn thiện bảng tóm tắt công thức cốt lõi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện nhóm thuyết trình tóm tắt các điểm cần nhớ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh các bẫy thường gặp: Lỗi quên đổi dấu mẫu âm, nhầm lẫn giữa hai bài toán phân số, nhầm lẫn vị trí dấu phẩy. | **Hệ thống lý thuyết giữa kì II:**<br>1. Phân số: Phân số bằng nhau, quy đồng so sánh, 4 phép tính, hai bài toán phân số.<br>2. Số thập phân: Cấu tạo số đối, quy tắc so sánh số âm, tính toán cộng trừ nhân chia có dấu âm, làm tròn và ước lượng. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Luyện tập các dạng bài trọng tâm: Tính hợp lí, tìm $x$ và bài toán thực tế.
b) Nội dung: Đề ôn tập giữa kì trong tài liệu đề cương.
c) Sản phẩm: Bài làm chi tiết của học sinh trên bảng và trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 3 dạng bài tập ôn tập:<br>  Dạng 1 (Tính hợp lí): $A = \\left(\\frac{-5}{8}\\right) \\cdot \\frac{5}{12} + \\left(\\frac{-5}{8}\\right) \\cdot \\frac{7}{12} + 2\\frac{5}{8}$.<br>  Dạng 2 (Tìm $x$): $\\frac{2}{3} \\cdot x - \\frac{1}{2} = \\frac{-3}{4}$.<br>  Dạng 3 (Toán thực tế): Một khu vườn có diện tích $360\\text{ m}^2$. Người ta dùng $\\frac{4}{9}$ diện tích để trồng hoa, $\\frac{3}{5}$ diện tích còn lại để trồng rau. Tính diện tích phần đất còn lại.<br>- **HS:** Nhận đề.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài nghiêm túc vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS lên bảng chữa 3 dạng bài.<br>- Dạng 1: $A = \\left(\\frac{-5}{8}\\right) \\cdot \\left(\\frac{5}{12} + \\frac{7}{12}\\right) + \\frac{21}{8} = \\frac{-5}{8} \\cdot 1 + \\frac{21}{8} = \\frac{16}{8} = 2$.<br>- Dạng 2: $\\frac{2}{3} \\cdot x = \\frac{-3}{4} + \\frac{1}{2} = \\frac{-1}{4} \\Rightarrow x = \\frac{-1}{4} : \\frac{2}{3} = \\frac{-3}{8}$.<br>- Dạng 3: Diện tích trồng hoa: $360 \\cdot \\frac{4}{9} = 160\\text{ m}^2$. Diện tích còn lại sau khi trồng hoa: $360 - 160 = 200\\text{ m}^2$. Diện tích trồng rau: $200 \\cdot \\frac{3}{5} = 120\\text{ m}^2$. Diện tích còn lại: $200 - 120 = 80\\text{ m}^2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa: Lưu ý kết luận rõ $x = \\frac{-3}{8}$, không kết luận tập nghiệm. | **Đáp số bài tập:**<br>**Dạng 1:**<br>$$A = \\frac{-5}{8} \\cdot 1 + \\frac{21}{8} = \\frac{16}{8} = 2$$<br>**Dạng 2:**<br>$$\\frac{2}{3} \\cdot x = \\frac{-1}{4} \\Rightarrow x = \\frac{-3}{8}$$<br>Vậy $x = \\frac{-3}{8}$.<br>**Dạng 3:**<br>- Diện tích trồng hoa: $160\\text{ m}^2$.<br>- Diện tích trồng rau: $120\\text{ m}^2$.<br>- Diện tích còn lại: $80\\text{ m}^2$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Rèn luyện kỹ năng phân bổ thời gian và chiến thuật làm bài kiểm tra trắc nghiệm kết hợp tự luận.
b) Nội dung: Giáo viên dặn dò các lưu ý khi làm bài kiểm tra giữa học kì II.
c) Sản phẩm: Kế hoạch ôn tập cá nhân của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn chiến thuật làm bài: Đọc kĩ đề, làm câu dễ trước, kiểm tra lại phép tính bằng máy tính cầm tay, trình bày tự luận rõ ràng từng bước.<br>- **HS:** Lắng nghe và ghi chú.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi lại các điểm cần lưu ý vào trang đầu vở ôn tập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu các thắc mắc về dạng bài tập còn chưa rõ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giải đáp thắc mắc, chúc cả lớp đạt kết quả cao trong bài kiểm tra giữa kì. | Chiến thuật làm bài: Đọc kĩ đề, làm câu dễ trước, cẩn thận dấu âm và rút gọn phân số tối giản. |
"""
    },
    {
        "filename": "13_KHBD_Toan6_KiemTraGiuaHK2_Tiet73.md",
        "header": "TIẾT 73 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (SỐ HỌC)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 73 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (SỐ HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ nắm vững chuẩn kiến thức kĩ năng của học sinh về Chương VI (Phân số) và Chương VII (Số thập phân đến Tiết 70).
- Đánh giá khả năng vận dụng quy tắc tính toán, tìm thành phần chưa biết và giải quyết vấn đề thực tế.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Độc lập làm bài, trung thực, tự giác tuân thủ nghiêm túc quy chế kiểm tra.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày bài giải logic, có căn cứ lập luận chính xác.
- Năng lực giải quyết vấn đề toán học: Chuyển đổi ngôn ngữ thực tế sang mô hình toán học số học để tính toán chính xác.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay đúng quy định trong phòng thi để kiểm tra kết quả tính toán.***

## 3. Về phẩm chất
- Trung thực, nghiêm túc, không gian lận trong kiểm tra.
- Tinh thần trách nhiệm đối với kết quả học tập của bản thân.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận và bản đặc tả chuẩn Bộ GD&ĐT (Trắc nghiệm 30% - Tự luận 70%), đáp án và biểu điểm.
2. Học sinh: Giấy kiểm tra, bút mực, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (3 phút)
a) Mục tiêu: Ổn định tổ chức, tạo tâm thế bình tĩnh, tự tin cho học sinh trước khi làm bài.
b) Nội dung: Nhắc nhở quy chế thi, phát đề kiểm tra.
c) Sản phẩm: Học sinh nhận đề kiểm tra.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định chỗ ngồi, quán triệt quy chế phòng kiểm tra. Phát đề kiểm tra tới từng học sinh.<br>- **HS:** Nhận đề, kiểm tra số trang và độ rõ nét của đề.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Điền đầy đủ thông tin: Họ tên, lớp, số báo danh vào giấy làm bài.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo nếu đề bị mờ hoặc thiếu trang.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Ra hiệu lệnh bắt đầu tính giờ làm bài. | 100% học sinh ổn định chỗ ngồi, có đề thi nguyên vẹn, rõ nét. |

## B. THỰC HIỆN BÀI KIỂM TRA (HOẠT ĐỘNG 2) (40 phút)
a) Mục tiêu: Độc lập làm bài kiểm tra trong thời gian quy định.
b) Nội dung: Học sinh làm bài kiểm tra theo cấu trúc đề in sẵn.
c) Sản phẩm: Bài làm hoàn thiện trên giấy thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Theo dõi, giám sát phòng thi, bao quát đảm bảo tính nghiêm túc, công bằng, khách quan.<br>- **HS:** Độc lập làm bài, không trao đổi, không quay cóp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm phần Trắc nghiệm (tô/khoanh đáp án đúng), sau đó làm phần Tự luận (trình bày chi tiết từng bước tính).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Nhắc nhở thời gian còn lại: 15 phút, 5 phút để học sinh rà soát lại bài làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **HS:** Kiểm tra lại họ tên, các phép biến đổi dấu âm và kết luận nghiệm. | Học sinh làm bài nghiêm túc, độc lập, chất lượng. |

## C. THU BÀI VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (2 phút)
a) Mục tiêu: Thu bài đủ số lượng và nhận xét ý thức kiểm tra của lớp.
b) Nội dung: Thu giấy thi theo danh sách lớp.
c) Sản phẩm: Tập bài thi đầy đủ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ra hiệu lệnh hết giờ làm bài, yêu cầu tất cả học sinh dừng bút, nộp bài theo dãy.<br>- **HS:** Dừng bút, sắp xếp bài làm theo thứ tự nộp lên giáo viên.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Đếm và kiểm tra số lượng bài thu được.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp báo cáo sĩ số làm bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét tinh thần, thái độ làm bài của cả lớp; dặn dò chuẩn bị cho Bài 31 ở tiết sau. | Thu đủ 100% bài kiểm tra theo sĩ số lớp. |
"""
    },
    {
        "filename": "14_KHBD_Toan6_Bai31_MotSoBaiToanVeTiSoVaTiSoPhanTram_Tiet74-76.md",
        "header": "TIẾT 74, 75, 76 - BÀI 31: MỘT SỐ BÀI TOÁN VỀ TỈ SỐ VÀ TỈ SỐ PHẦN TRĂM\n*Thời lượng thực hiện: 03 tiết (135 phút)*",
        "md": """TIẾT 74, 75, 76 - BÀI 31: MỘT SỐ BÀI TOÁN VỀ TỈ SỐ VÀ TỈ SỐ PHẦN TRĂM
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết tỉ số của hai số $a$ và $b$ ($b \\neq 0$) là thương của phép chia $a$ cho $b$, kí hiệu là $\\frac{a}{b}$ hoặc $a : b$.
- Hiểu và tính được tỉ số phần trăm của hai số: $\\frac{a \\cdot 100}{b}\\%$.
- Vận dụng thành thạo hai bài toán về tỉ số phần trăm:
  + Tìm giá trị phần trăm của một số: Muốn tìm $m\\%$ của số $a$, ta tính $a \\cdot \\frac{m}{100}$.
  + Tìm một số khi biết giá trị phần trăm của nó: Muốn tìm một số biết $m\\%$ của nó bằng $b$, ta tính $b : \\frac{m}{100}$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tìm kiếm các bảng số liệu tỉ số phần trăm trên báo chí, bao bì sản phẩm hàng hóa.
- Giao tiếp và hợp tác: Làm việc nhóm phân tích biểu đồ phần trăm và tính toán giá trị thực tế.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh hiệu quả kinh doanh, mức tăng trưởng dựa vào tỉ số phần trăm.
- Năng lực mô hình hoá toán học: Giải bài toán tính tiền lãi gửi tiết kiệm ngân hàng, tính giá trị sau khi giảm giá hoặc tăng thuế VAT.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phím phần trăm (%) trên máy tính cầm tay để tính toán tự động số tiền giảm giá hóa đơn.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh sử dụng AI để tra cứu tỉ lệ lạm phát, tỉ lệ tăng trưởng GDP của Việt Nam trong những năm gần đây.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng trong tính toán tài chính và kinh tế.
- Nhận thức được giá trị của việc tiết kiệm và quản lý chi tiêu thông minh.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, bảng biểu thị tỉ số phần trăm, máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay, hóa đơn mua hàng mẫu.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt tình huống từ các biển quảng cáo khuyến mãi "Giảm giá 20%", "Sale 50%" để tạo hứng thú học tập.
b) Nội dung: Quan sát hình ảnh cửa hàng thời trang giảm giá và trả lời câu hỏi: Giảm giá $20\\%$ có nghĩa là gì?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh biển giảm giá $20\\%$. Nếu một chiếc áo có giá niêm yết $200\\,000$ đồng thì người mua được giảm bao nhiêu tiền?<br>- **HS:** Quan sát và tính nhẩm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm: Giảm $20$ trên mỗi $100$, nên $200\\,000$ được giảm $40\\,000$ đồng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và giới thiệu bài học: Bài 31 sẽ giúp chúng ta tính toán chính xác mọi bài toán về tỉ số và tỉ số phần trăm. | Giảm giá $20\\%$ nghĩa là cứ $100$ đồng tiền hàng thì được bớt $20$ đồng. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (95 phút)
### Hoạt động 2.1: Tỉ số và tỉ số phần trăm (30 phút)
a) Mục tiêu: HS nắm vững khái niệm tỉ số của hai số và công thức tính tỉ số phần trăm.
b) Nội dung: Tỉ số $\\frac{a}{b}$ và tỉ số phần trăm $\\frac{a}{b} \\cdot 100\\%$.
c) Sản phẩm: Lời giải bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu khái niệm: Thương trong phép chia số $a$ cho số $b$ ($b \\neq 0$) gọi là tỉ số của $a$ và $b$, kí hiệu là $\\frac{a}{b}$ hoặc $a : b$. Tỉ số phần trăm của $a$ và $b$ là $\\frac{a \\cdot 100}{b}\\%$.<br>- **HS:** Tiếp nhận định nghĩa.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính tỉ số phần trăm của $15$ và $40$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Tỉ số phần trăm là: $\\frac{15 \\cdot 100}{40}\\% = \\frac{1500}{40}\\% = 37{,}5\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy tắc tính tỉ số phần trăm. | **1. Tỉ số và tỉ số phần trăm:**<br>- Tỉ số của $a$ và $b$ ($b \\neq 0$) là $\\frac{a}{b}$ hoặc $a : b$.<br>- Tỉ số phần trăm của $a$ và $b$ là:<br>$$\\frac{a \\cdot 100}{b}\\%$$<br>- Ví dụ: Tỉ số phần trăm của $15$ và $40$ là $37{,}5\\%$. |

### Hoạt động 2.2: Hai bài toán về tỉ số phần trăm (65 phút)
a) Mục tiêu: Vận dụng thành thạo bài toán tìm giá trị phần trăm của một số và tìm số khi biết giá trị phần trăm.
b) Nội dung: Công thức tính $m\\%$ của số $a$ ($a \\cdot \\frac{m}{100}$) và tìm số biết $m\\%$ là $b$ ($b : \\frac{m}{100}$).
c) Sản phẩm: Lời giải các ví dụ trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu hai bài toán:<br>  + Bài toán 1: Tìm $m\\%$ của $a$: Tính $a \\cdot \\frac{m}{100}$.<br>  + Bài toán 2: Tìm một số biết $m\\%$ của nó bằng $b$: Tính $b : \\frac{m}{100}$.<br>- **HS:** Ghi nhận công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải 2 ví dụ:<br>  Ví dụ 1: Tìm $15\\%$ của $60\\text{ kg}$.<br>  Ví dụ 2: Tìm một số biết $25\\%$ của nó bằng $50$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Ví dụ 1: $60 \\cdot \\frac{15}{100} = 9\\text{ kg}$. Ví dụ 2: $50 : \\frac{25}{100} = 50 \\cdot \\frac{100}{25} = 200$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Đây là sự mở rộng trực tiếp của "Hai bài toán về phân số" với phân số có mẫu là $100$. | **2. Hai bài toán về tỉ số phần trăm:**<br>- **Bài toán 1:** Tìm $m\\%$ của số $a$:<br>$$a \\cdot \\frac{m}{100}$$<br>- **Bài toán 2:** Tìm số khi biết $m\\%$ của nó bằng $b$:<br>$$b : \\frac{m}{100} = \\frac{b \\cdot 100}{m}$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (25 phút)
a) Mục tiêu: Giải quyết các bài toán tính toán giá tiền sau khuyến mãi và bài toán lãi suất tiền gửi tiết kiệm.
b) Nội dung: Bài 7.18, 7.19 SGK trang 40.
c) Sản phẩm: Lời giải chi tiết trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Bác An gửi tiết kiệm $50\\,000\\,000$ đồng vào ngân hàng với kì hạn một năm, lãi suất $6\\%/\\text{năm}$. Hỏi sau một năm bác An nhận được bao nhiêu tiền cả gốc lẫn lãi?<br>- **HS:** Nhận đề và phân tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính tiền lãi sau 1 năm: $50\\,000\\,000 \\cdot 6\\%$. Sau đó cộng với tiền gốc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br>- Tiền lãi sau 1 năm: $50\\,000\\,000 \\cdot \\frac{6}{100} = 3\\,000\\,000$ đồng.<br>- Tổng tiền nhận được: $50\\,000\\,000 + 3\\,000\\,000 = 53\\,000\\,000$ đồng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và lưu ý có thể tính gộp: $50\\,000\\,000 \\cdot (1 + 6\\%) = 53\\,000\\,000$ đồng. | **Bài giải:**<br>- Số tiền lãi sau một năm bác An nhận được là:<br>$$50\\,000\\,000 \\cdot \\frac{6}{100} = 3\\,000\\,000\\text{ (đồng)}$$<br>- Tổng số tiền cả gốc và lãi bác An nhận được sau một năm là:<br>$$50\\,000\\,000 + 3\\,000\\,000 = 53\\,000\\,000\\text{ (đồng)}$$<br>Đáp số: $53\\,000\\,000$ đồng. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Vận dụng kiến thức tỉ lệ phần trăm tính nồng độ dung dịch muối thực tế.
b) Nội dung: Hòa tan $20\\text{ g}$ muối vào $180\\text{ g}$ nước tinh khiết. Tính tỉ số phần trăm của muối trong dung dịch nước muối thu được.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu đề bài toán nồng độ muối. Lưu ý: Khối lượng dung dịch bằng khối lượng muối cộng khối lượng nước.<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khối lượng dung dịch: $20 + 180 = 200\\text{ g}$. Tỉ số phần trăm muối: $\\frac{20 \\cdot 100}{200}\\% = 10\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu đáp số $10\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao tính tích hợp giữa Toán học và Hóa học, Sinh học. | Khối lượng dung dịch nước muối là:<br>$$20 + 180 = 200\\text{ (g)}$$<br>Tỉ số phần trăm của muối trong dung dịch là:<br>$$\\frac{20 \\cdot 100}{200}\\% = 10\\%$$<br>Đáp số: $10\\%$. |
"""
    },
    {
        "filename": "15_KHBD_Toan6_LuyenTapChung_Tiet77-78.md",
        "header": "TIẾT 77, 78 - LUYỆN TẬP CHUNG (TRANG 41)\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 77, 78 - LUYỆN TẬP CHUNG (TRANG 41)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và nâng cao kỹ năng tính tỉ số, tỉ số phần trăm và giải thành thạo hai bài toán về tỉ số phần trăm.
- Phối hợp linh hoạt các phép tính số thập phân, phân số và tỉ số phần trăm trong giải toán thực tiễn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa sơ đồ phân biệt bài toán tìm $m\\%$ của một số và tìm số khi biết $m\\%$ của nó.
- Giao tiếp và hợp tác: Tương tác nhóm giải bài toán kinh tế gia đình, lập kế hoạch chi tiêu.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh hiệu quả của các chương trình khuyến mãi (mua 3 tặng 1 hay giảm giá $25\\%$) bằng lập luận toán học.
- Năng lực mô hình hoá toán học: Chuyển các thông tin quảng cáo, tài chính thành bài toán tỉ số phần trăm để ra quyết định tiêu dùng tối ưu.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng bảng tính điện tử hoặc máy tính cầm tay để lập bảng so sánh mức giá sau khi áp dụng các mã giảm giá khác nhau.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI giải thích khái niệm lãi suất kép và mô phỏng sự tăng trưởng tiền gửi theo thời gian.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn thận và thói quen tính toán có căn cứ khoa học.
- Hình thành ý thức người tiêu dùng thông thái trong thời đại số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 77-78 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khởi động tinh thần học tập qua câu hỏi thực tế so sánh hai chương trình khuyến mãi.
b) Nội dung: Cửa hàng A giảm giá $20\\%$, cửa hàng B mua 4 tặng 1 (mua 4 món trả tiền 4 món nhưng nhận được 5 món). Chương trình nào giảm giá nhiều hơn?
c) Sản phẩm: Thảo luận nhanh của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi tình huống mua sắm khuyến mãi.<br>- **HS:** Suy nghĩ và trao đổi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cửa hàng B: Nhận 5 món trả tiền 4 món, mức giảm là $\\frac{1}{5} = 20\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Cả hai chương trình đều giảm mức tương đương $20\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tư duy sắc bén của học sinh và dẫn dắt vào bài luyện tập. | Cả hai chương trình khuyến mãi đều có mức giảm giá tương đương là $20\\%$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (20 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức về tỉ số và tỉ số phần trăm thông qua Sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 77-78; phân tích mối quan hệ giữa các nhánh.

![Sơ đồ tư duy Luyện tập chung Tiết 77-78](khbd-ill:mindmap-toan6-tiet77-78)

c) Sản phẩm: Sơ đồ tư duy ghi chép trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 77-78. Yêu cầu học sinh nhắc lại 3 nội dung trọng tâm: 1. Khái niệm tỉ số và tỉ số phần trăm; 2. Tìm giá trị phần trăm của một số; 3. Tìm một số khi biết giá trị phần trăm.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoạt động nhóm đôi tóm tắt công thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS xung phong lên bảng điền công thức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa sơ đồ kiến thức. | **Hệ thống kiến thức trọng tâm:**<br>1. Tỉ số phần trăm của $a$ và $b$: $\\frac{a \\cdot 100}{b}\\%$.<br>2. Tìm $m\\%$ của $a$: Lấy $a \\cdot \\frac{m}{100}$.<br>3. Tìm số biết $m\\%$ của nó bằng $b$: Lấy $b : \\frac{m}{100}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Giải thành thạo các bài toán lời văn thực tế có nhiều bước tính toán phức hợp.
b) Nội dung: Bài 7.21, 7.22, 7.23 SGK trang 41, 42.
c) Sản phẩm: Lời giải hoàn thiện trên bảng và trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài tập:<br>  Bài 1: Một siêu thị điện máy niêm yết giá chiếc tivi là $12\\,000\\,000$ đồng. Nhân dịp khai trương, siêu thị giảm giá $15\\%$. Nếu khách hàng thanh toán qua ví điện tử thì được giảm thêm $2\\%$ trên giá đã giảm. Hỏi người mua phải trả bao nhiêu tiền?<br>  Bài 2: Khối lượng quặng sắt chứa $65\\%$ sắt nguyên chất. Hỏi cần bao nhiêu tấn quặng để luyện được $13$ tấn sắt nguyên chất?<br>- **HS:** Nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br>- Bài 1: Giá sau khi giảm $15\\%$: $12\\,000\\,000 \\cdot (100\\% - 15\\%) = 10\\,200\\,000$ đồng. Giá thanh toán qua ví điện tử: $10\\,200\\,000 \\cdot (100\\% - 2\\%) = 9\\,996\\,000$ đồng.<br>- Bài 2: Khối lượng quặng cần là: $13 : 65\\% = 13 : \\frac{65}{100} = 13 \\cdot \\frac{100}{65} = 20$ (tấn).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao cách giải gộp thông minh và tính chính xác của học sinh. | **Lời giải chi tiết:**<br>**Bài 1:**<br>- Giá tivi sau khi giảm $15\\%$ là:<br>$$12\\,000\\,000 \\cdot (1 - 0{,}15) = 10\\,200\\,000\\text{ (đồng)}$$<br>- Số tiền người mua phải thanh toán qua ví điện tử là:<br>$$10\\,200\\,000 \\cdot (1 - 0{,}02) = 9\\,996\\,000\\text{ (đồng)}$$<br>Đáp số: $9\\,996\\,000$ đồng.<br>**Bài 2:**<br>Số tấn quặng sắt cần dùng là:<br>$$13 : 65\\% = 13 : \\frac{65}{100} = 20\\text{ (tấn)}$$<br>Đáp số: $20$ tấn quặng. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Vận dụng tỉ số phần trăm tính chỉ số khối cơ thể (BMI) và tỷ lệ mỡ cơ thể.
b) Nội dung: Tìm hiểu các chỉ số sức khỏe của lứa tuổi học sinh trung học.
c) Sản phẩm: Báo cáo ngắn của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cách đọc các tỉ số phần trăm dinh dưỡng trên nhãn bao bì sữa và bánh kẹo.<br>- **HS:** Đọc các nhãn bao bì đã chuẩn bị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính toán lượng đường, chất béo theo khối lượng hộp sữa.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chia sẻ thông tin trong nhóm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giáo dục thói quen ăn uống lành mạnh, hạn chế đồ uống quá nhiều đường. | Đọc và phân tích thành thạo các tỉ số phần trăm trên bao bì sản phẩm dinh dưỡng hàng ngày. |
"""
    },
    {
        "filename": "16_KHBD_Toan6_BaiTapCuoiChuong7_Tiet79-80.md",
        "header": "TIẾT 79, 80 - BÀI TẬP CUỐI CHƯƠNG VII (TRANG 43)\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 79, 80 - BÀI TẬP CUỐI CHƯƠNG VII (TRANG 43)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Chương VII: Số thập phân, so sánh số thập phân, 4 phép tính với số thập phân, làm tròn và ước lượng, tỉ số và tỉ số phần trăm.
- Vận dụng kiến thức toàn chương để giải quyết các bài tập tổng hợp và các bài toán thực tiễn đời sống.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng kết kiến thức toàn chương qua sơ đồ tư duy; chủ động rà soát và sửa chữa các lỗi sai hay gặp.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải các bài toán kinh tế, tài chính trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa quy tắc, lựa chọn công thức giải toán chính xác và ngắn gọn nhất.
- Năng lực giải quyết vấn đề toán học: Mô hình hóa các bài toán kinh tế thực tế nhiều bước thành chuỗi các phép tính số thập phân.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay để kiểm tra kết quả tính toán của toàn bộ đề bài tập ôn tập cuối chương VII.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Ứng dụng trợ lý AI tổng hợp các bài toán thực tế đoạt giải sáng tạo liên quan đến tính toán số thập phân và phần trăm.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật và tác phong khoa học trong học tập.
- Nâng cao ý thức tiết kiệm và quản lý tài chính cá nhân phù hợp với lứa tuổi học sinh.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 79-80 (vector 300 DPI), tivi/máy chiếu, phiếu học tập.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập nhanh các công thức trọng tâm qua trò chơi "Ai là triệu phú Toán học".
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm kiến thức cốt lõi chương VII.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu hỏi trắc nghiệm.<br>- **HS:** Chuẩn bị bảng con ghi đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ đáp án sau hiệu lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giải thích ngắn gọn lý do chọn đáp án.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và dẫn vào bài ôn tập tổng kết chương VII. | Bảng đáp án trắc nghiệm chuẩn xác của học sinh. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (20 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ cấu trúc kiến thức Chương VII bằng Sơ đồ tư duy tổng hợp 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 79-80; hoàn thiện bức tranh tổng thể về số thập phân và tỉ số phần trăm.

![Sơ đồ tư duy Bài tập cuối chương VII Tiết 79-80](khbd-ill:mindmap-toan6-tiet79-80)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy tổng thể Chương VII. Hướng dẫn HS hệ thống theo 4 nhánh lớn: 1. Khái niệm & So sánh số thập phân; 2. Bốn phép tính số thập phân; 3. Làm tròn và ước lượng; 4. Tỉ số và tỉ số phần trăm.<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành các chỗ trống trong phiếu tóm tắt lý thuyết.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS đứng tại chỗ trình bày tổng quan cấu trúc chương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại các lưu ý quan trọng: Quy tắc dấu âm, quy tắc làm tròn số và hai bài toán về phần trăm. | **Tổng kết lý thuyết Chương VII:**<br>- Số thập phân: Cấu tạo, số đối, so sánh hai số âm.<br>- Bốn phép tính: Quy tắc dấu, tính chất phân phối để tính nhanh.<br>- Làm tròn: Nhìn chữ số sau hàng làm tròn ($< 5$ giữ nguyên, $\\ge 5$ tăng $1$).<br>- Tỉ số phần trăm: $\\frac{a \\cdot 100}{b}\\%$; $a \\cdot \\frac{m}{100}$; $b : \\frac{m}{100}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Luyện tập toàn diện các bài tập trắc nghiệm và tự luận cuối chương trong SGK.
b) Nội dung: Giải Bài 7.24, 7.25, 7.26, 7.28 SGK trang 43, 44.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài toán tổng hợp:<br>  Bài 1: Tính hợp lí: $Q = 3{,}75 \\cdot (-4{,}2) + 6{,}25 \\cdot (-4{,}2)$.<br>  Bài 2: Một người gửi tiết kiệm $100\\,000\\,000$ đồng với lãi suất $6{,}5\\%/\\text{năm}$. Sau một năm người đó rút toàn bộ gốc và lãi rồi dùng $40\\%$ số tiền đó để mua sắm vật dụng gia đình. Hỏi người đó còn lại bao nhiêu tiền?<br>- **HS:** Nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện giải bài tập độc lập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng:<br>- Bài 1: $Q = (-4{,}2) \\cdot (3{,}75 + 6{,}25) = (-4{,}2) \\cdot 10 = -42$.<br>- Bài 2: Tiền sau 1 năm: $100\\,000\\,000 \\cdot (1 + 0{,}065) = 106\\,500\\,000$ đồng. Số tiền còn lại: $106\\,500\\,000 \\cdot (1 - 0{,}4) = 106\\,500\\,000 \\cdot 0{,}6 = 63\\,900\\,000$ đồng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa: Lời giải chính xác, các bước tính toán logic, chặt chẽ. | **Lời giải bài tập tổng hợp:**<br>**Bài 1:**<br>$$Q = (-4{,}2) \\cdot (3{,}75 + 6{,}25) = (-4{,}2) \\cdot 10 = -42$$<br>**Bài 2:**<br>- Tổng số tiền sau 1 năm (cả gốc và lãi) là:<br>$$100\\,000\\,000 \\cdot (1 + 0{,}065) = 106\\,500\\,000\\text{ (đồng)}$$<br>- Số tiền người đó còn lại sau khi mua sắm là:<br>$$106\\,500\\,000 \\cdot (1 - 0{,}4) = 63\\,900\\,000\\text{ (đồng)}$$<br>Đáp số: $63\\,900\\,000$ đồng. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Vận dụng kiến thức tổng hợp giải bài toán thực tế về tính chỉ số ô nhiễm không khí hoặc mức tiêu thụ năng lượng.
b) Nội dung: Tính tỉ lệ tiết kiệm điện năng của bóng đèn LED so với bóng đèn dây tóc.
c) Sản phẩm: Báo cáo ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Một bóng đèn dây tóc tiêu thụ $60\\text{ W}$, trong khi một bóng đèn LED có độ sáng tương đương chỉ tiêu thụ $9\\text{ W}$. Hỏi bóng đèn LED tiết kiệm được bao nhiêu phần trăm điện năng so với bóng đèn dây tóc?<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lượng điện tiết kiệm: $60 - 9 = 51\\text{ W}$. Tỉ lệ phần trăm tiết kiệm: $\\frac{51 \\cdot 100}{60}\\% = 85\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng: Tiết kiệm được $85\\%$ điện năng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên truyền ý thức tiết kiệm năng lượng điện và bảo vệ môi trường trong sinh hoạt gia đình. | Điện năng tiết kiệm được là: $60 - 9 = 51\\text{ (W)}$.<br>Tỉ lệ phần trăm điện năng tiết kiệm được là:<br>$$\\frac{51 \\cdot 100}{60}\\% = 85\\%$$<br>Đáp số: Tiết kiệm $85\\%$ điện năng. |
"""
    }
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print("Hoàn tất tạo 8 KHBD Chương VII: Số thập phân (Tiết 66 - 80)!")
