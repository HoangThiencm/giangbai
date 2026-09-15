# IMPLEMENT

## Phạm vi đã triển khai
1. **Phóng to Đề Bài trong Trình Chiếu (Presentation View):**
   - Mở rộng vùng hiển thị `#presentationContent` toàn diện (`w-full`, giảm padding dư thừa từ 96px xuống `p-2 sm:p-4`).
   - Đặt kích thước ảnh đề bài tự động mở rộng bao quát màn hình chiếu: `width: min(94vw, 1200px); max-height: 80vh; min-height: 300px; object-contain` trên thẻ trượt nền trắng bo góc `rounded-2xl shadow-2xl bg-white p-3 sm:p-6`.
   - Bổ sung biến tỉ lệ `presentationImageScale` và nút điều khiển:
     + `A-`: Thu nhỏ cả chữ và ảnh đề bài (bước 15%).
     + `100%`: Đặt lại cỡ chuẩn tức thì.
     + `A+`: Phóng to cả chữ và ảnh đề bài (lên tới 300%).
     + Phím tắt bàn phím: `+`/`=` để phóng to, `-`/`_` để thu nhỏ, `0` để reset về 100%, `ArrowLeft`/`ArrowRight` chuyển câu, `Space` dừng/bật đồng hồ, `Esc` thoát trình chiếu.
2. **Dán ảnh đề bài siêu tốc:**
   - Nút **Dán ảnh (Ctrl+V)** đọc ảnh trực tiếp từ clipboard (`navigator.clipboard.read()`).
   - Lắng nghe `paste` toàn cục (`window.addEventListener('paste', handleGlobalPaste)`): Chụp màn hình xong bấm `Ctrl + V` ở bất kỳ đâu trên trang đều nhận ảnh tức thì, hiển thị ngay lên khung xem trước và sẵn sàng trình chiếu.
   - Bổ sung Toast thông báo thành công.
3. **Khắc phục triệt để danh sách học sinh & điểm số từ CSDL:**
   - `api/sodiem.php`:
     + `sodiem_teacher`: Chấp nhận cả `teacher` và `admin`.
     + `action === 'classes'`: Trả về danh sách lớp từ bảng `users` (`WHERE role = 'student' AND is_active = 1`) và bảng `gradebooks`.
     + `action === 'load'`: Trả về `gradebook` (có fallback theo `class_name` & `subject`) và luôn kèm `roster` chính thức từ `users`.
   - `sodiem.html`:
     + Gắn `onchange="onClassChange()"` trên `<select id="classSelect">` và `onchange="loadBook()"` trên `#subject`.
     + Nhớ lớp gần nhất bằng `sodiem:last_class`.
     + `init()` nạp lớp đa tầng và tự động gọi `loadBook()` ngay khi mở trang.
     + Thuật toán **Safe Score Merge**: Gộp học sinh từ `roster`, `gradebook` và `localStorage`, giữ nguyên 100% điểm số đã chấm, không bao giờ bị xóa trắng.
     + `persist()` chống ghi đè dữ liệu khi chưa chọn lớp.

## Kiểm tra
- `node tests/sodiem-smoke.js`: PASS.
- `node tests/teacher-permissions-smoke.js`: PASS.
- `node tests/security-f12-smoke.js`: PASS.
- `git diff --check`: PASS.
