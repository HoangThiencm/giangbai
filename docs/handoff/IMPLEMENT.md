# IMPLEMENT: Phân quyền và truy cập Quản lý văn bản

Đã sửa đúng `docs/handoff/PLAN.md`. Chưa commit, chưa push.

## admin.html

- Thêm `quanlyvanban` vào `CLIENT_FEATURE_CHECKS`, `FEATURE_NAMES` ("Quản lý văn bản") và nhóm `USER_FEATURE_GROUPS` "Công cụ AI trên hub giáo viên".
- Form tạo tài khoản: khi chọn vai trò Giáo viên mà chưa tích trang nào, danh sách quyền nạp `defaultTeacherPages` (có `quanlyvanban`). Sau khi tạo xong, form giáo viên cũng trở về bộ quyền mặc định này.

## .htaccess

- `^quanlyvanban/?$` → `quanlyvanban.html`
- `^quanlyvanban-(hanhchinh|chuyenmon|dang)/?$` → `quanlyvanban-$1.html`
- Cả hai dùng `[L,QSA]`.

## access-control.js

- Tên file không có đuôi được gắn `.html` trước khi tra `pageKeys`, nên `/quanlyvanban` và `/quanlyvanban-hanhchinh` vẫn ra khóa `quanlyvanban`.
- Giáo viên chưa có quyền `quanlyvanban` thấy thông báo "Không đủ quyền" và nút "Quay lại trang chủ", không `alert` rồi chuyển hướng ngay.

## Kiểm tra

- `node --check access-control.js`: thoát 0.
- Kiểm tra trình duyệt để `/verify`.
