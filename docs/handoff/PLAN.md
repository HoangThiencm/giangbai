# PLAN: Khắc Phục Lỗi Cảnh Báo "Phát Hiện DevTools" Trên Điện Thoại Di Động Trong `js/security-guard.js`

## Hiện trạng
1. **Lỗi báo DevTools giả (False Positive) trên thiết bị di động**:
   - Khi học sinh, giáo viên hoặc quản trị viên truy cập hệ thống làm bài trên điện thoại di động (iPhone / iPad / Safari / Android Chrome), màn hình lập tức bị khóa và hiển thị cảnh báo:
     > *"Phát hiện DevTools. Hãy đóng công cụ phát triển để tiếp tục."*
   - **Nguyên nhân cốt lõi trong `js/security-guard.js`**:
     * Cơ chế đo chênh lệch kích thước cửa sổ (`checkDevToolsOpen` - dòng 220-234):
       `window.outerWidth - window.innerWidth > 170` hoặc `window.outerHeight - window.innerHeight > 170`.
     * Trên các trình duyệt di động (đặc biệt là iOS Safari, Chrome Mobile), `outerHeight` là toàn bộ chiều cao màn hình thiết bị, trong khi `innerHeight` bị thu hẹp bởi thanh địa chỉ (URL bar), thanh điều hướng dưới đáy (tab bar/navigation bar), tai thỏ (Notch / Dynamic Island) và bàn phím ảo.
     * Mức chênh lệch tự nhiên này thường vượt quá `170px` (ví dụ trên iPhone 13/14/15 là ~180px - 220px), khiến `checkDevToolsOpen()` lập tức đánh giá là mở DevTools và kích hoạt `showLockOverlay()` chặn toàn bộ trang.
     * Ngoài ra, cơ chế bẫy đo độ trễ `triggerDebuggerTrap()` (`performance.now() > 100ms`) hoặc getter `probeDevToolsConsole()` có thể gây lag hoặc nhận diện sai trên các dòng máy di động cấu hình thấp hoặc trình duyệt WebKit Mobile.

## Phạm vi
1. **Cập nhật và tối ưu `js/security-guard.js`**:
   - Bổ sung hàm kiểm tra thiết bị di động / máy tính bảng (`isMobile` / touch device):
     * Nhận diện qua User-Agent (`/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet/i`) và/hoặc `navigator.maxTouchPoints > 0`.
   - Vô hiệu hóa hoặc bỏ qua cơ chế đo chênh lệch kích thước cửa sổ (`checkDevToolsOpen`) đối với môi trường thiết bị di động.
   - Giữ nguyên toàn bộ các cơ chế bảo mật cốt lõi trên Desktop (chặn F12, Ctrl+Shift+I, Ctrl+U, phím tắt Admin `Ctrl+Alt+Shift+D`, context menu chống sao chép).
   - Đảm bảo an toàn không gây false positive trên WebKit/Safari mobile và Android.
2. **Bổ sung và cập nhật Bộ Kiểm thử Tự động (`tests/security-f12-smoke.js`)**:
   - Thêm test case giả lập môi trường Mobile (User-Agent iOS/Android, `outerHeight - innerHeight = 200px`) -> xác nhận KHÔNG bị kích hoạt lock overlay.
   - Thêm test case xác nhận trên môi trường Desktop với `outerHeight - innerHeight > 170px` -> vẫn kích hoạt lock overlay như thiết kế.
   - Chạy toàn bộ test suite để kiểm tra tính tương thích với `tools/build-obfuscate.js` và hệ thống CI/CD.

## Ngoài phạm vi
- Không thay đổi giao diện các bài kiểm tra, trang làm bài hay luồng đăng nhập quản trị viên.
- Không xóa bỏ chức năng bảo vệ bản quyền mã nguồn trên máy tính Desktop.

## File dự kiến tác động
- `js/security-guard.js` [TỐI ƯU NHẬN DIỆN MOBILE, BỎ QUA KIỂM TRA KÍCH THƯỚC DEVTOOLS TRÊN DI ĐỘNG]
- `tests/security-f12-smoke.js` [BỔ SUNG TEST CASE KIỂM TRA MOBILE VÀ DESKTOP CHO SECURITY GUARD]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Cập nhật `js/security-guard.js`**:
   - Bổ sung logic kiểm tra `isMobile`:
     ```js
     var isMobile = Boolean(
         typeof navigator !== 'undefined' && (
             /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet/i.test(navigator.userAgent || '') ||
             (navigator.maxTouchPoints && navigator.maxTouchPoints > 1 && !/Windows NT|Macintosh/i.test(navigator.userAgent || ''))
         )
     );
     ```
   - Trong `checkDevToolsOpen()`: nếu `isMobile` thì lập tức `return;` (không thực hiện so sánh `outerWidth`/`outerHeight` với threshold).
   - Đảm bảo các hàm bẫy debugger và console probe hoạt động an toàn, không tự kích hoạt sai trên WebKit/Mobile.
2. **Bước 2: Cập nhật `tests/security-f12-smoke.js`**:
   - Thêm test case `testMobileNoFalsePositive`: Giả lập sandbox Mobile với User-Agent iPhone/Android và độ chênh kích thước màn hình lớn (`outerHeight: 844, innerHeight: 640`), kiểm tra overlay `__gb_devtools_lock__` không bị tạo / không hiển thị.
   - Giữ nguyên và mở rộng test case Desktop để đảm bảo tính năng chống DevTools trên máy tính vẫn hoạt động 100%.
   - Chạy lệnh `node tests/security-f12-smoke.js` để xác thực toàn bộ test passed.
3. **Bước 3: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro tablet (iPadOS) gửi User-Agent giống desktop Safari**:
   - *Giải pháp*: Kết hợp kiểm tra `navigator.maxTouchPoints > 1` cùng với kiểm tra touch event / screen dimensions để nhận diện chính xác tablet và tránh khóa nhầm.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/security-f12-smoke.js`
   - Chạy lệnh: `node tools/build-obfuscate.js --dry-run`
2. **Kiểm thử thủ công**:
   - Mở hệ thống làm bài hoặc trang quản trị trên trình duyệt điện thoại (iOS Safari / Android Chrome):
     * Giao diện tải bình thường, hoàn toàn không xuất hiện bảng đen cảnh báo DevTools.
     * Làm bài, cuộn trang, bật bàn phím ảo, xoay màn hình không bị gián đoạn hay khóa trang.
   - Mở hệ thống trên Desktop Chrome/Edge:
     * Nhấn F12 hoặc mở DevTools -> Vẫn hiển thị bảng cảnh báo khóa như thiết kế.

## Tiêu chí nghiệm thu
- [ ] Truy cập trên điện thoại di động (iPhone / Android) không còn bị hiện popup/overlay "Phát hiện DevTools. Hãy đóng công cụ phát triển để tiếp tục."
- [ ] Các thao tác trên điện thoại (cuộn trang, ẩn/hiện thanh công cụ Safari/Chrome, gõ bàn phím ảo) hoạt động bình thường, mượt mà.
- [ ] Cơ chế chống DevTools trên môi trường máy tính (Desktop) vẫn được bảo toàn.
- [ ] 100% kiểm thử tự động trong `tests/security-f12-smoke.js` chạy đạt PASS.
