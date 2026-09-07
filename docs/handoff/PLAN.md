# PLAN: Khắc phục Triệt để Dấu "]" Sót lại ở Cuối Dòng NLS & AI, Hoàn thiện Tùy chỉnh Phân bổ NLS và Ô AI Rỗng

## Hiện trạng
1. **Lỗi sót lại dấu "]" ở cuối dòng mô tả NLS và AI**:
   - Khi hiển thị Phụ lục 1, ở cuối câu mô tả NLS hoặc AI vẫn còn xuất hiện dấu đóng ngoặc vuông `]`, ví dụ:
     + `5.3.TC2a - Sử dụng phần mềm GeoGebra vẽ đồ thị].`
     + `8.A1.1 - Học sinh sử dụng AI để giải bài tập]. (Áp dụng: tiết 1).`
     + `8.A1.1 - Học sinh sử dụng AI hỗ trợ học tập].`
   - **Nguyên nhân kỹ thuật**:
     + Regex hiện tại trong `cleanNlsColumnText` và `cleanAiColumnText` dùng `replace(/[\],\s]+$/g, '')`. Khi câu mô tả của LLM kết thúc bằng dấu chấm sau ngoặc (`].`) hoặc dấu chấm phẩy/khoảng trắng (`] .`), regex bị chặn lại bởi ký tự `.` và không xóa được dấu `]`.
     + Trong `enrichNlsCode`: biến `after` cắt phần chuỗi sau mã bằng `slice(...)` mà không làm sạch dấu `]` ở đuôi, dẫn đến kết quả trả về `${code} - ${after}` vẫn giữ nguyên dấu `]` hoặc `].`.
     + Trong `cleanAiColumnText`: cụm `(Áp dụng: tiết X)` được nối vào sau chuỗi đã có sẵn dấu `]` (ví dụ `Mô tả AI] (Áp dụng: ...)`), khiến dấu `]` bị kẹp lại ở giữa hoặc cuối dòng.
2. **Các yêu cầu sư phạm và kỹ thuật kèm theo**:
   - Tùy chỉnh phân bổ số lượng mã NLS trên giao diện Mục 4 (1 tiết: 2 mã; ≥ 2 tiết có AI: 2 mã; ≥ 2 tiết không AI: 2–3 mã).
   - Cột AI trong Phụ lục 1 để trống hoàn toàn (chuỗi rỗng `''`) đối với các bài không chọn AI.
   - Tăng timeout gọi Gemini lên 90s–120s.

## Phạm vi
- Cập nhật hàm làm sạch `cleanNlsColumnText`, `enrichNlsCode`, `cleanAiColumnText` trên cả:
  + `xaydungphuluc.html`
  + `backupcode viettailieu/canvas_xaydungphuluc.html`
- Cập nhật giao diện tùy chọn phân bổ NLS theo tiết & AI tại Mục 4.
- Cập nhật các bài kiểm thử tự động trong `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`.

## Ngoài phạm vi
- Không can thiệp vào Phụ lục 3 (cột gộp vẫn cần giữ tiền tố `[NLS: ...]` và `[AI: ...]`).
- Không đổi cấu trúc CSDL hay luồng lưu nháp.

## File dự kiến tác động
- `xaydungphuluc.html`
- `backupcode viettailieu/canvas_xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `tests/canvas-xaydungphuluc-smoke.js`

## Các bước thực hiện

### Bước 1: Khắc phục triệt để việc sót dấu "]" trong `cleanNlsColumnText` và `enrichNlsCode`
1. Cập nhật `enrichNlsCode(line)`:
   - Làm sạch triệt để `after`:
     ```javascript
     function enrichNlsCode(line){
       const match = String(line || '').match(/\b(\d+\.\d+\.TC\w+)\b/i);
       if(!match) return String(line || '').trim();
       const code = match[1];
       let after = String(line).slice((match.index || 0) + code.length).replace(/^\s*[-:–—]?\s*/, '').trim();
       // Bóc tách triệt để dấu ] ở cuối chuỗi, kể cả khi đi kèm dấu chấm hoặc dấu phẩy
       after = after.replace(/\s*\]\s*(?=[.,;]?\s*$)/g, '').replace(/[\],\s]+$/g, '').trim();
       if(after) return `${code} - ${after}`;
       const entry = typeof KHBD_STANDARDS !== 'undefined' ? KHBD_STANDARDS.digital?.entries?.find(item => String(item.code).toLowerCase() === code.toLowerCase()) : null;
       return entry ? `${code} - ${entry.label}` : code;
     }
     ```
2. Cập nhật `cleanNlsColumnText(text)`:
   - Bóc tách tiền tố `[NLS:` và loại bỏ mọi dấu `]` ở cuối mục trước khi chuyển sang `enrichNlsCode`:
     ```javascript
     function cleanNlsColumnText(text){
       const lines = String(text || '').split(/\n|\s*,\s*(?=\[?\s*(?:NLS\s*:\s*)?\d+\.\d+\.TC\w+)/i)
         .map(line => {
           let l = line.replace(/^\s*\[\s*(?:NLS\s*:\s*)?/i, '').replace(/^\s*\[/, '');
           l = l.replace(/\s*\]\s*(?=[.,;]?\s*$)/g, '').replace(/[\],\s]+$/g, '').trim();
           return l;
         })
         .filter(line => line && line !== '-')
         .map(enrichNlsCode)
         .map(line => line.replace(/\s*\]\s*(?=[.,;]?\s*$)/g, '').replace(/[\],\s]+$/g, '').trim())
         .filter(Boolean);
       return lines.length ? lines.join('\n') : '';
     }
     ```

### Bước 2: Khắc phục triệt để việc sót dấu "]" trong `cleanAiColumnText`
1. Cập nhật `cleanAiColumnText(text)`:
   - Xóa sạch dấu `]` trước phạm vi `(Áp dụng: ...)` hoặc ở cuối dòng (kể cả có dấu chấm hay không):
     ```javascript
     function cleanAiColumnText(text){
       const lines = String(text || '').split('\n')
         .map(line => {
           let l = line.replace(/^\s*\[\s*(?:AI\s*:\s*)?/i, '').replace(/^\s*\[/, '');
           // Xóa dấu ] đứng trước dấu chấm hoặc trước cụm (Áp dụng: ...)
           l = l.replace(/\s*\]\s*(?=[.,;]?\s*(?:\(Áp dụng|$))/gi, '');
           // Chuẩn hóa khoảng trắng trước cụm (Áp dụng: ...)
           l = l.replace(/([^\s])(\(Áp dụng:[^)]+\))/gi, '$1 $2');
           // Xóa mọi dấu ] hoặc dấu phẩy thừa ở cuối dòng
           l = l.replace(/[\],\s]+$/g, '').trim();
           return l;
         })
         .filter(line => line && line !== '-');
       return lines.length ? lines.join('\n') : '';
     }
     ```

### Bước 3: Đồng bộ tùy chỉnh phân bổ NLS và ô AI rỗng
1. Giao diện Mục 4: Có bộ chọn phân bổ NLS thông minh theo số tiết & AI (1 tiết: 2 mã; ≥ 2 tiết có AI: 2 mã; ≥ 2 tiết không AI: tùy chọn 2–3 mã).
2. Prompt LLM: Quy định rõ số lượng mã NLS cho từng bài và cấm xuất dấu `]` trơ trọi.
3. Cột AI: Nếu không có nội dung AI thì để ô trống `''`.

### Bước 4: Cập nhật Smoke Test và Kiểm thử
1. Thêm các trường hợp kiểm thử đặc thù trong `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`:
   - Chuỗi NLS có `].` ở cuối: `[NLS: 5.3.TC2a - Sử dụng phần mềm GeoGebra].` -> làm sạch thành `5.3.TC2a - Sử dụng phần mềm GeoGebra.` (không còn `]`).
   - Chuỗi AI có `].` trước hoặc sau `(Áp dụng: ...)`:
     `[AI: 8.A1.1 - Học sinh sử dụng AI]. (Áp dụng: tiết 1).` -> `8.A1.1 - Học sinh sử dụng AI. (Áp dụng: tiết 1).` (hoàn toàn không còn `]`).
   - Chuỗi AI kết thúc bằng `]`: `8.A1.1 - Mô tả AI]` -> `8.A1.1 - Mô tả AI`.
2. Chạy kiểm thử:
   - `node tests/canvas-xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`

## Rủi ro
- Khi xử lý chuỗi regex xóa `]`, không được xóa nhầm dấu ngoặc đơn `)` trong phạm vi tiết `(Áp dụng: tiết X)`.

## Cách kiểm thử
1. `node tests/canvas-xaydungphuluc-smoke.js` -> PASS.
2. `node tests/xaydungphuluc-smoke.js` -> PASS.
3. Kiểm tra các fixture test đặc thù với các chuỗi kết thúc bằng `].`, `]`, `],`, `] .` đều biến mất ký tự `]`.
4. Mở giao diện thực tế: kiểm tra cột NLS và AI trên bảng xem trước không còn bất kỳ ký tự `]` nào ở cuối dòng hay trước `(Áp dụng: ...)`.

## Tiêu chí nghiệm thu
- Không còn bất kỳ dấu `]` nào xuất hiện ở cuối dòng hay bị kẹp trước dấu chấm trong cột NLS và cột AI.
- Phụ lục 1 hiển thị mô tả NLS và AI hoàn toàn sạch sẽ, đúng chuẩn sư phạm.
- Toàn bộ smoke test đều PASS.
