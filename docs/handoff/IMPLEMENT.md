# IMPLEMENT: Thu gọn Tab 4 Lịch báo giảng — Modal PPCT & lịch nghỉ + cảnh báo collapsible

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Module 1 — Modal `#baogiang-config-modal`
- Thêm modal chuẩn (`modal-overlay` / `modal-card`, `max-width: 900px`).
- Header: `Cài đặt PPCT & Lịch nghỉ` + nút đóng `closeBaoGiangConfigModal()`.
- Body phần 1: Khối/Môn, nạp tệp AI, JSON, `#bg-curriculum`, `#bg-ppct-library`.
- Body phần 2: Form ngoại lệ nghỉ/dạy bù + `#bg-exceptions`.
- Footer: Đóng / Lưu & Áp dụng (`closeBaoGiangConfigModal(); renderBaoGiangView(); showToast(...)`).
- `openBaoGiangConfigModal()` / `closeBaoGiangConfigModal()` bật/tắt class `active`.

## Module 2 — Giao diện chính Tab 4
- Toolbar: nút `Cài đặt PPCT & Lịch nghỉ` + `Lưu kế hoạch`.
- Giữ hàng bộ lọc: Tuần 1, Giáo viên, Tháng, Chế độ xem.
- Đã bỏ `<details>` PPCT, dropdown khối/môn lộ thiên và khối Ngày nghỉ khỏi mặt chính.
- Mọi ID (`bg-curriculum`, `bg-ppct-grade`, `bg-ppct-subject`, `bg-ppct-file`, `bg-exceptions`, …) giữ nguyên, chuyển vào modal.

## Module 3 — Cảnh báo PPCT thu gọn
- Thêm `baoGiangWarningsHtml(warnings)` sinh `<details class="bg-warning-box">` (mặc định đóng).
- Summary: `Cần kiểm tra PPCT trước khi gửi email (N cảnh báo — Bấm để xem/ẩn)`.
- Nội dung cuộn `max-height: 180px; overflow-y: auto`.
- Dùng trong `renderBaoGiangBaseView()` và `renderBaoGiangView()`.

## Module 4 — Smoke
- `tests/baogiang-teacher-month-smoke.js`: kiểm tra modal chứa đủ ID, nút mở modal, cảnh báo bọc `<details>`.

## Test đã chạy
- `node tests/baogiang-teacher-month-smoke.js` — PASS
- `node tests/baogiang-weekday-segment-smoke.js` — PASS
- `node tests/baogiang-recognition-smoke.js` — PASS
- `node tests/timetable-render-smoke.js` — PASS
- `node tests/attendance-autosync-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity: mở Tab 4 → Cài đặt PPCT & Lịch nghỉ; kiểm tra cảnh báo PPCT thu gọn còn 1 dòng.
