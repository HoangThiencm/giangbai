# IMPLEMENT: Padlet xem PDF Google Drive

## Đã làm
1. `api/padlet.php`: thêm `padlet_share_uploaded_file()` gọi `drive_share_file_anyone` trong `try/catch`. Lỗi Drive chỉ ghi `error_log`, không trả 500.
2. Gọi chia sẻ `anyone` + `reader` ngay sau `drive_upload_file` ở `post` và `edit-post`.
3. Khi `GET action=board`, thử chia sẻ lại mọi `drive_file_id` đang gắn bài (kể cả tệp cũ).
4. `padlet_ht.html`: khối `documentEmbedHtml` có nút chữ **Mở tệp ngoài** và dòng *Nếu không tải được trên điện thoại, bấm Mở tệp ngoài*.
5. `#previewModal` có `#previewExternalLink` (**Mở tab mới**). `previewFile()` gán `href` bằng `view_url` hoặc link Drive `/view`.
6. `tests/padlet-ui-smoke.js` kiểm tra nút mở ngoài trên thẻ bài và modal.

## Chưa đụng
- Không sửa `api/config.php` (file hosting, không nằm trong repo làm việc).
- Không đổi module ngoài Padlet.

## Cấu hình hosting (bước thủ công)
Trong `api/config.php` trên hosting, đặt:

```php
define('GOOGLE_DRIVE_SHARE_MODE', 'anyone');
```

Padlet vẫn gọi `drive_share_file_anyone` kể cả khi hằng số đang là `private`. Nếu Google Workspace chặn chia sẻ ra ngoài miền, bài viết vẫn lưu; giáo viên dùng **Mở tệp ngoài** / **Mở tab mới** sau khi đăng nhập tài khoản trường.

Tệp cũ (ví dụ `CONG TAC THANG 10.pdf`) được thử chia sẻ lại mỗi lần mở bảng. Nếu API từ chối, quản trị vào Google Drive và cấp **Bất kỳ ai có đường liên kết đều có thể xem** cho thư mục bảng đó.

## Smoke
- `node tests/padlet-ownership-smoke.js` — passed
- `node tests/padlet-ui-smoke.js` — passed
- `node tests/padlet-comment-ui-smoke.js` — passed

Chưa kiểm tra trình duyệt / iPhone. Phần đó thuộc `/verify`.

## Bước tiếp
Antigravity IDE, chat mới: `/verify`
