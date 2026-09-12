# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `phancongtochuyenmon.html`:
  - Hoán đổi vị trí trường nhập liệu trên form Sổ Dạy thay: đưa `Giáo viên nghỉ` (`#new-sub-for-teacher`) lên hàng đầu tiên cạnh `Ngày dạy` và `Loại hình`.
  - Thêm khung xem nhanh TKB `#daythay-absent-schedule-preview` ngay dưới hàng đầu tiên: hiển thị trực quan lịch dạy trong ngày (tiết, lớp, môn) của cả Buổi sáng và Buổi chiều.
  - Tích hợp các nút chọn nhanh buổi dạy (`Chọn buổi Sáng`, `Chọn buổi Chiều`, `Chọn Cả ngày`) ngay trên khung preview.
  - Xây dựng cơ chế tự động nhận diện buổi dạy (`auto-detect session`): tự động chọn Sáng / Chiều / Cả ngày dựa trên lịch thực tế của giáo viên nghỉ và nạp các tiết tương ứng mà không tạo vòng lặp.
  - Quản lý trạng thái ngữ cảnh (`daythaySessionAuto`) giúp giữ nguyên lựa chọn thủ công của người dùng, chỉ tự động nhận diện lại khi thay đổi ngày hoặc giáo viên nghỉ.
  - Tự động ẩn khung preview khi chọn loại hình `Dạy bù`, ngày Chủ nhật hoặc khi chưa chọn giáo viên nghỉ.
  - Giữ nguyên toàn bộ cấu trúc dữ liệu lưu trữ, in ấn thông báo, báo cáo và quyết toán tăng giờ.
- `tests/daythay-suggest-smoke.js`:
  - Bổ sung kiểm thử DOM thứ tự các trường trên form (Giáo viên nghỉ trước Buổi dạy và Giáo viên thực dạy).
  - Kiểm thử render khung preview TKB giáo viên nghỉ hiển thị đúng tiết, lớp, môn của từng buổi.
  - Kiểm thử cơ chế auto-detect buổi dạy cho các trường hợp: chỉ dạy sáng, chỉ dạy chiều, dạy cả hai buổi.
  - Kiểm thử các nút chọn nhanh buổi và tính bền vững của lựa chọn thủ công khi đổi ngữ cảnh.

## Test đã chạy
- `node tests/daythay-suggest-smoke.js`: PASS
- `node tests/baogiang-weekday-segment-smoke.js`: PASS
- `node tests/timetable-render-smoke.js`: PASS
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS
- `node tests/auto-reload-smoke.js`: PASS
- `git diff --check`: PASS (không lỗi cú pháp/khoảng trắng)

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Thứ tự form sắp xếp đúng quy trình nghiệp vụ (chọn Giáo viên nghỉ trước) -> PASS
- Tiêu chí 2: Khung preview hiển thị chính xác TKB trong ngày của giáo viên nghỉ (tiết/lớp/môn cả 2 buổi) -> PASS
- Tiêu chí 3: Tự động nhận diện buổi dạy (Sáng/Chiều/Cả ngày) và nạp đúng tiết của giáo viên nghỉ -> PASS
- Tiêu chí 4: Các nút chọn nhanh hoạt động tức thì, lựa chọn thủ công không bị ghi đè ngoài ý muốn -> PASS
- Tiêu chí 5: Bảng đề xuất thông minh 2 cột cập nhật ngay khi chọn giáo viên nghỉ -> PASS
- Tiêu chí 6: Toàn bộ 5 bộ test smoke của dự án chạy tự động đều PASS 100% -> PASS

## Bug
Không phát hiện bug tồn đọng.

