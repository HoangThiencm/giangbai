# PLAN: Thêm Bộ Lọc Quản Lý Theo Lớp & Sửa Lỗi Sót Câu Khi Nhập Đề Word (thitructuyen.html)

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng
1. Giáo viên chưa có bộ lọc chọn theo Lớp trên thanh công cụ Quản lý thi.
2. Hàm isDuplicate trong exam-stitch-client.js xóa nhầm câu hỏi toán có mở đầu giống nhau, làm đề 20 câu Word bị tụt xuống 19 câu ở cột Tổng hợp.

## Phạm vi
1. **Thêm Bộ lọc Quản lý đề theo Lớp trong `TeacherDashboard`**:
   - Thêm dropdown `Lọc theo lớp` (`classFilter`) bên cạnh dropdown phân loại.
   - Hiển thị danh sách các lớp đã tạo đề + danh sách lớp được phân công giảng dạy.
   - Cập nhật logic `filteredExams` lọc chính xác theo lớp được chọn.
2. **Sửa dứt điểm Lỗi Nuốt Câu trong `exam-stitch-client.js`**:
   - Tinh chỉnh thuật toán `isDuplicate`: So sánh đồng thời cả `question` và `options.join('')` với độ tương đồng khắt khe (>98%), loại bỏ logic đếm index `t1[i] === t2[i]` sai lệch.
   - Đảm bảo khi nhập đề Word 20 câu thì cột Tổng hợp hiển thị đủ 100% 20/20 câu.
3. **Bộ kiểm thử tự động**:
   - Tạo/Cập nhật test `tests/exam-word-stitch-smoke.js` kiểm tra độ chính xác của bộ lọc lớp và xác nhận 20 câu Word được giữ nguyên 20 câu ở Tổng hợp.

## Ngoài phạm vi
- Không đổi cấu trúc lưu trữ đề thi trong cơ sở dữ liệu.
- Không đổi giao diện làm bài của học sinh (StudentView).

## File dự kiến tác động
- `thitructuyen.html`
- `exam-stitch-client.js`
- `tests/exam-word-stitch-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Sửa logic dedupe trong `exam-stitch-client.js`**:
   - Sửa hàm `isDuplicate` để không xóa nhầm câu hỏi khác biệt có tiền tố tương tự.
2. **Bước 2: Cập nhật UI & Logic lọc theo lớp trong `thitructuyen.html`**:
   - Thêm state `classFilter`, dropdown Lọc theo lớp, và điều kiện lọc trong `filteredExams`.
3. **Bước 3: Kiểm thử tự động**:
   - Chạy `node tests/exam-word-stitch-smoke.js`.

## Tiêu chí nghiệm thu
1. Thanh công cụ Quản lý thi có dropdown lọc theo từng Lớp mượt mà.
2. Nhập file Word 20 câu toán có LaTeX: Cột Chi tiết có 20 câu, cột Tổng hợp giữ nguyên 100% đúng 20/20 câu.
3. Bộ kiểm thử tự động pass 100%.
