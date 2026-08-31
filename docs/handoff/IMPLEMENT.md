# IMPLEMENT: Bảo toàn bảng PPCT nguồn và chuẩn hóa Phụ lục 1 theo CV 5512

## Phạm vi đã triển khai

- `xaydungphuluc.html` lưu bảng PPCT nguồn theo mô hình động (nguyên tên cột, thứ tự cột, ô dữ liệu và dòng phân cấp), thay vì ép về bảy cột cố định.
- Khi có PPCT nguồn, ứng dụng chỉ nối một cột cuối: `Mã NLS & AI (CV 3456 & QĐ 2422)`. Gemini chỉ được dùng để điền nội dung cột này; dữ liệu nguồn không bị thay thế.
- Preview Phụ lục 1 hiển thị đủ khung hành chính: tiêu ngữ, căn cứ CV 5512, mục I (đặc điểm, thiết bị, phòng học), mục II (PPCT, chuyên đề, KTĐG), mục III và bảng ký hai bên.
- Xuất Word Phụ lục 1 dùng cùng cấu trúc hành chính, bảng PPCT động và cột NLS/AI bổ sung. Phụ lục 2, 3 vẫn xuất Word được, trong đó Phụ lục 3 dùng bảng PPCT động nếu có nguồn.
- Cập nhật smoke test bằng tình huống PPCT sáu cột bất kỳ, có cột `Yêu cầu cần đạt`; test xác nhận nguyên cột/dữ liệu được giữ và chỉ có đúng một cột mới được thêm.

## File thay đổi

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`

Không sửa `docs/handoff/PLAN.md`, `docs/handoff/VERIFY.md` hoặc `docs/handoff/.lock`; không commit/push.

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `node --check` cho JavaScript nội tuyến — PASS.
- `git diff --check` — PASS.

## Cần nghiệm thu thủ công

Mở `xaydungphuluc.html`, tải file mẫu `GIAO AN/XAYDUNGPHULUC/Phụ lục 1 - Lớp 6 - Toán.docx`, sinh Phụ lục 1 và mở file Word xuất ra để đối chiếu trực quan font/căn lề với mẫu Office.
