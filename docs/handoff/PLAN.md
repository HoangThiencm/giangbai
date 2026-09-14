# PLAN: Gỡ bỏ khối toolbar lưới bài học "Mở bài theo lớp" trên lộ trình

## Hiện trạng
- Trong `lotrinh.js`, khối toolbar `#teacherClassPublishToolbar` ("Mở bài theo lớp") hiện đang tự động sinh ra một lưới các card bài học ở đầu khu vực quản lý bài học của giáo viên.
- Khi lộ trình có số lượng bài lớn (50–100 bài), khối này hiển thị tràn ngập màn hình, gây rối mắt và làm phân tán trải nghiệm người dùng.
- Đồng thời, ngay trong form "Thiết kế bài học" bên dưới (`admin-lesson-manager.js`), giáo viên đã có sẵn chức năng chọn mở bài cho tất cả các lớp hoặc tick chọn từng lớp cụ thể (`#lessonClassScopeContainer`) kèm theo nhãn hiển thị trong danh sách chọn bài (`#lessonSelect`). Do đó, khối lưới bài học ở trên là thừa thãi và không cần thiết.

---

## Phạm vi
1. **Gỡ bỏ khối toolbar `#teacherClassPublishToolbar` khỏi `lotrinh.js`:**
   - Xóa bỏ hàm `renderTeacherClassPublishToolbar` và hàm thao tác `toggleTeacherLessonClass`.
   - Gỡ bỏ lệnh gọi `renderTeacherClassPublishToolbar()` tại hàm `render()` (khoảng dòng 1324) và trong các luồng liên quan của `lotrinh.js`.
   - Đảm bảo nếu có element `#teacherClassPublishToolbar` cũ thì được xóa sạch khỏi DOM, không còn render bất kỳ card bài học nào ở đầu trang.
2. **Giữ nguyên cơ chế mở bài theo lớp tại form Thiết kế bài học (`admin-lesson-manager.js`):**
   - Giáo viên tiếp tục quản lý trạng thái mở bài theo từng lớp (6/1, 6/2...) trực tiếp trong form biên tập bài học bên dưới một cách gọn gàng, tập trung.
   - Backend `api/lessons.php` và logic phân quyền truy cập bài học theo lớp của học sinh được giữ nguyên 100%.

---

## Ngoài phạm vi
- Không can thiệp vào backend `api/lessons.php`.
- Không thay đổi giao diện form biên tập bài học trong `admin-lesson-manager.js`.
- Không thay đổi trang quản trị tài khoản `admin.html` (đã nghiệm thu đạt chuẩn).

---

## File dự kiến tác động
- `lotrinh.js`: Gỡ bỏ khối toolbar lưới bài học `teacherClassPublishToolbar` và các hàm liên quan.

---

## Các bước thực hiện
### Bước 1: Dọn dẹp mã nguồn trong `lotrinh.js`
1. Xóa hàm `renderTeacherClassPublishToolbar()` (dòng ~1254 đến 1290).
2. Xóa hàm `toggleTeacherLessonClass()` (dòng ~1232 đến 1253).
3. Xóa lệnh gọi `renderTeacherClassPublishToolbar()` trong hàm `render()` (dòng ~1324).
4. Dọn dẹp các hằng số hoặc tham chiếu không còn sử dụng như `LS_TEACHER_CLASS_FILTER_KEY` nếu chỉ dùng riêng cho toolbar này.
5. Nếu còn thẻ `#teacherClassPublishToolbar` nào đang tồn tại trong cache DOM thì đảm bảo không được tạo lại.

### Bước 2: Kiểm tra cú pháp và tính toàn vẹn
1. Chạy `node --check lotrinh.js` bảo đảm mã nguồn không có lỗi cú pháp.
2. Kiểm tra giao diện lộ trình phía giáo viên để xác nhận khối lưới card đã biến mất hoàn toàn.
3. Kiểm tra form Thiết kế bài học bên dưới để xác nhận việc tick chọn lớp và lưu bài vẫn hoạt động chính xác.

---

## Rủi ro
- **Rủi ro:** Không có rủi ro kỹ thuật vì form Thiết kế bài học (`admin-lesson-manager.js`) hoạt động độc lập và trực tiếp gửi payload `published_classes` lên `api/lessons.php`.

---

## Cách kiểm thử
1. Chạy kiểm tra tĩnh cú pháp: `node --check lotrinh.js`.
2. Đăng nhập tài khoản giáo viên, mở lộ trình (ví dụ `lotrinhtoan6.html`):
   - Xác nhận không còn khối "Mở bài theo lớp" với lưới card bài học ở đầu trang.
   - Xác nhận form "Thiết kế bài học" bên dưới vẫn hiển thị đầy đủ checkbox mở bài theo lớp (`Mở cho tất cả lớp phụ trách` / tick từng lớp).
3. Thử lưu một bài học với lớp 6/1: xác nhận lưu thành công và học sinh lớp 6/1 vào học bình thường.

---

## Tiêu chí nghiệm thu
1. Khối lưới card "Mở bài theo lớp" ở đầu trang lộ trình đã được gỡ bỏ hoàn toàn, không còn gây rối giao diện khi số lượng bài học lớn.
2. Giáo viên vẫn có thể mở hoặc khóa bài theo từng lớp bình thường tại form thiết kế bài học bên dưới.
