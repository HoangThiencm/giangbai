# IMPLEMENT: Lịch báo giảng — số tiết đầu tiêu đề, cả ngày, Webcal

## Đã làm
- `buildTeacherBaoGiangIcs` đặt tiêu đề `[Tiết N] Môn Lớp - bài`. Mặc định sự kiện cả ngày (`DTSTART;VALUE=DATE`). `DTEND` là ngày hôm sau vì iCalendar tính ngày kết thúc kiểu loại trừ; nếu trùng ngày bắt đầu thì lịch không hiện thẻ. Tham số thứ tư `false` giữ khung giờ `BAOGIANG_PERIOD_TIMES`.
- Tab Lịch báo giảng và tab Gửi email có hộp **Định dạng Lịch** (mặc định không gán giờ / kèm khung giờ) và nút **Lấy link đồng bộ Lịch (iPhone / Google Calendar)**. Modal hiện link Webcal, nút sao chép, và 3 bước cho iPhone lẫn Google Calendar.
- `api/calendar_feed.php`: `action=link` (cần phiên đăng nhập) trả `https_url` và `webcal_url`. Feed công khai kiểm HMAC `owner_id|teacher_id` bằng `ADMIN_KEY`, đọc `phancong_chuyenmon.data_json`, trải TKB khoảng 280 ngày, xuất `text/calendar`. `all_day=0` giữ khung giờ.

## Kiểm thử
- `node tests/timetable-render-smoke.js` — PASS (tiêu đề `[Tiết 1]`, cả ngày, không còn `T071500` ở mặc định, khung giờ khi chọn kèm giờ, nút và endpoint).
- `node tests/baogiang-mail-smoke.js` — PASS (cùng hàm `.ics` trong email; assertion tiêu đề và lời gọi đã cập nhật cho đúng hợp đồng mới).
- Không chạy được `php -l` vì máy không có PHP trong PATH. Chưa mở trang trên trình duyệt; bước đó thuộc `/verify`.

## Ngoài phạm vi
Không đổi nhận diện TKB bằng Gemini, không thêm OAuth Google.
