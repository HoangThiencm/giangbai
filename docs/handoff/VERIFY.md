# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Khóa cứng thời lượng 90 phút và Dedupe Hoạt động D (`js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - `PROMPTS.GENERATE_ACTIVITIES_AE` và `GENERATE_ACTIVITY_B` đã siết chặt quy tắc khóa thời lượng Hoạt động B = `{time_budget_B}` (45 phút chia 2 nhánh con là 23p và 22p; cấm 45p + 30p = 75p), và tổng cả bài A–E đúng bằng `{duration}` (02 tiết = đúng 90 phút).
   - `clipKhbdActivityMarkdown("D")` và `parseKhbdSections` đã dedupe triệt để để chỉ giữ lại đúng 1 khối Hoạt động D duy nhất.
   - `normalizeActivityTimeHeadings` tự động chuẩn hóa các phút trên tiêu đề A–E và các nhánh B khớp chính xác với `calculateActivityTimeBudgets`.
   - Khớp 100% scope trong PLAN.md.

2. **Triệt tiêu 7 trang dòng chấm trong Phụ lục F và file Word (`js/khbd-prompts.js`, `js/khbd-docx.js`, `js/khbd-app.js`)**:
   - `GENERATE_PORTFOLIO_WORKSHEETS` đã cấm sinh các khối dòng chấm rác kéo dài, khống chế phiếu học tập trình bày trong bảng hoặc tối đa 1–2 dòng chấm ngắn.
   - `collapseDottedLines` / `stripExcessiveDottedLines` trong `js/khbd-docx.js` và `js/khbd-app.js` đã tự động gom các khối dòng chấm liên tiếp ngoài bảng về tối đa 1 dòng, loại bỏ hoàn toàn hiện tượng phình thành 7 trang giấy trắng toàn dấu chấm trong file Word.
   - Khớp 100% scope trong PLAN.md.

## Test đã chạy
```
node tests/khbd-dotted-lines-smoke.js
node tests/khbd-activity-d-dedupe-smoke.js
node tests/khbd-activity-e-dedupe-smoke.js
node tests/khbd-time-budgets-smoke.js
node tests/khbd-sanitize-smoke.js
node tests/khbd-docx-format-smoke.js
node tests/khbd-docx-layout-smoke.js
node tests/khbd-table-columns-smoke.js
node tests/khbd-list-numbering-smoke.js
node tests/khbd-activity-e-smoke.js
node tests/khbd-pedagogy-script-smoke.js
```
- Tất cả 11 bài unit / smoke test trực tiếp và liên quan đều PASS 100%.

## Pass / Fail từng tiêu chí
1. **Tiêu chí 1**: Giáo án 2 tiết có tổng thời lượng các hoạt động A, B, C, D, E khớp chính xác 100% bằng 90 phút (Hoạt động B đúng 45 phút, các nhánh con cộng lại đúng 45 phút), không còn hiện tượng lặp lại Hoạt động D. -> **PASS**
2. **Tiêu chí 2**: Mục IV. Phụ lục F được trình bày gọn gàng, loại bỏ hoàn toàn hiện tượng sinh 7 trang giấy trắng toàn dòng chấm `.....` trong Word. -> **PASS**
3. **Tiêu chí 3**: Tất cả các bài kiểm thử tự động liên quan đều PASS 100%. -> **PASS**

## Bug
Không có.


