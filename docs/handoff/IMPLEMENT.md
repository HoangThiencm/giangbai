# IMPLEMENT: Nhận diện số tiết PPCT đầy đủ

## Đã triển khai

- Thêm nhận diện số tiết từ số thường, cách ghi `tiết`, ngoặc, `/tuần`, khoảng tiết và số đếm tiếng Việt cơ bản.
- Khi cột Số tiết trống, mô hình PPCT, bảng chọn AI và PL1 suy ra số tiết từ Tiết CT; bảng PPCT thô vẫn được bảo toàn.
- Danh sách chọn AI dùng số tiết đã suy ra, nên số checkbox và tỷ lệ phản ánh đúng tổng tiết.
- PPCT mẫu vẫn có 35 bài/hai học kỳ nhưng phân bổ chính xác tổng số tiết năm học theo môn, với Tiết CT liên tiếp.

## File thay đổi

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`

`docs/handoff/.lock` được giữ với nội dung `LOCK`. Không sửa `docs/handoff/PLAN.md` hoặc `docs/handoff/VERIFY.md`.

## Kiểm thử

- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-integration-smoke.js` — PASS.
- `git diff --check` — PASS.
