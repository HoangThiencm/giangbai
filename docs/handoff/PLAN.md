# PLAN: Sửa lỗi trang Quản lý văn bản (quanlyvanban.html, quanlyvanban-hanhchinh.html, quanlyvanban-dang.html) không hiển thị dữ liệu

## Hiện trạng & Khẳng định an toàn dữ liệu
1. **Dữ liệu KHÔNG bị mất**:
   - Cơ sở dữ liệu MySQL (`office_documents`, `office_document_files`) và các tệp lưu trên Google Drive vẫn nguyên vẹn, API `api/vanban.php` vẫn hoạt động tốt.
2. **Nguyên nhân gốc rễ**:
   - Kiểm tra trực tiếp trên server hosting (`hoangthiencm.id.vn`): **toàn bộ các file JavaScript của module Quản lý văn bản đều bị 0 bytes**:
     * `vanban-hub.js`: 0 bytes (khiến `quanlyvanban.html` trống trơn mục "Chọn lĩnh vực").
     * `vanban-app.js`: 0 bytes (khiến `quanlyvanban-hanhchinh.html` và `quanlyvanban-dang.html` không chạy được script -> không hiển thị danh sách văn bản, không thấy tệp đính kèm, không thấy nội dung báo cáo trước đó).
     * `js/quanlyvanban-hanhchinh.bundle.js`: 0 bytes.
   - Do file script trên hosting bị rỗng, trình duyệt tải trang HTML về nhưng không có mã JavaScript để gọi API `api/vanban.php?action=list` và không có hàm để vẽ bảng danh sách, tệp đính kèm hay tóm tắt/nội dung báo cáo.
3. **Phân quyền trong `api/vanban.php`**:
   - Cần đảm bảo tài khoản `admin` / `superadmin` cũng xem và quản lý được văn bản giống như giáo viên (tránh lỗi 403 khi admin đăng nhập).

---

## Phạm vi thực hiện
1. **Cập nhật `api/vanban.php`**:
   - Cho phép vai trò `admin`, `superadmin` truy cập đầy đủ trong `vbd_current_user`.
2. **Cập nhật các trang HTML và file JS module Quản lý văn bản**:
   - `quanlyvanban.html`: tăng version query param `vanban-hub.js?v=20260928-hub-fix`.
   - `quanlyvanban-hanhchinh.html`: tăng version query param `vanban-app.js?v=20260928-app-fix`.
   - `quanlyvanban-dang.html`: tăng version query param `vanban-app.js?v=20260928-app-fix`.
   - `vanban-hub.js`: đảm bảo render giao diện skeleton/thẻ lĩnh vực ngay cả khi đang chờ dữ liệu.
   - `vanban-app.js`: đảm bảo các hàm render tệp đính kèm và nội dung báo cáo hoạt động mượt mà, bắt lỗi hiển thị rõ ràng nếu mất kết nối mạng.
3. **Đồng bộ FTP lên hosting**:
   - Trigger commit & push để GitHub Actions FTP Deploy tải lại đầy đủ toàn bộ file `vanban-hub.js`, `vanban-app.js` lên hosting (thay thế các file 0 bytes hiện tại).

---

## Ngoài phạm vi
- Không xóa hoặc thay đổi cấu trúc bảng database MySQL.
- Không can thiệp vào các tệp đã lưu trên Google Drive.

---

## File dự kiến tác động
- `api/vanban.php`
- `quanlyvanban.html`
- `quanlyvanban-hanhchinh.html`
- `quanlyvanban-dang.html`
- `vanban-hub.js`
- `vanban-app.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa handoff**:
   - Xóa `docs/handoff/.lock` nếu có.
2. **Bước 2: Cập nhật `api/vanban.php`**:
   - Cập nhật hàm `vbd_current_user`:
     ```php
     $role = (string)($user['role'] ?? '');
     if (!in_array($role, ['teacher', 'admin', 'superadmin'], true)) {
         respond(['error' => 'Chức năng quản lý văn bản chỉ dành cho giáo viên hoặc quản trị viên.'], 403);
     }
     ```
3. **Bước 3: Cập nhật version query params để ép hosting và trình duyệt nạp file mới**:
   - Trong `quanlyvanban.html`: `<script src="vanban-hub.js?v=20260928-hub-fix"></script>`
   - Trong `quanlyvanban-hanhchinh.html`: `<script src="vanban-app.js?v=20260928-app-fix"></script>`
   - Trong `quanlyvanban-dang.html`: `<script src="vanban-app.js?v=20260928-app-fix"></script>`
4. **Bước 4: Cập nhật `vanban-hub.js` và `vanban-app.js`**:
   - Thêm comment timestamp vào cuối file `vanban-hub.js` và `vanban-app.js` để đảm bảo file hash thay đổi, ép FTP Deploy Action bắt buộc phải upload lại toàn bộ nội dung file (loại bỏ hoàn toàn trạng thái 0 bytes).
5. **Bước 5: Ghi nhật ký & Khóa**:
   - Ghi nội dung vào `docs/handoff/IMPLEMENT.md`.
   - Tạo lại file `docs/handoff/.lock` nội dung `LOCK`.

---

## Tiêu chí nghiệm thu
- Truy cập `quanlyvanban.html`: Thẻ "Hành chính", "Đảng" và thống kê số liệu hiển thị đầy đủ.
- Truy cập `quanlyvanban-hanhchinh.html` & `quanlyvanban-dang.html`: Danh sách văn bản, tệp đính kèm và nội dung báo cáo trước đó hiển thị đầy đủ, nguyên vẹn, không bị mất bất kỳ dữ liệu nào.
