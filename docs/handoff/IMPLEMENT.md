# IMPLEMENT: Sửa lặp dòng Năng lực số & ký tự thô `***` trong Word

Đã triển khai đúng `docs/handoff/PLAN.md`.

## 1. Regex tiêu đề NLS/AI (tiếng Việt)

- `js/khbd-app.js`: thêm `OBJECTIVES_NLS_HEADING_RE` / `OBJECTIVES_AI_HEADING_RE`.
- Thay `\b` ASCII bằng `(?::|\s|$)` để khớp `### c) Năng lực số: ...` và `### d) Năng lực AI: ...`.
- `stripObjectivesStandardSection`, `upsertObjectivesStandardSection`, `applyPpctVerbatimObjectives`, `ensureObjectivesDigitalCodes` dùng chung 2 regex này.
- Hệ quả: xóa đúng section cũ rồi chèn đúng 1 dòng, không còn nhân bản `c) Năng lực số`.

## 2. Parse markdown inline cho tiêu đề Word

- `js/khbd-docx.js` `parseMarkdownToDocxElements`: tiêu đề `#` / `##` / `###` / `####` gọi `parseInlineTextToRuns` thay vì `coloredTextRun(headingText)` thô.
- `***[5.3.TC2a]:***` và `***[9.B2.1]:***` được bóc dấu sao, in đậm + in nghiêng, màu `0369A1` (NLS) / `6D28D9` (AI).

## 3. Giao diện & test

- `soankhbd.html`: cache-bust `js/khbd-docx.js` lên `textbook-exact-v18` (cùng bộ với Canvas).
- `canvas_soankhbd.html` và bản sao lưu nạp cùng `js/khbd-app.js` / `js/khbd-docx.js`.
- `tests/docx-export-format-smoke.js`: xuất tiêu đề NLS/AI không còn `***`, mã đúng màu/đậm/nghiêng.
- `tests/khbd-4steps-workflow-smoke.js`: regex tiếng Việt; `applyPpctVerbatimObjectives` chỉ giữ đúng 1 dòng Năng lực số / Năng lực AI.

Kiểm thử đã chạy:

- `node tests/docx-export-format-smoke.js` — PASS
- `node tests/khbd-4steps-workflow-smoke.js` — PASS
- `node tests/khbd-nls-ai-bold-italic-smoke.js` — PASS
- `node tests/khbd-docx-format-smoke.js` — PASS
- `node tests/canvas-soankhbd-smoke.js` — PASS
- `node tests/ppct-settings-import-smoke.js` — PASS
- `node tests/khbd-docx-layout-smoke.js` — PASS
- `node tests/khbd-integrations-smoke.js` — PASS
- `node tests/soankhbd-ppct-standards-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity: xuất Word Bài 1, kiểm tra Phần I không lặp Năng lực số và không còn `***` thô.
