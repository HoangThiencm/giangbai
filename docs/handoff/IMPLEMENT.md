# IMPLEMENT

## Đã triển khai hoàn tất theo PLAN.md & VERIFY.md

1. **Tầng CSDL (`api/phancong.php`):**
   - Bổ sung bảng `phancong_weekly_timetables` (`PHANCONG_SCHEMA_VERSION = '20261126-v4'`), đồng bộ 2 chiều với `data_json.weekly_timetables` khi `get` / `save` (giữ nguyên khóa chuỗi `(string)$tid` cho cả ID giáo viên dạng số), ưu tiên `bao_giang.start_date` khi tính khoảng ngày tuần, kiểm tra `$dataJson` đúng thứ tự sau `json_encode`, tự động archive TKB tuần cũ trên server trước khi ghi đè, bổ sung `action=get_week_timetable` và dọn sạch khi `reset`.

2. **Tầng Quản lý TKB theo Tuần & Đợt (`phancongtochuyenmon.html`):**
   - Khởi tạo mặc định Tab `2. Thời khoá biểu GV` ở tuần học hiện tại (`W<n>`), đưa bộ chọn **Tuần áp dụng TKB** kèm dấu `✓ Đã lưu riêng`, trạng thái nguồn và nút **Sao chép TKB tuần/đợt khác** lên ngay `#tt-workspace-header`.
   - Bật tự động lưu CSDL (`saveToLocal()` có `autoSave: true`) cho toàn bộ thao tác lưu/sửa TKB theo tuần.
   - Sửa chuẩn `snapshotPreviousWeekBeforeOverride` chụp đúng `W(week - 1)` kể cả khi đã có `W1`/`W5`; bảo toàn TKB tuần cũ ở chế độ mặc định `weekKey === ''`; bảo vệ tuyệt đối TKB hiện hành và phân công lớp hiện hành khi quay lui nhập bù TKB tuần quá khứ (`W11`).
   - Đồng bộ danh sách giáo viên Tab TKB (`filteredTimetableTeachers`, `renderTimetableTeacherList`, `selectAllTimetableTeachers`, `goToNextTimetableTeacher`), `baoGiangTeacherHasTimetable`, và các hàm tạo/gửi email TKB theo tuần áp dụng.
   - Chuẩn hóa dịch năm một lần cho bộ Đợt mẫu gốc `2025`, tự tính khoảng ngày cho các Đợt chỉ có số tuần, điền Thứ Hai đầu tuần hiện tại trong `openQuickNewPhaseModal` và tự đóng `date_end` của đợt trước trong `submitQuickNewPhase`.

3. **Tầng Sổ Dạy Thay - Bù (`#view-daythay` trong `phancongtochuyenmon.html`):**
   - Tra cứu TKB của GV nghỉ và GV dạy thay qua `resolveTeacherTimetableForDate(teacher, date, daythayTimetableSourceOverride)` trên toàn bộ luồng xem trước, gợi ý tiết tự động, phân loại GV rảnh/trùng lịch và lưu bản ghi.
   - Sửa dứt điểm lỗi kẹt tiết cũ của Tuần 12 trên `#period-slots-builder` khi đổi `#new-sub-date` về Tuần 11 (cả khi cùng buổi lẫn khi ngày mới không có tiết).
   - Hiển thị nhãn tuần cạnh `Ngày dạy`, badge nguồn CSDL rõ ràng, cảnh báo màu cam khi tuần quá khứ chưa có bản lưu riêng kèm hộp chọn **Nguồn TKB** (`onDayThaySourceOverrideChange`) và nút 1 chạm **Nhập / Sửa TKB Tuần X** mở thẳng Tab TKB đúng tuần.

4. **Kiểm thử tự động (`tests/daythay-suggest-smoke.js`, `tests/timetable-render-smoke.js`):**
   - Bổ sung đầy đủ các ca kiểm thử E2E chuyển đổi Tuần 12 ↔ Tuần 11 trong Sổ Dạy Thay, chụp snapshot `W11` khi đã có `W1`/`W5`, nhập bù tuần quá khứ `W11` bảo toàn `W12`, và kiểm tra tĩnh `api/phancong.php`.

## Tệp đã thay đổi

- `api/phancong.php`
- `phancongtochuyenmon.html`
- `tests/daythay-suggest-smoke.js`
- `tests/timetable-render-smoke.js`
- `docs/handoff/IMPLEMENT.md`

## Kiểm thử

- `node tests/daythay-suggest-smoke.js` — PASS
- `node tests/timetable-render-smoke.js` — PASS
- `node tests/baogiang-teacher-month-smoke.js` — PASS
- `node tests/baogiang-weekday-segment-smoke.js` — PASS
- `node tests/attendance-autosync-smoke.js` — PASS
- `git diff --check` — PASS
