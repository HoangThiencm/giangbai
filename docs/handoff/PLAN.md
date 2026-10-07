# PLAN

## Hiện trạng
1. **Bản chất ứng dụng:**
   - App Trợ lý sư phạm bắt buộc phải có kết nối Internet để gọi AI của Google / Antigravity (`agy.exe`). Không có Internet thì app không thể suy luận, không thể soạn KHBD hay vẽ hình.
   - Do đó, việc duy trì cơ chế "Mã kích hoạt Offline" là dư thừa, làm phức tạp giao diện `LicenseDialog` và gây rối cho người dùng.
2. **Cơ chế Kích hoạt Online qua `hoangthiencm.id.vn`:**
   - Cần tinh gọn quy trình kích hoạt về **1 luồng duy nhất — Kích hoạt Online 1-Click**.
   - Giáo viên chỉ cần nhập Email Gmail và bấm «Kích hoạt bản quyền». Hệ thống gửi Email + Mã máy lên `https://hoangthiencm.id.vn/api/license.php`.
   - Thầy Thiên duyệt trên `admin.html` là app tự động mở khóa vĩnh viễn trên máy tính.

## Phạm vi
1. **Tinh gọn `LicenseDialog` (`ui/license_dialog.py`):**
   - Xóa bỏ hoàn toàn:
     + Ô nhập mã offline `self.key` ("Mã kích hoạt offline").
     + Nút "Nhập Mã kích hoạt" (`self._offline`).
   - Giao diện mới cực kỳ tinh giản:
     + Hướng dẫn: "Nhập Email và bấm Kích hoạt bản quyền. Thầy Thiên phê duyệt trên trang quản trị hoangthiencm.id.vn để mở khóa ứng dụng."
     + Ô nhập Email Gmail.
     + Ô hiển thị Mã máy (Device ID) + Nút "Copy Mã máy & Email".
     + Nút chính: **«Kích hoạt bản quyền»** (gọi `verify_license_online`).
     + Nút "Đóng".
2. **Dọn dẹp `core/license.py`:**
   - Tập trung vào luồng `verify_license_online` và lưu chứng thực `save_activation(email, "online")`.
   - Giữ mã nguồn tinh gọn, không để thừa các luồng offline gây nhầm lẫn.
3. **Đóng gói lại File thực thi (`build_exe.bat`):**
   - Chạy PyInstaller đóng gói lại `TroLyHoangThien.exe` để cập nhật giao diện mới nhất và cơ chế khóa bản quyền chuẩn xác.

## Ngoài phạm vi
- Không thay đổi backend `api/license.php` và trang quản trị `admin.html` (đã được thiết kế sẵn sàng cho luồng online).

## File dự kiến tác động
1. `app_trolythien/ui/license_dialog.py` *(Sửa)*: Bỏ ô mã offline và nút offline, chỉ giữ 1 nút Kích hoạt bản quyền Online.
2. `app_trolythien/core/license.py` *(Dọn dẹp/Tối ưu)*: Đơn giản hóa các ghi chú và thông báo hướng dẫn sang online 100%.
3. `tests/test_verify_phase4.py` *(Cập nhật)*: Đồng bộ kiểm thử theo giao diện chỉ kích hoạt online.
4. `app_trolythien/build_exe.bat`: Đóng gói lại file `TroLyHoangThien.exe`.

## Các bước thực hiện
1. **Sửa `ui/license_dialog.py`:**
   - Xóa `self.key` và `_offline()`.
   - Đặt lại nhãn nút chính thành: **«Kích hoạt bản quyền»**.
   - Cập nhật thông báo trạng thái rõ ràng khi gửi thành công lên `hoangthiencm.id.vn`.
2. **Cập nhật bộ test:**
   - Chạy `tests/test_verify_phase4.py` đảm bảo tất cả test PASS.
3. **Đóng gói lại ứng dụng:**
   - Chạy `build_exe.bat` tạo `dist/TroLyHoangThien/TroLyHoangThien.exe` mới.

## Tiêu chí nghiệm thu
- [ ] `LicenseDialog` không còn ô nhập mã offline và nút offline.
- [ ] Chỉ còn 1 nút bấm «Kích hoạt bản quyền» (Online 1-click qua `hoangthiencm.id.vn`).
- [ ] Bộ test tự động PASS 100%.
- [ ] Bản `.exe` mới được biên dịch sẵn sàng sử dụng.
