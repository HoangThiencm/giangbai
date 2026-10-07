# -*- coding: utf-8 -*-
import os

OUT_DIR = "tools/khbd_toan8_builder"
os.makedirs(OUT_DIR, exist_ok=True)

# ==============================================================================
# BÀI 01: BÀI 5. PHÉP CHIA ĐA THỨC CHO ĐƠN THỨC (TIẾT 9, 10 - TUẦN 5)
# ==============================================================================
bai_01_content = """Tiết 9, 10 - BÀI 5: PHÉP CHIA ĐA THỨC CHO ĐƠN THỨC
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và giải thích được điều kiện để đơn thức $A$ chia hết cho đơn thức $B$, đa thức $A$ chia hết cho đơn thức $B$ (trong trường hợp chia hết).
- Thực hiện thành thạo phép chia đơn thức cho đơn thức và phép chia đa thức cho đơn thức.
- Vận dụng được phép chia đa thức cho đơn thức để giải quyết một số bài toán thực tế và bài toán rút gọn biểu thức.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác tìm hiểu quy tắc chia thông qua các hoạt động khám phá và ví dụ mẫu trong SGK.
- Giao tiếp và hợp tác: Tương tác tích cực, thảo luận nhóm hiệu quả để so sánh số mũ của biến và tìm thương của phép chia.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh số mũ của từng biến để rút ra điều kiện chia hết.
- Năng lực giải quyết vấn đề toán học: Phân tích bài toán thực tế (tính chiều cao khối hộp chữ nhật) thành phép toán chia đa thức.

c) Năng lực số (NLS):
- **3.4.TC2a:** HS liệt kê các bước chỉ dẫn (thuật toán) thực hiện phép chia trên máy tính.
- **5.3.TC2b:** HS gắn kết cá nhân vào quá trình xử lý tư duy khi dùng phần mềm gỡ lỗi phép chia.
- **4.1.TC2a:** HS thiết lập cách bảo vệ các tệp bài tập đa thức đã lưu trên máy cá nhân.

## 3. Về phẩm chất
- Chăm chỉ, cẩn thận trong tính toán lũy thừa và dấu của hệ số.
- Có tinh thần trách nhiệm trong hợp tác nhóm và ý thức tự học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Kết nối tri thức, Kế hoạch bài dạy, thước kẻ, máy vi tính, máy chiếu/Tivi, phiếu học tập.
2. Học sinh: SGK, vở ghi, dụng cụ học tập (thước kẻ, bút màu), máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)
a) Mục tiêu: Gợi mở nhu cầu thực hiện phép chia đơn thức cho đơn thức thông qua bài toán thực tế tính kích thước khối hộp chữ nhật.
b) Nội dung: HS quan sát hình ảnh hai khối hộp chữ nhật, tiếp nhận bài toán mở đầu SGK trang 22.
![Mô hình hai khối hộp chữ nhật](khbd-ill:hinh_01_khoi_hop_chu_nhat)
c) Sản phẩm: Câu trả lời ban đầu của HS về công thức thể tích và nhận định cần thực hiện phép chia $6x^2y : 2xy$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh hai khối hộp chữ nhật và nêu bài toán mở đầu: Khối hộp thứ nhất có ba kích thước $x, 2x$ và $3y$. Khối hộp thứ hai có diện tích đáy là $2xy$. Biết hai khối hộp có cùng thể tích, hãy nêu cách tính chiều cao của khối hộp thứ hai.<br>- **HS:** Tiếp nhận nhiệm vụ, quan sát hình vẽ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại công thức tính thể tích hình hộp chữ nhật: $V = \text{chiều dài} \cdot \text{chiều rộng} \cdot \text{chiều cao} = \text{diện tích đáy} \cdot \text{chiều cao}$.<br>- **HS:** Tính thể tích khối hộp thứ nhất: $V = x \cdot 2x \cdot 3y = 6x^2y$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Để tìm chiều cao khối hộp thứ hai khi biết thể tích $V = 6x^2y$ và diện tích đáy $S = 2xy$, ta cần làm phép tính gì?<br>- **HS:** Ta cần lấy thể tích chia cho diện tích đáy: $6x^2y : 2xy$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Để thực hiện phép chia này cũng như chia một đa thức cho một đơn thức, chúng ta cùng tìm hiểu bài học hôm nay. | **Bài toán mở đầu (SGK trang 22):**<br>- Thể tích khối hộp thứ nhất:<br>$V = x \cdot 2x \cdot 3y = 6x^2y$.<br>- Vì hai khối hộp có cùng thể tích nên thể tích khối hộp thứ hai cũng là $6x^2y$.<br>- Diện tích đáy khối hộp thứ hai là $S = 2xy$.<br>- Chiều cao của khối hộp thứ hai là thương của phép chia:<br>$h = 6x^2y : 2xy$.<br><br>*(Phép chia này sẽ được giải quyết sau khi học quy tắc chia đơn thức cho đơn thức)*. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (47 phút)

### 1. Hoạt động 2.1: Chia đơn thức cho đơn thức (25 phút)
a) Mục tiêu: HS phát biểu được điều kiện để đơn thức $A$ chia hết cho đơn thức $B$ và nắm vững quy tắc chia đơn thức cho đơn thức; tích hợp chỉ báo NLS 3.4.TC2a và 5.3.TC2b.
b) Nội dung: HS thực hiện HĐ1, HĐ2, rút ra quy tắc, nghiên cứu Ví dụ 1, làm Luyện tập 1 và Vận dụng 1.
c) Sản phẩm: Lời giải HĐ1, HĐ2, quy tắc chia đơn thức, bài giải Ví dụ 1, Luyện tập 1, Vận dụng 1.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS nhớ lại quy tắc chia hai lũy thừa cùng cơ số ở lớp 7 để thực hiện HĐ1:<br>a) Tính $6x^3 : 3x^2$;<br>b) Với $a, b \in \mathbb{R}, b \ne 0; m, n \in \mathbb{N}$, khi nào $ax^m$ chia hết cho $bx^n$?<br>- **GV:** Yêu cầu HS thảo luận nhóm đôi làm HĐ2 (SGK trang 23).<br>- **HS:** Đọc yêu cầu, làm việc cá nhân rồi thảo luận cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành HĐ1: $6x^3 : 3x^2 = (6:3) \cdot x^{3-2} = 2x$. $ax^m$ chia hết cho $bx^n$ khi $m \ge n$.<br>- **HS:** HĐ2: Xét các trường hợp chia hết và không chia hết.<br>- ***(Tích hợp NLS 3.4.TC2a: GV hướng dẫn HS liệt kê các bước chỉ dẫn thuật toán chia hai đơn thức trên máy tính: Bước 1: Lấy hệ số chia hệ số; Bước 2: Với từng biến, lấy số mũ bị chia trừ số mũ chia; Bước 3: Nhân các kết quả lại với nhau).***<br>- ***(Tích hợp NLS 5.3.TC2b: HS gắn kết tư duy logic khi phát hiện điều kiện máy tính báo lỗi: nếu số mũ của biến trong đơn thức chia lớn hơn số mũ trong đơn thức bị chia ($n > m$) thì phần mềm sẽ báo lỗi không chia hết).***<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Gọi đại diện HS trình bày quy tắc và điều kiện chia hết.<br>- **HS:** Nêu kết luận trong khung màu cam SGK trang 23.<br>- **GV:** Cho HS làm Ví dụ 1 và Luyện tập 1 cá nhân.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy tắc chia đơn thức cho đơn thức. Chốt lại kết quả Luyện tập 1 và giải bài toán Vận dụng 1. | **1. CHIA ĐƠN THỨC CHO ĐƠN THỨC**<br><br>**HĐ1:**<br>a) $6x^3 : 3x^2 = 2x$.<br>b) $ax^m$ chia hết cho $bx^n$ khi $m \ge n$. Khi đó: $ax^m : bx^n = (a:b) \cdot x^{m-n}$.<br><br>**HĐ2:**<br>a) $A = 6x^3y$ chia hết cho $B = 3x^2y$. Thương là: $(6:3)(x^3:x^2)(y:y) = 2x$.<br>b) $A = x^2y$ không chia hết cho $B = xy^2$ vì số mũ của $y$ trong $B$ (là 2) lớn hơn số mũ của $y$ trong $A$ (là 1).<br><br>**Quy tắc (SGK trang 23):**<br>- Đơn thức $A$ chia hết cho đơn thức $B$ ($B \ne 0$) khi mỗi biến của $B$ đều là biến của $A$ với số mũ không lớn hơn số mũ của nó trong $A$.<br>- **Muốn chia đơn thức $A$ cho đơn thức $B$ (trường hợp chia hết):**<br>+ Chia hệ số của $A$ cho hệ số của $B$;<br>+ Chia luỹ thừa của từng biến trong $A$ cho luỹ thừa của cùng biến đó trong $B$;<br>+ Nhân các kết quả tìm được với nhau.<br><br>**Ví dụ 1 (SGK trang 23):**<br>Cho $A = 5x^2yz^3$.<br>a) $A$ không chia hết cho $B = x^2y^2z^2$ vì số mũ của $y$ trong $B$ (là 2) lớn hơn số mũ của $y$ trong $A$ (là 1).<br>b) $A$ chia hết cho $C = -2x^2z^2$. Thương là:<br>$A : C = 5x^2yz^3 : (-2x^2z^2) = -\frac{5}{2}yz$.<br><br>**Luyện tập 1:**<br>a) $-15x^2y^2 : 3x^2y = -5y$.<br>b) $6xy$ không chia hết cho $2yz$ vì biến $z$ có trong đơn thức chia nhưng không có trong đơn thức bị chia.<br>c) $4xy^3 : 6xy^2 = \frac{2}{3}y$.<br><br>**Vận dụng 1:**<br>Chiều cao khối hộp thứ hai là:<br>$h = 6x^2y : 2xy = 3x$. |

### 2. Hoạt động 2.2: Chia đa thức cho đơn thức (22 phút)
a) Mục tiêu: HS nắm được điều kiện đa thức chia hết cho đơn thức và thành thạo quy tắc chia đa thức cho đơn thức; tích hợp chỉ báo NLS 4.1.TC2a.
b) Nội dung: Nhận xét điều kiện chia hết, quy tắc chia đa thức cho đơn thức, nghiên cứu Ví dụ 2, làm Luyện tập 2 và Vận dụng 2.
c) Sản phẩm: Lời giải Ví dụ 2, Luyện tập 2, Vận dụng 2.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Một đa thức $A$ gồm nhiều hạng tử. Khi nào thì đa thức $A$ chia hết cho đơn thức $B$?<br>- **GV:** Để chia đa thức $A$ cho đơn thức $B$, ta làm như thế nào? Hãy liên hệ với quy tắc nhân đơn thức với đa thức.<br>- **HS:** Đọc SGK trang 24, suy nghĩ câu trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đa thức $A$ chia hết cho đơn thức $B$ nếu mọi hạng tử của $A$ đều chia hết cho $B$.<br>- **HS:** Muốn chia đa thức $A$ cho $B$, ta chia từng hạng tử của $A$ cho $B$ rồi cộng các kết quả lại.<br>- **GV:** Hướng dẫn HS phân tích Ví dụ 2 SGK.<br>- ***(Tích hợp NLS 4.1.TC2a: GV nhắc nhở HS khi làm bài tập trên máy tính hoặc phần mềm bảng tính, cần biết cách đặt tên tệp rõ ràng, lưu trữ có cấu trúc thư mục khoa học và thiết lập bảo vệ tệp bằng sao lưu định kỳ để không bị mất dữ liệu học tập).***<br>- **HS:** Thực hiện làm Luyện tập 2 và Vận dụng 2 vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Gọi 2 HS lên bảng làm Luyện tập 2 và Vận dụng 2.<br>- **HS:** Cả lớp theo dõi, nhận xét bài làm trên bảng.<br>- **GV:** Lưu ý dấu của từng hạng tử khi thực hiện phép chia.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định quy tắc chia đa thức cho đơn thức. Đánh giá kết quả làm bài của HS. | **2. CHIA ĐA THỨC CHO ĐƠN THỨC**<br><br>**Nhận xét:**<br>Đa thức $A$ chia hết cho đơn thức $B$ nếu mọi hạng tử của $A$ đều chia hết cho $B$.<br><br>**Quy tắc (SGK trang 24):**<br>Muốn chia đa thức $A$ cho đơn thức $B$, ta chia từng hạng tử của $A$ cho $B$ rồi cộng các kết quả với nhau.<br><br>**Ví dụ 2 (SGK trang 24):**<br>$(15x^2y^4 - 4x^3y^3 + 20x^2y) : 5x^2y$<br>$= (15x^2y^4 : 5x^2y) + (-4x^3y^3 : 5x^2y) + (20x^2y : 5x^2y)$<br>$= 3y^3 - \frac{4}{5}xy^2 + 4$.<br><br>**Luyện tập 2:**<br>$(6x^4y^3 - 8x^3y^4 + 3x^2y^2) : 2xy^2$<br>$= (6x^4y^3 : 2xy^2) - (8x^3y^4 : 2xy^2) + (3x^2y^2 : 2xy^2)$<br>$= 3x^3y - 4x^2y^2 + \frac{3}{2}x$.<br><br>**Vận dụng 2:**<br>Vì $A \cdot (-3xy) = 9x^3y + 3xy^3 - 6x^2y^2$ nên:<br>$A = (9x^3y + 3xy^3 - 6x^2y^2) : (-3xy)$<br>$A = (9x^3y : -3xy) + (3xy^3 : -3xy) - (6x^2y^2 : -3xy)$<br>$A = -3x^2 - y^2 + 2xy$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (23 phút)
a) Mục tiêu: Củng cố kỹ năng chia đơn thức cho đơn thức và chia đa thức cho đơn thức thông qua giải các bài tập SGK trang 24.
b) Nội dung: HS làm các bài tập 1.30, 1.31, 1.32 SGK.
c) Sản phẩm: Bài làm hoàn chỉnh các bài tập 1.30, 1.31, 1.32 trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ cho HS hoạt động cá nhân làm Bài 1.30, 1.31 và 1.32 SGK trang 24.<br>- **HS:** Nhận nhiệm vụ, mở SGK và làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện tính toán cẩn thận.<br>- **GV:** Quan sát, giúp đỡ các HS còn lúng túng trong việc tìm thương có phân số hoặc dấu trừ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Gọi 3 HS lên bảng trình bày 3 bài tập.<br>- **HS:** Nhận xét, đối chiếu kết quả với bài làm của mình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét bài làm của HS trên bảng, chỉ rõ các lỗi sai thường gặp về dấu và luỹ thừa. | **Bài 1.30 (SGK trang 24):**<br>a) Ta có $\frac{7}{3}x^3y^2 : M = 7xy^2$, suy ra:<br>$M = \frac{7}{3}x^3y^2 : 7xy^2 = \frac{1}{3}x^2$.<br>b) $N : 0,5xy^2z = -xy$, suy ra:<br>$N = (-xy) \cdot 0,5xy^2z = -0,5x^2y^3z$.<br><br>**Bài 1.31 (SGK trang 24):**<br>Đa thức $A = 9xy^4 - 12x^2y^3 + 6x^3y^2$.<br>a) Với $B = 3x^2y$: Hạng tử $9xy^4$ có số mũ của $x$ là 1 < 2 nên không chia hết cho $B$. Do đó đa thức $A$ không chia hết cho $B$.<br>b) Với $B = -3xy^2$: Mọi hạng tử của $A$ đều có số mũ của $x \ge 1$ và số mũ của $y \ge 2$, nên $A$ chia hết cho $B$.<br>Thương là:<br>$A : B = (9xy^4 - 12x^2y^3 + 6x^3y^2) : (-3xy^2)$<br>$= -3y^2 + 4xy - 2x^2$.<br><br>**Bài 1.32 (SGK trang 24):**<br>$(7y^5z^2 - 14y^4z^3 + 2,1y^3z^4) : (-7y^3z^2)$<br>$= [7y^5z^2 : (-7y^3z^2)] - [14y^4z^3 : (-7y^3z^2)] + [2,1y^3z^4 : (-7y^3z^2)]$<br>$= -y^2 + 2yz - 0,3z^2$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)
a) Mục tiêu: Vận dụng kiến thức chia đa thức cho đơn thức vào bài toán tìm diện tích và khối lượng trong hình học thực tế.
b) Nội dung: HS giải bài toán thực tế: Một mảnh vườn hình chữ nhật có diện tích được biểu diễn bởi $S = 12x^3y + 8x^2y^2 - 4xy$ ($\text{m}^2$) và chiều rộng là $2xy$ ($\text{m}$). Tính chiều dài của mảnh vườn.
c) Sản phẩm: Lời giải bài toán thực tế của HS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đưa ra bài toán thực tế mảnh vườn: Cho diện tích $S = 12x^3y + 8x^2y^2 - 4xy$ và chiều rộng $b = 2xy$. Tìm công thức tính chiều dài $a$.<br>- **HS:** Đọc kỹ đề bài và xác định mối liên hệ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chiều dài = Diện tích : Chiều rộng.<br>- **HS:** Thực hiện phép chia đa thức cho đơn thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đọc kết quả: $a = 6x^2 + 4xy - 2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại ý nghĩa thực tiễn của phép chia đa thức trong các đại lượng hình học.<br>- **GV dặn dò về nhà:** Ôn tập quy tắc chia đơn thức, đa thức; làm lại các bài tập; chuẩn bị bài tiết sau "Luyện tập chung". | **Bài toán thực tế vận dụng:**<br>Chiều dài của mảnh vườn hình chữ nhật là:<br>$a = S : b = (12x^3y + 8x^2y^2 - 4xy) : 2xy$<br>$a = (12x^3y : 2xy) + (8x^2y^2 : 2xy) - (4xy : 2xy)$<br>$a = 6x^2 + 4xy - 2$ ($\text{m}$).<br><br>**Hướng dẫn tự học tại nhà:**<br>- Ghi nhớ điều kiện chia hết và quy tắc chia đơn thức, đa thức.<br>- Làm bài tập trong Sách bài tập Toán 8.<br>- Xem trước các ví dụ và bài tập của tiết Luyện tập chung. |
"""

with open(os.path.join(OUT_DIR, "BAI_01.md"), "w", encoding="utf-8") as f:
    f.write(bai_01_content.strip())
print("Saved BAI_01.md")
