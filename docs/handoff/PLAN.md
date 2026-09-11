# PLAN: Khắc phục lỗi NLS & AI trên Canvas, Mặc định đợt TKB rỗng & Chuẩn hoá Lịch báo giảng

Trạng thái: CHỜ CODER THỰC HIỆN

---

## 1. Yêu cầu & Hiện trạng

### Yêu cầu 1 (MỚI): `canvas_xaydungphuluc` — Khi bỏ check NLS & AI rồi nhấn lại báo không có tiết nào được chọn
- **Hiện trạng**:
  - Checkbox Trí tuệ nhân tạo `#aiEnabled` hoàn toàn không có sự kiện `onchange`.
  - Checkbox Năng lực số `#nlsEnabled` chỉ có `onchange="updateAiPicker()"`, không có hàm đồng bộ lại bài học khi bật lại.
  - Khi người dùng bỏ check (hoặc bấm nút "Bỏ NLS", "Bỏ chọn tất cả"), `nlsRate` và `aiRate` bị đồng bộ về `0`.
  - Khi người dùng tích chọn lại (nhấn lại), hệ thống không tự phục hồi tỉ trọng mặc định (50% / 30%) và không gọi `sync...SelectionFromRate()`, dẫn đến danh sách bài/tiết đã chọn vẫn bằng `0`.
  - Kết quả Mục 4 hiển thị: `📊 NLS: 0 tiết dạy bài mới (0 bài) · 🎯 AI: 0 tiết dạy bài mới (0 bài)` và tất cả checkbox trong bảng đều trống, thông báo "không có tiết nào được chọn".
- **Yêu cầu**:
  - Khi bỏ check NLS hoặc AI: toàn bộ bài/tiết tương ứng được bỏ chọn sạch sẽ.
  - Khi nhấn check lại NLS hoặc AI: tự động khôi phục tỉ lệ mặc định (NLS: 50%, AI: 30%) nếu đang là 0, tự động chọn lại các bài/tiết ưu tiên và cập nhật ngay vào bảng và dòng tổng số Mục 4.
  - Khi bấm nút "Gợi ý NLS theo tỉ trọng" hoặc "Gợi ý AI theo tỉ trọng": nếu checkbox tương ứng đang tắt thì tự động bật lên; nếu rate đang là 0 thì phục hồi 50%/30% để luôn gợi ý đúng bài/tiết thay vì ra 0.
  - Áp dụng đồng bộ cho cả `canvas_xaydungphuluc.html` và `xaydungphuluc.html`.

### Yêu cầu 2: Quản lý tổ chuyên môn — Mặc định dữ liệu giáo viên đều rỗng khi tạo đợt phân công TKB
- **Hiện trạng**: Checkbox `#qp-inherit-assignments` mặc định `checked = true`. Khi bỏ chọn thì hàm `submitQuickNewPhase` vẫn giữ nguyên TKB (`t.timetable`) của giáo viên từ đợt cũ.
- **Yêu cầu**: Đổi mặc định `#qp-inherit-assignments` thành không chọn (`checked = false`), làm rỗng toàn bộ `assignments: {}` và `timetable: emptyTimetable()` của toàn bộ giáo viên để nhận diện TKB mới hoàn toàn sạch.

### Yêu cầu 3: Lịch báo giảng — Hiển thị rõ ngày thứ mấy
- **Hiện trạng**: Thẻ ngày chỉ ghi `Ngày 2026-09-09`, `Ngày 2026-09-10`, chưa có Thứ mấy.
- **Yêu cầu**: Thể hiện rõ Thứ mấy trong tuần ở cả email gửi giáo viên (HTML card & plain text) và bảng xem trực tiếp trên giao diện web (ví dụ: `Thứ Tư, ngày 09/09/2026`).

### Yêu cầu 4: Lịch báo giảng — Hiển thị sai phân đoạn tiết của bài dạy (`1 · 1/1` thay vì `1 · 1/3`)
- **Hiện trạng**: Bài 11 (Toán 9: *Tỉ số lượng giác của góc nhọn*) có 3 tiết, chia Tuần 1 (1 tiết) và Tuần 2 (2 tiết). Hàm `parseBaoGiangCurriculum` hiện tại tính phân đoạn `segment` độc lập theo từng dòng PPCT nên Tuần 1 (dòng có 1 tiết) bị ra `1/1`.
- **Yêu cầu**: Gom khối bài học liền kề trong cùng mạch môn học để tính tổng số tiết lũy kế (1 + 2 = 3 tiết), hiển thị chính xác `Tiết PPCT 1 · 1/3` ở Tuần 1, và `2 · 2/3`, `3 · 3/3` ở Tuần 2.

---

## 2. Giải pháp kỹ thuật chi tiết

### 2.1. Xử lý Toggle & Gợi ý NLS / AI trên `canvas_xaydungphuluc.html` & `xaydungphuluc.html`

1. **Xây dựng hàm xử lý sự kiện `onNlsEnabledChange(checked)`**:
   ```javascript
   function onNlsEnabledChange(checked){
       const enabled = checked !== undefined ? checked : document.querySelector('#nlsEnabled')?.checked;
       if(enabled){
           const rateEl = document.querySelector('#nlsRate');
           if(rateEl && (Number(rateEl.value) <= 0 || nlsSelectedLessonIds.size === 0)){
               rateEl.value = '50';
           }
           syncNlsSelectionFromRate();
       } else {
           nlsSelectedLessonIds.clear();
           syncNlsRateFromSelection();
           updateAiPicker();
       }
   }
   ```

2. **Xây dựng hàm xử lý sự kiện `onAiEnabledChange(checked)`**:
   ```javascript
   function onAiEnabledChange(checked){
       const enabled = checked !== undefined ? checked : document.querySelector('#aiEnabled')?.checked;
       if(enabled){
           const rateEl = document.querySelector('#aiRate');
           if(rateEl && (Number(rateEl.value) <= 0 || aiSelectedLessonIds.size === 0)){
               rateEl.value = '30';
           }
           syncAiSelectionFromRate();
       } else {
           aiSelectedLessonIds.clear();
           syncAiRateFromSelection();
           updateAiPicker();
       }
   }
   ```

3. **Gắn sự kiện `onchange` vào thẻ HTML trong cả 2 file**:
   ```html
   <label><input id="nlsEnabled" type="checkbox" checked onchange="onNlsEnabledChange(this.checked)"> <b>Năng lực số (CV 3456 / TT 02)</b></label>
   ...
   <label><input id="aiEnabled" type="checkbox" checked onchange="onAiEnabledChange(this.checked)"> <b>Trí tuệ nhân tạo (QĐ 2422)</b></label>
   ```

4. **Nâng cấp hàm `suggestNlsLessons()` & `suggestAiLessons()`**:
   - `suggestNlsLessons()`:
     ```javascript
     function suggestNlsLessons(){
         const nlsCheckbox = document.querySelector('#nlsEnabled');
         if(nlsCheckbox && !nlsCheckbox.checked) nlsCheckbox.checked = true;
         const rateEl = document.querySelector('#nlsRate');
         if(rateEl && Number(rateEl.value) <= 0) rateEl.value = '50';
         syncNlsSelectionFromRate();
         notify(`Đã gợi ý ${nlsSelectedLessonIds.size} bài học tích hợp NLS theo tỉ trọng.`);
     }
     ```
   - `suggestAiLessons()`:
     ```javascript
     function suggestAiLessons(){
         const aiCheckbox = document.querySelector('#aiEnabled');
         if(aiCheckbox && !aiCheckbox.checked) aiCheckbox.checked = true;
         const rateEl = document.querySelector('#aiRate');
         if(rateEl && Number(rateEl.value) <= 0) rateEl.value = '30';
         syncAiSelectionFromRate();
         notify(`Đã gợi ý ${aiSelectedLessonIds.size} tiết AI.`);
     }
     ```

---

### 2.2. Quản lý đợt phân công & TKB rỗng mặc định (`phancongtochuyenmon.html`)

1. **Giao diện Modal Tạo nhanh Đợt mới (`#quick-phase-modal`)**:
   - Bỏ thuộc tính `checked` mặc định của `#qp-inherit-assignments` trong HTML.
   - Sửa nhãn: `Kế thừa phân công & TKB từ đợt hiện tại (mặc định để trống để làm rỗng và nhận diện lại TKB mới cho chính xác)`.
   - Trong `openQuickNewPhaseModal()`: gán `document.getElementById('qp-inherit-assignments').checked = false;`.

2. **Hàm xử lý `submitQuickNewPhase()`**:
   - Khi `inherit === false` (mặc định):
     - Gán `assignments: {}` và `timetable: emptyTimetable()` cho toàn bộ giáo viên:
       ```javascript
       const freshTeachers = state.teachers.map(t => ({
           ...t,
           assignments: {},
           timetable: emptyTimetable(),
           school_duties: Array.isArray(t.school_duties) ? [...t.school_duties] : []
       }));
       const freshUnassigned = {};
       state.subjects.forEach(sub => {
           freshUnassigned[sub.key] = getSubjectDutyType(sub) === 'school_duty' ? [] : [...state.classes];
       });
       state.phase_assignments[newPhaseId] = {
           teachers: freshTeachers,
           unassigned: freshUnassigned
       };
       editingTimetable = emptyTimetable();
       clearTimetablePreview();
       ```

3. **Hàm chuyển đợt `switchPhase(phaseId)`**:
   - Khi chuyển sang một đợt chưa từng có snapshot phân công: khởi tạo `teachers` với `timetable: emptyTimetable()` và `assignments: {}`.

---

### 2.3. Lịch báo giảng: Bổ sung Thứ mấy (`phancongtochuyenmon.html`)

1. **Hàm tiện ích `baoGiangWeekdayLabel(dateValue)`**:
   ```javascript
   function baoGiangWeekdayLabel(dateValue) {
       const d = dateValue instanceof Date ? dateValue : baoGiangDate(dateValue);
       if (!d) return '';
       const weekdays = ['Chủ nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'];
       return weekdays[d.getDay()] || '';
   }
   ```

2. **Cập nhật hiển thị email gửi giáo viên (`buildBaoGiangSelfEmail`)**:
   - Tiêu đề từng ngày:
     `<div style="padding:11px 12px;background:#dbeafe;color:#1e3a8a;font-weight:700;font-size:15px;">${escapeHtml(baoGiangWeekdayLabel(date))}, ngày ${escapeHtml(formatVnDate(date))}</div>`
   - Dòng văn bản plain text (`list`):
     `${baoGiangWeekdayLabel(row.date)}, ${formatVnDate(row.date)} | ...`

3. **Cập nhật `composeBaoGiangEmail()` & bảng Lịch báo giảng web (`renderBaoGiangView`)**:
   - Cột ngày trong bảng: `<b>${escapeHtml(baoGiangWeekdayLabel(row.date))}</b><br><small style="color:#64748b;">${escapeHtml(formatVnDate(row.date))}</small>`.

---

### 2.4. Lịch báo giảng: Gộp khối bài học đa tuần & tính phân đoạn `segment` chính xác (`phancongtochuyenmon.html`)

1. **Chuẩn hoá tên bài học (`normalizeBaoGiangLessonTitle`)**:
   - Xử lý các hậu tố: `(tiếp theo)`, `(t.t)`, `(tiếp)`, `(tiết \d+)`, `[tiết \d+]`.

2. **Thuật toán gom cụm khối bài học liên tục theo mạch (`parseBaoGiangCurriculum`)**:
   - Nhóm các dòng liền kề trong cùng mạch môn học có cùng tên bài đã chuẩn hoá thành 1 khối bài học duy nhất (`totalPeriods = sum(entry.periods)`).
   - Đánh số phân đoạn `segment` theo khối lũy kế: `segIndex / block.totalPeriods`.
   - Kết quả: Bài 11 (3 tiết) dạy 1 tiết Tuần 1 và 2 tiết Tuần 2 sẽ hiển thị:
     - Tuần 1: `Tiết PPCT 1 · 1/3`
     - Tuần 2: `Tiết PPCT 2 · 2/3`, `Tiết PPCT 3 · 3/3`

---

## 3. Danh sách File tác động

1. `canvas_xaydungphuluc.html`:
   - Bổ sung `onNlsEnabledChange`, `onAiEnabledChange`.
   - Gắn `onchange` cho `#nlsEnabled` và `#aiEnabled`.
   - Nâng cấp `suggestNlsLessons` và `suggestAiLessons`.
2. `xaydungphuluc.html`:
   - Bổ sung `onNlsEnabledChange`, `onAiEnabledChange`.
   - Gắn `onchange` cho `#nlsEnabled` và `#aiEnabled`.
   - Nâng cấp `suggestNlsLessons` và `suggestAiLessons`.
3. `phancongtochuyenmon.html`:
   - Modal tạo đợt mới: `#qp-inherit-assignments` mặc định `false`, làm sạch `timetable` và `assignments`.
   - Hàm `baoGiangWeekdayLabel(date)` và hiển thị Thứ mấy trong email / bảng web.
   - Chuẩn hoá `normalizeBaoGiangLessonTitle` và thuật toán gom khối bài học trong `parseBaoGiangCurriculum`.
4. `tests/xaydungphuluc-smoke.js` & `tests/baogiang-recognition-smoke.js`:
   - Thêm assertion kiểm tra toggle NLS/AI và phục hồi gợi ý.
   - Kiểm tra phân đoạn `1/3` và hiển thị Thứ mấy.

---

## 4. Tiêu chí nghiệm thu (Acceptance Criteria)

1. **Toggle NLS & AI trên Canvas**:
   - Bỏ check NLS hoặc AI: toàn bộ bài/tiết tương ứng được bỏ chọn, tổng tiết về 0.
   - Nhấn check lại NLS hoặc AI: hệ thống tự phục hồi 50% / 30%, bảng tự động tick lại các bài/tiết ưu tiên ngay lập tức, không bị 0 tiết.
   - Bấm nút "Gợi ý NLS theo tỉ trọng" hoặc "Gợi ý AI": luôn sinh ra số bài/tiết hợp lệ (> 0).
2. **Tạo đợt phân công TKB mới**:
   - Mở modal: ô "Kế thừa phân công" mặc định KHÔNG chọn.
   - Tạo đợt mới: toàn bộ giáo viên ở đợt mới có TKB trống ("⏳ Chưa có TKB") và phân công trống, sẵn sàng nhận diện TKB mới.
3. **Lịch báo giảng**:
   - Thẻ hiển thị ngày trong email và giao diện web ghi rõ Thứ mấy: `Thứ Tư, ngày 09/09/2026`.
   - Bài 11 (Toán 9) dạy 1 tiết Tuần 1 và 2 tiết Tuần 2 hiển thị chính xác: `1 · 1/3` ở Tuần 1, và `2 · 2/3`, `3 · 3/3` ở Tuần 2.
4. **Smoke test**: Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/baogiang-recognition-smoke.js` đạt 100% PASS.
