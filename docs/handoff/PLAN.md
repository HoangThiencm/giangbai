# PLAN: Sửa Lỗi Nạp File Word Cho Game Giáo Dục (trochoi.html) & Lỗi Chưa Nạp Thư Viện GameQuizImporter

## 1. Hiện Trạng & Phân Tích Nguyên Nhân

Người dùng phản ánh 2 vấn đề khi liên thông từ `taobaitap.html` sang `trochoi.html`:
1. **Báo lỗi popup khi bấm xem trước:**
   > *"Lỗi nạp câu hỏi: Chưa nạp thư viện GameQuizImporter."* (Ảnh `media_1790002788886.png`)
2. **Xuất từ taobaitap không nhận, phải mở Word chọn toàn bộ sang Times New Roman rồi lưu mới nhận.**

---

### Phân tích kỹ thuật chi tiết:

#### Nguyên nhân 1: Tệp `js/game-quiz-importer.js` trên hosting đang bị rỗng (0 bytes)
- Kiểm tra trực tiếp trên máy chủ live `https://www.hoangthiencm.id.vn/js/game-quiz-importer.js`: phản hồi `Status: 200`, nhưng **kích thước file là 0 bytes**!
- Trong file `trochoi.html`, thẻ `<script src="js/game-quiz-importer.js?v=20260910"></script>` tải file 0 bytes $\rightarrow$ không thực thi bất kỳ mã nào $\rightarrow$ `window.GameQuizImporter` là `undefined`.
- Trong `trochoi.compiled.js` (dòng 703):
  ```javascript
  const importer = window.GameQuizImporter;
  if (!importer) throw new Error('Chưa nạp thư viện GameQuizImporter.');
  ```
  Khi người dùng click nút **"Xử lý câu hỏi & Chuyển sang xem trước"**, code kiểm tra `!importer` và văng ra đúng lỗi trong ảnh.
- **Nguyên nhân sâu xa:** Script build deploy CI `.github/workflows/ftp-deploy.yml` chạy `node tools/build-obfuscate.js --in-place`. Trong `tools/build-obfuscate.js`, file `trochoi.compiled.js` nằm trong `SKIP_FILE_NAMES`, nhưng `js/game-quiz-importer.js` KHÔNG nằm trong danh sách bỏ qua, dẫn đến quá trình obfuscate hoặc FTP sync gặp lỗi làm file bị ghi đè thành 0 bytes.

#### Nguyên nhân 2: File Word xuất từ nút "LaTeX" / "100% TN" dùng bảng `options-table` và dấu sao `*` đánh dấu đáp án
- Trong ảnh, tên chủ đề là `De_Thi_Tong_Hop_LaTeX` $\rightarrow$ Người dùng đã bấm nút **LaTeX** (`exportWordLatex`) thay vì nút **Xuất Word cho Game**.
- File `De_Thi_Tong_Hop_LaTeX.docx` và `De_Thi_100_Trac_Nghiem.docx` dùng bảng HTML 2 cột `<table class="options-table">` và đánh dấu đáp án đúng bằng dấu sao `*` sau phương án (như trong ảnh: `C. 0*`).
- Khi thư viện `mammoth.js` đọc bảng từ file docx do thư viện `html-docx-js` tạo ra, cấu trúc bảng HTML bị dính cột. Khi người dùng mở file trong Word rồi chọn font Times New Roman và Ctrl+S lưu lại, Word chuyển đổi tài liệu sang chuẩn OpenXML của Microsoft nên Mammoth mới trích xuất được từng dòng vào ô textarea.
- Tuy nhiên, bộ parser `GameQuizImporter.parseQuizQuestions` hiện tại **chưa nhận diện dấu `*` ở cuối phương án** để xác định đáp án đúng (nó chỉ tìm `Đáp án: A` hoặc bảng đáp án ở cuối).

---

## 2. Giải Pháp Toàn Diện Cho Coder

### Bước 1: Nhúng dự phòng (Fallback / Inline) `GameQuizImporter` vào `trochoi.compiled.js` hoặc `trochoi.html`
- Để đảm bảo `trochoi.html` hoạt động bền bỉ 100%, không bao giờ bị lỗi `Chưa nạp thư viện GameQuizImporter` kể cả khi file ngoài hosting gặp sự cố mạng/sync:
  1. Trong `trochoi.compiled.js`: Nếu `!window.GameQuizImporter`, tự động sử dụng bộ parser dự phòng tích hợp sẵn (hoặc nhúng trực tiếp object `GameQuizImporter` vào đầu file `trochoi.compiled.js`).
  2. Cập nhật `tools/build-obfuscate.js`: Thêm `game-quiz-importer.js` vào `SKIP_FILE_NAMES` để tránh bị CI làm rỗng file khi deploy.
  3. Đảm bảo `js/game-quiz-importer.js` được gán vào `window.GameQuizImporter` một cách an toàn:
     ```javascript
     if (typeof window !== 'undefined') {
         window.GameQuizImporter = GameQuizImporter;
     }
     ```

### Bước 2: Nâng cấp `GameQuizImporter.parseQuizQuestions` nhận diện đáp án có dấu sao `*`
- Trong `js/game-quiz-importer.js` (và bản nhúng dự phòng):
  Khi phân tích các lựa chọn A, B, C, D:
  ```javascript
  let asteriskAnswer = '';
  for (let j = 0; j < optionMatches.length; j++) {
      const optCur = optionMatches[j];
      const optNext = optionMatches[j + 1];
      const optEnd = optNext ? optNext.markerStart : block.length;
      let optText = block.slice(optCur.bodyStart, optEnd).trim();

      // Nhận diện phương án có dấu sao (*) đánh dấu đáp án đúng: vd "0*", "Phương án C*"
      if (/\*$/.test(optText) || /\(\*\)$/.test(optText)) {
          asteriskAnswer = optCur.letter;
          optText = optText.replace(/\s*\(\*\)$|\s*\*$/, '').trim();
      }
      optionsByLetter[optCur.letter] = optText;
  }

  // Ưu tiên: Dấu sao (*) trong phương án -> Bảng đáp án cuối bài -> Dòng "Đáp án: X" -> Phương án A
  const finalAnswerLetter = asteriskAnswer || inlineAnswer || answerTable[cur.number] || (optionMatches[0]?.letter || 'A');
  ```
  Nhờ đó, bất kể file Word xuất từ **Xuất Word cho Game**, **LaTeX**, hay **Xuất 100% TN** thì `trochoi.html` đều bóc tách đúng 100% câu hỏi và đáp án đúng!

### Bước 3: Tối ưu cấu trúc Word xuất từ `taobaitap.html`
- Đảm bảo nút **"🎮 Xuất Word cho Game"** (`De_Thi_Game_Giao_Duc.docx`) xuất theo từng đoạn `<p>` rõ ràng, không dùng bảng `<table>`, giữ nguyên công thức LaTeX `\(...\)` hoặc `$...$`.
- Thêm gợi ý/chú thích nhỏ cạnh các nút xuất trong `taobaitap.html`:
  * Nút "🎮 Xuất Word cho Game": Ghi rõ *"Dùng riêng để nạp vào Game Giáo Dục (trochoi.html) mà không cần chỉnh sửa"*.

---

## 3. Các Tệp Cần Chỉnh Sửa
1. `js/game-quiz-importer.js`: Bổ sung nhận diện đáp án có dấu `*`, gán `window.GameQuizImporter` rõ ràng.
2. `trochoi.compiled.js`: Tích hợp dự phòng `GameQuizImporter` (để nếu file ngoài bị thiếu thì vẫn chạy mượt mà, không bao giờ văng lỗi "Chưa nạp thư viện").
3. `tools/build-obfuscate.js`: Thêm `game-quiz-importer.js` vào `SKIP_FILE_NAMES`.
4. `taobaitap.html`: Đảm bảo các định dạng xuất Word đều tương thích tốt với bộ đọc của Game.

---

## 4. Kế Hoạch Kiểm Thử (Verification Plan)
1. **Kiểm tra nạp thư viện `GameQuizImporter`**:
   - Mở `trochoi.html` trên trình duyệt $\rightarrow$ Kiểm tra `window.GameQuizImporter` luôn tồn tại và có đầy đủ các hàm (`parseQuizQuestions`, `parseMatchingPairs`, `extractTextFromFile`).
2. **Kiểm tra bóc tách file Word có dấu sao `*`**:
   - Dán hoặc upload nội dung như trong ảnh:
     ```text
     Câu 3: Bậc của đơn thức là:
     A. 1
     B. 3
     C. 0*
     D. Không có bậc
     ```
   - Bấm "Xử lý câu hỏi & Chuyển sang xem trước":
     - Không còn báo lỗi "Chưa nạp thư viện".
     - Chuyển sang màn hình xem trước thành công.
     - Nhận diện đúng đáp án là **C**, nội dung phương án C là `0` (đã bỏ dấu `*`).
3. **Kiểm tra xuất file từ `taobaitap.html` nạp thẳng vào `trochoi.html`**:
   - Tạo bài tập trắc nghiệm Toán có công thức LaTeX.
   - Bấm "Xuất Word cho Game" $\rightarrow$ Tải file `De_Thi_Game_Giao_Duc.docx`.
   - Kéo thả trực tiếp file này vào `trochoi.html` $\rightarrow$ Nhận diện đủ 100% câu hỏi và công thức toán học mà KHÔNG cần mở Word đổi font Times New Roman.
