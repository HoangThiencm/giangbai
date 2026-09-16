# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Sửa `activityHeadingRegex` trong `js/khbd-app.js` dùng negative lookahead `(?!\\.\\d+)` sau số thứ tự hoạt động 1, 2, 3, 4: ĐÚNG SCOPE (không nhận nhầm tiêu đề nhánh 1.1, 2.1, 2.2 thành tiêu đề hoạt động chính).
- Gia cố `keepBestActivityBlock` trong `js/khbd-app.js`: ĐÚNG SCOPE (không loại bỏ các nhánh con `Hoạt động \d+\.\d+`, không làm mất nhánh 2.2).
- Đồng bộ version cache-busting `20260916-textbook-exact-v17` trên `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`, `js/khbd-app.js`, `js/khbd-prompts.js` và cập nhật test `tests/canvas-prompts-integrity-smoke.js`: ĐÚNG SCOPE.
- Thêm bài test hồi quy `tests/canvas-activity-b-multi-branches-smoke.js`: ĐÚNG SCOPE.
- Không thay đổi prompt SGK/sư phạm, không thay đổi giao diện Canvas: ĐÚNG SCOPE.

## Test đã chạy
1. `node -c js/khbd-app.js js/khbd-prompts.js`: PASS.
2. `node tests/canvas-activity-b-multi-branches-smoke.js`: PASS (bảo tồn đầy đủ cả nhánh 2.1 và 2.2, cắt đúng ranh giới Hoạt động 3).
3. `node tests/canvas-prompts-integrity-smoke.js`: PASS (kiểm tra đầy đủ guard tài nguyên, export window/globalThis, stub HTML và cache-busting v17).
4. `node tests/canvas-soankhbd-smoke.js`: PASS 100% (cả bản chính và bản backup).
5. `node tests/canvas-gemini-api-smoke.js`: PASS.
6. `node tests/canvas-textbook-analysis-smoke.js`: PASS.
7. Kiểm nghiệm trực tiếp trên dữ liệu phản hồi thực tế `scratch/gemini_response_b.txt` (5.161 ký tự) qua `clipKhbdActivityMarkdown("B", raw, { subsectionCount: 2 })`: PASS (giữ nguyên vẹn 5.135 ký tự, có cả `Hoạt động 2.1` và `Hoạt động 2.2`).

## Pass / Fail từng tiêu chí
1. Tiêu chí 1: Test `node tests/canvas-activity-b-multi-branches-smoke.js` đạt PASS 100% -> PASS.
2. Tiêu chí 2: Tất cả các test canvas hiện có đạt PASS 100% -> PASS.
3. Tiêu chí 3: Sau khi 1-Click Generate trên Canvas, Hoạt động B bảo tồn trọn vẹn cả 2.1 và 2.2, không bị cắt cụt -> PASS.

## Bug
Không có bug.


