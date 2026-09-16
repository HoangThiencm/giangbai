# IMPLEMENT: Khóa cứng NLS & AI theo PPCT + Bảo toàn 100% mô tả PPCT vào Mục tiêu

Đã triển khai đúng `docs/handoff/PLAN.md`.

## 1. Khóa cứng NLS/AI theo PPCT

- `js/khbd-app.js`: thêm `extractPpctDetailedEntries`, `ppctRowDetailedEntries`, `applyPpctLockedStandards`.
- `applyPpctCatalogRow` chỉ tick đúng mã NLS/AI của dòng PPCT, gắn `fromPpct: true` / `lockedFromPpct: true`, gán mô tả vào `proposedTask` / `taskDescription`.
- Bài không có mã: tắt tích hợp tương ứng, không tự tick.
- `requestStructuredIntegrationCandidates`, `applySuggestedStandardRecords`, `ensureIntegrationStandards`, Bước 3 và Bước 4 AI: nếu bài đã chọn từ PPCT thì không ghi đè / không tự tick thêm mã `[ĐỀ XUẤT THEO BÀI]` (ví dụ `1.1.TC2a`, `5.2.TC2a`).

## 2. Bảo toàn 100% mô tả PPCT vào Phần I. Mục tiêu

- Bóc cặp `{ code, description }` từ evidence / `digital_competency` / `ai_competency` (dạng `Mã : Mô tả`).
- `getPromptTemplate('GENERATE_OBJECTIVES')` nhận `digital_objectives_section` / `ai_objectives_section` nguyên văn:
  - `### c) Năng lực số: ***[5.3.TC2a]:*** Sử dụng máy tính cầm tay (phím CALC)...`
  - `### d) Năng lực AI: ***[9.B2.1]:*** Sử dụng trợ lý AI tạo các ví dụ ngẫu nhiên...`
- Prompt cấm diễn đạt lại / bịa câu chữ khi PPCT đã có mô tả.
- `applyPpctVerbatimObjectives` (gọi từ `applyObjectivesOutput`) chèn đúng nguyên văn mô tả PPCT vào kết quả Phần I.

## 3. Giao diện Canvas & test

- `soankhbd.html`, `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`: ghi rõ mã NLS/AI và mô tả PPCT được khóa đúng nguồn.
- `soankhbd.html`: cache-bust `khbd-prompts.js` / `khbd-app.js` lên `textbook-exact-v18`.
- `tests/ppct-settings-import-smoke.js`, `tests/khbd-4steps-workflow-smoke.js`: khi nạp Bài 1 PPCT chỉ còn `5.3.TC2a` + `9.B2.1`; Phần I giữ nguyên văn mô tả.

Kiểm thử đã chạy:

- `node tests/ppct-settings-import-smoke.js` — PASS
- `node tests/khbd-4steps-workflow-smoke.js` — PASS
- `node tests/soankhbd-ppct-standards-smoke.js` — PASS
- `node tests/ppct-dedupe-smoke.js` — PASS
- `node tests/khbd-nls-ai-bold-italic-smoke.js` — PASS
- `node tests/khbd-structured-candidates-smoke.js` — PASS
- `node tests/khbd-recommendation-flow-smoke.js` — PASS
- `node tests/khbd-ppct-integration-smoke.js` — PASS
- `node tests/canvas-soankhbd-smoke.js` — PASS
- `node tests/canvas-soanbaigiang-smoke.js` — PASS
- `node tests/khbd-textbook-exact-structure-smoke.js` — PASS
- `node tests/khbd-activity-b-subsections-smoke.js` — PASS
- `node tests/docx-export-format-smoke.js` — PASS
- `node tests/khbd-docx-layout-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity để đối chiếu trực quan Bài 1 PPCT (mã `5.3.TC2a`, `9.B2.1`) và Phần I. Mục tiêu.
