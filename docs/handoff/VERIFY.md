# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Modal "Cài đặt AI & Key" (`js/user-ai-settings.js`): bổ sung danh mục model mới nhất (`gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-2.0-pro-exp-02-05`, `gemini-2.0-flash-thinking-exp-01-21`, `gemini-3.7-flash-thinking`, ...).
- [x] Cho phép tự nhập model thủ công: hỗ trợ tùy chọn `__custom__` ("Tự nhập model khác...") và hiển thị ô input text để người dùng tự do nhập bất kỳ model ID nào.
- [x] Tách 02 cấu hình rõ ràng:
  - **Module Gemini mặc định**: lưu vào `default_gemini_module` và `khbd_gemini_model`.
  - **Module Gemini dự phòng (Fallback)**: lưu vào `default_gemini_fallback` và `khbd_gemini_fallback_model`.
- [x] Module `js/khbd-gemini.js`: `_fallbackModelId()` đọc động từ localStorage (`default_gemini_fallback` / `khbd_gemini_fallback_model`), tự động thêm custom fallback model vào `availableModels`.
- [x] Module `xaydungphuluc.html` và `nghiencuubaihoc.html`: đọc fallback model động qua `getFallbackModel()`, có guard chống lặp khi fallback trùng model chính.
- [x] Bộ test tự động kiểm thử regression và retry fallback chạy pass 100%.

## Test đã chạy
1. `node tests/user-ai-settings-smoke.js`: PASS (exited with code 0).
2. `node tests/khbd-gemini-retry-smoke.js`: PASS 5/5 cases (exited with code 0).
3. `node tests/xaydungphuluc-smoke.js`: PASS (exited with code 0).
4. `node tests/xaydungphuluc-integration-smoke.js`: PASS (exited with code 0).

## Pass / Fail từng tiêu chí
- [x] Cho phép khai báo thủ công model mới: PASS.
- [x] Cho phép chọn/nhập model mặc định: PASS.
- [x] Cho phép chọn/nhập model fallback: PASS.
- [x] Lưu và nạp lại chính xác từ localStorage: PASS.
- [x] Cơ chế xoay vòng fallback sử dụng đúng model được cấu hình: PASS.
- [x] Không gây lặp vô hạn khi model chính trùng model fallback: PASS.
- [x] Tất cả smoke test liên quan đều PASS: PASS.

## Bug
Không có.
