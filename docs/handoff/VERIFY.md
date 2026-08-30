# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Khắc phục định dạng gạch dưới `_Trạm X:_` và rò rỉ dòng bảng trong Word (`js/khbd-docx.js`, `js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - `parseInlineTextToRuns` trong `js/khbd-docx.js` đã nhận diện và bóc tách đầy đủ cú pháp `_..._` (in nghiêng) và `__...__` (in đậm) thành docx `TextRun`, không còn xuất thô các ký tự gạch dưới `_`.
   - `parseMarkdownToDocxElements` và `sanitizeLessonMarkdown` đã tự động lọc bỏ các dòng pipe rác/separator bảng rò rỉ (`|`, `---`).
   - Khớp 100% scope trong PLAN.md.

2. **Khóa chuẩn thời lượng Hoạt động B và toàn bộ bài dạy (`js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - `PROMPTS.GENERATE_ACTIVITY_B` đã bổ sung `{time_budget_B}` vào tiêu đề: `## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI ({time_budget_B})`.
   - Prompt đã bổ sung quy tắc khóa cứng: Tổng thời gian các nhánh con trong B phải đúng bằng `{time_budget_B}` và tổng toàn bài (A + B + C + D + E) khớp chính xác 100% với `{duration}` (02 tiết = đúng 90 phút).
   - Khớp 100% scope trong PLAN.md.

## Test đã chạy
```
node tests/khbd-docx-format-smoke.js
node tests/khbd-time-budgets-smoke.js
node tests/khbd-sanitize-smoke.js
node tests/khbd-docx-layout-smoke.js
node tests/khbd-docx-math-smoke.js
node tests/khbd-table-columns-smoke.js
node tests/khbd-list-numbering-smoke.js
node tests/khbd-activity-e-smoke.js
node tests/khbd-pedagogy-script-smoke.js
```
- Tất cả unit / smoke tests trực tiếp và liên quan đều PASS 100%.

## Pass / Fail từng tiêu chí
1. **Tiêu chí 1**: File Word xuất ra hiển thị định dạng in nghiêng chuẩn mực, bóc sạch ký tự gạch dưới `_Trạm X:_` và không rò rỉ đường kẻ/dấu pipe thừa. -> **PASS**
2. **Tiêu chí 2**: Tiêu đề Hoạt động B và toàn bộ các hoạt động con có thời lượng chuẩn xác, tổng thời lượng toàn bộ giáo án 2 tiết đúng 90 phút (không bị đội lên 135 phút). -> **PASS**
3. **Tiêu chí 3**: Toàn bộ các bài kiểm thử liên quan đều PASS 100%. -> **PASS**

## Bug
Không có.

