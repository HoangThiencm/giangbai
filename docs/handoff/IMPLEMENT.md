# IMPLEMENT: Khắc phục hiển thị Thời khoá biểu

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Thay đổi đã thực hiện
- `phancongtochuyenmon.html`
  - Khi mở tab Thời khoá biểu, luôn gọi `selectTimetableTeacher()` để nạp TKB của giáo viên trước khi dựng lưới.
  - Chuẩn hoá so sánh ID giáo viên bằng `String(...)` ở các luồng chọn, lưu, chuyển giáo viên, hiển thị workspace và đồng bộ phân công.
  - Bọc bước tự động đồng bộ phân công sau nhận diện AI trong `try...catch`; workspace và danh sách giáo viên luôn được render lại.
  - Bổ sung khung tiết mặc định: sáng 1–5, chiều 1–4, nếu cấu hình không có dữ liệu.
- `tests/timetable-render-smoke.js`
  - Thêm kiểm tra nạp TKB qua ID HTML dạng chuỗi, khung tiết fallback, và việc render vẫn diễn ra khi đồng bộ phân công lỗi.

## Kiểm tra
- `git diff --check`: đạt, không có lỗi khoảng trắng.
- Không thể chạy bài kiểm tra Node trong máy hiện tại: Windows chặn `node.exe` đi kèm môi trường với cảnh báo tệp có thể không an toàn, kể cả khi đã xin quyền chạy. Bài kiểm tra đã sẵn sàng để chạy lại trên môi trường cho phép Node.

## Bàn giao
Đề nghị Antigravity IDE chạy `/verify` và ghi kết quả vào `docs/handoff/VERIFY.md`.
