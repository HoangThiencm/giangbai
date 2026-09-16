# VERIFY

## Kết luận
FAIL

## Đối chiếu scope
- Scope 1: Xóa bỏ hoàn toàn thời gian ở Hồ sơ dạy học (Mục IV / Phụ lục E): ĐÃ ĐẠT (tiêu đề Phụ lục E không còn dính `(4 phút)`, bảo toàn thời lượng 45/90 phút).
- Scope 2: Chuẩn hóa cấu trúc tiến trình cho tiết "Luyện tập chung", "Ôn tập": ĐÃ TRIỂN KHAI (đã tích hợp `isPracticeOrReviewLesson` vào `calculateActivityTimeBudgets` với $B=0$, $C=70$ phút cho 90p, và bổ sung định hướng trò chơi khởi động A).
- Scope 3: Khắc phục lỗi rỉ thẻ `<br>- GV:` vào `Nhận xét của GV:`: ĐÃ SỬA NHƯNG GÂY BUG HỒI QUY (phá vỡ test tách lượt lời `sticky` trong `tests/khbd-pedagogy-rate-smoke.js`).
- Scope 4: Kiểm tra tính toàn vẹn hệ thống Canvas: FAIL (test `tests/canvas-soankhbd-smoke.js` thất bại do model hệ thống chưa được đồng bộ).

## Test đã chạy
1. `tests/khbd-activity-e-smoke.js`: PASS.
2. `tests/khbd-time-budgets-smoke.js`: PASS.
3. `tests/sodiem-smoke.js`: PASS.
4. `tests/khbd-table-columns-smoke.js`: PASS.
5. `tests/khbd-pedagogy-rate-smoke.js`: **FAIL** (`AssertionError: Phải chèn <br>- **GV:**` tại dòng 75 do regex phân vai mới làm mất khả năng ngắt dòng của các chuỗi `sticky`).
6. `tests/canvas-soankhbd-smoke.js`: **FAIL** (`AssertionError: canvas_soankhbd.html phải sử dụng model hệ thống gemini-2.5-flash` tại dòng 41).

## Pass / Fail từng tiêu chí
1. Tiêu chí 1: Mục Phụ lục / Hồ sơ dạy học không còn gắn thời gian `(X phút)` -> PASS.
2. Tiêu chí 2: Toàn bộ thời lượng bài dạy được bảo toàn cho các hoạt động dạy học -> PASS.
3. Tiêu chí 3: Cấu hình tiết "Luyện tập chung" / "Ôn tập" ($B=0$, $C=75-80\%$) -> PASS.
4. Tiêu chí 4: Triệt tiêu lỗi rỉ `<br>- GV:` mà KHÔNG phá vỡ kịch bản phân vai hiện hữu -> **FAIL** (gây hồi quy test `khbd-pedagogy-rate-smoke.js`).
5. Tiêu chí 5: Toàn bộ bài kiểm thử tự động đạt PASS 100% -> **FAIL** (2 smoke tests bị FAIL).

## Bug
- Lỗi 1: Regex phân vai mới trong `formatKhbdRoleLine` phá vỡ trường hợp lượt lời đứng sau dấu ngoặc hoặc tiền tố khác dòng (`sticky`).
  - Tái hiện: Chạy `node tests/khbd-pedagogy-rate-smoke.js` bị FAIL tại dòng 75: `+ Bước 1: Chuyển giao nhiệm vụ: (Kỹ thuật TPS) GV: "Mở SGK..."` không được chèn `<br>- **GV:**`.
  - Nguyên nhân: Dùng `(^|<br>\s*|-\s*)` quá chặt nên không khớp được `GV:` khi đứng sau dấu ngoặc `) ` hoặc hai chấm `: `.
  - Giải pháp: Dùng negative lookbehind để chỉ loại trừ cụm từ sở hữu:
    `replace(/(?<!(?:nhận\s*xét|đánh\s*giá|ý\s*kiến|chữ\s*ký)?\s*của\s+)(?:\*\*)?(GV|HS)\s*:(?:\*\*)?/gi, ...)` trong `js/khbd-app.js`, `canvas_soankhbd.html` và file backup.
  - File liên quan: `js/khbd-app.js`, `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`.
- Lỗi 2: `canvas_soankhbd.html` chưa đồng bộ model `gemini-2.5-flash` làm rớt test smoke.
  - Tái hiện: Chạy `node tests/canvas-soankhbd-smoke.js` bị FAIL tại dòng 41 vì dòng 33 `canvas_soankhbd.html` vẫn là `gemini-3-flash-preview`.
  - Giải pháp: Đổi `model: "gemini-2.5-flash"` trong `window.__KHBD_CANVAS__` tại `canvas_soankhbd.html` để khớp với tiêu chuẩn ổn định.
  - File liên quan: `canvas_soankhbd.html`.
