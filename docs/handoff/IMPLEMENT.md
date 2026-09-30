# IMPLEMENT: Đồng bộ API Key và OCR ảnh trên Quản lý văn bản

## Đã làm
- `vanban-app.js`: `syncUserKeysFromServer()` gọi `api/user_gemini_keys.php` (`credentials: 'include'`, `cache: 'no-store'`) và ghi `global_gemini_keys` / `global_mistral_keys`. `init()` gọi hàm này và `AiDesignConfig.loadHostingFallbackConfig().catch(() => {})` khi hàm tồn tại.
- Thanh `renderNav` có nút `#vanbanAiConfigBtn` “Cấu hình AI”; click gọi `AiDesignConfig.openModal()`.
- OCR ảnh: `hasGeminiVision()`, `extractTextViaGeminiVision()` (model `AiDesignConfig.getModule()` hoặc `gemini-2.5-flash`, `inline_data`). `ocrImageData` ưu tiên `MistralOcr.ocrImageDataUrl`, không có Mistral thì Gemini Vision (`mode: 'gemini-vision'`). Không có key thì toast “Ảnh chụp cần API Key (Mistral hoặc Gemini)...” và mở modal. `ingestClipboardImage` gọi `ocrImageData`; không còn thông báo “Ảnh vùng chữ ký cần Mistral OCR”.
- Ba trang `quanlyvanban-chuyenmon.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-dang.html` đã nạp `ai-design-config.js` và `mistral-ocr-client.js` trong `<head>`. Không đổi layout.
- `tests/vanban-ocr-clipboard-smoke.js` kiểm tra các token trên.

## Kiểm thử (Coder)
- `node tests/vanban-ocr-clipboard-smoke.js` — PASS
- `node tests/vanban-chuyenmon-signature-smoke.js` — PASS
- `node tests/vanban-display-saved-smoke.js` — PASS
- `python tests/vanban-chuyenmon-root-smoke.py` — PASS

## Ngoài phạm vi
Không sửa API PHP, không commit/push. `docs/handoff/.lock` giữ nội dung `LOCK`.
