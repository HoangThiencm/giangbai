# IMPLEMENT: Khắc phục [GLOBAL] Script error do tải trùng thư viện & race fallback

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### 1. Chốt idempotent trong thư viện JS
- `js/khbd-prompts.js`: guard `window.__KHBD_PROMPTS_LOADED__` — lần nạp 2 bỏ qua, không redeclare `const`.
- `js/khbd-docx.js`: guard `window.docxGenerator || window.DocxGenerator || window.__KHBD_DOCX_LOADED__`; gán `window.DocxGenerator` / `window.docxGenerator`.
- `js/khbd-pedagogy-catalog.js`: guard `window.KHBD_PEDAGOGY_CATALOG` — lần nạp 2 bỏ qua.

### 2. Loader HTML không còn race `document.write` kép
- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`
- Gộp primary + fallback thành một luồng: `document.write` primary kèm `onload` / `onerror` gọi `ensureKhbd*Fallback` **sau khi** primary kết thúc.
- CDN fallback dùng `crossorigin="anonymous"` để lộ chi tiết lỗi thay vì `[GLOBAL] Script error.`
- Xóa IIFE fallback chạy tức thì ngay sau primary (nguyên nhân tải kép host+CDN).

### 3. `tests/canvas-soankhbd-smoke.js`
- Assert onload/onerror, `crossorigin="anonymous"`, không còn IIFE race.
- Assert chốt idempotent trong 3 file JS + smoke vm nạp prompts 2 lần an toàn.

## Test đã chạy (100% PASS)

- `node tests/canvas-soankhbd-smoke.js`
- `node tests/canvas-prompts-integrity-smoke.js`
- `node tests/khbd-table-columns-smoke.js`
- `node tests/khbd-nls-ai-bold-italic-smoke.js`
- `node tests/khbd-pedagogy-rate-smoke.js`

## File đã đụng

1. `js/khbd-prompts.js`
2. `js/khbd-docx.js`
3. `js/khbd-pedagogy-catalog.js`
4. `canvas_soankhbd.html`
5. `backupcode viettailieu/canvas_soankhbd.html`
6. `tests/canvas-soankhbd-smoke.js`
7. `docs/handoff/IMPLEMENT.md`

UI E2E / Console không còn `[GLOBAL] Script error.` → Antigravity `/verify`.
