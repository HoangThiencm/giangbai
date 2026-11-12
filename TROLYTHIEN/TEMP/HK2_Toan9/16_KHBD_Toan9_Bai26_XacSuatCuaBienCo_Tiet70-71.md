**TIẾT 70, 71 - BÀI 26: XÁC SUẤT CỦA BIẾN CỐ LIÊN QUAN TỚI PHÉP THỬ**
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm biến cố liên quan tới một phép thử ngẫu nhiên: Một biến cố $A$ là một tập con của không gian mẫu $\Omega$ ($A \subseteq \Omega$).
- Nhận biết kết quả thuận lợi cho biến cố $A$: Những kết quả thuộc $\Omega$ làm cho biến cố $A$ xảy ra, số lượng là $n(A)$.
- Nắm vững định nghĩa cổ điển về xác suất của biến cố trong mô hình đồng khả năng:
  $$P(A) = \frac{n(A)}{n(\Omega)}$$
- Nắm vững các tính chất cơ bản của xác suất: $0 \le P(A) \le 1$; xác suất của biến cố chắc chắn bằng $1$ ($P(\Omega) = 1$); xác suất của biến cố không thể bằng $0$ ($P(\emptyset) = 0$); xác suất của biến cố đối: $P(\overline{A}) = 1 - P(A)$.

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
a) Mục tiêu: Nắm vững khái niệm biến cố là tập con của $\Omega$, tập các kết quả thuận lợi và số phần tử $n(A)$.
b) Nội dung: Xác định tập hợp $A$ và số phần tử $n(A)$.
c) Sản phẩm: Vở ghi bài định nghĩa biến cố và kết quả thuận lợi.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Biến cố $A$ liên quan đến phép thử là một tập con của không gian mẫu $\Omega$. Các phần tử của $A$ gọi là các kết quả thuận lợi cho $A$. Kí hiệu số kết quả thuận lợi là $n(A)$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Gieo xúc xắc 1 lần. Gọi $A$ là biến cố: "Mặt xuất hiện có số chấm là số nguyên tố". Liệt kê các phần tử của $A$ và tính $n(A)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Các số nguyên tố trong $\{1; 2; 3; 4; 5; 6\}$ là $2, 3, 5$. Do đó $A = \{2; 3; 5\}$, $n(A) = 3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách trình bày biến cố dưới dạng tập hợp. | **1. Biến cố và Kết quả thuận lợi:**<br>- Biến cố $A$ là tập con của $\Omega$: $A \subseteq \Omega$.<br>- Mỗi phần tử của $A$ là một kết quả thuận lợi cho $A$.<br>- Số kết quả thuận lợi cho $A$ kí hiệu là $n(A)$.<br>- Ví dụ: $A = \{2; 3; 5\} \Rightarrow n(A) = 3$. |

### Hoạt động 2.2: Công thức tính xác suất của biến cố (35 phút)
a) Mục tiêu: Nắm vững công thức $P(A) = \frac{n(A)}{n(\Omega)}$ và các tính chất của xác suất.
b) Nội dung: Phát biểu công thức cổ điển trong mô hình đồng khả năng và biến cố đối.
c) Sản phẩm: Vở ghi công thức và lời giải ví dụ mẫu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu công thức: Giả sử các kết quả có thể của phép thử là đồng khả năng. Xác suất của biến cố $A$ là:<br>$$P(A) = \frac{n(A)}{n(\Omega)}$$<br>Nêu các tính chất: $0 \le P(A) \le 1$; $P(\Omega) = 1$; $P(\emptyset) = 0$.<br>Biến cố đối $\overline{A}$: Biến cố "Không xảy ra $A$", có $P(\overline{A}) = 1 - P(A)$.<br>- **HS:** Ghi chép công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính xác suất biến cố $A$ ở trên.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $P(A) = \frac{n(A)}{n(\Omega)} = \frac{3}{6} = \frac{1}{2} = 0{,}5$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Xác suất luôn là một số từ $0$ đến $1$, có thể viết dưới dạng phân số tối giản, số thập phân hoặc phần trăm ($50\%$). | **2. Định nghĩa cổ điển về xác suất:**<br>Giả sử các kết quả của phép thử là đồng khả năng. Khi đó:<br>$$P(A) = \frac{n(A)}{n(\Omega)}$$<br>**Tính chất:**<br>- $0 \le P(A) \le 1$.<br>- $P(\Omega) = 1$ (chắc chắn), $P(\emptyset) = 0$ (không thể).<br>- Biến cố đối: $P(\overline{A}) = 1 - P(A)$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vận dụng công thức xác suất giải bài toán rút thẻ số ngẫu nhiên.
b) Nội dung: Một hộp đựng 20 tấm thẻ được đánh số từ $1$ đến $20$. Rút ngẫu nhiên một thẻ. Tính xác suất của các biến cố:
1) $A$: "Số ghi trên thẻ là số chia hết cho 5".
2) $B$: "Số ghi trên thẻ là số chính phương".
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao đề bài toán rút thẻ từ 1 đến 20.<br>- **HS:** Xác định $n(\Omega) = 20$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** 1) Các số chia hết cho 5: $\{5; 10; 15; 20\} \Rightarrow n(A) = 4 \Rightarrow P(A) = \frac{4}{20} = \frac{1}{5}$.<br>2) Các số chính phương: $\{1; 4; 9; 16\} \Rightarrow n(B) = 4 \Rightarrow P(B) = \frac{4}{20} = \frac{1}{5}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài giải chuẩn mực. | **Bài giải:**<br>Không gian mẫu là tập hợp 20 thẻ: $n(\Omega) = 20$.<br>1) Các kết quả thuận lợi cho $A$ là: $5, 10, 15, 20$. Suy ra $n(A) = 4$.<br>Xác suất của biến cố $A$ là:<br>$$P(A) = \frac{n(A)}{n(\Omega)} = \frac{4}{20} = \frac{1}{5} = 0{,}2$$<br><br>2) Các kết quả thuận lợi cho $B$ là: $1, 4, 9, 16$. Suy ra $n(B) = 4$.<br>Xác suất của biến cố $B$ là:<br>$$P(B) = \frac{n(B)}{n(\Omega)} = \frac{4}{20} = \frac{1}{5} = 0{,}2$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng biến cố đối tính xác suất biến cố "có ít nhất một số chẵn" khi gieo 2 xúc xắc.
b) Nội dung: Biến cố đối của "có ít nhất một số chẵn" là "cả hai số đều lẻ".
c) Sản phẩm: Lời giải $P = 1 - \frac{9}{36} = \frac{27}{36} = \frac{3}{4}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn dùng biến cố đối khi gặp cụm từ "ít nhất một".<br>- **HS:** Tính số kết quả cả 2 cùng lẻ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $3 \times 3 = 9$ kết quả. Xác suất cả 2 lẻ là $\frac{9}{36} = \frac{1}{4}$. Suy ra ít nhất một chẵn là $1 - \frac{1}{4} = \frac{3}{4}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị tiết Luyện tập chung. | Ứng dụng biến cố đối: $P(A) = 1 - P(\overline{A})$. |