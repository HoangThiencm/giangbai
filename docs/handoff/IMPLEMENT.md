# IMPLEMENT: Khắc phục numbering Preview và chuẩn bảng Hoạt động 2 cột

## Phạm vi đã triển khai

- Giữ nguyên thay đổi có sẵn tại `docs/handoff/PLAN.md` và `docs/handoff/.lock`.
- `js/khbd-app.js`
  - `sanitizePreviewHtml()` giữ có kiểm tra các thuộc tính danh sách: `ol[start]`, `li[value]`, cùng `type` hợp lệ (`ol/li`: `1`, `a`, `A`, `i`, `I`; `ul`: `disc`, `circle`, `square`).
  - Chuẩn hoá mọi hàng của bảng Hoạt động: chỉ giữ cột trái và gộp các cell từ vị trí 2 trở đi bằng ` | ` vào cột Nội dung.
- `js/khbd-docx.js`
  - Chỉ nhận diện bảng Hoạt động khi header đồng thời có `Hoạt động của GV` và `Nội dung`.
  - Với bảng nhận diện được, ép đúng 2 cột rộng `[4819, 4820]` và gộp cell dư vào cột Nội dung.
- `js/khbd-prompts.js`
  - Siết hợp đồng prompt: cấm cột thứ ba và yêu cầu dùng `\\vert` hoặc `\\|` cho ký hiệu gạch đứng.
- Thêm smoke test:
  - `tests/khbd-list-numbering-smoke.js`
  - `tests/khbd-table-columns-smoke.js`

## Kiểm thử

Đạt:

- `node tests/khbd-list-numbering-smoke.js`
- `node tests/khbd-table-columns-smoke.js`
- `node tests/khbd-sanitize-smoke.js`
- `node tests/khbd-pedagogy-script-smoke.js`
- `git diff --check`

Toàn bộ suite đã được chạy bằng `node tests/run-all-tests.js` nhưng dừng ở test có sẵn `tests/khbd-1click-chain-smoke.js` do assertion hướng dẫn Bước 4 sang Tab 2, 3, 4. Lỗi này không thuộc các file/phạm vi thay đổi của đợt triển khai; các kiểm thử liên quan trực tiếp đều PASS.

## Vấn đề còn lại

- Cần xử lý hoặc cập nhật riêng smoke test `khbd-1click-chain-smoke.js` trước khi có thể xác nhận toàn bộ suite PASS 100%.
