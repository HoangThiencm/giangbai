# IMPLEMENT: Trang Quản lý văn bản không hiện dữ liệu

## Đã làm
- `api/vanban.php`: `vbd_current_user` cho phép `teacher`, `admin`, `superadmin`. Tài khoản chưa đăng nhập hoặc không hoạt động vẫn bị từ chối. Thông báo 403: «Chức năng quản lý văn bản chỉ dành cho giáo viên hoặc quản trị viên.»
- `quanlyvanban.html` tải `vanban-hub.js?v=20260928-hub-fix`.
- `quanlyvanban-hanhchinh.html` và `quanlyvanban-dang.html` tải `vanban-app.js?v=20260928-app-fix`.
- `vanban-hub.js`: `boot()` vẫn gọi `renderSummary()` rồi `renderSectors()` trước `load()`. Cuối file có `/* deploy-touch: 20260928-hub-fix */`. File local 9702 bytes.
- `vanban-app.js`: khi đang tải và chưa có dữ liệu, `#documentList` hiện dòng chờ. `fetch` lỗi mạng thành câu «Mất kết nối mạng. Không tải được danh sách văn bản, tệp đính kèm và nội dung báo cáo.» (toast và khung đỏ trong danh sách). Bấm trích yếu vẫn mở tóm tắt, hạn/ghi chú báo cáo và tệp đính kèm. Cuối file có `/* deploy-touch: 20260928-app-fix */`. File local 83500 bytes.

## Kiểm thử
- `node --check vanban-hub.js` và `node --check vanban-app.js`: PASS.
- Script Node tạm: `fetch` từ chối thì danh sách hiện câu mất kết nối. `fetch` trả một văn bản mẫu thì bảng có «Công văn kiểm tra»; mở chi tiết có «Nộp báo cáo trước hạn», «Đã nộp bản giấy» và `congvan.pdf`. PASS.
- Máy này không có `php` trên PATH. Không có trình duyệt, chưa mở ba trang trên `hoangthiencm.id.vn`.

## Chưa đẩy hosting
Chưa commit và chưa push. `docs/handoff/VERIFY.md` đang PASS của kế hoạch Gemini cũ, chưa nghiệm thu module văn bản. File 0 byte trên hosting chỉ được FTP Deploy thay sau khi push lên `main`.

## Ngoài phạm vi
Không đổi bảng MySQL và không đụng tệp Google Drive.
