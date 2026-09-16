# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Host & CI Integrity**:
   - Đã thêm `js/khbd-prompts.js` và `js/khbd-app.js` vào mảng `required` trong `tools/check-required-assets.js`. CI tự động chặn deploy nếu các file này rỗng (0 bytes).
   - Đã nâng version cache-busting lên `20260916-textbook-exact-v16` trong `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html` và `js/khbd-prompts.js`.
2. **Khai báo toàn cục**:
   - `js/khbd-prompts.js` đã xuất đầy đủ `window.PROMPTS = PROMPTS;` và `globalThis.PROMPTS = PROMPTS;`.
3. **Phòng thủ đa tầng**:
   - `js/khbd-app.js` đã thêm hàm `getSafePrompts()` và bọc `buildPedagogicalPrompt` với fallback an toàn `__KHBD_DEFAULT_OUTPUT_CONTRACT`, triệt tiêu hoàn toàn nguy cơ quăng `ReferenceError: PROMPTS is not defined`.
4. **Dự phòng nhúng (Canvas Stub)**:
   - Cả hai file `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html` đều đã nhúng stub fallback cho `window.PROMPTS` trước khi nạp `khbd-app.js`.

## Test đã chạy
1. `node tools/check-required-assets.js`: PASS (quét thành công 6 assets bắt buộc gồm curriculum, standards, yccd, prompts, app, config).
2. `node tests/canvas-prompts-integrity-smoke.js`: PASS (kiểm tra đầy đủ 4 trường hợp: guard tài nguyên, export window/globalThis, fallback khi thiếu prompt, stub HTML).
3. `node -c js/khbd-prompts.js js/khbd-app.js`: PASS (cú pháp JS hợp lệ 100%).
4. `node tests/canvas-soankhbd-smoke.js`: PASS 100% (cả bản chính và bản backup).
5. `node tests/canvas-gemini-api-smoke.js`: PASS.
6. `node tests/canvas-textbook-analysis-smoke.js`: PASS.
7. `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
8. `node tools/build-obfuscate.js --dry-run`: PASS (44 files, các bundle và mã hóa HTML hoạt động bình thường).

## Pass / Fail từng tiêu chí
- [PASS] Tiêu chí 1: `node tests/canvas-prompts-integrity-smoke.js` đạt PASS 100%.
- [PASS] Tiêu chí 2: Toàn bộ test canvas hiện có đạt PASS 100%.
- [PASS] Tiêu chí 3: Phòng thủ đa tầng không còn phụ thuộc vào việc host có trả về file rỗng hay không.
- [PASS] Tiêu chí 4: Mã nguồn sạch, không lỗi cú pháp, tương thích 1-1 giữa Canvas và bản backup.

## Bug
Không phát hiện bug mới.
