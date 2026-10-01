# IMPLEMENT — Bút trình chiếu, zoom ảnh, dẫn dắt 4 bước

## Đã làm
- `master_lecture_template.html`: phím tiến `ArrowRight`, `ArrowDown`, `PageDown`, Space, `Enter`; phím lùi `ArrowLeft`, `ArrowUp`, `PageUp`, `Backspace`; phím `b` và `.` bật/tắt `#blankScreen` (`.blank-screen`). `preventDefault()` khi nhận các phím này ngoài ô nhập. Nút `.control-bar` gọi `blur()` sau click.
- Click trên `#slideDeck`: `zoomableFigure()` mở Lightbox cho `svg` / `img` / `.figure-box` / `[data-zoomable]` (bỏ `mjx-container`) và không gọi `nextStep()`. Delegation không phụ thuộc listener gắn trên từng ảnh.
- Slide mẫu 5 và 7 trong template tách đề (bước 1), gợi ý (bước 2), lời giải chi tiết (bước 3), đáp số và ghi bảng (bước 4).
- `PROMPT_TAO_BAI_GIANG_HTML.md` và `.agents/rules/tao-bai-giang-html.md`: Vá 22 nêu event delegation; thêm Vá 23 (4 bước) và Vá 24 (bút trình chiếu).
- `Bai_12_...html` và `Bai_4_...html`: cùng bộ phím, màn hình đen, delegation zoom. Khối có huy hiệu Lời giải đang `data-step="2"` được chuyển thành `data-step="3"` (15 khối ở bài 12, 16 khối ở bài 4). Khối gợi ý giữ bước 2.

## Kiểm thử
- `node tests/trolythien-template-smoke.js` — PASS
- `node tests/trolythien-bai-giang-html-smoke.js` — PASS

## Ghi chú cho /verify
- Câu «Vậy» trong hai file Ket_qua vẫn nằm trong khối lời giải bước 3. Tách thành khối bước 4 riêng trên HTML một dòng làm vỡ thẻ; mẫu 4 bước đầy đủ nằm ở slide 5 và 7 của master template và trong Vá 23.
- Chưa commit, chưa push.
