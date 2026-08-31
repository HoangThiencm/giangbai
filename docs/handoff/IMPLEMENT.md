# IMPLEMENT: Nạp và chọn tiết PPCT cho Phụ lục 1/3

## Đã triển khai

- Nạp PPCT DOCX/XLSX/PDF, bảo toàn bảng nguồn và hiển thị từng bài với Bài học, Số tiết (có thể sửa), Tiết CT, Tuần, Thiết bị, Địa điểm cùng checkbox từng tiết AI.
- Giới hạn, gợi ý và bỏ chọn AI hoạt động theo tối đa 12 tiết; khi giảm số tiết, checkbox thừa tự bị loại và PL1/PL3 được làm mới.
- Nhận diện số tiết từ số thường, ngoặc, `/tuần`, khoảng, danh sách `1, 2` và số đếm tiếng Việt; khi Số tiết trống, suy ra từ Tiết CT.
- PL1 lấy Bài học/Số tiết từ PPCT và sinh Yêu cầu cần đạt; PL3 giữ nguyên bảng nguồn và chỉ nối một cột Mã NLS & AI. Preview/DOCX tách NLS xanh `0070C0`, AI tím `7030A0`.

## File thay đổi

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`

Không sửa `docs/handoff/PLAN.md`, `docs/handoff/VERIFY.md` hoặc `docs/handoff/.lock` trong lần triển khai này.

## Kiểm thử

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `git diff --check` — PASS.
