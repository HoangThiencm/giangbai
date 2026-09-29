# IMPLEMENT — Giữ bản gốc Hành chính khi chuyển sang Chuyên môn

Trạng thái: ĐÃ SỬA lỗi VERIFY (UTF-8 stdout/stderr trong smoke test). Chưa commit.

## Đã sửa

- `api/vanban.php`
  - `transfer_sector` và `copy_sector` cùng tạo bản ghi mới ở sector đích. Không còn `UPDATE office_documents SET sector` và không gọi `vbd_move_local_storage`.
  - Thông điệp chuyển: bản gốc tại Hành chính được giữ nguyên.
  - Thêm `vbd_copy_local_storage`. `vbd_copy_document_files` nhận `$fromDoc`, `$toDoc`, tạo lại `view_url`/`download_url` cho tệp cục bộ theo ID mới, rồi sao chép thư mục tệp.
  - `vbd_delete_document_file_storage` đếm `drive_file_id` còn được văn bản khác dùng. Còn tham chiếu thì không gọi `drive_delete_file`.
- `vanban-app.js`
  - `moveToChuyenMon`: câu xác nhận nói rõ bản gốc Hành chính vẫn được lưu trữ; toast dùng `data.message`; sau đó `await load()`.
  - Giữ `transfer_sector`, `copy_sector`, `data-action="transfer"`, `data-detail-action="transfer|copy"`, nhãn nút.
- `quanlyvanban-hanhchinh.html`: không sửa. `transferSelectedBtn` và `copySelectedBtn` giữ nguyên.
- `tests/vanban-chuyenmon-root-smoke.py`: tạo mới. Sau các import, gọi `sys.stdout.reconfigure(encoding="utf-8")` và `sys.stderr.reconfigure(encoding="utf-8")` khi stream hỗ trợ `reconfigure`, để `print()` tiếng Việt không lỗi trên console Windows mã cp1252.

## Kiểm tra

- `py tests/vanban-chuyenmon-root-smoke.py`: exit 0. 27/27 PASS và dòng tổng `PASS: giữ bản gốc Hành chính khi chuyển sang Chuyên môn.`
- Chạy lại cùng script khi stdout/stderr bắt đầu ở `cp1252`: exit 0, cùng 27/27 PASS, không `UnicodeEncodeError`.
