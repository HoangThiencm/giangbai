# -*- coding: utf-8 -*-
"""
Script sinh 6 tệp KHBD Markdown môn Toán 6 (Tuần 9 - 12):
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "TROLYTHIEN/TEMP/02.11_Toan6"
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 04. BÀI 13: TẬP HỢP CÁC SỐ NGUYÊN (Tiết 30, 31)
# -------------------------------------------------------------
md_04 = """Tiết 30, 31 - BÀI 13: TẬP HỢP CÁC SỐ NGUYÊN
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và hiểu được sự cần thiết của số nguyên âm trong đời sống thực tế (biểu thị nhiệt độ dưới $0^\\circ\\text{C}$, độ sâu dưới mực nước biển, số tiền nợ, thời gian trước Công nguyên).
- Nhận biết và viết được tập hợp các số nguyên $\\mathbb{Z} = \\{...; -3; -2; -1; 0; 1; 2; 3; ...\\}$.
- Biểu diễn được các số nguyên trên trục số (trục số nằm ngang và trục số thẳng đứng); nhận biết gốc $0$, chiều dương, chiều âm.
- Nhận biết và tìm được số đối của một số nguyên; hiểu rằng hai số đối nhau nằm về hai phía so với gốc $0$ và cách đều gốc $0$.
- So sánh được hai số nguyên bất kì; nhận biết thứ tự trong tập hợp số nguyên.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát các hiện tượng thực tế (nhiệt kế, độ cao địa lý), đọc hiểu SGK để rút ra khái niệm số nguyên âm.
- Giao tiếp và hợp tác: Tương tác tích cực trong nhóm khi thực hành xác định vị trí điểm trên trục số và so sánh các số nguyên.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh thứ tự các số nguyên dựa trên vị trí tương đối trên trục số.
- Năng lực mô hình hóa toán học: Sử dụng số nguyên âm và số nguyên dương để mô tả các đại lượng có hướng đối nghịch trong thực tiễn.

c) Năng lực số (NLS):
- ***1.1.TC1a: HS khai thác ứng dụng thời tiết số trên điện thoại thông minh/máy tính hoặc bản đồ số Google Earth để tra cứu nhiệt độ các thành phố vùng cực và độ sâu các rãnh đại dương.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS sử dụng trợ lý học tập AI để tra cứu các ví dụ thực tiễn về ứng dụng của số nguyên âm trong kinh tế học và vật lý học.***

## 3. Về phẩm chất
- Trung thực, cẩn trọng trong việc đọc và ghi dấu của số nguyên (phân biệt rõ dấu "+" và dấu "-").
- Có ý thức vận dụng kiến thức số học vào việc đọc hiểu các chỉ số thời tiết, đời sống hàng ngày.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, máy chiếu, hình ảnh nhiệt kế đo nhiệt độ âm, mô hình trục số nằm ngang và thẳng đứng, phiếu học tập.
2. Học sinh: SGK Toán 6, vở ghi bài, thước kẻ có chia vạch độ dài, bút màu.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: Tạo tình huống xuất hiện nhu cầu mở rộng tập hợp số tự nhiên sang tập hợp số nguyên qua các đại lượng ngược hướng.
b) Nội dung: Quan sát bảng dự báo nhiệt độ của một số thủ đô trên thế giới vào mùa đông và trả lời câu hỏi.
c) Sản phẩm: Câu trả lời của HS về ý nghĩa của các dấu trừ đằng trước các con số nhiệt độ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu bản tin thời tiết thế giới: Mát-xcơ-va nhiệt độ là $-5^\\circ\\text{C}$, Bắc Kinh $-2^\\circ\\text{C}$, Hà Nội $20^\\circ\\text{C}$. Đặt câu hỏi:<br>  1. Dấu \"-\" trước số $5$ có ý nghĩa gì?<br>  2. Các số tự nhiên ta đã học có đủ để biểu thị nhiệt độ dưới $0^\\circ\\text{C}$ không?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trao đổi cặp đôi và rút ra nhận xét.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 HS phát biểu: Dấu trừ nghĩa là nhiệt độ dưới $0^\\circ\\text{C}$. Tập số tự nhiên không có các số này.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định sự cần thiết phải có tập hợp số mới bao gồm cả các số âm, dẫn dắt vào bài mới. | **Tình huống thực tế:**<br>- Nhiệt độ $0^\\circ\\text{C}$ là mốc nhiệt độ nước đóng băng.<br>- Nhiệt độ dưới $0^\\circ\\text{C}$ được ghi với dấu trừ đằng trước: $-5^\\circ\\text{C}$ đọc là \"âm năm độ C\" hoặc \"trừ năm độ C\". |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (48 phút)
### Hoạt động 2.1: Làm quen với số nguyên âm và tập hợp các số nguyên (18 phút)
a) Mục tiêu: Nhận biết số nguyên âm, số nguyên dương, số 0 và kí hiệu tập hợp số nguyên $\\mathbb{Z}$.
b) Nội dung: Đọc thông tin mục 1 SGK, thực hiện HĐ1, HĐ2, Luyện tập 1.
c) Sản phẩm: Khái niệm số nguyên âm, tập hợp $\\mathbb{Z}$, hoàn thành Luyện tập 1.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu:<br>  + Các số $-1, -2, -3, ...$ là các số nguyên âm.<br>  + Các số tự nhiên khác $0$ là $1, 2, 3, ...$ còn gọi là các số nguyên dương.<br>  + Số $0$ không phải là số nguyên âm, cũng không phải là số nguyên dương.<br>  + Tập hợp gồm các số nguyên âm, số $0$ và các số nguyên dương gọi là tập hợp các số nguyên, kí hiệu là $\\mathbb{Z}$.<br>- **GV:** Yêu cầu HS làm Luyện tập 1 (đọc và viết số nguyên mô tả độ cao, độ sâu).<br>- **HS:** Đọc SGK và hoàn thành yêu cầu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi bài và hoàn thành phiếu học tập cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng ghi lại tập hợp $\\mathbb{Z}$ và viết số nguyên tương ứng: Đỉnh Phan-xi-păng cao $3143\\text{ m} \\rightarrow +3143\\text{ m}$; Rãnh Ma-ri-a-na sâu $10994\\text{ m} \\rightarrow -10994\\text{ m}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy ước biểu diễn đại lượng ngược chiều trong thực tế. | **1. Tập hợp các số nguyên:**<br>- Số nguyên âm: $-1; -2; -3; ...$<br>- Số nguyên dương: $1; 2; 3; ...$ (có thể viết $+1; +2; +3; ...$).<br>- Số $0$ không là số nguyên âm, cũng không là số nguyên dương.<br>- Tập hợp số nguyên:<br>$\\mathbb{Z} = \\{...; -3; -2; -1; 0; 1; 2; 3; ...\\}$.<br>- Quy ước thực tế:<br>+ Độ cao trên mực nước biển: dấu dương (+).<br>+ Độ sâu dưới mực nước biển: dấu âm (-).<br>+ Số tiền gửi: dương (+); Số tiền nợ: âm (-). |

### Hoạt động 2.2: Biểu diễn số nguyên trên trục số (15 phút)
a) Mục tiêu: Vẽ được trục số, xác định điểm biểu diễn số nguyên, nhận biết gốc, chiều dương, chiều âm.
b) Nội dung: Thực hiện HĐ3, HĐ4, Luyện tập 2 SGK trang 58-59.
c) Sản phẩm: Hình vẽ trục số chuẩn xác của học sinh trên vở và bảng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn vẽ trục số nằm ngang:<br>  + Vẽ đường thẳng nằm ngang, đánh dấu mũi tên sang phải (chiều dương).<br>  + Chọn một điểm làm gốc $0$.<br>  + Chọn đoạn thẳng đơn vị chia đều hai phía.<br>  + Bên phải gốc $0$ ghi các số dương $1, 2, 3, ...$; bên trái gốc $0$ ghi các số âm $-1, -2, -3, ...$<br>- **GV:** Giới thiệu thêm trục số thẳng đứng (chiều từ dưới lên trên là chiều dương).<br>- **HS:** Dùng thước kẻ chia vạch chính xác vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành vẽ trục số và biểu diễn các điểm $-4, -1, 0, 2, 5$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ và biểu diễn các điểm. Cả lớp quan sát, nhận xét khoảng cách các đoạn đơn vị.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa khái niệm điểm biểu diễn số nguyên $a$ trên trục số. | **2. Trục số:**<br>- Trục số là một đường thẳng trên đó đã chọn gốc $0$, chiều dương (thường là từ trái sang phải hoặc từ dưới lên trên) và đơn vị đo.<br>- Chiều ngược lại với chiều dương là chiều âm.<br>- Điểm biểu diễn số nguyên $a$ gọi là điểm $a$. |

### Hoạt động 2.3: Số đối của một số nguyên và So sánh hai số nguyên (15 phút)
a) Mục tiêu: Tìm được số đối của số nguyên; so sánh hai số nguyên bất kì và sắp xếp dãy số.
b) Nội dung: Tìm hiểu mục 3 và mục 4 SGK trang 60-61; làm Luyện tập 3, Luyện tập 4.
c) Sản phẩm: Lời giải bài tập so sánh số nguyên và tìm số đối.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Trên trục số, hai điểm $3$ và $-3$ có vị trí như thế nào đối với gốc $0$?<br>- **GV:** Rút ra định nghĩa hai số đối nhau. Số đối của số $0$ là gì?<br>- **GV:** Hướng dẫn quy tắc so sánh hai số nguyên:<br>  + Trên trục số nằm ngang, điểm $a$ nằm bên trái điểm $b$ thì $a < b$.<br>  + Mọi số âm đều nhỏ hơn $0$; mọi số dương đều lớn hơn $0$.<br>  + Trong hai số nguyên âm, số nào có khoảng cách đến gốc $0$ lớn hơn thì số đó nhỏ hơn (hoặc số nào có số đối lớn hơn thì số đó nhỏ hơn).<br>- **HS:** Tiếp nhận quy tắc và làm Luyện tập 3, 4.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm bàn, so sánh: $-5$ và $-3$; $-10$ và $2$; $0$ và $-7$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ trả lời: $-5 < -3$ vì điểm $-5$ nằm bên trái điểm $-3$; $-10 < 2$; $-7 < 0$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng kết quy tắc so sánh hai số nguyên và lưu ý học sinh tránh nhầm lẫn giữa so sánh số dương và số âm. | **3. Số đối của một số nguyên:**<br>- Hai số nguyên trên trục số nằm về hai phía đối với gốc $0$ và cách đều gốc $0$ gọi là hai số đối nhau.<br>- Số đối của $a$ là $-a$. Số đối của $-a$ là $a$.<br>- Số đối của $0$ là $0$.<br><br>**4. So sánh hai số nguyên:**<br>- Khi biểu diễn trên trục số nằm ngang, nếu điểm $a$ nằm bên trái điểm $b$ thì $a < b$ (hay $b > a$).<br>- Nhận xét:<br>+ Số nguyên âm < $0$ < Số nguyên dương.<br>+ Với hai số nguyên âm, số nào có số đối lớn hơn thì số đó nhỏ hơn. Ví dụ: vì $5 > 3$ nên $-5 < -3$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (25 phút)
a) Mục tiêu: Vận dụng thành thạo các kiến thức về tập hợp $\\mathbb{Z}$, trục số, số đối và so sánh số nguyên để giải bài tập SGK.
b) Nội dung: HS giải các bài tập 3.1, 3.2, 3.4, 3.5, 3.7 SGK trang 61.
c) Sản phẩm: Bài giải chi tiết của học sinh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ theo 3 nhóm bài:<br>  + Dạng 1: Viết số nguyên mô tả đại lượng thực tế (Bài 3.1, 3.2).<br>  + Dạng 2: Biểu diễn trên trục số và tìm số đối (Bài 3.4, 3.5).<br>  + Dạng 3: So sánh và sắp xếp thứ tự các số nguyên (Bài 3.7).<br>- **HS:** Làm việc cá nhân sau đó đổi chéo bài kiểm tra.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự lực làm bài vào vở. GV theo dõi, hướng dẫn HS còn lúng túng khi so sánh hai số âm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS lên bảng trình bày 3 bài.<br>- Cả lớp nhận xét, bổ sung.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Sửa bài chi tiết, chốt lại kĩ năng sắp xếp số nguyên từ bé đến lớn. | **Bài 3.1 (SGK tr.61):**<br>Bác Năm nợ ngân hàng $10\\,000\\,000$ đồng $\\rightarrow -10\\,000\\,000$ đồng.<br>Bà Sáu có $5\\,000\\,000$ đồng gửi tiết kiệm $\\rightarrow +5\\,000\\,000$ đồng.<br><br>**Bài 3.4 (SGK tr.61):**<br>- Số đối của $6$ là $-6$.<br>- Số đối của $-4$ là $4$.<br>- Số đối của $0$ là $0$.<br>- Số đối của $-(-5) = 5$ là $-5$.<br><br>**Bài 3.7 (SGK tr.61):**<br>Sắp xếp theo thứ tự tăng dần:<br>$-12 < -7 < -3 < 0 < 2 < 5 < 8$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
a) Mục tiêu: Ứng dụng số nguyên âm để đọc nhiệt độ thế giới và giải quyết tình huống tài chính, địa lý.
b) Nội dung: Bài toán thực tế đọc nhiệt độ và xếp thứ tự các địa điểm từ lạnh nhất đến nóng nhất.
c) Sản phẩm: Bảng sắp xếp nhiệt độ hoàn chỉnh của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho bảng nhiệt độ lúc 6 giờ sáng tại 4 địa điểm:<br>  A: $-8^\\circ\\text{C}$; B: $-3^\\circ\\text{C}$; C: $5^\\circ\\text{C}$; D: $-15^\\circ\\text{C}$.<br>  1. Địa điểm nào lạnh nhất? Địa điểm nào ấm nhất?<br>  2. Sắp xếp các địa điểm theo thứ tự nhiệt độ tăng dần.<br>- **HS:** Tiếp nhận bài toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở nháp, trao đổi nhanh với bạn bên cạnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời và nêu lý do so sánh $-15 < -8 < -3 < 5$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tinh thần học tập, giao nhiệm vụ về nhà: Tìm thêm 3 ứng dụng của số nguyên âm trong đời sống thực tế. | **Giải quyết tình huống thực tế:**<br>1. So sánh nhiệt độ: $-15^\\circ\\text{C} < -8^\\circ\\text{C} < -3^\\circ\\text{C} < 5^\\circ\\text{C}$.<br>- Địa điểm D lạnh nhất ($-15^\\circ\\text{C}$).<br>- Địa điểm C ấm nhất ($5^\\circ\\text{C}$).<br>2. Thứ tự nhiệt độ tăng dần:<br>Địa điểm D $\\rightarrow$ Địa điểm A $\\rightarrow$ Địa điểm B $\\rightarrow$ Địa điểm C. |
"""

# -------------------------------------------------------------
# 05. BÀI 14: PHÉP CỘNG VÀ PHÉP TRỪ SỐ NGUYÊN (Tiết 32, 33, 34)
# -------------------------------------------------------------
md_05 = """Tiết 32, 33, 34 - BÀI 14: PHÉP CỘNG VÀ PHÉP TRỪ SỐ NGUYÊN
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Thực hiện được phép cộng hai số nguyên cùng dấu (cùng dương, cùng âm).
- Thực hiện được phép cộng hai số nguyên khác dấu.
- Nhận biết và vận dụng thành thạo các tính chất của phép cộng số nguyên: giao hoán, kết hợp, cộng với số $0$, cộng với số đối để tính toán một cách hợp lí.
- Hiểu và thực hiện được phép trừ hai số nguyên thông qua quy tắc: Muốn trừ số nguyên $a$ cho số nguyên $b$, ta cộng $a$ với số đối của $b$ ($a - b = a + (-b)$).
- Vận dụng được phép cộng, trừ số nguyên vào giải quyết các bài toán thực tiễn đời sống (tính toán chênh lệch nhiệt độ, tài chính thu chi, chuyển động lên xuống).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đọc hiểu các quy tắc cộng, trừ số nguyên qua mô hình di chuyển trên trục số hoặc mô hình thu chi điểm số.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp tính nhanh, hợp tác nhóm giải bài toán thực tế.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích căn cứ chuyển đổi phép trừ thành phép cộng với số đối.
- Năng lực giải quyết vấn đề toán học: Phân tích bài toán thực tiễn đưa về phép cộng, trừ số nguyên.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phím dấu âm (-) trên máy tính cầm tay để thực hiện phép cộng, trừ số nguyên có giá trị lớn và kiểm chứng kết quả tính nhẩm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng công cụ AI học tập để phân tích nguyên nhân lỗi sai thường gặp khi cộng, trừ hai số nguyên khác dấu (quên đổi dấu hoặc nhầm lẫn dấu kết quả).***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, tỉ mỉ khi xử lý dấu âm và dấu ngoặc.
- Ý thức trách nhiệm và tính kỷ luật trong học tập tập thể.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, máy chiếu, mô hình trục số di chuyển điểm, phiếu bài tập nhóm.
2. Học sinh: SGK Toán 6, vở ghi, máy tính cầm tay, bút dạ.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)
a) Mục tiêu: Xuất phát từ tình huống thực tế về sự tăng giảm nhiệt độ hoặc tiền nợ để tạo nhu cầu hình thành phép cộng hai số âm và hai số khác dấu.
b) Nội dung: Xét bài toán: Nhiệt độ buổi sáng ở Sa Pa là $-1^\\circ\\text{C}$, buổi trưa giảm thêm $2^\\circ\\text{C}$. Hỏi nhiệt độ buổi trưa là bao nhiêu?
c) Sản phẩm: Phép tính dự đoán $(-1) + (-2)$ và câu trả lời $-3^\\circ\\text{C}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế:<br>  + Hôm qua bạn Nam nợ $10\\,000$ đồng ($-10\\,000$). Hôm nay Nam nợ thêm $15\\,000$ đồng ($-15\\,000$). Tổng số tiền Nam nợ là bao nhiêu?<br>  + Biểu diễn bằng phép tính toán học như thế nào?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh với bạn cùng bàn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng lên trả lời: Nam nợ tổng cộng $25\\,000$ đồng, tương ứng với $(-10\\,000) + (-15\\,000) = -25\\,000$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Xác nhận kết quả và giới thiệu: Đó chính là phép cộng hai số nguyên âm. Chúng ta cùng tìm hiểu quy tắc tổng quát trong bài học hôm nay. | **Khởi động:**<br>- Nợ thêm nghĩa là cộng thêm số âm:<br>$(-10) + (-15) = -25$.<br>- Quy tắc cộng hai số âm sẽ được khái quát hóa trong bài học. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (65 phút)
### Hoạt động 2.1: Phép cộng hai số nguyên cùng dấu (20 phút - Tiết 32)
a) Mục tiêu: Phát biểu và áp dụng được quy tắc cộng hai số nguyên cùng dấu (cùng dương, cùng âm).
b) Nội dung: Tìm hiểu HĐ1, HĐ2 trang 62; thực hiện Ví dụ 1 và Luyện tập 1.
c) Sản phẩm: Quy tắc cộng hai số nguyên cùng dấu và kết quả các phép tính trong Luyện tập 1.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn quy tắc:<br>  + Cộng hai số nguyên dương chính là cộng hai số tự nhiên khác $0$.<br>  + Muốn cộng hai số nguyên âm, ta cộng hai số đối của chúng rồi thêm dấu \"-\" đằng trước kết quả:<br>    $(-a) + (-b) = -(a + b)$ (với $a, b > 0$).<br>- **GV:** Yêu cầu HS thực hiện Luyện tập 1: Tính $(-12) + (-48)$ và $(-235) + (-165)$.<br>- **HS:** Ghi nhớ quy tắc và làm bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự làm vào vở, đổi vở kiểm tra bạn bên cạnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng tính và nêu rõ từng bước:<br>  $(-12) + (-48) = -(12 + 48) = -60$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, nhấn mạnh: Tổng của hai số nguyên âm luôn là một số nguyên âm. | **1. Cộng hai số nguyên cùng dấu:**<br>- Cộng hai số nguyên dương: làm như cộng hai số tự nhiên.<br>- Cộng hai số nguyên âm:<br>Muốn cộng hai số nguyên âm, ta cộng phần số đối của chúng rồi đặt dấu \"-\" trước kết quả.<br>Ví dụ:<br>$(-15) + (-20) = -(15 + 20) = -35$.<br>$(-12) + (-48) = -(12 + 48) = -60$. |

### Hoạt động 2.2: Phép cộng hai số nguyên khác dấu và Tính chất (25 phút - Tiết 33)
a) Mục tiêu: Thực hiện thành thạo phép cộng hai số nguyên khác dấu; vận dụng các tính chất giao hoán, kết hợp, số đối.
b) Nội dung: Tìm hiểu HĐ3, HĐ4, HĐ5 trang 63-64; thực hiện Luyện tập 2 và Luyện tập 3.
c) Sản phẩm: Quy tắc cộng hai số khác dấu, các công thức tính chất và bài giải luyện tập.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn quy tắc cộng hai số nguyên khác dấu:<br>  + Hai số nguyên đối nhau có tổng bằng $0$: $a + (-a) = 0$.<br>  + Muốn cộng hai số nguyên khác dấu không đối nhau: Ta tìm hiệu hai số đối của chúng (lấy số lớn trừ số bé) rồi đặt trước hiệu dấu của số có số đối lớn hơn.<br>- **GV:** Giới thiệu các tính chất của phép cộng số nguyên:<br>  + Giao hoán: $a + b = b + a$.<br>  + Kết hợp: $(a + b) + c = a + (b + c)$.<br>  + Cộng với $0$: $a + 0 = 0 + a = a$.<br>  + Cộng với số đối: $a + (-a) = 0$.<br>- **HS:** Tiếp thu quy tắc và thực hiện Luyện tập 2, 3.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính nhẩm: $(-28) + 18$; $150 + (-200)$; tính nhanh biểu thức kết hợp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng thực hiện, trình bày rõ bước lấy số lớn trừ số bé và đặt dấu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu: Dấu của tổng phụ thuộc vào số có giá trị lớn hơn khi bỏ dấu trừ. | **2. Cộng hai số nguyên khác dấu:**<br>- Hai số đối nhau có tổng bằng $0$:<br>$a + (-a) = 0$.<br>- Quy tắc cộng hai số khác dấu không đối nhau:<br>Bước 1: Tìm số đối của mỗi số.<br>Bước 2: Lấy số lớn trừ đi số bé trong hai số vừa tìm.<br>Bước 3: Đặt trước hiệu dấu của số có số đối lớn hơn.<br>Ví dụ:<br>$(-28) + 18 = -(28 - 18) = -10$.<br>$35 + (-15) = +(35 - 15) = 20$.<br><br>**3. Tính chất phép cộng số nguyên:**<br>- Giao hoán: $a + b = b + a$.<br>- Kết hợp: $(a + b) + c = a + (b + c)$.<br>- Cộng với số $0$: $a + 0 = a$. |

### Hoạt động 2.3: Phép trừ hai số nguyên (20 phút - Tiết 34)
a) Mục tiêu: Nắm vững và thực hiện đúng quy tắc trừ hai số nguyên ($a - b = a + (-b)$).
b) Nội dung: Tìm hiểu mục 4 SGK trang 65; thực hiện Luyện tập 4 và Vận dụng 2.
c) Sản phẩm: Bài giải phép trừ số nguyên chuyển thành phép cộng với số đối.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt vấn đề: Trong tập số tự nhiên, phép trừ $3 - 5$ không thực hiện được. Trong tập số nguyên $\\mathbb{Z}$, phép trừ này bằng bao nhiêu?<br>- **GV:** Phát biểu quy tắc trừ hai số nguyên: Muốn trừ số nguyên $a$ cho số nguyên $b$, ta cộng $a$ với số đối của $b$:<br>  $a - b = a + (-b)$.<br>- **GV:** Yêu cầu HS tính: $5 - 9$; $(-3) - 8$; $4 - (-7)$; $(-6) - (-10)$.<br>- **HS:** Đọc SGK và áp dụng quy tắc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đổi phép trừ sang phép cộng với số đối rồi tính theo quy tắc đã học.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 4 HS lên bảng làm 4 câu. Nhận xét trường hợp trừ đi số âm: $a - (-b) = a + b$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc: Phép trừ trong $\\mathbb{Z}$ luôn thực hiện được và bản chất quy về phép cộng. | **4. Phép trừ hai số nguyên:**<br>- Quy tắc: Muốn trừ số nguyên $a$ cho số nguyên $b$, ta cộng $a$ với số đối của $b$:<br>$a - b = a + (-b)$.<br>- Chú ý: Trừ đi một số âm là cộng với số đối của nó (số dương):<br>$a - (-b) = a + b$.<br>Ví dụ:<br>$5 - 9 = 5 + (-9) = -4$.<br>$(-3) - 8 = (-3) + (-8) = -11$.<br>$4 - (-7) = 4 + 7 = 11$.<br>$(-6) - (-10) = (-6) + 10 = 4$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (42 phút)
a) Mục tiêu: Luyện tập củng cố kĩ năng tính toán và vận dụng tính chất để tính nhanh các biểu thức chứa phép cộng, trừ số nguyên.
b) Nội dung: HS làm các bài tập 3.9, 3.11, 3.13, 3.14, 3.15 SGK trang 66.
c) Sản phẩm: Vở bài tập giải chi tiết các dạng toán cộng trừ số nguyên.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phân hóa bài tập:<br>  + Dạng 1: Thực hiện phép tính cơ bản (Bài 3.9, 3.11).<br>  + Dạng 2: Tính hợp lý bằng cách nhóm các cặp số đối nhau hoặc tròn chục, tròn trăm (Bài 3.13, 3.14).<br>  + Dạng 3: Bài toán tìm $x$ (Bài 3.15).<br>- **HS:** Nhận nhiệm vụ và tiến hành giải.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài theo nhóm đôi, GV hỗ trợ các em học sinh có khó khăn trong việc xác định dấu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện các nhóm lên bảng chữa bài.<br>- Cả lớp nhận xét cách nhóm số hạng tối ưu nhất.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, tổng kết phương pháp tính hợp lý khi gặp biểu thức dài. | **Bài 3.9 (SGK tr.66):**<br>a) $(-17) + (-23) = -(17 + 23) = -40$.<br>b) $(-56) + 40 = -(56 - 40) = -16$.<br>c) $125 + (-25) = 100$.<br><br>**Bài 3.13 (SGK tr.66): Tính hợp lý:**<br>$A = (-385) + 210 + (385) + (-210)$<br>$A = [(-385) + 385] + [210 + (-210)] = 0 + 0 = 0$.<br><br>**Bài 3.15 (SGK tr.66): Tìm $x$:**<br>a) $x - 12 = -25$<br>$x = -25 + 12$<br>$x = -13$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (20 phút)
a) Mục tiêu: Vận dụng phép cộng, trừ số nguyên vào tính toán độ cao tàu ngầm, nhiệt độ và tài chính thực tiễn.
b) Nội dung: Giải bài tập 3.16 và bài toán độ cao tàu ngầm.
c) Sản phẩm: Lời giải bài toán thực tế của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán: Một tàu ngầm đang ở độ cao $-50\\text{ m}$ so với mực nước biển. Sau một thời gian, tàu nổi lên $20\\text{ m}$, rồi sau đó lặn xuống thêm $35\\text{ m}$. Hỏi vị trí mới của tàu ngầm ở độ cao bao nhiêu mét?<br>- **HS:** Đọc kỹ đề bài, chuyển ngôn ngữ thực tế sang phép toán số học.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết biểu thức: $(-50) + 20 - 35$ hoặc $(-50) + 20 + (-35)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày lời giải chi tiết kèm đơn vị.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt lại cách diễn đạt kết quả: Ở độ cao $-65\\text{ m}$ hoặc ở độ sâu $65\\text{ m}$ dưới mực nước biển. Giao bài tập về nhà. | **Bài toán thực tế tàu ngầm:**<br>- Vị trí ban đầu: $-50\\text{ m}$.<br>- Nổi lên $20\\text{ m}$: $+ 20\\text{ m}$.<br>- Lặn xuống thêm $35\\text{ m}$: $- 35\\text{ m}$.<br>Độ cao mới của tàu ngầm là:<br>$(-50) + 20 - 35 = -30 - 35 = -65\\text{ m}$.<br>Trả lời: Tàu ngầm đang ở độ cao $-65\\text{ m}$ (nghĩa là ở độ sâu $65\\text{ m}$ so với mực nước biển). |
"""

# -------------------------------------------------------------
# 06. BÀI 15: QUY TẮC DẤU NGOẶC (Tiết 35, 36)
# -------------------------------------------------------------
md_06 = """Tiết 35, 36 - BÀI 15: QUY TẮC DẤU NGOẶC
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và phát biểu được quy tắc bỏ dấu ngoặc khi đằng trước có dấu cộng \"+\" và khi đằng trước có dấu trừ \"-\".
- Vận dụng thành thạo quy tắc dấu ngoặc để bỏ dấu ngoặc và thu gọn biểu thức số.
- Vận dụng linh hoạt tính chất giao hoán, kết hợp cùng quy tắc đặt dấu ngoặc để nhóm các số hạng một cách hợp lí nhằm tính nhanh.
- Giải quyết được một số bài toán tính toán đại lượng thực tiễn có chứa nhiều bước cộng, trừ.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự khám phá mối quan hệ về dấu khi bỏ ngoặc qua so sánh kết quả hai cách tính trong SGK.
- Giao tiếp và hợp tác: Trao đổi trong nhóm để tìm cách nhóm ngoặc thuận tiện nhất.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận chặt chẽ khi đổi dấu các số hạng trong ngoặc nếu đằng trước có dấu trừ.
- Năng lực giải quyết vấn đề toán học: Biến đổi biểu thức phức tạp về dạng tính toán đơn giản.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng máy tính cầm tay thực hiện nhập nguyên biểu thức có chứa ngoặc và biểu thức đã bỏ ngoặc để đối chiếu kết quả, phát hiện sai sót về dấu.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng chatbot AI để tạo các bài tập tự luyện về quy tắc dấu ngoặc với các mức độ từ cơ bản đến nâng cao.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác, không chủ quan khi trước dấu ngoặc là dấu \"-\".
- Tinh thần kiên trì, vượt khó trong tính toán số học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, máy chiếu, bảng phụ tổng hợp quy tắc dấu ngoặc, phiếu bài tập.
2. Học sinh: SGK Toán 6, vở ghi, máy tính cầm tay, bút nhớ dòng.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (6 phút)
a) Mục tiêu: Tạo mâu thuẫn nhận thức và kích thích sự tò mò về sự thay đổi dấu khi bỏ ngoặc.
b) Nội dung: So sánh giá trị của hai biểu thức: $A = 12 - (5 - 3)$ và $B = 12 - 5 + 3$.
c) Sản phẩm: Kết quả tính toán của HS: $A = 12 - 2 = 10$; $B = 7 + 3 = 10$. Nhận xét về dấu của các số hạng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho hai biểu thức:<br>  $A = 15 - (8 - 3)$<br>  $B = 15 - 8 + 3$<br>  1. Hãy tính giá trị của $A$ và $B$.<br>  2. Nhận xét gì về kết quả và sự thay đổi dấu của các số trong ngoặc?<br>- **HS:** Nhận nhiệm vụ tính nhẩm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính $A = 15 - 5 = 10$; $B = 7 + 3 = 10$. Thấy rằng $A = B$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS phát biểu: Khi bỏ ngoặc có dấu trừ đằng trước, số $+8$ biến thành $-8$, số $-3$ biến thành $+3$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét câu trả lời, giới thiệu: Quy tắc bỏ dấu ngoặc giúp ta biến đổi và tính toán nhanh chóng mà không cần tính trong ngoặc trước. | **Khởi động:**<br>$A = 15 - (8 - 3) = 15 - 5 = 10$.<br>$B = 15 - 8 + 3 = 7 + 3 = 10$.<br>Nhận xét: $15 - (8 - 3) = 15 - 8 + 3$.<br>Dấu của các số hạng trong ngoặc đã bị đổi khi bỏ dấu ngoặc có dấu trừ đằng trước. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (44 phút)
### Hoạt động 2.1: Quy tắc dấu ngoặc (24 phút - Tiết 35)
a) Mục tiêu: Nắm vững quy tắc bỏ dấu ngoặc có dấu \"+\" hoặc dấu \"-\" đằng trước.
b) Nội dung: Tìm hiểu HĐ1, HĐ2 SGK trang 67; hình thành quy tắc; thực hiện Luyện tập 1.
c) Sản phẩm: Phát biểu quy tắc dấu ngoặc và kết quả Luyện tập 1.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Khái quát quy tắc dấu ngoặc:<br>  + Khi bỏ dấu ngoặc có dấu \"+\" đằng trước, ta giữ nguyên dấu của các số hạng trong ngoặc:<br>    $+(a - b + c) = a - b + c$.<br>  + Khi bỏ dấu ngoặc có dấu \"-\" đằng trước, ta phải đổi dấu tất cả các số hạng trong dấu ngoặc: dấu \"+\" đổi thành dấu \"-\" và dấu \"-\" đổi thành dấu \"+\":<br>    $-(a - b + c) = -a + b - c$.<br>- **GV:** Yêu cầu HS áp dụng làm Luyện tập 1:<br>  Bỏ dấu ngoặc rồi tính:<br>  a) $A = (21 - 32) - (-12 + 32)$;<br>  b) $B = -(125 - 63 + 57) - (63 - 57)$.<br>- **HS:** Đọc SGK và giải Luyện tập 1.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện bỏ ngoặc cẩn thận từng số hạng, chú ý đổi dấu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng thực hiện:<br>  a) $A = 21 - 32 + 12 - 32$...<br>  b) $B = -125 + 63 - 57 - 63 + 57$. Triệt tiêu các cặp số đối nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, lưu ý HS: Số hạng đầu tiên trong ngoặc nếu không ghi dấu thì hiểu là mang dấu cộng. | **1. Quy tắc dấu ngoặc:**<br>- Bỏ dấu ngoặc có dấu \"+\" đằng trước: Giữ nguyên dấu các số hạng trong ngoặc.<br>$+(a + b - c) = a + b - c$.<br>- Bỏ dấu ngoặc có dấu \"-\" đằng trước: Đổi dấu toàn bộ các số hạng trong ngoặc:<br>\"+\" $\\rightarrow$ \"-\", \"-\" $\\rightarrow$ \"+\".<br>$-(a + b - c) = -a - b + c$.<br><br>**Ví dụ (Luyện tập 1 tr.68):**<br>$B = -(125 - 63 + 57) - (63 - 57)$<br>$B = -125 + 63 - 57 - 63 + 57$<br>$B = -125 + (63 - 63) + (-57 + 57)$<br>$B = -125 + 0 + 0 = -125$. |

### Hoạt động 2.2: Đặt dấu ngoặc để nhóm các số hạng một cách hợp lí (20 phút - Tiết 36)
a) Mục tiêu: Nắm vững quy tắc đưa các số hạng vào trong dấu ngoặc để tính toán hợp lí.
b) Nội dung: Đọc phần Nhận xét SGK trang 68; làm Luyện tập 2 và Ví dụ 2.
c) Sản phẩm: Lời giải các bài toán tính nhanh bằng cách nhóm số hạng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn quy tắc ngược lại (đưa số hạng vào trong ngoặc):<br>  + Nếu đặt dấu \"+\" đằng trước dấu ngoặc thì dấu các số hạng trong ngoặc vẫn giữ nguyên.<br>  + Nếu đặt dấu \"-\" đằng trước dấu ngoặc thì phải đổi dấu tất cả các số hạng đưa vào trong ngoặc.<br>- **GV:** Cho bài toán tính nhanh:<br>  $S = 215 + 43 - 215 - 143$. Hãy nhóm các số hạng thích hợp.<br>- **HS:** Quan sát và nhận ra các cặp số triệt tiêu nhau hoặc trừ ra số tròn trăm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài vào vở nháp: $S = (215 - 215) - (143 - 43) = 0 - 100 = -100$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng làm, giải thích vì sao khi đặt dấu \"-\" trước ngoặc thì $-143$ thành $143$ và $+43$ đổi thành $-43$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Việc nhóm các số hạng có dấu trừ phía trước rất dễ sai sót, cần luôn kiểm tra lại bằng cách nhẩm ngược bỏ ngoặc. | **2. Nhóm các số hạng một cách hợp lí:**<br>- Quy tắc đưa vào trong ngoặc:<br>$a - b - c = a - (b + c)$.<br>$a + b - c = a + (b - c)$.<br>- Phương pháp tính nhanh:<br>+ Nhóm các số đối nhau có tổng bằng $0$.<br>+ Nhóm các số tạo thành số tròn chục, tròn trăm, tròn nghìn. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (28 phút)
a) Mục tiêu: Vận dụng thành thạo quy tắc bỏ dấu ngoặc và nhóm số hạng để tính giá trị biểu thức.
b) Nội dung: Giải bài 3.19, 3.20, 3.21 SGK trang 68.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 3 bài tập SGK trang 68:<br>  + Bài 3.19: Bỏ dấu ngoặc rồi tính các biểu thức.<br>  + Bài 3.20: Tính một cách hợp lí các tổng đại số.<br>  + Bài 3.21: Bỏ dấu ngoặc rồi rút gọn biểu thức có chứa biến số.<br>- **HS:** Làm việc cá nhân và trao đổi cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự lực làm bài. GV đi quan sát và uốn nắn kịp thời.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS đại diện lên bảng chữa bài.<br>- Cả lớp đối chiếu kết quả, phát hiện và sửa lỗi sai dấu nếu có.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kết quả làm bài của lớp, nhấn mạnh quy tắc vàng: \"Trước ngoặc dấu trừ - trong ngoặc đổi dấu tất cả\". | **Bài 3.19 (SGK tr.68):**<br>a) $15 - (4 - 7) = 15 - 4 + 7 = 11 + 7 = 18$.<br>b) $(-23) - (12 - 23) = -23 - 12 + 23 = (-23 + 23) - 12 = -12$.<br><br>**Bài 3.20 (SGK tr.68):**<br>a) $B = (13 - 135 + 49) - (13 + 49)$<br>$B = 13 - 135 + 49 - 13 - 49$<br>$B = (13 - 135) + (49 - 49) - 135$<br>$B = (13 - 13) + (49 - 49) - 135 = 0 + 0 - 135 = -135$.<br><br>**Bài 3.21 (SGK tr.68):**<br>$(x + 12) - (12 - y) = x + 12 - 12 + y = x + y$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)
a) Mục tiêu: Vận dụng quy tắc dấu ngoặc để giải bài toán tính tổng các số nguyên thỏa mãn điều kiện cho trước.
b) Nội dung: Tính tổng tất cả các số nguyên $x$ thỏa mãn: $-10 < x \\le 10$.
c) Sản phẩm: Lời giải bài toán tính tổng của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đưa ra bài toán:<br>  Cho tập hợp các số nguyên $x$ sao cho $-10 < x \\le 10$.<br>  1. Hãy liệt kê các giá trị của $x$.<br>  2. Tính tổng của tất cả các số nguyên $x$ đó bằng cách nhóm hợp lý.<br>- **HS:** Tiếp nhận đề bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Liệt kê: $x \\in \\{-9; -8; ...; 8; 9; 10\\}$. Nhóm các cặp số đối nhau.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày:<br>  Tổng $S = [(-9) + 9] + [(-8) + 8] + ... + [(-1) + 1] + 0 + 10 = 0 + ... + 10 = 10$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, biểu dương học sinh đã biết vận dụng tính chất số đối và quy tắc ngoặc. Hướng dẫn ôn tập ở nhà. | **Vận dụng:**<br>Các số nguyên $x$ thỏa mãn là:<br>$-9; -8; -7; ...; 7; 8; 9; 10$.<br>Tổng cần tìm là:<br>$S = (-9 + 9) + (-8 + 8) + ... + (-1 + 1) + 0 + 10$<br>$S = 0 + 0 + ... + 0 + 10 = 10$. |
"""

# -------------------------------------------------------------
# 07. ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HKI (HÌNH HỌC) - Tiết 9
# -------------------------------------------------------------
md_07 = """Tiết 09 - ÔN TẬP KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ I (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ các kiến thức về các hình phẳng trong thực tiễn đã học ở nửa đầu học kì I: Tam giác đều, Hình vuông, Lục giác đều (Bài 18); Hình chữ nhật, Hình thoi, Hình bình hành, Hình thang cân (Bài 19).
- Khắc sâu các yếu tố đặc trưng của từng hình: cạnh (độ dài, song song), góc (bằng nhau, góc vuông), đường chéo (bằng nhau, cắt nhau tại trung điểm, vuông góc).
- Ôn tập và vận dụng thành thạo các công thức tính chu vi và diện tích của hình vuông, hình chữ nhật, hình bình hành, hình thoi, hình thang cân (Bài 20).
- Rèn luyện kĩ năng nhận biết hình thực tế và giải các bài toán thực tiễn về tính toán chi phí, vật liệu.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ lại sơ đồ tư duy hệ thống kiến thức hình học phẳng, tự giải bài tập ôn tập.
- Giao tiếp và hợp tác: Tự tin trao đổi các bước vẽ hình và phương pháp tính diện tích hình phẳng phức hợp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh, phân biệt các tính chất cạnh, góc, đường chéo giữa các hình (hình vuông với hình chữ nhật, hình thoi với hình bình hành).
- Năng lực giải quyết vấn đề toán học: Phân tích một mảnh đất hay bề mặt phức tạp thành các hình quen thuộc để tính chu vi, diện tích.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm GeoGebra trên máy tính hoặc điện thoại thông minh để kiểm tra tính chất song song, bằng nhau của cạnh và đường chéo các hình tứ giác đã học.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS sử dụng ứng dụng AI nhận diện hình ảnh chụp để phát hiện các dạng hình hình học phẳng trong kiến trúc ngôi trường hoặc ngôi nhà của em.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác và thẩm mỹ khi vẽ hình hình học.
- Ý thức trách nhiệm, tự giác ôn tập chuẩn bị cho bài kiểm tra giữa học kì I.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Mindmap Ôn tập Hình học giữa HKI (vector 300 DPI), thước kẻ, êke, compa, máy chiếu.
2. Học sinh: SGK Toán 6, vở ghi, bộ đồ dùng học tập vẽ hình (thước thẳng, êke, compa), máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt trí nhớ và phản xạ nhanh của học sinh về các hình phẳng đã học qua trò chơi ghép thẻ tên hình và đặc điểm.
b) Nội dung: Nối tên hình ở Cột A với đặc điểm tương ứng ở Cột B.
c) Sản phẩm: Bảng nối chính xác tên hình và tính chất.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu bảng nối nhanh:<br>  1. Hình thoi $\\rightarrow$ A. Có 4 cạnh bằng nhau và 4 góc vuông.<br>  2. Hình thang cân $\\rightarrow$ B. Có 2 đường chéo vuông góc với nhau và cắt nhau tại trung điểm mỗi đường.<br>  3. Hình vuông $\\rightarrow$ C. Có 2 cạnh đáy song song và 2 đường chéo bằng nhau.<br>  4. Hình bình hành $\\rightarrow$ D. Các cạnh đối song song và bằng nhau, hai đường chéo cắt nhau tại trung điểm mỗi đường.<br>- **HS:** Chuẩn bị bảng con trả lời nhanh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ đáp án nối.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ đọc: 1 - B, 2 - C, 3 - A, 4 - D.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kiến thức khởi động và giới thiệu vào tiết ôn tập. | **Đáp án khởi động:**<br>1 - B (Hình thoi: 2 đường chéo vuông góc tại trung điểm).<br>2 - C (Hình thang cân: đáy song song, 2 đường chéo bằng nhau).<br>3 - A (Hình vuông: 4 cạnh bằng nhau, 4 góc vuông).<br>4 - D (Hình bình hành: cạnh đối song song và bằng nhau). |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (12 phút)
a) Mục tiêu: Tổng hợp toàn bộ hệ thống hình phẳng và các công thức tính chu vi, diện tích một cách trực quan, logic.
b) Nội dung: Quan sát và phân tích Sơ đồ tư duy Mindmap Ôn tập Hình học giữa HKI; nhắc lại các công thức tính chu vi, diện tích.

![Sơ đồ tư duy Ôn tập Giữa HK1 Hình học](khbd-ill:mindmap-tiet09)

c) Sản phẩm: Bảng tổng kết các công thức chu vi $C$ và diện tích $S$ của các hình phẳng trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Ôn tập Hình học giữa HKI lên màn chiếu. Yêu cầu HS nhắc lại:<br>  + Công thức chu vi, diện tích hình chữ nhật kích thước $a, b$.<br>  + Công thức chu vi, diện tích hình vuông cạnh $a$.<br>  + Công thức diện tích hình bình hành đáy $a$, chiều cao tương ứng $h$.<br>  + Công thức diện tích hình thoi có hai đường chéo $m, n$.<br>  + Công thức diện tích hình thang cân hai đáy $a, b$ và chiều cao $h$.<br>- **HS:** Quan sát sơ đồ tư duy và viết lại công thức vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành bảng công thức vào vở ghi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng ghi lại các công thức diện tích.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng công thức, lưu ý học sinh đơn vị đo phải đồng nhất khi tính chu vi và diện tích. | **Bảng công thức Chu vi và Diện tích:**<br>- **Hình vuông:** $C = 4a$; $S = a^2$.<br>- **Hình chữ nhật:** $C = 2(a + b)$; $S = a \\cdot b$.<br>- **Hình bình hành:** $C = 2(a + b)$; $S = a \\cdot h$.<br>- **Hình thoi:** $C = 4a$; $S = \\frac{1}{2} m \\cdot n$.<br>- **Hình thang cân:** $C = a + b + c + d$; $S = \\frac{(a + b) \\cdot h}{2}$. |

### Hoạt động 2.2: Luyện giải bài tập phân dạng (20 phút)
a) Mục tiêu: Vận dụng công thức chu vi, diện tích để giải các bài toán hình học tính toán và thực tế.
b) Nội dung: HS làm Bài tập 1 (tính diện tích hình thoi và hình bình hành) và Bài tập 2 (tính chi phí lát gạch sân hình chữ nhật).
c) Sản phẩm: Lời giải chi tiết của học sinh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài tập ôn tập:<br>  + **Bài 1:** Một mảnh vườn hình bình hành có độ dài đáy là $12\\text{ m}$, chiều cao tương ứng là $8\\text{ m}$. Một bồn hoa hình thoi ở giữa có hai đường chéo dài $4\\text{ m}$ và $3\\text{ m}$. Tính diện tích phần đất còn lại của mảnh vườn.<br>  + **Bài 2:** Một căn phòng hình chữ nhật có chiều dài $8\\text{ m}$, chiều rộng $6\\text{ m}$. Người ta lát nền bằng gạch hình vuông cạnh $40\\text{ cm}$. Tính số viên gạch cần dùng (bỏ qua mạch vữa).<br>- **HS:** Đọc kỹ đề bài và vẽ hình tóm tắt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm bài cá nhân, thảo luận theo nhóm bàn.<br>- **GV:** Hướng dẫn đổi đơn vị đo ở Bài 2: $40\\text{ cm} = 0{,}4\\text{ m}$ hoặc đổi diện tích phòng ra $\\text{cm}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài 1 và bài 2.<br>- Cả lớp nhận xét, kiểm tra các bước tính toán.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại phương pháp giải các bài toán diện tích thực tế. | **Bài 1:**<br>- Diện tích mảnh vườn hình bình hành là:<br>$S_1 = 12 \\cdot 8 = 96\\text{ m}^2$.<br>- Diện tích bồn hoa hình thoi là:<br>$S_2 = \\frac{1}{2} \\cdot 4 \\cdot 3 = 6\\text{ m}^2$.<br>- Diện tích phần đất còn lại là:<br>$S = S_1 - S_2 = 96 - 6 = 90\\text{ m}^2$.<br><br>**Bài 2:**<br>- Diện tích căn phòng hình chữ nhật là:<br>$S_\\text{phòng} = 8 \\cdot 6 = 48\\text{ m}^2 = 480\\,000\\text{ cm}^2$.<br>- Diện tích một viên gạch hình vuông là:<br>$S_\\text{gạch} = 40 \\cdot 40 = 1\\,600\\text{ cm}^2$.<br>- Số viên gạch cần dùng để lát nền là:<br>$480\\,000 : 1\\,600 = 300$ (viên). |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức chu vi để tính chiều dài hàng rào bao quanh khu đất thực tế.
b) Nội dung: Giải bài toán tính chiều dài dây thép gai rào quanh mảnh đất hình thang cân.
c) Sản phẩm: Lời giải của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán: Bác Ba có mảnh đất hình thang cân có hai cạnh đáy là $15\\text{ m}$ và $25\\text{ m}$, hai cạnh bên mỗi cạnh dài $8\\text{ m}$. Bác muốn rào dây thép gai xung quanh mảnh đất này và bớt lại $3\\text{ m}$ làm cổng ra vào. Hỏi chiều dài dây thép gai bác Ba cần mua là bao nhiêu mét?<br>- **HS:** Nhận đề bài và tính nhẩm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính chu vi hình thang cân rồi trừ đi phần cổng $3\\text{ m}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu cách làm và kết quả: $53\\text{ m}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá tiết học, dặn dò HS ôn kĩ lý thuyết và bài tập để chuẩn bị làm bài kiểm tra giữa kì I thật tốt. | **Lời giải bài toán hàng rào:**<br>- Chu vi của mảnh đất hình thang cân là:<br>$C = 15 + 25 + 8 + 8 = 56\\text{ m}$.<br>- Chiều dài dây thép gai cần mua là:<br>$56 - 3 = 53\\text{ m}$.<br>Đáp số: $53\\text{ m}$. |
"""

# -------------------------------------------------------------
# 08. LUYỆN TẬP CHUNG HÌNH HỌC (Tiết 11)
# -------------------------------------------------------------
md_08 = """Tiết 11 - LUYỆN TẬP CHUNG (HÌNH HỌC CHƯƠNG IV)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và khắc sâu các tính chất của các hình phẳng trong thực tiễn: hình chữ nhật, hình thoi, hình bình hành, hình thang cân.
- Rèn luyện kĩ năng sử dụng dụng cụ học tập (thước thẳng chia vạch, compa, êke) để vẽ chính xác các hình hình học phẳng theo kích thước cho trước.
- Vận dụng linh hoạt công thức tính chu vi và diện tích để giải quyết các bài toán ghép hình phức hợp trong SGK trang 95-96.
- Ứng dụng giải các bài toán thực tiễn về tính diện tích lối đi, sân vườn, tính chi phí trồng cỏ hoặc lát nền.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát hình vẽ phức hợp, phân tích các thành phần hình học đơn giản để tính diện tích.
- Giao tiếp và hợp tác: Làm việc nhóm hiệu quả khi chia sẻ phương pháp chia hình và tính toán.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Lập luận chứng minh tính đúng đắn khi phân chia diện tích một đa giác phức tạp.
- Năng lực sử dụng công cụ, phương tiện học toán: Sử dụng thành thạo thước đo độ dài, êke, compa để vẽ hình chính xác.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm GeoGebra để mô phỏng hình vẽ sân vườn phức hợp và dùng công cụ Area để kiểm tra nhanh kết quả tính diện tích.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng trợ lý AI để tra cứu các ý tưởng thiết kế sân vườn sử dụng các khối hình học đối xứng và tính toán vật liệu tối ưu.***

## 3. Về phẩm chất
- Tỉ mỉ, cẩn thận, chính xác trong từng nét vẽ và phép tính số học.
- Ý thức làm đẹp môi trường sống thông qua ứng dụng toán học vào thiết kế cảnh quan sân trường, sân vườn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Mindmap Luyện tập chung Hình học Chương IV (vector 300 DPI), bộ dụng cụ vẽ hình trên bảng (thước, êke, compa), máy chiếu.
2. Học sinh: SGK Toán 6, vở ghi, dụng cụ vẽ hình học cá nhân, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Khơi gợi hứng thú và rèn luyện phản xạ tính nhanh chu vi, diện tích qua câu đố hình học.
b) Nội dung: Tính diện tích hình thoi có độ dài hai đường chéo lần lượt là $6\\text{ cm}$ và $8\\text{ cm}$. Tính chu vi hình thoi biết cạnh là $5\\text{ cm}$.
c) Sản phẩm: Câu trả lời của học sinh: $S = \\frac{1}{2} \\cdot 6 \\cdot 8 = 24\\text{ cm}^2$; $C = 4 \\cdot 5 = 20\\text{ cm}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đưa ra câu hỏi nhanh trên màn chiếu:<br>  1. Nhắc lại công thức tính diện tích hình thoi khi biết độ dài hai đường chéo $m$ và $n$.<br>  2. Áp dụng tính $S$ và $C$ của hình thoi với $m = 6\\text{ cm}$, $n = 8\\text{ cm}$, cạnh $a = 5\\text{ cm}$.<br>- **HS:** Tính nhanh vào bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhẩm và giơ bảng kết quả.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ giải thích: Diện tích bằng nửa tích hai đường chéo; chu vi bằng 4 lần độ dài cạnh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá câu trả lời, dẫn dắt vào bài luyện tập chung. | **Khởi động:**<br>- Công thức hình thoi:<br>$S = \\frac{1}{2} m \\cdot n = \\frac{1}{2} \\cdot 6 \\cdot 8 = 24\\text{ cm}^2$.<br>$C = 4 \\cdot a = 4 \\cdot 5 = 20\\text{ cm}$. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Hệ thống hóa phương pháp vẽ hình và các công thức tính diện tích hình phức hợp.
b) Nội dung: Phân tích Sơ đồ tư duy Mindmap Luyện tập chung Hình học Chương IV; ôn lại quy trình chia hình để tính diện tích.

![Sơ đồ tư duy Luyện tập chung Hình học](khbd-ill:mindmap-tiet11)

c) Sản phẩm: Bản ghi nhớ phương pháp phân rã hình phẳng trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Luyện tập chung Hình học Chương IV. Nêu vấn đề:<br>  Khi gặp một hình phẳng phức tạp không có công thức trực tiếp, ta có những phương pháp nào để tính diện tích?<br>- **HS:** Quan sát sơ đồ và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi rút ra 2 phương pháp chính:<br>  1. Phương pháp phân chia hình (cắt hình lớn thành các hình nhỏ quen thuộc rồi cộng diện tích lại).<br>  2. Phương pháp bổ sung hình (ghép thêm hình phụ để tạo hình chữ nhật lớn rồi trừ đi diện tích phần bổ sung).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS phát biểu, GV minh họa trực tiếp trên bảng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại 2 phương pháp kinh điển giải toán diện tích đa giác thực tế. | **Hệ thống hóa phương pháp tính diện tích hình phức hợp:**<br>1. **Phương pháp chia hình (Cộng diện tích):**<br>Chia mảnh đất thành các hình chữ nhật, hình thang, hình tam giác quen thuộc:<br>$S = S_1 + S_2 + ...$<br>2. **Phương pháp bù hình (Trừ diện tích):**<br>Bổ sung thêm hình phụ để được hình lớn đơn giản (hình chữ nhật, hình vuông), sau đó lấy diện tích hình lớn trừ đi phần bổ sung:<br>$S = S_\\text{lớn} - S_\\text{phụ}$. |

### Hoạt động 2.2: Luyện giải bài tập SGK trang 95-96 (22 phút)
a) Mục tiêu: Thực hành vẽ hình bằng thước và compa; giải thành thạo Bài 4.23, 4.24, 4.27 SGK.
b) Nội dung: HS vẽ hình bình hành/hình thoi theo yêu cầu và giải bài toán tính diện tích lối đi quanh sân vườn.
c) Sản phẩm: Hình vẽ chuẩn trong vở và bài giải chi tiết Bài 4.27 SGK.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 2 bài tập:<br>  + **Bài 4.23 (SGK tr.95):** Dùng thước và compa vẽ hình thoi $ABCD$ có cạnh $AB = 5\\text{ cm}$ và đường chéo $AC = 8\\text{ cm}$.<br>  + **Bài 4.27 (SGK tr.96):** Một mảnh vườn hình chữ nhật có chiều dài $25\\text{ m}$, chiều rộng $15\\text{ m}$. Người ta làm một lối đi xung quanh vườn rộng $1\\text{ m}$. Phần đất còn lại dùng để trồng hoa. Tính diện tích phần đất trồng hoa.<br>- **HS:** Đọc đề và tiến hành vẽ hình, giải bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hành vẽ hình bằng compa vào vở. Nhóm khác tính kích thước mảnh đất trồng hoa.<br>- **GV:** Quan sát, hướng dẫn thao tác quay compa để lấy giao điểm các cung tròn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng thực hành vẽ hình thoi.<br>- 1 HS lên bảng trình bày bài toán diện tích phần đất trồng hoa.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa thao tác vẽ hình và lưu ý cách trừ chiều dài, chiều rộng khi lối đi chạy quanh cả hai phía: $25 - 2 \\cdot 1 = 23\\text{ m}$. | **Bài 4.23 (SGK tr.95):**<br>- Thao tác vẽ hình thoi bằng compa:<br>1. Vẽ đoạn thẳng $AC = 8\\text{ cm}$.<br>2. Vẽ cung tròn tâm $A$ bán kính $5\\text{ cm}$ và cung tròn tâm $C$ bán kính $5\\text{ cm}$. Hai cung tròn cắt nhau tại $B$ và $D$.<br>3. Nối $A, B, C, D$ ta được hình thoi $ABCD$.<br><br>**Bài 4.27 (SGK tr.96):**<br>- Chiều dài phần đất trồng hoa là:<br>$25 - 1 - 1 = 23\\text{ m}$.<br>- Chiều rộng phần đất trồng hoa là:<br>$15 - 1 - 1 = 13\\text{ m}$.<br>- Diện tích phần đất trồng hoa là:<br>$S = 23 \\cdot 13 = 299\\text{ m}^2$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng tính diện tích và chu vi vào bài toán chi phí trồng hoa và làm hàng rào.
b) Nội dung: Giải bài toán tính tiền mua cây hoa giống để trồng trên diện tích $299\\text{ m}^2$ ở Bài 4.27 với giá $50\\,000\\text{ đồng/m}^2$.
c) Sản phẩm: Kết quả tính chi phí của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu tiếp bài toán thực tế từ Bài 4.27:<br>  Biết chi phí mua giống hoa và công trồng là $50\\,000$ đồng cho mỗi mét vuông. Hỏi người chủ vườn phải chi bao nhiêu tiền để hoàn thành vườn hoa?<br>- **HS:** Tiếp nhận bài toán và tính nhẩm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lấy diện tích trồng hoa nhân với đơn giá: $299 \\cdot 50\\,000$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng tính: $14\\,950\\,000$ đồng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học. Giao nhiệm vụ ôn tập chuẩn bị cho tiết Bài tập cuối chương IV. | **Vận dụng thực tế:**<br>- Tổng chi phí trồng hoa là:<br>$299 \\cdot 50\\,000 = 14\\,950\\,000$ (đồng).<br>Đáp số: $14\\,950\\,000$ đồng. |
"""

# -------------------------------------------------------------
# 09. BÀI TẬP CUỐI CHƯƠNG IV (Tiết 12)
# -------------------------------------------------------------
md_09 = """Tiết 12 - BÀI TẬP CUỐI CHƯƠNG IV (CÁC HÌNH PHẲNG TRONG THỰC TIỄN)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết và hệ thống hóa toàn bộ kiến thức Chương IV:
  + Các hình phẳng đều: Tam giác đều, hình vuông, lục giác đều.
  + Các tứ giác đặc biệt: Hình chữ nhật, hình thoi, hình bình hành, hình thang cân.
  + Hệ thống công thức tính chu vi và diện tích của tất cả các hình đã học.
- Rèn luyện kĩ năng phân loại hình học, vẽ hình chính xác và giải quyết các bài toán tổng hợp cuối chương (trang 97 SGK).
- Nâng cao năng lực ứng dụng toán học vào các bài toán thực tiễn đời sống: lát sàn, làm vườn, thiết kế đồ họa.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đánh giá mức độ nắm vững kiến thức của bản thân sau khi hoàn thành toàn bộ Chương IV.
- Giao tiếp và hợp tác: Tự tin phản biện, bảo vệ lời giải toán hình học trước tập thể lớp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh mối quan hệ bao hàm giữa các hình tứ giác (hình vuông vừa là hình chữ nhật vừa là hình thoi).
- Năng lực mô hình hóa toán học: Chuyển đổi các bài toán đời sống (thiết kế khu vui chơi, lát gạch) sang mô hình tính toán chu vi, diện tích.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm bảng tính Excel lập bảng tính tự động chu vi và diện tích các hình phẳng khi thay đổi độ dài các cạnh.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS sử dụng AI để tạo bản đồ tóm tắt kiến thức chương và các câu hỏi trắc nghiệm kiểm tra độ hiểu bài.***

## 3. Về phẩm chất
- Rèn luyện tư duy logic, sự ngăn nắp, cẩn trọng trong học toán.
- Yêu thích môn học, trân trọng vẻ đẹp đối xứng và hài hòa của các hình học trong tự nhiên và kiến trúc.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, Sơ đồ tư duy Mindmap Bài tập cuối chương IV (vector 300 DPI), bảng phụ trắc nghiệm, máy chiếu.
2. Học sinh: SGK Toán 6, vở ghi, bộ dụng cụ hình học đầy đủ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (6 phút)
a) Mục tiêu: Khởi động tinh thần thi đua qua bài trắc nghiệm nhanh 4 câu hỏi tổng kết đặc điểm các hình trong Chương IV.
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm nhanh trên màn chiếu.
c) Sản phẩm: Bảng chọn đáp án của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu trắc nghiệm nhanh:<br>  1. Hình nào có 3 cạnh bằng nhau và 3 góc bằng nhau?<br>  2. Tứ giác có hai đường chéo bằng nhau và cắt nhau tại trung điểm của mỗi đường là hình gì?<br>  3. Hình thoi có hai đường chéo là $8\\text{ cm}$ và $10\\text{ cm}$ thì diện tích là bao nhiêu?<br>  4. Hình thang cân có độ dài hai cạnh bên bằng nhau đúng hay sai?<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ bảng đáp án.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Cả lớp đồng thanh đưa ra đáp án và giải thích ngắn gọn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ nắm vững kiến thức toàn chương của cả lớp, bắt đầu vào tiết ôn tập bài tập cuối chương. | **Đáp án trắc nghiệm:**<br>1. Tam giác đều.<br>2. Hình chữ nhật.<br>3. $S = \\frac{1}{2} \\cdot 8 \\cdot 10 = 40\\text{ cm}^2$.<br>4. Đúng. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (30 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức toàn chương qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Giúp học sinh nhìn thấy bức tranh tổng thể của toàn bộ Chương IV qua Sơ đồ tư duy trực quan, cô đọng.
b) Nội dung: Quan sát, phân tích Sơ đồ tư duy Mindmap Bài tập cuối chương IV; củng cố các mối quan hệ hình học.

![Sơ đồ tư duy Bài tập cuối chương IV](khbd-ill:mindmap-tiet12)

c) Sản phẩm: Bảng tổng kết phân loại và công thức tính toán toàn bộ Chương IV trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Bài tập cuối chương IV. Yêu cầu HS:<br>  1. Kể tên 3 hình đều đã học.<br>  2. Kể tên 4 hình tứ giác đặc biệt và nêu sự giống/khác nhau về đường chéo.<br>  3. Nêu các công thức diện tích cần ghi nhớ.<br>- **HS:** Quan sát sơ đồ tư duy trên màn hình và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh nhóm 4 người, tóm tắt lại các ý chính.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm trình bày: Nêu rõ hình chữ nhật có 2 đường chéo bằng nhau; hình thoi có 2 đường chéo vuông góc; hình vuông có 2 đường chéo vừa bằng nhau vừa vuông góc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa sơ đồ phân loại, khen ngợi học sinh đã nắm rất chắc tính chất cốt lõi. | **Tổng kết Chương IV:**<br>- **Các hình phẳng đều:** Tam giác đều (3 cạnh bằng nhau, 3 góc bằng $60^\\circ$); Hình vuông (4 cạnh bằng nhau, 4 góc vuông); Lục giác đều (6 cạnh bằng nhau, 6 góc bằng nhau, 3 đường chéo chính bằng nhau).<br>- **Các tứ giác:**<br>+ Hình chữ nhật: Cạnh đối song song và bằng nhau, 4 góc vuông, 2 đường chéo bằng nhau.<br>+ Hình thoi: 4 cạnh bằng nhau, cạnh đối song song, 2 đường chéo vuông góc.<br>+ Hình bình hành: Cạnh đối song song và bằng nhau, góc đối bằng nhau.<br>+ Hình thang cân: Hai đáy song song, hai cạnh bên bằng nhau, hai đường chéo bằng nhau. |

### Hoạt động 2.2: Luyện giải bài tập tổng hợp cuối chương (20 phút)
a) Mục tiêu: Vận dụng thành thạo các kiến thức đã học để giải bài tập 4.28, 4.31, 4.32 SGK trang 97.
b) Nội dung: HS giải bài tập nhận diện hình và bài toán tính diện tích lối đi lát sỏi trong khu đất.
c) Sản phẩm: Lời giải chi tiết của học sinh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao các bài tập tổng hợp:<br>  + **Bài 4.28 (SGK tr.97):** Nhận diện hình trong thực tế.<br>  + **Bài 4.31 (SGK tr.97):** Một khu vườn hình chữ nhật có chiều dài $30\\text{ m}$, chiều rộng $20\\text{ m}$. Ở giữa người ta xây một hồ nước hình tròn hoặc hình vuông cạnh $5\\text{ m}$, phần còn lại trồng cỏ. Tính diện tích phần đất trồng cỏ.<br>  + **Bài 4.32 (SGK tr.97):** Tính diện tích hình thang cân khi biết đáy lớn $10\\text{ cm}$, đáy nhỏ $6\\text{ cm}$ và chiều cao $4\\text{ cm}$.<br>- **HS:** Làm bài theo nhóm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự lực tính toán vào vở bài tập, đối chiếu kết quả với bạn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày Bài 4.31 và 4.32.<br>- Cả lớp nhận xét, bổ sung các bước lập luận.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Sửa bài cẩn thận, chốt lại phương pháp giải quyết các bài toán hình học kết hợp. | **Bài 4.32 (SGK tr.97):**<br>Diện tích hình thang cân là:<br>$S = \\frac{(10 + 6) \\cdot 4}{2} = \\frac{16 \\cdot 4}{2} = 32\\text{ cm}^2$.<br><br>**Bài 4.31 (SGK tr.97):**<br>- Diện tích cả khu vườn hình chữ nhật là:<br>$S_\\text{vườn} = 30 \\cdot 20 = 600\\text{ m}^2$.<br>- Diện tích hồ nước hình vuông cạnh $5\\text{ m}$ là:<br>$S_\\text{hồ} = 5 \\cdot 5 = 25\\text{ m}^2$.<br>- Diện tích phần đất trồng cỏ là:<br>$S_\\text{cỏ} = S_\\text{vườn} - S_\\text{hồ} = 600 - 25 = 575\\text{ m}^2$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (9 phút)
a) Mục tiêu: Vận dụng toàn diện kiến thức để giải bài toán tính tổng chi phí trồng cỏ và làm bờ kè hồ nước.
b) Nội dung: Từ Bài 4.31, tính tổng chi phí biết giá trồng cỏ là $40\\,000\\text{ đồng/m}^2$ và chi phí làm bờ kè quanh hồ hình vuông là $100\\,000\\text{ đồng/m}$.
c) Sản phẩm: Bảng tính chi phí chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tiễn tổng hợp:<br>  Từ kết quả Bài 4.31, người ta muốn:<br>  1. Trồng cỏ trên diện tích $575\\text{ m}^2$ với chi phí $40\\,000$ đồng/$\\text{m}^2$.<br>  2. Xây bờ kè quanh hồ nước hình vuông cạnh $5\\text{ m}$ với chi phí $100\\,000$ đồng/$\\text{m}$.<br>  Hãy tính tổng chi phí cần để hoàn thiện công trình.<br>- **HS:** Đọc đề và phân tích: Phần 1 tính theo diện tích, phần 2 tính theo chu vi hồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính chu vi hồ nước: $C = 4 \\cdot 5 = 20\\text{ m}$. Tính chi phí bờ kè và chi phí trồng cỏ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng thực hiện phép tính tổng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng kết tiết học, khen ngợi tinh thần làm việc tích cực của cả lớp. Dặn dò HS chuẩn bị cho Chương V: Tính đối xứng của hình phẳng trong tự nhiên. | **Bài toán chi phí hoàn thiện:**<br>- Chi phí trồng cỏ là:<br>$575 \\cdot 40\\,000 = 23\\,000\\,000$ (đồng).<br>- Chu vi hồ nước hình vuông là:<br>$C = 4 \\cdot 5 = 20\\text{ m}$.<br>- Chi phí xây bờ kè hồ là:<br>$20 \\cdot 100\\,000 = 2\\,000\\,000$ (đồng).<br>- Tổng chi phí cần chi trả là:<br>$23\\,000\\,000 + 2\\,000\\,000 = 25\\,000\\,000$ (đồng).<br>Đáp số: $25\\,000\\,000$ đồng. |
"""

tasks = [
    ("04_Bai13_TapHopCacSoNguyen_Tiet30-31.md", md_04),
    ("05_Bai14_PhepCongVaPhepTruSoNguyen_Tiet32-34.md", md_05),
    ("06_Bai15_QuyTacDauNgoac_Tiet35-36.md", md_06),
    ("07_OnTapGiuaHK1_HinhHoc_Tiet09.md", md_07),
    ("08_LuyenTapChung_HinhHoc_Tiet11.md", md_08),
    ("09_BaiTapCuoiChuong4_Tiet12.md", md_09),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")

print(">>> ĐÃ TẠO XONG 6 TỆP MARKDOWN CÒN LẠI! <<<")
