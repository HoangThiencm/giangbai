# Báo cáo triển khai

## Phạm vi đã thực hiện

- `nopbai.html`:
  + Loại bỏ thẻ `<script src="access-control.js"></script>` khỏi `nopbai.html` vì đây là cổng nộp bài công khai, tuyệt đối không đòi hỏi đăng nhập.
  + Thay liên kết header sang chính trang hiện tại để giữ nguyên đường link nộp và không điều hướng về trang chủ/đăng nhập.
  + Thêm huy hiệu và thông báo xác nhận rằng người nộp không cần tài khoản hay mật khẩu đăng nhập.
  + Làm rõ lựa chọn mã cá nhân là phương án phụ.
- `access-control.js`: Loại bỏ `'nopbai.html': 'nopbai'` khỏi `pageKeys` để trang nộp bài công khai không bị route guard chặn. (`nopbai-quanly.html` vẫn được bảo vệ bởi quyền `nopbai`).
- `nopbai-quanly.html`: Thêm chú thích và tooltip cho link chung/link cá nhân, đồng thời cập nhật thông báo sau khi sao chép để phân biệt hai loại link.
- `tests/nopbai-report-link-smoke.js`: Thêm kiểm tra tĩnh không liên kết đến `index.html` hoặc `login.html`, không nạp `access-control.js`, có thông báo không cần đăng nhập và vẫn giữ luồng chọn người nộp.

## Kiểm thử

- `node tests/nopbai-report-link-smoke.js` — PASS (`nopbai report link smoke: passed`).
- `node tests/teacher-permissions-smoke.js` — PASS.
- `git diff --check` — PASS.

## Vấn đề còn lại

Không có.
