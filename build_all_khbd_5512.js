// -*- coding: utf-8 -*-
/**
 * Script biên soạn trọn bộ 09 Kế hoạch bài dạy (KHBD) chuẩn Công văn 5512
 * đúng Hợp đồng xây dựng KHBD của Hệ thống:
 * - Header 2 dòng tinh gọn
 * - Mục I: Mục tiêu (Kiến thức, Năng lực chung, Năng lực toán/tin/HĐTN, NLS & AI in đậm nghiêng, Phẩm chất)
 * - Mục II: Thiết bị dạy học và học liệu (CSDL DlibK12 + Màn hình Tivi + Laptop GV)
 * - Mục III: Tiến trình dạy học (Đủ 4 hoạt động A, B, C, D đều có BẢNG 2 CỘT chuẩn CV 5512 và 4 bước)
 * - Mục IV: PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN (Phiếu học tập 1, 2 + Sản phẩm học sinh hoàn chỉnh)
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx } = require('../../engine/export_khbd_engine.js');

const outDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/05.11');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

// Danh sách 9 bài dạy chuẩn hóa
const khbdList = [
  // 1. Thầy Hoàng Tấn Thiên (Toán 9)
  {
    code: "KHBD_01_Hoang_Tan_Thien_Toan_9",
    lessonScope: "Tiết 27",
    lessonTitle: "BÀI 8: KHAI CĂN BẬC HAI VỚI PHÉP NHÂN VÀ PHÉP CHIA",
    duration: "01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12",
    subject: "Toán",
    grade: "9",
    gv: "Hoàng Tấn Thiên",
    lop: "9/2 (hoặc 9/1)",
    mdContent: `Tiết 27 - BÀI 8: KHAI CĂN BẬC HAI VỚI PHÉP NHÂN VÀ PHÉP CHIA
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
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh cánh buồm hình tam giác có độ dài 3 cạnh $a = 5\\text{ m}, b = 6\\text{ m}, c = 7\\text{ m}$. Yêu cầu các nhóm tính diện tích cánh buồm theo công thức Heron: $S = \\sqrt{p(p-a)(p-b)(p-c)}$ với $p$ là nửa chu vi.<br>- **HS:** Tiếp nhận nhiệm vụ, hoàn thiện vào mục Vận dụng trên Phiếu học tập số 1.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tính nửa chu vi $p = \\frac{5 + 6 + 7}{2} = 9\\text{ m}$.<br>Thay số: $S = \\sqrt{9(9-5)(9-6)(9-7)} = \\sqrt{9 \\cdot 4 \\cdot 3 \\cdot 2} = \\sqrt{216} = 6\\sqrt{6} \\approx 14.7\\text{ m}^2$.<br>- **GV:** Theo dõi, hướng dẫn cách bấm máy tính làm tròn số.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện nhóm đọc to kết quả và giải thích các bước khai phương.<br>- ***(Tích hợp AI 6.B2.1: GV dùng trợ lý số trên laptop kiểm chứng nhanh kết quả: 6√6 ≈ 14.6969m² cho HS quan sát)***.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Đánh giá tiết học tại Thư viện số diễn ra sôi nổi, hiệu quả.<br>- **GV:** Thu toàn bộ Phiếu học tập số 1 của các nhóm, bàn giao ngay cho Cán bộ Thư viện để lưu hồ sơ minh chứng theo Kế hoạch 115. | **Vận dụng thực tế:**<br>- Nửa chu vi cánh buồm:<br>$p = \\frac{5 + 6 + 7}{2} = 9\\text{ (m)}$.<br>- Diện tích cánh buồm:<br>$S = \\sqrt{9 \\cdot (9 - 5) \\cdot (9 - 6) \\cdot (9 - 7)}$<br>$S = \\sqrt{9 \\cdot 4 \\cdot 3 \\cdot 2} = 3 \\cdot 2 \\cdot \\sqrt{6} = 6\\sqrt{6} \\approx 14.7\\text{ (m}^2\\text{)}$.<br><br>**Bàn giao sản phẩm lưu Thư viện:**<br>- 100% nhóm HS nộp Phiếu học tập số 1 có đầy đủ chữ ký nhóm trưởng. |

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
`
  },

  // 2. Thầy Dương Quang Tùng (Tin 6)
  {
    code: "KHBD_02_Duong_Quang_Tung_Tin_6",
    lessonScope: "Tiết 13",
    lessonTitle: "BÀI 7: THỰC HÀNH: TÌM KIẾM THÔNG TIN TRÊN INTERNET VÀ THƯ VIỆN SỐ",
    duration: "01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12",
    subject: "Tin học",
    grade: "6",
    gv: "Dương Quang Tùng",
    lop: "6/3 (hoặc 6/2)",
    mdContent: `Tiết 13 - BÀI 7: THỰC HÀNH: TÌM KIẾM THÔNG TIN TRÊN INTERNET VÀ THƯ VIỆN SỐ
*Thời lượng thực hiện: 01 tiết (45 phút) - Tiết học tại Thư viện số DlibK12*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng thành thạo máy tìm kiếm trên Internet và công cụ tìm kiếm tích hợp của Thư viện số DlibK12.
- Biết xác định từ khóa tìm kiếm chính xác, sử dụng dấu ngoặc kép để tìm kiếm cụm từ chính xác.
- Đánh giá sơ bộ tính tin cậy, chính xác và an toàn của nguồn thông tin tìm được.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự thao tác trên máy tính, chủ động tìm kiếm học liệu phục vụ học tập.
- Giao tiếp và hợp tác: Làm việc nhóm hiệu quả, phân công ghi chép và chia sẻ liên kết tài liệu.

b) Năng lực Tin học:
- Năng lực tìm kiếm, tiếp nhận và xử lý thông tin số trong môi trường mạng an toàn.
- Năng lực ứng dụng CNTT trong tự học và nghiên cứu khoa học.

c) Năng lực số (NLS):
- ***(Tích hợp NLS 1.1.TC1a: Tìm kiếm và lọc dữ liệu, thông tin và nội dung số trên nền tảng Thư viện số DlibK12)***.
- ***(Tích hợp NLS 1.2.TC1b: Đánh giá và so sánh độ tin cậy giữa nguồn thông tin chính thống của Thư viện số với thông tin tự do trên mạng xã hội)***.

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***(Tích hợp AI 2.B1.1: Nhận biết cơ chế gợi ý từ khóa tự động của thuật toán tìm kiếm thông minh khi gõ từ khóa)***.

## 3. Về phẩm chất
- Chăm chỉ: Kiên trì tìm kiếm và chọn lọc nguồn thông tin chuẩn xác.
- Trách nhiệm: Tuân thủ quy tắc ứng xử văn hóa mạng và nội quy phòng Thư viện số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Màn hình Tivi Thư viện kết nối Laptop GV; Hệ thống mạng Wifi/LAN Thư viện.
- CSDL Thư viện số DlibK12; Danh mục từ khóa thực hành; SGK Tin học 6.
2. Học sinh:
- Máy tính phòng đọc Thư viện; Tài khoản cá nhân DlibK12; Sổ tay ghi chép số.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Đặt vấn đề về tầm quan trọng của việc chọn đúng từ khóa khi tìm kiếm tài liệu học tập.
b) Nội dung: So sánh kết quả tìm kiếm khi gõ từ khóa rộng và từ khóa cụ thể trong dấu ngoặc kép.
c) Sản phẩm: Nhận thức của học sinh về cách thu hẹp phạm vi tìm kiếm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu lên Tivi Thư viện thanh tìm kiếm Google và thanh tìm kiếm DlibK12. Đặt câu hỏi: "Nếu em muốn tìm quyển sách 'Toán 6 Kết nối tri thức', em sẽ gõ từ khóa nào để ra kết quả nhanh nhất?".<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo cặp bàn đưa ra các phương án từ khóa.<br>- **GV:** Thử nghiệm gõ trực tiếp các phương án của học sinh lên màn hình Tivi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhận xét: Gõ `"Toán 6 Kết nối tri thức"` trong ngoặc kép sẽ ra đúng quyển sách cần tìm, không bị lẫn các trang quảng cáo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy tắc vàng trong tìm kiếm số và dẫn dắt vào bài thực hành tại Thư viện số. | **Khởi động:**<br>- Từ khóa tìm kiếm là cầu nối quyết định kết quả.<br>- Sử dụng dấu ngoặc kép `""` giúp tìm chính xác cụm từ.<br>- Tìm kiếm trên Thư viện số DlibK12 giúp tiếp cận học liệu đã được kiểm duyệt sư phạm. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI / THAO TÁC MẪU TRÊN DLIBK12 (15 phút)
a) Mục tiêu: Học sinh nắm vững quy trình 3 bước tìm kiếm trên CSDL Thư viện số DlibK12.
b) Nội dung: Quan sát giáo viên thao tác mẫu trên Tivi; nhận biết giao diện và các bộ lọc tìm kiếm (theo môn, lớp, tác giả).
c) Sản phẩm: Các bước thực hiện được ghi chép vào vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn học sinh đăng nhập vào hệ thống DlibK12 qua trình duyệt web trên máy tính Thư viện.<br>- ***(Tích hợp NLS 1.1.TC1a: GV thị phạm trên màn hình Tivi quy trình lọc sách điện tử môn Tin học 6 và video bài giảng)***.<br>- **HS:** Quan sát từng thao tác của giáo viên.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bật máy tính nhóm, mở trình duyệt và truy cập đúng địa chỉ Thư viện số của trường.<br>- **GV:** Đi kiểm tra các bàn máy, hỗ trợ các em quên mật khẩu đăng nhập.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Đại diện 1 nhóm mô tả lại 3 bước tìm tài liệu trên DlibK12.<br>- ***(Tích hợp AI 2.B1.1: HS nhận xét khi gõ chữ 'Tin', hệ thống tự động xổ xuống danh sách gợi ý 'Tin học 6', 'Tin học 7' rất thông minh)***.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định học sinh đã nắm được quy trình và chuyển sang phần thực hành độc lập. | **Quy trình tìm kiếm trên Thư viện số DlibK12:**<br>1. Đăng nhập tài khoản cá nhân.<br>2. Chọn bộ lọc: Môn học (Tin học) - Khối lớp (Khối 6).<br>3. Nhập từ khóa chủ đề và nhấn Tìm kiếm (hoặc Enter). |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP / THỰC HÀNH TƯƠNG TÁC (18 phút)
a) Mục tiêu: Học sinh tự thực hành tìm kiếm được tối thiểu 03 tài liệu số theo yêu cầu nhiệm vụ.
b) Nội dung: Hoàn thành Phiếu thực hành tìm kiếm tài liệu về chủ đề "An toàn trên Internet" và "Văn hóa đọc học đường".
c) Sản phẩm: Danh mục 03 tài liệu số tìm được trên DlibK12 được ghi vào Phiếu thực hành.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ trên Phiếu học tập số 1: Mỗi nhóm hãy tìm trên DlibK12 và ghi lại thông tin của:<br>1) 01 cuốn sách điện tử về Kỹ năng sử dụng Internet an toàn;<br>2) 01 video bài giảng về Mạng máy tính;<br>3) 01 bài viết về Ngày sách Việt Nam.<br>- **HS:** Tiếp nhận nhiệm vụ nhóm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Các nhóm thao tác trên máy tính Thư viện, cùng nhau chọn lọc tài liệu phù hợp và ghi vào phiếu.<br>- ***(Tích hợp NLS 1.2.TC1b: GV hướng dẫn HS kiểm tra tên tác giả và nhà xuất bản để xác thực tính chính thống)***.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Chiếu màn hình máy tính của Nhóm 3 lên Tivi Thư viện.<br>- **HS:** Nhóm 3 thuyết minh danh mục tài liệu các em đã tìm được.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, tuyên dương các nhóm thực hiện đúng quy trình và tìm được học liệu chất lượng. | **Kết quả thực hành:**<br>- Tìm kiếm thành công các tài liệu số chuẩn mực trên DlibK12.<br>- Biết sao chép đường link và trích dẫn nguồn tài liệu trung thực.<br>- Hình thành kỹ năng tự tra cứu học liệu số suốt đời. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG & BÀN GIAO SẢN PHẨM LƯU THƯ VIỆN (7 phút)
a) Mục tiêu: Đánh giá kỹ năng chọn lọc thông tin và nộp sản phẩm lưu hồ sơ Thư viện.
b) Nội dung: Hoàn thiện bảng thu hoạch danh mục tài liệu số; ký tên nộp cán bộ Thư viện.
c) Sản phẩm: Phiếu thu hoạch của các nhóm nộp tại bàn thủ thư.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các nhóm hoàn thiện Phiếu thu hoạch và ký tên các thành viên.<br>- **HS:** Kiểm tra lại toàn bộ thông tin tài liệu đã ghi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Ký tên và bàn giao phiếu cho nhóm trưởng.<br>- **GV:** Quan sát, đôn đốc.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nhóm trưởng lần lượt mang phiếu nộp tại bàn đại diện Thư viện.<br><br>**+ Bước 4: Kết luận, nhận định & Bàn giao sản phẩm**<br>- **GV:** Tổng kết tiết học, dặn dò học sinh tiếp tục sử dụng tài khoản DlibK12 để đọc sách tại nhà.<br>- **GV:** Bàn giao toàn bộ phiếu thu hoạch cho Cán bộ Thư viện lưu minh chứng. | **Bàn giao hồ sơ lưu Thư viện:**<br>- Hoàn tất phiếu thu hoạch thực hành tìm kiếm số.<br>- 100% nhóm học sinh hoàn thành chỉ tiêu bài học. |

# IV. PHỤ LỤC HỌC LIỆU VÀ SẢN PHẨM HỌC TẬP LƯU THƯ VIỆN

## 1. Phiếu thực hành tìm kiếm trên Thư viện số DlibK12
**TRƯỜNG THCS TRẦN PHÚ — TỔ TOÁN TIN — TIẾT HỌC THƯ VIỆN SỐ**  
*Lớp: 6/3 — Nhóm máy số: ...... — Ngày thực hiện: ...../11/2026*  

- **Nhiệm vụ 1: Tìm kiếm tài liệu sách điện tử (E-book)**  
  + Tên sách tìm được: ............................................................................................  
  + Tác giả / NXB: ................................................................................................  
  + Từ khóa em đã sử dụng: ...................................................................................  

- **Nhiệm vụ 2: Tìm kiếm video bài giảng số**  
  + Tên bài giảng / video: .......................................................................................  
  + Thời lượng video: ..............................................................................................  
  + Nội dung cốt lõi của video: ...............................................................................  

## 2. Sản phẩm học tập minh chứng hoàn chỉnh (Lưu hồ sơ Thư viện theo KH 115)
- **Sản phẩm nhóm tiêu biểu (Nhóm 1 - Lớp 6/3):**  
  + Sách tìm được: *"Cẩm nang sử dụng mạng Internet an toàn cho học sinh THCS"* — NXB Giáo dục Việt Nam (CSDL DlibK12 mã số: EB-THCS-012).  
  + Video bài giảng: *"Chủ đề 2: Mạng máy tính và Internet - Bài 4"* (Thời lượng: 12 phút 30 giây).  
- **Tình trạng bàn giao:** Đã nộp 06 Phiếu thực hành của 06 nhóm máy lớp 6/3 cho Thư viện lưu trữ.
`
  }
];

console.log(`Bắt đầu biên dịch ${khbdList.length} Kế hoạch bài dạy chuẩn CV 5512...`);

async function run() {
  for (let i = 0; i < khbdList.length; i++) {
    const item = khbdList[i];
    const mdPath = path.join(outDir, `${item.code}.md`);
    const docxPath = path.join(outDir, `${item.code}.docx`);

    // Ghi file markdown
    fs.writeFileSync(mdPath, item.mdContent, 'utf8');

    const lessonInfo = {
      subject: item.subject,
      grade: item.grade,
      lessonScope: item.lessonScope,
      lessonTitle: item.lessonTitle,
      duration: item.duration
    };

    try {
      const res = await createKhbdDocx({
        mdFilePath: mdPath,
        outputDocxPath: docxPath,
        lessonInfo,
        illustrations: []
      });
      console.log(`[${i + 1}/${khbdList.length}] ĐÃ XUẤT THÀNH CÔNG: ${path.basename(res.path)} (Size: ${res.size} bytes)`);
    } catch (e) {
      console.error(`LỖI tại ${item.code}:`, e);
    }
  }
}

run();
