# PLAN: Nhận Diện Bài Luyện Tập Chung / Ôn Tập — Chuyển Mục B Thành "Luyện Tập & Chữa Bài Tập SGK", Xóa Bỏ Prompt Leak

## User Review Required
> [!IMPORTANT]
> - **Hiện tượng**:
>   1. Đối với các bài **Luyện tập chung / Ôn tập chương / Bài tập cuối chương / Ôn tập học kỳ**, bài học hoàn toàn KHÔNG CÓ kiến thức mới, nhưng hệ thống (cả `soankhbd.html` lẫn `canvas_soankhbd.html`) vẫn ép cứng Mục B là "## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI" và bắt tìm "Mục 1, Mục 2 lớn", khiến AI bị xung đột logic, tự bịa lý thuyết và bỏ quên bài tập trong SGK.
>   2. Prompt leak dòng `(Các YCCĐ của bài học theo CT GDPT 2018; mỗi ý một gạch đầu dòng, giữ động từ hành vi.)` bị in thẳng vào Mục I.
>   3. Nút 1-Click trên `soankhbd.html` chưa tự động kích hoạt đọc SGK nếu người dùng chưa nhấn nút phân tích trước đó.
> - **Giải pháp**:
>   1. Bổ sung bộ nhận diện `isReviewOrPracticeLesson(topic)` trong `js/khbd-prompts.js` và `js/khbd-app.js`.
>   2. Khi là bài Luyện tập / Ôn tập / Bài tập cuối chương:
>      - Mục B tự động chuyển thành: `## B. HOẠT ĐỘNG 2: LUYỆN TẬP (HỆ THỐNG HÓA KIẾN THỨC VÀ CHỮA CÁC BÀI TẬP TRỌNG TÂM TRONG SGK)`. Các nhánh 2.1, 2.2... ánh xạ trực tiếp theo từng Bài tập trong SGK (Bài 1, Bài 2...).
>      - Mục C tự động chuyển thành: `## C. HOẠT ĐỘNG 3: LUYỆN TẬP NÂNG CAO VÀ VẬN DỤNG CÁC BÀI TẬP CÒN LẠI TRONG SGK`.
>      - Mục I (Mục tiêu): Tự động chuyển thành củng cố, hệ thống hóa kiến thức và rèn kỹ năng giải bài tập SGK (không ép chép YCCĐ bài mới).
>   3. Xóa dòng prompt leak khỏi template và bổ sung bộ lọc regex trong `sanitizeLessonMarkdown`.
>   4. Bổ sung bước tự động đọc SGK trước khi chạy 1-Click nếu có ảnh mà chưa OCR.

---

## I. Thiết Kế Kỹ Thuật Chi Tiết

### Module 1: Xây Dựng Hàm Nhận Diện & Chuẩn Hóa Prompt Trong `js/khbd-prompts.js`
1. **Thêm hàm nhận diện thể loại bài dạy**:
   ```javascript
   function isReviewOrPracticeLesson(topic) {
     return /(?:luyện\s*tập\s*chung|luyện\s*tập|bài\s*tập\s*cuối\s*chương|ôn\s*tập\s*chương|ôn\s*tập|thực\s*hành\s*tổng\s*hợp)/i.test(String(topic || ""));
   }
   ```
2. **Cập nhật `GENERATE_OBJECTIVES`**:
   - Xóa bỏ dòng chữ nhắc `(Các YCCĐ của bài học theo CT GDPT 2018; mỗi ý một gạch đầu dòng, giữ động từ hành vi.)` tại dòng ~535.
   - Nếu `isReviewOrPracticeLesson(context.topic)`:
     - Mục tiêu kiến thức tập trung:
       - Hệ thống hoá, củng cố vững chắc các kiến thức, định lý, công thức trọng tâm trong chương/chủ đề.
       - Vận dụng thành thạo các phương pháp và quy tắc để giải quyết các bài tập trong SGK.
       - Rèn luyện kỹ năng giải toán, nhận diện và khắc phục các sai lầm, ngộ nhận thường gặp.
       *(CẤM chép các câu nhận biết khái niệm ban đầu của bài học mới).*
3. **Cập nhật `GENERATE_ACTIVITY_B`**:
   - Kiểm tra `isReviewOrPracticeLesson(context.topic)`:
     - **Nếu là bài Luyện tập / Ôn tập**:
       - Tiêu đề bắt buộc:
         `## B. HOẠT ĐỘNG 2: LUYỆN TẬP (HỆ THỐNG HÓA KIẾN THỨC VÀ CHỮA CÁC BÀI TẬP TRỌNG TÂM TRONG SGK) ({time_budget_B})`
       - Chỉ dẫn AI: *"Đây là tiết Luyện tập / Ôn tập / Bài tập cuối chương, KHÔNG CÓ HÌNH THÀNH KIẾN THỨC MỚI. Mục B chuyển trọng tâm thành: Ôn nhanh kiến thức trọng tâm và chữa các bài tập cơ bản trong dữ liệu SGK đã nạp. BẮT BUỘC chia các nhánh 2.1, 2.2... theo từng bài tập hoặc cụm bài tập trong SGK (Ví dụ: ### Hoạt động 2.1: Chữa Bài tập 1 trong SGK; ### Hoạt động 2.2: Chữa Bài tập 2 trong SGK). Bắt buộc trích dẫn nguyên văn đề bài từ SGK vào cột Nội dung và giải chi tiết từng bước."*
     - **Nếu là bài lý thuyết thông thường**: Giữ nguyên tiêu đề `## B. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI ({time_budget_B})`.
4. **Cập nhật `GENERATE_ACTIVITY_C`**:
   - Nếu là bài Luyện tập / Ôn tập:
     - Tiêu đề: `## C. HOẠT ĐỘNG 3: LUYỆN TẬP NÂNG CAO VÀ VẬN DỤNG CÁC BÀI TẬP CÒN LẠI TRONG SGK ({time_budget_C})`.
     - Chữa tiếp các bài tập tự luận nâng cao, bài toán thực tiễn tiếp theo trong SGK.

### Module 2: Cập Nhật `js/khbd-app.js`
1. **Lọc sạch Prompt Leak trong `sanitizeLessonMarkdown`** (dòng ~6175):
   ```javascript
   text = text.replace(/(?:^|\n)\s*\((?:Các YCCĐ|mỗi ý một gạch đầu dòng|Yêu cầu cần đạt của bài học|giữ động từ hành vi)[^)]*\)(?:\s*\n|\s*$)/gi, "\n");
   text = text.replace(/\((?:Các YCCĐ của bài học[^)]*)\)/gi, "");
   ```
2. **Tự động đọc SGK trong `handle1ClickGenerate`** (dòng ~8190):
   ```javascript
   if (hasTextbookMedia() && !hasAnalyzedLessonContent()) {
     updateProgress(5, "Đang đọc nội dung học liệu SGK...");
     if (typeof handleAnalyzeSourceMaterials === "function") {
       await handleAnalyzeSourceMaterials({ internal: true });
     }
   }
   ```
3. **Cập nhật nhãn động cho Subtab B trên giao diện**:
   - Trong `syncDraftDom` hoặc hàm đổi bài học:
     - Nếu `isReviewOrPracticeLesson(topic)`: Đổi nhãn nút `[data-act="B"]` thành `B. Luyện tập & Chữa bài tập SGK` (và tiêu đề card khi click vào tab B thành `B. Hoạt động Luyện tập & Chữa bài tập SGK`).
     - Ngược lại: Trả về `B. Hình thành Kiến thức`.

### Module 3: Kiểm Thử Tự Động (`tests/khbd-review-practice-lesson-smoke.js`)
- Kiểm tra:
  1. `isReviewOrPracticeLesson` nhận diện chính xác "Bài tập cuối chương I", "Luyện tập chung trang 21", "Ôn tập chương 2", và trả `false` cho "Bài 1. Phương trình bậc nhất".
  2. Template `GENERATE_ACTIVITY_B` sinh tiêu đề `LUYỆN TẬP` khi topic là bài ôn tập/bài tập.
  3. Prompt leak `(Các YCCĐ...)` không còn xuất hiện trong prompt và được hàm `sanitizeLessonMarkdown` gọt sạch.
  4. Bộ test cũ `tests/soankhbd-generation-mode-smoke.js` và `tests/canvas-soankhbd-smoke.js` tiếp tục PASS 100%.

---

## II. Danh Sách Tệp Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục đích thay đổi |
| :--- | :--- | :--- |
| `js/khbd-prompts.js` | Dòng ~516, ~535, ~710, ~754, ~795 | Thêm `isReviewOrPracticeLesson`, đổi tiêu đề/chỉ dẫn Mục B & C cho bài ôn tập, xóa prompt leak |
| `js/khbd-app.js` | Dòng ~6175, ~8190, ~8850 | Thêm regex sanitize prompt leak, tự động đọc SGK trước 1-Click, cập nhật nhãn tab B động |
| `tests/khbd-review-practice-lesson-smoke.js` | Tệp mới | Smoke test kiểm thử nhận diện bài ôn tập và loại bỏ prompt leak |

---

## III. Kế Hoạch Kiểm Thử (Verification Plan)

### Kiểm thử tự động
- `node tests/khbd-review-practice-lesson-smoke.js` — PASS 100%.
- `node tests/soankhbd-generation-mode-smoke.js` — PASS 100%.
- `node tests/canvas-soankhbd-smoke.js` — PASS 100%.
