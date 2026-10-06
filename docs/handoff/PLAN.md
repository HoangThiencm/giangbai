# PLAN

## Hiện trạng
1. **Toàn bộ tri thức và nghiệp vụ của Trợ lý Sư phạm Hoàng Thiên hiện nằm trong thư mục `TROLYTHIEN/`:**
   - `1_SOAN_KHBD`: Mẫu prompt và quy chuẩn soạn Kế hoạch bài dạy Toán 6, 7, 8, 9 theo Công văn 5512.
   - `2_TAO_BAI_TAP`: Quy chuẩn cắt ghép đề, sinh bài tập bám sát SGK và chuẩn hóa câu hỏi.
   - `3_DUYET_GIAO_AN` & `4_DUYET_DE`: Đối soát hồ sơ tổ chuyên môn, xuất biên bản duyệt giáo án.
   - `8_TAO_BAO_CAO` & `9_VIET_SANG_KIEN`: Mẫu báo cáo chuyên môn, hợp đồng đào tạo và viết sáng kiến kinh nghiệm.
   - `10_BAI_GIANG_HTML`: Template bài giảng trình chiếu tương tác (`master_lecture_template.html`), menu chuột phải sư phạm, bảng viết, trắc nghiệm.
   - `11_VE_HINH`: Hướng dẫn và mã nguồn vẽ hình học, đồ thị.
   - `12_CHUAN_HOA_VAN_BAN`: Chuẩn hóa thể thức văn bản theo Nghị định 30/2020/NĐ-CP và Hướng dẫn 05-HD/VPTW.
   - `13_CHUYEN_GHI_AM`: Xử lý âm thanh và chuyển văn bản.
2. **Môi trường kỹ thuật trên máy tính:**
   - Đã có Python 3.14.7 cài đặt sẵn và hoạt động tốt.
   - Đã có công cụ dòng lệnh `agy.exe` của Google Antigravity tại `C:\Users\HoangThien\AppData\Local\agy\agy.exe` (phiên bản 1.2.13).
   - PySide6 có sẵn gói binary tương thích (`pyside6-6.11.2`) sẵn sàng cài đặt qua pip.
3. **Vấn đề cần giải quyết:**
   - Hiện tại tất cả các chức năng sư phạm trên chỉ có thể vận hành thông qua việc chat thủ công trong IDE Antigravity. Giáo viên chưa có một phần mềm desktop độc lập với giao diện đồ họa nút bấm thân thiện để chỉ cần click chọn và nhập thông tin là chạy ngầm Antigravity tự động.

## Phạm vi
- Xây dựng ứng dụng Desktop hoàn chỉnh bằng **PySide6 (Qt for Python)** mang tên: **Trợ lý Sư phạm Hoàng Thiên (HoangThien AI Assistant Desktop)**.
- Đóng gói toàn bộ các phân hệ nghiệp vụ của `TROLYTHIEN/` thành các Tab giao diện trực quan:
  1. **Tab Soạn KHBD:** Form chọn khối lớp, bài học, số tiết, bộ sách; nhập yêu cầu bổ sung; nút bấm tạo KHBD.
  2. **Tab Tạo bài tập & Đề thi:** Form chọn nguồn (nạp file hoặc chủ đề), mức độ, hình thức (CV 7991, trắc nghiệm, tự luận), ô nhập ý kiến sư phạm riêng; nút bấm tạo đề.
  3. **Tab Bài giảng HTML:** Form chọn bài học, sinh slide HTML tương tác sư phạm và nút mở trực tiếp trên trình duyệt.
  4. **Tab Vẽ hình học & Đồ thị:** Form nhập mô tả hình cần vẽ, xuất ảnh hoặc code trực quan.
  5. **Tab Chuẩn hóa văn bản:** Nạp file Word/văn bản và xuất văn bản chuẩn thể thức NĐ 30/2020.
  6. **Tab Duyệt giáo án & Báo cáo:** Kiểm tra hồ sơ giáo án, xuất biên bản báo cáo.
- Xây dựng module cầu nối chạy ngầm (**Antigravity Engine Bridge**):
  - Chạy `QThread` nền không gây đơ giao diện.
  - Gọi ngầm `agy.exe` (hoặc SDK Antigravity), truyền đúng System Instructions và Prompt nghiệp vụ từ `TROLYTHIEN/`.
  - Bắt luồng xuất dữ liệu thời gian thực (realtime stdout stream) hiển thị thanh tiến độ (% và log) cho giáo viên theo dõi.
  - Tự động mở file kết quả (`.docx`, `.html`, `.md`) hoặc thư mục đích sau khi hoàn thành.
- Cung cấp script đóng gói ứng dụng thành file thực thi `.exe` độc lập bằng PyInstaller.

## Ngoài phạm vi
- Không sửa đổi mã nguồn gốc của Antigravity binary (`agy.exe`).
- Không can thiệp vào các trang web online hiện tại (`taobaitap.html`, `khaosat.html`,...) trừ việc liên kết mở bài giảng HTML khi sinh xong.

## File dự kiến tác động
- **`.gitignore`**: Bổ sung quy tắc chặn Git cho `app_trolythien/`, `dist/`, `build/`, `*.spec`, `*.exe` để đảm bảo toàn bộ thư mục app và bản build đóng gói không bị đưa lên GitHub, tránh làm nặng kho mã nguồn.
- **QUY ĐỊNH BẮT BUỘC:** Toàn bộ mã nguồn ứng dụng PySide6 phải nằm 100% bên trong thư mục riêng **`app_trolythien/`**, TUYỆT ĐỐI KHÔNG sinh file code hay config lẻ ra thư mục gốc `giangbai/` để giữ gìn dự án luôn sạch sẽ, ngăn nắp.
- Cấu trúc các file dự kiến tạo mới trong `app_trolythien/`:
  1. `app_trolythien/requirements.txt`: Khai báo thư viện (`PySide6>=6.6.0`, `pyinstaller`).
  2. `app_trolythien/main.py`: Điểm khởi chạy ứng dụng GUI PySide6 (`QApplication`, thiết lập theme, icon).
  3. `app_trolythien/core/bridge.py`: Luồng thực thi ngầm `QThread` điều khiển `agy.exe`, quản lý tiến trình và log.
  4. `app_trolythien/core/prompts.py`: Bộ nạp và đóng gói prompt chuẩn từ thư mục `TROLYTHIEN/`.
  5. `app_trolythien/ui/main_window.py`: Cửa sổ chính với Sidebar điều hướng hiện đại (Modern Qt Fluent/Material Style).
  6. `app_trolythien/ui/tab_khbd.py`: Giao diện phân hệ Soạn KHBD.
  7. `app_trolythien/ui/tab_baitap.py`: Giao diện phân hệ Tạo bài tập.
  8. `app_trolythien/ui/tab_baigiang.py`: Giao diện phân hệ Bài giảng HTML.
  9. `app_trolythien/ui/tab_vehinh.py`: Giao diện phân hệ Vẽ hình học.
  10. `app_trolythien/ui/tab_chuanhoa.py`: Giao diện phân hệ Chuẩn hóa văn bản.
  11. `app_trolythien/ui/tab_duyet.py`: Giao diện phân hệ Duyệt giáo án / Báo cáo.
  12. `app_trolythien/ui/widgets/log_panel.py`: Widget hiển thị log trực tiếp và thanh tiến trình.
  13. `app_trolythien/build_exe.bat`: Script đóng gói ứng dụng ra file `.exe`.

## Các bước thực hiện
1. **Chặn Git (`.gitignore`):**
   - Thêm vào cuối file `.gitignore`:
     ```gitignore
     # Ứng dụng Desktop PySide6 & Bản đóng gói (tránh nặng GitHub)
     app_trolythien/
     dist/
     build/
     *.spec
     *.exe
     ```
   - Đảm bảo lệnh `git status` không hiển thị bất kỳ file nào của `app_trolythien/`.
2. **Thiết lập môi trường và cấu hình thư viện:**
   - Tạo file `app_trolythien/requirements.txt` với `PySide6`.
   - Cài đặt thư viện: `python -m pip install -r app_trolythien/requirements.txt`.
3. **Xây dựng lõi kết nối ngầm (`core/bridge.py`):**
   - Xây dựng lớp `AntigravityWorker(QThread)` kế thừa từ PySide6.
   - Tìm kiếm tự động đường dẫn `agy.exe` (kiểm tra `PATH` và `C:\Users\HoangThien\AppData\Local\agy\agy.exe`).
   - Sử dụng `subprocess.Popen` chạy `agy -p "<prompt>" --headless` với thư mục làm việc trỏ về repo `giangbai`.
   - Lắng nghe dòng xuất stdout, phát tín hiệu `signal_log(str)` và `signal_progress(int)`.
   - Bắt tín hiệu hoàn thành `signal_finished(bool, str)`.
4. **Đóng gói Prompt nghiệp vụ (`core/prompts.py`):**
   - Viết các hàm builder ghép prompt theo đúng quy chuẩn đã có trong `TROLYTHIEN/`:
     - `build_khbd_prompt(mon, lop, ten_bai, so_tiet, bo_sach, yeu_cau_rieng)`
     - `build_baitap_prompt(nguon_text, so_cau, hinh_thuc, muc_do, y_kien_su_pham)`
     - `build_baigiang_html_prompt(ten_bai, noi_dung_bai, yeu_cau_slide)`
     - `build_vehinh_prompt(mo_ta_hinh)`
     - `build_chuanhoa_prompt(noi_dung_van_ban)`
5. **Thiết kế giao diện người dùng PySide6 (`ui/`):**
   - Cửa sổ chính `MainWindow` phong cách giao diện hiện đại:
     - Sidebar bên trái với danh sách icon và tên các phân hệ.
     - QStackedWidget bên phải chuyển đổi mượt mà giữa các Tab.
     - Panel dưới cùng là khung hiển thị tiến trình (Progress Bar) và nút mở thư mục kết quả (`QDesktopServices.openUrl`).
   - Thiết kế từng Tab với đầy đủ form nhập liệu, combo box chọn nhanh và ô text mở rộng.
6. **Tích hợp và kiểm thử tương tác:**
   - Kết nối tín hiệu (Signals & Slots) từ các nút "Thực hiện" trên từng Tab tới `AntigravityWorker`.
   - Kiểm tra giao diện phản hồi mượt mà, không bị khóa giao diện khi Antigravity đang xử lý.
7. **Tạo kịch bản đóng gói `.exe`:**
   - Viết `build_exe.bat` sử dụng `pyinstaller --noconsole --name "TroLyHoangThien" --icon ... app_trolythien/main.py`.

## Rủi ro
1. **Tiến trình Antigravity chạy lâu làm đơ giao diện:**
   - *Biện pháp:* Bắt buộc tách toàn bộ quá trình gọi `agy` vào `QThread` riêng biệt, giao tiếp qua Qt Signals/Slots.
2. **Đường dẫn file và font tiếng Việt có dấu:**
   - *Biện pháp:* Thiết lập encoding UTF-8 đồng bộ trên mọi tiến trình subprocess (`encoding='utf-8'`, `errors='replace'`).
3. **Bộ nhớ khi log quá dài:**
   - *Biện pháp:* Khung log giới hạn số lượng dòng hiển thị tối đa (`setMaximumBlockCount(1000)`).

## Cách kiểm thử
1. Cài đặt `PySide6`: `python -m pip install PySide6`.
2. Khởi chạy ứng dụng: `python app_trolythien/main.py`.
3. Kiểm tra hiển thị:
   - Cửa sổ ứng dụng mở lên với giao diện PySide6 đầy đủ các Tab.
   - Chuyển đổi giữa các phân hệ: Soạn KHBD, Tạo bài tập, Bài giảng HTML, Vẽ hình, Chuẩn hóa văn bản.
4. Thử nghiệm thực thi chức năng:
   - Vào Tab "Soạn KHBD", nhập: Toán 6, Bài "Phương trình tích", bấm "Soạn bài".
   - Quan sát khung log hiển thị tiến trình Antigravity đang chạy ngầm.
   - Sau khi hoàn thành, file kết quả xuất hiện đúng trong `TROLYTHIEN/1_SOAN_KHBD/Ket_qua/` và tự động mở lên.
5. Thử nghiệm đóng gói `.exe`: Chạy `build_exe.bat` và mở file `.exe` trong thư mục `dist/`.

## Tiêu chí nghiệm thu
- Ứng dụng Desktop viết bằng PySide6 khởi chạy mượt mà, giao diện chuyên nghiệp, trực quan.
- Đóng gói đầy đủ các chức năng nghiệp vụ của Trợ lý Hoàng Thiên.
- Gọi ngầm `agy.exe` thực thi hoàn toàn tự động trong luồng nền, không đơ UI.
- Có log tiến độ thời gian thực và tự động mở file kết quả sau khi làm xong.
- Có script sẵn sàng đóng gói thành phần mềm `.exe` độc lập.
