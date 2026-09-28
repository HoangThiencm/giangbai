# PLAN: Tối ưu hóa xuất Google Calendar / Lịch iPhone (Đưa số tiết lên đầu, loại bỏ mốc giờ giả định và hỗ trợ Webcal 1-chạm cho iPhone iOS 18 & Google Calendar)

## Hiện trạng
1. **Lược bỏ Mistral AI**:
   - Thống nhất theo kết quả khảo sát: Không đưa Mistral vào nhận diện TKB vì `mistral-ocr-latest` không hỗ trợ phân tách cấu trúc bảng JSON theo khung tiết THCS, còn Pixtral không tối ưu bằng Gemini 2.5 Flash trên biểu mẫu tiếng Việt THCS. Hệ thống giữ nguyên Gemini 2.5 Flash làm engine nhận diện chính.

2. **Vấn đề hiển thị giờ và số tiết trong Google Calendar / Lịch iPhone**:
   - Trong `buildTeacherBaoGiangIcs()` (`phancongtochuyenmon.html`, dòng ~3439), hệ thống đang tự động gán mốc giờ cứng giả định (`BAOGIANG_PERIOD_TIMES`: Tiết 1 là 07:15 - 08:00, Tiết 2 là 08:05 - 08:50,...). Thời gian này không đúng với thực tế của trường.
   - Tiêu đề sự kiện (`SUMMARY`) hiện đang ghi dạng: `${row.subject} ${row.class_name} (Tiết ${row.period})` (Ví dụ: `Toán 63 (Tiết 1)`).
   - Khi xem trên iPhone hoặc Google Calendar Mobile: Màn hình hẹp làm chữ `(Tiết 1)` ở cuối bị che khuất (truncate), trong khi ứng dụng lại làm nổi bật mốc giờ `07:15` sai lệch. Giáo viên không biết được mình dạy tiết mấy.
   - Người dùng phản hồi: "Tôi đâu cần thời gian, nhìn vô không biết dạy tiết mấy".

3. **Vấn đề đẩy thẳng lịch vào iPhone (iOS 18 / iPhone 16 Pro) & Google Calendar**:
   - Hiện tại hệ thống gửi email đính kèm tệp `.ics`. Trên iPhone, ứng dụng Mail chỉ mở bản xem trước của tệp đính kèm để bấm "Thêm vào Lịch", không tự động đẩy ngầm vào Google Calendar được do giới hạn bảo mật (không có Google OAuth 2.0).
   - Trên các dòng máy mới như **iPhone 16 Pro (chạy iOS 18)**: Apple đã thay đổi giao diện Cài đặt (mục Lịch nằm trong mục *Ứng dụng (Apps)* ở cuối Settings), khiến giáo viên khó tìm thấy chỗ thêm lịch thủ công.
   - **Giải pháp tối ưu chuẩn quốc tế: Nút 1-chạm Webcal (`webcal://`)**:
     + Trên iPhone (Safari/Chrome): Khi bấm vào đường link dạng `webcal://ten-mien/api/calendar_feed.php?token=...`, hệ thống iOS tự động hiển thị hộp thoại pop-up: *"Bạn có muốn đăng ký lịch này không?"*. Thầy/cô chỉ cần bấm **Đăng ký (Subscribe)** là xong ngay 1 chạm, không cần vào Cài đặt hay dán link thủ công.
     + Toàn bộ TKB và Lịch báo giảng sẽ **tự động đẩy và đồng bộ xuyên suốt cả năm** vào iPhone và Google Calendar, không cần gửi email hay tải mở từng tệp `.ics` mỗi tuần.

---

## Phạm vi
1. **Chuẩn hóa tiêu đề sự kiện Lịch (.ics)**:
   - Sửa `buildTeacherBaoGiangIcs`:
     + Đưa số Tiết lên đầu tiêu đề: `SUMMARY:[Tiết ${row.period}] ${row.subject} - Lớp ${row.class_name}${lessonTitle ? ' (' + lessonTitle + ')' : ''}`.
     + Bổ sung chế độ sự kiện Cả ngày (All-day) / Không gán giờ (`allDayMode`): Sử dụng `DTSTART;VALUE=DATE:YYYYMMDD` để các tiết học hiển thị thành các thẻ rõ ràng trên đầu ngày theo đúng thứ tự Tiết 1, Tiết 2, Tiết 3..., loại bỏ hoàn toàn mốc giờ giả định 07:15.
2. **Xây dựng luồng đồng bộ trực tiếp qua Webcal (`api/calendar_feed.php`)**:
   - Tạo endpoint `api/calendar_feed.php?token=...&teacher_id=...` cung cấp chuẩn iCalendar Feed (Webcal) với đầy đủ dữ liệu TKB / Lịch báo giảng mới nhất.
   - Cung cấp nút **"Đồng bộ vào iPhone (1 chạm)"** bằng link `webcal://...` để iOS tự bật hộp thoại đăng ký.
   - Cung cấp nút **"Đồng bộ vào Google Calendar"** bằng link `https://calendar.google.com/calendar/r?cid=webcal://...`.
   - Hướng dẫn rõ ràng vị trí trên iOS 18 (iPhone 16 Pro) cả 2 cách:
     * Cách A (Trong app Lịch): Mở app Lịch -> Bấm chữ "Lịch" dưới cùng -> Bấm "Thêm lịch" góc trái dưới -> Chọn "Thêm lịch đăng ký...".
     * Cách B (Trong Cài đặt iOS 18): Cài đặt -> Ứng dụng -> Lịch -> Tài khoản Lịch -> Thêm tài khoản -> Khác -> Thêm lịch đã đăng ký.
3. **Cập nhật giao diện tùy chọn xuất lịch**:
   - Thêm nút/hộp chọn: "Định dạng Lịch: [Tiết 1, 2, 3... không gán giờ] hoặc [Kèm khung giờ]" khi bấm xuất hoặc gửi lịch.

---

## Ngoài phạm vi
- Không can thiệp vào AI nhận diện TKB (giữ nguyên Gemini Flash).
- Không can thiệp sang các mô-đun Soạn KHBD, Đề thi, Sổ điểm.
- Không cấu hình Google Cloud Console OAuth 2.0 (sử dụng cơ chế Webcal Feed chuẩn quốc tế để mọi giáo viên dùng được ngay lập tức).

---

## File dự kiến tác động
- `api/calendar_feed.php` (Tạo mới: Cung cấp endpoint Webcal feed cho iPhone / Google Calendar).
- `phancongtochuyenmon.html` (Cập nhật định dạng `SUMMARY` trong .ics, bổ sung tùy chọn All-day không gán giờ, thêm nút đồng bộ 1-chạm Webcal và hướng dẫn chi tiết cho iOS 18 / iPhone 16 Pro).
- `tests/timetable-render-smoke.js` (Bổ sung kiểm thử tự động định dạng .ics mới và endpoint calendar feed).
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

4. **Bước 4: Bổ sung giao diện và hướng dẫn trên `phancongtochuyenmon.html`**:
   - Thêm nút "Đồng bộ Lịch (iPhone / Google Calendar)" cạnh nút "Xuất Google Calendar (.ics)".
   - Khi bấm, mở modal popup có:
     * Nút bấm 1-chạm: **"Thêm ngay vào Lịch iPhone"** (`href="webcal://..."`).
     * Nút bấm 1-chạm: **"Thêm ngay vào Google Calendar"** (`href="https://calendar.google.com/calendar/r?cid=webcal://..."`).
     * Hướng dẫn trực quan riêng cho iPhone chạy iOS 18 (iPhone 16 Pro).

5. **Bước 5: Kiểm thử và cập nhật nhật ký**:
   - Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.
   - Ghi nhật ký vào `docs/handoff/IMPLEMENT.md`.
   - Tạo lại `docs/handoff/.lock` nội dung `LOCK`.

---

## Rủi ro
1. **Chu kỳ làm mới của Google Calendar**:
   - Google Calendar quét link Webcal định kỳ (khoảng vài tiếng/lần theo cơ chế Google). Khi đổi TKB trên web, lịch trên Google Calendar có thể mất một khoảng thời gian ngắn để đồng bộ.
2. **Khả năng tương thích trên iPhone**:
   - Chuẩn `webcal://` được Apple hỗ trợ trực tiếp trên toàn bộ các đời iOS, đặc biệt là iOS 18 trên iPhone 16 Pro.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/timetable-render-smoke.js`.
2. **Kiểm thử thủ công**:
   - Mở file `.ics` trên iPhone: Xác nhận dòng tiêu đề hiển thị rõ ràng `[Tiết 1] Toán 63` ngay đầu dòng.
   - Bấm nút link 1-chạm `webcal://` trên iPhone 16 Pro: Xác nhận iOS 18 bật pop-up đăng ký lịch tự động.
   - Kiểm tra chế độ sự kiện cả ngày: Không còn thấy các mốc giờ 07:15 giả định.

---

## Tiêu chí nghiệm thu
- Tiêu đề sự kiện lịch đưa số tiết lên đầu (`[Tiết 1]...`), không bị che khuất trên màn hình iPhone / Google Calendar.
- Hỗ trợ chế độ không gán mốc giờ sai lệch, đúng nhu cầu "không cần thời gian, chỉ cần biết tiết mấy" của giáo viên.
- Có nút 1-chạm `webcal://` tự động kích hoạt hộp thoại đăng ký trên iPhone 16 Pro (iOS 18) và Google Calendar.
