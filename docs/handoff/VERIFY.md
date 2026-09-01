# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Triệt tiêu hoàn toàn lỗi lệch pha YCCĐ giữa các bài học ("râu ông nọ cắm cằm bà kia").
- [x] Xóa bỏ triệt để lệnh fallback theo chỉ số dòng `generatedRows[normal]` trong `appendixOneTable`.
- [x] Triển khai thành công Chiến lược dự phòng 4 tầng: CSDL CTGDPT 2018 (`KHBD_YCCD`) $\to$ Ngữ cảnh SGK $\to$ AI có kiểm chứng từ khóa $\to$ Khung YCCĐ Sư phạm chuẩn hóa theo thể loại bài.
- [x] Xử lý ngữ cảnh chủ đề cho các bài Luyện tập, Luyện tập chung, Ôn tập chương và bài học lạ.
- [x] Cho phép giáo viên chỉnh sửa trực tiếp (Inline Edit) ô Yêu cầu cần đạt trong bảng xem trước Phụ lục 1 trước khi xuất Word.
- [x] Chuẩn hóa độ rộng cột khi xuất Word (.docx) theo nội dung thực tế (Phụ lục 1: `[5, 22, 6, 47, 20]`, Phụ lục 3: `[22, 6, 8, 6, 18, 16, 24]`).
- [x] Thiết lập `cantSplit: true` trên từng hàng và `tableHeader: true` trên hàng tiêu đề trên nền khổ giấy A4 Landscape chuẩn.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS

## Pass / Fail từng tiêu chí
- [x] PASS: Bài 5 (Phép nhân và phép chia) nhận đúng YCCĐ phép nhân, chia, luỹ thừa; không dính YCCĐ tập hợp/La Mã.
- [x] PASS: Luyện tập chung nhận đúng YCCĐ củng cố chủ đề đứng trước.
- [x] PASS: Bài học không có trong CSDL nhận đúng khung sư phạm tương ứng (`generatePedagogicalOutcome`).
- [x] PASS: Sửa trực tiếp ô YCCĐ đồng bộ vào model và lưu cho xuất Word.
- [x] PASS: Tỉ lệ cột DOCX và thuộc tính `cantSplit`, `tableHeader`, A4 Landscape được cấu hình chuẩn xác.

## Bug
- Không có.
