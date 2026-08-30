# VERIFY: Tích hợp ứng dụng Xây dựng Phụ lục vào Portal và Phân quyền Quản trị Admin

## Kết luận
PASS

## Đối chiếu scope
- Đã tích hợp thẻ công cụ `data-tool="xaydungphuluc"` vào lưới công cụ giáo viên (`#mainToolsGrid`) trên Cổng thông tin trung tâm [index.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/index.html).
- Thẻ công cụ thiết lập mở trong **Tab Mới** (`target="_blank" rel="noopener noreferrer"`), trỏ chính xác đến [GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/xaydungphuluc.html), kèm định dạng CSS phong cách đồng bộ (`.tool-tile--xaydungphuluc`).
- Đã bổ sung `xaydungphuluc` vào danh mục ánh xạ `TOOL_PAGE_LINKS` trong `index.html` để tự động kiểm soát hiển thị theo quyền giáo viên.
- Đã tích hợp đầy đủ phân quyền quản trị trên [admin.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/admin.html):
  + Công tắc Bật/Tắt Toàn cục (Admin Global Feature Toggle): `cfg_xaydungphuluc`.
  + Danh mục cấu hình trang (`PAGE_CONFIG`) và danh mục quyền mặc định của Giáo viên (`defaultTeacherPages`).
  + Hỗ trợ phân quyền `xaydungphuluc` khi Tạo tài khoản mới (`#createAllowedPages`), Import tài khoản từ file Excel (`#importAllowedPages`), và Chỉnh sửa quyền tài khoản (`#editAllowedPages`).
  + Đồng bộ `user_features` và `allowed_pages` khi cấp/thu hồi quyền.
- Ứng dụng `xaydungphuluc.html` đã được bổ sung nút liên kết quay về [Trang chủ Portal](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/index.html) và tự động nhận diện danh tính giáo viên (`teacherName`, `userName`, `userEmail`) từ `localStorage`.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\rightarrow$ PASS.
- `node tests/xaydungphuluc-integration-smoke.js` $\rightarrow$ PASS.
- Kiểm tra cú pháp JavaScript cho tất cả các file test và mã nội tuyến `node --check` $\rightarrow$ PASS 100%.

## Pass / Fail từng tiêu chí
1. **Thẻ công cụ trên Portal**: Thẻ xuất hiện trong `#mainToolsGrid` trên `index.html` với `data-tool="xaydungphuluc"`, mở tab mới với `target="_blank"` và `rel="noopener noreferrer"` $\rightarrow$ **PASS**.
2. **Ánh xạ điều hướng**: `TOOL_PAGE_LINKS.xaydungphuluc` trỏ đúng file `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html` $\rightarrow$ **PASS**.
3. **Quản trị toàn cục Admin**: Bật/tắt `cfg_xaydungphuluc` được đồng bộ vào cấu hình tính năng `admin.html` $\rightarrow$ **PASS**.
4. **Phân quyền từng tài khoản**: Cấu hình `PAGE_CONFIG`, `defaultTeacherPages`, các modal Tạo mới, Import Excel và Sửa quyền đều có mục chọn `xaydungphuluc` $\rightarrow$ **PASS**.
5. **Điều hướng ngược và Danh tính**: Nút Trang chủ và hàm `prefillTeacherIdentity` hoạt động chính xác trong `xaydungphuluc.html` $\rightarrow$ **PASS**.
6. **Kiểm thử tự động**: Cả hai bộ smoke test đều PASS $\rightarrow$ **PASS**.

## Bug
- Không có lỗi tồn đọng.
