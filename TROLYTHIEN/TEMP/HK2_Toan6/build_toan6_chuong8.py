# -*- coding: utf-8 -*-
"""
Script sinh 14 KHBD Chương VIII: Hình học cơ bản (Tiết 23 - 39) - Toán 6 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Ký hiệu góc \\widehat{...} - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan6"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    {
        "filename": "17_KHBD_Toan6_Bai32_DiemVaDuongThang_Tiet23-24.md",
        "header": "TIẾT 23, 24 - BÀI 32: ĐIỂM VÀ ĐƯỜNG THẲNG\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 23, 24 - BÀI 32: ĐIỂM VÀ ĐƯỜNG THẲNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết các khái niệm cơ bản không định nghĩa: Điểm, đường thẳng; cách đặt tên điểm (chữ cái in hoa $A, B, C,...$) và tên đường thẳng (chữ cái in thường $a, b, d,...$ hoặc qua hai điểm $AB$).
- Nắm vững quan hệ điểm thuộc/không thuộc đường thẳng ($A \\in d, B \\notin d$).
- Hiểu và vẽ được ba điểm thẳng hàng, ba điểm không thẳng hàng; hai đường thẳng cắt nhau, song song, trùng nhau.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát các hình ảnh thực tế (dây điện căng thẳng, mép bàn, tia laser) để hình dung đường thẳng.
- Giao tiếp và hợp tác: Làm việc nhóm vẽ hình và sử dụng đúng các ký hiệu toán học hình học.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khẳng định qua hai điểm phân biệt có một và chỉ một đường thẳng.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo thước thẳng để vẽ điểm, đường thẳng, kiểm tra tính thẳng hàng.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm hình học động GeoGebra vẽ điểm, đường thẳng và kiểm tra tính liên thuộc của điểm trên đường thẳng.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh ứng dụng AI để tạo các hình ảnh kiến trúc thực tế minh họa cho khái niệm hai đường thẳng song song và cắt nhau.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác và tỉ mỉ trong từng nét vẽ hình học.
- Ý thức giữ gìn dụng cụ học tập thước kẻ, bút chì sạch đẹp.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, thước thẳng giáo viên, bài giảng trình chiếu GeoGebra.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng có chia vạch, bút chì.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề từ thực tế hình ảnh dây đàn ghi-ta hoặc mép bảng để hình thành khái niệm điểm và đường thẳng.
b) Nội dung: Quan sát sợi dây đàn căng thẳng và chấm tròn trên phím đàn.
c) Sản phẩm: Phát biểu cảm nhận của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh sợi dây đàn ghi-ta kéo căng và các chấm tròn đánh dấu vị trí phím bấm. Hỏi: Hình ảnh đó gợi cho em khái niệm hình học nào?<br>- **HS:** Quan sát và liên hệ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chấm tròn gợi hình ảnh về điểm, sợi dây căng gợi hình ảnh đường thẳng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu bài mới: Điểm và đường thẳng là hai hình học cơ bản đầu tiên của Hình học phẳng. | Chấm nhỏ là hình ảnh của điểm; sợi chỉ căng thẳng là hình ảnh của đường thẳng. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Điểm và đường thẳng. Quan hệ thuộc/không thuộc (35 phút)
a) Mục tiêu: Biết cách đặt tên điểm, đường thẳng và viết đúng kí hiệu $\\in, \\notin$.
b) Nội dung: Tìm hiểu cách biểu diễn điểm, đường thẳng trên trang giấy.
c) Sản phẩm: Hình vẽ và kí hiệu đúng trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dùng bút chấm một chấm trên bảng và đặt tên $A$. Dùng thước vạch một đường thẳng đặt tên $d$. Chấm điểm $B$ nằm ngoài $d$. Giới thiệu kí hiệu $A \\in d$, $B \\notin d$.<br>- **HS:** Quan sát và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ vào vở một đường thẳng $a$, lấy điểm $M$ thuộc $a$ và điểm $N$ không thuộc $a$. Viết kí hiệu tương ứng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Viết bảng: $M \\in a$ và $N \\notin a$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy ước dùng chữ in hoa cho điểm, chữ in thường cho đường thẳng. | **1. Điểm và đường thẳng:**<br>- Điểm: Dùng dấu chấm nhỏ, đặt tên bằng chữ in hoa: $A, B, C,...$<br>- Đường thẳng: Dùng thước vạch một đường, đặt tên bằng chữ in thường: $a, b, m,...$<br>- Kí hiệu:<br>  + Điểm $A$ thuộc đường thẳng $d$: $A \\in d$.<br>  + Điểm $B$ không thuộc đường thẳng $d$: $B \\notin d$. |

### Hoạt động 2.2: Ba điểm thẳng hàng. Hai đường thẳng cắt nhau, song song (30 phút)
a) Mục tiêu: Hiểu khái niệm ba điểm thẳng hàng, vẽ hai đường thẳng cắt nhau (chung 1 điểm), song song (không có điểm chung).
b) Nội dung: Khái niệm thẳng hàng và các vị trí tương đối của hai đường thẳng.
c) Sản phẩm: Hình vẽ chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khi nào ba điểm được gọi là thẳng hàng? Nêu các vị trí tương đối giữa hai đường thẳng phân biệt.<br>- **HS:** Tiếp thu kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ ba điểm $A, B, C$ cùng thuộc một đường thẳng $d$. Vẽ hai đường thẳng $a, b$ cắt nhau tại $O$ và hai đường thẳng $m, n$ song song.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng vẽ hình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Ba điểm cùng thuộc một đường thẳng gọi là ba điểm thẳng hàng. Hai đường thẳng phân biệt hoặc có 1 điểm chung (cắt nhau) hoặc không có điểm chung nào (song song). | **2. Ba điểm thẳng hàng. Vị trí tương đối:**<br>- Ba điểm cùng thuộc một đường thẳng gọi là ba điểm thẳng hàng.<br>- Vị trí tương đối của hai đường thẳng phân biệt:<br>  + Cắt nhau: Có duy nhất một điểm chung.<br>  + Song song: Không có điểm chung nào. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Nhận biết vị trí tương đối và đọc đúng tên các điểm, đường thẳng trên hình vẽ.
b) Nội dung: Bài 8.1, 8.2, 8.3 SGK trang 49.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình vẽ gồm 3 đường thẳng cắt nhau từng đôi một tại 3 điểm $A, B, C$. Yêu cầu chỉ ra các điểm thuộc mỗi đường thẳng và các cặp đường thẳng cắt nhau.<br>- **HS:** Quan sát hình vẽ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết các câu trả lời vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách đọc tên đường thẳng qua hai điểm: Đường thẳng $AB, BC, CA$. | Điểm $A$ thuộc đường thẳng $AB$ và $AC$. Các cặp đường thẳng cắt nhau là: $AB$ và $AC$ (tại $A$); $AB$ và $BC$ (tại $B$); $AC$ và $BC$ (tại $C$). |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng tính thẳng hàng vào thực tiễn trồng cây thẳng hàng hoặc cắm cọc tiêu.
b) Nội dung: Giải thích cách người thợ xây dùng dây dọi hoặc dây căng để xây bức tường thẳng hàng.
c) Sản phẩm: Lời giải thích của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tại sao người thợ xây lại căng một sợi dây trước khi đặt từng viên gạch?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhờ tính chất qua hai điểm xác định duy nhất một đường thẳng, sợi dây căng tạo đường thẳng chuẩn để các viên gạch thẳng hàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, nhấn mạnh ý nghĩa thực tế của tiên đề đường thẳng. | Sợi dây căng định hình đường thẳng chuẩn giúp các viên gạch được đặt thẳng hàng, bức tường phẳng đẹp. |
"""
    },
    {
        "filename": "18_KHBD_Toan6_Bai33_DiemNamGiuaHaiDiem_Tia_Tiet25.md",
        "header": "TIẾT 25 - BÀI 33: ĐIỂM NẰM GIỮA HAI ĐIỂM. TIA\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 25 - BÀI 33: ĐIỂM NẰM GIỮA HAI ĐIỂM. TIA
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm điểm nằm giữa hai điểm (chỉ xảy ra khi ba điểm thẳng hàng).
- Hiểu định nghĩa tia (nửa đường thẳng bị giới hạn bởi một gốc): Tia $Ox$ gồm điểm $O$ và một phần đường thẳng bị chia ra bởi điểm $O$.
- Nhận biết hai tia đối nhau (chung gốc và tạo thành một đường thẳng) và hai tia trùng nhau.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự vẽ hình và phân biệt rõ gốc của tia với hướng kéo dài vô tận của tia.
- Giao tiếp và hợp tác: Trao đổi nhóm chỉ ra hai tia đối nhau trên một đường thẳng.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khẳng định trong ba điểm thẳng hàng, có một và chỉ một điểm nằm giữa hai điểm còn lại.
- Năng lực sử dụng công cụ, phương tiện học toán: Vẽ thành thạo tia, hai tia đối nhau bằng thước thẳng.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm GeoGebra vẽ tia và quan sát tính một phía của tia xuất phát từ gốc.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI giải thích khái niệm tia sáng trong vật lý học tương ứng với mô hình toán học của tia hình học.***

## 3. Về phẩm chất
- Cẩn thận, chính xác khi đặt tên tia (viết gốc trước, hướng sau: tia $Ox, Oy$).
- Ý thức học tập nghiêm túc, đam mê khám phá hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, thước thẳng, đèn laser minh họa tia sáng.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng, bút chì.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Minh họa tia qua chùm sáng đèn pin hoặc tia laser để dẫn vào bài học.
b) Nội dung: Quan sát tia sáng phát ra từ bóng đèn pin kéo dài vô tận về một phía.
c) Sản phẩm: Phát biểu của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Bật đèn pin chiếu lên bảng và hỏi: Ánh sáng phát ra từ đâu và lan truyền như thế nào?<br>- **HS:** Quan sát vệt sáng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời: Ánh sáng xuất phát từ bóng đèn và đi thẳng về một phía.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu tên gọi quen thuộc: "Tia sáng".<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Khái niệm tia trong hình học có nguồn gốc trực quan từ tia sáng. | Tia sáng xuất phát từ nguồn sáng và lan truyền vô tận về một hướng. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Điểm nằm giữa hai điểm (8 phút)
a) Mục tiêu: Hiểu rõ tính chất duy nhất của điểm nằm giữa khi ba điểm thẳng hàng.
b) Nội dung: Trực quan hóa điểm nằm giữa trên đường thẳng.
c) Sản phẩm: Vở ghi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vẽ ba điểm thẳng hàng $A, B, C$ trên đường thẳng sao cho $B$ nằm giữa $A$ và $C$. Nêu nhận xét: Hai điểm $A$ và $C$ nằm về hai phía đối với điểm $B$.<br>- **HS:** Quan sát và vẽ hình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét vị trí của ba điểm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trong ba điểm thẳng hàng, có một và chỉ một điểm nằm giữa hai điểm còn lại.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Nếu ba điểm không thẳng hàng thì không có khái niệm điểm nằm giữa. | **1. Điểm nằm giữa hai điểm:**<br>- Trong ba điểm thẳng hàng, có một và chỉ một điểm nằm giữa hai điểm còn lại.<br>- Điểm $B$ nằm giữa hai điểm $A$ và $C$ thì hai điểm $A, C$ nằm khác phía đối với $B$; hai điểm $A, B$ nằm cùng phía đối với $C$. |

### Hoạt động 2.2: Khái niệm tia. Hai tia đối nhau (12 phút)
a) Mục tiêu: Định nghĩa tia, phân biệt hai tia đối nhau và hai tia trùng nhau.
b) Nội dung: Điểm $O$ chia đường thẳng $xy$ thành hai tia đối nhau $Ox$ và $Oy$.
c) Sản phẩm: Hình vẽ và ghi chú phân biệt tia trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Lấy điểm $O$ trên đường thẳng $xy$. Điểm $O$ chia đường thẳng thành hai phần. Mỗi phần cùng với điểm $O$ gọi là một tia gốc $O$. Giới thiệu hai tia đối nhau $Ox$ và $Oy$.<br>- **HS:** Ghi nhận khái niệm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ hình vào vở và lấy điểm $A$ trên tia $Ox$. So sánh tia $Ox$ và tia $OA$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Tia $Ox$ và tia $OA$ là hai tia trùng nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Hai tia đối nhau phải chung gốc và tạo thành một đường thẳng thẳng hàng. | **2. Khái niệm tia:**<br>- Hình gồm điểm $O$ và một phần đường thẳng bị chia ra bởi điểm $O$ gọi là một tia gốc $O$ (hay nửa đường thẳng gốc $O$).<br>- Hai tia đối nhau: Hai tia chung gốc tạo thành một đường thẳng gọi là hai tia đối nhau (ví dụ: $Ox$ và $Oy$).<br>- Hai tia trùng nhau: Tia $Ox$ và tia $OA$ ($A \\in Ox$) là hai tia trùng nhau. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Rèn kỹ năng đọc tên các tia đối nhau, tia trùng nhau trên hình vẽ.
b) Nội dung: Bài 8.6, 8.7 SGK trang 52.
c) Sản phẩm: Bài làm trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho đường thẳng chứa 3 điểm theo thứ tự $A, B, C$. Hãy chỉ ra:<br>  a) Các cặp tia đối nhau gốc $B$;<br>  b) Tia trùng với tia $BA$;<br>  c) Tia đối của tia $AC$.<br>- **HS:** Nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ hình và viết câu trả lời.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Cặp tia đối nhau gốc $B$ là tia $BA$ và tia $BC$. Tia đối của tia $AC$ là tia $Ax$ (về phía ngược lại). | a) Cặp tia đối nhau gốc $B$ là: tia $BA$ và tia $BC$.<br>b) Tia trùng với tia $BA$ là tia $Bx$ (nếu đường thẳng kéo dài qua $A$).<br>c) Tia đối của tia $AB$ là tia $Ax$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhận biết ứng dụng của tia trong hải trình la bàn hoặc đồng hồ mặt trời.
b) Nội dung: Kim la bàn chỉ hướng Bắc - Nam tương ứng với hai tia đối nhau.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Quan sát chiếc la bàn, kim chỉ hướng Bắc và kim chỉ hướng Nam có tạo thành hai tia đối nhau không?<br>- **HS:** Quan sát và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét trục quay kim là gốc chung, hai đầu kim tạo thành đường thẳng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đó là hình ảnh hai tia đối nhau chung gốc là trục xoay.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định kết quả và dặn dò xem trước Bài 34. | Hai đầu kim la bàn chỉ hướng Bắc và hướng Nam là hình ảnh hai tia đối nhau chung gốc tại trục quay của la bàn. |
"""
    },
    {
        "filename": "19_KHBD_Toan6_Bai34_DoanThang_DoDaiDoanThang_Tiet26-27.md",
        "header": "TIẾT 26, 27 - BÀI 34: ĐOẠN THẲNG. ĐỘ DÀI ĐOẠN THẲNG\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 26, 27 - BÀI 34: ĐOẠN THẲNG. ĐỘ DÀI ĐOẠN THẲNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa đoạn thẳng $AB$: Là hình gồm hai điểm $A, B$ và tất cả các điểm nằm giữa $A$ và $B$.
- Nắm vững khái niệm độ dài đoạn thẳng: Mỗi đoạn thẳng có một độ dài là một số dương.
- Biết cách đo và so sánh độ dài hai đoạn thẳng (bằng nhau, lớn hơn, nhỏ hơn).
- Vận dụng tính chất: Nếu điểm $M$ nằm giữa hai điểm $A$ và $B$ thì $AM + MB = AB$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự sử dụng thước đo cm để đo đạc chính xác kích thước đồ dùng cá nhân (bút chì, quyển sách).
- Giao tiếp và hợp tác: Hợp tác nhóm thực hành đo chiều dài, chiều rộng bàn học và so sánh kết quả đo.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận nếu $AM + MB = AB$ thì điểm $M$ nằm giữa hai điểm $A$ và $B$ và ngược lại.
- Năng lực giải quyết vấn đề toán học: Tính toán độ dài các chặng đường di chuyển trong bài toán thực tế.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm GeoGebra để đo khoảng cách giữa hai điểm với độ chính xác đến hàng phần nghìn.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Ứng dụng AI mô phỏng bài toán tìm đường đi ngắn nhất giữa các địa điểm trên bản đồ vệ tinh.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng khi đọc số đo trên vạch chia thước kẻ.
- Ý thức giữ gìn độ chính xác của các dụng cụ đo lường.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, thước cuộn, thước thẳng giáo viên, máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng chia khoảng mm.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Phân biệt sự khác nhau giữa đường thẳng (kéo dài vô tận) và đoạn thẳng (bị giới hạn bởi hai đầu mút).
b) Nội dung: Cây bút chì dài $15\\text{ cm}$ là hình ảnh của đường thẳng hay đoạn thẳng?
c) Sản phẩm: Câu trả lời của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cầm một cây bút chì và hỏi: Cây bút chì có đo được chiều dài không? Hình ảnh này bị giới hạn hay kéo dài vô tận?<br>- **HS:** Quan sát cây bút.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cây bút chì có độ dài xác định và bị giới hạn bởi hai đầu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đây là hình ảnh của đoạn thẳng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu bài mới: Đoạn thẳng và độ dài đoạn thẳng. | Cây bút chì bị giới hạn ở hai đầu là hình ảnh của đoạn thẳng. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Đoạn thẳng và độ dài đoạn thẳng (35 phút)
a) Mục tiêu: Định nghĩa đoạn thẳng $AB$, cách đo và quy ước độ dài.
b) Nội dung: Định nghĩa đoạn thẳng, hai mút của đoạn thẳng, quy ước độ dài luôn là số dương.
c) Sản phẩm: Vở ghi bài và số đo đoạn thẳng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Đoạn thẳng $AB$ là hình gồm hai điểm $A, B$ và tất cả các điểm nằm giữa $A$ và $B$. Hai điểm $A, B$ gọi là hai đầu mút. Hướng dẫn cách đo độ dài bằng thước kẻ vạch chia cm.<br>- **HS:** Tiếp thu kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ hai điểm $A, B$ cách nhau $6\\text{ cm}$ vào vở. Đo độ dài đoạn thẳng $AB$ và viết $AB = 6\\text{ cm}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo: Đoạn thẳng $AB$ có độ dài $6\\text{ cm}$, hay khoảng cách giữa $A$ và $B$ là $6\\text{ cm}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Độ dài đoạn thẳng luôn là một số dương; hai điểm trùng nhau thì khoảng cách bằng $0$. | **1. Đoạn thẳng và độ dài đoạn thẳng:**<br>- Đoạn thẳng $AB$ (hay $BA$) gồm hai điểm $A, B$ và các điểm nằm giữa chúng.<br>- Mỗi đoạn thẳng có một độ dài xác định là số dương.<br>- Độ dài đoạn thẳng $AB$ kí hiệu là $AB$.<br>- So sánh hai đoạn thẳng:<br>  + $AB = CD$ nếu chúng có cùng độ dài.<br>  + $AB > CD$ nếu độ dài $AB$ lớn hơn độ dài $CD$. |

### Hoạt động 2.2: Khi nào thì $AM + MB = AB$? (30 phút)
a) Mục tiêu: Nắm vững hệ thức cộng độ dài khi một điểm nằm giữa hai điểm.
b) Nội dung: Định lý: Nếu điểm $M$ nằm giữa $A$ và $B$ thì $AM + MB = AB$ và ngược lại.
c) Sản phẩm: Lời giải bài tập tính độ dài đoạn thẳng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho điểm $M$ nằm giữa $A$ và $B$. Yêu cầu đo $AM, MB$ và $AB$. Rút ra nhận xét về tổng $AM + MB$ so với $AB$.<br>- **HS:** Đo đạc thực tế.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét: $AM + MB = AB$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu định lý tính chất cộng độ dài đoạn thẳng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Nếu $M$ nằm giữa $A$ và $B$ thì $AM + MB = AB$. Ngược lại, nếu $AM + MB = AB$ thì điểm $M$ nằm giữa $A$ và $B$. | **2. Hệ thức cộng độ dài đoạn thẳng:**<br>- Nếu điểm $M$ nằm giữa hai điểm $A$ và $B$ thì:<br>$$AM + MB = AB$$<br>- Ngược lại, nếu $AM + MB = AB$ thì điểm $M$ nằm giữa hai điểm $A$ và $B$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính độ dài đoạn thẳng chưa biết thông qua hệ thức cộng độ dài.
b) Nội dung: Bài 8.10, 8.11 SGK trang 55.
c) Sản phẩm: Lời giải bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho đoạn thẳng $AB = 8\\text{ cm}$. Điểm $C$ nằm giữa $A$ và $B$ sao cho $AC = 3\\text{ cm}$. Tính độ dài đoạn thẳng $CB$.<br>- **HS:** Đọc đề và vẽ hình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vì $C$ nằm giữa $A$ và $B$ nên $AC + CB = AB$. Thay số: $3 + CB = 8 \\Rightarrow CB = 8 - 3 = 5\\text{ cm}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy trình 3 bước: 1. Nêu điểm nằm giữa; 2. Viết hệ thức cộng; 3. Thay số và tính. | **Bài giải:**<br>Vì điểm $C$ nằm giữa hai điểm $A$ và $B$ nên ta có:<br>$$AC + CB = AB$$<br>Thay số ta được:<br>$$3 + CB = 8$$<br>$$CB = 8 - 3 = 5\\text{ (cm)}$$<br>Vậy độ dài đoạn thẳng $CB$ là $5\\text{ cm}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng hệ thức cộng độ dài tính khoảng cách đường bay quốc tế giữa các trạm trung chuyển.
b) Nội dung: Chặng bay từ Hà Nội đến Tokyo quá cảnh tại Đài Bắc.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Một máy bay bay thẳng từ điểm $A$ qua trạm trung chuyển $B$ đến điểm $C$ trên cùng một đường bay thẳng. Biết $AB = 1800\\text{ km}, BC = 2100\\text{ km}$. Tính quãng đường máy bay đã bay từ $A$ đến $C$.<br>- **HS:** Nhận đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tổng quãng đường: $AC = AB + BC = 1800 + 2100 = 3900\\text{ km}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò HS chuẩn bị bài học tiếp theo. | Quãng đường máy bay đã bay từ $A$ đến $C$ là:<br>$$AC = AB + BC = 1800 + 2100 = 3900\\text{ (km)}$$<br>Đáp số: $3900\\text{ km}$. |
"""
    },
    {
        "filename": "20_KHBD_Toan6_Bai35_TrungDiemCuaDoanThang_Tiet28.md",
        "header": "TIẾT 28 - BÀI 35: TRUNG ĐIỂM CỦA ĐOẠN THẲNG (TÍCH HỢP AI)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 28 - BÀI 35: TRUNG ĐIỂM CỦA ĐOẠN THẲNG (TÍCH HỢP AI)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa trung điểm của đoạn thẳng: Điểm $M$ nằm giữa hai điểm $A, B$ và cách đều hai điểm đó ($MA = MB = \\frac{AB}{2}$).
- Biết cách vẽ trung điểm của một đoạn thẳng bằng thước chia khoảng hoặc bằng phương pháp gấp giấy.
- Nhận biết tính đối xứng qua trung điểm trong thực tiễn và trong kiến trúc xây dựng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự gấp giấy để xác định chính xác nếp gấp là trung điểm của mép giấy hình chữ nhật.
- Giao tiếp và hợp tác: Làm việc nhóm đo đạc và xác định vị trí cân bằng của bập bênh hoặc đòn gánh.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Chứng minh một điểm là trung điểm của đoạn thẳng thỏa mãn đồng thời hai điều kiện (nằm giữa và cách đều).
- Năng lực giải quyết vấn đề toán học: Tính độ dài các đoạn thẳng dựa vào tính chất trung điểm.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm GeoGebra sử dụng công cụ "Midpoint or Center" để xác định tự động trung điểm của một đoạn thẳng bất kì.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh trải nghiệm công cụ nhận diện cử chỉ AI (AI Vision), phân tích vị trí các khớp ngón tay và nhận diện trung điểm bàn tay khi điều khiển trò chơi thực tế ảo.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, đo đạc chuẩn xác từng milimet.
- Có ý thức tìm tòi, ứng dụng công nghệ trí tuệ nhân tạo hiện đại vào phân tích hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, thước thẳng, máy chiếu, máy tính cài GeoGebra và demo ứng dụng AI Vision nhận diện cử chỉ bàn tay.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng chia khoảng mm, dải giấy thủ công.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt tình huống từ trò chơi bập bênh để nhận biết điểm tựa chính giữa là trung điểm.
b) Nội dung: Quan sát chiếc bập bênh và trả lời: Trục xoay của bập bênh được đặt ở vị trí nào của thanh gỗ?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh trò chơi bập bênh trong công viên. Trục xoay của bập bênh phải đặt ở đâu để hai bên cân bằng?<br>- **HS:** Quan sát và liên hệ thực tế.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận: Đặt chính giữa thanh bập bênh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Điểm chính giữa chia thanh gỗ thành hai phần bằng nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Điểm chính giữa đó trong toán học được gọi là trung điểm của đoạn thẳng. | Điểm chính giữa chia đoạn thẳng làm hai phần bằng nhau gọi là trung điểm của đoạn thẳng. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Định nghĩa trung điểm của đoạn thẳng (12 phút)
a) Mục tiêu: Nắm vững định nghĩa trung điểm: Điểm nằm giữa và cách đều hai mút.
b) Nội dung: Công thức $M$ nằm giữa $A, B$ và $MA = MB = \\frac{AB}{2}$.
c) Sản phẩm: Vở ghi bài và hình vẽ trung điểm của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Trung điểm $M$ của đoạn thẳng $AB$ là điểm nằm giữa hai điểm $A$ và $B$ sao cho $MA = MB$. Điểm $M$ còn được gọi là điểm chính giữa của đoạn thẳng $AB$.<br>- **HS:** Ghi nhận định nghĩa.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ đoạn thẳng $AB = 8\\text{ cm}$. Xác định vị trí điểm $M$ trên đoạn thẳng $AB$ sao cho $AM = 4\\text{ cm}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đo $MB$ thấy $MB = 4\\text{ cm}$. Vậy $MA = MB = \\frac{AB}{2} = 4\\text{ cm}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại hai điều kiện bắt buộc để $M$ là trung điểm: $M$ nằm giữa $A, B$ VÀ $MA = MB$. | **1. Trung điểm của đoạn thẳng:**<br>- Trung điểm $M$ của đoạn thẳng $AB$ là điểm nằm giữa hai điểm $A, B$ sao cho $MA = MB$.<br>- Ta có công thức:<br>$$MA = MB = \\frac{AB}{2}$$<br>- Điểm $M$ còn được gọi là điểm chính giữa của đoạn thẳng $AB$. |

### Hoạt động 2.2: Tích hợp AI - Nhận diện trung điểm trong thị giác máy tính (8 phút)
a) Mục tiêu: Trải nghiệm ứng dụng AI Vision xác định tọa độ trung điểm xương bàn tay và cơ thể người.
b) Nội dung: Trình chiếu mô hình MediaPipe/OpenPose nhận diện điểm khớp ngón tay và trung điểm xương cổ tay.
c) Sản phẩm: Báo cáo trải nghiệm công nghệ AI của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Bật camera máy tính trình chiếu demo ứng dụng nhận diện cử chỉ bàn tay bằng AI. Chỉ ra cách AI tự động tính toán trung điểm của đoạn nối giữa khớp cổ tay và đầu ngón tay để bắt chuyển động chuột trên màn hình.<br>- **HS:** Hào hứng quan sát các đường nối khung xương bàn tay hiển thị trên màn hình lớn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cử 2 đại diện lên thực hiện các cử chỉ giơ tay, di chuyển ngón tay trước camera để AI bắt tọa độ trung điểm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Thảo luận: Nhờ toán học tính trung điểm cực nhanh, máy tính có thể hiểu được cử chỉ của con người trong tích tắc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định: Toán học là nền tảng cốt lõi của công nghệ Trí tuệ Nhân tạo hiện đại. | ***Ứng dụng AI: Thuật toán AI Vision sử dụng công thức trung điểm tọa độ $M\\left(\\frac{x_A+x_B}{2}; \\frac{y_A+y_B}{2}\\right)$ để xác định tâm cử chỉ bàn tay trong thực tế ảo.*** |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính độ dài các đoạn thẳng dựa vào tính chất trung điểm.
b) Nội dung: Bài 8.13, 8.14 SGK trang 58.
c) Sản phẩm: Lời giải trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho đoạn thẳng $PQ = 10\\text{ cm}$. Gọi $I$ là trung điểm của $PQ$. Tính độ dài đoạn thẳng $PI$. Lấy điểm $K$ là trung điểm của đoạn thẳng $PI$, tính độ dài đoạn thẳng $PK$.<br>- **HS:** Nhận đề và vẽ hình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: $PI = \\frac{PQ}{2} = \\frac{10}{2} = 5\\text{ cm}$. $PK = \\frac{PI}{2} = \\frac{5}{2} = 2{,}5\\text{ cm}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt phương pháp giải tuần tự dựa vào định nghĩa trung điểm. | **Bài giải:**<br>- Vì $I$ là trung điểm của $PQ$ nên:<br>$$PI = \\frac{PQ}{2} = \\frac{10}{2} = 5\\text{ (cm)}$$<br>- Vì $K$ là trung điểm của $PI$ nên:<br>$$PK = \\frac{PI}{2} = \\frac{5}{2} = 2{,}5\\text{ (cm)}$$<br>Vậy $PI = 5\\text{ cm}$ và $PK = 2{,}5\\text{ cm}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng phương pháp gấp giấy để tìm trung điểm của một đoạn dây hoặc mép giấy.
b) Nội dung: Thực hành gấp đôi dải giấy thủ công để tìm nếp gấp trung điểm.
c) Sản phẩm: Dải giấy gấp nếp của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu mỗi HS lấy dải giấy đã chuẩn bị, gấp hai mép mút trùng khít lên nhau và miết phẳng tạo nếp gấp.<br>- **HS:** Thực hiện thao tác gấp giấy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mở dải giấy ra, quan sát nếp gấp ở chính giữa.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nếp gấp chính là trung điểm của dải giấy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kỹ năng khéo tay và dặn dò xem lại bài chuẩn bị cho tiết Luyện tập chung. | Nếp gấp tạo bởi phương pháp gấp đôi dải giấy chính là trung điểm của đoạn thẳng. |
"""
    },
    {
        "filename": "21_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet29.md",
        "header": "TIẾT 29 - LUYỆN TẬP CHUNG (TRANG 58)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 29 - LUYỆN TẬP CHUNG (TRANG 58)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và khắc sâu các kiến thức về: Điểm, đường thẳng, ba điểm thẳng hàng, tia, hai tia đối nhau, đoạn thẳng, độ dài đoạn thẳng và trung điểm của đoạn thẳng.
- Rèn luyện kỹ năng vẽ hình chính xác và lập luận hình học có căn cứ logic chặt chẽ.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa các kiến thức hình học nửa đầu HKII qua sơ đồ tư duy trực quan.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp vẽ hình và lập luận chứng minh trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận chứng minh điểm nằm giữa hoặc chứng minh trung điểm của đoạn thẳng.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thước thẳng, compa chuẩn mực, vẽ hình rõ ràng, đẹp mắt.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay để thực hiện các phép cộng trừ số thập phân trong tính toán độ dài đoạn thẳng.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI kiểm tra tính logic của các bước suy luận hình học trong lời giải của học sinh.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, tỉ mỉ, kiên nhẫn trong vẽ hình và trình bày bài giải.
- Say mê, yêu thích môn hình học phẳng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Hình học Tiết 29 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng có chia vạch mm, compa, bút chì.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tái hiện nhanh các hình ảnh hình học cơ bản qua bảng so sánh.
b) Nội dung: Phân biệt: Đường thẳng, Tia, Đoạn thẳng về số mút và khả năng đo độ dài.
c) Sản phẩm: Bảng so sánh của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: So sánh đường thẳng, tia và đoạn thẳng về: Số đầu mút và việc có đo được độ dài hay không?<br>- **HS:** Nhận câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kẻ bảng nhanh vào vở nháp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đường thẳng không có mút, không đo được; Tia có 1 gốc, không đo được; Đoạn thẳng có 2 mút, đo được độ dài xác định.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn dắt vào bài luyện tập. | Đường thẳng không bị giới hạn; Tia bị giới hạn ở gốc; Đoạn thẳng bị giới hạn ở cả hai đầu mút và đo được độ dài. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn diện các khái niệm hình học cơ bản bằng Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Hình học Tiết 29; đối chiếu các định nghĩa và tính chất.

![Sơ đồ tư duy Luyện tập chung Hình học Tiết 29](khbd-ill:mindmap-toan6-hinh-tiet29)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở ghi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 29. Yêu cầu HS phân tích các nhánh: Điểm & Đường thẳng; Thẳng hàng; Tia & Tia đối; Đoạn thẳng & Trung điểm.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoạt động nhóm đôi nhắc lại các hệ thức toán học liên quan ($AM + MB = AB$; $MA = MB = \\frac{AB}{2}$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình ngắn gọn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt lại sơ đồ kiến thức chuẩn mực. | **Hệ thống kiến thức trọng tâm:**<br>1. Điểm và đường thẳng: $A \\in d, B \\notin d$.<br>2. Ba điểm thẳng hàng: Cùng thuộc một đường thẳng.<br>3. Tia: Gốc và hướng vô tận. Hai tia đối nhau chung gốc tạo thành đường thẳng.<br>4. Đoạn thẳng: $AM + MB = AB$ khi $M$ nằm giữa $A, B$.<br>5. Trung điểm: $MA = MB = \\frac{AB}{2}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tính độ dài đoạn thẳng và chứng minh một điểm là trung điểm.
b) Nội dung: Bài 8.16, 8.17 SGK trang 58, 59.
c) Sản phẩm: Lời giải chi tiết trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho đoạn thẳng $AB = 6\\text{ cm}$. Trên tia $AB$ lấy điểm $C$ sao cho $AC = 3\\text{ cm}$.<br>  a) Điểm $C$ có nằm giữa hai điểm $A$ và $B$ không? Vì sao?<br>  b) Tính độ dài đoạn thẳng $CB$.<br>  c) Điểm $C$ có là trung điểm của đoạn thẳng $AB$ không? Vì sao?<br>- **HS:** Vẽ hình và giải bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết 3 câu.<br>- Câu a: Vì $C$ và $B$ cùng thuộc tia $AB$ mà $AC < AB$ ($3\\text{ cm} < 6\\text{ cm}$) nên điểm $C$ nằm giữa $A$ và $B$.<br>- Câu b: Do $C$ nằm giữa nên $AC + CB = AB \\Rightarrow 3 + CB = 6 \\Rightarrow CB = 3\\text{ cm}$.<br>- Câu c: Vì $C$ nằm giữa $A, B$ và $AC = CB = 3\\text{ cm}$ nên $C$ là trung điểm của đoạn thẳng $AB$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá lời giải chặt chẽ, đầy đủ căn cứ lập luận. | **Lời giải chi tiết:**<br>a) Trên tia $AB$, ta có $AC < AB$ (vì $3\\text{ cm} < 6\\text{ cm}$) nên điểm $C$ nằm giữa hai điểm $A$ và $B$.<br>b) Vì điểm $C$ nằm giữa $A$ và $B$ nên:<br>$$AC + CB = AB$$<br>$$3 + CB = 6 \\Rightarrow CB = 6 - 3 = 3\\text{ (cm)}$$<br>c) Vì điểm $C$ nằm giữa $A, B$ và $AC = CB = 3\\text{ cm}$ nên điểm $C$ là trung điểm của đoạn thẳng $AB$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng trung điểm vào thiết kế các hình học hoa văn cân đối trong đời sống.
b) Nội dung: Giới thiệu ứng dụng tính đối xứng tâm trong các logo thương hiệu nổi tiếng.
c) Sản phẩm: Báo cáo ngắn của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu logo thương hiệu hình tròn có tâm đối xứng và các nan hoa xe đạp.<br>- **HS:** Quan sát và nhận diện tâm bánh xe là trung điểm của các đường kính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò HS chuẩn bị cho bài kiểm tra giữa học kì II ở tiết sau. | Tâm đối xứng của hình tròn là trung điểm của mọi đường kính đi qua nó. |
"""
    },
    {
        "filename": "22_KHBD_Toan6_KiemTraGiuaHK2_HinhHoc_Tiet30.md",
        "header": "TIẾT 30 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 30 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ nắm vững chuẩn kiến thức kĩ năng hình học của học sinh từ Tiết 23 đến Tiết 29 (Điểm, đường thẳng, tia, đoạn thẳng, trung điểm).
- Kiểm tra kỹ năng vẽ hình chuẩn xác bằng thước thẳng và compa; khả năng trình bày bài toán tính độ dài và chứng minh trung điểm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác, nghiêm túc làm bài thi độc lập, tuân thủ đúng quy chế kiểm tra.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày bài giải hình học mạch lạc, có căn cứ lập luận chính xác.
- Năng lực sử dụng công cụ học toán: Vẽ hình đúng yêu cầu của đề bài, kí hiệu hình vẽ chuẩn mực.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay đúng quy định trong phòng thi để kiểm tra các phép cộng trừ độ dài đoạn thẳng.***

## 3. Về phẩm chất
- Trung thực, khách quan trong kiểm tra.
- Tự giác, có ý thức vươn lên trong học tập môn Toán.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận và bản đặc tả chuẩn (Trắc nghiệm 30% - Tự luận 70%), đáp án và biểu điểm.
2. Học sinh: Giấy thi, bút mực, thước thẳng chia khoảng mm, compa, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (3 phút)
a) Mục tiêu: Ổn định lớp học, tạo tâm lý thoải mái và nhắc nhở quy chế kiểm tra.
b) Nội dung: Phát đề kiểm tra.
c) Sản phẩm: Đề thi trong tay học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định trật tự phòng thi. Phát đề kiểm tra tới từng bàn.<br>- **HS:** Nhận đề, kiểm tra chất lượng in ấn của đề.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Điền đầy đủ thông tin cá nhân vào giấy thi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo ngay nếu có đề bị lỗi mờ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Phát lệnh bắt đầu làm bài. | 100% học sinh sẵn sàng bước vào bài làm. |

## B. THỰC HIỆN BÀI KIỂM TRA (HOẠT ĐỘNG 2) (40 phút)
a) Mục tiêu: Làm bài nghiêm túc, vẽ hình chính xác và lập luận bài giải chặt chẽ.
b) Nội dung: Học sinh làm bài kiểm tra theo nội dung đề thi.
c) Sản phẩm: Bài làm hoàn chỉnh trên giấy thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giám sát phòng thi nghiêm túc, nhắc nhở học sinh vẽ hình bằng bút chì hoặc bút mực rõ ràng.<br>- **HS:** Độc lập làm bài, tuyệt đối không trao đổi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm phần Trắc nghiệm trước, sau đó làm phần Tự luận vẽ hình và giải chi tiết.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Báo mốc thời gian còn lại 15 phút và 5 phút.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **HS:** Soát lại toàn bộ bài làm, đặc biệt là các bước chứng minh trung điểm. | Học sinh làm bài độc lập, nghiêm túc, vẽ hình đẹp. |

## C. THU BÀI VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (2 phút)
a) Mục tiêu: Thu bài đầy đủ theo danh sách lớp và nhận xét ý thức kiểm tra.
b) Nội dung: Thu bài thi theo dãy bàn.
c) Sản phẩm: Toàn bộ bài thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hết giờ làm bài, yêu cầu học sinh dừng bút, nộp bài theo dãy.<br>- **HS:** Dừng bút và chuyển bài lên đầu bàn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm đủ số bài thi theo sĩ số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp xác nhận sĩ số tham gia kiểm tra.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét thái độ làm bài của học sinh; dặn dò chuẩn bị thước đo góc cho Bài 36 ở tiết sau. | Thu đủ 100% bài kiểm tra theo sĩ số lớp. |
"""
    },
    {
        "filename": "23_KHBD_Toan6_Bai36_Goc_Tiet31.md",
        "header": "TIẾT 31 - BÀI 36: GÓC\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 31 - BÀI 36: GÓC
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa góc: Góc là hình gồm hai tia chung gốc. Gốc chung gọi là đỉnh của góc, hai tia gọi là hai cạnh của góc.
- Nắm vững kí hiệu góc: $\\widehat{xOy}$ hoặc $\\widehat{O}$, đỉnh viết ở giữa; kí hiệu góc bẹt (góc có hai cạnh là hai tia đối nhau).
- Nhận biết điểm nằm trong góc và điểm nằm ngoài góc.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát hình ảnh cái kéo mở, hai kim đồng hồ để nhận biết đỉnh và cạnh của góc.
- Giao tiếp và hợp tác: Làm việc nhóm chỉ ra các góc và gọi tên góc chính xác trên hình vẽ phức hợp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phân biệt góc bẹt với đường thẳng; nhận diện điểm nằm trong góc.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thước thẳng vẽ góc, đặt tên góc đúng quy chuẩn.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm GeoGebra để vẽ góc qua 3 điểm và quan sát đỉnh và hai cạnh của góc.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh ứng dụng AI để tạo ảnh minh họa các cấu trúc mái nhà tam giác có góc nhọn và góc tù trong kiến trúc cổ kính.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi ghi kí hiệu mũ góc $\\widehat{...}$ trên đỉnh góc.
- Tinh thần say mê học tập và khám phá các hình ảnh toán học trong thực tế.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, thước thẳng, compa, mô hình đồng hồ kim.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng, bút chì.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề từ thực tế hình ảnh hai kim đồng hồ tạo thành một góc.
b) Nội dung: Quan sát đồng hồ lúc 3 giờ, 6 giờ và nhận xét hình ảnh hai kim tạo ra.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh đồng hồ lúc 3 giờ và lúc 6 giờ. Hai kim đồng hồ có chung điểm gì và tạo nên hình gì?<br>- **HS:** Quan sát đồng hồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hai kim chung gốc tại trục quay.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Tạo nên hình ảnh một góc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Khái niệm góc trong hình học. | Hai kim đồng hồ chung gốc tại trục quay tạo nên hình ảnh của một góc. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Khái niệm góc và góc bẹt (12 phút)
a) Mục tiêu: Nắm vững định nghĩa góc, đỉnh, hai cạnh và góc bẹt.
b) Nội dung: Góc gồm hai tia chung gốc. Kí hiệu $\\widehat{xOy}$.
c) Sản phẩm: Vở ghi và hình vẽ góc của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Góc là hình gồm hai tia chung gốc. Gốc chung là đỉnh của góc, hai tia là hai cạnh của góc. Góc bẹt là góc có hai cạnh là hai tia đối nhau. Hướng dẫn cách viết kí hiệu góc có dấu mũ: $\\widehat{xOy}$ hoặc $\\widehat{O}$.<br>- **HS:** Ghi nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ góc $\\widehat{xOy}$ đỉnh $O$, hai cạnh $Ox, Oy$. Vẽ góc bẹt $\\widehat{uOv}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** 1 HS lên bảng vẽ hình và chỉ rõ đỉnh, hai cạnh của góc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Tên đỉnh luôn viết ở chính giữa trong kí hiệu ba chữ cái: $\\widehat{xOy}$. Luôn dùng kí hiệu mũ $\\widehat{...}$. | **1. Khái niệm góc:**<br>- Góc là hình gồm hai tia chung gốc.<br>- Gốc chung gọi là đỉnh, hai tia gọi là hai cạnh.<br>- Kí hiệu góc: $\\widehat{xOy}$ hoặc $\\widehat{yOx}$ hoặc $\\widehat{O}$.<br>- Góc bẹt: Góc có hai cạnh là hai tia đối nhau. |

### Hoạt động 2.2: Điểm nằm trong góc (8 phút)
a) Mục tiêu: Nhận biết điểm nằm bên trong góc và điểm nằm ngoài góc.
b) Nội dung: Điểm $M$ nằm trong góc $\\widehat{xOy}$ không bẹt.
c) Sản phẩm: Hình vẽ và xác định điểm trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Lấy điểm $M$ không thuộc hai cạnh của góc $\\widehat{xOy}$. Kẻ đoạn thẳng nối một điểm trên tia $Ox$ và một điểm trên tia $Oy$. Giới thiệu khái niệm điểm nằm trong góc.<br>- **HS:** Quan sát và tiếp thu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ góc và chấm điểm $M$ nằm trong góc, điểm $N$ nằm ngoài góc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chỉ rõ vị trí điểm $M$ và điểm $N$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa khái niệm điểm nằm trong góc. | **2. Điểm nằm trong góc:**<br>- Điểm $M$ nằm giữa hai tia $Ox$ và $Oy$ gọi là điểm nằm trong góc $\\widehat{xOy}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Đọc tên các góc, chỉ rõ đỉnh và các cạnh trên hình vẽ tam giác.
b) Nội dung: Bài 8.25, 8.26 SGK trang 63.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho tam giác $ABC$. Hãy viết tên tất cả các góc có đỉnh $A, B, C$ và chỉ rõ đỉnh, cạnh của từng góc.<br>- **HS:** Vẽ tam giác $ABC$ vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết tên: $\\widehat{BAC}, \\widehat{ABC}, \\widehat{BCA}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt: Một tam giác có 3 góc là $\\widehat{A}, \\widehat{B}, \\widehat{C}$. | Ba góc của tam giác $ABC$ là:<br>- Góc $\\widehat{BAC}$ (đỉnh $A$, hai cạnh $AB$ và $AC$).<br>- Góc $\\widehat{ABC}$ (đỉnh $B$, hai cạnh $BA$ và $BC$).<br>- Góc $\\widehat{BCA}$ (đỉnh $C$, hai cạnh $CA$ và $CB$). |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhận biết góc trong thực tế đời sống qua hình ảnh góc mở của chiếc quạt xòe.
b) Nội dung: Chiếc quạt nan khi xòe hết cỡ tạo thành góc gì?
c) Sản phẩm: Câu trả lời của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cầm một chiếc quạt giấy, xòe dần từ hẹp đến phẳng hoàn toàn. Khi xòe phẳng hoàn toàn thì hai nan ngoài cùng tạo thành góc gì?<br>- **HS:** Quan sát chiếc quạt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời: Tạo thành một đường thẳng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đó là hình ảnh của góc bẹt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò HS chuẩn bị thước đo góc cho Bài 37. | Chiếc quạt xòe phẳng tạo thành hình ảnh của góc bẹt. |
"""
    },
    {
        "filename": "24_KHBD_Toan6_Bai37_SoDoGoc_Tiet32-33.md",
        "header": "TIẾT 32, 33 - BÀI 37: SỐ ĐO GÓC\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 32, 33 - BÀI 37: SỐ ĐO GÓC
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết thước đo góc (thước đo độ) và đơn vị đo góc là độ ($^\\circ$). Mỗi góc có một số đo xác định, số đo của góc bẹt bằng $180^\\circ$.
- Biết cách đo góc bằng thước đo độ và so sánh hai góc dựa vào số đo của chúng.
- Phân loại góc: Góc vuông ($90^\\circ$), góc nhọn ($0^\\circ < \\text{số đo} < 90^\\circ$), góc tù ($90^\\circ < \\text{số đo} < 180^\\circ$), góc bẹt ($180^\\circ$).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đặt thước đo độ chuẩn xác (tâm thước trùng đỉnh góc, một cạnh góc đi qua vạch $0^\\circ$).
- Giao tiếp và hợp tác: Hợp tác nhóm đo các góc của êke, góc phòng học và kiểm tra kết quả chéo.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh góc nhọn, góc vuông, góc tù với góc $90^\\circ$ để phân loại nhanh.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo thước đo độ và êke để đo góc và vẽ góc theo số đo cho trước.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng phần mềm GeoGebra để đo góc tự động và xác minh tính chất góc nhọn, tù, vuông.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI mô phỏng góc tới và góc phản xạ của tia sáng khi chiếu vào gương phẳng.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi nhìn vạch độ (chọn đúng cung chia độ trong hay ngoài).
- Ý thức giữ gìn thước đo góc không bị mờ vạch số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, thước đo góc giáo viên bảng lớn, êke.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước đo độ, êke, bút chì.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tạo nhu cầu định lượng độ lớn của góc thay vì chỉ quan sát bằng mắt.
b) Nội dung: Làm thế nào để biết góc mở của chiếc cửa sổ nào rộng hơn?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh hai cánh cửa sổ đang mở ở hai độ rộng khác nhau. Làm thế nào để biết chính xác cánh cửa nào mở rộng hơn?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cần phải đo độ mở của góc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Dùng dụng cụ đo góc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Số đo góc và dụng cụ đo góc. | Để so sánh độ lớn của góc ta dùng số đo góc với đơn vị đo là độ ($^\\circ$). |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Cách đo góc và đơn vị đo góc (35 phút)
a) Mục tiêu: Nắm vững cấu tạo thước đo độ và quy trình 3 bước đo góc.
b) Nội dung: Quy trình đo góc: Tâm thước trùng đỉnh, cạnh đi qua vạch $0^\\circ$, đọc vạch chia tương ứng cạnh còn lại.
c) Sản phẩm: Vở ghi và số đo các góc thực hành đo.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu thước đo góc: Là nửa hình tròn có tâm thước và các vạch chia từ $0^\\circ$ đến $180^\\circ$. Hướng dẫn 3 bước đo góc $\\widehat{xOy}$ trên bảng lớn.<br>- **HS:** Quan sát thước đo độ cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt thước đo góc $\\widehat{xOy}$ đã vẽ trong vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng đo góc giáo viên đã vẽ và đọc kết quả: $\\widehat{xOy} = 60^\\circ$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở lưu ý: Cần chọn đúng thang đo bắt đầu từ vạch số $0$ trên cạnh góc. | **1. Cách đo góc và đơn vị đo:**<br>- Đơn vị đo góc là độ, kí hiệu là $^\\circ$.<br>- Mỗi góc có một số đo xác định.<br>- Số đo góc bẹt là $180^\\circ$.<br>- Quy trình đo:<br>  1. Đặt tâm thước trùng với đỉnh của góc.<br>  2. Xoay thước sao cho một cạnh của góc đi qua vạch số $0$ của thước.<br>  3. Cạnh còn lại của góc đi qua vạch nào thì đó là số đo của góc. |

### Hoạt động 2.2: Phân loại các góc (30 phút)
a) Mục tiêu: Phân loại rõ ràng: Góc vuông, góc nhọn, góc tù, góc bẹt.
b) Nội dung: Bảng phân loại 4 loại góc dựa vào số đo độ.
c) Sản phẩm: Bảng phân loại trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu định nghĩa các loại góc:<br>  + Góc vuông: Số đo bằng $90^\\circ$.<br>  + Góc nhọn: Số đo lớn hơn $0^\\circ$ và nhỏ hơn $90^\\circ$.<br>  + Góc tù: Số đo lớn hơn $90^\\circ$ và nhỏ hơn $180^\\circ$.<br>  + Góc bẹt: Số đo bằng $180^\\circ$.<br>- **HS:** Ghi nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân loại các góc sau: $45^\\circ, 90^\\circ, 120^\\circ, 180^\\circ, 75^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $45^\\circ, 75^\\circ$ là góc nhọn; $90^\\circ$ là góc vuông; $120^\\circ$ là góc tù; $180^\\circ$ là góc bẹt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Dùng êke có thể kiểm tra nhanh góc vuông. | **2. Phân loại góc:**<br>- Góc vuông: Có số đo bằng $90^\\circ$.<br>- Góc nhọn: $0^\\circ < \\text{số đo} < 90^\\circ$.<br>- Góc tù: $90^\\circ < \\text{số đo} < 180^\\circ$.<br>- Góc bẹt: Có số đo bằng $180^\\circ$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Đo số đo các góc của một hình tứ giác và tính tổng số đo các góc.
b) Nội dung: Bài 8.30, 8.31 SGK trang 67.
c) Sản phẩm: Bảng số đo góc trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu đo 3 góc của một chiếc thước êke hình tam giác vuông.<br>- **HS:** Dùng thước đo góc thực hiện đo.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đo được góc vuông bằng $90^\\circ$, hai góc còn lại là $45^\\circ$ và $45^\\circ$ (hoặc $30^\\circ$ và $60^\\circ$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Tổng 3 góc bằng $90^\\circ + 45^\\circ + 45^\\circ = 180^\\circ$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định tổng 3 góc của một tam giác luôn bằng $180^\\circ$. | Số đo các góc của êke là: $90^\\circ, 45^\\circ, 45^\\circ$ hoặc $90^\\circ, 30^\\circ, 60^\\circ$. Tổng 3 góc bằng $180^\\circ$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng số đo góc tính góc tạo bởi hai kim đồng hồ tại thời điểm 2 giờ, 3 giờ, 6 giờ.
b) Nội dung: Bài toán góc của kim đồng hồ.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Mặt đồng hồ chia thành 12 khoảng bằng nhau. Hỏi mỗi khoảng tương ứng với góc bao nhiêu độ? Lúc 2 giờ hai kim tạo thành góc bao nhiêu độ?<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mỗi khoảng: $360^\\circ : 12 = 30^\\circ$. Lúc 2 giờ có 2 khoảng: $30^\\circ \\cdot 2 = 60^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng: $60^\\circ$ (góc nhọn).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò xem lại bài. | - Mỗi khoảng giờ tương ứng với: $360^\\circ : 12 = 30^\\circ$.<br>- Lúc 2 giờ, góc tạo bởi kim giờ và kim phút là: $30^\\circ \\cdot 2 = 60^\\circ$ (góc nhọn). |
"""
    },
    {
        "filename": "25_KHBD_Toan6_LuyenTapChung_HinhHoc_Tiet34.md",
        "header": "TIẾT 34 - LUYỆN TẬP CHUNG (TRANG 67)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 34 - LUYỆN TẬP CHUNG (TRANG 67)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Rèn luyện kỹ năng vẽ góc theo số đo cho trước, đo góc và phân loại các góc: Vuông, nhọn, tù, bẹt.
- Khắc sâu mối quan hệ giữa các hình hình học cơ bản: Điểm, đường thẳng, tia, đoạn thẳng và góc.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự vẽ sơ đồ tư duy hệ thống các loại góc và cách phân loại dựa vào mốc $90^\\circ, 180^\\circ$.
- Giao tiếp và hợp tác: Tương tác nhóm giải các bài toán thực hành đo góc công trình xây dựng.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh độ lớn của hai góc bất kì thông qua so sánh số đo góc của chúng.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo thước đo góc vẽ góc có số đo cho trước (ví dụ $45^\\circ, 120^\\circ$).

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay thực hiện chuyển đổi đơn vị góc giữa độ, phút, giây khi cần thiết.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Ứng dụng trợ lý AI tạo đề trắc nghiệm nhận diện góc nhọn, góc tù từ hình ảnh thực tế.***

## 3. Về phẩm chất
- Cẩn thận, chính xác khi đặt thước và vẽ cạnh góc theo đúng số vạch chia.
- Tinh thần học tập chủ động, trách nhiệm và kỷ luật cao.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Hình học Tiết 34 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, thước thẳng, thước đo độ, êke, bút chì.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập nhanh các mốc số đo phân loại góc qua trò chơi hỏi đáp nhanh.
b) Nội dung: Nêu nhanh góc $89^\\circ, 90^\\circ, 91^\\circ, 179^\\circ, 180^\\circ$ thuộc loại góc nào.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đọc lần lượt các số đo góc: $89^\\circ, 90^\\circ, 91^\\circ, 180^\\circ$. Yêu cầu học sinh giơ bảng ghi loại góc tương ứng.<br>- **HS:** Đọc kỹ số đo.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết tên loại góc lên bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con: Nhọn, Vuông, Tù, Bẹt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn vào bài luyện tập chung. | $89^\\circ$: góc nhọn; $90^\\circ$: góc vuông; $91^\\circ$: góc tù; $180^\\circ$: góc bẹt. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức về góc và số đo góc qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 34; đối chiếu các đặc điểm của từng loại góc.

![Sơ đồ tư duy Luyện tập chung Hình học Tiết 34](khbd-ill:mindmap-toan6-hinh-tiet34)

c) Sản phẩm: Sơ đồ tư duy hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 34. Yêu cầu HS phân tích các nhánh: Định nghĩa góc, Kí hiệu mũ $\\widehat{...}$, Thước đo góc, 4 loại góc.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm 4 hoàn thiện bảng tóm tắt đặc trưng số đo góc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa: Lưu ý luôn dùng kí hiệu mũ $\\widehat{...}$, cấm dùng kí hiệu thô. | **Hệ thống kiến thức trọng tâm:**<br>1. Góc: Gồm hai tia chung gốc. Kí hiệu $\\widehat{xOy}$.<br>2. Đo góc: Đơn vị độ ($^\\circ$). Đo qua 3 bước chuẩn.<br>3. Bốn loại góc:<br>  + Vuông: $90^\\circ$<br>  + Nhọn: $0^\\circ < \\alpha < 90^\\circ$<br>  + Tù: $90^\\circ < \\alpha < 180^\\circ$<br>  + Bẹt: $180^\\circ$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Rèn luyện kỹ năng vẽ góc theo số đo và so sánh các góc của một hình.
b) Nội dung: Bài 8.33, 8.34 SGK trang 68.
c) Sản phẩm: Hình vẽ và số đo góc trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ:<br>  a) Vẽ góc $\\widehat{xOy} = 50^\\circ$.<br>  b) Vẽ góc $\\widehat{mIn} = 130^\\circ$.<br>  c) So sánh hai góc $\\widehat{xOy}$ và $\\widehat{mIn}$, chỉ rõ góc nào là góc nhọn, góc nào là góc tù.<br>- **HS:** Dùng thước thẳng và thước đo độ vẽ hình vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác vẽ hình cẩn thận.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng thực hiện vẽ hình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét đường nét vẽ hình, độ chính xác của góc và chốt lời giải: $\\widehat{xOy} < \\widehat{mIn}$ vì $50^\\circ < 130^\\circ$. | **Kết quả bài tập:**<br>- Vẽ đúng góc $\\widehat{xOy} = 50^\\circ$ và góc $\\widehat{mIn} = 130^\\circ$.<br>- Ta có: $\\widehat{xOy} < \\widehat{mIn}$ (vì $50^\\circ < 130^\\circ$).<br>- Góc $\\widehat{xOy}$ là góc nhọn, góc $\\widehat{mIn}$ là góc tù. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng góc vào việc điều chỉnh góc nâng của giá đỡ tấm pin mặt trời để thu nhiều năng lượng nhất.
b) Nội dung: Giới thiệu góc nâng tối ưu của tấm pin năng lượng mặt trời tại Việt Nam ($15^\\circ - 20^\\circ$).
c) Sản phẩm: Ghi chú kiến thức thực tế của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh các tấm pin năng lượng mặt trời được đặt nghiêng một góc nhọn so với mặt đất.<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận: Góc nghiêng giúp đón ánh nắng vuông góc với mặt pin nhiều nhất trong ngày.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, củng cố tầm quan trọng của góc trong kỹ thuật hiện đại. | Góc nghiêng của tấm pin năng lượng mặt trời là một góc nhọn được tính toán tối ưu theo vĩ độ địa lý. |
"""
    },
    {
        "filename": "26_KHBD_Toan6_BaiTapCuoiChuong8_Tiet35.md",
        "header": "TIẾT 35 - BÀI TẬP CUỐI CHƯƠNG VIII (TRANG 69)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 35 - BÀI TẬP CUỐI CHƯƠNG VIII (TRANG 69)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết toàn bộ kiến thức Chương VIII: Điểm, đường thẳng, tia, đoạn thẳng, độ dài đoạn thẳng, trung điểm của đoạn thẳng, góc và số đo góc.
- Củng cố kỹ năng vẽ hình hình học phẳng chuẩn mực và phân tích mối quan hệ giữa các hình.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức hình học toàn chương vào sơ đồ tư duy tổng kết; kiểm tra chéo bài vẽ hình với bạn.
- Giao tiếp và hợp tác: Tự tin thuyết trình giải thích các bước vẽ hình và lập luận chứng minh.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa các mối quan hệ hình học; chứng minh tính thẳng hàng và trung điểm.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng linh hoạt phối hợp thước thẳng, thước đo góc, compa.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay kiểm tra kết quả tính tổng, hiệu các góc và độ dài đoạn thẳng.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Nhờ AI tổng hợp bộ câu hỏi trắc nghiệm hình học trực quan giúp ôn tập chương VIII hiệu quả.***

## 3. Về phẩm chất
- Rèn luyện tính kỷ luật, tác phong khoa học và sự cẩn trọng tuyệt đối trong vẽ hình.
- Nâng cao tính tự giác và ý thức trách nhiệm trong học tập.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 35 (vector 300 DPI), tivi/máy chiếu, phiếu ôn tập.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, bộ dụng cụ vẽ hình (thước thẳng, thước đo độ, compa, êke).

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập nhanh các khái niệm chương VIII qua trò chơi ghép thẻ kiến thức.
b) Nội dung: Ghép tên hình với định nghĩa hình học tương ứng.
c) Sản phẩm: Kết quả ghép thẻ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chia lớp thành 4 đội chơi ghép nối thẻ: Tên khái niệm $\\rightarrow$ Định nghĩa/Công thức.<br>- **HS:** Các đội chuẩn bị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghép thẻ trên bảng nhóm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đối chiếu kết quả chéo giữa các đội.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn vào bài ôn tập cuối chương VIII. | Bảng nối ghép thẻ chính xác 100%. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức Chương VIII bằng Sơ đồ tư duy tổng hợp 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 35; hoàn thiện bức tranh tổng thể về hình học cơ bản.

![Sơ đồ tư duy Bài tập cuối chương VIII Tiết 35](khbd-ill:mindmap-toan6-hinh-tiet35)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy tổng kết Chương VIII. Yêu cầu HS phân tích hai trục lớn: 1. Đoạn thẳng (Điểm, Đường thẳng, Tia, Trung điểm); 2. Góc (Định nghĩa, Kí hiệu, Đo góc, 4 loại góc).<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo bàn hoàn thiện các nhánh còn thiếu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS lên bảng điền các công thức trọng tâm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa toàn bộ cấu trúc chương, nhấn mạnh tính liên kết chặt chẽ giữa các khái niệm. | **Tổng kết lý thuyết Chương VIII:**<br>- Điểm, đường thẳng, ba điểm thẳng hàng.<br>- Tia, hai tia đối nhau, hai tia trùng nhau.<br>- Đoạn thẳng: $AM + MB = AB$; Trung điểm: $MA = MB = \\frac{AB}{2}$.<br>- Góc: Kí hiệu $\\widehat{xOy}$; Đo góc; Phân loại 4 góc (Nhọn, Vuông, Tù, Bẹt). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Luyện tập giải các bài tập tổng hợp kết hợp đoạn thẳng và góc.
b) Nội dung: Bài 8.35, 8.36 SGK trang 69.
c) Sản phẩm: Lời giải trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tổng hợp: Cho đoạn thẳng $AB = 8\\text{ cm}$. Điểm $M$ là trung điểm của $AB$. Trên tia $Ax$ vuông góc với tia $AB$, lấy điểm $C$.<br>  a) Tính độ dài đoạn thẳng $AM$.<br>  b) Góc $\\widehat{BAC}$ là góc gì? Có số đo bao nhiêu độ?<br>- **HS:** Vẽ hình và làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: $AM = \\frac{AB}{2} = \\frac{8}{2} = 4\\text{ cm}$. Góc $\\widehat{BAC} = 90^\\circ$ là góc vuông.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá bài vẽ hình và cách trình bày chuẩn mực. | **Lời giải:**<br>a) Vì $M$ là trung điểm của đoạn thẳng $AB$ nên:<br>$$AM = \\frac{AB}{2} = \\frac{8}{2} = 4\\text{ (cm)}$$<br>b) Vì tia $Ax$ vuông góc với tia $AB$ nên góc $\\widehat{BAC}$ là góc vuông và có số đo bằng $90^\\circ$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Định hướng chuẩn bị cho các tiết Hoạt động thực hành trải nghiệm GeoGebra tiếp theo.
b) Nội dung: Giáo viên giới thiệu tổng quan về phần mềm GeoGebra và phân công chuẩn bị phòng máy tính.
c) Sản phẩm: Kế hoạch học tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến nội dung tiết thực hành trải nghiệm phần mềm GeoGebra ở Tiết 36. Yêu cầu chuẩn bị tài khoản và máy tính.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kiểm tra máy tính cá nhân hoặc đăng kí phòng thực hành tin học của trường.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp tổng hợp danh sách.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, dặn dò cả lớp ôn lại các thao tác vẽ hình cơ bản. | Chuẩn bị đầy đủ điều kiện kỹ thuật để thực hành phần mềm GeoGebra ở tiết sau. |
"""
    },
    {
        "filename": "27_KHBD_Toan6_HDTN_GeoGebra1_Tiet36.md",
        "header": "TIẾT 36 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA (TIẾT 1)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 36 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA (TIẾT 1)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Làm quen với giao diện phần mềm hình học động GeoGebra (Thanh bảng chọn, Vùng làm việc đồ họa, Vùng đại số).
- Sử dụng thành thạo các công cụ hình học cơ bản: Vẽ điểm, đường thẳng đi qua hai điểm, đoạn thẳng với độ dài cho trước, tia và đường thẳng song song, cắt nhau.
- Kiểm tra tính thẳng hàng của ba điểm và tính liên thuộc của điểm trên đường thẳng thông qua tương tác kéo thả chuột.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác trên máy tính, khám phá các công cụ trên thanh công cụ GeoGebra.
- Giao tiếp và hợp tác: Hỗ trợ bạn cùng bàn khắc phục sự cố phần mềm và chia sẻ sản phẩm vẽ hình đẹp.

b) Năng lực đặc thù môn Toán:
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng chuột và bàn phím máy tính để vẽ hình học động chuẩn xác.
- Năng lực tư duy và lập luận toán học: Quan sát tính bất biến của các quan hệ hình học khi di chuyển các điểm tự do.

c) Năng lực số (NLS):
- ***5.3.TC1a: Học sinh khởi động phần mềm GeoGebra, sử dụng các công cụ vẽ điểm, đoạn thẳng và lưu tệp sản phẩm định dạng .ggb vào thư mục cá nhân.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh tìm hiểu tính năng tự động gợi ý đường nét và nhận diện hình vẽ AI tích hợp trong các phần mềm vẽ hình hiện đại.***

## 3. Về phẩm chất
- Rèn luyện ý thức bảo quản thiết bị máy tính trong phòng thực hành tin học.
- Tinh thần hứng thú, say mê ứng dụng công nghệ thông tin vào học toán.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn GeoGebra (hoặc bản GeoGebra trực tuyến), máy chiếu, bài giảng hướng dẫn trực quan.
2. Học sinh: Máy vi tính, sổ tay tin học, SGK Toán 6 Tập 2 trang 70, 71.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Giới thiệu phần mềm GeoGebra và tạo hứng thú khám phá hình học động.
b) Nội dung: Quan sát giáo viên biểu diễn kéo rê một đỉnh tam giác trên màn chiếu mà hình vẽ không bị méo mó.
c) Sản phẩm: Sự hào hứng tiếp thu của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu màn hình GeoGebra, vẽ đoạn thẳng $AB$ và trung điểm $M$. Kéo điểm $A$ di chuyển, quan sát điểm $M$ luôn tự động chạy theo giữ đúng vị trí trung điểm. Hỏi: Em thấy phần mềm này có gì đặc biệt?<br>- **HS:** Quan sát trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận: Hình vẽ có thể chuyển động mà vẫn giữ nguyên tính chất toán học.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đây là hình học động.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài thực hành trải nghiệm vẽ hình với GeoGebra. | GeoGebra là phần mềm toán học động trực quan, giúp vẽ hình chính xác và duy trì các quan hệ hình học. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Làm quen giao diện và công cụ vẽ điểm, đường thẳng (12 phút)
a) Mục tiêu: Nắm vững các nút công cụ: Điểm mới (Point), Đường thẳng qua hai điểm (Line), Đoạn thẳng (Segment).
b) Nội dung: Thực hành nhấp chọn công cụ và vẽ lên vùng đồ họa.
c) Sản phẩm: Các đối tượng hình học xuất hiện trên màn hình máy tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn vị trí các nút công cụ trên thanh menu:<br>  + Nút thứ 2: Điểm mới (Point).<br>  + Nút thứ 3: Đường thẳng đi qua hai điểm (Line), Đoạn thẳng (Segment), Tia (Ray).<br>- **HS:** Quan sát và thực hành trên máy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ 3 điểm $A, B, C$. Vẽ đường thẳng $AB$, đoạn thẳng $BC$ và tia $CA$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo hoàn thành thao tác.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đi vòng quanh phòng máy hỗ trợ, chỉnh sửa thao tác cho học sinh. | Học sinh sử dụng thành thạo các công cụ: Point, Line, Segment, Ray trên thanh công cụ GeoGebra. |

### Hoạt động 2.2: Vẽ trung điểm của đoạn thẳng (8 phút)
a) Mục tiêu: Biết sử dụng công cụ Midpoint or Center để tìm trung điểm chính xác 100%.
b) Nội dung: Chọn công cụ Midpoint or Center và nhấp vào hai điểm đầu mút của đoạn thẳng.
c) Sản phẩm: Trung điểm xuất hiện trên màn hình.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn: Chọn nút Điểm $\\rightarrow$ Chọn "Midpoint or Center" $\\rightarrow$ Nhấp chuột lần lượt vào điểm $A$ và điểm $B$. Quan sát trung điểm $M$ xuất hiện.<br>- **HS:** Thực hiện trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kéo điểm $A$ hoặc $B$ để thấy $M$ luôn là trung điểm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trải nghiệm tính năng động của phần mềm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tinh thần thao tác nhanh của học sinh. | Xác định trung điểm đoạn thẳng tự động bằng công cụ "Midpoint or Center". |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tự vẽ hình mô phỏng bài toán hình học trong SGK bằng GeoGebra.
b) Nội dung: Vẽ đoạn thẳng $AB = 6\\text{ cm}$, trung điểm $M$ và đường thẳng qua $M$ vuông góc với $AB$.
c) Sản phẩm: Tệp hình vẽ trên máy tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao đề bài thực hành: Dùng GeoGebra vẽ tam giác $ABC$, xác định trung điểm của 3 cạnh tam giác.<br>- **HS:** Nhận nhiệm vụ và bắt đầu vẽ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Độc lập thực hành trên máy tính cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Chiếu bài vẽ của một số học sinh tiêu biểu lên màn hình lớn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá tính chuẩn xác và thẩm mỹ của hình vẽ. | Hình vẽ tam giác và 3 trung điểm hoàn thiện chuẩn xác trên phần mềm GeoGebra. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Biết cách lưu tệp sản phẩm và xuất ảnh hình vẽ chèn vào văn bản Word.
b) Nội dung: Thao tác: File $\\rightarrow$ Save hoặc Export Image.
c) Sản phẩm: Tệp ảnh hình vẽ được lưu trong máy.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn thao tác xuất ảnh: Vào File $\\rightarrow$ Export Image $\\rightarrow$ Copy to Clipboard hoặc Download PNG.<br>- **HS:** Thực hiện thao tác xuất ảnh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Dán ảnh vào văn bản Word kiểm tra.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác nhận xuất ảnh thành công.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò HS chuẩn bị cho tiết thực hành GeoGebra thứ hai (vẽ góc và đường tròn). | Học sinh nắm vững kỹ năng lưu tệp (.ggb) và xuất tệp ảnh (.png) từ GeoGebra. |
"""
    },
    {
        "filename": "28_KHBD_Toan6_OnTapCuoiHK2_HinhHoc_Tiet37.md",
        "header": "TIẾT 37 - ÔN TẬP CUỐI HỌC KÌ II (HÌNH HỌC)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 37 - ÔN TẬP CUỐI HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn diện các kiến thức hình học phẳng trong HKII: Điểm, đường thẳng, ba điểm thẳng hàng, tia, đoạn thẳng, trung điểm, góc và số đo góc.
- Rèn luyện kỹ năng giải các bài toán tổng hợp: Tính độ dài đoạn thẳng, chứng minh trung điểm, đo góc và phân loại góc.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức hình học HKII qua sơ đồ tư duy tổng hợp; rà soát các lỗi sai trong trình bày lời giải hình học.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp chứng minh và vẽ hình trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận logic từng bước, sử dụng đúng căn cứ định lý và tính chất hình học.
- Năng lực sử dụng công cụ, phương tiện học toán: Vẽ hình chính xác, đẹp mắt, đúng tỉ lệ đề bài.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay để kiểm tra các phép cộng trừ số đo góc và đoạn thẳng.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Sử dụng AI để tạo sơ đồ tư duy hình học trực quan ôn tập cuối học kì II.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, tỉ mỉ, tác phong làm bài thi nghiêm túc.
- Tự tin, sẵn sàng tâm thế bước vào bài kiểm tra đánh giá cuối HKII.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Ôn tập cuối HK2 Hình học Tiết 37 (vector 300 DPI), đề cương ôn tập.
2. Học sinh: SGK Toán 6 Tập 2, vở ghi, bộ dụng cụ vẽ hình, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt tư duy qua trò chơi "Giải mã hình học".
b) Nội dung: Trả lời 3 câu hỏi nhanh về điều kiện trung điểm và phân loại góc.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu nhanh 3 câu hỏi trắc nghiệm.<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết nhanh câu trả lời.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con đồng loạt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và dẫn vào bài ôn tập cuối HKII môn Hình học. | Bảng đáp án trắc nghiệm chuẩn xác của học sinh. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức hình học HKII qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 37; nhắc lại các công thức và điều kiện hình học.

![Sơ đồ tư duy Ôn tập cuối HK2 Hình học Tiết 37](khbd-ill:mindmap-toan6-hinh-tiet37)

c) Sản phẩm: Sơ đồ tư duy hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy Tiết 37. Yêu cầu HS phân tích các nhánh: 1. Đoạn thẳng & Trung điểm; 2. Góc & Phân loại góc.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo cặp đôi nhắc lại các hệ thức toán học.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Lưu ý ký hiệu góc $\\widehat{...}$, cấm bỏ quên dấu mũ hoặc dùng kí hiệu thô. | **Hệ thống kiến thức hình học HKII:**<br>1. Đoạn thẳng: $AM + MB = AB$ khi $M$ nằm giữa $A, B$; Trung điểm: $MA = MB = \\frac{AB}{2}$.<br>2. Góc: Kí hiệu $\\widehat{xOy}$; Đo góc; Phân loại: Nhọn, Vuông, Tù, Bẹt. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tự luận hình học tổng hợp trong đề cương ôn tập cuối kì.
b) Nội dung: Bài toán vẽ hình, tính độ dài và chứng minh trung điểm.
c) Sản phẩm: Lời giải hoàn thiện trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đưa đề bài: Trên tia $Ox$, lấy hai điểm $A$ và $B$ sao cho $OA = 3\\text{ cm}, OB = 6\\text{ cm}$.<br>  a) Điểm $A$ có nằm giữa hai điểm $O$ và $B$ không? Vì sao?<br>  b) Tính độ dài đoạn thẳng $AB$.<br>  c) Điểm $A$ có là trung điểm của đoạn thẳng $OB$ không? Vì sao?<br>- **HS:** Vẽ hình và làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện giải bài tập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa cách trình bày 3 bước chặt chẽ: Nêu điểm nằm giữa $\\rightarrow$ Hệ thức cộng $\\rightarrow$ Kết luận trung điểm. | **Lời giải chi tiết:**<br>a) Trên tia $Ox$, ta có $OA < OB$ (vì $3\\text{ cm} < 6\\text{ cm}$) nên điểm $A$ nằm giữa hai điểm $O$ và $B$.<br>b) Vì điểm $A$ nằm giữa $O$ và $B$ nên:<br>$$OA + AB = OB$$<br>$$3 + AB = 6 \\Rightarrow AB = 6 - 3 = 3\\text{ (cm)}$$<br>c) Vì điểm $A$ nằm giữa hai điểm $O, B$ và $OA = AB = 3\\text{ cm}$ nên điểm $A$ là trung điểm của đoạn thẳng $OB$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Dặn dò chiến thuật làm bài kiểm tra cuối học kì II môn Hình học.
b) Nội dung: Các lưu ý về dụng cụ vẽ hình và cách trình bày bài thi.
c) Sản phẩm: Kế hoạch làm bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò: Mang đầy đủ thước kẻ, thước đo độ, compa, bút chì; vẽ hình rõ ràng, ghi đúng kí hiệu góc và tên điểm.<br>- **HS:** Ghi chép lưu ý vào đầu vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kiểm tra lại túi đồ dùng học tập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác nhận sẵn sàng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em tự tin làm bài thi đạt kết quả tốt nhất. | Chuẩn bị đầy đủ dụng cụ vẽ hình và tâm thế tự tin cho bài kiểm tra cuối học kì II. |
"""
    },
    {
        "filename": "29_KHBD_Toan6_KiemTraCuoiHK2_HinhHoc_Tiet38.md",
        "header": "TIẾT 38 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 38 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện chuẩn kiến thức, kĩ năng hình học của học sinh trong toàn bộ Học kì II (Chương VIII).
- Đánh giá kỹ năng dựng hình, đo đạc, lập luận chứng minh điểm nằm giữa, tính độ dài đoạn thẳng và nhận diện phân loại góc.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác làm bài độc lập, nghiêm túc, trung thực, tuân thủ đúng quy chế phòng thi.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày bài giải hình học logic, chặt chẽ, đầy đủ căn cứ.
- Năng lực sử dụng công cụ học toán: Vẽ hình bằng thước thẳng và thước đo góc chính xác theo đúng số liệu của đề bài.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng máy tính cầm tay đúng quy chế phòng thi để kiểm tra kết quả tính toán độ dài và góc.***

## 3. Về phẩm chất
- Trung thực, khách quan, có trách nhiệm với kết quả học tập của bản thân.
- Tác phong khoa học, cẩn trọng trong từng phép tính và nét vẽ.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận và bản đặc tả chuẩn Bộ GD&ĐT (Trắc nghiệm 30% - Tự luận 70%), đáp án và biểu điểm.
2. Học sinh: Giấy thi, bút mực, thước thẳng, thước đo độ, compa, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (3 phút)
a) Mục tiêu: Ổn định tổ chức, phát đề thi và nhắc nhở thời gian làm bài.
b) Nội dung: Phát đề kiểm tra.
c) Sản phẩm: Đề thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định phòng kiểm tra, nhắc nhở quy chế thi nghiêm túc. Phát đề thi cho học sinh.<br>- **HS:** Nhận đề, kiểm tra số trang và độ rõ của đề.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Điền đầy đủ thông tin cá nhân vào giấy thi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo ngay nếu có đề bị lỗi mờ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Ra lệnh bắt đầu tính giờ làm bài. | 100% học sinh sẵn sàng bước vào bài làm. |

## B. THỰC HIỆN BÀI KIỂM TRA (HOẠT ĐỘNG 2) (40 phút)
a) Mục tiêu: Độc lập làm bài thi trắc nghiệm và tự luận.
b) Nội dung: Học sinh giải bài kiểm tra trên giấy thi.
c) Sản phẩm: Bài làm hoàn thiện của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giám sát phòng thi nghiêm túc, bao quát đảm bảo tính công bằng, khách quan.<br>- **HS:** Độc lập làm bài, không trao đổi, không quay cóp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm phần Trắc nghiệm trước, sau đó làm phần Tự luận vẽ hình và giải chi tiết.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Báo mốc thời gian còn lại 15 phút và 5 phút.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **HS:** Soát lại toàn bộ bài làm, đặc biệt là các bước chứng minh trung điểm và kí hiệu góc. | Học sinh làm bài độc lập, nghiêm túc, vẽ hình đẹp. |

## C. THU BÀI VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (2 phút)
a) Mục tiêu: Thu bài đầy đủ theo danh sách lớp và nhận xét ý thức kiểm tra.
b) Nội dung: Thu bài thi theo dãy bàn.
c) Sản phẩm: Toàn bộ bài thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hết giờ làm bài, yêu cầu học sinh dừng bút, nộp bài theo dãy.<br>- **HS:** Dừng bút và chuyển bài lên đầu bàn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm đủ số bài thi theo sĩ số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp xác nhận sĩ số tham gia kiểm tra.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét thái độ làm bài của học sinh; dặn dò chuẩn bị cho tiết trải nghiệm GeoGebra 2 ở tiết sau. | Thu đủ 100% bài kiểm tra theo sĩ số lớp. |
"""
    },
    {
        "filename": "30_KHBD_Toan6_HDTN_GeoGebra2_Tiet39.md",
        "header": "TIẾT 39 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA (TIẾT 2)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 39 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA (TIẾT 2)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng thành thạo công cụ vẽ góc theo số đo cho trước (Angle with Given Size) và đo góc (Angle) trong GeoGebra.
- Sử dụng công cụ vẽ đường tròn khi biết tâm và một điểm hoặc tâm và bán kính (Circle with Center and Radius).
- Thực hành phối hợp các công cụ vẽ hình hoa văn trang trí hình tròn cân đối, đẹp mắt.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự sáng tạo các mẫu hoa văn hình học dựa trên sự kết hợp giữa các đường tròn và góc.
- Giao tiếp và hợp tác: Làm việc nhóm thiết kế logo hoặc huy hiệu lớp học bằng phần mềm GeoGebra.

b) Năng lực đặc thù môn Toán:
- Năng lực sử dụng công cụ, phương tiện học toán: Thao tác thuần thục các lệnh vẽ hình nâng cao trong GeoGebra.
- Năng lực mô hình hoá toán học: Chuyển các ý tưởng thiết kế mỹ thuật thành các bước dựng hình hình học chính xác.

c) Năng lực số (NLS):
- ***5.3.TC1a: Sử dụng công cụ Angle và Circle trong GeoGebra để thiết kế một bức tranh hoa văn hình học và xuất bản dưới dạng tệp ảnh .png độ phân giải cao.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: Học sinh trải nghiệm công cụ AI tạo ảnh nghệ thuật (Generative AI) từ các hình mẫu hình học cơ bản do chính mình thiết kế trên GeoGebra.***

## 3. Về phẩm chất
- Say mê, hào hứng khám phá vẻ đẹp của toán học kết hợp với công nghệ thông tin và nghệ thuật.
- Rèn luyện tính kiên nhẫn, gu thẩm mỹ và tính sáng tạo không ngừng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy tính cài GeoGebra, máy chiếu, các mẫu hoa văn hình học đẹp mẫu.
2. Học sinh: Máy vi tính, vở ghi thực hành, tài liệu SGK Toán 6 Tập 2.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khơi gợi cảm hứng sáng tạo qua việc trình chiếu các mẫu hoa văn hình học phức tạp được vẽ từ các đường tròn và góc đơn giản.
b) Nội dung: Quan sát hình hoa văn "Bông hoa 6 cánh" tạo bởi các cung tròn có bán kính bằng nhau.
c) Sản phẩm: Sự thích thú của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình vẽ "Bông hoa 6 cánh" tuyệt đẹp. Hỏi: Hình này được cấu tạo từ những hình học cơ bản nào?<br>- **HS:** Quan sát hình vẽ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận: Được tạo bởi một đường tròn tâm $O$ và các đường tròn cùng bán kính có tâm nằm trên đường tròn đó.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài thực hành: Hôm nay chúng ta sẽ dùng GeoGebra để tự tay vẽ nên những tác phẩm nghệ thuật hình học này. | Các hoa văn hình học phức tạp đều bắt nguồn từ sự kết hợp khéo léo của các đường tròn và góc đơn giản. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Công cụ vẽ góc và đo góc trong GeoGebra (10 phút)
a) Mục tiêu: Biết sử dụng công cụ Angle (đo góc) và Angle with Given Size (vẽ góc có số đo cho trước).
b) Nội dung: Thực hành vẽ góc $\\widehat{xOy} = 60^\\circ$ trên màn hình GeoGebra.
c) Sản phẩm: Góc có số đo chính xác trên máy tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn công cụ:<br>  + Chọn nút Góc (Angle).<br>  + Chọn "Angle with Given Size" $\\rightarrow$ Nhấp vào điểm đầu mút, nhấp vào đỉnh, nhập số đo $60^\\circ$ và chọn chiều quay (ngược chiều kim đồng hồ).<br>- **HS:** Thực hiện trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ góc $60^\\circ$ và dùng công cụ Ray để nối tạo thành góc $\\widehat{xOy}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Hoàn thành thao tác vẽ góc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy trình vẽ góc theo số đo. | Sử dụng thành thạo công cụ "Angle with Given Size" để vẽ góc chuẩn xác. |

### Hoạt động 2.2: Công cụ vẽ đường tròn (10 phút)
a) Mục tiêu: Biết sử dụng công cụ Circle with Center and Radius để vẽ đường tròn có bán kính định sẵn.
b) Nội dung: Chọn công cụ đường tròn, nhấp tâm và nhập bán kính $R = 4$.
c) Sản phẩm: Đường tròn hiển thị trên màn hình.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn công cụ Đường tròn: Chọn nút thứ 6 $\\rightarrow$ Chọn "Circle with Center and Radius" $\\rightarrow$ Nhấp chọn tâm $\\rightarrow$ Nhập bán kính (ví dụ $4$).<br>- **HS:** Thao tác trên máy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ đường tròn tâm $O$ bán kính $4\\text{ cm}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đổi màu sắc và nét vẽ của đường tròn trong bảng thuộc tính Object Properties.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tinh thần tìm tòi trang trí màu sắc của học sinh. | Nắm vững công cụ vẽ đường tròn với bán kính cho trước và tùy biến màu sắc đường nét. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Sáng tạo vẽ bức tranh "Bông hoa 6 cánh" hoặc hoa văn trang trí đối xứng bằng GeoGebra.
b) Nội dung: Thực hành vẽ theo hướng dẫn trong SGK trang 72.
c) Sản phẩm: Tác phẩm đồ họa hình học của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ thực hành sáng tạo: Vẽ bông hoa 6 cánh bằng cách vẽ 1 đường tròn tâm $O$ bán kính $R$, sau đó lấy 1 điểm trên đường tròn làm tâm vẽ đường tròn bán kính $R$ tiếp theo, lặp lại liên tiếp 6 lần.<br>- **HS:** Nhận nhiệm vụ và say mê thực hiện.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành độc lập hoặc hỗ trợ nhau theo cặp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Chiếu các tác phẩm xuất sắc nhất lên màn chiếu phòng học.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao tính thẩm mỹ và kỹ năng tin học - toán học xuất sắc của học sinh. | Tác phẩm bông hoa 6 cánh hoàn chỉnh, các cung tròn giao nhau cân đối tuyệt đối. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Đánh giá tổng kết chuyên đề hình học và ứng dụng CNTT trong toán học lớp 6.
b) Nội dung: Tổng kết cảm nhận của học sinh sau hai tiết thực hành GeoGebra.
c) Sản phẩm: Phiếu đánh giá thu hoạch cá nhân.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS lưu tệp bài làm và nộp vào thư mục nộp bài chung của lớp trên mạng nội bộ.<br>- **HS:** Đổi tên tệp: `HoTen_Lop6_GeoGebra.ggb` và lưu bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tắt máy tính, sắp xếp bàn ghế phòng thực hành gọn gàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp kiểm tra phòng máy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương tinh thần học tập xuất sắc của cả lớp trong toàn bộ Chương VIII môn Hình học. | 100% học sinh lưu và nộp tệp sản phẩm thành công; phòng máy sạch đẹp, an toàn. |
"""
    }
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print("Hoàn tất tạo 14 KHBD Chương VIII: Hình học cơ bản (Tiết 23 - 39)!")
