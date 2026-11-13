**TIẾT 46, 47, 48, 49 - BÀI 19: PHƯƠNG TRÌNH BẬC HAI MỘT ẨN**
*Thời lượng thực hiện: 04 tiết (180 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa phương trình bậc hai một ẩn: Dạng tổng quát $ax^2 + bx + c = 0$ ($a \neq 0$), trong đó $x$ là ẩn; $a, b, c$ là các số cho trước gọi là hệ số.
- Nhận biết các trường hợp khuyết hệ số: Khuyết $c$ ($ax^2 + bx = 0$), khuyết $b$ ($ax^2 + c = 0$) và phương pháp giải nhanh không dùng biệt thức.
- Nắm vững công thức nghiệm tổng quát thông qua biệt thức $\Delta = b^2 - 4ac$:
  + $\Delta > 0$: Phương trình có hai nghiệm phân biệt $x_1 = \frac{-b + \sqrt{\Delta}}{2a};\; x_2 = \frac{-b - \sqrt{\Delta}}{2a}$.
  + $\Delta = 0$: Phương trình có nghiệm kép $x_1 = x_2 = -\frac{b}{2a}$.
  + $\Delta < 0$: Phương trình vô nghiệm.
- Nắm vững công thức nghiệm thu gọn khi hệ số $b = 2b'$ qua biệt thức $\Delta' = b'^2 - ac$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tính toán biệt thức $\Delta$ và $\Delta'$, đối chiếu điều kiện để kết luận số nghiệm và giá trị nghiệm chính xác.
- Giao tiếp và hợp tác: Làm việc nhóm phân loại phương trình bậc hai và trao đổi kinh nghiệm tránh sai sót về dấu.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Biến đổi đại số chặt chẽ đưa phương trình về dạng bình phương một tổng/hiệu để chứng minh công thức nghiệm.
- Năng lực giải quyết vấn đề toán học: Giải các phương trình bậc hai quy về hoặc chứa tham số.

c) Năng lực số (NLS):
- ***5.3.TC2a: HS sử dụng chức năng giải phương trình bậc hai trên máy tính cầm tay để tìm nghiệm và kiểm tra kết quả giải tự luận; 3.1.TC2a: HS sử dụng công cụ số (GeoGebra/trình chiếu) để mô hình hóa và trình bày các bước giải bài Phương trình bậc hai một ẩn.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn trọng, tỉ mỉ khi xác định các hệ số $a, b, c$ (đặc biệt khi hệ số mang dấu âm).
- Tinh thần kiên trì, không nản lòng khi gặp các số liệu căn thức phức tạp.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, máy tính cầm tay chiếu màn hình giả lập, bài trình chiếu.
2. Học sinh: SGK Toán 9 Tập 2, vở ghi, máy tính cầm tay có chức năng giải phương trình bậc hai (EQUA/Equation).

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề bài toán tìm kích thước thửa ruộng hình chữ nhật dẫn tới phương trình bậc hai.
b) Nội dung: Một thửa ruộng hình chữ nhật có chiều dài hơn chiều rộng $5\text{ m}$ và diện tích bằng $150\text{ m}^2$. Tìm chiều rộng của thửa ruộng.
c) Sản phẩm: Phương trình $x(x + 5) = 150 \Rightarrow x^2 + 5x - 150 = 0$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gọi chiều rộng thửa ruộng là $x\text{ (m, } x > 0)$. Chiều dài là $x + 5$. Hãy lập phương trình diện tích.<br>- **HS:** Lập phương trình $x(x + 5) = 150$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Biến đổi: $x^2 + 5x - 150 = 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phương trình này chứa $x^2$ nên không phải bậc nhất. Ta gọi nó là gì và giải ra sao?<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đây là phương trình bậc hai một ẩn. Bài học hôm nay ta học cách giải tổng quát. | Phương trình $x^2 + 5x - 150 = 0$ là phương trình bậc hai một ẩn. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (140 phút)
### Hoạt động 2.1: Định nghĩa phương trình bậc hai và các dạng khuyết (35 phút)
a) Mục tiêu: Nhận biết phương trình bậc hai, chỉ rõ các hệ số $a, b, c$ và giải thành thạo dạng khuyết $b$ hoặc khuyết $c$.
b) Nội dung: Định nghĩa dạng tổng quát $ax^2 + bx + c = 0$ ($a \neq 0$); giải phương trình $2x^2 - 8 = 0$ và $3x^2 - 6x = 0$.
c) Sản phẩm: Vở ghi định nghĩa và lời giải phương trình dạng khuyết.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Phương trình bậc hai một ẩn là phương trình có dạng $ax^2 + bx + c = 0$ ($a \neq 0$). Nêu cách giải khi $c = 0$ (đặt nhân tử chung) và khi $b = 0$ (chuyển vế lấy căn).<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải: $2x^2 - 8 = 0 \Rightarrow x^2 = 4 \Rightarrow x = 2$ hoặc $x = -2$.<br>Giải: $3x^2 - 6x = 0 \Rightarrow 3x(x - 2) = 0 \Rightarrow x = 0$ hoặc $x = 2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng làm 2 ví dụ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Với phương trình khuyết, giải bằng phương pháp đưa về tích hoặc khai căn nhanh hơn rất nhiều so với dùng công thức tổng quát. | **1. Định nghĩa và dạng khuyết:**<br>- Phương trình bậc hai một ẩn: $ax^2 + bx + c = 0$ ($a \neq 0$).<br>- Dạng khuyết $c$ ($ax^2 + bx = 0$): Đặt $x(ax + b) = 0 \Rightarrow x = 0$ hoặc $x = -\frac{b}{a}$.<br>- Dạng khuyết $b$ ($ax^2 + c = 0$): $x^2 = -\frac{c}{a}$. Nếu $-\frac{c}{a} \ge 0$ thì $x = \pm \sqrt{-\frac{c}{a}}$; nếu $-\frac{c}{a} < 0$ thì vô nghiệm. |

### Hoạt động 2.2: Công thức nghiệm tổng quát qua biệt thức $\Delta$ (55 phút)
a) Mục tiêu: Nắm vững và vận dụng biệt thức $\Delta = b^2 - 4ac$ để giải phương trình bậc hai tổng quát.
b) Nội dung: Chứng minh công thức nghiệm bằng biến đổi tách bình phương; quy tắc tính nghiệm theo dấu của $\Delta$.
c) Sản phẩm: Bảng công thức nghiệm trong vở và bài tập áp dụng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa biệt thức $\Delta = b^2 - 4ac$.<br>Phát biểu định lí công thức nghiệm:<br>- $\Delta > 0$: 2 nghiệm phân biệt $x_1 = \frac{-b + \sqrt{\Delta}}{2a};\; x_2 = \frac{-b - \sqrt{\Delta}}{2a}$.<br>- $\Delta = 0$: Nghiệm kép $x_1 = x_2 = -\frac{b}{2a}$.<br>- $\Delta < 0$: Phương trình vô nghiệm.<br>- **HS:** Ghi chép công thức cẩn thận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải phương trình: $x^2 - 7x + 12 = 0$.<br>Hệ số $a = 1, b = -7, c = 12$.<br>$\Delta = (-7)^2 - 4 \cdot 1 \cdot 12 = 49 - 48 = 1 > 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $\sqrt{\Delta} = 1$. Suy ra $x_1 = \frac{7 + 1}{2} = 4$; $x_2 = \frac{7 - 1}{2} = 3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Cần xác định đúng dấu của các hệ số $a, b, c$, đặc biệt $b = -7$ thì $(-7)^2 = 49$ chứ không phải $-49$. | **2. Công thức nghiệm tổng quát:**<br>Phương trình $ax^2 + bx + c = 0$ ($a \neq 0$).<br>Biệt thức: $\Delta = b^2 - 4ac$.<br>- Nếu $\Delta > 0$, phương trình có hai nghiệm phân biệt:<br>$$x_1 = \frac{-b + \sqrt{\Delta}}{2a};\quad x_2 = \frac{-b - \sqrt{\Delta}}{2a}$$<br>- Nếu $\Delta = 0$, phương trình có nghiệm kép:<br>$$x_1 = x_2 = -\frac{b}{2a}$$<br>- Nếu $\Delta < 0$, phương trình vô nghiệm. |

### Hoạt động 2.3: Công thức nghiệm thu gọn và bấm máy tính kiểm tra (50 phút)
a) Mục tiêu: Nắm vững công thức nghiệm thu gọn với $\Delta' = b'^2 - ac$ khi $b$ chẵn và biết dùng MTBT kiểm tra kết quả.
b) Nội dung: Quy tắc giải nhanh bằng $\Delta'$ và thao tác bấm máy Casio (MODE 5-3 hoặc MENU 9-2-2).
c) Sản phẩm: Vở ghi công thức nghiệm thu gọn và kỹ năng bấm máy tính kiểm tra nghiệm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khi $b = 2b'$, đặt $\Delta' = b'^2 - ac$. Nếu $\Delta' > 0$ thì $x = \frac{-b' \pm \sqrt{\Delta'}}{a}$. Hướng dẫn bấm MTBT kiểm tra nghiệm.<br>- **HS:** Ghi chép và chuẩn bị máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải phương trình: $3x^2 - 8x + 4 = 0$.<br>Ta có $b = -8 \Rightarrow b' = -4$. $\Delta' = (-4)^2 - 3 \cdot 4 = 16 - 12 = 4 > 0$.<br>Nghiệm: $x_1 = \frac{4 + 2}{3} = 2$; $x_2 = \frac{4 - 2}{3} = \frac{2}{3}$.<br>Bấm máy kiểm tra thấy ra đúng $2$ và $\frac{2}{3}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS trình bày lời giải và nêu thao tác bấm máy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét sự tiện lợi của công thức thu gọn giúp số tính toán nhỏ hơn nhiều. | **3. Công thức nghiệm thu gọn:**<br>Khi $b = 2b'$, xét biệt thức thu gọn: $\Delta' = b'^2 - ac$.<br>- $\Delta' > 0$: Hai nghiệm phân biệt: $x_1 = \frac{-b' + \sqrt{\Delta'}}{a};\; x_2 = \frac{-b' - \sqrt{\Delta'}}{a}$.<br>- $\Delta' = 0$: Nghiệm kép: $x_1 = x_2 = -\frac{b'}{a}$.<br>- $\Delta' < 0$: Vô nghiệm.<br>*Tích hợp NLS:* Sử dụng chức năng Equation trên MTBT để đối chiếu kết quả. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (30 phút)
a) Mục tiêu: Giải phương trình bài toán mở đầu để tìm kích thước thửa ruộng.
b) Nội dung: Giải phương trình $x^2 + 5x - 150 = 0$.
c) Sản phẩm: Lời giải tìm được $x = 10$ (thỏa mãn) và $x = -15$ (loại). Chiều rộng $10\text{ m}$, chiều dài $15\text{ m}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giải phương trình mở đầu: $x^2 + 5x - 150 = 0$.<br>- **HS:** Tính biệt thức $\Delta$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $\Delta = 5^2 - 4 \cdot 1 \cdot (-150) = 25 + 600 = 625 = 25^2 > 0$.<br>Nghiệm: $x_1 = \frac{-5 + 25}{2} = 10$ (thỏa mãn $x > 0$);<br>$x_2 = \frac{-5 - 25}{2} = -15$ (loại do $x > 0$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, lưu ý khi giải bài toán thực tế phải đối chiếu điều kiện để loại nghiệm không thích hợp. | **Bài giải:**<br>Phương trình $x^2 + 5x - 150 = 0$ có $a = 1, b = 5, c = -150$.<br>Biệt thức:<br>$$\Delta = 5^2 - 4 \cdot 1 \cdot (-150) = 25 + 600 = 625 > 0$$<br>Ta có $\sqrt{\Delta} = \sqrt{625} = 25$.<br>Phương trình có hai nghiệm phân biệt:<br>$$x_1 = \frac{-5 + 25}{2} = 10\text{ (thỏa mãn ĐK)}$$<br>$$x_2 = \frac{-5 - 25}{2} = -15\text{ (loại)}$$<br>Vậy chiều rộng thửa ruộng là $10\text{ m}$ và chiều dài là $15\text{ m}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhận biết dấu hiệu phương trình có hai nghiệm trái dấu khi $a$ và $c$ trái dấu ($a \cdot c < 0$).
b) Nội dung: Vì sao khi $ac < 0$ thì phương trình luôn luôn có 2 nghiệm phân biệt mà không cần tính $\Delta$?
c) Sản phẩm: Giải thích của HS: Vì $ac < 0 \Rightarrow -4ac > 0$, mà $b^2 \ge 0$ nên $\Delta = b^2 - 4ac > 0$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nếu $a$ và $c$ trái dấu ($ac < 0$), có kết luận gì về số nghiệm của phương trình?<br>- **HS:** Suy nghĩ và phân tích biểu thức $\Delta$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $ac < 0 \Rightarrow -4ac > 0 \Rightarrow \Delta = b^2 - 4ac > 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phương trình luôn có 2 nghiệm phân biệt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt định lí: Khi $ac < 0$, phương trình luôn có hai nghiệm phân biệt trái dấu. | **Nhận xét quan trọng:**<br>Nếu $ac < 0$ thì phương trình $ax^2 + bx + c = 0$ luôn có hai nghiệm phân biệt trái dấu. |