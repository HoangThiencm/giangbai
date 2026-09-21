# IMPLEMENT: Tối Ưu Hóa Giao Diện Thi Trực Tuyến

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

- Thêm `ExamSettingsModal` trong `thitructuyen.html`: thời lượng/khung giờ, chống gian lận, thí sinh, số lần thi và định dạng đề.
- Thêm nút **Cài đặt** cùng badge thời lượng/lớp; modal cập nhật trực tiếp `examInfo`.
- Tinh gọn thanh công cụ, giữ **Lưu Đề** xanh nổi bật và hỗ trợ cuộn ngang khi thiếu không gian.
- Không thay đổi `handleSave` hay payload lưu đề.

## Kiểm tra

- Kiểm tra cấu trúc Babel script: PASS.
- Biên dịch toàn bộ JSX trong `thitructuyen.html` bằng Babel Standalone 7.26.4: PASS.

## Còn lại

- Cần kiểm thử trực quan trình duyệt theo `docs/handoff/VERIFY.md`.
