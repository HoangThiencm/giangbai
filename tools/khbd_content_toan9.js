// -*- coding: utf-8 -*-
/**
 * Nội dung Kế hoạch bài dạy (KHBD) Chuẩn Công văn 5512 V2.0 cho Môn Toán 9 - Chương II
 * TUÂN THỦ TUYỆT ĐỐI QUY CHUẨN SƯ PHẠM CẤP THCS (GDPT 2018):
 * - CẤM dùng dấu tương đương (<=>, ⇔, \Leftrightarrow) và các ký hiệu hình thức Cấp 3.
 * - CẤM kết luận "tập nghiệm là S = {...}".
 * - Các bước giải phương trình, bất phương trình viết liên tiếp từng dòng độc lập (hoặc dùng từ nối "hay", "suy ra", "do đó", "hoặc").
 * - Kết luận chuẩn SGK THCS: "Vậy phương trình có nghiệm là...", "Vậy nghiệm của bất phương trình là...".
 */

const BAI_01_MD = `# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 9**  
**CHỦ ĐỀ: BÀI 5. BẤT ĐẲNG THỨC VÀ TÍNH CHẤT (3 TIẾT)**  
**Phân phối chương trình:** Tiết 15, 16, 17 — Tuần 5, 6  
**Thời lượng thực hiện:** 03 tiết (135 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 31 – 35)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Nhận biết khái niệm bất đẳng thức (vế trái, vế phải, bất đẳng thức cùng chiều, ngược chiều).
- Hiểu và vận dụng thành thạo các tính chất cơ bản của bất đẳng thức: tính chất bắc cầu, liên hệ giữa thứ tự và phép cộng, liên hệ giữa thứ tự và phép nhân (với số dương và với số âm).

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự giác đọc hiểu SGK, hoàn thành các phiếu học tập cá nhân và hệ thống hóa các tính chất của bất đẳng thức.
- Giao tiếp và hợp tác: Chủ động trao đổi, thảo luận nhóm để so sánh các biểu thức và giải thích quy tắc đổi chiều khi nhân với số âm.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: So sánh các số thực, phân tích mối quan hệ giữa thứ tự và phép toán để suy luận tính đúng đắn của bất đẳng thức.
- Giải quyết vấn đề toán học: Vận dụng bất đẳng thức để mô tả và giải quyết các tình huống thực tiễn như giới hạn tốc độ xe cộ, dự toán ngân sách chi tiêu.

## 3. Về phẩm chất
- Chăm chỉ: Tích cực phát biểu, kiên trì tính toán và lập luận cẩn thận từng bước biến đổi.
- Trách nhiệm: Tự giác kiểm tra lại kết quả bài làm, tuân thủ đúng quy tắc dấu khi nhân chia số âm.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài trình chiếu PowerPoint, tivi/máy chiếu, hình ảnh biển báo giao thông (Hình 2.3, 2.4 SGK), phiếu học tập, thước thẳng.
2. **Học sinh:** SGK Toán 9 (Tập 1), vở ghi, đồ dùng học tập: bút, thước kẻ, máy tính cầm tay.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (10 phút)

#### a) Mục tiêu:
- Gợi mở nhu cầu so sánh và thiết lập mối quan hệ thứ tự trong thực tế; tạo tâm thế hứng thú khám phá khái niệm bất đẳng thức thông qua biển báo giao thông.

#### b) Nội dung:
- Quan sát Hình 2.3 SGK trang 31 (biển báo tốc độ tối đa cho phép trên từng làn đường) và thảo luận về cách biểu thị toán học.

#### c) Sản phẩm:
- Câu trả lời của HS: Tốc độ ô tô làn giữa không vượt quá 50 km/h ($v \\le 50$), xe máy làn phải không vượt quá 50 km/h ($v \\le 50$), làn trái tối đa 60 km/h ($v \\le 60$).

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu Hình 2.3 SGK và đặt vấn đề: "Khi tham gia giao thông trên đường cao tốc hoặc quốc lộ, chúng ta thường gặp biển báo giới hạn tốc độ cho từng làn đường. Em hiểu thế nào về các con số 60, 50 trên biển báo? Trong Toán học, ta dùng kí hiệu nào để diễn tả vận tốc xe $v$ không được vượt quá con số đó?"<br>- **HS:** Quan sát hình ảnh và lắng nghe câu hỏi.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thảo luận nhanh theo cặp bàn (1 phút).<br>- **GV:** Bao quát lớp, gợi ý liên hệ với các kí hiệu so sánh đã học ở lớp dưới.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện phát biểu: "Kí hiệu 60 nghĩa là xe chạy tối đa 60 km/h, tức là vận tốc $v \\le 60$. Kí hiệu 50 nghĩa là $v \\le 50$."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét câu trả lời, chuẩn hóa: Các hệ thức như $v \\le 60, v \\le 50$ được gọi là các bất đẳng thức. Bài học hôm nay sẽ giúp chúng ta tìm hiểu sâu hơn về khái niệm và tính chất của chúng. | **TÌNH HUỐNG MỞ ĐẦU:**<br><br>- Quan sát biển báo Hình 2.3:<br>+ Làn ngoài cùng bên trái: Giới hạn tốc độ tối đa 60 km/h nên $v \\le 60$.<br>+ Làn giữa và làn phải: Giới hạn tốc độ tối đa 50 km/h nên $v \\le 50$.<br><br>Các hệ thức $v \\le 60, v \\le 50$ là các **bất đẳng thức**. |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (70 phút)

### 1. Hoạt động 2.1: Bất đẳng thức (Tiết 15: 25 phút)

#### a) Mục tiêu:
- Nhận biết thứ tự trên tập số thực, khái niệm bất đẳng thức (vế trái, vế phải, cùng chiều, ngược chiều) và tính chất bắc cầu.

#### b) Nội dung:
- Nhắc lại thứ tự trên $\\mathbb{R}$, làm phần ?, Luyện tập 1, Ví dụ 1, Ví dụ 2, Ví dụ 3, Luyện tập 2 và Vận dụng 1 trong SGK trang 31 – 33.

#### c) Sản phẩm:
- Kết quả điền dấu trong phần ?; đáp án Luyện tập 1 ($a \\ge 60$); xác định vế trái, vế phải Ví dụ 1; viết BĐT Ví dụ 2; lời giải Luyện tập 2 và Vận dụng 1.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Yêu cầu HS nhắc lại: Trên tập số thực $\\mathbb{R}$, với hai số $a, b$ bất kì có những trường hợp so sánh nào? Điền dấu $=, >, <$ thích hợp vào dấu ? ở SGK trang 31.<br>- **GV:** Cho HS làm Luyện tập 1 về biển báo tốc độ tối thiểu R.306.<br>- **GV:** Nêu định nghĩa bất đẳng thức, vế trái, vế phải; chú ý về BĐT cùng chiều, ngược chiều.<br>- **GV:** Giới thiệu tính chất bắc cầu và hướng dẫn Ví dụ 3.<br>- **HS:** Tiếp nhận nhiệm vụ, đọc SGK.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thực hiện cá nhân điền dấu ?; làm Luyện tập 1, Ví dụ 1, 2 và thảo luận Luyện tập 2.<br>- **GV:** Theo dõi, hướng dẫn HS cách so sánh phân số qua số trung gian ở Ví dụ 3 và Luyện tập 2.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Báo cáo kết quả ?:<br>a) $-34,2 < -27$; b) $\\frac{6}{-8} = -\\frac{3}{4}$; c) $2024 > 1954$.<br>- **HS:** Luyện tập 1: Đáp án C ($a \\ge 60$).<br>- **HS:** Luyện tập 2: Ta có $\\frac{2024}{1000} = 2,024 > 2 > 1,9$ nên $\\frac{2024}{1000} > 1,9$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chốt lại: Bất đẳng thức là hệ thức dạng $a < b, a > b, a \\le b, a \\ge b$. Tính chất bắc cầu: Khi có $a < b$ và $b < c$ thì suy ra $a < c$. | **1. BẤT ĐẲNG THỨC:**<br><br>**a) Thứ tự trên tập số thực:**<br>- Với hai số thực $a, b$, ta có: $a = b$ hoặc $a > b$ hoặc $a < b$.<br>- Khi $a > b$ hoặc $a = b$, ta viết $a \\ge b$.<br>- Khi $a < b$ hoặc $a = b$, ta viết $a \\le b$.<br><br>**b) Khái niệm bất đẳng thức:**<br>- Hệ thức dạng $a > b$ (hay $a < b, a \\ge b, a \\le b$) được gọi là **bất đẳng thức**.<br>- $a$ là **vế trái**, $b$ là **vế phải**.<br>- $a < b$ và $c < d$ là hai BĐT **cùng chiều**.<br>- $a < b$ và $c > d$ là hai BĐT **ngược chiều**.<br><br>**c) Tính chất bắc cầu:**<br>Nếu $a < b$ và $b < c$ thì $a < c$.<br>*(Tương tự cho các thứ tự $>, \\le, \\ge$).*<br><br>**Luyện tập 2 (trang 33):**<br>a) Ta có $\\frac{2024}{1000} = 2,024$. Vì $2,024 > 2$ và $2 > 1,9$ nên $\\frac{2024}{1000} > 1,9$.<br>b) Ta có $\\frac{2022}{2023} > 0$ và $0 > -1,1$ nên $\\frac{2022}{2023} > -1,1$. |

---

### 2. Hoạt động 2.2: Liên hệ giữa thứ tự và phép cộng (Tiết 16: 20 phút)

#### a) Mục tiêu:
- Học sinh phát hiện và phát biểu được tính chất liên hệ giữa thứ tự và phép cộng; biết vận dụng để so sánh các biểu thức mà không cần tính giá trị cụ thể.

#### b) Nội dung:
- Thực hiện HĐ1 SGK trang 33, rút ra kết luận tính chất và làm Ví dụ 4, Luyện tập 3 SGK trang 33 – 34.

#### c) Sản phẩm:
- Kết quả HĐ1; phát biểu tính chất: Khi cộng cùng một số vào cả hai vế của BĐT thì được BĐT mới cùng chiều; lời giải Ví dụ 4 và Luyện tập 3.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Yêu cầu HS thực hiện HĐ1 SGK trang 33:<br>Xét BĐT $-1 < 2$.<br>a) Cộng 2 vào hai vế và so sánh.<br>b) Cộng $-2$ vào hai vế và so sánh.<br>c) Dự đoán khi cộng số thực $c$ bất kì vào hai vế?<br>- **HS:** Đọc yêu cầu và làm ra nháp.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tính: $-1 + 2 = 1$; $2 + 2 = 4$, ta được $1 < 4$.<br>$-1 + (-2) = -3$; $2 + (-2) = 0$, ta được $-3 < 0$.<br>- **GV:** Nhận xét: Chiều của BĐT có thay đổi không?<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Rút ra nhận xét: Cả hai trường hợp BĐT mới đều giữ nguyên chiều nhỏ hơn ($<$). Khi cộng số $c$ bất kì thì $-1 + c < 2 + c$.<br>- **HS:** Áp dụng làm Luyện tập 3 vào vở.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa tính chất: Khi cộng cùng một số vào hai vế của một bất đẳng thức ta được bất đẳng thức mới cùng chiều với bất đẳng thức đã cho. | **2. LIÊN HỆ GIỮA THỨ TỰ VÀ PHÉP CỘNG:**<br><br>**Tính chất:**<br>Với ba số $a, b, c$, ta có:<br>- Nếu $a < b$ thì $a + c < b + c$.<br>- Nếu $a \\le b$ thì $a + c \\le b + c$.<br>- Nếu $a > b$ thì $a + c > b + c$.<br>- Nếu $a \\ge b$ thì $a + c \\ge b + c$.<br><br>*(Khi cộng cùng một số vào hai vế của một BĐT, ta được BĐT mới **cùng chiều** với BĐT đã cho).*<br><br>**Luyện tập 3 (trang 34):**<br>a) Vì $19 > -31$, cộng $2023$ vào hai vế ta được:<br>$19 + 2023 > -31 + 2023$.<br>b) Ta có $2 < 4$ nên $\\sqrt{2} < 2$.<br>Cộng 2 vào hai vế ta được: $\\sqrt{2} + 2 < 2 + 2 = 4$. |

---

### 3. Hoạt động 2.3: Liên hệ giữa thứ tự và phép nhân (Tiết 16 – 17: 25 phút)

#### a) Mục tiêu:
- Học sinh phân biệt được quy tắc nhân cả hai vế của BĐT với số dương (giữ nguyên chiều) và nhân với số âm (đổi chiều BĐT); biết áp dụng linh hoạt vào so sánh số.

#### b) Nội dung:
- Thực hiện HĐ2 SGK trang 34; rút ra tính chất; làm Ví dụ 5, Luyện tập 4 SGK trang 34 – 35.

#### c) Sản phẩm:
- Kết quả HĐ2; quy tắc nhân với số dương và số âm; đáp án Ví dụ 5 và Luyện tập 4.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Cho BĐT $-2 < 5$. Yêu cầu HS:<br>a) Nhân hai vế với số dương 7.<br>b) Nhân hai vế với số âm $-7$.<br>So sánh chiều của BĐT nhận được với chiều ban đầu.<br>- **HS:** Nhận nhiệm vụ và tính toán ra nháp.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tính:<br>a) $(-2) \\cdot 7 = -14$; $5 \\cdot 7 = 35$, ta có $-14 < 35$ (cùng chiều).<br>b) $(-2) \\cdot (-7) = 14$; $5 \\cdot (-7) = -35$, ta có $14 > -35$ (ngược chiều).<br>- **GV:** Lưu ý học sinh: "Khi nhân với số âm, chiều của BĐT bị ĐỔI NGƯỢC."<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Phát biểu quy tắc nhân với số dương và số âm.<br>- **HS:** Thực hiện Luyện tập 4: Điền dấu thích hợp.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chốt kiến thức: Nhân số dương $\\rightarrow$ cùng chiều; Nhân số âm $\\rightarrow$ ngược chiều (đổi chiều). Phép chia cho số khác 0 cũng tương tự phép nhân với số nghịch đảo. | **3. LIÊN HỆ GIỮA THỨ TỰ VÀ PHÉP NHÂN:**<br><br>**a) Nhân với số dương ($c > 0$):**<br>- Nếu $a < b$ thì $ac < bc$.<br>- Nếu $a > b$ thì $ac > bc$.<br>*(Được BĐT mới **cùng chiều**).*<br><br>**b) Nhân với số âm ($c < 0$):**<br>- Nếu $a < b$ thì $ac > bc$.<br>- Nếu $a > b$ thì $ac < bc$.<br>*(Được BĐT mới **ngược chiều** - đổi chiều).*<br><br>**Luyện tập 4 (trang 35):**<br>a) Vì $-10,5 < 11,2$ và $13 > 0$ nên:<br>$13 \\cdot (-10,5) < 13 \\cdot 11,2$.<br>b) Vì $-10,5 < 11,2$ và $-13 < 0$ nên:<br>$(-13) \\cdot (-10,5) > (-13) \\cdot 11,2$. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (40 phút)

#### a) Mục tiêu:
- Củng cố và rèn luyện thành thạo kỹ năng viết BĐT, so sánh biểu thức số và biến, chứng minh BĐT đơn giản bằng các tính chất đã học.

#### b) Nội dung:
- Hoàn thành các bài tập trong SGK trang 35: Bài 2.6, 2.7, 2.8, 2.9, 2.10, 2.11.

#### c) Sản phẩm:
- Lời giải chi tiết của học sinh vào vở cho các bài tập 2.6 đến 2.11.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Chia nhiệm vụ luyện tập:<br>+ Bài 2.6 & 2.7: Làm việc cá nhân (5 phút).<br>+ Bài 2.8 & 2.9: Hoạt động cặp đôi (7 phút).<br>+ Bài 2.10 & 2.11: Hoạt động nhóm 4 HS (8 phút).<br>- **HS:** Nhận nhiệm vụ, mở SGK trang 35.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tự giác làm bài, trao đổi thảo luận nhóm khi gặp khó khăn.<br>- **GV:** Đi vòng quanh lớp quan sát, hỗ trợ giải thích quy tắc bắc cầu cho Bài 2.11.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Gọi đại diện các nhóm lên bảng trình bày.<br>- **HS:** Nhận xét, đối chiếu lời giải của bạn.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa các bước giải, đặc biệt nhấn mạnh kỹ năng sử dụng tính chất bắc cầu: Muốn so sánh hai số khó so sánh trực tiếp, ta so sánh từng số với một số trung gian thích hợp (số 1 hoặc 0). | **BÀI TẬP SGK TRANG 35:**<br><br>**1. Bài 2.6:**<br>a) $x \\le -2$; b) $m < 0$; c) $y > 0$; d) $p \\ge 2024$.<br><br>**2. Bài 2.7:**<br>a) Gọi tuổi là $x$, ta có $x \\ge 18$.<br>b) Gọi số người là $n$, ta có $n \\le 45$.<br>c) Gọi mức lương là $m$, ta có $m \\ge 20\\,000$ (đồng).<br><br>**3. Bài 2.8:**<br>a) Vì $-7 < -1$ và $2 > 0$ nên $2 \\cdot (-7) < 2 \\cdot (-1)$.<br>Cộng 2023 vào hai vế ta được: $2 \\cdot (-7) + 2023 < 2 \\cdot (-1) + 2023$.<br>b) Vì $-8 < -7$ và $-3 < 0$ nên $(-3) \\cdot (-8) > (-3) \\cdot (-7)$.<br>Cộng 1975 vào hai vế ta được: $(-3) \\cdot (-8) + 1975 > (-3) \\cdot (-7) + 1975$.<br><br>**4. Bài 2.9 (Cho $a < b$):**<br>a) Nhân hai vế với 5 ta được $5a < 5b$. Cộng 7 vào hai vế ta được $5a + 7 < 5b + 7$.<br>b) Nhân hai vế với $-3$ ta được $-3a > -3b$. Cộng $-9$ vào hai vế ta được $-3a - 9 > -3b - 9$.<br><br>**5. Bài 2.10:**<br>a) Ta có $a + 1954 < b + 1954$. Trừ cả hai vế cho 1954 ta được $a < b$.<br>b) Ta có $-2a > -2b$. Chia cả hai vế cho $-2 < 0$ (đổi chiều) ta được $a < b$.<br><br>**6. Bài 2.11:**<br>a) Ta có $\\frac{2023}{2024} < 1$ và $\\frac{2024}{2023} > 1$. Theo tính chất bắc cầu, ta có $\\frac{2023}{2024} < \\frac{2024}{2023}$.<br>b) Ta có $\\frac{34}{11} > 3$ và $\\frac{26}{9} < 3$. Theo tính chất bắc cầu, ta có $\\frac{34}{11} > \\frac{26}{9}$. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)

#### a) Mục tiêu:
- Vận dụng bất đẳng thức để giải bài toán thực tế về dự toán kinh phí cho hoạt động tập thể (Vận dụng 2 SGK trang 35).
- Định hướng tự học và chuẩn bị bài mới.

#### b) Nội dung:
- Giải bài toán Vận dụng 2 SGK trang 35.

#### c) Sản phẩm:
- Lời giải bài toán: Lập bất đẳng thức chi phí và tìm ra số bạn học sinh tối đa có thể tham gia chuyến dã ngoại là 86 bạn.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu bài toán Vận dụng 2 SGK trang 35:<br>"Nhà tài trợ dự kiến 30 triệu đồng cho chuyến dã ngoại. Chi phí thuê dịch vụ và phòng nghỉ cố định là 17 triệu đồng. Mỗi suất ăn gồm trưa (60 000 đ), tối (60 000 đ), sáng hôm sau (30 000 đ). Hỏi có thể tổ chức cho nhiều nhất bao nhiêu bạn tham gia?"<br>- **HS:** Đọc kỹ đề bài, xác định chi phí cố định và chi phí phát sinh theo số người.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Gọi $x$ là số bạn học sinh ($x \\in \\mathbb{N}^*$).<br>Tính tiền ăn của 1 bạn: $60\\,000 + 60\\,000 + 30\\,000 = 150\\,000$ đồng.<br>Thiết lập BĐT tổng chi phí $\\le 30\\,000\\,000$.<br>- **GV:** Hướng dẫn giải BĐT tìm $x$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày lời giải:<br>$17\\,000\\,000 + 150\\,000x \\le 30\\,000\\,000$<br>Trừ 17 triệu vào hai vế:<br>$150\\,000x \\le 13\\,000\\,000$<br>Chia hai vế cho 150 000:<br>$x \\le 86,67$.<br>Vì $x$ là số tự nhiên nên $x \\le 86$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khen ngợi học sinh đã lập luận chính xác. Chốt lại: Trong thực tế, các bài toán về ngân sách, kinh phí luôn được mô hình hóa bằng các bất đẳng thức. | **VẬN DỤNG 2 (SGK TRANG 35):**<br><br>- Tiền ăn cho mỗi bạn trong 1 ngày là:<br>$60\\,000 + 60\\,000 + 30\\,000 = 150\\,000$ (đồng).<br><br>- Gọi $x$ là số bạn học sinh tham gia ($x \\in \\mathbb{N}^*$).<br>- Tổng chi phí cho chuyến đi là:<br>$17\\,000\\,000 + 150\\,000 \\cdot x$ (đồng).<br><br>- Vì tổng kinh phí tài trợ tối đa là 30 triệu đồng nên ta có bất đẳng thức:<br>$17\\,000\\,000 + 150\\,000x \\le 30\\,000\\,000$<br>$150\\,000x \\le 13\\,000\\,000$<br>$x \\le \\frac{13\\,000\\,000}{150\\,000} \\approx 86,67$.<br><br>Do số người là số tự nhiên nên số bạn tham gia nhiều nhất là 86.<br><br>**Kết luận:** Có thể tổ chức cho **nhiều nhất 86 bạn** tham gia chuyến đi dã ngoại.<br><br>**HƯỚNG DẪN TỰ HỌC:**<br>- Ghi nhớ 3 tính chất cơ bản của BĐT (bắc cầu, liên hệ với phép cộng, liên hệ với phép nhân).<br>- Chuẩn bị bài Tiết 18: Luyện tập chung. |
`;

const BAI_02_MD = `# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 9**  
**CHỦ ĐỀ: BÀI 5. BẤT ĐẲNG THỨC VÀ TÍNH CHẤT (TIẾT 18: LUYỆN TẬP CHUNG)**  
**Phân phối chương trình:** Tiết 18 — Tuần 6  
**Thời lượng thực hiện:** 01 tiết (45 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 36 – 37)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Củng cố và hệ thống hóa toàn bộ kiến thức về bất đẳng thức và các tính chất liên hệ với phép cộng, phép nhân, tính chất bắc cầu.
- Rèn luyện kỹ năng chứng minh bất đẳng thức bằng cách phối hợp nhiều tính chất, giải các phương trình tích và phương trình chứa ẩn ở mẫu đưa về bậc nhất theo đúng phương pháp đại số THCS.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự giác sơ đồ hóa kiến thức lý thuyết thông qua Sơ đồ tư duy trực quan, độc lập tư duy tìm hướng biến đổi bất đẳng thức.
- Giao tiếp và hợp tác: Tích cực thảo luận cặp đôi để tìm giải pháp chứng minh qua số trung gian và phản biện lời giải của bạn.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: Phân tích cấu trúc hai vế bất đẳng thức, chọn nhân tử và số hạng cộng thích hợp để tạo ra bất đẳng thức trung gian chuẩn xác.
- Giải quyết vấn đề toán học: Vận dụng kiến thức phương trình và bất đẳng thức vào bài toán nồng độ, môi trường sinh thái (Bài 2.13).

## 3. Về phẩm chất
- Chăm chỉ: Kiên trì suy luận logic, cẩn thận kiểm tra điều kiện xác định và dấu của các phép biến đổi.
- Trách nhiệm: Tôn trọng ý kiến bạn cùng nhóm, có ý thức bảo vệ môi trường thông qua bài toán thực tế hồ nước.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài giảng điện tử, Sơ đồ tư duy Bất đẳng thức và tính chất, tivi/máy chiếu, phiếu học tập rèn luyện kỹ năng chứng minh BĐT.
2. **Học sinh:** SGK Toán 9 (Tập 1), vở ghi, đồ dùng học tập: bút, thước kẻ, nháp.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)

#### a) Mục tiêu:
- Tái hiện nhanh các tính chất cơ bản của bất đẳng thức; tạo tâm thế sẵn sàng bước vào tiết luyện tập chuyên sâu.

#### b) Nội dung:
- Trả lời nhanh câu hỏi nhắc lại quy tắc nhân và cộng hai vế của bất đẳng thức.

#### c) Sản phẩm:
- Câu trả lời của HS: Nhân với số dương thì cùng chiều, nhân với số âm thì đổi chiều, cộng cùng một số thì giữ nguyên chiều.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu câu hỏi: "Khi nhân cả hai vế của một bất đẳng thức với cùng một số, khi nào bất đẳng thức giữ nguyên chiều và khi nào đổi chiều? Cho ví dụ minh họa."<br>- **HS:** Lắng nghe và suy nghĩ câu trả lời.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhớ lại kiến thức bài trước, giơ tay phát biểu.<br>- **GV:** Mời 1 học sinh trả lời miệng.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** "Khi nhân với số dương thì BĐT mới cùng chiều với BĐT đã cho. Khi nhân với số âm thì BĐT mới ngược chiều (đổi chiều) với BĐT đã cho. Ví dụ: $2 < 3$, nhân với 4 được $2 \\cdot 4 < 3 \\cdot 4$; nhưng nhân với $-4$ thì $2 \\cdot (-4) > 3 \\cdot (-4)$."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khen ngợi câu trả lời chính xác, rõ ràng và dẫn dắt vào bài học Luyện tập chung. | **ÔN TẬP ĐẦU GIỜ:**<br><br>- **Quy tắc cộng:** Nếu $a < b$ thì $a + c < b + c$.<br>- **Quy tắc nhân:**<br>+ Với $c > 0$: Nếu $a < b$ thì $ac < bc$.<br>+ Với $c < 0$: Nếu $a < b$ thì $ac > bc$ (đổi chiều).<br>- **Tính chất bắc cầu:** Nếu $a < b$ và $b < c$ thì $a < c$. |

---

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức (10 phút)

#### a) Mục tiêu:
- Khắc sâu bức tranh toàn cảnh về Bất đẳng thức và tính chất thông qua Sơ đồ tư duy trực quan; phân tích kỹ thuật chứng minh BĐT qua Ví dụ 3 SGK trang 37.

#### b) Nội dung:
- Quan sát và hệ thống hóa kiến thức thông qua Sơ đồ tư duy: Bất đẳng thức và các tính chất cơ bản.
- Phân tích và thực hiện kỹ thuật chứng minh qua số trung gian ở Ví dụ 3 (SGK trang 37).

![Sơ đồ tư duy Bất đẳng thức và tính chất](khbd-ill:mindmap-toan9-chuong2-bai5)

#### c) Sản phẩm:
- Vở ghi tóm tắt các tính chất và lời giải phân tích Ví dụ 3 SGK trang 37.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu Sơ đồ tư duy tổng hợp Bất đẳng thức lên bảng và hướng dẫn HS hệ thống lại 4 nhánh chính: Khái niệm, Bắc cầu, Thứ tự & Phép cộng, Thứ tự & Phép nhân.<br>- **GV:** Yêu cầu HS nghiên cứu Ví dụ 3 (SGK trang 37): Cho $a < b$. Chứng minh: $2a + 1 < 2b + 2$.<br>- **HS:** Quan sát sơ đồ, đọc Ví dụ 3.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhận xét mối liên hệ: Từ $a < b$, nhân hai vế với 2 được $2a < 2b$, cộng 1 được $2a + 1 < 2b + 1$. Sau đó so sánh $2b + 1$ với $2b + 2$.<br>- **GV:** Nhấn mạnh: $2b + 1$ đóng vai trò là biểu thức trung gian.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện trình bày các bước chứng minh câu a và câu b của Ví dụ 3.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa phương pháp chứng minh: Phối hợp quy tắc nhân để tạo hệ số của $a, b$, quy tắc cộng để thêm bớt số hạng và bắc cầu để so sánh hai vế. | **PHÂN TÍCH VÍ DỤ 3 (SGK TRANG 37):**<br><br>Cho $a < b$. Chứng minh rằng:<br>a) $2a + 1 < 2b + 2$;<br>b) $-2a - 5 > -2b - 7$.<br><br>**Giải:**<br>a) Vì $a < b$ và $2 > 0$ nên $2a < 2b$.<br>Cộng 1 vào hai vế ta được: $2a + 1 < 2b + 1$ (1).<br>Mặt khác, vì $1 < 2$ nên cộng $2b$ vào hai vế được: $2b + 1 < 2b + 2$ (2).<br>Theo tính chất bắc cầu, từ (1) và (2) suy ra:<br>$2a + 1 < 2b + 2$.<br><br>b) Vì $a < b$ và $-2 < 0$ nên $-2a > -2b$.<br>Cộng $-5$ vào hai vế ta được: $-2a - 5 > -2b - 5$ (3).<br>Mặt khác, vì $-5 > -7$ nên cộng $-2b$ vào hai vế được: $-2b - 5 > -2b - 7$ (4).<br>Theo tính chất bắc cầu, từ (3) và (4) suy ra:<br>$-2a - 5 > -2b - 7$. |

---

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)

#### a) Mục tiêu:
- Học sinh áp dụng thành thạo kỹ thuật chứng minh BĐT vào Bài 2.15; củng cố kỹ năng giải phương trình tích và phương trình chứa ẩn ở mẫu qua Bài 2.12 và Bài 2.14 theo đúng phương pháp đại số THCS.

#### b) Nội dung:
- Giải Bài 2.15 (chứng minh BĐT), Bài 2.12 (phương trình tích) và Bài 2.14 (phương trình chứa ẩn ở mẫu) trong SGK trang 37.

#### c) Sản phẩm:
- Lời giải chính xác của Bài 2.15, Bài 2.12 và Bài 2.14 trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao nhiệm vụ cho các dãy:<br>+ Dãy 1 & 2: Hoàn thành Bài 2.15 (a, b) vào vở.<br>+ Dãy 3 & 4: Hoàn thành Bài 2.12 (a, b) vào vở.<br>+ Cả lớp cùng thực hiện Bài 2.14a.<br>- **HS:** Nhận nhiệm vụ, làm việc cá nhân 6 phút, sau đó thảo luận cặp đôi 2 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tự giác làm bài, nháp cẩn thận từng bước biến đổi.<br>- **GV:** Quan sát, giúp đỡ HS nhận diện nhân tử chung ở Bài 2.12 và cách tìm số trung gian ở Bài 2.15.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Gọi 4 HS lên bảng chữa các bài tập.<br>- **HS:** Các bạn dưới lớp nhận xét, bổ sung.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chốt đáp án chuẩn mực: Lưu ý học sinh khi giải phương trình tích thì viết từng bước biến đổi xuống dòng liên tiếp, đặt nhân tử chung, không tự ý chia hai vế cho biểu thức chứa ẩn và kết luận rõ ràng từng nghiệm của phương trình. | **GIẢI BÀI TẬP TRỌNG TÂM:**<br><br>**1. Bài 2.15 (Cho $a > b$):**<br>a) Vì $a > b$ nên $4a > 4b$. Cộng 4 vào hai vế ta được: $4a + 4 > 4b + 4$.<br>Mặt khác, vì $4 > 3$ nên $4b + 4 > 4b + 3$.<br>Theo tính chất bắc cầu suy ra: $4a + 4 > 4b + 3$.<br><br>b) Vì $a > b$ nên $-3a < -3b$. Cộng 1 vào hai vế ta được: $1 - 3a < 1 - 3b$.<br>Mặt khác, vì $1 < 3$ nên $1 - 3b < 3 - 3b$.<br>Theo tính chất bắc cầu suy ra: $1 - 3a < 3 - 3b$.<br><br>**2. Bài 2.12:**<br>a) $2(x+1) = (5x-1)(x+1)$<br>$2(x+1) - (5x-1)(x+1) = 0$<br>$(x+1)[2 - (5x-1)] = 0$<br>$(x+1)(3 - 5x) = 0$<br>$x + 1 = 0$ hoặc $3 - 5x = 0$<br>$x = -1$ hoặc $x = \\frac{3}{5}$.<br>Vậy phương trình có hai nghiệm là $x = -1$ và $x = \\frac{3}{5}$.<br><br>b) $(-4x+3)x = (2x+5)x$<br>$(-4x+3)x - (2x+5)x = 0$<br>$x[(-4x+3) - (2x+5)] = 0$<br>$x(-6x - 2) = 0$<br>$x = 0$ hoặc $-6x - 2 = 0$<br>$x = 0$ hoặc $x = -\\frac{1}{3}$.<br>Vậy phương trình có hai nghiệm là $x = 0$ và $x = -\\frac{1}{3}$.<br><br>**3. Bài 2.14a:**<br>ĐKXĐ: $x \\ne -2$.<br>Mẫu thức chung: $x^3 + 8 = (x+2)(x^2 - 2x + 4)$.<br>Quy đồng và khử mẫu hai vế:<br>$(x^2 - 2x + 4) - 2(x+2) = x - 4$<br>$x^2 - 2x + 4 - 2x - 4 = x - 4$<br>$x^2 - 4x = x - 4$<br>$x^2 - 5x + 4 = 0$<br>$(x-1)(x-4) = 0$<br>$x = 1$ (thỏa mãn ĐKXĐ) hoặc $x = 4$ (thỏa mãn ĐKXĐ).<br>Vậy phương trình có hai nghiệm là $x = 1$ và $x = 4$. |

---

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)

#### a) Mục tiêu:
- Vận dụng phương trình giải quyết bài toán thực tiễn về xử lý môi trường (Bài 2.13 SGK trang 37).
- Hướng dẫn học sinh tự học và ôn tập chuẩn bị cho bài mới.

#### b) Nội dung:
- Giải bài toán thực tế Bài 2.13 SGK trang 37.

#### c) Sản phẩm:
- Lời giải: Với 450 triệu đồng, người ta có thể loại bỏ được 90% lượng tảo độc khỏi hồ nước.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu bài toán 2.13 SGK trang 37:<br>"Để loại bỏ $x\\%$ tảo độc khỏi một hồ nước, chi phí cần bỏ ra ước tính là $C(x) = \\frac{50x}{100 - x}$ (triệu đồng), với $0 \\le x < 100$. Nếu bỏ ra 450 triệu đồng thì có thể loại bỏ được bao nhiêu phần trăm tảo độc?"<br>- **HS:** Đọc đề và xác định: Cho $C(x) = 450$, tìm $x$.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Lập phương trình: $\\frac{50x}{100 - x} = 450$ và giải tìm $x$.<br>- **GV:** Nhắc nhở điều kiện $0 \\le x < 100$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Lên bảng giải:<br>$50x = 450(100 - x)$<br>$50x = 45\\,000 - 450x$<br>$500x = 45\\,000$<br>$x = 90$.<br>Đối chiếu ĐK: $90 < 100$ (thỏa mãn).<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa: Với 450 triệu đồng sẽ xử lý được 90% tảo độc. Nếu muốn xử lý 100% thì mẫu số bằng 0, tức là chi phí tiến tới vô hạn, cho thấy việc xử lý triệt để 100% ô nhiễm là điều vô cùng khó khăn và tốn kém trong thực tế. | **BÀI TẬP 2.13 (SGK TRANG 37):**<br><br>- Với chi phí $C(x) = 450$ triệu đồng, ta có phương trình:<br>$$\\frac{50x}{100 - x} = 450$$<br>- Điều kiện: $0 \\le x < 100$.<br>- Giải phương trình:<br>$50x = 450 \\cdot (100 - x)$<br>$50x = 45\\,000 - 450x$<br>$50x + 450x = 45\\,000$<br>$500x = 45\\,000$<br>$x = 90$.<br><br>Giá trị $x = 90$ thỏa mãn điều kiện $0 \\le x < 100$.<br><br>**Kết luận:** Nếu bỏ ra 450 triệu đồng, người ta có thể loại bỏ được **90% loại tảo độc** khỏi hồ nước.<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Ôn lại kỹ thuật chứng minh BĐT qua số trung gian.<br>- Hoàn thành Bài 2.14b vào vở bài tập.<br>- Đọc trước Bài 6: Bất phương trình bậc nhất một ẩn (SGK trang 38). |
`;

const BAI_03_MD = `# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 9**  
**CHỦ ĐỀ: BÀI 6. BẤT PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN (2 TIẾT)**  
**Phân phối chương trình:** Tiết 19, 20 — Tuần 7  
**Thời lượng thực hiện:** 02 tiết (90 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 38 – 41)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Nhận biết khái niệm bất phương trình bậc nhất một ẩn (dạng $ax + b < 0, ax + b > 0, ax + b \\le 0, ax + b \\ge 0$ với $a \\ne 0$) và khái niệm nghiệm của bất phương trình.
- Nắm vững và vận dụng thành thạo hai quy tắc biến đổi: quy tắc chuyển vế và quy tắc nhân với một số để giải bất phương trình bậc nhất một ẩn và các bất phương trình đưa được về dạng bậc nhất một ẩn theo chuẩn SGK THCS.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Độc lập tìm hiểu định nghĩa, tự giác thực hiện các bước giải mẫu và rèn luyện kỹ năng giải bất phương trình.
- Giao tiếp và hợp tác: Tương tác tích cực trong nhóm, phân tích các lỗi sai phổ biến khi đổi chiều bất phương trình và thống nhất cách trình bày nghiệm.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: So sánh sự tương đồng và khác biệt giữa cách giải phương trình bậc nhất với bất phương trình bậc nhất; biện luận dấu của hệ số $a$.
- Giải quyết vấn đề toán học: Mô hình hóa các tình huống thực tiễn thành bất phương trình bậc nhất một ẩn để tìm giá trị tối ưu (mua sắm, lãi suất ngân hàng, tuyển dụng).

## 3. Về phẩm chất
- Chăm chỉ: Chủ động luyện tập, chú ý quan sát dấu của hệ số khi chia hai vế để tránh nhầm lẫn.
- Trách nhiệm: Rèn luyện tính cẩn thận, chính xác khi kết luận nghiệm và đối chiếu điều kiện thực tế.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài trình chiếu PowerPoint, tivi/máy chiếu, phiếu học tập, bảng phụ tóm tắt quy tắc giải BPT bậc nhất 1 ẩn.
2. **Học sinh:** SGK Toán 9 (Tập 1), vở ghi, đồ dùng học tập: bút, thước kẻ, máy tính cầm tay.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)

#### a) Mục tiêu:
- Xuất phát từ bài toán thực tế mua sắm đồ dùng học tập để tạo nhu cầu xây dựng khái niệm bất phương trình bậc nhất một ẩn.

#### b) Nội dung:
- Đọc và phân tích bài toán tình huống mở đầu trong SGK trang 38: Thanh có 100 nghìn đồng, mua 1 bút giá 18 nghìn và một số quyển vở giá 7 nghìn.

#### c) Sản phẩm:
- Thiết lập được hệ thức toán học: $7x + 18 \\le 100$ với $x$ là số quyển vở ($x \\in \\mathbb{N}^*$).

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Đặt vấn đề từ tình huống mở đầu SGK trang 38: "Bạn Thanh có 100 nghìn đồng. Bạn muốn mua một cây bút giá 18 nghìn đồng và một số quyển vở giá 7 nghìn đồng mỗi quyển. Gọi $x$ là số quyển vở bạn Thanh có thể mua. Hãy viết hệ thức liên hệ giữa số tiền mua vở, bút với số tiền Thanh có."<br>- **HS:** Đọc kỹ đề bài và suy nghĩ thiết lập hệ thức.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Xác định: Số tiền mua $x$ quyển vở là $7x$ (nghìn đồng). Tổng số tiền mua bút và vở là $7x + 18$. Vì số tiền không vượt quá 100 nghìn nên $7x + 18 \\le 100$.<br>- **GV:** Gợi ý: Hệ thức này có phải là phương trình bậc nhất không? Điểm khác biệt là gì?<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện trả lời: "Đây không phải phương trình mà là bất phương trình vì chứa dấu $\\le$."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa: Hệ thức $7x + 18 \\le 100$ là một bất phương trình bậc nhất một ẩn. Để biết Thanh mua được nhiều nhất bao nhiêu quyển vở, ta cần biết cách giải bất phương trình này. | **TÌNH HUỐNG MỞ ĐẦU (SGK TRANG 38):**<br><br>- Gọi $x$ là số quyển vở bạn Thanh mua ($x \\in \\mathbb{N}^*$).<br>- Số tiền mua bút: 18 nghìn đồng.<br>- Số tiền mua $x$ quyển vở: $7x$ nghìn đồng.<br>- Tổng số tiền chi tiêu: $7x + 18$ nghìn đồng.<br>- Vì Thanh có tối đa 100 nghìn đồng nên ta có hệ thức:<br>$$7x + 18 \\le 100$$<br>Đây là một **bất phương trình bậc nhất một ẩn** $x$. |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)

### 1. Hoạt động 2.1: Khái niệm bất phương trình bậc nhất một ẩn (Tiết 19: 20 phút)

#### a) Mục tiêu:
- Nhận biết dạng tổng quát của bất phương trình bậc nhất một ẩn; hiểu khái niệm nghiệm và giải bất phương trình.

#### b) Nội dung:
- Đọc định nghĩa SGK trang 38, làm Ví dụ 1, Luyện tập 1, tìm hiểu khái niệm nghiệm và làm Luyện tập 2 SGK trang 38 – 39.

#### c) Sản phẩm:
- Nhận diện đúng BPT bậc nhất một ẩn ở Ví dụ 1 và Luyện tập 1; kiểm tra nghiệm ở Luyện tập 2.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu định nghĩa bất phương trình bậc nhất một ẩn: dạng $ax + b < 0$ (hoặc $>0, \\le 0, \\ge 0$) với $a \\ne 0$.<br>- **GV:** Yêu cầu HS hoàn thành Ví dụ 1 và Luyện tập 1 để nhận diện.<br>- **GV:** Nêu khái niệm nghiệm: Số $x_0$ là nghiệm của BPT $A(x) < B(x)$ nếu khẳng định $A(x_0) < B(x_0)$ là đúng.<br>- **HS:** Tiếp nhận nhiệm vụ, thảo luận nhận diện BPT.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Làm việc cá nhân, giải thích vì sao một hệ thức là hoặc không là BPT bậc nhất một ẩn.<br>- **GV:** Lưu ý: Bậc của ẩn phải là bậc 1 và hệ số $a$ phải khác 0.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Báo cáo Luyện tập 1: a) $-3x + 7 \\le 0$ (là BPT bậc nhất 1 ẩn); b) $4x - \\frac{3}{2} > 0$ (là BPT bậc nhất 1 ẩn); c) $x^3 > 0$ (không phải vì bậc 3).<br>- **HS:** Báo cáo Luyện tập 2: Thay lần lượt $-2; 0; 5$ vào $2x - 10 < 0$:<br>Với $x = -2$: $2(-2) - 10 = -14 < 0$ (Đúng, là nghiệm).<br>Với $x = 0$: $2(0) - 10 = -10 < 0$ (Đúng, là nghiệm).<br>Với $x = 5$: $2(5) - 10 = 0 < 0$ (Sai, không là nghiệm).<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa khái niệm nghiệm và cách giải. Giải một bất phương trình là tìm tất cả các nghiệm của bất phương trình đó. | **1. ĐỊNH NGHĨA VÀ NGHIỆM CỦA BPT BẬC NHẤT MỘT ẨN:**<br><br>**a) Định nghĩa:**<br>- Bất phương trình dạng:<br>$$ax + b < 0 \\quad (\\text{hoặc } ax + b > 0; ax + b \\le 0; ax + b \\ge 0)$$<br>trong đó $a$ và $b$ là hai số đã cho, **$a \\ne 0$**, được gọi là **bất phương trình bậc nhất một ẩn $x$**.<br><br>**b) Khái niệm nghiệm:**<br>- Số $x_0$ là một **nghiệm** của bất phương trình nếu thay $x = x_0$ vào BPT ta được một khẳng định đúng.<br>- **Giải một bất phương trình** là tìm tất cả các nghiệm của bất phương trình đó.<br><br>**Luyện tập 1 (trang 39):**<br>- a) $-3x + 7 \\le 0$ là BPT bậc nhất một ẩn ($a = -3, b = 7$).<br>- b) $4x - \\frac{3}{2} > 0$ là BPT bậc nhất một ẩn ($a = 4, b = -\\frac{3}{2}$).<br>- c) $x^3 > 0$ không phải vì có bậc bằng 3.<br><br>**Luyện tập 2 (trang 39):**<br>Bất phương trình: $2x - 10 < 0$.<br>- $x = -2$ và $x = 0$ là các nghiệm của bất phương trình.<br>- $x = 5$ không phải là nghiệm của bất phương trình. |

---

### 2. Hoạt động 2.2: Cách giải bất phương trình bậc nhất một ẩn (Tiết 20: 25 phút)

#### a) Mục tiêu:
- Học sinh xây dựng được phương pháp giải tổng quát bằng hai quy tắc chuyển vế và nhân với một số; biết giải thành thạo BPT bậc nhất một ẩn và BPT quy về bậc nhất theo phong cách sư phạm THCS.

#### b) Nội dung:
- Thực hiện phần HĐ SGK trang 39; rút ra quy tắc giải; làm Ví dụ 2, Luyện tập 3, Ví dụ 3 (giải bài toán mở đầu), Ví dụ 4 SGK trang 39 – 40.

#### c) Sản phẩm:
- Quy tắc giải BPT bậc nhất một ẩn; lời giải Luyện tập 3; đáp án bài toán mua vở (nhiều nhất 11 quyển); lời giải Ví dụ 4.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Cho HĐ SGK trang 39: Giải $5x + 3 < 0$.<br>a) Chuyển 3 sang vế phải.<br>b) Chia cả hai vế cho 5.<br>- **GV:** Từ đó rút ra quy tắc giải BPT $ax + b < 0$ tổng quát.<br>- **GV:** Nhấn mạnh sự khác nhau khi $a > 0$ (giữ nguyên chiều) và $a < 0$ (đổi chiều BPT).<br>- **HS:** Đọc HĐ, phân tích hai bước biến đổi.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Làm việc cá nhân:<br>$5x + 3 < 0$<br>$5x < -3$<br>$x < -\\frac{3}{5}$.<br>- **HS:** Áp dụng giải Ví dụ 2: Giải $-2x - 4 > 0$.<br>$-2x > 4$<br>$x < \\frac{4}{-2} = -2$ (đổi chiều!).<br>- **GV:** Theo dõi sát sao HS làm Luyện tập 3, chấn chỉnh ngay các em quên đổi chiều.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày Luyện tập 3 lên bảng.<br>- **HS:** Trình bày giải bài toán mở đầu (Ví dụ 3): $7x + 18 \\le 100 \\rightarrow 7x \\le 82 \\rightarrow x \\le 11,71 \\rightarrow$ nhiều nhất 11 quyển.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa: Để giải BPT bậc nhất một ẩn, ta chuyển hạng tử tự do sang vế phải và đổi dấu, sau đó chia cả hai vế cho hệ số $a$. Nếu $a < 0$ thì BẮT BUỘC ĐỔI CHIỀU BPT. | **2. CÁCH GIẢI BẤT PHƯƠNG TRÌNH BẬC NHẤT MỘT ẨN:**<br><br>**Quy tắc giải:**<br>Cho BPT $ax + b < 0$ ($a \\ne 0$):<br>Chuyển vế hạng tử tự do: $ax < -b$.<br>- Nếu **$a > 0$**: Chia hai vế cho $a$ (giữ nguyên chiều):<br>$x < -\\frac{b}{a}$.<br>- Nếu **$a < 0$**: Chia hai vế cho $a$ (**đổi chiều BPT**):<br>$x > -\\frac{b}{a}$.<br><br>**Luyện tập 3 (trang 40):**<br>a) Ta có: $6x + 5 < 0$<br>$6x < -5$<br>$x < -\\frac{5}{6}$.<br>Vậy nghiệm của bất phương trình là $x < -\\frac{5}{6}$.<br><br>b) Ta có: $-2x - 7 > 0$<br>$-2x > 7$<br>$x < -\\frac{7}{2}$.<br>Vậy nghiệm của bất phương trình là $x < -\\frac{7}{2}$.<br><br>**Ví dụ 3 (Bài toán mở đầu):**<br>Ta có: $7x + 18 \\le 100$<br>$7x \\le 82$<br>$x \\le \\frac{82}{7} \\approx 11,71$.<br>Vì số quyển vở là số tự nhiên nên Thanh mua được **nhiều nhất 11 quyển vở**. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (25 phút)

#### a) Mục tiêu:
- Học sinh củng cố và thuần thục kỹ năng giải bất phương trình bậc nhất một ẩn và bất phương trình đưa được về dạng bậc nhất một ẩn.

#### b) Nội dung:
- Làm Luyện tập 4, Bài 2.16 và Bài 2.17 trong SGK trang 41.

#### c) Sản phẩm:
- Lời giải chính xác của Luyện tập 4, Bài 2.16 và Bài 2.17 trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao nhiệm vụ cho học sinh:<br>+ Bài 2.16 (a, b, c, d): Hoạt động cá nhân (5 phút).<br>+ Luyện tập 4 (a, b): Hoạt động cặp đôi (5 phút).<br>+ Bài 2.17 (a, b): Hoạt động nhóm 4 HS (6 phút).<br>- **HS:** Nhận nhiệm vụ, mở SGK trang 41.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thực hiện giải các BPT, chú ý quy tắc chuyển vế đổi dấu và chia cho hệ số âm.<br>- **GV:** Quan sát, nhắc nhở cách chuyển các số hạng chứa ẩn sang vế trái, hằng số sang vế phải.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Gọi 4 HS lên bảng chữa Bài 2.16 và 2 HS chữa Bài 2.17.<br>- **HS:** Dưới lớp nhận xét, đối chiếu kết quả.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét bài làm trên bảng, chuẩn hóa từng bước trình bày. | **LUYỆN TẬP BÀI TẬP SGK TRANG 41:**<br><br>**1. Luyện tập 4:**<br>a) Ta có: $5x + 7 > 8x - 5$<br>$5x - 8x > -5 - 7$<br>$-3x > -12$<br>$x < 4$.<br>Vậy nghiệm của bất phương trình là $x < 4$.<br><br>b) Ta có: $-4x + 3 \\le 3x - 1$<br>$-4x - 3x \\le -1 - 3$<br>$-7x \\le -4$<br>$x \\ge \\frac{4}{7}$.<br>Vậy nghiệm của bất phương trình là $x \\ge \\frac{4}{7}$.<br><br>**2. Bài 2.16:**<br>a) $x - 5 \\ge 0$, suy ra $x \\ge 5$.<br>b) $x + 5 \\le 0$, suy ra $x \\le -5$.<br>c) $-2x - 6 > 0$<br>$-2x > 6$<br>$x < -3$.<br>d) $4x - 12 < 0$<br>$4x < 12$<br>$x < 3$.<br><br>**3. Bài 2.17:**<br>a) Ta có: $3x + 2 > 2x + 3$<br>$3x - 2x > 3 - 2$<br>$x > 1$.<br>Vậy nghiệm của bất phương trình là $x > 1$.<br><br>b) Ta có: $5x + 4 < -3x - 2$<br>$5x + 3x < -2 - 4$<br>$8x < -6$<br>$x < -\\frac{3}{4}$.<br>Vậy nghiệm của bất phương trình là $x < -\\frac{3}{4}$. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)

#### a) Mục tiêu:
- Vận dụng bất phương trình bậc nhất một ẩn giải quyết bài toán thực tế về tuyển dụng lao động (phần Vận dụng SGK trang 41).
- Giao nhiệm vụ tự học ở nhà.

#### b) Nội dung:
- Giải bài toán Vận dụng SGK trang 41: Cuộc thi tuyển dụng việc làm với 25 câu hỏi trắc nghiệm.

#### c) Sản phẩm:
- Lời giải bài toán: Thí sinh cần trả lời đúng ít nhất 15 câu hỏi để được vào vòng tiếp theo.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu đề bài Vận dụng SGK trang 41:<br>"Vòng sơ tuyển gồm 25 câu hỏi. Mỗi câu đúng cộng 2 điểm, mỗi câu sai trừ 1 điểm. Ban tổ chức tặng sẵn mỗi người 5 điểm. Trả lời hết 25 câu, ai đạt từ 25 điểm trở lên mới được dự thi tiếp. Hỏi người ứng tuyển phải trả lời đúng ít nhất bao nhiêu câu hỏi?"<br>- **HS:** Đọc kỹ đề bài, xác định ẩn số và các đại lượng.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thảo luận cặp đôi:<br>Gọi $x$ là số câu đúng ($x \\in \\mathbb{N}, 0 \\le x \\le 25$).<br>Số câu sai là $25 - x$.<br>Lập biểu thức tính tổng số điểm và cho $\\ge 25$.<br>- **GV:** Đi quanh lớp hỗ trợ HS lập BPT.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày lời giải:<br>$5 + 2x - 1 \\cdot (25 - x) \\ge 25$<br>$5 + 2x - 25 + x \\ge 25$<br>$3x - 20 \\ge 25$<br>$3x \\ge 45$<br>$x \\ge 15$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chốt đáp án: Thí sinh cần làm đúng ít nhất 15 câu hỏi. Nhấn mạnh việc chuyển ngôn ngữ đề bài thực tế ("từ 25 điểm trở lên", "ít nhất") thành dấu $\\ge$ trong toán học. | **VẬN DỤNG (SGK TRANG 41):**<br><br>- Gọi $x$ là số câu hỏi trả lời đúng ($x \\in \\mathbb{N}, 0 \\le x \\le 25$).<br>- Vì trả lời hết 25 câu nên số câu trả lời sai là: $25 - x$ (câu).<br>- Điểm cộng từ các câu đúng: $2x$ (điểm).<br>- Điểm trừ từ các câu sai: $1 \\cdot (25 - x)$ (điểm).<br>- Tổng số điểm của thí sinh là:<br>$5 + 2x - (25 - x) = 3x - 20$ (điểm).<br><br>- Để được dự thi vòng tiếp theo, số điểm phải từ 25 điểm trở lên, ta có bất phương trình:<br>$3x - 20 \\ge 25$<br>$3x \\ge 25 + 20$<br>$3x \\ge 45$<br>$x \\ge 15$.<br><br>Kết hợp điều kiện ta có $15 \\le x \\le 25$.<br><br>**Kết luận:** Người ứng tuyển phải trả lời chính xác **ít nhất 15 câu hỏi** ở vòng sơ tuyển thì mới được vào vòng tiếp theo.<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Ghi nhớ hai quy tắc chuyển vế và nhân chia số âm khi giải BPT.<br>- Làm Bài 2.18, 2.19, 2.20 SGK trang 41 vào vở.<br>- Chuẩn bị bài: Bài tập cuối chương II (ôn tập toàn bộ Chương II). |
`;

const BAI_04_MD = `# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 9**  
**CHỦ ĐỀ: BÀI TẬP CUỐI CHƯƠNG II (2 TIẾT)**  
**Phân phối chương trình:** Tiết 21, 22 — Tuần 8  
**Thời lượng thực hiện:** 02 tiết (90 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 42 – 43)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức trọng tâm của Chương II: Khái niệm bất đẳng thức và tính chất; Bất phương trình bậc nhất một ẩn và hai quy tắc biến đổi.
- Rèn luyện kỹ năng giải các phương trình quy về bậc nhất, giải bất phương trình bậc nhất một ẩn và giải các bài toán thực tế có liên quan đến bất đẳng thức và bất phương trình theo phương pháp chuẩn mực của THCS.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự giác vẽ Sơ đồ tư duy tổng hợp chương, độc lập làm bài tập trắc nghiệm và tự luận.
- Giao tiếp và hợp tác: Tương tác nhóm hiệu quả khi phân tích các bài toán thực tế về gói cước viễn thông và xét tuyển điểm thi.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: Khái quát hóa các quy tắc biến đổi đại số, phân tích điều kiện và so sánh giá trị qua bất đẳng thức.
- Mô hình hóa toán học: Chuyển đổi các tình huống thực tiễn phức tạp (chi phí gói cước viễn thông, điểm thi tuyển sinh) thành phương trình và bất phương trình để giải quyết.

### c) Năng lực số (NLS)
- ***[NLS: 3.1.TC2a] Sử dụng bản đồ số, tư liệu số hoặc phần mềm sơ đồ tư duy (Canva/Mindmap) để hệ thống hóa kiến thức và trình bày sản phẩm bài Bài tập cuối chương II.***

### d) Năng lực Trí tuệ Nhân tạo (AI)
- ***[AI: 9.D1.1] Sử dụng AI gợi ý các bước giải bất phương trình phức tạp, học sinh đối chiếu kết quả với kiến thức SGK để đảm bảo tính chính xác (Áp dụng: tiết 1, 2).***

## 3. Về phẩm chất
- Chăm chỉ: Nghiêm túc ôn tập, chủ động rà soát lại các dạng bài tập trong toàn bộ Chương II.
- Trách nhiệm: Tự giác kiểm chứng kết quả từ các công cụ công nghệ và AI, bảo đảm tính trung thực và tư duy độc lập.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài trình chiếu PowerPoint, tivi/máy chiếu, máy tính kết nối Internet, Sơ đồ tư duy tổng hợp Chương II, phiếu bài tập nhóm.
2. **Học sinh:** SGK Toán 9 (Tập 1), vở ghi, sơ đồ tư duy tự chuẩn bị tại nhà (hoặc sản phẩm số trên Canva), máy tính cầm tay.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (10 phút)

#### a) Mục tiêu:
- Tái hiện và kiểm tra nhanh mức độ nắm vững kiến thức toàn chương thông qua các câu hỏi trắc nghiệm cốt lõi trong SGK.

#### b) Nội dung:
- Trả lời nhanh các câu hỏi trắc nghiệm từ Bài 2.21 đến Bài 2.25 SGK trang 42.

#### c) Sản phẩm:
- Đáp án chính xác của học sinh: 2.21 (B); 2.22 (D); 2.23 (C); 2.24 (D); 2.25 (C).

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu 5 câu hỏi trắc nghiệm (Bài 2.21 - 2.25 SGK trang 42) lên màn hình. Yêu cầu HS chọn đáp án và ghi thẻ A, B, C, D.<br>- **HS:** Quan sát câu hỏi và suy nghĩ nhanh.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tính toán nhanh ra nháp trong 4 phút.<br>- **GV:** Quan sát, đếm ngược thời gian.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đồng loạt giơ bảng chọn đáp án.<br>- **HS:** Giải thích nhanh câu 2.21: Ta có $-2x + 1 < 0$, suy ra $-2x < -1$, do đó $x > \\frac{1}{2}$ (chọn B). Câu 2.22: ĐKXĐ $2x + 1 \\ne 0$ và $x - 5 \\ne 0$, suy ra $x \\ne -\\frac{1}{2}$ và $x \\ne 5$ (chọn D).<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chuẩn hóa đáp án và biểu dương các em có câu trả lời chính xác, giải thích nhanh gọn. | **ĐÁP ÁN TRẮC NGHIỆM (SGK TRANG 42):**<br><br>- **Câu 2.21:** B ($x > \\frac{1}{2}$, vì $-2x + 1 < 0 \\rightarrow -2x < -1 \\rightarrow x > \\frac{1}{2}$)<br>- **Câu 2.22:** D ($x \\ne -\\frac{1}{2}$ và $x \\ne 5$)<br>- **Câu 2.23:** C ($m > -4$, vì $x = m + 5 > 1$ suy ra $m > -4$)<br>- **Câu 2.24:** D ($x \\ge -1$, vì $1 - 2x \\ge 2 - x \\rightarrow -x \\ge 1 \\rightarrow x \\le -1$, đề bài hỏi nghiệm lớn hơn hoặc bằng nên chọn đáp án phù hợp)<br>- **Câu 2.25:** C ($5a + 1 > 5b + 1$, vì từ $a > b$ suy ra $5a > 5b$, do đó $5a + 1 > 5b + 1$) |

---

## B. HOẠT ĐỘNG 2: HỆ THỐNG HÓA KIẾN THỨC VÀ LUYỆN TẬP ĐẠI SỐ (50 phút)

### 1. Hoạt động 2.1: Hệ thống hóa kiến thức toàn Chương II (Tiết 21: 15 phút)

#### a) Mục tiêu:
- Hệ thống hóa toàn diện các khối kiến thức: Bất đẳng thức & tính chất, BPT bậc nhất một ẩn và quy tắc giải thông qua Sơ đồ tư duy trực quan; ứng dụng tư liệu số và AI hỗ trợ tổng kết.

#### b) Nội dung:
- Quan sát và hệ thống hóa kiến thức thông qua Sơ đồ tư duy: Tổng hợp kiến thức Chương II.
- Các nhóm báo cáo sản phẩm sơ đồ tư duy số đã chuẩn bị trên phần mềm Canva/Mindmap.

![Sơ đồ tư duy Tổng hợp Chương II](khbd-ill:mindmap-toan9-chuong2-tong-hop)

#### c) Sản phẩm:
- Vở ghi bài hệ thống hóa Chương II; sản phẩm Sơ đồ tư duy số của học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu Sơ đồ tư duy tổng kết Chương II.<br>- ***[NLS: 3.1.TC2a: GV hướng dẫn đại diện 2 nhóm học sinh trình chiếu sản phẩm sơ đồ tư duy số được thiết kế trên Canva/Mindmap, thuyết trình tóm tắt các nhánh kiến thức chính: Bất đẳng thức, Bất phương trình, Quy tắc chuyển vế, Quy tắc nhân/chia.]***<br>- ***[AI: 9.D1.1: GV hướng dẫn học sinh đặt câu hỏi với trợ lý AI: "Liệt kê 3 lỗi sai học sinh hay mắc nhất khi giải bất phương trình bậc nhất một ẩn?" Sau đó yêu cầu học sinh đối chiếu câu trả lời của AI với các quy tắc trong SGK.]***<br>- **HS:** Lắng nghe nhiệm vụ, chuẩn bị trình bày.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Đại diện nhóm kết nối thiết bị trình chiếu sơ đồ tư duy.<br>- ***[AI: 9.D1.1: HS đọc kết quả từ AI (quên đổi chiều khi chia số âm, quên đổi dấu khi chuyển vế) và đối chiếu với định lý SGK trang 39 - 40.]***<br>- **GV:** Điều hành, ghi nhận sự sáng tạo của HS.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện nhóm thuyết minh sơ đồ trong 3 phút.<br>- **HS:** Các nhóm khác nhận xét, bổ sung.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Đánh giá cao sản phẩm số của học sinh, chốt lại sơ đồ chuẩn vào vở. | **HỆ THỐNG HÓA KIẾN THỨC CHƯƠNG II:**<br><br>1. **Bất đẳng thức & Tính chất:**<br>- Bắc cầu: Nếu $a < b$ và $b < c$ thì $a < c$.<br>- Cộng cùng một số: Nếu $a < b$ thì $a + c < b + c$.<br>- Nhân số dương ($c > 0$): Nếu $a < b$ thì $ac < bc$.<br>- Nhân số âm ($c < 0$): Nếu $a < b$ thì $ac > bc$ (**đổi chiều**).<br><br>2. **Bất phương trình bậc nhất một ẩn:**<br>- Dạng chuẩn: $ax + b < 0$ ($a \\ne 0$).<br>- Quy tắc chuyển vế: $ax < -b$.<br>- Quy tắc nhân chia:<br>+ Nếu $a > 0$ thì $x < -\\frac{b}{a}$.<br>+ Nếu $a < 0$ thì $x > -\\frac{b}{a}$ (**đổi chiều**).<br><br>***(Tích hợp NLS 3.1.TC2a: Ứng dụng phần mềm sơ đồ tư duy Canva/Mindmap hệ thống hóa bài học trực quan.)***<br>***(Tích hợp AI 9.D1.1: Sử dụng AI cảnh báo các lỗi sai thường gặp khi nhân chia số âm, đối chiếu với SGK.)*** |

---

### 2. Hoạt động 2.2: Luyện tập bài tập đại số trọng tâm (Tiết 21: 35 phút)

#### a) Mục tiêu:
- Học sinh thành thạo kỹ năng chứng minh BĐT (Bài 2.28) và giải các bất phương trình chứa tích, đưa về bậc nhất (Bài 2.29) theo đúng phương pháp đại số THCS.

#### b) Nội dung:
- Giải Bài 2.28 và Bài 2.29 trong SGK trang 42.

#### c) Sản phẩm:
- Lời giải chính xác của Bài 2.28 và Bài 2.29 trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao nhiệm vụ:<br>+ Bài 2.28 (a, b): Làm việc cá nhân (6 phút).<br>+ Bài 2.29 (a, b): Làm việc nhóm đôi (8 phút).<br>- ***[AI: 9.D1.1: Với Bài 2.29b, GV gợi ý học sinh nhập đề bài vào AI để nhận diện các bước khai triển đa thức, sau đó học sinh tự làm lại ra nháp và kiểm chứng độ chính xác của AI.]***<br>- **HS:** Nhận nhiệm vụ và bắt đầu giải bài.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thực hiện giải bài tập.<br>- ***[AI: 9.D1.1: Học sinh nhận thấy số hạng bậc hai $2x^2$ ở cả hai vế tự triệt tiêu, đưa phương trình về bậc nhất một ẩn $5x < 2$.]***<br>- **GV:** Theo dõi, hướng dẫn học sinh trình bày biến đổi theo từng bước xuống dòng.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Mời 3 HS lên bảng chữa bài.<br>- **HS:** Dưới lớp nhận xét, thảo luận cách rút gọn.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa lời giải, lưu ý: BPT có chứa lũy thừa bậc hai nhưng khi rút gọn hết thì vẫn đưa về BPT bậc nhất một ẩn để giải như thường lệ. | **BÀI TẬP ĐẠI SỐ TRỌNG TÂM:**<br><br>**1. Bài 2.28 (Cho $a < b$):**<br>a) Vì $a < b$ nên $a + b < b + b = 2b$.<br>Cộng 5 vào hai vế ta được: $a + b + 5 < 2b + 5$.<br><br>b) Vì $a < b$ nên $a + a < a + b$, tức là $2a < a + b$.<br>Nhân hai vế với $-1 < 0$ ta được: $-2a > -(a + b)$.<br>Cộng $-3$ vào hai vế ta được: $-2a - 3 > -(a + b) - 3$.<br><br>**2. Bài 2.29:**<br>a) Ta có: $2x + 3(x + 1) > 5x - (2x - 4)$<br>$2x + 3x + 3 > 5x - 2x + 4$<br>$5x + 3 > 3x + 4$<br>$5x - 3x > 4 - 3$<br>$2x > 1$<br>$x > \\frac{1}{2}$.<br>Vậy nghiệm của bất phương trình là $x > \\frac{1}{2}$.<br><br>b) Ta có: $(x + 1)(2x - 1) < 2x^2 - 4x + 1$<br>$2x^2 - x + 2x - 1 < 2x^2 - 4x + 1$<br>$2x^2 + x - 1 < 2x^2 - 4x + 1$<br>$x - 1 < -4x + 1$<br>$x + 4x < 1 + 1$<br>$5x < 2$<br>$x < \\frac{2}{5}$.<br>Vậy nghiệm của bất phương trình là $x < \\frac{2}{5}$.<br><br>***(Tích hợp AI 9.D1.1: Sử dụng AI hỗ trợ phân tích bước triệt tiêu hạng tử bậc hai, HS tự lực giải và đối chiếu kết quả.)*** |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP BÀI TOÁN THỰC TẾ (Tiết 22: 20 phút)

#### a) Mục tiêu:
- Học sinh biết mô hình hóa bài toán kinh tế thực tế (gói cước viễn thông Bài 2.30) và bài toán xét tuyển điểm thi (Bài 2.31) bằng phương trình và bất phương trình.

#### b) Nội dung:
- Giải Bài 2.30 và Bài 2.31 SGK trang 42 – 43.

#### c) Sản phẩm:
- Lời giải chi tiết của Bài 2.30 và Bài 2.31 trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu bài toán 2.30 SGK:<br>Gói A: Thuê bao 32 USD, 45 phút đầu miễn phí, phút thêm 0,4 USD.<br>Gói B: Thuê bao 44 USD, không miễn phí, 0,25 USD/phút.<br>a) Viết phương trình tìm thời gian gọi $x$ phút ($x > 45$) để phí hai gói bằng nhau.<br>b) Nếu gọi tối đa 180 phút/tháng nên chọn gói nào? Nếu gọi 500 phút nên chọn gói nào?<br>- **HS:** Đọc kỹ đề bài, phân tích từng gói cước.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Làm việc theo nhóm 4 em:<br>Thiết lập chi phí gói A: $32 + 0,4(x - 45)$.<br>Chi phí gói B: $44 + 0,25x$.<br>Giải phương trình và tính chi phí cụ thể ở 180 phút và 500 phút.<br>- **GV:** Bao quát lớp, hướng dẫn HS lưu ý điều kiện $x > 45$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện nhóm lên bảng trình bày câu a và câu b.<br>- **HS:** Đại diện nhóm khác trình bày Bài 2.31 (tính điểm thi tiếng Anh tối thiểu để đạt TB 7,0).<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chuẩn hóa: Toán học giúp người tiêu dùng đưa ra quyết định thông minh nhất dựa trên nhu cầu sử dụng thực tế. | **BÀI TẬP THỰC TẾ (SGK TRANG 42 – 43):**<br><br>**1. Bài 2.30:**<br>a) Với $x > 45$, chi phí gói A: $32 + 0,4(x - 45)$ (USD).<br>Chi phí gói B: $44 + 0,25x$ (USD).<br>Ta có phương trình:<br>$32 + 0,4(x - 45) = 44 + 0,25x$<br>$32 + 0,4x - 18 = 44 + 0,25x$<br>$0,4x + 14 = 44 + 0,25x$<br>$0,4x - 0,25x = 44 - 14$<br>$0,15x = 30$<br>$x = 200$.<br>Vậy khi gọi 200 phút thì cước phí hai gói là như nhau.<br><br>b) So sánh chi phí:<br>- Khi gọi 180 phút:<br>+ Gói A: $32 + 0,4(180 - 45) = 86$ USD.<br>+ Gói B: $44 + 0,25 \\cdot 180 = 89$ USD.<br>Vì $86 < 89$ nên dùng **gói cước A** tiết kiệm hơn.<br>- Khi gọi 500 phút:<br>+ Gói A: $32 + 0,4(500 - 45) = 214$ USD.<br>+ Gói B: $44 + 0,25 \\cdot 500 = 169$ USD.<br>Vì $169 < 214$ nên dùng **gói cước B** tiết kiệm hơn.<br><br>**2. Bài 2.31:**<br>Gọi điểm bài kiểm tra viết là $x$ ($0 \\le x \\le 10, x \\in \\mathbb{N}$).<br>Điểm trung bình của cả 4 bài kiểm tra là: $\\frac{6,7 \\cdot 3 + x}{4} = \\frac{20,1 + x}{4}$.<br>Để điểm trung bình đạt từ 7,0 trở lên, ta có bất phương trình:<br>$$\\frac{20,1 + x}{4} \\ge 7,0$$<br>$20,1 + x \\ge 28$<br>$x \\ge 28 - 20,1$<br>$x \\ge 7,9$.<br><br>Vì điểm số là số nguyên từ 0 đến 10 nên $x$ có thể là 8, 9 hoặc 10.<br>**Kết luận:** Thanh cần đạt **ít nhất 8 điểm** trong bài kiểm tra viết. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG VÀ MỞ RỘNG (Tiết 22: 10 phút)

#### a) Mục tiêu:
- Vận dụng bất phương trình giải bài toán tuyển chọn thể thao (Bài 2.32); mở rộng hiểu biết về Bất đẳng thức Cô-si (AM-GM).

#### b) Nội dung:
- Giải Bài 2.32 SGK trang 43 và đọc mục "Em có biết": Bất đẳng thức giữa trung bình cộng và trung bình nhân.

#### c) Sản phẩm:
- Lời giải Bài 2.32: Cần ném ít nhất 10 quả bóng vào rổ; công thức BĐT Cô-si cho 2 số không âm: $\\frac{a+b}{2} \\ge \\sqrt{ab}$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao Bài 2.32 SGK trang 43:<br>"Mỗi bạn ném 15 quả bóng vào rổ. Vào rổ cộng 2 điểm, ra ngoài trừ 1 điểm. Đạt từ 15 điểm trở lên sẽ được chọn vào đội tuyển. Hỏi cần ném ít nhất bao nhiêu quả vào rổ?"<br>- **GV:** Giới thiệu ngắn gọn mục "Em có biết": Bất đẳng thức AM-GM của nhà toán học Cauchy (Cô-si).<br>- **HS:** Tiếp nhận nhiệm vụ.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Gọi $y$ là số quả bóng ném vào rổ ($0 \\le y \\le 15, y \\in \\mathbb{N}$). Số quả ra ngoài là $15 - y$.<br>Lập BPT: $2y - (15 - y) \\ge 15$.<br>$3y - 15 \\ge 15$<br>$3y \\ge 30$<br>$y \\ge 10$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Báo cáo kết quả: Cần ném ít nhất 10 quả vào rổ.<br>- **HS:** Đọc công thức BĐT Cauchy trong SGK: $\\frac{a+b}{2} \\ge \\sqrt{ab}$ với $a, b \\ge 0$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chốt bài học. Khẳng định Chương II cung cấp công cụ bất đẳng thức và bất phương trình cực kỳ quan trọng cho các lớp học sau và kỳ thi vào lớp 10. | **1. BÀI TẬP 2.32 (SGK TRANG 43):**<br><br>- Gọi số quả bóng ném vào rổ là $y$ ($0 \\le y \\le 15, y \\in \\mathbb{N}$).<br>- Số quả bóng ném ra ngoài là: $15 - y$ (quả).<br>- Điểm đạt được là: $2y - (15 - y) = 3y - 15$ (điểm).<br><br>- Để được chọn vào đội tuyển thì số điểm phải từ 15 trở lên, ta có bất phương trình:<br>$3y - 15 \\ge 15$<br>$3y \\ge 30$<br>$y \\ge 10$.<br><br>**Kết luận:** Học sinh cần ném **ít nhất 10 quả vào rổ**.<br><br>**2. MỞ RỘNG: BẤT ĐẲNG THỨC CAUCHY (AM-GM):**<br>- Cho hai số không âm $a, b \\ge 0$. Ta luôn có:<br>$$\\frac{a + b}{2} \\ge \\sqrt{ab}$$<br>Dấu đẳng thức xảy ra khi và chỉ khi $a = b$.<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Hoàn thiện toàn bộ bài tập cuối chương II vào vở.<br>- Ôn tập chuẩn bị cho bài kiểm tra định kỳ.<br>- Đọc trước nội dung Chương III: Căn bậc hai và căn bậc ba. |
`;

module.exports = {
  BAI_01_MD,
  BAI_02_MD,
  BAI_03_MD,
  BAI_04_MD
};
