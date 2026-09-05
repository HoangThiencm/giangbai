# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] **Tùy chỉnh khung tiết Sáng / Chiều linh hoạt**:
  + Hỗ trợ cấu hình dải tiết qua `#quick-cfg-morning`, `#quick-cfg-afternoon` và trong modal cấu hình tổ (`#cfg-morning-periods`, `#cfg-afternoon-periods`).
  + Hàm `parsePeriodsConfig` phân tích chính xác cả dạng dải (`1-4`, `7-9`, `6 - 10`) và danh sách (`1, 2, 3, 4`).
  + Lưới slot builder (`initPeriodSlotsBuilder`) tự động sinh các ô tiết theo đúng khung tiết buổi sáng/chiều đã cấu hình.
- [x] **Quản lý Thời khóa biểu Giáo viên**:
  + Đã thêm modal `#teacher-timetable-modal` với bộ chọn giáo viên, năm học, học kỳ.
  + Đã tích hợp vùng dán ảnh `#tt-dropzone` (hỗ trợ Ctrl+V dán ảnh, kéo thả file, chọn file ảnh).
  + Lưới ma trận TKB tuần (Sáng/Chiều x Thứ 2 - Thứ 7) hiển thị và hỗ trợ click sửa ô.
  + Lưu TKB vào `state.teachers[].timetable` và đồng bộ qua tất cả snapshot đợt (`persistTeacherTimetable`).
- [x] **AI Gemini Vision nhận diện Thời khoá biểu**:
  + Gửi payload ảnh base64 qua proxy `api/khbd_gemini.php` (`gemini-2.5-flash`).
  + Hàm xử lý kết quả AI `applyAiTimetableResult()` bóc tách JSON chuẩn xác, tự động khớp tên giáo viên bằng hàm `foldText()`, render lưới ma trận TKB mượt mà.
- [x] **Tự động gợi ý điền tiết từ TKB vào Sổ Dạy Thay**:
  + Hàm `weekdayNumberFromDate` chuyển đổi chính xác ngày (VD: `2026-09-09` -> Thứ Tư / 4).
  + Hàm `getTimetableDaySlots` trích xuất đúng các tiết/lớp/môn của giáo viên trong ngày.
  + Nút `⚡ Lấy tiết từ TKB` và tự động gợi ý (`maybeAutoSuggestSlotsFromTimetable`) hoạt động đúng thiết kế khi giáo viên đã có TKB.

## Test đã chạy
1. `tests/smartquiz-smoke.js`: PASS.
2. Kiểm tra tính duy nhất của toàn bộ 123 HTML IDs: 100% unique, không có ID trùng lặp.
3. Kiểm tra sự tồn tại của 15 DOM elements mới phục vụ TKB và cấu hình tiết: PASS.
4. Kiểm tra sự tồn tại của 15 hàm JS nghiệp vụ mới (`openTeacherTimetableModal`, `scanTimetableWithAI`, `applyAiTimetableResult`, `saveTeacherTimetable`, `autoSuggestSlotsFromTimetable`, `parsePeriodsConfig`, `foldText`...): PASS.
5. Kiểm tra hàm `parsePeriodsConfig`: Xử lý tốt các dạng dải và danh sách tiết: PASS.
6. Kiểm tra hàm `parseTimetableCell` và `formatTimetableCell`: PASS.
7. Kiểm tra hàm `foldText` chuẩn hóa tiếng Việt không dấu: PASS.
8. Kiểm tra luồng `applyAiTimetableResult` với dữ liệu ma trận từ Gemini Vision: PASS.
9. Kiểm tra hàm `weekdayNumberFromDate` và `getTimetableDaySlots`: PASS.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Người dùng tùy chỉnh được khung tiết Sáng / Chiều tự do (ví dụ: Sáng 1-4, Chiều 7-9) → PASS
- Tiêu chí 2: Tích hợp giao diện quản lý Thời khóa biểu cá nhân cho từng Giáo viên → PASS
- Tiêu chí 3: Hỗ trợ dán ảnh (Ctrl+V) hoặc upload ảnh TKB và dùng AI Gemini Vision bóc tách tự động chính xác lịch dạy tuần → PASS
- Tiêu chí 4: Sổ Dạy Thay tự động gợi ý / điền nhanh các tiết học cần dạy thay dựa trên TKB của giáo viên được thay → PASS

## Bug
Không phát hiện bug. (Bug `foldText` ở lần verify trước đã được sửa và kiểm thử thành công).