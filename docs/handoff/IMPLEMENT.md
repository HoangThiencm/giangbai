# IMPLEMENT: Nhận diện số, thể loại, cơ quan từ nội dung, tên tệp và caption

## Phạm vi đã thực hiện

Thực hiện theo `docs/handoff/PLAN.md` ngày 14/11/2026. Chỉ đụng `api/vanban.php`, `api/telegram_vanban.php`, `tests/telegram-vanban-webhook-smoke.py`.

1. **`api/vanban.php`**
   - `vbd_is_reference_context()` chỉ coi là địa chỉ nhà khi có `Địa chỉ`/`Trụ sở` hoặc tên đường, ngõ, hẻm, ấp, khu phố, phố. `THÀNH PHỐ`, `THỊ PHỐ`, `HÀNH PHỐ` không còn chặn số văn bản. Thêm cụm `triển khai Kế hoạch/Công văn/Quyết định số`.
   - `vbd_find_document_number()` chỉ quét 700 ký tự đầu, gom ứng viên, ưu tiên nhãn `Số:` rồi vị trí sớm nhất, bỏ số ngày `dd/mm`, ghép annotation, và nối ký hiệu bị ngắt dòng như `S` / `GDĐT` / `-` / `VP`.
   - Thêm `vbd_parse_from_name_and_caption()`: tên tệp `93_2026_TT_BGDDT.signed.pdf` ra `93/2026/TT-BGDĐT`, `Thông tư`, `Bộ Giáo dục và Đào tạo`; dạng `265_KH_UBND` và `6725_SGDDT_QLCL`; caption tự nhiên `Thông tư 93`, `CV 663`, `KH 265`, `QĐ 15`, `TB 02`.
2. **`api/telegram_vanban.php`**
   - Sau `vbd_parse_document`, điền số, thể loại, cơ quan còn trống từ tên tệp và caption. Số đầy đủ có dấu `/` từ tên tệp được ưu tiên. Caption cấu trúc `Số:`/`Thể loại:` vẫn ghi đè sau đó.
3. **`tests/telegram-vanban-webhook-smoke.py`**
   - Assert tên tệp + caption, `THÀNH PHỐ`/`PHƯỜNG`/`XÃ` không phải địa chỉ nhà, `6959/KH-SGDĐT`, `6925/SGDĐT-VP` không lấy `16416`, và ký hiệu ngắt dòng `7038/SGDĐT-VP`.

## Kiểm thử đã chạy

- `php -l api/vanban.php`: PASS.
- `php -l api/telegram_vanban.php`: PASS.
- PHP portable `%TEMP%/php-portable-834/php.exe`.
- `python tests/telegram-vanban-webhook-smoke.py`: PASS — `telegram-vanban-webhook smoke: OK`.
- `git diff --check` trên ba file trên: PASS.
- 12 PDF trong `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/09.11/VAN BAN TRIEN KHAI/`:
  - `93_2026_TT_BGDDT.signed.pdf` + caption `Thông tư 93`: số `93/2026/TT-BGDĐT`, thể loại `Thông tư`, cơ quan `Bộ Giáo dục và Đào tạo`, ngày `2026-11-04`.
  - `KH trien khai KH 359 UBND.pdf`: `6959/KH-SGDĐT`.
  - `CV huong dan quan ly DTHT...`: `7037/SGDĐT-GDPT&GDTX`.
  - `CV trienkhai VB12151...`: `6925/SGDĐT-VP`.
  - `2.11 CV 663...`: `/MTTQ-BTT`, không còn `25/10`.
  - `T11_2026...`: `7038/SGDĐT-VP`.
  - Giữ đúng `6725/SGDĐT-QLCL`, `03/KH-CM`, `265/KH-UBND`, `6328/SKHCN-CĐS`.
  - `02. TB KẾT LUẬN...` và `115-KE HOACH...` vẫn không có số: font CMap lỗi và file scan không có lớp chữ.
  - Đúng số trên 10/12 tệp (83%).
- Chưa gửi file qua bot Telegram đang chạy.

## Bàn giao

- Không sửa `PLAN.md`, không sửa `VERIFY.md`.
- `VERIFY.md` là kết quả của phạm vi trước. Cần `/verify` cho kế hoạch này.
- Đã xóa `docs/handoff/.lock` trước khi sửa, tạo lại nội dung `LOCK` sau khi ghi file này.
- Chưa commit/push.
- Bước tiếp theo: Antigravity IDE, chat mới: `/verify`.
