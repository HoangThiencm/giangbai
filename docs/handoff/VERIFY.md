# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Duyệt Giáo Án AI (`duyetgiaoan.html` & `api/duyetgiaoan.php`)**:
   - Giao diện 4 bước chuyên nghiệp, hỗ trợ bóc tách tài liệu PDF/DOCX/XLSX bằng `pdf.js` và Mammoth.
   - Cơ chế đối chiếu 3 trụ cột: Khung PPCT môn học, Chuẩn YCCĐ CTGDPT 2018 (`js/khbd-yccd.js`, `js/khbd-standards.js`), và tiến trình 4 hoạt động CV 5512.
   - Thẩm định qua Gemini AI với fallback minh bạch khi mất kết nối.
   - Xuất Báo cáo Tổng hợp tổ chuyên môn và Phiếu nhận xét cá nhân định dạng Word (.docx).
   - Backend `api/duyetgiaoan.php` hỗ trợ lưu trữ, tải và quản lý lịch sử các đợt duyệt theo tháng/năm học.
   - Tích hợp hoàn chỉnh trên `index.html`, `admin.html`, `access-control.js`, `api/helpers.php` và `global_config.json`.
2. **Sửa lỗi xuất Word & Đồng bộ Gemini API Key (`matrande.html` & `kttx.html`)**:
   - Gỡ bỏ hoàn toàn thẻ `<script>` khỏi các template Word (`exportWord`, `exportWordRaw`), bảo toàn khối script Babel nguyên vẹn.
   - Triển khai `syncUserKeysFromServer()` tự động nạp Gemini API Keys từ tài khoản CSDL (`api/user_gemini_keys.php`) khi mount, kèm cơ chế fallback an toàn vào `localStorage`.

## Test đã chạy
- `node tests/matrande-smoke.js` $\to$ PASS
- `node tests/kttx-smoke.js` $\to$ PASS
- `node tests/duyetgiaoan-smoke.js` $\to$ PASS
- `node tests/duyetgiaoan-integration-smoke.js` $\to$ PASS
- `node tests/xaydungphuluc-smoke.js` $\to$ PASS

## Pass / Fail từng tiêu chí
- [x] Công cụ `duyetgiaoan.html` và backend `api/duyetgiaoan.php` hoạt động đầy đủ chức năng và tích hợp hệ thống: PASS
- [x] `matrande.html` và `kttx.html` không còn lỗi thẻ script trong template Word, xuất Word sạch đẹp: PASS
- [x] Tự động đồng bộ Gemini API Key từ tài khoản CSDL khi tải trang: PASS
- [x] 100% các bộ kiểm thử smoke của các tính năng mới và tính năng liên quan đều đạt PASS: PASS

## Bug
*(Không có)*
