# IMPLEMENT: Nhập Thời khóa biểu Word và đối chiếu giáo viên

**Ngày thực hiện:** 2026-11-17
**Phạm vi:** Triển khai đúng `docs/handoff/PLAN.md` trong `phancongtochuyenmon.html`.

## Đã thực hiện

- Bổ sung vùng nạp/kéo thả file `.docx` trong khu vực nhập thời khóa biểu; giữ nguyên luồng nhập ảnh hiện có.
- Dùng `mammoth.js` đã có để đổi Word thành HTML, mở rộng bảng có `rowspan`/`colspan`, tìm từng bảng giáo viên, và cố định 5 hàng dữ liệu sau mỗi tiêu đề buổi sáng/chiều thành 5 tiết tương ứng.
- Thêm modal đối chiếu: checkbox, chọn lại giáo viên từ CSDL, chọn nhanh, trạng thái khớp, và lưu bí danh vào `localStorage` với khóa `tkb_word_aliases`.
- So khớp tên có dấu nghiêm ngặt (không dùng hàm bỏ dấu), do đó `Thiên` và `Thiện` là hai tên khác nhau.
- Thêm Engine A nạp trực tiếp: chuẩn hóa lớp theo danh mục, kiểm tra dải tiết, lớp chưa có trong CSDL, và xung đột cùng lớp/cùng tiết; sau khi xác nhận sẽ lưu TKB và đồng bộ phân công môn.
- Thêm Engine B: sinh prompt kèm dữ liệu bảng nguồn cho các giáo viên đã chọn, sao chép một chạm, và nạp lại JSON AI sau khi kiểm tra schema/qui tắc.

## Kiểm tra đã chạy

- Kiểm tra cú pháp toàn bộ JavaScript nhúng bằng Node: đạt (`JavaScript syntax OK`).
- Kiểm tra whitespace/diff cho `phancongtochuyenmon.html`: đạt.
- Đọc cấu trúc file Word mẫu được cung cấp: xác nhận có 50 bảng Word và các nhãn `Giáo viên …`, `Buổi sáng`, `Buổi chiều`, `THỨ 2`–`THỨ 7` phù hợp với bộ tách bảng.
- Sửa lỗi hiển thị lặp tên: tên giáo viên nay được đọc từ ô tiêu đề Word nguyên gốc, trước khi xử lý các ô gộp `colspan`/`rowspan`.
- Sửa ánh xạ tiết buổi chiều: hàng kế tiếp trong Word tiếp tục theo tiết đầu của khung chiều (ví dụ sau 7–9 là tiết 10), không bị gán sai về tiết 4.
- Rà soát các điểm tích hợp: input Word, modal, parser, ghép CSDL/bí danh, nạp trực tiếp, prompt AI và nạp JSON đều có liên kết sự kiện.

## Cần kiểm thử giao diện

- Dùng file TKB Word thực tế có bảng của giáo viên `Thiên` và `Thiện`, kiểm tra hai hàng được tách riêng và chọn đúng giáo viên trong CSDL.
- Thử nạp trực tiếp, kiểm tra 5 hàng buổi sáng/chiều không bị dồn tiết.
- Thử lưu bí danh, tải lại trang rồi nhập lại file để kiểm tra tự ghép.
