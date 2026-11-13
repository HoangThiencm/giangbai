# -*- coding: utf-8 -*-
"""
Script sinh tiếp các tệp KHBD Hình học 6 (Bài 11 đến Bài 15):
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Toan6"
os.makedirs(OUT_DIR, exist_ok=True)

# 11. Luyện tập chung Hình học Tiết 17
md_11 = """Tiết 17 - LUYỆN TẬP CHUNG (HÌNH HỌC TRỰC QUAN CHƯƠNG V)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và khắc sâu các kiến thức về tính đối xứng của hình phẳng: Hình có trục đối xứng và Hình có tâm đối xứng.
- Rèn luyện kĩ năng xác định số trục đối xứng, vẽ trục đối xứng và xác định tâm đối xứng của các hình phẳng, hoa văn, chữ cái và hình ảnh thực tế.
- Biết cách vẽ phần còn lại của một hình khi biết một nửa hình và trục đối xứng hoặc tâm đối xứng của nó.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát sơ đồ tư duy so sánh đối xứng trục và tâm, chủ động giải bài tập vẽ hình đối xứng.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp vẽ hình đối xứng qua giấy kẻ ô vuông trong nhóm bạn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh và chỉ rõ sự khác biệt bản chất giữa trục đối xứng (phép gấp) và tâm đối xứng (phép quay nửa vòng).
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo thước kẻ và compa để lấy điểm đối xứng.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm GeoGebra thực hành vẽ các hình đối xứng trên lưới ô vuông và dùng các công cụ kiểm tra tính đối xứng tự động.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để phân tích tính đối xứng trong cấu trúc tự nhiên của tinh thể tuyết và cánh hoa hồng.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác, khéo léo và thẩm mỹ trong từng nét vẽ.
- Ý thức làm đẹp không gian sống và tôn trọng các công trình kiến trúc đối xứng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Luyện tập chung Hình học Tiết 17 (vector 300 DPI), tivi/máy chiếu, giấy kẻ ô vuông.
2. Học sinh: SGK Toán 6, vở bài tập, thước kẻ, compa, bút màu.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy và sự nhanh nhạy qua trò chơi phân loại hình ảnh đối xứng.
b) Nội dung: Phân loại 4 hình ảnh trên màn chiếu vào hai nhóm: Nhóm có trục đối xứng và Nhóm có tâm đối xứng.
c) Sản phẩm: Bảng phân loại của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 hình ảnh: 1. Ngôi sao 5 cánh; 2. Cánh quạt 3 cánh; 3. Hình bình hành; 4. Hình chữ nhật. Yêu cầu HS phân loại.<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm và giơ bảng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ giải thích: Ngôi sao 5 cánh có 5 trục đối xứng (không có tâm); Cánh quạt 3 cánh không có tâm đối xứng quay nửa vòng; Hình bình hành có tâm đối xứng; Hình chữ nhật có cả hai.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương học sinh nhận biết rất chính xác, dẫn dắt vào bài luyện tập. | **Đáp án khởi động:**<br>- Trục đối xứng: Ngôi sao 5 cánh, Hình chữ nhật.<br>- Tâm đối xứng: Hình bình hành, Hình chữ nhật. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Tổng kết toàn diện các tính chất đối xứng trục và tâm qua Sơ đồ tư duy trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 17; củng cố các bảng so sánh.

![Sơ đồ tư duy Luyện tập chung Hình học Tiết 17](khbd-ill:mindmap-toan6-hinh-tiet17)

c) Sản phẩm: Bảng ghi nhớ so sánh trục và tâm đối xứng trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Tiết 17 lên màn hình. Yêu cầu HS nêu:<br>  + Các hình vừa có trục đối xứng, vừa có tâm đối xứng.<br>  + Cách xác định trục đối xứng và tâm đối xứng của hình chữ nhật, hình thoi.<br>- **HS:** Quan sát sơ đồ tư duy và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trình bày tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng tổng kết. | **Hệ thống kiến thức:**<br>1. Trục đối xứng: Gấp hình trùng khít.<br>2. Tâm đối xứng: Quay nửa vòng ($180^\\circ$) trùng khít.<br>3. Hình tròn, hình vuông, hình chữ nhật, hình thoi: Vừa có trục đối xứng, vừa có tâm đối xứng. |

### Hoạt động 2.2: Luyện giải bài tập SGK trang 108-109 (22 phút)
a) Mục tiêu: Thực hành vẽ phần còn lại của hình đối xứng trên lưới ô vuông; giải các bài tập 5.8, 5.9, 5.10 SGK.
b) Nội dung: Vẽ hình đối xứng qua trục và qua tâm trên vở kẻ ô vuông.
c) Sản phẩm: Hình vẽ chuẩn xác và đẹp mắt trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 5.8 và 5.10 SGK trang 108-109: Hoàn thành nửa còn lại của hình con bướm và chiếc bình hoa qua trục đối xứng cho trước.<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đếm ô vuông để lấy các điểm đối xứng qua trục thẳng đứng, sau đó nối các điểm lại.<br>- **GV:** Đi quan sát, hướng dẫn các em học sinh cách đếm số ô từ điểm đến trục đối xứng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng vẽ hoàn thiện hình.<br>- Cả lớp quan sát, nhận xét độ cân đối.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi nét vẽ chính xác và tính cẩn thận của học sinh. | **Kĩ thuật vẽ hình đối xứng trên lưới ô:**<br>1. Xác định các đỉnh cốt lõi của nửa hình đã cho.<br>2. Đếm khoảng cách từ mỗi đỉnh đến trục đối xứng $d$.<br>3. Lấy điểm đối xứng phía bên kia cách trục $d$ đúng bằng khoảng cách đó.<br>4. Nối các điểm tương ứng ta được hình hoàn chỉnh. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Nhận diện tính đối xứng trong trang trí gạch bông lát nền nhà hoặc gạch ốp tường thực tế.
b) Nội dung: Quan sát mẫu gạch bông hoa văn cổ điển và chỉ ra các yếu tố đối xứng.
c) Sản phẩm: Câu trả lời của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu viên gạch bông hình vuông có hoa văn trang trí ở giữa. Đặt câu hỏi: Viên gạch này có mấy trục đối xứng và có tâm đối xứng không?<br>- **HS:** Quan sát và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu: Viên gạch có 4 trục đối xứng và tâm đối xứng là giao điểm hai đường chéo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học. Dặn dò ôn tập chuẩn bị cho tiết Bài tập cuối chương V. | **Ứng dụng đời sống:**<br>- Hầu hết các mẫu gạch lát nền nghệ thuật đều được thiết kế dựa trên tính đối xứng trục và đối xứng tâm để khi lát ghép nhiều viên cạnh nhau sẽ tạo nên một bức tranh sàn nhà hài hòa, liên tục. |
"""

# 12. Bài tập cuối chương V (Tiết 18)
md_12 = """Tiết 18 - BÀI TẬP CUỐI CHƯƠNG V (TÍNH ĐỐI XỨNG CỦA HÌNH PHẲNG)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết toàn bộ kiến thức Chương V: Nhận biết hình có trục đối xứng, tìm trục đối xứng; Nhận biết hình có tâm đối xứng, tìm tâm đối xứng.
- Rèn luyện kĩ năng phân loại hình học phẳng theo tính chất đối xứng; vẽ hình đối xứng bằng tay và trên lưới ô vuông.
- Nâng cao năng lực ứng dụng tính đối xứng vào nghệ thuật cắt dán, thiết kế họa tiết và nhận diện các vẻ đẹp thiên nhiên.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức toàn chương qua sơ đồ tư duy cô đọng.
- Giao tiếp và hợp tác: Tự tin bảo vệ ý kiến phân loại hình học trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học; Năng lực thẩm mỹ toán học.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm đồ họa Paint hoặc GeoGebra để vẽ logo có tính đối xứng trục và tâm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS sử dụng AI để tìm kiếm các công trình kiến trúc mang phong cách đối xứng tiêu biểu trên thế giới (Lăng Taj Mahal, Nhà thờ Đức Bà Paris).***

## 3. Về phẩm chất
- Rèn luyện tư duy logic, sự tỉ mỉ, khéo léo và óc thẩm mỹ cao.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Tổng kết Chương V (vector 300 DPI), tivi/máy chiếu, bảng phụ trắc nghiệm.
2. Học sinh: SGK Toán 6, vở bài tập, thước kẻ, bút màu.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Khởi động qua câu đố nhận diện logo các hãng xe hơi nổi tiếng có tính đối xứng.
b) Nội dung: Quan sát logo các hãng xe (Mercedes-Benz, Toyota, Audi, BMW, Mitsubishi) và chỉ ra tính đối xứng.
c) Sản phẩm: Câu trả lời của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu hình ảnh 4 logo xe hơi: Mercedes (ngôi sao 3 cánh), Toyota, Audi (4 vòng tròn lồng nhau), Mitsubishi (3 viên kim cương). Hỏi tính đối xứng của từng logo.<br>- **HS:** Chuẩn bị trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét nhanh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu: Logo Mercedes có 3 trục đối xứng; Toyota có 1 trục đối xứng đứng; Audi vừa có 2 trục đối xứng vừa có tâm đối xứng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định tính đối xứng tạo nên sự sang trọng và cân đối trong thương hiệu, bắt đầu tiết học. | **Khởi động:**<br>Tính đối xứng được ứng dụng rộng rãi và đắc lực trong thiết kế biểu trưng, thương hiệu của các tập đoàn hàng đầu thế giới. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Giúp học sinh nắm vững toàn bộ kiến thức Chương V một cách tổng thể, logic qua Sơ đồ tư duy.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tổng kết Chương V; nhắc lại các nội dung cốt lõi.

![Sơ đồ tư duy Tổng kết Chương V](khbd-ill:mindmap-toan6-hinh-tiet18)

c) Sản phẩm: Bản ghi nhớ hệ thống kiến thức trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Tổng kết Chương V lên màn hình. Yêu cầu HS tóm tắt các nhánh kiến thức chính.<br>- **HS:** Quan sát và ghi nhận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm đôi trong 3 phút.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 HS phát biểu tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa sơ đồ, khen ngợi học sinh. | **Tổng kết Chương V:**<br>1. Trục đối xứng: Thao tác gấp hình.<br>2. Tâm đối xứng: Thao tác quay nửa vòng.<br>3. Bảng phân loại các hình học phẳng quen thuộc. |

### Hoạt động 2.2: Luyện giải bài tập tổng hợp SGK trang 110 (22 phút)
a) Mục tiêu: Vận dụng giải các bài tập 5.11, 5.12, 5.13, 5.14 SGK trang 110.
b) Nội dung: Nhận biết và vẽ trục, tâm đối xứng của các hình học và hoa văn.
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao các bài tập cuối chương SGK trang 110.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ hình và giải bài tập vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Sửa bài cẩn thận, khen ngợi tinh thần học tập tích cực. | **Bài 5.11 (SGK tr.110):**<br>- Hình có trục đối xứng: Hình a (ngôi sao biển), Hình c (con bướm).<br>- Hình có tâm đối xứng: Hình b (bánh lái tàu thủy). |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức đối xứng để sáng tạo mẫu hoa văn vải thổ cẩm đơn giản.
b) Nội dung: Thiết kế một mẫu họa tiết hình học trên giấy kẻ ô vuông có cả trục đối xứng và tâm đối xứng.
c) Sản phẩm: Bản vẽ họa tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS dùng bút màu vẽ một họa tiết hình thoi hoặc hình vuông có hoa văn đối xứng trên giấy kẻ ô.<br>- **HS:** Tự do sáng tạo.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành vẽ và tô màu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Trưng bày 3 bài vẽ đẹp nhất lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá tiết học, dặn dò chuẩn bị cho tiết Ôn tập cuối học kì I Hình học. | **Vận dụng sáng tạo:**<br>Học sinh thể hiện được tính thẩm mỹ và vận dụng tốt quy tắc lấy điểm đối xứng qua trục và qua tâm trên lưới ô vuông. |
"""

# 13. Ôn tập cuối học kì I Hình học (Tiết 19)
md_13 = """Tiết 19 - ÔN TẬP CUỐI HỌC KÌ I (HÌNH HỌC TRỰC QUAN 6)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Hình học trực quan của Học kì I gồm 2 chương:
  + **Chương IV: Các hình phẳng trong thực tiễn:** Tam giác đều, hình vuông, lục giác đều; Hình chữ nhật, hình thoi, hình bình hành, hình thang cân; Hệ thống công thức tính chu vi và diện tích của tất cả các hình đã học.
  + **Chương V: Tính đối xứng của hình phẳng trong tự nhiên:** Hình có trục đối xứng, hình có tâm đối xứng, số trục đối xứng và tâm đối xứng của các hình hình học phẳng.
- Rèn luyện kĩ năng nhận biết hình, phân biệt tính chất các tứ giác đặc biệt, vẽ hình chính xác và giải quyết thành thạo các bài toán tính chu vi, diện tích trong thực tiễn đời sống.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ lại sơ đồ tư duy hệ thống toàn bộ công thức chu vi, diện tích và tính đối xứng.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp chia hình để tính diện tích mảnh đất phức hợp trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh các công thức diện tích; lập luận giải thích tính đối xứng.
- Năng lực giải quyết vấn đề toán học: Phân tích bài toán thực tế (lát sân, làm vườn, chi phí vật liệu).

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm GeoGebra để dựng các hình tứ giác đã học và kiểm chứng công thức tính diện tích.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để tổng hợp các công thức chu vi diện tích hình học phẳng dưới dạng bảng so sánh thông minh.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác, thẩm mỹ và ý thức ứng dụng toán học vào đời sống.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Ôn tập cuối HKI Hình học (vector 300 DPI), tivi/máy chiếu, phiếu bài tập.
2. Học sinh: SGK Toán 6, vở bài tập, thước kẻ, êke, compa, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt trí nhớ về hệ thống công thức diện tích các hình qua trò chơi ghép thẻ công thức.
b) Nội dung: Nối tên hình ở Cột A với công thức diện tích ở Cột B.
c) Sản phẩm: Bảng nối chính xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu bảng nối nhanh công thức diện tích:<br>  1. Hình chữ nhật $\\rightarrow$ A. $S = a^2$<br>  2. Hình vuông $\\rightarrow$ B. $S = a \\cdot b$<br>  3. Hình bình hành $\\rightarrow$ C. $S = \\frac{1}{2} m \\cdot n$<br>  4. Hình thoi $\\rightarrow$ D. $S = a \\cdot h$<br>  5. Hình thang cân $\\rightarrow$ E. $S = \\frac{(a + b) \\cdot h}{2}$<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nối nhanh và giơ bảng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy đọc to: 1-B, 2-A, 3-D, 4-C, 5-E.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kiến thức khởi động, dẫn dắt vào bài ôn tập. | **Đáp án khởi động:**<br>1-B; 2-A; 3-D; 4-C; 5-E. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (12 phút)
a) Mục tiêu: Tổng hợp toàn bộ kiến thức Hình học Học kì I (Chương IV và Chương V) qua Sơ đồ tư duy trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Ôn tập cuối HKI Hình học; củng cố các công thức và tính chất.

![Sơ đồ tư duy Ôn tập Cuối HK1 Hình học](khbd-ill:mindmap-toan6-hinh-tiet19)

c) Sản phẩm: Bảng tổng kết toàn diện Hình học Học kì I trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Ôn tập cuối HKI Hình học lên màn hình. Yêu cầu HS nêu:<br>  + Các hình tứ giác và tính chất đường chéo của chúng.<br>  + Số trục đối xứng và tâm đối xứng của từng hình.<br>- **HS:** Quan sát sơ đồ tư duy và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm trình bày tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng kiến thức cốt lõi. | **Hệ thống kiến thức trọng tâm:**<br>1. **Hình vuông:** $C = 4a$; $S = a^2$; 4 trục đối xứng, có tâm đối xứng.<br>2. **Hình chữ nhật:** $C = 2(a+b)$; $S = a \\cdot b$; 2 trục đối xứng, có tâm đối xứng.<br>3. **Hình thoi:** $S = \\frac{1}{2} m \\cdot n$; 2 trục đối xứng, có tâm đối xứng.<br>4. **Hình bình hành:** $S = a \\cdot h$; không có trục đối xứng, có tâm đối xứng.<br>5. **Hình thang cân:** $S = \\frac{(a+b) \\cdot h}{2}$; 1 trục đối xứng, không có tâm đối xứng. |

### Hoạt động 2.2: Luyện giải bài tập phân dạng (20 phút)
a) Mục tiêu: Rèn luyện kĩ năng giải bài toán tính chu vi, diện tích và tính chi phí thực tế.
b) Nội dung: HS giải Bài tập 1 (tính diện tích bồn hoa hình thoi trong sân hình chữ nhật) và Bài tập 2 (tính số viên gạch lát nền).
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài tập ôn tập:<br>  + **Bài 1:** Một mảnh sân hình chữ nhật có chiều dài $15\\text{ m}$, chiều rộng $10\\text{ m}$. Ở chính giữa sân người ta làm một bồn hoa hình thoi có độ dài hai đường chéo là $6\\text{ m}$ và $4\\text{ m}$. Phần sân còn lại lát gạch chống trượt. Tính diện tích phần sân lát gạch.<br>  + **Bài 2:** Biết chi phí lát gạch là $120\\,000\\text{ đồng/m}^2$. Hỏi cần bao nhiêu tiền để lát phần sân trên?<br>- **HS:** Đọc đề và làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính diện tích sân chữ nhật, diện tích bồn hoa hình thoi, lấy hiệu diện tích rồi nhân đơn giá.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại phương pháp giải toán hình học thực tế. | **Bài giải:**<br>- Diện tích mảnh sân hình chữ nhật là:<br>$S_\\text{sân} = 15 \\cdot 10 = 150\\text{ m}^2$.<br>- Diện tích bồn hoa hình thoi là:<br>$S_\\text{hoa} = \\frac{1}{2} \\cdot 6 \\cdot 4 = 12\\text{ m}^2$.<br>- Diện tích phần sân lát gạch là:<br>$S = S_\\text{sân} - S_\\text{hoa} = 150 - 12 = 138\\text{ m}^2$.<br>- Tổng chi phí lát gạch là:<br>$138 \\cdot 120\\,000 = 16\\,560\\,000$ (đồng).<br>Đáp số: $138\\text{ m}^2$ và $16\\,560\\,000$ đồng. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức chu vi để tính chiều dài dây đèn led trang trí quanh bồn hoa hình thoi.
b) Nội dung: Tính chiều dài dây đèn trang trí bồn hoa hình thoi biết cạnh hình thoi là $3{,}6\\text{ m}$.
c) Sản phẩm: Lời giải của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán: Người ta muốn chăng dây đèn led quanh viền bồn hoa hình thoi ở Bài 1. Biết cạnh bồn hoa dài $3{,}6\\text{ m}$. Hỏi cần mua cuộn dây đèn dài tối thiểu bao nhiêu mét?<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính chu vi hình thoi: $C = 4 \\cdot 3{,}6 = 14{,}4\\text{ m}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trả lời: Cần tối thiểu $14{,}4\\text{ m}$ (hoặc mua cuộn $15\\text{ m}$).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học. Dặn dò ôn tập chuẩn bị kiểm tra cuối học kì I. | **Lời giải:**<br>Chu vi của bồn hoa hình thoi là:<br>$C = 4 \\cdot 3{,}6 = 14{,}4\\text{ m}$.<br>Đáp số: Cần mua dây đèn dài tối thiểu $14{,}4\\text{ m}$. |
"""

# 14. Kiểm tra cuối học kì I Hình học (Tiết 20)
md_14 = """Tiết 20 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (HÌNH HỌC TRỰC QUAN 6)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá kiến thức, kĩ năng của học sinh về phần Hình học trực quan Học kì I:
  + Chương IV: Nhận biết đặc điểm các hình tam giác đều, hình vuông, hình chữ nhật, hình thoi, hình bình hành, hình thang cân; Vận dụng công thức tính chu vi và diện tích vào giải toán thực tế.
  + Chương V: Nhận biết và chỉ ra trục đối xứng, tâm đối xứng của các hình phẳng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Nghiêm túc, tự giác, trung thực làm bài thi.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận hình học; Năng lực giải quyết vấn đề toán học.

c) Năng lực số (NLS) & AI:
- ***5.3.TC1a: HS thực hiện bài kiểm tra nghiêm túc, tuân thủ đúng quy chế thi cử.***
- ***6.D1.1: HS có ý thức tự lực tư duy làm bài, trung thực học thuật.***

## 3. Về phẩm chất
- Trung thực, cẩn thận, kỷ luật và tự trọng.

# II. CẤU TRÚC ĐỀ KIỂM TRA (KẾT HỢP TRẮC NGHIỆM VÀ TỰ LUẬN)

## 1. Hình thức
- Trắc nghiệm khách quan (50% - 5,0 điểm gồm 10 câu) và Tự luận (50% - 5,0 điểm gồm 2 câu).
- Thời gian làm bài: 45 phút.

---

## 2. ĐỀ KIỂM TRA MẪU CHUẨN

### PHẦN I. TRẮC NGHIỆM KHÁCH QUAN (5,0 điểm - Mỗi câu 0,5 điểm)
**Câu 1 (NB):** Tam giác đều có:
A. 3 cạnh bằng nhau và 3 góc bằng nhau.
B. 2 cạnh bằng nhau.
C. 1 góc vuông.
D. 3 cạnh có độ dài khác nhau.

**Câu 2 (NB):** Hình vuông cạnh $a$ có chu vi là:
A. $a^2$.
B. $2a$.
C. $4a$.
D. $4 + a$.

**Câu 3 (NB):** Diện tích của hình chữ nhật có chiều dài $8\\text{ cm}$ và chiều rộng $5\\text{ cm}$ là:
A. $13\\text{ cm}^2$.
B. $26\\text{ cm}^2$.
C. $40\\text{ cm}^2$.
D. $80\\text{ cm}^2$.

**Câu 4 (TH):** Hình thoi có độ dài hai đường chéo là $6\\text{ cm}$ và $8\\text{ cm}$ thì diện tích bằng:
A. $48\\text{ cm}^2$.
B. $24\\text{ cm}^2$.
C. $14\\text{ cm}^2$.
D. $28\\text{ cm}^2$.

**Câu 5 (TH):** Hình bình hành có cạnh đáy bằng $10\\text{ cm}$ và chiều cao tương ứng bằng $6\\text{ cm}$ thì diện tích bằng:
A. $60\\text{ cm}^2$.
B. $30\\text{ cm}^2$.
C. $16\\text{ cm}^2$.
D. $32\\text{ cm}^2$.

**Câu 6 (NB):** Hình nào sau đây **không có** trục đối xứng?
A. Hình thang cân.
B. Tam giác đều.
C. Hình bình hành.
D. Hình chữ nhật.

**Câu 7 (NB):** Hình nào sau đây **không có** tâm đối xứng?
A. Hình thoi.
B. Hình vuông.
C. Tam giác đều.
D. Hình tròn.

**Câu 8 (TH):** Hình vuông có mấy trục đối xứng?
A. 1.
B. 2.
C. 4.
D. Vô số.

**Câu 9 (TH):** Tâm đối xứng của đoạn thẳng $AB$ là:
A. Điểm $A$.
B. Điểm $B$.
C. Trung điểm của đoạn thẳng $AB$.
D. Một điểm bất kì trên đoạn thẳng.

**Câu 10 (VD):** Một mảnh đất hình thang cân có độ dài hai đáy là $8\\text{ m}$ và $12\\text{ m}$, chiều cao là $5\\text{ m}$. Diện tích mảnh đất là:
A. $50\\text{ m}^2$.
B. $100\\text{ m}^2$.
C. $25\\text{ m}^2$.
D. $48\\text{ m}^2$.

---

### PHẦN II. TỰ LUẬN (5,0 điểm)

**Câu 1 (2,0 điểm):**
Vẽ hình chữ nhật $ABCD$ có chiều dài $AB = 6\\text{ cm}$ và chiều rộng $BC = 4\\text{ cm}$. Hãy chỉ ra và vẽ tất cả các trục đối xứng của hình chữ nhật đó.

**Câu 2 (3,0 điểm):**
Một mảnh vườn hình chữ nhật có chiều dài $20\\text{ m}$, chiều rộng $12\\text{ m}$. Ở giữa mảnh vườn, người ta làm một lối đi bê tông hình bình hành có cạnh đáy là $2\\text{ m}$ và chiều cao bằng chiều rộng mảnh vườn (hình vẽ). Phần đất còn lại dùng để trồng rau.
a) Tính diện tích toàn bộ mảnh vườn.
b) Tính diện tích phần lối đi bê tông.
c) Tính diện tích phần đất trồng rau và chi phí mua hạt giống rau, biết mỗi mét vuông đất trồng rau tốn $15\\,000$ đồng tiền giống.

---

# III. HƯỚNG DẪN CHẤM VÀ THANG ĐIỂM

## 1. Trắc nghiệm (5,0 điểm - Mỗi câu 0,5 điểm)
- Câu 1: **A** | Câu 2: **C** | Câu 3: **C** | Câu 4: **B** | Câu 5: **A**
- Câu 6: **C** | Câu 7: **C** | Câu 8: **C** | Câu 9: **C** | Câu 10: **A**

## 2. Tự luận (5,0 điểm)

| Câu | Nội dung đáp án chuẩn | Điểm |
| :---: | :--- | :---: |
| **Câu 1**<br>*(2,0 đ)* | - Vẽ đúng hình chữ nhật kích thước $6\\text{ cm} \\times 4\\text{ cm}$.<br>- Nêu và vẽ đúng 2 trục đối xứng (hai đường thẳng đi qua trung điểm các cặp cạnh đối diện). | 1,0 đ<br><br>1,0 đ |
| **Câu 2**<br>*(3,0 đ)* | **a)** Diện tích toàn bộ mảnh vườn là:<br>$S_\\text{vườn} = 20 \\cdot 12 = 240\\text{ m}^2$.<br><br>**b)** Diện tích lối đi hình bình hành là:<br>$S_\\text{lối đi} = 2 \\cdot 12 = 24\\text{ m}^2$.<br><br>**c)** Diện tích phần đất trồng rau là:<br>$S_\\text{rau} = 240 - 24 = 216\\text{ m}^2$.<br>Chi phí mua hạt giống là:<br>$216 \\cdot 15\\,000 = 3\\,240\\,000$ (đồng).<br>Đáp số: $216\\text{ m}^2$ và $3\\,240\\,000$ đồng. | 1,0 đ<br><br>1,0 đ<br><br>0,5 đ<br><br>0,5 đ |
"""

# 15. HĐTN Tấm thiệp và GeoGebra (Tiết 21, 22)
md_15 = """Tiết 21, 22 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: TẤM THIỆP CỦA EM & VẼ HÌNH VỚI GEOGEBRA
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tiết 21 (STEM - Tấm thiệp của em): Vận dụng tính chất đối xứng trục và đối xứng tâm vào thực hành thiết kế, cắt dán tấm thiệp chúc mừng năm mới hoặc thiệp tri ân thầy cô, người thân.
- Tiết 22 (GeoGebra - Vẽ hình đơn giản): Làm quen và sử dụng các công cụ cơ bản của phần mềm hình học động GeoGebra để:
  + Dựng đoạn thẳng, đường thẳng, điểm.
  + Dựng tam giác đều, hình vuông, lục giác đều bằng công cụ Đa giác đều (Regular Polygon).
  + Kiểm tra tính chất độ dài cạnh, số đo góc bằng công cụ Đo khoảng cách (Distance) và Đo góc (Angle).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự lên ý tưởng thiết kế thiệp, tự mò mẫm các công cụ trên thanh bảng chọn của phần mềm GeoGebra.
- Giao tiếp và hợp tác: Hợp tác nhóm hoàn thành sản phẩm thiệp STEM và hỗ trợ nhau thực hành trên máy vi tính.

b) Năng lực đặc thù môn Toán:
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo phần mềm GeoGebra để mô phỏng hình học phẳng.
- Năng lực mô hình hóa toán học: Chuyển đổi các hình học lý thuyết thành sản phẩm thủ công hữu ích trong đời sống.

c) Năng lực số (NLS):
- ***3.1.TC1a: HS sử dụng phần mềm đồ họa số hoặc công cụ trình chiếu để thiết kế mẫu thiệp có tính đối xứng.***
- ***5.3.TC1a: HS sử dụng phần mềm GeoGebra để dựng chính xác tam giác đều, hình vuông và lục giác đều bằng công cụ đa giác đều; đo đạc và kiểm chứng các tính chất hình học.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để tạo các gợi ý lời chúc ý nghĩa viết vào thiệp mừng năm mới.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, óc thẩm mỹ, tình yêu thương gia đình, thầy cô qua sản phẩm tấm thiệp tự làm.
- Say mê công nghệ và yêu thích khám phá toán học ứng dụng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, máy tính có cài GeoGebra, máy chiếu, một số mẫu thiệp đối xứng mẫu.
2. Học sinh: Giấy bìa cứng A4 màu, kéo, keo dán, bút màu; phòng thực hành máy tính có cài GeoGebra.

# III. TIẾN TRÌNH DẠY HỌC

## A. TIẾT 21: STEM - LÀM TẤM THIỆP ĐỐI XỨNG (45 phút)
### 1. Khởi động và Giao nhiệm vụ (10 phút)
- **GV:** Trình chiếu một số mẫu thiệp chúc mừng năm mới có họa tiết hoa mai, hoa đào, bông tuyết đối xứng rất đẹp.
- **Yêu cầu:** Mỗi nhóm học sinh tự thiết kế 1 tấm thiệp gấp đôi có:
  + Trang bìa có ít nhất 1 họa tiết có trục đối xứng hoặc tâm đối xứng.
  + Bên trong có ghi lời chúc ý nghĩa.
- **HS:** Phân công nhiệm vụ trong nhóm.

### 2. Thực hành chế tạo sản phẩm (25 phút)
- **HS:** Gấp đôi giấy bìa, vẽ và cắt hoa văn đối xứng, dán trang trí lên bìa thiệp.
- **GV:** Đi quan sát, hướng dẫn các nhóm căn chỉnh vị trí trục đối xứng sao cho cân đối, hài hòa.

### 3. Trưng bày và Đánh giá (10 phút)
- Các nhóm trưng bày tấm thiệp lên bàn triển lãm của lớp.
- Đại diện nhóm thuyết minh về ý tưởng đối xứng trên tấm thiệp của mình.
- GV nhận xét, đánh giá cao sự khéo léo và tính sáng tạo của học sinh.

---

## B. TIẾT 22: THỰC HÀNH VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA (45 phút)
### 1. Khởi động và Khám phá giao diện GeoGebra (10 phút)
- **GV:** Hướng dẫn HS khởi động phần mềm GeoGebra. Giới thiệu:
  + Thanh công cụ (Toolbar) ở phía trên: Điểm (Point), Đoạn thẳng (Segment), Đa giác đều (Regular Polygon), Đo góc (Angle).
  + Vùng làm việc (Graphics view) có lưới tọa độ.
- **HS:** Di chuột làm quen với các biểu tượng công cụ.

### 2. Thực hành dựng hình đều bằng GeoGebra (25 phút)
- **Nhiệm vụ 1: Dựng tam giác đều:**
  + Chọn công cụ **Đa giác đều (Regular Polygon)**.
  + Nhấp chuột chọn 2 điểm $A$ và $B$ trên màn hình.
  + Hộp thoại hiện ra hỏi số đỉnh (Vertices), gõ số `3` rồi bấm OK. Ta được tam giác đều $ABC$.
- **Nhiệm vụ 2: Dựng hình vuông và lục giác đều:**
  + Tương tự, gõ số `4` để dựng hình vuông; gõ số `6` để dựng lục giác đều.
- **Nhiệm vụ 3: Kiểm tra độ dài và góc:**
  + Dùng công cụ **Distance or Length** nhấp vào các cạnh để xem độ dài.
  + Dùng công cụ **Angle** nhấp vào các góc để thấy số đo góc tam giác đều là $60^\\circ$, hình vuông là $90^\\circ$, lục giác đều là $120^\\circ$.
- **HS:** Tự lực thực hành trên máy vi tính cá nhân.

### 3. Tổng kết và Đánh giá học kì I (10 phút)
- GV biểu dương các em học sinh thao tác nhanh, vẽ hình chuẩn xác trên GeoGebra.
- Tổng kết toàn bộ học kì I môn Toán 6, dặn dò chuẩn bị sách vở cho Học kì II.
"""

tasks = [
    ("11_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet17.md", md_11),
    ("12_KHBD_Toan6_BaiTapCuoiChuong5_Tiet18.md", md_12),
    ("13_KHBD_Toan6_OnTapCuoiHK1_HinhHoc_Tiet19.md", md_13),
    ("14_KHBD_Toan6_KiemTraCuoiHK1_HinhHoc_Tiet20.md", md_14),
    ("15_KHBD_Toan6_HDTN_TamThiep_GeoGebra_Tiet21-22.md", md_15),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")

print(">>> HOÀN TẤT TẠO TOÀN BỘ 15 TỆP MARKDOWN TOÁN 6! <<<")
