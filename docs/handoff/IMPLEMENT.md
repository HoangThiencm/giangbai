# IMPLEMENT: Đề xuất thông minh giáo viên dạy thay theo Thời khóa biểu

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `phancongtochuyenmon.html`
  - Bổ sung panel `#daythay-suggestion-panel` ngay dưới cụm chọn giáo viên; panel chỉ có hai cột: **Trống cả buổi** và **Có mặt, trống tiết cần thay**.
  - Thêm `computeDayThayTeacherAvailability(date, session, forTeacherId, neededPeriods)`: kiểm tra ngày hợp lệ Thứ 2–Thứ 7, loại giáo viên nghỉ, lấy tiết thực tế bằng `getTimetableDaySlots`, rồi phân loại trống cả buổi / trống các tiết cần thay / trùng lịch.
  - Thêm `renderDayThaySuggestions()` để lấy các tiết đang bật, xử lý thiếu dữ liệu hoặc Chủ nhật an toàn, ẩn gợi ý với Dạy bù, đồng thời ghi trạng thái rảnh/trùng lịch vào dropdown giáo viên thực dạy.
  - Bấm “Chọn dạy thay” tự điền dropdown, tô nổi thẻ đang chọn và báo toast xác nhận. ID được mã hóa khi gắn vào sự kiện chọn.
  - Đồng bộ gợi ý khi đổi ngày, buổi, giáo viên nghỉ, các tiết đã chọn, khi nạp lại dropdown, tạo/reset lưới tiết hoặc chuyển loại Dạy thay/Dạy bù. Không thay đổi dữ liệu lưu Sổ Dạy thay, báo cáo hay in thông báo.
- `tests/daythay-suggest-smoke.js`
  - Kiểm tra ba nhóm khả dụng từ TKB thực tế, loại trừ giáo viên nghỉ, xử lý Chủ nhật, chọn một chạm cập nhật dropdown/toast và cấu trúc panel hai cột/ẩn khi Dạy bù.

## Kiểm tra đã chạy

- `node tests/daythay-suggest-smoke.js`: PASS.
- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `node tests/auto-reload-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần `/verify` trực quan: chọn ngày có TKB, giáo viên nghỉ và các tiết cần thay; xác nhận hai cột cùng trạng thái dropdown khớp lịch thật.

---

# IMPLEMENT: Khôi phục JSON phản hồi AI an toàn cho Xây dựng Phụ lục

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `canvas_xaydungphuluc.html` và `xaydungphuluc.html`
  - Thêm cùng một hàm `safeParseAiJson(raw)`: ưu tiên `JSON.parse` nguyên bản, sau đó lấy đúng cấu trúc JSON ngoài cùng bằng bộ quét nhận biết chuỗi/escape.
  - Khi AI tạo ký tự điều khiển thô trong chuỗi, tự chuyển thành escape JSON hợp lệ; backslash LaTex đơn như `\alpha` cũng được giữ lại dưới dạng chuỗi thay vì làm lỗi parse.
  - Khôi phục được dấu phẩy thừa trước `}` hoặc `]`, nhưng không sửa dữ liệu nằm bên trong chuỗi JSON hợp lệ.
  - `readGeminiResponse` ở hai giao diện và `callMistral` ở giao diện thường đều dùng bộ đọc này. Prompt, schema và logic chuẩn hóa Phụ lục không thay đổi.
- `tests/canvas-xaydungphuluc-smoke.js`
  - Kiểm thử JSON chuẩn không bị thay đổi, newline/tab/ký tự điều khiển thô, prose + code fence, dấu phẩy thừa, backslash LaTex và lỗi không thể khôi phục.
  - Xác nhận hai giao diện dùng cùng implementation parser.

## Kiểm tra đã chạy

- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `node tests/auto-reload-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần `/verify` với một PPCT lớn trên cả Canvas và giao diện thường để xác nhận phản hồi AI thực tế được xử lý ổn định.

---

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

# IMPLEMENT: Tùy chọn Buổi dạy “Cả ngày” trong Sổ Dạy thay

## Phạm vi đã triển khai

- `phancongtochuyenmon.html`
  - Thêm lựa chọn `Cả ngày (Sáng & Chiều)` vào Buổi dạy; nhãn tự hiển thị hai khung tiết đã cấu hình.
  - Gộp/loại trùng khung tiết cho form; đồng thời lấy và sắp xếp toàn bộ tiết sáng/chiều từ TKB và đề xuất giáo viên khi chọn `all_day`.
  - Phân loại đúng giáo viên trống cả ngày, trống các tiết cần thay hoặc trùng lịch; tiêu đề và thẻ gợi ý hiển thị “Cả ngày”.
  - Khi lập thông báo, từng tiết của bản ghi cả ngày được ghi theo buổi thực tế (Sáng hoặc Chiều); lưu, sửa và các bảng/xuất sổ vẫn giữ giá trị `all_day`.
- `tests/daythay-suggest-smoke.js`
  - Kiểm tra lựa chọn giao diện, gộp khung tiết/TKB và phân loại độ khả dụng cho cả ngày.

## Kiểm tra đã chạy

- `node tests/daythay-suggest-smoke.js`: PASS.
- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/auto-reload-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.

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
