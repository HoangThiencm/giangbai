# IMPLEMENT: Khắc phục nhảy lựa chọn 2 lần và trùng lặp thông báo khi Đề xuất PPDH, Năng lực số & Khung AI

## Phạm vi đã triển khai

- Giữ nguyên `docs/handoff/PLAN.md` và `docs/handoff/.lock`.
- Không đổi danh mục PPDH, Thông tư 02 (NLS) hay Quyết định 2422.
- Không đổi thuật toán trong `khbd-pedagogy-catalog.js`.
- Chỉ sửa `js/khbd-app.js` và thêm `tests/khbd-recommendation-flow-smoke.js`.

### `js/khbd-app.js`

- `triggerStep3PedagogyAndDigitalRecommendations`:
  - Nút `btnStep3Recommend`, `btnStep3PedagogyDigital`, `btnSuggestPedagogyStandards` chuyển sang `⏳ Đang phân tích SGK & đề xuất...`, disabled, `aria-busy`.
  - Panel PPDH/NLS hiện chỉ báo đang phân tích; không tick checkbox tạm.
  - `ensurePedagogyFromLesson({ force: true, silent: true, skipRender: true })` và `requestStructuredIntegrationCandidates("digital", { silent: true, skipRender: true, force: true })`.
  - Render checkbox **một lần** trong `finally`; luôn khôi phục nút (không treo khi Gemini lỗi).
  - Chỉ 1 toast hoàn tất: *"✅ Đã đề xuất PPDH, kỹ thuật dạy học 4 pha và Năng lực số (NLS) bám sát nội dung SGK."*
- `triggerAiCompetencyRecommendations` (bật toggle AI):
  - Loading trên panel AI, chờ Gemini (hoặc fallback nếu không OCR), rồi tick 1 lần.
  - 1 toast hoàn tất khi có OCR; nếu chưa đọc SGK thì chỉ toast hướng dẫn đọc SGK.
  - Không ghi đè mục AI đã chọn tay (`autoSuggested === false`) trừ khi `force`.
- `skipRender` trên `ensurePedagogyFromLesson`, `ensureIntegrationStandards`, `applySuggestedStandardRecords`, `requestStructuredIntegrationCandidates`.

## Kiểm thử đã chạy

- `node tests/khbd-recommendation-flow-smoke.js` — PASS
- `node tests/khbd-4steps-workflow-smoke.js` — PASS
- `node tests/khbd-structured-candidates-smoke.js` — PASS

## Vấn đề còn lại

- Không có trong phạm vi triển khai này. Cần `/verify` trên `soankhbd.html`: Bước 3 và bật AI không còn chớp checkbox / 2 toast.
