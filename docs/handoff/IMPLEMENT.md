# Báo cáo triển khai: Không tự đánh số đề mục SGK

## Đã thực hiện

- `js/khbd-app.js`
  - `canvasTextbookAnalysisPrompt`: nếu SGK có chỉ số thì giữ nguyên; nếu không có thì cấm tự thêm số.
  - `normalizeCanvasTextbookSection`: không còn ép `index = index + 1`.
  - `formatCanvasTextbookContext`: xuất `### ${title}` và `- Đề mục: ${title}`; bỏ `${idx}.` và `Mục ${idx}:`.
- `js/khbd-prompts.js`
  - `extractTextbookSubsections`: giữ nguyên văn chỉ số SGK (`1.`, `I.`, `A.`); không tự chèn số vào đề mục không có số.
  - `GENERATE_ACTIVITY_B`: `### Hoạt động 2.k: [tên nguyên văn]`; nếu SGK có `1. ...` thì `### Hoạt động 2.1: 1. ...`, không lặp `1. 1.`.
- Cache-bust `textbook-exact-v12` trên `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`.
- `tests/khbd-textbook-exact-structure-smoke.js`: thêm TEST 5 (có số / La Mã / không số).

## Kiểm thử

- `node tests/khbd-textbook-exact-structure-smoke.js`: PASS
- `node tests/canvas-soankhbd-smoke.js`: PASS
- `node tests/khbd-activity-b-subsections-smoke.js`: PASS
- `node tests/canvas-textbook-analysis-smoke.js`: PASS
- `node tests/khbd-weighted-duration-smoke.js`: PASS

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.
