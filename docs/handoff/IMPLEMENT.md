# IMPLEMENT: Quản lý nhiều bản kế hoạch phụ lục

## Phạm vi đã triển khai

- Nâng cấp API bản nháp sang nhiều bản lưu cho mỗi tài khoản. Migration chỉ gỡ index giới hạn `uniq_user_phuluc_draft_user`, thêm metadata `title`, `appendix_type`, `summary` và các index hỗ trợ; không xóa bảng, dòng, hay `draft_data` cũ.
- Bản nháp cũ được gắn nhãn từ metadata đã lưu để hiển thị trong danh sách mà không thay đổi nội dung bản nháp.
- Thêm API danh sách, tải theo ID, lưu mới/cập nhật bản đang mở và xóa có kiểm tra quyền sở hữu theo `user_id`.
- Nhánh cập nhật xác minh bản lưu thuộc tài khoản trước khi ghi, nên lưu lại dữ liệu không đổi vẫn thành công thay vì nhầm là không tìm thấy.
- Thêm modal lưu với môn, lớp, năm học, trường, tổ chuyên môn, tên kế hoạch và thống kê PPCT/AI/phụ lục; tách rõ Lưu bản mới và Cập nhật bản đang mở.
- Thêm modal quản lý/tải với bộ lọc môn, lớp, năm học, tìm theo tên, cùng các nút Mở và Xóa có xác nhận.
- Bổ sung trạng thái bản nháp đang làm việc và mở rộng smoke test cho phần tử, hàm và API đa bản lưu.

## File đã sửa

- `api/user_phuluc_draft.php`
- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS
- PHP syntax check — không chạy được vì môi trường không có lệnh `php` trên PATH.

## Vấn đề còn lại

- Chưa thực hiện kiểm thử thủ công với CSDL và phiên đăng nhập thật.
- Chưa commit hoặc push theo yêu cầu.
