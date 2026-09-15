# IMPLEMENT: Tách Riêng Các Môn Lịch Sử, Địa Lí, Vật Lí, Hoá Học, Sinh Học & Bỏ Qua Ràng Buộc Tổng Số Tiết

## Phạm vi đã triển khai

### 1. Dữ liệu chuẩn THCS (`js/khbd-curriculum.js` & `agent-tools/thcs-toc.json`)
- Đăng ký 5 môn học độc lập mới:
  - `{ id: 'lichsu', name: 'Lịch sử', grades: [6, 7, 8, 9] }`
  - `{ id: 'diali', name: 'Địa lí', grades: [6, 7, 8, 9] }`
  - `{ id: 'vatli', name: 'Vật lí', grades: [6, 7, 8, 9] }`
  - `{ id: 'hoahoc', name: 'Hoá học', grades: [6, 7, 8, 9] }`
  - `{ id: 'sinhhoc', name: 'Sinh học', grades: [6, 7, 8, 9] }`
- Nạp danh mục bài học chuẩn xác 100% từ SGK Thống nhất (theo đúng thứ tự chương, bài, số tiết và gợi ý mã NLS/AI):
  - **Lịch sử**: Khối 6 (20 bài), Khối 7 (20 bài), Khối 8 (21 bài), Khối 9 (25 bài).
  - **Địa lí**: Khối 6 (31 bài), Khối 7 (21 bài), Khối 8 (14 bài), Khối 9 (24 bài).
  - **Vật lí**: Khối 6 (23 bài), Khối 7 (14 bài), Khối 8 (17 bài), Khối 9 (16 bài).
  - **Hoá học**: Khối 6 (9 bài), Khối 7 (6 bài), Khối 8 (12 bài), Khối 9 (18 bài).
  - **Sinh học**: Khối 6 (22 bài), Khối 7 (22 bài), Khối 8 (18 bài), Khối 9 (16 bài).
- Duy trì song song môn ghép `khtn` (140 tiết) và `lichsudialy` (105 tiết) để bảo đảm tính tương thích ngược hoàn hảo.
- Tuân thủ quy tắc không xuất hiện nhãn tên bộ sách.

### 2. Giao diện & Công cụ Kế hoạch Giáo dục (`canvas_xaydungphuluc.html` & `xaydungphuluc.html`)
- Cấu hình số tiết trong menu môn học (`SUBJECTS`):
  - Lịch sử: 52 tiết/năm
  - Địa lí: 53 tiết/năm
  - Vật lí: 47 tiết/năm
  - Hoá học: 43 tiết/năm
  - Sinh học: 50 tiết/năm
  - Khoa học tự nhiên: 140 tiết/năm
  - Lịch sử và Địa lí: 105 tiết/năm
- Cập nhật chuẩn hóa chuỗi và nhận diện môn:
  - `getSubjectCurriculumKey()`: Phân tách rõ ràng giữa `vatli/ly`, `hoahoc/hoa`, `sinhhoc/sinh`, `lichsu`, `diali/dia ly`, `khtn`, `lichsudialy`.
  - `detectGradeAndSubjectFromFileName()`: Nhận diện chính xác tên môn từ file tải lên.
  - `getStandardSubjectYccd()`: Tạo câu YCCĐ chuẩn cho riêng từng phân môn.
  - `EQUIPMENT`: Bổ sung thiết bị dạy học chuyên biệt cho từng phân môn.
  - `SUBJECT_SAMPLE_TOPICS`: Bổ sung chuyên đề/CLB ngoại khóa trải nghiệm phù hợp cho từng môn.
  - `nlsSubjectToolkit` & `lessonAppliedAiFallback`: Thiết lập công cụ số và prompt AI sư phạm riêng biệt cho từng môn.

### 3. Cơ chế Bỏ qua ràng buộc tổng số tiết & Linh hoạt thời lượng
- **Nút tick Bỏ qua ràng buộc tổng số tiết (`#ignoreTotalPeriods` & `#ignoreTotalPeriodsSection3`)**:
  - Mặc định được tick chọn (`checked = true`).
  - Đồng bộ hai chiều giữa Mục 1 (Thông tin trường học) và Mục 3 (Cấu hình NLS & AI) thông qua hàm `syncIgnoreTotalPeriods(checked)`.
- **Ô nhập tùy chọn Số tiết/năm (`#customAnnualPeriods`)**:
  - Bổ sung vào Mục 1 thành lưới 12 ô hoàn hảo. Giáo viên có thể nhập số tiết năm thực tế của trường mình (ví dụ 48, 50, 52, 54...) hoặc để trống dùng mặc định môn.
- **Thẩm định sư phạm linh hoạt (`calculateComplianceReport`)**:
  - Khi bật bỏ qua: tiêu chí "Thời lượng chương trình" luôn đạt chuẩn `pass = (periods > 0)`, căn cứ "Phân phối nhà trường / Linh hoạt", báo cáo thẩm định đạt **100% ĐẠT CHUẨN** không bị chặn bởi số tiết lệch chuẩn.
  - Khi tắt bỏ qua: đối chiếu nghiêm ngặt `periods === expected`.
- **Phân bổ thời lượng thích ứng (`defaultPpctRows`, `periodsPerWeekForSubject`)**:
  - Nhận diện `customAnnualPeriods` khi sinh bảng mẫu hoặc tính số tiết/tuần.
  - Giữ nguyên số tiết cố định `entry.periods` nếu có trong danh mục.
  - NLS và AI tính toán theo tổng số tiết thực tế của bảng PPCT hiện tại.
- **Bảo lưu cấu hình trong bản nháp (`getConfig`, `applyDraftConfig`)**:
  - Tự động lưu và khôi phục `ignoreTotalPeriods` và `customAnnualPeriods` khi lưu/tải bản nháp trên trình duyệt và CSDL máy chủ.

### 4. Khắc phục lỗi nạp nhầm môn Địa lí 8 & Chuẩn hóa Kho Tri thức SGK dùng chung
- **Nguyên nhân gốc rễ**:
  1. Trong JS, `String.prototype.normalize('NFD')` không phân rã chữ `Đ`/`đ` (`\u0110`, `\u0111`). Khi chạy `foldText('Địa lí')`, kết quả trả về là `'ĐIA LI'`.
  2. Hàm `getSubjectCurriculumKey()` dùng regex `/dia[ _-]*(?:li|ly)/i` kiểm tra chuỗi ASCII `d`, không khớp với `Đ`.
  3. Hàm thiếu các nhánh phân môn `vatli`, `hoahoc`, `sinhhoc` và rơi vào nhánh cuối cùng `return 'toan'`.
  4. Quá trình kiểm thử/seed trước đây đã vô tình lưu 39 bài Toán 8 vào cuốn sách Địa lí 8 (Book ID 65).
  5. Các cuốn Giáo dục địa phương (ID 27, 39, 51, 63) cũng gặp lỗi tương tự do `ĐIA PHUONG`.
- **Giải pháp xử lý triệt để**:
  1. **Cập nhật Client (`canvas_xaydungphuluc.html` & `xaydungphuluc.html`)**:
     - Cập nhật hàm `foldText(s)`: thêm `.replace(/[đĐ]/g, 'D')`.
     - Cập nhật `getSubjectCurriculumKey(subjectName)`: chuẩn hóa chuỗi không dấu, kiểm tra `diali` trước `vatli` (tránh regex `\bli\b` của Vật lí nuốt mất chữ `lí` trong `Địa lí`), hỗ trợ đầy đủ `lichsu`, `diali`, `vatli`, `hoahoc`, `sinhhoc`, `gddp`.
     - Cập nhật `detectGradeAndSubjectFromFileName()`: dùng chung logic nhận diện môn chuẩn xác.
     - Bổ sung cơ chế phòng vệ Auto-purge Cache: nếu môn học không phải Toán nhưng các bài học chứa từ khóa đặc trưng môn Toán (đơn thức, đa thức, số vô tỉ...), Client sẽ tự động thanh lọc bộ nhớ cache và kéo bản danh mục chuẩn mới nhất từ hệ thống.
  2. **Dọn sạch & Nạp mới 100% CSDL Hosting (`https://hoangthiencm.id.vn/api/sgk_knowledge.php`)**:
     - Xóa Book ID 65 (Địa lí 8 nạp nhầm bài Toán).
     - Xóa các Book ID 27, 39, 51, 63 (GDDP nạp nhầm bài Toán).
     - Tạo mới Book ID 66: Địa lí 8 chuẩn xác 14 bài của CTGDPT 2018 (bắt đầu bằng *Bài 1: Vị trí địa lí và phạm vi lãnh thổ Việt Nam*).
     - Nạp mới và kiểm tra toàn diện 100% các môn Lịch sử (khối 6-9), Địa lí (khối 6-9), Vật lí (khối 6-9), Hoá học (khối 6-9), Sinh học (khối 6-9), Giáo dục địa phương (khối 6-9).

### 5. Cổng học tập học sinh & Phân quyền giao diện User (`login.html`, `index.html`, `access-control.js`)
- **Vấn đề trước đây**:
  - Khi học sinh đăng nhập, hàm `landingPageFor()` trong `login.html` tự động ép chuyển hướng thẳng vào một trang lộ trình cố định (vd: `lotrinhtoan6.html` hoặc `primary`), khiến học sinh bị cô lập bên trong lộ trình mà không thể mở các chức năng khác được giao (Thi trực tuyến, Giao & nộp bài, Padlet, SmartQuiz...).
  - Trang chủ `index.html` cũng có đoạn mã ép đá học sinh sang lộ trình bài học ở đầu trang. Nếu truy cập vào `index.html`, học sinh lại thấy toàn bộ công cụ của giáo viên (Soạn KHBD, Xây dựng phụ lục, Duyệt đề, Sổ điểm, Quản lý văn bản, Cài đặt AI & Key...).
- **Giải pháp triển khai**:
  1. **`login.html`**:
     - `landingPageFor(user)`: Với role `student`, trả về `index.html` (Cổng học tập học sinh) thay vì ép nhảy thẳng vào lộ trình bài học.
  2. **`index.html`**:
     - Xóa bỏ đoạn mã ép chuyển hướng học sinh ở đầu trang.
     - Bổ sung cấu trúc giao diện User riêng biệt `#studentPortalDeck` với Tailwind CSS hiện đại:
       + Welcome Banner: Lời chào thân thiện, tên học sinh, lớp học.
       + Khối Lộ trình tự học Toán: Lọc hiển thị chính xác các khối lớp Toán mà học sinh được phân quyền (`lotrinhtoan4` đến `lotrinhtoan9`).
       + Khối Hoạt động & Tiện ích học tập: Lọc hiển thị chính xác các chức năng được cấp quyền trong `allowed_pages` (`thitructuyen`, `nopbai`, `padlet`, `smartquiz`, `gslides`, `vehinh`).
       + Trạng thái chờ: Nếu học sinh chưa có quyền nào, hiển thị thông báo hướng dẫn liên hệ giáo viên.
     - Hàm `setupStudentPortal(allowedPages)`:
       + Ẩn toàn bộ giao diện và công cụ giáo viên (`#toolsDeck`, `#teacherLotrinhHub`, `#defaultToolsHeader`, accordion hướng dẫn nhanh, nút "Cài đặt AI & Key"...).
       + Đổi tiêu đề Navbar thành: *CỔNG HỌC TẬP VÀ RÈN LUYỆN CHO HỌC SINH*, hiển thị rõ tên học sinh và lớp, badge *Cổng Học Sinh*.
     - Giữ nguyên vẹn 100% logic không gian làm việc cho role `teacher`.
   3. **`access-control.js` & `lotrinh.js`**:
      - Bổ sung danh sách toàn bộ các trang công cụ chỉ dành cho giáo viên (`soankhbd`, `xaydungphuluc`, `duyetgiaoan`, `duyetde`, `nghiencuubaihoc`, `matrande`, `tronde`, `kttx`, `sodiem`, `phancongtochuyenmon`, `thoikhoabieu`, `thongketientrinh`, `theodoiai`, `quanlyvanban`, `rutgon`, `vietbaocao`, `thanhtich`, `taovideo`).
      - Khi role là `student`, nếu cố tình truy cập vào bất kỳ trang nào của giáo viên hoặc trang chưa được cấp quyền, hệ thống sẽ chặn lại ngay và điều hướng về `index.html` (Trang chủ học sinh).
      - Áp dụng Route Guard cho cả giáo viên: chỉ mở được các khối Lộ trình Toán có trong `allowedPages`.
      - Khóa chặn toàn diện bằng universal route guard: bất kỳ user nào truy cập vào trang không có trong `allowedPages` sẽ bị chặn và điều hướng về `index.html`.
      - `lotrinh.js`: Cập nhật chuyển hướng dự phòng khi không được cấp quyền Toán từ `login.html` thành `index.html`.

### 6. Khóa chặn bảo mật Đặc quyền tối thiểu toàn diện (Universal Least-Privilege Route Guards)
- Nhúng `<script src="access-control.js"></script>` vào 100% tất cả 34 file HTML nghiệp vụ trong hệ thống (bao gồm `canvas_xaydungphuluc.html`, `giaoantichhop.html`, `nopbai.html`, `trochoi.html`, `taobaitap.html`, `matrande copy.html`, và 8 minigames `game-*.html`).
- Đăng ký đầy đủ ánh xạ `pageKey` cho tất cả các trang phụ và minigames về quyền cha tương ứng (ví dụ: `game-*.html` -> `smartquiz`).
- Đảm bảo người dùng (kể cả học sinh hay giáo viên) không thể vượt quyền bằng cách gõ trực tiếp URL thanh địa chỉ trình duyệt.

### 7. Kiểm thử & Đảm bảo chất lượng
- Kiểm thử toàn diện 100% pass:
  - `verify_patch.py`: Kiểm tra giao diện, logic nút tick bỏ qua tổng số tiết, cấu trúc dữ liệu trên cả `canvas_xaydungphuluc.html` và `xaydungphuluc.html`.
  - `verify_period_bypass.py`: Kiểm tra tính toán thẩm định sư phạm với nhiều mức tiết khác nhau (48, 50, 52, 53, 54 tiết).
  - `verify_all_subjects_catalog.py`: Kiểm tra live API cho Địa lí 8 và kiểm thử 32 trường hợp chuỗi tên môn trong Javascript.
  - `audit_server_books.py`: Quét toàn bộ 52 đầu sách trên server hosting live, phát hiện: **0 sách bị nhiễm bẩn** (`Total contaminated books found: 0`).
  - `test_smoke_contracts.py`: Đảm bảo 100% hợp đồng phân quyền giáo viên theo nguyên tắc đặc quyền tối thiểu (least privilege) không bị ảnh hưởng.
  - `test_student_portal.py`: Kiểm thử chuyển hướng đăng nhập học sinh, kiểm thử route guard của `access-control.js`, kiểm thử rendering Cổng học sinh phân quyền trên `index.html` (3/3 PASSED).
  - `test_strict_permissions.py`: Kiểm thử toàn diện 34 file HTML nghiệp vụ đều được bảo vệ bởi `access-control.js` và có ánh xạ quyền hợp lệ (34/34 PASSED).
  - Toàn bộ bài test PASSED.

### 8. Khắc phục workflow deploy
- Sửa dấu đóng ngoặc nhọn thừa ngay trước khóa gdcd trong js/khbd-curriculum.js. Lỗi cú pháp này là nguyên nhân javascript-obfuscator dừng với Unexpected token khi workflow deploy chạy.
