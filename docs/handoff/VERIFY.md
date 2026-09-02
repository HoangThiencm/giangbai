# VERIFY

## Kết luận
FAIL

## Đối chiếu scope
- `js/security-guard.js`: Chưa triển khai các bước sửa triệt để theo `PLAN.md` mới:
  + Hàm `probeDevToolsConsole()` (Error stack getter) vẫn còn tồn tại và chạy `setInterval(..., 3000)` -> Gây lỗi bắt nhầm 100% trên trình duyệt WebKit / Safari (iPhone, iPad, Mac).
  + `showLockOverlay()` và `onDevToolsDetected()` chưa có điều kiện `if (isMobileOrTablet) return;` -> Khi bẫy kích hoạt, màn hình mobile vẫn bị phủ đen và khóa vĩnh viễn.
  + `triggerDebuggerTrap()` chưa có điều kiện `if (isMobileOrTablet) return;` -> Khi CPU mobile bị nghẽn tải trang, bẫy đo thời gian > 100ms sẽ kích hoạt khóa màn hình.
- `tests/security-f12-smoke.js`: Chưa bổ sung test case kiểm tra việc loại bỏ `probeDevToolsConsole` và kiểm tra chặn `showLockOverlay` trực tiếp trên môi trường mobile sandbox.

## Test đã chạy
- `node tests/security-f12-smoke.js` — PASS (chỉ chạy các test cũ, chưa có test case phát hiện lỗi console getter WebKit).

## Pass / Fail từng tiêu chí
- [FAIL] Loại bỏ hoàn toàn cơ chế bẫy `probeDevToolsConsole` (Error stack getter) trong `js/security-guard.js`.
- [FAIL] Chặn hiển thị `showLockOverlay` và `onDevToolsDetected` khi `isMobileOrTablet` là true.
- [FAIL] Chặn chạy `triggerDebuggerTrap` khi `isMobileOrTablet` là true.
- [PASS] Cơ chế bảo mật trên Desktop (chặn F12, Ctrl+U, Ctrl+Shift+I, phím tắt admin).

## Bug
- Lỗi: `probeDevToolsConsole()` và `triggerDebuggerTrap()` vẫn chưa được loại bỏ/chặn trên mobile trong `js/security-guard.js`. Trên iPhone / Safari, WebKit tự động truy cập getter `.stack` khi xử lý buffer console, làm `detected = true` và kích hoạt overlay khóa "Phát hiện DevTools" sau 3 giây tải trang.
- Tái hiện: Mở trang web trên trình duyệt Safari (iOS / macOS) hoặc thiết bị Android có tải CPU.
- File liên quan: `js/security-guard.js` (dòng 113, 146, 213-227, 247-262).
