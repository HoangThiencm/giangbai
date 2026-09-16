# PLAN

## Hiện trạng
- Trong `soankhbd.html`, `canvas_soankhbd.html` và `js/khbd-app.js`:
  1. Khi phân tích SGK, hệ thống đang dùng các câu lệnh cấm đoán ("không chép nguyên văn", "diễn đạt lại") khiến AI tự ý thay đổi từ ngữ, làm sai lệch:
     - **Tên các đề mục chính trong bài** (1. ..., 2. ...).
     - **Tên các hoạt động khám phá, luyện tập, thực hành** (HĐ 1, HĐ 2, Luyện tập 1, Thực hành 1...).
     - **Đề bài, dữ liệu số học, công thức toán học và yêu cầu của các bài tập trong SGK** (Bài 1.1, Bài 1.36...).
  2. Khi giáo viên soạn bài giảng, các Hoạt động 2 (Hình thành kiến thức), Hoạt động 3 (Luyện tập) và Hoạt động 4 (Vận dụng) bị lệch so với sách học sinh đang cầm, gây nguy hiểm trong thực tế giảng dạy.

## Phạm vi
- Chuẩn hóa toàn diện quy trình trích xuất học liệu SGK:
  1. `js/khbd-app.js`:
     - Tái cấu trúc Prompt phân tích SGK (`canvasTextbookAnalysisPrompt` và các hàm phân tích): Yêu cầu trích xuất **chính xác nguyên văn 100%** các thực thể dữ liệu sư phạm:
       + Tên Đề mục mục lớn (`sections.title`).
       + Công thức toán học / Định nghĩa đóng khung (`coreKnowledge`).
       + Tên và đề bài nguyên văn của từng Hoạt động con (`HĐ 1`, `Luyện tập 1`, `Thực hành 1`, `Vận dụng 1`...).
       + Tên mã bài và đề bài nguyên văn của toàn bộ hệ thống bài tập SGK (`Bài 1.36: ...`, `Bài 1.37: ...`).
     - Sử dụng Schema JSON có cấu trúc để Gemini không bị chặn bởi bộ lọc bản quyền `RECITATION`.
     - Cập nhật `formatCanvasTextbookContext` để xuất văn bản ngữ cảnh rõ ràng, rành mạch từng phần đề mục và bài tập.
  2. `js/khbd-prompts.js`:
     - Trong `GENERATE_ACTIVITY_B`: Ràng buộc bắt buộc đặt tên Hoạt động 2.1, 2.2 trùng khớp 100% với tên đề mục SGK đã trích xuất.
     - Trong `GENERATE_ACTIVITY_C` (Luyện tập): Ràng buộc bắt buộc lấy **nguyên văn 100% đề bài** từ các mục `Luyện tập`, `Thực hành` hoặc bài tập SGK đã trích xuất; tuyệt đối cấm đổi số liệu, cấm tự tạo đề bài lạ ngoài sách.
     - Trong `GENERATE_ACTIVITY_D` (Vận dụng): Ràng buộc ưu tiên lấy nguyên văn đề bài mục `Vận dụng` trong SGK.
  3. `canvas_soankhbd.html` & `soankhbd.html`: Đồng bộ cache-busting các tệp JS.
  4. Test tự động: `tests/khbd-textbook-exact-structure-smoke.js`.

## Ngoài phạm vi
- Không thay đổi các khung tiêu chuẩn sư phạm GDPT 2018 (CV 5512, Khung NLS, Khung AI).

## File dự kiến tác động
- `js/khbd-app.js`
- `js/khbd-prompts.js`
- `canvas_soankhbd.html`
- `backupcode viettailieu/canvas_soankhbd.html`
- `tests/khbd-textbook-exact-structure-smoke.js`

## Các bước thực hiện
1. **Thiết kế lại Prompt trích xuất SGK có cấu trúc trong `js/khbd-app.js`**:
   - Chuyển sang trích xuất JSON Schema với các trường rõ ràng:
     ```json
     {
       "subject": "Toán",
       "grade": "6",
       "topic": "Tên bài học",
       "periodCount": 2,
       "sections": [
         {
           "index": "1",
           "title": "Tên nguyên văn Đề mục 1 trong SGK",
           "coreKnowledge": "Quy tắc, định nghĩa, công thức LaTeX chuẩn",
           "activities": [
             { "label": "HĐ 1", "task": "Đề bài / yêu cầu nguyên văn của HĐ 1" },
             { "label": "Luyện tập 1", "task": "Đề bài nguyên văn của Luyện tập 1" },
             { "label": "Vận dụng 1", "task": "Đề bài nguyên văn của Vận dụng 1" }
           ]
         }
       ],
       "exercises": [
         { "code": "Bài 1.36", "statement": "Đề bài nguyên văn đầy đủ số liệu và biểu thức của Bài 1.36" }
       ]
     }
     ```
2. **Cập nhật `formatCanvasTextbookContext`**:
   - Trình bày trực quan, đầy đủ từng đề mục và từng đề bài bài tập để nạp vào `{textbook_content}`.
3. **Cập nhật `GENERATE_ACTIVITY_B`, `GENERATE_ACTIVITY_C`, `GENERATE_ACTIVITY_D` trong `js/khbd-prompts.js`**:
   - Yêu cầu AI giữ nguyên văn 100% đề bài và số liệu từ dữ liệu SGK đã trích xuất khi đưa vào Hoạt động dạy học và lời giải ở bảng phụ/phiếu học tập.
4. **Kiểm thử tự động**:
   - Chạy `node tests/khbd-textbook-exact-structure-smoke.js` và `node tests/canvas-soankhbd-smoke.js`.

## Rủi ro
- Lỗi bản quyền `RECITATION`: Đã phòng ngừa bằng việc trích xuất JSON theo từng trường dữ liệu ngắn (Fact extraction) thay vì xuất nguyên văn toàn trang văn bản.
- Đề bài chứa công thức toán học phức tạp: Sử dụng ký hiệu LaTeX `$ ... $` chuẩn mực để giữ độ chính xác của biểu thức.

## Cách kiểm thử
- `node tests/khbd-textbook-exact-structure-smoke.js`.
- Kiểm tra dữ liệu trích xuất hiển thị trong ô "Nội dung SGK đã đọc" có đúng 100% đề mục và đề bài bài tập.

## Tiêu chí nghiệm thu
- Tên các Đề mục (1. ..., 2. ...) trong giáo án trùng khớp 100% với mục lục và tiêu đề trong SGK.
- Đề bài các bài Luyện tập, Vận dụng, Bài tập trong giáo án trùng khớp 100% về câu chữ, số liệu, công thức với SGK thật.
- Không xảy ra lỗi từ chối bản quyền `RECITATION`.
- Mọi bài kiểm thử smoke đều PASS 100%.
