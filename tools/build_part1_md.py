# -*- coding: utf-8 -*-
"""
Tạo toàn bộ 8 file Markdown KHBD Toán 6 KNTT chuẩn CV 5512 V2.0
"""
import os

OUT_DIR = os.path.abspath(r"TROLYTHIEN\1_SOAN_KHBD\Ket_qua")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. BÀI 1
MD_01 = """# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 6**  
**CHỦ ĐỀ: BÀI 7. THỨ TỰ THỰC HIỆN CÁC PHÉP TÍNH (TIẾT 12: LUYỆN TẬP CHUNG)**  
**Phân phối chương trình:** Tiết 12 — Tuần 4  
**Thời lượng thực hiện:** 01 tiết (45 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 27)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Củng cố và hệ thống hóa quy tắc về thứ tự thực hiện các phép tính trong tập hợp các số tự nhiên (biểu thức không có dấu ngoặc và biểu thức có các dấu ngoặc).
- Rèn luyện kỹ năng thực hiện thành thạo các phép tính cộng, trừ, nhân, chia và nâng lên lũy thừa; nhận biết và tính toán hợp lý giá trị của biểu thức số.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự giác hệ thống hóa quy tắc thực hiện phép tính, độc lập thực hiện các phép tính và bài toán có lời văn.
- Giao tiếp và hợp tác: Tương tác tích cực với bạn học, thảo luận nhóm để tìm ra thứ tự tính toán tối ưu và đối chiếu kết quả.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: Nhận biết cấu trúc của biểu thức, phân tích mức độ ưu tiên giữa các phép toán để thực hiện đúng từng bước.
- Giải quyết vấn đề toán học: Vận dụng quy tắc thứ tự tính toán để giải các bài toán thực tế (tính diện tích, thể tích hình khối).

## 3. Về phẩm chất
- Chăm chỉ: Cẩn thận, tỉ mỉ trong từng bước tính toán, không bỏ sót ngoặc và không làm tắt khi chưa thành thạo.
- Trách nhiệm: Tự giác kiểm tra lại kết quả bài làm trước khi báo cáo.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài trình chiếu PowerPoint, tivi/máy chiếu, phiếu học tập nhóm, thước kẻ, mô hình/hình ảnh khối lập phương ghép.
2. **Học sinh:** SGK Toán 6 (Tập 1), vở ghi, đồ dùng học tập: bút, thước kẻ, nháp, máy tính cầm tay để kiểm chứng.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)

#### a) Mục tiêu:
- Tái hiện quy tắc thứ tự thực hiện các phép tính; tạo hứng thú và tâm thế chủ động trước khi luyện tập.

#### b) Nội dung:
- Trả lời nhanh câu hỏi nhắc lại quy tắc thứ tự ưu tiên các phép tính.

#### c) Sản phẩm:
- Câu trả lời của HS về thứ tự: Lũy thừa -> Nhân, chia -> Cộng, trừ; Ngoặc tròn () -> Ngoặc vuông [] -> Ngoặc nhọn {}.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu câu hỏi: "Khi thực hiện phép tính trong một biểu thức chứa nhiều phép toán và các dấu ngoặc, ta cần tuân theo thứ tự ưu tiên nào?"<br>- **HS:** Tiếp nhận nhiệm vụ, chuẩn bị trả lời miệng.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhớ lại kiến thức Bài 7, giơ tay phát biểu.<br>- **GV:** Quan sát và gọi 1 học sinh trả lời.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** "Thưa thầy/cô: Với biểu thức không có ngoặc: Lũy thừa -> Nhân và chia -> Cộng và trừ (từ trái sang phải). Với biểu thức có ngoặc: trong ngoặc tròn () -> trong ngoặc vuông [] -> trong ngoặc nhọn {}."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khen ngợi câu trả lời chuẩn xác và dẫn dắt vào bài luyện tập.<br>- **HS:** Lắng nghe và mở SGK trang 27. | **QUY TẮC THỨ TỰ PHÉP TÍNH:**<br><br>1. **Biểu thức không có dấu ngoặc:**<br>$$\\text{Lũy thừa} \\rightarrow \\text{Nhân và chia} \\rightarrow \\text{Cộng và trừ}$$<br>*(Nếu chỉ có cộng, trừ hoặc chỉ có nhân, chia thì thực hiện từ trái sang phải).*<br><br>2. **Biểu thức có dấu ngoặc:**<br>$$( \\ ) \\rightarrow [ \\ ] \\rightarrow \\{ \\ \}$$ |

---

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức (10 phút)

#### a) Mục tiêu:
- Hệ thống hóa toàn bộ các dạng bài tính toán qua Sơ đồ tư duy trực quan và phân tích kỹ các bước giải mẫu trong Ví dụ 1, Ví dụ 2.

#### b) Nội dung:
- Phân tích cách giải Ví dụ 1 SGK trang 27.

#### c) Sản phẩm:
- Vở ghi bài tóm tắt các bước giải Ví dụ 1: $120 + [55 - (11 - 3 \\cdot 2)^2] + 2^3 = 158$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu Ví dụ 1 và yêu cầu HS phân tích các bước biến đổi: "Quan sát Ví dụ 1, hãy nêu thứ tự từng bước tính đã được thực hiện."<br>- **HS:** Quan sát bảng phụ/màn hình chiếu, thảo luận cặp đôi 1 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Xác định: bước 1 tính trong ngoặc tròn (nhân trước, trừ sau) -> bước 2 tính lũy thừa -> bước 3 tính trong ngoặc vuông -> bước 4 tính lũy thừa ngoài -> bước 5 thực hiện phép cộng từ trái sang phải.<br>- **GV:** Hướng dẫn học sinh chú ý không bỏ sót số hạng ngoài ngoặc.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện một cặp đôi trình bày lại các bước giải chi tiết.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chốt lại phương pháp: Luôn nhận diện cấu trúc ngoặc trước khi bấm bút tính. | **PHÂN TÍCH VÍ DỤ 1 (SGK TRANG 27):**<br><br>Tính: $A = 120 + [55 - (11 - 3 \\cdot 2)^2] + 2^3$<br><br>- Trong ngoặc (): $11 - 3 \\cdot 2 = 11 - 6 = 5$.<br>- Trong ngoặc []: $55 - 5^2 = 55 - 25 = 30$.<br>- Tính lũy thừa: $2^3 = 8$.<br>- Biểu thức trở thành: $120 + 30 + 8 = 150 + 8 = 158$.<br><br>**Lưu ý sư phạm:** Giữ nguyên các số hạng chưa tính theo đúng trật tự từ trái sang phải. |

---

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)

#### a) Mục tiêu:
- Giải quyết bài tập trọng tâm: Bài 1.50 (tính giá trị biểu thức cơ bản), Bài 1.51 (lũy thừa), Bài 1.53 (biểu thức phối hợp nhiều phép toán).

#### b) Nội dung:
- Cá nhân làm Bài 1.50 và Bài 1.51 vào vở; hoạt động nhóm thực hiện Bài 1.53.

#### c) Sản phẩm:
- Lời giải chính xác của Bài 1.50, Bài 1.51 và Bài 1.53 trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao nhiệm vụ:<br>1. Dãy 1, 2: Hoàn thành Bài 1.50 (a, b, c).<br>2. Dãy 3, 4: Hoàn thành Bài 1.51 (a, b, c, d).<br>3. Toàn lớp cùng làm Bài 1.53 (a, b).<br>- **HS:** Mở vở bài tập, làm việc cá nhân trong 5 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tự giác làm bài, kiểm tra từng bước tính lũy thừa và nhân chia.<br>- **GV:** Đi quan sát, hỗ trợ các em học sinh tính còn chậm.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Gọi 3 HS lên bảng chữa Bài 1.50; 2 HS chữa Bài 1.51; 2 HS chữa Bài 1.53.<br>- **HS:** Dưới lớp nhận xét, so sánh với bài làm của mình.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chuẩn hóa lời giải và lưu ý lỗi sai phổ biến: tính nhân chia trước cộng trừ nhưng nhầm lẫn thứ tự ngoặc. | **GIẢI BÀI TẬP TRỌNG TÂM:**<br><br>1. **Bài 1.50:**<br>a) $36 - 18 : 6 = 36 - 3 = 33$.<br>b) $2 \\cdot 3^2 + 24 : 6 \\cdot 2 = 2 \\cdot 9 + 4 \\cdot 2 = 18 + 8 = 26$.<br>c) $2 \\cdot 3^2 - 24 : (6 \\cdot 2) = 2 \\cdot 9 - 24 : 12 = 18 - 2 = 16$.<br><br>2. **Bài 1.51:**<br>a) $3^3 : 3^2 = 3^{3-2} = 3^1 = 3$.<br>b) $5^4 : 5^2 = 5^{4-2} = 5^2$.<br>c) $8^3 \\cdot 8^2 = 8^{3+2} = 8^5$.<br>d) $5^4 \\cdot 5^3 : 5^2 = 5^{4+3-2} = 5^5$.<br><br>3. **Bài 1.53:**<br>a) $110 - 7^2 + 22 : 2 = 110 - 49 + 11 = 61 + 11 = 72$.<br>b) $9 \\cdot (8^2 - 15) = 9 \\cdot (64 - 15) = 9 \\cdot 49 = 441$. |

---

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)

#### a) Mục tiêu:
- Vận dụng biểu thức toán học giải quyết bài toán thực tế (Bài 1.52: diện tích hình hộp chữ nhật).
- Định hướng tự học tại nhà.

#### b) Nội dung:
- Phân tích và thiết lập biểu thức tính diện tích toàn phần hình hộp chữ nhật có kích thước $a, b, c$.

#### c) Sản phẩm:
- Biểu thức $S_{tp} = 2 \\cdot (a \\cdot b + b \\cdot c + c \\cdot a)$; kết quả số đo diện tích khi $a = 5, b = 4, c = 3$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Yêu cầu HS đọc đề Bài 1.52 SGK trang 27:<br>"Hãy viết biểu thức tính diện tích toàn phần của hình hộp chữ nhật có độ dài các cạnh là $a, b, c$. Sau đó tính giá trị của biểu thức khi $a = 5\\text{ cm}, b = 4\\text{ cm}, c = 3\\text{ cm}$."<br>- **HS:** Đọc đề và suy nghĩ cách giải.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhớ lại diện tích 6 mặt của hình hộp chữ nhật gồm 3 cặp mặt bằng nhau.<br>- **GV:** Gợi ý cách viết biểu thức thu gọn có dấu ngoặc.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày biểu thức và kết quả tính: $S = 2 \\cdot (5 \\cdot 4 + 4 \\cdot 3 + 3 \\cdot 5) = 2 \\cdot (20 + 12 + 15) = 2 \\cdot 47 = 94\\text{ (cm}^2\\text{)}$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Đánh giá kết quả, dặn dò học sinh về nhà xem lại toàn bộ lý thuyết Chương I để chuẩn bị tiết sau làm bài tập cuối chương. | **BÀI 1.52 (VẬN DỤNG THỰC TẾ):**<br><br>- Biểu thức tính diện tích toàn phần hình hộp chữ nhật:<br>$$S_{tp} = 2 \\cdot (a \\cdot b + b \\cdot c + c \\cdot a)$$<br>- Thay $a = 5\\text{ cm}, b = 4\\text{ cm}, c = 3\\text{ cm}$, ta có:<br>$$S_{tp} = 2 \\cdot (5 \\cdot 4 + 4 \\cdot 3 + 3 \\cdot 5) = 2 \\cdot (20 + 12 + 15) = 2 \\cdot 47 = 94\\text{ (cm}^2\\text{)}$$<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Làm tiếp các câu còn lại của Bài 1.53 SGK.<br>- Ôn tập toàn bộ lý thuyết Chương I: Tập hợp, các phép toán trên $\\mathbb{N}$, lũy thừa và thứ tự thực hiện phép tính. |
"""

# 2. BÀI 2
MD_02 = """# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 6**  
**CHỦ ĐỀ: BÀI TẬP CUỐI CHƯƠNG I (TIẾT 13: ÔN TẬP VÀ GIẢI BÀI TẬP)**  
**Phân phối chương trình:** Tiết 13 — Tuần 5  
**Thời lượng thực hiện:** 01 tiết (45 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 28)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Ôn tập, củng cố và hệ thống hóa toàn bộ các kiến thức cốt lõi của Chương I: tập hợp các số tự nhiên, các phép tính cộng, trừ, nhân, chia, lũy thừa và thứ tự thực hiện phép tính.
- Vận dụng thành thạo kiến thức đã học để giải các bài toán tính giá trị biểu thức và các bài toán thực tiễn tổng hợp.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự tổng hợp kiến thức qua sơ đồ tư duy, tự giác hoàn thành các bài tập ôn tập cuối chương.
- Giao tiếp và hợp tác: Tích cực trao đổi, phản biện trong hoạt động nhóm khi giải bài toán thực tế.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: Phân tích các mối quan hệ số học, giải thích tính đúng đắn của lời giải toán thực tế có dư.
- Mô hình hóa toán học: Chuyển đổi các bài toán thực tế (thuê xe ô tô, tính tiền bán vé) thành biểu thức toán học tương ứng.

## 3. Về phẩm chất
- Chăm chỉ: Nghiêm túc rà soát lại các dạng bài tập, rèn tính cẩn thận trong tính toán số lớn.
- Trách nhiệm: Ý thức cao trong làm việc nhóm và chuẩn bị chuyển tiếp sang kiến thức Chương II.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài giảng điện tử PowerPoint, phiếu học tập tổng hợp Chương I, bảng phụ ghi đề bài toán thực tế.
2. **Học sinh:** SGK Toán 6 (Tập 1), vở ghi bài, đồ dùng học tập, máy tính cầm tay để kiểm chứng kết quả.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)

#### a) Mục tiêu:
- Tái hiện tổng quan bức tranh kiến thức Chương I; kích thích tinh thần ôn tập qua mini-quiz trắc nghiệm.

#### b) Nội dung:
- Trả lời nhanh các câu hỏi ôn tập cấu tạo số tự nhiên, quan hệ số liền trước, liền sau.

#### c) Sản phẩm:
- Câu trả lời của HS về số tự nhiên, tính chất số 0, số liền trước và liền sau.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu câu hỏi nhanh: "1. Số tự nhiên nào không có số liền trước? 2. Mọi số tự nhiên đều có số liền sau đúng hay sai?"<br>- **HS:** Lắng nghe và suy nghĩ trong 30 giây.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhớ lại kiến thức tập hợp $\\mathbb{N}$.<br>- **GV:** Chỉ định 1 HS trả lời.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** "Thưa thầy/cô: Số 0 là số tự nhiên nhỏ nhất và không có số liền trước trong $\\mathbb{N}$. Mọi số tự nhiên đều có số liền sau duy nhất."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chốt lại tính chất và dẫn dắt vào tiết ôn tập cuối chương I. | **TỔNG QUAN CHƯƠNG I:**<br><br>- Tập hợp số tự nhiên: $\\mathbb{N} = \\{0; 1; 2; 3; ...\\}$; $\\mathbb{N}^* = \\{1; 2; 3; ...\\}$.<br>- Số 0 không có số liền trước trong $\\mathbb{N}$.<br>- Hai số tự nhiên liên tiếp hơn kém nhau 1 đơn vị. |

---

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức Chương I (10 phút)

#### a) Mục tiêu:
- Hệ thống hóa các kiến thức Chương I qua Sơ đồ tư duy liên hoàn: Tập hợp -> Phép tính -> Lũy thừa -> Thứ tự tính toán.

#### b) Nội dung:
- Quan sát và hoàn thiện sơ đồ tư duy tóm tắt Chương I; phân tích cấu trúc số trong Bài 1.54, 1.55.

#### c) Sản phẩm:
- Sơ đồ tư duy trong vở; câu trả lời Bài 1.54, 1.55.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu sơ đồ tư duy tóm tắt 3 nhánh: (1) Tập hợp số tự nhiên; (2) Phép toán cộng trừ nhân chia lũy thừa; (3) Thứ tự phép tính. Yêu cầu HS hoàn thành Bài 1.54 SGK.<br>- **HS:** Quan sát và thực hiện Bài 1.54 vào vở.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Viết số theo đúng từng lớp: lớp tỉ, lớp triệu, lớp nghìn, lớp đơn vị.<br>- **GV:** Quan sát, nhắc nhở cách viết cách cụm 3 chữ số.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện đọc số: $a = 15\\ 267\\ 021\\ 908$.<br>a) Số $a$ có 11 chữ số. Tập hợp các chữ số của $a$: $\\{0; 1; 2; 5; 6; 7; 8; 9\\}$.<br>b) Chữ số hàng triệu là chữ số 7.<br>c) Có hai chữ số 1: chữ số 1 thứ nhất ở hàng chục tỉ (giá trị $10\\ 000\\ 000\\ 000$), chữ số 1 thứ hai ở hàng nghìn (giá trị $1\\ 000$).<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa câu trả lời và nhấn mạnh ý nghĩa giá trị vị trí của chữ số trong hệ thập phân. | **BÀI 1.54 (SGK TRANG 28):**<br><br>Số tự nhiên $a = 15\\ 267\\ 021\\ 908$.<br><br>a) Số $a$ có 11 chữ số.<br>Tập hợp các chữ số là: $\\{0; 1; 2; 5; 6; 7; 8; 9\\}$.<br><br>b) Chữ số hàng triệu là chữ số 7.<br><br>c) Hai chữ số 1 nằm ở:<br>- Hàng chục tỉ: có giá trị $10\\ 000\\ 000\\ 000$.<br>- Hàng nghìn: có giá trị $1\\ 000$. |

---

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)

#### a) Mục tiêu:
- Giải quyết bài tập tính toán phức tạp (Bài 1.57) và bài toán thực tế có dư (Bài 1.58).

#### b) Nội dung:
- Nhóm 1, 2: Thực hiện Bài 1.57.<br>- Nhóm 3, 4: Phân tích và giải Bài 1.58.

#### c) Sản phẩm:
- Kết quả Bài 1.57: $21 \\cdot [(2232 : 8) - 180] + 21 = 2100$.<br>- Kết quả Bài 1.58: Cần ít nhất 8 xe ô tô 45 chỗ.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Phân công 2 nhiệm vụ rõ ràng:<br>1. Bài 1.57: Tính giá trị biểu thức: $B = 21 \\cdot [(1245 + 987) : 2^3 - 15 \\cdot 12] + 21$.<br>2. Bài 1.58: Khối 6 có 320 học sinh đi tham quan. Cần thuê ít nhất bao nhiêu xe ô tô 45 chỗ để đủ chỗ cho tất cả học sinh?<br>- **HS:** Làm việc nhóm 4 người trong 5 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thảo luận, tính nhẩm và kiểm tra phép chia có dư.<br>- **GV:** Hướng dẫn nhóm giải thích tại sao phép chia có dư cần cộng thêm 1 xe.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS nhóm 1:** Lên bảng trình bày Bài 1.57.<br>- **HS nhóm 3:** Trình bày Bài 1.58: Ta có $320 : 45 = 7$ (dư 5). Vì còn dư 5 học sinh nên nhà trường phải thuê thêm 1 xe nữa. Vậy số xe ít nhất là $7 + 1 = 8$ xe.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khen ngợi lập luận thực tế sắc bén của học sinh trong Bài 1.58 và chuẩn hóa kết quả. | **GIẢI BÀI TẬP TRỌNG TÂM:**<br><br>1. **Bài 1.57:**<br>$$B = 21 \\cdot [(1245 + 987) : 2^3 - 15 \\cdot 12] + 21$$<br>- Tính trong ngoặc tròn: $1245 + 987 = 2232$.<br>- Tính lũy thừa và nhân: $2^3 = 8$; $15 \\cdot 12 = 180$.<br>- Thực hiện phép chia trong ngoặc vuông: $2232 : 8 = 279$.<br>- Trong ngoặc vuông: $279 - 180 = 99$.<br>- Biểu thức: $21 \\cdot 99 + 21 = 21 \\cdot (99 + 1) = 21 \\cdot 100 = 2100$.<br>*(Áp dụng tính chất phân phối để tính nhanh).*<br><br>2. **Bài 1.58:**<br>Thực hiện phép chia có dư:<br>$$320 = 45 \\cdot 7 + 5$$<br>Nếu thuê 7 xe thì chở được $45 \\cdot 7 = 315$ học sinh, còn dư 5 học sinh chưa có chỗ. Do đó, nhà trường cần thuê ít nhất là:<br>$$7 + 1 = 8\\text{ (xe)}.$$ |

---

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)

#### a) Mục tiêu:
- Vận dụng các phép tính số học giải quyết bài toán kinh tế đời sống (Bài 1.59: Doanh thu rạp chiếu phim).
- Tổng kết Chương I và dặn dò chuẩn bị Chương II.

#### b) Nội dung:
- Phân tích tình huống bán vé rạp chiếu phim trong Bài 1.59 SGK.

#### c) Sản phẩm:
- Lời giải Bài 1.59: Tổng số ghế $18 \\times 18 = 324$ ghế; doanh thu tối thứ Bảy $324 \\times 50\\ 000 = 16\\ 200\\ 000$ đồng.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu Bài 1.59 SGK: Rạp có 18 hàng ghế, mỗi hàng 18 ghế. Giá vé 50 000 đồng/vé.<br>a) Tối thứ Bảy bán hết vé, tính số tiền thu được?<br>b) Tối Chủ nhật còn 41 vé không bán được, tính số tiền thu được?<br>- **HS:** Đọc đề và phân tích phép tính.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tính tổng số ghế: $18 \\cdot 18 = 18^2 = 324$ ghế.<br>- **GV:** Khuyến khích HS dùng lũy thừa $18^2$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trả lời miệng:<br>a) Tiền tối thứ Bảy: $324 \\cdot 50\\ 000 = 16\\ 200\\ 000$ đồng.<br>b) Tối Chủ nhật bán được: $324 - 41 = 283$ vé. Tiền thu được: $283 \\cdot 50\\ 000 = 14\\ 150\\ 000$ đồng.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Đánh giá chung toàn tiết, dặn dò học sinh chuẩn bị bài cho Chương II: Tính chia hết trong tập hợp các số tự nhiên. | **BÀI 1.59 (VẬN DỤNG THỰC TẾ):**<br><br>- Tổng số ghế trong phòng chiếu phim là:<br>$$18 \\cdot 18 = 18^2 = 324\\text{ (ghế)}$$<br>a) Tối thứ Bảy bán hết vé, số tiền thu được là:<br>$$324 \\cdot 50\\ 000 = 16\\ 200\\ 000\\text{ (đồng)}$$<br>b) Tối Chủ nhật số vé bán được là:<br>$$324 - 41 = 283\\text{ (vé)}$$<br>Số tiền thu được tối Chủ nhật là:<br>$$283 \\cdot 50\\ 000 = 14\\ 150\\ 000\\text{ (đồng)}$$<br><br>**DẶN DÒ TỰ HỌC:**<br>- Hoàn thành câu c Bài 1.59 vào vở.<br>- Đọc trước Bài 8: Quan hệ chia hết và tính chất (Chương II). |
"""

# 3. BÀI 3
MD_03 = """# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 6**  
**CHỦ ĐỀ: BÀI 8. QUAN HỆ CHIA HẾT VÀ TÍNH CHẤT (2 TIẾT)**  
**Phân phối chương trình:** Tiết 14, 15 — Tuần 5  
**Thời lượng thực hiện:** 02 tiết (90 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 29 – 33)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Nhận biết được quan hệ chia hết, khái niệm ước và bội của một số tự nhiên; nắm vững ký hiệu $a \\ \\vdots \\ b$ và $a \\ \\not\\vdots \\ b$.
- Biết cách tìm tập hợp các ước $Ư(a)$ và tập hợp các bội $B(a)$ của số tự nhiên $a$.
- Nắm vững và vận dụng được tính chất chia hết của một tổng/hiệu để xét xem một tổng hoặc một hiệu có chia hết cho một số hay không mà không cần tính giá trị của tổng/hiệu đó.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự tìm tòi mối liên hệ giữa phép chia hết với ước và bội, chủ động tìm tập hợp các ước và bội.
- Giao tiếp và hợp tác: Tương tác nhóm trao đổi cách tìm ước và bội, chia sẻ kết quả kiểm chứng số học.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: Sử dụng tính chất chia hết của một tổng để lập luận chặt chẽ tính chia hết mà không cần tính cụ thể kết quả.
- Giải quyết vấn đề toán học: Giải các bài toán chia đồ vật thực tế sao cho đều nhau.

### c) Năng lực số (NLS)
- ***[NLS: 1.1.TC1a] Khai thác học liệu số mô phỏng tia số để tìm tập hợp các ước và bội của một số tự nhiên.***

### d) Năng lực Trí tuệ Nhân tạo (AI)
- ***[AI: 6.B2.1] Sử dụng trợ lý AI để gợi ý cách kiểm tra tính chia hết của các số lớn và đối chiếu với quy tắc trong SGK (Áp dụng: tiết 1, 2).***

## 3. Về phẩm chất
- Chăm chỉ: Tích cực khám phá kiến thức mới, làm quen với ngôn ngữ ký hiệu toán học chính xác.
- Trách nhiệm: Cẩn thận đối chiếu quy tắc chia hết khi sử dụng công cụ công nghệ hỗ trợ.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài giảng PowerPoint, phần mềm mô phỏng tia số trực tuyến, trợ lý AI, tivi/máy chiếu, phiếu học tập nhóm.
2. **Học sinh:** SGK Toán 6 (Tập 1), vở ghi bài, thước thẳng, bảng con/giấy nháp.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)

#### a) Mục tiêu:
- Gợi mở nhu cầu tìm hiểu về quan hệ chia hết qua tình huống thực tế chia đều đồ vật; tạo không khí học tập sôi nổi.

#### b) Nội dung:
- Giải quyết tình huống chia 15 chiếc kẹo cho 3 bạn và chia 15 chiếc kẹo cho 4 bạn.

#### c) Sản phẩm:
- HS nhận xét: Khi chia cho 3 thì mỗi bạn được 5 chiếc và không dư (chia hết); khi chia cho 4 thì mỗi bạn được 3 chiếc và còn dư 3 chiếc (không chia hết).

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Đặt vấn đề: "Cô có 15 chiếc kẹo muốn chia đều cho các bạn: Trường hợp 1 chia cho 3 bạn, trường hợp 2 chia cho 4 bạn. Em hãy nhận xét về số kẹo mỗi bạn nhận được và số kẹo còn thừa trong mỗi trường hợp?"<br>- **HS:** Tiếp nhận nhiệm vụ, suy nghĩ trong 1 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thực hiện nhẩm phép tính: $15 : 3 = 5$ (dư 0) và $15 : 4 = 3$ (dư 3).<br>- **GV:** Mời đại diện học sinh trả lời.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** "Trường hợp 1 chia hết vì số dư bằng 0; trường hợp 2 không chia hết vì còn dư 3 chiếc kẹo."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa: Phép chia có số dư bằng 0 là phép chia hết. Ta nói 15 chia hết cho 3. Ký hiệu và tính chất như thế nào, ta cùng tìm hiểu bài hôm nay. | **TÌNH HUỐNG KHỞI ĐỘNG:**<br><br>- $15 : 3 = 5$ (dư 0) $\\Rightarrow$ 15 chia hết cho 3.<br>- $15 : 4 = 3$ (dư 3) $\\Rightarrow$ 15 không chia hết cho 4.<br><br>Trong tập hợp số tự nhiên, khi nào số $a$ chia hết cho số $b$? Mối quan hệ giữa ước và bội được xác định ra sao? |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)

### 1. Hoạt động 2.1: Quan hệ chia hết, khái niệm ước và bội (25 phút)

#### a) Mục tiêu:
- Hình thành định nghĩa quan hệ chia hết, khái niệm ước và bội, ký hiệu $a \\ \\vdots \\ b$ và $a \\ \\not\\vdots \\ b$.
- Nắm vững cách tìm tập hợp các ước $Ư(a)$ và tập hợp các bội $B(a)$.
- ***[NLS: 1.1.TC1a] Khai thác học liệu số mô phỏng tia số để tìm tập hợp các ước và bội của một số tự nhiên.***
- ***[AI: 6.B2.1] Sử dụng trợ lý AI để gợi ý cách kiểm tra tính chia hết của các số lớn và đối chiếu với quy tắc trong SGK.***

#### b) Nội dung:
- Đọc định nghĩa SGK; thực hiện Hoạt động 1 và Hoạt động 2; quan sát mô phỏng tia số số học; trải nghiệm đối chiếu kết quả với AI.

#### c) Sản phẩm:
- Khái niệm ước, bội; tập hợp $Ư(12) = \\{1; 2; 3; 4; 6; 12\\}$; tập hợp $B(3) = \\{0; 3; 6; 9; 12; ...\\}$.
- Sản phẩm tương tác: Nhận diện bước nhảy trên tia số số học và kiểm tra số lớn bằng câu lệnh AI.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu định nghĩa: Cho $a, b \\in \\mathbb{N}, b \\ne 0$. Nếu có số tự nhiên $q$ sao cho $a = b \\cdot q$ thì ta nói $a$ chia hết cho $b$ (kí hiệu $a \\ \\vdots \\ b$). Khi đó $a$ là bội của $b$, và $b$ là ước của $a$.<br>- ***[NLS: 1.1.TC1a] GV trình chiếu mô phỏng học liệu số tia số tương tác: "Hãy quan sát các bước nhảy có độ dài bằng 3 trên tia số bắt đầu từ vạch 0 (0, 3, 6, 9, 12, ...). Đây chính là tập hợp các bội của 3."***<br>- ***[AI: 6.B2.1] GV hướng dẫn học sinh cách dùng câu hỏi chuẩn với trợ lý AI: "Hỏi AI: Số 234 576 có chia hết cho 12 không và vì sao? Sau đó yêu cầu học sinh đối chiếu lời giải của AI với định nghĩa $a = b \\cdot q$ trong SGK."***<br>- **HS:** Quan sát mô phỏng tia số và câu lệnh gợi ý từ AI.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Ghi bài vào vở, thực hiện tìm $Ư(12)$ và $B(4)$.<br>- **GV:** Hướng dẫn cách tìm ước bằng cách lần lượt chia cho $1, 2, 3...$ và tìm bội bằng cách nhân với $0, 1, 2, 3...$<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày: $Ư(12) = \\{1; 2; 3; 4; 6; 12\\}$, $B(4) = \\{0; 4; 8; 12; 16; ...\\}$.<br>- ***[AI: 6.B2.1] HS đối chiếu: AI chia $234\\ 576 : 12 = 19\\ 548$ (dư 0), do đó số này chia hết cho 12 vì tồn tại thương nguyên $q = 19\\ 548$.***<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa: Số 0 là bội của mọi số tự nhiên khác 0; số 1 là ước của mọi số tự nhiên. | **1. QUAN HỆ CHIA HẾT, ƯỚC VÀ BỘI:**<br><br>- **Định nghĩa:** Cho $a, b \\in \\mathbb{N}$ ($b \\ne 0$). Nếu có số tự nhiên $q$ sao cho $a = b \\cdot q$ thì:<br>$$a \\ \\vdots \\ b \\ (a \\text{ chia hết cho } b)$$<br>Ta gọi $a$ là **bội** của $b$, còn $b$ là **ước** của $a$.<br>- **Ký hiệu:**<br>+ Tập hợp các ước của $a$ là $Ư(a)$.<br>+ Tập hợp các bội của $a$ là $B(a)$.<br><br>- **Cách tìm:**<br>+ Muốn tìm các ước của $a$ ($a > 1$), ta lần lượt chia $a$ cho các số tự nhiên từ $1$ đến $a$.<br>+ Muốn tìm các bội của $a$ ($a \\ne 0$), ta nhân $a$ lần lượt với $0, 1, 2, 3...$<br><br>***[Tích hợp NLS 1.1.TC1a]: Khai thác tia số động trực quan hóa bội là các bước nhảy đều đặn $0, b, 2b, 3b...$ trên tia số.***<br>***[Tích hợp AI 6.B2.1]: Trợ lý AI hỗ trợ kiểm tra tính chia hết của số lớn và đối chiếu lại với định nghĩa SGK.*** |

---

### 2. Hoạt động 2.2: Tính chất chia hết của một tổng (20 phút)

#### a) Mục tiêu:
- Nhận biết Tính chất 1 và Tính chất 2 về sự chia hết của một tổng/hiệu.
- Vận dụng tính chất để xét tính chia hết mà không cần tính giá trị tổng/hiệu.

#### b) Nội dung:
- Thực hiện Hoạt động 3, 4 SGK trang 31; rút ra hai tính chất chia hết của một tổng.

#### c) Sản phẩm:
- Quy tắc Tính chất 1 và Tính chất 2; lời giải Luyện tập 2 SGK trang 32.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu câu hỏi: "Xét xem tổng $A = 24 + 36$ và tổng $B = 24 + 15$ có chia hết cho 6 hay không mà không cần tính kết quả?"<br>- **HS:** Thảo luận cặp đôi trong 2 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhận xét: $24 \\ \\vdots \\ 6$ và $36 \\ \\vdots \\ 6$ nên tổng chia hết cho 6. Còn $24 \\ \\vdots \\ 6$ nhưng $15 \\ \\not\\vdots \\ 6$ nên tổng không chia hết cho 6.<br>- **GV:** Hướng dẫn phát biểu thành tính chất tổng quát.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Phát biểu Tính chất 1 (các số hạng cùng chia hết) và Tính chất 2 (chỉ có 1 số hạng không chia hết).<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhấn mạnh: Tính chất chia hết của tổng cũng đúng cho hiệu và tổng nhiều số hạng. | **2. TÍNH CHẤT CHIA HẾT CỦA MỘT TỔNG:**<br><br>- **Tính chất 1:** Nếu tất cả các số hạng của một tổng đều chia hết cho cùng một số thì tổng chia hết cho số đó:<br>$$a \\ \\vdots \\ m \\text{ và } b \\ \\vdots \\ m \\Rightarrow (a + b) \\ \\vdots \\ m$$<br>- **Tính chất 2:** Nếu có một số hạng của tổng không chia hết cho một số, còn các số hạng khác đều chia hết cho số đó thì tổng không chia hết cho số đó:<br>$$a \\ \\not\\vdots \\ m \\text{ và } b \\ \\vdots \\ m \\Rightarrow (a + b) \\ \\not\\vdots \\ m$$<br>*(Áp dụng tương tự cho hiệu $a - b$ với $a \\ge b$).* |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (25 phút)

#### a) Mục tiêu:
- Củng cố kỹ năng tìm ước, bội và vận dụng tính chất chia hết của một tổng/hiệu vào giải bài tập SGK.

#### b) Nội dung:
- Giải Bài 2.1, 2.2, 2.3 SGK trang 33.

#### c) Sản phẩm:
- Lời giải chính xác các bài tập trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Yêu cầu HS làm việc cá nhân hoàn thành Bài 2.1, 2.2; thảo luận nhóm Bài 2.3 SGK.<br>- **HS:** Đọc đề và làm vào vở.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tự giác làm bài, áp dụng tính chất chia hết không cộng gộp số.<br>- **GV:** Theo dõi, nhắc nhở cách trình bày lập luận dấu suy ra $\\Rightarrow$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Gọi 3 HS lên bảng chữa bài.<br>- **HS:** Nhận xét, so sánh lời giải.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Đánh giá, chuẩn hóa cách trình bày bài toán chứng minh chia hết. | **GIẢI BÀI TẬP SGK TRANG 33:**<br><br>1. **Bài 2.1:**<br>- Các ước của 30 là: $Ư(30) = \\{1; 2; 3; 5; 6; 10; 15; 30\\}$.<br>- Các bội của 6 nhỏ hơn 40 là: $\\{0; 6; 12; 18; 24; 30; 36\\}$.<br><br>2. **Bài 2.2:** Không thực hiện phép tính, xét tính chia hết:<br>a) $48 + 56$ chia hết cho 8 vì $48 \\ \\vdots \\ 8$ và $56 \\ \\vdots \\ 8$.<br>b) $80 + 17$ không chia hết cho 8 vì $80 \\ \\vdots \\ 8$ nhưng $17 \\ \\not\\vdots \\ 8$.<br><br>3. **Bài 2.3:** Tổng $A = 12 + 14 + 16 + x$ chia hết cho 2 khi nào?<br>Vì 12, 14, 16 đều chia hết cho 2 nên tổng $A$ chia hết cho 2 khi và chỉ khi $x$ chia hết cho 2 ($x$ là số chẵn). |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)

#### a) Mục tiêu:
- Vận dụng quan hệ chia hết vào tình huống thực tế và trò chơi toán học.

#### b) Nội dung:
- Giải Bài 2.4 SGK: Đội văn nghệ có thể xếp thành các hàng đều nhau hay không?

#### c) Sản phẩm:
- Lời giải Bài 2.4 trong vở.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu bài toán Bài 2.4 SGK: Có thể chia 24 bạn nam và 30 bạn nữ thành các tổ sao cho số bạn nam và nữ trong mỗi tổ đều bằng nhau không?<br>- **HS:** Đọc đề và thảo luận cặp đôi.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Phân tích: Số tổ phải vừa là ước của 24 vừa là ước của 30.<br>- **GV:** Giới thiệu bước đệm cho khái niệm ước chung sắp học ở Bài 11.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Nêu các cách chia số tổ có thể là: 1 tổ, 2 tổ, 3 tổ hoặc 6 tổ.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khen ngợi tinh thần học tập của cả lớp và giao nhiệm vụ về nhà. | **BÀI 2.4 (VẬN DỤNG THỰC TẾ):**<br><br>Số tổ phải là ước của 24 và cũng là ước của 30.<br>- $Ư(24) = \\{1; 2; 3; 4; 6; 8; 12; 24\\}$.<br>- $Ư(30) = \\{1; 2; 3; 5; 6; 10; 15; 30\\}$.<br>Các số vừa là ước của 24 vừa là ước của 30 là: $1; 2; 3; 6$.<br>Do đó, có thể chia thành 1, 2, 3 hoặc 6 tổ.<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Học thuộc định nghĩa ước, bội và 2 tính chất chia hết của một tổng.<br>- Hoàn thành Bài 2.5 SGK trang 33.<br>- Xem trước Bài 9: Dấu hiệu chia hết. |
"""

# 4. BÀI 4
MD_04 = """# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 6**  
**CHỦ ĐỀ: BÀI 9. DẤU HIỆU CHIA HẾT (2 TIẾT)**  
**Phân phối chương trình:** Tiết 16, 17 — Tuần 6  
**Thời lượng thực hiện:** 02 tiết (90 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 34 – 37)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Nhận biết và phát biểu được dấu hiệu chia hết cho 2, cho 5 (dựa vào chữ số tận cùng).
- Nhận biết và phát biểu được dấu hiệu chia hết cho 9, cho 3 (dựa vào tổng các chữ số).
- Vận dụng thành thạo các dấu hiệu để nhận biết một số đã cho có chia hết cho 2, 3, 5, 9 hay không mà không cần thực hiện phép chia.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự quan sát đặc điểm chữ số tận cùng và tổng các chữ số để rút ra quy luật chia hết.
- Giao tiếp và hợp tác: Tương tác, thảo luận nhóm phân loại các số theo từng dấu hiệu chia hết.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: Giải thích tại sao một số vừa chia hết cho 2 vừa chia hết cho 5 thì tận cùng là 0; một số chia hết cho 9 thì chắc chắn chia hết cho 3.
- Giải quyết vấn đề toán học: Điền chữ số thích hợp vào dấu $*$ để số tạo thành thỏa mãn điều kiện chia hết.

### c) Năng lực số (NLS)
- ***[NLS: 5.3.TC1a] Sử dụng bảng tính Excel lập danh sách số và dùng Conditional Formatting để tự động nhận diện các số chia hết cho 2 và 5.***

### d) Năng lực Trí tuệ Nhân tạo (AI)
- ***[AI: 6.D1.1] Nêu tình huống không nên lạm dụng AI để giải hộ bài tập dấu hiệu chia hết nhằm bảo vệ khả năng tư duy logic cá nhân (Áp dụng: tiết 1, 2).***

## 3. Về phẩm chất
- Chăm chỉ: Chủ động thực hành bài tập, rèn luyện phản xạ tính nhẩm nhanh.
- Trách nhiệm: Ý thức rèn luyện năng lực tư duy tự thân, không ỷ lại máy móc và công cụ giải hộ.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài giảng PowerPoint, tệp Excel mẫu minh họa định dạng có điều kiện (Conditional Formatting), tivi/máy chiếu, bảng nhóm.
2. **Học sinh:** SGK Toán 6 (Tập 1), vở ghi bài, bút màu, nháp.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)

#### a) Mục tiêu:
- Tạo tình huống có vấn đề để học sinh nhận thấy lợi ích của việc nhận biết nhanh tính chia hết mà không cần đặt phép tính.

#### b) Nội dung:
- Trò chơi "Ai nhanh hơn": Cho một danh sách các số lớn và yêu cầu tìm số chia hết cho 2 và 5 trong 10 giây.

#### c) Sản phẩm:
- Câu trả lời của HS: Nhìn vào chữ số tận cùng của mỗi số.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Đưa ra các số: $234; 1\\ 565; 4\\ 890; 7\\ 821; 9\\ 432$. "Trong vòng 10 giây, em hãy chọn ra các số chia hết cho 2 và giải thích vì sao em biết nhanh như vậy?"<br>- **HS:** Quan sát và suy nghĩ nhanh.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhận diện các số có chữ số tận cùng là chẵn.<br>- **GV:** Mời 1 HS trả lời.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** "Các số chia hết cho 2 là $234; 4\\ 890; 9\\ 432$ vì chúng có chữ số cuối cùng là $4, 0, 2$."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khẳng định: Không cần đặt tính chia, chỉ cần nhìn chữ số tận cùng. Đó chính là dấu hiệu chia hết. | **TÌNH HUỐNG KHỞI ĐỘNG:**<br><br>Có những dấu hiệu nào giúp ta nhận biết một số tự nhiên chia hết cho 2, 5, 9, 3 mà không cần thực hiện phép chia? |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)

### 1. Hoạt động 2.1: Dấu hiệu chia hết cho 2, cho 5 (25 phút)

#### a) Mục tiêu:
- Nắm vững dấu hiệu chia hết cho 2 và cho 5 (chữ số tận cùng).
- ***[NLS: 5.3.TC1a] Sử dụng bảng tính Excel lập danh sách số và dùng Conditional Formatting để tự động nhận diện các số chia hết cho 2 và 5.***
- ***[AI: 6.D1.1] Nêu tình huống không nên lạm dụng AI để giải hộ bài tập dấu hiệu chia hết nhằm bảo vệ khả năng tư duy logic cá nhân.***

#### b) Nội dung:
- Tìm hiểu Hoạt động 1, 2 SGK trang 34; quan sát minh họa bảng tính Excel tự động đổi màu; thảo luận tình huống dùng AI.

#### c) Sản phẩm:
- Quy tắc dấu hiệu chia hết cho 2 và cho 5; lời giải Luyện tập 1 SGK.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Hướng dẫn HS rút ra quy tắc từ chữ số tận cùng: tận cùng $0, 2, 4, 6, 8$ chia hết cho 2; tận cùng $0, 5$ chia hết cho 5.<br>- ***[NLS: 5.3.TC1a] GV trình chiếu bảng tính Excel: "Quan sát cột dữ liệu gồm 20 số ngẫu nhiên. Khi thiết lập Conditional Formatting với công thức =MOD(A1,2)=0 (tô màu xanh) và =MOD(A1,5)=0 (tô màu vàng), bảng tính sẽ tự động nhận diện số chia hết cho 2 và 5."***<br>- ***[AI: 6.D1.1] GV nêu tình huống thảo luận: "Nếu các em chụp ảnh đề bài dấu hiệu chia hết đưa cho AI giải hộ thì rất nhanh có đáp án. Nhưng tại sao chúng ta không nên lạm dụng AI trong bài học này?"***<br>- **HS:** Quan sát bảng tính Excel và suy nghĩ câu hỏi thảo luận.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thảo luận cặp đôi về quy tắc và câu hỏi về AI.<br>- **GV:** Quan sát, định hướng.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Phát biểu dấu hiệu chia hết cho 2 và cho 5.<br>- ***[AI: 6.D1.1] HS trả lời: "Dấu hiệu chia hết rất đơn giản, chỉ cần nhìn chữ số tận cùng. Nếu nhờ AI làm thay thì não bộ sẽ bị thụ động, mất phản xạ quan sát và làm giảm khả năng tư duy logic cá nhân."***<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Biểu dương ý thức tự rèn luyện của học sinh và chốt kiến thức vào vở. | **1. DẤU HIỆU CHIA HẾT CHO 2, CHO 5:**<br><br>- **Dấu hiệu chia hết cho 2:**<br>Các số có chữ số tận cùng là $0, 2, 4, 6, 8$ (chữ số chẵn) thì chia hết cho 2 và chỉ những số đó mới chia hết cho 2.<br>- **Dấu hiệu chia hết cho 5:**<br>Các số có chữ số tận cùng là $0$ hoặc $5$ thì chia hết cho 5 và chỉ những số đó mới chia hết cho 5.<br>- **Chú ý:** Các số có chữ số tận cùng là $0$ thì vừa chia hết cho 2 vừa chia hết cho 5.<br><br>***[Tích hợp NLS 5.3.TC1a]: Ứng dụng Excel tự động lọc và tô màu số chia hết bằng Conditional Formatting.***<br>***[Tích hợp AI 6.D1.1]: Tự chủ học tập, tránh lạm dụng AI để bảo vệ tư duy logic cá nhân.*** |

---

### 2. Hoạt động 2.2: Dấu hiệu chia hết cho 9, cho 3 (20 phút)

#### a) Mục tiêu:
- Nắm vững dấu hiệu chia hết cho 9 và cho 3 (tính tổng các chữ số).
- Phân biệt sự khác nhau cơ bản giữa nhóm dấu hiệu $(2, 5)$ và nhóm dấu hiệu $(9, 3)$.

#### b) Nội dung:
- Tìm hiểu Hoạt động 3, 4 SGK trang 36; tính tổng các chữ số và rút ra kết luận.

#### c) Sản phẩm:
- Quy tắc dấu hiệu chia hết cho 9 và cho 3; lời giải Luyện tập 2 SGK.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Yêu cầu HS tính tổng các chữ số của số 243 và số 157. Xét xem tổng đó có chia hết cho 9 và cho 3 không?<br>- **HS:** Tính: $2 + 4 + 3 = 9$ (chia hết cho 9 và 3); $1 + 5 + 7 = 13$ (không chia hết).<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhận xét mối quan hệ giữa tổng các chữ số với tính chia hết cho 9 và 3.<br>- **GV:** Hướng dẫn phát biểu quy tắc.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** "Các số có tổng các chữ số chia hết cho 9 thì chia hết cho 9; các số có tổng các chữ số chia hết cho 3 thì chia hết cho 3."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhấn mạnh: Số chia hết cho 9 thì luôn chia hết cho 3, nhưng số chia hết cho 3 chưa chắc chia hết cho 9 (ví dụ số 12). | **2. DẤU HIỆU CHIA HẾT CHO 9, CHO 3:**<br><br>- **Dấu hiệu chia hết cho 9:**<br>Các số có tổng các chữ số chia hết cho 9 thì chia hết cho 9 và chỉ những số đó mới chia hết cho 9.<br>- **Dấu hiệu chia hết cho 3:**<br>Các số có tổng các chữ số chia hết cho 3 thì chia hết cho 3 và chỉ những số đó mới chia hết cho 3.<br>- **Nhận xét quan trọng:**<br>Một số chia hết cho 9 thì chắc chắn chia hết cho 3. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (25 phút)

#### a) Mục tiêu:
- Vận dụng phối hợp các dấu hiệu để phân loại số và điền chữ số thích hợp vào dấu $*$.

#### b) Nội dung:
- Thực hiện Bài 2.10, 2.11, 2.12 SGK trang 37.

#### c) Sản phẩm:
- Lời giải chính xác trong vở ghi của học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao nhiệm vụ cho 3 nhóm:<br>+ Nhóm 1: Bài 2.10 (phân loại số chia hết cho 2, cho 5).<br>+ Nhóm 2: Bài 2.11 (phân loại số chia hết cho 3, cho 9).<br>+ Nhóm 3: Bài 2.12 (tìm chữ số $*$ để số $\\overline{12*}$ chia hết cho cả 2 và 5).<br>- **HS:** Làm việc nhóm trong 5 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Làm bài ra bảng phụ, đối chiếu kết quả.<br>- **GV:** Quan sát, hỗ trợ.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện các nhóm treo bảng phụ và thuyết minh lời giải.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chốt đáp án chuẩn mực. | **GIẢI BÀI TẬP SGK TRANG 37:**<br><br>1. **Bài 2.10:** Trong các số $324; 245; 1\\ 010; 4\\ 568$:<br>- Số chia hết cho 2 là: $324; 1\\ 010; 4\\ 568$.<br>- Số chia hết cho 5 là: $245; 1\\ 010$.<br>- Số vừa chia hết cho 2 vừa chia hết cho 5 là: $1\\ 010$.<br><br>2. **Bài 2.11:** Xét các số $135; 252; 341; 486$:<br>- Tổng chữ số: $135 \\rightarrow 9$; $252 \\rightarrow 9$; $341 \\rightarrow 8$; $486 \\rightarrow 18$.<br>- Số chia hết cho 3 là: $135; 252; 486$.<br>- Số chia hết cho 9 là: $135; 252; 486$.<br><br>3. **Bài 2.12:** Số $\\overline{12*}$ chia hết cho cả 2 và 5 $\\Rightarrow$ Chữ số tận cùng phải là $0$. Vậy $* = 0$. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)

#### a) Mục tiêu:
- Vận dụng kiến thức dấu hiệu chia hết giải bài toán chia nhóm thực tiễn và kiểm tra mã số.

#### b) Nội dung:
- Giải bài toán chia phần thưởng: Cô giáo có 45 quyển vở và 60 chiếc bút, có thể chia đều cho 5 tổ được không? Có thể chia đều cho 3 tổ được không?

#### c) Sản phẩm:
- Lời giải bài toán thực tế trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu bài toán thực tế: "Cô giáo có 45 quyển vở và 60 chiếc bút. Cô có thể chia đều số vở và bút này cho 5 tổ được không? Cho 3 tổ được không? Vì sao?"<br>- **HS:** Đọc đề và suy nghĩ cách giải.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Dùng dấu hiệu chia hết cho 5 và cho 3 để giải thích mà không cần thực hiện phép chia.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trả lời: Chia đều cho 5 tổ được vì 45 và 60 đều có chữ số tận cùng là 5 và 0 nên đều chia hết cho 5. Chia đều cho 3 tổ được vì $4+5=9$ chia hết cho 3 và $6+0=6$ chia hết cho 3.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Đánh giá cao lập luận chặt chẽ của HS và dặn dò về nhà. | **BÀI TOÁN THỰC TẾ (VẬN DỤNG):**<br><br>- Vì $45$ và $60$ đều có chữ số tận cùng là $5$ và $0$ nên đều chia hết cho 5 $\\Rightarrow$ Chia đều được cho 5 tổ.<br>- Vì tổng các chữ số của $45$ là $4+5=9 \\ \\vdots \\ 3$ và của $60$ là $6+0=6 \\ \\vdots \\ 3$ nên cả hai số đều chia hết cho 3 $\\Rightarrow$ Chia đều được cho 3 tổ.<br><br>**DẶN DÒ TỰ HỌC:**<br>- Học thuộc 4 dấu hiệu chia hết cho 2, 5, 9, 3.<br>- Hoàn thành các bài tập còn lại trong SGK trang 37.<br>- Đọc trước Bài 10: Số nguyên tố. |
"""

all_lessons = [
    ("KHBD_01_Toan6_LuyenTapChung_Tiet12.md", MD_01),
    ("KHBD_02_Toan6_BaiTapCuoiChuong1_Tiet13.md", MD_02),
    ("KHBD_03_Toan6_Bai8_QuanHeChiaHetVaTinhChat_Tiet14-15.md", MD_03),
    ("KHBD_04_Toan6_Bai9_DauHieuChiaHet_Tiet16-17.md", MD_04)
]

for filename, content in all_lessons:
    fpath = os.path.join(OUT_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {filename} ({len(content)} chars)")

print("Hoàn thành tạo 4 bài đầu tiên!")
