# -*- coding: utf-8 -*-
"""
Script sinh 18 KHBD Chương IX: Tam giác đồng dạng & Chương X: Một số hình khối trong thực tiễn (Tiết 32 - 57) - Toán 8 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan8"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    # 28: Bài 33
    {
        "filename": "28_KHBD_Toan8_Bai33_HaiTamGiacDongDang_Tiet32-33.md",
        "md": """TIẾT 32, 33 - BÀI 33: HAI TAM GIÁC ĐỒNG DẠNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa hai tam giác đồng dạng: $\\Delta ABC \\backsim \\Delta A'B'C'$ nếu $\\widehat{A} = \\widehat{A'}, \\widehat{B} = \\widehat{B'}, \\widehat{C} = \\widehat{C'}$ và $\\frac{AB}{A'B'} = \\frac{BC}{B'C'} = \\frac{CA}{C'A'} = k$ (với $k$ là tỉ số đồng dạng).
- Nắm vững các tính chất cơ bản của tam giác đồng dạng (tính phản xạ, đối xứng, bắc cầu).
- Hiểu và vận dụng định lí: Nếu một đường thẳng cắt hai cạnh của một tam giác và song song với cạnh còn lại thì nó tạo thành một tam giác mới đồng dạng với tam giác đã cho.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ hình, đo đạc tỉ số độ dài các cạnh và so sánh các góc tương ứng.
- Giao tiếp và hợp tác: Làm việc nhóm thiết lập các tỉ lệ thức cạnh tương ứng của hai tam giác đồng dạng.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Suy luận mối quan hệ giữa định lí Thalès và định lí tạo thành tam giác đồng dạng.
- Năng lực giải quyết vấn đề toán học: Vận dụng tỉ số đồng dạng để tính độ dài cạnh chưa biết trong hình học.

c) Năng lực số (NLS):
- ***3.1.TC2a: HS tạo nội dung số vẽ tam giác đồng dạng và đo tỉ số trên máy; 5.3.TC2a: HS sử dụng công cụ số tạo tri thức về tính chất tam giác đồng dạng; 1.1.TC2c: HS mô tả cách truy cập và tìm hình ảnh đồng dạng trong thực tế.***

## 3. Về phẩm chất
- Cẩn thận, chính xác khi ghi kí hiệu các đỉnh tương ứng của hai tam giác đồng dạng.
- Tinh thần trách nhiệm, hăng hái tham gia xây dựng bài học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, thước kẻ, compa, máy tính, bảng phụ hoặc bài trình chiếu.
2. Học sinh: SGK Toán 8 Tập 2, thước thẳng có vạch chia, thước đo góc, compa, vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích thích sự tò mò về hình ảnh các hình có hình dạng giống nhau nhưng kích thước khác nhau trong thực tế (phóng to, thu nhỏ).
b) Nội dung: Quan sát bức ảnh chụp một công trình kiến trúc và mô hình thu nhỏ của nó, nhận xét về hình dạng và kích thước của các tam giác tương ứng.
c) Sản phẩm: Câu trả lời của HS: Hình dạng giống hệt nhau nhưng kích thước khác nhau.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh mô hình tháp Eiffel thu nhỏ đặt cạnh tháp Eiffel thật. Yêu cầu HS nhận xét về góc nghiêng và tỉ lệ các kích thước.<br>- **HS:** Quan sát và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo cặp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 1 HS phát biểu: Hình dáng giống nhau, các góc bằng nhau nhưng độ dài cạnh bị thu nhỏ theo cùng tỉ lệ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Trong toán học, hai hình có hình dạng như vậy được gọi là hai hình đồng dạng. Bài học hôm nay ta nghiên cứu về hai tam giác đồng dạng. | Quan sát thực tế: Hai hình có cùng hình dạng nhưng kích thước khác nhau gọi là hình đồng dạng. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Định nghĩa hai tam giác đồng dạng (35 phút)
a) Mục tiêu: Nắm vững định nghĩa hai tam giác đồng dạng, kí hiệu và khái niệm tỉ số đồng dạng.
b) Nội dung: Khám phá các góc tương ứng bằng nhau và các cạnh tương ứng tỉ lệ; định nghĩa tam giác đồng dạng.
c) Sản phẩm: Vở ghi bài định nghĩa, kí hiệu và tỉ số đồng dạng $k$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Tam giác $A'B'C'$ gọi là đồng dạng với tam giác $ABC$ nếu:<br>$$\\widehat{A'} = \\widehat{A},\\; \\widehat{B'} = \\widehat{B},\\; \\widehat{C'} = \\widehat{C}$$<br>và:<br>$$\\frac{A'B'}{AB} = \\frac{B'C'}{BC} = \\frac{C'A'}{CA} = k$$<br>- **GV:** Giới thiệu kí hiệu $\\backsim$ và tỉ số đồng dạng $k$.<br>- **HS:** Chú ý thứ tự viết các đỉnh tương ứng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết các cặp cạnh tương ứng tỉ lệ khi $\\Delta MNP \\backsim \\Delta DEF$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $\\frac{MN}{DE} = \\frac{NP}{EF} = \\frac{MP}{DF}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh tính thứ tự của các đỉnh khi viết kí hiệu đồng dạng. | **1. Định nghĩa:**<br>- $\\Delta A'B'C' \\backsim \\Delta ABC$ nếu:<br>$\\begin{cases} \\widehat{A'} = \\widehat{A},\\; \\widehat{B'} = \\widehat{B},\\; \\widehat{C'} = \\widehat{C} \\\\ \\frac{A'B'}{AB} = \\frac{B'C'}{BC} = \\frac{C'A'}{CA} = k \\end{cases}$<br>- $k$ là tỉ số đồng dạng của $\\Delta A'B'C'$ đối với $\\Delta ABC$.<br>- Tính chất: Tự phản xạ, đối xứng (tỉ số nghịch đảo $\\frac{1}{k}$), bắc cầu. |

### Hoạt động 2.2: Định lí về tạo thành tam giác đồng dạng (30 phút)
a) Mục tiêu: Nắm vững định lí đường thẳng song song với một cạnh của tam giác và cắt hai cạnh còn lại tạo thành tam giác mới đồng dạng với tam giác đã cho.
b) Nội dung: Chứng minh và áp dụng định lí vào tính toán cạnh.
c) Sản phẩm: Lời giải bài tập áp dụng định lí trong vở ghi.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát biểu định lí: Nếu một đường thẳng cắt hai cạnh $AB, AC$ của $\\Delta ABC$ lần lượt tại $M, N$ và song song với $BC$ thì $\\Delta AMN \\backsim \\Delta ABC$.<br>- **HS:** Vẽ hình và ghi giả thiết, kết luận.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng định lí Thalès và tính chất góc đồng vị để giải thích định lí.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Vì $MN \\parallel BC$ nên $\\widehat{AMN} = \\widehat{B}$, $\\widehat{ANM} = \\widehat{C}$, $\\widehat{A}$ chung; các cạnh tỉ lệ theo hệ quả định lí Thalès.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Định lí cũng đúng trong trường hợp đường thẳng cắt phần kéo dài của hai cạnh tam giác. | **2. Định lí:**<br>Cho $\\Delta ABC$, đường thẳng $d \\parallel BC$ cắt $AB, AC$ lần lượt tại $M, N$.<br>Khi đó $\\Delta AMN \\backsim \\Delta ABC$.<br>*Chú ý:* Định lí vẫn đúng khi $d$ cắt phần kéo dài của các cạnh $AB, AC$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vận dụng định lí và định nghĩa tam giác đồng dạng để tính độ dài đoạn thẳng.
b) Nội dung: Cho $\\Delta ABC$ có $AB = 6\\text{ cm}, AC = 8\\text{ cm}, BC = 10\\text{ cm}$. Đường thẳng song song với $BC$ cắt $AB$ tại $M$ với $AM = 2\\text{ cm}$ và cắt $AC$ tại $N$. Tính $AN$ và $MN$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho bài toán tính $AN, MN$ với số liệu trên.<br>- **HS:** Vẽ hình và tìm tỉ số đồng dạng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Do $MN \\parallel BC$ nên $\\Delta AMN \\backsim \\Delta ABC$. Tỉ số $k = \\frac{AM}{AB} = \\frac{2}{6} = \\frac{1}{3}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt phương pháp tính cạnh bằng tỉ số đồng dạng. | **Bài giải:**<br>Vì $MN \\parallel BC$ nên $\\Delta AMN \\backsim \\Delta ABC$.<br>Suy ra:<br>$$\\frac{AM}{AB} = \\frac{AN}{AC} = \\frac{MN}{BC}$$<br>Thay số ta có:<br>$$\\frac{2}{6} = \\frac{AN}{8} = \\frac{MN}{10}$$<br>Suy ra:<br>$$AN = \\frac{2 \\cdot 8}{6} = \\frac{8}{3}\\text{ (cm)}$$<br>$$MN = \\frac{2 \\cdot 10}{6} = \\frac{10}{3}\\text{ (cm)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng kiến thức tam giác đồng dạng giải thích cách ước lượng chiều cao cây bóng mát ngoài sân trường.
b) Nội dung: Dùng một chiếc cọc cắm thẳng đứng trên mặt đất, so sánh tỉ số chiều cao và bóng của cọc với chiều cao và bóng của cây.
c) Sản phẩm: Lời giải thích ngắn gọn dựa trên hiện tượng các tia nắng mặt trời song song tạo thành hai tam giác đồng dạng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS nêu cách đo chiều cao của cây dựa vào bóng cây trên mặt đất và bóng một chiếc cọc thẳng đứng.<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Các tia nắng song song tạo nên hai tam giác vuông đồng dạng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Tỉ số chiều cao cây trên chiều cao cọc bằng tỉ số chiều dài bóng cây trên bóng cọc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị cho bài các trường hợp đồng dạng tiếp theo. | Ứng dụng đo đạc: Chiều cao cây $H$ và bóng $L$, chiều cao cọc $h$ và bóng $l$ thỏa mãn:<br>$$\\frac{H}{h} = \\frac{L}{l} \\Rightarrow H = \\frac{L \\cdot h}{l}$$ |
"""
    },

    # 29: Bài 34
    {
        "filename": "29_KHBD_Toan8_Bai34_BaTruongHopDongDang_Tiet34-36.md",
        "md": """TIẾT 34, 35, 36 - BÀI 34: BA TRƯỜNG HỢP ĐỒNG DẠNG CỦA HAI TAM GIÁC
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và nắm vững ba trường hợp đồng dạng của hai tam giác:
  + Trường hợp 1 (Cạnh - Cạnh - Cạnh: c.c.c): Nếu ba cạnh của tam giác này tỉ lệ với ba cạnh của tam giác kia thì hai tam giác đó đồng dạng.
  + Trường hợp 2 (Cạnh - Góc - Cạnh: c.g.c): Nếu hai cạnh của tam giác này tỉ lệ với hai cạnh của tam giác kia và hai góc tạo bởi các cặp cạnh đó bằng nhau thì hai tam giác đó đồng dạng.
  + Trường hợp 3 (Góc - Góc: g.g): Nếu hai góc của tam giác này lần lượt bằng hai góc của tam giác kia thì hai tam giác đó đồng dạng.
- Vận dụng các trường hợp đồng dạng để chứng minh hai tam giác đồng dạng, tính độ dài đoạn thẳng và chứng minh hai góc bằng nhau.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đối chiếu các tỉ số cạnh và góc xen giữa, chủ động phát hiện điều kiện đồng dạng phù hợp.
- Giao tiếp và hợp tác: Làm việc nhóm phân tích các bài toán hình học phức hợp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Suy luận logic, lựa chọn đúng trường hợp đồng dạng (c.c.c, c.g.c hay g.g) để lập luận chặt chẽ.
- Năng lực mô hình hoá toán học: Chuyển đổi bài toán thực tế đo đạc khoảng cách không tới được thành bài toán tam giác đồng dạng.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS chọn công cụ đo tự động trên máy kiểm tra điều kiện đồng dạng; 2.4.TC2a: HS lựa chọn công cụ số phù hợp cùng bạn hoàn thành thử thách; 3.2.TC2a: HS thảo luận cách tích hợp hình tam giác vào tệp bài giảng lớp.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, cẩn thận và lập luận logic trong chứng minh hình học.
- Ý thức hợp tác, tương trợ đồng đội trong học tập.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, thước thẳng, compa, thước đo góc, máy tính, máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, dụng cụ vẽ hình đầy đủ, vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại điều kiện hai tam giác bằng nhau (c.c.c, c.g.c, g.c.g) và dẫn dắt sang tìm điều kiện tinh giản cho hai tam giác đồng dạng.
b) Nội dung: Liệu có cần kiểm tra đủ 3 góc bằng nhau và 3 cạnh tỉ lệ để khẳng định hai tam giác đồng dạng không?
c) Sản phẩm: Dự đoán của HS: Chỉ cần một số điều kiện tối giản như đối với tam giác bằng nhau.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hai tam giác bằng nhau có 3 trường hợp đơn giản hóa. Vậy với hai tam giác đồng dạng, có những trường hợp đơn giản hóa nào?<br>- **HS:** Lắng nghe và suy ngẫm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trao đổi cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Dự đoán có các trường hợp cạnh - cạnh - cạnh, cạnh - góc - cạnh và góc - góc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định dự đoán đúng và bắt đầu bài học nghiên cứu chi tiết 3 trường hợp. | Đặt vấn đề: Tìm các điều kiện rút gọn để khẳng định hai tam giác đồng dạng. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (105 phút)
### Hoạt động 2.1: Trường hợp đồng dạng thứ nhất (c.c.c) (35 phút)
a) Mục tiêu: Nắm vững và áp dụng trường hợp đồng dạng cạnh - cạnh - cạnh.
b) Nội dung: Phát biểu định lí c.c.c và giải các ví dụ minh họa.
c) Sản phẩm: Vở ghi bài và lời giải bài toán chứng minh tam giác đồng dạng theo c.c.c.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí: Nếu ba cạnh của tam giác này tỉ lệ với ba cạnh của tam giác kia thì hai tam giác đó đồng dạng.<br>Nếu $\\frac{A'B'}{AB} = \\frac{B'C'}{BC} = \\frac{C'A'}{CA}$ thì $\\Delta A'B'C' \\backsim \\Delta ABC$ (c.c.c).<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho $\\Delta ABC$ có cạnh $4, 6, 8\\text{ cm}$ và $\\Delta DEF$ có cạnh $2, 3, 4\\text{ cm}$. Hỏi hai tam giác có đồng dạng không?<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Ta có $\\frac{DEF}{ABC}$: $\\frac{2}{4} = \\frac{3}{6} = \\frac{4}{8} = \\frac{1}{2}$. Vậy $\\Delta DEF \\backsim \\Delta ABC$ (c.c.c).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Cần sắp xếp các cạnh theo thứ tự từ bé đến lớn trước khi lập tỉ số. | **1. Trường hợp đồng dạng thứ nhất (c.c.c):**<br>Nếu $\\Delta A'B'C'$ và $\\Delta ABC$ có:<br>$$\\frac{A'B'}{AB} = \\frac{B'C'}{BC} = \\frac{C'A'}{CA}$$<br>thì $\\Delta A'B'C' \\backsim \\Delta ABC$ (c.c.c). |

### Hoạt động 2.2: Trường hợp đồng dạng thứ hai (c.g.c) (35 phút)
a) Mục tiêu: Nắm vững và áp dụng trường hợp đồng dạng cạnh - góc - cạnh (góc xen giữa hai cặp cạnh tỉ lệ).
b) Nội dung: Phát biểu định lí c.g.c, lưu ý vị trí góc xen giữa.
c) Sản phẩm: Lời giải bài tập chứng minh tam giác đồng dạng theo c.g.c.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí: Nếu hai cạnh của tam giác này tỉ lệ với hai cạnh của tam giác kia và hai góc tạo bởi các cặp cạnh đó bằng nhau thì hai tam giác đó đồng dạng.<br>- **HS:** Ghi nhớ góc phải nằm xen giữa hai cạnh tương ứng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho $\\Delta ABC$ có $AB = 4, AC = 6, \\widehat{A} = 60^\\circ$ và $\\Delta MNP$ có $MN = 2, MP = 3, \\widehat{M} = 60^\\circ$. Xét tính đồng dạng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Ta có $\\frac{MN}{AB} = \\frac{2}{4} = \\frac{1}{2}$, $\\frac{MP}{AC} = \\frac{3}{6} = \\frac{1}{2}$ và $\\widehat{M} = \\widehat{A} = 60^\\circ$. Do đó $\\Delta MNP \\backsim \\Delta ABC$ (c.g.c).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Nếu góc bằng nhau không xen giữa thì chưa thể kết luận đồng dạng. | **2. Trường hợp đồng dạng thứ hai (c.g.c):**<br>Nếu $\\Delta A'B'C'$ và $\\Delta ABC$ có:<br>$$\\frac{A'B'}{AB} = \\frac{A'C'}{AC}\\text{ và }\\widehat{A'} = \\widehat{A}$$<br>thì $\\Delta A'B'C' \\backsim \\Delta ABC$ (c.g.c). |

### Hoạt động 2.3: Trường hợp đồng dạng thứ ba (g.g) (35 phút)
a) Mục tiêu: Nắm vững và áp dụng trường hợp đồng dạng góc - góc.
b) Nội dung: Định lí hai tam giác có hai cặp góc bằng nhau thì đồng dạng.
c) Sản phẩm: Vở ghi và các bài toán áp dụng trường hợp g.g.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí: Nếu hai góc của tam giác này lần lượt bằng hai góc của tam giác kia thì hai tam giác đó đồng dạng.<br>- **HS:** Nhận thức đây là trường hợp được dùng phổ biến nhất trong hình học.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho hình thang $ABCD$ ($AB \\parallel CD$). Gọi $O$ là giao điểm hai đường chéo. Chứng minh $\\Delta OAB \\backsim \\Delta OCD$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Vì $AB \\parallel CD$ nên $\\widehat{OAB} = \\widehat{OCD}$ (so le trong) và $\\widehat{OBA} = \\widehat{ODC}$ (so le trong). Vậy $\\Delta OAB \\backsim \\Delta OCD$ (g.g).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và chốt định lí g.g. | **3. Trường hợp đồng dạng thứ ba (g.g):**<br>Nếu $\\Delta A'B'C'$ và $\\Delta ABC$ có:<br>$$\\widehat{A'} = \\widehat{A}\\text{ và }\\widehat{B'} = \\widehat{B}$$<br>thì $\\Delta A'B'C' \\backsim \\Delta ABC$ (g.g). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Rèn luyện kỹ năng phối hợp linh hoạt ba trường hợp đồng dạng.
b) Nội dung: Cho tam giác $ABC$ có đường cao $AH$. Kẻ $HM \\perp AB, HN \\perp AC$. Chứng minh $\\Delta AMN \\backsim \\Delta ACB$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở ghi.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập hình học chứng minh tam giác đồng dạng.<br>- **HS:** Vẽ hình và tìm mối quan hệ tỉ số.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Dùng hệ thức lượng hoặc các cặp tam giác vuông đồng dạng để suy ra tỉ số $\\frac{AM}{AC} = \\frac{AN}{AB}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xét $\\Delta AMN$ và $\\Delta ACB$ có $\\widehat{A}$ chung và $\\frac{AM}{AC} = \\frac{AN}{AB}$ nên $\\Delta AMN \\backsim \\Delta ACB$ (c.g.c).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa lời giải chứng minh trên bảng. | **Bài giải:**<br>Ta có $\\Delta AMH \\backsim \\Delta AHB$ (g.g) suy ra $AH^2 = AM \\cdot AB$.<br>Tương tự $\\Delta ANH \\backsim \\Delta AHC$ (g.g) suy ra $AH^2 = AN \\cdot AC$.<br>Do đó $AM \\cdot AB = AN \\cdot AC \\Rightarrow \\frac{AM}{AC} = \\frac{AN}{AB}$.<br>Xét $\\Delta AMN$ và $\\Delta ACB$ có:<br>- $\\widehat{A}$ chung;<br>- $\\frac{AM}{AC} = \\frac{AN}{AB}$.<br>Vậy $\\Delta AMN \\backsim \\Delta ACB$ (c.g.c). |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng trường hợp góc - góc đo bề rộng con sông mà không cần qua sông.
b) Nội dung: Mô phỏng bài toán xác định khoảng cách giữa hai điểm $A$ và $B$ bị ngăn cách bởi hồ nước.
c) Sản phẩm: Lời giải sơ đồ đo đạc dựa trên trường hợp g.g.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán đo khoảng cách $AB$ bờ bên kia bằng việc chọn cọc mốc và tạo hai tam giác đồng dạng theo trường hợp g.g.<br>- **HS:** Quan sát mô hình thực tế.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định các góc bằng nhau nhờ ngắm thẳng hàng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trình bày công thức tính khoảng cách dựa vào tỉ số đồng dạng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và chốt kiến thức ứng dụng thực tiễn của tam giác đồng dạng. | Ứng dụng đo bề rộng sông/hồ nhờ tính chất tam giác đồng dạng g.g. |
"""
    },

    # 30: Tiết 37: Luyện tập chung (Mindmap: mindmap_toan8_hinh_tiet37.png)
    {
        "filename": "30_KHBD_Toan8_LuyenTapChung_Tiet37.md",
        "md": """TIẾT 37 - LUYỆN TẬP CHUNG KIỂM TRA ĐÁNH GIÁ THƯỜNG XUYÊN
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố định nghĩa hai tam giác đồng dạng và ba trường hợp đồng dạng của hai tam giác (c.c.c, c.g.c, g.g).
- Vận dụng thành thạo các trường hợp đồng dạng để chứng minh tam giác đồng dạng, tính độ dài đoạn thẳng, chứng minh tỉ lệ thức và các góc bằng nhau.
- Thực hiện kiểm tra đánh giá thường xuyên kiến thức tam giác đồng dạng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức các trường hợp đồng dạng bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp chứng minh hình học.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng nhìn nhận hình học, phát hiện các yếu tố góc bằng nhau và tỉ số cạnh để chọn đúng trường hợp đồng dạng.
- Năng lực giải quyết vấn đề toán học: Hoàn thành bài kiểm tra đánh giá thường xuyên đúng thời gian quy định.

c) Năng lực số (NLS):
- ***1.2.TC2a: HS so sánh độ chính xác giữa phép đo tay và phép đo phần mềm; 2.2.TC2a: HS chia sẻ nội dung số về phương pháp chứng minh cho cả lớp; 5.1.TC2a: HS xác định lỗi khi các đỉnh tam giác không liên kết đúng trên máy.***

## 3. Về phẩm chất
- Trung thực, nghiêm túc khi làm bài kiểm tra đánh giá thường xuyên.
- Rèn tính cẩn thận, vẽ hình chính xác và rõ ràng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, phiếu kiểm tra đánh giá thường xuyên 15 phút, sơ đồ tư duy vector 300 DPI.
2. Học sinh: SGK, vở ghi, dụng cụ vẽ hình đầy đủ, giấy làm bài kiểm tra.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt tư duy và tổng hợp nhanh ba trường hợp đồng dạng của tam giác.
b) Nội dung: Trò chơi ghép nối các điều kiện với tên gọi trường hợp đồng dạng tương ứng.
c) Sản phẩm: Bảng ghép nối đúng các trường hợp c.c.c, c.g.c, g.g của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Nêu điều kiện để hai tam giác đồng dạng theo trường hợp c.c.c, c.g.c, g.g.<br>- **HS:** Suy nghĩ nhanh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại nhanh 3 trường hợp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện phát biểu miệng trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá và chiếu sơ đồ tư duy tổng hợp. | Tổng hợp điều kiện đồng dạng: c.c.c (3 cặp cạnh tỉ lệ), c.g.c (2 cặp cạnh tỉ lệ và góc xen giữa bằng nhau), g.g (2 cặp góc bằng nhau). |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức tam giác đồng dạng bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Khái quát hóa toàn bộ kiến thức định nghĩa, tính chất, định lí Thalès tạo tam giác đồng dạng và ba trường hợp đồng dạng.
b) Nội dung: Quan sát và phân tích sơ đồ tư duy trực quan 300 DPI.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Tam giác đồng dạng Tiết 37](khbd-ill:mindmap-toan8-hinh-tiet37)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI hệ thống kiến thức Tam giác đồng dạng. Yêu cầu HS phân tích các nhánh kiến thức chính.<br>- **HS:** Quan sát sơ đồ tư duy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh: Định nghĩa, Định lí tạo tam giác đồng dạng, Ba trường hợp đồng dạng (c.c.c, c.g.c, g.g), Ứng dụng thực tế.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS trình bày lại toàn bộ cấu trúc sơ đồ tư duy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại trọng tâm kiến thức và lưu ý các sai lầm thường gặp (quên điều kiện góc xen giữa ở c.g.c, viết sai thứ tự đỉnh tương ứng). | **Hệ thống kiến thức trọng tâm:**<br>1. Định nghĩa & Tỉ số đồng dạng $k$.<br>2. Định lí đường song song tạo tam giác đồng dạng.<br>3. Ba trường hợp đồng dạng: c.c.c, c.g.c, g.g.<br>4. Ứng dụng: Tính khoảng cách, chiều cao, chứng minh hình học. |

## C. LUYỆN TẬP VÀ KIỂM TRA ĐÁNH GIÁ (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Đánh giá thường xuyên mức độ nắm kiến thức và kỹ năng chứng minh tam giác đồng dạng của học sinh (kiểm tra 15 phút).
b) Nội dung: Đề kiểm tra đánh giá thường xuyên gồm 2 câu: 1 câu trắc nghiệm đúng/sai và 1 bài tập tự luận chứng minh tam giác đồng dạng.
c) Sản phẩm: Bài làm trên giấy kiểm tra của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát đề kiểm tra 15 phút:<br>Cho $\\Delta ABC$ có $AB = 6\\text{ cm}, AC = 9\\text{ cm}$. Trên $AB$ lấy điểm $D$ sao cho $AD = 3\\text{ cm}$, trên $AC$ lấy điểm $E$ sao cho $AE = 2\\text{ cm}$.<br>a) Chứng minh $\\Delta ADE \\backsim \\Delta ACB$.<br>b) Biết $BC = 12\\text{ cm}$, tính độ dài $DE$.<br>- **HS:** Nghiêm túc làm bài độc lập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lập tỉ số $\\frac{AD}{AC}$ và $\\frac{AE}{AB}$, xét góc chung $\\widehat{A}$, tính độ dài $DE$.<br><br>**+ Bước 3: Thu bài**<br>- **GV:** Hết giờ, GV thu bài kiểm tra của cả lớp.<br><br>**+ Bước 4: Nhận xét nhanh**<br>- **GV:** Hướng dẫn sơ lược đáp án để HS tự đối chiếu kết quả. | **Đáp án kiểm tra:**<br>a) Ta có:<br>$$\\frac{AD}{AC} = \\frac{3}{9} = \\frac{1}{3}$$<br>$$\\frac{AE}{AB} = \\frac{2}{6} = \\frac{1}{3}$$<br>Suy ra $\\frac{AD}{AC} = \\frac{AE}{AB} = \\frac{1}{3}$.<br>Xét $\\Delta ADE$ và $\\Delta ACB$ có:<br>- $\\widehat{A}$ chung;<br>- $\\frac{AD}{AC} = \\frac{AE}{AB}$.<br>Vậy $\\Delta ADE \\backsim \\Delta ACB$ (c.g.c).<br><br>b) Vì $\\Delta ADE \\backsim \\Delta ACB$ nên:<br>$$\\frac{DE}{BC} = \\frac{AD}{AC} = \\frac{1}{3} \\Rightarrow DE = \\frac{BC}{3} = \\frac{12}{3} = 4\\text{ (cm)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Mở rộng kiến thức về mối quan hệ giữa tỉ số diện tích và tỉ số đồng dạng của hai tam giác.
b) Nội dung: Nếu $\\Delta A'B'C' \\backsim \\Delta ABC$ với tỉ số đồng dạng $k$ thì $\\frac{S_{A'B'C'}}{S_{ABC}} = k^2$.
c) Sản phẩm: Ghi nhận định lí mở rộng vào vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi mở rộng: Nếu kích thước một tam giác tăng gấp đôi thì diện tích tăng gấp mấy lần?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đáy tăng $2$ lần, chiều cao tăng $2$ lần, diện tích tăng $4$ lần ($2^2 = 4$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát biểu tỉ số diện tích bằng bình phương tỉ số đồng dạng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt định lí và giao bài tập về nhà. | **Định lí mở rộng:**<br>Nếu $\\Delta A'B'C' \\backsim \\Delta ABC$ theo tỉ số $k$ thì:<br>$$\\frac{S_{A'B'C'}}{S_{ABC}} = k^2$$ |
"""
    },

    # 31: Bài 35
    {
        "filename": "31_KHBD_Toan8_Bai35_DinhLiPythagoreVaUngDung_Tiet38-39.md",
        "md": """TIẾT 38, 39 - BÀI 35: ĐỊNH LÍ PYTHAGORE VÀ ỨNG DỤNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu và nắm vững định lí Pythagore: Trong một tam giác vuông, bình phương của cạnh huyền bằng tổng các bình phương của hai cạnh góc vuông: $a^2 + b^2 = c^2$.
- Hiểu định lí Pythagore đảo: Nếu một tam giác có bình phương của một cạnh bằng tổng các bình phương của hai cạnh kia thì tam giác đó là tam giác vuông.
- Vận dụng định lí Pythagore để tính độ dài cạnh trong tam giác vuông và ứng dụng vào giải quyết các bài toán thực tiễn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự khám phá mối quan hệ diện tích hình vuông dựng trên các cạnh của tam giác vuông.
- Giao tiếp và hợp tác: Cùng nhóm tính toán độ dài các cạnh huyền và cạnh góc vuông trong các hình vẽ thực tế.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Vận dụng định lí Pythagore đảo để nhận biết một tam giác có phải là tam giác vuông hay không.
- Năng lực mô hình hoá toán học: Tính chiều dài chiếc thang cần thiết để leo lên tường, khoảng cách đường chéo màn hình tivi.

c) Năng lực số (NLS):
- ***5.3.TC2a: HS sử dụng phần mềm mô phỏng hình học trực quan về định lí; 1.1.TC2b: HS tổ chức tìm kiếm ứng dụng Pythagore trong kiến trúc; 5.2.TC2b: HS chọn công cụ vẽ thực nghiệm định lí Pythagore đảo.***

## 3. Về phẩm chất
- Khơi gợi niềm say mê lịch sử toán học và các định lí bất hủ.
- Cẩn thận, chính xác trong các phép tính căn bậc hai và bình phương số thực.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, mô hình ghép hình chứng minh định lí Pythagore, máy tính cầm tay, bài trình chiếu.
2. Học sinh: SGK, máy tính cầm tay, thước kẻ có chia vạch, kéo cắt giấy thực nghiệm ghép hình.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt bài toán tính khoảng cách đường chéo màn hình tivi theo đơn vị inch khi biết chiều rộng và chiều cao.
b) Nội dung: Màn hình tivi phẳng có chiều rộng $40\\text{ cm}$ và chiều cao $30\\text{ cm}$. Hỏi đường chéo màn hình dài bao nhiêu xentimét?
c) Sản phẩm: Dự đoán của HS và mong muốn tìm quy tắc tính cạnh huyền khi biết hai cạnh góc vuông.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu tình huống thực tế về kích thước màn hình tivi 40 cm x 30 cm. Làm thế nào tính độ dài đường chéo?<br>- **HS:** Tiếp nhận bài toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh cách tính độ dài cạnh huyền.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhớ lại định lí Pythagore đã từng nghe ở lớp dưới hoặc ước lượng trực tiếp bằng thước đo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu định lí mang tên nhà toán học Pythagore thời Hy Lạp cổ đại. | Tình huống dẫn nhập: Tính cạnh huyền của tam giác vuông khi biết hai cạnh góc vuông. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Định lí Pythagore thuận (35 phút)
a) Mục tiêu: Nắm vững định lí Pythagore thuận và công thức tính $c = \\sqrt{a^2 + b^2}$, $a = \\sqrt{c^2 - b^2}$.
b) Nội dung: Khám phá thông qua diện tích các hình vuông dựng trên cạnh tam giác vuông; phát biểu định lí.
c) Sản phẩm: Vở ghi định lí và bài tập tính cạnh tam giác vuông.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh ghép 4 tam giác vuông bằng nhau tạo thành hình vuông lớn. Dẫn dắt đến công thức $a^2 + b^2 = c^2$. Phát biểu định lí Pythagore.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho tam giác $ABC$ vuông tại $A$ có $AB = 5\\text{ cm}, AC = 12\\text{ cm}$. Tính độ dài cạnh huyền $BC$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $BC^2 = AB^2 + AC^2 = 5^2 + 12^2 = 25 + 144 = 169$. Do đó $BC = \\sqrt{169} = 13\\text{ (cm)}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt công thức: Muốn tìm cạnh huyền ta lấy căn bậc hai của tổng bình phương hai cạnh góc vuông. Muốn tìm cạnh góc vuông ta lấy căn bậc hai của hiệu bình phương cạnh huyền trừ bình phương cạnh góc vuông còn lại. | **1. Định lí Pythagore:**<br>Trong một tam giác vuông, bình phương của cạnh huyền bằng tổng các bình phương của hai cạnh góc vuông:<br>Cho $\\Delta ABC$ vuông tại $A$:<br>$$BC^2 = AB^2 + AC^2$$<br>Ví dụ: $AB = 5, AC = 12 \\Rightarrow BC = \\sqrt{5^2 + 12^2} = 13\\text{ (cm)}$. |

### Hoạt động 2.2: Định lí Pythagore đảo (30 phút)
a) Mục tiêu: Nắm vững định lí Pythagore đảo để kiểm tra một tam giác có vuông hay không.
b) Nội dung: Phát biểu định lí đảo, so sánh bình phương cạnh lớn nhất với tổng bình phương hai cạnh nhỏ hơn.
c) Sản phẩm: Lời giải các bài tập nhận biết tam giác vuông trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí Pythagore đảo: Nếu tam giác có bình phương của một cạnh bằng tổng các bình phương của hai cạnh kia thì tam giác đó là tam giác vuông.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kiểm tra tam giác có độ dài ba cạnh sau có vuông không: $9\\text{ cm}, 12\\text{ cm}, 15\\text{ cm}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Cạnh lớn nhất là $15$. Ta có $15^2 = 225$. Tổng bình phương hai cạnh kia: $9^2 + 12^2 = 81 + 144 = 225$. Vì $15^2 = 9^2 + 12^2$ nên tam giác đó vuông.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt quy tắc: So sánh bình phương cạnh lớn nhất với tổng bình phương hai cạnh còn lại. | **2. Định lí Pythagore đảo:**<br>Nếu một tam giác có bình phương một cạnh bằng tổng bình phương hai cạnh kia thì tam giác đó là tam giác vuông:<br>Nếu $\\Delta ABC$ có $BC^2 = AB^2 + AC^2$ thì $\\Delta ABC$ vuông tại $A$.<br>Bộ ba số tự nhiên $(a, b, c)$ thỏa mãn $a^2 + b^2 = c^2$ gọi là bộ ba số Pythagore (ví dụ: $(3, 4, 5); (5, 12, 13); (6, 8, 10); (9, 12, 15)$). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Rèn luyện tính toán cạnh hình chữ nhật, hình thoi bằng định lí Pythagore.
b) Nội dung: Một hình thoi có độ dài hai đường chéo là $12\\text{ cm}$ và $16\\text{ cm}$. Tính độ dài cạnh của hình thoi.
c) Sản phẩm: Lời giải chi tiết trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho hình thoi $ABCD$ có đường chéo $AC = 16\\text{ cm}, BD = 12\\text{ cm}$. Tính cạnh $AB$.<br>- **HS:** Nhắc lại tính chất hai đường chéo hình thoi vuông góc và cắt nhau tại trung điểm mỗi đường.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Gọi $O$ là giao điểm hai đường chéo. $OA = 8\\text{ cm}, OB = 6\\text{ cm}$. Áp dụng định lí Pythagore cho $\\Delta OAB$ vuông tại $O$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và chốt kết quả cạnh hình thoi bằng $10\\text{ cm}$. | **Bài giải:**<br>Gọi $O$ là giao điểm hai đường chéo của hình thoi $ABCD$.<br>Ta có $AC \\perp BD$ tại $O$, và:<br>$$OA = \\frac{AC}{2} = \\frac{16}{2} = 8\\text{ (cm)}$$<br>$$OB = \\frac{BD}{2} = \\frac{12}{2} = 6\\text{ (cm)}$$<br>Áp dụng định lí Pythagore vào $\\Delta OAB$ vuông tại $O$:<br>$$AB^2 = OA^2 + OB^2 = 8^2 + 6^2 = 64 + 36 = 100$$<br>Suy ra $AB = \\sqrt{100} = 10\\text{ (cm)}$.<br>Vậy cạnh của hình thoi dài $10\\text{ cm}$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Giải quyết bài toán thực tế đo đường chéo màn hình tivi nêu ở phần khởi động.
b) Nội dung: Màn hình kích thước $40\\text{ cm} \\times 30\\text{ cm}$. Tính đường chéo theo cm và đổi ra inch ($1\\text{ inch} \\approx 2{,}54\\text{ cm}$).
c) Sản phẩm: Lời giải tính được đường chéo $50\\text{ cm} \\approx 19{,}7\\text{ inch}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Quay lại bài toán khởi động: Tính đường chéo màn hình tivi $40\\text{ cm} \\times 30\\text{ cm}$.<br>- **HS:** Tính nhanh vào nháp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $d = \\sqrt{40^2 + 30^2} = \\sqrt{1600 + 900} = \\sqrt{2500} = 50\\text{ (cm)}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đổi ra inch: $\\frac{50}{2{,}54} \\approx 19{,}7\\text{ inch}$ (tivi khoảng 20 inch).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao sự liên hệ thực tế của học sinh. | Đường chéo màn hình tivi:<br>$$d = \\sqrt{40^2 + 30^2} = 50\\text{ (cm)}$$<br>Đổi ra đơn vị inch:<br>$$50 : 2{,}54 \\approx 19{,}7\\text{ (inch)}$$ |
"""
    },

    # 32: Bài 36
    {
        "filename": "32_KHBD_Toan8_Bai36_CacTruongHopDongDangTamGiacVuong_Tiet40-41.md",
        "md": """TIẾT 40, 41 - BÀI 36: CÁC TRƯỜNG HỢP ĐỒNG DẠNG CỦA HAI TAM GIÁC VUÔNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết các trường hợp đồng dạng đặc biệt của hai tam giác vuông:
  + Tam giác vuông có một góc nhọn bằng nhau (hệ quả của trường hợp g.g).
  + Tam giác vuông có hai cạnh góc vuông tỉ lệ (hệ quả của trường hợp c.g.c).
  + Trường hợp đồng dạng đặc biệt về cạnh huyền và cạnh góc vuông: Nếu cạnh huyền và một cạnh góc vuông của tam giác vuông này tỉ lệ với cạnh huyền và một cạnh góc vuông của tam giác vuông kia thì hai tam giác vuông đó đồng dạng.
- Vận dụng các trường hợp đồng dạng của tam giác vuông vào tính toán độ dài và chứng minh hệ thức lượng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đối chiếu và rút ra tính chất đặc thù của tam giác vuông từ tam giác thường.
- Giao tiếp và hợp tác: Phối hợp giải các bài toán ứng dụng tam giác vuông đồng dạng.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Sử dụng định lí Pythagore để chứng minh trường hợp cạnh huyền - cạnh góc vuông.
- Năng lực giải quyết vấn đề toán học: Thiết lập tỉ số cạnh để tính chiều cao của một công trình.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS lựa chọn MTBT tính các hệ thức lượng trong tam giác vuông; 3.1.TC2a: HS chỉ ra cách vẽ tam giác vuông đồng dạng tỉ số cho trước; 1.3.TC2a: HS sắp xếp các bộ số Pythagore vào bảng tính quản lý.***

## 3. Về phẩm chất
- Rèn thói quen tư duy khoa học, cẩn trọng trong từng bước lập luận.
- Hăng say tìm tòi các ứng dụng của hình học vuông góc.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, eke, thước thẳng, máy tính, bảng phụ hoặc slide trình chiếu.
2. Học sinh: SGK, thước kẻ, eke có góc $90^\\circ$, máy tính cầm tay, vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhận biết tam giác vuông đã có sẵn một góc bằng $90^\\circ$, từ đó suy ra các trường hợp đồng dạng tối giản hơn nữa.
b) Nội dung: So sánh hai tam giác vuông có một góc nhọn bằng $30^\\circ$. Chúng có đồng dạng không?
c) Sản phẩm: Khẳng định của HS: Đồng dạng vì đã có 2 góc bằng nhau ($90^\\circ$ và $30^\\circ$).
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Hai tam giác vuông có một góc nhọn bằng nhau thì có đồng dạng không? Vì sao?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Do cả hai tam giác đều có góc vuông $90^\\circ$, thêm một góc nhọn bằng nhau nên đồng dạng theo trường hợp g.g.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đúng. Hôm nay ta nghiên cứu sâu hơn về các trường hợp đồng dạng của tam giác vuông. | Hai tam giác vuông có một góc nhọn bằng nhau thì luôn đồng dạng. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Các trường hợp suy biến từ tam giác thường (30 phút)
a) Mục tiêu: Nắm vững hai dấu hiệu đồng dạng cơ bản của tam giác vuông (góc nhọn và hai cạnh góc vuông).
b) Nội dung: Hệ quả từ trường hợp g.g và c.g.c đối với góc vuông.
c) Sản phẩm: Vở ghi bài hai dấu hiệu đồng dạng cơ bản.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu hai dấu hiệu đồng dạng đầu tiên của tam giác vuông:<br>1) Có một góc nhọn bằng nhau.<br>2) Có hai cạnh góc vuông tỉ lệ.<br>- **HS:** Ghi chép và lấy ví dụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho tam giác $ABC$ vuông tại $A$ và tam giác $A'B'C'$ vuông tại $A'$. Nếu $\\frac{A'B'}{AB} = \\frac{A'C'}{AC}$ thì kết luận gì?<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $\\Delta A'B'C' \\backsim \\Delta ABC$ (vì góc xen giữa $\\widehat{A'} = \\widehat{A} = 90^\\circ$).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và chốt hai dấu hiệu. | **1. Hai dấu hiệu đồng dạng cơ bản:**<br>Hai tam giác vuông đồng dạng nếu:<br>- Chúng có một góc nhọn bằng nhau.<br>- Hoặc hai cạnh góc vuông của tam giác này tỉ lệ với hai cạnh góc vuông của tam giác kia. |

### Hoạt động 2.2: Dấu hiệu đặc biệt (Cạnh huyền - Cạnh góc vuông) (35 phút)
a) Mục tiêu: Hiểu và chứng minh dấu hiệu cạnh huyền và một cạnh góc vuông tỉ lệ.
b) Nội dung: Phát biểu định lí và dùng định lí Pythagore giải thích.
c) Sản phẩm: Lời giải chứng minh định lí và vở ghi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định lí: Nếu cạnh huyền và một cạnh góc vuông của tam giác vuông này tỉ lệ với cạnh huyền và một cạnh góc vuông của tam giác vuông kia thì hai tam giác vuông đó đồng dạng.<br>Tức là: $\\frac{B'C'}{BC} = \\frac{A'B'}{AB} = k$. Chứng minh $\\frac{A'C'}{AC} = k$.<br>- **HS:** Suy nghĩ áp dụng Pythagore.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Biểu diễn $A'C' = \\sqrt{B'C'^2 - A'B'^2} = \\sqrt{k^2 BC^2 - k^2 AB^2} = k \\sqrt{BC^2 - AB^2} = k \\cdot AC$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Do đó $\\frac{A'C'}{AC} = k$. Ba cạnh tỉ lệ nên hai tam giác đồng dạng theo c.c.c.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và chuẩn hóa chứng minh. | **2. Dấu hiệu cạnh huyền - cạnh góc vuông:**<br>Nếu $\\Delta A'B'C'$ vuông tại $A'$ và $\\Delta ABC$ vuông tại $A$ có:<br>$$\\frac{B'C'}{BC} = \\frac{A'B'}{AB}$$<br>thì $\\Delta A'B'C' \\backsim \\Delta ABC$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vận dụng tam giác vuông đồng dạng chứng minh hệ thức $AH^2 = BH \\cdot CH$.
b) Nội dung: Cho tam giác $ABC$ vuông tại $A$, đường cao $AH$. Chứng minh $\\Delta HBA \\backsim \\Delta HAC$ và suy ra $AH^2 = BH \\cdot CH$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu chứng minh $\\Delta HBA \\backsim \\Delta HAC$ từ đó suy ra hệ thức đường cao.<br>- **HS:** Vẽ hình và tìm các góc bằng nhau.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xét hai tam giác vuông có $\\widehat{HBA} = \\widehat{HAC}$ (cùng phụ với $\\widehat{C}$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt hệ thức lượng quan trọng của tam giác vuông. | **Bài giải:**<br>Xét $\\Delta HBA$ (vuông tại $H$) và $\\Delta HAC$ (vuông tại $H$) có:<br>$$\\widehat{HBA} = \\widehat{HAC}\\text{ (cùng phụ với }\\widehat{C}\\text{)}$$<br>Do đó $\\Delta HBA \\backsim \\Delta HAC$ (góc nhọn).<br>Suy ra:<br>$$\\frac{HA}{HC} = \\frac{HB}{HA} \\Rightarrow HA^2 = HB \\cdot HC$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng hệ thức lượng vừa chứng minh để tính chiều cao khi biết độ dài hai hình chiếu.
b) Nội dung: Cho $BH = 4\\text{ m}, CH = 9\\text{ m}$. Tính chiều cao $AH$.
c) Sản phẩm: Kết quả $AH = \\sqrt{4 \\cdot 9} = 6\\text{ m}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tính $AH$ khi $BH = 4\\text{ m}, CH = 9\\text{ m}$.<br>- **HS:** Thay số tính toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $AH^2 = 4 \\cdot 9 = 36 \\Rightarrow AH = 6\\text{ (m)}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời nhanh miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và giao bài tập về nhà. | Chiều cao $AH$ là:<br>$$AH = \\sqrt{4 \\cdot 9} = 6\\text{ (m)}$$ |
"""
    },

    # 33: Bài 37
    {
        "filename": "33_KHBD_Toan8_Bai37_HinhDongDang_Tiet42.md",
        "md": """TIẾT 42 - BÀI 37: HÌNH ĐỒNG DẠNG
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết khái niệm hình đồng dạng trong hình học và thực tiễn (hai hình có hình dạng giống nhau nhưng có thể khác nhau về kích thước).
- Nhận biết hình đồng dạng phối cảnh (hình vị tự): Hình phóng to hoặc thu nhỏ từ một tâm phối cảnh.
- Nhận biết các cặp hình phẳng đồng dạng: Hai đoạn thẳng bất kì, hai đường tròn bất kì, hai hình vuông bất kì luôn đồng dạng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tìm kiếm hình ảnh đồng dạng trong thiên nhiên, nghệ thuật và kiến trúc.
- Giao tiếp và hợp tác: Cùng nhóm thảo luận về tâm phối cảnh và tỉ số đồng dạng của hình.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh tỉ lệ kích thước tương ứng giữa hình gốc và hình đồng dạng phối cảnh.
- Năng lực mô hình hoá toán học: Giải thích nguyên lí chiếu bóng trên màn hình, phóng to bản đồ địa lí.

c) Năng lực số (NLS):
- ***1.1.TC2c: HS mô tả cách tìm hình ảnh thực tế về phối cảnh trên mạng; 5.3.TC2a: HS sử dụng công cụ số sáng tạo họa tiết đồng dạng đổi mới; 3.1.TC2b: HS thể hiện ý tưởng thiết kế vật dụng đồng dạng qua phần mềm.***

## 3. Về phẩm chất
- Nâng cao năng lực thẩm mỹ, cảm thụ vẻ đẹp của tính cân đối và đồng dạng trong thiên nhiên (lá cây, vỏ ốc, hoa văn trống đồng).
- Tinh thần khám phá khoa học và sáng tạo nghệ thuật.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, các hình ảnh minh họa tranh phối cảnh, hoa văn nghệ thuật, máy chiếu.
2. Học sinh: SGK, vở ghi, thước kẻ.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khơi gợi trực giác về hình đồng dạng qua thao tác phóng to - thu nhỏ (zoom in - zoom out) trên điện thoại thông minh.
b) Nội dung: Khi dùng hai ngón tay zoom một bức ảnh trên màn hình cảm ứng, hình ảnh bức ảnh thay đổi thế nào?
c) Sản phẩm: HS nhận xét: Bức ảnh phóng to hoặc thu nhỏ nhưng mọi tỉ lệ chi tiết không bị méo mó.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu tình huống phóng to ảnh trên smartphone: Kích thước đổi nhưng hình dạng có đổi không?<br>- **HS:** Quan sát và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời: Hình dáng giữ nguyên, chỉ kích thước to lên hoặc nhỏ đi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện phát biểu miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đó chính là hiện tượng hình đồng dạng phối cảnh trong toán học. | Thao tác zoom ảnh trên điện thoại cho ta một hình đồng dạng phối cảnh với hình ban đầu. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Khái niệm hình đồng dạng phối cảnh (15 phút)
a) Mục tiêu: Nhận biết tâm phối cảnh $O$ và tỉ số đồng dạng phối cảnh.
b) Nội dung: Quan sát các tia đi qua một điểm $O$ nối các điểm tương ứng của hai hình.
c) Sản phẩm: Vở ghi bài và hình vẽ minh họa tâm phối cảnh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình vẽ điểm $O$ và hai đa giác $ABCD$, $A'B'C'D'$ sao cho các đường thẳng $AA', BB', CC', DD'$ cùng đi qua $O$ và $\\frac{OA'}{OA} = \\frac{OB'}{OB} = k$. Nêu khái niệm hình đồng dạng phối cảnh.<br>- **HS:** Ghi nhận khái niệm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định tâm phối cảnh trong các hình vẽ SGK.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chỉ rõ tâm phối cảnh $O$ và tính tỉ số phóng to/thu nhỏ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Điểm $O$ gọi là tâm phối cảnh, $k$ là tỉ số phối cảnh. | **1. Hình đồng dạng phối cảnh:**<br>- Điểm $O$ là tâm phối cảnh.<br>- Tỉ số $k = \\frac{OA'}{OA}$ là tỉ số vị tự (phối cảnh).<br>- Nếu $k > 1$: Hình phóng to; nếu $k < 1$: Hình thu nhỏ. |

### Hoạt động 2.2: Hình đồng dạng trong đời sống (10 phút)
a) Mục tiêu: Nhận biết hai hình đồng dạng tổng quát và tính đồng dạng của các hình hình học cơ bản.
b) Nội dung: Hai hình vuông bất kì, hai đường tròn bất kì luôn đồng dạng.
c) Sản phẩm: Nhận biết được các hình luôn luôn đồng dạng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hai hình tròn bán kính khác nhau có đồng dạng không? Hai hình vuông có đồng dạng không? Hai tam giác đều có đồng dạng không?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mọi hình vuông đều có 4 góc vuông và 4 cạnh bằng nhau nên luôn đồng dạng. Tương tự với hình tròn và tam giác đều.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa kiến thức: Mọi đường tròn, mọi hình vuông, mọi tam giác đều đều là các hình đồng dạng. | **2. Hình đồng dạng trong đời sống:**<br>- Hai hình gọi là đồng dạng nếu một hình đồng dạng phối cảnh với hình kia hoặc bằng một hình đồng dạng phối cảnh với hình kia.<br>- Các hình luôn đồng dạng: Hai đoạn thẳng, hai đường tròn, hai hình vuông, hai tam giác đều. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (10 phút)
a) Mục tiêu: Nhận dạng hình đồng dạng và tìm tâm phối cảnh trong các bài tập SGK.
b) Nội dung: Bài tập nhận biết các cặp hình đồng dạng trong hình chụp lá cây, logo, họa tiết kiến trúc.
c) Sản phẩm: Câu trả lời chính xác của học sinh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu các hình vẽ logo và tranh ảnh, yêu cầu chỉ ra các cặp hình đồng dạng.<br>- **HS:** Quan sát và đối chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS chỉ rõ các cặp hình đồng dạng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ chính xác và khả năng quan sát của học sinh. | Xác định đúng các cặp hình đồng dạng và ước lượng tỉ số đồng dạng của chúng. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng vẽ họa tiết đồng dạng thu nhỏ trang trí bìa sách vở hoặc thiệp chúc mừng.
b) Nội dung: Vẽ liên tiếp 3 hình vuông thu nhỏ lồng nhau có cùng tâm đối xứng.
c) Sản phẩm: Hình vẽ trang trí trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn vẽ hình vuông lồng nhau thu nhỏ theo tỉ số $\\frac{1}{2}$ tạo hoa văn fractal.<br>- **HS:** Thực hành vẽ nhanh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nối trung điểm các cạnh để tạo hình vuông thu nhỏ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ vở khoe sản phẩm hình vẽ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi sự khéo léo và sáng tạo của học sinh. | Tạo họa tiết trang trí hình học đồng dạng. |
"""
    },

    # 34: Tiết 43: Luyện tập chung (Mindmap: mindmap_toan8_hinh_tiet43.png)
    {
        "filename": "34_KHBD_Toan8_LuyenTapChung_Tiet43.md",
        "md": """TIẾT 43 - LUYỆN TẬP CHUNG
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và rèn luyện kỹ năng vận dụng định lí Pythagore thuận và đảo, các trường hợp đồng dạng của tam giác vuông và khái niệm hình đồng dạng.
- Rèn luyện kỹ năng tính toán độ dài đoạn thẳng, chứng minh tam giác vuông, chứng minh tam giác vuông đồng dạng và thiết lập hệ thức hình học.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống kiến thức toàn bộ các bài 35, 36, 37 bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Hợp tác nhóm giải quyết bài toán hình học tổng hợp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Kết hợp linh hoạt định lí Pythagore và tam giác vuông đồng dạng để suy ra các hệ thức lượng.
- Năng lực mô hình hoá toán học: Giải bài toán ứng dụng đo khoảng cách thực tế ngoài trời.

c) Năng lực số (NLS):
- ***2.4.TC2a: HS chọn quy trình hợp tác số cùng nhóm giải bài toán đo vật thể; 3.2.TC2a: HS tinh chỉnh và tích hợp hình vẽ đồng dạng vào bài báo cáo; 1.2.TC2a: HS phân tích tính xác thực thông tin đo đạc từ nguồn trực tuyến.***

## 3. Về phẩm chất
- Tỉ mỉ, cẩn thận trong việc tính toán căn thức và làm tròn số thập phân.
- Tinh thần chủ động, vượt khó khi đối diện bài toán hình học có hình vẽ phức tạp.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, thước thẳng, compa, sơ đồ tư duy vector 300 DPI, máy chiếu.
2. Học sinh: SGK, vở ghi, dụng cụ vẽ hình đầy đủ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn nhanh công thức Pythagore và các trường hợp đồng dạng của tam giác vuông.
b) Nội dung: Trả lời nhanh: Tam giác vuông có cạnh huyền $10\\text{ cm}$ và một cạnh góc vuông $6\\text{ cm}$ thì cạnh góc vuông còn lại là bao nhiêu?
c) Sản phẩm: Đáp án $8\\text{ cm}$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi khởi động tính nhanh cạnh góc vuông.<br>- **HS:** Nhẩm nhanh theo bộ ba số Pythagore $(6, 8, 10)$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời cạnh còn lại là $\\sqrt{10^2 - 6^2} = 8\\text{ (cm)}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo kết quả miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang phần hệ thống kiến thức. | Khởi động: Vận dụng bộ ba số Pythagore tính nhanh cạnh tam giác vuông. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Định lí Pythagore và Tam giác vuông đồng dạng bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống toàn diện định lí Pythagore (thuận và đảo), 3 trường hợp đồng dạng của tam giác vuông và hình đồng dạng phối cảnh.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy 300 DPI.
c) Sản phẩm: Sơ đồ tư duy được vẽ hoặc tóm tắt vào vở ghi của học sinh.

![Sơ đồ tư duy Luyện tập chung Định lí Pythagore và Tam giác vuông đồng dạng Tiết 43](khbd-ill:mindmap-toan8-hinh-tiet43)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu sơ đồ tư duy vector 300 DPI về Định lí Pythagore và Tam giác vuông đồng dạng. Yêu cầu HS phân tích các mối liên hệ.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc các nhánh: 1) Định lí Pythagore ($c^2 = a^2 + b^2$); 2) Định lí đảo; 3) Tam giác vuông đồng dạng (Góc nhọn, Hai cạnh góc vuông, Cạnh huyền - Cạnh góc vuông); 4) Hình đồng dạng phối cảnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích sự kết hợp giữa định lí Pythagore và tam giác vuông đồng dạng trong việc tìm các hệ thức lượng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại phương pháp giải toán hình học tam giác vuông. | **Hệ thống kiến thức trọng tâm:**<br>1. Định lí Pythagore thuận & đảo.<br>2. Ba trường hợp đồng dạng của tam giác vuông.<br>3. Hình đồng dạng phối cảnh (tâm vị tự, tỉ số $k$).<br>4. Phương pháp tính đoạn thẳng và chứng minh hệ thức lượng. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Rèn luyện kỹ năng kết hợp định lí Pythagore và tam giác vuông đồng dạng.
b) Nội dung: Cho hình chữ nhật $ABCD$ có $AB = 8\\text{ cm}, BC = 6\\text{ cm}$. Kẻ $AH \\perp BD$ ($H \\in BD$).
1) Tính độ dài đường chéo $BD$.
2) Chứng minh $\\Delta AHB \\backsim \\Delta BCD$.
3) Tính độ dài $AH$.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao đề bài toán hình chữ nhật với các yêu cầu trên.<br>- **HS:** Vẽ hình chính xác vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng định lí Pythagore tính $BD = \\sqrt{8^2 + 6^2} = 10\\text{ (cm)}$.<br>Chứng minh hai tam giác vuông có $\\widehat{ABH} = \\widehat{BDC}$ (so le trong).<br>Lập tỉ số $\\frac{AH}{BC} = \\frac{AB}{BD}$ để tính $AH$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa lời giải mẫu trên bảng. | **Bài giải:**<br>1) Áp dụng định lí Pythagore cho $\\Delta ABD$ vuông tại $A$:<br>$$BD^2 = AB^2 + AD^2 = 8^2 + 6^2 = 100$$<br>Suy ra $BD = \\sqrt{100} = 10\\text{ (cm)}$.<br><br>2) Xét $\\Delta AHB$ (vuông tại $H$) và $\\Delta BCD$ (vuông tại $C$) có:<br>$$\\widehat{ABH} = \\widehat{BDC}\\text{ (hai góc so le trong do }AB \\parallel CD\\text{)}$$<br>Do đó $\\Delta AHB \\backsim \\Delta BCD$ (góc nhọn).<br><br>3) Vì $\\Delta AHB \\backsim \\Delta BCD$ nên:<br>$$\\frac{AH}{BC} = \\frac{AB}{BD} \\Rightarrow AH = \\frac{AB \\cdot BC}{BD} = \\frac{8 \\cdot 6}{10} = 4{,}8\\text{ (cm)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tính diện tích tam giác $AHB$ và so sánh với diện tích hình chữ nhật $ABCD$.
b) Nội dung: Tính $S_{\\Delta AHB}$ khi đã biết $AH = 4{,}8\\text{ cm}$ và $BH = \\sqrt{8^2 - 4{,}8^2} = 6{,}4\\text{ cm}$.
c) Sản phẩm: Kết quả $S = \\frac{1}{2} \\cdot 4{,}8 \\cdot 6{,}4 = 15{,}36\\text{ cm}^2$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn tính $BH$ bằng Pythagore và tính diện tích tam giác vuông $AHB$.<br>- **HS:** Thực hiện tính toán nhanh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $BH = 6{,}4\\text{ cm}$, $S_{\\Delta AHB} = 15{,}36\\text{ cm}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo kết quả miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá và giao bài tập ôn tập chuẩn bị cuối chương IX. | Vận dụng tính diện tích tam giác vuông từ đường cao và hình chiếu. |
"""
    },

    # 35: Tiết 44: Bài tập cuối chương IX (Mindmap: mindmap_toan8_hinh_tiet44.png)
    {
        "filename": "35_KHBD_Toan8_BaiTapCuoiChuong9_Tiet44.md",
        "md": """TIẾT 44 - BÀI TẬP CUỐI CHƯƠNG IX
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập toàn diện kiến thức Chương IX: Tam giác đồng dạng:
  + Định nghĩa, tính chất, tỉ số đồng dạng.
  + Định lí tạo thành tam giác đồng dạng.
  + Ba trường hợp đồng dạng của tam giác (c.c.c, c.g.c, g.g).
  + Định lí Pythagore thuận và đảo.
  + Các trường hợp đồng dạng của tam giác vuông.
  + Hình đồng dạng phối cảnh.
- Rèn luyện kỹ năng giải các bài toán tổng hợp cuối chương.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tổng kết kiến thức toàn bộ chương IX dưới dạng sơ đồ tư duy hoàn chỉnh.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp giải hình học khác nhau.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng phân tích hình phức tạp thành các tam giác đồng dạng quen thuộc.
- Năng lực giải quyết vấn đề toán học: Hoàn thành bài tập trắc nghiệm và tự luận tổng kết chương.

## 3. Về phẩm chất
- Rèn luyện thói quen tự kiểm tra bài làm, vẽ hình cẩn thận, kí hiệu đầy đủ.
- Tinh thần nghiêm túc, sẵn sàng cho bài kiểm tra giữa học kì II sắp tới.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI Chương IX, bảng phụ các câu hỏi trắc nghiệm ôn tập.
2. Học sinh: SGK, vở ghi, dụng cụ vẽ hình đầy đủ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khởi động ôn tập bằng trò chơi ô chữ toán học liên quan đến các từ khóa của chương IX.
b) Nội dung: Giải ô chữ với các từ khóa: ĐỒNG DẠNG, PYTHAGORE, PHỐI CẢNH, TỈ LỆ THỨC.
c) Sản phẩm: Các từ khóa được học sinh giải mã chính xác.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu các câu hỏi gợi ý để tìm từ khóa trọng tâm của Chương IX.<br>- **HS:** Hào hứng tham gia.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời các câu hỏi về tam giác đồng dạng và định lí Pythagore.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát hiện từ khóa hàng dọc: HÌNH HỌC ĐỒNG DẠNG.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang sơ đồ tư duy tổng kết toàn chương. | Khởi động: Nhận diện các từ khóa cốt lõi của Chương IX. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Tổng kết Chương IX bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Khái quát toàn bộ cấu trúc kiến thức Chương IX: Tam giác đồng dạng.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI tổng kết Chương IX.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Bài tập cuối chương IX Tiết 44](khbd-ill:mindmap-toan8-hinh-tiet44)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy 300 DPI tổng kết toàn bộ Chương IX. Yêu cầu HS nêu mối liên hệ giữa các phần kiến thức.<br>- **HS:** Theo dõi và quan sát sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích: Từ Định nghĩa $\\rightarrow$ Định lí tạo tam giác đồng dạng $\\rightarrow$ Ba trường hợp đồng dạng $\\rightarrow$ Định lí Pythagore $\\rightarrow$ Tam giác vuông đồng dạng $\\rightarrow$ Hình đồng dạng phối cảnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trình bày tổng quan chương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ và nhấn mạnh các dạng toán điển hình. | **Tổng kết toàn bộ Chương IX:**<br>1. Định nghĩa và tính chất hai tam giác đồng dạng.<br>2. Ba trường hợp đồng dạng (c.c.c, c.g.c, g.g).<br>3. Định lí Pythagore và định lí đảo.<br>4. Các trường hợp đồng dạng của tam giác vuông.<br>5. Hình đồng dạng phối cảnh và ứng dụng. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài tập tổng hợp cuối chương trong SGK Toán 8 Tập 2.
b) Nội dung: Cho tam giác nhọn $ABC$, các đường cao $BD$ và $CE$ cắt nhau tại $H$.
1) Chứng minh $\\Delta ABD \\backsim \\Delta ACE$.
2) Chứng minh $HD \\cdot HB = HE \\cdot HC$.
3) Chứng minh $\\Delta ADE \\backsim \\Delta ABC$.
c) Sản phẩm: Lời giải hoàn chỉnh 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập hình học tổng hợp với hai đường cao cắt nhau tại trực tâm $H$.<br>- **HS:** Vẽ hình cẩn thận vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** 1) Xét hai tam giác vuông có góc $A$ chung.<br>2) Xét $\\Delta HED \\backsim \\Delta HCD$ hoặc $\\Delta HEB \\backsim \\Delta HDC$.<br>3) Dùng tỉ số $\\frac{AD}{AC} = \\frac{AE}{AB}$ và góc $A$ chung.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lần lượt lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, đánh giá lập luận chặt chẽ và chuẩn hóa bài giải. | **Bài giải:**<br>1) Xét $\\Delta ABD$ (vuông tại $D$) và $\\Delta ACE$ (vuông tại $E$) có:<br>$$\\widehat{A}\\text{ chung}$$<br>Do đó $\\Delta ABD \\backsim \\Delta ACE$ (góc nhọn).<br><br>2) Xét $\\Delta HEB$ (vuông tại $E$) và $\\Delta HDC$ (vuông tại $D$) có:<br>$$\\widehat{EHB} = \\widehat{DHC}\\text{ (đối đỉnh)}$$<br>Do đó $\\Delta HEB \\backsim \\Delta HDC$ (góc nhọn).<br>Suy ra:<br>$$\\frac{HE}{HD} = \\frac{HB}{HC} \\Rightarrow HD \\cdot HB = HE \\cdot HC$$<br><br>3) Từ câu 1, ta có $\\frac{AD}{AC} = \\frac{AE}{AB}$.<br>Xét $\\Delta ADE$ và $\\Delta ABC$ có:<br>- $\\widehat{A}$ chung;<br>- $\\frac{AD}{AB} = \\frac{AE}{AC}$ (suy ra từ $\\frac{AD}{AC} = \\frac{AE}{AB}$).<br>Vậy $\\Delta ADE \\backsim \\Delta ABC$ (c.g.c). |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Hướng dẫn học sinh chuẩn bị cho tiết hoạt động thực hành trải nghiệm ngoài trời tiếp theo.
b) Nội dung: Giới thiệu dụng cụ đo góc (giác kế), thước dây và phân công nhiệm vụ nhóm cho tiết thực hành trải nghiệm.
c) Sản phẩm: Bảng phân công nhiệm vụ và chuẩn bị dụng cụ của các tổ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị cho tiết 45: Hoạt động thực hành trải nghiệm đo chiều cao cột cờ và khoảng cách hai điểm.<br>- **HS:** Ghi chép phân công dụng cụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Các tổ trưởng nhận nhiệm vụ chuẩn bị giác kế, thước cuộn, cọc tiêu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các tổ trưởng báo cáo danh sách dụng cụ đã chuẩn bị.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở quy tắc an toàn ngoài trời và tinh thần hợp tác. | Phân công chuẩn bị dụng cụ cho tiết thực hành trải nghiệm ngoài trời. |
"""
    },

    # 36: Tiết 45: HĐTN Đo chiều cao khoảng cách
    {
        "filename": "36_KHBD_Toan8_HDTN_DoChieuCaoKhoangCach_Tiet45.md",
        "md": """TIẾT 45 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: ỨNG DỤNG ĐỊNH LÍ THALES, ĐỊNH LÍ PYTHAGORE VÀ TAM GIÁC ĐỒNG DẠNG ĐỂ ĐO CHIỀU CAO, KHOẢNG CÁCH
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng phối hợp định lí Thalès, định lí Pythagore và các trường hợp đồng dạng của tam giác để giải quyết các bài toán đo đạc thực tế:
  + Đo chiều cao của một vật không tới được đỉnh (cột cờ trường học, cây bóng mát).
  + Đo khoảng cách giữa hai điểm trong đó có một điểm không tới được (khoảng cách qua sông, qua hồ nước).
- Rèn luyện kỹ năng sử dụng giác kế, thước cuộn và ghi chép số liệu đo thực địa.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Chủ động thực hiện thao tác ngắm giác kế và đọc số đo góc, ghi chép số liệu trung thực.
- Giao tiếp và hợp tác: Làm việc nhóm phân công vai trò rõ ràng (người ngắm, người giữ cọc tiêu, người kéo thước đo, người ghi biên bản).

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Chuyển đổi không gian thực địa thành mô hình tam giác vuông đồng dạng trên mặt phẳng giấy.
- Năng lực giải quyết vấn đề toán học: Tính toán số học từ số liệu đo thực nghiệm, tính sai số đo đạc.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS lựa chọn ứng dụng đo đạc trên điện thoại thay cho công cụ cũ; 2.1.TC2b: HS lựa chọn phương tiện số phù hợp ghi lại kết quả đo thực địa; 4.3.TC2b: HS thảo luận cách bảo vệ sức khỏe khi dùng công nghệ ngoài trời.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS trình bày cách AI "nhìn" để đo khoảng cách không tới được từ ảnh chụp camera; HS hiểu cách AI nhận diện các mẫu (pattern) để thực hiện chức năng phóng to/thu nhỏ hình ảnh; 8.A3.2: HS giải thích trách nhiệm cá nhân khi sử dụng kết quả từ AI đo đạc vào thực tế xây dựng; 8.B2.1: HS đề xuất các biện pháp giảm thiểu rủi ro khi chia sẻ vị trí GPS cho ứng dụng đo đạc AI.***

## 3. Về phẩm chất
- Tinh thần trách nhiệm, kỷ luật cao khi thực hành ngoài trời.
- Trung thực, khách quan với số liệu đo đạc thực tế.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Giác kế đứng, thước dây (thước cuộn $20\\text{ m}$), cọc tiêu, phiếu ghi biên bản thực hành trải nghiệm, bài hướng dẫn an toàn ngoài trời.
2. Học sinh: Giác kế cầm tay của nhóm, thước kẻ, máy tính cầm tay, điện thoại thông minh (nếu được phép) cài ứng dụng đo góc/thước đo laser, mũ nón bảo hộ.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ GIAO NHIỆM VỤ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Xác định nhiệm vụ thực hành đo chiều cao cột cờ sân trường và phổ biến quy chế an toàn ngoài sân.
b) Nội dung: Các nhóm nhận phiếu học tập thực địa và dụng cụ đo đạc.
c) Sản phẩm: Đội hình các nhóm xếp hàng sẵn sàng ra sân trường.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu mục tiêu buổi thực hành: Mỗi nhóm đo chiều cao cột cờ trường học bằng 2 phương pháp: Phương pháp cọc bóng nắng và Phương pháp giác kế ngắm đỉnh.<br>- **HS:** Nhận phiếu học tập và kiểm tra dụng cụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm trưởng phân công nhiệm vụ cụ thể cho từng thành viên.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các nhóm trưởng xác nhận đã đủ dụng cụ và hiểu rõ nhiệm vụ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở quy tắc an toàn và hiệu lệnh di chuyển ra sân trường. | Phổ biến mục tiêu, dụng cụ và phân công nhiệm vụ thực hành thực địa. |

## B. TIẾN HÀNH THỰC HÀNH NGOÀI TRỜI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Đo chiều cao cột cờ bằng giác kế (15 phút)
a) Mục tiêu: Vận dụng giác kế đo góc nâng $\\alpha$, đo khoảng cách từ chân giác kế đến chân cột cờ, tính chiều cao cột cờ.
b) Nội dung: Đặt giác kế tại điểm $C$ cách chân cột cờ $B$ một đoạn $d = 10\\text{ m}$. Ngắm đỉnh cột cờ $A$ được góc $\\alpha = 35^\\circ$. Chiều cao giác kế $CD = h = 1{,}5\\text{ m}$. Tính chiều cao $AB$.
c) Sản phẩm: Số liệu đo góc và khoảng cách trong biên bản thực hành của từng nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn các nhóm đặt giác kế thẳng đứng, cân chỉnh bọt thủy, ngắm ống ngắm tới đỉnh cột cờ $A$. Đọc góc $\\alpha$ trên giác kế. Dùng thước cuộn đo khoảng cách $BC = d$.<br>- **HS:** Tiến hành thao tác tại vị trí được phân công.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm 1 ngắm được góc $\\alpha$, đo khoảng cách $d$, ghi số liệu vào biên bản.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Thư ký các nhóm ghi nhận số đo lần 1, lần 2 và lấy giá trị trung bình.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Quan sát, hỗ trợ các nhóm thao tác ngắm chuẩn xác và đảm bảo an toàn. | **Mô hình tính toán:**<br>Gọi $D$ là đỉnh giác kế, $C$ là chân giác kế. Kẻ $DH \\perp AB$ tại $H$.<br>Ta có $DH = BC = d$, $HB = CD = h$.<br>Trong $\\Delta ADH$ vuông tại $H$:<br>$$AH = DH \\cdot \\tan \\alpha = d \\cdot \\tan \\alpha$$<br>Chiều cao cột cờ là:<br>$$AB = AH + HB = d \\cdot \\tan \\alpha + h$$ |

### Hoạt động 2.2: Ứng dụng công nghệ số và AI đo khoảng cách (10 phút)
a) Mục tiêu: Tích hợp công nghệ đo đạc thông minh qua camera điện thoại (AR / AI đo khoảng cách) và đối chiếu với phương pháp hình học truyền thống.
b) Nội dung: Sử dụng ứng dụng AR Measure trên điện thoại (sử dụng AI nhận diện mặt phẳng và góc nghiêng camera) để đo trực tiếp chiều cao và khoảng cách.
c) Sản phẩm: Ảnh chụp màn hình số đo AI và so sánh với số đo giác kế truyền thống.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho phép đại diện các nhóm mở ứng dụng AR Measure trên điện thoại. Hướng camera vào cột cờ và đọc số đo AI hiển thị.<br>- **HS:** Thực hiện thao tác công nghệ số.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nguyên lí: AI nhận diện đáy và đỉnh vật thể thông qua xử lý ảnh camera và cảm biến gia tốc để tính chiều cao.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** So sánh số liệu đo bằng giác kế và số liệu do app AI tính.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét sự tiện lợi của công nghệ AI và nhắc nhở ý thức bảo mật dữ liệu GPS khi dùng ứng dụng. | Tích hợp NLS và AI: Tìm hiểu nguyên lí AI đo khoảng cách qua camera và so sánh độ chính xác với phương pháp hình học. |

## C. BÁO CÁO KẾT QUẢ VÀ TÍNH TOÁN (HOẠT ĐỘNG 3) (10 phút)
a) Mục tiêu: Tính toán kết quả chiều cao cột cờ từ số liệu thu thập được và hoàn thành biên bản.
b) Nội dung: Thay số liệu trung bình vào công thức và tính chiều cao cột cờ.
c) Sản phẩm: Báo cáo thực hành hoàn chỉnh của 4 tổ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các tổ về phòng học, hoàn thiện tính toán và điền kết quả vào bảng tổng hợp.<br>- **HS:** Bấm máy tính tính toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ví dụ số liệu: $d = 10\\text{ m}, \\alpha = 38^\\circ, h = 1{,}5\\text{ m}$.<br>$$AH = 10 \\cdot \\tan 38^\\circ \\approx 10 \\cdot 0{,}7813 = 7{,}81\\text{ m}$$<br>$$AB = 7{,}81 + 1{,}5 = 9{,}31\\text{ m}$$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 4 tổ nộp biên bản và trình bày kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** So sánh kết quả các tổ, công bố chiều cao thiết kế thực tế của cột cờ ($9{,}5\\text{ m}$) và đánh giá sai số của từng tổ. | **Biên bản báo cáo kết quả:**<br>- Số liệu đo góc: $\\alpha \\approx 38^\\circ$.<br>- Khoảng cách: $d = 10\\text{ m}$.<br>- Chiều cao giác kế: $h = 1{,}5\\text{ m}$.<br>- Kết quả tính toán: Chiều cao cột cờ xấp xỉ $9{,}3\\text{ m} - 9{,}5\\text{ m}$. |

## D. ĐÁNH GIÁ VÀ TỔNG KẾT (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tổng kết hoạt động thực hành, đánh giá tinh thần làm việc nhóm và ý nghĩa thực tiễn của toán học.
b) Nội dung: Nhận xét tinh thần thái độ, chấm điểm báo cáo của các tổ.
c) Sản phẩm: Bảng điểm đánh giá hoạt động trải nghiệm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nhận xét chung về buổi học: Tinh thần kỷ luật, sự hợp tác và độ chính xác của số liệu.<br>- **HS:** Lắng nghe và tự rút kinh nghiệm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Các tổ tự chấm điểm thành viên theo mức độ đóng góp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các nhóm trưởng nộp bảng tự đánh giá.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương các nhóm làm việc xuất sắc, dặn dò chuẩn bị cho tiết ôn tập giữa kì tiếp theo. | Đánh giá tổng kết hoạt động thực hành trải nghiệm hình học ngoài trời. |
"""
    },

    # 37: Tiết 46: Ôn tập giữa HK2 Hình học (Mindmap: mindmap_toan8_hinh_tiet46.png)
    {
        "filename": "37_KHBD_Toan8_OnTapGiuaHK2_HinhHoc_Tiet46.md",
        "md": """TIẾT 46 - ÔN TẬP GIỮA HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Hình học trọng tâm nửa đầu Học kì II (Chương IX: Tam giác đồng dạng):
  + Định nghĩa, tính chất và các trường hợp đồng dạng của hai tam giác thường (c.c.c, c.g.c, g.g).
  + Định lí Pythagore thuận và định lí Pythagore đảo.
  + Các trường hợp đồng dạng của hai tam giác vuông.
  + Các bài toán tính toán cạnh, tỉ số diện tích và chứng minh hệ thức hình học.
- Chuẩn bị đầy đủ kiến thức và kỹ năng cho bài Kiểm tra đánh giá giữa Học kì II (Tiết 47).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự ôn luyện lại các định lí, tính chất và xem lại các dạng bài tập trọng tâm.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải và sửa lỗi sai cho nhau trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Trình bày bài toán hình học có lập luận chặt chẽ, có căn cứ định lí rõ ràng.
- Năng lực giải quyết vấn đề toán học: Phân bổ thời gian hợp lí khi giải quyết bài toán hình học giữa kì.

## 3. Về phẩm chất
- Cẩn thận, chính xác trong từng bước suy luận hình học.
- Tự tin, nghiêm túc trước kì kiểm tra đánh giá giữa kì.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2, KHBD, đề cương ôn tập giữa HK2 phần Hình học, sơ đồ tư duy vector 300 DPI, máy chiếu.
2. Học sinh: SGK, vở ghi, dụng cụ vẽ hình đầy đủ, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tạo tâm thế tập trung và rà soát nhanh ma trận đề kiểm tra giữa kì phần hình học.
b) Nội dung: GV giới thiệu cấu trúc điểm phần hình học trong đề kiểm tra giữa HK2 (chiếm khoảng 30% - 35% tổng số điểm toàn đề).
c) Sản phẩm: HS nắm rõ cấu trúc đề thi để có chiến lược làm bài hiệu quả.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu ma trận đề thi giữa kì phần hình học: Gồm các câu hỏi nhận biết định nghĩa tam giác đồng dạng, thông hiểu định lí Pythagore và vận dụng chứng minh tam giác đồng dạng, tính độ dài đoạn thẳng.<br>- **HS:** Lắng nghe và ghi chú trọng tâm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trao đổi cặp đôi về các định lí hay nhầm lẫn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu lại các công thức cần nhớ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuyển sang phần sơ đồ tư duy ôn tập tổng quát. | Nắm vững ma trận và định hướng ôn tập kiểm tra giữa HK2 Hình học. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Hình học giữa HK2 bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ các định lí then chốt của Chương IX bằng sơ đồ tư duy 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI ôn tập giữa HK2 Hình học.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Ôn tập giữa HK2 Hình học Tiết 46](khbd-ill:mindmap-toan8-hinh-tiet46)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Ôn tập giữa HK2 Hình học. Yêu cầu HS phân tích các nhánh kiến thức chính.<br>- **HS:** Quan sát và nhắc lại các định lí trọng tâm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 3 nhánh lớn:<br>1) Các trường hợp đồng dạng tam giác thường (c.c.c, c.g.c, g.g).<br>2) Định lí Pythagore và định lí đảo.<br>3) Các trường hợp đồng dạng tam giác vuông và ứng dụng đo đạc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS nhắc lại cách phân biệt trường hợp c.g.c của tam giác thường và cạnh huyền - cạnh góc vuông của tam giác vuông.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại những lỗi thường gặp: Thiếu điều kiện góc xen giữa, quên giải thích lí do góc bằng nhau. | **Hệ thống kiến thức ôn tập giữa HK2:**<br>1. Tam giác đồng dạng: 3 trường hợp đồng dạng c.c.c, c.g.c, g.g.<br>2. Định lí Pythagore: $c^2 = a^2 + b^2$ và định lí đảo nhận biết tam giác vuông.<br>3. Tam giác vuông đồng dạng: Góc nhọn, hai cạnh góc vuông, cạnh huyền - cạnh góc vuông.<br>4. Phương pháp tính đoạn thẳng và chứng minh hệ thức hình học. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài tập mẫu sát với cấu trúc đề kiểm tra giữa kì.
b) Nội dung: Cho tam giác $ABC$ vuông tại $A$ ($AB < AC$), đường cao $AH$.
1) Chứng minh $\\Delta HBA \\backsim \\Delta ABC$.
2) Cho $AB = 6\\text{ cm}, BC = 10\\text{ cm}$. Tính $AC, AH, BH$.
3) Trên cạnh $AC$ lấy điểm $E$ sao cho $AE = 3\\text{ cm}$. Kẻ $EK \\perp BC$ tại $K$. Chứng minh $CK \\cdot CB = CE \\cdot CA$.
c) Sản phẩm: Lời giải mẫu chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập hình học tổng hợp sát cấu trúc đề kiểm tra.<br>- **HS:** Vẽ hình chính xác vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện giải từng câu:<br>Câu 1: Chứng minh đồng dạng theo trường hợp góc nhọn.<br>Câu 2: Tính $AC$ theo Pythagore, tính $AH$ và $BH$ theo tỉ số đồng dạng.<br>Câu 3: Chứng minh $\\Delta CKE \\backsim \\Delta CAB$ (góc nhọn).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, lưu ý cách trình bày chặt chẽ để đạt điểm tối đa. | **Bài giải:**<br>1) Xét $\\Delta HBA$ (vuông tại $H$) và $\\Delta ABC$ (vuông tại $A$) có:<br>$$\\widehat{B}\\text{ chung}$$<br>Do đó $\\Delta HBA \\backsim \\Delta ABC$ (góc nhọn).<br><br>2) Áp dụng định lí Pythagore vào $\\Delta ABC$ vuông tại $A$:<br>$$AC = \\sqrt{BC^2 - AB^2} = \\sqrt{10^2 - 6^2} = 8\\text{ (cm)}$$<br>Vì $\\Delta HBA \\backsim \\Delta ABC$ nên:<br>$$\\frac{HA}{AC} = \\frac{BA}{BC} = \\frac{HB}{AB}$$<br>Suy ra:<br>$$AH = \\frac{AB \\cdot AC}{BC} = \\frac{6 \\cdot 8}{10} = 4{,}8\\text{ (cm)}$$<br>$$BH = \\frac{AB^2}{BC} = \\frac{6^2}{10} = 3{,}6\\text{ (cm)}$$<br><br>3) Xét $\\Delta CKE$ (vuông tại $K$) và $\\Delta CAB$ (vuông tại $A$) có:<br>$$\\widehat{C}\\text{ chung}$$<br>Do đó $\\Delta CKE \\backsim \\Delta CAB$ (góc nhọn).<br>Suy ra:<br>$$\\frac{CK}{CA} = \\frac{CE}{CB} \\Rightarrow CK \\cdot CB = CE \\cdot CA$$ |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Hướng dẫn học sinh phương pháp chuẩn bị tâm lí và dụng cụ cho tiết kiểm tra giữa kì.
b) Nội dung: Dặn dò chuẩn bị đầy đủ thước kẻ, eke, compa, bút viết, máy tính cầm tay cho tiết kiểm tra tiếp theo.
c) Sản phẩm: Học sinh ghi nhận đầy đủ yêu cầu dặn dò.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò ôn kĩ lí thuyết và các dạng bài tập đã ôn, chuẩn bị đầy đủ dụng cụ vẽ hình.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự kiểm tra lại đồ dùng học tập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Hỏi thêm những điểm còn băn khoăn về cách trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chúc các em ôn tập tốt và làm bài đạt kết quả cao. | Dặn dò chuẩn bị cho tiết Kiểm tra giữa Học kì II. |
"""
    },

    # 38: Tiết 47: Kiểm tra giữa HK2 Hình học
    {
        "filename": "38_KHBD_Toan8_KiemTraGiuaHK2_HinhHoc_Tiet47.md",
        "md": """TIẾT 47 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ đạt chuẩn kiến thức kĩ năng của học sinh trong nửa đầu Học kì II môn Toán 8 (phần Hình học - Chương IX: Tam giác đồng dạng):
  + Nhận biết các trường hợp đồng dạng của tam giác thường và tam giác vuông.
  + Vận dụng định lí Pythagore và định lí Pythagore đảo.
  + Chứng minh hai tam giác đồng dạng, tính độ dài đoạn thẳng và chứng minh hệ thức hình học.
- Đánh giá khả năng vẽ hình chính xác và trình bày bài toán hình học khoa học.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác, nghiêm túc làm bài kiểm tra, không trao đổi hoặc sử dụng tài liệu.
- Giải quyết vấn đề: Phân tích đề bài, lựa chọn phương pháp chứng minh và tính toán chính xác.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng lập luận logic, suy diễn hình học chặt chẽ.
- Năng lực tính toán: Tính toán chính xác độ dài cạnh, căn bậc hai và làm tròn số.

## 3. Về phẩm chất
- Trung thực, thẳng thắn trong kiểm tra đánh giá.
- Rèn tính cẩn trọng, kỷ luật và tinh thần vượt khó.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo đúng ma trận và đặc tả đề kiểm tra giữa kì, đáp án và biểu điểm chi tiết.
2. Học sinh: Dụng cụ vẽ hình (thước thẳng có chia vạch, eke, compa), máy tính cầm tay, bút mực, bút chì.

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
### Ma trận và Đề bài kiểm tra Hình học giữa HK2 (35 phút)
a) Mục tiêu: Học sinh độc lập vận dụng toàn diện kiến thức Chương IX để hoàn thành bài kiểm tra.
b) Nội dung: Đề kiểm tra gồm 2 phần: Trắc nghiệm khách quan (3 điểm) và Tự luận (7 điểm).
c) Sản phẩm: Bài làm hoàn chỉnh trên giấy kiểm tra của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Làm bài độc lập**<br>- **HS:** Đọc kĩ đề, vẽ hình nháp, làm bài tự luận theo từng câu từ dễ đến khó.<br>- **GV:** Quan sát, bao quát lớp, giữ trật tự nghiêm túc tuyệt đối.<br><br>**+ Bước 2: Hướng dẫn giám sát**<br>- **GV:** Thông báo thời gian còn lại (còn 15 phút, còn 5 phút).<br>- **HS:** Kiểm tra lại bài làm, rà soát tên đỉnh tam giác tương ứng, soát lỗi tính toán.<br><br>**+ Bước 3: Hoàn thành bài làm**<br>- **HS:** Đếm số tờ giấy thi, chuẩn bị nộp bài.<br><br>**+ Bước 4: Hết giờ**<br>- **GV:** Ra hiệu lệnh hết giờ làm bài, yêu cầu tất cả HS dừng bút. | **Nội dung Đề kiểm tra minh họa:**<br>**Phần I. Trắc nghiệm (3 điểm):**<br>- Câu 1: Điều kiện hai tam giác đồng dạng.<br>- Câu 2: Tỉ số diện tích hai tam giác đồng dạng bằng bình phương tỉ số đồng dạng.<br>- Câu 3: Định lí Pythagore tính cạnh huyền tam giác vuông $3\\text{ cm}, 4\\text{ cm} \\Rightarrow 5\\text{ cm}$.<br><br>**Phần II. Tự luận (7 điểm):**<br>Cho tam giác $ABC$ vuông tại $A$ ($AB = 9\\text{ cm}, AC = 12\\text{ cm}$), đường cao $AH$.<br>a) (2,0 điểm) Tính độ dài cạnh $BC$ và $AH$.<br>b) (3,0 điểm) Chứng minh $\\Delta HBA \\backsim \\Delta ABC$ và suy ra $AB^2 = BH \\cdot BC$. Tính độ dài $BH$.<br>c) (2,0 điểm) Kẻ tia phân giác của $\\widehat{ABC}$ cắt $AH$ tại $D$ và cắt $AC$ tại $E$. Chứng minh $\\frac{DA}{DH} = \\frac{EC}{EA}$. |

## C. THU BÀI VÀ ĐÁNH GIÁ Ý THỨC LÀM BÀI (HOẠT ĐỘNG 3) (5 phút)
a) Mục tiêu: Thu bài kiểm tra đầy đủ, kiểm tra khớp số lượng bài và nhận xét ý thức làm bài của học sinh.
b) Nội dung: GV thu bài theo từng bàn, đếm đủ số bài thi và nhận xét tinh thần phòng thi.
c) Sản phẩm: Đủ 100% bài kiểm tra của cả lớp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các tổ trưởng thu bài theo thứ tự số báo danh.<br>- **HS:** Nộp bài nghiêm túc, không đứng lên lộn xộn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm tổng số bài kiểm tra khớp với sĩ số lớp học.<br><br>**+ Bước 3: Nhận xét giờ kiểm tra**<br>- **GV:** Nhận xét tinh thần, thái độ làm bài của học sinh: Đa số nghiêm túc, làm bài tập trung; nhắc nhở một số em vẽ hình chưa dùng thước chuẩn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Hướng dẫn sơ bộ đáp án và dặn dò tiết học tiếp theo (bắt đầu Chương X: Một số hình khối trong thực tiễn). | Thu đủ số bài kiểm tra và nhận xét nền nếp kiểm tra. |
"""
    },
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print(f"Hoàn tất tạo đợt 1 (11 bài Chương IX Tiết 32 - 47)!")
