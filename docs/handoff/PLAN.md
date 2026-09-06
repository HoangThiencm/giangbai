# PLAN: Tách Riêng 02 Cột Năng Lực Số & AI Ở Phụ Lục 1 Và Định Dạng Khổ Giấy Ngang Khi Xuất Word

## Hiện trạng
1. **Phụ lục 1 đang gộp chung 1 cột NLS & AI**:
   - Trong `xaydungphuluc.html`, bảng Phụ lục 1 (`APPENDIX_1_COLUMNS`) hiện có 5 cột: `STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, và cột gộp `Mã NLS & AI (CV 3456 & QĐ 2422)`.
   - Cả mã Năng lực số (CV 3456) và Trí tuệ nhân tạo (QĐ 2422) đang được nối chung trong cùng một ô dữ liệu của cột này, chưa tách riêng thành 02 cột độc lập theo yêu cầu chuyên môn mới.
2. **Lỗi định dạng hướng giấy ngang khi xuất Word**:
   - Trong hàm `exportDocx(n, save)` (dòng 398), thuộc tính trang đang cấu hình:
     `size: { width: 16838, height: 11906, orientation: PageOrientation.LANDSCAPE }`.
   - Trong thư viện `docx` v8.5.0 (lớp `PageSize`), khi `orientation === PageOrientation.LANDSCAPE`, thư viện tự động hoán đổi (`flip`) chiều rộng và chiều cao: gán thuộc tính XML `w:w` bằng `height` (11906) và `w:h` bằng `width` (16838).
   - Kết quả là file DOCX tạo ra có thẻ `<w:pgSz w:w="11906" w:h="16838" w:orient="landscape"/>`. Vì chiều rộng (11906 twips ~ 210mm) nhỏ hơn chiều cao (16838 twips ~ 297mm), Microsoft Word nhận diện đây là kích thước trang dọc (Portrait) dẫn đến tài liệu khi mở ra không hiển thị đúng hướng giấy ngang.

---

## Phạm vi
1. **Tách 02 cột riêng cho Phụ lục 1 trong `xaydungphuluc.html`**:
   - Định nghĩa lại `APPENDIX_1_COLUMNS` gồm 6 cột:
     1. `STT` (`stt`)
     2. `Bài học` (`lesson`)
     3. `Số tiết` (`periods`)
     4. `Yêu cầu cần đạt` (`outcomes`)
     5. `Biểu hiện năng lực số` (`nls`)
     6. `Biểu hiện năng lực AI` (`ai`)
   - Cập nhật hàm `appendixOneTable()`: phân tách dữ liệu `integration` thành 2 giá trị độc lập: `nlsText` (chứa các biểu hiện NLS theo CV 3456) và `aiText` (chứa các biểu hiện AI theo QĐ 2422 kèm tiết áp dụng, hoặc `-` nếu bài học không chọn AI).
   - Cập nhật hàm hiển thị xem trước `dynamicPpctTable()`: nhận diện độc lập cột `Biểu hiện năng lực số` (áp dụng định dạng `.nls-code`) và `Biểu hiện năng lực AI` (áp dụng định dạng `.ai-code`).
   - Tinh chỉnh `calculateComplianceReport()`: đối chiếu tỷ lệ NLS và AI trên các cột riêng biệt của Phụ lục 1 để báo cáo thẩm định đạt chuẩn 100%.
2. **Sửa định dạng xuất Word hướng giấy ngang (Landscape)**:
   - Trong hàm `exportDocx()`: điều chỉnh tham số `page.size` thành:
     `size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }`
     để sau khi thư viện `docx` áp dụng logic `flip`, kết quả xuất ra OpenXML sẽ đúng chuẩn:
     `<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>` (chiều ngang 297mm, chiều dọc 210mm).
   - Cập nhật `DOCX_WIDTHS.appendixOne` thành mảng 6 tỉ lệ tương ứng cho 6 cột: ví dụ `[4, 20, 5, 35, 18, 18]` (tổng 100%).
   - Cập nhật hàm `addPpct()` trong `exportDocx()`: render ô NLS với màu xanh dương (`0070C0`) và ô AI với màu tím (`7030A0`) khi xuất bảng Phụ lục 1.
3. **Cập nhật bộ kiểm thử tự động**:
   - Cập nhật `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` để kiểm tra 6 cột của Phụ lục 1 và kích thước ngang chuẩn của DOCX.

---

## Ngoài phạm vi
- Giữ nguyên cấu trúc bảng 7 cột của Phụ lục 3 (Kế hoạch giáo dục của giáo viên / PPCT) và bảng Phụ lục 2 (Hoạt động giáo dục).
- Không sửa đổi logic các trang khác (`duyetgiaoan.html`, `duyetde.html`, v.v.).

---

## File dự kiến tác động
- `xaydungphuluc.html`: Cập nhật cấu hình cột, hàm tạo dữ liệu bảng, renderer xem trước HTML và logic xuất DOCX khổ ngang.
- `tests/xaydungphuluc-smoke.js`: Cập nhật assertions về các cột Phụ lục 1 và cấu hình page size landscape.
- `tests/xaydungphuluc-integration-smoke.js`: Cập nhật assertion về page size.
- `docs/handoff/PLAN.md` (kế hoạch này).
- `docs/handoff/.lock` (file khóa).

---

## Các bước thực hiện
1. **Bước 1: Cấu hình danh mục cột Phụ lục 1**:
   - Trong `xaydungphuluc.html`, cập nhật:
     ```javascript
     const APPENDIX_1_COLUMNS = [
       ['stt', 'STT'],
       ['lesson', 'Bài học'],
       ['periods', 'Số tiết'],
       ['outcomes', 'Yêu cầu cần đạt'],
       ['nls', 'Biểu hiện năng lực số'],
       ['ai', 'Biểu hiện năng lực AI']
     ];
     ```
2. **Bước 2: Xây dựng hàm trích xuất tách bạch NLS & AI**:
   - Bổ sung hàm `separateIntegration(value, selectedPeriods, index, c, lesson)`:
     + Trích xuất danh sách NLS (nếu cấu hình NLS bật, lấy từ catalog hoặc fallback; ngược lại trả `-`).
     + Trích xuất danh sách AI (nếu cấu hình AI bật và bài/tiết có chọn AI, gán phạm vi tiết; ngược lại trả `-`).
3. **Bước 3: Cập nhật hàm tạo bảng Phụ lục 1 (`appendixOneTable`)**:
   - Dùng `separateIntegration` để điền 6 ô:
     `{ cells: [String(++stt), row.lesson, row.periods, outcomes, nlsText, aiText], isHeader: false }`.
4. **Bước 4: Cập nhật renderer xem trước (`dynamicPpctTable`) & `normalizeIntegrationTable`**:
   - Kiểm tra nếu bảng là Phụ lục 1 (có cột `Biểu hiện năng lực số` và `Biểu hiện năng lực AI`) thì giữ nguyên 6 cột không chèn thêm `INTEGRATION_COLUMN_LABEL`.
   - Tô màu `.nls-code` cho cột NLS và `.ai-code` cho cột AI.
5. **Bước 5: Cập nhật hàm `calculateComplianceReport`**:
   - Tính toán số bài có NLS và số bài/tiết có AI dựa trên cột tương ứng khi bảng có 2 cột riêng biệt.
6. **Bước 6: Cập nhật xuất DOCX cho Phụ lục 1**:
   - Cấu hình lại `DOCX_WIDTHS.appendixOne = [4, 20, 5, 35, 18, 18]`.
   - Trong `addPpct()`, phân biệt cột NLS và cột AI để gán màu TextRun tương ứng (`0070C0` cho NLS, `7030A0` cho AI).
7. **Bước 7: Sửa hướng giấy ngang trong DOCX**:
   - Đổi tham số tạo section trong `exportDocx`:
     ```javascript
     page: {
       size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE },
       margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 }
     }
     ```
     Đảm bảo file sinh ra có `<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>`.
8. **Bước 8: Cập nhật test và kiểm thử**:
   - Cập nhật `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js`.
   - Chạy kiểm tra tự động `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`.

---

## Rủi ro
- **Rủi ro xung đột bộ chuyển đổi bảng**: Hàm `normalizeIntegrationTable` đang được gọi tại nhiều nơi. Cần phân biệt rõ bảng Phụ lục 1 (đã có 2 cột riêng) và bảng Phụ lục 3 / PPCT nguồn (bảng 7-8 cột với 1 cột tích hợp chung) để tránh bị gộp cột ngoài ý muốn.
- **Tương thích kiểm thử cũ**: Hai file smoke test đang assert chuỗi `'width:16838,height:11906'`. Coder cần đồng bộ kiểm thử sang kích thước đúng để test pass.

---

## Cách kiểm thử
1. **Kiểm thử tự động bằng Node**:
   - Chạy `node tests/xaydungphuluc-smoke.js` -> Phải báo PASS.
   - Chạy `node tests/xaydungphuluc-integration-smoke.js` -> Phải báo PASS.
2. **Kiểm thử tạo file DOCX bằng script**:
   - Chạy script Node mô phỏng `exportDocx('1')`, kiểm tra file DOCX tạo ra:
     + Chứa `<w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>`.
     + Bảng có đúng 6 cột tiêu đề: `STT`, `Bài học`, `Số tiết`, `Yêu cầu cần đạt`, `Biểu hiện năng lực số`, `Biểu hiện năng lực AI`.
3. **Kiểm thử trực quan trên trình duyệt**:
   - Mở `xaydungphuluc.html`, xem tab "Phụ lục 1": bảng hiển thị 2 cột riêng biệt NLS và AI to rõ, có màu phân biệt.
   - Bấm nút "Xuất phụ lục đang xem (.docx)", mở file tải về trên Microsoft Word: trang hiển thị đúng chiều giấy ngang (Landscape) chuẩn A4.

---

## Tiêu chí nghiệm thu
- Phụ lục 1 có đủ 02 cột tách biệt: `Biểu hiện năng lực số` và `Biểu hiện năng lực AI`.
- Nội dung NLS hiển thị ở cột NLS; nội dung AI hiển thị ở cột AI (có chú thích tiết áp dụng); bài không có AI hiển thị `-`.
- File Word (.docx) của tất cả các Phụ lục khi mở trong Microsoft Word hiển thị đúng định dạng hướng giấy ngang (Landscape), khổ A4 (297mm x 210mm).
- Báo cáo thẩm định sư phạm (Compliance report) vẫn đạt 100%.
- Tất cả các bộ smoke test tự động đều PASS.
