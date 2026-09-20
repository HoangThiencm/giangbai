# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Thêm `ensureKhbdPromptsFallback()` tự động nạp từ CDN GitHub jsDelivr (`https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-prompts.js`) khi file hosting rỗng 0 bytes trên `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`.
- [x] Thêm `ensureKhbdDocxFallback()` dự phòng CDN cho `khbd-docx.js` trên cả 2 trang.
- [x] Đồng bộ `ensureKhbdPedagogyCatalogFallback()` cho cả bản backup.
- [x] Nâng cấp `isOffTopicObjectivesHallucination` trong `js/khbd-app.js`: Nhận diện trường hợp output thiếu Năng lực chung / Năng lực đặc thù để tự động tái tạo bằng siêu prompt cứng chuẩn CV 5512.
- [x] Xử lý preview KaTeX trong `js/khbd-app.js`: Loại bỏ gạch đầu dòng trơ trọi (`- `) trước thẻ badge NLS/AI.
- [x] Cập nhật và bổ sung smoke tests kiểm tra trọn vẹn cơ chế CDN fallback và tính toàn vẹn của siêu prompt.

## Test đã chạy
- `node tests/canvas-prompts-integrity-smoke.js` (PASS)
- `node tests/canvas-soankhbd-smoke.js` (PASS)
- `node tests/khbd-competencies-smoke.js` (PASS)
- `node tests/khbd-nls-ai-bold-italic-smoke.js` (PASS)

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: `canvas_soankhbd.html` và bản backup có `ensureKhbdPromptsFallback()` nạp CDN khi host 0 bytes: PASS.
- [x] Tiêu chí 2: Guard kiểm tra `getPromptTemplate` và `PROMPTS.GENERATE_OBJECTIVES`: PASS.
- [x] Tiêu chí 3: `ensureKhbdDocxFallback()` dự phòng cho DOCX: PASS.
- [x] Tiêu chí 4: Lọc và tái tạo output mục tiêu thiếu chuẩn CV 5512 trong `khbd-app.js`: PASS.
- [x] Tiêu chí 5: Hiển thị preview KaTeX cho thẻ NLS/AI không bị dấu gạch ngang mồ côi: PASS.
- [x] Tiêu chí 6: Tự động hóa kiểm thử hồi quy 100% PASS: PASS.

## Bug
(Không có)
