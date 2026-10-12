# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Thư mục Staging và Endpoint `save_upload_stage` trên backend (`api/vanban.php`)**: Đã triển khai đầy đủ `vbd_staging_dir()`, lưu tệp đệm vào `storage/vanban/staging/{document_id}/`, tạo `.htaccess` chặn truy cập trực tiếp, gán mã `staging:{doc_id}:{stored_name}`, phản hồi tức thì 1–2 giây không chờ Drive.
2. **Endpoint `sync_drive_file` và tự động xóa tệp đệm (`api/vanban.php`)**: Đã triển khai đầy đủ, tận dụng `drive_folder_id`, gọi `drive_upload_file()`, cập nhật ID Drive thật và link xem/tải, gọi `@unlink()` xóa sạch tệp đệm và `@rmdir()` xóa thư mục con nếu rỗng (dung lượng file đệm về 0).
3. **Xem/tải trước tệp staging (`action=file`)**: Đã hỗ trợ phục vụ tệp trực tiếp từ đĩa khi tệp mang tiền tố `staging:` trước khi sang Drive.
4. **Tự động dọn rác Staging (`vbd_clean_orphan_staging`)**: Đã tích hợp vào `list`, `save`, `save_upload`, `save_upload_stage`. Xóa tệp đã sync xong hoặc mồ côi > 24h, giữ tệp đang chờ.
5. **Frontend lưu tức thì và đồng bộ ngầm (`vanban-app.js`)**: `saveDocument` gom tệp đính kèm gửi `save_upload_stage` trong 1 request, tách đợt nếu > 50 MB, đóng modal và báo thành công ngay; hàm `syncPendingStagedFiles()` tự động đồng bộ ngầm và cập nhật chip Drive.
6. **Bảo toàn phạm vi**: Không đổi schema bảng MySQL, không sửa cấu hình Service Account, không can thiệp các module khác.

## Test đã chạy
1. `php -l api/vanban.php`: PASS — không có lỗi cú pháp.
2. `node tests/vanban-staging-sync-smoke.js`: PASS — kiểm thử đầy đủ lưu staging, sync Drive, xóa file đệm (`unlink`), verify dung lượng đệm = 0, GC dọn rác, frontend batching và chip.
3. `node tests/vanban-display-saved-smoke.js`: PASS.
4. `node tests/vanban-chuyenmon-signature-smoke.js`: PASS.
5. `node tests/vanban-ocr-clipboard-smoke.js`: PASS.

## Pass / Fail từng tiêu chí
- [x] Lưu văn bản và tệp vào Staging tức thì: PASS
- [x] Đồng bộ sang Google Drive thành công: PASS
- [x] Tự động xóa sạch tệp trên hosting sau khi sync (bảo vệ 3GB): PASS
- [x] Xem/tải tệp đệm trước khi sang Drive: PASS
- [x] Quét dọn tệp mồ côi định kỳ (Garbage Collection): PASS
- [x] Không ảnh hưởng các luồng và kiểm thử hiện có: PASS

## Bug
Không phát hiện bug.
