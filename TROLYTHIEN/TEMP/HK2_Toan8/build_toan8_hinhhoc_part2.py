# -*- coding: utf-8 -*-
"""
Script sinh 7 KHBD Chương X: Một số hình khối trong thực tiễn & Ôn tập cuối HK2 (Tiết 48 - 57) - Toán 8 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan8"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    # 39: Bài 38
    {
        "filename": "39_KHBD_Toan8_Bai38_HinhChopTamGiacDeu_Tiet48-49.md",
        "md": """TIẾT 48, 49 - BÀI 38: HÌNH CHÓP TAM GIÁC ĐỀU
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết các yếu tố cơ bản của hình chóp tam giác đều: Đỉnh, cạnh bên, mặt bên (là các tam giác cân bằng nhau), cạnh đáy, mặt đáy (là tam giác đều), chiều cao (đoạn nối đỉnh với trọng tâm tam giác đáy), trung đoạn (chiều cao của mặt bên).
- Nhận biết hình khai triển trên mặt phẳng của hình chóp tam giác đều.
- Nắm vững và vận dụng công thức tính diện tích xung quanh: $S_{xq} = p \\cdot d$ (trong đó $p$ là nửa chu vi đáy, $d$ là độ dài trung đoạn) hoặc tổng diện tích ba mặt bên.
- Nắm vững và vận dụng công thức tính thể tích của hình chóp tam giác đều: $V = \\frac{1}{3} S_{đáy} \\cdot h$ (trong đó $S_{đáy}$ là diện tích tam giác đều ở đáy, $h$ là chiều cao hình chóp).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự gấp dán mô hình hình chóp tam giác đều từ tấm bìa khai triển phẳng.
- Giao tiếp và hợp tác: Cùng nhóm đo đạc và tính toán diện tích xung quanh, thể tích các vật thể có dạng hình chóp tam giác đều.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Tưởng tượng không gian, phân biệt rõ trung đoạn $d$ của mặt bên và chiều cao $h$ của hình chóp.
- Năng lực mô hình hoá toán học: Tính lượng giấy bìa cần dùng làm hộp quà hình chóp tam giác đều.

c) Năng lực số (NLS):
- ***3.1.TC2a: HS chỉ ra cách tạo và chỉnh sửa các khối chóp 3D trên máy; 5.2.TC2b: HS chọn mô phỏng 3D giải quyết nhu cầu quan sát hình khai triển; 1.3.TC2a: HS sắp xếp dữ liệu kích thước vào bảng tính tự động tính diện tích.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS hiểu cách AI xử lý dữ liệu 3D để "nhìn" thấy các mặt và đỉnh của hình chóp; 8.D1.1: HS xác định vấn đề tính diện tích mái nhà hình chóp có thể dùng AI hỗ trợ tính toán; 8.B2.1: HS thực hiện bảo vệ dữ liệu khi tải ảnh các công trình thực tế lên hệ thống AI nhận diện.***

## 3. Về phẩm chất
- Say mê khám phá các hình khối không gian trong thế giới thực tế và kiến trúc.
- Cẩn thận, khéo léo trong vẽ hình không gian và gấp mô hình bìa.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, mô hình hình chóp tam giác đều bằng nhựa trong, mô hình khai triển bằng bìa, máy chiếu mô phỏng không gian 3D.
2. Học sinh: SGK, vở ghi, kéo, thước kẻ, bìa cứng để gấp hình, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích thích sự tò mò của học sinh qua hình ảnh hộp quà hoặc lều cắm trại hình chóp tam giác đều.
b) Nội dung: Quan sát hình ảnh kim tự tháp mini bằng pha lê hoặc chiếc bánh ú, lều tam giác và nhận xét về số mặt, hình dạng các mặt.
c) Sản phẩm: HS chỉ ra mặt đáy là hình tam giác, các mặt xung quanh là các hình tam giác chung đỉnh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho HS quan sát mô hình lều trại có đáy tam giác đều và các mặt bên là tam giác cân chụm lại tại một đỉnh. Giới thiệu tên gọi khối hình.<br>- **HS:** Quan sát và liên hệ thực tế.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đếm số đỉnh, số mặt bên, hình dạng đáy.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đáy là tam giác đều, 3 mặt bên là các tam giác cân bằng nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khối hình đó gọi là hình chóp tam giác đều. | Hình ảnh thực tế: Khối chóp tam giác đều trong đời sống (lều trại, khối rubik tam giác). |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Các yếu tố của hình chóp tam giác đều (35 phút)
a) Mục tiêu: Nhận biết đỉnh, cạnh bên, mặt bên, cạnh đáy, mặt đáy, chiều cao và trung đoạn.
b) Nội dung: Mô tả cấu tạo hình học không gian của hình chóp tam giác đều $S.ABC$.
c) Sản phẩm: Hình vẽ chuẩn trong vở và bảng phân biệt các yếu tố hình học.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vẽ hình chóp tam giác đều $S.ABC$ lên bảng. Giới thiệu:<br>- Đỉnh: $S$.<br>- Mặt đáy: Tam giác đều $ABC$.<br>- Các mặt bên: Các tam giác cân bằng nhau $SAB, SBC, SCA$.<br>- Chiều cao: Đoạn nối đỉnh $S$ với trọng tâm $O$ của đáy ($SO \\perp (ABC)$).<br>- Trung đoạn: Chiều cao kẻ từ đỉnh của một mặt bên (ví dụ $SI \\perp BC$).<br>- **HS:** Lắng nghe và vẽ hình theo nét đứt, nét liền.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chỉ ra trung đoạn trên từng mặt bên.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Hình chóp tam giác đều có $4$ mặt, $4$ đỉnh và $6$ cạnh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Cần phân biệt rõ chiều cao hình chóp ($SO$) và trung đoạn của mặt bên ($SI$). | **1. Các yếu tố của hình chóp tam giác đều $S.ABC$:**<br>- Đỉnh: $S$.<br>- Mặt đáy: Tam giác đều $ABC$.<br>- Các mặt bên: Các tam giác cân bằng nhau ($SAB, SBC, SCA$).<br>- Các cạnh bên bằng nhau: $SA = SB = SC$.<br>- Chiều cao: $h = SO$ (với $O$ là trọng tâm đáy).<br>- Trung đoạn: $d = SI$ (với $I$ là trung điểm cạnh đáy $BC$). |

### Hoạt động 2.2: Diện tích xung quanh và Thể tích của hình chóp tam giác đều (30 phút)
a) Mục tiêu: Nắm vững và áp dụng công thức $S_{xq} = p \\cdot d$ và $V = \\frac{1}{3} S_{đáy} \\cdot h$.
b) Nội dung: Xây dựng công thức tính diện tích xung quanh qua khai triển phẳng và công thức thể tích.
c) Sản phẩm: Vở ghi bài công thức và bài tập tính $S_{xq}, V$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn:<br>- Diện tích xung quanh là tổng diện tích 3 mặt bên: $S_{xq} = 3 \\cdot \\left(\\frac{1}{2} a \\cdot d\\right) = \\frac{3a}{2} \\cdot d = p \\cdot d$ (với $p$ là nửa chu vi đáy).<br>- Thể tích hình chóp bằng một phần ba diện tích đáy nhân với chiều cao: $V = \\frac{1}{3} S_{đáy} \\cdot h$.<br>- **HS:** Tiếp nhận công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho hình chóp tam giác đều có cạnh đáy $6\\text{ cm}$, trung đoạn $8\\text{ cm}$. Tính $S_{xq}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nửa chu vi đáy: $p = \\frac{3 \\cdot 6}{2} = 9\\text{ cm}$. Suy ra $S_{xq} = 9 \\cdot 8 = 72\\text{ cm}^2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt quy tắc tính diện tích xung quanh và thể tích. | **2. Diện tích xung quanh và Thể tích:**<br>- Diện tích xung quanh:<br>$$S_{xq} = p \\cdot d$$<br>với $p$ là nửa chu vi đáy, $d$ là độ dài trung đoạn.<br>- Thể tích:<br>$$V = \\frac{1}{3} S_{đáy} \\cdot h$$<br>với $S_{đáy}$ là diện tích tam giác đáy, $h$ là chiều cao hình chóp. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Rèn luyện kỹ năng tính diện tích toàn phần và thể tích khối chóp tam giác đều.
b) Nội dung: Cho hình chóp tam giác đều có cạnh đáy $10\\text{ cm}$, trung đoạn $12\\text{ cm}$, chiều cao hình chóp $h = 10\\text{ cm}$, diện tích đáy $S_{đáy} \\approx 43{,}3\\text{ cm}^2$. Tính diện tích xung quanh và thể tích hình chóp.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tính $S_{xq}$ và $V$ với số liệu cụ thể.<br>- **HS:** Ghi tóm tắt đề bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính nửa chu vi $p = \\frac{3 \\cdot 10}{2} = 15\\text{ cm}$.<br>Tính $S_{xq} = 15 \\cdot 12 = 180\\text{ cm}^2$.<br>Tính $V = \\frac{1}{3} \\cdot 43{,}3 \\cdot 10 \\approx 144{,}33\\text{ cm}^3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài giải chuẩn mực. | **Bài giải:**<br>Nửa chu vi đáy là:<br>$$p = \\frac{3 \\cdot 10}{2} = 15\\text{ (cm)}$$<br>Diện tích xung quanh của hình chóp là:<br>$$S_{xq} = p \\cdot d = 15 \\cdot 12 = 180\\text{ (cm}^2\\text{)}$$<br>Thể tích của hình chóp là:<br>$$V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} \\cdot 43{,}3 \\cdot 10 \\approx 144{,}33\\text{ (cm}^3\\text{)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng tính diện tích giấy làm hộp quà hình chóp tam giác đều.
b) Nội dung: Cần bao nhiêu diện tích bìa để làm một hộp quà hình chóp tam giác đều có diện tích toàn phần $250\\text{ cm}^2$, biết hao hụt mép dán là $10\\%$?
c) Sản phẩm: Lời giải $250 \\times 1{,}1 = 275\\text{ cm}^2$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế sản xuất hộp quà có hao hụt mép dán 10%.<br>- **HS:** Tính nhanh vào nháp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Diện tích bìa cần là: $250 \\cdot 1{,}10 = 275\\text{ cm}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị bài hình chóp tứ giác đều tiếp theo. | Diện tích bìa cần mua tính cả hao phí mép dán là $275\\text{ cm}^2$. |
"""
    },

    # 40: Bài 39
    {
        "filename": "40_KHBD_Toan8_Bai39_HinhChopTuGiacDeu_Tiet50-51.md",
        "md": """TIẾT 50, 51 - BÀI 39: HÌNH CHÓP TỨ GIÁC ĐỀU
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết các yếu tố cơ bản của hình chóp tứ giác đều: Đỉnh, cạnh bên, mặt bên (là các tam giác cân bằng nhau), cạnh đáy, mặt đáy (là hình vuông), chiều cao (đoạn nối đỉnh với giao điểm hai đường chéo của đáy), trung đoạn (chiều cao của mặt bên).
- Nhận biết hình khai triển trên mặt phẳng của hình chóp tứ giác đều (gồm một hình vuông ở giữa và bốn tam giác cân xung quanh).
- Nắm vững và vận dụng công thức tính diện tích xung quanh: $S_{xq} = p \\cdot d$ (trong đó $p$ là nửa chu vi hình vuông đáy, $d$ là trung đoạn).
- Nắm vững và vận dụng công thức tính thể tích của hình chóp tứ giác đều: $V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} a^2 \\cdot h$ (trong đó $a$ là độ dài cạnh đáy, $h$ là chiều cao hình chóp).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự gấp mô hình Kim tự tháp Ai Cập từ bìa giấy phẳng.
- Giao tiếp và hợp tác: Làm việc nhóm đo đạc và tính thể tích các khối chóp tứ giác đều.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng chuyển đổi giữa góc nhìn 2D (khai triển) và 3D (không gian), tính độ dài trung đoạn từ chiều cao và cạnh đáy bằng định lí Pythagore.
- Năng lực mô hình hoá toán học: Tính thể tích không khí bên trong một chiếc lều hình chóp tứ giác đều.

c) Năng lực số (NLS):
- ***3.1.TC2a: HS tạo nội dung số bằng cách thiết kế khối chóp tứ giác đều 3D; 5.3.TC2a: HS sử dụng công cụ số tạo tri thức về thể tích các khối đa diện; 1.1.TC2b: HS tìm kiếm ứng dụng hình chóp trong kiến trúc kim tự tháp.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D2.1: HS đánh giá độ chính xác của các mô hình Kim tự tháp 3D do AI tạo ra (trải nghiệm UX); 8.C1.1: HS mô tả cách AI "đọc" các tham số chiều cao và cạnh đáy để xuất ra thể tích.***

## 3. Về phẩm chất
- Say mê tìm hiểu kì quan kiến trúc thế giới (Kim tự tháp Kê-ốp, bảo tàng Louvre Paris).
- Rèn luyện tính cẩn thận, chính xác khi thực hiện tính toán số mũ và phân số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, mô hình hình chóp tứ giác đều, video/hình ảnh 3D về Kim tự tháp Kê-ốp và Kim tự tháp kính Louvre, máy chiếu.
2. Học sinh: SGK, vở ghi, thước kẻ, máy tính cầm tay, bìa mô hình gấp hình chóp.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Dẫn nhập vào bài học bằng hình ảnh kì quan thế giới Kim tự tháp Kê-ốp (Ai Cập).
b) Nội dung: Quan sát hình ảnh Kim tự tháp Kê-ốp, nhận xét về dạng hình học của mặt đáy và các mặt bên.
c) Sản phẩm: Câu trả lời của HS: Đáy là hình vuông, 4 mặt bên là 4 tam giác cân có chung đỉnh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh Kim tự tháp Kê-ốp (Giza, Ai Cập). Nêu câu hỏi: Kim tự tháp có đáy là hình gì và các mặt xung quanh là hình gì?<br>- **HS:** Quan sát và liên hệ kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh trong bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đáy là hình vuông, 4 mặt bên là các tam giác cân chụm lại ở đỉnh chóp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khối hình này được gọi là hình chóp tứ giác đều. | Hình ảnh thực tế: Kim tự tháp Kê-ốp có hình dạng khối chóp tứ giác đều khổng lồ. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Các yếu tố của hình chóp tứ giác đều (35 phút)
a) Mục tiêu: Nhận biết đỉnh, mặt đáy (hình vuông), các mặt bên (tam giác cân bằng nhau), chiều cao $h$, trung đoạn $d$.
b) Nội dung: Quan sát hình chóp tứ giác đều $S.ABCD$ và phân tích cấu tạo không gian.
c) Sản phẩm: Hình vẽ chuẩn trong vở và bảng liệt kê các yếu tố.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vẽ hình chóp tứ giác đều $S.ABCD$ với đáy là hình bình hành biểu diễn cho hình vuông $ABCD$. Gọi $O$ là giao điểm của $AC$ và $BD$.<br>Giới thiệu:<br>- Chiều cao: $SO = h$ ($SO \\perp (ABCD)$).<br>- Trung đoạn: Đoạn nối đỉnh $S$ với trung điểm một cạnh đáy (ví dụ $SI \\perp BC$ với $I$ là trung điểm $BC$).<br>- **HS:** Vẽ hình cẩn thận theo hướng dẫn nét đứt / nét liền.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đếm số đỉnh ($5$), số mặt ($5$), số cạnh ($8$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Bốn mặt bên là các tam giác cân bằng nhau ($SAB = SBC = SCD = SDA$).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định: Trong tam giác vuông $SOI$ vuông tại $O$, ta có hệ thức Pythagore: $SI^2 = SO^2 + OI^2 = h^2 + \\left(\\frac{a}{2}\\right)^2$. | **1. Các yếu tố của hình chóp tứ giác đều $S.ABCD$:**<br>- Đỉnh: $S$.<br>- Mặt đáy: Hình vuông $ABCD$ cạnh $a$.<br>- Chiều cao: $h = SO$ ($O$ là giao điểm của hai đường chéo $AC, BD$).<br>- Trung đoạn: $d = SI$ ($I$ là trung điểm cạnh đáy).<br>- Mối liên hệ: $d^2 = h^2 + \\left(\\frac{a}{2}\\right)^2$. |

### Hoạt động 2.2: Diện tích xung quanh và Thể tích của hình chóp tứ giác đều (30 phút)
a) Mục tiêu: Nắm vững và áp dụng công thức $S_{xq} = p \\cdot d$ và $V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} a^2 \\cdot h$.
b) Nội dung: Phát biểu công thức và giải bài toán tính diện tích xung quanh, thể tích.
c) Sản phẩm: Vở ghi công thức và bài giải ví dụ mẫu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn công thức:<br>- Chu vi đáy: $C = 4a \\Rightarrow p = 2a$ (nửa chu vi).<br>- Diện tích xung quanh: $S_{xq} = p \\cdot d = 2a \\cdot d$.<br>- Thể tích: $V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} a^2 \\cdot h$.<br>- **HS:** Ghi chép công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho hình chóp tứ giác đều có cạnh đáy $a = 10\\text{ cm}$, trung đoạn $d = 13\\text{ cm}$, chiều cao $h = 12\\text{ cm}$. Tính $S_{xq}$ và $V$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $p = 2 \\cdot 10 = 20\\text{ cm} \\Rightarrow S_{xq} = 20 \\cdot 13 = 260\\text{ cm}^2$.<br>$V = \\frac{1}{3} \\cdot 10^2 \\cdot 12 = 400\\text{ cm}^3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách làm và lưu ý đơn vị đo. | **2. Công thức Diện tích xung quanh và Thể tích:**<br>- Diện tích xung quanh:<br>$$S_{xq} = p \\cdot d = 2a \\cdot d$$<br>- Thể tích:<br>$$V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} a^2 \\cdot h$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính thể tích và diện tích xung quanh của một kim tự tháp kính thực tế.
b) Nội dung: Kim tự tháp bằng kính tại bảo tàng Louvre (Paris) có đáy là hình vuông cạnh $35\\text{ m}$, chiều cao $h = 21{,}6\\text{ m}$. Tính thể tích khoảng không gian bên trong kim tự tháp.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế tính thể tích Kim tự tháp Louvre với $a = 35\\text{ m}, h = 21{,}6\\text{ m}$.<br>- **HS:** Tóm tắt dữ kiện đề bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng công thức $V = \\frac{1}{3} a^2 \\cdot h$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng bấm máy tính và trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kết quả $8820\\text{ m}^3$. | **Bài giải:**<br>Diện tích đáy của kim tự tháp là:<br>$$S_{đáy} = a^2 = 35^2 = 1225\\text{ (m}^2\\text{)}$$<br>Thể tích khoảng không gian bên trong kim tự tháp là:<br>$$V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} \\cdot 1225 \\cdot 21{,}6 = 8820\\text{ (m}^3\\text{)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng tính trung đoạn $d$ từ chiều cao $h$ và cạnh đáy $a$ nhờ định lí Pythagore.
b) Nội dung: Biết một chiếc lều có cạnh đáy $a = 2{,}4\\text{ m}$, chiều cao $h = 1{,}6\\text{ m}$. Tính diện tích vải bạt cần dùng để dựng 4 mặt xung quanh lều (không tính đáy).
c) Sản phẩm: Kết quả $d = \\sqrt{1{,}6^2 + 1{,}2^2} = 2\\text{ m}$, $S_{xq} = 2 \\cdot 2{,}4 \\cdot 2 = 9{,}6\\text{ m}^2$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn tìm $OI = \\frac{a}{2} = 1{,}2\\text{ m}$, áp dụng Pythagore tính trung đoạn $d$.<br>- **HS:** Bấm máy tính tính trung đoạn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $d = \\sqrt{1{,}6^2 + 1{,}2^2} = 2\\text{ m}$. Diện tích vải bạt: $S_{xq} = 2a \\cdot d = 2 \\cdot 2{,}4 \\cdot 2 = 9{,}6\\text{ m}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo kết quả miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và chốt ứng dụng thực tế. | Diện tích vải bạt xung quanh lều là $9{,}6\\text{ m}^2$. |
"""
    },

    # 41: Tiết 52: Luyện tập chung (Mindmap: mindmap_toan8_hinh_tiet52.png)
    {
        "filename": "41_KHBD_Toan8_LuyenTapChung_Tiet52.md",
        "md": """TIẾT 52 - LUYỆN TẬP CHUNG
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- So sánh, phân biệt và củng cố toàn diện kiến thức về hai hình khối không gian: Hình chóp tam giác đều và Hình chóp tứ giác đều:
  + Cấu tạo đáy (tam giác đều so với hình vuông), số mặt bên, số cạnh, số đỉnh.
  + Chiều cao, trung đoạn, hình khai triển phẳng.
  + Công thức diện tích xung quanh: $S_{xq} = p \\cdot d$.
  + Công thức thể tích: $V = \\frac{1}{3} S_{đáy} \\cdot h$.
- Rèn luyện kỹ năng giải các bài toán thực tế kết hợp định lí Pythagore để tìm chiều cao hoặc trung đoạn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp bảng so sánh hai loại hình chóp bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận giải các bài toán hình khối không gian.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng tưởng tượng hình học không gian, vận dụng định lí Pythagore trong mặt phẳng vuông góc chứa chiều cao và trung đoạn.
- Năng lực mô hình hoá toán học: Tính toán chi phí vật liệu, khối lượng và thể tích của các vật thể thực tế hình chóp.

c) Năng lực số (NLS):
- ***2.2.TC2a: HS vận dụng công nghệ số chia sẻ quy trình tính thể tích vật thể thực; 1.2.TC2a: HS đánh giá độ tin cậy của các mô phỏng hình học trên mạng; 5.1.TC2a: HS xác định lỗi khi xoay mô hình khối 3D không đúng góc.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D1.1: HS lập kế hoạch dùng AI mô phỏng quá trình khai triển các mặt hình chóp thành hình phẳng.***

## 3. Về phẩm chất
- Rèn thói quen làm việc khoa học, tỉ mỉ, kiểm tra kĩ đơn vị đo thể tích ($1\\text{ m}^3 = 1000\\text{ lít}$, $1\\text{ dm}^3 = 1\\text{ lít}$).
- Tinh thần đồng đội, chủ động trao đổi kiến thức.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI, máy chiếu, bảng phụ ghi bài tập so sánh.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, dụng cụ vẽ hình.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: So sánh nhanh sự giống và khác nhau giữa hình chóp tam giác đều và hình chóp tứ giác đều.
b) Nội dung: Điền vào bảng so sánh về số mặt, số đỉnh, số cạnh, hình dạng đáy của hai hình chóp.
c) Sản phẩm: Bảng so sánh điền đúng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: So sánh số mặt, số cạnh, số đỉnh và hình dạng đáy của hình chóp tam giác đều và hình chóp tứ giác đều.<br>- **HS:** Nhớ lại kiến thức bài trước.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm nhanh các thông số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chóp tam giác đều: 4 mặt, 4 đỉnh, 6 cạnh, đáy tam giác đều. Chóp tứ giác đều: 5 mặt, 5 đỉnh, 8 cạnh, đáy hình vuông.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt bảng so sánh và chuyển sang sơ đồ tư duy. | Bảng so sánh đặc điểm hình học của hai loại khối chóp đều. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Hình chóp đều bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ công thức và phương pháp giải toán hình khối chóp đều bằng sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy 300 DPI Hình chóp tam giác đều & Hình chóp tứ giác đều.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Hình chóp tam giác đều và tứ giác đều Tiết 52](khbd-ill:mindmap-toan8-hinh-tiet52)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu sơ đồ tư duy vector 300 DPI tổng hợp kiến thức Hình chóp tam giác đều và Hình chóp tứ giác đều. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Hình chóp tam giác đều (đáy, mặt bên, $S_{xq}, V$).<br>2) Hình chóp tứ giác đều (đáy, mặt bên, $S_{xq}, V$).<br>3) Khai triển phẳng.<br>4) Mối liên hệ Pythagore giữa chiều cao $h$, trung đoạn $d$ và bán kính/cạnh đáy.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS trình bày lại phương pháp tính trung đoạn $d$ từ chiều cao $h$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Công thức $S_{xq} = p \\cdot d$ và $V = \\frac{1}{3} S_{đáy} \\cdot h$ dùng chung cho cả hai loại hình chóp đều. | **Tổng hợp kiến thức trọng tâm:**<br>1. Công thức chung: $S_{xq} = p \\cdot d$ và $V = \\frac{1}{3} S_{đáy} \\cdot h$.<br>2. Chóp tam giác đều: Đáy là tam giác đều, $p = \\frac{3a}{2}$.<br>3. Chóp tứ giác đều: Đáy là hình vuông, $p = 2a$, $S_{đáy} = a^2$.<br>4. Định lí Pythagore tính trung đoạn: $d^2 = h^2 + \\left(\\frac{a}{2}\\right)^2$ (với chóp tứ giác đều). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán thực tế hỗn hợp tính diện tích sơn mái nhà hình chóp tứ giác đều và thể tích không khí trong mái.
b) Nội dung: Mái một chòi ngắm cảnh có dạng hình chóp tứ giác đều với cạnh đáy $a = 4\\text{ m}$, chiều cao của mái $h = 1{,}5\\text{ m}$.
1) Tính độ dài trung đoạn của mái nhà.
2) Tính diện tích ngói cần để lợp 4 mặt mái chòi (diện tích xung quanh).
3) Tính thể tích không gian bên trong mái chòi.
c) Sản phẩm: Lời giải hoàn chỉnh 3 phần trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài toán mái chòi ngắm cảnh với các yêu cầu trên.<br>- **HS:** Vẽ hình phác họa không gian mái chòi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** 1) Tính khoảng cách từ tâm đáy đến cạnh đáy: $OI = \\frac{a}{2} = 2\\text{ m}$. Áp dụng Pythagore: $d = \\sqrt{h^2 + OI^2} = \\sqrt{1{,}5^2 + 2^2} = 2{,}5\\text{ m}$.<br>2) Nửa chu vi đáy: $p = 2 \\cdot 4 = 8\\text{ m}$. Diện tích lợp ngói: $S_{xq} = p \\cdot d = 8 \\cdot 2{,}5 = 20\\text{ m}^2$.<br>3) Thể tích không gian: $V = \\frac{1}{3} \\cdot 4^2 \\cdot 1{,}5 = 8\\text{ m}^3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán ứng dụng thực tế kiến trúc mái chòi. | **Bài giải:**<br>1) Gọi $O$ là tâm đáy hình vuông, $I$ là trung điểm cạnh đáy.<br>Ta có $OI = \\frac{4}{2} = 2\\text{ (m)}$.<br>Độ dài trung đoạn $d$ là:<br>$$d = \\sqrt{h^2 + OI^2} = \\sqrt{1{,}5^2 + 2^2} = \\sqrt{2{,}25 + 4} = \\sqrt{6{,}25} = 2{,}5\\text{ (m)}$$<br><br>2) Nửa chu vi đáy là:<br>$$p = \\frac{4 \\cdot 4}{2} = 8\\text{ (m)}$$<br>Diện tích ngói lợp 4 mặt mái chòi là:<br>$$S_{xq} = p \\cdot d = 8 \\cdot 2{,}5 = 20\\text{ (m}^2\\text{)}$$<br><br>3) Thể tích không gian bên trong mái chòi là:<br>$$V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} \\cdot 4^2 \\cdot 1{,}5 = 8\\text{ (m}^3\\text{)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tính số tiền mua ngói lợp mái dựa trên diện tích vừa tính được.
b) Nội dung: Biết giá lợp mỗi mét vuông ngói trọn gói là $350\\,000\\text{ đồng}$. Tính tổng chi phí lợp ngói mái chòi.
c) Sản phẩm: Kết quả $20 \\times 350\\,000 = 7\\,000\\,000\\text{ đồng}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tính chi phí lợp ngói cho $20\\text{ m}^2$ với đơn giá $350\\,000\\text{ đ/m}^2$.<br>- **HS:** Tính nhẩm nhanh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $20 \\cdot 350\\,000 = 7\\,000\\,000\\text{ (đồng)}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo kết quả miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò làm bài tập cuối chương X. | Chi phí lợp ngói mái chòi là $7\\,000\\,000\\text{ đồng}$. |
"""
    },

    # 42: Tiết 53: Bài tập cuối chương X (Mindmap: mindmap_toan8_hinh_tiet53.png)
    {
        "filename": "42_KHBD_Toan8_BaiTapCuoiChuong10_Tiet53.md",
        "md": """TIẾT 53 - BÀI TẬP CUỐI CHƯƠNG X
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập và củng cố toàn diện kiến thức Chương X: Một số hình khối trong thực tiễn:
  + Hình chóp tam giác đều (đặc điểm hình học, diện tích xung quanh, thể tích).
  + Hình chóp tứ giác đều (đặc điểm hình học, diện tích xung quanh, thể tích).
  + Hình khai triển phẳng và mối liên hệ hình học không gian.
- Rèn luyện kỹ năng giải bài tập trắc nghiệm và tự luận tổng hợp của chương.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức Chương X dưới dạng sơ đồ tư duy hệ thống.
- Giao tiếp và hợp tác: Hợp tác tích cực trong nhóm để hoàn thành phiếu bài tập cuối chương.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng nhìn nhận không gian ba chiều, lập luận mối quan hệ giữa các kích thước trong khối đa diện.
- Năng lực giải quyết vấn đề toán học: Hoàn thành bài toán thực tế về bao bì, xây dựng, kiến trúc hình chóp đều.

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi thực hiện tính toán số thập phân và làm tròn.
- Tinh thần nghiêm túc ôn tập chuẩn bị cho đợt Ôn tập và Kiểm tra cuối Học kì II.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI Chương X, phiếu bài tập ôn tập cuối chương.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, dụng cụ vẽ hình.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khởi động ôn tập bằng trò chơi ghép công thức nhanh.
b) Nội dung: Nối công thức tính diện tích xung quanh và thể tích với từng loại hình khối.
c) Sản phẩm: Bảng nối chính xác các công thức của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi trắc nghiệm nối công thức tính $S_{xq}$ và $V$ của hình chóp đều.<br>- **HS:** Quan sát bảng phụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại nhanh: $S_{xq} = p \\cdot d$, $V = \\frac{1}{3} S_{đáy} \\cdot h$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng nối công thức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá đúng và chuyển sang sơ đồ tư duy tổng kết toàn chương. | Nhắc lại công thức cốt lõi: $S_{xq} = p \\cdot d$ và $V = \\frac{1}{3} S_{đáy} \\cdot h$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Tổng kết Chương X bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Khái quát hóa toàn bộ kiến thức Chương X: Một số hình khối trong thực tiễn.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI tổng kết Chương X.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Bài tập cuối chương X Tiết 53](khbd-ill:mindmap-toan8-hinh-tiet53)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu sơ đồ tư duy vector 300 DPI tổng kết toàn bộ Chương X. Yêu cầu HS phân tích các nhánh.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trình bày 3 nhánh chính:<br>1) Hình chóp tam giác đều (đáy tam giác đều, 3 mặt bên tam giác cân, $S_{xq}, V$).<br>2) Hình chóp tứ giác đều (đáy hình vuông, 4 mặt bên tam giác cân, $S_{xq}, V$).<br>3) Ứng dụng thực tiễn (kiến trúc, bao bì, thể tích không gian).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 1 HS phát biểu tóm tắt toàn bộ chương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt trọng tâm ôn tập. | **Tổng kết toàn bộ Chương X:**<br>1. Phân biệt hình chóp tam giác đều và tứ giác đều.<br>2. Nhận biết trung đoạn, chiều cao, đường khai triển.<br>3. Công thức: $S_{xq} = p \\cdot d$, $V = \\frac{1}{3} S_{đáy} \\cdot h$.<br>4. Ứng dụng thực tế: Thể tích lều trại, kim tự tháp, diện tích vỏ hộp quà. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài tập tổng hợp cuối chương trong SGK Toán 8 Tập 2.
b) Nội dung: Cho một hộp quà bằng bìa cứng có dạng hình chóp tứ giác đều có cạnh đáy $a = 12\\text{ cm}$, độ dài trung đoạn $d = 10\\text{ cm}$.
1) Tính diện tích bìa cần dùng để làm chiếc hộp (bao gồm cả đáy), bỏ qua mép dán.
2) Tính chiều cao $h$ của hộp quà.
3) Tính thể tích của hộp quà.
c) Sản phẩm: Lời giải hoàn chỉnh 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao đề bài toán hộp quà hình chóp tứ giác đều.<br>- **HS:** Tóm tắt dữ kiện và vẽ hình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** 1) Nửa chu vi đáy: $p = 2 \\cdot 12 = 24\\text{ cm}$. $S_{xq} = 24 \\cdot 10 = 240\\text{ cm}^2$.<br>Diện tích đáy: $S_{đáy} = 12^2 = 144\\text{ cm}^2$. Diện tích toàn phần: $S_{tp} = 240 + 144 = 384\\text{ cm}^2$.<br>2) Trong tam giác vuông chứa chiều cao và trung đoạn: $OI = 6\\text{ cm}$. Áp dụng Pythagore: $h = \\sqrt{d^2 - OI^2} = \\sqrt{10^2 - 6^2} = 8\\text{ cm}$.<br>3) Thể tích: $V = \\frac{1}{3} \\cdot 144 \\cdot 8 = 384\\text{ cm}^3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lần lượt lên bảng làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài giải mẫu chuẩn mực trên bảng. | **Bài giải:**<br>1) Nửa chu vi đáy là:<br>$$p = \\frac{4 \\cdot 12}{2} = 24\\text{ (cm)}$$<br>Diện tích xung quanh là:<br>$$S_{xq} = p \\cdot d = 24 \\cdot 10 = 240\\text{ (cm}^2\\text{)}$$<br>Diện tích đáy là:<br>$$S_{đáy} = 12^2 = 144\\text{ (cm}^2\\text{)}$$<br>Diện tích bìa cần dùng là:<br>$$S_{tp} = S_{xq} + S_{đáy} = 240 + 144 = 384\\text{ (cm}^2\\text{)}$$<br><br>2) Khoảng cách từ tâm đáy đến cạnh đáy là $OI = \\frac{12}{2} = 6\\text{ (cm)}$.<br>Chiều cao của chiếc hộp là:<br>$$h = \\sqrt{d^2 - OI^2} = \\sqrt{10^2 - 6^2} = \\sqrt{100 - 36} = \\sqrt{64} = 8\\text{ (cm)}$$<br><br>3) Thể tích chiếc hộp là:<br>$$V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} \\cdot 144 \\cdot 8 = 384\\text{ (cm}^3\\text{)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Liên hệ thú vị giữa giá trị diện tích toàn phần ($384\\text{ cm}^2$) và thể tích ($384\\text{ cm}^3$) của chiếc hộp.
b) Nội dung: GV giải thích vì sao hai giá trị bằng nhau về mặt số học nhưng khác nhau về đơn vị đo lường.
c) Sản phẩm: HS nhận thức rõ sự khác biệt giữa đơn vị diện tích và đơn vị thể tích.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu hiện tượng trùng lặp số học $384$: Liệu diện tích toàn phần và thể tích có bằng nhau không?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời: Về số học bằng nhau do vô tình, nhưng đơn vị đo hoàn toàn khác nhau ($\text{cm}^2$ là diện tích mặt phẳng, $\text{cm}^3$ là độ lớn không gian).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và dặn dò chuẩn bị cho tuần ôn tập cuối học kì II. | Phân biệt bản chất đại lượng diện tích ($\text{cm}^2$) và thể tích ($\text{cm}^3$). |
"""
    },

    # 43: Tiết 54-55: Ôn tập cuối HK2 Hình học (Mindmap: mindmap_toan8_hinh_tiet54_55.png)
    {
        "filename": "43_KHBD_Toan8_OnTapCuoiHK2_HinhHoc_Tiet54-55.md",
        "md": """TIẾT 54, 55 - ÔN TẬP HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Hình học Học kì II môn Toán 8:
  + Chương IX: Tam giác đồng dạng: Định nghĩa, ba trường hợp đồng dạng (c.c.c, c.g.c, g.g), định lí Pythagore thuận và đảo, các trường hợp đồng dạng của tam giác vuông, hình đồng dạng phối cảnh.
  + Chương X: Một số hình khối trong thực tiễn: Hình chóp tam giác đều, hình chóp tứ giác đều, công thức diện tích xung quanh $S_{xq} = p \\cdot d$ và thể tích $V = \\frac{1}{3} S_{đáy} \\cdot h$.
- Rèn luyện kỹ năng tổng hợp giải các bài toán hình học phẳng và hình học không gian có trong ma trận đề kiểm tra cuối kì.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức hình học cả học kì dưới dạng sơ đồ tư duy bao quát.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp chứng minh hình học khác nhau trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng suy luận logic, chứng minh hình học chặt chẽ, kết hợp nhuần nhuyễn giữa tam giác đồng dạng và định lí Pythagore.
- Năng lực giải quyết vấn đề toán học: Phân tích bài toán thực tế thành mô hình hình học không gian hoặc hình học phẳng để giải quyết.

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, vẽ hình chính xác và rõ ràng.
- Tự tin, sẵn sàng tâm thế bước vào kì kiểm tra đánh giá cuối năm học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, đề cương ôn tập cuối HK2 phần Hình học, sơ đồ tư duy vector 300 DPI, máy chiếu.
2. Học sinh: SGK, vở ghi, dụng cụ vẽ hình đầy đủ, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Định hướng ôn tập và nắm rõ cấu trúc đề kiểm tra đánh giá cuối năm học phần Hình học.
b) Nội dung: GV giới thiệu ma trận đề kiểm tra cuối HK2 phần Hình học (chiếm khoảng 3,5 - 4,0 điểm trong thang điểm 10).
c) Sản phẩm: HS xác định được các nội dung trọng tâm cần ôn tập.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến cấu trúc phần hình học trong đề thi học kì II: Gồm câu trắc nghiệm nhận biết khối chóp và tam giác đồng dạng, 1 câu tự luận tính thể tích hình khối thực tế và 1 bài hình tổng hợp tam giác đồng dạng 3 câu.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự rà soát các nội dung kiến thức còn cảm thấy chưa vững.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu các dạng bài cần thầy cô giải đáp kĩ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chiếu sơ đồ tư duy tổng kết toàn diện hình học HK2. | Nắm vững ma trận đề kiểm tra cuối HK2 phần Hình học. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Hệ thống hóa toàn bộ Hình học HK2 bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ Chương IX (Tam giác đồng dạng) và Chương X (Một số hình khối trong thực tiễn) bằng sơ đồ tư duy 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Ôn tập cuối HK2 Hình học.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Ôn tập cuối HK2 Hình học Tiết 54 - 55](khbd-ill:mindmap-toan8-hinh-tiet54_55)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Ôn tập cuối HK2 Hình học. Yêu cầu HS phân tích hai trụ cột chính của sơ đồ.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 2 trụ cột:<br>1) Chương IX - Tam giác đồng dạng: 3 trường hợp đồng dạng thường (c.c.c, c.g.c, g.g), Định lí Pythagore thuận và đảo, các trường hợp tam giác vuông đồng dạng, hình đồng dạng phối cảnh.<br>2) Chương X - Khối chóp đều: Chóp tam giác đều, chóp tứ giác đều, công thức $S_{xq} = p \\cdot d$, $V = \\frac{1}{3} S_{đáy} \\cdot h$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS nhắc lại cách áp dụng Pythagore để chuyển đổi qua lại giữa $h$ và $d$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt sơ đồ và nhấn mạnh phương pháp trình bày chứng minh hình học mạch lạc, có căn cứ. | **Hệ thống kiến thức Hình học HK2:**<br>1. Tam giác đồng dạng: 3 trường hợp c.c.c, c.g.c, g.g.<br>2. Định lí Pythagore và định lí đảo.<br>3. Tam giác vuông đồng dạng và hệ thức lượng.<br>4. Hình đồng dạng phối cảnh và ứng dụng đo đạc.<br>5. Hình chóp tam giác đều và hình chóp tứ giác đều ($S_{xq}, V$). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
### Hoạt động 3.1: Luyện tập bài toán Hình học không gian thực tế (20 phút)
a) Mục tiêu: Giải bài toán tính diện tích xung quanh và thể tích hình chóp tứ giác đều thực tế.
b) Nội dung: Một chiếc lều trại có dạng hình chóp tứ giác đều có đáy là hình vuông cạnh $3\\text{ m}$, chiều cao của chiếc lều là $2\\text{ m}$.
1) Tính thể tích không gian bên trong chiếc lều.
2) Tính diện tích vải bạt cần để phủ 4 mặt xung quanh lều (biết hao hụt các mép may là $5\\%$).
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập lều trại hình chóp tứ giác đều.<br>- **HS:** Vẽ hình và tóm tắt đề bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính $V = \\frac{1}{3} \\cdot 3^2 \\cdot 2 = 6\\text{ m}^3$.<br>Khoảng cách $OI = 1{,}5\\text{ m}$. Trung đoạn $d = \\sqrt{2^2 + 1{,}5^2} = 2{,}5\\text{ m}$.<br>Nửa chu vi đáy: $p = 2 \\cdot 3 = 6\\text{ m}$. $S_{xq} = 6 \\cdot 2{,}5 = 15\\text{ m}^2$.<br>Diện tích bạt tính hao hụt: $15 \\cdot 1{,}05 = 15{,}75\\text{ m}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán hình khối không gian. | **Bài giải:**<br>1) Thể tích không gian bên trong lều là:<br>$$V = \\frac{1}{3} S_{đáy} \\cdot h = \\frac{1}{3} \\cdot 3^2 \\cdot 2 = 6\\text{ (m}^3\\text{)}$$<br><br>2) Ta có $OI = \\frac{3}{2} = 1{,}5\\text{ (m)}$.<br>Độ dài trung đoạn $d$ là:<br>$$d = \\sqrt{h^2 + OI^2} = \\sqrt{2^2 + 1{,}5^2} = \\sqrt{4 + 2{,}25} = 2{,}5\\text{ (m)}$$<br>Nửa chu vi đáy là:<br>$$p = \\frac{4 \\cdot 3}{2} = 6\\text{ (m)}$$<br>Diện tích xung quanh của lều là:<br>$$S_{xq} = p \\cdot d = 6 \\cdot 2{,}5 = 15\\text{ (m}^2\\text{)}$$<br>Diện tích vải bạt cần mua là:<br>$$S = 15 \\cdot 1{,}05 = 15{,}75\\text{ (m}^2\\text{)}$$ |

### Hoạt động 3.2: Luyện tập bài toán Hình học phẳng tổng hợp (35 phút)
a) Mục tiêu: Giải bài toán hình học phẳng tổng hợp tam giác đồng dạng 3 câu chuẩn đề thi học kì.
b) Nội dung: Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$.
1) Chứng minh $\\Delta HBA \\backsim \\Delta ABC$ và suy ra $AB^2 = BH \\cdot BC$.
2) Gọi $M$ là trung điểm của $AC$. Kẻ $AK \\perp BM$ tại $K$. Chứng minh $\\Delta BKH \\backsim \\Delta BMA$.
3) Chứng minh $\\widehat{BHK} = \\widehat{BAC}$.
c) Sản phẩm: Lời giải chi tiết bài toán hình học tổng hợp trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài toán hình học phẳng tổng hợp.<br>- **HS:** Vẽ hình cẩn thận, chính xác bằng thước và eke.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận giải quyết từng câu:<br>1) Chứng minh đồng dạng góc nhọn.<br>2) Chứng minh $\\Delta BKM \\backsim \\Delta BHA$ (g.g) suy ra tỉ số $BK \\cdot BM = BH \\cdot BA \\Rightarrow \\frac{BK}{BH} = \\frac{BA}{BM}$. Kết hợp góc $B$ chung suy ra $\\Delta BKH \\backsim \\Delta BMA$ (c.g.c).<br>3) Từ câu 2 suy ra $\\widehat{BHK} = \\widehat{BAM} = 90^\\circ = \\widehat{BAC}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS lên bảng trình bày từng phần.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, hướng dẫn kĩ năng phân tích tỉ số chéo để chứng minh hai tam giác đồng dạng theo c.g.c. | **Bài giải:**<br>1) Xét $\\Delta HBA$ (vuông tại $H$) và $\\Delta ABC$ (vuông tại $A$) có:<br>$$\\widehat{B}\\text{ chung}$$<br>Do đó $\\Delta HBA \\backsim \\Delta ABC$ (góc nhọn).<br>Suy ra $\\frac{AB}{BC} = \\frac{BH}{AB} \\Rightarrow AB^2 = BH \\cdot BC$.<br><br>2) Xét $\\Delta BKA$ (vuông tại $K$) và $\\Delta BHM$ có thể quy về:<br>$\\Delta BKM$ (vuông tại $K$) và $\\Delta BHA$ (vuông tại $H$) có $\\widehat{B}$ chung.<br>Do đó $\\Delta BKM \\backsim \\Delta BHA$ (góc nhọn).<br>Suy ra: $\\frac{BK}{BH} = \\frac{BM}{BA} \\Rightarrow BK \\cdot BA = BH \\cdot BM$ hay $\\frac{BK}{BH} = \\frac{BM}{BA}$.<br>Xét $\\Delta BKH$ và $\\Delta BMA$ có:<br>- $\\widehat{B}$ chung;<br>- $\\frac{BK}{BM} = \\frac{BH}{BA}$.<br>Vậy $\\Delta BKH \\backsim \\Delta BMA$ (c.g.c).<br><br>3) Vì $\\Delta BKH \\backsim \\Delta BMA$ nên:<br>$$\\widehat{BHK} = \\widehat{BAM}$$<br>Mà $\\widehat{BAM} = 90^\\circ$ (do $\\Delta ABC$ vuông tại $A$ và $M \\in AC$).<br>Do đó $\\widehat{BHK} = 90^\\circ = \\widehat{BAC}$. |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhắc nhở dặn dò chuẩn bị cho tiết Kiểm tra cuối học kì II.
b) Nội dung: Rà soát đồ dùng thi (thước, eke, compa, máy tính cầm tay có pin tốt) và quy chế phòng thi.
c) Sản phẩm: HS ghi nhận đầy đủ dặn dò.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò ôn tập kỹ toàn bộ kiến thức cả Đại số và Hình học HK2, chuẩn bị đầy đủ dụng cụ cho tiết Kiểm tra đánh giá cuối HK2.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kiểm tra lại đồ dùng học tập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu những điều cần lưu ý khi làm bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em ôn tập hiệu quả và đạt điểm cao trong kì kiểm tra cuối năm học. | Dặn dò chuẩn bị cho kì Kiểm tra cuối Học kì II. |
"""
    },

    # 44: Tiết 56: Kiểm tra cuối HK2 Hình học
    {
        "filename": "44_KHBD_Toan8_KiemTraCuoiHK2_HinhHoc_Tiet56.md",
        "md": """TIẾT 56 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện chuẩn kiến thức kĩ năng phần Hình học Toán 8 Học kì II:
  + Nắm vững và vận dụng các định lí đồng dạng của tam giác thường và tam giác vuông.
  + Nắm vững và vận dụng định lí Pythagore thuận và đảo.
  + Tính diện tích xung quanh và thể tích hình chóp tam giác đều, hình chóp tứ giác đều.
  + Kỹ năng vẽ hình chuẩn xác, trình bày lời giải bài toán hình học chặt chẽ.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Ý thức tự giác, trung thực, nghiêm túc làm bài kiểm tra độc lập.
- Giải quyết vấn đề: Phân bổ hợp lí thời gian giữa các câu trắc nghiệm và câu tự luận.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng lập luận logic, suy diễn hình học chặt chẽ.
- Năng lực mô hình hoá toán học: Giải bài toán ứng dụng hình học vào thực tế.

## 3. Về phẩm chất
- Trung thực, khách quan trong kiểm tra đánh giá.
- Rèn tính kiên nhẫn, cẩn thận, không bỏ sót các trường hợp.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo đúng ma trận và đặc tả đề kiểm tra cuối kì của nhà trường, đáp án và biểu điểm chi tiết.
2. Học sinh: Dụng cụ vẽ hình đầy đủ, máy tính cầm tay, bút viết, giấy thi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ PHÁT ĐỀ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ổn định phòng thi, phổ biến quy chế và phát đề kiểm tra cho học sinh.
b) Nội dung: GV điểm danh, nhắc nhở quy chế thi và phát đề.
c) Sản phẩm: 100% học sinh nhận đề và ghi đầy đủ thông tin vào giấy làm bài.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định chỗ ngồi, kiểm tra trật tự, nhắc nhở nghiêm cấm mọi hành vi gian lận.<br>- **HS:** Cất toàn bộ tài liệu và chuẩn bị dụng cụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Phát đề kiểm tra.<br>- **HS:** Kiểm tra độ rõ của đề, ghi thông tin cá nhân.<br><br>**+ Bước 3: Bắt đầu làm bài**<br>- **GV:** Ghi thời gian làm bài lên bảng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giám sát phòng thi nghiêm túc. | Phát đề kiểm tra và ổn định phòng thi. |

## B. TIẾN HÀNH LÀM BÀI KIỂM TRA (HOẠT ĐỘNG 2) (35 phút)
### Ma trận và Đề kiểm tra Hình học cuối HK2 (35 phút)
a) Mục tiêu: Học sinh làm bài kiểm tra độc lập, đạt kết quả cao nhất theo năng lực.
b) Nội dung: Đề gồm 2 phần: Trắc nghiệm (3 điểm) và Tự luận (7 điểm).
c) Sản phẩm: Bài làm hoàn chỉnh trên giấy thi của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Làm bài độc lập**<br>- **HS:** Làm bài nghiêm túc, vẽ hình chính xác vào giấy thi.<br>- **GV:** Giám thị bao quát lớp thi.<br><br>**+ Bước 2: Theo dõi thời gian**<br>- **GV:** Nhắc nhở thời gian làm bài (còn 15 phút, còn 5 phút).<br>- **HS:** Soát lại bài làm, kiểm tra kĩ đơn vị đo.<br><br>**+ Bước 3: Hoàn thành bài làm**<br>- **HS:** Sắp xếp lại tờ giấy thi, chuẩn bị nộp bài.<br><br>**+ Bước 4: Hết giờ làm bài**<br>- **GV:** Thu bài kiểm tra của cả lớp. | **Nội dung đề kiểm tra minh họa:**<br>**Phần I. Trắc nghiệm (3 điểm):**<br>- Câu 1: Công thức thể tích hình chóp $V = \\frac{1}{3} S_{đáy} \\cdot h$.<br>- Câu 2: Trường hợp đồng dạng của tam giác vuông.<br>- Câu 3: Định lí Pythagore đảo.<br><br>**Phần II. Tự luận (7 điểm):**<br>**Bài 1 (2,0 điểm):** Một mái chòi hình chóp tứ giác đều có cạnh đáy $3\\text{ m}$, trung đoạn $2{,}5\\text{ m}$. Tính diện tích xung quanh của mái chòi.<br>**Bài 2 (5,0 điểm):** Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$.<br>a) (2,0 điểm) Chứng minh $\\Delta HBA \\backsim \\Delta ABC$ và suy ra $AB^2 = BH \\cdot BC$.<br>b) (2,0 điểm) Biết $AB = 15\\text{ cm}, BC = 25\\text{ cm}$. Tính $AC, AH, BH$.<br>c) (1,0 điểm) Kẻ phân giác $BD$ của góc $B$ ($D \\in AC$). Qua $C$ kẻ đường thẳng vuông góc với tia $BD$ tại $E$. Chứng minh $BA \\cdot CE = BC \\cdot AE$. |

## C. THU BÀI VÀ NHẬN XÉT (HOẠT ĐỘNG 3) (5 phút)
a) Mục tiêu: Thu đủ số lượng bài thi và nhận xét nền nếp buổi kiểm tra.
b) Nội dung: Thu bài theo hàng, kiểm đếm đủ số bài thi và giải tỏa căng thẳng cho học sinh.
c) Sản phẩm: Thu đủ 100% bài kiểm tra của cả lớp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thu bài kiểm tra của học sinh theo thứ tự bàn học.<br>- **HS:** Nộp bài trật tự, nghiêm túc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm khớp số bài thi với sĩ số.<br><br>**+ Bước 3: Nhận xét giờ kiểm tra**<br>- **GV:** Tuyên dương ý thức làm bài nghiêm túc, tự giác của cả lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò chuẩn bị cho tiết Trả bài kiểm tra tiếp theo. | Thu đủ số bài kiểm tra và nhận xét nền nếp phòng thi. |
"""
    },

    # 45: Tiết 57: Trả bài kiểm tra cuối HK2 Hình học
    {
        "filename": "45_KHBD_Toan8_TraBaiKiemTraCuoiHK2_HinhHoc_Tiet57.md",
        "md": """TIẾT 57 - TRẢ BÀI KIỂM TRA HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết các ưu điểm và các lỗi sai sót phổ biến trong bài làm kiểm tra cuối học kì II phần Hình học của học sinh:
  + Lỗi vẽ hình không chính xác, thiếu kí hiệu góc vuông, đỉnh tương ứng viết sai thứ tự.
  + Lỗi nhầm lẫn giữa chiều cao $h$ của hình chóp và trung đoạn $d$ của mặt bên.
  + Lỗi tính toán và làm tròn số thập phân.
- Nắm vững đáp án, thang điểm chi tiết và phương pháp chuẩn mực giải từng câu trong đề kiểm tra.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đánh giá bài làm của bản thân, đối chiếu với đáp án và tự giác chữa bài vào vở.
- Giao tiếp và hợp tác: Cởi mở trao đổi cách giải hay, phân tích nguyên nhân sai lầm cùng bạn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng tự phản biện, nhận ra điểm gãy trong suy luận hình học của chính mình.
- Năng lực giải quyết vấn đề toán học: Trình bày lại lời giải hoàn chỉnh cho những câu chưa đạt điểm tối đa.

## 3. Về phẩm chất
- Trung thực, thẳng thắn nhìn nhận kết quả học tập của bản thân.
- Có ý chí vượt khó, rút kinh nghiệm sâu sắc để học tập tốt hơn trong năm học tiếp theo (Toán 9).

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Bài kiểm tra của học sinh đã chấm điểm và phê nhận xét chi tiết, bảng tổng hợp điểm số, đáp án và biểu điểm chi tiết chiếu trên màn hình.
2. Học sinh: Vở ghi bài chữa, bút đỏ để sửa lỗi.

# III. TIẾN TRÌNH DẠY HỌC

## A. NHẬN XÉT CHUNG VỀ KẾT QUẢ BÀI KIỂM TRA (HOẠT ĐỘNG 1) (10 phút)
a) Mục tiêu: Đánh giá tổng quan kết quả kiểm tra của cả lớp, công bố phổ điểm và biểu dương các học sinh đạt thành tích xuất sắc.
b) Nội dung: GV nhận xét ưu điểm, nhược điểm chung và công bố phổ điểm phần hình học.
c) Sản phẩm: Bảng thống kê điểm số và sự lắng nghe nghiêm túc của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Báo cáo tổng quan tình hình làm bài của lớp:<br>- Đa số nắm chắc công thức tính diện tích xung quanh, thể tích khối chóp và định lí Pythagore.<br>- Kỹ năng chứng minh tam giác đồng dạng đã có nhiều tiến bộ.<br>- Phổ điểm đạt tỉ lệ khá giỏi cao.<br>- **HS:** Lắng nghe nhận xét.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Biểu dương các học sinh đạt điểm $9, 10$ và có bài vẽ hình sạch đẹp, lập luận mẫu mực.<br>- Nhắc nhở một số em còn chủ quan, tính toán nhầm căn bậc hai.<br><br>**+ Bước 3: Phát bài kiểm tra**<br>- **GV:** Phát bài kiểm tra cho từng học sinh.<br>- **HS:** Nhận bài, xem điểm số và lời phê của giáo viên.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Yêu cầu HS đối chiếu kĩ các phần bị trừ điểm để chuẩn bị chữa bài. | Nhận xét ưu - nhược điểm chung và phát bài kiểm tra cho học sinh. |

## B. CHỮA BÀI CHI TIẾT TỪNG CÂU (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Chữa phần trắc nghiệm và câu tính khối chóp (10 phút)
a) Mục tiêu: Giải thích rõ lí do chọn đáp án đúng phần trắc nghiệm và khắc phục lỗi tính hình chóp.
b) Nội dung: Giải chi tiết các câu trắc nghiệm và Bài 1 tự luận về hình chóp tứ giác đều.
c) Sản phẩm: Bài chữa chuẩn trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu đáp án trắc nghiệm và câu tính diện tích xung quanh mái chòi.<br>- **HS:** Soát lại đáp án của mình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chữa Bài 1: $p = \\frac{4 \\cdot 3}{2} = 6\\text{ m}$. $S_{xq} = 6 \\cdot 2{,}5 = 15\\text{ m}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ nêu lỗi sai nếu có.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Lưu ý không được quên chia 2 khi tính nửa chu vi $p$. | **Chữa Bài 1:**<br>Nửa chu vi đáy là $p = \\frac{4 \\cdot 3}{2} = 6\\text{ (m)}$.<br>Diện tích xung quanh của mái chòi là:<br>$$S_{xq} = p \\cdot d = 6 \\cdot 2{,}5 = 15\\text{ (m}^2\\text{)}$$ |

### Hoạt động 2.2: Chữa bài toán Hình học phẳng tổng hợp (15 phút)
a) Mục tiêu: Chữa chi tiết câu hình học phẳng tổng hợp, phân tích phương pháp tư duy câu phân loại điểm 10.
b) Nội dung: Chữa Bài 2 tự luận: Tam giác đồng dạng và phân giác.
c) Sản phẩm: Lời giải hoàn chỉnh câu a, b, c trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gọi 2 HS lên bảng chữa câu a, b.<br>- GV trực tiếp phân tích câu c (chứng minh $BA \\cdot CE = BC \\cdot AE$).<br>- **HS:** Chú ý lắng nghe hướng dẫn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Câu c: Xét $\\Delta BAE$ và $\\Delta BCE$ hoặc dùng tính chất phân giác để lập tỉ số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu ý tưởng chứng minh hai tam giác đồng dạng chứa các đoạn thẳng trên.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa lời giải mẫu mực lên bảng. | **Chữa Bài 2:**<br>a) $\\Delta HBA \\backsim \\Delta ABC$ (g.g) suy ra $AB^2 = BH \\cdot BC$.<br>b) $AC = \\sqrt{25^2 - 15^2} = 20\\text{ (cm)}$.<br>$$AH = \\frac{15 \\cdot 20}{25} = 12\\text{ (cm)}$$<br>$$BH = \\frac{15^2}{25} = 9\\text{ (cm)}$$<br>c) Do $BD$ là phân giác nên góc bằng nhau. Sử dụng tam giác vuông đồng dạng chứng minh $\\frac{BA}{BC} = \\frac{AE}{CE} \\Rightarrow BA \\cdot CE = BC \\cdot AE$. |

## C. HỌC SINH TỰ SỬA BÀI VÀ THẮC MẮC (HOẠT ĐỘNG 3) (7 phút)
a) Mục tiêu: Học sinh tự sửa lỗi sai vào vở bằng bút đỏ và giải đáp thắc mắc về điểm số.
b) Nội dung: HS tự rà soát lại bài kiểm tra và trao đổi với giáo viên nếu có khiếu nại điểm chính đáng.
c) Sản phẩm: Vở ghi có bài chữa hoàn chỉnh bằng mực đỏ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho thời gian để HS tự sửa bài vào vở và giải đáp thắc mắc điểm số.<br>- **HS:** Chữa bài cẩn thận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Soát lại điểm thành phần từng câu khớp với điểm tổng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- GV giải đáp thắc mắc thỏa đáng cho từng học sinh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Thu lại bài kiểm tra để lưu trữ hồ sơ theo quy định. | Học sinh chữa bài cẩn thận vào vở và giải đáp thắc mắc điểm số. |

## D. TỔNG KẾT NĂM HỌC VÀ HƯỚNG DẪN HỌC HÈ (HOẠT ĐỘNG 4) (3 phút)
a) Mục tiêu: Đánh giá sự tiến bộ của học sinh trong cả năm học môn Toán 8 và dặn dò ôn tập hè chuẩn bị lên lớp 9.
b) Nội dung: GV tổng kết chặng đường môn Toán 8 và giao nhiệm vụ tự học trong kì nghỉ hè.
c) Sản phẩm: Kế hoạch tự học hè môn Toán của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tổng kết: Chúc mừng cả lớp đã hoàn thành xuất sắc chương trình Toán 8. Môn Toán 9 năm tới là năm cuối cấp rất quan trọng cho kì thi vào lớp 10.<br>- **HS:** Lắng nghe và tiếp thu.<br><br>**+ Bước 2: Hướng dẫn tự học hè**<br>- **GV:** Dặn dò ôn chắc hằng đẳng thức, phân thức, tam giác đồng dạng và định lí Pythagore trong hè.<br><br>**+ Bước 3: Kết thúc tiết học**<br>- Cả lớp chào giáo viên kết thúc năm học. | Tổng kết môn Toán 8 và định hướng chuẩn bị cho môn Toán 9. |
"""
    },
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print(f"Hoàn tất tạo đợt 2 (7 bài Chương X & Ôn tập cuối HK2 Tiết 48 - 57)!")
