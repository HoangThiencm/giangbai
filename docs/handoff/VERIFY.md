# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Tạo ứng dụng Desktop PySide6 độc lập hoàn toàn trong thư mục riêng `app_trolythien/`.
- [x] Đóng gói toàn bộ 10 phân hệ nghiệp vụ Trợ lý Sư phạm Hoàng Thiên vào `app_trolythien/troly/` (prompts và templates), không phụ thuộc bên ngoài repo `giangbai`.
- [x] Tiền kiểm tra (Preflight Check): kiểm tra `agy.exe` đã cài đặt và kiểm tra đăng nhập AI (`agy models`). Có hộp thoại hướng dẫn cài đặt và nút đăng nhập.
- [x] Cơ chế Đầu vào kép (Dual-Input): Khung dán đề bài/nội dung trực tiếp (`QTextEdit`) hỗ trợ Ctrl+V và nút dán nhanh, kết hợp nút chọn tệp đính kèm (`QFileDialog`).
- [x] Cơ chế Đầu ra linh hoạt: Cho phép chọn thư mục lưu kết quả (`PathSelector` qua `QFileDialog`), có nút mở file và mở thư mục sau khi hoàn tất.
- [x] Lõi Antigravity Bridge (`core/bridge.py`): Chạy nền qua `QThread`, gọi `agy.exe -p` với `--dangerously-skip-permissions` và `--disable-slash-commands`, đọc stream log thời gian thực và phát hiện `KET_QUA`.
- [x] Đóng gói độc lập: `build_exe.bat` đóng gói thành công ra `dist/TroLyHoangThien/TroLyHoangThien.exe` kèm toàn bộ tri thức `troly/`.
- [x] Chặn Git: `.gitignore` chứa đầy đủ 5 quy tắc chặn `app_trolythien/`, `dist/`, `build/`, `*.spec`, `*.exe`, không làm nặng kho GitHub.

## Test đã chạy
1. **Kiểm tra Preflight (`core/preflight.py`):**
   - `check_agy_installed()`: Trả về `(True, 'C:\\Users\\HoangThien\\AppData\\Local\\agy\\bin\\agy.exe')`.
   - `check_agy_login()`: Trả về `(True, 'gemini-3.8-flash-high')`.
2. **Kiểm tra Tri thức độc lập (`core/prompt_builder.py`):**
   - `knowledge_ready()`: Trả về `True`, đầy đủ 10 file prompt và 2 template HTML trong `app_trolythien/troly/`.
3. **Kiểm tra Dựng Prompt (`prompt_builder`):**
   - KHBD Prompt: 12,846 ký tự (nhúng quy chuẩn CV 5512).
   - Vẽ hình Prompt: 4,669 ký tự (nhúng tọa độ giải tích Oxy và 4 file kết quả).
   - Bài giảng HTML Prompt: 61,323 ký tự (nhúng master prompt bài giảng 16:9).
   - Chuẩn hoá văn bản Prompt: 9,523 ký tự (nhúng NĐ 30/2020 và văn bản Đảng).
4. **Kiểm tra Giao diện PySide6 Offscreen (`scratch/test_verify.py`):**
   - Tiêu đề cửa sổ: «Trợ lý Sư phạm Hoàng Thiên».
   - Bảng điều khiển Dashboard và chuyển đổi qua lại giữa tất cả các Tab hoạt động mượt mà.
   - Tab Vẽ hình: Nhận văn bản dán trực tiếp, hiển thị khung xem trước ảnh.
   - Tab Bài giảng: Form Môn, Lớp, Số tiết, Tên bài, nút mở HTML.
   - Tab Chuẩn hoá: Nhận file Word và dán trực tiếp.
5. **Kiểm tra Đóng gói (`build_exe.bat`):**
   - Tiến trình PyInstaller hoàn tất exit code 0.
   - File thực thi `dist/TroLyHoangThien/TroLyHoangThien.exe` khởi chạy thành công.
6. **Kiểm tra Git Protection (`.gitignore`):**
   - 5 mẫu chặn hoạt động chuẩn mực, không track thư mục app và bản build.

## Pass / Fail từng tiêu chí
- Kiểm tra cài đặt và đăng nhập agy: PASS
- Đóng gói tri thức độc lập trong app: PASS
- Cơ chế dán đề bài và chọn tệp đầu vào: PASS
- Cơ chế chọn thư mục lưu và mở đầu ra: PASS
- Khung xem trước hình ảnh và nút mở kết quả: PASS
- Giao diện PySide6 và điều hướng Sidebar: PASS
- Kết nối luồng chạy agy ngầm: PASS
- Đóng gói PyInstaller thành .exe: PASS
- Chặn Git kho mã nguồn: PASS

## Bug
Không phát hiện bug.
