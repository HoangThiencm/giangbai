# IMPLEMENT: Đồng bộ gọi Gemini Canvas trực tiếp không cần API key

Đã triển khai đúng `docs/handoff/PLAN.md`.

## File đã thay đổi

- `canvas_soankhbd.html`
  - Sao chép nguyên vẹn payload gọi Gemini Canvas, giữ riêng `systemInstruction`, `contents` và `generationConfig`; chỉ loại `thinkingConfig` không tương thích.
  - Bỏ `credentials: "omit"` để môi trường Gemini Canvas có thể dùng xác thực phiên sẵn có.
  - Thử model đã chọn trước, sau đó tự động thử `gemini-2.5-flash` khi nhận HTTP 401, 403 hoặc 404.
  - Không có fallback tới proxy hoặc API key hệ thống.
- `tests/canvas-soankhbd-smoke.js`
  - Bổ sung hồi quy cho payload Canvas giữ nguyên `systemInstruction`, không tước credentials, và fallback model.

## Kiểm tra

- `node tests/canvas-soankhbd-smoke.js`: PASS.
- `git diff --check -- canvas_soankhbd.html tests/canvas-soankhbd-smoke.js docs/handoff/IMPLEMENT.md`: PASS.

## Giới hạn

Việc Canvas cấp quyền cho request trực tiếp phụ thuộc phiên Gemini đang đăng nhập; chưa thể tự động kiểm tra UI Canvas từ môi trường dự án.
