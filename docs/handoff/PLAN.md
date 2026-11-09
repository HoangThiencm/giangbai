# PLAN

## Hiện trạng
- Người dùng vào trang quản trị `admin.html` bật quyền "Sửa lỗi chính tả AI" (`sualoichinhta`) cho tài khoản giáo viên/học sinh và lưu lại, nhưng tài khoản không nhận được quyền và công cụ không hiển thị trên trang chủ (`index.html`).
- Nguyên nhân:
  + Trong backend `api/helpers.php`: Hàm `page_catalog()` (danh mục trang hợp lệ của hệ thống) chưa khai báo key `'sualoichinhta'`. Do đó, hàm `normalize_pages()` khi xử lý lưu quyền (`api/admin_students.php`) và khi trả về phiên đăng nhập (`api/me.php` -> `teacher_allowed_pages_resolved()`) đã tự động loại bỏ `'sualoichinhta'` ra khỏi mảng `allowed_pages`.
  + Trong `api/helpers.php`: Các hàm `teacher_workspace_page_ids()` và `teacher_feature_keys_for_pages()` cũng chưa đăng ký `'sualoichinhta'`.
  + Trong frontend `admin.html`: Mảng `CLIENT_FEATURE_CHECKS` và khối toggle tính năng toàn cục chưa có `'sualoichinhta'`, dẫn đến cờ tính năng `user_features` không được đồng bộ chuẩn xác khi lưu quyền giáo viên.

## Phạm vi
1. Cập nhật `api/helpers.php`:
   - Bổ sung `'sualoichinhta'` vào `page_catalog()`:
     `'sualoichinhta' => ['title' => 'Sửa lỗi chính tả AI', 'url' => 'sualoichinhta.html'],`
   - Bổ sung `'sualoichinhta'` vào mảng trả về của hàm `teacher_workspace_page_ids()`.
   - Bổ sung `'sualoichinhta' => 'sualoichinhta'` vào mảng trả về của hàm `teacher_feature_keys_for_pages()`.
2. Cập nhật `admin.html`:
   - Bổ sung `'sualoichinhta'` vào mảng `CLIENT_FEATURE_CHECKS`.
   - Bổ sung ô checkbox cấu hình tính năng toàn cục `cfg_sualoichinhta` trong phần quản trị tính năng của Admin.

## Ngoài phạm vi
- Không thay đổi logic phân quyền trong `access-control.js` hay cấu trúc giao diện `sualoichinhta.html`.
- Không can thiệp vào cấu trúc cơ sở dữ liệu bảng `users`.

## File dự kiến tác động
- `api/helpers.php`
- `admin.html`

## Các bước thực hiện
1. Bước 1: Chỉnh sửa `api/helpers.php`:
   - Thêm `'sualoichinhta' => ['title' => 'Sửa lỗi chính tả AI', 'url' => 'sualoichinhta.html']` vào mảng trả về của `page_catalog()`.
   - Thêm `'sualoichinhta'` vào mảng trả về của `teacher_workspace_page_ids()`.
   - Thêm `'sualoichinhta' => 'sualoichinhta'` vào mảng trả về của `teacher_feature_keys_for_pages()`.
2. Bước 2: Chỉnh sửa `admin.html`:
   - Thêm `'sualoichinhta'` vào mảng `CLIENT_FEATURE_CHECKS`.
   - Thêm ô checkbox `cfg_sualoichinhta` trong tab cấu hình tính năng chung (Global Features).
3. Bước 3: Kiểm thử đồng bộ:
   - Dùng script kiểm tra Node.js xác nhận `api/helpers.php` và `admin.html` chứa đầy đủ các khai báo.
   - Đảm bảo `normalize_pages` không còn lọc mất `sualoichinhta`.

## Rủi ro
- Cache phiên làm việc trình duyệt (`sessionStorage` chứa `global_config_cache_v1` hoặc `localStorage.getItem('allowedPages')` cũ): Cần hướng dẫn người dùng nhấn F5 hoặc đăng nhập lại để cập nhật quyền mới nhất từ server.

## Cách kiểm thử
1. Kiểm tra tĩnh file code:
   - Xác nhận `page_catalog()`, `teacher_workspace_page_ids()`, `teacher_feature_keys_for_pages()` trong `api/helpers.php` đều chứa `sualoichinhta`.
   - Xác nhận `CLIENT_FEATURE_CHECKS` trong `admin.html` chứa `sualoichinhta`.
2. Kiểm tra lưu và đọc quyền:
   - Vào `admin.html`, mở cấu hình một tài khoản giáo viên, bật switch "Sửa lỗi chính tả AI" và bấm lưu.
   - Kiểm tra CSDL hoặc response từ `api/admin_students.php` xác nhận `allowed_pages` trả về có chứa `sualoichinhta` và `allowed_count` tăng tương ứng.
   - Đăng nhập tài khoản giáo viên, kiểm tra `api/me.php` trả về `allowed_pages` có `sualoichinhta`.
   - Mở trang chủ `index.html`, xác nhận thẻ "Sửa lỗi chính tả AI" xuất hiện và click mở được `sualoichinhta.html`.

## Tiêu chí nghiệm thu
- Backend `api/helpers.php` chấp nhận và lưu `sualoichinhta` vào CSDL không bị lọc bỏ.
- Cấp quyền trong `admin.html` lưu thành công, thông báo hiển thị đúng số lượng quyền.
- Trang chủ `index.html` của tài khoản được cấp quyền hiển thị ngay thẻ công cụ "Sửa lỗi chính tả AI".
