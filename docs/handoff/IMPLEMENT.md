# IMPLEMENT: Xem công khai Quản lý văn bản và tab Chuyên môn

## Đã làm
- `access-control.js`: thêm `quanlyvanban-chuyenmon.html` vào `pageKeys`. Bốn trang văn bản được xem khi chưa có `authToken` (`isPublicVanbanPage`), không chuyển về `login.html`.
- `api/vanban.php`: `vbd_optional_user` cho `list`, `file`, `reminder_count`, `drive_check`. Khách nhận toàn bộ văn bản theo sector, `is_guest: true`, `user: null`. `action=file` đọc tệp hosting theo id trong CSDL khi không có phiên. Các action ghi vẫn gọi `vbd_current_user` (401 nếu chưa đăng nhập). Sector hợp lệ thêm `chuyenmon`, nhãn Chuyên môn, thư mục Drive `CHUYEN_MON`. Action `copy_from_hanhchinh` nhận `source_ids` (hoặc `document_ids`), sao chép văn bản `hanhchinh` sang `chuyenmon` cùng bản ghi tệp (giữ `drive_file_id` và URL). Khi xóa tệp Drive, nếu `drive_file_id` còn bản ghi khác thì chỉ bỏ liên kết CSDL.
- `vanban-hub.js` và `quanlyvanban.html`: thẻ Chuyên môn (icon `fa-graduation-cap`, indigo), lưới 3 cột, thống kê và nhắc việc theo sector, liên kết Đăng nhập giáo viên khi chưa có token.
- `quanlyvanban-chuyenmon.html`: trang lĩnh vực `window.VANBAN_SECTOR = 'chuyenmon'`. `quanlyvanban-hanhchinh.html` và `quanlyvanban-dang.html` dùng cùng `vanban-app.js`.
- `vanban-app.js`: `SECTOR_META.chuyenmon`, thanh Hành chính · Chuyên môn · Đảng. Khách ẩn Thêm văn bản, Tạo năm học, Lấy từ Hành chính, Sửa, Xóa, đổi trạng thái và xóa tệp; giữ lọc, xem chi tiết, xem tệp, Xuất Excel và nút Đăng nhập giáo viên. Đã đăng nhập ở Chuyên môn: nút Lấy từ Hành chính, modal lọc năm học / tìm kiếm / checkbox / Chọn tất cả / nhãn (Đã lấy), gửi `copy_from_hanhchinh` rồi tải lại danh sách.
- `teacher-lotrinh-nav.js`: `isVanbanPage()` nhận `quanlyvanban-chuyenmon.html`.

## Kiểm thử
- `node --check` trên `vanban-app.js`, `vanban-hub.js`, `access-control.js`, `teacher-lotrinh-nav.js` → ok.
- Máy không có `php` trong PATH nên chưa chạy `php -l`.
- Chưa mở trình duyệt. Bước sau: Antigravity IDE, chat mới, `/verify`.

## File
- `access-control.js`
- `teacher-lotrinh-nav.js`
- `quanlyvanban.html`
- `vanban-hub.js`
- `quanlyvanban-hanhchinh.html`
- `quanlyvanban-dang.html`
- `quanlyvanban-chuyenmon.html`
- `vanban-app.js`
- `api/vanban.php`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`
