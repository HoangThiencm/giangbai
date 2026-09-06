# PLAN: Bổ sung Nhiệm vụ Kiêm nhiệm Trường (Không dạy lớp, tính tiết trực tiếp cho GV)

## Hiện trạng & Nhu cầu người dùng
1. **Hiện trạng phân loại nhiệm vụ trong `phancongtochuyenmon.html`**:
   - Hiện tại trong modal "Khai báo & Cài đặt Tổ Chuyên Môn" -> Tab "4. Môn học", cột "Loại nhiệm vụ" chỉ có 2 lựa chọn:
     + `Môn chính (Toàn trường)` (`is_core = true`)
     + `Kiêm nhiệm (Chỉ vài lớp)` (`is_core = false`)
   - Cả 2 loại này đều được hệ thống coi là **môn dạy theo lớp**, tự động sinh toàn bộ danh sách lớp học (`state.classes`, ví dụ 25 lớp) vào Kho lớp bên trái (`#pool-container`) để người dùng kéo thả vào giáo viên.
   - Bảng Ma trận theo Lớp học (`#matrix-classes-table`) cũng tạo cột cho môn đó và kiểm tra tình trạng lớp.

2. **Nhu cầu thực tế cấp thiết**:
   - Trong trường học, có 2 hình thức kiêm nhiệm:
     + **Kiêm nhiệm theo lớp**: Chủ nhiệm (GVCN), Hoạt động trải nghiệm (HĐTN)... $\rightarrow$ gắn với từng lớp cụ thể.
     + **Kiêm nhiệm công tác nhà trường / phong trào**: Chuyển đổi số (CĐS), Quản trị website/hệ thống, Phụ trách phòng máy / thiết bị / thí nghiệm, Thư ký hội đồng, Trưởng ban TTND, Công tác Đoàn/Đội, Ban thanh tra... $\rightarrow$ **Không dạy ở lớp nào cả nhưng vẫn được quy đổi số tiết/tuần** (ví dụ CĐS tính 3 tiết/tuần).
   - Khi người dùng khai báo "CĐS (3 tiết)", hiện tại hệ thống sinh ra 25 lớp CĐS trong kho lớp đòi kéo thả, và trên ma trận lớp cũng hiện cột CĐS cho từng lớp, gây sai lệch bản chất và bất tiện khi thao tác.
   - Người dùng cần: Bổ sung loại nhiệm vụ **"Kiêm nhiệm trường (Không dạy lớp, tính tiết)"**, gán trực tiếp cho giáo viên, không sinh kho lớp, không đưa vào ma trận lớp, và tự động tính số tiết vào tổng tải/kiêm nhiệm của giáo viên.

---

## Mục tiêu kỹ thuật

### 1. Chuẩn hóa 3 loại nhiệm vụ trong `state.subjects` (`duty_type`)
Mỗi môn/nhiệm vụ trong `state.subjects` có thuộc tính:
- `duty_type`:
  + `'core'`: **Môn chính (Toàn trường)** (mặc định cho Toán, Văn, KHTN...). Phải phân công đủ mọi lớp.
  + `'class_duty'`: **Kiêm nhiệm theo lớp (Chỉ vài lớp)** (GVCN, HĐTN...). Kéo thả theo từng lớp.
  + `'school_duty'`: **Kiêm nhiệm trường / Công tác (Không dạy lớp, tính tiết/GV)** (CĐS, Thiết bị, Thư ký HĐ...). Gán trực tiếp cho GV.
- **Tương thích ngược dữ liệu**:
  ```javascript
  function getSubjectDutyType(sub) {
      if (sub.duty_type) return sub.duty_type;
      return (sub.is_core !== false) ? 'core' : 'class_duty';
  }
  ```
  Khi lưu và chuẩn hóa:
  - Nếu `duty_type === 'school_duty'` $\rightarrow$ `is_core = false`.
  - Nếu `duty_type === 'core'` $\rightarrow$ `is_core = true`.
  - Nếu `duty_type === 'class_duty'` $\rightarrow$ `is_core = false`.

### 2. Giao diện Cấu hình Tab "4. Môn học & Nhiệm vụ" (`#config-modal`)
- Cột "Loại nhiệm vụ" hiển thị dropdown 3 lựa chọn:
  1. `<option value="core">Môn chính (Toàn trường)</option>`
  2. `<option value="class_duty">Kiêm nhiệm theo lớp (Chỉ vài lớp)</option>`
  3. `<option value="school_duty">Kiêm nhiệm trường (Không dạy lớp, tính tiết)</option>`
- Đổi tiêu đề cột "Số tiết/lớp/tuần" thành: **"Số tiết / tuần"** (kèm chú thích: *"Theo lớp: tiết/lớp; Kiêm nhiệm trường: tiết/GV"*).
- Bổ sung nút preset / mẫu nhiệm vụ nhanh:
  + Mẫu Toán - Tin: Toán (4t), Tin học (1t), Chủ nhiệm (4t), HĐTN (3t), CĐS (3t - Kiêm nhiệm trường).

### 3. Điều chỉnh Kho Lớp bên trái (`#pool-container`)
- Đối với nhiệm vụ `duty_type === 'school_duty'`:
  + **KHÔNG** sinh mảng 25 lớp vào `state.unassigned[sub.key]`.
  + Thay vào đó, tạo một khối riêng phía dưới kho lớp hoặc nhóm nhiệm vụ:
    **"Nhiệm vụ kiêm nhiệm trường"**:
    Hiển thị các thẻ chip nhiệm vụ, ví dụ:
    `<div class="school-duty-chip" draggable="true" ondragstart="dragStartSchoolDuty(event, '${sub.key}')">`
    Kèm badge trạng thái: *"Đã gán: Thầy Danh"* hoặc *"Chưa phân công"*.
    Có thể kéo thả vào Thẻ Giáo viên HOẶC bấm trực tiếp để chọn/gán GV nhanh!

### 4. Giao diện Thẻ Giáo viên (`renderTeachers`)
- Trên mỗi Thẻ Giáo viên (`.teacher-card`):
  + Hỗ trợ thả nhiệm vụ kiêm nhiệm trường (hàm `dropSchoolDuty(subKey, teacherId)`).
  + Thêm khu vực hiển thị các nhiệm vụ kiêm nhiệm trường đã gán:
    Mỗi nhiệm vụ hiển thị dưới dạng badge/tag nổi bật:
    `<span class="school-duty-badge" style="background:${sub.color}15; color:${sub.color}; border: 1px solid ${sub.color};">
       ⚙️ ${sub.name} (+${sub.periods}t)
       <i class="fas fa-times" onclick="unassignSchoolDuty('${sub.key}', '${t.id}')" title="Hủy kiêm nhiệm"></i>
     </span>`
  + Thêm nút bấm nhỏ `+ Kiêm nhiệm` để mở menu popup/dropdown chọn nhanh nhiệm vụ kiêm nhiệm trường gán cho GV đó mà không cần kéo thả.

### 5. Cấu trúc lưu trữ và Phép tính Định mức / Tải giảng dạy
1. **Lưu trữ trên đối tượng Giáo viên**:
   - Thêm thuộc tính `t.school_duties = ['CDS', ...]` (danh sách các `sub.key` kiêm nhiệm trường).
   - Hàm `normalizeState` đảm bảo mọi giáo viên đều có `t.school_duties = Array.isArray(t.school_duties) ? t.school_duties : []`.
   - Đồng bộ vào snapshot đợt (`state.phase_assignments[phaseId].teachers` và `persistTeacherTimetable`).
2. **Tính toán số tiết**:
   - Viết hàm `calcSchoolDutiesPeriods(t)`:
     ```javascript
     function calcSchoolDutiesPeriods(t) {
         if (!Array.isArray(t.school_duties)) return 0;
         return t.school_duties.reduce((sum, key) => {
             const s = state.subjects.find(sub => sub.key === key);
             return sum + ((s && getSubjectDutyType(s) === 'school_duty') ? (s.periods || 0) : 0);
         }, 0);
     }
     ```
   - Cập nhật `calcTeacherTotalPeriods(t)`:
     ```javascript
     function calcTeacherTotalPeriods(t) {
         const teaching = calcTeachingPeriods(t);
         const qlpmPeriods = t.qlpm ? PERIOD_QLPM : 0;
         const schoolDutyPeriods = calcSchoolDutiesPeriods(t);
         return teaching + (t.allowance || 0) + qlpmPeriods + schoolDutyPeriods;
     }
     ```
   - Cập nhật dòng hiển thị footer thẻ GV:
     `Dạy: ${teaching}t · Giảm trừ/kiêm nhiệm: ${(t.allowance || 0) + qlpmPeriods + schoolDutyPeriods}t`
   - Cập nhật bảng tổng hợp Ma trận giáo viên (`#matrix-teachers-table`) và Báo cáo (`#rep-teachers-table`):
     Trong cột "Giảm trừ / kiêm nhiệm", liệt kê rõ:
     `TTCM (3t) + CĐS (3t) + QL Máy (3t)` $\rightarrow$ Cực kỳ rõ ràng, minh bạch!

### 6. Điều chỉnh Bảng Ma trận Lớp học (`#matrix-classes-table`)
- Bảng Ma trận Lớp học (`matrix-classes-table`) chỉ lặp qua các môn học có `duty_type !== 'school_duty'` (tức là chỉ gồm môn chính và kiêm nhiệm theo lớp).
- Tuyệt đối không sinh cột lớp cho các nhiệm vụ kiêm nhiệm trường.

---

## File tác động
- `phancongtochuyenmon.html` [SỬA: Tab 4 Môn học & Nhiệm vụ, duty_type, school_duty chip/drag-drop/quick-assign, tính toán định mức, ma trận lớp và báo cáo]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch này]
- `docs/handoff/.lock` [TẠO: LOCK]

---

## Chi tiết các bước thực hiện cho Coder

### Bước 1: Khai báo và Chuẩn hóa `duty_type` & `school_duties`
1. Trong `normalizeState(s)`:
   - Chuẩn hóa `sub.duty_type`:
     + Nếu `sub.duty_type` chưa có: nếu `sub.is_core === false` thì `'class_duty'`, ngược lại `'core'`.
     + Đảm bảo `sub.is_core = (sub.duty_type === 'core')`.
   - Với `sub.duty_type === 'school_duty'`:
     + Không khởi tạo `s.unassigned[sub.key] = [...s.classes]`. Nếu có lớp cũ trong `s.unassigned[sub.key]` thì dọn dẹp thành `[]`.
   - Với mỗi giáo viên trong `s.teachers`:
     + Khởi tạo `t.school_duties = Array.isArray(t.school_duties) ? t.school_duties : []`.
2. Viết các helper:
   - `getSubjectDutyType(sub)`: Trả về `'core' | 'class_duty' | 'school_duty'`.
   - `calcSchoolDutiesPeriods(t)`: Tính tổng tiết kiêm nhiệm trường của giáo viên.
   - Cập nhật `calcTeacherTotalPeriods(t)` tính thêm `calcSchoolDutiesPeriods(t)`.

### Bước 2: Nâng cấp Tab 4 Môn học & Nhiệm vụ trong Modal Cấu hình
1. Trong `renderConfigSubjectsTable()`:
   - Cột "Loại nhiệm vụ" đổi thành dropdown 3 giá trị:
     ```html
     <select class="form-control" style="padding:4px 8px; font-weight:700;" onchange="updateEditingSubjectDutyType(${index}, this.value)">
         <option value="core" ${dtype === 'core' ? 'selected' : ''}>Môn chính (Toàn trường)</option>
         <option value="class_duty" ${dtype === 'class_duty' ? 'selected' : ''}>Kiêm nhiệm theo lớp (Chỉ vài lớp)</option>
         <option value="school_duty" ${dtype === 'school_duty' ? 'selected' : ''}>Kiêm nhiệm trường (Không dạy lớp, tính tiết)</option>
     </select>
     ```
   - Tiêu đề cột số tiết đổi thành: `"Số tiết/tuần"`.
2. Hàm `updateEditingSubjectDutyType(index, value)`:
   - Cập nhật `sub.duty_type = value`.
   - Cập nhật `sub.is_core = (value === 'core')`.
3. Cập nhật các preset môn học:
   - Mẫu Toán - Tin: thêm môn `key: 'cds', name: 'Chuyển đổi số', periods: 3, color: '#0891b2', duty_type: 'school_duty', is_core: false`.

### Bước 3: Cập nhật Kho Lớp & Khối Nhiệm vụ Kiêm nhiệm Trường
1. Trong `renderPool()`:
   - Các môn `core` và `class_duty` giữ nguyên cách hiển thị lớp học.
   - Các môn `school_duty`: Hiển thị trong một section riêng biệt `"Nhiệm vụ Kiêm nhiệm Trường / Hoạt động"`:
     + Hiển thị từng nhiệm vụ kèm số tiết và danh sách giáo viên đang đảm nhiệm.
     + Có nút `+ Gán GV` để gán nhanh cho một giáo viên từ dropdown.
     + Hỗ trợ kéo thả chip nhiệm vụ vào thẻ card của giáo viên.

### Bước 4: Cập nhật Thẻ Card Giáo viên (`renderTeachers`)
1. Trong hàm `renderTeachers()`:
   - Thêm khu vực hiển thị danh sách nhiệm vụ kiêm nhiệm trường đã gán cho giáo viên:
     `<div class="teacher-school-duties">...</div>`
   - Bấm vào icon `✕` trên tag để hủy nhiệm vụ (`unassignSchoolDuty(dutyKey, teacherId)`).
   - Thêm nút dropdown `+ Kiêm nhiệm` để chọn nhanh một nhiệm vụ kiêm nhiệm trường gán cho giáo viên.
   - Cập nhật footer: hiển thị rõ tổng tiết kiêm nhiệm trường trong phần `Giảm trừ/kiêm nhiệm`.

### Bước 5: Cập nhật Ma trận Lớp học & Báo cáo Tổng hợp
1. Trong `matrix-classes-table`:
   - Chỉ lọc và vẽ cột cho các môn có `getSubjectDutyType(sub) !== 'school_duty'`.
2. Trong `matrix-teachers-table` và `rep-teachers-table`:
   - Cột "Giảm trừ / kiêm nhiệm" liệt kê chi tiết cả các nhiệm vụ kiêm nhiệm trường:
     Ví dụ: `TTCM (3t) + CĐS (3t)`.
   - Cột "Tổng" và "Định mức chuẩn" tự động phản ánh chính xác số tiết.
3. Trong xuất Excel:
   - Xuất đầy đủ tên các nhiệm vụ kiêm nhiệm trường vào cột Kiêm nhiệm.

### Bước 6: Đồng bộ Snapshot Đợt & Lưu CSDL
1. Cập nhật `saveCurrentPhaseSnapshot()` và `switchPhase()`:
   - Đảm bảo `school_duties` của từng giáo viên được lưu trữ và khôi phục đồng bộ theo từng đợt phân công.

---

## PHẦN 2: TỰ ĐỘNG DỊCH NGƯỢC TỪ THỜI KHÓA BIỂU SANG PHÂN CÔNG CHUYÊN MÔN

### 1. Nhu cầu nghiệp vụ
- Nhiều giáo viên hoặc tổ chuyên môn đã có Thời khóa biểu (qua dán ảnh AI Gemini Vision nhận diện hoặc nhập tay vào ma trận TKB).
- Trong TKB đã có đầy đủ: Thứ, Buổi, Tiết, Môn học, Lớp học (VD: `Toán - 63`, `Toán - 64`, `Toán - 93`, `Toán - 94`, `HĐTN - 64`).
- Thay vì phải kéo thả từng lớp thủ công vào Thẻ Giáo viên, người dùng chỉ cần:
  + Bấm 1 nút: **"⚡ Dịch sang Phân công chuyên môn"** $\rightarrow$ Hệ thống tự động bóc tách tất cả các lớp của từng môn mà GV dạy và cập nhật trực tiếp vào phân công lớp (`teacher.assignments`)!

### 2. Thiết kế Kỹ thuật
1. **Hàm trích xuất phân công từ TKB của một giáo viên (`extractAssignmentsFromTimetable(teacher)`)**:
   - Duyệt qua `teacher.timetable.morning` và `teacher.timetable.afternoon` (Thứ 2 đến Thứ 7, các tiết 1 đến 10).
   - Gọi `parseTimetableCell(cell)` để lấy `subject` và `class_name`.
   - Nếu ô có môn và lớp:
     + Khớp `subject` với `state.subjects` (so sánh `foldText(s.name) === foldText(subject)` hoặc `foldText(s.key) === foldText(subject)`). Nếu không tìm thấy, tạo môn mới hoặc bỏ qua kèm thông báo.
     + Chuẩn hóa tên lớp: cắt khoảng trắng (VD: `63`, `6/3`, `9A1`).
     + Lưu vào map: `bySubject[sub.key].add(className)`.
   - Trả về đối tượng: `{ [subjectKey]: ['63', '64', ...] }`.

2. **Hàm áp dụng phân công cho một giáo viên (`applyTimetableToAssignments(teacherId)`)**:
   - Lấy danh sách lớp theo môn từ hàm trích xuất trên.
   - Với các lớp chưa có trong `state.classes`: tự động bổ sung vào `state.classes` để không bị sót lớp.
   - Gán vào `teacher.assignments[subKey]`:
     + Hợp nhất danh sách lớp hoặc ghi đè (hỏi người dùng hoặc thông báo số lớp được gán).
     + Tự động dọn dẹp các lớp này khỏi `state.unassigned[subKey]`.
     + Nếu lớp đó trước đây đang được gán cho một giáo viên khác, gỡ khỏi GV cũ (chuyển giao phân công về GV này).
   - Lưu snapshot và gọi `render()`.
   - Hiển thị Toast thông báo: *"Đã cập nhật phân công X lớp cho GV [Tên GV] từ Thời khoá biểu!"*.

3. **Hàm đồng bộ phân công toàn tổ từ TKB (`syncAllAssignmentsFromTimetables()`)**:
   - Duyệt qua tất cả giáo viên trong `state.teachers` có `timetableHasLessons(t.timetable)`.
   - Tự động chạy bóc tách và phân công hàng loạt cho cả tổ.
   - Toast thông báo tổng hợp: *"Đã cập nhật phân công cho X giáo viên từ Thời khoá biểu!"*.

4. **Giao diện Người dùng (UI)**:
   - **Trong Modal Thời khoá biểu Giáo viên (`#teacher-timetable-modal`)**:
     + Thêm nút cạnh nút Lưu: `<button type="button" class="btn btn-outline-primary" onclick="applyCurrentTimetableToAssignments()"><i class="fas fa-arrows-rotate"></i> Dịch sang Phân công</button>`.
     + Thêm tùy chọn checkbox: `☑️ Tự động cập nhật phân công chuyên môn khi lưu TKB`.
   - **Trên Thẻ Giáo viên (View 1)**:
     + Trong menu / nút TKB có nút nhanh: `⚡ Nạp phân công từ TKB`.
   - **Trên Thanh Công cụ (Menu Tệp / Công cụ)**:
     + Thêm mục: `⚡ Đồng bộ phân công từ TKB toàn tổ`.

---

## Cách kiểm thử
1. **Kiểm tra Khai báo Nhiệm vụ Kiêm nhiệm Trường**:
   - Mở Khai báo tổ -> Tab 4 Môn học.
   - Thêm hàng mới: Mã `CDS`, Tên `Chuyển đổi số`, Loại: `Kiêm nhiệm trường (Không dạy lớp, tính tiết)`, Số tiết: `3`.
   - Bấm "Áp dụng cấu hình".
2. **Kiểm tra Kho Lớp và Ma trận Lớp**:
   - Kho lớp bên trái KHÔNG sinh 25 lớp `CDS`.
   - Bảng Ma trận Lớp học KHÔNG có cột `CDS`.
3. **Kiểm tra Gán nhiệm vụ Kiêm nhiệm Trường cho Giáo viên**:
   - Gán `Chuyển đổi số (3t)` cho Thầy Danh.
   - Thẻ của Thầy Danh hiện tag `⚙️ Chuyển đổi số (+3t)`.
   - Tổng tiết của Thầy Danh tự động tăng thêm 3 tiết.
   - Bảng Ma trận Giáo viên và Báo cáo hiển thị: `CĐS (3t)` trong cột Giảm trừ / kiêm nhiệm.
4. **Kiểm tra Dịch ngược từ TKB sang Phân công**:
   - Mở modal TKB của Thầy Danh (đã có các tiết Toán 63, 64, 93, 94).
   - Bấm nút "Dịch sang Phân công".
   - Đóng modal: Quan sát Thẻ của Thầy Danh trên View 1:
     + Môn Toán tự động có 4 lớp: `63, 64, 93, 94`.
     + Kho lớp môn Toán tự động giảm 4 lớp tương ứng.
     + Tổng tiết dạy tăng lên 16 tiết (4 lớp x 4 tiết).
5. **Kiểm tra Snapshot Đợt**:
   - Đổi đợt phân công -> Dữ liệu kiêm nhiệm trường và phân công lớp được bảo toàn đúng từng đợt.

---

## Tiêu chí nghiệm thu
1. Cung cấp tùy chọn loại nhiệm vụ thứ 3: `Kiêm nhiệm trường (Không dạy lớp, tính tiết)`.
2. Nhiệm vụ kiêm nhiệm trường không sinh lớp trong kho lớp và không tạo cột trong ma trận lớp.
3. Gán được trực tiếp cho giáo viên (qua kéo thả hoặc menu chọn nhanh).
4. Tự động tính số tiết kiêm nhiệm trường vào tổng định mức / tải công tác của giáo viên và hiển thị minh bạch.
5. Hỗ trợ dịch ngược 1-click từ Thời khóa biểu sang Phân công chuyên môn (bóc tách các lớp/môn từ TKB gán vào `teacher.assignments`).