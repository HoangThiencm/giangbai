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
- [x] Bổ sung hiển thị phần trăm tiến trình rõ ràng: sidebar có "Tiến độ bài hiện tại", header bài học có "Tiến trình học", và bảng "Kỹ năng của bài" hiển thị `0%`, `50%`, ... thay vì `--`.
- [x] Gia cố AI giải thích để tránh câu trả lời bị cụt giữa chừng: tăng `maxOutputTokens`, yêu cầu AI kết thúc câu trọn vẹn, nếu phản hồi có dấu hiệu bị ngắt thì gọi tiếp một lượt để nối phần thiếu.
- [x] Cập nhật bong bóng AI: phần thân bong bóng có `max-height: 320px` và cuộn dọc, để nội dung dài không bị tràn hoặc tạo cảm giác mất nội dung.

## Cần người dùng phản biện lại trên giao diện
- [ ] Mở lại AI giải thích ở đoạn lý thuyết: kiểm tra câu trả lời không còn dừng cụt kiểu "Khái"; nếu AI vẫn trả câu lửng, cần chụp lại nội dung mới để kiểm tra response thực tế từ Gemini.
- [ ] Vào tab Luyện tập khi chưa chọn đáp án: kiểm tra sidebar/header đã hiện phần trăm tiến trình bài học và bảng kỹ năng không còn `--`.
- [ ] Chọn từng đáp án trắc nghiệm: kiểm tra phần trăm tiến trình bài hiện tại tăng theo số câu đã làm, dấu đúng/sai hiện ngay, và kỹ năng đổi phần trăm tương ứng.

## Các công việc tiếp theo (To-do)
- [ ] Tiếp tục hoàn thiện phần bài tập thực hành (Luyện tập 1, 2, 3...) theo format Điền khuyết, Kéo thả và tự luận nâng cao.
- [ ] Kiểm tra thực tế phần tính điểm (`score`) và các chỉ số kỹ năng (`skill_scores_json`) trên dữ liệu nhiều bài học/học sinh để đảm bảo báo cáo giáo viên khớp UI học sinh.
- [ ] Mở rộng tính năng dùng module Gemini tự nhập key của riêng người dùng quản trị (bổ sung giao diện vào trang `admin.html`).
- [ ] Chăm chút thêm cho giao diện di động (Responsive) của các trang lộ trình.
