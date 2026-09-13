# PLAN: Sửa hiển thị tiêu đề NLS/AI và hoàn thiện đầy đủ danh sách bài học, cột Ghi chú cho Phụ lục 3

## Hiện trạng & Nguyên nhân gốc rễ

### 1. Mất tiêu đề "Năng lực số" và "Năng lực AI" khi có từ 2 mã trở lên
- **Hiện trạng**: Bài 1 mã NLS/AI hiển thị đầy đủ dòng `- Năng lực số: Mã : Mô tả`. Nhưng khi bài có 2 mã trở lên, chỉ hiển thị các dòng con `+ Mã 1 : ...`, `+ Mã 2 : ...`, mất hẳn dòng tiêu đề `- Năng lực số:`.
- **Nguyên nhân**: Trong `integrationParts(value)` (dòng 1544 của `xaydungphuluc.html` và tương ứng trong các file canvas), khi `subItems.length > 0`, hàm chỉ lặp và `push` các dòng con `sub` vào `results`, bỏ rơi dòng tiêu đề `lines[0]` (`- Năng lực số:` hoặc `- Năng lực AI:`).

### 2. Phụ lục 3 chỉ làm được mấy bài ("làm mấy bài thôi, không đầy đủ")
- **Hiện trạng**: Xuất Phụ lục 3 chỉ ra 9–10 bài đầu (Chương I và đầu Chương II), mất toàn bộ phần còn lại của năm học (30–40 bài).
- **Nguyên nhân**:
  1. `appendixPrompt(3, c)` yêu cầu AI sinh lại toàn bộ bảng PPCT `{plan: [...]}`. Do giới hạn token, Gemini bị cắt ngắn, chỉ trả về được 9–10 bài đầu.
  2. Trong `normalizeAppendix(data, '3', c)` (dòng 1637):
     ```javascript
     let planCandidate = Array.isArray(data.plan) && data.plan.length ? data.plan : ...
     ```
     Vì `data.plan` có 9 bài do AI trả về, `planCandidate` lấy luôn mảng 9 bài này và vứt bỏ toàn bộ danh sách đầy đủ 47 bài của PPCT nguồn / Phụ lục 1.
  3. Trong `renderPreview` (dòng 1662) và `exportDocx` (dòng 1674):
     Điều kiện kiểm tra `r.planTable.columns.length === 8` bị sai lệch vì bảng Phụ lục 3 chuẩn hiện hành có 7 cột (kết thúc bằng `Ghi chú`). Do `7 === 8` luôn trả về `false`, `planModel` bị hủy và buộc phải chạy lại hàm tạo bảng trên dữ liệu thiếu.

### 3. Phụ lục 3 không đưa ra được Ghi chú (toàn bộ cột Ghi chú bị dấu gạch `-`)
- **Hiện trạng**: Toàn bộ các dòng trong cột Ghi chú của Phụ lục 3 bị gạch ngang `-`, không hiển thị NLS và AI.
- **Nguyên nhân**:
  1. Trong `appendixThreeTable` (dòng 211 / dòng 1690): Hàm tìm `isNlsColumn` và `isAiColumn` trên `pl1Model`, nhưng Phụ lục 1 đã gộp 2 cột này thành cột `Ghi chú` (`isNoteColumn`). Hàm không tìm thấy (`-1`) và không lấy nội dung cột `Ghi chú` của Phụ lục 1.
  2. Hàm sau đó fallback sang `separateIntegration(row.integration, ...)`. Trong `separateIntegration`, hàm `isLessonNlsSelected(lessonId, lessonName, ...)` kiểm tra ID: các dòng của Phụ lục 3 có ID dạng `ppct:0` trong khi danh sách tick chọn có ID dạng `source:0`. Do `hasId` là `true` nhưng không khớp, dòng 1396 trả về `false` ngay lập tức mà không tiếp tục so sánh theo `lessonName`. NLS bị xóa sạch thành `'-'`, khiến `formatNoteIntegration` trả về `'-'`.

---

## Phạm vi thực hiện

1. **Sửa `integrationParts(value)`**: Khi phân tách khối có các dòng con `subItems` (`+ ...`), bắt buộc đưa dòng tiêu đề `lines[0]` vào kết quả trước khi đưa các dòng `subItems`.
2. **Sửa `normalizeAppendix` cho Phụ lục 3**: Bảo đảm danh sách bài học của Phụ lục 3 luôn lấy trọn vẹn 100% từ tiến trình chuẩn (`results['1']?.schedule`, `sourcePpctRows` hoặc `defaultPpctRows(c)`), không bao giờ bị cắt cụt bởi kết quả AI trả về thiếu bài.
3. **Đồng bộ chuẩn xác cột Ghi chú cho Phụ lục 3 trong `appendixThreeTable`**:
   - Ưu tiên lấy trực tiếp nội dung cột `Ghi chú` đã có từ `pl1Model` (Phụ lục 1) theo bài học tương ứng để đảm bảo đồng bộ 100% giữa Tổ chuyên môn và Giáo viên.
   - Nếu không có bảng Phụ lục 1, sử dụng `formatNoteIntegration` từ chính `row.integration` của bài học.
4. **Sửa `isLessonNlsSelected`**: Khi `hasId` không khớp trong Set thì không được `return false` ngay mà phải tiếp tục đối chiếu theo `lessonName`.
5. **Sửa điều kiện kiểm tra số cột Phụ lục 3 trong `renderPreview` và `exportDocx`**: Chuyển từ `length === 8` sang `length === 7` (hoặc `APPENDIX_3_COLUMNS.length`).
6. **Đồng bộ 1:1 sang các file Canvas và cập nhật smoke test**.

---

## Ngoài phạm vi
- Không thay đổi các tiêu chí và công thức tính tỷ lệ NLS / AI.
- Không thay đổi cấu trúc bảng hay thông tin hành chính của Phụ lục 1 và Phụ lục 2.

---

## File dự kiến tác động
- `xaydungphuluc.html`
- `canvas_xaydungphuluc.html`
- `backupcode viettailieu/canvas_xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `tests/canvas-xaydungphuluc-smoke.js`

---

## Chi tiết các bước thực hiện

### Bước 1: Sửa hàm `integrationParts(value)` (giữ dòng tiêu đề `- Năng lực số:` / `- Năng lực AI:`)
Tại dòng 1544 trong `xaydungphuluc.html` (và tương ứng trong các file canvas):
```javascript
if (subItems.length) {
  if (lines[0]) results.push({ text: lines[0], ai: isAi });
  for (const sub of subItems) results.push({ text: sub, ai: isAi });
} else {
  results.push({ text: b, ai: isAi });
}
```

### Bước 2: Sửa `isLessonNlsSelected` (tránh nuốt NLS khi ID có prefix khác nhau)
Tại dòng 1395:
```javascript
if (hasExplicit) {
  if (hasId && nlsSelectedLessonIds.has(lessonId)) return true;
  if (lessonName) {
    const match = nlsCandidates().find(x => typeof lessonsMatch === 'function' ? lessonsMatch(x.lesson, lessonName) : x.lesson === lessonName);
    if (match && nlsSelectedLessonIds.has(match.id)) return true;
  }
  return false;
}
```
Và tại dòng 1410:
```javascript
if (hasId && topIds.has(lessonId)) return true;
if (lessonName) {
  const match = prioritized.slice(0, targetCount).find(x => typeof lessonsMatch === 'function' ? lessonsMatch(x.lesson, lessonName) : x.lesson === lessonName);
  if (match) return true;
}
return false;
```

### Bước 3: Sửa `normalizeAppendix` cho Phụ lục 3 (bảo toàn 100% danh sách bài học, không bị AI cắt cụt)
Tại dòng 1637 trong `normalizeAppendix` nhánh `no === '3'`:
Lấy `fullSchedule` từ `results['1']?.schedule` hoặc `sourcePpctRows` hoặc `defaultPpctRows(c)`.
Ánh xạ toàn bộ danh sách `fullSchedule`:
```javascript
const defaultEquip = (typeof EQUIPMENT !== 'undefined' && c && (EQUIPMENT[c.monHoc] || EQUIPMENT.default)) ? (EQUIPMENT[c.monHoc] || EQUIPMENT.default).slice(0, 2).join(', ') : 'Thiết bị dạy học tối thiểu';
let fullSchedule = [];
if (results['1'] && Array.isArray(results['1'].schedule) && results['1'].schedule.length) fullSchedule = results['1'].schedule;
else if (typeof sourcePpctRows !== 'undefined' && Array.isArray(sourcePpctRows) && sourcePpctRows.length) fullSchedule = sourcePpctRows;
else if (typeof defaultPpctRows === 'function') fullSchedule = defaultPpctRows(c);

const aiPlan = Array.isArray(data?.plan) && data.plan.length ? data.plan : (Array.isArray(data?.schedule) ? data.schedule : []);
data.plan = fullSchedule.map((baseRow, idx) => {
  if (baseRow.isHeader) return ppctRow(baseRow, idx, c);
  const matchingAi = aiPlan.find(r => !r.isHeader && typeof lessonsMatch === 'function' && lessonsMatch(r.lesson, baseRow.lesson));
  return ppctRow({
    ...baseRow,
    devices: matchingAi?.devices || baseRow.devices || defaultEquip,
    location: matchingAi?.location || baseRow.location || 'Lớp học',
    integration: matchingAi?.integration || baseRow.integration || ''
  }, idx, c);
}).filter(row => row.lesson && !isAdminLesson(row.lesson));

if (!results['1']) results['1'] = normalizeAppendix(fallback('1', c), '1', c);
data.plan = syncIntegrationFromAppendixOne(data.plan, results['1'].scheduleTable, c);
data.planTable = appendixThreeTable(data.plan, c);
```

### Bước 4: Sửa `appendixThreeTable` (đồng bộ trực tiếp Ghi chú từ Phụ lục 1)
Tại dòng 1690 trong `xaydungphuluc.html`:
```javascript
appendixThreeTable = function(rows, c) {
  const pl1Model = results?.['1']?.scheduleTable ? normalizeIntegrationTable(results['1'].scheduleTable) : null;
  const pl1NoteIdx = pl1Model ? pl1Model.columns.findIndex(isNoteColumn) : -1;
  const pl1LessonIdx = pl1Model ? pl1Model.columns.map(normalizeHeaderKey).indexOf('lesson') : -1;
  const usedPl1 = new Set();
  let normal = 0;

  const table = legacyAppendixThreeTableForNote(rows, c);
  const nlsIdx = table.columns.findIndex(isNlsColumn);
  const aiIdx = table.columns.findIndex(isAiColumn);
  const nlsCol = nlsIdx >= 0 ? nlsIdx : 6;
  const aiCol = aiIdx >= 0 ? aiIdx : 7;

  return {
    ...table,
    columns: APPENDIX_3_COLUMNS.map(([, label]) => label),
    rows: table.rows.map((row, idx) => {
      if (row.isHeader) return row;
      let note = '';
      if (pl1Model && pl1NoteIdx >= 0) {
        const pl1Row = typeof pickAppendixOneRow === 'function' ? pickAppendixOneRow(pl1Model, row.cells[0], usedPl1, normal) : pl1Model.rows.find(item => !item.isHeader && lessonsMatch((item.cells || [])[pl1LessonIdx], row.cells[0]));
        if (pl1Row) {
          note = String((pl1Row.cells || [])[pl1NoteIdx] || '').trim();
        }
      }
      if (!note || note === '-') {
        const nlsText = row.cells[nlsCol];
        const aiText = row.cells[aiCol];
        note = formatNoteIntegration(nlsText, aiText, row.cells[0]);
      }
      normal++;
      return { ...row, cells: [...row.cells.slice(0, 6), note || '-'] };
    })
  };
};
```

### Bước 5: Sửa điều kiện kiểm tra cột Phụ lục 3 trong `renderPreview` và `exportDocx`
Đổi `columns.length === 8` thành `columns.length === 7` (hoặc `columns.length === APPENDIX_3_COLUMNS.length`):
- Trong `renderPreview` (dòng 1662)
- Trong `exportDocx` (dòng 1674)
- Áp dụng tương tự cho các file canvas.

### Bước 6: Đồng bộ sang `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`
Đảm bảo đồng bộ 100% logic trên cả 3 file.

### Bước 7: Cập nhật smoke test và kiểm chứng
1. Cập nhật `tests/xaydungphuluc-smoke.js`:
   - Kiểm tra `multiNoteParts` có đủ dòng tiêu đề `- Năng lực số:` và `- Năng lực AI:`.
   - Kiểm tra `appendixThreeTable` giữ đủ toàn bộ danh sách bài học và cột `Ghi chú` khớp với Phụ lục 1.
2. Cập nhật `tests/canvas-xaydungphuluc-smoke.js` tương tự.
3. Chạy toàn bộ 4 suite test kiểm tra bảo đảm 100% PASS:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/canvas-xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-math-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`

---

## Tiêu chí nghiệm thu
1. Cột Ghi chú của bài có từ 2 mã NLS/AI trở lên luôn giữ dòng tiêu đề `- Năng lực số:` / `- Năng lực AI:` trước các bullet con `+ `.
2. Phụ lục 3 hiển thị và xuất Word trọn vẹn 100% số bài học của năm học (đủ 35 tuần / toàn bộ các chương), không bị dừng lại sau 9–10 bài.
3. Cột Ghi chú trong Phụ lục 3 cập nhật đầy đủ nội dung biểu hiện NLS và AI, khớp 100% với Phụ lục 1.
4. Báo cáo thẩm định đạt tiêu chí "Đồng bộ NLS & AI (PL1–PL3)" 100%.
5. Tất cả bài smoke test đều PASS.
