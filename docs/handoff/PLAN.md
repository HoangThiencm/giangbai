# PLAN: Đề xuất thông minh Giáo viên Dạy thay theo Thời khóa biểu (2 cột: Trống cả buổi & Trống tiết cần thay)

## Hiện trạng & Nhu cầu người dùng

1. **Hiện trạng quy trình ghi nhận Dạy thay (`#view-daythay`)**:
   - Khi có một giáo viên nghỉ dạy (do công tác, ốm, việc bận...), Tổ trưởng chuyên môn chọn:
     - Ngày dạy (`#new-sub-date`)
     - Buổi dạy (`#new-sub-session`: Sáng / Chiều)
     - Giáo viên được thay / nghỉ (`#new-sub-for-teacher`)
   - Hệ thống đã có sẵn tính năng tự động trích xuất các tiết cần dạy thay từ TKB của giáo viên nghỉ (`autoSuggestSlotsFromTimetable`).
   - Tuy nhiên, tại ô **"Giáo viên thực dạy" (`#new-sub-teacher`)**, hệ thống chỉ hiển thị một danh sách phẳng toàn bộ giáo viên trong tổ.
   - Tổ trưởng không biết giáo viên nào rảnh cả buổi, giáo viên nào đang có mặt ở trường nhưng trống tiết đó, hoặc giáo viên nào bị trùng giờ dạy. Người dùng phải tự nhớ hoặc tra cứu thủ công TKB của từng người rất mất thời gian.

2. **Nhu cầu người dùng**:
   - Khi chọn một giáo viên nghỉ dạy và buổi nghỉ:
     - Tự động lọc và hiển thị danh sách đề xuất giáo viên dạy thay chia làm **2 cột trực quan**:
       - **Cột 1**: Giáo viên trống cả buổi (không có bất kỳ tiết nào trong buổi đó).
       - **Cột 2**: Giáo viên có mặt tại trường nhưng trống đúng các tiết cần dạy thay (có tiết dạy trong buổi đó nhưng không trùng các tiết cần thay).
     - Bấm chọn 1 chạm vào bất kỳ giáo viên nào trong 2 cột là tự động điền vào ô "Giáo viên thực dạy".

---

## Mục tiêu & Giải pháp thiết kế

### 1. Thuật toán phân loại giáo viên rảnh dạy thay (`computeDayThayTeacherAvailability`)
Xây dựng hàm phân tích lịch dạy của tất cả giáo viên trong tổ cho một ngày và buổi cụ thể:
- **Đầu vào**:
  - `date`: Ngày dạy (`YYYY-MM-DD`).
  - `session`: `'morning'` hoặc `'afternoon'`.
  - `forTeacherId`: ID của giáo viên nghỉ dạy.
  - `neededPeriods`: Mảng các tiết cần dạy thay (ví dụ: `[1, 2]` lấy từ các tiết đang được chọn/bật trong `#period-slots-builder`).
- **Xử lý**:
  - `dayNum = weekdayNumberFromDate(date)` (2 đến 7). Nếu là Chủ nhật hoặc không hợp lệ -> bỏ qua.
  - Duyệt qua danh sách `state.teachers`, loại trừ giáo viên nghỉ (`t.id !== forTeacherId`):
    - Lấy các tiết dạy của giáo viên đó trong buổi và thứ tương ứng: `slots = getTimetableDaySlots(t, session, dayNum)`.
    - `busyPeriods = slots.map(s => s.period_num)`.
    - **Nhóm 1: Trống cả buổi (`freeSessionTeachers`)**:
      - Điều kiện: `slots.length === 0`.
      - Đây là những giáo viên không có tiết nào trong buổi đó, hoàn toàn rảnh cả buổi.
    - **Nhóm 2: Có mặt, trống đúng các tiết cần thay (`freeSlotTeachers`)**:
      - Điều kiện: `slots.length > 0` VÀ không có bất kỳ tiết nào trong `busyPeriods` trùng với `neededPeriods` (tức là `busyPeriods.every(p => !neededPeriods.includes(p))`).
      - Ví dụ: Cần thay tiết 1, 2; giáo viên này dạy tiết 3, 4 -> rảnh tiết 1, 2 và có mặt sẵn ở trường.
    - **Nhóm 3: Bị trùng tiết (`busyConflictTeachers`)**:
      - Điều kiện: Có ít nhất 1 tiết trong `busyPeriods` trùng với `neededPeriods`.

### 2. Giao diện người dùng (UI / UX)
- Tại `#view-daythay` (ngay dưới cụm chọn Giáo viên thực dạy và Giáo viên được thay):
  - Bổ sung một panel đề xuất thông minh `#daythay-suggestion-panel`:
    - Tiêu đề: `💡 Đề xuất giáo viên dạy thay (Thứ X - Buổi Sáng/Chiều · Cần thay tiết: 1, 2)`.
    - **Cột 1 — Giáo viên trống cả buổi**:
      - Badge số lượng giáo viên.
      - Danh sách thẻ giáo viên: Tên, môn/tổ, nút `[Chọn dạy thay]` (màu xanh lá `#16a34a`).
    - **Cột 2 — Giáo viên có mặt, trống tiết cần thay**:
      - Badge số lượng giáo viên.
      - Danh sách thẻ giáo viên: Tên, thông tin tiết rảnh/bận (ví dụ: `Rảnh tiết 1, 2 · Dạy tiết 3, 4 lớp 7A1`), nút `[Chọn dạy thay]` (màu tím xanh `#4f46e5`).
  - **Tương tác một chạm**:
    - Khi bấm nút `[Chọn dạy thay]` ở bất kỳ thẻ giáo viên nào:
      - Tự động gán giá trị vào dropdown `#new-sub-teacher`.
      - Đánh dấu active/highlight thẻ giáo viên vừa chọn.
      - Hiển thị toast thông báo: `"Đã chọn thầy/cô [Tên] làm giáo viên dạy thay."`.
  - **Nâng cấp dropdown `#new-sub-teacher`**:
    - Thêm nhãn trạng thái trực tiếp vào từng option trong thẻ `<select>`:
      - `Nguyễn Văn A (Trống cả buổi)`
      - `Trần Thị B (Trống tiết 1, 2 - Dạy tiết 3, 4)`
      - `Lê Văn C ⚠️ (Trùng lịch)`

### 3. Tự động kích hoạt đồng bộ
Hàm `renderDayThaySuggestions()` sẽ tự động chạy khi:
- Người dùng chọn hoặc thay đổi:
  - Ngày dạy (`#new-sub-date`)
  - Buổi dạy (`#new-sub-session`)
  - Giáo viên được thay (`#new-sub-for-teacher`)
  - Bật/tắt các tiết cần thay trong lưới `#period-slots-builder`
- Khi `Loại hình` là `makeup` (dạy bù): tự động ẩn panel đề xuất (vì dạy bù là cho chính lớp của mình, không cần tìm người dạy thay).

---

## Phạm vi thực hiện

1. `phancongtochuyenmon.html`:
   - Bổ sung markup HTML của `#daythay-suggestion-panel` gồm 2 cột (Trống cả buổi & Trống tiết).
   - Thêm hàm `computeDayThayTeacherAvailability(date, session, forTeacherId, neededPeriods)`.
   - Thêm hàm `renderDayThaySuggestions()`.
   - Thêm hàm `selectDayThaySuggestedTeacher(teacherId)`.
   - Tích hợp gọi `renderDayThaySuggestions()` vào các hàm: `maybeAutoSuggestSlotsFromTimetable()`, `onDayThaySessionChange()`, `onSlotToggle()`, `setQuickSlots()`, `clearAllSlots()`, `populateDayThayFormSelects()`, `resetDayThayForm()`.
2. `tests/daythay-suggest-smoke.js`:
   - Viết bài test smoke chuyên biệt:
     - Kiểm tra thuật toán phân loại đúng 3 nhóm: trống cả buổi, trống tiết phù hợp, và trùng lịch.
     - Kiểm tra hàm `selectDayThaySuggestedTeacher` cập nhật đúng `#new-sub-teacher`.
     - Kiểm tra ẩn panel khi loại hình là `makeup`.

---

## Ngoài phạm vi

- Không thay đổi cấu trúc dữ liệu lưu trữ bản ghi Sổ Dạy Thay (`state.attendance.substitutes`).
- Không thay đổi định dạng in thông báo dạy thay hoặc xuất báo cáo.

---

## Kế hoạch kiểm thử (Verification Plan)

1. `node tests/daythay-suggest-smoke.js`: PASS toàn bộ logic tính toán độ khả dụng và phân loại 2 cột.
2. `node tests/baogiang-weekday-segment-smoke.js`: PASS.
3. `node tests/timetable-render-smoke.js`: PASS.
4. `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
5. `node tests/auto-reload-smoke.js`: PASS.
6. `git diff --check`: PASS.
