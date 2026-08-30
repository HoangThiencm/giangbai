# PLAN: Đưa xaydungphuluc.html ra Thư mục Gốc (Đồng cấp index.html), Tự động Dùng Chung API Key từ soankhbd.html, và Bật Security Guard Chống Lộ Code

## Hiện trạng
1. **Vị trí tệp**: `xaydungphuluc.html` hiện đang nằm trong thư mục con `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`. Người dùng muốn đưa ra ngoài thư mục gốc (đồng cấp với `index.html`, `soankhbd.html`, `admin.html`) để đường dẫn trực quan `https://hoangthiencm.id.vn/xaydungphuluc.html` và thuận tiện tích hợp.
2. **Chia sẻ API Key**: Trong [js/khbd-gemini.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/js/khbd-gemini.js) của `soankhbd.html`, API keys được lưu trong `localStorage` theo cấu trúc:
   - `khbd_user_gemini_keys_${userEmail}` (khóa chính theo tài khoản giáo viên đăng nhập)
   - `khbd_user_gemini_keys_default`
   - `khbd_gemini_api_keys`
   - `gemini_api_keys`
   - `global_gemini_keys`
   Khi giáo viên đã nhập key trong `soankhbd.html`, `xaydungphuluc.html` cần tự động đọc các key này để giáo viên không phải nhập lại.
3. **Bảo vệ mã nguồn (Chống F12 / DevTools)**: Trong ảnh chụp thực tế của người dùng, cửa sổ DevTools (F12) mở được và thấy toàn bộ mã HTML/JS vì trong `<head>` của `xaydungphuluc.html` chưa nhúng [js/security-guard.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/js/security-guard.js) và [access-control.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/access-control.js) như các trang khác (`soankhbd.html`, `index.html`, `admin.html`).
4. **Phân quyền Admin & Backend**: Cần hoàn thiện cả `api/helpers.php`, `admin.html`, `access-control.js` để đường dẫn trang được đồng bộ chuẩn `xaydungphuluc.html`.

## Phạm vi
1. **Đưa tệp `xaydungphuluc.html` ra Thư mục Gốc**:
   - Di chuyển / tạo `xaydungphuluc.html` trực tiếp tại thư mục gốc của dự án (`/xaydungphuluc.html`).
   - Cập nhật liên kết Trang chủ trong header: `<a href="index.html" class="btn secondary">🏠 Trang chủ</a>`.
   - Cập nhật tất cả các đường dẫn tương đối tài nguyên:
     + `<script src="js/security-guard.js"></script>`
     + `<script src="access-control.js"></script>`
   - Dọn dẹp/chuyển đổi tệp cũ trong `GIAO AN/XAYDUNGPHULUC/` hoặc để file chuyển hướng về trang gốc.
2. **Bảo mật Chống Xem Mã Nguồn / DevTools (Security Guard)**:
   - Nhúng `<script src="js/security-guard.js"></script>` làm thẻ đầu tiên trong `<head>` của `xaydungphuluc.html`.
   - Nhúng `<script src="access-control.js"></script>` để kiểm tra phân quyền giáo viên theo tài khoản đăng nhập.
   - Khi chạy trên domain `hoangthiencm.id.vn`, `security-guard.js` sẽ tự động vô hiệu hóa F12, Ctrl+Shift+I, Ctrl+U, chuột phải và chặn Inspect Element.
3. **Tự động Dùng Chung API Key từ `soankhbd.html`**:
   - Hàm `loadKeys()` trong `xaydungphuluc.html` sẽ quét toàn bộ danh sách key lưu trữ theo tài khoản:
     + `const email = String(localStorage.getItem('userEmail') || 'default').trim().toLowerCase();`
     + `khbd_user_gemini_keys_${email}`
     + `khbd_user_gemini_keys_default`
     + `khbd_gemini_api_keys`
     + `gemini_api_keys`
     + `xdpl_gemini_api_keys`
     + `global_gemini_keys`
   - Nếu phát hiện danh sách API keys hợp lệ (dạng `AIza...`), tự động nạp vào bộ nhớ và hiển thị số lượng key sẵn sàng, tuyệt đối không bắt người dùng nhập lại.
4. **Đồng bộ Hệ thống Portal & Phân quyền Quản trị Admin**:
   - **`index.html`**:
     + Cập nhật thẻ công cụ: `<a href="xaydungphuluc.html" target="_blank" rel="noopener noreferrer" data-tool="xaydungphuluc" class="tool-tile tool-tile--colored tool-tile--xaydungphuluc">`.
     + Cập nhật `TOOL_PAGE_LINKS.xaydungphuluc = 'xaydungphuluc.html'`.
   - **`admin.html`**:
     + Cập nhật `hostingPages.xaydungphuluc = { title: 'Xây dựng Phụ lục 1, 2, 3 (CV 5512 - THCS)', url: 'xaydungphuluc.html' }`.
     + Đảm bảo `hostingPages` được merge an toàn: `hostingPages = Object.assign({}, hostingPages, data.pages || {});`.
     + Đảm bảo `teacherFeatureGroups`, `USER_FEATURE_GROUPS`, `defaultTeacherPages`, `CLIENT_FEATURE_CHECKS`, `FEATURE_NAMES` đều có `xaydungphuluc`.
   - **`api/helpers.php`**:
     + Đăng ký `xaydungphuluc` với `url => 'xaydungphuluc.html'` trong `page_catalog()`.
     + Đăng ký trong `teacher_workspace_page_ids()`, `teacher_default_workspace_extras()`, `teacher_feature_keys_for_pages()`.
   - **`access-control.js`**:
     + Đăng ký `pageKeys['xaydungphuluc.html'] = 'xaydungphuluc'`.
     + Đăng ký `pageUrls['xaydungphuluc'] = 'xaydungphuluc.html'`.
   - **`global_config.json`**:
     + Bổ sung `"xaydungphuluc": true` vào `features`.
5. **Cập nhật Bộ Kiểm thử Tự động ([tests/xaydungphuluc-integration-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-integration-smoke.js))**:
   - Kiểm tra file `xaydungphuluc.html` ở thư mục gốc có nhúng `security-guard.js`, `access-control.js`, hàm load key `khbd_user_gemini_keys_...`.
   - Kiểm tra `index.html`, `admin.html`, `api/helpers.php`, `access-control.js`, `global_config.json` đồng bộ chính xác.

## Ngoài phạm vi
- Không thay đổi các chức năng nội tại của `soankhbd.html` hay các công cụ khác.
- Không thay đổi bảng cơ sở dữ liệu MySQL.

## File dự kiến tác động
- `xaydungphuluc.html` [TẠO Ở GỐC / NHÚNG SECURITY-GUARD & AUTO-LOAD KEY SOANKHBD]
- `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html` [CHUYỂN HƯỚNG HOẶC ĐỒNG BỘ NỘI DUNG VỀ GỐC]
- `index.html` [CẬP NHẬT ĐƯỜNG DẪN XAYDUNGPHULUC.HTML]
- `admin.html` [CẬP NHẬT ĐƯỜNG DẪN XAYDUNGPHULUC.HTML & MERGE HOSTING_PAGES]
- `api/helpers.php` [CẬP NHẬT URL XAYDUNGPHULUC.HTML VÀ QUYỀN GIÁO VIÊN]
- `access-control.js` [CẬP NHẬT ÁNH XẠ XAYDUNGPHULUC.HTML]
- `global_config.json` [THÊM XAYDUNGPHULUC VÀO FEATURES]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT ĐƯỜNG DẪN FILE TEST GỐC]
- `tests/xaydungphuluc-integration-smoke.js` [CẬP NHẬT KIỂM TRA ĐẦY ĐỦ SECURITY & KEY SHARING]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Tạo và hoàn thiện `xaydungphuluc.html` tại thư mục gốc**:
   - Thêm `<script src="js/security-guard.js"></script>` và `<script src="access-control.js"></script>` vào ngay đầu `<head>`.
   - Nút Trang chủ trỏ về `index.html`.
   - Nâng cấp hàm `loadKeys()`: Tự động nạp danh sách key từ `khbd_user_gemini_keys_${userEmail}`, `khbd_user_gemini_keys_default`, `khbd_gemini_api_keys`, `gemini_api_keys`, `xdpl_gemini_api_keys`, `global_gemini_keys`.
2. **Bước 2: Cập nhật `api/helpers.php`**:
   - Cập nhật `page_catalog()`: `'xaydungphuluc' => ['title' => 'Xây dựng Phụ lục 1, 2, 3 (CV 5512 - THCS)', 'url' => 'xaydungphuluc.html']`.
   - Cập nhật `teacher_workspace_page_ids()`, `teacher_default_workspace_extras()`, `teacher_feature_keys_for_pages()`.
3. **Bước 3: Cập nhật `access-control.js` & `global_config.json`**:
   - Đăng ký `pageKeys['xaydungphuluc.html'] = 'xaydungphuluc'` và `pageUrls['xaydungphuluc'] = 'xaydungphuluc.html'`.
   - Thêm `"xaydungphuluc": true` vào `global_config.json`.
4. **Bước 4: Cập nhật `index.html` & `admin.html`**:
   - `index.html`: `href="xaydungphuluc.html"`, `TOOL_PAGE_LINKS.xaydungphuluc = 'xaydungphuluc.html'`.
   - `admin.html`: `hostingPages.xaydungphuluc.url = 'xaydungphuluc.html'`, merge `hostingPages = Object.assign({}, hostingPages, data.pages || {});`.
5. **Bước 5: Cập nhật và chạy kiểm thử tự động**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro 1**: Người dùng truy cập bookmark hoặc URL cũ `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`.
  - *Giải pháp*: Trong `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`, thêm mã tự động chuyển hướng sang `../../xaydungphuluc.html`.
- **Rủi ro 2**: Trình duyệt lưu cache localStorage theo domain.
  - *Giải pháp*: `xaydungphuluc.html` và `soankhbd.html` cùng nằm trên cùng domain (`hoangthiencm.id.vn`) nên truy cập chung `localStorage` hoàn toàn tự nhiên và tức thì.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/xaydungphuluc-smoke.js` và `node tests/xaydungphuluc-integration-smoke.js`:
     + Xác nhận file `xaydungphuluc.html` ở thư mục gốc tồn tại và hợp lệ.
     + Xác nhận `security-guard.js` và `access-control.js` được nhúng trong `<head>`.
     + Xác nhận hàm nạp key quét qua `khbd_user_gemini_keys_...`.
     + Xác nhận `index.html`, `admin.html`, `api/helpers.php`, `access-control.js` đều trỏ đúng `xaydungphuluc.html`.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `xaydungphuluc.html` trực tiếp trên domain `https://hoangthiencm.id.vn/xaydungphuluc.html`.
   - Thử bấm F12 hoặc chuột phải $\rightarrow$ Xác nhận Security Guard chặn và bảo vệ mã nguồn.
   - Nhập API Key bên `soankhbd.html`, sau đó mở `xaydungphuluc.html` $\rightarrow$ Xác nhận badge hiển thị ngay số lượng key sẵn sàng mà không cần nhập lại.
   - Mở `admin.html` $\rightarrow$ Xác nhận mục phân quyền giáo viên hiển thị toggle `Xây dựng Phụ lục 1, 2, 3 (CV 5512 - THCS)`.

## Tiêu chí nghiệm thu
1. File `xaydungphuluc.html` nằm ở thư mục gốc (đồng cấp với `index.html`), mở trực tiếp tại `https://hoangthiencm.id.vn/xaydungphuluc.html`.
2. Nhúng đầy đủ `js/security-guard.js` và `access-control.js`, bảo vệ chống mở F12/DevTools khi chạy production.
3. Tự động nhận diện và dùng chung API Key đã lưu từ `soankhbd.html` (`khbd_user_gemini_keys_...`), người dùng không phải nhập lại.
4. Tích hợp phân quyền hoàn chỉnh trên `admin.html`, `index.html`, `api/helpers.php` và `access-control.js`.
5. Toàn bộ smoke test tự động đều PASS 100%.
