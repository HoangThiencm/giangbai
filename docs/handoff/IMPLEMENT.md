# IMPLEMENT: Nhận diện bài Luyện tập / Ôn tập — đổi Mục B/C, xóa prompt leak YCCĐ

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Module 1 — `js/khbd-prompts.js`
- Thêm `isReviewOrPracticeLesson(topic)` (regex: luyện tập chung / luyện tập / bài tập cuối chương / ôn tập chương / ôn tập / thực hành tổng hợp).
- Giữ alias `isPracticeOrReviewLesson` → gọi hàm mới (tương thích phân bổ thời lượng).
- `GENERATE_OBJECTIVES`: xóa dòng prompt leak `(Các YCCĐ của bài học theo CT GDPT 2018; mỗi ý một gạch đầu dòng, giữ động từ hành vi.)`.
- Khi bài ôn/luyện tập: bổ sung ràng buộc Mục I tập trung củng cố / hệ thống hóa / chữa bài tập SGK; CẤM chép YCCĐ kiểu bài mới.
- `GENERATE_ACTIVITY_B` (ôn tập): thay tiêu đề `HÌNH THÀNH KIẾN THỨC MỚI` → `LUYỆN TẬP (HỆ THỐNG HÓA KIẾN THỨC VÀ CHỮA CÁC BÀI TẬP TRỌNG TÂM TRONG SGK)`; chỉ dẫn chia 2.1, 2.2… theo bài tập SGK.
- `GENERATE_ACTIVITY_C` (ôn tập): tiêu đề → `LUYỆN TẬP NÂNG CAO VÀ VẬN DỤNG CÁC BÀI TẬP CÒN LẠI TRONG SGK`.
- Export `isReviewOrPracticeLesson` / alias trên `window`, `globalThis`, `module.exports`.

## Module 2 — `js/khbd-app.js`
- Đồng bộ `isReviewOrPracticeLesson` (+ alias).
- `sanitizeLessonMarkdown`: thêm regex gọt dòng/cụm `(Các YCCĐ...)` / `(mỗi ý một gạch đầu dòng...)`.
- `handle1ClickGenerate`: đã có sẵn bước tự đọc SGK khi `hasTextbookMedia() && !hasAnalyzedLessonContent()` với `{ internal: true }` — giữ nguyên.
- Nhãn động tab B: `getActivityTitleInfo` / `syncActivityBTabLabels`
  - Ôn/luyện tập: `B. Luyện tập & Chữa bài tập SGK` / `B. Hoạt động Luyện tập & Chữa bài tập SGK`
  - Ngược lại: giữ `B. Hình thành Kiến thức`
- Gọi sync từ `syncDraftDom` và `switchActivitySubtab`; export Word / tạo mục hiện tại dùng nhãn động.

## Module 3 — Smoke mới
- `tests/khbd-review-practice-lesson-smoke.js`: nhận diện topic, tiêu đề B/C, xóa leak template, sanitize, wiring 1-Click OCR nội bộ.

## Test đã chạy
- `node tests/khbd-review-practice-lesson-smoke.js` — PASS
- `node tests/soankhbd-generation-mode-smoke.js` — PASS
- `node tests/canvas-soankhbd-smoke.js` — PASS
- Thêm regression: `khbd-time-budgets-smoke.js`, `khbd-sanitize-smoke.js`, `khbd-tabs-reorganized-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity.
