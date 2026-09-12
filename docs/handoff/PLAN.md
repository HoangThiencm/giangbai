# PLAN

## Hiện trạng

### 1. Vấn đề 1: Cảnh báo lệch tiết TKB và PPCT ("Tuần 1 – Toán lớp 71: TKB có 8 tiết, PPCT xác định 4 tiết...")
- **Bản chất cảnh báo**:
  - Hệ thống đối chiếu số tiết giữa Thời khóa biểu (TKB) và Phân phối chương trình (PPCT).
  - TKB xếp 8 tiết trong khi PPCT tuần 1 chỉ có 4 tiết, dẫn đến chênh lệch 4 tiết không có bài dạy ghép vào (bị gắn nhãn "PPCT tuần này chưa đủ tiết").
- **Nguyên nhân cốt lõi**:
  1. **1 lớp có 2 người cùng dạy**: Có trường hợp 2 giáo viên cùng có TKB dạy môn Toán cho lớp 71 (ví dụ Thầy A dạy 4 tiết, Cô B dạy 4 tiết). Hiện tại hệ thống gom chung tất cả GV vào một giỏ `coverage` của lớp mà chưa kiểm tra/cảnh báo hiện tượng 2 GV cùng dạy.
  2. **TKB học cả sáng và chiều**: Lớp học chính khóa buổi sáng 4 tiết và học tăng cường/phụ đạo buổi chiều 4 tiết.
  3. **Tuần đã qua trong quá khứ vẫn bị tính dồn**: Hàm `baoGiangRows(until)` luôn duyệt từ ngày bắt đầu năm học `start_date` đến ngày xem. Dù người dùng đang xem các tuần sau thì cảnh báo của các tuần đã qua trong quá khứ (như Tuần 1) vẫn liên tục bị tính lại và treo cảnh báo trên màn hình cũng như chặn gửi email.
  4. **Cơ chế chặn cứng email**: Hàm `buildBaoGiangSelfEmail` dùng chung `warningDetails` của toàn trường để chặn giáo viên (`throw new Error`), khiến giáo viên không thể gửi email báo giảng cá nhân.

### 2. Vấn đề 2: Thể hiện bài dạy đa tuần (Ví dụ: Bài 11 học ở 3 tuần: Tuần 4, 5, 6)
- **Yêu cầu thực tế**:
  Khi một bài học (ví dụ: *Bài 11. Tỉ số lượng giác của góc nhọn*) được dạy kéo dài qua 3 tuần (mỗi tuần 1 tiết), phải thể hiện rõ ràng và đầy đủ:
  - Tuần 4: `Tuần 4  Bài 11. Tỉ số lượng giác của góc nhọn (tiết ppct: ví dụ tiết 6) 1/3`
  - Tuần 5: `Tuần 5  Bài 11. Tỉ số lượng giác của góc nhọn (tiết ppct ví dụ tiết 7) 2/3`
  - Tuần 6: `Tuần 6  Bài 11. Tỉ số lượng giác của góc nhọn (tiết ppct ví dụ tiết 8) 3/3`
- **Tồn tại hiện nay**:
  - Thuật toán `parseBaoGiangCurriculum()` hiện phụ thuộc vào khối liền kề của Mạch (`strand`). Nếu không có Mạch hoặc giữa các tuần có bài khác xen vào thì bài học bị cắt nhỏ thành các khối độc lập `1/1, 1/1, 1/1`.
  - Định dạng hiển thị trên bảng Web và nội dung Email chưa thống nhất cú pháp đầy đủ: `Tuần X  Tên bài (tiết ppct: Y) A/B`.

### 3. Vấn đề 3: Gửi Thời khóa biểu các giáo viên được tick chọn qua email cá nhân
- **Yêu cầu thực tế**:
  - Trong tab "2. Thời khoá biểu GV", cho phép người dùng **tick chọn (checkbox)** các giáo viên cần xem (có tùy chọn chọn tất cả / bỏ chọn).
  - Có nút bấm gửi TKB của **toàn bộ các giáo viên được tick chọn** về email cá nhân (tài khoản đang đăng nhập).
  - Định dạng email:
    + Phân tách rõ ràng từng giáo viên (mỗi giáo viên là một bảng TKB trực quan độc lập gồm Buổi sáng, Buổi chiều, Thứ 2 đến Thứ 7, Tiết, Môn, Lớp).
    + **Chỉ chứa Thời khóa biểu, hoàn toàn không có lịch báo giảng hay PPCT**, giúp người nhận mở email ra là tra cứu được ngay TKB của các GV cần xem.
- **Hiện trạng code**:
  - Đã có sẵn backend gửi mail SMTP qua `api/baogiang_mail.php`.
  - Cột danh sách giáo viên bên trái (`#tt-teacher-list`) hiện chưa có checkbox chọn nhiều GV và chưa có hàm gom TKB nhiều giáo viên thành mẫu HTML email gửi đi.

---

## Phạm vi

1. **Xử lý cảnh báo lệch tiết và phát hiện 1 lớp 2 người dạy**:
   - **Bỏ qua tuần đã qua**: Chỉ tính và cảnh báo cho tuần đang xem / tuần hiện tại trở đi. Các tuần đã qua trong quá khứ tuyệt đối không cảnh báo và không tính vào lỗi chặn gửi email.
   - **Phát hiện và cảnh báo "1 lớp 2 người cùng dạy"**: Trong mỗi tuần/lớp/môn, theo dõi danh sách các giáo viên có tiết TKB. Nếu phát hiện từ 2 giáo viên trở lên cùng dạy môn đó cho lớp đó, hiển thị cảnh báo chi tiết nêu rõ tên các giáo viên cùng dạy (ví dụ: `Tuần 1 – Toán lớp 71: Có 2 giáo viên cùng dạy gồm Thầy A, Cô B (TKB có tổng cộng 8 tiết)`).
   - **Phạm vi gửi email cá nhân**: Chỉ kiểm tra đối chiếu TKB đối với các lớp do chính giáo viên đang đăng nhập giảng dạy; không lấy dữ liệu toàn trường để chặn giáo viên.
   - **Bỏ chặn cứng**: Đổi cơ chế `throw new Error` thành thông báo nhắc nhở / hộp thoại xác nhận cho phép người dùng vẫn tiếp tục gửi email nếu muốn.
2. **Cải tiến thuật toán phân đoạn PPCT đa tuần liên tục**:
   - Hỗ trợ đầy đủ bài học trải dài qua 3 tuần trở lên (như Bài 11 học ở Tuần 4, Tuần 5, Tuần 6; mỗi tuần 1 tiết -> phân đoạn lũy kế chuẩn xác `1/3, 2/3, 3/3`).
   - Gom cụm thông minh dựa trên tên bài học đã chuẩn hóa (`normalizeBaoGiangLessonTitle`) qua các tuần kế tiếp nhau.
   - Chuẩn hóa định dạng hiển thị: `Tuần [X]  [Tên bài dạy] (tiết ppct: [Y]) [A/B]`.
3. **Tính năng tick chọn nhiều giáo viên và gửi TKB qua email cá nhân**:
   - Thêm ô checkbox cho từng giáo viên trong danh sách giáo viên của tab Thời khóa biểu (`#tt-teacher-list`).
   - Thêm nút tiện ích: `Chọn tất cả GV có TKB`, `Bỏ chọn`, hiển thị số lượng GV đang được chọn.
   - Thêm nút hành động: **"Gửi TKB các GV đã chọn qua email"** tại thanh công cụ hoặc phía trên danh sách GV.
   - Xây dựng hàm `buildSelectedTeachersTimetableEmail(teacherIds)`:
     + Duyệt qua danh sách giáo viên được tick chọn.
     + Tạo nội dung HTML chứa các bảng TKB tách biệt từng giáo viên, trình bày dạng thẻ card sang trọng, rõ ràng từng buổi (sáng/chiều) và từng thứ trong tuần.
     + Tiêu đề email rõ nghĩa: `Thời khóa biểu [X] giáo viên - [Năm học] [Học kỳ]`.
     + Hoàn toàn không chứa lịch báo giảng hay PPCT.
     + Gửi về email của tài khoản đang đăng nhập thông qua `api/baogiang_mail.php`.

---

## Ngoài phạm vi

- Không thay đổi cấu trúc lưu trữ LocalStorage cốt lõi để giữ tương thích ngược toàn diện.
- Không can thiệp vào các module Phân công chuyên môn, Quản lý chấm công, Dạy thay.

---

## File dự kiến tác động

1. `phancongtochuyenmon.html`:
   - `parseBaoGiangCurriculum(text)`: Gom bài học liên tục qua nhiều tuần (từ 3 tuần trở lên) và tính lũy kế phân đoạn `1/n, 2/n, ..., n/n`.
   - `decorateBaoGiangRows(until)`:
     + Lọc bỏ các tuần đã qua (`week < activeWeek`), không đưa vào cảnh báo.
     + Bổ sung cảnh báo phát hiện 1 lớp 2 người cùng dạy.
   - `buildBaoGiangSelfEmail()` & `composeBaoGiangEmail()`: Bỏ chặn cứng, chuẩn hóa hiển thị `Tuần X  Bài dạy (tiết ppct: Y) A/B`.
   - `renderTimetableTeacherList()`: Bổ sung checkbox tick chọn giáo viên, nút chọn tất cả / bỏ chọn.
   - `buildSelectedTeachersTimetableEmail(teacherIds)`: Dựng mẫu email HTML chứa bảng TKB phân tách từng giáo viên được chọn.
   - `sendSelectedTeachersTimetableEmail()`: Gửi TKB của các GV được tick chọn về email cá nhân.
2. `tests/baogiang-weekday-segment-smoke.js`:
   - Bổ sung test case kiểm tra bài học 3 tuần liên tiếp (Tuần 4 tiết 6, Tuần 5 tiết 7, Tuần 6 tiết 8) -> `1/3, 2/3, 3/3`.
   - Kiểm tra bộ lọc tuần đã qua và cảnh báo 1 lớp 2 giáo viên cùng dạy.
3. `tests/timetable-render-smoke.js`:
   - Bổ sung test case kiểm tra tính năng tick chọn nhiều giáo viên và hàm sinh mã HTML email TKB đa giáo viên `buildSelectedTeachersTimetableEmail`.

---

## Các bước thực hiện

### Bước 1: Nâng cấp thuật toán PPCT đa tuần trong `parseBaoGiangCurriculum`
- Duyệt qua các dòng PPCT theo trình tự tuần, gom các tiết của cùng một bài học (sau khi chuẩn hóa tiêu đề) thuộc các tuần liên tiếp thành một khối bài học duy nhất.
- Gán phân đoạn lũy kế: Tuần 4 tiết 6 là `1/3`, Tuần 5 tiết 7 là `2/3`, Tuần 6 tiết 8 là `3/3`.

### Bước 2: Cập nhật logic cảnh báo TKB - PPCT trong `decorateBaoGiangRows`
1. **Bỏ qua tuần đã qua**: Xác định tuần đang chọn xem (`activeWeek`). Những tuần `week < activeWeek` không đưa vào danh sách cảnh báo `warnings`.
2. **Phát hiện 1 lớp 2 người cùng dạy**:
   - Thu thập `teachers = new Set()` cho từng cặp `Lớp | Môn | Tuần`.
   - Nếu `teachers.size > 1`: Thêm cảnh báo rõ ràng:
     `Tuần ${week} – ${subject} lớp ${className}: Phát hiện ${teachers.size} giáo viên cùng có TKB gồm ${[...teachers].join(', ')} (${slots} tiết).`

### Bước 3: Chuẩn hóa hiển thị lịch báo giảng
- Định dạng bài dạy trên Web và trong Email: `Tuần [X]  [Tên bài] (tiết ppct: [Y]) [A/B]`.
- Bỏ chặn cứng trong `buildBaoGiangSelfEmail`.

### Bước 4: Triển khai tính năng gửi Thời khóa biểu các GV được tick chọn qua email
1. **Quản lý danh sách GV được tick chọn**:
   - Khởi tạo `selectedTimetableTeacherIds = new Set()`.
   - Trong `renderTimetableTeacherList()`: Thêm checkbox trước tên mỗi giáo viên.
   - Thêm nút "Chọn tất cả GV có TKB" và "Bỏ chọn" trên danh sách giáo viên.
2. **Xây dựng nội dung Email TKB đa giáo viên (`buildSelectedTeachersTimetableEmail`)**:
   - Lọc danh sách các giáo viên có trong `selectedTimetableTeacherIds`.
   - Mỗi giáo viên được render một khối riêng biệt:
     + Card header: Tên giáo viên, vai trò, số tiết TKB.
     + Bảng Buổi sáng: Thứ 2 – Thứ 7, Tiết 1 – 5, Môn và Lớp.
     + Bảng Buổi chiều: Thứ 2 – Thứ 7, Tiết 1 – 4, Môn và Lớp.
     + Đường phân cách rõ ràng giữa các giáo viên.
     + Tuyệt đối không có lịch báo giảng hay PPCT.
3. **Thao tác gửi Email (`sendSelectedTeachersTimetableEmail`)**:
   - Gửi payload `{ subject, body, html }` tới `api/baogiang_mail.php`.
   - Hiển thị toast thông báo kết quả.

### Bước 5: Viết test tự động và nghiệm thu
- Chạy test kiểm tra phân đoạn đa tuần, lọc tuần cũ, cảnh báo 2 GV cùng dạy, và kiểm tra render HTML email TKB cho nhiều giáo viên được tick chọn.

---

## Rủi ro

- **Email chứa nhiều giáo viên có dung lượng lớn**: Nếu người dùng chọn 20-30 giáo viên cùng lúc, nội dung HTML có thể vượt quá giới hạn hoặc bị Gmail cắt bớt (clipped).
  - *Kiểm soát*: Tối ưu mã HTML gọn gàng, dùng inline CSS tối giản; có cảnh báo nếu người dùng chọn quá 15 giáo viên một lần gửi.

---

## Cách kiểm thử

1. **Kiểm thử tự động bằng script**:
   - Chạy `tests/baogiang-weekday-segment-smoke.js` và `tests/timetable-render-smoke.js`.
   - Xác nhận:
     + Phân đoạn Bài 11 đạt `1/3, 2/3, 3/3`.
     + Cảnh báo lọc đúng tuần cũ và phát hiện lớp có 2 GV.
     + Hàm `buildSelectedTeachersTimetableEmail` trả về HTML hợp lệ chứa đầy đủ các giáo viên được tick chọn.
2. **Kiểm thử giao diện**:
   - Tick chọn 2-3 giáo viên trong danh sách TKB.
   - Bấm "Gửi TKB các GV đã chọn qua email".
   - Kiểm tra email nhận được: hiển thị lần lượt TKB của từng giáo viên được chọn, bố cục chuẩn đẹp, không có lịch báo giảng.

---

## Tiêu chí nghiệm thu

1. **Tuần đã qua không còn cảnh báo**: Các tuần cũ không còn gây báo động giả.
2. **Cảnh báo rõ 1 lớp 2 người cùng dạy**: Nêu rõ tên các GV cùng có TKB.
3. **Bài học đa tuần hiển thị đúng**: `Tuần 4  Bài 11... (tiết ppct: 6) 1/3`, `Tuần 5 ... 2/3`, `Tuần 6 ... 3/3`.
4. **Tick chọn và gửi TKB các GV qua email**:
   - Có ô checkbox tick chọn từng GV hoặc chọn tất cả.
   - Gửi TKB của toàn bộ các GV được tick chọn về email cá nhân thành công.
   - Email phân tách từng giáo viên rõ ràng, hiển thị trực quan dạng lưới TKB, không có lịch báo giảng.
5. **Bộ test tự động**: Đạt **PASS 100%**.
