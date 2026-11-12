# -*- coding: utf-8 -*-
"""
Script sinh 5 KHBD Chương VII: Tần số và tần số tương đối (Tiết 59 - 68) - Toán 9 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan9"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    # 10: Bài 22 (Tiết 59-60)
    {
        "filename": "10_KHBD_Toan9_Bai22_BangTanSoVaBieuDoTanSo_Tiet59-60.md",
        "md": """TIẾT 59, 60 - BÀI 22: BẢNG TẦN SỐ VÀ BIỂU ĐỒ TẦN SỐ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm tần số của một giá trị trong mẫu số liệu: Số lần xuất hiện của giá trị đó trong tập dữ liệu khảo sát (kí hiệu là $m$ hoặc $n$).
- Lập được bảng tần số cho mẫu dữ liệu thống kê rời rạc.
- Nhận biết và vẽ được biểu đồ tần số: Biểu đồ cột (chiều cao cột thể hiện tần số) và Biểu đồ đoạn thẳng (nối các điểm tọa độ biểu diễn giá trị và tần số).
- Đọc, giải thích và rút ra các nhận xét thống kê quan trọng từ bảng tần số và biểu đồ tần số.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác thu thập, kiểm đếm và phân loại dữ liệu thống kê một cách khoa học.
- Giao tiếp và hợp tác: Làm việc nhóm khảo sát dữ liệu thực tế trong lớp học (chiều cao, sở thích môn học, điểm kiểm tra) và thống kê kết quả.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh quy mô và tần suất xuất hiện của các đối tượng qua biểu đồ trực quan.
- Năng lực mô hình hoá toán học: Chuyển đổi dữ liệu thống kê thô thành bảng biểu và biểu đồ trực quan giúp đưa ra quyết định.

c) Năng lực số (NLS):
- ***3.1.TC2a: Sử dụng phần mềm bảng tính để nhập dữ liệu và tự động tạo biểu đồ tần số từ bảng số liệu cho trước; 5.3.TC2a: Sử dụng bản đồ số, tư liệu số hoặc phần mềm sơ đồ tư duy (Canva/Mindmap) để khai thác tư liệu, hệ thống hóa kiến thức và trình bày sản phẩm trong bài Bảng tần số và biểu đồ tần số; học sinh đối chiếu với SGK và hoàn thành sản phẩm học tập.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn thận, chính xác khi thu thập và kiểm đếm dữ liệu thống kê.
- Tinh thần khách quan, không làm sai lệch số liệu thực tế.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2 Kết nối tri thức, KHBD, bảng tính Excel chiếu trên màn hình, máy chiếu.
2. Học sinh: SGK, vở ghi, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt tư duy về việc sắp xếp một danh sách dài các số liệu điểm kiểm tra thành bảng gọn gàng.
b) Nội dung: Cho danh sách điểm kiểm tra môn Toán của 20 học sinh: $8, 7, 9, 8, 6, 8, 10, 7, 8, 9, 6, 7, 8, 9, 10, 8, 7, 8, 9, 7$. Làm thế nào để biết có bao nhiêu bạn đạt điểm $8$?
c) Sản phẩm: Bảng đếm của học sinh: Có 7 bạn đạt điểm 8.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu dãy điểm số của 20 học sinh. Đặt câu hỏi: Làm sao để đếm nhanh số lượng từng loại điểm?<br>- **HS:** Quan sát và đếm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đếm số lần xuất hiện của từng điểm số $6, 7, 8, 9, 10$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Điểm 6 xuất hiện 2 lần, điểm 7 có 5 lần, điểm 8 có 7 lần, điểm 9 có 4 lần, điểm 10 có 2 lần.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Số lần xuất hiện của mỗi giá trị được gọi là tần số của giá trị đó. Bảng sắp xếp như vậy gọi là bảng tần số. | Giới thiệu khái niệm tần số và bảng tần số qua tình huống thống kê điểm số. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Khái niệm tần số và lập bảng tần số (35 phút)
a) Mục tiêu: Nắm vững định nghĩa tần số $m$, quy mô mẫu $N = \\sum m_i$ và lập bảng tần số dạng ngang/dọc.
b) Nội dung: Định nghĩa, kí hiệu và cách lập bảng tần số từ dữ liệu điều tra thực tế.
c) Sản phẩm: Bảng tần số hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Số lần xuất hiện của một giá trị trong mẫu dữ liệu được gọi là tần số của giá trị đó, kí hiệu là $m$. Bảng gồm hai dòng (hoặc hai cột): Dòng trên ghi các giá trị khác nhau $x_i$, dòng dưới ghi các tần số tương ứng $m_i$ gọi là bảng tần số.<br>Tổng các tần số bằng kích thước mẫu: $N = m_1 + m_2 + \\dots + m_k$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lập bảng tần số cho dữ liệu điểm số khởi động.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Kiểm tra tổng $N = 2 + 5 + 7 + 4 + 2 = 20$. Khớp với sĩ số 20.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Tổng các tần số luôn luôn phải bằng kích thước mẫu $N$. | **1. Tần số và Bảng tần số:**<br>- Tần số $m$: Số lần xuất hiện của một giá trị trong mẫu số liệu.<br>- Bảng tần số:<br>| Điểm ($x$) | 6 | 7 | 8 | 9 | 10 | Tổng |<br>| :--- | :---: | :---: | :---: | :---: | :---: | :---: |<br>| Tần số ($m$) | 2 | 5 | 7 | 4 | 2 | $N = 20$ |<br>- Chú ý: $N = \\sum m_i$. |

### Hoạt động 2.2: Biểu đồ tần số (Biểu đồ cột và Biểu đồ đoạn thẳng) (30 phút)
a) Mục tiêu: Nắm vững cách vẽ biểu đồ cột và biểu đồ đoạn thẳng biểu diễn tần số.
b) Nội dung: Vẽ trục tọa độ: Trục ngang biểu diễn giá trị $x$, trục đứng biểu diễn tần số $m$.
c) Sản phẩm: Hai dạng biểu đồ vẽ chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cách vẽ:<br>1. Biểu đồ cột: Dựng các cột chữ nhật cách đều nhau, chiều cao tương ứng với tần số $m$.<br>2. Biểu đồ đoạn thẳng: Xác định các điểm tọa độ $(x_i; m_i)$, sau đó dùng các đoạn thẳng nối liên tiếp các điểm đó lại.<br>- **HS:** Thực hành vẽ trên giấy kẻ ô.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ biểu đồ cột biểu diễn bảng điểm trên.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ biểu đồ cột, 1 HS vẽ biểu đồ đoạn thẳng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét sự trực quan của biểu đồ giúp nhìn thấy ngay giá trị xuất hiện nhiều nhất (Mode) là điểm 8. | **2. Biểu đồ tần số:**<br>- Biểu đồ cột: Trục hoành ghi giá trị $x$, trục tung ghi tần số $m$. Chiều rộng cột như nhau, chiều cao bằng $m$.<br>- Biểu đồ đoạn thẳng: Nối các đỉnh $(x_i; m_i)$ bằng các đoạn thẳng.<br>*Tích hợp NLS:* Sử dụng Excel (Insert $\\rightarrow$ Chart $\\rightarrow$ Column Chart) để tạo biểu đồ tự động. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Đọc biểu đồ tần số để trả lời các câu hỏi phân tích số liệu.
b) Nội dung: Cho biểu đồ số lượng áo bán được theo size ($S, M, L, XL, XXL$) tại một cửa hàng thời trang trong một tuần. Xác định size áo bán chạy nhất và tổng số áo đã bán.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu biểu đồ tần số bán áo: Size S: 15 chiếc, Size M: 45 chiếc, Size L: 50 chiếc, Size XL: 30 chiếc, Size XXL: 10 chiếc.<br>Yêu cầu: Lập bảng tần số và tính tổng số áo bán được.<br>- **HS:** Đọc số liệu từ biểu đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tổng số áo: $15 + 45 + 50 + 30 + 10 = 150$ chiếc. Size L bán chạy nhất ($50$ chiếc).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt ý nghĩa của bảng tần số trong việc nhập hàng và kinh doanh. | **Bài giải:**<br>Bảng tần số số lượng áo bán theo size:<br>| Size áo | S | M | L | XL | XXL | Tổng |<br>| :--- | :---: | :---: | :---: | :---: | :---: | :---: |<br>| Tần số | 15 | 45 | 50 | 30 | 10 | $150$ |<br>- Tổng số áo bán được trong tuần là $150$ chiếc.<br>- Size áo bán chạy nhất là Size L với tần số $50$ chiếc. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Giới thiệu khái niệm tần số tương đối chuẩn bị cho bài học tiếp theo.
b) Nội dung: Tỉ lệ phần trăm áo size L bán được so với tổng số áo là bao nhiêu?
c) Sản phẩm: Kết quả $\\frac{50}{150} \\approx 33{,}3\\%$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tính tỉ lệ phần trăm số áo size L bán được.<br>- **HS:** Tính toán: $\\frac{50}{150} \\cdot 100\\% \\approx 33{,}3\\%$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi nhận tỉ số phần trăm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tỉ lệ phần trăm này trong toán học gọi là tần số tương đối, ta sẽ học ở bài tiếp theo. | Dẫn dắt sang khái niệm tần số tương đối. |
"""
    },

    # 11: Bài 23 (Tiết 61-62)
    {
        "filename": "11_KHBD_Toan9_Bai23_BangTanSoTuongDoiVaBieuDo_Tiet61-62.md",
        "md": """TIẾT 61, 62 - BÀI 23: BẢNG TẦN SỐ TƯƠNG ĐỐI VÀ BIỂU ĐỒ TẦN SỐ TƯƠNG ĐỐI
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm tần số tương đối của một giá trị: Tỉ số giữa tần số $m$ của giá trị đó và quy mô mẫu $N$, thường viết dưới dạng phần trăm:
  $$f = \\frac{m}{N} \\cdot 100\\%$$
- Nắm vững tính chất: Tổng các tần số tương đối của tất cả các giá trị luôn bằng $100\\%$ ($f_1 + f_2 + \\dots + f_k = 100\\%$).
- Lập được bảng tần số tương đối cho mẫu số liệu thống kê.
- Nhận biết và vẽ được biểu đồ tần số tương đối: Biểu đồ cột, biểu đồ đoạn thẳng và Biểu đồ hình quạt tròn (tính góc ở tâm tương ứng $n^\\circ = f \\cdot 3{,}6^\\circ$).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tính toán tỉ lệ phần trăm chính xác bằng máy tính cầm tay, làm tròn hợp lí.
- Giao tiếp và hợp tác: Cùng nhóm so sánh hai tập dữ liệu có quy mô khác nhau thông qua tần số tương đối.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Hiểu vì sao tần số tương đối cho phép so sánh khách quan hơn tần số tuyệt đối khi hai mẫu có số lượng cá thể khác nhau.
- Năng lực mô hình hoá toán học: Chuyển đổi dữ liệu tần số tương đối sang số đo góc ở tâm để vẽ biểu đồ quạt tròn.

## 3. Về phẩm chất
- Cẩn thận trong các phép tính phần trăm và làm tròn số thập phân.
- Tinh thần khách quan, khoa học trong phân tích số liệu.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, thước đo góc (thước đo độ), compa, bảng phụ, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, thước đo góc, compa.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề so sánh tỉ lệ học sinh giỏi của hai lớp có sĩ số khác nhau.
b) Nội dung: Lớp 9A có 10 học sinh giỏi trên tổng số 40 bạn. Lớp 9B có 12 học sinh giỏi trên tổng số 50 bạn. Lớp nào có thành tích học sinh giỏi cao hơn?
c) Sản phẩm: HS tính: Lớp 9A là $\\frac{10}{40} = 25\\%$; Lớp 9B là $\\frac{12}{50} = 24\\%$. Lớp 9A cao hơn.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán so sánh 10/40 và 12/50. Lớp nào đạt tỉ lệ cao hơn?<br>- **HS:** Tính phần trăm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lớp 9A: 25%. Lớp 9B: 24%.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Mặc dù 10 < 12 nhưng tỉ lệ lớp 9A lại lớn hơn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khi so sánh hai tập dữ liệu khác quy mô mẫu, ta phải dùng tần số tương đối (tỉ lệ phần trăm). | Ý nghĩa của tần số tương đối trong việc so sánh khách quan các mẫu số liệu. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Tần số tương đối và Bảng tần số tương đối (35 phút)
a) Mục tiêu: Nắm vững công thức $f = \\frac{m}{N} \\cdot 100\\%$ và lập bảng tần số tương đối.
b) Nội dung: Định nghĩa, tính chất tổng $100\\%$ và lập bảng mẫu.
c) Sản phẩm: Vở ghi bài định nghĩa và bảng tần số tương đối của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Tần số tương đối của một giá trị là tỉ số giữa tần số của giá trị đó và kích thước mẫu $N$:<br>$$f_i = \\frac{m_i}{N} \\cdot 100\\%$$<br>Tổng các tần số tương đối: $f_1 + f_2 + \\dots + f_k = 100\\%$.<br>- **HS:** Ghi chép công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho mẫu số liệu có $N = 50$, các tần số $m_1 = 15, m_2 = 20, m_3 = 10, m_4 = 5$. Tính các tần số tương đối.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $f_1 = \\frac{15}{50} \\cdot 100\\% = 30\\%$; $f_2 = 40\\%$; $f_3 = 20\\%$; $f_4 = 10\\%$. Tổng: $30 + 40 + 20 + 10 = 100\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bảng tần số tương đối. | **1. Định nghĩa và tính chất:**<br>- Công thức tần số tương đối:<br>$$f = \\frac{m}{N} \\cdot 100\\%$$<br>- Tính chất: $\\sum f_i = 100\\%$.<br>- Bảng tần số tương đối: Gồm dòng giá trị và dòng tần số tương đối (%). |

### Hoạt động 2.2: Biểu đồ hình quạt tròn biểu diễn tần số tương đối (30 phút)
a) Mục tiêu: Nắm vững cách chuyển đổi tần số tương đối sang số đo góc ở tâm và vẽ biểu đồ hình quạt tròn.
b) Nội dung: Công thức tính góc ở tâm: $n^\\circ = f \\cdot 3{,}6^\\circ$ (vì $100\\% = 360^\\circ \\Rightarrow 1\\% = 3{,}6^\\circ$).
c) Sản phẩm: Biểu đồ quạt tròn được vẽ chuẩn xác bằng compa và thước đo góc.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cách tính góc ở tâm biểu đồ quạt tròn:<br>$$n_i^\\circ = f_i \\cdot 3{,}6^\\circ$$<br>Ví dụ: $30\\% \\Rightarrow 30 \\cdot 3{,}6^\\circ = 108^\\circ$.<br>$40\\% \\Rightarrow 40 \\cdot 3{,}6^\\circ = 144^\\circ$.<br>$20\\% \\Rightarrow 72^\\circ$; $10\\% \\Rightarrow 36^\\circ$.<br>Kiểm tra: $108 + 144 + 72 + 36 = 360^\\circ$.<br>- **HS:** Dùng compa vẽ đường tròn, dùng thước đo góc vẽ các quạt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành vẽ biểu đồ quạt tròn vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng dùng compa và thước đo góc vẽ biểu đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa kỹ năng vẽ biểu đồ hình quạt tròn. | **2. Biểu đồ hình quạt tròn:**<br>- Mỗi hình quạt biểu diễn một giá trị.<br>- Góc ở tâm của hình quạt tương ứng với tần số tương đối $f$ là:<br>$$n^\\circ = f \\cdot 3{,}6^\\circ$$<br>(hoặc $n^\\circ = \\frac{f}{100} \\cdot 360^\\circ$).<br>- Tổng các góc ở tâm bằng $360^\\circ$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Lập bảng tần số tương đối và vẽ biểu đồ cột tương đối.
b) Nội dung: Thống kê phương tiện đến trường của 40 học sinh lớp 9C: Xe đạp: 16 bạn; Xe buýt: 8 bạn; Đi bộ: 6 bạn; Bố mẹ chở: 10 bạn.
c) Sản phẩm: Bảng tần số tương đối và biểu đồ cột trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao đề bài thống kê phương tiện đến trường của 40 học sinh.<br>- **HS:** Tính các giá trị $f_i$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xe đạp: $\\frac{16}{40} = 40\\%$. Xe buýt: $\\frac{8}{40} = 20\\%$. Đi bộ: $\\frac{6}{40} = 15\\%$. Bố mẹ chở: $\\frac{10}{40} = 25\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng lập bảng và vẽ biểu đồ cột.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài tập chuẩn mực. | **Bài giải:**<br>Bảng tần số tương đối phương tiện đến trường:<br>| Phương tiện | Xe đạp | Xe buýt | Đi bộ | Bố mẹ chở | Tổng |<br>| :--- | :---: | :---: | :---: | :---: | :---: |<br>| Tần số ($m$) | 16 | 8 | 6 | 10 | 40 |<br>| Tần số tương đối ($f$) | $40\\%$ | $20\\%$ | $15\\%$ | $25\\%$ | $100\\%$ | |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Dẫn dắt khi số liệu điều tra liên tục (như cân nặng, thời gian chạy) có quá nhiều giá trị khác nhau thì phải ghép nhóm thế nào?
b) Nội dung: Đặt vấn đề khi đo chiều cao 100 học sinh, hầu như mỗi bạn có một số đo khác nhau (152,1 cm; 153,4 cm...). Làm sao lập bảng?
c) Sản phẩm: Dự đoán của HS: Phải gom các bạn vào từng khoảng, ví dụ từ 150 cm đến 155 cm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nếu có 100 số liệu đo chiều cao khác nhau thì bảng tần số rời rạc có phù hợp không?<br>- **HS:** Trả lời: Bảng sẽ quá dài, không tiện theo dõi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đề xuất chia thành các khoảng nhóm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu ý tưởng ghép nhóm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đó chính là nội dung của bảng tần số ghép nhóm ta sẽ học sau tiết Luyện tập chung. | Giới thiệu nhu cầu ghép nhóm số liệu. |
"""
    },

    # 12: Tiết 63: Luyện tập chung (Mindmap: mindmap_toan9_tiet63.png)
    {
        "filename": "12_KHBD_Toan9_LuyenTapChung_Tiet63.md",
        "md": """TIẾT 63 - LUYỆN TẬP CHUNG: BẢNG TẦN SỐ VÀ BIỂU ĐỒ TẦN SỐ
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và rèn luyện thành thạo kỹ năng:
  + Lập bảng tần số và bảng tần số tương đối từ mẫu số liệu thô.
  + Chuyển đổi qua lại giữa tần số tuyệt đối $m$ và tần số tương đối $f = \\frac{m}{N} \\cdot 100\\%$.
  + Vẽ và đọc hiểu các dạng biểu đồ: Biểu đồ cột, biểu đồ đoạn thẳng, biểu đồ hình quạt tròn.
  + Tính góc ở tâm $n^\\circ = f \\cdot 3{,}6^\\circ$ để vẽ biểu đồ quạt tròn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa toàn bộ kiến thức về tần số và biểu đồ bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận phân tích số liệu thống kê.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng nhận định xu thế, giá trị đặc trưng từ các biểu đồ thống kê.
- Năng lực giải quyết vấn đề toán học: Xử lý và trình bày số liệu thống kê rõ ràng, minh bạch.

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng khi thống kê số liệu.
- Ý thức trách nhiệm, nhìn nhận vấn đề khách quan dựa trên dữ liệu.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI, máy chiếu, bảng phụ ghi số liệu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, dụng cụ vẽ biểu đồ (thước kẻ, compa, thước đo độ).

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn nhanh mối quan hệ giữa tần số $m$ và tần số tương đối $f$.
b) Nội dung: Cho biết quy mô mẫu $N = 80$, một giá trị có tần số $m = 24$. Hỏi tần số tương đối của giá trị đó là bao nhiêu?
c) Sản phẩm: Kết quả $f = \\frac{24}{80} \\cdot 100\\% = 30\\%$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi tính nhanh tần số tương đối.<br>- **HS:** Bấm máy tính nhẩm nhanh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $f = \\frac{24}{80} \\cdot 100\\% = 30\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang phần sơ đồ tư duy tổng kết. | Khởi động: Tính nhanh tần số tương đối từ tần số tuyệt đối. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Tần số & Biểu đồ bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống toàn diện định nghĩa, bảng biểu và các dạng biểu đồ bằng sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Bảng tần số & Biểu đồ tần số.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Tần số và Biểu đồ tần số Tiết 63](khbd-ill:mindmap-toan9-tiet63)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Tần số & Biểu đồ. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Tần số $m$ (số lần xuất hiện, tổng $N$).<br>2) Tần số tương đối $f$ ($f = \\frac{m}{N} \\cdot 100\\%$, tổng $100\\%$).<br>3) Biểu đồ tần số (cột, đoạn thẳng).<br>4) Biểu đồ hình quạt tròn ($n^\\circ = f \\cdot 3{,}6^\\circ$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích mối quan hệ giữa các nhánh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại kiến thức trọng tâm và các lưu ý khi vẽ biểu đồ quạt tròn. | **Hệ thống kiến thức trọng tâm:**<br>1. Tần số $m$ và quy mô mẫu $N = \\sum m_i$.<br>2. Tần số tương đối: $f = \\frac{m}{N} \\cdot 100\\%$ (tổng bằng $100\\%$).<br>3. Biểu đồ cột và biểu đồ đoạn thẳng ghi rõ tên trục và đơn vị.<br>4. Biểu đồ quạt tròn: Góc ở tâm $n^\\circ = f \\cdot 3{,}6^\\circ$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Lập bảng phân bố tần số, tần số tương đối và vẽ biểu đồ hình quạt tròn từ số liệu thực tế.
b) Nội dung: Kết quả xếp loại học lực của 40 học sinh lớp 9B: Tốt: 12 bạn; Khá: 18 bạn; Đạt: 8 bạn; Chưa đạt: 2 bạn.
1) Lập bảng tần số và bảng tần số tương đối.
2) Tính số đo góc ở tâm tương ứng và vẽ biểu đồ hình quạt tròn.
c) Sản phẩm: Lời giải chi tiết và biểu đồ hình quạt tròn trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao đề bài thống kê xếp loại học lực của 40 học sinh.<br>- **HS:** Lập bảng và tính toán các đại lượng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>- Tốt: $m_1 = 12 \\Rightarrow f_1 = \\frac{12}{40} \\cdot 100\\% = 30\\% \\Rightarrow n_1 = 30 \\cdot 3{,}6^\\circ = 108^\\circ$.<br>- Khá: $m_2 = 18 \\Rightarrow f_2 = \\frac{18}{40} \\cdot 100\\% = 45\\% \\Rightarrow n_2 = 45 \\cdot 3{,}6^\\circ = 162^\\circ$.<br>- Đạt: $m_3 = 8 \\Rightarrow f_3 = \\frac{8}{40} \\cdot 100\\% = 20\\% \\Rightarrow n_3 = 20 \\cdot 3{,}6^\\circ = 72^\\circ$.<br>- Chưa đạt: $m_4 = 2 \\Rightarrow f_4 = \\frac{2}{40} \\cdot 100\\% = 5\\% \\Rightarrow n_4 = 5 \\cdot 3{,}6^\\circ = 18^\\circ$.<br>Kiểm tra: $108^\\circ + 162^\\circ + 72^\\circ + 18^\\circ = 360^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng hoàn thành bảng số liệu và vẽ biểu đồ quạt tròn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bài giải mẫu mực trên bảng. | **Bài giải:**<br>Bảng tần số và tần số tương đối xếp loại học lực:<br>| Xếp loại | Tốt | Khá | Đạt | Chưa đạt | Tổng |<br>| :--- | :---: | :---: | :---: | :---: | :---: |<br>| Tần số ($m$) | 12 | 18 | 8 | 2 | 40 |<br>| Tần số tương đối ($f$) | $30\\%$ | $45\\%$ | $20\\%$ | $5\\%$ | $100\\%$ |<br>| Góc ở tâm ($n^\\circ$) | $108^\\circ$ | $162^\\circ$ | $72^\\circ$ | $18^\\circ$ | $360^\\circ$ |<br>Vẽ biểu đồ hình quạt tròn chính xác với các góc ở tâm đã tính. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhắc nhở dặn dò chuẩn bị cho bài Bảng tần số, tần số tương đối ghép nhóm tiếp theo.
b) Nội dung: Xem trước khái niệm nửa khoảng $[a; b)$ và giá trị đại diện của nhóm.
c) Sản phẩm: HS ghi nhận nhiệm vụ tự học ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò xem trước bài Bảng tần số ghép nhóm.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc lướt SGK bài 24.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu những câu hỏi ban đầu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em học tốt. | Dặn dò chuẩn bị bài Bảng tần số ghép nhóm. |
"""
    },

    # 13: Bài 24 (Tiết 64-66)
    {
        "filename": "13_KHBD_Toan9_Bai24_BangTanSoGhepNhomVaBieuDo_Tiet64-66.md",
        "md": """TIẾT 64, 65, 66 - BÀI 24: BẢNG TẦN SỐ, TẦN SỐ TƯƠNG ĐỐI GHÉP NHÓM VÀ BIỂU ĐỒ
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm nhóm số liệu (dạng nửa khoảng $[a; b)$), giá trị đại diện của nhóm $c = \\frac{a + b}{2}$, độ dài của nhóm $l = b - a$.
- Lập được bảng tần số ghép nhóm và bảng tần số tương đối ghép nhóm từ mẫu số liệu cho trước.
- Nhận biết và vẽ được biểu đồ tần số ghép nhóm dạng biểu đồ cột liền kề (Histogram) và biểu đồ tần số tương đối ghép nhóm.
- Đọc, giải thích và rút ra các kết luận thống kê về phân bố dữ liệu từ biểu đồ ghép nhóm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự phân chia các khoảng nhóm số liệu có độ dài bằng nhau một cách hợp lí.
- Giao tiếp và hợp tác: Cùng nhóm phân tích dữ liệu thực tế kích thước lớn (chiều cao, cân nặng, thời gian tự học).

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Hiểu nguyên lí nén thông tin khi ghép nhóm (chấp nhận mất mát chi tiết để nhìn thấy bức tranh tổng thể).
- Năng lực mô hình hoá toán học: Sử dụng biểu đồ Histogram phân tích phân bố chuẩn, phân bố lệch trong thực tế.

c) Năng lực số (NLS):
- ***1.2.TC2a: Đánh giá tính hợp lý của việc phân nhóm dữ liệu trên bảng tính điện tử phục vụ vẽ biểu đồ histogram; 3.1.TC2a: Sử dụng công cụ số để ghi chép, hệ thống hóa và trình bày kết quả học tập Bảng tần số, tần số tương đối ghép nhóm và biểu đồ.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, tỉ mỉ khi phân loại các số liệu thuộc mút trái $[$ và không thuộc mút phải $)$.
- Tinh thần khoa học, khách quan trong xử lý dữ liệu lớn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, bảng tính Excel minh họa Histogram, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, thước kẻ có vạch chia.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề thống kê thời gian sử dụng Internet trong ngày của 50 học sinh với nhiều giá trị phân tán.
b) Nội dung: Các giá trị thời gian dao động từ 15 phút đến 180 phút. Nếu lập bảng tần số rời rạc thì bảng sẽ rất dài. Làm cách nào để thu gọn?
c) Sản phẩm: Đề xuất của HS: Chia thành các nhóm thời gian như $[0; 30), [30; 60), [60; 90), [90; 120), [120; 180)$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu tình huống dữ liệu thời gian phân tán từ 15 đến 180 phút. Làm thế nào để trình bày trực quan?<br>- **HS:** Suy nghĩ và đề xuất giải pháp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận chia thành các khoảng thời gian.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Gom các giá trị vào từng khoảng gọi là nhóm số liệu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Phương pháp đó gọi là ghép nhóm số liệu. Bảng tương ứng gọi là bảng tần số ghép nhóm. | Dẫn nhập vào bài học: Nhu cầu ghép nhóm đối với mẫu số liệu có nhiều giá trị khác nhau. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (105 phút)
### Hoạt động 2.1: Nhóm số liệu và Bảng tần số ghép nhóm (35 phút)
a) Mục tiêu: Nắm vững cấu trúc nhóm $[a; b)$, giá trị đại diện và cách đếm tần số của nhóm.
b) Nội dung: Định nghĩa nhóm số liệu, giá trị đại diện $c = \\frac{a + b}{2}$; quy tắc phần tử $x \\in [a; b) \\Leftrightarrow a \\le x < b$.
c) Sản phẩm: Vở ghi bài và bảng tần số ghép nhóm đầu tiên của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu nhóm số liệu $[a; b)$:<br>- Mút trái $a$, mút phải $b$. Giá trị $x$ thuộc nhóm nếu $a \\le x < b$.<br>- Giá trị đại diện của nhóm: $c = \\frac{a + b}{2}$.<br>- Độ dài nhóm: $l = b - a$. Thường chọn các nhóm có độ dài bằng nhau.<br>- Tần số của nhóm: Số lượng giá trị thuộc vào nhóm đó.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho nhóm $[150; 155)$. Tìm giá trị đại diện và kiểm tra xem số $155$ có thuộc nhóm này không?<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giá trị đại diện $c = \\frac{150 + 155}{2} = 152{,}5$. Giá trị $155$ không thuộc nhóm này mà thuộc nhóm kế tiếp $[155; 160)$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Cần chú ý mút phải ngoặc tròn $)$ không lấy giá trị bằng $b$. | **1. Nhóm số liệu và Bảng tần số ghép nhóm:**<br>- Nhóm số liệu có dạng $[a; b) = \\{x \\in \\mathbb{R} \\mid a \\le x < b\\}$.<br>- Giá trị đại diện: $c = \\frac{a + b}{2}$.<br>- Tần số nhóm: Số lượng cá thể thuộc $[a; b)$.<br>- Bảng tần số ghép nhóm: Gồm dòng các nhóm số liệu và dòng tần số tương ứng. |

### Hoạt động 2.2: Bảng tần số tương đối ghép nhóm (35 phút)
a) Mục tiêu: Nắm vững công thức tần số tương đối của nhóm $f = \\frac{m_{nhóm}}{N} \\cdot 100\\%$.
b) Nội dung: Lập bảng tần số tương đối ghép nhóm và tính tổng phần trăm $100\\%$.
c) Sản phẩm: Bảng tần số tương đối ghép nhóm trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tần số tương đối của nhóm $[a; b)$ là tỉ số giữa tần số của nhóm đó và kích thước mẫu $N$:<br>$$f_i = \\frac{m_i}{N} \\cdot 100\\%$$<br>- **HS:** Tiếp nhận công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho mẫu $N = 40$ với các tần số nhóm: $6, 14, 12, 8$. Lập bảng tần số tương đối ghép nhóm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $f_1 = \\frac{6}{40} \\cdot 100\\% = 15\\%$; $f_2 = 35\\%$; $f_3 = 30\\%$; $f_4 = 20\\%$. Tổng: $100\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng tần số tương đối ghép nhóm. | **2. Bảng tần số tương đối ghép nhóm:**<br>| Nhóm | $[a_1; a_2)$ | $[a_2; a_3)$ | $[a_3; a_4)$ | $[a_4; a_5)$ | Tổng |<br>| :--- | :---: | :---: | :---: | :---: | :---: |<br>| Tần số ($m$) | $m_1$ | $m_2$ | $m_3$ | $m_4$ | $N$ |<br>| Tần số tương đối ($f$) | $f_1$ | $f_2$ | $f_3$ | $f_4$ | $100\\%$ | |

### Hoạt động 2.3: Biểu đồ tần số ghép nhóm (Histogram) (35 phút)
a) Mục tiêu: Nhận biết và vẽ được biểu đồ cột liền kề (Histogram) biểu diễn tần số ghép nhóm.
b) Nội dung: Trục hoành ghi các mút $a_1, a_2, a_3, \\dots$, các cột dựng sát liền kề nhau có đáy là đoạn $[a_i; a_{i+1}]$ và chiều cao là tần số $m_i$.
c) Sản phẩm: Biểu đồ Histogram vẽ chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cách vẽ biểu đồ Histogram:<br>- Trục hoành: Chia tỉ lệ và đánh dấu các mút $a_1, a_2, a_3, \\dots$<br>- Các cột hình chữ nhật nằm sát liền nhau, không có khoảng cách trống như biểu đồ cột thông thường.<br>- **HS:** Quan sát hình vẽ mẫu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành vẽ biểu đồ cột liền kề cho bảng số liệu trên.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ biểu đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Do dữ liệu liên tục nên các cột trong Histogram phải dính liền kề nhau tại các mút ranh giới. | **3. Biểu đồ tần số ghép nhóm (Histogram):**<br>- Là biểu đồ gồm các cột chữ nhật liền kề nhau.<br>- Đáy mỗi cột là đoạn biểu diễn nhóm số liệu trên trục hoành.<br>- Chiều cao mỗi cột bằng tần số (hoặc tần số tương đối) của nhóm đó.<br>*Tích hợp NLS:* Đánh giá tính hợp lí của việc chọn số lượng nhóm trên phần mềm bảng tính. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Lập bảng tần số ghép nhóm và vẽ Histogram từ dữ liệu chiều cao học sinh.
b) Nội dung: Cho bảng số liệu chiều cao của 30 học sinh:
Nhóm $[150; 155)$: 5 bạn; Nhóm $[155; 160)$: 12 bạn; Nhóm $[160; 165)$: 9 bạn; Nhóm $[165; 170)$: 4 bạn.
1) Tính các giá trị đại diện của từng nhóm.
2) Lập bảng tần số tương đối ghép nhóm.
3) Vẽ biểu đồ Histogram.
c) Sản phẩm: Lời giải hoàn chỉnh và hình vẽ biểu đồ trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập với các yêu cầu trên.<br>- **HS:** Tính toán giá trị đại diện và phần trăm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giá trị đại diện: $152{,}5; 157{,}5; 162{,}5; 167{,}5$.<br>Tần số tương đối: $\\frac{5}{30} \\approx 16{,}7\\%$; $\\frac{12}{30} = 40\\%$; $\\frac{9}{30} = 30\\%$; $\\frac{4}{30} \\approx 13{,}3\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa biểu đồ Histogram trên bảng. | **Bài giải:**<br>1) Giá trị đại diện các nhóm:<br>- Nhóm $[150; 155)$: $c_1 = 152{,}5\\text{ (cm)}$.<br>- Nhóm $[155; 160)$: $c_2 = 157{,}5\\text{ (cm)}$.<br>- Nhóm $[160; 165)$: $c_3 = 162{,}5\\text{ (cm)}$.<br>- Nhóm $[165; 170)$: $c_4 = 167{,}5\\text{ (cm)}$.<br><br>2) Bảng tần số tương đối ghép nhóm:<br>| Chiều cao (cm) | $[150; 155)$ | $[155; 160)$ | $[160; 165)$ | $[165; 170)$ | Tổng |<br>| :--- | :---: | :---: | :---: | :---: | :---: |<br>| Tần số | 5 | 12 | 9 | 4 | 30 |<br>| Tần số tương đối | $16{,}7\\%$ | $40{,}0\\%$ | $30{,}0\\%$ | $13{,}3\\%$ | $100\\%$ |<br><br>3) Vẽ biểu đồ Histogram chính xác các cột liền kề. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng biểu đồ Histogram đánh giá tỉ lệ học sinh đạt chuẩn chiều cao theo lứa tuổi.
b) Nội dung: Dựa vào biểu đồ, tính tỉ lệ học sinh có chiều cao từ $160\\text{ cm}$ trở lên.
c) Sản phẩm: Kết quả $30\\% + 13{,}3\\% = 43{,}3\\%$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tính tỉ lệ phần trăm học sinh cao từ 160 cm trở lên.<br>- **HS:** Cộng tỉ lệ của nhóm 3 và nhóm 4.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $30\\% + 13{,}3\\% = 43{,}3\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò làm bài tập cuối chương VII. | Tỉ lệ học sinh cao từ $160\\text{ cm}$ trở lên là $43{,}3\\%$. |
"""
    },

    # 14: Tiết 67-68: Bài tập cuối chương VII (Mindmap: mindmap_toan9_tiet67_68.png)
    {
        "filename": "14_KHBD_Toan9_BaiTapCuoiChuong7_Tiet67-68.md",
        "md": """TIẾT 67, 68 - BÀI TẬP CUỐI CHƯƠNG VII
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập và củng cố toàn diện kiến thức Chương VII: Tần số và tần số tương đối:
  + Tần số tuyệt đối $m$, quy mô mẫu $N = \\sum m_i$.
  + Tần số tương đối $f = \\frac{m}{N} \\cdot 100\\%$, tính chất tổng bằng $100\\%$.
  + Biểu đồ tần số: Biểu đồ cột, biểu đồ đoạn thẳng, biểu đồ hình quạt tròn ($n^\\circ = f \\cdot 3{,}6^\\circ$).
  + Bảng tần số ghép nhóm, giá trị đại diện $c = \\frac{a + b}{2}$, độ dài nhóm $l = b - a$.
  + Biểu đồ tần số ghép nhóm (Histogram cột liền kề).
- Rèn luyện kỹ năng đọc, phân tích và xử lý dữ liệu thống kê từ các bảng biểu và đồ thị thực tế.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức Chương VII dưới dạng sơ đồ tư duy hoàn chỉnh.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp xử lý số liệu và phân tích kết quả thống kê.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng suy luận từ dữ liệu mẫu ra đặc trưng của tổng thể.
- Năng lực giải quyết vấn đề toán học: Hoàn thành bài tập trắc nghiệm và tự luận cuối chương.

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng khi thực hiện tính toán số liệu thống kê.
- Tinh thần nghiêm túc, chuẩn bị cho chương học tiếp theo về Xác suất của biến cố.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI Chương VII, phiếu bài tập ôn tập, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, dụng cụ vẽ biểu đồ.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khởi động ôn tập bằng trò chơi giải nhanh các câu hỏi trắc nghiệm kiến thức cốt lõi Chương VII.
b) Nội dung: Trả lời nhanh 3 câu hỏi về công thức tần số tương đối, góc ở tâm quạt tròn và giá trị đại diện nhóm.
c) Sản phẩm: Câu trả lời chính xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu 3 câu hỏi trắc nghiệm ôn tập nhanh.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc nhanh công thức $f = \\frac{m}{N} \\cdot 100\\%$, $n^\\circ = f \\cdot 3{,}6^\\circ$, $c = \\frac{a + b}{2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS trả lời miệng trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá đúng và chuyển sang sơ đồ tư duy tổng kết toàn chương. | Tái hiện nhanh các công thức trọng tâm Chương VII. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Tổng kết Chương VII bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Khái quát toàn bộ cấu trúc kiến thức Chương VII: Tần số và tần số tương đối.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI tổng kết Chương VII.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Bài tập cuối chương VII Tiết 67 - 68](khbd-ill:mindmap-toan9-tiet67-68)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI tổng kết toàn bộ Chương VII. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trình bày 4 nhánh:<br>1) Dữ liệu rời rạc: Tần số $m$, bảng tần số, biểu đồ cột và đoạn thẳng.<br>2) Tần số tương đối $f$: Công thức, tính chất tổng $100\\%$, biểu đồ quạt tròn.<br>3) Dữ liệu ghép nhóm: Nhóm $[a; b)$, giá trị đại diện $c$, độ dài nhóm $l$.<br>4) Biểu đồ tần số ghép nhóm (Histogram cột liền kề).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích sự khác nhau giữa biểu đồ cột rời rạc và biểu đồ Histogram ghép nhóm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ và nhấn mạnh các dạng toán điển hình. | **Tổng kết toàn bộ Chương VII:**<br>1. Tần số và Tần số tương đối (rời rạc).<br>2. Biểu đồ: Cột, Đoạn thẳng, Hình quạt tròn.<br>3. Tần số và Tần số tương đối ghép nhóm.<br>4. Biểu đồ cột liền kề Histogram.<br>5. Ứng dụng thực tế: Phân tích số liệu điều tra kinh tế, xã hội, giáo dục. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Giải bài tập tổng hợp cuối chương trong SGK Toán 9 Tập 2.
b) Nội dung: Cho mẫu số liệu về thời gian chạy cự li $100\\text{ m}$ (tính bằng giây) của 40 học sinh lớp 9:
$[12; 13)$: 4 bạn; $[13; 14)$: 10 bạn; $[14; 15)$: 16 bạn; $[15; 16)$: 8 bạn; $[16; 17)$: 2 bạn.
1) Lập bảng tần số và bảng tần số tương đối ghép nhóm.
2) Tính số học sinh có thành tích chạy dưới $14$ giây.
3) Vẽ biểu đồ Histogram biểu diễn bảng tần số ghép nhóm trên.
c) Sản phẩm: Lời giải hoàn chỉnh 3 câu và biểu đồ Histogram trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tổng hợp về thời gian chạy 100m của 40 học sinh.<br>- **HS:** Lập bảng và tính toán các đại lượng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) Tính phần trăm: $\\frac{4}{40} = 10\\%$; $\\frac{10}{40} = 25\\%$; $\\frac{16}{40} = 40\\%$; $\\frac{8}{40} = 20\\%$; $\\frac{2}{40} = 5\\%$.<br>2) Số học sinh chạy dưới 14 giây là tổng của 2 nhóm đầu: $4 + 10 = 14$ bạn (chiếm $10\\% + 25\\% = 35\\%$).<br>3) Vẽ biểu đồ cột liền kề Histogram.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bài giải mẫu mực trên bảng. | **Bài giải:**<br>1) Bảng tần số và tần số tương đối ghép nhóm:<br>| Thời gian (giây) | $[12; 13)$ | $[13; 14)$ | $[14; 15)$ | $[15; 16)$ | $[16; 17)$ | Tổng |<br>| :--- | :---: | :---: | :---: | :---: | :---: | :---: |<br>| Giá trị đại diện | $12{,}5$ | $13{,}5$ | $14{,}5$ | $15{,}5$ | $16{,}5$ | — |<br>| Tần số ($m$) | 4 | 10 | 16 | 8 | 2 | 40 |<br>| Tần số tương đối ($f$) | $10\\%$ | $25\\%$ | $40\\%$ | $20\\%$ | $5\\%$ | $100\\%$ |<br><br>2) Số học sinh chạy dưới $14$ giây là: $4 + 10 = 14$ (học sinh), chiếm tỉ lệ $35\\%$.<br><br>3) Vẽ biểu đồ Histogram với 5 cột chữ nhật liền kề nhau chuẩn xác. |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhắc nhở dặn dò chuẩn bị cho Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản.
b) Nội dung: Xem lại khái niệm biến cố, phép thử đã học ở lớp 7 và lớp 8.
c) Sản phẩm: HS ghi nhận nhiệm vụ tự học ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò xem lại các bài toán xác suất tung đồng xu, gieo xúc xắc chuẩn bị cho Chương VIII.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự ôn luyện lại các kiến thức xác suất lớp 8.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu những câu hỏi ban đầu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em học tốt. | Dặn dò chuẩn bị bài mới Chương VIII. |
"""
    },
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print(f"Hoàn tất tạo đợt 2 (5 bài Chương VII Tiết 59 - 68) Toán 9 HK2!")
