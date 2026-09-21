# PLAN: Xuất File Word (.docx) Chuẩn Cấu Trúc Cho Game Giáo Dục từ taobaitap.html

## 1. Hiện trạng & Phân tích Yêu cầu

### Hiện trạng
1. **Tại `taobaitap.html`:**
   - Giáo viên tạo bài tập (từ chủ đề, PDF scan, tài liệu Word/ảnh, hoặc bộ câu hỏi tổng hợp).
   - Ở Bước 2 ("KẾT QUẢ TẠO ĐỀ"), hệ thống cung cấp các nút xuất:
     + `Xuất Mẫu CV 7991`: Xuất theo thể thức văn bản hành chính Công văn 7991 (chia 3 phần Phần I, II, III).
     + `Xuất 100% TN`: Xuất bảng 2 cột kèm ký hiệu `*` sau phương án đúng.
     + `.txt`: File text đơn thuần.
     + `LaTeX`: Giữ nguyên công thức LaTeX nhưng dùng bảng 2 cột `options-table` và bảng đáp án ở cuối.
     + `DẠY NGAY`: Chế độ trình chiếu trực tiếp trên máy chiếu.
     + `🚀 THI TRỰC TUYẾN`: Đóng gói và liên thông 1-Click sang `thitructuyen.html`.
   - **Vấn đề khi giáo viên lấy các file Word hiện tại nạp vào Game Giáo Dục (`trochoi.html`):**
     - `De_Thi_Tong_Hop.docx` (`exportWord`): Chuyển đổi công thức LaTeX sang MathML (`<math>`). Khi thư viện `Mammoth` trong `trochoi.html` đọc file Word, toàn bộ công thức MathML bị loại bỏ hoàn toàn, dẫn đến câu hỏi bị mất sạch công thức toán!
     - `De_Thi_CV7991.docx`: Chia nhiều phần, có phần II (4 ý mệnh đề) và phần III (trả lời ngắn) không theo mẫu 4 lựa chọn A-B-C-D nên bộ bóc tách `GameQuizImporter` bỏ qua.
     - `options-table` (dạng bảng 2 cột): `Mammoth` trích xuất nội dung bảng đôi khi bị dính chữ hoặc xáo trộn thứ tự dòng.

2. **Cơ chế nạp file Word của Game Giáo Dục (`trochoi.html` / `js/game-quiz-importer.js`):**
   - Game Giáo Dục sử dụng `mammoth.extractRawText({ arrayBuffer })` để lấy văn bản thô từ file `.docx`.
   - Sau đó chuyển văn bản qua bộ phân tích `GameQuizImporter`:
     + **Đối với các game Trắc nghiệm (Mở khóa kiến thức, Tháp tri thức, Đấu trường, Đua xe, Đua vịt, Thoát hiểm):**
       `GameQuizImporter.parseQuizQuestions` yêu cầu cấu trúc:
       ```text
       Câu 1: [Nội dung câu hỏi - giữ nguyên công thức LaTeX \(...\)]
       A. [Nội dung lựa chọn A]
       B. [Nội dung lựa chọn B]
       C. [Nội dung lựa chọn C]
       D. [Nội dung lựa chọn D]
       Đáp án: A (hoặc B, C, D)
       Lời giải: [Giải thích nếu có]
       ```
       (Hoặc có bảng đáp án `BẢNG ĐÁP ÁN: 1.A 2.B...` ở cuối).
     + **Đối với Game Ghép Cặp (`matching`):**
       `GameQuizImporter.parseMatchingPairs` yêu cầu:
       `[Khái niệm/Vế trái] - [Định nghĩa/Vế phải]`
       (hoặc nếu là câu hỏi trắc nghiệm thì tự động lấy câu hỏi làm vế trái và đáp án đúng làm vế phải).

### Yêu cầu người dùng
Giáo viên muốn tạo bài tập từ tab `taobaitap.html`, sau đó xuất một file Word chuyên biệt cho Game Giáo Dục sao cho khi vào `trochoi.html` chỉ cần tải (upload) file Word này lên là trò chơi lập tức nhận diện đầy đủ câu hỏi, đáp án và công thức toán học!

---

## 2. Kế hoạch Triển khai Chi tiết cho Coder

### Bước 1: Xây dựng hàm `exportWordForGame()` trong `taobaitap.html`

Vị trí: Bổ sung trong `taobaitap.html` (trước khối render của `App`, cạnh các hàm `exportWord...`).

1. **Quy tắc định dạng tài liệu Word cho Game:**
   - **Tên file tải về:** `De_Thi_Game_Giao_Duc.docx`.
   - **Công thức Toán:** Giữ nguyên cú pháp LaTeX `\(...\)` hoặc `$...$` (tuyệt đối KHÔNG dùng MathML để `Mammoth` đọc được nguyên vẹn 100%).
   - **Cấu trúc mỗi dòng câu hỏi:** Dùng các thẻ `<p>` riêng biệt cho từng dòng thay vì `<table>`, đảm bảo `Mammoth` chuyển thành các dòng `\n` sạch:
     + Dòng 1: `<p><b>Câu {i + 1}:</b> {Nội dung câu hỏi}</p>`
     + Dòng 2: `<p>A. {Phương án A}</p>`
     + Dòng 3: `<p>B. {Phương án B}</p>`
     + Dòng 4: `<p>C. {Phương án C}</p>`
     + Dòng 5: `<p>D. {Phương án D}</p>`
     + Dòng 6: `<p><b>Đáp án:</b> {A/B/C/D}</p>`
     + Dòng 7 (nếu có): `<p><b>Lời giải:</b> {Giải thích}</p>`
     + Dòng 8: `<p></p>` (ngăn cách các câu).

2. **Bộ chuyển đổi thông minh cho các dạng câu hỏi khác nhau:**
   - **Câu Trắc nghiệm 4 phương án (`multiple-choice`):**
     Lấy 4 lựa chọn từ `q.options`, xác định ký tự đáp án đúng `String.fromCharCode(65 + q.correctAnswerIndex)`.
   - **Câu Đúng/Sai đơn (`true-false` thường):**
     Chuyển thành dạng 2 lựa chọn A/B:
     + `A. Đúng`
     + `B. Sai`
     + `Đáp án: ${q.correctAnswerIndex === 0 ? 'A' : 'B'}`
   - **Câu Đúng/Sai CV 7991 (`isCv7991TrueFalseItem(q)`):**
     Tách từng ý con a, b, c, d thành từng câu hỏi trắc nghiệm độc lập:
     + Câu `i.1`: `[Đề bài] - Mệnh đề a: [Nội dung a]` $\rightarrow$ A. Đúng / B. Sai $\rightarrow$ Đáp án theo `sub.isCorrect`.
     + Tương tự cho các ý b, c, d. Giúp học sinh trả lời trọn vẹn từng ý trong trò chơi.
   - **Câu Nối cột (`matching`):**
     Xuất dạng từng cặp ghép:
     `<p>${itemA} - ${itemB}</p>`
     và đồng thời tạo thêm dạng câu hỏi trắc nghiệm nối ô để tương thích cả game Ghép cặp lẫn các game trắc nghiệm khác.
   - **Câu Trả lời ngắn / Điền khuyết (`short-answer`, `fill-blank`):**
     Tạo câu hỏi kèm đáp án đúng rõ ràng.

3. **Bảng đáp án tổng hợp ở cuối tài liệu:**
   Bổ sung khối:
   ```html
   <div class="answer-key">
       <p><b>BẢNG ĐÁP ÁN:</b></p>
       <p>${answerKeys.join('   ')}</p>
   </div>
   ```
   (Ví dụ: `1.A   2.C   3.B   ...`).

4. **Thêm nút bấm "🎮 Xuất Word cho Game" trên thanh công cụ Bước 2:**
   Tại thanh công cụ kết quả tạo đề (dòng ~16788–16802):
   ```html
   <button
       onClick={exportWordForGame}
       className="px-3.5 py-2 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-lg hover:shadow-md font-bold text-sm transition flex items-center gap-1.5 shadow-sm"
       title="Xuất file Word (.docx) cấu trúc chuẩn để upload vào Game Giáo Dục"
   >
       <i className="fas fa-gamepad"></i> Xuất Word cho Game
   </button>
   ```

---

### Bước 2: Đồng bộ sang `backupcode viettailieu/taobaitap.html` và `smartquiz.html`

- Bổ sung hàm `exportWordForGame()` và nút bấm tương ứng trong:
  + `backupcode viettailieu/taobaitap.html` (Bước 2).
  + `smartquiz.html` (Bước 2).

---

### Bước 3: Nâng cấp linh hoạt cho `GameQuizImporter` trong `js/game-quiz-importer.js` (nếu cần)

Kiểm tra và đảm bảo `GameQuizImporter.parseQuizQuestions` và `GameQuizImporter.parseMatchingPairs`:
- Nhận diện linh hoạt câu hỏi có 2 lựa chọn (A. Đúng / B. Sai) cũng như 4 lựa chọn (A, B, C, D).
- Xử lý tốt các khoảng trắng, thẻ xuống dòng, ký tự đặc biệt của LaTeX `\(...\)`.

---

### Bước 4: Viết bài kiểm thử tự động `tests/taobaitap-game-word-export-smoke.js`

Viết test Node.js:
1. Mô phỏng dữ liệu tạo đề gồm đủ các loại câu hỏi:
   - Multiple-choice (có công thức LaTeX).
   - True/False đơn.
   - True/False CV 7991 (4 ý con).
   - Matching.
   - Short answer / Fill blank.
2. Chạy logic sinh nội dung HTML của hàm `exportWordForGame`.
3. Giả lập giải nén văn bản (bằng text cleaner tương tự `mammoth.extractRawText`).
4. Truyền văn bản qua `GameQuizImporter.parseQuizQuestions` và `GameQuizImporter.parseMatchingPairs`:
   - Xác nhận: Số lượng câu hỏi trắc nghiệm parse được > 0 và khớp với dữ liệu đầu vào.
   - Xác nhận: Công thức LaTeX trong câu hỏi và lựa chọn được bảo tồn 100%.
   - Xác nhận: Đáp án đúng (`answer`) khớp chính xác với đáp án trong đề.
   - Xác nhận: Cặp ghép matching được bóc tách đúng vế trái và vế phải.
5. Chạy toàn bộ test suite đảm bảo 100% PASS:
   - `tests/taobaitap-game-word-export-smoke.js`
   - `tests/game-quiz-importer-smoke.js`
   - `tests/taobaitap-presentation-smoke.js`
   - `tests/taobaitap-plan-smoke.js`
   - `tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`
   - `tests/taobaitap-thitructuyen-bridge-smoke.js`

---

## 3. Danh sách File Cần Chỉnh Sửa

1. `taobaitap.html` (Thêm hàm `exportWordForGame`, thêm nút "Xuất Word cho Game")
2. `backupcode viettailieu/taobaitap.html` (Đồng bộ hàm và nút xuất)
3. `smartquiz.html` (Đồng bộ hàm và nút xuất)
4. `tests/taobaitap-game-word-export-smoke.js` (Tạo mới bài test kiểm thử tự động liên thông Word $\rightarrow$ Game)
