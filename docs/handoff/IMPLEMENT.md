# IMPLEMENT: Đính kèm Google Calendar (.ics) cho Lịch báo giảng

## Đã làm
- `api/baogiang_mail.php`: `baogiang_send_gmail` nhận thêm `$ics`. Khi có nội dung lịch, thư gửi dạng `multipart/mixed`: khối `multipart/alternative` (text/plain và text/html) và file đính kèm `text/calendar; method=REQUEST` tên `lich_bao_giang.ics`. Không có `ics` thì MIME giữ như cũ. Vòng `deliveries` đọc trường `ics`.
- `phancongtochuyenmon.html`:
  - `BAOGIANG_PERIOD_TIMES`: sáng tiết 1–5 từ 07:15; chiều tiết 1/6 đến 5/10 từ 13:30 đến 17:45.
  - `buildTeacherBaoGiangIcs`: VCALENDAR `METHOD:REQUEST`, `VTIMEZONE Asia/Ho_Chi_Minh`, mỗi tiết một VEVENT (môn, lớp, bài, PPCT, giáo viên) và `VALARM` `-PT15M`.
  - `downloadIcsFile` và `exportCurrentBaoGiangIcs`: tải `LichBaoGiang_<tên>_<ngày đầu tuần>.ics`. Trên tab Lịch báo giảng lấy giáo viên đang lọc (hoặc giáo viên đầu tiên) và tuần của ngày đang xem. Trên tab Gửi email lấy tuần đang chọn và giáo viên được tích đầu tiên.
  - `buildTeacherBaoGiangWeekEmail` trả thêm `ics`. `sendBaoGiangSelectedWeekToTeachers` gửi trường đó trong payload.
  - Nút **Xuất Google Calendar (.ics)** cạnh **Cài đặt PPCT & Lịch nghỉ** và trên tab LBG của Gửi email. Tab email có dòng ghi lịch được đính kèm tự động.
- `tests/baogiang-mail-smoke.js`: kiểm tra PHP nhận `ics` và header `text/calendar`; kiểm tra hàm, nút, ghi chú; chạy `buildTeacherBaoGiangIcs` với tiết sáng 1, chiều 8 và chiều 10.

## Kiểm thử
- `node tests/baogiang-mail-smoke.js` → PASS.
- `node tests/timetable-render-smoke.js` → PASS.
- `node tests/baogiang-teacher-month-smoke.js` → PASS.

## Chưa kiểm trên trình duyệt
- Chưa bấm tải file `.ics` trên giao diện và chưa gửi thư Gmail để xem nút thêm vào Google Calendar. Phần đó để `/verify`.
