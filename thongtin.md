# Thông tin dự án

## Cấu trúc hiện tại của dự án
Dự án được xây dựng dựa trên stack: HTML, CSS (Tailwind), JS thuần ở phía Frontend và PHP (PDO) + MySQL ở phía Backend.

### Các file và chức năng chính
1. **Giao diện bài học (`lotrinhtoan6.html`, `lotrinhtoan7.html`, `lotrinhtoan8.html`, `lotrinhtoan9.html`)**
   - Chứa cấu trúc HTML cho lộ trình học môn Toán các lớp.
   - Định dạng CSS nội bộ (`<style>`) giúp render MathJax SVG và popup Modal AI giải thích.

2. **Logic Frontend (`lotrinh.js`)**
   - Quản lý trạng thái học tập của học sinh.
   - Gửi yêu cầu lưu tiến độ lên Server (`syncLessonState`).
   - Xử lý các tương tác AI: `bindAiExplainButtons`, `showAiModal`.
   - Kết xuất giao diện dựa trên dữ liệu (tiến độ, nội dung lý thuyết, bài tập).

3. **Backend API (`api/`)**
   - `lessons.php`: Quản lý lấy danh sách bài học, và **lưu tiến độ** (trạng thái `started_at`, `completed_at`, `state_json`, ...). Đã có cơ chế auto-migrate cột database độc lập (`ensure_progress_schema`) sử dụng từng khối try-catch riêng.
   - `ai_explain.php`: Chịu trách nhiệm gọi API LLM (Gemini) để sinh text giải thích dựa trên nội dung và ngữ cảnh. Trả về định dạng JSON súc tích.
   - `helpers.php`: Gồm các hàm tiện ích chung (`respond()`, `column_exists()`, `mysql_datetime_or_null()`).

## Vấn đề cần lưu ý (Notes)
- **MathJax & Tailwind:** Tailwind CSS mặc định thiết lập `svg { display: block; }`, điều này làm vỡ các công thức inline của MathJax. Dự án khắc phục bằng cách thiết lập cẩn thận thuộc tính `display: inline !important` cho `mjx-container svg`.
- **Database Schema:** Chức năng lưu tiến độ học phụ thuộc vào bảng `student_lesson_progress`. Việc tự động thêm cột (`ALTER TABLE`) có thể gặp rủi ro nếu quyền Database không đủ. Đã bọc `try-catch` độc lập cho từng cột để tránh làm sập luồng.
- **AI Explain:** Đầu ra từ AI cần được loại bỏ markdown thô trước khi hiển thị. Frontend gọi `typesetMath()` trên Modal sau khi chèn text để đảm bảo công thức toán học được render đúng chuẩn.
- **Trạng thái lưu trữ:** Lỗi "Unknown column 'state_json'" (Error 500) đã được khắc phục hoàn toàn bằng bản vá auto-migrate an toàn.

---
*File này được tạo và cập nhật nhằm mục đích đồng bộ thông tin trạng thái dự án khi chuyển đổi môi trường làm việc.*
