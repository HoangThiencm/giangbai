# PLAN: Mở tab Chuyên môn, hỗ trợ chuyển văn bản từ Hành chính sang Chuyên môn và tối ưu nhận diện Số văn bản & Ký số điện tử

## Hiện trạng
1. **Lĩnh vực trong Quản lý văn bản**:
   - Hiện tại hệ thống Quản lý văn bản (`quanlyvanban.html`, `vanban-hub.js`) chỉ hỗ trợ 2 lĩnh vực: **Hành chính** (`quanlyvanban-hanhchinh.html`) và **Đảng** (`quanlyvanban-dang.html`).
   - Chưa có trang `quanlyvanban-chuyenmon.html` và chưa có lĩnh vực `chuyenmon`.
   - `api/vanban.php` hàm `vbd_sector()` chỉ chấp nhận `['hanhchinh', 'dang']`, tự động quy về `hanhchinh` nếu gặp giá trị khác.
   - `access-control.js` chưa khai báo đường dẫn `quanlyvanban-chuyenmon.html`.
   - Trong tab Hành chính (`quanlyvanban-hanhchinh.html` và `vanban-app.js`), chưa có cơ chế tick chọn (checkbox) hay nút thao tác để chuyển văn bản sang lĩnh vực Chuyên môn (chuyển từng văn bản hoặc chọn nhiều văn bản cùng lúc).

2. **Nhận diện Số văn bản và Ngày ký số / Quyết định ký số điện tử**:
   - `vanban-app.js` dùng `extractPdfTextLayer(file)` chỉ lấy text layer thô (`page.getTextContent()`) và chỉ đọc 20 dòng đầu của 3 trang đầu.
   - Chữ ký số (con dấu đỏ điện tử, chữ ký số của thủ trưởng/Hiệu trưởng) thường nằm ở **trang cuối cùng** hoặc nằm trong **PDF Annotations / Signature Fields (`/Type /Sig`) / Form XObject / Ảnh**, khiến `getTextContent()` không thu thập được chữ ký số và ngày ký.
   - Cấu hình `global_config.json` có mảng `mistral_keys: []` rỗng nên cơ chế OCR ảnh dự phòng không kích hoạt được khi gặp PDF dạng scan/ảnh con dấu.
   - Backend `api/vanban.php` trong hàm `vbd_preprocess_source()` có danh sách từ khóa `$skipKeywords` đang chủ động xóa bỏ toàn bộ các dòng chứa `'ký bởi'`, `'ngày ký'`, `'chữ ký số'`, `'ký số'`, `'thời gian ký'`... Dẫn đến việc dù văn bản điện tử có ngày ký thì backend cũng tự động lọc bỏ, làm mất ngày ban hành của văn bản.
   - Regex nhận diện số văn bản ở backend chưa bao quát hết các trường hợp số quyết định, công văn có ký hiệu đặc thù hoặc bị phân tách khoảng trắng khi trích xuất từ PDF ký số.

---

## Phạm vi
1. **Mở lĩnh vực Chuyên môn (`chuyenmon`) trong Quản lý văn bản**:
   - Cập nhật `vanban-hub.js`: Thêm sector `chuyenmon` (`{ label: 'Chuyên môn', icon: 'fa-graduation-cap', accent: 'indigo', page: 'quanlyvanban-chuyenmon.html' }`), cập nhật hàm `sectorOf(doc)` và thẻ thống kê trên `quanlyvanban.html`.
   - Tạo trang `quanlyvanban-chuyenmon.html` (kế thừa đầy đủ giao diện, màu sắc chủ đạo indigo/xanh dương chuyên môn, liên kết với `vanban-app.js` qua `window.VANBAN_SECTOR = 'chuyenmon'`).
   - Cập nhật `access-control.js`: Khai báo `'quanlyvanban-chuyenmon.html': 'quanlyvanban'`.
   - Cập nhật `api/vanban.php`:
     + Mở rộng `vbd_sector()` chấp nhận `'chuyenmon'`.
     + Cập nhật `vbd_sector_label()` hiển thị "Chuyên môn".
     + Cập nhật đường dẫn thư mục lưu trữ Google Drive (`CHUYEN_MON`) và thư mục cục bộ cho sector `chuyenmon`.

2. **Tính năng Tick chọn chuyển / sao chép văn bản từ Hành chính sang Chuyên môn**:
   - Trên tab Hành chính (`quanlyvanban-hanhchinh.html`):
     + Mỗi dòng/thẻ văn bản bổ sung checkbox chọn văn bản và nút thao tác nhanh "Chuyển sang Chuyên môn".
     + Thêm thanh công cụ hàng loạt (Bulk action bar): Khi tick chọn 1 hoặc nhiều văn bản, hiển thị nút "Chuyển đã chọn sang Chuyên môn" và "Sao chép đã chọn sang Chuyên môn".
     + Trong Modal chi tiết văn bản (`documentDetailModal`), bổ sung nút hành động "Chuyển sang Chuyên môn" / "Sao chép sang Chuyên môn".
   - Backend `api/vanban.php`:
     + Bổ sung action `transfer_sector` (chuyển sector của danh sách văn bản sang `chuyenmon`) và `copy_sector` (nhân bản bản ghi và liên kết file đính kèm sang sector `chuyenmon`).
     + Kiểm tra quyền sở hữu (`owner_id`) an toàn trước khi chuyển/sao chép.

3. **Tối ưu nhận diện Số văn bản & Ngày ký số / Quyết định ký số trong ứng dụng**:
   - **Đọc trực tiếp chữ ký số chuẩn PDF (Binary & Annotations)** trong `vanban-app.js`:
     + Đọc cấu trúc nhị phân của PDF (`/Type /Sig`), bóc tách trường `/M (D:YYYYMMDD...)` để lấy ngày ký số chuẩn xác trong 0.05s mà không cần OCR.
     + Bóc tách trường `/Name` hoặc trường chủ thể ký để nhận diện cơ quan/người ký số.
     + Gọi `page.getAnnotations()` để lấy nội dung text trong các Annotation/Stamp được phần mềm văn thư chèn vào.
   - **Quét trang cuối (Last Page)**:
     + Khi đọc PDF, ngoài trang đầu (chứa Số/Ký hiệu, Tiêu đề), tự động quét thêm trang cuối cùng (nơi có con dấu ký số điện tử của Quyết định/Công văn) để gom thông tin ký số vào nội dung nhận diện.
   - **Cải tiến Backend `api/vanban.php`**:
     + Sửa `vbd_preprocess_source()`: Không xóa các dòng chứa `'ngày ký'`, `'ký số'`, `'thời gian ký'`.
     + Trích xuất ngày từ dòng chữ ký số (ví dụ: `Ngày ký: 26/09/2026 09:30:15`) làm ngày dự phòng (`document_date`) khi văn bản không có ngày ở phần tiêu đề.
     + Nâng cấp regex `vbd_regex_extract()` nhận diện tốt các mẫu số quyết định, công văn như `123/QĐ-UBND`, `45/QĐ-SGDĐT`, `12/KH-THCS...` kể cả khi có khoảng trắng hay định dạng đặc thù.
   - **Công cụ hỗ trợ quét nhanh vùng chữ ký**:
     + Bổ sung nút "Dán nhanh từ Clipboard" và cho phép dán trực tiếp ảnh chụp vùng con dấu/số văn bản (từ Snipping Tool / Firefox Copy Text) để bóc tách ngay vào các trường.

4. **Smoke test**:
   - Tạo file test tự động `tests/vanban-chuyenmon-signature-smoke.js` kiểm tra toàn bộ luồng chuyển sector, nhận diện ký số và bóc tách dữ liệu.

---

## Ngoài phạm vi
- Không can thiệp vào các trang ngoài Quản lý văn bản (như phân công chuyên môn, sổ điểm, soạn bài...).
- Không ép buộc người dùng phải cài thêm phần mềm ngoài; các cải tiến chạy trực tiếp trong mã nguồn ứng dụng hiện có.

---

## File dự kiến tác động
- `quanlyvanban-chuyenmon.html` (tạo mới)
- `quanlyvanban.html`
- `vanban-hub.js`
- `quanlyvanban-hanhchinh.html`
- `vanban-app.js`
- `api/vanban.php`
- `access-control.js`
- `tests/vanban-chuyenmon-signature-smoke.js` (tạo mới)
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện
1. **Bước 1: Mở khóa handoff**:
   - Coder xóa `docs/handoff/.lock` trước khi sửa source.

2. **Bước 2: Cập nhật Hub, Access Control và tạo `quanlyvanban-chuyenmon.html`**:
   - Cập nhật `access-control.js`: Thêm route `'quanlyvanban-chuyenmon.html': 'quanlyvanban'`.
   - Cập nhật `vanban-hub.js`: Thêm lĩnh vực `chuyenmon` vào `SECTORS`, cập nhật `sectorOf(doc)`.
   - Cập nhật `quanlyvanban.html`: Điều chỉnh lưới sector để hiển thị 3 cột/thẻ đẹp mắt (Hành chính, Chuyên môn, Đảng).
   - Tạo `quanlyvanban-chuyenmon.html`: Thiết lập `window.VANBAN_SECTOR = 'chuyenmon'`, đồng bộ theme màu xanh Indigo chuyên nghiệp, liên kết `vanban-app.js`.

3. **Bước 3: Mở rộng Backend `api/vanban.php`**:
   - Mở rộng `vbd_sector()` hỗ trợ `'chuyenmon'`, `vbd_sector_label()` trả về "Chuyên môn".
   - Điều chỉnh thư mục Drive: Sector `chuyenmon` lưu vào folder `CHUYEN_MON`.
   - Thêm endpoint action `transfer_sector` và `copy_sector`:
     + Nhận mảng `document_ids` và `target_sector`.
     + Cập nhật hoặc sao chép văn bản sang sector đích, giữ nguyên hoặc sao chép liên kết tệp.
   - Sửa hàm `vbd_preprocess_source()`: Bảo lưu thông tin ngày ký số.
   - Sửa hàm `vbd_regex_extract()`: Thêm logic bóc tách `document_date` từ ngày ký số nếu phần header chưa có ngày; tối ưu regex bắt số quyết định / công văn.

4. **Bước 4: Nâng cấp `vanban-app.js` & Giao diện Hành chính**:
   - **Xử lý chuyển sang Chuyên môn trong tab Hành chính**:
     + Render checkbox chọn văn bản trên từng card/row.
     + Thêm thanh chọn nhiều văn bản với nút "Chuyển sang Chuyên môn" và "Sao chép sang Chuyên môn".
     + Thêm nút "Chuyển sang Chuyên môn" trong popup chi tiết văn bản.
     + Gọi API `transfer_sector` / `copy_sector`, hiển thị thông báo thành công và reload danh sách.
   - **Tối ưu nhận diện PDF ký số**:
     + Viết hàm đọc nhị phân PDF để trích xuất chữ ký số `/Type /Sig`, ngày ký `/M`, người ký `/Name`.
     + Cập nhật `extractPdfTextLayer`: Đọc thêm `page.getAnnotations()` và đọc thêm trang cuối cùng của PDF.
     + Kết hợp text trang đầu, text trang cuối và dữ liệu ký số trước khi gửi vào `runAutoParse()`.

5. **Bước 5: Viết bài test tự động `tests/vanban-chuyenmon-signature-smoke.js`**:
   - Kiểm tra cấu hình sector `chuyenmon` trong hub và backend.
   - Kiểm tra định dạng trích xuất ngày ký số từ chuỗi định dạng PDF `/M (D:20260925...)` -> `2026-09-25`.
   - Kiểm tra regex bóc tách số quyết định `.../QĐ-...`, ngày ký số và trích yếu.
   - Kiểm tra file `quanlyvanban-chuyenmon.html` có đủ các thành phần giao diện bắt buộc.
   - Chạy `node tests/vanban-chuyenmon-signature-smoke.js` đạt PASS 100%.

6. **Bước 6: Ghi nhật ký vào `docs/handoff/IMPLEMENT.md` và tạo lại `docs/handoff/.lock` nội dung `LOCK`**.

---

## Rủi ro
- **Xung đột tệp đính kèm khi chuyển sector**: Khi chuyển sector từ Hành chính sang Chuyên môn, nếu file đã lưu trên Google Drive dưới folder `HANH_CHINH`, liên kết xem/tải tệp vẫn giữ nguyên `drive_file_id` nên không bị mất file. Khi sao chép (copy), cần nhân bản bản ghi trong `office_document_files` để cả 2 văn bản đều truy cập được tệp đính kèm.
- **Văn bản ký số có nhiều chữ ký**: Một số văn bản có cả chữ ký nháy của chuyên viên và chữ ký số chính thức của thủ trưởng. Cần ưu tiên chữ ký số của cơ quan/thủ trưởng (thường ở trang cuối hoặc có thời gian ký mới nhất).

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/vanban-chuyenmon-signature-smoke.js` -> PASS 100%.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `quanlyvanban.html`: Hiển thị đầy đủ 3 lĩnh vực (Hành chính, Chuyên môn, Đảng). Bấm vào Chuyên môn mở đúng trang `quanlyvanban-chuyenmon.html`.
   - Mở `quanlyvanban-hanhchinh.html`:
     + Tick chọn 1 hoặc nhiều văn bản -> Hiện thanh tác vụ -> Bấm "Chuyển sang Chuyên môn".
     + Mở `quanlyvanban-chuyenmon.html` -> Thấy các văn bản vừa chuyển xuất hiện đầy đủ thông tin và tệp đính kèm.
   - Kiểm tra nhận diện văn bản ký số:
     + Chọn file PDF có chữ ký số điện tử (dấu đỏ điện tử / quyết định ký số).
     + Hệ thống tự động trích xuất đúng Số văn bản (dạng `.../QĐ-...`) và Ngày ký số điện tử điền tự động vào ô Ngày văn bản.

---

## Tiêu chí nghiệm thu
- Có tab Chuyên môn hoạt động độc lập, quản lý văn bản chuyên môn riêng biệt.
- Tab Hành chính có checkbox tick chọn và nút chuyển/sao chép văn bản sang Chuyên môn nhanh chóng, tiện lợi.
- Hệ thống tự động nhận diện được Số văn bản và Ngày ký số của các văn bản/quyết định ký số điện tử trực tiếp trong ứng dụng.
- Tất cả các bài test kiểm thử tự động đều PASS.
