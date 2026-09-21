# IMPLEMENT: Nạp danh sách học sinh CSDL cho Game Đua Vịt

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### `trochoi.compiled.js`
- Thêm chế độ **Từ lớp dạy (CSDL)** cạnh Nhập tay và Import Excel.
- Nạp lớp qua `api/exam.php?route=student-classes` và nạp học sinh qua `api/exam.php?route=class-students&class_name=...`, đều kèm `credentials: 'include'`.
- Chuyển roster thành danh sách vịt, đồng bộ tên vào ô Nhập tay và hiển thị trạng thái nạp.
- Có nút tải lại lớp, trạng thái đang tải và thông báo khi lớp trống/lỗi.

## Kiểm tra
- Kiểm tra cú pháp JavaScript bằng Node (`node --check trochoi.compiled.js`) — PASS.
- Chưa kiểm tra luồng gọi API trực tiếp trong trình duyệt; cần `/verify` theo PLAN §4.
