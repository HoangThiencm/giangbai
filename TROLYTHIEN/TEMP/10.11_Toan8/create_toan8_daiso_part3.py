# -*- coding: utf-8 -*-
"""
Script sinh tiếp các tệp KHBD Đại số & Thống kê 8 (Bài 07 đến Bài 12):
- 07_KHBD_Toan8_Bai20_PhanTichSoLieuThongKe_Tiet33.md
- 08_KHBD_Toan8_LuyenTapChung_ThongKe_Tiet34.md (Mindmap: mindmap_toan8_tiet34.png)
- 09_KHBD_Toan8_BaiTapCuoiChuong5_Tiet35.md (Mindmap: mindmap_toan8_tiet35.png)
- 10_KHBD_Toan8_HDTN_PhanTichDacDiemKhiHauVN_Tiet36.md
- 11_KHBD_Toan8_OnTapCuoiHK1_DaiSo_Tiet37-39.md (Mindmap: mindmap_toan8_tiet37_39.png)
- 12_KHBD_Toan8_KiemTraTraBaiCuoiHK1_DaiSo_Tiet40-41.md
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/10.11_Toan8"
os.makedirs(OUT_DIR, exist_ok=True)

# 07. Bài 20: Phân tích số liệu thống kê dựa vào biểu đồ (Tiết 33)
md_07 = """Tiết 33 - BÀI 20: PHÂN TÍCH SỐ LIỆU THỐNG KÊ DỰA VÀO BIỂU ĐỒ
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đọc, hiểu và trích xuất thông tin định lượng, định tính từ các dạng biểu đồ thống kê đã học (biểu đồ tranh, biểu đồ cột đơn, cột kép, biểu đồ đoạn thẳng và biểu đồ hình quạt tròn).
- Nhận biết và phát hiện những điểm bất thường hoặc sai lệch, dữ liệu không hợp lí trong biểu đồ thống kê thực tế.
- Rút ra nhận xét, xu thế biến động của số liệu và đưa ra các dự đoán, kết luận hợp lí phục vụ đời sống.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Chủ động khai thác thông tin từ biểu đồ thực tế, phân tích xu hướng tăng trưởng.
- Giao tiếp và hợp tác: Trình bày rõ ràng các lập luận thống kê trước nhóm và phản biện các nhận định sai lệch.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh tỉ lệ, đối chiếu số liệu tuyệt đối và số liệu tương đối.
- Năng lực mô hình hóa toán học: Chuyển đổi dữ liệu từ biểu đồ sang bảng số liệu và ngược lại để phân tích quy luật.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2b: Biết khai thác và phân tích số liệu thống kê từ biểu đồ số, sử dụng máy tính và bảng tính điện tử để trích xuất dữ liệu trực quan.***

## 3. Về phẩm chất
- Chăm chỉ: Tỉ mỉ quan sát các trục số, đơn vị đo, chú giải biểu đồ để không rút ra kết luận ngộ nhận.
- Trách nhiệm: Tôn trọng tính khách quan, trung thực của các số liệu điều tra thống kê.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng điện tử PowerPoint trình chiếu các biểu đồ thống kê thực tế (kinh tế, khí hậu, giáo dục).
2. Học sinh: SGK Toán 8 tập 1, vở ghi, thước kẻ, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Kích thích nhu cầu tìm hiểu cách phân tích số liệu thống kê từ biểu đồ.
b) Nội dung: Quan sát biểu đồ tranh và biểu đồ đoạn thẳng về kim ngạch xuất khẩu gạo của Việt Nam qua một số năm.
c) Sản phẩm: Câu trả lời nhận xét về xu thế xuất khẩu gạo tăng hay giảm.
d) Tổ chức thực hiện:
- **Bước 1 (Chuyển giao nhiệm vụ):** GV chiếu biểu đồ đoạn thẳng thể hiện sản lượng lúa gạo xuất khẩu và đặt câu hỏi: Biểu đồ cho biết xu thế xuất khẩu thay đổi như thế nào qua các năm? Năm nào đạt giá trị cao nhất?
- **Bước 2 (Thực hiện nhiệm vụ):** HS quan sát biểu đồ và suy nghĩ cá nhân.
- **Bước 3 (Báo cáo, thảo luận):** 1 HS chỉ ra điểm đỉnh của đường gấp khúc và giai đoạn tăng trưởng mạnh nhất.
- **Bước 4 (Kết luận, nhận định):** GV dẫn dắt vào bài học: Phân tích số liệu thống kê từ biểu đồ giúp ta đưa ra quyết định sản xuất và tiêu dùng chính xác.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (22 phút)
### Hoạt động 2.1: Đọc và phân tích biểu đồ thống kê (12 phút)
a) Mục tiêu: Đọc chính xác các giá trị trên biểu đồ và nhận biết xu thế của dãy số liệu.
b) Nội dung: Đọc mục 1 SGK trang 99 - 101; làm Luyện tập 1.
c) Sản phẩm: Bảng số liệu thống kê trích xuất từ biểu đồ và các câu trả lời phân tích.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS quan sát Biểu đồ cột kép Hình 5.14 SGK biểu diễn số lượng học sinh giỏi các môn Toán, Văn của 4 lớp 8A, 8B, 8C, 8D.<br>- **GV:** Đặt câu hỏi: Lớp nào có nhiều HS giỏi Toán nhất? Tổng số HS giỏi hai môn của lớp nào cao nhất?<br>- **HS:** Đọc độ cao từng cột.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi hoàn thành bảng thống kê số liệu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện cặp đôi trình bày kết quả: Lớp 8A có 15 HS giỏi Toán, 12 HS giỏi Văn; Tổng cộng 27 lượt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc đọc biểu đồ cột kép: Chú ý màu sắc của từng cột tương ứng với chú giải. | **1. Nhận xét về xu thế của số liệu qua biểu đồ:**<br>- Biểu đồ đoạn thẳng: Chiều hướng đi lên thể hiện xu thế tăng, đi xuống thể hiện xu thế giảm.<br>- Biểu đồ cột: So sánh độ cao các cột để đánh giá mức độ lớn nhỏ giữa các đối tượng.<br>- Biểu đồ quạt tròn: So sánh độ lớn các hình quạt để thấy cơ cấu tỉ lệ phần trăm. |

### Hoạt động 2.2: Nhận biết những lỗi sai lệch trong biểu đồ (10 phút)
a) Mục tiêu: Phát hiện biểu đồ vẽ không đúng tỉ lệ hoặc gây hiểu lầm thị giác.
b) Nội dung: Khảo sát mục 2 SGK trang 101 - 102; xem xét các ví dụ về trục tung không bắt đầu từ số 0.
c) Sản phẩm: Lời chỉ ra điểm bất thường của biểu đồ gây hiểu nhầm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hai biểu đồ cột cùng thể hiện một dữ liệu doanh thu nhưng một biểu đồ có gốc trục tung từ 0, một biểu đồ gốc trục tung từ 90.<br>- **GV:** Hỏi HS: Biểu đồ thứ hai có làm người xem phóng đại sự chênh lệch doanh thu không?<br>- **HS:** Suy nghĩ và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét sự sai khác về cảm giác trực quan giữa hai biểu đồ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS phát biểu: Khi cắt cụt trục tung, chênh lệch dù rất nhỏ cũng biến thành cột cao gấp nhiều lần cột khác.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu: Khi đọc biểu đồ cần kiểm tra kỹ gốc tọa độ $0$ và các khoảng chia trên trục số. | **2. Nhận biết tính hợp lí của biểu đồ:**<br>- Trục số phải có vạch chia đều nhau và ghi rõ đơn vị.<br>- Cần lưu ý trường hợp trục tung không bắt đầu từ số $0$, vì có thể phóng đại mức độ chênh lệch trực quan.<br>- Tổng các tỉ lệ phần trăm trên biểu đồ hình quạt tròn phải đúng bằng $100\\%$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (12 phút)
a) Mục tiêu: Thực hành giải quyết các bài tập phân tích biểu đồ SGK.
b) Nội dung: Giải bài tập 5.10, 5.11 SGK trang 104.
c) Sản phẩm: Lời giải chính xác trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 5.10 SGK trang 104.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc dữ liệu từ biểu đồ hình quạt tròn về tỉ lệ các phương tiện giao thông đến trường của học sinh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày tỉ lệ đi xe đạp ($45\\%$), đi bộ ($30\\%$), xe buýt ($15\\%$), khác ($10\\%$).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt đáp số đúng. | **Bài 5.10 (SGK tr.104):**<br>- Tỉ lệ học sinh đi xe đạp là lớn nhất ($45\\%$).<br>- Nếu trường có $800$ học sinh thì số học sinh đi xe buýt là:<br>$800 \\cdot 15\\% = 800 \\cdot \\frac{15}{100} = 120$ (học sinh). |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (6 phút)
- **Tích hợp NLS 1.2.TC2b:** GV hướng dẫn học sinh tìm kiếm biểu đồ phân bố nhiệt độ và lượng mưa của tỉnh nhà trong 12 tháng từ trang web của Trung tâm Dự báo Khí tượng Thủy văn Quốc gia. Nhận xét tháng có nhiệt độ cao nhất và tháng có lượng mưa lớn nhất. Dặn dò chuẩn bị tiết Luyện tập chung.
"""

# 08. Luyện tập chung (Thống kê - Tiết 34)
md_08 = """Tiết 34 - LUYỆN TẬP CHUNG: THU THẬP, BIỂU DIỄN VÀ PHÂN TÍCH DỮ LIỆU THỐNG KÊ
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố toàn bộ các kỹ năng thống kê cơ bản: Thu thập và phân loại dữ liệu; Biểu diễn dữ liệu bằng các dạng bảng và biểu đồ thích hợp; Đọc, hiểu và phân tích dữ liệu trên biểu đồ.
- Phát hiện và giải thích các kết luận không hợp lí, các số liệu thiếu trung thực từ các biểu đồ sai quy chuẩn.
- Thực hiện kiểm tra đánh giá thường xuyên kiến thức Chương V.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa các dạng biểu đồ tương ứng với từng dạng dữ liệu (định tính, định lượng).
- Giao tiếp và hợp tác: Hợp tác nhóm nhỏ để thảo luận lựa chọn dạng biểu đồ trực quan tối ưu nhất.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: So sánh hiệu quả thể hiện của biểu đồ cột, biểu đồ đoạn thẳng và biểu đồ quạt tròn.
- Năng lực giải quyết vấn đề toán học: Tính toán số lượng thực tế từ tỉ lệ phần trăm và ngược lại.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 2.4.TC2a: Sử dụng công cụ số (bảng tính điện tử, ứng dụng trình chiếu) để chia sẻ và cộng tác biểu diễn số liệu thống kê.***

## 3. Về phẩm chất
- Trung thực: Báo cáo số liệu chính xác, không làm sai lệch thông tin thực tế.
- Trách nhiệm: Ý thức được vai trò của số liệu thống kê trong việc ra quyết định học tập và sinh hoạt.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy hệ thống hóa Chương V, phiếu học tập, đề kiểm tra thường xuyên ngắn (10 phút).
2. Học sinh: SGK Toán 8 tập 1, vở ghi, dụng cụ vẽ biểu đồ (thước thẳng, compa, thước đo góc).

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (4 phút)
a) Mục tiêu: Khởi động không khí học tập và tạo liên kết ôn tập Chương V.
b) Nội dung: Trả lời nhanh câu hỏi trắc nghiệm: "Dữ liệu nào sau đây là số liệu liên tục?".
c) Sản phẩm: Đáp án chọn câu hỏi của học sinh.
d) Tổ chức thực hiện:
- **Bước 1 (Chuyển giao nhiệm vụ):** GV chiếu 4 phương án: A. Số lượng học sinh; B. Điểm số bài kiểm tra; C. Chiều cao của học sinh; D. Tên các môn thể thao yêu thích.
- **Bước 2 (Thực hiện nhiệm vụ):** HS giơ thẻ chọn phương án C.
- **Bước 3 (Báo cáo, thảo luận):** HS giải thích: Chiều cao có thể nhận mọi giá trị trong một khoảng số thực.
- **Bước 4 (Kết luận, nhận định):** GV biểu dương và chuyển sang hoạt động ôn tập hệ thống.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (33 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức bằng sơ đồ tư duy (8 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ chuỗi quy trình thống kê: Thu thập $\\rightarrow$ Phân loại $\\rightarrow$ Biểu diễn $\\rightarrow$ Phân tích số liệu.
b) Nội dung: Quan sát và phân tích Sơ đồ tư duy Chương V: Dữ liệu và Biểu đồ thống kê.
c) Sản phẩm: Sơ đồ tư duy được khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy hệ thống hóa kiến thức Chương V.<br>- **GV:** Yêu cầu HS nêu các nhánh chính: Các cách thu thập dữ liệu; Các loại biểu đồ và mục đích sử dụng từng loại.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại mối liên hệ giữa bảng tần số và các loại biểu đồ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đại diện tóm tắt: Biểu đồ cột dùng so sánh số lượng; Biểu đồ đoạn thẳng theo dõi xu thế qua thời gian; Biểu đồ quạt tròn biểu diễn cơ cấu tỉ lệ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, nhấn mạnh kỹ năng lựa chọn biểu đồ đúng bản chất dữ liệu. | **SƠ ĐỒ TƯ DUY CHƯƠNG V: DỮ LIỆU VÀ BIỂU ĐỒ THỐNG KÊ**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Luyện tập chung Thống kê Toán 8](khbd-ill:mindmap-toan8-tiet34)

### Hoạt động 2.2: Luyện tập các bài toán phân tích và biểu diễn số liệu (15 phút)
a) Mục tiêu: Vận dụng biểu diễn bảng số liệu thành biểu đồ thích hợp và rút ra nhận xét.
b) Nội dung: Làm bài tập 5.15, 5.16 SGK trang 107 - 108.
c) Sản phẩm: Bài làm biểu diễn biểu đồ đoạn thẳng và nhận xét xu thế.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 5.15 SGK: Cho bảng số liệu nhiệt độ trung bình các tháng trong năm tại Hà Nội. Vẽ biểu đồ đoạn thẳng và nhận xét.<br>- **HS:** Làm việc theo nhóm 4 em.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định trục hoành (tháng 1 đến tháng 12), trục tung (nhiệt độ từ $0^\\circ\\text{C}$ đến $35^\\circ\\text{C}$), chấm điểm và nối các đoạn thẳng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện nhóm 1 dán bảng phụ vẽ biểu đồ lên bảng lớp.<br>- Các nhóm nhận xét chéo về tỉ lệ và độ chính xác của các điểm mốc.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kỹ năng dựng biểu đồ của HS, nhấn mạnh: Nhiệt độ thấp nhất vào tháng 1, cao nhất vào tháng 6 - 7. | **Bài 5.15 (SGK tr.107):**<br>- Dạng biểu đồ thích hợp: Biểu đồ đoạn thẳng (vì biểu diễn sự thay đổi của một đại lượng theo thời gian liên tục).<br>- Nhận xét: Nhiệt độ Hà Nội tăng dần từ tháng 1 đến tháng 6, đạt đỉnh vào mùa hè (tháng 6, tháng 7 khoảng $30^\\circ\\text{C}$), sau đó giảm dần từ tháng 8 đến tháng 12. |

### Hoạt động 2.3: Kiểm tra đánh giá thường xuyên (10 phút)
a) Mục tiêu: Đánh giá nhanh mức độ tiếp thu kiến thức thống kê của học sinh.
b) Nội dung: Làm bài kiểm tra ngắn 4 câu trắc nghiệm và 1 câu tự luận đọc biểu đồ.
c) Sản phẩm: Phiếu bài làm nộp cho GV chấm điểm.
d) Tổ chức thực hiện:
- GV phát đề kiểm tra ngắn. HS làm bài nghiêm túc, độc lập trong 10 phút. GV thu bài để đánh giá thường xuyên.

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
- **Tích hợp NLS 2.4.TC2a:** GV giao nhiệm vụ về nhà: Mỗi nhóm thu thập điểm trung bình học tập môn Toán của các bạn trong tổ, nhập vào Google Trang tính hoặc Excel, chia sẻ file cho GV qua email/Zalo nhóm và tạo một biểu đồ cột kép so sánh giữa nam và nữ. Dặn dò chuẩn bị Bài tập cuối chương V.
"""

# 09. Bài tập cuối chương V (Tiết 35)
md_09 = """Tiết 35 - BÀI TẬP CUỐI CHƯƠNG V (DỮ LIỆU VÀ BIỂU ĐỒ THỐNG KÊ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Tổng kết toàn diện kiến thức Chương V: Nhận biết tính đại diện của dữ liệu; Lựa chọn dạng biểu đồ thích hợp; Phân tích các thông tin thống kê để trả lời câu hỏi thực tiễn.
- Khắc phục các sai lầm thường gặp khi đọc biểu đồ: nhầm lẫn giữa tỉ lệ và tần số tuyệt đối, bỏ qua chú giải, đọc sai vạch chia trục số.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác hệ thống lại các bài toán tổng hợp cuối chương trong SGK.
- Giải quyết vấn đề và sáng tạo: Đề xuất các giải pháp dựa trên kết quả phân tích số liệu thống kê.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Biện luận tính hợp lí của các phương án thu thập mẫu dữ liệu.
- Năng lực mô hình hóa toán học: Dùng mô hình biểu đồ để giải thích các hiện tượng xã hội học tập.

c) Năng lực số (NLS):
- Năng lực số: Biết sử dụng máy tính bỏ túi tính toán tỉ lệ phần trăm chính xác đến hàng phần mười.

## 3. Về phẩm chất
- Trung thực, khách quan và có trách nhiệm trong xử lý và báo cáo thông tin dữ liệu.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy tổng kết Chương V, hệ thống bài tập trắc nghiệm và tự luận cuối chương V.
2. Học sinh: SGK Toán 8 tập 1, vở ghi, máy tính cầm tay, thước kẻ.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (4 phút)
a) Mục tiêu: Tạo hứng thú và kiểm tra mức độ sẵn sàng làm bài tập cuối chương.
b) Nội dung: Trả lời câu hỏi: Khi muốn biểu diễn tỉ lệ phần trăm các thành phần của một tổng thể, ta nên dùng loại biểu đồ nào?
c) Sản phẩm: Câu trả lời: Biểu đồ hình quạt tròn.
d) Tổ chức thực hiện: GV đặt câu hỏi nhanh, gọi 1 HS trả lời và vào bài mới.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (33 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức tổng kết Chương V (8 phút)
a) Mục tiêu: Ôn tập có hệ thống các kiến thức trọng tâm của Chương V bằng sơ đồ tư duy.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy tổng hợp Chương V.
c) Sản phẩm: Ghi nhớ cấu trúc nội dung toàn chương trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Sơ đồ tư duy tổng kết toàn bộ Chương V: Dữ liệu và Biểu đồ thống kê.<br>- **GV:** Đặt câu hỏi: Hãy nêu tiêu chí để một mẫu dữ liệu có tính đại diện?<br>- **HS:** Quan sát sơ đồ và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại: Kích thước mẫu đủ lớn và được chọn ngẫu nhiên, không thiên vị.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trình bày các lưu ý khi thu thập dữ liệu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu quy trình xử lý dữ liệu thống kê từ thực tế đến báo cáo. | **SƠ ĐỒ TƯ DUY TỔNG HỢP KIẾN THỨC CHƯƠNG V**<br><br>*(Sơ đồ tư duy tổng hợp hiển thị dưới đây)* |

![Sơ đồ tư duy Tổng kết Chương V Toán 8](khbd-ill:mindmap-toan8-tiet35)

### Hoạt động 2.2: Chữa các bài tập trắc nghiệm và tự luận cuối chương V (25 phút)
a) Mục tiêu: Vận dụng kiến thức giải quyết trọn vẹn các bài tập 5.17 đến 5.21 SGK trang 109 - 110.
b) Nội dung: Giải bài tập trắc nghiệm 5.17, 5.18 và bài toán tổng hợp 5.20 SGK.
c) Sản phẩm: Đáp án đúng và lời giải chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho HS làm nhanh các câu trắc nghiệm 5.17, 5.18 SGK trang 109.<br>- **GV:** Giao bài tập 5.20 SGK trang 110: Phân tích biểu đồ cột thể hiện lượng tiêu thụ điện năng qua các quý trong năm.<br>- **HS:** Làm việc cá nhân và trao đổi cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính toán tỉ lệ tăng trưởng giữa Quý II và Quý III.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng chữa bài.<br>- HS cả lớp nhận xét, bổ sung lập luận.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại kết quả, uốn nắn cách trình bày lời giải bài toán thống kê thực tiễn. | **1. Trắc nghiệm (SGK tr.109):**<br>- Bài 5.17: Chọn phương án **B** (Dữ liệu định lượng).<br>- Bài 5.18: Chọn phương án **C** (Biểu đồ quạt tròn biểu diễn tỉ lệ cơ cấu).<br><br>**2. Tự luận - Bài 5.20 (SGK tr.110):**<br>- Lượng điện tiêu thụ ở Quý III là cao nhất do thời tiết nắng nóng cao điểm của mùa hè.<br>- Mức tăng từ Quý I ($1200\\text{ kWh}$) lên Quý III ($2100\\text{ kWh}$) là:<br>$\\frac{2100 - 1200}{1200} \\cdot 100\\% = 75\\%$.<br>- Kết luận: Điện năng tiêu thụ mùa hè tăng $75\\%$ so với mùa xuân. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
- **Vận dụng thực tế:** GV yêu cầu học sinh liên hệ hóa đơn tiền điện của gia đình trong các tháng mùa nóng và mùa lạnh để giải thích nguyên nhân biến động theo bài học. Dặn dò chuẩn bị tiết Hoạt động thực hành trải nghiệm: Phân tích đặc điểm khí hậu Việt Nam.
"""

# 10. HĐTN: Phân tích đặc điểm khí hậu Việt Nam (Tiết 36)
md_10 = """Tiết 36 - HOẠT ĐỘNG THỰC HÀNH TRẢI NGHIỆM: PHÂN TÍCH ĐẶC ĐIỂM KHÍ HẬU VIỆT NAM
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng các kiến thức thu thập, phân loại, biểu diễn và phân tích dữ liệu thống kê vào một chủ đề tích hợp liên môn Địa lí - Khí hậu học Việt Nam.
- Đọc và phân tích biểu đồ nhiệt độ và lượng mưa của các trạm khí tượng tiêu biểu cho các miền khí hậu nước ta (Hà Nội, Đà Nẵng, TP. Hồ Chí Minh).
- Rút ra những đặc điểm nổi bật của khí hậu nhiệt đới gió mùa: tính chất nóng ẩm, mưa nhiều và sự phân hóa mùa rõ rệt.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tra cứu dữ liệu khí hậu qua sách báo và internet.
- Giao tiếp và hợp tác: Làm việc nhóm để thiết kế báo cáo thống kê khí hậu nhỏ.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hóa toán học: Xây dựng biểu đồ kết hợp (cột lượng mưa và đường nhiệt độ) để mô tả khí hậu một địa phương.
- Năng lực giải quyết vấn đề toán học: Tính nhiệt độ trung bình năm, tổng lượng mưa năm và biên độ nhiệt độ.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.1.TC2b: Tìm kiếm và trích xuất dữ liệu khí tượng thủy văn trực tuyến, xử lý bảng biểu trên máy tính.***

## 3. Về phẩm chất
- Tình yêu thiên nhiên, ý thức bảo vệ môi trường và ứng phó với biến đổi khí hậu toàn cầu.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, biểu đồ khí hậu trạm Láng (Hà Nội) và trạm Tân Sơn Nhất (TP. Hồ Chí Minh), máy chiếu, bảng phụ hoạt động nhóm.
2. Học sinh: SGK Toán 8 tập 1 trang 120 - 121, máy tính cầm tay, thước kẻ, bút màu.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Dẫn dắt học sinh vào chủ đề tích hợp Toán - Địa lí.
b) Nội dung: Trả lời câu hỏi: Việt Nam có mấy miền khí hậu chính và thời tiết nơi em sống có đặc trưng gì?
c) Sản phẩm: Câu trả lời mô tả thời tiết mùa đông - mùa hè của học sinh.
d) Tổ chức thực hiện: GV gợi mở câu hỏi, học sinh thảo luận sôi nổi và bước vào nội dung trải nghiệm.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC VÀ TRẢI NGHIỆM (28 phút)
### Hoạt động 2.1: Khai thác bảng số liệu khí hậu các trạm quan trắc (13 phút)
a) Mục tiêu: Tính toán các chỉ số thống kê cơ bản: nhiệt độ trung bình năm, biên độ nhiệt, tổng lượng mưa năm.
b) Nội dung: Đọc bảng số liệu nhiệt độ và lượng mưa trong SGK trang 120.
c) Sản phẩm: Bảng số liệu đã được tính toán đầy đủ các giá trị đặc trưng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chia lớp thành 3 nhóm lớn: Nhóm 1 nghiên cứu trạm Hà Nội; Nhóm 2 nghiên cứu trạm Đà Nẵng; Nhóm 3 nghiên cứu trạm TP. Hồ Chí Minh.<br>- **GV:** Giao nhiệm vụ tính: Nhiệt độ tháng cao nhất, thấp nhất, biên độ nhiệt độ; Tổng lượng mưa trong cả năm.<br>- **HS:** Sử dụng máy tính cầm tay để tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận, tính tổng lượng mưa 12 tháng và lấy trung bình cộng nhiệt độ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện mỗi nhóm điền kết quả vào bảng tổng hợp trên bảng lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa công thức: Biên độ nhiệt = $T_{\\max} - T_{\\min}$; Tổng lượng mưa = $\\sum_{i=1}^{12} P_i$. | **1. Các chỉ số khí hậu đặc trưng:**<br>- Trạm Hà Nội: $T_{\\max} = 29{,}8^\\circ\\text{C}$ (tháng 6), $T_{\\min} = 16{,}4^\\circ\\text{C}$ (tháng 1). Biên độ nhiệt: $29{,}8 - 16{,}4 = 13{,}4^\\circ\\text{C}$. Tổng lượng mưa: khoảng $1680\\text{ mm}$.<br>- Trạm TP. Hồ Chí Minh: Nhiệt độ trung bình quanh năm cao trên $27^\\circ\\text{C}$, biên độ nhiệt nhỏ ($3{,}1^\\circ\\text{C}$). Có hai mùa mưa - khô rõ rệt (mùa mưa từ tháng 5 đến tháng 11). |

### Hoạt động 2.2: Phân tích biểu đồ khí hậu và nhận xét (15 phút)
a) Mục tiêu: Đọc biểu đồ kết hợp (cột lượng mưa - đường nhiệt độ) và rút ra nhận xét về sự khác biệt giữa các miền khí hậu.
b) Nội dung: Quan sát biểu đồ khí hậu SGK trang 121, thảo luận trả lời các câu hỏi hướng dẫn.
c) Sản phẩm: Lời nhận xét phân hóa khí hậu Bắc - Nam.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt câu hỏi so sánh: Vì sao biên độ nhiệt ở miền Bắc lại lớn hơn rất nhiều so với miền Nam? Mùa mưa ở miền Trung có điểm gì đặc biệt?<br>- **HS:** Trao đổi nhóm đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vận dụng kiến thức gió mùa Đông Bắc và vị trí địa lí để giải thích số liệu toán học.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS phát biểu: Miền Bắc có mùa đông lạnh do chịu ảnh hưởng gió mùa Đông Bắc nên biên độ nhiệt lớn; Miền Trung mùa mưa lệch về thu đông (tháng 9 đến tháng 12).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao sự liên môn sâu sắc giữa Toán học và Địa lí của học sinh. | **2. Nhận xét đặc điểm khí hậu Việt Nam qua số liệu:**<br>- Khí hậu nhiệt đới gió mùa ẩm: Tổng lượng mưa lớn (trên $1500\\text{ mm}$), nhiệt độ trung bình năm cao.<br>- Tính phân hóa đa dạng: Miền Bắc có mùa đông lạnh, nhiệt độ hạ thấp; Miền Nam nóng quanh năm; Miền Trung mưa nhiều vào các tháng cuối năm. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (7 phút)
- Hoàn thành bài thu hoạch trải nghiệm cá nhân: Ghi tóm tắt 3 kết luận toán học rút ra từ biểu đồ khí hậu vào vở.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
- **Tích hợp NLS 1.1.TC2b:** GV hướng dẫn học sinh truy cập trang web `kttv.gov.vn` để xem biểu đồ dự báo xu thế thời tiết tuần tới của địa phương. Dặn dò chuẩn bị chu đáo cho 3 tiết Ôn tập học kì I môn Toán 8.
"""

# 11. Ôn tập học kì I (Đại số - Tiết 37, 38, 39)
md_11 = """Tiết 37, 38, 39 - ÔN TẬP HỌC KÌ I (ĐẠI SỐ VÀ THỐNG KÊ)
*Thời lượng thực hiện: 03 tiết (135 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Đại số và Thống kê Học kì I Toán 8:
  + Chương I: Đơn thức và đa thức nhiều biến; Các phép toán cộng, trừ, nhân, chia đơn thức và đa thức.
  + Chương II: Bảy hằng đẳng thức đáng nhớ; Các phương pháp phân tích đa thức thành nhân tử và ứng dụng.
  + Chương V: Thu thập, phân loại, biểu diễn và phân tích dữ liệu thống kê qua các dạng bảng, biểu đồ.
- Rèn luyện kỹ năng biến đổi đại số thành thạo, tính nhanh hợp lí, giải bài toán tìm giá trị của biến và phân tích số liệu thực tế.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa toàn bộ sơ đồ kiến thức Đại số & Thống kê HKI.
- Giao tiếp và hợp tác: Tích cực trao đổi, chữa bài tập tổng hợp cho bạn trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khái quát hóa các dạng bài tập phân tích đa thức và ứng dụng.
- Năng lực giải quyết vấn đề toán học: Phối hợp linh hoạt nhiều phương pháp đại số để tìm cực trị đơn giản hoặc rút gọn biểu thức phức tạp.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 1.2.TC2a: Tìm kiếm và chọn lọc tài liệu ôn tập trực tuyến đáng tin cậy.***
- ***Giáo dục AI (9.D1.1): Làm quen với việc sử dụng công cụ AI kiểm tra bước biến đổi đại số hoặc gợi ý bài tập nâng cao phù hợp.***

## 3. Về phẩm chất
- Kiên trì, cẩn thận, chính xác trong từng bước biến đổi dấu và lũy thừa.
- Tự giác, trung thực trong quá trình tự ôn tập chuẩn bị kiểm tra học kì I.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Ôn tập tổng hợp HKI (Đại số & Thống kê), hệ thống đề cương ôn tập phân hóa 4 mức độ.
2. Học sinh: SGK Toán 8 tập 1, vở ghi, đề cương ôn tập học kì I, máy tính cầm tay, giấy nháp.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Xác định rõ mục tiêu ôn tập học kì I và tạo động lực phấn đấu đạt kết quả cao.
b) Nội dung: Điểm lại cấu trúc đề kiểm tra học kì I môn Toán 8 (tỉ lệ trắc nghiệm - tự luận, phân bố điểm các chương).
c) Sản phẩm: Tâm thế học tập tích cực, sẵn sàng ôn tập của học sinh.
d) Tổ chức thực hiện: GV công bố cấu trúc đề thi, nhắc nhở thái độ học tập và dẫn dắt vào bài ôn tập.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (110 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Đại số và Thống kê qua Sơ đồ tư duy (20 phút)
a) Mục tiêu: Khái quát toàn bộ mạng lưới kiến thức Đại số HKI một cách trực quan, mạch lạc.
b) Nội dung: Trình chiếu, phân tích Sơ đồ tư duy Ôn tập học kì I (Đại số & Thống kê).
c) Sản phẩm: Sơ đồ tư duy được vẽ và khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Ôn tập tổng hợp Đại số & Thống kê HKI.<br>- **GV:** Yêu cầu HS nêu 3 nhánh kiến thức cốt lõi: Phép toán đa thức nhiều biến; Hằng đẳng thức & Phân tích thành nhân tử; Thống kê & Biểu đồ.<br>- **HS:** Theo dõi sơ đồ và nhắc lại các công thức then chốt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Viết lại 7 hằng đẳng thức đáng nhớ và 4 phương pháp phân tích đa thức vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS đọc thuộc lòng các hằng đẳng thức bậc 2 và bậc 3.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại các lỗi học sinh hay nhầm lẫn: Dấu trong hiệu hai lập phương và lập phương của một hiệu. | **SƠ ĐỒ TƯ DUY ÔN TẬP HỌC KÌ I: ĐẠI SỐ VÀ THỐNG KÊ**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Ôn tập Học kì I Đại số và Thống kê Toán 8](khbd-ill:mindmap-toan8-tiet37_39)

### Hoạt động 2.2: Rèn luyện kỹ năng thực hiện phép tính và rút gọn đa thức (30 phút)
a) Mục tiêu: Thành thạo các phép toán cộng, trừ, nhân đa thức và chia đa thức cho đơn thức.
b) Nội dung: Giải các bài tập rút gọn biểu thức trong đề cương ôn tập.
c) Sản phẩm: Lời giải chính xác trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao các bài tập rút gọn biểu thức:<br>a) $A = 2x(x - 3) - (x + 2)(2x - 1)$<br>b) $B = (x + 2y)^2 - (x - 2y)^2$<br>c) $C = (x - 1)(x^2 + x + 1) - x(x^2 - 2)$<br>- **HS:** Làm việc độc lập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện khai triển hằng đẳng thức và nhân đơn thức với đa thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt đáp số đúng. | **Dạng 1: Rút gọn biểu thức:**<br>a) $A = 2x^2 - 6x - (2x^2 - x + 4x - 2) = 2x^2 - 6x - 2x^2 - 3x + 2 = -9x + 2$.<br>b) $B = [(x + 2y) - (x - 2y)][(x + 2y) + (x - 2y)] = (4y)(2x) = 8xy$.<br>*(Cách 2: Khai triển từng bình phương rồi trừ)*.<br>c) $C = (x^3 - 1) - (x^3 - 2x) = x^3 - 1 - x^3 + 2x = 2x - 1$. |

### Hoạt động 2.3: Rèn luyện kỹ năng phân tích đa thức thành nhân tử và tìm x (35 phút)
a) Mục tiêu: Vận dụng linh hoạt các phương pháp phân tích đa thức thành nhân tử để giải phương trình tích và tính nhanh.
b) Nội dung: Giải các bài toán phân tích và tìm $x$.
c) Sản phẩm: Lời giải chi tiết của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập:<br>1. Phân tích thành nhân tử: $x^2 - 4y^2 + 2x + 1$; $x^2 - 7x + 12$.<br>2. Tìm $x$ biết: $x^2 - 25 = 0$; $x(x - 2) + 3(x - 2) = 0$.<br>- **HS:** Làm bài theo cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận dạng: $x^2 + 2x + 1 = (x + 1)^2$, tách $7x = 3x + 4x$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS lên bảng chữa.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Uốn nắn cách kết luận giá trị của $x$, không dùng dấu tương đương $\\Leftrightarrow$ rời rạc không có lời giải thích. | **Dạng 2: Phân tích thành nhân tử & Tìm $x$:**<br>1. $x^2 - 4y^2 + 2x + 1 = (x^2 + 2x + 1) - (2y)^2 = (x + 1)^2 - (2y)^2 = (x + 1 - 2y)(x + 1 + 2y)$.<br>$x^2 - 7x + 12 = x^2 - 3x - 4x + 12 = x(x - 3) - 4(x - 3) = (x - 3)(x - 4)$.<br><br>2. Tìm $x$:<br>a) $x^2 - 25 = 0$ suy ra $(x - 5)(x + 5) = 0$. Do đó $x = 5$ hoặc $x = -5$.<br>b) $x(x - 2) + 3(x - 2) = 0$ suy ra $(x - 2)(x + 3) = 0$. Do đó $x = 2$ hoặc $x = -3$. |

### Hoạt động 2.4: Rèn luyện giải bài toán thống kê thực tiễn (25 phút)
a) Mục tiêu: Đọc biểu đồ, phân tích số liệu và giải quyết các bài toán tỉ lệ thực tế.
b) Nội dung: Làm bài toán phân tích biểu đồ cơ cấu và biểu đồ tăng trưởng trong đề cương.
c) Sản phẩm: Bài giải hoàn chỉnh của học sinh.
d) Tổ chức thực hiện:
- GV chiếu biểu đồ thống kê cơ cấu sản lượng nông sản. HS tính toán sản lượng từng loại mặt hàng khi biết tổng sản lượng và tỉ lệ phần trăm. GV chốt đáp số và kỹ năng phân tích bảng số liệu.

## C. HOẠT ĐỘNG 3: VẬN DỤNG (20 phút)
- **Bài toán vận dụng cao:** Tìm giá trị nhỏ nhất của biểu thức $P = x^2 - 4x + y^2 - 6y + 20$.
  + Hướng dẫn giải: Biến đổi $P = (x^2 - 4x + 4) + (y^2 - 6y + 9) + 7 = (x - 2)^2 + (y - 3)^2 + 7$.
  + Vì $(x - 2)^2 \\ge 0$ và $(y - 3)^2 \\ge 0$ với mọi $x, y$ nên $P \\ge 7$.
  + Dấu bằng xảy ra khi $x - 2 = 0$ và $y - 3 = 0$, tức là $x = 2$ và $y = 3$.
  + Vậy giá trị nhỏ nhất của $P$ bằng $7$, đạt được khi $x = 2$ và $y = 3$.
- Dặn dò học sinh ôn tập kỹ lưỡng chuẩn bị kiểm tra đánh giá cuối học kì I.
"""

# 12. Kiểm tra đánh giá cuối HKI & Trả bài (Đại số - Tiết 40, 41)
md_12 = """Tiết 40, 41 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I VÀ TRẢ BÀI (ĐẠI SỐ)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá chuẩn xác mức độ đạt chuẩn kiến thức, kĩ năng của học sinh sau khi hoàn thành chương trình Học kì I môn Toán 8 mảng Đại số và Thống kê.
- Nhận biết các lỗ hổng kiến thức, các lỗi sai phổ biến của học sinh để có kế hoạch phụ đạo, bồi dưỡng trong Học kì II.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác, nghiêm túc làm bài kiểm tra; tự đánh giá kết quả và sửa chữa lỗi sai khi nhận bài kiểm tra.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học; Năng lực giải quyết vấn đề toán học: Trình bày bài thi mạch lạc, khoa học, đúng chuẩn mực đại số.

## 3. Về phẩm chất
- Trung thực, nghiêm túc, tự giác, có trách nhiệm với kết quả rèn luyện của bản thân.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo ma trận và bản đặc tả đề kiểm tra cuối HKI, đáp án và thang điểm chi tiết; Sổ điểm điện tử.
2. Học sinh: Bút viết, máy tính cầm tay, thước kẻ, giấy nháp.

# III. TIẾN TRÌNH DẠY HỌC
## A. TIẾT 40: KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (45 phút)
### 1. Ổn định lớp và phát đề (3 phút)
- GV kiểm tra sĩ số, phổ biến nội quy phòng thi, yêu cầu học sinh cất tài liệu vào ngăn bàn.
- GV phát đề kiểm tra đến từng học sinh.

### 2. Học sinh làm bài kiểm tra (40 phút)
- Học sinh làm bài kiểm tra nghiêm túc, độc lập theo đúng thời gian quy định.
- Giáo viên bao quát phòng kiểm tra, theo dõi và nhắc nhở học sinh giữ trật tự.

### 3. Thu bài kiểm tra (2 phút)
- GV yêu cầu học sinh dừng bút, kiểm tra lại họ tên, lớp và số tờ giấy thi.
- GV thu bài theo từng bàn, kiểm đếm đủ số lượng bài thi trước khi cho học sinh nghỉ.

## B. TIẾT 41: TRẢ BÀI KIỂM TRA HỌC KÌ I VÀ SỬA BÀI (45 phút)
### Hoạt động 1: Nhận xét chung về kết quả bài kiểm tra (10 phút)
- **Ưu điểm:** Đa số học sinh nắm vững các hằng đẳng thức đáng nhớ, thực hiện phép nhân đơn thức với đa thức tốt, đọc biểu đồ thống kê cơ bản chính xác.
- **Tồn tại:** Một số em còn nhầm dấu khi khai triển lập phương của một hiệu, phân tích đa thức thành nhân tử chưa triệt để, lập luận thiếu chặt chẽ khi tìm $x$.
- GV công bố phổ điểm chung của lớp: Giỏi, Khá, Trung bình, Yếu.

### Hoạt động 2: Hướng dẫn chữa bài và hoàn thiện lời giải chuẩn (25 phút)
- GV chữa chi tiết từng câu trong đề thi trên bảng:
  + Chữa các câu trắc nghiệm hay chọn nhầm và giải thích nguyên nhân gây nhiễu.
  + Chữa câu phân tích đa thức thành nhân tử phối hợp nhiều phương pháp.
  + Chữa câu tìm giá trị nhỏ nhất của biểu thức bậc hai.
- Học sinh chú ý đối chiếu với bài làm của mình, chữa vào vở các câu làm sai.

### Hoạt động 3: Đánh giá cá nhân và kế hoạch cải tiến Học kì II (10 phút)
- GV trả bài kiểm tra cho từng học sinh xem lại và ký nhận điểm số.
- Học sinh giải đáp thắc mắc (nếu có khiếu nại về điểm).
- GV giao bài tập rèn luyện thêm cho nhóm học sinh còn yếu để củng cố kiến thức trong kì nghỉ giữa hai học kì.
"""

tasks = [
    ("07_KHBD_Toan8_Bai20_PhanTichSoLieuThongKe_Tiet33.md", md_07),
    ("08_KHBD_Toan8_LuyenTapChung_ThongKe_Tiet34.md", md_08),
    ("09_KHBD_Toan8_BaiTapCuoiChuong5_Tiet35.md", md_09),
    ("10_KHBD_Toan8_HDTN_PhanTichDacDiemKhiHauVN_Tiet36.md", md_10),
    ("11_KHBD_Toan8_OnTapCuoiHK1_DaiSo_Tiet37-39.md", md_11),
    ("12_KHBD_Toan8_KiemTraTraBaiCuoiHK1_DaiSo_Tiet40-41.md", md_12),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
