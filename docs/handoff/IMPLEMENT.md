# IMPLEMENT: Nhận diện TKB chính xác hơn

## Đã làm

- `compressTimetableImage()` giữ nguyên PNG/JPEG khi ảnh ≤ 2MB và mỗi cạnh ≤ 2048px. Ảnh lớn hơn được xuất PNG hoặc JPEG chất lượng 0.95, không còn JPEG 0.85.
- `scanTimetableWithAI()` đưa tên giáo viên đang chọn, `state.classes` và `state.subjects` vào prompt. Prompt yêu cầu quét hàng ngang, giữ ô trống (Thứ 2 tiết 1 trống, Thứ 6 tiết 4 trống) và đổi mã 2 chữ số theo danh sách lớp. Đã bỏ câu gán cứng “Nếu Thứ 3 có môn ở Hàng 3 và Hàng 4…”. Giữ câu “tuyệt đối không bỏ sót bất kỳ tiết nào có phân công dạy”.
- `matchClassFromTimetable()` khớp `93` ↔ `9/3`, `64` ↔ `6/4`, `63` ↔ `6A3`, và giữ `71` khi danh sách lớp đã dùng mã 2 số. `normalizeClassNameFromTimetable()` không xóa dấu `/`.
- `applyAiTimetableResult()` và `extractAssignmentsFromTimetable()` dùng tên lớp đã khớp, nên không tạo lớp rác khi đã có lớp tương đương.
- `alignSessionPeriods()` giữ nguyên tiết 1–5 khi khung buổi bắt đầu bằng tiết 1.
- Sau khi AI đọc xong, badge `#tt-ai-scan-badge` hiện số tiết sáng, số tiết chiều và danh sách lớp.

## Kiểm tra

- `node tests/timetable-render-smoke.js` → PASS (gồm `new vm.Script` cho mọi khối script trong `phancongtochuyenmon.html`).

## Ngoài phạm vi

Không sửa file ngoài `phancongtochuyenmon.html`, `tests/timetable-render-smoke.js` và handoff. Chưa commit, chưa push.
