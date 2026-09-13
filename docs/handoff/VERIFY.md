# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `api/baogiang_mail.php`: Đã hỗ trợ payload `deliveries`, `recipients`, `recipient`, tôn trọng cờ `BAOGIANG_GMAIL_TO_SELF_ONLY`, lọc email hợp lệ, giới hạn 50 email/lần, giãn cách 150ms chống spam/chặn SMTP.
- `api/config.sample.php`: Đã cập nhật cờ `BAOGIANG_GMAIL_TO_SELF_ONLY = false` kèm ghi chú hướng dẫn chi tiết.
- `phancongtochuyenmon.html`:
  - Thẻ Thời khóa biểu: Bổ sung xem/sửa nhanh email giáo viên; thêm hàm `buildTeacherIndividualTimetableEmail` và các nút gửi riêng TKB cho từng GV đã chọn cũng như gửi bản tổng hợp cá nhân.
  - Thẻ Lịch báo giảng: Bổ sung nút "Gửi lịch tuần cho các GV đã chọn" (`sendBaoGiangSelectedWeekToTeachers`), lọc đúng tiết của từng GV trong tuần, tạo email cá nhân hóa và gửi qua `deliveries`.
- `tests/timetable-render-smoke.js`: Đã cập nhật test case kiểm thử email TKB cá nhân và các thành phần giao diện mới.

## Test đã chạy
- `node tests/timetable-render-smoke.js`: PASS
- `node tests/baogiang-weekday-segment-smoke.js`: PASS
- `node tests/daythay-suggest-smoke.js`: PASS
- `node tests/baogiang-recognition-smoke.js`: PASS
- Rà soát mã nguồn PHP `api/baogiang_mail.php` và `api/config.sample.php`: Cú pháp chuẩn xác, bảo mật và an toàn.

## Pass / Fail từng tiêu chí
- [PASS] Hỗ trợ gửi TKB riêng lẻ cho từng giáo viên đã chọn.
- [PASS] Hỗ trợ gửi Lịch báo giảng tuần riêng cho từng giáo viên đã chọn.
- [PASS] Kiểm tra hợp lệ email và thông báo khi thiếu email giáo viên.
- [PASS] Bảo vệ chế độ thử nghiệm qua cờ `BAOGIANG_GMAIL_TO_SELF_ONLY`.
- [PASS] Giữ tương thích hoàn toàn với luồng gửi email cá nhân cũ.

## Bug
- Lỗi: Không có.
- Tái hiện: Không có.
- File liên quan: Không có.





