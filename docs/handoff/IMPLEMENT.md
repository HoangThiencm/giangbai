# IMPLEMENT: Khắc phục phân đoạn PPCT cho bài lặp định kỳ

Đã triển khai đúng `docs/handoff/PLAN.md`.

## File đã thay đổi

- `phancongtochuyenmon.html`
  - Chuẩn hóa `periods` về 1 khi `period_no` chỉ là một tiết đơn lẻ.
  - Phân biệt block PPCT theo mạch kiến thức (`strand`).
  - Không gộp các bài lặp định kỳ như “Luyện tập chung”, “Ôn tập”, “Kiểm tra” giữa các tuần, trừ khi dòng tiếp theo có chỉ dẫn tiếp diễn rõ ràng.
  - Chuẩn hóa dòng PPCT do AI trả về và bổ sung chỉ dẫn prompt để số tiết khớp với tiết PPCT.
- `tests/baogiang-weekday-segment-smoke.js`
  - Bổ sung kiểm thử lỗi “Luyện tập chung” 1 tiết ở các tuần khác nhau, trường hợp có “(tiếp theo)”, khác mạch cùng tuần, và dữ liệu `period_no` đơn lẻ nhưng `periods` sai.

## Kiểm tra

- `node tests/baogiang-weekday-segment-smoke.js`: PASS.
- `node tests/baogiang-recognition-smoke.js`: PASS.
- `node tests/baogiang-teacher-month-smoke.js`: PASS.
- `git diff --check -- phancongtochuyenmon.html tests/baogiang-weekday-segment-smoke.js docs/handoff/IMPLEMENT.md`: PASS.

## Giới hạn

Chưa thực hiện kiểm tra trực quan trên trình duyệt; các đường đi và tình huống hồi quy trong kế hoạch đã được kiểm tra tự động.
