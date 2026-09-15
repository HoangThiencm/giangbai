# Báo cáo triển khai: Định mức PPDH/KTDH 1 tiết + xuống dòng GV/HS trên Canvas

## Phạm vi đã thực hiện

Tiếp tục bản dở (mất điện). Canvas Gemini nạp JS cũ từ host nên gate local chưa chạy; đề xuất 1 tiết vẫn còn Trạm/5W1H/TPS; xuất Word GV/HS dính một dòng.

- `js/khbd-app.js`:
  - Gate 1 tiết: đúng 1 PPDH; pha B đúng 1 KTDH nhẹ (TPS / khăn trải bàn / 5W1H); pha A/C/D để trống (vấn đáp/luyện tập tự nhiên).
  - Lọc hoạt động đặc thù nặng: `station`, `station-act` (Trạm xoay vòng), `product`, jigsaw/gallery/PBL/STEAM.
  - `enforceTimeBudgetGateOnCurrentPedagogy()` chạy khi đề xuất và khi render catalog (gỡ lựa chọn cũ, gỡ badge “Phù hợp môn này” cho kỹ thuật nặng).
  - `formatKhbdRoleLineBreaks` tách `GV:`/`HS:` dính dòng, cả trong ô bảng Markdown, cả dạng `GV: "...". HS giải thích...`; không nhân đôi `<br>` khi đã chuẩn.
  - Áp format khi `getFullLessonPlanMarkdown` (xuất Word / preview toàn bài).
- `js/khbd-docx.js`: `parseTableCellParagraphs` gọi formatter nếu có; tách Paragraph riêng cho GV/HS.
- `js/khbd-prompts.js` + bối cảnh sư phạm: cấm Trạm/Station Rotation ở bài 1 tiết.
- `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`:
  - Nhúng patch `canvasTimeBudgetAndRoleBreaks` ngay trong HTML (không phụ thuộc JS host cũ).
  - Patch: gate + prune checkbox HĐ đặc thù, wrap `recommendPedagogyFromLesson` / `ensurePedagogyFromLesson` / `renderPedagogyCatalogs` / `getFullLessonPlanMarkdown` / `parseTableCellParagraphs`.
  - Cache-bust `?v=20260915-ppdh-gvhs`.

## Kiểm thử

- `node tests/khbd-pedagogy-rate-smoke.js`: PASS (gate 1 tiết gồm `station-act`, format bảng + HS sau câu thoại GV).
- `node tests/canvas-soankhbd-smoke.js`: PASS (cả live và backup có patch).
- `node tests/khbd-4steps-workflow-smoke.js`: PASS.
- `node tests/khbd-docx-format-smoke.js`: PASS.
- `node tests/khbd-nls-ai-bold-italic-smoke.js`: PASS.
- `node tests/khbd-integrations-smoke.js`: PASS.
- `node tests/khbd-dynamic-integrations-smoke.js`: PASS.
- `node tests/backupcode-canvas-smoke.js`: PASS.

## Cách thấy ngay trên Gemini Canvas

Host `hoangthiencm.id.vn` vẫn có thể nạp `khbd-app.js` cũ. Không cần chờ upload JS: **dán lại toàn bộ `canvas_soankhbd.html` vào Canvas**. Patch nằm trong HTML, chạy ngay sau khi dán.

## Bảo toàn

- Không sửa `docs/handoff/PLAN.md`.
- Không commit hoặc push.
- Không đổi kiến trúc; không đụng file ngoài plan.
