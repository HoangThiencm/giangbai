# IMPLEMENT: Đồng bộ lịch 1 chạm iPhone (iOS 18) và Google Calendar

## Đã làm
- Giữ tiêu đề `[Tiết N] Môn Lớp - bài` và chế độ cả ngày. `DTEND` là ngày hôm sau (iCalendar loại trừ ngày kết thúc) để thẻ cả ngày hiện được. Hộp **Định dạng Lịch** vẫn chọn không gán giờ hoặc kèm khung giờ.
- Nút cạnh xuất `.ics` đổi thành **Đồng bộ Lịch (iPhone / Google Calendar)** trên tab Lịch báo giảng và tab Gửi email.
- Modal có **Thêm ngay vào Lịch iPhone** (`href` = `webcal://...`) và **Thêm ngay vào Google Calendar** (`https://calendar.google.com/calendar/r?cid=` + link webcal đã mã hóa). Link lấy từ `api/calendar_feed.php?action=link`, kèm `all_day` theo hộp định dạng.
- Hướng dẫn iPhone 16 Pro (iOS 18): Cách A trong app Lịch (Lịch → Thêm lịch → Thêm lịch đăng ký); Cách B trong Cài đặt (Cài đặt → Ứng dụng → Lịch → Tài khoản Lịch → Thêm tài khoản → Khác → Thêm lịch đã đăng ký).

## Kiểm thử
- `node tests/timetable-render-smoke.js` — PASS.

## Ngoài phạm vi
Không đổi Gemini nhận diện TKB, không thêm OAuth Google. Chưa bấm được hộp thoại Đăng ký trên iPhone 16 Pro; bước đó thuộc `/verify` thủ công.
