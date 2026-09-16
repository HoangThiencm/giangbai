# PLAN: Hoàn thiện Triệt để `canvas_soanbaigiang.html` — Đọc SGK Thật & Sinh Bài Giảng Trình Chiếu AI Thật 100%

## Hiện trạng & Nguyên nhân gốc rễ (Root Cause)

1. **Lỗi tải script `js/khbd-slides.js` trên Gemini Canvas**:
   - Trong `canvas_soanbaigiang.html` (dòng 1426), code đang dùng:
     `document.write('<script src="js/khbd-slides.js"><\/script>');`
   - Khi chạy trong môi trường Gemini Canvas (`gemini.google.com`), trình duyệt hiểu đây là đường dẫn tương đối và cố tải từ `https://gemini.google.com/app/js/khbd-slides.js` $\rightarrow$ gặp lỗi 404.
   - Hậu quả: Toàn bộ module `KhbdSlides` và hàm `generateAiLessonSlides()` không bao giờ được nạp vào Canvas, khiến các nút tạo slide bị tê liệt hoặc undefined.

2. **Nút 1-Click trong `canvas_soanbaigiang.html` vẫn đang chạy luồng Soạn KHBD (Giáo án Word)**:
   - Trong `handle1ClickGenerate()` của `canvas_soanbaigiang.html` (dòng 1826–1915), mã nguồn vẫn đang lần lượt gọi:
     + I. Mục tiêu (`GENERATE_OBJECTIVES`)
     + II. Thiết bị & Học liệu (`GENERATE_MATERIALS`)
     + III.A Khởi động (`GENERATE_ACTIVITY_A`)
     + III.B Hình thành kiến thức (`GENERATE_ACTIVITY_B`)
     + III.C Luyện tập (`GENERATE_ACTIVITY_C`)
     + III.D Vận dụng (`GENERATE_ACTIVITY_D`)
     + III.E Hồ sơ học tập (`GENERATE_PORTFOLIO_WORKSHEETS`)
   - Đây là luồng tạo bảng Word 2 cột của `canvas_soankhbd.html`. Khi chạy trên `canvas_soanbaigiang.html`, các thẻ editor/preview này không khớp hoặc không đúng mục đích của Bài giảng trình chiếu.
   - Hậu quả: Không hề gọi AI để nhận diện bài và sinh bài giảng trình chiếu.

3. **Khâu nhận diện bài học SGK chưa tự động kích hoạt**:
   - Khi người dùng tải ảnh/PDF bài học lên nhưng chưa bấm nút "Phân tích SGK", luồng 1-Click kiểm tra `hasCurrentTextbookOcrContext()` và ném lỗi dừng lại thay vì tự động gọi `readTextbookWithMistral` / `analyzeCanvasTextbookSafely` để đọc SGK rồi sinh slide luôn.

---

## Phạm vi thực hiện cho Coder

### 1. Nhúng trực tiếp toàn bộ logic `khbd-slides.js` vào `canvas_soanbaigiang.html`
- **File**: `canvas_soanbaigiang.html`, `backupcode viettailieu/canvas_soanbaigiang.html`.
- **Giải pháp**:
  - Không nạp `js/khbd-slides.js` qua `document.write` tương đối.
  - Nhúng trực tiếp (inline) toàn bộ mã nguồn của `js/khbd-slides.js` (hoặc fallback đầy đủ của `KhbdSlides` và `generateAiLessonSlides`) vào bên trong `canvas_soanbaigiang.html`.
  - Đảm bảo 100% khi chạy trên Gemini Canvas, đối tượng `window.KhbdSlides` luôn sẵn sàng hoạt động mà không phụ thuộc file ngoài.

### 2. Tái cấu trúc 100% nút 1-Click thành "TẠO BÀI GIẢNG TRÌNH CHIẾU AI":
- **File**: `canvas_soanbaigiang.html`, `backupcode viettailieu/canvas_soanbaigiang.html`.
- **Luồng hoạt động chuẩn của nút 1-Click**:
  1. **Bước 1 (Đọc SGK)**: Kiểm tra nếu có file ảnh/PDF mà chưa phân tích $\rightarrow$ Tự động gọi `readTextbookWithMistral` / `analyzeCanvasTextbookSafely` để nhận diện Bài học thật, Khối lớp, Môn học, Đề mục kiến thức và bài tập từ SGK.
  2. **Bước 2 (Sinh Slide AI)**: Gọi `KhbdSlides.generateAiLessonSlides()` với model `gemini-3-flash-preview`:
     - Truyền toàn bộ ngữ cảnh bài học thực tế vừa bóc tách.
     - Yêu cầu AI trả về JSON kịch bản 15–25 slide (Title, Khởi động, Khám phá từng mục, Quy tắc đóng khung, Ví dụ mẫu giải từng bước KaTeX, Luyện tập, Vận dụng).
  3. **Bước 3 (Hiển thị & Sẵn sàng xuất PPTX)**:
     - Render ngay lập tức toàn bộ slide deck vào khung chiếu 16:9.
     - Kích hoạt tab Trình chiếu bài giảng và bật nút xuất file PowerPoint `.pptx`.
  - **LOẠI BỎ TOÀN BỘ 7 BƯỚC SOẠN GIÁO ÁN KHBD WORD TRONG FILE NÀY**.

### 3. Đồng bộ giao diện & Trình chiếu 16:9
- Khi nạp bài học từ SGK: Tự động cập nhật tiêu đề bài học lên Header và thanh tiêu đề slide.
- Khung trình chiếu render công thức Toán bằng KaTeX chuẩn nét, nút Previous / Next / F5 Toàn màn hình và click chuột chuyển bước hoạt động mượt mà.
- Nút "Tải file PowerPoint (.pptx)" tạo file `.pptx` chuẩn từ deck AI vừa sinh.

---

## File dự kiến tác động
- `canvas_soanbaigiang.html`
- `backupcode viettailieu/canvas_soanbaigiang.html`
- `js/khbd-slides.js`
- `tests/canvas-soanbaigiang-smoke.js`

---

## Các bước thực hiện chi tiết
1. Nhúng nội dung `js/khbd-slides.js` vào thẻ `<script>` bên trong `canvas_soanbaigiang.html` và `backupcode viettailieu/canvas_soanbaigiang.html`.
2. Viết lại hàm `handle1ClickGenerate()` trong `canvas_soanbaigiang.html`:
   - Nếu chưa có OCR context mà có media SGK $\rightarrow$ chạy phân tích SGK trước (`readTextbookWithMistral`).
   - Gọi `generateAiLessonSlides()` sinh kịch bản JSON slide từ Gemini.
   - Render deck vào giao diện trình chiếu 16:9.
3. Kiểm tra nút "Phân tích SGK" (`btnAnalyzeVision`): Đảm bảo khi bấm riêng nút này cũng phân tích đầy đủ và điền đúng Tên bài, Môn, Khối lớp.
4. Cập nhật test `tests/canvas-soanbaigiang-smoke.js` kiểm tra đầy đủ luồng 1-click tạo slide và xuất PPTX.

---

## Tiêu chí nghiệm thu
1. Mở `canvas_soanbaigiang.html` trên Gemini Canvas: không bị lỗi 404 nạp `khbd-slides.js`.
2. Tải ảnh hoặc PDF SGK lên và bấm "TẠO BÀI GIẢNG TRÌNH CHIẾU AI (1-CLICK)":
   - Tự động gọi Gemini phân tích SGK ra đúng Tên bài và các Đề mục.
   - Tự động gọi Gemini sinh 15–25 slide bám sát bài học thật.
   - Tự động chuyển sang khung chiếu 16:9 có hiệu ứng từng bước và công thức toán KaTeX.
3. Nút xuất PowerPoint `.pptx` tải về file trình chiếu bài giảng thật.
4. Tuyệt đối không đụng vào `canvas_soankhbd.html`.
5. 100% test suites PASS.
