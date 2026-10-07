# VERIFY

## Kết luận
FAIL

## Đối chiếu scope
1. **Kiểm tra API trên máy chủ trực tuyến `https://hoangthiencm.id.vn/api/license.php`:**
   - Kết quả: **FAIL** (Máy chủ trả về HTTP 404 Not Found).
   - Tệp `api/license.php` mới chỉ tồn tại ở mã nguồn cục bộ trong thư mục dự án trên máy tính, chưa được đẩy (commit/push hoặc upload FTP/Hosting) lên hosting thực tế `hoangthiencm.id.vn`.
2. **Kiểm tra giao diện trang quản trị trực tuyến `https://hoangthiencm.id.vn/admin.html`:**
   - Kết quả: **FAIL** (Giao diện web trực tuyến chưa có tab «Bản Quyền App Desktop»).
   - Nguyên nhân do tệp `admin.html` đã sửa ở local nhưng chưa được đồng bộ/upload lên hosting của Thầy.
3. **Ứng dụng Desktop kết nối trực tuyến:**
   - Khi mở app hoặc bấm «Kích hoạt Online», app gọi đến `https://hoangthiencm.id.vn/api/license.php` nhưng do máy chủ hosting chưa có tệp này (404) nên không thể đăng ký máy và không kích hoạt được qua web.

## Test đã chạy
- Gửi HTTP POST request trực tiếp đến `https://hoangthiencm.id.vn/api/license.php` với payload `{"action":"verify","email":"test@example.com","device_id":"TLHT-AAAA-BBBB-CCCC"}`:
  + Kết quả trả về: `(404) Not Found`.
- Kiểm tra mã nguồn cục bộ:
  + `api/license.php` đã được viết và sẵn sàng trong thư mục `api/`.
  + `admin.html` đã được tích hợp tab và bảng quản lý bản quyền desktop.
  + Nhưng toàn bộ thay đổi này chưa được cập nhật lên máy chủ live.

## Pass / Fail từng tiêu chí
- [ ] Tệp `api/license.php` hoạt động trực tiếp trên `https://hoangthiencm.id.vn`: **FAIL** (404 Not Found do chưa deploy lên hosting)
- [ ] Giao diện quản lý `admin.html` trực tuyến hiển thị mục duyệt bản quyền: **FAIL** (chưa đồng bộ lên hosting)
- [ ] Kích hoạt trực tuyến từ App Desktop thành công qua web thật: **FAIL** (bị chặn do API web trả 404)
- [x] Logic API và mã nguồn `api/license.php` cục bộ: **PASS**
- [x] Logic Client Desktop (`app_trolythien/core/license.py`) cục bộ: **PASS**

## Bug
- Lỗi 1: Máy chủ web `https://hoangthiencm.id.vn` trả về lỗi 404 Not Found khi truy cập `api/license.php`.
  + Tái hiện: Gọi `Invoke-RestMethod -Uri "https://hoangthiencm.id.vn/api/license.php" -Method Post`.
  + File liên quan: `api/license.php`, `admin.html`.
  + Hướng xử lý: Cần deploy / upload các tệp mới từ thư mục local lên hosting `hoangthiencm.id.vn` (qua GitHub push nếu có tự động deploy, hoặc qua File Manager / FTP của hosting):
    1. `api/license.php`
    2. `admin.html`
    3. Thư mục `api/storage/` (cấp quyền ghi để tạo file `licenses.json`).
