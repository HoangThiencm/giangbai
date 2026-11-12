# -*- coding: utf-8 -*-
"""
Script sinh 7 tệp KHBD Đại số 9 (Tuần 13 - 18):
- 01_KHBD_Toan9_Bai09_BienDoiRutGonCanThuc_Tiet32.md
- 02_KHBD_Toan9_Bai10_CanBacBaVaCanThucBacBa_Tiet33-34.md
- 03_KHBD_Toan9_LuyenTapChung_DaiSo_Tiet35.md (Mindmap: mindmap_toan9_tiet35.png)
- 04_KHBD_Toan9_BaiTapCuoiChuong3_Tiet36-37.md (Mindmap: mindmap_toan9_tiet36_37.png)
- 05_KHBD_Toan9_OnTapCuoiHK1_DaiSo_Tiet38-39.md (Mindmap: mindmap_toan9_tiet38_39.png)
- 06_KHBD_Toan9_KiemTraCuoiHK1_DaiSo_Tiet40.md
- 07_KHBD_Toan9_HDTN_PhaCheDungDich_STEM_Tiet41-42.md
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/10.11_Toan9"
os.makedirs(OUT_DIR, exist_ok=True)

# 01. Bài 9: Biến đổi đơn giản và rút gọn căn thức (Tiết 3 - Tiết 32)
md_01 = """Tiết 32 - BÀI 9: BIẾN ĐỔI ĐƠN GIẢN VÀ RÚT GỌN BIỂU THỨC CHỨA CĂN THỨC BẬC HAI (TIẾT 3)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và phối hợp linh hoạt các phép biến đổi căn thức bậc hai: Đưa thừa số ra ngoài/vào trong dấu căn, khử mẫu của biểu thức lấy căn, trục căn thức ở mẫu bằng nhân lượng liên hợp.
- Vận dụng vào rút gọn các biểu thức chứa biến số phức tạp; tính giá trị của biểu thức tại một giá trị cho trước của biến.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác phát hiện các nhân tử chung và nhận diện biểu thức liên hợp thích hợp để khử căn thức ở mẫu.
- Giao tiếp và hợp tác: Tự tin trao đổi các bước rút gọn biểu thức trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh các phương pháp rút gọn (quy đồng mẫu số trước hay rút gọn từng phân thức trước).
- Năng lực giải quyết vấn đề toán học: Thực hiện chuỗi biến đổi đại số chính xác, không làm thay đổi điều kiện xác định.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Sử dụng máy tính cầm tay để kiểm tra nhanh kết quả số sau khi rút gọn biểu thức đại số.***

## 3. Về phẩm chất
- Cẩn thận, kiên trì, chính xác trong việc đổi dấu, rút gọn và đối chiếu điều kiện xác định.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bảng phụ ghi bài tập rút gọn phân hóa, máy chiếu.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, máy tính cầm tay, giấy nháp.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Khởi động và kiểm tra kỹ năng trục căn thức ở mẫu.
b) Nội dung: Trục căn thức ở mẫu của hai biểu thức: $\\frac{2}{\\sqrt{3}}$ và $\\frac{1}{\\sqrt{5} - 2}$.
c) Sản phẩm: Lời giải: $\\frac{2\\sqrt{3}}{3}$ và $\\sqrt{5} + 2$.
d) Tổ chức thực hiện: GV gọi 2 HS lên bảng tính nhanh, cả lớp nhận xét, GV dẫn dắt vào bài mới.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (20 phút)
### Hoạt động 2.1: Phối hợp các phép biến đổi để rút gọn biểu thức chứa căn (20 phút)
a) Mục tiêu: Nắm vững quy trình rút gọn biểu thức chứa căn thức bậc hai tổng hợp.
b) Nội dung: Khảo sát Ví dụ 4 SGK trang 56 và làm Luyện tập 3.
c) Sản phẩm: Lời giải chi tiết rút gọn biểu thức $P = \\left(\\frac{1}{\\sqrt{x} - 1} - \\frac{1}{\\sqrt{x}}\\right) : \\frac{\\sqrt{x} + 1}{x - 1}$ với $x > 0, x \\ne 1$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu biểu thức $P$ và yêu cầu HS phân tích các mẫu thức.<br>- **GV:** Lưu ý: $x - 1 = (\\sqrt{x} - 1)(\\sqrt{x} + 1)$.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quy đồng phân thức trong ngoặc: MTC là $\\sqrt{x}(\\sqrt{x} - 1)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày từng bước biến đổi.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy tắc: Rút gọn trong ngoặc trước, chuyển phép chia thành phép nhân nghịch đảo. | **Ví dụ rút gọn biểu thức tổng hợp:**<br>Với $x > 0, x \\ne 1$, ta có:<br>$\\frac{1}{\\sqrt{x} - 1} - \\frac{1}{\\sqrt{x}} = \\frac{\\sqrt{x} - (\\sqrt{x} - 1)}{\\sqrt{x}(\\sqrt{x} - 1)} = \\frac{1}{\\sqrt{x}(\\sqrt{x} - 1)}$.<br>Phân thức thứ hai:<br>$\\frac{\\sqrt{x} + 1}{x - 1} = \\frac{\\sqrt{x} + 1}{(\\sqrt{x} - 1)(\\sqrt{x} + 1)} = \\frac{1}{\\sqrt{x} - 1}$.<br>Do đó:<br>$P = \\frac{1}{\\sqrt{x}(\\sqrt{x} - 1)} : \\frac{1}{\\sqrt{x} - 1} = \\frac{1}{\\sqrt{x}(\\sqrt{x} - 1)} \\cdot (\\sqrt{x} - 1) = \\frac{1}{\\sqrt{x}}$.<br>Vậy với $x > 0, x \\ne 1$ thì $P = \\frac{1}{\\sqrt{x}}$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (13 phút)
a) Mục tiêu: Rèn kỹ năng tính giá trị của biểu thức sau khi rút gọn.
b) Nội dung: Giải bài tập 3.19, 3.20 SGK trang 57.
c) Sản phẩm: Lời giải tính giá trị tại $x = 4$ và $x = 9$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu tính giá trị biểu thức $P = \\frac{1}{\\sqrt{x}}$ vừa rút gọn tại $x = 4$ và $x = \\frac{1}{9}$.<br>- **HS:** Làm việc độc lập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kiểm tra điều kiện: $x = 4$ thỏa mãn $x > 0, x \\ne 1$. Thay số và tính.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng dậy đọc kết quả: Tại $x = 4$ thì $P = \\frac{1}{2}$; Tại $x = \\frac{1}{9}$ thì $P = 3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Chỉ thay số khi giá trị của biến thỏa mãn ĐKXĐ ban đầu. | **Bài 3.19 (SGK tr.57):**<br>- Tại $x = 4$ (thỏa mãn ĐKXĐ):<br>$P = \\frac{1}{\\sqrt{4}} = \\frac{1}{2}$.<br>- Tại $x = \\frac{1}{9}$ (thỏa mãn ĐKXĐ):<br>$P = \\frac{1}{\\sqrt{\\frac{1}{9}}} = \\frac{1}{\\frac{1}{3}} = 3$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (7 phút)
- **Tích hợp NLS 1.2.TC2a:** GV hướng dẫn học sinh bấm máy tính Casio để gán $x = 4$ vào biểu thức gốc $P$ bằng phím `CALC`, so sánh với kết quả sau rút gọn để tự kiểm chứng độ chính xác. Dặn dò học sinh chuẩn bị Bài 10: Căn bậc ba và căn thức bậc ba.
"""

# 02. Bài 10: Căn bậc ba và căn thức bậc ba (Tiết 33, 34)
md_02 = """Tiết 33, 34 - BÀI 10: CĂN BẬC BA VÀ CĂN THỨC BẬC BA
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nắm vững định nghĩa căn bậc ba của một số thực: Căn bậc ba của số $a$ là số $x$ sao cho $x^3 = a$, kí hiệu là $\\sqrt[3]{a}$.
- Nhận biết các tính chất cơ bản: Mọi số thực đều có duy nhất một căn bậc ba; Số dương có căn bậc ba dương, số âm có căn bậc ba âm, số 0 có căn bậc ba là 0.
- Nắm vững quy tắc khai căn bậc ba của một tích và một thương: $\\sqrt[3]{a \\cdot b} = \\sqrt[3]{a} \\cdot \\sqrt[3]{b}$; $\\sqrt[3]{\\frac{a}{b}} = \\frac{\\sqrt[3]{a}}{\\sqrt[3]{b}}$ ($b \\ne 0$).
- Làm quen với căn thức bậc ba $\\sqrt[3]{A}$ và hiểu rằng nó xác định với mọi biểu thức $A$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự nghiên cứu sự tương đồng và khác biệt giữa căn bậc hai và căn bậc ba.
- Giao tiếp và hợp tác: Thảo luận nhóm giải các bài toán thực tế liên quan đến thể tích hình lập phương.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh điều kiện xác định giữa $\\sqrt{A}$ ($A \\ge 0$) và $\\sqrt[3]{A}$ (với mọi $A$).
- Năng lực mô hình hóa toán học: Tính độ dài cạnh hình lập phương khi biết thể tích $V$: $a = \\sqrt[3]{V}$.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Sử dụng phím căn bậc ba trên máy tính bỏ túi để tính căn bậc ba của các số thực lớn hoặc số thập phân.***

## 3. Về phẩm chất
- Chăm chỉ, cẩn thận trong việc tính lũy thừa bậc ba và giữ nguyên dấu của số dưới dấu căn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, mô hình khối lập phương, máy chiếu, bảng phụ ghi tính chất căn bậc ba.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, máy tính cầm tay có phím $\\sqrt[3]{\\cdot}$.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Xuất phát từ bài toán tính cạnh khối rubik/thùng chứa hình lập phương có thể tích cho trước.
b) Nội dung: Một bể nước hình lập phương có dung tích $64\\text{ m}^3$. Hỏi độ dài cạnh bể là bao nhiêu mét?
c) Sản phẩm: Lời giải: Cạnh bể bằng $4\\text{ m}$ vì $4^3 = 64$.
d) Tổ chức thực hiện: GV nêu bài toán thực tiễn, học sinh tìm số có lập phương bằng 64 và GV giới thiệu khái niệm căn bậc ba.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (50 phút)
### Hoạt động 2.1: Khái niệm căn bậc ba của một số thực (25 phút)
a) Mục tiêu: Nắm vững định nghĩa và kí hiệu căn bậc ba của một số thực.
b) Nội dung: Đọc mục 1 SGK trang 58 - 59; làm các ví dụ tính $\\sqrt[3]{8}, \\sqrt[3]{-27}, \\sqrt[3]{0}, \\sqrt[3]{-125}$.
c) Sản phẩm: Kết quả tính toán chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Định nghĩa: Căn bậc ba của số $a$ là số $x$ thỏa mãn $x^3 = a$. Kí hiệu là $\\sqrt[3]{a}$.<br>- **GV:** Hỏi: Số âm có căn bậc ba không? Cho ví dụ?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét: $(-3)^3 = -27$ nên $\\sqrt[3]{-27} = -3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS nêu: Mọi số thực đều có duy nhất một căn bậc ba.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu: Khác với căn bậc hai (chỉ số không âm mới có căn bậc hai và số dương có hai căn bậc hai đối nhau), căn bậc ba luôn tồn tại duy nhất cho mọi số thực. | **1. Định nghĩa căn bậc ba:**<br>- Căn bậc ba của số $a$ là số $x$ sao cho $x^3 = a$.<br>- Kí hiệu: $\\sqrt[3]{a}$.<br>- Tính chất nhận xét:<br>+ $(\\sqrt[3]{a})^3 = \\sqrt[3]{a^3} = a$.<br>+ $\\sqrt[3]{a} > 0$ khi $a > 0$.<br>+ $\\sqrt[3]{a} < 0$ khi $a < 0$.<br>+ $\\sqrt[3]{0} = 0$.<br>**Ví dụ:**<br>$\\sqrt[3]{8} = 2$; $\\sqrt[3]{-27} = -3$; $\\sqrt[3]{-125} = -5$. |

### Hoạt động 2.2: Tính chất của căn bậc ba và căn thức bậc ba (25 phút)
a) Mục tiêu: Vận dụng tính chất khai phương tích, thương của căn bậc ba và hiểu khái niệm căn thức bậc ba.
b) Nội dung: Khảo sát mục 2 SGK trang 60 - 61; làm Luyện tập 2 và Luyện tập 3.
c) Sản phẩm: Lời giải rút gọn các biểu thức chứa căn bậc ba.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu các tính chất tương tự như căn bậc hai:<br>1. $a < b \\Rightarrow \\sqrt[3]{a} < \\sqrt[3]{b}$.<br>2. $\\sqrt[3]{ab} = \\sqrt[3]{a} \\cdot \\sqrt[3]{b}$.<br>3. $\\sqrt[3]{\\frac{a}{b}} = \\frac{\\sqrt[3]{a}}{\\sqrt[3]{b}}$ ($b \\ne 0$).<br>- **GV:** Yêu cầu tính: $\\sqrt[3]{135 : 5}$ và $\\sqrt[3]{8 \\cdot 27}$.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Áp dụng tính chất thương và tích.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Căn thức bậc ba $\\sqrt[3]{A}$ xác định với mọi biểu thức $A$. | **2. Tính chất căn bậc ba:**<br>- Với $a, b \\in \\mathbb{R}$, ta có:<br>+ $\\sqrt[3]{ab} = \\sqrt[3]{a} \\cdot \\sqrt[3]{b}$.<br>+ $\\sqrt[3]{\\frac{a}{b}} = \\frac{\\sqrt[3]{a}}{\\sqrt[3]{b}}$ ($b \\ne 0$).<br>**Ví dụ:**<br>a) $\\sqrt[3]{8 \\cdot 27} = \\sqrt[3]{8} \\cdot \\sqrt[3]{27} = 2 \\cdot 3 = 6$.<br>b) $\\sqrt[3]{135 : 5} = \\sqrt[3]{27} = 3$.<br><br>**3. Căn thức bậc ba:**<br>- Cho $A$ là một biểu thức đại số, $\\sqrt[3]{A}$ được gọi là căn thức bậc ba của $A$.<br>- Biểu thức $\\sqrt[3]{A}$ luôn xác định với mọi giá trị của biến. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Củng cố kỹ năng tính toán và so sánh các căn bậc ba.
b) Nội dung: Giải bài tập 3.22, 3.24 SGK trang 61.
c) Sản phẩm: Lời giải đúng trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 3.22: Tính giá trị của biểu thức $A = \\sqrt[3]{64} - \\sqrt[3]{-125} + \\sqrt[3]{-216}$.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khai căn từng số: $\\sqrt[3]{64} = 4$; $\\sqrt[3]{-125} = -5$; $\\sqrt[3]{-216} = -6$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng làm bài: $A = 4 - (-5) + (-6) = 4 + 5 - 6 = 3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt quy tắc xử lý dấu trừ cẩn thận. | **Bài 3.22 (SGK tr.61):**<br>$A = \\sqrt[3]{64} - \\sqrt[3]{-125} + \\sqrt[3]{-216}$<br>$A = 4 - (-5) + (-6)$<br>$A = 4 + 5 - 6 = 3$.<br><br>**Bài 3.24 (SGK tr.61): So sánh:**<br>So sánh $3$ và $\\sqrt[3]{26}$:<br>Ta có $3 = \\sqrt[3]{27}$. Vì $27 > 26$ nên $\\sqrt[3]{27} > \\sqrt[3]{26}$.<br>Vậy $3 > \\sqrt[3]{26}$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)
- **Tích hợp NLS 1.2.TC2a:** Hướng dẫn học sinh sử dụng tổ hợp phím `SHIFT` + $\\sqrt{\\cdot}$ trên máy tính cầm tay Casio để gọi phím căn bậc ba $\\sqrt[3]{\\cdot}$. Thực hành tính thể tích và bán kính khối cầu bằng công thức $R = \\sqrt[3]{\\frac{3V}{4\\pi}}$. Dặn dò chuẩn bị tiết Luyện tập chung Chương III.
"""

# 03. Luyện tập chung (Đại số - Tiết 35)
md_03 = """Tiết 35 - LUYỆN TẬP CHUNG: CĂN BẬC HAI VÀ CĂN BẬC BA
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa và khắc sâu các tính chất, phép biến đổi căn bậc hai và căn bậc ba.
- Rèn luyện kỹ năng kết hợp các phép biến đổi căn thức để giải quyết bài toán rút gọn biểu thức chứa căn bậc hai và căn bậc ba ở mức độ vận dụng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng kết các quy tắc khai phương và trục căn thức bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp tìm điều kiện xác định và rút gọn phân thức.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh điều kiện tồn tại của căn bậc hai và căn bậc ba.
- Năng lực giải quyết vấn đề toán học: Biến đổi căn thức linh hoạt để giải phương trình vô tỉ cơ bản.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Sử dụng phần mềm vẽ sơ đồ tư duy số hoặc bảng tính để phân loại các dạng toán rút gọn căn thức.***

## 3. Về phẩm chất
- Kiên trì, tỉ mỉ, kiểm tra kĩ lưỡng điều kiện có nghĩa trước khi thực hiện các phép biến đổi.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Luyện tập chung Căn bậc hai & Căn bậc ba, phiếu học tập nhóm.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, máy tính cầm tay, giấy nháp.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (4 phút)
a) Mục tiêu: Tạo hứng thú và kiểm tra nhanh điều kiện xác định của biểu thức chứa căn.
b) Nội dung: Biểu thức $\\sqrt{2x - 6}$ và $\\sqrt[3]{2x - 6}$ xác định khi nào?
c) Sản phẩm: Trả lời: $\\sqrt{2x - 6}$ xác định khi $x \\ge 3$; $\\sqrt[3]{2x - 6}$ xác định với mọi $x \\in \\mathbb{R}$.
d) Tổ chức thực hiện: GV đặt câu hỏi nhanh, gọi 1 HS trả lời, cả lớp nhận xét và vào bài luyện tập.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (33 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức bằng sơ đồ tư duy (8 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ các công thức biến đổi căn thức Chương III qua sơ đồ tư duy.
b) Nội dung: Trình chiếu và phân tích Sơ đồ tư duy Căn bậc hai và Căn bậc ba.
c) Sản phẩm: Sơ đồ tư duy được vẽ và khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Luyện tập chung Chương III.<br>- **GV:** Yêu cầu HS nhắc lại 4 nhánh chính: Khái niệm & Điều kiện; Khai phương tích & thương; Đưa thừa số ra/vào căn; Trục căn thức ở mẫu.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại công thức nhân lượng liên hợp khử căn ở mẫu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy thuyết minh các công thức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Trục căn thức ở mẫu là chìa khóa để cộng trừ các phân thức chứa căn. | **SƠ ĐỒ TƯ DUY LUYỆN TẬP CHUNG: CĂN BẬC HAI VÀ CĂN BẬC BA**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Luyện tập chung Căn bậc hai và Căn bậc ba](khbd-ill:mindmap-toan9-tiet35)

### Hoạt động 2.2: Luyện tập rút gọn biểu thức và giải phương trình vô tỉ (25 phút)
a) Mục tiêu: Thành thạo giải phương trình vô tỉ cơ bản và rút gọn biểu thức chứa căn bậc hai, bậc ba.
b) Nội dung: Giải bài tập 3.26, 3.27 SGK trang 62.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 3.26: Giải các phương trình:<br>a) $\\sqrt{2x - 1} = 3$<br>b) $\\sqrt[3]{x + 2} = -2$<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tìm điều kiện của phương trình căn bậc hai, bình phương hai vế. Với phương trình căn bậc ba, lập phương hai vế.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở: Không kết luận tập nghiệm $S = \\{...\\}$, chỉ kết luận: Vậy giá trị của $x$ cần tìm là... | **Bài 3.26 (SGK tr.62):**<br>**a) Giải phương trình $\\sqrt{2x - 1} = 3$:**<br>- Điều kiện: $2x - 1 \\ge 0$, tức là $x \\ge \\frac{1}{2}$.<br>- Bình phương hai vế ta được:<br>$2x - 1 = 9$<br>$2x = 10$<br>$x = 5$ (thỏa mãn điều kiện).<br>- Vậy phương trình có nghiệm là $x = 5$.<br><br>**b) Giải phương trình $\\sqrt[3]{x + 2} = -2$:**<br>- Phương trình xác định với mọi $x \\in \\mathbb{R}$.<br>- Lập phương hai vế ta được:<br>$x + 2 = (-2)^3$<br>$x + 2 = -8$<br>$x = -10$.<br>- Vậy phương trình có nghiệm là $x = -10$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
- **Tích hợp NLS 3.1.TC2a:** GV hướng dẫn học sinh tạo sơ đồ cây tóm tắt các bước giải phương trình vô tỉ $\\sqrt{f(x)} = g(x)$ bằng phần mềm hoặc sơ đồ tư duy trên sổ tay số. Dặn dò chuẩn bị cho 2 tiết Bài tập cuối chương III.
"""

# 04. Bài tập cuối chương III (Đại số - Tiết 36, 37)
md_04 = """Tiết 36, 37 - BÀI TẬP CUỐI CHƯƠNG III (CĂN BẬC HAI VÀ CĂN BẬC BA)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết toàn bộ kiến thức Chương III: Căn bậc hai và căn bậc ba; Các phép biến đổi đơn giản biểu thức chứa căn; Kỹ năng rút gọn biểu thức đại số chứa căn phức tạp.
- Rèn luyện kỹ năng giải các bài toán phụ sau rút gọn: Tính giá trị của biểu thức, tìm biến để biểu thức nhận giá trị nguyên, so sánh biểu thức với một số thực.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác làm đề cương ôn tập cuối chương III.
- Giải quyết vấn đề và sáng tạo: Lựa chọn phương pháp rút gọn tối ưu, biến đổi nhân tử nhanh chóng.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Biện luận điều kiện xác định và đối chiếu nghiệm sau khi giải bài toán.
- Năng lực giải quyết vấn đề toán học: Phối hợp linh hoạt hằng đẳng thức bậc hai và bậc ba.

c) Năng lực số (NLS):
- Năng lực số: Sử dụng máy tính cầm tay thành thạo để kiểm tra giá trị biểu thức và giải nhanh các bài toán trắc nghiệm.

## 3. Về phẩm chất
- Kiên trì, cẩn trọng, chính xác trong từng bước nhân liên hợp và phân tích đa thức thành nhân tử.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy tổng hợp Chương III, hệ thống bài tập trắc nghiệm và tự luận cuối chương.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Kiểm tra trắc nghiệm nhanh để kích hoạt kiến thức toàn chương III.
b) Nội dung: Làm 2 câu trắc nghiệm nhanh về điều kiện xác định của biểu thức chứa căn và căn bậc ba.
c) Sản phẩm: Đáp án chọn đúng của học sinh.
d) Tổ chức thực hiện: GV chiếu câu hỏi, học sinh giơ thẻ đáp án và vào bài ôn tập.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (75 phút)
### Hoạt động 2.1: Hệ thống hóa toàn bộ kiến thức Chương III qua sơ đồ tư duy (15 phút)
a) Mục tiêu: Khắc sâu mạng lưới kiến thức trọng tâm toàn chương III một cách trực quan.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy tổng kết Chương III.
c) Sản phẩm: Bản ghi nhớ sơ đồ tư duy trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy tổng kết Chương III: Căn bậc hai và Căn bậc ba.<br>- **GV:** Yêu cầu HS nêu 4 nhánh chính: Căn bậc hai & bậc ba; Các phép biến đổi; Rút gọn biểu thức; Ứng dụng bài toán.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết lại các công thức hằng đẳng thức $\\sqrt{A^2} = |A|$ và các phép khai phương.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy thuyết minh toàn bộ sơ đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Căn bậc hai đòi hỏi biểu thức lấy căn không âm, còn căn bậc ba xác định với mọi số thực. | **SƠ ĐỒ TƯ DUY TỔNG KẾT CHƯƠNG III: CĂN BẬC HAI VÀ CĂN BẬC BA**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Bài tập cuối chương III Toán 9](khbd-ill:mindmap-toan9-tiet36_37)

### Hoạt động 2.2: Giải bài tập trắc nghiệm cuối chương III (15 phút)
a) Mục tiêu: Củng cố kỹ năng phân tích và chọn đáp án chính xác trong các đề thi tuyển sinh.
b) Nội dung: Giải các bài tập trắc nghiệm 3.28 đến 3.31 SGK trang 63.
c) Sản phẩm: Đáp án giải thích của học sinh.
d) Tổ chức thực hiện: GV cho học sinh làm độc lập, sau đó gọi HS giải thích lý do loại trừ các phương án gây nhiễu.

### Hoạt động 2.3: Giải bài toán tự luận rút gọn và các câu hỏi phụ (45 phút)
a) Mục tiêu: Rèn luyện bài toán rút gọn biểu thức chứa căn dạng đề thi vào lớp 10.
b) Nội dung: Giải bài tập 3.33 SGK trang 64.
c) Sản phẩm: Lời giải chi tiết và câu trả lời hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập: Cho biểu thức $A = \\left(\\frac{\\sqrt{x}}{\\sqrt{x} + 2} + \\frac{\\sqrt{x}}{\\sqrt{x} - 2}\\right) : \\frac{2\\sqrt{x}}{x - 4}$ với $x > 0, x \\ne 4$.<br>a) Rút gọn biểu thức $A$.<br>b) Tìm $x$ để $A = 3$.<br>- **HS:** Làm việc theo cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quy đồng mẫu số chung là $(\\sqrt{x} + 2)(\\sqrt{x} - 2) = x - 4$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa câu a và câu b.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa lời giải, đối chiếu điều kiện $x > 0, x \\ne 4$. | **Bài 3.33 (SGK tr.64):**<br>**a) Rút gọn:**<br>Với $x > 0, x \\ne 4$, ta có:<br>$\\frac{\\sqrt{x}}{\\sqrt{x} + 2} + \\frac{\\sqrt{x}}{\\sqrt{x} - 2} = \\frac{\\sqrt{x}(\\sqrt{x} - 2) + \\sqrt{x}(\\sqrt{x} + 2)}{x - 4} = \\frac{x - 2\\sqrt{x} + x + 2\\sqrt{x}}{x - 4} = \\frac{2x}{x - 4}$.<br>Do đó:<br>$A = \\frac{2x}{x - 4} : \\frac{2\\sqrt{x}}{x - 4} = \\frac{2x}{x - 4} \\cdot \\frac{x - 4}{2\\sqrt{x}} = \\frac{x}{\\sqrt{x}} = \\sqrt{x}$.<br>Vậy với $x > 0, x \\ne 4$ thì $A = \\sqrt{x}$.<br><br>**b) Tìm $x$ để $A = 3$:**<br>Để $A = 3$ thì $\\sqrt{x} = 3$, suy ra $x = 9$.<br>Giá trị $x = 9$ thỏa mãn điều kiện $x > 0, x \\ne 4$.<br>Vậy $x = 9$ thì $A = 3$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (10 phút)
- **Vận dụng nâng cao:** Tìm giá trị nhỏ nhất của biểu thức $P = x - 4\\sqrt{x} + 5$ với $x \\ge 0$.
  + Biến đổi $P = (\\sqrt{x} - 2)^2 + 1 \\ge 1$.
  + Dấu bằng xảy ra khi $\\sqrt{x} - 2 = 0$, tức là $x = 4$ (thỏa mãn $x \\ge 0$).
  + Vậy giá trị nhỏ nhất của $P$ bằng $1$, đạt được khi $x = 4$.
- Dặn dò học sinh chuẩn bị chu đáo cho 2 tiết Ôn tập cuối học kì I môn Toán 9.
"""

# 05. Ôn tập cuối HKI (Đại số - Tiết 38, 39)
md_05 = """Tiết 38, 39 - ÔN TẬP CUỐI HỌC KÌ I (ĐẠI SỐ)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Đại số kì I môn Toán 9:
  + Chương I: Phương trình và hệ hai phương trình bậc nhất hai ẩn (Quy tắc thế, quy tắc cộng đại số, giải bài toán bằng cách lập hệ phương trình).
  + Chương II: Bất đẳng thức và bất phương trình bậc nhất một ẩn (Tính chất liên hệ thứ tự, quy tắc chuyển vế và nhân với một số, biểu diễn tập nghiệm trên trục số).
  + Chương III: Căn bậc hai và căn bậc ba (Định nghĩa, tính chất, các phép biến đổi đơn giản và rút gọn biểu thức).
- Nâng cao kỹ năng tư duy đại số, biến đổi chính xác, giải quyết trọn vẹn các dạng bài toán thi học kì I.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp toàn bộ các phương pháp giải đại số qua sơ đồ tư duy.
- Giao tiếp và hợp tác: Tích cực thảo luận, chia sẻ cách giải hay trong nhóm bạn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Nhận diện nhanh phương pháp thích hợp để giải hệ phương trình hoặc rút gọn biểu thức.
- Năng lực giải quyết vấn đề toán học: Phối hợp linh hoạt nhiều kiến thức đại số để giải quyết bài toán thực tiễn.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Khai thác kho học liệu số, giải đề ôn tập trực tuyến để tự đánh giá năng lực.***
- ***Giáo dục AI (9.D1.1): Làm quen với việc sử dụng công cụ AI để kiểm tra lời giải toán học hoặc gợi ý bước giải khi gặp bế tắc.***

## 3. Về phẩm chất
- Trung thực, nghiêm túc, cẩn trọng trong từng phép tính và từng câu lập luận toán học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Ôn tập tổng hợp Đại số HKI, đề cương ôn tập bám sát ma trận kiểm tra HKI.
2. Học sinh: SGK Toán 9 tập 1, vở ghi, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Xác định rõ trọng tâm ôn tập Đại số để chuẩn bị thi cuối học kì I.
b) Nội dung: Điểm lại cấu trúc điểm số phần Đại số trong đề thi HKI (hệ phương trình, bất phương trình, rút gọn căn thức).
c) Sản phẩm: Tâm thế tự tin, sẵn sàng ôn tập tích cực của học sinh.
d) Tổ chức thực hiện: GV quán triệt mục tiêu, tạo động lực phấn đấu cho cả lớp và dẫn dắt vào bài học.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (75 phút)
### Hoạt động 2.1: Khái quát toàn bộ kiến thức Đại số HKI qua Sơ đồ tư duy (15 phút)
a) Mục tiêu: Hệ thống hóa mạch lạc ba chương Đại số HKI một cách logic và trực quan.
b) Nội dung: Trình chiếu và phân tích Sơ đồ tư duy Ôn tập học kì I: Đại số 9.
c) Sản phẩm: Sơ đồ tư duy được vẽ và khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Ôn tập học kì I Đại số 9.<br>- **GV:** Yêu cầu HS nêu 4 nhánh chính: Chương I (Hệ phương trình); Chương II (Bất đẳng thức & BPT); Chương III (Căn thức); Kĩ năng làm bài thi HKI.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết lại các công thức và quy tắc then chốt.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS đứng dậy trình bày các lưu ý quan trọng khi giải hệ PT và BPT.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Tuyệt đối không dùng dấu tương đương $\\Leftrightarrow$ tùy tiện và không kết luận tập nghiệm $S = \\{...\\}$ hình thức. | **SƠ ĐỒ TƯ DUY ÔN TẬP HỌC KÌ I: ĐẠI SỐ 9**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Ôn tập Học kì I Đại số Toán 9](khbd-ill:mindmap-toan9-tiet38_39)

### Hoạt động 2.2: Ôn luyện giải hệ phương trình và toán bằng cách lập hệ (25 phút)
a) Mục tiêu: Rèn luyện thành thạo giải hệ hai phương trình bậc nhất hai ẩn và bài toán chuyển động thực tế.
b) Nội dung: Giải hệ phương trình và bài toán lập hệ phương trình trong đề cương ôn tập.
c) Sản phẩm: Lời giải chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 1: Giải hệ phương trình:<br>$\\begin{cases} 2x - y = 5 \\\\ 3x + 2y = 11 \\end{cases}$<br>- **HS:** Làm bài cá nhân bằng phương pháp cộng hoặc thế.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhân phương trình thứ nhất với 2: $4x - 2y = 10$. Cộng từng vế với phương trình thứ hai.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa lời giải: $7x = 21 \\Rightarrow x = 3$. Thay vào tìm được $y = 1$. Kết luận nghiệm là $(3; 1)$. | **Dạng 1: Giải hệ phương trình:**<br>Nhân cả hai vế của phương trình thứ nhất với 2 ta được:<br>$\\begin{cases} 4x - 2y = 10 \\\\ 3x + 2y = 11 \\end{cases}$<br>Cộng từng vế hai phương trình của hệ ta được:<br>$7x = 21$, suy ra $x = 3$.<br>Thay $x = 3$ vào phương trình $2x - y = 5$ ta được:<br>$2 \\cdot 3 - y = 5$, suy ra $y = 6 - 5 = 1$.<br>Vậy hệ phương trình có nghiệm duy nhất là $(x; y) = (3; 1)$. |

### Hoạt động 2.3: Ôn luyện bất phương trình và rút gọn căn thức (35 phút)
a) Mục tiêu: Vận dụng giải bất phương trình bậc nhất một ẩn và rút gọn biểu thức chứa căn thức.
b) Nội dung: Giải bất phương trình $3(x - 2) \\ge 5x + 4$ và bài toán rút gọn tổng hợp.
c) Sản phẩm: Lời giải chi tiết và kết luận chuẩn xác.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập giải bất phương trình: $3(x - 2) \\ge 5x + 4$.<br>- **HS:** Khai triển và chuyển vế.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $3x - 6 \\ge 5x + 4 \\Rightarrow -2x \\ge 10 \\Rightarrow x \\le -5$ (đổi chiều khi chia số âm).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng chữa bài và biểu diễn trên trục số.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu quy tắc: Chia cho số âm phải đổi chiều bất phương trình. | **Dạng 2: Giải bất phương trình:**<br>Ta có: $3(x - 2) \\ge 5x + 4$<br>$3x - 6 \\ge 5x + 4$<br>$3x - 5x \\ge 4 + 6$<br>$-2x \\ge 10$<br>$x \\le -5$.<br>Vậy nghiệm của bất phương trình là $x \\le -5$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (10 phút)
- **Tích hợp NLS & AI (9.D1.1):** GV giới thiệu cách nhập biểu thức vào ứng dụng hỗ trợ học toán để kiểm tra kết quả rút gọn căn thức, nhắc nhở học sinh sử dụng công nghệ như một công cụ hỗ trợ đối soát kết quả, không lạm dụng để sao chép bài làm. Dặn dò ôn tập kỹ chuẩn bị tiết Kiểm tra đánh giá cuối học kì I.
"""

# 06. Kiểm tra cuối HKI (Đại số - Tiết 40)
md_06 = """Tiết 40 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (ĐẠI SỐ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá mức độ đạt chuẩn kiến thức kĩ năng của học sinh sau khi học xong chương trình Đại số Học kì I Toán 9 theo ma trận và bản đặc tả đề kiểm tra học kì I.
- Phân loại học sinh, phát hiện các nội dung còn hổng (như nhầm lẫn dấu khi nhân số âm trong bất phương trình, sai điều kiện căn thức) để có kế hoạch phụ đạo bổ trợ trong Học kì II.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Nghiêm túc, tự giác, độc lập hoàn thành bài kiểm tra theo đúng thời gian quy định.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học; Năng lực giải quyết vấn đề toán học: Trình bày bài thi mạch lạc, khoa học, chính xác từng bước biến đổi đại số.

## 3. Về phẩm chất
- Trung thực, nghiêm túc, có trách nhiệm với kết quả học tập của bản thân.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận đề HKI đã được Ban giám hiệu phê duyệt, đáp án và thang điểm chi tiết.
2. Học sinh: Bút viết, máy tính cầm tay, thước kẻ, giấy nháp.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: ỔN ĐỊNH LỚP VÀ PHÁT ĐỀ (3 phút)
- GV kiểm tra sĩ số, phổ biến quy chế phòng thi, yêu cầu học sinh cất toàn bộ tài liệu vào ngăn bàn.
- GV phát đề kiểm tra đến từng học sinh.

## B. HOẠT ĐỘNG 2: HỌC SINH LÀM BÀI KIỂM TRA (40 phút)
- Học sinh làm bài nghiêm túc, độc lập theo đúng thời gian quy định.
- Giáo viên quan sát, bao quát phòng kiểm tra, không giải thích gì thêm về đề thi.

## C. HOẠT ĐỘNG 3: THU BÀI VÀ DẶN DÒ (2 phút)
- GV cho học sinh dừng bút, kiểm tra lại thông tin họ tên, lớp trên bài làm.
- GV thu bài theo từng dãy bàn, kiểm đếm đủ số lượng bài thi trước khi cho học sinh nghỉ. Dặn dò chuẩn bị cho tiết Hoạt động thực hành trải nghiệm STEM: Pha chế dung dịch theo nồng độ.
"""

# 07. HĐTN: Pha chế dung dịch theo nồng độ yêu cầu (STEM - Tiết 41, 42)
md_07 = """Tiết 41, 42 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: PHA CHẾ DUNG DỊCH THEO NỒNG ĐỘ YÊU CẦU (KHBD STEM)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng kiến thức giải bài toán bằng cách lập hệ phương trình bậc nhất hai ẩn vào bài toán pha chế dung dịch trong môn Hóa học và đời sống thực tế (pha nước muối sinh lí $0{,}9\\%$, pha dung dịch sát khuẩn, pha nước đường).
- Hiểu và áp dụng định luật bảo toàn khối lượng chất tan: $m_{\\text{ct}} = m_{\\text{dd}} \\cdot C\\%$.
- Thực hành đo lường, tính toán khối lượng dung dịch cần lấy từ các dung dịch nồng độ ban đầu để pha thành dung dịch có nồng độ mong muốn.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đọc công thức nồng độ phần trăm trong Hóa học và chuyển hóa thành mô hình toán học.
- Giao tiếp và hợp tác: Làm việc nhóm hiệu quả, phân công nhiệm vụ tính toán và thực hành đo đong hóa chất.

b) Năng lực đặc thù môn Toán & Năng lực STEM:
- Năng lực mô hình hóa toán học: Lập hệ phương trình bậc nhất hai ẩn biểu diễn khối lượng dung dịch và khối lượng chất tan.
- Năng lực thực hành thực nghiệm (STEM): Sử dụng cân điện tử, ống đong để pha chế chính xác dung dịch thực tế.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Sử dụng bảng tính Excel/Google Trang tính thiết kế bảng tự động tính toán khối lượng nguyên liệu cần lấy khi thay đổi nồng độ yêu cầu.***

## 3. Về phẩm chất
- Cẩn thận, an toàn, tiết kiệm hóa chất và có ý thức ứng dụng toán học vào phục vụ sức khỏe gia đình và cộng đồng.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy STEM, muối ăn tinh khiết ($\text{NaCl}$), nước cất, cân điện tử mini, cốc đong thủy tinh chia vạch ($\text{ml}$), đũa khuấy.
2. Học sinh: Vở ghi, máy tính cầm tay, phiếu học tập thiết kế quy trình pha chế của nhóm.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU - XÁC ĐỊNH VẤN ĐỀ STEM (10 phút)
a) Mục tiêu: Đặt ra bài toán thực tiễn về nhu cầu pha chế nước muối sinh lí $0{,}9\\%$ từ nước muối $5\\%$ và nước cất ($0\\%$).
b) Nội dung: Trạm y tế trường học cần $500\\text{ g}$ dung dịch nước muối sinh lí nồng độ $0{,}9\\%$ để rửa mắt, súc họng. Hiện tại trong tủ thuốc chỉ có dung dịch nước muối $5\\%$ và nước cất. Cần lấy bao nhiêu gam dung dịch muối $5\\%$ và bao nhiêu gam nước cất để pha được lượng nước muối trên?
c) Sản phẩm: Mô hình hóa vấn đề thành bài toán lập hệ hai phương trình bậc nhất hai ẩn.
d) Tổ chức thực hiện: GV nêu tình huống thực tế, các nhóm học sinh thảo luận xác định các đại lượng cần tìm ($x, y$).

## B. HOẠT ĐỘNG 2: NGHIÊN CỨU KIẾN THỨC NỀN VÀ ĐỀ XUẤT GIẢI PHÁP (35 phút)
### Hoạt động 2.1: Xây dựng mô hình toán học giải bài toán pha chế (15 phút)
a) Mục tiêu: Lập và giải hệ phương trình xác định khối lượng từng loại dung dịch.
b) Nội dung: Gọi $x$ (gam) là khối lượng dung dịch muối $5\\%$; $y$ (gam) là khối lượng nước cất cần lấy ($x, y > 0$).
c) Sản phẩm: Lời giải toán học chi tiết.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn các nhóm lập hai phương trình:<br>1. Phương trình tổng khối lượng dung dịch: $x + y = 500$.<br>2. Phương trình bảo toàn khối lượng muối tan: $5\\% \\cdot x + 0\\% \\cdot y = 0{,}9\\% \\cdot 500$.<br>- **HS:** Thảo luận nhóm giải hệ phương trình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Từ phương trình thứ hai: $0{,}05x = 4{,}5 \\Rightarrow x = 90\\text{ g}$.<br>Thay vào phương trình thứ nhất: $y = 500 - 90 = 410\\text{ g}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện nhóm 1 trình bày kết quả toán học.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Cần lấy $90\\text{ g}$ dung dịch muối $5\\%$ và $410\\text{ g}$ nước cất. | **Lời giải toán học bài toán pha chế:**<br>- Gọi $x$ (g) là khối lượng dung dịch muối $5\\%$; $y$ (g) là khối lượng nước cất cần dùng ($0 < x, y < 500$).<br>- Vì tổng khối lượng dung dịch là $500\\text{ g}$ nên ta có phương trình:<br>$x + y = 500$.<br>- Khối lượng muối nguyên chất trong $500\\text{ g}$ dung dịch $0{,}9\\%$ là:<br>$500 \\cdot 0{,}9\\% = 4{,}5\\text{ g}$.<br>- Khối lượng muối nguyên chất trong dung dịch $5\\%$ là $5\\% \\cdot x = 0{,}05x$.<br>Vì nước cất không chứa muối nên ta có phương trình:<br>$0{,}05x = 4{,}5 \\Rightarrow x = 90$ (thỏa mãn).<br>- Thay vào ta được: $y = 500 - 90 = 410$ (thỏa mãn).<br>- Vậy cần lấy $90\\text{ g}$ dung dịch muối $5\\%$ và $410\\text{ g}$ nước cất. |

### Hoạt động 2.2: Thiết kế quy trình thực hành thực nghiệm (20 phút)
a) Mục tiêu: Các nhóm lên kế hoạch các bước thao tác đo lường hóa chất an toàn, chính xác.
b) Nội dung: Viết quy trình 4 bước pha chế vào phiếu học tập STEM.
c) Sản phẩm: Bản kế hoạch thao tác pha chế của các nhóm.
d) Tổ chức thực hiện: GV kiểm tra bản thiết kế quy trình của từng nhóm trước khi cho phép nhận thiết bị thực hành.

## C. HOẠT ĐỘNG 3: CHẾ TẠO MẪU VÀ THỬ NGHIỆM THỰC HÀNH (35 phút)
### Hoạt động 3.1: Các nhóm thực hành pha chế mẫu tại bàn (20 phút)
a) Mục tiêu: Sử dụng cân điện tử và ống đong để cân đúng $90\\text{ g}$ dung dịch $5\\%$ và $410\\text{ g}$ nước cất, hòa tan đều.
b) Nội dung: Thao tác thực nghiệm theo nhóm.
c) Sản phẩm: Cốc dung dịch nước muối sinh lí $0{,}9\\%$ đạt chuẩn $500\\text{ g}$.
d) Tổ chức thực hiện: GV giám sát an toàn, kiểm tra việc cân đong của học sinh.

### Hoạt động 3.2: Báo cáo, đánh giá sản phẩm dung dịch (15 phút)
a) Mục tiêu: Đánh giá độ chính xác về khối lượng và độ trong suốt của sản phẩm.
b) Nội dung: Đại diện các nhóm mang sản phẩm lên bàn giáo viên để cân kiểm chứng.
c) Sản phẩm: Bảng điểm đánh giá sản phẩm STEM của các nhóm.
d) Tổ chức thực hiện: Các nhóm chấm chéo nhau theo tiêu chí: Tính toán đúng (4 điểm), Thao tác an toàn chính xác (3 điểm), Sản phẩm đạt chuẩn khối lượng (3 điểm).

## D. HOẠT ĐỘNG 4: VẬN DỤNG VÀ MỞ RỘNG (10 phút)
- **Tích hợp NLS 3.1.TC2a:** GV hướng dẫn học sinh tạo một file Google Trang tính có sẵn công thức: Nhập nồng độ dung dịch ban đầu $C_1, C_2$ và nồng độ mục tiêu $C_3$, trang tính sẽ tự động xuất ra khối lượng $x, y$ cần lấy bằng công thức nghiệm của hệ phương trình. Dặn dò học sinh tự chế tạo nước muối sinh lí an toàn tại gia đình.
"""

tasks = [
    ("01_KHBD_Toan9_Bai09_BienDoiRutGonCanThuc_Tiet32.md", md_01),
    ("02_KHBD_Toan9_Bai10_CanBacBaVaCanThucBacBa_Tiet33-34.md", md_02),
    ("03_KHBD_Toan9_LuyenTapChung_DaiSo_Tiet35.md", md_03),
    ("04_KHBD_Toan9_BaiTapCuoiChuong3_Tiet36-37.md", md_04),
    ("05_KHBD_Toan9_OnTapCuoiHK1_DaiSo_Tiet38-39.md", md_05),
    ("06_KHBD_Toan9_KiemTraCuoiHK1_DaiSo_Tiet40.md", md_06),
    ("07_KHBD_Toan9_HDTN_PhaCheDungDich_STEM_Tiet41-42.md", md_07),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
