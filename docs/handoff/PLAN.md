# PLAN: Tối ưu hóa xuất Google Calendar / Lịch iPhone (Đưa số tiết lên đầu, loại bỏ mốc giờ giả định và gắn nút 1-chạm Webcal trực tiếp trong Email)

## Hiện trạng
1. **Lược bỏ Mistral AI**:
   - Thống nhất theo kết quả khảo sát: Không đưa Mistral vào nhận diện TKB vì `mistral-ocr-latest` không hỗ trợ phân tách cấu trúc bảng JSON theo khung tiết THCS, còn Pixtral không tối ưu bằng Gemini 2.5 Flash trên biểu mẫu tiếng Việt THCS. Hệ thống giữ nguyên Gemini 2.5 Flash làm engine nhận diện chính.

2. **Vấn đề hiển thị giờ và số tiết trong Google Calendar / Lịch iPhone**:
   - Trong `buildTeacherBaoGiangIcs()` (`phancongtochuyenmon.html`, dòng ~3439), hệ thống đang tự động gán mốc giờ cứng giả định (`BAOGIANG_PERIOD_TIMES`: Tiết 1 là 07:15 - 08:00, Tiết 2 là 08:05 - 08:50,...). Thời gian này không đúng với thực tế của trường.
   - Tiêu đề sự kiện (`SUMMARY`) hiện đang ghi dạng: `${row.subject} ${row.class_name} (Tiết ${row.period})` (Ví dụ: `Toán 63 (Tiết 1)`).
   - Khi xem trên iPhone hoặc Google Calendar Mobile: Màn hình hẹp làm chữ `(Tiết 1)` ở cuối bị che khuất (truncate), trong khi ứng dụng lại làm nổi bật mốc giờ `07:15` sai lệch. Giáo viên không biết được mình dạy tiết mấy.
   - Người dùng phản hồi: "Tôi đâu cần thời gian, nhìn vô không biết dạy tiết mấy".

3. **Vấn đề khi mở Email trên iPhone ("rõ ràng trong email thì nó có ứng dụng chứ đâu có mở trên Safari")**:
   - Khi giáo viên mở email bằng ứng dụng **Gmail** hoặc **Mail** trên iPhone:
     + Ở cuối thư có tệp đính kèm `lich_bao_giang.ics`.
     + Khi bấm vào tệp này: Ứng dụng Gmail trên iPhone **chỉ mở trình xem tệp (file viewer) nội bộ** của nó, hiển thị văn bản thô hoặc bản xem trước, chứ KHÔNG có nút đẩy vào Google Calendar hay tự động lưu lịch.
     + Giáo viên bị "mắc kẹt" tại màn hình xem tệp của ứng dụng email mà không biết làm sao để lịch vào ứng dụng Calendar.
   - **Giải pháp dứt điểm ngay trong nội dung Email**:
     + Không bắt giáo viên phải bấm vào tệp đính kèm phức tạp nữa.
     + Trong chính nội dung email (ngay bên dưới bảng TKB/Lịch báo giảng), hệ thống chèn **2 Nút bấm hành động trực tiếp**:
       1. Nút 📅 **"Thêm tự động vào Lịch iPhone (1 chạm)"** (liên kết dạng `webcal://...`).
       2. Nút 📆 **"Thêm vào Google Calendar"** (liên kết dạng `https://calendar.google.com/calendar/r?cid=webcal://...`).
     + Khi giáo viên đọc email trên iPhone và bấm vào nút này: Ứng dụng email sẽ tự động chuyển hướng gọi hệ điều hành iOS / Google Calendar bật bảng xác nhận: *"Bạn có muốn đăng ký lịch này không?"* $\rightarrow$ Bấm **Đăng ký** là toàn bộ lịch vào thẳng ứng dụng Calendar, không bao giờ bị rơi vào màn hình xem tệp nữa!

---

## Phạm vi
1. **Chuẩn hóa tiêu đề sự kiện Lịch (.ics)**:
   - Sửa `buildTeacherBaoGiangIcs`:
     + Đưa số Tiết lên đầu tiêu đề: `SUMMARY:[Tiết ${row.period}] ${row.subject} - Lớp ${row.class_name}${lessonTitle ? ' (' + lessonTitle + ')' : ''}`.
     + Bổ sung chế độ sự kiện Cả ngày (All-day) / Không gán giờ (`allDayMode`): Sử dụng `DTSTART;VALUE=DATE:YYYYMMDD` để các tiết học hiển thị thành các thẻ rõ ràng trên đầu ngày theo đúng thứ tự Tiết 1, Tiết 2, Tiết 3..., loại bỏ hoàn toàn mốc giờ giả định 07:15.
2. **Gắn nút kích hoạt trực tiếp trong Email**:
   - Cập nhật mẫu email trong `buildTeacherIndividualTimetableEmail` và `buildTeacherBaoGiangWeekEmail`:
     Thêm thanh nút bấm nổi bật ngay dưới bảng lịch:
     + Nút: **[📱 Thêm vào Lịch iPhone]**
     + Nút: **[🌐 Thêm vào Google Calendar]**
3. **Xây dựng endpoint Webcal Feed (`api/calendar_feed.php`)**:
   - Cung cấp endpoint nhận `teacher_id` và `token`, trả về dữ liệu lịch chuẩn iCalendar `text/calendar`.
   - Giúp lịch tự động cập nhật cả năm trên iPhone và Google Calendar.
4. **Cập nhật giao diện tùy chọn xuất lịch trên Web**:
   - Thêm nút/hộp chọn: "Định dạng Lịch: [Tiết 1, 2, 3... không gán giờ] hoặc [Kèm khung giờ]" khi bấm xuất hoặc gửi lịch.

---

## Ngoài phạm vi
- Không can thiệp vào AI nhận diện TKB (giữ nguyên Gemini Flash).
- Không can thiệp sang các mô-đun Soạn KHBD, Đề thi, Sổ điểm.
- Không cấu hình Google Cloud Console OAuth 2.0 (sử dụng cơ chế Webcal Feed chuẩn quốc tế để mọi giáo viên dùng được ngay lập tức).

---

## File dự kiến tác động
- `api/calendar_feed.php` (Tạo mới: Cung cấp endpoint Webcal feed cho iPhone / Google Calendar).
- `phancongtochuyenmon.html` (Cập nhật định dạng `SUMMARY` trong .ics, chèn nút 1-chạm vào mẫu HTML của email, bổ sung tùy chọn All-day không gán giờ).
- `tests/timetable-render-smoke.js` (Bổ sung kiểm thử tự động định dạng .ics mới, nút trong email và endpoint calendar feed).
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa handoff**:
   - Xóa `docs/handoff/.lock` trước khi sửa source code.

2. **Bước 2: Cải tiến định dạng sự kiện Lịch (.ics) trong `phancongtochuyenmon.html`**:
   - Trong hàm `buildTeacherBaoGiangIcs`:
     + Sửa `summary`:
       ```javascript
       const summary = `[Tiết ${row.period}] ${row.subject || ''} ${row.class_name || ''}${lessonTitle ? ' - ' + lessonTitle : ''}`;
       ```
     + Thêm tùy chọn `allDay`:
       Khi `allDay` được bật:
       ```javascript
       `DTSTART;VALUE=DATE:${String(row.date).replace(/-/g, '')}`,
       `DTEND;VALUE=DATE:${String(row.date).replace(/-/g, '')}`,
       ```
       Lịch trên iPhone và Google Calendar sẽ hiển thị các thanh sự kiện trong ngày dạng `[Tiết 1] Toán 63`, `[Tiết 2] Văn 64` cực kỳ trực quan, không còn bị chèn giờ `07:15` sai lệch.

3. **Bước 3: Tạo endpoint `api/calendar_feed.php` (Đồng bộ trực tiếp cả năm)**:
   - Endpoint nhận `teacher_id` và mã xác thực `token` (hoặc mã bảo mật của tổ/trường).
   - Đọc dữ liệu TKB / Lịch báo giảng từ CSDL, xuất ra định dạng `text/calendar; charset=utf-8`.
   - Hỗ trợ giao thức `webcal://` khi người dùng bấm trực tiếp từ iPhone.

4. **Bước 4: Chèn nút 1-chạm vào thẳng nội dung Email và giao diện Web**:
   - Trong hàm tạo HTML email (`buildTeacherBaoGiangWeekEmail` và `buildTeacherIndividualTimetableEmail`):
     Bổ sung đoạn HTML chứa 2 nút bấm với kiểu dáng đẹp mắt (màu sắc rõ nét, dễ bấm trên điện thoại):
     ```html
     <div style="margin: 20px 0; text-align: center;">
         <a href="webcal://..." style="display:inline-block; padding:12px 20px; background:#0284c7; color:#fff; text-decoration:none; border-radius:8px; font-weight:bold; margin-right:10px;">📱 Thêm vào Lịch iPhone</a>
         <a href="https://calendar.google.com/calendar/r?cid=webcal://..." target="_blank" style="display:inline-block; padding:12px 20px; background:#4f46e5; color:#fff; text-decoration:none; border-radius:8px; font-weight:bold;">🌐 Thêm vào Google Calendar</a>
     </div>
     ```

5. **Bước 5: Kiểm thử và cập nhật nhật ký**:
   - Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.
   - Ghi nhật ký vào `docs/handoff/IMPLEMENT.md`.
   - Tạo lại `docs/handoff/.lock` nội dung `LOCK`.

---

## Rủi ro
1. **Chu kỳ làm mới của Google Calendar**:
   - Google Calendar quét link Webcal định kỳ (khoảng vài tiếng/lần theo cơ chế Google). Khi đổi TKB trên web, lịch trên Google Calendar có thể mất một khoảng thời gian ngắn để đồng bộ.
2. **Khả năng tương thích trên iPhone**:
   - Chuẩn `webcal://` được Apple hỗ trợ trực tiếp từ trong ứng dụng email và Safari trên mọi dòng iPhone.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/timetable-render-smoke.js`.
2. **Kiểm thử thủ công**:
   - Mở email trên ứng dụng Gmail/Mail của iPhone: Bấm nút "Thêm vào Lịch iPhone", xác nhận iOS tự động bật hộp thoại đăng ký.
   - Xác nhận tiêu đề sự kiện hiển thị rõ `[Tiết 1]...` ngay đầu dòng.
   - Kiểm tra chế độ sự kiện cả ngày: Không còn thấy các mốc giờ 07:15 giả định.

---

## Tiêu chí nghiệm thu
- Tiêu đề sự kiện lịch đưa số tiết lên đầu (`[Tiết 1]...`), không bị che khuất trên màn hình iPhone / Google Calendar.
- Hỗ trợ chế độ không gán mốc giờ sai lệch, đúng nhu cầu "không cần thời gian, chỉ cần biết tiết mấy" của giáo viên.
- Trong chính nội dung email có nút bấm 1-chạm để tự động lưu vào Lịch iPhone / Google Calendar, không bắt giáo viên phải bấm mở tệp đính kèm xem trước.
