# IMPLEMENT: Ổn định tạo SVG Canvas

## Định tuyến và phục hồi SVG

- `js/khbd-app.js`: `generateSvgDrawing` gửi đúng tùy chọn `{ maxOutputTokens: 8192, purpose: 'svg_drawing', timeoutMs: 90000 }`. `extractSvgCode` bỏ fence Markdown `xml`/`svg`, trả lại SVG sạch, và chỉ tự thêm `</svg>` khi phản hồi thực sự đã mở thẻ `<svg>` nhưng bị cắt; văn bản không có SVG vẫn trả chuỗi rỗng.
- `canvas_soankhbd.html`: adapter Canvas nhận diện `options.purpose === 'svg_drawing'` và định tuyến sang `gemini-2.5-flash`, thay vì model preview/thinking mặc định.
- `tests/khbd-illustrations-smoke.js`: kiểm tra phản hồi SVG bị cắt trong fence được khép đúng và kiểm tra cấu hình token/purpose/timeout.
- `tests/canvas-soankhbd-smoke.js`: kiểm tra tuyến Canvas dành riêng cho `svg_drawing` dùng Flash 2.5.

## Kiểm thử SVG Canvas

- PASS: `node tests/khbd-illustrations-smoke.js`
- PASS: `node tests/canvas-geometry-figures-smoke.js`
- PASS: `node tests/canvas-soankhbd-smoke.js`
- PASS: `git diff --check`

# IMPLEMENT: Mở khóa tạo ảnh Gemini Canvas trực tiếp

## Tạo ảnh Canvas không dùng browser API key

- `js/khbd-gemini.js`: `generateImage` chỉ bỏ chặn API key khi `window.__KHBD_CANVAS__.directGemini === true`; trang không phải Canvas vẫn bị chặn trước khi gửi yêu cầu.
- `canvas_soankhbd.html`: Canvas bọc `generateImage` để dùng adapter Gemini trực tiếp không có key/proxy/xác thực; adapter giữ `gemini-2.5-flash-image` cho yêu cầu tạo ảnh và không hạ model này về `gemini-2.5-flash`.
- `tests/khbd-gemini-retry-smoke.js`: kiểm tra Canvas không key nhận được inline image với payload IMAGE/model ảnh đúng; kiểm tra trang thường không key vẫn báo lỗi.
- `tests/canvas-soankhbd-smoke.js`: kiểm tra tĩnh wrapper tạo ảnh, không remap model ảnh, và direct request không gửi credentials.

## Kiểm thử tạo ảnh Canvas

- PASS: `node tests/khbd-gemini-retry-smoke.js`
- PASS: `node tests/canvas-soankhbd-smoke.js`
- PASS: `node tests/canvas-geometry-figures-smoke.js`
- PASS: `git diff --check`

# IMPLEMENT: Duyệt giáo án theo tổ chuyên môn

## PPCT cũ và tự chọn trường theo khối

- `api/khbd_ppct_catalog.php` và `api/canvas_ppct_catalog.php`: GET danh sách hồ sơ PPCT không còn lọc theo năm học; GET catalog ưu tiên đúng năm học đang chọn, sau đó mới tìm bản cũ có `academic_year = ''` với cùng giáo viên, môn, khối và trường. PUT/DELETE vẫn dùng khóa năm học chính xác.
- `js/khbd-app.js`: danh sách trường PPCT luôn tải đủ hồ sơ theo môn/khối; khi đổi khối, ứng dụng kiểm tra hồ sơ của khối mới và tự chuyển sang trường đầu tiên phù hợp nếu trường hiện tại không có. Cache PPCT chưa đặt tên có dữ liệu vẫn được bảo toàn. Luồng chuyển trường không tự gọi lặp vô hạn.
- `tests/ppct-legacy-fallback-smoke.js`: mock lớp 8/Trường A sang lớp 6/Trường B, kiểm tra tự chuyển đúng trường và PPCT; đồng thời kiểm tra hồ sơ/catalog PPCT cũ chưa đặt năm vẫn tìm thấy khi năm học hiện hành đã được chọn.

## Kiểm thử PPCT cũ

- PASS: `node tests/ppct-legacy-fallback-smoke.js`
- PASS: `node tests/khbd-ppct-multi-school-smoke.js`
- PASS: `node tests/duyetgiaoan-smoke.js`
- PASS: `node tests/duyetgiaoan-integration-smoke.js`
- PASS: `git diff --check`

## Bổ sung Canvas: hình vẽ SGK và hình học

- `js/khbd-app.js`: Canvas nay trích xuất `figures` (`id`, `description`, `subsection`) ở từng lô SGK, chuẩn hóa và khử trùng lặp giữa các lô; ngữ cảnh SGK có mục `## Hình vẽ trong SGK`.
- Khi AI liệt kê ảnh trả rỗng nhưng nguồn có hình SGK hoặc có tín hiệu hình học mạnh, Canvas dựng tối đa ba đặc tả SVG SGK từ nguồn. Detector fallback riêng chỉ nhận các tín hiệu trực quan như tam giác, đường tròn, đồ thị, trục số, hình không gian hoặc tọa độ; không coi `tập hợp` hay đại số thuần là hình học. Fallback cấm tự thêm nhãn, ký hiệu hoặc số đo không nhìn thấy; bài thuần chữ/số vẫn giữ thông báo không cần hình.
- `js/khbd-prompts.js`: prompt minh họa bắt buộc trả 1–3 hình SGK cho hình học/đồ thị/trục số hoặc khi SGK có figures.
- `tests/canvas-geometry-figures-smoke.js`: kiểm tra schema, merge, ngữ cảnh figures và nhánh fallback.

## Kiểm thử Canvas hình vẽ

- PASS: `node tests/canvas-geometry-figures-smoke.js`
- PASS: `node tests/canvas-textbook-analysis-smoke.js`
- PASS: `node tests/canvas-prompts-integrity-smoke.js`
- PASS: `node tests/canvas-soankhbd-smoke.js`
- PASS: `git diff --check`

## Phạm vi đã thực hiện

- `api/duyetgiaoan.php`: thêm `get_department_teachers`, dùng `state.teachers` của kế hoạch phân công mới nhất (hoặc `plan_id` được chọn), chuẩn hóa phân công môn/lớp; `get_ppct_catalog` kiểm tra giáo viên có trong kế hoạch trước khi đọc PPCT của chính giáo viên đó.
- `duyetgiaoan.html`: đồng bộ giáo viên từ tổ, tự nạp PPCT theo giáo viên/môn/khối, tách giáo án thành bài, duyệt tuần tự từng bài (mỗi lời gọi AI tối đa 5.000 ký tự), có heuristic CV 5512 và fallback khi AI lỗi.
- Kết quả lưu theo từng bài trong `session_data` v2, vẫn tải được dữ liệu đợt cũ; xuất biên bản tổ có mục I–V và bảng tám cột, chỗ ký TTCM/BGH.
- `tests/duyetgiaoan-department-smoke.js`: kiểm tra các điểm tích hợp mới.
- Đã nghiệm thu bổ sung: heading `I. MỤC TIÊU`/`TIẾT` nội bộ không tạo bài giả khi đã có `KẾ HOẠCH BÀI DẠY` hoặc `BÀI`; xếp loại trong biên bản được chuẩn hóa theo điểm bình quân: `Tốt`, `Khá`, `Đạt`, `Chưa đạt`.
- PPCT dùng riêng trường `schoolName` (Trường/Đơn vị PPCT), không dùng tên tổ/kế hoạch làm khóa; giá trị này được lưu và khôi phục cùng đợt duyệt. Để trống sẽ truy vấn hồ sơ PPCT cũ chưa đặt tên và hiện trạng thái giải thích rõ.

## Kiểm thử đợt này

- PASS: `node tests/duyetgiaoan-department-smoke.js`
- PASS: `node tests/duyetgiaoan-smoke.js`
- PASS: `node tests/duyetgiaoan-integration-smoke.js`
- `git diff --check` phát hiện khoảng trắng cuối dòng đã có trong `docs/handoff/PLAN.md`; không sửa vì nằm ngoài phạm vi triển khai.
- Không chạy PHP lint vì môi trường hiện tại không có PHP CLI.

## Phạm vi đã thực hiện trước đó

- `api/khbd_ppct_catalog.php`, `api/canvas_ppct_catalog.php`: migration idempotent thêm `school_name`, khóa duy nhất gồm trường, GET danh sách hồ sơ khi không truyền trường, GET/PUT/DELETE theo trường.
- `js/khbd-app.js`: lưu cache PPCT theo trường, chuyển nhanh hồ sơ, đưa `school_name` vào tải/lưu/xuất/nhập và đồng bộ danh sách bài học.
- Khi chưa có trường được chọn, tự mở hồ sơ đầu tiên từ server; PPCT cũ chưa đặt tên còn dữ liệu luôn được giữ nguyên.
- `soankhbd.html`, `canvas_soankhbd.html`: thêm dropdown trường, ô nhập trường và danh sách chọn/xóa hồ sơ trong modal.
- `tests/khbd-ppct-multi-school-smoke.js`: kiểm tra hai PPCT cùng môn/lớp/năm không ghi đè và chuyển trường nạp đúng dữ liệu.

## Kiểm thử

- PASS: `node tests/khbd-ppct-multi-school-smoke.js`
- PASS: `node tests/khbd-ppct-integration-smoke.js`
- PASS: `git diff --check`
- Không chạy PHP lint vì môi trường hiện tại không có PHP CLI.
