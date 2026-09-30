# IMPLEMENT: Đồng bộ API Key và OCR ảnh trên Quản lý văn bản

## Đã làm
- `vanban-app.js`: `syncUserKeysFromServer()` gọi `api/user_gemini_keys.php` (credentials include, cache no-store) và ghi `global_gemini_keys` / `global_mistral_keys`. `init()` gọi hàm này và `AiDesignConfig.loadHostingFallbackConfig()`.
- Thanh `renderNav` có nút `#vanbanAiConfigBtn` “Cấu hình AI”, click gọi `AiDesignConfig.openModal()`.
- OCR ảnh: `ocrImageData` ưu tiên `MistralOcr.ocrImageDataUrl`, không có Mistral thì `extractTextViaGeminiVision` (`getModule()` hoặc `gemini-2.5-flash`). Không có key thì toast và mở modal. `ingestClipboardImage` và nhánh ảnh / trang đầu PDF trong `extractPdf` đi qua `ocrImageData`.
- Smoke mới: `tests/vanban-ocr-clipboard-smoke.js`.

## Kiểm thử (Coder)
- `node --check vanban-app.js`
- `node tests/vanban-ocr-clipboard-smoke.js` — PASS
- `node tests/vanban-chuyenmon-signature-smoke.js` — PASS
- `python tests/vanban-chuyenmon-root-smoke.py` — PASS
- `node tests/vanban-display-saved-smoke.js` — PASS

## Ngoài phạm vi
Không sửa API PHP, không commit/push. Nghiệm thu giao diện thật thuộc `/verify`.
