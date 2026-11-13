TIẾT 78 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: MÔ TẢ THÍ NGHIỆM NGẪU NHIÊN VỚI PHẦN MỀM EXCEL
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng hàm sinh số ngẫu nhiên `=RANDBETWEEN(bottom, top)` trong phần mềm Microsoft Excel để mô phỏng tự động hàng trăm, hàng nghìn lần phép thử gieo xúc xắc hoặc tung đồng xu.
- Sử dụng hàm đếm có điều kiện `=COUNTIF(range, criteria)` để thống kê tần số xuất hiện của từng mặt xúc xắc.
- Tính xác suất thực nghiệm tự động và vẽ biểu đồ hình cột so sánh tần số xuất hiện của các mặt.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự nhập các công thức hàm vào bảng tính Excel và sao chép công thức nhanh chóng bằng thao tác kéo chuột (Fill Handle).
- Giao tiếp và hợp tác: Làm việc nhóm hỗ trợ nhau xử lý lỗi công thức và tùy biến biểu đồ cột đẹp mắt.

b) Năng lực đặc thù môn Toán:
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng công nghệ thông tin và bảng tính điện tử để giải quyết bài toán mô phỏng toán học thực nghiệm.
- Năng lực tư duy và lập luận toán học: Nhận xét sự san bằng tần số của 6 mặt xúc xắc khi số lần mô phỏng tăng từ 100 lên 1000 lần.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng các hàm số RANDBETWEEN và COUNTIF trong Excel để xử lý dữ liệu thực nghiệm; 1.3.TC2a: HS lưu trữ và quản lý bảng tính khoa học.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu cách các nhà khoa học máy tính sử dụng các bộ tạo số giả ngẫu nhiên (Pseudo-random Number Generator) để huấn luyện AI.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, tác phong làm việc khoa học, ngăn nắp.
- Tinh thần hứng thú, say mê ứng dụng tin học vào giải quyết các bài toán toán học hiện đại.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn Microsoft Excel, máy chiếu, bài giảng hướng dẫn trực quan.
2. Học sinh: Máy vi tính phòng máy, sổ tay tin học, tài liệu SGK Toán 8 Tập 2 trang 71, 72.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề nếu muốn gieo xúc xắc $1000$ lần bằng tay sẽ mất rất nhiều thời gian, từ đó thấy được sức mạnh của phần mềm máy tính.
b) Nội dung: Gieo $1000$ lần xúc xắc bằng tay mất khoảng 1 tiếng, máy tính làm trong 1 giây.
c) Sản phẩm: Sự hào hứng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nếu thầy yêu cầu cả lớp gieo con xúc xắc 1000 lần và đếm số lần ra mặt 6 chấm thì mất bao lâu? Có công cụ nào làm việc đó trong chớp mắt không?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bằng tay rất lâu và mỏi. Dùng máy tính sẽ làm rất nhanh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài thực hành: Microsoft Excel sẽ giúp chúng ta mô phỏng 1000 lần gieo xúc xắc trong 1 giây. | Phần mềm bảng tính Excel là công cụ mạnh mẽ mô phỏng các thí nghiệm ngẫu nhiên quy mô lớn. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Các hàm ngẫu nhiên và đếm điều kiện trong Excel (10 phút)
a) Mục tiêu: Nắm vững cú pháp hàm `=RANDBETWEEN(1, 6)` và `=COUNTIF(vùng, điều kiện)`.
b) Nội dung: Cú pháp và ý nghĩa của hai hàm Excel quan trọng.
c) Sản phẩm: Vở ghi bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cú pháp:<br>  + `=RANDBETWEEN(1, 6)`: Sinh ngẫu nhiên một số nguyên từ 1 đến 6 (mô phỏng 1 lần gieo xúc xắc).<br>  + `=COUNTIF(A1:A1000, 1)`: Đếm số lần xuất hiện số 1 trong vùng dữ liệu từ ô A1 đến A1000.<br>- **HS:** Ghi chép cú pháp hàm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khởi động Excel trên máy tính cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhập thử nghiệm hàm tại ô đầu tiên.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở lưu ý: Dấu ngăn cách trong hàm có thể là dấu phẩy `,` hoặc dấu chấm phẩy `;` tùy cài đặt máy tính. | **Cú pháp hàm Excel:**<br>- Sinh số ngẫu nhiên: `=RANDBETWEEN(1, 6)`.<br>- Đếm số lần: `=COUNTIF(A1:A1000, 6)`. |

### Hoạt động 2.2: Quy trình 3 bước thực hiện trên bảng tính (10 phút)
a) Mục tiêu: Nắm vững quy trình: 1. Tạo cột số ngẫu nhiên; 2. Lập bảng thống kê tần số; 3. Tính tỉ số xác suất thực nghiệm.
b) Nội dung: Các bước thao tác từ ô A1 kéo xuống A1000, lập bảng tại vùng C1:D7.
c) Sản phẩm: Bảng tính hoàn chỉnh trên màn hình máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn 3 bước:<br>  1. Tại ô A1 gõ `=RANDBETWEEN(1, 6)`, dùng chuột kéo chốt Fill Handle xuống đến ô A1000.<br>  2. Tại cột C ghi các mặt từ 1 đến 6. Tại cột D dùng hàm COUNTIF đếm số lần.<br>  3. Tại cột E tính xác suất thực nghiệm: `=D1/1000` và đổi sang định dạng $\%$.<br>- **HS:** Thao tác tuần tự trên máy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhấn phím F9 để quan sát số liệu tự động nhảy ngẫu nhiên mỗi lần tính toán lại.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Thích thú khi thấy xác suất mỗi mặt luôn dao động quanh mức $16{,}7\% = \frac{1}{6}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Đây chính là bằng chứng thực nghiệm của định luật số lớn. | Học sinh thao tác kéo sao chép công thức 1000 dòng thành thạo, bảng số liệu tự động cập nhật khi nhấn F9. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vẽ biểu đồ cột trực quan biểu diễn số lần xuất hiện của 6 mặt xúc xắc trong Excel.
b) Nội dung: Chọn vùng dữ liệu C1:D7 $\rightarrow$ Insert $\rightarrow$ Column Chart.
c) Sản phẩm: Biểu đồ cột rực rỡ trên màn hình của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn vẽ biểu đồ: Bôi đen bảng tần số $\rightarrow$ Vào Menu Insert $\rightarrow$ Chọn Column Chart $\rightarrow$ Chọn kiểu cột 2D Clustered Column. Đổi tiêu đề biểu đồ thành: "KẾT QUẢ 1000 LẦN GIEO XÚC XẮC".<br>- **HS:** Thực hiện vẽ biểu đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tùy biến màu sắc các cột biểu đồ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Chiếu các biểu đồ đẹp của học sinh lên màn hình lớn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét độ cao của 6 cột xấp xỉ ngang nhau, khẳng định tính đồng khả năng tuyệt đối của 6 mặt. | Biểu đồ cột hoàn thiện chuẩn xác, thể hiện độ cao các cột xấp xỉ bằng nhau quanh mức 160 - 170 lần. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Lưu và nộp tệp bài làm thực hành Excel.
b) Nội dung: Lưu tệp `Toan8_NhomX_MoPhongExcel.xlsx` vào thư mục chung của lớp.
c) Sản phẩm: Tệp bảng tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS lưu tệp bài làm và nộp lên mạng nội bộ.<br>- **HS:** Thao tác File $\rightarrow$ Save As.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tắt máy vi tính, sắp xếp bàn ghế gọn gàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp kiểm tra phòng máy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương tinh thần học tập nghiêm túc, dặn dò chuẩn bị cho đợt Ôn tập học kì II ở các tiết sau. | 100% học sinh hoàn thành bài thực hành và nộp tệp Excel thành công. |
