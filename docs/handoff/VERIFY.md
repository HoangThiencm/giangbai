# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `api/pdf_text_extractor.php`: Thêm ngắt dòng `$newline()` tại toán tử `BT` và `ET`, đưa timestamp chữ ký số vào đầu text để không bị trôi khỏi cửa sổ xử lý.
- `api/vanban.php`:
  - `vbd_find_document_number()`: nhận diện số hiệu khuyết chữ số đầu (`/KH-SGDĐT`), chặn triệt để số hiệu từ các trích dẫn/căn cứ (`4200/SGDĐT-GDPT`, `1170/SGDĐT-GDPT`, `2019/TT-BGDĐT`).
  - Tiêu ngữ khuyết ngày `ngày tháng 11 năm 2026`: ưu tiên lấy ngày ký số điện tử (`2026-11-12`). Chặn lấy ngày từ các đoạn căn cứ dẫn chiếu (`2019-12-20`).
  - `vbd_match_type_line()` & `vbd_title_below_type()`: nhận diện đúng thể loại `Kế hoạch` và trích yếu `Tổ chức Hội thi giáo viên dạy giỏi...` tối đa 3 dòng liên tiếp.
- `api/telegram_vanban.php`:
  - `tvb_summary()`: bổ sung dòng `<b>Thể loại:</b>` ngay sau `Lĩnh vực`.
  - Phản hồi khi đổi lĩnh vực: gửi tin nhắn xác nhận chuyển lĩnh vực.
  - Phản hồi khi xác nhận: hiển thị modal alert (`show_alert => true`) và gửi tin nhắn xác nhận vào chat.

## Test đã chạy
1. Syntax lint PHP:
   - `php -l api/pdf_text_extractor.php` (PHP 8.3.36): No syntax errors detected.
   - `php -l api/telegram_vanban.php` (PHP 8.3.36): No syntax errors detected.
   - `php -l api/vanban.php` (PHP 8.3.36): No syntax errors detected.
2. Smoke test:
   - `python tests/telegram-vanban-webhook-smoke.py`: `telegram-vanban-webhook smoke: OK`.
3. Kiểm tra với tệp PDF thực tế (`KH_THI_GIÁO_VIÊN_DẠY_GỎI_THCS_-_2026-2027_pH.pdf`):
   - Đạt 100% các tiêu chí.

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Nhận diện thể loại `Kế hoạch` từ văn bản thực tế — PASS
- [x] Tiêu chí 2: Trích yếu `Tổ chức Hội thi giáo viên dạy giỏi cơ sở giáo dục Trung học cơ sở cấp thành phố năm học 2026 - 2027` (không bị fallback về tên tệp Telegram) — PASS
- [x] Tiêu chí 3: Ngày ban hành nhận `2026-11-12` (ngày ký số), không bị nhầm thành `2019-12-20` của Thông tư 22 — PASS
- [x] Tiêu chí 4: Số hiệu văn bản nhận `/KH-SGDĐT`, không bị nhầm thành `4200/SGDĐT-GDPT` của Công văn thực hiện — PASS
- [x] Tiêu chí 5: Tin nhắn tóm tắt Telegram hiển thị dòng `Thể loại` — PASS
- [x] Tiêu chí 6: Phản hồi rõ ràng (tin nhắn xác nhận và alert) khi bấm nút menu trên Telegram — PASS

## Bug
Không phát hiện lỗi.

## Sửa từng mục (yêu cầu thêm sau plan)
Chưa nằm trong các tiêu chí trên. Phiếu có nút `Sửa từng mục`. Khi thiếu thể loại, số hiệu, hoặc trích yếu chỉ còn tên tệp, bot hỏi lần lượt từng mục kèm giá trị đang đề xuất. Chưa bấm thử trên Telegram thật.
