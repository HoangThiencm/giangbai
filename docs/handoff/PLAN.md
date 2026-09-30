# Kế hoạch thực hiện (PLAN) - Khắc phục triệt để lỗi OCR dán ảnh clipboard & Đồng bộ API Key trong Quản lý văn bản

## 1. Nguyên nhân gốc rễ (Root Cause)
1. **Lệch khóa lưu trữ (Key Storage Mismatch)**:
   - Tài khoản giáo viên trong hệ thống lưu API Key ở các khóa `localStorage` đa dạng:
     - `khbd_user_gemini_keys_<email>` / `khbd_user_gemini_keys_default`
     - `khbd_user_mistral_keys_<email>` / `khbd_user_mistral_keys_default`
     - `khbd_gemini_api_keys`, `gemini_api_keys`, `xdpl_gemini_api_keys`, `geometryAiApiKeys`
     - `xdpl_mistral_api_keys`
   - Nhưng `vanban-app.js` hiện tại chỉ gọi `AiDesignConfig.getApiKeys()` và `AiDesignConfig.getMistralKeys()` (vốn chỉ đọc đúng 2 khóa `global_gemini_keys` và `global_mistral_keys`). Khi 2 khóa `global_*` chưa được ghi hoặc bị trống, hệ thống kết luận là "0 key" và chặn ngay lập tức.
2. **Race condition (Chưa await đồng bộ trước khi OCR)**:
   - `syncUserKeysFromServer()` là async nhưng chỉ gọi ngầm (fire-and-forget) lúc tải trang. Khi người dùng vừa mở trang hoặc dán ảnh ngay, `ocrImageData` không `await syncUserKeysFromServer()`, dẫn đến kiểm tra key khi dữ liệu từ máy chủ chưa về.
3. **Modal cấu hình không tương thích**:
   - `AiDesignConfig.openModal()` là modal canvas cũ, chỉ có nút tải tệp `.txt` cho Gemini/Groq, không có ô nhập hay lưu Mistral Key. Trong khi đó hệ thống chuẩn dùng `UserAiSettings.openModal('keys')` (từ `js/user-ai-settings.js`).

---

## 2. Danh sách file tác động
| STT | Đường dẫn file | Thao tác | Mục đích / Nội dung tác động |
| :-- | :--- | :--- | :--- |
| 1 | `vanban-app.js` | Cập nhật | Bổ sung hàm đọc key đa nguồn `getAvailableGeminiKeys()`, `getAvailableMistralKeys()`, `ensureKeysLoaded()`, cập nhật `hasMistralOcr()`, `hasGeminiVision()`, `extractTextViaGeminiVision()`, `ocrImageData()`. Ưu tiên mở `UserAiSettings` khi thiếu key. |
| 2 | `quanlyvanban-chuyenmon.html` | Cập nhật | Nạp thêm `<script src="js/user-ai-settings.js"></script>` trong `<head>` để đồng bộ cấu hình AI chuẩn. |
| 3 | `quanlyvanban-hanhchinh.html` | Cập nhật | Nạp thêm `<script src="js/user-ai-settings.js"></script>` trong `<head>`. |
| 4 | `quanlyvanban-dang.html` | Cập nhật | Nạp thêm `<script src="js/user-ai-settings.js"></script>` trong `<head>`. |
| 5 | `tests/vanban-ocr-clipboard-smoke.js` | Cập nhật | Bổ sung kiểm tra đọc key từ `khbd_user_*`, `ensureKeysLoaded`, và cơ chế fallback. |

---

## 3. Các bước thực hiện chi tiết cho Coder

### Bước 1: Chuẩn bị
- Xóa `docs/handoff/.lock` trước khi sửa source code.
- Tuyệt đối không sửa file ngoài danh sách đã nêu.

### Bước 2: Bổ sung cơ chế đọc key đa nguồn & đồng bộ trong `vanban-app.js`
1. Thêm 2 hàm gom key đa nguồn (ưu tiên `global_*`, sau đó fallback sang `khbd_user_*`, legacy keys):
   ```javascript
   function getAvailableGeminiKeys() {
       const email = String(localStorage.getItem('userEmail') || '').trim().toLowerCase();
       const candidates = [
           'global_gemini_keys',
           email ? `khbd_user_gemini_keys_${email}` : null,
           'khbd_user_gemini_keys_default',
           'khbd_gemini_api_keys',
           'gemini_api_keys',
           'xdpl_gemini_api_keys',
           'geometryAiApiKeys'
       ].filter(Boolean);
       const found = [];
       for (const key of candidates) {
           try {
               const raw = localStorage.getItem(key);
               if (!raw) continue;
               const parsed = JSON.parse(raw);
               const list = Array.isArray(parsed) ? parsed : [parsed];
               for (const item of list) {
                   const s = String(item || '').trim();
                   if (s.length > 10 && !found.includes(s)) found.push(s);
               }
           } catch (_) {}
       }
       if (!found.length && window.AiDesignConfig?.getApiKeys) {
           return window.AiDesignConfig.getApiKeys();
       }
       return found;
   }

   function getAvailableMistralKeys() {
       const email = String(localStorage.getItem('userEmail') || '').trim().toLowerCase();
       const candidates = [
           'global_mistral_keys',
           email ? `khbd_user_mistral_keys_${email}` : null,
           'khbd_user_mistral_keys_default',
           'xdpl_mistral_api_keys'
       ].filter(Boolean);
       const found = [];
       for (const key of candidates) {
           try {
               const raw = localStorage.getItem(key);
               if (!raw) continue;
               const parsed = JSON.parse(raw);
               const list = Array.isArray(parsed) ? parsed : [parsed];
               for (const item of list) {
                   const s = String(item || '').trim();
                   if (s.length > 10 && !found.includes(s)) found.push(s);
               }
           } catch (_) {}
       }
       if (!found.length && window.AiDesignConfig?.getMistralKeys) {
           return window.AiDesignConfig.getMistralKeys();
       }
       return found;
   }
   ```
2. Cập nhật `hasMistralOcr()` và `hasGeminiVision()`:
   ```javascript
   function hasMistralOcr() {
       return window.MistralOcr && getAvailableMistralKeys().length > 0;
   }

   function hasGeminiVision() {
       return getAvailableGeminiKeys().length > 0;
   }
   ```
3. Đảm bảo có `ensureKeysLoaded()`:
   ```javascript
   let syncKeysPromise = null;
   async function ensureKeysLoaded() {
       if (!syncKeysPromise) {
           syncKeysPromise = syncUserKeysFromServer().catch(() => {});
       }
       return syncKeysPromise;
   }
   ```
4. Trong `extractTextViaGeminiVision(dataUrl)`:
   Sử dụng danh sách key từ `getAvailableGeminiKeys()`:
   ```javascript
   const keys = getAvailableGeminiKeys();
   if (!keys.length) throw new Error('Chưa có Gemini API Key.');
   const key = keys[Math.floor(Math.random() * keys.length)];
   ```
5. Trong `ocrImageData(dataUrl)`:
   - Đầu hàm: `await ensureKeysLoaded();`
   - Khi không có key:
     ```javascript
     function openSystemAiConfig() {
         if (window.UserAiSettings?.openModal) {
             window.UserAiSettings.openModal('keys');
             return;
         }
         if (window.AiDesignConfig?.openModal) {
             window.AiDesignConfig.openModal();
         }
     }
     ```
     Gọi `openSystemAiConfig()` khi người dùng chưa có cả Mistral lẫn Gemini key.
6. Trong `renderNav()`:
   Nút `#vanbanAiConfigBtn` khi bấm cũng ưu tiên gọi `openSystemAiConfig()`.

### Bước 3: Nạp `js/user-ai-settings.js` vào 3 trang HTML
- Trong `<head>` của `quanlyvanban-chuyenmon.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`:
  Thêm `<script src="js/user-ai-settings.js?v=20261001"></script>`.

### Bước 4: Cập nhật kiểm thử tự động
- Cập nhật `tests/vanban-ocr-clipboard-smoke.js`:
  - Kiểm tra `getAvailableGeminiKeys()` và `getAvailableMistralKeys()` nhận diện được key từ `khbd_user_*`.
  - Kiểm tra `ensureKeysLoaded` được định nghĩa và gọi trong luồng OCR.
  - Chạy toàn bộ các test suites:
    ```powershell
    node tests/vanban-ocr-clipboard-smoke.js
    node tests/vanban-chuyenmon-signature-smoke.js
    node tests/vanban-display-saved-smoke.js
    python tests/vanban-chuyenmon-root-smoke.py
    ```

### Bước 5: Bàn giao
- Tạo lại file `docs/handoff/.lock` với nội dung `LOCK`.
- Cập nhật `docs/handoff/IMPLEMENT.md` ghi nhận các thay đổi thực tế.

---

## 4. Tiêu chí nghiệm thu (Verify Checklist)
- [ ] Người dùng có key trong `khbd_user_gemini_keys_*` hoặc `khbd_user_mistral_keys_*` được tự động nhận diện, không còn bị báo thiếu key.
- [ ] Dán ảnh (Ctrl+V hoặc nút "Dán nhanh từ Clipboard") tự động chạy OCR mà không bị chặn báo lỗi.
- [ ] Nút "Cấu hình AI" mở hộp thoại `UserAiSettings` chuẩn với đầy đủ cả 2 tab Gemini & Mistral.
- [ ] Tất cả smoke tests đều PASS (exit code 0).
