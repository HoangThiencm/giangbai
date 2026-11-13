# -*- coding: utf-8 -*-
"""
Script sinh 6 tệp KHBD Markdown môn Tin học 6 (Tuần 19 - 27):
- 01_KHBD_Tin6_Bai09_AnToanThongTinTrenInternet_Tiet19.md
- 02_KHBD_Tin6_Bai10_SoDoTuDuy_Tiet20-21.md
- 03_KHBD_Tin6_Bai11_DinhDangVanBan_Tiet22-23.md
- 04_KHBD_Tin6_Bai12_TrinhBayThongTinDangBang_Tiet24-25.md
- 05_KHBD_Tin6_Bai13_ThucHanh_TimKiemVaThayThe_Tiet26.md
- 06_KHBD_Tin6_Bai14_ThucHanhTongHop_HoanThienSoLuuNiem_Tiet27.md (Mindmap: mindmap_tin6_tiet27_giuahk2.png)
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "C:/Users/HoangThien/Documents/GitHub/giangbai/TROLYTHIEN/TEMP/HK2_Tin6"
os.makedirs(OUT_DIR, exist_ok=True)

# 01. Bài 9: An toàn thông tin trên Internet (Tiết 19)
md_01 = """Tiết 19 - BÀI 9: AN TOÀN THÔNG TIN TRÊN INTERNET
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết được tầm quan trọng của sự an toàn và bảo mật thông tin cá nhân khi tham gia môi trường Internet.
- Nêu được những tác hại, nguy cơ tiềm ẩn khi sử dụng Internet: bị đánh cắp thông tin cá nhân, bị lừa đảo, máy tính nhiễm virus/mã độc, bị bắt nạt trên mạng.
- Biết và thực hiện được các biện pháp cơ bản để bảo vệ thông tin cá nhân và thiết bị khi truy cập Internet (đặt mật khẩu mạnh, không cung cấp thông tin cho người lạ, không truy cập đường link độc hại).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác hình thành thói quen kiểm tra tính an toàn trước khi bấm vào các liên kết lạ hoặc tải tệp về máy tính.
- Giao tiếp và hợp tác: Tự tin thảo luận trong nhóm về các tình huống lừa đảo phổ biến trên không gian mạng.

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng xử phù hợp trong môi trường số (NLa): Biết bảo vệ bí mật đời tư số của bản thân và tôn trọng quyền riêng tư của người khác.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 4.1.TC1a: Nhận diện các mối nguy hại trực tuyến và biết cách bảo vệ thông tin đăng nhập, thiết bị cá nhân.***

## 3. Về phẩm chất
- Trách nhiệm: Tuân thủ các quy tắc văn hóa ứng xử trên mạng xã hội, có trách nhiệm bảo vệ thông tin của bạn bè và người thân.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng điện tử PowerPoint trình chiếu các tình huống thực tế về lừa đảo qua mạng, video phóng sự ngắn về an toàn thông tin.
2. Học sinh: SGK Tin học 6, vở ghi chép, máy tính có kết nối Internet an toàn.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Kích hoạt nhận thức của học sinh về các nguy cơ tiềm ẩn khi dùng Internet.
b) Nội dung: Trả lời câu hỏi: Em hoặc người thân đã bao giờ nhận được tin nhắn trúng thưởng lạ hoặc yêu cầu chuyển tiền từ người không quen biết chưa? Khi đó em xử lí như thế nào?
c) Sản phẩm: Câu trả lời chia sẻ trải nghiệm thực tế của học sinh.
d) Tổ chức thực hiện: GV nêu tình huống gợi mở, học sinh phát biểu sôi nổi, GV dẫn dắt vào bài học mới.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (25 phút)
### Hoạt động 2.1: Tác hại và nguy cơ khi dùng Internet (12 phút)
a) Mục tiêu: Nêu được 4 nhóm nguy cơ chính trên Internet: Thông tin không lành mạnh, Bị đánh cắp thông tin, Bị lừa đảo và Bắt nạt qua mạng.
b) Nội dung: Đọc mục 1 SGK trang 37 - 38; thảo luận các tình huống minh họa.
c) Sản phẩm: Bảng phân loại các nguy cơ khi tham gia môi trường mạng.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chia lớp thành 4 nhóm, mỗi nhóm thảo luận một tình huống trong SGK:<br>Nhóm 1: Nhận tin nhắn thông báo trúng xe máy SH.<br>Nhóm 2: Nhận lời mời kết bạn từ người lạ hỏi địa chỉ nhà, trường học.<br>Nhóm 3: Tải phần mềm trò chơi miễn phí từ trang web không rõ nguồn gốc.<br>Nhóm 4: Bị ai đó lấy ảnh chế giễu trên mạng xã hội.<br>- **HS:** Thảo luận trong 5 phút.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Xác định nguy cơ tiềm ẩn tương ứng với từng tình huống.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện từng nhóm trình bày nguy cơ: Lừa đảo tiền bạc; Lộ bí mật cá nhân; Máy tính nhiễm virus; Bị tổn thương tinh thần.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Tổng kết 4 nguy cơ chính khi sử dụng Internet. | **1. Một số nguy cơ khi sử dụng Internet:**<br>- **Thông tin không chính xác hoặc độc hại:** Tin giả, nội dung bạo lực, phản cảm.<br>- **Bị đánh cắp thông tin cá nhân:** Họ tên, ngày sinh, số điện thoại, mật khẩu tài khoản.<br>- **Bị lừa đảo:** Mạo danh người thân mượn tiền, trúng thưởng ảo.<br>- **Máy tính bị nhiễm mã độc/virus:** Làm hỏng hệ điều hành, mất dữ liệu.<br>- **Bị bắt nạt trên mạng:** Nói xấu, chế giễu, đe dọa trực tuyến. |

### Hoạt động 2.2: Quy tắc bảo vệ an toàn thông tin cá nhân (13 phút)
a) Mục tiêu: Nắm vững các quy tắc an toàn: Đặt mật khẩu mạnh, Bảo vệ thông tin cá nhân, Cẩn trọng khi chia sẻ.
b) Nội dung: Đọc mục 2 SGK trang 39 - 40; thực hành nhận diện mật khẩu mạnh/yếu.
c) Sản phẩm: Bộ quy tắc 5 không khi tham gia Internet.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt câu hỏi: Thế nào là một mật khẩu mạnh? Cho ví dụ?<br>- **GV:** Hướng dẫn quy tắc "5 Không": Không chia sẻ thông tin cá nhân; Không mở link lạ; Không kết bạn người lạ; Không tin tin trúng thưởng; Không chia sẻ mật khẩu.<br>- **HS:** Làm việc cá nhân.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** So sánh hai mật khẩu: `123456` và `H@oToanTin#2026`.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu: Mật khẩu thứ hai mạnh hơn vì có chữ hoa, chữ thường, số và ký tự đặc biệt, độ dài trên 8 ký tự.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn mạnh: Đổi mật khẩu định kỳ 3 - 6 tháng/lần. | **2. Quy tắc an toàn thông tin cá nhân:**<br>- **Đặt mật khẩu mạnh:** Dài ít nhất 8 ký tự, bao gồm cả chữ hoa, chữ thường, chữ số và ký tự đặc biệt (`@, #, $, %`).<br>- **Bảo vệ dữ liệu cá nhân:** Không tùy tiện cung cấp địa chỉ, số CCCD, hình ảnh riêng tư cho người lạ.<br>- **Cẩn trọng với tệp đính kèm và liên kết:** Không nhấp vào đường link lạ trong email, tin nhắn.<br>- **Cài đặt phần mềm diệt virus** và thường xuyên cập nhật hệ điều hành. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
a) Mục tiêu: Củng cố kỹ năng phân biệt hành vi đúng/sai khi dùng mạng.
b) Nội dung: Trả lời các câu hỏi tình huống trong mục Luyện tập SGK trang 41.
c) Sản phẩm: Phiếu bài làm chọn phương án xử lí đúng của học sinh.
d) Tổ chức thực hiện:
- GV chiếu 3 câu hỏi trắc nghiệm tình huống. HS giơ thẻ đáp án và giải thích lý do lựa chọn hành vi an toàn.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
- **Tích hợp NLS 4.1.TC1a:** GV giao bài tập về nhà: Em hãy tự kiểm tra lại mật khẩu các tài khoản trực tuyến của mình (email trường, tài khoản học trực tuyến) xem đã đủ độ mạnh chưa và tiến hành cập nhật nếu cần thiết. Dặn dò chuẩn bị cho Bài 10: Sơ đồ tư duy.
"""

# 02. Bài 10: Sơ đồ tư duy (Tiết 20, 21)
md_02 = """Tiết 20, 21 - BÀI 10: SƠ ĐỒ TƯ DUY
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được sơ đồ tư duy là gì và ý nghĩa của việc sử dụng sơ đồ tư duy trong học tập và đời sống.
- Nhận biết được các thành phần chính của một sơ đồ tư duy: Chủ đề chính, các nhánh chủ đề phụ, từ khóa ngắn gọn, màu sắc và hình ảnh minh họa.
- Biết các bước cơ bản để tạo sơ đồ tư duy (bằng cách vẽ tay hoặc sử dụng phần mềm trên máy tính).
- Sử dụng được phần mềm vẽ sơ đồ tư duy đơn giản để tóm tắt một bài học hoặc lập kế hoạch hoạt động nhóm.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự đọc hiểu thông tin và trích xuất các từ khóa trọng tâm để đưa vào nhánh sơ đồ.
- Giao tiếp và hợp tác: Hợp tác nhóm phác thảo sơ đồ tư duy cho một dự án học tập nhỏ.

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng dụng công nghệ thông tin và truyền thông (NLc): Sử dụng thành thạo phần mềm sơ đồ tư duy để tổ chức và biểu diễn tri thức trực quan.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Sử dụng phần mềm sơ đồ tư duy số (XMind, Mindomo hoặc GitMind) để thiết kế sơ đồ học tập tương tác.***

## 3. Về phẩm chất
- Sáng tạo, thẩm mĩ, có ý thức tổ chức công việc khoa học, ngăn nắp.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, phòng máy vi tính cài sẵn phần mềm vẽ sơ đồ tư duy, máy chiếu, một số mẫu sơ đồ tư duy đẹp mắt.
2. Học sinh: SGK Tin học 6, vở ghi, giấy A4, bút màu (để vẽ tay) và máy tính thực hành.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: So sánh cách ghi chép truyền thống toàn chữ và cách ghi chép bằng sơ đồ tư duy có màu sắc, hình ảnh.
b) Nội dung: Quan sát hai trang vở cùng ghi chép nội dung bài học Lịch sử: Một trang kín đặc chữ và một trang vẽ sơ đồ tư duy nhiều màu sắc. Trang nào giúp em ghi nhớ nhanh và hứng thú hơn?
c) Sản phẩm: Đa số học sinh chọn trang vẽ sơ đồ tư duy.
d) Tổ chức thực hiện: GV chiếu hai hình ảnh, học sinh so sánh và GV giới thiệu khái niệm Sơ đồ tư duy.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (50 phút)
### Hoạt động 2.1: Sơ đồ tư duy là gì và các thành phần chính (25 phút)
a) Mục tiêu: Nắm vững định nghĩa và 4 thành phần cơ bản của sơ đồ tư duy.
b) Nội dung: Đọc mục 1 SGK trang 42 - 44; chỉ ra các thành phần trên sơ đồ mẫu.
c) Sản phẩm: Ghi chép khái niệm và nhận diện chính xác các nhánh trên sơ đồ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu cha đẻ sơ đồ tư duy: Tony Buzan.<br>- **GV:** Chiếu sơ đồ tư duy chủ đề "Kế hoạch dã ngoại của lớp" và hỏi: Trung tâm là gì? Các nhánh chính tỏa ra gồm những nội dung gì?<br>- **HS:** Quan sát và phân tích.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chỉ ra: Trung tâm là Kế hoạch dã ngoại; Các nhánh: Địa điểm, Thời gian, Chuẩn bị, Hoạt động.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy nêu nhận xét về màu sắc và từ khóa ngắn gọn trên các nhánh.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại định nghĩa và các thành phần cốt lõi. | **1. Sơ đồ tư duy là gì?**<br>- Sơ đồ tư duy (Mindmap) là phương pháp trình bày thông tin một cách trực quan bằng cách sử dụng từ khóa, hình ảnh, đường nối và màu sắc.<br>- **Các thành phần chính:**<br>+ **Chủ đề chính:** Nằm ở vị trí trung tâm của sơ đồ.<br>+ **Các nhánh chính (cấp 1):** Tỏa ra từ chủ đề chính, đại diện cho các ý lớn.<br>+ **Các nhánh phụ (cấp 2, 3):** Tỏa ra từ nhánh chính, thể hiện các chi tiết cụ thể.<br>+ **Từ khóa, hình ảnh minh họa, màu sắc:** Giúp não bộ liên tưởng và ghi nhớ sâu sắc. |

### Hoạt động 2.2: Các bước tạo sơ đồ tư duy bằng phần mềm (25 phút)
a) Mục tiêu: Nắm vững quy trình 4 bước tạo sơ đồ tư duy trên phần mềm máy tính.
b) Nội dung: Đọc mục 2 SGK trang 45 - 46; làm quen giao diện phần mềm.
c) Sản phẩm: Thao tác tạo được nút trung tâm và thêm các nút nhánh con trên máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn 4 bước tạo sơ đồ tư duy:<br>Bước 1: Tạo chủ đề chính ở trung tâm.<br>Bước 2: Thêm các nhánh cấp 1 bằng phím `Tab` hoặc nút `Insert Subtopic`.<br>Bước 3: Thêm các nhánh cấp 2 bằng phím `Enter` hoặc `Tab`.<br>Bước 4: Thêm từ khóa, chèn icon/hình ảnh và đổi màu sắc cho sinh động.<br>- **HS:** Quan sát thao tác mẫu của GV trên máy chiếu.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Khởi động phần mềm trên máy tính cá nhân.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS thực hành gõ chủ đề trung tâm: "GIA ĐÌNH EM" và tạo 4 nhánh: Ông bà, Bố mẹ, Anh chị, Em.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đi vòng quanh hỗ trợ các học sinh còn lúng túng khi dùng phím tắt `Tab`, `Enter`. | **2. Các bước tạo sơ đồ tư duy trên phần mềm:**<br>- **Bước 1:** Viết chủ đề chính ở giữa trang.<br>- **Bước 2:** Vẽ các nhánh chính tỏa ra từ chủ đề trung tâm, viết từ khóa ngắn gọn.<br>- **Bước 3:** Phát triển các nhánh phụ từ mỗi nhánh chính để làm rõ ý.<br>- **Bước 4:** Trang trí bằng biểu tượng, hình vẽ, màu sắc khác biệt cho từng nhánh để dễ phân biệt. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Tự tạo một sơ đồ tư duy hoàn chỉnh tóm tắt nội dung Bài 9: An toàn thông tin trên Internet.
b) Nội dung: Thực hành trên máy tính trong 20 phút.
c) Sản phẩm: Tệp sơ đồ tư duy lưu trong thư mục bài làm của học sinh.
d) Tổ chức thực hiện:
- Học sinh làm bài thực hành độc lập. GV quan sát, đánh giá sản phẩm của 3 em nhanh và đẹp nhất, chiếu lên màn hình lớn để cả lớp nhận xét.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)
- **Tích hợp NLS 3.1.TC2a:** GV hướng dẫn học sinh xuất sơ đồ tư duy ra tệp ảnh định dạng `.png` hoặc `.pdf` để chia sẻ cho giáo viên và các bạn trong tổ qua email hoặc gửi lên Google Classroom. Dặn dò chuẩn bị cho Bài 11: Định dạng văn bản.
"""

# 03. Bài 11: Định dạng văn bản (Tiết 22, 23)
md_03 = """Tiết 22, 23 - BÀI 11: ĐỊNH DẠNG VĂN BẢN
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được mục đích của việc định dạng văn bản: Làm cho văn bản đẹp mắt, rõ ràng, dễ đọc, nhấn mạnh các nội dung quan trọng và tăng tính thuyết phục.
- Biết và thực hiện thành thạo các thao tác định dạng ký tự: Phông chữ (Font), Cỡ chữ (Size), Kiểu chữ (Đậm `Bold`, Nghiêng `Italic`, Gạch chân `Underline`), Màu chữ (Color).
- Biết và thực hiện được các thao tác định dạng đoạn văn bản: Căn lề (Trái, Phải, Giữa, Đều hai bên), Thụt đầu dòng, Giãn cách dòng và khoảng cách giữa các đoạn.
- Nắm vững các bước định dạng trang văn bản: Chọn hướng giấy (Dọc/Ngang), Chọn khổ giấy (A4), Căn lề trang (Trên, Dưới, Trái, Phải).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự khám phá các nút lệnh trên dải lệnh `Home` và `Layout` của phần mềm Word.
- Giải quyết vấn đề và sáng tạo: Thiết kế bố cục một bài thơ hoặc lời chúc mừng sinh nhật hài hòa, thẩm mĩ.

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng dụng CNTT (NLc): Sử dụng thành thạo phần mềm soạn thảo Word để định dạng văn bản chuẩn hành chính và văn bản trang trí.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Thành thạo các công cụ định dạng số, phím tắt (`Ctrl+B`, `Ctrl+I`, `Ctrl+E`, `Ctrl+J`) nâng cao tốc độ soạn thảo.***

## 3. Về phẩm chất
- Kiên nhẫn, cẩn thận, tôn trọng các quy tắc chuẩn mực khi soạn thảo văn bản tiếng Việt.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, bài giảng PowerPoint, tệp văn bản mẫu chưa định dạng và tệp văn bản đã định dạng đẹp chuẩn mực, phòng máy tính.
2. Học sinh: SGK Tin học 6, vở ghi, máy tính thực hành Word.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Cho học sinh thấy rõ sự khác biệt giữa văn bản thô chưa định dạng và văn bản đã được định dạng đẹp mắt.
b) Nội dung: Quan sát hai văn bản cùng một nội dung bài thơ "Hạt gạo làng ta": Một văn bản toàn chữ thẳng đơ một cỡ; Một văn bản tiêu đề to đậm giữa trang, tên tác giả nghiêng, lề thụt đều đặn. Em thích đọc bản nào hơn?
c) Sản phẩm: Học sinh nhận ra giá trị thẩm mĩ và sự cần thiết của định dạng văn bản.
d) Tổ chức thực hiện: GV dẫn dắt vào bài mới.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (50 phút)
### Hoạt động 2.1: Định dạng ký tự và định dạng đoạn văn bản (25 phút)
a) Mục tiêu: Thành thạo các nút lệnh trong nhóm `Font` và `Paragraph` trên dải lệnh `Home`.
b) Nội dung: Khảo sát mục 1, 2 SGK trang 48 - 50; thao tác mẫu trên máy.
c) Sản phẩm: Văn bản mẫu được định dạng chuẩn xác theo yêu cầu.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giới thiệu nhóm lệnh `Font`: Phông chữ (chọn Times New Roman hoặc Arial), Cỡ chữ (13 hoặc 14pt), Nút `B` (đậm), `I` (nghiêng), `U` (gạch chân).<br>- **GV:** Giới thiệu nhóm lệnh `Paragraph`: 4 nút căn lề (Align Left, Center, Align Right, Justify), khoảng cách dòng `Line Spacing`.<br>- **HS:** Thao tác trên tệp mẫu giáo viên gửi vào máy.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chọn (bôi đen) khối văn bản trước khi bấm nút lệnh.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS trình diễn các phím tắt nhanh: `Ctrl+B`, `Ctrl+I`, `Ctrl+E` (căn giữa), `Ctrl+J` (căn đều hai bên).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khắc sâu quy tắc vàng: "Chọn phần văn bản trước - Ra lệnh định dạng sau". | **1. Định dạng ký tự:**<br>- Chọn phần văn bản cần định dạng.<br>- Trong dải lệnh `Home`, nhóm `Font`:<br>+ Phông chữ (`Font`), Cỡ chữ (`Font Size`).<br>+ Kiểu chữ: **B** (Đậm), *I* (Nghiêng), <u>U</u> (Gạch chân).<br>+ Màu chữ (`Font Color`).<br><br>**2. Định dạng đoạn văn bản:**<br>- Trong dải lệnh `Home`, nhóm `Paragraph`:<br>+ Căn lề: Căn trái (`Ctrl+L`), Căn giữa (`Ctrl+E`), Căn phải (`Ctrl+R`), Căn đều hai bên (`Ctrl+J`).<br>+ Thụt đầu dòng đoạn văn (`First line indent`).<br>+ Khoảng cách dòng và đoạn: `Line and Paragraph Spacing`. |

### Hoạt động 2.2: Định dạng trang văn bản (25 phút)
a) Mục tiêu: Biết cách đặt hướng giấy, khổ giấy và căn lề trang in chuẩn.
b) Nội dung: Đọc mục 3 SGK trang 51; thực hành mở hộp thoại `Page Setup` trên dải lệnh `Layout`.
c) Sản phẩm: Trang văn bản được thiết lập khổ A4, hướng dọc, lề chuẩn $2\text{ cm}$.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn mở dải lệnh `Layout`:<br>+ `Orientation`: Chọn `Portrait` (hướng dọc) hoặc `Landscape` (hướng ngang).<br>+ `Size`: Chọn khổ giấy `A4`.<br>+ `Margins`: Chọn lề trang in (Top, Bottom, Left, Right).<br>- **HS:** Thao tác theo từng bước.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Chuyển văn bản từ hướng dọc sang hướng ngang và ngược lại để quan sát bố cục thay đổi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy giải thích: Khi nào nên chọn hướng ngang? (Khi văn bản có bảng biểu nhiều cột hoặc hình ảnh rộng).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa thao tác lưu văn bản sau khi định dạng (`Ctrl+S`). | **3. Định dạng trang văn bản:**<br>- Vào dải lệnh `Layout` (hoặc `Page Layout`):<br>+ **Hướng giấy (`Orientation`):** Hướng dọc (`Portrait`) hoặc hướng ngang (`Landscape`).<br>+ **Khổ giấy (`Size`):** Thường dùng khổ `A4` ($210 \times 297\text{ mm}$).<br>+ **Đặt lề trang (`Margins`):** Lề trên, lề dưới, lề trái, lề phải (theo quy chuẩn: Trên/Dưới $20\text{ mm}$, Trái $30\text{ mm}$, Phải $15\text{ mm}$). |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Thực hành định dạng hoàn chỉnh bài giới thiệu danh lam thắng cảnh quê hương.
b) Nội dung: Mở tệp văn bản thô do GV cung cấp, tiến hành định dạng tiêu đề, đoạn văn bản, chèn màu sắc và căn lề trang.
c) Sản phẩm: Tệp Word định dạng đẹp mắt của học sinh.
d) Tổ chức thực hiện: Học sinh làm việc cá nhân, giáo viên theo dõi và chấm điểm tại máy.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)
- **Tích hợp NLS 3.1.TC2a:** GV hướng dẫn học sinh xuất văn bản vừa định dạng sang định dạng PDF (`File` $\rightarrow$ `Export` $\rightarrow$ `Create PDF/XPS`) để đảm bảo không bị lỗi phông chữ khi gửi cho người khác xem trên điện thoại hoặc máy tính khác. Dặn dò chuẩn bị Bài 12: Trình bày thông tin ở dạng bảng.
"""

# 04. Bài 12: Trình bày thông tin ở dạng bảng (Tiết 24, 25)
md_04 = """Tiết 24, 25 - BÀI 12: TRÌNH BÀY THÔNG TIN Ở DẠNG BẢNG
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết được ưu điểm của việc trình bày thông tin ở dạng bảng: Cô đọng, mạch lạc, dễ tra cứu, thuận tiện cho việc so sánh và tổng hợp dữ liệu.
- Biết và thực hiện thành thạo các thao tác tạo bảng: Chọn số hàng và số cột bằng công cụ `Insert Table`.
- Biết thao tác hiệu chỉnh cấu trúc bảng: Chèn thêm hàng/cột, xóa hàng/cột, gộp nhiều ô thành một ô (`Merge Cells`), tách ô (`Split Cells`), thay đổi độ rộng của cột và chiều cao của hàng.
- Biết định dạng nội dung trong ô (căn lề giữa ô, màu nền, đường viền bảng).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự nghiên cứu và vận dụng các thao tác bảng biểu để lập Thời khóa biểu cá nhân.
- Giao tiếp và hợp tác: Hợp tác nhóm để thiết kế bảng phân công trực nhật hoặc bảng theo dõi thi đua tổ.

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng dụng CNTT (NLc): Sử dụng thành thạo công cụ Table trong phần mềm Word để giải quyết các nhu cầu trình bày dữ liệu trong học tập và sinh hoạt.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Thiết kế bảng số liệu khoa học, sử dụng các mẫu bảng biểu có sẵn (Table Styles) trong Word để nâng cao tính trực quan.***

## 3. Về phẩm chất
- Tỉ mỉ, cẩn thận, có tư duy logic trong việc tổ chức và sắp xếp thông tin.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, máy chiếu, các mẫu Thời khóa biểu, bảng điểm lớp, phòng máy tính.
2. Học sinh: SGK Tin học 6, vở ghi, máy tính thực hành.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Thấy được sự tiện lợi vượt trội của bảng biểu so với việc viết đoạn văn xuôi khi liệt kê danh sách.
b) Nội dung: So sánh hai cách trình bày Thời khóa biểu của một tuần: Cách 1 viết thành đoạn văn dài 10 dòng; Cách 2 kẻ thành bảng 6 cột và 5 hàng. Cách nào giúp em tìm môn học nhanh hơn?
c) Sản phẩm: 100% học sinh chọn bảng biểu vì dễ tra cứu tức thời.
d) Tổ chức thực hiện: GV giới thiệu lợi ích của bảng và vào bài học.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC (50 phút)
### Hoạt động 2.1: Cách tạo bảng và nhập dữ liệu (20 phút)
a) Mục tiêu: Tạo được bảng với số hàng và số cột tùy ý bằng dải lệnh `Insert`.
b) Nội dung: Đọc mục 1 SGK trang 53 - 54; thực hành tạo bảng 4 cột, 5 hàng.
c) Sản phẩm: Bảng trống được tạo trên màn hình Word và điền thông tin tiêu đề cột.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cách tạo bảng:<br>Vào dải lệnh `Insert` $\rightarrow$ chọn `Table` $\rightarrow$ kéo chuột chọn số cột và số hàng (hoặc chọn `Insert Table` và gõ số cột `Number of columns`, số hàng `Number of rows`).<br>- **GV:** Hướng dẫn cách di chuyển giữa các ô bằng phím mũi tên hoặc phím `Tab`.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tạo bảng danh sách tổ gồm các cột: STT, Họ và tên, Ngày sinh, Nhiệm vụ.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS gõ thông tin 3 bạn trong tổ vào các hàng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhắc nhở: Khi đang ở ô cuối cùng của bảng, nhấn phím `Tab` sẽ tự động sinh ra một hàng mới. | **1. Cách tạo bảng:**<br>- Đặt con trỏ soạn thảo tại vị trí cần tạo bảng.<br>- Chọn dải lệnh `Insert` $\rightarrow$ nhấp chọn nút `Table`.<br>- Kéo thả chuột để chọn số hàng và số cột mong muốn, hoặc nhấp vào `Insert Table...` rồi nhập số cột, số hàng.<br>- Nhập dữ liệu vào các ô: Dùng chuột hoặc các phím mũi tên, phím `Tab` để di chuyển giữa các ô. |

### Hoạt động 2.2: Thay đổi cấu trúc và định dạng bảng (30 phút)
a) Mục tiêu: Thành thạo chèn/xóa hàng cột, gộp ô và căn chỉnh văn bản trong ô.
b) Nội dung: Khảo sát hai dải lệnh phụ trợ `Table Design` và `Layout`; làm theo hướng dẫn SGK trang 55 - 56.
c) Sản phẩm: Bảng danh sách được gộp ô tiêu đề và căn giữa nội dung.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn khi nhấp con trỏ vào bảng sẽ xuất hiện 2 dải lệnh mới: `Table Design` và `Layout`.<br>+ Nhóm `Rows & Columns`: `Insert Above/Below` (chèn hàng), `Insert Left/Right` (chèn cột), `Delete` (xóa).<br>+ Nhóm `Merge`: `Merge Cells` (gộp nhiều ô đã chọn thành 1 ô).<br>+ Nhóm `Alignment`: 9 nút căn lề trong ô (đặc biệt là căn giữa cả ngang và dọc).<br>- **HS:** Thao tác gộp các ô của hàng đầu tiên làm tiêu đề bảng.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Bôi đen hàng 1, nhấp chuột phải chọn `Merge Cells` và gõ "DANH SÁCH TỔ 1".<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS chỉnh độ rộng các cột bằng cách kéo rê đường biên giữa các cột.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi học sinh đã biết cách phối màu nền cho hàng tiêu đề (`Shading`). | **2. Hiệu chỉnh và định dạng bảng:**<br>- **Chèn thêm hàng/cột:** Nhấp chuột phải $\rightarrow$ `Insert` $\rightarrow$ chọn chèn hàng trên/dưới hoặc cột trái/phải.<br>- **Xóa hàng/cột/bảng:** Chọn hàng/cột cần xóa $\rightarrow$ nhấp chuột phải $\rightarrow$ `Delete`.<br>- **Gộp ô (`Merge Cells`):** Chọn các ô cần gộp $\rightarrow$ nhấp nút `Merge Cells` trên dải lệnh `Layout`.<br>- **Căn lề nội dung trong ô:** Chọn dải lệnh `Layout` $\rightarrow$ chọn biểu tượng căn giữa `Align Center`.<br>- **Định dạng viền và màu nền:** Dùng nút `Borders` và `Shading` trên dải lệnh `Table Design`. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (20 phút)
a) Mục tiêu: Tự tay thiết kế Bảng Thời khóa biểu tuần học của lớp mình.
b) Nội dung: Tạo bảng gồm 7 cột (Thứ, Tiết, Thứ Hai, Thứ Ba, Thứ Tư, Thứ Năm, Thứ Sáu) và 6 hàng (Tiết 1 đến 5). Định dạng tiêu đề nổi bật, màu nền xen kẽ.
c) Sản phẩm: Bảng Thời khóa biểu hoàn chỉnh, đẹp mắt lưu trên máy.
d) Tổ chức thực hiện: Học sinh thực hành độc lập, GV hỗ trợ cá nhân.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (15 phút)
- **Tích hợp NLS 3.1.TC2a:** GV hướng dẫn học sinh tạo Bảng kế hoạch chi tiêu cá nhân hoặc Bảng theo dõi mục tiêu học tập 5 môn chính trong tuần. Dặn dò chuẩn bị cho Bài 13: Thực hành tìm kiếm và thay thế.
"""

# 05. Bài 13: Thực hành Tìm kiếm và thay thế (Tiết 26)
md_05 = """Tiết 26 - BÀI 13: THỰC HÀNH TÌM KIẾM VÀ THAY THẾ
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hiểu được mục đích và tác dụng của công cụ Tìm kiếm (`Find`) và Thay thế (`Replace`) trong phần mềm soạn thảo văn bản.
- Thực hiện được thao tác tìm kiếm một từ hoặc cụm từ bất kỳ trong văn bản dài một cách nhanh chóng, tự động.
- Thực hiện được thao tác thay thế một từ/cụm từ cũ bằng từ/cụm từ mới cho từng vị trí (`Replace`) hoặc cho toàn bộ văn bản (`Replace All`).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự phát hiện các lỗi sai chính tả lặp đi lặp lại trong văn bản dài và biết dùng công cụ thay thế tự động để sửa lỗi.
- Giải quyết vấn đề và sáng tạo: Lựa chọn từ khóa tìm kiếm chính xác, phân biệt khi nào dùng `Replace` (thay thế từng từ để kiểm tra) và `Replace All` (thay thế hàng loạt).

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng dụng CNTT (NLc): Sử dụng thành thạo hộp thoại `Find and Replace` trong Word để tiết kiệm thời gian chỉnh sửa văn bản.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Sử dụng tổ hợp phím tắt nhanh `Ctrl+F` (tìm kiếm) và `Ctrl+H` (thay thế) để tự động hóa xử lý văn bản số.***

## 3. Về phẩm chất
- Cẩn trọng, tỉ mỉ, kiểm tra kỹ ngữ cảnh trước khi thay thế hàng loạt để tránh làm thay đổi nghĩa của các từ ngữ khác.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, máy chiếu, tệp văn bản mẫu dài 3 trang (chứa nhiều từ viết sai chính tả hoặc cần đổi tên nhân vật).
2. Học sinh: SGK Tin học 6, vở ghi, máy tính thực hành.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (5 phút)
a) Mục tiêu: Đặt ra bài toán thực tế chứng minh sự ưu việt của công cụ tự động so với tìm thủ công bằng mắt.
b) Nội dung: Trong một cuốn truyện dài 100 trang, tên nhân vật "Dế Mèn" vô tình bị gõ nhầm thành "Dế Choắt" ở hàng chục chỗ. Nếu đọc từng dòng để tìm và sửa thì mất bao lâu? Có công cụ nào sửa xong chỉ trong 1 giây không?
c) Sản phẩm: Học sinh tò mò và hào hứng muốn biết công cụ Thay thế tự động.
d) Tổ chức thực hiện: GV dẫn dắt vào bài mới.

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC VÀ THỰC HÀNH (25 phút)
### Hoạt động 2.1: Công cụ Tìm kiếm (Find) (10 phút)
a) Mục tiêu: Biết mở thanh điều hướng tìm kiếm và nhập từ khóa cần tìm.
b) Nội dung: Đọc mục 1 SGK trang 58 - 59; thực hành phím tắt `Ctrl + F`.
c) Sản phẩm: Các từ khóa tìm kiếm được bôi vàng nổi bật trên trang văn bản.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn cách mở công cụ Tìm kiếm:<br>Cách 1: Vào dải lệnh `Home` $\rightarrow$ nhóm `Editing` $\rightarrow$ chọn `Find`.<br>Cách 2: Nhấn tổ hợp phím `Ctrl + F`.<br>- **GV:** Nhập từ khóa cần tìm vào ô `Navigation` bên trái màn hình.<br>- **HS:** Thao tác trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhập từ "Việt Nam" vào ô tìm kiếm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS quan sát: Tất cả các từ "Việt Nam" trong văn bản đều được tô màu nổi bật và thông báo số lượng kết quả tìm thấy.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhấn phím mũi tên lên/xuống để chuyển nhanh đến từng vị trí từ tìm thấy. | **1. Tìm kiếm văn bản:**<br>- Nhấn `Ctrl + F` (hoặc `Home` $\rightarrow$ `Find`).<br>- Gõ từ hoặc cụm từ cần tìm vào ô tìm kiếm.<br>- Kết quả: Các từ tìm thấy sẽ được tô sáng tự động trong văn bản, số lần xuất hiện được thống kê rõ ràng. |

### Hoạt động 2.2: Công cụ Thay thế (Replace) (15 phút)
a) Mục tiêu: Nắm vững cách dùng hộp thoại `Find and Replace` để thay thế từ cũ bằng từ mới.
b) Nội dung: Đọc mục 2 SGK trang 59 - 60; thực hành phím tắt `Ctrl + H`.
c) Sản phẩm: Thay thế thành công các từ viết sai trong bài thực hành.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Hướng dẫn mở hộp thoại Thay thế:<br>Cách 1: `Home` $\rightarrow$ nhóm `Editing` $\rightarrow$ chọn `Replace`.<br>Cách 2: Nhấn tổ hợp phím `Ctrl + H`.<br>- **GV:** Giải thích hai ô:<br>+ `Find what`: Nhập từ/cụm từ cũ cần thay.<br>+ `Replace with`: Nhập từ/cụm từ mới thay thế.<br>- **GV:** Phân biệt nút `Replace` (thay từng từ) và `Replace All` (thay thế tất cả).<br>- **HS:** Thao tác theo hướng dẫn.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thay thế từ viết tắt "hn" thành "Hà Nội" trong tệp thực hành.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS báo cáo: Hộp thoại báo "All done. We made 8 replacements." (Đã thay thế 8 vị trí).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Lưu ý cảnh báo: Cần cẩn thận khi bấm `Replace All`, tránh thay thế nhầm các từ có chứa từ khóa (ví dụ thay "ba" thành "bố" có thể làm từ "bà" bị đổi nhầm). | **2. Thay thế văn bản:**<br>- Nhấn tổ hợp phím `Ctrl + H`.<br>- Trong hộp thoại `Find and Replace`:<br>+ Ô `Find what`: Nhập từ/cụm từ cần tìm.<br>+ Ô `Replace with`: Nhập từ/cụm từ thay thế.<br>+ Nhấp `Find Next` để tìm vị trí tiếp theo.<br>+ Nhấp `Replace` để thay thế từng vị trí sau khi đã kiểm tra.<br>+ Nhấp `Replace All` để thay thế tự động toàn bộ văn bản. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP (10 phút)
- Thực hiện bài tập Luyện tập SGK trang 60: Tìm tất cả các từ "máy vi tính" và thay thế bằng từ "máy tính". Báo cáo số lần thay thế được.

## D. HOẠT ĐỘNG 4: VẬN DỤNG (5 phút)
- **Tích hợp NLS 3.1.TC2a:** GV giới thiệu tính năng tìm kiếm nâng cao: Tìm kiếm phân biệt chữ hoa/chữ thường (`Match case`) trong nút `More >>`. Dặn dò chuẩn bị cho Bài 14: Thực hành tổng hợp - Hoàn thiện sổ lưu niệm (Ôn tập giữa HKII).
"""

# 06. Bài 14: Thực hành tổng hợp: Hoàn thiện sổ lưu niệm - Ôn tập giữa HKII (Tiết 27)
md_06 = """Tiết 27 - BÀI 14: THỰC HÀNH TỔNG HỢP: HOÀN THIỆN SỔ LƯU NIỆM (ÔN TẬP GIỮA HỌC KÌ II)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ các kiến thức và kỹ năng trong Chủ đề 5: Ứng dụng tin học (Định dạng ký tự, định dạng đoạn, định dạng trang, chèn và định dạng bảng biểu, tìm kiếm và thay thế, sơ đồ tư duy).
- Thực hành phối hợp linh hoạt các kỹ năng đã học để hoàn thiện một sản phẩm số thực tế: "Trang Sổ lưu niệm lớp 6" hoặc "Tập san chào mừng ngày 26/3".
- Chuẩn bị kiến thức và kỹ năng vững vàng cho tiết Kiểm tra đánh giá giữa học kì II.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự tổng hợp kiến thức qua sơ đồ tư duy hệ thống hóa giữa học kì II.
- Giải quyết vấn đề và sáng tạo: Thiết kế bố cục trang sổ lưu niệm mang phong cách riêng, màu sắc hài hòa, trình bày thông tin khoa học.

b) Năng lực đặc thù môn Tin học:
- Năng lực ứng dụng CNTT (NLc): Phối hợp văn bản, hình ảnh, bảng biểu và sơ đồ tư duy để tạo ra ấn phẩm số có tính thẩm mĩ cao.

c) Năng lực số (NLS) và Trí tuệ nhân tạo (AI):
- ***NLS 3.1.TC2a: Tích hợp đa phương tiện (văn bản số, bảng biểu, sơ đồ đồ họa) để hoàn thiện sản phẩm truyền thông số hoàn chỉnh.***

## 3. Về phẩm chất
- Tình cảm bạn bè, yêu quý trường lớp, có ý thức lưu giữ những kỷ niệm đẹp tuổi học trò qua các sản phẩm công nghệ.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: Kế hoạch bài dạy, Sơ đồ tư duy Ôn tập giữa HKII môn Tin học 6, các mẫu trang sổ lưu niệm xuất sắc của các khóa trước, phòng máy tính.
2. Học sinh: SGK Tin học 6, ảnh chụp tập thể lớp/tổ (đã chuẩn bị sẵn trên USB hoặc tài khoản đám mây), máy tính thực hành Word.

# III. TIẾN TRÌNH DẠY HỌC
## A. HOẠT ĐỘNG 1: MỞ ĐẦU (4 phút)
a) Mục tiêu: Tạo cảm hứng sáng tạo sản phẩm lưu niệm của lớp.
b) Nội dung: Trình chiếu một video ngắn ghép các trang sổ lưu niệm điện tử của các anh chị lớp trước.
c) Sản phẩm: Sự thích thú và mong muốn tự tay tạo ra trang lưu niệm cho tổ mình.
d) Tổ chức thực hiện: GV giới thiệu nhiệm vụ của buổi thực hành tổng hợp và dẫn dắt vào bài.

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (33 phút)
### Hoạt động 2.1: Hệ thống hóa kiến thức Ứng dụng tin học qua Sơ đồ tư duy (8 phút)
a) Mục tiêu: Ôn tập có hệ thống toàn bộ chuỗi kỹ năng soạn thảo văn bản và sơ đồ tư duy chuẩn bị cho kiểm tra giữa HKII.
b) Nội dung: Trình chiếu và phân tích Sơ đồ tư duy Ôn tập giữa học kì II: Ứng dụng tin học.
c) Sản phẩm: Sơ đồ tư duy được khắc sâu trong vở của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy hệ thống hóa kiến thức giữa HKII.<br>- **GV:** Yêu cầu HS nêu 4 trụ cột kiến thức: 1. Sơ đồ tư duy; 2. Định dạng văn bản; 3. Trình bày bảng biểu; 4. Tìm kiếm và thay thế.<br>- **HS:** Quan sát và theo dõi sơ đồ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Nhắc lại các thao tác cốt lõi trong Word.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy thuyết minh toàn bộ 4 nhánh của sơ đồ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt lại các kỹ năng bắt buộc phải thành thạo trong bài kiểm tra giữa kì. | **SƠ ĐỒ TƯ DUY ÔN TẬP GIỮA HỌC KÌ II: ỨNG DỤNG TIN HỌC**<br><br>*(Sơ đồ tư duy hệ thống hóa hiển thị dưới đây)* |

![Sơ đồ tư duy Ôn tập giữa học kì II Tin học 6](khbd-ill:mindmap-tin6-tiet27-giuahk2)

### Hoạt động 2.2: Thực hành tổng hợp hoàn thiện Sổ lưu niệm lớp (25 phút)
a) Mục tiêu: Hoàn thiện một văn bản Word 1 trang gồm: Tiêu đề trang trí, Ảnh tập thể lớp/tổ, Bảng danh sách thành viên và cảm nghĩ ngắn.
b) Nội dung: Thực hành trên máy tính theo các tiêu chí đánh giá của GV.
c) Sản phẩm: Tệp `SoLuuNiem_ToX.docx` lưu trong máy tính của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ thực hành tổng hợp:<br>1. Tiêu đề: "SỔ LƯU NIỆM TỔ ... - LỚP 6A" (chữ hoa, cỡ 18pt, đậm, căn giữa, màu xanh).<br>2. Chèn 01 ảnh tập thể lớp/tổ, căn giữa trang.<br>3. Chèn 01 bảng gồm 4 cột (STT, Họ tên, Biệt danh, Ước mơ) và điền 4 thành viên.<br>4. Một đoạn văn cảm nghĩ (3 - 4 câu) căn lề đều hai bên (`Justify`).<br>5. Đặt lề trang in chuẩn A4.<br>- **HS:** Thực hành trên máy tính.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện tuần tự các thao tác định dạng và chèn bảng.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Các tổ chiếu sản phẩm của mình lên màn hình lớn.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá, chấm điểm tại chỗ và khen ngợi sự sáng tạo của các nhóm. | **Tiêu chí đánh giá sản phẩm Sổ lưu niệm:**<br>- **Định dạng ký tự và đoạn:** Tiêu đề nổi bật, đoạn văn căn đều hai bên, không có lỗi phông chữ tiếng Việt (3 điểm).<br>- **Bảng biểu:** Bảng cân đối, có tiêu đề bảng gộp ô, căn lề trong ô đẹp mắt (3 điểm).<br>- **Hình ảnh minh họa:** Chèn ảnh hài hòa, không làm xô lệch bố cục trang (2 điểm).<br>- **Bố cục trang in:** Khổ A4, căn lề chuẩn mực, vừa vặn trong 1 trang (2 điểm). |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
- **Tích hợp NLS 3.1.TC2a:** Xuất sản phẩm sang định dạng PDF và chia sẻ lên thư mục dùng chung của lớp trên Google Drive để tạo thành "Cuốn Kỷ yếu số của Lớp 6A". Dặn dò ôn tập kỹ toàn bộ lý thuyết và kỹ năng thực hành để chuẩn bị cho tiết Kiểm tra giữa học kì II tuần tới.
"""

tasks = [
    ("01_KHBD_Tin6_Bai09_AnToanThongTinTrenInternet_Tiet19.md", md_01),
    ("02_KHBD_Tin6_Bai10_SoDoTuDuy_Tiet20-21.md", md_02),
    ("03_KHBD_Tin6_Bai11_DinhDangVanBan_Tiet22-23.md", md_03),
    ("04_KHBD_Tin6_Bai12_TrinhBayThongTinDangBang_Tiet24-25.md", md_04),
    ("05_KHBD_Tin6_Bai13_ThucHanh_TimKiemVaThayThe_Tiet26.md", md_05),
    ("06_KHBD_Tin6_Bai14_ThucHanhTongHop_HoanThienSoLuuNiem_Tiet27.md", md_06),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo: {filename}")
