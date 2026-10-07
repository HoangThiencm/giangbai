# IMPLEMENT

Hộp thoại bản quyền chỉ còn kích hoạt online. Không còn ô mã offline và nút «Nhập Mã kích hoạt». Nút chính là «Kích hoạt bản quyền», gửi Email và Mã máy tới hoangthiencm.id.vn. File `license.dat` chỉ được công nhận khi `mode` là `online`.

## Đã làm

- `app_trolythien/ui/license_dialog.py`: bỏ `self.key` và `_offline`. Lời dẫn đúng câu trong plan. Ô Email, ô Mã máy chỉ đọc, nút «Copy Mã máy & Email», nút «Kích hoạt bản quyền», nút «Đóng». Khi gửi, trạng thái là «Đang gửi Email và Mã máy tới hoangthiencm.id.vn…». Duyệt thành công thì `save_activation(email, "online")` và đóng hộp thoại.
- `app_trolythien/core/license.py`: xóa `issue_offline_key` và `verify_license_offline`. Thông báo lỗi online không còn hướng dẫn mã offline. `save_activation` chỉ ghi `mode` online. `current_license` bỏ qua bản ghi không phải online.
- `tests/test_verify_phase4.py`: hộp thoại không còn nhãn/nút offline; mở khóa bằng `save_activation(email, "online")`; mã nguồn `license.py` không còn hai hàm offline.

## Kiểm thử

- `tests/test_verify_phase4.py` bằng Python 3.14.7, `QT_QPA_PLATFORM=offscreen`, mã thoát 0.
- `app_trolythien/build_exe.bat` với PyInstaller 6.22.3. Log có «Copying icon to EXE» và «Build complete!».
- `app_trolythien/dist/TroLyHoangThien/TroLyHoangThien.exe` (2 215 051 byte, 2026-10-07 08:21) mở lên còn sống sau 4 giây, rồi bị tắt.

## Giới hạn

- `tests/test_verify_phase3.py` vẫn import `issue_offline_key` và `verify_license_offline`. File đó nằm ngoài plan nên không sửa. Chạy phase 3 sẽ lỗi import.
- Bản quyền offline đã lưu trên máy trước đây không còn mở khóa.
- Chưa bấm duyệt thật trên hoangthiencm.id.vn trong lần này. Chưa commit.

## Việc tiếp

- Antigravity, chat mới: `/verify`.
