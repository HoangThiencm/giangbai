# -*- coding: utf-8 -*-
"""
Script sinh 5 tệp KHBD Hình học 8 (Tuần 13 - 18):
- 13_KHBD_Toan8_HinhHoc_LuyenTapChung_Tiet25.md (Mindmap: mindmap_toan8_hinh_tiet25.png)
- 14_KHBD_Toan8_HinhHoc_BaiTapCuoiChuong4_Tiet26-27.md (Mindmap: mindmap_toan8_hinh_tiet26_27.png)
- 15_KHBD_Toan8_HinhHoc_HDTN_VeHinhGeoGebra_Tiet28.md
- 16_KHBD_Toan8_HinhHoc_OnTapCuoiHK1_Tiet29.md (Mindmap: mindmap_toan8_hinh_tiet29.png)
- 17_KHBD_Toan8_HinhHoc_KiemTraTraBaiCuoiHK1_Tiet30-31.md
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/10.11_Toan8"
os.makedirs(OUT_DIR, exist_ok=True)

# 13. Luyện tập chung (Hình học - Tiết 25)
md_13 = """Tiết 25 - LUYỆN TẬP CHUNG: ĐỊNH LÍ THALÈS VÀ TÍNH CHẤT ĐƯỜNG PHÂN GIÁC
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và khắc sâu các định lí hình học trọng tâm của Chương IV: Định lí Thalès thuận, đảo và hệ quả; Tính chất đường trung bình của tam giác; Tính chất đường phân giác trong và ngoài của tam giác.
- Vận dụng thành thạo các tỉ số đoạn thẳng để tính độ dài đoạn thẳng chưa biết và chứng minh hai đường thẳng song song.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức hình học qua sơ đồ tư duy.
- Giao tiếp và hợp tác: Tự tin trình bày lập luận chứng minh hình học trước lớp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Suy luận logic, phân tích giả thiết - kết luận.
- Năng lực mô hình hóa toán học: Ứng dụng định lí Thalès đo gián tiếp chiều cao vật thể hoặc khoảng cách không tới được.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Biết tìm kiếm và khai thác hình ảnh minh họa hình học trực quan từ nguồn học liệu số.***

## 3. Về phẩm chất
- Cẩn thận, tỉ mỉ, chính xác trong vẽ hình và lập luận từng bước suy diễn hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Chương IV, thước thẳng có chia vạch, compa, êke.
2. Học sinh: SGK Toán 8 tập 1, vở ghi, dụng cụ vẽ hình đầy đủ.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (4 phút)
a) Mục tiêu: Nhắc lại các tỉ lệ thức trong tam giác có đường thẳng song song một cạnh.
b) Nội dung: Trả lời câu hỏi: Nêu hệ quả của định lí Thalès trong $\\Delta ABC$ khi $MN \\parallel BC$ ($M \\in AB, N \\in AC$).
c) Sản phẩm: Tỉ số: $\\frac{AM}{AB} = \\frac{AN}{AC} = \\frac{MN}{BC}$.
d) Tổ chức thực hiện: GV gọi 1 HS nêu nhanh, cả lớp nhận xét và vào bài luyện tập.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (33 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức bằng sơ đồ tư duy (8 phút)
a) Mục tiêu: Kết nối các định lí trọng tâm Chương IV trên một sơ đồ logic trực quan.
b) Nội dung: Quan sát và phân tích Sơ đồ tư duy Chương IV: Định lí Thalès.
c) Sản phẩm: Sơ đồ tư duy được vẽ và khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy hệ thống hóa kiến thức Chương IV.<br>- **GV:** Đặt câu hỏi: Phân biệt khi nào dùng định lí Thalès thuận, khi nào dùng hệ quả của định lí Thalès?<br>- **HS:** Theo dõi sơ đồ và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại: Định lí thuận tính các đoạn trên hai cạnh bên; Hệ quả tính thêm cạnh song song thứ ba.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đại diện phân tích mối quan hệ giữa định lí Thalès và tính chất đường trung bình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại tính chất quan trọng: Đường trung bình là trường hợp đặc biệt tỉ số bằng $\\frac{1}{2}$. | **SƠ ĐỒ TƯ DUY CHƯƠNG IV: ĐỊNH LÍ THALÈS**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Luyện tập chung Định lí Thalès](khbd-ill:mindmap-toan8-hinh-tiet25)

### Hoạt động 2.2: Luyện tập tính độ dài và chứng minh song song (15 phút)
a) Mục tiêu: Thành thạo tính toán độ dài và dùng định lí Thalès đảo chứng minh song song.
b) Nội dung: Làm bài tập 4.14, 4.15 SGK trang 88.
c) Sản phẩm: Bài giải chi tiết và hình vẽ chính xác trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 4.14 SGK: Cho $\\Delta ABC$, $M \\in AB, N \\in AC$ sao cho $AM = 3\\text{ cm}, MB = 2\\text{ cm}, AN = 4{,}5\\text{ cm}, NC = 3\\text{ cm}$. Chứng minh $MN \\parallel BC$. Tính $BC$ biết $MN = 6\\text{ cm}$.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lập tỉ số $\\frac{AM}{MB}$ và $\\frac{AN}{NC}$, so sánh hai tỉ số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ hình và trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học: Khi tỉ số trên hai cạnh bằng nhau thì hai đường thẳng song song. | **Bài 4.14 (SGK tr.88):**<br>- Xét $\\Delta ABC$, ta có:<br>$\\frac{AM}{MB} = \\frac{3}{2}$; $\\frac{AN}{NC} = \\frac{4{,}5}{3} = \\frac{3}{2}$.<br>Suy ra $\\frac{AM}{MB} = \\frac{AN}{NC}$.<br>Theo định lí Thalès đảo, ta có $MN \\parallel BC$.<br>- Theo hệ quả định lí Thalès:<br>$\\frac{AM}{AB} = \\frac{MN}{BC} \\Rightarrow \\frac{3}{3 + 2} = \\frac{6}{BC} \\Rightarrow \\frac{3}{5} = \\frac{6}{BC}$.<br>Suy ra $BC = \\frac{5 \\cdot 6}{3} = 10\\text{ cm}$. |

### Hoạt động 2.3: Luyện tập tính chất đường phân giác của tam giác (10 phút)
a) Mục tiêu: Vận dụng tính chất đường phân giác để tính độ dài đoạn thẳng.
b) Nội dung: Làm bài tập 4.16 SGK trang 88.
c) Sản phẩm: Lời giải tính tỉ số đoạn thẳng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 4.16: Cho $\\Delta ABC$ có phân giác $AD$ ($D \\in BC$). Biết $AB = 6\\text{ cm}, AC = 9\\text{ cm}, BC = 10\\text{ cm}$. Tính $DB, DC$.<br>- **HS:** Vận dụng tỉ lệ thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết tỉ số $\\frac{DB}{DC} = \\frac{AB}{AC}$ và sử dụng tính chất dãy tỉ số bằng nhau.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS chữa trên bảng: $\\frac{DB}{6} = \\frac{DC}{9} = \\frac{DB + DC}{6 + 9} = \\frac{10}{15} = \\frac{2}{3}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa lời giải. | **Bài 4.16 (SGK tr.88):**<br>Vì $AD$ là phân giác của $\\widehat{BAC}$ nên:<br>$\\frac{DB}{DC} = \\frac{AB}{AC} = \\frac{6}{9} = \\frac{2}{3}$.<br>Theo tính chất dãy tỉ số bằng nhau:<br>$\\frac{DB}{2} = \\frac{DC}{3} = \\frac{DB + DC}{2 + 3} = \\frac{10}{5} = 2$.<br>Do đó: $DB = 2 \\cdot 2 = 4\\text{ cm}$; $DC = 3 \\cdot 2 = 6\\text{ cm}$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
- **Tích hợp NLS 1.2.TC2a:** GV giới thiệu hình ảnh minh họa phương pháp đo chiều cao của kim tự tháp của nhà toán học Thalès thời cổ đại qua việc đo bóng nắng trên mặt đất. Dặn dò học sinh chuẩn bị cho 2 tiết Bài tập cuối chương IV.
"""

# 14. Bài tập cuối chương IV (Hình học - Tiết 26, 27)
md_14 = """Tiết 26, 27 - BÀI TẬP CUỐI CHƯƠNG IV (ĐỊNH LÍ THALÈS)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập và củng cố toàn bộ các kiến thức của Chương IV: Định lí Thalès trong tam giác, Định lí đảo và hệ quả; Đường trung bình của tam giác; Tính chất đường phân giác trong tam giác.
- Nâng cao kĩ năng phân tích giả thiết, dựng thêm đường phụ (kẻ đường thẳng song song) để áp dụng định lí Thalès chứng minh các hệ thức hình học.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng kết các phương pháp chứng minh hai đường thẳng song song và tính độ dài đoạn thẳng.
- Giải quyết vấn đề và sáng tạo: Tìm tòi nhiều cách giải cho một bài toán hình học.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Chuỗi suy luận có căn cứ, rõ ràng từng bước.
- Năng lực giao tiếp toán học: Diễn đạt chuẩn xác các kí hiệu hình học, góc $\\widehat{ABC}$ và đoạn thẳng.

c) Năng lực số (NLS):
- Năng lực số: Biết khai thác các phần mềm hình học động để kiểm chứng các tính chất đồng dạng, tỉ lệ.

## 3. Về phẩm chất
- Rèn luyện tính kỷ luật, chính xác, cẩn thận trong từng nét vẽ và từng câu khẳng định hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy tổng hợp Chương IV, hệ thống bài tập trắc nghiệm và tự luận phân loại.
2. Học sinh: SGK Toán 8 tập 1, vở ghi, bộ thước kẻ, êke, compa, máy tính bỏ túi.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Tạo hứng thú và kết nối vào buổi ôn tập toàn diện Chương IV.
b) Nội dung: Trả lời nhanh 2 câu trắc nghiệm về định lí Thalès và tính chất đường trung bình.
c) Sản phẩm: Đáp án chọn đúng của học sinh.
d) Tổ chức thực hiện: GV chiếu câu hỏi, học sinh xung phong trả lời và nhận xét.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (75 phút)
### Hoạt động 2.1: Hệ thống hóa toàn bộ kiến thức Chương IV (15 phút)
a) Mục tiêu: Khắc sâu sơ đồ kiến thức tổng hợp Chương IV.
b) Nội dung: Trình chiếu và thuyết minh sơ đồ tư duy tổng kết Chương IV.
c) Sản phẩm: Bản ghi nhớ sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy tổng kết Chương IV.<br>- **GV:** Yêu cầu HS nêu các nhánh trọng tâm: 1. Định lí Thalès (thuận, đảo, hệ quả); 2. Đường trung bình của tam giác; 3. Tính chất đường phân giác.<br>- **HS:** Theo dõi và nhắc lại điều kiện áp dụng từng định lí.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi chép và hoàn thiện sơ đồ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy thuyết minh toàn bộ sơ đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Điểm chung của cả ba nội dung là đều dẫn đến các dãy tỉ số bằng nhau. | **SƠ ĐỒ TƯ DUY TỔNG KẾT CHƯƠNG IV: ĐỊNH LÍ THALÈS**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Bài tập cuối chương IV Hình học 8](khbd-ill:mindmap-toan8-hinh-tiet26_27)

### Hoạt động 2.2: Giải các bài tập trắc nghiệm cuối chương IV (15 phút)
a) Mục tiêu: Củng cố khả năng nhận biết nhanh các khẳng định đúng/sai về tỉ số đoạn thẳng.
b) Nội dung: Giải các câu trắc nghiệm 4.18, 4.19 SGK trang 89.
c) Sản phẩm: Đáp án giải thích của học sinh.
d) Tổ chức thực hiện:
- GV chiếu từng câu trắc nghiệm. HS giơ bảng chọn đáp án. GV gọi 1 em giải thích lý do chọn và chốt đáp án đúng.

### Hoạt động 2.3: Giải bài toán tự luận tổng hợp tính độ dài và chứng minh (45 phút)
a) Mục tiêu: Vận dụng phối hợp đường phân giác và định lí Thalès vào bài toán tổng hợp.
b) Nội dung: Giải bài tập 4.21, 4.22 SGK trang 89.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 4.21 SGK: Cho $\\Delta ABC$, phân giác $AD$. Kẻ $DE \\parallel AB$ ($E \\in AC$). Kẻ $EF \\parallel BC$ ($F \\in AB$). Chứng minh $AF = DE$.<br>- **HS:** Vẽ hình vào vở và phân tích giả thiết.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét: $AD$ là phân giác nên $\\frac{DB}{DC} = \\frac{AB}{AC}$. Kẻ song song nên áp dụng định lí Thalès.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày từng bước chứng minh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Uốn nắn cách trình bày tỉ số, khen ngợi học sinh đã kết hợp nhuần nhuyễn hai định lí. | **Bài 4.21 (SGK tr.89):**<br>- Vì $DE \\parallel AB$, theo định lí Thalès trong $\\Delta ABC$ ta có:<br>$\\frac{DE}{AB} = \\frac{CD}{CB}$.<br>- Vì $EF \\parallel BC$, theo định lí Thalès trong $\\Delta ABC$ ta có:<br>$\\frac{AF}{AB} = \\frac{AE}{AC}$.<br>- Mặt khác, vì $DE \\parallel AB$ nên $\\frac{AE}{AC} = \\frac{BD}{BC} = 1 - \\frac{CD}{CB}$.<br>- Vì $AD$ là phân giác nên kết hợp với tính chất hình thoi (hoặc tam giác cân $ADE$ có $\\widehat{EAD} = \\widehat{EDA}$ do so le trong), ta có $AE = ED$.<br>- Do đó $\\frac{AF}{AB} = \\frac{AE}{AC} = \\frac{DE}{AB} \\Rightarrow AF = DE$ (đpcm). |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (10 phút)
- **Vận dụng thực tế:** Bài toán đo khoảng cách hai bờ sông bằng cách cắm cọc tiêu và áp dụng định lí Thalès. GV hướng dẫn học sinh lập mô hình tam giác, đo các đoạn bờ sông và tính khoảng cách cần tìm. Dặn dò chuẩn bị cho tiết HĐTN: Vẽ hình đơn giản với phần mềm GeoGebra.
"""

# 15. HĐTN: Vẽ hình đơn giản với phần mềm GeoGebra (Tiết 28)
md_15 = """Tiết 28 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Làm quen và thành thạo các công cụ cơ bản của phần mềm hình học động GeoGebra: Vẽ điểm, đoạn thẳng, đường thẳng, tia, trung điểm, đường thẳng song song, đường thẳng vuông góc, đường phân giác của một góc.
- Thực hành vẽ các hình hình học cơ bản đã học trong Học kì I: Hình tam giác, hình thang cân, hình bình hành, hình chữ nhật, hình thoi, hình vuông.
- Kiểm nghiệm trực quan các định lí hình học (định lí Thalès, tính chất đường trung bình) khi kéo rê các đỉnh trên màn hình tương tác.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác các biểu tượng công cụ trên phần mềm GeoGebra.
- Giao tiếp và hợp tác: Chia sẻ tệp hình vẽ với bạn bè qua mạng máy tính nội bộ của trường.

b) Năng lực đặc thù môn Toán:
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo phần mềm GeoGebra để vẽ hình chính xác và khám phá tính chất hình học.
- Năng lực tư duy và lập luận toán học: Nhận biết tính bất biến của các tỉ số đoạn thẳng khi thay đổi vị trí các điểm.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Sử dụng phần mềm hình học động GeoGebra để tạo dựng, kiểm chứng và chia sẻ các đối tượng hình học tương tác.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, đam mê khám phá công nghệ và tính thẩm mĩ trong việc thiết kế hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn phần mềm GeoGebra (hoặc truy cập `geogebra.org/classic`), máy chiếu, bài giảng hướng dẫn từng thao tác.
2. Học sinh: Mỗi học sinh hoặc nhóm 2 học sinh một máy vi tính, vở ghi hướng dẫn lệnh GeoGebra.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Giới thiệu giao diện GeoGebra và tạo hứng thú khám phá vẽ hình động.
b) Nội dung: Quan sát GV thao tác kéo rê đỉnh một tam giác mà đường trung bình luôn song song và bằng một nửa cạnh đáy.
c) Sản phẩm: Sự hào hứng và chú ý của học sinh trước tính năng chuyển động của phần mềm.
d) Tổ chức thực hiện: GV biểu diễn mẫu trên màn chiếu, dẫn dắt học sinh khởi động phần mềm trên máy cá nhân.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC VÀ THỰC HÀNH (28 phút)
### Hoạt động 2.1: Hướng dẫn các công cụ dựng hình cơ bản trong GeoGebra (10 phút)
a) Mục tiêu: Nắm vững vị trí và cách dùng các nút công cụ: Điểm, Đoạn thẳng, Đường song song, Đường phân giác.
b) Nội dung: Đọc hướng dẫn SGK trang 115 - 117 và thực hiện theo từng bước của GV.
c) Sản phẩm: Các thao tác chuẩn xác trên thanh công cụ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu thanh công cụ: Nhóm công cụ Điểm, Đường thẳng, Đường vuông góc/song song, Phân giác, Đa giác.<br>- **GV:** Hướng dẫn vẽ đoạn thẳng $AB$, lấy trung điểm $M$ của $AB$.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tìm biểu tượng `Midpoint or Center` để xác định trung điểm tức thời.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS kiểm tra tọa độ và tính chuyển động của điểm $M$ khi kéo $A$ hoặc $B$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu: $M$ luôn là trung điểm của $AB$ dù kéo $A, B$ đi bất cứ vị trí nào. | **1. Các công cụ dựng hình cơ bản:**<br>- Điểm (`Point`): Nhấp chuột vào mặt phẳng tọa độ.<br>- Đoạn thẳng (`Segment`): Nhấp vào hai điểm mút.<br>- Trung điểm (`Midpoint`): Nhấp vào hai điểm hoặc một đoạn thẳng.<br>- Đường thẳng song song (`Parallel Line`): Chọn một điểm và chọn một đường thẳng cho trước.<br>- Đường phân giác (`Angle Bisector`): Chọn ba điểm tạo thành góc. |

### Hoạt động 2.2: Thực hành dựng hình và kiểm nghiệm định lí Thalès (18 phút)
a) Mục tiêu: Tự tay dựng một tam giác, kẻ đường thẳng song song một cạnh và hiển thị các tỉ số đoạn thẳng để kiểm nghiệm định lí Thalès.
b) Nội dung: Làm theo hướng dẫn mục 2, 3 SGK trang 118 - 119.
c) Sản phẩm: Tệp hình vẽ GeoGebra hiển thị chính xác tỉ số $\\frac{AM}{AB} = \\frac{AN}{AC}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS dựng $\\Delta ABC$. Lấy điểm $M$ trên $AB$. Dùng công cụ `Parallel Line` dựng đường thẳng qua $M$ song song với $BC$, cắt $AC$ tại $N$.<br>- **GV:** Hướng dẫn dùng ô nhập lệnh `Input` để tính: $t_1 = AM / AB$ và $t_2 = AN / AC$.<br>- **HS:** Thao tác trên máy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát giá trị của $t_1$ và $t_2$ trên màn hình.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS dùng chuột kéo điểm $A$ hoặc điểm $M$: Giá trị của $t_1$ và $t_2$ thay đổi nhưng luôn bằng nhau tại mọi thời điểm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá: Đây chính là bằng chứng trực quan sinh động minh chứng tính đúng đắn của định lí Thalès. | **2. Kiểm nghiệm định lí Thalès trên GeoGebra:**<br>- Dựng $\\Delta ABC$ và đường thẳng qua $M$ song song $BC$ cắt $AC$ tại $N$.<br>- Tính toán trong ô `Input`:<br>$t_1 = \\text{Distance}(A, M) / \\text{Distance}(A, B)$<br>$t_2 = \\text{Distance}(A, N) / \\text{Distance}(A, C)$<br>- Kết quả: $t_1 = t_2$ luôn không đổi khi kéo rê các đỉnh. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (7 phút)
- Học sinh thực hành dựng một hình chữ nhật hoặc hình bình hành bằng các công cụ đường thẳng song song và đường vuông góc. Lưu tệp vẽ với tên của mình.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
- **Tích hợp NLS 3.1.TC2a:** GV khuyến khích học sinh cài đặt ứng dụng GeoGebra Geometry trên điện thoại thông minh để tự luyện tập dựng các hình học trong chương trình. Dặn dò chuẩn bị cho tiết Ôn tập học kì I phần Hình học.
"""

# 16. Ôn tập học kì I (Hình học - Tiết 29)
md_16 = """Tiết 29 - ÔN TẬP HỌC KÌ I (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn diện các kiến thức Hình học cốt lõi đã học trong Học kì I môn Toán 8:
  + Chương III: Tứ giác, Định lí tổng các góc trong một tứ giác; Định nghĩa, tính chất và dấu hiệu nhận biết của hình thang cân, hình bình hành, hình chữ nhật, hình thoi, hình vuông.
  + Chương IV: Định lí Thalès trong tam giác (thuận, đảo, hệ quả); Đường trung bình của tam giác; Tính chất đường phân giác trong tam giác.
- Rèn luyện kỹ năng vẽ hình đúng chuẩn, ghi giả thiết - kết luận và xây dựng sơ đồ suy luận ngược để chứng minh bài toán hình học tổng hợp.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa mối quan hệ giữa các loại tứ giác đặc biệt và các định lí tỉ số đoạn thẳng.
- Giao tiếp và hợp tác: Trao đổi mạch lạc các bước chứng minh hình học trong nhóm bạn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát chuỗi dấu hiệu nhận biết từ tứ giác $\\rightarrow$ hình thang cân / hình bình hành $\\rightarrow$ hình chữ nhật / hình thoi $\\rightarrow$ hình vuông.
- Năng lực giải quyết vấn đề toán học: Phối hợp linh hoạt tính chất tứ giác và định lí Thalès.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Khai thác sơ đồ tư duy số và tài liệu ôn tập hình học trực tuyến để tự kiểm tra kiến thức.***

## 3. Về phẩm chất
- Trung thực, cẩn trọng, chính xác trong vẽ hình và trình bày lời giải chứng minh hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Ôn tập Hình học HKI, thước thẳng, êke, compa, phiếu học tập bài toán tổng hợp.
2. Học sinh: SGK Toán 8 tập 1, vở ghi, dụng cụ vẽ hình đầy đủ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (4 phút)
a) Mục tiêu: Tạo tâm thế tập trung và định hướng các nội dung ôn tập trọng tâm phần Hình học.
b) Nội dung: Trả lời nhanh: Cần thêm điều kiện gì để một hình bình hành trở thành hình chữ nhật? Trở thành hình thoi?
c) Sản phẩm: Câu trả lời: Có một góc vuông (hoặc hai đường chéo bằng nhau) $\\rightarrow$ hình chữ nhật; Có hai cạnh kề bằng nhau (hoặc hai đường chéo vuông góc) $\\rightarrow$ hình thoi.
d) Tổ chức thực hiện: GV gọi 1 HS nhắc lại, lớp nhận xét và dẫn dắt vào bài ôn tập.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (33 phút)
### Hoạt động 2.1: Khái quát mạng lưới kiến thức Hình học HKI qua Sơ đồ tư duy (8 phút)
a) Mục tiêu: Xâu chuỗi toàn bộ hệ thống tứ giác đặc biệt và định lí Thalès một cách hệ thống, khoa học.
b) Nội dung: Quan sát và phân tích Sơ đồ tư duy Ôn tập học kì I (Hình học).
c) Sản phẩm: Sơ đồ tư duy được vẽ và khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Ôn tập Hình học HKI.<br>- **GV:** Yêu cầu HS nêu 2 nhánh lớn: Nhánh 1: Các loại tứ giác đặc biệt (tính chất và dấu hiệu nhận biết); Nhánh 2: Định lí Thalès và đường phân giác.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại sơ đồ "gia phả" từ tứ giác chuyển dần thành hình vuông.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy tóm tắt các dấu hiệu nhận biết hình chữ nhật và hình thoi.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Hình vuông là hình vừa mang đầy đủ tính chất của hình chữ nhật vừa mang đầy đủ tính chất của hình thoi. | **SƠ ĐỒ TƯ DUY ÔN TẬP HỌC KÌ I: HÌNH HỌC 8**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Ôn tập Học kì I Hình học 8](khbd-ill:mindmap-toan8-hinh-tiet29)

### Hoạt động 2.2: Luyện tập bài toán tổng hợp về tứ giác và định lí Thalès (25 phút)
a) Mục tiêu: Vận dụng đồng thời tính chất hình bình hành, hình chữ nhật và đường trung bình vào một bài toán chứng minh.
b) Nội dung: Giải bài toán ôn tập tổng hợp trong đề cương.
c) Sản phẩm: Lời giải hoàn chỉnh và hình vẽ chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài toán: Cho $\\Delta ABC$ cân tại $A$, đường cao $AH$. Gọi $M$ là trung điểm của $AC$. Kẻ $Hx \\parallel AC$ cắt tia $AM$ tại $D$.<br>a) Chứng minh tứ giác $ADCH$ là hình chữ nhật.<br>b) Tìm điều kiện của $\\Delta ABC$ để $ADCH$ là hình vuông.<br>- **HS:** Vẽ hình và ghi GT - KL.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo cặp đôi: Xét tứ giác $ADCH$ có $Hx \\parallel AC$ và $M$ là trung điểm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày câu a: Chứng minh $ADCH$ có hai đường chéo cắt nhau tại trung điểm và có $\\widehat{AHC} = 90^\\circ$.<br>- 1 HS lên bảng làm câu b: Hình chữ nhật có hai cạnh kề $AH = HC$ hoặc $AC \\perp HD$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt phương pháp chứng minh hình chữ nhật và biện luận điều kiện để hình chữ nhật là hình vuông. | **Bài toán tổng hợp:**<br>**a) Chứng minh $ADCH$ là hình chữ nhật:**<br>- Vì $HD \\parallel AC$ và $M$ là trung điểm của $AC$, $HD$ cắt $AC$ tại $M$ nên tứ giác $ADCH$ là hình bình hành.<br>- Mặt khác, $AH \\perp BC$ tại $H$ nên $\\widehat{AHC} = 90^\\circ$.<br>- Hình bình hành $ADCH$ có một góc vuông $\\widehat{AHC} = 90^\\circ$ nên là hình chữ nhật.<br><br>**b) Điều kiện để $ADCH$ là hình vuông:**<br>- Hình chữ nhật $ADCH$ là hình vuông khi và chỉ khi $AH = HC$.<br>- Vì $\\Delta ABC$ cân tại $A$ có $AH$ là đường cao nên $AH$ cũng là trung tuyến, suy ra $HC = \\frac{1}{2} BC$.<br>- Do đó $AH = \\frac{1}{2} BC$, suy ra $\\Delta ABC$ vuông cân tại $A$.<br>- Vậy $\\Delta ABC$ vuông cân tại $A$ thì $ADCH$ là hình vuông. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
- **Tích hợp NLS 1.2.TC2a:** Hướng dẫn học sinh tra cứu các dạng bài tập hình học tổng hợp cuối HKI trên các trang web học tập trực tuyến uy tín (như Violympic, OLM) để luyện thêm kỹ năng vẽ hình phụ. Dặn dò học sinh chuẩn bị chu đáo đồ dùng (thước kẻ, compa, máy tính) cho buổi kiểm tra đánh giá cuối học kì I.
"""

# 17. Kiểm tra đánh giá cuối HKI & Trả bài (Hình học - Tiết 30, 31)
md_17 = """Tiết 30, 31 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I VÀ TRẢ BÀI (HÌNH HỌC)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ nắm vững các chuẩn kiến thức, kĩ năng Hình học kì I Toán 8: Các loại tứ giác đặc biệt; Định lí Thalès và tính chất đường phân giác trong tam giác.
- Phân loại học sinh, phát hiện các sai sót thường gặp trong vẽ hình và lập luận chứng minh hình học để có biện pháp bổ khuyết kịp thời trong Học kì II.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Nghiêm túc làm bài kiểm tra; tự giác kiểm tra và sửa lỗi sau khi nhận lại bài làm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học; Năng lực giải quyết vấn đề toán học: Diễn đạt mạch lạc, chứng minh chặt chẽ, vẽ hình chuẩn xác.

## 3. Về phẩm chất
- Trung thực, thẳng thắn, có ý thức vươn lên trong học tập môn Toán.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn, ma trận, bản đặc tả, đáp án và biểu điểm chi tiết môn Toán 8 (phần Hình học); Sổ điểm.
2. Học sinh: Dụng cụ vẽ hình (thước thẳng chia mm, êke, compa, thước đo góc), bút viết, giấy nháp.

# III. TIẾN TRÌNH DẠY HỌC
## A. TIẾT 30: KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (HÌNH HỌC) (45 phút)
### 1. Ổn định tổ chức và phát đề (3 phút)
- GV kiểm tra sĩ số, quán triệt quy chế phòng kiểm tra.
- GV phát đề kiểm tra cho từng học sinh.

### 2. Học sinh làm bài kiểm tra (40 phút)
- Học sinh làm bài kiểm tra nghiêm túc, vẽ hình rõ ràng, trình bày lập luận chặt chẽ.
- Giáo viên quan sát, giữ trật tự phòng thi.

### 3. Thu bài kiểm tra (2 phút)
- GV cho học sinh dừng bút, kiểm tra lại thông tin cá nhân.
- GV thu bài và kiểm đếm đủ số bài theo sĩ số.

## B. TIẾT 31: TRẢ BÀI KIỂM TRA HỌC KÌ I VÀ SỬA BÀI (HÌNH HỌC) (45 phút)
### Hoạt động 1: Nhận xét đánh giá kết quả kiểm tra phần Hình học (10 phút)
- **Ưu điểm:** Học sinh cơ bản vẽ hình đúng yêu cầu, nắm vững tính chất hình bình hành, hình chữ nhật và hệ quả định lí Thalès.
- **Tồn tại:** Một số em vẽ hình trường hợp đặc biệt (ví dụ tam giác thường vẽ thành tam giác cân hoặc vuông), quên ghi kí hiệu góc vuông, lập luận thiếu căn cứ chứng minh song song.
- GV thông báo kết quả chung: Điểm giỏi, khá, trung bình.

### Hoạt động 2: Hướng dẫn chữa đề chi tiết và rút kinh nghiệm (25 phút)
- GV vẽ hình chuẩn lên bảng và hướng dẫn chữa từng câu:
  + Chữa các câu trắc nghiệm hình học: Phân tích các dấu hiệu nhận biết dễ bị ngộ nhận.
  + Chữa câu tự luận chứng minh hình chữ nhật và tính độ dài đoạn thẳng theo định lí Thalès.
  + Hướng dẫn cách trình bày ngắn gọn, tránh thừa lời văn không cần thiết.
- Học sinh chữa các câu sai vào vở bài tập.

### Hoạt động 3: Đánh giá cá nhân và định hướng Học kì II (10 phút)
- GV trả bài kiểm tra cho từng học sinh kiểm tra lại điểm số.
- Giải đáp thắc mắc của học sinh.
- GV động viên học sinh phát huy các kết quả đạt được, đồng thời giao bài tập rèn luyện thêm kỹ năng chứng minh tam giác đồng dạng chuẩn bị cho chương trình Hình học kì II.
"""

tasks = [
    ("13_KHBD_Toan8_HinhHoc_LuyenTapChung_Tiet25.md", md_13),
    ("14_KHBD_Toan8_HinhHoc_BaiTapCuoiChuong4_Tiet26-27.md", md_14),
    ("15_KHBD_Toan8_HinhHoc_HDTN_VeHinhGeoGebra_Tiet28.md", md_15),
    ("16_KHBD_Toan8_HinhHoc_OnTapCuoiHK1_Tiet29.md", md_16),
    ("17_KHBD_Toan8_HinhHoc_KiemTraTraBaiCuoiHK1_Tiet30-31.md", md_17),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
