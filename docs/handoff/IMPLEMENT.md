# IMPLEMENT: API Key theo user và quyền Quản lý văn bản

## Đã làm
1. `api/helpers.php`: `teacher_allowed_pages_resolved()` trả về đúng `normalize_pages(...)`, không tự thêm `quanlyvanban`. `maybe_upgrade_teacher_allowed_pages()` không ghi đè quyền này khi đăng nhập. `teacher_default_workspace_extras()` bỏ `quanlyvanban`.
2. `filter_posted_api_keys()`, `save_user_key_column()` và `looks_like_masked_api_key()` chuyển sang `api/helpers.php` để admin dùng chung với `encode_stored_api_keys()` và `collect_api_keys_from_input()`. `api/user_gemini_keys.php` vẫn gọi các hàm này.
3. `api/admin_students.php`: `update` lưu `gemini_keys` / `mistral_keys` khi request có trường đó, mã hóa bằng `save_user_key_column()`, và trả hai mảng đã lưu. `create` lưu key sau `lastInsertId()` khi request có gửi key. Request không gửi key thì không xóa key đang có.
4. `admin.html`: modal Cài đặt có `editGeminiKeys`, `editMistralKeys` và ghi chú dùng key chung khi để trống. `saveUserConfig` gửi hai mảng và cập nhật `cachedUsers`. Danh sách tài khoản có cột API Key: `Gemini (X key)`, `Mistral (Y key)`, hoặc `Dùng key chung`. `defaultTeacherPages` không còn tick sẵn Quản lý văn bản.
5. `index.html`: thẻ `[data-tool="teacher-documents"]` chỉ hiện khi `allowedSet` có `quanlyvanban` và feature không bị tắt.
6. `js/user-ai-settings.js`: `openModal()` không truyền tab thì mở tab `keys`. Nút navbar vẫn gọi `UserAiSettings.openModal()`.
7. `access-control.js`: giáo viên vào trang văn bản công khai mà không có `quanlyvanban` thì được báo và về `index.html`. Khách và admin vẫn xem theo thiết kế cũ. Học sinh vẫn bị chặn.
8. `api/vanban.php`: giáo viên không có `quanlyvanban` nhận 403 `Tài khoản chưa được cấp quyền Quản lý văn bản.`

## Chưa đụng
- Không đổi schema. Không đổi key trong `global_config.json`.
- Không đổi staging, Drive hay OCR của văn bản.
- Không khôi phục `taovideo/index.html` (đã bị gỡ khỏi cây làm việc trước kế hoạch này).

## Kiểm thử
- `php -l api/helpers.php`, `api/admin_students.php`, `api/vanban.php`, `api/user_gemini_keys.php`: không lỗi cú pháp. Dùng `C:\Users\HoangThien\AppData\Local\Temp\php-portable-834\php.exe` vì `php` không có trên PATH.
- `node tests/user-ai-settings-smoke.js`: PASS.
- `node tests/khbd-user-ai-keys-smoke.js`: PASS.
- `node tests/admin-user-api-keys-smoke.js`: các hợp đồng mới PASS, rồi dừng vì bước gọi `tests/teacher-permissions-smoke.js` thất bại.
- `node tests/teacher-permissions-smoke.js`: FAIL. Hợp đồng `allowed_pages_json` trong `api/helpers.php` đã khớp test. Script dừng ở dòng đọc `taovideo/index.html` (ENOENT). File này không có trong repo hiện tại.
- Node dùng `C:\Users\HoangThien\AppData\Local\OpenAI\Codex\runtimes\cua_node\cfb32733c877621e\bin\node.exe`.
- Chưa mở trình duyệt để bấm modal Admin, thẻ văn bản trên trang chủ, và tab Cài đặt AI.

## Bước tiếp
Antigravity IDE, chat mới: `/verify`
