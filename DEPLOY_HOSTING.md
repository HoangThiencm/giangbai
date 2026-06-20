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

Đăng nhập bằng tài khoản giáo viên đã cấp. Nếu là học sinh, hệ thống chuyển vào lộ trình được mở, ví dụ `lotrinhtoan6.html`, `lotrinhtoan7.html`, `lotrinhtoan8.html` hoặc `lotrinhtoan9.html`; nếu là giáo viên, chuyển vào `index.html`.

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

## 7. Thi trực tuyến (MySQL trên hosting)

Đề thi và kết quả học sinh lưu trên hosting qua `api/exam.php` (không còn Supabase).

1. Chạy thêm SQL trong `database_schema.sql` (bảng `exams`, `exam_submissions`) — hoặc mở `thitructuyen.html` một lần, API sẽ tự tạo bảng nếu thiếu.
2. Upload `api/exam.php` và `thitructuyen.html` mới.
3. Giáo viên cần **đăng nhập** (`login.html`) trước khi soạn đề / xem kết quả — API dùng session PHP.
4. Học sinh làm bài qua link QR **không cần đăng nhập** (chỉ `get` đề + `submit` kết quả).
5. Chức năng **AI quét PDF / nhận diện câu** vẫn gọi HuggingFace (`omr_backend_url` trong localStorage nếu cần đổi URL).

**Lưu ý:** Đề và kết quả cũ trên Supabase/HuggingFace không tự chuyển sang MySQL — cần soạn lại hoặc nhập tay nếu muốn giữ dữ liệu cũ.

## 8. Giao và nhận bài (Google Drive + hosting PHP)

Mô-đun này không dùng backend Hugging Face. Trang quản lý là `nopbai-quanly.html`,
trang dành cho người nộp là `nopbai.html`, API chạy tại `api/submissions.php`.
Thông tin đợt nộp và trạng thái được lưu trong MySQL; tệp thật được tải thẳng từ
hosting lên Google Drive.

### Cấu hình Google Drive

1. Bật **Google Drive API** trong Google Cloud Console.
2. Chọn một trong hai cách xác thực:
   - **OAuth Client** (phù hợp Drive cá nhân): dùng JSON OAuth Client và token JSON có `refresh_token`.
   - **Service Account** (phù hợp Google Shared Drive): chia sẻ thư mục/Shared Drive cho email service account với quyền Editor. Service Account thường không có dung lượng Drive cá nhân, vì vậy nên dùng Shared Drive.
3. Lấy ID thư mục gốc từ URL Google Drive.
4. Thêm vào `api/config.php` trên hosting:

```php
define('GOOGLE_DRIVE_CREDENTIALS_JSON', '{...JSON credentials đầy đủ...}');
define('GOOGLE_DRIVE_TOKEN_JSON', '{...JSON có refresh_token...}'); // để trống nếu dùng Service Account
define('GOOGLE_DRIVE_ROOT_FOLDER_ID', 'id-thu-muc-goc');
define('GOOGLE_DRIVE_SHARE_MODE', 'private');
define('SUBMISSION_MAX_FILE_MB', 25);
```

Giữ `GOOGLE_DRIVE_SHARE_MODE` là `private` để tệp kế thừa quyền của thư mục Drive.
Chỉ dùng `anyone` nếu mọi tệp đều được phép công khai cho bất kỳ ai có đường link.

Hosting PHP cần bật các extension `openssl`, `curl`, `fileinfo` và cho phép kết nối
HTTPS ra `oauth2.googleapis.com`, `www.googleapis.com`. Đồng thời đặt `upload_max_filesize`
và `post_max_size` lớn hơn giới hạn tệp muốn nhận.

Các bảng `submission_assignments`, `submission_participants`, `assignment_submissions`
và `assignment_submission_files` có trong `database_schema.sql`. API cũng tự tạo các
bảng này lần đầu được mở để thuận tiện khi nâng cấp hệ thống đang chạy.

### Các kiểu người nộp

- **Tự do:** ai có link cũng nộp được, tự khai họ tên, vai trò, đơn vị và thông tin nhận diện.
- **Theo lớp/nhóm:** lấy tài khoản hiện có của lớp/nhóm và cấp mã cá nhân.
- **Danh sách chỉ định:** chọn tài khoản sẵn có hoặc nhập thêm học sinh, phụ huynh,
  giáo viên, cán bộ và người ngoài hệ thống. Người chưa có tài khoản dùng mã cá nhân,
  không cần đăng ký tài khoản mới.
