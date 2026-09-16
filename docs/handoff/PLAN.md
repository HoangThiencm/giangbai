# PLAN: Hoàn thiện `canvas_soanbaigiang.html` — Kế thừa 100% Luồng Đọc SGK Thật của `canvas_soankhbd` & Sinh Bài Giảng AI Thật (Không Mock/Demo)

## Phản ánh của Người dùng & Hiện trạng

1. **Vấn đề thực tế**:
   - Hiện tại file `canvas_soanbaigiang.html` mới chỉ có giao diện vỏ demo, module `js/khbd-slides.js` đang dùng regex cắt chuỗi thô sơ và fallback các câu mẫu chung chung ("Quan sát tình huống trong SGK...", "Ví dụ mẫu trong SGK..."), không gọi AI thật.
   - Khi người dùng tải tài liệu SGK (như Bài 5) lên, hệ thống không đọc và trích xuất được ngữ cảnh thực của bài mà điền thông tin tào lao / rỗng.
   - Ngoài ra, việc nạp script từ `https://hoangthiencm.id.vn/js/khbd-slides.js` bị lỗi khi chạy trên Canvas do file này chưa được tải lên hosting.
2. **Yêu cầu cốt lõi**:
   - Bê toàn bộ cấu trúc chức năng nạp, phân tích SGK (Gemini Vision / PDF OCR / PPCT) từ `canvas_soankhbd.html` sang `canvas_soanbaigiang.html`: Khi người dùng tải Bài 5 lên và bấm đọc SGK, hệ thống phải phân tích ra **đúng 100% tên bài, các đề mục, định nghĩa, ví dụ và bài tập thực tế của Bài 5**.
   - Điểm khác biệt DUY NHẤT so với `canvas_soankhbd.html`: **Không tạo giáo án Word (bảng 2 cột KHBD)**, mà chuyển toàn bộ trọng tâm sang **Tạo Kịch bản Bài giảng Trình chiếu (Slides) thật qua Gemini AI**, hiển thị 16:9 có hiệu ứng từng bước và xuất file `.pptx`.

---

## Phạm vi Thực hiện cho Coder

1. **Đồng bộ 100% Luồng Đọc SGK & Điền Metadata trong `canvas_soanbaigiang.html`**:
   - Giữ nguyên toàn bộ pipeline xử lý ảnh/PDF SGK, PPCT từ `canvas_soankhbd.html`: Sử dụng `analyzeCanvasTextbookSafely`, `readTextbookWithMistral`, `geminiAPI.generateContent` với `model: "gemini-3-flash-preview"`.
   - Đảm bảo khi bấm "Đọc sách giáo khoa" với Bài 5: Tự động điền chính xác Tên bài học, Môn, Khối lớp, Số tiết, YCCĐ, và ngữ cảnh SGK đầy đủ (không được điền tào lao hay mock).
2. **Thay thế Luồng Soạn KHBD bằng Luồng Soạn Bài Giảng Trình Chiếu Thật (AI Lesson Slides)**:
   - Viết Prompt chuyên biệt `GENERATE_LESSON_SLIDES` gọi Gemini (`gemini-3-flash-preview`):
     + Đầu vào: Ngữ cảnh SGK thực tế vừa đọc của Bài 5 (các mục kiến thức, định nghĩa, ví dụ, bài tập).
     + Đầu ra: Kịch bản JSON đầy đủ cho 15–25 slide bám sát bài học thật:
       * **Slide Bìa & Mục tiêu**: Thông tin thực của Bài 5.
       * **Slide Khởi động**: Tình huống / trò chơi ngắn khởi động cho Bài 5.
       * **Slide Đơn vị kiến thức (Từng mục của Bài 5)**:
         - Slide Khám phá: Tình huống bài toán mở đầu của bài 5 $\rightarrow$ bước click hiện câu trả lời.
         - Slide Quy tắc / Công thức trọng tâm: Đóng khung công thức toán chuẩn của bài 5.
         - Slide Ví dụ mẫu: Đề bài ví dụ thực trong SGK $\rightarrow$ từng bước click hiện lời giải chi tiết (bằng KaTeX/Toán học).
         - Slide Luyện tập / Thực hành: Đề bài trong SGK $\rightarrow$ click hiện đáp án.
       * **Slide Bài tập củng cố & Vận dụng**: Các bài toán thực tế của bài 5.
3. **Nhúng trực tiếp logic Slide vào `canvas_soanbaigiang.html`**:
   - Tránh phụ thuộc vào đường link hosting ngoài chưa deploy (`https://hoangthiencm.id.vn/js/khbd-slides.js`).
   - Tích hợp inline hoặc nạp fallback an toàn đảm bảo chạy ngay lập tức cả trên file cục bộ lẫn trên Gemini Canvas.
4. **Trình chiếu 16:9 & Xuất file PowerPoint `.pptx` thật**:
   - Khung trình chiếu render KaTeX thật, nút Previous / Next / F5 Toàn màn hình, click chuột chuyển bước hiệu ứng.
   - Nút "Tải file PowerPoint (.pptx)" dùng PptxGenJS tạo file thật chứa trọn vẹn nội dung của Bài 5 vừa tạo.
5. **Tuyệt đối KHÔNG đụng chạm đến `canvas_soankhbd.html`**:
   - Giữ nguyên vẹn 100% `canvas_soankhbd.html` cho luồng tạo giáo án KHBD.

---

## File cần chỉnh sửa bởi Coder

1. `canvas_soanbaigiang.html` (chỉnh sửa chính: kết nối luồng đọc SGK thật và nút Tạo Bài giảng AI thật)
2. `js/khbd-slides.js` (cập nhật hàm gọi Gemini prompt thật thay vì regex mock)
3. `backupcode viettailieu/canvas_soanbaigiang.html` (đồng bộ 1-1)
4. `tests/canvas-soanbaigiang-smoke.js` (cập nhật test xác nhận luồng AI thật)

---

## Các bước thực hiện chi tiết cho Coder

### Bước 1: Khắc phục lỗi đọc SGK trong `canvas_soanbaigiang.html`
- Đảm bảo các hàm `readTextbookWithMistral`, `analyzeCanvasTextbookSafely`, `handleAnalyzeSourceMaterials` được liên kết chính xác với các nút trên giao diện.
- Xác nhận sau khi AI đọc SGK Bài 5, các trường `inputTopicCustom`, `selectGrade`, `selectSubject`, `inputDuration`, `editorVision` nhận đúng dữ liệu thật từ Gemini.

### Bước 2: Xây dựng hàm `generateAiLessonSlides()` gọi Gemini thật
- Viết prompt ép trả về JSON cấu trúc slide chuẩn:
  ```javascript
  const prompt = `Bạn là chuyên gia thiết kế bài giảng trình chiếu môn Toán. Dựa trên ngữ cảnh SGK sau đây của bài học:
  ${lessonContext}
  Hãy tạo kịch bản bài giảng trình chiếu chi tiết gồm 15-25 slide. BẮT BUỘC phân rã từng đơn vị kiến thức thành: Khám phá -> Quy tắc đóng khung -> Ví dụ mẫu giải từng bước -> Luyện tập tại chỗ.
  Trả về JSON: { "slides": [ { "type": "title|intro|explore|rule|example|practice|summary", "title": "...", "content": "...", "steps": ["bước 1", "bước 2"], "mathFormula": "..." } ] }`;
  ```
- Gọi `geminiAPI.generateContent` với `model: "gemini-3-flash-preview"`.
- Nhận kết quả và chuyển thành slide deck hiển thị trực tiếp.

### Bước 3: Đưa giao diện nút bấm & Trình chiếu vào hoạt động
- Nút **"TẠO BÀI GIẢNG TRÌNH CHIẾU AI (1-CLICK)"**:
  + Bấm nút $\rightarrow$ Gọi AI đọc dữ liệu bài $\rightarrow$ Tạo 15–25 slide thật $\rightarrow$ Chuyển sang khung chiếu 16:9 $\rightarrow$ Tự động sẵn sàng xuất file `.pptx`.
- Nút **"Tải file PowerPoint (.pptx)"**: Tạo file `.pptx` với nội dung bài học thật, có animation xuất hiện cho các `steps`.

### Bước 4: Kiểm thử và nghiệm thu
- Chạy `tests/canvas-soanbaigiang-smoke.js` để đảm bảo không có lỗi cú pháp, tương thích 100%.
- Kiểm tra trực quan: Tải ảnh/PDF bài học lên, đọc SGK và tạo slide thật.

---

## Tiêu chí nghiệm thu

1. Đẩy Bài 5 (ảnh hoặc PDF SGK) lên `canvas_soanbaigiang.html`: Hệ thống đọc bằng Gemini và điền chính xác Tên bài, Khối lớp, Môn học, không còn tình trạng điền tào lao.
2. Bấm tạo bài giảng: Gemini sinh ra bài giảng thật bám sát nội dung Bài 5 với đầy đủ các mục kiến thức, ví dụ mẫu giải chi tiết, không dùng câu chữ placeholder giả mạo.
3. Trình chiếu Web 16:9 sắc nét với công thức KaTeX và hiệu ứng từng bước.
4. Xuất file PowerPoint `.pptx` tải về mở được mượt mà trên máy tính.
5. Không làm thay đổi bất kỳ tính năng nào của `canvas_soankhbd.html`.
