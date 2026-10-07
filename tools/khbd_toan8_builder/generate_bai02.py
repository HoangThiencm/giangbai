# -*- coding: utf-8 -*-
import os

OUT_DIR = "tools/khbd_toan8_builder"
os.makedirs(OUT_DIR, exist_ok=True)

bai_02_content = r"""Tiết 11 - LUYỆN TẬP CHUNG
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hoá và củng cố vững chắc các quy tắc nhân đơn thức với đa thức, nhân đa thức với đa thức, chia đơn thức cho đơn thức và chia đa thức cho đơn thức.
- Rèn luyện kỹ năng rút gọn biểu thức, tìm điều kiện để đa thức chia hết cho đơn thức, và tìm đa thức chưa biết.
- Vận dụng các phép tính đại số vào giải quyết bài toán thực tế (tính số tiền mua hàng, chuyển động).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức qua sơ đồ tư duy và chủ động hoàn thành các bài luyện tập.
- Giao tiếp và hợp tác: Tương tác nhóm hiệu quả, biết lắng nghe và phản biện khi giải các bài toán rút gọn phức tạp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phân tích cấu trúc biểu thức để lựa chọn thứ tự thực hiện phép tính hợp lý.
- Năng lực giải quyết vấn đề toán học: Chuyển đổi ngôn ngữ thực tế thành mô hình toán học (biểu thức đại số).

c) Năng lực số (NLS):
- **1.2.TC2b:** HS thực hiện diễn giải thông tin kết quả phép tính đa thức từ tài liệu số.
- **2.4.TC2a:** HS lựa chọn quy trình hợp tác số để cùng hoàn thành các thử thách nhóm.
- **5.2.TC2b:** HS lựa chọn công cụ số phù hợp để kiểm tra tính đúng đắn của phép chia.

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác trong biến đổi đại số và tính toán dấu.
- Tự tin, kiên trì vượt qua các bài toán có nhiều bước biến đổi.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Kết nối tri thức, Kế hoạch bài dạy, bài giảng điện tử, sơ đồ tư duy dạng ảnh, máy vi tính, Tivi/máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay Casio/Vinacal, bảng nhóm học tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy, tái hiện nhanh các quy tắc nhân và chia đa thức cho đơn thức.
b) Nội dung: Trò chơi tiếp sức "Ghép đôi quy tắc" qua 4 câu hỏi trắc nghiệm tương tác nhanh.
c) Sản phẩm: Câu trả lời chính xác của các đội về công thức nhân và chia đa thức.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu hỏi ghép đôi quy tắc:<br>1) $A(B + C) = ...$<br>2) $(A + B)(C + D) = ...$<br>3) $x^m : x^n = ...$<br>4) $(A + B) : C = ...$<br>- **HS:** Chuẩn bị tinh thần tham gia trò chơi tiếp sức theo bàn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đại diện các bàn đứng tại chỗ trả lời nhanh nối tiếp nhau.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu đáp án ghép đôi tương ứng:<br>1) $AB + AC$; 2) $AC + AD + BC + BD$; 3) $x^{m-n}$ ($m \ge n$); 4) $A:C + B:C$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ phản xạ của học sinh, giới thiệu vào tiết Luyện tập chung để rèn luyện kỹ năng phối hợp các phép tính. | **Khởi động nhanh: Bốn quy tắc cốt lõi**<br>1) Nhân đơn thức với đa thức: $A(B + C) = AB + AC$.<br>2) Nhân đa thức với đa thức: $(A+B)(C+D) = AC + AD + BC + BD$.<br>3) Chia luỹ thừa cùng biến: $x^m : x^n = x^{m-n}$ ($m \ge n, x \ne 0$).<br>4) Chia đa thức cho đơn thức: $(A+B) : C = A:C + B:C$ (khi mọi hạng tử của $A, B$ chia hết cho $C$). |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức (10 phút)
a) Mục tiêu: Khái quát hoá kiến thức phép nhân và chia đa thức cho đơn thức thông qua sơ đồ tư duy trực quan; tích hợp chỉ báo NLS 1.2.TC2b.
b) Nội dung: Quan sát và phân tích sơ đồ tư duy hệ thống hóa phép nhân, phép chia đa thức cho đơn thức.
![Sơ đồ tư duy Phép nhân và phép chia đa thức cho đơn thức](khbd-ill:mindmap_toan8_chuong1_luyentap)
c) Sản phẩm: Bản ghi hệ thống hoá kiến thức của HS trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu sơ đồ tư duy tổng kết các nhánh kiến thức trọng tâm của bài nhân và chia đa thức lên màn hình.<br>- **GV:** Yêu cầu HS quan sát sơ đồ và nêu mối liên hệ giữa điều kiện chia hết và quy tắc thực hiện.<br>- **HS:** Quan sát sơ đồ tư duy trên màn hình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 3 nhánh chính: Nhánh 1 (Nhân đơn/đa thức); Nhánh 2 (Chia đơn thức cho đơn thức); Nhánh 3 (Chia đa thức cho đơn thức).<br>- ***(Tích hợp NLS 1.2.TC2b: HS thực hiện diễn giải thông tin kết quả phép tính đa thức từ tài liệu số: đọc hiểu sơ đồ số hoá, trình bày mạch lạc điều kiện số mũ biến và các bước nhân, chia theo luồng chỉ dẫn).***<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Gọi 1 HS đại diện tóm tắt lại toàn bộ sơ đồ trong 2 phút.<br>- **HS:** Trình bày rõ ràng, nhấn mạnh điều kiện số mũ $m \ge n$ và việc phân phối dấu trừ khi chia.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi phần diễn giải của HS, nhấn mạnh sơ đồ tư duy là công cụ giúp ghi nhớ logic, chuyển sang phần luyện giải bài tập trọng tâm. | **Hệ thống kiến thức trọng tâm (Sơ đồ tư duy):**<br>- **Nhánh 1: Phép nhân đa thức**<br>+ Phân phối hệ số và luỹ thừa biến: $x^m \cdot x^n = x^{m+n}$.<br>+ Đa thức nhân đa thức: nhân từng hạng tử rồi thu gọn đồng dạng.<br>- **Nhánh 2: Chia đơn thức cho đơn thức**<br>+ Điều kiện: Mọi biến trong số chia đều có trong số bị chia với số mũ không lớn hơn.<br>+ Công thức: $ax^m : bx^n = (a:b)x^{m-n}$.<br>- **Nhánh 3: Chia đa thức cho đơn thức**<br>+ Chia từng hạng tử rồi cộng kết quả.<br>+ Chú ý dấu âm của từng số hạng để tránh sai sót. |

### 2. Hoạt động 2.2: Giải quyết bài tập (22 phút)
a) Mục tiêu: HS thành thạo kỹ năng rút gọn biểu thức, tìm điều kiện chia hết và tìm đa thức chưa biết; tích hợp chỉ báo NLS 2.4.TC2a và 5.2.TC2b.
b) Nội dung: HS làm việc với Ví dụ 1, Ví dụ 2 (SGK trang 25), Bài tập 1.33, 1.34, 1.36.
c) Sản phẩm: Lời giải chi tiết các bài tập trong vở HS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chia lớp thành 4 nhóm thực hiện các nhiệm vụ:<br>+ Nhóm 1 & 2: Phân tích Ví dụ 1 và làm Bài tập 1.33 (chứng minh biểu thức không phụ thuộc vào $y$).<br>+ Nhóm 3 & 4: Phân tích Ví dụ 2 và làm Bài tập 1.34 (rút gọn biểu thức tổng hợp) cùng Bài tập 1.36.<br>- **HS:** Nhận nhiệm vụ, phân công trong nhóm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm làm việc tích cực, thực hiện biến đổi đại số.<br>- ***(Tích hợp NLS 2.4.TC2a: HS lựa chọn quy trình hợp tác số để cùng hoàn thành các thử thách nhóm: các nhóm dùng bảng nhóm điện tử hoặc máy tính bảng kết nối để chia sẻ các bước giải, cùng phát hiện và sửa lỗi tính toán cho nhau).***<br>- ***(Tích hợp NLS 5.2.TC2b: HS lựa chọn công cụ số phù hợp để kiểm tra tính đúng đắn của phép chia: sử dụng máy tính cầm tay bấm phím CALC để gán giá trị bất kỳ của $x, y$ kiểm tra biểu thức rút gọn có khớp với biểu thức ban đầu).***<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện các nhóm lên trình bày bài giải.<br>- **HS:** Nhóm 1 trình bày Bài 1.33: Sau khi nhân phân phối và thu gọn, biểu thức chỉ còn chứa biến $x$, biến $y$ triệt tiêu hoàn toàn.<br>- **HS:** Nhóm 3 trình bày Bài 1.34: Tách riêng phần nhân và phần chia đa thức, sau đó thu gọn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài giải chuẩn xác từng bước. | **1. Ví dụ 1 (SGK trang 25):**<br>$T = (5xy - 4y^2)(3x^2 + 4xy) - 15xy(x+y)(x-y)$<br>$= 15x^3y + 20x^2y^2 - 12x^2y^2 - 16xy^3 - 15xy(x^2 - y^2)$<br>$= 15x^3y + 8x^2y^2 - 16xy^3 - 15x^3y + 15xy^3$<br>$= 8x^2y^2 - xy^3$.<br>Để $T : D = xy^2$, suy ra:<br>$D = (8x^2y^2 - xy^3) : xy^2 = 8x - y$.<br><br>**2. Ví dụ 2 (SGK trang 25):**<br>$A = 2x^2y^2 - 5xy^3$ và $B = 3x^m y^2$.<br>a) Để $A$ chia hết cho $B$, ta cần số mũ của $x$ trong $B$ không lớn hơn số mũ của $x$ trong từng hạng tử của $A$:<br>$m \le 2$ và $m \le 1$, suy ra $m \le 1$.<br>Vì $m$ là số nguyên dương nên $m = 1$.<br>b) Khi $m = 1$, ta có $B = 3xy^2$.<br>$A : B = (2x^2y^2 - 5xy^3) : 3xy^2 = \frac{2}{3}x - \frac{5}{3}y$.<br><br>**3. Bài tập 1.33 (SGK trang 25):**<br>$P = 5x(3x^2y - 2xy^2 + 1) - 3xy(5x^2 - 3xy) + x^2y^2$<br>$= 15x^3y - 10x^2y^2 + 5x - 15x^3y + 9x^2y^2 + x^2y^2$<br>$= (15x^3y - 15x^3y) + (-10x^2y^2 + 9x^2y^2 + x^2y^2) + 5x$<br>$= 5x$.<br>a) Biểu thức $P = 5x$ chỉ phụ thuộc vào biến $x$ mà không phụ thuộc vào biến $y$.<br>b) Khi $P = 10$, ta có $5x = 10$, suy ra $x = 2$.<br><br>**4. Bài tập 1.34 (SGK trang 25):**<br>Biểu thức:<br>$(3x^2 - 5xy - 4y^2)(2x^2 + y^2) + (2x^4y^2 + x^3y^3 + x^2y^4) : \left(\frac{1}{5}xy\right)$<br>Thực hiện phần 1: $6x^4 + 3x^2y^2 - 10x^3y - 5xy^3 - 8x^2y^2 - 4y^4$<br>$= 6x^4 - 10x^3y - 5x^2y^2 - 5xy^3 - 4y^4$.<br>Thực hiện phần 2:<br>$(2x^4y^2 + x^3y^3 + x^2y^4) : \left(\frac{1}{5}xy\right)$<br>$= 10x^3y + 5x^2y^2 + 5xy^3$.<br>Cộng hai phần lại:<br>$= (6x^4 - 10x^3y - 5x^2y^2 - 5xy^3 - 4y^4) + (10x^3y + 5x^2y^2 + 5xy^3)$<br>$= 6x^4 - 4y^4$.<br><br>**5. Bài tập 1.36 (SGK trang 26):**<br>a) $4x^3y^2 : B = -2xy$, suy ra:<br>$B = 4x^3y^2 : (-2xy) = -2x^2y$.<br>b) $(4x^3y^2 - 3x^2y^3) : B = -2xy + H$<br>$(4x^3y^2 - 3x^2y^3) : (-2x^2y) = -2xy + \frac{3}{2}y^2$.<br>Vậy $H = \frac{3}{2}y^2$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức vào giải quyết bài toán thực tế về số tiền mua hàng và chuyển động của rùa và thỏ.
b) Nội dung: HS giải Bài tập 1.35 và Bài tập 1.38 SGK trang 26.
c) Sản phẩm: Lời giải Bài 1.35 và Bài 1.38 trong vở của HS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế Bài 1.35: Bà Khanh dự định mua $x$ hộp sữa giá $y$ đồng/hộp. Đến cửa hàng thấy giảm 1500 đồng/hộp nên bà mua thêm 3 hộp. Tìm đa thức biểu thị tổng số tiền phải trả.<br>- **GV:** Nêu Bài 1.38: Chuyện Rùa chạy đua với Thỏ.<br>- **HS:** Đọc kỹ đề bài, phân tích các đại lượng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bài 1.35: Số hộp sữa thực tế mua là $x + 3$. Giá tiền mỗi hộp thực tế là $y - 1500$. Tổng số tiền là $(x + 3)(y - 1500)$.<br>- **HS:** Bài 1.38: Tính quãng đường Thỏ chạy và Rùa chạy.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trình bày kết quả Bài 1.35 và 1.38 lên bảng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán ứng dụng.<br>- **GV dặn dò về nhà:** Ôn tập toàn bộ Chương I, chuẩn bị cho tiết sau "Bài tập cuối chương I". | **Bài tập 1.35 (SGK trang 26):**<br>- Số hộp sữa bà Khanh đã mua là: $x + 3$ (hộp).<br>- Giá tiền mỗi hộp sau khi giảm là: $y - 1500$ (đồng).<br>- Đa thức biểu thị tổng số tiền bà Khanh phải trả là:<br>$S = (x + 3)(y - 1500) = xy - 1500x + 3y - 4500$ (đồng).<br><br>**Bài tập 1.38 (SGK trang 26):**<br>a) Vận tốc của Rùa là $v$ (m/phút). Vận tốc của Thỏ là $60v$ (m/phút).<br>- Quãng đường Thỏ đã chạy trong $t$ phút là:<br>$S_{\text{Thỏ}} = 60v \cdot t = 60vt$ (m).<br>- Quãng đường Rùa đã chạy trong $90t$ phút là:<br>$S_{\text{Rùa}} = v \cdot 90t = 90vt$ (m).<br>b) Quãng đường Rùa chạy gấp số lần quãng đường Thỏ chạy là:<br>$90vt : 60vt = \frac{90}{60} = 1,5$ (lần).<br><br>**Dặn dò tự học:**<br>- Hoàn thành các bài tập còn lại vào vở.<br>- Tự vẽ lại sơ đồ tư duy tóm tắt Chương I vào vở để chuẩn bị cho tiết Ôn tập cuối chương. |
"""

with open(os.path.join(OUT_DIR, "BAI_02.md"), "w", encoding="utf-8") as f:
    f.write(bai_02_content.strip())
print("Saved BAI_02.md")
