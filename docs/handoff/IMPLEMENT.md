# Báo cáo triển khai: Trích xuất SGK nguyên văn cho Hoạt động 2–4

## Đã thực hiện

- `js/khbd-app.js`
  - `canvasTextbookAnalysisPrompt`: schema JSON fact-extraction (`sections`, `activities`, `exercises`); giữ nguyên văn 100% tên đề mục, HĐ/Luyện tập/Thực hành/Vận dụng, mã bài và đề bài; không chép nguyên trang (tránh RECITATION); vẫn cấm điền trí nhớ/suy đoán.
  - `parseCanvasTextbookAnalysis` + `formatCanvasTextbookContext`: xuất đề mục, kiến thức cốt lõi, hoạt động con và bài tập rõ từng phần; suy `subsections` cho phân bổ thời lượng.
  - `maxOutputTokens` lô phân tích: 4096.
- `js/khbd-prompts.js`
  - `GENERATE_ACTIVITY_B`: khóa tên Hoạt động 2.1, 2.2 trùng 100% tên đề mục SGK.
  - `GENERATE_ACTIVITY_C`: lấy nguyên văn đề bài Luyện tập/Thực hành/bài tập; cấm đổi số liệu, cấm bịa đề.
  - `GENERATE_ACTIVITY_D`: ưu tiên nguyên văn đề bài mục Vận dụng.
- Cache-bust `textbook-exact-v11`: `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html`, `soankhbd.html`.
- `tests/khbd-textbook-exact-structure-smoke.js`: test mới. Cập nhật `tests/canvas-textbook-analysis-smoke.js` cho schema mới.

## Kiểm thử

- `node tests/khbd-textbook-exact-structure-smoke.js`: PASS
- `node tests/canvas-soankhbd-smoke.js`: PASS
- `node tests/canvas-textbook-analysis-smoke.js`: PASS
- `node tests/khbd-activity-b-subsections-smoke.js`: PASS
- `node tests/khbd-weighted-duration-smoke.js`: PASS
- `node tests/khbd-integrations-smoke.js`: PASS

Không commit, push hoặc deploy. `docs/handoff/PLAN.md` không bị sửa.
