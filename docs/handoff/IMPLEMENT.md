# IMPLEMENT: Nút Webcal ngay trong nội dung email

## Đã làm
- Giữ tiêu đề `[Tiết N] Môn Lớp - bài` và sự kiện cả ngày (`DTEND` là ngày hôm sau theo quy tắc iCalendar). Hộp **Định dạng Lịch** và modal đồng bộ trên web giữ nguyên.
- `calendarSubscribeButtonsHtml` chèn dưới bảng lịch hai nút: **📱 Thêm vào Lịch iPhone** (`webcal://...`) và **🌐 Thêm vào Google Calendar** (`https://calendar.google.com/calendar/r?cid=` + link đã mã hóa).
- Nút nằm trong HTML của `buildTeacherBaoGiangWeekHtml` / `buildTeacherBaoGiangWeekEmail` và `buildTeacherIndividualTimetableEmail`.
- Khi gửi, `baoGiangCalendarFeedWebcal` gọi `api/calendar_feed.php?action=link` (phiên đăng nhập) để lấy link cá nhân theo giáo viên và theo chế độ cả ngày hoặc kèm giờ, rồi mới gắn vào thư.

## Kiểm thử
- `node tests/timetable-render-smoke.js` — PASS (nút trong email TKB cá nhân, cid Google, email lịch báo giảng gọi helper).
- `node tests/baogiang-mail-smoke.js` — PASS.

## Ngoài phạm vi
Không đổi Gemini nhận diện TKB, không thêm OAuth. Chưa bấm nút trong app Gmail/Mail trên iPhone; bước đó thuộc `/verify`.
