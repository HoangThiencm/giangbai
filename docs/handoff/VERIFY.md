# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `api/user_gemini_keys.php`: Đã thêm safe session check `session_status() === PHP_SESSION_NONE`; `public_ai_keys_payload` trả đầy đủ `keys` và `mistral_keys` plain song song với `masked_keys`/`masked_mistral_keys`; hỗ trợ alias `gemini_keys`; tự động phân giải và khôi phục key thật từ DB khi client gửi lại masked key; `DELETE` trả mảng rỗng cho cả 2 loại key.
- `access-control.js`: Hàm `refreshSessionPages` đã đồng bộ cả `global_gemini_keys` và `global_mistral_keys` khi có key từ `api/me.php`.
- `login.html`: Cả 2 luồng xác thực (phiên còn hiệu lực và đăng nhập mới) đều lưu `global_gemini_keys` và `global_mistral_keys`.
- `ai-design-config.js`: `loadHostingFallbackConfig` chỉ cập nhật khi `gemini_keys` / `mistral_keys` trong file cấu hình có độ dài > 0, chống ghi đè rỗng lên key người dùng.
- `index.html`: `applyGlobalConfig` chỉ nạp khi mảng key cấu hình > 0, bảo vệ key cá nhân.
- `api/ai_runtime_config.php`: `load_ai_runtime_config` tự nạp `gemini_keys` của user từ bảng `users` theo `$_SESSION['user_id']`, giải mã bằng `parse_stored_api_keys` và ưu tiên hơn key admin.
- `api/hf_fallback.php`: `hf_load_gemini_keys` nạp key từ CSDL của user qua `$_SESSION['user_id']`, có sẵn `hf_parse_user_stored_keys` khi chạy độc lập.
- `js/khbd-gemini.js`: Hàm `persistGlobalKeys` ghi đè `global_gemini_keys` và `global_mistral_keys`; `saveUserAiKeysToServer` trả cờ `saved_to_db`, `not_logged_in`, `offline`.
- `js/khbd-app.js`: Nút lưu key chỉ gửi `mistral_keys` khi textarea có dữ liệu, tránh xóa nhầm Mistral key cũ; thông báo toast phân biệt rõ giữa lưu CSDL và lưu trên máy (nhắc đăng nhập khi 401).
- `tests/khbd-user-ai-keys-smoke.js`: Bổ sung toàn bộ assert xác minh các cải tiến trên.

## Test đã chạy
- `node tests/khbd-user-ai-keys-smoke.js` (PASS)
- `node tests/matrande-smoke.js` (PASS)
- `node tests/kttx-smoke.js` (PASS)
- `node tests/xaydungphuluc-smoke.js` (PASS)
- `node tests/duyetgiaoan-smoke.js` (PASS)

## Pass / Fail từng tiêu chí
1. `api/user_gemini_keys.php` trả về đầy đủ `keys: [...]`, `mistral_keys: [...]`, `masked_keys: [...]`: PASS.
2. Khi giáo viên đăng nhập, `global_gemini_keys` và `global_mistral_keys` tự động được nạp key từ CSDL trên mọi trang: PASS.
3. Không bị ghi đè mất key khi mở trang chủ `index.html` hoặc mở modal `ai-design-config.js`: PASS.
4. Các endpoint AI backend (`vehinh_ai.php`, `exam_ai.php`, `tronde.php`) tự động nhận diện và sử dụng API key cá nhân của giáo viên trong CSDL: PASS.
5. Toàn bộ smoke tests liên quan đều PASS 100%: PASS.

## Bug
Không phát hiện lỗi.