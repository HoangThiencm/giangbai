**TIẾT 30, 31 - BÀI 16: CÁC CẤU TRÚC ĐIỀU KHIỂN**
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và phân biệt được 3 cấu trúc điều khiển cơ bản trong thuật toán và lập trình: Cấu trúc tuần tự (Sequential structure), Cấu trúc rẽ nhánh (Selection structure: dạng thiếu 'Nếu... thì...' và dạng đủ 'Nếu... thì... không thì...'), Cấu trúc lặp (Loop/Iteration structure: lặp với số lần cố định và lặp có điều kiện).
- Hiểu được ý nghĩa, vai trò của từng cấu trúc điều khiển trong việc giải quyết các bài toán đời sống và bài toán khoa học.
- Nhận biết và vẽ đúng biểu diễn của 3 cấu trúc điều khiển bằng sơ đồ khối sử dụng khối hình thoi để kiểm tra điều kiện ĐÚNG (True) / SAI (False).
- Xác định và phân tích được cấu trúc điều khiển phù hợp cho các tình huống thực tế (quy trình đánh răng, robot hút bụi tránh chướng ngại vật, thuật toán tính tiền cước taxi, vòng lặp tập thể dục).

## 2. Về năng lực
### a) Năng lực chung
- **Năng lực tự chủ và tự học:** Tự giác nghiên cứu các sơ đồ khối trong SGK; chủ động phân tích các tình huống điều kiện ĐÚNG / SAI trong thực tế.
- **Năng lực giao tiếp và hợp tác:** Thảo luận nhóm sôi nổi, biết lắng nghe và cùng nhau xây dựng sơ đồ khối điều khiển hoạt động của robot thông minh.

### b) Năng lực Tin học
- **Năng lực C (Tư duy máy tính và lập trình):** Rèn luyện tư duy logic: phân tích bài toán thành các nhánh rẽ và vòng lặp có điều kiện; biết tối ưu hóa các bước thực hiện bằng cấu trúc lặp thay vì viết đi viết lại nhiều lần.

## 3. Về phẩm chất
- **Chăm chỉ:** Kiên trì phân tích từng trường hợp rẽ nhánh, không nản lòng khi gặp các bài toán có nhiều nhánh điều kiện lồng nhau.
- **Chính xác:** Cẩn trọng trong việc xác định điều kiện và hướng mũi tên ĐÚNG/SAI trong sơ đồ khối.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
## 1. Giáo viên
- Kế hoạch bài dạy, bài giảng trình chiếu PowerPoint.
- Hình ảnh minh họa trích xuất từ SGK: Hình 6.7 (Sơ đồ khối cấu trúc rẽ nhánh trang 68), sơ đồ cấu trúc lặp trang 69 SGK.
## 2. Học sinh
- SGK Tin học 6 Kết nối tri thức (Trang 67 – 70), vở ghi bài, thước kẻ.

---

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
### a) Mục tiêu
- Dẫn dắt học sinh nhận ra trong cuộc sống không phải công việc nào cũng diễn ra tuần tự thẳng tuột từ đầu đến cuối mà thường xuyên có các tình huống cần đưa ra quyết định hoặc lặp đi lặp lại một hành động.
### b) Nội dung
- Học sinh quan sát tình huống chú Robot hút bụi thông minh đang di chuyển trong phòng khách (trang 67 SGK).
### c) Sản phẩm
- Câu trả lời của học sinh về cách xử lí của robot khi gặp chướng ngại vật và khi nào robot dừng hút bụi.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV chiếu hình ảnh chú Robot hút bụi thông minh và nêu tình huống:<br>*Một chú robot hút bụi tự động đang di chuyển thẳng để làm sạch sàn nhà. Bất ngờ phía trước xuất hiện một chân bàn hoặc một bức tường chắn ngang. Theo em robot sẽ làm gì? Làm thế nào để robot không bị đâm vào tường và biết khi nào thì pin yếu để tự quay về dock sạc?* | - HS quan sát hình ảnh robot hút bụi, liên hệ với thiết bị thông minh trong gia đình. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS suy nghĩ trong 1 phút: Robot cần kiểm tra cảm biến: *Nếu gặp vật cản thì quay sang hướng khác; Nếu pin dưới 10% thì quay về trạm sạc*. | - HS nhận ra robot hoạt động theo các quy tắc kiểm tra điều kiện. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV mời 2 học sinh trả lời trước lớp. | - HS phát biểu: *"Thưa thầy, robot phải biết rẽ nhánh khi gặp vật cản và lặp lại công việc hút bụi cho đến khi hết phòng hoặc hết pin."* |
| **+ Bước 4: Kết luận, nhận định**<br>- GV nhận xét: Đúng vậy! Để máy móc và con người xử lí linh hoạt mọi tình huống phức tạp, thuật toán cần sử dụng **Các cấu trúc điều khiển**. Chúng ta cùng tìm hiểu bài học hôm nay: **Bài 16: Các cấu trúc điều khiển**. | - HS mở vở ghi tên bài mới. |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (60 phút)
*(Tiết 1: Cấu trúc tuần tự và Cấu trúc rẽ nhánh; Tiết 2: Cấu trúc lặp và Thực hành vẽ sơ đồ khối)*

### 1. Hoạt động 2.1: Cấu trúc tuần tự (15 phút - Tiết 1)
#### a) Mục tiêu
- Hiểu được khái niệm cấu trúc tuần tự: các bước thực hiện lần lượt theo đúng thứ tự viết ra, từ bước đầu tiên đến bước cuối cùng.
#### b) Nội dung
- Học sinh nghiên cứu mục 1 trang 67 SGK, phân tích ví dụ thuật toán đánh răng hoặc thuật toán gấp giấy ở Bài 15.
#### c) Sản phẩm
- Sơ đồ khối cấu trúc tuần tự và câu trả lời củng cố trang 67 SGK.
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV yêu cầu học sinh đọc mục 1 trang 67 SGK và trả lời: Thế nào là cấu trúc tuần tự? Nêu ví dụ các công việc hàng ngày diễn ra tuần tự? | - HS mở SGK trang 67, nghiên cứu khái niệm cấu trúc tuần tự. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS thảo luận cặp đôi: Ví dụ quy trình rửa tay bằng xà phòng 6 bước, quy trình pha sữa, thuật toán tính chu vi hình chữ nhật ($P = (a + b) 	imes 2$). | - HS nhận thấy các bước nối tiếp nhau bằng một đường thẳng duy nhất, không có rẽ nhánh hay quay đầu. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi đại diện học sinh phát biểu định nghĩa.<br>- Cả lớp giải quyết câu hỏi củng cố trang 67 SGK: *Trong cấu trúc tuần tự, các bước được thực hiện như thế nào?* | - HS trả lời: Các bước được thực hiện lần lượt theo đúng trình tự từ trên xuống dưới, hoàn thành bước này mới chuyển sang bước tiếp theo. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV chốt lại khung ghi nhớ: Cấu trúc tuần tự là cấu trúc cơ bản nhất của mọi thuật toán. | - HS ghi bài vào vở. |

---

### 2. Hoạt động 2.2: Cấu trúc rẽ nhánh (25 phút - Tiết 1)
#### a) Mục tiêu
- Phân biệt cấu trúc rẽ nhánh dạng thiếu và dạng đủ; biết cách biểu diễn bằng sơ đồ khối với khối hình thoi.
#### b) Nội dung
- Học sinh quan sát Hình 6.7 trang 68 SGK; phân tích ví dụ dự báo thời tiết 'Nếu trời mưa thì mang áo mưa'.

![Sơ đồ khối cấu trúc rẽ nhánh dạng thiếu và dạng đủ](khbd-ill:hinh-sodokhoi_renhanh_6_7)

#### c) Sản phẩm
- Sơ đồ khối rẽ nhánh; đáp án 2 câu hỏi củng cố trang 68 SGK.
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV trình chiếu Hình 6.7 và giới thiệu 2 dạng rẽ nhánh:<br>1. *Dạng thiếu (Nếu... thì...):* Kiểm tra điều kiện ➔ Nếu ĐÚNG thì thực hiện câu lệnh A; Nếu SAI thì bỏ qua chuyển sang bước tiếp theo.<br>2. *Dạng đủ (Nếu... thì... không thì...):* Kiểm tra điều kiện ➔ Nếu ĐÚNG thì thực hiện câu lệnh A; Nếu SAI thì thực hiện câu lệnh B.<br>- Yêu cầu HS lấy ví dụ đời sống cho cả 2 dạng. | - HS quan sát 2 sơ đồ khối trên màn hình, chú ý 2 nhánh rẽ tỏa ra từ khối hình thoi: nhánh ĐÚNG (Yes) và nhánh SAI (No). |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS làm việc theo nhóm 4 bạn:<br>+ Ví dụ dạng thiếu: *Nếu trời mưa thì em mang theo áo mưa.*<br>+ Ví dụ dạng đủ: *Nếu hôm nay là Chủ nhật thì em được đi chơi công viên, không thì em phải đi học.*<br>+ Ví dụ Toán học: *Nếu $a > 0$ thì $a$ là số dương, không thì $a$ không phải số dương.* | - Các nhóm thảo luận hào hứng, tìm ra nhiều ví dụ phong phú. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2 nhóm trình bày.<br>- Cả lớp giải quyết câu hỏi củng cố trang 68 SGK: *Biểu diễn điều kiện trong sơ đồ khối bằng hình gì? Khối hình thoi có bao nhiêu nhánh rẽ đi ra?* | - HS trả lời: Biểu diễn bằng **Hình thoi**; luôn có **2 nhánh rẽ** đi ra ứng với trường hợp ĐÚNG và SAI. |
| **+ Bước 4: Kết luận, nhận định (Chuyển giao Tiết 2)**<br>- GV tổng kết: Cấu trúc rẽ nhánh giúp máy tính có khả năng ra quyết định dựa trên điều kiện thực tế. Tiết sau cả lớp sẽ khám phá cấu trúc lặp. | - HS ghi nhớ kiến thức, chuẩn bị cho Tiết 2. |

---

### 3. Hoạt động 2.3: Cấu trúc lặp (20 phút - Tiết 2)
#### a) Mục tiêu
- Nhận biết cấu trúc lặp trong thuật toán; phân biệt lặp với số lần biết trước và lặp có điều kiện; vẽ được sơ đồ khối cấu trúc lặp.
#### b) Nội dung
- Học sinh nghiên cứu mục 3 trang 69 SGK, phân tích ví dụ kim đồng hồ quay, thuật toán nhảy dây 100 cái hoặc rửa bát cho đến khi sạch.
#### c) Sản phẩm
- Sơ đồ khối cấu trúc lặp; đáp án câu hỏi củng cố trang 69 SGK.
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV đặt câu hỏi: Khi học bài tập đọc, nếu chưa thuộc thì em làm gì? Khi tập thể dục nhảy dây 50 lần, em đếm thế nào?<br>- GV giới thiệu cấu trúc lặp: Khi một hành động được lặp đi lặp lại nhiều lần cho đến khi thỏa mãn một điều kiện dừng nào đó.<br>- GV chiếu sơ đồ khối lặp (trang 69 SGK): Nhánh quay ngược trở lại phía trước để tạo thành một vòng khép kín (vòng lặp). | - HS nhận ra: Chưa thuộc bài thì đọc lại; nhảy dây thì lặp lại động tác nhảy 50 lần; kim giây đồng hồ lặp lại 60 lần tích tắc tạo thành 1 phút. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS thảo luận phân biệt 2 dạng lặp:<br>1. *Lặp với số lần biết trước:* Nhảy dây 50 lần, chống đẩy 20 cái, viết chính tả 3 lần.<br>2. *Lặp với điều kiện (chưa biết trước số lần):* Rửa bát đến khi sạch dầu mỡ; chạy bộ cho đến khi mệt thì nghỉ. | - HS phân tích sự khác nhau giữa điều kiện dừng của 2 trường hợp. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi học sinh lên bảng vẽ sơ đồ khối vòng lặp rửa bát.<br>- Cả lớp quan sát đường mũi tên quay ngược lại kiểm tra: *Đã sạch chưa? Nếu Chưa (SAI) ➔ Rửa tiếp; Nếu Rồi (ĐÚNG) ➔ Tráng nước sạch và Dừng*. | - HS hiểu sâu sắc bản chất của vòng lặp máy tính. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV chốt lại khung màu cam trang 70 SGK: Cấu trúc lặp giúp giải quyết những công việc mang tính lặp lại một cách cực kỳ ngắn gọn, không cần viết lại hàng nghìn dòng lệnh giống nhau. | - HS ghi bài vào vở. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (15 phút - Tiết 2)
### a) Mục tiêu
- Nhận diện chính xác 3 cấu trúc điều khiển trong các tình huống thực tế và bài toán tin học qua các câu hỏi SGK trang 70.
### b) Nội dung
- Học sinh làm việc nhóm giải quyết Bài tập 1 và Bài tập 2 trang 70 SGK.
### c) Sản phẩm
- Bảng phân loại các câu lệnh thuộc cấu trúc tuần tự, rẽ nhánh hay lặp.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV chiếu các tình huống Luyện tập (trang 70 SGK):<br>1. *Mỗi sáng thức dậy: đánh răng ➔ rửa mặt ➔ ăn sáng ➔ đi học.* (Cấu trúc gì?)<br>2. *Nếu đèn tín hiệu giao thông màu đỏ thì dừng lại, nếu màu xanh thì đi tiếp.* (Cấu trúc gì?)<br>3. *Hàng ngày, người đưa thư đi phát báo cho đến khi phát hết báo trên xe.* (Cấu trúc gì?)<br>4. *Thuật toán tính giá cước taxi: 1km đầu 12.000đ; từ km thứ 2 đến km thứ 10 giá 10.000đ/km; từ km thứ 11 trở đi giá 8.000đ/km.* (Cấu trúc gì?) | - Các nhóm thảo luận nhanh và ghi đáp án vào bảng con. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS trao đổi sôi nổi trong nhóm 2 phút. | - Các nhóm giơ bảng kết quả. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- Kết quả chuẩn xác:<br>+ Tình huống 1: Cấu trúc **Tuần tự**.<br>+ Tình huống 2: Cấu trúc **Rẽ nhánh (dạng đủ)**.<br>+ Tình huống 3: Cấu trúc **Lặp (có điều kiện)**.<br>+ Tình huống 4: Cấu trúc **Rẽ nhánh lồng nhau**. | - Cả lớp nhất trí 100% với đáp án. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV chấm điểm biểu dương các nhóm nắm bài xuất sắc. | - HS tự chấm điểm và chữa bài vào vở. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút - Tiết 2)
### a) Mục tiêu
- Vẽ sơ đồ khối hoàn chỉnh kết hợp cả cấu trúc tuần tự, rẽ nhánh và lặp để điều khiển robot lau nhà thông minh.
### b) Nội dung
- Học sinh làm bài tập phần Vận dụng trang 70 SGK: Mô tả thuật toán robot lau nhà tránh chướng ngại vật bằng sơ đồ khối.
### c) Sản phẩm
- Sơ đồ khối thuật toán robot lau nhà trên vở học sinh.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV giao nhiệm vụ Vận dụng trang 70 SGK: Hãy vẽ sơ đồ khối mô tả thuật toán cho robot lau nhà:<br>+ Bắt đầu lau từ góc phòng ➔ Di chuyển thẳng ➔ Kiểm tra phía trước có vật cản không? (Nếu có thì quay sang phải 90 độ, không thì đi tiếp) ➔ Kiểm tra đã lau hết phòng chưa? (Nếu chưa thì lặp lại việc lau, nếu rồi thì quay về dock sạc và kết thúc). | - HS chăm chú lắng nghe yêu cầu bài toán điều khiển robot. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS vẽ sơ đồ khối vào vở, sử dụng đầy đủ các khối: Oval (Bắt đầu/Kết thúc), Hình chữ nhật (Di chuyển, Quay phải), Hình thoi (Gặp vật cản? Hết phòng?). | - HS tập trung vẽ cẩn thận, kẻ mũi tên rõ ràng. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV mời 1 học sinh lên bảng vẽ sơ đồ khối.<br>- Cả lớp cùng phân tích dòng điều khiển của robot. | - HS quan sát và cảm thấy rất thích thú khi hiểu được nguyên lí vận hành của các thiết bị tự động hóa. |
| **+ Bước 4: Kết luận, nhận định & Dặn dò về nhà**<br>- GV tổng kết bài học: 3 cấu trúc Tuần tự - Rẽ nhánh - Lặp là nền tảng của mọi ngôn ngữ lập trình trên thế giới.<br>- **Dặn dò về nhà:** Chuẩn bị máy tính để tuần sau học bài lập trình thực hành: **Bài 17: Chương trình máy tính**. | - HS ghi chép dặn dò và kết thúc buổi học. |
