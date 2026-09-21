# IMPLEMENT: Sửa chế độ "Dạy Ngay" (CV7991 Đúng/Sai + nhập số)

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### `taobaitap.html` — `QuizPresentationMode`
- Thêm state `cv7991Answers` + reset theo câu; `handleCv7991Select(subIdx, isTrue)`.
- UI câu Đúng/Sai CV7991: mỗi ý có nút **Đúng** / **Sai** (highlight khi chọn); khi hiện đáp án hiện badge `[ĐÚNG]`/`[SAI]` và ✓/✗ theo lựa chọn.
- Tính điểm CV7991 khi `showAns` theo thang 0.1 / 0.25 / 0.5 / 1.0.
- `handleFillBlankSubmit`: so sánh số thông minh (LaTeX `$`, dấu phẩy thập phân), gọi `setShowAns(true)`.
- Input fill-blank: `onKeyDown` Enter nộp bài; `handleKeyDown` bỏ qua phím tắt khi focus INPUT/TEXTAREA; xóa `case "Enter"` trùng.

### `smartquiz.html` — `QuizPresentationMode`
- Đồng bộ sửa fill-blank (so sánh số + `setShowAns(true)`) và chặn phím tắt khi đang gõ trong input.
- Không port CV7991 helpers (file này chưa có `isCv7991TrueFalseItem` / `getCv7991TrueFalseItems`).

### `tests/taobaitap-presentation-smoke.js`
- Cập nhật assertion fill-blank cho logic mới; vẫn tương thích bản backup chưa sửa.

## Kiểm tra
- `node tests/taobaitap-presentation-smoke.js` — PASS.
- Marker check tĩnh cho state/UI/scoring/Enter/INPUT guard trên `taobaitap.html` và fill-blank trên `smartquiz.html` — PASS.
- Chưa verify tương tác trình duyệt (không có browser tool trong phiên này). Bước tiếp: Antigravity `/verify` theo kế hoạch thủ công trong PLAN §4.
