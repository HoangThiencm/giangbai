# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] **Kiêm nhiệm trường (Không dạy lớp, tính tiết trực tiếp cho GV)**:
  + Chuẩn hóa 3 loại nhiệm vụ trong `state.subjects` (`duty_type: 'core' | 'class_duty' | 'school_duty'`) và bảo toàn tương thích ngược dữ liệu cũ.
  + Modal Khai báo tổ -> Tab 4 Môn học & Nhiệm vụ hiển thị dropdown 3 lựa chọn kèm chú thích số tiết rõ ràng.
  + Nhiệm vụ `school_duty` không sinh kho lớp chưa phân công (`state.unassigned`), không tạo cột trong bảng ma trận lớp (`#matrix-classes-table`).
  + Hỗ trợ gán trực tiếp cho giáo viên bằng kéo thả hoặc nút chọn nhanh `+ Kiêm nhiệm` trên thẻ GV.
  + Hàm `calcSchoolDutiesPeriods` tính chính xác số tiết quy đổi và cộng vào tổng số tiết / định mức (`calcTeacherTotalPeriods`).
  + Hiển thị minh bạch tag nhiệm vụ `[Tên nhiệm vụ (+Xt)] ✕` trên thẻ GV, trong cột Giảm trừ/kiêm nhiệm ở Bảng ma trận tổng hợp và Báo cáo / Xuất Excel.
- [x] **Dịch ngược từ Thời khóa biểu sang Phân công chuyên môn**:
  + Hàm `extractAssignmentsFromTimetable` duyệt qua toàn bộ ma trận TKB tuần của giáo viên, bóc tách chính xác các cặp `{ môn, lớp }` và gom nhóm lớp theo môn học.
  + Hàm `applyTimetableToAssignments` tự động cập nhật danh sách lớp vào `teacher.assignments[subKey]`, dọn dẹp khỏi kho lớp chưa gán (`state.unassigned`), tự động bổ sung lớp mới vào `state.classes`, và chuyển giao lớp nếu lớp từng được gán cho GV khác.
  + Hàm `syncAllAssignmentsFromTimetables` duyệt toàn bộ giáo viên đã có TKB và cập nhật phân công hàng loạt cho cả tổ.
  + Giao diện tích hợp đầy đủ: nút "Dịch sang Phân công" + checkbox tự động trong Modal TKB, nút "Nạp phân công từ TKB" trên Thẻ GV, và mục "Đồng bộ phân công từ TKB toàn tổ" trong Menu Công cụ / Tệp.

## Test đã chạy
1. `tests/smartquiz-smoke.js`: PASS.
2. `tests/xaydungphuluc-smoke.js`: PASS.
3. Kiểm tra tính duy nhất của toàn bộ 124 HTML IDs: 100% unique, không có ID trùng lặp.
4. Kiểm tra sự tồn tại và cú pháp của 9 hàm JS nghiệp vụ mới (`getSubjectDutyType`, `assignSchoolDuty`, `unassignSchoolDuty`, `calcSchoolDutiesPeriods`, `extractAssignmentsFromTimetable`, `applyTimetableToAssignments`, `syncAllAssignmentsFromTimetables`...): PASS.
5. Kiểm tra hàm `getSubjectDutyType` với 3 loại nhiệm vụ và dữ liệu cũ tương thích ngược: PASS.
6. Kiểm tra quy trình gán, hủy nhiệm vụ kiêm nhiệm trường và phép tính số tiết (`calcSchoolDutiesPeriods`, `calcTeacherTotalPeriods`): PASS.
7. Kiểm tra hàm `extractAssignmentsFromTimetable` bóc tách đúng các lớp từ ma trận TKB tuần: PASS.
8. Kiểm tra hàm `applyTimetableToAssignments` gán lớp cho GV, dọn kho lớp, chuyển lớp trùng từ GV khác: PASS.
9. Kiểm tra hàm `syncAllAssignmentsFromTimetables` đồng bộ phân công toàn tổ từ TKB: PASS.
10. Bộ kiểm thử TKB & Khung tiết trước đó (`scratch/verify_test_timetable.js`): ALL 7 TESTS PASS.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Cung cấp tùy chọn loại nhiệm vụ thứ 3 `Kiêm nhiệm trường (Không dạy lớp, tính tiết)` → PASS
- Tiêu chí 2: Nhiệm vụ kiêm nhiệm trường không sinh lớp trong kho lớp và không tạo cột trong ma trận lớp → PASS
- Tiêu chí 3: Gán được trực tiếp cho giáo viên, tự động tính số tiết vào tổng định mức / tải công tác của GV → PASS
- Tiêu chí 4: Hỗ trợ dịch ngược 1-click từ Thời khóa biểu sang Phân công chuyên môn của từng GV và toàn tổ → PASS

## Bug
Không phát hiện bug.