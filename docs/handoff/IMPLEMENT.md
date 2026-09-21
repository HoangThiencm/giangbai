# IMPLEMENT: Nâng Cấp Bộ Game Giáo Dục

Đã triển khai đúng `docs/handoff/PLAN.md` trong phạm vi đã duyệt.

## Bổ sung: Phản hồi đáp án tức thì

- Cập nhật `game-racing.html`: lưu lựa chọn A/B/C/D của từng tổ bằng `teamAnswers`; bảng ghi nhận cho phép chọn trực tiếp theo tổ, thẻ đáp án hiển thị ngay các huy hiệu tổ đã chọn, và `confirmBoost` tự chấm đáp án để chỉ các tổ đúng nhận Nitro.
- Cập nhật `game-bell.html`: các đáp án là nút chọn có state `selectedChoice`, hiệu ứng vàng cùng nhãn **ĐÃ CHỌN**, âm thanh xác nhận, phản hồi xanh/đỏ khi công bố đáp án và banner kết quả đúng/sai. Lựa chọn được xóa khi bắt đầu câu mới hoặc đếm giờ lại.
- Cập nhật `tests/game-suite-smoke.js`: kiểm tra sự hiện diện của cơ chế chọn và phản hồi tức thì ở cả hai game.

### Kiểm tra bổ sung

- `node tests/game-suite-smoke.js`: PASS.
- `node tests/change-password-smoke.js`: PASS.
- `node tests/canvas-tabs-permissions-smoke.js`: PASS.
- `git diff --check -- game-racing.html game-bell.html tests/game-suite-smoke.js docs/handoff/IMPLEMENT.md`: PASS.

### Giới hạn

- `git diff --check` trên toàn bộ working tree còn báo whitespace sẵn có ở `docs/handoff/PLAN.md`; file kế hoạch này không được sửa theo phạm vi được duyệt.
- Chưa kiểm thử thủ công trong trình duyệt.

## Thay đổi

- Cập nhật `game-crossword.html`: giới hạn 10 hàng ngang với đáp án 2–14 ký tự, chuẩn hóa bỏ dấu/ký tự dư thừa, căn cột từ khóa theo ký tự thực tế, hiển thị MathText, số chữ cái, gợi ý một chữ cái, hiện từ khóa và ô responsive.
- Cập nhật `trochoi.compiled.js`: làm sạch dữ liệu tạo ô chữ, giới hạn đáp án/hàng; đăng ký `bell` (Rung Chuông Vàng), đổi mô tả Đua Xe thành 2–6 tổ và xóa toàn bộ liên kết “Quay lại SmartQuiz”.
- Cập nhật `game-racing.html`: màn hình chuẩn bị cho phép chọn 2–6 tổ và tự đặt tên; đường đua, chọn tổ, phím tắt, xếp hạng và bục vinh danh sử dụng danh sách tổ động.
- Thêm `game-bell.html`: đấu trường Rung Chuông Vàng với thí sinh từ `gameData` hoặc SBD 01–40, MathText/KaTeX, đồng hồ 15/20/30 giây, loại trực tiếp, cứu 50%/tất cả, chuông Web Audio và confetti vinh danh.
- Thêm bảo vệ route `game-bell.html` trong `access-control.js`.
- Thêm `tests/game-suite-smoke.js`.

## Thay đổi trước đó trong kế hoạch khác

- Thêm `api/change_password.php`: chỉ nhận POST, yêu cầu session `user_id`, xác thực mật khẩu hiện tại bằng `password_verify`, kiểm tra mật khẩu mới và cập nhật hash mới bằng `password_hash`.
- Thêm `js/change-password.js`: modal tự tạo DOM, đóng bằng nút/overlay/Escape, ẩn-hiện mật khẩu, kiểm tra dữ liệu phía trình duyệt và gọi endpoint với cookie phiên.
- Cập nhật `index.html`: thêm nút **Đổi mật khẩu** trước Đăng xuất và nạp module mới. `setupStudentPortal` chỉ tiếp tục ẩn nút cài đặt AI; không ẩn chức năng đổi mật khẩu với học sinh. Đổi SmartQuiz thành **Game giáo dục** ở `TOOL_PAGE_LINKS`, thẻ công cụ giáo viên và hoạt động học sinh; cả ba liên kết đến `https://www.hoangthiencm.id.vn/trochoi.html`.
- Cập nhật `tests/change-password-smoke.js` để kiểm tra cấu trúc giao diện, module, endpoint và các liên kết/nhãn Game giáo dục.

## Kiểm tra

- `node tests/change-password-smoke.js`: PASS.
- `node tests/user-ai-settings-smoke.js`: PASS.
- `node tests/canvas-tabs-permissions-smoke.js`: PASS.
- `git diff --check`: PASS; Git chỉ cảnh báo quy đổi LF/CRLF.
- `php -l api/change_password.php`: không chạy được vì môi trường hiện tại không có lệnh `php` trong PATH.

## Vấn đề còn lại

- Chưa kiểm thử thủ công qua trình duyệt hoặc với cơ sở dữ liệu thật; cần chạy bước `/verify` theo quy trình dự án.
