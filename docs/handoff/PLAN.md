# PLAN: Khắc Phục & Đồng Bộ API Keys Người Dùng Từ CSDL Cho Toàn Bộ Hệ Thống

## Hiện trạng
1. **Nguyên nhân gốc (Root Cause) khiến người dùng lưu API keys lên CSDL không được / bị mất**:
   - Ở commit `a612acd`, hàm `public_ai_keys_payload` trong `api/user_gemini_keys.php` đã loại bỏ các trường trả về `keys` và `mistral_keys`, chỉ trả về `masked_keys` và `masked_mistral_keys` (dạng `AIzaSy...****`).
   - Hầu hết các công cụ gọi API trực tiếp từ trình duyệt (`matrande.html`, `kttx.html`, `duyetgiaoan.html`, `xaydungphuluc.html`, `js/khbd-gemini.js` / `soankhbd.html`) phụ thuộc vào `data.keys` và `data.mistral_keys` từ `api/user_gemini_keys.php`. Khi thiếu các trường này, các trang nhận danh sách rỗng, xóa trắng ô nhập hoặc báo lỗi đỏ *"Tài khoản chưa có Gemini API Key"*.
2. **Thiếu cơ chế phổ biến API Key người dùng sang các module dùng `global_gemini_keys`**:
   - Rất nhiều công cụ trên hệ thống (`smartquiz.html`, `vehinh.html` thông qua `app.js`, `thitructuyen.html`, `tronde.html`, `taobaitap.html`, 6 trò chơi `game-*.html`, `trochoi.compiled.js`, `exam-vision-client.js`) đọc trực tiếp API Key từ `localStorage.getItem('global_gemini_keys')`.
   - Tuy nhiên, trong `access-control.js` và `login.html`, khi đăng nhập và nạp thông tin user từ `api/me.php`, hệ thống chỉ lưu vào key riêng `khbd_user_gemini_keys_<username>`, HOÀN TOÀN KHÔNG ghi vào `global_gemini_keys`.
   - Thêm vào đó, `index.html` (`applyGlobalConfig`) và `ai-design-config.js` (`loadHostingFallbackConfig`) khi nạp tệp `global_config.json` nếu thấy mảng rỗng `gemini_keys: []` lại ghi đè `[]` vào `global_gemini_keys`, xóa sạch key của người dùng nếu có.
3. **Các backend AI trên máy chủ chưa nạp key cá nhân của user trong CSDL**:
   - Các API thực thi AI phía máy chủ (`api/vehinh_ai.php`, `api/ai_explain.php`, `api/exam_ai.php`, `api/tronde.php` qua `hf_fallback.php` và `ai_runtime_config.php`) mới chỉ đọc cấu hình admin chung (`api/config.php` và `global_config.json`). Khi giáo viên đăng nhập thực hiện thao tác vẽ hình hay trích xuất đề từ ảnh, server không lấy API key cá nhân của giáo viên đã lưu trong bảng `users`.
4. **Các lỗi phụ khi lưu (`POST`)**:
   - `api/user_gemini_keys.php` chưa chấp nhận alias `gemini_keys`.
   - Khi lưu trong `khbd-app.js`, để trống Mistral khiến server hiểu là xóa trắng Mistral key cũ.
   - Submit lại masked key khiến server xóa mất key thật trong DB.
   - `session_start()` gọi trùng lặp có thể gây warning làm hỏng JSON.

## Phạm vi
1. **Khắc phục `api/user_gemini_keys.php`**:
   - Trả về đầy đủ `keys` (Gemini plain keys) và `mistral_keys` (Mistral plain keys) song song với `masked_keys`, `masked_mistral_keys` và metadata.
   - Hỗ trợ alias `gemini_keys`, khôi phục key thật khi nhận lại masked key trùng khớp key đã lưu trong DB.
   - Bọc an toàn `session_start()`.
2. **Đồng bộ toàn diện sang `global_gemini_keys` và `global_mistral_keys`**:
   - Cập nhật `access-control.js` (chạy trên tất cả các trang): khi `api/me.php` trả về `user.gemini_keys` và `user.mistral_keys`, tự động ghi đồng thời vào `global_gemini_keys` và `global_mistral_keys`.
   - Cập nhật `login.html`: đồng bộ ngay khi đăng nhập thành công.
   - Bảo vệ `global_gemini_keys` trong `index.html` và `ai-design-config.js`: không để cấu hình admin rỗng ghi đè mất key người dùng.
3. **Hỗ trợ nạp key cá nhân của user trong Backend AI**:
   - Cập nhật `api/ai_runtime_config.php` và `api/hf_fallback.php`: khi có session user (`$_SESSION['user_id']`), nạp và ưu tiên API keys trong CSDL của user đó.
4. **Chuẩn hóa Client & Kiểm thử**:
   - Cập nhật `js/khbd-gemini.js` và `js/khbd-app.js`: báo rõ khi chưa đăng nhập, không xóa nhầm Mistral khi chỉ lưu Gemini.
   - Cập nhật bài kiểm thử trong `tests/khbd-user-ai-keys-smoke.js` để kiểm tra độ phủ đồng bộ toàn bộ hệ thống.

## Ngoài phạm vi
- Không thay đổi mã hóa đối xứng AES-256-CBC trong CSDL (`users` table).
- Không sửa đổi logic nghiệp vụ AI cụ thể của từng công cụ.

## File dự kiến tác động
- `api/user_gemini_keys.php` [SỬA: Khôi phục trả về `keys`, `mistral_keys`, nhận diện alias, bảo lưu key gốc khi gặp mask, an toàn session]
- `access-control.js` [SỬA: Đồng bộ `user.gemini_keys` và `user.mistral_keys` vào `global_gemini_keys` và `global_mistral_keys` trên mọi trang]
- `login.html` [SỬA: Ghi `global_gemini_keys` và `global_mistral_keys` khi đăng nhập]
- `ai-design-config.js` [SỬA: Chống ghi đè mảng rỗng lên `global_gemini_keys`, ưu tiên key user]
- `index.html` [SỬA: `applyGlobalConfig` chỉ nạp key nếu admin có key và không ghi đè mảng rỗng]
- `api/ai_runtime_config.php` [SỬA: Tự động nạp Gemini keys của user từ CSDL theo `$_SESSION['user_id']`]
- `api/hf_fallback.php` [SỬA: `hf_load_gemini_keys` nạp keys từ CSDL của user theo `$_SESSION['user_id']`]
- `js/khbd-gemini.js` [SỬA: Nhận diện phản hồi và phân biệt lưu CSDL vs offline]
- `js/khbd-app.js` [SỬA: Xử lý toast chính xác, bảo lưu Mistral key khi để trống]
- `tests/khbd-user-ai-keys-smoke.js` [SỬA: Bổ sung kiểm tra đồng bộ toàn diện `keys`, `mistral_keys`, `global_gemini_keys`]

## Các bước thực hiện
1. **Bước 1: Sửa chữa Backend API keys (`api/user_gemini_keys.php`)**:
   - Đảm bảo `if (session_status() === PHP_SESSION_NONE) { session_start(); }`.
   - Trong `public_ai_keys_payload`: Bổ sung `'keys' => $gemini['keys']` và `'mistral_keys' => $mistral['keys']`.
   - Trong `DELETE`: Trả về `keys: []` và `mistral_keys: []`.
   - Trong `POST`: Nhận diện `$body['gemini_keys']`. Thêm logic phân giải masked key dựa trên danh sách key đã lưu của user.
2. **Bước 2: Phổ biến key người dùng tới toàn bộ client qua `access-control.js` & `login.html`**:
   - Trong `access-control.js` (`refreshSessionPages`):
     ```javascript
     if (Array.isArray(user.gemini_keys) && user.gemini_keys.length > 0) {
         localStorage.setItem('khbd_user_gemini_keys_' + (user.username || user.email || 'default'), JSON.stringify(user.gemini_keys));
         localStorage.setItem('global_gemini_keys', JSON.stringify(user.gemini_keys));
     }
     if (Array.isArray(user.mistral_keys) && user.mistral_keys.length > 0) {
         localStorage.setItem('khbd_user_mistral_keys_' + (user.username || user.email || 'default'), JSON.stringify(user.mistral_keys));
         localStorage.setItem('global_mistral_keys', JSON.stringify(user.mistral_keys));
     }
     ```
   - Trong `login.html`: Bổ sung 2 dòng tương tự khi lưu thông tin đăng nhập thành công.
   - Trong `ai-design-config.js` và `index.html`: Thêm điều kiện kiểm tra `cfg.gemini_keys.length > 0` trước khi lưu vào `global_gemini_keys` để tránh ghi đè rỗng lên key cá nhân.
3. **Bước 3: Nạp key người dùng trong Backend AI Runtime (`api/ai_runtime_config.php` và `api/hf_fallback.php`)**:
   - Khi có `$_SESSION['user_id']`, truy vấn cột `gemini_keys` từ bảng `users`, giải mã qua `parse_stored_api_keys` và nạp vào danh sách key thực thi.
4. **Bước 4: Chuẩn hóa Modal lưu key trong `js/khbd-gemini.js` và `js/khbd-app.js`**:
   - Tránh xóa nhầm Mistral key khi người dùng chỉ cập nhật Gemini key.
   - Thông báo rõ ràng cho người dùng khi chưa đăng nhập.
5. **Bước 5: Cập nhật kiểm thử tự động & Xác minh**:
   - Cập nhật `tests/khbd-user-ai-keys-smoke.js`.
   - Chạy toàn bộ các file smoke tests:
     * `node tests/khbd-user-ai-keys-smoke.js`
     * `node tests/matrande-smoke.js`
     * `node tests/kttx-smoke.js`
     * `node tests/xaydungphuluc-smoke.js`
     * `node tests/duyetgiaoan-smoke.js`

## Rủi ro
- **Xung đột giữa key cá nhân và key admin**: Key cá nhân của giáo viên được ưu tiên cho các tác vụ của chính giáo viên đó; khi giáo viên đăng xuất, key admin hoặc cache tạm vẫn hoạt động bình thường.
- **Tính tương thích**: Giữ nguyên `masked_keys` cho `duyetde.html`, đồng thời khôi phục `keys` và `mistral_keys` cho toàn bộ các module còn lại.

## Cách kiểm thử
- Chạy toàn bộ smoke tests tự động bằng Node.js:
  ```powershell
  node tests/khbd-user-ai-keys-smoke.js
  node tests/matrande-smoke.js
  node tests/kttx-smoke.js
  node tests/xaydungphuluc-smoke.js
  node tests/duyetgiaoan-smoke.js
  ```
- Kiểm tra tính đồng bộ thực tế:
  1. Đăng nhập tài khoản giáo viên đã lưu key trong CSDL.
  2. Truy cập lần lượt: `soankhbd.html`, `xaydungphuluc.html`, `matrande.html`, `kttx.html`, `duyetgiaoan.html`, `smartquiz.html`, `vehinh.html`, `thitructuyen.html`, `tronde.html`, `game-tower.html`.
  3. Xác nhận trên tất cả các trang, API key của tài khoản đều được nạp đầy đủ (không còn thông báo "Chưa nạp API Key" hoặc ô nhập bị rỗng).

## Tiêu chí nghiệm thu
1. `api/user_gemini_keys.php` trả về đầy đủ `keys: [...]`, `mistral_keys: [...]`, `masked_keys: [...]`.
2. Khi giáo viên đăng nhập, `global_gemini_keys` và `global_mistral_keys` tự động được nạp key từ CSDL trên TẤT CẢ các trang công cụ.
3. Không bị ghi đè mất key khi mở trang chủ `index.html` hoặc mở modal `ai-design-config.js`.
4. Các endpoint AI backend (`vehinh_ai.php`, `exam_ai.php`, `tronde.php`) tự động nhận diện và sử dụng API key cá nhân của giáo viên trong CSDL.
5. Toàn bộ smoke tests liên quan đều PASS 100%.