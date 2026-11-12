# -*- coding: utf-8 -*-
import os

out_dir = r"C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\1_SOAN_KHBD\Ket_qua\05.11"

# 4. Cô Lê Thị Bình (Toán 8)
md_04 = """Tiết 24 - BÀI 15: ĐỊNH LÍ THALÈS TRONG TAM GIÁC
*Thời lượng thực hiện: 01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12 (Luyện tập ứng dụng)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và vận dụng thành thạo định lí Thalès thuận, định lí Thalès đảo và hệ quả trong tam giác.
- Biết cách lập các tỉ số đoạn thẳng tương ứng tỉ lệ khi có đường thẳng song song với một cạnh của tam giác.
- Vận dụng tính độ dài đoạn thẳng và giải bài toán thực tế đo gián tiếp khoảng cách.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác thực hiện các bài tập trên phiếu học tập, chủ động tương tác với mô phỏng trên DlibK12.
- Giao tiếp và hợp tác: Thảo luận nhóm hiệu quả, biết phản biện và thống nhất cách chọn tỉ số tối ưu.

b) Năng lực Toán học:
- Tư duy và lập luận hình học: Chứng minh quan hệ song song dựa vào định lí Thalès đảo.
- Mô hình hóa toán học: Chuyển bài toán đo khoảng cách thực tế giữa hai bờ kênh thành bài toán hình học tam giác.

c) Năng lực số (NLS):
- ***(Tích hợp NLS 5.3.TC2a: Khai thác tệp mô phỏng hình học GeoGebra nhúng trên DlibK12 qua màn hình Tivi Thư viện để kiểm chứng tỉ số đoạn thẳng)***.

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***(Tích hợp AI 6.B2.1: Quan sát công cụ kiểm chứng tỉ số số học tự động trên giao diện học liệu số DlibK12)***.

## 3. Về phẩm chất
- Chăm chỉ: Cẩn thận trong vẽ hình và thay số tính toán.
- Trách nhiệm: Nghiêm túc hoàn thành nhiệm vụ nhóm, giữ gìn trật tự và bảo quản thiết bị Thư viện.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Màn hình Tivi Thư viện kết nối Laptop GV; Tệp mô phỏng Thalès nhúng trên DlibK12.
- SGK Toán 8 Tập 1; Phiếu học tập số 1 và số 2.
2. Học sinh:
- SGK Toán 8 Tập 1, vở ghi, máy tính cầm tay, thước kẻ, compa.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Nhắc lại 3 hệ thức tỉ số của định lí Thalès thuận và điều kiện áp dụng.
b) Nội dung: Quan sát hình vẽ trên Tivi Thư viện và phát biểu các cặp tỉ số tương ứng.
c) Sản phẩm: Câu trả lời chính xác của học sinh về các hệ thức Thalès.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình tam giác $ABC$ có $MN // BC$ trên màn hình Tivi Thư viện. Yêu cầu học sinh viết 3 hệ thức Thalès.<br>- **HS:** Quan sát hình và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhớ lại kiến thức, trao đổi nhanh với bạn cùng bàn.<br>- **GV:** Quan sát, khích lệ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đứng tại chỗ phát biểu: $\\frac{AM}{AB} = \\frac{AN}{AC}$; $\\frac{AM}{MB} = \\frac{AN}{NC}$; $\\frac{MB}{AB} = \\frac{NC}{AC}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kiến thức và dẫn dắt vào bài luyện tập ứng dụng. | **Khởi động:**<br>- Xét $\\Delta ABC$ có $MN // BC$ ($M \\in AB, N \\in AC$).<br>- Hệ thức Thalès:<br>$\\frac{AM}{AB} = \\frac{AN}{AC}$; $\\frac{AM}{MB} = \\frac{AN}{NC}$; $\\frac{MB}{AB} = \\frac{NC}{AC}$. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI / KHÁM PHÁ TRÊN DLIBK12 (15 phút)
a) Mục tiêu: Trực quan hóa định lí Thalès đảo và kỹ thuật chọn tỉ số phù hợp.
b) Nội dung: Khai thác tệp mô phỏng tương tác trên DlibK12; giải bài tập chứng minh song song.
c) Sản phẩm: Lời giải bài toán chứng minh song song trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu tệp mô phỏng GeoGebra từ DlibK12 lên Tivi Thư viện. Cho $\\Delta ABC$, lấy $M \\in AB, N \\in AC$ sao cho $AM = 3, MB = 2, AN = 4.5, NC = 3$. Đặt câu hỏi: "$MN$ có song song với $BC$ không?".<br>- ***(Tích hợp NLS 5.3.TC2a: GV chạm kéo điểm trên màn hình Tivi cho HS thấy khi tỉ số bằng nhau thì hai đường thẳng luôn song song)***.<br>- **HS:** Tiếp nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính tỉ số $\\frac{AM}{MB} = \\frac{3}{2} = 1.5$ và $\\frac{AN}{NC} = \\frac{4.5}{3} = 1.5$. Thấy hai tỉ số bằng nhau.<br>- **GV:** Gợi ý vận dụng định lí Thalès đảo.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm phát biểu: Do $\\frac{AM}{MB} = \\frac{AN}{NC}$ nên theo định lí Thalès đảo, ta có $MN // BC$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách trình bày định lí Thalès đảo. Nhắc nhở điều kiện bắt buộc để chứng minh song song. | **Định lí Thalès đảo:**<br>- Xét $\\Delta ABC$ có $M \\in AB, N \\in AC$.<br>Ta có: $\\frac{AM}{MB} = \\frac{3}{2}$ và $\\frac{AN}{NC} = \\frac{4.5}{3} = \\frac{3}{2}$.<br>Suy ra $\\frac{AM}{MB} = \\frac{AN}{NC}$.<br>Theo định lí Thalès đảo $\\Rightarrow MN // BC$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP / THỰC HÀNH TƯƠNG TÁC (18 phút)
a) Mục tiêu: Vận dụng định lí Thalès tính độ dài đoạn thẳng và giải toán nhóm.
b) Nội dung: Hoàn thành bài toán tính khoảng cách trên Phiếu học tập số 1.
c) Sản phẩm: Lời giải chi tiết của Bài 1 và Bài 2 trên Phiếu học tập.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát Phiếu học tập số 1 cho các nhóm. Đề bài: Cho $\\Delta DEF, PQ // EF$ ($P \\in DE, Q \\in DF$). Biết $DP = 4\\text{ cm}, PE = 6\\text{ cm}, DQ = 5\\text{ cm}$. Tính độ dài $QF$ và $DF$.<br>- **HS:** Nhận phiếu học tập, phân công làm bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm thảo luận, lập tỉ lệ thức $\\frac{DP}{PE} = \\frac{DQ}{QF} \\Rightarrow \\frac{4}{6} = \\frac{5}{QF} \\Rightarrow QF = 7.5\\text{ cm}$. Tính $DF = DQ + QF = 12.5\\text{ cm}$.<br>- **GV:** Theo dõi, hướng dẫn học sinh trình bày chặt chẽ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm 2 lên bảng Tivi Thư viện ghi lời giải.<br>- **GV:** Cho các nhóm khác nhận xét.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt đáp án, biểu dương các nhóm làm đúng và nhanh. | **Bài tập luyện tập:**<br>- Xét $\\Delta DEF$ có $PQ // EF$.<br>Theo định lí Thalès: $\\frac{DP}{PE} = \\frac{DQ}{QF}$<br>Thay số: $\\frac{4}{6} = \\frac{5}{QF} \\Rightarrow QF = \\frac{6 \\cdot 5}{4} = 7.5\\text{ (cm)}$.<br>Độ dài $DF = DQ + QF = 5 + 7.5 = 12.5\\text{ (cm)}$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (7 phút)
a) Mục tiêu: Giải bài toán thực tế đo khoảng cách hai điểm bị ngăn cách bởi bờ kênh; nộp sản phẩm lưu hồ sơ.
b) Nội dung: Giải bài toán ứng dụng thực tế trên Phiếu học tập số 1; nộp phiếu về Thư viện.
c) Sản phẩm: Phiếu học tập hoàn thiện của các nhóm nộp tại bàn thủ thư.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu sơ đồ đo chiều rộng khúc sông bằng cọc ngắm lên Tivi Thư viện. Yêu cầu các nhóm hoàn thành câu hỏi Vận dụng.<br>- **HS:** Quan sát mô hình thực tế và làm bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vận dụng định lí Thalès lập tỉ số tính chiều rộng sông $x = 24\\text{ m}$.<br>- **GV:** Kiểm tra, hướng dẫn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm đọc to kết quả và lập luận.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Đánh giá tiết học thành công; thu phiếu học tập bàn giao cho cán bộ Thư viện lưu minh chứng. | **Vận dụng thực tế:**<br>- Ứng dụng định lí Thalès đo khoảng cách không tới được.<br>- 100% nhóm hoàn thành và nộp sản phẩm lưu hồ sơ Thư viện theo KH 115. |

# IV. PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN

## 1. Phiếu học tập số 1: Luyện tập định lí Thalès
**TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN TIN — THƯ VIỆN SỐ**  
*Lớp: 8/1 — Nhóm số: ......*  

- **Bài 1:** Cho $\\Delta DEF, PQ // EF$. Biết $DP = 4\\text{ cm}, PE = 6\\text{ cm}, DQ = 5\\text{ cm}$.  
  + Tính độ dài $QF = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  + Tính độ dài $DF = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  

- **Bài 2 (Thực tế):** Hai bạn An và Bình muốn đo khoảng cách $AB$ qua một cái hồ. Các bạn cắm cọc tạo thành $\\Delta ABC$ có $MN // BC$ ($M \\in AB, N \\in AC$). Đo được $AM = 12\\text{ m}, MB = 8\\text{ m}, MN = 15\\text{ m}$. Tính khoảng cách $BC = \\dots\\dots\\dots\\dots\\dots\\dots\\text{ m}$.  

## 2. Sản phẩm học tập minh chứng hoàn chỉnh (Lưu hồ sơ Thư viện theo KH 115)
- **Đáp án Bài 1:** $QF = 7.5\\text{ cm}; DF = 12.5\\text{ cm}$.  
- **Đáp án Bài 2:** Theo hệ quả định lí Thalès: $\\frac{AM}{AB} = \\frac{MN}{BC} \\Rightarrow \\frac{12}{20} = \\frac{15}{BC} \\Rightarrow BC = 25\\text{ m}$.  
- **Tình trạng bàn giao:** Đã nộp 08 Phiếu học tập của 08 nhóm học sinh lớp 8/1 cho Thư viện lưu trữ.
"""

# 5. Thầy Hoàng Xuân Ánh (Toán 7)
md_05 = """Tiết 29 - BÀI 10: TIÊN ĐỀ EUCLID VÀ TÍNH CHẤT HAI ĐƯỜNG THẲNG SONG SONG
*Thời lượng thực hiện: 01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu và phát biểu được nội dung tiên đề Euclid về đường thẳng song song.
- Nắm vững tính chất của hai đường thẳng song song: Nếu một đường thẳng cắt hai đường thẳng song song thì hai góc so le trong bằng nhau, hai góc đồng vị bằng nhau.
- Vận dụng tính chất để tính số đo góc và giải thích các hiện tượng thực tế.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Chủ động nghiên cứu bài học trên DlibK12, tự giác làm bài tập.
- Giao tiếp và hợp tác: Tương tác tích cực với bạn học và giáo viên qua màn hình Tivi Thư viện.

b) Năng lực Toán học:
- Tư duy và lập luận toán học: Suy luận tính bằng nhau của các góc từ quan hệ song song.
- Giao tiếp toán học: Diễn đạt đúng các thuật ngữ so le trong, đồng vị, trong cùng phía.

c) Năng lực số (NLS):
- ***(Tích hợp NLS 1.1.TC1a: Khai thác mô phỏng 3D hình học tương tác trên DlibK12 chiếu trên Tivi Thư viện)***.
- ***(Tích hợp NLS 2.2.TC1b: Hợp tác giải bài tập trắc nghiệm trực tuyến qua phần mềm Thư viện số)***.

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***(Tích hợp AI 1.B1.1: Tiếp cận mô hình nhận diện đường thẳng song song tự động trong xử lý ảnh giao thông)***.

## 3. Về phẩm chất
- Chăm chỉ: Cẩn thận trong đo góc và vẽ hình.
- Trách nhiệm: Ý thức kỷ luật tốt trong phòng đọc Thư viện số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Màn hình Tivi Thư viện kết nối Laptop GV; Mô phỏng góc song song trên DlibK12.
- SGK Toán 7 Tập 1; Thước đo góc; Phiếu học tập số 1.
2. Học sinh:
- SGK Toán 7 Tập 1, vở ghi, thước thẳng, thước đo độ.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Gợi mở vấn đề về tính duy nhất của đường thẳng song song qua một điểm ngoài đường thẳng.
b) Nội dung: Vẽ hình theo yêu cầu và trả lời câu hỏi: Qua điểm $A$ ngoài đường thẳng $d$, vẽ được bao nhiêu đường thẳng song song với $d$?
c) Sản phẩm: Câu trả lời khẳng định chỉ vẽ được duy nhất 1 đường thẳng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu lên Tivi Thư viện hình ảnh điểm $A$ nằm ngoài đường thẳng $a$. Yêu cầu học sinh vẽ đường thẳng đi qua $A$ và song song với $a$. Hỏi có bao nhiêu đường thẳng như vậy?<br>- **HS:** Vẽ hình vào nháp.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác vẽ hình.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời: "Chỉ vẽ được duy nhất một đường thẳng".<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định đó chính là nội dung Tiên đề Euclid nổi tiếng và dẫn dắt vào bài. | **Tiên đề Euclid:**<br>Qua một điểm ở ngoài một đường thẳng, chỉ có một đường thẳng song song với đường thẳng đó. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI / KHÁM PHÁ TRÊN DLIBK12 (15 phút)
a) Mục tiêu: Khắc sâu tính chất hai góc so le trong và hai góc đồng vị bằng nhau.
b) Nội dung: Xem mô phỏng tương tác trên DlibK12, đo các góc tạo bởi đường thẳng cắt hai đường thẳng song song.
c) Sản phẩm: Kết luận tính chất hai đường thẳng song song trong vở ghi.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Mở phần mềm đo góc tương tác trên DlibK12 chiếu lên Tivi Thư viện. Xoay đường thẳng cắt và yêu cầu học sinh đọc số đo góc so le trong và đồng vị.<br>- ***(Tích hợp NLS 1.1.TC1a: HS quan sát số đo hai góc so le trong luôn luôn bằng nhau dù vị trí xoay thay đổi)***.<br>- **HS:** Quan sát và so sánh số đo.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ghi nhận số liệu: $\\widehat{A_1} = 60^\\circ, \\widehat{B_3} = 60^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Rút ra nhận xét: Hai góc so le trong bằng nhau, hai góc đồng vị bằng nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa tính chất hai đường thẳng song song. | **Tính chất hai đường thẳng song song:**<br>Nếu một đường thẳng cắt hai đường thẳng song song thì:<br>- Hai góc so le trong bằng nhau.<br>- Hai góc đồng vị bằng nhau. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP / THỰC HÀNH TƯƠNG TÁC (18 phút)
a) Mục tiêu: Tính được số đo các góc còn lại khi biết một góc tạo bởi hai đường thẳng song song.
b) Nội dung: Hoàn thành bài tập trên Phiếu học tập số 1; giải trắc nghiệm số trên Tivi Thư viện.
c) Sản phẩm: Lời giải tính góc của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát Phiếu học tập số 1. Cho hình vẽ $a // b$, đường thẳng $c$ cắt $a$ tại $A$, cắt $b$ tại $B$. Biết $\\widehat{A_4} = 75^\\circ$. Tính các góc còn lại tại đỉnh $B$.<br>- **HS:** Nhận phiếu học tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm thảo luận, vận dụng tính chất so le trong $\\widehat{B_2} = \\widehat{A_4} = 75^\\circ$; đồng vị $\\widehat{B_4} = \\widehat{A_4} = 75^\\circ$; góc kề bù $\\widehat{B_1} = 180^\\circ - 75^\\circ = 105^\\circ$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm lên ghi kết quả trên bảng Tivi.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt đáp án, sửa lỗi trình bày lập luận hình học. | **Luyện tập tính góc:**<br>Do $a // b$ nên:<br>- $\\widehat{B_2} = \\widehat{A_4} = 75^\\circ$ (so le trong).<br>- $\\widehat{B_4} = \\widehat{A_4} = 75^\\circ$ (đồng vị).<br>- $\\widehat{B_1} = 180^\\circ - \\widehat{B_2} = 105^\\circ$ (kề bù). |

## D. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (7 phút)
a) Mục tiêu: Giải thích ứng dụng đường song song trong thiết kế thanh ray xe lửa hoặc cầu đường.
b) Nội dung: Trả lời câu hỏi thực tế trên Phiếu học tập số 1; bàn giao phiếu cho Thư viện.
c) Sản phẩm: Phiếu học tập hoàn thiện của các nhóm nộp lại bàn thủ thư.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh đường ray tàu hỏa và thang leo. Hỏi: "Nếu hai thanh ray không song song thì điều gì sẽ xảy ra?".<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Hoàn thành phần trả lời vào phiếu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời: Bánh tàu hỏa có khoảng cách cố định, nếu hai thanh ray không song song thì tàu sẽ bị trật bánh.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Tổng kết tiết học; thu phiếu nộp cán bộ Thư viện lưu hồ sơ theo Kế hoạch 115. | **Vận dụng thực tế:**<br>- Đường song song đảm bảo khoảng cách không đổi giữa hai thanh ray, giúp phương tiện di chuyển an toàn.<br>- Bàn giao đủ phiếu học tập lưu hồ sơ Thư viện. |

# IV. PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN

## 1. Phiếu học tập số 1: Tiên đề Euclid và tính góc
**TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN TIN — THƯ VIỆN SỐ**  
*Lớp: 7/2 — Nhóm số: ......*  

- **Bài 1:** Cho hình vẽ có $a // b$. Biết $\\widehat{A_4} = 75^\\circ$.  
  + Góc so le trong với $\\widehat{A_4}$ là góc nào? Số đo là bao nhiêu? ......................................................  
  + Tính số đo góc $\\widehat{B_1}$ (kề bù với $\\widehat{B_2}$): ............................................................................  

- **Bài 2 (Thực tế):** Hãy nêu 2 hình ảnh thực tế về hai đường thẳng song song trong trường học của em:  
  1) ....................................................................................................................................................  
  2) ....................................................................................................................................................  

## 2. Sản phẩm học tập minh chứng hoàn chỉnh (Lưu hồ sơ Thư viện theo KH 115)
- **Đáp án Bài 1:** $\\widehat{B_2} = 75^\\circ$ (so le trong); $\\widehat{B_1} = 105^\\circ$.  
- **Đáp án Bài 2:** Hai mép của bảng đen; hai thanh đối diện của khung cửa sổ lớp học.  
- **Tình trạng bàn giao:** Đã nộp 08 bản Phiếu học tập của 08 nhóm học sinh lớp 7/2 về Thư viện lưu trữ.
"""

# 6. Thầy Trần Long Hải (Toán 8)
md_06 = """Tiết 18 - BÀI 15: ĐỊNH LÍ THALÈS TRONG TAM GIÁC
*Thời lượng thực hiện: 01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12 (STEM Đo bóng nắng thực tế)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu nguyên lý toán học ứng dụng định lí Thalès và tam giác đồng dạng để đo gián tiếp chiều cao vật thể thực tế.
- Biết lập tỉ lệ thức giữa chiều cao cọc và bóng cọc, chiều cao vật thể và bóng vật thể dưới ánh nắng mặt trời.
- Xử lý số liệu đo đạc thực nghiệm, tính toán sai số và rút ra kết luận.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự chuẩn bị dụng cụ đo, chủ động phân công nhiệm vụ thực nghiệm nhóm.
- Giao tiếp và hợp tác: Phối hợp nhịp nhàng giữa bạn giữ cọc, bạn kéo thước đo bóng và bạn ghi số liệu.

b) Năng lực Toán học:
- Năng lực mô hình hóa toán học: Chuyển đổi vật thể thực (cột cờ, tòa nhà Thư viện) thành mô hình toán học tam giác vuông có các tia nắng song song.
- Giải quyết vấn đề toán học: Tính chiều cao vật thể từ các số đo thực nghiệm.

c) Năng lực số (NLS):
- ***(Tích hợp NLS 3.1.TC2a: Học sinh xem video hướng dẫn kỹ thuật đo ngoài trời trên DlibK12 và nhập số liệu đo vào bảng tính số trên Tivi Thư viện)***.

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***(Tích hợp AI 4.B2.1: Nhận diện hiện tượng sai số thực nghiệm do độ nghiêng mặt đất và sự thay đổi góc chiếu mặt trời)***.

## 3. Về phẩm chất
- Chăm chỉ: Nghiêm túc, cẩn trọng trong đo đạc thực địa.
- Trung thực: Ghi chép trung thực số liệu đo được, không chỉnh sửa số liệu tùy tiện.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Màn hình Tivi Thư viện kết nối Laptop GV; Video kỹ thuật đo gián tiếp trên DlibK12.
- Thước dây cuộn 10m; Cọc ngắm tiêu chuẩn 1.5m có gắn dây dọi; SGK Toán 8 Tập 1.
2. Học sinh:
- Phiếu báo cáo thực nghiệm STEM; Máy tính cầm tay; Thước dây cá nhân.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Nhắc lại phương pháp Thalès đo kim tự tháp và phổ biến nhiệm vụ đo chiều cao cột cờ trường.
b) Nội dung: Xem lại clip 2 phút trên DlibK12 về mô hình đo bóng nắng của Thalès.
c) Sản phẩm: Học sinh nhắc lại được công thức $\\frac{h_1}{h_2} = \\frac{b_1}{b_2}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Bật Tivi Thư viện chiếu lại sơ đồ Thalès đo bóng nắng. Nêu nhiệm vụ: "Hôm nay chúng ta sẽ đo chiều cao cột cờ trước sân Thư viện bằng cọc tiêu $1.5\\text{ m}$ và thước dây".<br>- **HS:** Lắng nghe và tiếp nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại công thức tính chiều cao vật thể: $H = h_{cọc} \\cdot \\frac{Bóng_{cột cờ}}{Bóng_{cọc}}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm nêu điều kiện: Cọc và cột cờ phải vuông góc với mặt đất, cùng đo tại một thời điểm nắng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định chính xác và chuyển giao thiết bị đo cho các nhóm. | **Nguyên lý đo bóng nắng:**<br>- Do tia nắng mặt trời song song nên:<br>$\\frac{H_{cột cờ}}{H_{cọc}} = \\frac{Bóng_{cột cờ}}{Bóng_{cọc}}$<br>$\\Rightarrow H_{cột cờ} = H_{cọc} \\cdot \\frac{Bóng_{cột cờ}}{Bóng_{cọc}}$. |

## B. HOẠT ĐỘNG 2: HƯỚNG DẪN KỸ THUẬT & MÔ PHỎNG TRÊN DLIBK12 (15 phút)
a) Mục tiêu: Học sinh nắm vững 4 bước thực hiện đo đạc và cách ghi số liệu thực nghiệm.
b) Nội dung: Xem video hướng dẫn quy trình đo trên DlibK12; phân tích các vị trí đo và cách khắc phục sai số.
c) Sản phẩm: Bảng phân công nhiệm vụ và quy trình đo được ghi vào Phiếu thực nghiệm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu video kỹ thuật đo mẫu trên DlibK12 lên Tivi Thư viện. Hướng dẫn cách dùng dây dọi giữ cọc thẳng đứng và cách kéo thước dây sát mặt đất.<br>- ***(Tích hợp NLS 3.1.TC2a: GV chiếu bảng tính Excel trên Tivi mô tả công thức tự động tính chiều cao khi nhập số đo bóng)***.<br>- **HS:** Quan sát và ghi nhận các lưu ý.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm trưởng phân công: 1 bạn giữ cọc tiêu, 2 bạn kéo thước dây, 1 bạn ghi số liệu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Các nhóm kiểm tra lại thước dây và cọc ngắm trước khi ra sân đo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở an toàn và thời gian đo thực địa là 15 phút. | **Quy trình 4 bước đo đạc:**<br>1. Cắm cọc tiêu $1.5\\text{ m}$ thẳng đứng bằng dây dọi.<br>2. Đo chiều dài bóng cọc trên mặt đất ($b_1$).<br>3. Đo chiều dài bóng cột cờ trên mặt đất ($b_2$).<br>4. Tính $H = 1.5 \\cdot \\frac{b_2}{b_1}$. |

## C. HOẠT ĐỘNG 3: THỰC HÀNH ĐO THỰC ĐỊA & XỬ LÝ SỐ LIỆU (18 phút)
a) Mục tiêu: Đo đạc trực tiếp ngoài sân trước Thư viện, thu thập số liệu và tính toán chiều cao cột cờ.
b) Nội dung: Các nhóm tiến hành đo bóng cọc và bóng cột cờ; quay lại phòng đọc Thư viện tính toán kết quả.
c) Sản phẩm: Số liệu đo đạc thực tế và kết quả tính chiều cao cột cờ của mỗi nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho các nhóm ra sân trước Thư viện thực hiện đo đạc.<br>- **HS:** Nhanh chóng di chuyển đến vị trí cột cờ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cắm cọc tiêu $h_1 = 1.5\\text{ m}$. Đo bóng cọc: $b_1 = 1.2\\text{ m}$. Đo bóng cột cờ: $b_2 = 8.4\\text{ m}$.<br>- **GV:** Giám sát, hướng dẫn các nhóm đặt thước thẳng mép bóng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Các nhóm trở lại phòng đọc Thư viện, nhập số liệu vào bảng tính trên Tivi Thư viện.<br>- Tính toán: $H = 1.5 \\cdot \\frac{8.4}{1.2} = 10.5\\text{ m}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** So sánh kết quả giữa các nhóm: dao động từ $10.4\\text{ m}$ đến $10.6\\text{ m}$. Sai số dưới $2\\%$, kết quả rất đáng tin cậy. | **Xử lý số liệu thực tế:**<br>- Chiều cao cọc: $h_1 = 1.5\\text{ m}$.<br>- Bóng cọc: $b_1 = 1.2\\text{ m}$.<br>- Bóng cột cờ: $b_2 = 8.4\\text{ m}$.<br>- Chiều cao cột cờ trường THCS Trần Phú:<br>$H = 1.5 \\cdot \\frac{8.4}{1.2} = 10.5\\text{ (m)}$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (7 phút)
a) Mục tiêu: Hoàn thiện bản tường trình thực nghiệm STEM và bàn giao hồ sơ lưu chiểu Thư viện.
b) Nội dung: Các nhóm hoàn tất Bản tường trình thực nghiệm; nộp lại cho thủ thư.
c) Sản phẩm: 08 Bản tường trình thực nghiệm STEM hoàn chỉnh của lớp 8/4.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các nhóm hoàn thiện mục Kết luận và Nguyên nhân sai số vào Bản tường trình.<br>- **HS:** Thảo luận và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thành viên trong nhóm ký tên xác nhận số liệu.<br>- ***(Tích hợp AI 4.B2.1: HS ghi chú nguyên nhân sai số nhỏ do mặt sân hơi dốc 1-2 độ và gió nhẹ làm lay ngọn cờ)***.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhóm trưởng đại diện nộp bản tường trình tại bàn Thư viện.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Tuyên dương tinh thần làm việc khoa học của học sinh.<br>- **GV:** Bàn giao toàn bộ hồ sơ cho Cán bộ Thư viện lưu minh chứng theo Kế hoạch 115. | **Bàn giao hồ sơ lưu Thư viện:**<br>- 100% nhóm hoàn thành bản tường trình thực nghiệm STEM đo bóng nắng.<br>- Bàn giao đủ hồ sơ cho Thư viện lưu trữ. |

# IV. PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN

## 1. Bản tường trình thực nghiệm STEM: Đo chiều cao bằng định lí Thalès
**TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN TIN — THƯ VIỆN SỐ**  
*Lớp: 8/4 — Nhóm số: ...... — Thời điểm đo: 08h30 ngày ...../11/2026*  

| Lần đo | Chiều cao cọc ($h_1$) | Bóng cọc ($b_1$) | Bóng vật thể ($b_2$) | Chiều cao tính được ($H$) |
| :---: | :---: | :---: | :---: | :---: |
| **Lần 1** | $1.5\\text{ m}$ | .............. | .............. | .............. |
| **Lần 2** | $1.5\\text{ m}$ | .............. | .............. | .............. |
| **Trung bình** | $1.5\\text{ m}$ | .............. | .............. | **$H_{TB} = \\dots\\dots\\dots\\text{ m}$** |

- **Kết luận chiều cao vật thể:** ................................................................................  
- **Nhận xét nguyên nhân sai số:** .............................................................................  

## 2. Sản phẩm học tập minh chứng hoàn chỉnh (Lưu hồ sơ Thư viện theo KH 115)
- **Kết quả đo mẫu (Nhóm 1 - Lớp 8/4):**  
  + Lần 1: $b_1 = 1.20\\text{ m}, b_2 = 8.40\\text{ m} \\Rightarrow H_1 = 10.50\\text{ m}$.  
  + Lần 2: $b_1 = 1.22\\text{ m}, b_2 = 8.52\\text{ m} \\Rightarrow H_2 = 10.48\\text{ m}$.  
  + Giá trị trung bình: $H_{TB} = 10.49\\text{ m} \\approx 10.5\\text{ m}$.  
- **Tình trạng bàn giao:** Đã nộp 08 Bản tường trình thực nghiệm của 08 nhóm học sinh lớp 8/4 về Thư viện trường lưu trữ.
"""

with open(os.path.join(out_dir, "KHBD_04_Le_Thi_Binh_Toan_8.md"), "w", encoding="utf-8") as f:
    f.write(md_04.strip())

with open(os.path.join(out_dir, "KHBD_05_Hoang_Xuan_Anh_Toan_7.md"), "w", encoding="utf-8") as f:
    f.write(md_05.strip())

with open(os.path.join(out_dir, "KHBD_06_Tran_Long_Hai_Toan_8.md"), "w", encoding="utf-8") as f:
    f.write(md_06.strip())

print("Đã tạo xong KHBD 04, 05 và 06.")
