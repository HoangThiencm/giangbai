# IMPLEMENT: Khắc phục SyntaxError DocxGenerator already been declared

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Root cause đã xử lý
- Host `khbd-docx.js` khai báo `class DocxGenerator` / `const docxGenerator` ở **script lexical scope**, không gắn `window`.
- Guard cũ chỉ xem `window.DocxGenerator` → luôn fail → CDN nạp lần 2 → `SyntaxError: Identifier 'DocxGenerator' has already been declared`.

## Thay đổi

### 1. IIFE wrappers (function scope, không đụng global lexical)
- `js/khbd-docx.js`: `(function (global) { ... nested define ... })(window|globalThis)`
  - Guard: `global.DocxGenerator` / `global.docxGenerator` **hoặc** lexical `DocxGenerator`+`docxGenerator`
  - Luôn gán `global.DocxGenerator` / `global.docxGenerator`
  - `class` nằm trong nested IIFE để tránh TDZ khi check lexical ở outer
- `js/khbd-prompts.js`: IIFE tương tự; early-return nếu `global.getPromptTemplate` + `global.PROMPTS.GENERATE_OBJECTIVES`
- `js/khbd-pedagogy-catalog.js`: IIFE; early-return nếu `global.KHBD_PEDAGOGY_CATALOG`

### 2. Guard HTML (lexical + window)
- `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`
- `ensureKhbdPromptsFallback`: `window.getPromptTemplate` **hoặc** lexical `getPromptTemplate`
- `ensureKhbdDocxFallback`: lexical `docxGenerator`/`DocxGenerator` **hoặc** `window.*`
- `ensureKhbdPedagogyCatalogFallback`: lexical `KHBD_PEDAGOGY_CATALOG` **hoặc** `window.KHBD_PEDAGOGY_CATALOG`

### 3. Smoke
- Assert IIFE `(function (global)`, global assigns, lexical+window guards
- Vm nạp prompts/docx 2 lần → early-return, cùng instance

## Test đã chạy (100% PASS)

- `node tests/canvas-soankhbd-smoke.js`
- `node tests/canvas-prompts-integrity-smoke.js`
- `node tests/khbd-table-columns-smoke.js`
- `node tests/khbd-pedagogy-rate-smoke.js`
- `node tests/khbd-nls-ai-bold-italic-smoke.js`

## File đã đụng

1. `js/khbd-docx.js`
2. `js/khbd-prompts.js`
3. `js/khbd-pedagogy-catalog.js`
4. `canvas_soankhbd.html`
5. `backupcode viettailieu/canvas_soankhbd.html`
6. `tests/canvas-soankhbd-smoke.js`
7. `tests/canvas-prompts-integrity-smoke.js` (đồng bộ assert guard mới)
8. `docs/handoff/IMPLEMENT.md`

Console runtime → Antigravity `/verify`.
