# PLAN: Gỡ bỏ hoàn toàn cơ chế tự động refresh (Auto-Reload) và trả về nguyên trạng

## Hiện trạng

1. **Hiện tượng người dùng gặp phải**:
   - Toàn bộ các trang trong hệ thống (bao gồm trang Quản lý tổ chuyên môn `phancongtochuyenmon.html` và các trang khác) liên tục tự động refresh / reload dù người dùng không thao tác gì hoặc đang nhập liệu.
   - Nguyên nhân:
     - Trong file `js/security-guard.js` (được nạp trên toàn bộ các trang HTML của hệ thống), cơ chế `initAutoUpdateChecker()` lắng nghe các sự kiện `focus`, `visibilitychange` và `setInterval(60000)` để gọi `checkAppVersionUpdate()`.
     - Khi kiểm tra manifest `/version.json`, việc fetch hoặc đọc/ghi bộ nhớ `localStorage`/`sessionStorage` giữa các tab hoặc do chênh lệch phiên bản kích hoạt lệnh `window.location.reload()`, gây ra tình trạng tải lại trang liên tục (refresh loop), làm gián đoạn người dùng và mất dữ liệu đang nhập dở.
2. **Yêu cầu của người dùng**:
   - Gỡ bỏ hoàn toàn tính năng tự động refresh này, trả về nguyên trạng như cũ. Không cho phép script tự động reload trang dưới bất kỳ hình thức nào.

---

## Mục tiêu & Giải pháp thiết kế

1. **Gỡ bỏ hoàn toàn module Auto-Update Checker trong `js/security-guard.js`**:
   - Xóa bỏ các biến và hàm:
     - `appVersionStorageKey`, `appVersionReloadAtKey`, `appVersionReloadDebounceMs`, `appVersionCheckInFlight`.
     - `getVersionValue(payload)`.
     - `checkAppVersionUpdate()`.
     - `initAutoUpdateChecker()`.
     - Lệnh gọi `initAutoUpdateChecker();`.
   - Đảm bảo `js/security-guard.js` chỉ thực hiện các chức năng bảo vệ cơ bản như cũ, hoàn toàn không có bất kỳ lệnh `fetch('/version.json')` hay `window.location.reload()` tự động nào.
2. **Cập nhật bộ test tự động**:
   - Cập nhật file test `tests/auto-reload-smoke.js` (hoặc loại bỏ việc kiểm tra auto-reload bắt buộc) để xác nhận hệ thống an toàn, không còn tự reload.
   - Chạy lại toàn bộ test suites (`baogiang-weekday-segment-smoke.js`, `timetable-render-smoke.js`).
3. **Giữ nguyên các cải tiến đã đạt tiêu chuẩn trước đó**:
   - Giữ nguyên giao diện Thời khoá biểu 2 cột thu gọn không cần trượt con lăn.
   - Giữ nguyên thuật toán căn chỉnh tiết AI buổi chiều (7–9).
   - Giữ nguyên các tính năng Báo giảng và PPCT đa tuần.

---

## Phạm vi thực hiện

1. `js/security-guard.js`:
   - Gỡ bỏ hoàn toàn logic kiểm tra phiên bản và tự động reload trang (dòng 34 đến dòng 105).
2. `tests/auto-reload-smoke.js`:
   - Cập nhật test để xác nhận `js/security-guard.js` không còn kích hoạt `window.location.reload()`.

---

## Ngoài phạm vi

- Không sửa đổi các logic chuyên môn khác trong `phancongtochuyenmon.html`.
- Giữ nguyên cấu hình build cơ bản trong `.github/workflows/ftp-deploy.yml`.

---

## File dự kiến tác động

1. `js/security-guard.js`
2. `tests/auto-reload-smoke.js`

---

## Các bước thực hiện

### Bước 1: Xóa bỏ module auto-reload trong `js/security-guard.js`
- Xóa toàn bộ đoạn code từ `// Kiểm tra manifest deploy độc lập...` đến hết `initAutoUpdateChecker();` (dòng 34 đến 105).
- Trả `js/security-guard.js` về trạng thái an toàn, không có cơ chế tự refresh.

### Bước 2: Cập nhật kiểm thử `tests/auto-reload-smoke.js`
- Điều chỉnh nội dung kiểm thử để xác nhận rằng `js/security-guard.js` không còn chứa `initAutoUpdateChecker` và không còn tự gọi `reload()`.

### Bước 3: Chạy toàn bộ các test suites
- `node tests/baogiang-weekday-segment-smoke.js`
- `node tests/timetable-render-smoke.js`
- `node tests/auto-reload-smoke.js`
- `git diff --check`

---

## Tiêu chí nghiệm thu

1. `js/security-guard.js` hoàn toàn không còn mã tự động fetch `/version.json` và không còn tự gọi `window.location.reload()`.
2. Toàn bộ hệ thống hoạt động ổn định, mở trang bình thường, không bao giờ bị tự động reload/refresh ngoài ý muốn.
3. Toàn bộ các bộ test tự động đạt **PASS 100%**.
