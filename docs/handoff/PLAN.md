# PLAN

## Hiện trạng
- Trong `js/khbd-app.js` và `js/khbd-prompts.js`:
  1. Khi phân tích và định dạng đề mục SGK, hệ thống có cơ chế tự động gán số thứ tự tăng dần (`index + 1`, `${idx}. `).
  2. Điều này dẫn đến các sai phạm nghiêm trọng đối với tính chính xác của SGK:
     - Nếu SGK **KHÔNG ĐÁNH SỐ** (ví dụ đề mục chỉ ghi tên: *Khởi động*, *Định nghĩa lũy thừa*, *Tổng kết bài học*...), hệ thống lại tự ý đánh số `1.`, `2.`, `3.` vào trước tiêu đề.
     - Nếu SGK **ĐÃ CÓ ĐÁNH SỐ** (ví dụ: *1. Lũy thừa với số mũ tự nhiên* hoặc *I. Khái niệm*), hệ thống lại chèn thêm số dẫn đến bị lặp số (*1. 1. ...*) hoặc bị ép sai định dạng số (*1. I. ...*).

## Phạm vi
- Chuẩn hóa quy tắc tuyệt đối về Đề mục và Chỉ mục SGK:
  1. **Quy tắc bất di bất dịch**:
     - **SGK có chỉ số/ký hiệu gì thì giữ đúng 100% chỉ số/ký hiệu đó** (ví dụ: `1.`, `2.`, `I.`, `II.`, `A.`, `B.`, `1.1`, `1.2`...).
     - **SGK KHÔNG CÓ chỉ số thì TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ ĐÁNH SỐ** (giữ nguyên tên đề mục thuần túy, cấm tự chèn `1.`, `2.`, `Mục 1`, `Mục 2`).
  2. `js/khbd-app.js`:
     - Cập nhật `canvasTextbookAnalysisPrompt`: Ràng buộc AI ghi trường `title` nguyên văn 100% cả chỉ mục (nếu có) và tên đề mục. CẤM tự ý thêm số thứ tự nếu trang SGK không có.
     - Cập nhật `normalizeCanvasTextbookSection` & `formatCanvasTextbookContext`:
       + Bỏ hoàn toàn việc tự động gán `index = index + 1` và bỏ tiền tố `${idx}.`.
       + Chỉ xuất đúng `### ${section.title}` và `- ${section.title}` (không chèn thêm `Mục ${idx}:` hay `${idx}.`).
  3. `js/khbd-prompts.js`:
     - `extractTextbookSubsections`: Giữ nguyên vẹn 100% chuỗi `title` đã trích xuất từ SGK, không tự động sinh số thứ tự đè lên.
     - `GENERATE_ACTIVITY_B`: Tên các hoạt động con 2.1, 2.2... BẮT BUỘC hiển thị `### Hoạt động 2.k: [Tên nguyên văn đề mục trong SGK]` (nếu SGK có số `1. ...` thì là `### Hoạt động 2.1: 1. ...`, nếu SGK không có số thì là `### Hoạt động 2.1: ...`).
  4. Cập nhật test tự động `tests/khbd-textbook-exact-structure-smoke.js`.

## Ngoài phạm vi
- Không thay đổi các cấu trúc sư phạm khác.

## File dự kiến tác động
- `js/khbd-app.js`
- `js/khbd-prompts.js`
- `canvas_soankhbd.html`
- `backupcode viettailieu/canvas_soankhbd.html`
- `tests/khbd-textbook-exact-structure-smoke.js`

## Các bước thực hiện
1. **Sửa `canvasTextbookAnalysisPrompt` trong `js/khbd-app.js`**:
   - Thêm quy định rõ ràng:
     `"VỀ ĐỀ MỤC VÀ CHỈ SỐ: BẮT BUỘC sao chép chính xác 100% tên đề mục và chỉ số nhìn thấy trong SGK. Nếu SGK có ghi số/ký hiệu (ví dụ '1. Lũy thừa...', 'I. Khái niệm...', 'A. Định nghĩa...') thì giữ nguyên. Nếu SGK KHÔNG CÓ số thứ tự (chỉ ghi tiêu đề chữ) thì TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ Ý ĐÁNH SỐ THÊM."`
2. **Sửa `normalizeCanvasTextbookSection` & `formatCanvasTextbookContext` trong `js/khbd-app.js`**:
   - `normalizeCanvasTextbookSection`: Trả về `{ title: sectionTitle, coreKnowledge, activities }`, không ép `index: index + 1`.
   - `formatCanvasTextbookContext`:
     ```javascript
     sectionLines.push(`### ${section.title}`);
     sectionLines.push(`- Đề mục: ${section.title}`);
     ```
     (Tuyệt đối không có `${idx}.` hay `Mục ${idx}:`).
3. **Sửa `extractTextbookSubsections` trong `js/khbd-prompts.js`**:
   - Đảm bảo giữ nguyên văn trường `title` của đề mục, không tự động chèn thêm số.
4. **Kiểm thử tự động**:
   - Kiểm tra các trường hợp:
     + SGK có số `1. Lũy thừa...` -> Giữ đúng `1. Lũy thừa...` (không thành `1. 1. ...`).
     + SGK có số La Mã `I. Khái niệm...` -> Giữ đúng `I. Khái niệm...` (không bị đổi thành `1. Khái niệm...`).
     + SGK không có số `Khái niệm lũy thừa` -> Giữ nguyên `Khái niệm lũy thừa` (không bị tự động đánh số `1.`).
   - Chạy `node tests/khbd-textbook-exact-structure-smoke.js` và `node tests/canvas-soankhbd-smoke.js`.

## Rủi ro
- Phân bổ thời lượng (`subsections`): Dùng số lượng các mục thực tế có trong bài để tính toán thời gian cho Hoạt động B mà không cần phụ thuộc vào việc tiêu đề có đánh số hay không.

## Cách kiểm thử
- `node tests/khbd-textbook-exact-structure-smoke.js`.

## Tiêu chí nghiệm thu
- 100% đúng đề mục và chỉ số theo SGK.
- SGK không có chỉ số -> Tuyệt đối không tự động đánh số.
- SGK có chỉ số (1, 2, I, II, A, B) -> Giữ nguyên văn đúng chỉ số đó, không bị lặp số đúp (`1. 1. ...`).
- Tất cả smoke test PASS 100%.
