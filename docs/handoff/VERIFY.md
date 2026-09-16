# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Scope 1: Chuẩn hóa tiết Luyện tập / Ôn tập: ĐẠT (Đủ 4 hoạt động A, B, C, D; Hoạt động B = 22 phút cho bài 90p, chia nhánh 2.1/2.2 hệ thống hóa kiến thức & phân tích ví dụ mẫu SGK; C = 51 phút; D = 9 phút; E = 0 phút; tổng 90 phút bảo toàn 100%).
- Scope 2: Cấu hình Model hệ thống Canvas: ĐẠT (Giữ nguyên và đồng bộ `gemini-3-flash-preview` cho cả `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`; test `canvas-soankhbd-smoke.js` PASS 100%).
- Scope 3: Phân vai GV/HS và xử lý thẻ xuất Word: ĐẠT (`khbd-pedagogy-rate-smoke.js` và `khbd-docx-format-smoke.js` PASS 100%).
- Scope 4: Mục Phụ lục E không dính nhãn thời gian: ĐẠT (`khbd-activity-e-smoke.js` PASS).
- Scope 5: Tự động lưu sổ điểm `sodiem.html`: ĐẠT (`sodiem-smoke.js` PASS).

## Test đã chạy
1. `tests/khbd-time-budgets-smoke.js`: PASS.
2. `tests/canvas-soankhbd-smoke.js`: PASS.
3. `tests/khbd-pedagogy-rate-smoke.js`: PASS.
4. `tests/khbd-activity-e-smoke.js`: PASS.
5. `tests/sodiem-smoke.js`: PASS.
6. `tests/khbd-docx-format-smoke.js`: PASS.
7. `tests/khbd-table-columns-smoke.js`: PASS.
8. `tests/khbd-activities-ad-standard-smoke.js`: PASS.
9. `tests/khbd-activity-b-subsections-smoke.js`: PASS.

## Pass / Fail từng tiêu chí
1. Tiêu chí 1: Tiết Luyện tập / Ôn tập có đủ 4 hoạt động A–D, Hoạt động B không bị gán bằng 0 -> PASS.
2. Tiêu chí 2: Hoạt động 2 định hướng hệ thống hóa kiến thức và phân tích ví dụ mẫu SGK -> PASS.
3. Tiêu chí 3: Model Canvas duy trì `gemini-3-flash-preview` đúng yêu cầu người dùng -> PASS.
4. Tiêu chí 4: Triệt tiêu lỗi rỉ `<br>- GV:` mà không phá vỡ kịch bản phân vai hiện hữu -> PASS.
5. Tiêu chí 5: Toàn bộ bài kiểm thử tự động đạt PASS 100% -> PASS.

## Bug
(Không có lỗi tồn đọng)
