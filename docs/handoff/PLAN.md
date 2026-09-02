# PLAN: Khắc Phục Triệt Để Báo DevTools Trên Chrome iOS (CriOS) Và Các Trình Duyệt Mobile/Touch

## Hiện trạng
1. **Chrome trên iPhone / iPad (CriOS) vẫn bị báo "Phát hiện DevTools"**:
   - Sau khi Safari trên iPhone đã hoạt động bình thường, người dùng mở bằng **Google Chrome trên iPhone** (`CriOS`) thì vẫn bị khóa màn hình và xuất hiện thông báo:
     > *"Phát hiện DevTools. Hãy đóng công cụ phát triển để tiếp tục."*
   - **Nguyên nhân kỹ thuật trong `js/security-guard.js`**:
     * Trình duyệt Google Chrome trên iOS sử dụng định danh User-Agent chứa token `CriOS` (ví dụ: `Mozilla/5.0 (iPhone; CPU iPhone OS 18_0...) CriOS/120.0...` hoặc khi bật chế độ Desktop site sẽ gửi `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/... CriOS/... Safari/...`).
     * Regex hiện tại `/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet/i` chưa bao quát các token đặc thù của các trình duyệt bên thứ ba trên iOS (`CriOS` - Chrome, `FxiOS` - Firefox, `EdgiOS` - Edge, `OPiOS` - Opera).
     * Đồng thời, điều kiện nhận diện qua `navigator.maxTouchPoints > 1` không bắt được trường hợp `maxTouchPoints = 1` hoặc khi WKWebView ở chế độ desktop mode không trả về `maxTouchPoints > 1`.
     * Khi đó `isMobileOrTablet` bị đánh giá là `false`, dẫn tới việc `checkDevToolsOpen()` so sánh `outerHeight - innerHeight > 170` (trên Chrome iOS thanh URL bar + bottom menu chênh lệch ~180px - 220px) và lập tức kích hoạt khóa màn hình.

## Phạm vi
1. **Nâng cấp toàn diện bộ nhận diện Thiết bị Di động & Cảm ứng (`isMobileOrTablet`) trong `js/security-guard.js`**:
   - Bổ sung nhận diện tất cả trình duyệt di động iOS / Android:
     * Regex User-Agent mở rộng: `/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet|CriOS|FxiOS|EdgiOS|OPiOS|Silk|Kindle/i`.
   - Kết hợp đa tầng nhận diện Touch & Media Queries:
     * `Boolean(navigator.maxTouchPoints && navigator.maxTouchPoints > 0)`
     * `Boolean('ontouchstart' in window || (window.DocumentTouch && document instanceof window.DocumentTouch))`
     * `Boolean(window.matchMedia && window.matchMedia('(pointer: coarse)').matches)`
     * `Boolean(window.matchMedia && window.matchMedia('(hover: none)').matches)`
     * `Boolean(window.screen && Math.min(window.screen.width, window.screen.height) <= 1024 && (navigator.maxTouchPoints > 0 || 'ontouchstart' in window))`
   - Đảm bảo 100% tất cả các trình duyệt trên điện thoại/máy tính bảng (Safari, Chrome iOS, Firefox iOS, Edge iOS, Android Chrome, Samsung Internet) đều được nhận diện chính xác là Mobile/Touch và không bao giờ bị kích hoạt khóa DevTools.
   - Vẫn duy trì đầy đủ tính năng bảo vệ trên máy tính Desktop (chuột, phím F12, Ctrl+Shift+I, Ctrl+U, devtools size check trên desktop).
2. **Cập nhật bộ kiểm thử `tests/security-f12-smoke.js`**:
   - Thêm test case giả lập Chrome iOS (`CriOS`), Firefox iOS (`FxiOS`), Edge iOS (`EdgiOS`).
   - Thêm test case giả lập chế độ Desktop của Chrome iOS (`Macintosh` + `CriOS`).
   - Thêm test case giả lập màn hình Touch (`maxTouchPoints: 1`, `pointer: coarse`).
   - Đảm bảo toàn bộ 100% test suite chạy đạt PASS.

## Ngoài phạm vi
- Không can thiệp vào các logic AI hoặc các trang công cụ khác.

## File dự kiến tác động
- `js/security-guard.js` [MỞ RỘNG NHẬN DIỆN CROS / FXIOS / EDGIOS VÀ ĐA TẦNG TOUCH / COARSE POINTER]
- `tests/security-f12-smoke.js` [THÊM TEST CASES CHO CHROME IOS, FXIOS, TOUCH POINTER]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Cập nhật hàm nhận diện `isMobileOrTablet` trong `js/security-guard.js`**:
   - Cập nhật logic:
     ```js
     var isMobileOrTablet = false;
     try {
         var userAgent = String((navigator && navigator.userAgent) || '');
         var maxTouchPoints = Number((navigator && navigator.maxTouchPoints) || 0);
         var hasTouch = Boolean(
             maxTouchPoints > 0 ||
             'ontouchstart' in window ||
             (window.DocumentTouch && document instanceof window.DocumentTouch)
         );
         var isCoarsePointer = Boolean(
             window.matchMedia && (
                 window.matchMedia('(pointer: coarse)').matches ||
                 window.matchMedia('(hover: none)').matches
             )
         );
         var isMobileUa = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet|CriOS|FxiOS|EdgiOS|OPiOS|Silk|Kindle/i.test(userAgent);
         var isAppleTouchDesktop = /Macintosh/i.test(userAgent) && hasTouch;

         isMobileOrTablet = isMobileUa || isAppleTouchDesktop || (hasTouch && isCoarsePointer);
     } catch (err) {}
     ```
2. **Bước 2: Cập nhật `tests/security-f12-smoke.js`**:
   - Bổ sung test sandbox với User-Agent Chrome iOS (`CriOS/120.0...`), Firefox iOS (`FxiOS`), Edge iOS (`EdgiOS`).
   - Bổ sung test sandbox với `Macintosh` + `CriOS` (Chrome iOS chế độ Desktop site).
   - Xác nhận không có overlay nào được tạo ra.
   - Chạy lệnh `node tests/security-f12-smoke.js` để xác thực toàn bộ test PASS.
3. **Bước 3: Khóa trạng thái giao việc**:
   - Ghi nội dung `LOCK` vào `docs/handoff/.lock`.

## Rủi ro
1. **Rủi ro trình duyệt Desktop có màn hình cảm ứng (Touchscreen Laptop / All-in-One)**:
   - *Giải pháp*: Desktop Windows/Macintosh có chuột và bàn phím (`pointer: fine`) sẽ không bị nhận nhầm là mobile thuần túy; các phím tắt F12, Ctrl+U vẫn được bảo vệ bình thường.

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh: `node tests/security-f12-smoke.js`
   - Chạy lệnh: `node tools/build-obfuscate.js --dry-run`
2. **Kiểm thử thực tế**:
   - Mở hệ thống trên iPhone bằng **Google Chrome**: Hoàn toàn không còn xuất hiện popup "Phát hiện DevTools".
   - Mở hệ thống trên iPhone bằng **Safari**: Hoạt động bình thường.
   - Mở hệ thống trên máy tính **Desktop**: Nhấn F12 / mở DevTools vẫn kích hoạt cảnh báo khóa như thiết kế.

## Tiêu chí nghiệm thu
- [ ] Truy cập trên iPhone qua trình duyệt Chrome (`CriOS`) không còn bị popup "Phát hiện DevTools".
- [ ] Truy cập trên iPhone qua Safari, Firefox, Edge và Android Chrome hoạt động mượt mà.
- [ ] Các cơ chế bảo vệ mã nguồn trên Desktop được bảo toàn 100%.
- [ ] 100% kiểm thử tự động trong `tests/security-f12-smoke.js` chạy đạt PASS.
