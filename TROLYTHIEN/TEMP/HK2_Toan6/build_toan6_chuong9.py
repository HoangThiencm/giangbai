# -*- coding: utf-8 -*-
"""
Script sinh 13 KHBD Chương IX: Dữ liệu và Xác suất thực nghiệm (Tiết 81 - 101) - Toán 6 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan6"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    {
        "filename": "31_KHBD_Toan6_Bai38_DuLieuVaThuThapDuLieu_Tiet81-82.md",
        "header": "TIẾT 81, 82 - BÀI 38: DỮ LIỆU VÀ THU THẬP DỮ LIỆU\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 81, 82 - BÀI 38: DỮ LIỆU VÀ THU THẬP DỮ LIỆU
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết dữ liệu là các thông tin thu thập được dưới nhiều hình thức: Số, chữ cái, hình ảnh, âm thanh,...
- Phân biệt dữ liệu là số (số liệu) và dữ liệu không phải là số.
- Biết các phương pháp thu thập dữ liệu phổ biến: Quan sát, đo đạc, làm thí nghiệm, phỏng vấn, lập bảng hỏi.
- Đánh giá tính hợp lí của dữ liệu thu thập được.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thiết kế bảng hỏi ngắn phỏng vấn các bạn trong lớp về sở thích đọc sách, chơi thể thao.
- Giao tiếp và hợp tác: Làm việc nhóm tổng hợp và kiểm tra tính hợp lí của các câu trả lời.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phát hiện các dữ liệu không hợp lí (ví dụ: tuổi học sinh lớp 6 là $50$ hoặc chiều cao là $-150\\text{ cm}$).
- Năng lực giải quyết vấn đề toán học: Thu thập số liệu thời gian tự học ở nhà của học sinh trong tuần.

c) Năng lực số (NLS):
- ***5.3.TC1a: Học sinh sử dụng Google Forms để tạo biểu mẫu khảo sát trực tuyến thu thập dữ liệu tự động từ các bạn trong lớp.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Ứng dụng trợ lý AI để phân loại và làm sạch dữ liệu bảng hỏi, loại bỏ các câu trả lời nhiễu hoặc không hợp lệ.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, khách quan khi thu thập và ghi chép số liệu điều tra.
- Tinh thần trách nhiệm, tôn trọng ý kiến cá nhân của người được phỏng vấn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, máy chiếu, các mẫu phiếu khảo sát thu thập dữ liệu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, điện thoại thông minh hoặc máy tính bảng kết nối Internet.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề từ thực tế muốn biết môn thể thao nào được yêu thích nhất lớp ta cần làm gì.
b) Nội dung: Trả lời câu hỏi: Làm thế nào để biết chính xác bạn thích chơi cầu lông, bóng đá hay bóng rổ?
c) Sản phẩm: Ý kiến đề xuất của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt vấn đề: Lớp trưởng muốn tổ chức giải thi đấu thể thao cho lớp. Làm thế nào để chọn được môn thể thao có nhiều bạn tham gia nhất?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cần hỏi từng bạn trong lớp và ghi lại số lượng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đó là công việc thu thập dữ liệu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Dữ liệu và các phương pháp thu thập dữ liệu. | Để đưa ra quyết định chính xác ta cần tiến hành thu thập và xử lý dữ liệu. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Dữ liệu và phân loại dữ liệu (35 phút)
a) Mục tiêu: Nhận biết dữ liệu và phân biệt dữ liệu là số với dữ liệu không phải là số.
b) Nội dung: Khái niệm dữ liệu, số liệu và phân loại.
c) Sản phẩm: Bảng phân loại dữ liệu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu khái niệm: Các thông tin thu thập được như: số, chữ, hình ảnh,... gọi là dữ liệu. Dữ liệu là số gọi là số liệu. Yêu cầu chỉ ra dữ liệu là số và không phải là số trong danh sách học sinh: Tên, Chiều cao, Giới tính, Điểm thi Toán.<br>- **HS:** Tiếp thu và phân loại.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết bảng phân loại vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Dữ liệu là số: Chiều cao, Điểm thi Toán; Dữ liệu không là số: Tên, Giới tính.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Số liệu có thể thực hiện các phép tính cộng, trừ, tính trung bình cộng. | **1. Dữ liệu và phân loại dữ liệu:**<br>- Các thông tin thu thập được gọi là dữ liệu.<br>- Dữ liệu gồm hai loại chính:<br>  + Dữ liệu là số (số liệu): Điểm số, chiều cao, cân nặng, nhiệt độ.<br>  + Dữ liệu không phải là số: Họ tên, giới tính, màu sắc, sở thích. |

### Hoạt động 2.2: Thu thập dữ liệu và tính hợp lí của dữ liệu (30 phút)
a) Mục tiêu: Biết các cách thu thập dữ liệu và cách kiểm tra tính hợp lí của số liệu.
b) Nội dung: Các phương pháp thu thập (quan sát, phỏng vấn, bảng hỏi, nguồn có sẵn) và tiêu chí đánh giá tính hợp lí.
c) Sản phẩm: Báo cáo phát hiện lỗi sai trong dữ liệu mẫu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu các phương pháp thu thập dữ liệu. Cho bảng số liệu nhiệt độ Sa Pa: $12^\\circ\\text{C}, 15^\\circ\\text{C}, -3^\\circ\\text{C}, 120^\\circ\\text{C}$. Hỏi: Giá trị nào không hợp lí? Vì sao?<br>- **HS:** Đọc kỹ các giá trị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phát hiện giá trị $120^\\circ\\text{C}$ không hợp lí vì nhiệt độ tự nhiên trên Trái Đất không thể nóng đến $120^\\circ\\text{C}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Cần kiểm tra tính hợp lí của dữ liệu theo các tiêu chí thực tiễn trước khi phân tích. | **2. Thu thập và tính hợp lí của dữ liệu:**<br>- Phương pháp thu thập: Quan sát, đo đạc, phỏng vấn, lập bảng hỏi, tra cứu tài liệu.<br>- Đánh giá tính hợp lí: Số liệu phải phù hợp với quy luật thực tế khách quan. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Xác định phương pháp thu thập dữ liệu phù hợp cho từng tình huống cụ thể.
b) Nội dung: Bài 9.1, 9.2 SGK trang 76.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu chọn phương pháp thu thập phù hợp cho các tình huống:<br>  a) Số lượng xe máy đi qua cổng trường trong 15 phút;<br>  b) Món ăn sáng yêu thích của các bạn trong lớp.<br>- **HS:** Nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** a) Dùng phương pháp quan sát và đếm; b) Dùng phương pháp phỏng vấn hoặc lập bảng hỏi.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt phương pháp tối ưu. | a) Quan sát, ghi chép và đếm trực tiếp.<br>b) Lập bảng hỏi hoặc phỏng vấn trực tiếp từng bạn. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng lập bảng thu thập số liệu thời gian ngủ của các thành viên trong gia đình.
b) Nội dung: Khảo sát thời gian ngủ trung bình mỗi đêm của các thành viên trong nhà.
c) Sản phẩm: Bảng ghi chép tại nhà của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập về nhà: Lập bảng thu thập số giờ ngủ mỗi đêm của bố, mẹ, anh chị em trong nhà trong 3 ngày cuối tuần.<br>- **HS:** Ghi chép yêu cầu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện phỏng vấn tại nhà.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Nộp báo cáo vào đầu tiết học sau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò HS chuẩn bị cho Bài 39: Bảng thống kê và biểu đồ tranh. | Thực hành thu thập số liệu thời gian ngủ của các thành viên trong gia đình. |
"""
    },
    {
        "filename": "32_KHBD_Toan6_Bai39_BangThongKeVaBieuDoTranh_Tiet83-84.md",
        "header": "TIẾT 83, 84 - BÀI 39: BẢNG THỐNG KÊ VÀ BIỂU ĐỒ TRANH\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 83, 84 - BÀI 39: BẢNG THỐNG KÊ VÀ BIỂU ĐỒ TRANH
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Biết cách lập bảng thống kê từ dãy dữ liệu thu thập được.
- Đọc và mô tả được các dữ liệu trên bảng thống kê và biểu đồ tranh.
- Nhận biết cấu tạo biểu đồ tranh: Biểu tượng/hình ảnh đại diện cho một số lượng cá thể nhất định; biết cách vẽ biểu đồ tranh.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đếm và chuyển đổi số liệu thô thành bảng thống kê có các hàng và cột khoa học.
- Giao tiếp và hợp tác: Làm việc nhóm vẽ biểu đồ tranh trực quan, sáng tạo biểu tượng sinh động.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Tính toán số lượng thực tế bằng cách nhân số biểu tượng với giá trị quy ước của mỗi biểu tượng.
- Năng lực giải quyết vấn đề toán học: Đọc hiểu các thông tin kinh tế, môi trường trình bày bằng biểu đồ tranh.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm bảng tính Excel hoặc Google Sheets để lập bảng thống kê và đếm tự động bằng hàm COUNTIF.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI tự động đề xuất các biểu tượng icon trực quan phù hợp với chủ đề biểu đồ tranh cần thiết kế.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, ngăn nắp, trình bày bảng biểu sạch đẹp, khoa học.
- Tinh thần sáng tạo và gu thẩm mỹ trong việc lựa chọn hình ảnh minh họa.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, bảng phụ, các mẫu biểu đồ tranh đẹp.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước kẻ, bút màu.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Trực quan hóa dữ liệu qua biểu tượng tranh ảnh để thấy tính hấp dẫn, dễ nhớ của biểu đồ tranh.
b) Nội dung: Quan sát bảng theo dõi thời tiết trong tuần với các biểu tượng ông mặt trời, đám mây, hạt mưa.
c) Sản phẩm: Nhận xét của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu bảng thời tiết có các icon mặt trời, đám mây mưa. So sánh với bảng chỉ toàn chữ viết thì bảng nào dễ nhìn, sinh động hơn?<br>- **HS:** Quan sát và so sánh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bảng có biểu tượng hình ảnh trực quan, dễ nhớ hơn rất nhiều.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Bảng thống kê và biểu đồ tranh. | Biểu đồ tranh sử dụng các biểu tượng giúp trực quan hóa số liệu một cách sinh động, dễ hiểu. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Bảng thống kê (35 phút)
a) Mục tiêu: Biết cách tổ chức dữ liệu vào bảng thống kê gồm các dòng và cột có tiêu đề rõ ràng.
b) Nội dung: Lập bảng thống kê xếp loại học tập của học sinh một tổ.
c) Sản phẩm: Bảng thống kê hoàn thiện trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho dãy dữ liệu điểm chữ của tổ 1 gồm 10 bạn: T, T, Đ, Đ, Đ, T, C, Đ, T, Đ (T: Tốt, Đ: Đạt, C: Cần cố gắng). Hướng dẫn lập bảng thống kê gồm 2 dòng: Xếp loại và Số học sinh.<br>- **HS:** Đếm và ghi nhận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kẻ bảng và điền số liệu: Tốt: 4, Đạt: 5, Cần cố gắng: 1. Tổng cộng: 10.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng kẻ bảng thống kê.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt cấu trúc chuẩn của một bảng thống kê. | **1. Bảng thống kê:**<br>- Bảng thống kê là cách trình bày dữ liệu dạng bảng gồm các dòng và cột với tiêu đề rõ ràng.<br>- Bảng phân loại điểm tổ 1:<br><br>| Xếp loại | Tốt | Đạt | Cần cố gắng |<br>| :--- | :---: | :---: | :---: |<br>| Số học sinh | 4 | 5 | 1 | |

### Hoạt động 2.2: Biểu đồ tranh (30 phút)
a) Mục tiêu: Hiểu quy ước biểu tượng trong biểu đồ tranh và cách tính số lượng tương ứng.
b) Nội dung: Đọc biểu đồ tranh số cây xanh trồng được của các lớp trong trường.
c) Sản phẩm: Lời giải bài tập đọc biểu đồ tranh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu biểu đồ tranh số cây trồng được của 4 khối lớp. Quy ước: Mỗi biểu tượng $\\bigstar$ tương ứng với $10$ cây xanh. Yêu cầu tính số cây của từng lớp khi biết số biểu tượng $\\bigstar$.<br>- **HS:** Quan sát quy ước và đếm biểu tượng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khối 6 có 5 ngôi sao: $5 \\cdot 10 = 50$ cây. Khối 7 có 4 ngôi sao: $4 \\cdot 10 = 40$ cây.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo kết quả tính toán.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Số lượng bằng số biểu tượng nhân với giá trị quy ước của một biểu tượng. | **2. Biểu đồ tranh:**<br>- Biểu đồ tranh sử dụng các biểu tượng hoặc hình ảnh để thể hiện dữ liệu.<br>- Cần chú ý phần chú giải: Mỗi biểu tượng đại diện cho bao nhiêu đối tượng.<br>- Ví dụ: Một biểu tượng $\\bigstar = 10$ cây xanh $\\Rightarrow 5$ biểu tượng $= 50$ cây xanh. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vẽ biểu đồ tranh biểu diễn số điểm $10$ của 4 bạn học sinh trong tháng.
b) Nội dung: Bài 9.6 SGK trang 81.
c) Sản phẩm: Biểu đồ tranh vẽ đẹp mắt trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho số điểm 10 của: Mai: 20; Lan: 25; Hùng: 15; Tuấn: 10. Chọn biểu tượng bông hoa $\\circledast$ đại diện cho 5 điểm 10 để vẽ biểu đồ tranh.<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính số bông hoa: Mai: 4; Lan: 5; Hùng: 3; Tuấn: 2. Kẻ bảng và vẽ biểu tượng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ biểu đồ tranh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá biểu đồ tranh rõ ràng, thẩm mỹ. | Biểu đồ tranh biểu diễn số điểm 10 với chú giải mỗi $\\circledast = 5$ điểm 10. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Ứng dụng biểu đồ tranh để trình bày kế hoạch đọc sách cá nhân theo tuần.
b) Nội dung: Học sinh thiết kế biểu đồ tranh số trang sách đã đọc mỗi ngày bằng biểu tượng quyển sách.
c) Sản phẩm: Bản phác thảo trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn HS cách theo dõi thói quen đọc sách bằng biểu đồ tranh với biểu tượng mỗi cuốn sách nhỏ đại diện cho 10 trang đọc được.<br>- **HS:** Ghi chép ý tưởng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thiết kế bảng theo dõi vào trang cuối vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chia sẻ ý tưởng với bạn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò chuẩn bị thước kẻ cho Bài 40: Biểu đồ cột. | Thiết kế biểu đồ tranh theo dõi thói quen đọc sách hàng ngày. |
"""
    },
    {
        "filename": "33_KHBD_Toan6_Bai40_BieuDoCot_Tiet85-86.md",
        "header": "TIẾT 85, 86 - BÀI 40: BIỂU ĐỒ CỘT\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 85, 86 - BÀI 40: BIỂU ĐỒ CỘT
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết cấu tạo của biểu đồ cột (Trục ngang ghi danh mục đối tượng, Trục đứng ghi số lượng theo thang đo, các cột có bề rộng bằng nhau, khoảng cách bằng nhau).
- Đọc và mô tả được dữ liệu từ biểu đồ cột; so sánh độ cao của các cột để rút ra kết luận.
- Biết cách vẽ biểu đồ cột từ bảng số liệu cho trước.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự chia tỉ lệ thang đo trên trục đứng hợp lí để vẽ các cột cân đối.
- Giao tiếp và hợp tác: Làm việc nhóm phân tích xu hướng biến động số liệu từ biểu đồ cột.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh chênh lệch giữa các đối tượng dựa trên độ cao của các cột.
- Năng lực giải quyết vấn đề toán học: Phân tích biểu đồ cột lượng mưa, dân số để rút ra nhận định kinh tế - xã hội.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm Excel hoặc GeoGebra tạo biểu đồ cột tự động từ bảng dữ liệu nhập vào.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Sử dụng AI để tạo các đoạn thuyết minh ngắn gọn, súc tích dựa trên biểu đồ cột doanh số bán hàng.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn thận trong việc chia vạch tỉ lệ trục đứng.
- Ý thức quan tâm đến các vấn đề môi trường, kinh tế thể hiện qua số liệu thống kê.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, thước thẳng, máy chiếu, các mẫu biểu đồ cột thực tế.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng có chia mm, bút màu.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: So sánh biểu đồ cột với biểu đồ tranh để thấy ưu điểm khi số liệu lớn và đa dạng.
b) Nội dung: Nếu số liệu là $157$ và $183$ thì biểu đồ tranh có vẽ thuận tiện không? Cần dùng biểu đồ nào?
c) Sản phẩm: Câu trả lời của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khi số liệu lớn và lẻ như $157, 183$, việc vẽ biểu đồ tranh rất khó khăn. Giải pháp nào tối ưu hơn?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Dùng độ cao của các cột hình chữ nhật để biểu diễn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Dùng biểu đồ cột.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Biểu đồ cột. | Biểu đồ cột cho phép biểu diễn các số liệu lớn và chính xác hơn thông qua độ cao của các cột. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Đọc và phân tích biểu đồ cột (35 phút)
a) Mục tiêu: Đọc chính xác giá trị tương ứng của mỗi cột và nhận xét so sánh giữa các cột.
b) Nội dung: Đọc biểu đồ cột số lượng huy chương của đoàn thể thao Việt Nam tại SEA Games.
c) Sản phẩm: Bảng số liệu trích xuất từ biểu đồ cột.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu biểu đồ cột và hướng dẫn cách đọc: Nhìn đỉnh cột dóng sang trục đứng để đọc số liệu. Cột nào cao hơn biểu thị số lượng nhiều hơn.<br>- **HS:** Quan sát và thực hành đọc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc số lượng huy chương Vàng, Bạc, Đồng và so sánh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo số liệu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Đỉnh của cột ứng với vạch nào trên trục thẳng đứng thì đó là số liệu của đối tượng ghi ở chân cột. | **1. Đọc biểu đồ cột:**<br>- Trục ngang: Ghi danh sách các đối tượng.<br>- Trục đứng: Ghi thang đo số lượng.<br>- Độ cao của cột biểu diễn số lượng của đối tượng tương ứng. |

### Hoạt động 2.2: Các bước vẽ biểu đồ cột (30 phút)
a) Mục tiêu: Nắm vững quy trình 4 bước vẽ biểu đồ cột.
b) Nội dung: 1. Vẽ hai trục vuông góc; 2. Chia vạch tỉ lệ trên trục đứng; 3. Vẽ các cột có bề rộng bằng nhau; 4. Ghi tiêu đề và số liệu.
c) Sản phẩm: Biểu đồ cột vẽ chuẩn xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn 4 bước vẽ biểu đồ cột trên bảng. Nhấn mạnh: Khoảng cách giữa các cột phải bằng nhau, độ rộng các cột bằng nhau.<br>- **HS:** Ghi chép 4 bước.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành vẽ biểu đồ cột biểu diễn số học sinh giỏi của 4 lớp 6A, 6B, 6C, 6D.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ biểu đồ cột.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa tỉ lệ vẽ. | **2. Các bước vẽ biểu đồ cột:**<br>- Bước 1: Vẽ trục ngang và trục đứng vuông góc.<br>- Bước 2: Chia tỉ lệ thích hợp trên trục đứng và ghi tên các đối tượng trên trục ngang.<br>- Bước 3: Vẽ các cột chữ nhật cách đều nhau, cùng bề rộng.<br>- Bước 4: Ghi tên biểu đồ, số liệu trên đỉnh cột (nếu cần). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Đọc và trả lời các câu hỏi phân tích từ biểu đồ cột doanh thu nhà sách.
b) Nội dung: Bài 9.11, 9.12 SGK trang 86.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu biểu đồ cột doanh số bán sách của nhà sách trong 5 ngày trong tuần. Yêu cầu cho biết:<br>  a) Ngày nào bán được nhiều sách nhất?<br>  b) Tổng số sách bán được trong cả 5 ngày là bao nhiêu?<br>- **HS:** Quan sát và tính toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cộng tổng các cột: $50 + 65 + 40 + 75 + 90 = 320$ cuốn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kết quả chính xác. | a) Ngày thứ Sáu bán được nhiều nhất (90 cuốn).<br>b) Tổng số sách bán được trong 5 ngày là: $320$ cuốn. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng biểu đồ cột để biểu diễn số giờ tự học trong tuần của bản thân.
b) Nội dung: Vẽ phác thảo biểu đồ cột số giờ học từ thứ Hai đến Chủ Nhật.
c) Sản phẩm: Biểu đồ cột cá nhân trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ vẽ biểu đồ cột theo dõi thời gian tự học của bản thân trong một tuần.<br>- **HS:** Tiếp nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phác thảo khung biểu đồ vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Nộp lại vào tiết sau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò chuẩn bị cho Bài 41: Biểu đồ cột kép. | Biểu đồ cột theo dõi thời gian tự học cá nhân trong một tuần. |
"""
    },
    {
        "filename": "34_KHBD_Toan6_Bai41_BieuDoCotKep_Tiet87-88.md",
        "header": "TIẾT 87, 88 - BÀI 41: BIỂU ĐỒ CỘT KÉP\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 87, 88 - BÀI 41: BIỂU ĐỒ CỘT KÉP
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết biểu đồ cột kép được sử dụng để so sánh từng cặp số liệu của hai đối tượng hoặc hai nhóm đối tượng cùng loại.
- Đọc và mô tả được dữ liệu từ biểu đồ cột kép; phân biệt hai cột kép nhờ màu sắc hoặc hoa văn kèm chú giải.
- Biết cách vẽ biểu đồ cột kép từ bảng số liệu hai dòng/hai cột tương ứng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát hai cột đứng liền kề để so sánh ngay đối tượng nào lớn hơn tại từng thời điểm.
- Giao tiếp và hợp tác: Thảo luận nhóm phân tích so sánh kết quả học tập giữa học kì I và học kì II.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh xu hướng tăng hay giảm của hai nhóm đối tượng theo thời gian.
- Năng lực giải quyết vấn đề toán học: Phân tích số liệu xuất khẩu - nhập khẩu, lượng mưa giữa hai thành phố.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm bảng tính Excel vẽ biểu đồ cột kép (Clustered Column) và tùy chỉnh màu sắc hai nhóm cột kèm nhãn dữ liệu.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI phân tích biểu đồ cột kép và đưa ra dự báo xu hướng phát triển trong tương lai.***

## 3. Về phẩm chất
- Cẩn thận, tỉ mỉ khi phân biệt màu sắc và vẽ hai cột sát nhau cho từng đối tượng.
- Tinh thần khách quan khi phân tích, đánh giá số liệu so sánh.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, máy chiếu, các mẫu biểu đồ cột kép so sánh.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng, bút màu (ít nhất 2 màu khác nhau).

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt tình huống cần so sánh điểm thi môn Toán của học sinh nam và học sinh nữ ở các lớp.
b) Nội dung: Làm thế nào để vừa nhìn thấy điểm số của nam, vừa thấy của nữ của từng lớp trên cùng một biểu đồ?
c) Sản phẩm: Đề xuất của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Để so sánh số học sinh nam và nữ xếp loại giỏi của 4 lớp 6A, 6B, 6C, 6D trên cùng một biểu đồ, ta nên làm thế nào?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ hai cột đứng cạnh nhau tại mỗi lớp, một cột tô màu xanh (nam), một cột tô màu đỏ (nữ).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Biểu đồ cột kép chính là công cụ hoàn hảo cho việc so sánh này. | Biểu đồ cột kép ghép từng cặp hai cột sát nhau giúp so sánh trực tiếp hai đối tượng cùng loại. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Đọc và phân tích biểu đồ cột kép (35 phút)
a) Mục tiêu: Đọc chính xác số liệu của từng đối tượng qua phần chú giải màu sắc.
b) Nội dung: Đọc biểu đồ cột kép so sánh nhiệt độ cao nhất và thấp nhất trong tuần tại Hà Nội.
c) Sản phẩm: Bảng số liệu trích xuất từ biểu đồ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu biểu đồ cột kép nhiệt độ. Hướng dẫn đọc: Cột màu đỏ là nhiệt độ cao nhất, cột màu xanh là nhiệt độ thấp nhất. Nhìn vào từng ngày để so sánh chênh lệch nhiệt độ trong ngày.<br>- **HS:** Quan sát và thực hành đọc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tìm ngày có nhiệt độ cao nhất, ngày có nhiệt độ thấp nhất và ngày có chênh lệch nhiệt độ lớn nhất.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Biểu đồ cột kép bắt buộc phải có phần Chú giải màu sắc hoặc hoa văn. | **1. Đọc biểu đồ cột kép:**<br>- Biểu đồ cột kép gồm các cặp cột sát nhau, mỗi cột biểu diễn một nhóm số liệu khác nhau.<br>- Bắt buộc phải có phần Chú giải để phân biệt ý nghĩa hai màu cột.<br>- Giúp so sánh trực quan hai nhóm số liệu tại từng mốc quan sát. |

### Hoạt động 2.2: Các bước vẽ biểu đồ cột kép (30 phút)
a) Mục tiêu: Nắm vững quy trình vẽ biểu đồ cột kép.
b) Nội dung: Vẽ từng cặp cột chữ nhật sát nhau tại mỗi đối tượng, khoảng cách giữa các cặp cột bằng nhau.
c) Sản phẩm: Biểu đồ cột kép hoàn thiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn các bước vẽ: Tại mỗi đối tượng trên trục ngang, vẽ liền kề hai cột hình chữ nhật có cùng bề rộng, một cột tô màu A, một cột tô màu B. Nhớ vẽ bảng chú giải ở góc trên biểu đồ.<br>- **HS:** Ghi chép quy trình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành vẽ biểu đồ cột kép so sánh số lượng học sinh giỏi môn Toán và môn Ngữ văn của 3 lớp 6A, 6B, 6C.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ hình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá tính chuẩn xác của các cột sát nhau và màu sắc phân biệt rõ ràng. | **2. Các bước vẽ biểu đồ cột kép:**<br>- Vẽ hai trục vuông góc và chia vạch tỉ lệ trục đứng.<br>- Tại mỗi mốc đối tượng trên trục ngang, vẽ 2 cột chữ nhật sát nhau có bề rộng bằng nhau.<br>- Tô màu hoặc kẻ sọc khác nhau cho 2 cột.<br>- Vẽ bảng Chú giải và ghi tên biểu đồ. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Phân tích so sánh số liệu hai năm liên tiếp từ biểu đồ cột kép.
b) Nội dung: Bài 9.15, 9.16 SGK trang 90.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho biểu đồ cột kép sản lượng lúa của hai tỉnh A và B trong hai năm 2020 và 2021. Yêu cầu so sánh tốc độ tăng trưởng sản lượng của hai tỉnh.<br>- **HS:** Đọc số liệu và tính hiệu số giữa hai năm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tỉnh A tăng từ $120$ lên $135$ nghìn tấn (tăng $15$). Tỉnh B tăng từ $110$ lên $130$ nghìn tấn (tăng $20$). Tỉnh B có mức tăng trưởng nhanh hơn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi năng lực lập luận và nhận định số liệu của học sinh. | Tỉnh B có mức tăng sản lượng lúa lớn hơn tỉnh A ($20 > 15$ nghìn tấn). |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng biểu đồ cột kép so sánh chi tiêu giữa hai tháng của gia đình.
b) Nội dung: So sánh tiền điện, tiền nước, tiền ăn giữa tháng 1 và tháng 2.
c) Sản phẩm: Bản kế hoạch vẽ biểu đồ ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ: Thu thập hóa đơn tiền điện, tiền nước tháng trước và tháng này của gia đình để chuẩn bị vẽ biểu đồ cột kép ở tiết Luyện tập chung.<br>- **HS:** Ghi chép bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lên kế hoạch thu thập số liệu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác nhận nhiệm vụ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò chuẩn bị cho Tiết 89 Luyện tập chung. | Thu thập số liệu chi tiêu điện nước của gia đình trong hai tháng. |
"""
    },
    {
        "filename": "35_KHBD_Toan6_LuyenTapChung_Tiet89.md",
        "header": "TIẾT 89 - LUYỆN TẬP CHUNG: EM SẼ LÀM GÌ TRONG TƯƠNG LAI? (TRANG 91)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 89 - LUYỆN TẬP CHUNG: EM SẼ LÀM GÌ TRONG TƯƠNG LAI? (TRANG 91)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố toàn bộ kỹ năng thu thập, phân loại, tổ chức dữ liệu vào bảng thống kê, biểu đồ tranh, biểu đồ cột và biểu đồ cột kép.
- Vận dụng biểu diễn và phân tích số liệu điều tra về ước mơ nghề nghiệp tương lai của học sinh.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa các dạng biểu đồ đã học qua sơ đồ tư duy; chủ động hoàn thành bảng điều tra nghề nghiệp.
- Giao tiếp và hợp tác: Làm việc nhóm tổng hợp số liệu nghề nghiệp của cả lớp và thuyết trình báo cáo.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phân tích cơ cấu nghề nghiệp yêu thích của các bạn học sinh; so sánh giữa nam và nữ.
- Năng lực mô hình hoá toán học: Sử dụng biểu đồ cột kép để so sánh sở thích nghề nghiệp giữa học sinh nam và nữ.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng bảng tính Google Sheets để vẽ biểu đồ cột kép phân tích khảo sát nghề nghiệp tương lai của lớp.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI tổng hợp các xu hướng nghề nghiệp mới nổi trong kỷ nguyên số để học sinh định hướng tương lai.***

## 3. Về phẩm chất
- Khơi dậy ước mơ, hoài bão và ý thức phấn đấu trong học tập để hiện thực hóa nghề nghiệp tương lai.
- Rèn luyện tính trung thực, cẩn trọng trong xử lý số liệu điều tra.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 89 (vector 300 DPI), tivi/máy chiếu, phiếu khảo sát nghề nghiệp.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước kẻ, bút màu.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tạo hứng thú học tập qua câu hỏi gợi mở về ước mơ nghề nghiệp tương lai của học sinh.
b) Nội dung: Quan sát các hình ảnh về các ngành nghề: Bác sĩ, Kỹ sư phần mềm AI, Giáo viên, Phi hành gia, Nghệ sĩ.
c) Sản phẩm: Sự hào hứng chia sẻ ước mơ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu các bức tranh sinh động về các ngành nghề trong xã hội hiện đại. Hỏi: Em ước mơ sau này sẽ làm nghề gì?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS chia sẻ ước mơ nghề nghiệp cá nhân.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt: Hôm nay chúng ta sẽ dùng toán học thống kê để khảo sát và vẽ bức tranh nghề nghiệp tương lai của lớp mình. | Ước mơ nghề nghiệp là động lực để học sinh nỗ lực rèn luyện mỗi ngày. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ các công cụ thống kê (Bảng thống kê, Biểu đồ tranh, Biểu đồ cột, Biểu đồ cột kép) qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 89; đối chiếu ưu điểm và trường hợp sử dụng của từng dạng biểu đồ.

![Sơ đồ tư duy Luyện tập chung Tiết 89](khbd-ill:mindmap-toan6-tiet89)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 89. Yêu cầu HS phân tích các nhánh: 1. Thu thập dữ liệu; 2. Bảng thống kê; 3. Biểu đồ tranh; 4. Biểu đồ cột; 5. Biểu đồ cột kép.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoạt động nhóm đôi so sánh: Khi nào nên dùng biểu đồ cột kép thay cho biểu đồ cột đơn?<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình ngắn gọn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Dùng biểu đồ cột kép khi cần so sánh trực diện hai nhóm đối tượng cùng tiêu chí. | **Hệ thống kiến thức thống kê:**<br>1. Thu thập: Số liệu và phi số liệu, tính hợp lí.<br>2. Bảng thống kê: Hàng và cột khoa học.<br>3. Biểu đồ tranh: Biểu tượng quy ước.<br>4. Biểu đồ cột: Thang đo trục đứng, độ cao cột.<br>5. Biểu đồ cột kép: Ghép cặp 2 cột sát nhau, có chú giải màu sắc để so sánh. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Thực hành lập bảng thống kê và vẽ biểu đồ cột kép khảo sát nghề nghiệp tương lai của lớp.
b) Nội dung: Thu thập số liệu 5 nhóm nghề của các bạn nam và nữ trong lớp, vẽ biểu đồ cột kép.
c) Sản phẩm: Bảng thống kê và biểu đồ cột kép trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát phiếu khảo sát nhanh cho 4 tổ: Chọn 1 trong 5 nghề (Bác sĩ, Giáo viên, Kỹ sư công nghệ, Kinh doanh, Khác). Thu thập số liệu phân theo Nam và Nữ.<br>- **HS:** Nhận phiếu và điền khảo sát.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tổ trưởng tổng hợp, kẻ bảng thống kê lớp và vẽ biểu đồ cột kép vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm lên bảng vẽ biểu đồ cột kép của lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét sản phẩm hoàn thiện, nhận định nghề nghiệp nào được bạn nam thích nhất, nghề nào bạn nữ thích nhất. | Hoàn thành bảng thống kê và biểu đồ cột kép khảo sát nghề nghiệp lớp học sinh động, chính xác. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Khơi gợi tinh thần học tập hướng nghiệp cho học sinh.
b) Nội dung: Giáo viên dặn dò kế hoạch học tập để theo đuổi ước mơ.
c) Sản phẩm: Suy nghĩ và mục tiêu cá nhân của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Để đạt được ước mơ nghề nghiệp đã chọn, em cần rèn luyện những năng lực và phẩm chất gì ngay từ năm học lớp 6 này?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi 3 mục tiêu rèn luyện vào cuối trang vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chia sẻ trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Động viên các em kiên trì học tập, chuẩn bị cho Bài 42: Kết quả có thể và sự kiện trong trò chơi, thí nghiệm. | Tinh thần học tập chủ động, rèn luyện tư duy logic để chuẩn bị cho tương lai. |
"""
    },
    {
        "filename": "36_KHBD_Toan6_Bai42_KetQuaCoTheVaSuKien_Tiet90.md",
        "header": "TIẾT 90 - BÀI 42: KẾT QUẢ CÓ THỂ VÀ SỰ KIỆN TRONG TRÒ CHƠI, THÍ NGHIỆM\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 90 - BÀI 42: KẾT QUẢ CÓ THỂ VÀ SỰ KIỆN TRONG TRÒ CHƠI, THÍ NGHIỆM
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết các kết quả có thể xảy ra trong một trò chơi hoặc thí nghiệm đơn giản (tung đồng xu, gieo xúc xắc, rút thẻ từ hộp).
- Nhận biết khái niệm sự kiện trong trò chơi, thí nghiệm; biết một sự kiện xảy ra hay không xảy ra khi thực hiện phép thử.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự liệt kê đầy đủ tất cả các kết quả có thể xảy ra mà không bỏ sót hoặc trùng lặp.
- Giao tiếp và hợp tác: Làm việc nhóm thực hành tung đồng xu hoặc gieo xúc xắc và ghi lại kết quả.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khẳng định tính ngẫu nhiên của kết quả trước khi thực hiện phép thử.
- Năng lực giải quyết vấn đề toán học: Phân tích các tình huống bốc thăm trúng thưởng trong thực tế đời sống.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng trình mô phỏng gieo xúc xắc trực tuyến hoặc hàm RANDBETWEEN trong Excel để mô phỏng 100 lần gieo xúc xắc tự động.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh tìm hiểu cách AI sử dụng lý thuyết xác suất ngẫu nhiên để dự đoán hành vi người dùng trong các trò chơi điện tử.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, tôn trọng kết quả thực nghiệm khách quan.
- Tinh thần hào hứng, vui vẻ khi tham gia các hoạt động trò chơi toán học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, đồng xu kim loại, con xúc xắc 6 mặt, hộp đựng thẻ số.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, mỗi nhóm chuẩn bị 1 đồng xu hoặc 1 con xúc xắc.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tạo hứng thú qua trò chơi tung đồng xu chọn sân trong trận bóng đá.
b) Nội dung: Trọng tài tung đồng xu trước trận đấu để làm gì? Có thể đoán trước chắc chắn mặt nào xuất hiện không?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trước trận bóng đá, trọng tài tung đồng xu để quyết định quyền chọn sân. Vì sao lại dùng cách này? Có thể biết trước mặt nào ngửa không?<br>- **HS:** Quan sát đồng xu và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vì đồng xu có 2 mặt cơ hội như nhau, không ai đoán trước được chắc chắn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Đây là ví dụ kinh điển về trò chơi ngẫu nhiên và các kết quả có thể. | Kết quả tung đồng xu là hoàn toàn ngẫu nhiên và công bằng cho cả hai đội. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Kết quả có thể của trò chơi, thí nghiệm (10 phút)
a) Mục tiêu: Biết cách liệt kê tập hợp tất cả các kết quả có thể của một phép thử đơn giản.
b) Nội dung: Liệt kê các mặt của đồng xu (Sấp - Ngửa) và các mặt của con xúc xắc (1, 2, 3, 4, 5, 6 chấm).
c) Sản phẩm: Vở ghi bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu: Khi tung một đồng xu một lần, có những kết quả nào có thể xảy ra? Khi gieo một con xúc xắc 6 mặt, có những kết quả nào?<br>- **HS:** Đọc SGK và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tung đồng xu có 2 kết quả: Mặt Sấp (S) hoặc Mặt Ngửa (N). Gieo xúc xắc có 6 kết quả: Xuất hiện mặt 1, 2, 3, 4, 5, hoặc 6 chấm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt khái niệm: Các kết quả có thể xảy ra của một trò chơi, thí nghiệm. | **1. Kết quả có thể:**<br>- Khi thực hiện một trò chơi hoặc thí nghiệm, ta không thể biết trước kết quả nào sẽ xảy ra, nhưng có thể liệt kê được tất cả các kết quả có thể xảy ra.<br>- Ví dụ:<br>  + Tung đồng xu: Có 2 kết quả có thể (mặt Sấp, mặt Ngửa).<br>  + Gieo xúc xắc: Có 6 kết quả có thể (mặt 1, 2, 3, 4, 5, 6 chấm). |

### Hoạt động 2.2: Sự kiện trong trò chơi, thí nghiệm (10 phút)
a) Mục tiêu: Hiểu một sự kiện xảy ra khi kết quả của phép thử thỏa mãn điều kiện của sự kiện.
b) Nội dung: Xét sự kiện "Mặt xuất hiện có số chấm là số chẵn" khi gieo xúc xắc.
c) Sản phẩm: Phân tích sự kiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu sự kiện $E$: "Gieo được mặt có số chấm là số chẵn". Nếu gieo được mặt 4 chấm thì sự kiện $E$ có xảy ra không? Nếu gieo được mặt 3 chấm thì sao?<br>- **HS:** Tiếp nhận tình huống.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mặt 4 chấm: Sự kiện $E$ xảy ra (vì 4 là số chẵn). Mặt 3 chấm: Sự kiện $E$ không xảy ra (vì 3 là số lẻ).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định: Một sự kiện xảy ra hay không xảy ra hoàn toàn phụ thuộc vào kết quả của phép thử. | **2. Sự kiện trong trò chơi, thí nghiệm:**<br>- Sự kiện xảy ra nếu kết quả thực nghiệm thỏa mãn điều kiện của sự kiện.<br>- Ví dụ: Sự kiện "Mặt xuất hiện có số chấm là số chẵn" xảy ra khi gieo được mặt 2, 4, hoặc 6 chấm. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Liệt kê các kết quả làm cho một sự kiện xảy ra trong trò chơi rút thẻ từ hộp kín.
b) Nội dung: Bài 9.18, 9.19 SGK trang 94.
c) Sản phẩm: Bài giải trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trong hộp có 5 chiếc thẻ đánh số từ 1 đến 5. Rút ngẫu nhiên 1 chiếc thẻ. Hãy liệt kê các kết quả làm cho sự kiện "Số trên thẻ là số nguyên tố" xảy ra.<br>- **HS:** Đọc đề và phân tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Các số nguyên tố từ 1 đến 5 là 2, 3, 5.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Các kết quả làm sự kiện xảy ra là: Rút được thẻ số 2, thẻ số 3, hoặc thẻ số 5.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Có 3 kết quả thuận lợi làm sự kiện xảy ra. | Các kết quả làm cho sự kiện xảy ra là rút được thẻ số 2, thẻ số 3, hoặc thẻ số 5. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Ứng dụng vòng quay may mắn trong các hội chợ xuân.
b) Nội dung: Xác định các kết quả có thể khi quay một vòng quay may mắn chia 8 ô thưởng.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh vòng quay may mắn có 8 ô phần thưởng khác nhau. Khi quay mạnh vòng quay, kim dừng lại ở ô nào là kết quả có thể không?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Có 8 kết quả có thể xảy ra tương ứng với 8 ô phần thưởng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò HS chuẩn bị cho Bài 43: Xác suất thực nghiệm. | Vòng quay may mắn có 8 ô tương ứng với 8 kết quả có thể xảy ra. |
"""
    },
    {
        "filename": "37_KHBD_Toan6_Bai43_XacSuatThucNghiem_Tiet91.md",
        "header": "TIẾT 91 - BÀI 43: XÁC SUẤT THỰC NGHIỆM\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 91 - BÀI 43: XÁC SUẤT THỰC NGHIỆM
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm xác suất thực nghiệm của một sự kiện trong trò chơi, thí nghiệm lặp lại nhiều lần.
- Nắm vững công thức tính xác suất thực nghiệm: Tỉ số giữa số lần sự kiện xảy ra và tổng số lần thực hiện thí nghiệm:
$$\\text{Xác suất thực nghiệm} = \\frac{\\text{Số lần sự kiện xảy ra}}{\\text{Tổng số lần thực hiện thí nghiệm}}$$
- Biết biểu diễn xác suất thực nghiệm dưới dạng phân số, số thập phân hoặc tỉ số phần trăm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thực hiện thí nghiệm lặp lại $20$ lần và ghi chép số liệu chính xác vào bảng kiểm đếm.
- Giao tiếp và hợp tác: Hợp tác nhóm gộp số liệu thực nghiệm của các thành viên để tính xác suất với số lần thử lớn hơn ($80$ - $100$ lần).

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Nhận xét quy luật số lớn: Khi số lần thực nghiệm càng lớn thì xác suất thực nghiệm càng tiến gần đến xác suất lý thuyết.
- Năng lực giải quyết vấn đề toán học: Ước lượng xác suất bắn trúng bia hoặc tỉ lệ hạt nảy mầm trong nông nghiệp.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng bảng tính Excel lập bảng đếm tần số xuất hiện của mặt ngửa và tự động tính tỉ số phần trăm xác suất thực nghiệm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh tìm hiểu ứng dụng xác suất thực nghiệm trong các thuật toán máy học (Machine Learning) để phân loại thư rác (Spam Filter).***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, không bịa đặt số liệu thực nghiệm.
- Kiên trì, tỉ mỉ khi thực hiện nhiều lần phép thử lặp đi lặp lại.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, đồng xu, xúc xắc, máy chiếu, bảng ghi số liệu tổng hợp.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, mỗi nhóm 1 đồng xu hoặc 1 con xúc xắc.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề từ thực tế một xạ thủ bắn 20 phát trúng đích 17 phát để định lượng khả năng bắn trúng.
b) Nội dung: Khả năng bắn trúng của xạ thủ được đo bằng tỉ số nào?
c) Sản phẩm: Câu trả lời của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Một cầu thủ bóng đá sút luân lưu 10 quả và ghi bàn 8 quả. Tỉ số giữa số lần ghi bàn và tổng số lần sút là bao nhiêu?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tỉ số là $\\frac{8}{10} = \\frac{4}{5} = 80\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Tỉ số đó trong toán học được gọi là xác suất thực nghiệm của sự kiện ghi bàn. | Xác suất thực nghiệm đo lường mức độ thường xuyên xảy ra của một sự kiện qua thực tế thử nghiệm. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Khái niệm và công thức xác suất thực nghiệm (12 phút)
a) Mục tiêu: Nắm vững định nghĩa và công thức tính xác suất thực nghiệm.
b) Nội dung: Công thức $P = \\frac{k}{n}$ với $k$ là số lần sự kiện xảy ra, $n$ là tổng số lần thực hiện.
c) Sản phẩm: Vở ghi bài và công thức của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Khi thực hiện một thí nghiệm lặp lại $n$ lần, nếu sự kiện $E$ xảy ra $k$ lần thì tỉ số $\\frac{k}{n}$ gọi là xác suất thực nghiệm của sự kiện $E$ sau $n$ lần thử. Viết công thức tổng quát.<br>- **HS:** Tiếp nhận công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi công thức vào vở: $\\text{Xác suất thực nghiệm} = \\frac{k}{n}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu ví dụ: Tung đồng xu 50 lần có 27 lần ngửa thì xác suất thực nghiệm xuất hiện mặt ngửa là $\\frac{27}{50} = 54\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Xác suất thực nghiệm luôn là một số từ $0$ đến $1$ (tức là từ $0\\%$ đến $100\\%$). | **1. Xác suất thực nghiệm:**<br>- Thực hiện lặp lại một thí nghiệm $n$ lần.<br>- Gọi $k$ là số lần sự kiện $A$ xảy ra.<br>- Xác suất thực nghiệm của sự kiện $A$ là tỉ số:<br>$$\\frac{k}{n} = \\frac{\\text{Số lần sự kiện } A \\text{ xảy ra}}{\\text{Tổng số lần thực hiện thí nghiệm}}$$<br>- Ta có: $0 \\le \\frac{k}{n} \\le 1$. |

### Hoạt động 2.2: Thực hành thực nghiệm tung đồng xu theo nhóm (8 phút)
a) Mục tiêu: Trải nghiệm thực hành tung đồng xu 20 lần và tính xác suất thực nghiệm mặt ngửa.
b) Nội dung: Nhóm 4 học sinh tung đồng xu 20 lần, kẻ bảng kiểm đếm và tính xác suất.
c) Sản phẩm: Bảng số liệu kiểm đếm của từng nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu mỗi nhóm 4 HS tung đồng xu 20 lần, ghi lại số lần xuất hiện mặt Ngửa ($N$) và mặt Sấp ($S$). Tính xác suất thực nghiệm mặt Ngửa.<br>- **HS:** Nhận đồng xu và bắt đầu tung.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành nghiêm túc, đếm số lần và tính tỉ số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các nhóm đọc to kết quả: Nhóm 1 được $\\frac{11}{20} = 55\\%$; Nhóm 2 được $\\frac{9}{20} = 45\\%$,...<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng hợp toàn bộ số lần tung của cả lớp ($20 \\times 10 = 200$ lần), thấy xác suất xấp xỉ $50\\%$. | Học sinh nắm vững cách thực hành, ghi chép và tính toán xác suất thực nghiệm từ số liệu thực tế. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính xác suất thực nghiệm từ bảng số liệu có sẵn trong bài tập SGK.
b) Nội dung: Bài 9.22, 9.23 SGK trang 97.
c) Sản phẩm: Lời giải bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gieo một con xúc xắc 100 lần, ghi được mặt 6 chấm xuất hiện 18 lần. Hãy tính xác suất thực nghiệm của sự kiện "Xuất hiện mặt 6 chấm".<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng công thức: $\\frac{18}{100} = \\frac{9}{50} = 0{,}18 = 18\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kết quả chuẩn xác. | Xác suất thực nghiệm của sự kiện xuất hiện mặt 6 chấm là:<br>$$\\frac{18}{100} = \\frac{9}{50} = 18\\%$$<br>Đáp số: $18\\%$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng xác suất thực nghiệm ước tính tỉ lệ nảy mầm của hạt giống cây trồng.
b) Nội dung: Gieo 200 hạt giống thì có 184 hạt nảy mầm thành cây non. Tính xác suất thực nghiệm nảy mầm của giống cây đó.
c) Sản phẩm: Lời giải bài toán thực tế.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế nông nghiệp về tỉ lệ nảy mầm của 200 hạt giống.<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tỉ lệ: $\\frac{184}{200} = \\frac{92}{100} = 92\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác suất thực nghiệm nảy mầm là $92\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định tầm quan trọng của xác suất thực nghiệm trong chọn giống và sản xuất nông nghiệp. | Xác suất thực nghiệm nảy mầm của hạt giống là:<br>$$\\frac{184}{200} = 92\\%$$<br>Đáp số: $92\\%$. |
"""
    },
    {
        "filename": "38_KHBD_Toan6_LuyenTapChung_Tiet92.md",
        "header": "TIẾT 92 - LUYỆN TẬP CHUNG: XÁC SUẤT THỰC NGHIỆM (TRANG 97)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 92 - LUYỆN TẬP CHUNG: XÁC SUẤT THỰC NGHIỆM (TRANG 97)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và rèn luyện kỹ năng xác định kết quả có thể, sự kiện và tính xác suất thực nghiệm của một sự kiện trong các trò chơi, thí nghiệm.
- Vận dụng xác suất thực nghiệm để dự đoán số lần xuất hiện của một sự kiện trong tương lai khi số lần thử tăng lên.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức xác suất thực nghiệm qua sơ đồ tư duy; chủ động làm các bài tập phân tích tình huống ngẫu nhiên.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận chiến lược chơi trò chơi công bằng dựa trên xác suất.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh xác suất thực nghiệm của các sự kiện khác nhau để đánh giá sự kiện nào có khả năng xảy ra cao hơn.
- Năng lực giải quyết vấn đề toán học: Ước tính số sản phẩm lỗi trong một lô hàng công nghiệp dựa trên mẫu kiểm tra xác suất thực nghiệm.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay để tính nhanh tỉ số phần trăm xác suất thực nghiệm và giải các bài toán ước lượng tỉ lệ.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI mô phỏng bài toán xác suất thực nghiệm với 10000 lần tung đồng xu để quan sát tính ổn định của tần số ngẫu nhiên.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật trong tính toán số liệu.
- Ý thức phòng tránh các trò chơi cá cược, cờ bạc may rủi có hại cho bản thân và xã hội.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Xác suất Tiết 92 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tái hiện nhanh công thức tính xác suất thực nghiệm qua trò chơi trắc nghiệm vui.
b) Nội dung: Trả lời câu hỏi: Tung đồng xu 40 lần thấy có 22 lần ngửa thì xác suất thực nghiệm mặt sấp là bao nhiêu?
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi tính xác suất thực nghiệm mặt sấp khi biết có 22 lần ngửa trong 40 lần tung.<br>- **HS:** Nhận đề và tính nhẩm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Số lần sấp: $40 - 22 = 18$ lần. Xác suất: $\\frac{18}{40} = \\frac{9}{20} = 45\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con: $45\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn dắt vào bài luyện tập chung. | Số lần sấp là $18$ lần. Xác suất thực nghiệm xuất hiện mặt sấp là $\\frac{18}{40} = 45\\%$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức xác suất thực nghiệm qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 92; đối chiếu các khái niệm cốt lõi.

![Sơ đồ tư duy Luyện tập chung Xác suất Tiết 92](khbd-ill:mindmap-toan6-tiet92)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 92. Yêu cầu HS phân tích các nhánh: 1. Trò chơi & Thí nghiệm; 2. Kết quả có thể; 3. Sự kiện; 4. Công thức xác suất thực nghiệm; 5. Dự đoán số lần xảy ra.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoạt động nhóm đôi tóm tắt công thức và các bước tính.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ kiến thức chuẩn mực. | **Hệ thống kiến thức xác suất:**<br>1. Phép thử: Các hoạt động ngẫu nhiên.<br>2. Kết quả có thể: Tập hợp tất cả các trường hợp có thể xuất hiện.<br>3. Sự kiện: Kết quả thỏa mãn điều kiện chỉ định.<br>4. Công thức xác suất: $P = \\frac{k}{n}$.<br>5. Dự đoán tương lai: Số lần xảy ra dự đoán $= N \\cdot P$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tính xác suất thực nghiệm và vận dụng dự đoán số lần xuất hiện trong thực tế.
b) Nội dung: Bài 9.25, 9.26 SGK trang 98.
c) Sản phẩm: Lời giải trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Kiểm tra chất lượng ngẫu nhiên 500 bóng đèn xuất xưởng thấy có 8 bóng đèn bị lỗi hỏng.<br>  a) Tính xác suất thực nghiệm chọn phải bóng đèn bị lỗi hỏng.<br>  b) Nếu nhà máy sản xuất $50\\,000$ bóng đèn thì ước lượng có khoảng bao nhiêu bóng đèn bị lỗi?<br>- **HS:** Đọc đề và làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: a) $\\frac{8}{500} = 0{,}016 = 1{,}6\\%$. b) Số bóng lỗi ước lượng: $50\\,000 \\cdot 0{,}016 = 800$ bóng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá bài giải chuẩn xác và ý nghĩa thực tế to lớn của xác suất trong kiểm soát chất lượng sản phẩm (KCS). | **Lời giải chi tiết:**<br>a) Xác suất thực nghiệm chọn phải bóng đèn bị lỗi là:<br>$$\\frac{8}{500} = \\frac{2}{125} = 1{,}6\\%$$<br>b) Ước lượng số bóng đèn bị lỗi trong lô $50\\,000$ bóng là:<br>$$50\\,000 \\cdot \\frac{8}{500} = 800\\text{ (bóng)}$$<br>Đáp số: a) $1{,}6\\%$; b) $800$ bóng đèn. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhận thức sự nguy hiểm của cờ bạc và các trò chơi may rủi dựa trên hiểu biết toán học về xác suất.
b) Nội dung: Giáo dục học sinh về việc tỉ lệ thắng trong các trò chơi may rủi luôn có lợi thế nghiêng về nhà cái.
c) Sản phẩm: Bài học nhận thức của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vì sao toán học chứng minh rằng việc tham gia cờ bạc, cá cược luôn dẫn đến thua lỗ về lâu dài?<br>- **HS:** Lắng nghe và suy ngẫm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vì xác suất thắng luôn được thiết kế nhỏ hơn xác suất thua, càng chơi nhiều lần thì tổng tiền mất càng lớn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên truyền lối sống lành mạnh, bài trừ cờ bạc và trò chơi may rủi. | Hiểu biết về xác suất giúp hình thành tư duy tỉnh táo, tránh xa các cạm bẫy cờ bạc và trò chơi cá cược. |
"""
    },
    {
        "filename": "39_KHBD_Toan6_OnTapCuoiHK2_SoHocThongKe_Tiet93-97.md",
        "header": "TIẾT 93 ĐẾN 97 - ÔN TẬP ĐÁNH GIÁ CUỐI HỌC KÌ II (SỐ HỌC VÀ THỐNG KÊ)\n*Thời lượng thực hiện: 05 tiết (225 phút)*",
        "md": """TIẾT 93 ĐẾN 97 - ÔN TẬP ĐÁNH GIÁ CUỐI HỌC KÌ II (SỐ HỌC VÀ THỐNG KÊ)
*Thời lượng thực hiện: 05 tiết (225 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Số học và Thống kê xác suất trong cả Học kì II:
  + Chương VI: Phân số (Khái niệm, so sánh, 4 phép tính, hỗn số, hai bài toán về phân số).
  + Chương VII: Số thập phân (Khái niệm, 4 phép tính, làm tròn, tỉ số và tỉ số phần trăm).
  + Chương IX: Dữ liệu và Xác suất (Thu thập, bảng thống kê, biểu đồ tranh, biểu đồ cột, biểu đồ cột kép, kết quả có thể, xác suất thực nghiệm).
- Vận dụng kiến thức tổng hợp giải quyết các bài toán liên môn và thực tế đời sống.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự lập bảng kế hoạch ôn tập chi tiết 5 tiết; tự giác giải các đề ôn tập tổng hợp và tự chấm điểm chéo.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải toán, tranh biện tìm ra cách giải ngắn gọn nhất trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa các công thức toán học; phân tích logic nhiều tầng để giải các bài toán thực tế phức tạp.
- Năng lực mô hình hoá toán học: Chuyển đổi các bài toán tài chính, môi trường, kinh tế gia đình thành các mô hình số học và thống kê chuẩn xác.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay thành thạo mọi chức năng tính toán (phân số, số thập phân, phần trăm, số mũ) để kiểm tra kết quả bài làm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh sử dụng AI để tạo đề thi thử trắc nghiệm trực tuyến cuối học kì II và nhận phản hồi giải thích chi tiết cho từng câu sai.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, kỷ luật, trung thực và tác phong làm bài thi nghiêm túc.
- Tự tin, sẵn sàng tâm thế bước vào kỳ thi đánh giá cuối năm học với kết quả cao nhất.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Ôn tập cuối HK2 Tiết 93-97 (vector 300 DPI), bộ đề ôn tập tổng hợp.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay, đề cương ôn tập cuối HKII.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (10 phút)
a) Mục tiêu: Tạo tâm thế hào hứng và quán triệt kế hoạch ôn tập tổng thể 5 tiết cuối năm.
b) Nội dung: Phổ biến ma trận đề thi cuối kì II môn Toán và mục tiêu ôn tập 5 chuyên đề trọng tâm.
c) Sản phẩm: Bản kế hoạch ôn tập của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu cấu trúc đề kiểm tra cuối kì II (Số học 40%, Thống kê - Xác suất 30%, Hình học 30%). Kế hoạch ôn tập 5 tiết chia thành 4 chuyên đề lớn.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định mục tiêu điểm số cá nhân và lên kế hoạch ôn tập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự học tập phát biểu quyết tâm của cả lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Động viên tinh thần học tập của cả lớp. | Kế hoạch ôn tập 5 tiết rõ ràng, bám sát ma trận và cấu trúc đề thi chuẩn Bộ GD&ĐT. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (45 phút)
### Hoạt động 2.1: Hệ thống hoá toàn diện kiến thức HKII qua Sơ đồ tư duy (45 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ cấu trúc kiến thức Số học và Thống kê qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 93-97; phân tích sự gắn kết liên hoàn giữa các mảng kiến thức.

![Sơ đồ tư duy Ôn tập cuối HK2 Tiết 93-97](khbd-ill:mindmap-toan6-tiet93-97)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở ghi học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy tổng hợp HKII. Hướng dẫn ôn theo 3 trục kiến thức lớn:<br>  1. Phân số: Quy tắc dấu, 4 phép tính, hai bài toán phân số.<br>  2. Số thập phân: Cấu tạo số âm, 4 phép tính, làm tròn và ước lượng, tỉ số phần trăm.<br>  3. Thống kê & Xác suất: Thu thập, bảng biểu đồ, kết quả có thể và xác suất thực nghiệm.<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành sơ đồ tư duy vào vở ôn tập theo các nhóm chuyên đề.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 3 nhóm lần lượt thuyết trình 3 trục kiến thức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa toàn bộ hệ thống lý thuyết, khắc sâu các quy tắc tính toán cốt lõi. | **Tổng kết lý thuyết Số học và Thống kê HKII:**<br>- Phân số: Cộng trừ đưa về mẫu dương; Nhân tử nhân mẫu; Chia nhân nghịch đảo; Hai bài toán phân số.<br>- Số thập phân: Quy tắc dấu như số nguyên; Làm tròn số; Tỉ số phần trăm ($a \\cdot \\frac{m}{100}$ và $b : \\frac{m}{100}$).<br>- Thống kê & Xác suất: Biểu đồ cột kép; $P = \\frac{k}{n}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (150 phút)
a) Mục tiêu: Luyện tập toàn diện 4 dạng bài tập cốt lõi của đề thi: Tính giá trị biểu thức hợp lí, Tìm $x$, Đọc biểu đồ thống kê và Bài toán thực tế.
b) Nội dung: Giải các đề ôn tập số 1, số 2 và số 3 trong tập tài liệu đề cương.
c) Sản phẩm: Bài làm chi tiết của học sinh trên bảng và trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 4 bài tập điển hình qua các tiết ôn tập:<br>  Bài 1 (Tính hợp lí): $A = \\left(\\frac{-3}{7}\\right) \\cdot \\frac{4}{11} + \\left(\\frac{-3}{7}\\right) \\cdot \\frac{7}{11} + 1\\frac{3}{7}$.<br>  Bài 2 (Tìm $x$): $\\frac{3}{4} + \\frac{1}{4} : x = \\frac{2}{5}$.<br>  Bài 3 (Thống kê): Cho biểu đồ cột kép so sánh sản lượng lúa và ngô của một hợp tác xã trong 3 năm. Đọc số liệu và tính tổng sản lượng.<br>  Bài 4 (Toán thực tế): Một cửa hàng thời trang nhập về $200$ chiếc áo với giá gốc $150\\,000$ đồng$/$chiếc. Cửa hàng bán $120$ chiếc đầu tiên với giá lãi $30\\%$ so với giá gốc. Số áo còn lại bán giảm giá $20\\%$ so với giá đã bán trước đó. Hỏi sau khi bán hết $200$ chiếc áo, cửa hàng lãi bao nhiêu tiền?<br>- **HS:** Nhận đề và phân tích từng bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài nghiêm túc vào vở cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Lần lượt các HS lên bảng chữa chi tiết từng bài.<br>- Bài 1: $A = \\left(\\frac{-3}{7}\\right) \\cdot \\left(\\frac{4}{11} + \\frac{7}{11}\\right) + \\frac{10}{7} = \\frac{-3}{7} \\cdot 1 + \\frac{10}{7} = \\frac{7}{7} = 1$.<br>- Bài 2: $\\frac{1}{4} : x = \\frac{2}{5} - \\frac{3}{4} = \\frac{8-15}{20} = \\frac{-7}{20} \\Rightarrow x = \\frac{1}{4} : \\left(\\frac{-7}{20}\\right) = \\frac{1}{4} \\cdot \\frac{-20}{7} = \\frac{-5}{7}$.<br>- Bài 4: Giá bán 120 chiếc đầu: $150\\,000 \\cdot 1{,}3 = 195\\,000$ đồng. Tiền thu được từ 120 chiếc: $120 \\cdot 195\\,000 = 23\\,400\\,000$ đồng. Giá bán 80 chiếc sau: $195\\,000 \\cdot (1 - 0{,}2) = 156\\,000$ đồng. Tiền thu từ 80 chiếc: $80 \\cdot 156\\,000 = 12\\,480\\,000$ đồng. Tổng tiền thu được: $23\\,400\\,000 + 12\\,480\\,000 = 35\\,880\\,000$ đồng. Tiền vốn gốc: $200 \\cdot 150\\,000 = 30\\,000\\,000$ đồng. Tiền lãi: $35\\,880\\,000 - 30\\,000\\,000 = 5\\,880\\,000$ đồng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa: Nhắc nhở kết luận $x = \\frac{-5}{7}$, không kết luận tập nghiệm. Chuẩn hóa cách giải bài toán kinh tế nhiều bước rõ ràng, mạch lạc. | **Đáp số bài tập ôn tập tổng hợp:**<br>**Bài 1:**<br>$$A = 1$$<br>**Bài 2:**<br>$$\\frac{1}{4} : x = \\frac{-7}{20} \\Rightarrow x = \\frac{-5}{7}$$<br>Vậy $x = \\frac{-5}{7}$.<br>**Bài 4:**<br>- Tổng tiền thu được từ bán áo: $35\\,880\\,000$ đồng.<br>- Tổng tiền vốn nhập hàng: $30\\,000\\,000$ đồng.<br>- Tiền lãi cửa hàng thu được là:<br>$$35\\,880\\,000 - 30\\,000\\,000 = 5\\,880\\,000\\text{ (đồng)}$$<br>Đáp số: $5\\,880\\,000$ đồng. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (20 phút)
a) Mục tiêu: Quán triệt quy chế thi và kỹ năng phân bổ thời gian 90 phút làm bài thi học kì II.
b) Nội dung: Chiến thuật làm bài: Trắc nghiệm làm trong 20 phút, Tự luận 60 phút, soát lại bài 10 phút.
c) Sản phẩm: Bản ghi nhớ chiến thuật làm bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chiến thuật làm bài thi: Đọc kĩ đề, làm câu dễ trước, cẩn thận dấu âm, rút gọn phân số tối giản và kiểm tra lại bằng máy tính cầm tay.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự rà soát lại các dụng cụ học tập cần mang vào phòng thi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đặt các câu hỏi còn băn khoăn về nội dung ôn tập.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giải đáp thắc mắc, chúc cả lớp bình tĩnh, tự tin và đạt thành tích xuất sắc nhất trong kỳ thi cuối năm học. | 100% học sinh sẵn sàng với tâm thế tự tin nhất bước vào bài kiểm tra đánh giá cuối HKII. |
"""
    },
    {
        "filename": "40_KHBD_Toan6_KiemTraCuoiHK2_SoHocThongKe_Tiet98.md",
        "header": "TIẾT 98 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (SỐ HỌC VÀ THỐNG KÊ)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 98 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (SỐ HỌC VÀ THỐNG KÊ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện chuẩn kiến thức, kỹ năng của học sinh về toàn bộ chương trình Số học và Thống kê - Xác suất trong Học kì II (Chương VI, Chương VII, Chương IX).
- Đánh giá năng lực giải quyết vấn đề toán học thực tiễn, tính toán và suy luận logic.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Độc lập làm bài, trung thực, nghiêm túc tuân thủ quy chế kiểm tra cuối kì.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày bài giải mạch lạc, chặt chẽ, đầy đủ căn cứ toán học.
- Năng lực giải quyết vấn đề toán học: Mô hình hóa và giải quyết trọn vẹn các bài toán thực tế.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay đúng quy định trong phòng thi để kiểm tra các phép biến đổi số học phức tạp.***

## 3. Về phẩm chất
- Trung thực, khách quan, tự trọng và có trách nhiệm cao với kết quả học tập của mình.
- Tác phong làm bài nghiêm túc, khoa học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận và bản đặc tả chuẩn Bộ GD&ĐT (Trắc nghiệm 30% - Tự luận 70%), đáp án và thang điểm chi tiết.
2. Học sinh: Giấy thi, bút mực, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (3 phút)
a) Mục tiêu: Ổn định phòng thi, tạo tâm lý tự tin và phát đề kiểm tra.
b) Nội dung: Nhắc nhở quy chế thi và phát đề.
c) Sản phẩm: Đề thi trên bàn của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định trật tự phòng thi, phổ biến quy chế. Phát đề thi cho học sinh.<br>- **HS:** Nhận đề, kiểm tra số trang và độ rõ của đề.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Điền đầy đủ thông tin cá nhân vào giấy thi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo ngay nếu có đề bị lỗi mờ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Phát lệnh bắt đầu tính giờ làm bài. | 100% học sinh sẵn sàng bước vào bài làm. |

## B. THỰC HIỆN BÀI KIỂM TRA (HOẠT ĐỘNG 2) (40 phút)
a) Mục tiêu: Học sinh độc lập làm bài thi trắc nghiệm và tự luận.
b) Nội dung: Học sinh giải các câu hỏi trong đề kiểm tra.
c) Sản phẩm: Bài làm hoàn thiện trên giấy thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giám sát phòng thi nghiêm túc, bao quát đảm bảo tính công bằng, khách quan.<br>- **HS:** Độc lập làm bài, không trao đổi, không quay cóp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm phần Trắc nghiệm trước, sau đó làm phần Tự luận trình bày chi tiết.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Báo mốc thời gian còn lại 15 phút và 5 phút.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **HS:** Soát lại toàn bộ bài làm, đặc biệt là các bước biến đổi dấu âm và kết luận nghiệm. | Học sinh làm bài độc lập, nghiêm túc, đạt chất lượng cao. |

## C. THU BÀI VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (2 phút)
a) Mục tiêu: Thu bài đầy đủ theo danh sách lớp và nhận xét ý thức kiểm tra.
b) Nội dung: Thu bài thi theo dãy bàn.
c) Sản phẩm: Toàn bộ bài thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hết giờ làm bài, yêu cầu học sinh dừng bút, nộp bài theo dãy.<br>- **HS:** Dừng bút và chuyển bài lên đầu bàn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm đủ số bài thi theo sĩ số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp xác nhận sĩ số tham gia kiểm tra.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét thái độ làm bài của học sinh; dặn dò chuẩn bị cho Bài tập cuối chương IX ở tiết sau. | Thu đủ 100% bài kiểm tra theo sĩ số lớp. |
"""
    },
    {
        "filename": "41_KHBD_Toan6_BaiTapCuoiChuong9_Tiet99.md",
        "header": "TIẾT 99 - BÀI TẬP CUỐI CHƯƠNG IX (TRANG 99)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 99 - BÀI TẬP CUỐI CHƯƠNG IX (TRANG 99)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết toàn bộ kiến thức Chương IX: Thu thập, phân loại, biểu diễn dữ liệu bằng bảng thống kê, biểu đồ tranh, biểu đồ cột, biểu đồ cột kép; kết quả có thể, sự kiện và xác suất thực nghiệm.
- Vận dụng kiến thức toàn chương để giải quyết các bài tập tổng hợp và dự án điều tra nhỏ.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng kết toàn bộ kiến thức chương IX qua sơ đồ tư duy; chủ động rà soát và đánh giá các kỹ năng thống kê của bản thân.
- Giao tiếp và hợp tác: Tự tin thuyết trình báo cáo kết quả điều tra số liệu trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa các phương pháp biểu diễn số liệu trực quan; giải thích sự biến động của dữ liệu.
- Năng lực giải quyết vấn đề toán học: Xử lý các bài toán thống kê thực tế nhiều bước tính toán.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay hoặc phần mềm bảng tính để vẽ đồ thị và tính toán các chỉ số thống kê cơ bản.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI tổng hợp các bài viết phân tích dữ liệu lớn (Big Data) để học sinh nhận thức được tương lai của ngành khoa học dữ liệu.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật và tác phong khoa học.
- Ý thức quan tâm đến các vấn đề xã hội thông qua các số liệu thống kê.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 99 (vector 300 DPI), tivi/máy chiếu, phiếu học tập.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay, thước kẻ, bút màu.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập nhanh các dạng biểu đồ qua trò chơi trắc nghiệm chọn biểu đồ phù hợp.
b) Nội dung: Tình huống so sánh dân số giữa 2 thành phố qua 5 năm thì chọn loại biểu đồ nào tối ưu nhất?
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Để so sánh dân số giữa 2 thành phố lớn qua 5 năm, biểu đồ nào là lựa chọn tối ưu nhất?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết nhanh câu trả lời lên bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con: Biểu đồ cột kép.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn vào bài ôn tập cuối chương IX. | Biểu đồ cột kép là lựa chọn tối ưu nhất để so sánh hai nhóm dữ liệu qua nhiều thời điểm. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức Chương IX bằng Sơ đồ tư duy tổng hợp 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 99; hoàn thiện bức tranh tổng thể về Thống kê và Xác suất.

![Sơ đồ tư duy Bài tập cuối chương IX Tiết 99](khbd-ill:mindmap-toan6-tiet99)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy tổng thể Chương IX. Hướng dẫn HS hệ thống theo 2 mảng lớn: 1. Thống kê (Dữ liệu, Bảng thống kê, Biểu đồ tranh, Biểu đồ cột, Biểu đồ cột kép); 2. Xác suất (Kết quả có thể, Sự kiện, Xác suất thực nghiệm).<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành các chỗ trống trong phiếu tóm tắt.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS lên bảng điền các công thức trọng tâm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại toàn bộ hệ thống lý thuyết chương IX chuẩn mực. | **Tổng kết lý thuyết Chương IX:**<br>- Thống kê: Thu thập, phân loại, tính hợp lí; Biểu diễn qua bảng và 3 loại biểu đồ.<br>- Xác suất: Phép thử ngẫu nhiên, sự kiện; Xác suất thực nghiệm $P = \\frac{k}{n}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Luyện tập toàn diện các bài tập trắc nghiệm và tự luận cuối chương trong SGK.
b) Nội dung: Giải Bài 9.27, 9.28, 9.29 SGK trang 99, 100.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài tập:<br>  Bài 1: Đọc biểu đồ cột kép lượng mưa tại Huế và Đà Nẵng trong 6 tháng cuối năm. Cho biết tháng nào có lượng mưa cao nhất ở cả 2 thành phố?<br>  Bài 2: Gieo một con xúc xắc 60 lần, mặt 1 chấm xuất hiện 9 lần, mặt 2 chấm xuất hiện 12 lần. Tính xác suất thực nghiệm của sự kiện "Xuất hiện mặt có số chấm nhỏ hơn 3".<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bài 2: Số lần xuất hiện mặt nhỏ hơn 3 (mặt 1 hoặc 2 chấm) là $9 + 12 = 21$ lần. Xác suất: $\\frac{21}{60} = \\frac{7}{20} = 35\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá bài giải chuẩn xác, logic. | **Lời giải:**<br>Số lần xuất hiện mặt có số chấm nhỏ hơn 3 là:<br>$$9 + 12 = 21\\text{ (lần)}$$<br>Xác suất thực nghiệm của sự kiện đó là:<br>$$\\frac{21}{60} = \\frac{7}{20} = 35\\%$$<br>Đáp số: $35\\%$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Chuẩn bị cho 2 tiết Hoạt động thực hành trải nghiệm cuối năm (Tiết 100 và Tiết 101).
b) Nội dung: Giáo viên phân công nhiệm vụ cho các nhóm chuẩn bị dự án chi tiêu và khảo sát thể thao.
c) Sản phẩm: Phân công nhiệm vụ nhóm của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến chủ đề 2 tiết trải nghiệm: Tiết 100: Kế hoạch chi tiêu cá nhân và gia đình; Tiết 101: Khảo sát môn thể thao yêu thích trong hè.<br>- **HS:** Ghi chép phân công nhóm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Các nhóm họp nhanh bầu nhóm trưởng và phân chia chuẩn bị số liệu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp nộp danh sách phân công nhóm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở các nhóm chuẩn bị chu đáo để có tiết trải nghiệm thú vị. | Phân công nhóm chuẩn bị số liệu và đồ dùng cho 2 tiết thực hành trải nghiệm cuối năm. |
"""
    },
    {
        "filename": "42_KHBD_Toan6_HDTN_KeHoachChiTieu_Tiet100.md",
        "header": "TIẾT 100 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: KẾ HOẠCH CHI TIÊU CÁ NHÂN VÀ GIA ĐÌNH\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 100 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: KẾ HOẠCH CHI TIÊU CÁ NHÂN VÀ GIA ĐÌNH
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng các kiến thức về số thập phân, phân số và tỉ số phần trăm vào việc lập kế hoạch chi tiêu tài chính cá nhân và gia đình một cách hợp lí.
- Nhận biết các khoản chi tiêu thiết yếu (nhu cầu thiết yếu) và các khoản chi tiêu mong muốn (sở thích giải trí); áp dụng quy tắc tài chính phổ biến (như quy tắc $50/30/20$).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự xây dựng kế hoạch quản lý tiền tiêu vặt hoặc tiền thưởng của bản thân trong một tháng.
- Giao tiếp và hợp tác: Làm việc nhóm thảo luận, phản biện kế hoạch ngân sách gia đình của các thành viên.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh tỉ lệ phần trăm của các khoản chi tiêu để đánh giá mức độ cân đối tài chính.
- Năng lực mô hình hoá toán học: Thiết lập bảng ngân sách tài chính bằng các phép tính phân số và phần trăm.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng bảng tính Google Sheets để thiết kế bảng quản lý tài chính cá nhân tự động tính tổng chi tiêu và phần trăm số dư tiết kiệm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh tương tác với chatbot AI đóng vai chuyên gia tài chính để nhận lời khuyên về cách tối ưu hóa chi tiêu sinh hoạt.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, tiết kiệm, có trách nhiệm trong việc sử dụng đồng tiền do cha mẹ lao động vất vả tạo ra.
- Hình thành thói quen quản lý tài chính thông minh ngay từ khi còn ngồi trên ghế nhà trường.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, máy chiếu, các mẫu bảng ngân sách tài chính gia đình.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, máy tính cầm tay, phiếu lập kế hoạch chi tiêu in sẵn.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề về sự cần thiết của việc lập kế hoạch chi tiêu tài chính trong gia đình.
b) Nội dung: Trả lời câu hỏi: Nếu chi tiêu không có kế hoạch thì điều gì sẽ xảy ra vào cuối tháng?
c) Sản phẩm: Ý kiến chia sẻ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt tình huống: Nếu một gia đình kiếm được $15$ triệu đồng mỗi tháng nhưng không ghi chép chi tiêu thì điều gì thường xảy ra vào cuối tháng?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận: Hết sạch tiền, thậm chí bị thiếu hụt, không có khoản tiền dự phòng lúc ốm đau.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài thực hành: Lập kế hoạch chi tiêu giúp chúng ta chủ động về tài chính và tích lũy cho tương lai. | Quản lý tài chính và lập kế hoạch chi tiêu là kỹ năng sống thiết yếu của con người hiện đại. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Tìm hiểu quy tắc phân bổ ngân sách 50/30/20 (15 phút)
a) Mục tiêu: Hiểu quy tắc phân bổ tài chính: $50\\%$ nhu cầu thiết yếu, $30\\%$ mong muốn cá nhân, $20\\%$ tiết kiệm tích lũy.
b) Nội dung: Phân tích 3 nhóm chi tiêu chính trong cuộc sống.
c) Sản phẩm: Bảng phân loại các khoản chi tiêu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu quy tắc phân bổ tài chính $50/30/20$ nổi tiếng:<br>  + $50\\%$ thu nhập: Dành cho các nhu cầu thiết yếu (ăn uống, tiền nhà, học phí, điện nước).<br>  + $30\\%$ thu nhập: Dành cho mong muốn cá nhân (mua sắm đồ yêu thích, giải trí, du lịch).<br>  + $20\\%$ thu nhập: Dành cho tiết kiệm tích lũy hoặc dự phòng khẩn cấp.<br>- **HS:** Ghi chép quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân loại các khoản chi sau vào 3 nhóm: Mua gạo, Đi xem phim, Tiền điện, Mua đồ chơi điện tử, Gửi sổ tiết kiệm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phân loại đúng từng khoản mục.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Cần luôn ưu tiên khoản thiết yếu và giữ nghiêm ngặt tỉ lệ tiết kiệm $20\\%$. | **Quy tắc phân bổ tài chính $50/30/20$:**<br>- $50\\%$: Nhu cầu thiết yếu (ăn, ở, học tập).<br>- $30\\%$: Chi tiêu cá nhân, giải trí.<br>- $20\\%$: Tiết kiệm và dự phòng tương lai. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Thực hành lập kế hoạch chi tiêu cho một gia đình có thu nhập $20\\,000\\,000$ đồng$/$tháng.
b) Nội dung: Tính toán số tiền phân bổ cho 3 nhóm theo quy tắc $50/30/20$ và chi tiết hóa từng khoản.
c) Sản phẩm: Bảng ngân sách gia đình hoàn thiện của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao đề bài: Gia đình bạn An có tổng thu nhập $20\\,000\\,000$ đồng$/$tháng. Hãy áp dụng quy tắc $50/30/20$ để tính số tiền dành cho mỗi nhóm và lập bảng dự toán chi tiết.<br>- **HS:** Làm việc theo nhóm 4.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: Thiết yếu: $20\\,000\\,000 \\cdot 50\\% = 10\\,000\\,000$ đồng. Mong muốn: $20\\,000\\,000 \\cdot 30\\% = 6\\,000\\,000$ đồng. Tiết kiệm: $20\\,000\\,000 \\cdot 20\\% = 4\\,000\\,000$ đồng. Sau đó phân bổ chi tiết các mục con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm lên bảng dán bảng ngân sách của nhóm mình và thuyết trình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao tính thực tiễn và sự hợp lí của các phương án tài chính. | **Bảng phân bổ ngân sách $20\\,000\\,000$ đồng:**<br>- Nhu cầu thiết yếu ($50\\%$): $10\\,000\\,000$ đồng.<br>- Chi tiêu cá nhân ($30\\%$): $6\\,000\\,000$ đồng.<br>- Tiết kiệm tích lũy ($20\\%$): $4\\,000\\,000$ đồng. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Lập kế hoạch quản lý chi tiêu cá nhân trong dịp hè sắp tới.
b) Nội dung: Học sinh tự lập bảng chi tiêu cho số tiền tiết kiệm của bản thân trong 3 tháng hè.
c) Sản phẩm: Bảng kế hoạch hè trong sổ tay cá nhân.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ: Em hãy lên kế hoạch chi tiêu số tiền tiêu vặt hoặc tiền thưởng hè của mình để vừa có thể mua sách truyện, vừa có thể đi bơi và vẫn giữ được tiền tiết kiệm.<br>- **HS:** Tiếp nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi chép ý tưởng vào sổ tay.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chia sẻ nhanh với bạn cùng bàn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò chuẩn bị cho tiết thực hành trải nghiệm cuối cùng của năm học: Tiết 101. | Tự giác hình thành thói quen chi tiêu thông minh và tiết kiệm trong dịp hè. |
"""
    },
    {
        "filename": "43_KHBD_Toan6_HDTN_MonTheThaoYeuThich_Tiet101.md",
        "header": "TIẾT 101 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: HOẠT ĐỘNG THỂ THAO NÀO ĐƯỢC YÊU THÍCH NHẤT TRONG HÈ (TIẾT KẾT THÚC NĂM HỌC)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 101 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: HOẠT ĐỘNG THỂ THAO NÀO ĐƯỢC YÊU THÍCH NHẤT TRONG HÈ (TIẾT KẾT THÚC NĂM HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng toàn diện quy trình nghiên cứu thống kê: Xác định mục tiêu điều tra, thiết kế phiếu hỏi, thu thập số liệu, tổ chức vào bảng thống kê và biểu diễn bằng biểu đồ cột kép.
- Phân tích số liệu để xác định môn thể thao được học sinh nam và nữ yêu thích nhất trong dịp hè; đưa ra các kiến nghị thành lập các câu lạc bộ thể thao hè phù hợp.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tin điều tra, phỏng vấn các bạn trong lớp và ghi chép số liệu khoa học.
- Giao tiếp và hợp tác: Làm việc nhóm phân công nhiệm vụ nhịp nhàng (phỏng vấn, kiểm đếm, vẽ biểu đồ, thuyết trình).

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh sở thích thể thao giữa nam và nữ dựa vào độ cao của các cột kép.
- Năng lực giải quyết vấn đề toán học: Đưa ra đề xuất tổ chức hoạt động hè dựa trên kết quả phân tích số liệu thực chứng.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm trình chiếu PowerPoint hoặc Canva để thiết kế poster báo cáo kết quả khảo sát thể thao kèm biểu đồ trực quan.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Sử dụng AI để tổng hợp các bài tập thể thao rèn luyện sức khỏe phù hợp với từng lứa tuổi học sinh THCS trong kỳ nghỉ hè.***

## 3. Về phẩm chất
- Nâng cao ý thức rèn luyện thân thể, nâng cao sức khỏe thông qua các hoạt động thể dục thể thao bổ ích.
- Tinh thần đoàn kết, gắn bó bạn bè trong buổi học toán cuối cùng của năm học lớp 6.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, máy chiếu, giấy A0, bút dạ màu cho các nhóm.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước kẻ, bút màu, số liệu khảo sát đã chuẩn bị trước.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tạo không khí vui tươi, phấn khởi chào đón kỳ nghỉ hè thông qua bài hát hoặc clip thể thao sôi động.
b) Nội dung: Xem đoạn clip ngắn về các hoạt động thể thao hè: Bơi lội, Bóng đá, Cầu lông, Bóng rổ, Điền kinh.
c) Sản phẩm: Sự hào hứng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu clip thể thao học đường sôi động. Hỏi: Mùa hè này các em dự định tham gia môn thể thao nào để rèn luyện sức khỏe?<br>- **HS:** Hào hứng theo dõi clip.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các bạn sôi nổi nêu tên các môn thể thao yêu thích.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào tiết học thực hành trải nghiệm cuối cùng: Khảo sát và phân tích môn thể thao hè của lớp 6. | Thể thao giúp tăng cường sức khỏe, tinh thần sảng khoái và phát triển thể chất toàn diện. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Tổng hợp và xử lý dữ liệu khảo sát (15 phút)
a) Mục tiêu: Tổng hợp số liệu phiếu khảo sát của cả lớp vào bảng thống kê phân loại theo Nam và Nữ.
b) Nội dung: Kẻ bảng thống kê 5 môn thể thao (Bóng đá, Bơi lội, Cầu lông, Bóng rổ, Cờ vua) phân theo giới tính.
c) Sản phẩm: Bảng thống kê hoàn thiện trên bảng lớn của lớp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thu thập nhanh phiếu khảo sát của 4 tổ. Yêu cầu 2 bạn thư ký lên bảng kiểm đếm và ghi số liệu vào bảng thống kê 2 dòng Nam và Nữ.<br>- **HS:** Thư ký thực hiện kiểm đếm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cả lớp cùng theo dõi và đối chiếu số liệu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Thư ký công bố số liệu: Bóng đá (Nam: 14, Nữ: 2); Bơi lội (Nam: 12, Nữ: 15); Cầu lông (Nam: 6, Nữ: 10); Bóng rổ (Nam: 8, Nữ: 4); Cờ vua (Nam: 3, Nữ: 5).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng số liệu thống kê chung của cả lớp. | **Bảng thống kê sở thích thể thao lớp 6:**<br><br>| Môn thể thao | Bóng đá | Bơi lội | Cầu lông | Bóng rổ | Cờ vua |<br>| :--- | :---: | :---: | :---: | :---: | :---: |<br>| Nam | 14 | 12 | 6 | 8 | 3 |<br>| Nữ | 2 | 15 | 10 | 4 | 5 | |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Vẽ poster biểu đồ cột kép trên giấy A0 và thuyết trình nhận xét trước lớp.
b) Nội dung: 4 nhóm thực hành vẽ biểu đồ cột kép trên giấy A0 bằng bút màu và phân tích số liệu.
c) Sản phẩm: Poster biểu đồ cột kép rực rỡ của các nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát giấy A0 và bút dạ màu cho 4 nhóm. Yêu cầu vẽ biểu đồ cột kép biểu diễn bảng thống kê trên, ghi rõ chú giải và viết 2 nhận xét, 1 đề xuất hoạt động hè.<br>- **HS:** Các nhóm nhận vật liệu và phân công vẽ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm trưởng phân công: Bạn kẻ trục, bạn vẽ cột, bạn tô màu, bạn viết nhận xét.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các nhóm dán poster lên bảng lớp. Đại diện từng nhóm thuyết trình trong 2 phút.<br>- Nhận xét: Nam thích Bóng đá nhất (14 bạn); Nữ thích Bơi lội nhất (15 bạn). Môn có tổng số bạn yêu thích nhiều nhất là Bơi lội ($12 + 15 = 27$ bạn).<br>- Đề xuất: Nhà trường nên mở Câu lạc bộ Bơi lội và Câu lạc bộ Bóng đá trong hè.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao sự phối hợp nhóm tuyệt vời, tính chính xác và thẩm mỹ của các poster. | - Môn thể thao được cả lớp yêu thích nhất là Bơi lội.<br>- Bạn nam thích nhất là Bóng đá; Bạn nữ thích nhất là Bơi lội.<br>- Đề xuất thành lập CLB Bơi lội và CLB Bóng đá hè. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tổng kết toàn bộ năm học môn Toán lớp 6 và dặn dò kế hoạch hè an toàn, bổ ích.
b) Nội dung: Lời chúc mừng và dặn dò của giáo viên kết thúc chương trình Toán lớp 6.
c) Sản phẩm: Niềm vui và tinh thần sẵn sàng cho kỳ nghỉ hè bổ ích của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tổng kết chặng đường học tập môn Toán 6: Chúng ta đã chinh phục Số tự nhiên, Số nguyên, Hình học phẳng, Phân số, Số thập phân và Thống kê xác suất. Chúc mừng cả lớp đã hoàn thành xuất sắc chương trình năm học!<br>- **HS:** Lắng nghe và vỗ tay nhiệt liệt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chia sẻ những kỷ niệm đẹp trong giờ học Toán.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện lớp cảm ơn thầy cô giáo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò: Chú ý an toàn phòng chống đuối nước khi bơi lội, duy trì thói quen đọc sách và giữ gìn sức khỏe để chuẩn bị bước vào lớp 7 thành công hơn nữa! | Hoàn thành xuất sắc toàn bộ chương trình môn Toán lớp 6 năm học 2026 - 2027. |
"""
    }
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print("Hoàn tất tạo 13 KHBD Chương IX: Dữ liệu và Xác suất thực nghiệm (Tiết 81 - 101)!")
