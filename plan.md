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
- [x] Sửa lại cách tính "Tiến độ chương": trước đây chỉ tăng khi bài đạt `mastered`, giờ tính trung bình phần trăm hoàn thành của các bài nên đánh dấu lý thuyết/ví dụ/luyện tập sẽ làm tiến trình tăng ngay.
- [x] Đổi nhãn trạng thái hoàn tất bài từ "Đã vững" sang "Đã học xong" để khớp với hành động người dùng bấm nút "Đã học".
- [x] Sửa bảng "Kỹ năng của bài" để phản ánh tiến độ học của chính bài: đánh dấu lý thuyết hiển thị tối thiểu 30%, đánh dấu ví dụ tối thiểu 50%, bấm "Đã học" toàn bài hiển thị 100% thay vì đứng yên 0%.
- [x] Sửa hành vi bài đã học xong: nếu tài khoản đã học xong bài thì UI hiển thị trạng thái "Đã học xong" và nút "Học lại"; bấm "Học lại" sẽ reset tiến trình bài đó để học sinh học lại từ đầu.
- [x] Đưa panel "Theo dõi tiến độ học sinh" vào giao diện giáo viên soạn bài (`lessonDesignerMount`) để giáo viên được cấp quyền dạy vẫn xem tiến độ mà không cần vào trang admin.
- [x] Mở API `api/admin_progress.php` cho giáo viên đang đăng nhập, ngoài admin key, để nhiều giáo viên có thể theo dõi tiến độ trong phạm vi giao diện giáo viên.
- [x] Render công thức Toán trong bảng theo dõi tiến độ của giáo viên: `admin-progress.js` xử lý LaTeX trong cột "Cần lưu ý", `index.html` và các trang lộ trình Toán đã có/nạp MathJax để không còn hiện raw như `$\mathbb{N}$`.
- [x] Gỡ "Theo dõi tiến độ" khỏi `admin.html` và tab admin; admin chỉ giữ các việc tổng quát như tạo bài học, tạo tài khoản và cài đặt hệ thống.

## Cần người dùng phản biện lại trên giao diện
- [ ] Mở lại AI giải thích ở đoạn lý thuyết: kiểm tra câu trả lời không còn dừng cụt kiểu "Khái"; nếu AI vẫn trả câu lửng, cần chụp lại nội dung mới để kiểm tra response thực tế từ Gemini.
- [ ] Vào tab Luyện tập khi chưa chọn đáp án: kiểm tra sidebar/header đã hiện phần trăm tiến trình bài học và bảng kỹ năng không còn `--`.
- [ ] Chọn từng đáp án trắc nghiệm: kiểm tra phần trăm tiến trình bài hiện tại tăng theo số câu đã làm, dấu đúng/sai hiện ngay, và kỹ năng đổi phần trăm tương ứng.
- [ ] Bấm "Đánh dấu đã học" ở lý thuyết hoặc "Đánh dấu đã xem ví dụ": kiểm tra "Tiến độ chương" và "Tiến độ bài hiện tại" tăng ngay sau khi lưu.
- [ ] Bấm nút "Đã học" trên header bài học: kiểm tra trạng thái chuyển "Đã học xong" và các thanh trong "Kỹ năng của bài" lên 100%.
- [ ] Đăng nhập bằng tài khoản giáo viên, vào giao diện soạn bài: kiểm tra có panel "Theo dõi tiến độ học sinh" ngay trong trang giáo viên và công thức trong cột "Cần lưu ý" được render.
- [ ] Đăng nhập admin: kiểm tra không còn tab/panel "Theo dõi tiến độ" trong admin.
- [ ] Với bài đã học xong, kiểm tra nút hiển thị "Học lại"; bấm vào thì bài quay về trạng thái đang học và tiến trình được reset.

## Các công việc tiếp theo (To-do)
- [ ] Tiếp tục hoàn thiện phần bài tập thực hành (Luyện tập 1, 2, 3...) theo format Điền khuyết, Kéo thả và tự luận nâng cao.
- [ ] Kiểm tra thực tế phần tính điểm (`score`) và các chỉ số kỹ năng (`skill_scores_json`) trên dữ liệu nhiều bài học/học sinh để đảm bảo báo cáo giáo viên khớp UI học sinh.
- [ ] Mở rộng tính năng dùng module Gemini tự nhập key của riêng người dùng quản trị (bổ sung giao diện vào trang `admin.html`).
- [ ] Chăm chút thêm cho giao diện di động (Responsive) của các trang lộ trình.
