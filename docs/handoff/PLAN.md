# PLAN: Sửa lỗi phân quyền và truy cập Quản lý văn bản (quanlyvanban)

## 1. Hiện trạng & Nguyên nhân gốc rễ

1. **Không thấy Quản lý văn bản trong phân quyền:**
   - Trong `admin.html`, danh sách phân quyền tính năng theo tài khoản (`USER_FEATURE_GROUPS` và `CLIENT_FEATURE_CHECKS`) thiếu mục `quanlyvanban`.
   - Khi Admin cấp tài khoản Giáo viên mới, mặc định các quyền bị rỗng `[]` thay vì nạp `defaultTeacherPages` (đã có sẵn `quanlyvanban`).
   - Khi đăng nhập vào `index.html`, thẻ Quản lý văn bản chỉ xuất hiện nếu `allowed_pages` có `quanlyvanban`. Nếu tài khoản chưa được gán quyền thì thẻ này hoàn toàn biến mất.
   - Đối với Học sinh (`role: student`), `quanlyvanban` bị chặn hoàn toàn vì nằm trong `teacherOnlyPages`.

2. **Mở bằng link bị trắng trang:**
   - Người dùng thường truy cập qua link rút gọn hoặc URL không có đuôi `.html` (`/quanlyvanban`). Trong `.htaccess` chưa có RewriteRule từ `quanlyvanban` sang `quanlyvanban.html`.
   - Khi truy cập trực tiếp file HTML (`quanlyvanban.html` hoặc `quanlyvanban-*.html`), nếu tài khoản đã đăng nhập nhưng chưa được cấp quyền `quanlyvanban`, `access-control.js` chặn và điều hướng về `index.html`. Nếu không có thông báo hoặc tài khoản khách (guest) gặp lỗi CDN / security-guard thì dẫn đến trắng trang.

## 2. Giải pháp thực hiện (Handoff cho Coder)

1. **Cập nhật `admin.html`:**
   - Bổ sung `quanlyvanban` vào `CLIENT_FEATURE_CHECKS`, `FEATURE_NAMES` và `USER_FEATURE_GROUPS` (mục Công cụ trên hub giáo viên).
   - Khi chọn role Giáo viên trong form tạo mới tài khoản, tự động tích chọn `defaultTeacherPages` (trong đó có `quanlyvanban`).

2. **Cập nhật `.htaccess`:**
   - Thêm RewriteRule hỗ trợ URL thân thiện:
     ```apache
     RewriteRule ^quanlyvanban/?$ quanlyvanban.html [L,QSA]
     RewriteRule ^quanlyvanban-(hanhchinh|chuyenmon|dang)/?$ quanlyvanban-$1.html [L,QSA]
     ```

3. **Cập nhật `access-control.js`:**
   - Đảm bảo `pageKeys` nhận diện đúng URL khi không có đuôi `.html` (`quanlyvanban`).
   - Khi tài khoản giáo viên chưa được cấp quyền, hiển thị thông báo rõ ràng kèm nút quay lại thay vì bị trắng trang hoặc chuyển hướng đột ngột.

## 3. Các file cần chỉnh sửa
- `admin.html`
- `.htaccess`
- `access-control.js`
