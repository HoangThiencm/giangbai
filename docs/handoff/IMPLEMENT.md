# IMPLEMENT: Sửa hiển thị NLS/AI và Phụ lục 3

## Đã thực hiện

- Giữ lại dòng tiêu đề `- Năng lực số:` và `- Năng lực AI:` khi ghi chú có nhiều mã.
- Cho phép đối chiếu NLS theo tên bài khi mã bài dùng tiền tố khác nhau.
- Phụ lục 3 luôn dựng lại từ toàn bộ tiến trình chuẩn (ưu tiên Phụ lục 1), chỉ dùng phản hồi AI để bổ sung thiết bị, địa điểm và tích hợp cho bài khớp.
- Đồng bộ trực tiếp cột `Ghi chú` của Phụ lục 1 sang Phụ lục 3; chỉ tự tạo ghi chú từ `integration` khi chưa có dữ liệu Phụ lục 1.
- Dùng số cột thực tế của `APPENDIX_3_COLUMNS` khi xem trước và xuất Word.
- Đồng bộ logic sang cả hai bản Canvas và mở rộng smoke test cho tiêu đề nhiều mã, lịch đầy đủ và mô hình 7 cột.

## Kiểm chứng

- `git diff --check`: đạt.
- Đã kiểm tra tĩnh sự có mặt của toàn bộ thay đổi trên cả ba bản HTML.
- Không chạy được bốn smoke test Node vì Windows chặn runtime `node.exe` của môi trường với thông báo tệp có khả năng không an toàn (`ResourceUnavailable`). Cần gỡ chặn hoặc cài Node hợp lệ rồi chạy lại đầy đủ các lệnh trong `PLAN.md`.
