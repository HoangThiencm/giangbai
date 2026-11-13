# Kế hoạch: Chuẩn hóa toàn diện nhận diện số văn bản (Cấp Bộ, Phòng ban ghép &, Đảng, Bỏ qua địa chỉ)

## 1. Mục tiêu
Khắc phục triệt để hiện tượng "nhận diện số văn bản lúc được lúc không" trên kho văn bản hành chính thực tế:
1. **Khớp đúng số văn bản cấp Bộ (Thông tư / Quyết định)**:
   - Các văn bản có năm ban hành ở giữa: `Số: 93/2026/TT-BGDĐT` (hiện tại bị nhặt thiếu thành `2026/TT-BGDĐT`, mất `93/`).
2. **Hỗ trợ ký hiệu phòng ban ghép ký tự `&`**:
   - Các công văn liên phòng: `4200/SGDĐT-GDPT&GDTX` hoặc `7037/SGDĐT-GDPT&GDTX` (hiện tại bị cắt cụt mất phần `&GDTX`).
3. **Chuẩn hóa văn bản của Đảng**:
   - Các định dạng: `193-QĐ/THCS`, `02-HD/ĐU`, `193-QĐ/QU-THCS`.
4. **Loại bỏ hoàn toàn việc nhầm lẫn với "Số nhà / Địa chỉ"**:
   - Dòng địa chỉ cơ quan: `Số 1597, đường Phạm Văn Thuận...` (chặn không được coi là số văn bản).
5. **Nới lỏng thời gian bóc tách PDF (Deadline)**:
   - Tăng `$deadline` trong `api/pdf_text_extractor.php` từ 1.4s lên 3.0s để không bị timeout trên các file PDF dung lượng lớn có nhiều lớp chữ ký số.

---

## 2. Chi tiết triển khai cho Coder

### Bước 1: Nâng cấp `api/vanban.php`
- Cập nhật định nghĩa ký hiệu cơ quan trong `vbd_find_document_number(string $head)`:
  - `$org = '[A-Za-zÀ-ỹ0-9.&]+';` (bổ sung ký tự `&`).
- Bổ sung các pattern ưu tiên nhận diện số hiệu:
  1. **Văn bản cấp Bộ (có năm ở giữa)**:
     `/(?:Số|So)\s*[:\.]?\s*([0-9]{1,6}' . $sp . '\/' . $sp . '[0-9]{4}' . $sp . '\/' . $sp . $org . '(?:' . $sp . '-' . $sp . $org . ')*)/iu`
     -> Khớp `93/2026/TT-BGDĐT`.
  2. **Văn bản chuẩn có mã thể thức**:
     `/(?:Số|So)\s*[:\.]?\s*([0-9]{1,6}' . $sp . '\/' . $sp . $code . '(?:' . $sp . '-' . $sp . $org . ')+)/iu`
     -> Khớp `7400/KH-SGDĐT`, `123/QĐ-UBND`.
  3. **Văn bản của Đảng**:
     `/(?:Số|So)\s*[:\.]?\s*([0-9]{1,6}' . $sp . '-' . $sp . $partyCode . $sp . '\/' . $sp . $org . '(?:' . $sp . '-' . $sp . $org . ')*)/iu`
     -> Khớp `193-QĐ/THCS`, `02-HD/ĐU`.
  4. **Văn bản cơ quan thông thường**:
     `/(?:Số|So)\s*[:\.]?\s*([0-9]{1,6}' . $sp . '\/' . $sp . $org . '(?:' . $sp . '-' . $sp . $org . ')*)/iu`
     -> Khớp `4200/SGDĐT-GDPT&GDTX`.
  5. **Văn bản khuyết số đầu (dự thảo/ký số)**:
     `/(?:Số|So)\s*[:\.]?\s*([0-9]*' . $sp . '[\/\-]' . $sp . $org . '(?:' . $sp . '-' . $sp . $org . ')*)/iu`
     -> Khớp `/KH-SGDĐT` (sau đó ghép số từ annotation).
  6. **Tìm số không có chữ "Số" phía trước**:
     `/\b([0-9]{1,6}' . $sp . '\/' . $sp . '[0-9]{4}' . $sp . '\/' . $sp . $org . '(?:' . $sp . '-' . $sp . $org . ')*)/iu`
     `/\b([0-9]{1,6}' . $sp . '\/' . $sp . $code . '(?:' . $sp . '-' . $sp . $org . ')+)/iu`
     `/\b([0-9]{1,6}' . $sp . '-' . $sp . $partyCode . $sp . '\/' . $sp . $org . '(?:' . $sp . '-' . $sp . $org . ')*)/iu`
- Trong `vbd_is_reference_context($before)`:
  - Bổ sung loại trừ ngữ cảnh địa chỉ:
    Nếu trước số có các từ `Địa chỉ`, `Dia chi`, `Trụ sở`, `Tru so` thì bỏ qua:
    `preg_match('/(Địa chỉ|Dia chi|Trụ sở|Tru so|đường|phố|ngõ|ấp|khu|phường|xã).{0,40}$/ius', $tail)`
- Trong `vbd_normalize_doc_number(string $raw)`:
  - Chuẩn hóa khoảng trắng quanh dấu `/`, `-`, `&`.

### Bước 2: Nâng cấp `api/pdf_text_extractor.php`
- Trong `vbd_pdf_extract_text(string $pdfPath, int $maxPages = 3)`:
  - Tăng `$deadline = microtime(true) + 3.0;` (thay vì 1.4s) để tránh bị timeout trên file nặng.
- Trong `vbd_pdf_annot_texts`:
  - Giới hạn chỉ duyệt Annotation ở trang 1 và trang 2 để tiết kiệm tài nguyên.

### Bước 3: Cập nhật kiểm thử trong `tests/telegram-vanban-webhook-smoke.py`
- Thêm các test case kiểm tra:
  - `Số: 93/2026/TT-BGDĐT` -> nhận diện `93/2026/TT-BGDĐT` (không bị mất `93/`).
  - `Số: 4200/SGDĐT-GDPT&GDTX` -> nhận diện đầy đủ `4200/SGDĐT-GDPT&GDTX` (không bị mất `&GDTX`).
  - `Số: 193-QĐ/THCS` -> nhận diện `193-QĐ/THCS`.
  - Chuỗi có địa chỉ `Địa chỉ: Số 1597, đường Phạm Văn Thuận... Số: 6328/SKHCN-CĐS` -> nhận diện đúng `6328/SKHCN-CĐS`.
  - Tệp mẫu `KH THI GIÁO VIÊN DẠY GỎI THCS - 2026-2027 pH.pdf` -> `7400/KH-SGDĐT`.
- Toàn bộ smoke test phải đạt 100%.

---

## 3. Tiêu chí nghiệm thu (Acceptance Criteria)
1. Số Thông tư cấp Bộ có năm ở giữa (`93/2026/TT-BGDĐT`) được nhận diện chính xác 100%.
2. Ký hiệu phòng ban có `&` (`4200/SGDĐT-GDPT&GDTX`) giữ nguyên vẹn ký tự `&` và vế sau.
3. Không bị nhầm số nhà / địa chỉ thành số văn bản.
4. `php -l` không lỗi, smoke test pass 100%.
