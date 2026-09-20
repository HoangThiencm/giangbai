# IMPLEMENT: Khắc phục khởi động và AI vẽ hình

## Phạm vi đã thực hiện

- `app.js`: Đưa khởi tạo vào `bootVehinhApp()` có cờ chống khởi động lặp, chạy ngay khi DOM đã sẵn sàng hoặc chờ `DOMContentLoaded` khi cần. `createPatterns()` nay chịu được Fabric.js chưa tải; formatter GeoGebra cũng chạy an toàn trong sandbox cô lập.
- `vehinh.html`: Thêm CDN dự phòng cho Fabric.js và danh sách model/tóm tắt AI mặc định để giao diện không còn kẹt ở placeholder khi mạng hoặc API chậm.
- `api/vehinh_ai.php`: GET cấu hình model không yêu cầu phiên đăng nhập; POST chấp nhận API key hợp lệ từ client khi chưa đăng nhập.
- `tests/game-quiz-importer-smoke.js`: Nạp helper GeoGebra còn thiếu và cập nhật kỳ vọng ẩn trục/lưới cho hình không dùng tọa độ.
- `tests/vehinh-boot-smoke.js`: Thêm smoke test cho lifecycle, Fabric fallback, model HTML tĩnh và thứ tự xác thực endpoint.

## Kiểm thử

- PASS: `node --check app.js`
- PASS: `node tests/vehinh-boot-smoke.js`
- PASS: `node tests/game-quiz-importer-smoke.js`
- Không chạy được PHP lint vì môi trường hiện tại không có executable `php` trong PATH hoặc các vị trí cài đặt thông dụng.
