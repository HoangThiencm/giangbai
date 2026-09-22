# IMPLEMENT: Duyệt giáo án theo tổ chuyên môn

## Phạm vi đã thực hiện

- `api/duyetgiaoan.php`: thêm `get_department_teachers`, dùng `state.teachers` của kế hoạch phân công mới nhất (hoặc `plan_id` được chọn), chuẩn hóa phân công môn/lớp; `get_ppct_catalog` kiểm tra giáo viên có trong kế hoạch trước khi đọc PPCT của chính giáo viên đó.
- `duyetgiaoan.html`: đồng bộ giáo viên từ tổ, tự nạp PPCT theo giáo viên/môn/khối, tách giáo án thành bài, duyệt tuần tự từng bài (mỗi lời gọi AI tối đa 5.000 ký tự), có heuristic CV 5512 và fallback khi AI lỗi.
- Kết quả lưu theo từng bài trong `session_data` v2, vẫn tải được dữ liệu đợt cũ; xuất biên bản tổ có mục I–V và bảng tám cột, chỗ ký TTCM/BGH.
- `tests/duyetgiaoan-department-smoke.js`: kiểm tra các điểm tích hợp mới.

## Kiểm thử đợt này

- PASS: `node tests/duyetgiaoan-department-smoke.js`
- PASS: `node tests/duyetgiaoan-smoke.js`
- PASS: `node tests/duyetgiaoan-integration-smoke.js`
- `git diff --check` phát hiện khoảng trắng cuối dòng đã có trong `docs/handoff/PLAN.md`; không sửa vì nằm ngoài phạm vi triển khai.
- Không chạy PHP lint vì môi trường hiện tại không có PHP CLI.

## Phạm vi đã thực hiện trước đó

- `api/khbd_ppct_catalog.php`, `api/canvas_ppct_catalog.php`: migration idempotent thêm `school_name`, khóa duy nhất gồm trường, GET danh sách hồ sơ khi không truyền trường, GET/PUT/DELETE theo trường.
- `js/khbd-app.js`: lưu cache PPCT theo trường, chuyển nhanh hồ sơ, đưa `school_name` vào tải/lưu/xuất/nhập và đồng bộ danh sách bài học.
- Khi chưa có trường được chọn, tự mở hồ sơ đầu tiên từ server; PPCT cũ chưa đặt tên còn dữ liệu luôn được giữ nguyên.
- `soankhbd.html`, `canvas_soankhbd.html`: thêm dropdown trường, ô nhập trường và danh sách chọn/xóa hồ sơ trong modal.
- `tests/khbd-ppct-multi-school-smoke.js`: kiểm tra hai PPCT cùng môn/lớp/năm không ghi đè và chuyển trường nạp đúng dữ liệu.

## Kiểm thử

- PASS: `node tests/khbd-ppct-multi-school-smoke.js`
- PASS: `node tests/khbd-ppct-integration-smoke.js`
- PASS: `git diff --check`
- Không chạy PHP lint vì môi trường hiện tại không có PHP CLI.
