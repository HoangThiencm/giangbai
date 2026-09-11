# IMPLEMENT

Trạng thái: HOÀN THÀNH

## File đã đổi

- `canvas_xaydungphuluc.html`
- `xaydungphuluc.html`
- `phancongtochuyenmon.html`
- `tests/xaydungphuluc-smoke.js`
- `tests/baogiang-recognition-smoke.js`

## Nội dung chính

### 1. Toggle NLS / AI trên Canvas và Phụ lục

- Gắn `onchange="onNlsEnabledChange(this.checked)"` vào `#nlsEnabled` và `onchange="onAiEnabledChange(this.checked)"` vào `#aiEnabled`.
- Bỏ check: xóa hết bài/tiết đã chọn, đồng bộ tỉ trọng về 0, làm mới bảng Mục 4.
- Check lại: nếu tỉ trọng đang 0 hoặc chưa chọn bài/tiết thì khôi phục NLS 50% / AI 30%, rồi `syncNlsSelectionFromRate()` / `syncAiSelectionFromRate()`.
- Nút "Gợi ý NLS theo tỉ trọng" / "Gợi ý AI": tự bật checkbox nếu đang tắt; nếu rate = 0 thì phục hồi 50%/30% trước khi gợi ý.

### 2. Đợt phân công TKB mới mặc định rỗng

- `#qp-inherit-assignments` giữ mặc định không chọn; nhãn đã ghi rõ để trống nhằm nhận diện TKB mới.
- `submitQuickNewPhase()` khi không kế thừa: `assignments: {}`, `timetable: emptyTimetable()`, `editingTimetable` rỗng.
- `switchPhase()` khi đợt chưa có snapshot: gán luôn `state.teachers` / `state.unassigned` từ bản rỗng, không giữ TKB đợt cũ trên giao diện.

### 3. Lịch báo giảng — Thứ mấy và phân đoạn tiết

- Email HTML: tiêu đề ngày là `Thứ Tư, ngày 09/09/2026` (không còn prefix `Ngày` chồng lên thứ).
- Email plain text giữ `Thứ Tư, 09/09/2026 | ...`.
- Bảng web: cột ngày là thứ đậm + ngày nhỏ (`09/09/2026`).
- `parseBaoGiangCurriculum` gom khối bài liền kề cùng mạch/tên chuẩn hoá; Bài 11 (1 tiết tuần 1 + 2 tiết tuần 2) ra `1/3`, `2/3`, `3/3`.

### 4. Smoke test

- `tests/xaydungphuluc-smoke.js`: assertion HTML + mô phỏng bỏ check / check lại / gợi ý NLS-AI.
- `tests/baogiang-recognition-smoke.js`: assertion Thứ mấy trên email/bảng và phân đoạn `1/3`.

## Test đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/baogiang-recognition-smoke.js` — PASS
- `node tests/baogiang-weekday-segment-smoke.js` — PASS
- `node tests/canvas-xaydungphuluc-smoke.js` — PASS
- `node tests/khbd-nls-rate-smoke.js` — PASS

## Vấn đề còn lại

Không có. `git` không có trên PATH nên chưa chạy `git diff --check`.
