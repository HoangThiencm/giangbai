# -*- coding: utf-8 -*-
import os

md_content = """**TIẾT 15, 16 - BÀI 15: ĐỘ DÀI CỦA CUNG TRÒN. DIỆN TÍCH HÌNH QUẠT TRÒN VÀ HÌNH VÀNH KHUYÊN (BÀI HỌC STEM: VÒNG QUAY HÀNH ĐỘNG XANH)**
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhớ lại và khắc sâu các công thức cốt lõi của hình tròn: Chu vi đường tròn $C = 2\\pi R = \\pi d$ và diện tích hình tròn $S = \\pi R^2$.
- Thiết lập và vận dụng thành thạo công thức tính độ dài cung tròn $n^\\circ$: $l = \\frac{\\pi R n}{180}$.
- Hiểu rõ khái niệm hình quạt tròn và hình vành khuyên; thiết lập và vận dụng chính xác công thức tính diện tích hình quạt tròn bán kính $R$, cung $n^\\circ$:
  $$S_q = \\frac{\\pi R^2 n}{360} = \\frac{l R}{2}$$
  và diện tích hình vành khuyên giới hạn bởi hai đường tròn đồng tâm bán kính $R_1 > R_2$:
  $$S_{vk} = \\pi (R_1^2 - R_2^2)$$
- Áp dụng các công thức trên vào thực tiễn thông qua **Bài học STEM: "Thiết kế Vòng quay hành động xanh (tuyên truyền phân loại rác, tiết kiệm điện, tiết kiệm nước, bảo vệ môi trường)"**.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tìm hiểu vật liệu tái chế (bìa carton, compa, thước kẻ, đinh bấm, giấy màu) và tự phác thảo bản vẽ kỹ thuật phân chia hình quạt tròn, dải viền vành khuyên.
- Giao tiếp và hợp tác: Làm việc nhóm phân công rõ ràng các vai trò kỹ thuật, mỹ thuật và thuyết trình; biết lắng nghe, phản biện và tiếp thu góp ý để hoàn thiện sản phẩm STEM.

b) Năng lực đặc thù môn Toán & Năng lực STEM:
- Năng lực mô hình hóa toán học: Chuyển đổi ý tưởng vòng quay tuyên truyền thành bài toán phân chia hình tròn theo tỉ lệ phần trăm ($40\\% - 25\\% - 20\\% - 15\\%$), tính toán chính xác số đo góc ở tâm $n^\\circ$, độ dài cung viền $l$, diện tích từng hình quạt $S_q$ và diện tích dải viền vành khuyên $S_{vk}$.
- Năng lực thiết kế kỹ thuật (Engineering): Lập bản vẽ kỹ thuật tỉ lệ chuẩn với bán kính $R = 15\\text{ cm}$, dải viền ngoài từ $13.5\\text{ cm}$ đến $15\\text{ cm}$; chế tạo cơ cấu mũi tên quay quanh trục tâm nhẹ nhàng, cân bằng động, không bị kẹt rít.
- Năng lực công nghệ (Technology): Khai thác vật liệu thân thiện môi trường, thao tác đo đạc, cắt dán an toàn và chính xác.

c) Năng lực số (NLS):
- ***5.2.TC2b: HS sử dụng máy tính cầm tay để tính toán với số $\\pi$ (phím SHIFT $\\times 10^x$), làm tròn số thập phân theo yêu cầu thực tế; hoặc sử dụng phần mềm GeoGebra/Canva để thiết kế trực quan kích thước các hình quạt tròn và dải viền trước khi gia công.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***9.D1.1: HS phối hợp sử dụng AI Chatbot để tra cứu các ý tưởng trang trí hoa văn biểu tượng hành động xanh (biểu tượng tái chế, bóng đèn tiết kiệm điện, giọt nước, mầm cây) và tối ưu hóa diện tích cắt ghép giấy màu trên khổ A4 nhằm giảm thiểu giấy thừa phế liệu.***

## 3. Về phẩm chất
- Say mê sáng tạo, yêu thích ứng dụng toán học vào đời sống; hình thành lối sống xanh, ý thức giữ gìn vệ sinh môi trường học đường.
- Cẩn thận, trung thực, chính xác trong đo đạc kỹ thuật; tinh thần trách nhiệm trong thực hiện nhiệm vụ và nộp sản phẩm đúng hạn.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên:
- Kế hoạch bài dạy STEM, bài giảng trình chiếu đa phương tiện (PowerPoint/Canva).
- Mô hình mẫu "Vòng quay hành động xanh" hoàn chỉnh làm trực quan.
- Dụng cụ bảng: Compa giáo viên, thước thẳng chia mm, thước đo góc $180^\\circ$.
- Phiếu học tập số 1 (Nghiên cứu kiến thức nền), Phiếu học tập số 2 (Bản thiết kế kỹ thuật & Bảng số liệu toán học), Phiếu đánh giá Rubric chấm điểm sản phẩm STEM.

2. Học sinh:
- Mỗi nhóm học tập (4 – 6 HS) chuẩn bị:
  + 01 tấm bìa cứng carton dày (kích thước tối thiểu $35 \\times 35\\text{ cm}$) làm mặt vòng quay và đế đỡ.
  + Giấy thủ công màu sắc: xanh lá cây (rác tái chế), vàng (tiết kiệm điện), xanh dương (tiết kiệm nước), cam (rác hữu cơ / mầm cây), trắng (nền viền hoa văn).
  + Bộ dụng cụ vẽ: Compa, thước kẻ thẳng, thước đo góc $180^\\circ$, bút chì, bút dạ màu.
  + Dụng cụ gia công: Kéo thủ công, keo dán (hồ dán/keo hai mặt), 01 chốt đinh bấm (hoặc chốt cánh bướm/đinh tán nhỏ) làm trục quay của mũi tên.
  + Máy tính cầm tay Casio/Vinacal.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ XÁC ĐỊNH VẤN ĐỀ STEM (HOẠT ĐỘNG 1) (10 phút)
a) Mục tiêu: Kích hoạt sự hứng thú học tập qua tình huống tổ chức trò chơi tuyên truyền lối sống xanh trong trường học; nhận biết cấu trúc hình học của vòng quay may mắn gồm các hình quạt tròn và dải viền vành khuyên; xác định nhiệm vụ thiết kế sản phẩm STEM.
b) Nội dung: Quan sát vòng quay tuyên truyền "Hành động xanh", thảo luận câu hỏi: Làm thế nào để chia đều hoặc chia theo tỉ lệ phần trăm các ô hành động xanh trên một mặt đĩa tròn? Cần bao nhiêu diện tích giấy màu cho từng ô và viền ngoài?
c) Sản phẩm: Câu hỏi nghiên cứu STEM và bản đăng ký nhiệm vụ của các nhóm: "Thiết kế Vòng quay hành động xanh với bán kính $R = 15\\text{ cm}$ gồm 4 hình quạt tròn và viền trang trí hình vành khuyên".
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt vấn đề: Đoàn trường phát động chiến dịch "Trường học không rác thải nhựa và tiết kiệm năng lượng". Để gian hàng hội chợ thanh niên thêm phần sôi nổi, mỗi lớp cần thiết kế một **"Vòng quay hành động xanh"**.<br>- **GV:** Cho HS quan sát hình ảnh chiếc vòng quay với kim chỉ nam xoay được. Hỏi:<br>  1. Mặt vòng quay có dạng hình gì?<br>  2. Các ô màu (tái chế, tiết kiệm điện, tiết kiệm nước, rác hữu cơ) có dạng hình học gì?<br>  3. Dải viền trang trí hoa văn bao quanh mép ngoài có dạng hình gì?<br>  4. Để cắt giấy màu vừa khít từng ô và viền ngoài, ta cần tính những đại lượng toán học nào?<br>- **HS:** Quan sát, lắng nghe và tiếp nhận câu hỏi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo nhóm bàn.<br>- Nhận diện: Các ô màu là các hình quạt tròn có chung đỉnh tại tâm, dải viền ngoài là hình vành khuyên giới hạn bởi hai đường tròn đồng tâm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS trả lời: Cần tính số đo góc ở tâm để dùng thước đo độ vẽ, cần tính độ dài cung tròn để cắt dải viền, cần tính diện tích hình quạt tròn và diện tích hình vành khuyên để chuẩn bị lượng giấy màu vừa đủ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chính xác! Để làm được chiếc vòng quay chuẩn xác và thẩm mỹ, hôm nay chúng ta sẽ cùng nghiên cứu kiến thức nền: **Độ dài cung tròn, diện tích hình quạt tròn và hình vành khuyên**, sau đó trực tiếp chế tạo sản phẩm STEM. | **Vấn đề STEM:**<br>- Sản phẩm cần chế tạo: "Vòng quay hành động xanh" có bán kính $R = 15\\text{ cm}$, quay được quanh trục tâm.<br>- Cấu trúc hình học cần giải quyết:<br>  1. Phân chia mặt tròn thành các **hình quạt tròn** tương ứng với các tỉ lệ phần trăm nhiệm vụ.<br>  2. Tính số đo góc ở tâm $n^\\circ$ và độ dài cung viền $l$.<br>  3. Tính diện tích hình quạt $S_q$ để cắt dán giấy màu.<br>  4. Tính diện tích dải viền **hình vành khuyên** $S_{vk}$ bao quanh mép ngoài. |

## B. NGHIÊN CỨU KIẾN THỨC NỀN (HOẠT ĐỘNG 2) (35 phút)
### Hoạt động 2.1: Công thức tính độ dài cung tròn (15 phút)
a) Mục tiêu: HS thiết lập được công thức tính độ dài cung tròn $n^\\circ$ từ chu vi đường tròn; tính toán thành thạo độ dài cung; tích hợp chỉ báo NLS 5.2.TC2b.
b) Nội dung: Làm việc với SGK trang 88 – 90, suy luận quy tắc tỉ lệ thuận từ chu vi đường tròn ($360^\\circ$) sang cung $1^\\circ$ và cung $n^\\circ$; làm Luyện tập 1.
c) Sản phẩm: Công thức $l = \\frac{\\pi R n}{180}$ và bài giải Luyện tập 1 trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nhắc lại: Đường tròn bán kính $R$ có chu vi $C = 2\\pi R$, tương ứng với góc ở tâm cả đường tròn là $360^\\circ$.<br>- **GV:** Hỏi: Cung tròn $1^\\circ$ có độ dài là bao nhiêu? Vậy cung tròn $n^\\circ$ có độ dài $l$ bằng bao nhiêu?<br>- **HS:** Ghi chép câu hỏi và suy luận quy tắc tam suất.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy luận:<br>  + Độ dài cung $1^\\circ$ là: $\\frac{2\\pi R}{360} = \\frac{\\pi R}{180}$.<br>  + Độ dài cung $n^\\circ$ là: $l = \\frac{\\pi R n}{180}$.<br>- **GV:** Yêu cầu HS làm Luyện tập 1 SGK: Tính độ dài cung $60^\\circ$ của đường tròn có bán kính $R = 6\\text{ cm}$.<br>- ***Tích hợp NLS (5.2.TC2b):*** HS sử dụng máy tính cầm tay bấm phím $\\pi$, tính kết quả chính xác theo $\\pi$ và làm tròn đến hai chữ số thập phân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng làm Luyện tập 1:<br>  $$l = \\frac{\\pi \\cdot 6 \\cdot 60}{180} = 2\\pi \\approx 6.28\\text{ cm}$$<br>- HS dưới lớp nhận xét, đối chiếu bài làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa công thức độ dài cung tròn. Lưu ý HS: Muốn tính độ dài cung $l$, cần biết bán kính $R$ và số đo độ của cung $n^\\circ$. | **1. Độ dài cung tròn:**<br>- Chu vi đường tròn bán kính $R$ là: $C = 2\\pi R = \\pi d$.<br>- Trên đường tròn bán kính $R$, độ dài $l$ của một cung $n^\\circ$ được tính theo công thức:<br>  $$l = \\frac{\\pi R n}{180}$$<br>  *(Trong đó: $R$ là bán kính đường tròn, $n$ là số đo độ của cung tròn, $l$ là độ dài cung).*<br><br>**Luyện tập 1 (SGK trang 90):**<br>- Với $R = 6\\text{ cm}$, $n = 60^\\circ$:<br>  $$l = \\frac{\\pi \\cdot 6 \\cdot 60}{180} = 2\\pi \\approx 6.28\\text{ cm}$$ |

### Hoạt động 2.2: Diện tích hình quạt tròn và diện tích hình vành khuyên (20 phút)
a) Mục tiêu: HS nắm vững định nghĩa hình quạt tròn và hình vành khuyên; thiết lập công thức tính diện tích hình quạt tròn $S_q = \\frac{\\pi R^2 n}{360} = \\frac{l R}{2}$ và diện tích hình vành khuyên $S_{vk} = \\pi (R_1^2 - R_2^2)$; tích hợp chỉ báo AI 9.D1.1.
b) Nội dung: Làm việc với SGK trang 90 – 92; thực hiện HĐ2, HĐ3; áp dụng giải Luyện tập 2 và Luyện tập 3.
c) Sản phẩm: Vở ghi bài với hệ thống định nghĩa và công thức tính $S_q, S_{vk}$; bài giải chi tiết Luyện tập 2 và Luyện tập 3.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu định nghĩa: Hình quạt tròn là phần hình tròn giới hạn bởi một cung tròn và hai bán kính đi qua hai mút của cung đó.<br>- **GV:** Hình tròn diện tích $S = \\pi R^2$ ứng với cung $360^\\circ$. Hỏi: Diện tích hình quạt tròn $1^\\circ$ là bao nhiêu? Diện tích hình quạt tròn cung $n^\\circ$ là bao nhiêu?<br>- **GV:** Nêu mối liên hệ giữa $S_q$ và độ dài cung $l$.<br>- **GV:** Giới thiệu hình vành khuyên: Là phần mặt phẳng nằm giữa hai đường tròn đồng tâm $(O; R_1)$ và $(O; R_2)$ với $R_1 > R_2$. Nêu công thức tính diện tích $S_{vk}$.<br>- ***Tích hợp AI (9.D1.1):*** GV trình chiếu mô phỏng hình học trực quan do trợ lý AI tạo ra, minh họa cách tính diện tích hình vành khuyên bằng hiệu diện tích hai hình tròn đồng tâm.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thiết lập công thức:<br>  + Diện tích hình quạt tròn cung $1^\\circ$: $\\frac{\\pi R^2}{360}$.<br>  + Diện tích hình quạt tròn cung $n^\\circ$: $S_q = \\frac{\\pi R^2 n}{360}$.<br>  + Nhận xét: $S_q = \\frac{\\pi R n}{180} \\cdot \\frac{R}{2} = \\frac{l R}{2}$.<br>  + Diện tích hình vành khuyên: $S_{vk} = \\pi R_1^2 - \\pi R_2^2 = \\pi (R_1^2 - R_2^2)$.<br>- **HS:** Làm Luyện tập 2 và Luyện tập 3 SGK.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Hai HS lên bảng làm bài:<br>  + Luyện tập 2: Tính $S_q$ với $R = 10\\text{ cm}, n = 72^\\circ$.<br>  + Luyện tập 3: Tính $S_{vk}$ với $R_1 = 5\\text{ cm}, R_2 = 3\\text{ cm}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt kiến thức: Công thức $S_q = \\frac{l R}{2}$ rất dễ nhớ vì có dạng tương tự diện tích tam giác $\\frac{1}{2} \\cdot \\text{đáy} \\cdot \\text{chiều cao}$, trong đó độ dài cung $l$ đóng vai trò như đáy cong và bán kính $R$ là chiều cao. | **2. Diện tích hình quạt tròn và hình vành khuyên:**<br>- **Hình quạt tròn:** Diện tích hình quạt tròn bán kính $R$, cung $n^\\circ$ là:<br>  $$S_q = \\frac{\\pi R^2 n}{360} \\quad \\text{hay} \\quad S_q = \\frac{l R}{2}$$<br>- **Hình vành khuyên:** Giới hạn bởi hai đường tròn đồng tâm $(O; R_1)$ và $(O; R_2)$ ($R_1 > R_2$):<br>  $$S_{vk} = \\pi (R_1^2 - R_2^2)$$<br><br>**Luyện tập 2 (SGK trang 91):**<br>- Với $R = 10\\text{ cm}, n = 72^\\circ$:<br>  $$S_q = \\frac{\\pi \\cdot 10^2 \\cdot 72}{360} = 20\\pi \\approx 62.83\\text{ cm}^2$$<br><br>**Luyện tập 3 (SGK trang 92):**<br>- Với $R_1 = 5\\text{ cm}, R_2 = 3\\text{ cm}$:<br>  $$S_{vk} = \\pi (5^2 - 3^2) = \\pi (25 - 9) = 16\\pi \\approx 50.27\\text{ cm}^2$$ |

## C. ĐỀ XUẤT GIẢI PHÁP VÀ THIẾT KẾ KỸ THUẬT STEM (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: HS vận dụng kiến thức độ dài cung, diện tích hình quạt tròn và hình vành khuyên để tính toán các thông số kỹ thuật của "Vòng quay hành động xanh" bán kính $R = 15\\text{ cm}$; lập bảng số liệu chi tiết và phác thảo bản vẽ kỹ thuật.
b) Nội dung: Làm việc nhóm trên Phiếu học tập số 2:
- Tính số đo góc ở tâm $n_i$, độ dài cung $l_i$, diện tích $S_{qi}$ cho 4 hình quạt tròn theo tỉ lệ: $40\\% - 25\\% - 20\\% - 15\\%$.
- Tính diện tích dải viền trang trí hình vành khuyên với $R_1 = 15\\text{ cm}, R_2 = 13.5\\text{ cm}$.
- Thiết kế cơ cấu trục quay cho kim chỉ nam.
c) Sản phẩm: Phiếu học tập số 2 hoàn thiện của các nhóm có đầy đủ các thông số toán học và bản vẽ phác thảo cơ cấu quay.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ kỹ thuật cho các nhóm:<br>  1. Vòng quay có bán kính $R = 15\\text{ cm}$.<br>  2. Mặt vòng quay chia thành 4 hình quạt tròn tương ứng 4 chủ đề tuyên truyền:<br>     + **Ô 1 (Màu xanh lá):** Rác tái chế — Tỉ lệ $40\\%$.<br>     + **Ô 2 (Màu vàng):** Tiết kiệm điện — Tỉ lệ $25\\%$.<br>     + **Ô 3 (Màu xanh dương):** Tiết kiệm nước — Tỉ lệ $20\\%$.<br>     + **Ô 4 (Màu cam):** Rác hữu cơ / Trồng cây xanh — Tỉ lệ $15\\%$.<br>  3. Tính: Góc ở tâm $n_i$, độ dài cung viền $l_i$, diện tích $S_{qi}$ cho từng ô.<br>  4. Dải viền ngoài trang trí hoa văn dạng hình vành khuyên có bán kính ngoài $R_1 = 15\\text{ cm}$, bán kính trong $R_2 = 13.5\\text{ cm}$. Tính diện tích dải viền $S_{vk}$ và chu vi viền ngoài $C_1$.<br>  5. Phác thảo cơ cấu mũi tên quay quanh trục tâm bằng đinh bấm.<br>- **HS:** Tiếp nhận Phiếu học tập số 2, nhóm trưởng phân công nhiệm vụ tính toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhóm làm việc với máy tính cầm tay:<br>  + $n_1 = 360^\\circ \\cdot 40\\% = 144^\\circ$; $l_1 = \\frac{\\pi \\cdot 15 \\cdot 144}{180} = 12\\pi \\approx 37.70\\text{ cm}$; $S_{q1} = \\frac{\\pi \\cdot 15^2 \\cdot 144}{360} = 90\\pi \\approx 282.74\\text{ cm}^2$.<br>  + $n_2 = 360^\\circ \\cdot 25\\% = 90^\\circ$; $l_2 = \\frac{\\pi \\cdot 15 \\cdot 90}{180} = 7.5\\pi \\approx 23.56\\text{ cm}$; $S_{q2} = \\frac{\\pi \\cdot 15^2 \\cdot 90}{360} = 56.25\\pi \\approx 176.71\\text{ cm}^2$.<br>  + $n_3 = 360^\\circ \\cdot 20\\% = 72^\\circ$; $l_3 = \\frac{\\pi \\cdot 15 \\cdot 72}{180} = 6\\pi \\approx 18.85\\text{ cm}$; $S_{q3} = \\frac{\\pi \\cdot 15^2 \\cdot 72}{360} = 45\\pi \\approx 141.37\\text{ cm}^2$.<br>  + $n_4 = 360^\\circ \\cdot 15\\% = 54^\\circ$; $l_4 = \\frac{\\pi \\cdot 15 \\cdot 54}{180} = 4.5\\pi \\approx 14.14\\text{ cm}$; $S_{q4} = \\frac{\\pi \\cdot 15^2 \\cdot 54}{360} = 33.75\\pi \\approx 106.03\\text{ cm}^2$.<br>  + $S_{vk} = \\pi (15^2 - 13.5^2) = \\pi (225 - 182.25) = 42.75\\pi \\approx 134.30\\text{ cm}^2$.<br>  + $C_1 = 2\\pi \\cdot 15 = 30\\pi \\approx 94.25\\text{ cm}$.<br>- **GV:** Quan sát, hỗ trợ các nhóm kiểm tra tính hợp lý của số liệu tổng:<br>  $\\sum n_i = 360^\\circ$; $\\sum l_i = 30\\pi\\text{ cm}$; $\\sum S_{qi} = 225\\pi\\text{ cm}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện Nhóm 1 và Nhóm 3 báo cáo bảng số liệu.<br>- Các nhóm đối chiếu chéo số liệu tính toán.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Phê duyệt bản thiết kế và bảng số liệu của các nhóm. Cho phép các nhóm chuyển sang bước chế tạo thực tế. | **Bản thiết kế kỹ thuật Vòng quay hành động xanh:**<br><br>| Chủ đề & Màu sắc | Tỉ lệ (%) | Góc ở tâm ($n^\\circ$) | Độ dài cung ($l$ cm) | Diện tích quạt ($S_q\\text{ cm}^2$) |<br>| :--- | :---: | :---: | :---: | :---: |<br>| **Rác tái chế** (Xanh lá) | $40\\%$ | $144^\\circ$ | $12\\pi \\approx 37.70$ | $90\\pi \\approx 282.74$ |<br>| **Tiết kiệm điện** (Vàng) | $25\\%$ | $90^\\circ$ | $7.5\\pi \\approx 23.56$ | $56.25\\pi \\approx 176.71$ |<br>| **Tiết kiệm nước** (Xanh dương) | $20\\%$ | $72^\\circ$ | $6\\pi \\approx 18.85$ | $45\\pi \\approx 141.37$ |<br>| **Rác hữu cơ** (Cam) | $15\\%$ | $54^\\circ$ | $4.5\\pi \\approx 14.14$ | $33.75\\pi \\approx 106.03$ |<br>| **TỔNG CỘNG** | **$100\\%$** | **$360^\\circ$** | **$30\\pi \\approx 94.25$** | **$225\\pi \\approx 706.86$** |<br><br>- **Dải viền hoa văn (Hình vành khuyên):**<br>  + $R_1 = 15\\text{ cm}, R_2 = 13.5\\text{ cm}$.<br>  + Diện tích: $S_{vk} = \\pi (15^2 - 13.5^2) = 42.75\\pi \\approx 134.30\\text{ cm}^2$.<br>  + Chu vi mép ngoài: $C_1 = 30\\pi \\approx 94.25\\text{ cm}$. |

## D. CHẾ TẠO SẢN PHẨM, THỬ NGHIỆM VÀ HOÀN THIỆN STEM (HOẠT ĐỘNG 4) (20 phút)
a) Mục tiêu: HS trực tiếp đo đạc, dùng compa vẽ hình tròn $R = 15\\text{ cm}$, dùng thước đo độ chia góc ở tâm, cắt dán giấy màu theo đúng diện tích đã tính toán; vẽ viền vành khuyên hoa văn; lắp mũi tên quay và thử nghiệm độ nhạy của vòng quay.
b) Nội dung: Các nhóm học sinh thao tác chế tạo theo 4 bước công nghệ:
- Bước 1: Cắt đĩa tròn carton bán kính $R = 15\\text{ cm}$.
- Bước 2: Dùng compa và thước đo độ chia 4 góc: $144^\\circ, 90^\\circ, 72^\\circ, 54^\\circ$. Cắt dán 4 miếng giấy màu tương ứng vào từng hình quạt. Vẽ biểu tượng tuyên truyền (tái chế, bóng đèn, giọt nước, mầm cây).
- Bước 3: Dán dải viền trang trí hình vành khuyên bề rộng $1.5\\text{ cm}$, vẽ hoa văn lá cây và bông hoa.
- Bước 4: Chế tạo kim mũi tên bằng bìa cứng màu đen dài $10\\text{ cm}$, dùi lỗ tại trọng tâm, dùng đinh bấm/chốt xoay cố định tại tâm $O$. Thử nghiệm quay và điều chỉnh.
c) Sản phẩm: Sản phẩm thực tế **"Vòng quay hành động xanh"** hoàn chỉnh, xoay trơn tru, đúng chuẩn kích thước toán học.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phát lệnh chế tạo. Yêu cầu các nhóm tuân thủ quy tắc an toàn khi dùng kéo, compa nhọn; giữ gìn vệ sinh lớp học, thu gom giấy thừa vào túi tái chế.<br>- **GV:** Trình chiếu hình ảnh mẫu sản phẩm chuẩn để HS đối chiếu thao tác kỹ thuật.<br>- **HS:** Mở hòm dụng cụ, phân công công việc cụ thể.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Các thành viên phối hợp nhịp nhàng:<br>  + HS 1 & 2: Dùng compa vẽ đường tròn bán kính $R = 15\\text{ cm}$ trên bìa carton, cắt rời làm thân đĩa.<br>  + HS 3: Dùng thước đo góc xác định chuẩn 4 góc ở tâm: $144^\\circ$ (xanh lá), $90^\\circ$ (vàng), $72^\\circ$ (xanh dương), $54^\\circ$ (cam).<br>  + HS 4: Cắt các miếng giấy màu hình quạt tròn dán kín mặt đĩa theo đúng cung đã chia; dán icon tái chế, bóng đèn, giọt nước, mầm cây.<br>  + HS 5: Dán dải viền hình vành khuyên trắng, dùng bút màu vẽ hoa văn họa tiết dây lá và hoa.<br>  + HS 6: Cắt mũi tên màu đen, gài chốt xoay ở tâm đĩa, kiểm tra độ quay trơn tru.<br>- **GV:** Đi từng bàn hướng dẫn kỹ thuật: Cách bấm đinh chốt vừa phải không quá chặt làm kẹt kim, không quá lỏng làm kim bị lắc; nhắc nhở kiểm tra các góc đã cộng lại đúng $360^\\circ$ chưa.<br><br>**+ Bước 3: Báo cáo, thử nghiệm**<br>- Từng nhóm thực hiện quay thử kim 5 lần, ghi nhận kim dừng ngẫu nhiên ở các ô màu, vòng quay cân bằng không bị lệch trọng tâm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tiến độ hoàn thành của các nhóm. Chuẩn bị cho phần trưng bày và báo cáo thuyết minh. | **Quy trình công nghệ chế tạo STEM:**<br>1. Đo đạc & Cắt phôi đĩa tròn ($R = 15\\text{ cm}$).<br>2. Đo góc ở tâm & Dán 4 hình quạt tròn màu sắc.<br>3. Vẽ hoa văn dải viền ngoài (Hình vành khuyên).<br>4. Lắp ráp trục quay kim mũi tên.<br>5. Thử nghiệm cơ cấu quay và hoàn thiện thẩm mỹ.<br><br>![Mô hình "Vòng quay hành động xanh" hoàn chỉnh của học sinh](khbd-ill:vong-quay-hanh-dong-xanh) |

## E. BÁO CÁO, ĐÁNH GIÁ SẢN PHẨM VÀ YÊU CẦU NỘP HỒ SƠ STEM (HOẠT ĐỘNG 5) (10 phút)
a) Mục tiêu: HS trưng bày sản phẩm "Vòng quay hành động xanh", thuyết minh về quá trình tính toán toán học, kỹ thuật chế tạo và thông điệp giáo dục môi trường; đánh giá sản phẩm theo Rubric chuẩn; tiếp nhận yêu cầu nộp hồ sơ sản phẩm STEM.
b) Nội dung:
- Trưng bày sản phẩm tại bục giảng.
- Đại diện nhóm thuyết minh 2 phút: Kích thước toán học, ý nghĩa các tỉ lệ phần trăm và cách thức hoạt động.
- Đánh giá chéo giữa các nhóm và đánh giá của giáo viên theo Rubric.
- GV công bố quy định nộp hồ sơ sản phẩm STEM.
c) Sản phẩm: Bảng điểm đánh giá Rubric của các nhóm và Bộ hồ sơ sản phẩm STEM nộp về tổ bộ môn.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Yêu cầu các nhóm đặt vòng quay lên bàn trưng bày.<br>- **GV:** Hướng dẫn cách thức chấm điểm theo Phiếu đánh giá Rubric (Thang điểm 100):<br>  1. Tính chính xác toán học (40 điểm).<br>  2. Cơ cấu kỹ thuật và trục quay (25 điểm).<br>  3. Tính thẩm mỹ và thông điệp xanh (20 điểm).<br>  4. Hồ sơ thiết kế và thuyết minh nhóm (15 điểm).<br>- **HS:** Chuẩn bị nội dung thuyết minh và phiếu chấm chéo.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đại diện các nhóm lần lượt lên giới thiệu:<br>  + Giải thích cơ sở toán học tính góc $144^\\circ, 90^\\circ, 72^\\circ, 54^\\circ$, độ dài cung viền và diện tích từng hình quạt.<br>  + Giải thích công thức tính diện tích dải viền vành khuyên $42.75\\pi \\approx 134.30\\text{ cm}^2$.<br>  + Thực hiện quay kim chỉ nam trước lớp.<br>  + Nêu thông điệp: "Mỗi ngày một hành động xanh vì Trái Đất tương lai".<br>- Các nhóm còn lại quan sát và chấm điểm chéo trên phiếu Rubric.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Thư ký lớp tổng hợp điểm số các nhóm.<br>- Các nhóm đặt câu hỏi phản biện: "Tại sao nhóm bạn lại chọn tỉ lệ rác tái chế cao nhất $40\\%$?"; "Làm thế nào để trục quay không bị tuột sau nhiều lần quay?".<br><br>**+ Bước 4: Kết luận, nhận định & Dặn dò**<br>- **GV:** Nhận xét, tổng kết: Các nhóm đều đã chuyển hóa xuất sắc các công thức toán học khô khan (độ dài cung, diện tích hình quạt, diện tích vành khuyên) thành một sản phẩm STEM vừa đẹp mắt, vừa có tính ứng dụng tuyên truyền thực tế rất cao.<br>- **GV:** Tuyên dương nhóm đạt điểm cao nhất và phổ biến quy định nộp hồ sơ STEM hoàn chỉnh. | **Phiếu đánh giá Rubric sản phẩm STEM (Thang điểm 100):**<br><br>| Tiêu chí | Mức Tốt (8 - 10đ) | Mức Khá (5 - 7đ) | Mức Đạt (1 - 4đ) |<br>| :--- | :--- | :--- | :--- |<br>| **1. Tính chính xác Toán học** *(40đ)* | Tính đúng $100\\%$ số đo 4 góc ở tâm, độ dài 4 cung, 4 diện tích quạt và diện tích vành khuyên; chia góc trên đĩa sai số $< 1^\\circ$. | Tính đúng các công thức nhưng có sai sót nhỏ trong làm tròn số; sai số đo góc từ $1^\\circ - 3^\\circ$. | Nhầm lẫn công thức $S_q$ hoặc $S_{vk}$; sai số đo góc $> 3^\\circ$. |<br>| **2. Kỹ thuật & Trục quay** *(25đ)* | Đĩa cắt tròn đều, không móp méo; kim quay trơn tru, quay được nhiều vòng, dừng ngẫu nhiên. | Đĩa tròn tương đối; kim quay được nhưng đôi lúc bị rít nhẹ. | Đĩa méo; trục quay lỏng lẻo hoặc kẹt cứng không quay được. |<br>| **3. Thẩm mỹ & Thông điệp** *(20đ)* | Màu sắc hài hòa, biểu tượng xanh rõ nét, viền vành khuyên vẽ hoa văn đẹp mắt, thông điệp ý nghĩa. | Cắt dán khá sạch sẽ; có vẽ biểu tượng nhưng viền trang trí đơn điệu. | Cắt dán lem nhem keo; thiếu biểu tượng hoặc viền trang trí. |<br>| **4. Hồ sơ STEM & Báo cáo** *(15đ)* | Hồ sơ bản vẽ kỹ thuật đầy đủ, trình bày tự tin, thuyết phục, trả lời tốt câu hỏi phản biện. | Hồ sơ đủ số liệu nhưng trình bày chưa mạch lạc; trả lời phản biện còn lúng túng. | Hồ sơ sơ sài, thiếu bản vẽ thiết kế hoặc thiếu số liệu toán học. | |

---

# IV. QUY ĐỊNH YÊU CẦU NỘP HỒ SƠ SẢN PHẨM STEM
Mỗi nhóm học tập hoàn thiện và nộp lại **Bộ hồ sơ học tập STEM Bài 15** cho Giáo viên bộ môn Toán theo các yêu cầu sau:

1. **Thành phần Hồ sơ nộp:**
   - **Mục 1 - Sản phẩm thực tế:** 01 "Vòng quay hành động xanh" hoàn chỉnh bằng bìa carton cứng (đường kính $30\\text{ cm}$, bán kính $R = 15\\text{ cm}$), kim mũi tên xoay được, dán nhãn tên nhóm và danh sách thành viên ở mặt sau.
   - **Mục 2 - Bản thuyết minh kỹ thuật (Báo cáo giấy A4):**
     + Trang 1: Thông tin nhóm, tên dự án STEM, thông điệp môi trường.
     + Trang 2: Bản vẽ kỹ thuật hình học tỉ lệ $1:2$ ghi rõ các kích thước $R, n_i, l_i, S_{qi}, R_1, R_2, S_{vk}$.
     + Trang 3: Bảng số liệu toán học chi tiết (công thức áp dụng, các bước thay số và kết quả làm tròn).
     + Trang 4: Bảng phân công nhiệm vụ và tự đánh giá mức độ hoàn thành của từng thành viên trong nhóm.
   - **Mục 3 - Nhật ký chế tạo (Tệp số):** Ảnh chụp hoặc video ngắn (dưới 1 phút) ghi lại cảnh nhóm cùng nhau đo vẽ, cắt dán và thử nghiệm vòng quay gửi lên nhóm học tập trực tuyến (Zalo/Google Classroom).

2. **Thời hạn nộp:**
   - Sản phẩm thực tế và Bản thuyết minh giấy: Nộp trực tiếp tại lớp vào đầu tiết học tiếp theo.
   - Nhật ký số: Nộp trước $21\\text{h}00$ ngày hôm sau.

3. **Hướng dẫn bài tập về nhà:**
   - Vận dụng công thức $S_{vk} = \\pi (R_1^2 - R_2^2)$ giải bài toán thực tế: Tính chi phí trải cỏ nhân tạo cho một lối đi dạo hình vành khuyên bao quanh đài phun nước tròn trong công viên, biết bán kính ngoài là $8\\text{ m}$, bán kính trong là $5\\text{ m}$, giá cỏ nhân tạo là $120\\,000$ đồng/$\\text{m}^2$.
   - Chuẩn bị bài học tiếp theo: **Luyện tập chung (trang 96 SGK)**.
"""

out_dir = "TROLYTHIEN/TEMP"
os.makedirs(out_dir, exist_ok=True)
md_path = os.path.join(out_dir, "KHBD_Toan9_Bai15_STEM_VongQuayHanhDongXanh.md")

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Đã tạo tệp Markdown STEM Bài 15 thành công tại: {md_path}")
"""
