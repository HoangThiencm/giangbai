# -*- coding: utf-8 -*-
"""Tạo trọn bộ 09 Kế hoạch bài dạy (KHBD) chuẩn Công văn 5512
Đúng 100% hợp đồng soạn KHBD của Hệ thống:
- Tiêu đề 2 dòng tinh gọn
- Cấu trúc 4 hoạt động A, B, C, D có BẢNG 2 CỘT chuẩn CV 5512
- Khai thác CSDL Thư viện số DlibK12 + Màn hình Tivi + Laptop GV
- Tích hợp Năng lực số và AI in đậm, in nghiêng
- Kèm Phần IV: Phụ lục Phiếu học tập & Sản phẩm học tập minh chứng hoàn chỉnh lưu Thư viện
"""

import os
import sys

out_dir = r"C:\Users\HoangThien\Documents\GitHub\giangbai\TROLYTHIEN\1_SOAN_KHBD\Ket_qua\05.11"
os.makedirs(out_dir, exist_ok=True)

# 1. Thầy Hoàng Tấn Thiên (Toán 9)
md_01 = """Tiết 27 - BÀI 8: KHAI CĂN BẬC HAI VỚI PHÉP NHÂN VÀ PHÉP CHIA
*Thời lượng thực hiện: 01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12 (Luyện tập ứng dụng)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Vận dụng thành thạo định lí khai phương một tích $\\sqrt{a \\cdot b} = \\sqrt{a} \\cdot \\sqrt{b}$ và quy tắc nhân các căn bậc hai (với $a \\ge 0, b \\ge 0$).
- Vận dụng thành thạo định lí khai phương một thương $\\sqrt{\\frac{a}{b}} = \\frac{\\sqrt{a}}{\\sqrt{b}}$ và quy tắc chia các căn bậc hai (với $a \\ge 0, b > 0$).
- Vận dụng các quy tắc để rút gọn biểu thức chứa căn, tính giá trị số và giải quyết bài toán thực tế hình học.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác thực hiện các bài tập trên Phiếu học tập, chủ động tra cứu bài giảng số trên hệ thống Thư viện số DlibK12.
- Giao tiếp và hợp tác: Tương tác nhóm tích cực, biết lắng nghe và phản biện kết quả rút gọn căn thức trên màn hình Tivi Thư viện.

b) Năng lực Toán học:
- Tư duy và lập luận toán học: Phân tích các số dưới dấu căn thành tích của các số chính phương để khai phương nhanh chóng.
- Giải quyết vấn đề toán học: Thiết lập biểu thức căn bậc hai mô tả đại lượng thực tế và tính toán kết quả chính xác.

c) Năng lực số (NLS):
- ***(Tích hợp NLS 1.1.TC2a: Học sinh khai thác CSDL Thư viện số DlibK12 để quan sát video bài giảng số minh họa ứng dụng khai căn trong công thức vật lý và hình học)***.
- ***(Tích hợp NLS 2.2.TC2b: Học sinh hợp tác nhóm, trình bày và kiểm tra chéo kết quả bài làm qua màn hình Tivi tương tác lớn của Thư viện)***.

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***(Tích hợp AI 6.B2.1: Tiếp cận và quan sát giáo viên sử dụng công cụ AI kiểm chứng kết quả biến đổi rút gọn biểu thức đại số phức tạp)***.

## 3. Về phẩm chất
- Chăm chỉ: Cẩn thận trong biến đổi căn thức, không bỏ sót điều kiện xác định.
- Trách nhiệm: Hoàn thành nhiệm vụ nhóm được phân công, bảo quản trang thiết bị Thư viện số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Màn hình Tivi tương tác lớn tại phòng đọc Thư viện kết nối Laptop giáo viên qua cổng HDMI.
- Đường truyền mạng Internet Thư viện truy cập CSDL Thư viện số DlibK12.
- Video bài giảng số, gói bài tập trắc nghiệm tương tác trên DlibK12.
- SGK Toán 9 Tập 1 (bộ Kết nối tri thức với cuộc sống), Phiếu học tập số 1 và số 2.
2. Học sinh:
- SGK Toán 9 Tập 1, vở ghi chép, máy tính cầm tay, bút viết.
- Tài khoản học sinh đăng nhập Thư viện số DlibK12.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Nhắc lại quy tắc khai phương một tích và một thương; tạo hứng thú học tập qua tình huống tính toán thực tế.
b) Nội dung: Trả lời nhanh hai câu hỏi khởi động và xem clip ngắn trên DlibK12 về công thức tính vận tốc rơi tự do $v = \\sqrt{2gh}$.
c) Sản phẩm: Câu trả lời của học sinh về công thức khai phương và giá trị vận tốc.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Bật màn hình Tivi Thư viện, kết nối Laptop chiếu video 2 phút từ DlibK12 về chuyển động rơi tự do với công thức $v = \\sqrt{2gh}$. Yêu cầu học sinh nhắc lại công thức khai phương một tích và một thương.<br>- **HS:** Quan sát màn hình Tivi và lắng nghe câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhớ lại kiến thức bài trước, thảo luận nhanh theo cặp bàn.<br>- **GV:** Quan sát, khích lệ học sinh xung phong.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát biểu: Với $a \\ge 0, b \\ge 0$ thì $\\sqrt{a \\cdot b} = \\sqrt{a} \\cdot \\sqrt{b}$. Với $a \\ge 0, b > 0$ thì $\\sqrt{\\frac{a}{b}} = \\frac{\\sqrt{a}}{\\sqrt{b}}$.<br>- **GV:** Mời học sinh khác nhận xét.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định câu trả lời chính xác, khen ngợi học sinh và dẫn dắt vào tiết luyện tập ứng dụng tại Thư viện số. | **Khởi động:**<br>- Quy tắc khai phương một tích: $\\sqrt{a \\cdot b} = \\sqrt{a} \\cdot \\sqrt{b}$ ($a \\ge 0, b \\ge 0$).<br>- Quy tắc khai phương một thương: $\\sqrt{\\frac{a}{b}} = \\frac{\\sqrt{a}}{\\sqrt{b}}$ ($a \\ge 0, b > 0$).<br>- Ứng dụng thực tế: Tính vận tốc, khoảng cách và diện tích chứa căn bậc hai. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI / KHÁM PHÁ TRÊN DLIBK12 (18 phút)
a) Mục tiêu: Khắc sâu kỹ thuật phân tích số dưới dấu căn thành tích các thừa số chính phương và kỹ thuật nhân liên hợp khử căn ở mẫu.
b) Nội dung: Khai thác bài giảng số trên DlibK12, làm việc với các ví dụ biến đổi nâng cao và bài toán thực tế.
c) Sản phẩm: Lời giải các ví dụ rút gọn biểu thức trong vở học sinh và trên phiếu học tập.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Mở chuyên mục Học liệu số Toán 9 trên DlibK12, chiếu ví dụ mẫu lên Tivi Thư viện:<br>1) Tính: $A = \\sqrt{12} \\cdot \\sqrt{27}$; $B = \\sqrt{\\frac{49}{81}} : \\sqrt{\\frac{25}{36}}$.<br>2) Rút gọn biểu thức: $P = \\sqrt{20a} - \\sqrt{45a} + \\sqrt{80a}$ với $a \\ge 0$.<br>- ***(Tích hợp NLS 1.1.TC2a: GV hướng dẫn HS quan sát sơ đồ tư duy tương tác phân tích số 20, 45, 80 trên màn hình DlibK12 để tìm nhân tử chính phương)***.<br>- **HS:** Đọc đề bài, ghi nhận nhiệm vụ vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc cá nhân 5 phút, sau đó thảo luận nhóm 4 em để thống nhất lời giải.<br>- **GV:** Đi quanh các bàn đọc Thư viện quan sát, hỗ trợ các nhóm còn lúng túng khi tách căn.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời 2 đại diện nhóm lên bảng Tivi Thư viện trình bày lời giải.<br>- **HS:** Nhóm 1 trình bày câu 1: $A = \\sqrt{12 \\cdot 27} = \\sqrt{324} = 18$ hoặc $A = 2\\sqrt{3} \\cdot 3\\sqrt{3} = 18$.<br>- **HS:** Nhóm 2 trình bày câu 2: $P = 2\\sqrt{5a} - 3\\sqrt{5a} + 4\\sqrt{5a} = (2 - 3 + 4)\\sqrt{5a} = 3\\sqrt{5a}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chuẩn hóa lời giải. Nhấn mạnh kỹ năng tách số chính phương $4, 9, 16, 25...$ giúp việc rút gọn diễn ra cực kỳ nhanh chóng. | **1. Kỹ năng nhân và chia căn thức bậc hai:**<br>- Tách nhân tử chính phương trước khi khai căn:<br>$A = \\sqrt{12} \\cdot \\sqrt{27} = \\sqrt{4 \\cdot 3} \\cdot \\sqrt{9 \\cdot 3} = 2\\sqrt{3} \\cdot 3\\sqrt{3} = 6 \\cdot 3 = 18$.<br>$B = \\sqrt{\\frac{49}{81}} : \\sqrt{\\frac{25}{36}} = \\frac{7}{9} : \\frac{5}{6} = \\frac{7}{9} \\cdot \\frac{6}{5} = \\frac{14}{15}$.<br><br>**2. Rút gọn biểu thức đồng dạng:**<br>Với $a \\ge 0$:<br>$P = \\sqrt{4 \\cdot 5a} - \\sqrt{9 \\cdot 5a} + \\sqrt{16 \\cdot 5a}$<br>$P = 2\\sqrt{5a} - 3\\sqrt{5a} + 4\\sqrt{5a} = 3\\sqrt{5a}$. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP / THỰC HÀNH TƯƠNG TÁC (15 phút)
a) Mục tiêu: Vận dụng làm bài tập nhóm trên Phiếu học tập số 1 và tham gia giải câu hỏi trắc nghiệm trực tuyến trên DlibK12.
b) Nội dung: Giải bài tập 1, 2 trên Phiếu học tập và thi đua chọn đáp án trắc nghiệm trên Tivi Thư viện.
c) Sản phẩm: Kết quả bài làm trên Phiếu học tập số 1 và điểm số trắc nghiệm trên DlibK12.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát Phiếu học tập số 1 cho các nhóm. Đồng thời mở gói câu hỏi trắc nghiệm 4 câu trên giao diện DlibK12 chiếu lên màn hình Tivi Thư viện.<br>- **HS:** Nhận phiếu học tập, cử nhóm trưởng điều hành.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm thảo luận giải bài tập số 1 trong phiếu. Sau đó cử 1 đại diện cầm điều khiển/chuột máy tính chọn đáp án trắc nghiệm trực tiếp trên Tivi.<br>- ***(Tích hợp NLS 2.2.TC2b: Các nhóm thi đua thao tác bấm chọn đáp án trên nền tảng số DlibK12, hệ thống phản hồi âm thanh đúng/sai tức thì)***.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Chiếu bảng tổng hợp điểm thi đua giữa các nhóm trên Tivi Thư viện.<br>- **HS:** Các nhóm đối chiếu bài làm, thảo luận câu hỏi có tỉ lệ chọn sai nhiều nhất.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương các nhóm hoàn thành nhanh và chính xác. Khắc phục lỗi sai phổ biến: quên dấu giá trị tuyệt đối khi khai phương bình phương $\\sqrt{A^2} = |A|$. | **Luyện tập tương tác:**<br>- Bài tập trắc nghiệm số DlibK12:<br>+ Câu 1: $\\sqrt{0.16 \\cdot 25} = 0.4 \\cdot 5 = 2$ (Đúng).<br>+ Câu 2: $\\sqrt{\\frac{144}{a^2}} = \\frac{12}{|a|}$ với $a \\ne 0$.<br>- Rèn luyện phản xạ tính nhanh và tính chính xác trong môi trường số. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (7 phút)
a) Mục tiêu: Giải bài toán thực tế về tính diện tích tam giác và nộp sản phẩm học tập lưu hồ sơ Thư viện.
b) Nội dung: Giải bài toán ứng dụng tính diện tích cánh buồm tam giác theo công thức Heron; bàn giao Phiếu học tập số 1 cho cán bộ Thư viện.
c) Sản phẩm: Bài giải hoàn chỉnh trên Phiếu học tập số 1 được các nhóm ký tên nộp lại Thư viện.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh cánh buồm hình tam giác có độ dài 3 cạnh $a = 5\\text{ m}, b = 6\\text{ m}, c = 7\\text{ m}$. Yêu cầu các nhóm tính diện tích cánh buồm theo công thức Heron: $S = \\sqrt{p(p-a)(p-b)(p-c)}$ với $p$ là nửa chu vi.<br>- **HS:** Tiếp nhận nhiệm vụ, hoàn thiện vào mục Vận dụng trên Phiếu học tập số 1.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính nửa chu vi $p = \\frac{5 + 6 + 7}{2} = 9\\text{ m}$. Thay số: $S = \\sqrt{9(9-5)(9-6)(9-7)} = \\sqrt{9 \\cdot 4 \\cdot 3 \\cdot 2} = \\sqrt{216} = 6\\sqrt{6} \\approx 14.7\\text{ m}^2$.<br>- **GV:** Theo dõi, hướng dẫn cách bấm máy tính làm tròn số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm đọc to kết quả và giải thích các bước khai phương.<br>- ***(Tích hợp AI 6.B2.1: GV dùng trợ lý số trên laptop kiểm chứng nhanh kết quả: 6√6 ≈ 14.6969m² cho HS quan sát)***.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Đánh giá tiết học tại Thư viện số diễn ra sôi nổi, hiệu quả.<br>- **GV:** Thu toàn bộ Phiếu học tập số 1 của các nhóm, bàn giao ngay cho Cán bộ Thư viện để lưu hồ sơ minh chứng theo Kế hoạch 115. | **Vận dụng thực tế:**<br>- Nửa chu vi cánh buồm: $p = \\frac{5 + 6 + 7}{2} = 9\\text{ (m)}$.<br>- Diện tích cánh buồm: $S = \\sqrt{9 \\cdot (9 - 5) \\cdot (9 - 6) \\cdot (9 - 7)} = \\sqrt{9 \\cdot 4 \\cdot 3 \\cdot 2} = 6\\sqrt{6} \\approx 14.7\\text{ (m}^2\\text{)}$.<br><br>**Bàn giao sản phẩm lưu Thư viện:**<br>- 100% nhóm HS nộp Phiếu học tập số 1 có đầy đủ chữ ký nhóm trưởng. |

# IV. PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN

## 1. Phiếu học tập số 1 (Đính kèm sản phẩm thực hành tại Thư viện)
**TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN TIN — THƯ VIỆN SỐ DLIBK12**  
*Lớp: 9/2 — Nhóm số: ...... — Ngày thực hiện: ...../11/2026*  

- **Phần 1: Luyện tập rút gọn căn thức (Khám phá trên DlibK12)**  
  1) Tính: $A = \\sqrt{20} \\cdot \\sqrt{45} = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  2) Tính: $B = \\sqrt{\\frac{25}{16}} : \\sqrt{\\frac{9}{64}} = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  3) Rút gọn biểu thức ($x \\ge 0$): $M = \\sqrt{18x} + \\sqrt{50x} - \\sqrt{72x} = \\dots\\dots\\dots\\dots\\dots$  

- **Phần 2: Bài toán thực tế Heron (Sản phẩm bàn giao Thư viện)**  
  Một khu đất tam giác trong khuôn viên trường có 3 cạnh là $a = 5\\text{ m}, b = 6\\text{ m}, c = 7\\text{ m}$.  
  + Nửa chu vi $p = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  + Diện tích khu đất $S = \\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots\\dots$  
  + Kết luận: $S \\approx \\dots\\dots\\dots\\dots\\dots\\text{ m}^2$.  

## 2. Sản phẩm học tập minh chứng hoàn chỉnh (Lưu hồ sơ Thư viện theo KH 115)
- **Đáp án phần 1:**  
  1) $A = \\sqrt{20 \\cdot 45} = \\sqrt{900} = 30$.  
  2) $B = \\frac{5}{4} : \\frac{3}{8} = \\frac{5}{4} \\cdot \\frac{8}{3} = \\frac{10}{3}$.  
  3) $M = 3\\sqrt{2x} + 5\\sqrt{2x} - 6\\sqrt{2x} = (3 + 5 - 6)\\sqrt{2x} = 2\\sqrt{2x}$.  
- **Đáp án phần 2:**  
  $p = 9\\text{ m} \\Rightarrow S = \\sqrt{9 \\cdot 4 \\cdot 3 \\cdot 2} = 6\\sqrt{6} \\approx 14.7\\text{ m}^2$.  
- **Tình trạng bàn giao:** Đã nộp 08 bản Phiếu học tập của 08 nhóm học sinh lớp 9/2 về bàn thủ thư lưu trữ.
"""

with open(os.path.join(out_dir, "KHBD_01_Hoang_Tan_Thien_Toan_9.md"), "w", encoding="utf-8") as f:
    f.write(md_01.strip())

print("Đã tạo xong KHBD 01 Markdown.")
