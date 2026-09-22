# PLAN: AI Tự Động Thẩm Định Mức Độ Nhận Thức ([NB], [TH], [VD], [VDC]) Cho Từng Câu Hỏi

## 1. Yêu Cầu Đúng Bản Chất Của Người Dùng

- **Không chia tỉ lệ máy móc (index / total)**: Khi tạo đề (dù chọn "Hỗn hợp" hay bất kỳ mức độ nào), **chính AI là người hiểu sâu sắc bản chất câu hỏi** (nội dung, mức độ tư duy, độ phức tạp của bài toán) để tự thẩm định và gắn nhãn mức độ nhận thức phù hợp nhất cho từng câu:
  + **Nhận biết (`[NB]`)**: Câu hỏi kiểm tra định nghĩa, công thức, nhận diện kiến thức trực tiếp.
  + **Thông hiểu (`[TH]`)**: Câu hỏi yêu cầu hiểu bản chất, giải thích hiện tượng, biến đổi công thức 1 bước.
  + **Vận dụng (`[VD]`)**: Bài toán qua nhiều bước biến đổi, áp dụng kiến thức vào bài toán thực tế.
  + **Vận dụng cao (`[VDC]`)**: Bài toán phân hóa mạnh, tư duy tổng hợp, cực trị, tối ưu hóa.

- **Vì sao trước đây bị mất nhãn**:
  + Trong prompt yêu cầu AI sinh JSON (`generateContent`, `generateSynthesizedFromSource`, `handleFileUpload`), chúng ta **chưa đưa trường `"level"` vào cấu trúc JSON bắt buộc**.
  + Vì vậy, dù AI hiểu câu hỏi ở mức độ nào, AI cũng không có chỗ để điền, dẫn đến dữ liệu trả về bị thiếu trường `level`.
  + Khi xuất Word OLM, `getOlmLevelTag(q)` đọc `q.level` thấy rỗng nên không in thẻ, khiến OLM phải hỏi lại từng câu.

---

## 2. Giải Pháp Chi Tiết

### 1. Cập nhật tất cả các Prompt AI yêu cầu AI tự thẩm định `level`
Trong cả 3 luồng tạo/đọc câu hỏi:
- **`generateContent`** (Tạo câu hỏi từ danh sách chủ đề):
  + Yêu cầu AI: *"Dựa vào bản chất và độ sâu sư phạm của từng câu hỏi, bạn hãy tự đánh giá và gán chính xác mức độ nhận thức vào trường 'level': 'Nhận biết', 'Thông hiểu', 'Vận dụng', hoặc 'Vận dụng cao'."*
  + Schema mẫu:
    ```json
    {"question":"...","options":["A","B","C","D"],"correctAnswerIndex":0,"type":"multiple-choice","level":"Nhận biết"}
    ```
- **`generateSynthesizedFromSource`** (Tạo đề tổng hợp từ file tài liệu):
  + Yêu cầu AI quét học liệu và khi sinh câu hỏi nào thì tự gán `level` tương ứng cho câu đó.
- **`handleFileUpload`** (Trích xuất đề có sẵn từ file PDF/Word):
  + Yêu cầu AI phân tích nội dung từng câu hỏi trong đề gốc để tự động nhận diện mức độ nhận thức và ghi vào `level`.

### 2. Chuẩn hóa trong `normalizeQuizItems`
Đảm bảo thuộc tính `level` do AI trả về được lưu trữ và chuẩn hóa chính xác:
```javascript
const normalizeQuizItems = (items) => {
    if (!Array.isArray(items)) return [];

    return items.map((item, index) => {
        const rawLevel = String(item.level || '').toLowerCase().trim();
        let level = 'Nhận biết';
        if (rawLevel.includes('thông hiểu') || rawLevel === 'th') {
            level = 'Thông hiểu';
        } else if (rawLevel.includes('vận dụng cao') || rawLevel.includes('rất khó') || rawLevel === 'vdc') {
            level = 'Vận dụng cao';
        } else if (rawLevel.includes('vận dụng') || rawLevel.includes('nâng cao') || rawLevel.includes('khó') || rawLevel === 'vd') {
            level = 'Vận dụng';
        } else if (rawLevel.includes('nhận biết') || rawLevel.includes('cơ bản') || rawLevel.includes('dễ') || rawLevel === 'nb') {
            level = 'Nhận biết';
        } else {
            // Mặc định an toàn nếu AI quên trả về
            level = 'Nhận biết';
        }

        const normalized = {
            ...item,
            level,
            question: cleanGeneratedQuestionText(item.question)
        };
        // Các xử lý options, true-false, short-answer hiện tại giữ nguyên...
        return normalized;
    });
};
```

### 3. Hiển thị mức độ AI đã đánh giá trên giao diện Bước 2 (Step 2)
Trên từng thẻ câu hỏi ở Bước 2 (`questions.map((q, i) => ...)`):
- Hiển thị badge mức độ mà AI đã xác định (ví dụ: `🟢 [NB] Nhận biết`, `🔵 [TH] Thông hiểu`, `🟠 [VD] Vận dụng`, `🔴 [VDC] Vận dụng cao`).
- Dưới dạng thẻ chọn (dropdown) cho phép giáo viên nhìn thấy ngay kết quả phân loại của AI, đồng thời có thể bấm đổi mức độ nếu muốn trước khi xuất file:
  ```jsx
  <select
      value={q.level || "Nhận biết"}
      onChange={(e) => {
          const newLvl = e.target.value;
          setQuestions(prev => prev.map((item, idx) => idx === i ? { ...item, level: newLvl } : item));
      }}
      className="px-2.5 py-1 rounded-lg text-xs font-bold border border-slate-200 bg-white text-slate-700 hover:border-indigo-400 cursor-pointer shadow-sm focus:outline-none"
      title="Mức độ nhận thức do AI đánh giá (xuất chuẩn OLM.vn)"
  >
      <option value="Nhận biết">🟢 [NB] Nhận biết</option>
      <option value="Thông hiểu">🔵 [TH] Thông hiểu</option>
      <option value="Vận dụng">🟠 [VD] Vận dụng</option>
      <option value="Vận dụng cao">🔴 [VDC] Vận dụng cao</option>
  </select>
  ```

### 4. Xuất Word OLM (`exportWordOLM`)
Hàm `getOlmLevelTag(q)` đọc trực tiếp mức độ của câu hỏi:
```javascript
const getOlmLevelTag = (q) => {
    const raw = String(q?.level || "").toLowerCase().trim();
    if (raw.includes("thông hiểu") || raw === "th") return "[TH] ";
    if (raw.includes("vận dụng cao") || raw === "vdc") return "[VDC] ";
    if (raw.includes("vận dụng") || raw === "vd") return "[VD] ";
    return "[NB] ";
};
```
Khi xuất ra Word:
- Câu 1: `Câu 1. [NB] Để giải hệ phương trình bằng phương pháp thế, bước đầu tiên ta thường làm gì?`
- Câu 2: `Câu 2. [TH] Trong phương pháp cộng đại số, nếu hệ số của cùng một ẩn...`
- Câu 6: `Câu 6. [VD] Trong bài toán thực tế về số cây cải bắp...`
- Tất cả các câu hỏi đều có nhãn mức độ do AI đánh giá, khi import vào OLM sẽ được phân loại tự động 100%, không còn popup hỏi từng câu.

---

## 3. Kế Hoạch Kiểm Thử (Verification Plan)

1. **Test kiểm tra `taobaitap.html`**:
   - Xác nhận các prompt sinh câu hỏi và trích xuất đều có hướng dẫn AI thẩm định `"level"` và schema JSON chứa `"level"`.
   - Xác nhận `normalizeQuizItems` chuẩn hóa và giữ trường `level`.
   - Xác nhận `getOlmLevelTag` xuất đúng `[NB] `, `[TH] `, `[VD] `, `[VDC] ` cho từng câu hỏi.
   - Xác nhận giao diện Bước 2 hiển thị dropdown chọn mức độ nhận thức cho từng câu.
2. **Chạy test tự động**:
   - `node tests/taobaitap-olm-export-smoke.js`
   - `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js`
   - `node tests/taobaitap-game-word-export-smoke.js`
   - `git diff --check`
