# PLAN: Khắc phục lỗi cột Ghi chú chưa cập nhật biểu hiện NLS & AI và Báo cáo thẩm định Chưa đạt (0 tiết)

## Hiện trạng & Kết quả điều tra chi tiết

Người dùng đã tích chọn đúng số tiết NLS và AI ở Mục 5, nhưng:
1. **Trong cột Ghi chú (Phụ lục 1 và Phụ lục 3)**: Hoàn toàn không hiển thị biểu hiện NLS và AI (chỉ hiển thị dấu gạch ngang `'-'`).
2. **Trong Báo cáo thẩm định**:
   - Năng lực số: `0/140 tiết (0/89 bài), mục tiêu 28 tiết` -> **Chưa đạt**
   - Trí tuệ nhân tạo: `0/12 tiết AI đã chọn có mã và phạm vi` -> **Chưa đạt**

---

## Ba nguyên nhân gốc rễ (Root Causes)

### 1. Nguyên nhân 1 (Gây mất trắng dữ liệu cột Ghi chú thành `'-'`): Sai lệch chỉ số cột trong hàm bọc `appendixOneTable` và `appendixThreeTable`
- Tại cuối file (`xaydungphuluc.html` dòng 1688–1689, `canvas_xaydungphuluc.html` dòng 1762–1763):
  ```javascript
  appendixOneTable = function(generated, c) {
    const table = legacyAppendixOneTableForNote(generated, c),
          nls = table.columns.findIndex(isNlsColumn),
          ai = table.columns.findIndex(isAiColumn);
    return {
      ...table,
      columns: APPENDIX_1_COLUMNS.map(([, label]) => label),
      rows: table.rows.map(row => row.isHeader ? row : {
        ...row,
        cells: [...row.cells.slice(0, 4), formatNoteIntegration(row.cells[nls], row.cells[ai], row.cells[1])]
      })
    };
  };
  ```
- **Lý do**: Khi gộp sang 5 cột (`APPENDIX_1_COLUMNS`), bảng trả về từ `legacyAppendixOneTableForNote` đã có cột là `['STT', 'Bài học', 'Số tiết', 'Yêu cầu cần đạt', 'Ghi chú']`. Các cột không còn nhãn `Biểu hiện năng lực số` hay `Biểu hiện năng lực AI`.
- Do đó `table.columns.findIndex(isNlsColumn)` và `findIndex(isAiColumn)` luôn trả về `-1`.
- Trong JS, `row.cells[-1]` là `undefined`.
- Hàm `formatNoteIntegration(undefined, undefined, ...)` trả về giá trị mặc định là `'-'`.
- Toàn bộ nội dung `nlsText` (ở `row.cells[4]`) và `aiText` (ở `row.cells[5]`) được tính toán chuẩn xác từ `separateIntegration` bị bỏ rơi hoàn toàn, thay thế bằng `'-'`.
- Tương tự với Phụ lục 3: `legacyAppendixThreeTableForNote` trả về `nlsText` ở `cells[6]` và `aiText` ở `cells[7]`, nhưng `findIndex()` cũng trả về `-1`, khiến ô Ghi chú của PL3 cũng bị biến thành `'-'`.

### 2. Nguyên nhân 2: Các hàm tick chọn NLS/AI ở Mục 5 chưa kích hoạt cập nhật lại bảng xem trước
- Tại các hàm sự kiện tick chọn:
  - `toggleNlsLesson(lessonId, checked)` (dòng 1341)
  - `toggleAiLesson(id, checked)` (dòng 1474)
  - `toggleAiLessonRow(lessonId, checked)` (dòng 1475)
- Các hàm này chỉ gọi `syncNlsRateFromSelection()` và `updateAiPicker()`, **hoàn toàn không gọi `schedulePreviewUpdate()`** (hoặc `refreshPpctDependents()`).
- Khi người dùng tick chọn các ô checkbox NLS hoặc AI trong bảng Mục 5, bảng xem trước Phụ lục 1 / Phụ lục 3 ở Mục 8 và Báo cáo thẩm định không được thông báo để tính toán và vẽ lại theo các tiết vừa chọn.

### 3. Nguyên nhân 3: `integrationParts(value)` không nhận diện định dạng khối `- Năng lực AI:`
- Tại dòng 1544:
  ```javascript
  function integrationParts(value) {
    const raw = integrationText(value);
    if (!raw || raw === '-') return [];
    const parts = /^\s*\d+\.[A-Z]/i.test(raw) ? [raw] : raw.split(/(?=\[\s*(?:AI\s*:|NLS\s*:|\d+\.[A-Z]))/i).filter(Boolean);
    return parts.map(text => ({ text: integrationText(text), ai: /^\s*(?:\[\s*AI\s*:|\d+\.[A-Z])/i.test(text) }));
  }
  ```
- Định dạng mới trong ô Ghi chú là:
  ```text
  - Năng lực số: 1.1.TC1a : ...
  - Năng lực AI: 6.B2.1 : ... (Áp dụng: tiết 1, 2)
  ```
  hoặc danh sách gạch đầu dòng ` + `.
- Regex cũ chỉ tìm `[` ngoặc vuông hoặc chuỗi bắt đầu bằng `\d+\.[A-Z]`, nên không nhận diện được `- Năng lực AI:` và gán `ai: false`.
- Dẫn đến `appendixAiCoverage` bóc tách danh sách tiết AI bị rỗng `[]`, khiến số tiết AI thẩm định luôn bằng `0/12`.

---

## Phạm vi file sửa đổi

1. **`xaydungphuluc.html`**
2. **`canvas_xaydungphuluc.html`**
3. **`backupcode viettailieu/canvas_xaydungphuluc.html`**
4. **`tests/xaydungphuluc-smoke.js`**
5. **`tests/canvas-xaydungphuluc-smoke.js`**

---

## Các bước triển khai chi tiết cho Coder

### Bước 1: Sửa hàm `appendixOneTable` và `appendixThreeTable` (Bảo đảm lấy đúng NLS & AI)
Tại cuối mỗi file HTML (đoạn bọc `appendixOneTable` và `appendixThreeTable`):
1. **Với Phụ lục 1 (`appendixOneTable`)**:
   ```javascript
   appendixOneTable = function(generated, c) {
     const table = legacyAppendixOneTableForNote(generated, c);
     const nlsIdx = table.columns.findIndex(isNlsColumn);
     const aiIdx = table.columns.findIndex(isAiColumn);
     // Fallback sang vị trí mặc định của legacy table nếu cột đã bị đổi thành Ghi chú: nls=4, ai=5
     const nlsCol = nlsIdx >= 0 ? nlsIdx : 4;
     const aiCol = aiIdx >= 0 ? aiIdx : 5;
     return {
       ...table,
       columns: APPENDIX_1_COLUMNS.map(([, label]) => label),
       rows: table.rows.map(row => {
         if (row.isHeader) return row;
         const nlsText = row.cells[nlsCol];
         const aiText = row.cells[aiCol];
         const note = formatNoteIntegration(nlsText, aiText, row.cells[1]);
         return {
           ...row,
           cells: [...row.cells.slice(0, 4), note]
         };
       })
     };
   };
   ```
2. **Với Phụ lục 3 (`appendixThreeTable`)**:
   ```javascript
   appendixThreeTable = function(rows, c) {
     const table = legacyAppendixThreeTableForNote(rows, c);
     const nlsIdx = table.columns.findIndex(isNlsColumn);
     const aiIdx = table.columns.findIndex(isAiColumn);
     // Fallback sang vị trí mặc định của legacy table nếu cột đã bị đổi thành Ghi chú: nls=6, ai=7
     const nlsCol = nlsIdx >= 0 ? nlsIdx : 6;
     const aiCol = aiIdx >= 0 ? aiIdx : 7;
     return {
       ...table,
       columns: APPENDIX_3_COLUMNS.map(([, label]) => label),
       rows: table.rows.map(row => {
         if (row.isHeader) return row;
         const nlsText = row.cells[nlsCol];
         const aiText = row.cells[aiCol];
         const note = formatNoteIntegration(nlsText, aiText, row.cells[0]);
         return {
           ...row,
           cells: [...row.cells.slice(0, 6), note]
         };
       })
     };
   };
   ```

### Bước 2: Thêm `schedulePreviewUpdate()` vào các sự kiện tick chọn Mục 5
Trong các hàm:
1. `toggleNlsLesson`:
   ```javascript
   function toggleNlsLesson(lessonId, checked) {
     if (checked && isSinglePeriodLesson(lessonId)) toggleAiLessonRow(lessonId, false);
     if (checked) nlsSelectedLessonIds.add(lessonId); else nlsSelectedLessonIds.delete(lessonId);
     syncNlsRateFromSelection();
     updateAiPicker();
     schedulePreviewUpdate();
   }
   ```
2. `toggleAiLesson`:
   ```javascript
   function toggleAiLesson(id, checked) {
     const selected = selectedAiPeriodIds(), period = aiPeriodCandidates().find(item => item.id === id);
     if (checked && period && isSinglePeriodLesson(period.lessonId)) nlsSelectedLessonIds.delete(period.lessonId);
     if (checked) selected.add(id); else selected.delete(id);
     syncNlsRateFromSelection();
     updateAiPicker();
     schedulePreviewUpdate();
   }
   ```
3. `toggleAiLessonRow`:
   ```javascript
   function toggleAiLessonRow(lessonId, checked) {
     const periods = aiPeriodCandidates().filter(x => x.lessonId === lessonId), selected = selectedAiPeriodIds();
     if (checked && isSinglePeriodLesson(lessonId)) nlsSelectedLessonIds.delete(lessonId);
     if (checked) periods.forEach(period => selected.add(period.id)); else periods.forEach(period => selected.delete(period.id));
     syncNlsRateFromSelection();
     updateAiPicker();
     schedulePreviewUpdate();
   }
   ```

### Bước 3: Nâng cấp `integrationParts(value)` để phân tách chuẩn xác khối NLS và AI trong Ghi chú
Cập nhật hàm `integrationParts`:
```javascript
function integrationParts(value) {
  const raw = integrationText(value);
  if (!raw || raw === '-') return [];
  // Phân tách định dạng Ghi chú mới: - Năng lực số / - Năng lực AI
  if (/-\s*Năng lực\s*(?:số|AI)/i.test(raw)) {
    const blocks = raw.split(/(?=-\s*Năng lực\s*(?:số|AI))/i);
    const results = [];
    for (const block of blocks) {
      const b = block.trim();
      if (!b) continue;
      const isAi = /^-\s*Năng lực\s*AI/i.test(b);
      const lines = b.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
      const subItems = lines.slice(1).filter(l => l.startsWith('+'));
      if (subItems.length) {
        for (const sub of subItems) {
          results.push({ text: sub, ai: isAi });
        }
      } else {
        results.push({ text: b, ai: isAi });
      }
    }
    return results;
  }
  // Định dạng ngoặc vuông legacy: [NLS: ...] [AI: ...]
  const parts = /^\s*\d+\.[A-Z]/i.test(raw) ? [raw] : raw.split(/(?=\[\s*(?:AI\s*:|NLS\s*:|\d+\.[A-Z]))/i).filter(Boolean);
  return parts.map(text => ({ text: integrationText(text), ai: /^\s*(?:\[\s*AI\s*:|\d+\.[A-Z])/i.test(text) }));
}
```

### Bước 4: Đồng bộ 1:1 trên cả 3 file mã nguồn
Cập nhật đầy đủ, đồng nhất trên:
- `xaydungphuluc.html`
- `canvas_xaydungphuluc.html`
- `backupcode viettailieu/canvas_xaydungphuluc.html`

### Bước 5: Cập nhật kiểm thử tự động
Trong `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`:
1. Kiểm tra khi gọi `appendixOneTable(...)`: ô `cells[4]` phải chứa chuỗi định dạng `- Năng lực số:` hoặc mã NLS, và `- Năng lực AI:` hoặc mã AI (tuyệt đối không được bằng `'-'`).
2. Kiểm tra `toggleAiLesson` / `toggleNlsLesson`: kích hoạt `schedulePreviewUpdate` và cập nhật lại bảng xem trước.
3. Kiểm tra `appendixAiCoverage` và `calculateComplianceReport`: tính toán đúng số tiết AI và NLS từ cột Ghi chú, đạt `pass === true`.

---

## Tiêu chí nghiệm thu (Acceptance Criteria)
1. Trong bảng xem trước Phụ lục 1 (Mục 8) và Phụ lục 3: Cột `Ghi chú` hiển thị đầy đủ biểu hiện NLS và biểu hiện AI theo đúng quy chuẩn 1 mã hoặc nhiều mã `+`.
2. Khi tick chọn / bỏ chọn ở Mục 5: Bảng xem trước và thẻ thẩm định cập nhật tức thì.
3. Báo cáo thẩm định:
   - Năng lực số: Đạt đủ số tiết theo mục tiêu (ví dụ `28/140 tiết`, Đạt).
   - Trí tuệ nhân tạo: Đạt đủ số tiết AI đã chọn (ví dụ `12/12 tiết`, Đạt).
   - Đạt chuẩn 100% CV 5512 & CTGDPT 2018.
4. Xuất Word (.docx): Cột `Ghi chú` chứa đủ nội dung, phân màu đúng chuẩn (AI tím, NLS xanh).
5. Tất cả smoke tests đều PASS.
