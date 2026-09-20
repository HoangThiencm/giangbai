# IMPLEMENT: Bỏ dấu ngoặc vuông [ ] ở tên năng lực / phẩm chất (canvas_soankhbd)

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Root cause đã xử lý
- Prompt `GENERATE_OBJECTIVES` / `getPromptTemplate` / `GENERATE_CORE_LESSON` dùng mẫu `- [Tên năng lực]: [mô tả...]` → Gemini xuất nguyên văn ngoặc vuông quanh tên năng lực chung, đặc thù và phẩm chất.
- `applyObjectivesOutput` chưa có bước hậu xử lý loại `[ ]` ở các mục đó (trong khi mã NLS/AI dạng `***[5.3.TC2a]:***` vẫn phải giữ).

## Thay đổi

### 1. `js/khbd-prompts.js`
- `GENERATE_OBJECTIVES`: mẫu dòng năng lực/phẩm chất bỏ `[ ]`; thêm chỉ thị `TUYỆT ĐỐI CẤM dùng dấu ngoặc vuông [ ]`.
- `getPromptTemplate` (runtime injection cho `GENERATE_OBJECTIVES` / `GENERATE_CORE_LESSON`): cùng quy tắc cấm `[ ]` cho NL chung, NL đặc thù, phẩm chất.
- `GENERATE_CORE_LESSON`: bổ sung chỉ thị cấm ngoặc vuông ở mục 2.a / 2.b / 3.
- **Không đụng** định dạng mã NLS/AI `***[Mã]:***`.

### 2. `js/khbd-app.js`
- Thêm `stripSquareBracketsFromCompetencies(markdown)`: chỉ strip trong section a) NL chung, b) NL đặc thù, phẩm chất; bỏ qua c) NLS / d) AI.
- Gọi sau `ensureObjectivesDigitalCodes` trong `applyObjectivesOutput`.
- Export `window.stripSquareBracketsFromCompetencies` và `module.exports`.

### 3. `tests/khbd-competency-brackets-smoke.js` (mới)
- Assert prompt không còn mẫu `- [Tên năng lực...`.
- Assert chỉ thị cấm ngoặc vuông có trong template + runtime prompt.
- Assert sanitizer bỏ `[ ]` ở NL/phẩm chất và giữ `***[5.3.TC2a]:***` / `***[9.B2.1]:***`.
- Assert pipeline `applyObjectivesOutput` có gọi sanitizer.

## Test đã chạy (100% PASS)

- `node tests/khbd-competency-brackets-smoke.js`
- `node tests/canvas-soankhbd-smoke.js`
- `node tests/canvas-prompts-integrity-smoke.js`
- `node tests/khbd-competencies-smoke.js`
- `node tests/khbd-nls-ai-bold-italic-smoke.js`
- `node tests/ppct-settings-import-smoke.js`

## File đã đụng

1. `js/khbd-prompts.js`
2. `js/khbd-app.js`
3. `tests/khbd-competency-brackets-smoke.js`
