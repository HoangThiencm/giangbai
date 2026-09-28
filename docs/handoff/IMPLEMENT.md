# IMPLEMENT: Kéo thả tiết TKB và Tab 9 Đánh giá xếp loại

## Đã làm
- `phancongtochuyenmon.html`: ô tiết có nội dung `draggable="true"`. Kéo vào ô trống thì chuyển tiết; ô đích đã có tiết thì hộp thoại `1` hoán đổi / `2` ghi đè / Hủy. Sau thao tác cập nhật `editingTimetable`, vẽ lại lưới, `persistAndSaveTimetableLocal()`, và `applyTimetableToAssignments` khi checkbox tự động phân công đang bật. Class `.tt-cell.drag-target` tô viền khi kéo qua ô.
- Tab `tab-nav-danhgia` và view `view-danhgia`: lọc tháng, bảng STT / họ tên / chức vụ / số tiết TKB / số liệu chấm công / xếp loại A–D / ghi chú. Nút xếp tất cả là A, gợi ý theo chấm công (KP hoặc nghỉ nhiều → D, có phép → C, có dự giờ hoặc SHCM → A, còn lại B), xuất Excel, Lưu CSDL (`saveToDB`).
- `state.evaluations.records[YYYY-MM][teacherId] = { rating, note }`, `normalizeState` bổ sung object này, mỗi lần sửa gọi `saveToLocal()` và `hasUnsavedChanges`.
- `tests/timetable-render-smoke.js`: di chuyển sang ô trống khác buổi, hoán đổi hai ô, HTML tab/view, lưu rating C và ghi chú.

## Kiểm thử
- `node tests/timetable-render-smoke.js` → PASS (exit 0).
- Chưa mở trình duyệt. Bước sau: Antigravity IDE, chat mới, `/verify`.

## File
- `phancongtochuyenmon.html`
- `tests/timetable-render-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`
