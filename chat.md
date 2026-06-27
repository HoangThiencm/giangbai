## 1. Tích hợp LiteParse V2.1 vào `chuyenpdf.html`

### Câu hỏi

Có thể tích hợp dự án LiteParse V2.1 vào trang `chuyenpdf.html` không?

### Kết luận ngắn

**Có, tích hợp được** — nhưng LiteParse và `chuyenpdf.html` giải **hai bài toán khác nhau**. Hợp lý nhất là **bổ sung provider mới** (hybrid), không thay hẳn Mistral/Gemini.

### `chuyenpdf.html` hiện tại (HT Math Canvas)

- Chạy **trong trình duyệt**: `pdf.js` render PDF → ảnh từng trang
- OCR qua **API đám mây**: Mistral OCR (mặc định) hoặc Gemini Vision
- Ba chế độ: Toán + LaTeX, văn bản thường, văn bản hành chính
- Hậu xử lý nặng cho đề thi VN (tách A/B/C/D, layout Word…)
- Badge: *Client-side Canvas*

### LiteParse V2 (LlamaIndex)

Nguồn: [github.com/run-llama/liteparse](https://github.com/run-llama/liteparse)

- Parser **local**, core Rust (PDFium), không phụ thuộc LLM
- Xuất Markdown / JSON / Text + bounding box
- Có bản **WASM** (`@llamaindex/liteparse-wasm`) chạy trong browser
- OCR native (Tesseract) **không có sẵn trên WASM** — phải tự gắn `ocrEngine` (Tesseract.js hoặc API OCR)

```text
chuyenpdf.html hiện tại:
  PDF/ảnh → pdf.js render → Mistral/Gemini OCR → hậu xử lý → Word

LiteParse V2.1:
  PDF bytes → LiteParse WASM → Markdown/JSON local
              └─ (tuỳ chọn) Tesseract.js hoặc API OCR
```

### Hướng tích hợp khả thi

| Hướng | Khả thi với giangbai | Ghi chú |
|--------|----------------------|---------|
| **WASM trong `chuyenpdf.html`** | Cao | Khớp kiến trúc client-side hiện tại |
| **PHP trên shared hosting** | Thấp | Cần Rust/Python binary |
| **Docker / VPS riêng** | Trung bình | API `POST /parse` tách khỏi HTML |
| **HuggingFace Space** | Trung bình | Giống backend thi trực tuyến |

### Mô hình hybrid đề xuất

Thêm mục thứ 3 trong dropdown **Bộ nhận diện OCR**:

1. **LiteParse (local)** — PDF có lớp text (đề Word xuất PDF, tài liệu số)
2. **Mistral / Gemini** — ảnh scan, đề toán, văn bản hành chính khó

Luồng gợi ý:

```text
Upload PDF
  → LiteParse.isComplex()        // rẻ, không OCR
  → needsOcr = false  → parse local → Markdown → pipeline Word hiện có
  → needsOcr = true   → fallback Mistral/Gemini (hoặc Tesseract.js)
```

Ưu điểm:

- PDF số: nhanh, không tốn API key, không upload file lên cloud
- Giữ Mistral/Gemini cho scan và toán học
- Tái dùng `renderPreview()`, `buildDocumentBodyHtml()`, hậu xử lý đề thi đã có

### Điểm cần lưu ý

**1. Không thay được chế độ Toán + LaTeX**

LiteParse xuất Markdown theo layout, không hiểu công thức như prompt Gemini (`$...$`). Đề toán scan vẫn cần Mistral/Gemini.

**2. OCR tiếng Việt trên browser**

WASM không bundle Tesseract sẵn. Muốn scan local phải gắn Tesseract.js + gói `vie`, hoặc `ocrEngine` gọi Mistral/Gemini.

**3. Dung lượng tải trang**

WASM LiteParse + (tuỳ chọn) Tesseract.js + `vie.traineddata` có thể vài chục MB — nặng hơn `chuyenpdf.html` hiện tại.

**4. Dự án chưa có bundler**

`chuyenpdf.html` là vanilla JS một file. LiteParse WASM cần copy `pkg/` vào repo, hoặc thêm bước build, hoặc import map ESM.

**5. Ảnh đơn lẻ (PNG/JPG)**

LiteParse mạnh với **PDF**. Ảnh rời nên giữ luồng Mistral/Gemini hiện tại.

**6. API key**

File đang có `MISTRAL_API_KEY` hardcode — LiteParse local giảm lần gọi API cho PDF số, nhưng key vẫn lộ nếu không chuyển sang backend.

### Bảng tóm tắt

| Câu hỏi | Trả lời |
|---------|---------|
| Tích hợp LiteParse V2.1 vào `chuyenpdf.html`? | **Có** |
| Thay hẳn Mistral/Gemini? | **Không nên** |
| Cách hợp lý nhất? | Provider thứ 3: LiteParse WASM + auto-detect PDF số/scan |
| Use case phù hợp? | Đề Word→PDF, tài liệu có text layer — nhanh, miễn phí |

### Câu hỏi mở (chưa quyết định)

Mục tiêu ưu tiên là gì?

1. **Tiết kiệm API** khi xử lý PDF số?
2. **Chạy offline** hoàn toàn trong trường?
3. **Thay Mistral** làm engine mặc định?

Mục tiêu khác nhau → thiết kế khác (hybrid nhẹ vs full local OCR với Tesseract.js).

---

## 3. Việc chưa làm (từ các trao đổi trên)

| Chủ đề | Trạng thái |
|--------|------------|
| DNS ad block cho Wi‑Fi trường | Chỉ trao đổi, chưa triển khai |
| LiteParse WASM trong `chuyenpdf.html` | Chỉ trao đổi, chưa triển khai |
| Whitelist domain cho giangbai (nếu dùng Pi-hole) | Chưa liệt kê chính thức |
| Chuyển `MISTRAL_API_KEY` ra backend | Chưa làm |

---

*Tài liệu này chỉ ghi lại trao đổi. Khi triển khai, cập nhật `thongtin.md` hoặc tài liệu kỹ thuật tương ứng.*