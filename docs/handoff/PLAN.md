# PLAN: Tự Động Phân Tuyến Mô Hình (Gemini 2.5 Flash cho Nhận Diện SGK/Ảnh + Gemini 3 Flash Preview cho Soạn Giảng)

## 1. Tổng Quan & Yêu Cầu Cốt Lõi

### Bối cảnh:
Khi chạy `canvas_soankhbd.html` trên **Gemini Canvas (`gemini.google.com`)**:
1. Bước nhận diện/phân tích SGK bị đứng ở mức **90%** do gửi trực tiếp batch ảnh/media SGK tới mô hình `gemini-3-flash-preview`. Trong môi trường iframe Canvas, model 3-flash preview xử lý multimodal vision nặng thường bị stall, nghẽn hàng đợi hoặc timeout.
2. Mô hình `gemini-2.5-flash` (như đang dùng rất nhanh và ổn định ở `taobaocao.html`) có khả năng OCR/Vision đọc ảnh và văn bản SGK vượt trội, xử lý xong chỉ trong vài giây.
3. **Chỉ đạo dứt khoát của người dùng**:
   > *"vậy chuyển tự động đi. Gemini-2.5-flash nó nhận diện văn bản, còn lại là 3-lash-preview. Nãy giờ tôi nói với bạn mà vẫn đứng 90%. chắc lỗi rồi"*
4. **Kỷ luật sư phạm**:
   - Tuyệt đối **KHÔNG gộp hay làm xáo trộn `systemInstruction`** vào prompt. Giữ nguyên trường `systemInstruction` độc lập để bảo toàn tính chuẩn mực sư phạm (chuẩn 5512, bảng phân vai GV-HS, NLS, AI).
   - Tuyệt đối **KHÔNG đặt `credentials: "omit"`** để tránh lỗi 401 trên Canvas.

---

## 2. Giải Pháp Kỹ Thuật

Tại hàm điều phối mạng trung tâm `geminiAPI.fetchGeminiGenerate` trong `canvas_soankhbd.html`:

1. **Phát hiện tự động tác vụ Vision / Phân tích SGK**:
   Kiểm tra nếu payload chứa dữ liệu ảnh (`inlineData`, `fileData`), hoặc tham số model yêu cầu `image`:
   ```javascript
   const hasMedia = Boolean(
     /image/i.test(String(model || "")) ||
     (payload && Array.isArray(payload.contents) && payload.contents.some(c => Array.isArray(c.parts) && c.parts.some(p => p && (p.inlineData || p.fileData))))
   );
   ```

2. **Tự động gán mô hình tối ưu theo loại tác vụ**:
   - **Nhận diện SGK / Hình ảnh / OCR (`hasMedia === true`)**: Tự động dùng `gemini-2.5-flash` (nhanh, chính xác, không bị đứng ở 90%).
   - **Soạn thảo giáo án / Nội dung văn bản (`hasMedia === false`)**: Dùng `gemini-3-flash-preview` (tư duy sâu, chất lượng nội dung cao).

3. **Cơ chế dự phòng (Fallback)**:
   - Nếu gọi `gemini-3-flash-preview` mà Canvas trả về HTTP 401, 403, 404, 429 hoặc 503, tự động chuyển hướng gọi lại bằng `gemini-2.5-flash`.

4. **Làm sạch Payload an toàn**:
   - Sao chép nguyên vẹn `systemInstruction` và `contents`.
   - Chỉ loại bỏ `thinkingConfig` (nếu có) để tránh lỗi không tương thích trên các bản Canvas.

---

## 3. Chi Tiết Thực Hiện Cho Coder

### Bước 1: Cập nhật `geminiAPI.fetchGeminiGenerate` trong `canvas_soankhbd.html`
Vị trí: khoảng dòng 1396 trong thẻ `<script id="canvasCoreBootstrap">`:

```javascript
      geminiAPI.fetchGeminiGenerate = async function (model, key, payload, signal, timeoutMs) {
        // 1. Kiểm tra tự động xem payload có chứa dữ liệu ảnh/media SGK không
        const hasMedia = Boolean(
          /image/i.test(String(model || "")) ||
          (payload && Array.isArray(payload.contents) && payload.contents.some(c => Array.isArray(c.parts) && c.parts.some(p => p && (p.inlineData || p.fileData))))
        );

        // 2. Phân tuyến tự động:
        // - Nhận diện ảnh/văn bản SGK: dùng gemini-2.5-flash (tốc độ cao, không nghẽn 90%)
        // - Soạn thảo bài giảng/giáo án: dùng gemini-3-flash-preview
        const fallbackModel = "gemini-2.5-flash";
        const primaryModel = hasMedia ? fallbackModel : (MODEL || "gemini-3-flash-preview");

        // Giữ nguyên 100% payload sư phạm (systemInstruction, contents, v.v.)
        // Chỉ dọn sạch trường thinkingConfig nếu có để tránh lỗi 400
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

        // Nếu model preview gặp lỗi HTTP 401/403/404/429/503, tự động fallback sang gemini-2.5-flash
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

### Bước 2: Cập nhật kiểm thử tự động `tests/canvas-soankhbd-smoke.js`
Thêm các assertion xác thực:
1. `hasMedia` tự động kiểm tra `inlineData` / `fileData`.
2. Khẳng định `hasMedia ? fallbackModel : ...` để SGK luôn chạy `gemini-2.5-flash`.
3. Kiểm tra không chứa `credentials: "omit"`.
4. Chạy kiểm thử:
   ```powershell
   node tests/canvas-soankhbd-smoke.js
   ```

---

## 4. Kế Hoạch Nghiệm Thu (Verification)

1. Chạy pass toàn bộ test tự động:
   `node tests/canvas-soankhbd-smoke.js`
2. Mở file `canvas_soankhbd.html`, copy toàn bộ mã nguồn dán vào cửa sổ **Gemini Canvas trên `gemini.google.com`**.
3. Tải lên trang SGK và bấm **Phân tích SGK** hoặc **TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)**:
   - Giai đoạn nhận diện SGK (20% -> 90% -> 100%): gọi `gemini-2.5-flash`, xử lý trơn tru chỉ trong 5-10 giây, không còn hiện tượng treo ở 90%.
   - Giai đoạn soạn các mục giáo án: gọi `gemini-3-flash-preview` để cho chất lượng sư phạm cao nhất.
   - Toàn bộ chuẩn 5512, bảng phân vai GV-HS, NLS, AI giữ nguyên vẹn 100%.
