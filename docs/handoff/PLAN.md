# PLAN: Chuyển Dứt Điểm gemini-2.5-flash Cho Khâu Trích Xuất Ảnh / SGK Trong canvas_soankhbd.html

## 1. Nguyên Nhân Hiện Tại Vẫn Thấy Gọi gemini-3-flash-preview Khi Đọc Ảnh

Trong console của trình duyệt hiện tại vẫn ghi nhận:
```text
khbd-gemini.js?v=20260916-canvas-module-v9:1 [Gemini] Đang gọi Gemini (gemini-3-flash-preview)...
```

**Nguyên nhân gốc rễ**:
1. Trong file `canvas_soankhbd.html`, `geminiAPI.selectedModel` đang được gán cố định bằng `MODEL` (`"gemini-3-flash-preview"`).
2. Khi khâu phân tích SGK / OCR gọi hàm `geminiAPI.generateContent(prompt, images, ...)`:
   File `js/khbd-gemini.js` đọc `const selectedModel = this.selectedModel;` và ngay lập tức ghi log ra console:
   `[Gemini] Đang gọi Gemini (${activeModel})...` (vẫn là `gemini-3-flash-preview`) **trước khi** hàm `fetchGeminiGenerate` được kích hoạt!
3. Do đó, việc can thiệp chỉ ở tầng `fetchGeminiGenerate` là chưa đủ: `generateContent` vẫn khởi tạo với `gemini-3-flash-preview`, gây hiểu nhầm và có thể gửi model 3-flash vào các luồng xử lý trước đó.

---

## 2. Giải Pháp Toàn Diện (2 Tầng Đồng Bộ)

Trong `canvas_soankhbd.html` (khối `<script id="canvasCoreBootstrap">`):

### Tầng 1: Can thiệp ngay tại `geminiAPI.generateContent`
Khi nhận vào tham số `images` (hoặc cờ trích xuất SGK):
- Tự động gán `this.selectedModel = "gemini-2.5-flash"` trước khi gọi logic nạp nội dung.
- Khi không có ảnh (soạn thảo giáo án văn bản 5512, 1-Click): giữ nguyên `this.selectedModel = MODEL || "gemini-3-flash-preview"`.
- Nhờ vậy, `khbd-gemini.js` sẽ in đúng log:
  `[Gemini] Đang gọi Gemini (gemini-2.5-flash)...`
  và toàn bộ thanh tiến trình, footer trạng thái đều hiển thị chính xác `gemini-2.5-flash`.

### Tầng 2: Đồng bộ tại `geminiAPI.fetchGeminiGenerate`
Đảm bảo khi phát hiện `hasMedia` (ảnh, inlineData, fileData, hoặc model có chứa 2.5/image):
- Luôn gửi request tới `gemini-2.5-flash`.
- Text drafting gửi tới `gemini-3-flash-preview`, tự động fallback về `gemini-2.5-flash` nếu gặp lỗi 401/403/404/429/503.
- Bảo toàn nguyên vẹn 100% `systemInstruction` và prompt sư phạm.

---

## 3. Chi Tiết Thay Đổi Trong `canvas_soankhbd.html`

Vị trí: thẻ `<script id="canvasCoreBootstrap">` (khoảng dòng 1392-1437):

```javascript
      // --- TẦNG 1: TỰ ĐỘNG CHUYỂN MODEL KHI CÓ ẢNH / MEDIA ---
      const canvasGenerateContent = geminiAPI.generateContent.bind(geminiAPI);
      geminiAPI.generateContent = function (prompt, images, systemRole, temperature, signal, options) {
        const hasMedia = (Array.isArray(images) && images.length > 0) || Boolean(options && (options.hasMedia || options.purpose === "textbook_analysis"));
        const targetModel = hasMedia ? "gemini-2.5-flash" : (MODEL || "gemini-3-flash-preview");
        const prevModel = this.selectedModel;
        this.selectedModel = targetModel;
        try {
          return canvasGenerateContent(prompt, images, systemRole, temperature, signal, Object.assign({}, options || {}, { allowEmptyKey: true }));
        } finally {
          this.selectedModel = prevModel;
        }
      };

      // --- TẦNG 2: ĐIỀU PHỐI NETWORK VÀ GỌI DIRECT API ---
      geminiAPI.fetchGeminiGenerate = async function (model, key, payload, signal, timeoutMs) {
        const hasMedia = Boolean(
          /2\.5/i.test(String(model || "")) ||
          /image/i.test(String(model || "")) ||
          (payload && Array.isArray(payload.contents) && payload.contents.some(c => Array.isArray(c.parts) && c.parts.some(p => p && (p.inlineData || p.fileData))))
        );
        const fallbackModel = "gemini-2.5-flash";
        const primaryModel = hasMedia ? fallbackModel : (MODEL || "gemini-3-flash-preview");

        function cleanPayloadForCanvas(sourcePayload) {
          const copy = JSON.parse(JSON.stringify(sourcePayload || {}));
          if (copy.generationConfig && copy.generationConfig.thinkingConfig) {
            delete copy.generationConfig.thinkingConfig;
          }
          return copy;
        }

        const executeCall = async (targetModel) => this.fetchWithTimeout(GEMINI_DIRECT_ENDPOINT + targetModel + ":generateContent", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(cleanPayloadForCanvas(payload)),
          signal: signal
        }, timeoutMs || 95000);

        let response = await executeCall(primaryModel);
        let activeUsedModel = primaryModel;
        if (!response.ok && (response.status === 401 || response.status === 403 || response.status === 404 || response.status === 429 || response.status === 503) && primaryModel !== fallbackModel) {
          console.warn("[Gemini Canvas] Model " + primaryModel + " trả về HTTP " + response.status + ". Tự động fallback sang " + fallbackModel + "...");
          response = await executeCall(fallbackModel);
          activeUsedModel = fallbackModel;
        }

        const metadata = { route: "canvas_direct", model: activeUsedModel, hasMedia: hasMedia };
        geminiAPI.lastCanvasMeta = metadata;
        geminiAPI.emitGeminiStatus({
          type: "canvas_direct",
          message: "Gemini Canvas: gọi trực tiếp · " + activeUsedModel + (hasMedia ? " (nhận diện SGK)" : " (soạn KHBD)"),
          route: metadata.route,
          model: activeUsedModel
        });

        if (response.ok) {
          setBanner("Gemini Canvas đang gọi trực tiếp (" + activeUsedModel + "), không dùng proxy hoặc API key hệ thống.", "ok");
        } else {
          setBanner("Gemini Canvas báo lỗi (HTTP " + response.status + "). Không dùng tuyến hệ thống.", "err");
        }

        response.canvasMeta = metadata;
        return response;
      };
```

---

## 4. Kiểm Thử & Nghiệm Thu

1. Chạy test tự động:
   ```powershell
   node tests/canvas-soankhbd-smoke.js
   ```
2. Copy `canvas_soankhbd.html` dán vào Gemini Canvas:
   - Tải ảnh SGK và bấm nhận diện: Console bắt buộc hiện `[Gemini] Đang gọi Gemini (gemini-2.5-flash)...` và hoàn thành nhận diện SGK trong 5–10s, không đứng ở 90%.
   - Bấm tạo giáo án: Console hiện `[Gemini] Đang gọi Gemini (gemini-3-flash-preview)...` để tạo nội dung sâu.
