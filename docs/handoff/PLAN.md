# PLAN: Chuẩn hóa hiển thị Mã NLS, Mã AI và xử lý hàng không AI trong Phụ lục 1 (kèm sửa lỗi CSDL Canvas)

## Hiện trạng
1. **Hiển thị Mã NLS và Mã AI trong Phụ lục 1**:
   - Bảng Phụ lục 1 hiện tại đã tách thành 2 cột riêng biệt: Cột 5 là `Biểu hiện năng lực số`, Cột 6 là `Biểu hiện năng lực AI`.
   - Tuy nhiên, dữ liệu trong từng ô vẫn giữ nguyên tiền tố và dấu ngoặc vuông:
     + NLS: `[NLS: 1.1.TC2a - Sử dụng công cụ số để tìm kiếm thông tin theo yêu cầu]`
     + AI: `[AI: 8.A1.1 - Nhận diện vai trò dữ liệu đầu vào trong mô hình AI] (Áp dụng: tiết 1, 2).`
   - Vì tiêu đề cột đã ghi rõ "Biểu hiện năng lực số" và "Biểu hiện năng lực AI", việc lặp lại chữ `[NLS: ` và `[AI: ` cùng dấu ngoặc `]` gây rườm rà, lặp từ và choán diện tích bảng.
2. **Xử lý dòng không tích hợp AI**:
   - Đối với các bài học không được tick chọn tiết AI, cột `Biểu hiện năng lực AI` cần đảm bảo luôn tự động điền một dấu gạch ngang `-` rõ ràng, chuẩn văn bản hành chính theo CV 5512.
3. **Lỗi Tải/Lưu CSDL trong môi trường Canvas** (từ khảo sát trước):
   - `canvas_xaydungphuluc.html` trong iframe Canvas bị lỗi `Failed to parse URL` do dùng URL tương đối `api/user_phuluc_draft.php` và thiếu CORS + thiếu định danh tài khoản giáo viên (`username`).

## Phạm vi
- Cập nhật hàm tách và làm sạch mã `separateIntegration` trong `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`:
  + Bỏ tiền tố `[NLS: ` và dấu đóng `]` ở cột `Biểu hiện năng lực số`: `1.1.TC2a - Sử dụng công cụ số để tìm kiếm thông tin theo yêu cầu`.
  + Bỏ tiền tố `[AI: ` và dấu `]` ở cột `Biểu hiện năng lực AI`: `8.A1.1 - Nhận diện vai trò dữ liệu đầu vào trong mô hình AI (Áp dụng: tiết 1, 2).`
  + Tự động điền dấu `-` cho cột AI ở các bài học không được tick chọn tiết AI.
- Cập nhật các hàm phụ thuộc trong `xaydungphuluc.html` và `canvas_xaydungphuluc.html`:
  + `appendixAiCoverage` và `calculateComplianceReport`: Điều chỉnh regex để nhận diện mã NLS (`\d+\.\d+\.TC\w+`) và mã AI (`\d+\.A\d+\.\d+`) kể cả khi không còn `[NLS:` và `[AI:`.
  + `exportDocx`: Đảm bảo khi xuất Word, các ô NLS/AI hiển thị đúng chữ số màu chuẩn (NLS: `#0070C0`, AI: `#7030A0`), và dòng không có AI hiển thị đúng `-`.
- Đồng bộ sửa lỗi CSDL Canvas:
  + Backend `api/user_phuluc_draft.php`: Bật CORS và nhận diện user qua `username` khi không có session.
  + Frontend `canvas_xaydungphuluc.html`: Dùng `DRAFT_API_ENDPOINT` tuyệt đối và thêm ô nhập username.
- Cập nhật smoke tests: `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`.

## Ngoài phạm vi
- Không thay đổi bảng Phụ lục 3 (cột gộp `Mã NLS & AI (CV 3456 & QĐ 2422)` vẫn giữ `[NLS:` và `[AI:` để phân biệt hai loại mã khi nằm chung một ô).
- Không sửa đổi nội dung chuẩn hóa của CTGDPT 2018 (YCCĐ) hay danh mục mã NLS/AI gốc.

## File dự kiến tác động
- `xaydungphuluc.html`
- `backupcode viettailieu/canvas_xaydungphuluc.html`
- `api/user_phuluc_draft.php`
- `tests/xaydungphuluc-smoke.js`
- `tests/canvas-xaydungphuluc-smoke.js`

## Các bước thực hiện
1. **Bước 1: Bổ sung hàm làm sạch mã hiển thị NLS và AI**:
   - Viết hàm `cleanNlsColumnText(text)`:
     ```javascript
     function cleanNlsColumnText(text){
       if(!text||text==='-')return '-';
       const lines=String(text).split('\n').map(line=>{
         const l=line.trim();
         if(!l||l==='-')return '';
         return l.replace(/^\[\s*NLS\s*:\s*/i,'').replace(/\]\s*$/,'').trim();
       }).filter(Boolean);
       return lines.length?lines.join('\n'):'-';
     }
     ```
   - Viết hàm `cleanAiColumnText(text)`:
     ```javascript
     function cleanAiColumnText(text){
       if(!text||text==='-')return '-';
       const lines=String(text).split('\n').map(line=>{
         const l=line.trim();
         if(!l||l==='-')return '';
         return l.replace(/^\[\s*AI\s*:\s*/i,'').replace(/\](\s*\(Áp dụng:[^)]+\)\.?)/i,'$1').replace(/\]\s*$/,'').trim();
       }).filter(Boolean);
       return lines.length?lines.join('\n'):'-';
     }
     ```
2. **Bước 2: Cập nhật `separateIntegration` trong `xaydungphuluc.html` & `canvas_xaydungphuluc.html`**:
   - Khi tách phần NLS: Chạy qua `cleanNlsColumnText(...)`. Nếu không có hoặc NLS bị tắt, trả về `'-'`.
   - Khi tách phần AI: Nếu bài học không có tiết AI nào được chọn (hoặc AI bị tắt), trả về `'-'`. Nếu có, chạy qua `cleanAiColumnText(...)`.
3. **Bước 3: Cập nhật `appendixAiCoverage` và `calculateComplianceReport`**:
   - Cập nhật regex kiểm tra mã trong ô:
     + NLS: `/(?:\[\s*NLS\s*:\s*)?\b\d+\.\d+\.TC\w+/i`
     + AI: `/(?:\[\s*AI\s*:\s*|\b)\d+\.A\d+\.\d+/i`
     + Phạm vi tiết: `/(?:Áp dụng:\s*tiết\s*([\d, ]+))/i`
4. **Bước 4: Cập nhật `api/user_phuluc_draft.php` và `canvas_xaydungphuluc.html`**:
   - Cấu hình CORS và hỗ trợ `username` cho API nháp.
   - Thêm ô tài khoản giáo viên và nút cứu hộ Local/JSON trong Canvas.
5. **Bước 5: Cập nhật kiểm thử và chạy test**:
   - Cập nhật các câu lệnh `assert` trong `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js` khớp với định dạng mã sạch mới.
   - Chạy `node tests/xaydungphuluc-smoke.js; node tests/canvas-xaydungphuluc-smoke.js` đảm bảo PASS 100%.

## Rủi ro
- Khi loại bỏ tiền tố `[NLS:` và `[AI:`, các hàm báo cáo thẩm định sư phạm (`calculateComplianceReport`) hoặc xuất Docx nếu tìm cứng chuỗi `[NLS:` sẽ bị đếm thiếu -> Cần đồng bộ sửa regex nhận diện cả định dạng mã sạch.

## Cách kiểm thử
1. Chạy `node tests/xaydungphuluc-smoke.js` -> PASS.
2. Chạy `node tests/canvas-xaydungphuluc-smoke.js` -> PASS.
3. Chạy `node tests/xaydungphuluc-integration-smoke.js` -> PASS.
4. Kiểm tra trực quan:
   - Cột Biểu hiện năng lực số chỉ hiện mã và mô tả: `1.1.TC2a - Sử dụng công cụ số...` (không có `[NLS:` và `]`).
   - Cột Biểu hiện năng lực AI chỉ hiện mã, mô tả và phạm vi: `8.A1.1 - Nhận diện... (Áp dụng: tiết 1, 2).` (không có `[AI:` và `]`).
   - Các bài học không có AI hiển thị đúng một dấu `-`.

## Tiêu chí nghiệm thu
- Phụ lục 1 hiển thị mã sạch không còn `[NLS: ]` và `[AI: ]`.
- Mọi dòng không chọn tiết AI đều tự động điền `-`.
- Xuất file Word (.docx) hiển thị đúng format sạch và giữ đúng màu xanh/tím.
- Toàn bộ bài test chạy PASS.
