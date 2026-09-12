# IMPLEMENT: Bộ chọn tích hợp NLS/AI tại Mục 1 Xây dựng Phụ lục

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `canvas_xaydungphuluc.html`
  - Đưa `#nlsUnit`, `#nlsCountInput`, `#aiUnit` và `#aiCountInput` vào đúng hai thẻ NLS/AI tại Mục 1.
  - Bổ sung bố cục inline gọn: chọn đơn vị, nhập tổng số tiết/bài và gợi ý kéo tỉ lệ %.
  - Xóa thẻ phân bổ NLS/AI trùng lặp ở cuối trang; mỗi ID chỉ còn một lần.
  - Giữ cơ chế gắn sự kiện Canvas hiện có để đồng bộ số lượng ↔ tỉ lệ mà không xử lý thay đổi hai lần.
- `xaydungphuluc.html`
  - Đồng bộ bố cục Mục 1 với Canvas: khoảng cách và nhãn hướng dẫn cho hai cách cấu hình.
- `tests/canvas-xaydungphuluc-smoke.js`
  - Kiểm tra ID phân bổ là duy nhất, không còn thẻ trùng lặp và mọi điều khiển nằm trong thẻ Mục 1 trước thanh tỉ lệ.
  - Bộ kiểm tra hiện có tiếp tục xác nhận cả luồng nhập số lượng → tỉ lệ và kéo tỉ lệ → số lượng, cho đơn vị tiết và bài.

## Kiểm tra đã chạy

- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần chạy `/verify` để xác nhận trực quan trên hai giao diện.
