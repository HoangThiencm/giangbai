# IMPLEMENT

Trạng thái: ĐÃ LÀM — vá VERIFY FAIL soankhbd: NLS/AI tự tick + Mistral OCR bắt buộc

## File đã đổi

- `js/khbd-app.js`
- `mistral-ocr-client.js` (export `getKeys` để `getUserMistralKeys` đọc được)
- `tests/khbd-structured-candidates-smoke.js`
- `tests/khbd-mistral-ocr-smoke.js`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **NLS**: `normalizeTeachingContext` và `ensureIntegrationStandards` nạp 2–3 mục `catalogFallbackRecords("digital", grade)` khi tích hợp số bật. Checkbox con không còn `disabled` vì thiếu OCR.
2. **AI**: khi tick `toggleAiCompetency`, gọi `catalogFallbackRecords("ai", grade)` (1–3 mã). Bỏ tick thì xóa mã AI như cũ.
3. **Mistral OCR**: `getUserMistralKeys` đọc thêm `global_mistral_keys`, `AiDesignConfig.getMistralKeys()`, `MistralOcr.getKeys()`. `readTextbookWithMistral` luôn hiện “Đang nhận diện SGK bằng Mistral OCR...”, chỉ fallback Gemini khi hết key/lỗi. `handleAnalyzeSourceMaterials` gọi `readTextbookWithMistral` thay vì `handleGenerateVision`.

## Test đã chạy

```
node tests/khbd-structured-candidates-smoke.js
node tests/khbd-mistral-ocr-smoke.js
```

Kết quả: **pass** (`khbd-structured-candidates-smoke.js`, `khbd-mistral-ocr-smoke.js`).
