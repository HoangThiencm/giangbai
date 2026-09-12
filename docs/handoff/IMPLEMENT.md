# IMPLEMENT: Báo giảng, TKB và tự cập nhật phiên bản sau deploy

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Thay đổi đã thực hiện

- `phancongtochuyenmon.html`
  - Gom bài PPCT theo tên đã chuẩn hóa qua các tuần liên tiếp, kể cả khi mạch khác xen giữa; Bài 11 ba tuần nhận đúng `1/3`, `2/3`, `3/3`.
  - Chỉ tạo cảnh báo từ tuần đang xem trở đi; tuần cũ không còn xuất hiện trong cảnh báo hoặc ảnh hưởng tới gửi email.
  - Phát hiện nhiều giáo viên cùng có TKB cho một lớp/môn/tuần và liệt kê tên cùng tổng số tiết.
  - Email cá nhân chỉ xét cảnh báo thuộc các lớp/môn của giáo viên đăng nhập. Cảnh báo trở thành hộp xác nhận tiếp tục gửi, không còn chặn cứng.
  - Chuẩn hóa bài dạy trên bảng web, email văn bản, email HTML cá nhân và email tổ: `Tuần [X]  [Tên bài] (tiết ppct: [Y]) [A/B]`. Email HTML dùng chung hàm định dạng này trong cột Bài dạy.
  - Tab **Thời khoá biểu GV** có checkbox chọn từng giáo viên, nút **Chọn tất cả GV có TKB**, **Bỏ chọn**, và bộ đếm số giáo viên đang chọn.
  - Thêm `buildSelectedTeachersTimetableEmail(teacherIds)`: tạo email chỉ có TKB của các giáo viên đã chọn, tách thành từng card; mỗi card có lưới Buổi sáng/Buổi chiều, Thứ 2–Thứ 7, tiết, môn và lớp. Nội dung này không bao gồm báo giảng hoặc PPCT.
  - Thêm `sendSelectedTeachersTimetableEmail()`: kiểm tra phải chọn ít nhất một giáo viên có TKB, rồi gửi `{ subject, body, html }` qua `api/baogiang_mail.php` về email của tài khoản hiện hành; hiển thị toast thành công hoặc lỗi.
- `tests/baogiang-weekday-segment-smoke.js`
  - Kiểm tra Bài 11 qua tuần 4–6, phát hiện hai giáo viên cùng dạy, loại trừ cảnh báo tuần đã qua, và định dạng bài dạy chuẩn cho email HTML.
- `tests/timetable-render-smoke.js`
  - Kiểm tra mẫu email TKB nhiều giáo viên có card riêng, hai lưới sáng/chiều, cột Thứ 2–Thứ 7, môn/lớp; xác nhận email không kèm báo giảng hoặc PPCT.
- `.github/workflows/ftp-deploy.yml`
  - Sinh `version.json` gồm commit SHA và thời điểm deploy trước bước đồng bộ FTP.
- `.htaccess`
  - Buộc trình duyệt kiểm tra lại `.html`, `.htm` và `.json`, không lưu cache các tài nguyên này.
- `js/security-guard.js`
  - Thêm `initAutoUpdateChecker()` dùng manifest `/version.json` với `cache: 'no-store'`; lần truy cập đầu chỉ ghi nhận phiên bản. Khi SHA thay đổi, trang reload một lần và lưu mốc debounce 10 giây trong session để tránh vòng lặp.
  - Kiểm tra khi trang được mở lại, nhận focus và mỗi 60 giây; lỗi mạng/manifest không làm gián đoạn trang.
- `tests/auto-reload-smoke.js`
  - Kiểm tra lần truy cập đầu, phiên bản thay đổi, debounce, lỗi mạng, workflow manifest và cấu hình cache máy chủ.

## Kiểm tra

- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `node tests/auto-reload-smoke.js`: PASS.
- `git diff --check`: PASS.

## Cần xác minh trong `/verify`

- Tick 2–3 giáo viên có TKB trong tab Thời khoá biểu GV, gửi email và kiểm tra bố cục email trên hộp thư cá nhân.
