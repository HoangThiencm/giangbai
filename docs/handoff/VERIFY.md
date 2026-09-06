# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Tách Phụ lục 1 (`APPENDIX_1_COLUMNS`) thành 02 cột độc lập: `Biểu hiện năng lực số` và `Biểu hiện năng lực AI`.
- [x] Hàm `appendixOneTable()` trích xuất riêng `nlsText` và `aiText` qua hàm `separateIntegration()`, điền đầy đủ 6 ô cho mỗi dòng.
- [x] Renderer xem trước `dynamicPpctTable()` nhận diện cột NLS (class `.nls-code`) và cột AI (class `.ai-code`), hiển thị đúng màu.
- [x] `normalizeIntegrationTable()` phân biệt bảng Phụ lục 1 có sẵn 2 cột NLS & AI để không gộp nhầm cột.
- [x] `calculateComplianceReport()` đối chiếu tỷ lệ NLS và AI trên các cột mới chính xác.
- [x] `DOCX_WIDTHS.appendixOne` được cập nhật 6 phần tử `[4, 20, 5, 35, 18, 18]` (tổng 100%).
- [x] Trong `addPpct()`, các ô xuất Word được gán đúng màu (#0070C0 cho NLS, #7030A0 cho AI).
- [x] Khổ giấy ngang DOCX được sửa: `page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE } }`, tạo ra thẻ OpenXML `<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>` chuẩn khổ A4 Landscape (297mm x 210mm).
- [x] Bộ smoke test tự động và tích hợp đã được cập nhật đồng bộ và chạy pass.

## Test đã chạy
1. `node tests/xaydungphuluc-smoke.js`: PASS (exited with code 0).
2. `node tests/xaydungphuluc-integration-smoke.js`: PASS (exited with code 0).
3. Kiểm thử trích xuất OpenXML thực tế trên tệp DOCX xuất ra từ `exportDocx('1', false)`:
   - Thẻ kích thước trang: `<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>` (A4 Landscape chuẩn xác).
   - Đủ 6 cột tiêu đề: `STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Biểu hiện năng lực số`, `Biểu hiện năng lực AI`.

## Pass / Fail từng tiêu chí
- [x] Phụ lục 1 có đủ 02 cột tách biệt: `Biểu hiện năng lực số` và `Biểu hiện năng lực AI`: PASS.
- [x] Nội dung NLS hiển thị ở cột NLS; nội dung AI hiển thị ở cột AI: PASS.
- [x] File Word (.docx) khi xuất ra có hướng giấy ngang chuẩn (Landscape, 297mm x 210mm): PASS.
- [x] Báo cáo thẩm định sư phạm đạt chuẩn: PASS.
- [x] Tất cả các bộ smoke test tự động đều PASS.

## Bug
Không có.
