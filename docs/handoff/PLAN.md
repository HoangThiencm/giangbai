# PLAN: Tổng Hợp Dữ Liệu Biểu Mẫu Báo Cáo Thành Bảng Excel Mỗi Người Một Dòng (nopbai-quanly.html)

## Hiện trạng
1. **Khảo sát hệ thống hiện tại**:
   - Trang `nopbai-quanly.html` đã hỗ trợ tính năng thiết kế biểu mẫu báo cáo (`submission_type === 'report'`) với các chỉ tiêu tùy chỉnh (như trong ảnh: *Họ và Tên GV, Năm sinh, Trình độ CM, Năm vào ngành, Phân công môn dạy, Lớp dạy, Ghi chú...*).
   - Cấu trúc các trường này được lưu trữ trong `submission_assignments.form_fields_json` (mỗi trường có `key`, `label`, `type`, `required`, `allow_evidence`...).
   - Trang nộp bài `nopbai.html` khi người dùng gửi biểu mẫu đã thu thập toàn bộ dữ liệu vào `report_data` (dạng JSON `{ [field.key]: "giá trị người dùng nhập" }`) và lưu an toàn vào bảng `assignment_submissions.report_data_json`.
   - Backend `api/submissions.php` (hàm `submission_rows_for_teacher`) khi trả về danh sách bài nộp đã tự động giải mã `report_data` thành đối tượng dữ liệu cho từng lượt nộp.
2. **Hạn chế cần khắc phục**:
   - Trong `nopbai-quanly.html` (dòng 486), hàm `exportSubmissions()` hiện chỉ xuất file CSV tĩnh với 7 cột cố định (`Họ tên, Vai trò, Nhóm/đơn vị, Mã/SĐT/email, Thời gian, Ghi chú, Tệp`). Toàn bộ dữ liệu các trường biểu mẫu người dùng nhập vào đang bị dồn cục vào 1 cột văn bản nối nhau bằng dấu gạch ` | ` hoặc bị bỏ quên.
   - Hệ thống chưa có nút xuất tệp Excel `.xlsx` chuyên nghiệp (mới chỉ có xuất `.csv`).
   - Bảng xem trước "Bài đã nhận" trên giao diện web cũng đang gộp tất cả các chỉ tiêu vào một cột duy nhất `Nội dung/Ghi chú`, gây khó khăn cho việc đối soát trực quan.

## Phạm vi
1. **Khẳng định giải pháp**:
   - **Hoàn toàn thực hiện được 100%** và nền tảng dữ liệu đã sẵn sàng đáp ứng.
2. **Nâng cấp chức năng xuất Excel tổng hợp trong `nopbai-quanly.html`**:
   - Tích hợp thư viện SheetJS (`xlsx.full.min.js`) — thư viện chuẩn đã dùng xuyên suốt hệ thống GiangBai (`thitructuyen.html`, `thoikhoabieu.html`, `xaydungphuluc.html`).
   - Nâng cấp logic xuất bảng tổng hợp:
     + Khi đợt nộp là **Báo cáo biểu mẫu** (`submission_type === 'report'`):
       * Cột cố định định danh: `STT`, `Họ tên người nộp`, `Vai trò`, `Tổ / Nhóm / Đơn vị`, `Mã định danh / SĐT`, `Thời gian nộp`.
       * **Mỗi trường mà người quản lý thiết kế sẽ tự động trở thành một cột riêng biệt** (Ví dụ đúng như ảnh: Cột *Họ và Tên GV*, Cột *Năm sinh*, Cột *Trình độ CM*, Cột *Năm vào ngành*, Cột *Phân công môn dạy*, Cột *Lớp dạy*, Cột *Ghi chú*).
       * Cột thông tin bổ sung: `Tệp đính kèm / Minh chứng`, `Ghi chú chung`.
     + **Mỗi người nộp là một dòng độc lập** trong Excel, các giá trị người dùng nhập được điền chính xác vào đúng cột tương ứng.
     + Cung cấp 2 lựa chọn xuất: **"Xuất Excel (.xlsx)"** (chuẩn đẹp, tự động căn độ rộng cột, không bao giờ lỗi font tiếng Việt) và **"Xuất CSV"** (dành cho các hệ thống nhập liệu phụ trợ).
3. **Cải tiến bảng xem trước "Bài đã nhận" trên giao diện Web (modal Kết quả)**:
   - Khi xem một đợt nộp dạng biểu mẫu, bảng hiển thị động các cột tương ứng với các chỉ tiêu đã thiết kế, giúp giáo viên/quản lý có thể xem dạng lưới bảng tính ngay trên trình duyệt mà không bắt buộc phải tải file về máy.

## Ngoài phạm vi
- Không thay đổi cấu trúc bảng cơ sở dữ liệu MySQL (giữ nguyên bảng `submission_assignments`, `assignment_submissions`, `assignment_submission_files`).
- Không thay đổi quy trình nộp bài của người dùng trên `nopbai.html`.
- Không ảnh hưởng đến các đợt nộp tệp thông thường (`submission_type === 'file'`).

## File dự kiến tác động
- `nopbai-quanly.html` [SỬA: Thêm CDN SheetJS, cập nhật hàm render bảng chi tiết và hàm xuất Excel/CSV động theo trường biểu mẫu]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch handoff cho Coder]
- `docs/handoff/.lock` [GHI: LOCK]

## Các bước thực hiện cho Coder
1. **Bước 1: Bổ sung thư viện SheetJS vào `nopbai-quanly.html`**:
   - Thêm thẻ `<script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>` vào phần `<head>`.
2. **Bước 2: Xây dựng hàm trích xuất cấu trúc cột động**:
   - Viết hàm `getAssignmentReportColumns(assignment)`:
     + Lấy mảng trường từ `assignment.form_fields` (hoặc parse `assignment.form_fields_json`).
     + Lọc bỏ các mục `type === 'heading'`.
     + Trả về mảng các cột gồm `{ key, label, type }`.
3. **Bước 3: Nâng cấp hàm xuất Excel `exportSubmissionsExcel()`**:
   - Tạo mảng tiêu đề cột (Headers):
     `['STT', 'Họ tên', 'Vai trò', 'Tổ / Nhóm / Đơn vị', 'Mã / SĐT / Email', 'Thời gian nộp', ...customLabels, 'Tệp minh chứng / Đính kèm', 'Ghi chú']`
   - Tạo mảng dòng dữ liệu (Data rows):
     + Duyệt từng lượt nộp `s` trong `submissions`:
       * Cột cơ bản: `index + 1`, `s.submitter_name`, `s.submitter_role`, `s.group_name`, `s.identifier`, `fmt(s.submitted_at)`
       * Các cột dữ liệu biểu mẫu: lấy trực tiếp từ `s.report_data?.[col.key] || ''`
       * Cột tệp: ghép link xem file từ `(s.files || []).map(f => f.view_url).join('\n')`
       * Cột ghi chú: `s.note || ''`
   - Dùng `XLSX.utils.aoa_to_sheet(rows)` để tạo Worksheet.
   - Tự động thiết lập độ rộng cột (`!cols`) để bảng tính thoáng đẹp, dễ đọc.
   - Tạo Workbook và gọi `XLSX.writeFile(wb, \`tong-hop-\${a.public_code}.xlsx\`)`.
4. **Bước 4: Cập nhật giao diện modal Kết quả (`renderDetail`)**:
   - Thêm nút bấm xanh lá `<button onclick="exportSubmissionsExcel()" class="rounded-lg bg-emerald-700 px-3 py-2 text-xs font-bold text-white hover:bg-emerald-800"><i class="fas fa-file-excel mr-1"></i>Xuất Excel (.xlsx)</button>`.
   - Điều chỉnh bảng HTML hiển thị các cột biểu mẫu nếu đợt nộp là `report`.

## Rủi ro
- Một số đợt nộp cũ hoặc đợt nộp dạng tệp (`file`) không có `form_fields` -> Cần kiểm tra điều kiện an toàn (`if (reportCols.length === 0)`), tự động quay về cấu trúc cột mặc định để không gây lỗi.
- Người dùng nhập dữ liệu số hoặc ngày tháng -> Cần định dạng text an toàn để không bị Excel hiểu sai định dạng ngày tháng.

## Cách kiểm thử
1. Mở `nopbai-quanly.html`, tạo một đợt nộp với 7 trường đúng như ảnh chụp của người dùng:
   - Họ và Tên GV (Văn bản ngắn)
   - Năm sinh (Văn bản ngắn)
   - Trình độ CM (Văn bản ngắn)
   - Năm vào ngành (Văn bản ngắn)
   - Phân công môn dạy (Văn bản ngắn)
   - Lớp dạy (Văn bản ngắn)
   - Ghi chú (Văn bản ngắn)
2. Mở link đợt nộp trên `nopbai.html` và nhập thử 2 bài nộp với các thông tin mẫu khác nhau.
3. Quay lại `nopbai-quanly.html`, mở "Kết quả" của đợt nộp.
4. Bấm **"Xuất Excel (.xlsx)"** và mở file bằng Excel / Google Sheets:
   - Kiểm tra mỗi người là 1 dòng riêng biệt.
   - Kiểm tra 7 cột trường dữ liệu tương ứng hiển thị chuẩn xác từng trường.
   - Tiếng Việt hiển thị sắc nét, chuẩn Unicode.

## Tiêu chí nghiệm thu
1. Xác nhận chắc chắn với người dùng: Hệ thống hoàn toàn làm được và tổng hợp cực kỳ chuẩn xác.
2. File Excel xuất ra có cấu trúc cột động khớp 100% với các trường người dùng thiết lập trong biểu mẫu.
3. Mỗi người nộp là một dòng dữ liệu tương ứng.