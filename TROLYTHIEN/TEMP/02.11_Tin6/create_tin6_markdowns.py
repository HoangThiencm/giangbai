# -*- coding: utf-8 -*-
"""
Script sinh 3 tệp KHBD Markdown môn Tin học 6 (Tuần 9 - 12):
Bài 01: Ôn tập kiểm tra đánh giá giữa HK1 (Tiết 9 - Tuần 9)
Bài 02: Kiểm tra giữa kì I (Tiết 10 - Tuần 10)
Bài 03: Bài 6 - Mạng thông tin toàn cầu (Tiết 11, 12 - Tuần 11, 12)
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "TROLYTHIEN/TEMP/02.11_Tin6"
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 01. ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (Tiết 9)
# -------------------------------------------------------------
md_01 = """Tiết 09 - ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức cốt lõi của hai chủ đề đầu năm học:
  + **Chủ đề 1: Máy tính và cộng đồng:** Phân biệt được thông tin, dữ liệu và vật mang tin (Bài 1); Các bước trong hoạt động xử lí thông tin của con người và máy tính: thu nhận, lưu trữ, xử lí, truyền (Bài 2); Khái niệm bit, dãy bit biểu diễn thông tin trong máy tính, các đơn vị đo dung lượng thông tin: $\\text{Byte, KB, MB, GB, TB}$ và quy tắc đổi đơn vị (Bài 3).
  + **Chủ đề 2: Mạng máy tính và Internet:** Khái niệm mạng máy tính, các thành phần chính của mạng (thiết bị đầu cuối, thiết bị kết nối, phần mềm mạng), phân biệt cáp mạng, Switch, Access Point (Bài 4); Khái niệm Internet, các đặc điểm chính và lợi ích to lớn của Internet đối với học tập và đời sống (Bài 5).
- Rèn luyện kĩ năng giải bài tập trắc nghiệm và câu hỏi tình huống thực tế chuẩn bị cho bài kiểm tra giữa học kì I.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ lại sơ đồ tư duy hệ thống kiến thức hai chủ đề, tích cực rà soát lại các nội dung chưa nắm vững.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải các bài toán quy đổi dung lượng nhớ trong nhóm học tập.

b) Năng lực đặc thù môn Tin học:
- Năng lực C (Ứng dụng công nghệ thông tin và truyền thông): Nhận biết các thiết bị mạng và biết cách kết nối máy tính vào mạng có dây hoặc không dây.
- Năng lực D (Hợp tác trong môi trường số): Sử dụng công cụ số tương tác để làm bài ôn tập trắc nghiệm.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm sơ đồ tư duy số (hoặc xem sơ đồ tư duy số hóa) và tham gia giải bài trắc nghiệm trực tuyến trên phần mềm Quizizz/Azota để tự đánh giá mức độ hiểu bài.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng trợ lý AI để tra cứu bảng so sánh chi tiết giữa Mạng máy tính nội bộ (LAN) và Mạng toàn cầu (Internet), từ đó củng cố khả năng phân tích khái niệm.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, nghiêm túc, cẩn trọng trong học tập và chuẩn bị kiểm tra đánh giá.
- Tinh thần vượt khó, chủ động hỗ trợ bạn bè trong nhóm ôn tập.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Tin học 6, KHBD, Sơ đồ tư duy Mindmap Ôn tập giữa HKI Tin học 6 (vector 300 DPI), hệ thống câu hỏi trắc nghiệm tương tác trên tivi/máy chiếu, phiếu học tập.
2. Học sinh: SGK Tin học 6, vở ghi, bảng con hoặc điện thoại/máy tính bảng kết nối phòng máy (nếu có).

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy và sự hứng khởi của học sinh qua trò chơi khởi động \"Vòng quay công nghệ\".
b) Nội dung: Trả lời nhanh 3 câu hỏi nhận diện nhanh thuật ngữ tin học.
c) Sản phẩm: Bảng ghi đáp án của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 3 câu hỏi khởi động nhanh:<br>  1. Đơn vị nhỏ nhất để đo dung lượng thông tin trong máy tính là gì?<br>  2. Thiết bị nào dùng để kết nối không dây cho các máy tính vào mạng?<br>  3. Đổi $1\\text{ KB}$ bằng bao nhiêu Byte?<br>- **HS:** Chuẩn bị bảng con ghi đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ trong 1 phút và giơ bảng kết quả.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ đọc to kết quả và giải thích: $1\\text{ KB} = 1024\\text{ Byte}$, không phải $1000\\text{ Byte}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ phản xạ của cả lớp, biểu dương tinh thần học tập và dẫn dắt vào bài ôn tập giữa kì. | **Đáp án khởi động:**<br>1. Bit (kí hiệu là b, nhận một trong hai giá trị 0 hoặc 1).<br>2. Điểm truy cập không dây (Access Point - Wi-Fi).<br>3. $1\\text{ KB} = 1024\\text{ Byte}$ ($2^{10}\\text{ Byte}$). |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (12 phút)
a) Mục tiêu: Tổng hợp toàn bộ mạng lưới kiến thức của Chủ đề 1 và Chủ đề 2 một cách logic, trực quan qua Sơ đồ tư duy.
b) Nội dung: Quan sát và phân tích Sơ đồ tư duy Mindmap Ôn tập giữa HKI Tin học 6; nhắc lại các kiến thức trọng tâm.

![Sơ đồ tư duy Ôn tập Giữa HK1 Tin học 6](khbd-ill:mindmap-tiet09)

c) Sản phẩm: Bảng tóm tắt hệ thống kiến thức trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Ôn tập giữa HKI lên màn hình lớn. Yêu cầu 4 nhóm học sinh thảo luận 4 nhánh:<br>  + Nhóm 1: Nhánh Thông tin và dữ liệu (vật mang tin, phân biệt thông tin và dữ liệu).<br>  + Nhóm 2: Nhánh Xử lí thông tin (4 bước: thu nhận, lưu trữ, xử lí, truyền).<br>  + Nhóm 3: Nhánh Biểu diễn và đo thông tin (Dãy bit, các bội số của Byte).<br>  + Nhóm 4: Nhánh Mạng máy tính và Internet (thành phần mạng, thiết bị mạng, đặc điểm Internet).<br>- **HS:** Đọc sơ đồ tư duy và chuẩn bị trình bày tóm tắt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm trong 4 phút.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 4 nhóm lần lượt đứng tại chỗ thuyết trình ngắn gọn từng nhánh.<br>- Cả lớp đối chiếu với sơ đồ tư duy trên màn hình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa toàn bộ nội dung, chốt lại bảng quy đổi đơn vị đo dung lượng nhớ. | **Hệ thống kiến thức trọng tâm:**<br>1. **Thông tin - Dữ liệu - Vật mang tin:**<br>- Thông tin là hiểu biết; Dữ liệu là văn bản, hình ảnh, âm thanh mang thông tin; Vật mang tin chứa dữ liệu.<br>2. **4 bước xử lí thông tin:**<br>Thu nhận $\\rightarrow$ Lưu trữ $\\rightarrow$ Xử lí $\\rightarrow$ Truyền thông tin.<br>3. **Biểu diễn thông tin & Đơn vị đo:**<br>- Mọi dữ liệu đều được chuyển thành dãy bit gồm hai số 0 và 1.<br>- Các đơn vị: $1\\text{ Byte} = 8\\text{ bit}$.<br>$1\\text{ KB} = 1024\\text{ B}$; $1\\text{ MB} = 1024\\text{ KB}$;<br>$1\\text{ GB} = 1024\\text{ MB}$; $1\\text{ TB} = 1024\\text{ GB}$.<br>4. **Mạng máy tính & Internet:**<br>- Mạng: Kết nối chia sẻ dữ liệu và dùng chung thiết bị.<br>- Thiết bị: Cáp mạng, Switch, Access Point, Modem.<br>- Internet: Mạng toàn cầu lớn nhất thế giới, không ai sở hữu. |

### Hoạt động 2.2: Luyện giải hệ thống câu hỏi trắc nghiệm và tình huống (20 phút)
a) Mục tiêu: Vận dụng kiến thức đã ôn tập để trả lời chính xác các câu hỏi trắc nghiệm và giải quyết các bài toán tình huống thực tế.
b) Nội dung: HS làm phiếu bài tập ôn tập gồm 6 câu trắc nghiệm và 2 bài tập tình huống thực tế.
c) Sản phẩm: Phiếu bài tập đã hoàn thành của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát phiếu học tập (hoặc hiển thị trên máy chiếu) gồm các câu hỏi tiêu biểu:<br>  + **Câu 1:** Tiếng trống trường báo giờ ra chơi là: A. Dữ liệu; B. Thông tin; C. Vật mang tin; D. Bộ xử lí.<br>  + **Câu 2:** Thẻ nhớ dung lượng $16\\text{ GB}$ có thể chứa được bao nhiêu bức ảnh dung lượng mỗi bức khoảng $4\\text{ MB}$?<br>  + **Câu 3:** Thiết bị nào sau đây là thiết bị đầu cuối: A. Switch; B. Máy in mạng; C. Cáp mạng; D. Access Point.<br>  + **Câu 4:** Trình bày sự khác nhau giữa mạng có dây và mạng không dây.<br>- **HS:** Nhận phiếu học tập và làm bài cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Độc lập suy nghĩ, tính toán bài tập quy đổi đơn vị.<br>- **GV:** Quan sát, gợi ý phương pháp đổi $16\\text{ GB} = 16 \\cdot 1024\\text{ MB} = 16384\\text{ MB}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 4 HS lên bảng trả lời và giải thích từng câu hỏi.<br>- Cả lớp lắng nghe, nhận xét và chấm chéo phiếu học tập.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt đáp án, nhấn mạnh cách phân biệt thiết bị đầu cuối (máy tính, máy in, camera) và thiết bị kết nối (Switch, Hub, Cáp mạng). | **Đáp án phiếu bài tập:**<br>- **Câu 1:** Chọn **B** (Thông tin: giúp em biết đã đến giờ ra chơi).<br>- **Câu 2:**<br>Đổi: $16\\text{ GB} = 16 \\cdot 1024 = 16384\\text{ MB}$.<br>Số bức ảnh thẻ nhớ có thể chứa là:<br>$16384 : 4 = 4096$ (bức ảnh).<br>- **Câu 3:** Chọn **B** (Máy in mạng là thiết bị đầu cuối).<br>- **Câu 4:**<br>+ Mạng có dây: Sử dụng dây cáp mạng để truyền dữ liệu, kết nối ổn định, tốc độ cao, nhưng phạm vi di chuyển hạn chế.<br>+ Mạng không dây: Sử dụng sóng điện từ (Wi-Fi, Bluetooth), tiện lợi khi di chuyển, lắp đặt dễ dàng nhưng có thể bị suy hao do vật cản. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức mạng máy tính vào việc tư vấn lắp đặt mạng mạng cho gia đình học sinh.
b) Nội dung: Bài toán tình huống: Nhà bạn Nam có 2 tầng, gồm 1 máy tính để bàn ở tầng 1, 2 điện thoại thông minh và 1 tivi thông minh ở tầng 2. Hãy tư vấn giúp Nam các thiết bị cần mua để kết nối Internet cho cả nhà.
c) Sản phẩm: Bảng đề xuất thiết bị của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đưa ra tình huống tư vấn mạng gia đình như trên.<br>- **HS:** Làm việc theo cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận, liệt kê thiết bị: Modem kết nối nhà mạng, bộ phát Wi-Fi (Access Point/Router Wi-Fi), cáp mạng nối máy để bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đại diện trình bày giải pháp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá tính khả thi và thẩm mỹ của phương án mạng. Dặn dò học sinh ôn tập kĩ theo đề cương để chuẩn bị làm bài kiểm tra giữa học kì I ở tiết sau. | **Tư vấn giải pháp mạng gia đình:**<br>1. Thiết bị kết nối Internet: Modem quang do nhà mạng cung cấp (thường tích hợp Wi-Fi đặt ở tầng 1).<br>2. Dây cáp mạng: Nối từ Modem vào máy tính để bàn ở tầng 1 để đường truyền ổn định nhất.<br>3. Bộ phát Wi-Fi phụ (hoặc thiết bị kích sóng Mesh Wi-Fi) đặt ở tầng 2 để phủ sóng mạnh mẽ cho tivi thông minh và điện thoại của gia đình. |
"""

# -------------------------------------------------------------
# 02. KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (Tiết 10)
# -------------------------------------------------------------
md_02 = """Tiết 10 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (TIN HỌC 6)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ đạt chuẩn kiến thức, kĩ năng của học sinh sau khi học xong hai chủ đề:
  + **Chủ đề 1: Máy tính và cộng đồng** (Bài 1, Bài 2, Bài 3).
  + **Chủ đề 2: Mạng máy tính và Internet** (Bài 4, Bài 5).
- Kiểm tra khả năng nhận biết, thông hiểu và vận dụng các kiến thức về: thông tin và dữ liệu, quá trình xử lí thông tin, biểu diễn thông tin bằng bit, các đơn vị đo dung lượng thông tin, các thành phần của mạng máy tính, vai trò và lợi ích của Internet.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác, nghiêm túc hoàn thành bài kiểm tra độc lập, không xem tài liệu, không trao đổi trong giờ kiểm tra.

b) Năng lực đặc thù môn Tin học:
- Năng lực giải quyết vấn đề với sự hỗ trợ của công nghệ: Vận dụng tư duy logic và kiến thức tin học để giải quyết các bài toán tính toán dung lượng và phân tích tình huống mạng.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS thực hiện bài kiểm tra trắc nghiệm kết hợp tự luận trên máy tính phòng máy hoặc hệ thống khảo thí số của nhà trường một cách thành thạo, đúng quy chế thi cử số.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.D1.1: HS có ý thức tự lực hoàn thành bài kiểm tra, trung thực học thuật, không lạm dụng các công cụ giải bài tập tự động nhằm rèn luyện năng lực tự tư duy cá nhân.***

## 3. Về phẩm chất
- Rèn luyện phẩm chất trung thực, cẩn thận, kỷ luật và tự trọng trong thi cử.
- Có ý thức tự đánh giá năng lực học tập của bản thân để có kế hoạch rèn luyện trong nửa sau học kì I.

# II. THIẾT BỊ VÀ ĐỀ KIỂM TRA

## 1. Hình thức kiểm tra
- Kết hợp Trắc nghiệm khách quan (70% - 7,0 điểm gồm 14 câu) và Tự luận (30% - 3,0 điểm gồm 2 câu).
- Thời gian làm bài: 45 phút.

## 2. Ma trận và Bản đặc tả đề kiểm tra giữa HKI
- **Chủ đề 1 (Máy tính và cộng đồng):** 60% tổng điểm (Nhận biết: 3 câu TN; Thông hiểu: 3 câu TN; Vận dụng: 1 câu Tự luận tính dung lượng).
- **Chủ đề 2 (Mạng máy tính và Internet):** 40% tổng điểm (Nhận biết: 4 câu TN; Thông hiểu: 4 câu TN; Vận dụng: 1 câu Tự luận tình huống mạng).

---

## 3. ĐỀ KIỂM TRA MẪU CHUẨN

### PHẦN I. TRẮC NGHIỆM KHÁCH QUAN (7,0 điểm - Mỗi câu 0,5 điểm)
*Khoanh tròn vào chữ cái đứng trước câu trả lời đúng nhất:*

**Câu 1 (NB):** Thông tin là gì?
A. Là các con số và văn bản ghi trên giấy.
B. Là những hiểu biết của con người về thế giới xung quanh và về chính bản thân mình.
C. Là các tín hiệu âm thanh và hình ảnh phát ra từ tivi.
D. Là những gì máy tính hiển thị trên màn hình.

**Câu 2 (NB):** Vật mang tin là gì?
A. Là người đưa tin tức.
B. Là phương tiện được dùng để lưu trữ và truyền đạt thông tin (như giấy, đĩa cứng, thẻ nhớ).
C. Là nguồn phát ra thông tin.
D. Là phần mềm trong máy tính.

**Câu 3 (NB):** Dãy bit là dãy chỉ gồm những kí hiệu nào?
A. Các chữ cái từ A đến Z.
B. Các số tự nhiên từ 0 đến 9.
C. Hai kí hiệu 0 và 1.
D. Các kí hiệu phép toán cộng, trừ, nhân, chia.

**Câu 4 (TH):** Quá trình xử lí thông tin của máy tính gồm những bước cơ bản nào?
A. Thu nhận $\\rightarrow$ Lưu trữ $\\rightarrow$ Xử lí $\\rightarrow$ Truyền thông tin.
B. Nhập dữ liệu $\\rightarrow$ In ra giấy $\\rightarrow$ Xóa dữ liệu.
C. Mở máy $\\rightarrow$ Tính toán $\\rightarrow$ Tắt máy.
D. Thu âm $\\rightarrow$ Chiếu hình ảnh $\\rightarrow$ Phát loa.

**Câu 5 (TH):** Đơn vị đo dung lượng thông tin nào sau đây là lớn nhất?
A. Byte (B).
B. Kilobyte (KB).
C. Gigabyte (GB).
D. Terabyte (TB).

**Câu 6 (TH):** Một tệp văn bản có dung lượng $2048\\text{ Byte}$ tương đương với bao nhiêu Kilobyte?
A. $1\\text{ KB}$.
B. $2\\text{ KB}$.
C. $4\\text{ KB}$.
D. $20\\text{ KB}$.

**Câu 7 (NB):** Mạng máy tính là gì?
A. Tập hợp các máy tính đứng độc lập trong một phòng học.
B. Tập hợp các máy tính được kết nối với nhau để truyền thông tin và chia sẻ tài nguyên.
C. Một chiếc máy tính hiện đại có kết nối máy in.
D. Mạng lưới các cửa hàng bán linh kiện máy tính.

**Câu 8 (NB):** Thiết bị nào sau đây là thiết bị kết nối trong mạng máy tính?
A. Máy tính xách tay (Laptop).
B. Máy tính để bàn (PC).
C. Bộ chuyển mạch (Switch).
D. Điện thoại thông minh (Smartphone).

**Câu 9 (NB):** Thiết bị nào sau đây cho phép các thiết bị kết nối vào mạng không dây (Wi-Fi)?
A. Điểm truy cập không dây (Access Point).
B. Bàn phím máy tính.
C. Chuột quang.
D. Dây cáp mạng UTP.

**Câu 10 (TH):** Mạng không dây thường sử dụng môi trường truyền dẫn nào để kết nối các máy tính?
A. Dây cáp đồng trục.
B. Sóng điện từ (sóng vô tuyến).
C. Dây cáp quang.
D. Dây cáp mạng xoắn đôi.

**Câu 11 (TH):** Phát biểu nào sau đây về Internet là **SAI**?
A. Internet là mạng kết nối hàng triệu máy tính trên toàn thế giới.
B. Internet thuộc quyền sở hữu độc quyền của một quốc gia hay một công ty duy nhất.
C. Người dùng có thể tìm kiếm thông tin, gửi email, học trực tuyến qua Internet.
D. Không có cơ quan nào hoàn toàn quản lý hay sở hữu toàn bộ hệ thống Internet toàn cầu.

**Câu 12 (TH):** Lợi ích nào sau đây **KHÔNG** phải là lợi ích chính của Internet?
A. Giúp người dùng liên lạc tức thời qua thư điện tử, tin nhắn, video call.
B. Giúp tra cứu kho tàng tri thức khổng lồ về mọi lĩnh vực khoa học, đời sống.
C. Tự động thay thế hoàn toàn con người trong việc suy nghĩ và làm việc nhà.
D. Cung cấp môi trường giải trí đa dạng như nghe nhạc, xem phim, chơi trò chơi trí tuệ.

**Câu 13 (NB):** Để kết nối máy in dùng chung cho tất cả các máy tính trong phòng thực hành, người ta sử dụng:
A. Mạng máy tính.
B. USB cắm rút thủ công từng máy.
C. Ổ đĩa mềm.
D. Đĩa CD.

**Câu 14 (TH):** Khẳng định nào sau đây là đúng khi so sánh thông tin và dữ liệu?
A. Dữ liệu là hiểu biết của con người, còn thông tin là văn bản ghi chép.
B. Thông tin chứa trong dữ liệu, từ dữ liệu con người rút ra được thông tin.
C. Thông tin và dữ liệu là hai khái niệm hoàn toàn giống nhau.
D. Dữ liệu không thể biến đổi thành thông tin.

---

### PHẦN II. TỰ LUẬN (3,0 điểm)

**Câu 1 (1,5 điểm):**
Một thẻ nhớ điện thoại có dung lượng lưu trữ là $32\\text{ GB}$.
a) Hãy đổi dung lượng của thẻ nhớ này ra đơn vị Megabyte (MB).
b) Giả sử mỗi bài hát MP3 có dung lượng trung bình khoảng $4\\text{ MB}$. Hỏi chiếc thẻ nhớ trên có thể chứa tối đa bao nhiêu bài hát như vậy?

**Câu 2 (1,5 điểm):**
Trường THCS Trần Phú vừa xây dựng một phòng máy vi tính mới gồm 30 máy tính để bàn cho học sinh học môn Tin học.
a) Em hãy kể tên các thiết bị cần thiết để kết nối 30 máy tính này thành một mạng máy tính nội bộ (mạng có dây).
b) Nêu 2 lợi ích cụ thể của mạng máy tính trong phòng máy đối với việc dạy và học của thầy cô giáo và học sinh.

---

# III. HƯỚNG DẪN CHẤM VÀ THANG ĐIỂM

## 1. Phần Trắc nghiệm (7,0 điểm - Mỗi câu đúng được 0,5 điểm)
- Câu 1: **B** | Câu 2: **B** | Câu 3: **C** | Câu 4: **A** | Câu 5: **D**
- Câu 6: **B** ($2048 : 1024 = 2\\text{ KB}$) | Câu 7: **B** | Câu 8: **C** | Câu 9: **A** | Câu 10: **B**
- Câu 11: **B** | Câu 12: **C** | Câu 13: **A** | Câu 14: **B**

## 2. Phần Tự luận (3,0 điểm)

| Câu | Nội dung đáp án chuẩn | Điểm |
| :---: | :--- | :---: |
| **Câu 1**<br>*(1,5 đ)* | **a)** Đổi dung lượng thẻ nhớ sang MB:<br>Vì $1\\text{ GB} = 1024\\text{ MB}$ nên:<br>Dung lượng thẻ nhớ là: $32 \\cdot 1024 = 32768\\text{ MB}$.<br><br>**b)** Số bài hát tối đa thẻ nhớ có thể chứa:<br>$32768 : 4 = 8192$ (bài hát).<br>Đáp số: $8192$ bài hát. | 0,75 đ<br><br>0,75 đ |
| **Câu 2**<br>*(1,5 đ)* | **a)** Các thiết bị cần thiết để kết nối mạng có dây cho phòng máy:<br>- 30 máy tính để bàn (thiết bị đầu cuối trang bị cổng mạng LAN).<br>- Bộ chuyển mạch (Switch) có số cổng phù hợp (ví dụ Switch 32 cổng hoặc 2 Switch 16 cổng, 24 cổng).<br>- Dây cáp mạng (cáp xoắn đôi bấm đầu cáp RJ45).<br>- Thiết bị Modem/Router kết nối đường truyền Internet từ nhà mạng.<br><br>**b)** 2 lợi ích của mạng phòng máy trong dạy và học:<br>- Giáo viên có thể truyền phát bài giảng, chia sẻ tệp học liệu, giao bài tập trực tiếp đến máy của từng học sinh.<br>- Dùng chung máy in phòng máy, học sinh nộp bài thực hành nhanh chóng qua thư mục chia sẻ mà không cần cắm USB. | 0,75 đ<br><br><br><br>0,75 đ |

---

# IV. TIẾN TRÌNH TỔ CHỨC KIỂM TRA TRÊN LỚP (45 phút)
1. **Ổn định tổ chức và phổ biến quy chế (3 phút):** GV ổn định chỗ ngồi, kiểm tra sĩ số, quán triệt học sinh nghiêm túc làm bài, không sử dụng tài liệu.
2. **Phát đề và học sinh làm bài (37 phút):** HS tập trung làm bài thi độc lập. GV bao quát phòng thi, không giải thích gì thêm về đề thi.
3. **Thu bài và nhận xét (5 phút):** Hết giờ làm bài, GV yêu cầu HS dừng bút, thu bài thi (hoặc lưu bài/nộp bài trên hệ thống số), đếm đủ số lượng bài thi và nhận xét tinh thần, thái độ làm bài của học sinh.
"""

# -------------------------------------------------------------
# 03. BÀI 6: MẠNG THÔNG TIN TOÀN CẦU (Tiết 11, 12)
# -------------------------------------------------------------
md_03 = """Tiết 11, 12 - BÀI 6: MẠNG THÔNG TIN TOÀN CẦU
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và hiểu được khái niệm **Mạng thông tin toàn cầu (World Wide Web - viết tắt là WWW)**: Là mạng lưới các website trên toàn thế giới được liên kết với nhau qua Internet.
- Phân biệt rõ các khái niệm:
  + **Siêu văn bản (Hypertext):** Là văn bản tích hợp nhiều dạng dữ liệu khác nhau (chữ, hình ảnh, âm thanh, video) và có chứa các liên kết trỏ tới các vị trí hoặc văn bản khác.
  + **Siêu liên kết (Hyperlink):** Là cầu nối liên kết dẫn người dùng chuyển từ trang web này sang trang web khác khi nhấp chuột vào.
  + **Trang web (Webpage):** Là một siêu văn bản được gán một địa chỉ truy cập trên Internet.
  + **Website:** Là một tập hợp các trang web liên quan được tổ chức dưới một địa chỉ chung (tên miền).
  + **Trang chủ (Homepage):** Là trang web đầu tiên xuất hiện khi truy cập vào một website.
  + **Địa chỉ website (URL):** Là địa chỉ định danh duy nhất của một website trên mạng (ví dụ: `https://thieunientienphong.vn`).
- Nhận biết và sử dụng được **Trình duyệt web (Web Browser)**: Là phần mềm ứng dụng dùng để xem các trang web trên Internet (Google Chrome, Microsoft Edge, Mozilla Firefox, Cốc Cốc, Safari...).
- Khai thác được các thành phần chính của cửa sổ trình duyệt: Thanh địa chỉ, các nút điều hướng (Back, Forward, Tải lại trang - Reload).
- Thực hành truy cập website, điều hướng qua các siêu liên kết để tìm đọc thông tin đa phương tiện.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác mở trình duyệt, nhập đúng địa chỉ website và tự khám phá nội dung thông tin theo yêu cầu.
- Giao tiếp và hợp tác: Làm việc nhóm đôi trong phòng máy tính, chia sẻ các địa chỉ website bổ ích và hướng dẫn bạn cách nhấp vào siêu liên kết.

b) Năng lực đặc thù môn Tin học:
- Năng lực C (Ứng dụng công nghệ thông tin và truyền thông): Sử dụng thành thạo trình duyệt web để khai thác thông tin học tập an toàn trên Internet.

c) Năng lực số (NLS):
- ***1.1.TC1a: HS sử dụng trình duyệt web mở các trang web giáo dục chính thống (như Cổng thông tin Bộ GD&ĐT `moet.gov.vn`, website Báo Thiếu niên Tiền phong), phân tích cấu trúc địa chỉ URL và nhận diện các siêu liên kết.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng công cụ AI để giải thích mối quan hệ giữa Internet và World Wide Web, phân biệt rõ vai trò của Trình duyệt web (Web Browser) và Máy tìm kiếm (Search Engine).***

## 3. Về phẩm chất
- Rèn luyện tính kỷ luật, ý thức sử dụng Internet an toàn, chỉ truy cập các website lành mạnh, phù hợp với lứa tuổi học sinh THCS.
- Tinh thần khám phá khoa học, ham học hỏi và tôn trọng bản quyền thông tin trên mạng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Tin học 6, KHBD, Sơ đồ tư duy Bài 6: Mạng thông tin toàn cầu (vector 300 DPI), phòng máy tính có kết nối mạng Internet, máy chiếu hoặc phần mềm quản lý phòng máy (NetOp School/LanSchool).
2. Học sinh: SGK Tin học 6, vở ghi bài, máy tính phòng thực hành có cài sẵn trình duyệt Google Chrome/Microsoft Edge.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: Xuất phát từ nhu cầu đọc báo, xem tin tức thời sự trên mạng để dẫn dắt học sinh đến khái niệm World Wide Web và trình duyệt web.
b) Nội dung: Quan sát một trang báo giấy và một trang báo điện tử trên màn chiếu, chỉ ra các điểm khác biệt.
c) Sản phẩm: Câu trả lời của học sinh về khả năng nhấp chuột chuyển trang và xem video trên báo điện tử.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 2 hình ảnh:<br>  + Hình 1: Một trang báo Thiếu niên Tiền phong in trên giấy.<br>  + Hình 2: Trang web điện tử của Báo Thiếu niên Tiền phong trên màn hình máy tính.<br>- **GV:** Đặt câu hỏi so sánh:<br>  1. Em có thể xem video hoặc nhấp chuột vào một dòng chữ để mở sang bài viết khác trên báo giấy được không?<br>  2. Nhờ hệ thống nào mà báo điện tử có thể chứa cả chữ, ảnh động, video và cho phép chuyển trang tức thì?<br>- **HS:** Quan sát và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi trong 2 phút.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời: Báo giấy chỉ xem được chữ và ảnh tĩnh. Báo điện tử có thể xem video, nghe nhạc và có các liên kết bấm vào để sang trang khác nhờ mạng World Wide Web.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt ý: Đó chính là sức mạnh của Mạng thông tin toàn cầu (World Wide Web) và Siêu văn bản. Hôm nay chúng ta cùng tìm hiểu Bài 6. | **Tình huống khởi động:**<br>- Báo giấy: Văn bản thông thường, cố định.<br>- Báo điện tử: Là siêu văn bản trên mạng World Wide Web (WWW), chứa thông tin đa phương tiện và các siêu liên kết cho phép di chuyển linh hoạt giữa các trang web. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (50 phút)
### Hoạt động 2.1: Thông tin trên Internet - World Wide Web, Siêu văn bản và Siêu liên kết (25 phút - Tiết 11)
a) Mục tiêu: Hiểu rõ khái niệm WWW, siêu văn bản, siêu liên kết, phân biệt trang web, website, trang chủ và địa chỉ URL.
b) Nội dung: Đọc thông tin mục 1 SGK trang 23-25; trả lời các câu hỏi Hoạt động 1 và Hoạt động 2 trong SGK.
c) Sản phẩm: Bảng ghi nhớ các khái niệm cốt lõi trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tổ chức cho HS tìm hiểu qua các câu hỏi gợi mở:<br>  1. World Wide Web (WWW) là gì? Do ai sáng lập?<br>  2. Thế nào là siêu văn bản (Hypertext) và siêu liên kết (Hyperlink)? Dấu hiệu nhận biết siêu liên kết khi rê chuột?<br>  3. Phân biệt trang web, website và trang chủ.<br>  4. Nêu một ví dụ về địa chỉ website.<br>- **HS:** Đọc SGK trang 23, 24 và trao đổi theo nhóm 4 người.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm, hoàn thành phiếu học tập số 1.<br>- **GV:** Quan sát, hướng dẫn các nhóm phân biệt giữa \"Internet\" (hạ tầng mạng) và \"WWW\" (dịch vụ thông tin chạy trên Internet).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện Nhóm 1 và Nhóm 2 lên bảng trình bày.<br>- HS nhóm khác nhận xét, nêu ví dụ địa chỉ website trường hoặc báo em biết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa kiến thức, ghi bảng mục 1. | **1. Thông tin trên Internet:**<br>- **World Wide Web (WWW):** Là mạng thông tin toàn cầu, hệ thống các website liên kết với nhau trên Internet. Được sáng lập bởi Tim Berners-Lee vào năm 1989.<br>- **Siêu văn bản (Hypertext):** Là văn bản tích hợp chữ, hình ảnh, âm thanh, video và các siêu liên kết.<br>- **Siêu liên kết (Hyperlink):** Đoạn văn bản hoặc hình ảnh đưa người dùng đến vị trí khác hoặc trang web khác khi nhấp chuột vào. Con trỏ chuột chuyển từ hình mũi tên sang hình bàn tay chỉ ngón trỏ.<br>- **Website:** Tập hợp các trang web liên quan được tổ chức dưới một địa chỉ chung.<br>- **Trang chủ (Homepage):** Trang đầu tiên mở ra khi truy cập vào website.<br>- **Địa chỉ website (URL):** Địa chỉ truy cập duy nhất, ví dụ: `https://thieunientienphong.vn`, `https://moet.gov.vn`. |

### Hoạt động 2.2: Trình duyệt web (Web Browser) (25 phút - Tiết 12)
a) Mục tiêu: Biết trình duyệt web là gì; kể tên các trình duyệt phổ biến; nắm vững các thành phần trên cửa sổ trình duyệt và thao tác cơ bản.
b) Nội dung: Tìm hiểu mục 2 SGK trang 25-26; quan sát giao diện Google Chrome/Microsoft Edge trên máy tính.
c) Sản phẩm: Thao tác mở trình duyệt, nhận biết thanh địa chỉ và các nút điều hướng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu giao diện màn hình máy tính có các biểu tượng trình duyệt: Chrome, Edge, Firefox, Cốc Cốc, Safari. Đặt câu hỏi:<br>  1. Trình duyệt web là gì?<br>  2. Hãy chỉ ra thanh địa chỉ, nút Back, nút Forward, nút Tải lại trang (Reload) trên màn hình.<br>  3. Để xem một trang web khi đã biết địa chỉ, em thực hiện các bước nào?<br>- **HS:** Quan sát và theo dõi trên máy tính cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mở trình duyệt Google Chrome trên máy tính của mình, quan sát thanh địa chỉ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên máy chủ thao tác chỉ rõ từng khu vực trên giao diện trình duyệt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại 3 bước cơ bản để truy cập trang web bằng trình duyệt. | **2. Trình duyệt web (Web Browser):**<br>- Khái niệm: Là phần mềm giúp người dùng truy cập và xem thông tin trên các trang web của World Wide Web.<br>- Các trình duyệt phổ biến: Google Chrome, Microsoft Edge, Mozilla Firefox, Apple Safari, Cốc Cốc.<br>- Các thành phần cơ bản của trình duyệt:<br>+ **Thanh địa chỉ:** Dùng để nhập địa chỉ website.<br>+ **Nút Back ($\\leftarrow$):** Quay lại trang web vừa xem trước đó.<br>+ **Nút Forward ($\\rightarrow$):** Đi tiếp đến trang web kế tiếp.<br>+ **Nút Tải lại trang ($\\circlearrowright$):** Tải lại nội dung trang hiện tại.<br>- Các bước truy cập website:<br>1. Khởi động trình duyệt web.<br>2. Nhập địa chỉ website vào thanh địa chỉ.<br>3. Nhấn phím Enter. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP VÀ THỰC HÀNH (23 phút)
### Hoạt động 3.1: Hệ thống hoá bài học qua Sơ đồ tư duy (8 phút)
a) Mục tiêu: Khắc sâu và củng cố toàn diện mối liên hệ giữa Internet, WWW, Siêu văn bản và Trình duyệt.
b) Nội dung: Quan sát Sơ đồ tư duy Bài 6: Mạng thông tin toàn cầu và trả lời câu hỏi trắc nghiệm nhanh.

![Sơ đồ tư duy Bài 6 Mạng thông tin toàn cầu](khbd-ill:mindmap-tiet11-12)

c) Sản phẩm: Câu trả lời phân biệt rõ ràng giữa Internet và WWW.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Bài 6: Mạng thông tin toàn cầu. Nêu câu hỏi:<br>  WWW và Internet có phải là một không? Vì sao?<br>- **HS:** Quan sát sơ đồ tư duy để tìm câu trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời: Internet là mạng kết nối toàn cầu về mặt vật lý, còn WWW là dịch vụ thông tin chia sẻ trên nền Internet. WWW là một phần của Internet.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương học sinh nắm bản chất kiến thức rất chuẩn xác. | **Ghi nhớ cốt lõi qua Sơ đồ tư duy:**<br>- Internet là mạng máy tính khổng lồ.<br>- World Wide Web (WWW) là dịch vụ chia sẻ thông tin dạng siêu văn bản hoạt động trên Internet.<br>- Trình duyệt web là công cụ phần mềm để đọc siêu văn bản trên WWW. |

### Hoạt động 3.2: Thực hành khám phá website (15 phút)
a) Mục tiêu: Vận dụng thực hành mở trình duyệt, truy cập website Báo Thiếu niên Tiền phong hoặc Vườn quốc gia Cúc Phương, nhấp vào siêu liên kết.
b) Nội dung: HS ngồi trước máy tính thực hiện Nhiệm vụ thực hành SGK trang 26-27.
c) Sản phẩm: Trang web được mở thành công trên màn hình máy tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ thực hành trên phòng máy:<br>  1. Khởi động trình duyệt Google Chrome.<br>  2. Nhập địa chỉ: `cucphuongtourism.com.vn` (hoặc `thieunientienphong.vn`) vào thanh địa chỉ rồi nhấn Enter.<br>  3. Rê chuột trên trang web để tìm 3 siêu liên kết (quan sát con trỏ chuột đổi hình bàn tay).<br>  4. Nhấp chuột vào một siêu liên kết để chuyển trang, sau đó nhấn nút Back để quay lại trang trước.<br>- **HS:** Lắng nghe và chuẩn bị thực hành.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác trên máy tính cá nhân.<br>- **GV:** Đi quan sát từng máy, hỗ trợ học sinh gõ đúng địa chỉ URL (không gõ thừa khoảng trắng).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- GV chọn ngẫu nhiên màn hình của 2 học sinh chiếu lên màn hình máy chủ để cả lớp quan sát thao tác.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tinh thần thực hành nghiêm túc, kỹ năng gõ URL và điều hướng thành thạo của học sinh. | **Kết quả thực hành:**<br>- Mở đúng website mục tiêu.<br>- Nhận diện chính xác siêu liên kết qua hình dạng con trỏ chuột.<br>- Sử dụng thành thạo nút Back ($\\leftarrow$) và Forward ($\\rightarrow$) trên thanh điều hướng. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
a) Mục tiêu: Vận dụng trình duyệt web để tra cứu thông tin thời tiết phục vụ kế hoạch sinh hoạt cá nhân an toàn.
b) Nội dung: Truy cập website Trung tâm Dự báo Khí tượng Thủy văn Quốc gia `nchmf.gov.vn` để xem dự báo thời tiết tỉnh/thành phố của em trong ngày mai.
c) Sản phẩm: Thông tin nhiệt độ, thời tiết ngày mai được ghi chép vào vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế: Ngày mai lớp dự kiến có buổi hoạt động ngoài trời. Em hãy dùng trình duyệt web truy cập trang web dự báo thời tiết quốc gia để xem ngày mai trời mưa hay nắng, nhiệt độ bao nhiêu độ C.<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhập địa chỉ website dự báo thời tiết và tìm kiếm thông tin địa phương.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy báo cáo thông tin thời tiết vừa tra cứu được.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt lại: Trình duyệt web và WWW là công cụ vô cùng hữu ích trong cuộc sống hàng ngày. Dặn dò HS chuẩn bị bài học tiếp theo: Bài 7 - Tìm kiếm thông tin trên Internet. | **Vận dụng thực tiễn:**<br>- Học sinh biết cách tự tra cứu thông tin thời tiết chính thống phục vụ sinh hoạt cá nhân.<br>- Có thói quen tiếp cận các website uy tín của cơ quan nhà nước để nhận thông tin đáng tin cậy. |
"""

tasks = [
    ("01_OnTapGiuaHK1_Tin6_Tiet09.md", md_01),
    ("02_KiemTraGiuaHK1_Tin6_Tiet10.md", md_02),
    ("03_Bai06_MangThongTinToanCau_Tiet11-12.md", md_03),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo Markdown: {filename}")

print(">>> HOÀN TẤT TẠO 3 TỆP MARKDOWN TIN HỌC 6! <<<")
