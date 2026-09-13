# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Khắc phục lỗi Fetch Header**: Đã bọc `encodeURIComponent(account)` vào `X-User-Account`, `api/user_phuluc_draft.php` giải mã `rawurldecode()`, và chặn dùng họ tên giáo viên có dấu làm username trong `prefillCanvasDraftAccount`.
- **Tối ưu hóa thuật toán chọn tiết NLS**: Đã chuyển sang bài toán Knapsack 0/1 tối ưu điểm sư phạm (`nlsLessonPriorityScore`), ràng buộc dung lượng chính xác đúng số tiết yêu cầu (ví dụ 28 tiết); đồng bộ sự kiện `input` tức thì trên `#nlsCountInput`.
- **Chuẩn hóa Phụ lục 3 kế thừa 100% từ Phụ lục 1 / Nguồn PPCT**: Đã loại bỏ hoàn toàn việc gọi AI tái tạo bảng PPCT ở Phụ lục 3; kế thừa nguyên vẹn dòng tiêu đề phân cấp (`HỌC KÌ I`, `CHƯƠNG I...`), Tiết CT, Tuần, thiết bị, địa điểm và cột Ghi chú tích hợp NLS/AI từ Phụ lục 1; xuất Word merge full 7 cột cho dòng tiêu đề.
- **Đồng bộ file**: Đã đồng bộ đầy đủ trên `canvas_xaydungphuluc.html`, `xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html` và `api/user_phuluc_draft.php`.

## Test đã chạy
- `node tests/canvas-xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-smoke.js` — PASS.
- Kiểm thử tĩnh và logic trên các file triển khai — PASS.

## Pass / Fail từng tiêu chí
1. **Lỗi Fetch Header `String contains non ISO-8859-1 code point`**: PASS — Header được mã hóa an toàn, không còn crash khi tài khoản có dấu tiếng Việt.
2. **Chọn đúng số tiết NLS đã chỉ định**: PASS — Nhập 28 tiết được thuật toán Knapsack chọn các bài có điểm sư phạm cao nhất đạt chính xác 28 tiết.
3. **Phụ lục 3 đủ Tiết CT, Tuần, Tiêu đề Học kỳ / Chương và cột Ghi chú**: PASS — Kế thừa 100% từ Phụ lục 1 / PPCT nguồn, xuất Word chuẩn CV 5512.

## Bug
Không có.
