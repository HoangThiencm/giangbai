# PLAN

## Hiện trạng
- Trong tệp `thitructuyen.html` (chức năng Tạo/Nhập đề thi từ file Word/Văn bản và nhận diện bảng đáp án):
  1. Hàm `getImportedAnswerKey` hiện chỉ dùng biểu thức chính quy `pairRegex = /(\d{1,3})\s*[\.\)\-:]?\s*([A-D])/gi` để bóc tách đáp án Trắc nghiệm 4 lựa chọn (A, B, C, D).
  2. Hàm `stripImportedAnswerKey` cũng chỉ đếm số cặp chữ cái A-D để xác định và cắt bỏ phần Bảng đáp án ở cuối văn bản.
  3. Khi đề thi theo cấu trúc **Công văn 7991/BGDĐT** (gồm 3 phần: Phần I - Trắc nghiệm nhiều lựa chọn; Phần II - Đúng/Sai; Phần III - Trả lời ngắn), bảng đáp án có dạng hỗn hợp:
     ```text
     1.B   2.C   3.A   4.B   5.C   6.B   7.A   8.D   9.B   10.C   11.C   12.C   
     13.Đúng   14.Sai   
     15.27	16.2000   17.100   18.30
     ```
     -> Hệ thống hiện tại bỏ qua toàn bộ đáp án của các câu Đúng/Sai (13, 14) và Trả lời ngắn (15, 16, 17, 18), khiến các câu này bị thiếu đáp án chuẩn hoặc giáo viên phải tự nhập tay lại.

## Phạm vi
- Tệp `thitructuyen.html`:
  + Nâng cấp hàm `getImportedAnswerKey` để nhận diện đa dạng cả 3 loại đáp án:
    1. Trắc nghiệm nhiều lựa chọn (`A-D`).
    2. Đúng / Sai (`Đúng`, `Sai`, `Đ`, `S`, `True`, `False`, `T`, `F`, hoặc dạng tổ hợp các ý `a-Đ, b-S, c-Đ, d-S`).
    3. Trả lời ngắn (số nguyên, số thực, phân số, kết quả dạng chuỗi ngắn: `27`, `2000`, `100`, `30`, `3.14`, `-1/2`...).
  + Cập nhật hàm `stripImportedAnswerKey` để nhận diện chính xác phần Bảng đáp án hỗn hợp cuối đề và cắt bỏ khỏi nội dung câu hỏi.
  + Cập nhật hàm `parseLatexWordQuiz` để gán chính xác `correct_answers` cho câu `tf` và `correct_answer` cho câu `short_answer` từ `answerKey`.
- Tệp test kiểm thử mới hoặc bổ sung: `tests/thitructuyen-cv7991-answerkey-smoke.js` (hoặc cập nhật `scratch/test_cv7991_parse.js`) để kiểm tra tự động chuỗi đáp án mẫu.

## Ngoài phạm vi
- Không thay đổi thuật toán chấm điểm và phân bổ trọng số điểm chuẩn CV 7991 (6.0đ trắc nghiệm - 2.0đ đúng sai - 2.0đ trả lời ngắn) trong `backend/thitructuyen.py` và `api/exam.php`.
- Không thay đổi luồng giao diện làm bài thi của học sinh.

## File dự kiến tác động
- `thitructuyen.html`
- `tests/thitructuyen-cv7991-answerkey-smoke.js` (tạo test kiểm thử)

## Các bước thực hiện
1. **Khảo sát & Tái hiện**:
   - Vị trí `getImportedAnswerKey` và `stripImportedAnswerKey` trong `thitructuyen.html` (khoảng dòng 1285–1306).
   - Vị trí gán đáp án cho `tf` và `short_answer` trong `parseLatexWordQuiz` (khoảng dòng 1360–1455).
2. **Cải tiến `getImportedAnswerKey(text)`**:
   - Bắt block đáp án `(?:đáp\s*án|dap\s*an|answer\s*key|answers?)\s*[:：]`.
   - Phân tích từng token `(\d{1,3})\s*[\.\)\-:]\s*([^\s\t\n\r]+)`:
     + Nếu khớp `^[A-Da-d]$`: lưu `{ type: 'mc', value: char.toUpperCase() }` hoặc gán chữ cái hoa.
     + Nếu khớp `^(Đúng|Sai|Đ|S|True|False|T|F)$`: lưu `{ type: 'tf', value: /đ|đúng|t|true/i.test(val) }`.
     + Nếu là chuỗi khác (như `27`, `2000`, `100`, `30`): lưu `{ type: 'short_answer', value: val.trim() }`.
     + Hỗ trợ thêm trường hợp câu Đúng/Sai có nhiều ý phụ (ví dụ: `13. a.Đúng b.Sai c.Đúng d.Sai` hoặc `13: Đ, S, Đ, S`).
3. **Cải tiến `stripImportedAnswerKey(text)`**:
   - Đếm số lượng cặp nhận diện được từ `getImportedAnswerKey`. Nếu `>= 1`, cắt bỏ phần text bảng đáp án khỏi đề thi.
4. **Cập nhật ánh xạ đáp án trong `parseLatexWordQuiz`**:
   - Với câu `type: "tf"`: Nếu `correctAnswers` chưa được gán từ `inlineAnswer`, lấy từ `answerKey[item.number]`.
   - Với câu `type: "short_answer"`: Gán `correct_answer: inlineAnswer || (answerKey[item.number] ? String(answerKey[item.number]) : "")`.
5. **Tạo bài test kiểm thử & nghiệm thu**:
   - Viết test với chuỗi đề thi chứa đúng đoạn bảng đáp án người dùng đưa ra:
     `1.B 2.C 3.A 4.B 5.C 6.B 7.A 8.D 9.B 10.C 11.C 12.C`
     `13.Đúng 14.Sai`
     `15.27 16.2000 17.100 18.30`
   - Kiểm tra kết quả parse trả về đúng 18 câu với đầy đủ đáp án cho cả 3 phần.

## Rủi ro
- Khoảng trắng dạng Tab `\t` hoặc nhiều dấu cách liên tiếp: đã có `normalizeImportedQuizText` thay thế `\t` thành ` ` và chuẩn hóa khoảng trắng.
- Giá trị số thập phân có dấu chấm (VD: `15. 3.14`): regex cần phân biệt rõ số thứ tự câu `15.` và giá trị đáp án `3.14`.

## Cách kiểm thử
- Chạy kiểm thử tự động với Node.js: `node tests/thitructuyen-cv7991-answerkey-smoke.js`.
- Kiểm tra tính tương thích khi nhập file Word hoặc dán text đề thi trực tiếp trên giao diện `thitructuyen.html`.

## Tiêu chí nghiệm thu
- Tự động nhận diện chính xác 100% các câu trắc nghiệm (1..12: B, C, A, B, C, B, A, D, B, C, C, C).
- Tự động nhận diện câu Đúng/Sai (13: Đúng, 14: Sai).
- Tự động nhận diện các câu Trả lời ngắn (15: 27, 16: 2000, 17: 100, 18: 30).
- Không làm xáo trộn các định dạng đề thi cũ (100% trắc nghiệm thuần).
