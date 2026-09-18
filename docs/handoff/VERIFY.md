# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] `taobaitap.html` & `backupcode viettailieu/taobaitap.html`: Bổ sung nút **🚀 THI TRỰC TUYẾN** cạnh "DẠY NGAY"; hàm `startOnlineExam()` và `mapToThiTrucTuyenPayload` đóng gói chuẩn xác 3 dạng câu CV 7991 (`mc`, `tf` 4 ý, `short_answer`) sang `localStorage`.
- [x] `thitructuyen.html`: Tiếp nhận đề thi 1-Click, điền sẵn thời gian mặc định 15 phút kèm các nút chọn nhanh 15p, 20p, 30p, 45p, chuyển thẳng Bước 2 sẵn sàng tổ chức thi.
- [x] `thitructuyen.html`: Áp dụng tùy chọn thi cuốn chiếu và watermark bảo mật cho cả đề mới và các đề cũ khi giáo viên bấm "Sửa đề".
- [x] `thitructuyen.html`: Chế độ thi cuốn chiếu chống chụp gửi AI (One-by-one mode) hiển thị 1 câu/lúc, có timer riêng từng câu, khóa vĩnh viễn không cho quay lại câu cũ (No Backtrack), lưu tiến trình câu hỏi chống mất dữ liệu khi F5.
- [x] `thitructuyen.html`: Watermark bảo mật in mờ thông tin học sinh (Họ tên, SBD, lớp, ngày giờ) xoay góc -25 độ chống chụp ảnh chia sẻ và gây nhiễu AI Vision OCR.
- [x] `canvas_soankhbd.html`: Bổ sung fallback cứu hộ nạp catalog PPDH từ CDN GitHub jsDelivr khi file trên host bị 0 byte.

## Test đã chạy
- `node tests/taobaitap-thitructuyen-bridge-smoke.js` — PASS
- `node tests/canvas-soankhbd-smoke.js` — PASS
- `node tests/cv7991-taobaitap-thitructuyen-sync-smoke.js` — PASS
- `node tests/taobaitap-plan-smoke.js` — PASS

## Pass / Fail từng tiêu chí
- Nút liên thông 1-Click & đóng gói payload CV 7991: PASS
- Tiếp nhận đề, mặc định 15 phút và preset thời gian: PASS
- Chế độ thi cuốn chiếu (One-by-one & No Backtrack): PASS
- Watermark bảo mật chống chụp màn hình & Anti-OCR: PASS
- Hỗ trợ cập nhật cấu hình cho cả đề cũ: PASS
- Fallback CDN catalog PPDH trên Canvas: PASS
- Toàn bộ test suite kiểm thử: PASS

## Bug
- Lỗi: Không có
- Tái hiện: Không
- File liên quan: Không

