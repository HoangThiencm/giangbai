# IMPLEMENT: Khóa cố định mốc Ngày bắt đầu áp dụng (Tuần 1) trong Lịch báo giảng

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `phancongtochuyenmon.html`
  - Bổ sung `start_date_locked`; dữ liệu đã có ngày Tuần 1 hợp lệ tự được khóa khi nạp, còn dữ liệu chưa có ngày không tự lấy ngày hiện tại.
  - Nhãn đổi thành “Ngày bắt đầu áp dụng (Tuần 1)”, có badge Chưa thiết lập / Đang mở khóa / Đã khóa và nút Mở khóa sửa / Khóa lại.
  - Khi khóa, ô ngày bị `disabled` và `readOnly`, có kiểu hiển thị không thể chỉnh sửa. DOM bị thay đổi bên ngoài cũng không thể ghi đè ngày đã khóa qua `updateBaoGiangSettings`.
  - Mở khóa yêu cầu xác nhận cảnh báo nghiêm ngặt; chọn một ngày hợp lệ sẽ lưu cục bộ, khóa lại ngay và thông báo rõ ràng. Có thể khóa lại ngày không đổi bằng nút riêng.
- `tests/baogiang-weekday-segment-smoke.js`
  - Kiểm thử hydrate dữ liệu cũ thành trạng thái khóa, kiểm tra ngày hợp lệ, bảo vệ khỏi DOM thay đổi, Cancel/OK khi mở khóa, tự khóa khi chọn ngày mới và khóa lại thủ công.

## Kiểm tra đã chạy

- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `node tests/auto-reload-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần `/verify` trực quan: mở tab Lịch báo giảng, thử Cancel/OK ở Mở khóa sửa và chọn ngày mới.

---

# IMPLEMENT: Khắc phục Canvas Xây dựng Phụ lục trắng trang trong Gemini

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `canvas_xaydungphuluc.html`
  - Gỡ PDF.js và cấu hình PDF Worker từ xa; Canvas không còn tạo hoặc nạp Worker, phù hợp Content Security Policy của Gemini Canvas.
  - Khởi tạo giao diện chính không phụ thuộc thư viện xử lý tài liệu tùy chọn.
  - Khi chọn PDF, ứng dụng hiển thị thông báo rõ rằng Gemini Canvas không thể đọc PDF trực tiếp và hướng dẫn dùng DOCX/XLSX hoặc dán văn bản; không còn lỗi trắng trang hoặc crash.
  - Các đường đọc DOCX/XLSX kiểm tra sự hiện diện của thư viện tương ứng trước khi chạy và hiển thị thông báo phục hồi nếu CDN không tải được.
- `tests/canvas-xaydungphuluc-smoke.js`
  - Bổ sung kiểm thử không còn PDF.js, PDF Worker, `new Worker` hay `importScripts`.
  - Kiểm thử thông báo dự phòng PDF/DOCX/XLSX và xác nhận `initApp()` không phụ thuộc thư viện nhập tài liệu.

## Kiểm tra đã chạy

- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/sgk-knowledge-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần mở lại ứng dụng trong Gemini Canvas để xác nhận giao diện hiển thị trên môi trường thực tế.

---

# IMPLEMENT: Gỡ bỏ hoàn toàn cơ chế tự động refresh (Auto-Reload)

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `js/security-guard.js`
  - Xóa toàn bộ module Auto-Update Checker (biến `appVersionStorageKey`, `appVersionReloadAtKey`, `appVersionReloadDebounceMs`, `appVersionCheckInFlight`; hàm `getVersionValue`, `checkAppVersionUpdate`, `initAutoUpdateChecker`; lệnh gọi `initAutoUpdateChecker();`).
  - File không còn `fetch('/version.json')` và không còn tự gọi `window.location.reload()` khi focus, visibilitychange hoặc theo chu kỳ 60 giây.
  - Giữ nguyên các chức năng bảo vệ DevTools hiện có, gồm reload thủ công sau khi Admin nhập mã mở khóa.
- `tests/auto-reload-smoke.js`
  - Đổi kiểm thử sang xác nhận `js/security-guard.js` không còn `initAutoUpdateChecker` / `checkAppVersionUpdate`, không fetch `version.json`, và không tự reload khi nạp script hay khi có sự kiện focus/visibilitychange.

## Kiểm tra đã chạy

- `node tests/auto-reload-smoke.js`: PASS.
- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.

---

# IMPLEMENT: Khớp chính xác tên giáo viên khi AI nhận diện Thời khóa biểu

## Phạm vi đã triển khai

- `phancongtochuyenmon.html`
  - Thêm `matchTeacherByName(rawName, teachers, currentTeacherId)` và dùng hàm này trong `applyAiTimetableResult()`.
  - Chuẩn hóa/tách tên thành từng từ, bỏ tiền tố như “Giáo viên”, và chỉ xét giáo viên có từ cuối (tên chính) trùng khớp.
  - Ưu tiên giáo viên đang được chọn khi tên đầy đủ hoặc tên chính khớp; khớp tên đầy đủ chính xác; dùng số từ họ/đệm trùng để phân giải; trả về `null` khi vẫn mơ hồ.
  - Không còn so khớp chuỗi con, nên “Ánh” không thể bị gán nhầm sang “Hồ Đăng Danh”.
- `tests/timetable-render-smoke.js`
  - Bổ sung kiểm thử “Giáo viên: Ánh” → “Hoàng Xuân Ánh”, tên đầy đủ, giữ giáo viên đang chọn đúng tên chính, trường hợp mơ hồ và trường hợp không được khớp theo chuỗi con.

## Kiểm tra đã chạy

- `node Tests/timetable-render-smoke.js`: PASS.
- `node Tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node Tests/auto-reload-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.

---

# IMPLEMENT: Phân bổ NLS/AI theo tổng PPCT

## Phạm vi đã triển khai

- `xaydungphuluc.html` và `canvas_xaydungphuluc.html`
  - Đổi bộ chọn sang “Theo tổng số tiết PPCT” và “Theo tổng số bài PPCT” cho cả NLS lẫn AI.
  - Thay toàn bộ phần tóm tắt/số đếm bằng “tiết PPCT” và “bài PPCT”.
  - Viết lại Mục 4: AI đề xuất bài/tiết phù hợp từ PPCT và ngữ cảnh SGK; người dùng vẫn có thể rà soát, tick hoặc bỏ tick để điều chỉnh.
  - Gỡ toàn bộ wording ngụ ý giới hạn 12 tiết; không thay đổi thuật toán phân bổ, thứ tự ưu tiên hoặc các ID/handler điều khiển.
- `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`
  - Kiểm tra nhãn mới, không còn cụm “dạy bài mới”, tổng PPCT vẫn gồm dòng ôn tập/kiểm tra không phải tiêu đề, và hành vi ưu tiên gợi ý được giữ nguyên.

## Kiểm tra đã chạy

- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần chạy `/verify` để xác nhận các trang không còn tự refresh.

---

# IMPLEMENT: Giá trị mặc định thông tin đơn vị tại Xây dựng Phụ lục

## Phạm vi đã triển khai

- `xaydungphuluc.html` và `canvas_xaydungphuluc.html`
  - Đặt giá trị khởi tạo có thể chỉnh sửa cho Năm học `2026-2027`, Tên trường `THCS Trần Phú`, Tổ chuyên môn `Tổ Toán - Tin` và Giáo viên / Tổ trưởng `Hoàng Tấn Thiên`.
  - Giữ nguyên cơ chế bản nháp/storage; người dùng vẫn có thể nhập tay từng trường.
- `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`
  - Kiểm tra giá trị khởi tạo, tính chỉnh sửa, và việc `getConfig()` phản ánh thay đổi thủ công.

## Kiểm tra đã chạy

- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
