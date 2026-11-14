# IMPLEMENT: Nâng cấp nhận diện số/ngày/thể loại/trích yếu văn bản bot Telegram

## Phạm vi đã thực hiện

Thực hiện theo `docs/handoff/PLAN.md` ngày 14/11/2026. Chỉ đụng `api/vanban.php`, `api/telegram_vanban.php`, `tests/telegram-vanban-webhook-smoke.py`.

1. **`api/vanban.php`**
   - `vbd_is_reference_context()`: đuôi ngữ cảnh kết thúc bằng `ngày` / `tháng` / `năm` được coi là dẫn chiếu, không lấy làm số văn bản.
   - Fallback số chỉ chạy khi 500 ký tự đầu có nhãn `Số` đứng đầu dòng và theo sau là chữ số. Số nằm ngay sau `Căn cứ`, `Thực hiện` hoặc `triển khai` bị bỏ qua ở cả ba nhánh cứu hộ.
   - Thể loại chỉ tìm trong 600 ký tự đầu (`$headForType`).
   - Có số văn bản và `Kính gửi:` mà chưa có thể loại thì gán `Công văn`.
   - `vbd_title_line_skipped()` bỏ dòng địa chỉ, email, website, điện thoại khi lấy trích yếu dưới dòng thể loại.
2. **`api/telegram_vanban.php`**
   - Thêm `tvb_parse_caption_structured()`. Sau `vbd_parse_document`, caption có cấu trúc ghi đè số, ngày, thể loại, trích yếu, cơ quan.
   - Text sau khi bóc ngắn hơn 80 ký tự và không có caption thì gửi tin hướng dẫn mẫu caption, rồi vẫn lưu văn bản.
3. **`tests/telegram-vanban-webhook-smoke.py`**
   - Thêm `date_in_context`, `type_deep`, `cv_no_vv` và assert số/thể loại.
   - Assert có `tvb_parse_caption_structured` và `$captionData`.

## Kiểm thử đã chạy

- `php -l api/vanban.php`: PASS — No syntax errors detected.
- `php -l api/telegram_vanban.php`: PASS — No syntax errors detected.
- Dùng PHP portable tại `%TEMP%/php-portable-834/php.exe`.
- `python tests/telegram-vanban-webhook-smoke.py`: PASS — telegram-vanban-webhook smoke: OK.
- `git diff --check` trên ba file trên: PASS.
- Chưa gọi webhook Telegram thật, chưa gửi file scan lên bot.

## Bàn giao

- Không sửa `PLAN.md`, không sửa `VERIFY.md`.
- `VERIFY.md` hiện tại là kết quả của phạm vi trước; cần chạy `/verify` cho kế hoạch này.
- Đã xóa `docs/handoff/.lock` trước khi sửa, tạo lại nội dung `LOCK` sau khi ghi file này.
- Chưa commit/push.
- Bước tiếp theo: Antigravity IDE, chat mới: `/verify`.
