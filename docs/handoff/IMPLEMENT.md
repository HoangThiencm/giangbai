# IMPLEMENT: Sửa bot Telegram và bộ bóc tách văn bản

## Phạm vi đã thực hiện

- Tạo `api/pdf_text_extractor.php`: bóc chữ PDF thuần PHP (FlateDecode, ToUnicode CMap, Identity-H, WinAnsi). Chỉ đọc tối đa 3 trang đầu và dừng sau 1,4 giây. Không gọi `exec()`.
- `api/vanban.php` nạp module trên. `vbd_find_document_number()` nhận cả số hành chính (`03/KH-CM`, `45/QĐ-SGDĐT`) và số Đảng/đoàn thể (`193-QĐ/THCS`, `02-HD/ĐU`, `12-NQ/CB`), bỏ qua số nằm trong căn cứ.
- Thể loại ưu tiên dòng tên in hoa, rồi mã trong số hiệu, rồi cấu trúc Công văn (`Kính gửi` + `V/v`). Đã bỏ `stripos('Công văn')`. Trích yếu lấy dòng ngay dưới tên loại; Công văn lấy nội dung sau `V/v`.
- Sửa regex lĩnh vực Đảng trong `vbd_detect_sector()`: dấu `/` trong `[-/]` trước đây cắt hỏng pattern.
- `api/telegram_vanban.php`: nếu `pdftotext` không có hoặc ra dưới 30 ký tự thì gọi `vbd_pdf_extract_text()`. `$updateId` gán ngay đầu `try`. Callback nới `owner_id` (`owner_id` khớp, `0` hoặc `NULL`), trả `answerCallbackQuery` trước, nuốt lỗi Telegram `message is not modified`, và đánh dấu lĩnh vực đang chọn bằng `[• … •]`.

## Kiểm thử

- `php -l` với PHP 8.3.36 portable: `api/pdf_text_extractor.php`, `api/vanban.php`, `api/telegram_vanban.php` không lỗi cú pháp.
- `python tests/telegram-vanban-webhook-smoke.py`: đạt. Bản PDF `DỰ THẢO KE HOACH CM THANG 11.pdf` ra số `03/KH-CM`, thể loại `Kế hoạch`, trích yếu `Hoạt động chuyên môn tháng 11/2026` khi không dùng `pdftotext`.
- Cùng script kiểm số `193-QĐ/THCS`, `02-HD/ĐU`, Công văn `663/UBND-VP` và số có khoảng trắng `45 / QĐ - SGDĐT`.
- `2.11 CV 663...pdf`: có lớp chữ tiếng Việt, trích yếu gần đúng (`phối hợp tuyên truyền, vận động`). Dòng số trên file là `Số: /MTTQ-BTT` (thiếu phần số ở lớp chữ), nên số hiệu chưa ra `663`.
- `193-QĐ...pdf`: không có lớp chữ dùng được (ảnh quét), bộ bóc thuần PHP không đọc được nội dung.

## Chưa kiểm trên hosting

- Chưa gọi webhook Telegram thật, chưa bấm nút trên ứng dụng. Nhánh `message is not modified` được khóa trong mã và trong smoke test tĩnh để không còn ném HTTP 500.
- Chưa commit.

## Việc tiếp theo

Antigravity IDE, chat mới: `/verify`.
