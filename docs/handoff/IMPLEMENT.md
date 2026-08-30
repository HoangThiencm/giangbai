# IMPLEMENT: Tích hợp Xây dựng Phụ lục vào Portal và phân quyền Admin

## Phạm vi đã triển khai

- Hoàn tất các hạng mục trong `docs/handoff/PLAN.md` cho công cụ `xaydungphuluc`.
- Giữ nguyên `PLAN.md`, `VERIFY.md`, `.lock` (nếu có) và các thay đổi có sẵn ngoài phạm vi.
- Không commit hoặc push.

## File thay đổi

### `index.html`

- Thêm thẻ công cụ `data-tool="xaydungphuluc"` vào `#mainToolsGrid`.
- Liên kết đúng tới `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`, mở tab mới với `noopener noreferrer`.
- Bổ sung `TOOL_PAGE_LINKS.xaydungphuluc`; logic quyền tài khoản và công tắc global hiện có tự áp dụng cho thẻ mới.
- Thêm kiểu thẻ màu, hover/glow và nội dung nhận diện CV 5512, THCS 6–9, NLS & AI.

### `admin.html`

- Thêm công tắc global `cfg_xaydungphuluc` và đăng ký trong `CLIENT_FEATURE_CHECKS`.
- Bổ sung cấu hình trang `xaydungphuluc` (qua `PAGE_CONFIG`/`hostingPages`), tên tính năng và nhóm quyền công cụ giáo viên.
- Thêm quyền này cho `defaultTeacherPages`, nên xuất hiện trong giao diện tạo và chỉnh sửa tài khoản giáo viên.
- Đồng bộ `user_features` khi tạo, sửa hoặc cấp full quyền cho giáo viên bằng luồng đồng bộ sẵn có.

### `GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html`

- Bổ sung nút `Trang chủ` về `../../index.html` ở header.
- Bổ sung nạp sẵn giáo viên từ `teacherName`, `userName` hoặc `userEmail` trong localStorage.

### `tests/xaydungphuluc-integration-smoke.js`

- Thêm smoke test tích hợp Portal/Admin/ứng dụng: thẻ mở tab mới, link map, checkbox global, cấu hình trang, các vùng cấp quyền, liên kết Trang chủ và identity prefill.

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- Kiểm tra cú pháp JavaScript nội tuyến của `xaydungphuluc.html` — PASS.
- `git diff --check` — PASS (chỉ có cảnh báo CRLF trên các tệp đã thay đổi từ trước).

## Vấn đề còn lại

- Chưa kiểm thử thao tác thật trên trình duyệt với phiên đăng nhập Admin/giáo viên; thực hiện bằng `/verify` theo quy trình.
