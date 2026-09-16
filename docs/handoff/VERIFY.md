# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Khớp 100% yêu cầu trong `PLAN.md`:
  + `canvasTextbookAnalysisPrompt`: Ràng buộc AI giữ nguyên văn chỉ số đề mục có trong SGK (`1.`, `I.`, `A.`), và TUYỆT ĐỐI CẤM tự ý đánh thêm số nếu SGK không có số thứ tự.
  + `normalizeCanvasTextbookSection`: Bỏ hoàn toàn cơ chế ép `index = index + 1`.
  + `formatCanvasTextbookContext`: Xuất đúng `### ${section.title}` và `- Đề mục: ${section.title}`, loại bỏ hoàn toàn việc tự chèn tiền tố `${idx}. ` hay `Mục ${idx}:`, tránh lặp số `1. 1. ...`.
  + `js/khbd-prompts.js`: `extractTextbookSubsections` và `GENERATE_ACTIVITY_B` bảo lưu nguyên vẹn 100% đề mục gốc của SGK.
  + Đồng bộ cache-bust `textbook-exact-v12` trên Canvas và soankhbd.

## Test đã chạy
1. `node tests/khbd-textbook-exact-structure-smoke.js` (PASS 100% 5/5 test cases):
   - [TEST 1] Prompt phân tích SGK dùng schema fact-extraction nguyên văn.
   - [TEST 2] `parseCanvasTextbookAnalysis` và `formatCanvasTextbookContext` giữ nguyên văn đề mục, HĐ và bài tập.
   - [TEST 3] `GENERATE_ACTIVITY_B/C/D` khóa tên đề mục và đề bài nguyên văn 100%.
   - [TEST 4] Cache-bust JS `textbook-exact-v12`.
   - [TEST 5] Đề mục có số (`1.`, `I.`) giữ nguyên không bị lặp số; đề mục không số không bị tự động đánh số.
2. `node tests/canvas-soankhbd-smoke.js` (PASS 100%).
3. `node tests/canvas-textbook-analysis-smoke.js` (PASS 100%).
4. `node tests/khbd-activity-b-subsections-smoke.js` (PASS 100%).
5. `node tests/khbd-weighted-duration-smoke.js` (PASS 100%).

## Pass / Fail từng tiêu chí
- [PASS] Đề mục có chỉ số trong SGK (1, 2, I, II, A, B) giữ đúng 100% chỉ số đó, không bị lặp số đúp (`1. 1. ...`).
- [PASS] Đề mục không có chỉ số trong SGK tuyệt đối không bị tự động đánh số thêm.
- [PASS] Tên Hoạt động 2.1, 2.2 hiển thị đúng đề mục gốc của SGK.

## Bug
Không có.
