# IMPLEMENT

Ứng dụng desktop PySide6 «Trợ lý Sư phạm Hoàng Thiên» nằm trong `app_trolythien/`. Mỗi phân hệ ghép prompt từ quy chuẩn `TROLYTHIEN/` rồi gọi `agy.exe` trong `QThread`. Thư mục app và bản đóng gói được chặn khỏi Git.

## Đã làm

- `.gitignore`: thêm `app_trolythien/`, `dist/`, `build/`, `*.spec`, `*.exe`.
- `app_trolythien/requirements.txt`: `PySide6>=6.6.0`, `pyinstaller>=6.0`. Đã cài PySide6 6.11.2 và PyInstaller 6.22.3.
- `app_trolythien/main.py`: cửa sổ Fusion, theme, icon `assets/icon.ico`.
- `app_trolythien/core/bridge.py`: `AntigravityWorker(QThread)` với `signal_log`, `signal_progress`, `signal_finished`. Tìm `agy.exe` trên PATH, rồi `%LOCALAPPDATA%\agy\bin\agy.exe` và `...\agy\agy.exe`.
- `app_trolythien/core/prompts.py`: `build_khbd_prompt`, `build_baitap_prompt`, `build_baigiang_html_prompt`, `build_vehinh_prompt`, `build_chuanhoa_prompt`, và `build_duyet_prompt` cho tab duyệt/báo cáo.
- Giao diện: sidebar 6 phân hệ, `QStackedWidget`, form từng tab, `LogPanel` (`setMaximumBlockCount(1000)`), thanh %, nút Dừng, Mở file kết quả, Mở thư mục kết quả (`QDesktopServices.openUrl`).
- `app_trolythien/build_exe.bat`: PyInstaller `--noconsole --name TroLyHoangThien`. Bản build nằm trong `app_trolythien/dist/`, không ở gốc repo.

## Cách gọi agy

Bản `agy` 1.2 trên máy không có cờ `--headless`. `-p` chính là chế độ một lượt không tương tác. Worker ghi prompt UTF-8 vào `app_trolythien/.runtime/lenh_hien_tai.md` rồi chạy:

`agy -p "Đọc tệp ... và thực hiện" --disable-slash-commands --dangerously-skip-permissions`

Thư mục làm việc là repo `giangbai`. stdout dùng `encoding=utf-8`, `errors=replace`. Cờ `--disable-slash-commands` tránh kích hoạt skill khi quy chuẩn có dấu `/`. Cờ quyền tự duyệt để tiến trình không dừng chờ bấm chấp nhận trong CLI.

## Kiểm thử

- `python -m pip install -r app_trolythien/requirements.txt`: xong.
- Qt offscreen, `MainWindow`: tiêu đề «Trợ lý Sư phạm Hoàng Thiên», 6 trang, chuyển sidebar 0→5, log tối đa 1000 dòng. Prompt KHBD có «Phương trình tích» và Công văn 5512. Ô ý kiến bài tập để trống thì prompt không có khối chỉ đạo riêng.
- Trong lúc `agy` chạy, bấm sang tab Vẽ hình vẫn đổi trang và nút Soạn bài đang khóa.
- Lượt `agy` ngắn, lệnh không sửa file: log có `PING_OK`, tiến độ 100, UI không đơ. `find_agy()` trả `C:\Users\HoangThien\AppData\Local\agy\bin\agy.exe`.
- `app_trolythien\build_exe.bat`: exit 0. File `app_trolythien\dist\TroLyHoangThien\TroLyHoangThien.exe` mở được và còn sống sau 4 giây, rồi bị tắt.
- `git status` không liệt kê file trong `app_trolythien/`.

## Giới hạn

- Chưa bấm «Soạn bài» cho bài «Phương trình tích» trên lượt agy thật, nên chưa có file mới trong `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/` từ phiên này. Lượt thật đó viết giáo án và chạy lâu.
- Chưa bấm lần lượt các form trên file `.exe` đã đóng gói. Đã kiểm cửa sổ nguồn bằng Qt offscreen và xác nhận tiến trình `.exe` khởi chạy.
- Không sửa `agy.exe`, không sửa các trang web (`taobaitap.html`, `khaosat.html`, …).
