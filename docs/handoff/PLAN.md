# PLAN: Phân Quyền Bảng Padlet Theo Lớp Học & Tối Ưu Hiển Thị Cho Học Sinh

## 1. Bối cảnh & Yêu cầu
- Giáo viên muốn chia sẻ bảng Padlet riêng cho từng lớp (ví dụ lớp 9/2).
- Học sinh thuộc lớp 9/2 khi đăng nhập chỉ thấy các bảng của lớp 9/2 (và bảng công khai).
- Học sinh lớp khác (9/1, 9/3,...) không được nhìn thấy bảng của lớp 9/2 trong danh sách và bị chặn nếu truy cập trái phép.
- Giao diện Padlet cần trực quan: hiển thị nhãn lớp trên thẻ bảng, và giao diện tinh gọn dành riêng cho học sinh.

## 2. Giải pháp Kỹ thuật
1. **Backend (`api/padlet.php`)**:
   - `action === 'manager'`:
     - Nếu là giáo viên / admin: giữ nguyên truy vấn toàn bộ bảng do giáo viên quản lý.
     - Nếu là học sinh: truy vấn có điều kiện `status = 'open' AND ((access_mode = 'class' AND TRIM(target_class) = studentClass) OR access_mode = 'public')`. Không trả về dữ liệu các bảng của lớp khác.
   - `padlet_access()`: Kiểm tra quyền truy cập chi tiết khi vào xem/đăng bài, chặn và thông báo rõ ràng nếu học sinh không thuộc lớp được gán.
2. **Frontend (`padlet_ht.html`)**:
   - `loadManager()`: Đọc `is_teacher` và `student_class` từ phản hồi API.
   - `renderLibrary()`:
     - Thêm nhãn `Lớp [Tên Lớp]` trên thẻ bảng khi bảng được cấu hình `access_mode === 'class'`.
     - Với học sinh: hiển thị nút "Vào bảng" thay cho các nút Sửa/Xóa của giáo viên.
   - `renderManager()`:
     - Với học sinh: hiển thị tiêu đề thân thiện "Bảng chia sẻ của lớp", ẩn các thư viện mẫu tạo bảng.
   - `openBoardEditor()`: Bảo toàn giá trị lớp đã chọn ngay cả khi danh sách lớp trả về có độ trễ hoặc thiếu.

## 3. Tiêu chí Nghiệm thu
- [x] Học sinh lớp 9/2 chỉ thấy bảng của lớp 9/2 hoặc bảng công khai.
- [x] Thẻ bảng có nhãn nhận diện lớp rõ ràng.
- [x] Giao diện học sinh tinh gọn, chỉ có danh sách bảng và nút "Vào bảng".
- [x] Giáo viên chỉnh sửa bảng giữ nguyên lớp đã lưu.
- [x] Toàn bộ test `padlet-ownership-smoke.js`, `sodiem-smoke.js`, `teacher-permissions-smoke.js` đạt PASS.
