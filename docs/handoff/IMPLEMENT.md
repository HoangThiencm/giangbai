# IMPLEMENT

Trạng thái: ĐÃ LÀM — Quy trình 4 bước KHBD (OCR SGK không tự tick, dán PPCT trực tiếp, đề xuất PPDH/NLS, AI opt-in)

## File đã đổi

- `soankhbd.html`
- `js/khbd-app.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **Bước 1**: `applyTextbookOcrResult` chỉ ghi `content.vision`, `ocrReady = true` và preview. Không gọi `ensurePedagogyFromLesson` / `requestStructuredIntegrationCandidatesForEnabled`. Bỏ auto-tick khi blur editor SGK. `normalizeTeachingContext` không còn seed sẵn mã NLS khi mở trang.
2. **Bước 2**: `activeDropzoneTarget` (`sgk` | `ppct`). Click / focus / hover card PPCT rồi Ctrl+V đưa ảnh vào `handlePpctFiles`. Viền xanh (SGK) / cam (PPCT). Đọc PPCT vẫn Mistral OCR.
3. **Bước 3**: Card + stepper nút `triggerStep3PedagogyAndDigitalRecommendations()` — force PPDH/kỹ thuật 4 pha, bật NLS, Gemini đề xuất NLS (kèm PPCT trong prompt). Không tick AI.
4. **Bước 4**: `toggleAiCompetency` mặc định tắt. Khi bật: fallback 2–3 mục rồi Gemini nếu đã OCR. Khi tắt: xóa mã AI. Nút "Bắt đầu soạn" chuyển Tab Mục tiêu.
5. **Stepper 4 bước** trên đầu Tab 0, badge trạng thái theo SGK/PPCT/đề xuất/AI.

## Ngoài phạm vi giữ nguyên

- `js/khbd-standards.js` không đổi cấu trúc TT 02 / QĐ 2422.
- Xuất Word 5512 không đổi.

## Test đã chạy

```
node tests/khbd-4steps-workflow-smoke.js
```

Kết quả: **pass** (`khbd-4steps-workflow-smoke.js`, kèm `khbd-structured-candidates-smoke.js`, `khbd-mistral-ocr-smoke.js`, `khbd-ppct-integration-smoke.js`).
