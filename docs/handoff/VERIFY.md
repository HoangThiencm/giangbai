# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `api/baogiang_mail.php`: Hàm `baogiang_send_gmail` đã nhận tham số `$ics`. Khi có tệp lịch, tạo thư dạng `multipart/mixed` với phần đính kèm `text/calendar; method=REQUEST; charset=UTF-8; name="lich_bao_giang.ics"` kèm `Content-Disposition: attachment; filename="lich_bao_giang.ics"`. Khi không có `$ics`, bảo toàn định dạng MIME cũ. Vòng lặp `$deliveries` đọc và chuyển tiếp trường `ics`. -> ĐẠT
- `phancongtochuyenmon.html`:
  + Đã khai báo bảng thời gian chuẩn `BAOGIANG_PERIOD_TIMES` (sáng tiết 1–5 từ 07:15; chiều tiết 1/6 đến 5/10 từ 13:30 đến 17:45). -> ĐẠT
  + Hàm `buildTeacherBaoGiangIcs`: tạo chuẩn VCALENDAR `METHOD:REQUEST`, `VTIMEZONE Asia/Ho_Chi_Minh`, mỗi tiết một VEVENT (đầy đủ môn, lớp, bài dạy, PPCT, giáo viên) và `VALARM` nhắc trước 15 phút (`-PT15M`). -> ĐẠT
  + Hàm `downloadIcsFile` và `exportCurrentBaoGiangIcs`: hỗ trợ tải file `LichBaoGiang_<tên>_<ngày đầu tuần>.ics` trực tiếp trên trình duyệt. -> ĐẠT
  + Giao diện đã bổ sung nút **Xuất Google Calendar (.ics)** tại tab Lịch báo giảng và tab Gửi email; tab Gửi email có ghi chú tự động đính kèm sự kiện lịch. -> ĐẠT
  + `buildTeacherBaoGiangWeekEmail` đã đính kèm `ics`, `sendBaoGiangSelectedWeekToTeachers` gửi trường `ics` trong payload sang backend. -> ĐẠT
- Đồng thời đã kiểm tra bản vá nhận diện TKB tiết chiều (quy tắc ánh xạ hàng 1-đối-1 và bảo vệ `vnEduPlusOne` trong `alignSessionPeriods`). -> ĐẠT

## Test đã chạy
- `node tests/baogiang-mail-smoke.js`: PASS
  + Khớp MIME `multipart/mixed` và header `text/calendar; method=REQUEST`.
  + Khớp `buildTeacherBaoGiangIcs`, `exportCurrentBaoGiangIcs`, `downloadIcsFile`.
  + Khớp VCALENDAR, VTIMEZONE, DTSTART/DTEND, VALARM nhắc trước 15 phút.
- `node tests/timetable-render-smoke.js`: PASS
- `node tests/baogiang-teacher-month-smoke.js`: PASS

## Pass / Fail từng tiêu chí
1. Tạo tệp lịch chuẩn `.ics` theo tuần cho từng giáo viên: PASS
2. Đính kèm `.ics` vào email gửi trực tiếp để kích hoạt nút Add to Calendar trên Gmail: PASS
3. Tải tệp `.ics` trực tiếp từ giao diện web Lịch báo giảng: PASS
4. Không ảnh hưởng đến các luồng gửi email cũ (giữ nguyên khi không có `ics`): PASS
5. Cú pháp và kiểm thử tự động toàn bộ test suite liên quan: PASS

## Bug
Không phát hiện bug mới.
