# IMPLEMENT: Markdown underscore trong Word và khóa thời lượng Hoạt động B

## Phạm vi đã triển khai

- Giữ nguyên thay đổi sẵn có tại `docs/handoff/PLAN.md` và `docs/handoff/.lock`.
- `js/khbd-docx.js`
  - `parseInlineTextToRuns` hỗ trợ `_italic_` và `__bold__`, đồng thời vẫn ưu tiên nhận diện biểu thức LaTeX trước khi xử lý Markdown.
  - Các mảnh bảng rò rỉ đứng riêng (`|`, separator pipe, `---` gắn với pipe) bị bỏ qua; bảng Markdown hợp lệ vẫn được xuất Word.
  - Khi bỏ artifact, chỉ số dòng được tăng đúng một lần ở cuối vòng lặp nên không bỏ qua nội dung hợp lệ ngay sau đó.
- `js/khbd-app.js`
  - `sanitizeLessonMarkdown` loại bỏ riêng pipe/separator rò rỉ sau khi chuẩn hóa bảng hoạt động mà không xóa separator của bảng hợp lệ.
- `js/khbd-prompts.js`
  - Tiêu đề Hoạt động B có `{time_budget_B}`.
  - Prompt khóa tổng các nhánh B đúng bằng thời lượng B và tổng A–E đúng bằng `{duration}`; đồng thời yêu cầu không dùng `_Trạm X:_` / `__tiêu đề__`.
- Kiểm thử
  - Thêm `tests/khbd-docx-format-smoke.js`.
  - Cập nhật `tests/khbd-sanitize-smoke.js` và `tests/khbd-time-budgets-smoke.js`.
  - Smoke test định dạng Word xác nhận dòng sau pipe rò rỉ vẫn được xuất.

## Kiểm thử đã chạy

- `node tests/khbd-docx-format-smoke.js` — PASS
- `node tests/khbd-sanitize-smoke.js` — PASS
- `node tests/khbd-time-budgets-smoke.js` — PASS
- `node tests/khbd-docx-math-smoke.js` — PASS
- `node tests/khbd-docx-layout-smoke.js` — PASS
- `git diff --check` — PASS (cảnh báo newline thuộc `docs/handoff/PLAN.md` có sẵn, không chỉnh sửa).

## Vấn đề còn lại

- Không có trong phạm vi triển khai này.
