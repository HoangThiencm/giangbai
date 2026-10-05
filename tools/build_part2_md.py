# -*- coding: utf-8 -*-
import os

OUT_DIR = os.path.abspath(r"TROLYTHIEN\1_SOAN_KHBD\Ket_qua")
os.makedirs(OUT_DIR, exist_ok=True)

MD_05 = """# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 6**  
**CHỦ ĐỀ: BÀI 10. SỐ NGUYÊN TỐ (2 TIẾT)**  
**Phân phối chương trình:** Tiết 18, 19 — Tuần 6, 7  
**Thời lượng thực hiện:** 02 tiết (90 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 38 – 42)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Nhận biết được khái niệm số nguyên tố, hợp số; phân biệt được số nguyên tố và hợp số.
- Biết cách dùng bảng số nguyên tố nhỏ hơn 100 để tra cứu và nhận biết số nguyên tố.
- Thực hiện được việc phân tích một số tự nhiên lớn hơn 1 ra thừa số nguyên tố bằng phương pháp sơ đồ cột và sơ đồ cây; viết gọn kết quả dưới dạng tích các lũy thừa.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự tìm hiểu bảng các số nguyên tố, chủ động thực hành phân tích số ra thừa số nguyên tố.
- Giao tiếp và hợp tác: Trao đổi nhóm đối chiếu kết quả phân tích theo các nhánh sơ đồ cây khác nhau để thấy kết quả cuối cùng là duy nhất.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: Lập luận giải thích một số tự nhiên lớn hơn 2 có chữ số tận cùng là chẵn hoặc 5 (khác 5) thì chắc chắn là hợp số.
- Giải quyết vấn đề toán học: Vận dụng phân tích ra thừa số nguyên tố để giải các bài toán chia nhóm và xác định số ước của một số.

## 3. Về phẩm chất
- Chăm chỉ: Kiên trì thực hiện phép chia liên tiếp cho các số nguyên tố từ nhỏ đến lớn.
- Trách nhiệm: Cẩn thận trong cách ghi lũy thừa, kiểm tra lại tích các thừa số để đảm bảo tính chính xác.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài giảng điện tử PowerPoint, bảng số nguyên tố nhỏ hơn 100 (Sàng Eratosthenes), phiếu học tập sơ đồ cây.
2. **Học sinh:** SGK Toán 6 (Tập 1), vở ghi bài, bút màu, máy tính cầm tay để kiểm tra phép chia.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)

#### a) Mục tiêu:
- Tạo hứng thú khám phá thông qua hoạt động đếm số lượng ước của các số tự nhiên từ 1 đến 11.

#### b) Nội dung:
- Tìm tập hợp các ước của số 1, số 2, số 6, số 7, số 9, số 11.

#### c) Sản phẩm:
- Bảng phân loại: số chỉ có 1 ước (số 1), số có đúng 2 ước (2, 7, 11), số có nhiều hơn 2 ước (6, 9).

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Yêu cầu HS tìm các ước của các số sau và đếm số lượng ước: $1; 2; 6; 7; 9; 11$.<br>- **HS:** Làm việc cá nhân trong 2 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Liệt kê: $Ư(1)=\{1\}$ (1 ước); $Ư(2)=\{1; 2\}$ (2 ước); $Ư(6)=\{1; 2; 3; 6\}$ (4 ước); $Ư(7)=\{1; 7\}$ (2 ước); $Ư(9)=\{1; 3; 9\}$ (3 ước); $Ư(11)=\{1; 11\}$ (2 ước).<br>- **GV:** Hướng dẫn chia các số này thành các nhóm theo số lượng ước.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện 1 HS phát biểu 3 nhóm: nhóm có 1 ước, nhóm có đúng 2 ước, nhóm có từ 3 ước trở lên.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Dẫn dắt: Nhóm có đúng 2 ước được gọi là số nguyên tố; nhóm có nhiều hơn 2 ước gọi là hợp số. | **KHÁM PHÁ KHỞI ĐỘNG:**<br><br>- Số 1: có đúng 1 ước.<br>- Số 2, 7, 11: có đúng 2 ước (là 1 và chính nó).<br>- Số 6, 9: có nhiều hơn 2 ước.<br><br>Số tự nhiên lớn hơn 1 có đúng 2 ước gọi là gì? Số có nhiều hơn 2 ước gọi là gì? |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)

### 1. Hoạt động 2.1: Số nguyên tố và hợp số (22 phút)

#### a) Mục tiêu:
- Nắm vững định nghĩa số nguyên tố, hợp số; lưu ý trường hợp đặc biệt của số 0 và số 1; biết dùng Bảng số nguyên tố nhỏ hơn 100.

#### b) Nội dung:
- Đọc định nghĩa SGK; thực hiện Hoạt động 1, 2; quan sát Bảng số nguyên tố nhỏ hơn 100.

#### c) Sản phẩm:
- Định nghĩa vào vở; lời giải Luyện tập 1 SGK trang 39.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giới thiệu định nghĩa: Số nguyên tố là số tự nhiên lớn hơn 1, chỉ có hai ước là 1 và chính nó. Hợp số là số tự nhiên lớn hơn 1, có nhiều hơn hai ước.<br>- **GV:** "Số 0 và số 1 có phải là số nguyên tố hay hợp số không? Số 2 có gì đặc biệt?"<br>- **HS:** Suy nghĩ và trả lời.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhận xét: Số 0 và 1 không là số nguyên tố cũng không là hợp số. Số 2 là số nguyên tố chẵn duy nhất và là số nguyên tố nhỏ nhất.<br>- **GV:** Giới thiệu Bảng số nguyên tố nhỏ hơn 100 cuối SGK.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Thực hiện Luyện tập 1: Trong các số $11; 12; 25$, số nào là số nguyên tố, số nào là hợp số?<br>-> $11$ là số nguyên tố; $12$ và $25$ là hợp số.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chốt kiến thức và quy tắc nhận biết nhanh: Số chẵn lớn hơn 2 luôn là hợp số. | **1. SỐ NGUYÊN TỐ VÀ HỢP SỐ:**<br><br>- **Số nguyên tố:** Là số tự nhiên lớn hơn 1, chỉ có hai ước là 1 và chính nó.<br>*(Ví dụ: 2, 3, 5, 7, 11, 13, 17, 19, ...)*<br>- **Hợp số:** Là số tự nhiên lớn hơn 1, có nhiều hơn hai ước.<br>*(Ví dụ: 4, 6, 8, 9, 10, 12, ...)*<br><br>- **Chú ý quan trọng:**<br>+ Số 0 và số 1 không là số nguyên tố và không là hợp số.<br>+ Số 2 là số nguyên tố nhỏ nhất và là số nguyên tố chẵn duy nhất.<br>+ Để chứng minh một số tự nhiên $a > 1$ là hợp số, chỉ cần chỉ ra $a$ có một ước khác 1 và khác $a$. |

---

### 2. Hoạt động 2.2: Phân tích một số ra thừa số nguyên tố (23 phút)

#### a) Mục tiêu:
- Hiểu thế nào là phân tích một số ra thừa số nguyên tố.
- Nắm vững 2 cách phân tích: theo sơ đồ cây và theo sơ đồ cột; viết gọn kết quả dưới dạng tích các lũy thừa.

#### b) Nội dung:
- Quan sát Ví dụ 2, Ví dụ 3 SGK trang 40; thực hành phân tích số 60 và 84.

#### c) Sản phẩm:
- Kết quả phân tích: $60 = 2^2 \cdot 3 \cdot 5$; $84 = 2^2 \cdot 3 \cdot 7$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu định nghĩa: Phân tích một số tự nhiên lớn hơn 1 ra thừa số nguyên tố là viết số đó dưới dạng một tích các thừa số nguyên tố.<br>- **GV:** Hướng dẫn 2 cách thực hiện:<br>1. Sơ đồ cây (tách dần thành các tích).<br>2. Sơ đồ cột (chia liên tiếp cho các số nguyên tố từ nhỏ đến lớn).<br>- **HS:** Theo dõi ví dụ mẫu phân tích số 60.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thực hành phân tích số 84 theo sơ đồ cột vào vở.<br>- **GV:** Nhắc nhở chia theo thứ tự các số nguyên tố: 2, 3, 5, 7... cho đến khi được thương là 1.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày trên bảng: $84 : 2 = 42$; $42 : 2 = 21$; $21 : 3 = 7$; $7 : 7 = 1$. Kết quả $84 = 2^2 \cdot 3 \cdot 7$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khẳng định: Dù phân tích theo sơ đồ cây hay sơ đồ cột thì kết quả phân tích cuối cùng ra thừa số nguyên tố của một số là duy nhất (chỉ khác thứ tự thừa số). | **2. PHÂN TÍCH RA THỪA SỐ NGUYÊN TỐ:**<br><br>- **Định nghĩa:** Phân tích một số tự nhiên lớn hơn 1 ra thừa số nguyên tố là viết số đó dưới dạng một tích các thừa số nguyên tố.<br><br>- **Phương pháp sơ đồ cột (Ví dụ số 60):**<br>$$\begin{array}{r|l} 60 & 2 \\ 30 & 2 \\ 15 & 3 \\ 5 & 5 \\ 1 & \end{array}$$<br>Ta viết: $60 = 2 \cdot 2 \cdot 3 \cdot 5 = 2^2 \cdot 3 \cdot 5$.<br><br>- **Nhận xét:** Trong cách viết, các thừa số nguyên tố thường được viết theo thứ tự từ bé đến lớn và các thừa số giống nhau được viết dưới dạng lũy thừa. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (25 phút)

#### a) Mục tiêu:
- Rèn luyện kỹ năng phân loại số nguyên tố, hợp số và phân tích các số tự nhiên thành tích thừa số nguyên tố.

#### b) Nội dung:
- Giải Bài 2.17, 2.18, 2.19 SGK trang 41.

#### c) Sản phẩm:
- Lời giải chính xác trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Yêu cầu HS hoàn thành Bài 2.17 (xác định số nguyên tố, hợp số), Bài 2.18 (phân tích số 70, 115 ra thừa số nguyên tố).<br>- **HS:** Làm việc cá nhân.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tự giác làm bài, tra cứu bảng số nguyên tố khi cần.<br>- **GV:** Quan sát, uốn nắn cách trình bày sơ đồ cột.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Gọi 2 HS lên bảng thực hiện.<br>- **HS:** Dưới lớp nhận xét, đối chiếu.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa lời giải và biểu dương các em phân tích nhanh, chính xác. | **GIẢI BÀI TẬP SGK TRANG 41:**<br><br>1. **Bài 2.17:**<br>- Các số nguyên tố là: $17; 23$.<br>- Các hợp số là: $12; 25; 38$ (vì ngoài 1 và chính nó chúng còn có các ước khác: 12 chia hết cho 2, 25 chia hết cho 5, 38 chia hết cho 2).<br><br>2. **Bài 2.18:** Phân tích ra thừa số nguyên tố:<br>- $70 = 2 \cdot 5 \cdot 7$.<br>- $115 = 5 \cdot 23$.<br><br>3. **Bài 2.19:** Các khẳng định sau đúng hay sai?<br>a) "Mọi số nguyên tố đều là số lẻ" -> **Sai** (vì số 2 là số chẵn).<br>b) "Mọi số chẵn đều là hợp số" -> **Sai** (vì số 2 là số nguyên tố). |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)

#### a) Mục tiêu:
- Mở rộng kiến thức về ứng dụng thực tế của số nguyên tố trong bảo mật thông tin và mật mã học hiện đại.

#### b) Nội dung:
- Đọc mục "Em có biết": Số nguyên tố và bảo mật thông tin; tìm hiểu về hệ mật mã khóa công khai RSA.

#### c) Sản phẩm:
- Hiểu biết ban đầu về vai trò của tích hai số nguyên tố cực lớn trong mã hóa giao dịch ngân hàng và Internet.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giới thiệu: "Các số nguyên tố không chỉ là khái niệm lý thuyết mà là nền tảng của toàn bộ hệ thống an ninh mạng ngày nay! Khi các em thực hiện chuyển tiền ngân hàng hay đăng nhập mạng, hệ thống dùng tích của hai số nguyên tố cực lớn (hàng trăm chữ số). Máy tính có thể nhân 2 số rất nhanh, nhưng từ tích đó phân tích ngược lại để tìm 2 số ban đầu thì siêu máy tính phải mất hàng ngàn năm!"<br>- **HS:** Lắng nghe hào hứng.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Đọc phần "Em có biết" SGK trang 42.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Nêu cảm nghĩ về vẻ đẹp kỳ diệu và ứng dụng thực tiễn của Toán học.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Tổng kết bài học và hướng dẫn chuẩn bị tiết sau: Luyện tập chung. | **ỨNG DỤNG SỐ NGUYÊN TỐ (EM CÓ BIẾT):**<br><br>- Trong kỷ nguyên số, các số nguyên tố rất lớn được dùng để tạo ra **khóa bảo mật mã hóa thông tin (Mật mã RSA)**.<br>- Nhờ tính chất: "Nhân hai số nguyên tố rất dễ, nhưng phân tích một số cực lớn ra tích hai thừa số nguyên tố lại cực kỳ khó", dữ liệu ngân hàng và thông tin cá nhân của người dùng trên toàn cầu luôn được bảo vệ an toàn.<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Ghi nhớ bảng số nguyên tố nhỏ hơn 30: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29.<br>- Luyện tập phân tích các số $120, 180, 200$ ra thừa số nguyên tố.<br>- Chuẩn bị tiết 20: Luyện tập chung. |
"""

MD_06 = """# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 6**  
**CHỦ ĐỀ: CHƯƠNG II: TÍNH CHIA HẾT TRONG TẬP HỢP CÁC SỐ TỰ NHIÊN (TIẾT 20: LUYỆN TẬP CHUNG)**  
**Phân phối chương trình:** Tiết 20 — Tuần 7  
**Thời lượng thực hiện:** 01 tiết (45 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 43)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Hệ thống hóa và củng cố toàn bộ các kiến thức trọng tâm đã học: Quan hệ chia hết, tính chất chia hết của một tổng, các dấu hiệu chia hết cho 2, 5, 9, 3, định nghĩa số nguyên tố, hợp số và kỹ năng phân tích một số ra thừa số nguyên tố.
- Vận dụng linh hoạt các kiến thức trên vào giải quyết các bài toán viết số theo điều kiện chia hết, phân tích biểu thức tích ra thừa số nguyên tố và giải bài toán thực tế.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự hệ thống hóa kiến thức bằng sơ đồ tư duy, độc lập hoàn thành các bài tập phân tích và tìm ẩn số.
- Giao tiếp và hợp tác: Tương tác nhóm trao đổi cách phân tích tích các lũy thừa ra thừa số nguyên tố mà không cần tính giá trị tích.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: Lập luận phối hợp nhiều dấu hiệu chia hết cùng lúc; phân tích số nguyên tố sinh đôi.
- Giải quyết vấn đề toán học: Vận dụng ước số và quan hệ chia hết để giải bài toán chia tổ học sinh dự án nhỏ.

## 3. Về phẩm chất
- Chăm chỉ: Chủ động ôn tập, cẩn thận trong việc tách thừa số nguyên tố của các cơ số hợp số.
- Trách nhiệm: Hợp tác tích cực với các thành viên trong nhóm, trung thực khi báo cáo kết quả.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài giảng PowerPoint, sơ đồ tư duy tổng hợp các nhánh kiến thức Chương II, phiếu bài tập nhóm.
2. **Học sinh:** SGK Toán 6 (Tập 1), vở ghi bài, nháp, máy tính cầm tay kiểm tra kết quả.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)

#### a) Mục tiêu:
- Tái hiện nhanh các kiến thức đã học ở các bài 8, 9, 10; tạo không khí sôi nổi bước vào tiết luyện tập chung.

#### b) Nội dung:
- Trò chơi trắc nghiệm nhanh 4 câu hỏi về dấu hiệu chia hết và số nguyên tố.

#### c) Sản phẩm:
- Câu trả lời đúng của học sinh: Số chia hết cho 2 và 5 tận cùng là 0; số nguyên tố nhỏ nhất là 2; số 0 và 1 không là số nguyên tố; hợp số có từ 3 ước trở lên.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu 3 câu hỏi nhanh:<br>1. Dấu hiệu một số vừa chia hết cho 2 vừa chia hết cho 5?<br>2. Số nguyên tố chẵn duy nhất là số nào?<br>3. Số 1 có phải là số nguyên tố không?<br>- **HS:** Chuẩn bị giơ tay trả lời.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Nhớ lại kiến thức cũ.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trả lời chính xác: (1) Tận cùng là chữ số 0; (2) Số 2; (3) Số 1 không là số nguyên tố và không là hợp số.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, dẫn dắt vào tiết Luyện tập chung trang 43. | **KHỞI ĐỘNG ÔN TẬP:**<br><br>- Số chia hết cho 2 và 5: Tận cùng là 0.<br>- Số 2: Số nguyên tố chẵn duy nhất.<br>- Số 0 và 1: Không là số nguyên tố, không là hợp số. |

---

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức (10 phút)

#### a) Mục tiêu:
- Hệ thống hóa kiến thức toàn diện bằng Sơ đồ tư duy liên kết: Chia hết -> Dấu hiệu chia hết -> Số nguyên tố, hợp số -> Phân tích thừa số nguyên tố.
- Phân tích kỹ thuật phân tích số ra thừa số nguyên tố qua Ví dụ 3 SGK trang 43.

#### b) Nội dung:
- Quan sát sơ đồ tư duy; phân tích 2 cách phân tích số 140 trong Ví dụ 3 SGK.

#### c) Sản phẩm:
- Sơ đồ tư duy trong vở; kết quả $140 = 2^2 \cdot 5 \cdot 7$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu sơ đồ tư duy và Ví dụ 3 SGK trang 43: Phân tích số 140 ra thừa số nguyên tố theo sơ đồ cây và sơ đồ cột.<br>- **HS:** Quan sát bảng chiếu và thảo luận.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** So sánh 2 cách: Sơ đồ cây tách $140 = 5 \cdot 28 = 5 \cdot (2 \cdot 14) = 5 \cdot 2 \cdot (2 \cdot 7)$; Sơ đồ cột chia liên tiếp cho $2, 2, 5, 7$.<br>- **GV:** Nhấn mạnh: Cả hai cách đều cho kết quả $140 = 2^2 \cdot 5 \cdot 7$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện 1 HS nhắc lại các bước phân tích.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chốt lại: Tùy sự thuận tiện có thể chọn sơ đồ cây hoặc sơ đồ cột. | **HỆ THỐNG KIẾN THỨC CỐT LÕI (VÍ DỤ 3 SGK):**<br><br>Phân tích số 140 ra thừa số nguyên tố:<br><br>- **Sơ đồ cây:**<br>$$140 = 5 \cdot 28 = 5 \cdot (2 \cdot 14) = 5 \cdot 2 \cdot (2 \cdot 7) = 2^2 \cdot 5 \cdot 7$$<br>- **Sơ đồ cột:**<br>$$\begin{array}{r|l} 140 & 2 \\ 70 & 2 \\ 35 & 5 \\ 7 & 7 \\ 1 & \end{array}$$<br>$$\Rightarrow 140 = 2^2 \cdot 5 \cdot 7$$ |

---

### 2. Hoạt động 2.2: Giải quyết bài tập trọng tâm (22 phút)

#### a) Mục tiêu:
- Giải quyết 3 bài tập trọng tâm: Bài 2.25 (viết số theo điều kiện chia hết), Bài 2.26 (phân tích tích lũy thừa ra thừa số nguyên tố), Bài 2.27 (tìm ẩn số $x$ thỏa mãn tính chất chia hết).

#### b) Nội dung:
- Làm việc theo nhóm 4 HS giải quyết các bài tập trên bảng phụ.

#### c) Sản phẩm:
- Lời giải Bài 2.25, Bài 2.26 và Bài 2.27 trên bảng phụ và trong vở ghi.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao nhiệm vụ:<br>+ Nhóm 1: Bài 2.25 (Từ các chữ số 5; 0; 1; 3 viết số có 3 chữ số khác nhau chia hết cho 5, chia hết cho 3).<br>+ Nhóm 2: Bài 2.26 (Phân tích $A = 4^2 \cdot 6^3$, $B = 9^2 \cdot 15^2$ ra thừa số nguyên tố).<br>+ Nhóm 3: Bài 2.27 (Tìm số tự nhiên $x \le 22$ để $100 - x \ \vdots \ 4$ và $18 + 90 + x \ \vdots \ 9$).<br>- **HS:** Làm việc nhóm trong 6 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thảo luận, tìm các phương án số.<br>- **GV:** Lưu ý Bài 2.26: Không nên tính ra giá trị cụ thể mà nên tách từng cơ số: $4 = 2^2, 6 = 2 \cdot 3...$<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Đại diện 3 nhóm lên trình bày lời giải chi tiết.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Nhận xét, chuẩn hóa phương pháp giải tối ưu. | **GIẢI BÀI TẬP TRỌNG TÂM SGK TRANG 43:**<br><br>1. **Bài 2.25:** Các chữ số: $\{5; 0; 1; 3\}$ (3 chữ số khác nhau):<br>a) Chia hết cho 5 (tận cùng là 0 hoặc 5):<br>- Tận cùng là 0: $130, 150, 310, 350, 510, 530$.<br>- Tận cùng là 5: $105, 135, 305, 315$.<br>b) Chia hết cho 3 (tổng 3 chữ số chia hết cho 3):<br>- Chọn bộ 3 số có tổng chia hết cho 3: $\{5; 1; 0\}$ (tổng 6), $\{5; 1; 3\}$ (tổng 9).<br>- Các số lập được: $150, 510, 105, 501, 135, 153, 315, 351, 513, 531$.<br><br>2. **Bài 2.26:** Phân tích ra thừa số nguyên tố:<br>- $A = 4^2 \cdot 6^3 = (2^2)^2 \cdot (2 \cdot 3)^3 = 2^4 \cdot 2^3 \cdot 3^3 = 2^7 \cdot 3^3$.<br>- $B = 9^2 \cdot 15^2 = (3^2)^2 \cdot (3 \cdot 5)^2 = 3^4 \cdot 3^2 \cdot 5^2 = 3^6 \cdot 5^2$.<br><br>3. **Bài 2.27:** Với số tự nhiên $x \le 22$:<br>a) $100 - x \ \vdots \ 4$: Vì $100 \ \vdots \ 4$ nên $x \ \vdots \ 4$.<br>Do $x \le 22$ nên $x \in \{0; 4; 8; 12; 16; 20\}$.<br>b) $18 + 90 + x \ \vdots \ 9$: Vì $18 \ \vdots \ 9$ và $90 \ \vdots \ 9$ nên $x \ \vdots \ 9$.<br>Do $x \le 22$ nên $x \in \{0; 9; 18\}$. |

---

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)

#### a) Mục tiêu:
- Vận dụng kiến thức số nguyên tố vào tìm hiểu các cặp số nguyên tố sinh đôi (Bài 2.29).
- Định hướng nhiệm vụ tự học ở nhà.

#### b) Nội dung:
- Khám phá định nghĩa số nguyên tố sinh đôi và liệt kê tất cả các cặp nhỏ hơn 40.

#### c) Sản phẩm:
- Các cặp số nguyên tố sinh đôi nhỏ hơn 40: $(3, 5); (5, 7); (11, 13); (17, 19); (29, 31)$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu Bài 2.29 SGK: "Hai số nguyên tố được gọi là sinh đôi nếu chúng hơn kém nhau 2 đơn vị (ví dụ 17 và 19). Em hãy liệt kê hết các cặp số nguyên tố sinh đôi nhỏ hơn 40."<br>- **HS:** Đọc đề và tra cứu bảng số nguyên tố nhỏ hơn 40.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Liệt kê các số nguyên tố nhỏ hơn 40: $2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37$.<br>- Tìm các cặp hơn kém nhau 2 đơn vị.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trả lời các cặp: $(3, 5); (5, 7); (11, 13); (17, 19); (29, 31)$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Đánh giá tiết học, dặn dò học sinh chuẩn bị bài cho Bài 11: Ước chung và ước chung lớn nhất. | **BÀI 2.29 (VẬN DỤNG - SỐ NGUYÊN TỐ SINH ĐÔI):**<br><br>- Các số nguyên tố nhỏ hơn 40 là:<br>$$2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37$$<br>- Các cặp số nguyên tố sinh đôi (hơn kém nhau 2 đơn vị) là:<br>$$(3, 5); (5, 7); (11, 13); (17, 19); (29, 31)$$<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Hoàn thành Bài 2.28 SGK vào vở.<br>- Xem trước Bài 11: Ước chung. Ước chung lớn nhất (tìm hiểu cách tìm ước chung). |
"""

MD_07 = """# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
**TRƯỜNG THCS TRẦN PHÚ**  
**TỔ: TOÁN - TIN HỌC**  
**Họ và tên giáo viên:** .....................................................  
**KẾ HOẠCH BÀI DẠY MÔN TOÁN — LỚP 6**  
**CHỦ ĐỀ: BÀI 11. ƯỚC CHUNG. ƯỚC CHUNG LỚN NHẤT (2 TIẾT)**  
**Phân phối chương trình:** Tiết 21, 22 — Tuần 7, 8  
**Thời lượng thực hiện:** 02 tiết (90 phút)  
**Bộ sách:** Kết nối tri thức với cuộc sống (SGK trang 44 – 48)  

---

# I. MỤC TIÊU

## 1. Về kiến thức
- Nhận biết được khái niệm ước chung ($ƯC$) và ước chung lớn nhất ($ƯCLN$) của hai hoặc nhiều số tự nhiên; nắm vững ký hiệu $ƯC(a, b)$ và $ƯCLN(a, b)$.
- Nắm vững và thực hiện thành thạo quy tắc 3 bước tìm $ƯCLN$ bằng cách phân tích các số ra thừa số nguyên tố.
- Nhận biết được hai số nguyên tố cùng nhau; vận dụng $ƯCLN$ để rút gọn phân số về phân số tối giản.

## 2. Về năng lực

### a) Năng lực chung
- Tự chủ và tự học: Tự tìm ước của từng số để tìm ước chung, chủ động thực hiện các bước tìm ƯCLN.
- Giao tiếp và hợp tác: Làm việc nhóm phân chia đồ vật, chia phần thưởng đều nhau trong bài toán thực tế.

### b) Năng lực đặc thù môn Toán
- Tư duy và lập luận toán học: So sánh phương pháp liệt kê ước với phương pháp phân tích ra thừa số nguyên tố để thấy ưu điểm khi tìm ƯCLN của các số lớn.
- Mô hình hóa toán học: Vận dụng ƯCLN giải bài toán chia đều (chia tổ, chia quà, cắt thanh gỗ thành các đoạn bằng nhau dài nhất).

## 3. Về phẩm chất
- Chăm chỉ: Rèn tính cẩn thận, không chọn nhầm thừa số chung với thừa số riêng.
- Trách nhiệm: Ý thức hợp tác chia sẻ công việc trong hoạt động nhóm.

---

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU

1. **Giáo viên:** Kế hoạch bài dạy, bài giảng PowerPoint, phiếu học tập nhóm, các thẻ số minh họa tập hợp ước chung.
2. **Học sinh:** SGK Toán 6 (Tập 1), vở ghi bài, nháp, máy tính cầm tay để kiểm chứng kết quả.

---

# III. TIẾN TRÌNH DẠY HỌC

---

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (8 phút)

#### a) Mục tiêu:
- Xuất phát từ tình huống thực tế chia đều phần thưởng để tạo động cơ tìm hiểu khái niệm ước chung và ước chung lớn nhất.

#### b) Nội dung:
- Tình huống: Cô giáo có 18 chiếc bút và 24 quyển vở muốn chia đều vào các túi quà. Số túi quà có thể là bao nhiêu? Số túi quà nhiều nhất là bao nhiêu?

#### c) Sản phẩm:
- HS nhận xét: Số túi quà phải vừa là ước của 18 vừa là ước của 24; số túi quà nhiều nhất chính là số lớn nhất trong các ước chung đó.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Đặt vấn đề: "Cô có 18 chiếc bút bi và 24 quyển vở. Cô muốn chia đều số bút và vở vào các phần thưởng sao cho mỗi phần có số bút và số vở như nhau. Có thể chia được thành mấy phần thưởng? Số phần thưởng nhiều nhất có thể chia là bao nhiêu?"<br>- **HS:** Thảo luận cặp đôi trong 2 phút.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Liệt kê các ước của 18 và ước của 24; tìm các số chung.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** "Các số vừa chia hết cho 18 vừa chia hết cho 24 là: 1, 2, 3, 6. Do đó số túi quà nhiều nhất là 6 túi."<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa: 1, 2, 3, 6 là các ước chung của 18 và 24; 6 là ước chung lớn nhất. Ta cùng tìm hiểu bài hôm nay. | **TÌNH HUỐNG KHỞI ĐỘNG:**<br><br>- $Ư(18) = \{1; 2; 3; 6; 9; 18\}$.<br>- $Ư(24) = \{1; 2; 3; 4; 6; 8; 12; 24\}$.<br>- Các số chung: $\{1; 2; 3; 6\}$.<br>- Số lớn nhất trong các số chung là: $6$.<br><br>Khái niệm ước chung, ước chung lớn nhất và cách tìm ra sao? |

---

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (45 phút)

### 1. Hoạt động 2.1: Ước chung và Ước chung lớn nhất (20 phút)

#### a) Mục tiêu:
- Định nghĩa ước chung, ước chung lớn nhất; ký hiệu $ƯC(a, b)$ và $ƯCLN(a, b)$.
- Nhận biết nhận xét: Tất cả các ước chung của hai hay nhiều số đều là ước của ƯCLN của chúng.

#### b) Nội dung:
- Đọc định nghĩa SGK; thực hiện Hoạt động 1, 2 SGK trang 44.

#### c) Sản phẩm:
- Định nghĩa và ký hiệu vào vở; lời giải Luyện tập 1 SGK.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giới thiệu định nghĩa: Một số được gọi là ước chung của hai hay nhiều số nếu nó là ước của tất cả các số đó. Số lớn nhất trong tập hợp các ước chung của $a$ và $b$ gọi là ước chung lớn nhất của $a$ và $b$.<br>- **HS:** Ghi bài và ký hiệu.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tìm $ƯC(12, 16)$ và chỉ ra $ƯCLN(12, 16)$.<br>- **GV:** Hướng dẫn nhận xét mối liên hệ giữa các ước chung với ƯCLN.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** $ƯC(12, 16) = \{1; 2; 4\}$; $ƯCLN(12, 16) = 4$. Nhận thấy các ước chung 1, 2, 4 đều là ước của 4.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chốt nhận xét: $ƯC(a, b) = Ư(ƯCLN(a, b))$. | **1. ƯỚC CHUNG VÀ ƯỚC CHUNG LỚN NHẤT:**<br><br>- **Định nghĩa:**<br>+ Ước chung của hai hay nhiều số là ước của tất cả các số đó.<br>Ký hiệu: $ƯC(a, b)$, $ƯC(a, b, c)$.<br>+ Ước chung lớn nhất của hai hay nhiều số là số lớn nhất trong tập hợp các ước chung của các số đó.<br>Ký hiệu: $ƯCLN(a, b)$, $ƯCLN(a, b, c)$.<br><br>- **Nhận xét quan trọng:**<br>Tất cả các ước chung của hai hay nhiều số đều là ước của ƯCLN của chúng:<br>$$ƯC(a, b) = Ư(ƯCLN(a, b))$$ |

---

### 2. Hoạt động 2.2: Cách tìm ƯCLN bằng phân tích ra thừa số nguyên tố (15 phút)

#### a) Mục tiêu:
- Nắm vững quy tắc 3 bước tìm ƯCLN bằng cách phân tích ra thừa số nguyên tố.
- Nhận biết hai số nguyên tố cùng nhau.

#### b) Nội dung:
- Tìm hiểu quy tắc SGK trang 45; thực hành tìm $ƯCLN(36, 84)$.

#### c) Sản phẩm:
- Quy tắc 3 bước; kết quả $ƯCLN(36, 84) = 2^2 \cdot 3 = 12$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu quy tắc 3 bước tìm ƯCLN của hai hay nhiều số lớn hơn 1:<br>+ Bước 1: Phân tích mỗi số ra thừa số nguyên tố.<br>+ Bước 2: Chọn ra các thừa số nguyên tố **chung**.<br>+ Bước 3: Lập tích các thừa số đã chọn, mỗi thừa số lấy với số mũ **nhỏ nhất** của nó.<br>- **HS:** Đọc quy tắc và ghi nhớ từ khóa: "thừa số chung" và "số mũ nhỏ nhất".<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thực hiện tìm $ƯCLN(36, 84)$ theo đúng 3 bước.<br>- **GV:** Quan sát, chỉnh sửa cách chọn số mũ.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày: $36 = 2^2 \cdot 3^2$; $84 = 2^2 \cdot 3 \cdot 7$. Thừa số chung là 2 và 3. Số mũ nhỏ nhất: $2^2$ và $3^1$. Do đó $ƯCLN(36, 84) = 2^2 \cdot 3 = 12$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa và giới thiệu: Hai số có $ƯCLN = 1$ gọi là hai số nguyên tố cùng nhau (ví dụ 8 và 9). | **2. QUY TẮC TÌM ƯCLN (3 BƯỚC):**<br><br>- **Bước 1:** Phân tích mỗi số ra thừa số nguyên tố.<br>- **Bước 2:** Chọn ra các thừa số nguyên tố chung.<br>- **Bước 3:** Lập tích các thừa số đã chọn, mỗi thừa số lấy với số mũ nhỏ nhất của nó. Tích đó là ƯCLN phải tìm.<br><br>**Ví dụ:** Tìm $ƯCLN(36, 84)$:<br>- $36 = 2^2 \cdot 3^2$<br>- $84 = 2^2 \cdot 3 \cdot 7$<br>$\Rightarrow ƯCLN(36, 84) = 2^2 \cdot 3^1 = 12$.<br><br>- **Hai số nguyên tố cùng nhau:** Là hai số có ước chung lớn nhất bằng 1 (Ví dụ: $ƯCLN(8, 9) = 1$). |

---

### 3. Hoạt động 2.3: Ứng dụng rút gọn phân số (10 phút)

#### a) Mục tiêu:
- Nhận biết phân số tối giản và cách rút gọn phân số về tối giản bằng cách chia cả tử và mẫu cho ƯCLN.

#### b) Nội dung:
- Rút gọn phân số $\frac{24}{108}$.

#### c) Sản phẩm:
- $ƯCLN(24, 108) = 12 \Rightarrow \frac{24}{108} = \frac{24 : 12}{108 : 12} = \frac{2}{9}$.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** "Để rút gọn một phân số về phân số tối giản nhanh nhất chỉ trong một lần chia, ta làm thế nào?"<br>- **HS:** Suy nghĩ và trả lời.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Chia cả tử và mẫu cho $ƯCLN$ của tử và mẫu.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Thực hiện rút gọn $\frac{24}{108}$ bằng cách chia cho 12 được $\frac{2}{9}$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khẳng định đây là phương pháp rút gọn phân số tối ưu nhất. | **3. RÚT GỌN VỀ PHÂN SỐ TỐI GIẢN:**<br><br>- **Phân số tối giản:** Là phân số mà tử và mẫu là hai số nguyên tố cùng nhau ($ƯCLN(\text{tử}, \text{mẫu}) = 1$).<br>- **Quy tắc rút gọn:** Muốn rút gọn phân số về tối giản, ta chia cả tử và mẫu cho $ƯCLN$ của chúng. |

---

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (25 phút)

#### a) Mục tiêu:
- Thành thạo kỹ năng tìm ƯCLN của hai hay ba số tự nhiên và ứng dụng rút gọn phân số.

#### b) Nội dung:
- Giải Bài 2.30, 2.31, 2.32 SGK trang 47.

#### c) Sản phẩm:
- Lời giải bài tập trong vở học sinh.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao bài tập: Bài 2.30 (tìm ƯCLN của các cặp số), Bài 2.32 (rút gọn phân số).<br>- **HS:** Làm việc cá nhân và đổi chéo vở kiểm tra.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Phân tích ra thừa số nguyên tố, lập tích lũy thừa.<br>- **GV:** Hỗ trợ học sinh tính toán thừa số.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Gọi 3 HS lên bảng làm bài.<br>- **HS:** Nhận xét bài của bạn trên bảng.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa kết quả và lưu ý không nhầm lẫn giữa thừa số chung và riêng. | **GIẢI BÀI TẬP SGK TRANG 47:**<br><br>1. **Bài 2.30:** Tìm $ƯCLN$:<br>a) $ƯCLN(40, 70)$:<br>$40 = 2^3 \cdot 5$; $70 = 2 \cdot 5 \cdot 7 \Rightarrow ƯCLN(40, 70) = 2 \cdot 5 = 10$.<br>b) $ƯCLN(55, 110)$:<br>Vì $110 \ \vdots \ 55$ nên $ƯCLN(55, 110) = 55$.<br><br>2. **Bài 2.32:** Rút gọn về phân số tối giản:<br>a) $\frac{24}{108}$: $ƯCLN(24, 108) = 12 \Rightarrow \frac{24 : 12}{108 : 12} = \frac{2}{9}$.<br>b) $\frac{80}{140}$: $ƯCLN(80, 140) = 20 \Rightarrow \frac{80 : 20}{140 : 20} = \frac{4}{7}$. |

---

## D. HOẠT ĐỘNG 4: VẬN DỤNG (12 phút)

#### a) Mục tiêu:
- Vận dụng ƯCLN giải bài toán chia tổ thực tế trong học đường (Bài 2.34 SGK).

#### b) Nội dung:
- Giải Bài 2.34 SGK: Một đội tình nguyện gồm 36 bạn nam và 48 bạn nữ. Có thể chia đội thành nhiều nhất bao nhiêu tổ sao cho số nam và nữ trong mỗi tổ đều bằng nhau?

#### c) Sản phẩm:
- Số tổ nhiều nhất là $ƯCLN(36, 48) = 12$ tổ; mỗi tổ có 3 nam và 4 nữ.

#### d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung |
| :--- | :--- |
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Nêu Bài 2.34 SGK và gợi ý: "Số tổ nhiều nhất có thể chia có mối quan hệ gì với 36 và 48?"<br>- **HS:** Đọc đề và thảo luận cặp đôi.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Lập luận: Số tổ là ước chung của 36 và 48, mà số tổ là nhiều nhất nên số tổ là $ƯCLN(36, 48)$.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày: $36 = 2^2 \cdot 3^2; 48 = 2^4 \cdot 3 \Rightarrow ƯCLN(36, 48) = 2^2 \cdot 3 = 12$ tổ.<br>Mỗi tổ có: $36 : 12 = 3$ bạn nam và $48 : 12 = 4$ bạn nữ.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Khen ngợi học sinh và giao bài tự học ở nhà. | **BÀI 2.34 (VẬN DỤNG THỰC TẾ):**<br><br>Gọi số tổ chia được nhiều nhất là $x$ ($x \in \mathbb{N}^*$).<br>Theo đề bài ta có $36 \ \vdots \ x$ và $48 \ \vdots \ x$, đồng thời $x$ lớn nhất.<br>Do đó $x = ƯCLN(36, 48)$.<br>Ta có:<br>- $36 = 2^2 \cdot 3^2$<br>- $48 = 2^4 \cdot 3$<br>$\Rightarrow x = ƯCLN(36, 48) = 2^2 \cdot 3 = 12$.<br>Vậy có thể chia được nhiều nhất **12 tổ**.<br>Khi đó mỗi tổ có: $36 : 12 = 3$ bạn nam và $48 : 12 = 4$ bạn nữ.<br><br>**HƯỚNG DẪN TỰ HỌC TẠI NHÀ:**<br>- Học thuộc quy tắc 3 bước tìm ƯCLN.<br>- Hoàn thành Bài 2.33, 2.35 SGK trang 48.<br>- Đọc trước Bài 12: Bội chung. Bội chung nhỏ nhất. |
"""

MD_08 = """# KẾ HOẠCH BÀI DẠY (GIÁO ÁN) CHUẨN CÔNG VĂN 5512 — HỆ THỐNG SOANKHBD
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
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Trình chiếu quy tắc 3 bước tìm BCNN:<br>+ Bước 1: Phân tích mỗi số ra thừa số nguyên tố.<br>+ Bước 2: Chọn ra các thừa số nguyên tố **chung và riêng**.<br>+ Bước 3: Lập tích các thừa số đã chọn, mỗi thừa số lấy với số mũ **lớn nhất** của nó.<br>- ***[NLS: 5.3.TC1a] GV hướng dẫn học sinh thao tác trên bảng tính Excel: "Gõ lệnh =LCM(12, 18, 30) hoặc dùng phím BCNN trên máy tính Casio để kiểm tra nhanh kết quả tính tay."***<br>- ***[AI: 6.C1.1] GV mô tả cách hệ thống AI xử lý: "Khi nhận đầu vào là các số tự nhiên, AI sử dụng thuật toán phân tích thừa số nguyên tố và giải thuật Euclid mở rộng để tìm BCNN chỉ trong vài mili-giây, sau đó xuất ra từng bước giải thích logic cho người dùng."***<br>- **HS:** Ghi bài và đối chiếu giữa ƯCLN (chung, số mũ nhỏ nhất) với BCNN (chung và riêng, số mũ lớn nhất).<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Thực hiện tìm $BCNN(12, 18, 30)$ ra nháp.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **HS:** Trình bày: $12 = 2^2 \cdot 3$; $18 = 2 \cdot 3^2$; $30 = 2 \cdot 3 \cdot 5$. Thừa số chung và riêng: 2, 3, 5. Lấy số mũ lớn nhất: $2^2, 3^2, 5^1$. Kết quả $BCNN = 2^2 \cdot 3^2 \cdot 5 = 4 \cdot 9 \cdot 5 = 180$.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa kiến thức, khen ngợi học sinh. | **2. QUY TẮC TÌM BCNN (3 BƯỚC):**<br><br>- **Bước 1:** Phân tích mỗi số ra thừa số nguyên tố.<br>- **Bước 2:** Chọn ra các thừa số nguyên tố **chung và riêng**.<br>- **Bước 3:** Lập tích các thừa số đã chọn, mỗi thừa số lấy với số mũ **lớn nhất** của nó. Tích đó là BCNN phải tìm.<br><br>**Ví dụ:** Tìm $BCNN(12, 18, 30)$:<br>- $12 = 2^2 \cdot 3$<br>- $18 = 2 \cdot 3^2$<br>- $30 = 2 \cdot 3 \cdot 5$<br>$\Rightarrow BCNN(12, 18, 30) = 2^2 \cdot 3^2 \cdot 5 = 180$.<br><br>***[Tích hợp NLS 5.3.TC1a]: Sử dụng lệnh =LCM() trong Excel hoặc máy tính cầm tay kiểm tra kết quả BCNN nhanh chóng.***<br>***[Tích hợp AI 6.C1.1]: Mô tả quy trình thuật toán AI phân tích dữ liệu số học để tìm BCNN tự động.*** |

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
| + Bước 1: Chuyển giao nhiệm vụ:<br>- **GV:** Giao nhiệm vụ Bài 2.36 (tìm BCNN), Bài 2.38 (quy đồng mẫu phân số).<br>- **HS:** Làm vào vở, 2 HS lên bảng.<br>+ Bước 2: Thực hiện nhiệm vụ:<br>- **HS:** Tự giác làm bài.<br>- **GV:** Đi quan sát, nhắc nhở chọn đúng số mũ lớn nhất.<br>+ Bước 3: Báo cáo, thảo luận:<br>- **GV:** Yêu cầu HS nhận xét bài làm trên bảng.<br>+ Bước 4: Kết luận, nhận định:<br>- **GV:** Chuẩn hóa lời giải và củng cố phương pháp. | **GIẢI BÀI TẬP SGK TRANG 53:**<br><br>1. **Bài 2.36:** Tìm $BCNN$:<br>a) $BCNN(6, 8)$: $6 = 2 \cdot 3; 8 = 2^3 \Rightarrow BCNN(6, 8) = 2^3 \cdot 3 = 24$.<br>b) $BCNN(10, 1, 12)$:<br>Vì $BCNN(a, 1) = a$ nên $BCNN(10, 1, 12) = BCNN(10, 12) = 60$.<br><br>2. **Bài 2.38:** Quy đồng mẫu số:<br>a) $\frac{3}{8}$ và $\frac{5}{24}$:<br>Vì $24 \ \vdots \ 8$ nên mẫu chung là $24$.<br>$\frac{3}{8} = \frac{3 \cdot 3}{8 \cdot 3} = \frac{9}{24}$; giữ nguyên $\frac{5}{24}$. |

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
"""

all_lessons = [
    ("KHBD_05_Toan6_Bai10_SoNguyenTo_Tiet18-19.md", MD_05),
    ("KHBD_06_Toan6_LuyenTapChung_Tiet20.md", MD_06),
    ("KHBD_07_Toan6_Bai11_UocChung_UocChungLonNhat_Tiet21-22.md", MD_07),
    ("KHBD_08_Toan6_Bai12_BoiChung_BoiChungNhoNhat_Tiet23-24.md", MD_08)
]

for filename, content in all_lessons:
    fpath = os.path.join(OUT_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {filename} ({len(content)} chars)")

print("Hoàn thành tạo 4 bài tiếp theo (Bài 5 đến 8)!")
