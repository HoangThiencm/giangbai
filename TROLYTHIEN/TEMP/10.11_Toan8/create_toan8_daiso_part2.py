# -*- coding: utf-8 -*-
"""
Script sinh tiếp các tệp KHBD Đại số & Thống kê 8 (Bài 03 đến Bài 12):
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Toan8"
os.makedirs(OUT_DIR, exist_ok=True)

# 03. Bài tập cuối chương II (Tiết 27)
md_03 = """Tiết 27 - BÀI TẬP CUỐI CHƯƠNG II (HẰNG ĐẲNG THỨC ĐÁNG NHỚ VÀ ỨNG DỤNG)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Chương II: Bảy hằng đẳng thức đáng nhớ; Các phương pháp phân tích đa thức thành nhân tử; Ứng dụng vào tính nhanh, rút gọn và giải phương trình tích.
- Rèn luyện kĩ năng biến đổi đại số chính xác, nhận diện dạng hằng đẳng thức ngược và xuôi.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức qua sơ đồ tư duy toàn chương.
- Giao tiếp và hợp tác: Hợp tác nhóm giải các bài toán tổng hợp cuối chương.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học; Năng lực giải quyết vấn đề toán học.

c) Năng lực số (NLS):
- ***5.3.TC2a: HS sử dụng phần mềm GeoGebra hoặc máy tính cầm tay thực hiện lệnh tính toán mở rộng đa thức (Expand) và phân tích nhân tử (Factor) để tự kiểm tra bài làm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để phân loại các dạng bài toán cực trị đại số ứng dụng từ hằng đẳng thức.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác, kỷ luật và kiên nhẫn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 1, KHBD, Sơ đồ tư duy Tổng kết Chương II (vector 300 DPI), tivi/máy chiếu, phiếu bài tập.
2. Học sinh: SGK Toán 8, vở bài tập, máy tính cầm tay, bảng con.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Khởi động tinh thần qua bài trắc nghiệm nhanh 7 hằng đẳng thức.
b) Nội dung: Điền biểu thức thích hợp vào chỗ trống để được hằng đẳng thức đúng.
c) Sản phẩm: Bảng kết quả của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu: $A^3 + B^3 = (A + B)(\\dots)$; $(A - B)^2 = \\dots$<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm và viết vào bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cả lớp đồng thanh đọc các hằng đẳng thức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, dẫn dắt vào tiết ôn tập bài tập cuối chương. | **Đáp án khởi động:**<br>$A^3 + B^3 = (A + B)(A^2 - AB + B^2)$<br>$(A - B)^2 = A^2 - 2AB + B^2$. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Giúp học sinh nắm vững bức tranh tổng thể Chương II qua Sơ đồ tư duy.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tổng kết Chương II; nhắc lại các kiến thức cốt lõi.

![Sơ đồ tư duy Tổng kết Chương II](khbd-ill:mindmap-toan8-tiet27)

c) Sản phẩm: Bản ghi nhớ hệ thống kiến thức trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Tổng kết Chương II. Yêu cầu HS nêu các nhánh kiến thức chính.<br>- **HS:** Quan sát và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa sơ đồ. | **Hệ thống kiến thức:**<br>1. Bảy hằng đẳng thức đáng nhớ.<br>2. Bốn phương pháp phân tích đa thức.<br>3. Ứng dụng tính nhanh và tìm $x$. |

### Hoạt động 2.2: Luyện giải bài tập tổng hợp SGK trang 44 (22 phút)
a) Mục tiêu: Giải thành thạo các bài tập 2.27, 2.28, 2.30 SGK trang 44.
b) Nội dung: Rút gọn biểu thức, tính giá trị và chứng minh bất đẳng thức phụ.
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 2.27, 2.28 SGK.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự lực làm bài vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Sửa bài cẩn thận. | **Bài 2.27 (SGK tr.44): Rút gọn biểu thức:**<br>$A = (x - 2y)^2 - (x + 2y)^2$<br>$A = [(x - 2y) - (x + 2y)][(x - 2y) + (x + 2y)] = (-4y)(2x) = -8xy$.<br><br>**Bài 2.28 (SGK tr.44):**<br>Chứng minh biểu thức $B = x^2 - 4x + 5$ luôn dương với mọi $x$:<br>$B = (x^2 - 4x + 4) + 1 = (x - 2)^2 + 1$.<br>Vì $(x - 2)^2 \\ge 0$ với mọi $x$ nên $(x - 2)^2 + 1 \\ge 1 > 0$ với mọi $x$.<br>Vậy biểu thức $B$ luôn dương với mọi $x$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng hằng đẳng thức để tìm giá trị nhỏ nhất của tam thức bậc hai.
b) Nội dung: Tìm giá trị nhỏ nhất của biểu thức $M = x^2 - 6x + 15$.
c) Sản phẩm: Lời giải của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán: Tìm giá trị nhỏ nhất của biểu thức $M = x^2 - 6x + 15$.<br>- **HS:** Biến đổi đưa về dạng bình phương một hiệu cộng một số.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính $M = (x - 3)^2 + 6 \\ge 6$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Giá trị nhỏ nhất là $6$ khi $x = 3$. Dặn dò chuẩn bị cho tiết HĐTN GeoGebra. | **Lời giải:**<br>$M = x^2 - 6x + 9 + 6 = (x - 3)^2 + 6$.<br>Vì $(x - 3)^2 \\ge 0$ nên $M \\ge 6$ với mọi $x$.<br>Dấu bằng xảy ra khi $x - 3 = 0$ hay $x = 3$.<br>Vậy giá trị nhỏ nhất của $M$ là $6$ khi $x = 3$. |
"""

# 04. HĐTN Tính toán đa thức với GeoGebra (Tiết 28)
md_04 = """Tiết 28 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: TÍNH TOÁN TRÊN ĐA THỨC VỚI PHẦN MỀM GEOGEBRA
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Làm quen với cửa sổ tính toán đại số CAS (Computer Algebra System) trong phần mềm GeoGebra.
- Sử dụng thành thạo các câu lệnh cơ bản trên đa thức:
  + Lệnh `KhaiTrien(...)` hoặc `Expand(...)`: Khai triển tích thành đa thức.
  + Lệnh `PhanTichNhanTu(...)` hoặc `Factor(...)`: Phân tích đa thức thành nhân tử.
  + Lệnh `ThuGon(...)` hoặc `Simplify(...)`: Rút gọn biểu thức đại số phức tạp.
- Vận dụng phần mềm để kiểm chứng kết quả các bài toán đã giải bằng tay và khám phá các đẳng thức đại số mở rộng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tra cứu cú pháp lệnh trong tài liệu hướng dẫn SGK trang 113-114.
- Giao tiếp và hợp tác: Hợp tác nhóm thực hành trên phòng máy tính, chia sẻ các thủ thuật gõ nhanh biến số và số mũ.

b) Năng lực đặc thù môn Toán:
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng công nghệ CAS hỗ trợ học tập và nghiên cứu toán học.

c) Năng lực số (NLS):
- ***3.1.TC2a: HS chỉ ra được cách tạo và chỉnh sửa đa thức trong phần mềm GeoGebra; sử dụng thành thạo các lệnh Expand và Factor để tính toán và kiểm tra kết quả.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS tìm hiểu cơ chế hoạt động của các hệ thống CAS và AI trong việc biến đổi biểu thức toán học hình thức.***

## 3. Về phẩm chất
- Rèn luyện tính chính xác, tính công nghệ và niềm đam mê khám phá toán học hiện đại.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng thực hành máy tính có cài GeoGebra (hoặc truy cập `geogebra.org/cas`), máy chiếu, phiếu thực hành số.
2. Học sinh: Máy tính cá nhân phòng máy, vở ghi bài.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt sự hào hứng khám phá công cụ CAS của GeoGebra.
b) Nội dung: Quan sát giáo viên nhập lệnh `Factor(x^4 - 16)` trên máy chiếu.
c) Sản phẩm: Kết quả `(x - 2)(x + 2)(x^2 + 4)` hiển thị tức thời.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu màn hình GeoGebra CAS. Nhập biểu thức đa thức bậc 4 và bấm Factor.<br>- **HS:** Quan sát kết quả hiển thị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận về tính tiện ích của phần mềm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy nhận xét: Phần mềm phân tích rất nhanh và chính xác.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu bài thực hành: Làm chủ các lệnh đa thức trên GeoGebra. | **Khởi động:**<br>GeoGebra CAS là phần mềm toán học mạnh mẽ giúp thực hiện các phép biến đổi đại số tự động. |

## B. HOẠT ĐỘNG 2: THỰC HÀNH CÁC LỆNH CƠ BẢN (25 phút)
### 1. Thực hành lệnh Khai triển Expand (12 phút)
- **Cú pháp:** Nhập vào dòng lệnh CAS: `Expand((2x - 3y)^3)` rồi nhấn Enter.
- **Kết quả:** `$8x^3 - 36x^2y + 54xy^2 - 27y^3$`.
- **HS:** Tự lực nhập các biểu thức hằng đẳng thức bậc 2, bậc 3 vào máy tính.

### 2. Thực hành lệnh Phân tích nhân tử Factor (13 phút)
- **Cú pháp:** Nhập: `Factor(x^3 - 7x + 6)` rồi nhấn Enter.
- **Kết quả:** `$(x - 1)(x - 2)(x + 3)$`.
- **HS:** Nhập các bài toán phân tích đa thức trong SGK trang 43, 44 để đối chiếu kết quả làm tay.

## C. HOẠT ĐỘNG 3: LUYỆN TẬP PHÒNG MÁY (10 phút)
- **GV:** Phát phiếu thực hành gồm 4 biểu thức đa thức phức tạp.
- **HS:** Tự lực nhập lệnh trên GeoGebra và ghi kết quả vào phiếu.
- **GV:** Quan sát, hỗ trợ học sinh gặp lỗi cú pháp (thiếu dấu ngoặc hoặc dấu nhân `*`).

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
- Thảo luận về vai trò của công nghệ số: Phần mềm là công cụ trợ giúp đắc lực để kiểm tra, nhưng học sinh cần hiểu sâu bản chất biến đổi bằng tay để phát triển tư duy. Dặn dò chuẩn bị cho Chương V: Dữ liệu và biểu đồ.
"""

# 05. Bài 18: Thu thập và phân loại dữ liệu (Tiết 29, 30)
md_05 = """Tiết 29, 30 - BÀI 18: THU THẬP VÀ PHÂN LOẠI DỮ LIỆU
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm được các phương pháp thu thập dữ liệu: Thu thập trực tiếp (quan sát, đo đạc, làm thí nghiệm, phỏng vấn, lập phiếu khảo sát); Thu thập gián tiếp (từ sách báo, niên giám thống kê, mạng Internet, cơ sở dữ liệu số).
- Biết phân loại dữ liệu thành hai loại chính: Dữ liệu định tính (dữ liệu là chữ hoặc kí hiệu, không đo đếm được bằng số) và Dữ liệu định lượng (dữ liệu là số thực, đo đếm được).
- Hiểu được tính đại diện và độ tin cậy của dữ liệu thu thập được.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thiết kế một bảng hỏi khảo sát đơn giản.
- Giao tiếp và hợp tác: Hợp tác nhóm tiến hành thu thập số liệu trong lớp học.

b) Năng lực đặc thù môn Toán:
- Năng lực giải quyết vấn đề toán học: Lựa chọn phương pháp thu thập dữ liệu phù hợp với vấn đề cần nghiên cứu.

c) Năng lực số (NLS):
- ***1.1.TC2a: HS sử dụng Google Forms hoặc ứng dụng biểu mẫu số để tạo phiếu khảo sát thu thập dữ liệu trực tuyến; xuất dữ liệu sang bảng tính và phân loại dữ liệu số.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để gợi ý các câu hỏi khảo sát chuẩn mực và phân tích tính đại diện của mẫu khảo sát.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, khách quan trong thu thập và xử lí số liệu.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 1, KHBD, máy tính kết nối Internet, máy chiếu, biểu mẫu Google Forms mẫu.
2. Học sinh: SGK Toán 8, vở ghi, điện thoại thông minh hoặc máy tính phòng máy.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: Xuất phát từ nhu cầu khảo sát sở thích đọc sách của học sinh trong trường để hình thành bài học.
b) Nội dung: Trả lời câu hỏi: Làm thế nào để biết khối 8 thích đọc thể loại sách nào nhất?
c) Sản phẩm: Câu trả lời của HS: Phát phiếu điều tra hoặc lập biểu mẫu trực tuyến.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu vấn đề khảo sát sở thích đọc sách.<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy nêu phương án: Lập biểu mẫu Google Forms gửi vào nhóm lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương ý tưởng ứng dụng công nghệ số, dẫn dắt vào bài mới. | **Khởi động:**<br>Thu thập dữ liệu là bước đầu tiên và cốt lõi trong mọi nghiên cứu thống kê đời sống. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (50 phút)
### Hoạt động 2.1: Các phương pháp thu thập dữ liệu (25 phút - Tiết 29)
a) Mục tiêu: Phân biệt thu thập trực tiếp và thu thập gián tiếp.
b) Nội dung: Đọc mục 1 SGK trang 93-95; thực hiện HĐ1, HĐ2.
c) Sản phẩm: Bảng so sánh hai phương pháp thu thập trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu các tình huống:<br>  1. Đo chiều cao của các bạn trong lớp.<br>  2. Tìm kiếm số liệu dân số Việt Nam năm 2026.<br>  Hỏi: Tình huống nào thu thập trực tiếp, tình huống nào gián tiếp?<br>- **HS:** Đọc SGK và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ trả lời: Tình huống 1 là trực tiếp; tình huống 2 là gián tiếp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa khái niệm. | **1. Thu thập dữ liệu:**<br>- Trực tiếp: Phỏng vấn, điều tra, quan sát, đo đạc, làm thí nghiệm.<br>- Gián tiếp: Thu thập từ nguồn có sẵn (sách, báo, Internet, Tổng cục Thống kê). |

### Hoạt động 2.2: Phân loại dữ liệu định tính và định lượng (25 phút - Tiết 30)
a) Mục tiêu: Phân loại chính xác dữ liệu định tính và định lượng.
b) Nội dung: Đọc mục 2 SGK trang 96-98; làm Luyện tập 2.
c) Sản phẩm: Bảng phân loại dữ liệu của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu:<br>  + Dữ liệu định tính: Dạng chữ, không đo bằng số (ví dụ: giới tính, môn học yêu thích, mức độ hài lòng).<br>  + Dữ liệu định lượng: Dạng số thực (chiều cao, cân nặng, điểm số, nhiệt độ).<br>- **GV:** Yêu cầu HS phân loại danh sách dữ liệu trong Luyện tập 2.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân loại vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng ghi kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng phân loại. | **2. Phân loại dữ liệu:**<br>- Dữ liệu định tính: Dữ liệu không phải là số (thể loại phim, màu sắc, ý kiến đánh giá).<br>- Dữ liệu định lượng: Dữ liệu là số (số học sinh, nhiệt độ, thời gian chạy). |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (23 phút)
- Giải bài tập 5.1, 5.2, 5.3 SGK trang 98. Học sinh luyện tập nhận diện tính đại diện của mẫu khảo sát (ví dụ: muốn khảo sát thời gian tự học của học sinh toàn trường thì không thể chỉ hỏi các bạn học sinh giỏi trong lớp chuyên).

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
- **Tích hợp NLS 1.1.TC2a:** Hướng dẫn học sinh tạo biểu mẫu Google Forms đơn giản gồm 3 câu hỏi (1 câu định tính, 2 câu định lượng) để khảo sát thói quen sử dụng Internet của nhóm bạn. Dặn dò chuẩn bị cho Bài 19: Biểu diễn dữ liệu bằng bảng, biểu đồ.
"""

# 06. Bài 19: Biểu diễn dữ liệu bằng bảng, biểu đồ (Tiết 31, 32)
md_06 = """Tiết 31, 32 - BÀI 19: BIỂU DIỄN DỮ LIỆU BẰNG BẢNG, BIỂU ĐỒ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Biết cách biểu diễn dữ liệu thống kê bằng các bảng thống kê và các loại biểu đồ thích hợp: Biểu đồ cột đơn, biểu đồ cột kép, biểu đồ đoạn thẳng, biểu đồ hình quạt tròn.
- Lựa chọn được dạng biểu đồ phù hợp nhất với mục đích biểu diễn dữ liệu:
  + Biểu đồ cột: So sánh dữ liệu của các đối tượng khác nhau.
  + Biểu đồ đoạn thẳng: Thể hiện xu hướng biến động của dữ liệu theo thời gian.
  + Biểu đồ hình quạt tròn: Thể hiện cơ cấu, tỉ lệ phần trăm các thành phần so với toàn thể.
- Đọc và rút ra thông tin có ý nghĩa từ các biểu đồ đã cho.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát các dạng biểu đồ trong SGK, lựa chọn loại biểu đồ phù hợp.
- Giao tiếp và hợp tác: Hợp tác nhóm thực hành vẽ biểu đồ bằng công cụ số.

b) Năng lực đặc thù môn Toán:
- Năng lực biểu diễn toán học: Chuyển đổi dữ liệu từ bảng số liệu sang biểu đồ trực quan.

c) Năng lực số (NLS):
- ***3.1.TC2a: HS sử dụng phần mềm bảng tính Excel hoặc Google Sheets để nhập bảng dữ liệu và tự động tạo biểu đồ cột, biểu đồ đoạn thẳng, biểu đồ hình quạt tròn đẹp mắt.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để phân tích và đánh giá xem việc lựa chọn dạng biểu đồ đã tối ưu và chính xác về mặt trực quan hóa số liệu hay chưa.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn thận, chính xác và tư duy thẩm mỹ dữ liệu.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 1, KHBD, máy tính có phần mềm Excel, máy chiếu, các mẫu biểu đồ thống kê thực tế.
2. Học sinh: SGK Toán 8, vở ghi, thước kẻ, máy tính cầm tay, phòng máy tính.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: Kích hoạt nhu cầu trực quan hóa dữ liệu qua so sánh bảng số liệu và biểu đồ.
b) Nội dung: So sánh bảng số liệu doanh thu 12 tháng với biểu đồ đoạn thẳng, nhận xét xem hình thức nào giúp nhìn ra xu hướng tăng giảm nhanh hơn.
c) Sản phẩm: Câu trả lời của HS: Biểu đồ đoạn thẳng giúp nhìn ngay ra tháng nào cao nhất, thấp nhất và xu hướng đi lên hay đi xuống.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu bảng số liệu và biểu đồ đoạn thẳng cạnh nhau. Hỏi: Hình thức nào trực quan và dễ nhận xét hơn?<br>- **HS:** Quan sát và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy phát biểu: Biểu đồ trực quan và dễ so sánh hơn rất nhiều.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định vai trò của biểu đồ trong truyền thông dữ liệu, dẫn dắt vào bài mới. | **Khởi động:**<br>Biểu đồ là công cụ trực quan hóa dữ liệu mạnh mẽ, giúp người xem nắm bắt thông tin nhanh chóng và sâu sắc. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (50 phút)
### Hoạt động 2.1: Biểu diễn dữ liệu bằng bảng thống kê và biểu đồ cột, đoạn thẳng (25 phút - Tiết 31)
a) Mục tiêu: Nắm vững quy trình lập bảng thống kê và vẽ biểu đồ cột, đoạn thẳng.
b) Nội dung: Đọc mục 1 SGK trang 99-102; làm Luyện tập 1.
c) Sản phẩm: Bảng thống kê và biểu đồ cột học sinh vẽ vào vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn các thành phần của biểu đồ: Tên biểu đồ, trục nằm ngang (trục hoành), trục thẳng đứng (trục tung), gốc tọa độ, đơn vị đo, chú giải.<br>- **GV:** Cho bảng số liệu nhiệt độ trung bình các tháng tại Hà Nội. Yêu cầu vẽ biểu đồ đoạn thẳng.<br>- **HS:** Dùng thước vẽ vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định tọa độ các điểm và nối lại thành đường gấp khúc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ biểu đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy chuẩn vẽ biểu đồ đoạn thẳng. | **1. Biểu đồ cột và biểu đồ đoạn thẳng:**<br>- Biểu đồ cột: Dùng các cột chữ nhật để so sánh.<br>- Biểu đồ đoạn thẳng: Nối các điểm bằng đoạn thẳng để biểu diễn xu thế biến động theo thời gian. |

### Hoạt động 2.2: Biểu diễn dữ liệu bằng biểu đồ hình quạt tròn (25 phút - Tiết 32)
a) Mục tiêu: Nắm vững cách biểu diễn tỉ lệ phần trăm bằng biểu đồ quạt tròn.
b) Nội dung: Đọc mục 2 SGK trang 103-105; làm Luyện tập 2.
c) Sản phẩm: Biểu đồ hình quạt tròn và bảng phân bố tỉ lệ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn: Toàn bộ hình tròn biểu diễn $100\\%$ ($360^\\circ$). Tỉ lệ phần trăm của mỗi thành phần tương ứng với số đo cung hình quạt tròn: $n\\% \\rightarrow \\frac{n}{100} \\cdot 360^\\circ$.<br>- **GV:** Yêu cầu HS phân tích biểu đồ cơ cấu các loại cây trồng trong Luyện tập 2.<br>- **HS:** Đọc biểu đồ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu: Cây lúa chiếm tỉ lệ lớn nhất ($55\\%$), cây ngô ($25\\%$), hoa màu ($20\\%$).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách đọc biểu đồ quạt tròn. | **2. Biểu đồ hình quạt tròn:**<br>- Dùng để biểu diễn tỉ lệ phần trăm của từng thành phần so với tổng thể.<br>- Tổng các tỉ lệ phần trăm trên các hình quạt luôn bằng $100\\%$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (23 phút)
- Giải bài tập 5.6, 5.7 SGK trang 105. Lựa chọn dạng biểu đồ thích hợp nhất cho bảng số liệu về cơ cấu chi tiêu gia đình và bảng số liệu về số học sinh giỏi qua các năm học.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
- **Tích hợp NLS 3.1.TC2a:** Thực hành trên phòng máy tính: Nhập bảng số liệu vào Excel, chọn vùng dữ liệu, vào thẻ `Insert` $\\rightarrow$ `Chart` chọn tạo biểu đồ cột hoặc biểu đồ quạt tròn tức thời. Dặn dò chuẩn bị cho Bài 20: Phân tích số liệu thống kê.
"""

tasks = [
    ("03_KHBD_Toan8_BaiTapCuoiChuong2_Tiet27.md", md_03),
    ("04_KHBD_Toan8_HDTN_TinhToanDaThuc_GeoGebra_Tiet28.md", md_04),
    ("05_KHBD_Toan8_Bai18_ThuThapPhanLoaiDuLieu_Tiet29-30.md", md_05),
    ("06_KHBD_Toan8_Bai19_BieuDienDuLieuBangBieuDo_Tiet31-32.md", md_06),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
