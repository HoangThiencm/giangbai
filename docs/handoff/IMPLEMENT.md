# IMPLEMENT

Trạng thái: ĐÃ LÀM — PPCT Mistral OCR + khóa khung Năng lực AI 2–3 mục

## File đã đổi

- `js/khbd-app.js`
- `js/khbd-standards.js`
- `tests/khbd-mistral-ocr-smoke.js`
- `tests/khbd-structured-candidates-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **PPCT**: `handleGeneratePpctAnalysis` gọi `extractPpctOcrText`, tiến trình “Đang nhận diện PPCT bằng Mistral OCR...”, parse cục bộ `parsePpctLessonDetails` để điền ô phân tích / thời lượng / phạm vi tiết. Gemini chỉ khi hết key hoặc OCR lỗi.
2. **AI chưa tick**: `isAiStandardRecord` dọn mọi bản ghi AI (`standardKind`, framework QĐ 2422). `autoDetectAndFillLessonMetadata` và đọc PPCT **không** tự `integrations.ai = true`.
3. **AI đã tick**: `recommendOfficialStandards` / `catalogFallbackRecords` / `applySuggestedStandardRecords` khóa **2–3 mục**, `capAiStandardRecords` cắt tối đa 3.

## Test đã chạy

```
node tests/khbd-mistral-ocr-smoke.js
node tests/khbd-structured-candidates-smoke.js
```

Kết quả: **pass**.
