**TIẾT 79 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: XÁC ĐỊNH TẦN SỐ, TẦN SỐ TƯƠNG ĐỐI, VẼ CÁC BIỂU ĐỒ BẰNG EXCEL**
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng thành thạo phần mềm bảng tính điện tử Microsoft Excel để:
  + Nhập liệu và sử dụng hàm `COUNTIF` để tự động đếm tần số của từng giá trị trong mẫu dữ liệu lớn.
  + Thiết lập công thức tính tần số tương đối bằng phép chia `=m/N*100`.
  + Tự động vẽ các biểu đồ thống kê chuyên nghiệp: Biểu đồ cột (Column Chart), biểu đồ đường thẳng (Line Chart) và Biểu đồ hình quạt tròn (Pie Chart).
  + Định dạng, gắn nhãn dữ liệu (Data Labels), tiêu đề biểu đồ (Chart Title) và ghi chú (Legend).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác nhập liệu bảng tính, xử lý lỗi công thức `#DIV/0!`, `#VALUE!`.
- Giao tiếp và hợp tác: Hợp tác nhóm tạo bài báo cáo thống kê trực quan bằng slide hoặc tệp Excel.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Chuyển đổi dữ liệu điều tra thực tế trong trường học thành biểu đồ phân tích trực quan.
- Năng lực số (NLS):
  + ***3.1.TC2a: HS sử dụng phần mềm bảng tính để nhập dữ liệu và tự động tạo biểu đồ tần số từ bảng số liệu cho trước; 5.2.TC2b: HS lựa chọn dạng biểu đồ thích hợp (cột, quạt tròn) để thể hiện trực quan thông tin dữ liệu.***

## 3. Về phẩm chất
- Rèn luyện kỹ năng tin học văn phòng hiện đại, tác phong làm việc khoa học, ngăn nắp.
- Tinh thần trung thực với số liệu thống kê.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài Microsoft Excel, tệp dữ liệu mẫu `Du_lieu_thong_ke_9.xlsx`, máy chiếu.
2. Học sinh: Máy vi tính phòng thực hành, vở ghi chép công thức hàm Excel.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ GIAO NHIỆM VỤ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Giới thiệu tập dữ liệu điều tra 100 học sinh về môn thể thao yêu thích và đặt nhiệm vụ xử lý trên Excel.
b) Nội dung: Mở tệp Excel chứa cột dữ liệu 100 dòng ghi tên các môn thể thao: Bóng đá, Bóng rổ, Cầu lông, Bơi lội, Cờ vua.
c) Sản phẩm: 100% học sinh mở được tệp dữ liệu trên máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS mở file dữ liệu 100 học sinh. Nêu nhiệm vụ: Dùng Excel tính tần số, tần số tương đối và vẽ biểu đồ hình quạt tròn.<br>- **HS:** Mở máy và mở tệp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát bảng dữ liệu 100 hàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS xác nhận tệp dữ liệu đã sẵn sàng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Bắt đầu hướng dẫn các hàm thống kê Excel. | Khởi động và nhận tệp dữ liệu thực hành Excel. |

## B. TIẾN HÀNH THỰC HÀNH TRÊN MÁY TÍNH (HOẠT ĐỘNG 2) (30 phút)
### Hoạt động 2.1: Sử dụng hàm COUNTIF và tính tần số tương đối (15 phút)
a) Mục tiêu: Sử dụng hàm `=COUNTIF(range, criteria)` và công thức phần trăm.
b) Nội dung: Nhập công thức đếm số học sinh thích từng môn thể thao và tính phần trăm.
c) Sản phẩm: Bảng tần số và tần số tương đối tự động hoàn chỉnh trên Excel.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cú pháp hàm:<br>- Tại ô tần số môn Bóng đá, nhập: `=COUNTIF($A$2:$A$101, "Bóng đá")`. Kéo công thức cho các môn còn lại.<br>- Tại ô tổng cộng: `=SUM(B2:B6)` (kết quả phải ra đúng 100).<br>- Tại cột tần số tương đối: `=B2/$B$7*100` hoặc định dạng ô dạng `%`.<br>- **HS:** Nhập công thức theo hướng dẫn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác trên bàn phím.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Kết quả tự động hiện ra ngay lập tức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giải thích ý nghĩa dấu `$` (địa chỉ tuyệt đối) để khi copy công thức vùng dữ liệu không bị trôi. | Sử dụng thành thạo hàm COUNTIF và công thức tính phần trăm trong Excel. |

### Hoạt động 2.2: Tự động vẽ Biểu đồ quạt tròn và Biểu đồ cột (15 phút)
a) Mục tiêu: Chèn biểu đồ Pie Chart và Column Chart, thêm nhãn dữ liệu phần trăm.
b) Nội dung: Chọn vùng dữ liệu $\rightarrow$ Insert $\rightarrow$ Charts $\rightarrow$ Pie $\rightarrow$ Chọn kiểu hiển thị phần trăm.
c) Sản phẩm: Biểu đồ quạt tròn và biểu đồ cột đẹp mắt trên trang tính Excel.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn vẽ biểu đồ:<br>1. Bôi đen cột Tên môn và cột Tần số tương đối.<br>2. Chọn thẻ `Insert` $\rightarrow$ Chọn biểu tượng `Pie Chart` (2D Pie).<br>3. Nhấp chọn `Chart Elements` ($+$) $\rightarrow$ Tích chọn `Data Labels` để hiển thị số phần trăm trên từng múi quạt.<br>4. Đổi tên tiêu đề: BIỂU ĐỒ SỞ THÍCH MÔN THỂ THAO.<br>- **HS:** Thao tác tạo biểu đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đổi màu sắc các phần quạt và tùy chỉnh định dạng chuyên nghiệp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trình chiếu sản phẩm của nhóm lên màn hình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao thẩm mỹ và kỹ năng tin học ứng dụng của học sinh. | Tạo biểu đồ hình quạt tròn và biểu đồ cột chuyên nghiệp trong Excel. |

## C. BÁO CÁO KẾT QUẢ VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (7 phút)
a) Mục tiêu: Chấm điểm bài thực hành của các tổ và nhận xét.
b) Nội dung: GV kiểm tra file Excel trên máy của từng nhóm học sinh.
c) Sản phẩm: Điểm số thực hành của các nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thu file Excel của các nhóm qua mạng nội bộ.<br>- **HS:** Ghi tên nhóm vào file và lưu tệp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Chiếu 2 bài làm nhanh và đẹp nhất lên máy chiếu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện nhóm thuyết minh ngắn gọn về kết quả thống kê.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Cho điểm tối đa các nhóm thao tác đúng và trình bày đẹp. | Đánh giá và chấm điểm hoạt động thực hành bảng tính Excel. |

## D. TỔNG KẾT VÀ DẶN DÒ (HOẠT ĐỘNG 4) (3 phút)
a) Mục tiêu: Tắt máy tính và dặn dò tiết HĐTN tiếp theo về Di truyền học Mendel.
b) Nội dung: Chuẩn bị kiến thức môn Sinh học về lai một cặp tính trạng của Men-đen.
c) Sản phẩm: HS ghi nhận nhiệm vụ liên môn Toán - Sinh học.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tắt máy tính an toàn. Dặn dò xem lại bài Di truyền học Men-đen lớp 9.<br>- **HS:** Thực hiện trật tự.<br><br>**+ Bước 2: Kết thúc buổi học**<br>- Cả lớp chào giáo viên ra về. | Tắt máy tính an toàn và dặn dò bài liên môn Sinh học tiếp theo. |