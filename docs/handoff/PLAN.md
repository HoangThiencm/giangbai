# PLAN: Sửa lỗi lặp dòng Năng lực số & Sửa lỗi hiển thị ký tự thô `***` trong file Word (.docx)

## Hiện trạng & Nguyên nhân gốc rễ (Root Cause)

1. **Lỗi lặp lại dòng Năng lực số (`c) Năng lực số` xuất hiện 2 lần)**:
   - Trong `js/khbd-app.js`, hàm `stripObjectivesStandardSection` và `upsertObjectivesStandardSection` dùng biểu thức chính quy:
     `matchRe = /^#{1,6}\s*(?:[a-z]\)\s*)?năng lực số\b/i`
   - **Bản chất lỗi**: Trong JavaScript RegExp, ký tự `\b` (ranh giới từ) chỉ nhận diện ký tự ASCII `\w` (`[a-zA-Z0-9_]`). Ký tự tiếng Việt có dấu `ố` trong từ `số` không thuộc `\w`. Khi đi kèm dấu hai chấm `:` hoặc khoảng trắng, `số\b` **không thể khớp được** (`test()` trả về `false`).
   - **Hậu quả**: Hàm `stripObjectivesStandardSection` không xóa được phần NLS cũ, và `upsertObjectivesStandardSection` cũng tưởng chưa có NLS nên đã chèn thêm một lần nữa, khiến `c) Năng lực số:` bị nhân bản thành 2 dòng liên tiếp.

2. **Lỗi chưa render ký tự markdown `***` (hiện ký tự thô `***[5.3.TC2a]:***` trong file Word)**:
   - Trong `js/khbd-docx.js`, tại hàm `markdownToDocxParagraphs` (dòng 738–749):
     ```javascript
     if (trimmed.startsWith("### ")) {
       const headingText = trimmed.substring(4).trim();
       runColor = this.headingIntegrationColor(headingText);
       elements.push(new Paragraph({
         ...
         children: [
           this.coloredTextRun(headingText, { size: this.fontSizeH3, bold: true, italics: Boolean(runColor), color: runColor })
         ]
       }));
     ```
   - **Bản chất lỗi**: Khi gặp tiêu đề `### `, code gán thẳng `headingText` thô vào `this.coloredTextRun(headingText)` mà **không chạy qua bộ phân tích markdown `this.parseInlineTextToRuns`**.
   - **Hậu quả**: Toàn bộ chuỗi thô gồm các dấu sao `***[5.3.TC2a]:***` bị đưa nguyên vẹn vào file Word, không được chuyển đổi thành chữ in đậm + in nghiêng. Tương tự đối với `d) Năng lực AI: ***[9.B2.1]:***`.

---

## Phạm vi thực hiện

### 1. Sửa biểu thức chính quy tiếng Việt trong `js/khbd-app.js`
- **File**: `js/khbd-app.js`.
- **Giải pháp**:
  - Thay thế `số\b` bằng `số(?::|\s|$)` hoặc `số\b` không phụ thuộc ASCII boundary:
    `matchRe = /^#{1,6}\s*(?:[a-z]\)\s*)?năng lực số(?::|\s|$)/i`
    và
    `matchRe = /^#{1,6}\s*(?:[a-z]\)\s*)?năng lực\s*AI(?::|\s|$)/i`
  - Đảm bảo `stripObjectivesStandardSection` và `upsertObjectivesStandardSection` nhận diện chính xác 100% dòng tiêu đề NLS và AI, xóa sạch bản cũ trước khi chèn bản mới duy nhất.

### 2. Sửa `markdownToDocxParagraphs` trong `js/khbd-docx.js` để parse inline markdown cho tiêu đề
- **File**: `js/khbd-docx.js`.
- **Giải pháp**:
  - Tại các khối xử lý tiêu đề `## `, `### `, `#### `:
    - Không dùng `this.coloredTextRun(headingText)`.
    - Thay bằng `this.parseInlineTextToRuns(headingText, runColor, { size: this.fontSizeH3, bold: true, italics: Boolean(runColor) })`.
  - Bộ phân tích `parseInlineTextToRuns` sẽ tự động bóc tách các dấu sao `***`, loại bỏ ký tự markdown thô và tạo các `TextRun` có định dạng `bold: true, italics: true, color: "0369A1"` (NLS) hoặc `"6D28D9"` (AI).

### 3. Đồng bộ vào `canvas_soankhbd.html` & Viết test kiểm thử
- **File**: `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`, `soankhbd.html`.
- **Test**: `tests/docx-export-format-smoke.js` và `tests/khbd-4steps-workflow-smoke.js`:
  - Thêm kiểm thử: Tiêu đề `### c) Năng lực số: ***[5.3.TC2a]:*** ...` khi xuất ra Word không còn chứa ký tự thô `***`.
  - Thêm kiểm thử: Mục tiêu chỉ có duy nhất 1 dòng Năng lực số, không bị lặp đúp.

---

## File dự kiến tác động
- `js/khbd-app.js`
- `js/khbd-docx.js`
- `canvas_soankhbd.html`
- `soankhbd.html`
- `backupcode viettailieu/canvas_soankhbd.html`
- `tests/docx-export-format-smoke.js`
- `tests/khbd-4steps-workflow-smoke.js`

---

## Tiêu chí nghiệm thu
1. Phần I. Mục tiêu chỉ hiển thị đúng 1 dòng `c) Năng lực số: [5.3.TC2a]: ...`, tuyệt đối không lặp lại lần 2.
2. File Word (.docx) xuất ra hiển thị đẹp mắt:
   - `[5.3.TC2a]:` được in đậm, in nghiêng màu xanh dương `0369A1`, không còn dấu `***`.
   - `[9.B2.1]:` được in đậm, in nghiêng màu tím `6D28D9`, không còn dấu `***`.
3. 100% test suites PASS.
