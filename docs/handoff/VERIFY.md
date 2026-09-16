# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Khớp 100% yêu cầu trong `PLAN.md`:
  + `canvasTextbookAnalysisPrompt`: Chuyển sang Schema JSON fact-extraction (`sections`, `activities`, `exercises`) giữ nguyên văn 100% tên đề mục, tên hoạt động (HĐ, Luyện tập, Thực hành, Vận dụng), mã bài và đề bài/số liệu/công thức LaTeX; loại bỏ hoàn toàn các câu lệnh cấm chép/diễn đạt lại; giữ nguyên tắc không tự suy đoán bằng trí nhớ.
  + `formatCanvasTextbookContext`: Xuất cấu trúc ngữ cảnh SGK rõ ràng từng phần Đề mục và Hệ thống bài tập.
  + `js/khbd-prompts.js`:
    - `GENERATE_ACTIVITY_B`: Khóa tên Hoạt động 2.1, 2.2 trùng khớp 100% với tên đề mục SGK đã trích xuất.
    - `GENERATE_ACTIVITY_C`: Khóa nguyên văn 100% đề bài, số liệu, công thức từ SGK, cấm đổi số liệu hoặc tự bịa bài.
    - `GENERATE_ACTIVITY_D`: Ưu tiên lấy nguyên văn đề bài mục Vận dụng trong SGK.
  + Đồng bộ cache-busting `textbook-exact-v11` trên `canvas_soankhbd.html`, `backupcode viettailieu/canvas_soankhbd.html` và `soankhbd.html`.

## Test đã chạy
1. `node tests/khbd-textbook-exact-structure-smoke.js` (PASS 100% 4/4 test cases):
   - [TEST 1] Prompt phân tích SGK dùng schema fact-extraction nguyên văn, không chép nguyên trang (tránh RECITATION).
   - [TEST 2] `parseCanvasTextbookAnalysis` và `formatCanvasTextbookContext` giữ nguyên văn đề mục, HĐ và bài tập.
   - [TEST 3] `GENERATE_ACTIVITY_B/C/D` khóa tên đề mục và đề bài nguyên văn 100%.
   - [TEST 4] Cache-bust JS `textbook-exact-v11` trên Canvas và soankhbd.
2. `node tests/canvas-soankhbd-smoke.js` (PASS 100%).
3. `node tests/canvas-textbook-analysis-smoke.js` (PASS 100%).
4. `node tests/khbd-activity-b-subsections-smoke.js` (PASS 100%).
5. `node tests/khbd-weighted-duration-smoke.js` (PASS 100%).
6. `node tests/khbd-integrations-smoke.js` (PASS 100%).

## Pass / Fail từng tiêu chí
- [PASS] Trích xuất đúng 100% tên các Đề mục lớn (1. ..., 2. ...) từ SGK.
- [PASS] Trích xuất đúng 100% đề bài, số liệu, công thức LaTeX của các bài tập SGK.
- [PASS] Hoạt động 2 (Hình thành kiến thức) đặt đúng tên các tiểu mục 2.1, 2.2 theo SGK.
- [PASS] Hoạt động 3 (Luyện tập) và Hoạt động 4 (Vận dụng) giữ nguyên văn đề bài SGK thật.
- [PASS] Không bị lỗi từ chối bản quyền `RECITATION`.

## Bug
Không có.
