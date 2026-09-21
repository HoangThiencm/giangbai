# IMPLEMENT: Đổi Mật Khẩu Cho Người Dùng

Đã triển khai đúng `docs/handoff/PLAN.md` trong phạm vi đã duyệt.

## Thay đổi

- Thêm `api/change_password.php`: chỉ nhận POST, yêu cầu session `user_id`, xác thực mật khẩu hiện tại bằng `password_verify`, kiểm tra mật khẩu mới và cập nhật hash mới bằng `password_hash`.
- Thêm `js/change-password.js`: modal tự tạo DOM, đóng bằng nút/overlay/Escape, ẩn-hiện mật khẩu, kiểm tra dữ liệu phía trình duyệt và gọi endpoint với cookie phiên.
- Cập nhật `index.html`: thêm nút **Đổi mật khẩu** trước Đăng xuất và nạp module mới. `setupStudentPortal` chỉ tiếp tục ẩn nút cài đặt AI; không ẩn chức năng đổi mật khẩu với học sinh.
- Thêm `tests/change-password-smoke.js` để kiểm tra cấu trúc giao diện, module và endpoint.

## Kiểm tra

- `node tests/change-password-smoke.js`: PASS.
- `node tests/user-ai-settings-smoke.js`: PASS.
- `node tests/canvas-tabs-permissions-smoke.js`: PASS.
- `git diff --check`: PASS; Git chỉ cảnh báo quy đổi LF/CRLF.
- `php -l api/change_password.php`: không chạy được vì môi trường hiện tại không có lệnh `php` trong PATH.

## Vấn đề còn lại

- Chưa kiểm thử thủ công qua trình duyệt hoặc với cơ sở dữ liệu thật; cần chạy bước `/verify` theo quy trình dự án.
