# IMPLEMENT: Chuẩn hóa nhận diện số văn bản

## Phạm vi đã thực hiện

Thực hiện theo `docs/handoff/PLAN.md` hiện tại, ngày 13/11/2026.

1. **`api/vanban.php`**
   - Ưu tiên nhận diện số có năm ở giữa, có hoặc không có nhãn Số: `93/2026/TT-BGDĐT`.
   - Bổ sung `&` trong mã cơ quan, giữ đủ `4200/SGDĐT-GDPT&GDTX` và `7037/SGDĐT-GDPT&GDTX`.
   - Giữ hậu tố ghép của văn bản Đảng: `193-QĐ/QU-THCS`; giữ các mẫu `193-QĐ/THCS`, `02-HD/ĐU`.
   - Bổ sung loại trừ ngữ cảnh địa chỉ theo các từ khóa và cửa sổ 40 ký tự trong kế hoạch.
   - Chuẩn hóa khoảng trắng quanh `/`, `-`, `&`.
2. **`api/pdf_text_extractor.php`**
   - Tăng deadline bóc tách từ 1.4 lên 3.0 giây.
   - Truyền thứ tự trang đến bộ đọc annotation; bỏ annotation từ trang 3, vẫn đọc nội dung trang đó theo maxPages.
3. **`tests/telegram-vanban-webhook-smoke.py`**
   - Thêm kiểm thử số cấp Bộ, phòng ban ghép, hậu tố văn bản Đảng, mẫu không có nhãn Số, địa chỉ cùng số văn bản và địa chỉ đơn thuần.
   - Kiểm tra chuẩn hóa khoảng trắng và các từ khóa địa chỉ.
   - Thêm PDF tổng hợp ba trang để xác nhận chỉ đọc annotation hai trang đầu, vẫn giữ nội dung trang 3.
   - Giữ kiểm thử PDF hội thi thực tế và các kiểm thử cũ.

## Kiểm thử đã chạy

- `php -l api/vanban.php`: PASS — No syntax errors detected.
- `php -l api/pdf_text_extractor.php`: PASS — No syntax errors detected.
- Dùng PHP portable tại `%TEMP%/php-portable-834/php.exe`.
- `python tests/telegram-vanban-webhook-smoke.py`: PASS — telegram-vanban-webhook smoke: OK. Bao gồm PDF dự thảo và PDF hội thi thực tế: số `7400/KH-SGDĐT`, ngày `2026-11-12`, thể loại và trích yếu đúng.
- `git diff --check`: PASS.

## Bàn giao

- Không sửa `PLAN.md` (thay đổi sẵn của người dùng), không sửa `VERIFY.md`.
- `VERIFY.md` hiện tại là kết quả PASS của phạm vi trước; cần chạy `/verify` cho kế hoạch này.
- Không có `.lock` khi bắt đầu, không gặp hook chặn sửa.
- Chưa commit/push.
- Bước tiếp theo: Antigravity IDE, chat mới: `/verify`.
