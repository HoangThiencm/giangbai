# PLAN: Thu gọn khung nhìn Thời khóa biểu & Sửa lỗi AI nhận diện lệch tiết Buổi chiều

## Hiện trạng

### 1. Vấn đề 1: Khung nhìn Thời khoá biểu bị tràn dọc, phải trượt con lăn chuột liên tục
- Khi vào tab "2. Thời khoá biểu GV" (`#view-timetable`), giao diện bị tràn dọc:
  - Khối nhập liệu / upload TKB `#tt-dropzone` và các input cấu hình ở trên cùng chiếm ~230px cố định.
  - Hai bảng Buổi sáng (`#tt-morning-wrap`) và Buổi chiều (`#tt-afternoon-wrap`) xếp chồng theo chiều dọc (stacked). Mỗi bảng cao ~250px-300px do chiều cao ô lớn (`min-height: 44px`), padding dày (`4px`) và tiêu đề `<h4>`.
  - Tổng chiều cao lên tới hơn 900px, khiến màn hình máy tính thông thường (chiều cao hữu dụng 600px - 800px) không thể nhìn thấy trọn vẹn cả sáng và chiều, buộc phải dùng con lăn chuột cuộn lên cuộn xuống.

### 2. Vấn đề 2: Cấu hình tiết chiều là 7–9 nhưng AI nhận diện thành 6–8
- **Hiện tượng**:
  - Người dùng cấu hình trong Khung tiết buổi học: Sáng `1-4`, Chiều `7-9`.
  - Trong ảnh TKB gửi giáo viên (ví dụ môn Toán của trường), bảng chỉ có các cột `THỨ 2 ... THỨ 7` và các hàng bài dạy, **hoàn toàn không có cột số Tiết** ở bên trái.
  - Buổi chiều có 3 hàng bài dạy (hàng 1: Toán 96, Toán 97, Toán 66; hàng 2: Toán 66, Toán 96, Toán 95; hàng 3: Toán 66, Toán 97). Lẽ ra 3 hàng này phải ứng với **Tiết 7, Tiết 8, Tiết 9**.
  - Nhưng khi bấm "AI nhận diện TKB", hệ thống lại hiển thị thành **Tiết 6, Tiết 7, Tiết 8** (và xuất hiện thêm một Tiết 6 không tồn tại trong cấu hình trường, còn Tiết 9 thì bị bỏ trống).
- **Nguyên nhân cốt lõi**:
  1. Trong hàm `scanTimetableWithAI()`: Prompt gửi sang Gemini không hề truyền thông tin cấu hình khung tiết của trường (`getSessionPeriods('morning')` và `getSessionPeriods('afternoon')`).
  2. Do ảnh TKB không in số tiết, Gemini tự suy đoán theo quy ước thông thường (chiều bắt đầu từ tiết 6), nên gán 3 hàng chiều thành keys `"6"`, `"7"`, `"8"`.
  3. Trong hàm `applyAiTimetableResult(raw)`: Hệ thống chỉ gán thô `next[session][day][String(period)] = parsed` mà không có bước chuẩn hóa (normalize / align) số tiết theo `getSessionPeriods(session)`.
  4. Hàm `periodsForTimetableSession('afternoon')` lấy hợp (union) giữa cấu hình `[7, 8, 9]` và các tiết xuất hiện trong dữ liệu `[6, 7, 8]`, tạo thành danh sách `[6, 7, 8, 9]` và đẩy các bài dạy vào tiết 6, 7, 8 sai lệch so với thực tế.

---

## Mục tiêu & Giải pháp thiết kế

### 1. Thu gọn khung nhìn Thời khóa biểu (Không cần trượt con lăn chuột)
1. **Collapsible Box cho cụm upload & cấu hình (`<details>`)**:
   - Đưa form Năm học/Học kỳ, `#tt-dropzone` và nút `#btn-ai-scan-tt` vào thẻ `<details class="tt-import-card" id="tt-import-details">` với thanh `<summary>` tinh gọn (~28px).
   - Tự động mở khi người dùng dán ảnh (Ctrl+V) hoặc kéo thả file ảnh vào. Khi đã có TKB hoặc khi xem, khối này thu gọn giúp tiết kiệm ngay ~200px chiều cao.
2. **Bố trí 2 cột Buổi sáng & Buổi chiều song song (Dual-column layout)**:
   - Dùng CSS Grid `.tt-sessions-container`:
     - Desktop / Laptop (>= 1024px): Cột trái là Buổi sáng, cột phải là Buổi chiều.
     - Màn hình nhỏ (< 1024px): Tự động co về 1 cột dọc (responsive).
     - Chiều cao dọc của toàn bộ 2 bảng giảm 50% (chỉ bằng chiều cao 1 bảng ~160px - 180px).
3. **Thu gọn kích thước ô bảng TKB (`.tt-grid`, `.tt-cell`)**:
   - `table-layout: fixed`, padding ô `th, td` giảm còn `2px 2px`.
   - Cột Tiết thu gọn `min-width: 44px`, font `0.68rem`.
   - Nút ô môn học `.tt-cell`: `min-height: 26px - 28px`, font `0.68rem`, `line-height: 1.1`.
   - Ô trống `.tt-cell.empty`: `min-height: 22px`, font `0.62rem`.
   - Tiêu đề buổi `.tt-session-title`: Nhỏ gọn kèm icon mặt trời/mặt trăng.
   - `#tt-right-panel`: padding giảm xuống `10px 14px 12px`, `gap: 8px`.
   - Toàn bộ giao diện TKB gói gọn trong ~300px - 320px chiều cao, vừa khít màn hình máy tính không cần cuộn chuột.

### 2. Sửa lỗi AI nhận diện lệch tiết Buổi chiều
1. **Truyền cấu hình khung tiết vào Prompt gửi Gemini**:
   - Lấy `mPeriods = getSessionPeriods('morning')` (ví dụ `[1, 2, 3, 4]`) và `aPeriods = getSessionPeriods('afternoon')` (ví dụ `[7, 8, 9]`).
   - Bổ sung chỉ thị nghiêm ngặt vào Prompt:
     + Khung tiết thực tế của trường: Sáng gồm các tiết `${mPeriods.join(', ')}`, Chiều gồm các tiết `${aPeriods.join(', ')}`.
     + Bắt buộc key của các tiết trong `morning` phải là một trong các số `${mPeriods.join(', ')}`.
     + Bắt buộc key của các tiết trong `afternoon` phải là một trong các số `${aPeriods.join(', ')}`.
     + Nếu ảnh không có số tiết hoặc chỉ có các hàng, BẮT BUỘC map lần lượt các hàng từ trên xuống dưới theo đúng danh sách tiết trên (Buổi chiều hàng 1 là tiết `${aPeriods[0]}`, hàng 2 là tiết `${aPeriods[1]}`..., TUYỆT ĐỐI KHÔNG tự ý đánh số tiết 6 nếu trường cấu hình bắt đầu từ tiết `${aPeriods[0]}`).
2. **Bộ chuẩn hóa và tự động căn chỉnh số tiết (Period Alignment Fallback) trong `applyAiTimetableResult`**:
   - Trước khi lưu các tiết của buổi vào `next[session]`:
     + Lấy `configured = getSessionPeriods(session)`.
     + Thu thập các số tiết thực tế xuất hiện trong kết quả AI của buổi đó: `aiPeriods = [k1, k2, ...]`.
     + Nếu các tiết AI trả về bị lệch khỏi `configured` (ví dụ AI trả `[6, 7, 8]` hoặc `[1, 2, 3]` trong khi cấu hình chiều là `[7, 8, 9]`):
       * Sắp xếp các tiết AI theo thứ tự tăng dần.
       * Ánh xạ tuần tự `aiPeriods[i]` sang `configured[i]`.
       * Ví dụ: Tiết 6 -> Tiết 7, Tiết 7 -> Tiết 8, Tiết 8 -> Tiết 9.
     + Nhờ đó, dù AI có trả về thứ tự hàng tương đối (1, 2, 3) hay giả định mặc định (6, 7, 8), hệ thống luôn chuyển đổi chuẩn xác 100% về khung tiết của trường (`7, 8, 9`).

---

## Phạm vi thực hiện

1. **`phancongtochuyenmon.html`**:
   - CSS: Bổ sung style cho `.tt-import-card`, `.tt-import-summary`, `.tt-import-badge`, `.tt-import-body`, `.tt-sessions-container`, `.tt-session-col`, `.tt-session-title`, `.tt-grid`, `.tt-cell`.
   - HTML: Bọc cụm nhập ảnh trong `<details id="tt-import-details">`, bọc 2 bảng sáng/chiều vào `.tt-sessions-container`.
   - JS `scanTimetableWithAI()`: Truyền khung tiết `mPeriods` và `aPeriods` vào prompt AI với quy tắc map hàng nghiêm ngặt.
   - JS `applyAiTimetableResult()`: Bổ sung logic Period Alignment mapping số tiết AI về đúng khung tiết `getSessionPeriods(session)`.
   - JS `setTimetablePreview()` & `bindTimetableInputEvents()`: Tự động mở `<details id="tt-import-details">` khi dán hoặc kéo thả ảnh.
2. **`tests/timetable-render-smoke.js`**:
   - Bổ sung test kiểm tra:
     + Bố cục 2 cột `.tt-sessions-container` và khối `<details id="tt-import-details">`.
     + Test Period Alignment: Cấu hình chiều `[7, 8, 9]`, AI trả về `"6"`, `"7"`, `"8"` -> `applyAiTimetableResult` tự động đưa về `"7"`, `"8"`, `"9"`, không sinh ra tiết 6.

---

## Ngoài phạm vi

- Không thay đổi các module Báo giảng, Phân công chuyên môn, Quản lý chấm công.
- Giữ nguyên cấu trúc dữ liệu lưu CSDL và LocalStorage.

---

## File dự kiến tác động

1. `phancongtochuyenmon.html`
2. `tests/timetable-render-smoke.js`

---

## Các bước thực hiện

### Bước 1: Cập nhật CSS và HTML thu gọn giao diện TKB trong `phancongtochuyenmon.html`
1. Thay đổi `#tt-right-panel` CSS: `padding: 10px 14px 14px; gap: 8px;`.
2. Thêm CSS cho khối import thu gọn:
   - `.tt-import-card { border: 1px solid #e2e8f0; border-radius: 8px; background: #ffffff; padding: 4px 10px; }`
   - `.tt-import-summary { cursor: pointer; font-size: 0.78rem; font-weight: 700; color: #4338ca; display: flex; justify-content: space-between; align-items: center; padding: 4px 0; user-select: none; }`
   - `.tt-import-badge { font-size: 0.68rem; color: #64748b; font-weight: normal; }`
   - `.tt-import-body { padding-top: 8px; border-top: 1px solid #f1f5f9; margin-top: 4px; }`
3. Thêm CSS cho bố cục 2 cột và bảng compact:
   - `.tt-sessions-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: start; }`
   - `@media (max-width: 1024px) { .tt-sessions-container { grid-template-columns: 1fr; } }`
   - `.tt-session-col { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }`
   - `.tt-session-title { font-size: 0.78rem; font-weight: 800; color: #1e293b; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }`
   - `.tt-grid { width: 100%; border-collapse: collapse; font-size: 0.68rem; table-layout: fixed; }`
   - `.tt-grid th, .tt-grid td { border: 1px solid #e2e8f0; padding: 2px; text-align: center; }`
   - `.tt-grid th { background: #f8fafc; font-weight: 800; color: #334155; padding: 2px 1px; font-size: 0.68rem; line-height: 1.1; }`
   - `.tt-grid th:first-child, .tt-grid tbody th { min-width: 44px; width: 44px; padding: 2px 3px; font-size: 0.66rem; }`
   - `.tt-cell { min-height: 26px; width: 100%; border: none; background: #eef2ff; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 0.68rem; font-weight: 700; color: #312e81; padding: 2px 1px; line-height: 1.1; display: flex; flex-direction: column; justify-content: center; align-items: center; }`
   - `.tt-cell.empty { background: #fafafa; color: #94a3b8; font-weight: 500; font-size: 0.62rem; min-height: 22px; }`
4. Cập nhật DOM `<main id="tt-right-panel">`:
   - Bọc cụm `form-grid`, `#tt-dropzone`, `#btn-ai-scan-tt` vào `<details class="tt-import-card" id="tt-import-details">`.
   - Đặt `#tt-morning-wrap` và `#tt-afternoon-wrap` vào `.tt-sessions-container` với 2 cột `.tt-session-col`.

### Bước 2: Cập nhật `scanTimetableWithAI` và `applyAiTimetableResult` trong `phancongtochuyenmon.html`
1. Trong `scanTimetableWithAI()`:
   - Đọc `const mPeriods = getSessionPeriods('morning');` và `const aPeriods = getSessionPeriods('afternoon');`.
   - Đưa danh sách tiết này vào prompt gửi Gemini, yêu cầu bắt buộc dùng các số tiết này và map thứ tự hàng tương ứng nếu ảnh không có số tiết.
2. Trong `applyAiTimetableResult(raw)`:
   - Bổ sung hàm ánh xạ số tiết `alignSessionPeriods(srcSessionObj, configuredPeriods)`:
     + Lấy tập hợp các key tiết từ `srcSessionObj` (ví dụ: `["6", "7", "8"]` hoặc `["1", "2", "3"]`).
     + Nếu tập hợp này không khớp với `configuredPeriods` (ví dụ `[7, 8, 9]`):
       * Sắp xếp tăng dần và tạo bản đồ ánh xạ `map[oldKey] = configuredPeriods[idx]`.
       * Chuyển đổi dữ liệu của từng ngày theo bản đồ ánh xạ mới.
     + Nếu đã khớp: Giữ nguyên.

### Bước 3: Cập nhật và chạy smoke test
- Bổ sung test kiểm tra:
  + Cấu trúc `.tt-sessions-container` và `#tt-import-details`.
  + Khả năng tự động căn chỉnh số tiết chiều từ 6–8 về 7–9 khi cấu hình chiều là 7–9.
- Chạy:
  - `node tests/baogiang-weekday-segment-smoke.js`
  - `node tests/timetable-render-smoke.js`
  - `node tests/auto-reload-smoke.js`

---

## Rủi ro & Giải pháp kiểm soát

- **Rủi ro**: Khi ảnh TKB có sẵn cột số tiết (ví dụ đã in rõ Tiết 7, Tiết 8, Tiết 9) thì ánh xạ có làm sai lệch không?
  - *Kiểm soát*: Nếu các key AI trả về đã trùng khớp với `configuredPeriods`, thuật toán giữ nguyên 100%, không thực hiện ánh xạ lại.
- **Rủi ro**: Giáo viên dạy số tiết ít hơn khung cấu hình (ví dụ chỉ dạy 2 tiết chiều).
  - *Kiểm soát*: Ánh xạ tuần tự theo chỉ số từ tiết bắt đầu của buổi học (tiết 7, tiết 8), không làm mất dữ liệu.

---

## Tiêu chí nghiệm thu

1. Cả Buổi sáng và Buổi chiều hiển thị song song 2 cột trên cùng màn hình máy tính, xem trọn vẹn từ tiết 1 đến tiết cuối cùng mà không cần trượt con lăn chuột.
2. Khi trường cấu hình chiều `7-9`, nhận diện ảnh TKB (kể cả ảnh không có cột số tiết) tự động đưa vào đúng **Tiết 7, Tiết 8, Tiết 9**, hoàn toàn không bị gán vào Tiết 6.
3. Khối nhập ảnh TKB thu gọn dưới dạng `<details>`, tự động mở khi dán hoặc kéo thả ảnh.
4. Toàn bộ các bộ test tự động đạt **PASS 100%**.
