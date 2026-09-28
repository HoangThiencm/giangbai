# PLAN: Sửa lỗi trang Quản lý văn bản (quanlyvanban.html) không hiển thị nội dung

## Hiện trạng & Nguyên nhân gốc rễ
1. **File `vanban-hub.js` trên hosting bị rỗng (0 bytes)**:
   - Qua kiểm tra trực tiếp trên server production (`https://hoangthiencm.id.vn/vanban-hub.js`), file trả về mã 200 nhưng dung lượng đúng 0 bytes (`Content-Length: 0`).
   - Do đó, trình duyệt tải `quanlyvanban.html` nhưng file script điều khiển chính `vanban-hub.js` không chạy, khiến khu vực thống kê `#summary` và thẻ lĩnh vực `#sectorCards` ("Chọn lĩnh vực") hoàn toàn trống trơn.
2. **Kiểm tra quyền người dùng trong `api/vanban.php` bị chặn đối với Admin**:
   - Trong `api/vanban.php` (dòng 13), hàm `vbd_current_user` đang kiểm tra cứng:
     ```php
     if (!$user || !(bool)$user['is_active'] || ($user['role'] ?? '') !== 'teacher') {
         respond(['error' => 'Chức năng quản lý văn bản chỉ dành cho giáo viên.'], 403);
     }
     ```
   - Khi tài khoản `admin` hoặc `superadmin` truy cập sẽ bị trả về lỗi 403 Forbidden. Trong khi đó ở các module khác (`thoikhoabieu.php`, `phancong.php`), `admin` và `superadmin` đều được phân quyền hợp lệ.
3. **Cơ chế cache và triển khai FTP**:
   - `quanlyvanban.html` đang gọi `vanban-hub.js?v=20260624-drive-banner-fix`. Vì hash/version chưa đổi nên FTP Deploy Action bỏ qua không tải lại file đã bị rỗng trên hosting.

---

## Phạm vi thực hiện
1. **Sửa `api/vanban.php`**:
   - Bổ sung phân quyền cho `admin` và `superadmin` trong `vbd_current_user`.
2. **Cập nhật `quanlyvanban.html` & `vanban-hub.js`**:
   - Tăng version query param trong `quanlyvanban.html` (ví dụ: `vanban-hub.js?v=20260928-fix-hub-render`).
   - Đảm bảo `vanban-hub.js` có xử lý dự phòng: gọi render dữ liệu mặc định (loading skeleton hoặc thẻ lĩnh vực cơ bản) ngay cả trước/trong khi fetch API hoàn tất.
3. **Trigger FTP deploy**:
   - Chạm (touch/thay đổi) `vanban-hub.js` và `quanlyvanban.html` để GitHub Actions FTP Deploy bắt buộc đồng bộ lại file đầy đủ lên hosting.

---

## Ngoài phạm vi
- Không thay đổi cấu trúc database hoặc logic Google Drive upload/delete.
- Không sửa đổi các trang khác ngoài phạm vi module quản lý văn bản.

---

## File dự kiến tác động
- `api/vanban.php`
- `quanlyvanban.html`
- `vanban-hub.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa handoff**:
   - Xóa `docs/handoff/.lock` nếu có.
2. **Bước 2: Cập nhật quyền trong `api/vanban.php`**:
   - Cho phép vai trò `admin`, `superadmin`, `teacher`:
     ```php
     $role = (string)($user['role'] ?? '');
     if (!in_array($role, ['teacher', 'admin', 'superadmin'], true)) {
         respond(['error' => 'Chức năng quản lý văn bản chỉ dành cho giáo viên hoặc quản trị viên.'], 403);
     }
     ```
3. **Bước 3: Tối ưu `vanban-hub.js`**:
   - Thêm gọi `renderSectors();` ngay lúc khởi tạo (trước khi `fetch` dữ liệu hoàn tất) để giao diện 2 thẻ lĩnh vực ("Hành chính", "Đảng") luôn hiển thị ngay lập tức, không để màn hình trống trơn.
   - Thêm version bump trong `quanlyvanban.html`: `vanban-hub.js?v=20260928-fix-hub-render`.
4. **Bước 4: Cập nhật nhật ký**:
   - Ghi nội dung vào `docs/handoff/IMPLEMENT.md`.
   - Tạo file `docs/handoff/.lock` nội dung `LOCK`.

---

## Tiêu chí nghiệm thu
- Truy cập `hoangthiencm.id.vn/quanlyvanban.html`: hiển thị đầy đủ thẻ "Hành chính", "Đảng" cùng 4 thẻ thống kê số lượng văn bản.
- Admin và giáo viên đều tải dữ liệu bình thường, không bị lỗi 403.
