# Kế hoạch thực hiện (PLAN) - Khắc phục lỗi OCR dán ảnh clipboard & Đồng bộ Cấu hình AI trong Quản lý văn bản

## 1. Mục tiêu
- Khắc phục lỗi khi người dùng chụp màn hình số, ngày tháng, trích yếu hoặc vùng chữ ký văn bản rồi dán (Ctrl+V hoặc nút "Dán nhanh từ Clipboard") vào ô nhập liệu: không còn bị chặn cứng bởi thông báo lỗi chỉ hỗ trợ Mistral OCR.
- Tự động đồng bộ API Key từ server (`api/user_gemini_keys.php`) và cấu hình hosting (`loadHostingFallbackConfig()`) khi khởi tạo trang Quản lý văn bản (`quanlyvanban-*.html`).
- Cung cấp nút "Cấu hình AI" trên thanh điều hướng để người dùng có thể chủ động kiểm tra, nạp key Gemini / Mistral OCR bất kỳ lúc nào.
- Mở rộng cơ chế nhận diện OCR ảnh đa kênh: Ưu tiên Mistral OCR (nếu có key), tự động fallback sang Gemini Vision (sử dụng API Key Gemini có sẵn), và nếu chưa có key nào thì hiện hướng dẫn trực quan đồng thời mở bảng Cấu hình AI.
- Bảo đảm giữ nguyên toàn bộ các luồng nhận diện cũ: PDF lớp chữ (`text-layer`), chữ ký số nhị phân (`/Type /Sig`), nhận diện regex ngày/số VB, cũng như Mistral OCR khi đã có key.

---

## 2. Danh sách file dự kiến tác động
| STT | Đường dẫn file | Thao tác | Mục đích / Nội dung tác động |
| :-- | :--- | :--- | :--- |
| 1 | `vanban-app.js` | Kiểm tra / Cập nhật | Bổ sung/chuẩn hóa hàm `syncUserKeysFromServer()`, gọi `loadHostingFallbackConfig()`, nút `#vanbanAiConfigBtn`, hàm `hasGeminiVision()`, `extractTextViaGeminiVision()`, `ocrImageData()`, và luồng `ingestClipboardImage()`. |
| 2 | `quanlyvanban-chuyenmon.html` | Kiểm tra / Cập nhật | Đảm bảo nạp đầy đủ script `ai-design-config.js` và `mistral-ocr-client.js`. |
| 3 | `quanlyvanban-hanhchinh.html` | Kiểm tra / Cập nhật | Đảm bảo nạp đầy đủ script `ai-design-config.js` và `mistral-ocr-client.js`. |
| 4 | `quanlyvanban-dang.html` | Kiểm tra / Cập nhật | Đảm bảo nạp đầy đủ script `ai-design-config.js` và `mistral-ocr-client.js`. |
| 5 | `tests/vanban-ocr-clipboard-smoke.js` | Tạo mới / Cập nhật | Test tự động kiểm tra cú pháp, sự tồn tại của các hàm đồng bộ key, nút cấu hình AI, fallback Gemini Vision và không còn lỗi chặn Mistral cứng. |

---

## 3. Các bước thực hiện chi tiết cho Coder

### Bước 1: Tiếp nhận và chuẩn bị
- Đọc kỹ yêu cầu trong `docs/handoff/PLAN.md`.
- Xóa file `docs/handoff/.lock` trước khi sửa source code. Sau khi sửa code xong, tạo lại file `docs/handoff/.lock` với nội dung `LOCK`.
- Tuyệt đối không sửa file ngoài danh sách đã nêu.

### Bước 2: Chuẩn hóa cơ chế đồng bộ Key và Cấu hình AI trong `vanban-app.js`
1. Đảm bảo có hàm đồng bộ key người dùng từ server:
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
   - Gọi `syncUserKeysFromServer()`.
   - Gọi `AiDesignConfig.loadHostingFallbackConfig().catch(() => {})` nếu hàm này tồn tại.

### Bước 3: Nút "Cấu hình AI" trong thanh điều hướng (`renderNav`)
1. Trong hàm `renderNav()` của `vanban-app.js`:
   - Bổ sung nút:
     ```html
     <button id="vanbanAiConfigBtn" type="button" class="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 sm:text-sm">
         <i class="fa-solid fa-sliders text-indigo-500"></i> Cấu hình AI
     </button>
     ```
   - Gắn sự kiện click cho `$('vanbanAiConfigBtn')`:
     ```javascript
     $('vanbanAiConfigBtn')?.addEventListener('click', () => {
         if (window.AiDesignConfig?.openModal) AiDesignConfig.openModal();
     });
     ```

### Bước 4: Triển khai nhận diện OCR đa kênh (Mistral OCR + Gemini Vision Fallback)
1. Thêm hàm kiểm tra Gemini Vision:
   ```javascript
   function hasGeminiVision() {
       return window.AiDesignConfig && AiDesignConfig.getApiKeys().length > 0;
   }
   ```
2. Triển khai hàm trích xuất text từ ảnh bằng Gemini Vision:
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
3. Chuẩn hóa hàm `ocrImageData(dataUrl)`:
   ```javascript
   async function ocrImageData(dataUrl) {
       if (hasMistralOcr()) {
           const res = await window.MistralOcr.ocrImageDataUrl(dataUrl);
           return { text: res.text || res.markdown || '', mode: 'mistral-ocr' };
       }
       if (hasGeminiVision()) {
           const text = await extractTextViaGeminiVision(dataUrl);
           return { text, mode: 'gemini-vision' };
       }
       toast('Ảnh chụp cần API Key (Mistral hoặc Gemini). Đang mở hộp thoại Cấu hình AI...', 'amber');
       if (window.AiDesignConfig?.openModal) AiDesignConfig.openModal();
       throw new Error('Chưa có API Key OCR.');
   }
   ```
4. Kiểm tra `ingestClipboardImage(blob)`: Sử dụng `ocrImageData(dataUrl)` thay vì kiểm tra cứng chỉ riêng Mistral OCR.

### Bước 5: Kiểm tra các tệp HTML giao diện
- Kiểm tra `quanlyvanban-chuyenmon.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html`:
  - Đảm bảo thẻ `<script src="ai-design-config.js..."></script>` và `<script src="mistral-ocr-client.js..."></script>` đã được nạp ở phần `<head>`.
  - Giữ nguyên cấu trúc giao diện và layout hiện có.

### Bước 6: Kiểm thử tự động (Smoke Test)
- Cập nhật hoặc chạy kiểm thử `tests/vanban-ocr-clipboard-smoke.js`.
- Chạy toàn bộ các bộ test liên quan đến văn bản để đảm bảo không có bất kỳ hồi quy nào:
  ```powershell
  node tests/vanban-ocr-clipboard-smoke.js
  node tests/vanban-chuyenmon-signature-smoke.js
  node tests/vanban-display-saved-smoke.js
  python tests/vanban-chuyenmon-root-smoke.py
  ```

---

## 4. Rủi ro và Giải pháp
1. **Rủi ro API Key Gemini không có quyền truy cập Vision hoặc model bị deprecated**:
   - *Giải pháp*: Mặc định chọn model thị giác thông dụng `gemini-2.5-flash` hoặc model đang chọn trong `AiDesignConfig.getModule()`. Hỗ trợ xoay vòng ngẫu nhiên danh sách key người dùng đã lưu.
2. **Rủi ro xung đột giữa lớp chữ PDF và OCR ảnh**:
   - *Giải pháp*: Giữ nguyên luồng PDF ưu tiên đọc lớp chữ (`extractPdfTextLayer`) và chữ ký nhị phân (`/Type /Sig`), chỉ khi text layer quá ngắn hoặc kém mới kích hoạt OCR ảnh trang đầu.
3. **Rủi ro người dùng chưa có cả Mistral lẫn Gemini key**:
   - *Giải pháp*: Không throw error làm đơ ứng dụng; hiển thị toast màu hổ phách cảnh báo rõ ràng và tự động mở modal `AiDesignConfig.openModal()` để người dùng nạp key ngay.

---

## 5. Lệnh máy kiểm thử cụ thể (Test Commands)
Coder cần chạy và đảm bảo tất cả các lệnh sau đều PASS:
```powershell
node tests/vanban-ocr-clipboard-smoke.js
node tests/vanban-chuyenmon-signature-smoke.js
node tests/vanban-display-saved-smoke.js
python tests/vanban-chuyenmon-root-smoke.py
```
