TIẾT 69, 70 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: ỨNG DỤNG CỦA HÀM SỐ BẬC NHẤT TRONG TÀI CHÍNH VÀ VẼ ĐỒ THỊ VỚI PHẦN MỀM GEOGEBRA
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng hàm số bậc nhất $y = ax + b$ để mô hình hóa và phân tích các bài toán tài chính đời sống: Giá cước vận chuyển, tính điểm hòa vốn (Break-even Point), phân tích doanh thu và chi phí sản xuất.
- Sử dụng thành thạo phần mềm hình học động GeoGebra để:
  + Nhập và tính toán các phép biến đổi trên phân thức đại số;
  + Vẽ đồ thị của hàm số bậc nhất và xác định trực quan tọa độ giao điểm của hai đường thẳng;
  + Tạo thanh trượt (Slider) để khảo sát sự biến thiên của đồ thị hàm số khi hệ số $a, b$ thay đổi.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác các lệnh trên GeoGebra, khám phá các tính năng đồ họa và bảng tính đại số.
- Giao tiếp và hợp tác: Làm việc nhóm thiết kế bảng tính so sánh chi phí đi taxi giữa các hãng khác nhau và thuyết trình đề xuất lựa chọn kinh tế nhất.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Chuyển đổi bảng giá dịch vụ thực tế thành hệ các hàm số bậc nhất trên cùng một mặt phẳng tọa độ.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng công nghệ thông tin giải quyết nhanh các bài toán toán học phức tạp.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS chọn mô phỏng đồ thị hàm số trên GeoGebra để xác định điểm hòa vốn; 1.3.TC2a: HS tổ chức số liệu chi phí vào bảng tính phân tích tự động.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu cách AI sử dụng mô hình tối ưu hóa đồ thị tuyến tính để phân bổ tài nguyên kinh tế thông minh.***

## 3. Về phẩm chất
- Rèn luyện tư duy thực tế, tính toán chi tiêu thông thái và tiết kiệm trong sinh hoạt.
- Tinh thần say mê ứng dụng toán học và công nghệ vào giải quyết các bài toán đời sống.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn phần mềm GeoGebra (hoặc bản GeoGebra Online), máy chiếu, bảng giá cước taxi thực tế của 3 hãng xe lớn.
2. Học sinh: Máy vi tính phòng máy, sổ tay ghi chép, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (10 phút)
a) Mục tiêu: Đặt bài toán lựa chọn hãng taxi kinh tế nhất cho chuyến đi tham quan của gia đình.
b) Nội dung: Hãng taxi A có giá mở cửa $10\,000$ đồng và $14\,000$ đồng$/\text{km}$ tiếp theo. Hãng B không có giá mở cửa nhưng tính đồng giá $16\,000$ đồng$/\text{km}$. Đi bao nhiêu km thì giá tiền hai hãng bằng nhau? Đi xa thì nên chọn hãng nào?
c) Sản phẩm: Sự hào hứng tranh luận của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán so sánh chi phí của hai hãng taxi A và B. Hướng dẫn lập hai hàm số bậc nhất tương ứng: $y_A = 14x + 10$ và $y_B = 16x$ (đơn vị nghìn đồng).<br>- **HS:** Đọc đề và thảo luận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho hai hàm số bằng nhau: $14x + 10 = 16x \Rightarrow 2x = 10 \Rightarrow x = 5\text{ km}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nếu đi đúng $5\text{ km}$ thì giá hai hãng bằng nhau ($80\,000$ đồng). Nếu đi trên $5\text{ km}$ thì hãng A rẻ hơn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài thực hành: Hôm nay chúng ta sẽ dùng GeoGebra để vẽ đồ thị và trực quan hóa điểm cắt nhau này trong chớp mắt. | Điểm cắt nhau của hai đường thẳng chính là điểm hòa vốn để ra quyết định kinh tế tối ưu. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (35 phút)
### Hoạt động 2.1: Thực hành tính toán phân thức trên GeoGebra CAS (15 phút)
a) Mục tiêu: Sử dụng vùng tính toán biểu thức đại số (CAS) của GeoGebra để rút gọn phân thức tự động.
b) Nội dung: Nhập lệnh Simplify và Factor trên GeoGebra để rút gọn các phân thức cồng kềnh.
c) Sản phẩm: Thao tác thành thạo của học sinh trên máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn mở vùng CAS trong GeoGebra: Vào Menu View $\rightarrow$ Chọn CAS. Nhập lệnh: `Simplify((x^2 - 4)/(x^2 + 2x))` và quan sát kết quả tự động xuất ra `(x - 2)/x`.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự thực hành nhập các phân thức của Bài tập cuối chương VI để kiểm tra kết quả tính tay.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác nhận kết quả máy tính khớp hoàn toàn với bài làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định: GeoGebra là công cụ kiểm tra đắc lực giúp học sinh tự học và tự soát lỗi hiệu quả. | Sử dụng thành thạo lệnh `Simplify` và `Factor` trong môi trường GeoGebra CAS để xử lý phân thức đại số. |

### Hoạt động 2.2: Vẽ đồ thị hàm số và xác định giao điểm bằng GeoGebra (20 phút)
a) Mục tiêu: Biết cách nhập hàm số vào thanh Input và dùng công cụ Intersect tìm giao điểm đồ thị.
b) Nội dung: Nhập hai hàm số cước taxi $f(x) = 14x + 10$ và $g(x) = 16x$.
c) Sản phẩm: Hình vẽ hai đường thẳng cắt nhau tại điểm $(5; 80)$ trên màn hình máy tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn:<br>  1. Nhập vào ô lệnh: `f(x) = 14x + 10` (nhấn Enter).<br>  2. Nhập tiếp: `g(x) = 16x` (nhấn Enter).<br>  3. Chọn công cụ Điểm $\rightarrow$ "Intersect" (Giao điểm của hai đối tượng) $\rightarrow$ Nhấp lần lượt vào hai đường thẳng. Quan sát tọa độ giao điểm $A(5; 80)$ xuất hiện trên Vùng đại số.<br>- **HS:** Thực hiện thao tác trên máy tính cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát đồ thị: Với $x < 5$, đường $g(x)$ nằm dưới đường $f(x)$ (hãng B rẻ hơn); với $x > 5$, đường $f(x)$ nằm dưới (hãng A rẻ hơn).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Thuyết minh sự so sánh trực quan qua màu sắc hai đường thẳng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương kỹ năng đọc đồ thị hình học xuất sắc của học sinh. | Tọa độ giao điểm $A(5; 80)$ thể hiện rõ tại $x = 5\text{ km}$ thì chi phí hai hãng bằng nhau là $80\,000$ đồng. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (35 phút)
a) Mục tiêu: Thực hành tạo thanh trượt (Slider) hệ số $a, b$ để khảo sát chuyển động của đường thẳng.
b) Nội dung: Tạo thanh trượt $a \in [-5; 5]$, $b \in [-5; 5]$ và vẽ đường thẳng $y = ax + b$.
c) Sản phẩm: Mô phỏng đồ thị động chuyển động theo thanh trượt của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn tạo Slider:<br>  1. Chọn công cụ Slider $\rightarrow$ Nhấp chuột tạo thanh trượt $a$ và thanh trượt $b$.<br>  2. Nhập lệnh vẽ hàm số: `y = ax + b`.<br>  3. Dùng chuột kéo rê thanh trượt $a$ để quan sát độ nghiêng thay đổi; kéo thanh trượt $b$ để quan sát đường thẳng tịnh tiến lên xuống song song với chính nó.<br>- **HS:** Thực hành tạo sản phẩm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hào hứng điều khiển các thanh trượt và quan sát đường thẳng xoay quanh điểm $(0; b)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Chiếu sản phẩm của các nhóm lên màn hình lớn phòng máy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá: Việc trực quan hóa giúp khắc sâu bản chất hình học của hệ số góc và tung độ gốc một cách tự nhiên, sâu sắc nhất. | Học sinh làm chủ công cụ Slider, hiểu sâu sắc ý nghĩa của hệ số góc $a$ và tung độ gốc $b$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Đóng gói và lưu sản phẩm thực hành trải nghiệm.
b) Nội dung: Học sinh lưu tệp `.ggb` và xuất ảnh poster phân tích tài chính cá nhân.
c) Sản phẩm: Tệp bài làm nộp lên hệ thống học tập của trường.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các nhóm lưu tệp: `Toan8_NhomX_TaiChinhGeoGebra.ggb` và xuất ảnh đồ thị nộp bài.<br>- **HS:** Thực hiện thao tác lưu tệp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thu dọn phòng máy, tắt máy vi tính gọn gàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp kiểm tra và báo cáo sĩ số nộp bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương tinh thần học tập sáng tạo, làm chủ công nghệ của cả lớp; dặn dò chuẩn bị bước sang Chương VIII: Xác suất biến cố ở tiết sau. | Hoàn thành xuất sắc 2 tiết thực hành trải nghiệm ứng dụng tài chính và phần mềm GeoGebra. |
