# VERIFY: Sổ Điểm (Phóng To Trình Chiếu Đề, Dán Ảnh & Nạp Học Sinh/Điểm CSDL)

## Kết luận
PASS

## Đối chiếu Scope & Tính năng
- [x] **Trình chiếu đề bài to, rõ nét trên màn hình lớn/máy chiếu:**
  - Ảnh đề bài tự động mở rộng bao quát toàn màn hình (`width: min(94vw, 1200px); max-height: 80vh; min-height: 300px`), không còn bị thu nhỏ cục bộ ở giữa.
  - Thẻ trượt nền trắng bo góc `rounded-2xl shadow-2xl bg-white p-3 sm:p-6` giúp công thức và chữ trong ảnh nổi bật, khử chói mắt trên nền tối.
  - Phóng to / Thu nhỏ đa cấp độ: Nút `A-`, `100%`, `A+` điều khiển biến tỉ lệ `presentationImageScale` từ 50% đến 300%.
  - Phím tắt bàn phím: `+`/`=` để phóng to, `-`/`_` để thu nhỏ, `0` để trở về 100%, `ArrowLeft`/`ArrowRight` chuyển câu, `Space` tạm dừng/bật đồng hồ, `Esc` đóng trình chiếu.
- [x] **Dán ảnh đề bài siêu tốc:**
  - Nút **Dán ảnh (Ctrl+V)** đọc ảnh trực tiếp từ clipboard (`navigator.clipboard.read()`).
  - Phím tắt Ctrl+V toàn cục bắt sự kiện dán ở mọi nơi trên trang, tự động nạp đề và hiển thị thông báo thành công.
- [x] **Khắc phục lỗi CSDL & mất điểm:**
  - Tự động lấy danh sách lớp từ bảng `users` và `gradebooks`.
  - Tự động chọn lớp và gọi `loadBook()` khi mở trang.
  - Safe Score Merge: Hợp nhất học sinh từ CSDL và bảng lưu với điểm số trong `localStorage`, tuyệt đối bảo toàn 100% điểm đã chấm.

## Test đã chạy
1. `node tests/sodiem-smoke.js` -> PASS.
2. `node tests/teacher-permissions-smoke.js` -> PASS.
3. `node tests/security-f12-smoke.js` -> PASS.
4. `git diff --check` -> PASS.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Phóng to đề bài trình chiếu: PASS.
- Tiêu chí 2: Điều chỉnh cỡ zoom ảnh và chữ bằng A+/A-/100%: PASS.
- Tiêu chí 3: Dán ảnh đề bài clipboard & Ctrl+V toàn cục: PASS.
- Tiêu chí 4: Nạp học sinh CSDL và khôi phục điểm: PASS.
- Tiêu chí 5: Toàn bộ smoke test: PASS.

## Bug
Không có.
