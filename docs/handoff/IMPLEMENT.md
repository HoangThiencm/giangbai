# IMPLEMENT: Khử trùng mã NLS và AI từ PPCT

Đã triển khai đúng `docs/handoff/PLAN.md`.

- Cập nhật duy nhất hàm `ppctRowCodes` trong `js/khbd-app.js`.
- Chuẩn hóa mã bằng `String(...).trim()` và dùng `Set` để chỉ giữ một lần mỗi mã khi dữ liệu đồng thời có trong `nls`/`digital_competency` hoặc `ai`/`ai_competency`.
- Thêm `tests/ppct-dedupe-smoke.js` để kiểm tra mã NLS `1.2.TC1a` và AI `6.A1.1` không còn lặp.
- Đã tạo lại `docs/handoff/.lock` với nội dung `LOCK` sau khi sửa mã nguồn.

Kiểm thử Node chưa thể chạy trong môi trường hiện tại vì Windows chặn tiến trình `node.exe` là tệp có khả năng không mong muốn. Cần chạy `/verify` trên Antigravity IDE để xác nhận PASS toàn bộ suite.
