# IMPLEMENT: Nhận đủ tiết khi dán ảnh Thời khóa biểu

## Đã làm
- `scanTimetableWithAI` trong `phancongtochuyenmon.html`: bỏ lệnh buộc key tiết chỉ nằm trong khung sáng/chiều đang cấu hình. Prompt yêu cầu lấy mọi tiết có phân công (kể cả 6–10), chia buổi theo nhãn Sáng/Chiều hoặc theo dải liên tục (1–5 sang morning, từ tiết 6 hoặc từ tiết bắt đầu chiều sang afternoon), và giữ đúng số tiết in trên ảnh.
- `alignSessionPeriods`: tiết đã thuộc khung cấu hình được giữ nguyên, kể cả khi giáo viên không dạy đủ mọi tiết trong buổi. Tiết ngoài khung (Tiết 7 khi chiều đang là 1–4, dải 6–9, tiết ngắt 1/3/5) không còn bị nén theo index. Chỉ dịch cả dải khi cùng số tiết và lệch đều lên khung người dùng đã cấu hình muộn hơn (ví dụ AI 6–8, khung chiều 7–9).
- Tab Thời khóa biểu GV: nút `Khung tiết` gọi `openQuickPeriodsConfig()` cạnh nút AI nhận diện, kèm dòng gợi ý sáng 1–5 và chiều 1–4 hoặc 6–9 / 7–9.
- `periodsForTimetableSession` giữ nguyên: tiết thực tế ngoài khung vẫn thêm hàng trên lưới.

## Kiểm thử
- `node tests/timetable-render-smoke.js` → PASS.
- Ca mới: chỉ Tiết 7; Tiết 6 và 7; Tiết 1, 3, 5; dải 6–9 và 7–9 khi khung chiều là 1–4; hàng Tiết 7 được thêm vào lưới chiều; prompt không còn câu cấm key ngoài khung; tab TKB có nút Khung tiết.
- Ca cũ vẫn đúng: AI 6–8 căn sang khung chiều 7–9; tiết đã khớp khung không đổi.

## Chưa kiểm trên trình duyệt
- Dán ảnh TKB thật và bấm AI nhận diện / mở modal Khung tiết trên tab Thời khóa biểu GV để `/verify` kiểm tra.
