# IMPLEMENT: Nâng cấp Padlet — màu chữ tiêu đề, sửa bài đăng, gallery nhiều ảnh

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### `api/padlet.php`
- Migration: thêm cột `padlet_boards.title_color VARCHAR(30) DEFAULT NULL AFTER color_mode`.
- `padlet_title_color()`: validate hex / tên màu (tối đa 30 ký tự).
- `save-board`: lưu `title_color`; nếu client không gửi field thì giữ giá trị cũ khi update.
- `edit-post`: quyền `$isOwner || $isAuthor`; cập nhật `body` / `link_url` / `card_color`; xóa tệp theo `deleted_file_ids` qua `padlet_delete_drive_files_by_ids`; nhận upload `files[]` mới (tối đa 5 tệp còn lại).

### `padlet_ht.html`
- Settings → Bảng màu: swatch màu tiêu đề + `input type="color"` + đặt lại mặc định.
- Header bảng (quản trị): nút palette cạnh tiêu đề, áp dụng `title_color` inline (`color` / `caret-color !important`).
- `postMediaHtml`: 1 ảnh full; ≥2 ảnh → lưới `grid-cols-2/3`, click mở preview.
- Thẻ bài: nút **Sửa** khi `state.canManage || p.can_delete`.
- Modal `#editPostModal` + `openEditPostModal` / `submitEditPost` (sửa nội dung, link, màu thẻ, xóa tệp cũ, thêm tệp mới; hỗ trợ paste ảnh khi modal mở).

### Tests
- `tests/padlet-ui-smoke.js`: title color UI, edit modal, gallery grid, `edit-post`.
- `tests/padlet-ownership-smoke.js`: migrate/`padlet_title_color`/`save-board`, quyền `edit-post`, xóa tệp an toàn.

## Test đã chạy

- `node tests/padlet-ui-smoke.js` — PASS
- `node tests/padlet-ownership-smoke.js` — PASS

Không mở rộng quyền phân quyền cơ bản ngoài PLAN. Chưa verify click UI trong browser (không có browser tool trong session); hợp đồng nguồn đã được smoke khóa. Cần `/verify` trên Antigravity.
