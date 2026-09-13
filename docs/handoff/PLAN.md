# PLAN

## Hiện trạng
- Trong `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, và `backupcode viettailieu/canvas_xaydungphuluc.html`:
  - Phụ lục 1 đang được định nghĩa 6 cột: `['STT', 'Bài học', 'Số tiết', 'Yêu cầu cần đạt', 'Biểu hiện năng lực số', 'Biểu hiện năng lực AI']` (`APPENDIX_1_COLUMNS`).
  - Phụ lục 3 đang được định nghĩa 8 cột: `['Bài học', 'Số tiết', 'Tiết CT', 'Tuần', 'Thiết bị dạy học (*)', 'Địa điểm dạy học (**)', 'Biểu hiện năng lực số', 'Biểu hiện năng lực AI']` (`APPENDIX_3_COLUMNS`).
  - Mã NLS và mã AI hiện đang tách thành 2 cột riêng rẽ thông qua `separateIntegration()`, làm bảng biểu bị kéo dài theo chiều ngang trong cả bản xem trước HTML lẫn file Word (.docx) xuất ra.
  - Các hàm chuẩn hóa bảng (`normalizeIntegrationTable`), thẩm định chuẩn hóa (`calculateComplianceReport`, `appendixAiCoverage`), trích xuất tích hợp (`appendixOneIntegrationForLesson`, `syncIntegrationFromAppendixOne`), và xuất Word (`exportDocx`, `DOCX_WIDTHS`) đang gắn chặt với số lượng cột và nhãn cột cũ (`length === 8`, `isNlsColumn`, `isAiColumn`).

## Phạm vi
- **Phụ lục 1**: Gộp 2 cột `Biểu hiện năng lực số` và `Biểu hiện năng lực AI` thành 1 cột duy nhất là `Ghi chú`. Số cột giảm từ 6 cột xuống 5 cột: `STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Ghi chú`.
- **Phụ lục 3**: Gộp 2 cột `Biểu hiện năng lực số` và `Biểu hiện năng lực AI` thành 1 cột duy nhất là `Ghi chú`. Số cột giảm từ 8 cột xuống 7 cột: `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, `Ghi chú`.
- **Quy tắc định dạng nội dung cột Ghi chú**:
  - Đối với Năng lực số:
    + Nếu có đúng 1 mã: ghi trên cùng dòng theo dạng `- Năng lực số: Mã: Mô tả`
    + Nếu có từ 2 mã trở lên:
      ```text
      - Năng lực số:
       + Mã 1: Mô tả
       + Mã 2: Mô tả
      ```
  - Đối với Năng lực AI:
    + Nếu có đúng 1 mã: ghi trên cùng dòng theo dạng `- Năng lực AI: Mã: Mô tả (Áp dụng: tiết ...)`
    + Nếu có từ 2 mã trở lên:
      ```text
      - Năng lực AI:
       + Mã 1: Mô tả (Áp dụng: tiết ...)
       + Mã 2: Mô tả (Áp dụng: tiết ...)
      ```
  - Khi một bài học có cả NLS và AI: gộp cả hai khối vào ô Ghi chú theo đúng định dạng trên, ngăn cách nhau bằng dòng mới.
  - Khi một bài học không có NLS lẫn AI: hiển thị `-`.
- Giữ nguyên 100% logic tạo/sinh dữ liệu (Gemini prompt, nguyên tắc bảo toàn PPCT nguồn, tỷ lệ %, mật độ mã adaptive, danh mục bài học SGK/CTGDPT 2018).
- Cập nhật bảng xem trước HTML (`dynamicPpctTable`, `renderPreview`, chỉnh sửa inline `contenteditable` cho ô Ghi chú).
- Cập nhật cơ chế thẩm định dữ liệu (`calculateComplianceReport`, `appendixAiCoverage`) và cơ chế đồng bộ Phụ lục 1 sang Phụ lục 3 (`appendixOneIntegrationForLesson`, `syncIntegrationFromAppendixOne`) để phân tích chuẩn xác mã NLS và AI từ cột Ghi chú.
- Cập nhật cấu hình xuất Word DOCX (`DOCX_WIDTHS` và logic dựng bảng trong `exportDocx`).
- Đồng bộ nhất quán trên cả 3 file mã nguồn: `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`.
- Cập nhật các test suite tương ứng (`tests/xaydungphuluc-smoke.js`, `tests/canvas-xaydungphuluc-smoke.js`, `tests/xaydungphuluc-math-smoke.js`).

## Ngoài phạm vi
- Không thay đổi bảng Phân phối chương trình nguồn (PPCT 7 cột chuẩn ban đầu).
- Không thay đổi Phụ lục 2 (Kế hoạch tổ chức các hoạt động giáo dục).
- Không thay đổi logic trích xuất PDF SGK hay API lưu trữ draft (`user_phuluc_draft.php`).

## File dự kiến tác động
- `xaydungphuluc.html`
- `canvas_xaydungphuluc.html`
- `backupcode viettailieu/canvas_xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `tests/canvas-xaydungphuluc-smoke.js`
- `tests/xaydungphuluc-math-smoke.js`

## Các bước thực hiện
1. **Xây dựng hàm định dạng ô Ghi chú**:
   - Viết hàm `formatNoteIntegration(nlsText, aiText, lesson)`:
     - Tách từng dòng mã từ `nlsText` và `aiText`.
     - Phân tích `{ code, desc }` cho từng mục. Đảm bảo thay thế định dạng `code - desc` thành `code: desc`.
     - Áp dụng điều kiện độ dài: 1 mã thì ghi thẳng sau nhãn `- Năng lực số: Mã: Mô tả`; >= 2 mã thì xuống dòng với thụt đầu dòng ` + Mã: Mô tả`.
     - Tương tự cho Năng lực AI với tiền tố `- Năng lực AI:`.
     - Ghép khối NLS và khối AI thành chuỗi văn bản hoàn chỉnh cho ô Ghi chú.
2. **Cập nhật định nghĩa cột Phụ lục 1 và Phụ lục 3**:
   - `APPENDIX_1_COLUMNS = [['stt','STT'],['lesson','Bài học'],['periods','Số tiết'],['outcomes','Yêu cầu cần đạt'],['note','Ghi chú']]`
   - `APPENDIX_3_COLUMNS = [['lesson','Bài học'],['periods','Số tiết'],['tietCT','Tiết CT'],['week','Tuần'],['devices','Thiết bị dạy học (*)'],['location','Địa điểm dạy học (**)'],['note','Ghi chú']]`
   - Gán `PLAN_COLUMNS = APPENDIX_3_COLUMNS`.
3. **Cập nhật hàm dựng bảng Phụ lục 1 & 3**:
   - `appendixOneTable`: Sinh 5 cột, gọi `formatNoteIntegration(nlsText, aiText, row.lesson)` để điền vào cột `note`.
   - `appendixThreeTable`: Sinh 7 cột, gọi `formatNoteIntegration(nlsText, aiText, row.lesson)` để điền vào cột `note`.
4. **Cập nhật nhận diện cột tích hợp và chuẩn hóa**:
   - Bổ sung nhận diện nhãn cột `Ghi chú` trong `isIntegrationColumn(label)` và hàm kiểm tra `isNoteColumn(label)`.
   - Điều chỉnh `normalizeIntegrationTable` để xử lý mượt mà bảng 5 cột (PL1) và 7 cột (PL3).
5. **Cập nhật đồng bộ PL1 -> PL3 và kiểm tra thẩm định**:
   - Điều chỉnh `appendixOneIntegrationForLesson` trích xuất thông tin tích hợp từ cột Ghi chú của Phụ lục 1.
   - Cập nhật `appendixAiCoverage` và `calculateComplianceReport` để bóc tách mã NLS (`\b\d+\.\d+\.TC\w+`) và mã AI (`\b\d+\.[A-Z]\d+` kèm phạm vi tiết) từ ô Ghi chú, bảo đảm tỷ lệ thẩm định đạt 100%.
6. **Cập nhật giao diện xem trước HTML và xuất file Word**:
   - Trong `dynamicPpctTable`: Cột `Ghi chú` hiển thị đa dòng đẹp mắt (hỗ trợ xuống dòng, giữ định dạng bullet `+ `), cho phép `contenteditable` chỉnh sửa trực tiếp.
   - Trong `renderPreview` và `exportDocx`: Đổi điều kiện kiểm tra số cột PL3 `planModel.columns.length === 7` (thay vì `=== 8`).
   - Cập nhật độ rộng Word `DOCX_WIDTHS`:
     - `appendixOne`: `[5, 22, 6, 37, 30]` (tổng 100%).
     - `appendixThree`: `[20, 5, 6, 5, 15, 14, 35]` (tổng 100%).
7. **Đồng bộ hóa 1:1 sang Canvas và bản sao lưu**:
   - Đồng bộ toàn bộ các hàm và hằng số đã sửa sang `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.
8. **Cập nhật kiểm thử tự động**:
   - Điều chỉnh các assert về số lượng cột và tên cột trong `tests/xaydungphuluc-smoke.js`, `tests/canvas-xaydungphuluc-smoke.js`, `tests/xaydungphuluc-math-smoke.js`.
   - Chạy toàn bộ test suites bảo đảm 100% PASS.

## Rủi ro
- **Nhận diện mã AI/NLS khi thẩm định**: Chuỗi trong cột Ghi chú có tiền tố `- Năng lực số:` và ` + ` có thể làm lệch regex nhận diện mã hoặc phạm vi tiết `(Áp dụng: tiết ...)`.
  -> Khắc phục: Giữ nguyên chuẩn mã regex `\b\d+\.\d+\.TC\w+` và `\b\d+\.[A-Z]\d+`, bảo toàn nguyên vẹn cụm `(Áp dụng: tiết ...)` trong mô tả AI.
- **Đồng bộ từ Phụ lục 1 sang Phụ lục 3**: Khi người dùng chỉnh sửa trực tiếp ô Ghi chú của Phụ lục 1, Phụ lục 3 cần đồng bộ chính xác.
  -> Khắc phục: Hàm `appendixOneIntegrationForLesson` đọc nguyên văn nội dung ô Ghi chú từ Phụ lục 1 và truyền sang Phụ lục 3.
- **Lệch layout khi xuất Word DOCX**: Nếu tỉ lệ phần trăm cột không tròn 100% có thể gây tràn viền Word.
  -> Khắc phục: Cân đối tỉ lệ phần trăm `DOCX_WIDTHS` chính xác đạt tổng 100%, ưu tiên cột Ghi chú chiếm 30% (PL1) và 35% (PL3).

## Cách kiểm thử
1. Chạy các lệnh kiểm thử tự động:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/canvas-xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-math-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`
2. Kiểm tra dữ liệu trực quan trên sandbox/runtime:
   - Bài có 1 mã NLS: hiển thị `- Năng lực số: [Mã]: [Mô tả]`.
   - Bài có 2+ mã NLS: hiển thị `- Năng lực số:\n + [Mã 1]: [Mô tả 1]\n + [Mã 2]: [Mô tả 2]`.
   - Bài có mã AI: hiển thị tương ứng `- Năng lực AI: ...` hoặc dạng danh sách bullet ` + `.
   - Bảng Phụ lục 1 có đúng 5 cột; Bảng Phụ lục 3 có đúng 7 cột.
   - Báo cáo thẩm định CV 5512 đạt 100%.

## Tiêu chí nghiệm thu
- Phụ lục 1 hiển thị và xuất file Word đúng 5 cột: `STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Ghi chú`.
- Phụ lục 3 hiển thị và xuất file Word đúng 7 cột: `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị dạy học (*)`, `Địa điểm dạy học (**)`, `Ghi chú`.
- Cột `Ghi chú` hiển thị chuẩn xác quy tắc định dạng 1 mã vs từ 2 mã trở lên cho cả NLS và AI.
- Logic sinh dữ liệu AI, tỷ lệ NLS/AI và các tính năng khác được giữ nguyên trọn vẹn.
- Toàn bộ các bài kiểm thử tự động đều PASS.
