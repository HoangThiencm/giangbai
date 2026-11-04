# PLAN: Quản lý Thời khóa biểu theo Tuần/Đợt và Xuất Lịch Báo Giảng / PDF Chuẩn Xác

## Hiện trạng
1. **Lỗi nhân bản TKB tĩnh:** Trong `phancongtochuyenmon.html`, hàm `baoGiangRows(until)` (dòng 3252) lặp qua từng ngày từ ngày bắt đầu năm học đến ngày xem lịch nhưng chỉ đọc từ một bảng `teacher.timetable` tĩnh duy nhất của đợt hiện tại. Hệ thống không lưu lịch sử TKB theo từng tuần hoặc theo từng đợt áp dụng có khoảng ngày hiệu lực.
2. **Hậu quả thực tế:** Dù trường học thay đổi TKB hàng tuần từ tháng 9 đến nay và đã gửi TKB từng tuần cho giáo viên (như thầy Hoàng Tấn Thiên), hệ thống vẫn lấy TKB cũ áp đặt cho tất cả các tuần. Ngày 02/10/2026 (Thứ Sáu) giáo viên không có tiết nhưng khi xuất báo giảng/CSDL vẫn bị ghi nhận 4 tiết Toán cũ.
3. **Thiếu liên kết dữ liệu theo mốc thời gian:** Hệ thống đã có tính năng tạo Đợt (`phases`) có trường `date_start`, `date_end`, nhưng Lịch báo giảng hoàn toàn bỏ qua các mốc này, không tự động chuyển TKB theo ngày thực tế.
4. **Bảng tổng hợp thiếu định danh:** Hàm `baoGiangMonthTable` khi xem ở chế độ "Tất cả giáo viên" không có cột Tên giáo viên, dễ gây hiểu nhầm tiết của đồng nghiệp là tiết của mình.
5. **Chưa có xuất PDF linh hoạt:** Chưa có bộ chọn khoảng thời gian tự do `Từ ngày ... Đến ngày ...` và thiếu CSS `@media print` chuyên biệt cho trang in A4.

## Phạm vi
1. **Kiến trúc dữ liệu TKB theo tuần / đợt hiệu lực:**
   - Bổ sung cấu trúc lưu trữ `weekly_timetables` trong `state` (ví dụ: `state.weekly_timetables[week_key][teacher_id]` hoặc gắn TKB theo đợt có `date_start` -> `date_end`).
   - Tương thích ngược: Nếu tuần nào chưa có TKB riêng, tự động kế thừa TKB của đợt/tuần gần nhất trước đó (hoặc `teacher.timetable` mặc định).
2. **Cập nhật giao diện nhập và quản lý TKB (Tab 2):**
   - Cho phép chọn tuần/đợt áp dụng khi xem, chỉnh sửa, nhận diện AI hoặc nạp TKB.
   - Khi lưu TKB cho một tuần (hoặc khi gửi email TKB tuần), dữ liệu được lưu cố định vào tuần đó trong CSDL, không ghi đè làm hỏng các tuần khác.
3. **Cải tiến logic sinh Lịch báo giảng (`baoGiangRows`):**
   - Với mỗi ngày `date`, tự động xác định tuần tương ứng (`week_key`) hoặc đợt hiệu lực để lấy đúng TKB của giáo viên trong tuần đó từ CSDL.
   - Ngày nào không có tiết trong TKB tuần đó (như ngày 02/10/2026) sẽ tự động sạch tiết, PPCT tự dồn chính xác.
4. **Bộ chọn thời gian & Xuất PDF chuẩn A4:**
   - Bổ sung bộ lọc khoảng thời gian tùy ý: `Từ ngày [dd/mm/yyyy]` đến `Đến ngày [dd/mm/yyyy]` trong Tab 4 (Lịch báo giảng).
   - Thêm nút "Xuất PDF" kèm bộ CSS `@media print` chuẩn trang A4 (khổ ngang/dọc, ẩn navbar, sidebar, thanh nút bấm; giữ nguyên bảng biểu sắc nét, có tiêu đề và chữ ký).
5. **Đồng bộ hiển thị:** Bổ sung cột Tên giáo viên trong bảng chi tiết ngày khi chọn chế độ "Tất cả giáo viên".

## Ngoài phạm vi
- Không can thiệp vào bộ giải thuật toán xếp TKB tự động trong `thoikhoabieu.html` / `thoikhoabieu-engine.js`.
- Không thay đổi các chức năng khác không liên quan (`duyetde.html`, `smartquiz.html`, `sodiem.html`, `KHBD/`, v.v.).

## File dự kiến tác động
- `phancongtochuyenmon.html` (Giao diện chính, state management, logic sinh lịch `baoGiangRows`, bộ lọc thời gian, in ấn/PDF).
- `api/calendar_feed.php` (Đọc đúng TKB theo tuần/đợt cho feed lịch cá nhân).
- `api/phancong.php` (Đảm bảo cấu trúc lưu trữ JSON trong `phancong_chuyenmon.data_json` bảo toàn `weekly_timetables`).

## Các bước thực hiện
1. **Nâng cấp State Schema (`defaultState` & `normalizeState`):**
   - Thêm trường `weekly_timetables: {}` vào state.
   - Đảm bảo khi lưu và tải từ LocalStorage / CSDL MySQL, trường `weekly_timetables` được duy trì nguyên vẹn.
2. **Gắn bộ chọn Tuần vào Tab 2 (Thời khoá biểu GV):**
   - Thêm dropdown/input chọn tuần học cần cập nhật TKB (mặc định là tuần hiện tại hoặc toàn năm học).
   - Khi chỉnh sửa hoặc AI nhận diện TKB cho tuần $W$, lưu vào `state.weekly_timetables[W][teacher_id]`.
3. **Cải tiến hàm `baoGiangRows(until)` trong `phancongtochuyenmon.html`:**
   - Thay vì luôn đọc `teacher.timetable` cố định, hàm sẽ gọi `getTeacherTimetableForDate(teacher, date)`:
     - Kiểm tra `state.weekly_timetables[week_key]?.[teacher.id]`.
     - Nếu không có, kiểm tra TKB của Phase tương ứng với ngày `date`.
     - Nếu vẫn không có, fallback về `teacher.timetable`.
   - Lọc chính xác các tiết theo đúng TKB có hiệu lực tại ngày đó.
4. **Thêm bộ lọc khoảng ngày tự do trong Tab 4 (Lịch báo giảng):**
   - Thêm 2 trường `Từ ngày` (`bg-date-from`) và `Đến ngày` (`bg-date-to`).
   - Cập nhật hàm `renderBaoGiangView()` để lọc các dòng trong khoảng ngày này thay vì chỉ gò bó theo tháng.
5. **Tối ưu bảng biểu & Xây dựng bản in PDF (`@media print`):**
   - Thêm cột `Giáo viên` vào `baoGiangMonthTable` khi xem "Tất cả giáo viên".
   - Thêm nút "Xuất PDF / In báo giảng" mở hộp thoại in với CSS `@media print` chuyên biệt:
     - Ẩn `#top-navbar`, `#left-panel`, `#tt-left-panel`, thanh công cụ, nút bấm.
     - Căn lề khổ A4, nền trắng, kẻ viền nét mảnh chuẩn văn bản sư phạm.
6. **Kiểm thử hồi quy:**
   - Kiểm tra ngày 02/10/2026: Đảm bảo không xuất hiện 4 tiết Toán cũ.
   - Kiểm tra các tuần khác: Đảm bảo mỗi tuần hiển thị đúng TKB riêng của tuần đó.

## Rủi ro
1. **Tương thích ngược dữ liệu cũ:** Các bản ghi cũ trong CSDL chưa có `weekly_timetables` có thể bị rỗng ➔ Giải pháp: Cơ chế Fallback nhiều tầng (Tuần ➔ Đợt ➔ TKB mặc định).
2. **Lệch mốc tuần (ISO week vs Tuần trường học):** Tuần học có thể bắt đầu từ Thứ Hai nhưng ngày khai giảng/áp dụng rơi vào giữa tuần ➔ Giải pháp: Dùng hàm `baoGiangWeekRange` đồng nhất với `bg-start-date` (Tuần 1).

## Cách kiểm thử
1. **Kiểm thử logic ngày 02/10/2026:**
   - Cài đặt TKB tuần 4 (chứa ngày 02/10) không có tiết Thứ 6 cho thầy Hoàng Tấn Thiên / Hoàng Tấn.
   - Chạy hàm xuất báo giảng: Ngày 02/10/2026 phải hiển thị trống/không có tiết.
2. **Kiểm thử đa tuần:**
   - Tuần 3 có tiết Thứ 6, Tuần 4 không có tiết Thứ 6.
   - Xuất dữ liệu tháng 10: Tuần 3 có tiết, Tuần 4 không có tiết.
3. **Kiểm thử xuất PDF:**
   - Chọn khoảng ngày từ `2026-10-01` đến `2026-10-15`.
   - Bấm nút Xuất PDF / In: Bản in hiển thị đúng 15 ngày, trang in vừa vặn, không bị tràn lề, không xuất hiện nút bấm hay thanh điều hướng.

## Tiêu chí nghiệm thu
- Không còn tình trạng lấy 1 TKB mẫu áp đặt mù quáng cho mọi tuần trong năm.
- Hệ thống tự động đọc đúng TKB của từng tuần từ CSDL khi xuất Báo giảng / Lịch dạy.
- Ngày 02/10/2026 và các ngày nghỉ thực tế không còn bị chèn tiết sai.
- Người dùng không phải xóa tay hay thêm ngoại lệ thủ công mỗi tuần.
- Xuất được PDF / In chuẩn A4 theo khoảng thời gian tùy chọn.
