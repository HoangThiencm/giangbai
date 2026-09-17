# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Khắc phục dropdown giáo viên (#bg-filter-teacher) trống khi state.teachers ở root rỗng: Đã thêm `getBaoGiangTeacherList()` fallback thông minh từ `state.phase_assignments` và `systemData.teachers`. ĐÚNG SCOPE.
- Hiển thị đầy đủ số lượng giáo viên `Tất cả giáo viên (X GV)` và tên GV kèm chức vụ/phân công. ĐÚNG SCOPE.
- Bổ sung banner hướng dẫn điều hướng sang Tab 2 khi giáo viên có phân công chuyên môn nhưng chưa có thời khóa biểu chi tiết. ĐÚNG SCOPE.
- Tự động đồng bộ số tiết Dạy thay / Dạy bù và bảo toàn dữ liệu khi autoFillAttendance, tự động lưu CSDL (`performSaveToDB`). ĐÚNG SCOPE.
- Không thêm chức năng ngoài kế hoạch, không can thiệp kiến trúc ngoài plan.

## Test đã chạy
- `node tests/baogiang-teacher-month-smoke.js` — PASS (lọc GV, fallback đợt, hiển thị cảnh báo TKB, lịch tháng).
- `node tests/attendance-autosync-smoke.js` — PASS (đồng bộ Chấm công, bảo toàn dạy thay/bù, lưu CSDL).
- `node tests/baogiang-weekday-segment-smoke.js` — PASS (PPCT đa tuần, cảnh báo hai GV, khóa mốc).
- `node tests/baogiang-recognition-smoke.js` — PASS (compile, PPCT retry/success, parse PDF/legacy).
- `node tests/timetable-render-smoke.js` — PASS (render TKB GV, layout compact, responsive).

## Pass / Fail từng tiêu chí
- Fallback danh sách giáo viên từ phase_assignments / systemData: PASS.
- Dropdown hiển thị đầy đủ tên giáo viên khi có PCCM: PASS.
- Trạng thái chưa có TKB hiển thị thông báo hướng dẫn và nút điều hướng: PASS.
- Sổ báo giảng theo tháng, lọc theo GV, các chế độ xem: PASS.
- Chấm công tự động đồng bộ và lưu CSDL: PASS.

## Bug
Không phát hiện bug còn tồn đọng.
