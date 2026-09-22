# IMPLEMENT: Đồng bộ model Gemini Canvas từ generateContent đến request mạng

Đã triển khai đúng `docs/handoff/PLAN.md`.

## File đã thay đổi

- `canvas_soankhbd.html`
  - Vá `geminiAPI.generateContent` trước khi gọi logic gốc: ảnh hoặc cờ `textbook_analysis` đặt tạm `selectedModel` thành `gemini-2.5-flash`, vì vậy log/trạng thái của `khbd-gemini.js` hiển thị đúng model OCR ngay từ đầu; luồng văn bản vẫn là `gemini-3-flash-preview`.
  - Nhận diện `inlineData`/`fileData`, model đã là 2.5, và model ảnh ở tầng mạng; tự động chuyển các lượt phân tích SGK/OCR sang `gemini-2.5-flash`.
  - Các lượt soạn KHBD không có media tiếp tục dùng `gemini-3-flash-preview` (hoặc model Canvas đã cấu hình).
  - Sao chép nguyên vẹn payload gọi Gemini Canvas, giữ riêng `systemInstruction`, `contents` và `generationConfig`; chỉ loại `thinkingConfig` không tương thích.
  - Không đặt `credentials: "omit"`, nên Canvas có thể dùng xác thực phiên sẵn có.
  - Với lượt soạn KHBD, tự động thử `gemini-2.5-flash` khi model chính trả HTTP 401, 403, 404, 429 hoặc 503.
  - Không có fallback tới proxy hoặc API key hệ thống.
- `tests/canvas-soankhbd-smoke.js`
  - Bổ sung hồi quy cho phân tuyến `generateContent`, nhận diện `inlineData`/`fileData`, phân tuyến media sang Flash 2.5, không tước credentials, và fallback model.

## Kiểm tra

- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `git diff --check -- canvas_soankhbd.html tests/canvas-soankhbd-smoke.js docs/handoff/IMPLEMENT.md`: PASS.

## Giới hạn

Việc Canvas cấp quyền cho request trực tiếp phụ thuộc phiên Gemini đang đăng nhập; chưa thể tự động kiểm tra UI Canvas từ môi trường dự án.
