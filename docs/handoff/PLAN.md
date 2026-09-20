# PLAN: Cứu Hộ Khung Prompt Mục Tiêu & Năng Lực Chuẩn CV 5512 Trên canvas_soankhbd.html

## Hiện trạng & Nguyên nhân gốc rễ (Root Cause)

1. **File `js/khbd-prompts.js` trên hosting `hoangthiencm.id.vn` bị rỗng (0 bytes)**:
   - Khi chạy `canvas_soankhbd.html` trên môi trường Canvas (trỏ host `https://hoangthiencm.id.vn`), trang nạp file qua thẻ:
     `<script src="https://hoangthiencm.id.vn/js/khbd-prompts.js?v=20260916-textbook-exact-v18"></script>`
   - Do sự cố truyền file FTP trước đó, file `js/khbd-prompts.js` trên hosting trả về HTTP 200 nhưng dung lượng đúng **0 bytes** (đã kiểm chứng qua HTTP request).
   - Tương tự như file `js/khbd-pedagogy-catalog.js` từng bị 0 bytes trước đây, trình duyệt nạp xong file 0 bytes mà không báo lỗi, nhưng toàn bộ mã trong file không được thực thi.

2. **Hậu quả khiến phần Năng lực bị nhảy tào lao / mất cấu trúc**:
   - `window.PROMPTS.GENERATE_OBJECTIVES` và hàm `window.getPromptTemplate` không hề tồn tại.
   - Khi bấm tạo I. Mục tiêu (hoặc bấm nút "⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)"), hàm `executeStep` gọi `getPromptTemplate('GENERATE_OBJECTIVES', context)` trả về chuỗi rỗng `""`.
   - Hàm `buildPedagogicalPrompt("")` chỉ còn lại hợp đồng đầu ra chung chung: *"NLS là Năng lực số... AI là Năng lực AI... BẮT BUỘC: Các vị trí tích hợp NLS và AI phải được in đậm và in nghiêng (***...***)"*.
   - **Gemini hoàn toàn không nhận được template yêu cầu**:
     + Mất sạch yêu cầu mục `## 1. Về kiến thức` (YCCĐ chuẩn CT GDPT 2018).
     + Mất sạch mục `### a) Năng lực chung` (Tự chủ và tự học, Giao tiếp và hợp tác, Giải quyết vấn đề và sáng tạo).
     + Mất sạch mục `### b) Năng lực đặc thù môn học` (môn Toán: Tư duy và lập luận toán học, Mô hình hoá toán học...).
     + Mất sạch các tiểu mục `### c) Năng lực số`, `### d) Năng lực AI` kèm mã chuẩn `[1-5].x.TC...` hay `[6-9].[A-D]...`.
   - Kết quả là AI tự "bịa" cấu trúc tự do:
     ```markdown
     2. Năng lực:
     - Năng lực tư duy và lập luận toán học: Phân biệt được các đối tượng...
     - ***NLS: Sử dụng máy tính cầm tay...***
     - ***AI: Sử dụng các phần mềm...***
     ```
   - Ngoài ra, ở khung xem trước KaTeX (cột phải), vì AI sinh gạch đầu dòng `- ***NLS:...***` nên Marked.js tạo thẻ `<li>`, logic tô màu đóng khung NLS/AI biến nội dung thành thẻ box nhưng để lại dấu gạch đầu dòng `- ` trơ trọi phía trước.
   - Các hoạt động tiếp theo (Thiết bị, Khởi động, Hình thành kiến thức, Luyện tập, Vận dụng) cũng bị ảnh hưởng nặng vì toàn bộ prompt nghiệp vụ trong `khbd-prompts.js` bị mất.

3. **Thiếu cơ chế CDN Fallback cho `khbd-prompts.js`**:
   - Trước đây trong `canvas_soankhbd.html` chỉ mới bổ sung `ensureKhbdPedagogyCatalogFallback()` cho `khbd-pedagogy-catalog.js` (nạp từ CDN jsDelivr `https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-pedagogy-catalog.js`).
   - Chưa hề có `ensureKhbdPromptsFallback()` để tự động nạp `khbd-prompts.js` từ CDN GitHub jsDelivr (`https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-prompts.js` - file trên GitHub hiện đang có đầy đủ 156KB).
   - Đoạn guard `if (typeof window.PROMPTS === "undefined")` ở dòng 1242 chỉ gán một object cụt gồm `OUTPUT_CONTRACT` và `ENGLISH_ELT_DIRECTIVE`, vô tình làm che giấu sự thiếu hụt của toàn bộ kho prompt mà không kích hoạt tải lại.

---

## Phạm vi thực hiện

1. **Thêm cơ chế tự cứu hộ CDN jsDelivr cho `khbd-prompts.js` trên `canvas_soankhbd.html` và `backupcode viettailieu/canvas_soankhbd.html`**:
   - Ngay sau khối nạp `js/khbd-prompts.js`, thêm hàm `ensureKhbdPromptsFallback()`:
     Kiểm tra nếu `typeof window.getPromptTemplate !== "function" || !window.PROMPTS || !window.PROMPTS.GENERATE_OBJECTIVES`, lập tức dùng `document.write` nạp dự phòng từ CDN GitHub jsDelivr:
     `https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-prompts.js`
   - Đảm bảo khi file trên hosting bị rỗng (0 bytes) hoặc lỗi mạng, trình duyệt sẽ tự động tải file đầy đủ 156KB từ CDN GitHub jsDelivr, phục hồi 100% kho siêu prompt sư phạm.

2. **Thêm cơ chế tự cứu hộ CDN jsDelivr cho `khbd-docx.js` (phòng ngừa rủi ro tương tự)**:
   - Thêm `ensureKhbdDocxFallback()` kiểm tra `typeof window.createKhbdDocxDocument !== "function"` để nạp từ CDN jsDelivr nếu hosting bị lỗi 0 bytes.

3. **Cải tiến `guardGeminiLessonOutput` / `applyObjectivesOutput` & Preview Rendering**:
   - Trong `js/khbd-app.js`, tại `applyObjectivesOutput`, nếu phát hiện AI trả về cấu trúc thiếu Năng lực chung (`### a) Năng lực chung`) hoặc thiếu tiêu đề Năng lực đặc thù (`### b) Năng lực đặc thù`), tự động chuẩn hóa hoặc kích hoạt tái tạo lại bằng prompt cứng chuẩn.
   - Tại `applyLiteralListMarkers` / `applyIntegrationPreviewColors` trong `js/khbd-app.js`: Xử lý trường hợp `li` chứa badge NLS/AI dạng inline để loại bỏ dấu gạch ngang đầu dòng bị trơ trọi `- `.

4. **Kiểm thử tự động**:
   - Bổ sung test case trong `tests/canvas-prompts-integrity-smoke.js` kiểm tra sự hiện diện của `ensureKhbdPromptsFallback`, kiểm tra template `GENERATE_OBJECTIVES` có đủ các section:
     + `### a) Năng lực chung`
     + `### b) Năng lực đặc thù môn học`
     + `{digital_objectives_section}`
     + `{ai_objectives_section}`
   - Bổ sung test trong `tests/canvas-soankhbd-smoke.js` xác nhận cả hai file HTML (`canvas_soankhbd.html` và bản backup) đều có fallback CDN jsDelivr cho cả `khbd-prompts.js`, `khbd-pedagogy-catalog.js` và `khbd-docx.js`.
   - Chạy toàn bộ test suite để đảm bảo không gãy bất kỳ bài kiểm thử nào.

---

## File dự kiến tác động
1. `canvas_soankhbd.html`
2. `backupcode viettailieu/canvas_soankhbd.html`
3. `js/khbd-app.js`
4. `tests/canvas-prompts-integrity-smoke.js`
5. `tests/canvas-soankhbd-smoke.js`

---

## Các bước Coder triển khai chi tiết

### Bước 1: Thêm `ensureKhbdPromptsFallback` vào `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`
- Vị trí: Ngay sau script nạp `khbd-prompts.js` (khoảng dòng 1124).
- Nội dung:
```html
  <script>
    (function ensureKhbdPromptsFallback() {
      if (typeof window.getPromptTemplate === "function" && window.PROMPTS && window.PROMPTS.GENERATE_OBJECTIVES) return;
      var isLocal = typeof window !== "undefined" && (window.location.protocol === "file:" || /^(localhost|127\.0\.0\.1)$/.test(window.location.hostname));
      var cdnPrompts = "https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-prompts.js";
      document.write('<script src="' + (isLocal ? "js/khbd-prompts.js" : cdnPrompts) + '"><\/script>');
    })();
  </script>
```

### Bước 2: Thêm `ensureKhbdDocxFallback` vào `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`
- Vị trí: Ngay sau script nạp `khbd-docx.js`.
- Nội dung:
```html
  <script>
    (function ensureKhbdDocxFallback() {
      if (typeof window.createKhbdDocxDocument === "function" || typeof window.KHBD_DOCX !== "undefined") return;
      var isLocal = typeof window !== "undefined" && (window.location.protocol === "file:" || /^(localhost|127\.0\.0\.1)$/.test(window.location.hostname));
      var cdnDocx = "https://cdn.jsdelivr.net/gh/HoangThiencm/giangbai@main/js/khbd-docx.js";
      document.write('<script src="' + (isLocal ? "js/khbd-docx.js" : cdnDocx) + '"><\/script>');
    })();
  </script>
```

### Bước 3: Cải thiện nhận diện cấu trúc Năng lực trong `js/khbd-app.js`
- Tại `isOffTopicObjectivesHallucination(text)`:
  Nếu text thiếu cả `năng lực chung` lẫn `năng lực đặc thù`, đánh dấu là thiếu chuẩn để kích hoạt tái tạo với prompt cứng đầy đủ.
- Tại bộ render preview `applyLiteralListMarkers`:
  Xử lý khi nội dung item chỉ là badge NLS/AI để không render bullet `- ` trơ trọi.

### Bước 4: Viết và chạy kiểm thử tự động
- Chạy:
  `node tests/canvas-prompts-integrity-smoke.js`
  `node tests/canvas-soankhbd-smoke.js`
  `node tests/khbd-competencies-smoke.js`
  `node tests/khbd-nls-ai-bold-italic-smoke.js`
- Xác nhận 100% tests PASS.
