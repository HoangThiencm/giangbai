# -*- coding: utf-8 -*-
"""
Script sinh 4 tệp KHBD Markdown môn Tin học 6 (Tuần 13 - 18):
1. Bài 7: Tìm kiếm thông tin trên Internet (Tiết 13, 14)
2. Bài 8: Thư điện tử (Tiết 15, 16)
3. Ôn tập cuối học kì I (Tiết 17)
4. Kiểm tra đánh giá cuối học kì I (Tiết 18)
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = "TROLYTHIEN/TEMP/10.11_Tin6"
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 01. BÀI 7: TÌM KIẾM THÔNG TIN TRÊN INTERNET (Tiết 13, 14)
# -------------------------------------------------------------
md_01 = """Tiết 13, 14 - BÀI 7: TÌM KIẾM THÔNG TIN TRÊN INTERNET
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và hiểu được khái niệm **Máy tìm kiếm (Search Engine)**: Là trang web/công cụ phần mềm giúp người dùng tìm kiếm thông tin trên Internet theo yêu cầu (ví dụ: Google, Microsoft Bing, Yahoo, Cốc Cốc...).
- Hiểu được khái niệm **Từ khóa (Keyword)**: Là từ hoặc cụm từ ngắn gọn, cốt lõi mô tả nội dung thông tin cần tìm.
- Nắm được các bước tìm kiếm thông tin bằng máy tìm kiếm:
  1. Truy cập vào trang web của máy tìm kiếm (ví dụ: `google.com`).
  2. Nhập từ khóa tìm kiếm vào ô tìm kiếm rồi nhấn Enter (hoặc nhấp chuột vào nút Tìm kiếm).
  3. Lựa chọn kết quả tìm kiếm phù hợp trong danh sách kết quả hiển thị.
- Biết cách sử dụng **dấu ngoặc kép `""`** để tìm kiếm chính xác cụm từ.
- Biết đánh giá sơ bộ độ tin cậy của thông tin tìm được dựa trên nguồn gốc xuất xứ (website cơ quan nhà nước `.gov.vn`, cơ sở giáo dục `.edu.vn`, tác giả, thời gian xuất bản).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự xác định từ khóa phù hợp với chủ đề cần tra cứu, chủ động đối chiếu kết quả tìm kiếm với mục tiêu ban đầu.
- Giao tiếp và hợp tác: Làm việc nhóm đôi trong phòng máy, cùng thảo luận lựa chọn trang web chứa thông tin tin cậy nhất.

b) Năng lực đặc thù môn Tin học:
- Năng lực C (Ứng dụng công nghệ thông tin và truyền thông): Sử dụng thành thạo máy tìm kiếm trên trình duyệt web để tìm kiếm văn bản, hình ảnh phục vụ học tập.
- Năng lực D (Đạo đức, pháp luật và văn hóa trong môi trường số): Biết tôn trọng quyền tác giả và chọn lọc thông tin tích cực, văn minh.

c) Năng lực số (NLS):
- ***1.1.TC1a: HS sử dụng thành thạo máy tìm kiếm Google, phân biệt được kết quả tìm kiếm dạng văn bản và dạng hình ảnh, áp dụng kĩ thuật tìm kiếm chính xác bằng cặp dấu ngoặc kép để nâng cao hiệu quả tra cứu.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.A3.1: Thực hành ra quyết định chọn lọc từ khóa tìm kiếm với sự hỗ trợ gợi ý của trợ lý AI; học sinh cân nhắc lựa chọn kết quả tìm kiếm kèm lý do và đối chiếu SGK (Áp dụng: tiết 1, 2).***

## 3. Về phẩm chất
- Rèn luyện tính kiên nhẫn, cẩn trọng trong việc kiểm chứng nguồn gốc thông tin trên môi trường mạng.
- Có ý thức tự bảo vệ mình trước những thông tin giả mạo, sai lệch trên Internet.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Tin học 6, KHBD, máy tính kết nối Internet, máy chiếu, bảng phụ ghi các kĩ thuật từ khóa.
2. Học sinh: SGK Tin học 6, vở ghi bài, máy tính phòng thực hành có kết nối Internet.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: Xuất phát từ tình huống thực tế cần tìm tư liệu làm bài thuyết trình Lịch sử - Địa lý để tạo nhu cầu sử dụng máy tìm kiếm.
b) Nội dung: Tình huống: Cô giáo giao nhiệm vụ tìm hình ảnh và tư liệu về \"Hang Sơn Đoòng - hang động tự nhiên lớn nhất thế giới\". Em sẽ làm thế nào để tìm được nhanh nhất?
c) Sản phẩm: Câu trả lời của HS: Sử dụng Google để gõ tìm kiếm từ khóa \"Hang Sơn Đoòng\".
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt vấn đề: Trong kho tàng hàng tỉ trang web của thế giới, làm thế nào để ta tìm được chính xác trang web nói về Hang Sơn Đoòng chỉ trong vài giây?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Trao đổi cặp đôi rút ra phương án: Dùng Google gõ tên bài cần tìm.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời: Em mở trình duyệt lên rồi vào Google gõ từ khóa.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Giới thiệu công cụ hỗ trợ kỳ diệu đó chính là Máy tìm kiếm (Search Engine), dẫn dắt vào bài mới. | **Khởi động:**<br>- Để tìm kiếm thông tin nhanh chóng trên Internet, con người sử dụng các công cụ gọi là Máy tìm kiếm (Search Engine). |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (50 phút)
### Hoạt động 2.1: Tìm kiếm thông tin trên Internet và Máy tìm kiếm (25 phút - Tiết 13)
a) Mục tiêu: Hiểu rõ máy tìm kiếm là gì, từ khóa là gì và quy trình 3 bước tìm kiếm thông tin.
b) Nội dung: Đọc mục 1 SGK trang 28-29; thực hiện HĐ1, HĐ2.
c) Sản phẩm: Khái niệm máy tìm kiếm, cách chọn từ khóa và các bước tìm kiếm.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt các câu hỏi:<br>  1. Kể tên một số máy tìm kiếm phổ biến mà em biết.<br>  2. Từ khóa là gì? Nếu muốn tìm thông tin về cách làm món bánh chưng ngày Tết, em sẽ chọn từ khóa nào?<br>  3. Nêu các bước cơ bản để tìm kiếm thông tin bằng máy tìm kiếm.<br>- **HS:** Đọc SGK trang 28, 29 và thảo luận nhóm đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc nhóm, ghi nhận câu trả lời vào vở nháp.<br>- **GV:** Quan sát, hướng dẫn HS cách rút gọn từ khóa (loại bỏ từ nối không cần thiết như \"làm thế nào để\", \"những cách\").<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 2 nhóm phát biểu: Từ khóa là `cách làm bánh chưng` hoặc `\"cách làm bánh chưng\"`. Các máy tìm kiếm: Google, Bing, Yahoo.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy trình 3 bước tìm kiếm. | **1. Tìm kiếm thông tin trên Internet:**<br>- **Máy tìm kiếm (Search Engine):** Là công cụ hỗ trợ người dùng tìm kiếm thông tin trên Internet theo yêu cầu.<br>- Các máy tìm kiếm thông dụng: `google.com`, `bing.com`, `coccoc.com`.<br>- **Từ khóa (Keyword):** Là từ hoặc cụm từ ngắn gọn thể hiện nội dung cần tìm.<br>- **Các bước tìm kiếm thông tin:**<br>1. Truy cập vào trang web của máy tìm kiếm.<br>2. Gõ từ khóa vào ô tìm kiếm rồi nhấn phím Enter.<br>3. Xem danh sách kết quả và nhấp chọn trang web phù hợp nhất. |

### Hoạt động 2.2: Kĩ thuật thu hẹp phạm vi tìm kiếm và Đánh giá độ tin cậy thông tin (25 phút - Tiết 14)
a) Mục tiêu: Biết sử dụng dấu ngoặc kép để tìm kiếm cụm từ chính xác; biết cách đánh giá nguồn tin cậy trên Internet.
b) Nội dung: Đọc mục 2 SGK trang 30-31; so sánh số lượng kết quả khi dùng và không dùng dấu ngoặc kép.
c) Sản phẩm: Thao tác tìm kiếm chính xác và bảng tiêu chí đánh giá website tin cậy.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Thực hiện mẫu trên máy chiếu:<br>  + Tìm từ khóa: `Vườn quốc gia Cúc Phương` (cho ra hàng triệu kết quả).<br>  + Tìm từ khóa: `\"Vườn quốc gia Cúc Phương\"` (số lượng kết quả giảm rõ rệt và chính xác hơn).<br>- **GV:** Đặt câu hỏi: Dấu ngoặc kép `\" \"` có tác dụng gì?<br>- **GV:** Nêu tiếp vấn đề: Thông tin trên mạng có phải lúc nào cũng đúng không? Dựa vào đâu để em tin tưởng một trang web?<br>- **HS:** Quan sát và lắng nghe.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thử nghiệm trực tiếp trên máy tính cá nhân cả 2 cách gõ từ khóa.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS nêu nhận xét: Dấu ngoặc kép giúp tìm chính xác nguyên vẹn cả cụm từ theo đúng thứ tự. Website tin cậy thường là của cơ quan nhà nước, tổ chức uy tín, có tên tác giả rõ ràng.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại kĩ thuật dấu ngoặc kép và lưu ý HS tuyệt đối không vội tin các tin đồn vô căn cứ trên mạng xã hội. | **2. Kĩ thuật tìm kiếm và chọn lọc thông tin:**<br>- **Sử dụng dấu ngoặc kép `\"...\"`:** Để máy tìm kiếm lọc ra những trang web chứa chính xác cụm từ khóa theo đúng trật tự từ.<br>- **Đánh giá độ tin cậy của thông tin:**<br>+ Tác giả: Tác giả là chuyên gia hoặc cơ quan có thẩm quyền.<br>+ Tên miền tin cậy: `.gov.vn` (cơ quan chính phủ), `.edu.vn` (giáo dục).<br>+ Thời gian: Bài viết mới cập nhật, có dẫn nguồn số liệu cụ thể. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP VÀ THỰC HÀNH (23 phút)
a) Mục tiêu: Vận dụng máy tìm kiếm để tìm thông tin và hình ảnh về một danh lam thắng cảnh Việt Nam.
b) Nội dung: HS thực hiện bài thực hành SGK trang 31: Tìm kiếm thông tin và hình ảnh về Vịnh Hạ Long.
c) Sản phẩm: Đoạn văn bản ngắn tóm tắt và 1 hình ảnh đẹp về Vịnh Hạ Long được HS lưu vào máy tính.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ thực hành trên phòng máy:<br>  1. Dùng Google tìm kiếm từ khóa `\"Vịnh Hạ Long\"`.<br>  2. Chuyển sang mục \"Hình ảnh\" (Images) để chọn và tải về 1 bức ảnh vịnh Hạ Long sắc nét.<br>  3. Tìm đọc xem Vịnh Hạ Long được UNESCO công nhận là Di sản thiên nhiên thế giới vào năm nào?<br>- **HS:** Lắng nghe và sẵn sàng thao tác.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Tự lực thao tác trên máy tính cá nhân. GV bao quát, hướng dẫn học sinh cách lưu ảnh (nhấp chuột phải $\\rightarrow$ Lưu hình ảnh thành...).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- GV gọi 2 HS trả lời: Vịnh Hạ Long được công nhận vào năm 1994 và 2000.<br>- Trình chiếu sản phẩm hình ảnh của một số học sinh lên máy chủ.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá kĩ năng tìm kiếm thông tin và thao tác hình ảnh của cả lớp. | **Kết quả thực hành:**<br>- Tìm kiếm chính xác thông tin: Vịnh Hạ Long được UNESCO công nhận Di sản thiên nhiên thế giới lần 1 năm 1994 (về giá trị thẩm mỹ) và lần 2 năm 2000 (về giá trị địa chất - địa mạo).<br>- Biết cách chuyển tab tìm kiếm hình ảnh và lưu ảnh về máy. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
a) Mục tiêu: Vận dụng công cụ tìm kiếm và trợ lý AI để tra cứu mẹo học tốt môn Tiếng Anh và môn Tin học.
b) Nội dung: Thực hiện tìm kiếm mẹo học tập trên Google và nhờ trợ lý AI gợi ý 3 từ khóa tìm kiếm hay nhất.
c) Sản phẩm: Danh sách 3 mẹo học tập được ghi lại vào vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu bài toán thực tiễn: Em hãy tìm 3 trang web cung cấp bài tập trắc nghiệm ôn thi môn Tin học 6 uy tín nhất.<br>- **HS:** Nhận nhiệm vụ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thực hiện tìm kiếm với từ khóa: `bài tập trắc nghiệm tin học 6 kết nối tri thức`.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- HS báo cáo: Trang web `vietjack.com`, `loigiaihay.com`, `hoc247.net`.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, chốt bài học. Dặn dò HS chuẩn bị bài học tiếp theo: Bài 8 - Thư điện tử. | **Vận dụng thực tế:**<br>- Biết chọn lọc từ khóa dài chứa đầy đủ thông tin bộ sách và môn học.<br>- Khai thác nguồn tài liệu trực tuyến phong phú phục vụ việc tự học ở nhà. |
"""

# -------------------------------------------------------------
# 02. BÀI 8: THƯ ĐIỆN TỬ (Tiết 15, 16)
# -------------------------------------------------------------
md_02 = """Tiết 15, 16 - BÀI 8: THƯ ĐIỆN TỬ
*Thời lượng thực hiện: 02 tiết (90 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Nhận biết và hiểu được khái niệm **Thư điện tử (Electronic Mail - viết tắt là Email)**: Là dịch vụ gửi và nhận thư dưới dạng số qua mạng Internet.
- Phân tích được các ưu điểm vượt trội của thư điện tử so với thư truyền thống (tốc độ gửi nhận tức thời, chi phí rất thấp, có thể gửi cùng lúc cho nhiều người, đính kèm được nhiều dạng dữ liệu: văn bản, hình ảnh, âm thanh, video...).
- Hiểu được cấu trúc chuẩn của một địa chỉ thư điện tử: `<Tên người dùng>@<Tên máy chủ thư>` (ví dụ: `hoangthien@gmail.com`).
- Nhận biết các thành phần cơ bản trong một hộp thư điện tử: Hộp thư đến (Inbox), Đã gửi (Sent), Thư nháp (Drafts), Thùng rác (Trash/Bin), Thư rác (Spam).
- Thực hiện được các thao tác: Soạn thư, đính kèm tệp tin, gửi thư, mở đọc thư nhận được và trả lời thư.
- Nắm vững các quy tắc an toàn và văn hóa khi sử dụng thư điện tử (bảo vệ mật khẩu, không mở liên kết lạ, sử dụng ngôn từ lịch sự, có tiêu đề rõ ràng).

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Chủ động tìm hiểu giao diện dịch vụ email, tự soạn thảo nội dung thư gửi cho bạn học.
- Giao tiếp và hợp tác: Biết cách gửi thư điện tử trao đổi bài tập nhóm, biết sử dụng ngôn phong tôn trọng và lịch sự.

b) Năng lực đặc thù môn Tin học:
- Năng lực C (Ứng dụng công nghệ thông tin và truyền thông): Sử dụng thành thạo dịch vụ thư điện tử trên môi trường mạng để giao tiếp và trao đổi học liệu.

c) Năng lực số (NLS):
- ***2.1.TC1a: HS sử dụng dịch vụ thư điện tử để gửi thông tin đính kèm tệp văn bản bài tập; hiểu rõ cấu trúc địa chỉ email và cách phân biệt hộp thư đến với thư rác.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.A1.2: HS sử dụng công cụ AI để học cách viết một bức thư điện tử chuẩn mực (có đầy đủ lời chào mở đầu, nội dung súc tích và lời chúc kết thư trang trọng).***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, bảo vệ bí mật thông tin cá nhân và tôn trọng quyền riêng tư thư từ của người khác.
- Có ý thức phòng tránh mã độc và thư rác trong môi trường truyền thông số.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Tin học 6, KHBD, máy tính kết nối mạng Internet, máy chiếu, tài khoản email giáo viên dùng để minh họa.
2. Học sinh: SGK Tin học 6, vở ghi bài, máy tính phòng thực hành có kết nối Internet.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (7 phút)
a) Mục tiêu: So sánh cách thức gửi thư qua bưu điện truyền thống và gửi thư điện tử để học sinh thấy được sự tiện lợi của email.
b) Nội dung: Quan sát bảng so sánh thời gian và chi phí khi gửi một bức thư tay từ Hà Nội vào TP. Hồ Chí Minh với việc gửi một email.
c) Sản phẩm: Câu trả lời của học sinh về tốc độ và chi phí gửi thư điện tử.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu câu hỏi:<br>  1. Ngày xưa, khi ông bà ta muốn gửi một lá thư từ Bắc vào Nam thì mất bao lâu và cần những gì?<br>  2. Ngày nay, muốn gửi một bức thư có kèm 10 bức ảnh kỷ niệm cho bạn ở nước ngoài, ta dùng cách nào nhanh nhất và gần như miễn phí?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhanh cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời: Thư bưu điện mất vài ngày đến cả tuần, tốn tiền mua tem. Thư điện tử chỉ mất vài giây là người nhận đọc được ngay.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Nhận xét, nhấn mạnh thư điện tử là một bước ngoặt lớn trong giao tiếp của nhân loại, dẫn dắt vào bài học. | **Khởi động:**<br>- Thư truyền thống: Chậm, chi phí giấy bút, tem thư, chỉ gửi được chữ viết và ảnh in.<br>- Thư điện tử (Email): Nhanh chóng tức thời, chi phí rất thấp, gửi được tệp đa phương tiện đến nhiều người cùng lúc. |

## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI (50 phút)
### Hoạt động 2.1: Thư điện tử và Địa chỉ thư điện tử (25 phút - Tiết 15)
a) Mục tiêu: Nắm vững khái niệm thư điện tử, cấu trúc địa chỉ thư điện tử và các ưu điểm chính.
b) Nội dung: Đọc mục 1 SGK trang 32-34; phân tích ví dụ địa chỉ email.
c) Sản phẩm: Cấu trúc địa chỉ email và bài giải bài tập phân biệt địa chỉ hợp lệ.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình bày:<br>  + Khái niệm thư điện tử (Email).<br>  + Cấu trúc địa chỉ email: `<Tên người dùng>@<Tên máy chủ thư>`.<br>  + Quy tắc: Tên người dùng do người lập chọn (viết liền không dấu, không chứa dấu cách); Kí hiệu `@` (a còng) là bắt buộc.<br>- **GV:** Yêu cầu HS chỉ ra địa chỉ email hợp lệ trong các địa chỉ sau:<br>  1. `nguyenvanan@gmail.com`<br>  2. `nguyen van an@gmail.com`<br>  3. `tranthib@yahoo`<br>  4. `lehoang@outlook.com.vn`<br>- **HS:** Đọc SGK và hoàn thành bài tập.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Làm việc cá nhân vào vở.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 HS đứng tại chỗ giải thích: Địa chỉ 1 và 4 hợp lệ. Địa chỉ 2 sai vì có dấu cách. Địa chỉ 3 sai vì thiếu tên miền máy chủ (`.com`).<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa quy tắc đặt tên địa chỉ thư điện tử. | **1. Thư điện tử và Địa chỉ email:**<br>- **Thư điện tử (Email):** Là hệ thống gửi và nhận thư dưới dạng số qua mạng Internet.<br>- **Cấu trúc địa chỉ email:**<br>`<Tên người dùng>@<Tên nhà cung cấp dịch vụ>`<br>Ví dụ: `thcs.tranphu@moet.edu.vn`, `hoangthien@gmail.com`.<br>- **Lưu ý:** Tên người dùng viết liền không dấu, không có khoảng trắng. Kí hiệu `@` phân cách giữa tên người dùng và nhà cung cấp. |

### Hoạt động 2.2: Các thành phần của hộp thư điện tử và Quy trình gửi/nhận thư (25 phút - Tiết 16)
a) Mục tiêu: Biết các thư mục trong hộp thư, các bước soạn và gửi một bức thư có đính kèm tệp; nắm vững quy tắc an toàn.
b) Nội dung: Đọc mục 2 SGK trang 34-36; quan sát giao diện hộp thư điện tử Gmail/Outlook.
c) Sản phẩm: Ghi nhớ các bước gửi thư và các lưu ý an toàn email trong vở.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Chiếu giao diện hộp thư điện tử, chỉ rõ:<br>  + Nút \"Soạn thư\" (Compose).<br>  + Mục \"Đến\" (To): Nhập địa chỉ người nhận.<br>  + Mục \"Chủ đề/Tiêu đề\" (Subject): Tóm tắt ngắn gọn nội dung thư.<br>  + Vùng soạn thảo nội dung thư.<br>  + Biểu tượng chiếc kẹp giấy (Attach files): Đính kèm tệp tin.<br>  + Nút \"Gửi\" (Send).<br>- **GV:** Nêu các quy tắc an toàn: Đặt mật khẩu mạnh, không mở tệp lạ có đuôi `.exe`, không bấm vào liên kết trong thư rác.<br>- **HS:** Theo dõi và ghi chép.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm về các phép lịch sự khi gửi thư (có lời chào, xưng hô phù hợp, cảm ơn).<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS nhắc lại quy trình gửi thư có đính kèm tệp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chốt lại quy trình gửi thư điện tử chuẩn mực. | **2. Sử dụng thư điện tử an toàn:**<br>- **Các bước gửi thư:**<br>1. Đăng nhập vào hộp thư điện tử cá nhân.<br>2. Nhấp vào nút **Soạn thư** (Compose).<br>3. Nhập chính xác địa chỉ người nhận vào ô **Đến** (To).<br>4. Nhập tiêu đề thư vào ô **Chủ đề** (Subject).<br>5. Gõ nội dung thư và nhấp vào biểu tượng kẹp giấy để đính kèm tệp (nếu có).<br>6. Nhấp nút **Gửi** (Send).<br>- **Nguyên tắc an toàn:**<br>+ Đặt mật khẩu phức tạp (gồm chữ hoa, chữ thường, số, kí tự đặc biệt).<br>+ Đăng xuất tài khoản khi dùng máy tính công cộng.<br>+ Không mở thư lạ từ người không quen biết. |

## C. HOẠT ĐỘNG 3: LUYỆN TẬP VÀ THỰC HÀNH (23 phút)
a) Mục tiêu: Thực hành đăng nhập hộp thư học tập, soạn một bức thư gửi cho bạn cùng bàn có đính kèm tệp văn bản bài học.
b) Nội dung: Thực hành theo hướng dẫn SGK trang 35-36 trên máy tính phòng máy.
c) Sản phẩm: Thư điện tử được gửi thành công và hiển thị trong hộp thư đến của bạn.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao nhiệm vụ thực hành cặp đôi:<br>  1. Học sinh A lấy địa chỉ email của bạn B ngồi cạnh.<br>  2. Soạn một bức thư với tiêu đề: `Chào bạn - [Tên mình]`<br>  3. Nội dung: Chúc bạn một ngày học tập tốt lành và đính kèm 1 tệp hình ảnh đã tải ở Bài 7.<br>  4. Bấm Gửi, sau đó bạn B mở hộp thư đến kiểm tra, đọc thư và bấm \"Trả lời\" (Reply).<br>- **HS:** Nhận nhiệm vụ và bắt đầu thực hành.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thao tác trên máy tính cá nhân.<br>- **GV:** Quan sát, nhắc nhở học sinh gõ đúng địa chỉ email và không quên gõ Tiêu đề thư.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 2 cặp học sinh giơ tay báo cáo đã gửi và nhận thư thành công.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Khen ngợi tinh thần hợp tác và kĩ năng thực hành thành thạo của học sinh. | **Kết quả thực hành:**<br>- Gửi thành công thư điện tử có đính kèm tệp.<br>- Biết cách mở đọc thư trong Hộp thư đến (Inbox) và sử dụng chức năng Trả lời (Reply).<br>- Tuân thủ văn hóa ứng xử lịch thiệp trong giao tiếp qua thư từ điện tử. |

## D. HOẠT ĐỘNG 4: VẬN DỤNG (10 phút)
a) Mục tiêu: Vận dụng kiến thức email vào việc đăng ký dịch vụ học tập trực tuyến an toàn.
b) Nội dung: Trả lời câu hỏi tình huống về cách xử lý khi nhận được email giả mạo trúng thưởng.
c) Sản phẩm: Câu trả lời xử lý tình huống đúng đắn của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Nêu tình huống: Bỗng nhiên em nhận được một email từ địa chỉ lạ thông báo: \"Chúc mừng bạn đã trúng thưởng 1 chiếc điện thoại iPhone, hãy nhấp vào đường link này và nhập mật khẩu tài khoản để nhận thưởng\". Em sẽ xử lý thế nào?<br>- **HS:** Lắng nghe và suy nghĩ.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng dậy trả lời: Tuyệt đối không bấm vào link và không cung cấp mật khẩu, báo cho bố mẹ hoặc thầy cô và bấm chuyển thư vào mục Thư rác/Xóa thư.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương ý thức cảnh giác cao độ của học sinh. Dặn dò HS chuẩn bị cho tiết Ôn tập cuối học kì I ở tuần sau. | **Bài học thực tiễn:**<br>- Nhận biết dấu hiệu lừa đảo qua email (thông báo trúng thưởng lớn, yêu cầu nhập mật khẩu hoặc thông tin cá nhân).<br>- Hành động đúng: Không nhấp vào liên kết lạ, đánh dấu thư rác (Spam) và xóa thư ngay lập tức. |
"""

# -------------------------------------------------------------
# 03. ÔN TẬP CUỐI HỌC KÌ I (Tiết 17)
# -------------------------------------------------------------
md_03 = """Tiết 17 - ÔN TẬP CUỐI HỌC KÌ I (TIN HỌC 6)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Hệ thống hóa toàn bộ các kiến thức trọng tâm đã học trong toàn bộ Học kì I môn Tin học 6:
  + **Chủ đề 1: Máy tính và cộng đồng (Bài 1, 2, 3):** Phân biệt thông tin, dữ liệu, vật mang tin; 4 bước xử lí thông tin; biểu diễn thông tin bằng dãy bit (0 và 1); các đơn vị đo dung lượng nhớ (Byte, KB, MB, GB, TB) và bài toán quy đổi dung lượng.
  + **Chủ đề 2: Mạng máy tính và Internet (Bài 4, 5):** Khái niệm mạng máy tính; các thành phần chính của mạng; phân biệt mạng có dây và không dây; khái niệm, đặc điểm và lợi ích to lớn của Internet.
  + **Chủ đề 3: Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin (Bài 6, 7, 8):** Khái niệm World Wide Web (WWW); Siêu văn bản, Siêu liên kết, Website, Trang chủ và Địa chỉ URL; Trình duyệt web (Chrome, Edge, Firefox...); Máy tìm kiếm, từ khóa, kĩ thuật dấu ngoặc kép `\" \"`; Khái niệm Thư điện tử (Email), cấu trúc địa chỉ email và quy tắc an toàn khi sử dụng email.
- Củng cố kĩ năng giải bài tập trắc nghiệm khách quan và giải quyết các bài toán tình huống thực tiễn để chuẩn bị tốt nhất cho bài kiểm tra cuối học kì I.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác vẽ lại sơ đồ tư duy hệ thống kiến thức toàn học kì, chủ động rà soát những phần kiến thức còn chưa vững.
- Giao tiếp và hợp tác: Tự tin trao đổi phương pháp giải các bài toán quy đổi đơn vị và kĩ năng tìm kiếm thông tin trong nhóm học tập.

b) Năng lực đặc thù môn Tin học:
- Năng lực C (Ứng dụng công nghệ thông tin và truyền thông): Tổng hợp và vận dụng thành thạo trình duyệt web, máy tìm kiếm và dịch vụ thư điện tử vào học tập.
- Năng lực D (Đạo đức, pháp luật và văn hóa trong môi trường số): Tuân thủ các nguyên tắc an toàn thông tin, bảo vệ tài khoản cá nhân.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS sử dụng sơ đồ tư duy số hóa và phần mềm trắc nghiệm tương tác để tự tổng hợp kiến thức toàn diện 3 chủ đề học kì I.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.B2.1: HS ứng dụng trợ lý AI để tạo các bảng đối sánh giữa các thuật ngữ dễ nhầm lẫn: Internet vs World Wide Web; Trình duyệt web vs Máy tìm kiếm.***

## 3. Về phẩm chất
- Rèn luyện phẩm chất chăm chỉ, cẩn thận, trung thực và tinh thần trách nhiệm trong học tập.
- Có ý thức tự giác chuẩn bị chu đáo cho kì kiểm tra đánh giá cuối học kì I.

# II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU
1. Giáo viên: SGK Tin học 6, KHBD, Sơ đồ tư duy Mindmap Ôn tập cuối HKI Tin học 6 (vector 300 DPI), tivi/máy chiếu, hệ thống câu hỏi trắc nghiệm tương tác.
2. Học sinh: SGK Tin học 6, vở ghi bài, bảng con hoặc phiếu bài tập ôn tập.

# III. TIẾN TRÌNH DẠY HỌC

## A. HOẠT ĐỘNG 1: KHỞI ĐỘNG (5 phút)
a) Mục tiêu: Kích hoạt sự hào hứng và phản xạ nhanh của học sinh qua trò chơi \"Ai là triệu phú Tin học\".
b) Nội dung: Trả lời nhanh 3 câu hỏi trắc nghiệm tổng hợp kiến thức học kì I.
c) Sản phẩm: Bảng chọn đáp án của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu 3 câu hỏi nhanh:<br>  1. Kí hiệu bắt buộc phải có trong một địa chỉ thư điện tử là gì?<br>  2. Muốn tìm kiếm chính xác nguyên vẹn một cụm từ khóa, ta đặt cụm từ đó trong cặp dấu nào?<br>  3. World Wide Web (WWW) ra đời vào năm nào?<br>- **HS:** Chuẩn bị bảng con ghi đáp án.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Suy nghĩ và giơ bảng đáp án.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS đứng tại chỗ giải thích đáp án: `@`, dấu ngoặc kép `\" \"`, năm 1989.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Đánh giá phản xạ của học sinh, dẫn dắt vào bài ôn tập tổng kết cuối học kì I. | **Đáp án khởi động:**<br>1. Kí hiệu `@` (a còng).<br>2. Cặp dấu ngoặc kép `\"...\"`.<br>3. Năm 1989 (bởi Tim Berners-Lee). |

## B. HOẠT ĐỘNG 2: LUYỆN TẬP VÀ ÔN TẬP (32 phút)
### Hoạt động 2.1: Hệ thống hoá kiến thức qua Sơ đồ tư duy (12 phút)
a) Mục tiêu: Giúp học sinh nắm vững bức tranh tổng thể toàn bộ kiến thức 3 chủ đề học kì I qua Sơ đồ tư duy trực quan, sinh động.
b) Nội dung: Quan sát và phân tích Sơ đồ tư duy Mindmap Ôn tập cuối HKI Tin học 6; nhắc lại các kiến thức cốt lõi.

![Sơ đồ tư duy Ôn tập Cuối HK1 Tin học 6](khbd-ill:mindmap-tiet17)

c) Sản phẩm: Bản ghi nhớ hệ thống kiến thức toàn học kì trong vở học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Trình chiếu Sơ đồ tư duy Mindmap Ôn tập cuối HKI lên màn chiếu. Chia lớp thành 4 nhóm tương ứng 4 nhánh kiến thức:<br>  + Nhóm 1: Chủ đề 1 (Thông tin, dữ liệu, dãy bit, các bội số của Byte).<br>  + Nhóm 2: Chủ đề 2 (Mạng máy tính, thiết bị mạng, đặc điểm Internet).<br>  + Nhóm 3: Chủ đề 3 - Phần 1 (WWW, siêu văn bản, siêu liên kết, trình duyệt web, máy tìm kiếm).<br>  + Nhóm 4: Chủ đề 3 - Phần 2 (Thư điện tử, cấu trúc địa chỉ email, quy tắc an toàn).<br>- **HS:** Quan sát sơ đồ tư duy trên màn hình và chuẩn bị tóm tắt.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận nhóm trong 4 phút.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- Đại diện 4 nhóm lần lượt thuyết trình tóm tắt từng nhánh.<br>- Cả lớp lắng nghe, nhận xét và bổ sung.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Chuẩn hóa toàn bộ nội dung, nhấn mạnh các điểm học sinh thường hay nhầm lẫn. | **Hệ thống kiến thức trọng tâm Học kì I:**<br>1. **Chủ đề 1: Máy tính và cộng đồng:**<br>- Quá trình xử lí thông tin: Thu nhận $\\rightarrow$ Lưu trữ $\\rightarrow$ Xử lí $\\rightarrow$ Truyền.<br>- Đơn vị đo: $1\\text{ Byte} = 8\\text{ bit}$; $1\\text{ KB} = 1024\\text{ B}$; $1\\text{ MB} = 1024\\text{ KB}$; $1\\text{ GB} = 1024\\text{ MB}$; $1\\text{ TB} = 1024\\text{ GB}$.<br>2. **Chủ đề 2: Mạng máy tính và Internet:**<br>- Thiết bị mạng: Cáp mạng, Switch (bộ chuyển mạch), Access Point (điểm truy cập không dây).<br>- Internet: Mạng toàn cầu kết nối hàng triệu máy tính.<br>3. **Chủ đề 3: WWW, Tìm kiếm & Thư điện tử:**<br>- WWW là mạng lưới website chứa siêu văn bản liên kết trên Internet.<br>- Trình duyệt: Phần mềm xem web (Chrome, Edge...).<br>- Máy tìm kiếm: Công cụ tra cứu thông tin (Google...).<br>- Email: `<Tên người dùng>@<Tên máy chủ thư>`. |

### Hoạt động 2.2: Luyện giải bài tập trắc nghiệm và câu hỏi tình huống (20 phút)
a) Mục tiêu: Vận dụng kiến thức toàn học kì để giải quyết hệ thống câu hỏi trắc nghiệm và câu hỏi thực tế.
b) Nội dung: HS giải phiếu học tập ôn tập gồm 6 câu trắc nghiệm và 2 câu hỏi tình huống.
c) Sản phẩm: Lời giải chi tiết của học sinh trong phiếu học tập.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Giao phiếu bài tập ôn tập:<br>  + **Câu 1:** Đơn vị đo dung lượng nào tương đương $1024\\text{ MB}$?<br>  + **Câu 2:** Phân biệt Trình duyệt web và Máy tìm kiếm.<br>  + **Câu 3:** Một USB có dung lượng $8\\text{ GB}$, có thể chứa được bao nhiêu video bài giảng dung lượng mỗi video là $512\\text{ MB}$?<br>  + **Câu 4:** Nêu 3 biện pháp an toàn khi sử dụng thư điện tử và Internet.<br>- **HS:** Làm việc cá nhân sau đó trao đổi cặp đôi.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Độc lập làm bài. GV hướng dẫn HS tính Câu 3: Đổi $8\\text{ GB} = 8 \\cdot 1024 = 8192\\text{ MB}$, sau đó chia cho $512$.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 4 HS lên bảng trình bày 4 câu.<br>- Cả lớp nhận xét, đối chiếu kết quả.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Sửa bài chi tiết, chốt lại phương pháp giải dạng bài tính toán dung lượng nhớ. | **Đáp án bài tập ôn tập:**<br>- **Câu 1:** $1\\text{ GB} = 1024\\text{ MB}$.<br>- **Câu 2:**<br>+ Trình duyệt web: Là phần mềm cài trên máy để mở và xem các trang web (Chrome, Edge...).<br>+ Máy tìm kiếm: Là một trang web cung cấp dịch vụ tra cứu thông tin trên Internet (Google, Bing...).<br>- **Câu 3:**<br>Đổi: $8\\text{ GB} = 8 \\cdot 1024 = 8192\\text{ MB}$.<br>Số lượng video bài giảng USB có thể chứa là:<br>$8192 : 512 = 16$ (video).<br>- **Câu 4:**<br>1. Không chia sẻ mật khẩu tài khoản cho người khác.<br>2. Không nhấp vào các liên kết lạ hoặc tải tệp đính kèm không rõ nguồn gốc.<br>3. Luôn đăng xuất khỏi tài khoản khi dùng máy tính công cộng. |

## C. HOẠT ĐỘNG 3: VẬN DỤNG (8 phút)
a) Mục tiêu: Vận dụng kiến thức tìm kiếm thông tin và email để lên kế hoạch học tập nhóm hiệu quả.
b) Nội dung: Xây dựng quy trình trao đổi học tập giữa các thành viên trong nhóm ôn thi học kì bằng thư điện tử.
c) Sản phẩm: Bản quy trình 3 bước của học sinh.
d) Tổ chức thực hiện:

| Hoạt động của GV và HS | Nội dung cần đạt |
| :--- | :--- |
| **+ Bước 1: Chuyển giao nhiệm vụ**<br>- **GV:** Đặt vấn đề: Nhóm em có 4 bạn muốn cùng nhau ôn thi học kì I môn Tin học. Em hãy đề xuất cách sử dụng thư điện tử và tìm kiếm Internet để cả nhóm cùng ôn tập tốt nhất.<br>- **HS:** Tiếp nhận bài toán.<br><br>**+ Bước 2: Thực hiện nhiệm vụ**<br>- **HS:** Thảo luận cặp đôi.<br><br>**+ Bước 3: Báo cáo, thảo luận**<br>- 1 HS phát biểu: Nhóm trưởng tìm tài liệu ôn tập trên Google, sau đó soạn email đính kèm tệp gửi cho tất cả các bạn trong nhóm. Các bạn làm bài xong gửi lại để nhóm trưởng tổng hợp.<br><br>**+ Bước 4: Kết luận, nhận định**<br>- **GV:** Biểu dương ý tưởng ứng dụng công nghệ thông tin vào việc tự học nhóm. Dặn dò học sinh ôn tập kĩ theo đề cương để chuẩn bị làm bài kiểm tra cuối học kì I ở tiết sau. | **Quy trình học tập nhóm qua mạng:**<br>1. Tìm kiếm và chọn lọc học liệu số uy tín bằng máy tìm kiếm.<br>2. Soạn thư điện tử gửi tệp học liệu cho toàn bộ thành viên trong nhóm bằng chức năng gửi cho nhiều địa chỉ.<br>3. Thảo luận, phản hồi và hoàn thiện sản phẩm học tập qua email văn minh, an toàn. |
"""

# -------------------------------------------------------------
# 04. KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (Tiết 18)
# -------------------------------------------------------------
md_04 = """Tiết 18 - KIỂM TRA ĐÁNH GIÁ CUỐI HỌC KÌ I (TIN HỌC 6)
*Thời lượng thực hiện: 01 tiết (45 phút)*

# I. MỤC TIÊU
## 1. Về kiến thức
- Đánh giá toàn diện chuẩn kiến thức, kĩ năng của học sinh sau khi hoàn thành chương trình môn Tin học 6 Học kì I gồm 3 chủ đề:
  + **Chủ đề 1: Máy tính và cộng đồng** (Bài 1, 2, 3): Thông tin và dữ liệu, quá trình xử lí thông tin, dãy bit và các đơn vị đo dung lượng thông tin.
  + **Chủ đề 2: Mạng máy tính và Internet** (Bài 4, 5): Thành phần mạng máy tính, thiết bị mạng, đặc điểm và lợi ích của Internet.
  + **Chủ đề 3: Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin** (Bài 6, 7, 8): Mạng thông tin toàn cầu (WWW), Siêu văn bản và Siêu liên kết, Trình duyệt web, Máy tìm kiếm, Từ khóa, Thư điện tử (Email) và an toàn thông tin mạng.

## 2. Về năng lực
a) Năng lực chung:
- Tự chủ và tự học: Tự giác làm bài nghiêm túc, độc lập tư duy, trung thực trong kiểm tra đánh giá.

b) Năng lực đặc thù môn Tin học:
- Năng lực giải quyết vấn đề với sự hỗ trợ của công nghệ: Khả năng tư duy logic, lựa chọn công cụ số thích hợp để giải quyết tình huống thực tế.

c) Năng lực số (NLS):
- ***5.3.TC1a: HS thực hiện bài kiểm tra khảo thí số trên máy tính hoặc giấy thi nghiêm túc, đúng quy chế kiểm tra đánh giá của nhà trường.***

d) Năng lực Trí tuệ Nhân tạo (AI):
- ***6.D1.1: HS có ý thức tự lực tư duy làm bài, không sử dụng các thiết bị số thu phát tín hiệu trái phép, giữ gìn tính trung thực học thuật.***

## 3. Về phẩm chất
- Rèn luyện tính trung thực, kỷ luật, tự trọng và trách nhiệm trong học tập và thi cử.

# II. CẤU TRÚC ĐỀ KIỂM TRA

## 1. Hình thức kiểm tra
- Kết hợp Trắc nghiệm khách quan (70% - 7,0 điểm gồm 14 câu) và Tự luận (30% - 3,0 điểm gồm 2 câu).
- Thời gian làm bài: 45 phút.

## 2. Ma trận đề kiểm tra cuối HKI
- **Chủ đề 1 (Máy tính và cộng đồng):** 30% tổng điểm (Nhận biết: 2 câu TN; Thông hiểu: 2 câu TN; Vận dụng: 1 ý Tự luận tính dung lượng).
- **Chủ đề 2 (Mạng máy tính và Internet):** 30% tổng điểm (Nhận biết: 2 câu TN; Thông hiểu: 2 câu TN; Vận dụng: 1 câu TN).
- **Chủ đề 3 (Tổ chức lưu trữ, tìm kiếm và trao đổi thông tin):** 40% tổng điểm (Nhận biết: 3 câu TN; Thông hiểu: 2 câu TN; Vận dụng: 1 câu Tự luận tình huống tìm kiếm & email).

---

## 3. ĐỀ KIỂM TRA MẪU CHUẨN

### PHẦN I. TRẮC NGHIỆM KHÁCH QUAN (7,0 điểm - Mỗi câu 0,5 điểm)
*Khoanh tròn vào chữ cái đứng trước câu trả lời đúng nhất:*

**Câu 1 (NB):** Dữ liệu trong máy tính được lưu trữ dưới dạng nào?
A. Các văn bản chữ in hoa.
B. Các hình ảnh màu sắc.
C. Dãy bit gồm các số 0 và 1.
D. Các âm thanh tự nhiên.

**Câu 2 (NB):** Một Byte bằng bao nhiêu bit?
A. 2 bit.
B. 8 bit.
C. 10 bit.
D. 16 bit.

**Câu 3 (TH):** Thao tác sao chép một tệp tài liệu từ máy tính vào thẻ nhớ USB thuộc bước nào trong quá trình xử lí thông tin?
A. Thu nhận thông tin.
B. Lưu trữ thông tin.
C. Xử lí thông tin.
D. Hiển thị thông tin.

**Câu 4 (TH):** Dung lượng $1\\text{ GB}$ bằng bao nhiêu Megabyte?
A. $100\\text{ MB}$.
B. $1000\\text{ MB}$.
C. $1024\\text{ MB}$.
D. $2048\\text{ MB}$.

**Câu 5 (NB):** Thiết bị nào sau đây dùng để kết nối các máy tính với nhau bằng dây cáp mạng trong mạng nội bộ?
A. Chuột không dây.
B. Bộ chuyển mạch (Switch).
C. Bàn phím máy tính.
D. Máy quét ảnh (Scanner).

**Câu 6 (NB):** Mạng Internet là gì?
A. Là mạng kết nối các máy tính trong một phòng học.
B. Là mạng kết nối hàng triệu máy tính trên phạm vi toàn cầu.
C. Là một phần mềm máy tính hiện đại.
D. Là mạng máy tính nội bộ của cơ quan nhà nước.

**Câu 7 (TH):** Nhận định nào sau đây về mạng không dây (Wi-Fi) là đúng?
A. Sử dụng dây cáp mạng đồng trục để truyền dữ liệu.
B. Bắt buộc các máy tính phải đặt cố định, không thể di chuyển.
C. Sử dụng sóng điện từ để truyền dữ liệu, thuận tiện cho thiết bị di động.
D. Không thể kết nối với mạng Internet toàn cầu.

**Câu 8 (NB):** World Wide Web (WWW) là gì?
A. Là một loại máy tính thế hệ mới.
B. Là mạng thông tin toàn cầu, hệ thống các website liên kết trên Internet.
C. Là trò chơi điện tử trực tuyến.
D. Là một loại dây cáp mạng xuyên đại dương.

**Câu 9 (NB):** Phần mềm nào sau đây là Trình duyệt web?
A. Microsoft Word.
B. Google Chrome.
C. Windows Media Player.
D. Paint.

**Câu 10 (TH):** Đoạn văn bản hoặc hình ảnh khi nhấp chuột vào sẽ đưa người dùng chuyển sang một trang web khác được gọi là:
A. Văn bản thuần túy.
B. Siêu liên kết (Hyperlink).
C. Từ khóa tìm kiếm.
D. Tệp tin đính kèm.

**Câu 11 (TH):** Để tìm kiếm chính xác cụm từ \"Di sản văn hóa Huế\", em nên nhập từ khóa như thế nào vào máy tìm kiếm?
A. Di sản văn hóa Huế
B. \"Di sản văn hóa Huế\"
C. Di_sản_văn_hóa_Huế
D. di san van hoa hue*

**Câu 12 (NB):** Trong các địa chỉ sau, địa chỉ nào có cấu trúc là một địa chỉ thư điện tử (email) hợp lệ?
A. `www.google.com.vn`
B. `nguyenvanan@gmail.com`
C. `nguyen van an@yahoo.com`
D. `https://thieunien.vn`

**Câu 13 (TH):** Trong cửa sổ soạn thư điện tử, muốn gửi kèm một bức ảnh hoặc tệp tài liệu, em nhấp vào biểu tượng nào?
A. Biểu tượng chiếc kẹp giấy (Attach files).
B. Biểu tượng thùng rác.
C. Biểu tượng dấu nhân (Close).
D. Biểu tượng kính lúp.

**Câu 14 (VD):** Hành động nào sau đây là **KHÔNG AN TOÀN** khi sử dụng Internet?
A. Đặt mật khẩu tài khoản dài và chứa cả chữ, số, kí tự đặc biệt.
B. Đăng xuất tài khoản sau khi dùng xong ở máy tính công cộng.
C. Nhấp vào đường liên kết lạ trong email thông báo trúng thưởng để nhập thông tin cá nhân.
D. Chỉ tải tệp tin từ những trang web uy tín, chính thống.

---

### PHẦN II. TỰ LUẬN (3,0 điểm)

**Câu 1 (1,5 điểm):**
Một ổ đĩa flash USB có dung lượng lưu trữ là $16\\text{ GB}$.
a) Em hãy đổi dung lượng của chiếc USB này ra đơn vị Megabyte (MB).
b) Giả sử mỗi video bài giảng Tin học ngắn có dung lượng khoảng $256\\text{ MB}$. Hỏi chiếc USB trên có thể chứa tối đa bao nhiêu video bài giảng như vậy?

**Câu 2 (1,5 điểm):**
Bạn Hoa muốn gửi một tệp báo cáo bài tập nhóm môn Khoa học tự nhiên (dạng tệp Word dung lượng $3\\text{ MB}$) cho cô giáo chủ nhiệm qua thư điện tử.
a) Em hãy nêu các bước cụ thể để bạn Hoa có thể soạn và gửi bức thư có đính kèm tệp báo cáo cho cô giáo.
b) Nêu 2 điều bạn Hoa cần lưu ý để bức thư điện tử thể hiện sự tôn trọng, lịch sự đối với cô giáo.

---

# III. HƯỚNG DẪN CHẤM VÀ THANG ĐIỂM

## 1. Phần Trắc nghiệm (7,0 điểm - Mỗi câu đúng được 0,5 điểm)
- Câu 1: **C** | Câu 2: **B** | Câu 3: **B** | Câu 4: **C** | Câu 5: **B**
- Câu 6: **B** | Câu 7: **C** | Câu 8: **B** | Câu 9: **B** | Câu 10: **B**
- Câu 11: **B** | Câu 12: **B** | Câu 13: **A** | Câu 14: **C**

## 2. Phần Tự luận (3,0 điểm)

| Câu | Nội dung đáp án chuẩn | Điểm |
| :---: | :--- | :---: |
| **Câu 1**<br>*(1,5 đ)* | **a)** Đổi dung lượng USB sang MB:<br>Vì $1\\text{ GB} = 1024\\text{ MB}$ nên:<br>Dung lượng USB là: $16 \\cdot 1024 = 16384\\text{ MB}$.<br><br>**b)** Số lượng video bài giảng tối đa USB có thể chứa là:<br>$16384 : 256 = 64$ (video bài giảng).<br>Đáp số: $64$ video. | 0,75 đ<br><br>0,75 đ |
| **Câu 2**<br>*(1,5 đ)* | **a)** Các bước soạn và gửi thư kèm tệp báo cáo:<br>1. Đăng nhập vào hộp thư điện tử cá nhân của Hoa.<br>2. Nhấp vào nút **Soạn thư** (Compose).<br>3. Nhập chính xác địa chỉ email của cô giáo vào ô **Đến** (To).<br>4. Nhập tiêu đề thư vào ô **Chủ đề** (ví dụ: `Báo cáo bài tập nhóm KHTN - Tổ 1`).<br>5. Viết nội dung thư, nhấp biểu tượng **kẹp giấy** chọn tệp Word báo cáo tải lên.<br>6. Nhấp nút **Gửi** (Send).<br><br>**b)** 2 điều lưu ý thể hiện sự tôn trọng, lịch sự:<br>- Có lời chào mở đầu kính gửi cô giáo và lời chúc/cảm ơn ở cuối thư.<br>- Ghi rõ tiêu đề thư và tên người gửi, lớp học để cô giáo dễ nhận biết. | 0,75 đ<br><br><br><br><br><br>0,75 đ |

---

# IV. TIẾN TRÌNH TỔ CHỨC KIỂM TRA (45 phút)
1. **Ổn định lớp và phổ biến quy chế thi (3 phút):** Kiểm tra sĩ số, yêu cầu HS cất toàn bộ tài liệu, không sử dụng điện thoại và thiết bị số cá nhân.
2. **Phát đề và học sinh làm bài thi (37 phút):** HS nghiêm túc làm bài. Giám thị coi thi bao quát trật tự phòng thi.
3. **Thu bài và tổng kết (5 phút):** Thu đủ bài thi, kiểm đếm số lượng và nhận xét ý thức làm bài của học sinh.
"""

tasks = [
    ("01_Bai07_TimKiemThongTinTrenInternet_Tiet13-14.md", md_01),
    ("02_Bai08_ThuDienTu_Tiet15-16.md", md_02),
    ("03_OnTapCuoiHK1_Tin6_Tiet17.md", md_03),
    ("04_KiemTraCuoiHK1_Tin6_Tiet18.md", md_04),
]

for filename, content in tasks:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f" -> Đã tạo Markdown Tin 6: {filename}")

print(">>> HOÀN TẤT TẠO 4 TỆP MARKDOWN TIN HỌC 6 (TUẦN 13 - 18)! <<<")
