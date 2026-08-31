# IMPLEMENT: PPCT/SGK riêng biệt và chọn tối đa 12 tiết AI

## Đã triển khai

- Tách khu vực nạp dữ liệu thành ô PPCT (DOCX/XLSX/PDF) và ô SGK (PDF/DOCX), với luồng xử lý độc lập.
- Bổ sung nút nạp PPCT mẫu theo Môn & Lớp; danh sách bài học mẫu được nạp ngay khi mở trang và khi thay đổi Môn/Lớp.
- Bảng chọn tiết AI luôn hiển thị, có checkbox từng bài, bộ đếm `X/12`, gợi ý 12 tiết ưu tiên Hình học/Thống kê/Trải nghiệm, và nút bỏ chọn tất cả.
- Luồng SGK chỉ giữ tên bài, mục tiêu và hoạt động; ngữ cảnh tinh gọn này được đưa vào prompt Gemini. Mã `[AI: ...]` chỉ được giữ hoặc bổ sung tại các bài được tick.
- Giữ liên thông Phụ lục 3 sang Phụ lục 1: PL3 bảo toàn bảng PPCT nguồn, còn PL1 tự sinh Yêu cầu cần đạt theo GDPT 2018.
- Preview và DOCX tách màu mã NLS xanh `0070C0` và mã NLAI tím `7030A0`.

## File thay đổi

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/.lock` (nội dung `LOCK`)
- `docs/handoff/IMPLEMENT.md`

Không sửa `docs/handoff/PLAN.md` hoặc `docs/handoff/VERIFY.md`.

## Kiểm thử

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `git diff --check` — PASS.
