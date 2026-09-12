# PLAN: Bổ sung tùy chọn Buổi dạy "Cả ngày" (Sáng / Chiều / Cả ngày) trong Sổ Dạy thay

## Hiện trạng & Yêu cầu người dùng

1. **Hiện trạng**:
   - Tại form ghi nhận Dạy thay / Dạy bù (`#view-daythay`), dropdown **Buổi dạy** (`#new-sub-session`) hiện chỉ có 2 lựa chọn:
     - `Sáng (tiết ...)`
     - `Chiều (tiết ...)`
   - Khi một giáo viên nghỉ trọn vẹn cả ngày (ví dụ: đi công tác cả ngày, nghỉ ốm, hội nghị...), Tổ trưởng phải tạo tách rời làm 2 lượt (1 lượt sáng, 1 lượt chiều) hoặc không thể lấy đồng thời toàn bộ các tiết dạy trong ngày của giáo viên đó từ TKB.

2. **Yêu cầu người dùng**:
   - Thêm lựa chọn **"Cả ngày"** vào mục Buổi dạy (`#new-sub-session`):
     - `Sáng (tiết ...)`
     - `Chiều (tiết ...)`
     - `Cả ngày (Sáng & Chiều)`

---

## Mục tiêu & Giải pháp thiết kế

### 1. Cập nhật giao diện Dropdown Buổi dạy (`#new-sub-session`)
- Trong HTML `phancongtochuyenmon.html` (dòng 2027):
  ```html
  <select class="form-control" id="new-sub-session" onchange="onDayThaySessionChange()">
      <option value="morning">Sáng</option>
      <option value="afternoon">Chiều</option>
      <option value="all_day">Cả ngày (Sáng & Chiều)</option>
  </select>
  ```
- Cập nhật hàm `updateSessionSelectLabels()`:
  - Cập nhật text option `morning`: `Sáng (tiết ${mLabel})`
  - Cập nhật text option `afternoon`: `Chiều (tiết ${aLabel})`
  - Cập nhật text option `all_day`: `Cả ngày (Sáng & Chiều)` hoặc `Cả ngày (tiết ${mLabel}, ${aLabel})`

### 2. Xử lý logic khung tiết và TKB cho "Cả ngày" (`all_day`)
1. **Hàm `getSessionLabel(session)`**:
   - Trả về `'Cả ngày'` nếu `session === 'all_day'`, `'Chiều'` nếu `session === 'afternoon'`, ngược lại `'Sáng'`.
2. **Hàm `getSessionPeriods(session)`**:
   - Khi `session === 'all_day'`: Lấy cả danh sách tiết sáng và tiết chiều gộp lại và sắp xếp tăng dần:
     `return [...new Set([...mPeriods, ...aPeriods])].sort((a, b) => a - b);`
3. **Hàm `getTimetableDaySlots(teacher, session, dayNum)`**:
   - Khi `session === 'all_day'`: Thu thập toàn bộ các tiết từ cả hai khối sáng (`'morning'`) và chiều (`'afternoon'`):
     `return [...getTimetableDaySlots(teacher, 'morning', dayNum), ...getTimetableDaySlots(teacher, 'afternoon', dayNum)].sort((a, b) => a.period_num - b.period_num);`
   - Khi bấm "Lấy tiết từ TKB" (`autoSuggestSlotsFromTimetable`), hệ thống sẽ nạp tự động đầy đủ tất cả các tiết trong ngày (cả sáng và chiều) của giáo viên nghỉ.
4. **Hàm `initPeriodSlotsBuilder` và `getVisibleSlotNumbers`**:
   - Hiển thị đầy đủ các ô tiết của cả sáng và chiều để người dùng tick chọn phân bổ cho từng lớp.
5. **Đề xuất giáo viên dạy thay thông minh (`computeDayThayTeacherAvailability` & `renderDayThaySuggestions`)**:
   - Hỗ trợ `session === 'all_day'`:
     - **Trống cả buổi (Trống cả ngày)**: Giáo viên không có bất kỳ tiết nào trong cả sáng lẫn chiều của ngày hôm đó (`slots.length === 0`).
     - **Có mặt, trống tiết cần thay**: Giáo viên có giờ dạy trong ngày nhưng toàn bộ các tiết dạy không trùng với bất kỳ tiết nào cần thay.
     - **Trùng lịch**: Giáo viên có ít nhất một tiết trùng với các tiết cần thay.
     - Tiêu đề đề xuất hiển thị: `Buổi Cả ngày · Cần thay tiết: ...`
6. **Bảng thông báo / Xuất sổ dạy thay (`collectFormAnnouncementRows`)**:
   - Khi lưu bản ghi với `session === 'all_day'`, phân tách buổi của từng tiết theo đúng khung giờ: tiết thuộc sáng ghi "Sáng", tiết thuộc chiều ghi "Chiều".
7. **Bản ghi Sổ Dạy thay (`saveDayThayRecord` & `editDayThayRecord`)**:
   - Lưu trữ an toàn giá trị `session: 'all_day'` vào bản ghi `state.attendance.substitutes`.
   - Khi chỉnh sửa (`editDayThayRecord`), khôi phục đúng giá trị `#new-sub-session` là `'all_day'`.

---

## Phạm vi thực hiện

1. `phancongtochuyenmon.html`:
   - Bổ sung `<option value="all_day">` vào `#new-sub-session`.
   - Cập nhật `updateSessionSelectLabels()`, `getSessionLabel()`, `getSessionPeriods()`, `getTimetableDaySlots()`.
   - Cập nhật `computeDayThayTeacherAvailability()` và `renderDayThaySuggestions()` hỗ trợ `'all_day'`.
   - Cập nhật `collectFormAnnouncementRows()` xác định buổi từng tiết khi `'all_day'`.
2. `tests/daythay-suggest-smoke.js`:
   - Bổ sung test kiểm tra:
     - Dropdown `#new-sub-session` có đủ 3 lựa chọn (Sáng, Chiều, Cả ngày).
     - `getSessionPeriods('all_day')` trả về kết hợp tiết sáng và chiều.
     - `getTimetableDaySlots(teacher, 'all_day', dayNum)` gom đủ tiết cả sáng và chiều.
     - `computeDayThayTeacherAvailability` tính đúng độ khả dụng cho `all_day`.

---

## Ngoài phạm vi

- Không làm thay đổi cấu trúc bảng CSDL của `phancong.php` hay file JSON sao lưu.

---

## Kế hoạch kiểm thử (Verification Plan)

1. `node tests/daythay-suggest-smoke.js`: PASS toàn bộ kiểm thử `all_day`, lấy tiết TKB và gợi ý giáo viên.
2. `node tests/baogiang-weekday-segment-smoke.js`: PASS.
3. `node tests/timetable-render-smoke.js`: PASS.
4. `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
5. `node tests/auto-reload-smoke.js`: PASS.
6. `git diff --check`: PASS.
