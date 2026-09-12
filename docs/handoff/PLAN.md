# PLAN: Xử lý lỗi "Bad control character in string literal in JSON" khi Gemini sinh Phụ lục trên Canvas và Xây dựng Phụ lục

## Hiện trạng & Phân tích nguyên nhân

1. **Hiện tượng lỗi**:
   - Khi chạy "Sinh trọn bộ Phụ lục" hoặc "Sinh PL 1" trên `canvas_xaydungphuluc.html` (chạy trên môi trường Google Gemini Canvas):
     - Sau khi nhận diện xong 87 dòng PPCT từ tệp, hệ thống chuyển sang Giai đoạn 2: *sinh nội dung phụ lục...*
     - Gọi AI cho Phụ lục 1...
     - Lỗi xuất hiện ngay tại hộp thoại tiến trình:
       `Lỗi AI: Bad control character in string literal in JSON at position 12828 (line 222 column 73)`
2. **Nguyên nhân kỹ thuật**:
   - Trong `canvas_xaydungphuluc.html` (dòng 247) và `xaydungphuluc.html` (dòng 185):
     ```javascript
     async function readGeminiResponse(result) {
         ...
         return JSON.parse(String(text).replace(/^```json\s*|\s*```$/g, ''));
     }
     ```
   - Khi phân tích PPCT lớn (ví dụ 87 bài/tiết), Gemini 2.5 Flash trả về phản hồi JSON có dung lượng lớn (15KB - 30KB).
   - Trong chuỗi giá trị (string literal) của các trường như `lesson`, `muc_tieu`, `noi_dung`, `ghi_chu`, hoặc `yeu_cau_can_dat`, mô hình AI thường chèn các ký tự điều khiển thô (raw unescaped control characters) như:
     - Xuống dòng thô `0x0A` (`\n`) hoặc `0x0D` (`\r`) thay vì chuỗi thoát `\n` (`\\n`).
     - Ký tự tab thô `0x09` (`\t`).
     - Các mã điều khiển ASCII từ `0x00` đến `0x1F`.
   - Theo đặc tả chuẩn JSON (RFC 8259, mục 7 "Strings"): tất cả ký tự điều khiển trong dải U+0000 đến U+001F bắt buộc phải được escape (`\n`, `\r`, `\t`, `\u00XX`). Nếu để thô bên trong cặp dấu ngoặc kép `"..."`, hàm `JSON.parse()` của trình duyệt (V8 / Chromium) sẽ lập tức văng lỗi `SyntaxError: Bad control character in string literal in JSON at position ...`.
   - Ngoài ra, AI đôi khi có thể để lại trailing comma (dấu phẩy thừa trước `}` hoặc `]`) hoặc trả về các ký tự backslash LaTeX chưa escape (`\alpha`, `\times`).

---

## Mục tiêu & Giải pháp thiết kế

### 1. Xây dựng bộ phân tích cú pháp an toàn `safeParseAiJson(raw)`
Triển khai hàm `safeParseAiJson(raw)` trong cả `canvas_xaydungphuluc.html` và `xaydungphuluc.html`:
1. **Làm sạch định dạng cơ bản**:
   - Xóa bỏ các khối bọc markdown code fence: `replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '')`.
2. **Fast-path**:
   - Thử gọi `JSON.parse(str)` trực tiếp trước. Nếu JSON chuẩn hoàn toàn, trả về ngay lập tức để đạt hiệu năng cao nhất.
3. **Trích xuất cấu trúc JSON ngoài cùng**:
   - Nếu AI trả kèm lời thoại ("Dưới đây là JSON:", "Hy vọng giúp ích..."), tìm vị trí `{` hoặc `[` đầu tiên và `}` hoặc `]` cuối cùng để cắt đúng phạm vi JSON.
4. **Bộ quét (Scanner) xử lý ký tự điều khiển bên trong chuỗi**:
   - Duyệt qua từng ký tự của chuỗi với trạng thái `inString`:
     - Theo dõi dấu backslash `\` và cặp dấu ngoặc kép `"`.
     - Khi `inString === true`:
       - Nếu gặp ký tự có mã `code < 32`:
         - `\n` -> thay bằng chuỗi thoát `\\n`.
         - `\r` -> thay bằng chuỗi thoát `\\r`.
         - `\t` -> thay bằng chuỗi thoát `\\t`.
         - Ký tự điều khiển khác -> thay bằng `\\u` + mã hex 4 chữ số (`code.toString(16).padStart(4, '0')`).
       - Nếu gặp backslash thoát không hợp lệ trong JSON (ví dụ LaTeX `\alpha`), tự động chuẩn hóa thành `\\alpha`.
5. **Xử lý dấu phẩy thừa (Trailing Comma Recovery)**:
   - Nếu vẫn lỗi, xóa dấu phẩy thừa trước dấu đóng: `replace(/,\s*([\}\]])/g, '$1')` và thử lại `JSON.parse()`.

### 2. Tích hợp vào các luồng gọi AI
- Trong `canvas_xaydungphuluc.html`:
  - Thay thế `JSON.parse(String(text).replace(/^```json\s*|\s*```$/g,''))` trong `readGeminiResponse` bằng `safeParseAiJson(text)`.
- Trong `xaydungphuluc.html`:
  - Cập nhật `readGeminiResponse` và `callMistral` sử dụng `safeParseAiJson`.
- Đảm bảo tính nhất quán giữa hai trang để thỏa mãn điều kiện đồng bộ hàm `for(const name of sourceFunctions) assert(targetFunctions.has(name))` trong bộ test.

---

## Phạm vi thực hiện

1. `canvas_xaydungphuluc.html`:
   - Thêm hàm `safeParseAiJson(raw)`.
   - Cập nhật `readGeminiResponse` gọi `safeParseAiJson`.
2. `xaydungphuluc.html`:
   - Thêm hàm `safeParseAiJson(raw)`.
   - Cập nhật `readGeminiResponse` và `callMistral` gọi `safeParseAiJson`.
3. `tests/canvas-xaydungphuluc-smoke.js`:
   - Bổ sung test kiểm thử `safeParseAiJson` với các trường hợp:
     - Ký tự xuống dòng thô trong chuỗi JSON (`Bad control character`).
     - Ký tự tab thô trong chuỗi JSON.
     - Dấu phẩy thừa (`trailing comma`).
     - Khối code markdown và lời thoại bao quanh.
4. `tests/xaydungphuluc-smoke.js`:
   - Xác nhận bộ test vượt qua 100%.

---

## Ngoài phạm vi

- Không thay đổi prompt hoặc cấu trúc trả về của Phụ lục 1, 2, 3.
- Không can thiệp vào logic chuẩn hóa dữ liệu sau khi parse (`normalizeAppendix`).

---

## Kế hoạch kiểm thử (Verification Plan)

1. `node tests/canvas-xaydungphuluc-smoke.js`: PASS toàn bộ kiểm thử cấu trúc và `safeParseAiJson`.
2. `node tests/xaydungphuluc-smoke.js`: PASS.
3. `node tests/baogiang-weekday-segment-smoke.js`: PASS.
4. `node tests/timetable-render-smoke.js`: PASS.
5. `node tests/auto-reload-smoke.js`: PASS.
6. `git diff --check`: PASS, không có lỗi định dạng hay khoảng trắng thừa.
