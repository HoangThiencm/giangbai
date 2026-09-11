# PLAN: Khắc phục triệt để lỗi thanh kéo % tỉ lệ Năng lực số và Năng lực AI không hoạt động

Trạng thái: ĐÃ DUYỆT

## 1. Hiện trạng & Nguyên nhân gốc rễ (Root Cause)

Khi người dùng thao tác kéo thanh trượt `<input type="range">` cho **Năng lực số (`#nlsRate`)** hoặc **Trí tuệ nhân tạo (`#aiRate`)**, giao diện bị đơ/treo cứng, nhãn phần trăm vĩnh viễn không đổi (vẫn hiển thị 50% cho NLS và 30% cho AI) do 4 nguyên nhân kỹ thuật cụ thể sau:

### 1.1. Thủ phạm trực tiếp: Tràn ngăn xếp đệ quy vô hạn (`RangeError: Maximum call stack size exceeded`)
- Trong `xaydungphuluc.html`:
  - Khi kéo chuột, sự kiện `oninput="syncNlsSelectionFromRate()"` kích hoạt.
  - Chuỗi gọi hàm:
    `syncNlsSelectionFromRate()` → `nlsCandidates()` → `aiCandidates()` → `aiPickerRows()` → `defaultPpctRows(getConfig())`.
  - Trong `xaydungphuluc.html`, hàm `getConfig()` khai báo không tham số:
    `getConfig()` → `ai: { selectedLessons: selectedAiLessons(), selectedPeriods: selectedAiPeriods() }`.
  - Hàm `selectedAiPeriods()` gọi `aiPeriodCandidates()` → `aiCandidates()` → `aiPickerRows()` → `defaultPpctRows(getConfig())`...
  - **Vòng lặp đệ quy khép kín**: `getConfig()` gọi `selectedAiPeriods()`, mà `selectedAiPeriods()` lại gọi `getConfig()`.
  - **Hậu quả**: Trình duyệt ném ngoại lệ `RangeError: Maximum call stack size exceeded` ngay tại dòng lệnh đầu tiên của `syncNlsSelectionFromRate()`. Mã lệnh bị sập ngay lập tức trước khi kịp chạy đến dòng cập nhật nhãn `nlsRateOutEl.value = ...`. Do đó nhãn `%` không bao giờ được cập nhật, vĩnh viễn bị treo ở giá trị HTML tĩnh ban đầu là `50%` và `30%`.
- Trong `canvas_xaydungphuluc.html` (và bản backup):
  - Hàm `getConfig({includeAiSelection=true}={})` có nhận tham số, NHƯNG các vị trí gọi nội bộ lại dùng cú pháp:
    `const cfg = getConfig.length ? getConfig({includeAiSelection:false}) : getConfig();`
    (tại các hàm `nlsLessonPriorityScore`, `aiSelectionLimit`, `prioritizedAiPeriods`).
  - Trong chuẩn JavaScript ES6, một hàm có tham số mặc định destructuring (`{includeAiSelection=true}={}`) thì thuộc tính `getConfig.length` luôn luôn bằng `0`!
  - Do đó biểu thức `getConfig.length ? ... : getConfig()` luôn đánh giá vào nhánh `else: getConfig()` (không đối số, mặc định `includeAiSelection=true`), gây đệ quy vô tận và sập call stack tương tự.

### 1.2. Nghẽn hiệu năng O(N log N) & vòng lặp lồng nhau gây giật lag
- Trong `selectedAiPeriods()`:
  `for(const period of aiPeriodCandidates()) if(selectedAiPeriodIds().has(period.id))`
  Hàm `selectedAiPeriodIds()` bị gọi lặp lại 140 lần bên trong điều kiện `if` của từng vòng lặp, mỗi lần lại tính toán lại danh sách ứng viên và mức trần.
- Trong `prioritizedNlsLessons()`:
  `[...nlsCandidates()].sort((a,b)=>nlsLessonPriorityScore(b.lesson)-nlsLessonPriorityScore(a.lesson)...)`
  Hàm `nlsLessonPriorityScore` bị gọi hàng trăm lần lặp đi lặp lại trong quá trình sort thay vì tính điểm trước (map/score) rồi mới sort, làm kéo chuột bị nghẽn CPU hàng chục giây.

### 1.3. Khóa trần thanh trượt AI ở mức 9% (`aiRate.max`)
- Trong `syncAiRateFromSelection()`, mã lệnh gán:
  `aiRate.max = String(aiRateMaximum(candidates));`
  Với môn 140 tiết (như Toán 6), định mức trần AI là 12 tiết, khiến `aiRateMaximum` chỉ bằng `Math.round(12/140*100) = 9%`.
- Việc ép `max = 9` khiến thanh trượt chỉ kéo được trong khoảng 0% đến 9%, kéo sang phải (20%, 30%, 50%) bị dội ngược lại hoặc không di chuyển được.

### 1.4. Gán đè ngược lại `slider.value` trong sự kiện kéo `oninput`
- Cả `syncNlsRateFromSelection` và `syncAiRateFromSelection` đều gán `slider.value = String(rate)` ngay trong luồng `oninput`, gây xung đột với trạng thái drag chuột của trình duyệt, làm con trượt bị nhảy giật lùi về vị trí cũ.

---

## 2. Phạm vi thay đổi

Khắc phục triệt để và đồng bộ 100% trên cả 3 file:
1. `xaydungphuluc.html` (Mã nguồn web chính)
2. `canvas_xaydungphuluc.html` (Mã nguồn bản Canvas)
3. `backupcode viettailieu/canvas_xaydungphuluc.html` (Bản đồng bộ dự phòng 1:1)
4. `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js` (Bổ sung kiểm thử tự động cho tương tác kéo trượt slider).

---

## 3. Giải pháp kỹ thuật chi tiết cho Coder

### Bước 1: Bảo vệ `getConfig` chống đệ quy (Áp dụng cho cả 3 file HTML)
- Thêm cờ bảo vệ re-entrancy `let _isGettingConfig = false;` (hoặc kiểm tra cờ tham số `opts` an toàn):
  ```javascript
  let _isGettingConfig = false;
  function getConfig(opts){
    const includeAi = (opts && opts.includeAiSelection === false) || _isGettingConfig ? false : true;
    _isGettingConfig = true;
    try {
      return {
        capHoc: 'THCS',
        lop: grade.value,
        monHoc: subject.value,
        boSach: (typeof bookSeries !== 'undefined' && bookSeries ? bookSeries.value : 'Sách giáo khoa dùng chung (từ 2026-2027)'),
        namHoc: schoolYear.value,
        truong: school.value,
        toChuyenMon: department.value,
        giaoVien: teacher.value,
        thongKe: {
          classes: classCount.value.trim(),
          students: studentCount.value.trim(),
          teachers: teacherCount.value.trim()
        },
        nls: {
          enabled: nlsEnabled.checked,
          rate: +nlsRate.value,
          density: nlsDensity.value,
          noAiDensity: typeof nlsNoAiDensity !== 'undefined' ? nlsNoAiDensity.value : '2-3'
        },
        ai: {
          enabled: aiEnabled.checked,
          rate: +aiRate.value,
          density: aiDensity.value,
          selectedLessons: includeAi && typeof selectedAiLessons === 'function' ? selectedAiLessons() : [],
          selectedPeriods: includeAi && typeof selectedAiPeriods === 'function' ? selectedAiPeriods() : []
        },
        clil: clil.checked,
        hoaNhap: inclusive.checked,
        chiDao: instructions.value,
        sgkContext: sgkCompactContext
      };
    } finally {
      _isGettingConfig = false;
    }
  }
  ```
- Thay thế toàn bộ biểu thức lỗi `getConfig.length ? getConfig({includeAiSelection:false}) : getConfig()` thành `getConfig({includeAiSelection:false})`.
- Trong `aiPickerRows()`: gọi `defaultPpctRows(getConfig({includeAiSelection:false}))`.

### Bước 2: Tối ưu hiệu năng `selectedAiPeriods` & `prioritizedNlsLessons` (Áp dụng cho cả 3 file HTML)
- Trong `selectedAiPeriods()`: Hoisting `selectedAiPeriodIds()` ra ngoài vòng lặp:
  ```javascript
  function selectedAiPeriods(){
    const groups = new Map(), selected = selectedAiPeriodIds();
    for (const period of aiPeriodCandidates()) {
      if (selected.has(period.id)) {
        if (!groups.has(period.lessonId)) {
          groups.set(period.lessonId, { lesson: period.lesson, lessonId: period.lessonId, periods: [] });
        }
        groups.get(period.lessonId).periods.push(period.period);
      }
    }
    return [...groups.values()];
  }
  ```
- Trong `prioritizedNlsLessons()`: Tính điểm 1 lần (map) rồi mới sort:
  ```javascript
  function prioritizedNlsLessons(){
    const candidates = nlsCandidates(), scored = candidates.map((x, i) => ({
      ...x,
      score: nlsLessonPriorityScore(x.lesson),
      index: i
    }));
    return scored.sort((a, b) => b.score - a.score || a.index - b.index || String(a.id).localeCompare(String(b.id)));
  }
  ```

### Bước 3: Sửa logic thanh trượt `#aiRate` & `#nlsRate`
- **Thanh trượt `#aiRate`**:
  - Không gán `aiRate.max = String(aiRateMaximum(candidates))`. Giữ `aiRate.max = '100'`.
  - Trong `syncAiSelectionFromRate()`:
    - Đọc tỉ lệ người dùng đang kéo: `const rate = Number(aiRate.value) || 0`.
    - Tính số lượng tiết mục tiêu theo tỉ lệ, chặn trần `aiSelectionLimit()`:
      `const total = aiPeriodCandidates().length;`
      `const limit = aiSelectionLimit();`
      `const target = Math.min(limit, Math.max(0, Math.round(rate / 100 * total)));`
      `aiSelectedLessonIds = new Set(prioritizedAiPeriods().slice(0, target).map(x => x.id));`
    - Cập nhật nhãn `#aiRateOut`:
      `if (typeof aiRateOut !== 'undefined') aiRateOut.value = `${rate}% (${aiSelectedLessonIds.size}/${total} tiết, tối đa ${limit} tiết)``;
    - Gọi `updateAiPicker()`.
  - Trong `syncAiRateFromSelection(candidates, selected)`:
    - Chỉ gán `aiRate.value = String(rate)` khi người dùng tick chọn checkbox thủ công trong bảng (không gán đè khi đang kéo `oninput`).
- **Thanh trượt `#nlsRate`**:
  - Trong `syncNlsSelectionFromRate()`:
    - Lấy giá trị thanh kéo: `const rate = Number(nlsRate.value) || 0`.
    - Tính số bài: `const total = nlsCandidates().length, targetCount = Math.round(rate / 100 * total);`
    - Gán `nlsSelectedLessonIds = new Set(prioritizedNlsLessons().slice(0, targetCount).map(x => x.id));`
    - Cập nhật trực tiếp nhãn: `if (nlsRateOutEl) nlsRateOutEl.value = `${rate}% (${targetCount}/${total} bài)``;
    - Không gán đè `nlsRate.value` trong `syncNlsSelectionFromRate()`.
    - Gọi `updateAiPicker()`.

### Bước 4: Bổ sung smoke test xác thực tương tác kéo trượt slider
- Bổ sung test case vào `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`:
  - Mô phỏng kéo `#nlsRate` về `0` và `80`: xác nhận `nlsRateOut.value` cập nhật tương ứng `0%` và `80%`, không văng `RangeError`.
  - Mô phỏng kéo `#aiRate` về `0` và `50`: xác nhận `aiRateOut.value` cập nhật đúng theo thời gian thực.

---

## 4. Ngoài phạm vi
- Không thay đổi danh mục năng lực số CV 3456, tiêu chí AI QĐ 2422.
- Không thay đổi cấu trúc xuất tệp DOCX Phụ lục 1, 2, 3 hay API CSDL nháp.

---

## 5. Tiêu chí nghiệm thu (Acceptance Criteria)
1. Kéo thanh `#nlsRate` về `0%`: Nhãn hiển thị ngay lập tức `0% (0/... bài)`, danh sách bài NLS được bỏ tick tương ứng.
2. Kéo thanh `#nlsRate` lên các mốc (25%, 50%, 80%, 100%): Nhãn cập nhật tức thì, con trượt mượt mà không bị kẹt hay giật lùi.
3. Kéo thanh `#aiRate` từ 0% đến 100%: Con trượt di chuyển tự do toàn dải 0–100% (không bị khóa cứng ở 9%), nhãn hiển thị rõ tỉ lệ % và số tiết đã chọn (chặn trần định mức theo quy định).
4. Cả 3 file `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` đồng bộ nhất quán.
5. Toàn bộ các bộ kiểm thử tự động đạt kết quả **PASS**:
   ```bash
   node tests/khbd-nls-rate-smoke.js
   node tests/canvas-xaydungphuluc-smoke.js
   node tests/xaydungphuluc-smoke.js
   ```

---

# KẾ HOẠCH ĐÃ DUYỆT — Điều chỉnh kỹ thuật bắt buộc

- Không dùng `getConfig.length` để nhận biết chữ ký hàm, vì tham số mặc định làm giá trị đó bằng `0`. Mọi helper nội bộ cần gọi trực tiếp `getConfig({includeAiSelection:false})`.
- Chuẩn hoá `getConfig({includeAiSelection=true}={})` cho cả ba trang. Ở chế độ `false`, hai mảng chọn AI phải rỗng để chặn đường đệ quy; không dựa chỉ vào cờ re-entrancy.
- `selectedAiPeriods()` phải tính candidate set và selected set một lần; `prioritizedNlsLessons()` phải tính score một lần trước khi sort.
- Luồng `oninput` cho hai slider phải truyền `preserveSlider` qua `updateAiPicker`/các hàm đồng bộ để không bị ghi ngược sau khi render. Cập nhật nhãn bằng tỷ lệ người dùng vừa kéo, còn số lựa chọn vẫn tuân thủ mức trần.
- Test phải thay assertion cũ đòi AI slider snap về `92` thành xác nhận `max=100`; bổ sung mô phỏng NLS 0/80 và AI 0/50, kiểm tra nhãn, không ném `RangeError`, giá trị slider giữ nguyên và số AI không vượt trần.
