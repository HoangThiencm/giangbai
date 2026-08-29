# IMPLEMENT

Trạng thái: ĐÃ LÀM — Bộ lọc sư phạm chống khiên cưỡng (dạng bài, Time-Budget, Facility Gate)

## File đã đổi

- `js/khbd-standards.js`
- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `tests/khbd-pedagogy-script-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **Dạng bài**: `detectLessonMathBranch` phân loại geometry / algebra / statistics. `isUnnaturalOfficialStandard` đưa điểm 0 cho mã không khớp (Hình học: 3.3, 3.4; Đại số: 4.2; không pad các mã bị cấm). Thống kê ưu tiên 1.1–1.3.
2. **Time-Budget Gate**: `applyTimeBudgetGateToPedagogy` — bài 1 tiết chỉ 1 kỹ thuật nhẹ pha B (`tps-tech` hoặc `tablecloth`), loại Mảnh ghép / Trạm / Dự án.
3. **Facility Gate + prompt**: `PROMPTS.NATURAL_INTEGRATION_GATE` gắn Mục tiêu, Thiết bị, Hoạt động A–D. Không có devices/internet: cấm tra cứu mạng, điện thoại, Canva, laptop/chatbot trong giờ. `buildPedagogicalContext` lặp lại các cổng này.

## Ngoài phạm vi giữ nguyên

- Danh mục mã TT 02 / QĐ 2422 không đổi.
- Xuất Word 5512 không đổi.

## Test đã chạy

```
node tests/khbd-4steps-workflow-smoke.js
node tests/khbd-pedagogy-script-smoke.js
```

Kết quả: **pass** (`khbd-4steps-workflow-smoke.js`, `khbd-pedagogy-script-smoke.js`).
