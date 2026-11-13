# IMPLEMENT: Bot Telegram Quản lý văn bản (ngày ban hành, thể loại, trích yếu, phản hồi menu)

## Phạm vi đã thực hiện

1. **`api/pdf_text_extractor.php`**
   - `BT` và `ET` đều xuống dòng, nên `KẾ HOẠCH` không dính vào câu trích yếu.
   - Ghép gợi ý chữ ký số mới nhất `/M(D:YYYYMMDD)` lên đầu text để còn nằm trong cửa sổ 2500 ký tự.

2. **`api/vanban.php`**
   - `vbd_find_document_number()` nhận số khuyết chữ số đầu (`/KH-SGDĐT`), bỏ số chỉ toàn chữ số (`22/2019`), và bỏ số nằm sau căn cứ/dẫn chiếu (`4200/SGDĐT-GDPT`, `1170/SGDĐT-GDPT`, `2019/TT-BGDĐT`).
   - Cửa sổ ngữ cảnh chỉ lấy phần đứng trước số và được làm sạch UTF-8 trước khi kiểm tra dẫn chiếu.
   - Tiêu ngữ `ngày tháng 11 năm 2026` lấy ngày ký số cùng tháng (`2026-11-12`), nếu không có thì ngày 01. Phần `Căn cứ` / `Thực hiện Công văn` / `Theo Quyết định` bị cắt trước khi đọc ngày.
   - Thể loại lấy từ dòng in hoa (`KẾ HOẠCH`). Trích yếu nối tối đa 3 dòng, gồm dòng tiếp viết thường.

3. **`api/telegram_vanban.php`**
   - `tvb_summary()` có dòng `Thể loại` ngay sau `Lĩnh vực`.
   - Đổi lĩnh vực: trả lời callback không alert, rồi gửi tin `Đã chuyển lĩnh vực sang`.
   - Xác nhận: `show_alert` true, rồi gửi tin `Đã xác nhận thông tin văn bản #...`.

4. **`tests/telegram-vanban-webhook-smoke.py`**
   - Thêm ca số khuyết, ngày ký số, và PDF hội thi trên Desktop.

## Kiểm thử

- `php -l` (PHP 8.3.36, bật mbstring): `api/pdf_text_extractor.php`, `api/vanban.php`, `api/telegram_vanban.php` — không lỗi cú pháp.
- `python tests/telegram-vanban-webhook-smoke.py` — in `telegram-vanban-webhook smoke: OK`.
- PDF mẫu `KH THI GIÁO VIÊN DẠY GỎI THCS - 2026-2027 pH.pdf`: số `/KH-SGDĐT`, thể loại `Kế hoạch`, trích yếu đủ câu hội thi, ngày `2026-11-12`.
- Chưa gọi webhook Telegram thật. Chưa commit.

## Bổ sung sau plan, theo yêu cầu người dùng

Khi nhận diện thiếu thể loại, số hiệu, hoặc trích yếu chỉ còn tên tệp, bot hỏi lần lượt 5 mục: Thể loại, Số/Ký hiệu, Ngày ban hành, Cơ quan ban hành, Trích yếu. Mỗi mục hiện giá trị bot đang đề xuất. Người dùng bấm **Giữ đề xuất**, chọn thể loại, gõ giá trị mới, gõ `xóa`, hoặc `hủy`. Nút **Sửa từng mục** luôn có trên phiếu văn bản, kể cả khi nhận diện đã đủ. Phiên sửa nằm ở bảng `office_telegram_edits`, một phiên cho mỗi cuộc trò chuyện.

## Việc tiếp theo

Antigravity IDE, chat mới: `/verify`.
