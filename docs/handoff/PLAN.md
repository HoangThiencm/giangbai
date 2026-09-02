# PLAN: Xử Lý Triệt Để Lỗi Báo "Phát Hiện DevTools" Trên Điện Thoại Di Động (iOS / Android / Safari) Trong `js/security-guard.js`

## Hiện trạng
1. **Lỗi báo DevTools giả vẫn tiếp tục xảy ra trên iPhone / Android**:
   - Mặc dù lần trước đã thêm `if (isMobileOrTablet) return;` trong hàm `checkDevToolsOpen()`, người dùng mở trang trên điện thoại (iPhone Safari, Android Chrome) vẫn bị popup đen khóa màn hình:
     > *"Phát hiện DevTools. Hãy đóng công cụ phát triển để tiếp tục."*
   - **Nguyên nhân cốt lõi trong `js/security-guard.js`**:
     * **Nguyên nhân 1 - Bẫy Console Getter (`probeDevToolsConsole`)**:
       Hàm `probeDevToolsConsole` (dòng 247-262) chạy định kỳ 3 giây: tạo object `new Error()` với getter `stack` rồi gọi `nativeConsole.debug(probe)`.
       Trên trình duyệt WebKit (Safari trên iOS và macOS), trình duyệt **luôn tự động truy cập thuộc tính `.stack` của Error object khi ghi log vào console buffer, bất kể người dùng có mở DevTools hay không**. Điều này khiến `detected = true` ngay lập tức và gọi `onDevToolsDetected()` -> `showLockOverlay()` khóa màn hình của 100% người dùng iPhone / iPad / Safari.
     * **Nguyên nhân 2 - Bẫy Debugger Trap (`triggerDebuggerTrap`)**:
       Hàm `triggerDebuggerTrap` (dòng 213-227) chạy định kỳ 2.5 giây: thực thi `Function('debugger')()` và đo `performance.now() > 100ms`. Trên chip di động, khi máy đang tải trang, cuộn trang hoặc tiết kiệm pin, việc biên dịch động và chạy hàm mất > 100ms dẫn đến báo giả và gọi `onDevToolsDetected()`.
     * **Nguyên nhân 3 - Hàm `showLockOverlay()` và `onDevToolsDetected()` chưa có chốt chặn an toàn `isMobileOrTablet`**:
       Khi `probeDevToolsConsole` hoặc `triggerDebuggerTrap` gọi `onDevToolsDetected()`, hàm `showLockOverlay()` lập tức tạo overlay khóa màn hình. Đồng thời, vì `checkDevToolsOpen()` có `if (isMobileOrTablet) return;`, hàm `hideLockOverlay()` **không bao giờ được gọi trên mobile**, khiến màn hình bị khóa vĩnh viễn không thể tắt.

## Phạm vi
1. **Sửa triệt để module `js/security-guard.js`**:
   - **Chặn toàn diện ở cấp độ overlay**:
     * Trong `showLockOverlay()` và `onDevToolsDetected()`: Bổ sung điều kiện `if (isMobileOrTablet) return;` để đảm bảo trên thiết bị di động / tablet, overlay cảnh báo DevTools **tuyệt đối không bao giờ được phép hiển thị**.
   - **Loại bỏ / vô hiệu hóa các bẫy gây False Positive**:
     * **Loại bỏ hoàn toàn cơ chế `probeDevToolsConsole`** (Error stack getter): Đây là kỹ thuật không đáng tin cậy, gây lỗi 100% trên Safari/WebKit (iOS & Mac).
     * **Bỏ qua `triggerDebuggerTrap` trên mobile / tablet**: Chỉ chạy bẫy timing debugger trên môi trường Desktop không phải Safari WebKit hoặc nâng ngưỡng an toàn để không bắt nhầm CPU lag.
   - **Giữ vững bảo mật Desktop**:
     * Duy trì đầy đủ các tính năng bảo vệ trên Desktop: Chặn F12, chặn Ctrl+Shift+I, chặn Ctrl+U, chặn chuột phải sao chép ngoài ô input, phím tắt quản trị `Ctrl+Alt+Shift+D` mở khóa debug.
2. **Cập nhật và mở rộng bộ kiểm thử tự động `tests/security-f12-smoke.js`**:
   - Thêm test case giả lập gọi trực tiếp `onDevToolsDetected()` / `showLockOverlay()` trong môi trường Mobile/Tablet -> đảm bảo không tạo hoặc hiển thị overlay `__gb_devtools_lock__`.
   - Thêm test case xác nhận không còn bẫy console getter gây lỗi WebKit.
   - Đảm bảo 100% các bài test trong `tests/security-f12-smoke.js` chạy đạt PASS.

## Ngoài phạm vi
- Không can thiệp vào các logic nghiệp vụ khác của website.

## File dự kiến tác động
- `js/security-guard.js` [SỬA TRIỆT ĐỂ: LOẠI BỎ PROBE CONSOLE GETTER, CHẶN SHOW OVERLAY TRÊN MOBILE/TABLET]
- `tests/security-f12-smoke.js` [BỔ SUNG TEST CASE KIỂM TRA CHẶN OVERLAY HOÀN TOÀN TRÊN MOBILE]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Cập nhật `js/security-guard.js`**:
   - Cập nhật `showLockOverlay()` và `onDevToolsDetected()`:
     ```js
     function showLockOverlay() {
         if (isDebugUnlocked || isMobileOrTablet) return;
         // ...
     }
     function onDevToolsDetected() {
         if (isDebugUnlocked || isMobileOrTablet) return;
         // ...
     }
     ```
   - Xóa bỏ hoàn toàn hàm `probeDevToolsConsole()` và `setInterval(probeDevToolsConsole, ...)` vì xung đột với WebKit Safari.
   - Trong `triggerDebuggerTrap()`: thêm `if (isDebugUnlocked || isMobileOrTablet) return;`.
   - Trong `checkDevToolsOpen()`: đảm bảo `if (isDebugUnlocked || isMobileOrTablet) return;`.
2. **Bước 2: Cập nhật `tests/security-f12-smoke.js`**:
   - Cập nhật test case tĩnh và sandbox test:
     * Kiểm tra `showLockOverlay` không hiển thị trên mobile/tablet ngay cả khi kích hoạt sự kiện phát hiện.
     * Kiểm tra sandbox iPhone và iPadOS không tạo phần tử `__gb_devtools_lock__`.
     * Kiểm tra Desktop vẫn phát hiện và hiển thị khóa khi mở DevTools.
   - Chạy lệnh `node tests/security-f12-smoke.js` kiểm tra toàn bộ test PASS.
3. **Bước 3: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro trình duyệt Safari Desktop cũng bị ảnh hưởng bởi WebKit getter**:
   - *Giải pháp*: Việc xóa bỏ hoàn toàn `probeDevToolsConsole` sẽ giải quyết dứt điểm lỗi cho cả Safari trên iPhone/iPad và Safari trên máy Mac.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/security-f12-smoke.js`
   - Chạy lệnh: `node tools/build-obfuscate.js --dry-run`
2. **Kiểm thử thủ công**:
   - Mở bất kỳ trang nào (`index.html`, `admin.html`,...) trên điện thoại iPhone (Safari / Chrome) và điện thoại Android:
     * Trang tải mượt mà, hoàn toàn không xuất hiện popup "Phát hiện DevTools".
     * Thao tác làm bài, bấm nút, cuộn trang không bị khóa.
   - Mở trên máy tính Desktop Chrome/Edge:
     * Bấm F12 hoặc Inspect -> Vẫn hiển thị thông báo khóa DevTools theo đúng thiết kế.

## Tiêu chí nghiệm thu
- [ ] Truy cập trên điện thoại iPhone (iOS Safari) và Android 100% không còn bị popup/overlay "Phát hiện DevTools. Hãy đóng công cụ phát triển để tiếp tục."
- [ ] Đã loại bỏ hoàn toàn cơ chế bẫy `probeDevToolsConsole` (Error stack getter) gây lỗi trên WebKit.
- [ ] Toàn bộ các cơ chế bảo mật trên Desktop (F12, Ctrl+U, Ctrl+Shift+I, DevTools size check) vẫn hoạt động chính xác.
- [ ] 100% kiểm thử tự động `tests/security-f12-smoke.js` chạy đạt PASS.
