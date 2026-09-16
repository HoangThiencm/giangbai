# PLAN

## Hiện trạng
- Trong `thitructuyen.html`:
  1. Nút bấm **"Nạp Đáp Án"** mở popup `AnswerImportModal`.
  2. Tại hàm `handleManualImport` (dòng ~1012), regex hiện tại `textInput.toUpperCase().match(/(\d+)[\.\-\:\s]*([A-D])/g)` chỉ bắt được các câu Trắc nghiệm 4 lựa chọn (A, B, C, D). Khi gặp `13.Đúng`, `14.Sai`, `15.27`, `16.2000`, `17.100`, `18.30` thì hoàn toàn bỏ qua.
  3. Tại hàm `handleBulkAnswer` (dòng ~2006), logic cập nhật chỉ tìm trong map `A, B, C, D` để gán `correct_index`, không gán `correct_answers` cho câu Đúng/Sai (`q.type === 'tf'`) và không gán `correct_answer` cho câu Trả lời ngắn (`q.type === 'short_answer'`).

## Phạm vi
- Cập nhật trong `thitructuyen.html`:
  1. `handleManualImport` trong `AnswerImportModal`: Dùng hàm chuẩn hóa `getImportedAnswerKey("Đáp án: " + textInput)` hoặc parse token theo thứ tự câu để trích xuất đầy đủ các loại câu hỏi (MC, TF, Short Answer).
  2. `handleBulkAnswer`: Nâng cấp để kiểm tra loại câu hỏi `q.type` (hoặc cấu trúc câu hỏi):
     - Nếu câu `mc`: gán `correct_index` theo A-D.
     - Nếu câu `tf`: gán `correct_answers` (mảng 4 boolean hoặc mảng boolean theo giá trị).
     - Nếu câu `short_answer`: gán `correct_answer` là chuỗi giá trị đáp án.
  3. Cập nhật test `tests/thitructuyen-cv7991-answerkey-smoke.js` để bao phủ cả trường hợp gọi qua `handleBulkAnswer` / `handleManualImport`.

## Ngoài phạm vi
- Không đổi giao diện bảng thi hay backend chấm điểm.

## File dự kiến tác động
- `thitructuyen.html`
- `tests/thitructuyen-cv7991-answerkey-smoke.js`

## Các bước thực hiện
1. **Cập nhật `handleManualImport` trong `AnswerImportModal`**:
   - Gọi `getImportedAnswerKey("Đáp án: " + textInput)` (hoặc duyệt các cặp câu/đáp án):
     ```javascript
     const parsedMap = getImportedAnswerKey("Đáp án:\n" + textInput);
     const results = Object.keys(parsedMap).map(num => ({
         index: parseInt(num, 10),
         rawEntry: parsedMap[num],
         answer: importedAnswerKeyLetter(parsedMap[num]) || importedAnswerKeyText(parsedMap[num]),
         tfList: importedAnswerKeyTfList(parsedMap[num])
     }));
     ```
   - Nếu `results.length === 0`, báo lỗi định dạng. Ngược lại gọi `onImport(results)` và đóng modal.
2. **Cập nhật `handleBulkAnswer(importedData)`**:
   - Với mỗi câu hỏi `q` tại vị trí toàn cục `globalIdx`:
     - Tìm `found = importedData.find(d => d.index === globalIdx)`.
     - Nếu `found`:
       - Xác định loại câu `qType = q.type || (q.correct_answers ? 'tf' : (q.correct_answer !== undefined && (!q.options || q.options.length === 0) ? 'short_answer' : 'mc'))`.
       - Nếu `qType === 'tf'`:
         + Nếu `found.tfList`: gán `correct_answers: found.tfList`.
         + Hoặc nếu `found.rawEntry?.type === 'tf'` / `found.answer`: parse thành boolean hoặc mảng boolean để gán vào `correct_answers`.
       - Nếu `qType === 'short_answer'`:
         + Gán `correct_answer: String(found.answer || found.rawEntry?.value || "")`.
       - Nếu `qType === 'mc'`:
         + Map `A: 0, B: 1, C: 2, D: 3` gán vào `correct_index`.
3. **Kiểm thử**:
   - Thêm test case mô phỏng gọi `handleBulkAnswer` với 18 câu đề mẫu và danh sách đáp án hỗn hợp.
   - Chạy `node tests/thitructuyen-cv7991-answerkey-smoke.js`.

## Rủi ro
- Định dạng nạp từ ảnh AI (`aiResult`): giữ nguyên định dạng `{ index, answer }` tương thích ngược.

## Cách kiểm thử
- `node tests/thitructuyen-cv7991-answerkey-smoke.js`.

## Tiêu chí nghiệm thu
- Khi dán chuỗi `1.B ... 12.C 13.Đúng 14.Sai 15.27 16.2000 17.100 18.30` vào Modal Nạp Đáp Án, cả 18 câu trên giao diện soạn đề đều nhận được đáp án chính xác (12 câu MC có `correct_index`, 2 câu TF có `correct_answers`, 4 câu TLN có `correct_answer`).
