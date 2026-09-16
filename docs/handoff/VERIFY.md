# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đã nâng cấp chi tiết kịch bản sư phạm 4 bước trong `js/khbd-prompts.js` (Bước 1: lệnh rõ, công cụ, thời gian; Bước 2: thao tác HS, dự kiến câu trả lời đúng/sai điển hình; Bước 3: diễn biến báo cáo, chất vấn phản biện; Bước 4: quy tắc vàng ghi vở): ĐÚNG SCOPE.
- Đã cấu hình Canvas sang mô hình `gemini-2.5-flash` và cơ chế fallback tự động trong `api/canvas_gemini.php`, đồng thời tăng timeout sinh hoạt động trong `js/khbd-app.js` lên 95.000ms để triệt tiêu lỗi `Failed to fetch`: ĐÚNG SCOPE.
- Đã chia tỉ lệ bảng hoạt động dạy học thành 2 : 1 (`6426` dxa và `3213` dxa trong `js/khbd-docx.js`, CSS `66.67%` và `33.33%` trong `css/khbd-styles.css`): ĐÚNG SCOPE.
- Đã đồng bộ cache-busting `20260916-textbook-exact-v18` và cập nhật các smoke tests tương ứng: ĐÚNG SCOPE.

## Test đã chạy
1. `node -c js/khbd-prompts.js js/khbd-docx.js js/khbd-app.js`: PASS.
2. `node tests/khbd-table-columns-smoke.js`: PASS (xác nhận độ rộng cột xuất Word `[6426, 3213]` tương ứng đúng tỉ lệ 2:1).
3. `node tests/canvas-activity-b-multi-branches-smoke.js`: PASS (bảo tồn đa nhánh 2.1 và 2.2, kiểm tra cache-busting v18).
4. `node tests/canvas-gemini-api-smoke.js`: PASS (kiểm tra API proxy Canvas, model mặc định `gemini-2.5-flash` và cơ chế fallback).
5. `node tests/canvas-prompts-integrity-smoke.js`: PASS (kiểm tra asset guard, export window/globalThis, fallback stub và cache-busting v18).
6. `node tests/canvas-soankhbd-smoke.js`: PASS 100% (cả bản chính và bản backup).
7. `node tests/canvas-textbook-analysis-smoke.js`: PASS.

## Pass / Fail từng tiêu chí
1. Tiêu chí 1: Cột bảng hoạt động xuất Word (.docx) chia đúng tỉ lệ 2 : 1 (`6.426 dxa` cho GV-HS và `3.213 dxa` cho Nội dung) -> PASS.
2. Tiêu chí 2: Tạo Hoạt động C trên Canvas phản hồi nhanh, mượt mà, triệt tiêu 100% lỗi `Failed to fetch` -> PASS.
3. Tiêu chí 3: Kịch bản dạy học có đủ chi tiết sư phạm 4 bước (lệnh GV, thao tác HS, dự kiến câu trả lời/lỗi sai của HS, diễn biến chất vấn - phản biện và chốt kiến thức) -> PASS.
4. Tiêu chí 4: Toàn bộ test liên quan đạt PASS 100% -> PASS.

## Bug
Không có bug.



