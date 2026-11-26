# PLAN

## Hiện trạng

Khi người dùng ở Tuần 12 (đã có Thời khóa biểu mới của Tuần 12) quay lại tab **5. Sổ Dạy Thay - Bù** chọn ngày thuộc Tuần 11 để nhập bổ sung lượt dạy thay bị quên, hệ thống vẫn hiển thị TKB của Tuần 12 mà không lấy được dữ liệu TKB của Tuần 11 từ CSDL. Khảo sát mã nguồn thực tế (`phancongtochuyenmon.html` và `api/phancong.php`) xác định **6 nguyên nhân gốc rễ**:

1. **CSDL MySQL (`api/phancong.php`) chỉ lưu đè 1 bản ghi duy nhất, chưa lưu lịch sử TKB theo tuần trên CSDL và tắt auto-save khi lưu TKB tuần:**
   - Bảng `phancong_chuyenmon` (dòng 131–147, 374–380 của `api/phancong.php`) chỉ có 1 dòng `data_json` cho mỗi `(owner_id, plan_key)`. Mỗi lần lưu ở Tuần 12 là `UPDATE` ghi đè thẳng lên `data_json` cũ mà không có bảng CSDL lưu riêng từng tuần (`W1..W35`) và không tự động archive bản TKB đang lưu của tuần trước (`W11`) trước khi ghi đè.
   - Tại `phancongtochuyenmon.html` dòng 7321 (`saveTimetableForSelectedWeek`) và dòng 7363 (`persistAndSaveTimetableLocal`), hệ thống gọi `saveToLocal({ autoSave: false })`, khiến thao tác sửa TKB hoặc bấm **Lưu TKB tuần này** chỉ lưu ở `localStorage` máy cục bộ mà không tự động đồng bộ lên CSDL MySQL.

2. **Tab `2. Thời khoá biểu GV` giấu hộp chọn tuần trong `<details>` đóng kín và mặc định `selectedTimetableWeekKey = ''` (ghi đè toàn đợt):**
   - `<select id="tt-apply-week">` (dòng 2017) nằm ẩn bên trong `<details id="tt-import-details">` (mặc định thu gọn), trên thanh tiêu đề `#tt-workspace-header` không hiển thị đang xem/sửa TKB của tuần nào.
   - Biến `selectedTimetableWeekKey` khởi tạo bằng `''` (`"Theo Đợt hiện tại (mặc định)"`, dòng 6891). Khi người dùng nạp TKB ở Tuần 11 rồi sang Tuần 12 nạp TKB mới (bằng Word `.docx`, ảnh AI, JSON AI hoặc sửa ô trực tiếp) mà không mở `<details>` chọn tuần, `saveTimetableForTeacherWeek` (dòng 7297) gặp `if (!weekKey) { persistTeacherTimetable(...); return; }` nên **ghi đè thẳng TKB Tuần 12 lên TKB Tuần 11** trong `teacher.timetable` và `phase_assignments[current_phase_id]`, không hề lưu `W11` hay `W12` vào `state.weekly_timetables`.

3. **Lỗi chụp snapshot `snapshotPreviousWeekBeforeOverride` và lỗi che khuất (shadowing) trong `weekly_timetables`:**
   - Tại dòng 7282–7294, `snapshotPreviousWeekBeforeOverride(teacherId, targetWeekNum)` kiểm tra `hasEarlier` trên toàn bộ `W1..W(targetWeekNum - 1)` và chỉ lưu vào `W1`. Nếu từ đầu năm đã có bất kỳ bản lưu tuần nào (ví dụ `W1` hoặc `W5`), thì khi sang `W12` lưu TKB mới, `hasEarlier === true` làm hàm này **bỏ qua không chụp lại TKB của `W11` (`W(targetWeekNum - 1)`)**.
   - Ngược lại, nếu trong `weekly_timetables` đã có một tuần cũ (ví dụ `W1`), sau đó người dùng sửa TKB ở chế độ mặc định (`weekKey = ''`), `persistTeacherTimetable` chỉ cập nhật `teacher.timetable` trong khi `getTeacherTimetableForDate` (dòng 3501–3507) luôn ưu tiên quét lùi `weekly_timetables` trước `phaseTimetableForDate` và `teacher.timetable`, gây lệch dữ liệu giữa các tuần/đợt.

4. **Lỗi tra cứu TKB theo Đợt (`phaseTimetableForDate`, `normalizeState`, `openQuickNewPhaseModal`, `submitQuickNewPhase`):**
   - Dữ liệu CSDL của các tổ tạo từ bộ mẫu cũ `DEFAULT_PHASES` (dòng 3220–3225) vẫn mang ngày năm `2025` (`2025-09-05`..`2026-01-10`) dù `school_year` là `2026 - 2027`; `normalizeState` chưa chuẩn hóa lại năm cho các đợt mẫu lệch năm này, khiến khi chọn ngày `2026-11-16` (Tuần 11) không khớp đợt nào và rơi thẳng về `teacher.timetable` (Tuần 12).
   - Các đợt khai báo trong `Khai báo tổ -> 2. Các Đợt Phân Công` (`renderConfigPhasesTable`, dòng 10539) chỉ nhập `Số tuần` mà để trống `Từ ngày`/`Đến ngày` bị `phaseTimetableForDate` bỏ qua hoàn toàn.
   - `openQuickNewPhaseModal` (dòng 5009) gán `qp-date-start` bằng ngày hiện tại giữa tuần (ví dụ Thứ Năm `2026-11-26`) thay vì Thứ Hai đầu tuần (`2026-11-23`), và `submitQuickNewPhase` không đóng `date_end` của đợt liền trước dẫn tới chồng lấn khoảng ngày; `phaseTimetableForDate` lại duyệt xuôi từ `index = 0` nên khớp nhầm đợt khi các đợt lồng nhau.

5. **Lỗi giữ kẹt tiết cũ trên lưới Sổ Dạy Thay và thiếu kết nối nguồn CSDL tuần trên `#view-daythay`:**
   - Trong `onDayThayAbsentContextChange()` -> `renderAbsentTeacherSchedulePreview()` (dòng 6798–6805, 9485–9494): khi mở Sổ Dạy Thay ở Tuần 12 (đã nạp tiết của Tuần 12 vào `#period-slots-builder`), rồi đổi `#new-sub-date` về một ngày thuộc Tuần 11 mà ngày đó GV nghỉ không có tiết (`autoSession === ''`) hoặc không kích hoạt `onDayThaySessionChange`, lưới `#period-slots-builder` không được làm mới nên **vẫn giữ nguyên các tiết/lớp của Tuần 12**.
   - Bấm nút `TKB Giáo viên` (`openTeacherTimetableModal`, dòng 2224 & 7331) khi đang chọn ngày Tuần 11 ở Sổ Dạy Thay không truyền tuần của `#new-sub-date` sang Tab TKB, khiến Tab TKB mở ra vẫn hiển thị TKB hiện hành của Tuần 12.
   - Khung xem trước lịch dạy trong Sổ Dạy Thay chưa cho người dùng biết dữ liệu đang lấy từ **bản CSDL riêng của Tuần 11**, **kế thừa từ tuần/đợt nào**, hay **đang fallback tạm về TKB hiện hành (Tuần 12) do Tuần 11 chưa có bản lưu riêng trên CSDL**; đồng thời chưa có công cụ chọn nguồn TKB tuần/đợt/kế hoạch CSDL hoặc mở nhập bổ sung đúng TKB Tuần 11 ngay từ Sổ Dạy Thay.

6. **Lỗi hiển thị danh sách GV ở Tab TKB & đồng bộ phân công khi nhập bù TKB tuần quá khứ:**
   - Danh sách giáo viên bên trái Tab TKB (`filteredTimetableTeachers` dòng 7372, `renderTimetableTeacherList` dòng 7407, 7417–7418, `goToNextTimetableTeacher` dòng 7791) luôn kiểm tra `t.timetable` thay vì TKB hiệu lực của tuần đang chọn (`selectedTimetableWeekKey`).
   - Khi đang ở Tuần 12 nhưng chọn `Tuần 11 (W11)` để nạp lại file Word/AI/JSON khôi phục TKB Tuần 11, lệnh `applyTimetableToAssignments` (dòng 7113, 7130, 8397) vẫn tự chạy làm ảnh hưởng phân công hiện hành của Tuần 12 hoặc đọc nhầm `teacher.timetable`.

## Phạm vi

1. **Tầng CSDL (`api/phancong.php`):**
   - Bổ sung bảng MySQL `phancong_weekly_timetables` lưu độc lập bản chụp TKB của từng tuần (`owner_id`, `plan_key`, `week_key`, `week_num`, `start_date`, `end_date`, `timetables_json`, `updated_at`).
   - Tự động bảo vệ lịch sử trên server khi `action=save`: trước khi ghi đè `phancong_chuyenmon`, nếu dữ liệu cũ trên CSDL có TKB giáo viên và tuần tương ứng với thời điểm cập nhật cũ (`oldWeekKey`) chưa có trong `phancong_weekly_timetables`, tự động lưu trữ bản TKB cũ đó vào `phancong_weekly_timetables` để không bao giờ mất TKB tuần trước trên CSDL.
   - Đồng bộ 2 chiều giữa `phancong_weekly_timetables` và `data_json.weekly_timetables` khi `action=get` / `action=save`, đồng thời thêm action đọc TKB từ một kế hoạch/tuần CSDL đã lưu (`action=get_week_timetable`) khi người dùng muốn nạp/khôi phục chéo.
2. **Tầng Quản lý TKB theo Tuần & Đợt (`phancongtochuyenmon.html`):**
   - Đưa thanh chọn **Tuần áp dụng TKB** ra ngay đầu khu vực làm việc `#tt-workspace-header` (hiển thị rõ khoảng ngày, trạng thái đã lưu CSDL riêng hay kế thừa), đồng bộ với `#tt-apply-week`, và mặc định chọn **Tuần học hiện tại** (ví dụ `W12`) khi mở Tab TKB để mọi thao tác nhập mới ở Tuần 12 không ghi đè mất Tuần 11.
   - Bật tự động lưu CSDL (`saveToLocal()` có `autoSave: true`) cho toàn bộ thao tác lưu/nhập/chỉnh sửa TKB theo tuần.
   - Sửa chuẩn xác `snapshotPreviousWeekBeforeOverride` (chụp đúng trạng thái hiệu lực của `W(week - 1)` trước khi ghi `W<week>`), xử lý không để tuần cũ che khuất khi cập nhật theo Đợt, và chuẩn hóa tra cứu ngày/đợt (`normalizeState`, `phaseTimetableForDate`, `resolveTeacherTimetableForDate` trả kèm thông tin nguồn dữ liệu).
   - Khi chọn xem/nhập một tuần quá khứ (`week < currentWeek`, ví dụ quay về `W11` để nạp lại TKB Tuần 11): hiển thị đúng số tiết của `W11` trên danh sách GV bên trái, bảo toàn nguyên vẹn TKB `W12`, và không ghi đè phân công lớp hiện hành của `W12`.
3. **Tầng Sổ Dạy Thay - Bù (`#view-daythay` trong `phancongtochuyenmon.html`):**
   - Đảm bảo khi chọn/đổi ngày thuộc Tuần 11, toàn bộ preview lịch dạy của GV nghỉ, gợi ý tự động lưới tiết `#period-slots-builder`, danh sách gợi ý GV dạy thay rảnh/trùng lịch và kiểm tra lưu bản ghi đều lấy đúng TKB của Tuần 11 (xóa sạch tiết cũ của Tuần 12 trên lưới nếu ngày/buổi ở Tuần 11 không có tiết hoặc khác tiết).
   - Hiển thị rõ badge **Nguồn CSDL TKB đang áp dụng** ngay trên khung lịch Sổ Dạy Thay (VD: `✓ CSDL TKB Tuần 11`, `↪ Kế thừa TKB Tuần X / Đợt ...`, hoặc cảnh báo màu cam nếu Tuần 11 chưa có CSDL riêng mà đang tạm dùng TKB hiện hành) kèm:
     + Hộp chọn nhanh **Nguồn TKB áp dụng cho lượt này** (`Tự động theo ngày (Tuần 11)` hoặc chọn đích danh một Tuần `W1..W35` / Đợt / Kế hoạch CSDL khác đã lưu nếu cần đối chiếu/lấy lịch).
     + Nút 1 chạm **`Nhập / Sửa TKB Tuần 11`** mở thẳng Tab TKB đã chọn sẵn đúng `Tuần 11` và giáo viên đó.
4. **Kiểm thử tự động:** Cập nhật và mở rộng `tests/daythay-suggest-smoke.js` và `tests/timetable-render-smoke.js`.

## Ngoài phạm vi

- Không thay đổi giao diện hay thuật toán xếp TKB tự động của trang độc lập `thoikhoabieu.html` / `api/thoikhoabieu.php`.
- Không thay đổi công thức tính định mức chuẩn, công thức quyết toán tăng giờ hay cấu trúc bảng chấm công tháng.
- Không sửa các trang HTML/PHP khác ngoài danh sách file dự kiến tác động.

## File dự kiến tác động

1. `api/phancong.php`
2. `phancongtochuyenmon.html`
3. `tests/daythay-suggest-smoke.js`
4. `tests/timetable-render-smoke.js`

## Các bước thực hiện

### Bước 1: Bổ sung lưu trữ & tự động bảo toàn lịch sử TKB theo tuần trong CSDL (`api/phancong.php`)
- Nâng `PHANCONG_SCHEMA_VERSION` lên `'20261126-v4'`. Trong `phancong_ensure_schema(PDO $pdo)`, tạo bảng `phancong_weekly_timetables`:
  - Các cột: `id INT AUTO_INCREMENT PRIMARY KEY`, `owner_id INT NOT NULL`, `plan_key VARCHAR(80) NOT NULL DEFAULT 'default'`, `school_year VARCHAR(40) NOT NULL DEFAULT ''`, `week_key VARCHAR(16) NOT NULL`, `week_num INT NOT NULL DEFAULT 0`, `start_date VARCHAR(10) NOT NULL DEFAULT ''`, `end_date VARCHAR(10) NOT NULL DEFAULT ''`, `timetables_json LONGTEXT NOT NULL`, `updated_by INT DEFAULT NULL`, `created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP`, `updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`.
  - Khóa duy nhất `UNIQUE KEY uq_phancong_owner_plan_week (owner_id, plan_key, week_key)` và index `(owner_id, plan_key, week_num)`.
- Viết hàm phụ trợ PHP:
  - `phancong_infer_week_key(array $stateData, string $isoDate): string`: tính `W<n>` (`1..45`) từ `bao_giang.start_date`, hoặc `phases` hợp lệ cùng năm học `info.school_year`, hoặc mốc khai giảng Thứ Hai tuần `05/09` của năm bắt đầu năm học.
  - `phancong_extract_teacher_timetables(array $stateData): array`: trích map `[ (string)$teacherId => $timetable ]` của các giáo viên có tiết học thực sự trong `morning`/`afternoon`.
  - `phancong_load_weekly_timetables(PDO $pdo, int $ownerId, string $planKey): array`: đọc toàn bộ các dòng từ `phancong_weekly_timetables` của `(owner_id, plan_key)` trả về `['map' => [ 'W11' => [...], ... ], 'meta' => [ 'W11' => ['updated_at' => ..., 'start_date' => ..., 'end_date' => ..., 'teacher_count' => ... ] ]]`.
  - `phancong_sync_weekly_timetables(PDO $pdo, int $ownerId, string $planKey, string $schoolYear, array $weeklyMap, int $userId): void`: upsert từng `week_key` hợp lệ (`/^W([1-9]\d?)$/`) có dữ liệu vào bảng `phancong_weekly_timetables`; nếu một tuần trong `weeklyMap` bị xóa rỗng hoàn toàn (`empty`), đồng bộ xóa bản ghi tuần đó khi client gửi cờ xác nhận.
- Trong `action === 'save'`:
  1. Trước khi `UPDATE phancong_chuyenmon`, đọc `data_json` và `updated_at` hiện có của `(owner_id, plan_key)`.
  2. Nếu bản ghi cũ tồn tại, trích `$oldTimetables = phancong_extract_teacher_timetables($oldState)` và xác định `$oldWeekKey = $oldState['info']['active_timetable_week'] ?? phancong_infer_week_key($oldState, substr((string)$existing['updated_at'], 0, 10))`.
  3. Nếu `$oldWeekKey !== ''` và `$oldTimetables` không rỗng, kiểm tra nếu cả bảng `phancong_weekly_timetables` lẫn `$incomingState['weekly_timetables'][$oldWeekKey]` chưa có dữ liệu cho `$oldWeekKey` (trong khi TKB mới gửi lên đã thay đổi khác `$oldTimetables`), tự động chèn bản chụp `$oldTimetables` vào `$incomingState['weekly_timetables'][$oldWeekKey]` và lưu xuống `phancong_weekly_timetables`.
  4. Merge thêm các tuần đã có trong `phancong_weekly_timetables` mà client chưa gửi xóa để không bao giờ làm rơi rụng lịch sử tuần cũ, sau đó lưu `data_json` và gọi `phancong_sync_weekly_timetables(...)`.
- Trong `action === 'get'`:
  - Tải thêm `phancong_load_weekly_timetables($pdo, $ownerId, $planKey)`, hợp nhất vào `$parsedData['weekly_timetables']` (ưu tiên dữ liệu hợp lệ đầy đủ cho từng `week_key` + `teacher_id`), và trả thêm trường `'weekly_meta' => $loadedWeeks['meta']` trong JSON phản hồi.
- Bổ sung `action === 'get_week_timetable'`:
  - Cho phép truyền `plan_key` và `week_key` (hoặc `source_plan_key` từ một kế hoạch khác của cùng `owner_id`) để lấy trực tiếp TKB từ CSDL khi người dùng muốn nạp/khôi phục TKB cho một tuần cụ thể.
- Trong `action === 'reset'`: xóa kèm các dòng tương ứng của `(owner_id, plan_key)` trong `phancong_weekly_timetables`.

### Bước 2: Chuẩn hóa giải thuật xác định mốc tuần, Đợt phân công và tra cứu TKB kèm nguồn dữ liệu (`phancongtochuyenmon.html`)
- **Lưu ý kỹ thuật bắt buộc cho các bài smoke test hiện hữu:** Các file test trong `tests/*.js` dùng hàm `declaration(name)` cắt từ `function <name>(` đến `\n        function ` tiếp theo và chạy trong `vm.createContext` tối giản. Vì vậy:
  - Mọi biến cấp module phải khai báo ở vùng biến đầu `<script>`, không đặt `let`/`const` xen giữa các hàm cấp cao.
  - Giữ đúng thụt lề 8 dấu cách `        function tênHàm(` cho tất cả các hàm top-level.
  - Khi gọi hàm phụ trợ mới bên trong các hàm cũ đang được unit-test cô lập (`renderTimetableView`, `selectTimetableTeacher`, `getTimetableDaySlots`, `renderAbsentTeacherSchedulePreview`, `renderDayThaySuggestions`, `computeDayThayTeacherAvailability`), luôn kiểm tra `typeof ... === 'function'` để tương thích ngược 100% với sandbox `vm`.
- Trong `normalizeState(s)`:
  - Nếu `s.phases` đang chứa bộ ngày mẫu năm `2025` (`2025-09-05`, `2025-11-06`, `2026-01-12`, `2026-03-23`) trong khi `s.info.school_year` hoặc `s.bao_giang.start_date` xác định năm học bắt đầu khác `2025` (ví dụ `2026 - 2027` -> năm bắt đầu `2026`), tự động dịch năm của các đợt mẫu chưa chỉnh sửa sang đúng năm học thực tế (`+ (startYear - 2025)`).
- Viết hàm `resolvePhaseDateRanges(phases)`:
  - Tính khoảng `[from, to, fromWeek, toWeek]` đầy đủ cho mọi phần tử trong `state.phases`:
    + Nếu đợt có `date_start` / `date_end`: dùng trực tiếp; nếu thiếu một đầu nhưng có `from_week` / `to_week` thì suy ra qua `baoGiangSchoolWeekRange`.
    + Nếu đợt để trống cả `date_start` và `from_week` nhưng có `weeks_count > 0`: tự động nối tiếp tuần tuần tự bắt đầu từ Tuần 1 (hoặc sau tuần kết thúc của đợt liền trước trong cùng năm học) để các đợt khai báo kiểu "Đợt 1: 11 tuần, Đợt 2: 7 tuần" luôn có khoảng ngày hiệu lực chính xác.
    + Nếu `from` có mà `to` trống: lấy ngày liền trước `from` của đợt kế tiếp có `from > current.from`, hoặc `'9999-12-31'`.
- Cải tiến `phaseTimetableForDate(teacher, iso)` và tách hàm `resolvePhaseTimetableInfoForDate(teacher, iso)`:
  - Lọc tất cả các đợt có `from <= iso && iso <= to` mà giáo viên có TKB khác rỗng; nếu có nhiều đợt chồng lấn khoảng ngày, **chọn đợt có `from` lớn nhất (mới nhất nhưng `<= iso`), nếu trùng `from` thì chọn đợt đứng sau (tạo muộn hơn)** thay vì lấy đợt đầu tiên `index = 0`.
  - Trả về `{ timetable, phase, from, to, startWeek }` (hàm `phaseTimetableForDate(teacher, iso)` giữ nguyên chữ ký trả về `timetable | null`).
- Viết hàm `resolveTeacherTimetableForDate(teacher, dateValue, overrideSource = '')`:
  - Hỗ trợ `overrideSource` tùy chọn (ví dụ `'W11'`, `'phase:phase_hk1_d1'`, `'current'`) khi người dùng chủ động chọn nguồn trên giao diện.
  - Khi tra tự động theo `dateValue` (`iso`, `weekKey = timetableWeekKeyForDate(iso)`, `weekNum`):
    1. **Ưu tiên 1 (Lưu riêng đúng tuần):** Nếu `weekKey` tồn tại và `weeklyTimetableSaved(weekKey, teacher.id)` có dữ liệu -> trả về `{ timetable, sourceType: 'week_exact', weekKey, label: 'CSDL TKB Tuần ' + weekNum }`.
    2. **Tìm thông tin Đợt chứa ngày `iso`:** `phaseInfo = resolvePhaseTimetableInfoForDate(teacher, iso)` (có `phaseStartWeek`).
    3. **Ưu tiên 2 (Kế thừa tuần gần nhất trước đó trong phạm vi hợp lệ):** Duyệt lùi `w = weekNum - 1` về `Math.max(1, phaseInfo?.startWeek || 1)`: nếu `weeklyTimetableSaved('W' + w, teacher.id)` -> trả về `{ timetable, sourceType: 'week_inherited', weekKey: 'W' + w, targetWeekKey: weekKey, label: 'Kế thừa TKB Tuần ' + w }`.
    4. **Ưu tiên 3 (TKB của Đợt phân công chứa ngày đó):** Nếu `phaseInfo?.timetable` tồn tại -> trả về `{ timetable: phaseInfo.timetable, sourceType: 'phase', phaseId: phaseInfo.phase.id, phaseName: phaseInfo.phase.name, label: 'TKB ' + phaseInfo.phase.name }`.
    5. **Ưu tiên 4 (Kế thừa tuần cũ hơn trước Đợt nếu Đợt chưa có TKB riêng):** Duyệt lùi phần còn lại về `W1`.
    6. **Ưu tiên 5 (Fallback cuối cùng về `teacher.timetable` hiện hành):** Kiểm tra xem có bất kỳ bản lưu tuần nào ở tương lai (`w > weekNum`, ví dụ đang tra `W11` mà chỉ có `W12` đã lưu hoặc `teacher.timetable.updated_at > weekEndDate`) hay không; trả về `{ timetable: normalizeTeacherTimetable(teacher?.timetable), sourceType: 'fallback_current', isFallbackFromNewer: Boolean(...), label: 'TKB hiện hành (chưa có bản lưu riêng cho ' + (weekKey ? 'Tuần ' + weekNum : 'ngày này') + ')' }`.
  - Hàm `getTeacherTimetableForDate(teacher, dateValue)` gọi `resolveTeacherTimetableForDate(teacher, dateValue).timetable` để giữ nguyên 100% chữ ký trả về `timetable`.
- Cải tiến `openQuickNewPhaseModal()` và `submitQuickNewPhase()`:
  - Trong `openQuickNewPhaseModal()`: tự tính tuần hiện tại `curWeek` từ hôm nay; điền gợi ý `qp-from-week = curWeek`, và đặt `qp-date-start` là **Thứ Hai đầu tuần hiện tại** (`baoGiangSchoolWeekRange(curWeek)?.start`) thay vì ngày lẻ giữa tuần.
  - Trong `submitQuickNewPhase()`: trước khi push đợt mới có `date_start`, nếu đợt liền trước chưa có `date_end` hoặc có `date_end >= date_start` (và `phase.date_start < date_start`), tự động cắt `phase.date_end` của đợt trước thành ngày liền trước `date_start` để hai đợt nối tiếp sạch sẽ, không chồng lấn.

### Bước 3: Nâng cấp toàn diện luồng lưu/chọn TKB theo Tuần ở Tab `2. Thời khoá biểu GV` (`phancongtochuyenmon.html`)
- **Hiển thị nổi bật bộ chọn Tuần ngay trên `#tt-workspace-header`:**
  - Trong `renderTimetableWorkspace()`, bổ sung thanh điều khiển tuần cố định, trực quan ngay trên đầu bảng TKB (đồng bộ 2 chiều với `#tt-apply-week`):
    + Dropdown chọn `Tuần 1` .. `Tuần 35` (kèm khoảng ngày `dd/mm – dd/mm` và dấu `✓ Đã lưu CSDL riêng`) + tùy chọn `Theo Đợt hiện tại (áp dụng chung cả đợt)`.
    + Badge trạng thái rõ ràng cho giáo viên đang chọn: `✓ Đã lưu CSDL riêng cho Tuần X`, `↪ Đang kế thừa từ Tuần Y / Đợt Z`, hoặc `⚠️ Đang sửa tuần quá khứ (không ảnh hưởng TKB Tuần hiện tại)`.
    + Nút nhanh `Sao chép TKB tuần khác sang tuần này` (cho phép copy TKB của cả tổ hoặc GV đang chọn từ một tuần/đợt/kế hoạch CSDL khác sang tuần đang chọn).
- **Mặc định chọn Tuần học hiện tại khi mở Tab TKB:**
  - Trong `renderTimetableView()`, nếu `selectedTimetableWeekKey` đang rỗng lần đầu mở trong phiên (`!timetableWeekInitialized`), tự động khởi tạo `selectedTimetableWeekKey = timetableWeekKeyForDate(baoGiangIso(new Date())) || ''` (ví dụ hôm nay ở Tuần 12 sẽ mặc định chọn sẵn `W12`), giúp người dùng dán ảnh / nạp Word / sửa ô ở Tuần 12 tự động lưu vào `W12` và bảo toàn `W11`! (Vẫn cho phép người dùng chủ động chọn về `""` nếu muốn sửa gốc của cả Đợt).
- **Sửa triệt để `snapshotPreviousWeekBeforeOverride` và `saveTimetableForTeacherWeek`:**
  - Trong `snapshotPreviousWeekBeforeOverride(teacherId, targetWeekNum)`:
    + Lấy TKB đang có hiệu lực thực tế ở tuần liền trước `prevWeek = targetWeekNum - 1` (trước khi ghi TKB mới) qua `prevRange ? getTeacherTimetableForDate(teacher, prevRange.start) : teacher?.timetable`.
    + Nếu `!weeklyTimetableSaved('W' + prevWeek, teacherId)` và bản TKB trước đó có tiết học (`timetableHasLessons(prevTt)`), lưu bản chụp đó vào **`state.weekly_timetables['W' + prevWeek][String(teacherId)]`** (và nếu từ `W1..W(prevWeek)` chưa có tuần nào được lưu thì lưu thêm mốc gốc `W1` để các tuần `1..prevWeek` đều có lịch!). Nhờ đó dù trước đó `W1` hay `W5` đã có dữ liệu hay chưa, `W11` luôn giữ đúng TKB của Tuần 11 trước khi sang `W12`!
  - Trong `saveTimetableForTeacherWeek(teacherId, timetable, weekKey = selectedTimetableWeekKey)`:
    + Lưu `state.info.active_timetable_week = weekKey || timetableWeekKeyForDate(baoGiangIso(new Date())) || ''` để backend biết mốc tuần hiện hành.
    + Khi `weekKey === ''` (người dùng chủ động chọn `"Theo Đợt hiện tại"`): nếu `currentWeek > 1` và `teacher.timetable` cũ có tiết học khác với `timetable` mới, đồng thời `teacher.timetable.updated_at` thuộc một tuần `< currentWeek` mà tuần đó chưa lưu riêng, tự động snapshot bản cũ vào tuần cũ trước khi `persistTeacherTimetable`; nếu tuần hiện tại `W<currentWeek>` đã có bản lưu riêng trong `weekly_timetables` thì đồng bộ cập nhật luôn `W<currentWeek>` để không bị tuần cũ che khuất.
    + Khi `weekKey` là một tuần quá khứ (`currentWeek && week < currentWeek`, ví dụ đang ở Tuần 12 quay lại chọn `W11` để nhập TKB Tuần 11):
      * Tự động chốt bản TKB hiện hành của giáo viên vào `W<currentWeek>` (`W12`) nếu `W12` chưa lưu riêng (bảo vệ tuyệt đối TKB Tuần 12!).
      * Ghi TKB mới vào `state.weekly_timetables['W11'][String(teacherId)]`.
      * **Không** gọi `persistTeacherTimetable` đè lên `teacher.timetable` của Tuần 12.
- **Bật Auto-save CSDL & cô lập đồng bộ phân công khi nạp tuần quá khứ:**
  - Trong `persistAndSaveTimetableLocal()` và `saveTimetableForSelectedWeek()`: đổi `saveToLocal({ autoSave: false })` thành `saveToLocal()` để tự động lưu lên CSDL MySQL (`performSaveToDB`).
  - Trong `applyWordTimetableDirectly()`, `importTimetableFromJson()`, `applyAiTimetableResult()` và `finishTimetableDragSave()`:
    + Kiểm tra `isEditingPastWeek = Boolean(selectedTimetableWeekKey && currentWeek && Number(selectedTimetableWeekKey.slice(1)) < currentWeek)`.
    + Chỉ tự động gọi `applyTimetableToAssignments(...)` khi `!isEditingPastWeek` (nếu đang nhập bổ sung TKB quá khứ `W11` phục vụ Sổ Dạy Thay thì giữ nguyên phân công chuyên môn hiện hành của `W12`, thông báo toast rõ: `Đã lưu TKB riêng cho Tuần 11 lên CSDL (giữ nguyên TKB & phân công hiện hành của Tuần 12)`).
  - Trong `filteredTimetableTeachers()`, `renderTimetableTeacherList()`, `selectAllTimetableTeachers()`, `goToNextTimetableTeacher()`:
    + Đánh giá `const effectiveTt = getTeacherTimetableForWeekKey(t, selectedTimetableWeekKey);` thay cho `t.timetable` để danh sách giáo viên bên trái phản ánh chính xác số tiết và trạng thái TKB của đúng tuần đang chọn (`W11` vs `W12`).

### Bước 4: Sửa dứt điểm Sổ Dạy Thay - Bù (`#view-daythay`) và kết nối nguồn CSDL tuần
- Bổ sung biến trạng thái nhẹ `daythayTimetableSourceOverride = ''` (mặc định `''` = Tự động tra chuẩn theo `Ngày dạy`; cho phép người dùng chọn ghi đè tạm nguồn TKB tuần `W1..W35` hoặc Đợt nếu muốn ép lấy lịch từ một tuần/đợt cụ thể). Reset về `''` mỗi khi người dùng đổi `#new-sub-date` sang tuần khác hoặc bấm `Làm mới`.
- Cập nhật `getTimetableDaySlots(teacher, session, dayNum, dateValue = '')`:
  - Sử dụng `resolveTeacherTimetableForDate(teacher, dateValue, daythayTimetableSourceOverride)` (với kiểm tra `typeof` an toàn cho unit test).
- Sửa lỗi kẹt tiết cũ trong `onDayThayAbsentContextChange()` và `renderAbsentTeacherSchedulePreview()`:
  - Trong `onDayThayAbsentContextChange()`: khi cặp `(date, teacherId)` thay đổi và `!editingSubId`, reset `extraPeriodSlots = []`, `hiddenPeriodSlots = new Set()`.
  - Trong `renderAbsentTeacherSchedulePreview()`:
    + Khi `!editingSubId && daythaySessionAuto.scope === scope && !daythaySessionAuto.manual && !daythaySessionAuto.applied`:
      * Nếu `autoSession` có tiết (`'morning'`, `'afternoon'`, `'all_day'`): cập nhật `sessionEl.value = autoSession`, đánh dấu `daythaySessionAuto.applied = true`, và **luôn gọi `onDayThaySessionChange({ auto: true })`** (kể cả khi `sessionEl.value` trước đó đã trùng `autoSession`, để bắt buộc nạp lại `#period-slots-builder` theo đúng tiết/lớp của ngày mới ở Tuần 11 thay vì giữ tiết của Tuần 12!).
      * Nếu `!autoSession` (ngày đó ở Tuần 11 giáo viên nghỉ không có tiết nào): đánh dấu `daythaySessionAuto.applied = true` và gọi `initPeriodSlotsBuilder([])` để **xóa sạch các tiết cũ của Tuần 12** khỏi `#period-slots-builder`!
- Minh bạch hóa nguồn CSDL TKB ngay trên khung `#daythay-absent-schedule-preview` và cạnh ô `Ngày dạy`:
  - Hiển thị nhãn tuần ngay dưới `#new-sub-date` (`#new-sub-weekday`): ví dụ `Thứ Tư · Tuần 11 (16/11 – 22/11/2026)`.
  - Trên đầu khung `#daythay-absent-schedule-preview`, hiển thị rõ **Badge Nguồn CSDL TKB**:
    + Nếu `sourceType === 'week_exact'`: badge xanh lá `✓ Đang lấy CSDL: TKB Tuần 11 (đã lưu riêng)`.
    + Nếu `sourceType === 'week_inherited'` hoặc `'phase'`: badge xanh lam `ℹ️ Đang lấy CSDL: ${sourceInfo.label}`.
    + Nếu `sourceType === 'fallback_current'` (đặc biệt khi `isFallbackFromNewer` là `true`, tức ngày chọn ở Tuần 11 nhưng CSDL chưa có bản lưu Tuần 11 mà đang có bản mới hơn ở Tuần 12): hiển thị hộp cảnh báo màu cam nổi bật:
      `⚠️ CSDL chưa có bản TKB lưu riêng cho Tuần 11 (đang hiển thị tạm theo TKB hiện hành). Nếu Tuần 11 có TKB khác Tuần 12, hãy bấm "Nhập / Khôi phục TKB Tuần 11" bên dưới để nạp đúng TKB Tuần 11 lên CSDL.`
  - Ngay trong thanh công cụ nhỏ của khung lịch xem trước, cung cấp:
    + Dropdown nhỏ `Nguồn TKB: [ Tự động theo ngày (Tuần 11) ▾ ]` liệt kê các bản TKB tuần đã lưu trong CSDL (`state.weekly_timetables`) và các Đợt (`state.phases`) để người dùng có thể đổi/đối chiếu tức thì.
    + Nút **`Nhập / Sửa TKB Tuần X`** gọi `openTeacherTimetableForDate(teacher.id, date)`: chuyển sang Tab `2. Thời khoá biểu GV`, tự động gán `selectedTimetableWeekKey = 'W11'` và chọn đúng giáo viên đó để nạp file Word/ảnh TKB của Tuần 11 chỉ trong 1 bước.
- Cập nhật nút `TKB Giáo viên` trên thanh công cụ Sổ Dạy Thay (`openTeacherTimetableModal(teacherId)`):
  - Nếu đang mở từ Sổ Dạy Thay và `#new-sub-date` có ngày hợp lệ, tự động đồng bộ `selectedTimetableWeekKey = timetableWeekKeyForDate(newSubDate)` trước khi chuyển sang `view-timetable` để luôn mở đúng TKB của tuần tương ứng với ngày dạy thay đang chọn!
- Đồng bộ nốt `baoGiangTeacherHasTimetable(teacher)`, `buildSelectedTeachersTimetableEmail`, và `buildTeacherIndividualTimetableEmail` (phần plain text và kiểm tra có tiết) dùng `getTeacherTimetableForDate` khi có `weekRange`.

### Bước 5: Bổ sung kiểm thử tự động toàn diện (`tests/daythay-suggest-smoke.js`, `tests/timetable-render-smoke.js`)
- Trong `tests/daythay-suggest-smoke.js`:
  - Kiểm chứng kịch bản thực tế End-to-End: Người dùng mở Sổ Dạy Thay ở Tuần 12 (`2026-11-26`, lưới tiết đã nạp tiết của Tuần 12), sau đó đổi `#new-sub-date` về ngày thuộc Tuần 11 (`2026-11-16` hoặc ngày không có tiết ở Tuần 11):
    1. Cùng buổi Sáng nhưng khác tiết/lớp giữa Tuần 12 và Tuần 11 -> `#period-slots-builder`, `#daythay-absent-schedule-preview` và `computeDayThayTeacherAvailability` đều tự động nạp lại đúng tiết/lớp và GV rảnh của **Tuần 11**, không còn sót tiết của Tuần 12.
    2. Ngày ở Tuần 11 GV nghỉ không có tiết -> `#period-slots-builder` tự xóa sạch tiết đã tick của Tuần 12.
    3. Khung preview hiển thị đúng nguồn CSDL (`TKB Tuần 11` khi đã lưu `W11`, hoặc cảnh báo rõ khi fallback).
- Trong `tests/timetable-render-smoke.js`:
  - Kiểm chứng `snapshotPreviousWeekBeforeOverride` khi đã có `W1` (TKB đầu năm), `W5` (TKB giữa kỳ), sang `W12` nạp TKB mới -> `W11` được chụp lại chính xác, không bị bỏ sót bởi `hasEarlier`.
  - Kiểm chứng khi mở Tab TKB ở Tuần 12 mặc định chọn `W12`, nạp TKB mới không làm mất `W11`; và khi đang ở Tuần 12 chọn `W11` nạp bù TKB Word/AI cho Tuần 11 thì `W12` và phân công lớp của `W12` được giữ nguyên 100%, đồng thời danh sách GV bên trái hiển thị đúng số tiết của tuần đang chọn (`W11` vs `W12`).
  - Kiểm chứng cú pháp PHP (`php -l api/phancong.php` nếu môi trường có PHP) và cú pháp toàn bộ inline `<script>` trong `phancongtochuyenmon.html`, chạy lại các bài smoke test liên quan (`baogiang-teacher-month-smoke.js`, `attendance-autosync-smoke.js`) đảm bảo không hồi quy.

## Rủi ro

1. **Rủi ro dữ liệu của người dùng đã bị ghi đè mất TKB Tuần 11 trước thời điểm cập nhật bản vá:** Nếu trên CSDL hiện tại chỉ còn duy nhất TKB Tuần 12 (do lần lưu trước đã ghi đè `data_json`), không hệ thống nào tự đoán lại được tiết cũ nếu chưa từng lưu. -> **Giảm thiểu:** Hiển thị cảnh báo minh bạch ngay trên Sổ Dạy Thay khi chọn ngày Tuần 11 kèm nút 1 chạm **`Nhập / Sửa TKB Tuần 11`** (hỗ trợ nạp lại file Word `.docx` toàn tổ cho riêng `Tuần 11` trong vài giây mà không ảnh hưởng gì đến `Tuần 12`); từ bản vá này trở đi, cả frontend lẫn `api/phancong.php` đều tự động snapshot lịch sử tuần vào bảng `phancong_weekly_timetables` trước mọi thao tác ghi đè.
2. **Rủi ro tương thích với cách cắt hàm `declaration(name)` trong bộ smoke test Node `vm`:** Các test cũ cắt chuỗi hàm theo `\n        function ` và truyền context tối giản. -> **Giảm thiểu:** Tuân thủ nghiêm quy tắc thụt lề 8 dấu cách cho hàm top-level, không đặt biến `let`/`const` xen giữa các hàm, và dùng `typeof ... === 'function'` cho mọi lời gọi chéo mới trong các hàm được test đơn lẻ.
3. **Rủi ro quyền ALTER/CREATE TABLE trên MySQL hosting:** Một số shared hosting giới hạn quyền DDL lặp lại. -> **Giảm thiểu:** Đặt `CREATE TABLE IF NOT EXISTS phancong_weekly_timetables` trong `phancong_ensure_schema` được bọc bởi `schema_is_ready('phancong_chuyenmon', PHANCONG_SCHEMA_VERSION)` và `try/catch` an toàn giống hệt cơ chế hiện hành của `phancong_chuyenmon`.

## Cách kiểm thử

1. Chạy kiểm thử tự động Sổ Dạy Thay & TKB theo tuần:
   - `node tests/daythay-suggest-smoke.js`
   - `node tests/timetable-render-smoke.js`
2. Chạy kiểm thử hồi quy các phân hệ liên quan trong Quản lý Tổ Chuyên Môn:
   - `node tests/baogiang-teacher-month-smoke.js`
   - `node tests/baogiang-weekday-segment-smoke.js`
   - `node tests/attendance-autosync-smoke.js`
3. Kiểm tra cú pháp `api/phancong.php` (bằng `php -l api/phancong.php` nếu có PHP CLI, hoặc kiểm tra cấu trúc PHP) và toàn bộ thẻ `<script>` trong `phancongtochuyenmon.html`.

## Tiêu chí nghiệm thu

1. **CSDL lưu trữ độc lập TKB theo tuần:** Bảng `phancong_weekly_timetables` trong `api/phancong.php` tự động lưu và hợp nhất TKB từng tuần (`W1..W35`), tự động archive TKB tuần cũ trên server trước khi ghi đè `phancong_chuyenmon`, và mọi thao tác lưu/sửa TKB ở giao diện đều tự động đẩy lên CSDL (`autoSave` hoạt động đầy đủ).
2. **Không bao giờ mất TKB tuần trước khi sang tuần mới:** Mở Tab `2. Thời khoá biểu GV` hiển thị ngay thanh chọn **Tuần áp dụng TKB** (mặc định là tuần hiện hành, ví dụ `Tuần 12`). Khi nạp/sửa TKB cho `Tuần 12`, TKB của `Tuần 11` (dù trước đó đã có `W1`, `W5` hay chưa) vẫn được bảo toàn nguyên vẹn.
3. **Quay lại nhập Dạy thay ở Tuần 11 lấy đúng CSDL Tuần 11:** Tại thời điểm Tuần 12, vào `5. Sổ Dạy Thay - Bù` chọn bất kỳ ngày nào thuộc Tuần 11:
   - Khung xem trước lịch dạy của GV nghỉ, lưới tiết `#period-slots-builder` (kể cả khi cùng buổi với Tuần 12 hoặc khi ngày ở Tuần 11 không có tiết), danh sách đề xuất GV dạy thay và điều kiện lưu bản ghi đều phản ánh **100% TKB của Tuần 11**, tuyệt đối không còn hiển thị hay kẹt lại tiết của Tuần 12.
   - Hiển thị rõ nguồn CSDL đang áp dụng (`TKB Tuần 11`, kế thừa tuần/đợt, hoặc cảnh báo kèm nút 1 chạm `Nhập / Sửa TKB Tuần 11` nếu Tuần 11 chưa có dữ liệu riêng).
   - Khi chuyển ngày sang Tuần 12, lập tức hiển thị đúng TKB của Tuần 12.
4. **Hỗ trợ nạp bù TKB tuần quá khứ an toàn tuyệt đối:** Đang ở Tuần 12 có thể chọn `Tuần 11` (từ Tab TKB hoặc bấm từ Sổ Dạy Thay) để nạp lại TKB của Tuần 11 (Word/AI/JSON/chỉnh ô) và lưu lên CSDL mà không làm mất TKB `Tuần 12` cũng như không làm xáo trộn bảng phân công lớp của `Tuần 12`.
5. Toàn bộ các bài smoke test nêu trong mục Cách kiểm thử chạy **PASS 100%**.
