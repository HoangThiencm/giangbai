# VERIFY: Lĩnh vực Chuyên môn, chuyển/sao chép văn bản và nhận diện ký số

## Kết luận
PASS

## Đối chiếu scope
1. **Lĩnh vực Chuyên môn (`chuyenmon`)**:
   - `vanban-hub.js`: Đã bổ sung cấu hình sector `chuyenmon` (Chuyên môn, icon `fa-graduation-cap`, theme indigo, trang `quanlyvanban-chuyenmon.html`). Hàm `sectorOf(doc)` nhận dạng chính xác sector `chuyenmon`.
   - `quanlyvanban.html`: Đã cập nhật mô tả tổng quan và lưới thẻ lĩnh vực `md:grid-cols-2 lg:grid-cols-3` hiển thị đồng thời cả 3 mục Hành chính, Chuyên môn và Đảng.
   - `quanlyvanban-chuyenmon.html`: Đã tạo mới hoàn chỉnh với `window.VANBAN_SECTOR = 'chuyenmon'`, đồng bộ theme màu xanh indigo, liên kết `vanban-app.js` và `access-control.js`.
   - `access-control.js`: Đã khai báo route `'quanlyvanban-chuyenmon.html': 'quanlyvanban'` đảm bảo phân quyền chuẩn cho giáo viên và quản trị viên.
   - `api/vanban.php`: Hàm `vbd_sector()` cho phép `'chuyenmon'`, `vbd_sector_label()` trả về "Chuyên môn", và thư mục Drive đồng bộ `CHUYEN_MON`.

2. **Chuyển / sao chép văn bản từ Hành chính sang Chuyên môn**:
   - Giao diện `quanlyvanban-hanhchinh.html`: Đã thêm thanh công cụ hàng loạt `#sectorBulkBar` ("Chuyển đã chọn sang Chuyên môn", "Sao chép đã chọn sang Chuyên môn").
   - `vanban-app.js`: Đã gắn checkbox chọn từng văn bản, hiển thị nút thao tác nhanh "Chuyển sang Chuyên môn", và thêm 2 nút tương ứng trong modal chi tiết văn bản `#documentDetailModal`.
   - `api/vanban.php`: Đã triển khai hoàn chỉnh 2 action `transfer_sector` (chuyển sector và di chuyển lưu trữ cục bộ) và `copy_sector` (nhân bản bản ghi văn bản cùng toàn bộ bản ghi tệp đính kèm trong `office_document_files`), kiểm tra quyền `owner_id` chặt chẽ trong transaction.

3. **Nhận diện Số văn bản và Ngày ký số / Quyết định ký số**:
   - `vanban-app.js`: Đã bổ sung module `VanbanParse` bóc tách trực tiếp metadata chữ ký số từ byte buffer PDF (`/Type /Sig`, trường `/M`, trường `/Name`). Hàm `extractPdfTextLayer` đọc thêm `page.getAnnotations()` và quét thêm trang cuối cùng `pdf.numPages` (nơi có con dấu ký số của thủ trưởng).
   - `api/vanban.php`: Danh sách `$skipKeywords` trong `vbd_preprocess_source()` đã loại bỏ các từ khóa ngày ký số; hàm `vbd_latest_signature_date()` tự động lấy ngày ký mới nhất làm `document_date` dự phòng khi văn bản chưa có ngày ở phần tiêu đề; hàm `vbd_find_document_number()` nhận diện chuẩn xác các số quyết định dạng `123/QĐ-UBND`, `45 / QĐ - SGDĐT`, `12/KH-THCS`.
   - Tiện ích dán nhanh: Đã tích hợp nút "Dán nhanh từ Clipboard" và bắt sự kiện paste ảnh trực tiếp vào modal.

## Test đã chạy
- Lệnh: `agy-node tests/vanban-chuyenmon-signature-smoke.js`
- Kết quả: PASS (exit code 0).
- Nội dung kiểm tra:
  + Cấu hình route, sector trong `access-control.js`, `vanban-hub.js`, `quanlyvanban.html`.
  + Schema và endpoint trong `api/vanban.php` (`vbd_sector`, `transfer_sector`, `copy_sector`, `vbd_find_document_number`, `vbd_latest_signature_date`).
  + Giao diện HTML của `quanlyvanban-chuyenmon.html` và `quanlyvanban-hanhchinh.html`.
  + Logic trích xuất chữ ký số PDF, bóc tách ngày ký dạng `D:YYYYMMDD...`, định dạng số quyết định có dấu cách / gạch chéo, và trích xuất ngày ký mới nhất từ khối ký số.

## Pass / Fail từng tiêu chí
- Mở tab Chuyên môn và trang `quanlyvanban-chuyenmon.html`: PASS
- Checkbox tick chọn và nút chuyển/sao chép sang Chuyên môn trong tab Hành chính: PASS
- Backend xử lý chuyển/sao chép sector an toàn: PASS
- Nhận diện trực tiếp chữ ký số PDF, ngày ký và số quyết định: PASS
- Smoke test tự động chạy thành công: PASS

## Bug
- Không phát hiện lỗi.
