# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 6**  
**CHỦ ĐỀ: BÀI 12. BỘI CHUNG. BỘI CHUNG NHỎ NHẤT (2 TIẾT)**  
**Phân phối chương trình:** Tiết 23, 24 — Tuần 8  
**Thời lượng thực hiện:** 02 tiết (90 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 49 – 54)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Nhận biết được khái niệm bội chung ($BC$) và bội chung nhỏ nhất ($BCNN$) của hai hoặc nhiều số tự nhiên; nắm vững ký hiệu $BC(a, b)$ và $BCNN(a, b)$.
- Nắm vững và thực hiện thành thạo quy tắc 3 bước tìm $BCNN$ bằng cách phân tích các số ra thừa số nguyên tố.
- Vận dụng $BCNN$ để tìm mẫu chung và thực hiện quy đồng mẫu các phân số.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự tìm bội của từng số để tìm bội chung, chủ động tìm BCNN bằng phân tích thừa số nguyên tố.
- Giao tiếp và hợp tác: Làm việc nhóm phân tích bài toán thực tế có chu kỳ lặp lại.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: So sánh sự giống và khác nhau giữa quy tắc tìm ƯCLN và BCNN; lập luận mối quan hệ $BC(a, b) = B(BCNN(a, b))$.
- Giải quyết vấn đề toán học: Vận dụng BCNN vào quy đồng mẫu phân số và giải bài toán chuyển động lặp lại theo chu kỳ.

### c) Năng lực số (NLS)
- ***[NLS: 5.3.TC1a] Sử dụng lệnh LCM trong phần mềm bảng tính hoặc phím chức năng trên máy tính cầm tay để tìm BCNN của các số lớn.***

### d) Năng lực Trí tuệ Nhân tạo (AI)
- ***[AI: 6.C1.1] Mô tả cách AI xử lý dữ liệu đầu vào là các số tự nhiên để tìm ra bội chung nhỏ nhất thông qua thuật toán phân tích thừa số (Áp dụng: tiết 1, 2).***

## 3. Về phẩm chất
- Chăm chỉ: Kiên trì tính toán tích các lũy thừa với số mũ lớn nhất.
- Trách nhiệm: Cẩn thận đối chiếu kết quả tính tay với công cụ số để rèn tính chuẩn xác.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài giảng PowerPoint, tệp bảng tính Excel có hàm LCM, mô hình thuật toán AI phân tích thừa số, tivi/máy chiếu, phiếu học tập nhóm.
2. **Học sinh:** SGK Toán 6 (Tập 1), vở ghi bài, máy tính cầm tay Casio FX-580VNX/880BTG.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)

#### a) Mục tiêu:
- Đặt vấn đề bằng bài toán thực tế chu kỳ gặp nhau của hai tuyến xe buýt để dẫn dắt vào khái niệm bội chung nhỏ nhất.

#### b) Nội dung:
- Tình huống: Tuyến xe buýt A cứ 15 phút xuất bến một chuyến, tuyến xe buýt B cứ 20 phút xuất bến một chuyến. Nếu hai xe cùng xuất bến lúc 6 giờ sáng thì sau ít nhất bao nhiêu phút hai xe lại cùng xuất bến một lần nữa?

#### c) Sản phẩm:
- HS nhận xét: Khoảng thời gian hai xe cùng xuất bến phải là bội của 15 và bội của 20; thời gian ít nhất là số nhỏ nhất khác 0 trong các bội chung đó (60 phút = 1 giờ).

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu bài toán thực tế xe buýt và yêu cầu HS suy nghĩ tìm thời điểm hai xe cùng xuất bến lần tiếp theo.<br>- **HS:** Thảo luận cặp đôi trong 2 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Liệt kê các thời điểm xe A xuất bến: 15, 30, 45, 60, 75, ... phút. Xe B xuất bến: 20, 40, 60, 80, ... phút. Hai xe cùng xuất bến tại mốc 60 phút.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trả lời: Sau ít nhất 60 phút (tức lúc 7 giờ sáng) hai xe lại cùng xuất bến.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** 60 là bội chung nhỏ nhất của 15 và 20. Ta vào bài học hôm nay. | **TÌNH HUỐNG KHỞI ĐỘNG:**<br><br>- Tuyến A: $B(15) = \{0; 15; 30; 45; 60; 75; ...\}$.<br>- Tuyến B: $B(20) = \{0; 20; 40; 60; 80; ...\}$.<br>- Các bội chung khác 0: $60; 120; ...$<br>- Bội chung nhỏ nhất khác 0 là: $60$.<br><br>Khái niệm bội chung, BCNN và thuật toán tìm kiếm như thế nào? |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)

### 1. Hoạt động 2.1: Bội chung và Bội chung nhỏ nhất (18 phút)

#### a) Mục tiêu:
- Định nghĩa bội chung, bội chung nhỏ nhất; ký hiệu $BC(a, b)$ và $BCNN(a, b)$.
- Nắm vững mối liên hệ: Mọi bội chung đều là bội của BCNN.

#### b) Nội dung:
- Đọc định nghĩa SGK; thực hiện Hoạt động 1, 2 SGK trang 49.

#### c) Sản phẩm:
- Khái niệm và ký hiệu vào vở; lời giải Luyện tập 1 SGK.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Định nghĩa: Bội chung của hai hay nhiều số là bội của tất cả các số đó. Bội chung nhỏ nhất của hai hay nhiều số là số nhỏ nhất **khác 0** trong tập hợp các bội chung của các số đó.<br>- **HS:** Ghi bài và chú ý cụm từ "khác 0".<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tìm $BC(4, 6)$ và chỉ ra $BCNN(4, 6)$.<br>- **GV:** Nhấn mạnh: Nếu có số 0 thì số nhỏ nhất luôn là 0, do đó định nghĩa BCNN bắt buộc phải loại số 0.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** $BC(4, 6) = \{0; 12; 24; 36; ...\} \Rightarrow BCNN(4, 6) = 12$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chốt nhận xét: $BC(a, b) = B(BCNN(a, b))$. | **1. BỘI CHUNG VÀ BỘI CHUNG NHỎ NHẤT:**<br><br>- **Định nghĩa:**<br>+ Bội chung của hai hay nhiều số là bội của tất cả các số đó.<br>Ký hiệu: $BC(a, b)$, $BC(a, b, c)$.<br>+ Bội chung nhỏ nhất của hai hay nhiều số là số nhỏ nhất **khác 0** trong tập hợp các bội chung của các số đó.<br>Ký hiệu: $BCNN(a, b)$, $BCNN(a, b, c)$.<br><br>- **Nhận xét quan trọng:**<br>Tất cả các bội chung của hai hay nhiều số đều là bội của BCNN của chúng:<br>$$BC(a, b) = B(BCNN(a, b))$$ |

---

### 2. Hoạt động 2.2: Quy tắc tìm BCNN bằng phân tích ra thừa số nguyên tố (17 phút)

#### a) Mục tiêu:
- Nắm vững quy tắc 3 bước tìm BCNN bằng cách phân tích ra thừa số nguyên tố.
- So sánh đối chiếu phân biệt rõ với quy tắc tìm ƯCLN.
- ***[NLS: 5.3.TC1a] Sử dụng lệnh LCM trong phần mềm bảng tính hoặc phím chức năng trên máy tính cầm tay để tìm BCNN của các số lớn.***
- ***[AI: 6.C1.1] Mô tả cách AI xử lý dữ liệu đầu vào là các số tự nhiên để tìm ra bội chung nhỏ nhất thông qua thuật toán phân tích thừa số.***

#### b) Nội dung:
- Tìm hiểu quy tắc SGK trang 51; thực hành tìm $BCNN(9, 12)$ và $BCNN(12, 18, 30)$; trải nghiệm hàm LCM trên Excel và lắng nghe giải thích thuật toán AI.

#### c) Sản phẩm:
- Quy tắc 3 bước vào vở; $BCNN(9, 12) = 36$; $BCNN(12, 18, 30) = 180$.
- Bảng tính Excel hiển thị `=LCM(12, 18, 30) = 180`.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu quy tắc 3 bước tìm BCNN:<br>+ Bước 1: Phân tích mỗi số ra thừa số nguyên tố.<br>+ Bước 2: Chọn ra các thừa số nguyên tố **chung và riêng**.<br>+ Bước 3: Lập tích các thừa số đã chọn, mỗi thừa số lấy với số mũ **lớn nhất** của nó.<br>- ***[NLS: 5.3.TC1a] GV hướng dẫn học sinh thao tác trên bảng tính Excel: "Gõ lệnh =LCM(12, 18, 30) hoặc dùng phím BCNN trên máy tính Casio để kiểm tra nhanh kết quả tính tay."***<br>- ***[AI: 6.C1.1] GV mô tả cách hệ thống AI xử lý: "Khi nhận đầu vào là các số tự nhiên, AI sử dụng thuật toán phân tích thừa số nguyên tố và giải thuật Euclid mở rộng để tìm BCNN chỉ trong vài mili-giây, sau đó xuất ra từng bước giải thích logic cho người dùng."***<br>- **HS:** Ghi bài và đối chiếu giữa ƯCLN (chung, số mũ nhỏ nhất) với BCNN (chung và riêng, số mũ lớn nhất).<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thực hiện tìm $BCNN(12, 18, 30)$ ra nháp.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày: $12 = 2^2 \cdot 3$; $18 = 2 \cdot 3^2$; $30 = 2 \cdot 3 \cdot 5$. Thừa số chung và riêng: 2, 3, 5. Lấy số mũ lớn nhất: $2^2, 3^2, 5^1$. Kết quả $BCNN = 2^2 \cdot 3^2 \cdot 5 = 4 \cdot 9 \cdot 5 = 180$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa kiến thức, khen ngợi học sinh. | **2. QUY TẮC TÌM BCNN (3 BƯỚC):**<br><br>- **Bước 1:** Phân tích mỗi số ra thừa số nguyên tố.<br>- **Bước 2:** Chọn ra các thừa số nguyên tố **chung và riêng**.<br>- **Bước 3:** Lập tích các thừa số đã chọn, mỗi thừa số lấy với số mũ **lớn nhất** của nó. Tích đó là BCNN phải tìm.<br><br>**Ví dụ:** Tìm $BCNN(12, 18, 30)$:<br>- $12 = 2^2 \cdot 3$<br>- $18 = 2 \cdot 3^2$<br>- $30 = 2 \cdot 3 \cdot 5$<br>$\Rightarrow BCNN(12, 18, 30) = 2^2 \cdot 3^2 \cdot 5 = 180$.<br><br>***(Tích hợp NLS 5.3.TC1a: Sử dụng lệnh =LCM() trong Excel hoặc máy tính cầm tay kiểm tra kết quả BCNN nhanh chóng.)***<br>***(Tích hợp AI 6.C1.1: Mô tả quy trình thuật toán AI phân tích dữ liệu số học để tìm BCNN tự động.)*** |

---

### 3. Hoạt động 2.3: Ứng dụng quy đồng mẫu các phân số (10 phút)

#### a) Mục tiêu:
- Vận dụng BCNN để tìm mẫu chung nhỏ nhất và thực hiện quy đồng mẫu các phân số.

#### b) Nội dung:
- Quy đồng mẫu hai phân số: $\frac{5}{12}$ và $\frac{7}{30}$.

#### c) Sản phẩm:
- Mẫu chung $BCNN(12, 30) = 60$; các phân số sau quy đồng: $\frac{25}{60}$ và $\frac{14}{60}$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu quy trình quy đồng mẫu phân số:<br>1. Tìm mẫu chung bằng cách tìm BCNN của các mẫu số.<br>2. Tìm thừa số phụ của mỗi mẫu.<br>3. Nhân cả tử và mẫu với thừa số phụ tương ứng.<br>Yêu cầu HS quy đồng $\frac{5}{12}$ và $\frac{7}{30}$.<br>- **HS:** Làm việc cá nhân.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tìm $BCNN(12, 30) = 60$. Thừa số phụ: $60 : 12 = 5$; $60 : 30 = 2$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** $\frac{5}{12} = \frac{5 \cdot 5}{12 \cdot 5} = \frac{25}{60}$; $\frac{7}{30} = \frac{7 \cdot 2}{30 \cdot 2} = \frac{14}{60}$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khẳng định quy đồng bằng BCNN giúp mẫu số gọn nhất, tính toán cộng trừ phân số sau này thuận tiện nhất. | **3. ỨNG DỤNG QUY ĐỒNG MẪU PHÂN SỐ:**<br><br>- **Quy tắc:** Để quy đồng mẫu nhiều phân số, ta lấy mẫu chung là $BCNN$ của các mẫu số.<br><br>**Ví dụ:** Quy đồng mẫu $\frac{5}{12}$ và $\frac{7}{30}$:<br>- Mẫu chung: $BCNN(12, 30) = 60$.<br>- Thừa số phụ: $60 : 12 = 5$; $60 : 30 = 2$.<br>- Quy đồng:<br>$$\frac{5}{12} = \frac{5 \cdot 5}{12 \cdot 5} = \frac{25}{60}; \quad \frac{7}{30} = \frac{7 \cdot 2}{30 \cdot 2} = \frac{14}{60}$$ |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (25 phút)

#### a) Mục tiêu:
- Luyện tập thành thạo kỹ năng tìm BCNN của hai hoặc ba số và quy đồng mẫu các phân số.

#### b) Nội dung:
- Giải Bài 2.36, 2.37, 2.38 SGK trang 53.

#### c) Sản phẩm:
- Lời giải chính xác trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao nhiệm vụ Bài 2.36 (tìm BCNN), Bài 2.38 (quy đồng mẫu phân số).<br>- **HS:** Làm vào vở, 2 HS lên bảng.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tự giác làm bài.<br>- **GV:** Đi quan sát, nhắc nhở chọn đúng số mũ lớn nhất.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Yêu cầu HS nhận xét bài làm trên bảng.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa lời giải và củng cố phương pháp. | **GIẢI BÀI TẬP SGK TRANG 53:**<br><br>1. **Bài 2.36:** Tìm $BCNN$:<br>a) $BCNN(6, 8)$: $6 = 2 \cdot 3; 8 = 2^3 \Rightarrow BCNN(6, 8) = 2^3 \cdot 3 = 24$.<br>b) $BCNN(10, 1, 12)$:<br>Vì $BCNN(a, 1) = a$ nên $BCNN(10, 1, 12) = BCNN(10, 12) = 60$.<br><br>2. **Bài 2.38:** Quy đồng mẫu số:<br>a) $\frac{3}{8}$ và $\frac{5}{24}$:<br>Vì $24 \vdots 8$ nên mẫu chung là $24$.<br>$\frac{3}{8} = \frac{3 \cdot 3}{8 \cdot 3} = \frac{9}{24}$; giữ nguyên $\frac{5}{24}$. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)

#### a) Mục tiêu:
- Vận dụng BCNN giải quyết bài toán thực tế về số học sinh khối 6 xếp hàng (Bài 2.41 SGK).

#### b) Nội dung:
- Giải Bài 2.41 SGK: Học sinh khối 6 khi xếp hàng 2, hàng 3, hàng 6 đều vừa đủ hàng. Biết số học sinh trong khoảng từ 30 đến 50. Tính số học sinh khối 6.

#### c) Sản phẩm:
- Lời giải bài toán thực tế: Số học sinh là bội chung của 2, 3, 6; kết quả có thể là 36, 42, 48 học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu Bài 2.41 SGK: "Số học sinh khi xếp hàng 2, hàng 3, hàng 6 đều vừa đủ hàng thì số học sinh có quan hệ gì với 2, 3, 6?"<br>- **HS:** Thảo luận nhanh.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Số học sinh là bội chung của 2, 3, 6.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** $BCNN(2, 3, 6) = 6$. Tập hợp bội chung: $BC(2, 3, 6) = \{0; 6; 12; 18; 24; 30; 36; 42; 48; 54; ...\}$. Trong khoảng từ 30 đến 50 em, các số thỏa mãn là $36, 42, 48$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Đánh giá tiết học, tổng kết Chương II và giao bài tự học ở nhà. | **BÀI 2.41 (VẬN DỤNG THỰC TẾ):**<br><br>Gọi số học sinh khối 6 là $a$ ($a \in \mathbb{N}^*$, $30 \le a \le 50$).<br>Vì khi xếp hàng 2, hàng 3, hàng 6 đều vừa đủ hàng nên:<br>$$a \in BC(2, 3, 6)$$<br>Ta có $BCNN(2, 3, 6) = 6$.<br>$\Rightarrow a \in B(6) = \{0; 6; 12; 18; 24; 30; 36; 42; 48; 54; ...\}$.<br>Vì $30 \le a \le 50$ nên $a \in \{30; 36; 42; 48\}$.<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Học thuộc quy tắc 3 bước tìm BCNN.<br>- Hoàn thành các bài tập còn lại SGK trang 53 – 54.<br>- Ôn tập toàn bộ Chương II để chuẩn bị tiết sau làm bài tập ôn chương. |
