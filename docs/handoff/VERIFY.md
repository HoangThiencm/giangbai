# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `api/pdf_text_extractor.php`:
  - `vbd_pdf_annot_texts()` đệ quy duyệt `/Annots -> /AP /N` và các Form XObject lồng nhau, giải mã nội dung stream theo đúng font map.
  - Chèn dòng `ANNOT_TEXT:` vào text trang, trích xuất chính xác số `7400` và ngày `12` từ lớp chữ ký số VNPT-CA.
- `api/vanban.php`:
  - `vbd_find_document_number()` tự động ghép số từ annotation `7400` vào đuôi `/KH-SGDĐT` thành `7400/KH-SGDĐT`.
  - Tiêu ngữ khuyết số ngày tự động nhận ngày `12` từ annotation thành `2026-11-12`.
- `api/telegram_vanban.php`:
  - Xóa bỏ hoàn toàn wizard hỏi 5 bước, bảng `office_telegram_edits`, nút `Sửa từng mục`, và callback `e:`.
  - Thêm hàm `tvb_recent_previous_document()` tìm văn bản gần nhất trong vòng 30 phút của cùng người dùng.
  - Khi có văn bản trước, bàn phím tự động hiển thị nút 1 chạm: `📎 Ghép vào VB trước (#<prevId>)`.
  - Callback `merge:id:prevId` di chuyển tệp trong `office_document_files`, xóa bản ghi văn bản thừa, phản hồi alert và cập nhật tin nhắn gọn gàng.
- `tests/telegram-vanban-webhook-smoke.py`:
  - Cập nhật kiểm tra bóc tách `7400/KH-SGDĐT` và hợp đồng `merge:(\d+):(\d+)`.

## Test đã chạy
1. Syntax check:
   - `php -l api/pdf_text_extractor.php`: No syntax errors detected.
   - `php -l api/vanban.php`: No syntax errors detected.
   - `php -l api/telegram_vanban.php`: No syntax errors detected.
2. Smoke test:
   - `python tests/telegram-vanban-webhook-smoke.py`: `telegram-vanban-webhook smoke: OK`.
3. Kiểm thử trực tiếp với tệp mẫu thực tế `KH THI GIÁO VIÊN DẠY GỎI THCS - 2026-2027 pH.pdf`:
   - `document_number`: `7400/KH-SGDĐT` — PASS.
   - `document_type`: `Kế hoạch` — PASS.
   - `document_date`: `2026-11-12` — PASS.
   - `title`: `Tổ chức Hội thi giáo viên dạy giỏi cơ sở giáo dục Trung học cơ sở cấp thành phố năm học 2026 - 2027` — PASS.

## Pass / Fail từng tiêu chí
- [x] Bóc tách trọn vẹn số hiệu `7400/KH-SGDĐT` từ lớp Annotation chữ ký số — PASS
- [x] Bóc tách ngày ban hành `2026-11-12` — PASS
- [x] Bóc tách thể loại `Kế hoạch` — PASS
- [x] Bóc tách trích yếu `Tổ chức Hội thi giáo viên dạy giỏi...` — PASS
- [x] Bỏ hoàn toàn luồng hỏi 5 bước rườm rà trên Telegram — PASS
- [x] Hỗ trợ nút 1 chạm `📎 Ghép vào VB trước (#ID)` gộp phụ lục/văn bản kèm theo — PASS

## Bug
Không phát hiện lỗi.
