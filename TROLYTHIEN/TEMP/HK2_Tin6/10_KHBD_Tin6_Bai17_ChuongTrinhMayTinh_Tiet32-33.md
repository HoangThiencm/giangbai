**TIẾT 32, 33 - BÀI 17: CHƯƠNG TRÌNH MÁY TÍNH**
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
