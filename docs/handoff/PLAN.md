# PLAN

## Hiện trạng
- Trang `sualoichinhta.html` hiện tại khi xử lý sửa lỗi xong chỉ cung cấp nút tải file `.txt` (`van-ban-da-sua.txt`).
- Khi người dùng tải lên tệp Word (`.docx`), trang chỉ trích xuất text thô bằng `JSZip` rồi bỏ tệp zip gốc, khiến người dùng không thể nhận lại tệp Word đã sửa với đầy đủ định dạng ban đầu (font chữ, cỡ chữ, căn lề, bảng biểu, màu sắc).

## Phạm vi
1. Nâng cấp cơ chế quản lý tệp Word trong `sualoichinhta.html`:
   - Lưu trữ đối tượng `loadedDocxZip` (`JSZip`) và `loadedFileName` khi người dùng tải lên tệp `.docx`.
   - Giữ nguyên cấu trúc các đoạn văn `<w:p>` khi trích xuất hiển thị trên khung soạn thảo.
2. Đồng bộ hóa việc sửa lỗi vào tệp Word gốc (Patch XML):
   - Khi người dùng nhấn "Áp dụng" từng lỗi hoặc "Áp dụng tất cả", hệ thống thay thế chuỗi lỗi `original_text` bằng `suggested_text` đồng thời trên khung soạn thảo và trực tiếp vào tệp `word/document.xml` của `loadedDocxZip`.
   - Đảm bảo việc thay thế không làm hỏng thẻ cấu trúc OpenXML (escape ký tự đặc biệt `&`, `<`, `>`).
3. Chức năng xuất tệp Word (`.docx`):
   - Nếu có tệp `.docx` gốc tải lên: Đóng gói lại `loadedDocxZip` thành tệp `.docx` (dùng `generateAsync({ type: 'blob' })`) và tải về với tên `<ten_file>_da_sua.docx`. Toàn bộ định dạng, bảng biểu, lề trang và bố cục gốc được giữ nguyên 100%.
   - Nếu người dùng nhập/dán văn bản trực tiếp (hoặc file `.txt`): Tự động tạo tệp `.docx` chuẩn bằng OpenXML template (font Times New Roman 13pt, dãn dòng 1.25, lề chuẩn A4) thông qua `JSZip` để xuất file `.docx`.
4. Cải tiến giao diện người dùng:
   - Thêm nút "Tải file Word (.docx)" nổi bật kèm biểu tượng Word.
   - Thêm nút phụ "Tải .txt" cho người dùng khi có nhu cầu lưu text trơn.
   - Hiển thị badge trạng thái tệp gốc (ví dụ: `Đang xử lý: Van_Ban_Test_Loi_Chinh_Ta.docx`).

## Ngoài phạm vi
- Không thay đổi backend API `api/sualoichinhta_ai.php` (API chỉ tiếp nhận text và trả về JSON danh sách lỗi).
- Không can thiệp vào cơ chế phân quyền trong `access-control.js` hay `admin.html`.

## File dự kiến tác động
- `sualoichinhta.html`

## Các bước thực hiện
1. Bước 1: Khảo sát và nâng cấp hàm xử lý tệp trong `sualoichinhta.html`:
   - Tạo biến trạng thái `loadedDocxZip`, `loadedDocxXml`, `loadedFileName`.
   - Khi tải `.docx`: nạp qua `JSZip.loadAsync(file)`, lưu trữ XML gốc, trích xuất text có ngắt đoạn rõ ràng vào `#sourceText`, cập nhật nhãn tên tệp.
2. Bước 2: Nâng cấp hàm `applyOne()` và `applyAll()`:
   - Cập nhật `#sourceText` và mảng lỗi `errors`.
   - Nếu có `loadedDocxZip`, cập nhật chuỗi thay thế tương ứng trong `word/document.xml`.
3. Bước 3: Xây dựng hàm tạo file Word chuẩn từ văn bản thuần (Fallback generator):
   - Dùng `JSZip` tạo cấu trúc docx gồm `[Content_Types].xml`, `_rels/.rels`, `word/_rels/document.xml.rels`, `word/document.xml` với style Times New Roman 13pt.
4. Bước 4: Nâng cấp nút tải file:
   - Đổi nút tải chính thành "Tải file Word (.docx)" (`#downloadDocx`).
   - Thêm nút "Tải .txt" (`#downloadTxt`).
5. Bước 5: Kiểm thử:
   - Tải file Word mẫu `Van_Ban_Test_Loi_Chinh_Ta.docx` trên Desktop lên trang.
   - Bấm quét lỗi và áp dụng sửa.
   - Tải file Word về, mở và kiểm tra định dạng bảng biểu, font chữ được bảo toàn 100%.

## Rủi ro
- Từ lỗi bị ngắt giữa các thẻ run `<w:r>` trong Word XML (ví dụ: một phần in đậm, một phần thường): Xử lý thay thế an toàn trên cấp độ chuỗi văn bản và các thẻ `<w:t>`.
- Ký tự đặc biệt XML (`&`, `<`, `>`): Cần escape chuẩn xác khi đưa vào XML để tránh làm hỏng file docx.

## Cách kiểm thử
1. Kiểm tra cú pháp JavaScript của `sualoichinhta.html` bằng Node.js.
2. Kiểm tra luồng tải lên `.docx`:
   - Tải tệp `.docx` có bảng biểu và định dạng.
   - Nhấn kiểm tra và áp dụng sửa.
   - Nhấn tải file Word `.docx` và kiểm tra tệp sinh ra có thể giải nén/đọc được đầy đủ cấu trúc XML chuẩn.
3. Kiểm tra luồng nhập văn bản thuần:
   - Dán text vào ô nhập, nhấn tải file Word và xác nhận tải về được tệp `.docx` hợp lệ.

## Tiêu chí nghiệm thu
- Tải lên tệp Word (`.docx`) ➔ Sửa lỗi ➔ Tải về tệp Word (`.docx`) giữ nguyên định dạng, bảng biểu, layout gốc.
- Nhập text trực tiếp ➔ Vẫn có thể xuất ra file Word (`.docx`) chuẩn Times New Roman 13pt.
- Giữ thêm tùy chọn tải file `.txt` cho người dùng cần văn bản thuần.
