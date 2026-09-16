# IMPLEMENT: Tiết Luyện tập / Ôn tập đủ 4 hoạt động, B ≠ 0

Đã triển khai đúng PLAN.md:

- `calculateActivityTimeBudgets`: tiết Luyện tập/Ôn tập không còn `timeB = 0`. Phân bổ A 5–8 phút, B ~25% (22 phút/90p, 11 phút/45p), D ~10–12%, C phần còn lại ~55%, E = 0. Nhánh 2.1/2.2 chia đều B.
- Prompt Hoạt động B và 1-Click: khi `isPracticeOrReviewLesson` thì định hướng “Hệ thống hóa kiến thức trọng tâm & hướng dẫn giải ví dụ mẫu SGK”, đủ 4 bước và cột phải lời giải ví dụ.
- `canvas_soankhbd.html` giữ `gemini-3-flash-preview`; bản backup đồng bộ cùng model.
- Test: `khbd-time-budgets-smoke.js` (B=22, A+B+C+D=90, E=0); `canvas-soankhbd-smoke.js` khớp `gemini-3-flash-preview`.

File: `js/khbd-prompts.js`, `js/khbd-app.js`, `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`, `tests/khbd-time-budgets-smoke.js`, `tests/canvas-soankhbd-smoke.js`.
