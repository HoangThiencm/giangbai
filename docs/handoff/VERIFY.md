# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] **Tách Thời khóa biểu thành Tab riêng trong thanh Workspace Navigation**:
  + Thêm Tab `2. Thời khoá biểu GV` (`#tab-nav-timetable`, view `#view-timetable`) trên thanh menu tab.
  + Đánh số lại các tab mạch lạc: 1. Phân công · 2. TKB GV · 3. Sổ Dạy Thay · 4. Chấm công · 5. Tăng giờ · 6. Báo cáo.
  + Hàm `switchAppView('view-timetable')` kích hoạt giao diện toàn trang chuyên nghiệp 2 cột.
  + Bỏ modal cũ `#teacher-timetable-modal` để tránh trùng lặp ID và tránh chật chội; giữ alias `openTeacherTimetableModal(id)` điều hướng mượt mà sang Tab TKB và focus đúng GV.
- [x] **Không gian làm việc TKB toàn trang 2 cột**:
  + **Cột trái**: Danh sách giáo viên tổ kèm bộ lọc (`Tất cả`, `Đã có TKB`, `Chưa có TKB`), ô tìm kiếm nhanh và thống kê tiến độ `Đã có TKB: X / Y GV`. Badge trạng thái xanh lá `✓ Đã có TKB (X tiết)` và chấm xanh `● Chưa lưu CSDL`.
  + **Cột phải**: Header GV đang chọn kèm nút chuyển GV trước/sau, vùng dán ảnh thông minh Ctrl+V/Upload, nút AI nhận diện, lưới ma trận tuần Buổi sáng & Buổi chiều.
- [x] **Tự động lưu Local liên tục khi AI nhận diện**:
  + Hàm `applyAiTimetableResult` sau khi đọc JSON từ AI lập tức gọi `persistTeacherTimetable`, `saveCurrentPhaseSnapshot`, và `saveToLocal({ autoSave: false })` ghi thẳng vào `localStorage`.
  + Badge GV bên cột trái tự động chuyển sang `✓ Đã có TKB`.
  + Nút `GV tiếp theo ➔` cho phép nhảy nhanh sang giáo viên kế tiếp chưa có TKB để làm việc liên tục không ngắt quãng.
- [x] **Lưu CSDL 1 lần duy nhất cho toàn bộ tổ**:
  + Nút **`Lưu tất cả lên CSDL`** (`btn-db-save`) trên Tab TKB gọi `saveToDB()` đẩy toàn bộ `state` (chứa TKB của tất cả GV và phân công các đợt) lên server MySQL qua `api/phancong.php?action=save`.

## Test đã chạy
1. `tests/smartquiz-smoke.js`: PASS.
2. `tests/xaydungphuluc-smoke.js`: PASS.
3. Kiểm tra tính duy nhất của toàn bộ 134 HTML IDs: 100% unique, không có ID trùng lặp, modal cũ đã được loại bỏ an toàn.
4. Kiểm tra sự tồn tại của đầy đủ các phần tử DOM phục vụ Tab TKB (`tab-nav-timetable`, `view-timetable`, `tt-left-panel`, `tt-teacher-search`, `tt-teacher-list`, `tt-right-panel`, `tt-school-year`, `tt-semester`, `tt-dropzone`, `btn-ai-scan-tt`, `tt-morning-wrap`, `tt-afternoon-wrap`): PASS.
5. Kiểm tra 10 hàm JS nghiệp vụ (`switchAppView`, `renderTimetableView`, `renderTimetableTeacherList`, `selectTimetableTeacher`, `renderTimetableWorkspace`, `goToPrevTimetableTeacher`, `goToNextTimetableTeacher`, `applyAiTimetableResult`, `openTeacherTimetableModal`, `saveToDB`): PASS.
6. Kiểm tra `switchAppView('view-timetable')` kích hoạt view và chọn giáo viên mặc định: PASS.
7. Kiểm tra `openTeacherTimetableModal(id)` điều hướng tương thích ngược sang Tab TKB và focus đúng giáo viên: PASS.
8. Kiểm tra AI bóc tách TKB tự động lưu vào `localStorage`, cập nhật `state.teachers[].timetable` và bật cờ `hasUnsavedChanges`: PASS.
9. Kiểm tra điều hướng tuần tự `goToNextTimetableTeacher(true)` nhảy đúng giáo viên chưa có TKB và `goToPrevTimetableTeacher` quay lại chính xác: PASS.
10. Bộ kiểm thử kiêm nhiệm trường & dịch ngược TKB (`scratch/verify_test_school_duty_and_reverse_tt.js`): ALL 7 TESTS PASS.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Thời khóa biểu được tách thành một Tab riêng biệt trong thanh làm việc của Quản lý tổ chuyên môn (`view-timetable`) → PASS
- Tiêu chí 2: Giao diện toàn trang 2 cột chuyên nghiệp: Cột trái liệt kê giáo viên kèm trạng thái TKB trực quan, cột phải là bảng làm việc TKB chi tiết → PASS
- Tiêu chí 3: Nhận diện ảnh TKB tự động lưu ngay vào máy (`localStorage`), cho phép chuyển liên tục qua các giáo viên khác mà không bị đóng/mở ngắt quãng → PASS
- Tiêu chí 4: Cung cấp nút Lưu CSDL rõ ràng để người dùng nhấn lưu 1 lần sau khi đã hoàn tất toàn bộ giáo viên trong tổ → PASS
- Tiêu chí 5: Các nút xem TKB từ Thẻ GV và Sổ Dạy Thay tự động điều hướng mượt mà sang Tab Thời khóa biểu → PASS

## Bug
Không phát hiện bug.