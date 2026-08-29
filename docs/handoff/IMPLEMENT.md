# IMPLEMENT

Trạng thái: ĐÃ LÀM — Tab con 5: CLIL A1–B2 + 6 loại khuyết tật HSKT

## File đã đổi

- `soankhbd.html`
- `js/khbd-app.js`
- `js/khbd-prompts.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **HTML Tab con 5**: 2 card riêng.
   - Card xanh lục: `toggleForeignLanguage` + 4 radio `name="clilLevel"` (A1 mặc định, A2, B1, B2).
   - Card tím: `toggleInclusiveSupport` + 6 checkbox `.disability-type-choice` + `.support-choice` (ID không đổi).
2. **JS**: `teachingContext.clilLevel` (mặc định A1) và `disabilityTypes`. `normalizeTeachingContext` + `syncDraftDom` khôi phục khi mở trang/bản nháp. Change radio/checkbox ghi localStorage.
3. **Prompt**: `PROMPTS.CLIL_INCLUSIVE_GATE` gắn vào soạn mục tiêu/hoạt động. `buildPedagogicalContext` truyền cấp độ CLIL, loại HSKT và giải pháp hỗ trợ; marker `[CLIL]` (xanh lục) / `[HOANHAP]` (tím).

## Ngoài phạm vi (không đụng)

- ID `toggleForeignLanguage`, `toggleInclusiveSupport`, `.support-choice`.

## Test đã chạy

```
node tests/khbd-4steps-workflow-smoke.js
```

Kết quả: **pass** (4 mức CLIL A1–B2, 6 loại HSKT, clilLevel/disabilityTypes lưu state, CLIL_INCLUSIVE_GATE).
