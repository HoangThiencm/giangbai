# -*- coding: utf-8 -*-
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = r"c:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\TEMP\02.11"

# ==============================================================================
# 1. CẬP NHẬT 03_OnTapGiuaHK1_DaiSo.md
# ==============================================================================
f03_content = """Tiết 25 - ÔN TẬP GIỮA HỌC KÌ I (ĐẠI SỐ)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức trọng tâm phần Đại số nửa đầu Học kì I:
  + Phương trình quy về phương trình bậc nhất một ẩn (phương trình tích, phương trình chứa ẩn ở mẫu).
  + Khái niệm phương trình bậc nhất hai ẩn; các phương pháp giải hệ hai phương trình bậc nhất hai ẩn (phương pháp thế, phương pháp cộng đại số).
  + Các bước giải bài toán bằng cách lập hệ phương trình.
  + Bất đẳng thức và bất phương trình bậc nhất một ẩn: tính chất liên hệ thứ tự; cách giải và biểu diễn tập nghiệm trên trục số.
  + Căn bậc hai số học, điều kiện xác định của căn thức bậc hai $\\sqrt{A}$ ($A \\ge 0$) và hằng đẳng thức $\\sqrt{A^2} = |A|$.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác hệ thống hóa kiến thức đại số giữa HKI qua sơ đồ tư duy trực quan.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải ngắn gọn, mạch lạc trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phân tích mối quan hệ đại lượng, lựa chọn ẩn số và đặt điều kiện thích hợp cho bài toán thực tế.
- Năng lực giải quyết vấn đề toán học: Vận dụng linh hoạt các thuật toán đại số để tìm nghiệm chính xác của phương trình, hệ phương trình và căn thức.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng thành thạo máy tính cầm tay để giải hệ hai phương trình bậc nhất hai ẩn, kiểm tra nhanh nghiệm của phương trình và tính căn bậc hai số học.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***9.D1.1: HS phối hợp sử dụng trợ lý học tập AI để tra cứu các lỗi sai phổ biến khi làm bài thi giữa kì và tự kiểm tra chéo các bước giải.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, kỷ luật, tự kiểm tra lại kết quả giải toán bằng máy tính cầm tay trước khi nộp bài.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 1, Kế hoạch bài dạy, hình ảnh Sơ đồ tư duy Mindmap Đại số giữa HKI, máy chiếu/tivi, đề cương ôn tập.
2. Học sinh: SGK Toán 9, vở ghi, máy tính cầm tay, bút dạ, bảng nhóm.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy và tổng kết nhanh các mảng kiến thức Đại số nửa đầu HKI qua trò chơi trắc nghiệm phản xạ.
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm nhanh trên màn chiếu về hệ phương trình, bất đẳng thức và căn thức.
c) Sản phẩm: Bảng chọn đáp án A, B, C, D của các nhóm học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 4 câu hỏi trắc nghiệm nhanh:<br>  1. Hệ phương trình $\\begin{cases} x + y = 3 \\\\ x - y = 1 \\end{cases}$ có nghiệm là gì?<br>  2. Bất phương trình $-2x > 6$ có nghiệm là gì?<br>  3. Điều kiện xác định của $\\sqrt{2x - 4}$ là gì?<br>  4. Giá trị của $\\sqrt{(-5)^2}$ bằng bao nhiêu?<br>- **HS:** Chuẩn bị bảng con để giơ đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ bảng đáp án ngay khi có hiệu lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS giải thích vì sao chọn đáp án và nêu các bẫy dễ nhầm (như đổi chiều khi chia số âm, căn bậc hai số học không thể âm).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ phản xạ và dẫn dắt vào bài học ôn tập. | **Câu hỏi khởi động:**<br>1. Nghiệm hệ: $(x; y) = (2; 1)$.<br>2. Bất phương trình: $x < -3$ (chia cho $-2 < 0$ đổi chiều).<br>3. ĐKXĐ: $2x - 4 \\ge 0 \\Rightarrow x \\ge 2$.<br>4. $\\sqrt{(-5)^2} = |-5| = 5$. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức bằng Sơ đồ tư duy (10 phút)
a) Mục tiêu: Khắc sâu cấu trúc lý thuyết phương pháp giải hệ phương trình, bất phương trình và căn thức bậc hai thông qua sơ đồ tư duy trực quan; tích hợp chỉ báo AI 9.D1.1.
b) Nội dung: GV trình chiếu và hướng dẫn HS phân tích Sơ đồ tư duy tổng kết Đại số 9 giữa HKI.

![Sơ đồ tư duy Ôn tập Đại số giữa Học kì I](khbd-ill:mindmap-03)

c) Sản phẩm: Sơ đồ tư duy được ghi nhận và tóm tắt phương pháp giải vào vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy tổng hợp Đại số 9 Giữa Học kì I gồm 3 nhánh lớn:<br>  1. Phương trình & Hệ hai phương trình bậc nhất hai ẩn.<br>  2. Bất đẳng thức & Bất phương trình bậc nhất một ẩn.<br>  3. Căn bậc hai & Căn thức bậc hai.<br>- Yêu cầu HS quan sát sơ đồ, thảo luận cặp đôi để nhắc lại các thuật toán then chốt của từng nhánh.<br>- ***Tích hợp AI (9.D1.1): GV cho học sinh quan sát bảng cảnh báo do AI tổng hợp về 3 lỗi sai phổ biến học sinh hay mắc phải: (1) Quên đặt ĐKXĐ khi giải PT chứa ẩn ở mẫu hoặc căn thức; (2) Quên đổi chiều BĐT khi chia cho số âm; (3) Khai căn quên đặt dấu giá trị tuyệt đối.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát Sơ đồ tư duy, hệ thống lại kiến thức và ghi chép các điểm cốt lõi vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết minh lại 3 nhánh chính của sơ đồ tư duy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc ghi nhớ và chuyển sang phần giải bài tập trọng tâm. | **Hệ thống kiến thức trọng tâm (Mindmap):**<br>- **Nhánh 1 (Hệ PT):**<br>  + Phương pháp thế: Rút 1 ẩn từ PT này thế vào PT kia.<br>  + Phương pháp cộng đại số: Nhân tạo hệ số bằng hoặc đối nhau rồi trừ hoặc cộng.<br>- **Nhánh 2 (BĐT & BPT):**<br>  + Nhân/chia 2 vế với số âm bắt buộc phải đổi chiều BĐT.<br>- **Nhánh 3 (Căn bậc hai):**<br>  + $\\sqrt{A}$ có nghĩa khi và chỉ khi $A \\ge 0$.<br>  + Hằng đẳng thức: $\\sqrt{A^2} = |A| = \\begin{cases} A & \\text{khi } A \\ge 0 \\\\ -A & \\text{khi } A < 0 \\end{cases}$. |

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)
a) Mục tiêu: Rèn luyện kỹ năng giải hệ phương trình, giải bài toán thực tế bằng cách lập hệ PT và rút gọn căn thức; tích hợp chỉ báo NLS 5.2.TC2b.
b) Nội dung: Giải 3 bài tập điển hình thường gặp trong đề kiểm tra giữa kì I.
c) Sản phẩm: Lời giải hoàn chỉnh 3 bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao 3 bài tập lên bảng:<br>  **Bài 1:** Giải hệ phương trình: $\\begin{cases} 3x - 2y = 7 \\\\ 2x + 3y = 9 \\end{cases}$<br>  **Bài 2:** Hai tổ công nhân cùng làm chung một công việc trong 12 giờ thì hoàn thành. Nếu tổ thứ nhất làm trong 4 giờ và tổ thứ hai làm trong 6 giờ thì cả hai tổ làm được $\\frac{2}{5}$ công việc. Hỏi mỗi tổ làm một mình thì sau bao lâu xong công việc?<br>  **Bài 3:** Rút gọn biểu thức $P = \\sqrt{(2 - \\sqrt{5})^2} + \\sqrt{5} - \\sqrt{9x^2}$ với $x < 0$.<br>- ***Tích hợp NLS (5.2.TC2b): HS sử dụng máy tính cầm tay bấm kiểm tra trước nghiệm của Bài 1 để định hướng các bước giải.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cá nhân làm bài vào vở. 3 HS đại diện lên bảng thực hiện.<br>- **GV:** Quan sát, hướng dẫn học sinh trình bày dạng toán năng suất làm chung - riêng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS trên bảng trình bày chi tiết từng bước. Cả lớp đổi vở chéo kiểm tra.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa lời giải và thang điểm từng bước. | **Bài 1:**<br>$\\begin{cases} 3x - 2y = 7 \\\\ 2x + 3y = 9 \\end{cases} \\Rightarrow \\begin{cases} 6x - 4y = 14 \\\\ 6x + 9y = 27 \\end{cases} \\Rightarrow \\begin{cases} 13y = 13 \\\\ 3x - 2y = 7 \\end{cases} \\Rightarrow \\begin{cases} x = 3 \\\\ y = 1 \\end{cases}$.<br>Vậy hệ phương trình có nghiệm duy nhất là $(3; 1)$.<br><br>**Bài 2:**<br>- Gọi thời gian tổ 1 làm một mình xong công việc là $x$ (giờ, $x > 12$).<br>- Gọi thời gian tổ 2 làm một mình xong công việc là $y$ (giờ, $y > 12$).<br>- Trong 1 giờ, tổ 1 làm được $\\frac{1}{x}$ (công việc), tổ 2 làm được $\\frac{1}{y}$ (công việc).<br>- Vì hai tổ cùng làm trong 12 giờ xong nên: $\\frac{1}{x} + \\frac{1}{y} = \\frac{1}{12}$.<br>- Theo đề bài: $\\frac{4}{x} + \\frac{6}{y} = \\frac{2}{5}$.<br>- Đặt $u = \\frac{1}{x}, v = \\frac{1}{y}$, ta có hệ: $\\begin{cases} u + v = \\frac{1}{12} \\\\ 4u + 6v = \\frac{2}{5} \\end{cases} \\Rightarrow \\begin{cases} u = \\frac{1}{20} \\\\ v = \\frac{1}{30} \\end{cases}$.<br>- Suy ra: $x = 20$ (thỏa mãn), $y = 30$ (thỏa mãn).<br>Vậy tổ 1 làm một mình trong 20 giờ; tổ 2 làm trong 30 giờ.<br><br>**Bài 3:**<br>$P = |2 - \\sqrt{5}| + \\sqrt{5} - \\sqrt{(3x)^2}$.<br>Vì $2 < \\sqrt{5} \\Rightarrow |2 - \\sqrt{5}| = \\sqrt{5} - 2$.<br>Vì $x < 0 \\Rightarrow |3x| = -3x$.<br>Suy ra: $P = (\\sqrt{5} - 2) + \\sqrt{5} - (-3x) = 2\\sqrt{5} - 2 + 3x$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Giúp học sinh định hình cấu trúc đề kiểm tra giữa kì I và củng cố chiến lược làm bài thi.
b) Nội dung: Phân bổ thời gian làm bài kiểm tra giữa HKI và hướng dẫn tự học.
c) Sản phẩm: Bản ghi nhớ chiến thuật làm bài thi của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chiến thuật làm bài thi kiểm tra giữa HKI:<br>  1. Làm phần trắc nghiệm nhanh, cẩn thận với câu phủ định và điều kiện xác định.<br>  2. Kiểm tra lại nghiệm của hệ PT bằng máy tính Casio.<br>  3. Trình bày bài toán thực tế đầy đủ đơn vị và kết luận rõ ràng.<br>- **HS:** Lắng nghe, ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt các câu hỏi còn vướng mắc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- GV giải đáp nhanh cho cả lớp.<br><br>**+ Bước 4: Kết luận, nhận định & Dặn dò**<br>- **GV:** Nhắc nhở HS chuẩn bị chu đáo máy tính và dụng cụ cho tiết Kiểm tra đánh giá giữa HKI (Tiết 26). | **Dặn dò tự học tại nhà:**<br>1. Ôn tập kỹ các nhánh kiến thức trong Sơ đồ tư duy.<br>2. Tự giải lại các bài toán lập hệ phương trình năng suất và chuyển động trong SGK.<br>3. Chuẩn bị đầy đủ máy tính cầm tay và giấy nháp cho bài kiểm tra giữa kì I. |
"""

with open(os.path.join(TEMP_DIR, "03_OnTapGiuaHK1_DaiSo.md"), 'w', encoding='utf-8') as f:
    f.write(f03_content)
print(" -> Đã cập nhật chuẩn CV 5512 V2.1 + Mindmap: 03_OnTapGiuaHK1_DaiSo.md")

# ==============================================================================
# 2. CẬP NHẬT 04_OnTapGiuaHK1_HinhHoc.md
# ==============================================================================
f04_content = """Tiết 13 - ÔN TẬP GIỮA HỌC KÌ I (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức trọng tâm phần Hình học nửa đầu Học kì I:
  + Tỉ số lượng giác của góc nhọn ($\\sin, \\cos, \\tan, \\cot$); bảng tỉ số lượng giác góc đặc biệt.
  + Hệ thức về cạnh và góc trong tam giác vuông: cạnh góc vuông bằng cạnh huyền nhân $\\sin$ góc đối hoặc $\\cos$ góc kề; bằng cạnh góc vuông kia nhân $\\tan$ góc đối hoặc $\\cot$ góc kề. Ứng dụng giải bài toán thực tế.
  + Đường tròn: Định nghĩa, tính chất đối xứng (tâm đối xứng $O$, vô số trục đối xứng qua tâm).
  + Cung và dây của đường tròn: Góc ở tâm, số đo cung; định lý liên hệ giữa cung và dây; định lý đường kính vuông góc với dây.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Chủ động tổng kết hệ thống công thức tỉ số lượng giác và tính chất đường tròn qua sơ đồ tư duy.
- Giao tiếp và hợp tác: Trình bày bài giải hình học trước tập thể lớp mạch lạc, logic, vẽ hình chuẩn xác.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Suy luận hình học từ tam giác vuông, áp dụng định lý Pythagore kết hợp hệ thức lượng giác.
- Năng lực mô hình hóa toán học: Chuyển đổi bài toán thực tế (chiều cao hải đăng, bóng cây) thành mô hình tam giác vuông để tính toán.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng máy tính cầm tay bấm chính xác các hàm lượng giác sin, cos, tan, đổi góc từ số thập phân sang độ - phút - giây và ngược lại.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***9.D1.1: HS ứng dụng trợ lý học tập AI để tra cứu các tình huống ứng dụng thực tiễn của hệ thức lượng trong kiến trúc, hàng hải.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn trọng, tỉ mỉ khi vẽ hình bằng compa và thước thẳng.
- Tự tin chuẩn bị tâm thế vững vàng cho bài kiểm tra giữa Học kì I.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 1, KHBD, hình ảnh Sơ đồ tư duy Mindmap Hình học giữa HKI, thước thẳng, compa bảng, máy chiếu.
2. Học sinh: SGK Toán 9, vở ghi, bộ dụng cụ vẽ hình (thước kẻ, compa, thước đo độ), máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Ôn lại nhanh các công thức lượng giác và tính chất đường tròn qua trò chơi phản xạ nhanh.
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm nhanh chiếu trên màn hình.
c) Sản phẩm: Thẻ câu trả lời A, B, C, D của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu 4 câu hỏi trắc nghiệm ngắn:<br>  1. Trong tam giác vuông, $\\sin$ của góc nhọn bằng tỉ số nào?<br>  2. Nếu $\\alpha + \\beta = 90^\\circ$ thì $\\sin \\alpha$ bằng tỉ số lượng giác nào của $\\beta$?<br>  3. Góc có đỉnh nằm ở tâm đường tròn được gọi là góc gì?<br>  4. Đường kính vuông góc với dây thì đi qua vị trí nào của dây đó?<br>- **HS:** Chuẩn bị bảng con trả lời nhanh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát và giơ đáp án sau hiệu lệnh 5 giây.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đọc thuộc bài vè ghi nhớ tỉ số lượng giác: "Tìm sin lấy đối chia huyền, Cosin lấy cạnh kề huyền chia nhau, Còn tang ta tính làm sao: Đối trên kề dưới thế nào cũng ra".<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương tinh thần học tập và dẫn dắt vào bài học ôn tập. | **Ghi nhớ nhanh:**<br>1. $\\sin = \\frac{\\text{Đối}}{\\text{Huyền}}$, $\\cos = \\frac{\\text{Kề}}{\\text{Huyền}}$, $\\tan = \\frac{\\text{Đối}}{\\text{Kề}}$, $\\cot = \\frac{\\text{Kề}}{\\text{Đối}}$.<br>2. Nếu $\\alpha + \\beta = 90^\\circ$ thì $\\sin \\alpha = \\cos \\beta$; $\\tan \\alpha = \\cot \\beta$.<br>3. Góc ở tâm.<br>4. Đi qua trung điểm của dây và điểm chính giữa của cung bị chắn. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức bằng Sơ đồ tư duy (10 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ công thức giải tam giác vuông và các tính chất cơ bản của đường tròn; tích hợp chỉ báo AI 9.D1.1.
b) Nội dung: GV trình chiếu Sơ đồ tư duy Mindmap tổng kết Hình học 9 Giữa Học kì I.

![Sơ đồ tư duy Ôn tập Hình học giữa Học kì I](khbd-ill:mindmap-04)

c) Sản phẩm: Bảng công thức và sơ đồ tư duy được khắc sâu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Hình học 9 Giữa HKI gồm 3 nhánh lớn:<br>  1. Hệ thức lượng trong tam giác vuông (Tỉ số lượng giác, hệ thức cạnh và góc).<br>  2. Khái niệm và tính chất đối xứng của đường tròn.<br>  3. Cung và Dây của đường tròn (Góc ở tâm, liên hệ cung - dây, đường kính vuông góc với dây).<br>- Yêu cầu HS đọc sơ đồ và nhắc lại các hệ thức then chốt.<br>- ***Tích hợp AI (9.D1.1): GV cho học sinh quan sát bảng tra cứu nhanh do AI gợi ý về mối liên hệ giữa góc nâng, góc hạ trong các bài toán thực tế đo bóng cây, ngọn hải đăng.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát sơ đồ tư duy, hệ thống lại kiến thức và ghi vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ nêu rõ từng hệ thức cạnh - góc trong tam giác vuông.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại hai khối kiến thức trọng tâm của đề thi và chuyển sang luyện giải bài tập. | **1. Hệ thức lượng trong tam giác vuông:**<br>Trong $\\Delta ABC$ vuông tại $A$ ($a = BC, b = AC, c = AB$):<br>- $b = a \\cdot \\sin B = a \\cdot \\cos C$<br>- $c = a \\cdot \\sin C = a \\cdot \\cos B$<br>- $b = c \\cdot \\tan B = c \\cdot \\cot C$<br>- $c = b \\cdot \\tan C = b \\cdot \\cot B$<br><br>**2. Kiến thức về đường tròn (Chương V):**<br>- Tâm đối xứng: Tâm $O$; Trục đối xứng: Mọi đường thẳng qua tâm.<br>- $\\text{sđ }\\wideparen{AB} = \\widehat{AOB}$ (cung nhỏ).<br>- $OH \\perp AB \\Rightarrow H$ là trung điểm dây $AB$ ($AB$ không qua tâm). Khi đó: $R^2 = OH^2 + (AB/2)^2$. |

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)
a) Mục tiêu: Rèn luyện kỹ năng giải tam giác vuông bài toán thực tế và bài toán tính khoảng cách từ tâm đến dây trong đường tròn; tích hợp chỉ báo NLS 5.2.TC2b.
b) Nội dung: Giải 2 bài toán tổng hợp bám sát cấu trúc đề kiểm tra giữa kì.
c) Sản phẩm: Lời giải chi tiết vẽ hình chính xác trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu 2 bài toán trọng tâm:<br>  **Bài 1 (Thực tế):** Một tháp hải đăng cao $45\\text{ m}$. Một người từ đỉnh tháp nhìn thấy một con thuyền đang neo đậu trên biển dưới góc nghiêng xuống (góc hạ) so với phương nằm ngang là $28^\\circ$. Hỏi con thuyền cách chân tháp bao nhiêu mét (làm tròn kết quả đến hàng phần mười)?<br>  **Bài 2 (Hình học thuần túy):** Cho đường tròn $(O; R = 10\\text{ cm})$ và dây $AB = 16\\text{ cm}$.<br>  a) Tính khoảng cách từ tâm $O$ đến dây $AB$.<br>  b) Gọi $I$ là trung điểm của dây $AB$. Tia $OI$ cắt đường tròn $(O)$ tại điểm $C$. Chứng minh $CA = CB$ và tam giác $ABC$ cân.<br>- ***Tích hợp NLS (5.2.TC2b): HS sử dụng máy tính cầm tay bấm tan 28 độ và kiểm tra kết quả làm tròn thập phân.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Vẽ hình bài toán thực tế dưới dạng tam giác vuông $ABC$. Giải bài 2 vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Hai HS đại diện lên bảng trình bày. HS dưới lớp nhận xét, bổ sung.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt cách vẽ hình chuẩn và lập luận chặt chẽ. | **Bài 1:**<br>- Mô hình hóa bằng tam giác $ABC$ vuông tại $B$ ($AB = 45\\text{ m}$ là chiều cao tháp, $C$ là vị trí thuyền).<br>- Góc hạ là $28^\\circ \\Rightarrow$ góc nâng $\\widehat{ACB} = 28^\\circ$ (so le trong).<br>- Trong tam giác vuông $ABC$, ta có:<br>  $BC = \\frac{AB}{\\tan \\widehat{ACB}} = \\frac{45}{\\tan 28^\\circ} \\approx \\frac{45}{0,5317} \\approx 84,6\\text{ m}$.<br>Vậy con thuyền cách chân hải đăng khoảng $84,6\\text{ m}$.<br><br>**Bài 2:**<br>a) Vì $I$ là trung điểm dây $AB$ (dây không qua tâm) nên $OI \\perp AB$ tại $I$. Do đó khoảng cách từ $O$ đến $AB$ là độ dài đoạn $OI$.<br>- Ta có: $IA = IB = \\frac{AB}{2} = 8\\text{ cm}$.<br>- Áp dụng định lý Pythagore trong $\\Delta OIA$ vuông tại $I$ ($OA = R = 10\\text{ cm}$):<br>  $OI = \\sqrt{OA^2 - IA^2} = \\sqrt{10^2 - 8^2} = \\sqrt{36} = 6\\text{ cm}$.<br><br>b) Đoạn thẳng $OI$ vuông góc với $AB$ tại trung điểm $I$ của $AB$. Do đó đường thẳng $CI$ là đường trung trực của đoạn thẳng $AB$.<br>- Vì $C$ nằm trên trung trực của $AB$ nên $CA = CB$.<br>- Do đó tam giác $ABC$ là tam giác cân tại $C$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Giúp học sinh nắm chắc các kỹ năng vẽ hình, cách lập luận không bị trừ điểm và chuẩn bị tốt cho bài kiểm tra giữa HKI.
b) Nội dung: Quy tắc trình bày bài thi hình học tự luận và hướng dẫn tự học.
c) Sản phẩm: Bản ghi nhớ quy tắc trình bày của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nhắc nhở quy tắc làm bài thi hình học:<br>  1. Vẽ hình bằng compa và thước thẳng, đánh dấu góc vuông đầy đủ.<br>  2. Nêu rõ căn cứ định lý khi áp dụng hệ thức lượng hoặc định lý đường kính - dây.<br>  3. Kiểm tra kỹ đơn vị đo và yêu cầu làm tròn của đề bài.<br>- **HS:** Ghi nhớ để tránh mất điểm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự rà soát lại các dụng cụ học tập cần mang trong buổi kiểm tra (thước, compa, máy tính).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS nêu các câu hỏi thắc mắc cuối cùng.<br><br>**+ Bước 4: Kết luận, nhận định & Dặn dò**<br>- **GV:** Dặn dò HS ôn tập kỹ theo Sơ đồ tư duy để đạt kết quả cao nhất trong tiết Kiểm tra đánh giá giữa HKI (Tiết 14). | **Dặn dò tự học tại nhà:**<br>1. Học thuộc các công thức trong Sơ đồ tư duy Mindmap.<br>2. Làm lại bài tập tính khoảng cách từ tâm đến dây trong SGK.<br>3. Chuẩn bị đầy đủ thước kẻ, compa, êke cho buổi kiểm tra giữa kì I. |
"""

with open(os.path.join(TEMP_DIR, "04_OnTapGiuaHK1_HinhHoc.md"), 'w', encoding='utf-8') as f:
    f.write(f04_content)
print(" -> Đã cập nhật chuẩn CV 5512 V2.1 + Mindmap: 04_OnTapGiuaHK1_HinhHoc.md")

# ==============================================================================
# 3. CẬP NHẬT 07_LuyenTapChung_DaiSo_Tiet29.md
# ==============================================================================
f07_content = """Tiết 29 - LUYỆN TẬP CHUNG (TRANG 52 - 53)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và hệ thống hóa các kiến thức cơ bản đã học trong Bài 7 và Bài 8:
  + Điều kiện xác định của căn thức bậc hai $\\sqrt{A}$ ($A \\ge 0$).
  + Hằng đẳng thức $\\sqrt{A^2} = |A|$ và quy tắc phá dấu giá trị tuyệt đối khi biết dấu của biểu thức.
  + Quy tắc khai căn bậc hai của một tích: $\\sqrt{A \\cdot B} = \\sqrt{A} \\cdot \\sqrt{B}$ ($A \\ge 0, B \\ge 0$).
  + Quy tắc khai căn bậc hai của một thương: $\\sqrt{\\frac{A}{B}} = \\frac{\\sqrt{A}}{\\sqrt{B}}$ ($A \\ge 0, B > 0$).
- Rèn luyện kỹ năng kết hợp nhuần nhuyễn các quy tắc biến đổi căn thức để tính nhanh giá trị biểu thức số và rút gọn biểu thức chứa biến.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác hệ thống hóa kiến thức căn bậc hai qua sơ đồ tư duy, phát hiện các sai sót thường gặp khi biến đổi căn thức.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp phân tích số dưới dấu căn thành tích các số chính phương.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Phân tích cấu trúc biểu thức để nhận diện nhân tử chung, áp dụng linh hoạt tính chất phân phối.
- Năng lực giải quyết vấn đề toán học: Vận dụng công thức căn bậc hai vào bài toán thực tiễn tính khoảng cách tầm nhìn ra đường chân trời.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng máy tính cầm tay bấm phím căn bậc hai lồng nhau, kiểm tra tính đúng đắn của kết quả rút gọn biểu thức đại số bằng cách gán giá trị biến.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***9.D1.1: HS phối hợp sử dụng trợ lý học tập AI để kiểm tra các bước trung gian của bài toán rút gọn phức tạp, đối chiếu để tìm ra lỗi sơ suất về dấu.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, tỉ mỉ trong từng bước biến đổi đại số.
- Tự tin, chủ động tìm kiếm các cách giải ngắn gọn, sáng tạo.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 1, KHBD, hình ảnh Sơ đồ tư duy Mindmap Căn bậc hai & Căn thức bậc hai, máy chiếu, bảng phụ.
2. Học sinh: SGK Toán 9, vở bài tập, máy tính cầm tay, bút dạ bảng nhóm.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Nhắc lại các công thức then chốt của Bài 7 và Bài 8 thông qua hoạt động nối cột.
b) Nội dung: Ghép mỗi vế trái ở Cột A với một vế phải tương ứng ở Cột B.
c) Sản phẩm: Kết quả nối cột chính xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu bảng nối công thức:<br>  1. $\\sqrt{A^2}$ $\\rightarrow$ ?<br>  2. $\\sqrt{A \\cdot B}$ (với $A \\ge 0, B \\ge 0$) $\\rightarrow$ ?<br>  3. $\\sqrt{\\frac{A}{B}}$ (với $A \\ge 0, B > 0$) $\\rightarrow$ ?<br>  4. $\\sqrt{A}$ có nghĩa khi nào? $\\rightarrow$ ?<br>- **HS:** Chuẩn bị trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhanh chóng ghép đôi công thức vào vở nháp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ đọc kết quả nối. Cả lớp đồng thanh xác nhận.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, nhấn mạnh điều kiện đi kèm của mỗi công thức và chuyển tiếp vào bài học. | **Bảng nối công thức:**<br>1. $\\sqrt{A^2} = |A|$.<br>2. $\\sqrt{A \\cdot B} = \\sqrt{A} \\cdot \\sqrt{B}$ ($A \\ge 0, B \\ge 0$).<br>3. $\\sqrt{\\frac{A}{B}} = \\frac{\\sqrt{A}}{\\sqrt{B}}$ ($A \\ge 0, B > 0$).<br>4. $\\sqrt{A}$ có nghĩa khi và chỉ khi $A \\ge 0$. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức bằng Sơ đồ tư duy (10 phút)
a) Mục tiêu: Tổng kết toàn diện các định lý và quy tắc biến đổi căn thức bậc hai thông qua sơ đồ tư duy trực quan; tích hợp chỉ báo AI 9.D1.1.
b) Nội dung: GV trình chiếu Sơ đồ tư duy Mindmap Căn bậc hai & Căn thức bậc hai.

![Sơ đồ tư duy Căn bậc hai và Căn thức bậc hai](khbd-ill:mindmap-07)

c) Sản phẩm: Bảng hệ thống hóa công thức căn thức trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Căn bậc hai & Căn thức bậc hai gồm 3 nhánh:<br>  1. Điều kiện xác định & Hằng đẳng thức $\\sqrt{A^2} = |A|$.<br>  2. Nhân & Chia căn bậc hai (khai phương tích, khai phương thương).<br>  3. Rút gọn biểu thức chứa biến & Vận dụng thực tế.<br>- Yêu cầu HS thảo luận cặp đôi để tóm tắt các quy tắc cốt lõi.<br>- ***Tích hợp AI (9.D1.1): GV chiếu lời giải thử của AI cho Bài 3.15 và đặt câu hỏi cho học sinh: "AI phá dấu giá trị tuyệt đối như thế nào khi biết $3 \\le x \\le 5$?". HS đối chiếu với quy tắc phá dấu trên sơ đồ tư duy.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát sơ đồ tư duy, thảo luận cặp đôi và ghi chép nhanh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS thuyết minh lại các quy tắc biến đổi.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc và chuyển sang luyện giải bài tập rèn kỹ năng. | **Hệ thống kiến thức căn thức (Mindmap):**<br>- $\\sqrt{A}$ xác định $\\Leftrightarrow A \\ge 0$.<br>- Hằng đẳng thức: $\\sqrt{A^2} = |A| = \\begin{cases} A & \\text{khi } A \\ge 0 \\\\ -A & \\text{khi } A < 0 \\end{cases}$<br>- Tích: $\\sqrt{a \\cdot b} = \\sqrt{a} \\cdot \\sqrt{b}$ ($a, b \\ge 0$).<br>- Thương: $\\sqrt{\\frac{a}{b}} = \\frac{\\sqrt{a}}{\\sqrt{b}}$ ($a \\ge 0, b > 0$).<br>- Đưa thừa số ra ngoài căn: $\\sqrt{A^2 B} = |A|\\sqrt{B}$ ($B \\ge 0$). |

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)
a) Mục tiêu: Rèn luyện kỹ năng tính giá trị biểu thức số, tìm ĐKXĐ và rút gọn biểu thức chứa biến; tích hợp chỉ báo NLS 5.2.TC2b.
b) Nội dung: Giải Bài 3.12, Bài 3.13 và Bài 3.15 (SGK trang 52).
c) Sản phẩm: Lời giải hoàn chỉnh các bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập lên bảng:<br>  **Bài 3.12:** Tính giá trị: $A = \\sqrt{2,5} \\cdot \\sqrt{14,4}$; $B = \\frac{\\sqrt{72}}{\\sqrt{2}} - \\sqrt{\\frac{48}{3}}$.<br>  **Bài 3.13:** Tìm ĐKXĐ của $\\sqrt{3x - 6}$ và $\\sqrt{\\frac{5}{2x + 4}}$.<br>  **Bài 3.15:** Cho $M = \\sqrt{(x - 3)^2} + \\sqrt{(x - 5)^2}$ với $3 \\le x \\le 5$. Rút gọn $M$.<br>- ***Tích hợp NLS (5.2.TC2b): HS sử dụng máy tính cầm tay bấm kiểm tra kết quả tính nhẩm biểu thức A, B.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cá nhân làm bài vào vở. Ba HS lên bảng thực hiện.<br>- **GV:** Quan sát, lưu ý học sinh quy tắc phá dấu giá trị tuyệt đối theo khoảng giá trị của biến.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS trên bảng trình bày. Lớp nhận xét các cách tính nhẩm thông minh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa lời giải từng bài. | **Bài 3.12 (SGK trang 52):**<br>a) $A = \\sqrt{2,5 \\cdot 14,4} = \\sqrt{25 \\cdot 1,44} = 5 \\cdot 1,2 = 6$.<br>b) $B = \\sqrt{\\frac{72}{2}} - \\sqrt{\\frac{48}{3}} = \\sqrt{36} - \\sqrt{16} = 6 - 4 = 2$.<br><br>**Bài 3.13 (SGK trang 52):**<br>a) $\\sqrt{3x - 6}$ xác định khi $3x - 6 \\ge 0 \\Rightarrow x \\ge 2$.<br>b) $\\sqrt{\\frac{5}{2x + 4}}$ xác định khi $2x + 4 > 0 \\Rightarrow x > -2$ (vì tử $5 > 0$).<br><br>**Bài 3.15 (SGK trang 52):**<br>$M = |x - 3| + |x - 5|$.<br>Vì $3 \\le x \\le 5$ nên:<br>- $x \\ge 3 \\Rightarrow x - 3 \\ge 0 \\Rightarrow |x - 3| = x - 3$.<br>- $x \\le 5 \\Rightarrow x - 5 \\le 0 \\Rightarrow |x - 5| = 5 - x$.<br>Suy ra: $M = (x - 3) + (5 - x) = 2$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng công thức căn bậc hai vào bài toán thực tiễn tính khoảng cách tầm nhìn đến đường chân trời.
b) Nội dung: Giải Bài 3.16 SGK trang 53 (Tính tầm nhìn xa từ tầng quan sát của tòa tháp Landmark). Dặn dò tự học.
c) Sản phẩm: Lời giải Bài 3.16 trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế (Bài 3.16 SGK trang 53): Khoảng cách tầm nhìn xa $d$ (km) đến đường chân trời của một người ở độ cao $h$ (m) được ước tính theo công thức: $d \\approx 3,57 \\sqrt{h}$.<br>  Hỏi một người đứng ở đài quan sát cao $h = 361\\text{ m}$ thì có thể nhìn xa đến đường chân trời một khoảng bao nhiêu kilômét?<br>- **HS:** Nhận nhiệm vụ, áp dụng công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thay $h = 361$ vào công thức: $d \\approx 3,57 \\cdot \\sqrt{361} = 3,57 \\cdot 19 = 67,83\\text{ km}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đọc to kết quả, lớp kiểm tra bằng máy tính bỏ túi.<br><br>**+ Bước 4: Kết luận, nhận định & Dặn dò**<br>- **GV:** Đánh giá cao việc ứng dụng công thức căn bậc hai vào khoa học đời sống. | **Bài 3.16 (SGK trang 53):**<br>- Khoảng cách tầm nhìn xa đến đường chân trời:<br>  $$d \\approx 3,57 \\sqrt{h} = 3,57 \\cdot \\sqrt{361} = 3,57 \\times 19 = 67,83\\text{ km}$$<br>Vậy người đó có thể nhìn xa khoảng $67,83\\text{ km}$.<br><br>**Dặn dò tự học tại nhà:**<br>1. Ôn lại toàn bộ các phương pháp khai căn trong Sơ đồ tư duy.<br>2. Làm bài tập 3.14 SGK trang 52.<br>3. Đọc trước Bài 9: Biến đổi đơn giản và rút gọn biểu thức chứa căn thức bậc hai. |
"""

with open(os.path.join(TEMP_DIR, "07_LuyenTapChung_DaiSo_Tiet29.md"), 'w', encoding='utf-8') as f:
    f.write(f07_content)
print(" -> Đã cập nhật chuẩn CV 5512 V2.1 + Mindmap: 07_LuyenTapChung_DaiSo_Tiet29.md")

# ==============================================================================
# 4. CẬP NHẬT 09_LuyenTapChung_HinhHoc_Tiet17.md (NLS 3.1.TC2a)
# ==============================================================================
f09_content = """Tiết 17 - LUYỆN TẬP CHUNG (TRANG 96 - 98)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và khắc sâu toàn bộ kiến thức trọng tâm của Chương V đã học trong Bài 13, 14 và 15:
  + Khái niệm đường tròn, tính chất đối xứng của đường tròn (tâm đối xứng, trục đối xứng).
  + Góc ở tâm, số đo cung tròn, mối liên hệ giữa cung và dây trong một đường tròn.
  + Tính chất đường kính vuông góc với dây thì đi qua trung điểm của dây và đi qua điểm chính giữa của cung bị chắn; định lý đảo đi qua trung điểm của dây không đi qua tâm.
  + Các công thức tính toán: Chu vi đường tròn $C = 2\\pi R = \\pi d$; Độ dài cung tròn $l = \\frac{\\pi R n}{180}$; Diện tích hình tròn $S = \\pi R^2$; Diện tích hình quạt tròn $S_q = \\frac{\\pi R^2 n}{360} = \\frac{l R}{2}$; Diện tích hình vành khuyên $S_{vk} = \\pi (R_1^2 - R_2^2)$.
- Vận dụng linh hoạt các công thức và định lý để giải quyết các bài toán hình học tính toán và chứng minh tổng hợp.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác tổng kết hệ thống kiến thức chương đường tròn dưới dạng sơ đồ số trực quan.
- Giao tiếp và hợp tác: Tự tin thuyết trình sản phẩm số của nhóm, lắng nghe và phản biện ý kiến chuyên môn của bạn học.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Suy luận logic kết hợp tính chất đường kính vuông góc với dây và định lý Pythagore để tính bán kính hoặc khoảng cách.
- Năng lực mô hình hóa toán học: Chuyển đổi các bài toán thực tiễn đời sống liên quan đến hình tròn, hình quạt và vành khuyên thành bài toán hình học chuẩn tắc.

c) Năng lực số (NLS):
- ***3.1.TC2a: HS sử dụng công cụ số (phần mềm thiết kế đồ họa Canva, sơ đồ tư duy Mindmap, PowerPoint hoặc GeoGebra) để tạo lập một sản phẩm nội dung số (Infographic/Sơ đồ tư duy) tổng hợp toàn bộ các định lý, công thức tính toán của Chương V: Đường tròn.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***9.D1.1: HS ứng dụng trợ lý học tập AI để hỗ trợ lên dàn ý cấu trúc các nhánh nội dung chính của sơ đồ tư duy và tra cứu gợi ý các ứng dụng thực tế phong phú của hình tròn.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác trong vẽ hình và trình bày suy luận hình học.
- Nâng cao tính thẩm mỹ và niềm đam mê sáng tạo nội dung số trong học tập Toán học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 1, KHBD, hình ảnh Sơ đồ tư duy Mindmap Chương V: Đường tròn, máy tính kết nối màn hình tương tác/tivi, thước thẳng, compa bảng.
2. Học sinh: SGK Toán 9, vở ghi, compa, thước kẻ, máy tính cầm tay, sản phẩm sơ đồ tư duy số của nhóm.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt không khí học tập sôi nổi qua việc ôn lại các công thức tính chu vi, diện tích và độ dài cung tròn.
b) Nội dung: Trả lời 4 câu hỏi trắc nghiệm phản xạ nhanh chiếu trên màn hình.
c) Sản phẩm: Bảng chọn đáp án của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu 4 câu hỏi trắc nghiệm nhanh:<br>  1. Công thức tính độ dài cung $n^\\circ$ của đường tròn bán kính $R$ là gì?<br>  2. Công thức tính diện tích hình quạt tròn bán kính $R$, cung $n^\\circ$ là gì?<br>  3. Diện tích hình vành khuyên giới hạn bởi hai đường tròn đồng tâm bán kính $R_1 > R_2$ là gì?<br>  4. Trong một đường tròn, hai dây bằng nhau căng hai cung như thế nào?<br>- **HS:** Chuẩn bị bảng con để giơ đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ bảng đáp án ngay khi có hiệu lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS đứng tại chỗ giải thích nhanh công thức.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ phản xạ và dẫn dắt vào bài học ôn tập. | **Ghi nhớ nhanh:**<br>1. $l = \\frac{\\pi R n}{180}$.<br>2. $S_q = \\frac{\\pi R^2 n}{360} = \\frac{l R}{2}$.<br>3. $S_{vk} = \\pi (R_1^2 - R_2^2)$.<br>4. Hai cung bằng nhau căng hai dây bằng nhau. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức bằng Sơ đồ tư duy (10 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ các định lý, công thức tính toán và ứng dụng thực tiễn của Chương V Đường tròn qua Sơ đồ tư duy số; tích hợp chỉ báo NLS 3.1.TC2a và AI 9.D1.1.
b) Nội dung: GV và HS trình chiếu, phân tích Sơ đồ tư duy số tổng kết Chương V: Đường tròn.

![Sơ đồ tư duy Chương V: Đường tròn](khbd-ill:mindmap-09)

c) Sản phẩm: Sản phẩm sơ đồ tư duy số của nhóm học sinh và bảng công thức trong vở ghi.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Chương V: Đường tròn gồm 3 nhánh lớn:<br>  1. Góc ở tâm - Cung và Dây.<br>  2. Ứng dụng thực tế & Dự án STEM (Chế tạo quạt giấy, sân vận động, cần cẩu).<br>  3. Bộ 5 công thức tính toán ($C, l, S, S_q, S_{vk}$).<br>- Mời đại diện nhóm HS thuyết minh sản phẩm số được thiết kế theo chỉ báo ***NLS 3.1.TC2a***.<br>- ***Tích hợp AI (9.D1.1): GV cho học sinh quan sát bảng đối chiếu do AI gợi ý về cách lựa chọn công thức tính $S_q$: nếu đề bài cho số đo góc $n^\\circ$ thì dùng $S_q = \\frac{\\pi R^2 n}{360}$, nếu đề bài cho độ dài cung $l$ thì dùng ngay $S_q = \\frac{l R}{2}$.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đại diện nhóm lên thuyết trình sơ đồ tư duy (2 phút). Cả lớp lắng nghe, ghi chép vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các bạn trong lớp quan sát, nhận xét tính thẩm mỹ, độ chuẩn xác toán học của sơ đồ tư duy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chấm điểm sản phẩm số của nhóm theo Rubric và chuyển sang luyện giải bài tập. | **Hệ thống kiến thức Chương V (Mindmap - NLS 3.1.TC2a):**<br>1. **Góc ở tâm & Cung:**<br>  $\\text{sđ }\\wideparen{AB} = \\widehat{AOB}$ (cung nhỏ); Cung lớn $= 360^\\circ - \\text{sđ }\\wideparen{AB nhỏ}$.<br>2. **Cung và dây:**<br>  $\\wideparen{AB} = \\wideparen{CD} \\Leftrightarrow AB = CD$.<br>  Đường kính vuông góc với dây thì đi qua trung điểm của dây.<br>3. **Bộ công thức:**<br>  $C = 2\\pi R = \\pi d$; $l = \\frac{\\pi R n}{180}$;<br>  $S = \\pi R^2$; $S_q = \\frac{\\pi R^2 n}{360} = \\frac{l R}{2}$;<br>  $S_{vk} = \\pi (R_1^2 - R_2^2)$. |

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)
a) Mục tiêu: Rèn luyện kỹ năng tính độ dài cung tròn, diện tích hình quạt, hình vành khuyên và bài toán khoảng cách giữa hai dây song song; tích hợp chỉ báo NLS 5.2.TC2b.
b) Nội dung: Giải Bài 5.8, Bài 5.9 và Bài 5.10 (SGK trang 96 - 97).
c) Sản phẩm: Lời giải hoàn chỉnh các bài tập trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập lên bảng:<br>  **Bài 5.8:** Một hình quạt tròn có $R = 12\\text{ cm}$ và độ dài cung $l = 4\\pi\\text{ cm}$. Tính số đo độ của cung và diện tích hình quạt.<br>  **Bài 5.9:** Tính diện tích hình vành khuyên giới hạn bởi hai đường tròn đồng tâm có $R_1 = 8\\text{ cm}$ và $R_2 = 5\\text{ cm}$.<br>  **Bài 5.10:** Cho $(O; R = 6\\text{ cm})$. Hai dây $AB = 8\\text{ cm}$ và $CD = 10\\text{ cm}$ song song với nhau và nằm về hai phía đối với tâm $O$. Tính khoảng cách giữa hai dây $AB$ và $CD$.<br>- ***Tích hợp NLS (5.2.TC2b): HS sử dụng máy tính cầm tay bấm phím pi để tính giá trị diện tích làm tròn số thập phân.***<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Cá nhân làm bài vào vở. Ba HS lên bảng thực hiện.<br>- **GV:** Quan sát, hướng dẫn học sinh áp dụng công thức $S_q = \\frac{l R}{2}$ và định lý Pythagore trong Bài 5.10.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS trên bảng trình bày. Lớp nhận xét bài bạn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa lời giải và thang điểm từng bài. | **Bài 5.8 (SGK trang 96):**<br>a) Từ $l = \\frac{\\pi R n}{180} \\Rightarrow n = \\frac{180 \\cdot l}{\\pi R} = \\frac{180 \\cdot 4\\pi}{\\pi \\cdot 12} = 60^\\circ$.<br>b) Diện tích hình quạt tròn:<br>  $S_q = \\frac{l \\cdot R}{2} = \\frac{4\\pi \\cdot 12}{2} = 24\\pi \\approx 75,40\\text{ cm}^2$.<br><br>**Bài 5.9 (SGK trang 96):**<br>Diện tích hình vành khuyên:<br>$$S_{vk} = \\pi (R_1^2 - R_2^2) = \\pi (8^2 - 5^2) = 39\\pi \\approx 122,52\\text{ cm}^2$$<br><br>**Bài 5.10 (SGK trang 97):**<br>- Kẻ $OH \\perp AB$ tại $H$ và $OK \\perp CD$ tại $K$. Vì $AB \\parallel CD$ nên $H, O, K$ thẳng hàng.<br>- Vì hai dây nằm về hai phía đối với $O$ nên khoảng cách giữa hai dây là $HK = OH + OK$.<br>- Ta có: $AH = \\frac{AB}{2} = 4\\text{ cm} \\Rightarrow OH = \\sqrt{6^2 - 4^2} = \\sqrt{20} = 2\\sqrt{5}\\text{ cm}$.<br>- Ta có: $CK = \\frac{CD}{2} = 5\\text{ cm} \\Rightarrow OK = \\sqrt{6^2 - 5^2} = \\sqrt{11}\\text{ cm}$.<br>- Vậy khoảng cách giữa hai dây là: $HK = 2\\sqrt{5} + \\sqrt{11} \\approx 7,79\\text{ cm}$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức đường tròn vào giải bài toán thực tế về bán kính quay của cần cẩu xây dựng.
b) Nội dung: Bài toán tính diện tích mặt bằng thi công trong tầm quét của cần cẩu hình quạt tròn. Hướng dẫn tự học.
c) Sản phẩm: Lời giải bài toán thực tế và kế hoạch học tập ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế: Một cần cẩu tháp xây dựng có tầm với cánh tay đòn là $R = 40\\text{ m}$. Cần cẩu quay một góc tối đa là $270^\\circ$. Hỏi diện tích mặt bằng mà cần cẩu này có thể phục vụ vận chuyển vật liệu là bao nhiêu mét vuông?<br>- **HS:** Nhận nhiệm vụ, áp dụng công thức tính diện tích hình quạt tròn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính toán: $S = \\frac{\\pi \\cdot 40^2 \\cdot 270}{360} = 1200\\pi \\approx 3769,91\\text{ m}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS phát biểu kết quả, lớp đồng tình.<br><br>**+ Bước 4: Kết luận, nhận định & Dặn dò**<br>- **GV:** Đánh giá tiết học tích cực, biểu dương tinh thần tự học số của lớp. | **Bài toán tầm quét của cần cẩu:**<br>- Diện tích mặt bằng phục vụ:<br>  $$S = \\frac{\\pi R^2 n}{360} = \\frac{\\pi \\cdot 40^2 \\cdot 270}{360} = 1200\\pi \\approx 3770\\text{ m}^2$$<br><br>**Dặn dò tự học tại nhà:**<br>1. Lưu các sản phẩm số Infographic lên nhóm học tập chung.<br>2. Hoàn thiện bài tập 5.11 SGK trang 98.<br>3. Chuẩn bị thước kẻ, compa cho Bài 16: Vị trí tương đối của đường thẳng và đường tròn. |
"""

with open(os.path.join(TEMP_DIR, "09_LuyenTapChung_HinhHoc_Tiet17.md"), 'w', encoding='utf-8') as f:
    f.write(f09_content)
print(" -> Đã cập nhật chuẩn CV 5512 V2.1 + Mindmap: 09_LuyenTapChung_HinhHoc_Tiet17.md")

print(">>> ĐÃ CẬP NHẬT HOÀN TẤT CẢ 4 FILE TIẾT ÔN TẬP & LUYỆN TẬP! <<<")
