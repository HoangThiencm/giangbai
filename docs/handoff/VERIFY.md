# VERIFY: Nghiệm thu Đưa xaydungphuluc.html ra Thư mục Gốc, Tự động Nhận API Key từ soankhbd.html, và Bật Security Guard Bảo vệ Mã nguồn

## Kết luận
PASS

## Đối chiếu scope
1. **Vị trí tệp**:
   - Đã tạo và hoàn thiện [xaydungphuluc.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/xaydungphuluc.html) trực tiếp ở thư mục gốc (đồng cấp với `index.html`, `soankhbd.html`, `admin.html`), mở trực tiếp tại `https://hoangthiencm.id.vn/xaydungphuluc.html`.
   - Giữ tệp tương thích ngược tại [GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/xaydungphuluc.html) tự động chuyển hướng về trang gốc.
2. **Bảo vệ mã nguồn & Chống F12 / DevTools (Security Guard)**:
   - Đã nhúng `<script src="js/security-guard.js"></script>` và `<script src="access-control.js"></script>` làm các thẻ đầu tiên trong `<head>` của `xaydungphuluc.html`.
   - Khắc phục hoàn toàn hiện tượng mở được DevTools / xem mã nguồn khi chạy trên domain thật (`hoangthiencm.id.vn`).
3. **Tự động Dùng Chung API Key từ `soankhbd.html`**:
   - Hàm `loadKeys()` tự động quét tất cả các khóa lưu trữ của `soankhbd.html`: `khbd_user_gemini_keys_${userEmail}`, `khbd_user_gemini_keys_default`, `khbd_gemini_api_keys`, `gemini_api_keys`, `xdpl_gemini_api_keys`, `global_gemini_keys`.
   - Giáo viên đã nhập key bên `soankhbd.html` khi mở `xaydungphuluc.html` sẽ thấy ngay trạng thái "🔑 X key sẵn sàng" mà không phải nhập lại.
4. **Phân quyền Toàn diện trên Backend & Admin UI**:
   - [index.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/index.html): Thẻ công cụ mở `xaydungphuluc.html` trong tab mới với `target="_blank" rel="noopener noreferrer"`.
   - [admin.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/admin.html): Đã cập nhật URL `xaydungphuluc.html`, merge an toàn `hostingPages` với dữ liệu backend, hiển thị đầy đủ toggle *Xây dựng Phụ lục 1, 2, 3 (CV 5512 - THCS)* trong form cấp/sửa quyền giáo viên.
   - [api/helpers.php](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/api/helpers.php): Đăng ký `xaydungphuluc` trong `page_catalog()`, `teacher_workspace_page_ids()`, `teacher_default_workspace_extras()`, `teacher_feature_keys_for_pages()`.
   - [access-control.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/access-control.js): Đăng ký ánh xạ `xaydungphuluc.html` và `xaydungphuluc`.
   - [global_config.json](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/global_config.json): Đã thêm `"xaydungphuluc": true` vào `features`.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS.
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` qua `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. **Vị trí tệp gốc**: `xaydungphuluc.html` nằm ở thư mục gốc, có nút Trang chủ trỏ `index.html`, tệp cũ trong `GIAO AN/` tự chuyển hướng $\rightarrow$ **PASS**.
2. **Security Guard & Access Control**: Nhúng `js/security-guard.js` và `access-control.js` chặn xem mã nguồn / F12 trên production $\rightarrow$ **PASS**.
3. **Tự động nhận diện API Key**: Quét tự động các khóa `khbd_user_gemini_keys_...` từ `soankhbd.html`, không bắt nhập lại nếu đã có $\rightarrow$ **PASS**.
4. **Phân quyền Backend PHP**: `api/helpers.php` đăng ký `xaydungphuluc` trong `page_catalog` và các nhóm quyền giáo viên $\rightarrow$ **PASS**.
5. **Admin UI & Portal Link**: `index.html` và `admin.html` đồng bộ URL `xaydungphuluc.html`, merge an toàn `hostingPages` $\rightarrow$ **PASS**.
6. **Kiểm thử tự động**: Toàn bộ smoke test đều PASS $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
