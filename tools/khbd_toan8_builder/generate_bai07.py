# -*- coding: utf-8 -*-
import os

OUT_DIR = "tools/khbd_toan8_builder"
os.makedirs(OUT_DIR, exist_ok=True)

bai_07_content = r"""Tiết 12 - LUYỆN TẬP CHUNG
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hoá toàn diện mối quan hệ biện chứng giữa các tứ giác đặc biệt: Tứ giác $\rightarrow$ Hình thang $\rightarrow$ Hình thang cân / Hình bình hành $\rightarrow$ Hình chữ nhật / Hình thoi $\rightarrow$ Hình vuông.
- Rèn luyện kỹ năng phân tích hình học, tìm kiếm con đường chứng minh tứ giác là hình bình hành, hình chữ nhật, hình thoi, hình vuông.
- Vận dụng tính chất đường trung bình, phân giác và tính chất đường chéo để giải các bài toán chứng minh hình học và giải thích hiện tượng biến dạng cơ học thực tế (khung tre giằng chéo).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa sơ đồ phân loại tứ giác và chủ động hoàn thành các bài tập chứng minh.
- Giao tiếp và hợp tác: Tương tác nhóm hiệu quả, biết phối hợp phân chia công việc trong dự án học tập hình học.

b) Năng lực đặc thù môn Toán:
- Năng lực tư duy và lập luận toán học: Sử dụng phương pháp suy luận ngược và suy luận tiến để tìm lời giải hình học.
- Năng lực mô hình hoá toán học: Giải thích nguyên lý độ cứng vững của tam giác và sự biến dạng của tứ giác qua bài toán khung tre thực tế.

c) Năng lực số (NLS):
- **2.4.TC2a:** HS lựa chọn công cụ số hợp tác hoàn thành dự án "Tứ giác quanh ta".
- **3.2.TC2a:** HS tinh chỉnh và tích hợp hình vẽ vào hệ thống bài giảng điện tử lớp.
- **5.1.TC2a:** HS xác định lỗi khi thực hiện các lệnh quay hình trên phần mềm.

## 3. Về phẩm chất
- Rèn luyện tính cẩn thận, kỷ luật và tác phong vẽ hình hình học chính xác bằng dụng cụ.
- Có ý thức hợp tác trách nhiệm và tinh thần vượt khó trong giải toán hình học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Toán 8 Kết nối tri thức, Kế hoạch bài dạy, bài giảng điện tử, sơ đồ tư duy cây tứ giác, thước kẻ, compa, êke, máy vi tính, Tivi/máy chiếu, phần mềm GeoGebra.
2. Học sinh: SGK, vở ghi, bộ dụng cụ vẽ hình (thước thẳng, compa, êke), máy tính cầm tay, thiết bị thông minh phục vụ học tập nhóm.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt tư duy phân loại tứ giác, nhận diện nhanh các điều kiện để hình bình hành trở thành hình chữ nhật, hình thoi, hình vuông.
b) Nội dung: Trò chơi tiếp sức "Thêm một điều kiện": GV nêu tên hình ban đầu, HS nêu thêm 1 điều kiện để trở thành hình mong muốn.
c) Sản phẩm: Các câu trả lời chuẩn xác của HS về các dấu hiệu nhận biết tứ giác.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu các câu hỏi nhanh:<br>1) Hình bình hành cần thêm điều kiện gì để là Hình chữ nhật?<br>2) Hình bình hành cần thêm điều kiện gì để là Hình thoi?<br>3) Hình chữ nhật cần thêm điều kiện gì để là Hình vuông?<br>4) Hình thoi cần thêm điều kiện gì để là Hình vuông?<br>- **HS:** Chuẩn bị tinh thần trả lời tiếp sức.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Đứng tại chỗ phát biểu nhanh nối tiếp.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Nêu đủ các trường hợp về góc, về cạnh và về đường chéo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá độ thuộc bài của HS, dẫn dắt vào tiết Luyện tập chung để rèn luyện phương pháp chứng minh tổng hợp. | **Khởi động: Các điều kiện chuyển hóa tứ giác**<br>1) Hình bình hành $\rightarrow$ Hình chữ nhật: Thêm 1 góc vuông HOẶC 2 đường chéo bằng nhau.<br>2) Hình bình hành $\rightarrow$ Hình thoi: Thêm 2 cạnh kề bằng nhau HOẶC 2 đường chéo vuông góc HOẶC 1 đường chéo là phân giác.<br>3) Hình chữ nhật $\rightarrow$ Hình vuông: Thêm 2 cạnh kề bằng nhau HOẶC 2 đường chéo vuông góc HOẶC 1 đường chéo là phân giác.<br>4) Hình thoi $\rightarrow$ Hình vuông: Thêm 1 góc vuông HOẶC 2 đường chéo bằng nhau. |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP (32 phút)

### 1. Hoạt động 2.1: Hệ thống hoá kiến thức bằng Mindmap (10 phút)
a) Mục tiêu: Giúp học sinh nắm vững cây phả hệ tứ giác thông qua sơ đồ tư duy trực quan; tích hợp chỉ báo NLS 2.4.TC2a.
b) Nội dung: Quan sát và phân tích sơ đồ tư duy mối quan hệ giữa các tứ giác đặc biệt.
![Sơ đồ tư duy Mối quan hệ giữa các tứ giác đặc biệt](khbd-ill:mindmap_toan8_chuong3_tu_giac)
c) Sản phẩm: Bản ghi sơ đồ phân loại tứ giác của học sinh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu sơ đồ tư duy Cây quan hệ các tứ giác đặc biệt.<br>- **GV:** Yêu cầu HS phân tích các cấp bậc phát triển từ Tứ giác chung $\rightarrow$ Hình thang $\rightarrow$ Hình bình hành $\rightarrow$ Hình chữ nhật/Hình thoi $\rightarrow$ Hình vuông.<br>- **HS:** Quan sát sơ đồ tư duy trên màn hình.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi, chỉ ra các mũi tên liên kết giữa các hình.<br>- ***(Tích hợp NLS 2.4.TC2a: HS lựa chọn công cụ số hợp tác hoàn thành dự án "Tứ giác quanh ta": các nhóm học sinh cùng truy cập không gian số Padlet/Canva để tải lên các hình ảnh chụp thực tế về mái nhà hình thang, cửa sổ hình chữ nhật, hoa văn gạch bông hình thoi, gạch lát nền hình vuông và phân loại chính xác theo sơ đồ tư duy).***<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện HS thuyết minh sơ đồ cây tứ giác.<br>- **HS:** Trình bày tự tin, chỉ rõ vì sao hình vuông là giao thoa hoàn hảo giữa hình chữ nhật và hình thoi.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi phần trình bày của HS, chuyển sang giải quyết bài tập mẫu và bài tập luyện tập. | **Cây quan hệ các tứ giác đặc biệt (Sơ đồ tư duy):**<br>- **Cấp 1: Tứ giác tổng quát** (tổng 4 góc bằng $360^\circ$).<br>- **Cấp 2: Hình thang** (có 2 cạnh đối song song) & **Hình bình hành** (các cạnh đối song song và bằng nhau).<br>- **Cấp 3:**<br>+ **Hình thang cân:** 2 góc kề 1 đáy bằng nhau hoặc 2 đường chéo bằng nhau.<br>+ **Hình chữ nhật:** Có 4 góc vuông, 2 đường chéo bằng nhau và cắt nhau tại trung điểm.<br>+ **Hình thoi:** Có 4 cạnh bằng nhau, 2 đường chéo vuông góc và là phân giác.<br>- **Cấp 4: Hình vuông** (Tứ giác hoàn hảo): Vừa là hình chữ nhật, vừa là hình thoi. |

### 2. Hoạt động 2.2: Giải quyết bài tập (22 phút)
a) Mục tiêu: Rèn luyện kỹ năng dựng hình, chứng minh hình học đa bước; tích hợp chỉ báo NLS 3.2.TC2a và 5.1.TC2a.
b) Nội dung: HS làm việc với Ví dụ SGK (Hình 3.57), Bài tập 3.34, 3.35 (Hình 3.58) SGK trang 73.
![Ví dụ: Dựng hình vuông bằng hai đường tròn](khbd-ill:hinh_sgk_3_57_vi_du)
![Bài tập 3.35: Hình bình hành ABCD và các phân giác](khbd-ill:hinh_sgk_3_58_bai_3_35)
c) Sản phẩm: Lời giải chi tiết Ví dụ, Bài 3.34, Bài 3.35 trong vở HS.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu Hình 3.57 phân tích Ví dụ dựng hình vuông bằng 2 đường tròn.<br>- **GV:** Giao Bài 3.34: Cho $\triangle ABC$, $M, N$ là trung điểm $AB, AC$. Lấy $P$ sao cho $N$ là trung điểm $MP$.<br>a) Tứ giác $AMCP$ là hình gì?<br>b) Điều kiện của $\triangle ABC$ để $AMCP$ là hình chữ nhật; hình thoi; hình vuông?<br>- **GV:** Chiếu Hình 3.58 giao Bài 3.35: Chứng minh tứ giác $EFGH$ tạo bởi các tia phân giác của hình bình hành là hình chữ nhật.<br>- **HS:** Nhận nhiệm vụ, vẽ hình vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bài 3.34: Tứ giác $AMCP$ có 2 đường chéo cắt nhau tại trung điểm $N$ nên là hình bình hành.<br>- ***(Tích hợp NLS 3.2.TC2a: HS tinh chỉnh và tích hợp hình vẽ vào hệ thống bài giảng điện tử lớp: HS dùng phần mềm vẽ hình GeoGebra để vẽ chuẩn xác các tia phân giác của hình bình hành Hình 3.58, xuất ảnh độ nét cao và chèn vào bài trình chiếu nhóm).***<br>- ***(Tích hợp NLS 5.1.TC2a: HS xác định lỗi khi thực hiện các lệnh quay hình trên phần mềm: khi xoay hình bình hành hoặc đối xứng điểm qua trung điểm, HS kiểm tra và sửa lỗi sai lệch góc vuông tại các đỉnh E, F, G, H).***<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **GV:** Mời đại diện lên bảng trình bày bài giải 3.34 và 3.35.<br>- **HS:** Trình bày rõ ràng các bước chứng minh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt phương pháp tìm điều kiện của tam giác để tứ giác trở thành các hình đặc biệt. | **1. Ví dụ (SGK trang 73 - Hình 3.57):**<br>- $C$ thuộc đường tròn $(B; BA)$ nên $BC = BA$.<br>- $C$ thuộc đường tròn $(D; DA)$ nên $DC = DA$.<br>- Theo giả thiết $AB = AD$, suy ra $AB = BC = CD = DA$.<br>Do đó $ABCD$ là hình thoi.<br>- Mặt khác, $AB \perp AD$ nên góc $\widehat{A} = 90^\circ$.<br>Hình thoi $ABCD$ có một góc vuông nên là **hình vuông**.<br><br>**2. Bài tập 3.34 (SGK trang 73):**<br>a) Tứ giác $AMCP$ có hai đường chéo $AC$ và $MP$ cắt nhau tại trung điểm $N$ của mỗi đoạn (theo giả thiết), do đó $AMCP$ là **hình bình hành**.<br>b) Điều kiện của tam giác $ABC$:<br>- Để $AMCP$ là **hình chữ nhật**: Hình bình hành có 1 góc vuông $\implies \widehat{AMC} = 90^\circ \implies CM \perp AB$. Tam giác $ABC$ có trung tuyến $CM$ đồng thời là đường cao nên tam giác $ABC$ phải **cân tại $C$**.<br>- Để $AMCP$ là **hình thoi**: Hình bình hành có hai cạnh kề bằng nhau $\implies AM = MC$. Vì $M$ là trung điểm $AB$ nên $AM = \frac{1}{2}AB$, suy ra $CM = \frac{1}{2}AB$. Tam giác $ABC$ có đường trung tuyến ứng với cạnh $AB$ bằng một nửa cạnh đó nên tam giác $ABC$ phải **vuông tại $C$**.<br>- Để $AMCP$ là **hình vuông**: $AMCP$ vừa là hình chữ nhật vừa là hình thoi $\implies$ Tam giác $ABC$ phải **vuông cân tại $C$**.<br><br>**3. Bài tập 3.35 (SGK trang 73 - Hình 3.58):**<br>Vì $ABCD$ là hình bình hành nên $\widehat{A} + \widehat{D} = 180^\circ$ (hai góc trong cùng phía bù nhau).<br>Do $AG$ và $DE$ là các tia phân giác của góc $A$ và góc $D$ nên:<br>$\widehat{DAG} = \frac{1}{2}\widehat{A}$ và $\widehat{ADE} = \frac{1}{2}\widehat{D}$.<br>Suy ra trong $\triangle ADH$ có:<br>$\widehat{DAH} + \widehat{ADH} = \frac{1}{2}(\widehat{A} + \widehat{D}) = \frac{1}{2} \cdot 180^\circ = 90^\circ$.<br>Do đó $\widehat{AHD} = 180^\circ - 90^\circ = 90^\circ \implies \widehat{EHG} = 90^\circ$ (đối đỉnh).<br>Chứng minh hoàn toàn tương tự ta có:<br>$\widehat{E} = 90^\circ$ và $\widehat{G} = 90^\circ$.<br>Tứ giác $EFGH$ có 3 góc vuông nên là **hình chữ nhật**. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức hình học giải thích hiện tượng thực tế về kết cấu giằng chéo khung tre Bài 3.36.
b) Nội dung: HS giải Bài tập 3.36 SGK trang 73: Một khung tre hình chữ nhật có lắp đinh vít tại bốn đỉnh. Khi khung bị xô lệch, các góc không còn vuông nữa thì khung đó là hình gì? Tại sao? Hỏi khi nẹp thêm một đường chéo vào khung đó thì nó còn bị xô lệch không?
c) Sản phẩm: Lời giải thích khoa học của HS trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tế Bài 3.36 về chiếc khung tre.<br>- **HS:** Lắng nghe và liên hệ với các cấu trúc giàn giáo, cửa gỗ trong thực tế đời sống.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khi khung bị xô lệch, độ dài 4 thanh tre không đổi nên các cạnh đối vẫn bằng nhau $\rightarrow$ trở thành hình bình hành.<br>- **HS:** Khi nẹp thêm 1 thanh chéo, khung được chia thành hai tam giác có độ dài 3 cạnh cố định (theo trường hợp bằng nhau c-c-c). Tam giác có tính chất "bất biến về hình dạng" (độ cứng vững) nên khung không thể bị xô lệch nữa.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- **HS:** Phát biểu giải thích trước lớp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt ý nghĩa thực tiễn: Đây chính là nguyên lý thanh giằng chéo trong xây dựng cầu đường, giàn không gian, khung nhà tiền chế.<br>- **GV dặn dò về nhà:** Ôn tập toàn bộ Chương III, chuẩn bị cho tiết sau "Bài tập cuối chương III". | **Bài tập 3.36 (SGK trang 73):**<br>- Khi khung tre hình chữ nhật bị xô lệch tại các khớp vít, độ dài bốn cạnh không thay đổi (hai cặp cạnh đối vẫn bằng nhau từng đôi một), nhưng các góc không còn là góc vuông nữa. Do đó khung trở thành **hình bình hành**.<br>- Khi nẹp thêm một đường chéo vào khung:<br>Khung được chia thành hai tam giác. Một tam giác khi biết độ dài ba cạnh thì hình dạng và các góc hoàn toàn xác định (không thể biến dạng). Do đó khung tre sẽ trở nên cứng vững và **không còn bị xô lệch nữa**.<br><br>**Dặn dò tự học:**<br>- Vẽ lại sơ đồ cây quan hệ các tứ giác vào vở.<br>- Hoàn thành các bài tập 3.37 và 3.38 vào vở bài tập. |
"""

with open(os.path.join(OUT_DIR, "BAI_07.md"), "w", encoding="utf-8") as f:
    f.write(bai_07_content.strip())
print("Saved BAI_07.md")
