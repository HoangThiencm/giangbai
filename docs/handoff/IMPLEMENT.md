# IMPLEMENT: Cột bảng Word, header lặp, begincases, sư phạm Toán THCS

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Module 1 — 2 cột không lẫn nội dung
- Prompt `ACTIVITY_TABLE_CONTRACT`: `QUY TẮC CỘT BẢNG TUYỆT ĐỐI` — cấm `|` trong ô; liệt kê bằng `,` `/` `\vert`.
- `semanticSplitActivityRow` (`js/khbd-app.js`, `js/khbd-docx.js`): cell có `Bước 1–4` / `GV:` / `HS:` / `[Kỹ thuật` thuộc Cột 1; cell kiến thức (định nghĩa, công thức, `$...$`) thuộc Cột 2. Không còn `slice(1)` dồn hết sang Cột 2.
- `mergeSplitActivityTables` và `createDocxTableFromMarkdown` dùng splitter này.

## Module 2 — Tiêu đề bài chỉ trang 1
- `exportFullLessonPlan`: `section.children = [...headerElements, ...bodyElements]`. Không gán `section.headers.default`. Footer trang vẫn giữ.

## Module 3 — `\begin{cases}` có tiền tố
- `createCasesMath` nhận `^([\s\S]*?)\\begin{cases|aligned}...\\end`. Tiền tố `\Leftrightarrow` / `\Rightarrow` thành MathRun, rồi delimiter `{` + `m:eqArr`.
- `createNativeMath` xử lý lệnh `\begin{cases|aligned}` giữa biểu thức.
- `latexToUnicodeMath` không xóa `{` của hệ; chỉ gỡ `{}` rỗng hoặc ngoặc nhóm token ngắn.

## Module 4 — Sư phạm Toán CT GDPT 2018
- `getPromptTemplate` (môn `toan`) và `buildPedagogicalPrompt`: THCS cấm `$\Leftrightarrow$`; cấm `$\Rightarrow$` nhảy cóc từ hệ sang nghiệm; bắt buộc lời dẫn + phương pháp thế / cộng đại số + câu kết luận nghiệm SGK. THPT vẫn được dùng `$\Leftrightarrow$`.

Kiểm thử:
- `node tests/khbd-table-columns-smoke.js` — PASS (Bước 3/4 ở cột trái khi có `|` nội dung)
- `node tests/khbd-docx-math-smoke.js` — PASS (`$\Leftrightarrow \begin{cases}...$` có `{`, không `begincases`)
- `node tests/docx-export-format-smoke.js` — PASS (tiêu đề vào body)
- `node tests/canvas-prompts-integrity-smoke.js` — PASS
- `node tests/khbd-sanitize-smoke.js` — PASS
- `node tests/khbd-docx-format-smoke.js` — PASS
- `node tests/khbd-docx-layout-smoke.js` — PASS
- `node tests/khbd-nls-ai-bold-italic-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity: xuất Word bài Toán 9 — Giải hệ, kiểm tra 2 cột, không lặp header, không `begincases`.
