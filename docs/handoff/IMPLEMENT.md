# IMPLEMENT: Dropdown giáo viên Lịch báo giảng — fallback PCCM / đợt / CSDL

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Module 1 — `getBaoGiangTeacherList()`
Trong `phancongtochuyenmon.html`:
- Ưu tiên 1: `state.teachers` nếu còn phần tử.
- Ưu tiên 2: `state.phase_assignments[state.info.current_phase_id].teachers`.
- Ưu tiên 3: gom giáo viên duy nhất (theo `id` / `name`) từ mọi đợt trong `phase_assignments`.
- Ưu tiên 4: `systemData.teachers`.
- Nếu root rỗng mà tìm được giáo viên từ đợt/CSDL thì đồng bộ ngược vào `state.teachers`.

## Module 2 — Dropdown & hướng dẫn TKB
- `renderBaoGiangMonthView()` render `#bg-filter-teacher` từ `getBaoGiangTeacherList()`.
- Option tổng: `Tất cả giáo viên (X GV)`.
- Từng GV: `Họ tên (Chức vụ / Số lớp phân công)`.
- Có phân công lớp/môn nhưng chưa có TKB: banner `⚠️ Thầy/cô … đã có phân công chuyên môn …` kèm nút `👉 Sang Tab Thời khóa biểu GV để nhập TKB cho thầy/cô này` (`openBaoGiangTeacherTimetable` → Tab 2).
- `renderBaoGiangView()` gọi `getBaoGiangTeacherList()` trước khi vẽ; danh sách người nhận email cũng dùng cùng nguồn.

## Module 3 — Kiểm thử
- `tests/baogiang-teacher-month-smoke.js`: fallback đợt khi `state.teachers` rỗng; PCCM chưa TKB hiện hướng dẫn; có TKB hiện lịch tháng.

## Test đã chạy
- `node tests/baogiang-teacher-month-smoke.js` — PASS
- `node tests/attendance-autosync-smoke.js` — PASS
- `node tests/baogiang-weekday-segment-smoke.js` — PASS

Không thêm chức năng ngoài plan. Cần `/verify` trên Antigravity: mở Tab 4 với giáo viên nằm trong đợt PCCM, xác nhận dropdown đủ tên GV.
