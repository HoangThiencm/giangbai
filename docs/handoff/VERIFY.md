# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Sửa hàm bọc `appendixOneTable` và `appendixThreeTable` để lấy đúng chỉ số cột NLS/AI mặc định khi bảng đã gộp cột Ghi chú: ĐẠT.
- Bổ sung `schedulePreviewUpdate()` vào `toggleNlsLesson`, `toggleAiLesson`, `toggleAiLessonRow` để tick chọn Mục 5 làm mới bảng xem trước: ĐẠT.
- Cập nhật `integrationParts` phân tách đầy đủ khối `- Năng lực số:` và `- Năng lực AI:` (kể cả dòng sub-item `+`): ĐẠT.
- Đồng bộ 1:1 cả 3 file HTML (`xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`): ĐẠT.
- Bổ sung kiểm thử tự động trong các smoke test: ĐẠT.
- Không sửa file ngoài phạm vi kế hoạch: ĐẠT.

## Test đã chạy
- `tests/xaydungphuluc-smoke.js`: PASS
- `tests/canvas-xaydungphuluc-smoke.js`: PASS
- `tests/xaydungphuluc-math-smoke.js`: PASS
- `tests/xaydungphuluc-integration-smoke.js`: PASS

## Pass / Fail từng tiêu chí
1. Cột Ghi chú Phụ lục 1 và Phụ lục 3 hiển thị đầy đủ biểu hiện NLS và AI, không bị biến thành `'-'`: PASS.
2. Tick chọn / bỏ chọn bài hoặc tiết ở Mục 5 kích hoạt `schedulePreviewUpdate()` để làm mới bảng xem trước: PASS.
3. `integrationParts` bóc tách chính xác NLS và AI từ cột Ghi chú, phân biệt đúng loại: PASS.
4. `appendixAiCoverage` và `calculateComplianceReport` nhận diện đúng số tiết NLS và AI từ cột Ghi chú, đạt `pass === true`: PASS.
5. Cột Ghi chú của PL3 giữ nguyên cấu trúc 7 cột và đồng bộ nội dung từ PL1: PASS.

## Bug
Không phát hiện bug mới.
