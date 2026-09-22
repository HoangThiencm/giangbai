# PLAN: Mở Khóa Quyền Gọi Gemini Canvas Trực Tiếp (Không Cần Key) & Giữ Nguyên 100% Kỷ Luật Soạn Giảng

## 1. Tổng Quan & Yêu Cầu Cốt Lõi

### Bối cảnh:
Người dùng copy mã nguồn `canvas_soankhbd.html` dán vào cửa sổ **Gemini Canvas (trên `gemini.google.com`)** để chạy.
- Trước đó gặp lỗi:
  ```text
  [CONSOLE_ERROR] 1-Click Generate Error: Error: Lỗi Gemini API (401): HTTP 401: Something went wrong
  ```
- **Yêu cầu quan trọng từ người dùng**:
  Tuyệt đối **KHÔNG gộp hay làm xáo trộn `systemInstruction`** vào nội dung prompt thông thường, vì việc này làm thay đổi độ chú ý của mô hình AI và gây sai lệch, giảm tính kỷ luật chuẩn mực của giáo án (chuẩn 5512, bảng phân vai GV-HS, NLS, AI).
  Chỉ can thiệp kỹ thuật ở **tầng mạng (Network)** để khắc phục lỗi 401.

---

## 2. Nguyên Nhân Kỹ Thuật

1. **Lỗi 401 do cờ `credentials: "omit"`**:
   Trong `canvas_soankhbd.html` (dòng 1400):
   ```javascript
   const response = await this.fetchWithTimeout(GEMINI_DIRECT_ENDPOINT + useModel + ":generateContent", {
     method: "POST",
     headers: { "Content-Type": "application/json" },
     credentials: "omit", // <--- NGUYÊN NHÂN DUY NHẤT GÂY LỖI 401
     body: JSON.stringify(payload),
     signal: signal
   }, timeoutMs || 95000);
   ```
   Trong iframe của Gemini Canvas (`gemini.google.com`), Google dựa vào thông tin xác thực phiên (ambient credentials/session) của tài khoản Google để cho phép gọi API trực tiếp. Khi có cờ `credentials: "omit"`, trình duyệt bị bắt buộc tước bỏ toàn bộ cookies/phiên này, dẫn đến việc Google từ chối kết nối với mã lỗi 401.
2. **`systemInstruction` hoàn toàn hợp lệ**:
   Endpoint `https://generativelanguage.googleapis.com/v1beta/models/...:generateContent` hỗ trợ trường `systemInstruction: { parts: [...] }` là tính năng tiêu chuẩn cốt lõi. Không cần và không được gộp vào prompt.

---

## 3. Chi Tiết Thực Hiện Cho Coder

Chỉnh sửa trong `canvas_soankhbd.html`:

### Bước 1: Điều chỉnh lệnh gọi `fetch` trong `canvas_soankhbd.html`
Tại khối `geminiAPI.fetchGeminiGenerate`:
1. **Xóa bỏ thuộc tính `credentials: "omit"`**.
2. **Giữ nguyên 100% cấu trúc `payload`** (bao gồm cả `systemInstruction`, `contents`, `generationConfig`).
   - *Lưu ý nhỏ*: Chỉ lọc bỏ trường `thinkingConfig: { thinkingBudget: 0 }` trong `payload.generationConfig` nếu có (để tránh lỗi 400 trên một số phiên bản model của Canvas). Toàn bộ `systemInstruction` và prompt giữ nguyên vẹn.
3. **Thêm cơ chế tự động Fallback Model**:
   - Mặc định gọi model ưu tiên (`gemini-3-flash-preview` hoặc model được cấu hình).
   - Nếu phản hồi trả về mã lỗi 401, 403 hoặc 404 (do phiên Canvas hiện tại chưa mở preview model đó), tự động gọi lại với model ổn định `gemini-2.5-flash`.

Đoạn mã mẫu hoàn chỉnh cho `canvas_soankhbd.html`:
```javascript
geminiAPI.fetchGeminiGenerate = async function (model, key, payload, signal, timeoutMs) {
  const primaryModel = /image/i.test(String(model || "")) ? model : (MODEL || "gemini-3-flash-preview");
  const fallbackModel = "gemini-2.5-flash";

  // Giữ nguyên 100% payload sư phạm (systemInstruction, contents, v.v.), chỉ dọn sạch trường không tương thích
  function cleanPayloadForCanvas(srcPayload) {
    const copy = JSON.parse(JSON.stringify(srcPayload || {}));
    if (copy.generationConfig && copy.generationConfig.thinkingConfig) {
      delete copy.generationConfig.thinkingConfig;
    }
    return copy;
  }

  async function executeCall(targetModel) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${targetModel}:generateContent`;
    const cleanBody = cleanPayloadForCanvas(payload);

    // GỌI NGUYÊN BẢN TRỰC TIẾP: Không có credentials: "omit"
    return await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cleanBody),
      signal: signal
    });
  }

  let response = await executeCall(primaryModel);
  let activeUsedModel = primaryModel;

  // Nếu preview model bị lỗi quyền 401/403/404, tự động fallback sang gemini-2.5-flash
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

### Bước 2: Cập nhật file kiểm thử `tests/canvas-soankhbd-smoke.js`
Đảm bảo kiểm tra:
1. `canvas_soankhbd.html` **KHÔNG** chứa `credentials: "omit"`.
2. Có hàm làm sạch payload bảo toàn `systemInstruction` (`cleanPayloadForCanvas` hoặc tương đương).
3. Có cơ chế fallback model sang `gemini-2.5-flash`.
4. Chạy kiểm thử:
   ```powershell
   node tests/canvas-soankhbd-smoke.js
   ```

---

## 4. Kế Hoạch Nghiệm Thu (Verification)

1. Chạy pass toàn bộ test tự động:
   `node tests/canvas-soankhbd-smoke.js`
2. Mở file `canvas_soankhbd.html`, copy toàn bộ mã nguồn dán vào cửa sổ **Gemini Canvas trên `gemini.google.com`**.
3. Bấm **TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)**.
4. **Kỳ vọng:**
   - Kết nối thành công, không còn lỗi 401.
   - Giáo án tạo ra giữ nguyên 100% chuẩn mực sư phạm, đúng cấu trúc 5512, phân vai GV-HS và NLS/AI chặt chẽ như mong muốn.
