# -*- coding: utf-8 -*-
"""
Script sinh 6 tệp KHBD Markdown môn Tin học 6 (Tuần 28 - 35):
- 07_KHBD_Tin6_KiemTraGiuaHK2_Tiet28.md
- 08_KHBD_Tin6_Bai15_ThuatToan_Tiet29.md
- 09_KHBD_Tin6_Bai16_CacCauTrucDieuKhien_Tiet30-31.md
- 10_KHBD_Tin6_Bai17_ChuongTrinhMayTinh_Tiet32-33.md
- 11_KHBD_Tin6_OnTapCuoiHK2_Tiet34.md (Mindmap: mindmap_tin6_tiet34_cuoihk2.png)
- 12_KHBD_Tin6_KiemTraCuoiHK2_Tiet35.md
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/HK2_Tin6"
os.makedirs(OUT_DIR, exist_ok=True)

# 07. Kiểm tra giữa kỳ II (Tiết 28)
md_07 = """Tiết 28 - KIỂM TRA ĐÁNH GIÁ GIỮA HỌC KÌ II
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá chuẩn xác mức độ nắm vững kiến thức và kỹ năng thực hành của học sinh từ Tuần 19 đến Tuần 27:
  + Chủ đề 4: An toàn thông tin trên Internet.
  + Chủ đề 5: Ứng dụng tin học (Sơ đồ tư duy, Định dạng văn bản, Trình bày bảng biểu, Tìm kiếm và thay thế).
- Phân loại học sinh, phát hiện các kỹ năng còn yếu khi thao tác văn bản trên máy tính để có biện pháp hỗ trợ kịp thời trong nửa sau Học kì II.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Nghiêm túc, độc lập làm bài kiểm tra; tự giác kiểm tra và sửa lỗi trước khi nộp bài.

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng dụng CNTT (NLc): Thao tác thành thạo bàn phím, chuột và các chức năng định dạng văn bản trên máy tính.

## 3. Về phẩm chất
- Trung thực, nghiêm túc, có trách nhiệm với kết quả rèn luyện của bản thân.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn kết hợp Trắc nghiệm (4 điểm) và Thực hành trên máy tính (6 điểm), ma trận, bản đặc tả đề thi, đáp án và biểu điểm chi tiết.
2. Học sinh: Bút viết, máy vi tính hoạt động tốt (đã khóa kết nối Internet tự do trong giờ kiểm tra).

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: ỔN ĐỊNH LỚP VÀ PHÁT ĐỀ (3 phút)
- GV kiểm tra sĩ số, quán triệt nội quy phòng thực hành và quy chế giờ kiểm tra.
- GV phát đề kiểm tra cho từng học sinh và hướng dẫn lưu tệp bài làm vào thư mục quy định: `D:\\KIEMTRA_GIUAHK2\\HoVaTen_Lop6A.docx`.

## B. HOẠT ĐỘNG 2: HỌC SINH LÀM BÀI KIỂM TRA (40 phút)
- **Phần 1: Trắc nghiệm khách quan (15 phút - 4 điểm):** Gồm 8 câu hỏi về an toàn thông tin, sơ đồ tư duy và các lệnh định dạng Word.
- **Phần 2: Thực hành trên máy tính (25 phút - 6 điểm):**
  + Gõ một đoạn văn ngắn và định dạng ký tự, đoạn văn bản theo mẫu yêu cầu (2 điểm).
  + Chèn và định dạng một bảng gồm 4 cột, 3 hàng (2 điểm).
  + Sử dụng công cụ `Replace` để thay thế một từ quy định trong bài (1 điểm).
  + Thiết lập trang in khổ A4 và lưu tệp đúng tên (1 điểm).
- Giáo viên bao quát phòng máy, theo dõi sự cố kỹ thuật (nếu có hỏng phím, chuột) và nhắc nhở học sinh giữ trật tự.

## C. HOẠT ĐỘNG 3: THU BÀI VÀ NHẬN XÉT (2 phút)
- GV cho học sinh dừng thao tác, thu bài trắc nghiệm giấy và thu bài thực hành qua mạng nội bộ hoặc kiểm tra tệp đã lưu trên ổ đĩa `D:`.
- GV nhận xét tinh thần làm bài của cả lớp và dặn dò chuẩn bị cho Bài 15: Thuật toán.
"""

# 08. Bài 15: Thuật toán (Tiết 29)
md_08 = """Tiết 29 - BÀI 15: THUẬT TOÁN
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được khái niệm thuật toán: Thuật toán là một dãy hữu hạn các thao tác được sắp xếp theo một trình tự xác định nhằm giải quyết một bài toán hoặc thực hiện một nhiệm vụ cụ thể.
- Nắm được 3 đặc trưng cơ bản của thuật toán: Tính xác định, Tính hữu hạn và Tính đúng đắn.
- Biết hai cách cơ bản để mô tả thuật toán: Liệt kê các bước bằng ngôn ngữ tự nhiên và Dùng sơ đồ khối (với các hình khối quy ước: hình oval, hình bình hành, hình chữ nhật, hình thoi, mũi tên).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự phân tích một công việc thường ngày (pha trà, nấu cơm, đi đường) thành một chuỗi các bước logic.
- Giải quyết vấn đề và sáng tạo: Lựa chọn trình tự các bước thực hiện tối ưu để đạt được mục tiêu nhanh nhất.

b) Năng lực đặc thù môn Tin học:
- Năng lực giải quyết vấn đề với sự trợ giúp của CNTT (NLd): Rèn luyện tư duy thuật toán, bước đầu tiếp cận tư duy lập trình máy tính.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 5.1.TC1a: Hiểu nguyên lí hoạt động theo thuật toán của máy tính và trí tuệ nhân tạo thông qua chuỗi lệnh logic.***

## 3. Về phẩm chất
- Kiên trì, tư duy chặt chẽ, cẩn thận trong từng bước lập luận.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng điện tử PowerPoint trình chiếu các sơ đồ khối trực quan, phiếu học tập nhóm.
2. Học sinh: SGK Tin học 6, vở ghi, thước kẻ, bút chì.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Dẫn dắt học sinh nhận biết thuật toán thông qua một tình huống đời sống quen thuộc.
b) Nội dung: Quan sát các bước hướng dẫn gấp một chiếc thuyền giấy hoặc công thức luộc trứng. Nếu đảo lộn thứ tự các bước thì có làm được sản phẩm không?
c) Sản phẩm: Câu trả lời khẳng định: Các bước bắt buộc phải thực hiện theo một thứ tự xác định.
d) Tổ chức thực hiện: GV dẫn dắt vào bài mới: Đó chính là khái niệm thuật toán.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (25 phút)
### Hoạt động 2.1: Khái niệm thuật toán và các ví dụ (12 phút)
a) Mục tiêu: Nắm vững định nghĩa thuật toán và phân tích đầu vào (Input), đầu ra (Output).
b) Nội dung: Đọc mục 1 SGK trang 63 - 64; xét ví dụ thuật toán tìm đường đi hoặc thuật toán tính tổng hai số $a$ và $b$.
c) Sản phẩm: Xác định chính xác Input và Output của một bài toán.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu định nghĩa thuật toán.<br>- **GV:** Cho bài toán: Tính diện tích hình chữ nhật có chiều dài $a$ và chiều rộng $b$. Hãy chỉ ra Input, Output và các bước thực hiện?<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Input là $a, b$; Output là Diện tích $S$. Các bước: 1. Nhập $a, b$; 2. Tính $S = a \cdot b$; 3. Thông báo $S$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng trình bày.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt 3 đặc trưng: Tính xác định, hữu hạn và đúng đắn. | **1. Thuật toán là gì?**<br>- Thuật toán là dãy các thao tác rõ ràng, có trình tự nhằm biến đổi đầu vào (Input) thành đầu ra (Output) mong muốn.<br>- **Đặc trưng của thuật toán:**<br>+ **Tính xác định:** Sau mỗi thao tác, máy tính biết rõ thao tác tiếp theo là gì, không có sự mập mờ.<br>+ **Tính hữu hạn:** Thuật toán phải dừng lại sau một số hữu hạn bước.<br>+ **Tính đúng đắn:** Sau khi dừng, thuật toán phải trả về kết quả chính xác theo yêu cầu. |

### Hoạt động 2.2: Các cách mô tả thuật toán và sơ đồ khối (13 phút)
a) Mục tiêu: Phân biệt hai cách mô tả thuật toán và nhận diện các hình khối chuẩn trong sơ đồ khối.
b) Nội dung: Đọc mục 2 SGK trang 64 - 66; vẽ lại các hình khối quy ước vào vở.
c) Sản phẩm: Bảng quy ước hình khối của sơ đồ khối.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu hai cách mô tả thuật toán:<br>1. Liệt kê các bước bằng lời.<br>2. Dùng sơ đồ khối.<br>- **GV:** Chiếu các hình khối quy ước:<br>+ Hình oval: Bắt đầu / Kết thúc.<br>+ Hình bình hành: Nhập (Input) / Xuất (Output) dữ liệu.<br>+ Hình chữ nhật: Các phép tính toán, xử lí.<br>+ Hình thoi: Điều kiện / Kiểm tra rẽ nhánh.<br>+ Mũi tên: Chỉ hướng đi của thuật toán.<br>- **HS:** Vẽ các khối vào vở.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nối các khối thành sơ đồ tính tổng $S = a + b$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ sơ đồ khối hoàn chỉnh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa cách vẽ sơ đồ khối rõ ràng. | **2. Các cách mô tả thuật toán:**<br>- **Cách 1: Liệt kê từng bước bằng lời.**<br>- **Cách 2: Sử dụng sơ đồ khối (Flowchart):**<br>+ **Hình oval:** Bắt đầu (`Start`) hoặc Kết thúc (`End`).<br>+ **Hình bình hành:** Nhập dữ liệu hoặc Xuất kết quả.<br>+ **Hình chữ nhật:** Thao tác xử lí, tính toán.<br>+ **Hình thoi:** Kiểm tra điều kiện (Đúng/Sai).<br>+ **Mũi tên:** Xác định trình tự thực hiện các thao tác. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
a) Mục tiêu: Mô tả thuật toán giải quyết một bài toán số học đơn giản.
b) Nội dung: Mô tả thuật toán kiểm tra một số nguyên dương $n$ là số chẵn hay số lẻ bằng cả 2 cách (liệt kê và vẽ sơ đồ khối).
c) Sản phẩm: Lời giải và sơ đồ khối trong vở của học sinh.
d) Tổ chức thực hiện:
- HS làm bài cá nhân. GV gọi 1 em lên bảng chữa, lớp nhận xét.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
- **Tích hợp NLS & AI (5.1.TC1a):** GV giới thiệu: Các hệ thống AI thông minh thực chất đều được vận hành dựa trên hàng triệu thuật toán logic phức tạp được tối ưu hóa. Dặn dò chuẩn bị cho Bài 16: Các cấu trúc điều khiển.
"""

# 09. Bài 16: Các cấu trúc điều khiển (Tiết 30, 31)
md_09 = """Tiết 30, 31 - BÀI 16: CÁC CẤU TRÚC ĐIỀU KHIỂN
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và hiểu được ý nghĩa của 3 cấu trúc điều khiển cơ bản trong thuật toán:
  + Cấu trúc tuần tự: Các thao tác được thực hiện lần lượt theo đúng thứ tự xuất hiện.
  + Cấu trúc rẽ nhánh (dạng thiếu: Nếu...thì; dạng đủ: Nếu...thì...nếu không thì): Thao tác được thực hiện tùy thuộc vào điều kiện đúng hay sai.
  + Cấu trúc lặp (lặp với số lần biết trước và lặp với số lần chưa biết trước): Một hoặc một nhóm thao tác được lặp đi lặp lại nhiều lần.
- Vẽ được sơ đồ khối thể hiện 3 cấu trúc điều khiển trên cho các tình huống thực tế.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự quan sát các hoạt động hàng ngày và phân loại chúng vào các cấu trúc tuần tự, rẽ nhánh hoặc lặp.
- Giải quyết vấn đề và sáng tạo: Lựa chọn cấu trúc điều khiển phù hợp để giải quyết tối ưu bài toán.

b) Năng lực đặc thù môn Tin học:
- Năng lực giải quyết vấn đề với sự trợ giúp của CNTT (NLd): Phát triển tư duy logic có điều kiện và tư duy vòng lặp trong thiết kế giải thuật.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 5.1.TC1a: Hiểu cơ chế ra quyết định của máy tính thông qua cấu trúc điều kiện rẽ nhánh và vòng lặp.***

## 3. Về phẩm chất
- Kiên trì, cẩn trọng, tỉ mỉ khi phân tích các trường hợp điều kiện đúng/sai.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng điện tử PowerPoint trình chiếu các sơ đồ khối động, phiếu học tập nhóm.
2. Học sinh: SGK Tin học 6, vở ghi chép, thước kẻ, bút màu.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Nhận biết cấu trúc rẽ nhánh qua quyết định hàng ngày.
b) Nội dung: Trả lời câu hỏi: "Nếu sáng mai trời mưa thì em mang theo áo mưa, nếu không mưa thì em đi xe đạp bình thường." Câu nói trên chứa từ khóa điều kiện nào?
c) Sản phẩm: Câu trả lời: "Nếu...thì...nếu không thì...".
d) Tổ chức thực hiện: GV dẫn dắt vào bài mới: Cấu trúc rẽ nhánh và các cấu trúc điều khiển.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (50 phút)
### Hoạt động 2.1: Cấu trúc tuần tự và cấu trúc rẽ nhánh (25 phút)
a) Mục tiêu: Nắm vững khái niệm, biểu diễn bằng sơ đồ khối của cấu trúc tuần tự và cấu trúc rẽ nhánh (dạng thiếu, dạng đủ).
b) Nội dung: Khảo sát mục 1, 2 SGK trang 67 - 69; làm bài tập nhận biết.
c) Sản phẩm: Bản vẽ sơ đồ khối cấu trúc tuần tự và rẽ nhánh trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Phân tích cấu trúc tuần tự: Thao tác 1 $\rightarrow$ Thao tác 2 $\rightarrow$ Thao tác 3.<br>- **GV:** Phân tích cấu trúc rẽ nhánh:<br>+ Dạng thiếu: `Nếu <Điều kiện> đúng thì thực hiện <Lệnh>`.<br>+ Dạng đủ: `Nếu <Điều kiện> đúng thì thực hiện <Lệnh 1>, ngược lại thì thực hiện <Lệnh 2>`.<br>- **HS:** Quan sát khối hình thoi kiểm tra điều kiện.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận ví dụ: Kiểm tra điểm số để phân loại: Nếu điểm $\ge 5$ thì "Đạt", ngược lại thì "Chưa đạt".<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ sơ đồ khối rẽ nhánh dạng đủ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu: Khối hình thoi luôn có 2 nhánh đi ra: Nhánh Đúng (`True`) và Nhánh Sai (`False`). | **1. Cấu trúc tuần tự:**<br>- Các bước của thuật toán được thực hiện lần lượt từ trên xuống dưới theo thứ tự đã định.<br><br>**2. Cấu trúc rẽ nhánh:**<br>- Được dùng khi muốn thực hiện các thao tác khác nhau tùy thuộc vào một điều kiện cụ thể.<br>- **Dạng thiếu:** Nếu điều kiện đúng thì thực hiện công việc; nếu sai thì bỏ qua.<br>- **Dạng đủ:** Nếu điều kiện đúng thì làm công việc 1; nếu sai thì làm công việc 2. |

### Hoạt động 2.2: Cấu trúc lặp (25 phút)
a) Mục tiêu: Nắm vững khái niệm vòng lặp và cách biểu diễn bằng mũi tên quay ngược trong sơ đồ khối.
b) Nội dung: Đọc mục 3 SGK trang 69 - 70; làm Luyện tập 2.
c) Sản phẩm: Sơ đồ khối vòng lặp rửa bát hoặc vòng lặp đếm số từ 1 đến 10.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt câu hỏi: Kể tên các hành động lặp lại nhiều lần trong đời sống? (Kim đồng hồ chạy, đánh răng mỗi sáng, rửa từng chiếc bát cho đến khi hết bát bẩn).<br>- **GV:** Nêu định nghĩa cấu trúc lặp và hướng dẫn cách vẽ mũi tên quay ngược về trước điều kiện.<br>- **HS:** Làm việc theo cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Phân tích bài toán tính tổng $S = 1 + 2 + 3 + ... + 10$: Lặp lại thao tác cộng dồn 10 lần.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS lên bảng vẽ sơ đồ khối cấu trúc lặp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Cấu trúc lặp giúp giảm thiểu số lượng câu lệnh, tránh phải viết đi viết lại nhiều lần một thao tác. | **3. Cấu trúc lặp:**<br>- Được dùng để thực hiện lặp đi lặp lại một hoặc nhiều thao tác cho đến khi thỏa mãn một điều kiện dừng nào đó.<br>- Có hai loại lặp phổ biến:<br>+ **Lặp với số lần biết trước:** Ví dụ lặp đúng 10 lần.<br>+ **Lặp với số lần chưa biết trước:** Lặp cho đến khi hết dữ liệu hoặc khi điều kiện không còn thỏa mãn. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Phân biệt chính xác 3 cấu trúc điều khiển trong các bài toán thực tế.
b) Nội dung: Giải bài tập Luyện tập 1, 2 SGK trang 70.
c) Sản phẩm: Đáp án phân loại đúng trong vở học sinh.
d) Tổ chức thực hiện: Học sinh làm bài độc lập, thảo luận và chữa bài trên bảng.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)
- **Tích hợp NLS 5.1.TC1a:** GV yêu cầu học sinh mô tả thuật toán của trò chơi "Oẳn tù tì" hoặc "Đèn giao thông ngã tư" bằng cấu trúc rẽ nhánh dạng đủ. Dặn dò chuẩn bị cho Bài 17: Chương trình máy tính.
"""

# 10. Bài 17: Chương trình máy tính (Tiết 32, 33)
md_10 = """Tiết 32, 33 - BÀI 17: CHƯƠNG TRÌNH MÁY TÍNH
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được chương trình máy tính là gì: Chương trình máy tính là một dãy các lệnh được viết bằng một ngôn ngữ lập trình cụ thể để hướng dẫn máy tính thực hiện thuật toán.
- Làm quen với môi trường lập trình trực quan (như Scratch): Nhận biết khu vực sân khấu (`Stage`), khu vực nhân vật (`Sprites`), bảng các khối lệnh (`Blocks Palette`) và khu vực ghép mã lệnh (`Scripts Area`).
- Biết cách kéo thả các khối lệnh cơ bản (chuyển động `Motion`, hiển thị `Looks`, âm thanh `Sound`, sự kiện `Events`, điều khiển `Control`) để điều khiển nhân vật di chuyển và phát ra âm thanh.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự khám phá các nhóm khối lệnh màu sắc trong Scratch để điều khiển nhân vật.
- Giải quyết vấn đề và sáng tạo: Lập trình tạo chuyển động của chú mèo Scratch bước đi và chào người xem.

b) Năng lực đặc thù môn Tin học:
- Năng lực giải quyết vấn đề với sự trợ giúp của CNTT (NLd): Bước đầu chuyển dịch từ ý tưởng thuật toán thành mã lệnh chương trình chạy được trên máy tính.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 5.1.TC1a: Làm quen với ngôn ngữ lập trình trực quan khối kéo thả (Blockly/Scratch), hiểu cách máy tính thực thi mã lệnh.***

## 3. Về phẩm chất
- Đam mê khám phá lập trình, kiên nhẫn thử nghiệm và sửa lỗi (`Debug`) chương trình.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, phần mềm Scratch cài sẵn trên máy (hoặc truy cập `scratch.mit.edu`), máy chiếu, các dự án mẫu Scratch sinh động.
2. Học sinh: SGK Tin học 6, vở ghi chép, máy tính thực hành Scratch.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Kích thích trí tò mò của học sinh về việc làm thế nào để điều khiển máy tính làm theo ý mình.
b) Nội dung: Trình chiếu một đoạn hoạt hình ngắn do GV lập trình bằng Scratch: Chú mèo vừa đi vừa nói "Xin chào các bạn lớp 6A!".
c) Sản phẩm: Sự hào hứng và thích thú muốn tự tay lập trình của học sinh.
d) Tổ chức thực hiện: GV dẫn dắt vào bài học mới: Chương trình máy tính.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (50 phút)
### Hoạt động 2.1: Chương trình máy tính và ngôn ngữ lập trình (20 phút)
a) Mục tiêu: Nắm vững định nghĩa chương trình máy tính và vai trò của ngôn ngữ lập trình.
b) Nội dung: Đọc mục 1 SGK trang 71 - 72; thảo luận tại sao máy tính cần ngôn ngữ lập trình để hiểu thuật toán.
c) Sản phẩm: Bản ghi nhớ khái niệm trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giải thích: Con người nghĩ ra thuật toán bằng tiếng Việt, nhưng máy tính chỉ hiểu dãy số nhị phân `0` và `1`. Làm sao để máy tính hiểu được thuật toán của con người?<br>- **GV:** Giới thiệu ngôn ngữ lập trình là cầu nối phiên dịch.<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nêu tên một số ngôn ngữ lập trình đã từng nghe thấy (Scratch, Python, C++, Pascal).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu: Chương trình máy tính là tập hợp các lệnh điều khiển máy tính.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại: Lập trình là quá trình tạo ra chương trình máy tính. | **1. Chương trình máy tính:**<br>- Chương trình máy tính là một tập hợp các câu lệnh được viết bằng ngôn ngữ lập trình, hướng dẫn máy tính thực hiện các thao tác của một thuật toán.<br>- **Ngôn ngữ lập trình:** Là ngôn ngữ dùng để viết chương trình máy tính.<br>- **Ngôn ngữ lập trình trực quan:** Sử dụng các khối lệnh có sẵn nhiều màu sắc, người lập trình chỉ cần kéo và ghép chúng lại với nhau (như trò chơi xếp hình Lego) mà không sợ sai cú pháp chữ. |

### Hoạt động 2.2: Làm quen môi trường lập trình trực quan Scratch (30 phút)
a) Mục tiêu: Nắm được 4 khu vực chính của Scratch và ghép được đoạn mã lệnh đơn giản đầu tiên.
b) Nội dung: Khảo sát mục 2 SGK trang 72 - 74; thực hành khởi động Scratch và kéo thả lệnh.
c) Sản phẩm: Nhân vật chú mèo di chuyển 10 bước và kêu "Meo meo".
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu 4 khu vực trên màn hình Scratch:<br>1. Khu vực khối lệnh (`Blocks Palette`): Chứa các nhóm lệnh chuyển động (xanh lam), hiển thị (tím), sự kiện (vàng), điều khiển (cam).<br>2. Khu vực ghép lệnh (`Scripts Area`): Nơi kéo thả và lắp ghép các khối lệnh.<br>3. Sân khấu (`Stage`): Nơi nhân vật hoạt động biểu diễn kết quả.<br>4. Quản lí nhân vật (`Sprites Area`).<br>- **HS:** Quan sát và thực hành trên máy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Kéo khối lệnh `when green flag clicked` (khi bấm vào cờ xanh) từ nhóm `Events`.<br>- **HS:** Ghép tiếp khối `move 10 steps` (di chuyển 10 bước) và `say "Hello!" for 2 seconds`.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS bấm vào biểu tượng Lá cờ xanh: Chú mèo lập tức bước đi và hiện bóng thoại chào.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Hướng dẫn thêm khối lệnh lặp `repeat 10` để chú mèo bước đi liên tục. | **2. Làm quen với Scratch:**<br>- **Quy trình lập trình một hoạt động:**<br>+ Bước 1: Chọn nhân vật (`Sprite`).<br>+ Bước 2: Chọn khối lệnh kích hoạt trong nhóm `Events` (ví dụ: `when flag clicked`).<br>+ Bước 3: Kéo các khối lệnh hành động từ bảng khối lệnh sang khu vực lập trình và ghép nối chúng khít vào nhau.<br>+ Bước 4: Bấm vào Lá cờ xanh để chạy thử chương trình, quan sát nhân vật trên sân khấu và tinh chỉnh lệnh nếu chưa đúng ý. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Tự tạo một dự án Scratch hoàn chỉnh: Nhân vật đi bộ và đổi hướng khi chạm cạnh sân khấu.
b) Nội dung: Thực hành ghép các khối lệnh: `when flag clicked` $\rightarrow$ `forever` $\rightarrow$ `move 10 steps` $\rightarrow$ `if on edge, bounce` $\rightarrow$ `next costume`.
c) Sản phẩm: Chương trình Scratch chuyển động mượt mà lưu với tên `MeoDiBo.sb3`.
d) Tổ chức thực hiện: Học sinh thực hành độc lập, GV hỗ trợ cá nhân.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)
- **Tích hợp NLS 5.1.TC1a:** GV khuyến khích học sinh đổi nhân vật chú mèo thành con vật hoặc nhân vật hoạt hình khác, thêm âm thanh và phông nền sân khấu theo sở thích. Dặn dò ôn tập toàn bộ kiến thức để chuẩn bị cho tiết Ôn tập cuối học kì II.
"""

# 11. Ôn tập cuối học kì II (Tiết 34)
md_11 = """Tiết 34 - ÔN TẬP CUỐI HỌC KÌ II
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ kiến thức Tin học Học kì II lớp 6:
  + Chủ đề 4: An toàn thông tin trên Internet.
  + Chủ đề 5: Ứng dụng tin học (Sơ đồ tư duy, Định dạng văn bản, Trình bày bảng biểu, Tìm kiếm và thay thế).
  + Chủ đề 6: Thuật toán và Chương trình máy tính (Khái niệm thuật toán, 3 cấu trúc điều khiển, Môi trường lập trình trực quan Scratch).
- Rèn luyện kỹ năng tổng hợp kiến thức bằng sơ đồ tư duy, tư duy thuật toán và kỹ năng thực hành máy tính chuẩn bị cho kì kiểm tra cuối học kì II.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự hệ thống hóa toàn bộ sơ đồ kiến thức HKII và giải đề cương ôn tập.
- Giao tiếp và hợp tác: Tự tin trao đổi các bước thuật toán và kỹ năng lập trình với bạn cùng nhóm.

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng dụng CNTT (NLc) & Năng lực giải quyết vấn đề (NLd): Vận dụng tổng hợp soạn thảo văn bản và tư duy lập trình để giải quyết các nhiệm vụ học tập.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Tự thiết kế và khai thác sơ đồ tư duy số để ôn thi học kì hiệu quả.***
- ***NLS 5.1.TC1a: Khái quát hóa tư duy thuật toán và logic điều khiển trong lập trình máy tính.***

## 3. Về phẩm chất
- Nghiêm túc, tự giác, cẩn trọng trong từng thao tác máy tính và có ý thức rèn luyện môn học.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Ôn tập tổng kết Học kì II môn Tin học 6, hệ thống câu hỏi trắc nghiệm và bài tập thực hành tổng hợp.
2. Học sinh: SGK Tin học 6, vở ghi, đề cương ôn tập cuối HKII, máy tính thực hành.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (4 phút)
a) Mục tiêu: Điểm lại cấu trúc đề kiểm tra đánh giá cuối học kì II môn Tin học 6 (Trắc nghiệm 4 điểm, Thực hành 6 điểm).
b) Nội dung: Quán triệt mục tiêu ôn tập, tạo động lực đạt điểm cao cho học sinh.
c) Sản phẩm: Tâm thế tích cực, sẵn sàng ôn tập của học sinh.
d) Tổ chức thực hiện: GV dẫn dắt vào bài ôn tập.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (33 phút)
### Hoạt động 2.1: Hệ thống hóa toàn bộ kiến thức HKII qua Sơ đồ tư duy (10 phút)
a) Mục tiêu: Xâu chuỗi 3 chủ đề kiến thức lớn của Học kì II một cách logic, toàn diện và trực quan.
b) Nội dung: Trình chiếu và phân tích Sơ đồ tư duy Tổng kết Học kì II môn Tin học 6.
c) Sản phẩm: Sơ đồ tư duy được khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Tổng kết Học kì II Tin học 6.<br>- **GV:** Yêu cầu HS nêu 4 nhánh chính: 1. An toàn thông tin; 2. Soạn thảo văn bản & Bảng biểu; 3. Thuật toán; 4. Cấu trúc điều khiển & Chương trình máy tính.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại các quy tắc an toàn mạng và các hình khối trong sơ đồ khối.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy thuyết minh toàn bộ 4 nhánh của sơ đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu: Thuật toán là nền móng, chương trình máy tính là sự thể hiện thuật toán bằng ngôn ngữ lập trình. | **SƠ ĐỒ TƯ DUY TỔNG KẾT HỌC KÌ II: TIN HỌC 6**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Ôn tập cuối học kì II Tin học 6](khbd-ill:mindmap-tin6-tiet34-cuoihk2)

### Hoạt động 2.2: Rèn luyện giải câu hỏi trắc nghiệm và bài tập thực hành (23 phút)
a) Mục tiêu: Thành thạo các câu hỏi trắc nghiệm lí thuyết và hoàn thiện kỹ năng thực hành Word, Scratch.
b) Nội dung: Giải 8 câu hỏi trắc nghiệm trọng tâm và thực hành ghép một kịch bản Scratch đơn giản.
c) Sản phẩm: Phiếu trả lời trắc nghiệm và tệp dự án Scratch của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Cho HS làm nhanh các câu trắc nghiệm trên màn chiếu:<br>1. Phím tắt căn giữa đoạn văn bản là gì? (`Ctrl + E`).<br>2. Khối hình thoi trong sơ đồ khối có ý nghĩa gì? (Kiểm tra điều kiện).<br>3. Để tìm kiếm và thay thế tự động, ta dùng tổ hợp phím nào? (`Ctrl + H`).<br>4. Trong Scratch, khối lệnh `move 10 steps` thuộc nhóm nào? (`Motion`).<br>- **HS:** Giơ bảng trả lời.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **GV:** Giao bài thực hành máy tính: Mở Word, tạo bảng thời khóa biểu 3 cột 4 hàng, chèn hình ảnh và định dạng đẹp mắt.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS hoàn thành và lưu tệp bài làm.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt đáp án trắc nghiệm chuẩn và uốn nắn các lỗi thực hành còn vướng. | **Nội dung ôn luyện trọng tâm:**<br>- **Lí thuyết:**<br>+ Phân biệt mật khẩu mạnh/yếu.<br>+ 4 quy tắc định dạng ký tự, đoạn, trang văn bản.<br>+ 3 đặc trưng của thuật toán (xác định, hữu hạn, đúng đắn).<br>+ 3 cấu trúc điều khiển: tuần tự, rẽ nhánh, lặp.<br>- **Thực hành:**<br>+ Định dạng văn bản nhanh bằng phím tắt.<br>+ Tạo và căn chỉnh bảng biểu chuẩn mực.<br>+ Kéo ghép khối lệnh Scratch tạo chuyển động nhân vật. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
- **Tích hợp NLS 3.1.TC2a & 5.1.TC1a:** GV nhắc nhở học sinh về nhà xem lại Sơ đồ tư duy tổng kết, tự kiểm tra lại các kỹ năng thực hành trên máy tính gia đình để tự tin bước vào kì thi cuối học kì II. Dặn dò chuẩn bị chu đáo cho tiết Kiểm tra cuối kì II tuần tới.
"""

# 12. Kiểm tra cuối kỳ II (Tiết 35)
md_12 = """Tiết 35 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ II
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện kết quả học tập môn Tin học lớp 6 của học sinh trong cả Học kì II theo ma trận và bản đặc tả đề kiểm tra cuối HKI/HKII đã được Ban giám hiệu phê duyệt.
- Đánh giá năng lực thực hành tin học: Khả năng sử dụng phần mềm soạn thảo văn bản Word, phần mềm sơ đồ tư duy và phần mềm lập trình trực quan Scratch để giải quyết một nhiệm vụ số hoàn chỉnh.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác, nghiêm túc, độc lập hoàn thành bài kiểm tra theo đúng quy chế thi.

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng dụng CNTT (NLc) & Năng lực giải quyết vấn đề (NLd): Thao tác thành thạo máy tính, quản lí tệp bài làm khoa học, lập trình và định dạng chính xác.

## 3. Về phẩm chất
- Trung thực, nghiêm túc, có ý thức kỷ luật cao trong phòng máy tính.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Đề kiểm tra in sẵn kết hợp Trắc nghiệm (4 điểm) và Thực hành trên máy (6 điểm), đáp án và thang điểm chi tiết; Phòng máy tính hoạt động ổn định.
2. Học sinh: Bút viết, máy vi tính cá nhân (đã ngắt kết nối mạng Internet tự do).

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: ỔN ĐỊNH LỚP VÀ PHÁT ĐỀ (3 phút)
- GV kiểm tra sĩ số, phổ biến nội quy phòng thi nghiêm ngặt, yêu cầu học sinh cất toàn bộ tài liệu vào ngăn bàn.
- GV phát đề kiểm tra đến từng học sinh và hướng dẫn lưu bài vào thư mục: `D:\\THI_CUOI_HK2\\HoTen_Lop6A.docx`.

## B. HOẠT ĐỘNG 2: HỌC SINH LÀM BÀI KIỂM TRA (40 phút)
- **Phần 1: Trắc nghiệm khách quan (15 phút - 4 điểm):** Gồm 8 câu hỏi bao quát toàn bộ kiến thức An toàn thông tin, Ứng dụng tin học, Thuật toán và Lập trình Scratch.
- **Phần 2: Thực hành trên máy tính (25 phút - 6 điểm):**
  + Câu 1 (4 điểm - Soạn thảo Word): Soạn một thông báo ngắn, áp dụng định dạng ký tự, đoạn văn bản, chèn 01 bảng thống kê 3 cột và 01 hình ảnh minh họa theo mẫu.
  + Câu 2 (2 điểm - Lập trình Scratch): Tạo một đoạn mã lệnh điều khiển nhân vật chú mèo bước đi 20 bước, đổi trang phục và phát ra tiếng kêu khi bấm phím khoảng trắng (`Space`).
- Giáo viên bao quát phòng máy, giám sát tính độc lập của học sinh, không giải thích gì thêm về đề thi.

## C. HOẠT ĐỘNG 3: THU BÀI VÀ TỔNG KẾT NĂM HỌC (2 phút)
- GV cho học sinh dừng thao tác, thu bài trắc nghiệm giấy và thu toàn bộ tệp thực hành qua mạng LAN nội bộ hoặc kiểm tra trên ổ đĩa máy tính.
- GV nhận xét tinh thần làm bài nghiêm túc của học sinh, chúc mừng các em đã hoàn thành xuất sắc chương trình Tin học lớp 6 năm học 2026 - 2027.
"""

tasks = [
    ("07_KHBD_Tin6_KiemTraGiuaHK2_Tiet28.md", md_07),
    ("08_KHBD_Tin6_Bai15_ThuatToan_Tiet29.md", md_08),
    ("09_KHBD_Tin6_Bai16_CacCauTrucDieuKhien_Tiet30-31.md", md_09),
    ("10_KHBD_Tin6_Bai17_ChuongTrinhMayTinh_Tiet32-33.md", md_10),
    ("11_KHBD_Tin6_OnTapCuoiHK2_Tiet34.md", md_11),
    ("12_KHBD_Tin6_KiemTraCuoiHK2_Tiet35.md", md_12),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
