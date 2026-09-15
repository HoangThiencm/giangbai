# Báo cáo triển khai: AI tích hợp theo cả bài PPCT

## Phạm vi đã thực hiện

- Đồng bộ `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.
- AI chỉ lưu ID bài; dữ liệu cũ dạng `:period:N` được quy đổi an toàn về ID bài.
- Một checkbox `Tích hợp AI` đại diện cho toàn bộ bài; AI luôn tính theo tổng số tiết PPCT, không còn lựa chọn chế độ theo bài.
- Slider, số lượng nhập tay, tự chọn và giới hạn thao tác đều dùng tổng số tiết của bài; không vượt mục tiêu và tự chọn bài nguyên vẹn gần mục tiêu nhất.
- Cấu hình/xuất dữ liệu gửi `selectedLessonIds`, `selectedLessons` và các tiết đầy đủ của từng bài đã chọn. Phạm vi `Áp dụng: tiết` cũ được loại khỏi tích hợp AI.
- Coverage/compliance AI tính theo tổng số tiết của bài có mã AI; PL1/PL3 tiếp tục đồng bộ mã tích hợp.
- Cập nhật smoke test chính và Canvas để kiểm tra hợp đồng UI, migration, giới hạn tiết, config và coverage; test Canvas không còn thoát sớm.

## Kiểm thử

- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-math-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.
- `git diff --check`: PASS.

## Bảo toàn

`docs/handoff/PLAN.md` là thay đổi có sẵn của người dùng và được bảo toàn nguyên trạng; không sửa hoặc ghi đè. Không commit/push.
