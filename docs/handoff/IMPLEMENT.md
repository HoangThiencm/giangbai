# IMPLEMENT

Trạng thái: ĐÃ LÀM — Lọc chuỗi `\quad` rác trong prompt, KaTeX preview và xuất Word

## File đã đổi

- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `js/khbd-docx.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Nội dung chính

1. **Prompt (`js/khbd-prompts.js`)**
   - Thêm `LATEX_SPACING_BAN` cấm chuỗi `\quad` / `\qquad` / `\hspace{...}` / `\phantom{...}` để giả lập hình vẽ hoặc trục số.
   - Bài vẽ hình/trục số: mô tả bước thực hiện tường minh hoặc `![caption](khbd-ill:id)`.
   - Gắn vào `ACTIVITY_TABLE_CONTRACT`, `OUTPUT_CONTRACT`, `GENERATE_ACTIVITY_B`, `GENERATE_ACTIVITY_C`, `GENERATE_ACTIVITY_D`.

2. **Làm sạch Markdown / KaTeX (`js/khbd-app.js`)**
   - `stripGarbageLatexSpacing`: xóa khối `$...$` / `$$...$$` chỉ chứa lệnh khoảng trắng (và gạch nối/mũi tên giả lập trục số); rút gọn `(?:\quad|\qquad){3,}` còn 1 khoảng trắng.
   - Gọi trong `sanitizeLessonMarkdown`, `unwrapVietnameseMathForKatex`, `renderMathPreview`.
   - Giữ công thức hợp lệ kiểu `$x = 1 \quad \text{hoặc} \quad x = 2$`.

3. **Xuất Word (`js/khbd-docx.js`)**
   - `stripRepeatedLatexSpacing` + `isGarbageLatexMathInner` trong `latexToUnicodeMath` và `parseMarkdownToDocxElements`.
   - Bỏ khối `\quad` rác trước khi tạo Unicode / Paragraph / Equation, tránh hàng trăm dấu cách làm vỡ bảng 2 cột.

## Ngoài phạm vi (không đụng)

- Không đổi cấu trúc bảng 2 cột CV 5512.
- Không lọc `\quad` đơn/đôi trong công thức toán hợp lệ.

## Test đã chạy

```
node tests/khbd-sanitize-smoke.js
node tests/khbd-katex-vn-smoke.js
node tests/khbd-docx-math-smoke.js
node tests/khbd-docx-layout-smoke.js
node tests/khbd-4steps-workflow-smoke.js
```

Kết quả: **pass**.

Kiểm tra riêng bộ lọc `\quad`:
- `$$\quad \quad \quad...$$` bị xóa; lời văn giữ nguyên.
- Khối chỉ `\hspace` / `\phantom` / mũi tên + `\quad` bị xóa.
- `$x = 1 \quad \text{hoặc} \quad x = 2$` giữ nguyên.
- 3+ `\quad` liên tiếp rút gọn còn 1 khoảng trắng.
- `latexToUnicodeMath` không chèn chuỗi space dài.

Không mở được trình duyệt để bấm tạo bài AI / xuất Word trên `soankhbd.html`. Preview KaTeX và file .docx thật (Toán 6 Bài 3.4) cần `/verify` trên giao diện.
