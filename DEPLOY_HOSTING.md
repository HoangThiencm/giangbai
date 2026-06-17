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

Copy file:

```text
api/config.sample.php
```

thành:

```text
api/config.php
```

Sau đó điền thông tin thật:

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
