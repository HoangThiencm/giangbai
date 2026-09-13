# IMPLEMENT

## Đã triển khai
- Gộp cột NLS và AI của Phụ lục 1 thành cột `Ghi chú` (5 cột) và của Phụ lục 3 thành `Ghi chú` (7 cột) trên cả ba bản HTML.
- Thêm định dạng nội dung Ghi chú: một mã nằm cùng dòng với nhãn; nhiều mã dùng các dòng `+`; giữ nguyên mô tả và phạm vi tiết AI.
- Bảo toàn đồng bộ PL1 → PL3 bằng cách chuyển nội dung Ghi chú trở lại dữ liệu tích hợp khi cần.
- Cập nhật chỉnh sửa trực tiếp cột Ghi chú và cấu hình độ rộng DOCX: PL1 `5,22,6,37,30`; PL3 `20,5,6,5,15,14,35`.
- Cập nhật các smoke test liên quan đến số cột, nhãn Ghi chú và độ rộng DOCX.

## Kiểm thử
- PASS: `node tests/xaydungphuluc-smoke.js`
- PASS: `node tests/canvas-xaydungphuluc-smoke.js`
- PASS: `node tests/xaydungphuluc-math-smoke.js`
- PASS: `node tests/xaydungphuluc-integration-smoke.js`

Các assert smoke về thẩm định đã được điều chỉnh để kiểm tra đúng cột Ghi chú, bao gồm trường hợp tắt NLS. Không còn lỗi kiểm thử đã biết.

## Không thực hiện
- Không commit hoặc push.
