# PLAN: Nâng cấp gửi Thời khóa biểu và Lịch báo giảng trực tiếp cho các giáo viên trong tổ qua Email

---

## 1. Yêu cầu & Mục tiêu
- **Yêu cầu**: Nâng cấp hệ thống gửi email trong Quản lý tổ chuyên môn (`phancongtochuyenmon.html`) và backend (`api/baogiang_mail.php`) để có thể gửi Thời khóa biểu và Lịch báo giảng trực tiếp đến hòm thư (email) của từng giáo viên trong tổ chuyên môn, thay vì chỉ gửi về email cá nhân (`BAOGIANG_GMAIL_FROM`).
- **Mục tiêu chi tiết**:
  1. **Backend (`api/baogiang_mail.php`)**:
     - Hỗ trợ gửi danh sách email người nhận (`recipients`: mảng email hoặc mảng `deliveries: [{ to, subject, body, html }]`).
     - Tôn trọng cờ cấu hình `BAOGIANG_GMAIL_TO_SELF_ONLY`: nếu `true` thì chuyển hướng an toàn về `BAOGIANG_GMAIL_FROM`; nếu `false` thì cho phép gửi thẳng đến các email đích được chỉ định.
     - Xác thực tính hợp lệ của từng địa chỉ email trước khi gửi (`filter_var(..., FILTER_VALIDATE_EMAIL)`).
     - Giới hạn an toàn: tối đa 50 email / lần gửi để chống spam và tránh nghẽn SMTP Gmail.
     - Giãn cách an toàn (`usleep(150000)`) giữa các lần gửi liên tiếp để Gmail SMTP không chặn kết nối.
  2. **Thời khóa biểu (`phancongtochuyenmon.html` - view-timetable)**:
     - Tại danh sách giáo viên có TKB, bên cạnh nút chọn tất cả, bổ sung tùy chọn gửi email:
       - Tùy chọn 1: *Gửi riêng TKB cho từng GV đã chọn* (mỗi thầy cô nhận email chứa bảng TKB của chính mình).
       - Tùy chọn 2: *Gửi bản tổng hợp TKB các GV đã chọn về email cá nhân* (giữ nguyên tính năng cũ).
  3. **Lịch báo giảng (`phancongtochuyenmon.html` - view-baogiang)**:
     - Tại mục "Người nhận email" (`#bg-recipient-list`), người dùng đã tích chọn các giáo viên và điền email.
     - Bổ sung nút: **"Gửi lịch tuần cho các GV đã chọn"** bên cạnh nút "Gửi lịch tuần đã chọn (cá nhân)".
     - Khi bấm nút này: hệ thống lọc đúng các tiết dạy trong tuần của từng giáo viên đã chọn, tạo email lịch báo giảng cá nhân hóa cho từng thầy cô và gửi thẳng đến email của họ.
  4. **Cấu hình mẫu (`api/config.sample.php`)**:
     - Cập nhật hướng dẫn và giá trị mẫu `BAOGIANG_GMAIL_TO_SELF_ONLY` để người dùng hosting dễ dàng kích hoạt.

---

## 2. Phạm vi tệp tin cần sửa đổi (Scope)
1. `api/baogiang_mail.php`
2. `api/config.sample.php`
3. `phancongtochuyenmon.html`
4. `tests/timetable-render-smoke.js`

---

## 3. Hướng dẫn chi tiết cho Coder

### PHẦN A: Nâng cấp Backend `api/baogiang_mail.php`

1. **Hỗ trợ đa người nhận / đa gói gửi (deliveries)**:
   - Đọc payload JSON:
     - Hỗ trợ `deliveries` (mảng các object `{ to, subject, body, html }`).
     - Hoặc `recipients` (mảng email) dùng chung `subject`, `body`, `html`.
     - Hoặc `recipient` đơn lẻ / mặc định fallback về `BAOGIANG_GMAIL_FROM`.
2. **Kiểm tra cờ `BAOGIANG_GMAIL_TO_SELF_ONLY`**:
   ```php
   $selfOnly = !defined('BAOGIANG_GMAIL_TO_SELF_ONLY') || BAOGIANG_GMAIL_TO_SELF_ONLY === true;
   ```
   - Nếu `$selfOnly === true`: tất cả email đều được gửi về `(string) BAOGIANG_GMAIL_FROM` kèm lời chú thích trong kết quả.
   - Nếu `$selfOnly === false`: gửi trực tiếp đến địa chỉ email đích hợp lệ của từng giáo viên.
3. **Thực thi vòng lặp gửi an toàn**:
   - Lọc các email hợp lệ bằng `filter_var($to, FILTER_VALIDATE_EMAIL)`.
   - Giới hạn mảng tối đa 50 người nhận.
   - Với mỗi người nhận:
     - Gọi `baogiang_send_gmail($to, $itemSubject, $itemBody, $itemHtml)`.
     - Dừng nhẹ `usleep(150000)` (150ms) giữa các email.
   - Đếm số lượng thành công `$sentCount` và ghi nhận lỗi nếu có.
   - Trả về JSON:
     ```json
     {
       "ok": true,
       "sent_count": 5,
       "message": "Đã gửi email thành công cho 5 giáo viên."
     }
     ```

---

### PHẦN B: Cập nhật Cấu hình mẫu `api/config.sample.php`

- Dòng 49:
  ```php
  // Đặt false để cho phép gửi email trực tiếp tới từng giáo viên trong tổ; đặt true nếu chỉ muốn gửi về email cá nhân người gửi.
  define('BAOGIANG_GMAIL_TO_SELF_ONLY', false);
  ```

---

### PHẦN C: Nâng cấp Giao diện và Logic gửi Mail trong `phancongtochuyenmon.html`

#### 1. Tại Thẻ "Thời khoá biểu" (`view-timetable`):
- Trong danh sách giáo viên bên trái (`#tt-teacher-list`):
  - Cho phép xem/nhập nhanh email của từng giáo viên nếu chưa có (lấy từ `t.email` trong `state.teachers`).
- Bổ sung hàm xây dựng TKB riêng cho từng GV:
  - `buildTeacherIndividualTimetableEmail(teacher)`: Trả về `{ to: teacher.email, subject: `Thời khóa biểu - ${teacher.name} (${state.info?.school_year || ''})`, body: ..., html: ... }` chỉ chứa các buổi, thứ, tiết của riêng thầy cô đó.
- Nâng cấp hàm `sendSelectedTeachersTimetableEmail()`:
  - Kiểm tra xem các giáo viên được chọn có email hay không.
  - Cho phép người dùng chọn:
    - Nếu gửi riêng cho từng GV: Gửi danh sách `deliveries` tới `api/baogiang_mail.php`.
    - Nếu GV nào chưa có email, thông báo để người dùng bổ sung email.
  - Giữ tương thích 100% với smoke test hiện có (`tests/timetable-render-smoke.js`).

#### 2. Tại Thẻ "Lịch báo giảng" (`view-baogiang`):
- Tại cụm nút gửi lịch tuần (dòng ~3010):
  - Bổ sung nút:
    ```html
    <button class="btn-small btn-small-primary" onclick="sendBaoGiangSelectedWeekToTeachers()"><i class="fas fa-paper-plane"></i> Gửi lịch tuần cho các GV đã chọn</button>
    ```
- Xây dựng hàm `sendBaoGiangSelectedWeekToTeachers()`:
  - Lấy tuần được chọn từ `#bg-send-week`.
  - Lấy danh sách giáo viên được tích chọn trong `state.bao_giang.recipient_ids`.
  - Lọc các giáo viên có email hợp lệ (`t.email`).
  - Xây dựng lịch báo giảng cá nhân riêng cho từng giáo viên (chỉ chứa các tiết dạy trong tuần của giáo viên đó, không chứa tiết của người khác).
  - Gửi mảng `deliveries` lên `api/baogiang_mail.php`.
  - Hiển thị thông báo toast: *"Đã gửi lịch báo giảng tuần ... thành công cho X giáo viên."*

---

## 4. Kiểm tra và xác minh (Verification Plan)

Coder thực hiện các kiểm tra sau:

1. **Kiểm tra tự động với smoke test**:
   - Cập nhật và chạy `tests/timetable-render-smoke.js`:
     - Kiểm tra hàm `buildTeacherIndividualTimetableEmail` hoặc mở rộng của `sendSelectedTeachersTimetableEmail`.
     - Chạy `node tests/timetable-render-smoke.js`: PASS.
   - Chạy các test liên quan đến phân công / báo giảng:
     - `node tests/baogiang-weekday-segment-smoke.js`: PASS.
     - `node tests/daythay-suggest-smoke.js`: PASS.
     - `node tests/baogiang-recognition-smoke.js`: PASS.
2. **Kiểm tra cú pháp PHP của backend**:
   - `php -l api/baogiang_mail.php`: No syntax errors detected.
   - `php -l api/config.sample.php`: No syntax errors detected.
3. **Ghi chép bàn giao**:
   - Ghi lại toàn bộ nội dung đã sửa và kết quả kiểm thử vào `docs/handoff/IMPLEMENT.md`.

