# -*- coding: utf-8 -*-
"""
Script sinh 9 KHBD Chương VIII: Mở đầu về tính xác suất của biến cố & Ôn tập cuối HK2 (Tiết 71 - 83) - Toán 8 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan8"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    {
        "filename": "19_KHBD_Toan8_Bai30_KetQuaCoTheVaKetQuaThuanLoi_Tiet71-72.md",
        "header": "TIẾT 71, 72 - BÀI 30: KẾT QUẢ CÓ THỂ VÀ KẾT QUẢ THUẬN LỢI\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 71, 72 - BÀI 30: KẾT QUẢ CÓ THỂ VÀ KẾT QUẢ THUẬN LỢI
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết không gian các kết quả có thể của một hành động, thực nghiệm ngẫu nhiên (chọn ngẫu nhiên một vật từ tập hợp hữu hạn).
- Phân biệt biến cố chắc chắn, biến cố không thể và biến cố ngẫu nhiên.
- Biết cách liệt kê tập hợp các kết quả thuận lợi cho một biến cố ngẫu nhiên cho trước.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự liệt kê có hệ thống tất cả các phần tử của không gian mẫu mà không bị sót hoặc trùng lặp.
- Giao tiếp và hợp tác: Làm việc nhóm kiểm tra và phân tích tính đồng khả năng của các kết quả trong phép thử.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận chứng minh một kết quả là thuận lợi hay không thuận lợi cho biến cố.
- Năng lực giải quyết vấn đề toán học: Phân tích bài toán rút thăm trúng thưởng, bốc thăm phân bảng thi đấu thể thao.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng bảng tính Excel dùng hàm RANDBETWEEN để mô phỏng tập hợp các kết quả có thể của phép thử ngẫu nhiên.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu cách AI mô hình hóa không gian trạng thái (State Space) trong lý thuyết trò chơi và cờ vua tự động.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng trong liệt kê và ghi chép số liệu.
- Ý thức học tập tự giác, đam mê khám phá các hiện tượng ngẫu nhiên trong đời sống.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, hộp đựng thẻ số, xúc xắc, máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt tình huống bốc thăm chia bảng giải bóng đá World Cup để dẫn vào khái niệm kết quả có thể và kết quả thuận lợi.
b) Nội dung: Một bảng đấu có 4 đội bóng, bốc ngẫu nhiên 1 lá thăm. Có bao nhiêu kết quả có thể? Lá thăm nào là kết quả thuận lợi cho đội tuyển Việt Nam?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khi bốc thăm ngẫu nhiên 1 lá phiếu từ hộp chứa tên 4 đội bóng A, B, C, D. Có bao nhiêu kết quả có thể xảy ra? Nếu ta mong muốn đội A được chọn thì có bao nhiêu kết quả thuận lợi?<br>- **HS:** Đọc đề và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Có 4 kết quả có thể. Có 1 kết quả thuận lợi là bốc trúng lá phiếu ghi tên đội A.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Khái niệm kết quả có thể và kết quả thuận lợi. | Có 4 kết quả có thể; có 1 kết quả thuận lợi cho biến cố bốc được đội A. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Kết quả có thể của hành động, thực nghiệm (35 phút)
a) Mục tiêu: Nắm vững tập hợp tất cả các kết quả có thể của một phép thử và tính đồng khả năng.
b) Nội dung: Gieo một con xúc xắc 6 mặt cân đối; Rút một chiếc thẻ từ hộp có 10 thẻ đánh số từ 1 đến 10.
c) Sản phẩm: Vở ghi và danh sách liệt kê kết quả của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu khái niệm: Trong một trò chơi hay phép thử ngẫu nhiên, tập hợp tất cả các kết quả có thể xảy ra được gọi là không gian kết quả có thể. Các kết quả gọi là đồng khả năng nếu chúng có cơ hội xuất hiện ngang nhau.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Liệt kê các kết quả có thể khi rút ngẫu nhiên 1 chiếc thẻ từ hộp đựng 10 thẻ đánh số từ $1$ đến $10$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Có 10 kết quả có thể: Rút được thẻ số $1, 2, 3, 4, 5, 6, 7, 8, 9, 10$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: 10 kết quả này là đồng khả năng xuất hiện vì các thẻ có kích thước và trọng lượng như nhau. | **1. Kết quả có thể:**<br>- Tập hợp tất cả các kết quả có thể xảy ra của một phép thử ngẫu nhiên.<br>- Tính đồng khả năng: Khi các kết quả có cơ hội xảy ra như nhau. |

### Hoạt động 2.2: Kết quả thuận lợi cho một biến cố (30 phút)
a) Mục tiêu: Nắm vững định nghĩa kết quả thuận lợi: Là kết quả làm cho biến cố xảy ra.
b) Nội dung: Đếm số kết quả thuận lợi cho biến cố $E$: "Rút được thẻ ghi số chia hết cho 3".
c) Sản phẩm: Lời giải bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Một kết quả làm cho biến cố xảy ra được gọi là kết quả thuận lợi cho biến cố đó. Trong 10 thẻ số từ 1 đến 10, hãy tìm các kết quả thuận lợi cho biến cố $E$: "Rút được thẻ ghi số chia hết cho 3".<br>- **HS:** Đọc đề và lọc các số.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Các số chia hết cho 3 là: $3, 6, 9$. Có 3 kết quả thuận lợi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo: Có 3 kết quả thuận lợi là thẻ số 3, thẻ số 6 và thẻ số 9.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại phương pháp đếm số kết quả thuận lợi. | **2. Kết quả thuận lợi cho một biến cố:**<br>- Kết quả làm cho biến cố xảy ra gọi là kết quả thuận lợi cho biến cố đó.<br>- Ví dụ: Với biến cố $E$ "Số trên thẻ chia hết cho 3", có 3 kết quả thuận lợi là: Thẻ 3, thẻ 6, thẻ 9. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Liệt kê các kết quả thuận lợi khi gieo một con xúc xắc 6 mặt.
b) Nội dung: Bài 8.1, 8.2 SGK trang 61.
c) Sản phẩm: Bài giải trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gieo một con xúc xắc 6 mặt một lần. Tìm số kết quả thuận lợi cho các biến cố:<br>  a) $A$: "Mặt xuất hiện có số chấm là số nguyên tố";<br>  b) $B$: "Mặt xuất hiện có số chấm lớn hơn 4".<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** a) Các số nguyên tố từ 1 đến 6 là: 2, 3, 5 $\\Rightarrow$ có 3 kết quả thuận lợi. b) Các số lớn hơn 4 là: 5, 6 $\\Rightarrow$ có 2 kết quả thuận lợi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá bài làm chuẩn xác, rõ ràng. | **Lời giải:**<br>a) Các kết quả thuận lợi cho biến cố $A$ là: Mặt 2 chấm, mặt 3 chấm, mặt 5 chấm. Có $3$ kết quả thuận lợi.<br>b) Các kết quả thuận lợi cho biến cố $B$ là: Mặt 5 chấm, mặt 6 chấm. Có $2$ kết quả thuận lợi. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng kết quả thuận lợi vào bài toán chọn ban cán sự lớp ngẫu nhiên.
b) Nội dung: Tổ 1 có 4 bạn nam và 6 bạn nữ. Chọn ngẫu nhiên 1 bạn làm tổ trưởng. Có bao nhiêu kết quả thuận lợi cho biến cố chọn được bạn nữ?
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán chọn tổ trưởng ngẫu nhiên. Tìm số kết quả có thể và số kết quả thuận lợi chọn được bạn nữ.<br>- **HS:** Suy nghĩ và tính nhẩm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Có 10 kết quả có thể ($4 + 6 = 10$). Có 6 kết quả thuận lợi chọn được bạn nữ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò xem trước Bài 31: Cách tính xác suất của biến cố bằng tỉ số. | Có $10$ kết quả có thể và có $6$ kết quả thuận lợi cho biến cố chọn được bạn nữ. |
"""
    },
    {
        "filename": "20_KHBD_Toan8_Bai31_CachTinhXacSuatBangTiSo_Tiet73.md",
        "header": "TIẾT 73 - BÀI 31: CÁCH TÍNH XÁC SUẤT CỦA BIẾN CỐ BẰNG TỈ SỐ\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 73 - BÀI 31: CÁCH TÍNH XÁC SUẤT CỦA BIẾN CỐ BẰNG TỈ SỐ
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững công thức tính xác suất cổ điển của biến cố trong mô hình đồng khả năng:
$$P(A) = \\frac{k}{n} = \\frac{\\text{Số kết quả thuận lợi cho } A}{\\text{Tổng số kết quả có thể}}$$
- Nhận biết các tính chất cơ bản của xác suất: $0 \\le P(A) \\le 1$; Xác suất của biến cố chắc chắn bằng $1$; Xác suất của biến cố không thể bằng $0$.
- Vận dụng tính xác suất của các biến cố trong trò chơi tung đồng xu, gieo xúc xắc, rút thẻ, bốc thăm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đếm chính xác số kết quả thuận lợi $k$ và tổng số kết quả $n$ để thiết lập tỉ số xác suất.
- Giao tiếp và hợp tác: Làm việc nhóm giải các bài toán tính xác suất biến cố có nhiều điều kiện ràng buộc.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh xác suất của hai biến cố để đánh giá biến cố nào có cơ hội xảy ra lớn hơn.
- Năng lực mô hình hoá toán học: Tính toán xác suất trúng thưởng trong các chương trình bốc thăm may mắn thực tế.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng máy tính cầm tay thực hiện rút gọn tỉ số xác suất về phân số tối giản và chuyển sang số thập phân.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu ứng dụng của định lý Bayes và xác suất có điều kiện trong các mô hình AI dự báo thời tiết và chẩn đoán y tế.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng trong từng phép đếm.
- Ý thức sống khoa học, không tin vào bói toán may rủi mù quáng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, bảng phụ công thức xác suất, máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kết nối từ bài trước để đưa ra công thức định lượng xác suất bằng tỉ số.
b) Nội dung: Gieo xúc xắc có 6 kết quả đồng khả năng, biến cố ra mặt chẵn có 3 kết quả thuận lợi. Cơ hội ra mặt chẵn là bao nhiêu phần?
c) Sản phẩm: Tỉ số $\\frac{3}{6} = \\frac{1}{2}$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khi gieo xúc xắc có 6 mặt, có 3 mặt chẵn (2, 4, 6). Cơ hội xuất hiện mặt chẵn chiếm bao nhiêu phần trong tổng số cơ hội?<br>- **HS:** Đọc câu hỏi và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tỉ số là $\\frac{3}{6} = \\frac{1}{2} = 50\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Tỉ số $\\frac{k}{n}$ này chính là công thức tính xác suất của biến cố. | Tỉ số $\\frac{3}{6} = \\frac{1}{2}$ chính là xác suất của biến cố xuất hiện mặt chẵn. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Công thức tính xác suất của biến cố bằng tỉ số (20 phút)
a) Mục tiêu: Nắm vững định nghĩa và công thức tính xác suất cổ điển $P(A) = \\frac{k}{n}$.
b) Nội dung: Công thức $P(A) = \\frac{k}{n}$, các tính chất của xác suất.
c) Sản phẩm: Vở ghi bài và công thức của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu công thức: Giả sử một phép thử có $n$ kết quả có thể và đồng khả năng xảy ra. Nếu biến cố $A$ có $k$ kết quả thuận lợi thì xác suất của biến cố $A$ là:<br>$$P(A) = \\frac{k}{n}$$<br>Nêu các tính chất: $0 \\le P(A) \\le 1$; Biến cố chắc chắn có xác suất bằng $1$; Biến cố không thể có xác suất bằng $0$.<br>- **HS:** Tiếp nhận công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính xác suất xuất hiện mặt $5$ chấm khi gieo xúc xắc một lần.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Có 1 kết quả thuận lợi trên tổng số 6 kết quả $\\Rightarrow P = \\frac{1}{6}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Phải luôn kiểm tra điều kiện đồng khả năng trước khi áp dụng công thức tỉ số. | **Công thức tính xác suất của biến cố:**<br>- Nếu các kết quả của phép thử là đồng khả năng, xác suất của biến cố $A$ là:<br>$$P(A) = \\frac{k}{n} = \\frac{\\text{Số kết quả thuận lợi cho } A}{\\text{Tổng số kết quả có thể}}$$<br>- Tính chất: $0 \\le P(A) \\le 1$.<br>  + Biến cố chắc chắn: $P = 1$.<br>  + Biến cố không thể: $P = 0$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Tính xác suất trong bài toán rút thẻ ngẫu nhiên từ hộp.
b) Nội dung: Bài 8.4, 8.5 SGK trang 64: Một hộp có 20 chiếc thẻ đánh số từ 1 đến 20. Rút ngẫu nhiên 1 chiếc thẻ. Tính xác suất của biến cố: "Số trên thẻ là bội của 5".
c) Sản phẩm: Bài giải chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Tìm số kết quả có thể $n$ và số kết quả thuận lợi $k$ cho biến cố rút được thẻ là bội của 5.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tổng số kết quả $n = 20$. Các bội của 5 từ 1 đến 20 là: $5, 10, 15, 20$ $\\Rightarrow k = 4$. Xác suất: $P = \\frac{4}{20} = \\frac{1}{5} = 0{,}2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi kết quả chính xác, rút gọn phân số tối giản chuẩn mực. | **Bài giải:**<br>- Tổng số kết quả có thể là: $n = 20$.<br>- Các kết quả thuận lợi cho biến cố "Số trên thẻ là bội của 5" là: Thẻ 5, 10, 15, 20. Có $k = 4$ kết quả thuận lợi.<br>- Xác suất của biến cố là:<br>$$P = \\frac{4}{20} = \\frac{1}{5} = 0{,}2$$<br>Vậy xác suất cần tìm là $\\frac{1}{5}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng xác suất vào trò chơi quay bánh xe trúng thưởng tại siêu thị.
b) Nội dung: Bánh xe chia 12 phần bằng nhau gồm: 1 ô Trúng Tivi, 2 ô Trúng Nồi cơm, 3 ô Trúng Mũ bảo hiểm, 6 ô Chúc may mắn lần sau. Tính xác suất để khách hàng quay được quà.
c) Sản phẩm: Xác suất $P = \\frac{6}{12} = \\frac{1}{2}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán vòng quay siêu thị có 12 ô. Tính xác suất để quay được một phần quà bất kì (Tivi, Nồi cơm hoặc Mũ).<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Số ô có quà là $1 + 2 + 3 = 6$ ô. Xác suất: $P = \\frac{6}{12} = \\frac{1}{2} = 50\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học thực tế. Dặn dò xem trước Bài 32. | Xác suất để khách hàng quay được phần quà là:<br>$$P = \\frac{1 + 2 + 3}{12} = \\frac{6}{12} = \\frac{1}{2} = 50\\%$$ |
"""
    },
    {
        "filename": "21_KHBD_Toan8_Bai32_MoiLienHeXacSuatThucNghiem_Tiet74-75.md",
        "header": "TIẾT 74, 75 - BÀI 32: MỐI LIÊN HỆ GIỮA XÁC SUẤT THỰC NGHIỆM VỚI XÁC SUẤT VÀ ỨNG DỤNG\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 74, 75 - BÀI 32: MỐI LIÊN HỆ GIỮA XÁC SUẤT THỰC NGHIỆM VỚI XÁC SUẤT VÀ ỨNG DỤNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết mối liên hệ mật thiết giữa xác suất thực nghiệm của một biến cố với xác suất lý thuyết của nó: Khi số lần thực hiện phép thử càng lớn thì xác suất thực nghiệm của biến cố càng tiến gần đến xác suất lý thuyết (Định luật số lớn).
- Sử dụng xác suất lý thuyết để ước lượng xác suất thực nghiệm và ngược lại, dùng xác suất thực nghiệm để ước tính xác suất của các hiện tượng tự nhiên phức tạp.
- Vận dụng vào các bài toán ước lượng cá thể trong tự nhiên (phương pháp bắt - thả đánh dấu mẫu).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tìm hiểu các thí nghiệm lịch sử tung đồng xu hàng chục nghìn lần của Buffon và Pearson.
- Giao tiếp và hợp tác: Làm việc nhóm tổng hợp số liệu thực nghiệm gieo xúc xắc của cả lớp để quan sát tính ổn định của tần số.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích nguyên lý số lớn và ý nghĩa của việc tăng kích thước mẫu thực nghiệm.
- Năng lực giải quyết vấn đề toán học: Ước lượng số lượng cá trong một hồ nước bằng công thức tỉ lệ xác suất thực nghiệm.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng phần mềm Excel tạo bảng mô phỏng 1000 lần gieo xúc xắc và vẽ biểu đồ đường biểu diễn sự hội tụ của xác suất thực nghiệm về giá trị lý thuyết 1/6.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu phương pháp Monte Carlo trong AI sử dụng hàng triệu phép thử ngẫu nhiên mô phỏng để tính toán xấp xỉ các bài toán không có lời giải giải tích.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, trung thực, tôn trọng số liệu khoa học khách quan.
- Tinh thần trách nhiệm và ý thức bảo vệ môi trường tự nhiên (thông qua bài toán ước lượng đa dạng sinh học).

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, bảng dữ liệu lịch sử của Buffon và Pearson, máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Giới thiệu thí nghiệm lịch sử tung đồng xu của các nhà toán học vĩ đại để tạo cảm hứng khám phá.
b) Nội dung: Nhà toán học Buffon tung đồng xu $4040$ lần có $2048$ lần ngửa (tỉ lệ $0{,}5069$). Pearson tung $24000$ lần có $12012$ lần ngửa (tỉ lệ $0{,}5005$). Em có nhận xét gì về các tỉ số này so với số $\\frac{1}{2}$?
c) Sản phẩm: Nhận xét của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu bảng số liệu lịch sử tung đồng xu của Buffon và Pearson. Hỏi: Khi số lần tung tăng từ $4040$ lên $24000$ thì tỉ số xuất hiện mặt ngửa càng tiến gần đến số nào?<br>- **HS:** Quan sát bảng số liệu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thấy số liệu càng ngày càng sát với $0{,}5 = \\frac{1}{2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Đây chính là mối liên hệ kỳ diệu giữa xác suất thực nghiệm và xác suất lý thuyết. | Khi số lần thử càng lớn thì xác suất thực nghiệm càng tiến gần đến xác suất lý thuyết $\\frac{1}{2}$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Mối liên hệ giữa xác suất thực nghiệm và xác suất (35 phút)
a) Mục tiêu: Nắm vững định lý số lớn: Khi $n$ rất lớn thì xác suất thực nghiệm xấp xỉ bằng xác suất lý thuyết.
b) Nội dung: Quy luật số lớn và ứng dụng ước lượng số lần xuất hiện của biến cố trong tương lai.
c) Sản phẩm: Vở ghi bài và lời giải ví dụ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lý: Khi số lần thực hiện thí nghiệm càng lớn thì xác suất thực nghiệm của một biến cố càng tiến gần đến xác suất của biến cố đó. Vì vậy, ta có thể dùng xác suất lý thuyết $P(A)$ để ước lượng số lần xảy ra của $A$ trong $N$ lần thử: $\\text{Số lần dự đoán} \\approx N \\cdot P(A)$.<br>- **HS:** Ghi nhận công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Gieo một con xúc xắc cân đối $600$ lần. Ước lượng số lần xuất hiện mặt $6$ chấm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác suất lý thuyết mặt 6 chấm là $\\frac{1}{6}$. Số lần xuất hiện ước lượng là: $600 \\cdot \\frac{1}{6} = 100$ lần.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Trong thực tế số lần có thể dao động quanh $100$ lần. | **1. Mối liên hệ:**<br>- Khi số lần thử $n$ rất lớn, xác suất thực nghiệm $\\approx$ xác suất lý thuyết.<br>- Ước lượng số lần xuất hiện của biến cố $A$ trong $N$ phép thử:<br>$$\\text{Số lần xuất hiện} \\approx N \\cdot P(A)$$ |

### Hoạt động 2.2: Ứng dụng trong thực tiễn - Phương pháp đánh dấu mẫu (30 phút)
a) Mục tiêu: Hiểu phương pháp bắt - đánh dấu - thả để ước lượng kích thước quần thể sinh vật trong tự nhiên.
b) Nội dung: Bài toán ước lượng số lượng cá trong hồ.
c) Sản phẩm: Lời giải bài toán ước lượng cá thể trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Để ước lượng số cá trong hồ, người ta bắt $50$ con cá, đánh dấu rồi thả lại hồ. Hôm sau bắt ngẫu nhiên $100$ con cá thì thấy có $5$ con có dấu. Hãy ước lượng tổng số cá trong hồ.<br>- **HS:** Đọc đề và phân tích tỉ lệ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tỉ lệ cá có dấu trong mẫu bắt lại là: $\\frac{5}{100} = \\frac{1}{20}$. Tỉ lệ này xấp xỉ tỉ lệ cá có dấu trên toàn bộ hồ: $\\frac{50}{N} \\approx \\frac{1}{20} \\Rightarrow N \\approx 50 \\cdot 20 = 1000$ con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và giới thiệu: Đây là phương pháp "Capture-Recapture" được các nhà sinh học môi trường toàn cầu sử dụng. | **2. Phương pháp bắt - đánh dấu - thả lại:**<br>- Bắt $M$ cá thể đánh dấu, thả lại quần thể kích thước $N$.<br>- Bắt lại mẫu $n$ cá thể thấy có $m$ cá thể có dấu.<br>- Ta có tỉ lệ:<br>$$\\frac{m}{n} \\approx \\frac{M}{N} \\Rightarrow N \\approx \\frac{M \\cdot n}{m}$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Ước lượng số sản phẩm hỏng của nhà máy khi biết xác suất thực nghiệm kiểm tra mẫu.
b) Nội dung: Bài 8.8 SGK trang 68.
c) Sản phẩm: Lời giải chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Kiểm tra ngẫu nhiên $200$ linh kiện điện tử thấy có $3$ linh kiện bị lỗi. Hãy ước lượng số linh kiện bị lỗi trong lô hàng gồm $10\\,000$ linh kiện.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác suất thực nghiệm linh kiện lỗi là $\\frac{3}{200}$. Số linh kiện lỗi ước lượng trong $10\\,000$ chiếc là: $10\\,000 \\cdot \\frac{3}{200} = 150$ linh kiện.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kết quả chính xác, chuẩn mực. | Ước lượng số linh kiện bị lỗi trong lô $10\\,000$ linh kiện là:<br>$$10\\,000 \\cdot \\frac{3}{200} = 150\\text{ (linh kiện)}$$<br>Đáp số: Khoảng $150$ linh kiện lỗi. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng phương pháp mô phỏng Monte Carlo để tính diện tích hình phẳng có biên bất kì.
b) Nội dung: Giới thiệu ứng dụng gieo hạt ngẫu nhiên để đo diện tích lá cây.
c) Sản phẩm: Báo cáo ngắn của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt chiếc lá lên tờ giấy hình vuông cạnh $10\\text{ cm}$ (diện tích $100\\text{ cm}^2$). Gieo ngẫu nhiên $500$ hạt vừng thấy có $180$ hạt rơi trúng chiếc lá. Ước tính diện tích chiếc lá.<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Diện tích lá: $S \\approx 100 \\cdot \\frac{180}{500} = 36\\text{ cm}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị cho tiết Luyện tập chung. | Diện tích chiếc lá ước tính là:<br>$$S \\approx 100 \\cdot \\frac{180}{500} = 36\\text{ (cm}^2\\text{)}$$ |
"""
    },
    {
        "filename": "22_KHBD_Toan8_LuyenTapChung_Tiet76.md",
        "header": "TIẾT 76 - LUYỆN TẬP CHUNG: XÁC SUẤT CỦA BIẾN CỐ (TRANG 68)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 76 - LUYỆN TẬP CHUNG: XÁC SUẤT CỦA BIẾN CỐ (TRANG 68)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Rèn luyện kỹ năng phân tích và tính xác suất của biến cố trong các mô hình đồng khả năng bằng công thức tỉ số: $P(A) = \\frac{k}{n}$.
- Vận dụng linh hoạt mối liên hệ giữa xác suất thực nghiệm và xác suất lý thuyết để giải quyết các bài toán dự đoán, kiểm định chất lượng sản phẩm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức Chương VIII qua sơ đồ tư duy; chủ động rà soát các lỗi sai hay gặp khi đếm kết quả thuận lợi.
- Giao tiếp và hợp tác: Tương tác nhóm giải bài toán xác suất thực tế nhiều bước tính toán.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh xác suất các biến cố, đánh giá mức độ rủi ro trong đầu tư hoặc sản xuất.
- Năng lực giải quyết vấn đề toán học: Sử dụng công thức tỉ số giải bài toán rút thăm và bốc thăm thi đấu.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng máy tính cầm tay để tính toán nhanh các tỉ số xác suất và phân tích dữ liệu bảng kiểm tra mẫu.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D1.1: HS tìm hiểu vai trò cốt lõi của lý thuyết xác suất trong việc huấn luyện các mô hình học sâu (Deep Learning) và nhận diện giọng nói.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật và tác phong khoa học.
- Ý thức học tập tự giác, sẵn sàng tâm thế bước vào kỳ thi cuối năm học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 76 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tái hiện nhanh công thức tính xác suất cổ điển $P(A) = \\frac{k}{n}$ qua câu hỏi kiểm tra nhanh.
b) Nội dung: Nêu ý nghĩa của $k$ và $n$ trong công thức xác suất.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Viết công thức tính xác suất của biến cố $A$ trong mô hình đồng khả năng và giải thích các đại lượng.<br>- **HS:** Viết nhanh lên bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $P(A) = \\frac{k}{n}$ ($k$: số kết quả thuận lợi, $n$: tổng số kết quả có thể).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn dắt vào bài luyện tập chung. | $P(A) = \\frac{k}{n}$ với $k$ là số kết quả thuận lợi và $n$ là tổng số kết quả có thể. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức xác suất biến cố thông qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 76; đối chiếu các khái niệm và công thức.

![Sơ đồ tư duy Luyện tập chung Tiết 76](khbd-ill:mindmap-toan8-tiet76)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 76. Yêu cầu HS phân tích các nhánh: 1. Biến cố & Kết quả (chắc chắn, không thể, ngẫu nhiên); 2. Công thức xác suất $P = k/n$; 3. Xác suất thực nghiệm & Định luật số lớn; 4. Ứng dụng thực tiễn.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoạt động nhóm đôi tóm tắt công thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ kiến thức chuẩn mực. | **Hệ thống kiến thức trọng tâm:**<br>1. Không gian kết quả có thể ($n$) và kết quả thuận lợi ($k$).<br>2. Công thức: $P(A) = \\frac{k}{n}$.<br>3. Mối liên hệ: Xác suất thực nghiệm xấp xỉ xác suất lý thuyết khi số lần thử rất lớn.<br>4. Ước lượng tương lai: $\\text{Số lần} \\approx N \\cdot P(A)$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tính xác suất biến cố trong trò chơi chọn ngẫu nhiên hai chữ số.
b) Nội dung: Bài 8.9, 8.10 SGK trang 69.
c) Sản phẩm: Bài giải chi tiết trên bảng và trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Một hộp chứa 30 tấm thẻ cùng loại được đánh số từ 1 đến 30. Rút ngẫu nhiên một tấm thẻ. Tính xác suất của các biến cố:<br>  a) $E$: "Số ghi trên thẻ là số chính phương";<br>  b) $F$: "Số ghi trên thẻ chia hết cho cả 2 và 3".<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tổng số kết quả $n = 30$.<br>  a) Các số chính phương từ 1 đến 30 là: $1, 4, 9, 16, 25 \\Rightarrow k_1 = 5 \\Rightarrow P(E) = \\frac{5}{30} = \\frac{1}{6}$.<br>  b) Số chia hết cho cả 2 và 3 là bội của 6: $6, 12, 18, 24, 30 \\Rightarrow k_2 = 5 \\Rightarrow P(F) = \\frac{5}{30} = \\frac{1}{6}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi kết quả tính toán chính xác, tối giản phân số chuẩn mực. | **Lời giải:**<br>Tổng số kết quả có thể là $n = 30$.<br>a) Các kết quả thuận lợi cho $E$ là: $1, 4, 9, 16, 25$. Có $k = 5$ kết quả.<br>$$P(E) = \\frac{5}{30} = \\frac{1}{6}$$<br>b) Các số chia hết cho cả 2 và 3 là các bội của 6: $6, 12, 18, 24, 30$. Có $k = 5$ kết quả.<br>$$P(F) = \\frac{5}{30} = \\frac{1}{6}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng xác suất vào phân tích độ an toàn khi mua bảo hiểm tai nạn học sinh.
b) Nội dung: Giáo viên phân tích cách các công ty bảo hiểm sử dụng xác suất thống kê để định phí bảo hiểm hàng năm.
c) Sản phẩm: Hiểu biết thực tế của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vì sao phí bảo hiểm y tế hoặc bảo hiểm tai nạn học sinh lại có giá rất rẻ (chỉ vài trăm nghìn đồng một năm) trong khi mức chi trả bồi thường có thể lên tới hàng chục triệu đồng?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vì xác suất rủi ro xảy ra tai nạn trong một năm là rất nhỏ, dựa trên quy luật số lớn chia sẻ rủi ro giữa hàng triệu học sinh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học thực tế sâu sắc. Dặn dò chuẩn bị cho Bài tập cuối chương VIII. | Phí bảo hiểm được tính toán dựa trên xác suất rủi ro cực nhỏ kết hợp với quy luật số lớn của hàng triệu người tham gia. |
"""
    },
    {
        "filename": "23_KHBD_Toan8_BaiTapCuoiChuong8_Tiet77.md",
        "header": "TIẾT 77 - BÀI TẬP CUỐI CHƯƠNG VIII: MỞ ĐẦU VỀ TÍNH XÁC SUẤT CỦA BIẾN CỐ (TRANG 70)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 77 - BÀI TẬP CUỐI CHƯƠNG VIII: MỞ ĐẦU VỀ TÍNH XÁC SUẤT CỦA BIẾN CỐ (TRANG 70)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết toàn bộ kiến thức Chương VIII: Kết quả có thể và kết quả thuận lợi, cách tính xác suất của biến cố bằng tỉ số trong mô hình đồng khả năng, mối liên hệ giữa xác suất thực nghiệm và xác suất lý thuyết, ứng dụng phương pháp bắt - đánh dấu - thả lại.
- Vận dụng kiến thức toàn chương để giải quyết các bài tập tổng hợp và bài toán xác suất thực tiễn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức toàn chương qua sơ đồ tư duy; chủ động rà soát và đánh giá các kỹ năng tính xác suất của bản thân.
- Giao tiếp và hợp tác: Tự tin thuyết trình giải thích các bước tính xác suất trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa quy tắc, lựa chọn công thức giải toán chính xác và ngắn gọn nhất.
- Năng lực giải quyết vấn đề toán học: Xử lý các bài toán phối hợp phép đếm tổ hợp đơn giản và xác suất.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng máy tính cầm tay để kiểm tra kết quả tính toán của toàn bộ đề bài tập ôn tập cuối chương VIII.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D1.1: HS tìm hiểu ứng dụng của xác suất trong các mô hình xử lý ngôn ngữ tự nhiên lớn (LLMs) để dự đoán từ tiếp theo xuất hiện.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật và tác phong khoa học.
- Tự tin, sẵn sàng tâm thế bước vào các tiết Ôn tập học kì II.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 77 (vector 300 DPI), máy chiếu, phiếu ôn tập chương.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập nhanh các công thức trọng tâm qua trò chơi trắc nghiệm "Vượt chướng ngại vật".
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm kiểm tra lý thuyết chương VIII.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu hỏi trắc nghiệm lý thuyết xác suất.<br>- **HS:** Chuẩn bị bảng con ghi đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ đáp án sau hiệu lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giải thích ngắn gọn lý do chọn đáp án.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và dẫn vào bài ôn tập tổng kết chương VIII. | Bảng đáp án trắc nghiệm chuẩn xác của học sinh. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ cấu trúc kiến thức Chương VIII bằng Sơ đồ tư duy tổng hợp 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 77; hoàn thiện bức tranh tổng thể về xác suất biến cố.

![Sơ đồ tư duy Bài tập cuối chương VIII Tiết 77](khbd-ill:mindmap-toan8-tiet77)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy tổng thể Chương VIII. Hướng dẫn HS hệ thống theo 4 nhánh lớn: 1. Mô hình xác suất; 2. Tính xác suất bằng tỉ số $P = k/n$; 3. Mối liên hệ thực nghiệm & Định luật số lớn; 4. Tư duy xác suất & Ứng dụng.<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành các chỗ trống trong phiếu tóm tắt.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS lên bảng điền các công thức trọng tâm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại toàn bộ hệ thống lý thuyết chương VIII chuẩn mực. | **Tổng kết lý thuyết Chương VIII:**<br>- Mô hình đồng khả năng: Tập hợp $n$ kết quả có thể có cơ hội như nhau.<br>- Công thức: $P(A) = \\frac{k}{n}$ ($k$ là số kết quả thuận lợi).<br>- Thực nghiệm: Xác suất thực nghiệm hội tụ về xác suất lý thuyết khi $n \\to \\infty$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tự luận tổng hợp: Tính xác suất rút thẻ và ước lượng cá thể trong tự nhiên.
b) Nội dung: Bài 8.11, 8.12 SGK trang 70.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài tập:<br>  Bài 1: Một túi đựng 5 viên bi đỏ, 3 viên bi xanh và 2 viên bi vàng. Lấy ngẫu nhiên 1 viên bi. Tính xác suất lấy được viên bi không phải màu đỏ.<br>  Bài 2: Một kiểm lâm viên bắt và bấm thẻ tai 60 cá thể hươu sao rồi thả vào rừng. Lần thứ hai bắt 80 cá thể hươu sao thấy có 12 cá thể có thẻ tai. Ước lượng số lượng hươu sao trong khu rừng đó.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bài 1: Tổng số bi $n = 5 + 3 + 2 = 10$. Số bi không phải đỏ là bi xanh hoặc vàng: $3 + 2 = 5$ viên $\\Rightarrow P = \\frac{5}{10} = \\frac{1}{2}$. Bài 2: Tỉ lệ có thẻ tai: $\\frac{12}{80} = \\frac{3}{20}$. Số lượng hươu sao ước lượng: $N \\approx \\frac{60 \\cdot 80}{12} = 400$ con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá bài làm xuất sắc, phương pháp tính logic và chặt chẽ. | **Lời giải:**<br>**Bài 1:**<br>Tổng số viên bi trong túi là $n = 5 + 3 + 2 = 10$.<br>Số viên bi không phải màu đỏ là $3 + 2 = 5$ (viên).<br>Xác suất lấy được viên bi không phải màu đỏ là:<br>$$P = \\frac{5}{10} = \\frac{1}{2} = 50\\%$$<br>**Bài 2:**<br>Số lượng hươu sao ước lượng trong khu rừng là:<br>$$N \\approx \\frac{60 \\cdot 80}{12} = 400\\text{ (con)}$$<br>Đáp số: Khoảng $400$ con hươu sao. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Định hướng chuẩn bị cho Tiết 78: Hoạt động thực hành trải nghiệm mô tả thí nghiệm ngẫu nhiên với phần mềm Excel.
b) Nội dung: Giáo viên phân công chuẩn bị phòng máy tính và hướng dẫn hàm RANDBETWEEN trong Excel.
c) Sản phẩm: Kế hoạch làm bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến nội dung tiết thực hành tin học - toán học tiếp theo: Dùng Microsoft Excel mô phỏng 1000 lần gieo xúc xắc.<br>- **HS:** Ghi chép yêu cầu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ôn lại cách mở bảng tính Excel.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác nhận sẵn sàng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi kết quả học tập xuất sắc của cả lớp trong Chương VIII. | Chuẩn bị đầy đủ phòng máy và tâm thế cho tiết trải nghiệm Excel ở tiết sau. |
"""
    },
    {
        "filename": "24_KHBD_Toan8_HDTN_Excel_Tiet78.md",
        "header": "TIẾT 78 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: MÔ TẢ THÍ NGHIỆM NGẪU NHIÊN VỚI PHẦN MỀM EXCEL\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 78 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: MÔ TẢ THÍ NGHIỆM NGẪU NHIÊN VỚI PHẦN MỀM EXCEL
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng hàm sinh số ngẫu nhiên `=RANDBETWEEN(bottom, top)` trong phần mềm Microsoft Excel để mô phỏng tự động hàng trăm, hàng nghìn lần phép thử gieo xúc xắc hoặc tung đồng xu.
- Sử dụng hàm đếm có điều kiện `=COUNTIF(range, criteria)` để thống kê tần số xuất hiện của từng mặt xúc xắc.
- Tính xác suất thực nghiệm tự động và vẽ biểu đồ hình cột so sánh tần số xuất hiện của các mặt.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự nhập các công thức hàm vào bảng tính Excel và sao chép công thức nhanh chóng bằng thao tác kéo chuột (Fill Handle).
- Giao tiếp và hợp tác: Làm việc nhóm hỗ trợ nhau xử lý lỗi công thức và tùy biến biểu đồ cột đẹp mắt.

b) Năng lực đặc thù môn Toán:
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng công nghệ thông tin và bảng tính điện tử để giải quyết bài toán mô phỏng toán học thực nghiệm.
- Năng lực tư duy và lập luận toán học: Nhận xét sự san bằng tần số của 6 mặt xúc xắc khi số lần mô phỏng tăng từ 100 lên 1000 lần.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng các hàm số RANDBETWEEN và COUNTIF trong Excel để xử lý dữ liệu thực nghiệm; 1.3.TC2a: HS lưu trữ và quản lý bảng tính khoa học.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu cách các nhà khoa học máy tính sử dụng các bộ tạo số giả ngẫu nhiên (Pseudo-random Number Generator) để huấn luyện AI.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, tác phong làm việc khoa học, ngăn nắp.
- Tinh thần hứng thú, say mê ứng dụng tin học vào giải quyết các bài toán toán học hiện đại.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn Microsoft Excel, máy chiếu, bài giảng hướng dẫn trực quan.
2. Học sinh: Máy vi tính phòng máy, sổ tay tin học, tài liệu SGK Toán 8 Tập 2 trang 71, 72.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề nếu muốn gieo xúc xắc $1000$ lần bằng tay sẽ mất rất nhiều thời gian, từ đó thấy được sức mạnh của phần mềm máy tính.
b) Nội dung: Gieo $1000$ lần xúc xắc bằng tay mất khoảng 1 tiếng, máy tính làm trong 1 giây.
c) Sản phẩm: Sự hào hứng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nếu thầy yêu cầu cả lớp gieo con xúc xắc 1000 lần và đếm số lần ra mặt 6 chấm thì mất bao lâu? Có công cụ nào làm việc đó trong chớp mắt không?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bằng tay rất lâu và mỏi. Dùng máy tính sẽ làm rất nhanh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài thực hành: Microsoft Excel sẽ giúp chúng ta mô phỏng 1000 lần gieo xúc xắc trong 1 giây. | Phần mềm bảng tính Excel là công cụ mạnh mẽ mô phỏng các thí nghiệm ngẫu nhiên quy mô lớn. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (20 phút)
### Hoạt động 2.1: Các hàm ngẫu nhiên và đếm điều kiện trong Excel (10 phút)
a) Mục tiêu: Nắm vững cú pháp hàm `=RANDBETWEEN(1, 6)` và `=COUNTIF(vùng, điều kiện)`.
b) Nội dung: Cú pháp và ý nghĩa của hai hàm Excel quan trọng.
c) Sản phẩm: Vở ghi bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cú pháp:<br>  + `=RANDBETWEEN(1, 6)`: Sinh ngẫu nhiên một số nguyên từ 1 đến 6 (mô phỏng 1 lần gieo xúc xắc).<br>  + `=COUNTIF(A1:A1000, 1)`: Đếm số lần xuất hiện số 1 trong vùng dữ liệu từ ô A1 đến A1000.<br>- **HS:** Ghi chép cú pháp hàm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khởi động Excel trên máy tính cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhập thử nghiệm hàm tại ô đầu tiên.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở lưu ý: Dấu ngăn cách trong hàm có thể là dấu phẩy `,` hoặc dấu chấm phẩy `;` tùy cài đặt máy tính. | **Cú pháp hàm Excel:**<br>- Sinh số ngẫu nhiên: `=RANDBETWEEN(1, 6)`.<br>- Đếm số lần: `=COUNTIF(A1:A1000, 6)`. |

### Hoạt động 2.2: Quy trình 3 bước thực hiện trên bảng tính (10 phút)
a) Mục tiêu: Nắm vững quy trình: 1. Tạo cột số ngẫu nhiên; 2. Lập bảng thống kê tần số; 3. Tính tỉ số xác suất thực nghiệm.
b) Nội dung: Các bước thao tác từ ô A1 kéo xuống A1000, lập bảng tại vùng C1:D7.
c) Sản phẩm: Bảng tính hoàn chỉnh trên màn hình máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn 3 bước:<br>  1. Tại ô A1 gõ `=RANDBETWEEN(1, 6)`, dùng chuột kéo chốt Fill Handle xuống đến ô A1000.<br>  2. Tại cột C ghi các mặt từ 1 đến 6. Tại cột D dùng hàm COUNTIF đếm số lần.<br>  3. Tại cột E tính xác suất thực nghiệm: `=D1/1000` và đổi sang định dạng $\\%$.<br>- **HS:** Thao tác tuần tự trên máy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhấn phím F9 để quan sát số liệu tự động nhảy ngẫu nhiên mỗi lần tính toán lại.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Thích thú khi thấy xác suất mỗi mặt luôn dao động quanh mức $16{,}7\\% = \\frac{1}{6}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Đây chính là bằng chứng thực nghiệm của định luật số lớn. | Học sinh thao tác kéo sao chép công thức 1000 dòng thành thạo, bảng số liệu tự động cập nhật khi nhấn F9. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vẽ biểu đồ cột trực quan biểu diễn số lần xuất hiện của 6 mặt xúc xắc trong Excel.
b) Nội dung: Chọn vùng dữ liệu C1:D7 $\\rightarrow$ Insert $\\rightarrow$ Column Chart.
c) Sản phẩm: Biểu đồ cột rực rỡ trên màn hình của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn vẽ biểu đồ: Bôi đen bảng tần số $\\rightarrow$ Vào Menu Insert $\\rightarrow$ Chọn Column Chart $\\rightarrow$ Chọn kiểu cột 2D Clustered Column. Đổi tiêu đề biểu đồ thành: "KẾT QUẢ 1000 LẦN GIEO XÚC XẮC".<br>- **HS:** Thực hiện vẽ biểu đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tùy biến màu sắc các cột biểu đồ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Chiếu các biểu đồ đẹp của học sinh lên màn hình lớn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét độ cao của 6 cột xấp xỉ ngang nhau, khẳng định tính đồng khả năng tuyệt đối của 6 mặt. | Biểu đồ cột hoàn thiện chuẩn xác, thể hiện độ cao các cột xấp xỉ bằng nhau quanh mức 160 - 170 lần. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Lưu và nộp tệp bài làm thực hành Excel.
b) Nội dung: Lưu tệp `Toan8_NhomX_MoPhongExcel.xlsx` vào thư mục chung của lớp.
c) Sản phẩm: Tệp bảng tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS lưu tệp bài làm và nộp lên mạng nội bộ.<br>- **HS:** Thao tác File $\\rightarrow$ Save As.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tắt máy vi tính, sắp xếp bàn ghế gọn gàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp kiểm tra phòng máy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương tinh thần học tập nghiêm túc, dặn dò chuẩn bị cho đợt Ôn tập học kì II ở các tiết sau. | 100% học sinh hoàn thành bài thực hành và nộp tệp Excel thành công. |
"""
    },
    {
        "filename": "25_KHBD_Toan8_OnTapCuoiHK2_DaiSoXacSuat_Tiet79-81.md",
        "header": "TIẾT 79, 80, 81 - ÔN TẬP ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)\n*Thời lượng thực hiện: 03 tiết (135 phút)*",
        "md": """TIẾT 79, 80, 81 - ÔN TẬP ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Đại số và Xác suất trong cả Học kì II:
  + Chương VI: Phân thức đại số (ĐKXĐ, tính chất, 4 phép tính, rút gọn biểu thức hữu tỉ).
  + Chương VII: Phương trình bậc nhất một ẩn (giải phương trình, giải bài toán bằng cách lập PT, hàm số bậc nhất và đồ thị, hệ số góc, vị trí tương đối hai đường thẳng).
  + Chương VIII: Mở đầu về tính xác suất của biến cố (kết quả có thể, kết quả thuận lợi, công thức tỉ số $P = k/n$, mối liên hệ thực nghiệm).
- Vận dụng kiến thức tổng hợp giải quyết các bài toán liên môn và thực tế đời sống.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự lập kế hoạch ôn tập chi tiết 3 tiết; tự giải các đề ôn tập tổng hợp và tự đánh giá năng lực của mình.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải toán, tranh biện tìm ra lời giải ngắn gọn nhất trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa các công thức toán học; phân tích logic nhiều tầng để giải các bài toán thực tế phức tạp.
- Năng lực mô hình hoá toán học: Chuyển đổi các bài toán kinh tế, chuyển động, năng suất thành phương trình hoặc hàm số chuẩn xác.

c) Năng lực số (NLS):
- ***5.2.TC2b: Sử dụng máy tính cầm tay thành thạo mọi chức năng tính toán để kiểm tra kết quả bài làm; 1.3.TC2a: Sắp xếp các dạng bài tập vào bảng tính cá nhân để quản lý tiến độ ôn thi.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D2.1: HS sử dụng AI để tạo đề thi thử trắc nghiệm trực tuyến cuối học kì II và nhận phản hồi giải thích chi tiết cho từng câu sai.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, kỷ luật, trung thực và tác phong làm bài thi nghiêm túc.
- Tự tin, sẵn sàng tâm thế bước vào kỳ thi đánh giá cuối năm học với kết quả cao nhất.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Ôn tập cuối HK2 Tiết 79-81 (vector 300 DPI), bộ đề ôn tập tổng hợp.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay, đề cương ôn tập cuối HKII.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Quán triệt kế hoạch ôn tập tổng thể 3 tiết Đại số & Xác suất cuối năm.
b) Nội dung: Phổ biến ma trận đề thi cuối kì II và các chuyên đề trọng tâm cần giải quyết.
c) Sản phẩm: Kế hoạch ôn tập của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến cấu trúc đề thi cuối kì II phần Đại số - Xác suất (chiếm 70% tổng điểm đề thi). Kế hoạch ôn tập 3 tiết chia theo 3 chuyên đề.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt mục tiêu điểm số cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp phát biểu quyết tâm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Động viên tinh thần học tập của cả lớp. | Kế hoạch ôn tập 3 tiết rõ ràng, bám sát ma trận và cấu trúc đề thi chuẩn Bộ GD&ĐT. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (30 phút)
### Hoạt động 2.1: Hệ thống hoá toàn diện kiến thức HKII qua Sơ đồ tư duy (30 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ cấu trúc kiến thức Đại số và Xác suất qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 79-81; phân tích sự gắn kết liên hoàn giữa Phân thức, Phương trình, Hàm số và Xác suất.

![Sơ đồ tư duy Ôn tập cuối HK2 Tiết 79-81](khbd-ill:mindmap-toan8-tiet79-81)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở ghi học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy tổng hợp HKII. Hướng dẫn ôn theo 4 trục kiến thức lớn:<br>  1. Phân thức đại số: ĐKXĐ, rút gọn, 4 phép tính, giá trị nguyên.<br>  2. Phương trình bậc nhất & Giải bài toán bằng lập PT: Chuyển động, năng suất.<br>  3. Hàm số bậc nhất: $y = ax + b$, đồ thị, hệ số góc, vị trí tương đối.<br>  4. Xác suất biến cố: Mô hình đồng khả năng, công thức $P = k/n$, thực nghiệm.<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành sơ đồ tư duy vào vở ôn tập theo các nhóm chuyên đề.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện các nhóm lần lượt thuyết trình tóm tắt các trục kiến thức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa: Khắc sâu lưu ý không kết luận tập nghiệm $S = \\{...\\}$, không dùng dấu tương đương tùy tiện. | **Tổng kết lý thuyết Đại số và Xác suất HKII:**<br>- Phân thức: Rút gọn, quy đồng MTC, 4 phép tính.<br>- Phương trình: $ax + b = 0$ ($a \\neq 0$), nghiệm $x = -b/a$; 3 bước giải bài toán lập PT.<br>- Hàm số: $y = ax + b$, đồ thị qua $(0; b)$ và $(-b/a; 0)$; Song song $a=a', b \\neq b'$.<br>- Xác suất: $P(A) = \\frac{k}{n}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (90 phút)
a) Mục tiêu: Luyện tập toàn diện 4 dạng bài tập cốt lõi của đề thi: Rút gọn phân thức, Giải phương trình và bài toán lập PT, Bài toán hàm số đồ thị và Bài toán xác suất.
b) Nội dung: Giải các đề ôn tập số 1 và số 2 trong tập tài liệu đề cương.
c) Sản phẩm: Bài làm chi tiết của học sinh trên bảng và trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 4 bài tập điển hình qua các tiết ôn tập:<br>  Bài 1: Cho biểu thức $P = \\left(\\frac{x}{x^2 - 4} + \\frac{1}{x + 2} - \\frac{2}{x - 2}\\right) : \\left(1 - \\frac{x}{x + 2}\\right)$.<br>    a) Tìm điều kiện xác định và rút gọn biểu thức $P$;<br>    b) Tìm các giá trị nguyên của $x$ để biểu thức $P$ nhận giá trị nguyên.<br>  Bài 2: Giải bài toán bằng cách lập phương trình: Một xe máy khởi hành từ A đến B với vận tốc $40\\text{ km/h}$. Sau đó 1 giờ, một ô tô cũng xuất phát từ A đuổi theo xe máy với vận tốc $60\\text{ km/h}$. Hỏi sau bao lâu kể từ khi ô tô xuất phát thì ô tô đuổi kịp xe máy?<br>  Bài 3: Cho hai hàm số bậc nhất $y = 2x - 3$ ($d_1$) và $y = -x + 3$ ($d_2$).<br>    a) Vẽ đồ thị của hai hàm số trên cùng một mặt phẳng tọa độ $Oxy$;<br>    b) Tìm tọa độ giao điểm $M$ của hai đường thẳng $d_1$ và $d_2$.<br>  Bài 4: Một hộp có 50 chiếc thẻ đánh số từ 1 đến 50. Rút ngẫu nhiên một chiếc thẻ. Tính xác suất của biến cố: "Số trên thẻ là số có hai chữ số và có chữ số hàng đơn vị là 5".<br>- **HS:** Nhận đề và phân tích từng bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài nghiêm túc vào vở cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 4 HS lên bảng chữa chi tiết 4 bài tập.<br>- Bài 1: ĐKXĐ: $x \\neq \\pm 2$. Ngoặc 1: $\\frac{x + x - 2 - 2(x + 2)}{(x - 2)(x + 2)} = \\frac{-6}{x^2 - 4}$. Ngoặc 2: $\\frac{x + 2 - x}{x + 2} = \\frac{2}{x + 2}$. Biểu thức $P = \\frac{-6}{(x - 2)(x + 2)} \\cdot \\frac{x + 2}{2} = \\frac{-3}{x - 2}$. Để $P \\in \\mathbb{Z}$ thì $x - 2 \\in \\text{Ư}(-3) = \\{\\pm 1, \\pm 3\\} \\Rightarrow x \\in \\{3, 1, 5, -1\\}$ (đều thỏa mãn ĐK).<br>- Bài 2: Gọi thời gian ô tô đi đến khi đuổi kịp xe máy là $t$ ($t > 0$, giờ). Khi đó thời gian xe máy đi là $t + 1$. Quãng đường xe máy đi: $40(t + 1)$. Quãng đường ô tô đi: $60t$. Phương trình: $60t = 40(t + 1) \\Rightarrow 20t = 40 \\Rightarrow t = 2$ giờ (thỏa mãn ĐK). Vậy sau 2 giờ kể từ khi xuất phát thì ô tô đuổi kịp xe máy.<br>- Bài 3: Phương trình hoành độ giao điểm: $2x - 3 = -x + 3 \\Rightarrow 3x = 6 \\Rightarrow x = 2 \\Rightarrow y = 1 \\Rightarrow M(2; 1)$.<br>- Bài 4: Tổng số thẻ $n = 50$. Các số có 2 chữ số tận cùng bằng 5 là: $15, 25, 35, 45 \\Rightarrow k = 4$. Xác suất: $P = \\frac{4}{50} = \\frac{2}{25} = 0{,}08$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chuẩn hóa: Lời giải mẫu mực, kết luận rõ ràng, không dùng ký hiệu tập nghiệm. | **Đáp số bài tập ôn tập tổng hợp:**<br>**Bài 1:**<br>a) ĐKXĐ: $x \\neq \\pm 2$. Biểu thức rút gọn: $P = \\frac{-3}{x - 2}$.<br>b) $x \\in \\{3, 1, 5, -1\\}$.<br>**Bài 2:**<br>Thời gian ô tô đuổi kịp xe máy là $2$ giờ.<br>**Bài 3:**<br>Tọa độ giao điểm là điểm $M(2; 1)$.<br>**Bài 4:**<br>Xác suất cần tìm là $P = \\frac{4}{50} = \\frac{2}{25} = 8\\%$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Quán triệt quy chế thi và kỹ năng phân bổ thời gian 90 phút làm bài thi học kì II môn Toán.
b) Nội dung: Chiến thuật làm bài: Trắc nghiệm làm trong 20 phút, Tự luận 60 phút, soát lại bài 10 phút.
c) Sản phẩm: Bản ghi nhớ chiến thuật làm bài của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chiến thuật làm bài thi: Đọc kĩ đề, làm câu dễ trước, kiểm tra kỹ điều kiện xác định và kết luận nghiệm rõ ràng; kiểm tra lại bằng máy tính cầm tay.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự rà soát lại các dụng cụ học tập cần mang vào phòng thi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đặt các câu hỏi còn băn khoăn về nội dung ôn tập.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giải đáp thắc mắc, chúc cả lớp bình tĩnh, tự tin và đạt thành tích xuất sắc nhất trong kỳ thi cuối năm học. | 100% học sinh sẵn sàng với tâm thế tự tin nhất bước vào bài kiểm tra đánh giá cuối HKII. |
"""
    },
    {
        "filename": "26_KHBD_Toan8_KiemTraCuoiHK2_DaiSoXacSuat_Tiet82.md",
        "header": "TIẾT 82 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 82 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện chuẩn kiến thức, kỹ năng của học sinh về toàn bộ chương trình Đại số và Xác suất trong Học kì II môn Toán 8 (Chương VI, Chương VII, Chương VIII).
- Đánh giá năng lực giải quyết vấn đề toán học thực tiễn, năng lực mô hình hóa toán học và suy luận logic.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Độc lập làm bài, trung thực, nghiêm túc tuân thủ quy chế kiểm tra cuối năm học.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày bài giải mạch lạc, chặt chẽ, đầy đủ căn cứ toán học.
- Năng lực giải quyết vấn đề toán học: Mô hình hóa và giải quyết trọn vẹn các bài toán thực tế.

c) Năng lực số (NLS):
- ***5.2.TC2b: Sử dụng máy tính cầm tay đúng quy định trong phòng thi để kiểm tra các phép biến đổi đại số phức tạp.***

## 3. Về phẩm chất
- Trung thực, khách quan, tự trọng và có trách nhiệm cao với kết quả học tập của mình.
- Tác phong làm bài nghiêm túc, khoa học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận và bản đặc tả chuẩn Bộ GD&ĐT (Trắc nghiệm 30% - Tự luận 70%), đáp án và thang điểm chi tiết.
2. Học sinh: Giấy thi, bút mực, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (3 phút)
a) Mục tiêu: Ổn định phòng thi, tạo tâm lý tự tin và phát đề kiểm tra.
b) Nội dung: Nhắc nhở quy chế thi và phát đề.
c) Sản phẩm: Đề thi trên bàn của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định trật tự phòng thi, phổ biến quy chế. Phát đề thi cho học sinh.<br>- **HS:** Nhận đề, kiểm tra số trang và độ rõ của đề.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Điền đầy đủ thông tin cá nhân vào giấy thi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo ngay nếu có đề bị lỗi mờ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Phát lệnh bắt đầu tính giờ làm bài. | 100% học sinh sẵn sàng bước vào bài làm. |

## B. THỰC HIỆN BÀI KIỂM TRA (HOẠT ĐỘNG 2) (40 phút)
a) Mục tiêu: Học sinh độc lập làm bài thi trắc nghiệm và tự luận.
b) Nội dung: Học sinh giải các câu hỏi trong đề kiểm tra.
c) Sản phẩm: Bài làm hoàn thiện trên giấy thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giám sát phòng thi nghiêm túc, bao quát đảm bảo tính công bằng, khách quan.<br>- **HS:** Độc lập làm bài, không trao đổi, không quay cóp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm phần Trắc nghiệm trước, sau đó làm phần Tự luận trình bày chi tiết.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Báo mốc thời gian còn lại 15 phút và 5 phút.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **HS:** Soát lại toàn bộ bài làm, đặc biệt là các bước biến đổi dấu âm và kết luận nghiệm. | Học sinh làm bài độc lập, nghiêm túc, đạt chất lượng cao. |

## C. THU BÀI VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (2 phút)
a) Mục tiêu: Thu bài đầy đủ theo danh sách lớp và nhận xét ý thức kiểm tra.
b) Nội dung: Thu bài thi theo dãy bàn.
c) Sản phẩm: Toàn bộ bài thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hết giờ làm bài, yêu cầu học sinh dừng bút, nộp bài theo dãy.<br>- **HS:** Dừng bút và chuyển bài lên đầu bàn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm đủ số bài thi theo sĩ số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự lớp xác nhận sĩ số tham gia kiểm tra.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét thái độ làm bài của học sinh; dặn dò chuẩn bị cho Tiết 83: Trả bài kiểm tra. | Thu đủ 100% bài kiểm tra theo sĩ số lớp. |
"""
    },
    {
        "filename": "27_KHBD_Toan8_TraBaiKiemTraCuoiHK2_Tiet83.md",
        "header": "TIẾT 83 - TRẢ BÀI KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 83 - TRẢ BÀI KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (ĐẠI SỐ VÀ XÁC SUẤT)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết các lỗi sai phổ biến của học sinh trong bài kiểm tra cuối học kì II: Quên điều kiện xác định của phân thức, sai dấu khi chuyển vế, sai sót khi tính xác suất biến cố.
- Khắc sâu các phương pháp biến đổi đại số chuẩn mực và cách trình bày bài thi tự luận khoa học.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đối chiếu bài làm với đáp án chuẩn, phát hiện nguyên nhân dẫn đến mất điểm và tự sửa bài vào vở.
- Giao tiếp và hợp tác: Tự tin trao đổi với giáo viên và bạn bè về các thắc mắc trong cách chấm điểm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phân tích các bước lập luận còn thiếu căn cứ trong bài thi của mình.
- Năng lực giải quyết vấn đề toán học: Trình bày lại bài giải hoàn chỉnh cho các câu bị điểm trừ.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS xem điểm số và bảng phân tích phổ điểm bài kiểm tra của lớp được giáo viên công bố trên hệ thống quản lý học tập số (LMS).***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.A1.2: HS thảo luận về vai trò của con người trong việc thẩm định và phúc khảo bài thi so với các hệ thống chấm thi AI tự động.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, khiêm tốn khi đạt kết quả cao và không nản chí khi kết quả chưa như mong muốn.
- Tinh thần cầu tiến, có ý thức vươn lên chuẩn bị cho chương trình Toán 9.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Bài kiểm tra đã chấm của học sinh, bảng thống kê điểm số, đáp án và thang điểm chi tiết, máy chiếu.
2. Học sinh: Vở ghi bài, bút đỏ sửa bài.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhận xét chung về tình hình làm bài kiểm tra cuối học kì II của cả lớp.
b) Nội dung: Giáo viên công bố phổ điểm chung, biểu dương các bài làm xuất sắc và chỉ ra các lỗi sai phổ biến.
c) Sản phẩm: Tâm thế tích cực tiếp nhận phản hồi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Báo cáo tình hình làm bài: Đa số học sinh nắm vững kiến thức cơ bản, làm tốt phần trắc nghiệm và câu rút gọn. Một số bạn còn sai sót ở câu toán thực tế và tìm giá trị nguyên.<br>- **HS:** Lắng nghe nhận xét.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự liên hệ với bài làm của mình.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cán sự học tập báo cáo số bạn đạt điểm Giỏi.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào tiết chữa bài và trả bài kiểm tra. | Nhận thức rõ ưu điểm và các lỗi sai cần khắc phục trong bài kiểm tra. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Phân tích đáp án và chữa các câu sai phổ biến (15 phút)
a) Mục tiêu: Hiểu rõ từng bước giải chuẩn mực và biểu điểm chi tiết.
b) Nội dung: Trình chiếu đáp án chi tiết phần Tự luận (Câu rút gọn phân thức, Câu giải bài toán bằng lập PT, Câu xác suất).
c) Sản phẩm: Vở sửa bài bằng bút đỏ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu đáp án và biểu điểm chi tiết từng câu. Phân tích lỗi sai kinh điển: Quên đặt điều kiện xác định; Chuyển vế không đổi dấu; Quên đối chiếu điều kiện khi giải bài toán chuyển động.<br>- **HS:** Quan sát đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi chép các lưu ý quan trọng vào vở sửa bài.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày lại câu tìm giá trị nguyên chuẩn mực.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Từng bước biến đổi phải có căn cứ rõ ràng, không làm tắt. | Chữa chi tiết các câu tự luận trọng tâm, phân tích biểu điểm và lỗi sai thường gặp. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Trả bài kiểm tra đến từng học sinh, học sinh kiểm tra lại điểm số và tự chữa bài.
b) Nội dung: Trả bài kiểm tra, học sinh đối chiếu thang điểm và thảo luận thắc mắc.
c) Sản phẩm: Bài kiểm tra được đối soát cẩn thận của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trả bài kiểm tra đến từng học sinh. Yêu cầu kiểm tra lại tổng điểm, đối chiếu với đáp án.<br>- **HS:** Nhận bài và kiểm tra lại điểm số.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Dùng bút đỏ tự sửa lại các câu làm sai vào vở ghi bài.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu thắc mắc nếu có điểm chấm sót hoặc chưa rõ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giải đáp thỏa đáng mọi thắc mắc của học sinh, điều chỉnh điểm số nếu có sai sót kỹ thuật. | 100% học sinh kiểm tra lại bài thi, hiểu rõ lý do bị trừ điểm và tự sửa bài hoàn chỉnh. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tổng kết chương trình môn Toán 8 phần Đại số và định hướng chuẩn bị cho môn Toán 9.
b) Nội dung: Dặn dò kế hoạch tự học trong dịp hè môn Toán.
c) Sản phẩm: Tinh thần sẵn sàng bước vào lớp 9 của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tổng kết: Đại số 8 là nền tảng cốt lõi của môn Toán THCS. Lên lớp 9 các em sẽ học sâu về Căn bậc hai, Hệ phương trình và Phương trình bậc hai. Chúc các em có kỳ nghỉ hè vui tươi và bổ ích!<br>- **HS:** Lắng nghe và vỗ tay nhiệt liệt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi chép tài liệu đọc thêm dịp hè.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện lớp cảm ơn thầy cô giáo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em luôn giữ vững niềm đam mê toán học! | Hoàn thành xuất sắc toàn bộ chương trình Đại số và Xác suất môn Toán 8 năm học 2026 - 2027. |
"""
    }
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print("Hoàn tất tạo 9 KHBD Chương VIII: Mở đầu về tính xác suất của biến cố & Ôn tập cuối HK2 (Tiết 71 - 83)!")
