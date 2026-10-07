<<<<<<< HEAD
# IMPLEMENT

App khóa toàn bộ tính năng khi chưa kích hoạt và mở khóa ngay sau khi kích hoạt Online hoặc Offline. Tiêu đề cửa sổ và thương hiệu sidebar là «Trợ lý sư phạm». Danh sách mô hình AI chỉ lấy từ `agy models`. Desktop gửi kích hoạt tới `https://hoangthiencm.id.vn/api/license.php`. Trang quản trị có tab «Bản Quyền App Desktop».

## Đã làm

- `app_trolythien/ui/main_window.py`: `setWindowTitle("Trợ lý sư phạm")`. Nhãn sidebar `brand` đúng «Trợ lý sư phạm». Đã bỏ widget phụ đề và dòng chân «Chạy ngầm agy.exe…». `_set_app_locked(locked)` tắt `stack`, mọi `nav_buttons`, nút tài khoản, combobox mô hình, khung nhật ký và nút chạy/vẽ/soạn. Nút «Bản quyền» luôn bật. Banner `licenseOff` hiện khi đang khóa. Mở app nếu `is_licensed()` sai thì khóa và xếp `LicenseDialog`. Sau khi hộp thoại đóng, `_apply_license_gate()` gọi `_set_app_locked(False)` nếu đã kích hoạt, không cần khởi động lại. Combobox nhận danh sách preflight; chưa chọn thì lấy dòng đầu.
- `app_trolythien/core/preflight.py`: bỏ `_fallback_models` và mọi id mô hình gắn sẵn. `fetch_available_models()` trả bảng parse từ `agy models`, hoặc `[]` khi thiếu `agy`, lệnh lỗi, mã thoát khác 0, hoặc bảng rỗng. Preflight vẫn chạy trên QThread.
- `app_trolythien/core/license.py`: `LICENSE_ONLINE_URL = "https://hoangthiencm.id.vn/api/license.php"`. `TLHT_LICENSE_URL` ghi đè URL khi kiểm thử. `verify_license_online` POST JSON `action=verify`. Chỉ coi là đã cấp phép khi `status` là `active` (hoặc `ok` đúng và status rỗng/`active`) và email, mã máy khớp. `pending` và `revoked` không mở khóa. Đường mã HMAC offline giữ nguyên.
- `app_trolythien/ui/license_dialog.py`: lời dẫn nói gửi Email và mã máy tới hoangthiencm.id.vn, Thầy duyệt trên trang quản trị, bấm lại «Kích hoạt Online», hoặc nhập mã offline khi không có mạng. Trạng thái nút Online: «Đang gửi Email và Mã máy tới hoangthiencm.id.vn…».
- `api/license.php`: kho `api/storage/licenses.json` (hoặc `TLHT_LICENSE_STORE`), khóa `flock`. `verify` công khai: chưa có cặp email/mã máy thì ghi `pending`; `active` trả `ok`; `revoked` hoặc `pending` trả từ chối. `list`, `approve`, `revoke`, `delete` cần Admin Key (`TLHT_ADMIN_KEY`, không thì `ADMIN_KEY` trong `api/config.php`) qua header `X-Admin-Key`. Không nạp `db.php`.
- `admin.html`: tab `licenseapp` «Bản Quyền App Desktop». Ô tìm `desktopLicenseSearch`, bảng, nút Duyệt / Khóa / Xóa (`approve`, `revoke`, `delete`). Danh sách gọi `api/license.php?action=list` với `X-Admin-Key` lấy từ `cachedKey`.
- `tests/test_verify_phase4.py`: bốn kiểm thử khóa app, tiêu đề, không còn danh sách mô hình giả, client online, và token PHP/admin.
=======
# IMPLEMENT: Chuẩn hóa KHBD V2.0 (NLS/AI, hình vẽ, công thức)

## Đã làm
- Khóa ma trận sư phạm trong `.agents/rules/soankhbd.md`, `PROMPT_SOAN_GIAO_AN.md` và `HUONG_DAN_SOAN_KHBD_HANG_LOAT.md`: chỉ tích hợp NLS/AI khi cột Ghi chú PPCT có mã; bài số học lý thuyết không chèn ảnh; Mindmap chỉ ở Hoạt động 2.1 của tiết luyện tập chung / ôn tập; checklist trước khi xuất.
- `sanitizeKhbdMathSource` trong `TROLYTHIEN/engine/export_khbd_engine.js`: khôi phục Vertical Tab + `dots` thành `\vdots`, Form Feed + `rac` thành `\frac`, xóa ký tự điều khiển, rút `\ \vdots \` về `\vdots`, đổi `dots` giữa hai toán hạng thành `\vdots`, đổi `\not\vdots` thành `\nmid`. Cảnh báo khi Word khóa file (ghi `_Moi.docx`).
- `js/khbd-docx.js` dùng cùng lớp lọc trước `latexToUnicodeMath` và `normalizeLatexForMath`. Equation giữ `⋮` (U+22EE).
- `tools/export_all_8_khbd.js` cảnh báo khi đường dẫn ra là `_Moi.docx`.
- Ba bài 03, 04, 08 đổi dòng tích hợp sang `***(Tích hợp NLS …)***` và `***(Tích hợp AI …)***`. Năm bài còn lại không có dòng đó. Ảnh Mindmap chỉ còn ở bài 01, 02, 06.
>>>>>>> 866d88ee469e21394eb14b96c3a85563ad6a7cd6

## Kiểm thử
- `node tests/khbd-math-sanitize-smoke.js`: PASS (chuỗi `$36 \vdots x$`, `$48 \dots x$`, `100 - x \dots 4`, `a \not\vdots b`, `\frac{24}{108}`, VT/`dots`, FF/`frac`, và đối chiếu 8 file Markdown).
- `node tools/export_all_8_khbd.js`: 8/8 ghi đè thành công, không bị EBUSY.
- Giải nén `word/document.xml`: không file nào còn chữ `dots`. Số `m:oMath` và `⋮`: 01 (27/0), 02 (41/0), 03 (84/14), 04 (41/2), 05 (28/0), 06 (39/9), 07 (74/3), 08 (79/1). Bài 01 và 02 không có phép chia hết nên không có `⋮`.

<<<<<<< HEAD
- `tests/test_verify_phase4.py` bằng Python 3.14, `QT_QPA_PLATFORM=offscreen`, in «ALL PHASE 4 TESTS PASSED», mã thoát 0.
- Test 1: chưa kích hoạt thì cửa sổ và brand là «Trợ lý sư phạm», không còn hai dòng phụ, stack/nav/combo/nút chạy tắt, nút Bản quyền bật, banner khóa không bị ẩn. Ghi kích hoạt offline rồi `_apply_license_gate()` thì mở khóa ngay. Combobox trống prefer thì chọn model đầu.
- Test 2: parse bảng `agy models`; không còn `_fallback_models` hay `gpt-oss-120b-medium`. `find_agy` trả về rỗng thì danh sách model là `[]`.
- Test 3: máy chủ HTTP cục bộ. Lần verify `pending` không cấp phép; sau khi trạng thái `active` thì cấp phép. URL hằng số đúng `https://hoangthiencm.id.vn/api/license.php`.
- Test 4: `api/license.php` có `flock`, `licenses.json`, `verify`, `list`, `approve`, `revoke`, `delete`, `pending`, `active`, `HTTP_X_ADMIN_KEY`, `TLHT_LICENSE_STORE`. `admin.html` có tab, ô tìm và ba nút hành động.

## Giới hạn

- Máy không có `php` trên PATH. `api/license.php` được đối chiếu token và hợp đồng JSON phía client; chưa chạy bằng `php -S`.
- Không sửa `tests/test_verify_phase3.py`. Assertion tiêu đề cũ trong phase 3 sẽ lệch sau lần đổi tiêu đề này.
- Đã đóng gói lại bằng PyInstaller 6.22.3, Python 3.14.7, icon `assets\app_icon.ico`. Log có «Copying icon to EXE» và «Build complete!». Exe `app_trolythien\dist\TroLyHoangThien\TroLyHoangThien.exe` mở lên còn sống sau 4 giây, rồi bị tắt. Chưa commit.
- Chưa bấm duyệt thật trên hoangthiencm.id.vn và chưa gọi `agy models` sống trong lần test này.
=======
## Chưa kiểm
- Chưa mở 8 file trên Microsoft Word (viền, lề, ngắt dòng). Phần này để `/verify`.

## Việc tiếp
- Antigravity, chat mới: `/verify`.
>>>>>>> 866d88ee469e21394eb14b96c3a85563ad6a7cd6
