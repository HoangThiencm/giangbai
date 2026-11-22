# IMPLEMENT — Ngày nghỉ tuần, TKB email và LBG

**Ngày:** 2026-11-22  
**Nguồn:** `docs/handoff/PLAN.md`

## Đã làm

- `phancongtochuyenmon.html`
  - Modal `#modal-manage-holidays`: chọn nhiều ngày trong một tuần, khoảng ngày dài, đối tượng Toàn trường hoặc giáo viên, buổi, lý do, bảng ngày nghỉ và xóa.
  - Nút Quản lý Ngày nghỉ ở tab Thời khóa biểu GV, tab Gửi email, tab Lịch báo giảng và trong modal PPCT.
  - Tuần áp dụng TKB: `#email-tt-week` và `#email-tt-week-all`, nhãn `Tuần N (Từ dd/mm đến dd/mm/yyyy) — N ngày nghỉ (...)`.
  - Nút gửi riêng TKB tuần cho từng GV đã chọn.
  - `isTeacherDayOff` đối chiếu `state.bao_giang.exceptions`. Ô TKB email của ngày nghỉ là `NGHỈ LỄ` (toàn trường) hoặc `NGHỈ PHÉP` (cá nhân), kèm lý do. Tiêu đề thứ có ngày và huy hiệu `(Nghỉ)` khi nghỉ toàn trường.
  - Email LBG tuần hiện khối `NGHỈ TOÀN TRƯỜNG` / `NGHỈ CÁ NHÂN` cho ngày nghỉ cả sáng và chiều.

## Kiểm tra

- `node tests/timetable-render-smoke.js` → PASS
- `node tests/baogiang-mail-smoke.js` → PASS

## Ngoài phạm vi

Không sửa file ngoài PLAN. Không commit, không push. `/verify` chạy ở chat Antigravity mới.
