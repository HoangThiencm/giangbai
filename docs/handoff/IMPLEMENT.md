# IMPLEMENT

## Đã triển khai

- Mã hóa tài khoản trước khi gửi `X-User-Account`, giải mã an toàn ở API, và không còn dùng tên giáo viên có dấu/khoảng trắng làm tài khoản nháp.
- Thay chọn NLS bằng knapsack 0/1 tối ưu điểm sư phạm, ưu tiên tổng số tiết đúng bằng số nhập; ô số tiết NLS/AI đồng bộ ngay khi nhập.
- Phụ lục 3 không gọi AI để tái tạo PPCT; bảng kế thừa đầy đủ lịch Phụ lục 1, gồm dòng tiêu đề, Tiết CT, Tuần, thiết bị, địa điểm và Ghi chú tích hợp.
- Đồng bộ thay đổi giao diện sang `canvas_xaydungphuluc.html`, `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.

## Kiểm thử

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-smoke.js` — PASS.
- Không chạy được kiểm tra cú pháp PHP vì môi trường hiện tại không có lệnh `php`.

## Vấn đề còn lại

Không có vấn đề chức năng đã biết. Cần thực hiện `/verify` theo quy trình trước khi commit/push.
