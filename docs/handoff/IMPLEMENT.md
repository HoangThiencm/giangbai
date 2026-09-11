# IMPLEMENT

Trạng thái: HOÀN THÀNH

## File đã đổi

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`

## Nội dung chính

- Thêm hai chế độ phân bổ cho cả NLS và AI: theo số tiết dạy bài mới hoặc theo số bài dạy bài mới; slider và ô nhập số lượng đồng bộ hai chiều.
- NLS theo tiết chọn tập bài có tổng số tiết gần nhất với mục tiêu; AI theo tiết chọn đúng số tiết ưu tiên, còn theo bài chọn toàn bộ tiết thuộc số bài mục tiêu.
- Bỏ toàn bộ trần 12 tiết AI, bao gồm chọn tay, gợi ý, thông báo, báo cáo thẩm định và kiểm tra tuân thủ; 100% tương ứng với toàn bộ tiết dạy bài mới.
- Lưu và tải bản nháp nay giữ cả `nls.unit` và `ai.unit`.
- Giữ bảng PPCT hiệu quả: một lượt dựng bảng chỉ tính danh sách tiết AI một lần.
- Mở rộng smoke test cho hai đơn vị, nhập số lượng, nhãn, lưu/tải unit và phân bổ AI vượt 12 tiết.

## Test đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `git diff --check` — PASS

## Vấn đề còn lại

Không có.

## Khắc phục VERIFY FAIL (Canvas)

- Đồng bộ điều khiển phân bổ theo số tiết / số bài, ô nhập số lượng, nhãn “tiết dạy bài mới” và “bài dạy bài mới” sang `canvas_xaydungphuluc.html`.
- Canvas không còn giới hạn AI ở 12 tiết, kể cả thao tác chọn thủ công; bản nháp lưu và phục hồi `nls.unit` / `ai.unit`.
- Sửa smoke test NLS để trích xuất đầy đủ helper phân bổ; mở rộng smoke Canvas kiểm tra unit, count input và AI không còn cap.
- Đồng bộ `backupcode viettailieu/canvas_xaydungphuluc.html` byte-identical với Canvas chính.

## Xác minh bổ sung

- `node tests/khbd-nls-rate-smoke.js` — PASS
- `node tests/canvas-xaydungphuluc-smoke.js` — PASS
- SHA-256 hai bản Canvas — trùng khớp

## Khắc phục VERIFY FAIL (legacy AI cap còn sót)

- Gỡ hằng số và helper giới hạn AI cũ khỏi hai bản Canvas; dải AI nay luôn cho phép 0–100% số tiết hiện có.
- Thông báo khi nạp PPCT không còn yêu cầu chọn tối đa 12 tiết AI.
- Smoke test Canvas xác nhận mã nguồn không còn hằng số hoặc thông báo giới hạn cũ, và 100% chọn toàn bộ số tiết có thể chọn.

## Xác minh lần này

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS
- `node tests/khbd-nls-rate-smoke.js` — PASS
- `node tests/xaydungphuluc-smoke.js` — PASS
- `git diff --check` — PASS
- SHA-256 Canvas chính/backup — trùng khớp (`BED1D0B532D2F0D6B85C5847BCA94A8C1468BDEC6F0CDE029A788231DD42E1EE`)
