# IMPLEMENT: Đảo key Free khi 503 và chỉ giữ model Flash

## Đã làm
- `api/khbd_gemini.php`: `khbd_gemini_should_rotate` coi HTTP 503 và các thông báo high demand, overloaded, unavailable là lý do chuyển sang API key Free kế tiếp. Model đang chọn không đổi.
- `phancongtochuyenmon.html`: modal Gemini chỉ còn `gemini-2.5-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview` và ô tùy chỉnh. Đã bỏ `gemini-2.5-pro` và `gemini-1.5-flash`.
- Nút mở modal trên Top Navbar (`#top-nav-ai-model-label`, cạnh Khai báo tổ) và trên `.tt-toolbar` (`#tt-toolbar-model-label`).
- `updateAiModelLabels(model)` cập nhật cả ba nhãn: navbar, toolbar TKB và nút trong thẻ nhập ảnh.
- `tests/timetable-render-smoke.js`: không còn Pro/1.5 trong trang TKB; có hai nút mới; PHP xoay key khi 503 và high demand.

## Kiểm thử
- `node tests/timetable-render-smoke.js` → PASS.

## Chưa kiểm trên trình duyệt
- Chưa bấm hai nút mới và chưa gọi thử Gemini 503 để xem key kế tiếp. Phần đó để `/verify`.
