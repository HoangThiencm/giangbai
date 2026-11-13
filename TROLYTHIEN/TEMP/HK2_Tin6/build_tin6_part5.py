# -*- coding: utf-8 -*-
"""
Script sinh Markdown cho các bài 09 -> 12 của Tin học 6 HK2
Bám sát 100% nội dung SGK và Phụ lục 3 của Thầy Hoàng Tấn Thiên.
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Tin6"

# 09. BÀI 16: CÁC CẤU TRÚC ĐIỀU KHIỂN (Tiết 30, 31)
bai16_md = """**TIẾT 30, 31 - BÀI 16: CÁC CẤU TRÚC ĐIỀU KHIỂN**
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
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS thảo luận cặp đôi: Ví dụ quy trình rửa tay bằng xà phòng 6 bước, quy trình pha sữa, thuật toán tính chu vi hình chữ nhật ($P = (a + b) \times 2$). | - HS nhận thấy các bước nối tiếp nhau bằng một đường thẳng duy nhất, không có rẽ nhánh hay quay đầu. |
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
"""

# 10. BÀI 17: CHƯƠNG TRÌNH MÁY TÍNH (Tiết 32, 33)
bai17_md = """**TIẾT 32, 33 - BÀI 17: CHƯƠNG TRÌNH MÁY TÍNH**
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được khái niệm chương trình máy tính: Chương trình máy tính là một dãy các lệnh được viết bằng một ngôn ngữ lập trình cụ thể nhằm chỉ dẫn cho máy tính thực hiện từng bước của một thuật toán để giải quyết một bài toán.
- Làm quen với môi trường lập trình trực quan Scratch: nhận biết các thành phần chính trong giao diện phần mềm (Vùng sân khấu Stage, Vùng quản lí nhân vật Sprites, Vùng chứa các nhóm khối lệnh Blocks, Vùng soạn thảo kịch bản Scripts Area).
- Hiểu ý nghĩa các nhóm khối lệnh cơ bản: Chuyển động (Motion: di chuyển, xoay), Hiển thị (Looks: nói lời thoại, đổi trang phục), Âm thanh (Sound: phát tiếng kêu), Sự kiện (Events: khi bấm vào cờ xanh), Điều khiển (Control: đợi, lặp lại).
- Thực hành lắp ghép các khối lệnh tạo chương trình máy tính đầu tiên điều khiển nhân vật chú mèo Scratch di chuyển, phát ra tiếng kêu 'Meow' và hiển thị lời chào trên màn hình.

## 2. Về năng lực
### a) Năng lực chung
- **Năng lực tự chủ và tự học:** Tự tìm hiểu và khám phá các khối lệnh trong Scratch; chủ động thử nghiệm kéo thả khối lệnh và quan sát phản ứng của nhân vật trên sân khấu.
- **Năng lực giao tiếp và hợp tác:** Cùng bạn thảo luận kịch bản chuyển động của nhân vật, phối hợp sửa lỗi chương trình (debug) khi nhân vật chạy không đúng ý muốn.

### b) Năng lực Tin học
- **Năng lực C (Tư duy máy tính và giải quyết vấn đề):**
  + Chuyển hóa thuật toán trên sơ đồ khối thành các dòng lệnh/khối lệnh máy tính cụ thể.
  + Hình thành tư duy lập trình viên: biết thử nghiệm, kiểm tra và gỡ lỗi từng bước.

### c) Năng lực Trí tuệ nhân tạo (AI)
- ***(Tích hợp AI 6.B2.1: Ứng dụng công cụ AI hỗ trợ gợi ý các khối lệnh lập trình; học sinh đối chiếu kết quả chạy chương trình với SGK để kiểm chứng tính chính xác (Áp dụng: tiết 1, 2))***: Học sinh biết sử dụng trợ lý AI để hỏi gợi ý: 'Làm thế nào để chú mèo Scratch đi hình vuông?'. Học sinh đối chiếu gợi ý của AI với các khối lệnh có sẵn trong SGK, trực tiếp lắp ghép khối lệnh trên máy tính và chạy thử nghiệm để kiểm chứng tính đúng đắn của gợi ý AI.

## 3. Về phẩm chất
- **Chăm chỉ:** Kiên nhẫn thử nghiệm từng khối lệnh, không nản lòng khi chương trình gặp lỗi.
- **Sáng tạo:** Tự do sáng tạo lời thoại, thêm âm thanh và hình nền sân khấu cho nhân vật hoạt hình.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
## 1. Giáo viên
- Kế hoạch bài dạy, máy chiếu, bài giảng điện tử.
- Phòng máy tính đã cài đặt sẵn phần mềm Scratch 3.0 (hoặc truy cập trực tuyến `scratch.mit.edu`).
- Hình ảnh giao diện phần mềm Scratch (Hình 6.11 trang 72 SGK) và tệp chương trình mẫu `MeoCon_XinChao.sb3`.
## 2. Học sinh
- SGK Tin học 6 Kết nối tri thức (Trang 71 – 74), vở ghi bài.

---

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
### a) Mục tiêu
- Đặt ra vấn đề: Con người hiểu thuật toán bằng tiếng Việt, nhưng máy tính là cỗ máy điện tử thì làm sao hiểu được tiếng Việt để thực hiện công việc?
### b) Nội dung
- Học sinh quan sát tình huống mở đầu trang 71 SGK về giao tiếp giữa con người và máy tính.
### c) Sản phẩm
- Nhận thức của học sinh về sự cần thiết của Ngôn ngữ lập trình và Chương trình máy tính.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV đặt câu hỏi kích thích tư duy:<br>*"Ở bài trước chúng ta đã viết thuật toán bằng tiếng Việt. Nhưng nếu em nói 'Máy tính ơi, hãy tính trung bình cộng cho tôi' thì máy tính có tự động hiểu và tính được không? Làm thế nào để ra lệnh cho máy tính làm việc?"* | - HS suy nghĩ, trả lời: Máy tính không hiểu trực tiếp tiếng người nói, cần có một ngôn ngữ riêng để ra lệnh. |
| **+ Bước 2, 3: Thực hiện & Báo cáo**<br>- HS thảo luận và chỉ ra: Con người phải viết các câu lệnh chỉ dẫn cho máy tính bằng ngôn ngữ máy tính hiểu được, gọi là ngôn ngữ lập trình. | - Cả lớp lắng nghe và gật đầu đồng tình. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV dẫn dắt: Tập hợp các câu lệnh chỉ dẫn đó được gọi là **Chương trình máy tính**. Hôm nay chúng ta sẽ bước chân vào thế giới của các lập trình viên nhí qua: **Bài 17: Chương trình máy tính**. | - HS mở vở ghi tên bài mới. |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI & THỰC HÀNH (60 phút)
*(Tiết 1: Khái niệm chương trình và Khám phá Scratch; Tiết 2: Thực hành viết chương trình đầu tiên)*

### 1. Hoạt động 2.1: Khái niệm chương trình máy tính (15 phút - Tiết 1)
#### a) Mục tiêu
- Nêu được định nghĩa chương trình máy tính; hiểu được mối quan hệ giữa thuật toán và chương trình.
#### b) Nội dung
- Học sinh nghiên cứu mục 1 trang 71 SGK; trả lời câu hỏi củng cố trang 71.
#### c) Sản phẩm
- Ghi nhớ màu cam trang 71 SGK: *Chương trình máy tính là một dãy các lệnh chỉ dẫn cho máy tính thực hiện các bước của một thuật toán.*
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV yêu cầu HS đọc mục 1 trang 71 SGK và trả lời:<br>1. Chương trình máy tính là gì?<br>2. Người viết chương trình được gọi là gì?<br>3. Mối quan hệ giữa thuật toán và chương trình máy tính là gì? | - HS đọc thầm trang 71 SGK, gạch chân các ý chính. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS thảo luận theo cặp đôi.<br>- GV gợi ý: Thuật toán giống như bản vẽ thiết kế ngôi nhà, còn chương trình là ngôi nhà thực tế được xây bằng gạch đá (các câu lệnh). | - HS phân tích: Để máy tính thực hiện thuật toán, người lập trình (programmer) phải dịch thuật toán sang ngôn ngữ lập trình. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi đại diện học sinh trả lời câu hỏi củng cố trang 71 SGK:<br>*Chọn câu đúng: A. Chương trình là bản mô tả thuật toán bằng lời văn; B. Chương trình là một dãy các lệnh chỉ dẫn máy tính thực hiện thuật toán; C. Máy tính tự nghĩ ra chương trình.* | - HS chọn đáp án **B** hoàn toàn chính xác. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV tổng kết kiến thức mục 1 vào khung ghi nhớ. | - HS ghi bài vào vở. |

---

### 2. Hoạt động 2.2: Làm quen với môi trường lập trình Scratch (20 phút - Tiết 1)
#### a) Mục tiêu
- Nhận biết các vùng chức năng chính trên màn hình phần mềm Scratch 3.0 (Hình 6.11 trang 72 SGK).
#### b) Nội dung
- Học sinh quan sát màn hình Scratch máy tính và theo dõi hướng dẫn của GV.

![Giao diện phần mềm lập trình trực quan Scratch 3.0](khbd-ill:hinh-scratch-giaodien_6_11)

#### c) Sản phẩm
- Sơ đồ 4 vùng chức năng của Scratch; các nhóm khối lệnh cơ bản.
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV khởi động Scratch 3.0 và giới thiệu 4 vùng màn hình (Hình 6.11 trang 72 SGK):<br>1. *Vùng danh mục khối lệnh (Code Blocks):* Chứa các nhóm lệnh phân theo màu sắc (Chuyển động màu xanh lam, Hiển thị màu tím, Âm thanh màu hồng, Sự kiện màu vàng...).<br>2. *Vùng khu vực lập trình (Scripts Area):* Nơi kéo thả và lắp ghép các khối lệnh giống như trò chơi xếp hình Lego.<br>3. *Vùng sân khấu (Stage):* Nơi nhân vật biểu diễn hành động theo kịch bản.<br>4. *Vùng quản lí nhân vật (Sprites):* Quản lí chú mèo Scratch, phông nền sân khấu.<br>- GV giao nhiệm vụ cho học sinh khởi động Scratch trên máy và khám phá thử nghiệm. | - HS quan sát giao diện trực quan, đầy màu sắc của Scratch trên máy chiếu.<br>- HS mở Scratch trên máy tính phòng thực hành. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS thử kéo một khối lệnh `move 10 steps` vào vùng lập trình, nhấp đúp chuột và quan sát chú mèo nhích về phía trước trên sân khấu.<br>- GV hướng dẫn cách đổi ngôn ngữ sang Tiếng Việt (nhấp biểu tượng quả địa cầu ở góc trên bên trái). | - HS vô cùng thích thú khi thấy chú mèo di chuyển theo lệnh của mình gõ. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi học sinh chỉ ra vị trí nút cờ xanh (Bắt đầu) và nút tròn đỏ (Dừng lại). | - HS trả lời chính xác các nút điều khiển chính. |
| **+ Bước 4: Kết luận, nhận định (Chuyển giao Tiết 2)**<br>- GV nhận xét: Lập trình Scratch cực kỳ đơn giản và thú vị, chỉ cần kéo thả khối lệnh như lắp ghép đồ chơi Lego. Tiết sau cả lớp sẽ viết chương trình hoạt hình đầu tiên! | - HS lưu lại giao diện, chuẩn bị cho Tiết 2 thực hành. |

---

### 3. Hoạt động 2.3: Thực hành viết chương trình máy tính đầu tiên (25 phút - Tiết 2)
#### a) Mục tiêu
- Thực hành lắp ghép kịch bản khối lệnh điều khiển chú mèo Scratch: di chuyển, đổi hướng, phát âm thanh và nói lời chào 'Xin chào các bạn!'.
- ***(Tích hợp AI 6.B2.1)***: Vận dụng AI gợi ý khối lệnh và kiểm chứng thực tế.
#### b) Nội dung
- Học sinh thực hành trên máy tính theo hướng dẫn mục 3 trang 73 – 74 SGK.
#### c) Sản phẩm
- Chương trình Scratch hoàn chỉnh được lưu trên máy tính với tên `MeoCon_XinChao.sb3`.
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV giao nhiệm vụ thực hành: Hãy viết chương trình điều khiển chú mèo Scratch thực hiện kịch bản:<br>1. *Khi bấm vào lá cờ xanh (Sự kiện)*<br>2. *Di chuyển 50 bước (Chuyển động)*<br>3. *Phát âm thanh 'Meow' (Âm thanh)*<br>4. *Nói 'Xin chào các bạn!' trong 2 giây (Hiển thị)*<br>5. *Lưu tệp với tên:* `MeoCon_XinChao.sb3`.<br>- ***(Tích hợp AI 6.B2.1: GV hướng dẫn HS cách hỏi trợ lý AI: 'Để nhân vật Scratch vừa đi vừa nói thì ghép những khối lệnh nào?'. GV yêu cầu HS so sánh câu trả lời của AI với các khối lệnh trong SGK trang 73; tự mình kéo thả khối lệnh trên máy tính và bấm Cờ xanh để kiểm chứng xem gợi ý của AI có hoạt động đúng trên sân khấu không).*** | - HS tiếp nhận nhiệm vụ, mở Scratch trên máy tính.<br>- HS quan sát cách đặt câu hỏi cho AI và đối chiếu gợi ý của AI với các khối lệnh thực tế trong phần mềm. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS tiến hành kéo thả các khối lệnh từ danh mục vào vùng lập trình:<br>+ Khối `when green flag clicked` (Khi bấm vào cờ xanh)<br>+ Khối `move 50 steps` (Di chuyển 50 bước)<br>+ Khối `play sound Meow until done` (Phát âm thanh Meow)<br>+ Khối `say [Xin chào các bạn!] for 2 seconds` (Nói Xin chào các bạn! trong 2 giây)<br>- GV đi quanh hỗ trợ các học sinh ráp khớp nối các khối lệnh để chúng phát ra tiếng 'tách' gắn liền nhau. | - HS lắp ghép chính xác các khối lệnh theo trình tự.<br>- HS bấm cờ xanh và reo vui khi thấy chú mèo bước đi, kêu Meow vang phòng máy và hiện bóng bóng lời thoại 'Xin chào các bạn!'.<br>- HS vào Tập tin ➔ Lưu về máy tính với tên `MeoCon_XinChao.sb3`. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV trình chiếu bài làm của 3 học sinh lên màn hình lớn.<br>- Các học sinh biểu diễn sản phẩm hoạt hình của mình cho cả lớp xem. | - Cả lớp vỗ tay chúc mừng những lập trình viên nhí đầu tiên của lớp. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV nhận xét: Chúc mừng các em đã chính thức trở thành lập trình viên, biến máy tính thành công cụ sáng tạo hoạt hình tuyệt vời! | - HS hào hứng ghi nhớ các khối lệnh cơ bản. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (15 phút - Tiết 2)
### a) Mục tiêu
- Củng cố và mở rộng kỹ năng lập trình: sử dụng vòng lặp `repeat 4` để chú mèo đi thành hình vuông trên sân khấu qua bài tập SGK trang 74.
### b) Nội dung
- Học sinh làm bài tập phần Luyện tập trang 74 SGK.
### c) Sản phẩm
- Chương trình Scratch điều khiển chú mèo di chuyển hình vuông và vẽ nét đường đi.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV nêu bài tập Luyện tập trang 74 SGK: Làm thế nào để chú mèo di chuyển thành một hình vuông?<br>- GV gợi ý: Hình vuông có 4 cạnh bằng nhau và 4 góc vuông 90 độ. Hãy kết hợp khối `move 100 steps`, khối `turn right 90 degrees` và khối lặp `repeat 4`. | - HS suy nghĩ về hình học và thuật toán lặp. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS kéo khối `repeat 4`, đặt bên trong là `move 100 steps` và `turn right 90 degrees`, thêm khối `wait 1 seconds` để nhìn rõ từng bước đi. | - HS chạy thử nghiệm, chú mèo di chuyển đúng 4 cạnh hình vuông quanh sân khấu. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi 1 học sinh giải thích vì sao lại lặp lại 4 lần và vì sao phải xoay 90 độ. | - HS giải thích: Vì hình vuông có 4 cạnh và góc quay giữa hai cạnh là 90 độ. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV khen ngợi tư duy thuật toán hình học xuất sắc của học sinh. | - HS lưu lại bài tập `MeoDiHinhVuong.sb3`. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút - Tiết 2)
### a) Mục tiêu
- Vận dụng kiến thức lập trình Scratch để làm một đoạn phim hoạt hình ngắn giới thiệu về cuốn sổ lưu niệm của lớp.
### b) Nội dung
- Học sinh thực hiện yêu cầu phần Vận dụng trang 74 SGK: Lập trình chú mèo cầm cuốn sổ lưu niệm và nói lời giới thiệu về các thành viên lớp 6A.
### c) Sản phẩm
- Hoạt hình Scratch giới thiệu Sổ lưu niệm lớp 6A.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV giao nhiệm vụ dự án Vận dụng: Hãy đổi hình nền sân khấu thành phòng học (Chamber/School) và lập trình chú mèo nói: 'Chào mừng các bạn đến với Sổ lưu niệm lớp 6A!'. | - HS hào hứng chọn phông nền sân khấu mới và viết kịch bản lời thoại. |
| **+ Bước 2, 3: Thực hiện & Báo cáo**<br>- HS hoàn thành sản phẩm và chiếu thử cho bạn bên cạnh xem. | - Các bạn cùng trao đổi, góp ý cho lời thoại thêm phần dí dỏm. |
| **+ Bước 4: Kết luận & Dặn dò về nhà**<br>- GV tổng kết bài học: Kết thúc toàn bộ chương trình kiến thức HK2 môn Tin học 6.<br>- **Dặn dò về nhà:** Ôn tập toàn bộ lý thuyết và thực hành từ Bài 9 đến Bài 17 để chuẩn bị cho tiết **Ôn tập cuối học kì II** ở tuần sau. | - HS lưu bài, tắt máy và chuẩn bị kết thúc năm học. |
"""

# 11. ÔN TẬP CUỐI HỌC KÌ II (Tiết 34)
bai11_ontap_md = """**TIẾT 34 - ÔN TẬP CUỐI HỌC KÌ II**
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ các mảng kiến thức trọng tâm của môn Tin học 6 trong Học kì II theo chuẩn chương trình GDPT 2018:
  + Chủ đề 4: Đạo đức, pháp luật và văn hoá trong môi trường số (Bài 9: An toàn thông tin trên Internet, các nguy cơ mạng, 5 quy tắc an toàn).
  + Chủ đề 5: Ứng dụng Tin học (Bài 10: Sơ đồ tư duy; Bài 11: Định dạng văn bản; Bài 12: Trình bày bảng biểu; Bài 13: Tìm kiếm thay thế; Bài 14: Thực hành tổng hợp).
  + Chủ đề 6: Giải quyết vấn đề với sự trợ giúp của máy tính (Bài 15: Thuật toán; Bài 16: Các cấu trúc điều khiển; Bài 17: Chương trình máy tính và Scratch).
- Rèn luyện kỹ năng tổng hợp kiến thức bằng sơ đồ tư duy Mindmap tổng quan.
- Rèn luyện kỹ năng giải các câu hỏi trắc nghiệm khách quan và xử lí các tình huống thực hành tin học thực tế.

## 2. Về năng lực
- **Năng lực tự chủ và tự học:** Tự giác rà soát lại toàn bộ kiến thức đã học trong học kì II, lập kế hoạch ôn tập khoa học.
- **Năng lực giao tiếp và hợp tác:** Tham gia tích cực trò chơi học tập 'Rung chuông vàng Tin học 6', biết phối hợp giải thích các câu hỏi khó cho bạn bè.

## 3. Về phẩm chất
- **Chăm chỉ:** Tích cực ôn luyện, làm đầy đủ các bài tập trong đề cương ôn tập cuối năm.
- **Tự tin:** Sẵn sàng bước vào kỳ kiểm tra đánh giá cuối năm học với tâm thế vững vàng nhất.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. **Giáo viên:** Kế hoạch bài dạy, bài giảng trình chiếu tổng hợp, hệ thống câu hỏi trò chơi Quizizz / Kahoot, đề cương ôn tập cuối HK2.
2. **Học sinh:** SGK Tin học 6, vở ghi bài, đề cương ôn tập đã làm sẵn ở nhà.

---

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
- GV tổ chức trò chơi khởi động 'Vòng quay kỳ diệu': Quay ngẫu nhiên tên các chủ đề đã học trong HK2 để học sinh nêu nhanh từ khóa cốt lõi của chủ đề đó. Tạo tâm thế hứng khởi cho tiết ôn tập.

## B. HOẠT ĐỘNG 2: HỆ THỐNG HÓA KIẾN THỨC BẰNG SƠ ĐỒ TƯ DUY (15 phút)
- **Hoạt động 2.1: Sơ đồ hóa kiến thức Học kì II**
  + GV trình chiếu sơ đồ tư duy tổng thể gồm 3 nhánh lớn:
    1. *Nhánh 1 - An toàn thông tin:* 5 nguy cơ; 5 quy tắc an toàn (Giữ an toàn, Không gặp gỡ, Đừng chấp nhận, Kiểm tra độ tin cậy, Hãy nói ra); Mật khẩu mạnh.
    2. *Nhánh 2 - Ứng dụng Tin học:* Sơ đồ tư duy MindMaple; Định dạng đoạn và trang văn bản Word; Bảng biểu (Merge Cells, căn lề ô); Tìm kiếm và Thay thế (Ctrl+F, Ctrl+H).
    3. *Nhánh 3 - Thuật toán & Lập trình:* Khái niệm thuật toán, Input, Output; Sơ đồ khối (5 hình quy ước); 3 cấu trúc điều khiển (Tuần tự, Rẽ nhánh, Lặp); Chương trình máy tính Scratch.
  + HS thảo luận và hoàn thiện sơ đồ tư duy ôn tập vào vở.

## C. HOẠT ĐỘNG 3: LUYỆN TẬP GIẢI ĐỀ CƯƠNG (20 phút)
- GV chia lớp thành 4 đội thi đấu giải bộ 20 câu hỏi trắc nghiệm tiêu biểu bao quát toàn bộ 3 chủ đề.
- GV phân tích kỹ các câu hỏi vận dụng thực hành:
  + Cách xử lí bảng biểu khi chèn thêm hàng/cột.
  + Phân biệt nhánh ĐÚNG/SAI trong cấu trúc rẽ nhánh của sơ đồ khối.
  + Thứ tự ghép các khối lệnh Scratch.

## D. HOẠT ĐỘNG 4: VẬN DỤNG & DẶN DÒ KIỂM TRA (5 phút)
- GV chốt lại cấu trúc bài kiểm tra cuối học kì II (Tiết 35):
  + Trắc nghiệm (4,0 điểm - 16 câu)
  + Thực hành máy tính (6,0 điểm - Lập trình Scratch vẽ hình và soạn thảo văn bản bảng biểu).
- Dặn dò học sinh ôn tập kỹ lưỡng để đạt kết quả cao nhất trong kỳ thi học kì.
"""

# 12. KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (Tiết 35)
bai12_kiemtra_md = """**TIẾT 35 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II**
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện kết quả học tập của học sinh trong toàn bộ Học kì II theo các yêu cầu cần đạt của Chương trình GDPT 2018 môn Tin học lớp 6.
- Đo lường mức độ nắm vững lý thuyết và thành thạo kỹ năng thực hành qua 3 mảng kiến thức lớn: An toàn thông tin mạng, Ứng dụng phần mềm soạn thảo văn bản và Tư duy thuật toán - Lập trình trực quan Scratch.

## 2. Về năng lực
- **Năng lực tự chủ và tự học:** Tự giác làm bài nghiêm túc, trung thực, biết quản lí thời gian làm bài hiệu quả.
- **Năng lực tin học (NLA, NLC, NLD):** Vận dụng kiến thức tin học để giải quyết trọn vẹn các yêu cầu trắc nghiệm và bài toán thực hành trên máy tính.

## 3. Về phẩm chất
- **Trung thực:** Nghiêm túc, không gian lận trong thi cử.
- **Trách nhiệm:** Tuân thủ tuyệt đối quy chế thi và bảo quản thiết bị phòng máy.

---

# II. HÌNH THỨC VÀ MA TRẬN ĐỀ KIỂM TRA
1. **Hình thức:** Kết hợp Trắc nghiệm (4,0 điểm - 16 câu) và Thực hành trên máy (6,0 điểm).
2. **Thời gian:** 45 phút.
3. **Ma trận & Bản đặc tả:** Chuẩn Thông tư 22/2021/TT-BGDĐT.

---

# III. ĐỀ BÀI VÀ HƯỚNG DẪN CHẤM

### PHẦN I: TRẮC NGHIỆM KHÁCH QUAN (4,0 điểm - 16 câu, mỗi câu 0.25 điểm)
- Câu 1 (Chủ đề 4): Nhận diện hành vi vi phạm an toàn thông tin trên mạng.
- Câu 2 (Chủ đề 4): Biện pháp bảo vệ mật khẩu và tài khoản cá nhân.
- Câu 3 (Chủ đề 4): 5 quy tắc an toàn Internet (Quy tắc SMART).
- Câu 4 (Chủ đề 5): Lợi ích của sơ đồ tư duy so với văn bản liệt kê.
- Câu 5 (Chủ đề 5): Thao tác tạo chủ đề nhánh trong phần mềm MindMaple.
- Câu 6 (Chủ đề 5): Định dạng đoạn văn bản: phím tắt căn giữa, căn đều 2 bên.
- Câu 7 (Chủ đề 5): Định dạng trang: chọn hướng trang Portrait và lề trang Normal.
- Câu 8 (Chủ đề 5): Ưu điểm của việc trình bày thông tin ở dạng bảng.
- Câu 9 (Chủ đề 5): Thao tác gộp ô Merge Cells trong bảng biểu Word.
- Câu 10 (Chủ đề 5): Thao tác chèn thêm cột bên phải (Insert Right).
- Câu 11 (Chủ đề 5): Phím tắt mở hộp thoại Tìm kiếm (Ctrl+F) và Thay thế (Ctrl+H).
- Câu 12 (Chủ đề 5): Phân biệt lệnh Replace và Replace All.
- Câu 13 (Chủ đề 6): Định nghĩa thuật toán, xác định Input và Output.
- Câu 14 (Chủ đề 6): Ý nghĩa khối hình thoi trong sơ đồ khối (Kiểm tra điều kiện).
- Câu 15 (Chủ đề 6): Phân biệt 3 cấu trúc điều khiển: Tuần tự, Rẽ nhánh, Lặp.
- Câu 16 (Chủ đề 6): Khái niệm chương trình máy tính và ngôn ngữ lập trình Scratch.

### PHẦN II: THỰC HÀNH TRÊN MÁY TÍNH (6,0 điểm)
- **Bài 1 (3.0 điểm): Soạn thảo và Bảng biểu**
  Tạo tệp Word `HocKy2_HoTen.docx`, định dạng khổ A4 đứng, lề Normal. Tạo bảng Thời gian biểu ôn thi gồm 4 cột, 4 hàng, gộp ô tiêu đề và tô màu nền nhạt, căn giữa dữ liệu trong ô.
- **Bài 2 (3.0 điểm): Lập trình Scratch**
  Mở phần mềm Scratch, lập trình nhân vật chú mèo thực hiện kịch bản:
  + Khi bấm cờ xanh, nhân vật nói 'Bắt đầu vẽ hình!' trong 1 giây.
  + Lặp lại 4 lần: Di chuyển 80 bước, xoay phải 90 độ, đợi 0.5 giây.
  + Kết thúc: Phát âm thanh 'Meow' và nói 'Đã hoàn thành!'.
  + Lưu tệp với tên `HinhVuong_HoTen.sb3`.

---

# IV. TỔ CHỨC THỰC HIỆN
- Giám thị coi thi phát đề, phổ biến quy chế, giám sát học sinh làm bài nghiêm túc.
- Thu bài và niêm phong dữ liệu bài thi trên máy chủ phòng máy.
"""

with open(os.path.join(temp_dir, "09_KHBD_Tin6_Bai16_CacCauTrucDieuKhien_Tiet30-31.md"), "w", encoding="utf-8") as f:
    f.write(bai16_md)

with open(os.path.join(temp_dir, "10_KHBD_Tin6_Bai17_ChuongTrinhMayTinh_Tiet32-33.md"), "w", encoding="utf-8") as f:
    f.write(bai17_md)

with open(os.path.join(temp_dir, "11_KHBD_Tin6_OnTapCuoiHK2_Tiet34.md"), "w", encoding="utf-8") as f:
    f.write(bai11_ontap_md)

with open(os.path.join(temp_dir, "12_KHBD_Tin6_KiemTraCuoiHK2_Tiet35.md"), "w", encoding="utf-8") as f:
    f.write(bai12_kiemtra_md)

print("Đã tạo hoàn tất Markdown cho toàn bộ các bài 09 -> 12 của Tin học 6 HK2!")
