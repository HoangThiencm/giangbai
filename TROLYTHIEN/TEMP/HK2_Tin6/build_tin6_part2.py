# -*- coding: utf-8 -*-
"""
Script xây dựng toàn bộ nội dung Markdown chi tiết cho các bài 05 -> 12 của Tin học 6 HK2
Bám sát 100% nội dung SGK và Phụ lục 3 của Thầy Hoàng Tấn Thiên.
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Tin6"
os.makedirs(temp_dir, exist_ok=True)

# 05. BÀI 13: THỰC HÀNH TÌM KIẾM VÀ THAY THẾ (Tiết 26)
bai13_md = """**TIẾT 26 - BÀI 13: THỰC HÀNH: TÌM KIẾM VÀ THAY THẾ**
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Trình bày được mục đích và tác dụng to lớn của công cụ Tìm kiếm (Find) và Thay thế (Replace) trong phần mềm soạn thảo văn bản: giúp tìm kiếm nhanh, định vị chính xác vị trí từ/cụm từ cần tìm và tự động thay thế hàng loạt mà không bỏ sót, tiết kiệm tối đa thời gian và công sức, đặc biệt với những tài liệu dài hàng chục, hàng trăm trang.
- Sử dụng thành thạo công cụ Tìm kiếm (phím tắt Ctrl+F) để duyệt qua các từ tìm thấy trên thanh điều hướng Navigation.
- Sử dụng thành thạo hộp thoại Find and Replace (phím tắt Ctrl+H) để thay thế lần lượt từng từ (Replace) hoặc thay thế toàn bộ (Replace All) trong văn bản.
- Áp dụng vào chỉnh sửa tệp công thức làm kem: chuyển đổi công thức 'kem sữa chua dưa hấu' thành 'kem sữa chua xoài' và rà soát lỗi chính tả trong sổ lưu niệm.

## 2. Về năng lực
### a) Năng lực chung
- **Năng lực tự chủ và tự học:** Tự giác mở tệp văn bản mẫu trên máy tính; chủ động thực hiện từng bước thao tác tìm kiếm và thay thế theo hướng dẫn trong SGK; tự kiểm tra lại kết quả thay thế.
- **Năng lực giao tiếp và hợp tác:** Trao đổi cặp đôi để cùng tìm ra các từ viết tắt, lỗi chính tả thường gặp trong bài viết và phối hợp sửa lỗi nhanh chóng.

### b) Năng lực Tin học
- **Năng lực C (Ứng dụng công nghệ thông tin và truyền thông):** Sử dụng các công cụ tự động hóa của phần mềm soạn thảo văn bản để nâng cao năng suất và độ chính xác khi biên tập tài liệu số.

## 3. Về phẩm chất
- **Chăm chỉ:** Kiên trì luyện tập các thao tác tìm kiếm, kiểm tra cẩn thận từng từ được thay thế để tránh thay nhầm ngữ cảnh.
- **Trách nhiệm:** Có ý thức cẩn trọng khi sử dụng lệnh Replace All, luôn đọc kỹ nội dung trước khi quyết định thay thế hàng loạt.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
## 1. Giáo viên
- Kế hoạch bài dạy, máy chiếu, bài giảng trình chiếu.
- Phòng máy tính có cài đặt Microsoft Word và có sẵn tệp mẫu `kemsuachua-duahau.docx` trên máy học sinh.
## 2. Học sinh
- SGK Tin học 6 Kết nối tri thức (Trang 58 – 60), vở ghi bài.

---

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
### a) Mục tiêu
- Gợi mở tình huống thực tế cần thay đổi đồng loạt một từ/cụm từ trong tài liệu, giúp học sinh nhận thức được sự bất tiện khi làm thủ công bằng mắt và nhu cầu sử dụng công cụ tự động.
### b) Nội dung
- Học sinh đọc tình huống mở đầu trang 58 SGK về công thức làm kem sữa chua dưa hấu của bạn An và nhu cầu đổi sang kem sữa chua xoài của bạn Minh.
### c) Sản phẩm
- Câu trả lời của học sinh về cách thức chỉnh sửa công thức nhanh nhất.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV chiếu tình huống mở đầu trang 58 SGK:<br>*An đã học được cách làm kem sữa chua dưa hấu rất ngon và dùng Word để lưu lại công thức. Minh xin An công thức làm kem nhưng muốn đổi thành món kem sữa chua xoài.*<br>- GV đặt câu hỏi Hoạt động 1:<br>1. Từ công thức dưa hấu, muốn thành công thức xoài em làm thế nào?<br>2. Trong Word, em dùng thao tác nào để giúp An chỉnh sửa?<br>3. Em có biết cách nào chỉnh sửa nhanh hơn việc ngồi đọc từng dòng rồi xóa đi gõ lại không? | - HS đọc tình huống trong SGK, quan sát công thức làm kem.<br>- Cả lớp suy nghĩ cách đổi từ 'dưa hấu' thành từ 'xoài'. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS suy nghĩ cá nhân trong 1 phút.<br>- GV gợi ý: Trong công thức có bao nhiêu từ 'dưa hấu'? Nếu tài liệu dài 50 trang có 100 chữ 'dưa hấu' thì đọc bằng mắt liệu có sót không? | - HS trao đổi: Đọc bằng mắt rất lâu, mỏi mắt và dễ bị sót chữ; cần có công cụ máy tính tìm và đổi tự động. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV mời 2 học sinh phát biểu ý kiến.<br>- Cả lớp lắng nghe, tán thành sự cần thiết của công cụ tìm kiếm tự động. | - HS phát biểu: *"Thưa thầy, cần dùng chức năng Tìm kiếm và Thay thế của Word để máy tự tìm và tự sửa hết các chữ dưa hấu thành xoài."* |
| **+ Bước 4: Kết luận, nhận định**<br>- GV nhận xét, chốt lại: Chức năng Tìm kiếm và Thay thế (Find and Replace) chính là trợ thủ đắc lực giúp giải quyết bài toán này trong nháy mắt. Bài học hôm nay sẽ giúp các em làm chủ công cụ này qua: **Bài 13: Thực hành: Tìm kiếm và thay thế**. | - HS mở vở ghi tên bài mới. |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI & THỰC HÀNH (25 phút)

### 1. Hoạt động 2.1: Tìm hiểu tác dụng của công cụ Tìm kiếm và Thay thế (8 phút)
#### a) Mục tiêu
- Trình bày được mục đích và lợi ích vượt trội của công cụ Find and Replace.
#### b) Nội dung
- Học sinh nghiên cứu mục 1 trang 58 – 59 SGK, phân tích các trường hợp nên dùng công cụ.
#### c) Sản phẩm
- Ghi nhớ màu cam trang 59 SGK: *Công cụ Tìm kiếm và Thay thế giúp tìm kiếm, thay thế từ hoặc cụm từ theo yêu cầu một cách nhanh chóng và chính xác.*
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV yêu cầu học sinh đọc thầm phần 1 trang 58 SGK.<br>- GV đặt câu hỏi: Khi nào chúng ta nên sử dụng công cụ Tìm kiếm? Khi nào sử dụng công cụ Thay thế? Công cụ này mang lại lợi ích gì so với làm thủ công? | - HS mở SGK trang 58, đọc đoạn phân tích về nhu cầu tìm và thay thế trong văn bản dài. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS trao đổi cặp đôi, gạch chân các từ khóa quan trọng: nhanh chóng, chính xác, tiết kiệm thời gian, không bỏ sót. | - HS nắm vững: Dùng khi cần tra cứu thông tin trong văn bản dài, sửa lỗi chính tả lặp lại nhiều lần, hoặc cập nhật số liệu mới. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2 học sinh phát biểu trước lớp. | - HS trả lời rõ ràng các lợi ích của công cụ. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV chuẩn hóa kiến thức bằng khung ghi nhớ trang 59 SGK: Công cụ Find and Replace giúp xử lí văn bản tự động, chuyên nghiệp và chính xác tuyệt đối. | - HS ghi bài vào vở. |

---

### 2. Hoạt động 2.2: Thực hành sử dụng công cụ Tìm kiếm và Thay thế (17 phút)
#### a) Mục tiêu
- Thực hiện thuần thục 3 bước tìm kiếm và 4 bước thay thế trên phần mềm Word.
- Đổi thành công tệp `kemsuachua-duahau.docx` thành `kemsuachua-xoai.docx`.
#### b) Nội dung
- Học sinh theo dõi GV hướng dẫn thao tác trên máy chiếu (Hình 5.23 và Hình 5.24 trang 59 – 60 SGK), sau đó thực hành trên máy tính cá nhân.
#### c) Sản phẩm
- Tệp văn bản `kemsuachua-xoai.docx` đã được thay thế toàn bộ từ 'dưa hấu' thành 'xoài'.
#### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV thị phạm trên máy chiếu:<br>+ **Thao tác Tìm kiếm (3 bước):** 1. Vào Home ➔ nhóm Editing chọn Find (hoặc bấm Ctrl+F); 2. Gõ cụm từ cần tìm (ví dụ: `dưa hấu`) vào ô tìm kiếm; 3. Nhấn Enter, các từ tìm thấy được bôi màu vàng trong văn bản và liệt kê ở bảng Navigation bên trái.<br>+ **Thao tác Thay thế (4 bước):** 1. Vào Home ➔ nhóm Editing chọn Replace (hoặc bấm Ctrl+H); 2. Trong ô *Find what*, gõ từ cần tìm: `dưa hấu`; 3. Trong ô *Replace with*, gõ từ thay thế: `xoài`; 4. Nhấn *Replace* để thay thế từng từ một, hoặc nhấn *Replace All* để thay thế toàn bộ trong tích tắc.<br>- GV giao nhiệm vụ cho học sinh thực hành trên máy tính. | - HS quan sát thao tác mẫu của GV, ghi nhớ tổ hợp phím tắt Ctrl+F (Find) và Ctrl+H (Replace).<br>- HS mở tệp `kemsuachua-duahau.docx` trên máy tính của mình. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS mở tệp và thực hành lần lượt:<br>1. Dùng lệnh Find tìm từ 'dưa hấu', đếm số lượng từ xuất hiện trong bài.<br>2. Dùng lệnh Replace thay thế từng từ để quan sát sự biến đổi.<br>3. Dùng lệnh Replace All để thay thế tất cả.<br>4. Lưu tệp với tên `kemsuachua-xoai.docx`.<br>- GV bao quát, hướng dẫn học sinh phân biệt khi nào nên bấm Replace (thay có chọn lọc) và khi nào bấm Replace All (thay hàng loạt). | - HS thực hành nghiêm túc, hào hứng thấy 4 từ 'dưa hấu' trong công thức lập tức chuyển thành 'xoài'.<br>- HS kiểm tra lại dòng tiêu đề: *Kem sữa chua xoài*, nguyên liệu: *Xoài: 250 g*, cách làm: *Cho xoài vào tô; Nghiền nát xoài*.<br>- HS lưu tệp thành công. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV kiểm tra bài làm của 3 học sinh trên màn hình trung tâm.<br>- Cả lớp đối chiếu kết quả, xác nhận công thức đã được chuyển đổi hoàn toàn chính xác. | - HS theo dõi bài của bạn, tự tin đã nắm chắc thao tác. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV biểu dương tinh thần thực hành của cả lớp. Lưu ý học sinh: Khi dùng Replace All cần kiểm tra kỹ từ thay thế có bị trùng với các từ khác không (ví dụ thay 'ba' thành 'bố' có thể làm từ 'bà ba' biến thành 'bà bố'). | - HS lắng nghe lưu ý cẩn trọng của giáo viên. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
### a) Mục tiêu
- Củng cố kỹ năng tìm kiếm và thứ tự các bước thay thế thông qua 2 bài tập SGK trang 60.
### b) Nội dung
- Học sinh làm việc cá nhân giải quyết Bài tập 1 và Bài tập 2 trang 60 SGK.
### c) Sản phẩm
- Câu trả lời Bài 1 về cách xem lần lượt kết quả tìm kiếm; thứ tự đúng của các bước thay thế ở Bài 2.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV trình chiếu 2 bài tập phần Luyện tập (trang 60 SGK):<br>**Bài 1:** *Tệp văn bản chứa các bài viết cảm nghĩ của An gồm nhiều trang. An muốn tìm cụm từ 'nhóm bạn thân' nhưng không nhớ rõ ở trang nào. An phải thực hiện thao tác gì để xem lần lượt các kết quả tìm thấy?*<br>**Bài 2:** *Sắp xếp các bước theo thứ tự đúng để thực hiện thay thế một từ hoặc cụm từ:*<br>*a) Gõ từ, cụm từ cần thay thế.*<br>*b) Nháy chuột vào thẻ Home.*<br>*c) Trong nhóm lệnh Editing, chọn Replace.*<br>*d) Gõ từ, cụm từ cần tìm.*<br>*e) Nháy chuột vào nút Replace để thay thế lần lượt từng từ hoặc cụm từ.* | - HS đọc kỹ yêu cầu trong SGK trang 60 và suy nghĩ câu trả lời. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS làm bài vào vở trong 3 phút.<br>- GV bao quát lớp, khích lệ học sinh phát biểu. | - HS ghi đáp án vào vở. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2 học sinh trả lời:<br>+ Bài 1: An chỉ cần nháy chuột vào từng kết quả trong bảng Navigation bên trái, hoặc bấm phím Enter / nút mũi tên lên xuống để di chuyển lần lượt đến từng vị trí.<br>+ Bài 2: Thứ tự các bước đúng là **b ➔ c ➔ d ➔ a ➔ e**. | - Cả lớp nhận xét, đối chiếu đáp án với bài làm của mình. |
| **+ Bước 4: Kết luận, nhận định**<br>- GV chuẩn hóa đáp án, chấm điểm tuyên dương học sinh trả lời xuất sắc. | - HS chữa bài vào vở. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
### a) Mục tiêu
- Vận dụng công cụ Tìm kiếm và Thay thế để rà soát lỗi chính tả, chuẩn hóa các từ viết tắt trong toàn bộ các tệp văn bản của cuốn sổ lưu niệm lớp.
### b) Nội dung
- Học sinh mở tệp cảm nghĩ hoặc danh sách lớp đã tạo ở các bài trước, dùng Ctrl+H để tìm và sửa các từ viết tắt (vd: 'ko' thành 'không', 'dc' thành 'được').
### c) Sản phẩm
- Tệp văn bản cảm nghĩ đã được làm sạch hoàn toàn các lỗi viết tắt và lỗi chính tả.
### d) Tổ chức thực hiện

| Hoạt động của Giáo viên | Hoạt động của Học sinh |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- GV nêu yêu cầu phần Vận dụng (trang 60 SGK): Mở tệp `CamNghiVeBan.docx`, dùng chức năng Replace để tìm các từ viết tắt teen-code và thay thế bằng từ tiếng Việt chuẩn mực. | - HS mở tệp bài viết cảm nghĩ trên máy tính. |
| **+ Bước 2: Thực hiện nhiệm vụ**<br>- HS bấm Ctrl+H, gõ tìm và thay thế các từ viết tắt. | - HS kiểm tra văn bản, thấy bài viết trở nên trang trọng, chỉn chu. |
| **+ Bước 3: Báo cáo, thảo luận**<br>- GV kiểm tra nhanh sản phẩm của một số học sinh. | - HS hào hứng thấy văn bản được sửa lỗi toàn diện trong vài giây. |
| **+ Bước 4: Kết luận, nhận định & Dặn dò về nhà**<br>- GV dặn dò: Chuẩn bị đầy đủ tất cả các tệp bài viết cảm nghĩ, danh sách lớp, sơ đồ tư duy để tuần sau bước vào tiết **Bài 14: Thực hành tổng hợp: Hoàn thiện sổ lưu niệm**. | - HS lưu bài, tắt máy và ghi chép nhiệm vụ về nhà. |
"""

with open(os.path.join(temp_dir, "05_KHBD_Tin6_Bai13_ThucHanhTimKiemVaThayThe_Tiet26.md"), "w", encoding="utf-8") as f:
    f.write(bai13_md)

print("Đã tạo Markdown cho Bài 13!")
