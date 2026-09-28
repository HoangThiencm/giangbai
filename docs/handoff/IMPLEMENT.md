# IMPLEMENT: Sửa trang Quản lý văn bản trống và chặn admin

## Đã làm
- `api/vanban.php`: `vbd_current_user` vẫn từ chối khi chưa đăng nhập hoặc tài khoản không hoạt động. Vai trò được phép là `teacher`, `admin`, `superadmin`. Thông báo 403: «Chức năng quản lý văn bản chỉ dành cho giáo viên hoặc quản trị viên.»
- `vanban-hub.js`: `boot()` gọi `renderSummary()` rồi `renderSectors()` trước `load()`, nên 4 thẻ thống kê (số 0) và hai thẻ Hành chính / Đảng hiện ngay khi DOM sẵn sàng, kể cả khi `fetch` chưa xong.
- `quanlyvanban.html` tải `vanban-hub.js?v=20260928-fix-hub-render`. File hub local dài 9664 bytes (không rỗng).

## Kiểm thử
- Script Node tạm: DOM giả, `fetch` không bao giờ trả về. Sau khi chạy IIFE: `#summary` có 4 thẻ, `#sectorCards` có «Hành chính» và «Đảng» cùng link `quanlyvanban-hanhchinh.html` / `quanlyvanban-dang.html`. PASS.
- Máy này không có `php` trên PATH nên chưa chạy `php -l`.
- Không có trình duyệt trong phiên này. Chưa mở `hoangthiencm.id.vn/quanlyvanban.html` và chưa gọi API bằng tài khoản admin/giáo viên. File trên hosting chỉ đầy đủ sau khi FTP Deploy chạy từ commit đã push.

## Ngoài phạm vi
Không đổi schema, Google Drive, hay trang ngoài module quản lý văn bản.
