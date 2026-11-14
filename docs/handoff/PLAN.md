# PLAN: Nâng cấp nhận diện số, thể loại, cơ quan từ nội dung, tên tệp và caption tự nhiên

**Ngày:** 2026-11-14  
**Vấn đề:** 
1. Bot không nhận diện được số/thể loại/cơ quan của file scan ảnh (như `93_2026_TT_BGDDT.signed.pdf`) dù tên tệp có cấu trúc chuẩn và người dùng đã gõ caption tự nhiên (`Thông tư 93`).
2. Tên cơ quan có chứa `THÀNH PHỐ`, `UBND PHƯỜNG`, `UBND XÃ` bị hàm `vbd_is_reference_context` nhận nhầm là địa chỉ nhà, làm chặn đứng số văn bản chính ở đầu file (gây mất số ở file `KH 359`, lấy nhầm số dẫn chiếu ở file `CV hướng dẫn DTHT`, nhặt nhầm ngày `25/10` ở file `CV 663`).
3. Pattern quét sâu vào nội dung (1400 ký tự) bỏ qua số ký số ở dòng 90 đầu trang để lấy số dẫn chiếu ở dòng 1345 trong thân văn bản (file `CV trienkhai`).
4. Ký hiệu bị ngắt dòng dọc từng chữ cái (`Số:\n/\nS\nGDĐT\n-\nVP`) làm cụt số ở file `T11_2026`.

---

## Hiện trạng
- Hệ thống chỉ cố gắng bóc tách từ text layer của PDF. Với file scan ảnh 100% (như `93_2026_TT_BGDDT.signed.pdf`), text layer rỗng nên bot báo "Chưa nhận diện" cho thể loại, số và cơ quan.
- Caption hiện tại chỉ hỗ trợ cú pháp cứng nhắc `Số: ..., Thể loại: ...`, người dùng gõ tự nhiên `Thông tư 93` thì bot chỉ đưa vào trích yếu.
- Tên tệp tải về từ các cổng văn bản chính phủ (`93_2026_TT_BGDDT.signed.pdf`, `265_KH_UBND.pdf`, `6725_SGDDT_QLCL.pdf`) chứa đầy đủ siêu dữ liệu nhưng chưa được khai thác.
- Hàm `vbd_is_reference_context()` có regex `(Địa chỉ|đường|phố|ngõ|ấp|khu|phường|xã)` khớp trúng chữ `phố` trong `THÀNH PHỐ ĐỒNG NAI` hoặc `phường` trong `UBND PHƯỜNG`, gây false positive chặn số thật.
- Thứ tự duyệt regex trong `vbd_find_document_number()` ưu tiên pattern có sẵn số chữ số trước pattern khuyết số, khiến số chính ở đầu trang bị bỏ qua để nhặt số tham chiếu trong thân bài.

---

## Phạm vi
- `api/vanban.php`:
  1. Cải tiến `vbd_is_reference_context()`: Phân biệt rõ địa chỉ nhà (`Địa chỉ:`, `Trụ sở:`, tên đường/phố cụ thể `(?<!thành\s)(?<!thị\s)phố`) để không chặn tên cơ quan hành chính `THÀNH PHỐ`, `UBND PHƯỜNG`, `UBND XÃ`.
  2. Cải tiến `vbd_find_document_number()`:
     - Giới hạn cửa sổ tìm số chính trong header (<700 ký tự).
     - Gom tất cả ứng viên và ưu tiên theo vị trí xuất hiện sớm nhất ở đầu trang có tiền tố `Số:`.
     - Loại trừ số ngày dạng `dd/mm` (như `25/10`).
     - Hỗ trợ khoảng trắng và ký tự xuống dòng giữa các thành phần của ký hiệu tổ chức (khắc phục `S\nGDĐT\n-\nVP`).
  3. Thêm hàm `vbd_parse_from_name_and_caption(string $filename, string $caption): array`:
     - Bóc tách số văn bản, thể loại, cơ quan từ tên tệp chuẩn hành chính:
       * Dạng Bộ: `(\d+)[_\-\/](\d{4})[_\-\/](TT|QĐ|NĐ|CT)[_\-\/]([A-Za-z0-9]+)` $\rightarrow$ Số `93/2026/TT-BGDĐT`, Thể loại `Thông tư`, Cơ quan `Bộ Giáo dục và Đào tạo`.
       * Dạng địa phương: `(\d+)[_\-\/]([A-Za-z]+)[_\-\/]([A-Za-z]+)` $\rightarrow$ `265/KH-UBND` (Kế hoạch), `6725/SGDĐT-QLCL` (Công văn).
     - Bóc tách từ caption tự nhiên của người dùng:
       * `Thông tư 93`, `TT 93` $\rightarrow$ Thể loại: `Thông tư`, Số: `93`
       * `Kế hoạch 265`, `KH 265` $\rightarrow$ Thể loại: `Kế hoạch`, Số: `265`
       * `Quyết định 15`, `QĐ 15` $\rightarrow$ Thể loại: `Quyết định`, Số: `15`
       * `Công văn 663`, `CV 663` $\rightarrow$ Thể loại: `Công văn`, Số: `663`
       * `Thông báo 02`, `TB 02` $\rightarrow$ Thể loại: `Thông báo`, Số: `02`
- `api/telegram_vanban.php`:
  - Trong luồng tiếp nhận file, sau khi chạy `vbd_parse_document`, tự động gọi `vbd_parse_from_name_and_caption($file['name'], $caption)`.
  - Nếu bất kỳ trường nào (`document_number`, `document_type`, `organization`) còn trống hoặc chưa nhận diện được, tự động điền giá trị bóc tách được từ tên file / caption tự nhiên.
  - Nếu số từ tên file có dạng `93/2026/TT-BGDĐT` thì ưu tiên điền hoàn chỉnh.
- `tests/telegram-vanban-webhook-smoke.py`:
  - Thêm test case cho `vbd_parse_from_name_and_caption` với tên tệp `93_2026_TT_BGDDT.signed.pdf` và caption `Thông tư 93`.
  - Thêm assert kiểm tra `THÀNH PHỐ ĐỒNG NAI` không bị coi là địa chỉ nhà trong `vbd_is_reference_context`.
  - Thêm test case cho `CV trienkhai` không bị nhặt nhầm `16416/KH-UBND`.
  - Thêm test case cho `KH 359` nhận diện đúng `6959/KH-SGDĐT`.
  - Thêm test case ký hiệu ngắt dòng `S\nGDĐT\n-\nVP`.

---

## Ngoài phạm vi
- Không thay đổi cấu trúc bảng cơ sở dữ liệu (`office_documents`, `office_document_files`, `office_telegram_updates`).
- Không can thiệp Cloudflare Worker hay script CI/CD GitHub Actions.
- Không cài thêm binary bên thứ ba (không phụ thuộc `tesseract` hay `pdftotext`).

---

## File dự kiến tác động
- `api/vanban.php`
- `api/telegram_vanban.php`
- `tests/telegram-vanban-webhook-smoke.py`

---

## Các bước thực hiện

### Bước 1: Viết test case và assertions mới
- Mở `tests/telegram-vanban-webhook-smoke.py`.
- Thêm các mẫu kiểm thử cho `vbd_parse_from_name_and_caption` với:
  * `name = '93_2026_TT_BGDDT.signed.pdf', caption = 'Thông tư 93'` $\rightarrow$ `number: 93/2026/TT-BGDĐT`, `type: Thông tư`, `org: Bộ Giáo dục và Đào tạo`.
  * `name = 'CV_663.pdf', caption = 'CV 663'` $\rightarrow$ `type: Công văn`.
  * Text có `THÀNH PHỐ ĐỒNG NAI \n Số: /KH-SGDĐT` + annot `6959` $\rightarrow$ `6959/KH-SGDĐT`.
  * Text có `Số: /SGDĐT-VP` ở đầu và `16416/KH-UBND` ở cuối $\rightarrow$ chọn `6925/SGDĐT-VP`.
  * Text ngắt dòng `Số:\n/\nS\nGDĐT\n-\nVP` + annot `7038` $\rightarrow$ `7038/SGDĐT-VP`.

### Bước 2: Sửa `vbd_is_reference_context()` trong `api/vanban.php`
- Sửa regex địa chỉ:
  ```php
  if (preg_match('/(?:Địa chỉ|Dia chi|Trụ sở|Tru so)\s*[:\.]?.{0,40}$/ius', $tail)) return true;
  if (preg_match('/(?:đường|ngõ|hẻm|ấp|khu\s*phố|(?<!thành\s)(?<!thị\s)phố)\s+[A-Za-zÀ-ỹ0-9\s]{2,30}.{0,20}$/ius', $tail)) return true;
  ```
- Thêm `triển khai\s+(?:Kế hoạch|Công văn|Quyết định)\s*số` vào nhóm từ chỉ dẫn chiếu.

### Bước 3: Cải tiến `vbd_find_document_number()` trong `api/vanban.php`
- Thu hẹp phạm vi quét số chính trong header xuống 700 ký tự đầu.
- Cho phép khoảng trắng / xuống dòng trong cụm mã cơ quan (hỗ trợ `S\nGDĐT\n-\nVP`).
- Gom tất cả các match ứng viên, bỏ qua số ngày `dd/mm` (như `25/10`).
- Sắp xếp ứng viên ưu tiên:
  1. Có nhãn `Số:` đứng trước.
  2. Vị trí xuất hiện sớm nhất trong header.
- Áp dụng `vbd_apply_annot_number` để ghép số từ annotation chữ ký số.

### Bước 4: Viết hàm `vbd_parse_from_name_and_caption()` trong `api/vanban.php`
- Chuẩn hóa tên file: loại bỏ phần mở rộng (`.pdf`, `.signed`, `.dadongdau`).
- Bóc tách theo mẫu mã cơ quan trung ương / địa phương.
- Bóc tách thể loại và số từ caption tự nhiên (`Thông tư 93`, `KH 265`, `CV 663`...).

### Bước 5: Tích hợp vào `api/telegram_vanban.php`
- Trong hàm webhook, sau khi gọi `vbd_parse_document($source)`:
  ```php
  $fromNameCap = vbd_parse_from_name_and_caption($file['name'], (string)($message['caption'] ?? ''));
  foreach (['document_number', 'document_type', 'organization'] as $field) {
      if (empty($parsed[$field]) && !empty($fromNameCap[$field])) {
          $parsed[$field] = $fromNameCap[$field];
      }
  }
  // Nếu có số đầy đủ dạng NNNN/YYYY/TT-BGDĐT từ tên tệp thì ưu tiên dùng
  if (!empty($fromNameCap['document_number']) && str_contains($fromNameCap['document_number'], '/')) {
      $parsed['document_number'] = $fromNameCap['document_number'];
  }
  ```

### Bước 6: Kiểm thử xác nhận
- Chạy `python tests/telegram-vanban-webhook-smoke.py`.
- Chạy script kiểm thử trên bộ 12 file PDF thực tế.

---

## Rủi ro
- Tên tệp do người dùng đặt không theo quy chuẩn (ví dụ `Scan001.pdf`): Hàm sẽ trả về rỗng và không ảnh hưởng gì đến các luồng bóc tách khác.
- Caption có thể chứa nhiều số: Regex chỉ bắt số ngay sau từ khóa thể loại (`Thông tư 93`).

---

## Cách kiểm thử
1. `php -l api/vanban.php` $\rightarrow$ No syntax errors.
2. `php -l api/telegram_vanban.php` $\rightarrow$ No syntax errors.
3. `python tests/telegram-vanban-webhook-smoke.py` $\rightarrow$ PASS.
4. Chạy script trích xuất trên 12 file PDF thực tế trong `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/09.11/VAN BAN TRIEN KHAI/`:
   - `93_2026_TT_BGDDT.signed.pdf` với caption `Thông tư 93` $\rightarrow$ `93/2026/TT-BGDĐT`, `Thông tư`, `Bộ Giáo dục và Đào tạo`.
   - `KH trien khai KH 359 UBND.pdf` $\rightarrow$ `6959/KH-SGDĐT`.
   - `CV huong dan quan ly DTHT...` $\rightarrow$ `7037/SGDĐT-GDPT&GDTX`.
   - `CV trienkhai VB12151...` $\rightarrow$ `6925/SGDĐT-VP`.
   - `2.11 CV 663...` $\rightarrow$ không ra `25/10`.

---

## Tiêu chí nghiệm thu
- [ ] Smoke test `python tests/telegram-vanban-webhook-smoke.py` chạy qua 100% không cảnh báo.
- [ ] Trường hợp ảnh người dùng gửi: Tệp `93_2026_TT_BGDDT.signed.pdf` + caption `Thông tư 93` nhận diện đầy đủ:
  - Thể loại: `Thông tư`
  - Số/Ký hiệu: `93/2026/TT-BGDĐT`
  - Cơ quan: `Bộ Giáo dục và Đào tạo`
  - Ngày ban hành: `2026-11-04`
- [ ] Không còn tình trạng tên cơ quan `THÀNH PHỐ` bị coi là địa chỉ nhà làm mất số văn bản.
- [ ] Tỷ lệ nhận diện đúng trên 12 file thực tế đạt $\ge 75\%$.
