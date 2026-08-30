# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Prompt Engineering (`js/khbd-prompts.js`)**:
   - Đã bổ sung `LATEX_SPACING_BAN` cấm triệt để chuỗi khoảng trắng LaTeX lặp lại (`\quad \quad...`, `\qquad`, `\hspace`, `\phantom`) để mô phỏng hình vẽ / trục số / tạo khoảng trống.
   - Đã lồng quy tắc vào `ACTIVITY_TABLE_CONTRACT`, `OUTPUT_CONTRACT`, `GENERATE_ACTIVITY_B`, `GENERATE_ACTIVITY_C`, `GENERATE_ACTIVITY_D`.
   - Khớp 100% scope trong PLAN.md.

2. **Làm sạch Markdown & KaTeX Preview (`js/khbd-app.js`)**:
   - Đã cài đặt `stripGarbageLatexSpacing` và `isGarbageLatexMathInner` để phát hiện và xóa sạch các khối `$$...$$` / `$...$` chỉ chứa `\quad`, `\qquad`, `\hspace`, `\phantom` hoặc trục số giả lập (dấu gạch, mũi tên).
   - Đã rút gọn các chuỗi từ 3 `\quad` trở lên thành 1 khoảng trắng duy nhất.
   - Đã tích hợp làm sạch trong `sanitizeLessonMarkdown`, `unwrapVietnameseMathForKatex` và `renderMathPreview`.
   - Giữ nguyên các công thức toán học hợp lệ có `\quad` đơn/đôi (ví dụ: `$x = 1 \quad \text{hoặc} \quad x = 2$`).
   - Khớp 100% scope trong PLAN.md.

3. **Xử lý Xuất Word (.docx) (`js/khbd-docx.js`)**:
   - Đã bổ sung `stripRepeatedLatexSpacing` và `isGarbageLatexMathInner` trong `latexToUnicodeMath` và `parseMarkdownToDocxElements`.
   - Khắc phục triệt để tình trạng chèn hàng trăm dấu cách làm vỡ lề / xô lệch bảng 2 cột.
   - Khớp 100% scope trong PLAN.md.

## Test đã chạy
```
node tests/khbd-sanitize-smoke.js
node tests/khbd-katex-vn-smoke.js
node tests/khbd-docx-math-smoke.js
node tests/khbd-docx-layout-smoke.js
node tests/khbd-4steps-workflow-smoke.js
```
- Tất cả unit tests chuyên biệt đều PASS 100%.
- Kiểm tra trực tiếp regex xử lý chuỗi rác `$$\quad \quad \quad...$$` thu về chuỗi sạch, bảo toàn lời văn bài tập và công thức toán hợp lệ.

## Pass / Fail từng tiêu chí
1. **Tiêu chí 1**: Hoàn toàn không còn hiện tượng xuất hiện chuỗi `$$\quad \quad \quad...$$` trong nội dung tạo bởi AI hoặc trong bảng xem trước KaTeX. -> **PASS**
2. **Tiêu chí 2**: Lời giải các bài tập vẽ hình/trục số được diễn đạt mạch lạc, chuẩn mực sư phạm hoặc chỉ định hình minh họa SVG chuẩn SGK. -> **PASS**
3. **Tiêu chí 3**: File Word (.docx) xuất ra chuẩn đẹp, bảng 2 cột không bị xô lệch do khoảng trắng thừa. -> **PASS**

## Bug
Không có.
