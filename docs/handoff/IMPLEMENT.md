# IMPLEMENT

## Đã thực hiện
- Nâng cấp `giaoantichhop.html` thành công cụ công khai, hoạt động phía trình duyệt: không dùng đăng nhập, `authToken`, `access-control.js` hoặc backend.
- Bổ sung quản lý nhiều Gemini API key bằng `localStorage` (`tichhop_gemini_keys`), che khu vực nhập theo modal, nhập `.txt`, kiểm tra key, xóa key và hướng dẫn Google AI Studio.
- Bổ sung nạp/trích xuất DOCX (Mammoth), PDF (pdf.js), TXT và Markdown qua kéo-thả hoặc chọn tệp; nội dung có thể sửa trước khi gửi AI.
- Bổ sung gọi Gemini trực tiếp: ưu tiên `gemini-3.8-flash`, tự thử `gemini-2.5-flash` khi lỗi model/quá tải/hạn ngạch; xoay vòng các key đã lưu.
- Tinh gọn giao diện: ẩn hoàn toàn Markdown thô với giáo viên; giữ luồng nạp giáo án → tích hợp → xem trước → xuất Word.
- Bổ sung Smart PPCT Parser: nhận diện NLS/AI từ mã và từ khóa, hiển thị huy hiệu, tự đồng bộ mã khớp danh mục chuẩn và đưa nguyên văn PPCT vào prompt ưu tiên cao nhất.
- Bổ sung OCR PPCT bằng Gemini Vision: dán ảnh Ctrl+V, kéo-thả hoặc chọn PNG/JPG/WEBP; hiển thị thumbnail, trạng thái OCR, tự nén ảnh lớn hơn 2048px và đưa văn bản nhận diện vào Smart PPCT Parser.
- Nâng cấp `callGemini` để gửi ảnh qua `inlineData` trực tiếp đến Gemini, vẫn dùng fallback model và xoay vòng API key.
- Bổ sung thanh tiến trình, thông báo trạng thái, xuất `.doc` chứa OMML và tùy chọn `.docx`.
- Giữ danh mục/gợi ý chuẩn từ `js/khbd-standards.js`, prompt tích hợp bảo toàn nguồn, bổ sung NLS/AI ở Mục I, Mục III và bảng tổng hợp.
- Không tạo alias; công cụ được duy trì tại `giaoantichhop.html`.

## Kiểm tra
- `git diff --check`: đạt, không có lỗi whitespace.
- Kiểm tra tĩnh: không còn tham chiếu `authToken`, `access-control.js` hay nút/luồng sao chép Markdown trên giao diện.
- Xác nhận có Smart PPCT Parser với regex mã NLS/AI, nhận diện từ khóa, badge và tự tick danh mục chuẩn khi khớp.
- Kiểm tra tĩnh: có handler paste/drop/upload ảnh PPCT, preview ảnh và payload `inlineData` cho Gemini Vision.
- Trình kiểm tra cú pháp Node của môi trường bị Windows Security chặn thực thi, nên chưa chạy được kiểm tra JavaScript tự động trong phiên này.

## Chưa thực hiện
- Chưa kiểm thử gọi Gemini bằng API key thật, vì không có key của giáo viên trong workspace.

## Lưu ý phạm vi
- `tichhopgiaoan.html` không được tạo lại theo yêu cầu xóa mới nhất của người dùng, dù kế hoạch còn nêu alias này.
