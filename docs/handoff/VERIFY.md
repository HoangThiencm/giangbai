# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] PHẦN 1 (Sửa Ô chữ kỳ diệu `game-crossword.html` & `trochoi.compiled.js`):
  - [x] Giới hạn tối đa 10 hàng ngang, loại bỏ đáp án quá dài (>14 ký tự) tránh vỡ khung hình.
  - [x] Thuật toán căn cột từ khóa dọc thông minh, chuẩn hóa chữ cái không dấu.
  - [x] Modal câu hỏi render KaTeX `<MathText>`, hiển thị số chữ cái, nút gợi ý 1 chữ cái và hiện từ khóa.
- [x] PHẦN 2 (Game Đua xe tùy chỉnh số tổ `game-racing.html`):
  - [x] Màn hình chọn số tổ tham gia linh hoạt từ 2 đến 6 tổ.
  - [x] Cho phép người tổ chức tự đặt tên từng tổ.
  - [x] Làn đua, xe F1, bảng chọn tổ, xếp hạng và bục trao giải Podium thích ứng động theo số tổ đã chọn.
- [x] PHẦN 3 (Thiết kế Game mới "Rung Chuông Vàng" `game-bell.html`):
  - [x] Tạo mới `game-bell.html` với sàn đấu thí sinh (từ CSDL hoặc SBD 01–40).
  - [x] Câu hỏi render KaTeX, đồng hồ đếm ngược 15/20/30s có âm thanh chuông "Boong!".
  - [x] Cơ chế loại trực tiếp thí sinh trả lời sai và quyền "Thầy cô cứu trợ" (50% hoặc tất cả).
  - [x] Hiệu ứng Rung Chuông Vàng vinh danh Quán Quân kèm pháo hoa confetti rực rỡ.
  - [x] Đăng ký game `bell` trong `trochoi.compiled.js` và route bảo vệ trong `access-control.js`.
- [x] PHẦN 4 (Xóa "Quay lại SmartQuiz" trong `trochoi.compiled.js`):
  - [x] Đã xóa hoàn toàn liên kết và dấu ngăn cách, chỉ giữ nút "Về trang chủ".
- [x] PHẦN 5 (Tự động hóa kiểm thử):
  - [x] Tạo mới `tests/game-suite-smoke.js` và chạy pass toàn bộ 5 nhóm kiểm tra.

## Test đã chạy
- `node tests/game-suite-smoke.js`: PASS.
- `node tests/change-password-smoke.js`: PASS.
- `node tests/user-ai-settings-smoke.js`: PASS.
- `node tests/canvas-tabs-permissions-smoke.js`: PASS.
- `git diff --check`: PASS.

## Pass / Fail từng tiêu chí
- Tiêu chí 1 (Sửa lỗi Ô chữ kỳ diệu): PASS
- Tiêu chí 2 (Tùy chỉnh số tổ Game Đua xe 2-6 tổ): PASS
- Tiêu chí 3 (Trò chơi mới Rung Chuông Vàng): PASS
- Tiêu chí 4 (Xóa nút "Quay lại SmartQuiz"): PASS
- Tiêu chí 5 (Kiểm thử hồi quy toàn bộ hệ thống): PASS

## Bug
Không có bug nào được phát hiện.
