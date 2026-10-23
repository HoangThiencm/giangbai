Tiết 5, 6 - BÀI 3: THÔNG TIN TRONG MÁY TÍNH
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Giải thích được việc có thể biểu diễn thông tin (số, văn bản, hình ảnh, âm thanh) chỉ với hai kí hiệu 0 và 1.
- Biết được bit là đơn vị nhỏ nhất trong lưu trữ thông tin.
- Nêu được tên và độ lớn của các đơn vị cơ bản đo dung lượng thông tin: Byte (B), Kilobyte (KB), Megabyte (MB), Gigabyte (GB), Terabyte (TB).
- Ước lượng được khả năng lưu trữ của các thiết bị nhớ thông dụng (RAM, thẻ nhớ, USB, đĩa CD/DVD, ổ đĩa cứng).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự nghiên cứu SGK, thực hiện quy trình thu gọn dãy số để tìm mã hóa nhị phân của các số; chủ động thực hành tính toán dung lượng tệp và ổ đĩa.
- Giao tiếp và hợp tác: Tích cực thảo luận nhóm, phân công nhiệm vụ hoàn thành bảng mã hóa và chia sẻ cách biểu diễn dữ liệu chữ, hình ảnh, âm thanh.

b) Năng lực Tin học:
- NLa (Sử dụng và quản lý các phương tiện công nghệ thông tin và truyền thông): Nhận biết được đơn vị đo dung lượng thông tin, ước lượng và lựa chọn được thiết bị lưu trữ phù hợp với nhu cầu sử dụng thực tế.
- NLc (Tư duy giải quyết vấn đề với sự trợ giúp của máy tính): Hiểu được nguyên lý nhị phân hóa (mã hóa dữ liệu thành các dãy bit 0 và 1) để máy tính có thể tiếp nhận, xử lý và lưu trữ thông tin đa phương tiện.

## 3. Về phẩm chất
- Chăm chỉ: Kiên trì thực hiện các bài toán quy đổi dung lượng và các bước mã hóa nhị phân.
- Trách nhiệm: Có ý thức sử dụng thiết bị nhớ cẩn thận, tiết kiệm không gian lưu trữ và sắp xếp dữ liệu khoa học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng điện tử trình chiếu, máy tính kết nối Internet, máy chiếu/Tivi, phiếu học tập số 1 (Mã hóa số & văn bản), phiếu học tập số 2 (Mã hóa hình ảnh trái tim & âm thanh), phiếu học tập số 3 (Đổi đơn vị đo dung lượng), thiết bị lưu trữ vật lý thực tế để quan sát (thẻ nhớ MicroSD, USB, đĩa CD, ổ cứng di động).
2. Học sinh: Sách giáo khoa Tin học 6 (Kết nối tri thức với cuộc sống), vở ghi, bút, thước kẻ, đọc trước nội dung bài 3.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)
a) Mục tiêu: Kích hoạt sự tò mò của học sinh về cách thức máy tính lưu trữ và hiểu được ngôn ngữ con người; tạo cầu nối từ kiến thức "Xử lí thông tin" sang "Biểu diễn thông tin".
b) Nội dung: Trò chơi "Truyền tin bí mật bằng hai trạng thái (Bật/Tắt đèn pin)". Đặt vấn đề: Con người dùng hàng nghìn từ ngữ, chữ cái, nốt nhạc, màu sắc... nhưng tại sao máy tính hiện đại lại chỉ làm việc với hai kí hiệu 0 và 1?
c) Sản phẩm: Câu trả lời và dự đoán của học sinh về cơ chế làm việc của máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tổ chức trò chơi nhỏ "Mật mã 2 trạng thái":<br>+ GV chuẩn bị một bóng đèn pin (hoặc bật/tắt đèn flash điện thoại). Quy ước: Đèn Sáng tương ứng với kí hiệu 1, Đèn Tắt tương ứng với kí hiệu 0.<br>+ GV đặt câu hỏi: "Nếu chỉ dùng hai trạng thái Bật (1) và Tắt (0), làm thế nào để chúng ta có thể truyền đi các thông điệp khác nhau cho người ở xa?"<br>+ Đặt vấn đề tiếp: "Con người sử dụng các chữ số (0, 1, 2, ..., 9), bảng chữ cái (A, B, C...), các dấu câu, âm thanh lời nói và màu sắc hình ảnh để tư duy và trao đổi. Nhưng bên trong máy tính chỉ là các mạch điện tử, làm thế nào máy tính có thể hiểu, xử lý và lưu trữ được mọi dữ liệu của con người?"<br>- **HS:** Lắng nghe luật chơi, suy nghĩ và sẵn sàng tham gia.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi nhanh trong 2 phút để tìm cách quy ước các chữ cái hoặc thông điệp qua các lần bật/tắt đèn.<br>- **GV:** Quan sát, gợi ý học sinh liên tưởng đến mã Morse hoặc các tín hiệu nhấp nháy của đèn hải đăng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện 2 học sinh chia sẻ ý tưởng.<br>- **HS:** Đại diện trả lời: Có thể ghép nhiều lần bật/tắt liên tiếp thành một dãy để quy ước cho từng chữ cái hoặc con số.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi câu trả lời sáng tạo của học sinh. Chốt lại: Bản chất bên trong máy tính chỉ gồm các mạch điện tử với hai trạng thái cơ bản là Có điện (đóng mạch, tương ứng với 1) và Không có điện (ngắt mạch, tương ứng với 0). Để máy tính hiểu được thông tin của con người, mọi thông tin (số, chữ, hình ảnh, âm thanh) đều phải được chuyển đổi thành các dãy kí hiệu 0 và 1. Bài học hôm nay sẽ giúp các em khám phá bí mật kỳ diệu này! | **Khởi động: Đặt vấn đề về biểu diễn thông tin**<br>- Con người: Giao tiếp bằng chữ cái, chữ số, hình ảnh, âm thanh tự nhiên phong phú.<br>- Máy tính: Là thiết bị điện tử, chỉ xử lý được các tín hiệu điện với 2 trạng thái cơ bản: Đóng (Có điện - kí hiệu 1) và Ngắt (Không có điện - kí hiệu 0).<br>- Vấn đề cốt lõi: Làm thế nào để chuyển đổi mọi dạng thông tin tự nhiên thành các dãy gồm hai kí hiệu 0 và 1? |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (50 phút)

### 1. Hoạt động 2.1: Biểu diễn thông tin trong máy tính (25 phút)
a) Mục tiêu:
- Giải thích được việc biểu diễn số, văn bản, hình ảnh, âm thanh thành dãy bit 0 và 1.
- Hiểu khái niệm bit và bit là đơn vị nhỏ nhất trong lưu trữ thông tin.
b) Nội dung:
- Khám phá Hoạt động 1 SGK trang 12 (Hình 1.3: Cách mã hoá số 4).
![Hình 1.3. Cách mã hoá số 4](khbd-ill:hinh_1_3_ma_hoa_so_4)
- Thực hiện mã hóa số 3 và số 6.
- Khám phá biểu diễn văn bản (Bảng 1.2: Kí tự & Dãy bit; từ CAFE).
- Khám phá biểu diễn hình ảnh (Điểm ảnh - pixel; Hình 1.4: Biểu diễn chữ A; Hoạt động 2: Hình 1.6: Hình trái tim 8x8).
![Hình 1.4. Một cách biểu diễn hình ảnh chữ A thành dãy bit](khbd-ill:hinh_1_4_bieu_dien_chu_A)
![Hình 1.6. Hình trái tim 8x8](khbd-ill:hinh_1_6_trai_tim)
- Khám phá biểu diễn âm thanh (Hình 1.5: Biểu diễn âm thanh nốt La).
![Hình 1.5. Biểu diễn âm thanh nốt La thành dãy bit](khbd-ill:hinh_1_5_am_thanh_not_la)
- Trả lời 2 câu hỏi củng cố trang 14 SGK (Dãy bit là gì? Máy tính sử dụng dãy bit để làm gì?).
c) Sản phẩm: Bảng kết quả mã hóa các số 0-7, dãy bit của từ CAFE, dãy bit chữ A, dãy bit hình trái tim, đáp án câu hỏi củng cố.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Hình 1.3 SGK trang 12, giới thiệu Hoạt động 1 (Mã hoá): Cho dãy số từ 0 đến 7 viết theo thứ tự tăng dần.<br>- **GV:** Hướng dẫn cách mã hoá số 4 bằng phương pháp chia đôi liên tiếp:<br>+ Lần 1: Chia đôi dãy 0..7 thành nửa trái (0, 1, 2, 3) và nửa phải (4, 5, 6, 7). Số 4 nằm ở nửa phải $\rightarrow$ ghi "phải". Bỏ nửa trái, giữ nửa phải.<br>+ Lần 2: Chia đôi dãy 4..7 thành nửa trái (4, 5) và nửa phải (6, 7). Số 4 nằm ở nửa trái $\rightarrow$ ghi "trái". Bỏ nửa phải, giữ nửa trái.<br>+ Lần 3: Chia đôi dãy 4..5 thành nửa trái (4) và nửa phải (5). Số 4 nằm ở nửa trái $\rightarrow$ ghi "trái".<br>+ Quy tắc: "trái" $\rightarrow$ 0, "phải" $\rightarrow$ 1. Kết quả thu được: phải, trái, trái $\rightarrow$ dãy bit 100.<br>- **GV:** Yêu cầu các nhóm hoàn thành câu hỏi 2 trong Hoạt động 1: Mã hóa số 3 và số 6.<br>- **GV:** Giới thiệu tiếp các nội dung biểu diễn đa phương tiện:<br>+ Biểu diễn văn bản: Mỗi kí tự được gán một dãy bit cố định (Bảng 1.2). Yêu cầu HS viết dãy bit cho từ "CAFE".<br>+ Biểu diễn hình ảnh: Chiếu Hình 1.4, giải thích khái niệm pixel (điểm ảnh). Trong ảnh đen trắng, điểm đen là 1, điểm trắng là 0. Yêu cầu làm Hoạt động 2 (Hình 1.6 - Trái tim).<br>+ Biểu diễn âm thanh: Chiếu Hình 1.5, giải thích tần số rung (nốt La 440 Hz $\rightarrow$ 110111000).<br>- **HS:** Nhận phiếu học tập số 1 và số 2, sẵn sàng làm việc nhóm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc theo nhóm 4 em: Thực hiện chia đôi dãy số mã hóa số 3 và số 6; tra bảng ghép dãy bit cho từ CAFE; đếm ô đen/trắng viết dãy bit cho hình trái tim.<br>- **GV:** Đi vòng quanh lớp, quan sát, hướng dẫn các nhóm gặp lúng túng trong bước chia đôi dãy số và cách ghi bit theo thứ tự trên xuống dưới của hình trái tim.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện Nhóm 1 trình bày cách mã hóa số 3 và 6.<br>- **HS Nhóm 1:** Trình bày:<br>+ Số 3: Nửa trái (0..3) $\rightarrow$ ghi trái; Nửa phải (2, 3) $\rightarrow$ ghi phải; Nửa phải (3) $\rightarrow$ ghi phải. Kết quả: 011.<br>+ Số 6: Nửa phải (4..7) $\rightarrow$ ghi phải; Nửa phải (6, 7) $\rightarrow$ ghi phải; Nửa trái (6) $\rightarrow$ ghi trái. Kết quả: 110.<br>+ Hai dãy bit này hoàn toàn khác nhau.<br>- **GV:** Mời đại diện Nhóm 2 đọc dãy bit từ CAFE: 01000011 01000001 01000110 01000101.<br>- **GV:** Mời đại diện Nhóm 3 đọc dãy bit từng dòng của Hình 1.6 (Trái tim).<br>- **GV:** Cho cả lớp làm nhanh 2 câu hỏi củng cố trang 14.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại kiến thức trọng tâm:<br>1) Thông tin trong máy tính (số, văn bản, hình ảnh, âm thanh) đều được chuyển đổi thành dãy bit.<br>2) Mỗi bit là một kí hiệu 0 hoặc 1 (chữ số nhị phân).<br>3) Bit là đơn vị nhỏ nhất trong lưu trữ thông tin. | **1. Biểu diễn thông tin trong máy tính**<br><br>**a) Biểu diễn số:**<br>- Bằng cách chia đôi liên tiếp dãy số từ 0 đến 7, mỗi số từ 0 đến 7 được mã hóa thành dãy gồm 3 bit:<br>+ Số 0: 000  —  Số 1: 001<br>+ Số 2: 010  —  Số 3: 011<br>+ Số 4: 100  —  Số 5: 101<br>+ Số 6: 110  —  Số 7: 111<br>- Mỗi kí hiệu 0 hoặc 1 gọi là một **bit** (viết tắt từ Binary digIT - chữ số nhị phân).<br><br>**b) Biểu diễn văn bản:**<br>- Văn bản gồm các kí tự (chữ hoa, chữ thường, chữ số, dấu câu, kí hiệu...).<br>- Mỗi kí tự được gán một dãy bit tương ứng theo một bảng mã chuẩn.<br>- Ví dụ từ **CAFE**:<br>+ C: 01000011<br>+ A: 01000001<br>+ F: 01000110<br>+ E: 01000101<br>$\rightarrow$ Từ CAFE được biểu diễn thành: 01000011 01000001 01000110 01000101.<br><br>**c) Biểu diễn hình ảnh:**<br>- Hình ảnh số được tạo thành từ các điểm ảnh (**pixel**).<br>- Trong ảnh đen trắng đơn giản: Mỗi pixel được biểu thị bằng 1 bit (đen = 1, trắng = 0).<br>- Dãy bit của hình ảnh là sự kết hợp tuần tự dãy bit của từng dòng quét từ trên xuống dưới.<br><br>**d) Biểu diễn âm thanh:**<br>- Âm thanh phát ra nhờ dao động. Tốc độ rung (tần số) được ghi lại dưới dạng số trị, sau đó số trị được chuyển đổi thành dãy bit (Ví dụ nốt La 440 Hz $\rightarrow$ dãy bit 110111000).<br><br>**e) Ghi nhớ cốt lõi:**<br>- Mọi thông tin trong máy tính đều được biểu diễn bằng dãy các bit.<br>- Bit là đơn vị đo nhỏ nhất trong lưu trữ thông tin.<br><br>**f) Đáp án câu hỏi củng cố (SGK trang 14):**<br>- Câu 1: **Đáp án A** (Là dãy những kí hiệu 0 và 1).<br>- Câu 2: **Đáp án D** (Biểu diễn số, văn bản, hình ảnh, âm thanh). |

### 2. Hoạt động 2.2: Đơn vị đo thông tin (25 phút)
a) Mục tiêu:
- Biết được Byte là gì (1 Byte = 8 bit).
- Nêu được tên, kí hiệu, độ lớn và giá trị xấp xỉ của các đơn vị đo dung lượng thông tin: B, KB, MB, GB, TB.
- Ước lượng và đọc được dung lượng lưu trữ của các thiết bị nhớ thông dụng (RAM, CD/DVD, USB, ổ đĩa cứng...).
b) Nội dung:
- Tìm hiểu đơn vị Byte (1 Byte biểu diễn một kí tự).
- Bảng 1.3 SGK: Tên gọi, cách đọc, kí hiệu, giá trị theo lũy thừa 2 và giá trị xấp xỉ hệ thập phân.
- Đọc dung lượng ổ đĩa từ Hình Devices and drives:
![Hình minh họa dung lượng ổ đĩa](khbd-ill:hinh_devices_drives)
- Đọc dung lượng tệp từ Hình danh sách tệp ảnh:
![Hình minh họa dung lượng tệp ảnh](khbd-ill:hinh_file_size_list)
- Khảo sát dung lượng các thiết bị nhớ thực tế: RAM (2 GB - 16 GB), Đĩa CD (~700 MB), Đĩa DVD (~4.7 GB - 17 GB), Thẻ nhớ (vài GB đến hàng trăm GB), Ổ cứng (vài trăm GB đến vài TB).
c) Sản phẩm: Bảng đơn vị đo dung lượng đã hoàn thiện trong vở HS, kết quả đọc thông số dung lượng ổ đĩa và tệp ảnh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt vấn đề: "Vì 1 bit chỉ lưu được 1 chữ số 0 hoặc 1 (rất nhỏ), nên người ta gom 8 bit liên tiếp lại thành một đơn vị gọi là **Byte** (đọc là Bai, kí hiệu là B). 1 Byte đủ để lưu trữ một kí tự (chữ cái hoặc chữ số). Tuy nhiên, một cuốn sách hay một bài hát có hàng triệu kí tự, nếu chỉ dùng Byte thì số ghi sẽ rất dài. Do đó, người ta quy định các đơn vị lớn hơn."<br>- **GV:** Trình chiếu Bảng 1.3 SGK trang 14 (Các đơn vị cơ bản đo dung lượng thông tin): Byte, Kilobyte (KB), Megabyte (MB), Gigabyte (GB), Terabyte (TB).<br>- **GV:** Hướng dẫn quy tắc đổi: Mỗi đơn vị kế tiếp gấp 1024 lần đơn vị liền trước ($1024 = 2^{10}$), và xấp xỉ 1000 lần ($10^3$).<br>- **GV:** Chiếu hình minh họa 1 (Devices and drives) và hình minh họa 2 (File size) trang 15. Yêu cầu HS trả lời:<br>1) Đọc dung lượng còn trống và tổng dung lượng của ổ đĩa C:, E:, F:, G:.<br>2) Đọc dung lượng của các tệp ảnh IMG_0013.jpg, IMG_0038.jpg, IMG_0039.jpg.<br>- **GV:** Cho HS quan sát các thiết bị nhớ vật lý mang theo (thẻ nhớ MicroSD 32GB, USB 16GB, đĩa CD 700MB, ổ cứng di động 1TB) và giới thiệu dung lượng thông dụng.<br>- **HS:** Chú ý lắng nghe, quan sát bảng và hình ảnh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cá nhân đọc thông tin SGK, ghi nhớ tên và kí hiệu các đơn vị đo; làm việc cặp đôi để đọc thông số ổ đĩa và tệp ảnh.<br>- **GV:** Theo dõi, hướng dẫn học sinh cách phân biệt dung lượng còn trống (free) và tổng dung lượng (total) trên giao diện hệ điều hành Windows.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Gọi đại diện HS đọc thông số ổ đĩa:<br>+ Ổ C: Còn trống 37.9 GB trên tổng số 109 GB.<br>+ Ổ E: Còn trống 48.2 GB trên tổng số 111 GB.<br>+ Ổ F: Còn trống 153 GB trên tổng số 169 GB.<br>+ Ổ DATA2 (G:): Còn trống 27.2 GB trên tổng số 186 GB.<br>- **GV:** Gọi đại diện HS đọc dung lượng tệp ảnh:<br>+ IMG_0013.jpg: 372 KB.<br>+ IMG_0038.jpg: 1,095 KB (xấp xỉ hơn 1 MB).<br>+ IMG_0039.jpg: 1,100 KB (xấp xỉ 1.1 MB).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kết quả làm việc của học sinh. Chốt lại bảng đơn vị đo dung lượng thông tin và dung lượng phổ biến của các thiết bị nhớ hiện nay. | **2. Đơn vị đo thông tin**<br><br>**a) Khái niệm Byte:**<br>- Byte là đơn vị cơ bản dùng để đo dung lượng thông tin.<br>- Quy ước: **1 Byte (B) = 8 bit**.<br>- 1 Byte thường dùng để lưu trữ 1 kí tự.<br><br>**b) Các đơn vị đo dung lượng thông tin (Bảng 1.3 SGK):**<br>- **Byte (B):** 1 B.<br>- **Kilobyte (KB):** $1\text{ KB} = 1024\text{ B}$ (xấp xỉ 1 nghìn Byte).<br>- **Megabyte (MB):** $1\text{ MB} = 1024\text{ KB}$ (xấp xỉ 1 triệu Byte).<br>- **Gigabyte (GB):** $1\text{ GB} = 1024\text{ MB}$ (xấp xỉ 1 tỉ Byte).<br>- **Terabyte (TB):** $1\text{ TB} = 1024\text{ GB}$ (xấp xỉ 1 nghìn tỉ Byte).<br><br>**c) Dung lượng một số thiết bị lưu trữ thông dụng:**<br>- **RAM (Bộ nhớ trong):** Thường từ 2 GB đến 16 GB, máy tính đồ họa có thể 32 GB - 64 GB.<br>- **Đĩa quang CD:** Khoảng 700 MB.<br>- **Đĩa quang DVD:** Từ 4.7 GB đến 17 GB.<br>- **Thẻ nhớ / USB:** Thường từ vài GB đến hàng trăm GB (16 GB, 32 GB, 64 GB, 128 GB...).<br>- **Ổ đĩa cứng (HDD / SSD):** Thường từ vài trăm GB đến vài TB (256 GB, 512 GB, 1 TB, 2 TB...). |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Củng cố kiến thức về bit, dãy bit, các đơn vị đo dung lượng và khả năng tính toán dung lượng thiết bị lưu trữ.
b) Nội dung: Giải bài tập Luyện tập 1 và 2 SGK trang 15; trả lời câu hỏi trắc nghiệm nhanh.
c) Sản phẩm: Lời giải chi tiết bài tập 1, 2 và đáp án câu hỏi trắc nghiệm trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ cho học sinh làm việc cá nhân hoàn thành 2 bài tập trong mục Luyện tập SGK trang 15:<br>+ **Bài 1:** Một GB xấp xỉ bao nhiêu byte?<br>A. Một nghìn byte.<br>B. Một triệu byte.<br>C. Một tỉ byte.<br>D. Một nghìn tỉ byte.<br>+ **Bài 2:** Giả sử một bức ảnh được chụp bằng một máy ảnh chuyên nghiệp có dung lượng khoảng 12 MB. Vậy một thẻ nhớ 16 GB có thể chứa bao nhiêu bức ảnh như vậy?<br>- **GV:** Bổ sung thêm câu hỏi trắc nghiệm nhanh:<br>+ **Câu 3:** Đơn vị đo dung lượng thông tin nhỏ nhất là gì? (A. Byte; B. Bit; C. KB; D. MB).<br>+ **Câu 4:** Dãy bit 01000001 biểu diễn thông tin dạng nào? (A. Chữ cái A; B. Âm thanh; C. Hình ảnh; D. Cả A, B, C đều có thể).<br>- **HS:** Nhận nhiệm vụ, suy nghĩ giải bài tập vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Độc lập tính toán bài 2: Đổi 16 GB ra MB rồi chia cho 12 MB.<br>- **GV:** Quan sát, hướng dẫn học sinh có 2 cách tính (cách xấp xỉ và cách tính chuẩn $1024$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời 1 học sinh lên bảng giải Bài 2; gọi các học sinh khác trả lời câu 1, 3, 4.<br>- **HS:** Trình bày lời giải Bài 2:<br>+ Đổi: $16\text{ GB} = 16 \times 1024\text{ MB} = 16\,384\text{ MB}$.<br>+ Số lượng bức ảnh thẻ nhớ 16 GB có thể chứa là:<br>$16\,384 : 12 \approx 1365{,}33 \rightarrow$ Chứa được khoảng **1365 bức ảnh**.<br>*(Nếu tính theo hệ số xấp xỉ 1000: $16\text{ GB} \approx 16\,000\text{ MB} \implies 16\,000 : 12 \approx 1333$ bức ảnh).*<br>- **HS:** Đáp án Bài 1: Chọn C (Một tỉ byte). Câu 3: Chọn B (Bit). Câu 4: Chọn D.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài giải chuẩn xác. Nhấn mạnh trong thực tế khi mua thẻ nhớ hoặc ổ cứng, các nhà sản xuất thường tính theo hệ số 1000, còn hệ điều hành máy tính hiển thị theo chuẩn 1024. | **Đáp án bài tập Luyện tập (SGK trang 15):**<br><br>**1. Bài 1 (SGK trang 15):**<br>- **Đáp án đúng: C. Một tỉ byte**.<br>- Giải thích: $1\text{ GB} = 1024\text{ MB} = 1024 \times 1024\text{ KB} = 1024 \times 1024 \times 1024\text{ B} \approx 10^9\text{ B}$ (một tỉ byte).<br><br>**2. Bài 2 (SGK trang 15):**<br>- Tóm tắt: 1 bức ảnh $= 12\text{ MB}$. Thẻ nhớ $= 16\text{ GB}$. Hỏi chứa được bao nhiêu bức ảnh?<br>- Bài giải:<br>+ Đổi đơn vị: $16\text{ GB} = 16 \times 1024\text{ MB} = 16\,384\text{ MB}$.<br>+ Số bức ảnh thẻ nhớ 16 GB có thể chứa được là:<br>$16\,384 : 12 \approx 1365{,}33$ (bức ảnh).<br>+ Kết luận: Thẻ nhớ 16 GB có thể chứa được khoảng **1365 bức ảnh**.<br><br>**3. Trắc nghiệm củng cố mở rộng:**<br>- Câu 3: **B. Bit**.<br>- Câu 4: **D. Cả A, B, C đều có thể** (Dãy bit tùy theo ngữ cảnh của chương trình có thể là mã chữ cái, giá trị màu điểm ảnh hoặc mẫu âm thanh). |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)
a) Mục tiêu: Vận dụng kiến thức bài học vào thực tế máy tính gia đình/phòng thực hành và phát triển tư duy mở rộng về mã hóa nhị phân.
b) Nội dung:
- Bài 1 Vận dụng SGK trang 15: Kiểm tra và ghi lại dung lượng các ổ đĩa của máy tính em đang sử dụng (dung lượng tổng và dung lượng còn trống).
- Bài 2 Vận dụng SGK trang 15: Thực hiện tương tự Hoạt động 1 với dãy các số từ 0 đến 15 để tìm mã hoá của các số từ 8 đến 15 và đưa ra nhận xét.
- Hướng dẫn tự học ở nhà.
c) Sản phẩm: Phiếu kết quả khảo sát ổ đĩa máy tính và bảng mã hóa 4 bit của các số từ 8 đến 15.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn nhiệm vụ Vận dụng 1: Hướng dẫn học sinh cách mở File Explorer (nhấn tổ hợp phím Windows + E) $\rightarrow$ chọn "This PC" để xem các ổ đĩa của máy tính. Yêu cầu ghi lại tên ổ đĩa, dung lượng còn trống và tổng dung lượng.<br>- **GV:** Giao nhiệm vụ Vận dụng 2: "Ở Hoạt động 1, ta đã chia đôi dãy từ 0 đến 7 và cần 3 lần chia (3 bit). Bây giờ nếu mở rộng dãy số gấp đôi, từ 0 đến 15: Ta cần bao nhiêu lần chia đôi để xác định một số? Hãy tìm mã hoá của các số từ 8 đến 15 và nhận xét về chữ số bit đầu tiên của các số này."<br>- **HS:** Lắng nghe hướng dẫn, ghi chép nhiệm vụ vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh tại lớp để tìm quy luật cho dãy từ 0 đến 15: Chia đôi dãy 0..15 thành nửa trái (0..7) và nửa phải (8..15). Vì các số từ 8 đến 15 đều nằm ở nửa phải nên lần chia thứ nhất đều ghi nhận giá trị 1 (phải)!<br>- **GV:** Gợi ý: Sau lần chia thứ nhất, nửa phải (8..15) tương tự như dãy (0..7) nhưng được cộng thêm 8. Do đó cần đúng 4 bit để mã hóa.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời 1 học sinh lên bảng viết mã hóa của số 8 và số 15.<br>- **HS:** Trình bày:<br>+ Số 8: phải, trái, trái, trái $\rightarrow$ 1000.<br>+ Số 15: phải, phải, phải, phải $\rightarrow$ 1111.<br>+ Nhận xét: Tất cả các số từ 8 đến 15 đều có bit đầu tiên bên trái là **1**.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng kết: Dãy 1 bit mã hóa được 2 số ($2^1$); 2 bit mã hóa được 4 số ($2^2$); 3 bit mã hóa được 8 số ($2^3$); 4 bit mã hóa được 16 số ($2^4$). Đây chính là nền tảng của hệ đếm nhị phân trong khoa học máy tính.<br>- **GV:** Dặn dò HS về nhà thực hiện kiểm tra ổ đĩa máy tính ở nhà hoặc phòng thực hành trường, học bài và đọc trước Bài 4: Mạng máy tính. | **Vận dụng và Hướng dẫn tự học:**<br><br>**1. Bài 1 (SGK trang 15):**<br>- Hướng dẫn kiểm tra dung lượng ổ đĩa trên máy tính:<br>+ Bước 1: Mở **File Explorer** $\rightarrow$ chọn **This PC**.<br>+ Bước 2: Quan sát mục **Devices and drives**.<br>+ Bước 3: Ghi lại số liệu (Ví dụ mẫu: Ổ C: Dung lượng trống 45.5 GB / Tổng dung lượng 120 GB; Ổ D: Dung lượng trống 180 GB / Tổng dung lượng 380 GB).<br><br>**2. Bài 2 (SGK trang 15):**<br>- Với dãy số từ 0 đến 15 (gồm 16 số), cần 4 lần chia đôi liên tiếp nên mỗi số được mã hóa bằng một dãy gồm **4 bit**.<br>- Bảng mã hóa các số từ 8 đến 15:<br>+ Số 8: 1000  —  Số 9: 1001<br>+ Số 10: 1010  —  Số 11: 1011<br>+ Số 12: 1100  —  Số 13: 1101<br>+ Số 14: 1110  —  Số 15: 1111<br>- **Nhận xét quan trọng:** Tất cả các số từ 8 đến 15 đều bắt đầu bằng chữ số **1** ở vị trí ngoài cùng bên trái (vì chúng đều thuộc nửa phải trong lần chia đầu tiên). |


---

Tiết 7 - BÀI 4: MẠNG MÁY TÍNH
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nêu được khái niệm mạng máy tính và lợi ích của mạng máy tính trong cuộc sống.
- Kể được tên và phân loại đúng các thành phần chính của một mạng máy tính (thiết bị đầu cuối, thiết bị kết nối, phần mềm mạng).
- Nêu được ví dụ cụ thể về trường hợp mạng không dây tiện dụng hơn mạng có dây.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát các thiết bị mạng trong gia đình và phòng thực hành Tin học của trường; chủ động đọc hiểu các thuật ngữ mạng máy tính.
- Giao tiếp và hợp tác: Tích cực thảo luận nhóm để so sánh các loại mạng lưới, phân tích mô hình mạng Hình 2.1 và đề xuất giải pháp kết nối mạng tối ưu.

b) Năng lực Tin học:
- NLa (Sử dụng và quản lý các phương tiện công nghệ thông tin và truyền thông): Nhận biết, gọi đúng tên và phân biệt được các thiết bị mạng thông dụng (máy tính, máy in, router, switch, cáp mạng, wifi); hiểu được vai trò của từng thành phần trong hệ thống mạng.
- NLb (Ứng xử phù hợp trong môi trường số): Nhận thức được lợi ích và ý nghĩa của việc chia sẻ tài nguyên thông tin và thiết bị trong môi trường mạng an toàn, tiết kiệm.

## 3. Về phẩm chất
- Chăm chỉ: Tích cực tìm hiểu, liên hệ kiến thức bài học với các thiết bị mạng thực tế quanh mình.
- Trách nhiệm: Có ý thức bảo vệ, giữ gìn các thiết bị mạng, dây cáp mạng trong phòng thực hành Tin học của trường.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng điện tử trình chiếu, máy tính kết nối Internet, máy chiếu/Tivi, thiết bị mạng trực quan (đoạn cáp mạng xoắn đôi bấm đầu RJ45, USB thu Wifi, bộ định tuyến Wifi - Wireless Router, Switch mạng mini 5 cổng, máy in kết nối mạng), phiếu học tập số 1 (Phân loại thiết bị mạng).
2. Học sinh: Sách giáo khoa Tin học 6 (Kết nối tri thức với cuộc sống), vở ghi, chuẩn bị bài và quan sát trước mạng Internet tại gia đình hoặc trường học.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (6 phút)
a) Mục tiêu: Kích hoạt liên tưởng của học sinh từ các mạng lưới đời sống (giao thông, điện, nước) sang mạng máy tính; làm rõ 2 đặc tính cơ bản: Kết nối và Chia sẻ.
b) Nội dung:
- Đọc tình huống đối thoại của bạn An và Khoa về các con đường giao thông.
- Khám phá Hoạt động 1 SGK trang 16 (Mạng lưới).
c) Sản phẩm: Câu trả lời về các mạng lưới trong cuộc sống và điểm chung của chúng (kết nối các thành viên, chia sẻ tài nguyên).
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gọi hai học sinh đọc phân vai đoạn đối thoại giữa bạn An và bạn Khoa ở đầu trang 16 SGK:<br>+ An: "Tại sao những nơi có đường đi qua thường trù phú hơn những nơi khác?"<br>+ Khoa: "Đường làm nên sự kì diệu. Đường nối các ngôi nhà, làng mạc, thành phố... làm xa trở nên gần. Nhiều con đường đan với nhau tạo thành mạng lưới giao thông..."<br>- **GV:** Yêu cầu học sinh thực hiện Hoạt động 1 (Mạng lưới) trang 16 SGK:<br>1) Kể ra một số mạng lưới giống như mạng giao thông đường bộ?<br>2) Những gì được vận chuyển trên các mạng lưới đó?<br>3) Điểm chung của những mạng lưới đó là gì?<br>+ Phương án A: Có nhiều thành viên.<br>+ Phương án B: Chia sẻ tài nguyên.<br>+ Phương án C: Kết nối các thành viên.<br>+ Phương án D: Có nhiều đường cắt nhau.<br>- **HS:** Lắng nghe, theo dõi SGK và suy nghĩ câu trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ cá nhân trong 1 phút và trao đổi nhanh với bạn cùng bàn.<br>- **GV:** Bao quát lớp, khuyến khích học sinh liên hệ với các tiện ích sinh hoạt hàng ngày trong gia đình (nước máy, điện lưới, truyền hình cáp...).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện học sinh phát biểu.<br>- **HS:** Trả lời:<br>1) Các mạng lưới khác: Mạng lưới cấp nước sinh hoạt, mạng lưới điện quốc gia, mạng lưới viễn thông/điện thoại, mạng lưới đường sắt, đường thủy...<br>2) Vật được vận chuyển: Nước sạch (mạng nước), dòng điện/năng lượng (mạng điện), tín hiệu âm thanh/hình ảnh (mạng viễn thông), hàng hóa và con người (mạng giao thông).<br>3) Điểm chung: Chọn các phương án **A, B, C** (Có nhiều thành viên; Chia sẻ tài nguyên; Kết nối các thành viên).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa câu trả lời. Dẫn dắt vào bài mới: Mọi mạng lưới trong đời sống đều có hai đặc điểm cốt lõi là **Kết nối** và **Chia sẻ**. Vậy trong lĩnh vực công nghệ thông tin, khi các máy tính được kết nối với nhau để chia sẻ dữ liệu thì chúng tạo thành cái gì? Chúng ta cùng tìm hiểu Bài 4: Mạng máy tính! | **Khởi động: Khám phá khái niệm mạng lưới**<br>- Các mạng lưới quen thuộc trong cuộc sống: Mạng giao thông, mạng lưới điện, mạng lưới cấp nước, mạng viễn thông...<br>- Vật vận chuyển: Hàng hóa, con người, nước, dòng điện, thông tin...<br>- Hai đặc điểm cốt lõi của mạng lưới:<br>1) **Kết nối:** Nối các thành viên/địa điểm lại với nhau.<br>2) **Chia sẻ:** Chia sẻ tài nguyên dùng chung cho nhiều người sử dụng. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (24 phút)

### 1. Hoạt động 2.1: Mạng máy tính là gì? (10 phút)
a) Mục tiêu: Nêu được định nghĩa mạng máy tính và chỉ ra các lợi ích cốt lõi của mạng máy tính trong cuộc sống.
b) Nội dung:
- Hoạt động 2 SGK trang 17 (Mạng máy tính).
- Phân tích hình ảnh minh họa trao đổi dữ liệu và dùng chung máy in:
![Hình minh họa Trao đổi dữ liệu và chia sẻ máy in](khbd-ill:hinh_trao_doi_du_lieu_may_in)
- Khái niệm mạng máy tính (chỉ cần từ 2 máy tính kết nối với nhau để truyền thông tin).
- Hai lợi ích căn bản: Trao đổi dữ liệu và Chia sẻ thiết bị (dùng chung máy in, máy quét, ổ đĩa lưu trữ chung).
- Thảo luận câu hỏi củng cố: Lợi ích của mạng máy tính đối với học sinh và nhà trường.
c) Sản phẩm: Định nghĩa mạng máy tính và bảng liệt kê các lợi ích của mạng máy tính trong vở HS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình minh họa trang 17 SGK (Hình bạn Minh gửi tệp ảnh cho bạn An và hình nhiều máy tính cùng in ra một máy in).<br>- **GV:** Nêu câu hỏi trong Hoạt động 2:<br>1) Mạng máy tính chia sẻ những gì?<br>2) Em hãy nêu một số ví dụ về lợi ích của mạng máy tính trong đời sống?<br>- **GV:** Đặt tiếp câu hỏi: "Cần tối thiểu bao nhiêu máy tính kết nối với nhau để tạo thành một mạng máy tính?"<br>- **HS:** Quan sát hình ảnh, đọc thông tin mục 1 trang 17 SGK.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi trong 3 phút, tìm ý trả lời cho 2 câu hỏi.<br>- **GV:** Quan sát, hướng dẫn học sinh phân tích sự tiện lợi khi chia sẻ máy in thay vì mỗi bàn làm việc phải mua riêng một máy in.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện 2 nhóm báo cáo.<br>- **HS Nhóm 1:** Trình bày:<br>+ Mạng máy tính chia sẻ: Dữ liệu (tệp văn bản, hình ảnh, bài hát, video) và Thiết bị phần cứng (máy in, máy quét, ổ cứng lưu trữ...).<br>+ Chỉ cần từ 2 máy tính kết nối với nhau là tạo thành mạng máy tính.<br>- **HS Nhóm 2:** Nêu ví dụ lợi ích: Giúp học sinh học trực tuyến, gửi bài tập cho thầy cô qua email; giúp bố mẹ làm việc từ xa, mua sắm online; giúp trường học tiết kiệm chi phí mua thiết bị.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kiến thức và yêu cầu học sinh ghi nhớ hai nội dung trong khung cam trang 17 SGK: Định nghĩa mạng máy tính và Lợi ích của mạng máy tính. | **1. Mạng máy tính là gì?**<br><br>**a) Khái niệm:**<br>- Hai hay nhiều máy tính và các thiết bị được kết nối để truyền thông tin cho nhau tạo thành một **mạng máy tính**.<br>*(Lưu ý: Chỉ cần tối thiểu 2 máy tính kết nối với nhau là đã có một mạng máy tính).*<br><br>**b) Lợi ích của mạng máy tính:**<br>- Người sử dụng có thể:<br>1) **Liên lạc với nhau:** Gửi thư điện tử (email), nhắn tin, gọi video, hội họp trực tuyến.<br>2) **Trao đổi dữ liệu:** Gửi và nhận tệp tài liệu, bài giảng, hình ảnh, âm thanh, video dễ dàng, nhanh chóng.<br>3) **Dùng chung thiết bị (Chia sẻ tài nguyên phần cứng):** Nhiều máy tính có thể dùng chung một máy in, máy quét, ổ đĩa lưu trữ chung... giúp tiết kiệm chi phí mua sắm và vận hành. |

### 2. Hoạt động 2.2: Các thành phần của mạng máy tính (14 phút)
a) Mục tiêu:
- Kể tên và phân loại đúng 3 thành phần chính của mạng máy tính: Thiết bị đầu cuối, Thiết bị kết nối, Phần mềm mạng.
- Phân biệt đường truyền có dây và đường truyền không dây; nêu được ví dụ về tính tiện dụng của mạng không dây.
b) Nội dung:
- Khám phá Hoạt động 3 SGK trang 18 và Hình 2.1:
![Hình 2.1. Các thiết bị được nối vào mạng](khbd-ill:hinh_2_1_thiet_bi_mang)
- Phân tích 3 thành phần chính:
  1. Thiết bị đầu cuối: máy tính để bàn, máy tính xách tay, điện thoại thông minh, máy in, máy quét, máy chủ, máy ảnh số...
  2. Thiết bị kết nối: đường truyền dữ liệu (cáp xoắn, cáp quang, sóng vô tuyến wifi/bluetooth), bộ chia (Hub), bộ chuyển mạch (Switch), bộ định tuyến (Router), bộ định tuyến không dây (Wireless Router), điểm truy cập không dây (Access Point).
  3. Phần mềm mạng: ứng dụng truyền thông (trình duyệt web, email, Zalo, Google Meet...) và phần mềm điều khiển truyền dữ liệu.
- Tìm hiểu đường truyền có dây và không dây: ưu điểm vượt trội của mạng không dây (không vướng dây cáp, di chuyển cơ động, tiện lợi nơi công cộng, tránh đứt dây do chuột cắn hay thời tiết).
- Trả lời các câu hỏi củng cố trang 19 SGK.
c) Sản phẩm: Sơ đồ phân loại 3 thành phần mạng máy tính và bảng so sánh mạng có dây - không dây trong vở HS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Hình 2.1 SGK trang 18 (Các thiết bị được nối vào mạng).<br>- **GV:** Yêu cầu các nhóm hoàn thành Hoạt động 3:<br>1) Những thiết bị nào đang được nối vào mạng trong Hình 2.1?<br>2) Các thiết bị đó được nối với nhau như thế nào? Qua các thiết bị trung gian nào?<br>- **GV:** Giới thiệu mẫu vật trực quan: Đoạn dây cáp mạng bấm đầu RJ45, USB thu Wifi, bộ phát Wifi (Router).<br>- **GV:** Hướng dẫn học sinh phân loại mạng thành 3 thành phần chính và phân biệt giữa đường truyền có dây với đường truyền không dây.<br>- **GV:** Nêu câu hỏi thảo luận: "Vì sao mạng không dây (Wifi) ngày càng được sử dụng phổ biến và tiện dụng hơn mạng có dây?"<br>- **HS:** Quan sát Hình 2.1, các thiết bị mẫu và nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm 4 em trong 4 phút: Liệt kê các thiết bị trong Hình 2.1; xếp chúng vào 2 nhóm: thiết bị đầu cuối và thiết bị kết nối; nêu các ưu điểm của mạng không dây.<br>- **GV:** Theo dõi các nhóm, hướng dẫn học sinh nhận biết các biểu tượng sóng Wifi màu cam nối từ máy tính xách tay, điện thoại đến bộ định tuyến không dây.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện nhóm 1 chỉ ra các thiết bị trong Hình 2.1:<br>+ Thiết bị đầu cuối: Máy tính để bàn, máy tính xách tay, điện thoại di động, máy in, máy quét, máy chủ.<br>+ Thiết bị kết nối: Bộ chuyển mạch (Switch), bộ định tuyến không dây (Wireless Router), dây cáp mạng, sóng vô tuyến.<br>- **GV:** Mời đại diện nhóm 2 trả lời về ưu điểm của mạng không dây:<br>+ Mạng không dây kết nối bằng sóng vô tuyến (wifi, bluetooth...).<br>+ Tiện lợi: Không phải khoan tường, đi dây rườm rà; người dùng có thể tự do di chuyển (như đi trên ô tô, sân bay, quán cà phê vẫn vào được mạng); tránh bị sự cố chuột cắn đứt dây hoặc mưa bão làm hỏng đường dây.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa câu trả lời. Chốt lại 3 thành phần chính của mạng máy tính và yêu cầu học sinh ghi nhớ nội dung trong khung cam trang 18 SGK. | **2. Các thành phần của mạng máy tính**<br><br>Mạng máy tính gồm **3 thành phần chính**:<br><br>**a) Các thiết bị đầu cuối:**<br>- Là điểm xuất phát hoặc đích đến của dữ liệu trong mạng.<br>- Gồm: Máy tính để bàn, máy tính xách tay, máy tính bảng, điện thoại thông minh, máy in, máy quét, máy chủ, máy ảnh số, camera an ninh...<br><br>**b) Các thiết bị kết nối:**<br>- Dùng để kết nối các thiết bị đầu cuối lại với nhau.<br>- Gồm:<br>+ **Đường truyền dữ liệu:** Đường truyền có dây (dây cáp mạng, cáp quang) và đường truyền không dây (sóng vô tuyến như Wifi, Bluetooth).<br>+ **Thiết bị mạng:** Bộ chia (Hub), bộ chuyển mạch (Switch), bộ định tuyến (Router), bộ định tuyến không dây (Wireless Router), điểm truy cập không dây (Access Point).<br><br>**c) Phần mềm mạng:**<br>- Gồm các ứng dụng truyền thông trên thiết bị đầu cuối (trình duyệt web, email, mạng xã hội, phần mềm chat, học trực tuyến...) và phần mềm điều khiển quá trình truyền dữ liệu giữa các thiết bị.<br><br>**d) So sánh mạng có dây và mạng không dây:**<br>- **Mạng có dây:** Sử dụng dây dẫn mạng. Ưu điểm: Đường truyền tốc độ cao, tín hiệu ổn định. Nhược điểm: Vướng víu, cố định vị trí, tốn chi phí đi dây và bảo trì.<br>- **Mạng không dây:** Sử dụng sóng vô tuyến (Wifi). Ưu điểm: Thuận tiện lắp đặt (không cần đục tường), linh hoạt di chuyển thiết bị, phục vụ tốt nơi công cộng (sân bay, trung tâm thương mại, trường học). |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
a) Mục tiêu: Khắc sâu kiến thức về định nghĩa mạng, lợi ích và các thiết bị kết nối mạng có dây/không dây.
b) Nội dung: Giải bài tập Luyện tập 1 và 2 SGK trang 19.
![Hình 2.2. Các thiết bị được nối vào mạng](khbd-ill:hinh_2_2_ket_noi_mang)
c) Sản phẩm: Lời giải chính xác bài tập 1 và 2 trong vở HS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu nội dung 2 bài tập mục Luyện tập SGK trang 19 lên màn hình:<br>+ **Bài 1:** Em hãy chọn các phương án đúng. Máy tính kết nối với nhau để:<br>Phương án A: Chia sẻ các thiết bị.<br>Phương án B: Tiết kiệm điện.<br>Phương án C: Trao đổi dữ liệu.<br>Phương án D: Thuận lợi cho việc sửa chữa.<br>+ **Bài 2:** Chiếu Hình 2.2. Em hãy chọn các phương án đúng. Thiết bị có kết nối không dây ở Hình 2.2 là:<br>Phương án A: Máy tính để bàn.<br>Phương án B: Máy tính xách tay.<br>Phương án C: Điện thoại di động.<br>Phương án D: Bộ định tuyến.<br>- **HS:** Nhận nhiệm vụ, suy nghĩ độc lập và ghi câu trả lời vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc cá nhân trong 2 phút.<br>- **GV:** Quan sát, nhắc nhở học sinh chú ý kí hiệu sóng vô tuyến ở Hình 2.2.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Gọi 2 học sinh đứng tại chỗ trả lời và giải thích.<br>- **HS 1:** Trả lời Bài 1: Chọn phương án **A** và **C**. Vì mục đích cơ bản của mạng máy tính là chia sẻ thiết bị và trao đổi dữ liệu.<br>- **HS 2:** Trả lời Bài 2: Chọn phương án **B** (Máy tính xách tay) và **C** (Điện thoại di động). Vì ở Hình 2.2, hai thiết bị này có biểu tượng sóng phát tín hiệu đến Bộ định tuyến không dây, không có dây nối vật lý.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt đáp án đúng và tuyên dương học sinh trả lời nhanh, chính xác. | **Đáp án bài tập Luyện tập (SGK trang 19):**<br><br>**1. Bài 1 (SGK trang 19):**<br>- **Đáp án đúng: Phương án A và C**.<br>+ **A. Chia sẻ các thiết bị** (Ví dụ: dùng chung máy in, ổ cứng mạng).<br>+ **C. Trao đổi dữ liệu** (Ví dụ: gửi tệp văn bản, ảnh, thư điện tử).<br>- Phương án B và D sai vì kết nối mạng không nhằm mục đích tiết kiệm điện hay giúp sửa chữa máy tính dễ hơn.<br><br>**2. Bài 2 (SGK trang 19):**<br>- **Đáp án đúng: Phương án B và C**.<br>+ **B. Máy tính xách tay** (kết nối qua sóng Wifi).<br>+ **C. Điện thoại di động** (kết nối qua sóng Wifi).<br>- Máy tính để bàn trong hình được nối bằng dây cáp mạng đến Bộ chuyển mạch (Switch). |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
a) Mục tiêu: Vận dụng kiến thức thiết kế sơ đồ mạng và phân tích hệ thống mạng thực tế trong gia đình.
b) Nội dung: Giải bài tập Vận dụng 1 và 2 SGK trang 19.
![Hình 2.3. Ví dụ cách kết nối 5 máy tính thành một mạng](khbd-ill:hinh_2_3_ket_noi_5_may)
c) Sản phẩm: Bản vẽ 2 sơ đồ kết nối 5 máy tính và câu trả lời phân tích mạng gia đình bạn An.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Hình 2.3 và nêu nội dung 2 bài tập Vận dụng SGK trang 19:<br>+ **Bài 1:** Phòng thư viện của trường có 5 máy tính cần kết nối thành một mạng. Có thể có nhiều cách kết nối, ví dụ như Hình 2.3. Em hãy vẽ hai cách khác để kết nối chúng thành một mạng.<br>+ **Bài 2:** Nhà bạn An có điện thoại di động của bố, của mẹ và một máy tính xách tay đang cùng truy cập mạng Internet. Theo em, các thiết bị đó có đang được kết nối thành một mạng máy tính không? Nếu có, em hãy chỉ ra các thiết bị đầu cuối và thiết bị kết nối.<br>- **HS:** Nhận nhiệm vụ học tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh cách vẽ sơ đồ mạng và phân tích các thiết bị mạng gia đình bạn An.<br>- **GV:** Gợi ý cách kết nối hình sao (nối tập trung qua Switch) và kết nối hình vòng (nối tiếp vòng tròn khép kín).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện học sinh trả lời Bài 2.<br>- **HS:** Trả lời:<br>+ Các thiết bị nhà bạn An có tạo thành một mạng máy tính.<br>+ Thiết bị đầu cuối: Điện thoại của bố, điện thoại của mẹ, máy tính xách tay.<br>+ Thiết bị kết nối: Bộ định tuyến không dây (Modem Wifi / Wireless Router) và sóng vô tuyến (sóng Wifi).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa câu trả lời. Hướng dẫn học sinh vẽ hai sơ đồ kết nối mạng 5 máy tính vào vở tự học ở nhà.<br>- **GV:** Dặn dò: Ôn tập lại toàn bộ kiến thức Bài 3 và Bài 4; chuẩn bị đọc trước Bài 5: Internet. | **Vận dụng và Hướng dẫn tự học:**<br><br>**1. Bài 1 (SGK trang 19):**<br>- Hai cách kết nối khác cho 5 máy tính trong phòng thư viện:<br>+ **Cách 1 (Mô hình hình sao - Star Topology):** Đặt một thiết bị kết nối trung tâm (bộ chuyển mạch Switch). Cả 5 máy tính đều cắm dây cáp mạng trực tiếp về Switch này. Đây là cách phổ biến nhất vì nếu 1 máy hỏng thì các máy khác vẫn hoạt động bình thường.<br>+ **Cách 2 (Mô hình hình vòng - Ring Topology):** Nối máy 1 với máy 2, máy 2 với máy 3, máy 3 với máy 4, máy 4 với máy 5, và máy 5 nối ngược lại về máy 1 tạo thành một vòng tròn khép kín.<br><br>**2. Bài 2 (SGK trang 19):**<br>- **Kết luận:** Các thiết bị đó **CÓ** đang được kết nối thành một mạng máy tính.<br>- **Phân loại thành phần mạng:**<br>+ **Thiết bị đầu cuối:** Điện thoại di động của bố, điện thoại di động của mẹ, máy tính xách tay.<br>+ **Thiết bị kết nối:** Bộ định tuyến không dây (Modem Wifi / Wireless Router gia đình) và đường truyền không dây (sóng Wifi). |


---

Tiết 8 - BÀI 5: INTERNET
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Biết được Internet là gì (mạng toàn cầu liên kết các mạng máy tính).
- Nêu được các đặc điểm chính của Internet: tính toàn cầu, tính tương tác, tính dễ tiếp cận, tính không chủ sở hữu (cùng các đặc điểm bổ trợ: tính cập nhật, tính lưu trữ, tính đa dạng, tính ẩn danh).
- Nêu được một số lợi ích chính của Internet trong học tập, giao tiếp, giải trí và đời sống; nhận thức được việc sử dụng Internet điều độ, an toàn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác tìm hiểu các tiện ích và dịch vụ trên Internet qua trải nghiệm thực tế; chủ động lựa chọn những hoạt động hữu ích trên môi trường mạng.
- Giao tiếp và hợp tác: Tích cực thảo luận nhóm, chia sẻ các ứng dụng thực tế của Internet trong đời sống gia đình và xã hội.

b) Năng lực Tin học:
- NLa (Sử dụng và quản lý các phương tiện công nghệ thông tin và truyền thông): Biết cách kết nối máy tính với Internet thông qua nhà cung cấp dịch vụ Internet (ISP); nhận biết được các dịch vụ thông tin phổ biến (WWW, tìm kiếm, email, mạng xã hội...).
- NLb (Ứng xử phù hợp trong môi trường số): Nhận thức được tính hai mặt của Internet; hình thành thói quen sử dụng Internet an toàn, bảo vệ sức khỏe và không lạm dụng thời gian trực tuyến.

## 3. Về phẩm chất
- Chăm chỉ: Tích cực khai thác các nguồn học liệu bổ ích trên Internet để phục vụ học tập.
- Trách nhiệm: Tuân thủ các quy tắc ứng xử văn minh trên môi trường mạng; có ý thức tự điều chỉnh thời gian truy cập Internet khoa học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng điện tử trình chiếu, máy tính kết nối Internet, máy chiếu/Tivi, phiếu học tập số 1 (Đặc điểm và lợi ích của Internet).
2. Học sinh: Sách giáo khoa Tin học 6 (Kết nối tri thức với cuộc sống), vở ghi, đọc trước bài 5.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (6 phút)
a) Mục tiêu: Kích hoạt sự quan sát thực tế của học sinh về tiện ích mua sắm/đặt vé trực tuyến; dẫn dắt học sinh vào khái niệm Internet từ nhu cầu thực tiễn.
b) Nội dung:
- Đọc tình huống mở đầu trang 20 SGK: Mẹ bạn An cần mua vé máy bay gấp nhưng bận không đến phòng vé được. Bạn Minh đã gợi ý mẹ An đặt vé online qua Internet.
- Nêu câu hỏi: "Tại sao chỉ cần ngồi ở nhà có máy tính hoặc điện thoại kết nối Internet là có thể tra cứu chuyến bay, chọn ghế và thanh toán vé máy bay một cách nhanh chóng?"
c) Sản phẩm: Câu trả lời của học sinh về sự tiện lợi của Internet trong giao dịch đời sống.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gọi hai học sinh đọc phân vai đoạn đối thoại giữa bạn An và bạn Minh ở đầu trang 20 SGK:<br>+ An: "Mẹ tớ có việc gấp cần đi công tác ngay nhưng bận quá chưa đến phòng vé máy bay được."<br>+ Minh: "Quá đơn giản! Mẹ bạn có thể đặt vé trên Internet mà không cần phải đến phòng vé. Các hãng hàng không đăng tin về các chuyến bay, giờ bay, giá vé trên Internet. Nếu có kết nối Internet, mẹ bạn có thể tìm thông tin, đặt vé và thanh toán."<br>- **GV:** Đặt câu hỏi cho cả lớp: "Nhờ đâu mà bạn Minh lại khẳng định mẹ bạn An có thể đặt vé máy bay ngay tại nhà? Internet đã làm thay đổi thói quen mua sắm, đi lại của con người như thế nào?"<br>- **HS:** Lắng nghe, theo dõi SGK và suy nghĩ câu trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ cá nhân trong 1 phút và trao đổi nhanh với bạn cùng bàn.<br>- **GV:** Bao quát lớp, gợi ý học sinh liên hệ các dịch vụ quen thuộc (mua hàng Shopee/Lazada, đặt đồ ăn Grab/ShopeeFood, chuyển tiền ngân hàng...).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời 2 học sinh phát biểu.<br>- **HS:** Trả lời: Nhờ có mạng Internet kết nối các máy tính của hãng hàng không với máy tính/điện thoại của người dùng, giúp truyền tải dữ liệu và giao dịch tức thời mà không cần gặp mặt trực tiếp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa câu trả lời. Dẫn dắt vào bài mới: Ở Bài 4, các em đã biết mạng máy tính giúp kết nối các máy tính trong phạm vi hẹp (phòng học, gia đình). Khi hàng triệu mạng máy tính trên toàn thế giới kết nối lại với nhau, chúng tạo nên mạng Internet khổng lồ. Bài học hôm nay sẽ giúp các em hiểu rõ bản chất, đặc điểm và lợi ích to lớn của Internet! | **Khởi động: Đặt vấn đề về vai trò của Internet**<br>- Tình huống thực tế: Mua vé máy bay, đặt xe, mua hàng trực tuyến tại nhà qua Internet.<br>- Cơ chế: Máy tính của người dùng kết nối với hệ thống máy chủ của nhà cung cấp dịch vụ thông qua mạng toàn cầu Internet.<br>- Câu hỏi định hướng: Internet là gì? Nó có những đặc điểm và mang lại lợi ích gì cho con người? |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (24 phút)

### 1. Hoạt động 2.1: Internet là gì? (8 phút)
a) Mục tiêu: Biết được Internet là mạng liên kết các mạng máy tính trên phạm vi toàn cầu; nêu được vai trò của nhà cung cấp dịch vụ Internet (ISP).
b) Nội dung:
- Khám phá Hoạt động 1 SGK trang 20 (Internet là gì? Người sử dụng có thể làm được những gì?).
- Khái niệm: "Internet là mạng của các mạng máy tính".
- Muốn kết nối Internet: Cần đăng ký với nhà cung cấp dịch vụ Internet (ISP - Internet Service Provider) như VNPT, Viettel, FPT...
- Hoàn thành bài tập điền từ trang 21 SGK.
c) Sản phẩm: Khái niệm Internet và đáp án bài tập điền từ vào chỗ trống trong vở HS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu học sinh đọc thầm mục 1 SGK trang 20 và thảo luận câu hỏi trong Hoạt động 1:<br>1) Em hiểu Internet là gì?<br>2) Người sử dụng có thể làm được những gì khi truy cập Internet?<br>- **GV:** Đặt tiếp câu hỏi: "Để máy tính tại nhà hoặc trường học vào được Internet, chúng ta cần phải làm gì?"<br>- **GV:** Giao bài tập điền từ trang 21 SGK: Điền các từ (chia sẻ, liên kết, thông tin, dịch vụ, mạng) vào chỗ trống thích hợp.<br>- **HS:** Đọc thông tin SGK, suy nghĩ và hoàn thành bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cá nhân đọc SGK trong 2 phút, trao đổi cặp đôi hoàn thành 3 câu điền từ.<br>- **GV:** Quan sát, hướng dẫn học sinh nhận biết thuật ngữ viết tắt ISP (Internet Service Provider) qua các nhà mạng quen thuộc tại Việt Nam (Viettel, VNPT, FPT...).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện học sinh trả lời:<br>+ Khái niệm Internet.<br>+ Đáp án bài tập điền từ (a, b, c).<br>- **HS:** Trả lời:<br>+ Internet là mạng liên kết các mạng máy tính trên khắp thế giới.<br>+ Đáp án điền từ: a) (1) liên kết, (2) mạng; b) (3) chia sẻ, (4) thông tin; c) (5) dịch vụ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kiến thức và yêu cầu học sinh ghi nhớ nội dung khung cam trang 20 SGK. | **1. Internet là gì?**<br><br>**a) Khái niệm:**<br>- **Internet** là mạng liên kết các mạng máy tính trên khắp thế giới.<br>*(Ghi nhớ: "Internet là mạng của các mạng máy tính").*<br><br>**b) Kết nối Internet:**<br>- Để truy cập Internet, máy tính cần được kết nối với Internet thông qua một **nhà cung cấp dịch vụ Internet (ISP - Internet Service Provider)** như Viettel, VNPT, FPT...<br><br>**c) Mục đích sử dụng:**<br>- Người sử dụng truy cập Internet để tìm kiếm, chia sẻ, lưu trữ và trao đổi thông tin.<br>- Các dịch vụ phổ biến: Mạng thông tin toàn cầu (WWW), tìm kiếm thông tin (Google), thư điện tử (Email), mạng xã hội (Facebook, Zalo), học trực tuyến, giải trí...<br><br>**d) Đáp án bài tập điền từ (SGK trang 21):**<br>- a) Internet là mạng **(1) liên kết** các **(2) mạng** máy tính trên khắp thế giới.<br>- b) Người sử dụng truy cập Internet để tìm kiếm, **(3) chia sẻ**, lưu trữ và trao đổi **(4) thông tin**.<br>- c) Có nhiều **(5) dịch vụ** thông tin khác nhau trên Internet. |

### 2. Hoạt động 2.2: Đặc điểm của Internet (8 phút)
a) Mục tiêu: Nêu và phân tích được 4 đặc điểm chính của Internet: tính toàn cầu, tính tương tác, tính dễ tiếp cận, tính không chủ sở hữu.
b) Nội dung:
- Khám phá Hoạt động 2 SGK trang 21 (Đặc điểm của Internet).
- Phân tích 4 đặc điểm cốt lõi:
  1) Tính toàn cầu (hơn 1/3 dân số thế giới sử dụng, phủ sóng hầu hết các quốc gia).
  2) Tính tương tác (gửi và nhận phản hồi tức thì hai chiều, khác truyền hình/sách báo truyền thống).
  3) Tính dễ tiếp cận (kết nối mọi lúc mọi nơi bằng nhiều thiết bị thông minh).
  4) Tính không chủ sở hữu (là tài sản chung công cộng toàn cầu, không thuộc riêng quốc gia hay tập đoàn nào).
- Các đặc điểm bổ trợ: Tính cập nhật, tính lưu trữ, tính đa dạng, tính ẩn danh.
- Trả lời 2 câu hỏi củng cố mục 2 trang 21 SGK.
c) Sản phẩm: Bảng 4 đặc điểm chính của Internet và đáp án câu hỏi củng cố.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi Hoạt động 2: "Theo em, Internet có những đặc điểm gì nổi bật so với các phương tiện truyền thông trước đây (như sách in, đài phát thanh, truyền hình)?"<br>- **GV:** Hướng dẫn học sinh phân tích 4 đặc điểm chính:<br>1) Tính toàn cầu.<br>2) Tính tương tác.<br>3) Tính dễ tiếp cận.<br>4) Tính không chủ sở hữu.<br>- **GV:** Giải thích thêm các đặc điểm: Tính cập nhật, Tính lưu trữ, Tính đa dạng, Tính ẩn danh.<br>- **GV:** Yêu cầu học sinh làm việc cá nhân trả lời 2 câu hỏi củng cố trang 21 SGK.<br>- **HS:** Đọc thông tin mục 2 SGK, suy nghĩ và thảo luận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc cặp đôi trong 2 phút, so sánh tính tương tác của Internet (gửi tin nhắn nhận lại phản hồi ngay) với việc xem tivi (chỉ nhận thông tin một chiều).<br>- **GV:** Theo dõi, gợi ý làm rõ ý nghĩa của "Tính không chủ sở hữu" (Internet là mạng công cộng toàn cầu, không ai sở hữu toàn bộ Internet).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện học sinh trả lời câu hỏi 1 và 2 trang 21 SGK.<br>- **HS:** Trình bày:<br>+ Câu 1: Các đặc điểm chính là: **A (Tính toàn cầu), B (Tính tương tác), D (Tính dễ tiếp cận), F (Tính không chủ sở hữu)**.<br>+ Câu 2: Em thích nhất "Tính dễ tiếp cận" vì có thể học tập và tra cứu thông tin mọi lúc, mọi nơi chỉ với chiếc điện thoại thông minh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa câu trả lời. Chốt lại 4 đặc điểm chính của Internet và yêu cầu ghi nhớ nội dung khung cam trang 21 SGK. | **2. Đặc điểm của Internet**<br><br>**a) Bốn đặc điểm chính của Internet:**<br>- **Tính toàn cầu:** Kết nối hàng tỷ người dùng ở hầu hết các quốc gia và vùng lãnh thổ trên toàn Trái Đất.<br>- **Tính tương tác:** Người dùng có thể tức thời nhận và gửi thông tin phản hồi hai chiều (khác với truyền hình hay sách báo chỉ truyền thông một chiều).<br>- **Tính dễ tiếp cận:** Người dùng có thể tìm kiếm, lưu trữ, trao đổi và chia sẻ thông tin thuận tiện, nhanh chóng ở mọi lúc, mọi nơi.<br>- **Tính không chủ sở hữu:** Internet là mạng công cộng toàn cầu, không thuộc quyền sở hữu riêng hay do bất kỳ một tổ chức, cá nhân nào điều hành độc quyền.<br><br>**b) Một số đặc điểm khác:**<br>- **Tính cập nhật:** Thông tin mới được cập nhật liên tục từng giây.<br>- **Tính lưu trữ:** Dữ liệu được lưu trữ thường trực trên các máy chủ đám mây.<br>- **Tính đa dạng:** Truyền tải đa phương tiện (văn bản, âm thanh, hình ảnh, video).<br>- **Tính ẩn danh:** Người dùng có thể sử dụng biệt danh thay cho tên thật.<br><br>**c) Đáp án câu hỏi củng cố (SGK trang 21):**<br>- Câu 1: Chọn các phương án đúng: **A, B, D, F**.<br>- Câu 2: Học sinh tự do nêu quan điểm cá nhân có giải thích hợp lý. |

### 2. Hoạt động 2.3: Một số lợi ích của Internet (8 phút)
a) Mục tiêu: Trình bày được các lợi ích nổi bật của Internet đối với học tập, giải trí, kinh doanh và xã hội; có ý thức bảo vệ sức khỏe khi sử dụng Internet.
b) Nội dung:
- Khám phá Hoạt động 3 SGK trang 21 và Hình minh họa trang 22:
![Hình minh họa Lợi ích của Internet](khbd-ill:hinh_loi_ich_internet)
- Phân tích 5 lợi ích cốt lõi:
  1) Trao đổi thông tin nhanh chóng, hiệu quả (email, chat, video call).
  2) Học tập và làm việc trực tuyến (học online, làm việc từ xa).
  3) Cung cấp nguồn tài liệu phong phú (kho tri thức số, thư viện mở).
  4) Cung cấp các tiện ích phục vụ đời sống (thanh toán điện tử, mua sắm online, đặt vé, dịch vụ công).
  5) Là phương tiện vui chơi, giải trí (nghe nhạc, xem phim, chơi game trí tuệ).
- Lưu ý sức khỏe: Không nên truy cập Internet liên tục trong nhiều giờ (ảnh hưởng thị lực, xương khớp, sinh hoạt).
- Trả lời câu hỏi củng cố trang 22 SGK.
c) Sản phẩm: Bảng phân loại lợi ích của Internet trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu hình minh họa đầu trang 22 SGK (các bạn học sinh trong phòng máy chia sẻ các hoạt động trên Internet: học tiếng Anh, xem phim nghe nhạc, tìm tư liệu nhóm, gửi thư cho bạn ở nước ngoài, bán sản phẩm giúp mẹ...).<br>- **GV:** Nêu câu hỏi trong Hoạt động 3:<br>1) Em thường truy cập Internet để làm những việc gì?<br>2) Theo em, Internet mang lại những lợi ích gì cho con người?<br>- **GV:** Chiếu lời nhắc nhở trong SGK: *"Không nên truy cập Internet liên tục trong nhiều giờ"*. Hỏi: "Vì sao chúng ta không nên ngồi mạng quá lâu?"<br>- **GV:** Cho học sinh trả lời câu hỏi củng cố trang 22: Chọn những việc em có thể làm với Internet.<br>- **HS:** Quan sát hình ảnh, đọc nội dung mục 3 và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo bàn trong 2 phút: Kể tên các lợi ích của Internet và chỉ ra tác hại nếu nghiện Internet.<br>- **GV:** Quan sát, định hướng học sinh cân bằng giữa học tập trên mạng với hoạt động thể chất ngoài trời.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện học sinh phát biểu.<br>- **HS:** Trình bày 5 lợi ích lớn của Internet; chỉ ra ngồi mạng quá lâu sẽ hại mắt, gù lưng, thiếu ngủ, giảm giao tiếp ngoài đời.<br>- **HS:** Trả lời câu hỏi củng cố trang 22: Chọn các phương án **a, b, d, e** (Phương án c - Đá bóng là hoạt động thể chất ngoài trời, không thể làm trực tiếp với Internet).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa kiến thức. Chốt lại 5 lợi ích cốt lõi của Internet trong khung cam trang 22 SGK và nhấn mạnh thông điệp sử dụng Internet an toàn, văn minh, điều độ. | **3. Một số lợi ích của Internet**<br><br>**a) Các lợi ích cốt lõi (Khung cam SGK trang 22):**<br>1) **Trao đổi thông tin nhanh chóng, hiệu quả:** Gửi thư điện tử, gọi điện thoại qua Internet, nhắn tin, họp trực tuyến với bạn bè khắp năm châu.<br>2) **Học tập và làm việc trực tuyến:** Học online, tra cứu bài tập, tìm tư liệu cho bài thuyết trình nhóm, làm việc từ xa tại nhà.<br>3) **Cung cấp nguồn tài liệu phong phú:** Tiếp cận kho tri thức khổng lồ của nhân loại (bách khoa toàn thư mở, sách điện tử, video bài giảng).<br>4) **Cung cấp các tiện ích phục vụ đời sống:** Đặt vé máy bay/tàu xe, mua sắm qua mạng, thanh toán tiền điện/nước, sử dụng dịch vụ công trực tuyến.<br>5) **Là phương tiện vui chơi, giải trí:** Nghe nhạc, xem phim chất lượng cao, chơi trò chơi điện tử trí tuệ.<br><br>**b) Lời khuyên an toàn sức khỏe:**<br>- **Không nên truy cập Internet liên tục trong nhiều giờ** để tránh các tác hại về mắt (cận thị), cột sống, suy giảm trí nhớ và thiếu hụt vận động thể chất.<br><br>**c) Đáp án câu hỏi củng cố (SGK trang 22):**<br>- Các việc em có thể làm với Internet: **a, b, d, e**.<br>*(Lưu ý: Việc c "Chơi đá bóng nâng cao sức khỏe" là hoạt động thể chất ngoài đời thực).* |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
a) Mục tiêu: Củng cố vững chắc định nghĩa, đặc điểm và cách thức kết nối Internet.
b) Nội dung: Giải bài tập Luyện tập 1 và 2 SGK trang 22; trả lời câu hỏi trắc nghiệm mở rộng.
c) Sản phẩm: Đáp án và lời giải thích chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu nội dung 2 bài tập mục Luyện tập SGK trang 22 lên màn hình:<br>+ **Bài 1:** Em hãy chọn phương án đúng. Internet là mạng:<br>Phương án A: Kết nối hai máy tính với nhau.<br>Phương án B: Kết nối các máy tính trong một nước.<br>Phương án C: Kết nối nhiều mạng máy tính trên phạm vi toàn cầu.<br>Phương án D: Kết nối các máy tính trong một thành phố.<br>+ **Bài 2:** Để máy tính kết nối được Internet ta cần làm gì?<br>- **GV:** Bổ sung câu trắc nghiệm nhanh:<br>+ **Câu 3:** "Không ai là chủ sở hữu của Internet" thể hiện đặc điểm nào của Internet? (A. Tính toàn cầu; B. Tính tương tác; C. Tính không chủ sở hữu; D. Tính dễ tiếp cận).<br>- **HS:** Nhận nhiệm vụ, suy nghĩ độc lập và ghi câu trả lời vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc cá nhân trong 2 phút.<br>- **GV:** Quan sát, hỗ trợ học sinh giải thích rõ lý do chọn phương án C ở Bài 1.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Gọi 2 học sinh trả lời miệng.<br>- **HS 1:** Trả lời Bài 1: Chọn **Phương án C** (Kết nối nhiều mạng máy tính trên phạm vi toàn cầu). Vì phương án A, B, D chỉ mô tả mạng cục bộ hoặc mạng diện rộng trong phạm vi hẹp.<br>- **HS 2:** Trả lời Bài 2: Để máy tính kết nối được Internet, ta cần **đăng ký với một nhà cung cấp dịch vụ Internet (ISP)** để được cấp quyền truy cập, kéo đường dây cáp mạng hoặc lắp đặt thiết bị phát Wifi (Modem/Router).<br>- **HS 3:** Trả lời Câu 3: Chọn **Phương án C** (Tính không chủ sở hữu).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt đáp án đúng và tuyên dương các học sinh nắm vững kiến thức bài học. | **Đáp án bài tập Luyện tập (SGK trang 22):**<br><br>**1. Bài 1 (SGK trang 22):**<br>- **Đáp án đúng: Phương án C** (Kết nối nhiều mạng máy tính trên phạm vi toàn cầu).<br>- Giải thích: Internet là mạng toàn cầu liên kết hàng triệu mạng máy tính lớn nhỏ trên khắp thế giới.<br><br>**2. Bài 2 (SGK trang 22):**<br>- **Để máy tính kết nối được Internet ta cần:**<br>+ Đăng ký hợp đồng sử dụng dịch vụ với một nhà cung cấp dịch vụ Internet (**ISP** - như Viettel, VNPT, FPT...).<br>+ Trang bị các thiết bị kết nối: Modem, Router Wifi hoặc dây cáp mạng nối từ thiết bị mạng đến máy tính.<br>+ Cài đặt phần mềm trình duyệt web để bắt đầu truy cập.<br><br>**3. Trắc nghiệm mở rộng:**<br>- Câu 3: **Phương án C. Tính không chủ sở hữu**. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
a) Mục tiêu: Vận dụng kiến thức bài học giải thích sự bùng nổ của Internet và liên hệ thực tế bản thân.
b) Nội dung: Giải bài tập Vận dụng 1 và 2 SGK trang 22.
c) Sản phẩm: Bản ghi ví dụ thực tế và lời giải thích ngắn gọn, thuyết phục của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ cho học sinh thực hiện 2 bài tập mục Vận dụng SGK trang 22:<br>+ **Bài 1:** Em hãy lấy ví dụ cho thấy Internet mang lại lợi ích cho việc học tập và giải trí của chính bản thân em.<br>+ **Bài 2:** Em hãy giải thích tại sao Internet lại được sử dụng rộng rãi và ngày càng phát triển trên toàn thế giới?<br>- **HS:** Nhận nhiệm vụ học tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và viết nhanh 2 ví dụ thực tế của bản thân vào vở nháp trong 2 phút.<br>- **GV:** Gợi ý học sinh dựa vào 4 đặc điểm chính (toàn cầu, tương tác, dễ tiếp cận, không chủ sở hữu) để giải thích câu 2.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện học sinh chia sẻ ví dụ thực tế.<br>- **HS:** Trình bày:<br>+ Ví dụ học tập: Tra cứu từ điển tiếng Anh trên Cambridge Dictionary, xem video thí nghiệm Vật lý/Hóa học trên YouTube, nộp bài tập cho thầy qua OLM/Azota.<br>+ Ví dụ giải trí: Nghe các bài hát thiếu nhi, xem phim hoạt hình tiếng Anh, chơi cờ vua online cùng bạn bè.<br>+ Giải thích sự phát triển: Do Internet có nguồn tri thức khổng lồ, chi phí sử dụng ngày càng rẻ, tốc độ ngày càng cao và thiết bị kết nối (điện thoại thông minh) rất phổ biến.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa câu trả lời. Nhấn mạnh: Internet là công cụ học tập tuyệt vời nếu chúng ta biết sử dụng thông minh và có chừng mực.<br>- **GV:** Dặn dò: Ôn tập lại toàn bộ kiến thức Chủ đề 1 và Chủ đề 2 (từ Bài 1 đến Bài 5) để chuẩn bị cho tiết Ôn tập (Tiết 9) tuần tới. | **Vận dụng và Hướng dẫn tự học:**<br><br>**1. Bài 1 (SGK trang 22):**<br>- **Ví dụ học tập:** Em sử dụng Internet để tìm kiếm các bài giảng toán trực tuyến, xem video hướng dẫn làm đồ thủ công, tra từ điển tiếng Anh và tham gia câu lạc bộ học tập trực tuyến.<br>- **Ví dụ giải trí:** Sau giờ học, em nghe các bản nhạc không lời thư giãn, xem các chương trình thế giới động vật trên YouTube Kids hoặc thi đấu cờ vua trực tuyến với bạn.<br><br>**2. Bài 2 (SGK trang 22):**<br>- **Internet được sử dụng rộng rãi và ngày càng phát triển vì:**<br>1) Đáp ứng toàn diện các nhu cầu thiết yếu của con người: làm việc, học tập, giao tiếp, kinh doanh, khám phá tri thức và giải trí.<br>2) Tính dễ tiếp cận và chi phí hợp lý: Hạ tầng viễn thông (cáp quang, mạng di động 4G/5G) phát triển mạnh mẽ; các thiết bị đầu cuối như điện thoại thông minh, máy tính bảng ngày càng đa dạng, giá thành rẻ.<br>3) Kho dữ liệu phong phú và cập nhật từng giây, mang lại hiệu quả vượt trội so với các phương thức truyền thống. |
