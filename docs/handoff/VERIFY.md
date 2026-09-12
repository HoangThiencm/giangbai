# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Thu gọn khung nhìn tab Thời khoá biểu giáo viên: Đạt.
  - Cụm tải ảnh, năm học, học kỳ và nút AI được đưa vào `<details id="tt-import-details">`, mặc định đóng lại, tự động mở khi dán hoặc kéo thả ảnh.
  - Hai bảng Buổi sáng và Buổi chiều được bố trí song song 2 cột trên màn hình >= 1024px bằng `.tt-sessions-container` và co về 1 cột trên màn hình nhỏ.
  - Tối giản phần đệm, cột tiết và ô bài dạy (`.tt-cell`, `.tt-grid`), chiều cao toàn màn hình vừa khít, không cần trượt con lăn chuột.
- Căn chỉnh số tiết AI nhận diện lệch buổi chiều (6–8 về 7–9): Đạt.
  - `scanTimetableWithAI()` truyền cấu hình tiết sáng/chiều thực tế của trường vào prompt Gemini và quy định chặt chẽ thứ tự ánh xạ hàng khi ảnh không có cột số tiết.
  - `alignSessionPeriods()` trong `applyAiTimetableResult()` tự động căn chỉnh tập tiết do AI trả về (ví dụ `6, 7, 8` hoặc `1, 2, 3`) tương ứng vào khung tiết cấu hình của buổi (`[7, 8, 9]`), không làm phát sinh tiết 6. Kết quả đã khớp hoặc dữ liệu vượt khung được giữ nguyên.

## Test đã chạy
- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS (kiểm tra layout 2 cột, `<details>`, breakpoint responsive và căn chỉnh tiết AI 6–8 sang 7–9).
- `node tests/auto-reload-smoke.js`: PASS.
- `git diff --check`: PASS.

## Pass / Fail từng tiêu chí
1. Cả Buổi sáng và Buổi chiều hiển thị song song 2 cột trên cùng một màn hình chuẩn máy tính, không cần trượt con lăn chuột: PASS.
2. Khối nhập liệu / upload TKB thu gọn dưới dạng `<details>`, tự mở khi dán hoặc chọn ảnh: PASS.
3. Khi cấu hình chiều `7-9`, nhận diện ảnh TKB (kể cả ảnh không có cột số tiết) tự động đưa vào đúng Tiết 7, 8, 9, không bị gán vào Tiết 6: PASS.
4. Toàn bộ các bộ test tự động đạt 100%: PASS.

## Bug
Không có.
