# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Trích xuất PDF có lớp chữ trên hosting không có `pdftotext`:** Đạt. Đã tạo `api/pdf_text_extractor.php` xử lý thuần PHP qua core zlib (`FlateDecode`, `ToUnicode` CMap, font `Identity-H`, `WinAnsiEncoding`, khối `ObjStm`). Tự động ngắt an toàn sau tối đa 3 trang hoặc 1,4 giây, không gọi `exec()`. Đã nạp vào `api/vanban.php` và tích hợp làm fallback cấp 1 cho `tvb_extract_text()` trong `api/telegram_vanban.php`.
2. **Nhận diện số, thể loại và trích yếu văn bản:** Đạt.
   - Số hiệu: `vbd_find_document_number()` nhận đúng cả số hành chính (`03/KH-CM`, `45/QĐ-SGDĐT`) và số Đảng/đoàn thể theo Hướng dẫn 05 (`193-QĐ/THCS`, `02-HD/ĐU`, `12-NQ/CB`), bỏ qua các số trích dẫn trong căn cứ.
   - Thể loại: Ưu tiên dòng tên loại in hoa độc lập (`KẾ HOẠCH`, `QUYẾT ĐỊNH`...), mã trong số hiệu, rồi mới đến cấu trúc Công văn (`Kính gửi` + `V/v`). Đã loại bỏ hoàn toàn việc dùng `stripos('Công văn')` duyệt trước.
   - Trích yếu: Tự động trích dòng nội dung ngay dưới tên loại đối với văn bản có tên loại, và lấy nội dung sau `V/v` đối với Công văn.
3. **Sửa lỗi 500 khi bấm nút Chuyên môn trên Telegram:** Đạt.
   - Bắt và nuốt an toàn ngoại lệ `message is not modified` từ Telegram API trong `tvb_edit_callback_message()`.
   - Luôn trả `answerCallbackQuery` popup trước cho người dùng.
   - Nới lỏng điều kiện kiểm tra chủ sở hữu: `id=? AND (owner_id=? OR owner_id=0 OR owner_id IS NULL)`.
   - Gán `$updateId` ngay đầu khối `try` của webhook để log đầy đủ.
   - Hiển thị dấu chọn trực quan lĩnh vực hiện tại: `[• 🎓 Chuyên môn •]`.

## Test đã chạy
1. **Kiểm tra cú pháp PHP 8.3 (`php -l`):**
   - `api/pdf_text_extractor.php` -> No syntax errors detected.
   - `api/vanban.php` -> No syntax errors detected.
   - `api/telegram_vanban.php` -> No syntax errors detected.
2. **Smoke test tĩnh và runtime (`python tests/telegram-vanban-webhook-smoke.py`):**
   - Kết quả: `telegram-vanban-webhook smoke: OK`.
   - Trích xuất trực tiếp tệp PDF thực tế `DỰ THẢO KE HOACH CM THANG 11.pdf` bằng module thuần PHP: đạt 2102 ký tự, tiếng Việt chuẩn, nhận đúng số hiệu `03/KH-CM`, thể loại `Kế hoạch`, trích yếu `Hoạt động chuyên môn tháng 11/2026`.
   - Kiểm tra các mẫu regex: `03 / KH - CM`, `193-QĐ/THCS`, `02-HD/ĐU`, `663/UBND-VP`, `45 / QĐ - SGDĐT` đều bóc tách đúng số hiệu, thể loại và trích yếu.
   - Kiểm tra cấu trúc Webhook contract: gán `$updateId` trước callback, `answerCallbackQuery` chạy trước `editMessageText`, bắt lỗi `message is not modified`, nới lỏng `owner_id`.

## Pass / Fail từng tiêu chí
- [x] Pass: Bóc tách text PDF có lớp chữ bằng PHP thuần khi không có `pdftotext`.
- [x] Pass: Nhận diện chính xác số hiệu hành chính và số hiệu Đảng/đoàn thể.
- [x] Pass: Nhận diện đúng thể loại Kế hoạch/Quyết định, không bị gán nhầm thành Công văn vì căn cứ viện dẫn.
- [x] Pass: Nhận diện đúng trích yếu văn bản có tên loại (nằm dưới tên loại).
- [x] Pass: Không còn văng HTTP 500 khi bấm nút Chuyên môn hoặc bấm lại nút lĩnh vực hiện tại trên Telegram.
- [x] Pass: Toàn bộ kiểm thử tự động đạt 100%.

## Bug
Không phát hiện lỗi tồn đọng trong phạm vi đã triển khai.
