# IMPLEMENT: Lĩnh vực Chuyên môn, chuyển văn bản và nhận diện ký số

## Đã làm
- Hub `quanlyvanban.html` có 3 thẻ lĩnh vực. `vanban-hub.js` thêm sector `chuyenmon` (Chuyên môn, indigo, `quanlyvanban-chuyenmon.html`). `access-control.js` gắn trang này với quyền `quanlyvanban`.
- Trang mới `quanlyvanban-chuyenmon.html` đặt `window.VANBAN_SECTOR = 'chuyenmon'` và dùng `vanban-app.js`.
- `api/vanban.php`: `vbd_sector()` nhận `chuyenmon`, nhãn "Chuyên môn", thư mục Drive `CHUYEN_MON`. Action `transfer_sector` đổi sector của các văn bản thuộc `owner_id` hiện tại và chuyển thư mục tệp cục bộ. Action `copy_sector` nhân bản bản ghi và các dòng `office_document_files` (giữ `drive_file_id`).
- Tab Hành chính: checkbox từng dòng, nút "Chuyển sang Chuyên môn", thanh "Chuyển đã chọn sang Chuyên môn" / "Sao chép đã chọn sang Chuyên môn", và hai nút tương ứng trong modal chi tiết.
- Nhận diện PDF: đọc `/Type /Sig`, ngày `/M (D:YYYYMMDD...)`, người ký `/Name`; đọc annotation; đọc thêm trang cuối. Dòng `Ngày ký`, `ký số`, `thời gian ký` không còn bị `vbd_preprocess_source()` xóa. Ngày ký số chỉ điền khi header không có ngày ban hành. Regex nhận `123/QĐ-UBND`, `45 / QĐ - SGDĐT`, `12/KH-THCS`.
- Nút "Dán nhanh từ Clipboard" và dán ảnh vùng chữ ký vào ô nội dung. Ảnh cần Mistral OCR; PDF ký số đọc trực tiếp từ file.

## Kiểm thử
- `node tests/vanban-chuyenmon-signature-smoke.js` → PASS (exit 0).
- Chưa mở trình duyệt (không có công cụ trình duyệt trong phiên này). Bước sau: Antigravity IDE, chat mới, `/verify`.

## File
- `quanlyvanban-chuyenmon.html`
- `quanlyvanban.html`
- `quanlyvanban-hanhchinh.html`
- `vanban-hub.js`
- `vanban-app.js`
- `api/vanban.php`
- `access-control.js`
- `tests/vanban-chuyenmon-signature-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`
