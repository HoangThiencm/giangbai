# Triển khai tài khoản học sinh trên hosting PHP/MySQL

## 1. Tạo database

Trong hosting panel:

1. Vào **Database Wizard** hoặc **Manage My Databases**.
2. Tạo database mới, ví dụ `giangbai`.
3. Tạo database user và mật khẩu.
4. Gán user vào database với quyền đầy đủ.

## 2. Import bảng

Vào **phpMyAdmin**, chọn database vừa tạo, mở tab **SQL**, dán nội dung file `database_schema.sql` rồi chạy.

## 3. Tạo cấu hình PHP

Có 2 cách.

### Cách A: Dùng setup.php

```text
setup.php
```

Upload `setup.php`, thư mục `api/`, và `database_schema.sql` lên hosting. Sau đó mở:

```text
https://ten-mien-cua-thay/setup.php
```

Nhập DB_HOST, DB_NAME, DB_USER, DB_PASS và ADMIN_KEY. Trang này sẽ tự tạo:

```text
api/config.php
```

Nếu chọn tùy chọn tạo bảng, `setup.php` cũng sẽ tự chạy `database_schema.sql`.

Sau khi cài xong nên xóa hoặc đổi tên `setup.php`.

### Cách B: Tạo thủ công

Copy file `api/config.sample.php` thành `api/config.php`, sau đó điền thông tin thật:

```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'ten_database');
define('DB_USER', 'ten_user_database');
define('DB_PASS', 'mat_khau_database');
define('ADMIN_KEY', 'doi-thanh-key-rieng-cua-thay');
```

Không đưa `api/config.php` có mật khẩu thật lên GitHub công khai.

## 4. Cấp tài khoản học sinh

Mở:

```text
admin.html
```

Nhập `ADMIN_KEY`, sau đó dùng mục **Cấp tài khoản học sinh**:

- Tài khoản: ví dụ `HS001`
- Mật khẩu: ví dụ `123456`
- Họ tên
- Lớp/Nhóm
- Chọn các trang được phép mở, mặc định là `Lộ trình tự học Toán 6`

## 5. Học sinh đăng nhập

Học sinh mở:

```text
login.html
```

Đăng nhập bằng tài khoản giáo viên đã cấp. Nếu là học sinh, hệ thống chuyển vào `lotrinh.html`; nếu là giáo viên, chuyển vào `index.html`.

## 6. Tự động deploy bằng GitHub Actions FTP

Workflow đã có ở:

```text
.github/workflows/ftp-deploy.yml
```

Vào GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**, tạo các secret:

```text
FTP_SERVER
FTP_USERNAME
FTP_PASSWORD
FTP_SERVER_DIR
```

Ví dụ `FTP_SERVER_DIR` thường là:

```text
/public_html/
```

hoặc nếu domain nằm trong thư mục riêng:

```text
/public_html/hoangthiencm.id.vn/
```

Workflow sẽ không upload `api/config.php`, nên cấu hình database thật trên hosting không bị ghi đè.


test deploy