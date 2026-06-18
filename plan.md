# Kế hoạch dự án (Project Plan)

## Các công việc đã hoàn thành gần đây
- [x] Fix lỗi 500 khi lưu tiến độ bài học (do cột `state_json` chưa được tạo). Đã sửa file `api/lessons.php` tại hàm `ensure_progress_schema` bằng cách tách riêng biệt `try-catch` cho từng lần `ALTER TABLE`.
- [x] Chuyển đổi giao diện hiển thị AI giải thích từ dạng inline "bong bóng" (bị lỗi cắt xén nội dung do `overflow: hidden`) sang dạng **Popup Modal** mượt mà, bao gồm backdrop làm mờ, header, nút đóng, và hiển thị trọn vẹn cả nội dung text và công thức toán MathJax.
- [x] Khắc phục tình trạng công thức Toán học MathJax SVG bị rớt dòng (xuống dòng vô tội vạ) bằng cách ghi đè class của Tailwind CSS (`mjx-container svg { display: inline !important; }`).
- [x] Tích hợp logic catch lỗi chi tiết ở Frontend: Bọc `try-catch` ở `markTheoryDone` và `markExamplesDone` trong `lotrinh.js` để thông báo cho người dùng khi lỗi (không bị crash ngầm). Thêm `?debug=1` vào request lưu tiến độ để hiện rõ lý do lỗi.
- [x] Thêm Content-Type JSON header vào `helpers.php` (hàm `respond`) để ngăn lỗi parse JSON ở Frontend.

## Các công việc tiếp theo (To-do)
- [ ] Tiếp tục hoàn thiện phần bài tập thực hành (Luyện tập 1, 2, 3...) theo format Điền khuyết, Trắc nghiệm, Kéo thả.
- [ ] Tích hợp sâu hơn và kiểm tra kĩ phần tính điểm (`score`) và các chỉ số kỹ năng (`skill_scores_json`) theo từng bài học.
- [ ] Mở rộng tính năng dùng module Gemini tự nhập key của riêng người dùng quản trị (bổ sung giao diện vào trang `admin.html`).
- [ ] Chăm chút thêm cho giao diện di động (Responsive) của các trang lộ trình.
