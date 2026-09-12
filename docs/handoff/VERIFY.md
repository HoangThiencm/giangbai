# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Bỏ qua các tuần đã qua trong quá khứ khỏi danh sách cảnh báo và không làm ảnh hưởng/chặn gửi email.
- [x] Phát hiện và cảnh báo cụ thể khi 1 lớp có 2 giáo viên cùng dạy trong cùng tuần (liệt kê tên các giáo viên và tổng số tiết TKB).
- [x] Gửi email cá nhân không còn bị chặn cứng (`throw new Error`), chuyển thành hộp xác nhận tiếp tục gửi khi có cảnh báo.
- [x] Thuật toán PPCT đa tuần hỗ trợ trọn vẹn 3 tuần liên tiếp trở lên (Bài 11 dạy tuần 4, 5, 6 nhận chuẩn xác `1/3, 2/3, 3/3`).
- [x] Chuẩn hóa định dạng hiển thị bài dạy trên Web Lịch báo giảng, email văn bản, email HTML cá nhân và email tổ: `Tuần [X]  [Tên bài] (tiết ppct: [Y]) [A/B]`.
- [x] Thêm checkbox chọn từng giáo viên, nút chọn tất cả GV có TKB, bỏ chọn trong tab Thời khóa biểu (`#view-timetable`).
- [x] Xây dựng tính năng gửi Thời khóa biểu các giáo viên được tick chọn về email cá nhân qua `api/baogiang_mail.php`: phân tách rõ ràng từng giáo viên, dạng lưới TKB trực quan, hoàn toàn không kèm lịch báo giảng hay PPCT.
- [x] Tự động sinh manifest `version.json` trong workflow GitHub Actions `.github/workflows/ftp-deploy.yml` mỗi lần push lên GitHub.
- [x] Cấu hình file `.htaccess` chống cache cho tệp `.html`, `.htm`, `.json` trên máy chủ hosting `hoangthiencm.id.vn`.
- [x] Tích hợp module auto-reload vào `js/security-guard.js`: tự động phát hiện bản deploy mới từ GitHub và reload toàn bộ hệ thống trang web trên `hoangthiencm.id.vn`.

## Test đã chạy
1. `node tests/baogiang-weekday-segment-smoke.js`: **PASS**
   - Bài 11 học 3 tuần (Tuần 4 tiết 6, Tuần 5 tiết 7, Tuần 6 tiết 8) đạt đúng phân đoạn `1/3, 2/3, 3/3`.
   - Hàm `formatBaoGiangLessonDisplay` định dạng chuẩn `Tuần 4  Bài 11. Tỉ số lượng giác của góc nhọn (tiết ppct: 6) 1/3`.
   - Cảnh báo tuần đã qua được loại trừ khỏi danh sách cảnh báo.
   - Phát hiện chính xác trường hợp 1 lớp 2 giáo viên cùng dạy.
2. `node tests/timetable-render-smoke.js`: **PASS**
   - Tab Thời khóa biểu hỗ trợ nạp ID số và chuỗi JSON.
   - Kiểm tra đầy đủ giao diện checkbox, nút chọn tất cả / bỏ chọn.
   - Hàm `buildSelectedTeachersTimetableEmail` dựng email HTML TKB nhiều giáo viên dạng card tách biệt, có đầy đủ lưới sáng/chiều, Thứ 2–Thứ 7, môn/lớp và không kèm lịch báo giảng hay PPCT.
3. `node tests/auto-reload-smoke.js`: **PASS**
   - Lần truy cập đầu ghi nhận phiên bản mà không reload.
   - Request kiểm tra manifest luôn bỏ qua cache (`cache: 'no-store'`).
   - Tự động kiểm tra định kỳ mỗi 60 giây và khi focus/visibilitychange.
   - Khi phát hiện SHA mới trên server, tự động reload và cập nhật `localStorage`.
   - Debounce reload 10 giây ngăn chặn vòng lặp reload.
   - Lỗi mạng hoặc manifest tạm thời không làm gián đoạn trang web.
   - Workflow GitHub Actions tạo `version.json` trước khi FTP sync.
   - File `.htaccess` vô hiệu hóa cache cho HTML và JSON.

## Pass / Fail từng tiêu chí
1. Bỏ qua các tuần đã qua khỏi danh sách cảnh báo: **PASS**
2. Phát hiện và cảnh báo 1 lớp 2 giáo viên cùng dạy: **PASS**
3. Phân đoạn đa tuần 3 tuần liên tiếp (Bài 11 tuần 4, 5, 6 đạt `1/3, 2/3, 3/3`): **PASS**
4. Chuẩn hóa chuỗi hiển thị `Tuần X  Bài ... (tiết ppct: Y) A/B`: **PASS**
5. Tick chọn nhiều GV và gửi TKB qua email cá nhân dạng lưới TKB riêng biệt: **PASS**
6. Tự động reload toàn bộ web sau mỗi lần push lên GitHub cho `hoangthiencm.id.vn`: **PASS**
7. Toàn bộ 3 bộ test tự động của dự án: **PASS 100%**

## Bug
Không có bug tồn đọng.