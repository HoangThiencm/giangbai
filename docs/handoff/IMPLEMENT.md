# IMPLEMENT: Loại trừ NLS/AI bài một tiết và hoàn thiện Canvas mở rộng

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `canvas_xaydungphuluc.html` và `xaydungphuluc.html`
  - Bài một tiết được loại trừ lẫn nhau ở cả gợi ý tự động và checkbox thủ công: chọn NLS sẽ bỏ AI; chọn AI sẽ bỏ NLS.
  - Chọn NLS theo số tiết chỉ nhận các bài hợp lệ; thuật toán chọn tổ hợp theo số tiết để bù đúng mục tiêu khi có thể, không còn hụt tiết do các bài một tiết đã có AI.
  - Chọn AI tự động bỏ qua bài một tiết đang chọn NLS, nhưng vẫn giữ đầy đủ mục tiêu bằng các bài/tiết hợp lệ khác.
- `tests/canvas-xaydungphuluc-smoke.js` và `tests/xaydungphuluc-smoke.js`
  - Bổ sung hồi quy 140 tiết PPCT: 12 tiết AI ở bài một tiết và mục tiêu 28 tiết NLS; xác nhận chọn đủ 28, không giao nhau, và hai checkbox loại trừ tức thì.
- `backupcode viettailieu/taobaitap.html` và `backupcode viettailieu/taobaocao.html`
  - Xóa lệnh xác nhận trình duyệt còn sót lại ở thao tác xóa; dùng `canvasConfirm` DOM an toàn trong sandbox Canvas.
- `tests/backupcode-canvas-smoke.js`
  - Nghiệm thu 6 công cụ Canvas: tài liệu hoàn chỉnh, banner, anti-FOUC, layout mở rộng, nút Gọn, lưu trữ dự phòng trong bộ nhớ và hộp thoại Canvas; xác nhận file backup được bảo vệ vẫn tồn tại.

## Kiểm tra đã chạy

- `node tests/backupcode-canvas-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS (gồm mô phỏng 28/140).
- `node tests/xaydungphuluc-smoke.js`: PASS (gồm mô phỏng 28/140).
- `node tests/xaydungphuluc-math-smoke.js`: PASS.
- `node tests/sgk-knowledge-smoke.js`: PASS.
- `git diff --check` trong phạm vi thay đổi: PASS (chỉ có cảnh báo chuyển đổi CRLF của Git).

## Chưa thực hiện

- Chưa commit hoặc push.

---

# IMPLEMENT: Nâng cấp công cụ backupcode viettailieu cho Gemini Canvas mở rộng toàn màn hình

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `backupcode viettailieu/canvas_soankhbd.html`
  - Chống FOUC ngay đầu `<head>`, mở rộng `.app-body` sang `max-w-[98%]` / `1750px`, banner Canvas, `canvasStorage`, `canvasAlert`, nút Gọn, và `setupPdfJsForCanvas` (không gán PDF Worker CDN khi sandbox chặn Worker).
- `backupcode viettailieu/soanbaigemini.html`
  - Chống FOUC trước Tailwind CDN, container `max-w-[98%] 2xl:max-w-[1750px]`, banner Canvas, `canvasConfirm` / `canvasAlert` / `canvasStorage`, nút Gọn.
- `backupcode viettailieu/taobaitap.html`
  - Chống FOUC trước Tailwind CDN, hai khối chính `max-w-7xl` / `max-w-6xl` đổi sang `max-w-[98%] 2xl:max-w-[1750px]`, banner Canvas, nút Gọn, `canvasStorage` / `canvasConfirm`.
- `backupcode viettailieu/taobaocao.html`
  - Chống FOUC, body `max-w-[98%] 2xl:max-w-[1750px]`, banner Canvas, `canvasStorage` và `canvasConfirm` (bọc modal DOM sẵn có), nút Gọn.
- `backupcode viettailieu/sangkien.html`
  - Chống FOUC, container chính `max-w-[98%] 2xl:max-w-[1750px]`, banner Canvas, `canvasConfirm` / `canvasStorage`, nút Gọn, `setupPdfJsForCanvas`.
- `backupcode viettailieu/chuyenpdf.html`
  - Chống FOUC, `.app-shell` `max-w-[98%]` / `1750px`, banner Canvas, `canvasConfirm` / `canvasStorage`, nút Gọn, `setupPdfJsForCanvas`.
- Không chỉnh `backupcode viettailieu/soanbaigemini_bakcup_khong đụng tới.html`.
- `tests/backupcode-canvas-smoke.js`
  - Kiểm tra 6 tệp: banner, anti-FOUC, layout mở rộng, compact UI, canvasConfirm/storage, PDF Worker fallback, cú pháp JS inline; xác nhận bản sao lưu gốc không bị sửa.

## Kiểm tra đã chạy

- `node tests/backupcode-canvas-smoke.js`: PASS.
- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `node tests/soanbaigemini-plan-smoke.js`: PASS.
- `node tests/taobaitap-plan-smoke.js`: PASS.
- `node tests/taobaocao-account-sync-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-math-smoke.js`: PASS.
- `node tests/sgk-knowledge-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: FAIL sẵn có ngoài phạm vi (`AI lesson mode must select the requested number of lessons`, actual 2 expected 3). Không sửa `xaydungphuluc.html`.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần `/verify` trực quan trong Gemini Canvas: mở rộng toàn màn hình, banner, nút Gọn, và đọc PDF khi Worker bị chặn.

---

# IMPLEMENT: Điều chỉnh phân bổ NLS/AI adaptive

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `canvas_xaydungphuluc.html` và `xaydungphuluc.html`
  - Giao diện adaptive hiển thị đúng quy tắc mới và mặc định chọn `2 mã` cho bài từ 2 tiết không AI.
  - Phân bổ NLS theo số tiết và AI: bài 1 tiết có AI không có NLS; bài 1 tiết không AI có 1 NLS; bài từ 2 tiết có AI có 1 NLS; bài từ 2 tiết không AI có 2 hoặc tối đa 3 NLS theo lựa chọn.
  - Fallback không sinh mã NLS khi mức yêu cầu là 0; đầu ra lọc bỏ NLS trong trường hợp này.
  - Bài 1 tiết có AI bị giới hạn đúng 1 mã AI; bài từ 2 tiết giữ 1 hoặc 2 mã theo mật độ AI.
  - Prompt sinh phụ lục đồng bộ các quy tắc NLS/AI trên, gồm cả prompt chi tiết của Phụ lục 1.
- `tests/canvas-xaydungphuluc-smoke.js` và `tests/xaydungphuluc-smoke.js`
  - Cập nhật hồi quy cho toàn bộ ngưỡng min/max adaptive và trường hợp bài 1 tiết có AI không xuất mã NLS.

## Kiểm tra đã chạy

- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-math-smoke.js`: PASS.
- `node tests/sgk-knowledge-smoke.js`: PASS.
- `git diff --check` trong phạm vi thay đổi: PASS (chỉ cảnh báo CRLF của Git).

## Chưa thực hiện

- Chưa commit hoặc push.

---

# IMPLEMENT: Bảo toàn LaTeX và chuẩn hóa mô tả Năng lực số

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `canvas_xaydungphuluc.html` và `xaydungphuluc.html`
  - `safeParseAiJson()` bảo vệ lệnh LaTeX trước khi gọi `JSON.parse`, gồm `\\frac`, `\\begin`, `\\text`, `\\neq` và các lệnh toán học phổ biến; tránh giải mã nhầm thành ký tự điều khiển.
  - Khôi phục dữ liệu cũ chứa Form Feed trước `rac{...}` thành `\\frac{...}` trước khi bọc công thức.
  - Không còn trả nguyên khối `digital_evidence` nhiều dòng cho một mã NLS không khớp; chỉ dùng dòng khớp mã, hoặc minh chứng một dòng an toàn.
  - Làm sạch mã lồng, dấu `]`, khử trùng lặp theo mã NLS và chặn tích hợp trùng mã giữa dữ liệu AI/fallback.
- `js/khbd-docx.js`
  - Phục hồi Form Feed của dữ liệu cũ trước khi chuẩn hóa/biến đổi LaTeX sang OMML.
- Smoke tests
  - Thêm hồi quy cho LaTeX, Form Feed và chuỗi NLS nhiều mã bị lồng/lặp.

## Kiểm tra đã chạy

- `node tests/xaydungphuluc-math-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/sgk-knowledge-smoke.js`: PASS.
- `git diff --check` trên phạm vi thay đổi: không có lỗi (chỉ cảnh báo CRLF của Git).

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần `/verify` trực quan với công thức phân số và một bài có nhiều mã NLS.

---

# IMPLEMENT: Khắc phục thẩm định Năng lực số theo đơn vị PPCT

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `canvas_xaydungphuluc.html` và `xaydungphuluc.html`
  - `calculateComplianceReport()` nay phân biệt đơn vị NLS đã cấu hình.
  - Với `unit: 'period'`, báo cáo cộng số tiết thực tế của các dòng có mã NLS bằng `parsePeriodCount`, lấy tổng tiết PPCT làm mẫu số, làm tròn mục tiêu theo tỉ lệ phần trăm và cho phép lệch tối đa 1 tiết.
  - Chi tiết hiển thị rõ `x/y tiết (a/b bài), mục tiêu z tiết`; dòng NLS không có số tiết hợp lệ vẫn được thông tin trong số bài nhưng đóng góp 0 tiết.
  - Với `unit: 'lesson'`, giữ nguyên mục tiêu `ceil` theo số bài và điều kiện đạt theo số bài.
  - Không thay đổi prompt, schema hoặc thuật toán phân bổ NLS/AI.
- `tests/canvas-xaydungphuluc-smoke.js` và `tests/xaydungphuluc-smoke.js`
  - Bổ sung fixture 140 tiết/87 bài: 29 tiết NLS ở 16 bài với 21% đạt theo đơn vị tiết nhưng không đạt theo đơn vị bài (mục tiêu 19 bài).
  - Kiểm tra nhãn chính xác của cả hai đơn vị và dòng NLS thiếu số tiết không được tự suy diễn thành tiết hợp lệ.

## Kiểm tra đã chạy

- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/daythay-suggest-smoke.js`: PASS.
- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `node tests/auto-reload-smoke.js`: PASS.
- `git diff --check`: không có lỗi trong phạm vi thay đổi; còn cảnh báo dòng trống cuối tệp đã có tại `docs/handoff/PLAN.md`.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần `/verify` trực quan với một PPCT thực tế có cấu hình NLS theo tổng số tiết PPCT.

---

# IMPLEMENT: Tối ưu luồng chọn giáo viên nghỉ và xem nhanh TKB Dạy thay

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `phancongtochuyenmon.html`
  - Sắp xếp lại form theo luồng nghiệp vụ: Loại hình, Ngày dạy và Giáo viên nghỉ trước; khung xem nhanh TKB ngay bên dưới; sau đó mới đến Buổi dạy, Giáo viên thực dạy và Lý do; panel đề xuất giữ ở dưới các thông tin phân công.
  - Thêm `#daythay-absent-schedule-preview`: khi đã chọn ngày hợp lệ và giáo viên nghỉ cho Dạy thay, hiển thị toàn bộ tiết thực tế của cả Buổi sáng và Buổi chiều, gồm tiết, lớp và môn. Khung tự ẩn với Dạy bù, chưa đủ dữ liệu hoặc Chủ nhật.
  - Thêm `renderAbsentTeacherSchedulePreview()` cùng nút chọn nhanh Sáng, Chiều, Cả ngày. Lịch có một buổi sẽ tự chọn đúng buổi; lịch có hai buổi tự chọn Cả ngày và nạp tiết/gợi ý qua đúng luồng `onDayThaySessionChange()` có sẵn.
  - Thêm trạng thái theo cặp ngày + giáo viên nghỉ để một lựa chọn buổi thủ công không bị render vô hại ghi đè. Khi đổi ngày hoặc giáo viên nghỉ, trạng thái này được làm mới và cho phép tự nhận diện lại một lần; không tạo vòng lặp nạp tiết/gợi ý.
  - Không đổi ID biểu mẫu, cấu trúc lưu Sổ Dạy thay, báo cáo hoặc quyết toán.
- `tests/daythay-suggest-smoke.js`
  - Kiểm tra preview dùng dữ liệu TKB thật (tiết/lớp/môn) cho cả hai buổi, auto-detect Sáng/Chiều/Cả ngày, thao tác nhanh, tính bền của chọn thủ công, làm mới auto-detect khi đổi ngày, ẩn với Dạy bù và thứ tự DOM của form.

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

# IMPLEMENT: Luôn hiển thị gợi ý Dạy thay và sắp xếp Nhật ký

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `phancongtochuyenmon.html`
  - Panel đề xuất chỉ ẩn với Dạy bù, thiếu giáo viên nghỉ hoặc ngày không hợp lệ. Khi giáo viên nghỉ không có tiết trong buổi/ngày, panel vẫn hiển thị hướng dẫn chọn lại ngày/buổi; khi chưa tick tiết, panel hướng dẫn tick tiết cần thay.
  - Preview TKB hiển thị cảnh báo rõ ràng nếu không có lịch dạy; các nút chọn buổi không có tiết bị vô hiệu hóa và nút Cả ngày chỉ bật khi có ít nhất một tiết.
  - Chặn lưu một lượt Dạy thay 0 tiết do giáo viên nghỉ không có lịch trong ngày/buổi đã chọn; không thay đổi schema lưu trữ.
  - Nhật ký mặc định sắp xếp bản sao ổn định theo ngày, Sáng → Chiều → Cả ngày, rồi tiết đầu tiên. Nút “Sắp xếp theo ngày” sắp lại mảng đã lưu theo chính thứ tự này.
  - Thêm tay nắm và HTML5 drag/drop. Kéo thả đổi trực tiếp thứ tự mảng theo ID bản ghi, lưu và kích hoạt autosave. Để thao tác kéo nhìn thấy ngay, tháng đó dùng thứ tự thủ công cho tới khi bấm nút sắp xếp theo ngày; không thêm trường dữ liệu mới.
- `tests/daythay-suggest-smoke.js`
  - Kiểm tra panel 0 tiết vẫn hiện đúng hướng dẫn, preview cảnh báo/nút vô hiệu hóa, comparator theo thời gian, kéo thả đổi đúng mảng, và nút sắp xếp khôi phục thứ tự thời gian.

## Kiểm tra đã chạy

- `node tests/daythay-suggest-smoke.js`: PASS.
- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/auto-reload-smoke.js`: PASS.
- `git diff --check -- phancongtochuyenmon.html tests/daythay-suggest-smoke.js`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần `/verify` trực quan: chọn ngày giáo viên không có tiết, chọn ngày có tiết, kéo một dòng Nhật ký rồi bấm “Sắp xếp theo ngày”.
- Cần `/verify` trực quan: chọn một giáo viên chỉ dạy sáng, chỉ dạy chiều và cả ngày; thử chọn lại buổi bằng tay rồi đổi ngày/giáo viên nghỉ.

---

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
