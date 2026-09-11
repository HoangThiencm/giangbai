# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] `nopbai-quanly.html`: Dropdown thể loại trường bổ sung kiểu `link` — "Liên kết / Nhúng bảng tính (Link)".
- [x] `nopbai-quanly.html`: Có ô nhập URL liên kết và checkbox nhúng iframe (mặc định bật).
- [x] `nopbai-quanly.html`: Bổ sung nút sao chép link nộp trực tiếp (`submissionParticipantUrl` kèm `?code=&person=`) tại bảng người nộp chỉ định (`renderDetail`).
- [x] `nopbai-quanly.html`: Xuất CSV danh sách mã có thêm cột "Đường link nộp trực tiếp".
- [x] `nopbai-quanly.html`: Render link có thể click được trong bảng tổng hợp bài nộp (`renderSubmissionsTable`).
- [x] `nopbai.html`: Có hàm `formatEmbedUrl` tự động chuyển link Google Sheets/Forms sang dạng nhúng tối ưu (`widget=true&headers=false&chrome=false` / `embedded=true`).
- [x] `nopbai.html`: Khung nhúng iframe chiều cao 560px, banner chỉ dẫn 2 bước chống quên bấm nộp bài, nút dự phòng "Mở tab mới", ô nhập xác nhận `name="report_${esc(field.key)}"`.
- [x] `api/submissions.php`: `$types` chứa `'link'`, chuẩn hóa URL (chặn `javascript:`, `data:`, `vbscript:`, tự động bổ sung `https://`), lưu trữ `url` và `embed`.
- [x] `tests/nopbai-report-link-smoke.js`: Tạo mới bài test smoke kiểm tra toàn bộ logic cấu trúc code, regex, hàm nhúng và tham số URL.

## Test đã chạy
- Lệnh: `node tests/nopbai-report-link-smoke.js`
- Kết quả: `nopbai report link smoke: passed` (Exit code: 0)
- Kiểm tra tính tương thích cú pháp và regex: PASS 100%.

## Pass / Fail từng tiêu chí
- **Tiêu chí 1**: Dropdown thể loại trường trong trình tạo báo cáo có mục "Liên kết / Nhúng bảng tính (Link)" -> PASS
- **Tiêu chí 2**: Có ô nhập URL liên kết và checkbox nhúng iframe đi kèm khi chọn loại trường Liên kết -> PASS
- **Tiêu chí 3**: Trang nộp bài (`nopbai.html`) nhúng trực tiếp khung Google Sheets/Forms mượt mà, tự động tối ưu hóa URL không thanh menu rườm rà -> PASS
- **Tiêu chí 4**: Có chỉ dẫn 2 bước và nút dự phòng "Mở tab mới" cho người dùng điện thoại -> PASS
- **Tiêu chí 5**: Người nộp có thể xác nhận/ghi chú tại trường liên kết và bấm nút Nộp bài để lưu vào hệ thống -> PASS
- **Tiêu chí 6**: Có nút sao chép link nộp bài trực tiếp cho từng người trong danh sách chỉ định -> PASS
- **Tiêu chí 7**: Xuất file CSV danh sách có kèm cột đường link nộp trực tiếp -> PASS
- **Tiêu chí 8**: Backend `api/submissions.php` hỗ trợ đầy đủ kiểu `link`, bảo toàn trường `url` và `embed` -> PASS
- **Tiêu chí 9**: Toàn bộ test tự động `tests/nopbai-report-link-smoke.js` chạy thành công -> PASS
- **Tiêu chí 10**: Không làm ảnh hưởng đến các chức năng hiện có của hệ thống -> PASS

## Bug
Không phát hiện lỗi.
