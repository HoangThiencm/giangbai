# IMPLEMENT

## Sửa theo VERIFY (FAIL)

- Không tạo snapshot tuần trước khi sửa tuần quá khứ; bảo vệ tuần hiện hành.
- Suy mốc năm học khi thiếu cấu hình hoặc mốc Đợt cũ lệch năm; hiển thị mốc đang dùng và cập nhật năm của Đợt mẫu.
- Khi nhập khoảng tuần trong tạo Đợt nhanh, tự điền khoảng ngày tương ứng; người dùng vẫn có thể sửa ngày sau đó.
- Đã chạy lại hai smoke test và `git diff --check`: PASS. Cần `/verify` lại các luồng tích hợp.

## Đã triển khai

- Bổ sung mốc năm học dùng chung, tra TKB theo tuần/ngày và theo Đợt; hỗ trợ Đợt chỉ có tuần áp dụng hoặc không có ngày kết thúc.
- Hoàn thiện chọn/lưu TKB riêng từng tuần, bao gồm bảo toàn TKB tuần trước và bảo vệ TKB hiện hành khi quay lại sửa tuần quá khứ.
- Giới hạn cập nhật `persistTeacherTimetable` vào Đợt hiện tại, không còn ghi đè mọi snapshot Đợt cũ.
- Kết nối TKB hiệu lực theo ngày vào Sổ Dạy Thay - Bù, Lịch báo giảng và email TKB.
- Bổ sung smoke test cho hồi quy TKB Tuần 11/Tuần 12 và bảo toàn snapshot Đợt.

## Tệp đã thay đổi

- `phancongtochuyenmon.html`
- `tests/daythay-suggest-smoke.js`
- `tests/timetable-render-smoke.js`

## Kiểm thử

- `node tests/daythay-suggest-smoke.js` — PASS
- `node tests/timetable-render-smoke.js` — PASS
- Trích xuất và `node --check` toàn bộ 7 khối script trong `phancongtochuyenmon.html` — PASS
- `git diff --check` — PASS

## Vấn đề còn lại

Không có vấn đề đã biết trong phạm vi kế hoạch.
