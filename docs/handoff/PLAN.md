# PLAN: Tổng Hợp Dữ Liệu Biểu Mẫu Báo Cáo Thành Bảng Excel Mỗi Người Một Dòng & Tính Năng Xóa Bài Nộp Cho Phép Nộp Lại (nopbai-quanly.html)

## Hiện trạng
1. **Khảo sát hệ thống hiện tại**:
   - Trang `nopbai-quanly.html` đã hỗ trợ tính năng thiết kế biểu mẫu báo cáo (`submission_type === 'report'`) với các chỉ tiêu tùy chỉnh (như trong ảnh: *Họ và Tên GV, Năm sinh, Trình độ CM, Năm vào ngành, Phân công môn dạy, Lớp dạy, Ghi chú...*).
   - Cấu trúc các trường này được lưu trữ trong `submission_assignments.form_fields_json` (mỗi trường có `key`, `label`, `type`, `required`, `allow_evidence`...).
   - Trang nộp bài `nopbai.html` khi người dùng gửi biểu mẫu đã thu thập toàn bộ dữ liệu vào `report_data` (dạng JSON `{ [field.key]: "giá trị người dùng nhập" }`) và lưu an toàn vào bảng `assignment_submissions.report_data_json`.
   - Backend `api/submissions.php` (hàm `submission_rows_for_teacher`) khi trả về danh sách bài nộp đã tự động giải mã `report_data` thành đối tượng dữ liệu cho từng lượt nộp.
2. **Hai hạn chế cần khắc phục**:
   - **Hạn chế 1 (Xuất dữ liệu)**: Hàm `exportSubmissions()` hiện chỉ xuất file CSV tĩnh 7 cột mặc định, dồn tất cả dữ liệu các trường biểu mẫu vào một cột ghi chú duy nhất, chưa bóc tách thành các cột riêng biệt theo đúng biểu mẫu thiết kế và chưa có nút xuất tệp Excel `.xlsx`.
   - **Hạn chế 2 (Nộp lại & Xử lý trùng lặp)**: Khi một người đã nộp mà muốn nộp lại để sửa/bổ sung, hiện tại hệ thống chưa có nút **Xóa từng bài nộp riêng lẻ**. Nếu đợt nộp tắt "Cho nộp nhiều lần", hệ thống sẽ khóa không cho người đó nộp lại. Nếu bật "Cho nộp nhiều lần", họ nộp lại sẽ tạo thành 2 dòng bị trùng dữ liệu trong danh sách tổng hợp.

## Phạm vi
1. **Khẳng định giải pháp**:
   - **Hoàn toàn thực hiện được 100%**: Giáo viên có thể xóa bài nộp cũ của người đó để họ nộp lại một bài mới hoàn toàn, giữ cho danh sách tổng hợp Excel chỉ có duy nhất 1 dòng chuẩn xác cho mỗi người mà không bị trùng lặp.
2. **Nâng cấp chức năng xuất Excel tổng hợp trong `nopbai-quanly.html`**:
   - Tích hợp thư viện SheetJS (`xlsx.full.min.js`).
   - Tự động bóc tách các trường trong `form_fields`:
     * Các cột định danh: `STT`, `Họ tên người nộp`, `Vai trò`, `Tổ / Nhóm / Đơn vị`, `Mã định danh / SĐT`, `Thời gian nộp`.
     * **Mỗi trường biểu mẫu là một cột riêng biệt** (Ví dụ: Cột *Họ và Tên GV*, Cột *Năm sinh*, Cột *Trình độ CM*, Cột *Năm vào ngành*, Cột *Phân công môn dạy*, Cột *Lớp dạy*, Cột *Ghi chú*...).
     * Các cột phụ trợ: `Tệp đính kèm / Minh chứng`, `Ghi chú chung`.
   - **Mỗi người nộp là một dòng độc lập** trong Excel.
   - Thêm nút **"Xuất Excel (.xlsx)"** định dạng chuẩn đẹp, tự căn độ rộng cột, hiển thị tiếng Việt không bao giờ lỗi font.
3. **Bổ sung chức năng "Xóa bài nộp / Cho phép nộp lại"**:
   - Backend `api/submissions.php`: Thêm action `delete_submission` (xóa bài nộp trong `assignment_submission_files` và `assignment_submissions`, kiểm tra quyền sở hữu của giáo viên).
   - Frontend `nopbai-quanly.html`: Thêm nút icon thùng rác đỏ **"Xóa bài nộp (để cho nộp lại)"** ở từng dòng bài nộp trong modal `Kết quả`.
   - Khi xóa bài nộp:
     * Dữ liệu nộp cũ bị xóa sạch khỏi hệ thống.
     * Trạng thái người đó lập tức trở về **"Chưa nộp"**.
     * Người đó mở lại link nộp bài có thể nộp lại bình thường.
     * Danh sách tổng hợp Excel đảm bảo không còn dữ liệu trùng.

## Ngoài phạm vi
- Không thay đổi cấu trúc các bảng MySQL.
- Không xóa tệp minh chứng vật lý trên Google Drive để đảm bảo an toàn lưu trữ nếu cần tra soát.
- Không ảnh hưởng đến các đợt nộp tệp thông thường (`submission_type === 'file'`).

## File dự kiến tác động
- `api/submissions.php` [SỬA: Thêm action `delete_submission`]
- `nopbai-quanly.html` [SỬA: Thêm CDN SheetJS, nút xuất Excel động, nút Xóa từng bài nộp trong bảng kết quả]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch handoff cho Coder]
- `docs/handoff/.lock` [GHI: LOCK]

## Các bước thực hiện cho Coder
1. **Bước 1: Bổ sung action `delete_submission` vào `api/submissions.php`**:
   - Nhận `submission_id` qua POST.
   - Xác thực người gọi là giáo viên chủ sở hữu của đợt nộp tương ứng.
   - Chạy transaction xóa bản ghi trong `assignment_submission_files` và `assignment_submissions`.
   - Trả về thông báo thành công: *"Đã xóa bài nộp. Người này có thể nộp lại bình thường."*
2. **Bước 2: Bổ sung SheetJS vào `nopbai-quanly.html`**:
   - Thêm `<script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>` vào `<head>`.
3. **Bước 3: Thêm hàm `deleteSingleSubmission(submissionId, submitterName)` trong `nopbai-quanly.html`**:
   - Hiển thị hộp thoại xác nhận: *"Xóa bài nộp của [Tên]? Người này sẽ được phép nộp lại từ đầu và dữ liệu cũ sẽ không còn trong danh sách tổng hợp."*
   - Gọi API `delete_submission`, hiển thị toast thông báo và gọi lại `openDetail(currentAssignmentId)` để cập nhật bảng kết quả tức thì.
4. **Bước 4: Nâng cấp hàm xuất Excel `exportSubmissionsExcel()`**:
   - Trích xuất động các trường từ `form_fields` (bỏ qua `heading`).
   - Xây dựng mảng Header và Data Rows (mỗi người 1 dòng, dữ liệu map đúng cột).
   - Thiết lập độ rộng cột tự động (`!cols`) và xuất file `.xlsx` qua `XLSX.writeFile`.
5. **Bước 5: Cập nhật giao diện modal Kết quả (`renderDetail`)**:
   - Thêm nút xanh lá **"Xuất Excel (.xlsx)"** cạnh nút "Xuất CSV".
   - Thêm cột thao tác với nút **Xóa bài nộp** (<i class="fas fa-trash-can text-red-500"></i>) ở mỗi dòng bài nộp.
   - Hiển thị các cột biểu mẫu trực quan ngay trên bảng web.

## Rủi ro
- Xóa nhầm bài nộp -> Bắt buộc có hộp thoại xác nhận tên người nộp rõ ràng trước khi xóa.
- Quyền truy cập API -> Kiểm tra chặt chẽ giáo viên phải sở hữu đợt nộp mới được xóa.

## Cách kiểm thử
1. Tạo một đợt nộp biểu mẫu với 7 trường như ảnh.
2. Dùng 1 tài khoản/mã nộp thử 1 bài.
3. Vào trang quản lý, mở "Kết quả", bấm **"Xóa bài nộp"** của người đó -> Trạng thái chuyển thành "Chưa nộp".
4. Mở lại trang nộp bài bằng mã người đó -> Hệ thống cho phép nộp lại bài mới thành công.
5. Bấm **"Xuất Excel (.xlsx)"** -> Mở tệp kiểm tra danh sách chỉ có đúng 1 dòng của người đó với dữ liệu mới, các cột khớp đúng 7 trường đã thiết kế.

## Tiêu chí nghiệm thu
1. Người quản lý có thể xóa bài nộp riêng lẻ của từng người trực tiếp trên trang quản lý.
2. Sau khi xóa, người nộp mở link được phép nộp lại từ đầu mà không bị báo lỗi trùng lặp.
3. Xuất file Excel tổng hợp có mỗi người 1 dòng, các cột tương ứng đúng với biểu mẫu đã thiết kế.