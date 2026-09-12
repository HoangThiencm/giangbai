# PLAN: Khắc phục lỗi Thời khoá biểu đã nhận diện nhưng không hiển thị trên giao diện

Trạng thái: CHỜ CODER THỰC HIỆN

---

## 1. Vấn đề & Hiện trạng
- **Hiện tượng**:
  - Khi dùng tính năng "AI nhận diện TKB" hoặc chuyển sang tab "2. Thời khoá biểu GV", cột bên trái đã nhận diện thành công số tiết và hiện huy hiệu `✓ Đã có TKB (12 tiết)` cho giáo viên.
  - Tuy nhiên ở khung bên phải, dưới hai tiêu đề **Buổi sáng** và **Buổi chiều**, bảng thời khoá biểu hoàn toàn trống trơn (không có lưới bảng, không có ô tiết học nào).
- **Nguyên nhân cốt lõi**:
  1. **Không nạp `editingTimetable` khi mở tab / khởi tạo (`renderTimetableView`)**:
     - `renderTimetableView()` chỉ gán `selectedTimetableTeacherId = state.teachers[0].id` mà không gọi `selectTimetableTeacher(selectedId)`.
     - `editingTimetable` bị bỏ quên ở giá trị `null`. Khi `renderTimetableGrid()` chạy, nó thấy `null` nên gán thành `emptyTimetable()`, làm mất dữ liệu TKB của giáo viên vừa chọn.
  2. **So sánh ID giáo viên strict `===` giữa số và chuỗi**:
     - Trong `selectTimetableTeacher(teacherId)`, `persistTeacherTimetable`, `applyTimetableToAssignments`: dùng `t.id === teacherId`.
     - Nếu `t.id` là số (timestamp) và `teacherId` truyền từ chuỗi HTML `selectTimetableTeacher('${t.id}')` thì phép so sánh trả về `undefined`. Giáo viên không tìm thấy dẫn đến `editingTimetable` bị rỗng.
  3. **Lỗi Uncaught Exception trong `applyAiTimetableResult` ngắt render workspace**:
     - Trong `applyAiTimetableResult()`, cờ `autoApply` bật mặc định gọi `applyTimetableToAssignments` -> `renderPool()` -> `renderTeachers()` trước khi gọi `renderTimetableWorkspace()`.
     - Nếu phân công lớp có môn chưa khớp hoặc state unassigned thiếu key, exception sẽ chặn đứng luồng thực thi trước khi `renderTimetableWorkspace()` được gọi, để lại hai thẻ `#tt-morning-wrap` và `#tt-afternoon-wrap` rỗng nguyên thủy.
  4. **Fallback khung tiết trong `periodsForTimetableSession`**:
     - Khi cấu hình tiết trong `state.info.morning_periods` rỗng hoặc không parse được, danh sách tiết trả về mảng rỗng khiến `rows` không sinh được hàng nào.

---

## 2. Giải pháp kỹ thuật chi tiết (`phancongtochuyenmon.html`)

### 2.1. Sửa hàm `renderTimetableView()`
Đảm bảo luôn kích hoạt `selectTimetableTeacher` để nạp `editingTimetable` và render đầy đủ:
```javascript
function renderTimetableView() {
    bindTimetableInputEvents();
    const targetId = selectedTimetableTeacherId || (state.teachers[0] ? state.teachers[0].id : null);
    if (targetId) {
        selectTimetableTeacher(targetId);
    } else {
        renderTimetableTeacherList();
        renderTimetableWorkspace();
    }
}
```

### 2.2. Chuẩn hoá so sánh ID giáo viên (`String(id)`)
Thay thế toàn bộ các phép so sánh `t.id === teacherId` trong module Thời khoá biểu thành so sánh chuỗi an toàn:
- Trong `selectTimetableTeacher(teacherId)`:
  `const teacher = (state.teachers || []).find(t => String(t.id) === String(teacherId));`
- Trong `persistTeacherTimetable(teacherId, timetable)`:
  `const t = (teachers || []).find(x => String(x.id) === String(teacherId));`
- Trong `renderTimetableWorkspace()`:
  `const teacher = (state.teachers || []).find(t => String(t.id) === String(selectedTimetableTeacherId));`
- Trong `renderTimetableTeacherList()`:
  `const active = String(t.id) === String(selectedTimetableTeacherId) ? 'active' : '';`
- Trong `goToPrevTimetableTeacher` và `goToNextTimetableTeacher`:
  `const idx = list.findIndex(t => String(t.id) === String(selectedTimetableTeacherId));`

### 2.3. Bọc `applyAiTimetableResult()` an toàn bằng `try...catch`
Đảm bảo bảng lưới TKB luôn luôn được render ngay cả khi quá trình tự động đồng bộ phân công môn/lớp gặp cảnh báo:
- Bọc `applyTimetableToAssignments`, `renderLiveStatsBanner`, `renderPool`, `renderTeachers` trong `try...catch`.
- Luôn gọi `renderTimetableWorkspace()` và `renderTimetableTeacherList()`.

### 2.4. Đảm bảo fallback `periodsForTimetableSession`
Nếu `getSessionPeriods(session)` trả về mảng rỗng, bắt buộc fallback về `[1, 2, 3, 4, 5]` (sáng) và `[1, 2, 3, 4]` (chiều) để bảng luôn có hàng và cột hiển thị đầy đủ.

---

## 3. Danh sách File tác động
- `phancongtochuyenmon.html`: Cập nhật các hàm `renderTimetableView`, `selectTimetableTeacher`, `applyAiTimetableResult`, `persistTeacherTimetable`, `renderTimetableWorkspace`, `periodsForTimetableSession`.
- `tests/timetable-render-smoke.js`: Tạo test kiểm tra nạp TKB và render bảng HTML.

---

## 4. Tiêu chí nghiệm thu (Acceptance Criteria)
1. Khi bấm chọn bất kỳ giáo viên nào trong danh sách (kể cả giáo viên đầu tiên khi vừa chuyển tab): bảng Thời khoá biểu Buổi sáng & Buổi chiều hiển thị đầy đủ các tiết học đã có.
2. Khi dùng "AI nhận diện TKB": Sau khi nhận diện xong, bảng hiển thị ngay lập tức các tiết môn/lớp mà không bị trắng bảng.
3. Không phát sinh lỗi console JavaScript khi chọn giáo viên hoặc nhận diện TKB.
