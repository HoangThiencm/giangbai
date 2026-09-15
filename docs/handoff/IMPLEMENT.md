# IMPLEMENT: Phân Quyền Bảng Padlet Theo Lớp Học & Tối Ưu Hiển Thị

## Phạm vi đã triển khai

### 1. Backend (`api/padlet.php`)
- Cập nhật `action === 'manager'`:
  - Cho phép học sinh truy cập lấy danh sách bảng được chia sẻ.
  - Phân tách dữ liệu: Với học sinh, hệ thống truy vấn `b.status = 'open' AND ((b.access_mode = 'class' AND TRIM(b.target_class) = ?) OR (b.access_mode = 'public'))`. Các bảng thuộc lớp khác bị loại bỏ hoàn toàn.
  - Trả về cờ `is_teacher: false` và `student_class` để frontend hiển thị đúng ngữ cảnh lớp.
- Cập nhật `padlet_access()`:
  - Cho phép `admin` và `teacher` sở hữu bảng truy cập.
  - Chặn học sinh lớp khác kèm thông báo chi tiết: *"Bảng này được chia sẻ riêng cho lớp [Tên lớp]. Tài khoản của bạn không thuộc lớp này."*

### 2. Frontend (`padlet_ht.html`)
- `loadManager()`:
  - Ghi nhận `state.isTeacher` và `state.studentClass`.
- `renderLibrary()`:
  - Bổ sung huy hiệu `Lớp [Tên lớp]` cho các bảng cấu hình `access_mode === 'class'`.
  - Với học sinh: thay thế cụm nút `Sửa`/`Xóa` bằng nút `Vào bảng` (màu teal nổi bật).
  - Thông báo thân thiện khi lớp chưa có bảng: *"Chưa có bảng nào được chia sẻ cho lớp của bạn."*
- `renderManager()`:
  - Với học sinh: hiển thị giao diện tinh gọn *"Bảng chia sẻ của lớp"* kèm lời chào và tên lớp, ẩn hoàn toàn các mẫu tạo bảng của giáo viên.
- `openBoardEditor()`:
  - Đảm bảo `board?.target_class` luôn xuất hiện trong danh sách lựa chọn của `<select id="boardClass">` ngay cả khi danh sách lớp trả về chưa kịp nạp.

## Kiểm tra
- `node tests/padlet-ownership-smoke.js`: PASS.
- `node tests/sodiem-smoke.js`: PASS.
- `node tests/teacher-permissions-smoke.js`: PASS.
- `node tests/security-f12-smoke.js`: PASS.
- `git diff --check`: PASS.
