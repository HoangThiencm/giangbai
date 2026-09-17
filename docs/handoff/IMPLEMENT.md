# IMPLEMENT: Đồng bộ 2 phiên bản soạn + nút 1-Click sang `soankhbd.html`

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Module 1 — `soankhbd.html`
- Thêm `#btn1ClickGenerate` vào `.header-actions` (trước `#btnCancelGeneration`).
- Thêm `#selectGenerationMode` vào `.toolbar-grid` (giữa Môn học và Danh mục bài học).
- Mặc định `detailed`; có tùy chọn `compact`.

## Module 2 — `js/khbd-app.js`
- `appState.generationMode` khởi tạo từ `localStorage.khbd_generation_mode` (mặc định `detailed`).
- Helpers: `getGenerationMode`, `setGenerationMode`, `resolveGenerationMode`.
- Đồng bộ `#selectGenerationMode` lúc `setupEventListeners`; `change` → lưu localStorage + `appState`.
- `getGenerationPromptContext` truyền `generationMode` qua `resolveGenerationMode` (ưu tiên params → appState → canvasStorage/localStorage).
- `handle1ClickGenerate`:
  - Chặn khi thiếu bài học / đang chạy / thiếu API key (trang chuẩn).
  - Xác nhận theo chế độ compact (6 bước) hoặc detailed (8 bước).
  - Disable `#btn1ClickGenerate`, enable `#btnCancelGeneration`, AbortController + progress bar.
  - Tuần tự: I → II → A → B → C → D → (detailed: E + hình minh họa) → Tab `tabFullPreview`.
- Export `handle1ClickGenerate`, `getGenerationMode`, `setGenerationMode`, `resolveGenerationMode`.

## Module 3 — Smoke mới
- `tests/soankhbd-generation-mode-smoke.js`: HTML IDs, mặc định detailed, wiring app, prompt compact.

## Test đã chạy
- `node tests/soankhbd-generation-mode-smoke.js` — PASS
- `node tests/canvas-soankhbd-smoke.js` — PASS
- `node tests/baogiang-teacher-month-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity.
