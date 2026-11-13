# Kế hoạch: Bóc tách Annotation chữ ký số PDF, bỏ hỏi 5 bước và thêm nút 1 chạm "Ghép vào VB trước"

## 1. Mục tiêu
1. **Bóc tách chuẩn 100% lớp chữ ký số PDF (`api/pdf_text_extractor.php` & `api/vanban.php`)**:
   - Quét và giải mã text từ Annotation Appearance XObjects (`/Annots -> /AP /N`) của trang.
   - Nhặt được số `7400` và ngày `12` được đóng dấu/ký số bởi VNPT-CA trong file mẫu.
   - Tự động ghép thành số hiệu đầy đủ: `7400/KH-SGDĐT` (không còn bị khuyết thành `/KH-SGDĐT`) và ngày `2026-11-12`.
2. **Bỏ chế độ hỏi 5 bước rườm rà (`api/telegram_vanban.php`)**:
   - Tắt bỏ hoàn toàn luồng wizard 5 bước (`tvb_needs_manual`, `tvb_edit_begin`, bảng `office_telegram_edits`, nút `✏️ Sửa từng mục`).
   - Bot chỉ gửi phiếu tóm tắt trực quan, không hỏi han qua lại làm chậm thao tác.
3. **Thêm tính năng 1 chạm: `📎 Ghép vào VB trước (#ID)` (`api/telegram_vanban.php`)**:
   - Giải quyết bài toán: 1 văn bản đi kèm nhiều phụ lục, hoặc văn bản của Bộ + văn bản triển khai của Sở muốn lưu chung một hồ sơ.
   - Khi văn bản mới được gửi lên trong vòng 30 phút sau văn bản trước đó, bàn phím sẽ tự động xuất hiện nút:
     `📎 Ghép vào VB trước (#<prevId>)`.
   - Bấm 1 chạm: Tệp của văn bản mới được chuyển sang làm tệp đính kèm của văn bản trước (`office_document_files`), thu hồi bản ghi văn bản thừa.

---

## 2. Chi tiết triển khai cho Coder

### Bước 1: Nâng cấp `api/pdf_text_extractor.php` đọc Annotation XObjects
- Viết hàm `vbd_pdf_annot_texts(array $objects, string $pageDict): array`:
  - Tìm `/Annots [ ... ]` trong `pageDict`.
  - Với mỗi annotation ID, tìm `/AP` chứa `/N <id> 0 R`.
  - Đệ quy duyệt qua các Form XObject lồng nhau (`/Resources -> /XObject`), giải mã stream qua font map tương ứng (`vbd_pdf_font_maps` & `vbd_pdf_render_content`).
  - Lấy các đoạn text trích xuất được (như `7400`, `12`).
- Trong `vbd_pdf_page_text(array $objects, int $pageId)`:
  - Lấy mảng chuỗi từ `vbd_pdf_annot_texts($objects, $dict)`.
  - Nếu có text annotation, chèn thêm vào đầu hoặc cuối nội dung trang:
    `ANNOT_TEXT: ` . implode(' | ', $annotTexts) . "\n".

### Bước 2: Nâng cấp ghép số hiệu và ngày trong `api/vanban.php`
- Trong `vbd_find_document_number($head)`:
  - Nếu số hiệu tìm được bắt đầu bằng `/` (ví dụ `/KH-SGDĐT`), kiểm tra trong `$head` xem có chuỗi số annotation hoặc số độc lập `\b(\d{1,6})\b` (ví dụ `7400` từ `ANNOT_TEXT`).
  - Nếu có, ghép số này vào trước: `$digits . $number` -> thành `7400/KH-SGDĐT`.
- Trong `vbd_regex_extract($source)`:
  - Nếu tiêu ngữ khuyết số ngày (`ngày tháng 11 năm 2026`) nhưng có số ngày từ annotation (như `12`): ghép thành `2026-11-12`.

### Bước 3: Đơn giản hóa `api/telegram_vanban.php` & Bỏ hỏi 5 bước
- Xóa bỏ toàn bộ các hàm phục vụ luồng hỏi 5 bước: `tvb_needs_manual`, `tvb_edit_prompt`, `tvb_edit_keyboard`, `tvb_edit_send`, `tvb_edit_begin`, `tvb_edit_advance`, `tvb_edit_finish`, `tvb_edit_apply`, `tvb_edit_value`, `tvb_edit_command`, `tvb_edit_load`, `tvb_edit_save`, `tvb_edit_clear`, `tvb_process_edit_text`, `tvb_process_edit_callback`.
- Xóa bỏ việc tạo bảng `office_telegram_edits` trong `tvb_ensure_schema()`.
- Xóa xử lý callback `e:...` trong `tvb_process_callback()`.

### Bước 4: Thêm cơ chế 1 chạm `📎 Ghép vào VB trước` trong `api/telegram_vanban.php`
- Viết hàm tìm văn bản trước gần nhất:
  ```php
  function tvb_recent_previous_document(PDO $pdo, int $ownerId, int $excludeId): ?array
  ```
  - Tìm văn bản gần nhất của cùng `$ownerId` được tạo trong vòng 30 phút gần đây (`created_at >= NOW() - INTERVAL 30 MINUTE`) và `id <> $excludeId`.
- Cập nhật `tvb_keyboard(int $documentId, string $currentSector, ?int $prevId = null)`:
  - Hàng 1: 3 nút Lĩnh vực (`🏛 Hành chính`, `🎓 Chuyên môn`, `🚩 Đảng`).
  - Hàng 2 (nếu có `$prevId`): `['text' => "📎 Ghép vào VB trước (#{$prevId})", 'callback_data' => "merge:{$documentId}:{$prevId}"]`.
  - Hàng 3: `['text' => '✅ Xác nhận chính xác', 'callback_data' => "confirm:{$documentId}"]` và `['text' => '🔗 Mở trên Web', 'url' => ...]`.
- Xử lý callback `merge:(\d+):(\d+)`:
  - Di chuyển tệp: `UPDATE office_document_files SET document_id = ? WHERE document_id = ?`.
  - Xóa văn bản thừa: `DELETE FROM office_documents WHERE id = ?`.
  - Phản hồi alert: `tvb_answer_callback($callback, "Đã ghép tệp vào Văn bản #{$prevId}", true)`.
  - Gửi tin nhắn xác nhận: `tvb_api('sendMessage', ['chat_id' => $chatId, 'text' => "📎 Đã chuyển tệp sang làm phụ lục của Văn bản #{$prevId}."])`.
  - Sửa tin nhắn của văn bản vừa ghép thành:
    `tvb_api('editMessageText', ['chat_id' => $chatId, 'message_id' => $messageId, 'text' => "📎 <b>ĐÃ GHÉP TỆP VÀO VĂN BẢN #{$prevId}</b>\n(Tệp đã chuyển thành phụ lục đính kèm)", 'parse_mode' => 'HTML'])`.

### Bước 5: Cập nhật kiểm thử trong `tests/telegram-vanban-webhook-smoke.py`
- Kiểm tra bóc tách tệp `KH THI GIÁO VIÊN DẠY GỎI THCS - 2026-2027 pH.pdf`:
  - `document_number`: `7400/KH-SGDĐT` (đầy đủ số `7400`).
  - `document_type`: `Kế hoạch`.
  - `document_date`: `2026-11-12`.
  - `title`: `Tổ chức Hội thi giáo viên dạy giỏi...`.
- Kiểm tra hợp đồng callback `merge:(\d+):(\d+)` trong `telegram_vanban.php`.
- Smoke test pass 100%.

---

## 3. Tiêu chí nghiệm thu (Acceptance Criteria)
1. Tệp `KH THI GIÁO VIÊN DẠY GỎI THCS - 2026-2027 pH.pdf`:
   - Bóc tách đầy đủ số hiệu `7400/KH-SGDĐT`.
   - Ngày ban hành `2026-11-12`.
   - Thể loại `Kế hoạch`.
   - Trích yếu `Tổ chức Hội thi giáo viên dạy giỏi cơ sở giáo dục Trung học cơ sở cấp thành phố năm học 2026 - 2027`.
2. Trải nghiệm Telegram:
   - Gửi file -> Nhận phiếu tóm tắt gọn gàng, KHÔNG bị hỏi 5 bước.
   - Gửi tiếp file thứ 2 -> Phiếu có nút `📎 Ghép vào VB trước (#...)`. Bấm 1 phát là gộp thành phụ lục của file 1.
3. `php -l` không lỗi, smoke test pass 100%.
