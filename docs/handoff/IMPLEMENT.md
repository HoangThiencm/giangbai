# IMPLEMENT: Staging văn bản rồi đồng bộ Google Drive

## Đã làm
1. `api/vanban.php` thêm thư mục `storage/vanban/staging/{document_id}/`, tạo khi cần và ghi `.htaccess` chặn truy cập trực tiếp.
2. `action=save_upload_stage` lưu văn bản, chuyển tệp vào staging, ghi `office_document_files` với `drive_file_id = staging:{doc_id}:{stored_name}` (cắt tên để vừa `VARCHAR(160)`), `view_url`/`download_url` trỏ `action=file`. Trả `{ ok, document, staged_files }` ngay, không chờ Drive.
3. `action=sync_drive_file` nhận `file_id` hoặc `document_id`, kiểm tra quyền, dùng `office_documents.drive_folder_id` nếu đã có, không thì gọi `vbd_drive_folder()` một lần và lưu lại. Gọi `drive_upload_file()`, cập nhật mã Drive cùng link xem/tải, `unlink` tệp đệm và `rmdir` thư mục văn bản nếu rỗng.
4. `action=file` phục vụ cả tệp `staging:` và tệp `local:` khi người dùng bấm Xem/Tải trong lúc chưa sang Drive.
5. `vbd_clean_orphan_staging()` chạy ở `list`, `save`, `save_upload` và `save_upload_stage`: xóa tệp đĩa đã có mã Drive thật; xóa tệp không có dòng CSDL và cũ hơn 24 giờ; giữ tệp `staging:` còn chờ đồng bộ.
6. Xóa và sao chép văn bản gỡ hoặc copy đúng file staging. Mã `staging:` không bị tính là “đã có file Drive”.
7. `vanban-app.js`: có tệp đính kèm thì một `fetch` `FormData` tới `save_upload_stage` (tách đợt khi tổng vượt 50 MB, tệp lớn hơn 50 MB gửi riêng). Thanh tiến trình hiện “Đang lưu văn bản và tệp...”. Đóng modal, toast “Đã lưu văn bản”, rồi `syncPendingStagedFiles()` đồng bộ nền từng tệp. Chip hiện “Đang đồng bộ Drive”; xong thì icon Google Drive. Lần `load()` sau tiếp tục tệp `staging:` còn sót. `drive_file_id` dạng `staging:` không bị đưa vào link preview Drive.
8. Ba trang Hành chính, Chuyên môn, Đảng đổi cache `vanban-app.js?v=20261012-staging` để trình duyệt tải script mới.

## Chưa đụng
- Không đổi schema `office_documents` và `office_school_years`.
- Không đổi cấu hình Service Account Google Drive.
- Không sửa OCR, phân công, lịch, sổ điểm.
- `save_upload` và luồng chunk cũ vẫn còn cho client chưa cập nhật. Form hiện tại không đi qua chunk.

## Kiểm thử
- `php -l api/vanban.php`: không lỗi cú pháp. Máy không có `php` trên PATH; dùng PHP 8.3 portable.
- `node tests/vanban-staging-sync-smoke.js`: PASS.
  - Lưu văn bản và đưa PDF vào staging, tệp có trên đĩa, marker đúng.
  - Sync gọi upload với `drive_folder_id` đã lưu, ghi `drive_file_id = 1AbCDriveTestFileId`, link `drive.google.com`, `unlink` và thư mục staging của văn bản biến mất (dung lượng file đệm = 0).
  - Gọi sync lần hai không tải lên lại.
  - GC giữ staging còn chờ, xóa file đã có mã Drive, giữ mồ côi mới, xóa mồ côi quá 24 giờ.
  - Frontend: một request `save_upload_stage`, tách đợt 50 MB, toast đồng bộ, chip Drive sau khi sync.
- Bước upload HTTP của smoke test đi qua hook `vbd_drive_upload_handler` để không ghi tệp thật lên Shared Drive của nhà trường. Hàm production vẫn gọi `drive_upload_file()` khi hook không được gán.
- `node tests/vanban-display-saved-smoke.js`: PASS.
- Chưa mở trình duyệt để bấm Lưu trên trang văn bản.

## Bước tiếp
Antigravity IDE, chat mới: `/verify`
