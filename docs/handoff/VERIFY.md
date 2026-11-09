# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `api/short_links.php`: Đã bổ sung trường `escape_inapp TINYINT(1) NOT NULL DEFAULT 1` vào schema và cơ chế tự động migration qua `SHOW COLUMNS`. Hỗ trợ đầy đủ tham số `escape_inapp` trong các action `list`, `create`, `update`.
- `s.php`: Nhận diện chính xác User-Agent In-App Browser (Zalo, FB, Instagram...), hỗ trợ Android Intent tự động mở Chrome ngoài trên Android và màn hình đệm chỉ dẫn trực quan (mũi tên hướng dấu `...`, nút chép link, nút mở Chrome) trên iOS. Giữ nguyên HTTP 302 cho trình duyệt chuẩn hoặc link tắt Smart Bridge.
- `rutgon.html`: Đã thêm checkbox "Tự động thoát Zalo / In-App Browser" trong modal tạo/sửa link; hiển thị huy hiệu "Thoát Zalo" trong danh sách; hiển thị ghi chú bảo vệ và nút xem thử màn hình Zalo trong modal QR Code.

## Test đã chạy
1. Kiểm tra cú pháp JavaScript trong `rutgon.html` qua Node.js: Toàn bộ script inline parse thành công, không có lỗi cú pháp.
2. Kiểm tra cấu trúc SQL và migration trong `s.php` và `api/short_links.php`: Các lệnh ALTER TABLE và schema definition đồng bộ, hợp lệ.
3. Kiểm thử kịch bản chuyển hướng (Simulation Test):
   - Desktop Chrome UA $\rightarrow$ HTTP 302 trực tiếp đến target URL.
   - iOS Safari chuẩn UA $\rightarrow$ HTTP 302 trực tiếp đến target URL.
   - Zalo Android UA + `escape_inapp=1` $\rightarrow$ Android Intent Bridge (Chrome package + generic browser fallback).
   - Zalo iOS UA + `escape_inapp=1` $\rightarrow$ iOS Bridge UI (hướng dẫn bấm `...`, nút chép clipboard, `googlechromes://`).
   - Zalo UA + `escape_inapp=0` $\rightarrow$ HTTP 302 trực tiếp (tôn trọng cấu hình người dùng).

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Trình duyệt chuẩn (Desktop/Mobile Safari/Chrome) không bị ảnh hưởng, chuyển hướng 302 ngay lập tức. (PASS)
- [x] Tiêu chí 2: Zalo Android tự động gọi Android Intent mở Chrome ngoài. (PASS)
- [x] Tiêu chí 3: Zalo iOS hiển thị màn hình đệm chỉ dẫn bấm dấu `...`, có nút chép link và nút mở Chrome. (PASS)
- [x] Tiêu chí 4: Giao diện `rutgon.html` cho phép bật/tắt tính năng, hiển thị nhãn và hỗ trợ xem thử mã QR. (PASS)
- [x] Tiêu chí 5: CSDL tự động tương thích ngược cho dữ liệu cũ qua migration an toàn. (PASS)

## Bug
Không phát hiện bug.
