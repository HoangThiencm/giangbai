# Báo cáo triển khai: JSON AI an toàn và Danh mục PPCT/Phụ lục 3

## Đã thực hiện

- `js/khbd-app.js`: thêm `parseAiJsonSafely`, chỉ lấy JSON root cân bằng; sửa duy nhất escape sai trong chuỗi, control raw và dấu phẩy cuối. Các JSON cho Canvas SGK, PPCT, đề xuất và hình minh họa đều dùng chung parser. Lỗi còn lại trả thông báo rõ, không parse kiểu regex tham lam.
- PPCT nay tạo danh mục Phụ lục 3 theo dòng: mã ổn định, chương/bài, số tiết, tiết CT, tuần, NLS/AI (tick, mã, bằng chứng) và metadata nguồn. Dòng trùng tên vẫn khác nhau theo bối cảnh tuần/tiết. Chọn dòng dùng ngay thời lượng, phạm vi và tick tích hợp; ID bản nháp gồm mã dòng PPCT.
- `soankhbd.html`: có bảng duyệt danh mục, tick NLS/AI do giáo viên điều chỉnh và nút lưu CSDL. Canvas và bản backup chỉ lưu catalog trong localStorage, không tuyên bố đã lưu máy chủ; asset `khbd-app.js` cache-bust `ppct-catalog-v9`.
- `api/khbd_ppct_catalog.php` và `database_schema.sql`: API GET/PUT theo session giáo viên, không nhận/trust owner từ client; bảng `teacher_ppct_catalogs` unique theo giáo viên + môn + lớp + năm học. Chỉ lưu hàng cấu trúc/metadata, không lưu ảnh hay OCR thô.

## Kiểm thử

- `node tests/khbd-ppct-catalog-json-smoke.js`: PASS (JSON có fence, LaTex slash, newline hợp lệ, escape sai, lỗi thiếu JSON; PPCT trùng tên).
- `node tests/khbd-ppct-api-static-smoke.js`: PASS (hợp đồng session/teacher-only/schema).
- `node --check js/khbd-app.js`: PASS.
- `git diff --check`: PASS.
- PHP lint chưa chạy được vì PHP không có trong PATH.

Chưa commit, push hoặc deploy. Máy chủ cần chạy migration `database_schema.sql` (hoặc API tự tạo bảng khi gọi lần đầu) rồi triển khai các asset v9.

# Báo cáo triển khai: Phân bổ thời lượng KHBD theo khối lượng tiểu mục

## Cập nhật mới

- `js/khbd-prompts.js`: bổ sung hồ sơ tiểu mục (tên, độ phức tạp, tín hiệu, trọng số) và phân bổ largest-remainder có chặn, giữ nguyên chia đều khi thiếu trọng số hợp lệ.
- `js/khbd-app.js`: dùng cùng hồ sơ SGK/Canvas khi tạo từng pha, chuẩn hóa tiêu đề và ghép/xuất giáo án; không suy định mức từ độ dài văn bản AI sinh.
- Canvas phân tích cấu trúc 1–4 tiểu mục bằng diễn đạt lại, lưu trọng số phục vụ soạn bài; cache-bust nâng lên `canvas-system-v7` ở hai bản Canvas. Bản thường nạp `khbd-*-weighted-v7`.
- Thêm `tests/khbd-weighted-duration-smoke.js`.

### Hoàn tất luồng trọng số

- Prompt tạo Hoạt động B nay nhận hồ sơ tiểu mục từ Canvas ngay cả khi Canvas chỉ lưu ngữ cảnh cấu trúc, không có OCR nguyên văn. Do đó AI nhận đúng tên từng mục và số phút đã phân bổ, thay vì quay về chia đều.
- Trọng số chỉ nhận trong thang 1–6; thuật toán largest-remainder giữ tối thiểu 3 phút cho mỗi nhánh khi ngân sách cho phép. Khi thiếu hoặc sai hồ sơ, hệ thống giữ cơ chế chia đều tương thích dữ liệu cũ.
- Hồ sơ được truyền xuyên suốt: đọc SGK/Canvas → trạng thái bản nháp → prompt → chuẩn hóa tiêu đề từng pha → ghép và xuất Word. Đọc SGK mới ngoài Canvas cũng tự thay hồ sơ cũ, tránh dùng nhầm trọng số bài trước.

### Kiểm thử

- `node --check js/khbd-prompts.js`: PASS
- `node --check js/khbd-app.js`: PASS
- `node tests/khbd-weighted-duration-smoke.js`: PASS
- `node tests/khbd-dynamic-time-budgets-smoke.js`: PASS
- `node tests/khbd-activity-d-dedupe-smoke.js`: PASS
- `node tests/canvas-soankhbd-smoke.js`: PASS
- `node tests/canvas-textbook-analysis-smoke.js`: PASS
- `node tests/khbd-docx-layout-smoke.js`: PASS
- `git diff --check` (các tệp trong phạm vi): PASS

# Báo cáo triển khai: Đồng bộ thời lượng KHBD theo số nhánh Hoạt động 2

## Cập nhật: khóa tổng thời lượng 90 phút khi tạo từng pha riêng

- `js/khbd-app.js`
  - Thêm bộ phân giải số nhánh dùng chung cho Hoạt động 2: ưu tiên nội dung B đã lưu, sau đó suy từ ngữ cảnh SGK bằng `extractTextbookSubsections`, cuối cùng mới dùng đoạn đang xử lý hoặc 1 nhánh.
  - `clipKhbdActivityMarkdown`, luồng nhận kết quả từng pha và luồng ghép/xuất toàn bộ giáo án đều truyền cùng số nhánh B vào bộ chuẩn hóa tiêu đề thời lượng.
  - Với bài 90 phút có 3 nhánh B, thời lượng luôn là A 8 phút, B 48 phút (3 × 16), C 22 phút, D 12 phút; tổng đúng 90 phút.
- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`
  - Nâng cache-bust Canvas lên `20260915-canvas-system-v6` cho các tệp dùng chung, bao gồm `khbd-app.js`.
- `soankhbd.html`
  - Thêm cache-bust riêng cho `khbd-app.js` để trang soạn bài tải bản sửa thời lượng.
- `tests/khbd-activity-d-dedupe-smoke.js`
  - Bổ sung hồi quy: tạo B 3 nhánh trước rồi tạo A/C/D riêng lẻ, đồng thời kiểm tra đường ghép giáo án đầy đủ 90 phút.
- `tests/canvas-soankhbd-smoke.js`
  - Cập nhật kỳ vọng cache-bust Canvas v6.

### Kiểm thử

- `node --check js/khbd-app.js`: PASS.
- `node tests/khbd-activity-d-dedupe-smoke.js`: PASS.
- `node tests/khbd-time-budgets-smoke.js`: PASS.
- `node tests/khbd-activities-ad-standard-smoke.js`: PASS.
- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `node tests/backupcode-canvas-smoke.js`: PASS.
- `node tests/khbd-docx-layout-smoke.js`: PASS.
- `git diff --check` (tệp trong phạm vi): PASS.

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.

## Cập nhật: Cài đặt PPCT / Nạp Phụ lục 3 theo môn, lớp, năm học

- `soankhbd.html`: thêm nút và modal **Cài đặt PPCT** độc lập với Quản lý API Key. Modal chọn khối, môn, năm học; nhận nội dung dán hoặc PDF/ảnh; xem trước các bài và tick NLS/AI trước khi lưu.
- `js/khbd-app.js`: dùng chuẩn hoá chung `analyzePpctImport`; lưu/tải catalog theo đúng `subject`, `grade`, `academic_year`; nguồn gửi API chỉ có metadata định dạng/thời điểm/phạm vi/chế độ nạp, không có ảnh, data URL, OCR hoặc văn bản gốc. Bước 2 chỉ tiêu thụ danh mục và mở Cài đặt PPCT thay vì lưu trùng. Có xác nhận trước khi thay danh mục đã tồn tại.
- Canvas và bản backup chuyển cache-bust `ppct-settings-v10`; chỉ thông báo/lưu cục bộ, hướng người dùng mở website để lưu CSDL.

### Kiểm thử

- `node tests/ppct-settings-import-smoke.js`: PASS.
- `node tests/soankhbd-ppct-standards-smoke.js`: PASS.
- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `node --check js/khbd-app.js`: PASS.
- `git diff --check`: PASS.

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.

# Báo cáo triển khai: Gemini Canvas hệ thống không cần key cá nhân

## Cập nhật: giới hạn thời gian Canvas v5

- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`
  - Đồng bộ toàn bộ nguồn `khbd-prompts.js`, `khbd-gemini.js`, `khbd-docx.js` và `khbd-app.js` sang cache-bust `20260915-canvas-system-v5`; không còn tham chiếu Canvas v3.
- `js/khbd-gemini.js`
  - Tuyến Canvas vẫn là một yêu cầu duy nhất tới proxy hệ thống, không gửi key/định danh trình duyệt và không rơi về Google trực tiếp.
  - Proxy được yêu cầu tối đa 85 giây, còn trình duyệt chờ 105 giây để nhận chẩn đoán từ máy chủ. Nếu trình duyệt thực sự quá hạn, thông báo hướng dẫn giảm số trang hoặc thử lại.
  - Phản hồi HTTP 200 rỗng/`RECITATION` vẫn không tự retry.
- `api/canvas_gemini.php`
  - Mọi system key dùng chung một deadline toàn cục tối đa 85 giây. Mỗi lần cURL chỉ được dùng phần thời gian còn lại (và tối đa 55 giây), không còn tình huống nhiều key nối tiếp nhiều lượt chờ dài.
  - Khi hết deadline, trả HTTP 504 cùng thông báo an toàn `system_deadline`.
- `js/khbd-app.js`
  - Canvas phân tích một trang PDF hoặc một ảnh SGK trong mỗi yêu cầu, giữ tiến độ `trang/ảnh i/n` hiển thị rõ và chỉ lấy JSON diễn đạt lại về cấu trúc bài.
  - Mỗi lô truyền rõ `timeoutMs: 105000`; không trích xuất nguyên văn SGK.
- Kiểm thử đã cập nhật cho cache v5, chênh lệch deadline client/server, deadline proxy toàn cục, và lô SGK một trang/ảnh.

### Kiểm thử cập nhật v5

- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `node tests/khbd-gemini-retry-smoke.js`: PASS.
- `node tests/canvas-gemini-api-smoke.js`: PASS.
- `node tests/canvas-textbook-analysis-smoke.js`: PASS.
- `node tests/khbd-vision-batching-smoke.js`: PASS.
- `node tests/khbd-mistral-ocr-smoke.js`: PASS.
- `node tests/khbd-4steps-workflow-smoke.js`: PASS.
- `node tests/backupcode-canvas-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/soanbaigemini-plan-smoke.js`: PASS.
- `node --check js/khbd-gemini.js` và `node --check js/khbd-app.js`: PASS.
- `git diff --check`: PASS. PHP lint không chạy được vì máy không có `php` trong PATH.

Không commit, push hay deploy. `docs/handoff/PLAN.md` không bị sửa.

## Cập nhật: Phân tích SGK Canvas không chép nội dung nguồn

- `js/khbd-app.js`
  - Tuyến Canvas không còn dùng fallback Gemini theo kiểu OCR/chép SGK. Thay vào đó, nó gửi ảnh và đúng các trang PDF đã chọn theo lô tối đa 3 đơn vị, rồi nhận JSON ngắn gồm môn, lớp, chủ đề, số tiết/phạm vi, 1–3 ý chính, tóm lược và điểm chưa rõ.
  - Kết quả được diễn đạt lại, gom thành ngữ cảnh SGK và đi qua `applyTextbookOcrResult`, nên `ocrReady` cùng Bước 3–4 tiếp tục hoạt động mà không có bản sao văn bản SGK.
  - Không tự gửi lại yêu cầu khi Gemini trả `RECITATION`; thông báo hướng người dùng tải lại Canvas bản mới và dùng “Phân tích SGK”. Luồng không-Canvas vẫn ưu tiên Mistral OCR như cũ.
- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`
  - Đổi nhãn/tin nhắn thành “Phân tích SGK”, nói rõ chỉ tạo ngữ cảnh tóm lược.
  - Nâng cache-bust `khbd-app.js` lên `20260915-canvas-system-v4`.
- Kiểm thử bổ sung: `tests/canvas-textbook-analysis-smoke.js`; cập nhật smoke Canvas và workflow 4 bước cho hành vi phân tích mới.

### Kiểm thử cập nhật

- `node --check js/khbd-app.js`: PASS.
- `node tests/canvas-textbook-analysis-smoke.js`: PASS.
- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `node tests/khbd-mistral-ocr-smoke.js`: PASS.
- `node tests/khbd-vision-batching-smoke.js`: PASS.
- `node tests/khbd-4steps-workflow-smoke.js`: PASS.
- `git diff --check` cho tệp phạm vi: PASS. `thitructuyen.html` có whitespace tồn tại sẵn, ngoài phạm vi.

## Phạm vi đã thực hiện

- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`
  - Bỏ Mistral OCR client, pseudo key `canvas-session` và `window.MistralOcr` giả lập.
  - Canvas gọi trực tiếp một tuyến Gemini hệ thống cho OCR; không còn lần gọi Mistral giả rồi mới gọi Gemini lần hai.
  - Khai báo rõ `systemGemini` và endpoint Canvas tin cậy; giữ patch tương thích cho bản thư viện cũ.
  - Cache-bust `20260915-canvas-system-v3` cho các script Canvas được host (prompts, Gemini, DOCX, app), để trình duyệt tải đúng bản mới sau triển khai.
  - Giao diện OCR nói rõ dùng Gemini Canvas do hệ thống cấp; các trường Mistral cũ được vô hiệu hoá để tương thích DOM.
- `js/khbd-app.js`
  - Nhận diện Canvas và gọi Gemini ngay cho SGK/PPCT, không báo sai rằng Mistral không khả dụng.
- `js/khbd-gemini.js`
  - Trích xuất text từ toàn bộ candidates/parts.
  - Với HTTP 200 không có text, trả chẩn đoán an toàn gồm `finishReason`, `promptFeedback.blockReason` hoặc trạng thái safety (nếu có) và không retry/đổi model vô ích.
  - Tuyến Canvas có cấu hình tin cậy gọi `canvas_gemini.php` trực tiếp với đúng `{ preferred_model, payload, timeout }`, đọc an toàn `body`/`meta`, và không bao giờ rơi sang Google trực tiếp hay guard key cá nhân.
  - Trang không phải Canvas vẫn giữ nguyên cảnh báo bắt buộc có Gemini API Key cá nhân.
- `api/canvas_gemini.php`
  - Chỉ dùng Gemini key hệ thống cho Canvas, không nhận/trust `user_account` hoặc header tài khoản từ client.
  - Nhận `preferred_model`, vẫn tương thích body `model` cũ, trả `meta` an toàn và body Gemini cần để frontend chẩn đoán response rỗng/safety.
- Đã cập nhật `tests/canvas-soankhbd-smoke.js`, `tests/khbd-gemini-retry-smoke.js` và thêm `tests/canvas-gemini-api-smoke.js`.

## Kiểm thử

- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `node tests/khbd-gemini-retry-smoke.js`: PASS, gồm text nhiều parts, HTTP 200 safety/rỗng không retry, Canvas không key gọi proxy một lần, và trang thường không key vẫn bị chặn.
- `node tests/canvas-gemini-api-smoke.js`: PASS.
- `node tests/khbd-vision-batching-smoke.js`: PASS.
- `node tests/khbd-mistral-ocr-smoke.js`: PASS.
- `node tests/khbd-1click-chain-smoke.js`: PASS.
- `node tests/backupcode-canvas-smoke.js`: PASS.
- `git diff --check` cho các tệp phạm vi: PASS. Worktree có whitespace có sẵn trong `backend/thitructuyen.py`, ngoài phạm vi.
- PHP lint không chạy được vì môi trường không có `php` trong PATH.

## Lưu ý triển khai máy chủ

- Bản đang chạy tại `hoangthiencm.id.vn` vẫn là asset cũ (`canvas-ocr-v2`), nên vẫn có thể báo thiếu Gemini API Key cá nhân.
- Cần **commit, push và deploy** các tệp Canvas/`js/khbd-gemini.js` (cùng build obfuscation của dự án) thì URL cache-bust `canvas-system-v3` mới tải được và lỗi trên website mới hết. Turn này không commit, push hoặc deploy.

## Bảo toàn

- Không sửa `docs/handoff/PLAN.md`.
- Không commit hoặc push.
- Giữ nguyên các thay đổi không liên quan đã có trong worktree.

## Cập nhật: Canvas dự phòng danh mục môn học khi module host lỗi/rỗng

- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`
  - Nạp tuần tự có kiểm tra timeout cho `ai-design-config.js`, curriculum, standards và YCCĐ trước khi nạp `khbd-app.js`; HTTP 200 nhưng tệp rỗng được xem là lỗi nạp.
  - Khi curriculum host không khả dụng, dùng danh mục dự phòng gồm toàn bộ môn THCS hỗ trợ và các bài Lớp 6 (Toán có các bài 1–7), nên ô Môn học/Bài học không còn rỗng.
  - Banner phân biệt rõ đang dùng danh mục dự phòng, thay cho thông báo chung “không kết nối mạng”. Cache-bust đồng bộ `20260916-canvas-module-v8`.
- `js/khbd-app.js`: khởi động được cả khi ứng dụng được nạp sau `DOMContentLoaded`, tránh race giữa loader Canvas và app.
- `.github/workflows/ftp-deploy.yml` và `tools/check-required-assets.js`: chặn deploy nếu một trong bốn module bắt buộc thiếu hoặc 0 byte, kiểm tra cả trước và sau bước build; marker phiên bản v8 làm các asset này được FTP cập nhật lại.
- Thêm `tests/canvas-module-fallback-smoke.js`; cập nhật smoke Canvas sang v8.

### Kiểm thử

- `node tools/check-required-assets.js`: PASS.
- `node tests/canvas-module-fallback-smoke.js`: PASS (mô phỏng module rỗng và module bình thường).
- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `node tests/khbd-4steps-workflow-smoke.js`: PASS.
- `node tests/khbd-autofill-metadata-smoke.js`: PASS.
- `node --check js/khbd-app.js`: PASS.
- `git diff --check` cho các tệp trong phạm vi: PASS. Các cảnh báo whitespace ở `taobaitap.html`/`thitructuyen.html` là thay đổi có sẵn ngoài phạm vi.

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.
