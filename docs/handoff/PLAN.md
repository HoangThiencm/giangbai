# Kế hoạch Triển khai: Tối ưu Trải nghiệm Không cần Đăng nhập cho Đường link Khảo sát Nộp bài (nopbai.html)

## Hiện trạng & Phân tích Nguyên nhân
- **Khảo sát thực tế đường link người dùng cung cấp (`https://www.hoangthiencm.id.vn/nopbai.html?code=E6N2XG3F`):**
  + Đây là đợt nộp thuộc loại **Báo cáo biểu mẫu** (`submission_type = 'report'`) phục vụ khảo sát/nhập liệu qua Google Sheets:
    * Tiêu đề: *"Danh sách học sinh tham gia VioEdu năm học 2026-2027"*.
    * Mô tả: *"Thầy cô nhấn vào link chọn đúng tên của mình và nhập danh sách học sinh của lớp mình phụ trách có học sinh tham gia"*.
    * Chế độ nạp đối tượng: `access_mode = 'school_list'` (danh sách dùng chung Tổ Toán Tin gồm 10 giáo viên).
    * Trường khảo sát: Đường link Google Sheets ngoài (`https://docs.google.com/spreadsheets/d/1KUq6PFNT3LYDyO9H0NTWEJxJL2_0odJJ/edit?...`).
- **Phân tích kỹ thuật hệ thống:**
  + Về mặt backend API: Cả `GET api/submissions.php?action=public` và `POST api/submissions.php?action=submit` đều **hoàn toàn là API công khai**, không đòi hỏi token xác thực (`authToken`), không yêu cầu session người dùng đăng nhập.
  + Trang `nopbai.html` không nạp `access-control.js` và không có cơ chế chặn đăng nhập.
- **Nguyên nhân gốc rễ khiến giáo viên/người dùng phản ánh hoặc nhầm lẫn "cần đăng nhập":**
  1. **Nạp nhầm route guard `access-control.js`:** Trước đó `nopbai.html` bị nhúng thẻ `<script src="access-control.js"></script>` và khai báo trong `pageKeys` của `access-control.js`, khiến bất kỳ ai mở link nộp bài mà chưa có `authToken` giáo viên đều bị đá về `login.html`.
  2. **Cái bẫy chuyển hướng ở Logo Header:** Thẻ tiêu đề ở đầu trang `nopbai.html` từng đặt `<a href="index.html">`. Khi người dùng bấm vào logo hoặc dòng chữ "HỆ THỐNG NỘP DỮ LIỆU", trình duyệt chuyển sang `index.html` và tự động `location.replace('login.html')`.
  3. **Giao diện xác nhận tạo cảm giác như form Login/Xác thực tài khoản:**
     - Khối `<section id="accessSection">` với tiêu đề "Xác nhận người nộp bài" chưa có nhãn thông báo rõ ràng khẳng định: *"Không cần tài khoản hay mật khẩu hệ thống"*, dẫn đến việc giáo viên lầm tưởng phải có tài khoản/mật khẩu.

## Phạm vi
1. **Trang tiếp nhận nộp bài `nopbai.html`:**
   - Xóa bỏ hoàn toàn `<script src="access-control.js"></script>` khỏi `nopbai.html`.
   - Khắc phục nguy cơ chuyển hướng đăng nhập ngoài ý muốn: Đổi thẻ link logo header `<a href="index.html">` thành liên kết an toàn nội bộ (`nopbai.html` hoặc `href=""`), không dẫn người nộp bài về `index.html` hay `login.html`.
   - Bổ sung Huy hiệu / Thông báo nổi bật ngay đầu trang và trong khối xác nhận:
     * Badge rõ ràng: `✓ Không cần đăng nhập`.
     * Dòng hướng dẫn: *"Đường link mở công khai — Thầy/cô và các bạn không cần tài khoản hay mật khẩu đăng nhập. Chỉ cần chọn đúng họ và tên để hệ thống ghi nhận."*
   - Cải tiến giao diện khối `accessSection`: Làm nổi bật thanh tìm kiếm và hộp chọn tên giáo viên/người nộp; thu gọn mục nhập mã cá nhân thủ công thành tùy chọn phụ.
2. **Hệ thống phân quyền `access-control.js`:**
   - Xóa `'nopbai.html': 'nopbai'` khỏi `pageKeys` trong `access-control.js` để route guard không can thiệp vào link nộp bài công khai. (Giữ `'nopbai-quanly.html': 'nopbai'` cho trang quản trị của giáo viên).
3. **Trang quản trị `nopbai-quanly.html`:**
   - Cập nhật thông báo sau khi sao chép link chung và link cá nhân, phân biệt rõ link công khai tự chọn tên và link cá nhân mở sẵn tên.
4. **Kiểm thử tự động (Smoke tests):**
   - Bổ sung các kiểm tra tĩnh trong `tests/nopbai-report-link-smoke.js` nhằm đảm bảo:
     * `nopbai.html` không chứa liên kết trỏ sang `index.html` hoặc `login.html`.
     * `nopbai.html` không nạp `access-control.js`.
     * `nopbai.html` có chứa thông điệp rõ ràng khẳng định không cần đăng nhập tài khoản.
     * Quy trình chọn người nộp và nộp bài biểu mẫu khảo sát vẫn hoạt động chính xác.

## Tiêu chí nghiệm thu
1. Truy cập `nopbai.html?code=E6N2XG3F` (ở cả chế độ ẩn danh không có tài khoản):
   - Không bị `access-control.js` chặn chuyển hướng sang `login.html`.
   - Bấm vào logo/header trang không bị văng sang `login.html`.
   - Giao diện có thông báo nổi bật khẳng định không cần đăng nhập tài khoản hay mật khẩu.
   - Thao tác tìm kiếm, chọn tên trong danh sách Tổ Toán Tin và bấm nút tiếp tục diễn ra mượt mà, trực tiếp mở link khảo sát Google Sheets và ghi nhận hoàn thành.
2. Toàn bộ smoke test tự động `tests/nopbai-report-link-smoke.js` và `tests/teacher-permissions-smoke.js` đạt PASS 100%.
