# IMPLEMENT: Tối ưu PPCT và lưu/tải bản nháp Phụ lục 5512

## Phạm vi đã triển khai

- Giữ nguyên tối ưu nhập liệu PPCT hiện có: sửa ô cập nhật trực tiếp dữ liệu, preview được gộp theo khung hình kế tiếp, picker tiết AI gom nhóm bằng `Map`, và cache YCCĐ/NLS/AI được giữ nguyên.
- Thêm `api/user_phuluc_draft.php`: xác thực bằng `$_SESSION['user_id']`, tự khởi tạo bảng `user_phuluc_drafts`, tải bản nháp mới nhất bằng `GET` và lưu/cập nhật một bản nháp cho mỗi tài khoản bằng `POST`.
- Bản nháp lưu cấu hình sư phạm, PPCT nguồn/bảng nguồn, thiết bị/phòng/đánh giá, các tiết AI đã chọn, ngữ cảnh SGK, cơ sở tri thức SGK và kết quả Phụ lục 1, 2, 3.
- Bổ sung nút `💾 Lưu lên CSDL`, `📂 Tải từ CSDL`, trạng thái thời điểm lưu; khi mở trang hệ thống kiểm tra bản nháp và hỏi người dùng trước khi nạp.
- Bổ sung smoke assertions cho endpoint và cấu trúc dữ liệu bản nháp.

## File đã sửa/tạo

- `api/user_phuluc_draft.php` (mới)
- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `php -l api/user_phuluc_draft.php` — không chạy được vì môi trường hiện không có PHP CLI.
- `git diff --check` — PASS

## Vấn đề còn lại

- Chưa thể thực hiện kiểm thử thủ công với CSDL/session trên môi trường hiện tại; endpoint đã có xử lý 401 cho người chưa đăng nhập và kiểm thử cú pháp cần chạy lại ở máy chủ có PHP CLI.
- Chưa commit hoặc push theo yêu cầu.
