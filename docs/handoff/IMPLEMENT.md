# IMPLEMENT

## Đã triển khai

- Mã hóa tài khoản trước khi gửi `X-User-Account`, giải mã an toàn ở API, và không còn dùng tên giáo viên có dấu/khoảng trắng làm tài khoản nháp.
- Chọn NLS giữ đúng số tiết đã nhập (ví dụ 28), sử dụng mã dòng PPCT thay vì so khớp tên bài để không chọn trùng các bài có cùng tên ở các học kỳ; ô số tiết NLS/AI đồng bộ ngay khi nhập.
- Phụ lục 3 ưu tiên tuyệt đối bảng PPCT nguồn, tiếp đó PPCT chuẩn và chỉ cuối cùng mới dùng lịch Phụ lục 1; vì vậy giữ dòng tiêu đề, Tiết CT, Tuần, thiết bị, địa điểm và Ghi chú tích hợp thay vì dùng lịch AI đã rút gọn.
- Đồng bộ thay đổi giao diện sang `canvas_xaydungphuluc.html`, `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.

## Kiểm thử

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-smoke.js` — PASS.
- Smoke test trên còn kiểm tra riêng tổ hợp NLS đúng 28 tiết, chọn theo mã dòng PPCT, và PL3 giữ tiêu đề/Tiết CT/Tuần khi PL1 bị AI rút gọn.
- Không chạy được kiểm tra cú pháp PHP vì môi trường hiện tại không có lệnh `php`.

## Vấn đề còn lại

Không có vấn đề chức năng đã biết. Cần thực hiện `/verify` theo quy trình trước khi commit/push.
