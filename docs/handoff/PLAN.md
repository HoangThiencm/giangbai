# PLAN: Đưa bộ chọn tích hợp theo "Tổng số tiết" và "Tỉ lệ %" trực quan vào Mục 1 Xây dựng Phụ lục

## Hiện trạng

1. **Người dùng mong muốn 2 hướng chọn khi cấu hình tích hợp**:
   - Hướng 1: Chọn tích hợp theo **Tổng số tiết** (nhập trực tiếp số tiết cần tích hợp).
   - Hướng 2: Chọn tích hợp theo **Tỉ lệ %** (kéo thanh trượt % như hiện tại).
2. **Nguyên nhân hiện tại chỉ thấy thanh trượt %**:
   - Về logic JS (`canvas_xaydungphuluc.html` và `xaydungphuluc.html`): Hệ thống **đã có sẵn** đầy đủ các hàm xử lý tính toán hai chiều:
     + `syncNlsSelectionFromRate()` / `syncAiSelectionFromRate()`: Chọn theo tỉ lệ %.
     + `syncNlsSelectionFromCount(value)` / `syncAiSelectionFromCount(value)`: Chọn theo số tiết hoặc số bài.
     + `syncNlsRateFromSelection()` / `syncAiRateFromSelection()`: Đồng bộ ngược từ số bài/tiết đã chọn về % và số lượng.
     + `allocationUnit(kind)`: Đơn vị phân bổ (`period` - theo số tiết, `lesson` - theo số bài).
   - Về giao diện HTML trên `canvas_xaydungphuluc.html` (trang Canvas chính):
     + Cụm thẻ nhập số tiết `#nlsCountInput`, `#aiCountInput` và `#nlsUnit`, `#aiUnit` vô tình bị đặt trong một `<section class="card p-4">` phụ nằm ở **tận cuối trang** (dưới Mục 7 - Xem trước & xuất Word, dòng 73).
     + Trong khi đó, tại **Mục 1 (Thông tin & cấu hình sư phạm)** - nơi người dùng thao tác trực tiếp với NLS và AI, chỉ hiển thị mỗi thanh trượt `#nlsRate` và `#aiRate`.
     + Do đó, người dùng nhìn vào khung Mục 1 chỉ thấy thanh trượt % mà không thấy ô nhập / chọn theo Tổng số tiết.

---

## Mục tiêu & Giải pháp thiết kế

1. **Đưa bộ chọn 2 hướng (Số tiết / Tỉ lệ %) trực tiếp vào từng thẻ NLS và AI tại Mục 1**:
   - Trong thẻ **Năng lực số (CV 3456 / TT 02)**:
     + Hiển thị rõ ràng 2 cách điều chỉnh song hành, đồng bộ 2 chiều:
       * **Cách 1 - Theo tỉ lệ %**: Thanh trượt `0% - 100%`.
       * **Cách 2 - Theo tổng số tiết / bài**: Có ô chọn đơn vị (`Theo số tiết dạy bài mới` / `Theo số bài dạy bài mới`) và ô nhập số lượng trực tiếp (`#nlsCountInput`).
     + Người dùng có thể kéo thanh trượt % hoặc nhập trực tiếp số tiết (ví dụ nhập `36` tiết) -> hệ thống tự quy đổi % và tự động tích chọn các bài tương ứng trong bảng PPCT.
   - Trong thẻ **Trí tuệ nhân tạo (QĐ 2422)**:
     + Tương tự, đặt bộ chọn đơn vị (`#aiUnit`) và ô nhập số lượng trực tiếp (`#aiCountInput`) ngay dưới tiêu đề thẻ AI, liên kết 2 chiều với thanh trượt `#aiRate`.
2. **Dọn dẹp thẻ phụ thừa ở cuối trang**:
   - Xóa bỏ `<section class="card p-4" aria-label="Phân bổ linh hoạt NLS và AI">` ở cuối trang (dòng 73) sau Mục 7 để giao diện gọn gàng, tránh trùng lặp id.
3. **Đồng bộ trên cả 2 tệp giao diện**:
   - `canvas_xaydungphuluc.html`
   - `xaydungphuluc.html`
   - `backupcode viettailieu/canvas_xaydungphuluc.html` (nếu cần tương thích)

---

## Phạm vi thực hiện

1. **`canvas_xaydungphuluc.html`**:
   - Chuyển cụm `#nlsUnit`, `#nlsCountInput`, `#aiUnit`, `#aiCountInput` từ dòng 73 vào trong thẻ NLS và AI ở Mục 1 (dòng 64).
   - Thiết kế giao diện nhỏ gọn, hài hòa (dạng inline flex: Dropdown đơn vị + Input số tiết nằm cạnh nhau ngay trên thanh trượt).
   - Xóa bỏ section thừa ở dòng 73.
2. **`xaydungphuluc.html`**:
   - Đảm bảo cụm `#nlsUnit`, `#nlsCountInput`, `#aiUnit`, `#aiCountInput` được bố trí đẹp mắt, trực quan và đồng bộ.
3. **Smoke test**:
   - Chạy `tests/canvas-xaydungphuluc-smoke.js` và `tests/xaydungphuluc-smoke.js` để đảm bảo tất cả các selector và luồng đồng bộ 2 chiều đạt PASS.

---

## Ngoài phạm vi

- Không thay đổi thuật toán gợi ý mã NLS/AI.
- Không thay đổi cấu trúc bảng PPCT hay xuất file Word.

---

## File dự kiến tác động

1. `canvas_xaydungphuluc.html`
2. `xaydungphuluc.html`
3. `tests/canvas-xaydungphuluc-smoke.js`

---

## Các bước thực hiện

### Bước 1: Điều chỉnh HTML trong `canvas_xaydungphuluc.html`
- Tại Mục 1, thẻ NLS:
  ```html
  <div class="flex justify-between items-center">
    <label><input id="nlsEnabled" type="checkbox" checked onchange="onNlsEnabledChange(this.checked)"> <b>Năng lực số (CV 3456 / TT 02)</b></label>
    <output id="nlsRateOut">50%</output>
  </div>
  <div class="flex gap-2 items-center mt-2 mb-1">
    <select id="nlsUnit" class="field text-xs py-1 px-2 w-auto" onchange="onNlsUnitChange(this.value)">
      <option value="period" selected>Theo số tiết dạy bài mới</option>
      <option value="lesson">Theo số bài dạy bài mới</option>
    </select>
    <input id="nlsCountInput" type="number" min="0" class="field text-xs py-0.5 px-1.5 w-16 text-center" onchange="syncNlsSelectionFromCount(this.value)" aria-label="Số tiết hoặc bài NLS">
    <span class="text-xs opacity-70">hoặc kéo tỉ lệ % bên dưới:</span>
  </div>
  <input id="nlsRate" class="w-full" type="range" min="0" max="100" value="50" oninput="syncNlsSelectionFromRate()">
  ```
- Tương tự cho thẻ AI:
  ```html
  <div class="flex justify-between items-center">
    <label><input id="aiEnabled" type="checkbox" checked onchange="onAiEnabledChange(this.checked)"> <b>Trí tuệ nhân tạo (QĐ 2422)</b></label>
    <output id="aiRateOut">30%</output>
  </div>
  <div class="flex gap-2 items-center mt-2 mb-1">
    <select id="aiUnit" class="field text-xs py-1 px-2 w-auto" onchange="onAiUnitChange(this.value)">
      <option value="period" selected>Theo số tiết dạy bài mới</option>
      <option value="lesson">Theo số bài dạy bài mới</option>
    </select>
    <input id="aiCountInput" type="number" min="0" class="field text-xs py-0.5 px-1.5 w-16 text-center" onchange="syncAiSelectionFromCount(this.value)" aria-label="Số tiết hoặc bài AI">
    <span class="text-xs opacity-70">hoặc kéo tỉ lệ % bên dưới:</span>
  </div>
  <input id="aiRate" class="w-full" type="range" min="0" max="100" value="30" oninput="syncAiSelectionFromRate()">
  ```
- Xóa `<section class="card p-4" aria-label="Phân bổ linh hoạt NLS và AI">` ở cuối trang.

### Bước 2: Kiểm tra liên kết sự kiện trong JS
- Đảm bảo các hàm `onNlsUnitChange`, `syncNlsSelectionFromCount`, `syncNlsSelectionFromRate`, `onAiUnitChange`, `syncAiSelectionFromCount`, `syncAiSelectionFromRate` hoạt động đồng bộ hai chiều chính xác.

### Bước 3: Chạy test tự động
- Chạy:
  - `node tests/canvas-xaydungphuluc-smoke.js`
  - `node tests/xaydungphuluc-smoke.js`

---

## Tiêu chí nghiệm thu

1. Tại Mục 1 trên giao diện Xây dựng phụ lục, cả 2 thẻ NLS và AI đều hiển thị đầy đủ 2 hướng cấu hình:
   - Nhập trực tiếp **Tổng số tiết** (hoặc số bài).
   - Kéo thanh trượt **Tỉ lệ %**.
2. Nhập số tiết thì thanh trượt % tự động nhảy theo; kéo thanh trượt % thì ô số tiết tự động cập nhật số lượng tương ứng.
3. Không còn thẻ thừa ở cuối trang.
4. Toàn bộ các bộ test đạt **PASS 100%**.
