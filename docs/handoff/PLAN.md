# PLAN: Khắc phục lỗi thẩm định Năng lực số (CV 3456) khi chọn đơn vị "Theo tổng số tiết PPCT"

## 1. Hiện trạng & Nguyên nhân lỗi

### Phản ánh của người dùng
- Người dùng chọn Năng lực số (CV 3456 / TT 02) theo đơn vị **"Theo tổng số tiết PPCT"** với tỉ lệ ~20% - 21% (29 tiết / 140 tiết PPCT, bao gồm 15 hoặc 16 bài học).
- Tuy nhiên, khi xem **Báo cáo thẩm định (Báo cáo đối chiếu chuẩn)**, hệ thống lại báo:
  - `Năng lực số | CV 3456/BGDĐT-GDTrH · TT 02/2024 | 16/87 bài, mục tiêu 19 | Chưa đạt` (màu đỏ).
  - Khiến toàn bộ bảng thẩm định kết luận: `CẦN HOÀN THIỆN TRƯỚC KHI SỬ DỤNG`.

### Nguyên nhân kỹ thuật (Root Cause)
1. Trong hàm `calculateComplianceReport` ở cả `canvas_xaydungphuluc.html` và `xaydungphuluc.html`:
   - Hàm này **luôn tính mục tiêu NLS theo số BÀI HỌC**:
     ```javascript
     nlsTarget = c.nls?.enabled ? Math.ceil(rows.length * (Number(c.nls.rate) || 0) / 100) : 0;
     ```
     Trong đó: `rows.length` là tổng số bài học (87 bài), còn `c.nls.rate` là tỉ lệ phần trăm người dùng chọn trên thanh trượt (21%).
     Hệ thống tính: `Math.ceil(87 * 21 / 100) = 19 bài`.
   - Trong khi đó, người dùng đang cấu hình `c.nls.unit = 'period'` ("Theo tổng số tiết PPCT"). Mục tiêu của người dùng là **21% số TIẾT** (29 tiết / 140 tiết).
   - Vì 29 tiết chỉ nằm trong 15 hoặc 16 bài học, nên số bài có mã NLS thực tế là 16 bài.
   - Hàm thẩm định lại so sánh số bài (16 bài) với mục tiêu 19 bài (`16 < 19`), dẫn đến kết luận sai lệch là `Chưa đạt`!

---

## 2. Giải pháp kỹ thuật

### Đồng bộ hóa thẩm định NLS theo đúng đơn vị cấu hình (`c.nls.unit`)
Trong hàm `calculateComplianceReport` (cả `canvas_xaydungphuluc.html` và `xaydungphuluc.html`):
1. **Nhận diện đơn vị cấu hình**:
   - `const isPeriodUnit = c.nls?.unit === 'period';`
2. **Tính toán số liệu thực tế**:
   - Số bài tích hợp NLS: `nlsRows` (đếm các hàng có mã NLS).
   - Số tiết tích hợp NLS:
     ```javascript
     const nlsPeriods = rows.filter(isNlsRow).reduce((sum, row) => sum + (parsePeriodCount((row.cells || [])[2]) || 0), 0);
     ```
3. **Tính mục tiêu & điều kiện Đạt (`pass`)**:
   - **Nếu `isPeriodUnit` (Theo tổng số tiết PPCT)**:
     - Mục tiêu số tiết: `nlsPeriodTarget = Math.round(periods * (Number(c.nls.rate) || 0) / 100);`
     - Chi tiết hiển thị: `${nlsPeriods}/${periods} tiết (${nlsRows}/${rows.length} bài), mục tiêu ${nlsPeriodTarget} tiết`
     - Điều kiện Đạt: `nlsPeriods >= nlsPeriodTarget || Math.abs(nlsPeriods - nlsPeriodTarget) <= 1` (do tính chất nguyên khối của bài học).
   - **Nếu `c.nls?.unit === 'lesson'` (Theo tổng số bài PPCT)**:
     - Mục tiêu số bài: `nlsLessonTarget = Math.ceil(rows.length * (Number(c.nls.rate) || 0) / 100);`
     - Chi tiết hiển thị: `${nlsRows}/${rows.length} bài, mục tiêu ${nlsLessonTarget} bài`
     - Điều kiện Đạt: `nlsRows >= nlsLessonTarget`.

---

## 3. Phạm vi tệp tin thay đổi

1. `canvas_xaydungphuluc.html`:
   - Cập nhật hàm `calculateComplianceReport`: phân định rõ cách tính mục tiêu và đánh giá Đạt/Chưa đạt theo `c.nls?.unit` ('period' vs 'lesson').
2. `xaydungphuluc.html`:
   - Đồng bộ logic tương tự vào `calculateComplianceReport`.
3. `tests/canvas-xaydungphuluc-smoke.js` & `tests/xaydungphuluc-smoke.js`:
   - Bổ sung test case kiểm tra báo cáo thẩm định NLS khi `unit: 'period'` và `rate: 20` đạt chuẩn chính xác theo số tiết mà không bị đánh trượt theo số bài.

---

## 4. Kế hoạch kiểm thử (Verification Plan)

1. `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
2. `node tests/xaydungphuluc-smoke.js`: PASS.
3. `node tests/daythay-suggest-smoke.js`: PASS.
4. `node tests/baogiang-weekday-segment-smoke.js`: PASS.
5. `node tests/timetable-render-smoke.js`: PASS.
6. `node tests/auto-reload-smoke.js`: PASS.
7. `git diff --check`: PASS (không lỗi khoảng trắng hay cú pháp).
