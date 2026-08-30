# IMPLEMENT: Đưa Xây dựng Phụ lục ra thư mục gốc và đồng bộ quyền truy cập

## Phạm vi đã triển khai

- Tạo ứng dụng tại `xaydungphuluc.html` ở thư mục gốc, đồng cấp với Portal.
- Giữ URL cũ bằng một trang chuyển hướng từ `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`.
- Bổ sung Security Guard, kiểm soát truy cập và tự nhận các Gemini API key đã lưu từ KHBD.
- Đồng bộ liên kết Portal, cấu hình Admin, backend phân quyền, cấu hình global và các smoke test.
- Không sửa `PLAN.md`, `VERIFY.md` hoặc `.lock`; không commit/push.

## File thay đổi

- `xaydungphuluc.html`: ứng dụng chính ở thư mục gốc; nhúng `js/security-guard.js` và `access-control.js` đầu `head`, nút Trang chủ trỏ `index.html`, đọc key theo tài khoản và tất cả kho key dự phòng trong kế hoạch.
- `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`: trang chuyển hướng tương thích về URL gốc.
- `index.html`, `admin.html`: dùng URL gốc; Admin merge an toàn các trang cấu hình trả về từ backend.
- `api/helpers.php`, `access-control.js`, `global_config.json`: đăng ký tính năng `xaydungphuluc` cho danh mục trang, không gian giáo viên, feature key, route access-control và feature toàn cục.
- `tests/xaydungphuluc-smoke.js`, `tests/xaydungphuluc-integration-smoke.js`: kiểm tra vị trí mới, bảo mật, dùng chung key, chuyển hướng cũ và các ánh xạ tích hợp.

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `git diff --check` — PASS.

## Vấn đề còn lại

- Chưa thực hiện kiểm thử trình duyệt production cho F12/DevTools, đăng nhập giáo viên và key thật; bước này thuộc `/verify`.
- Không thể chạy `php -l api/helpers.php` vì môi trường hiện tại không cài PHP CLI.
