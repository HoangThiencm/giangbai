# IMPLEMENT: Nâng cấp chất lượng sư phạm & dàn trang slide/PPTX

Đã triển khai đúng `docs/handoff/PLAN.md`.

- Thiết kế lại hợp đồng prompt `generateAiLessonSlides`: schema giàu cấu trúc (`subtitle`, `problem`, `explanation`, `steps` có label, `ruleBox`, `note`, `mathFormula`). Cấm placeholder kiểu "Hiển thị...", "Liệt kê...", "Xuất hiện...".
- `normalizeAiDeck` lọc câu chỉ dẫn thao tác, bóc tách đề bài / bước giải từ `content` khi AI trả về một khối, map `concept`→`rule` và `objective`→`intro`.
- `exportToPptx` bỏ bước Y cố định `0.58"` (nguyên nhân đè chữ). Mỗi vùng là một card + một text box `paragraphs`. Slide bìa căn giữa; ví dụ/luyện tập/khám phá bố cục 2 cột (38% đề bài — 58% lời giải); slide quy tắc dùng hộp "GHI NHỚ / TRỌNG TÂM" nền `#EFF6FF`.
- `latexToPlain` chuyển `\begin{cases}`, `\frac`, `\text{...}` và ký hiệu phổ biến thành văn bản nhiều dòng, không lộ mã LaTeX trên PowerPoint. Web vẫn bọc công thức bằng `$`/`$$` để KaTeX render.
- HTML renderer + CSS: `.khbd-slide-split`, `.khbd-slide-col-left`, `.khbd-slide-col-right`, `.khbd-slide-rulebox`, `.khbd-step-badge`.
- Đồng bộ nguyên module vào `canvas_soanbaigiang.html` và `backupcode viettailieu/canvas_soanbaigiang.html`. Không đụng Canvas KHBD.

Kiểm thử:

- `node tests/canvas-soanbaigiang-smoke.js` — PASS 100% (schema mới, chống placeholder, LaTeX cases, không đè chữ PPTX, CSS 2 cột, luồng 1-click).
- `git diff --check` — PASS (chỉ cảnh báo LF/CRLF sẵn có).

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity để xem slide web và file PPTX với bài Toán 9 — Giải hệ phương trình bằng phương pháp thế.
