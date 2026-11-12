# -*- coding: utf-8 -*-
"""
Script sinh 9 KHBD Chương VIII: Xác suất của biến cố & Ôn tập cuối HK2 & HĐTN (Tiết 69 - 80) - Toán 9 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan9"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    # 15: Bài 25 (Tiết 69)
    {
        "filename": "15_KHBD_Toan9_Bai25_PhepThuNgauNhienVaKhongGianMau_Tiet69.md",
        "md": """TIẾT 69 - BÀI 25: PHÉP THỬ NGẪU NHIÊN VÀ KHÔNG GIAN MẪU
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm phép thử ngẫu nhiên (gọi tắt là phép thử): Một hành động hoặc thí nghiệm mà kết quả của nó không thể biết trước nhưng ta biết được tập hợp tất cả các kết quả có thể xảy ra.
- Nhận biết không gian mẫu của phép thử: Tập hợp tất cả các kết quả có thể xảy ra của phép thử, kí hiệu là $\\Omega$.
- Xác định và liệt kê được các phần tử của không gian mẫu $\\Omega$, tính được số phần tử của không gian mẫu $n(\\Omega)$ cho các phép thử đơn giản (gieo đồng xu, gieo xúc xắc, chọn ngẫu nhiên thẻ số, quả cầu).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác thực hiện các phép thử ngẫu nhiên, ghi chép kết quả thí nghiệm trung thực.
- Giao tiếp và hợp tác: Làm việc nhóm thiết lập bảng liệt kê hoặc vẽ sơ đồ hình cây để xác định không gian mẫu.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng tư duy logic, liệt kê có hệ thống tránh bỏ sót hoặc trùng lặp kết quả.
- Năng lực mô hình hoá toán học: Chuyển đổi các trò chơi bốc thăm, tung súc sắc thành mô hình toán học tập hợp.

## 3. Về phẩm chất
- Khách quan, trung thực với kết quả của các phép thử ngẫu nhiên.
- Hăng say tìm tòi các quy luật ngẫu nhiên trong đời sống.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2 Kết nối tri thức, KHBD, xúc xắc 6 mặt, đồng xu, hộp đựng các quả bóng đánh số, máy chiếu.
2. Học sinh: SGK, vở ghi, đồ dùng học tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt sự tò mò thông qua trò chơi tung đồng xu hoặc gieo con xúc xắc.
b) Nội dung: Tung một đồng xu hai lần liên tiếp. Có thể biết chắc chắn trước kết quả mặt xuất hiện không? Liệt kê tất cả các khả năng có thể xảy ra.
c) Sản phẩm: Các khả năng: $(S, S), (S, N), (N, S), (N, N)$ (với $S$ là mặt sấp, $N$ là mặt ngửa).
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu tình huống tung đồng xu 2 lần liên tiếp. Liệt kê tất cả các kết quả có thể xảy ra.<br>- **HS:** Suy nghĩ và liệt kê.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lần 1 có thể ra S hoặc N, lần 2 cũng ra S hoặc N.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Có 4 kết quả: $(S; S), (S; N), (N; S), (N; N)$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Hành động tung đồng xu gọi là phép thử ngẫu nhiên, tập hợp 4 kết quả đó gọi là không gian mẫu của phép thử. | Giới thiệu phép thử ngẫu nhiên và không gian mẫu qua hành động tung đồng xu 2 lần. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Phép thử ngẫu nhiên và Không gian mẫu (25 phút)
a) Mục tiêu: Nắm vững định nghĩa phép thử ngẫu nhiên, kí hiệu không gian mẫu $\\Omega$ và số phần tử $n(\\Omega)$.
b) Nội dung: Phát biểu định nghĩa; xác định không gian mẫu khi gieo một con xúc xắc 6 mặt cân đối và đồng chất.
c) Sản phẩm: Vở ghi bài định nghĩa và ví dụ mẫu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa:<br>1. Phép thử ngẫu nhiên (phép thử) là một hành động mà ta không thể đoán trước kết quả của nó, nhưng biết tập hợp tất cả các kết quả có thể xảy ra.<br>2. Tập hợp tất cả các kết quả có thể xảy ra của phép thử gọi là không gian mẫu, kí hiệu là $\\Omega$.<br>3. Số phần tử của không gian mẫu kí hiệu là $n(\\Omega)$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định không gian mẫu khi gieo một con xúc xắc 6 mặt một lần.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $\\Omega = \\{1; 2; 3; 4; 5; 6\\}$. Số phần tử $n(\\Omega) = 6$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Mỗi phần tử của $\\Omega$ được gọi là một kết quả có thể của phép thử. | **1. Phép thử ngẫu nhiên và Không gian mẫu:**<br>- Phép thử ngẫu nhiên: Kết quả không đoán trước được nhưng biết tập mọi khả năng.<br>- Không gian mẫu $\\Omega$: Tập hợp tất cả các kết quả có thể của phép thử.<br>- Số phần tử của không gian mẫu: $n(\\Omega)$.<br>- Ví dụ: Gieo xúc xắc 1 lần: $\\Omega = \\{1; 2; 3; 4; 5; 6\\}$, $n(\\Omega) = 6$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (10 phút)
a) Mục tiêu: Liệt kê không gian mẫu của phép thử gieo hai con xúc xắc hoặc rút thẻ số bằng sơ đồ hình cây hoặc bảng 2 chiều.
b) Nội dung: Một hộp chứa 3 tấm thẻ ghi các số $1, 2, 3$. Rút ngẫu nhiên một thẻ, ghi lại số rồi bỏ lại vào hộp, sau đó rút tiếp thẻ thứ hai. Liệt kê không gian mẫu và tính $n(\\Omega)$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập rút thẻ 2 lần có hoàn lại.<br>- **HS:** Lập bảng hai chiều hoặc sơ đồ hình cây.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lần 1 có 3 khả năng, lần 2 có 3 khả năng. Tổng có $3 \\times 3 = 9$ kết quả.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng viết tập hợp $\\Omega$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt cách liệt kê theo cặp thứ tự $(x; y)$. | **Bài giải:**<br>Mỗi kết quả là một cặp số $(a; b)$ trong đó $a$ là số ghi trên thẻ rút lần thứ nhất, $b$ là số ghi trên thẻ rút lần thứ hai ($a, b \\in \\{1; 2; 3\\}$).<br>Không gian mẫu là:<br>$$\\Omega = \\{(1; 1); (1; 2); (1; 3); (2; 1); (2; 2); (2; 3); (3; 1); (3; 2); (3; 3)\\}$$<br>Số phần tử của không gian mẫu là $n(\\Omega) = 9$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Xác định số phần tử không gian mẫu khi tung đồng xu 3 lần.
b) Nội dung: Dùng quy tắc nhân tính số kết quả có thể khi tung đồng xu 3 lần liên tiếp.
c) Sản phẩm: Kết quả $n(\\Omega) = 2 \\times 2 \\times 2 = 8$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Tung đồng xu 3 lần có bao nhiêu kết quả có thể?<br>- **HS:** Áp dụng quy tắc nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $2 \\cdot 2 \\cdot 2 = 8$ kết quả.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị bài Xác suất của biến cố tiếp theo. | Số kết quả có thể khi tung đồng xu 3 lần là $2^3 = 8$. |
"""
    },

    # 16: Bài 26 (Tiết 70-71)
    {
        "filename": "16_KHBD_Toan9_Bai26_XacSuatCuaBienCo_Tiet70-71.md",
        "md": """TIẾT 70, 71 - BÀI 26: XÁC SUẤT CỦA BIẾN CỐ LIÊN QUAN TỚI PHÉP THỬ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm biến cố liên quan tới một phép thử ngẫu nhiên: Một biến cố $A$ là một tập con của không gian mẫu $\\Omega$ ($A \\subseteq \\Omega$).
- Nhận biết kết quả thuận lợi cho biến cố $A$: Những kết quả thuộc $\\Omega$ làm cho biến cố $A$ xảy ra, số lượng là $n(A)$.
- Nắm vững định nghĩa cổ điển về xác suất của biến cố trong mô hình đồng khả năng:
  $$P(A) = \\frac{n(A)}{n(\\Omega)}$$
- Nắm vững các tính chất cơ bản của xác suất: $0 \\le P(A) \\le 1$; xác suất của biến cố chắc chắn bằng $1$ ($P(\\Omega) = 1$); xác suất của biến cố không thể bằng $0$ ($P(\\emptyset) = 0$); xác suất của biến cố đối: $P(\\overline{A}) = 1 - P(A)$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đếm số kết quả thuận lợi $n(A)$ một cách cẩn thận, không bỏ sót.
- Giao tiếp và hợp tác: Cùng nhóm tính toán và phân tích xác suất trúng thưởng trong các trò chơi dân gian.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh khả năng xảy ra của các biến cố dựa trên tỉ số xác suất.
- Năng lực giải quyết vấn đề toán học: Vận dụng biến cố đối để tính xác suất các bài toán có từ "ít nhất một".

## 3. Về phẩm chất
- Khách quan, trung thực khi đánh giá xác suất các sự kiện ngẫu nhiên.
- Tránh xa các trò chơi cờ bạc đỏ đen nhờ hiểu rõ quy luật xác suất luôn bất lợi cho người chơi.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, hộp bi màu, con xúc xắc, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt sự so sánh trực giác về cơ hội xuất hiện của mặt chẵn so với mặt chia hết cho 3 khi gieo xúc xắc.
b) Nội dung: Gieo một con xúc xắc 6 mặt một lần. Khả năng xuất hiện mặt chẵn và mặt chia hết cho 3, mặt nào dễ xảy ra hơn?
c) Sản phẩm: HS chỉ ra: Mặt chẵn có 3 khả năng ($2, 4, 6$), mặt chia hết cho 3 chỉ có 2 khả năng ($3, 6$). Do đó mặt chẵn dễ xảy ra hơn.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** So sánh khả năng xuất hiện mặt chẵn và mặt chia hết cho 3 khi gieo xúc xắc.<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đếm số kết quả của từng biến cố.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Mặt chẵn có 3 số, mặt chia hết cho 3 có 2 số.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Để đo lường chính xác khả năng xảy ra của một biến cố, người ta dùng khái niệm Xác suất. | Dẫn nhập vào công thức tính xác suất cổ điển. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Biến cố và kết quả thuận lợi (30 phút)
a) Mục tiêu: Nắm vững khái niệm biến cố là tập con của $\\Omega$, tập các kết quả thuận lợi và số phần tử $n(A)$.
b) Nội dung: Xác định tập hợp $A$ và số phần tử $n(A)$.
c) Sản phẩm: Vở ghi bài định nghĩa biến cố và kết quả thuận lợi.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Biến cố $A$ liên quan đến phép thử là một tập con của không gian mẫu $\\Omega$. Các phần tử của $A$ gọi là các kết quả thuận lợi cho $A$. Kí hiệu số kết quả thuận lợi là $n(A)$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Gieo xúc xắc 1 lần. Gọi $A$ là biến cố: "Mặt xuất hiện có số chấm là số nguyên tố". Liệt kê các phần tử của $A$ và tính $n(A)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Các số nguyên tố trong $\\{1; 2; 3; 4; 5; 6\\}$ là $2, 3, 5$. Do đó $A = \\{2; 3; 5\\}$, $n(A) = 3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách trình bày biến cố dưới dạng tập hợp. | **1. Biến cố và Kết quả thuận lợi:**<br>- Biến cố $A$ là tập con của $\\Omega$: $A \\subseteq \\Omega$.<br>- Mỗi phần tử của $A$ là một kết quả thuận lợi cho $A$.<br>- Số kết quả thuận lợi cho $A$ kí hiệu là $n(A)$.<br>- Ví dụ: $A = \\{2; 3; 5\\} \\Rightarrow n(A) = 3$. |

### Hoạt động 2.2: Công thức tính xác suất của biến cố (35 phút)
a) Mục tiêu: Nắm vững công thức $P(A) = \\frac{n(A)}{n(\\Omega)}$ và các tính chất của xác suất.
b) Nội dung: Phát biểu công thức cổ điển trong mô hình đồng khả năng và biến cố đối.
c) Sản phẩm: Vở ghi công thức và lời giải ví dụ mẫu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu công thức: Giả sử các kết quả có thể của phép thử là đồng khả năng. Xác suất của biến cố $A$ là:<br>$$P(A) = \\frac{n(A)}{n(\\Omega)}$$<br>Nêu các tính chất: $0 \\le P(A) \\le 1$; $P(\\Omega) = 1$; $P(\\emptyset) = 0$.<br>Biến cố đối $\\overline{A}$: Biến cố "Không xảy ra $A$", có $P(\\overline{A}) = 1 - P(A)$.<br>- **HS:** Ghi chép công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính xác suất biến cố $A$ ở trên.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $P(A) = \\frac{n(A)}{n(\\Omega)} = \\frac{3}{6} = \\frac{1}{2} = 0{,}5$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Xác suất luôn là một số từ $0$ đến $1$, có thể viết dưới dạng phân số tối giản, số thập phân hoặc phần trăm ($50\\%$). | **2. Định nghĩa cổ điển về xác suất:**<br>Giả sử các kết quả của phép thử là đồng khả năng. Khi đó:<br>$$P(A) = \\frac{n(A)}{n(\\Omega)}$$<br>**Tính chất:**<br>- $0 \\le P(A) \\le 1$.<br>- $P(\\Omega) = 1$ (chắc chắn), $P(\\emptyset) = 0$ (không thể).<br>- Biến cố đối: $P(\\overline{A}) = 1 - P(A)$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vận dụng công thức xác suất giải bài toán rút thẻ số ngẫu nhiên.
b) Nội dung: Một hộp đựng 20 tấm thẻ được đánh số từ $1$ đến $20$. Rút ngẫu nhiên một thẻ. Tính xác suất của các biến cố:
1) $A$: "Số ghi trên thẻ là số chia hết cho 5".
2) $B$: "Số ghi trên thẻ là số chính phương".
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao đề bài toán rút thẻ từ 1 đến 20.<br>- **HS:** Xác định $n(\\Omega) = 20$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** 1) Các số chia hết cho 5: $\\{5; 10; 15; 20\\} \\Rightarrow n(A) = 4 \\Rightarrow P(A) = \\frac{4}{20} = \\frac{1}{5}$.<br>2) Các số chính phương: $\\{1; 4; 9; 16\\} \\Rightarrow n(B) = 4 \\Rightarrow P(B) = \\frac{4}{20} = \\frac{1}{5}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài giải chuẩn mực. | **Bài giải:**<br>Không gian mẫu là tập hợp 20 thẻ: $n(\\Omega) = 20$.<br>1) Các kết quả thuận lợi cho $A$ là: $5, 10, 15, 20$. Suy ra $n(A) = 4$.<br>Xác suất của biến cố $A$ là:<br>$$P(A) = \\frac{n(A)}{n(\\Omega)} = \\frac{4}{20} = \\frac{1}{5} = 0{,}2$$<br><br>2) Các kết quả thuận lợi cho $B$ là: $1, 4, 9, 16$. Suy ra $n(B) = 4$.<br>Xác suất của biến cố $B$ là:<br>$$P(B) = \\frac{n(B)}{n(\\Omega)} = \\frac{4}{20} = \\frac{1}{5} = 0{,}2$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng biến cố đối tính xác suất biến cố "có ít nhất một số chẵn" khi gieo 2 xúc xắc.
b) Nội dung: Biến cố đối của "có ít nhất một số chẵn" là "cả hai số đều lẻ".
c) Sản phẩm: Lời giải $P = 1 - \\frac{9}{36} = \\frac{27}{36} = \\frac{3}{4}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn dùng biến cố đối khi gặp cụm từ "ít nhất một".<br>- **HS:** Tính số kết quả cả 2 cùng lẻ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $3 \\times 3 = 9$ kết quả. Xác suất cả 2 lẻ là $\\frac{9}{36} = \\frac{1}{4}$. Suy ra ít nhất một chẵn là $1 - \\frac{1}{4} = \\frac{3}{4}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị tiết Luyện tập chung. | Ứng dụng biến cố đối: $P(A) = 1 - P(\\overline{A})$. |
"""
    },

    # 17: Tiết 72: Luyện tập chung (Mindmap: mindmap_toan9_tiet72.png)
    {
        "filename": "17_KHBD_Toan9_LuyenTapChung_Tiet72.md",
        "md": """TIẾT 72 - LUYỆN TẬP CHUNG: XÁC SUẤT CỦA BIẾN CỐ
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và rèn luyện thành thạo kỹ năng:
  + Xác định không gian mẫu $\\Omega$ và tính số phần tử $n(\\Omega)$ bằng phương pháp liệt kê, bảng hai chiều hoặc sơ đồ hình cây.
  + Đếm chính xác số kết quả thuận lợi $n(A)$ cho biến cố $A$.
  + Áp dụng công thức cổ điển $P(A) = \\frac{n(A)}{n(\\Omega)}$ để tính xác suất biến cố.
  + Vận dụng linh hoạt tính chất biến cố đối $P(\\overline{A}) = 1 - P(A)$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa toàn bộ kiến thức xác suất bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Cùng nhóm giải quyết bài toán xác suất có nhiều giai đoạn thực hiện.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng tư duy tổ hợp, phân loại các trường hợp biến cố không trùng lặp.
- Năng lực giải quyết vấn đề toán học: Tính toán xác suất trong các bài toán thực tế đời sống.

## 3. Về phẩm chất
- Rèn tính cẩn thận, không bỏ sót các trường hợp khi liệt kê phần tử.
- Ý thức trung thực, nghiêm túc trong học tập.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI, máy chiếu, bảng phụ.
2. Học sinh: SGK, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại công thức tính xác suất và quy tắc đếm số phần tử.
b) Nội dung: Trả lời nhanh: Gieo 2 đồng xu cân đối đồng chất cùng lúc. Xác suất để xuất hiện 2 mặt giống nhau là bao nhiêu?
c) Sản phẩm: Kết quả $n(\\Omega) = 4$, thuận lợi có $(S, S)$ và $(N, N)$ nên $P = \\frac{2}{4} = \\frac{1}{2}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi tính nhanh xác suất xuất hiện 2 mặt giống nhau.<br>- **HS:** Nhẩm nhanh kết quả.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $n(\\Omega) = 4$, thuận lợi $2$, xác suất $\\frac{2}{4} = \\frac{1}{2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang phần sơ đồ tư duy. | Khởi động: Tính nhanh xác suất phép thử hai đồng xu. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Phép thử & Xác suất bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức về phép thử ngẫu nhiên, không gian mẫu, biến cố và công thức xác suất bằng sơ đồ tư duy 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Phép thử & Xác suất biến cố.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Xác suất của biến cố Tiết 72](khbd-ill:mindmap-toan9-tiet72)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Xác suất biến cố. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Phép thử ngẫu nhiên và Không gian mẫu $\\Omega$.<br>2) Biến cố và kết quả thuận lợi $n(A)$.<br>3) Công thức xác suất cổ điển $P(A) = \\frac{n(A)}{n(\\Omega)}$.<br>4) Mô hình xác suất và biến cố đối.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích mối quan hệ giữa các nhánh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy trình 3 bước tính xác suất cổ điển: 1) Tìm $n(\\Omega)$; 2) Tìm $n(A)$; 3) Lập tỉ số. | **Hệ thống kiến thức trọng tâm:**<br>1. Phép thử và không gian mẫu $\\Omega$, số phần tử $n(\\Omega)$.<br>2. Biến cố $A \\subseteq \\Omega$, số kết quả thuận lợi $n(A)$.<br>3. Công thức: $P(A) = \\frac{n(A)}{n(\\Omega)}$ ($0 \\le P(A) \\le 1$).<br>4. Biến cố đối: $P(\\overline{A}) = 1 - P(A)$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Tính xác suất phép thử gieo đồng thời hai con xúc xắc 6 mặt.
b) Nội dung: Gieo đồng thời hai con xúc xắc cân đối và đồng chất. Tính xác suất của các biến cố:
1) $A$: "Tổng số chấm xuất hiện trên hai con xúc xắc bằng 7".
2) $B$: "Tổng số chấm xuất hiện trên hai con xúc xắc lớn hơn 9".
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gieo 2 con xúc xắc thì $n(\\Omega)$ bằng bao nhiêu? Hãy tính xác suất của $A$ và $B$.<br>- **HS:** Xác định $n(\\Omega) = 6 \\times 6 = 36$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) Tổng bằng 7: $(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1) \\Rightarrow n(A) = 6 \\Rightarrow P(A) = \\frac{6}{36} = \\frac{1}{6}$.<br>2) Tổng lớn hơn 9 (tức là 10, 11, 12):<br>- Tổng 10: $(4, 6), (5, 5), (6, 4)$ (3 cặp).<br>- Tổng 11: $(5, 6), (6, 5)$ (2 cặp).<br>- Tổng 12: $(6, 6)$ (1 cặp).<br>Suy ra $n(B) = 3 + 2 + 1 = 6 \\Rightarrow P(B) = \\frac{6}{36} = \\frac{1}{6}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán gieo 2 con xúc xắc kinh điển. | **Bài giải:**<br>Số phần tử của không gian mẫu khi gieo 2 con xúc xắc là:<br>$$n(\\Omega) = 6 \\times 6 = 36$$<br>1) Các kết quả thuận lợi cho biến cố $A$ là:<br>$$A = \\{(1; 6); (2; 5); (3; 4); (4; 3); (5; 2); (6; 1)\\}$$<br>Suy ra $n(A) = 6$. Xác suất biến cố $A$ là:<br>$$P(A) = \\frac{n(A)}{n(\\Omega)} = \\frac{6}{36} = \\frac{1}{6}$$<br><br>2) Các kết quả thuận lợi cho biến cố $B$ (tổng bằng 10, 11, 12) là:<br>$$B = \\{(4; 6); (5; 5); (6; 4); (5; 6); (6; 5); (6; 6)\\}$$<br>Suy ra $n(B) = 6$. Xác suất biến cố $B$ là:<br>$$P(B) = \\frac{n(B)}{n(\\Omega)} = \\frac{6}{36} = \\frac{1}{6}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tính xác suất tổng số chấm là số chẵn bằng lập luận đối xứng.
b) Nội dung: Trong 36 kết quả, số kết quả có tổng chẵn và tổng lẻ bằng nhau.
c) Sản phẩm: Kết quả xác suất tổng chẵn bằng $\\frac{18}{36} = \\frac{1}{2}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tổng số chấm chẵn và lẻ có khả năng bằng nhau không?<br>- **HS:** Trả lời: Bằng nhau vì tính đối xứng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mỗi loại có $18$ kết quả, xác suất bằng $\\frac{1}{2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò bài tập cuối chương VIII. | Xác suất tổng số chấm là số chẵn bằng $\\frac{1}{2}$. |
"""
    },

    # 18: Tiết 73-74: Bài tập cuối chương VIII (Mindmap: mindmap_toan9_tiet73_74.png)
    {
        "filename": "18_KHBD_Toan9_BaiTapCuoiChuong8_Tiet73-74.md",
        "md": """TIẾT 73, 74 - BÀI TẬP CUỐI CHƯƠNG VIII
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập toàn diện kiến thức Chương VIII: Xác suất của biến cố trong một số mô hình xác suất đơn giản:
  + Phép thử ngẫu nhiên, không gian mẫu $\\Omega$, số phần tử $n(\\Omega)$.
  + Biến cố $A$, tập kết quả thuận lợi, số phần tử $n(A)$.
  + Định nghĩa cổ điển về xác suất: $P(A) = \\frac{n(A)}{n(\\Omega)}$.
  + Các tính chất của xác suất, biến cố chắc chắn, biến cố không thể, biến cố đối $P(\\overline{A}) = 1 - P(A)$.
  + Mối liên hệ giữa tần số tương đối thực nghiệm và xác suất lí thuyết (Quy luật số lớn).
- Rèn luyện kỹ năng giải các bài toán tổng hợp cuối chương trong SGK.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tổng kết kiến thức Chương VIII dưới dạng sơ đồ tư duy hoàn chỉnh.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận giải các bài toán xác suất tổng hợp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng nhìn nhận tính ngẫu nhiên dưới góc nhìn toán học chặt chẽ.
- Năng lực giải quyết vấn đề toán học: Hoàn thành bài tập trắc nghiệm và tự luận tổng kết chương.

## 3. Về phẩm chất
- Rèn thói quen tư duy khoa học, cẩn trọng trong từng bước lập luận và tính toán.
- Ý thức nghiêm túc, sẵn sàng cho đợt ôn tập và kiểm tra cuối năm học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI tổng kết Chương VIII, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tái hiện nhanh các định nghĩa và công thức cốt lõi của Chương VIII.
b) Nội dung: Trả lời nhanh các câu hỏi trắc nghiệm về không gian mẫu và công thức tính xác suất cổ điển.
c) Sản phẩm: Câu trả lời chính xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi trắc nghiệm nhanh kiểm tra kiến thức Chương VIII.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại công thức $P(A) = \\frac{n(A)}{n(\\Omega)}$ và $P(\\overline{A}) = 1 - P(A)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang sơ đồ tư duy tổng kết. | Tái hiện các công thức trọng tâm Chương VIII. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Tổng kết Chương VIII bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Khái quát hóa toàn bộ cấu trúc kiến thức Chương VIII: Xác suất của biến cố.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI tổng kết Chương VIII.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Bài tập cuối chương VIII Tiết 73 - 74](khbd-ill:mindmap-toan9-tiet73-74)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI tổng kết Chương VIII. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Không gian mẫu $\\Omega$ và số phần tử $n(\\Omega)$.<br>2) Biến cố và kết quả thuận lợi $n(A)$.<br>3) Tần số tương đối và xác suất (Quy luật số lớn).<br>4) Ứng dụng thực tế (dự báo, y tế, di truyền học Mendel).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trình bày tổng quan chương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ và nhấn mạnh các dạng toán điển hình. | **Tổng kết toàn bộ Chương VIII:**<br>1. Phép thử ngẫu nhiên và không gian mẫu $\\Omega$.<br>2. Biến cố và xác suất cổ điển $P(A) = \\frac{n(A)}{n(\\Omega)}$.<br>3. Tính chất: $0 \\le P(A) \\le 1$, $P(\\overline{A}) = 1 - P(A)$.<br>4. Mối liên hệ xác suất thực nghiệm và xác suất lí thuyết. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Giải bài tập tổng hợp cuối chương trong SGK Toán 9 Tập 2.
b) Nội dung: Một túi chứa 4 viên bi đỏ, 5 viên bi xanh và 3 viên bi vàng có cùng kích thước và khối lượng. Lấy ngẫu nhiên đồng thời 2 viên bi từ túi.
1) Tính số phần tử của không gian mẫu.
2) Tính xác suất để lấy được 2 viên bi cùng màu đỏ.
3) Tính xác suất để lấy được ít nhất một viên bi màu xanh.
c) Sản phẩm: Lời giải hoàn chỉnh 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tổng số viên bi là $4 + 5 + 3 = 12$ viên bi. Lấy đồng thời 2 viên bi.<br>- **HS:** Tính số cách chọn 2 viên bi từ 12 viên: $n(\\Omega) = \\frac{12 \\cdot 11}{2} = 66$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) $n(\\Omega) = 66$.<br>2) Lấy 2 bi đỏ từ 4 bi đỏ: $n(A) = \\frac{4 \\cdot 3}{2} = 6$. Suy ra $P(A) = \\frac{6}{66} = \\frac{1}{11}$.<br>3) Dùng biến cố đối $\\overline{B}$: "Không lấy được viên bi xanh nào" (tức lấy 2 bi từ $4 + 3 = 7$ bi đỏ và vàng).<br>$n(\\overline{B}) = \\frac{7 \\cdot 6}{2} = 21 \\Rightarrow P(\\overline{B}) = \\frac{21}{66} = \\frac{7}{22}$.<br>Suy ra $P(B) = 1 - P(\\overline{B}) = 1 - \\frac{7}{22} = \\frac{15}{22}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán xác suất chọn mẫu không hoàn lại mẫu mực. | **Bài giải:**<br>Tổng số viên bi trong túi là $4 + 5 + 3 = 12$ (viên bi).<br>1) Số phần tử của không gian mẫu (số cách chọn 2 viên bi từ 12 viên) là:<br>$$n(\\Omega) = \\frac{12 \\cdot 11}{2} = 66$$<br><br>2) Gọi $A$ là biến cố: "Lấy được 2 viên bi màu đỏ". Số kết quả thuận lợi cho $A$ là:<br>$$n(A) = \\frac{4 \\cdot 3}{2} = 6$$<br>Xác suất của biến cố $A$ là:<br>$$P(A) = \\frac{n(A)}{n(\\Omega)} = \\frac{6}{66} = \\frac{1}{11}$$<br><br>3) Gọi $B$ là biến cố: "Lấy được ít nhất một viên bi màu xanh".<br>Khi đó biến cố đối $\\overline{B}$ là: "Không lấy được viên bi màu xanh nào" (cả 2 viên bi đều là đỏ hoặc vàng, tổng có $4 + 3 = 7$ viên).<br>Số kết quả thuận lợi cho $\\overline{B}$ là:<br>$$n(\\overline{B}) = \\frac{7 \\cdot 6}{2} = 21$$<br>Xác suất của biến cố đối là:<br>$$P(\\overline{B}) = \\frac{21}{66} = \\frac{7}{22}$$<br>Xác suất của biến cố $B$ là:<br>$$P(B) = 1 - P(\\overline{B}) = 1 - \\frac{7}{22} = \\frac{15}{22}$$ |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Dặn dò chuẩn bị cho tiết Hoạt động thực hành trải nghiệm GeoGebra tiếp theo.
b) Nội dung: Chuẩn bị máy vi tính phòng máy để thực hành vẽ đồ thị Parabol và giải phương trình trên GeoGebra.
c) Sản phẩm: HS ghi nhận nhiệm vụ chuẩn bị phòng máy.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị cho tiết 75 thực hành tại phòng máy tin học.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân công máy tính cho các nhóm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Lớp trưởng báo cáo sĩ số và danh sách máy tính.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở nội quy phòng máy. | Chuẩn bị cho tiết thực hành GeoGebra. |
"""
    },

    # 19: Tiết 75: HĐTN GeoGebra
    {
        "filename": "19_KHBD_Toan9_HDTN_GiaiPTVaVeDoThiGeoGebra_Tiet75.md",
        "md": """TIẾT 75 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: GIẢI PHƯƠNG TRÌNH, HỆ PHƯƠNG TRÌNH. VẼ ĐỒ THỊ HÀM SỐ BẰNG PHẦN MỀM GEOGEBRA
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng thành thạo phần mềm toán học động GeoGebra để:
  + Vẽ đồ thị hàm số bậc nhất $y = ax + b$ và hàm số bậc hai $y = ax^2$ ($a \\neq 0$).
  + Tìm tọa độ giao điểm của Parabol và đường thẳng bằng công cụ `Intersect` (Giao điểm của hai đối tượng).
  + Giải phương trình bậc hai và hệ hai phương trình bậc nhất hai ẩn bằng lệnh giải đại số `Solve` trên cửa sổ CAS.
- Trực quan hóa mối liên hệ giữa nghiệm của phương trình và hoành độ giao điểm của các đồ thị tương ứng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác trên máy tính, nhập câu lệnh chính xác và tự sửa lỗi cú pháp.
- Giao tiếp và hợp tác: Chia sẻ kinh nghiệm tạo hiệu ứng đồ họa và thanh trượt Slider trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Kết hợp giữa góc nhìn đại số (CAS) và góc nhìn hình học (Graphics) để hiểu sâu sắc bản chất toán học.
- Năng lực số (NLS):
  + ***5.3.TC2a: HS sử dụng phần mềm GeoGebra để vẽ đồ thị hàm số và giải phương trình, quan sát sự thay đổi của đồ thị khi hệ số thay đổi; 3.1.TC2a: HS xuất ảnh đồ thị hoặc tệp GeoGebra trình bày báo cáo sản phẩm thực hành.***

## 3. Về phẩm chất
- Rèn luyện kỹ năng công nghệ số, làm quen với các công cụ toán học hiện đại.
- Ý thức giữ gìn thiết bị phòng máy vi tính của nhà trường.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn phần mềm GeoGebra (hoặc trình duyệt web truy cập geogebra.org/classic), máy chiếu, bài hướng dẫn thực hành.
2. Học sinh: Máy vi tính phòng thực hành, vở ghi bài thực hành.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ GIAO NHIỆM VỤ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Giới thiệu giao diện GeoGebra và giao nhiệm vụ thực hành cho từng nhóm học sinh.
b) Nội dung: GV giới thiệu thanh công cụ, vùng làm việc đồ họa (Graphics) và dòng nhập lệnh (Input / CAS).
c) Sản phẩm: 100% học sinh mở được phần mềm GeoGebra trên màn hình máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khởi động phần mềm GeoGebra. Phổ biến 3 nhiệm vụ:<br>1. Vẽ $(P): y = x^2$ và $(d): y = 2x + 3$.<br>2. Dùng công cụ Intersect xác định tọa độ giao điểm.<br>3. Mở cửa sổ CAS giải phương trình $x^2 - 2x - 3 = 0$.<br>- **HS:** Ngồi đúng vị trí máy tính được phân công.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mở phần mềm và làm quen giao diện.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các nhóm trưởng xác nhận máy tính hoạt động tốt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Bắt đầu tiến trình thực hành. | Khởi động phần mềm và nhận nhiệm vụ thực hành GeoGebra. |

## B. TIẾN HÀNH THỰC HÀNH TRÊN MÁY TÍNH (HOẠT ĐỘNG 2) (30 phút)
### Hoạt động 2.1: Vẽ đồ thị Parabol và Đường thẳng (15 phút)
a) Mục tiêu: Nhập lệnh vẽ hàm số và sử dụng Slider thay đổi tham số.
b) Nội dung: Nhập `f(x) = x^2` và `g(x) = 2x + 3`. Dùng lệnh `Intersect(f, g)` để tìm giao điểm.
c) Sản phẩm: Màn hình hiển thị Parabol, đường thẳng và hai điểm giao $A(-1; 1)$, $B(3; 9)$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn tại dòng lệnh Input:<br>- Nhập: `y = x^2` rồi ấn Enter.<br>- Nhập: `y = 2x + 3` rồi ấn Enter.<br>- Chọn công cụ Giao điểm (Intersect) hoặc nhập `Intersect(y = x^2, y = 2x + 3)`.<br>- **HS:** Thao tác trên bàn phím.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát trên màn hình xuất hiện đường Parabol màu xanh và đường thẳng màu đỏ cắt nhau tại 2 điểm $A(-1; 1)$ và $B(3; 9)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS các nhóm kiểm tra chéo màn hình của nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét sự ăn khớp tuyệt đối giữa kết quả đại số giải tay và kết quả hình học trực quan trên GeoGebra. | Thao tác thành công vẽ đồ thị và xác định tọa độ giao điểm trên GeoGebra. |

### Hoạt động 2.2: Giải phương trình và hệ phương trình trên cửa sổ CAS (15 phút)
a) Mục tiêu: Sử dụng lệnh `Solve` trên màn hình tính toán hình thức CAS để giải phương trình bậc hai và hệ phương trình.
b) Nội dung: Vào Menu $\\rightarrow$ View $\\rightarrow$ CAS. Nhập `Solve(x^2 - 5x + 6 = 0)` và `Solve({2x + y = 5, x - y = 1})`.
c) Sản phẩm: Kết quả hiển thị nghiệm chính xác trên màn hình CAS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn mở cửa sổ CAS:<br>- Nhập: `Solve(x^2 - 5x + 6 = 0, x)` $\\rightarrow$ Kết quả: $\\{x = 2, x = 3\\}$.<br>- Nhập: `Solve({2x + y = 5, x - y = 1}, {x, y})` $\\rightarrow$ Kết quả: $\\{x = 2, y = 1\\}$.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thử nghiệm giải các phương trình có nghiệm căn thức phức tạp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** GeoGebra cho kết quả dạng căn thức chính xác tuyệt đối mà không bị làm tròn thập phân.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao khả năng tiếp thu công nghệ của học sinh. | Giải phương trình và hệ phương trình trên cửa sổ CAS của GeoGebra. |

## C. BÁO CÁO SẢN PHẨM VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (7 phút)
a) Mục tiêu: Các nhóm lưu tệp sản phẩm và chụp ảnh màn hình nộp báo cáo thực hành.
b) Nội dung: Xuất file ảnh đồ thị và nộp bài qua hệ thống mạng nội bộ trường học.
c) Sản phẩm: Tệp hình ảnh đồ thị hoàn chỉnh của các nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn lưu file `.ggb` và xuất file ảnh `.png`.<br>- **HS:** Thực hiện thao tác xuất file.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nộp tệp sản phẩm về máy giáo viên.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- GV trình chiếu 2 sản phẩm xuất sắc nhất lên màn hình lớn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương các nhóm hoàn thành nhanh và chính xác. | Báo cáo và đánh giá sản phẩm thực hành GeoGebra. |

## D. TỔNG KẾT VÀ DẶN DÒ (HOẠT ĐỘNG 4) (3 phút)
a) Mục tiêu: Tắt máy tính đúng quy trình và dặn dò ôn tập cuối học kì II.
b) Nội dung: Shutdown máy tính, tắt màn hình, kê lại ghế và dặn dò tiết ôn tập cuối kì tiếp theo.
c) Sản phẩm: Phòng máy gọn gàng, an toàn.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS tắt máy tính, xếp ghế gọn gàng.<br>- **HS:** Thực hiện trật tự.<br><br>**+ Bước 2: Dặn dò**<br>- **GV:** Chuẩn bị cho 2 tiết Ôn tập cuối HKII Đại số tiếp theo.<br><br>**+ Bước 3: Kết thúc buổi học**<br>- Cả lớp chào giáo viên ra về. | Tắt máy tính an toàn và dặn dò ôn tập cuối kì. |
"""
    },

    # 20: Tiết 76-77: Ôn tập cuối HK2 Đại số (Mindmap: mindmap_toan9_tiet76_77.png)
    {
        "filename": "20_KHBD_Toan9_OnTapCuoiHK2_DaiSoThongKeXacSuat_Tiet76-77.md",
        "md": """TIẾT 76, 77 - ÔN TẬP HỌC KÌ II (ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Đại số, Thống kê và Xác suất Học kì II môn Toán 9:
  + Chương VI: Hàm số $y = ax^2$, đồ thị Parabol, phương trình bậc hai một ẩn, định lí Viète, giải bài toán bằng cách lập phương trình.
  + Chương VII: Tần số, tần số tương đối, biểu đồ cột, đoạn thẳng, hình quạt tròn, bảng tần số ghép nhóm và biểu đồ cột liền kề Histogram.
  + Chương VIII: Phép thử ngẫu nhiên, không gian mẫu $\\Omega$, xác suất cổ điển $P(A) = \\frac{n(A)}{n(\\Omega)}$, biến cố đối.
- Rèn luyện kỹ năng tổng hợp giải các bài toán trong ma trận đề kiểm tra đánh giá cuối năm học.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức cả 3 chương dưới dạng sơ đồ tư duy liên hoàn.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải và sửa lỗi sai cho nhau trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng vận dụng linh hoạt giữa mô hình hàm số, bảng biểu thống kê và xác suất.
- Năng lực giải quyết vấn đề toán học: Phân bổ hợp lí thời gian làm bài thi cuối năm đạt điểm tối đa.

## 3. Về phẩm chất
- Cẩn thận, chính xác trong từng phép tính số học, đại số và xác suất.
- Tự tin, nghiêm túc trước kì kiểm tra đánh giá cuối năm học quan trọng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, đề cương ôn tập cuối HK2, sơ đồ tư duy vector 300 DPI, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Định hướng ôn tập và nắm rõ cấu trúc đề kiểm tra đánh giá cuối năm học phần Đại số, Thống kê, Xác suất.
b) Nội dung: GV giới thiệu ma trận đề kiểm tra cuối HK2 phần Đại số, Thống kê và Xác suất (chiếm khoảng 6,0 - 6,5 điểm trong thang điểm 10).
c) Sản phẩm: HS nắm rõ cấu trúc đề thi để có chiến lược làm bài hiệu quả.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến ma trận đề thi cuối năm: Gồm giải phương trình bậc hai, hệ thức Viète, bài toán lập phương trình thực tế, câu hỏi thống kê (bảng tần số/biểu đồ) và câu hỏi tính xác suất biến cố.<br>- **HS:** Lắng nghe và ghi chép trọng tâm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự rà soát các nội dung kiến thức còn cảm thấy chưa vững.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu các dạng bài cần thầy cô giải đáp kĩ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chiếu sơ đồ tư duy tổng kết toàn diện Đại số, Thống kê và Xác suất HK2. | Nắm vững ma trận đề kiểm tra cuối HK2 phần Đại số, Thống kê và Xác suất. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Hệ thống hóa toàn bộ kiến thức bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ Chương VI, Chương VII và Chương VIII bằng sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Ôn tập cuối HK2 Đại số 9.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Ôn tập cuối HK2 Đại số và Thống kê Xác suất Tiết 76 - 77](khbd-ill:mindmap-toan9-tiet76-77)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Ôn tập cuối HK2 Đại số 9. Yêu cầu HS phân tích 4 trụ cột chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 trụ cột:<br>1) Hàm số và PT bậc hai (Parabol, công thức nghiệm $\\Delta$, $\\Delta'$, định lí Viète).<br>2) Lập phương trình bậc hai giải bài toán thực tế.<br>3) Thống kê dữ liệu (tần số, tần số tương đối, ghép nhóm, biểu đồ quạt tròn và Histogram).<br>4) Xác suất biến cố ($P(A) = \\frac{n(A)}{n(\\Omega)}$, biến cố đối).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích các lưu ý khi giải toán.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt sơ đồ và nhấn mạnh phương pháp trình bày bài thi mạch lạc, luôn kết luận nghiệm rõ ràng $x = ...$. | **Hệ thống kiến thức Đại số, Thống kê và Xác suất HK2:**<br>1. Hàm số và PT bậc hai: Khảo sát $y = ax^2$, giải PT bằng $\\Delta$ và $\\Delta'$, hệ thức Viète.<br>2. Giải bài toán bằng cách lập phương trình chuẩn 3 bước.<br>3. Thống kê: Bảng tần số, tần số tương đối, biểu đồ cột, quạt tròn, Histogram.<br>4. Xác suất: $P(A) = \\frac{n(A)}{n(\\Omega)}$, biến cố đối. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
### Hoạt động 3.1: Luyện tập bài toán Đại số tổng hợp (30 phút)
a) Mục tiêu: Giải bài toán tương giao Parabol và ứng dụng định lí Viète tìm tham số $m$.
b) Nội dung: Cho parabol $(P): y = x^2$ và đường thẳng $(d): y = 2mx - 2m + 1$.
1) Chứng minh rằng $(d)$ luôn cắt $(P)$ tại hai điểm phân biệt với mọi giá trị của $m$.
2) Gọi $x_1, x_2$ là hoành độ các giao điểm. Tìm $m$ để $x_1^2 + x_2^2 = 2$.
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tương giao chứa tham số $m$.<br>- **HS:** Lập phương trình hoành độ giao điểm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) Phương trình: $x^2 - 2mx + 2m - 1 = 0$.<br>Biệt thức: $\\Delta' = (-m)^2 - (2m - 1) = m^2 - 2m + 1 = (m - 1)^2$.<br>Để cắt tại 2 điểm phân biệt: $\\Delta' > 0 \\Leftrightarrow (m - 1)^2 > 0 \\Leftrightarrow m \\neq 1$.<br>2) Theo Viète: $x_1 + x_2 = 2m, x_1 x_2 = 2m - 1$.<br>Ta có: $x_1^2 + x_2^2 = (x_1 + x_2)^2 - 2x_1 x_2 = 4m^2 - 2(2m - 1) = 4m^2 - 4m + 2$.<br>Theo đề: $4m^2 - 4m + 2 = 2 \\Rightarrow 4m^2 - 4m = 0 \\Rightarrow 4m(m - 1) = 0 \\Rightarrow m = 0$ hoặc $m = 1$.<br>Đối chiếu điều kiện $m \\neq 1$: Chọn $m = 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán tương giao tham số mẫu mực. | **Bài giải:**<br>1) Phương trình hoành độ giao điểm của $(P)$ và $(d)$ là:<br>$$x^2 - 2mx + 2m - 1 = 0$$<br>Biệt thức thu gọn:<br>$$\\Delta' = (-m)^2 - 1 \\cdot (2m - 1) = m^2 - 2m + 1 = (m - 1)^2$$<br>Để $(d)$ cắt $(P)$ tại hai điểm phân biệt thì:<br>$$\\Delta' > 0 \\Leftrightarrow (m - 1)^2 > 0 \\Leftrightarrow m \\neq 1$$<br><br>2) Với $m \\neq 1$, theo định lí Viète ta có:<br>$$x_1 + x_2 = 2m;\\quad x_1 x_2 = 2m - 1$$<br>Biến đổi hệ thức:<br>$$x_1^2 + x_2^2 = (x_1 + x_2)^2 - 2x_1 x_2 = (2m)^2 - 2(2m - 1) = 4m^2 - 4m + 2$$<br>Theo đề bài ta có:<br>$$4m^2 - 4m + 2 = 2$$<br>$$4m(m - 1) = 0$$<br>Suy ra $m = 0$ hoặc $m = 1$.<br>Đối chiếu điều kiện $m \\neq 1$, ta nhận $m = 0$.<br>Vậy giá trị cần tìm là $m = 0$. |

### Hoạt động 3.2: Luyện tập Thống kê và Xác suất (25 phút)
a) Mục tiêu: Giải bài toán xác suất rút bi kết hợp lập bảng phân bố tần số.
b) Nội dung: Một hộp đựng 15 quả bóng gồm 6 bóng xanh, 5 bóng đỏ và 4 bóng vàng. Rút ngẫu nhiên một quả bóng. Tính xác suất để rút được quả bóng không phải màu đỏ.
c) Sản phẩm: Lời giải $P = 1 - \\frac{5}{15} = \\frac{10}{15} = \\frac{2}{3}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập xác suất rút bóng.<br>- **HS:** Tính toán nhanh theo biến cố đối hoặc trực tiếp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thuận lợi: $6 + 4 = 10$ bóng. $P = \\frac{10}{15} = \\frac{2}{3}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và chốt phương pháp tính xác suất. | Xác suất rút được bóng không phải màu đỏ là $\\frac{2}{3}$. |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Dặn dò chuẩn bị cho tiết Kiểm tra cuối học kì II phần Đại số.
b) Nội dung: Rà soát đồ dùng và tâm thế làm bài thi.
c) Sản phẩm: HS ghi nhận đầy đủ dặn dò.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị máy tính cầm tay, bút mực cho tiết Kiểm tra cuối HKII tiếp theo.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự kiểm tra lại đồ dùng.<br><br>**+ Bước 3: Kết thúc tiết học**<br>- Cả lớp chào giáo viên. | Dặn dò chuẩn bị cho tiết Kiểm tra cuối Học kì II Đại số. |
"""
    },

    # 21: Tiết 78: Kiểm tra cuối HK2 Đại số
    {
        "filename": "21_KHBD_Toan9_KiemTraCuoiHK2_DaiSo_Tiet78.md",
        "md": """TIẾT 78 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện chuẩn kiến thức kĩ năng phần Đại số, Thống kê và Xác suất môn Toán 9 Học kì II:
  + Giải phương trình bậc hai một ẩn, ứng dụng hệ thức Viète.
  + Giải bài toán thực tế bằng cách lập phương trình.
  + Lập và đọc hiểu bảng tần số, tần số tương đối, biểu đồ thống kê.
  + Tính xác suất biến cố trong các mô hình xác suất đơn giản.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác, nghiêm túc làm bài kiểm tra độc lập, không gian lận.
- Giải quyết vấn đề: Lựa chọn phương pháp giải tối ưu, phân bổ thời gian hợp lí.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng lập luận logic, trình bày bài thi mạch lạc, sạch đẹp.
- Năng lực tính toán: Tính toán chính xác biệt thức $\\Delta$, căn bậc hai và phân số.

## 3. Về phẩm chất
- Trung thực, thẳng thắn trong kiểm tra đánh giá.
- Rèn tính cẩn trọng, kỷ luật và tinh thần vượt khó.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo đúng ma trận và đặc tả đề kiểm tra cuối kì, đáp án và biểu điểm chi tiết.
2. Học sinh: Máy tính cầm tay, bút mực, thước kẻ, giấy kiểm tra.

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
### Ma trận và Đề kiểm tra Đại số cuối HK2 (35 phút)
a) Mục tiêu: Học sinh làm bài kiểm tra độc lập, đạt kết quả cao nhất theo năng lực.
b) Nội dung: Đề gồm 2 phần: Trắc nghiệm (3 điểm) và Tự luận (7 điểm).
c) Sản phẩm: Bài làm hoàn chỉnh trên giấy thi của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Làm bài độc lập**<br>- **HS:** Làm bài nghiêm túc, tính toán cẩn thận vào giấy thi.<br>- **GV:** Giám thị bao quát lớp thi.<br><br>**+ Bước 2: Theo dõi thời gian**<br>- **GV:** Nhắc nhở thời gian làm bài (còn 15 phút, còn 5 phút).<br>- **HS:** Soát lại bài làm, kiểm tra kĩ đơn vị đo.<br><br>**+ Bước 3: Hoàn thành bài làm**<br>- **HS:** Sắp xếp lại tờ giấy thi, chuẩn bị nộp bài.<br><br>**+ Bước 4: Hết giờ làm bài**<br>- **GV:** Thu bài kiểm tra của cả lớp. | **Nội dung đề kiểm tra minh họa:**<br>**Phần I. Trắc nghiệm (3 điểm):**<br>- Câu 1: Hàm số $y = 3x^2$ đồng biến khi $x > 0$.<br>- Câu 2: Tổng hai nghiệm $x_1 + x_2 = -\\frac{b}{a}$.<br>- Câu 3: Xác suất biến cố chắc chắn bằng $1$.<br><br>**Phần II. Tự luận (7 điểm):**<br>**Bài 1 (2,0 điểm):** Cho parabol $(P): y = \\frac{1}{2}x^2$ và đường thẳng $(d): y = x + 4$. Tìm tọa độ các giao điểm của $(P)$ và $(d)$.<br>**Bài 2 (2,0 điểm):** Cho phương trình $x^2 - 2(m - 1)x + m^2 - 4 = 0$. Tìm $m$ để phương trình có hai nghiệm $x_1, x_2$ thỏa mãn $x_1^2 + x_2^2 + x_1 x_2 = 7$.<br>**Bài 3 (2,0 điểm):** Một xe ô tô đi từ tỉnh $A$ đến tỉnh $B$ dài $120\\text{ km}$. Khi về, ô tô tăng vận tốc thêm $10\\text{ km/h}$ nên thời gian về ít hơn thời gian đi là $24\\text{ phút}$. Tính vận tốc lúc đi của ô tô.<br>**Bài 4 (1,0 điểm):** Một hộp chứa 3 bi đỏ, 4 bi xanh và 5 bi vàng. Lấy ngẫu nhiên 1 viên bi. Tính xác suất lấy được viên bi màu đỏ hoặc vàng. |

## C. THU BÀI VÀ NHẬN XÉT (HOẠT ĐỘNG 3) (5 phút)
a) Mục tiêu: Thu đủ số lượng bài thi và nhận xét nền nếp buổi kiểm tra.
b) Nội dung: Thu bài theo hàng, kiểm đếm đủ số bài thi và giải tỏa căng thẳng cho học sinh.
c) Sản phẩm: Thu đủ 100% bài kiểm tra của cả lớp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thu bài kiểm tra của học sinh theo thứ tự bàn học.<br>- **HS:** Nộp bài trật tự, nghiêm túc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm khớp số bài thi với sĩ số.<br><br>**+ Bước 3: Nhận xét giờ kiểm tra**<br>- **GV:** Tuyên dương ý thức làm bài nghiêm túc, tự giác của cả lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò chuẩn bị cho 2 tiết Hoạt động thực hành trải nghiệm Excel và Gene trội tiếp theo. | Thu đủ số bài kiểm tra và nhận xét nền nếp phòng thi. |
"""
    },

    # 22: Tiết 79: HĐTN Excel Thống kê
    {
        "filename": "22_KHBD_Toan9_HDTN_ExcelThongKe_Tiet79.md",
        "md": """TIẾT 79 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: XÁC ĐỊNH TẦN SỐ, TẦN SỐ TƯƠNG ĐỐI, VẼ CÁC BIỂU ĐỒ BẰNG EXCEL
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng thành thạo phần mềm bảng tính điện tử Microsoft Excel để:
  + Nhập liệu và sử dụng hàm `COUNTIF` để tự động đếm tần số của từng giá trị trong mẫu dữ liệu lớn.
  + Thiết lập công thức tính tần số tương đối bằng phép chia `=m/N*100`.
  + Tự động vẽ các biểu đồ thống kê chuyên nghiệp: Biểu đồ cột (Column Chart), biểu đồ đường thẳng (Line Chart) và Biểu đồ hình quạt tròn (Pie Chart).
  + Định dạng, gắn nhãn dữ liệu (Data Labels), tiêu đề biểu đồ (Chart Title) và ghi chú (Legend).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác nhập liệu bảng tính, xử lý lỗi công thức `#DIV/0!`, `#VALUE!`.
- Giao tiếp và hợp tác: Hợp tác nhóm tạo bài báo cáo thống kê trực quan bằng slide hoặc tệp Excel.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Chuyển đổi dữ liệu điều tra thực tế trong trường học thành biểu đồ phân tích trực quan.
- Năng lực số (NLS):
  + ***3.1.TC2a: HS sử dụng phần mềm bảng tính để nhập dữ liệu và tự động tạo biểu đồ tần số từ bảng số liệu cho trước; 5.2.TC2b: HS lựa chọn dạng biểu đồ thích hợp (cột, quạt tròn) để thể hiện trực quan thông tin dữ liệu.***

## 3. Về phẩm chất
- Rèn luyện kỹ năng tin học văn phòng hiện đại, tác phong làm việc khoa học, ngăn nắp.
- Tinh thần trung thực với số liệu thống kê.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài Microsoft Excel, tệp dữ liệu mẫu `Du_lieu_thong_ke_9.xlsx`, máy chiếu.
2. Học sinh: Máy vi tính phòng thực hành, vở ghi chép công thức hàm Excel.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ GIAO NHIỆM VỤ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Giới thiệu tập dữ liệu điều tra 100 học sinh về môn thể thao yêu thích và đặt nhiệm vụ xử lý trên Excel.
b) Nội dung: Mở tệp Excel chứa cột dữ liệu 100 dòng ghi tên các môn thể thao: Bóng đá, Bóng rổ, Cầu lông, Bơi lội, Cờ vua.
c) Sản phẩm: 100% học sinh mở được tệp dữ liệu trên máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS mở file dữ liệu 100 học sinh. Nêu nhiệm vụ: Dùng Excel tính tần số, tần số tương đối và vẽ biểu đồ hình quạt tròn.<br>- **HS:** Mở máy và mở tệp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát bảng dữ liệu 100 hàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS xác nhận tệp dữ liệu đã sẵn sàng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Bắt đầu hướng dẫn các hàm thống kê Excel. | Khởi động và nhận tệp dữ liệu thực hành Excel. |

## B. TIẾN HÀNH THỰC HÀNH TRÊN MÁY TÍNH (HOẠT ĐỘNG 2) (30 phút)
### Hoạt động 2.1: Sử dụng hàm COUNTIF và tính tần số tương đối (15 phút)
a) Mục tiêu: Sử dụng hàm `=COUNTIF(range, criteria)` và công thức phần trăm.
b) Nội dung: Nhập công thức đếm số học sinh thích từng môn thể thao và tính phần trăm.
c) Sản phẩm: Bảng tần số và tần số tương đối tự động hoàn chỉnh trên Excel.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cú pháp hàm:<br>- Tại ô tần số môn Bóng đá, nhập: `=COUNTIF($A$2:$A$101, "Bóng đá")`. Kéo công thức cho các môn còn lại.<br>- Tại ô tổng cộng: `=SUM(B2:B6)` (kết quả phải ra đúng 100).<br>- Tại cột tần số tương đối: `=B2/$B$7*100` hoặc định dạng ô dạng `%`.<br>- **HS:** Nhập công thức theo hướng dẫn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác trên bàn phím.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Kết quả tự động hiện ra ngay lập tức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giải thích ý nghĩa dấu `$` (địa chỉ tuyệt đối) để khi copy công thức vùng dữ liệu không bị trôi. | Sử dụng thành thạo hàm COUNTIF và công thức tính phần trăm trong Excel. |

### Hoạt động 2.2: Tự động vẽ Biểu đồ quạt tròn và Biểu đồ cột (15 phút)
a) Mục tiêu: Chèn biểu đồ Pie Chart và Column Chart, thêm nhãn dữ liệu phần trăm.
b) Nội dung: Chọn vùng dữ liệu $\\rightarrow$ Insert $\\rightarrow$ Charts $\\rightarrow$ Pie $\\rightarrow$ Chọn kiểu hiển thị phần trăm.
c) Sản phẩm: Biểu đồ quạt tròn và biểu đồ cột đẹp mắt trên trang tính Excel.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn vẽ biểu đồ:<br>1. Bôi đen cột Tên môn và cột Tần số tương đối.<br>2. Chọn thẻ `Insert` $\\rightarrow$ Chọn biểu tượng `Pie Chart` (2D Pie).<br>3. Nhấp chọn `Chart Elements` ($+$) $\\rightarrow$ Tích chọn `Data Labels` để hiển thị số phần trăm trên từng múi quạt.<br>4. Đổi tên tiêu đề: BIỂU ĐỒ SỞ THÍCH MÔN THỂ THAO.<br>- **HS:** Thao tác tạo biểu đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đổi màu sắc các phần quạt và tùy chỉnh định dạng chuyên nghiệp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trình chiếu sản phẩm của nhóm lên màn hình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao thẩm mỹ và kỹ năng tin học ứng dụng của học sinh. | Tạo biểu đồ hình quạt tròn và biểu đồ cột chuyên nghiệp trong Excel. |

## C. BÁO CÁO KẾT QUẢ VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (7 phút)
a) Mục tiêu: Chấm điểm bài thực hành của các tổ và nhận xét.
b) Nội dung: GV kiểm tra file Excel trên máy của từng nhóm học sinh.
c) Sản phẩm: Điểm số thực hành của các nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thu file Excel của các nhóm qua mạng nội bộ.<br>- **HS:** Ghi tên nhóm vào file và lưu tệp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Chiếu 2 bài làm nhanh và đẹp nhất lên máy chiếu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện nhóm thuyết minh ngắn gọn về kết quả thống kê.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Cho điểm tối đa các nhóm thao tác đúng và trình bày đẹp. | Đánh giá và chấm điểm hoạt động thực hành bảng tính Excel. |

## D. TỔNG KẾT VÀ DẶN DÒ (HOẠT ĐỘNG 4) (3 phút)
a) Mục tiêu: Tắt máy tính và dặn dò tiết HĐTN tiếp theo về Di truyền học Mendel.
b) Nội dung: Chuẩn bị kiến thức môn Sinh học về lai một cặp tính trạng của Men-đen.
c) Sản phẩm: HS ghi nhận nhiệm vụ liên môn Toán - Sinh học.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tắt máy tính an toàn. Dặn dò xem lại bài Di truyền học Men-đen lớp 9.<br>- **HS:** Thực hiện trật tự.<br><br>**+ Bước 2: Kết thúc buổi học**<br>- Cả lớp chào giáo viên ra về. | Tắt máy tính an toàn và dặn dò bài liên môn Sinh học tiếp theo. |
"""
    },

    # 23: Tiết 80: HĐTN Gene trội Mendel
    {
        "filename": "23_KHBD_Toan9_HDTN_GeneTroiMendel_Tiet80.md",
        "md": """TIẾT 80 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: GENE TRỘI TRONG CÁC THẾ HỆ LAI
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng mô hình xác suất của biến cố để giải thích định luật phân li của Men-đen (Gregor Mendel) trong di truyền học sinh học:
  + Phép lai một cặp tính trạng dị hợp $Aa \\times Aa$.
  + Xác định không gian mẫu kết hợp giao tử: $\\Omega = \\{AA; Aa; aA; aa\\}$ với $n(\\Omega) = 4$.
  + Tính xác suất xuất hiện kiểu gene đồng hợp trội ($AA$), dị hợp ($Aa$), đồng hợp lặn ($aa$): Tỉ lệ kiểu gene $1 AA : 2 Aa : 1 aa$.
  + Tính xác suất xuất hiện kiểu hình mang tính trạng trội (gồm $AA$ và $Aa$) là $\\frac{3}{4} = 75\\%$; kiểu hình lặn ($aa$) là $\\frac{1}{4} = 25\\%$: Tỉ lệ kiểu hình $3 : 1$.
- Thực nghiệm mô phỏng gieo hạt đậu hoặc bốc thăm thẻ gene để kiểm chứng quy luật số lớn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Chủ động liên hệ kiến thức môn Sinh học lớp 9 với mô hình xác suất toán học.
- Giao tiếp và hợp tác: Làm việc nhóm bốc thăm mô phỏng 100 lần kết hợp giao tử và ghi chép số liệu.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Sử dụng bảng Punnett hai chiều và sơ đồ hình cây để mô hình hóa quá trình thụ tinh ngẫu nhiên.
- Năng lực giải quyết vấn đề toán học: Giải thích vì sao khi số lượng cá thể con lai càng lớn thì tỉ lệ thực nghiệm càng tiệm cận sát tỉ lệ lí thuyết $3 : 1$.

## 3. Về phẩm chất
- Khơi gợi niềm say mê nghiên cứu khoa học liên môn Toán học - Sinh học - Di truyền học.
- Tinh thần khách quan, trung thực với kết quả thực nghiệm bốc thăm ngẫu nhiên.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, 2 hộp bốc thăm chứa các quả bóng/thẻ gene $A$ và $a$, bảng Punnett chiếu trên màn hình.
2. Học sinh: SGK, vở ghi, mỗi nhóm chuẩn bị 2 túi giấy đựng các mảnh giấy ghi chữ cái $A$ và $a$, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ ĐẶT VẤN ĐỀ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tái hiện định luật phân li kinh điển của Men-đen về hoa đỏ và hoa trắng ở cây đậu Hà Lan.
b) Nội dung: Khi lai hai cây đậu Hà Lan hoa đỏ dị hợp $Aa \\times Aa$, Men-đen thu được ở thế hệ $F_2$ tỉ lệ xấp xỉ 3 hoa đỏ : 1 hoa trắng. Vì sao lại có tỉ lệ kì diệu đó?
c) Sản phẩm: HS nhận thức được đây là kết quả của sự kết hợp ngẫu nhiên các giao tử trong thụ tinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nhắc lại định luật Men-đen $F_2$ có tỉ lệ 3 trội : 1 lặn. Toán học giải thích điều này như thế nào?<br>- **HS:** Lắng nghe và suy ngẫm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhớ lại cơ thể $Aa$ tạo ra 2 loại giao tử với tỉ lệ ngang nhau: $\\frac{1}{2} A$ và $\\frac{1}{2} a$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Sự thụ tinh là sự kết hợp ngẫu nhiên giữa giao tử đực và giao tử cái.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đó chính là một phép thử ngẫu nhiên hai giai đoạn độc lập trong toán học! | Dẫn nhập vào mô hình xác suất của phép lai di truyền Men-đen. |

## B. MÔ HÌNH HÓA TOÁN HỌC VÀ THỰC HÀNH MÔ PHỎNG (HOẠT ĐỘNG 2) (30 phút)
### Hoạt động 2.1: Mô hình toán học bảng Punnett (15 phút)
a) Mục tiêu: Thiết lập không gian mẫu $\\Omega$ và tính xác suất lí thuyết của các kiểu gene, kiểu hình.
b) Nội dung: Bảng Punnett $2 \\times 2$ biểu diễn sự kết hợp giao tử đực ($A, a$) và giao tử cái ($A, a$).
c) Sản phẩm: Bảng Punnett hoàn chỉnh và các công thức xác suất trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Kẻ bảng Punnett hai chiều:<br>Hàng ngang: Giao tử cái $A, a$. Hàng dọc: Giao tử đực $A, a$.<br>Mỗi ô là một kết hợp tổ hợp gene.<br>- **HS:** Điền vào bảng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Không gian mẫu có 4 kết quả đồng khả năng: $\\Omega = \\{AA; Aa; aA; aa\\}$, $n(\\Omega) = 4$.<br>Xác suất kiểu gene:<br>- $P(AA) = \\frac{1}{4} = 25\\%$.<br>- $P(Aa) = \\frac{2}{4} = 50\\%$ (gồm $Aa$ và $aA$).<br>- $P(aa) = \\frac{1}{4} = 25\\%$.<br>Tỉ lệ kiểu gene: $1 AA : 2 Aa : 1 aa$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Do $A$ là gene trội hoàn toàn nên cả $AA$ và $Aa$ đều cho kiểu hình trội (hoa đỏ).<br>Xác suất kiểu hình trội là: $\\frac{1}{4} + \\frac{2}{4} = \\frac{3}{4} = 75\\%$.<br>Xác suất kiểu hình lặn ($aa$) là: $\\frac{1}{4} = 25\\%$.<br>Tỉ lệ kiểu hình là: $3\\text{ trội} : 1\\text{ lặn}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định: Toán học xác suất giải thích hoàn hảo quy luật di truyền sinh học! | **Bảng Punnett và Xác suất lí thuyết:**<br>| Giao tử | $A$ ($0{,}5$) | $a$ ($0{,}5$) |<br>| :--- | :---: | :---: |<br>| $A$ ($0{,}5$) | $AA$ ($0{,}25$) | $Aa$ ($0{,}25$) |<br>| $a$ ($0{,}5$) | $aA$ ($0{,}25$) | $aa$ ($0{,}25$) |<br>- Tỉ lệ kiểu gene: $1 AA : 2 Aa : 1 aa$.<br>- Tỉ lệ kiểu hình: $3\\text{ trội} : 1\\text{ lặn}$ ($75\\% : 25\\%$). |

### Hoạt động 2.2: Thực hành bốc thăm ngẫu nhiên mô phỏng (15 phút)
a) Mục tiêu: Thực hiện thí nghiệm bốc thăm ngẫu nhiên 50 lần để kiểm chứng xác suất thực nghiệm tiệm cận xác suất lí thuyết.
b) Nội dung: Mỗi nhóm có 2 túi (Túi 1: giao tử bố; Túi 2: giao tử mẹ). Rút ngẫu nhiên từ mỗi túi 1 thẻ, ghi lại kiểu gene nhận được, sau đó bỏ thẻ lại vào túi. Lặp lại 50 lần.
c) Sản phẩm: Bảng ghi kết quả thực nghiệm 50 lần bốc thăm của từng nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến quy trình bốc thăm 50 lần có hoàn lại. Thư ký nhóm kẻ sẵn bảng đếm kiểm kê.<br>- **HS:** Tiến hành bốc thăm nhanh chóng, trung thực.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Rút thẻ, ghi chép: ví dụ ra 12 lần $AA$, 26 lần $Aa$, 12 lần $aa$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các nhóm tính tỉ lệ phần trăm kiểu hình trội của nhóm mình: ví dụ $(12 + 26) / 50 = 38 / 50 = 76\\% \\approx 75\\%$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng hợp số liệu của cả 4 nhóm trong lớp ($50 \\times 4 = 200$ lần rút). Khi số lần tăng lên 200, tỉ lệ càng sát $75\\%$. | Thực hành bốc thăm mô phỏng 50 lần kiểm chứng quy luật số lớn trong xác suất di truyền. |

## C. TỔNG HỢP KẾT QUẢ VÀ BÁO CÁO (HOẠT ĐỘNG 3) (7 phút)
a) Mục tiêu: Tổng hợp số liệu toàn lớp lên bảng và so sánh với thí nghiệm thực tế của Men-đen trên 7324 cây đậu.
b) Nội dung: GV công bố số liệu gốc của Men-đen: 5474 cây hoa đỏ và 1850 cây hoa trắng (tỉ lệ $2{,}96 : 1 \\approx 3 : 1$).
c) Sản phẩm: HS cảm nhận được sức mạnh của toán học thống kê và xác suất trong khoa học tự nhiên.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu bảng số liệu thực nghiệm gốc của Men-đen.<br>- **HS:** So sánh kết quả thí nghiệm lớp học với số liệu của Men-đen.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét sự hội tụ kì diệu của xác suất thực nghiệm về xác suất lí thuyết khi số mẫu lớn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu cảm nghĩ về mối liên hệ Toán học - Sinh học.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương tinh thần làm việc khoa học của cả lớp. | So sánh số liệu lớp học với thí nghiệm lịch sử của Gregor Mendel. |

## D. TỔNG KẾT VÀ DẶN DÒ (HOẠT ĐỘNG 4) (3 phút)
a) Mục tiêu: Đánh giá tiết học trải nghiệm liên môn và tổng kết phần Đại số - Thống kê - Xác suất Toán 9.
b) Nội dung: Dặn dò chuẩn bị sang các tuần học tiếp theo về phần Hình học.
c) Sản phẩm: Kế hoạch học tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đánh giá tiết học sinh động, ý nghĩa. Kết thúc toàn bộ chương trình Đại số, Thống kê và Xác suất HK2.<br>- **HS:** Lắng nghe và tiếp thu.<br><br>**+ Bước 2: Dặn dò**<br>- **GV:** Chuẩn bị đầy đủ compa, thước đo góc cho phần Hình học Chương IX: Đường tròn tiếp theo.<br><br>**+ Bước 3: Kết thúc tiết học**<br>- Cả lớp chào giáo viên. | Tổng kết chuyên đề liên môn Toán - Sinh và dặn dò phần Hình học tiếp theo. |
"""
    },
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print(f"Hoàn tất tạo đợt 3 (9 bài Chương VIII & Ôn tập cuối HK2 & HĐTN Tiết 69 - 80) Toán 9 HK2!")
