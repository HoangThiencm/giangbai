# IMPLEMENT: Nút "Thêm bình luận" và định danh người bình luận (Padlet)

## Đã làm
- `padlet_ht.html` `postCard`: thanh `post-action` hiện khi `canManage || can_delete || comments_enabled`. Nút **Thêm bình luận** (`far fa-comment-dots`, gọi `openComments`) chỉ khi `b.comments_enabled`. Duyệt, Từ chối, Ghim, Sửa, Xóa giữ nguyên điều kiện quản lý / `can_delete`.
- `#commentModal`: badge `#commentUserBadge` / `#commentUserName`; khối khách có nhãn, ô họ tên `required` (placeholder bắt buộc), ô lớp/vai trò.
- `openComments`: tài khoản đăng nhập hiện badge và ẩn form khách (bỏ `required` trên ô họ tên); khách điền sẵn `localStorage` `padlet_guest_name` / `padlet_guest_role`, không có tên thì lấy `#postAuthorName`. Danh sách bình luận có avatar chữ cái đầu, tên đậm, badge vai trò, thời gian.
- `submitComment`: khách thiếu họ tên thì toast và focus, không gửi. Gửi thành công thì nhớ localStorage (khách), xóa nội dung, toast, `loadBoard()`, rồi mở lại danh sách nếu modal còn mở.

## Smoke
- `node tests/padlet-ownership-smoke.js` — PASS
- `node tests/padlet-ui-smoke.js` — PASS
- `node tests/padlet-comment-ui-smoke.js` — PASS

## Ngoài phạm vi
- Không đổi `api/padlet.php` (server đã bắt buộc họ tên và gán vai trò Giáo viên/Học sinh khi đã đăng nhập).
- Chưa commit, chưa push. Kiểm tra trình duyệt để `/verify`.
