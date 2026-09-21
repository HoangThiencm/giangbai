# PLAN: Sửa Lỗi Chế Độ "Dạy Ngay" Trong taobaitap.html (Câu Đúng/Sai & Nhập Số)

## 1. Hiện Trạng & Phân Tích Nguyên Nhân Lỗi

Người dùng phản ánh 2 lỗi trong chế độ Trình chiếu ("DẠY NGAY" - `QuizPresentationMode`) của `taobaitap.html` (và tương ứng `smartquiz.html`):
1. **Đối với câu Đúng/Sai không có chức năng chọn**:
   - Khi vào câu hỏi Đúng/Sai chuẩn Công văn 7991 (gồm các ý a, b, c, d): giao diện chỉ hiển thị danh sách các thẻ `<div>` tĩnh ghi nội dung mệnh đề.
   - Hoàn toàn **không có nút bấm** để giáo viên hoặc học sinh chọn "Đúng" hoặc "Sai" cho từng ý.
   - Khi bấm hiện đáp án (hoặc phím cách/Enter), hệ thống ngay lập tức gắn nhãn cứng `[ĐÚNG]` hoặc `[SAI]` (như trong ảnh `media_1790002376960.png`), không ghi nhận được câu trả lời của người học và không chấm điểm.
2. **Nhập số (câu trả lời ngắn) thì không gửi được / báo Sai dù đáp án đúng (Ảnh `media_1790002459243.png`)**:
   - **Nguyên nhân 1 (Nút "Gửi" không phản hồi)**: Trong hàm `handleFillBlankSubmit()` (dòng ~14284 trong `taobaitap.html`):
     ```javascript
     const handleFillBlankSubmit = () => {
         if (showAns) return;
         const q = shuffledQuestions[idx] || safeQuestions[idx];
         if (!q) return;
         const target = String(q.correctAnswer || "").trim().toLowerCase();
         const isCorrect = fillBlankAnswer.trim().toLowerCase() === target;
         setSelectedOpt(isCorrect ? 0 : 1);
         if (isCorrect) {
             setScore(prev => prev + pointsPerQuestion);
         }
         // THIẾU: setShowAns(true);
     };
     ```
     Hàm `handleFillBlankSubmit()` tính điểm và gán `selectedOpt`, nhưng **quên không gọi `setShowAns(true)`**. Do đó khi người dùng click vào nút "Gửi", màn hình không hiển thị kết quả kiểm tra, người dùng thấy như nút "Gửi" bị liệt.
   - **Nguyên nhân 2 (Bấm Enter bị chấm "Sai! Đáp án đúng: -12")**:
     Trong `handleKeyDown()` (dòng ~14315 và 14341):
     ```javascript
     case "Enter": setShowAns(prev => !prev); break; // Dòng 14315: Bị bắt ngay tại đây!
     ...
     case "Enter": // Dòng 14341: Code chết, không bao giờ chạy tới!
         if (!showAns) {
             if (q && (q.type === "fill-blank" || q.type === "short-answer") && fillBlankAnswer.toString().trim()) {
                 handleFillBlankSubmit();
             }
         }
         break;
     ```
     Khi người dùng gõ `-12` vào input rồi nhấn phím `Enter`, nhánh `case "Enter"` đầu tiên kích hoạt `setShowAns(true)` ngay lập tức mà **không hề gọi `handleFillBlankSubmit()`**. Lúc này `selectedOpt` vẫn là `null`. Đoạn render kiểm tra `selectedOpt === 0 ? 'Đúng!' : 'Sai!'` $\rightarrow$ Vì `null === 0` là `false` nên giao diện hiển thị: `❌ Sai! Đáp án đúng: -12`.
   - **Nguyên nhân 3 (Xung đột phím tắt toàn cục với ô nhập liệu)**:
     Sự kiện `window.addEventListener("keydown", handleKeyDown)` không kiểm tra `e.target.tagName === 'INPUT'`. Khi người dùng gõ phím cách (Space), các số 1, 2, 3, 4 hoặc chữ d, s trong ô nhập liệu, các phím tắt toàn cục bị kích hoạt sai ngữ cảnh.

---

## 2. Giải Pháp Kỹ Thuật Chi Tiết Cho Coder

Áp dụng trên `taobaitap.html` (và đồng bộ sang `smartquiz.html`):

### Vấn đề 1: Thêm chức năng chọn Đúng / Sai cho từng ý CV7991
1. **Bổ sung state lưu câu trả lời Đúng/Sai**:
   - Thêm `const [cv7991Answers, setCv7991Answers] = useState({});` trong `QuizPresentationMode`.
   - Trong `useEffect` reset theo câu hỏi (`[idx, countdownTime]`): thêm `setCv7991Answers({});`.
2. **Hàm xử lý chọn**:
   ```javascript
   const handleCv7991Select = (subIdx, isTrue) => {
       if (showAns) return;
       setCv7991Answers(prev => ({ ...prev, [subIdx]: isTrue }));
   };
   ```
3. **Cập nhật giao diện hiển thị mệnh đề CV7991**:
   Thay thế khối render tại `q.type === "true-false" && isCv7991TrueFalseItem(q)`:
   - Với mỗi ý `item` (`sIdx`):
     - Bên trái: Ký tự (a, b, c, d) + Nội dung mệnh đề `<MathText text={item.text} />`.
     - Bên phải: Cặp nút chọn `[ Đúng ]` và `[ Sai ]`:
       - **Trước khi hiện đáp án (`!showAns`)**:
         - Nút "Đúng": nếu `cv7991Answers[sIdx] === true` thì nổi bật (nền xanh lá đậm `bg-emerald-600 text-white font-bold shadow`), ngược lại nền xám nhạt (`bg-gray-100 text-gray-700 hover:bg-emerald-50`).
         - Nút "Sai": nếu `cv7991Answers[sIdx] === false` thì nổi bật (nền đỏ `bg-rose-600 text-white font-bold shadow`), ngược lại nền xám nhạt (`bg-gray-100 text-gray-700 hover:bg-rose-50`).
       - **Sau khi hiện đáp án (`showAns`)**:
         - Đánh dấu rõ đáp án đúng của từng ý: Ý đúng có badge `[ĐÚNG]` viền xanh lá, ý sai có badge `[SAI]` viền đỏ.
         - Nếu người dùng đã chọn: hiển thị biểu tượng `✓` (nếu chọn đúng) hoặc `✗` (nếu chọn sai).
4. **Tính điểm chuẩn CV7991 khi hiện đáp án**:
   - Trong `useEffect` khi `showAns === true`:
     ```javascript
     if (q && q.type === "true-false" && isCv7991TrueFalseItem(q)) {
         const items = getCv7991TrueFalseItems(q).filter(it => it.text);
         if (items.length > 0 && Object.keys(cv7991Answers).length > 0) {
             const correctCount = items.filter((it, sIdx) => cv7991Answers[sIdx] === it.isCorrect).length;
             let scale = 0;
             if (correctCount === 1) scale = 0.1;
             else if (correctCount === 2) scale = 0.25;
             else if (correctCount === 3) scale = 0.5;
             else if (correctCount === 4) scale = 1.0;
             setScore(prev => prev + (pointsPerQuestion * scale));
         }
     }
     ```

---

### Vấn đề 2: Sửa chức năng nộp và so sánh câu trả lời ngắn (nhập số)
1. **Sửa hàm `handleFillBlankSubmit`**:
   - Thêm `setShowAns(true);` ngay khi chấm bài.
   - Nâng cấp so sánh đáp án số thông minh:
     ```javascript
     const handleFillBlankSubmit = () => {
         if (showAns) return;
         const q = shuffledQuestions[idx] || safeQuestions[idx];
         if (!q) return;
         
         const rawUser = String(fillBlankAnswer || "").trim();
         if (!rawUser) return;

         const rawTarget = String(q.correctAnswer || "").trim();
         
         // Làm sạch LaTeX $ và khoảng trắng
         const clean = (s) => s.replace(/^\$+|\$+$/g, "").replace(/^\\\(|\\\)$/g, "").trim();
         const cleanUser = clean(rawUser).replace(",", ".");
         const cleanTarget = clean(rawTarget).replace(",", ".");
         
         const numUser = parseFloat(cleanUser);
         const numTarget = parseFloat(cleanTarget);
         
         let isCorrect = false;
         if (!isNaN(numUser) && !isNaN(numTarget)) {
             isCorrect = Math.abs(numUser - numTarget) < 1e-6;
         } else {
             isCorrect = cleanUser.toLowerCase() === cleanTarget.toLowerCase();
         }

         setSelectedOpt(isCorrect ? 0 : 1);
         if (isCorrect) {
             setScore(prev => prev + pointsPerQuestion);
         }
         setShowAns(true);
     };
     ```
2. **Xử lý sự kiện bàn phím trên ô `<input>`**:
   - Bổ sung `onKeyDown` trên thẻ input:
     ```jsx
     <input
         type="text"
         value={fillBlankAnswer}
         onChange={(e) => setFillBlankAnswer(e.target.value)}
         onKeyDown={(e) => {
             if (e.key === "Enter") {
                 e.preventDefault();
                 e.stopPropagation();
                 handleFillBlankSubmit();
             }
         }}
         disabled={showAns}
         ...
     />
     ```
3. **Sửa `handleKeyDown` toàn cục**:
   - Ở đầu hàm `handleKeyDown`, chặn xử lý phím tắt nếu target là ô nhập liệu:
     ```javascript
     if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
         if (e.key === 'Enter') {
             e.preventDefault();
             handleFillBlankSubmit();
         }
         return;
     }
     ```
   - Xóa bỏ `case "Enter"` trùng lặp ở cuối hàm `handleKeyDown`.

---

## 3. Các Tệp Cần Chỉnh Sửa
- [taobaitap.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/taobaitap.html) (trong component `QuizPresentationMode`, dòng 14202 - 14520).
- [smartquiz.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/smartquiz.html) (trong component `QuizPresentationMode`, dòng 472 - 750).

---

## 4. Kế Hoạch Kiểm Thử (Verification Plan)
1. **Kiểm tra câu hỏi Đúng/Sai CV7991 trong "Dạy ngay"**:
   - Mở bài tập có câu hỏi Đúng/Sai CV7991 $\rightarrow$ Bấm "DẠY NGAY".
   - Kiểm tra mỗi ý con (a, b, c, d) có 2 nút "Đúng" và "Sai".
   - Click chọn các nút $\rightarrow$ Nút được chọn đổi màu rõ ràng.
   - Bấm "Hiện đáp án" $\rightarrow$ Hiển thị đáp án đúng/sai của từng ý, đánh dấu ý nào làm đúng (✓), ý nào làm sai (✗) và cộng điểm chính xác.
2. **Kiểm tra câu hỏi Trả lời ngắn / Điền khuyết (Nhập số)**:
   - Mở câu hỏi tính giá trị đơn thức (ví dụ đáp án `-12`).
   - Nhập `-12` rồi bấm nút **"Gửi"** $\rightarrow$ Hệ thống lập tức hiển thị kết quả "Đúng!" màu xanh lá, cộng điểm.
   - Thử nghiệm gõ `-12` rồi nhấn phím **Enter** ngay trong ô nhập liệu $\rightarrow$ Không bị lỗi sai, tự động nộp bài và chấm đúng.
   - Thử nghiệm nhập số thập phân dạng dấu phẩy (vd: `2,5` so với `2.5`) $\rightarrow$ Vẫn nhận diện đúng.
