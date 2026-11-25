# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- File source được phép sửa theo `docs/handoff/PLAN.md`:
  - `phancongtochuyenmon.html` — ĐÚNG SCOPE
  - `tests/daythay-suggest-smoke.js` — ĐÚNG SCOPE
  - `tests/timetable-render-smoke.js` — ĐÚNG SCOPE
- File handoff: `docs/handoff/IMPLEMENT.md`, `docs/handoff/VERIFY.md`; `docs/handoff/.lock` giữ nguyên (`LOCK`).
- Không có file ngoài scope bị đụng tới (`api/phancong.php` và các file khác không đổi).

## Test đã chạy
1. `node tests/daythay-suggest-smoke.js` -> **PASS** (`PASS: daythay suggestions classify availability, select a substitute teacher, and hide for makeup.`)
2. `node tests/timetable-render-smoke.js` -> **PASS** (`PASS: timetable view loads numeric IDs and JSON data, preserves phase history, supports weekly snapshots, aligns AI periods, renders after AI sync errors, and builds selected-teacher timetable email.`)
3. `git diff --check` + kiểm tra cú pháp inline `<script>` (`new vm.Script(...)`) trên `phancongtochuyenmon.html` -> **PASS**
4. Kịch bản tích hợp E2E trên hàm thực tế của `phancongtochuyenmon.html` (tách biệt TKB theo đợt `persistTeacherTimetable`, snapshot theo tuần `W11`/`W12`, sửa bù ngược quá khứ `W11` không ghi đè `W1`, tự suy ra mốc Tuần 1 `07/09/2026` khi `bao_giang.start_date` trống hoặc đợt mặc định lệch năm `2025`, và đồng bộ ngày `2026-11-23`..`2027-01-10` trong `calcWeeksFromRange`/`submitQuickNewPhase`) -> **PASS**

## Pass / Fail từng tiêu chí
1. **Tiêu chí 1 (Cách ly TKB giữa các đợt / tuần):** **PASS** — `persistTeacherTimetable` chỉ cập nhật `state.teachers` và `state.phase_assignments[state.info.current_phase_id]`, không ghi đè ngược sang các đợt lịch sử; `saveTimetableForTeacherWeek` bảo toàn cả trường hợp cập nhật tuần mới (`week >= currentWeek` -> snapshot mốc cũ) lẫn sửa bù tuần quá khứ (`week < currentWeek` -> snapshot `currentWeek` và không làm bẩn `W1`).
2. **Tiêu chí 2 (Tra cứu đúng TKB theo ngày dạy thay của cả GV nghỉ và GV dạy thay):** **PASS** — `getTimetableDaySlots(teacher, session, dayNum, dateValue)` tra qua `getTeacherTimetableForDate(teacher, dateValue)` tại toàn bộ 5 luồng Dạy thay (`renderAbsentTeacherSchedulePreview`, `autoSuggestSlotsFromTimetable`, `computeDayThayTeacherAvailability`, `renderDayThaySuggestions`, `saveDayThayRecord`), đồng thời đồng bộ ở `baoGiangRows` và `timetableEmailSessionTable`.
3. **Tiêu chí 3 (Hiển thị rõ nguồn TKB đang áp dụng ở modal Dạy thay & Báo giảng):** **PASS** — `#dt-absent-schedule-preview` hiển thị badge nguồn TKB cụ thể theo tuần/đợt áp dụng; `#tt-apply-week-select` và `#tt-apply-week-hint` hiển thị mốc áp dụng và cảnh báo mốc Tuần 1 suy luận khi chưa cấu hình `bao_giang.start_date`.
4. **Tiêu chí 4 (Tạo đợt mới nhanh theo tuần khớp mốc đầu tuần / cuối tuần):** **PASS** — `effectiveSchoolStartDate`, `generateDefaultPhases`, `calcWeeksFromRange`, `openQuickNewPhase` và `submitQuickNewPhase` tính đúng Thứ 2 đầu tuần bắt đầu và Chủ nhật cuối tuần kết thúc theo năm học hiện hành (VD: Tuần 12..18 năm học `2026 - 2027` -> `2026-11-23` đến `2027-01-10`).
5. **Tiêu chí 5 (Tương thích ngược dữ liệu JSON cũ & pass toàn bộ smoke tests):** **PASS** — Dữ liệu cũ chưa có `timetable_by_week` tự động fallback về TKB theo đợt hoặc `teacher.timetable`; cả 2 smoke tests `tests/daythay-suggest-smoke.js` và `tests/timetable-render-smoke.js` đều PASS.

## Bug
- Lỗi: Không phát hiện lỗi.
- Tái hiện: Không.
- File liên quan: Không.
