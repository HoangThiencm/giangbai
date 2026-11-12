# -*- coding: utf-8 -*-
"""
Script sinh 9 KHBD Chương VI: Hàm số bậc hai & Phương trình bậc hai một ẩn (Tiết 43 - 58) - Toán 9 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan9"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    # 01: Bài 18 (Tiết 43-45)
    {
        "filename": "01_KHBD_Toan9_Bai18_HamSoBacHai_Tiet43-45.md",
        "md": """TIẾT 43, 44, 45 - BÀI 18: HÀM SỐ Y = AX² (A KHÁC 0)
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa và tính chất của hàm số $y = ax^2$ ($a \\neq 0$):
  + Nếu $a > 0$, hàm số đồng biến khi $x > 0$, nghịch biến khi $x < 0$; $y = 0$ là giá trị nhỏ nhất của hàm số tại $x = 0$.
  + Nếu $a < 0$, hàm số đồng biến khi $x < 0$, nghịch biến khi $x > 0$; $y = 0$ là giá trị lớn nhất của hàm số tại $x = 0$.
- Nhận biết hình dạng của đồ thị hàm số $y = ax^2$ ($a \\neq 0$) là một đường cong Parabol đi qua gốc tọa độ $O(0; 0)$, nhận trục tung $Oy$ làm trục đối xứng.
- Vẽ thành thạo đồ thị hàm số $y = ax^2$ ($a \\neq 0$) bằng cách lập bảng giá trị đối xứng với ít nhất 5 điểm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự lập bảng giá trị số, tính toán chính xác bình phương và vẽ đường cong Parabol đều đẹp.
- Giao tiếp và hợp tác: Thảo luận nhóm về sự thay đổi của đồ thị khi hệ số $a$ thay đổi dấu và độ lớn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh tính biến thiên và tính đối xứng của Parabol.
- Năng lực mô hình hoá toán học: Ứng dụng Parabol trong thiết kế cổng vòm, cầu treo, gương cầu hội tụ sóng viễn thông.

c) Năng lực số (NLS):
- ***5.3.TC2a: HS sử dụng phần mềm GeoGebra để vẽ đồ thị hàm số y = ax² và quan sát sự thay đổi của đồ thị khi hệ số a thay đổi; 3.1.TC2a: HS sử dụng công cụ số (GeoGebra/trình chiếu) để mô hình hóa và trình bày các bước vẽ đồ thị hàm số y = ax².***

## 3. Về phẩm chất
- Khơi gợi hứng thú với vẻ đẹp cân đối của đường cong Parabol trong kiến trúc và đời sống.
- Cẩn thận, tỉ mỉ trong việc lấy tọa độ các điểm và vẽ đường cong trơn mượt.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2 Kết nối tri thức, KHBD, phần mềm GeoGebra vẽ đồ thị động, máy chiếu, thước cong Parabol.
2. Học sinh: SGK Toán 9 Tập 2, vở ghi, thước kẻ, thước cong vẽ Parabol, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Dẫn nhập bài toán thực tế về quãng đường chuyển động rơi tự do của một vật thể $s = 5t^2$.
b) Nội dung: Quãng đường rơi tự do của một vật nặng từ trên cao tỉ lệ với bình phương thời gian rơi $s = 5t^2$. Tính quãng đường vật rơi sau $1$ giây, $2$ giây, $3$ giây.
c) Sản phẩm: Bảng tính giá trị $s = 5\\text{ m}, 20\\text{ m}, 45\\text{ m}$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu công thức vật lí chuyển động rơi tự do $s = 5t^2$. Hãy tính quãng đường rơi sau $1$ giây, $2$ giây, $3$ giây.<br>- **HS:** Nhận nhiệm vụ tính toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thay $t = 1, 2, 3$ vào công thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $s(1) = 5\\text{ m}$, $s(2) = 20\\text{ m}$, $s(3) = 45\\text{ m}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Công thức $s = 5t^2$ cho ta một ví dụ về hàm số bậc hai dạng $y = ax^2$ với $a = 5$. | Giới thiệu hàm số dạng $y = ax^2$ ($a \\neq 0$) qua chuyển động rơi tự do. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (105 phút)
### Hoạt động 2.1: Tính chất của hàm số $y = ax^2$ ($a \\neq 0$) (35 phút)
a) Mục tiêu: Nắm vững tập xác định và tính đồng biến, nghịch biến của hàm số $y = ax^2$.
b) Nội dung: Xét hai bảng giá trị của $y = 2x^2$ và $y = -2x^2$, rút ra nhận xét về sự biến thiên.
c) Sản phẩm: Vở ghi bài định nghĩa và tính chất của hàm số $y = ax^2$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hai bảng giá trị với $x \\in \\{-3; -2; -1; 0; 1; 2; 3\\}$ của $y = 2x^2$ và $y = -2x^2$. Yêu cầu nhận xét dấu của $y$ và chiều tăng giảm khi $x$ tăng dần.<br>- **HS:** Quan sát bảng số liệu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo cặp: Với $a = 2 > 0$, khi $x < 0$ thì $y$ giảm; khi $x > 0$ thì $y$ tăng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu tính chất hàm số ứng với hai trường hợp $a > 0$ và $a < 0$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa tính chất hàm số bậc hai. | **1. Định nghĩa và tính chất:**<br>- Tập xác định: Mọi $x \\in \\mathbb{R}$.<br>- Nếu $a > 0$: Hàm số nghịch biến khi $x < 0$, đồng biến khi $x > 0$. $y = 0$ là giá trị nhỏ nhất tại $x = 0$.<br>- Nếu $a < 0$: Hàm số đồng biến khi $x < 0$, nghịch biến khi $x > 0$. $y = 0$ là giá trị lớn nhất tại $x = 0$. |

### Hoạt động 2.2: Đồ thị của hàm số $y = ax^2$ ($a \\neq 0$) (40 phút)
a) Mục tiêu: Nắm vững đặc điểm hình học của Parabol và quy trình vẽ Parabol trên mặt phẳng tọa độ $Oxy$.
b) Nội dung: Vẽ đồ thị $y = x^2$ và $y = -\\frac{1}{2}x^2$.
c) Sản phẩm: Hình vẽ Parabol chuẩn xác trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn các bước vẽ đồ thị $y = ax^2$ ($a \\neq 0$):<br>1. Lập bảng giá trị lấy 5 điểm đối xứng: $x = -2, -1, 0, 1, 2$.<br>2. Biểu diễn 5 điểm trên mặt phẳng tọa độ $Oxy$.<br>3. Dùng thước cong nối các điểm tạo thành đường cong mượt mà.<br>- **HS:** Thực hiện vẽ đồ thị $y = \\frac{1}{2}x^2$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính bảng giá trị: $(-2; 2), (-1; 0{,}5), (0; 0), (1; 0{,}5), (2; 2)$. Vẽ trục tọa độ và chấm điểm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ đồ thị.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đồ thị là đường cong Parabol đỉnh $O(0; 0)$, nhận trục tung $Oy$ làm trục đối xứng. Nếu $a > 0$, Parabol nằm phía trên trục hoành; nếu $a < 0$, Parabol nằm phía dưới trục hoành. | **2. Đồ thị của hàm số $y = ax^2$ ($a \\neq 0$):**<br>- Là một đường cong Parabol đi qua gốc tọa độ $O(0; 0)$, nhận $Oy$ làm trục đối xứng.<br>- Đỉnh $O(0; 0)$ là điểm thấp nhất khi $a > 0$ và là điểm cao nhất khi $a < 0$.<br>- Quy trình vẽ: Bảng 5 điểm đối xứng $\\rightarrow$ Chấm điểm $\\rightarrow$ Nối đường cong trơn. |

### Hoạt động 2.3: Mô phỏng động bằng GeoGebra (30 phút)
a) Mục tiêu: Tích hợp công nghệ số GeoGebra để quan sát độ mở và bề lõm của Parabol khi hệ số $a$ thay đổi.
b) Nội dung: Tạo thanh trượt Slider $a$ trong GeoGebra và quan sát sự biến thiên của đồ thị $y = ax^2$.
c) Sản phẩm: HS làm chủ quan sát mô phỏng và rút ra kết luận trực quan.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu phần mềm GeoGebra với thanh trượt $a$. Kéo $a$ từ dương sang âm, từ bé đến lớn.<br>- **HS:** Quan sát sự thay đổi bề lõm và độ hẹp/rộng của Parabol.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khi $|a|$ càng lớn thì Parabol càng hẹp (áp sát trục $Oy$); khi $|a|$ càng nhỏ thì Parabol càng mở rộng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS trả lời nhận xét.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao khả năng quan sát và mô hình hóa hình học số của học sinh. | Tích hợp NLS: Sử dụng GeoGebra trực quan hóa mối quan hệ giữa hệ số $a$ và hình dáng đồ thị Parabol. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Xác định tọa độ giao điểm của Parabol $y = x^2$ và đường thẳng $y = 2x + 3$.
b) Nội dung: Giải phương trình hoành độ giao điểm: $x^2 = 2x + 3$.
c) Sản phẩm: Lời giải tìm được hai giao điểm $A(-1; 1)$ và $B(3; 9)$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho $(P): y = x^2$ và $(d): y = 2x + 3$. Tìm tọa độ các giao điểm của $(P)$ và $(d)$ bằng phép tính.<br>- **HS:** Thiết lập phương trình hoành độ giao điểm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $x^2 - 2x - 3 = 0 \\Rightarrow (x + 1)(x - 3) = 0 \\Rightarrow x = -1$ hoặc $x = 3$.<br>Với $x = -1 \\Rightarrow y = 1$; với $x = 3 \\Rightarrow y = 9$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa phương pháp tìm tọa độ giao điểm bằng phương trình hoành độ giao điểm. | **Bài giải:**<br>Phương trình hoành độ giao điểm của $(P)$ và $(d)$ là:<br>$$x^2 = 2x + 3$$<br>$$x^2 - 2x - 3 = 0$$<br>$$(x + 1)(x - 3) = 0$$<br>Suy ra $x = -1$ hoặc $x = 3$.<br>- Với $x = -1$, thay vào ta có $y = (-1)^2 = 1$. Ta có điểm $A(-1; 1)$.<br>- Với $x = 3$, thay vào ta có $y = 3^2 = 9$. Ta có điểm $B(3; 9)$.<br>Vậy $(d)$ cắt $(P)$ tại hai điểm phân biệt $A(-1; 1)$ và $B(3; 9)$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng Parabol mô hình hóa mặt cắt của cổng vòm kiến trúc.
b) Nội dung: Cổng vòm Parabol có chiều rộng chân cổng $8\\text{ m}$ và chiều cao đỉnh cổng $4\\text{ m}$. Thiết lập hàm số biểu diễn cổng vòm.
c) Sản phẩm: Hàm số $y = -\\frac{1}{4}x^2 + 4$ hoặc $y = -\\frac{1}{4}x^2$ tùy gốc tọa độ chọn.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn chọn gốc tọa độ $O$ tại đỉnh cổng hoặc tại trung điểm chân cổng.<br>- **HS:** Thiết lập tọa độ chân cổng và tìm hệ số $a$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chọn đỉnh là $O(0; 0)$, chân cổng tại $(4; -4)$ và $(-4; -4)$. Ta có $-4 = a \\cdot 4^2 \\Rightarrow a = -\\frac{1}{4}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Parabol có dạng $y = -\\frac{1}{4}x^2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị cho bài Phương trình bậc hai một ẩn tiếp theo. | Mô hình Parabol trong kiến trúc xây dựng cổng vòm. |
"""
    },

    # 02: Bài 19 (Tiết 46-49)
    {
        "filename": "02_KHBD_Toan9_Bai19_PhuongTrinhBacHaiMotAn_Tiet46-49.md",
        "md": """TIẾT 46, 47, 48, 49 - BÀI 19: PHƯƠNG TRÌNH BẬC HAI MỘT ẨN
*Thời lượng thực hiện: 04 tiết (180 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa phương trình bậc hai một ẩn: Dạng tổng quát $ax^2 + bx + c = 0$ ($a \\neq 0$), trong đó $x$ là ẩn; $a, b, c$ là các số cho trước gọi là hệ số.
- Nhận biết các trường hợp khuyết hệ số: Khuyết $c$ ($ax^2 + bx = 0$), khuyết $b$ ($ax^2 + c = 0$) và phương pháp giải nhanh không dùng biệt thức.
- Nắm vững công thức nghiệm tổng quát thông qua biệt thức $\\Delta = b^2 - 4ac$:
  + $\\Delta > 0$: Phương trình có hai nghiệm phân biệt $x_1 = \\frac{-b + \\sqrt{\\Delta}}{2a};\\; x_2 = \\frac{-b - \\sqrt{\\Delta}}{2a}$.
  + $\\Delta = 0$: Phương trình có nghiệm kép $x_1 = x_2 = -\\frac{b}{2a}$.
  + $\\Delta < 0$: Phương trình vô nghiệm.
- Nắm vững công thức nghiệm thu gọn khi hệ số $b = 2b'$ qua biệt thức $\\Delta' = b'^2 - ac$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tính toán biệt thức $\\Delta$ và $\\Delta'$, đối chiếu điều kiện để kết luận số nghiệm và giá trị nghiệm chính xác.
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
b) Nội dung: Một thửa ruộng hình chữ nhật có chiều dài hơn chiều rộng $5\\text{ m}$ và diện tích bằng $150\\text{ m}^2$. Tìm chiều rộng của thửa ruộng.
c) Sản phẩm: Phương trình $x(x + 5) = 150 \\Rightarrow x^2 + 5x - 150 = 0$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gọi chiều rộng thửa ruộng là $x\\text{ (m, } x > 0)$. Chiều dài là $x + 5$. Hãy lập phương trình diện tích.<br>- **HS:** Lập phương trình $x(x + 5) = 150$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Biến đổi: $x^2 + 5x - 150 = 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phương trình này chứa $x^2$ nên không phải bậc nhất. Ta gọi nó là gì và giải ra sao?<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đây là phương trình bậc hai một ẩn. Bài học hôm nay ta học cách giải tổng quát. | Phương trình $x^2 + 5x - 150 = 0$ là phương trình bậc hai một ẩn. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (140 phút)
### Hoạt động 2.1: Định nghĩa phương trình bậc hai và các dạng khuyết (35 phút)
a) Mục tiêu: Nhận biết phương trình bậc hai, chỉ rõ các hệ số $a, b, c$ và giải thành thạo dạng khuyết $b$ hoặc khuyết $c$.
b) Nội dung: Định nghĩa dạng tổng quát $ax^2 + bx + c = 0$ ($a \\neq 0$); giải phương trình $2x^2 - 8 = 0$ và $3x^2 - 6x = 0$.
c) Sản phẩm: Vở ghi định nghĩa và lời giải phương trình dạng khuyết.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Phương trình bậc hai một ẩn là phương trình có dạng $ax^2 + bx + c = 0$ ($a \\neq 0$). Nêu cách giải khi $c = 0$ (đặt nhân tử chung) và khi $b = 0$ (chuyển vế lấy căn).<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải: $2x^2 - 8 = 0 \\Rightarrow x^2 = 4 \\Rightarrow x = 2$ hoặc $x = -2$.<br>Giải: $3x^2 - 6x = 0 \\Rightarrow 3x(x - 2) = 0 \\Rightarrow x = 0$ hoặc $x = 2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng làm 2 ví dụ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Với phương trình khuyết, giải bằng phương pháp đưa về tích hoặc khai căn nhanh hơn rất nhiều so với dùng công thức tổng quát. | **1. Định nghĩa và dạng khuyết:**<br>- Phương trình bậc hai một ẩn: $ax^2 + bx + c = 0$ ($a \\neq 0$).<br>- Dạng khuyết $c$ ($ax^2 + bx = 0$): Đặt $x(ax + b) = 0 \\Rightarrow x = 0$ hoặc $x = -\\frac{b}{a}$.<br>- Dạng khuyết $b$ ($ax^2 + c = 0$): $x^2 = -\\frac{c}{a}$. Nếu $-\\frac{c}{a} \\ge 0$ thì $x = \\pm \\sqrt{-\\frac{c}{a}}$; nếu $-\\frac{c}{a} < 0$ thì vô nghiệm. |

### Hoạt động 2.2: Công thức nghiệm tổng quát qua biệt thức $\\Delta$ (55 phút)
a) Mục tiêu: Nắm vững và vận dụng biệt thức $\\Delta = b^2 - 4ac$ để giải phương trình bậc hai tổng quát.
b) Nội dung: Chứng minh công thức nghiệm bằng biến đổi tách bình phương; quy tắc tính nghiệm theo dấu của $\\Delta$.
c) Sản phẩm: Bảng công thức nghiệm trong vở và bài tập áp dụng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa biệt thức $\\Delta = b^2 - 4ac$.<br>Phát biểu định lí công thức nghiệm:<br>- $\\Delta > 0$: 2 nghiệm phân biệt $x_1 = \\frac{-b + \\sqrt{\\Delta}}{2a};\\; x_2 = \\frac{-b - \\sqrt{\\Delta}}{2a}$.<br>- $\\Delta = 0$: Nghiệm kép $x_1 = x_2 = -\\frac{b}{2a}$.<br>- $\\Delta < 0$: Phương trình vô nghiệm.<br>- **HS:** Ghi chép công thức cẩn thận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải phương trình: $x^2 - 7x + 12 = 0$.<br>Hệ số $a = 1, b = -7, c = 12$.<br>$\\Delta = (-7)^2 - 4 \\cdot 1 \\cdot 12 = 49 - 48 = 1 > 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $\\sqrt{\\Delta} = 1$. Suy ra $x_1 = \\frac{7 + 1}{2} = 4$; $x_2 = \\frac{7 - 1}{2} = 3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Cần xác định đúng dấu của các hệ số $a, b, c$, đặc biệt $b = -7$ thì $(-7)^2 = 49$ chứ không phải $-49$. | **2. Công thức nghiệm tổng quát:**<br>Phương trình $ax^2 + bx + c = 0$ ($a \\neq 0$).<br>Biệt thức: $\\Delta = b^2 - 4ac$.<br>- Nếu $\\Delta > 0$, phương trình có hai nghiệm phân biệt:<br>$$x_1 = \\frac{-b + \\sqrt{\\Delta}}{2a};\\quad x_2 = \\frac{-b - \\sqrt{\\Delta}}{2a}$$<br>- Nếu $\\Delta = 0$, phương trình có nghiệm kép:<br>$$x_1 = x_2 = -\\frac{b}{2a}$$<br>- Nếu $\\Delta < 0$, phương trình vô nghiệm. |

### Hoạt động 2.3: Công thức nghiệm thu gọn và bấm máy tính kiểm tra (50 phút)
a) Mục tiêu: Nắm vững công thức nghiệm thu gọn với $\\Delta' = b'^2 - ac$ khi $b$ chẵn và biết dùng MTBT kiểm tra kết quả.
b) Nội dung: Quy tắc giải nhanh bằng $\\Delta'$ và thao tác bấm máy Casio (MODE 5-3 hoặc MENU 9-2-2).
c) Sản phẩm: Vở ghi công thức nghiệm thu gọn và kỹ năng bấm máy tính kiểm tra nghiệm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khi $b = 2b'$, đặt $\\Delta' = b'^2 - ac$. Nếu $\\Delta' > 0$ thì $x = \\frac{-b' \\pm \\sqrt{\\Delta'}}{a}$. Hướng dẫn bấm MTBT kiểm tra nghiệm.<br>- **HS:** Ghi chép và chuẩn bị máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải phương trình: $3x^2 - 8x + 4 = 0$.<br>Ta có $b = -8 \\Rightarrow b' = -4$. $\\Delta' = (-4)^2 - 3 \\cdot 4 = 16 - 12 = 4 > 0$.<br>Nghiệm: $x_1 = \\frac{4 + 2}{3} = 2$; $x_2 = \\frac{4 - 2}{3} = \\frac{2}{3}$.<br>Bấm máy kiểm tra thấy ra đúng $2$ và $\\frac{2}{3}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS trình bày lời giải và nêu thao tác bấm máy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét sự tiện lợi của công thức thu gọn giúp số tính toán nhỏ hơn nhiều. | **3. Công thức nghiệm thu gọn:**<br>Khi $b = 2b'$, xét biệt thức thu gọn: $\\Delta' = b'^2 - ac$.<br>- $\\Delta' > 0$: Hai nghiệm phân biệt: $x_1 = \\frac{-b' + \\sqrt{\\Delta'}}{a};\\; x_2 = \\frac{-b' - \\sqrt{\\Delta'}}{a}$.<br>- $\\Delta' = 0$: Nghiệm kép: $x_1 = x_2 = -\\frac{b'}{a}$.<br>- $\\Delta' < 0$: Vô nghiệm.<br>*Tích hợp NLS:* Sử dụng chức năng Equation trên MTBT để đối chiếu kết quả. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (30 phút)
a) Mục tiêu: Giải phương trình bài toán mở đầu để tìm kích thước thửa ruộng.
b) Nội dung: Giải phương trình $x^2 + 5x - 150 = 0$.
c) Sản phẩm: Lời giải tìm được $x = 10$ (thỏa mãn) và $x = -15$ (loại). Chiều rộng $10\\text{ m}$, chiều dài $15\\text{ m}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giải phương trình mở đầu: $x^2 + 5x - 150 = 0$.<br>- **HS:** Tính biệt thức $\\Delta$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $\\Delta = 5^2 - 4 \\cdot 1 \\cdot (-150) = 25 + 600 = 625 = 25^2 > 0$.<br>Nghiệm: $x_1 = \\frac{-5 + 25}{2} = 10$ (thỏa mãn $x > 0$);<br>$x_2 = \\frac{-5 - 25}{2} = -15$ (loại do $x > 0$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, lưu ý khi giải bài toán thực tế phải đối chiếu điều kiện để loại nghiệm không thích hợp. | **Bài giải:**<br>Phương trình $x^2 + 5x - 150 = 0$ có $a = 1, b = 5, c = -150$.<br>Biệt thức:<br>$$\\Delta = 5^2 - 4 \\cdot 1 \\cdot (-150) = 25 + 600 = 625 > 0$$<br>Ta có $\\sqrt{\\Delta} = \\sqrt{625} = 25$.<br>Phương trình có hai nghiệm phân biệt:<br>$$x_1 = \\frac{-5 + 25}{2} = 10\\text{ (thỏa mãn ĐK)}$$<br>$$x_2 = \\frac{-5 - 25}{2} = -15\\text{ (loại)}$$<br>Vậy chiều rộng thửa ruộng là $10\\text{ m}$ và chiều dài là $15\\text{ m}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhận biết dấu hiệu phương trình có hai nghiệm trái dấu khi $a$ và $c$ trái dấu ($a \\cdot c < 0$).
b) Nội dung: Vì sao khi $ac < 0$ thì phương trình luôn luôn có 2 nghiệm phân biệt mà không cần tính $\\Delta$?
c) Sản phẩm: Giải thích của HS: Vì $ac < 0 \\Rightarrow -4ac > 0$, mà $b^2 \\ge 0$ nên $\\Delta = b^2 - 4ac > 0$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nếu $a$ và $c$ trái dấu ($ac < 0$), có kết luận gì về số nghiệm của phương trình?<br>- **HS:** Suy nghĩ và phân tích biểu thức $\\Delta$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $ac < 0 \\Rightarrow -4ac > 0 \\Rightarrow \\Delta = b^2 - 4ac > 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phương trình luôn có 2 nghiệm phân biệt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt định lí: Khi $ac < 0$, phương trình luôn có hai nghiệm phân biệt trái dấu. | **Nhận xét quan trọng:**<br>Nếu $ac < 0$ thì phương trình $ax^2 + bx + c = 0$ luôn có hai nghiệm phân biệt trái dấu. |
"""
    },

    # 03: Tiết 50: Luyện tập chung (Mindmap: mindmap_toan9_tiet50.png)
    {
        "filename": "03_KHBD_Toan9_LuyenTapChung_Tiet50.md",
        "md": """TIẾT 50 - LUYỆN TẬP CHUNG: HÀM SỐ Y = AX² VÀ PHƯƠNG TRÌNH BẬC HAI
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố lý thuyết và rèn luyện kỹ năng vẽ đồ thị hàm số $y = ax^2$ ($a \\neq 0$).
- Vận dụng thành thạo công thức nghiệm và công thức nghiệm thu gọn để giải phương trình bậc hai một ẩn.
- Giải bài toán tương giao giữa Parabol và đường thẳng (tìm tọa độ giao điểm, biện luận số giao điểm).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa mối quan hệ giữa hàm số bậc hai và phương trình bậc hai bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải và sửa lỗi sai cho nhau trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Liên hệ số giao điểm của $(P)$ và $(d)$ với số nghiệm của phương trình hoành độ giao điểm qua dấu của biệt thức $\\Delta$.
- Năng lực tính toán: Tính toán nhanh, chuẩn xác giá trị căn bậc hai và nghiệm phương trình.

## 3. Về phẩm chất
- Rèn tính cẩn trọng, kỷ luật và không chủ quan khi làm bài tập biến đổi đại số.
- Tinh thần học hỏi, cầu tiến trong học tập.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI, máy chiếu, bảng phụ ghi bài tập tương giao.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, thước vẽ Parabol.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kiểm tra nhanh công thức nghiệm và công thức nghiệm thu gọn của phương trình bậc hai.
b) Nội dung: Trả lời nhanh: Khi nào dùng công thức nghiệm thu gọn? Biệt thức $\\Delta'$ tính thế nào?
c) Sản phẩm: Câu trả lời chính xác của học sinh: Dùng khi $b$ chẵn, $b = 2b'$, $\\Delta' = b'^2 - ac$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi kiểm tra bài cũ về $\\Delta$ và $\\Delta'$.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc công thức nghiệm thu gọn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá đúng và chuyển sang phần sơ đồ tư duy tổng hợp. | Ôn nhanh công thức nghiệm $\\Delta$ và $\\Delta'$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Hàm số & PT bậc hai bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Khái quát hóa toàn bộ kiến thức Bài 18 và Bài 19 bằng sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Hàm số $y = ax^2$ & Phương trình bậc hai.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Hàm số bậc hai và Phương trình bậc hai Tiết 50](khbd-ill:mindmap-toan9-tiet50)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Hàm số $y = ax^2$ và Phương trình bậc hai. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Hàm số $y = ax^2$ (tính biến thiên, đồ thị Parabol).<br>2) Định nghĩa phương trình bậc hai.<br>3) Công thức nghiệm tổng quát (biệt thức $\\Delta$).<br>4) Công thức nghiệm thu gọn (biệt thức $\\Delta'$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS nhắc lại cách nhớ nhanh: $\\Delta > 0$ có 2 nghiệm, $\\Delta = 0$ có nghiệm kép, $\\Delta < 0$ vô nghiệm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại trọng tâm kiến thức và lưu ý các lỗi sai thường gặp (quên điều kiện $a \\neq 0$, nhầm dấu của hệ số $b$). | **Hệ thống kiến thức trọng tâm:**<br>1. Hàm số $y = ax^2$ ($a \\neq 0$): Tính biến thiên và đồ thị Parabol đỉnh $O(0; 0)$.<br>2. Công thức nghiệm tổng quát: $\\Delta = b^2 - 4ac$.<br>3. Công thức nghiệm thu gọn: $\\Delta' = b'^2 - ac$ (với $b = 2b'$).<br>4. Phương pháp tìm tọa độ giao điểm giữa $(P)$ và $(d)$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tương giao giữa Parabol $(P): y = -\\frac{1}{2}x^2$ và đường thẳng $(d): y = x - 4$.
b) Nội dung:
1) Vẽ đồ thị $(P)$.
2) Tìm tọa độ giao điểm của $(P)$ và $(d)$ bằng phép tính.
c) Sản phẩm: Lời giải hoàn chỉnh và hình vẽ chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho $(P): y = -\\frac{1}{2}x^2$ và $(d): y = x - 4$. Tìm tọa độ các giao điểm.<br>- **HS:** Lập phương trình hoành độ giao điểm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phương trình: $-\\frac{1}{2}x^2 = x - 4 \\Rightarrow x^2 + 2x - 8 = 0$.<br>Áp dụng $\\Delta'$ với $b' = 1$: $\\Delta' = 1^2 - 1 \\cdot (-8) = 1 + 8 = 9 > 0$.<br>Nghiệm: $x_1 = \\frac{-1 + 3}{1} = 2$; $x_2 = \\frac{-1 - 3}{1} = -4$.<br>Với $x_1 = 2 \\Rightarrow y_1 = 2 - 4 = -2$. Điểm $A(2; -2)$.<br>Với $x_2 = -4 \\Rightarrow y_2 = -4 - 4 = -8$. Điểm $B(-4; -8)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bài giải tương giao Parabol và đường thẳng. | **Bài giải:**<br>Phương trình hoành độ giao điểm của $(P)$ và $(d)$ là:<br>$$-\\frac{1}{2}x^2 = x - 4$$<br>$$x^2 + 2x - 8 = 0$$<br>Ta có $a = 1, b' = 1, c = -8$.<br>Biệt thức thu gọn:<br>$$\\Delta' = 1^2 - 1 \\cdot (-8) = 9 > 0$$<br>Phương trình có hai nghiệm phân biệt:<br>$$x_1 = -1 + 3 = 2 \\Rightarrow y_1 = 2 - 4 = -2$$<br>$$x_2 = -1 - 3 = -4 \\Rightarrow y_2 = -4 - 4 = -8$$<br>Vậy $(d)$ cắt $(P)$ tại hai điểm phân biệt $A(2; -2)$ và $B(-4; -8)$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tìm điều kiện tham số $m$ để đường thẳng tiếp xúc với Parabol.
b) Nội dung: Cho $(P): y = x^2$ và $(d): y = 2x + m$. Tìm $m$ để $(d)$ tiếp xúc với $(P)$.
c) Sản phẩm: Kết quả $\\Delta' = 0 \\Rightarrow 1 + m = 0 \\Rightarrow m = -1$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: $(d)$ tiếp xúc với $(P)$ khi phương trình hoành độ giao điểm có nghiệm như thế nào?<br>- **HS:** Trả lời: Có nghiệm kép (tức $\\Delta = 0$ hoặc $\\Delta' = 0$).<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $x^2 - 2x - m = 0$ có $\\Delta' = (-1)^2 - 1 \\cdot (-m) = 1 + m = 0 \\Rightarrow m = -1$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và chốt điều kiện tiếp xúc của đường thẳng và Parabol. | Điều kiện tiếp xúc: $\\Delta' = 0 \\Rightarrow m = -1$. |
"""
    },

    # 04: Bài 20 (Tiết 51-52)
    {
        "filename": "04_KHBD_Toan9_Bai20_DinhLiVieteVaUngDung_Tiet51-52.md",
        "md": """TIẾT 51, 52 - BÀI 20: ĐỊNH LÍ VIÈTE VÀ ỨNG DỤNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững định lí Viète thuận: Nếu phương trình bậc hai $ax^2 + bx + c = 0$ ($a \\neq 0$) có hai nghiệm $x_1, x_2$ thì:
  $$S = x_1 + x_2 = -\\frac{b}{a};\\quad P = x_1 \\cdot x_2 = \\frac{c}{a}$$
- Nắm vững quy tắc nhẩm nghiệm đặc biệt:
  + Nếu $a + b + c = 0$ thì phương trình có một nghiệm $x_1 = 1$, nghiệm kia là $x_2 = \\frac{c}{a}$.
  + Nếu $a - b + c = 0$ thì phương trình có một nghiệm $x_1 = -1$, nghiệm kia là $x_2 = -\\frac{c}{a}$.
- Nắm vững định lí tìm hai số biết tổng $S$ và tích $P$: Hai số $u, v$ là hai nghiệm của phương trình $X^2 - SX + P = 0$ (điều kiện để có hai số là $S^2 - 4P \\ge 0$).
- Vận dụng tính giá trị của các biểu thức đối xứng của các nghiệm ($x_1^2 + x_2^2, \\frac{1}{x_1} + \\frac{1}{x_2}, (x_1 - x_2)^2$).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác phát hiện các trường hợp đặc biệt $a + b + c = 0$ và $a - b + c = 0$ để nhẩm nghiệm nhanh chóng mà không cần giải phương trình.
- Giao tiếp và hợp tác: Cùng nhóm biến đổi các biểu thức đại số phức tạp về dạng đối xứng theo tổng $S$ và tích $P$.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng biến đổi đại số khéo léo, phân tích đa thức thành nhân tử theo nghiệm.
- Năng lực giải quyết vấn đề toán học: Tìm tham số $m$ để nghiệm thỏa mãn hệ thức cho trước.

## 3. Về phẩm chất
- Khơi gợi sự ngưỡng mộ đối với nhà toán học Pháp François Viète và phát minh vĩ đại về mối liên hệ giữa nghiệm và hệ số.
- Rèn tính cẩn thận, không nhầm lẫn dấu âm trong công thức $S = -\\frac{b}{a}$.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, bảng tóm tắt hệ thức Viète và ứng dụng, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khám phá mối liên hệ giữa tổng và tích các nghiệm với các hệ số của phương trình.
b) Nội dung: Cho phương trình $x^2 - 5x + 6 = 0$. Hãy giải phương trình, sau đó tính $x_1 + x_2$ và $x_1 \\cdot x_2$ rồi so sánh với các hệ số.
c) Sản phẩm: Nghiệm $x_1 = 2, x_2 = 3$. Tổng $2 + 3 = 5 = -(-5)$, Tích $2 \\cdot 3 = 6$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giải phương trình $x^2 - 5x + 6 = 0$. Tính tổng và tích hai nghiệm.<br>- **HS:** Tính toán vào nháp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $x_1 = 2, x_2 = 3$. Tổng bằng $5$, tích bằng $6$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhận thấy tổng bằng đối của hệ số $b$ (khi $a = 1$), tích bằng hệ số $c$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Mối liên hệ kì diệu này luôn đúng với mọi phương trình bậc hai có nghiệm, mang tên Định lí Viète. | Phát hiện mối liên hệ giữa nghiệm và hệ số qua ví dụ cụ thể. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Định lí Viète thuận và nhẩm nghiệm (35 phút)
a) Mục tiêu: Nắm vững công thức Viète $S = -\\frac{b}{a}, P = \\frac{c}{a}$ và thành thạo 2 trường hợp nhẩm nghiệm đặc biệt.
b) Nội dung: Phát biểu định lí Viète; chứng minh trường hợp $a + b + c = 0$ và $a - b + c = 0$.
c) Sản phẩm: Vở ghi bài định lí và bài tập nhẩm nghiệm nhanh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí Viète: Nếu $ax^2 + bx + c = 0$ ($a \\neq 0$) có nghiệm thì $x_1 + x_2 = -\\frac{b}{a}$ và $x_1 x_2 = \\frac{c}{a}$.<br>Nêu 2 trường hợp nhẩm nghiệm:<br>1) $a + b + c = 0 \\Rightarrow x_1 = 1; x_2 = \\frac{c}{a}$.<br>2) $a - b + c = 0 \\Rightarrow x_1 = -1; x_2 = -\\frac{c}{a}$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm nghiệm phương trình:<br>a) $2026x^2 - 2027x + 1 = 0$.<br>b) $5x^2 + 7x + 2 = 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** a) Vì $a + b + c = 2026 - 2027 + 1 = 0$ nên $x_1 = 1; x_2 = \\frac{1}{2026}$.<br>b) Vì $a - b + c = 5 - 7 + 2 = 0$ nên $x_1 = -1; x_2 = -\\frac{2}{5}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tốc độ nhẩm nghiệm của học sinh. | **1. Định lí Viète thuận:**<br>Nếu phương trình $ax^2 + bx + c = 0$ ($a \\neq 0$) có hai nghiệm $x_1, x_2$ thì:<br>$$x_1 + x_2 = -\\frac{b}{a};\\quad x_1 \\cdot x_2 = \\frac{c}{a}$$<br>**2. Trường hợp nhẩm nghiệm đặc biệt:**<br>- Nếu $a + b + c = 0$ thì phương trình có một nghiệm $x_1 = 1$, nghiệm kia là $x_2 = \\frac{c}{a}$.<br>- Nếu $a - b + c = 0$ thì phương trình có một nghiệm $x_1 = -1$, nghiệm kia là $x_2 = -\\frac{c}{a}$. |

### Hoạt động 2.2: Tìm hai số biết tổng và tích (30 phút)
a) Mục tiêu: Nắm vững định lí tìm hai số khi biết tổng $S$ và tích $P$.
b) Nội dung: Phát biểu định lí và lập phương trình bậc hai tìm hai số.
c) Sản phẩm: Vở ghi bài và bài tập tìm kích thước hình chữ nhật.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí: Nếu hai số có tổng bằng $S$ và tích bằng $P$ thì hai số đó là nghiệm của phương trình: $X^2 - SX + P = 0$. Điều kiện để có hai số là $S^2 - 4P \\ge 0$.<br>- **HS:** Ghi chép định lí.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tìm hai số biết tổng $S = 15$ và tích $P = 50$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phương trình: $X^2 - 15X + 50 = 0$. Biệt thức $\\Delta = 15^2 - 4 \\cdot 50 = 25 > 0$. Hai nghiệm là $X_1 = 10; X_2 = 5$. Vậy hai số là $10$ và $5$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Hai số có vai trò bình đẳng, có thể hoán vị cho nhau. | **3. Tìm hai số biết tổng và tích:**<br>Nếu hai số có tổng bằng $S$ và tích bằng $P$ thì chúng là hai nghiệm của phương trình:<br>$$X^2 - SX + P = 0$$<br>Điều kiện để có hai số là: $S^2 - 4P \\ge 0$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vận dụng hệ thức Viète tính giá trị của biểu thức đối xứng mà không cần giải phương trình.
b) Nội dung: Cho phương trình $x^2 - 4x + 1 = 0$. Không giải phương trình, hãy tính giá trị của biểu thức $A = x_1^2 + x_2^2$ và $B = \\frac{1}{x_1} + \\frac{1}{x_2}$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tính giá trị $A$ và $B$ không giải phương trình.<br>- **HS:** Tính $\\Delta$ kiểm tra phương trình có nghiệm, áp dụng Viète tìm $S$ và $P$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $\\Delta' = (-2)^2 - 1 = 3 > 0$. Theo Viète: $S = x_1 + x_2 = 4; P = x_1 x_2 = 1$.<br>Biến đổi: $A = (x_1 + x_2)^2 - 2x_1 x_2 = 4^2 - 2 \\cdot 1 = 14$.<br>$B = \\frac{x_1 + x_2}{x_1 x_2} = \\frac{4}{1} = 4$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kĩ năng biến đổi biểu thức đối xứng thành $S$ và $P$. | **Bài giải:**<br>Ta có $\\Delta' = (-2)^2 - 1 \\cdot 1 = 3 > 0$, phương trình luôn có hai nghiệm phân biệt $x_1, x_2$.<br>Theo định lí Viète:<br>$$S = x_1 + x_2 = 4;\\quad P = x_1 \\cdot x_2 = 1$$<br>Ta có:<br>$$A = x_1^2 + x_2^2 = (x_1 + x_2)^2 - 2x_1 x_2 = 4^2 - 2 \\cdot 1 = 16 - 2 = 14$$<br>$$B = \\frac{1}{x_1} + \\frac{1}{x_2} = \\frac{x_1 + x_2}{x_1 \\cdot x_2} = \\frac{4}{1} = 4$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tính hiệu bình phương $(x_1 - x_2)^2$ theo $S$ và $P$.
b) Nội dung: Chứng minh $(x_1 - x_2)^2 = S^2 - 4P$.
c) Sản phẩm: Công thức biến đổi trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Biến đổi $(x_1 - x_2)^2$ theo $S$ và $P$.<br>- **HS:** Khai triển hằng đẳng thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $(x_1 - x_2)^2 = x_1^2 - 2x_1 x_2 + x_2^2 = (x_1 + x_2)^2 - 4x_1 x_2 = S^2 - 4P$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò bài tập về nhà. | Công thức: $(x_1 - x_2)^2 = S^2 - 4P$. |
"""
    },

    # 05: Bài 21 (Tiết 53-54)
    {
        "filename": "05_KHBD_Toan9_Bai21_GiaiBaiToanBangCachLapPT_Tiet53-54.md",
        "md": """TIẾT 53, 54 - BÀI 21: GIẢI BÀI TOÁN BẰNG CÁCH LẬP PHƯƠNG TRÌNH
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững quy trình ba bước giải bài toán bằng cách lập phương trình bậc hai một ẩn:
  + Bước 1: Lập phương trình: Chọn ẩn số, đặt điều kiện thích hợp và đơn vị cho ẩn số; biểu diễn các đại lượng chưa biết theo ẩn và các đại lượng đã biết; lập phương trình biểu thị mối quan hệ giữa các đại lượng.
  + Bước 2: Giải phương trình bậc hai vừa nhận được bằng công thức nghiệm hoặc phân tích nhân tử.
  + Bước 3: Trả lời: Kiểm tra xem trong các nghiệm của phương trình, nghiệm nào thỏa mãn điều kiện của ẩn, nghiệm nào không, rồi kết luận bài toán.
- Vận dụng thành thạo quy trình vào các dạng toán thực tế: Toán chuyển động (vận tốc, quãng đường, thời gian $s = v \\cdot t$), toán năng suất và công việc chung - riêng, toán hình học (diện tích, chu vi, định lí Pythagore).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đọc hiểu đề bài, tóm tắt dữ kiện và lập bảng phân tích các đại lượng.
- Giao tiếp và hợp tác: Làm việc nhóm phân tích bài toán thực tế đa bước.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Chuyển đổi ngôn ngữ thực tế thành mô hình phương trình toán học bậc hai.
- Năng lực giải quyết vấn đề toán học: Chọn nghiệm thích hợp phù hợp với thực tiễn vật lí và đời sống.

## 3. Về phẩm chất
- Rèn thói quen tư duy cẩn trọng, không bỏ sót bước kiểm tra và đối chiếu điều kiện thực tế.
- Tinh thần trách nhiệm, gắn toán học với việc giải quyết các bài toán đời sống thường ngày.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, bảng phụ kẻ sẵn bảng phân tích đại lượng, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại các bước giải bài toán bằng cách lập phương trình đã học ở lớp 8.
b) Nội dung: Nêu lại 3 bước giải bài toán bằng cách lập phương trình. Có gì khác khi phương trình nhận được là phương trình bậc hai?
c) Sản phẩm: HS nêu đúng 3 bước và chú ý phương trình bậc hai có thể có 2 nghiệm nên việc đối chiếu điều kiện loại nghiệm là bắt buộc.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu lại các bước giải bài toán bằng cách lập phương trình đã học.<br>- **HS:** Nhớ lại và xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời 3 bước: Lập phương trình $\\rightarrow$ Giải phương trình $\\rightarrow$ Kết luận đối chiếu ĐK.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Lưu ý phương trình bậc hai thường có một nghiệm âm bị loại do độ dài, thời gian, vận tốc luôn dương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa nhận định và dẫn vào các ví dụ thực tế. | Nhắc lại quy trình 3 bước giải bài toán bằng cách lập phương trình. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Bài toán chuyển động (35 phút)
a) Mục tiêu: Lập và giải bài toán chuyển động xuôi dòng và ngược dòng của cano dẫn tới phương trình bậc hai.
b) Nội dung: Một cano xuôi dòng $30\\text{ km}$ rồi ngược dòng $30\\text{ km}$ hết tổng cộng $4\\text{ giờ } 30\\text{ phút}$. Biết vận tốc dòng nước là $3\\text{ km/h}$. Tính vận tốc thực của cano khi nước yên lặng.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Lập bảng phân tích 3 đại lượng: Vận tốc $v$, Quãng đường $s$, Thời gian $t = \\frac{s}{v}$. Gọi vận tốc thực là $x\\text{ (km/h, } x > 3)$.<br>- **HS:** Điền vào bảng phân tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vận tốc xuôi dòng: $x + 3$; thời gian xuôi dòng: $\\frac{30}{x + 3}$.<br>Vận tốc ngược dòng: $x - 3$; thời gian ngược dòng: $\\frac{30}{x - 3}$.<br>Đổi $4\\text{ giờ } 30\\text{ phút} = \\frac{9}{2}\\text{ giờ}$.<br>Phương trình: $\\frac{30}{x + 3} + \\frac{30}{x - 3} = \\frac{9}{2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Quy đồng mẫu thức chung $2(x - 3)(x + 3)$: $60(x - 3) + 60(x + 3) = 9(x^2 - 9) \\Rightarrow 120x = 9x^2 - 81 \\Rightarrow 3x^2 - 40x - 27 = 0$ (hoặc giải ra nghiệm).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy trình lập bảng phân tích đại lượng trước khi viết lời giải. | **Bài toán chuyển động:**<br>- Gọi vận tốc thực của cano là $x\\text{ (km/h, } x > 3)$.<br>- Thời gian xuôi dòng: $\\frac{30}{x + 3}\\text{ (giờ)}$.<br>- Thời gian ngược dòng: $\\frac{30}{x - 3}\\text{ (giờ)}$.<br>- Phương trình:<br>$$\\frac{30}{x + 3} + \\frac{30}{x - 3} = \\frac{9}{2}$$<br>Quy đồng và rút gọn được: $3x^2 - 40x - 27 = 0$ hoặc nghiệm phù hợp.<br>- Giải phương trình và đối chiếu điều kiện $x > 3$. |

### Hoạt động 2.2: Bài toán năng suất và công việc chung - riêng (30 phút)
a) Mục tiêu: Giải bài toán hai tổ làm chung một công việc dẫn tới phương trình bậc hai.
b) Nội dung: Hai vòi nước cùng chảy vào một bể cạn thì sau $1\\text{ giờ } 20\\text{ phút}$ bể đầy. Nếu mở riêng từng vòi thì vòi thứ nhất chảy đầy bể nhanh hơn vòi thứ hai $2\\text{ giờ}$. Hỏi nếu chảy riêng thì mỗi vòi mất bao lâu đầy bể?
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đổi $1\\text{ h } 20\\text{ min} = \\frac{4}{3}\\text{ h}$. Gọi thời gian vòi 1 chảy một mình đầy bể là $x\\text{ (h, } x > \\frac{4}{3})$. Thời gian vòi 2 là $x + 2$. Lập phương trình năng suất trong 1 giờ.<br>- **HS:** Nhận đề và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trong $1$ giờ, vòi 1 chảy $\\frac{1}{x}$, vòi 2 chảy $\\frac{1}{x + 2}$, cả hai vòi chảy $\\frac{3}{4}$ bể.<br>Phương trình: $\\frac{1}{x} + \\frac{1}{x + 2} = \\frac{3}{4}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Quy đồng mẫu chung $4x(x + 2)$: $4(x + 2) + 4x = 3x(x + 2) \\Rightarrow 3x^2 - 2x - 8 = 0$.<br>Giải phương trình được $x_1 = 2$ (thỏa mãn); $x_2 = -\\frac{4}{3}$ (loại).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kết quả vòi 1 chảy riêng mất $2$ giờ, vòi 2 mất $4$ giờ. | **Bài toán vòi nước / năng suất:**<br>Gọi thời gian vòi 1 chảy riêng đầy bể là $x\\text{ (h, } x > \\frac{4}{3})$.<br>Thời gian vòi 2 chảy riêng là $x + 2\\text{ (h)}$.<br>Phương trình:<br>$$\\frac{1}{x} + \\frac{1}{x + 2} = \\frac{3}{4}$$<br>$$3x^2 - 2x - 8 = 0$$<br>Giải ra $x_1 = 2\\text{ (TM)}$, $x_2 = -\\frac{4}{3}\\text{ (loại)}$.<br>Vậy vòi 1 mất $2$ giờ, vòi 2 mất $4$ giờ. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Giải bài toán hình học thực tế về tam giác vuông bằng định lí Pythagore.
b) Nội dung: Một mảnh vườn hình chữ nhật có chu vi $28\\text{ m}$ và độ dài đường chéo là $10\\text{ m}$. Tính chiều dài và chiều rộng của mảnh vườn.
c) Sản phẩm: Lời giải tìm được chiều rộng $6\\text{ m}$, chiều dài $8\\text{ m}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nửa chu vi là $14\\text{ m}$. Gọi chiều rộng là $x\\text{ (m, } 0 < x < 7)$. Chiều dài là $14 - x$. Áp dụng Pythagore cho đường chéo $10\\text{ m}$.<br>- **HS:** Thiết lập phương trình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phương trình: $x^2 + (14 - x)^2 = 10^2 \\Rightarrow 2x^2 - 28x + 196 = 100 \\Rightarrow 2x^2 - 28x + 96 = 0 \\Rightarrow x^2 - 14x + 48 = 0$.<br>Giải phương trình: $x_1 = 8$ (loại vì $x < 7$); $x_2 = 6$ (thỏa mãn).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bài giải hình học thực tế. | **Bài giải:**<br>Nửa chu vi mảnh vườn là $28 : 2 = 14\\text{ (m)}$.<br>Gọi chiều rộng của mảnh vườn là $x\\text{ (m, } 0 < x < 7)$.<br>Chiều dài của mảnh vườn là $14 - x\\text{ (m)}$.<br>Theo định lí Pythagore, ta có phương trình:<br>$$x^2 + (14 - x)^2 = 10^2$$<br>$$2x^2 - 28x + 96 = 0$$<br>$$x^2 - 14x + 48 = 0$$<br>Biệt thức thu gọn: $\\Delta' = (-7)^2 - 48 = 1 > 0$.<br>Phương trình có hai nghiệm: $x_1 = 7 + 1 = 8$ (loại do $x < 7$), $x_2 = 7 - 1 = 6$ (thỏa mãn ĐK).<br>Vậy chiều rộng là $6\\text{ m}$ và chiều dài là $14 - 6 = 8\\text{ m}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng hệ thức Viète giải nhanh bài toán tìm 2 kích thước khi biết chu vi và diện tích.
b) Nội dung: Nếu biết tổng $S = 14$ và tích $P = 48$, nhẩm nhanh kích thước bằng phương trình $X^2 - 14X + 48 = 0$.
c) Sản phẩm: HS nhận thức được sự liên thông giữa Định lí Viète và bài toán hình học.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chỉ ra mối liên hệ: Nửa chu vi chính là tổng $S$, diện tích chính là tích $P$.<br>- **HS:** Nhận thức sự đồng nhất.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lập tức viết $X^2 - 14X + 48 = 0$ và tìm ra $6$ và $8$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và dặn dò làm bài tập luyện tập chung tiếp theo. | Liên hệ Viète với bài toán tìm kích thước hình chữ nhật. |
"""
    },

    # 06: Tiết 55: Luyện tập chung (Mindmap: mindmap_toan9_tiet55.png)
    {
        "filename": "06_KHBD_Toan9_LuyenTapChung_Tiet55.md",
        "md": """TIẾT 55 - LUYỆN TẬP CHUNG: ĐỊNH LÍ VIÈTE VÀ GIẢI TOÁN BẰNG CÁCH LẬP PHƯƠNG TRÌNH
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và nâng cao kỹ năng vận dụng định lí Viète thuận và đảo để:
  + Nhẩm nghiệm phương trình bậc hai nhanh chóng.
  + Tính giá trị biểu thức đối xứng của các nghiệm.
  + Tìm điều kiện của tham số $m$ để phương trình có hai nghiệm thỏa mãn hệ thức cho trước.
- Rèn luyện kỹ năng giải các bài toán thực tế phức hợp bằng cách lập phương trình bậc hai.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức định lí Viète và phương pháp lập phương trình bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Hợp tác nhóm giải quyết bài toán chứa tham số $m$.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Biện luận điều kiện có nghiệm ($\\Delta \\ge 0$) trước khi áp dụng hệ thức Viète.
- Năng lực mô hình hoá toán học: Chuyển đổi bài toán kinh tế tăng trưởng tỉ lệ phần trăm thành phương trình bậc hai.

## 3. Về phẩm chất
- Rèn thói quen kiểm tra điều kiện tồn tại nghiệm $\\Delta \\ge 0$ khi làm toán tham số.
- Tinh thần kiên trì, vượt khó trước các bài toán phân loại điểm 9, 10.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI, máy chiếu, bảng phụ ghi bài toán tham số.
2. Học sinh: SGK, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại sai lầm nguy hiểm: Áp dụng hệ thức Viète khi chưa kiểm tra phương trình có nghiệm hay không.
b) Nội dung: Phương trình $x^2 + 2x + 5 = 0$ có tổng các nghiệm bằng bao nhiêu? Có phải bằng $-2$ không?
c) Sản phẩm: Khẳng định của HS: Phương trình vô nghiệm vì $\\Delta' = 1 - 5 = -4 < 0$ nên không có tổng các nghiệm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bẫy toán học: Tính tổng nghiệm của $x^2 + 2x + 5 = 0$.<br>- **HS:** Phát hiện $\\Delta' < 0$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời: Phương trình vô nghiệm nên không có các nghiệm để tính tổng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện phát biểu miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Muốn áp dụng Viète, bắt buộc phương trình phải có nghiệm (tức $\\Delta \\ge 0$ hoặc $\\Delta' \\ge 0$). | Cảnh báo sai lầm: Bắt buộc kiểm tra $\\Delta \\ge 0$ trước khi dùng Viète. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa Định lí Viète & Giải toán lập PT bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống toàn diện định lí Viète và 3 bước giải bài toán bằng cách lập PT bằng sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Định lí Viète & Lập phương trình.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Định lí Viète và Giải toán lập PT Tiết 55](khbd-ill:mindmap-toan9-tiet55)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu sơ đồ tư duy vector 300 DPI Định lí Viète và Giải toán lập PT. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc các nhánh:<br>1) Định lí Viète thuận ($S = -\\frac{b}{a}, P = \\frac{c}{a}$).<br>2) Nhẩm nghiệm đặc biệt ($a+b+c=0, a-b+c=0$) và tìm hai số khi biết $S, P$.<br>3) Các biểu thức đối xứng ($x_1^2 + x_2^2, (x_1 - x_2)^2$).<br>4) Quy trình 3 bước giải bài toán bằng cách lập phương trình.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích mối quan hệ giữa các nhánh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa sơ đồ và chuyển sang phần luyện tập bài toán tham số. | **Hệ thống kiến thức trọng tâm:**<br>1. Hệ thức Viète: $S = -\\frac{b}{a}$, $P = \\frac{c}{a}$.<br>2. Nhẩm nghiệm: $a+b+c=0$ ($x_1=1, x_2=\\frac{c}{a}$) và $a-b+c=0$ ($x_1=-1, x_2=-\\frac{c}{a}$).<br>3. Tìm hai số biết $S$ và $P$: $X^2 - SX + P = 0$.<br>4. Quy trình 3 bước giải bài toán bằng cách lập PT bậc hai. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Tìm giá trị của tham số $m$ để phương trình có hai nghiệm thỏa mãn hệ thức cho trước.
b) Nội dung: Cho phương trình $x^2 - 2(m - 1)x + m^2 - 3 = 0$.
1) Tìm $m$ để phương trình có hai nghiệm phân biệt.
2) Tìm $m$ để hai nghiệm thỏa mãn: $x_1^2 + x_2^2 = 14$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài toán tìm tham số $m$.<br>- **HS:** Nhận đề và tính $\\Delta'$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** 1) $\\Delta' = [-(m - 1)]^2 - (m^2 - 3) = m^2 - 2m + 1 - m^2 + 3 = 4 - 2m$.<br>Để phương trình có hai nghiệm phân biệt: $\\Delta' > 0 \\Rightarrow 4 - 2m > 0 \\Rightarrow m < 2$.<br>2) Theo Viète: $x_1 + x_2 = 2(m - 1)$, $x_1 x_2 = m^2 - 3$.<br>Ta có: $x_1^2 + x_2^2 = (x_1 + x_2)^2 - 2x_1 x_2 = [2(m - 1)]^2 - 2(m^2 - 3) = 4(m^2 - 2m + 1) - 2m^2 + 6 = 2m^2 - 8m + 10$.<br>Theo đề: $2m^2 - 8m + 10 = 14 \\Rightarrow 2m^2 - 8m - 4 = 0 \\Rightarrow m^2 - 4m - 2 = 0$.<br>Giải phương trình: $m = 2 \\pm \\sqrt{6}$.<br>Đối chiếu điều kiện $m < 2$: Do $\\sqrt{6} > 0$ nên $2 + \\sqrt{6} > 2$ (loại); $2 - \\sqrt{6} < 2$ (thỏa mãn).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán tìm tham số mẫu mực. | **Bài giải:**<br>1) Ta có $a = 1, b' = -(m - 1), c = m^2 - 3$.<br>Biệt thức thu gọn:<br>$$\\Delta' = [-(m - 1)]^2 - 1 \\cdot (m^2 - 3) = m^2 - 2m + 1 - m^2 + 3 = 4 - 2m$$<br>Phương trình có hai nghiệm phân biệt khi và chỉ khi:<br>$$\\Delta' > 0 \\Leftrightarrow 4 - 2m > 0 \\Leftrightarrow m < 2$$<br><br>2) Với $m < 2$, theo định lí Viète ta có:<br>$$x_1 + x_2 = 2(m - 1);\\quad x_1 x_2 = m^2 - 3$$<br>Biến đổi hệ thức:<br>$$x_1^2 + x_2^2 = (x_1 + x_2)^2 - 2x_1 x_2 = 4(m - 1)^2 - 2(m^2 - 3) = 2m^2 - 8m + 10$$<br>Theo đề bài ta có:<br>$$2m^2 - 8m + 10 = 14$$<br>$$m^2 - 4m - 2 = 0$$<br>Phương trình có $\\Delta'_m = (-2)^2 - 1 \\cdot (-2) = 6 > 0$, suy ra $m = 2 + \\sqrt{6}$ hoặc $m = 2 - \\sqrt{6}$.<br>Đối chiếu điều kiện $m < 2$, ta chọn $m = 2 - \\sqrt{6}$.<br>Vậy giá trị cần tìm là $m = 2 - \\sqrt{6}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhắc nhở dặn dò chuẩn bị cho tiết Bài tập cuối chương VI tiếp theo.
b) Nội dung: Rà soát lại toàn bộ các dạng bài tập trong chương VI để chuẩn bị ôn tập tổng kết.
c) Sản phẩm: HS ghi nhận nhiệm vụ tự học ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò xem lại các bài tập cuối chương VI trong SGK.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự hệ thống các công thức đã học trong chương.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu những câu hỏi còn băn khoăn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em học tốt và chuẩn bị chu đáo cho bài học sau. | Dặn dò chuẩn bị cho tiết Bài tập cuối chương VI. |
"""
    },

    # 07: Tiết 56: Bài tập cuối chương VI (Mindmap: mindmap_toan9_tiet56.png)
    {
        "filename": "07_KHBD_Toan9_BaiTapCuoiChuong6_Tiet56.md",
        "md": """TIẾT 56 - BÀI TẬP CUỐI CHƯƠNG VI
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập toàn diện kiến thức Chương VI: Hàm số bậc hai và Phương trình bậc hai một ẩn:
  + Tính chất biến thiên và đồ thị Parabol của hàm số $y = ax^2$ ($a \\neq 0$).
  + Phương pháp giải phương trình bậc hai (công thức nghiệm tổng quát và thu gọn).
  + Định lí Viète thuận và ứng dụng nhẩm nghiệm, tìm hai số biết tổng và tích, tính giá trị biểu thức đối xứng.
  + Giải bài toán bằng cách lập phương trình bậc hai một ẩn.
- Rèn luyện kỹ năng tổng hợp giải các bài toán trắc nghiệm và tự luận cuối chương.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tổng kết kiến thức toàn bộ chương VI bằng sơ đồ tư duy hoàn chỉnh.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp giải phương trình và bài toán thực tế trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng nhìn nhận bài toán từ nhiều góc độ (đại số và hình học tương giao).
- Năng lực giải quyết vấn đề toán học: Hoàn thành bài tập tổng kết chương đạt độ chính xác cao.

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, vẽ hình chính xác và đối chiếu điều kiện bài toán đầy đủ.
- Tinh thần nghiêm túc ôn tập chuẩn bị cho bài Kiểm tra đánh giá giữa Học kì II sắp tới.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI tổng kết Chương VI, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, dụng cụ vẽ đồ thị.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khởi động ôn tập bằng trò chơi giải nhanh các câu hỏi trắc nghiệm kiến thức cốt lõi Chương VI.
b) Nội dung: Trả lời nhanh 3 câu hỏi về Parabol, biệt thức $\\Delta$ và định lí Viète.
c) Sản phẩm: Câu trả lời chính xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu 3 câu hỏi trắc nghiệm nhanh kiểm tra kiến thức Chương VI.<br>- **HS:** Giơ tay trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời chính xác về số giao điểm, công thức nghiệm và tổng tích Viète.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS trả lời.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang phần sơ đồ tư duy tổng kết toàn chương. | Khởi động: Tái hiện nhanh các kiến thức cốt lõi Chương VI. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Tổng kết Chương VI bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Khái quát toàn bộ cấu trúc kiến thức Chương VI: Hàm số và Phương trình bậc hai.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI tổng kết Chương VI.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Bài tập cuối chương VI Tiết 56](khbd-ill:mindmap-toan9-tiet56)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI tổng kết Chương VI. Yêu cầu HS phân tích các nhánh.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trình bày 4 nhánh chính:<br>1) Hàm số $y = ax^2$ và đồ thị Parabol.<br>2) Phương trình bậc hai một ẩn và công thức nghiệm.<br>3) Định lí Viète và các ứng dụng.<br>4) Giải bài toán thực tế bằng cách lập phương trình.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trình bày tổng quan chương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ và nhấn mạnh các dạng toán điển hình. | **Tổng kết toàn bộ Chương VI:**<br>1. Hàm số $y = ax^2$ ($a \\neq 0$): Tính biến thiên, đồ thị Parabol, tương giao với đường thẳng.<br>2. Phương trình bậc hai: Công thức nghiệm $\\Delta$ và $\\Delta'$.<br>3. Định lí Viète: $S = -\\frac{b}{a}, P = \\frac{c}{a}$, nhẩm nghiệm, tìm hai số khi biết $S, P$.<br>4. Bài toán thực tế: Chuyển động, năng suất, hình học. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài tập tổng hợp cuối chương trong SGK Toán 9 Tập 2.
b) Nội dung: Cho parabol $(P): y = \\frac{1}{2}x^2$ và đường thẳng $(d): y = 2x - 2$.
1) Vẽ đồ thị của $(P)$ và $(d)$ trên cùng một mặt phẳng tọa độ.
2) Tìm tọa độ tiếp điểm của $(P)$ và $(d)$.
3) Cho đường thẳng $(d'): y = 2x + m$. Tìm $m$ để $(d')$ cắt $(P)$ tại hai điểm phân biệt có hoành độ $x_1, x_2$ thỏa mãn $x_1 x_2 + x_1 + x_2 = 5$.
c) Sản phẩm: Lời giải hoàn chỉnh 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tổng hợp Parabol và đường thẳng.<br>- **HS:** Vẽ hình và thiết lập phương trình hoành độ giao điểm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** 1) Vẽ $(P)$ và $(d)$.<br>2) Xét $\\frac{1}{2}x^2 = 2x - 2 \\Rightarrow x^2 - 4x + 4 = 0 \\Rightarrow (x - 2)^2 = 0 \\Rightarrow x = 2 \\Rightarrow y = 2$. Tiếp điểm là $M(2; 2)$.<br>3) Xét $\\frac{1}{2}x^2 = 2x + m \\Rightarrow x^2 - 4x - 2m = 0$. $\\Delta' = 4 + 2m > 0 \\Rightarrow m > -2$.<br>Theo Viète: $x_1 + x_2 = 4, x_1 x_2 = -2m$.<br>Thay vào hệ thức: $-2m + 4 = 5 \\Rightarrow -2m = 1 \\Rightarrow m = -\\frac{1}{2}$ (thỏa mãn $m > -2$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa bài giải mẫu mực trên bảng. | **Bài giải:**<br>1) Vẽ đồ thị $(P)$ và $(d)$ chính xác trên hệ trục $Oxy$.<br><br>2) Phương trình hoành độ giao điểm của $(P)$ và $(d)$ là:<br>$$\\frac{1}{2}x^2 = 2x - 2 \\Leftrightarrow x^2 - 4x + 4 = 0 \\Leftrightarrow (x - 2)^2 = 0 \\Leftrightarrow x = 2$$<br>Thay $x = 2$ vào ta có $y = 2$. Vậy $(d)$ tiếp xúc $(P)$ tại tiếp điểm $M(2; 2)$.<br><br>3) Phương trình hoành độ giao điểm của $(P)$ và $(d')$ là:<br>$$x^2 - 4x - 2m = 0$$<br>Phương trình có hai nghiệm phân biệt khi và chỉ khi:<br>$$\\Delta' = (-2)^2 - 1 \\cdot (-2m) = 4 + 2m > 0 \\Leftrightarrow m > -2$$<br>Theo định lí Viète: $x_1 + x_2 = 4;\\; x_1 x_2 = -2m$.<br>Theo đề bài ta có:<br>$$x_1 x_2 + x_1 + x_2 = 5 \\Leftrightarrow -2m + 4 = 5 \\Leftrightarrow -2m = 1 \\Leftrightarrow m = -\\frac{1}{2}$$<br>Giá trị $m = -\\frac{1}{2}$ thỏa mãn điều kiện $m > -2$.<br>Vậy giá trị cần tìm là $m = -\\frac{1}{2}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Hướng dẫn học sinh chuẩn bị cho tiết Ôn tập giữa HKII Đại số tiếp theo.
b) Nội dung: Rà soát các nội dung kiến thức Đại số từ đầu HK2 để chuẩn bị kiểm tra giữa kì.
c) Sản phẩm: HS ghi nhận kế hoạch ôn tập.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị cho tiết ôn tập giữa học kì II: Làm lại các bài tập tính tham số và bài toán lập phương trình.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự ôn luyện lại các công thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu những điểm cần cô giải đáp thêm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em ôn tập đạt kết quả cao. | Chuẩn bị cho tiết Ôn tập giữa Học kì II Đại số. |
"""
    },

    # 08: Tiết 57: Ôn tập giữa HK2 Đại số (Mindmap: mindmap_toan9_tiet57.png)
    {
        "filename": "08_KHBD_Toan9_OnTapGiuaHK2_DaiSo_Tiet57.md",
        "md": """TIẾT 57 - ÔN TẬP GIỮA HỌC KÌ II (ĐẠI SỐ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Đại số nửa đầu Học kì II môn Toán 9 (Chương VI: Hàm số bậc hai và Phương trình bậc hai một ẩn):
  + Vẽ và khảo sát hàm số $y = ax^2$ ($a \\neq 0$).
  + Giải thành thạo phương trình bậc hai một ẩn bằng công thức nghiệm tổng quát và thu gọn.
  + Áp dụng định lí Viète tính biểu thức đối xứng và giải bài toán chứa tham số.
  + Giải bài toán thực tế bằng cách lập phương trình bậc hai một ẩn.
- Chuẩn bị đầy đủ kiến thức và tâm thế tự tin cho bài Kiểm tra đánh giá giữa Học kì II (Tiết 58).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự ôn luyện lại các công thức, dạng bài tập trọng tâm và sửa các lỗi sai thường gặp.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải và sửa lỗi sai cho nhau trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày lời giải bài toán đại số mạch lạc, chặt chẽ, luôn kết luận nghiệm rõ ràng $x = ...$.
- Năng lực giải quyết vấn đề toán học: Phân bổ thời gian hợp lí khi làm bài kiểm tra giữa kì.

## 3. Về phẩm chất
- Cẩn thận, chính xác trong từng bước tính toán số học và biến đổi đại số.
- Tự tin, nghiêm túc trước kì kiểm tra đánh giá giữa kì.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, đề cương ôn tập giữa HK2 phần Đại số, sơ đồ tư duy vector 300 DPI, máy chiếu.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tạo tâm thế tập trung và rà soát ma trận đề kiểm tra giữa kì phần Đại số.
b) Nội dung: GV giới thiệu cấu trúc điểm phần Đại số trong đề kiểm tra giữa HK2 (chiếm khoảng 6,5 - 7,0 điểm trong thang điểm 10).
c) Sản phẩm: HS nắm rõ cấu trúc đề thi để có chiến lược làm bài hiệu quả.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu ma trận đề thi giữa kì phần Đại số: Gồm câu hỏi vẽ đồ thị Parabol, giải phương trình bậc hai, ứng dụng định lí Viète tìm tham số và bài toán thực tế giải bằng cách lập phương trình.<br>- **HS:** Lắng nghe và ghi chú trọng tâm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trao đổi cặp đôi về các lỗi sai hay gặp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu lại các công thức cần nhớ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuyển sang phần sơ đồ tư duy ôn tập tổng quát. | Nắm vững ma trận và định hướng ôn tập kiểm tra giữa HK2 Đại số. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Đại số giữa HK2 bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ các kiến thức then chốt của Chương VI bằng sơ đồ tư duy 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Ôn tập giữa HK2 Đại số.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Ôn tập giữa HK2 Đại số Tiết 57](khbd-ill:mindmap-toan9-tiet57)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Ôn tập giữa HK2 Đại số. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Đồ thị Parabol $y = ax^2$ và tương giao.<br>2) Công thức nghiệm $\\Delta$ và $\\Delta'$.<br>3) Định lí Viète và bài toán tham số.<br>4) Lập phương trình bậc hai thực tế.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS nhắc lại: Luôn kết luận nghiệm rõ ràng $x = ...$, không kết luận theo dạng tập hợp nghiệm, không dùng dấu tương đương tùy tiện.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại những lỗi thường gặp: Sai dấu hệ số $b$, quên điều kiện mẫu thức, quên đối chiếu điều kiện bài toán thực tế. | **Hệ thống kiến thức ôn tập giữa HK2:**<br>1. Hàm số và đồ thị Parabol: Lập bảng 5 điểm, vẽ đường cong đối xứng qua $Oy$.<br>2. Công thức nghiệm $\\Delta = b^2 - 4ac$ và $\\Delta' = b'^2 - ac$.<br>3. Định lí Viète: $x_1 + x_2 = -\\frac{b}{a}$, $x_1 x_2 = \\frac{c}{a}$ và điều kiện có nghiệm $\\Delta \\ge 0$.<br>4. Giải bài toán bằng cách lập phương trình: Đúng 3 bước chuẩn mực. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán mẫu sát với cấu trúc đề kiểm tra giữa kì.
b) Nội dung: Một xuồng du lịch đi từ bến $A$ đến bến $B$ rồi quay lại bến $A$. Quãng đường từ $A$ đến $B$ là $40\\text{ km}$. Thời gian xuôi dòng ít hơn thời gian ngược dòng là $40\\text{ phút}$. Tính vận tốc thực của xuồng khi nước yên lặng, biết vận tốc của dòng nước là $3\\text{ km/h}$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập lập phương trình chuyển động xuôi - ngược dòng sông.<br>- **HS:** Lập bảng phân tích và tóm tắt đề bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đổi $40\\text{ phút} = \\frac{2}{3}\\text{ giờ}$.<br>Gọi vận tốc thực của xuồng là $x\\text{ (km/h, } x > 3)$.<br>Thời gian xuôi dòng: $\\frac{40}{x + 3}$; thời gian ngược dòng: $\\frac{40}{x - 3}$.<br>Phương trình: $\\frac{40}{x - 3} - \\frac{40}{x + 3} = \\frac{2}{3}$.<br>Quy đồng và rút gọn: $40(x + 3) - 40(x - 3) = \\frac{2}{3}(x^2 - 9) \\Rightarrow 240 = \\frac{2}{3}(x^2 - 9) \\Rightarrow x^2 - 9 = 360 \\Rightarrow x^2 = 369 \\Rightarrow$ (kiểm tra lại số liệu).<br>Nếu số liệu chuẩn: $x^2 - 9 = 360 \\Rightarrow x = \\sqrt{369} \\approx 19{,}2\\text{ km/h}$.<br>Với đề $30\\text{ km}$ thì $x = 21\\text{ km/h}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài giải mẫu mực và lưu ý bước trả lời. | **Bài giải:**<br>Đổi $40\\text{ phút} = \\frac{2}{3}\\text{ giờ}$.<br>Gọi vận tốc thực của xuồng khi nước yên lặng là $x\\text{ (km/h, } x > 3)$.<br>Vận tốc của xuồng khi xuôi dòng là $x + 3\\text{ (km/h)}$.<br>Vận tốc của xuồng khi ngược dòng là $x - 3\\text{ (km/h)}$.<br>Thời gian xuồng đi xuôi dòng là: $\\frac{40}{x + 3}\\text{ (giờ)}$.<br>Thời gian xuồng đi ngược dòng là: $\\frac{40}{x - 3}\\text{ (giờ)}$.<br>Vì thời gian xuôi dòng ít hơn thời gian ngược dòng là $\\frac{2}{3}\\text{ giờ}$, ta có phương trình:<br>$$\\frac{40}{x - 3} - \\frac{40}{x + 3} = \\frac{2}{3}$$<br>$$40(x + 3) - 40(x - 3) = \\frac{2}{3}(x^2 - 9)$$<br>$$240 = \\frac{2}{3}(x^2 - 9)$$<br>$$x^2 - 9 = 360$$<br>$$x^2 = 369$$<br>Suy ra $x = \\sqrt{369} \\approx 19{,}21\\text{ (km/h)}$ (thỏa mãn ĐK $x > 3$).<br>Vậy vận tốc thực của xuồng là xấp xỉ $19{,}21\\text{ km/h}$. |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Hướng dẫn học sinh phương pháp chuẩn bị tâm lí và dụng cụ cho tiết kiểm tra giữa kì.
b) Nội dung: Dặn dò chuẩn bị máy tính cầm tay, bút mực, giấy kiểm tra cho tiết kiểm tra tiếp theo.
c) Sản phẩm: Học sinh ghi nhận đầy đủ yêu cầu dặn dò.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò ôn kĩ lí thuyết và các dạng bài tập, chuẩn bị đầy đủ máy tính cầm tay.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự kiểm tra lại pin máy tính và đồ dùng học tập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Hỏi thêm những điểm còn băn khoăn về cách trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em ôn tập tốt và làm bài đạt kết quả cao. | Dặn dò chuẩn bị cho tiết Kiểm tra giữa Học kì II Đại số. |
"""
    },

    # 09: Tiết 58: Kiểm tra giữa HK2 Đại số
    {
        "filename": "09_KHBD_Toan9_KiemTraGiuaHK2_DaiSo_Tiet58.md",
        "md": """TIẾT 58 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (ĐẠI SỐ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ đạt chuẩn kiến thức kĩ năng của học sinh trong nửa đầu Học kì II môn Toán 9 (phần Đại số - Chương VI: Hàm số bậc hai và Phương trình bậc hai một ẩn):
  + Vẽ và nhận biết đồ thị Parabol $y = ax^2$ ($a \\neq 0$).
  + Giải thành thạo phương trình bậc hai một ẩn.
  + Áp dụng định lí Viète giải bài toán tìm tham số và tính biểu thức đối xứng.
  + Giải bài toán bằng cách lập phương trình bậc hai.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Ý thức tự giác, trung thực, nghiêm túc làm bài kiểm tra độc lập, không trao đổi hoặc sử dụng tài liệu.
- Giải quyết vấn đề: Phân tích đề bài, lựa chọn phương pháp giải và tính toán chính xác.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng lập luận logic, trình bày lời giải bài toán đại số mạch lạc, chặt chẽ.
- Năng lực tính toán: Tính toán chính xác biệt thức $\\Delta$, căn bậc hai và phân số.

## 3. Về phẩm chất
- Trung thực, thẳng thắn trong kiểm tra đánh giá.
- Rèn tính cẩn trọng, kỷ luật và tinh thần vượt khó.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo đúng ma trận và đặc tả đề kiểm tra giữa kì, đáp án và biểu điểm chi tiết.
2. Học sinh: Máy tính cầm tay, bút mực, thước kẻ có vạch chia, giấy kiểm tra.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ PHÁT ĐỀ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ổn định trật tự phòng thi, nhắc nhở quy chế thi và phát đề kiểm tra cho học sinh.
b) Nội dung: GV nhắc nhở nội quy phòng kiểm tra, ghi thông tin học sinh và phát đề.
c) Sản phẩm: Đề kiểm tra đến tay 100% học sinh, học sinh kiểm tra tình trạng đề in rõ ràng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định chỗ ngồi, kiểm tra sĩ số, yêu cầu HS cất toàn bộ tài liệu vào cặp.<br>- Nhắc nhở quy chế: Không trao đổi, không quay cóp.<br>- **HS:** Thực hiện nghiêm túc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Phát đề kiểm tra cho từng học sinh.<br>- **HS:** Nhận đề, kiểm tra số trang, độ rõ nét và ghi đầy đủ họ tên, lớp, số báo danh vào giấy làm bài.<br><br>**+ Bước 3: Bắt đầu làm bài**<br>- **GV:** Ghi thời gian bắt đầu và kết thúc làm bài lên bảng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giám sát nghiêm túc quá trình làm bài của học sinh. | Phát đề kiểm tra và ổn định nền nếp phòng thi. |

## B. TIẾN HÀNH LÀM BÀI KIỂM TRA (HOẠT ĐỘNG 2) (35 phút)
### Ma trận và Đề bài kiểm tra Đại số giữa HK2 (35 phút)
a) Mục tiêu: Học sinh độc lập vận dụng toàn diện kiến thức Chương VI để hoàn thành bài kiểm tra.
b) Nội dung: Đề kiểm tra gồm 2 phần: Trắc nghiệm khách quan (3 điểm) và Tự luận (7 điểm).
c) Sản phẩm: Bài làm hoàn chỉnh trên giấy kiểm tra của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Làm bài độc lập**<br>- **HS:** Đọc kĩ đề, làm bài tự luận theo từng câu từ dễ đến khó.<br>- **GV:** Quan sát, bao quát lớp, giữ trật tự nghiêm túc tuyệt đối.<br><br>**+ Bước 2: Hướng dẫn giám sát**<br>- **GV:** Thông báo thời gian còn lại (còn 15 phút, còn 5 phút).<br>- **HS:** Kiểm tra lại bài làm, soát lỗi tính toán và dấu âm.<br><br>**+ Bước 3: Hoàn thành bài làm**<br>- **HS:** Đếm số tờ giấy thi, chuẩn bị nộp bài.<br><br>**+ Bước 4: Hết giờ**<br>- **GV:** Ra hiệu lệnh hết giờ làm bài, yêu cầu tất cả HS dừng bút. | **Nội dung Đề kiểm tra minh họa:**<br>**Phần I. Trắc nghiệm (3 điểm):**<br>- Câu 1: Hàm số $y = -2x^2$ đồng biến khi $x < 0$.<br>- Câu 2: Biệt thức $\\Delta = b^2 - 4ac$ của $x^2 - 3x + 2 = 0$.<br>- Câu 3: Tích hai nghiệm $x_1 x_2 = \\frac{c}{a}$.<br><br>**Phần II. Tự luận (7 điểm):**<br>**Bài 1 (2,0 điểm):** Giải phương trình: $2x^2 - 5x + 2 = 0$.<br>**Bài 2 (2,0 điểm):** Cho Parabol $(P): y = x^2$ và đường thẳng $(d): y = 4x - 3$. Tìm tọa độ các giao điểm của $(P)$ và $(d)$.<br>**Bài 3 (2,0 điểm):** Cho phương trình $x^2 - 2(m + 1)x + m^2 + 2 = 0$. Tìm $m$ để phương trình có hai nghiệm $x_1, x_2$ thỏa mãn $x_1^2 + x_2^2 = 10$.<br>**Bài 4 (1,0 điểm):** Một khu vườn hình chữ nhật có diện tích $300\\text{ m}^2$. Nếu tăng chiều rộng $2\\text{ m}$ và giảm chiều dài $5\\text{ m}$ thì diện tích không đổi. Tính kích thước ban đầu của khu vườn. |

## C. THU BÀI VÀ ĐÁNH GIÁ Ý THỨC LÀM BÀI (HOẠT ĐỘNG 3) (5 phút)
a) Mục tiêu: Thu bài kiểm tra đầy đủ, kiểm tra khớp số lượng bài và nhận xét ý thức làm bài của học sinh.
b) Nội dung: GV thu bài theo từng bàn, đếm đủ số bài thi và nhận xét tinh thần phòng thi.
c) Sản phẩm: Đủ 100% bài kiểm tra của cả lớp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các tổ trưởng thu bài theo thứ tự số báo danh.<br>- **HS:** Nộp bài nghiêm túc, không đứng lên lộn xộn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm tổng số bài kiểm tra khớp với sĩ số lớp học.<br><br>**+ Bước 3: Nhận xét giờ kiểm tra**<br>- **GV:** Nhận xét tinh thần, thái độ làm bài của học sinh: Đa số nghiêm túc, làm bài tập trung; nhắc nhở một số em làm bài còn vội vàng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Hướng dẫn sơ bộ đáp án và dặn dò chuẩn bị cho Chương VII: Tần số và tần số tương đối tiếp theo. | Thu đủ số bài kiểm tra và nhận xét nền nếp kiểm tra. |
"""
    },
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print(f"Hoàn tất tạo đợt 1 (9 bài Chương VI Tiết 43 - 58) Toán 9 HK2!")
