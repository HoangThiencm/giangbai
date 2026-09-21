# IMPLEMENT: Nâng Cấp Game Đua Vịt Hài Hước Đỉnh Cao & Sửa Lỗi Toán/Kẹt Câu

Đã triển khai đúng `docs/handoff/PLAN.md` trong phạm vi `game-treasure.html` và `game-escape.html`.

## Thay đổi

### Game Đua Vịt (`game-treasure.html`)

- Bổ sung KaTeX cục bộ và Canvas Confetti; `MathText` chuẩn hóa công thức có `$...$`, `\\(...\\)`, `\\[...\\]` và backtick để render prompt/lựa chọn trong modal câu hỏi.
- Thay động cơ Canvas bằng đàn vịt bơi tự do với vị trí dọc ngẫu nhiên, gia tốc, bọt nước, va chạm đàn hồi và âm thanh Boing.
- Thêm phụ kiện ngẫu nhiên (kính, mũ cử nhân, phao, tên lửa, nơ), bảng tên học sinh nổi bật và âm thanh đếm ngược, quack, va chạm, chiến thắng.
- Thêm sự kiện bánh mì, xoáy nước, cụ rùa cứu trợ và Nitro; thanh bình luận viên trực tiếp mô tả diễn biến.
- Thêm slow-motion ở đoạn cuối cùng và thông báo Photo Finish trước khi pháo hoa/fanfare khi có vịt thắng.

### Hứng Trứng Vàng (`game-escape.html`)

- Dùng hai ref timer độc lập: `fallTimerRef` và `nextTimerRef`.
- Cleanup hiệu ứng rơi chỉ hủy timer rơi; timer chuyển câu được giữ để không kẹt ở câu đầu.
- `handleCatch` lên lịch qua `nextTimerRef`; `goNext` dùng updater của `setQIndex` để tránh stale closure.

## Kiểm tra

- Babel JSX: `game-treasure.html` PASS; `game-escape.html` PASS.
- Static check: xác nhận KaTeX, confetti, các sự kiện đua, commentary/Photo Finish, hai timer ref và `setQIndex(prevIndex => ...)` đều có mặt.
- `git diff --check`: PASS (chỉ có cảnh báo line-ending của Git, không có lỗi whitespace).
- Chưa kiểm thử tương tác trực tiếp trong trình duyệt. Bước tiếp theo: chạy `/verify` theo quy trình dự án.
