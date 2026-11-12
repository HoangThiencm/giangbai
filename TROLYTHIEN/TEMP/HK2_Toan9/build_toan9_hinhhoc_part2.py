# -*- coding: utf-8 -*-
"""
Script sinh 7 KHBD Chương X: Các hình khối trong thực tiễn & Ôn tập cuối HK2 & HĐTN (Tiết 47 - 60) - Toán 9 HK2
Chuẩn Công văn 5512 V2.1 - 100% Word Equation OMML - Mindmaps 300 DPI
"""

import os

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan9"
os.makedirs(temp_dir, exist_ok=True)

lessons = [
    # 33: Bài 31 (Tiết 47-50)
    {
        "filename": "33_KHBD_Toan9_Bai31_HinhTruVaHinhNon_STEM_Tiet47-50.md",
        "md": """TIẾT 47, 48, 49, 50 - BÀI 31: HÌNH TRỤ VÀ HÌNH NÓN (BÀI HỌC STEM)
*Thời lượng thực hiện: 04 tiết (180 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết sự tạo thành và các yếu tố hình học của hình trụ: Khi quay một hình chữ nhật một vòng quanh một cạnh cố định, ta được một hình trụ. Nhận biết đáy (hai hình tròn bằng nhau), bán kính đáy $R$, trục, chiều cao $h$, đường sinh $l$ ($l = h$).
- Nắm vững công thức tính diện tích xung quanh: $S_{xq} = 2\\pi Rh$, diện tích toàn phần: $S_{tp} = 2\\pi Rh + 2\\pi R^2$ và thể tích hình trụ: $V = \\pi R^2 h$.
- Nhận biết sự tạo thành và các yếu tố hình học của hình nón: Khi quay một tam giác vuông một vòng quanh một cạnh góc vuông cố định, ta được một hình nón. Nhận biết đỉnh, đáy (hình tròn), bán kính đáy $R$, chiều cao $h$, đường sinh $l$ ($l^2 = h^2 + R^2$).
- Nắm vững công thức tính diện tích xung quanh: $S_{xq} = \\pi Rl$, diện tích toàn phần: $S_{tp} = \\pi Rl + \\pi R^2$ và thể tích hình nón: $V = \\frac{1}{3} \\pi R^2 h$.
- Thực hiện hoạt động STEM: Thiết kế và chế tạo mô hình nón lá hoặc hộp đựng bút hình trụ từ bìa carton tái chế.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự cắt dán bìa giấy hình quạt tròn và hình chữ nhật để cuộn tạo hình nón, hình trụ.
- Giao tiếp và hợp tác: Làm việc nhóm phân công vai trò thiết kế sản phẩm STEM, tính toán lượng vật liệu cần dùng.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Tưởng tượng không gian tròn xoay, phân biệt rõ đường sinh $l$ và chiều cao $h$ của hình nón.
- Năng lực mô hình hoá toán học: Tính dung tích bồn chứa nước hình trụ, lượng tôn cần để gò chiếc phễu hình nón.

## 3. Về phẩm chất
- Nâng cao ý thức bảo vệ môi trường thông qua việc tái chế bìa carton, chai lọ cũ làm sản phẩm STEM.
- Tinh thần khéo léo, cẩn thận và tính thẩm mỹ trong tạo hình sản phẩm.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2 Kết nối tri thức, KHBD, mô hình hình trụ và hình nón bằng nhựa trong, mô hình khai triển phẳng, máy chiếu.
2. Học sinh: Bìa carton, kéo, keo dán, compa, thước kẻ, máy tính cầm tay, bút màu trang trí sản phẩm STEM.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khơi gợi sự quan sát các vật thể tròn xoay quen thuộc trong đời sống: Lon sữa bò, ống cống, chiếc nón lá, kem ốc quế.
b) Nội dung: Quan sát lon sữa bò và chiếc nón lá, nhận xét về dạng hình học của chúng.
c) Sản phẩm: HS chỉ ra lon sữa bò có dạng hình trụ, chiếc nón lá có dạng hình nón.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho HS quan sát lon nước ngọt hình trụ và chiếc nón lá hình nón. Nêu câu hỏi về sự tạo thành của chúng.<br>- **HS:** Quan sát vật thật.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh theo cặp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Lon nước có 2 đáy tròn phẳng và mặt xung quanh uốn cong; chiếc nón có 1 đáy tròn và đỉnh nhọn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Trong toán học, hai hình khối này gọi là hình trụ và hình nón. Chúng ta sẽ cùng nghiên cứu cấu tạo, công thức tính và thực hành chế tạo sản phẩm STEM. | Dẫn nhập vào bài học STEM Hình trụ và Hình nón. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (130 phút)
### Hoạt động 2.1: Hình trụ và các công thức tính toán (40 phút)
a) Mục tiêu: Nắm vững sự tạo thành hình trụ, công thức $S_{xq} = 2\\pi Rh$, $S_{tp} = 2\\pi Rh + 2\\pi R^2$ và $V = \\pi R^2 h$.
b) Nội dung: Khảo sát hình trụ sinh bởi phép quay hình chữ nhật quanh một cạnh; xây dựng công thức qua hình khai triển phẳng (gồm một hình chữ nhật kích thước $2\\pi R \\times h$ và hai hình tròn bán kính $R$).
c) Sản phẩm: Vở ghi bài và bài tập tính $S_{xq}, V$ của hình trụ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dùng mô hình quay hình chữ nhật $ABCD$ quanh trục $AB$.<br>Giới thiệu:<br>- Hai đáy là hai hình tròn bằng nhau bán kính $R$.<br>- Chiều cao $h = AB$, đường sinh $l = CD$ ($l = h$).<br>- Diện tích xung quanh: Khai triển ra hình chữ nhật có kích thước $2\\pi R$ và $h$, nên $S_{xq} = 2\\pi Rh$.<br>- Thể tích: $V = S_{đáy} \\cdot h = \\pi R^2 h$.<br>- **HS:** Tiếp nhận công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Một lon sữa đặc hình trụ có bán kính đáy $R = 3{,}5\\text{ cm}$, chiều cao $h = 8\\text{ cm}$. Tính diện tích vỏ lon (diện tích toàn phần) và thể tích lon sữa (lấy $\\pi \\approx 3{,}14$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $S_{xq} = 2 \\cdot 3{,}14 \\cdot 3{,}5 \\cdot 8 = 175{,}84\\text{ cm}^2$. $S_{đáy} = 3{,}14 \\cdot 3{,}5^2 = 38{,}465\\text{ cm}^2$.<br>$S_{tp} = 175{,}84 + 2 \\cdot 38{,}465 = 252{,}77\\text{ cm}^2$.<br>$V = 38{,}465 \\cdot 8 = 307{,}72\\text{ cm}^3 \\approx 308\\text{ ml}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt các công thức hình trụ. | **1. Hình trụ:**<br>- Bán kính đáy $R$, chiều cao $h$, đường sinh $l = h$.<br>- Diện tích xung quanh:<br>$$S_{xq} = 2\\pi Rh$$<br>- Diện tích toàn phần:<br>$$S_{tp} = 2\\pi Rh + 2\\pi R^2$$<br>- Thể tích:<br>$$V = \\pi R^2 h$$ |

### Hoạt động 2.2: Hình nón và các công thức tính toán (45 phút)
a) Mục tiêu: Nắm vững sự tạo thành hình nón, mối liên hệ $l^2 = h^2 + R^2$, công thức $S_{xq} = \\pi Rl$ và $V = \\frac{1}{3} \\pi R^2 h$.
b) Nội dung: Khảo sát hình nón sinh bởi phép quay tam giác vuông quanh một cạnh góc vuông; khai triển mặt xung quanh là một hình quạt tròn bán kính $l$.
c) Sản phẩm: Vở ghi bài và lời giải bài toán nón lá.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dùng mô hình quay tam giác vuông $SOA$ quanh trục $SO$.<br>Giới thiệu:<br>- Đỉnh $S$, đáy là hình tròn tâm $O$ bán kính $R = OA$.<br>- Chiều cao $h = SO$, đường sinh $l = SA$. Theo Pythagore: $l^2 = h^2 + R^2$.<br>- Khai triển mặt xung quanh là hình quạt tròn bán kính $l$, độ dài cung bằng chu vi đáy $2\\pi R$. Do đó $S_{xq} = \\pi Rl$.<br>- Thể tích: $V = \\frac{1}{3} \\pi R^2 h$.<br>- **HS:** Ghi chép công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Một chiếc nón lá có đường kính đáy $40\\text{ cm}$ (bán kính $R = 20\\text{ cm}$), độ dài đường sinh $l = 30\\text{ cm}$. Tính diện tích lá cọ cần dùng để phủ mặt xung quanh nón (lấy $\\pi \\approx 3{,}14$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $S_{xq} = \\pi Rl = 3{,}14 \\cdot 20 \\cdot 30 = 1884\\text{ cm}^2$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Cần chú ý phân biệt giữa đường sinh $l$ và chiều cao $h$. | **2. Hình nón:**<br>- Bán kính đáy $R$, chiều cao $h$, đường sinh $l$. Mối liên hệ: $l^2 = h^2 + R^2$.<br>- Diện tích xung quanh:<br>$$S_{xq} = \\pi Rl$$<br>- Diện tích toàn phần:<br>$$S_{tp} = \\pi Rl + \\pi R^2$$<br>- Thể tích:<br>$$V = \\frac{1}{3} \\pi R^2 h$$ |

### Hoạt động 2.3: Thực hành trải nghiệm STEM (45 phút)
a) Mục tiêu: Học sinh tự tay thiết kế và chế tạo mô hình hộp đựng bút hình trụ hoặc chiếc nón mini hình nón từ bìa carton.
b) Nội dung: Các nhóm sử dụng compa, kéo, thước đo góc để cắt khai triển phẳng và cuộn dán mô hình, trang trí sản phẩm.
c) Sản phẩm: Sản phẩm STEM hoàn chỉnh của 4 tổ (hộp đựng bút trang trí đẹp mắt).
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao tiêu chí sản phẩm STEM:<br>1. Kích thước đúng bản vẽ thiết kế.<br>2. Đường dán chắc chắn, đứng vững trên mặt bàn.<br>3. Tính toán chính xác diện tích vật liệu và thể tích chứa đựng.<br>4. Thẩm mỹ sáng tạo.<br>- **HS:** Các nhóm nhận nguyên vật liệu bìa tái chế.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân công cắt bìa, dán đáy, trang trí màu nước.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện các nhóm trưng bày sản phẩm lên bàn trưng bày phía trước lớp, thuyết trình về quy trình chế tạo và tính toán thể tích.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chấm điểm sản phẩm STEM theo thang tiêu chí. | Hoạt động STEM: Chế tạo thành công mô hình hình trụ và hình nón từ vật liệu tái chế. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (10 phút)
a) Mục tiêu: Giải bài toán kết hợp so sánh thể tích giữa hình trụ và hình nón có cùng bán kính đáy và cùng chiều cao.
b) Nội dung: Một hình trụ và một hình nón có cùng bán kính đáy $R$ và cùng chiều cao $h$. So sánh thể tích của chúng.
c) Sản phẩm: Thể tích hình trụ gấp 3 lần thể tích hình nón ($V_{trụ} = 3 V_{nón}$).
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** So sánh $V_{trụ} = \\pi R^2 h$ và $V_{nón} = \\frac{1}{3} \\pi R^2 h$.<br>- **HS:** So sánh tỉ số.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $V_{trụ} : V_{nón} = 3 : 1$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khẳng định: Nếu đổ đầy nước vào hình nón rồi trút vào hình trụ có cùng đáy và chiều cao, cần trút đúng 3 lần thì đầy hình trụ. | Thể tích hình trụ gấp đúng 3 lần thể tích hình nón có cùng đáy và chiều cao. |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Dặn dò chuẩn bị bài học tiếp theo về Hình cầu (khối tròn xoay hoàn hảo nhất trong không gian).
b) Nội dung: Quan sát các vật thể hình cầu trong đời sống (quả bóng đá, trái đất, viên bi kính).
c) Sản phẩm: HS ghi nhận nhiệm vụ chuẩn bị bài.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị cho Bài 32: Hình cầu (bài học STEM tiếp theo).<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Kết thúc buổi học**<br>- Cả lớp thu dọn bàn ghế gọn gàng. | Dặn dò chuẩn bị bài Hình cầu. |
"""
    },

    # 34: Bài 32 (Tiết 51-52)
    {
        "filename": "34_KHBD_Toan9_Bai32_HinhCau_STEM_Tiet51-52.md",
        "md": """TIẾT 51, 52 - BÀI 32: HÌNH CẦU (BÀI HỌC STEM)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết sự tạo thành và các yếu tố của hình cầu, mặt cầu: Khi quay nửa hình tròn tâm $O$ bán kính $R$ một vòng quanh đường kính cố định, ta được một hình cầu. Nửa đường tròn tạo nên mặt cầu. Tâm $O$ và bán kính $R$ của nửa hình tròn là tâm và bán kính của hình cầu (mặt cầu).
- Nhận biết mặt cắt của hình cầu bởi một mặt phẳng luôn là một hình tròn. Mặt cắt đi qua tâm là hình tròn lớn có bán kính $R$.
- Nắm vững công thức tính diện tích mặt cầu:
  $$S = 4\\pi R^2 = \\pi d^2$$
- Nắm vững công thức tính thể tích của hình cầu:
  $$V = \\frac{4}{3} \\pi R^3 = \\frac{1}{6} \\pi d^3$$
- Thực hiện hoạt động STEM: Tính toán vật liệu và thể tích quả địa cầu mini hoặc quả bóng thể thao.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đo đường kính quả bóng bàn, quả bóng đá bằng thước kẹp hoặc dây quấn để tính bán kính $R$.
- Giao tiếp và hợp tác: Làm việc nhóm đo đạc và tính thể tích không khí được bơm vào quả bóng.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng tưởng tượng mặt cắt hình học không gian 3 chiều.
- Năng lực mô hình hoá toán học: Tính diện tích da may quả bóng đá FIFA, diện tích bề mặt Trái Đất.

## 3. Về phẩm chất
- Khơi gợi sự tò mò về vũ trụ, thiên văn học và hình dạng các hành tinh hình cầu.
- Cẩn thận, chính xác khi thực hiện tính toán số mũ ba $R^3$ và số vô tỉ $\\pi$.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, mô hình quả địa cầu, mô hình cắt quả cầu, thước cuộn, máy chiếu.
2. Học sinh: SGK, quả bóng bàn hoặc bóng tennis, thước dây cuộn, máy tính cầm tay, vở ghi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Kích hoạt sự quan sát hình ảnh Trái Đất và các hành tinh trong Hệ Mặt Trời.
b) Nội dung: Trái Đất, Mặt Trăng, Mặt Trời và các hành tinh trong vũ trụ đều có dạng hình gì?
c) Sản phẩm: HS trả lời: Có dạng hình cầu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu hình ảnh Trái Đất chụp từ vệ tinh. Hỏi về dạng hình học.<br>- **HS:** Quan sát hình ảnh.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trả lời: Hình cầu.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Hình cầu là hình khối tròn xoay hoàn hảo và phổ biến nhất trong vũ trụ. Hôm nay ta tìm hiểu công thức diện tích và thể tích hình cầu. | Giới thiệu hình cầu qua hình ảnh Trái Đất và thiên thể vũ trụ. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Khái niệm hình cầu, mặt cầu và mặt cắt (30 phút)
a) Mục tiêu: Nắm vững sự tạo thành hình cầu bởi phép quay nửa hình tròn quanh đường kính; tính chất mọi mặt cắt bởi mặt phẳng đều là hình tròn.
b) Nội dung: Định nghĩa hình cầu, tâm $O$, bán kính $R$, đường kính $d = 2R$; mặt cắt hình cầu.
c) Sản phẩm: Vở ghi bài định nghĩa và tính chất mặt cắt.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dùng mô hình quay nửa hình tròn quanh đường kính $AB$.<br>Giới thiệu:<br>- Hình tạo thành là một hình cầu.<br>- Nửa đường tròn tạo thành mặt cầu.<br>- Tâm $O$, bán kính $R$, đường kính $d = 2R$.<br>- Tính chất mặt cắt: Cắt hình cầu bởi bất kì mặt phẳng nào, ta đều được mặt cắt là một hình tròn.<br>- **HS:** Tiếp nhận kiến thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Lấy ví dụ thực tế về việc bổ quả dưa hấu, quả cam theo mặt phẳng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Mặt cắt luôn luôn là hình tròn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa khái niệm hình tròn lớn khi mặt phẳng đi qua tâm $O$. | **1. Hình cầu và Mặt cầu:**<br>- Tạo thành khi quay nửa hình tròn quanh đường kính cố định.<br>- Tâm $O$, bán kính $R$, đường kính $d = 2R$.<br>- Mặt cắt bởi một mặt phẳng luôn là một hình tròn. Nếu mặt phẳng đi qua tâm thì mặt cắt là hình tròn lớn có bán kính $R$. |

### Hoạt động 2.2: Diện tích mặt cầu và Thể tích hình cầu (35 phút)
a) Mục tiêu: Nắm vững và vận dụng công thức $S = 4\\pi R^2 = \\pi d^2$ và $V = \\frac{4}{3} \\pi R^3 = \\frac{1}{6} \\pi d^3$.
b) Nội dung: Phát biểu định lí của Archimedes về diện tích mặt cầu và thể tích hình cầu; giải bài toán tính diện tích da quả bóng đá và thể tích quả bóng.
c) Sản phẩm: Vở ghi công thức và bài giải ví dụ mẫu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu công thức:<br>- Diện tích mặt cầu:<br>$$S = 4\\pi R^2 = \\pi d^2$$<br>- Thể tích hình cầu:<br>$$V = \\frac{4}{3} \\pi R^3 = \\frac{1}{6} \\pi d^3$$<br>- **HS:** Ghi chép công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Một quả bóng đá tiêu chuẩn số 5 có đường kính $d = 22\\text{ cm}$ (bán kính $R = 11\\text{ cm}$). Tính diện tích da may quả bóng và thể tích không khí bên trong quả bóng (lấy $\\pi \\approx 3{,}14$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** $S = 4 \\cdot 3{,}14 \\cdot 11^2 = 4 \\cdot 3{,}14 \\cdot 121 = 1519{,}76\\text{ cm}^2$.<br>$V = \\frac{4}{3} \\cdot 3{,}14 \\cdot 11^3 = \\frac{4}{3} \\cdot 3{,}14 \\cdot 1331 \\approx 5572{,}45\\text{ cm}^3 \\approx 5{,}57\\text{ lít}$.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách làm và lưu ý đơn vị $R^3$ trong công thức thể tích. | **2. Công thức Diện tích và Thể tích:**<br>- Diện tích mặt cầu:<br>$$S = 4\\pi R^2 = \\pi d^2$$<br>- Thể tích hình cầu:<br>$$V = \\frac{4}{3} \\pi R^3 = \\frac{1}{6} \\pi d^3$$ |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (15 phút)
a) Mục tiêu: Vận dụng công thức tính bán kính $R$ khi biết thể tích hoặc diện tích mặt cầu.
b) Nội dung: Một bồn chứa khí hóa lỏng hình cầu có thể tích $V = 288\\pi\\text{ m}^3$.
1) Tính bán kính $R$ của bồn chứa khí.
2) Tính diện tích kim loại cần dùng để làm vỏ bồn chứa (diện tích mặt cầu).
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập tính ngược từ thể tích $V = 288\\pi\\text{ m}^3$ ra $R$ và $S$.<br>- **HS:** Thiết lập phương trình thể tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $\\frac{4}{3} \\pi R^3 = 288\\pi \\Rightarrow R^3 = 288 \\cdot \\frac{3}{4} = 216 \\Rightarrow R = \\sqrt[3]{216} = 6\\text{ m}$.<br>Diện tích mặt cầu: $S = 4\\pi R^2 = 4\\pi \\cdot 6^2 = 144\\pi \\approx 452{,}16\\text{ m}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán tính ngược căn bậc ba chuẩn mực. | **Bài giải:**<br>1) Ta có công thức thể tích hình cầu:<br>$$V = \\frac{4}{3} \\pi R^3$$<br>Theo đề bài ta có:<br>$$\\frac{4}{3} \\pi R^3 = 288\\pi$$<br>$$R^3 = 288 \\cdot \\frac{3}{4} = 216$$<br>Suy ra $R = \\sqrt[3]{216} = 6\\text{ (m)}$.<br>Vậy bán kính của bồn chứa là $6\\text{ m}$.<br><br>2) Diện tích vỏ bồn chứa là:<br>$$S = 4\\pi R^2 = 4\\pi \\cdot 6^2 = 144\\pi\\text{ (m}^2\\text{)} \\approx 452{,}16\\text{ (m}^2\\text{)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tính tỉ số thể tích giữa hình cầu nội tiếp trong một hình lập phương.
b) Nội dung: Cho hình cầu nội tiếp hình lập phương cạnh $a$ (đường kính cầu $d = a$). Tính tỉ số thể tích hình cầu so với hình lập phương.
c) Sản phẩm: Tỉ số $\\frac{V_{cầu}}{V_{hộp}} = \\frac{\\frac{1}{6}\\pi a^3}{a^3} = \\frac{\\pi}{6} \\approx 52{,}4\\%$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Một quả bóng tròn xếp vừa khít trong hộp vuông chiếm bao nhiêu phần trăm thể tích hộp?<br>- **HS:** Lập tỉ số thể tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $V_{cầu} / V_{hộp} = \\frac{\\pi}{6} \\approx 0{,}524 = 52{,}4\\%$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị cho tiết Luyện tập chung cả 3 hình khối. | Quả cầu chiếm xấp xỉ $52{,}4\\%$ thể tích chiếc hộp lập phương chứa khít nó. |
"""
    },

    # 35: Tiết 53: Luyện tập chung (Mindmap: mindmap_toan9_hinh_tiet53.png)
    {
        "filename": "35_KHBD_Toan9_LuyenTapChung_Tiet53.md",
        "md": """TIẾT 53 - LUYỆN TẬP CHUNG: HÌNH TRỤ, HÌNH NÓN VÀ HÌNH CẦU
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- So sánh, phân biệt và củng cố toàn diện hệ thống công thức diện tích và thể tích của ba khối tròn xoay: Hình trụ, Hình nón và Hình cầu:
  + Hình trụ: $S_{xq} = 2\\pi Rh$, $V = \\pi R^2 h$.
  + Hình nón: $S_{xq} = \\pi Rl$, $V = \\frac{1}{3} \\pi R^2 h$ ($l^2 = h^2 + R^2$).
  + Hình cầu: $S = 4\\pi R^2$, $V = \\frac{4}{3} \\pi R^3$.
- Rèn luyện kỹ năng giải các bài toán thực tế về vật thể ghép (vật thể gồm hình trụ gắn hình nón hoặc hình trụ gắn bán cầu).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp bảng so sánh ba khối tròn xoay bằng sơ đồ tư duy.
- Giao tiếp và hợp tác: Hợp tác nhóm phân tích mô hình vật thể ghép phức tạp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng phân rã vật thể thực tế thành tổng hoặc hiệu các khối tròn xoay cơ bản.
- Năng lực giải quyết vấn đề toán học: Tính toán chi phí sơn, lượng nguyên vật liệu chế tạo chi tiết máy.

## 3. Về phẩm chất
- Rèn thói quen làm việc khoa học, tỉ mỉ, kiểm tra kĩ đơn vị đo lường thể tích ($1\\text{ dm}^3 = 1\\text{ lít}$, $1\\text{ m}^3 = 1000\\text{ lít}$).
- Tinh thần đồng đội, chủ động trao đổi kiến thức.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI, máy chiếu, bảng phụ ghi bài toán vật thể ghép.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, dụng cụ vẽ hình.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Trò chơi nối nhanh công thức tính thể tích của ba khối tròn xoay.
b) Nội dung: Nối tên khối hình với công thức thể tích tương ứng.
c) Sản phẩm: Bảng nối chính xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu trò chơi nối công thức thể tích: Trụ $\\rightarrow \\pi R^2 h$; Nón $\\rightarrow \\frac{1}{3} \\pi R^2 h$; Cầu $\\rightarrow \\frac{4}{3} \\pi R^3$.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc to các công thức.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương và chuyển sang sơ đồ tư duy tổng hợp. | Khởi động: Nối nhanh công thức thể tích 3 khối tròn xoay. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (15 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức ba khối tròn xoay bằng sơ đồ tư duy (15 phút)
a) Mục tiêu: Khái quát toàn bộ công thức và đặc điểm hình học của Hình trụ, Hình nón, Hình cầu bằng sơ đồ tư duy trực quan 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Hình trụ - Nón - Cầu.
c) Sản phẩm: Sơ đồ tư duy được hệ thống trong vở của học sinh.

![Sơ đồ tư duy Luyện tập chung Hình trụ Hình nón Hình cầu Tiết 53](khbd-ill:mindmap-toan9-hinh-tiet53)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Hình trụ - Nón - Cầu. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 4 nhánh:<br>1) Hình trụ (quay hình chữ nhật, $S_{xq} = 2\\pi Rh, V = \\pi R^2 h$).<br>2) Hình nón (quay tam giác vuông, $l^2 = h^2 + R^2, S_{xq} = \\pi Rl, V = \\frac{1}{3} \\pi R^2 h$).<br>3) Hình cầu (quay nửa hình tròn, $S = 4\\pi R^2, V = \\frac{4}{3} \\pi R^3$).<br>4) Vật thể ghép và ứng dụng thực tế.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện HS phân tích mối quan hệ tỉ lệ thể tích $3 : 1$ giữa hình trụ và hình nón.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại bảng công thức và chuyển sang giải bài toán vật thể ghép. | **Bảng tổng hợp công thức:**<br>1. Hình trụ: $S_{xq} = 2\\pi Rh;\\; V = \\pi R^2 h$.<br>2. Hình nón: $S_{xq} = \\pi Rl;\\; V = \\frac{1}{3} \\pi R^2 h$ ($l = \\sqrt{h^2 + R^2}$).<br>3. Hình cầu: $S = 4\\pi R^2;\\; V = \\frac{4}{3} \\pi R^3$. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (20 phút)
a) Mục tiêu: Tính thể tích và diện tích bề mặt của một chiếc bồn chứa nước gồm phần thân hình trụ và hai đầu là hai nửa hình cầu.
b) Nội dung: Một téc nước inox có phần thân là hình trụ dài $2\\text{ m}$ (chiều cao $h = 2\\text{ m}$), hai đầu là hai nửa hình cầu có cùng bán kính đáy $R = 0{,}6\\text{ m}$.
1) Tính thể tích của téc nước (lấy $\\pi \\approx 3{,}14$, làm tròn đến chữ số thập phân thứ hai).
2) Tính diện tích toàn bộ bề mặt inox của téc nước.
c) Sản phẩm: Lời giải chi tiết trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài toán téc nước gồm thân trụ và hai đầu bán cầu.<br>- **HS:** Phân tích: Hai nửa hình cầu ghép lại đúng thành một hình cầu bán kính $R$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) Thể tích téc nước bằng tổng thể tích hình trụ và một hình cầu:<br>$V = V_{trụ} + V_{cầu} = \\pi R^2 h + \\frac{4}{3} \\pi R^3$.<br>$V = 3{,}14 \\cdot 0{,}6^2 \\cdot 2 + \\frac{4}{3} \\cdot 3{,}14 \\cdot 0{,}6^3 = 2{,}2608 + 0{,}90432 \\approx 3{,}17\\text{ m}^3$ ($3170\\text{ lít}$).<br>2) Diện tích bề mặt bằng diện tích xung quanh hình trụ cộng diện tích một mặt cầu:<br>$S = S_{xq\\text{ trụ}} + S_{mặt cầu} = 2\\pi Rh + 4\\pi R^2$.<br>$S = 2 \\cdot 3{,}14 \\cdot 0{,}6 \\cdot 2 + 4 \\cdot 3{,}14 \\cdot 0{,}6^2 = 7{,}536 + 4{,}5216 \\approx 12{,}06\\text{ m}^2$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán vật thể ghép thực tế mẫu mực. | **Bài giải:**<br>Hai đầu téc nước là hai nửa hình cầu có cùng bán kính $R = 0{,}6\\text{ m}$, ghép lại thành một hình cầu bán kính $R = 0{,}6\\text{ m}$.<br>1) Thể tích của téc nước là:<br>$$V = V_{trụ} + V_{cầu} = \\pi R^2 h + \\frac{4}{3} \\pi R^3$$<br>$$V \\approx 3{,}14 \\cdot 0{,}6^2 \\cdot 2 + \\frac{4}{3} \\cdot 3{,}14 \\cdot 0{,}6^3 \\approx 2{,}26 + 0{,}90 = 3{,}17\\text{ (m}^3\\text{)}$$<br>(Dung tích chứa khoảng $3170$ lít nước).<br><br>2) Diện tích toàn bộ bề mặt inox của téc nước là:<br>$$S = S_{xq\\text{ trụ}} + S_{mặt cầu} = 2\\pi Rh + 4\\pi R^2$$<br>$$S \\approx 2 \\cdot 3{,}14 \\cdot 0{,}6 \\cdot 2 + 4 \\cdot 3{,}14 \\cdot 0{,}6^2 \\approx 7{,}54 + 4{,}52 = 12{,}06\\text{ (m}^2\\text{)}$$ |

## D. VẬN DỤNG VÀ MỞ RỘNG (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tính khối lượng nước chứa trong téc nước khi đầy biết $1\\text{ m}^3$ nước nặng $1\\text{ tấn}$.
b) Nội dung: Téc nước chứa $3{,}17\\text{ m}^3$ nước nặng bao nhiêu tấn?
c) Sản phẩm: Kết quả khoảng $3{,}17\\text{ tấn}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tính khối lượng nước trong téc.<br>- **HS:** Nhân với 1 tấn/m$^3$.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $3{,}17 \\cdot 1 = 3{,}17\\text{ tấn}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Báo cáo miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi và dặn dò chuẩn bị bài tập cuối chương X. | Khối lượng nước trong téc xấp xỉ $3{,}17\\text{ tấn}$. |
"""
    },

    # 36: Tiết 54-55: Bài tập cuối chương X (Mindmap: mindmap_toan9_hinh_tiet54_55.png)
    {
        "filename": "36_KHBD_Toan9_BaiTapCuoiChuong10_Tiet54-55.md",
        "md": """TIẾT 54, 55 - BÀI TẬP CUỐI CHƯƠNG X
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Ôn tập và củng cố toàn diện kiến thức Chương X: Các hình khối trong thực tiễn:
  + Hình trụ: Đặc điểm hình học, diện tích xung quanh $S_{xq} = 2\\pi Rh$, toàn phần $S_{tp} = 2\\pi Rh + 2\\pi R^2$, thể tích $V = \\pi R^2 h$.
  + Hình nón: Đường sinh $l = \\sqrt{h^2 + R^2}$, diện tích xung quanh $S_{xq} = \\pi Rl$, toàn phần $S_{tp} = \\pi Rl + \\pi R^2$, thể tích $V = \\frac{1}{3} \\pi R^2 h$.
  + Hình cầu: Diện tích mặt cầu $S = 4\\pi R^2 = \\pi d^2$, thể tích hình cầu $V = \\frac{4}{3} \\pi R^3 = \\frac{1}{6} \\pi d^3$.
  + Các bài toán vật thể ghép tròn xoay trong đời sống, công nghiệp và kỹ thuật.
- Rèn luyện kỹ năng tổng hợp giải các bài toán trắc nghiệm và tự luận cuối chương trong SGK.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tổng kết kiến thức Chương X dưới dạng sơ đồ tư duy hoàn chỉnh.
- Giao tiếp và hợp tác: Hợp tác nhóm thảo luận giải các bài toán vật thể tròn xoay phức hợp.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng tưởng tượng không gian 3 chiều và lập luận toán học chính xác.
- Năng lực mô hình hoá toán học: Chuyển đổi các vật thể thực tế thành mô hình hình khối tương ứng.

## 3. Về phẩm chất
- Cẩn thận trong các phép tính căn bậc hai, bình phương và làm tròn số thập phân.
- Tinh thần nghiêm túc ôn tập chuẩn bị cho đợt Ôn tập và Kiểm tra cuối năm học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, sơ đồ tư duy vector 300 DPI Chương X, máy chiếu, bảng phụ.
2. Học sinh: SGK, vở ghi, máy tính cầm tay, dụng cụ vẽ hình.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Khởi động ôn tập bằng trò chơi giải nhanh các câu hỏi trắc nghiệm kiến thức cốt lõi Chương X.
b) Nội dung: Trả lời nhanh 3 câu hỏi về công thức diện tích xung quanh hình nón, thể tích hình trụ và thể tích hình cầu.
c) Sản phẩm: Câu trả lời chính xác của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu 3 câu hỏi trắc nghiệm nhanh kiểm tra công thức Chương X.<br>- **HS:** Xung phong trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đọc to các công thức $\\pi Rl$, $\\pi R^2 h$, $\\frac{4}{3}\\pi R^3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS trả lời miệng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá đúng và chuyển sang sơ đồ tư duy tổng kết toàn chương. | Tái hiện các công thức trọng tâm Chương X. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Tổng kết Chương X bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Khái quát toàn bộ cấu trúc kiến thức Chương X: Các hình khối trong thực tiễn.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI tổng kết Chương X.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Bài tập cuối chương X Tiết 54 - 55](khbd-ill:mindmap-toan9-hinh-tiet54-55)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI tổng kết Chương X. Yêu cầu HS phân tích các nhánh chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trình bày 4 nhánh:<br>1) Bảng công thức diện tích ($S_{xq\\text{ trụ}} = 2\\pi Rh, S_{xq\\text{ nón}} = \\pi Rl, S_{\\text{cầu}} = 4\\pi R^2$).<br>2) Bảng công thức thể tích ($V_{\\text{trụ}} = \\pi R^2 h, V_{\\text{nón}} = \\frac{1}{3}\\pi R^2 h, V_{\\text{cầu}} = \\frac{4}{3}\\pi R^3$).<br>3) Khối tròn xoay kết hợp (vật thể ghép trụ + nón, trụ + cầu).<br>4) Bài toán kỹ thuật và đời sống (dung tích bồn chứa, sơn phủ).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ trình bày tổng quan chương.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt sơ đồ và nhấn mạnh các dạng toán điển hình. | **Tổng kết toàn bộ Chương X:**<br>1. Hệ thống công thức diện tích và thể tích của hình trụ, hình nón, hình cầu.<br>2. Phương pháp giải bài toán vật thể ghép tròn xoay.<br>3. Ứng dụng thực tế tính toán vật liệu và dung tích chứa đựng. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
a) Mục tiêu: Giải bài toán vật thể ghép gồm hình trụ và hình nón (mô hình ngọn hải đăng hoặc bút chì).
b) Nội dung: Một ngọn hải đăng có phần dưới là hình trụ có đường kính đáy $6\\text{ m}$ (bán kính $R = 3\\text{ m}$), chiều cao $h_1 = 15\\text{ m}$. Phần mái che phía trên có dạng hình nón có chiều cao $h_2 = 4\\text{ m}$ và cùng bán kính đáy $R = 3\\text{ m}$.
1) Tính độ dài đường sinh $l$ của phần mái hình nón.
2) Tính diện tích toàn bộ mặt ngoài của ngọn hải đăng (gồm diện tích xung quanh hình trụ và diện tích xung quanh hình nón, không tính đáy dưới).
3) Tính tổng thể tích không gian bên trong ngọn hải đăng.
c) Sản phẩm: Lời giải chi tiết 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài toán ngọn hải đăng ghép hình trụ và hình nón.<br>- **HS:** Vẽ hình phác họa không gian.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) Đường sinh hình nón: $l = \\sqrt{h_2^2 + R^2} = \\sqrt{4^2 + 3^2} = 5\\text{ m}$.<br>2) Diện tích mặt ngoài:<br>$S = S_{xq\\text{ trụ}} + S_{xq\\text{ nón}} = 2\\pi R h_1 + \\pi R l = 2\\pi \\cdot 3 \\cdot 15 + \\pi \\cdot 3 \\cdot 5 = 90\\pi + 15\\pi = 105\\pi \\approx 329{,}7\\text{ m}^2$.<br>3) Thể tích không gian bên trong:<br>$V = V_{\\text{trụ}} + V_{\\text{nón}} = \\pi R^2 h_1 + \\frac{1}{3} \\pi R^2 h_2 = \\pi \\cdot 3^2 \\cdot 15 + \\frac{1}{3} \\pi \\cdot 3^2 \\cdot 4 = 135\\pi + 12\\pi = 147\\pi \\approx 461{,}58\\text{ m}^3$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán vật thể ghép tròn xoay mẫu mực. | **Bài giải:**<br>1) Độ dài đường sinh $l$ của phần mái hình nón là:<br>$$l = \\sqrt{h_2^2 + R^2} = \\sqrt{4^2 + 3^2} = \\sqrt{16 + 9} = \\sqrt{25} = 5\\text{ (m)}$$<br><br>2) Diện tích toàn bộ mặt ngoài của ngọn hải đăng là:<br>$$S = S_{xq\\text{ trụ}} + S_{xq\\text{ nón}} = 2\\pi R h_1 + \\pi R l$$<br>$$S = 2\\pi \\cdot 3 \\cdot 15 + \\pi \\cdot 3 \\cdot 5 = 90\\pi + 15\\pi = 105\\pi\\text{ (m}^2\\text{)} \\approx 329{,}7\\text{ (m}^2\\text{)}$$<br><br>3) Tổng thể tích không gian bên trong ngọn hải đăng là:<br>$$V = V_{\\text{trụ}} + V_{\\text{nón}} = \\pi R^2 h_1 + \\frac{1}{3} \\pi R^2 h_2$$<br>$$V = \\pi \\cdot 3^2 \\cdot 15 + \\frac{1}{3} \\pi \\cdot 3^2 \\cdot 4 = 135\\pi + 12\\pi = 147\\pi\\text{ (m}^3\\text{)} \\approx 461{,}58\\text{ (m}^3\\text{)}$$ |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Chuẩn bị cho tuần Ôn tập cuối học kì II phần Hình học tiếp theo.
b) Nội dung: Rà soát lại toàn bộ kiến thức Hình học cả năm học (Hệ thức lượng trong tam giác vuông, Đường tròn, Tứ giác nội tiếp, Khối tròn xoay).
c) Sản phẩm: HS ghi nhận nhiệm vụ tự học ở nhà.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị cho 2 tiết Ôn tập cuối HKII Hình học: Chuẩn bị compa, thước kẻ và đề cương ôn tập.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự ôn luyện lại các kiến thức hình học.<br><br>**+ Bước 3: Kết thúc buổi học**<br>- Cả lớp chào giáo viên. | Dặn dò chuẩn bị tiết Ôn tập cuối HKII Hình học. |
"""
    },

    # 37: Tiết 56-57: Ôn tập cuối HK2 Hình học (Mindmap: mindmap_toan9_hinh_tiet56_57.png)
    {
        "filename": "37_KHBD_Toan9_OnTapCuoiHK2_HinhHoc_Tiet56-57.md",
        "md": """TIẾT 56, 57 - ÔN TẬP VÀ KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Hình học Học kì II môn Toán 9:
  + Chương IX: Góc với đường tròn, đường tròn ngoại tiếp và nội tiếp tam giác, bốn dấu hiệu nhận biết tứ giác nội tiếp kinh điển, đa giác đều.
  + Chương X: Hình trụ, hình nón, hình cầu, công thức tính diện tích xung quanh, toàn phần và thể tích.
- Rèn luyện kỹ năng giải các bài toán hình học phẳng tổng hợp 3 - 4 câu chuẩn cấu trúc đề thi tuyển sinh vào lớp 10 THPT.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức hình học cả học kì dưới dạng sơ đồ tư duy bao quát.
- Giao tiếp và hợp tác: Tự tin trao đổi các phương pháp chứng minh tiếp tuyến, vuông góc, thẳng hàng trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng suy luận logic, chứng minh hình học chặt chẽ, không ngộ nhận hình vẽ.
- Năng lực giải quyết vấn đề toán học: Phân tích bài toán thực tế thành mô hình hình khối tròn xoay hoặc tứ giác nội tiếp.

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, vẽ hình chính xác và rõ ràng bằng compa, eke.
- Tự tin, sẵn sàng tâm thế bước vào kì kiểm tra đánh giá cuối năm học và kì thi tuyển sinh vào lớp 10.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 9 Tập 2, KHBD, đề cương ôn tập cuối HK2 phần Hình học, sơ đồ tư duy vector 300 DPI, máy chiếu.
2. Học sinh: SGK, vở ghi, compa, thước kẻ, máy tính cầm tay, đề cương ôn tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Định hướng ôn tập và nắm rõ cấu trúc đề thi cuối năm học và thi vào 10 phần Hình học.
b) Nội dung: GV giới thiệu ma trận đề kiểm tra cuối HK2 phần Hình học (chiếm khoảng 3,5 - 4,0 điểm trong thang điểm 10).
c) Sản phẩm: HS xác định được các nội dung trọng tâm cần ôn tập.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phổ biến cấu trúc phần hình học trong đề thi: Gồm câu trắc nghiệm góc nội tiếp, khối tròn xoay; 1 câu tính thể tích hình thực tế và 1 bài hình phẳng tổng hợp 3 câu.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự rà soát các nội dung kiến thức còn cảm thấy chưa vững.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu các dạng bài cần thầy cô giải đáp kĩ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chiếu sơ đồ tư duy tổng kết toàn diện hình học HK2. | Nắm vững ma trận đề kiểm tra cuối HK2 phần Hình học. |

## B. HÌNH THÀNH KIẾN THỨC MỚI (HOẠT ĐỘNG 2) (25 phút)
### Hoạt động 2.1: Hệ thống hóa toàn bộ Hình học HK2 bằng sơ đồ tư duy (25 phút)
a) Mục tiêu: Hệ thống hóa toàn bộ Chương IX (Đường tròn ngoại tiếp/nội tiếp) và Chương X (Các hình khối trong thực tiễn) bằng sơ đồ tư duy 300 DPI.
b) Nội dung: Trình chiếu và phân tích sơ đồ tư duy vector 300 DPI Ôn tập cuối HK2 Hình học 9.
c) Sản phẩm: Sơ đồ tư duy được hoàn thiện trong vở ghi của học sinh.

![Sơ đồ tư duy Ôn tập cuối HK2 Hình học Tiết 56 - 57](khbd-ill:mindmap-toan9-hinh-tiet56-57)

d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy vector 300 DPI Ôn tập cuối HK2 Hình học 9. Yêu cầu HS phân tích hai trụ cột chính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích 2 trụ cột:<br>1) Chương IX - Đường tròn: Góc nội tiếp, góc chắn nửa đường tròn vuông, 4 dấu hiệu nhận biết tứ giác nội tiếp, đa giác đều.<br>2) Chương X - Các hình khối thực tiễn: Hình trụ ($2\\pi Rh, \\pi R^2 h$), hình nón ($\\pi Rl, \\frac{1}{3}\\pi R^2 h$), hình cầu ($4\\pi R^2, \\frac{4}{3}\\pi R^3$).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS nhắc lại kĩ thuật phân tích tứ giác nội tiếp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt sơ đồ và nhấn mạnh phương pháp trình bày chứng minh hình học mạch lạc, có căn cứ. | **Hệ thống kiến thức Hình học HK2:**<br>1. Góc nội tiếp và tính chất cùng chắn.<br>2. Bốn dấu hiệu nhận biết tứ giác nội tiếp kinh điển.<br>3. Đường tròn ngoại tiếp và nội tiếp tam giác, đa giác đều.<br>4. Công thức diện tích và thể tích hình trụ, hình nón, hình cầu.<br>5. Phương pháp làm bài thi hình học tuyển sinh vào lớp 10. |

## C. LUYỆN TẬP (HOẠT ĐỘNG 3) (55 phút)
### Hoạt động 3.1: Luyện tập bài toán thực tế hình khối tròn xoay (20 phút)
a) Mục tiêu: Giải bài toán tính diện tích xung quanh và thể tích một chiếc phễu hình nón hoặc hình trụ.
b) Nội dung: Một chiếc phễu hình nón có bán kính đáy $R = 9\\text{ cm}$, chiều cao $h = 12\\text{ cm}$.
1) Tính độ dài đường sinh $l$ của chiếc phễu.
2) Tính diện tích tôn cần dùng để gò chiếc phễu (diện tích xung quanh), bỏ qua mép gò.
3) Tính thể tích nước tối đa mà chiếc phễu có thể chứa.
c) Sản phẩm: Lời giải hoàn chỉnh trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài tập chiếc phễu hình nón.<br>- **HS:** Tóm tắt dữ kiện và áp dụng công thức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** $l = \\sqrt{12^2 + 9^2} = 15\\text{ cm}$.<br>$S_{xq} = \\pi Rl = \\pi \\cdot 9 \\cdot 15 = 135\\pi \\approx 423{,}9\\text{ cm}^2$.<br>$V = \\frac{1}{3} \\pi R^2 h = \\frac{1}{3} \\pi \\cdot 9^2 \\cdot 12 = 324\\pi \\approx 1017{,}36\\text{ cm}^3 \\approx 1{,}02\\text{ lít}$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán hình nón thực tế. | **Bài giải:**<br>1) Độ dài đường sinh của chiếc phễu là:<br>$$l = \\sqrt{h^2 + R^2} = \\sqrt{12^2 + 9^2} = \\sqrt{144 + 81} = \\sqrt{225} = 15\\text{ (cm)}$$<br><br>2) Diện tích tôn cần dùng để gò chiếc phễu là:<br>$$S_{xq} = \\pi Rl = \\pi \\cdot 9 \\cdot 15 = 135\\pi\\text{ (cm}^2\\text{)} \\approx 423{,}9\\text{ (cm}^2\\text{)}$$<br><br>3) Thể tích nước tối đa phễu có thể chứa là:<br>$$V = \\frac{1}{3} \\pi R^2 h = \\frac{1}{3} \\pi \\cdot 9^2 \\cdot 12 = 324\\pi\\text{ (cm}^3\\text{)} \\approx 1017{,}36\\text{ (cm}^3\\text{)}$$ |

### Hoạt động 3.2: Luyện tập bài toán Hình học phẳng tuyển sinh 10 (35 phút)
a) Mục tiêu: Giải bài toán hình học phẳng tổng hợp 3 câu chuẩn cấu trúc đề thi tuyển sinh vào lớp 10.
b) Nội dung: Cho đường tròn $(O; R)$ và điểm $A$ nằm ngoài $(O)$ sao cho $OA = 2R$. Kẻ hai tiếp tuyến $AB, AC$ với $(O)$ ($B, C$ là tiếp điểm). Kẻ dây cung $BD$ song song với $AC$. Đoạn thẳng $AD$ cắt $(O)$ tại điểm thứ hai là $E$ ($E \\neq D$).
1) Chứng minh tứ giác $ABOC$ nội tiếp đường tròn.
2) Chứng minh $AB^2 = AE \\cdot AD$.
3) Gọi $I$ là trung điểm của dây $ED$. Chứng minh năm điểm $A, B, I, O, C$ cùng thuộc một đường tròn.
c) Sản phẩm: Lời giải chi tiết 3 câu trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao bài toán hình học phẳng tổng hợp chuẩn thi vào 10.<br>- **HS:** Vẽ hình cẩn thận bằng compa và thước kẻ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:**<br>1) $\\widehat{ABO} + \\widehat{ACO} = 90^\\circ + 90^\\circ = 180^\\circ \\Rightarrow ABOC$ nội tiếp đường tròn đường kính $AO$.<br>2) $\\Delta ABE \\backsim \\Delta ADB$ (g.g) vì góc $A$ chung và $\\widehat{ABE} = \\widehat{ADB}$ (góc tạo bởi tiếp tuyến và dây cung bằng góc nội tiếp cùng chắn $\\overparen{BE}$). Suy ra $AB^2 = AE \\cdot AD$.<br>3) Vì $I$ là trung điểm của dây $ED$ không đi qua tâm nên $OI \\perp ED \\Rightarrow \\widehat{AIO} = 90^\\circ$. Điểm $I$ nhìn đoạn thẳng $AO$ dưới góc $90^\\circ$. Do đó điểm $I$ cũng thuộc đường tròn đường kính $AO$. Vậy 5 điểm $A, B, I, O, C$ cùng thuộc đường tròn đường kính $AO$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS lên bảng trình bày chi tiết.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài toán 5 điểm cùng thuộc một đường tròn kinh điển trong các đề thi vào lớp 10. | **Bài giải:**<br>1) Vì $AB, AC$ là hai tiếp tuyến của $(O)$ nên:<br>$$AB \\perp OB \\Rightarrow \\widehat{ABO} = 90^\\circ$$<br>$$AC \\perp OC \\Rightarrow \\widehat{ACO} = 90^\\circ$$<br>Xét tứ giác $ABOC$ có:<br>$$\\widehat{ABO} + \\widehat{ACO} = 90^\\circ + 90^\\circ = 180^\\circ$$<br>Vậy tứ giác $ABOC$ nội tiếp đường tròn đường kính $AO$.<br><br>2) Xét $\\Delta ABE$ và $\\Delta ADB$ có:<br>- $\\widehat{BAD}$ chung;<br>- $\\widehat{ABE} = \\widehat{ADB}$ (cùng chắn cung $\\overparen{BE}$).<br>Do đó $\\Delta ABE \\backsim \\Delta ADB$ (g.g).<br>Suy ra:<br>$$\\frac{AB}{AD} = \\frac{AE}{AB} \\Rightarrow AB^2 = AE \\cdot AD$$<br><br>3) Vì $I$ là trung điểm của dây $ED$ (không đi qua tâm $O$) nên:<br>$$OI \\perp ED \\Rightarrow \\widehat{AIO} = 90^\\circ$$<br>Do đó điểm $I$ thuộc đường tròn đường kính $AO$.<br>Mặt khác, theo câu 1, các điểm $A, B, O, C$ đều thuộc đường tròn đường kính $AO$.<br>Vậy năm điểm $A, B, I, O, C$ cùng thuộc một đường tròn (đường tròn đường kính $AO$). |

## D. VẬN DỤNG VÀ DẶN DÒ (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Nhắc nhở dặn dò chuẩn bị cho tiết Kiểm tra cuối học kì II phần Hình học.
b) Nội dung: Rà soát đồ dùng thi (thước kẻ, eke, compa, bút viết) và quy chế phòng thi.
c) Sản phẩm: HS ghi nhận đầy đủ dặn dò.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Dặn dò chuẩn bị đầy đủ compa, thước kẻ cho tiết Kiểm tra cuối HKII tiếp theo.<br>- **HS:** Lắng nghe và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự kiểm tra lại compa.<br><br>**+ Bước 3: Kết thúc tiết học**<br>- Cả lớp chào giáo viên. | Dặn dò chuẩn bị cho kì Kiểm tra cuối Học kì II Hình học. |
"""
    },

    # 38: Tiết 58: Kiểm tra cuối HK2 Hình học
    {
        "filename": "38_KHBD_Toan9_KiemTraCuoiHK2_HinhHoc_Tiet58.md",
        "md": """TIẾT 58 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II (HÌNH HỌC)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện chuẩn kiến thức kĩ năng phần Hình học Toán 9 Học kì II:
  + Nắm vững và vận dụng các định lí góc nội tiếp, tứ giác nội tiếp.
  + Chứng minh tứ giác nội tiếp, chứng minh các hệ thức hình học và tiếp tuyến.
  + Tính diện tích xung quanh, thể tích hình trụ, hình nón, hình cầu.
  + Kỹ năng vẽ hình chuẩn xác bằng compa và thước kẻ, trình bày lời giải bài toán hình học chặt chẽ.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Ý thức tự giác, trung thực, nghiêm túc làm bài kiểm tra độc lập.
- Giải quyết vấn đề: Phân bổ hợp lí thời gian giữa các câu trắc nghiệm và câu tự luận.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Khả năng lập luận logic, suy diễn hình học chặt chẽ.
- Năng lực mô hình hoá toán học: Giải bài toán ứng dụng hình khối tròn xoay vào thực tế.

## 3. Về phẩm chất
- Trung thực, khách quan trong kiểm tra đánh giá.
- Rèn tính kiên nhẫn, cẩn thận, không bỏ sót các trường hợp.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn theo đúng ma trận và đặc tả đề kiểm tra cuối kì, đáp án và biểu điểm chi tiết.
2. Học sinh: Dụng cụ vẽ hình đầy đủ, máy tính cầm tay, bút viết, giấy thi.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ PHÁT ĐỀ (HOẠT ĐỘNG 1) (5 phút)
a) Mục tiêu: Ổn định phòng thi, phổ biến quy chế và phát đề kiểm tra cho học sinh.
b) Nội dung: GV điểm danh, nhắc nhở quy chế thi và phát đề.
c) Sản phẩm: 100% học sinh nhận đề và ghi đầy đủ thông tin vào giấy làm bài.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Ổn định chỗ ngồi, kiểm tra trật tự, nhắc nhở nghiêm cấm mọi hành vi gian lận.<br>- **HS:** Cất toàn bộ tài liệu và chuẩn bị dụng cụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Phát đề kiểm tra.<br>- **HS:** Kiểm tra độ rõ của đề, ghi thông tin cá nhân.<br><br>**+ Bước 3: Bắt đầu làm bài**<br>- **GV:** Ghi thời gian làm bài lên bảng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giám sát phòng thi nghiêm túc. | Phát đề kiểm tra và ổn định phòng thi. |

## B. TIẾN HÀNH LÀM BÀI KIỂM TRA (HOẠT ĐỘNG 2) (35 phút)
### Ma trận và Đề kiểm tra Hình học cuối HK2 (35 phút)
a) Mục tiêu: Học sinh làm bài kiểm tra độc lập, đạt kết quả cao nhất theo năng lực.
b) Nội dung: Đề gồm 2 phần: Trắc nghiệm (3 điểm) và Tự luận (7 điểm).
c) Sản phẩm: Bài làm hoàn chỉnh trên giấy thi của từng học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Làm bài độc lập**<br>- **HS:** Làm bài nghiêm túc, vẽ hình chính xác vào giấy thi bằng compa.<br>- **GV:** Giám thị bao quát lớp thi.<br><br>**+ Bước 2: Theo dõi thời gian**<br>- **GV:** Nhắc nhở thời gian làm bài (còn 15 phút, còn 5 phút).<br>- **HS:** Soát lại bài làm, kiểm tra kĩ đơn vị đo.<br><br>**+ Bước 3: Hoàn thành bài làm**<br>- **HS:** Sắp xếp lại tờ giấy thi, chuẩn bị nộp bài.<br><br>**+ Bước 4: Hết giờ làm bài**<br>- **GV:** Thu bài kiểm tra của cả lớp. | **Nội dung đề kiểm tra minh họa:**<br>**Phần I. Trắc nghiệm (3 điểm):**<br>- Câu 1: Công thức thể tích hình cầu $V = \\frac{4}{3}\\pi R^3$.<br>- Câu 2: Góc nội tiếp chắn nửa đường tròn bằng $90^\\circ$.<br>- Câu 3: Diện tích xung quanh hình trụ $S_{xq} = 2\\pi Rh$.<br><br>**Phần II. Tự luận (7 điểm):**<br>**Bài 1 (2,0 điểm):** Một hộp sữa hình trụ có đường kính đáy $10\\text{ cm}$ (bán kính $R = 5\\text{ cm}$), chiều cao $h = 14\\text{ cm}$. Tính diện tích vỏ hộp (diện tích toàn phần) và thể tích hộp sữa (lấy $\\pi \\approx 3{,}14$).<br>**Bài 2 (5,0 điểm):** Cho đường tròn $(O; R)$ và một điểm $M$ nằm ngoài đường tròn. Kẻ hai tiếp tuyến $MA, MB$ với $(O)$ ($A, B$ là tiếp điểm). Kẻ đường kính $AC$ của $(O)$. Đoạn thẳng $MC$ cắt đường tròn $(O)$ tại điểm $D$ ($D \\neq C$).<br>a) (2,0 điểm) Chứng minh tứ giác $MAOB$ nội tiếp đường tròn.<br>b) (2,0 điểm) Chứng minh $\\widehat{ADC} = 90^\\circ$ và $MD \\cdot MC = MA^2$.<br>c) (1,0 điểm) Gọi $H$ là giao điểm của $AB$ và $MO$. Chứng minh $\\widehat{MDH} = \\widehat{MOC}$. |

## C. THU BÀI VÀ NHẬN XÉT (HOẠT ĐỘNG 3) (5 phút)
a) Mục tiêu: Thu đủ số lượng bài thi và nhận xét nền nếp buổi kiểm tra.
b) Nội dung: Thu bài theo hàng, kiểm đếm đủ số bài thi và giải tỏa căng thẳng cho học sinh.
c) Sản phẩm: Thu đủ 100% bài kiểm tra của cả lớp.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thu bài kiểm tra của học sinh theo thứ tự bàn học.<br>- **HS:** Nộp bài trật tự, nghiêm túc.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Kiểm đếm khớp số bài thi với sĩ số.<br><br>**+ Bước 3: Nhận xét giờ kiểm tra**<br>- **GV:** Tuyên dương ý thức làm bài nghiêm túc, tự giác của cả lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Dặn dò chuẩn bị cho 2 tiết Hoạt động thực hành trải nghiệm GeoGebra cuối cùng của năm học. | Thu đủ số bài kiểm tra và nhận xét nền nếp phòng thi. |
"""
    },

    # 39: Tiết 59-60: HĐTN GeoGebra Hình học
    {
        "filename": "39_KHBD_Toan9_HDTN_VeHinhGeoGebra_Tiet59-60.md",
        "md": """TIẾT 59, 60 - HOẠT ĐỘNG THỰC HÀNH VÀ TRẢI NGHIỆM: VẼ HÌNH ĐƠN GIẢN VỚI PHẦN MỀM GEOGEBRA
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Sử dụng thành thạo phần mềm toán học GeoGebra để:
  + Dựng đường tròn ngoại tiếp và đường tròn nội tiếp của một tam giác bất kì bằng các công cụ dựng hình trung trực, phân giác.
  + Dựng đa giác đều (tam giác đều, hình vuông, ngũ giác đều, lục giác đều) bằng công cụ `Regular Polygon` (Đa giác đều).
  + Dựng tứ giác nội tiếp và kiểm chứng tính chất tổng hai góc đối bằng $180^\\circ$ khi thay đổi vị trí các đỉnh trên đường tròn.
  + Vẽ các khối tròn xoay 3D (Hình trụ, Hình nón, Hình cầu) trên cửa sổ hiển thị không gian 3 chiều (3D Graphics).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự khám phá các công cụ vẽ hình học không gian 3D trên GeoGebra.
- Giao tiếp và hợp tác: Chia sẻ kinh nghiệm tạo hiệu ứng chuyển động xoay và xuất file ảnh động GIF trong nhóm.

b) Năng lực đặc thù môn Toán:
- Năng lực mô hình hoá toán học: Kết hợp hình học phẳng và hình học không gian 3 chiều trên phần mềm số.
- Năng lực số (NLS):
  + ***3.1.TC2a: HS sử dụng phần mềm GeoGebra để vẽ hình chính xác và sơ đồ hóa các tính chất hình học; 5.3.TC2a: HS sử dụng công cụ số tạo tri thức mới về các khối tròn xoay 3D.***

## 3. Về phẩm chất
- Say mê ứng dụng công nghệ thông tin trong học tập môn Toán.
- Ý thức trách nhiệm, bảo quản tốt trang thiết bị phòng máy vi tính.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Phòng máy vi tính cài sẵn GeoGebra Classic 5 hoặc 6, máy chiếu, các tệp mẫu dựng hình tròn xoay 3D.
2. Học sinh: Máy vi tính phòng thực hành, sổ tay ghi chép câu lệnh GeoGebra.

# III. TIẾN TRÌNH DẠY HỌC

## A. KHỞI ĐỘNG VÀ GIAO NHIỆM VỤ (HOẠT ĐỘNG 1) (10 phút)
a) Mục tiêu: Giới thiệu giao diện không gian 3 chiều (3D Graphics) của GeoGebra và phân công nhiệm vụ cho các nhóm.
b) Nội dung: GV trình chiếu cửa sổ 3D Graphics với hệ trục tọa độ $Oxyz$ và các công cụ tạo hình trụ, nón, cầu.
c) Sản phẩm: 100% học sinh mở được cửa sổ 3D Graphics trên màn hình máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Vào Menu View $\\rightarrow$ Chọn `3D Graphics`. Giới thiệu thanh công cụ 3D:<br>1. Công cụ vẽ mặt cầu (Sphere with Center and Radius).<br>2. Công cụ vẽ hình trụ (Cylinder).<br>3. Công cụ vẽ hình nón (Cone).<br>- **HS:** Mở phần mềm và kích hoạt cửa sổ 3D.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác làm quen chuột xoay góc nhìn không gian 3D.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các nhóm trưởng xác nhận máy tính hoạt động ổn định.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Bắt đầu tiến trình thực hành. | Làm quen giao diện và thanh công cụ 3D Graphics của GeoGebra. |

## B. TIẾN HÀNH THỰC HÀNH TRÊN MÁY TÍNH (HOẠT ĐỘNG 2) (65 phút)
### Hoạt động 2.1: Dựng đường tròn ngoại tiếp và nội tiếp tam giác (25 phút)
a) Mục tiêu: Tự tay dựng đường tròn ngoại tiếp và nội tiếp tam giác trên cửa sổ 2D Graphics.
b) Nội dung: Vẽ $\\Delta ABC$. Dùng công cụ `Perpendicular Bisector` dựng trung trực $\\rightarrow$ giao điểm $O$ $\\rightarrow$ vẽ đường tròn ngoại tiếp. Dùng công cụ `Angle Bisector` dựng phân giác $\\rightarrow$ giao điểm $I$ $\\rightarrow$ vẽ đường tròn nội tiếp.
c) Sản phẩm: Màn hình tam giác với 2 đường tròn nội tiếp và ngoại tiếp chuẩn xác.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn các bước dựng hình trên cửa sổ 2D:<br>1. Dùng công cụ Polygon vẽ tam giác $ABC$.<br>2. Dựng 2 đường trung trực, lấy giao điểm $O$. Chọn công cụ `Circle with Center through Point` vẽ đường tròn tâm $O$ qua $A$.<br>3. Kéo rê các đỉnh $A, B, C$ quan sát đường tròn luôn ôm khít 3 đỉnh.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Quan sát hiện tượng: Khi tam giác tù thì tâm $O$ tự động nhảy ra ngoài tam giác; khi vuông thì $O$ nằm chính giữa cạnh huyền.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS các nhóm trầm trồ trước tính năng hình học động của GeoGebra.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, đây là minh chứng trực quan sinh động nhất cho các định lí đã học. | Dựng thành công đường tròn ngoại tiếp và nội tiếp tam giác động trên GeoGebra. |

### Hoạt động 2.2: Dựng các khối tròn xoay 3D (Hình trụ, nón, cầu) (40 phút)
a) Mục tiêu: Tạo các mô hình 3D hình trụ, hình nón, hình cầu và quan sát từ mọi góc nhìn trong không gian.
b) Nội dung: Nhập lệnh hoặc dùng công cụ 3D để tạo hình trụ bán kính 2 chiều cao 5, hình nón bán kính 3 chiều cao 4, hình cầu bán kính 3.
c) Sản phẩm: Mô hình 3D sống động xoay tròn trên màn hình của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn tại dòng lệnh Input cửa sổ 3D:<br>- Vẽ hình cầu tâm $O(0; 0; 0)$ bán kính $3$: Nhập `Sphere((0, 0, 0), 3)`.<br>- Vẽ hình trụ: Chọn công cụ `Cylinder`, nhấp điểm đáy $(0; 0; 0)$, điểm đỉnh $(0; 0; 5)$, nhập bán kính $2$.<br>- Vẽ hình nón: Chọn công cụ `Cone`, nhấp đáy $(0; 0; 0)$, đỉnh $(0; 0; 4)$, nhập bán kính $3$.<br>- **HS:** Thao tác nhập lệnh và tạo khối.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đổi màu sắc trong suốt (Opacity) cho các khối hình, kích hoạt tính năng tự động xoay không gian 3D.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Màn hình hiển thị các khối tròn xoay tuyệt đẹp xoay tròn trong không gian.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá cao sự sáng tạo và kỹ năng công nghệ của học sinh. | Tạo thành công mô hình 3D khối tròn xoay hình trụ, nón, cầu trên GeoGebra. |

## C. BÁO CÁO KẾT QUẢ VÀ ĐÁNH GIÁ (HOẠT ĐỘNG 3) (10 phút)
a) Mục tiêu: Các nhóm trình chiếu sản phẩm 3D của mình lên máy chiếu và giải thích các yếu tố hình học.
b) Nội dung: Đại diện 4 nhóm lên bảng thuyết trình sản phẩm.
c) Sản phẩm: Đánh giá và chấm điểm hoạt động thực hành của giáo viên.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Gọi đại diện các nhóm lên trình chiếu sản phẩm.<br>- **HS:** Kết nối máy tính và thuyết minh ngắn gọn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Giải thích: Chiều cao, bán kính đáy, góc nghiêng của đường sinh trên mô hình 3D.<br><br>**+ Bước 3: Nhận xét chéo**<br>- Các nhóm đặt câu hỏi và nhận xét cho nhau.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tuyên dương, cho điểm xuất sắc các nhóm có sản phẩm hoàn thiện và thuyết trình tốt. | Báo cáo, chia sẻ và đánh giá sản phẩm hình học 3D GeoGebra. |

## D. TỔNG KẾT NĂM HỌC VÀ DẶN DÒ ÔN THI VÀO LỚP 10 (HOẠT ĐỘNG 4) (5 phút)
a) Mục tiêu: Tổng kết toàn bộ chương trình môn Toán lớp 9 và dặn dò ôn thi tuyển sinh vào lớp 10 THPT.
b) Nội dung: GV chúc mừng cả lớp đã hoàn thành toàn diện chương trình Toán cấp THCS, truyền cảm hứng và dặn dò chiến lược ôn thi vào lớp 10.
c) Sản phẩm: Kế hoạch ôn thi vào lớp 10 của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Tổng kết: Chúc mừng các em đã hoàn thành trọn vẹn chương trình môn Toán lớp 9 và 4 năm THCS. Kì thi tuyển sinh vào lớp 10 đang chờ đón các em phía trước.<br>- **HS:** Lắng nghe lời dặn dò tâm huyết của thầy cô.<br><br>**+ Bước 2: Dặn dò chiến lược thi 10**<br>- **GV:** Dặn dò:<br>1. Nắm chắc phần cơ bản (rút gọn biểu thức, giải phương trình, hệ thức Viète, câu hình a-b).<br>2. Trình bày bài thi cẩn thận, từng bước có căn cứ, kết luận nghiệm rõ ràng.<br>3. Giữ gìn sức khỏe, tự tin và bình tĩnh khi bước vào phòng thi.<br><br>**+ Bước 3: Kết thúc năm học**<br>- Cả lớp đứng lên chào giáo viên kết thúc khóa học môn Toán 9. | Tổng kết chương trình Toán 9 và dặn dò định hướng ôn thi tuyển sinh vào lớp 10. |
"""
    },
]

for lesson in lessons:
    filepath = os.path.join(temp_dir, lesson["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(lesson["md"].strip() + "\n")
    print(f" -> Đã tạo Markdown: {filepath}")

print(f"Hoàn tất tạo đợt 5 (7 bài Chương X & Ôn tập cuối HK2 & HĐTN Tiết 47 - 60) Toán 9 HK2!")
