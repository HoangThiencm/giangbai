# VERIFY

## Kết luận
FAIL

## Đối chiếu scope
- Scope 1: Xóa bỏ hoàn toàn thời gian ở Hồ sơ dạy học (Mục IV / Phụ lục E): ĐÃ LÀM MỘT PHẦN (trong `js/khbd-app.js` đã sửa `normalizeActivityTimeHeadings` xóa `(X phút)` và truyền `fourActivities: true`, nhưng chưa làm sạch tiêu đề con lặp lại khi xuất Word trong `js/khbd-docx.js`).
- Scope 2: Chuẩn hóa cấu trúc tiến trình cho tiết "Luyện tập chung", "Ôn tập": CHƯA LÀM (chưa có hàm `isPracticeOrReviewLesson`, chưa có prompt chuyên biệt cho tiết luyện tập chung/ôn tập, chưa cấu hình phân bổ thời lượng 75–80% cho Luyện tập).
- Scope 3: Khắc phục triệt để lỗi rỉ thẻ `<br>- GV:` vào `Nhận xét của GV:` và in thẻ HTML thô ra Word: CHƯA LÀM (`formatKhbdRoleLineBreaks` vẫn biến `*(Nhận xét của GV: ...)*` thành `*(Nhận xét của <br>- **GV:** ...)*`).
- Scope 4: Bắt buộc cập nhật `docs/handoff/IMPLEMENT.md`: CHƯA LÀM (`IMPLEMENT.md` chưa có nội dung cho đợt thay đổi này).

## Test đã chạy
1. Kiểm tra `isPracticeOrReviewLesson` trong `js/khbd-prompts.js` và `js/khbd-app.js`: FAIL (hàm chưa được định nghĩa).
2. Kiểm tra `formatKhbdRoleLineBreaks` với chuỗi `*(Nhận xét của GV: ...)*`: FAIL (kết quả trả về vẫn bị chèn `<br>- **GV:**`).
3. Kiểm tra hàm `clipKhbdActivityMarkdown('E', ...)`: PASS (tiêu đề Phụ lục E đã không còn dính `(4 phút)`).
4. Chạy `tests/khbd-activity-e-smoke.js`: PASS.
5. Chạy `tests/khbd-time-budgets-smoke.js`: PASS.
6. Chạy `tests/khbd-pedagogy-rate-smoke.js`: PASS.

## Pass / Fail từng tiêu chí
1. Tiêu chí 1: Mục Phụ lục / Hồ sơ dạy học khi xuất ra Word (.docx) hoặc Markdown toàn bài 100% không còn gắn thời gian `(X phút)` -> PASS một phần (cần hoàn thiện thêm ở khâu xuất Word trong `js/khbd-docx.js`).
2. Tiêu chí 2: Toàn bộ thời lượng bài dạy (45 phút / 90 phút) được bảo toàn nguyên vẹn cho các hoạt động dạy học trên lớp -> PASS.
3. Tiêu chí 3: Khi soạn tiết "Luyện tập chung" hoặc "Ôn tập" (Khởi động trò chơi -> Bỏ hình thành kiến thức mới -> Trọng tâm Luyện tập 75–80%) -> FAIL (chưa triển khai).
4. Tiêu chí 4: Triệt tiêu hoàn toàn lỗi chèn `<br>- GV:` vào `Nhận xét của GV:`; file Word xuất ra không chứa thẻ `<br>` thô -> FAIL (chưa sửa regex trong `formatKhbdRoleLine`).
5. Tiêu chí 5: Bắt buộc ghi `docs/handoff/IMPLEMENT.md` phản ánh đúng các thay đổi -> FAIL (`IMPLEMENT.md` chưa được ghi nhận cho task này).

## Bug
- Lỗi 1: `formatKhbdRoleLine` chèn `<br>- ` vào giữa cụm `Nhận xét của GV:`.
  - Tái hiện: Chạy `formatKhbdRoleLineBreaks("*(Nhận xét của GV: ....................)*")`, kết quả trả về `*(Nhận xét của <br>- **GV:** ....................)*`.
  - File liên quan: `js/khbd-app.js` (dòng 2301) và `canvas_soankhbd.html` (dòng 1421).
- Lỗi 2: Chưa triển khai tính năng nhận diện và cấu hình cho tiết "Luyện tập chung" / "Ôn tập".
  - Tái hiện: Thiếu hàm `isPracticeOrReviewLesson` và logic tính thời lượng/prompt luyện tập trong `js/khbd-prompts.js` và `js/khbd-app.js`.
  - File liên quan: `js/khbd-prompts.js`, `js/khbd-app.js`.
- Lỗi 3: Chưa cập nhật `docs/handoff/IMPLEMENT.md` cho đợt triển khai này.
  - Tái hiện: `IMPLEMENT.md` hiện tại chỉ có nội dung của task Auto-Save Sổ Điểm từ trước.
  - File liên quan: `docs/handoff/IMPLEMENT.md`.
