**TIẾT 75 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: GIẢI PHƯƠNG TRÌNH, HỆ PHƯƠNG TRÌNH. VẼ ĐỒ THỊ HÀM SỐ BẰNG PHẦN MỀM GEOGEBRA**
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng thành thạo phần mềm toán học động GeoGebra để:
  + Vẽ đồ thị hàm số bậc nhất $y = ax + b$ và hàm số bậc hai $y = ax^2$ ($a \neq 0$).
  + Tìm tọa độ giao điểm của Parabol và đường thẳng bằng công cụ `Intersect` (Giao điểm của hai đối tượng).
  + Giải phương trình bậc hai và hệ hai phương trình bậc nhất hai ẩn bằng lệnh giải đại số `Solve` trên cửa sổ CAS.
- Trực quan hóa mối liên hệ giữa nghiệm của phương trình và hoành độ giao điểm của các đồ thị tương ứng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác trên máy tính, nhập câu lệnh chính xác và tự sửa lỗi cú pháp.
- Giao tiếp và hợp tác: Chia sẻ kinh nghiệm tạo hiệu ứng đồ họa và thanh trượt Slider trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Kết hợp giữa góc nhìn đại số (CAS) và góc nhìn hình học (Graphics) để hiểu sâu sắc bản chất toán học.
- Năng lực số (NLS):
  + ***5.3.TC2a: HS sử dụng phần mềm GeoGebra để vẽ đồ thị hàm số và giải phương trình, quan sát sự thay đổi của đồ thị khi hệ số thay đổi; 3.1.TC2a: HS xuất ảnh đồ thị hoặc tệp GeoGebra trình bày báo cáo sản phẩm thực hành.***

## 3. Về phẩm chất
- Rèn luyện kỹ năng công nghệ số, làm quen với các công cụ toán học hiện đại.
- Ý thức giữ gìn thiết bị phòng máy vi tính của nhà trường.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn phần mềm GeoGebra (hoặc trình duyệt web truy cập geogebra.org/classic), máy chiếu, bài hướng dẫn thực hành.
2. Học sinh: Máy vi tính phòng thực hành, vở ghi bài thực hành.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ GIAO NHIỆM VỤ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Giới thiệu giao diện GeoGebra và giao nhiệm vụ thực hành cho từng nhóm học sinh.
b) Nội dung: GV giới thiệu thanh công cụ, vùng làm việc đồ họa (Graphics) và dòng nhập lệnh (Input / CAS).
c) Sản phẩm: 100% học sinh mở được phần mềm GeoGebra trên màn hình máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khởi động phần mềm GeoGebra. Phổ biến 3 nhiệm vụ:<br>1. Vẽ $(P): y = x^2$ và $(d): y = 2x + 3$.<br>2. Dùng công cụ Intersect xác định tọa độ giao điểm.<br>3. Mở cửa sổ CAS giải phương trình $x^2 - 2x - 3 = 0$.<br>- **HS:** Ngồi đúng vị trí máy tính được phân công.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mở phần mềm và làm quen giao diện.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các nhóm trưởng xác nhận máy tính hoạt động tốt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Bắt đầu tiến trình thực hành. | Khởi động phần mềm và nhận nhiệm vụ thực hành GeoGebra. |

## B. TIẾN HÀNH THỰC HÀNH TRÊN MÁY TÍNH (HOẠT ĐỘNG 2) (30 phút)
### Hoạt động 2.1: Vẽ đồ thị Parabol và Đường thẳng (15 phút)
a) Mục tiêu: Nhập lệnh vẽ hàm số và sử dụng Slider thay đổi tham số.
b) Nội dung: Nhập `f(x) = x^2` và `g(x) = 2x + 3`. Dùng lệnh `Intersect(f, g)` để tìm giao điểm.
c) Sản phẩm: Màn hình hiển thị Parabol, đường thẳng và hai điểm giao $A(-1; 1)$, $B(3; 9)$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn tại dòng lệnh Input:<br>- Nhập: `y = x^2` rồi ấn Enter.<br>- Nhập: `y = 2x + 3` rồi ấn Enter.<br>- Chọn công cụ Giao điểm (Intersect) hoặc nhập `Intersect(y = x^2, y = 2x + 3)`.<br>- **HS:** Thao tác trên bàn phím.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát trên màn hình xuất hiện đường Parabol màu xanh và đường thẳng màu đỏ cắt nhau tại 2 điểm $A(-1; 1)$ và $B(3; 9)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS các nhóm kiểm tra chéo màn hình của nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét sự ăn khớp tuyệt đối giữa kết quả đại số giải tay và kết quả hình học trực quan trên GeoGebra. | Thao tác thành công vẽ đồ thị và xác định tọa độ giao điểm trên GeoGebra. |

### Hoạt động 2.2: Giải phương trình và hệ phương trình trên cửa sổ CAS (15 phút)
a) Mục tiêu: Sử dụng lệnh `Solve` trên màn hình tính toán hình thức CAS để giải phương trình bậc hai và hệ phương trình.
b) Nội dung: Vào Menu $\rightarrow$ View $\rightarrow$ CAS. Nhập `Solve(x^2 - 5x + 6 = 0)` và `Solve({2x + y = 5, x - y = 1})`.
c) Sản phẩm: Kết quả hiển thị nghiệm chính xác trên màn hình CAS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn mở cửa sổ CAS:<br>- Nhập: `Solve(x^2 - 5x + 6 = 0, x)` $\rightarrow$ Kết quả: $\{x = 2, x = 3\}$.<br>- Nhập: `Solve({2x + y = 5, x - y = 1}, {x, y})` $\rightarrow$ Kết quả: $\{x = 2, y = 1\}$.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thử nghiệm giải các phương trình có nghiệm căn thức phức tạp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** GeoGebra cho kết quả dạng căn thức chính xác tuyệt đối mà không bị làm tròn thập phân.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao khả năng tiếp thu công nghệ của học sinh. | Giải phương trình và hệ phương trình trên cửa sổ CAS của GeoGebra. |

## C. BÁO CÁO SẢN PHẨM VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (7 phút)
a) Mục tiêu: Các nhóm lưu tệp sản phẩm và chụp ảnh màn hình nộp báo cáo thực hành.
b) Nội dung: Xuất file ảnh đồ thị và nộp bài qua hệ thống mạng nội bộ trường học.
c) Sản phẩm: Tệp hình ảnh đồ thị hoàn chỉnh của các nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn lưu file `.ggb` và xuất file ảnh `.png`.<br>- **HS:** Thực hiện thao tác xuất file.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nộp tệp sản phẩm về máy giáo viên.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- GV trình chiếu 2 sản phẩm xuất sắc nhất lên màn hình lớn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương các nhóm hoàn thành nhanh và chính xác. | Báo cáo và đánh giá sản phẩm thực hành GeoGebra. |

## D. TỔNG KẾT VÀ DẶN DÒ (HOẠT ĐỘNG 4) (3 phút)
a) Mục tiêu: Tắt máy tính đúng quy trình và dặn dò ôn tập cuối học kì II.
b) Nội dung: Shutdown máy tính, tắt màn hình, kê lại ghế và dặn dò tiết ôn tập cuối kì tiếp theo.
c) Sản phẩm: Phòng máy gọn gàng, an toàn.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS tắt máy tính, xếp ghế gọn gàng.<br>- **HS:** Thực hiện trật tự.<br><br>**+ Bước 2: Dặn dò**<br>- **GV:** Chuẩn bị cho 2 tiết Ôn tập cuối HKII Đại số tiếp theo.<br><br>**+ Bước 3: Kết thúc buổi học**<br>- Cả lớp chào giáo viên ra về. | Tắt máy tính an toàn và dặn dò ôn tập cuối kì. |