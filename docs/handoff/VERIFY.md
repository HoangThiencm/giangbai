# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Khắc phục lỗi Header Fetch Unicode**: `requestCanvasDraft` mã hóa `encodeURIComponent(account)` cho header `X-User-Account`, `api/user_phuluc_draft.php` giải mã an toàn qua `rawurldecode()`.
- **Tuyệt đối tuân thủ số tiết NLS (28 tiết)**:
  - `isLessonNlsSelected` loại bỏ hoàn toàn `lessonsMatch` tra cứu lỏng lẻo theo số thứ tự bài học, ưu tiên tra cứu ID chính xác và chuỗi tên tuyệt đối, triệt tiêu lỗi trùng bài và kích hoạt kép giữa các học kỳ.
  - `ppctRow` ngăn chặn chỉ số dòng đè lên dữ liệu cột tích hợp.
  - `getConfig().nls` lưu trữ `count` trực tiếp từ `#nlsCountInput`.
  - `calculateComplianceReport` kiểm tra trực tiếp số tiết mục tiêu đã chọn, không bị làm tròn qua lại với %.
- **Phụ lục 3 bảo toàn Tiết CT, Tuần và Tiêu đề chương**:
  - `normalizeAppendix` ưu tiên tuyệt đối bảng nguồn PPCT (`sourcePpctRows`) hoặc PPCT chuẩn (`defaultPpctRows`), không dùng lịch đã bị AI rút gọn của Phụ lục 1.
  - Giữ nguyên toàn bộ dòng tiêu đề (`isHeader: true`), Tiết CT, Tuần, thiết bị và địa điểm; cột Ghi chú tự động ánh xạ mã tích hợp từ Phụ lục 1.
  - Xuất Word Phụ lục 3 có đầy đủ cấu trúc 7 cột chuẩn CV 5512.
- **Đồng bộ file**: Đã đồng bộ sang `canvas_xaydungphuluc.html`, `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.

## Test đã chạy
- `node tests/canvas-xaydungphuluc-smoke.js` — PASS (toàn bộ kiểm thử giao diện, NLS period-unit và export).
- `node tests/xaydungphuluc-smoke.js` — PASS (toàn bộ kiểm thử bảng PPCT 7 cột, đồng bộ PL1-PL3, Knapsack).
- Sandbox unit test xác thực `isLessonNlsSelected` loại trừ trùng tên bài giữa các học kỳ (Bài 1 HK1 vs Bài 1 HK2) — PASS.

## Pass / Fail từng tiêu chí
1. **Lỗi Fetch Header `String contains non ISO-8859-1 code point`**: PASS — Header được mã hóa an toàn, không còn crash khi tài khoản có dấu tiếng Việt.
2. **Chọn đúng số tiết NLS đã chỉ định (28 tiết)**: PASS — Knapsack chọn chính xác 28 tiết, không còn bị kích hoạt kép thành 30 tiết.
3. **Phụ lục 3 xuất ra đủ Tiết CT, Tuần, Tiêu đề chương**: PASS — Ưu tiên bảng nguồn PPCT, bảo toàn 100% Tiết CT, Tuần và tiêu đề phân cấp.

## Bug
Không có.



