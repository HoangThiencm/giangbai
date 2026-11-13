# IMPLEMENT: Annotation chữ ký số, bỏ hỏi 5 bước, ghép vào văn bản trước

## Phạm vi đã thực hiện

1. **`api/pdf_text_extractor.php`**
   - `vbd_pdf_annot_texts()` đọc `/Annots` và appearance `/AP /N`, duyệt Form XObject lồng nhau.
   - Dòng `ANNOT_TEXT:` được chèn vào text trang. File mẫu ra `7400` và `12`.

2. **`api/vanban.php`**
   - Số hiệu khuyết chữ số `/KH-SGDĐT` được ghép thành `7400/KH-SGDĐT`.
   - Tiêu ngữ khuyết ngày lấy số ngày từ annotation, thành `2026-11-12`.

3. **`api/telegram_vanban.php`**
   - Không còn wizard 5 bước, nút `Sửa từng mục`, callback `e:`, hay bảng `office_telegram_edits`.
   - `tvb_recent_previous_document()` lấy văn bản cùng chủ sở hữu tạo trong 30 phút, trừ văn bản vừa gửi.
   - Nếu có văn bản đó, phiếu hiện nút `📎 Ghép vào VB trước (#ID)`.
   - Callback `merge:id:prevId` chuyển `office_document_files` sang văn bản trước, xóa bản ghi thừa, báo alert và sửa tin nhắn đã ghép.
   - Hàng cuối vẫn là `Xác nhận chính xác` và `Mở trên Web`.

4. **`tests/telegram-vanban-webhook-smoke.py`**
   - PDF hội thi phải ra `7400/KH-SGDĐT`.
   - Hợp đồng callback `merge:(\d+):(\d+)`.

## Kiểm thử

- `php -l` (PHP 8.3.36, bật mbstring): `api/telegram_vanban.php` — không lỗi cú pháp. Hai file PDF và `vanban.php` không đổi ở lượt này; smoke vẫn nạp chúng.
- `python tests/telegram-vanban-webhook-smoke.py` — in `telegram-vanban-webhook smoke: OK`.
- Chưa bấm ghép trên Telegram thật. Chưa commit.

## Việc tiếp theo

Antigravity IDE, chat mới: `/verify`.
