# IMPLEMENT: Khóa chuẩn tổng thời lượng 90 phút (chống lặp Hoạt động D) và Triệt tiêu 7 trang dòng chấm trong Phụ lục Phiếu học tập

## Phạm vi đã triển khai

- Giữ nguyên `docs/handoff/PLAN.md` và `docs/handoff/.lock`.
- Không đổi công thức `calculateActivityTimeBudgets`.
- Không đổi cấu trúc sư phạm 4 bước CV 5512.

### `js/khbd-prompts.js`

- `OUTPUT_CONTRACT`, `ACTIVITY_TABLE_CONTRACT`, `GENERATE_ACTIVITY_B`, `GENERATE_ACTIVITIES_AE`, `GENERATE_ACTIVITIES_AD`:
  - Khóa Hoạt động B = `{time_budget_B}`.
  - Nếu chia N nhánh (2.1, 2.2, ...), tổng phút N nhánh bắt buộc đúng bằng `{time_budget_B}` (ví dụ 45 phút chia 2 nhánh = 23 + 22; cấm 45 + 30 = 75).
  - Tổng A + B + C + D + E bắt buộc đúng bằng `{duration}` (02 tiết = đúng 90 phút).
  - `GENERATE_ACTIVITIES_AE` / `GENERATE_ACTIVITIES_AD`: đúng 5 marker duy nhất, cấm lặp marker hoặc tiêu đề `## D. HOẠT ĐỘNG 4`.
- `GENERATE_PORTFOLIO_WORKSHEETS`: cấm khối dòng chấm rác; câu hỏi/chỗ điền nằm trong bảng hoặc tối đa 1–2 dòng chấm ngắn; phụ lục F gọn 1–2 trang Word.

### `js/khbd-app.js`

- `collapseDottedLines` / `stripExcessiveDottedLines`: từ 3 dòng chấm/gạch liên tiếp ngoài bảng (`/^\s*[.\-_…\s]{10,}\s*$/`) rút còn 1 dòng. Gọi trong `sanitizeLessonMarkdown`.
- `clipKhbdActivityMarkdown("D")` và `parseKhbdSections`: nếu lặp tiêu đề D / marker `<<<KHBD_D>>>`, chỉ giữ 1 khối D tốt nhất.
- `normalizeActivityTimeHeadings`: chỉnh phút trên tiêu đề A–E và nhánh B cho khớp `calculateActivityTimeBudgets`.

### `js/khbd-docx.js`

- `collapseDottedLines` / `stripExcessiveDottedLines` trong `parseMarkdownToDocxElements` để Word không phình thành nhiều trang dấu chấm.

### Kiểm thử

- Thêm `tests/khbd-dotted-lines-smoke.js`.
- Thêm `tests/khbd-activity-d-dedupe-smoke.js`.

## Kiểm thử đã chạy

- `node tests/khbd-dotted-lines-smoke.js` — PASS
- `node tests/khbd-activity-d-dedupe-smoke.js` — PASS
- `node tests/khbd-activity-e-dedupe-smoke.js` — PASS
- `node tests/khbd-time-budgets-smoke.js` — PASS
- `node tests/khbd-sanitize-smoke.js` — PASS
- `node tests/khbd-docx-format-smoke.js` — PASS
- `node tests/khbd-activity-e-smoke.js` — PASS
- `node tests/khbd-activity-b-subsections-smoke.js` — PASS
- `node tests/khbd-docx-layout-smoke.js` — PASS
- `node tests/khbd-pedagogy-script-smoke.js` — PASS

Các suite không liên quan (1-click HTML, AI catalog, autofill metadata, clear-all) vẫn fail sẵn, không đụng trong phạm vi này.

## Vấn đề còn lại

- Không có trong phạm vi triển khai này. Cần `/verify` trên giao diện: bài 2 tiết không lặp D, B = 45 phút, Word Phụ lục F không còn 7 trang dòng chấm.
