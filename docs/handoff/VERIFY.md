# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Nhận diện bài Luyện tập chung / Ôn tập / Bài tập cuối chương: Đã thêm `isReviewOrPracticeLesson(topic)` trong `js/khbd-prompts.js` và đồng bộ sang `js/khbd-app.js`. ĐÚNG SCOPE.
- Xóa bỏ prompt leak `(Các YCCĐ của bài học...; mỗi ý một gạch đầu dòng...)`: Đã xóa khỏi template `GENERATE_OBJECTIVES` và thêm regex làm sạch triệt để trong `sanitizeLessonMarkdown`. ĐÚNG SCOPE.
- Chuyển đổi Mục B cho bài ôn tập: Đổi tiêu đề thành `## B. HOẠT ĐỘNG 2: LUYỆN TẬP (HỆ THỐNG HÓA KIẾN THỨC VÀ CHỮA CÁC BÀI TẬP TRỌNG TÂM TRONG SGK)` và chỉ dẫn chia nhánh theo bài tập SGK. ĐÚNG SCOPE.
- Chuyển đổi Mục C cho bài ôn tập: Đổi tiêu đề thành `## C. HOẠT ĐỘNG 3: LUYỆN TẬP NÂNG CAO VÀ VẬN DỤNG CÁC BÀI TẬP CÒN LẠI TRONG SGK`. ĐÚNG SCOPE.
- Chuẩn hóa Mục I (Mục tiêu) cho bài ôn tập: Tập trung củng cố kiến thức, giải bài tập SGK, khắc phục lỗi sai; cấm chép YCCĐ bài mới. ĐÚNG SCOPE.
- Nhãn tab động: Đã đồng bộ nhãn tab B thành `B. Luyện tập & Chữa bài tập SGK` khi gặp bài ôn/luyện tập. ĐÚNG SCOPE.
- Kiểm thử tự động mới: `tests/khbd-review-practice-lesson-smoke.js` đạt 100%. ĐÚNG SCOPE.
- Không thêm chức năng ngoài kế hoạch, không sửa file ngoài scope.

## Test đã chạy
- `node tests/khbd-review-practice-lesson-smoke.js` — PASS (nhận diện bài ôn tập, tiêu đề B/C, xóa leak template & sanitize).
- `node tests/soankhbd-generation-mode-smoke.js` — PASS (HTML IDs, chế độ soạn, 1-Click).
- `node tests/canvas-soankhbd-smoke.js` — PASS (tương thích Canvas 1-1).
- `node tests/baogiang-teacher-month-smoke.js` — PASS.
- `node tests/baogiang-weekday-segment-smoke.js` — PASS.
- `node tests/attendance-autosync-smoke.js` — PASS.

## Pass / Fail từng tiêu chí
- Nhận diện `isReviewOrPracticeLesson`: PASS.
- Đổi tiêu đề & chỉ dẫn Mục B, C: PASS.
- Mục tiêu kiến thức bài ôn tập: PASS.
- Xóa bỏ prompt leak template & sanitize: PASS.
- Nhãn tab động trên giao diện: PASS.
- Bộ test hồi quy hệ thống: PASS 100%.

## Bug
Không phát hiện bug còn tồn đọng.
