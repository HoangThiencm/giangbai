# IMPLEMENT

Trạng thái: ĐÃ LÀM

## File đã đổi

- `canvas_xaydungphuluc.html`
- `xaydungphuluc.html`
- `tests/canvas-xaydungphuluc-smoke.js`

## Nội dung chính

- Giao diện Canvas hẹp / laptop 13 inch: header `py-1.5`, badge rút gọn "Gemini Canvas", nút dùng icon khi < 768px, hero `p-3` + nút ẩn/hiện, form Mục 1 `grid-cols-2 sm:grid-cols-3 md:grid-cols-4`, compact mode, gom nút Mục 4 thành nhóm PPCT và NLS/AI.
- Ghim cột STT + Bài học (`ppct-sticky-lesson`, `min-width:200px; max-width:320px`) khi cuộn ngang bảng Mục 4 trên cả hai file.
- Khôi phục `defaultPpctRows` (và khối hàm phụ thuộc bị thiếu) trên Canvas; mẫu Toán 6 giữ 47 bài; các môn khác dùng catalog chuẩn hoặc `SUBJECT_SAMPLE_TOPICS`.
- Viết lại `nlsLessonPriorityScore` đa môn (Toán, Văn, Anh, KHTN, Sử-Địa, Tin, Công nghệ, GDCD, HĐTN-HN…) + cộng điểm khi có `digital_evidence` / `ai_pedagogy_hint` từ Kho Tri thức SGK.
- `prioritizedAiPeriods` xen kẽ HK1/HK2; môn < 70 tiết/năm trần AI = `min(12, floor(tổng tiết * 0.2))`.
- Canvas gọi Gemini qua `canvas_gemini.php` (`{payload,timeout:120}`), không gọi Google/Mistral trực tiếp.

## Test đã chạy

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS (responsive + picker đa môn + Gemini Canvas + draft)
- `node tests/khbd-nls-rate-smoke.js` — PASS
- `node tests/xaydungphuluc-smoke.js` — PASS (Toán 6 vẫn 47 bài, slider AI vẫn trần 12)
- `node tests/sgk-knowledge-smoke.js` — PASS
- `node tests/xaydungphuluc-math-smoke.js` — live `canvas_xaydungphuluc.html` PASS; backup Canvas (ngoài phạm vi) vẫn thiếu `standards`

## Vấn đề còn lại

- Không sửa `backupcode viettailieu/canvas_xaydungphuluc.html` (ngoài phạm vi PLAN).
- Chưa verify tay trên viewport 550–700px trong trình duyệt Gemini Canvas.
