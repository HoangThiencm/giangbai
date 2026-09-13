# IMPLEMENT

## Đã triển khai
- Sửa bọc `appendixOneTable` / `appendixThreeTable` trên cả 3 file HTML: nếu `findIndex(isNlsColumn/isAiColumn)` trả về `-1` (cột đã gộp thành `Ghi chú`) thì lấy NLS/AI ở vị trí legacy mặc định (PL1: 4/5, PL3: 6/7) rồi gọi `formatNoteIntegration`.
- Thêm `schedulePreviewUpdate()` vào `toggleNlsLesson`, `toggleAiLesson`, `toggleAiLessonRow` để tick chọn Mục 5 làm mới bảng xem trước và thẻ thẩm định.
- Nâng cấp `integrationParts` để tách khối `- Năng lực số:` / `- Năng lực AI:` (kể cả dòng `+`), vẫn giữ nhánh `[NLS:]` / `[AI:]` cũ. `appendixAiCoverage` và xuất Word nhờ đó đếm/phân màu đúng từ cột Ghi chú.
- Đồng bộ 1:1: `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.
- Bổ sung smoke test: ô Ghi chú không còn `'-'` khi đã chọn NLS/AI; toggle gọi `schedulePreviewUpdate`; `appendixAiCoverage` và `calculateComplianceReport` đạt khi đọc mã từ Ghi chú.

## Kiểm thử
- PASS: `node tests/xaydungphuluc-smoke.js`
- PASS: `node tests/canvas-xaydungphuluc-smoke.js`
- PASS: `node tests/xaydungphuluc-math-smoke.js`
- PASS: `node tests/xaydungphuluc-integration-smoke.js`

Không chạy được xác minh trình duyệt (không có browser tools trong phiên này). Hành vi Ghi chú, tick Mục 5 và thẩm định đã được kiểm tra bằng smoke test.

## Không thực hiện
- Không commit hoặc push.
- Không đổi kiến trúc hay thêm chức năng ngoài `docs/handoff/PLAN.md`.
