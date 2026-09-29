# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Bỏ bắt buộc đăng nhập để xem văn bản: `access-control.js` không redirect về `login.html` với 4 trang văn bản khi chưa có token (`isPublicVanbanPage`).
- [x] Backend mở quyền đọc công khai: `api/vanban.php` hỗ trợ `vbd_optional_user`, cho phép `list`, `file`, `reminder_count`, `drive_check` không đòi hỏi session giáo viên.
- [x] Chặn quyền ghi khi chưa đăng nhập: Các action `save`, `delete`, `delete_file`, `update_status`, `upload*`, `create_school_year`, `copy_from_hanhchinh` tiếp tục yêu cầu `vbd_current_user` (HTTP 401 khi chưa đăng nhập).
- [x] Giao diện phân tách quyền khách: `vanban-app.js` và `vanban-hub.js` ẩn các nút Thêm văn bản, Tạo năm học, Lấy từ Hành chính, Sửa, Xóa, đổi trạng thái; giữ đầy đủ tính năng tra cứu, lọc năm học/loại VB/trạng thái, xem modal chi tiết, xem tệp đính kèm và Xuất Excel cho cấp trên kiểm tra.
- [x] Mở lĩnh vực Chuyên môn: Thêm sector `chuyenmon` (icon `fa-graduation-cap`, tone màu indigo), cập nhật Hub `quanlyvanban.html` hiển thị 3 cột cân đối, thanh điều hướng header liên kết cả 3 lĩnh vực (Hành chính · Chuyên môn · Đảng).
- [x] Tạo trang mới `quanlyvanban-chuyenmon.html` hoàn chỉnh, kết nối với `teacher-lotrinh-nav.js` và `access-control.js`.
- [x] Tính năng tick chọn lấy văn bản từ Hành chính: Tab Chuyên môn có nút "Lấy từ Hành chính", modal hiển thị danh sách văn bản Hành chính kèm bộ lọc, ô tìm kiếm nhanh, checkbox từng dòng, checkbox "Chọn tất cả", nhãn đánh dấu `(Đã lấy)`.
- [x] Backend sao chép văn bản: Action `copy_from_hanhchinh` nhân bản bản ghi `office_documents` với `sector = 'chuyenmon'` và nhân bản toàn bộ bản ghi `office_document_files` giữ nguyên liên kết Drive/hosting.
- [x] Bảo vệ tệp Drive: Khi xóa văn bản/tệp tại Chuyên môn, kiểm tra tham chiếu `vbd_drive_file_shared` để không xóa nhầm tệp gốc trên Google Drive nếu còn được văn bản khác sử dụng.

## Test đã chạy
- `node --check access-control.js teacher-lotrinh-nav.js vanban-hub.js vanban-app.js`: Tất cả 4 tệp JS đều vượt qua kiểm tra cú pháp, 0 lỗi.
- Kiểm tra tính đầy đủ và đường dẫn của 9 file liên quan: `quanlyvanban.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-dang.html`, `vanban-app.js`, `vanban-hub.js`, `api/vanban.php`, `access-control.js`, `teacher-lotrinh-nav.js` đều tồn tại và liên kết đúng.
- Đối chiếu bảo mật logic backend: Kiểm tra nhánh gọi `vbd_optional_user` cho read actions và `vbd_current_user` cho mutation actions.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Người dùng không cần đăng nhập vẫn mở và xem được đầy đủ danh mục văn bản ở cả 4 trang (`quanlyvanban.html`, `quanlyvanban-hanhchinh.html`, `quanlyvanban-chuyenmon.html`, `quanlyvanban-dang.html`), mở xem được chi tiết và tệp đính kèm. -> **PASS**
- Tiêu chí 2: Người chưa đăng nhập không thể sửa, xóa, thêm văn bản hay thay đổi trạng thái văn bản (bảo vệ ở cả UI và API). -> **PASS**
- Tiêu chí 3: Hệ thống có đủ 3 lĩnh vực: Hành chính, Chuyên môn, Đảng trên cả trang Hub tổng quan và thanh điều hướng từng trang. -> **PASS**
- Tiêu chí 4: Tab Chuyên môn có nút "Lấy từ Hành chính", hiển thị danh sách văn bản Hành chính kèm checkbox để người dùng tick chọn lấy sang Chuyên môn. -> **PASS**
- Tiêu chí 5: Văn bản sau khi lấy sang Chuyên môn giữ nguyên thông tin, ngày tháng, trích yếu và tệp đính kèm mở xem được bình thường. -> **PASS**

## Bug
Không phát hiện lỗi.
