# PLAN

## Hiện trạng
1. **Khóa bản quyền (Licensing Lock):**
   - Hiện tại khi chưa kích hoạt bản quyền, ứng dụng mới chỉ cảnh báo khi bấm nút "Gửi việc/Chạy", người dùng vẫn bấm chuyển tab và thao tác trên giao diện bình thường.
   - Cần phải **khóa toàn bộ tính năng** (vô hiệu hóa các tab, nút chuyển trang, các ô nhập liệu) khi máy chưa được kích hoạt bản quyền. Chỉ mở khóa sau khi đã kích hoạt thành công.
2. **Nhận diện & Tiêu đề giao diện (UI/UX Branding):**
   - Tiêu đề cửa sổ và sidebar hiện đang quá dài dòng (`Trợ Lý Sư Phạm Hoàng Thiên — Nền Tảng Giảng Dạy & Khảo Thí 4.0`).
   - Có dòng ghi chú thừa ở chân sidebar: `Chạy ngầm agy.exe. Cửa sổ vẫn chuyển tab khi đang soạn.`.
   - Cần tối giản: Tiêu đề cửa sổ và thanh sidebar chỉ để duy nhất: **«Trợ lý sư phạm»**. Xóa toàn bộ các dòng phụ đề rườm rà.
3. **Mô hình AI từ Agy:**
   - Danh sách mô hình AI phải được lấy tự động trực tiếp từ lệnh `agy models` do chính Agy cung cấp.
   - Tránh việc hardcode hoặc hiển thị danh sách mô hình giả lập khiến người dùng nhầm lẫn.
4. **Hệ thống Kích hoạt Online qua hoangthiencm.id.vn:**
   - Website `hoangthiencm.id.vn` cần có `api/license.php` và giao diện quản lý trên `admin.html` để Thầy Thiên duyệt/khóa máy từ xa.
   - Desktop App kết nối trực tiếp đến API này để kích hoạt 1-click.

## Phạm vi
1. **Khóa toàn bộ tính năng khi chưa có bản quyền:**
   - Trong `main_window.py`: Tạo hàm quản lý trạng thái khóa `_set_app_locked(locked: bool)`.
   - Khi `locked = True` (chưa kích hoạt):
     + Vô hiệu hóa toàn bộ `self.stack` (hoặc hiển thị màn hình khóa thông báo bản quyền).
     + Vô hiệu hóa toàn bộ danh sách `self.nav_buttons` trên sidebar.
     + Vô hiệu hóa combobox mô hình AI và các thao tác soạn bài/vẽ hình/kiểm tra.
     + Nút «Bản quyền» trên Header luôn bật để người dùng mở hộp thoại kích hoạt.
   - Khi kích hoạt thành công (dù qua Online trên web Thầy hay nhập Offline key): Tự động gọi `_set_app_locked(False)` để mở khóa toàn bộ ứng dụng ngay lập tức mà không cần khởi động lại app.
2. **Tối giản giao diện & Tiêu đề:**
   - Sửa tiêu đề cửa sổ chính thành đúng: `Trợ lý sư phạm`.
   - Sửa nhãn thương hiệu trên sidebar thành: `Trợ lý sư phạm`.
   - Xóa bỏ hoàn toàn nhãn phụ đề `Nền tảng giảng dạy & khảo thí 4.0`.
   - Xóa bỏ hoàn toàn nhãn `Chạy ngầm agy.exe. Cửa sổ vẫn chuyển tab khi đang soạn.` ở chân sidebar.
3. **Mô hình AI lấy tự động theo Agy:**
   - Hoàn thiện việc đọc kết quả từ `agy models` trong `core/preflight.py`.
   - Combobox mô hình AI trên Header nạp danh sách trực tiếp từ các model do `agy models` trả về, tự động chọn model mặc định đầu tiên nếu người dùng chưa chọn.
4. **Tích hợp Quản lý Bản quyền Online trên hoangthiencm.id.vn:**
   - `api/license.php`: Hỗ trợ lưu trữ `api/storage/licenses.json`, xử lý `verify` (cho App Desktop) và `list`, `approve`, `revoke`, `delete` (cho trang `admin.html` bảo vệ bằng Admin Key).
   - `admin.html`: Thêm tab/panel «Bản Quyền App Desktop» hỗ trợ duyệt máy, khóa máy, xóa và tìm kiếm nhanh.
   - `app_trolythien/core/license.py`: Kết nối trực tiếp `https://hoangthiencm.id.vn/api/license.php`.

## Ngoài phạm vi
- Không can thiệp vào các logic nghiệp vụ môn học (Toán, KHBD, Văn bản...) bên trong từng tab.
- Giữ nguyên phương án nhập mã Offline Key dự phòng cho giáo viên ở vùng không có Internet.

## File dự kiến tác động
1. `app_trolythien/ui/main_window.py` *(Sửa)*: Khóa toàn bộ tính năng khi chưa kích hoạt; sửa tiêu đề và sidebar thành «Trợ lý sư phạm»; xóa các dòng mô tả phụ; cập nhật nạp models từ agy.
2. `app_trolythien/core/preflight.py` *(Sửa)*: Đảm bảo `fetch_available_models()` nạp chính xác các model từ `agy models`.
3. `app_trolythien/core/license.py` *(Sửa)*: Kết nối `https://hoangthiencm.id.vn/api/license.php`.
4. `app_trolythien/ui/license_dialog.py` *(Sửa)*: Cải tiến thông báo kích hoạt online rõ ràng.
5. `api/license.php` *(Tạo mới)*: API lưu trữ và quản lý bản quyền trên web Thầy Thiên.
6. `admin.html` *(Sửa)*: Bổ sung panel Quản trị Bản Quyền App Desktop.
7. `tests/test_verify_phase4.py` *(Tạo mới)*: Kiểm thử tự động cơ chế khóa app, tiêu đề, models agy và API license.

## Các bước thực hiện
1. **Thắt chặt cơ chế Khóa bản quyền trong `main_window.py`:**
   - Viết hàm `_set_app_locked(locked: bool)`: Khóa `stack`, sidebar nav buttons, header controls (trừ nút Bản quyền).
   - Khi mở app: Kiểm tra `is_licensed()`. Nếu `False`, áp dụng `_set_app_locked(True)` và mở `LicenseDialog`.
   - Trong `LicenseDialog` hoặc sau khi kích hoạt thành công: Gọi lại `_set_app_locked(False)` để mở khóa toàn bộ tính năng.
2. **Tối giản thông tin tiêu đề và Sidebar:**
   - Sửa `setWindowTitle("Trợ lý sư phạm")`.
   - Sửa `brand = QLabel("Trợ lý sư phạm")`, xóa widget `tag` và xóa widget `note`.
3. **Đồng bộ Mô hình AI tự động từ `agy`:**
   - `core/preflight.py`: Gọi `agy models` lấy danh sách chuẩn từ CLI Agy.
   - Đưa kết quả vào `model_combo` khi tiến trình preflight hoàn tất.
4. **Xây dựng Backend `api/license.php` & Giao diện `admin.html`:**
   - Viết `api/license.php` đọc/ghi `api/storage/licenses.json` bằng `flock`.
   - Bổ sung panel Bản Quyền App Desktop trên `admin.html` với nút Duyệt, Khóa, Xóa.
   - Trỏ `LICENSE_ONLINE_URL = "https://hoangthiencm.id.vn/api/license.php"` trong `core/license.py`.
5. **Kiểm thử nghiệm thu:**
   - Chạy kiểm thử tự động với `tests/test_verify_phase4.py`.

## Rủi ro & Giải pháp
- **Rủi ro:** Người dùng mở app khi chưa có mạng và chưa có bản quyền $\rightarrow$ Khóa toàn bộ tính năng, hướng dẫn copy Mã máy gửi Thầy Thiên lấy mã Offline hoặc kết nối mạng để Thầy duyệt Online.
- **Rủi ro:** Agy CLI mất nhiều giây để trả về danh sách models $\rightarrow$ Giữ Preflight chạy nền (QThread) để giao diện không bị đơ, khi có kết quả từ Agy thì nạp ngay vào combobox.

## Tiêu chí nghiệm thu
- [ ] Khi chưa kích hoạt: Mọi tính năng (các tab, nút chuyển trang, thao tác) bị KHÓA hoàn toàn, không thể sử dụng.
- [ ] Sau khi kích hoạt thành công (Online hoặc Offline): Toàn bộ tính năng tự động MỞ KHÓA ngay lập tức.
- [ ] Tiêu đề cửa sổ và Sidebar hiển thị đúng: **«Trợ lý sư phạm»** (đã xóa các dòng phụ đề và ghi chú rườm rà).
- [ ] Danh sách mô hình AI được nạp tự động từ chính Agy CLI cung cấp.
- [ ] `api/license.php` và `admin.html` kết nối đồng bộ, cho phép Thầy duyệt bản quyền online qua web.
- [ ] Toàn bộ bộ test `tests/test_verify_phase4.py` đạt PASS.
