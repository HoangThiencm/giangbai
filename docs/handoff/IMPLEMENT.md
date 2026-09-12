# IMPLEMENT: Báo giảng — PPCT đa tuần và cảnh báo TKB

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Thay đổi đã thực hiện

- `phancongtochuyenmon.html`
  - Gom bài PPCT theo tên đã chuẩn hóa qua các tuần liên tiếp, kể cả khi mạch khác xen giữa; Bài 11 ba tuần nhận đúng `1/3`, `2/3`, `3/3`.
  - Chỉ tạo cảnh báo từ tuần đang xem trở đi; tuần cũ không còn xuất hiện trong cảnh báo hoặc ảnh hưởng tới gửi email.
  - Phát hiện nhiều giáo viên cùng có TKB cho một lớp/môn/tuần và liệt kê tên cùng tổng số tiết.
  - Email cá nhân chỉ xét cảnh báo thuộc các lớp/môn của giáo viên đăng nhập. Cảnh báo trở thành hộp xác nhận tiếp tục gửi, không còn chặn cứng.
  - Chuẩn hóa bài dạy trên bảng web, email văn bản, email HTML cá nhân và email tổ: `Tuần [X]  [Tên bài] (tiết ppct: [Y]) [A/B]`. Email HTML dùng chung hàm định dạng này trong cột Bài dạy.
- `tests/baogiang-weekday-segment-smoke.js`
  - Kiểm tra Bài 11 qua tuần 4–6, phát hiện hai giáo viên cùng dạy, loại trừ cảnh báo tuần đã qua, và định dạng bài dạy chuẩn cho email HTML.

## Kiểm tra

- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `git diff --check`: PASS.

## Cần xác minh trong `/verify`

- Hiển thị cảnh báo khi đổi ngày xem và hộp xác nhận gửi email trên trình duyệt.
