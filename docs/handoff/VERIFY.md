# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] PHẦN 1 (Đổi SmartQuiz thành Game giáo dục trên `index.html`):
  - [x] Đổi link trong `TOOL_PAGE_LINKS.smartquiz` thành `'https://www.hoangthiencm.id.vn/trochoi.html'`.
  - [x] Đổi thẻ công cụ giáo viên `#mainToolsGrid` sang `href="https://www.hoangthiencm.id.vn/trochoi.html"` và tiêu đề "Game giáo dục".
  - [x] Đổi mục hoạt động học sinh trong `setupStudentPortal` sang tiêu đề "Game giáo dục" và `url: 'https://www.hoangthiencm.id.vn/trochoi.html'`.
  - [x] Bổ sung assert kiểm tra link `trochoi.html` và từ khóa `Game giáo dục` trong `tests/change-password-smoke.js`.
- [x] PHẦN 2 (Chức năng Đổi mật khẩu cho người dùng):
  - [x] Tạo endpoint `api/change_password.php` (kiểm tra session, xác thực `password_verify`, cập nhật `password_hash`).
  - [x] Tạo module `js/change-password.js` (modal DOM, ẩn/hiện mật khẩu, kiểm tra client-side, gọi API có cookie phiên).
  - [x] Thêm nút `#btnOpenChangePassword` trên Navbar `index.html` (dành cho cả Giáo viên và Học sinh).
  - [x] Nhúng `js/change-password.js` vào `index.html`.
  - [x] Tạo và cập nhật `tests/change-password-smoke.js`.

## Test đã chạy
- `node tests/change-password-smoke.js`: PASS.
- `node tests/user-ai-settings-smoke.js`: PASS.
- `node tests/canvas-tabs-permissions-smoke.js`: PASS.
- `git diff --check`: PASS.

## Pass / Fail từng tiêu chí
- Tiêu chí 1 (Thay SmartQuiz bằng Game giáo dục & link `https://www.hoangthiencm.id.vn/trochoi.html`): PASS
- Tiêu chí 2 (Chức năng Đổi mật khẩu cho Giáo viên và Học sinh): PASS
- Tiêu chí 3 (Test tự động và hồi quy): PASS

## Bug
Không có bug nào được phát hiện.
