# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Sửa `compressTimetableImage()`: Giữ nguyên chất lượng ảnh khi kích thước ≤ 2MB, không còn nén JPEG 0.85 gây mờ số.
- Cập nhật `scanTimetableWithAI()`: Prompt đưa tên giáo viên, danh sách lớp (`state.classes`) và danh sách môn (`state.subjects`); hướng dẫn quét 2D theo hàng ngang, bảo toàn ô trống (Thứ 2 tiết 1 trống, Thứ 6 tiết 4 trống); bỏ câu hardcode gán cứng Thứ 3; giữ câu kiểm tra phân công.
- Bổ sung `matchClassFromTimetable()`: Khớp mã lớp 2 chữ số (`93` ↔ `9/3`, `64` ↔ `6/4`, `63` ↔ `6A3`, `71` ↔ `71`); không xóa dấu `/` trong `normalizeClassNameFromTimetable()`.
- Cập nhật `applyAiTimetableResult()` và `extractAssignmentsFromTimetable()` để dùng tên lớp đã chuẩn hóa qua `matchClassFromTimetable()`.
- Tinh chỉnh `alignSessionPeriods()` giữ nguyên tiết 1–5 cho buổi sáng.
- Bổ sung badge hiển thị kết quả AI `#tt-ai-scan-badge`.
- Không đụng file ngoài phạm vi. Không xóa `.lock`.

## Test đã chạy
- `node tests/timetable-render-smoke.js`
- `node tests/daythay-suggest-smoke.js`
- `node tests/baogiang-weekday-segment-smoke.js`

## Pass / Fail từng tiêu chí
- Pass: Giữ nguyên độ sắc nét ảnh TKB khi gửi vào AI.
- Pass: Prompt quét hàng ngang ma trận 2D bảo toàn ô trống (không dồn môn từ tiết 2 lên tiết 1, tiết 5 lên tiết 4).
- Pass: Khớp lớp 2 số thông minh (`93` -> `9/3`, `64` -> `6/4`, `63` -> `6A3`).
- Pass: Không sinh thêm lớp rác trong `state.classes`.
- Pass: Mọi bài kiểm thử trong `timetable-render-smoke.js` đạt kết quả PASS mà không có regression.

## Bug
Không phát hiện bug.
