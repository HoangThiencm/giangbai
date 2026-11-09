# IMPLEMENT: Smart Bridge thoát Zalo / In-App Browser

## Phạm vi đã thực hiện

- `api/short_links.php`: thêm và tự nâng cấp cột `escape_inapp`; API danh sách, tạo và cập nhật link đều đọc/ghi thuộc tính này, mặc định bật.
- `s.php`: nhận diện In-App Browser; giữ chuyển hướng 302 cho trình duyệt thường hoặc link đã tắt Smart Bridge; trả Android Intent cho Android và màn hình hướng dẫn/sao chép/mở Chrome cho iOS.
- `rutgon.html`: bổ sung tùy chọn bật/tắt, huy hiệu “Thoát Zalo”, thông tin Smart Bridge và nút xem thử trong hộp QR.

## Kiểm thử

- `git diff --check`: đạt, không có lỗi khoảng trắng.
- Đã thử chạy `php -l api/short_links.php` và `php -l s.php`, nhưng môi trường hiện không có lệnh PHP trong `PATH`.

## Lưu ý

- Chưa kiểm thử end-to-end vì cần cơ sở dữ liệu và thiết bị/WebView Zalo thực tế.
