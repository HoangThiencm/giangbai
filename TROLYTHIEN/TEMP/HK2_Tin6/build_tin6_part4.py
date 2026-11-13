# -*- coding: utf-8 -*-
"""
Script sinh Markdown cho các bài 07 -> 12 của Tin học 6 HK2
Bám sát 100% nội dung SGK và Phụ lục 3 của Thầy Hoàng Tấn Thiên.
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Tin6"

# 07. KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (Tiết 28)
bai07_md = """**TIẾT 28 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II**
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ đạt chuẩn kiến thức, kỹ năng của học sinh sau khi học xong Chủ đề 4 (Đạo đức, pháp luật và văn hoá trong môi trường số: Bài 9) và Chủ đề 5 (Ứng dụng Tin học: Bài 10, Bài 11, Bài 12, Bài 13, Bài 14).
- Kiểm tra khả năng nhận biết các nguy cơ trên không gian mạng và các quy tắc bảo đảm an toàn thông tin cá nhân.
- Kiểm tra kỹ năng thực hành trên máy tính: tạo sơ đồ tư duy, soạn thảo và định dạng đoạn văn bản, tạo và căn chỉnh bảng biểu, sử dụng công cụ tìm kiếm và thay thế để biên tập văn bản.

## 2. Về năng lực
- **Năng lực tự chủ và tự học:** Nghiêm túc làm bài độc lập, trung thực trong kiểm tra, biết phân bổ thời gian hợp lí giữa phần lý thuyết trắc nghiệm và phần thực hành thao tác trên máy tính.
- **Năng lực giải quyết vấn đề với sự trợ giúp của CNTT (Năng lực C):** Vận dụng linh hoạt các kỹ năng phần mềm soạn thảo văn bản để xử lí một văn bản thực tế theo đúng yêu cầu kỹ thuật.

## 3. Về phẩm chất
- **Trung thực:** Tự giác làm bài, không quay cóp, không sao chép bài làm của bạn trong phòng thực hành máy tính.
- **Trách nhiệm:** Có ý thức giữ gìn thiết bị máy tính, tuân thủ nghiêm túc nội quy phòng máy trong giờ kiểm tra.

---

# II. HÌNH THỨC VÀ CẤU TRÚC ĐỀ KIỂM TRA
1. **Hình thức kiểm tra:** Kết hợp Trắc nghiệm khách quan (40% - 4,0 điểm) và Thực hành trực tiếp trên máy tính (60% - 6,0 điểm).
2. **Thời gian làm bài:** 45 phút.
3. **Cấu trúc đề:**
   - Phần I: Trắc nghiệm (8 câu, mỗi câu 0.5 điểm) kiểm tra kiến thức Bài 9, 10, 11, 12, 13.
   - Phần II: Thực hành (1 bài tập tổng hợp) yêu cầu tạo văn bản có định dạng, bảng biểu và chèn ảnh.

---

# III. TIẾN TRÌNH TỔ CHỨC KIỂM TRA

## A. MA TRẬN VÀ BẢN ĐẶC TẢ ĐỀ KIỂM TRA
*(Được thiết kế chuẩn theo Thông tư 22/2021/TT-BGDĐT với 4 mức độ: Nhận biết, Thông hiểu, Vận dụng, Vận dụng cao)*

## B. ĐỀ KIỂM TRA VÀ HƯỚNG DẪN CHẤM CHI TIẾT

### PHẦN I: TRẮC NGHIỆM KHÁCH QUAN (4,0 điểm - 8 câu)
- **Câu 1 (Bài 9):** Khi sử dụng Internet, hành động nào sau đây là an toàn?
  A. Cung cấp mật khẩu cho bạn bè qua mạng xã hội.
  B. Đăng xuất tài khoản sau khi dùng xong trên máy tính công cộng.
  C. Mở tất cả các tệp đính kèm trong thư rác.
  D. Nhập thông tin thẻ ngân hàng của bố mẹ vào đường link trúng thưởng.
  *Đáp án: B*
- **Câu 2 (Bài 9):** Đâu là tiêu chí của một mật khẩu mạnh?
  A. Tên của em và năm sinh (vd: `an2013`).
  B. Dãy số liên tiếp dễ nhớ (vd: `12345678`).
  C. Dài từ 8 ký tự trở lên, gồm chữ hoa, chữ thường, số và ký tự đặc biệt (vd: `An@2026!`).
  D. Chỉ gồm các chữ cái viết thường ngắn gọn.
  *Đáp án: C*
- **Câu 3 (Bài 10):** Ai là người sáng tạo ra sơ đồ tư duy?
  A. Bill Gates. B. Steve Jobs. C. Tony Buzan. D. Blaise Pascal.
  *Đáp án: C*
- **Câu 4 (Bài 10):** Sơ đồ tư duy giúp chúng ta:
  A. Nhìn thấy bức tranh tổng thể và ghi nhớ thông tin tốt hơn.
  B. Tính toán bảng lương tự động.
  C. Quét sạch virus trong máy tính.
  D. Kết nối mạng Internet tốc độ cao.
  *Đáp án: A*
- **Câu 5 (Bài 11):** Để căn thẳng hai lề cho đoạn văn bản, em chọn nút lệnh nào trong nhóm Paragraph?
  A. Align Left. B. Center. C. Align Right. D. Justify.
  *Đáp án: D*
- **Câu 6 (Bài 11):** Để chọn hướng trang in là trang đứng, em chọn lệnh nào trong Page Setup?
  A. Orientation ➔ Landscape.
  B. Orientation ➔ Portrait.
  C. Margins ➔ Normal.
  D. Size ➔ A4.
  *Đáp án: B*
- **Câu 7 (Bài 12):** Muốn gộp nhiều ô thành một ô trong bảng, em chọn các ô đó rồi nhấp lệnh:
  A. Split Cells. B. Delete Cells. C. Merge Cells. D. Insert Table.
  *Đáp án: C*
- **Câu 8 (Bài 13):** Tổ hợp phím tắt để mở nhanh hộp thoại Thay thế (Replace) là:
  A. Ctrl+F. B. Ctrl+H. C. Ctrl+S. D. Ctrl+P.
  *Đáp án: B*

### PHẦN II: THỰC HÀNH TRÊN MÁY TÍNH (6,0 điểm)
**Đề bài:** Khởi động phần mềm Microsoft Word, thực hiện các yêu cầu sau:
1. *Định dạng trang (1.0 điểm):* Chọn khổ giấy A4, hướng trang đứng Portrait, lề trang Normal (Top: 2.54cm, Bottom: 2.54cm, Left: 2.54cm, Right: 2.54cm).
2. *Gõ tiêu đề và định dạng (1.5 điểm):*
   Gõ tiêu đề in hoa đậm: `THỜI GIAN BIỂU HỌC TẬP VÀ SINH HOẠT`, font Times New Roman, cỡ 16pt, căn giữa.
3. *Tạo bảng và nhập dữ liệu (2.5 điểm):*
   Tạo bảng gồm 4 cột, 5 hàng:
   - Cột 1: Buổi (Sáng, Chiều, Tối). Gộp các ô phù hợp.
   - Cột 2: Thời gian.
   - Cột 3: Hoạt động học tập / sinh hoạt.
   - Cột 4: Ghi chú.
   Nhập đầy đủ thông tin thời gian biểu cá nhân, căn giữa tiêu đề cột, tô màu nền nhạt cho hàng tiêu đề.
4. *Tìm kiếm và thay thế (1.0 điểm):*
   Sử dụng công cụ Replace để tìm từ 'Chiều' và thay bằng cụm từ 'Buổi chiều'. Lưu tệp với tên `KiemTra_HoVaTen.docx`.

---

## C. TỔ CHỨC THỰC HIỆN VÀ ĐÁNH GIÁ
- GV phát đề trắc nghiệm, giám sát học sinh làm bài nghiêm túc trong 15 phút đầu.
- Hết 15 phút, thu bài trắc nghiệm; học sinh mở máy tính thực hiện phần thực hành trong 30 phút tiếp theo.
- Hết giờ, học sinh lưu bài vào thư mục nộp bài trên máy chủ mạng LAN; GV ký xác nhận nộp bài.
"""

# 08. BÀI 15: THUẬT TOÁN (Tiết 29)
bai15_md = """**TIẾT 29 - BÀI 15: THUẬT TOÁN**
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Diễn đạt được khái niệm thuật toán bằng ngôn ngữ tự nhiên: Thuật toán là một dãy các chỉ dẫn rõ ràng, có trình tự xác định sao cho khi thực hiện những chỉ dẫn này người ta giải quyết được vấn đề hoặc nhiệm vụ đã cho.
- Nêu được một vài ví dụ minh họa về thuật toán trong cuộc sống hàng ngày (thuật toán gấp hình trò chơi Đông-Tây-Nam-Bắc, quy trình làm kem, công thức nấu ăn, thuật toán tính toán học).
- Xác định được Đầu vào (Input - dữ liệu ban đầu) và Đầu ra (Output - kết quả nhận được) của một thuật toán.
- Biết rằng thuật toán có thể được mô tả bằng 2 cách chính: Liệt kê các bước bằng ngôn ngữ tự nhiên và Sử dụng sơ đồ khối (Flowchart).
- Nhận biết và vẽ đúng các hình khối quy ước trong sơ đồ khối: Hình oval (Bắt đầu/Kết thúc), Hình bình hành (Đầu vào/Đầu ra), Hình chữ nhật (Bước xử lí, tính toán), Hình thoi (Bước kiểm tra điều kiện), Mũi tên (Chỉ hướng thực hiện tiếp theo).

## 2. Về năng lực
### a) Năng lực chung
- **Năng lực tự chủ và tự học:** Tự giác nghiên cứu các bước gấp giấy trong SGK; chủ động suy nghĩ, phân tích các bước logic của một thuật toán tính toán quen thuộc.
- **Năng lực giao tiếp và hợp tác:** Làm việc nhóm để trao đổi, thảo luận về thứ tự các bước thực hiện và vẽ sơ đồ khối trên bảng nhóm.

### b) Năng lực Tin học
- **Năng lực C (Tư duy máy tính và giải quyết vấn đề):**
  + Rèn luyện tư duy thuật toán: biết chia một bài toán phức tạp thành các bước chỉ dẫn tuần tự, rõ ràng, không mập mờ.
  + Biết sử dụng sơ đồ khối để trực quan hóa quá trình giải quyết bài toán.

### c) Năng lực số (NLS)
- ***(Tích hợp NLS 3.1.TC1a: Sử dụng phần mềm số để sơ đồ hóa kiến thức thuật toán và trình bày sản phẩm học tập bài Thuật toán)***: Học sinh biết dùng công cụ vẽ hình khối (Shapes trong Word hoặc công cụ sơ đồ trực tuyến) để vẽ lại sơ đồ khối thuật toán và trình bày kết quả học tập.

### d) Năng lực Trí tuệ nhân tạo (AI)
- ***(Tích hợp AI 6.A1.1: Giải thích vai trò của con người khi thiết lập các bước thuật toán để điều khiển AI; học sinh đối chiếu các bước giải với SGK (Áp dụng: tiết 1, 2))***: Học sinh hiểu rằng mọi hệ thống AI thông minh thực chất đều hoạt động dựa trên các thuật toán do con người thiết kế và lập trình; con người giữ vai trò quyết định trong việc định hình logic thuật toán để điều khiển AI giải quyết bài toán chính xác.

## 3. Về phẩm chất
- **Chăm chỉ:** Kiên trì thực hành từng bước gấp giấy, cẩn thận vẽ đúng từng hình khối quy ước của sơ đồ khối.
- **Chính xác:** Rèn luyện thói quen tư duy mạch lạc, chính xác trong từng câu lệnh chỉ dẫn.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
## 1. Giáo viên
- Kế hoạch bài dạy, bài giảng trình chiếu PowerPoint.
- Giấy vuông màu cho học sinh thực hành gấp hình trò chơi Đông-Tây-Nam-Bắc.
- Hình ảnh minh họa trích xuất từ SGK: Hình 6.1 (Quy trình gấp hình), Hình 6.2 (Sơ đồ khối trò chơi Đông-Tây-Nam-Bắc).

## 2. Học sinh
- SGK Tin học 6 Kết nối tri thức (Trang 63 – 66), vở ghi bài, thước kẻ, bút màu.

---

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
### a) Mục tiêu
- Tạo không khí học tập sôi nổi thông qua trò chơi gấp giấy dân gian quen thuộc, từ đó dẫn dắt học sinh nhận thức được ý nghĩa của quy trình từng bước.
### b) Nội dung
- Học sinh quan sát Hình 6.1 trang 63 SGK và thực hiện gấp giấy theo hướng dẫn 6 bước.
### c) Sản phẩm
- Sản phẩm hình gấp trò chơi Đông-Tây-Nam-Bắc hoàn thành trên tay học sinh.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV phát cho mỗi học sinh 1 tờ giấy hình vuông màu rực rỡ.<br>- GV trình chiếu Hình 6.1 (trang 63 SGK) gồm 6 bước gấp hình trò chơi Đông-Tây-Nam-Bắc:<br>*1. Gấp hai đường chéo tạo nếp, mở ra.*<br>*2. Gấp bốn góc của tờ giấy vào tâm.*<br>*3. Lật mặt bên kia.*<br>*4. Tiếp tục gấp bốn góc vào tâm.*<br>*5. Đặt tờ giấy nằm ngang, luồn ngón tay vào bốn góc ở mặt dưới.*<br>*6. Chỉnh sửa các nếp gấp.*<br>- GV tổ chức thi đua: Ai gấp xong nhanh và đẹp nhất trong 2 phút! | - HS nhận giấy, háo hức quan sát các hình vẽ minh họa từ bước 1 đến bước 6 trong SGK. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS khẩn trương thực hiện gấp giấy theo đúng thứ tự chỉ dẫn.<br>- GV quan sát, khích lệ các học sinh thao tác khéo léo. | - Cả lớp tập trung gấp giấy, những bạn làm nhanh hỗ trợ bạn bên cạnh. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- Cả lớp cùng giơ cao sản phẩm trò chơi Đông-Tây-Nam-Bắc trên tay.<br>- GV đặt câu hỏi suy ngẫm Hoạt động 1 (trang 63 SGK):<br>1. *Nếu đảo thứ tự của bước 3 và bước 4 thì em có gấp được hình trò chơi không? Tại sao?*<br>2. *Trước khi thực hiện theo hướng dẫn, em cần có gì? Sau khi thực hiện xong 6 bước, em nhận được kết quả gì?* | - HS suy nghĩ và trả lời:<br>+ Nếu đảo bước 3 và bước 4 thì các nếp gấp bị sai hoàn toàn, không thể tạo ra được hình trò chơi.<br>+ Trước khi thực hiện cần có: *Tờ giấy hình vuông* (Đầu vào).<br>+ Sau khi thực hiện nhận được: *Hình gấp trò chơi Đông-Tây-Nam-Bắc* (Đầu ra). |
| **+ Bước 4: Kết luận, nhận định**<br>- GV nhận xét: Dãy 6 bước chỉ dẫn rõ ràng, có thứ tự tuần tự để biến tờ giấy hình vuông ban đầu thành đồ chơi hoàn chỉnh chính là một ví dụ sống động về **Thuật toán**. Bài học hôm nay sẽ giúp các em khám phá thế giới kỳ diệu của thuật toán: **Bài 15: Thuật toán**. | - HS mở vở ghi tên bài mới: **Bài 15: Thuật toán**. |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (25 phút)

### 1. Hoạt động 2.1: Khái niệm thuật toán (10 phút)
#### a) Mục tiêu
- Phát biểu được định nghĩa thuật toán; xác định được đầu vào (Input) và đầu ra (Output) của thuật toán; lấy được các ví dụ thuật toán trong cuộc sống.
- ***(Tích hợp AI 6.A1.1)***: Hiểu vai trò của con người trong việc thiết lập thuật toán điều khiển AI.
#### b) Nội dung
- Học sinh nghiên cứu mục 1 trang 63 – 64 SGK; trả lời 2 câu hỏi củng cố trang 64 SGK.
#### c) Sản phẩm
- Ghi nhớ màu cam trang 64 SGK; đáp án câu hỏi củng cố 1 và 2.
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV yêu cầu học sinh đọc thầm trang 64 SGK và trả lời các câu hỏi:<br>1. Thuật toán là gì?<br>2. Đầu vào (Input) và Đầu ra (Output) là gì?<br>3. Hãy nêu một số ví dụ về thuật toán trong đời sống hàng ngày?<br>- ***(Tích hợp AI 6.A1.1: GV đặt câu hỏi mở rộng: 'Các hệ thống Trí tuệ nhân tạo AI như xe tự lái, nhận diện khuôn mặt hay ChatGPT có tự nhiên thông minh không? Yếu tố nào giúp AI giải quyết được công việc? Con người đóng vai trò gì?').*** | - HS nghiên cứu SGK trang 64, suy nghĩ về các ví dụ trong thực tế như: công thức nấu ăn, quy trình đánh răng, cách pha trà, thuật toán giải phương trình trong Toán học. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS thảo luận theo cặp bàn trong 2 phút.<br>- ***(Tích hợp AI 6.A1.1: HS thảo luận về vai trò của con người: AI hoạt động dựa trên hàng triệu thuật toán do con người lập trình; con người thiết lập thuật toán, nạp dữ liệu và kiểm chứng kết quả; nếu thuật toán sai thì AI sẽ xử lí sai).*** | - HS ghi nhận định nghĩa thuật toán và liên hệ thực tế. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi đại diện học sinh phát biểu định nghĩa.<br>- Cả lớp giải quyết 2 câu hỏi củng cố (trang 64 SGK):<br>*Câu 1: Thuật toán là gì? (Chọn A, B, C hay D?)*<br>*Câu 2: Chọn các câu đúng về Đầu vào và Đầu ra.* | - HS trả lời:<br>+ Câu 1 chọn **C** (Một dãy các chỉ dẫn rõ ràng, có trình tự sao cho khi thực hiện ta giải quyết được vấn đề).<br>+ Câu 2 chọn **A và B** (Đầu vào là dữ liệu ban đầu, Đầu ra là kết quả nhận được sau khi thực hiện thuật toán). |
| **+ Bước 4: Kết luận, nhận định**<br>- GV tổng kết khung ghi nhớ màu cam trang 64 SGK.<br>- GV nhấn mạnh: Thuật toán phải có 3 đặc điểm sống còn: Tính xác định (rõ ràng, không mập mờ), Tính trình tự (đúng thứ tự) và Tính dừng (phải kết thúc cho ra kết quả). | - HS ghi bài vào vở. |

---

### 2. Hoạt động 2.2: Mô tả thuật toán bằng sơ đồ khối (15 phút)
#### a) Mục tiêu
- Nêu được 2 cách mô tả thuật toán (liệt kê bằng ngôn ngữ tự nhiên và sơ đồ khối).
- Nhận biết đúng 5 hình khối quy ước trong sơ đồ khối và vẽ được sơ đồ khối cho thuật toán đơn giản.
- ***(Tích hợp NLS 3.1.TC1a)***: Sử dụng phần mềm số để sơ đồ hóa thuật toán.
#### b) Nội dung
- Học sinh quan sát Hình 6.2 trang 65 SGK, nghiên cứu bảng quy ước hình khối và giải quyết bài tập nối cột trang 65.

![Sơ đồ khối mô tả thuật toán gấp hình trò chơi Đông-Tây-Nam-Bắc](khbd-ill:hinh-sodokhoi_dongtay_6_2)

#### c) Sản phẩm
- Bảng quy ước hình khối; sơ đồ khối Hình 6.2; đáp án bài tập nối cột trang 65 SGK.
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV chiếu Hình 6.2 và đặt câu hỏi Hoạt động 2 (trang 64 SGK): Ngoài cách liệt kê bằng lời văn, người ta còn mô tả thuật toán bằng cách nào? Cách đó có ưu điểm gì?<br>- GV giới thiệu 5 quy ước hình khối cơ bản (trang 65 SGK):<br>1. *Hình oval:* Bắt đầu hoặc Kết thúc.<br>2. *Hình bình hành:* Đầu vào (Input) hoặc Đầu ra (Output).<br>3. *Hình chữ nhật:* Bước xử lí, tính toán.<br>4. *Hình thoi:* Bước kiểm tra điều kiện (rẽ nhánh).<br>5. *Mũi tên:* Chỉ hướng thực hiện tiếp theo.<br>- Yêu cầu HS hoàn thành 2 câu hỏi củng cố trang 65 SGK. | - HS quan sát Hình 6.2 trên màn hình máy chiếu, theo dõi dòng chảy của mũi tên từ 'Bắt đầu' ➔ nạp giấy ➔ các bước gấp ➔ ra đồ chơi ➔ 'Kết thúc'. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS làm bài ghép nối vào vở.<br>- ***(Tích hợp NLS 3.1.TC1a: GV hướng dẫn HS sử dụng công cụ Insert ➔ Shapes trong phần mềm Word để vẽ các hình oval, hình chữ nhật và đường mũi tên nối các khối thuật toán trên máy tính).*** | - HS ghi nhớ hình dạng và ý nghĩa của từng khối:<br>+ Câu 1 củng cố: Chọn phương án **C** là câu sai (vì mũi tên không chỉ để kết nối mà còn chỉ rõ hướng đi của các bước).<br>+ Câu 2 củng cố (Ghép nối):<br>1) Hình oval ➔ a) Bắt đầu hoặc Kết thúc.<br>2) Hình bình hành ➔ c) Đầu vào hoặc Đầu ra.<br>3) Hình chữ nhật ➔ d) Bước xử lí.<br>4) Mũi tên ➔ b) Chỉ hướng thực hiện tiếp theo. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2 học sinh lên bảng vẽ nhanh các hình khối quy ước và nêu ý nghĩa.<br>- Cả lớp đối chiếu, nhận xét. | - HS tự tin vẽ đúng các hình khối chuẩn xác trên bảng lớp. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV chốt lại kiến thức khung màu cam trang 65 SGK: Sơ đồ khối là công cụ trực quan hóa thuật toán chuẩn quốc tế, giúp người lập trình dễ dàng quan sát cấu trúc và viết chương trình máy tính. | - HS hoàn thiện ghi chép vào vở học tập. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
### a) Mục tiêu
- Củng cố kỹ năng xác định Đầu vào, Đầu ra và thứ tự các khối trong sơ đồ khối qua 3 bài tập SGK trang 66.
### b) Nội dung
- Học sinh giải quyết Bài tập 1, 2, 3 trang 66 SGK.
### c) Sản phẩm
- Đáp án xác định Input/Output của thuật toán tính trung bình cộng và ƯCLN; Thứ tự sắp xếp các khối Hình 6.4.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV trình chiếu nội dung 3 bài tập Luyện tập (trang 66 SGK):<br>**Bài 1:** *Tìm đầu vào, đầu ra của:*<br>*a) Thuật toán tính trung bình cộng của hai số a, b.*<br>*b) Thuật toán tìm ƯCLN của hai số tự nhiên a và b.*<br>**Bài 2:** *Quan sát sơ đồ khối Hình 6.3: Cho biết sơ đồ mô tả thuật toán gì? Xác định đầu vào, đầu ra?*<br>**Bài 3:** *Sắp xếp các phần được đánh số 1 đến 6 trong Hình 6.4 để được sơ đồ khối tính trung bình cộng của 2 số a và b.* | - HS mở SGK trang 66, làm việc cá nhân vào vở trong 4 phút. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS suy nghĩ, vẽ sơ đồ và ghi đáp án.<br>- GV gợi ý Bài 3: Bắt đầu từ khối nào? Nạp giá trị a, b ở khối nào? Tính tổng trước hay tính TBC trước? | - HS phân tích logic các bước tính toán. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi 3 học sinh lên trình bày kết quả:<br>+ **Bài 1:**<br>  a) Đầu vào: Hai số a, b. Đầu ra: Giá trị trung bình cộng (a + b) / 2.<br>  b) Đầu vào: Hai số tự nhiên a, b. Đầu ra: Ước chung lớn nhất của a và b.<br>+ **Bài 2:** Sơ đồ khối Hình 6.3 mô tả thuật toán tính tổng hai số a và b. Đầu vào: Giá trị a, b. Đầu ra: Giá trị tổng.<br>+ **Bài 3:** Thứ tự sắp xếp đúng là: **1 (Bắt đầu) ➔ 3 (Giá trị a, giá trị b) ➔ 2 (Tổng <- a + b) ➔ 4 (Trung bình cộng <- Tổng : 2) ➔ 6 (Giá trị trung bình cộng) ➔ 5 (Kết thúc)**. | - Cả lớp chăm chú lắng nghe, đối chiếu với bài làm của mình và vỗ tay tán thành đáp án hoàn toàn chuẩn xác. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV chấm điểm khen ngợi các học sinh có tư duy thuật toán nhanh nhạy, rõ ràng. | - HS chữa bài cẩn thận vào vở. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
### a) Mục tiêu
- Vận dụng kiến thức thuật toán để mô tả một công việc thực tế quen thuộc bằng sơ đồ khối.
### b) Nội dung
- Học sinh làm Bài 1 phần Vận dụng trang 66 SGK: Xác định đầu vào, đầu ra và vẽ sơ đồ khối cho quy trình làm kem sữa chua xoài (Hình 6.5).
### c) Sản phẩm
- Sơ đồ khối mô tả thuật toán làm kem sữa chua xoài.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV giao nhiệm vụ Vận dụng 1 (trang 66 SGK):<br>a) Xác định đầu vào và đầu ra của thuật toán làm kem sữa chua xoài (Hình 6.5).<br>b) Hãy vẽ sơ đồ khối mô tả thuật toán này.<br>- Yêu cầu học sinh phác thảo nhanh các khối chính. | - HS đọc lại 7 bước làm kem ở Hình 6.5 trang 66 SGK. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS xác định nhanh:<br>+ Đầu vào: Xoài (250g), sữa chua (100g), mật ong (1 thìa cà phê), tô, khuôn kem, tủ lạnh.<br>+ Đầu ra: Món kem sữa chua xoài thơm ngon mát lạnh.<br>- HS vẽ sơ đồ khối gồm khối Bắt đầu ➔ Đầu vào ➔ 5 khối xử lí (cho xoài vào tô, nghiền nát, cho sữa chua mật ong, trộn đều, cho vào khuôn và để tủ lạnh 4 tiếng) ➔ Đầu ra (Lấy kem thưởng thức) ➔ Kết thúc. | - HS vẽ sơ đồ khối mạch lạc vào vở. |
| **+ Bước 3, 4: Kết luận & Dặn dò về nhà**<br>- GV đánh giá: Các em đã làm chủ được tư duy thuật toán, biết chuyển hóa mọi công việc đời sống thành quy trình khoa học.<br>- **Dặn dò về nhà:**<br>1. Ôn lại khái niệm thuật toán và các hình khối quy ước.<br>2. Vẽ lại sơ đồ khối làm kem sữa chua xoài thật đẹp vào vở.<br>3. Đọc trước **Bài 16: Các cấu trúc điều khiển (trang 67 SGK)**. | - HS ghi nhận dặn dò và kết thúc tiết học. |
"""

with open(os.path.join(temp_dir, "07_KHBD_Tin6_KiemTraGiuaHK2_Tiet28.md"), "w", encoding="utf-8") as f:
    f.write(bai07_md)

with open(os.path.join(temp_dir, "08_KHBD_Tin6_Bai15_ThuatToan_Tiet29.md"), "w", encoding="utf-8") as f:
    f.write(bai15_md)

print("Đã tạo Markdown cho Bài 07 (Kiểm tra giữa HK2) và Bài 08 (Bài 15 Thuật toán)!")
