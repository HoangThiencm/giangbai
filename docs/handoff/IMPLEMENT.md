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
