# PLAN

## Hiện trạng
- Giao diện hiện tại của `giaoantichhop.html` bị phản hồi là rườm rà, chưa tối ưu trải nghiệm người dùng:
  + Vẫn còn nút "Sao chép Markdown" và khung dán Markdown gây hiểu lầm người dùng phải xử lý mã nguồn thô, trong khi mục tiêu là nhận giáo án gốc, AI chèn nội dung tích hợp và xuất thẳng ra Word có công thức Equation (OMML).
  + Chưa có cơ chế nhận diện tự động thông minh khi giáo viên dán nội dung Phân phối chương trình (PPCT) có sẵn ghi chú tích hợp NLS và AI.
  + Bố cục hiển thị nhiều ô nhập liệu rời rạc, thiếu tính liền mạch của quy trình nghiệp vụ giáo viên.
- Điểm mạnh sẵn có cần giữ vững:
  + Công nghệ xuất Word có công thức Microsoft Word Equation (OMML `<m:oMath>`) chỉnh sửa được 100%.
  + Cơ chế gọi Gemini API trực tiếp phía client (ưu tiên `gemini-3.8-flash`, tự động fallback sang `gemini-2.5-flash`), xoay vòng key, lưu an toàn tại `localStorage` không cần đăng nhập tài khoản.
  + Bộ thư viện chuẩn: `mammoth.js` (đọc DOCX), `pdf.js` (đọc PDF), `js/khbd-standards.js` (chuẩn TT 02 / CV 3456 và QĐ 2422).

## Phạm vi
1. **Thiết kế lại giao diện tinh gọn, chuyên nghiệp, hiện đại (loại bỏ hoàn toàn rườm rà):**
   - Ẩn hoàn toàn khái niệm Markdown đối với người dùng cuối: Không còn nút "Sao chép Markdown", không bắt người dùng nhìn mã markdown thô.
   - Bố cục 2 cột rõ ràng, trực quan:
     + **Cột trái (Thiết lập & Dữ liệu đầu vào):**
       * Khối 1: Nạp giáo án gốc (Dropzone kéo thả DOCX/PDF/TXT tinh gọn, xem nhanh tệp đã nạp).
       * Khối 2: Thông tin bài dạy gọn gàng trên 1 hàng (Môn, Lớp 6–9, Tên bài, Thời lượng tiết).
       * Khối 3: **Khu vực Dán & Nhận diện PPCT thông minh (Trọng tâm mới):** Ô dán nguyên văn tiến trình/ghi chú PPCT; bộ nhận diện tự động bóc tách mã/nội dung NLS và AI; hiển thị huy hiệu (tags/pills) kết quả nhận diện trực quan; cho phép chọn thêm chuẩn chính thức nếu PPCT chưa đủ mã.
       * Khối 4: Nút hành động duy nhất: **"⚡ BẮT ĐẦU TÍCH HỢP VÀO GIÁO ÁN"** kèm thanh tiến trình thời gian thực.
     + **Cột phải (Xem trước A4 & Xuất Word trực tiếp):**
       * Xem trước trang giấy in A4 sống động: Hiển thị nguyên văn giáo án đã chèn tích hợp Mục I (NLS xanh lá, AI tím), Mục III (các hoạt động với marker chuẩn thực chiến) và Bảng tổng hợp cuối bài.
       * Công thức toán học render KaTeX sắc nét chuẩn thể thức.
       * Nút xuất bản chính: **"📥 Xuất file Word (.doc có Equation OMML)"** và nút **"Xuất .docx"**.
   - Quản lý API Key: Nút nhỏ gọn trên Header `🔑 Gemini API Key`, modal nhập key có che mờ và kiểm tra tính hợp lệ, lưu `localStorage`.

2. **Cơ chế Nhận diện Tự động từ PPCT (Smart PPCT Parser):**
   - Cho phép giáo viên dán văn bản phân phối chương trình có ghi chú tích hợp (ví dụ: `Tiết 12: Hình chóp - NLS: [1.1.TC2a] tìm kiếm thông tin; AI: [8.A1.2] kiểm chứng nguồn tin`).
   - Tự động nhận diện từ khóa, mã hiệu và nội dung:
     + Phát hiện phần NLS (`NLS`, `Năng lực số`, `TT 02`, `CV 3456`, các mã `1.1.TC...`, `TC...`).
     + Phát hiện phần AI (`AI`, `Trí tuệ nhân tạo`, `QĐ 2422`, các mã `6.A...`, `7.A...`, `8.A...`, `9.A...`).
   - Tự động đồng bộ sang danh mục chuẩn và đưa toàn bộ nội dung PPCT làm chỉ thị ràng buộc ưu tiên cao nhất cho AI.

3. **Chèn trực tiếp vào giáo án & Xuất Word có công thức Equation OMML:**
   - AI xử lý và chèn trực tiếp các đoạn tích hợp vào giáo án gốc:
     + Mục I: Nối `c) Năng lực số` và `d) Năng lực AI` (bảo toàn tuyệt đối a/b).
     + Mục III: Chèn các khối tích hợp thực chiến dưới hoạt động tương ứng (kèm marker, nhiệm vụ học sinh, sản phẩm minh chứng, kiểm chứng an toàn).
     + Cuối bài: Chèn Bảng tổng hợp tích hợp chuẩn 4 cột.
   - Xuất file Word `.doc` với công thức toán dạng Microsoft Word Equation (OMML) chỉnh sửa được trực tiếp bằng Equation Editor trong Word.

## Ngoài phạm vi
- Không giữ các nút hay giao diện hiển thị Markdown gây rối người dùng.
- Không sửa đổi bất kỳ file nào thuộc `soankhbd.html` hoặc thư viện hệ thống khác.
- Không yêu cầu đăng nhập tài khoản.

## File dự kiến tác động
- `giaoantichhop.html`: Tái cấu trúc toàn bộ giao diện và logic theo hướng tinh gọn, thông minh, loại bỏ rườm rà.
- `tichhopgiaoan.html`: Đồng bộ chuyển hướng sang `giaoantichhop.html`.

## Các bước thực hiện
### Bước 1: Thiết kế lại giao diện UI/UX hiện đại, tinh giản
- Bỏ các nút sao chép Markdown, bỏ các nhãn kỹ thuật không cần thiết.
- Tinh chỉnh header với màu sắc thanh lịch, nút quản lý API key gọn gàng.
- Thiết kế Dropzone nhỏ gọn kết hợp thông tin bài học cô đọng.
- Thiết kế ô nhập PPCT nổi bật kèm khu vực hiển thị kết quả nhận diện tự động (badges màu xanh cho NLS, màu tím cho AI).
- Nút xuất file Word `.doc OMML` và `.docx` đặt nổi bật ngay trên đầu khung xem trước A4.

### Bước 2: Phát triển Bộ nhận diện PPCT thông minh (Smart PPCT Parser)
- Viết hàm `parsePpctIntegration(text)`:
  + Tự động quét và phát hiện các mẫu NLS: mã `\d+\.\d+\.TC\d+[a-z]?`, từ khóa "năng lực số", "NLS", "công cụ số", "phần mềm".
  + Tự động quét và phát hiện các mẫu AI: mã `\d+\.[A-D]\d+(?:\.[A-Z0-9]+)?`, từ khóa "trí tuệ nhân tạo", "AI", "kiểm chứng", "prompt".
  + Khớp với danh mục `js/khbd-standards.js` để tự động tick chọn mã tương ứng.
  + Cập nhật huy hiệu hiển thị trực quan cho giáo viên thấy ngay kết quả nhận diện.

### Bước 3: Nâng cấp luồng xử lý AI tự động chèn vào giáo án
- Khi giáo viên bấm "⚡ Bắt đầu tích hợp vào giáo án":
  + Lấy giáo án gốc từ tệp tải lên (DOCX/PDF/TXT).
  + Tạo prompt tích hợp chuẩn CV 5512, TT 02 (CV 3456) và QĐ 2422, gắn thông tin bóc tách từ PPCT làm ưu tiên cao nhất.
  + Gọi `callGemini`: Ưu tiên `gemini-3.8-flash`, tự động fallback sang `gemini-2.5-flash` nếu quá tải/hạn ngạch, tự động xoay vòng key.
  + Nhận kết quả và cập nhật ngay vào khung xem trước A4 (được tô màu chuẩn NLS xanh lá, AI tím, công thức toán KaTeX).

### Bước 4: Tối ưu bộ xuất Word Equation OMML
- Đảm bảo toàn bộ công thức toán `$ ... $` và `$$ ... $$` trong giáo án đã tích hợp được chuyển thành `<m:oMath>` / `<m:oMathPara>` chuẩn Microsoft Word Equation.
- Khi người dùng bấm nút Xuất Word, tải ngay file `.doc` chuẩn in ấn A4 (Times New Roman 13pt, căn lề 2-1.5-1.5-1.5cm, bảng biểu viền nét đơn, công thức toán sửa được bằng Equation Editor).

### Bước 5: Kiểm thử và hoàn thiện
- Thử nghiệm kéo thả tệp DOCX/PDF.
- Thử nghiệm dán PPCT có ghi chú NLS/AI và xác nhận bộ nhận diện hoạt động chính xác.
- Thử nghiệm gọi AI, xem trước A4 và xuất Word OMML.

## Rủi ro
- Định dạng PPCT do mỗi trường/giáo viên viết có thể khác nhau:
  + Biện pháp: Dùng regex mềm dẻo kết hợp từ khóa; hiển thị kết quả nhận diện dạng badges cho phép giáo viên bấm chỉnh sửa hoặc chọn thêm mã từ danh mục chuẩn nếu muốn.
- Giáo viên chưa có API Key Gemini:
  + Biện pháp: Hiển thị hướng dẫn ngắn gọn, trực quan kèm link mở Google AI Studio tạo key miễn phí trong 1 phút.

## Cách kiểm thử
1. Kiểm tra giao diện: Giao diện sạch sẽ, hiện đại, không còn chữ/nút Markdown rườm rà.
2. Kiểm tra nhận diện PPCT: Dán đoạn PPCT có ghi chú NLS/AI -> Hệ thống tự động nhận diện đúng mã và nội dung tích hợp, hiển thị badges tương ứng.
3. Kiểm tra nạp giáo án: Kéo thả file DOCX/PDF -> Hệ thống đọc được nội dung bài dạy.
4. Kiểm tra gọi AI: Bấm nút tích hợp -> Hệ thống gọi Gemini 3.8 (fallback 2.5), hiển thị thanh tiến trình.
5. Kiểm tra chèn tích hợp: Giáo án sau tích hợp có đủ Mục I (NLS c, AI d), Mục III (các hoạt động với marker chuẩn), Bảng tổng hợp cuối bài.
6. Kiểm tra xuất Word: File Word tải về mở bằng Microsoft Word có công thức Equation OMML chỉnh sửa được 100%.

## Tiêu chí nghiệm thu
- Giao diện tinh gọn, chuyên nghiệp, không rườm rà, loại bỏ hoàn toàn các yếu tố Markdown thô.
- Có ô dán PPCT và tự động nhận diện thông minh nội dung tích hợp NLS & AI từ PPCT.
- Chèn trực tiếp nội dung tích hợp vào giáo án và hiển thị xem trước trực quan A4.
- Xuất file Word có công thức Microsoft Word Equation (OMML) chỉnh sửa được.
- Chạy hoàn toàn độc lập, không cần đăng nhập, bảo mật API key cá nhân tại `localStorage`.
- Không ảnh hưởng đến `soankhbd.html`.
