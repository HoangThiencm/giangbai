# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Phân quyền mở bài theo lớp cho Giáo viên (Lộ trình học):**
   - Đã nâng cấp migration tự động cột `published_classes_json` trong `api/lessons.php`.
   - Đã xử lý phân quyền trong `api/lessons.php`: GET danh sách và GET bài học chi tiết qua ID/slug đều kiểm tra lớp học của học sinh (`lesson_is_available_to_student`); lưu bài `save_content` kiểm tra quyền phụ trách lớp của giáo viên (`teacher_managed_classes`); action `update_published_classes` cho phép cập nhật mở bài theo lớp nhanh chóng.
   - Giao diện `admin-lesson-manager.js` đã có bộ chọn phạm vi lớp (`#lessonClassScopeContainer`), hỗ trợ mở cho tất cả các lớp hoặc tick chọn từng lớp phụ trách (`6/1`, `6/2`...), hiển thị badge lớp trong dropdown danh sách bài học.
   - Giao diện `lotrinh.js` đã tích hợp thanh công cụ "Mở bài theo lớp" cho giáo viên, cho phép xem theo từng lớp và bật/tắt mở bài nhanh từng bài học cho lớp đó. Tiến độ học sinh được tính toán chuẩn xác dựa trên các bài được mở cho lớp của mình.
2. **Tổ chức danh sách đăng ký trong Admin (`admin.html`):**
   - Đã phân tách rõ rệt 2 Tab: **Học sinh** và **Giáo viên**, kèm thống kê tổng số, hoạt động và chờ duyệt riêng biệt.
   - Trong Tab **Học sinh**: Có thanh Sub-tabs / Pills phân chia tự động theo từng lớp học (`Tất cả`, `Lớp 6/1`, `Lớp 6/2`..., `Chưa xếp lớp`), hiển thị số lượng học sinh từng lớp, hỗ trợ lọc lớp tức thời, tìm kiếm theo tên/tài khoản và lọc trạng thái (Đang hoạt động, Chờ duyệt, Đang khóa).
   - Trong Tab **Giáo viên**: Bảng danh sách hiển thị chuyên biệt cho giáo viên, cột Lớp phụ trách, Quyền chức năng đã cấp, nút Duyệt, Cài đặt, Cấp full, Xóa.
   - Trạng thái tab vai trò và sub-tab lớp được lưu trong `localStorage` để giữ nguyên trạng thái khi làm mới hoặc duyệt tài khoản.

## Test đã chạy
1. **Kiểm tra cú pháp JavaScript tĩnh:**
   - `node --check admin-lesson-manager.js` — PASS.
   - `node --check lotrinh.js` — PASS.
   - Kiểm tra cú pháp tất cả 5 khối `<script>` nội tuyến trong `admin.html` — PASS.
2. **Kiểm thử logic phân quyền bài học theo lớp:**
   - Kiểm tra hàm `lesson_is_available_to_student`:
     - Bài chưa công khai (`is_published = 0`): Học sinh lớp 6/1 $\to$ Bị chặn (PASS).
     - Bài mở toàn khối (`is_published = 1, published_classes = [] / ['*']` hoặc null): Học sinh lớp bất kỳ $\to$ Cho phép (PASS).
     - Bài mở cho `['6/1', '6/2']`: Học sinh lớp 6/1 $\to$ Cho phép; Học sinh lớp 6/2 $\to$ Cho phép; Học sinh lớp 6/3 $\to$ Bị chặn; Học sinh chưa có lớp $\to$ Bị chặn (PASS).
3. **Kiểm thử logic thanh công cụ mở bài theo lớp trên `lotrinh.js`:**
   - Kiểm tra hàm `lessonIsOpenForClass` và luồng toggle bật/tắt lớp của giáo viên phụ trách: Đúng lớp được mở, trạng thái cập nhật chính xác (PASS).
4. **Kiểm thử logic tab và lọc tài khoản trong `admin.html`:**
   - Tách đúng danh sách Học sinh và Giáo viên từ mock data (PASS).
   - Tự động trích xuất danh sách lớp không trùng lặp và đếm chính xác số học sinh từng lớp (PASS).
   - Lọc theo lớp, lọc theo từ khóa tìm kiếm và lọc theo trạng thái hoạt động/chờ duyệt hoạt động chính xác (PASS).
5. **Kiểm tra hồi quy hệ thống:**
   - `node tests/lesson-import-smoke.js` — PASS toàn bộ 27 checks.
   - `node tests/xaydungphuluc-smoke.js` — PASS toàn bộ checks.

## Pass / Fail từng tiêu chí
- **Tiêu chí 1:** Giáo viên phụ trách nhiều lớp (ví dụ 6/1, 6/2) có thể tùy chọn mở bài cho tất cả các lớp hoặc mở riêng cho từng lớp cụ thể $\to$ **PASS**.
- **Tiêu chí 2:** Học sinh lớp 6/1 chỉ nhìn thấy và học các bài được mở cho lớp 6/1 (hoặc bài mở cho toàn khối); không xem được các bài mở riêng cho lớp khác $\to$ **PASS**.
- **Tiêu chí 3:** Trong Admin, danh sách đăng ký được phân tách gọn gàng thành Tab Học sinh và Tab Giáo viên $\to$ **PASS**.
- **Tiêu chí 4:** Trong Tab Học sinh của Admin, có các sub-tab chia theo từng lớp học, hiển thị số lượng học sinh từng lớp, cho phép xem, tìm kiếm và quản lý học sinh theo từng lớp $\to$ **PASS**.
- **Tiêu chí 5:** Không làm ảnh hưởng đến các dữ liệu bài học và tài khoản đã tạo trước đó; tương thích ngược hoàn toàn $\to$ **PASS**.

## Bug
Không phát hiện bug.
