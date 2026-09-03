# IMPLEMENT: Khắc Phục & Đồng Bộ API Keys Người Dùng Từ CSDL Cho Toàn Bộ Hệ Thống

**Ngày implement**: 2026-09-03
**Coder**: Grok (xAI)
**Trạng thái**: DONE — 5 smoke tests PLAN yêu cầu đều PASS

## Tóm tắt thay đổi

VERIFY.md trước đó ghi FAIL vì `IMPLEMENT.md` cũ mô tả sửa source nhưng working copy chưa đổi. Lần này đã sửa đúng các file trong `PLAN.md`.

### Bước 1: Backend API keys (`api/user_gemini_keys.php`)
- `session_start()` bọc `if (session_status() === PHP_SESSION_NONE)`.
- `public_ai_keys_payload()` trả `'keys'` và `'mistral_keys'` plain, song song `masked_keys` / `masked_mistral_keys`.
- POST nhận alias `gemini_keys` bên cạnh `keys` / `api_keys`.
- POST khôi phục key thật khi client gửi lại masked key trùng `mask_user_api_key` trong DB.
- DELETE trả `'keys' => []` và `'mistral_keys' => []`.

### Bước 2: Phổ biến key người dùng tới client
- `access-control.js` (`refreshSessionPages`): khi `api/me.php` có `user.gemini_keys` / `user.mistral_keys` thì ghi cả `khbd_user_*` và `global_gemini_keys` / `global_mistral_keys`.
- `login.html`: cả 2 luồng (phiên còn hạn + form đăng nhập) ghi `global_gemini_keys` và `global_mistral_keys` khi mảng key không rỗng.
- `ai-design-config.js` (`loadHostingFallbackConfig`): chỉ ghi `global_gemini_keys` / `global_mistral_keys` khi `filter(Boolean).length > 0`.
- `index.html` (`applyGlobalConfig`): cùng điều kiện, không ghi đè mảng rỗng lên key cá nhân.

### Bước 3: Backend AI runtime
- `api/ai_runtime_config.php`: khi có `$_SESSION['user_id']`, đọc `gemini_keys` từ bảng `users`, giải mã bằng `parse_stored_api_keys`, ưu tiên hơn key admin. Tự `session_start` nếu chưa có session; tự mở PDO nếu `$GLOBALS['pdo']` chưa có.
- `api/hf_fallback.php` (`hf_load_gemini_keys`): cùng thứ tự ưu tiên. Có `hf_parse_user_stored_keys` để `exam_ai.php` (chỉ nạp `bootstrap.php`, không nạp `helpers.php`) vẫn giải mã được key đã mã hóa AES-256-CBC — không đổi thuật toán mã hóa.

### Bước 4: Modal lưu key
- `js/khbd-gemini.js`: `persistGlobalKeys()` ghi `global_gemini_keys` / `global_mistral_keys` khi sync/save; `saveUserAiKeysToServer` trả `saved_to_db` / `offline` / `not_logged_in` (401).
- `js/khbd-app.js`: nút lưu chỉ gửi `mistral_keys` khi textarea Mistral có nội dung (không xóa nhầm Mistral khi chỉ sửa Gemini). Toast phân biệt lưu CSDL vs lưu trên máy + "Đăng nhập để lưu lên CSDL".

### Bước 5: Kiểm thử
- `tests/khbd-user-ai-keys-smoke.js`: bổ sung assert `keys`/`mistral_keys` plain, alias, masked restore, safe session, đồng bộ `global_*` trên access-control/login, chống ghi đè rỗng, runtime/hf nạp key user, toast/offline, không gửi Mistral rỗng.

## Files đã sửa

| File | Thay đổi |
|------|----------|
| `api/user_gemini_keys.php` | Safe session, trả plain keys, alias `gemini_keys`, resolve masked key |
| `access-control.js` | Đồng bộ `global_gemini_keys` & `global_mistral_keys` |
| `login.html` | 2 luồng login ghi global keys |
| `ai-design-config.js` | Không ghi đè mảng rỗng |
| `index.html` | Không ghi đè mảng rỗng |
| `api/ai_runtime_config.php` | Nạp key user từ CSDL theo session |
| `api/hf_fallback.php` | Nạp key user từ CSDL theo session; parse khi thiếu helpers |
| `js/khbd-app.js` | Bảo lưu Mistral khi chỉ sửa Gemini; toast CSDL vs offline |
| `js/khbd-gemini.js` | Đồng bộ global keys; phân biệt lưu CSDL vs offline |
| `tests/khbd-user-ai-keys-smoke.js` | Kiểm tra đồng bộ toàn diện |

Không đụng file ngoài danh sách PLAN. Không đổi AES-256-CBC. Không đổi logic nghiệp vụ AI từng công cụ.

## Kết quả kiểm thử

```
khbd user AI keys smoke: passed
matrande smoke: Word templates and account Gemini key synchronization passed
kttx smoke: Word templates and account Gemini key synchronization passed
PASS xaydungphuluc smoke: PPCT 7-column form, independent table ingest, no admin-header leak, density ranges and auto-hiding progress UI are present.
duyetgiaoan smoke: passed
```

Không chạy được kiểm thử trình duyệt end-to-end (không có browser tool trong phiên này). Các tiêu chí đăng nhập thật / mở từng trang công cụ để xác nhận ô key không rỗng thuộc bước `/verify`.
