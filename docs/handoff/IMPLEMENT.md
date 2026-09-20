# IMPLEMENT: Cứu hộ khung prompt Mục tiêu & Năng lực chuẩn CV 5512 trên canvas_soankhbd.html

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### 1. CDN fallback `khbd-prompts.js` (cả hai HTML)
- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`
- Thêm `ensureKhbdPromptsFallback()` ngay sau script nạp `khbd-prompts.js`
- Guard: `getPromptTemplate` + `window.PROMPTS.GENERATE_OBJECTIVES`
- Host rỗng/0 bytes → nạp `https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-prompts.js`
- Local/`file:` → nạp lại `js/khbd-prompts.js`

### 2. CDN fallback `khbd-docx.js` (cả hai HTML)
- Thêm `ensureKhbdDocxFallback()` ngay sau script nạp `khbd-docx.js`
- Guard: `createKhbdDocxDocument` hoặc `window.KHBD_DOCX`
- CDN: `.../js/khbd-docx.js`

### 3. Backup đồng bộ pedagogy-catalog fallback
- Bản backup dùng `isLocal` + `ensureKhbdPedagogyCatalogFallback` giống bản chính (smoke yêu cầu cả hai HTML có đủ 3 fallback CDN)

### 4. `js/khbd-app.js` — cấu trúc Năng lực + preview
- `isOffTopicObjectivesHallucination`: nếu thiếu cả `năng lực chung` và `năng lực đặc thù` → đánh dấu lạc chuẩn → `applyObjectivesOutput` tái tạo bằng `GENERATE_OBJECTIVES`
- `isIntegrationBadgeListItem` + `applyLiteralListMarkers`: không chèn `- ` trơ trước mục chỉ là badge NLS/AI
- `applyIntegrationPreviewColors`: `li` NLS/AI → `listStyleType: none` và bỏ gạch đầu dòng text thừa

### 5. Smoke tests
- `tests/canvas-prompts-integrity-smoke.js`: assert `ensureKhbdPromptsFallback`, sections `### a) Năng lực chung`, `### b) Năng lực đặc thù môn học`, `{digital_objectives_section}`, `{ai_objectives_section}`, và guard hallucination/preview
- `tests/canvas-soankhbd-smoke.js`: cả hai HTML phải có CDN fallback cho `khbd-prompts.js`, `khbd-pedagogy-catalog.js`, `khbd-docx.js`

## Test đã chạy (100% PASS)

- `node tests/canvas-prompts-integrity-smoke.js`
- `node tests/canvas-soankhbd-smoke.js`
- `node tests/khbd-competencies-smoke.js`
- `node tests/khbd-nls-ai-bold-italic-smoke.js`

## File đã đụng

1. `canvas_soankhbd.html`
2. `backupcode viettailieu/canvas_soankhbd.html`
3. `js/khbd-app.js`
4. `tests/canvas-prompts-integrity-smoke.js`
5. `tests/canvas-soankhbd-smoke.js`
6. `docs/handoff/IMPLEMENT.md`

Không mở rộng ngoài PLAN. UI E2E / hosting 0-bytes → Antigravity `/verify`.
