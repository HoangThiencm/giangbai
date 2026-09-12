# PLAN: Khắc phục lỗi Gợi ý tích hợp & Thẩm định NLS chưa đạt & Nâng cấp Canvas mở rộng

## PHẦN A: Khắc phục triệt để lỗi gợi ý cả NLS và AI trên bài 1 tiết & Thẩm định NLS chưa đạt (22/140 tiết)

### 1. Hiện trạng & Nguyên nhân gốc rễ (Root Cause)
- **Hiện tượng người dùng phản ánh qua ảnh chụp**:
  1. Trong bảng chọn bài học (Mục 1 / `aiPickerRows`), các **bài 1 tiết** (ví dụ: *Bài 1. Tập hợp*, *Bài 2. Cách ghi số tự nhiên*, *Bài 3. Thứ tự trong tập hợp*, *Bài 4. Phép cộng và phép trừ*) đang bị hệ thống gợi ý **tích chọn cả hai cột**:
     - Cột *Tích hợp NLS*: `[x] Tích hợp NLS` (được tích).
     - Cột *Tích hợp AI*: `[x] Cả bài` / `[x] Tiết 1` (cũng được tích).
  2. Sự mâu thuẫn này dẫn trực tiếp đến lỗi Thẩm định:
     - Giao diện Mục 1 đếm đủ **28 tiết NLS** (do đếm theo checkbox đã tích).
     - Nhưng khi render bảng Phụ lục 1, hàm `selectedIntegration` áp dụng đúng quy tắc sư phạm đã thống nhất:
       `Bài 1 tiết có AI → 0 mã NLS, chỉ có 1 mã AI` (`if (p <= 1) return hasAi ? 0 : 1;`).
     - Vì vậy, 6 bài 1 tiết có AI này bị **xóa mã NLS** trong bảng Phụ lục 1, thực tế chỉ còn **22 tiết NLS** (13 bài).
     - Báo cáo Thẩm định (`calculateComplianceReport`) đếm các dòng thực tế có mã NLS trong bảng Phụ lục 1 thì chỉ thấy **22/140 tiết (mục tiêu 28 tiết)** -> Báo **Chưa đạt**!

- **Nguyên nhân kỹ thuật**:
  1. Thuật toán tự động gợi ý chọn bài NLS (`chooseNlsLessonsForPeriods` / `syncNlsSelectionFromRate`) và AI (`prioritizedAiPeriods` / `syncAiSelectionFromRate`) đang chạy **hoàn toàn độc lập**. Khi người dùng kéo thanh tỉ lệ (hoặc mở trang mẫu), cả hai hàm cùng ưu tiên các bài học đầu tiên (các bài 1 tiết của Chương I) mà không có cơ chế **loại trừ lẫn nhau (mutual exclusion)** đối với bài 1 tiết.
  2. Các hàm tương tác checkbox (`toggleNlsLesson`, `toggleAiLesson`, `toggleAiLessonRow`) chưa có logic ràng buộc loại trừ cho bài 1 tiết: khi người dùng hoặc hệ thống tích chọn AI cho bài 1 tiết thì chưa tự động hủy chọn NLS của bài đó, và ngược lại.

---

### 2. Giải pháp kỹ thuật khắc phục triệt để
Áp dụng trên cả 2 tệp: `canvas_xaydungphuluc.html` và `xaydungphuluc.html`:

1. **Nguyên tắc loại trừ lẫn nhau (Mutual Exclusion) cho bài 1 tiết khi gợi ý tự động**:
   - Khi gợi ý NLS (`chooseNlsLessonsForPeriods` / `syncNlsSelectionFromRate`):
     - Duyệt danh sách bài học ưu tiên, nếu gặp bài 1 tiết mà **đã được chọn tiết AI** (`selectedPeriodsForLesson(lesson.id).length > 0`) -> **Bỏ qua không chọn NLS cho bài đó**, tiếp tục chọn các bài khác (bài từ 2 tiết trở lên, hoặc bài 1 tiết chưa có AI) cho đến khi đạt đủ mục tiêu `target` số tiết NLS (đủ 28 tiết).
   - Khi gợi ý AI (`prioritizedAiPeriods` / `syncAiSelectionFromRate`):
     - Nếu bài 1 tiết đã được chọn NLS -> không tự động chọn AI cho bài đó (ưu tiên bài từ 2 tiết hoặc bài 1 tiết chưa có NLS).

2. **Ràng buộc loại trừ tức thì trên giao diện (Interactive Checkboxes)**:
   - Trong `toggleNlsLesson(lessonId, checked)`:
     - Nếu `checked = true` và bài đó là bài 1 tiết: Tự động bỏ chọn tất cả tiết AI của bài đó trong `aiSelectedLessonIds` (`toggleAiLessonRow(lessonId, false)`).
   - Trong `toggleAiLesson(periodId, checked)` và `toggleAiLessonRow(lessonId, checked)`:
     - Nếu `checked = true` và bài đó là bài 1 tiết: Tự động bỏ chọn NLS của bài đó trong `nlsSelectedLessonIds` (`nlsSelectedLessonIds.delete(lessonId)`).
   - Cập nhật lại thanh trượt tỉ lệ và số lượng hiển thị tức thì.

3. **Kết quả đạt được**:
   - Trên bảng giao diện Mục 1: **Tuyệt đối không có bài 1 tiết nào bị tích cả NLS lẫn AI**.
   - Mục tiêu 28 tiết NLS sẽ được phân bổ chính xác vào 28 tiết thực tế (các bài >= 2 tiết hoặc bài 1 tiết không có AI).
   - Bảng Phụ lục 1 xuất ra đủ đúng 28 tiết có mã NLS.
   - Báo cáo Thẩm định Sư phạm đếm đúng **28/140 tiết (Đạt 100%)**.

---

## PHẦN B: Nâng cấp các công cụ trong "backupcode viettailieu" chạy môi trường Gemini Canvas mở rộng

### 1. Mục tiêu
- **Tối ưu hiển thị mở rộng (Full-width / Expanded Canvas Mode)**: Tự động co giãn phủ rộng toàn màn hình (`w-full max-w-[98%] 2xl:max-w-[1750px] mx-auto`), không bị đóng khung hẹp cố định (`max-w-7xl` ~ 1280px hay `1440px`), tận dụng tối đa không gian khi người dùng nhấn nút mở rộng/toàn màn hình trong Gemini Canvas.
- **Tương thích tuyệt đối Sandbox Iframe của Gemini Canvas**:
  - Chống FOUC / màn hình trắng (Force visible styles & MutationObserver).
  - An toàn CSP: Tránh lỗi chặn Worker (PDF.js worker), tránh chặn popup (`window.confirm`/`alert`).
  - Hộp thoại tương tác DOM (`canvasConfirm`) thay cho `confirm()` vốn bị browser sandbox chặn.
  - Lưu trữ an toàn (`canvasStorage`) có bộ nhớ tạm in-memory khi `localStorage` bị hạn chế quyền truy cập.
  - Banner trạng thái kết nối Gemini Canvas (`canvasHostBanner`).
  - Nút chuyển giao diện "Gọn" (`toggleCompactMode`) để xem được nhiều nội dung hơn trên màn hình Canvas.

### 2. Danh mục tệp tin & Nội dung triển khai
1. `canvas_xaydungphuluc.html` & `xaydungphuluc.html`: Áp dụng bản vá Phần A (chọn bài NLS bù trừ thông minh chống hụt tiết).
2. `backupcode viettailieu/canvas_soankhbd.html`: Mở rộng layout `.app-body`, bổ sung `canvasConfirm` và xử lý an toàn sandbox.
3. `backupcode viettailieu/soanbaigemini.html`: Mở rộng layout `max-w-[98%]`, thêm banner canvas, anti-FOUC, `canvasConfirm`, `canvasStorage`.
4. `backupcode viettailieu/taobaitap.html`: Mở rộng layout 2 khối chính, thêm banner canvas, anti-FOUC.
5. `backupcode viettailieu/taobaocao.html`: Thêm banner canvas, mở rộng layout, anti-FOUC.
6. `backupcode viettailieu/sangkien.html`: Mở rộng layout container chính sang `max-w-[98%]`, thêm banner canvas, anti-FOUC.
7. `backupcode viettailieu/chuyenpdf.html`: Mở rộng `.app-shell` sang `max-w-[98%] 2xl:max-w-[1750px]`, thêm banner canvas, anti-FOUC.
*(Lưu ý giữ nguyên bản gốc `soanbaigemini_bakcup_khong đụng tới.html`).*

---

## 3. Kế hoạch kiểm thử (Verification Plan)

1. **Kiểm thử Thẩm định NLS (Phần A)**:
   - Chạy mô phỏng kiểm thử với cấu hình 140 tiết, 20% NLS (28 tiết), 9% AI (12 tiết).
   - Xác nhận bảng Phụ lục 1 xuất ra đủ 28 tiết có mã NLS, không bị hụt 6 tiết.
   - Xác nhận `calculateComplianceReport` trả về `pass: true` cho tiêu chí Năng lực số.
2. **Kiểm thử Canvas mở rộng (Phần B)**:
   - Tạo và chạy `tests/backupcode-canvas-smoke.js` kiểm tra toàn bộ 6 tệp trong `backupcode viettailieu`: cú pháp hợp lệ, container mở rộng, anti-FOUC và banner canvas.
3. **Hồi quy hệ thống**:
   - `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
   - `node tests/xaydungphuluc-smoke.js`: PASS.
   - `node tests/xaydungphuluc-math-smoke.js`: PASS.
   - `node tests/sgk-knowledge-smoke.js`: PASS.

