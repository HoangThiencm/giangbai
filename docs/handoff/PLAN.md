# PLAN: Khắc phục lỗi "getGradeLevel is not defined", Lệch Dropdown PPCT & Triệt tiêu ảo giác "Chiến lược doanh nghiệp / NLS" khi 1-Click Soạn KHBD

## Hiện trạng & Nguyên nhân gốc rễ

### 1. Hiện tượng ảo giác nghiêm trọng (Hallucination) dù đã có thông tin bài Toán
- **Mô tả**: Dù người dùng đã chọn bài "Bài 2: Giải hệ hai phương trình bậc nhất hai ẩn" (Toán 9), hộp thoại xác nhận 1-Click hiện rõ ràng:
  `"Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn" (Lớp 9 - Toán)`
  Nhưng khi bấm "Đồng ý" thì Bước 1 (I. Mục tiêu) lại sinh ra bài viết quản trị kinh doanh:
  `CHIẾN LƯỢC TỐI ƯU HÓA QUY TRÌNH DOANH NGHIỆP DỰA TRÊN CÔNG NGHỆ MỚI`
  `1. PHÂN TÍCH HỆ THỐNG VÀ XỬ LÝ NGÔN NGỮ TỰ NHIÊN (NLS)`
  `2. TÍCH HỢP TRÍ TUỆ NHÂN TẠO (AI) TRONG QUẢN TRỊ VẬN HÀNH`
- **Nguyên nhân cốt lõi**:
  1. **Hiểu nhầm từ viết tắt "NLS"**:
     - Trong giáo dục Việt Nam (CV 3456, TT 02), **NLS** là **Năng lực số** (Digital Competence).
     - Trong kho dữ liệu đào tạo AI quốc tế, LLM (Gemini) tự giải nghĩa **NLS** thành **Natural Language System (Hệ thống xử lý ngôn ngữ tự nhiên)**.
     - Ràng buộc đầu ra (`OUTPUT_CONTRACT`) yêu cầu: `BẮT BUỘC: Các vị trí tích hợp NLS và AI phải được in đậm và in nghiêng (***...***)`. 
     - Khi Gemini thấy bài toán "Giải hệ phương trình" không hề có khái niệm "Xử lý ngôn ngữ tự nhiên (NLS)", mà hợp đồng lại bắt buộc phải có NLS và AI, Gemini bị xung đột nhận thức. Nó tự suy luận rằng NLS (Xử lý ngôn ngữ tự nhiên) + AI (Trí tuệ nhân tạo) chỉ có trong ứng dụng công nghệ doanh nghiệp, nên nó đã vứt bỏ nội dung Toán học và phóng tác ra bài viết tối ưu hóa quy trình doanh nghiệp!
  2. **Lỗi nối dòng trong Prompt OCR SGK**:
     - Tại dòng 7002 file `js/khbd-app.js`, mảng prompt dùng `.join("\\n")` (nối thành chuỗi ký tự gạch chéo n) thay vì `.join("\n")` (xuống dòng thực sự), khiến prompt phân tích SGK bị dồn thành 1 dòng rối rắm.
  3. **Hàm `applyObjectivesOutput` sửa chữa sai lầm bằng `repairWithGemini`**:
     - Khi kiểm tra thấy thiếu mã chuẩn NLS, code gửi prompt: `Sửa đúng một lần phần I. Mục tiêu sau. Giữ nguyên Markdown và các dòng đã có... CẤM xóa dòng đã có`. Chỉ thị này vô tình ép Gemini GIỮ NGUYÊN nội dung ảo giác doanh nghiệp và lưu thẳng vào editor của giáo viên.

---

### 2. Lỗi mất lựa chọn trên Dropdown "DANH MỤC BÀI HỌC" khi chọn từ PPCT
- **Mô tả**: Khi giáo viên chọn bài trong danh mục PPCT (hoặc tab Thông tin bài & Lớp), thanh chọn "DANH MỤC BÀI HỌC" ở trên cùng bị nhảy về `-- Chọn bài học từ SGK --`.
- **Nguyên nhân**:
  - Dữ liệu PPCT lưu tiêu đề dạng dấu chấm: `"Bài 2. Giải hệ hai phương trình bậc nhất hai ẩn"`.
  - Dữ liệu `CURRICULUM_DATA` trong sách giáo khoa lưu tiêu đề dạng dấu hai chấm: `"Bài 2: Giải hệ hai phương trình bậc nhất hai ẩn"`.
  - Khi người dùng chọn dòng PPCT, `applyPpctCatalogRow` gán `appState.selectedLesson = row.title` (dấu chấm) rồi gọi `populateLessonDropdown()`.
  - Trong `populateLessonDropdown()` (dòng 3190), code so sánh trực tiếp: `if (item === appState.selectedLesson) opt.selected = true;`. Do dấu chấm khác dấu hai chấm (`.` !== `:`), điều kiện này bị sai, không có `<option>` nào được chọn, khiến Dropdown ở thanh trên cùng bị reset về `-- Chọn bài học từ SGK --`.

---

### 3. Lỗi Runtime `ReferenceError: getGradeLevel is not defined` & Nút tạo từng mục hoạt động bị "đơ"
- **Mô tả**:
  - Khi bấm nút 1-Click hoặc bấm **"Tạo nội dung mục này"** (`btnGenerateCurrentAct`) trong từng hoạt động A, B, C, D: Nút bấm dường như không hoạt động, không có phản hồi.
- **Nguyên nhân**:
  - `khbd-curriculum.js` tải qua thẻ script động `async`. Nếu mạng trễ hoặc bấm nút trước khi file nạp xong, hàm `getGradeLevel` chưa có trên scope toàn cục.
  - Hàm dự phòng `installCurriculumFallback()` trong các file HTML chỉ mock `CURRICULUM_DATA` mà quên mock `getGradeLevel` và `getGradeLevelName`.
  - Trong `handleGenerateCurrentActivity` (dòng 7624), code gọi `getGenerationPromptContext()` ngay đầu hàm mà không có `try/catch`. Khi `getGenerationPromptContext()` gặp lỗi `ReferenceError: getGradeLevel is not defined`, exception bị văng ra console làm crash hàm xử lý sự kiện click. Người dùng thấy nút bấm hoàn toàn bất động, không hiển thị bất kỳ thông báo lỗi hay thanh tiến trình nào.

---

## Phạm vi giải pháp

### A. Triệt tiêu ảo giác & Khóa chặt môn học / sư phạm
1. **Chuẩn hóa giải nghĩa NLS & Khung hợp đồng**:
   - Thay đổi định nghĩa trong `OUTPUT_CONTRACT` ở `canvas_soankhbd.html`, `canvas_soanbaigiang.html`, `backupcode viettailieu/`:
     Giải thích rõ ràng: **Năng lực số (NLS theo CV 3456/BGDĐT - máy tính cầm tay, GeoGebra, tra cứu bảng số) & Năng lực AI (theo QĐ 2422/BGDĐT)**.
     Nghiêm cấm tuyệt đối Gemini giải nghĩa NLS thành "Xử lý ngôn ngữ tự nhiên" hay văn bản doanh nghiệp, quy trình kinh doanh.
2. **Kỷ luật chủ đề & Môn học (Subject & Pedagogical Discipline Guard)**:
   - Trong `getPromptTemplate('GENERATE_OBJECTIVES', context)` (`js/khbd-prompts.js`) và `buildPedagogicalPrompt` (`js/khbd-app.js`):
     Bổ sung khối cấm tiệt ảo giác:
     `RÀNG BUỘC MÔN HỌC BẮT BUỘC: Kế hoạch bài dạy môn {subjectName}, lớp {grade}, cấp {gradeLevelName}. BÀI DẠY: "{topic}". TUYỆT ĐỐI CẤM soạn văn bản về quản trị doanh nghiệp, quy trình kinh doanh, chăm sóc khách hàng hay công nghệ thông tin thương mại. ĐÂY LÀ GIÁO ÁN PHỔ THÔNG DÀNH CHO HỌC SINH VÀ GIÁO VIÊN.`
3. **Chuẩn hóa Case-insensitive cho Môn học & Fallback an toàn**:
   - Chuẩn hóa `currentSubjectId()` và `appState.selectedSubject`: luôn dùng `toLowerCase()`.
   - Trong `getSystemRole`, `getSubjectCompetencies`, `latexSubjects.includes`: luôn chuyển `subjectId` thành lowercase trước khi so khớp.
   - Thêm hàm `getSubjectDisplayName(subjectId)` chuẩn trong `khbd-app.js` và `canvas_soankhbd.html` để trả về "Toán học" thay vì rơi về "Môn học".
4. **Sửa lỗi so khớp tiêu đề bài học trong `populateLessonDropdown`**:
   - Chuẩn hóa chuỗi so khớp bằng hàm chuẩn hóa dấu câu: `normalizeLessonTitleMatch(str)` loại bỏ dấu chấm/hai chấm sau số thứ tự bài (`Bài 2.` tương đương `Bài 2:`). Giúp Dropdown ở trên luôn đồng bộ đúng bài học khi chọn từ PPCT.
5. **Sửa lỗi ký tự xuống dòng prompt phân tích SGK**:
   - Tại dòng 7002 file `js/khbd-app.js`: Đổi `.join("\\n")` thành `.join("\n")`.
6. **Lọc bỏ nội dung rác trước khi repair trong `applyObjectivesOutput`**:
   - Trước khi gọi `repairWithGemini`, kiểm tra nếu văn bản chứa từ khóa lạc đề (`doanh nghiệp`, `quy trình doanh nghiệp`, `khách hàng`, `phân tích sắc thái`) hoặc không có cấu trúc mục tiêu của CV 5512:
     Hủy bỏ hoàn toàn văn bản lạc đề, không cho phép Gemini "giữ nguyên dòng đã có" của bài viết doanh nghiệp. Tái tạo lại bằng prompt cứng của môn học.

---

### B. Khắc phục dứt điểm lỗi `getGradeLevel is not defined` & Nút tạo từng mục
1. **Bổ sung Defensive Helper trong `js/khbd-app.js`**:
   - Bổ sung `safeGetGradeLevel(grade)` và `safeGetGradeLevelName(grade)` ở đầu file.
   - Thay thế toàn bộ lời gọi trực tiếp `getGradeLevel(...)` và `getGradeLevelName(...)` bằng các hàm an toàn này.
2. **Cập nhật `installCurriculumFallback` trong các file HTML Canvas**:
   - Khai báo đầy đủ `window.getGradeLevel` và `window.getGradeLevelName` với logic phân loại chuẩn CT GDPT 2018 (lớp 1–5: `tieu-hoc`, lớp 6–9: `thcs`, lớp 10–12: `thpt`).
3. **Đồng bộ hóa 1-Click chờ Core Ready**:
   - `await (window.__KHBD_CANVAS_CORE_READY__ || Promise.resolve());` ngay đầu `handle1ClickGenerate`.
4. **Export lên `window` trong `js/khbd-curriculum.js`**:
   - `window.getGradeLevel = getGradeLevel;`
   - `window.getGradeLevelName = getGradeLevelName;`
5. **Bọc phòng vệ `try/catch` & hiển thị Toast khi tạo từng mục**:
   - Trong `handleGenerateCurrentActivity`, `handleGenerateObjectives`, `handleGenerateMaterials`:
     Bọc toàn bộ trong khối `try { ... } catch (err) { hideProgress(); showToast("Lỗi khởi tạo: " + err.message, "danger", 6000); }` để người dùng luôn biết rõ nguyên nhân, không bao giờ xảy ra tình trạng nút bị đơ im lặng.

---

## File tác động
1. `js/khbd-app.js`
2. `js/khbd-prompts.js`
3. `js/khbd-curriculum.js`
4. `canvas_soankhbd.html`
5. `canvas_soanbaigiang.html`
6. `backupcode viettailieu/canvas_soankhbd.html`
7. `backupcode viettailieu/canvas_soanbaigiang.html`
8. `tests/canvas-module-fallback-smoke.js`
9. `tests/canvas-soankhbd-smoke.js`
10. `tests/khbd-nls-ai-bold-italic-smoke.js`

---

## Tiêu chí nghiệm thu (Acceptance Criteria)
1. Chọn bài học từ PPCT thì Dropdown **DANH MỤC BÀI HỌC** ở thanh trên cùng tự động đồng bộ và giữ nguyên tên bài, không bị nhảy về `-- Chọn bài học từ SGK --`.
2. Bấm 1-Click Soạn KHBD với bài Toán 9 (Bài 2), kết quả Mục tiêu và các hoạt động phải 100% là Toán học THCS (Phương pháp thế, giải hệ phương trình, máy tính cầm tay...), tuyệt đối KHÔNG có từ ngữ nào về doanh nghiệp/quản trị.
3. Bấm nút **"Tạo nội dung mục này"** ở bất kỳ hoạt động nào (A, B, C, D, E) đều phản hồi ngay lập tức, có thanh tiến trình và thông báo kết quả, không bị đơ im lặng.
4. Bấm 1-Click Soạn KHBD chạy ổn định 100%, không xuất hiện lỗi `ReferenceError: getGradeLevel is not defined`.
5. Toàn bộ smoke test suites chạy `node tests/...` đạt kết quả PASS 100%.
