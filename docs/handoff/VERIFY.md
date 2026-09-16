# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Mục tiêu**: Hoàn thiện `canvas_soanbaigiang.html` — Kế thừa 100% luồng đọc SGK thật của `canvas_soankhbd` & sinh bài giảng trình chiếu AI thật (không mock/demo).
- **Trạng thái đối chiếu**:
  - `canvas_soanbaigiang.html` & `js/khbd-slides.js`: Đã cài đặt `generateAiLessonSlides()` gọi `geminiAPI.generateContent` (`gemini-3-flash-preview`), sinh 15–25 slide chi tiết theo cấu trúc phân rã `title`, `intro`, `explore`, `rule`, `example`, `practice`, `summary`, không còn dùng câu chữ placeholder giả mạo.
  - Trình chiếu 16:9 sắc nét, hỗ trợ KaTeX, hiệu ứng từng bước và xuất file `.pptx` hoàn chỉnh.
  - Khắc phục triệt để lỗi phân tích SGK: `canvasTextbookAnalysisPrompt()` đã bổ sung chỉ thị fact extraction ngắn gọn, nguyên văn 100%, không lặp số đề mục; `mergeCanvasTextbookSections()` tự động nhập tiểu mục không số vào Mục 1.
  - `canvas_soankhbd.html` được bảo toàn nguyên vẹn 100%, không bị ảnh hưởng.

## Test đã chạy
- `node tests/canvas-soanbaigiang-smoke.js` — PASS
- `node tests/canvas-soankhbd-smoke.js` — PASS
- `node tests/khbd-textbook-exact-structure-smoke.js` — PASS
- `node tests/khbd-activity-b-subsections-smoke.js` — PASS
- `node tests/docx-export-format-smoke.js` — PASS
- `node tests/khbd-4steps-workflow-smoke.js` — PASS
- `node tests/ppct-settings-import-smoke.js` — PASS
- `node tests/khbd-docx-layout-smoke.js` — PASS

## Pass / Fail từng tiêu chí
- [PASS] `canvas_soanbaigiang.html`: Đọc SGK thật, sinh bài giảng AI thật bằng `gemini-3-flash-preview`.
- [PASS] Trình chiếu 16:9, KaTeX và xuất file PPTX.
- [PASS] Trích xuất SGK nguyên văn, không mất Mục 1, không tự đánh số.
- [PASS] `canvas_soankhbd.html` không bị ảnh hưởng.
- [PASS] Toàn bộ 8/8 test suites PASS 100%.

## Bug
Không phát hiện lỗi.
