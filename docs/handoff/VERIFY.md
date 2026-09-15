# VERIFY: Phân Quyền Bảng Padlet Theo Lớp Học & Tối Ưu Hiển Thị

## Kết luận
PASS

## Đối chiếu Scope & Tính năng
- [x] **Học sinh lớp 9/2 chỉ thấy bảng của lớp 9/2 (và bảng công khai):**
  - Truy vấn `action=manager` cho học sinh chỉ lọc ra bảng có `access_mode = 'public'` hoặc `access_mode = 'class' AND TRIM(target_class) = studentClass`.
  - Không bao giờ trả về bảng của lớp 9/1, 9/3 hay các lớp khác.
- [x] **Chặn học sinh lớp khác truy cập qua link trực tiếp:**
  - `padlet_access()` kiểm tra chặt chẽ và trả mã 403 kèm thông báo chi tiết: *"Bảng này được chia sẻ riêng cho lớp [Tên lớp]. Tài khoản của bạn không thuộc lớp này."*
- [x] **Hiển thị nhãn nhận diện lớp:**
  - Thẻ bảng hiển thị huy hiệu `Lớp [Tên lớp]` rõ ràng trên góc ảnh bìa.
- [x] **Giao diện học sinh tinh gọn:**
  - Tiêu đề "Bảng chia sẻ của lớp", ẩn các khối chọn mẫu tạo bảng, nút "Vào bảng" trực tiếp thay thế các thao tác Sửa/Xóa.
- [x] **Trình sửa bảng của giáo viên:**
  - Bảo toàn chính xác lớp đã chọn trong select `boardClass`.

## Test đã chạy
1. `node tests/padlet-ownership-smoke.js` -> PASS.
2. `node tests/sodiem-smoke.js` -> PASS.
3. `node tests/teacher-permissions-smoke.js` -> PASS.
4. `node tests/security-f12-smoke.js` -> PASS.
5. `git diff --check` -> PASS.

## Bug
Không có.
