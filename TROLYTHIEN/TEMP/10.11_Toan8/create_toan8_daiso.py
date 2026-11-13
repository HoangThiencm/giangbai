# -*- coding: utf-8 -*-
"""
Script sinh 12 tệp KHBD Markdown môn Toán 8 (Đại số & Thống kê - Tuần 13 - 18)
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Toan8"
os.makedirs(OUT_DIR, exist_ok=True)

# 01. Bài 9: Phân tích đa thức thành nhân tử (Tiết 3 - Tiết CT 25)
md_01 = """Tiết 25 - BÀI 9: PHÂN TÍCH ĐA THỨC THÀNH NHÂN TỬ (TIẾT 3)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và hoàn thiện kĩ năng phân tích đa thức thành nhân tử bằng phương pháp phối hợp nhiều phương pháp (đặt nhân tử chung, dùng hằng đẳng thức, nhóm hạng tử, tách hoặc thêm bớt hạng tử).
- Vận dụng thành thạo phân tích đa thức thành nhân tử để: tính nhanh giá trị của biểu thức tại giá trị cho trước của biến; tìm giá trị chưa biết $x$ (đưa về phương trình tích); rút gọn biểu thức phân thức.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát cấu trúc đa thức để lựa chọn phương pháp phân tích tối ưu.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp tách hạng tử trong nhóm bạn.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Giải thích căn cứ tách hạng tử $ax^2 + bx + c$ thành hai nhóm có nhân tử chung.
- Năng lực giải quyết vấn đề toán học: Biến đổi biểu thức đại số phức tạp về tích các đa thức bậc nhất.

c) Năng lực số (NLS):
- ***3.4.TC2a: HS liệt kê các bước câu lệnh để phần mềm GeoGebra hoặc máy tính cầm tay thực hiện lệnh Factor(đa_thức) nhằm kiểm chứng kết quả phân tích đa thức thành nhân tử.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để phân tích các bước biến đổi đa thức và tìm ra phương pháp giải ngắn gọn nhất.***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, cẩn trọng trong biến đổi dấu và hệ số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 1, KHBD, máy chiếu, bảng phụ ghi quy trình phối hợp các phương pháp.
2. Học sinh: SGK Toán 8, vở ghi, máy tính cầm tay.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy phân tích đa thức qua câu đố tìm $x$.
b) Nội dung: Tìm $x$ biết: $x^2 - 4x = 0$.
c) Sản phẩm: Bảng kết quả của học sinh: $x(x - 4) = 0 \\rightarrow x = 0$ hoặc $x = 4$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt câu hỏi: Tìm $x$ biết $x^2 - 4x = 0$.<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt nhân tử chung $x(x - 4) = 0$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ giải thích: Tích bằng $0$ khi một trong hai thừa số bằng $0$, do đó $x = 0$ hoặc $x = 4$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, dẫn dắt vào tiết học hoàn thiện kĩ năng phối hợp các phương pháp. | **Khởi động:**<br>$x^2 - 4x = 0$<br>$x(x - 4) = 0$<br>Suy ra $x = 0$ hoặc $x = 4$. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH VÀ HOÀN THIỆN KĨ NĂNG (25 phút)
### Hoạt động 2.1: Phối hợp nhiều phương pháp phân tích đa thức (15 phút)
a) Mục tiêu: Nắm vững thứ tự ưu tiên khi phân tích đa thức thành nhân tử.
b) Nội dung: Tìm hiểu Ví dụ 4, Luyện tập 3 SGK trang 42.
c) Sản phẩm: Lời giải bài tập phân tích đa thức phối hợp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho đa thức: $P = x^3 - 4x^2 + 4x$. Nêu câu hỏi:<br>  1. Bước đầu tiên ta nên làm gì?<br>  2. Biểu thức trong ngoặc có dạng hằng đẳng thức nào?<br>- **HS:** Quan sát và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đặt nhân tử chung $x$ ra ngoài: $P = x(x^2 - 4x + 4) = x(x - 2)^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy trình: 1. Đặt nhân tử chung $\\rightarrow$ 2. Dùng hằng đẳng thức $\\rightarrow$ 3. Nhóm hạng tử. | **1. Phối hợp nhiều phương pháp:**<br>Ví dụ: Phân tích $P = x^3 - 4x^2 + 4x$<br>$P = x(x^2 - 4x + 4)$ (Đặt nhân tử chung)<br>$P = x(x - 2)^2$ (Dùng hằng đẳng thức bình phương của một hiệu). |

### Hoạt động 2.2: Phương pháp tách hạng tử đối với tam thức bậc hai (10 phút)
a) Mục tiêu: Biết cách tách hạng tử bậc nhất trong tam thức bậc hai $x^2 + bx + c$.
b) Nội dung: Phân tích đa thức $x^2 - 5x + 6$ thành nhân tử.
c) Sản phẩm: Lời giải của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cách tách: Tìm hai số có tích bằng $6$ và có tổng bằng $-5$, đó là $-2$ và $-3$. Tách $-5x = -2x - 3x$.<br>- **HS:** Ghi nhận phương pháp và làm bài.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm: $(x^2 - 2x) - (3x - 6) = x(x - 2) - 3(x - 2) = (x - 2)(x - 3)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa kĩ thuật tách hạng tử kinh điển. | **2. Phương pháp tách hạng tử:**<br>$x^2 - 5x + 6 = x^2 - 2x - 3x + 6$<br>$= (x^2 - 2x) - (3x - 6)$<br>$= x(x - 2) - 3(x - 2)$<br>$= (x - 2)(x - 3)$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
a) Mục tiêu: Vận dụng giải bài tập tìm $x$ và tính nhanh.
b) Nội dung: Giải bài tập 2.24 SGK trang 43: Tìm $x$ biết $x^2 - 25 - (x - 5) = 0$.
c) Sản phẩm: Lời giải của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu HS giải bài 2.24 SGK.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Biến đổi $x^2 - 25 = (x - 5)(x + 5)$, sau đó đặt nhân tử chung $(x - 5)$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng giải: $(x - 5)(x + 5 - 1) = 0 \\rightarrow (x - 5)(x + 4) = 0$. Suy ra $x = 5$ hoặc $x = -4$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Sửa bài cẩn thận, khen ngợi học sinh. | **Bài 2.24 (SGK tr.43):**<br>$x^2 - 25 - (x - 5) = 0$<br>$(x - 5)(x + 5) - (x - 5) = 0$<br>$(x - 5)(x + 5 - 1) = 0$<br>$(x - 5)(x + 4) = 0$<br>Do đó $x = 5$ hoặc $x = -4$. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
a) Mục tiêu: Vận dụng lệnh Factor trong phần mềm số để kiểm tra phân tích đa thức.
b) Nội dung: Viết cú pháp lệnh phần mềm phân tích đa thức $2x^3 - 8x$.
c) Sản phẩm: Câu trả lời của học sinh: `Factor(2x^3 - 8x) = 2x(x - 2)(x + 2)`.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi: Trên GeoGebra/CAS, em nhập lệnh nào để kiểm tra kết quả phân tích đa thức $2x^3 - 8x$?<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu: Nhập lệnh `Factor(2x^3 - 8x)`.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt bài học, dặn dò chuẩn bị tiết Luyện tập chung. | **Vận dụng số (NLS 3.4.TC2a):**<br>Lệnh `Factor(đa_thức)` trong phần mềm GeoGebra trả về kết quả phân tích: `2x(x - 2)(x + 2)`. |
"""

# 02. Luyện tập chung Tiết 26
md_02 = """Tiết 26 - LUYỆN TẬP CHUNG (TRANG 43)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Củng cố và hệ thống hóa toàn bộ các phương pháp phân tích đa thức thành nhân tử: Đặt nhân tử chung, dùng hằng đẳng thức, nhóm hạng tử và phối hợp nhiều phương pháp.
- Rèn luyện kĩ năng nhận diện cấu trúc đa thức để áp dụng phương pháp thích hợp; vận dụng thành thạo vào bài toán rút gọn, tìm $x$ và tính nhanh giá trị biểu thức.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa kiến thức qua sơ đồ tư duy phân nhánh các phương pháp phân tích đa thức.
- Giao tiếp và hợp tác: Tự tin thuyết trình sản phẩm sơ đồ tư duy trước lớp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học; Năng lực giải quyết vấn đề toán học.

c) Năng lực số (NLS):
- ***3.1.TC2b: HS trình bày sản phẩm số là sơ đồ tư duy phân nhánh các phương pháp phân tích đa thức thành nhân tử và chia sẻ sản phẩm học tập trong nhóm.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng AI để tạo các bài toán phân tích đa thức nâng cao có tính ứng dụng thực tiễn.***

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, chính xác, kỷ luật và kiên trì trong học tập.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Tập 1, KHBD, Sơ đồ tư duy Luyện tập chung Tiết 26 (vector 300 DPI), tivi/máy chiếu, phiếu bài tập.
2. Học sinh: SGK Toán 8, vở bài tập, máy tính cầm tay, bảng con.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy và sự tập trung thông qua bảng ghép nối phương pháp phân tích đa thức.
b) Nội dung: Nối đa thức ở Cột A với phương pháp phân tích thích hợp ở Cột B.
c) Sản phẩm: Bảng nối của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu bảng nối nhanh:<br>  1. $5x(x - y) + 10(x - y) \\rightarrow$ A. Dùng hằng đẳng thức<br>  2. $x^2 - 9 \\rightarrow$ B. Đặt nhân tử chung<br>  3. $x^2 - y^2 + 2x + 2y \\rightarrow$ C. Nhóm hạng tử<br>- **HS:** Chuẩn bị bảng con.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nối nhanh và giơ bảng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ đọc: 1-B, 2-A, 3-C.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, dẫn dắt vào bài luyện tập chung. | **Đáp án khởi động:**<br>1-B; 2-A; 3-C. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ mạng lưới các phương pháp phân tích đa thức thành nhân tử qua Sơ đồ tư duy.
b) Nội dung: Quan sát Sơ đồ tư duy Mindmap Tiết 26; nhắc lại các công thức cốt lõi.

![Sơ đồ tư duy Luyện tập chung Tiết 26](khbd-ill:mindmap-toan8-tiet26)

c) Sản phẩm: Bảng ghi nhớ các phương pháp phân tích đa thức trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Tiết 26. Yêu cầu HS nêu 4 phương pháp chính và thứ tự ưu tiên áp dụng.<br>- **HS:** Quan sát sơ đồ tư duy và trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trình bày tóm tắt.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy trình phân tích đa thức. | **Hệ thống kiến thức:**<br>1. Đặt nhân tử chung: $A \\cdot B + A \\cdot C = A(B + C)$.<br>2. Dùng hằng đẳng thức: 7 hằng đẳng thức.<br>3. Nhóm hạng tử thích hợp.<br>4. Phối hợp nhiều phương pháp. |

### Hoạt động 2.2: Luyện giải bài tập phân dạng (22 phút)
a) Mục tiêu: Giải thành thạo các bài tập 2.25, 2.26 SGK trang 43.
b) Nội dung: Phân tích đa thức thành nhân tử, tính nhanh giá trị biểu thức và tìm $x$.
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập 2.25 và 2.26 SGK.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải bài tập vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 3 HS lên bảng chữa bài.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt phương pháp giải. | **Bài 2.25 (SGK tr.43): Phân tích đa thức:**<br>a) $x^3 + 4x = x(x^2 + 4)$.<br>b) $6ab - 9ab^2 = 3ab(2 - 3b)$.<br>c) $2a(x - 1) + 3b(1 - x) = 2a(x - 1) - 3b(x - 1) = (x - 1)(2a - 3b)$.<br><br>**Bài 2.26 (SGK tr.43): Tính nhanh:**<br>Tính giá trị biểu thức $A = x^2 - 2xy + y^2 - 100$ tại $x = 115$ và $y = 25$:<br>$A = (x - y)^2 - 10^2 = (x - y - 10)(x - y + 10)$.<br>Thay $x - y = 115 - 25 = 90$ vào $A$:<br>$A = (90 - 10)(90 + 10) = 80 \\cdot 100 = 8000$. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng phân tích đa thức thành nhân tử để chứng minh tính chia hết.
b) Nội dung: Chứng minh rằng với mọi số nguyên $n$, biểu thức $n^3 - n$ luôn chia hết cho $6$.
c) Sản phẩm: Lời giải chứng minh của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán: Chứng minh $n^3 - n$ chia hết cho $6$ với mọi $n \\in \\mathbb{Z}$.<br>- **HS:** Phân tích $n^3 - n = n(n^2 - 1) = (n - 1)n(n + 1)$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhận xét đây là tích của 3 số nguyên liên tiếp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy giải thích: Trong 3 số nguyên liên tiếp luôn có một số chia hết cho 2 và một số chia hết cho 3, do đó tích chia hết cho $2 \\cdot 3 = 6$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương học sinh có tư duy số học rất sắc bén. Dặn dò chuẩn bị tiết Bài tập cuối chương II. | **Lời giải chứng minh:**<br>Ta có: $n^3 - n = n(n^2 - 1) = (n - 1) \\cdot n \\cdot (n + 1)$.<br>Vì $(n - 1), n, (n + 1)$ là ba số nguyên liên tiếp nên trong đó luôn có ít nhất một số chia hết cho 2 và một số chia hết cho 3. Vì $\\text{ƯCLN}(2, 3) = 1$ nên tích của chúng chia hết cho $2 \\cdot 3 = 6$.<br>Vậy $(n^3 - n)$ chia hết cho $6$ với mọi số nguyên $n$. |
"""

tasks = [
    ("01_KHBD_Toan8_Bai09_PhanTichDaThucThanhNhanTu_Tiet25.md", md_01),
    ("02_KHBD_Toan8_LuyenTapChung_DaiSo_Tiet26.md", md_02),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
