# IMPLEMENT: Liên thông 1-Click + cuốn chiếu + CDN PPDH + chống trang trắng

Đã triển khai đúng `docs/handoff/PLAN.md` (kèm mục **Khắc phục triệt để lỗi Mở ra trang trắng**).

## Thay đổi vòng này (White Screen Fix — theo VERIFY FAIL)

### `thitructuyen.html`
1. **`cleanOptionText` / `cleanQuestionPrefix`**: Ép `String(text ?? "")` trước `replace` — không còn `TypeError` khi options/câu hỏi là số (`1`, `0`, `10`).
2. **`MathText`**: Ép chuỗi trong `formatTextMode`, `processedText` (`String(text ?? '')`) và `String(processedText).split(...)`.
3. **`ErrorBoundary`**: Class component bọc `<App />`; lỗi render hiện UI “Đã xảy ra lỗi hiển thị” + nút Tải lại / Về Tạo bài tập thay vì trắng `#root`.
4. **`App` khởi tạo đồng bộ**:
   - `editingData` lazy-init từ `thitructuyen_pending_import` (xóa key ngay khi nạp).
   - `view` lazy-init `"create"` khi có `editingData` hoặc `from=taobaitap`.
   - `userEmail` fallback `giaovien@giangbai.local` khi `from=taobaitap` hoặc có `editingData`.
5. **`HybridExamCreator`**: `pages` / `pageQuestions` / `activePageId` lazy-init `"imported"` khi `initialData.questions` có sẵn — Step 2 hiện câu ngay tick đầu.
6. **Cache-buster**: `access-control.js?v=20260919-taobaitap-bridge`.

## Đã có từ vòng trước (vẫn đúng PLAN)
- Nút **🚀 THI TRỰC TUYẾN**, `mapToThiTrucTuyenPayload`, pending import trên `taobaitap.html` + backup.
- Preset 15/20/30/45p, checkbox cuốn chiếu + watermark; lưu cờ qua `matrixConfig`; Sửa đề cũ khôi phục cờ.
- Student one-by-one: 1 câu/lần, countdown từng câu, no-backtrack, watermark, tiến trình localStorage.
- `access-control.js`: miễn token khi `from=taobaitap`.
- CDN jsDelivr fallback catalog PPDH trong `canvas_soankhbd.html`.

## Test đã chạy

- `node tests/taobaitap-thitructuyen-bridge-smoke.js` — PASS (đã bổ sung assert String coerce, ErrorBoundary, cache-buster, sync init; runtime `cleanOptionText(1)` / `cleanQuestionPrefix(1)` không throw)
- `node tests/canvas-soankhbd-smoke.js` — PASS
- `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` — PASS
- `node tests/taobaitap-plan-smoke.js` — PASS

Không sửa `api/exam.php` / prompt AI. Không có browser MCP trong phiên này — UI E2E để Antigravity `/verify`.

## File đã đụng
1. `thitructuyen.html`
2. `tests/taobaitap-thitructuyen-bridge-smoke.js`
3. `docs/handoff/IMPLEMENT.md`
