# PLAN: Khắc phục lỗi TypeError: undefined is not iterable trong QuizPresentationMode (taobaitap.html)

## 1. Hiện trạng & Phân tích nguyên nhân gốc rễ (Root Cause)

### Hiện trạng
Khi người dùng bấm **Trình chiếu** (hoặc Dạy ngay) trong `taobaitap.html`:
Trình duyệt báo lỗi màn hình đỏ / console:
```text
[06:25:39 PM] [GLOBAL] TypeError: undefined is not iterable (cannot read property Symbol(Symbol.iterator))
at _iterableToArray (<anonymous>:5:77)
    at _toConsumableArray (<anonymous>:3:66)
    at <anonymous>:1385:21
    at Array.map (<anonymous>)
    at <anonymous>:1383:30
    at commitHookEffectListMount (https://unpkg.com/react-dom@18/umd/react-dom.development.js:23199:28)
...
The above error occurred in the <QuizPresentationMode> component:
    at QuizPresentationMode (<anonymous>:1321:25)
    at App (<anonymous>:2443:21)
```

### Phân tích Root Cause

1. **Truy cập spread `[...q.options]` khi `q.options` là `undefined`:**
   - Tại dòng 14216–14229 của `taobaitap.html`:
     ```javascript
     useEffect(() => {
         document.body.style.overflow = 'hidden';
         const shuffled = questions.map(q => {
             if (!settings.shuffleOptions) return q;
             const options = [...q.options];
             const correctAnswer = options[q.correctAnswerIndex];
             const shuffledIndices = options.map((_, i) => i).sort(() => Math.random() - 0.5);
             const newOptions = shuffledIndices.map(i => options[i]);
             const newCorrectIndex = newOptions.indexOf(correctAnswer);
             return { ...q, options: newOptions, correctAnswerIndex: newCorrectIndex };
         });
         setShuffledQuestions(shuffled);
         return () => { document.body.style.overflow = 'auto'; };
     }, [questions, settings.shuffleOptions]);
     ```
   - Khi tùy chọn **Tráo đáp án** (`settings.shuffleOptions`) được bật:
     Khi người dùng tạo đề tổng hợp hoặc bài tập có nhiều dạng câu hỏi:
     + Dạng **Trả lời ngắn** (`short-answer`) hoặc **Điền khuyết** (`fill-blank`): câu hỏi chỉ có `question` và `correctAnswer`, **hoàn toàn không có thuộc tính `options`** (`q.options === undefined`).
     + Dạng **Nối cột** (`matching`): câu hỏi chỉ có `columnA`, `columnB`, `correctMatches`, **không có thuộc tính `options`**.
     + Dạng câu tự luận hoặc câu hỏi từ AI/import chưa có mảng `options`.
   - Trình biên dịch Babel biến đổi cú pháp spread `[...q.options]` thành `_toConsumableArray(q.options)` $\rightarrow$ gọi `_iterableToArray(q.options)`.
   - Khi `q.options` là `undefined`, trình duyệt quăng ngay ngoại lệ:
     `TypeError: undefined is not iterable (cannot read property Symbol(Symbol.iterator))`.
   - Do hàm này nằm trong `useEffect` đầu tiên của `QuizPresentationMode`, ngoại lệ xảy ra trong giai đoạn `commitHookEffectListMount` làm toàn bộ component bị sụp đổ (crash).

2. **Lỗi logic nghiêm trọng khi tráo đáp án các dạng câu hỏi đặc thù:**
   - **Câu Đúng/Sai đơn (`true-false` thường):** Có `options = ['Đúng', 'Sai']`. Nếu bị tráo ngẫu nhiên, vị trí `0` và `1` bị đảo lộn. Nhưng các phím tắt `D` (`handleOptionSelect(0)`), `S` (`handleOptionSelect(1)`) và giao diện hiển thị (`opt === 'Đúng' ? check : times`) mặc định cố định `0` là Đúng, `1` là Sai. Việc tráo sẽ làm sai lệch hoàn toàn kết quả chấm điểm.
   - **Câu Đúng/Sai Công văn 7991 (`isCv7991TrueFalseItem(q)`):** Có 4 ý con a, b, c, d với mảng đáp án `correct_answers` và `subItems`. Nếu tráo `q.options` đơn thuần mà không tráo tương ứng `correct_answers`, đề thi sẽ bị sai lệch toàn bộ đáp án.
   - **Do đó: Chỉ duy nhất câu trắc nghiệm 4 lựa chọn (`multiple-choice`) mới được phép tráo đáp án!**

3. **Thiếu guard phòng vệ (Defensive Guards) trong `QuizPresentationMode`:**
   - `settings` có thể bị `undefined` nếu không truyền đúng, dẫn đến crash khi truy cập `settings.countdownTime` hay `settings.pointsPerQuestion`.
   - `questions` rỗng hoặc phần tử hiện tại `q` bị undefined chưa có fallback UI an toàn.
   - Các lệnh `.map()` hiển thị options `q.options.map` chưa có fallback `(q.options || [])`.

4. **Các file cùng chứa mã nguồn này:**
   - `taobaitap.html` (dòng 14202–14643)
   - `backupcode viettailieu/taobaitap.html` (dòng 13912–14350)
   - `smartquiz.html` (dòng 471–910)

---

## 2. Kế hoạch Triển khai Chi tiết cho Coder

### Bước 1: Sửa chữa và bọc guard an toàn cho `QuizPresentationMode` trong `taobaitap.html`

Vị trí: Dòng ~14202 đến ~14643 trong `taobaitap.html`.

1. **Khởi tạo và bọc fallback cho `settings`:**
   ```javascript
   const safeSettings = settings || {};
   const countdownTime = Number(safeSettings.countdownTime) || 0;
   const pointsPerQuestion = Number(safeSettings.pointsPerQuestion) > 0 ? Number(safeSettings.pointsPerQuestion) : 1;
   const autoNext = !!safeSettings.autoNext;
   const shuffleOptions = !!safeSettings.shuffleOptions;
   const safeQuestions = Array.isArray(questions) ? questions : [];
   ```

2. **Sửa `useEffect` tráo đáp án — CHỈ tráo cho `multiple-choice` hợp lệ:**
   ```javascript
   useEffect(() => {
       document.body.style.overflow = 'hidden';
       const shuffled = safeQuestions.map(q => {
           if (!q) return q;
           // CHỈ tráo đáp án cho câu hỏi multiple-choice có mảng options hợp lệ
           if (!shuffleOptions || q.type !== 'multiple-choice' || !Array.isArray(q.options) || q.options.length < 2) {
               return q;
           }
           const options = [...q.options];
           const validIdx = (Number.isInteger(q.correctAnswerIndex) && q.correctAnswerIndex >= 0 && q.correctAnswerIndex < options.length)
               ? q.correctAnswerIndex
               : 0;
           const correctAnswer = options[validIdx];
           const shuffledIndices = options.map((_, i) => i).sort(() => Math.random() - 0.5);
           const newOptions = shuffledIndices.map(i => options[i]);
           const newCorrectIndex = newOptions.indexOf(correctAnswer);
           return { ...q, options: newOptions, correctAnswerIndex: newCorrectIndex >= 0 ? newCorrectIndex : validIdx };
       });
       setShuffledQuestions(shuffled);
       return () => { document.body.style.overflow = 'auto'; };
   }, [questions, shuffleOptions]);
   ```

3. **Bọc guard an toàn cho các `useEffect` khác và bộ đếm giờ:**
   - Dùng `countdownTime`, `autoNext`, `pointsPerQuestion` thay cho truy cập trực tiếp `settings.*`.
   - Trong `handleFillBlankSubmit`: kiểm tra `const target = String(q.correctAnswer || "").trim().toLowerCase();`.
   - Trong `handleOptionSelect`: kiểm tra `if (!q) return;`.

4. **Bọc guard UI khi `q` không tồn tại:**
   Trước khi render giao diện câu hỏi:
   ```javascript
   const q = shuffledQuestions[idx] || safeQuestions[idx];
   if (!q) {
       return (
           <div className="fixed inset-0 bg-slate-900 text-white z-50 flex flex-col items-center justify-center p-6">
               <div className="bg-slate-800 p-8 rounded-2xl max-w-md w-full text-center">
                   <i className="fas fa-exclamation-triangle text-4xl text-yellow-400 mb-4"></i>
                   <h3 className="text-xl font-bold mb-2">Không tìm thấy câu hỏi</h3>
                   <p className="text-gray-400 mb-6">Danh sách câu hỏi trống hoặc câu hỏi hiện tại không hợp lệ.</p>
                   <button onClick={onExit} className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold transition">Quay lại</button>
               </div>
           </div>
       );
   }
   ```

5. **Bọc guard mảng khi render:**
   - Multiple choice: `{(Array.isArray(q.options) ? q.options : []).map((opt, i) => { ... })}`
   - True-false đơn: `{((Array.isArray(q.options) && q.options.length) ? q.options : ['Đúng', 'Sai']).map((opt, i) => { ... })}`
   - Matching Cột A: `{(Array.isArray(q.columnA) ? q.columnA : []).map((item, i) => { ... })}`
   - Matching Cột B: `{(Array.isArray(q.columnB) ? q.columnB : []).map((item, j) => { ... })}`
   - Matching Kết quả: `{(Array.isArray(q.correctMatches) ? q.correctMatches : []).map((matchIdx, i) => ( ... ))}`

---

### Bước 2: Đồng bộ sửa chữa cho `backupcode viettailieu/taobaitap.html` và `smartquiz.html`

- Áp dụng cùng logic an toàn cho `QuizPresentationMode` trong:
  + `backupcode viettailieu/taobaitap.html` (dòng ~13912)
  + `smartquiz.html` (dòng ~471)

---

### Bước 3: Viết bài kiểm thử tự động `tests/taobaitap-presentation-smoke.js`

Viết file test chạy bằng Node:
1. Trích xuất logic `shuffle` và render helper của `QuizPresentationMode` từ cả 3 file:
   `taobaitap.html`, `backupcode viettailieu/taobaitap.html`, `smartquiz.html`.
2. Chạy test với các bộ dữ liệu:
   - Dữ liệu câu hỏi hỗn hợp gồm: Multiple choice, True/False đơn, True/False CV7991 (4 ý con), Short answer (không có `options`), Fill blank (không có `options`), Matching (`columnA`/`columnB`, không có `options`), câu bị null/undefined.
   - Chạy với `shuffleOptions = true` và `shuffleOptions = false`.
   - Chạy với `settings = undefined`, `settings = {}`.
3. Kiểm tra khẳng định (`assert`):
   - Tuyệt đối không ném lỗi `TypeError: undefined is not iterable` hoặc `Cannot read property of undefined`.
   - Đáp án của câu `multiple-choice` tráo đúng nhưng đáp án đúng (`correctAnswerIndex`) vẫn tương ứng nội dung đáp án ban đầu.
   - Các câu `short-answer`, `fill-blank`, `matching`, `true-false` không bị lỗi hoặc xáo trộn sai cấu trúc.
4. Chạy lại toàn bộ test suite:
   - `tests/taobaitap-presentation-smoke.js`
   - `tests/taobaitap-plan-smoke.js`
   - `tests/taobaitap-thitructuyen-bridge-smoke.js`
   - `tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`
   Đảm bảo 100% PASS.

---

## 3. Danh sách File Cần Chỉnh Sửa

1. `taobaitap.html` (Sửa guard `QuizPresentationMode`, bảo vệ `q.options`, bọc fallback `safeSettings` và render safe arrays)
2. `backupcode viettailieu/taobaitap.html` (Đồng bộ sửa `QuizPresentationMode`)
3. `smartquiz.html` (Đồng bộ sửa `QuizPresentationMode`)
4. `tests/taobaitap-presentation-smoke.js` (File test mới kiểm thử tự động toàn diện chế độ trình chiếu)
