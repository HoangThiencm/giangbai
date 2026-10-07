# VERIFY: Khắc phục lỗi xem tệp PDF Google Drive trong Padlet

## Kết luận
PASS

## Đối chiếu scope
- Backend (`api/padlet.php`): Đã bổ sung hàm `padlet_share_uploaded_file()` gọi `drive_share_file_anyone()` bọc trong `try/catch` chống sập. Tự động cấp quyền `anyone` + `reader` khi tải lên mới (`action=post`), cập nhật bài (`action=edit-post`) và tự động kích hoạt chia sẻ cho các tệp hiện hữu khi tải dữ liệu bảng (`action=board`). Đạt đúng phạm vi plan.
- Frontend (`padlet_ht.html`): Thêm nút chữ rõ ràng **Mở tệp ngoài** và dòng chỉ dẫn *"Nếu không tải được trên điện thoại, bấm Mở tệp ngoài"* tại `documentEmbedHtml`. Bổ sung nút **Mở tab mới** (`#previewExternalLink`) trên thanh tiêu đề của `#previewModal`. Hàm `previewFile()` gán tự động URL mở ngoài. Đạt đúng phạm vi plan.
- Cấu hình & hướng dẫn: Giữ nguyên tài liệu hướng dẫn đặt `GOOGLE_DRIVE_SHARE_MODE = 'anyone'` trong `api/config.php` trên hosting.

## Test đã chạy
- `node tests/padlet-ownership-smoke.js` — PASS (toàn bộ quyền duyệt, ghim, sửa, xóa giữ nguyên chuẩn bảo mật).
- `node tests/padlet-ui-smoke.js` — PASS (kiểm tra nút mở tệp ngoài, hướng dẫn cookie điện thoại, nút mở tab mới trên preview modal).
- `node tests/padlet-comment-ui-smoke.js` — PASS (tính năng bình luận và định danh người dùng hoạt động bình thường).

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Tệp tải lên Padlet tự động kích hoạt quyền chia sẻ công khai (`anyone` + `reader`) — PASS.
- Tiêu chí 2: Giao diện thẻ bài và modal xem tệp có lối tắt mở ngoài/tab mới rõ ràng, xử lý tình huống trình duyệt di động chặn iframe cookie — PASS.
- Tiêu chí 3: Không làm hỏng các tính năng bình luận, duyệt, sửa, xóa hiện có — PASS.

## Bug
Không phát hiện lỗi.
