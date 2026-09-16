# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Mục tiêu**: Khóa cứng NLS & AI theo PPCT + Bảo toàn 100% mô tả nhiệm vụ PPCT vào Phần I. Mục tiêu bài dạy.
- **Trạng thái đối chiếu**:
  - `applyPpctCatalogRow`: Khi chọn bài có mã NLS/AI từ PPCT, chỉ tick đúng duy nhất các mã đó (ví dụ Bài 1 chỉ có `5.3.TC2a` và `9.B2.1`), đánh dấu `fromPpct: true` / `lockedFromPpct: true`.
  - Vô hiệu hóa toàn bộ cơ chế tự động tick thêm mã [ĐỀ XUẤT THEO BÀI] (`1.1.TC2a`, `5.2.TC2a`) ở Bước 3 & Bước 4 đối với bài đã có PPCT.
  - Bóc tách cặp `{ code, description }` từ PPCT và bảo toàn nguyên văn 100% mô tả nhiệm vụ vào Phần I. Mục tiêu (`### c) Năng lực số` và `### d) Năng lực AI`).
  - Giao diện `canvas_soankhbd.html`, `soankhbd.html` và bản sao lưu được đồng bộ nhất quán.

## Test đã chạy
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

## Pass / Fail từng tiêu chí
- [PASS] Chọn bài từ PPCT chỉ tick đúng mã quy định (`5.3.TC2a` và `9.B2.1`), không tự ý tick thêm `1.1.TC2a` hay `5.2.TC2a`.
- [PASS] Bảo toàn nguyên văn mô tả nhiệm vụ từ PPCT vào Phần I. Mục tiêu.
- [PASS] Bài PPCT không có mã thì tắt tích hợp tương ứng.
- [PASS] Toàn bộ 14/14 test suites PASS 100%.

## Bug
Không phát hiện lỗi.
