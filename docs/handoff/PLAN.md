# Kế hoạch sửa lỗi Bot Telegram Quản lý văn bản (Ngày ban hành, Thể loại, Trích yếu, Phản hồi nút menu)

## 1. Mục tiêu
Khắc phục triệt để 4 vấn đề người dùng phản ánh dựa trên tệp PDF mẫu thực tế (`KH_THI_GIÁO_VIÊN_DẠY_GỎI_THCS_-_2026-2027_pH.pdf`):
1. **Phản hồi khi bấm nút menu**: Khi nhấn các nút (Hành chính, Chuyên môn, Đảng, Xác nhận chính xác), bot phải phản hồi rõ ràng bằng thông báo tin nhắn và/hoặc modal alert.
2. **Hiển thị Thể loại**: Bổ sung dòng `Thể loại:` trong tin nhắn tóm tắt `tvb_summary()` của Telegram.
3. **Nhận diện chính xác thể loại & trích yếu**: Tách dòng độc lập giữa các block text trong PDF (tránh dính chữ `KẾ HOẠCHTổ chức Hội thi...`), nhận diện đúng thể loại `Kế hoạch` và trích yếu `Tổ chức Hội thi giáo viên dạy giỏi...`, không bị fallback về tên tệp Telegram.
4. **Chuẩn hóa ngày ban hành & số hiệu**:
   - Chặn tuyệt đối việc nhặt ngày `2019-12-20` hoặc số hiệu `4200/SGDĐT-GDPT` từ các căn cứ/dẫn chiếu (`Căn cứ Thông tư...`, `Thực hiện Công văn...`).
   - Ưu tiên ngày ký số điện tử (`2026-11-12`) hoặc ngày/tháng/năm tại phần tiêu ngữ của văn bản.
   - Hỗ trợ số hiệu dạng `/KH-SGDĐT` khi văn bản chưa điền số trước dấu gạch chéo.

---

## 2. Phân tích nguyên nhân gốc rễ

1. **Lỗi nối dính text trong `api/pdf_text_extractor.php`**:
   - Hàm `vbd_pdf_render_content()` không gọi `$newline()` tại toán tử `BT` (bắt đầu khối text) và `ET` (kết thúc khối text).
   - Trong PDF mẫu, `KẾ HOẠCH` nằm ở một khối `BT...ET` và tiêu đề `Tổ chức Hội thi...` nằm ở khối `BT...ET` kế tiếp. Do thiếu ngắt dòng, chuỗi trích xuất trở thành `KẾ HOẠCHTổ chức Hội thi...`.
   - Hệ quả: `vbd_match_type_line()` không khớp được regex `^\s*KẾ HOẠCH\s*$`, dẫn đến không xác định được thể loại và không trích xuất được `title`, khiến tiêu đề bị fallback về tên tệp PDF.

2. **Lỗi lấy nhầm ngày ban hành thành `2019-12-20`**:
   - Ở tiêu ngữ, ngày ghi dạng: `Đồng Nai, ngày    tháng 11 năm 2026` (khuyết ngày để ký số/đóng dấu sau).
   - Do regex yêu cầu đủ ngày-tháng-năm bị trượt, hàm fallback `vbd_parse_vn_date($dateHead)` đã quét sâu xuống và nhặt trúng: `Căn cứ Thông tư số 22/2019/TT-BGDĐT ngày 20/12/2019...`.
   - File có chữ ký số điện tử chứa timestamp chuẩn `/M(D:20261112141848+07'00')` nhưng chưa được ưu tiên khai thác khi tiêu ngữ chỉ có tháng/năm.

3. **Lỗi lấy nhầm số hiệu thành `4200/SGDĐT-GDPT`**:
   - Header có `Số: /KH-SGDĐT`. Các regex hiện tại yêu cầu có chữ số trước dấu `/` (`[0-9]{1,6}`), nên bỏ qua `Số: /KH-SGDĐT`.
   - Các regex fallback tiếp theo quét thấy `4200/SGDĐT-GDPT&GDTX` từ câu: `Thực hiện Công văn số 4200/...` vì ngữ cảnh trước đó chứa `Thực hiện Công văn` chưa bị loại trừ chặt chẽ như `Căn cứ`.

4. **Thiếu dòng `Thể loại` trong `tvb_summary()`**:
   - Trong `api/telegram_vanban.php`, hàm `tvb_summary()` hoàn toàn chưa khai báo dòng `<b>Thể loại:</b>`.

5. **Phản hồi nút menu mờ nhạt**:
   - Trong `tvb_process_callback()`, chỉ gọi `tvb_answer_callback($callback, $popup)`. Với `show_alert => false`, Telegram chỉ hiện thanh toast rất nhỏ ở mép trên màn hình trong 2-3 giây rồi biến mất, người dùng trên Telegram Web/Desktop không nhận ra phản hồi.

---

## 3. Các bước triển khai chi tiết cho Coder

### Bước 1: Cập nhật `api/pdf_text_extractor.php`
- Tại hàm `vbd_pdf_render_content()`:
  - Khi gặp toán tử `BT`: gọi `$newline();`.
  - Khi gặp toán tử `ET`: gọi `$newline();`.
  - Giúp mọi khối văn bản độc lập (tiêu đề, số hiệu, nơi ban hành, trích yếu) được phân tách bằng dòng mới rõ ràng, không bị dính chữ.

### Bước 2: Nâng cấp nhận diện thể loại và trích yếu trong `api/vanban.php`
- Cải tiến `vbd_match_type_line(string $head)`:
  - Hỗ trợ trường hợp thể loại đứng đầu một dòng nhưng có thể đi kèm dấu hai chấm hoặc khoảng trắng trước nội dung:
    `/^\s*(' . implode('|', $parts) . ')(?:\s*[:\.\-–—]|\s*$|\s+(?=[A-ZÀ-Ỹ]))/uim`.
  - Trả về vị trí kết thúc của từ khóa thể loại để trích xuất trích yếu ngay bên dưới hoặc phần còn lại của dòng.
- Cải tiến `vbd_type_from_number(string $number)`:
  - Bổ sung regex khớp ký hiệu kể cả khi không có số phía trước: ví dụ `/KH-`, `/QĐ-`, `/TB-`, `/HD-`, `/BC-`.
  - Ví dụ: `Số: /KH-SGDĐT` -> suy ra ngay thể loại `Kế hoạch`.
- Nâng cấp `vbd_is_reference_context(string $before)`:
  - Bổ sung các từ khóa dẫn chiếu mở rộng: `Thực hiện`, `Thuc hien`, `Theo`, `Tại`, `V/v`, `về việc`.

### Bước 3: Chuẩn hóa ngày ban hành và số hiệu trong `api/vanban.php`
- Cắt bỏ phần căn cứ dẫn chiếu trước khi tìm ngày ban hành tiêu ngữ:
  - Tìm vị trí đầu tiên xuất hiện các từ `Căn cứ`, `Thực hiện Công văn`, `Theo Quyết định`. Cắt chuỗi `$dateHead` trước vị trí này để không bao giờ đọc phải ngày của văn bản cũ.
- Hỗ trợ tiêu ngữ khuyết ngày:
  - Nếu tiêu ngữ có dạng `ngày\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})` (khuyết số ngày):
    - Ưu tiên lấy ngày từ chữ ký số điện tử (`vbd_latest_signature_date`) nếu năm và tháng trùng khớp.
    - Nếu không có chữ ký số, lấy ngày mặc định là ngày đầu tháng: `sprintf('%04d-%02d-01', $year, $month)`.
- Nâng cấp `vbd_find_document_number()`:
  - Cho phép số hiệu khuyết chữ số đầu: `(?:Số|So)\s*[:\.]?\s*([0-9]*\s*[\/\-][A-Za-zÀ-ỹ0-9.\-]+(?:-[A-Za-zÀ-ỹ0-9.\-]+)*)`.
  - Tránh tuyệt đối việc lấy nhầm số hiệu từ phần nội dung dẫn chiếu.

### Bước 4: Cập nhật giao diện và phản hồi Telegram trong `api/telegram_vanban.php`
- Trong `tvb_summary()`:
  - Bổ sung dòng thể loại:
    ```php
    '<b>Thể loại:</b> ' . tvb_html((string)($document['document_type'] ?: 'Chưa nhận diện')),
    ```
    Đặt ngay sau dòng `Lĩnh vực`.
- Trong `tvb_answer_callback()`:
  - Bổ sung tham số `$showAlert = false`:
    ```php
    function tvb_answer_callback(array $callback, string $text, bool $showAlert = false): void
    {
        try {
            tvb_api('answerCallbackQuery', [
                'callback_query_id' => (string)($callback['id'] ?? ''),
                'text' => $text,
                'show_alert' => $showAlert,
            ]);
        } catch (Throwable $error) { ... }
    }
    ```
- Trong `tvb_process_callback()`:
  - Khi bấm đổi lĩnh vực (`sector:...`):
    - Gọi `tvb_answer_callback($callback, $popup, false)`.
    - Gửi tin nhắn phản hồi trực tiếp vào chat:
      `tvb_api('sendMessage', ['chat_id' => $chatId, 'text' => "🔄 Đã chuyển lĩnh vực sang: <b>{$labels[$match[2]]}</b>", 'parse_mode' => 'HTML']);`
  - Khi bấm xác nhận chính xác (`confirm:...`):
    - Gọi `tvb_answer_callback($callback, $popup, true)` (hiển thị popup modal xác nhận rõ ràng).
    - Gửi tin nhắn phản hồi trực tiếp vào chat:
      `tvb_api('sendMessage', ['chat_id' => $chatId, 'text' => "✅ Đã xác nhận thông tin văn bản #{$documentId}.", 'parse_mode' => 'HTML']);`
  - Giữ nguyên `tvb_edit_callback_message` để cập nhật trạng thái tin nhắn gốc.

### Bước 5: Cập nhật và chạy kiểm thử
- Bổ sung test case trong `tests/telegram-vanban-webhook-smoke.py` kiểm tra:
  - Tách text PDF khi có `BT`/`ET`.
  - Regex bóc tách đúng thể loại `Kế hoạch`, trích yếu `Tổ chức Hội thi giáo viên dạy giỏi...` và ngày tháng `2026-11-12` từ file mẫu.
  - Hợp đồng `<b>Thể loại:</b>` có trong `tvb_summary`.
  - Hợp đồng phản hồi tin nhắn trong `tvb_process_callback`.
- Chạy toàn bộ test suite để đảm bảo pass 100%.

---

## 4. Kiểm chứng nghiệm thu (Acceptance Criteria)
1. Bóc tách tệp `KH_THI_GIÁO_VIÊN_DẠY_GỎI_THCS_-_2026-2027_pH.pdf`:
   - `document_type`: `Kế hoạch` (KHÔNG được để trống).
   - `title`: `Tổ chức Hội thi giáo viên dạy giỏi cơ sở giáo dục Trung học cơ sở cấp thành phố năm học 2026 - 2027` (KHÔNG được fallback về tên tệp PDF).
   - `document_date`: `2026-11-12` (ngày ký số) hoặc `2026-11-01` (tháng 11/2026), TUYỆT ĐỐI KHÔNG phải `2019-12-20`.
   - `document_number`: `/KH-SGDĐT` (hoặc số chuẩn nếu có), TUYỆT ĐỐI KHÔNG phải `4200/SGDĐT-GDPT`.
2. Tin nhắn tóm tắt Telegram:
   - Có hiển thị rõ ràng dòng `Thể loại: Kế hoạch`.
3. Nhấn menu trên Telegram:
   - Có tin nhắn phản hồi trực tiếp vào chat xác nhận đã chuyển lĩnh vực hoặc đã xác nhận.
   - Nút xác nhận bật modal alert thông báo thành công.
