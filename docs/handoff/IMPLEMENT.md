# IMPLEMENT: Khắc phục phân đoạn PPCT đa tuần và hiển thị Thời khoá biểu

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Thay đổi đã thực hiện
- `phancongtochuyenmon.html`
  - Đổi việc theo dõi cụm bài PPCT từ theo Lớp–Môn sang theo Lớp–Môn–Mạch kiến thức. Vì vậy, dòng Đại số nằm giữa các dòng Hình học không còn cắt Bài 11 thành `1/1` và `1/2`.
  - Giữ cơ chế chuẩn hóa tên bài như hậu tố “(tiếp theo)”; Bài 11 dạy 1 tiết tuần 1 và 2 tiết tuần 2 nay có phân đoạn `1/3`, `2/3`, `3/3`.
  - `normalizeTeacherTimetable()` đọc an toàn dữ liệu TKB ở dạng chuỗi JSON trước khi chuẩn hóa. Đây là trường hợp có thể làm TKB đã lưu không được nạp để hiển thị.
  - Giữ các cải tiến TKB đã có: nạp GV khi mở tab, so sánh ID an toàn, khung tiết fallback, và render lại ngay cả khi tự đồng bộ phân công gặp lỗi.
- `tests/baogiang-weekday-segment-smoke.js`
  - Bổ sung tình huống thực tế: Đại số và Hình học xen kẽ giữa tuần 1 và tuần 2; xác nhận Bài 11 hiển thị `1/3`, `2/3`, `3/3`.
- `tests/timetable-render-smoke.js`
  - Bổ sung kiểm tra nạp dữ liệu TKB từ chuỗi JSON, bên cạnh ID chuỗi, khung tiết fallback và render sau lỗi đồng bộ.

## Kiểm tra
- `git diff --check`: đạt, không có lỗi khoảng trắng.
- Không thể chạy các bài kiểm tra Node trong máy hiện tại: Windows chặn `node.exe` đi kèm môi trường với cảnh báo tệp có thể không an toàn. Các bài kiểm tra đã sẵn sàng để chạy lại trong `/verify`.

## Bàn giao
Đề nghị Antigravity IDE chạy `/verify` và cập nhật `docs/handoff/VERIFY.md` với kết quả hai bài kiểm tra cùng kiểm tra giao diện TKB thực tế.
