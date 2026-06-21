# Quản lý văn bản giáo viên

## Chức năng

- Giáo viên có tab **Quản lý văn bản** trong thanh điều hướng.
- Năm học do giáo viên tự tạo trong giao diện; mỗi văn bản bắt buộc thuộc một
  năm học đã khai báo.
- Quản lý văn bản đến/đi, số ký hiệu, ngày, nơi gửi/nhận, trích yếu và tệp đính kèm.
- Đặt hạn báo cáo và xác nhận trạng thái: Chưa xử lý, Đang xử lý, Đã báo cáo.
  Nếu quá hạn mà chưa hoàn thành, giao diện tự hiển thị Quá hạn.
- Tệp văn bản lưu trên Google Drive; MySQL chỉ lưu danh mục, trạng thái và liên kết tệp.
- Với PDF, trình duyệt trích chữ tối đa 12 trang. Nội dung được gửi từ hosting tới
  Cloudflare Worker để AI gợi ý số/ký hiệu, ngày văn bản, hạn báo cáo và đầu việc.
  Không sử dụng HuggingFace.

## Triển khai

Upload các file sau lên thư mục gốc/hosting tương ứng:

- `quanlyvanban.html`
- `api/vanban.php`
- `access-control.js`
- `teacher-lotrinh-nav.js`
- `cloudflare-worker/worker.js` (dán lại và Deploy trên Cloudflare)

Google Drive dùng đúng cấu hình đã có trong `api/config.php`:

```php
define('GOOGLE_DRIVE_CREDENTIALS_JSON', '{...}');
define('GOOGLE_DRIVE_TOKEN_JSON', '{...}'); // để trống nếu dùng Service Account
define('GOOGLE_DRIVE_ROOT_FOLDER_ID', '...');
define('GOOGLE_DRIVE_SHARE_MODE', 'private');
```

Lần đầu gọi `api/vanban.php`, hệ thống tự tạo hai bảng MySQL:
`office_documents` và `office_document_files`.

Tệp được xếp trong Drive theo cấu trúc:

```text
04_QUAN_LY_VAN_BAN/
└── NAM_HOC_YYYY-YYYY/
    ├── VAN_BAN_DEN/
    └── VAN_BAN_DI/
```

Khi xóa một văn bản, giao diện hiện cảnh báo số tệp sẽ bị xóa. Sau khi xác nhận,
hệ thống xóa cả danh mục MySQL lẫn toàn bộ tệp đính kèm của văn bản trên Google Drive.
