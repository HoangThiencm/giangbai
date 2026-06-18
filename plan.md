# Kế hoạch dự án (Project Plan)

## Các công việc đã hoàn thành gần đây
- [x] Fix lỗi 500 khi lưu tiến độ bài học (do cột `state_json` chưa được tạo). Đã sửa file `api/lessons.php` tại hàm `ensure_progress_schema` bằng cách tách riêng biệt `try-catch` cho từng lần `ALTER TABLE`.
- [x] Cập nhật lại giao diện AI giải thích từ Popup Modal sang dạng **bong bóng chat theo ngữ cảnh**, xuất hiện ngay gần nút AI vừa bấm, có nút `x` để đóng, không bị cắt mũi/nội dung và vẫn render MathJax đúng.
- [x] Khắc phục tình trạng công thức Toán học MathJax SVG bị rớt dòng (xuống dòng vô tội vạ) bằng cách ghi đè class của Tailwind CSS (`mjx-container svg { display: inline !important; }`).
- [x] Tích hợp logic catch lỗi chi tiết ở Frontend: Bọc `try-catch` ở `markTheoryDone` và `markExamplesDone` trong `lotrinh.js` để thông báo cho người dùng khi lỗi (không bị crash ngầm). Thêm `?debug=1` vào request lưu tiến độ để hiện rõ lý do lỗi.
- [x] Thêm Content-Type JSON header vào `helpers.php` (hàm `respond`) để ngăn lỗi parse JSON ở Frontend.
- [x] Sửa `syncLessonState` để sau khi server lưu thành công, frontend cập nhật ngay `state.progress`; thanh tiến trình, trạng thái bài học, nhiệm vụ và kỹ năng không còn chờ reload mới thay đổi.
- [x] Sửa bài luyện tập trắc nghiệm: chọn đáp án xong hiện dấu đúng/sai, chuẩn hóa kiểu đáp án khi chấm để tránh lỗi so sánh số/chuỗi, và nộp bài cập nhật điểm + kỹ năng rõ ràng.
- [x] Sửa chức năng làm lại bài luyện: đổi nút thành "Làm lại bài luyện", reset đáp án/điểm luyện tập về trạng thái `in_progress` thay vì xóa toàn bộ tiến trình học.

## Các công việc tiếp theo (To-do)
- [ ] Tiếp tục hoàn thiện phần bài tập thực hành (Luyện tập 1, 2, 3...) theo format Điền khuyết, Kéo thả và tự luận nâng cao.
- [ ] Kiểm tra thực tế phần tính điểm (`score`) và các chỉ số kỹ năng (`skill_scores_json`) trên dữ liệu nhiều bài học/học sinh để đảm bảo báo cáo giáo viên khớp UI học sinh.
- [ ] Mở rộng tính năng dùng module Gemini tự nhập key của riêng người dùng quản trị (bổ sung giao diện vào trang `admin.html`).
- [ ] Chăm chút thêm cho giao diện di động (Responsive) của các trang lộ trình.
