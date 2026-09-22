# PLAN: Đồng Bộ Cơ Chế Gọi Gemini Canvas Trực Tiếp (Không Cần API Key) Theo Chuẩn `taobaocao.html`

## 1. Tổng Quan Vấn Đề

### Ngữ cảnh sử dụng thực tế của người dùng:
Người dùng sử dụng file `canvas_soankhbd.html` bằng cách **copy toàn bộ mã nguồn và dán vào khung cửa sổ Canvas của Google Gemini (trên `gemini.google.com`)**.
- File `taobaocao.html` khi dán vào Gemini Canvas chạy sinh văn bản thành công mà **không cần API key**.
- File `canvas_soankhbd.html` khi dán vào Gemini Canvas lại báo lỗi:
  ```text
  [03:31:18 PM] [CONSOLE_ERROR] 1-Click Generate Error: Error: Lỗi Gemini API (401): HTTP 401: Something went wrong
  Stack: Error: Lỗi Gemini API (401): HTTP 401: Something went wrong
      at GeminiAPIManager._generateContentInternal (https://hoangthiencm.id.vn/js/khbd-gemini.js?v=20260916-canvas-module-v9:1:40644)
  ```

---

## 2. Nguyên Nhân Kỹ Thuật (Root Cause)

So sánh giữa cơ chế gọi Gemini trong `backupcode viettailieu/taobaocao.html` (chạy thành công) và `canvas_soankhbd.html` (bị lỗi 401):

1. **Thuộc tính `credentials: "omit"` trong `fetch` (Nguyên nhân chí mạng gây 401)**:
   - Trong `canvas_soankhbd.html` (dòng 1400):
     ```javascript
     const response = await this.fetchWithTimeout(GEMINI_DIRECT_ENDPOINT + useModel + ":generateContent", {
       method: "POST",
       headers: { "Content-Type": "application/json" },
       credentials: "omit", // <--- LỖI NẰM Ở ĐÂY
       body: JSON.stringify(payload),
       signal: signal
     }, timeoutMs || 95000);
     ```
   - Trong môi trường Gemini Canvas (`gemini.google.com`), khung xem trước (iframe) dựa vào phiên đăng nhập (cookies/ambient credentials) của tài khoản Google để ủy quyền cho lệnh gọi đến `https://generativelanguage.googleapis.com/...`.
   - Việc chỉ định `credentials: "omit"` đã **ra lệnh cho trình duyệt tước bỏ toàn bộ cookies và thông tin xác thực phiên làm việc**, khiến máy chủ Google nhận diện đây là yêu cầu nặc danh không có danh tính $\rightarrow$ Google lập tức trả về `HTTP 401: Something went wrong`.
   - Trong `taobaocao.html` (dòng 7332): Gọi `fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(requestBody) })` — **hoàn toàn không có `credentials: "omit"`**.

2. **Cấu trúc `payload` không tương thích với Gemini Canvas Direct API**:
   - `khbd-gemini.js` gửi payload chứa các trường đặc thù của Google AI Studio như:
     `thinkingConfig: { thinkingBudget: 0 }` và `systemInstruction: { parts: [...] }`.
   - Trong môi trường Gemini Canvas, endpoint trực tiếp không hỗ trợ `thinkingConfig` hoặc định dạng `systemInstruction` riêng biệt, dẫn đến lỗi từ chối yêu cầu (400/401).
   - Trong `taobaocao.html`: Toàn bộ chỉ dẫn hệ thống được gộp thẳng vào prompt text:
     `contents: [{ parts: [{ text: effectivePrompt }] }]`
     và `generationConfig: { temperature, topP, topK, maxOutputTokens }`. Không có `thinkingConfig`.

3. **Thiếu cơ chế tự động Fallback Model khi Canvas chặn preview model**:
   - `canvas_soankhbd.html` đang khóa cứng `gemini-3-flash-preview`.
   - Trong `taobaocao.html`: Mặc dù hỗ trợ `gemini-3-flash-preview`, nếu model này gặp lỗi hoặc không khả dụng, hệ thống tự động đổi sang `gemini-2.5-flash` để đảm bảo luôn tạo được nội dung.

---

## 3. Chi Tiết Thực Hiện Cho Coder

Coder cần cập nhật `canvas_soankhbd.html` để đồng bộ hoàn toàn cơ chế gọi trực tiếp giống `taobaocao.html`:

### Bước 1: Chuẩn hóa hàm gọi Gemini trong `canvas_soankhbd.html`
Tại khối override `geminiAPI.fetchGeminiGenerate` trong `canvas_soankhbd.html`:
1. **Xóa bỏ hoàn toàn `credentials: "omit"`**.
2. **Chuẩn hóa requestBody theo chuẩn `taobaocao.html`**:
   - Nếu có `systemInstruction`, ghép nội dung của nó vào phần đầu của prompt text (hoặc gộp vào parts của user).
   - Loại bỏ `thinkingConfig` (không gửi `thinkingConfig` khi gọi direct trong Canvas).
   - Giữ nguyên `generationConfig` chuẩn: `temperature`, `topP`, `maxOutputTokens`.
   - Hỗ trợ gửi kèm ảnh (`inlineData`) nếu có xử lý OCR/ảnh SGK.
3. **Cơ chế Fallback Model tự động**:
   - Thử gọi với model ưu tiên (mặc định `gemini-3-flash-preview` hoặc model người dùng chọn).
   - Nếu phản hồi trả về HTTP 401, 403 hoặc 404 (do Canvas chưa mở preview model đó cho phiên hiện tại), tự động fallback gọi lại bằng `gemini-2.5-flash` giống `taobaocao.html`.

Đoạn mã mẫu triển khai cho `geminiAPI.fetchGeminiGenerate`:
```javascript
geminiAPI.fetchGeminiGenerate = async function (model, key, payload, signal, timeoutMs) {
  const primaryModel = /image/i.test(String(model || "")) ? model : (MODEL || "gemini-3-flash-preview");
  const fallbackModel = "gemini-2.5-flash";
  
  // Chuẩn hóa payload tương thích 100% với Gemini Canvas (giống taobaocao.html)
  function formatCanvasBody(sourcePayload) {
    const rawContents = sourcePayload.contents || [];
    let systemText = "";
    if (sourcePayload.systemInstruction?.parts) {
      systemText = sourcePayload.systemInstruction.parts.map(p => p.text || "").join("\n").trim();
    }
    
    const formattedContents = rawContents.map(c => {
      const parts = (c.parts || []).map(p => {
        if (p.inlineData) return { inlineData: p.inlineData };
        let text = p.text || "";
        if (systemText && c.role === "user") {
          text = `[CHỈ DẪN HỆ THỐNG]\n${systemText}\n\n[NỘI DUNG YÊU CẦU]\n${text}`;
          systemText = ""; // Chỉ ghép một lần vào đầu
        }
        return { text };
      });
      return { parts };
    });
    
    const genConfig = {
      temperature: sourcePayload.generationConfig?.temperature ?? 0.3,
      topP: sourcePayload.generationConfig?.topP ?? 0.95,
      maxOutputTokens: sourcePayload.generationConfig?.maxOutputTokens || 8192
    };
    if (sourcePayload.generationConfig?.topK) genConfig.topK = sourcePayload.generationConfig.topK;
    
    return {
      contents: formattedContents,
      generationConfig: genConfig
    };
  }

  async function executeCall(targetModel) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${targetModel}:generateContent`;
    const requestBody = formatCanvasBody(payload);
    
    // GỌI TRỰC TIẾP GIỐNG TAOBAOCAO.HTML: Không có credentials: "omit"
    return await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
      signal: signal
    });
  }

  let response = await executeCall(primaryModel);
  let activeUsedModel = primaryModel;
  
  // Nếu model preview bị 401/403/404, tự động fallback sang gemini-2.5-flash
  if (!response.ok && (response.status === 401 || response.status === 403 || response.status === 404) && primaryModel !== fallbackModel) {
    console.warn(`[Gemini Canvas] Model ${primaryModel} trả về HTTP ${response.status}. Tự động fallback sang ${fallbackModel}...`);
    response = await executeCall(fallbackModel);
    activeUsedModel = fallbackModel;
  }
  
  const metadata = { route: "canvas_direct", model: activeUsedModel };
  geminiAPI.lastCanvasMeta = metadata;
  geminiAPI.emitGeminiStatus({
    type: "canvas_direct",
    message: "Gemini Canvas: gọi trực tiếp · " + activeUsedModel,
    route: metadata.route,
    model: activeUsedModel
  });

  if (response.ok) {
    setBanner("Gemini Canvas đang gọi trực tiếp (" + activeUsedModel + ") không cần API key.", "ok");
  } else {
    setBanner("Gemini Canvas báo lỗi (HTTP " + response.status + ").", "err");
  }
  
  response.canvasMeta = metadata;
  return response;
};
```

### Bước 2: Cập nhật kiểm thử tự động trong `tests/canvas-soankhbd-smoke.js`
1. Đảm bảo test kiểm tra:
   - `canvas_soankhbd.html` **KHÔNG** chứa `credentials: "omit"` trong lệnh gọi Gemini Direct.
   - Có cơ chế format payload tương thích Canvas (`formatCanvasBody` hoặc tương đương).
   - Có cơ chế fallback về `gemini-2.5-flash` khi model preview bị lỗi xác thực.
2. Chạy test:
   ```powershell
   node tests/canvas-soankhbd-smoke.js
   ```

---

## 4. Kế Hoạch Nghiệm Thu (Verification)

1. Chạy pass toàn bộ test tự động:
   `node tests/canvas-soankhbd-smoke.js`
2. Mở file `canvas_soankhbd.html`, copy toàn bộ mã nguồn.
3. Dán vào khung Gemini Canvas trên `gemini.google.com`.
4. Bấm thử nghiệm **TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)** hoặc tạo từng mục.
5. **Kỳ vọng:** Lệnh gọi kết nối thành công mượt mà như `taobaocao.html`, không còn lỗi `HTTP 401: Something went wrong`.
