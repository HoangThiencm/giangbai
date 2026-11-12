# -*- coding: utf-8 -*-
"""
Script sinh 7 tệp KHBD Markdown môn Toán 6 (Hình học trực quan - Tuần 13 - 18)
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Toan6"
os.makedirs(OUT_DIR, exist_ok=True)

# 09. Bài 21: Hình có trục đối xứng (Tiết 13, 14)
md_09 = """Tiết 13, 14 - BÀI 21: HÌNH CÓ TRỤC ĐỐI XỨNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết được hình có trục đối xứng qua thao tác thực nghiệm (gấp giấy, cắt hoa văn).
- Hiểu được định nghĩa: Đường thẳng $d$ được gọi là trục đối xứng của một hình nếu gấp hình theo đường thẳng $d$ thì hai phần của hình trùng khít lên nhau.
- Chỉ ra và vẽ được trục đối xứng của các hình phẳng quen thuộc: đoạn thẳng (đường trung trực), góc (đường phân giác), tam giác cân (1 trục), tam giác đều (3 trục), hình thang cân (1 trục), hình chữ nhật (2 trục), hình thoi (2 trục), hình vuông (4 trục), hình tròn (vô số trục đối xứng).
- Nhận biết trục đối xứng trong các hình ảnh thiên nhiên (cánh bướm, lá cây), kiến trúc (chùa Một Cột, tháp Rùa), chữ cái và biển báo giao thông.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự gấp giấy, thực hành cắt hình đối xứng và quan sát các vật dụng xung quanh để phát hiện trục đối xứng.
- Giao tiếp và hợp tác: Tự tin trao đổi trong nhóm về số lượng trục đối xứng của từng hình.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh số trục đối xứng giữa hình vuông và hình chữ nhật, hình thoi.
- Năng lực mô hình hóa toán học: Ứng dụng trục đối xứng vào thiết kế họa tiết trang trí đối xứng.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm GeoGebra công cụ 'Reflect about Line' (Đối xứng qua đường thẳng) để dựng ảnh của một hình qua trục đối xứng và kiểm tra tính trùng khít.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS sử dụng ứng dụng AI nhận diện hình ảnh để phân tích tính đối xứng trục trong các công trình kiến trúc nổi tiếng của Việt Nam và thế giới.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, khéo léo, óc thẩm mỹ và tình yêu cái đẹp hài hòa trong tự nhiên.
- Ý thức giữ gìn các nét đẹp văn hóa kiến trúc dân tộc.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, giấy màu, kéo cắt giấy, máy chiếu, các hình ảnh minh họa đối xứng trục trong tự nhiên.
2. Học sinh: SGK Toán 6, vở ghi, giấy thủ công màu, kéo, thước thẳng.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: Khơi gợi sự tò mò và óc quan sát vẻ đẹp cân đối trong tự nhiên (con bướm, lá cây phong).
b) Nội dung: Quan sát ảnh con bướm đậu xòe cánh và trả lời câu hỏi về sự cân xứng hai bên.
c) Sản phẩm: Câu trả lời của học sinh: Hai cánh bướm giống hệt nhau và đối xứng qua thân bướm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu ảnh cận cảnh một chú bướm tuyệt đẹp đang dang cánh. Nêu câu hỏi: Em có nhận xét gì về hình dạng, hoa văn và kích thước của hai bên cánh bướm đối với thân mình của nó?<br>- **HS:** Quan sát và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trao đổi cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời: Hai bên cánh bướm giống hệt nhau về hoa văn, nếu gấp đôi lại theo thân bướm thì hai cánh sẽ úp khít vào nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định: Thân bướm chính là trục đối xứng. Ta cùng tìm hiểu khái niệm Hình có trục đối xứng trong bài học hôm nay. | **Khởi động:**<br>- Tính đối xứng là một vẻ đẹp tự nhiên kỳ diệu.<br>- Khi gấp theo đường trục ở giữa, hai nửa hình trùng khít hoàn toàn lên nhau. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (50 phút)
### Hoạt động 2.1: Khái niệm hình có trục đối xứng (25 phút - Tiết 13)
a) Mục tiêu: Hiểu định nghĩa trục đối xứng qua thực hành gấp giấy cắt trái tim hoặc bông hoa.
b) Nội dung: Tìm hiểu mục 1 SGK trang 98-99; thực hành gấp đôi giấy và cắt hình trái tim.
c) Sản phẩm: Hình trái tim cắt hoàn chỉnh và nhận xét về nếp gấp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát giấy màu, hướng dẫn HS:<br>  1. Gấp đôi tờ giấy theo một đường thẳng $d$.<br>  2. Vẽ một nửa hình trái tim có mép gắn liền với nếp gấp.<br>  3. Dùng kéo cắt theo nét vẽ rồi mở tờ giấy ra.<br>  4. Nhận xét về nếp gấp $d$ đối với hình trái tim vừa cắt được.<br>- **HS:** Nhận giấy và kéo, thực hành theo hướng dẫn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cắt và mở hình trái tim.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS giơ sản phẩm hình trái tim lên. 1 HS phát biểu: Nếp gấp $d$ chia hình trái tim thành hai phần bằng nhau, gấp lại thì trùng khít.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khái quát định nghĩa trục đối xứng của một hình. | **1. Hình có trục đối xứng:**<br>- Đường thẳng $d$ gọi là **trục đối xứng** của một hình nếu gấp hình theo đường thẳng $d$ thì hai phần của hình trùng khít lên nhau.<br>- Hình có tính chất như vậy gọi là **hình có trục đối xứng**.<br>Ví dụ:<br>+ Hình trái tim có 1 trục đối xứng.<br>+ Tháp Rùa (Hà Nội) có trục đối xứng đứng. |

### Hoạt động 2.2: Trục đối xứng của các hình hình học quen thuộc (25 phút - Tiết 14)
a) Mục tiêu: Xác định chính xác số lượng và vẽ được trục đối xứng của đoạn thẳng, tam giác đều, hình vuông, hình chữ nhật, hình tròn.
b) Nội dung: Tìm hiểu mục 2 SGK trang 100-101; làm Luyện tập 2.
c) Sản phẩm: Bảng tổng kết số trục đối xứng của các hình phẳng trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu các hình phẳng: Đoạn thẳng $AB$, Tam giác đều, Hình chữ nhật, Hình thoi, Hình vuông, Hình tròn. Yêu cầu các nhóm xác định số trục đối xứng của từng hình.<br>- **HS:** Thảo luận nhóm 4 người.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Dùng thước và bút chì vẽ nháp các đường trục đối xứng của từng hình.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện các nhóm lên bảng vẽ trục đối xứng cho từng hình:<br>  + Đoạn thẳng: 1 trục đối xứng (đường trung trực).<br>  + Tam giác đều: 3 trục đối xứng.<br>  + Hình chữ nhật: 2 trục đối xứng (nối trung điểm các cạnh đối).<br>  + Hình thoi: 2 trục đối xứng (hai đường chéo).<br>  + Hình vuông: 4 trục đối xứng (2 đường chéo và 2 đường nối trung điểm).<br>  + Hình tròn: Vô số trục đối xứng (mọi đường thẳng đi qua tâm).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng tổng kết số trục đối xứng. | **2. Trục đối xứng của một số hình:**<br>- **Đoạn thẳng:** 1 trục đối xứng (đường trung trực).<br>- **Tam giác cân:** 1 trục đối xứng.<br>- **Tam giác đều:** 3 trục đối xứng.<br>- **Hình thang cân:** 1 trục đối xứng.<br>- **Hình chữ nhật:** 2 trục đối xứng.<br>- **Hình thoi:** 2 trục đối xứng (là 2 đường chéo).<br>- **Hình vuông:** 4 trục đối xứng.<br>- **Hình tròn:** Vô số trục đối xứng (mỗi đường thẳng đi qua tâm là một trục đối xứng). |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (23 phút)
a) Mục tiêu: Nhận biết chữ cái và biển báo giao thông có trục đối xứng.
b) Nội dung: Giải bài tập 5.1, 5.2, 5.3 SGK trang 101-102.
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho các chữ cái in hoa: A, B, C, D, H, M, O, X, Y. Yêu cầu HS chỉ ra chữ cái có 1 trục đối xứng, chữ có 2 trục đối xứng và vẽ trục.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ các chữ in hoa vào vở và kẻ trục đối xứng bằng bút đỏ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng kẻ trục đối xứng cho chữ A (trục đứng), B (trục ngang), H (2 trục), O (vô số trục).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Sửa bài cẩn thận, khen ngợi học sinh nhận biết rất tinh tế. | **Bài 5.1 (SGK tr.101):**<br>- Chữ cái có 1 trục đối xứng đứng: A, M, Y, T, V, U.<br>- Chữ cái có 1 trục đối xứng ngang: B, C, D, E.<br>- Chữ cái có 2 trục đối xứng (đứng và ngang): H, X.<br>- Chữ O: có vô số trục đối xứng (như hình tròn). |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
a) Mục tiêu: Ứng dụng cắt giấy hoa văn đối xứng trang trí lớp học hoặc làm thiệp chúc mừng.
b) Nội dung: Thực hành gấp giấy làm 4 và cắt hoa văn 4 cánh đối xứng.
c) Sản phẩm: Bông hoa tuyết hoặc hoa văn trang trí của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn gấp giấy hình vuông làm 4 (gấp đôi 2 lần) rồi cắt một số đường viền tùy ý. Mở ra sẽ được hoa văn có 4 trục đối xứng.<br>- **HS:** Hào hứng thực hành.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự do sáng tạo đường cắt.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Trưng bày các sản phẩm hoa văn đẹp mắt lên bảng lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng kết tiết học, dặn dò chuẩn bị cho Bài 22: Hình có tâm đối xứng. | **Vận dụng thực tế:**<br>- Ứng dụng cắt hoa văn đối xứng trong nghệ thuật trang trí dân gian, làm thiệp mừng và thiết kế logo. |
"""

# 10. Bài 22: Hình có tâm đối xứng (Tiết 15, 16)
md_10 = """Tiết 15, 16 - BÀI 22: HÌNH CÓ TÂM ĐỐI XỨNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết được hình có tâm đối xứng qua thao tác thực nghiệm (quay nửa vòng quanh một điểm).
- Hiểu được định nghĩa: Điểm $O$ được gọi là tâm đối xứng của một hình nếu quay hình đó nửa vòng (góc $180^\\circ$) quanh điểm $O$ thì hình thu được trùng khít với chính hình ban đầu.
- Xác định và chỉ ra được tâm đối xứng của các hình phẳng quen thuộc:
  + Đoạn thẳng: Trung điểm của đoạn thẳng là tâm đối xứng.
  + Hình bình hành, hình thoi, hình chữ nhật, hình vuông: Giao điểm của hai đường chéo là tâm đối xứng.
  + Hình tròn: Tâm của hình tròn chính là tâm đối xứng.
  + Lục giác đều: Giao điểm của các đường chéo chính là tâm đối xứng.
- Phân biệt rõ hình có trục đối xứng và hình có tâm đối xứng (ví dụ: hình bình hành có tâm đối xứng nhưng không có trục đối xứng; tam giác đều có 3 trục đối xứng nhưng không có tâm đối xứng).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự làm chong chóng hoặc quay cánh quạt để cảm nhận tâm đối xứng.
- Giao tiếp và hợp tác: Tự tin phản biện, phân biệt giữa trục đối xứng và tâm đối xứng trong nhóm học tập.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích vì sao tâm đường tròn hay giao điểm hai đường chéo là tâm đối xứng.
- Năng lực mô hình hóa toán học: Nhận diện tâm đối xứng trong các thiết bị công nghệ (chong chóng, cánh quạt, bánh xe, la bàn).

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng phần mềm GeoGebra công cụ 'Rotate around Point' (Quay quanh điểm một góc 180 độ) để kiểm chứng tính chất tâm đối xứng của hình bình hành và hình chữ nhật.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để phân tích thiết kế logo của các thương hiệu lớn xem logo nào có tâm đối xứng, logo nào có trục đối xứng.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, tinh tế trong quan sát hình học.
- Yêu thích môn học, trân trọng các phát minh ứng dụng tính đối xứng tâm trong đời sống kỹ thuật.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 6 Tập 1, KHBD, mô hình chong chóng 2 cánh, 4 cánh, máy chiếu, hình ảnh logo các hãng xe.
2. Học sinh: SGK Toán 6, vở ghi, compa, thước kẻ.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: Xuất phát từ chuyển động quay của chong chóng hoặc cánh quạt gió để hình thành khái niệm tâm đối xứng.
b) Nội dung: Quan sát chong chóng 2 cánh khi quay nửa vòng quanh trục ghim.
c) Sản phẩm: Nhận xét của học sinh về vị trí hai cánh sau khi quay nửa vòng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cầm một chiếc chong chóng 2 cánh (hoặc cánh quạt trần 2 cánh), đánh dấu một đầu cánh màu đỏ, một đầu màu xanh. Quay chong chóng nửa vòng ($180^\\circ$). Đặt câu hỏi: Hình dạng của chong chóng sau khi quay nửa vòng có trùng khít với hình ban đầu không?<br>- **HS:** Quan sát chuyển động.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trao đổi cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời: Chong chóng sau khi quay nửa vòng vẫn có hình dạng y hệt như ban đầu, vị trí hai cánh đổi chỗ cho nhau nhưng tổng thể hình vẫn trùng khít.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định điểm chốt ở giữa chính là Tâm đối xứng. Bài học hôm nay ta cùng tìm hiểu: Hình có tâm đối xứng. | **Khởi động:**<br>- Điểm cố định ở giữa giúp hình quay nửa vòng trùng khít với chính nó gọi là Tâm đối xứng. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (50 phút)
### Hoạt động 2.1: Khái niệm hình có tâm đối xứng (25 phút - Tiết 15)
a) Mục tiêu: Nắm vững định nghĩa tâm đối xứng qua thao tác quay nửa vòng quanh điểm $O$.
b) Nội dung: Đọc mục 1 SGK trang 103-104; thực hiện HĐ1, HĐ2.
c) Sản phẩm: Định nghĩa tâm đối xứng và kết quả HĐ2.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa:<br>  Điểm $O$ gọi là **tâm đối xứng** của một hình nếu quay hình đó nửa vòng (góc $180^\\circ$) quanh điểm $O$ thì hình thu được trùng khít với chính nó.<br>  Hình có tính chất như vậy gọi là **hình có tâm đối xứng**.<br>- **GV:** Đặt câu hỏi: Trong các chữ cái in hoa sau: N, S, Z, H, O, chữ nào có tâm đối xứng?<br>- **HS:** Đọc SGK và thảo luận nhóm đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thử quay ngược trang vở $180^\\circ$ để kiểm tra chữ nào nhìn vẫn như cũ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS phát hiện: Chữ N, S, Z, H, O khi quay ngược $180^\\circ$ vẫn giữ nguyên hình dạng $\\rightarrow$ đều có tâm đối xứng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương mẹo quay vở rất thông minh của học sinh, chuẩn hóa khái niệm. | **1. Hình có tâm đối xứng:**<br>- Điểm $O$ là tâm đối xứng của một hình nếu quay hình nửa vòng quanh $O$, hình thu được trùng khít với chính nó.<br>- Mẹo nhận biết: Quay hình một góc $180^\\circ$ (lộn ngược đầu), nếu hình không đổi thì hình đó có tâm đối xứng.<br>Ví dụ: Các chữ cái N, S, Z, H, O có tâm đối xứng. |

### Hoạt động 2.2: Tâm đối xứng của các hình hình học quen thuộc (25 phút - Tiết 16)
a) Mục tiêu: Xác định chính xác tâm đối xứng của đoạn thẳng, hình bình hành, hình thoi, hình chữ nhật, hình vuông, hình tròn.
b) Nội dung: Đọc mục 2 SGK trang 105-106; làm Luyện tập 2.
c) Sản phẩm: Vị trí tâm đối xứng của từng hình phẳng trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu các hình phẳng và hỏi vị trí tâm đối xứng:<br>  1. Tâm đối xứng của đoạn thẳng $AB$ là điểm nào?<br>  2. Tâm đối xứng của hình bình hành, hình thoi, hình chữ nhật, hình vuông là điểm nào?<br>  3. Tâm đối xứng của hình tròn là điểm nào?<br>  4. Tam giác đều và hình thang cân có tâm đối xứng không?<br>- **HS:** Thảo luận nhóm 4 người.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận, vẽ hình và xác định tâm đối xứng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm lên bảng vẽ và giải thích:<br>  + Đoạn thẳng: trung điểm $I$.<br>  + Các hình tứ giác đặc biệt: giao điểm $O$ của hai đường chéo.<br>  + Hình tròn: tâm $O$.<br>  + Tam giác đều và hình thang cân KHÔNG có tâm đối xứng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa bảng ghi nhớ tâm đối xứng. | **2. Tâm đối xứng của một số hình:**<br>- **Đoạn thẳng:** Trung điểm của đoạn thẳng là tâm đối xứng.<br>- **Hình bình hành, hình thoi, hình chữ nhật, hình vuông:** Giao điểm của hai đường chéo là tâm đối xứng.<br>- **Hình tròn:** Tâm của hình tròn là tâm đối xứng.<br>- **Lục giác đều:** Giao điểm của các đường chéo chính là tâm đối xứng.<br>- **Lưu ý:** Tam giác đều và hình thang cân **không có** tâm đối xứng. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (23 phút)
a) Mục tiêu: Nhận biết hình có tâm đối xứng trong tự nhiên, hoa văn, biển báo giao thông.
b) Nội dung: Giải bài tập 5.5, 5.6, 5.7 SGK trang 107.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu bài tập 5.5 và 5.6 SGK trang 107: Nhận biết hình có tâm đối xứng trong các biển báo giao thông.<br>- **HS:** Quan sát và làm bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định biển báo cấm đi ngược chiều, biển báo nguy hiểm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS đứng tại chỗ trả lời và giải thích vị trí tâm đối xứng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt đáp án, nhấn mạnh ý nghĩa an toàn của biển báo giao thông. | **Bài 5.5, 5.6 (SGK tr.107):**<br>- Biển báo đường cấm (hình tròn đỏ): có tâm đối xứng.<br>- Biển báo cấm đi ngược chiều (hình tròn đỏ có vạch trắng ngang ở giữa): vừa có trục đối xứng, vừa có tâm đối xứng. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
a) Mục tiêu: Phân biệt rõ hình có trục đối xứng, hình có tâm đối xứng, hình có cả hai tính chất.
b) Nội dung: Hoàn thành bảng phân loại hình học tổng hợp.
c) Sản phẩm: Bảng phân loại của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho 5 hình: Tam giác đều, Hình thang cân, Hình bình hành, Hình chữ nhật, Hình thoi. Điền vào bảng:<br>  + Chỉ có trục đối xứng.<br>  + Chỉ có tâm đối xứng.<br>  + Vừa có trục, vừa có tâm đối xứng.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành bảng vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đọc kết quả phân loại.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi học sinh nắm bài chắc chắn. Dặn dò ôn tập chuẩn bị cho tiết Luyện tập chung. | **Bảng phân loại tổng hợp:**<br>1. Chỉ có trục đối xứng: Tam giác đều, Hình thang cân.<br>2. Chỉ có tâm đối xứng: Hình bình hành.<br>3. Vừa có trục đối xứng, vừa có tâm đối xứng: Hình chữ nhật, Hình thoi, Hình vuông, Hình tròn. |
"""

tasks = [
    ("09_KHBD_Toan6_Bai21_HinhCoTrucDoiXung_Tiet13-14.md", md_09),
    ("10_KHBD_Toan6_Bai22_HinhCoTamDoiXung_Tiet15-16.md", md_10),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
