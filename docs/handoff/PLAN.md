# PLAN: Thiết kế phân bổ Năng lực số và AI linh hoạt theo Số tiết / Số bài dạy bài mới

Trạng thái: CHỜ DUYỆT (Coder chuẩn bị thực hiện)

## 1. Mục tiêu & Yêu cầu từ Người dùng

1. **Linh hoạt 2 phương án phân bổ (cả NLS và AI)**:
   - **Phương án 1 - Theo số tiết**: Phân bổ theo số lượng tiết hoặc tỉ lệ % do người dùng quy định, ghi rõ là **"tiết dạy bài mới"** (ví dụ: `20/95 tiết dạy bài mới`).
   - **Phương án 2 - Theo số bài**: Phân bổ theo số lượng bài hoặc tỉ lệ % do người dùng quy định, ghi rõ là **"bài dạy bài mới"** (ví dụ: `9/47 bài dạy bài mới`).
2. **Không khóa cứng trần**:
   - Bỏ hoàn toàn việc khóa cứng trần (như trần 12 tiết AI trước đây). Người dùng có quyền tự do kéo hoặc nhập số tiết/bài theo nhu cầu thực tế của nhà trường (từ 0 đến toàn bộ 100% số tiết/bài dạy bài mới).
3. **Phạm vi áp dụng**:
   - **Chỉ điều chỉnh duy nhất trên file `xaydungphuluc.html`** (và bộ test `tests/xaydungphuluc-smoke.js`).
   - Không thay đổi `canvas_xaydungphuluc.html` hay các bản backup.

---

## 2. Thiết kế Giao diện (UI) trên `xaydungphuluc.html`

Tại Mục 1 (khối thẻ NLS và AI, dòng ~31 trong `xaydungphuluc.html`):

### 2.1. Thẻ Năng lực số (CV 3456 / TT 02)
- **Chọn chế độ phân bổ**:
  - Bổ sung `<select id="nlsUnit" class="field text-xs py-1 px-2 w-auto" onchange="onNlsUnitChange(this.value)">`:
    - `<option value="period" selected>Theo số tiết dạy bài mới</option>`
    - `<option value="lesson">Theo số bài dạy bài mới</option>`
- **Thanh kéo & Ô nhập số lượng trực tiếp**:
  - Thanh trượt `%`: `<input id="nlsRate" class="w-full" type="range" min="0" max="100" value="50" oninput="syncNlsSelectionFromRate()">`
  - Ô nhập số lượng trực tiếp cạnh nhãn: `<input id="nlsCountInput" type="number" min="0" class="field text-xs py-0.5 px-1.5 w-16 text-center" onchange="syncNlsSelectionFromCount(this.value)">`
  - Nhãn hiển thị `<output id="nlsRateOut">`:
    - Khi chế độ là **Theo số tiết**:
      `${rate}% (${selectedPeriods}/${totalPeriods} tiết dạy bài mới · ${selectedLessons}/${totalLessons} bài)`
      *(Ví dụ: `21% (20/95 tiết dạy bài mới · 10/47 bài)`)*
    - Khi chế độ là **Theo số bài**:
      `${rate}% (${selectedLessons}/${totalLessons} bài dạy bài mới · ${selectedPeriods}/${totalPeriods} tiết)`
      *(Ví dụ: `21% (10/47 bài dạy bài mới · 20/95 tiết)`)*

### 2.2. Thẻ Trí tuệ nhân tạo (QĐ 2422)
- **Chọn chế độ phân bổ**:
  - Bổ sung `<select id="aiUnit" class="field text-xs py-1 px-2 w-auto" onchange="onAiUnitChange(this.value)">`:
    - `<option value="period" selected>Theo số tiết dạy bài mới</option>`
    - `<option value="lesson">Theo số bài dạy bài mới</option>`
- **Thanh kéo & Ô nhập số lượng trực tiếp**:
  - Thanh trượt `%`: `<input id="aiRate" class="w-full" type="range" min="0" max="100" value="30" oninput="syncAiSelectionFromRate()">`
  - Ô nhập số lượng trực tiếp: `<input id="aiCountInput" type="number" min="0" class="field text-xs py-0.5 px-1.5 w-16 text-center" onchange="syncAiSelectionFromCount(this.value)">`
  - Nhãn hiển thị `<output id="aiRateOut">`:
    - Khi chế độ là **Theo số tiết**:
      `${rate}% (${selectedPeriods}/${totalPeriods} tiết dạy bài mới · ${selectedLessons}/${totalLessons} bài)`
      *(Ví dụ: `21% (20/95 tiết dạy bài mới · 9/47 bài)`)*
    - Khi chế độ là **Theo số bài**:
      `${rate}% (${selectedLessons}/${totalLessons} bài dạy bài mới · ${selectedPeriods}/${totalPeriods} tiết)`
- **Xóa bỏ khóa cứng trần**:
  - Giữ `aiRate.max = '100'`. Không chặn trần ở 12 tiết nữa.
  - Định mức 12 tiết cũ chỉ giữ vai trò gợi ý tham khảo nếu cần, không khóa hành vi người dùng.

### 2.3. Bảng chọn Mục 4 (`#aiLessonPicker`)
- Dòng thông tin tổng hợp trên thanh công cụ:
  `📊 NLS: ${nlsPeriods} tiết dạy bài mới (${nlsLessons} bài) · 🎯 AI: ${aiPeriods} tiết dạy bài mới (${aiLessons} bài)`
- Cột NLS: Checkbox từng bài hiển thị kèm số tiết: `Tích hợp NLS (${row.periodCount} tiết)`.
- Cột AI: Bỏ giới hạn chặn `if (selected.size >= limit) { notify(...); return; }` khi tick thủ công. Người dùng có thể tick tùy ý bao nhiêu tiết tùy nhu cầu.

---

## 3. Logic & Thuật toán chi tiết cho Coder

### 3.1. Dữ liệu nền tảng
- `totalLessons = aiCandidates().length` (Số bài dạy bài mới, ví dụ Toán 6: 47 bài).
- `totalPeriods = aiPeriodCandidates().length` (Số tiết của các bài dạy bài mới, ví dụ Toán 6: 95 tiết).

### 3.2. Thuật toán phân bổ NLS (`syncNlsSelectionFromRate` & `syncNlsSelectionFromCount`)
1. **Nếu `nlsUnit === 'period'` (Theo số tiết)**:
   - Từ `%` hoặc số lượng người dùng nhập, tính số tiết mục tiêu: `targetPeriods`.
   - Lấy danh sách bài đã ưu tiên: `prioritizedNlsLessons()`.
   - Lần lượt duyệt các bài trong danh sách ưu tiên, cộng dồn số tiết của từng bài vào tập chọn cho đến khi đạt hoặc xấp xỉ gần nhất với `targetPeriods`.
   - Lưu vào `nlsSelectedLessonIds`.
   - Cập nhật nhãn và ô số lượng: `${rate}% (${currentPeriods}/${totalPeriods} tiết dạy bài mới · ${currentLessons}/${totalLessons} bài)`.
2. **Nếu `nlsUnit === 'lesson'` (Theo số bài)**:
   - Từ `%` hoặc số lượng người dùng nhập, tính số bài mục tiêu: `targetLessons`.
   - Chọn đúng `targetLessons` bài đầu tiên trong `prioritizedNlsLessons()`.
   - Cập nhật nhãn và ô số lượng: `${rate}% (${targetLessons}/${totalLessons} bài dạy bài mới · ${currentPeriods}/${totalPeriods} tiết)`.

### 3.3. Thuật toán phân bổ AI (`syncAiSelectionFromRate` & `syncAiSelectionFromCount`)
1. **Nếu `aiUnit === 'period'` (Theo số tiết)**:
   - Tính số tiết mục tiêu: `targetPeriods = Math.round(rate / 100 * totalPeriods)` (hoặc lấy từ `aiCountInput`).
   - Lấy danh sách tiết ưu tiên: `prioritizedAiPeriods()`.
   - Chọn đúng `targetPeriods` tiết đầu tiên: `aiSelectedLessonIds = new Set(prioritizedAiPeriods().slice(0, targetPeriods).map(x => x.id))`.
   - Không áp đặt trần `Math.min(limit, ...)`.
   - Cập nhật nhãn và ô số lượng: `${rate}% (${targetPeriods}/${totalPeriods} tiết dạy bài mới · ${selectedLessonsCount}/${totalLessons} bài)`.
2. **Nếu `aiUnit === 'lesson'` (Theo số bài)**:
   - Tính số bài mục tiêu: `targetLessons = Math.round(rate / 100 * totalLessons)`.
   - Lấy `targetLessons` bài ưu tiên trong danh sách, chọn tất cả các tiết thuộc các bài đó.
   - Cập nhật nhãn và ô số lượng: `${rate}% (${targetLessons}/${totalLessons} bài dạy bài mới · ${selectedPeriodsCount}/${totalPeriods} tiết)`.

### 3.4. Đồng bộ 2 chiều giữa Slider `%` và Ô nhập số lượng
- Khi kéo Slider `%`: tính ra số lượng tiết/bài và điền vào ô input số lượng.
- Khi gõ số lượng vào ô input: tính ngược lại ra `%` tương ứng và cập nhật vị trí con trượt Slider.

### 3.5. Lưu / Tải bản nháp (Draft Config)
- Trong `getConfig()`: bổ sung `nls.unit` và `ai.unit`.
- Trong `applyDraftPayload()`: phục hồi `nlsUnit.value` và `aiUnit.value`.

---

## 4. Phạm vi File tác động
1. `xaydungphuluc.html`: Toàn bộ điều chỉnh UI, logic phân bổ, nhãn text và gỡ khóa cứng.
2. `tests/xaydungphuluc-smoke.js`: Cập nhật assertion kiểm tra 2 chế độ (theo số tiết và theo số bài), xác nhận nhãn có cụm từ "tiết dạy bài mới" / "bài dạy bài mới" và không bị khóa cứng trần 12 tiết.

---

## 5. Tiêu chí nghiệm thu (Acceptance Criteria)
1. Có thể chuyển đổi qua lại giữa 2 chế độ: "Theo số tiết dạy bài mới" và "Theo số bài dạy bài mới" cho cả NLS và AI.
2. Gõ trực tiếp ví dụ `20` vào ô số lượng:
   - NLS tự động chọn các bài có tổng khoảng 20 tiết dạy bài mới.
   - AI tự động chọn đúng 20 tiết dạy bài mới.
3. Kéo slider: Vị trí slider và ô số lượng đồng bộ 2 chiều mượt mà.
4. Nhãn hiển thị ghi rõ ràng:
   - `${...} tiết dạy bài mới`
   - `${...} bài dạy bài mới`
5. AI hoàn toàn không bị kẹt ở 12 tiết, người dùng có thể chọn 20 tiết, 30 tiết hoặc kéo đến 100%.
6. Tất cả smoke tests tự động đạt PASS:
   ```bash
   node tests/xaydungphuluc-smoke.js
   ```
