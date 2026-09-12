# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`:
  - Mục 1: Thu gọn chỉ còn thông tin trường học & giáo viên (`1. Thông tin trường học &amp; giáo viên`), loại bỏ khối NLS/AI và checkbox khỏi Mục 1.
  - Mục 3 mới: Tạo card cấu hình Năng lực số & Trí tuệ nhân tạo (`3. Cấu hình Năng lực số &amp; Trí tuệ nhân tạo`), đặt sau Mục 2 (Tài liệu & dữ liệu nguồn) và trước Mục "Chọn loại phụ lục".
  - Đánh số lại các mục tiếp theo: Mục 4 (Chọn loại phụ lục), Mục 5 (AI đề xuất bài/tiết tích hợp NLS & AI...), Mục 6 (Ý tưởng / chỉ đạo riêng), Mục 7 (Tiến trình xử lý), Mục 8 (Xem trước & xuất Word).
  - Phụ lục 3 phòng chống rỗng dữ liệu:
    - `appendixThreeTable()`: Tự động fallback về `results['1'].schedule` -> `sourcePpctRows` -> `defaultPpctRows(c)` khi `planRows` rỗng.
    - `syncIntegrationFromAppendixOne()`: Tự động fallback tương tự khi `targetPlanRows` rỗng.
    - `normalizeAppendix()` cho `no === '3'`: Hỗ trợ đa dạng cấu trúc trả về từ AI (`plan`, `schedule`, `ppct`, `items`, `rows`) và fallback tự động nếu không có dòng nào.
    - `renderPreview()`: Khi mở Phụ lục 3, tự động tái dựng `planModel` 8 cột có dữ liệu nếu bảng rỗng.
    - `exportDocx(3)`: Tự động kiểm tra và đảm bảo bảng 8 cột luôn có dữ liệu trước khi đóng gói file Word.
- `tests/xaydungphuluc-smoke.js`:
  - Thêm test case khẳng định `appendixThreeTable([])` luôn có dòng dữ liệu dự phòng và đủ 8 cột.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js`: PASS
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS
- `node tests/xaydungphuluc-math-smoke.js`: PASS
- `node tests/sgk-knowledge-smoke.js`: PASS

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Di chuyển khối Cấu hình NLS & AI xuống sau Mục 2 và trước Mục 3 (thành Mục 3 mới) -> PASS
- Tiêu chí 2: Đánh số lại các mục từ 1 đến 8 đồng bộ trên 3 tệp HTML -> PASS
- Tiêu chí 3: Phụ lục 3 mở xem trước không bị rỗng bảng (tự động khôi phục dữ liệu bài học) -> PASS
- Tiêu chí 4: Xuất Word Phụ lục 3 có đầy đủ các dòng bài học trong bảng 8 cột, không bị 0 dòng -> PASS
- Tiêu chí 5: Fallback an toàn khi AI không trả về trường `plan` hoặc trả về mảng rỗng -> PASS
- Tiêu chí 6: Bộ test tự động smoke tests và math tests đều đạt 100% -> PASS

## Bug
Không có bug tồn đọng.




