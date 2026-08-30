# IMPLEMENT: Xóa E cũ, Tab E Hồ sơ / Tab F Hình minh họa, phân bổ thời lượng động

## Phạm vi đã triển khai

- Giữ nguyên `docs/handoff/PLAN.md` và `docs/handoff/.lock`.
- Không đổi 4 bước CV 5512, TT 02, QĐ 2422.

### `soankhbd.html`

- Subtab Tab 4: A Mở đầu, B Hình thành Kiến thức, C Luyện tập, D Vận dụng & Hướng dẫn tự học, **E. Hồ sơ học tập**, **🎨 F. Hình minh họa SGK**.
- Xóa nhãn "E. Hướng dẫn về nhà".
- Panel `activityIllustrationCard` / `illustrationGalleryAct` cho subtab F.

### `js/khbd-prompts.js`

- `calculateActivityTimeBudgets` mặc định 4 hoạt động: A 7–10% (3–12p), D 12–15% (5–25p); phần còn lại chia B/C theo số tiểu mục N=1..4; A+B+C+D = T; tổng nhánh B = B.
- Chế độ 5 pha chỉ khi `{ fourActivities: false }` hoặc `mode: "ae"`.
- `GENERATE_PORTFOLIO_WORKSHEETS` gắn subtab E (`# E. HỒ SƠ...`).

### `js/khbd-app.js`

- `ACTIVITY_TITLES` đúng A–F mới.
- `switchActivitySubtab("F")` hiện gallery, ẩn editor markdown.
- Tạo E = `GENERATE_PORTFOLIO_WORKSHEETS`; tạo F = `generateLessonIllustrations`.
- `getFullLessonPlanMarkdown`: III = A–D; IV = `activities.E` (bỏ E cũ nếu là hướng dẫn về nhà).
- `migrateLegacyActivitiesPortfolio`: nếu F có nội dung và E rỗng → chuyển F sang E; xóa E kiểu "Hướng dẫn về nhà".

### `js/khbd-docx.js`

- `exportFullLessonPlan` bổ sung phụ lục từ `activities.E` nếu markdown chưa có mục IV.

### Kiểm thử

- Thêm `tests/khbd-dynamic-time-budgets-smoke.js`.
- Thêm `tests/khbd-tabs-reorganized-smoke.js`.

## Kiểm thử đã chạy

- `node tests/khbd-dynamic-time-budgets-smoke.js` — PASS
- `node tests/khbd-tabs-reorganized-smoke.js` — PASS
- `node tests/khbd-time-budgets-smoke.js` — PASS
- `node tests/khbd-activities-ad-standard-smoke.js` — PASS
- `node tests/khbd-docx-illustration-fallback-smoke.js` — PASS
- `node tests/khbd-illustrations-smoke.js` — PASS

## Vấn đề còn lại

- Không có trong phạm vi này. Cần `/verify` trên Tab 4: E = Hồ sơ, F = Hình minh họa, không còn E về nhà; bài 1 tiết / 3 tiết tổng A+B+C+D đúng phút.
