# PLAN

## Hiện trạng

Khi người dùng sang Tuần 12 cập nhật Thời khóa biểu (TKB) mới rồi quay lại Sổ Dạy Thay - Bù để bổ sung lượt dạy thay bị quên ở Tuần 11, hệ thống vẫn hiển thị TKB của Tuần 12 thay vì TKB của Tuần 11. Khảo sát trực tiếp `phancongtochuyenmon.html` xác định 4 nguyên nhân gốc rễ liên hoàn:

1. **Sổ Dạy Thay - Bù không tra cứu TKB theo ngày (`date`):**
   - Hệ thống đã có sẵn hàm `getTeacherTimetableForDate(teacher, dateValue)` (dòng ~3464–3481) hỗ trợ tra cứu TKB theo `state.weekly_timetables['W' + week]`, kế thừa lùi tuần trước, tra theo `phaseTimetableForDate(teacher, iso)` và fallback về `teacher.timetable`.
   - Tuy nhiên, hàm `getTimetableDaySlots(teacher, session, dayNum)` (dòng ~9296–9310) lại đọc cứng từ `teacher?.timetable` (TKB hiện hành của Tuần 12) mà không nhận tham số `date`. Toàn bộ 5 điểm gọi trong Sổ Dạy Thay gồm `renderAbsentTeacherSchedulePreview` (dòng ~9329–9330), `autoSuggestSlotsFromTimetable` (dòng ~9372–9376, kiểm tra cứng `timetableHasLessons(teacher.timetable)`), `computeDayThayTeacherAvailability` (dòng ~9461), `renderDayThaySuggestions` (dòng ~9489) và `saveDayThayRecord` (dòng ~9789) đều bỏ qua ngày hiệu lực của TKB.
2. **`persistTeacherTimetable` ghi đè xóa sạch TKB của mọi Đợt cũ:**
   - Tại dòng ~7183–7191, `persistTeacherTimetable(teacherId, timetable)` thực thi `Object.values(state.phase_assignments || {}).forEach(snap => apply(snap.teachers))`. Bất kỳ thao tác sửa/nhập TKB mới nào ở Tuần 12 cũng ghi đè TKB mới lên tất cả các đợt phân công lịch sử trong `state.phase_assignments` (làm mất TKB của đợt Tuần 1–11 ngay cả khi người dùng đã tách Đợt mới).
3. **Giao diện chọn “Tuần áp dụng TKB” (`#tt-apply-week`) và nút “Lưu TKB tuần này” bị thiếu hàm điều khiển JS:**
   - Trong HTML đã khai báo `<select id="tt-apply-week" onchange="onTimetableApplyWeekChange(this.value)">` (dòng ~2017) và nút `<button onclick="saveTimetableForSelectedWeek()">Lưu TKB tuần này</button>` (dòng ~2083), nhưng hai hàm `onTimetableApplyWeekChange` và `saveTimetableForSelectedWeek` chưa được định nghĩa trong thẻ `<script>`. Do đó người dùng không thể chọn lưu riêng TKB cho Tuần 11 hay áp dụng TKB mới bắt đầu từ Tuần 12.
4. **Điểm hở phụ trợ ở mốc tính tuần, tạo Đợt nhanh và Lịch báo giảng / Email TKB:**
   - `timetableWeekKeyForDate` và `baoGiangSchoolWeekRange` (dòng ~3428–3444) chỉ đọc `state.bao_giang.start_date`; nếu người dùng chưa mở Tab Lịch báo giảng để đặt ngày bắt đầu Tuần 1 thì không suy ra được mã tuần `W11`/`W12` dù `state.phases[0].date_start` đã có.
   - `submitQuickNewPhase` (dòng ~5010) có ô nhập `qp-from-week` / `qp-to-week` nhưng chưa lưu `from_week`, `to_week` và chưa tự suy `date_start` / `date_end` khi người dùng để trống ngày kết thúc, làm `phaseTimetableForDate` bỏ qua đợt đó.
   - `baoGiangRows` (dòng ~3517) và `timetableEmailSessionTable` (dòng ~7497) cũng đọc cứng `teacher.timetable` thay vì tra theo ngày/tuần.

## Phạm vi

1. Sửa triệt để luồng tra cứu TKB theo ngày/tuần trong **Sổ Dạy Thay - Bù** (`#view-daythay`): chọn ngày thuộc Tuần 11 phải hiển thị đúng lịch dạy của GV nghỉ và đề xuất đúng GV dạy thay theo TKB hiệu lực của Tuần 11, không bị lẫn sang TKB Tuần 12.
2. Cô lập lưu trữ TKB theo từng Đợt (`phase_assignments`) và hoàn thiện đầy đủ chức năng lưu/chọn **TKB theo Tuần** (`#tt-apply-week`, `onTimetableApplyWeekChange`, `saveTimetableForSelectedWeek`, nạp ảnh AI / Word / JSON theo tuần áp dụng).
3. Tự động bảo toàn bản chụp TKB của tuần liền trước (`W(k-1)`) khi người dùng nạp/cập nhật TKB mới cho tuần `W<k>` (ví dụ nạp TKB mới từ Tuần 12 thì tự động giữ nguyên bản chụp TKB cũ cho Tuần 11 nếu `W11` chưa lưu riêng), đồng thời cho phép quay lại chọn `Tuần 11` để nhập/chỉnh sửa bổ sung TKB riêng của Tuần 11 bất kỳ lúc nào.
4. Đồng bộ tra cứu `getTeacherTimetableForDate` cho `baoGiangRows` và `timetableEmailSessionTable` khi có ngày/tuần xác định.
5. Bổ sung kiểm thử tự động trong `tests/daythay-suggest-smoke.js` và `tests/timetable-render-smoke.js`.

## Ngoài phạm vi

- Không thay đổi cấu trúc bảng CSDL MySQL hoặc API backend `api/phancong.php` (`state.weekly_timetables` và `state.phase_assignments` đã nằm sẵn trong `data_json` và `normalizeState`).
- Không thay đổi giao diện tổng thể, thuật toán xếp TKB tự động (`thoikhoabieu.html`), hay công thức tính tăng giờ/chấm công.
- Không can thiệp các trang HTML/JS khác ngoài danh sách file dự kiến tác động.

## File dự kiến tác động

1. `phancongtochuyenmon.html`
2. `tests/daythay-suggest-smoke.js`
3. `tests/timetable-render-smoke.js`

## Các bước thực hiện

### Bước 1: Chuẩn hóa mốc tính tuần và tra cứu TKB theo ngày/tuần/đợt trong `phancongtochuyenmon.html`
- Tạo hàm phụ trợ lấy ngày bắt đầu năm học dùng chung `effectiveSchoolStartDate()`: ưu tiên `state.bao_giang?.start_date`, nếu trống thì fallback sang `state.phases?.[0]?.date_start` (hoặc `date_start` nhỏ nhất hợp lệ trong `state.phases`). Dùng hàm này trong `baoGiangSchoolWeekRange(weekNumber)` và `timetableWeekKeyForDate(dateValue)` để tính đúng `W1`..`W35` ngay cả khi người dùng chưa cấu hình riêng Tab Lịch báo giảng.
- Cải tiến `phaseTimetableForDate(teacher, iso)` (dòng ~3450):
  - Nếu `phase` có `date_start` và `date_end`: khớp `from <= iso && iso <= to`.
  - Nếu `phase` chỉ có `date_start` (chưa nhập `date_end`): coi `to` là ngày liền trước `date_start` của đợt kế tiếp (hoặc mở về cuối năm học nếu là đợt cuối).
  - Nếu `phase` có `from_week` / `to_week` và tính được khoảng ngày qua `baoGiangSchoolWeekRange`: dùng khoảng ngày đó làm dự phòng khi thiếu `date_start` / `date_end`.
- Trong `submitQuickNewPhase()` (dòng ~5010): lưu thêm `from_week`, `to_week` (nếu hợp lệ); nếu có `from_week`/`to_week` và `effectiveSchoolStartDate()` mà người dùng chưa điền đủ `date_start`/`date_end`, tự điền `date_start` (Thứ Hai của `from_week`) và `date_end` (Chủ nhật của `to_week`).
- Kiểm tra thứ tự ưu tiên trong `getTeacherTimetableForDate(teacher, dateValue)`:
  1. Nếu `weekKey` (`W<n>`) có bản lưu riêng cho `teacher.id` trong `state.weekly_timetables[weekKey]` -> trả về bản đó.
  2. Duyệt lùi `w = n - 1` về `1`: nếu gặp `state.weekly_timetables['W' + w][teacher.id]` -> trả về bản kế thừa gần nhất trước đó (lưu ý: nếu chỉ có bản lưu ở tuần tương lai như `W12` mà ngày tra cứu thuộc `W11`, vòng lặp `W10..W1` không chạm tới `W12` nên sẽ rơi đúng xuống Bước 3 là `phaseTimetableForDate` của Đợt 1!).
  3. Tra `phaseTimetableForDate(teacher, iso)`.
  4. Fallback cuối cùng về `normalizeTeacherTimetable(teacher?.timetable)`.

### Bước 2: Sửa lỗi ghi đè liên đợt và hoàn thiện bộ điều khiển “Tuần áp dụng TKB” trong `phancongtochuyenmon.html`
- Sửa `persistTeacherTimetable(teacherId, timetable, options = {})` (dòng ~7183):
  - Chỉ cập nhật giáo viên trong `state.teachers` và snapshot của **đợt hiện tại** (`state.phase_assignments[state.info.current_phase_id]`), **bỏ** vòng lặp ghi đè lên toàn bộ `Object.values(state.phase_assignments)`.
- Hiện thực hóa đầy đủ luồng TKB theo tuần cho Tab Thời khóa biểu (`#view-timetable`):
  - Khai báo biến trạng thái `selectedTimetableWeekKey = ''` (`''` = chế độ TKB mặc định của Đợt hiện tại; `'W1'`..`'W35'` = chế độ xem/sửa TKB theo tuần cụ thể).
  - Viết hàm `getTeacherTimetableForWeekKey(teacher, weekKey)`:
    + Nếu `!weekKey`: trả về `normalizeTeacherTimetable(teacher?.timetable)`.
    + Nếu có `weekKey` (`W<n>`): nếu có `baoGiangSchoolWeekRange(n)` thì gọi `getTeacherTimetableForDate(teacher, range.start)`; nếu chưa có mốc ngày bắt đầu năm học thì kiểm tra trực tiếp `state.weekly_timetables[weekKey]?.[teacher.id]` rồi lùi về `W(n-1)..W1`, cuối cùng fallback `teacher?.timetable`.
  - Viết hàm `populateTimetableApplyWeekSelect()`:
    + Render `<option value="">Theo Đợt hiện tại (mặc định)</option>` và danh sách `W1`..`W35` (hiển thị kèm khoảng ngày `dd/mm – dd/mm` nếu có `baoGiangSchoolWeekRange`, kèm ký hiệu `✓ Đã lưu riêng` nếu tuần đó có dữ liệu trong `state.weekly_timetables`).
    + Cập nhật `#tt-apply-week-hint` nêu rõ trạng thái của tuần đang chọn (đã lưu riêng cho GV đang chọn, hay đang kế thừa từ tuần/đợt nào, hoặc gợi ý đặt ngày bắt đầu Tuần 1 nếu chưa có mốc ngày).
  - Viết hàm `onTimetableApplyWeekChange(weekKey)`:
    + Gán `selectedTimetableWeekKey = String(weekKey || '')`.
    + Nạp lại `editingTimetable` của `selectedTimetableTeacherId` theo `selectedTimetableWeekKey`, cập nhật `#tt-apply-week-hint`, `renderTimetableTeacherList()` và `renderTimetableWorkspace()`.
  - Viết hàm `snapshotPreviousWeekBeforeOverride(teacherId, targetWeekNum)`:
    + Khi người dùng lưu/nạp TKB mới vào một tuần `W<k>` (`k > 1`), kiểm tra xem từ `W1` đến `W(k-1)` giáo viên `teacherId` đã có bản lưu tuần nào chưa và đợt cũ có giữ TKB khác hay không; nếu chưa có bất kỳ bản lưu nào cho giai đoạn trước `W<k>` mà `teacher.timetable` hiện có tiết học, tự động lưu bản chụp `teacher.timetable` cũ vào `state.weekly_timetables['W1'][String(teacherId)]` (hoặc `W(k-1)` nếu phù hợp) để toàn bộ các tuần `1..k-1` giữ nguyên TKB cũ không bị trôi theo `W<k>`.
  - Viết hàm `saveTimetableForSelectedWeek()`:
    + Xác định `weekKey` từ `#tt-apply-week` (nếu đang để `""`, tự gợi ý tuần hiện tại tính từ hôm nay qua `timetableWeekKeyForDate(baoGiangIso(new Date()))` hoặc hỏi xác nhận tuần muốn lưu).
    + Gọi `snapshotPreviousWeekBeforeOverride(teacherId, weekNum)` trước khi ghi vào `state.weekly_timetables[weekKey][String(teacherId)]`.
    + Nếu `weekKey` trùng hoặc lớn hơn tuần hiện tại (hoặc đang ở đợt hiện hành mà chưa có TKB gốc), đồng bộ vào `persistTeacherTimetable(teacherId, editingTimetable)` của đợt hiện tại; ngược lại nếu người dùng đang quay lại sửa một tuần quá khứ (ví dụ đang ở Tuần 12 nhưng chọn `W11` để nhập lại TKB cũ của Tuần 11), **chỉ ghi vào `state.weekly_timetables['W11']`** (và nếu Tuần 12 chưa chốt riêng thì tự chốt TKB hiện hành của GV vào `W12` trước để sửa `W11` không làm hỏng `W12`!).
    + Lưu `saveToLocal()`, cập nhật lại dropdown/hint và báo toast rõ ràng: `Đã lưu TKB riêng cho Tuần X của GV ...`.
  - Cập nhật `persistAndSaveTimetableLocal()`, `applyWordTimetableDirectly()`, `importTimetableFromJson()`, `applyAiTimetableResult()`, `selectTimetableTeacher()` và `renderTimetableView()`:
    + Khi `selectedTimetableWeekKey` đang là một tuần cụ thể `W<k>`, mọi thao tác sửa ô, kéo thả ô, AI nhận diện ảnh, nạp Word `.docx`, nạp JSON AI đều lưu đúng vào tuần `W<k>` (kèm cơ chế bảo vệ không làm hỏng tuần hiện tại nếu `W<k>` là tuần quá khứ, và bảo vệ tuần cũ `1..k-1` nếu `W<k>` là tuần mới bắt đầu áp dụng TKB mới!).

### Bước 3: Kết nối Sổ Dạy Thay - Bù, Lịch Báo Giảng và Email TKB với TKB theo ngày/tuần
- Cập nhật `getTimetableDaySlots(teacher, session, dayNum, dateValue = '')` (dòng ~9296):
  - Khi gọi đệ quy cho `session === 'all_day'`, truyền tiếp `dateValue`: `getTimetableDaySlots(teacher, part, dayNum, dateValue)`.
  - Lấy nguồn TKB bằng:
    ```javascript
    const resolvedTimetable = (dateValue && typeof getTeacherTimetableForDate === 'function')
        ? getTeacherTimetableForDate(teacher, dateValue)
        : teacher?.timetable;
    const block = resolvedTimetable?.[session === 'afternoon' ? 'afternoon' : 'morning'];
    ```
    (Giữ tương thích ngược 100% khi các bài test cũ gọi 3 tham số không truyền `dateValue` hoặc không nạp `getTeacherTimetableForDate`).
- Cập nhật toàn bộ 5 vị trí trong Sổ Dạy Thay - Bù:
  1. `renderAbsentTeacherSchedulePreview()` (dòng ~9329–9342):
     - Gọi `getTimetableDaySlots(teacher, 'morning', dayNum, date)` và `getTimetableDaySlots(teacher, 'afternoon', dayNum, date)`.
     - Hiển thị rõ ngữ cảnh tuần/đợt trên tiêu đề khung xem trước (ví dụ: `📅 Lịch dạy Thứ Tư (18/11/2026 · Tuần 11) của thầy/cô ...`) để người dùng thấy ngay hệ thống đang áp dụng đúng TKB của Tuần 11.
  2. `autoSuggestSlotsFromTimetable()` (dòng ~9372–9376):
     - Thay `timetableHasLessons(teacher.timetable)` bằng kiểm tra trên `const effectiveTt = typeof getTeacherTimetableForDate === 'function' ? getTeacherTimetableForDate(teacher, date) : teacher.timetable; if (!timetableHasLessons(effectiveTt)) ...`.
     - Gọi `getTimetableDaySlots(teacher, session, dayNum, date)`.
  3. `computeDayThayTeacherAvailability(date, session, forTeacherId, neededPeriods)` (dòng ~9461):
     - Gọi `getTimetableDaySlots(teacher, session, dayNum, date)`.
  4. `renderDayThaySuggestions()` (dòng ~9489):
     - Gọi `getTimetableDaySlots(absentTeacher, session, availability.dayNum, date)`.
  5. `saveDayThayRecord()` (dòng ~9789):
     - Gọi `getTimetableDaySlots(absentTeacher, session, dayNum, date)`.
- Đồng bộ thêm 2 điểm liên quan trực tiếp đến hiển thị TKB theo tuần:
  - `baoGiangRows(until)` (dòng ~3517): thay `normalizeTeacherTimetable(teacher.timetable)` bằng `getTeacherTimetableForDate(teacher, date)`.
  - `timetableEmailSessionTable(teacher, session, weekRange = null)` (dòng ~7497): khi có `weekRange?.start`, lấy `getTeacherTimetableForDate(teacher, weekRange.start)` thay vì đọc cứng `teacher.timetable`.

### Bước 4: Bổ sung kiểm thử tự động (Smoke Tests)
- Trong `tests/daythay-suggest-smoke.js`:
  - Thêm kịch bản tái hiện đúng lỗi thực tế của người dùng: Năm học bắt đầu `2026-09-07` (Tuần 1); Tuần 11 (`2026-11-16`) giáo viên A dạy `Tiết 1 - 7/9` và giáo viên B rảnh Tiết 1; sang Tuần 12 (`2026-11-23`) TKB đổi thành giáo viên A dạy `Tiết 3 - 7/10` và giáo viên B bận Tiết 1. Kiểm chứng khi chọn ngày `2026-11-16` (Tuần 11) trong Sổ Dạy Thay:
    + `renderAbsentTeacherSchedulePreview()` hiển thị đúng `Tiết 1 · 7/9` (TKB Tuần 11), không hiển thị `Tiết 3 · 7/10` (TKB Tuần 12).
    + `computeDayThayTeacherAvailability('2026-11-16', ...)` vẫn xếp giáo viên B vào nhóm rảnh tiết cần thay theo đúng TKB Tuần 11.
    + Khi chuyển ngày sang `2026-11-23` (Tuần 12), hệ thống lập tức hiển thị `Tiết 3 · 7/10` theo TKB Tuần 12.
  - Kiểm chứng cả hai con đường lưu lịch sử TKB: (a) qua `state.weekly_timetables` (`W11` vs `W12`) và (b) qua 2 Đợt phân công `state.phases` / `state.phase_assignments`.
- Trong `tests/timetable-render-smoke.js`:
  - Kiểm chứng `persistTeacherTimetable` chỉ cập nhật đợt hiện tại (`current_phase_id`), bảo toàn nguyên vẹn TKB của đợt trước trong `state.phase_assignments`.
  - Kiểm chứng `onTimetableApplyWeekChange` và `saveTimetableForSelectedWeek` tồn tại, hoạt động đúng và khi sửa bổ sung `W11` ở thời điểm Tuần 12 thì không làm mất TKB `W12`.

## Rủi ro

1. **Rủi ro mất TKB tuần hiện tại khi quay lui sửa tuần cũ:** Nếu người dùng đang ở Tuần 12 (chỉ mới lưu TKB Tuần 12 trong `teacher.timetable` mà chưa lưu vào `weekly_timetables['W12']`), rồi chọn `W11` trên `#tt-apply-week` để nhập lại TKB Tuần 11: nếu không tự chốt `teacher.timetable` hiện hành vào `W12` trước, thì từ `W12` trở đi sẽ kế thừa lùi từ `W11` và mất TKB Tuần 12. -> **Giải pháp kiểm soát:** Trước khi ghi bản lưu riêng cho một tuần quá khứ `W<past>` (`past < currentWeek`), nếu `W<currentWeek>` chưa có bản lưu riêng trong `weekly_timetables`, hệ thống tự động snapshot `teacher.timetable` hiện tại vào `W<currentWeek>` để bảo vệ tuyệt đối TKB Tuần 12.
2. **Rủi ro tương thích ngược với các bài smoke test hiện hữu dùng `vm.createContext`:** Một số test trong `tests/daythay-suggest-smoke.js` chỉ trích xuất riêng lẻ vài hàm vào sandbox `vm` không có `getTeacherTimetableForDate`. -> **Giải pháp kiểm soát:** Dùng kiểm tra `typeof getTeacherTimetableForDate === 'function'` trong `getTimetableDaySlots` và `autoSuggestSlotsFromTimetable` để giữ tương thích 100%.
3. **Rủi ro chưa nhập `bao_giang.start_date`:** Nếu cả `bao_giang.start_date` lẫn `phases[0].date_start` đều trống thì không quy đổi được ngày dương lịch sang số thứ tự tuần học `W11`/`W12`. -> **Giải pháp kiểm soát:** Fallback qua `effectiveSchoolStartDate()` và hiển thị thông báo rõ trong `#tt-apply-week-hint` để người dùng biết đặt ngày bắt đầu Tuần 1 hoặc ngày hiệu lực Đợt.

## Cách kiểm thử

Chạy bộ kiểm thử tự động bằng Node.js tại thư mục gốc dự án:
1. `node tests/daythay-suggest-smoke.js`
2. `node tests/timetable-render-smoke.js`
3. Kiểm tra cú pháp toàn khối script trong `phancongtochuyenmon.html` (extract script và `new Function` / `node --check`) bảo đảm không có lỗi cú pháp hay hàm bị gọi mà chưa định nghĩa.

## Tiêu chí nghiệm thu

1. Khi TKB thay đổi ở Tuần 12 (dù tách Đợt mới hay chọn lưu TKB áp dụng từ Tuần 12), quay lại Sổ Dạy Thay - Bù chọn bất kỳ ngày nào thuộc Tuần 11 đều hiển thị **đúng TKB của Tuần 11** (cả lịch dạy của GV nghỉ, gợi ý tiết tự động, danh sách GV rảnh/trùng lịch và điều kiện lưu bản ghi).
2. Khi chọn ngày thuộc Tuần 12 trong Sổ Dạy Thay - Bù, hệ thống hiển thị **đúng TKB mới của Tuần 12**.
3. Cập nhật TKB ở Đợt 2 không làm ghi đè mất TKB đã lưu ở Đợt 1 trong `state.phase_assignments`.
4. Dropdown `#tt-apply-week` và nút `Lưu TKB tuần này` (`saveTimetableForSelectedWeek`) hoạt động trơn tru, không phát sinh `ReferenceError`; cho phép người dùng quay lại chọn `Tuần 11` để nạp/sửa bổ sung TKB cũ mà vẫn giữ nguyên TKB `Tuần 12`.
5. Toàn bộ các bài test `node tests/daythay-suggest-smoke.js` và `node tests/timetable-render-smoke.js` đều **PASS 100%**.
