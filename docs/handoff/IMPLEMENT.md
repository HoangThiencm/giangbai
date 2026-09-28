# IMPLEMENT: Sổ báo giảng trên iPhone và mô tả lịch theo buổi

## Đã làm
- Tab Lịch báo giảng, khi đã chọn một giáo viên, vẽ `#bg-mobile-so` bằng đúng thẻ ngày của email: header `#dbeafe` / `#1e3a8a`, dải Buổi sáng `#fff7ed` / `#9a3412`, Buổi chiều `#eff6ff` / `#1d4ed8`, năm cột Tiết, Lớp (`#1e3a8a`), Môn (badge `#e0f2fe`), Bài dạy, PPCT (`#047857`).
- `phancongtochuyenmon.html` có meta `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, `apple-mobile-web-app-title` = Báo Giảng.
- Email lịch báo giảng có nút **📱 Mở xem Sổ Báo Giảng trên iPhone** (trang `api/calendar_feed.php?format=html&token=...`) và **📅 Đồng bộ vào Lịch iPhone / Google Calendar** (`webcal://`). Trang sổ nhắc Thêm vào Màn hình chính. Trang này đọc TKB đã lưu, 14 ngày tới, không chạy lại bộ ghép PPCT trên trình duyệt nên cột Bài dạy/PPCT hiện “Chưa khai báo PPCT”. Sổ trong tab Lịch báo giảng vẫn ghép PPCT đầy đủ.
- Sự kiện `.ics` và Webcal gom theo buổi. Mô tả dạng `BUỔI SÁNG:` rồi từng dòng `- Tiết N: Môn Lớp | bài (PPCT)`.

## Kiểm thử
- `node tests/timetable-render-smoke.js` — PASS.
- `node tests/baogiang-mail-smoke.js` — PASS.

## Ngoài phạm vi
Không đổi Gemini nhận diện TKB. Chưa thêm icon PNG riêng và chưa bấm “Thêm vào Màn hình chính” trên iPhone; bước đó thuộc `/verify`.
