# IMPLEMENT: Mặc định rỗng khi tạo đợt phân công TKB & Chuẩn hoá Lịch báo giảng

Trạng thái: ĐÃ THỰC HIỆN

## File đã thay đổi

- `phancongtochuyenmon.html`
  - Đợt phân công mới mặc định không kế thừa; snapshot mới xoá phân công và TKB giáo viên, đồng thời giữ riêng nhiệm vụ trường học.
  - Đợt chưa có snapshot cũng khởi tạo rỗng thay vì sao chép đợt hiện hành.
  - Bổ sung nhãn thứ tiếng Việt trong email văn bản, thẻ email và bảng lịch web.
  - Gom các dòng PPCT liền kề cùng mạch/bài và tính phân đoạn luỹ kế xuyên tuần.
- `tests/baogiang-weekday-segment-smoke.js`
  - Kiểm tra phân đoạn `1/3`, `2/3`, `3/3`, thứ tiếng Việt và cấu hình đợt mới rỗng.

## Kiểm thử

- `node tests/baogiang-recognition-smoke.js` — PASS
- `node tests/baogiang-weekday-segment-smoke.js` — PASS
