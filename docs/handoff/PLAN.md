# PLAN

## Hiện trạng
- Trên giao diện `sualoichinhta.html`, chưa có dropdown để người dùng chủ động chọn mô hình AI (như `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`). Backend đang chạy ngầm định danh sách cố định.
- Lỗi dấu câu và khoảng cách (ví dụ `vừa qua , ban` thay vì `vừa qua, ban`) bị bỏ sót:
  + Trong `api/sualoichinhta_ai.php`, việc sử dụng hàm `trim()` cho `original_text` và `suggested_text` trước khi so sánh `$from === $to` đã vô tình loại bỏ các lỗi dấu câu thuần túy khoảng cách (ví dụ `" , "` -> `", "` bị trim thành `","` và `","`, dẫn đến `$from === $to` trả về true và bị bỏ qua).
  + Prompt chưa răn đe và hướng dẫn cụ thể về quy chuẩn khoảng trắng dấu câu tiếng Việt (dấu phẩy, chấm phải viết sát ký tự trước và có 1 khoảng trắng sau).

## Phạm vi
1. Thêm dropdown lựa chọn mô hình Gemini trên giao diện `sualoichinhta.html`:
   - Các tùy chọn: Tự động (Khuyên dùng), `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`.
   - Gửi giá trị `model` được chọn lên backend qua payload kiểm tra.
   - Hiển thị badge tên model thực tế đã xử lý kết quả kiểm tra.
2. Nâng cấp backend `api/sualoichinhta_ai.php`:
   - Tiếp nhận tham số `model` từ client, ưu tiên gọi đúng model được chọn trước khi fallback.
   - Sửa thuật toán lọc lỗi dấu câu: Không `trim()` mù quáng làm mất các lỗi khoảng cách dấu câu; chỉ loại bỏ nếu chuỗi thực sự rỗng hoặc không xuất hiện trong văn bản nguồn.
   - Bổ sung quy tắc dấu câu vào Prompt: Nêu rõ quy tắc viết liền sát ký tự trước của các dấu phẩy, chấm, hai chấm, chấm phẩy, chấm than, hỏi và có 1 khoảng trắng phân tách sau (ví dụ: `vừa qua , ban` -> `vừa qua, ban`).
3. Đảm bảo hàm vá `patchDocxText` trong `sualoichinhta.html` xử lý chuẩn xác việc thay thế chuỗi có dấu câu và khoảng trắng.

## Ngoài phạm vi
- Không thay đổi các chức năng khác của hệ thống phân quyền trong `access-control.js` hay `admin.html`.
- Không thay đổi schema cơ sở dữ liệu.

## File dự kiến tác động
- `sualoichinhta.html`
- `api/sualoichinhta_ai.php`

## Các bước thực hiện
1. Bước 1: Cập nhật backend `api/sualoichinhta_ai.php`:
   - Tiếp nhận `$body['model']`. Xây dựng danh sách `$models` với model người dùng chọn ở đầu danh sách.
   - Bổ sung chỉ dẫn dấu câu tiếng Việt vào `$prompt`.
   - Điều chỉnh logic lọc lỗi để bảo toàn các lỗi sửa khoảng trắng và dấu câu (không để `trim()` triệt tiêu sự khác biệt về khoảng trắng).
2. Bước 2: Cập nhật giao diện `sualoichinhta.html`:
   - Thêm dropdown `<select id="modelSelect">` cạnh tùy chọn kiểm tra với các model Gemini phổ biến.
   - Gửi `model` lên trong hàm gọi API kiểm tra.
   - Cập nhật hiển thị tên model xử lý trong `#resultSummary`.
3. Bước 3: Kiểm thử:
   - Kiểm tra đoạn văn có lỗi `vừa qua , ban`: Xác nhận AI phát hiện và gợi ý thành `vừa qua, ban`.
   - Thử nghiệm chuyển đổi các model trong dropdown và xác nhận backend gọi đúng model tương ứng.

## Rủi ro
- Một số model (như `gemini-1.5-pro`) có thể chậm hơn dòng flash đối với văn bản dài: Có thông báo trạng thái rõ ràng trên giao diện.
- Tránh thay thế nhầm các dấu phẩy trong số thập phân (`3,14`): Đã có hướng dẫn ngữ cảnh trong prompt.

## Cách kiểm thử
1. Kiểm tra cú pháp JavaScript của `sualoichinhta.html` bằng Node.js.
2. Kiểm thử kiểm tra dấu câu với văn bản mẫu:
   - Nhập `Trong năm học vừa qua , ban giám hiệu`.
   - Nhấn kiểm tra: AI phải phát hiện lỗi tại `vừa qua , ban` và đề xuất `vừa qua, ban`.
   - Nhấn áp dụng và tải file Word: Xác nhận file Word kết quả đã mất khoảng trắng trước dấu phẩy.
3. Kiểm thử dropdown model:
   - Chọn `gemini-2.5-flash` và kiểm tra response trả về đúng model `gemini-2.5-flash`.
   - Chọn `gemini-2.0-flash` và xác nhận response trả về `gemini-2.0-flash`.

## Tiêu chí nghiệm thu
- Trên giao diện có dropdown chọn mô hình AI trực quan, hoạt động chuẩn xác.
- Lỗi khoảng cách dấu câu như `vừa qua , ban` hoặc `Tuy nhiên ,với` được AI phát hiện 100% và sửa thành `vừa qua, ban`, `Tuy nhiên, với`.
- Sau khi áp dụng và tải file Word `.docx`, lỗi dấu câu được sửa sạch sẽ trong tài liệu.
