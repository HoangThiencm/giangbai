# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **API Backend đa bản lưu (`api/user_phuluc_draft.php`)**:
   - Migration gỡ bỏ `UNIQUE KEY uniq_user_phuluc_draft_user`, bổ sung các cột `title`, `appendix_type`, `summary`, thêm index `idx_user_phuluc_drafts_user` và `idx_user_phuluc_drafts_mon_lop`.
   - Hỗ trợ đầy đủ các endpoint: `GET ?action=list` (kèm lọc `mon_hoc`, `lop`, `nam_hoc`), `GET ?id={id}`, `POST` (lưu mới / cập nhật có kiểm tra quyền sở hữu `user_id`), `POST ?action=delete` / `DELETE`.
   - Dữ liệu `draft_data` cũ của người dùng được bảo toàn 100% và tự động gắn nhãn tiêu đề hiển thị.
2. **Giao diện & Modal Quản lý Lưu / Tải (`xaydungphuluc.html`)**:
   - Đã thêm `#saveDraftModal` với đầy đủ Môn học, Khối lớp, Năm học, Tên trường, Tổ chuyên môn, trường nhập Tên kế hoạch, Tóm tắt thống kê và 2 lựa chọn "Lưu thành bản mới" / "Cập nhật bản đang mở".
   - Đã thêm `#loadDraftModal` với bộ lọc Môn học, Khối lớp, Năm học, ô tìm kiếm nhanh, danh sách bản lưu trực quan cùng nút "Mở" và "Xóa".
   - Quản lý trạng thái bản nháp đang mở (`currentDraftId`, `currentDraftTitle`) và hiển thị chi tiết trên `#draftStatus`.
3. **Bộ kiểm thử tự động (`tests/xaydungphuluc-smoke.js` & `tests/xaydungphuluc-integration-smoke.js`)**:
   - Bao phủ toàn bộ các hàm quản lý bản lưu, schema DB đa bản lưu, các phần tử modal UI mới.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\to$ PASS
- `node tests/xaydungphuluc-integration-smoke.js` $\to$ PASS

## Pass / Fail từng tiêu chí
- [x] Bảng `user_phuluc_drafts` cho phép mỗi tài khoản lưu nhiều bản kế hoạch độc lập, có đầy đủ metadata Môn học, Lớp, Năm học, Tiêu đề, Tóm tắt: PASS
- [x] Bấm "Lưu lên CSDL" mở modal xác nhận đầy đủ Môn, Lớp, Năm học, cho phép đặt tên và chọn Lưu mới / Cập nhật: PASS
- [x] Bấm "Tải từ CSDL" mở modal danh sách các bản lưu có bộ lọc theo Môn, Lớp, Năm học, hiển thị ngày giờ, cho phép Mở và Xóa: PASS
- [x] Thanh trạng thái hiển thị rõ ràng bản kế hoạch đang làm việc và thời gian đồng bộ CSDL: PASS
- [x] 100% kiểm thử tự động `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` chạy đạt PASS: PASS

## Bug
*(Không có)*
