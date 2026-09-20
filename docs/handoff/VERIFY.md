# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `js/khbd-prompts.js`: Đã có chốt idempotent `__KHBD_PROMPTS_LOADED__`, không redeclare top-level const khi nạp lặp.
- `js/khbd-docx.js`: Đã có chốt idempotent `DocxGenerator` và `__KHBD_DOCX_LOADED__`, gán `window.DocxGenerator` và `window.docxGenerator`.
- `js/khbd-pedagogy-catalog.js`: Đã có chốt idempotent `KHBD_PEDAGOGY_CATALOG`, ngăn redeclare const.
- `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`:
  + Xóa bỏ IIFE fallback chạy tức thì gây race condition tải kép host + CDN.
  + Gắn `onload` / `onerror` vào script primary để fallback chỉ kích hoạt sau khi primary kết thúc.
  + Thêm `crossorigin="anonymous"` cho script CDN fallback để không bị trình duyệt che giấu thành `[GLOBAL] Script error.`
- `tests/canvas-soankhbd-smoke.js`: Assert đầy đủ không còn IIFE race, có onload/onerror, có crossorigin="anonymous" và chốt idempotent hoạt động chính xác khi nạp 2 lần trong cùng context.

## Test đã chạy
- `node tests/canvas-soankhbd-smoke.js` (PASS)
- `node tests/canvas-prompts-integrity-smoke.js` (PASS)
- `node tests/khbd-table-columns-smoke.js` (PASS)
- `node tests/khbd-nls-ai-bold-italic-smoke.js` (PASS)
- `node tests/khbd-pedagogy-rate-smoke.js` (PASS)
- `node tests/khbd-competencies-smoke.js` (PASS)
- `node tests/khbd-docx-math-smoke.js` (PASS)
- `node tests/khbd-pedagogy-script-smoke.js` (PASS)
- `node tests/khbd-review-practice-lesson-smoke.js` (PASS)

## Pass / Fail từng tiêu chí
- [PASS] Triệt tiêu race condition gây tải trùng lặp giữa host chính và CDN fallback.
- [PASS] Chốt idempotent bảo vệ toàn diện 3 file JS (`khbd-prompts.js`, `khbd-docx.js`, `khbd-pedagogy-catalog.js`).
- [PASS] Không còn hiện tượng redeclare const/class ném `SyntaxError` và bắn `[GLOBAL] Script error.`
- [PASS] 100% test suite đạt chuẩn.

## Bug
Không có.
