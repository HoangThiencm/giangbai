# PLAN: Khắc phục triệt để lỗi "getGradeLevel is not defined" gây chập chờn khi 1-Click Soạn KHBD

## Hiện trạng
1. **Lỗi Runtime**:
   ```text
   [CONSOLE_ERROR] 1-Click Generate Error: Error: getGradeLevel is not defined
   Stack: ReferenceError: getGradeLevel is not defined
       at getGenerationPromptContext (https://hoangthiencm.id.vn/js/khbd-app.js:...)
       at executeStep (...)
       at HTMLButtonElement.handle1ClickGenerate (...)
   ```
2. **Nguyên nhân gốc rễ (Tại sao lúc tạo được, lúc báo lỗi?)**:
   - **Hiện tượng Race Condition (Tranh chấp thời gian tải mạng)**:
     * Trong `canvas_soankhbd.html` (và `canvas_soanbaigiang.html`), module `js/khbd-curriculum.js` được tải từ hosting qua thẻ script động có cờ `node.async = true;`.
     * Khi mạng nhanh: `khbd-curriculum.js` tải xong trước khi người dùng bấm 1-Click → Hàm `getGradeLevel` có sẵn → Chạy thành công.
     * Khi mạng chậm, hosting phản hồi trễ hoặc người dùng bấm 1-Click ngay sau khi mở trang: `khbd-curriculum.js` chưa kịp nạp xong → Gây lỗi `ReferenceError: getGradeLevel is not defined`.
   - **Thiếu sót trong hàm Fallback (`installCurriculumFallback`)**:
     * Khi kết nối hosting quá 8 giây hoặc tải file lỗi, hàm `installCurriculumFallback()` tự động kích hoạt để tạo dữ liệu dự phòng.
     * Tuy nhiên, `installCurriculumFallback()` chỉ mock `CURRICULUM_DATA`, `getCurriculumLessons`, `getSubjectsForGrade`... mà **hoàn toàn bỏ quên `getGradeLevel` và `getGradeLevelName`**.
   - **`js/khbd-curriculum.js` không gán tường minh lên `window`**:
     * File chỉ gán `window.CURRICULUM_DATA` và `window.SUBJECT_COMPETENCIES`, không gán `window.getGradeLevel = getGradeLevel` và `window.getGradeLevelName = getGradeLevelName`.
   - **`js/khbd-app.js` gọi trần trụi thiếu phòng vệ**:
     * Tại các dòng 5095, 5193, 5194, code gọi trực tiếp `getGradeLevel(appState.selectedGrade)` và `getGradeLevelName(appState.selectedGrade)` mà không có `typeof` kiểm tra hay hàm fallback nội bộ.

## Phạm vi
1. **Bổ sung hàm phòng vệ nội bộ (Defensive Helper) trong `js/khbd-app.js`**:
   - Tạo 2 hàm chuẩn hóa an toàn `safeGetGradeLevel(grade)` và `safeGetGradeLevelName(grade)` ngay trong `khbd-app.js`:
     * Kiểm tra `typeof getGradeLevel === "function"` hoặc `window.getGradeLevel`.
     * Nếu không có, tự phân loại chuẩn xác theo CT GDPT 2018:
       - Lớp 1–5: `tieu-hoc` / "Tiểu học"
       - Lớp 6–9: `thcs` / "THCS"
       - Lớp 10–12: `thpt` / "THPT"
       - Mặc định: `thcs` / "THCS"
   - Thay thế toàn bộ các lời gọi `getGradeLevel` và `getGradeLevelName` trong `js/khbd-app.js` bằng 2 hàm an toàn này.
2. **Cập nhật `installCurriculumFallback` trong các file HTML Canvas**:
   - Khai báo bổ sung `window.getGradeLevel` và `window.getGradeLevelName` ngay trong `installCurriculumFallback()` của:
     * `canvas_soankhbd.html`
     * `canvas_soanbaigiang.html`
     * `backupcode viettailieu/canvas_soankhbd.html`
     * `backupcode viettailieu/canvas_soanbaigiang.html`
3. **Cập nhật `handle1ClickGenerate` chờ Core Modules sẵn sàng**:
   - Thêm `await (window.__KHBD_CANVAS_CORE_READY__ || Promise.resolve());` ngay đầu hàm `handle1ClickGenerate` trước khi thực thi các bước soạn, đảm bảo không có race condition dù người dùng bấm nút cực nhanh.
4. **Cập nhật `js/khbd-curriculum.js`**:
   - Đảm bảo gán rõ ràng `window.getGradeLevel = getGradeLevel;` và `window.getGradeLevelName = getGradeLevelName;` khi chạy trên môi trường trình duyệt.
5. **Kiểm thử tự động**:
   - Cập nhật và chạy smoke test `tests/canvas-soankhbd-smoke.js` và `tests/canvas-module-fallback-smoke.js` để đảm bảo 100% PASS khi có hoặc không có mạng.

## Ngoài phạm vi
- Không làm thay đổi logic sinh kịch bản hay các hợp đồng prompt khác.
- Không thay đổi các biến state của giáo án.

## File dự kiến tác động
- `js/khbd-app.js`
- `js/khbd-curriculum.js`
- `canvas_soankhbd.html`
- `canvas_soanbaigiang.html`
- `backupcode viettailieu/canvas_soankhbd.html`
- `backupcode viettailieu/canvas_soanbaigiang.html`
- `tests/canvas-module-fallback-smoke.js`
- `tests/canvas-soankhbd-smoke.js`

## Các bước thực hiện
1. **Bước 1: Cập nhật `js/khbd-app.js`**:
   - Thêm hàm `safeGetGradeLevel(grade)` và `safeGetGradeLevelName(grade)`.
   - Thay thế các vị trí gọi `getGradeLevel` và `getGradeLevelName` tại dòng 5095, 5193, 5194.
2. **Bước 2: Cập nhật `js/khbd-curriculum.js`**:
   - Export lên `window` các hàm cấp học: `window.getGradeLevel = getGradeLevel; window.getGradeLevelName = getGradeLevelName;`.
3. **Bước 3: Cập nhật Fallback & 1-Click trong `canvas_soankhbd.html` & `canvas_soanbaigiang.html`**:
   - Bổ sung định nghĩa `getGradeLevel` và `getGradeLevelName` vào `installCurriculumFallback()`.
   - Thêm `await (window.__KHBD_CANVAS_CORE_READY__ || Promise.resolve());` trong `handle1ClickGenerate()`.
   - Đồng bộ vào thư mục `backupcode viettailieu/`.
4. **Bước 4: Kiểm thử tự động**:
   - Chạy `node tests/canvas-module-fallback-smoke.js`.
   - Chạy `node tests/canvas-soankhbd-smoke.js`.

## Rủi ro & Cách phòng tránh
- **Rủi ro**: Script tải từ hosting chưa xong khi chạy offline hoặc mạng chập chờn.
- **Phòng tránh**: Nhờ hàm phòng vệ nội bộ `safeGetGradeLevel` ngay trong `khbd-app.js` cùng `installCurriculumFallback()`, hệ thống sẽ hoạt động ổn định 100% mà không bao giờ phụ thuộc vào tốc độ tải mạng của `khbd-curriculum.js`.

## Cách kiểm thử
- Chạy `node tests/canvas-module-fallback-smoke.js`.
- Mô phỏng offline/ngắt kết nối `khbd-curriculum.js`: gọi `getGenerationPromptContext()` đảm bảo trả về đầy đủ `gradeLevel: "thcs"` và `gradeLevelName: "THCS"` mà không bắn ra bất kỳ exception nào.

## Tiêu chí nghiệm thu
1. 1-Click Soạn KHBD chạy mượt mà ngay khi vừa mở trang hoặc mạng chập chờn, không bao giờ xuất hiện lỗi `ReferenceError: getGradeLevel is not defined`.
2. Mọi trường hợp fallback đều có đầy đủ thông tin cấp học `gradeLevel` và `gradeLevelName`.
3. Toàn bộ test suites tự động PASS 100%.
