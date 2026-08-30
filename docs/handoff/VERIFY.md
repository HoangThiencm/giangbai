# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Chuẩn hóa 4 Hoạt động (A–D) theo Công văn 5512 (`js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - `calculateActivityTimeBudgets(..., { fourActivities: true })` phân bổ 100% thời lượng cho 4 hoạt động A + B + C + D (ví dụ 02 tiết 90 phút: A = 8p, B = 45p, C = 25p, D = 12p; tổng đúng 90 phút).
   - `GENERATE_ACTIVITIES_AD` và `GENERATE_ACTIVITY_D` đã tích hợp trọn vẹn 4 nhiệm vụ tự học ở nhà (ôn tập, bài tập SGK/SBT còn lại, chuẩn bị bài mới, tìm tòi mở rộng) vào Bước 4 của Hoạt động D.
   - `getFullLessonPlanMarkdown` ưu tiên ghép chuẩn 4 hoạt động A–D khi Hoạt động D đã bao gồm hướng dẫn tự học.
   - Khớp 100% scope trong PLAN.md.

2. **Xử lý Nhúng Ảnh & Fallback Chú thích Hình vẽ trong Word (`js/khbd-docx.js`)**:
   - `createIllustrationParagraphs`, `parseMarkdownToDocxElements` và `parseTableCellParagraphs` đã hỗ trợ xử lý marker `![caption](khbd-ill:id)`:
     * Khi đã có ảnh: Nhúng ảnh `ImageRun` căn lề giữa sắc nét.
     * Khi chưa vẽ ảnh / không có dữ liệu ảnh: Tự động chuyển đổi thành dòng chú thích in nghiêng thanh lịch `*(Hình vẽ minh họa: [caption])*`, loại bỏ 100% hiện tượng in chuỗi mã thô `![...](khbd-ill:id)` ra file Word.
   - Khớp 100% scope trong PLAN.md.

## Test đã chạy
```
node tests/khbd-activities-ad-standard-smoke.js
node tests/khbd-docx-illustration-fallback-smoke.js
node tests/khbd-time-budgets-smoke.js
node tests/khbd-activity-e-dedupe-smoke.js
node tests/khbd-activity-d-dedupe-smoke.js
node tests/khbd-docx-format-smoke.js
node tests/khbd-illustrations-smoke.js
node tests/khbd-recommendation-flow-smoke.js
node tests/khbd-dotted-lines-smoke.js
node tests/khbd-table-columns-smoke.js
node tests/khbd-list-numbering-smoke.js
```
- Tất cả 11 bài unit / smoke test trực tiếp và liên quan đều PASS 100%.

## Pass / Fail từng tiêu chí
1. **Tiêu chí 1**: Chuẩn hóa trọn vẹn 4 hoạt động A, B, C, D theo đúng Công văn 5512, tích hợp đầy đủ nhiệm vụ về nhà và mở rộng thực tế vào Hoạt động D; tổng thời gian các hoạt động đúng 100% theo số tiết khai báo (02 tiết = đúng 90 phút). -> **PASS**
2. **Tiêu chí 2**: File Word xuất ra nhúng đúng ảnh khi đã vẽ, hoặc hiển thị dòng chú thích `*(Hình vẽ minh họa: ...)*` lịch sự khi chưa vẽ ảnh, loại bỏ 100% mã thô `![...](khbd-ill:id)`. -> **PASS**
3. **Tiêu chí 3**: Toàn bộ các bài kiểm thử liên quan đều PASS 100%. -> **PASS**

## Bug
Không có.




