# -*- coding: utf-8 -*-
import os

OUT_DIR = "tools/khbd_toan8_builder"
os.makedirs(OUT_DIR, exist_ok=True)

bai_04_content = r"""Tiết 14 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: CÔNG THỨC LÃI KÉP
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được ý nghĩa thực tiễn của bài toán gửi tiết kiệm và khái niệm "lãi kép" (tiền lãi kỳ này được gộp vào vốn gốc để tính lãi cho kỳ tiếp theo).
- Nhận biết và vận dụng được công thức tính lãi kép tổng quát: $A = P(1 + r)^n$ để tính số tiền nhận được sau $n$ kỳ hạn.
- Biết sử dụng công cụ bảng tính (Excel/Google Sheets) để tự động hóa việc tính toán, so sánh phương án tài chính và lập kế hoạch tiết kiệm cá nhân.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tìm hiểu thông tin lãi suất của các ngân hàng thương mại và chủ động thực hành tính toán.
- Giao tiếp và hợp tác: Làm việc nhóm hiệu quả trong việc lập bảng tính và thảo luận phương án tài chính.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Chuyển bài toán gửi tiết kiệm thực tế thành mô hình luỹ thừa của đa thức $P(1+r)^n$.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo máy tính cầm tay và bảng tính điện tử để xử lý dữ liệu tài chính.

c) Năng lực số (NLS):
- **5.3.TC2a:** HS dùng sáng tạo Excel để đổi mới quy trình tính lãi suất ngân hàng.
- **1.3.TC2a:** HS sắp xếp dữ liệu ngân hàng vào bảng để dễ truy xuất và so sánh.
- **5.2.TC2b:** HS lựa chọn giải pháp bảng tính để lập kế hoạch tài chính cá nhân.

d) Năng lực Trí tuệ Nhân tạo (AI):
- **8.B1.1:** HS nêu rủi ro lừa đảo tài chính từ các app tính lãi suất AI không chính thống.
- **8.D2.1:** HS mô tả UX cần thiết cho một ứng dụng AI tư vấn tiết kiệm tiền cho học sinh.

## 3. Về phẩm chất
- Rèn luyện phẩm chất chăm chỉ, cẩn trọng và ý thức tiết kiệm, quản lý tài chính cá nhân thông minh.
- Có trách nhiệm và nâng cao ý thức cảnh giác trước các cạm bẫy lừa đảo trên không gian mạng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng điện tử, máy tính có kết nối mạng và phần mềm bảng tính Excel/Google Sheets, máy chiếu/Tivi, tệp mẫu bảng tính lãi kép.
2. Học sinh: Máy tính cầm tay, điện thoại thông minh/máy tính bảng hoặc máy tính phòng Tin học, vở ghi, bảng phụ học tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (6 phút)
a) Mục tiêu: Kích thích sự tò mò của HS về sức mạnh của lãi kép và sự khác biệt giữa lãi đơn và lãi kép.
b) Nội dung: GV giới thiệu câu nói nổi tiếng của Albert Einstein: "Lãi kép là kỳ quan thứ 8 của thế giới. Ai hiểu nó sẽ kiếm được tiền, ai không hiểu sẽ phải trả giá vì nó".
c) Sản phẩm: Sự nhận biết ban đầu của HS về việc tiền lãi sinh thêm tiền lãi theo thời gian.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt tình huống: Nếu bạn có 10 triệu đồng gửi tiết kiệm với lãi suất 6%/năm. Sau 1 năm bạn nhận được bao nhiêu? Nếu không rút tiền lãi mà để nguyên cả gốc và lãi trong 5 năm, số tiền sẽ tăng lên như thế nào?<br>- **HS:** Lắng nghe tình huống và suy nghĩ cách tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính nhẩm tiền lãi sau năm thứ nhất: $10 \times 6\% = 0,6$ triệu (600.000 đồng). Cả gốc lẫn lãi là 10,6 triệu đồng.<br>- **HS:** Thảo luận: Năm thứ hai tiền lãi sẽ tính trên 10 triệu hay trên 10,6 triệu?<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện phát biểu: Nếu gửi theo hình thức lãi kép, năm thứ hai ngân hàng sẽ tính lãi trên toàn bộ số tiền 10,6 triệu đồng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định đó chính là cơ chế của "Lãi kép". Hôm nay chúng ta sẽ khám phá công thức toán học và trải nghiệm lập bảng tính Excel để quản lý tài chính. | **Tình huống mở đầu:**<br>- Gửi số tiền ban đầu: $10\,000\,000$ đồng với lãi suất $r = 6\%/\text{năm}$.<br>- Tiền nhận được sau 1 năm:<br>$10\,000\,000 + 10\,000\,000 \times 6\% = 10\,000\,000 \times (1 + 0,06) = 10\,600\,000$ đồng.<br>- Bản chất lãi kép: Tiền lãi của kỳ trước được tự động cộng vào vốn gốc để tính lãi cho kỳ tiếp theo. |

## B. HOẠT ĐỘNG 2: THỰC HÀNH TÍNH TOÁN & LẬP BẢNG TÍNH SỐ (25 phút)

### 1. Hoạt động 2.1: Xây dựng công thức toán học tổng quát (10 phút)
a) Mục tiêu: HS tự thiết lập được công thức tổng quát $A = P(1+r)^n$ bằng phương pháp quy nạp toán học.
b) Nội dung: Phân tích số tiền nhận được sau năm thứ nhất, thứ hai, thứ ba để tìm ra quy luật luỹ thừa.
![Mô hình Toán học & Bảng tính Excel: Công thức lãi kép](khbd-ill:hinh_hdtn_cong_thuc_lai_kep)
c) Sản phẩm: Công thức tổng quát $A = P(1+r)^n$ và ý nghĩa từng đại lượng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gọi $P$ là số tiền gốc ban đầu, $r$ là lãi suất mỗi kỳ hạn (dạng số thập phân).<br>Hãy tính số tiền nhận được sau kỳ 1 ($A_1$), kỳ 2 ($A_2$), kỳ 3 ($A_3$) và dự đoán sau $n$ kỳ ($A$).<br>- **HS:** Thảo luận nhóm đôi ghi ra bảng phụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện biến đổi đặt nhân tử chung:<br>+ Sau kỳ 1: $A_1 = P + P \cdot r = P(1 + r)$.<br>+ Sau kỳ 2: $A_2 = A_1 + A_1 \cdot r = A_1(1 + r) = P(1 + r)(1 + r) = P(1 + r)^2$.<br>+ Sau kỳ 3: $A_3 = A_2(1 + r) = P(1 + r)^3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Dự đoán sau $n$ kỳ hạn, số tiền nhận được là $A = P(1 + r)^n$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa công thức và giới thiệu ý nghĩa từng đại lượng. | **CÔNG THỨC LÃI KÉP TOÁN HỌC**<br><br>$$A = P(1 + r)^n$$<br><br>Trong đó:<br>- $P$ (Principal): Số tiền gốc ban đầu gửi vào ngân hàng.<br>- $r$ (Rate): Lãi suất của mỗi kỳ hạn gửi (tính theo số thập phân, ví dụ $6,5\% = 0,065$).<br>- $n$ (Periods): Số kỳ hạn gửi tiền (ví dụ $n$ năm hoặc $n$ tháng).<br>- $A$ (Amount): Số tiền nhận được (cả gốc lẫn lãi) sau $n$ kỳ hạn.<br>- Số tiền lãi nhận được là: $I = A - P$. |

### 2. Hoạt động 2.2: Trải nghiệm bảng tính Excel và Năng lực số (15 phút)
a) Mục tiêu: HS biết thiết lập bảng tính Excel/Google Sheets để tính lãi kép tự động và so sánh các phương án; tích hợp chỉ báo NLS 5.3.TC2a, 1.3.TC2a, 5.2.TC2b.
b) Nội dung: HS thao tác nhập liệu bảng tính, viết công thức tính toán và lập bảng so sánh các kỳ hạn gửi.
c) Sản phẩm: Bảng tính Excel hoàn chỉnh mô phỏng lãi kép của các nhóm học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu giao diện bảng tính mẫu lên màn hình và giao nhiệm vụ cho các nhóm:<br>+ Giả sử gia đình có số tiền tiết kiệm $P = 100\,000\,000$ đồng.<br>+ Khảo sát 3 mức lãi suất của ngân hàng: 1 năm ($r = 5\%$), 3 năm ($r = 6\%$), 5 năm ($r = 6,8\%$).<br>+ Hãy lập bảng tính Excel để tự động tính tổng số tiền $A$ và tiền lãi sau từng mốc thời gian.<br>- **HS:** Các nhóm mở ứng dụng Excel hoặc Google Sheets trên thiết bị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- ***(Tích hợp NLS 5.3.TC2a: HS dùng sáng tạo Excel để đổi mới quy trình tính lãi suất ngân hàng: thay vì tính tay từng bước tốn thời gian, HS nhập công thức tự động tại ô B4: `=B1*(1+B2)^B3` và kéo công thức tự động cập nhật kết quả tức thì).***<br>- ***(Tích hợp NLS 1.3.TC2a: HS sắp xếp dữ liệu ngân hàng vào bảng để dễ truy xuất và so sánh: thiết kế các cột Kỳ hạn, Lãi suất, Tiền gốc, Tổng tiền nhận được, Tiền lãi thu được để so sánh trực quan).***<br>- ***(Tích hợp NLS 5.2.TC2b: HS lựa chọn giải pháp bảng tính để lập kế hoạch tài chính cá nhân: nhập thử nghiệm số tiền tiết kiệm 500.000 đồng/tháng để tính sau 3 năm học THCS sẽ tiết kiệm được bao nhiêu tiền để mua máy vi tính phục vụ học tập).***<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện nhóm chiếu màn hình bảng tính của nhóm mình.<br>- **HS:** Thuyết minh bảng tính và nhận xét: Thời gian gửi càng dài thì tiền lãi sinh ra theo cấp số nhân càng lớn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kỹ năng ứng dụng công nghệ số của học sinh, tuyên dương các nhóm thiết kế bảng tính khoa học, thẩm mỹ. | **Mô hình bảng tính Excel chuẩn:**<br><br>| Ô | Tên đại lượng | Giá trị / Công thức Excel |<br>| :--- | :--- | :--- |<br>| **B1** | Vốn gốc ban đầu ($P$) | `100000000` (100 triệu) |<br>| **B2** | Lãi suất năm ($r$) | `6.5%` |<br>| **B3** | Số năm gửi ($n$) | `5` |<br>| **B4** | Tổng tiền nhận ($A$) | `=B1*(1+B2)^B3` $\approx 137\,008\,666$ đ |<br>| **B5** | Tiền lãi nhận được ($I$) | `=B4 - B1` $\approx 37\,008\,666$ đ |<br><br>**Bảng so sánh phương án gửi tiết kiệm:**<br>- Gửi 1 năm ($r=5\%$): $A = 105\,000\,000$ đ (Lãi 5 triệu).<br>- Gửi 3 năm ($r=6\%$): $A \approx 119\,101\,600$ đ (Lãi ~19,1 triệu).<br>- Gửi 5 năm ($r=6,8\%$): $A \approx 138\,949\,000$ đ (Lãi ~38,9 triệu). |

## C. HOẠT ĐỘNG 3: VẬN DỤNG & AN TOÀN SỐ AI (14 phút)
a) Mục tiêu: Nhận diện các nguy cơ lừa đảo tài chính số và đề xuất ý tưởng ứng dụng AI hỗ trợ quản lý tài chính; tích hợp chỉ báo Năng lực AI 8.B1.1 và 8.D2.1.
b) Nội dung: Thảo luận về các rủi ro từ app tài chính ảo trên mạng và thiết kế ý tưởng chatbot/ứng dụng AI tiết kiệm thông minh.
c) Sản phẩm: Bảng ý kiến phân tích rủi ro và mô tả tính năng ứng dụng AI của các nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu hai vấn đề thảo luận thực tế:<br>1) Hiện nay trên mạng xã hội xuất hiện nhiều quảng cáo "Đầu tư tài chính AI cam kết sinh lời 30% - 50%/tháng", "App kiếm tiền online tự động". Đó có phải là lãi kép chân chính không?<br>2) Nếu em là một lập trình viên thiết kế một ứng dụng AI tư vấn tiết kiệm tiền cho học sinh THCS, em muốn ứng dụng đó có những tính năng và giao diện trải nghiệm người dùng (UX) như thế nào?<br>- **HS:** Thảo luận nhóm sôi nổi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- ***(Tích hợp AI 8.B1.1: HS nêu rủi ro lừa đảo tài chính từ các app tính lãi suất AI không chính thống: nhận diện bản chất mô hình đa cấp Ponzi, các app mạo danh trí tuệ nhân tạo để lừa đảo chiếm đoạt tiền gửi với cam kết lãi suất phi thực tế; rèn luyện thói quen cảnh giác và không chia sẻ thông tin cá nhân/mật khẩu).***<br>- ***(Tích hợp AI 8.D2.1: HS mô tả trải nghiệm người dùng (UX) cần thiết cho một ứng dụng AI tư vấn tiết kiệm tiền cho học sinh: giao diện thân thiện, sinh động, có trợ lý ảo nhắc nhở chi tiêu hàng ngày, tính năng mô phỏng trực quan mục tiêu mua đồ dùng học tập, và bảo mật thông tin tài khoản tuyệt đối).***<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện các nhóm chia sẻ góc nhìn và ý tưởng thiết kế ứng dụng AI.<br>- **GV:** Lắng nghe và điều phối các ý kiến phản biện.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng kết thông điệp giáo dục tài chính số: Lãi kép là công cụ mạnh mẽ đòi hỏi sự kiên nhẫn và kỷ luật; luôn tỉnh táo bảo vệ bản thân trước các cạm bẫy lừa đảo công nghệ.<br>- **GV dặn dò:** Vận dụng bảng tính Excel để quản lý tiền tiêu vặt hoặc tiền mừng tuổi; chuẩn bị ôn tập cho tiết Ôn tập giữa học kì I. | **1. Nhận diện rủi ro lừa đảo tài chính số:**<br>- Bất kỳ ứng dụng nào cam kết lãi suất cao bất thường (trên 20%/tháng) đều là lừa đảo (mô hình Ponzi lấy tiền người sau trả người trước).<br>- Trí tuệ nhân tạo (AI) chân chính chỉ là công cụ tính toán và tối ưu hóa danh mục, không thể đảm bảo lợi nhuận phi lý không có rủi ro.<br><br>**2. Thiết kế ý tưởng Ứng dụng AI tư vấn tài chính:**<br>- **Giao diện (UI/UX):** Trực quan, gam màu tươi sáng, dễ thao tác trên điện thoại.<br>- **Tính năng AI cốt lõi:**<br>+ Phân tích thói quen chi tiêu thông qua nhật ký hàng ngày.<br>+ Dự báo thời gian hoàn thành mục tiêu tiết kiệm bằng công thức lãi kép.<br>+ Cảnh báo khi học sinh chi tiêu vượt hạn mức quy định.<br><br>**Dặn dò tự học:**<br>- Chia sẻ với gia đình về bài toán lãi kép và bảng tính Excel đã học.<br>- Ôn lại các kiến thức Chương I để chuẩn bị cho bài kiểm tra giữa kì. |
"""

with open(os.path.join(OUT_DIR, "BAI_04.md"), "w", encoding="utf-8") as f:
    f.write(bai_04_content.strip())
print("Saved BAI_04.md")
