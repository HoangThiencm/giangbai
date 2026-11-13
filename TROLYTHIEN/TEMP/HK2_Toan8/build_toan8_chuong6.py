# -*- coding: utf-8 -*-
"""
Script sinh 7 KHBD Chương VI: Phân thức đại số (Tiết 42 - 54) - Toán 8 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan8"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    {
        "filename": "01_KHBD_Toan8_Bai21_PhanThucDaiSo_Tiet42-43.md",
        "header": "TIẾT 42, 43 - BÀI 21: PHÂN THỨC ĐẠI SỐ\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 42, 43 - BÀI 21: PHÂN THỨC ĐẠI SỐ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết định nghĩa phân thức đại số: Biểu thức có dạng $\\frac{A}{B}$, trong đó $A, B$ là những đa thức và đa thức $B$ khác đa thức không.
- Xác định được điều kiện xác định của phân thức đại số: Đa thức ở mẫu phải khác $0$ ($B \\neq 0$).
- Tính được giá trị của phân thức đại số tại giá trị của biến thỏa mãn điều kiện xác định.
- Nắm vững khái niệm hai phân thức bằng nhau: $\\frac{A}{B} = \\frac{C}{D}$ nếu $A \\cdot D = B \\cdot C$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tìm điều kiện xác định của phân thức và thay số tính giá trị cẩn thận.
- Giao tiếp và hợp tác: Thảo luận nhóm giải thích vì sao hai phân thức bằng nhau thông qua tích chéo.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh tích chéo $A \\cdot D$ và $B \\cdot C$ bằng các quy tắc nhân đa thức.
- Năng lực mô hình hoá toán học: Sử dụng phân thức đại số để biểu diễn thời gian hoàn thành công việc theo năng suất.

c) Năng lực số (NLS):
- ***1.1.TC2a: HS tìm ví dụ thực tế về phân thức trong các công thức kinh tế trên mạng Internet; 5.2.TC2b: HS lựa chọn công cụ số để kiểm tra giá trị của phân thức tại một biến số.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS hiểu cách AI phân tích biểu thức đại số để tự động phát hiện điều kiện xác định của mẫu thức.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác khi biến đổi các đa thức và đặt điều kiện cho mẫu.
- Tinh thần trách nhiệm, tích cực đóng góp trong thảo luận nhóm.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, máy chiếu, bảng phụ ghi bài tập.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Đặt vấn đề biểu diễn thời gian một chiếc cano xuôi dòng và ngược dòng bằng biểu thức đại số có chứa biến ở mẫu.
b) Nội dung: Một cano xuôi dòng quãng đường $30\\text{ km}$ với vận tốc thực $v\\text{ km/h}$, vận tốc dòng nước $3\\text{ km/h}$. Biểu diễn thời gian cano xuôi dòng.
c) Sản phẩm: Biểu thức $\\frac{30}{v + 3}$ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Một cano xuôi dòng quãng đường $30\\text{ km}$ với vận tốc riêng $v\\text{ (km/h)}$, vận tốc dòng nước $3\\text{ (km/h)}$. Hãy viết biểu thức biểu thị thời gian cano đi hết quãng đường đó.<br>- **HS:** Nhận đề và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vận tốc xuôi dòng là $v + 3$. Thời gian đi là: $\\frac{30}{v + 3}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Biểu thức có chứa biến ở mẫu số.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu bài mới: Biểu thức dạng $\\frac{30}{v + 3}$ được gọi là một phân thức đại số. | Biểu thức $\\frac{30}{v + 3}$ là một phân thức đại số với tử thức là $30$ và mẫu thức là đa thức $v + 3$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Khái niệm phân thức đại số và điều kiện xác định (35 phút)
a) Mục tiêu: Nắm vững định nghĩa phân thức $\\frac{A}{B}$ ($B \\neq 0$) và tìm điều kiện xác định của phân thức.
b) Nội dung: Định nghĩa, tử thức, mẫu thức và điều kiện mẫu thức khác đa thức không.
c) Sản phẩm: Vở ghi bài và lời giải bài tập tìm điều kiện xác định.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa: Một phân thức đại số (hay phân thức) là một biểu thức có dạng $\\frac{A}{B}$, trong đó $A, B$ là những đa thức và $B$ khác đa thức không. $A$ là tử thức, $B$ là mẫu thức. Điều kiện xác định của phân thức $\\frac{A}{B}$ là $B \\neq 0$.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tìm điều kiện xác định của phân thức $P = \\frac{x + 1}{x - 2}$ và tính giá trị của $P$ tại $x = 3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** ĐKXĐ: $x - 2 \\neq 0$ suy ra $x \\neq 2$. Tại $x = 3$ (thỏa mãn ĐK), giá trị của $P = \\frac{3 + 1}{3 - 2} = 4$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Chỉ tính được giá trị của phân thức tại các giá trị của biến thỏa mãn điều kiện xác định. | **1. Phân thức đại số:**<br>- Biểu thức có dạng $\\frac{A}{B}$ với $A, B$ là đa thức, $B \\neq 0$.<br>- ĐKXĐ: Mẫu thức khác $0$ ($B \\neq 0$).<br>- Mỗi đa thức cũng được coi là một phân thức với mẫu thức bằng $1$: $A = \\frac{A}{1}$. |

### Hoạt động 2.2: Hai phân thức bằng nhau (30 phút)
a) Mục tiêu: Nắm vững quy tắc hai phân thức bằng nhau: $\\frac{A}{B} = \\frac{C}{D}$ nếu $A \\cdot D = B \\cdot C$.
b) Nội dung: Kiểm tra tích chéo $A \\cdot D$ và $B \\cdot C$.
c) Sản phẩm: Lời giải các bài tập kiểm tra tính bằng nhau trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc: Hai phân thức $\\frac{A}{B}$ và $\\frac{C}{D}$ gọi là bằng nhau nếu $A \\cdot D = B \\cdot C$. Ta viết $\\frac{A}{B} = \\frac{C}{D}$. Yêu cầu kiểm tra: $\\frac{x - 1}{x^2 - 1} = \\frac{1}{x + 1}$.<br>- **HS:** Thực hiện tính tích chéo.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính tích: $(x - 1)(x + 1) = x^2 - 1$. Tích thứ hai: $(x^2 - 1) \\cdot 1 = x^2 - 1$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Vì $(x - 1)(x + 1) = (x^2 - 1) \\cdot 1$ nên hai phân thức bằng nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định quy tắc tích chéo áp dụng tương tự như phân số số học. | **2. Hai phân thức bằng nhau:**<br>- Ta có: $\\frac{A}{B} = \\frac{C}{D}$ nếu $A \\cdot D = B \\cdot C$.<br>- Ví dụ: $\\frac{x - 1}{x^2 - 1} = \\frac{1}{x + 1}$ vì $(x - 1)(x + 1) = x^2 - 1$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Rèn luyện kỹ năng tìm điều kiện xác định và kiểm tra các cặp phân thức bằng nhau.
b) Nội dung: Bài 6.1, 6.2 SGK trang 7.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tìm điều kiện xác định của phân thức: $Q = \\frac{2x - 3}{x^2 - 9}$.<br>- **HS:** Nhận đề và phân tích mẫu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cho mẫu khác $0$: $x^2 - 9 \\neq 0 \\Rightarrow (x - 3)(x + 3) \\neq 0 \\Rightarrow x \\neq 3$ và $x \\neq -3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao việc áp dụng hằng đẳng thức hiệu hai bình phương để tìm điều kiện xác định. | **Bài giải:**<br>Điều kiện xác định của phân thức $Q$ là:<br>$$x^2 - 9 \\neq 0$$<br>$$(x - 3)(x + 3) \\neq 0$$<br>Suy ra $x \\neq 3$ và $x \\neq -3$.<br>Vậy điều kiện xác định của phân thức là $x \\neq 3$ và $x \\neq -3$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng phân thức đại số mô hình hóa bài toán kinh tế chi phí sản xuất trung bình một sản phẩm.
b) Nội dung: Chi phí sản xuất $x$ sản phẩm là $C(x) = 5000x + 100\\,000$ (đồng). Viết phân thức biểu thị chi phí trung bình để sản xuất một sản phẩm.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán kinh tế chi phí trung bình: Chi phí sản xuất 1 sản phẩm bằng tổng chi phí chia cho số sản phẩm $x$.<br>- **HS:** Đọc đề và viết phân thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân thức là: $\\frac{5000x + 100\\,000}{x}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt ý nghĩa thực tiễn của phân thức trong kinh tế học. | Phân thức biểu thị chi phí trung bình sản xuất một sản phẩm là:<br>$$\\frac{5000x + 100\\,000}{x}$$ |
"""
    },
    {
        "filename": "02_KHBD_Toan8_Bai22_TinhChatCoBanPhanThuc_Tiet44-46.md",
        "header": "TIẾT 44, 45, 46 - BÀI 22: TÍNH CHẤT CƠ BẢN CỦA PHÂN THỨC ĐẠI SỐ\n*Thời lượng thực hiện: 03 tiết (135 phút)*",
        "md": """TIẾT 44, 45, 46 - BÀI 22: TÍNH CHẤT CƠ BẢN CỦA PHÂN THỨC ĐẠI SỐ
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững tính chất cơ bản của phân thức đại số:
  + Nếu nhân cả tử và mẫu với cùng một đa thức khác $0$ thì được phân thức bằng phân thức đã cho: $\\frac{A}{B} = \\frac{A \\cdot M}{B \\cdot M}$ ($M \\neq 0$).
  + Nếu chia cả tử và mẫu cho cùng một nhân tử chung thì được phân thức bằng phân thức đã cho: $\\frac{A}{B} = \\frac{A : N}{B : N}$ ($N$ là nhân tử chung).
- Nắm vững quy tắc đổi dấu: $\\frac{A}{B} = \\frac{-A}{-B}$ và $\\frac{-A}{B} = \\frac{A}{-B} = -\\frac{A}{B}$.
- Vận dụng thành thạo rút gọn phân thức đại số và quy đồng mẫu thức nhiều phân thức.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự phân tích đa thức thành nhân tử ở tử và mẫu để tìm nhân tử chung và rút gọn.
- Giao tiếp và hợp tác: Làm việc nhóm tìm mẫu thức chung (MTC) tối ưu nhất cho nhiều phân thức.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích căn cứ lựa chọn nhân tử phụ khi quy đồng mẫu thức.
- Năng lực giải quyết vấn đề toán học: Biến đổi phân thức phức tạp về phân thức tối giản.

c) Năng lực số (NLS):
- ***5.3.TC2a: HS sử dụng công cụ số để thực nghiệm rút gọn phân thức tự động; 2.4.TC2a: HS lựa chọn quy trình hợp tác số hoàn thành bài tập quy đồng mẫu nhóm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS hiểu cách AI phân tích các hạng tử để gợi ý mẫu thức chung thông qua chức năng nhận diện mẫu số học.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, cẩn trọng khi thực hiện phân tích nhân tử và đổi dấu.
- Tác phong làm việc khoa học, tỉ mỉ trong từng bước biến đổi đại số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, máy chiếu, bảng phụ quy trình quy đồng mẫu thức.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại tính chất cơ bản của phân số để tạo liên hệ tự nhiên sang phân thức đại số.
b) Nội dung: Nêu tính chất nhân/chia cả tử và mẫu của phân số với cùng một số khác $0$.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nhắc lại tính chất cơ bản của phân số ở lớp 6. Tính chất đó có áp dụng được cho phân thức đại số không?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khẳng định áp dụng được với đa thức khác đa thức không.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Tính chất cơ bản của phân thức đại số. | Tính chất cơ bản của phân thức đại số hoàn toàn tương tự tính chất cơ bản của phân số. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (95 phút)
### Hoạt động 2.1: Tính chất cơ bản và quy tắc đổi dấu (30 phút)
a) Mục tiêu: HS nắm vững tính chất nhân, chia cùng đa thức khác $0$ và quy tắc đổi dấu.
b) Nội dung: Công thức tính chất cơ bản và quy tắc đổi dấu.
c) Sản phẩm: Vở ghi và bài tập áp dụng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu tính chất cơ bản: Nhân/chia cả tử và mẫu với cùng một đa thức khác $0$. Giới thiệu quy tắc đổi dấu: Đổi dấu cả tử và mẫu thì phân thức không đổi: $\\frac{A}{B} = \\frac{-A}{-B}$.<br>- **HS:** Ghi nhận quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đổi dấu phân thức $\\frac{x - y}{3 - x}$ thành phân thức có mẫu là $x - 3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Ta có: $\\frac{x - y}{3 - x} = \\frac{-(x - y)}{-(3 - x)} = \\frac{y - x}{x - 3}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Quy tắc đổi dấu là công cụ cực kỳ hữu ích khi quy đồng và cộng trừ phân thức. | **1. Tính chất cơ bản:**<br>- $\\frac{A}{B} = \\frac{A \\cdot M}{B \\cdot M}$ ($M$ là đa thức khác đa thức $0$).<br>- $\\frac{A}{B} = \\frac{A : N}{B : N}$ ($N$ là nhân tử chung).<br>- Quy tắc đổi dấu: $\\frac{A}{B} = \\frac{-A}{-B}$. |

### Hoạt động 2.2: Rút gọn phân thức đại số (35 phút)
a) Mục tiêu: Nắm vững quy trình rút gọn phân thức: Phân tích tử và mẫu thành nhân tử rồi chia cho nhân tử chung.
b) Nội dung: Rút gọn phân thức $\\frac{x^2 - 4}{x^2 + 2x}$.
c) Sản phẩm: Lời giải rút gọn trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu các bước rút gọn phân thức: 1. Phân tích tử và mẫu thành nhân tử; 2. Chia cả tử và mẫu cho nhân tử chung.<br>- **HS:** Ghi nhớ 2 bước.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Rút gọn: $\\frac{x^2 - 4}{x^2 + 2x} = \\frac{(x - 2)(x + 2)}{x(x + 2)} = \\frac{x - 2}{x}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Lưu ý: Chỉ chia khi tử và mẫu đã ở dạng tích của các nhân tử. Tuyệt đối không rút gọn từng số hạng. | **2. Rút gọn phân thức:**<br>- Bước 1: Phân tích tử và mẫu thành nhân tử để tìm nhân tử chung.<br>- Bước 2: Chia cả tử và mẫu cho nhân tử chung.<br>- Ví dụ: $\\frac{x^2 - 4}{x^2 + 2x} = \\frac{(x-2)(x+2)}{x(x+2)} = \\frac{x-2}{x}$. |

### Hoạt động 2.3: Quy đồng mẫu thức nhiều phân thức (30 phút)
a) Mục tiêu: Nắm vững quy trình 3 bước tìm MTC và quy đồng mẫu thức.
b) Nội dung: Quy đồng mẫu thức hai phân thức $\\frac{1}{x^2 - 2x}$ và $\\frac{2}{x^2 - 4}$.
c) Sản phẩm: Lời giải quy đồng trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn 3 bước: 1. Phân tích các mẫu thành nhân tử; 2. Tìm MTC (BCNN các hệ số, lũy thừa bậc cao nhất); 3. Tìm nhân tử phụ và nhân cả tử và mẫu với nhân tử phụ tương ứng.<br>- **HS:** Ghi chép quy trình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Mẫu 1: $x(x - 2)$; Mẫu 2: $(x - 2)(x + 2)$. MTC: $x(x - 2)(x + 2)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phân thức 1 nhân với $x + 2$: $\\frac{x + 2}{x(x - 2)(x + 2)}$. Phân thức 2 nhân với $x$: $\\frac{2x}{x(x - 2)(x + 2)}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy trình quy đồng mẫu thức. | **3. Quy đồng mẫu thức:**<br>- Bước 1: Phân tích các mẫu thành nhân tử để tìm MTC.<br>- Bước 2: Tìm nhân tử phụ của từng mẫu (lấy MTC chia cho mẫu đó).<br>- Bước 3: Nhân cả tử và mẫu của mỗi phân thức với nhân tử phụ tương ứng. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (25 phút)
a) Mục tiêu: Thực hành rút gọn và quy đồng mẫu thức các phân thức phức hợp.
b) Nội dung: Bài 6.7, 6.8 SGK trang 12.
c) Sản phẩm: Bài giải chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Rút gọn phân thức: $P = \\frac{x^3 - 3x^2 + 3x - 1}{x^2 - 1}$.<br>- **HS:** Nhận đề và phát hiện hằng đẳng thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tử thức là $(x - 1)^3$. Mẫu thức là $(x - 1)(x + 1)$. Chia cho $(x - 1)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: $P = \\frac{(x - 1)^3}{(x - 1)(x + 1)} = \\frac{(x - 1)^2}{x + 1}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá việc vận dụng hằng đẳng thức lập phương của một hiệu chuẩn xác. | **Lời giải:**<br>$$P = \\frac{x^3 - 3x^2 + 3x - 1}{x^2 - 1}$$<br>$$P = \\frac{(x - 1)^3}{(x - 1)(x + 1)} = \\frac{(x - 1)^2}{x + 1}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Vận dụng rút gọn phân thức tính nhanh giá trị biểu thức tại giá trị biến lớn.
b) Nội dung: Tính giá trị của biểu thức $M = \\frac{x^2 - 25}{x + 5}$ tại $x = 995$.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu đề bài tính nhanh tại $x = 995$. Hướng dẫn rút gọn trước khi thay số.<br>- **HS:** Đọc đề và rút gọn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $M = \\frac{(x - 5)(x + 5)}{x + 5} = x - 5$. Thay $x = 995$ vào ta được $M = 995 - 5 = 990$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng: $M = 990$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học: Rút gọn biểu thức giúp việc tính toán trở nên cực kỳ đơn giản. | Ta có: $M = \\frac{(x - 5)(x + 5)}{x + 5} = x - 5$.<br>Tại $x = 995$, giá trị của biểu thức là:<br>$$M = 995 - 5 = 990$$ |
"""
    },
    {
        "filename": "03_KHBD_Toan8_LuyenTapChung_Tiet47.md",
        "header": "TIẾT 47 - LUYỆN TẬP CHUNG: PHÂN THỨC ĐẠI SỐ (TRANG 13)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 47 - LUYỆN TẬP CHUNG: PHÂN THỨC ĐẠI SỐ (TRANG 13)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và khắc sâu các kiến thức về: Phân thức đại số, điều kiện xác định, giá trị của phân thức, hai phân thức bằng nhau, tính chất cơ bản, quy tắc đổi dấu, rút gọn và quy đồng mẫu thức nhiều phân thức.
- Rèn luyện kỹ năng biến đổi phân thức thành thạo, chính xác.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức Bài 21 và Bài 22 qua sơ đồ tư duy; phát hiện và tự sửa các lỗi sai khi đổi dấu.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp tìm mẫu thức chung tối ưu trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích căn cứ phân tích đa thức thành nhân tử để rút gọn phân thức.
- Năng lực giải quyết vấn đề toán học: Giải các bài toán chứng minh phân thức có giá trị không phụ thuộc vào giá trị của biến.

c) Năng lực số (NLS):
- ***1.2.TC2a: HS đánh giá độ tin cậy của các thuật toán rút gọn từ nguồn Internet; 5.1.TC2a: HS xác định lỗi kỹ thuật khi máy tính báo lỗi chia cho 0 trong phân thức.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS hiểu cách AI phân tích các hạng tử để gợi ý mẫu thức chung; 8.D2.1: HS mô tả kịch bản hội thoại khi yêu cầu chatbot giải thích quy tắc quy đồng.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác, không nhầm lẫn dấu âm.
- Tinh thần kiên trì, vượt khó khi giải các biểu thức cồng kềnh.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 47 (vector 300 DPI), tivi/máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Tái hiện nhanh các công thức tính chất cơ bản và quy tắc đổi dấu.
b) Nội dung: Trả lời 2 câu hỏi trắc nghiệm lý thuyết.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: 1. Nêu điều kiện để phân thức $\\frac{A}{B}$ xác định. 2. Điền vào chỗ trống: $\\frac{A}{B} = \\frac{-A}{...}$.<br>- **HS:** Đọc câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết nhanh câu trả lời vào bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giơ bảng con: 1. $B \\neq 0$; 2. $-B$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn vào bài luyện tập chung. | 1. Điều kiện xác định: $B \\neq 0$.<br>2. $\\frac{A}{B} = \\frac{-A}{-B}$. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ kiến thức phân thức đại số thông qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 47; nhắc lại các nhánh kiến thức trọng tâm.

![Sơ đồ tư duy Luyện tập chung Tiết 47](khbd-ill:mindmap-toan8-tiet47)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 47. Yêu cầu HS phân tích các nhánh: 1. Định nghĩa & ĐKXĐ; 2. Hai phân thức bằng nhau; 3. Tính chất cơ bản & Đổi dấu; 4. Rút gọn & Quy đồng.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận theo cặp đôi nhắc lại các quy tắc cốt lõi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ chuẩn mực. | **Hệ thống kiến thức trọng tâm:**<br>1. Phân thức: $\\frac{A}{B}$ ($B \\neq 0$).<br>2. Bằng nhau: $A \\cdot D = B \\cdot C$.<br>3. Tính chất: Nhân chia cùng đa thức khác $0$; Đổi dấu $\\frac{A}{B} = \\frac{-A}{-B}$.<br>4. Rút gọn: Chia cho nhân tử chung; Quy đồng: Tìm MTC rồi nhân nhân tử phụ. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Rèn luyện kỹ năng rút gọn phân thức phức hợp và quy đồng mẫu thức 3 phân thức.
b) Nội dung: Bài 6.11, 6.12 SGK trang 13.
c) Sản phẩm: Bài giải chi tiết trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài toán:<br>  Bài 1: Rút gọn phân thức: $A = \\frac{2x^2 + 4x}{x^2 - 4}$.<br>  Bài 2: Quy đồng mẫu thức hai phân thức: $\\frac{x}{x^2 - 9}$ và $\\frac{1}{2x - 6}$.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bài 1: $A = \\frac{2x(x + 2)}{(x - 2)(x + 2)} = \\frac{2x}{x - 2}$. Bài 2: MTC là $2(x - 3)(x + 3)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá bài làm, lưu ý HS luôn tìm MTC đơn giản nhất (BCNN hệ số số học). | **Lời giải bài tập:**<br>**Bài 1:**<br>$$A = \\frac{2x(x + 2)}{(x - 2)(x + 2)} = \\frac{2x}{x - 2}$$<br>**Bài 2:**<br>- Ta có: $x^2 - 9 = (x - 3)(x + 3)$ và $2x - 6 = 2(x - 3)$.<br>- $\\text{MTC} = 2(x - 3)(x + 3)$.<br>- Quy đồng mẫu thức:<br>$$\\frac{x}{x^2 - 9} = \\frac{2x}{2(x - 3)(x + 3)}$$<br>$$\\frac{1}{2x - 6} = \\frac{x + 3}{2(x - 3)(x + 3)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Chứng minh một phân thức luôn nhận giá trị không đổi với mọi giá trị của biến thỏa mãn ĐKXĐ.
b) Nội dung: Cho biểu thức $H = \\frac{x^2 - 6x + 9}{2x - 6}$. Chứng minh giá trị của $H$ không phụ thuộc vào dấu của $x - 3$ khi xét tỉ số với $x - 3$.
c) Sản phẩm: Lời giải ngắn trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Rút gọn biểu thức $H = \\frac{x^2 - 6x + 9}{2x - 6}$ với $x \\neq 3$.<br>- **HS:** Đọc đề và rút gọn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $H = \\frac{(x - 3)^2}{2(x - 3)} = \\frac{x - 3}{2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và dặn dò xem trước Bài 23: Phép cộng và phép trừ phân thức đại số. | Biểu thức rút gọn là:<br>$$H = \\frac{(x - 3)^2}{2(x - 3)} = \\frac{x - 3}{2}$$ |
"""
    },
    {
        "filename": "04_KHBD_Toan8_Bai23_PhepCongVaTruPhanThuc_Tiet48-50.md",
        "header": "TIẾT 48, 49, 50 - BÀI 23: PHÉP CỘNG VÀ PHÉP TRỪ PHÂN THỨC ĐẠI SỐ\n*Thời lượng thực hiện: 03 tiết (135 phút)*",
        "md": """TIẾT 48, 49, 50 - BÀI 23: PHÉP CỘNG VÀ PHÉP TRỪ PHÂN THỨC ĐẠI SỐ
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Thực hiện được phép cộng và phép trừ hai phân thức cùng mẫu: Cộng/trừ tử thức và giữ nguyên mẫu thức: $\\frac{A}{M} \\pm \\frac{B}{M} = \\frac{A \\pm B}{M}$.
- Thực hiện được phép cộng và phép trừ hai phân thức khác mẫu thông qua bước quy đồng mẫu thức về MTC.
- Nắm vững khái niệm phân thức đối: $-\\frac{A}{B} = \\frac{-A}{B} = \\frac{A}{-B}$ và tính chất giao hoán, kết hợp của phép cộng phân thức.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quy đồng mẫu thức và cẩn thận đặt dấu ngoặc ở tử thức khi trừ phân thức.
- Giao tiếp và hợp tác: Làm việc nhóm nhóm các phân thức có mẫu đối nhau hoặc cùng mẫu để tính nhanh.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Nhận diện quy tắc đổi dấu $\\frac{A}{B - A} = -\\frac{A}{A - B}$ để tạo mẫu chung.
- Năng lực giải quyết vấn đề toán học: Biểu diễn tổng thời gian hoàn thành công việc của nhiều đội thợ.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS lựa chọn MTBT để kiểm tra kết quả cộng, trừ phân thức phức tạp; 2.2.TC2a: HS vận dụng công nghệ số chia sẻ các bước thực hiện phép tính cho bạn.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu thuật toán phân giải biểu thức đại số của AI trong việc tự động tối giản tổng các phân thức.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, không nhầm lẫn dấu khi thực hiện phép trừ tử thức có nhiều hạng tử.
- Ý thức tự giác, vượt khó trong giải toán đại số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, máy chiếu, bảng phụ ghi quy tắc dấu ngoặc.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại quy tắc cộng trừ phân số cùng mẫu và khác mẫu để kết nối sang phân thức đại số.
b) Nội dung: Tính: $\\frac{3}{x} + \\frac{5}{x}$ và dự đoán cách tính $\\frac{1}{x} + \\frac{1}{x + 1}$.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Thực hiện phép cộng $\\frac{3}{x} + \\frac{5}{x}$. Muốn cộng $\\frac{1}{x} + \\frac{1}{x + 1}$ thì ta phải làm gì trước?<br>- **HS:** Đọc đề và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cùng mẫu: $\\frac{3 + 5}{x} = \\frac{8}{x}$. Khác mẫu thì cần quy đồng mẫu thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Phép cộng và phép trừ phân thức đại số. | Quy tắc cộng trừ phân thức tương tự quy tắc cộng trừ phân số. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (95 phút)
### Hoạt động 2.1: Phép cộng phân thức đại số (45 phút)
a) Mục tiêu: Nắm vững quy tắc cộng cùng mẫu, khác mẫu và tính chất giao hoán, kết hợp.
b) Nội dung: Công thức cộng và các tính chất.
c) Sản phẩm: Vở ghi và lời giải ví dụ của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc: Cộng cùng mẫu giữ nguyên mẫu cộng tử. Khác mẫu quy đồng MTC rồi cộng tử. Tính chất: Giao hoán, kết hợp, cộng với $0$.<br>- **HS:** Tiếp thu kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: $\\frac{x}{x + 3} + \\frac{3}{x + 3}$ và $\\frac{1}{x - 1} + \\frac{2}{x + 1}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày.<br>- Phép tính 1: $\\frac{x + 3}{x + 3} = 1$.<br>- Phép tính 2: MTC là $(x - 1)(x + 1)$. Tổng: $\\frac{x + 1 + 2(x - 1)}{(x - 1)(x + 1)} = \\frac{3x - 1}{x^2 - 1}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Sau khi cộng xong luôn kiểm tra xem kết quả có rút gọn được nữa không. | **1. Phép cộng phân thức đại số:**<br>- Cùng mẫu: $\\frac{A}{M} + \\frac{B}{M} = \\frac{A + B}{M}$.<br>- Khác mẫu: Quy đồng mẫu thức rồi cộng tử thức, giữ nguyên mẫu chung.<br>- Tính chất: Giao hoán, kết hợp, cộng với số $0$. |

### Hoạt động 2.2: Phân thức đối và phép trừ phân thức (50 phút)
a) Mục tiêu: Nắm vững định nghĩa phân thức đối và quy tắc trừ: $\\frac{A}{B} - \\frac{C}{D} = \\frac{A}{B} + \\left(-\\frac{C}{D}\\right)$.
b) Nội dung: Định nghĩa phân thức đối, quy tắc đổi dấu phân thức và phép trừ.
c) Sản phẩm: Lời giải bài tập trừ phân thức trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hai phân thức gọi là đối nhau nếu tổng bằng $0$. Phân thức đối của $\\frac{A}{B}$ là $-\\frac{A}{B} = \\frac{-A}{B}$. Phép trừ: Muốn trừ phân thức $\\frac{A}{B}$ cho $\\frac{C}{D}$, ta cộng $\\frac{A}{B}$ với phân thức đối của $\\frac{C}{D}$.<br>- **HS:** Ghi nhận quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện tính: $\\frac{x + 1}{x - 2} - \\frac{3}{x - 2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $\\frac{x + 1 - 3}{x - 2} = \\frac{x - 2}{x - 2} = 1$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Lưu ý cực kỳ quan trọng: Khi trừ tử thức có nhiều hạng tử, bắt buộc phải đặt trong dấu ngoặc trước khi đổi dấu: $-(C) = -C$. | **2. Phép trừ phân thức đại số:**<br>- Phân thức đối của $\\frac{A}{B}$ là $-\\frac{A}{B}$ (ta có $\\frac{A}{B} + \\left(-\\frac{A}{B}\\right) = 0$).<br>- Quy tắc trừ:<br>$$\\frac{A}{B} - \\frac{C}{D} = \\frac{A}{B} + \\left(-\\frac{C}{D}\\right)$$<br>- Cùng mẫu: $\\frac{A}{M} - \\frac{B}{M} = \\frac{A - B}{M}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (25 phút)
a) Mục tiêu: Thực hiện dãy tính cộng trừ phân thức kết hợp đổi dấu.
b) Nội dung: Bài 6.16, 6.17 SGK trang 18.
c) Sản phẩm: Bài giải chi tiết trên bảng và trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Thực hiện phép tính:<br>$B = \\frac{x}{x - 2} + \\frac{2}{2 - x} + \\frac{4}{x^2 - 4}$.<br>- **HS:** Quan sát mẫu $2 - x$ và đổi dấu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đổi $\\frac{2}{2 - x} = -\\frac{2}{x - 2}$. MTC là $(x - 2)(x + 2)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: $B = \\frac{x - 2}{x - 2} + \\frac{4}{x^2 - 4} = 1 + \\frac{4}{x^2 - 4} = \\frac{x^2}{x^2 - 4}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao cách nhóm hai phân thức đầu rút gọn thành $1$ cực kỳ thông minh. | **Lời giải:**<br>$$B = \\frac{x}{x - 2} - \\frac{2}{x - 2} + \\frac{4}{x^2 - 4}$$<br>$$B = \\frac{x - 2}{x - 2} + \\frac{4}{x^2 - 4} = 1 + \\frac{4}{x^2 - 4} = \\frac{x^2}{x^2 - 4}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (10 phút)
a) Mục tiêu: Vận dụng phép cộng phân thức vào bài toán điện trở tương đương của đoạn mạch song song trong Vật lý.
b) Nội dung: Hai điện trở $R_1, R_2$ mắc song song có điện trở tương đương $R$ thỏa mãn $\\frac{1}{R} = \\frac{1}{R_1} + \\frac{1}{R_2}$. Viết phân thức biểu thị $R$ theo $R_1, R_2$.
c) Sản phẩm: Phân thức $R = \\frac{R_1 R_2}{R_1 + R_2}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu công thức điện trở song song trong Vật lý 8. Yêu cầu cộng hai phân thức $\\frac{1}{R_1} + \\frac{1}{R_2}$ rồi suy ra $R$.<br>- **HS:** Đọc đề và tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $\\frac{1}{R} = \\frac{R_2 + R_1}{R_1 R_2} \\Rightarrow R = \\frac{R_1 R_2}{R_1 + R_2}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định sự gắn kết mật thiết giữa Toán học và Vật lý thực nghiệm. | Điện trở tương đương của hai điện trở mắc song song là:<br>$$R = \\frac{R_1 R_2}{R_1 + R_2}$$ |
"""
    },
    {
        "filename": "05_KHBD_Toan8_Bai24_PhepNhanVaChiaPhanThuc_Tiet51-52.md",
        "header": "TIẾT 51, 52 - BÀI 24: PHÉP NHÂN VÀ PHÉP CHIA PHÂN THỨC ĐẠI SỐ\n*Thời lượng thực hiện: 02 tiết (90 phút)*",
        "md": """TIẾT 51, 52 - BÀI 24: PHÉP NHÂN VÀ PHÉP CHIA PHÂN THỨC ĐẠI SỐ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững quy tắc nhân hai phân thức đại số: Nhân tử với tử và mẫu với mẫu: $\\frac{A}{B} \\cdot \\frac{C}{D} = \\frac{A \\cdot C}{B \\cdot D}$.
- Nắm vững các tính chất của phép nhân phân thức: Giao hoán, kết hợp, nhân với $1$, phân phối của phép nhân đối với phép cộng.
- Nắm vững khái niệm phân thức nghịch đảo và quy tắc chia phân thức: Nhân với phân thức nghịch đảo của số chia: $\\frac{A}{B} : \\frac{C}{D} = \\frac{A}{B} \\cdot \\frac{D}{C}$ ($C \\neq 0$).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự phân tích đa thức thành nhân tử trước khi nhân để triệt tiêu các nhân tử chung nhanh nhất.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận áp dụng tính chất phân phối để tính nhanh biểu thức.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phát hiện các biểu thức nghịch đảo nhau có tích bằng $1$.
- Năng lực giải quyết vấn đề toán học: Biểu diễn bài toán tỉ số năng suất lao động giữa hai dây chuyền sản xuất.

c) Năng lực số (NLS):
- ***3.4.TC2a: HS liệt kê thuật toán các bước thực hiện phép nhân/chia cho máy tính; 5.2.TC2b: HS lựa chọn công cụ CAS phù hợp kiểm tra kết quả rút gọn phân thức.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.A1.2: HS nhận thức việc lạm dụng AI giải bài tập rút gọn phân thức có thể làm giảm khả năng tư duy biến đổi đại số và kỹ năng tính toán độc lập.***

## 3. Về phẩm chất
- Cẩn thận, chính xác khi biến đổi phân tích nhân tử và rút gọn.
- Tinh thần trung thực, tự giác trong học tập, không sao chép máy móc lời giải AI.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, máy chiếu, bài tập mẫu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại quy tắc nhân và chia phân số ở lớp 6 để tạo tiền đề cho phân thức đại số.
b) Nội dung: Nêu quy tắc nhân hai phân số và quy tắc chia hai phân số.
c) Sản phẩm: Câu trả lời miệng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc nhân, chia hai phân số đã học. Dự đoán quy tắc nhân, chia hai phân thức đại số.<br>- **HS:** Lắng nghe và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhân: Tử nhân tử, mẫu nhân mẫu. Chia: Nhân với nghịch đảo.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt vào bài mới: Phép nhân và phép chia phân thức đại số. | Phép nhân và phép chia phân thức đại số tuân theo các quy tắc hoàn toàn tương tự phân số. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Phép nhân phân thức đại số và tính chất (35 phút)
a) Mục tiêu: Nắm vững công thức nhân và các tính chất giao hoán, kết hợp, phân phối.
b) Nội dung: Công thức $\\frac{A}{B} \\cdot \\frac{C}{D} = \\frac{A \\cdot C}{B \\cdot D}$ và ví dụ áp dụng.
c) Sản phẩm: Lời giải bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu quy tắc nhân: Muốn nhân hai phân thức, ta nhân các tử thức với nhau và nhân các mẫu thức với nhau. Giới thiệu các tính chất tương tự như phép nhân số.<br>- **HS:** Ghi nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện tính: $\\frac{x^2 - 4}{2x + 1} \\cdot \\frac{4x + 2}{x - 2}$. Rút gọn trước khi nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng: $\\frac{(x - 2)(x + 2)}{2x + 1} \\cdot \\frac{2(2x + 1)}{x - 2} = 2(x + 2) = 2x + 4$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Cần phân tích thành nhân tử để rút gọn các nhân tử chung trước khi thực hiện nhân, tránh nhân bung ra thành đa thức bậc cao. | **1. Phép nhân phân thức đại số:**<br>- Quy tắc: $\\frac{A}{B} \\cdot \\frac{C}{D} = \\frac{A \\cdot C}{B \\cdot D}$.<br>- Tính chất: Giao hoán, kết hợp, nhân với $1$, phân phối đối với phép cộng:<br>$$\\frac{A}{B} \\cdot \\left(\\frac{C}{D} + \\frac{E}{F}\\right) = \\frac{A}{B} \\cdot \\frac{C}{D} + \\frac{A}{B} \\cdot \\frac{E}{F}$$ |

### Hoạt động 2.2: Phân thức nghịch đảo và phép chia phân thức (30 phút)
a) Mục tiêu: Nắm vững định nghĩa phân thức nghịch đảo và quy tắc chia phân thức.
b) Nội dung: Định nghĩa: Phân thức nghịch đảo của $\\frac{A}{B}$ ($A, B \\neq 0$) là $\\frac{B}{A}$. Quy tắc chia phân thức.
c) Sản phẩm: Lời giải bài tập chia phân thức trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hai phân thức gọi là nghịch đảo nếu tích bằng $1$. Phân thức nghịch đảo của $\\frac{A}{B}$ là gì? Muốn chia phân thức $\\frac{A}{B}$ cho $\\frac{C}{D}$ ta làm thế nào?<br>- **HS:** Trả lời miệng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân thức nghịch đảo là $\\frac{B}{A}$. Quy tắc chia: $\\frac{A}{B} : \\frac{C}{D} = \\frac{A}{B} \\cdot \\frac{D}{C}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Thực hiện: $\\frac{x^2 - 9}{x} : \\frac{x - 3}{x^2} = \\frac{(x - 3)(x + 3)}{x} \\cdot \\frac{x^2}{x - 3} = x(x + 3)$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy tắc chia phân thức chuẩn mực. | **2. Phép chia phân thức đại số:**<br>- Phân thức nghịch đảo của phân thức $\\frac{A}{B}$ ($A \\neq 0, B \\neq 0$) là $\\frac{B}{A}$.<br>- Quy tắc chia: Muốn chia phân thức $\\frac{A}{B}$ cho phân thức $\\frac{C}{D}$ khác $0$, ta nhân $\\frac{A}{B}$ với phân thức nghịch đảo của $\\frac{C}{D}$:<br>$$\\frac{A}{B} : \\frac{C}{D} = \\frac{A}{B} \\cdot \\frac{D}{C} = \\frac{A \\cdot D}{B \\cdot C} \\quad (C \\neq 0)$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Rèn kỹ năng tính giá trị biểu thức phân thức kết hợp nhân chia.
b) Nội dung: Bài 6.22, 6.23 SGK trang 22.
c) Sản phẩm: Bài làm chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Thực hiện phép tính:<br>$K = \\left(\\frac{x}{x^2 - 4} : \\frac{x}{x - 2}\\right) \\cdot (x + 2)$.<br>- **HS:** Nhận bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phép chia trong ngoặc: $\\frac{x}{(x - 2)(x + 2)} \\cdot \\frac{x - 2}{x} = \\frac{1}{x + 2}$. Nhân tiếp: $\\frac{1}{x + 2} \\cdot (x + 2) = 1$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi kết quả đẹp và cách biến đổi tuần tự chuẩn xác. | **Lời giải:**<br>$$K = \\left(\\frac{x}{(x - 2)(x + 2)} \\cdot \\frac{x - 2}{x}\\right) \\cdot (x + 2)$$<br>$$K = \\frac{1}{x + 2} \\cdot (x + 2) = 1$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Vận dụng phép nhân phân thức tính thể tích hình hộp chữ nhật có kích thước là các phân thức đại số.
b) Nội dung: Hình hộp chữ nhật có ba kích thước: $\\frac{x}{x + 1}, \\frac{x + 1}{x + 2}, \\frac{x + 2}{x}$. Tính thể tích khối hộp.
c) Sản phẩm: Thể tích $V = 1$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán tính thể tích hình hộp chữ nhật có ba cạnh là 3 phân thức.<br>- **HS:** Đọc đề và tính tích 3 kích thước.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $V = \\frac{x}{x + 1} \\cdot \\frac{x + 1}{x + 2} \\cdot \\frac{x + 2}{x} = 1$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng: $V = 1$ (không phụ thuộc vào $x$).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá tính độc đáo của bài toán và dặn dò xem lại bài. | Thể tích của hình hộp chữ nhật là:<br>$$V = \\frac{x}{x + 1} \\cdot \\frac{x + 1}{x + 2} \\cdot \\frac{x + 2}{x} = 1$$<br>Thể tích luôn bằng $1$ đơn vị thể tích với mọi $x > 0$. |
"""
    },
    {
        "filename": "06_KHBD_Toan8_LuyenTapChung_Tiet53.md",
        "header": "TIẾT 53 - LUYỆN TẬP CHUNG: CÁC PHÉP TÍNH PHÂN THỨC ĐẠI SỐ (TRANG 23)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 53 - LUYỆN TẬP CHUNG: CÁC PHÉP TÍNH PHÂN THỨC ĐẠI SỐ (TRANG 23)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Rèn luyện kỹ năng thực hiện phối hợp thành thạo cả 4 phép tính: Cộng, trừ, nhân, chia phân thức đại số.
- Vận dụng thứ tự thực hiện phép tính và các tính chất đại số để rút gọn các biểu thức hữu tỉ phức tạp.
- Tìm điều kiện xác định của biểu thức và tính giá trị của biểu thức tại giá trị của biến cho trước.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự lập kế hoạch rút gọn biểu thức nhiều tầng ngoặc; tự kiểm tra điều kiện xác định trước khi thay số.
- Giao tiếp và hợp tác: Tương tác nhóm giải bài toán tìm giá trị nguyên của biến để biểu thức nhận giá trị nguyên.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận logic khi chia đa thức cho đa thức để tách phần nguyên trong phân thức.
- Năng lực giải quyết vấn đề toán học: Mô hình hóa các bài toán toán học - vật lý bằng biểu thức phân thức tổng hợp.

c) Năng lực số (NLS):
- ***5.3.TC2a: HS dùng công cụ số đổi mới cách ôn tập chương qua sơ đồ tư duy số; 1.1.TC2d: HS tổ chức chiến lược tìm kiếm các dạng toán phân thức thực tế.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.D1.1: HS xác định các dạng toán phân thức thực tế trong kinh tế có thể mô phỏng bằng AI; 8.A1.2: HS nhận thức việc lạm dụng AI có thể làm giảm khả năng tư duy độc lập.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, kiên trì, không nản chí trước các bài toán biến đổi cồng kềnh.
- Ý thức học tập tự giác, trung thực, có trách nhiệm.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 53 (vector 300 DPI), máy chiếu.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Nhắc lại thứ tự thực hiện phép tính trong biểu thức hữu tỉ: Trong ngoặc trước, nhân chia trước, cộng trừ sau.
b) Nội dung: Nêu thứ tự thực hiện các phép tính trong biểu thức có ngoặc tròn, ngoặc vuông và các phép tính $+ - \\cdot :$.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu thứ tự thực hiện phép tính đối với biểu thức không có ngoặc và biểu thức có ngoặc.<br>- **HS:** Đọc câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết nhanh câu trả lời lên bảng con.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trong ngoặc: () -> [] -> {}; Phép tính: Nhân chia trước, cộng trừ sau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dẫn vào bài luyện tập chung. | Thứ tự thực hiện: Trong ngoặc trước ngoài ngoặc sau; Nhân chia trước cộng trừ sau. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ 4 phép tính phân thức đại số thông qua Sơ đồ tư duy 300 DPI trực quan.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 53; đối chiếu công thức và các lưu ý đổi dấu.

![Sơ đồ tư duy Luyện tập chung Tiết 53](khbd-ill:mindmap-toan8-tiet53)

c) Sản phẩm: Sơ đồ tư duy hoàn thiện trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tiết 53. Yêu cầu HS phân tích 4 nhánh: 1. Phép cộng; 2. Phép trừ & Phân thức đối; 3. Phép nhân & Tính chất; 4. Phép chia & Nghịch đảo.<br>- **HS:** Quan sát sơ đồ tư duy trên màn chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm đôi nhắc lại các công thức tương ứng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết trình tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ chuẩn mực. | **Hệ thống 4 phép tính phân thức:**<br>1. Phép cộng: Cùng mẫu cộng tử; Khác mẫu quy đồng MTC.<br>2. Phép trừ: $A - B = A + (-B)$; Chú ý dấu ngoặc ở tử thức.<br>3. Phép nhân: $\\frac{A}{B} \\cdot \\frac{C}{D} = \\frac{A \\cdot C}{B \\cdot D}$.<br>4. Phép chia: $\\frac{A}{B} : \\frac{C}{D} = \\frac{A \\cdot D}{B \\cdot C}$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Rút gọn biểu thức tổng hợp và tính giá trị biểu thức tại giá trị biến cho trước.
b) Nội dung: Cho biểu thức $P = \\left(\\frac{1}{x - 2} - \\frac{1}{x + 2}\\right) : \\frac{2}{x^2 - 4}$.<br>  a) Tìm điều kiện xác định của biểu thức $P$;<br>  b) Rút gọn biểu thức $P$.
c) Sản phẩm: Lời giải chi tiết trên bảng và vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tổng hợp rút gọn biểu thức $P$.<br>- **HS:** Nhận bài tập và tìm điều kiện xác định.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** a) ĐKXĐ: $x \\neq 2$ và $x \\neq -2$. b) Trong ngoặc: $\\frac{(x + 2) - (x - 2)}{(x - 2)(x + 2)} = \\frac{4}{x^2 - 4}$. Phép chia: $\\frac{4}{x^2 - 4} \\cdot \\frac{x^2 - 4}{2} = 2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao việc kết luận giá trị biểu thức $P = 2$ là hằng số (không phụ thuộc vào $x$). | **Lời giải:**<br>a) Điều kiện xác định của biểu thức $P$ là $x \\neq 2$ và $x \\neq -2$.<br>b) Rút gọn biểu thức:<br>$$P = \\frac{(x + 2) - (x - 2)}{(x - 2)(x + 2)} : \\frac{2}{x^2 - 4}$$<br>$$P = \\frac{4}{x^2 - 4} \\cdot \\frac{x^2 - 4}{2} = 2$$<br>Vậy biểu thức $P = 2$ với mọi $x \\neq \\pm 2$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tìm giá trị nguyên của $x$ để phân thức nhận giá trị nguyên.
b) Nội dung: Tìm số nguyên $x$ để phân thức $Q = \\frac{3}{x - 1}$ nhận giá trị nguyên.
c) Sản phẩm: Lời giải trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Để phân thức $\\frac{3}{x - 1}$ có giá trị nguyên ($x \\in \\mathbb{Z}$) thì mẫu số $x - 1$ phải là gì của $3$?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $x - 1$ phải là ước của $3$, tức là $x - 1 \\in \\{1, -1, 3, -3\\}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Các giá trị của $x$ là $2, 0, 4, -2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa phương pháp tìm giá trị nguyên của phân thức bằng cách tìm ước của tử số. | Để $Q$ nhận giá trị nguyên thì $x - 1 \\in \\text{Ư}(3) = \\{1, -1, 3, -3\\}$.<br>Suy ra $x \\in \\{2, 0, 4, -2\\}$. |
"""
    },
    {
        "filename": "07_KHBD_Toan8_BaiTapCuoiChuong6_Tiet54.md",
        "header": "TIẾT 54 - BÀI TẬP CUỐI CHƯƠNG VI: PHÂN THỨC ĐẠI SỐ (TRANG 24)\n*Thời lượng thực hiện: 01 tiết (45 phút)*",
        "md": """TIẾT 54 - BÀI TẬP CUỐI CHƯƠNG VI: PHÂN THỨC ĐẠI SỐ (TRANG 24)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết toàn bộ kiến thức Chương VI: Định nghĩa phân thức, điều kiện xác định, tính chất cơ bản, quy tắc đổi dấu, rút gọn, quy đồng mẫu thức và 4 phép tính với phân thức đại số.
- Vận dụng kiến thức toàn chương để giải quyết các bài toán rút gọn biểu thức tổng hợp và bài toán thực tế.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức chương VI qua sơ đồ tư duy; chủ động rà soát và đánh giá các kỹ năng biến đổi phân thức của bản thân.
- Giao tiếp và hợp tác: Tự tin thuyết trình giải thích các bước biến đổi đại số trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa quy tắc, lựa chọn công thức giải toán chính xác và ngắn gọn nhất.
- Năng lực giải quyết vấn đề toán học: Xử lý các bài toán phối hợp nhiều phép tính và giải quyết vấn đề thực tiễn.

c) Năng lực số (NLS):
- ***5.3.TC2a: HS sử dụng công cụ số để kiểm tra kết quả rút gọn toàn bộ đề ôn tập chương VI.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***8.C1.1: HS tìm hiểu ứng dụng của phân thức đại số trong các thuật toán máy học và mô hình hóa dữ liệu kinh tế.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, cẩn trọng, kỷ luật và tác phong khoa học.
- Tự tin, sẵn sàng tâm thế bước vào Chương VII: Phương trình bậc nhất một ẩn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 2 Kết nối tri thức, KHBD, Sơ đồ tư duy Mindmap Tiết 54 (vector 300 DPI), máy chiếu, đề ôn tập chương.
2. Học sinh: SGK Toán 8 Tập 2, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ôn tập nhanh các công thức trọng tâm qua trò chơi trắc nghiệm "Vượt chướng ngại vật".
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm kiểm tra lý thuyết chương VI.
c) Sản phẩm: Bảng con của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu hỏi trắc nghiệm lý thuyết.<br>- **HS:** Chuẩn bị bảng con ghi đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ đáp án sau hiệu lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Giải thích ngắn gọn lý do chọn đáp án.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét và dẫn vào bài ôn tập tổng kết chương VI. | Bảng đáp án trắc nghiệm chuẩn xác của học sinh. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ cấu trúc kiến thức Chương VI bằng Sơ đồ tư duy tổng hợp 300 DPI.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 54; hoàn thiện bức tranh tổng thể về phân thức đại số.

![Sơ đồ tư duy Bài tập cuối chương VI Tiết 54](khbd-ill:mindmap-toan8-tiet54)

c) Sản phẩm: Bảng tổng kết sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy tổng thể Chương VI. Hướng dẫn HS hệ thống theo 4 nhánh lớn: 1. Khái niệm & Tính chất; 2. Bốn phép tính phân thức; 3. Thứ tự thực hiện & Rút gọn; 4. Toán thực tế năng suất chuyển động.<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành các chỗ trống trong phiếu tóm tắt.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS lên bảng điền các công thức trọng tâm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại toàn bộ hệ thống lý thuyết chương VI chuẩn mực. | **Tổng kết lý thuyết Chương VI:**<br>- Phân thức $\\frac{A}{B}$ ($B \\neq 0$), ĐKXĐ: $B \\neq 0$.<br>- Tính chất cơ bản: Nhân chia cùng đa thức khác $0$; Đổi dấu $\\frac{A}{B} = \\frac{-A}{-B}$.<br>- Bốn phép tính: Cộng, Trừ (quy đồng MTC); Nhân (tử nhân tử, mẫu nhân mẫu); Chia (nhân nghịch đảo). |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Giải bài toán tự luận tổng hợp rút gọn biểu thức và tìm giá trị của $x$ để biểu thức đạt giá trị cho trước.
b) Nội dung: Bài 6.27, 6.28 SGK trang 24.
c) Sản phẩm: Vở bài tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho biểu thức $M = \\left(\\frac{x}{x - 3} - \\frac{x}{x + 3}\\right) : \\frac{6x}{x^2 - 9}$.<br>  a) Tìm điều kiện xác định của biểu thức $M$;<br>  b) Rút gọn biểu thức $M$;<br>  c) Tìm giá trị của $x$ để $M = 1$.<br>- **HS:** Làm bài vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** a) ĐKXĐ: $x \\neq 3, x \\neq -3, x \\neq 0$. b) Trong ngoặc: $\\frac{x(x + 3) - x(x - 3)}{x^2 - 9} = \\frac{6x}{x^2 - 9}$. Phép chia: $\\frac{6x}{x^2 - 9} : \\frac{6x}{x^2 - 9} = 1$. c) Biểu thức $M = 1$ với mọi $x$ thỏa mãn ĐKXĐ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá bài làm, lưu ý đối chiếu điều kiện xác định ở câu c: $x \\neq \\pm 3$ và $x \\neq 0$. Tuyệt đối không kết luận tập nghiệm. | **Lời giải:**<br>a) Điều kiện xác định: $x \\neq 3, x \\neq -3$ và $x \\neq 0$.<br>b) Rút gọn:<br>$$M = \\frac{x(x + 3) - x(x - 3)}{x^2 - 9} \\cdot \\frac{x^2 - 9}{6x}$$<br>$$M = \\frac{6x}{x^2 - 9} \\cdot \\frac{x^2 - 9}{6x} = 1$$<br>c) Vì $M = 1$ với mọi $x$ thuộc tập xác định, nên giá trị của $x$ để $M = 1$ là mọi $x \\neq \\pm 3$ và $x \\neq 0$. |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Định hướng chuẩn bị cho Chương VII: Phương trình bậc nhất một ẩn.
b) Nội dung: Giáo viên dặn dò xem lại các quy tắc chuyển vế và tìm $x$ đã học từ lớp 6, 7.
c) Sản phẩm: Kế hoạch học tập của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến nội dung chương tiếp theo: Chương VII sẽ nghiên cứu sâu về phương trình bậc nhất và các bài toán giải toán bằng cách lập phương trình.<br>- **HS:** Ghi chép yêu cầu chuẩn bị.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ôn lại quy tắc chuyển vế đổi dấu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Xác nhận sẵn sàng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi kết quả học tập xuất sắc của cả lớp trong Chương VI. | Chuẩn bị đầy đủ kiến thức về phương trình để bước sang Bài 25 ở tiết sau. |
"""
    }
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print("Hoàn tất tạo 7 KHBD Chương VI: Phân thức đại số (Tiết 42 - 54)!")
