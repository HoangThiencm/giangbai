# Thông tin dự án

## Cấu trúc hiện tại của dự án
Dự án được xây dựng dựa trên stack: HTML, CSS (Tailwind), JS thuần ở phía Frontend và PHP (PDO) + MySQL ở phía Backend.

### Các file và chức năng chính
1. **Giao diện bài học (`lotrinhtoan6.html`, `lotrinhtoan7.html`, `lotrinhtoan8.html`, `lotrinhtoan9.html`)**
   - Chứa cấu trúc HTML cho lộ trình học môn Toán các lớp.
   - Định dạng CSS nội bộ (`<style>`) giúp render MathJax SVG và bong bóng chat AI giải thích.
   - Đã thêm style `.ai-chat-bubble` đồng bộ cho cả Toán 6, 7, 8, 9; bong bóng có nút `x`, mũi nhọn chat, và không bị cắt nội dung.

2. **Logic Frontend (`lotrinh.js`)**
   - Quản lý trạng thái học tập của học sinh.
   - Gửi yêu cầu lưu tiến độ lên Server (`syncLessonState`) và cập nhật `state.progress` tại client ngay sau khi lưu thành công.
   - Xử lý các tương tác AI: `bindAiExplainButtons`, `showAiModal`; hiện tại `showAiModal` thực chất render bong bóng chat gần nút vừa bấm thay vì modal phủ toàn màn hình.
   - Kết xuất giao diện dựa trên dữ liệu (tiến độ, nội dung lý thuyết, bài tập).
   - Bài luyện tập trắc nghiệm hiển thị dấu đúng/sai ngay sau khi học sinh chọn đáp án; đáp án được chuẩn hóa kiểu dữ liệu để `1` và `"1"` đều chấm đúng.
   - Nút làm lại bài luyện chỉ reset phần luyện tập, giữ tiến trình học lý thuyết/ví dụ và cập nhật lại giao diện ngay.
   - Tiến trình bài hiện tại được tính theo các mốc: lý thuyết 30%, ví dụ 20%, luyện tập 50% theo tỷ lệ số câu đã làm. Giá trị này hiển thị ở sidebar và header bài học.
   - Tiến độ chương được tính bằng trung bình phần trăm hoàn thành của các bài trong lộ trình, không chỉ dựa vào số bài `mastered`; vì vậy đánh dấu đã học từng phần sẽ làm thanh tiến trình chương thay đổi.
   - Bảng kỹ năng không còn hiển thị `--` khi học sinh vào luyện tập; mặc định hiển thị `0%`, lấy tiến độ hoàn thành bài làm mức tối thiểu, và cập nhật theo thao tác đánh dấu/nộp bài.

3. **Backend API (`api/`)**
   - `lessons.php`: Quản lý lấy danh sách bài học, và **lưu tiến độ** (trạng thái `started_at`, `completed_at`, `state_json`, ...). Đã có cơ chế auto-migrate cột database độc lập (`ensure_progress_schema`) sử dụng từng khối try-catch riêng.
   - `ai_explain.php`: Chịu trách nhiệm gọi API LLM (Gemini) để sinh text giải thích dựa trên nội dung và ngữ cảnh. Trả về định dạng JSON súc tích. Đã tăng giới hạn token, yêu cầu câu cuối kết thúc trọn vẹn và tự gọi tiếp một lượt nếu phản hồi có dấu hiệu bị ngắt.
   - `helpers.php`: Gồm các hàm tiện ích chung (`respond()`, `column_exists()`, `mysql_datetime_or_null()`).

## Vấn đề cần lưu ý (Notes)
- **MathJax & Tailwind:** Tailwind CSS mặc định thiết lập `svg { display: block; }`, điều này làm vỡ các công thức inline của MathJax. Dự án khắc phục bằng cách thiết lập cẩn thận thuộc tính `display: inline !important` cho `mjx-container svg`.
- **Database Schema:** Chức năng lưu tiến độ học phụ thuộc vào bảng `student_lesson_progress`. Việc tự động thêm cột (`ALTER TABLE`) có thể gặp rủi ro nếu quyền Database không đủ. Đã bọc `try-catch` độc lập cho từng cột để tránh làm sập luồng.
- **AI Explain:** Đầu ra từ AI cần được loại bỏ markdown thô trước khi hiển thị. Frontend gọi `typesetMath()` sau khi chèn text vào bong bóng chat để đảm bảo công thức toán học được render đúng chuẩn. Bong bóng được gắn theo ngữ cảnh nút vừa bấm và người dùng có thể đóng bằng nút `x`.
- **AI Explain - điểm cần kiểm tra:** Nếu bong bóng vẫn hiện câu bị cụt, cần phân biệt hai nguyên nhân: CSS che mất nội dung hay Gemini trả response bị ngắt. Hiện frontend đã cho thân bong bóng cuộn dọc, backend đã thêm cơ chế nối tiếp khi câu trả lời chưa kết thúc bằng dấu câu.
- **Trạng thái lưu trữ:** Lỗi "Unknown column 'state_json'" (Error 500) đã được khắc phục hoàn toàn bằng bản vá auto-migrate an toàn.
- **Tiến trình học:** `syncLessonState` hiện cập nhật lại `state.progress` ở frontend sau khi API lưu thành công. Nhờ vậy thanh tiến trình, trạng thái bài, nhiệm vụ hằng ngày và bảng kỹ năng phản hồi ngay, không phụ thuộc hoàn toàn vào lần reload dữ liệu tiếp theo.
- **Tiến trình bài hiện tại:** Không dùng `score` làm đại diện duy nhất cho tiến trình học nữa. Frontend có `lessonCompletionPercent()` để tính tiến trình học theo hoạt động đã hoàn thành và `practiceProgress()` để tính tỷ lệ câu luyện tập đã làm.
- **Tiến độ chương:** `renderOverallProgress()` hiện lấy trung bình `lessonCompletionPercent()` của các bài đang hiển thị. Dòng phụ vẫn cho biết số bài đã học xong trên tổng số bài.
- **Trạng thái hoàn tất:** Trạng thái `mastered` trên UI được hiển thị là "Đã học xong" để phản hồi đúng hành động bấm nút "Đã học".
- **Kỹ năng của bài:** `renderSkills()` hiện hiển thị tối thiểu bằng `lessonCompletionPercent()`, nên học sinh đánh dấu đã học lý thuyết/ví dụ/toàn bài sẽ thấy thanh kỹ năng của bài thay đổi ngay, không đứng yên 0%.
- **Bài luyện tập:** Trắc nghiệm đã có phản hồi đúng/sai sau khi chọn đáp án; thao tác nộp bài cập nhật điểm, kỹ năng và trạng thái (`in_progress`, `needs_practice`, `mastered`). Nút "Làm lại bài luyện" reset đáp án/điểm luyện tập về trạng thái đang học để học sinh có thể làm lại.
- **Cần phản biện sau sửa:** Người dùng nên kiểm tra lại 3 điểm trên UI: AI có còn trả câu cụt không, tab Luyện tập có hiện phần trăm thay vì `--` không, và phần trăm có tăng khi chọn đáp án không.

---
*File này được tạo và cập nhật nhằm mục đích đồng bộ thông tin trạng thái dự án khi chuyển đổi môi trường làm việc.*
