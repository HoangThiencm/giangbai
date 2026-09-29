# IMPLEMENT: Hòa giải xung đột merge main / origin/main

## Đã làm
- Gỡ `docs/handoff/.lock` trước khi sửa, giải quyết 10 path unmerged.
- `api/vanban.php`: giữ `vbd_optional_user` / `vbd_current_user` cho xem công khai (`list`, `file`, `reminder_count`, `drive_check`); giữ `vbd_is_admin`, `vbd_copy_local_storage`, `vbd_copy_document_files`, `transfer_sector` / `copy_sector` (không xóa bản gốc) và `copy_from_hanhchinh`. Khách không lọc theo `owner_id`. Không xóa tệp Google Drive còn được văn bản khác tham chiếu.
- `vanban-app.js`: khách ẩn thêm/sửa/xóa và nút chuyển sang Chuyên môn; giữ nút đăng nhập, “Lấy từ Hành chính”, chuyển/sao chép khi đã đăng nhập, và dán clipboard/OCR.
- `vanban-hub.js`, `quanlyvanban.html`: 3 lĩnh vực, mô tả xem công khai.
- `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`, `quanlyvanban-chuyenmon.html`: lấy bản remote (UTF-8, indigo, clipboard, thanh chuyển/sao chép hàng loạt).

## Kiểm tra
- `node --check` trên `vanban-app.js`, `vanban-hub.js`, `access-control.js`: không lỗi cú pháp.
- `py tests/vanban-chuyenmon-root-smoke.py`: 27/27 PASS (kể cả đối chiếu ngoặc `api/vanban.php` vì máy không có `php`).
- `node tests/vanban-chuyenmon-signature-smoke.js`: PASS.
- `node tests/sodiem-smoke.js`: PASS.

## Chưa làm
- `git push origin main` chờ `/verify` PASS (không force push).
