# PLAN: Sửa Lỗi CV 7991 (Câu 13 Đúng/Sai) Và Lỗi Hiển Thị PPDH Trên Canvas Soạn KHBD

## Hiện trạng

### Vấn đề 1: Đề CV 7991 Câu 13 (Tạo bài tập ↔ Thi trực tuyến)
1. **Kiểu câu và các ý Đúng/Sai**:
   - Khi xuất bằng mẫu chuẩn CV 7991, câu 13 đã nhận diện đúng kiểu câu **Đúng / Sai** (`type: "tf"`) và hiển thị đủ 4 ý **a, b, c, d** với đáp án Đ, Đ, Đ, S.
   - Tuy nhiên, nếu người dùng xuất bằng nút **LaTeX** (`exportWordLatex`) hoặc **Xuất Word** (`exportWord`) tại [taobaitap.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/taobaitap.html), hàm xử lý bị hardcode theo chuẩn cũ (dòng 16023-16030), chỉ lấy 2 ý đầu vào bảng `A.` và `B.`, vứt bỏ ý `c, d`.
2. **Lỗi dính câu chỉ dẫn Phần III vào ý d**:
   - Trong [thitructuyen.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/thitructuyen.html#L1530) hàm `parseLatexWordQuiz`:
     ```javascript
     block = block.replace(/\n\s*PHẦN\s+(?:I|II|III)\b[^\n]*/gi, '').trim();
     ```
   - Regex trên chỉ xóa 1 dòng tiêu đề `PHẦN III...`, bỏ sót đoạn hướng dẫn thí sinh ngay dưới:
     `"Thí sinh trả lời từ câu 14 đến câu 17. Thí sinh chỉ điền số kết quả vào ô trả lời. Mỗi câu đúng được 0.5 điểm."`
   - Vì nằm trước `Câu 14` nên câu hướng dẫn này bị gộp thẳng vào đuôi nội dung của ý **d)** câu 13.
3. **Tự động nhận diện Đúng/Sai khi file Word dùng nhãn A-D**:
   - `parseLatexWordQuiz` chưa kiểm tra bảng đáp án (`answerKey[item.number]`) và chưa kiểm tra cụm từ đặc trưng `"Xét tính đúng/sai"` để tự động ánh xạ nhãn A-D thành a-d nếu file Word bị format dạng trắc nghiệm.

### Vấn đề 2: Không hiển thị PPDH & Kỹ thuật dạy học tại Canvas Soạn KHBD ([canvas_soankhbd.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/canvas_soankhbd.html))
1. **Nguyên nhân chính**:
   - Tại [dòng 1132](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/canvas_soankhbd.html#L1132): Thẻ script tải danh mục phương pháp:
     `<script src="https://hoangthiencm.id.vn/js/khbd-pedagogy-catalog.js?v=20260916-canvas-module-v9"></script>`
   - File `https://hoangthiencm.id.vn/js/khbd-pedagogy-catalog.js` trên host hiện tại đang có kích thước **0 byte (rỗng)**!
   - Trong khi đó, các script khác (`khbd-prompts.js`, `khbd-docx.js`) đều có kiểm tra `isLocal ? "js/..." : "https://..."`, còn `khbd-pedagogy-catalog.js` bị hardcode link host và **hoàn toàn không có fallback nhúng**.
   - Hậu quả: `window.KHBD_PEDAGOGY_CATALOG` bị `undefined`.
2. **Biểu hiện trên giao diện**:
   - Khi hàm `renderPedagogyCatalogs()` ([js/khbd-app.js:1042](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/js/khbd-app.js#L1042)) chạy:
     ```javascript
     if (typeof KHBD_PEDAGOGY_CATALOG === "undefined") return;
     ```
   - Hàm lập tức return mà không render HTML cho 3 panel (`methodsCatalogPanel`, `techniquesCatalogPanel`, `activitiesCatalogPanel`).
   - Ba panel này bị kẹt vĩnh viễn ở trạng thái chờ:
     `⏳ Đang phân tích SGK & đề xuất...`
     `⏳ Đang phân tích SGK & đề xuất...`
     `⏳ Đang phân tích SGK & đề xuất...`

---

## Phạm vi
1. **`thitructuyen.html`**:
   - Xóa triệt để tiêu đề và hướng dẫn phần ở cuối block câu hỏi trước câu kế tiếp.
   - Nâng cấp `isTF` nhận diện đa tầng (qua bảng đáp án, regex câu hỏi, nhãn).
2. **`taobaitap.html` & `backupcode viettailieu/taobaitap.html`**:
   - Sửa `exportWordLatex` và `exportWord` hỗ trợ chuẩn 4 ý CV 7991 cho câu Đúng/Sai.
3. **`canvas_soankhbd.html`**:
   - Đổi dòng tải script [khbd-pedagogy-catalog.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/js/khbd-pedagogy-catalog.js) sang cơ chế `isLocal ? "js/khbd-pedagogy-catalog.js" : "https://hoangthiencm.id.vn/js/khbd-pedagogy-catalog.js"`.
   - Bổ sung fallback: Nếu sau khi nạp mà `typeof window.KHBD_PEDAGOGY_CATALOG === "undefined"`, tự động nạp từ đường dẫn tương đối `js/khbd-pedagogy-catalog.js`.
4. **Kiểm thử**:
   - Cập nhật các smoke test để xác nhận toàn bộ lỗi đã được vá.

---

## Ngoài phạm vi
- Không thay đổi logic chấm thi backend hay luồng tạo bài của học sinh.

---

## File dự kiến tác động
1. `thitructuyen.html`
2. `taobaitap.html`
3. `backupcode viettailieu/taobaitap.html`
4. `canvas_soankhbd.html`
5. `tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`

---

## Các bước thực hiện

### Bước 1: Sửa lỗi hiển thị PPDH trong `canvas_soankhbd.html`
- Tại [canvas_soankhbd.html:1132](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/canvas_soankhbd.html#L1132):
  Thay thẻ `<script src="https://hoangthiencm.id.vn/js/khbd-pedagogy-catalog.js..."></script>` thành:
  ```html
  <script>
    (function () {
      const isLocal = typeof window !== "undefined" && (window.location.protocol === "file:" || /^(localhost|127\.0\.0\.1)$/.test(window.location.hostname));
      document.write(`<script src="${isLocal ? "js/khbd-pedagogy-catalog.js" : "https://hoangthiencm.id.vn/js/khbd-pedagogy-catalog.js?v=20260916-canvas-module-v9"}"><\/script>`);
    })();
  </script>
  ```
- Bổ sung script fallback ngay sau đó: nếu `typeof window.KHBD_PEDAGOGY_CATALOG === "undefined"` thì nạp fallback `js/khbd-pedagogy-catalog.js`.

### Bước 2: Sửa lọc hướng dẫn phần và nhận diện Đúng/Sai trong `thitructuyen.html`
- Tại `parseLatexWordQuiz` ([thitructuyen.html:1530](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/thitructuyen.html#L1530)):
  Xóa sạch tiêu đề và hướng dẫn phần cuối block:
  ```javascript
  block = block.replace(/\n\s*(?:PHẦN\s+(?:I|II|III)\b|Thí sinh trả lời\b)[\s\S]*$/i, '').trim();
  ```
- Trong vòng lặp cắt từng ý `tfMatches`, tại ý cuối cùng loại bỏ mọi đoạn văn bắt đầu bằng `PHẦN...` hoặc `Thí sinh trả lời...` nếu còn sót lại.
- Nâng cấp `isTF`: Kết hợp `importedAnswerKeyTfList(answerKey[item.number])`, regex `"xét tính đúng/sai"`, và ánh xạ nhãn A-D sang a-d.

### Bước 3: Sửa `exportWordLatex` và `exportWord` trong `taobaitap.html`
- Nếu `synthForm === 'cv7991'` hoặc `dataToExport.some(isCv7991TrueFalseItem)`:
  - Khi xuất câu Đúng/Sai: Duyệt 4 ý từ `getCv7991TrueFalseItems(q)` và in `a)`, `b)`, `c)`, `d)`.
  - Không rút gọn thành bảng 2 cột A, B.

### Bước 4: Kiểm thử
- Chạy:
  ```powershell
  node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js
  node tests/taobaitap-plan-smoke.js
  node tests/smartquiz-smoke.js
  ```

---

## Rủi ro
- Khi cập nhật script trên `canvas_soankhbd.html`, đảm bảo không làm gián đoạn kết nối tới API Canvas Gemini host.
- Cần tải file `js/khbd-pedagogy-catalog.js` đầy đủ lên host `hoangthiencm.id.vn` khi deploy để người dùng trực tiếp trên web cũng được cập nhật.

---

## Cách kiểm thử
```powershell
node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js
node tests/taobaitap-plan-smoke.js
node tests/smartquiz-smoke.js
```

---

## Tiêu chí nghiệm thu
1. Trên `canvas_soankhbd.html`: Danh mục Phương pháp dạy học, Kĩ thuật dạy học 4 pha và Hoạt động đặc thù hiển thị đầy đủ, không bị kẹt ở `⏳ Đang phân tích SGK & đề xuất...`.
2. Trên `thitructuyen.html`: Câu 13 Đúng / Sai hiển thị sạch sẽ, ý d dừng lại đúng ở nội dung câu hỏi, không dính câu chỉ dẫn của Phần III.
3. Xuất Word LaTeX ở `taobaitap.html` bảo toàn đủ 4 ý a, b, c, d cho câu Đúng/Sai.
4. Toàn bộ smoke test pass 100%.
