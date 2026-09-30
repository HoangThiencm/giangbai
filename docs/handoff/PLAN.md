# PLAN: Đồng bộ API Key tài khoản (Mistral/Gemini) và xử lý lỗi nhận diện ảnh chụp trong Quản lý văn bản

## 1. Hiện trạng & Nguyên nhân gốc rễ (Root Cause)
- **Hiện tượng**:
  + Người dùng đã cấu hình đầy đủ API Key trên trang chủ (bảng điều khiển hiển thị rõ: `🔑 API Key sẵn sàng · Gemini 10 · Mistral 1`).
  + Tuy nhiên, khi sang Quản lý văn bản (`quanlyvanban-*.html`), chụp dán (Ctrl+V) ảnh phần đầu văn bản (số, ngày) hoặc vùng chữ ký vào ô nhập liệu thì hệ thống vẫn báo lỗi đỏ:
    `"Ảnh vùng chữ ký cần Mistral OCR. Hãy dán chữ hoặc dùng PDF có chữ ký số."`
- **Nguyên nhân kỹ thuật đã xác định chính xác**:
  1. **Thiếu cơ chế đồng bộ Key từ CSDL tài khoản**:
     - Trên trang chủ `index.html`, API Key (10 Gemini, 1 Mistral) được lưu trên CSDL máy chủ thông qua API `api/user_gemini_keys.php`.
     - Các trang công cụ khác như `nghiencuubaihoc.html`, `xaydungphuluc.html`, `duyetgiaoan.html` đều có hàm `syncUserKeysFromServer()` gọi `api/user_gemini_keys.php` khi tải trang để kéo key về `localStorage` (`global_mistral_keys`, `global_gemini_keys`).
     - **Ngược lại, trang Quản lý văn bản (`vanban-app.js`) KHÔNG HỀ gọi `api/user_gemini_keys.php`** khi khởi tạo. Do đó, nếu người dùng mở trực tiếp trang Quản lý văn bản hoặc mở tab mới, `localStorage` của trang này không có key Mistral, khiến `hasMistralOcr()` trả về `false`.
  2. **Giao diện thiếu nút Cấu hình AI**:
     - Trang Quản lý văn bản không hiển thị badge trạng thái hay nút "Cấu hình AI" (`AiDesignConfig.openModal()`), khiến người dùng không biết key đã được nạp hay chưa.
  3. **Chưa tận dụng 10 Key Gemini đã có sẵn để làm OCR fallback**:
     - `vanban-app.js` đang ràng buộc cứng chỉ cho phép Mistral OCR, không có fallback sang Gemini Vision khi người dùng đã có sẵn 10 key Gemini hoạt động tốt.

---

## 2. Giải pháp kỹ thuật tổng thể (Architecture & Solution)
1. **Tự động đồng bộ Key từ CSDL tài khoản khi mở trang Quản lý văn bản**:
   - Thêm hàm `syncUserKeysFromServer()` trong `vanban-app.js`: gọi `fetch('api/user_gemini_keys.php', { credentials: 'include', cache: 'no-store' })`.
   - Lưu key tài khoản vào `localStorage`:
     + `localStorage.setItem('global_gemini_keys', JSON.stringify(d.keys))`
     + `localStorage.setItem('global_mistral_keys', JSON.stringify(d.mistral_keys))`
   - Đồng thời gọi `AiDesignConfig.loadHostingFallbackConfig()` để nạp thêm cấu hình fallback từ hosting.
2. **Bổ sung nút "Cấu hình AI" trên thanh điều hướng**:
   - Trên thanh header `renderNav` của `vanban-app.js`, hiển thị nút "Cấu hình AI" kèm số lượng key (ví dụ: `🔑 Gemini 10 · Mistral 1` hoặc nút bấm mở `AiDesignConfig.openModal()`).
3. **Bộ nhận diện OCR đa kênh (Mistral OCR + Gemini Vision Fallback)**:
   - Khi người dùng chụp dán ảnh:
     + **Ưu tiên 1 (Mistral OCR)**: Dùng `window.MistralOcr.ocrImageDataUrl(dataUrl)` nếu có Mistral Key.
     + **Ưu tiên 2 (Gemini Vision Fallback)**: Dùng Gemini API với model `gemini-2.5-flash` / `gemini-3.6-flash` và 10 key Gemini có sẵn để trích xuất số văn bản, ngày tháng, cơ quan ban hành, trích yếu hoặc thông tin chữ ký.
     + **Nếu cả 2 đều chưa có key**: Báo toast hướng dẫn rõ ràng kèm tự động mở bảng Cấu hình AI.

---

## 3. Phạm vi & File tác động
| STT | File | Hành động | Chi tiết |
| :--- | :--- | :--- | :--- |
| 1 | `vanban-app.js` | Sửa đổi | Thêm `syncUserKeysFromServer()`, nút Cấu hình AI, hàm `ocrImageFromDataUrl` (Mistral + Gemini Vision fallback), cập nhật `ingestClipboardImage` & `extractPdf` |
| 2 | `tests/vanban-ocr-clipboard-smoke.js` | Tạo mới | Kiểm thử cơ chế sync key từ `user_gemini_keys.php`, nút Cấu hình AI, fallback Gemini Vision và trích xuất chữ |

---

## 4. Các bước thực hiện chi tiết cho Coder
*(Dành cho Coder: Grok / ChatGPT / `agy` CLI)*

### Bước 1: Chuẩn bị
- Đọc kỹ `docs/handoff/PLAN.md`.
- Đảm bảo không có file `docs/handoff/.lock`.

### Bước 2: Thêm hàm đồng bộ Key tài khoản `syncUserKeysFromServer()` trong `vanban-app.js`
1. Định nghĩa hàm:
   ```javascript
   async function syncUserKeysFromServer() {
       try {
           const res = await fetch('api/user_gemini_keys.php', { credentials: 'include', cache: 'no-store' });
           if (!res.ok) return;
           const d = await res.json();
           const gemini = Array.isArray(d.keys) ? d.keys.filter(Boolean) : [];
           const mistral = Array.isArray(d.mistral_keys) ? d.mistral_keys.filter(Boolean) : [];
           if (gemini.length) localStorage.setItem('global_gemini_keys', JSON.stringify(gemini));
           if (mistral.length) localStorage.setItem('global_mistral_keys', JSON.stringify(mistral));
       } catch (_) { /* giữ key local nếu có */ }
   }
   ```
2. Trong hàm `init()`:
   Gọi đồng bộ khi mở trang:
   ```javascript
   syncUserKeysFromServer();
   if (window.AiDesignConfig?.loadHostingFallbackConfig) {
       AiDesignConfig.loadHostingFallbackConfig().catch(() => {});
   }
   ```

### Bước 3: Thêm nút Cấu hình AI trên thanh điều hướng `renderNav()`
1. Trong `renderNav()`:
   Thêm nút:
   ```html
   <button id="vanbanAiConfigBtn" type="button" class="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 sm:text-sm">
       <i class="fa-solid fa-sliders text-indigo-500"></i> Cấu hình AI
   </button>
   ```
   Gắn sự kiện click gọi `AiDesignConfig.openModal()`.

### Bước 4: Cài đặt OCR đa kênh (Mistral + Gemini Vision Fallback)
1. Thêm helper kiểm tra Gemini:
   ```javascript
   function hasGeminiVision() {
       return window.AiDesignConfig && AiDesignConfig.getApiKeys().length > 0;
   }
   ```
2. Thêm hàm gọi Gemini Vision trực tiếp:
   ```javascript
   async function extractTextViaGeminiVision(dataUrl) {
       const keys = AiDesignConfig.getApiKeys();
       if (!keys.length) throw new Error('Chưa có Gemini API Key.');
       const raw = String(dataUrl || '');
       const base64 = raw.includes('base64,') ? raw.split('base64,')[1] : raw;
       const mime = raw.startsWith('data:image/png') ? 'image/png' : 'image/jpeg';
       const model = AiDesignConfig.getModule() || 'gemini-2.5-flash';
       const key = keys[Math.floor(Math.random() * keys.length)];
       const prompt = 'Hãy đọc và trích xuất toàn bộ chữ trong ảnh văn bản hành chính này. Giữ nguyên vẹn số hiệu văn bản, ngày tháng năm ban hành, tên cơ quan, trích yếu nội dung hoặc thông tin chữ ký. Chỉ trả về văn bản tiếng Việt đã trích xuất, không thêm lời dẫn giải.';
       
       const res = await fetch(
           `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(key)}`,
           {
               method: 'POST',
               headers: { 'Content-Type': 'application/json' },
               body: JSON.stringify({
                   contents: [{
                       parts: [
                           { text: prompt },
                           { inline_data: { mime_type: mime, data: base64 } }
                       ]
                   }],
                   generationConfig: { temperature: 0.1, maxOutputTokens: 2048 }
               })
           }
       );
       const json = await res.json().catch(() => ({}));
       if (!res.ok) throw new Error(json.error?.message || `Lỗi Gemini API (${res.status})`);
       const parts = json.candidates?.[0]?.content?.parts || [];
       let out = '';
       parts.forEach(p => { if (p.text) out += p.text; });
       return out.trim();
   }
   ```
3. Cập nhật hàm OCR ảnh `ocrImageData(dataUrl)`:
   - Nếu `hasMistralOcr()`: gọi `window.MistralOcr.ocrImageDataUrl(dataUrl)`.
   - Nếu không có Mistral nhưng `hasGeminiVision()`: gọi `extractTextViaGeminiVision(dataUrl)` trả về `{ text, mode: 'gemini-vision' }`.
   - Nếu chưa có key nào: hiển thị toast và mở modal cấu hình:
     ```javascript
     toast('Ảnh chụp cần API Key (Mistral hoặc Gemini). Đang mở hộp thoại Cấu hình AI...', 'amber');
     if (window.AiDesignConfig?.openModal) AiDesignConfig.openModal();
     ```
4. Cập nhật `ingestClipboardImage(blob)` và `extractPdf` (cho ảnh/PDF scan) dùng hàm `ocrImageData(dataUrl)`.

### Bước 5: Viết và chạy bộ kiểm thử Smoke Test
Tạo file `tests/vanban-ocr-clipboard-smoke.js`:
- Kiểm tra `vanban-app.js` có chứa lời gọi `syncUserKeysFromServer` và API `api/user_gemini_keys.php`.
- Kiểm tra nút Cấu hình AI và sự kiện `AiDesignConfig.openModal()`.
- Kiểm tra cơ chế Gemini Vision fallback.
- Chạy toàn bộ các test hiện có:
  ```powershell
  node tests/vanban-ocr-clipboard-smoke.js
  node tests/vanban-chuyenmon-signature-smoke.js
  python tests/vanban-chuyenmon-root-smoke.py
  node tests/vanban-display-saved-smoke.js
  ```

### Bước 6: Hoàn tất bàn giao
- Ghi nhận chi tiết vào `docs/handoff/IMPLEMENT.md`.
- Cập nhật kết quả kiểm thử vào `docs/handoff/VERIFY.md`.

---

## 5. Tiêu chí nghiệm thu (Verify Checklist)
- [ ] Khi tải trang Quản lý văn bản, hệ thống tự động đồng bộ key từ `api/user_gemini_keys.php` vào `localStorage`.
- [ ] Người dùng đã nạp Mistral 1 key và Gemini 10 key trên trang chủ sẽ tự động có key hoạt động ngay trên Quản lý văn bản mà không bị báo lỗi thiếu key.
- [ ] Khi chụp dán ảnh số/ngày văn bản: OCR thành công bằng Mistral (hoặc fallback Gemini Vision), điền tự động vào trường số, ngày, trích yếu.
- [ ] Trang Quản lý văn bản có nút "Cấu hình AI" để kiểm tra và nạp thêm key.
- [ ] Tất cả các smoke test chạy thành công (PASS).
