# TASK

## Mô tả yêu cầu
Khắc phục lỗi khi chụp dán ảnh nhận diện văn bản (số, ngày tháng, vùng chữ ký) trong Quản lý văn bản (`quanlyvanban-*.html` / `vanban-app.js`):
1. **Hiện trạng lỗi**: Khi người dùng chụp màn hình tiêu đề/số/ngày hoặc vùng chữ ký của văn bản rồi dán (Ctrl+V) vào ô nhập liệu, hệ thống báo lỗi đỏ: `Ảnh vùng chữ ký cần Mistral OCR. Hãy dán chữ hoặc dùng PDF có chữ ký số.` do hệ thống chưa có API Key Mistral OCR.
2. **Vấn đề giao diện**: Trang Quản lý văn bản có nạp `ai-design-config.js` nhưng không có nút bấm "Cấu hình AI" để người dùng mở bảng nạp key (Mistral / Gemini), và chưa tự động gọi `loadHostingFallbackConfig()` để đồng bộ key.
3. **Mở rộng nhận diện**: Cho phép fallback qua Gemini Vision nếu người dùng đã có Gemini API Key (loại key phổ biến nhất trong hệ thống), đồng thời hướng dẫn trực tiếp mở bảng Cấu hình AI khi chưa có key nào.

## File hoặc phạm vi liên quan
- `vanban-app.js`
- `quanlyvanban-chuyenmon.html`
- `quanlyvanban-hanhchinh.html`
- `quanlyvanban-dang.html`
- `tests/vanban-ocr-clipboard-smoke.js`

## Yêu cầu đặc biệt / Giới hạn
- Không làm vỡ các luồng nhận diện cũ: PDF có lớp chữ (`text-layer`), chữ ký số nhị phân (`/Type /Sig`), hay Mistral OCR khi đã có key.
- Đảm bảo tuân thủ rule AGENTS.md: IDE đóng vai trò Planner/Tester, Coder thực hiện đúng `docs/handoff/PLAN.md`.
