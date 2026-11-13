# -*- coding: utf-8 -*-
import os

out_dir = r"C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\1_SOAN_KHBD\Ket_qua\05.11"

# 7. Thầy Trần Sáng (Toán 9)
md_07 = """Tiết 15 - BÀI 15: ĐỘ DÀI CUNG TRÒN, DIỆN TÍCH HÌNH QUẠT TRÒN VÀ VÀNH KHUYÊN
*Thời lượng thực hiện: 01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12 (STEM Mô hình quạt nghệ thuật)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu và ghi nhớ chính xác công thức tính độ dài cung tròn $l = \\frac{\\pi R n}{180}$ và diện tích hình quạt tròn $S = \\frac{\\pi R^2 n}{360} = \\frac{l R}{2}$ (với bán kính $R$ và góc ở tâm $n^\\circ$).
- Hiểu công thức tính diện tích hình vành khuyên $S = \\pi (R_2^2 - R_1^2)$.
- Vận dụng giải các bài toán thực tế về tính diện tích vật liệu, thiết kế quạt giấy nghệ thuật trang trí Thư viện.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Nghiên cứu công thức trên DlibK12, chủ động đo đạc góc và bán kính.
- Giao tiếp và hợp tác: Làm việc nhóm thiết kế mô hình quạt nghệ thuật.

b) Năng lực Toán học:
- Tư duy và lập luận toán học: Suy luận công thức tính độ dài cung và diện tích quạt từ chu vi và diện tích hình tròn toàn phần.
- Mô hình hóa toán học: Áp dụng công thức quạt tròn vào bài toán chế tạo đồ thủ công thực tế.

c) Năng lực số (NLS):
- ***(Tích hợp NLS 1.1.TC2a: Khai thác hoạt hình mô phỏng chuyển động quét góc ở tâm tạo nên quạt tròn trên CSDL DlibK12 qua màn hình Tivi Thư viện)***.
- ***(Tích hợp NLS 3.1.TC2b: Xây dựng bản vẽ kỹ thuật quạt giấy có ghi chú kích thước số)***.

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***(Tích hợp AI 5.B2.1: Quan sát gợi ý tối ưu hóa diện tích cắt giấy hình quạt từ phần mềm đồ họa số)***.

## 3. Về phẩm chất
- Chăm chỉ: Khéo léo, cẩn thận trong đo góc và tính diện tích.
- Trách nhiệm: Giữ gìn vệ sinh Thư viện, hoàn thành sản phẩm đúng thời hạn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Màn hình Tivi Thư viện kết nối Laptop GV; Hoạt hình mô phỏng quạt tròn trên DlibK12.
- Compa kỹ thuật lớn vẽ bảng; Giấy màu, que nan, keo dán; SGK Toán 9 Tập 1.
2. Học sinh:
- SGK Toán 9 Tập 1, thước đo độ, compa học sinh, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Xuất phát từ hình ảnh chiếc quạt giấy truyền thống để dẫn dắt đến khái niệm hình quạt tròn.
b) Nội dung: Quan sát chiếc quạt giấy xòe ra trên màn hình Tivi Thư viện; nhận diện tâm, bán kính và góc xòe.
c) Sản phẩm: Học sinh chỉ ra được bán kính và góc ở tâm của chiếc quạt.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh chiếc quạt giấy truyền thống xòe rộng trên Tivi Thư viện. Đặt câu hỏi: "Mặt quạt có dạng hình gì? Làm thế nào để tính diện tích giấy cần dùng để làm chiếc quạt này?".<br>- **HS:** Quan sát và liên tưởng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét mặt quạt giới hạn bởi hai bán kính và một cung tròn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Trả lời: Đó là hình quạt tròn, diện tích phụ thuộc vào bán kính quạt và độ mở của góc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định chính xác và dẫn dắt vào bài học. | **Khởi động:**<br>- Nhận biết hình quạt tròn là một phần hình tròn giới hạn bởi một cung tròn và hai bán kính đi qua hai đầu mút của cung đó.<br>- Đặt vấn đề thiết lập công thức tính diện tích hình quạt. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI / KHÁM PHÁ TRÊN DLIBK12 (15 phút)
a) Mục tiêu: Thiết lập công thức tính độ dài cung tròn và diện tích hình quạt tròn.
b) Nội dung: Xem mô phỏng trên DlibK12; lập tỉ lệ suy ra công thức từ hình tròn $360^\\circ$.
c) Sản phẩm: Công thức tính $l$ và $S$ được ghi nhớ vào vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Mở hoạt hình mô phỏng DlibK12 chiếu trên Tivi: Đường tròn bán kính $R$ có chu vi $C = 2\\pi R$ ứng với cung $360^\\circ$. Hỏi cung $1^\\circ$ dài bao nhiêu? Cung $n^\\circ$ dài bao nhiêu?<br>- ***(Tích hợp NLS 1.1.TC2a: HS theo dõi chuyển động quét góc n độ sinh động trên Tivi Thư viện)***.<br>- **HS:** Quan sát và suy luận tam tri thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cung $1^\\circ$ dài $\\frac{2\\pi R}{360} = \\frac{\\pi R}{180}$. Cung $n^\\circ$ dài $l = \\frac{\\pi R n}{180}$.<br>- **HS:** Tương tự với diện tích: Cung $360^\\circ$ có diện tích $\\pi R^2$. Quạt $n^\\circ$ có diện tích $S = \\frac{\\pi R^2 n}{360}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm lên bảng ghi công thức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa hai công thức trọng tâm. Lưu ý liên hệ $S = \\frac{l \\cdot R}{2}$. | **1. Độ dài cung tròn:**<br>$$l = \\frac{\\pi R n}{180}$$<br><br>**2. Diện tích hình quạt tròn:**<br>$$S = \\frac{\\pi R^2 n}{360} \\quad \\text{hay} \\quad S = \\frac{l R}{2}$$<br>($R$: bán kính; $n$: số đo độ của cung tròn). |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP / THỰC HÀNH STEM (18 phút)
a) Mục tiêu: Tính toán số liệu và thiết kế hoàn thiện chiếc quạt giấy mini có góc mở $120^\\circ$.
b) Nội dung: Làm bài tập tính toán trên Phiếu học tập số 1; thực hành cắt dán quạt giấy STEM.
c) Sản phẩm: Bản tính diện tích và chiếc quạt giấy mini hoàn thiện của mỗi nhóm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát Phiếu học tập số 1. Yêu cầu thiết kế chiếc quạt giấy có bán kính nan quạt $R = 18\\text{ cm}$, góc mở quạt $n = 120^\\circ$. Tính diện tích giấy làm mặt quạt.<br>- **HS:** Nhận vật liệu và thực hiện.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính: $S = \\frac{\\pi \\cdot 18^2 \\cdot 120}{360} = \\frac{\\pi \\cdot 324 \\cdot 1}{3} = 108\\pi \\approx 339.3\\text{ cm}^2$.<br>- **HS:** Dùng compa và thước đo góc vẽ hình quạt trên giấy màu và cắt dán.<br>- **GV:** Quan sát, hỗ trợ kỹ thuật nan quạt.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Các nhóm xòe quạt trưng bày trên bàn đọc Thư viện.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chấm điểm độ chính xác góc mở $120^\\circ$ và tính thẩm mỹ của sản phẩm. | **Luyện tập & Thực hành STEM:**<br>- Bán kính quạt: $R = 18\\text{ cm}$.<br>- Góc ở tâm: $n = 120^\\circ$.<br>- Diện tích mặt quạt:<br>$S = \\frac{\\pi \\cdot 18^2 \\cdot 120}{360} = 108\\pi \\approx 339.3\\text{ (cm}^2\\text{)}$.<br>- Hoàn thiện mô hình quạt nghệ thuật. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (7 phút)
a) Mục tiêu: Trưng bày quạt tại Góc truyền thống Thư viện và bàn giao minh chứng hồ sơ.
b) Nội dung: Các nhóm gắn bảng tên sản phẩm và nộp lại bàn Thư viện.
c) Sản phẩm: 08 mô hình quạt nghệ thuật có dán phiếu tính diện tích.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn các nhóm xếp quạt vào Tủ trưng bày sản phẩm Thư viện.<br>- **HS:** Đặt sản phẩm ngay ngắn kèm phiếu học tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm trưởng kiểm tra phiếu tính diện tích đính kèm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Cả lớp bình chọn chiếc quạt tinh xảo nhất.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Đánh giá cao sự sáng tạo của học sinh; bàn giao sản phẩm cho thủ thư lưu hồ sơ Kế hoạch 115. | **Bàn giao hồ sơ lưu Thư viện:**<br>- Đã lưu giữ 08 mô hình quạt nghệ thuật tại Thư viện trường.<br>- Minh chứng thực tế cho tiết học Thư viện số. |

# IV. PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN

## 1. Phiếu học tập số 1: Tính diện tích quạt tròn STEM
**TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN TIN — THƯ VIỆN SỐ**  
*Lớp: 9/5 — Nhóm số: ......*  

- **Nhiệm vụ 1: Tính toán lý thuyết**  
  Cho hình quạt tròn bán kính $R = 18\\text{ cm}$, góc ở tâm $n = 120^\\circ$.  
  + Độ dài cung tròn $l = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  + Diện tích hình quạt tròn $S = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  + Kết luận: $S \\approx \\dots\\dots\\dots\\dots\\dots\\text{ cm}^2$.  

- **Nhiệm vụ 2: Chế tạo sản phẩm quạt mini**  
  + Góc mở quạt: $120^\\circ$ — Số nan quạt: 05 nan tre.  
  + Màu sắc chủ đạo: ............................................................................................  

## 2. Sản phẩm học tập minh chứng hoàn chỉnh (Lưu hồ sơ Thư viện theo KH 115)
- **Đáp án tính toán:** $l = 12\\pi \\approx 37.7\\text{ cm}$; $S = 108\\pi \\approx 339.3\\text{ cm}^2$.  
- **Sản phẩm thực tế:** 08 chiếc quạt giấy nghệ thuật nan tre được lưu giữ tại Tủ trưng bày Thư viện THCS Trần Phú.
"""

# 8. Thầy Hồ Đăng Danh (Toán 6)
md_08 = """Tiết 49 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: SỬ DỤNG MÁY TÍNH CẦM TAY GIẢI TOÁN THỰC TẾ
*Thời lượng thực hiện: 01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng thành thạo máy tính cầm tay thực hiện các phép toán cộng, trừ, nhân, chia số tự nhiên, tính lũy thừa và sử dụng các phím dấu ngoặc `(`, `)`.
- Vận dụng máy tính cầm tay để giải nhanh các bài toán thực tế về tính tiền đi siêu thị, tính tiền điện nước và bài toán lịch sử.
- Biết kiểm tra tính hợp lý của kết quả trên màn hình máy tính.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác trên máy tính cá nhân, chủ động đối chiếu kết quả với phần mềm giả lập trên Tivi Thư viện.
- Giao tiếp và hợp tác: Hỗ trợ bạn cùng bàn khi bạn gặp lỗi cú pháp máy tính.

b) Năng lực Toán học:
- Năng lực công cụ toán học: Khai thác hiệu quả máy tính cầm tay như một công cụ hỗ trợ tư duy và giảm tải thời gian tính toán thô.
- Giải quyết vấn đề toán học: Lập quy trình bấm phím đúng thứ tự ưu tiên phép toán.

c) Năng lực số (NLS):
- ***(Tích hợp NLS 1.1.TC1a: Sử dụng phần mềm giả lập máy tính khoa học trên CSDL DlibK12 qua màn hình Tivi Thư viện)***.
- ***(Tích hợp NLS 3.2.TC1b: Tự động hóa quy trình tính toán số học phức tạp bằng thiết bị số)***.

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***(Tích hợp AI 2.B1.1: Nhận diện cơ chế thông báo lỗi cú pháp [Syntax ERROR] của máy tính điện tử khi nhập sai biểu thức)***.

## 3. Về phẩm chất
- Cẩn thận: Chú ý từng phím bấm, không bấm nhầm dấu ngoặc và số mũ.
- Trách nhiệm: Giữ gìn máy tính cầm tay, bảo quản thiết bị phòng Thư viện.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Màn hình Tivi Thư viện kết nối Laptop GV cài phần mềm giả lập Casio Fx-580VN X.
- Ngân hàng bài toán thực tế trên DlibK12; SGK Toán 6 Tập 1; Phiếu học tập số 1.
2. Học sinh:
- Máy tính cầm tay cá nhân; SGK Toán 6 Tập 1; Vở ghi bài.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Tạo không khí sôi nổi qua trò chơi tính nhanh giữa bấm máy và tính nhẩm.
b) Nội dung: So tài tính biểu thức phức tạp $125 \\cdot 48 - 25 \\cdot 48$ và $2^{10} + 3^5$.
c) Sản phẩm: Tốc độ và độ chính xác của học sinh khi bấm máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu phép tính $A = 2^{10} + 3^5$ lên Tivi Thư viện. Yêu cầu học sinh dùng máy tính cầm tay tìm kết quả trong 10 giây.<br>- **HS:** Bật máy tính và thao tác.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác bấm phím mũ `^` hoặc phím `x^■`.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đồng thanh hô kết quả: $1024 + 243 = 1267$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và giới thiệu phần mềm giả lập máy tính trên màn hình Tivi lớn để bắt đầu bài học. | **Khởi động:**<br>- Máy tính cầm tay giúp tính toán nhanh các lũy thừa lớn.<br>- Phím chức năng lũy thừa: `x^■` hoặc `x²`.<br>$2^{10} + 3^5 = 1024 + 243 = 1267$. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KỸ NĂNG BẤM PHÍM / KHÁM PHÁ TRÊN DLIBK12 (15 phút)
a) Mục tiêu: Nắm vững thứ tự bấm phím biểu thức chứa nhiều dấu ngoặc và phân số.
b) Nội dung: Quan sát giáo viên thao tác trên phần mềm giả lập chiếu Tivi Thư viện; thực hành bấm biểu thức nhiều tầng.
c) Sản phẩm: Thao tác bấm đúng và kết quả chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Bật phần mềm giả lập Casio trên Tivi Thư viện, phóng to bàn phím số. Chiếu biểu thức: $B = 35 \\cdot [130 - (12 - 4)^2]$. Hướng dẫn cách bấm dấu ngoặc tròn `(` `)` lồng nhau.<br>- ***(Tích hợp NLS 1.1.TC1a: HS quan sát con trỏ màn hình giả lập trên Tivi để theo dõi thứ tự nhập biểu thức)***.<br>- **HS:** Cầm máy tính bấm theo hướng dẫn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhập biểu thức: `35 × (130 - (12 - 4) x² ) =`.<br>- ***(Tích hợp AI 2.B1.1: Nếu quên đóng ngoặc, máy báo lỗi cú pháp. GV hướng dẫn HS bấm phím mũi tên [REPLAY] để sửa đúng vị trí lỗi)***.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Màn hình máy tính hiện kết quả: $2310$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Máy tính hiện đại tự hiểu thứ tự ưu tiên phép toán trong ngoặc trước, nhân chia trước, cộng trừ sau. | **Quy trình bấm biểu thức phức tạp:**<br>- Bấm các dấu ngoặc `(` `)` theo đúng đề bài.<br>- Dùng phím `REPLAY` (mũi tên) để di chuyển con trỏ sửa lỗi khi bị báo `Syntax ERROR`.<br>$B = 35 \\cdot [130 - 8^2] = 35 \\cdot [130 - 64] = 35 \\cdot 66 = 2310$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP / GIẢI TOÁN THỰC TẾ TRÊN DLIBK12 (18 phút)
a) Mục tiêu: Vận dụng giải các bài toán thực tế về hóa đơn tiền hàng và bài toán dân số.
b) Nội dung: Hoàn thành Phiếu học tập số 1; kiểm tra kết quả qua ngân hàng dữ liệu DlibK12.
c) Sản phẩm: Bảng tính tiền hóa đơn mua sắm dụng cụ Thư viện được tính toán chính xác.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát Phiếu học tập số 1. Bài toán: "Thư viện trường mua 45 quyển vở giá 8 500 đ/quyển, 12 hộp bút bi giá 42 000 đ/hộp, 5 ram giấy A4 giá 65 000 đ/ram. Tính tổng số tiền và số tiền được giảm giá $10\\%$".<br>- **HS:** Đọc đề bài và thiết lập biểu thức tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lập biểu thức tổng: $T = 45 \\cdot 8500 + 12 \\cdot 42000 + 5 \\cdot 65000$. Bấm máy tính tìm $T$. Sau đó tính số tiền thanh toán: $T \\cdot 0.9$.<br>- **GV:** Quan sát, hướng dẫn các nhóm bấm phím lưu nhớ `M+` hoặc dấu ngoặc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm đọc kết quả: Tổng tiền là $1 211 500\\text{ đ}$. Sau khi giảm $10\\%$ còn $1 090 350\\text{ đ}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định kết quả chuẩn xác; biểu dương tinh thần làm việc nhóm nhanh nhẹn. | **Bài toán thực tế hóa đơn:**<br>- Tổng tiền mua hàng:<br>$T = 45 \\cdot 8500 + 12 \\cdot 42000 + 5 \\cdot 65000$<br>$T = 382500 + 504000 + 325000 = 1211500\\text{ (đồng)}$.<br>- Số tiền sau khi giảm $10\\%$:<br>$1211500 \\cdot 90\\% = 1090350\\text{ (đồng)}$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (7 phút)
a) Mục tiêu: Đánh giá kỹ năng sử dụng máy tính qua bài test trắc nghiệm số và bàn giao phiếu học tập.
b) Nội dung: Học sinh hoàn thành phiếu học tập cá nhân; ký tên nộp về bàn Thư viện.
c) Sản phẩm: Toàn bộ Phiếu học tập của học sinh lớp 6/3 nộp lưu hồ sơ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các em kiểm tra lại toàn bộ đáp án trên Phiếu học tập số 1.<br>- **HS:** Rà soát lại số liệu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ký tên và nộp lại phiếu cho nhóm trưởng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhóm trưởng bàn giao phiếu cho thủ thư Thư viện.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Tổng kết tiết học, nhắc nhở học sinh luôn kiểm tra tính hợp lý của kết quả khi bấm máy tính.<br>- **GV:** Bàn giao hồ sơ lưu cho Thư viện theo Kế hoạch 115. | **Bàn giao hồ sơ lưu Thư viện:**<br>- 100% học sinh hoàn thành bài thực hành bấm máy tính cầm tay.<br>- Bàn giao đủ hồ sơ lưu chiểu tại Thư viện trường. |

# IV. PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN

## 1. Phiếu học tập số 1: Sử dụng máy tính cầm tay giải toán thực tế
**TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN TIN — THƯ VIỆN SỐ**  
*Lớp: 6/3 — Họ và tên HS: ....................................................*  

- **Bài 1: Thực hiện phép tính bằng máy tính cầm tay**  
  1) $125 \\cdot 34 - 125 \\cdot 14 = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  2) $3^4 + 2^5 \\cdot 5 = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  3) $[(150 - 2^3 \\cdot 5) : 11] + 2026 = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  

- **Bài 2: Hóa đơn mua sắm thiết bị Thư viện**  
  + Tổng tiền trước giảm giá: ............................................................................ đồng.  
  + Tiền thanh toán sau giảm $10\\%$: .............................................................. đồng.  

## 2. Sản phẩm học tập minh chứng hoàn chỉnh (Lưu hồ sơ Thư viện theo KH 115)
- **Đáp án Bài 1:** 1) $2500$; 2) $241$; 3) $10 + 2026 = 2036$.  
- **Đáp án Bài 2:** Tổng tiền: $1 211 500\\text{ đ}$; Thực trả: $1 090 350\\text{ đ}$.  
- **Tình trạng bàn giao:** Đã thu và bàn giao 38 Phiếu bài làm của học sinh lớp 6/3 cho Thư viện lưu trữ.
"""

# 9. Thầy Nguyễn Văn Tính (HĐTN 6)
md_09 = """Tiết 32 - CHỦ ĐỀ 3: XÂY DỰNG NỀN NẾP TỰ HỌC VÀ RÈN LUYỆN KỸ NĂNG ĐỌC SÁCH TẠI THƯ VIỆN
*Thời lượng thực hiện: 01 tiết (45 phút) - Tiết trải nghiệm tại Thư viện số DlibK12*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được ý nghĩa to lớn của việc tự học và vai trò của sách, tài liệu số trong việc phát triển tri thức và kỹ năng sống.
- Nắm được phương pháp đọc sách hiệu quả: đọc lướt, đọc sâu, ghi chú tóm tắt theo sơ đồ KWL (Biết - Muốn biết - Học được).
- Biết cách tìm kiếm và khai thác kho sách điện tử, tài liệu kỹ năng trên nền tảng Thư viện số DlibK12.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự lập kế hoạch đọc sách cá nhân, có thói quen đọc sách ít nhất 30 phút mỗi ngày.
- Giao tiếp và hợp tác: Tự tin chia sẻ cảm nhận về cuốn sách yêu thích trước tập thể.

b) Năng lực đặc thù Hoạt động trải nghiệm:
- Năng lực thích ứng với cuộc sống: Hình thành nề nếp sinh hoạt, học tập khoa học và cân bằng thời gian.
- Năng lực thiết kế và tổ chức hoạt động: Tham gia xây dựng Tủ sách mini và Góc văn hóa đọc Thư viện.

c) Năng lực số (NLS):
- ***(Tích hợp NLS 1.1.TC1a: Khai thác kho sách điện tử E-book kỹ năng sống trên nền tảng Thư viện số DlibK12)***.
- ***(Tích hợp NLS 4.1.TC1b: Xây dựng thói quen sử dụng thiết bị số an toàn, lành mạnh, không lạm dụng trò chơi điện tử)***.

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***(Tích hợp AI 1.B1.1: Tiếp cận trợ lý gợi ý đầu sách phù hợp theo lứa tuổi và sở thích cá nhân)***.

## 3. Về phẩm chất
- Chăm chỉ: Yêu thích việc đọc sách, say mê tìm tòi kiến thức mới.
- Trách nhiệm: Giữ gìn sách cẩn thận, không làm rách, gấp mép sách; tôn trọng không gian yên tĩnh của Thư viện.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Màn hình Tivi Thư viện kết nối Laptop GV; Kho sách điện tử Kỹ năng sống trên DlibK12.
- Video phóng sự truyền cảm hứng đọc sách; Mẫu Sổ tay đọc sách KWL; SGK HĐTN 6.
2. Học sinh:
- Sổ tay đọc sách cá nhân; Bút viết, bút màu trang trí; SGK Hoạt động trải nghiệm 6.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Khơi gợi tình yêu sách và chia sẻ thực trạng thời gian đọc sách của học sinh.
b) Nội dung: Xem clip 2 phút về câu chuyện đọc sách của các danh nhân; khảo sát nhanh thói quen đọc sách của lớp.
c) Sản phẩm: Sự hào hứng và nhận thức của học sinh về giá trị của sách.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Bật Tivi Thư viện chiếu clip ngắn: "Một cuốn sách có thể thay đổi cuộc đời bạn như thế nào?". Hỏi: "Tuần qua em đã đọc được trang sách nào chưa?".<br>- **HS:** Quan sát và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Một số em giơ tay chia sẻ về truyện tranh, sách lịch sử vừa đọc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Chia sẻ cảm xúc khi đọc được một câu chuyện ý nghĩa.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dẫn dắt: "Hôm nay chúng ta cùng đến với Thư viện số DlibK12 để khám phá kho tàng tri thức vô tận và rèn luyện kỹ năng tự học!". | **Khởi động:**<br>- Sách là người bạn lớn của tri thức.<br>- Đọc sách giúp mở rộng vốn từ, phát triển tư duy và bồi đắp tâm hồn. |

## B. HOẠT ĐỘNG 2: KHÁM PHÁ THƯ VIỆN SỐ VÀ PHƯƠNG PHÁP ĐỌC KWL (15 phút)
a) Mục tiêu: Học sinh biết cách khai thác kho sách số DlibK12 và ghi chép tóm tắt theo mô hình KWL.
b) Nội dung: GV hướng dẫn trên Tivi Thư viện; HS thực hành đăng nhập và chọn một bài đọc kỹ năng.
c) Sản phẩm: Bảng KWL bước đầu được ghi vào Sổ tay đọc sách của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn trên Tivi Thư viện mục "Sách kỹ năng sống THCS" trên DlibK12. Giới thiệu phương pháp đọc KWL: K (Điều đã biết), W (Điều muốn biết), L (Điều học được).<br>- ***(Tích hợp NLS 1.1.TC1a: GV thị phạm thao tác lật trang sách điện tử và đánh dấu đoạn trích hay trên màn hình DlibK12)***.<br>- **HS:** Mở Sổ tay đọc sách cá nhân kẻ bảng 3 cột K-W-L.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc lướt một mẩu chuyện ngắn trong kho sách điện tử DlibK12 hoặc sách in Thư viện.<br>- **GV:** Đi quan sát, hướng dẫn các em cách gạch chân từ khóa chính.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Một số em đứng lên chia sẻ cột K và W trước khi đọc sâu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và hướng dẫn các em tập trung đọc để hoàn thành cột L (Điều học được). | **Phương pháp đọc sách KWL:**<br>- **K (Know):** Những điều em đã biết về chủ đề.<br>- **W (Want):** Những điều em muốn tìm hiểu thêm.<br>- **L (Learned):** Những bài học quý giá em rút ra được sau khi đọc. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP / THỰC HÀNH GHI CHÉP VÀ THẢO LUẬN (18 phút)
a) Mục tiêu: Hoàn thiện Sổ tay đọc sách KWL và thảo luận nhóm về thông điệp cuốn sách.
b) Nội dung: Các nhóm đọc sách, ghi chép thu hoạch và chia sẻ bài học tâm đắc.
c) Sản phẩm: Trang sổ tay đọc sách hoàn chỉnh của mỗi học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu học sinh dành 10 phút đọc sâu và hoàn thành cột L trong Sổ tay đọc sách. Sau đó chia sẻ trong nhóm 4 em.<br>- **HS:** Tập trung đọc sách trong không gian yên tĩnh của Thư viện.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc và ghi chép bài học: lòng biết ơn cha mẹ, đức tính kiên trì, tình bạn đẹp...<br>- **GV:** Quan sát, giữ nề nếp trật tự phòng đọc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện 2 học sinh lên cầm micro chia sẻ câu chuyện và bài học của mình trước Tivi Thư viện.<br>- ***(Tích hợp NLS 4.1.TC1b: HS nêu bài học về việc hạn chế lướt mạng xã hội vô bổ để dành thời gian đọc sách)***.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao cảm xúc chân thành và sự tiến bộ trong kỹ năng trình bày của các em. | **Thu hoạch kỹ năng sống:**<br>- Rèn luyện tính kiên nhẫn và khả năng tập trung sâu.<br>- Rút ra bài học ý nghĩa từ trang sách áp dụng vào cuộc sống hằng ngày. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (7 phút)
a) Mục tiêu: Ký cam kết văn hóa đọc và bàn giao minh chứng hồ sơ cho Thư viện.
b) Nội dung: Học sinh điền Bản cam kết đọc sách cá nhân; bàn giao phiếu thu hoạch lưu hồ sơ.
c) Sản phẩm: Tập Sổ tay thu hoạch KWL của học sinh lớp 6/2 nộp lại Thư viện.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát Bản cam kết đọc sách: "Mỗi ngày đọc ít nhất 20 phút — Mỗi tháng đọc xong 1 cuốn sách".<br>- **HS:** Tiếp nhận và ký cam kết.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ký tên vào Bản cam kết và kẹp vào trang đầu Sổ tay đọc sách.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhóm trưởng thu gom sổ tay bàn giao về bàn thủ thư Thư viện.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Cảm ơn các em đã có một tiết trải nghiệm văn hóa đọc bổ ích.<br>- **GV:** Bàn giao toàn bộ tập Sổ tay đọc sách cho Cán bộ Thư viện lưu hồ sơ theo Kế hoạch 115. | **Bàn giao hồ sơ lưu Thư viện:**<br>- Bàn giao đủ tập Sổ tay đọc sách và Bản cam kết văn hóa đọc của lớp 6/2.<br>- Hoàn tất hồ sơ chuyên môn tiết Thư viện. |

# IV. PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN

## 1. Mẫu Sổ tay đọc sách cá nhân theo mô hình KWL
**TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN TIN — TIẾT TRẢI NGHIỆM THƯ VIỆN**  
*Lớp: 6/2 — Họ và tên HS: ....................................................*  

- Tên cuốn sách / bài viết đã đọc: ................................................................................  
- Tác giả: ........................................................ CSDL Thư viện số DlibK12  

| K (Điều em đã biết) | W (Điều em muốn biết) | L (Bài học quý giá em học được) |
| :--- | :--- | :--- |
| .........................................<br>......................................... | .........................................<br>......................................... | .........................................<br>......................................... |

- **Bản cam kết văn hóa đọc:** Em cam kết dành ít nhất 20 phút mỗi ngày để đọc sách và tra cứu học liệu số trên DlibK12.  
  *Ký tên: ........................................................*  

## 2. Sản phẩm học tập minh chứng hoàn chỉnh (Lưu hồ sơ Thư viện theo KH 115)
- **Bài thu hoạch tiêu biểu (Học sinh: Nguyễn Mai Anh - Lớp 6/2):**  
  + Sách đã đọc: *"Hạt giống tâm hồn — Cho những trái tim dũng cảm"* (DlibK12).  
  + Cột K: Đã biết cần phải dũng cảm đối mặt với khó khăn.  
  + Cột W: Muốn biết làm sao để vượt qua sự rụt rè trước đám đông.  
  + Cột L: Học được bài học: "Thất bại lớn nhất là không dám thử thách; mỗi lần đứng lên sau vấp ngã giúp ta trưởng thành hơn".  
- **Tình trạng bàn giao:** Đã nộp 36 bản Sổ tay thu hoạch KWL của học sinh lớp 6/2 về Thư viện trường lưu trữ.
"""

with open(os.path.join(out_dir, "KHBD_07_Tran_Sang_Toan_9.md"), "w", encoding="utf-8") as f:
    f.write(md_07.strip())

with open(os.path.join(out_dir, "KHBD_08_Ho_Dang_Danh_Toan_6.md"), "w", encoding="utf-8") as f:
    f.write(md_08.strip())

with open(os.path.join(out_dir, "KHBD_09_Nguyen_Van_Tinh_HDTN_6.md"), "w", encoding="utf-8") as f:
    f.write(md_09.strip())

print("Đã tạo xong KHBD 07, 08 và 09 Markdown.")
