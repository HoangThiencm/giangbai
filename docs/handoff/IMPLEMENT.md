# IMPLEMENT: Gỡ bỏ hoàn toàn cơ chế tự động refresh (Auto-Reload)

Trạng thái: ĐÃ THỰC HIỆN — chờ `/verify`

## Phạm vi đã triển khai

- `js/security-guard.js`
  - Xóa toàn bộ module Auto-Update Checker (biến `appVersionStorageKey`, `appVersionReloadAtKey`, `appVersionReloadDebounceMs`, `appVersionCheckInFlight`; hàm `getVersionValue`, `checkAppVersionUpdate`, `initAutoUpdateChecker`; lệnh gọi `initAutoUpdateChecker();`).
  - File không còn `fetch('/version.json')` và không còn tự gọi `window.location.reload()` khi focus, visibilitychange hoặc theo chu kỳ 60 giây.
  - Giữ nguyên các chức năng bảo vệ DevTools hiện có, gồm reload thủ công sau khi Admin nhập mã mở khóa.
- `tests/auto-reload-smoke.js`
  - Đổi kiểm thử sang xác nhận `js/security-guard.js` không còn `initAutoUpdateChecker` / `checkAppVersionUpdate`, không fetch `version.json`, và không tự reload khi nạp script hay khi có sự kiện focus/visibilitychange.

## Kiểm tra đã chạy

- `node tests/auto-reload-smoke.js`: PASS.
- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/timetable-render-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
- Cần chạy `/verify` để xác nhận các trang không còn tự refresh.

---

# IMPLEMENT: Giá trị mặc định thông tin đơn vị tại Xây dựng Phụ lục

## Phạm vi đã triển khai

- `xaydungphuluc.html` và `canvas_xaydungphuluc.html`
  - Đặt giá trị khởi tạo có thể chỉnh sửa cho Năm học `2026-2027`, Tên trường `THCS Trần Phú`, Tổ chuyên môn `Tổ Toán - Tin` và Giáo viên / Tổ trưởng `Hoàng Tấn Thiên`.
  - Giữ nguyên cơ chế bản nháp/storage; người dùng vẫn có thể nhập tay từng trường.
- `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js`
  - Kiểm tra giá trị khởi tạo, tính chỉnh sửa, và việc `getConfig()` phản ánh thay đổi thủ công.

## Kiểm tra đã chạy

- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `git diff --check`: PASS.

## Chưa thực hiện

- Chưa commit hoặc push.
