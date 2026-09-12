# IMPLEMENT: Thu gọn Thời khóa biểu & căn chỉnh tiết AI

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `phancongtochuyenmon.html`
  - Khối nhập ảnh TKB, năm học, học kỳ và nút AI được đưa vào `<details id="tt-import-details">`, mặc định thu gọn.
  - Khối nhập tự mở khi dán ảnh, kéo thả ảnh hoặc khi ảnh xem trước được thiết lập.
  - Hai lưới Buổi sáng/Buổi chiều nằm trong `.tt-sessions-container`: hai cột trên màn hình rộng và một cột khi màn hình nhỏ.
  - Tối giản phần đệm, cột tiết và ô môn học để toàn bộ tab TKB gọn hơn.
  - `scanTimetableWithAI()` truyền khung tiết sáng/chiều thực tế vào prompt Gemini và yêu cầu nghiêm ngặt map các hàng theo khung này nếu ảnh không có cột số tiết.
  - `applyAiTimetableResult()` dùng `alignSessionPeriods()`: khi tập tiết do AI trả về khác cấu hình (ví dụ `6, 7, 8` so với `7, 8, 9`), dữ liệu được căn theo thứ tự vào khung tiết. Kết quả đã trùng khung được giữ nguyên; dữ liệu vượt khung cũng được giữ nguyên để không mất bài dạy.
- `tests/timetable-render-smoke.js`
  - Kiểm tra cấu trúc `<details>`, lưới sáng/chiều hai cột và breakpoint một cột.
  - Gọi `applyAiTimetableResult()` thực tế để xác nhận cấu hình chiều `7–9` căn dữ liệu AI `6–8` thành `7–9`, không sinh tiết 6.

## Kiểm tra đã chạy

- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `node tests/auto-reload-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần chạy `/verify` để xác nhận trực quan khung nhìn TKB và nhận diện ảnh thật.
