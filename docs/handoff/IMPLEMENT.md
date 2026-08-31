# IMPLEMENT: Sửa thanh tiến trình 100% không dừng / không tự ẩn

## Phạm vi đã triển khai

- Sửa đúng bug FAIL trong `VERIFY.md`: khi sinh AI đạt 100%, spinner vẫn xoay, thanh nổi không tự ẩn và không có nút đóng `✕`.
- `setProgress`: nếu `percent >= 100` thì thay spinner bằng `✓`, giữ thông báo hoàn tất, rồi `setTimeout(() => hideProgress(), 1500)`.
- Nếu `percent < 100` và đang hiện: xóa timer ẩn cũ (`progressTimerId`) và hiện spinner xoay.
- `hideProgress()`: fade-out rồi `hidden`; nút `✕` gọi `hideProgress()` để đóng ngay.
- Hủy tác vụ / lỗi: hiện trạng thái hoàn tất rồi tự ẩn sau 2 giây.
- Không đổi schema 7 cột PPCT đã PASS; không sửa `PLAN.md`, `VERIFY.md` hoặc `.lock`; không commit/push.

## File thay đổi

- `xaydungphuluc.html`: `#progressContainer` thêm nút `✕`; thêm `hideProgress`, `progressTimerId`; nâng cấp `setProgress` và nhánh hủy/lỗi trong `generateSelected`.
- `tests/xaydungphuluc-smoke.js`: assert `hideProgress`, `setTimeout` 1.5s, nút `✕`, `progressTimerId`.
- `docs/handoff/IMPLEMENT.md`: báo cáo triển khai này.

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.

Không có browser MCP trong phiên này nên chưa bấm sinh AI trên trình duyệt.

## Vấn đề còn lại

- Cần `/verify` trên trình duyệt: sinh phụ lục đến 100%, xác nhận spinner dừng, `✓` hiện ra, thanh tự ẩn sau 1.5s, và nút `✕` đóng được ngay.
