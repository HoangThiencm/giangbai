# PLAN: Tích hợp ứng dụng Xây dựng Phụ lục (xaydungphuluc.html) vào Hệ thống Portal (Mở Tab Mới) và Phân quyền Quản trị Admin

## Hiện trạng
1. Đã hoàn thành xây dựng ứng dụng web độc lập [xaydungphuluc.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/xaydungphuluc.html) chuyên biệt cho khối THCS (Lớp 6 đến Lớp 9) chuẩn Công văn 5512/BGDĐT-GDTrH với đầy đủ chức năng quản lý API Key, cấu hình độc lập NLS và AI, bóc tách tài liệu và xuất Word .docx / Zip.
2. Hiện tại, ứng dụng chưa được gắn vào giao diện Cổng thông tin trung tâm ([index.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/index.html)) trong lưới công cụ dành cho giáo viên (`mainToolsGrid`).
3. Trong bảng điều khiển quản trị ([admin.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/admin.html)), danh mục tính năng toàn cục (`features`), danh mục phân quyền trang (`allowedPages` / `PAGE_CONFIG`), và cấu hình quyền cho từng giáo viên (`user_features`) chưa có mục quản lý bật/tắt và phân quyền cho công cụ `xaydungphuluc`.

## Phạm vi
1. **Tích hợp Thẻ công cụ vào Lưới công cụ Giáo viên trên Portal chính ([index.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/index.html))**:
   - Thêm thẻ công cụ `data-tool="xaydungphuluc"` vào cụm công cụ soạn giảng / sư phạm trong `#mainToolsGrid`.
   - Thiết lập mở ra tab mới: `target="_blank" rel="noopener noreferrer"`.
   - Đường dẫn liên kết: `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`.
   - Thiết kế giao diện thẻ đồng bộ với phong cách hệ thống: Tiêu đề *Xây dựng Phụ lục 1, 2, 3*, mô tả *Chuẩn CV 5512 · THCS Lớp 6–9 · Tích hợp NLS & AI*, icon sư phạm/tài liệu, hiệu ứng hover, glow và badge nhận diện.
   - Bổ sung `xaydungphuluc: 'GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html'` vào hằng số `TOOL_PAGE_LINKS` trong JavaScript của `index.html`.
   - Áp dụng logic kiểm soát hiển thị thẻ theo cấu hình phân quyền tài khoản giáo viên và cấu hình bật/tắt toàn cục của Admin.

2. **Tích hợp Phân quyền Quản trị Toàn diện trong Bảng điều khiển Admin ([admin.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/admin.html))**:
   - **Bật/Tắt Toàn cục (Admin Global Features)**:
     + Thêm ô checkbox cấu hình `id="cfg_xaydungphuluc"` trong khu vực *2. Cài đặt Ứng dụng Client (Admin Global)*.
     + Cập nhật danh sách hằng số tính năng `FEATURE_KEYS` và logic lưu/tải cấu hình toàn cục lên kho lưu trữ.
   - **Phân quyền Từng Tài khoản Giáo viên (User Permissions / Allowed Pages)**:
     + Bổ sung định nghĩa trang vào `PAGE_CONFIG`: `xaydungphuluc: { title: 'Xây dựng Phụ lục 1, 2, 3 (CV 5512 - THCS)', url: 'GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html' }`.
     + Đưa `xaydungphuluc` vào danh sách nhóm công cụ mở cho Giáo viên (`teacherPages` / `defaultTeacherPages`).
     + Hiển thị checkbox `xaydungphuluc` trong modal Tạo tài khoản mới (`#createAllowedPages`), modal Import danh sách tài khoản Excel (`#importAllowedPages`), và modal Chỉnh sửa quyền tài khoản (`#editAllowedPages`).
     + Đồng bộ tính năng `user_features` và `allowed_pages` khi Admin cấp/thu hồi quyền của giáo viên.

3. **Cập nhật Điều hướng & Xác thực Thân thiện trong ([xaydungphuluc.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/xaydungphuluc.html))**:
   - Thêm nút *Về Trang chủ Portal* trên thanh Header của `xaydungphuluc.html` (liên kết về `../../index.html`).
   - Kiểm tra xác thực nhẹ nhàng phía client: nếu chạy trong môi trường hệ thống đã đăng nhập, tự động lấy thông tin giáo viên / email từ `localStorage` (`userEmail`, `teacherName` nếu có) để điền sẵn vào biểu mẫu.

4. **Bộ kiểm thử tích hợp tự động ([tests/xaydungphuluc-integration-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-integration-smoke.js))**:
   - Viết bài kiểm thử Node.js tự động kiểm tra:
     + `index.html`: Thẻ công cụ `data-tool="xaydungphuluc"`, mở tab mới `target="_blank"`, `TOOL_PAGE_LINKS.xaydungphuluc`.
     + `admin.html`: Checkbox `cfg_xaydungphuluc`, cấu hình trong `PAGE_CONFIG`, mảng phân quyền giáo viên và logic đồng bộ quyền.
     + `xaydungphuluc.html`: Đường dẫn hợp lệ, liên kết quay về trang chủ.

## Ngoài phạm vi
- Không thay đổi các chức năng nội tại của các công cụ khác trong `index.html` và `admin.html`.
- Không thay đổi cấu trúc dữ liệu người dùng đang có trên cơ sở dữ liệu.

## File dự kiến tác động
- `index.html` [CHỈNH SỬA / TÍCH HỢP THẺ CÔNG CỤ & TOOL_PAGE_LINKS]
- `admin.html` [CHỈNH SỬA / TÍCH HỢP GLOBAL TOGGLE & PHÂN QUYỀN GIÁO VIÊN]
- `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html` [CẬP NHẬT HEADER LIÊN KẾT VỀ TRANG CHỦ]
- `tests/xaydungphuluc-integration-smoke.js` [TẠO MỚI]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Các bước thực hiện
1. **Bước 1: Cập nhật `index.html`**:
   - Thêm thẻ công cụ `xaydungphuluc` vào lưới `#mainToolsGrid` với thuộc tính `target="_blank" rel="noopener noreferrer"`, href trỏ đến `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`.
   - Cập nhật định nghĩa `TOOL_PAGE_LINKS`: thêm key `xaydungphuluc: 'GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html'`.
   - Bổ sung CSS định dạng màu sắc/hiệu ứng cho `.tool-tile--phuluc` / `.tool-tile--xaydungphuluc` hài hòa với giao diện chung.
2. **Bước 2: Cập nhật `admin.html`**:
   - Thêm ô checkbox `cfg_xaydungphuluc` vào khu vực *Cài đặt Ứng dụng Client (Admin Global)*.
   - Thêm `xaydungphuluc` vào danh sách `FEATURE_KEYS`.
   - Thêm `xaydungphuluc` vào `PAGE_CONFIG` và mảng quyền mặc định của Giáo viên (`defaultTeacherPages`).
   - Cập nhật hàm thu thập và lưu cài đặt tính năng toàn cục cũng như hàm đồng bộ `user_features`.
3. **Bước 3: Cập nhật `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`**:
   - Thêm nút liên kết `<a href="../../index.html" class="btn secondary">🏠 Trang chủ</a>` vào Header.
   - Tự động nạp sẵn tên giáo viên từ `localStorage.getItem('userName')` hoặc `localStorage.getItem('userEmail')` nếu có.
4. **Bước 4: Viết và chạy bộ kiểm thử tự động `tests/xaydungphuluc-integration-smoke.js`**:
   - Chạy kiểm thử tự động bằng Node.js và xác nhận PASS 100%.

## Rủi ro
- **Rủi ro 1**: Tài khoản giáo viên cũ chưa có cờ phân quyền `xaydungphuluc` trong danh sách `allowed_pages`.
  - *Giải pháp*: Trong hàm `ensureTeacherToolPages` hoặc `augmentTeacherAllowedSet`, tự động cấp quyền mặc định cho giáo viên khi tính năng toàn cục đang ở trạng thái bật (`features.xaydungphuluc !== false`), đồng thời cho phép Admin tùy chỉnh bật/tắt riêng cho từng tài khoản.
- **Rủi ro 2**: Đường dẫn tương đối từ `index.html` tới `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html` có khoảng trắng trong tên thư mục.
  - *Giải pháp*: Mã hóa URL chuẩn `GIAO%20AN/XAYDUNGPHULUC/xaydungphuluc.html` hoặc dùng đường dẫn hợp lệ đảm bảo mở chính xác trên mọi máy chủ web.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy lệnh `node tests/xaydungphuluc-integration-smoke.js`.
   - Xác nhận: Kiểm tra sự hiện diện của thẻ `data-tool="xaydungphuluc"` trong `index.html`, `target="_blank"`, `TOOL_PAGE_LINKS`, checkbox cấu hình trong `admin.html`, cấu hình `PAGE_CONFIG`, mảng phân quyền giáo viên $\rightarrow$ PASS 100%.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `index.html`: Xác nhận thẻ công cụ *Xây dựng Phụ lục 1, 2, 3* xuất hiện trong lưới công cụ.
   - Nhấp vào thẻ công cụ: Xác nhận trình duyệt mở ra **Tab Mới** với giao diện `xaydungphuluc.html`.
   - Mở `admin.html`: Đăng nhập admin, kiểm tra checkbox bật/tắt toàn cục *Xây dựng Phụ lục 1, 2, 3*, kiểm tra modal phân quyền cho giáo viên có mục chọn *Xây dựng Phụ lục 1, 2, 3*.
   - Thử nghiệm tắt tính năng trên Admin và kiểm tra thẻ công cụ trên `index.html` được ẩn tương ứng.

## Tiêu chí nghiệm thu
1. Trên giao diện chính `index.html` có thẻ công cụ *Xây dựng Phụ lục 1, 2, 3*, nhấp vào sẽ mở ứng dụng `xaydungphuluc.html` trong **Tab mới** (`target="_blank"`).
2. Trên bảng điều khiển `admin.html` có đầy đủ chức năng quản trị và phân quyền cho `xaydungphuluc`:
   - Công tắc Bật/Tắt toàn cục (Global feature toggle).
   - Tùy chọn phân quyền cho từng tài khoản Giáo viên (Tạo mới, Import Excel, Chỉnh sửa quyền).
3. Ứng dụng `xaydungphuluc.html` có nút liên kết quay về Trang chủ và tích hợp dữ liệu người dùng liền mạch.
4. Bộ kiểm thử tự động `tests/xaydungphuluc-integration-smoke.js` chạy thành công và PASS 100%.
