# VERIFY

## Kết luận
FAIL

## Đối chiếu scope
1. **Khóa toàn bộ tính năng khi chưa kích hoạt:**
   - Chưa đạt trọn vẹn trên bản thực thi thực tế của người dùng:
     + File thực thi `app_trolythien/dist/TroLyHoangThien/TroLyHoangThien.exe` chưa được đóng gói lại (vẫn là bản cũ được biên dịch từ Phase 3), nên khi người dùng nhấp chạy file `.exe` thì ứng dụng vẫn chạy code cũ chưa có cơ chế khóa.
     + Trong mã nguồn `app_trolythien/ui/main_window.py`: hàm `open_module` chưa kiểm tra `if self._app_locked: return` (khiến người dùng click vào thẻ trên Dashboard vẫn chuyển trang được); luồng `_apply_status` khi preflight xong vẫn gọi `model_combo.setEnabled(...)` ghi đè trạng thái khóa.
2. **Tiêu đề và nhận diện:**
   - Mã nguồn đã đổi thành «Trợ lý sư phạm», nhưng bản `.exe` cũ vẫn hiện tiêu đề dài dòng cũ.
3. **Mô hình AI:**
   - Mã nguồn đã nạp động từ `agy models`.
4. **Bản quyền Online:**
   - Đã có `api/license.php` và tab trên `admin.html`.

## Test đã chạy
- Kiểm tra tệp `.exe`: `app_trolythien/dist/TroLyHoangThien/TroLyHoangThien.exe` có thời gian tạo là `10/6/2026 19:38`, trước khi triển khai Phase 4.
- Kiểm tra logic `ui/main_window.py`:
  + `open_module()` thiếu `if self._app_locked: return`.
  + `_apply_status()` kích hoạt lại `model_combo` khi `_app_locked` đang là `True`.

## Pass / Fail từng tiêu chí
- [ ] File thực thi `.exe` được đóng gói cập nhật cơ chế khóa bản quyền: **FAIL**
- [ ] Chặn triệt để điều hướng từ Dashboard (`open_module`) khi ứng dụng đang khóa: **FAIL**
- [ ] Giữ khóa `model_combo` khi preflight kết nối xong nếu chưa có bản quyền: **FAIL**
- [x] Tiêu đề và thương hiệu tối giản trong mã nguồn: **PASS**
- [x] Mô hình AI nạp động từ `agy models`: **PASS**
- [x] API bản quyền `api/license.php` và giao diện `admin.html`: **PASS**

## Bug
- Lỗi 1: File thực thi `TroLyHoangThien.exe` chưa được build lại sau khi sửa code Phase 4, khiến người dùng mở app vẫn thấy giao diện cũ và chưa bị khóa.
  + Tái hiện: Chạy `app_trolythien\dist\TroLyHoangThien\TroLyHoangThien.exe`.
  + File liên quan: `app_trolythien/build_exe.bat`, `app_trolythien/dist/TroLyHoangThien/TroLyHoangThien.exe`.
  + Cách sửa: Chạy lại `build_exe.bat` để cập nhật bản phân phối `.exe`.

- Lỗi 2: Trong `ui/main_window.py`, người dùng có thể nhấp vào các nút thẻ trên Dashboard để chuyển tab vì `open_module` không kiểm tra `_app_locked`.
  + Tái hiện: Mở app ở trạng thái chưa kích hoạt, nhấp vào thẻ "Vẽ hình học" trên Dashboard, app vẫn chuyển tab sang vẽ hình.
  + File liên quan: `app_trolythien/ui/main_window.py`.
  + Cách sửa: Thêm `if self._app_locked: return` vào đầu hàm `open_module(self, key: str, label: str)`.

- Lỗi 3: Khi preflight xong, hàm `_apply_status` mở lại `model_combo` ngay cả khi `_app_locked == True`.
  + Tái hiện: Đợi 1-2 giây sau khi mở app khi có kết nối Agy, combobox mô hình AI sáng trở lại.
  + File liên quan: `app_trolythien/ui/main_window.py`.
  + Cách sửa: Trong `_apply_status`, đặt `self.model_combo.setEnabled(not self._app_locked and (ready or self.model_combo.count() > 0))`.
