# IMPLEMENT: Bài giảng trình chiếu AI từ SGK thật

Đã triển khai đúng `docs/handoff/PLAN.md`.

Sửa lỗi hồi quy theo `docs/handoff/VERIFY.md`:

- `js/khbd-app.js`: prompt `canvasTextbookAnalysisPrompt()` nay yêu cầu fact extraction theo từng trường ngắn; giữ nguyên văn 100% tên đề mục/đề bài, cấm diễn đạt lại, tự đánh số hoặc điền nội dung bằng trí nhớ. Quy tắc `mergeCanvasTextbookSections()` cũng nhập tiểu mục không đánh số đứng trước mục cấp 1 (ví dụ “Tính chất của phép nhân”) vào `coreKnowledge` của mục đánh số đầu tiên, thay vì tạo section cấp 1 giả.

- `js/khbd-slides.js`: thêm `generateAiLessonSlides()` gọi `geminiAPI.generateContent` bằng model `gemini-3-flash-preview`. Prompt chỉ dùng ngữ cảnh SGK đã phân tích, yêu cầu JSON 15–25 slide theo các loại `title`, `intro`, `explore`, `rule`, `example`, `practice`, `summary`; dữ liệu sai cấu trúc, thiếu loại slide hoặc không đủ ngữ cảnh sẽ báo lỗi thay vì sinh nội dung mẫu.
- Nút tạo slide tự gọi `handleAnalyzeSourceMaterials()` khi đã tải SGK nhưng chưa có ngữ cảnh; sau đó render deck AI với các bước click và KaTeX. Luồng 1-click chờ deck AI hoàn tất trước khi mở tab trình chiếu.
- `canvas_soanbaigiang.html` và bản sao lưu được đồng bộ: bundle slide dùng đường dẫn cùng ứng dụng `js/khbd-slides.js`, không còn phụ thuộc URL bundle slide ở host ngoài.
- `tests/canvas-soanbaigiang-smoke.js`: bổ sung kiểm tra prompt/model Gemini, cấm URL bundle ngoài và kiểm tra chuyển JSON AI thành deck thật.
- Đã loại bỏ tiếp mọi fallback và lời giải/câu hỏi mẫu khỏi `buildSlideDeck()` legacy. Đường này chỉ đưa các dòng thật trích từ ngữ cảnh SGK vào deck; nếu thiếu metadata hoặc ngữ cảnh, nó dừng với lỗi rõ ràng. Smoke test cấm các chuỗi placeholder cũ tái xuất hiện.

Kiểm thử đã chạy:

- `tests/khbd-textbook-exact-structure-smoke.js`: đồng bộ assertion cache-bust từ `textbook-exact-v14` sang `textbook-exact-v18`, khớp với `canvas_soankhbd.html` và bản sao lưu hiện tại; không thay đổi mã nguồn ứng dụng.

`node tests/canvas-soanbaigiang-smoke.js` — PASS.

`node tests/canvas-soankhbd-smoke.js` — PASS.

`node tests/khbd-textbook-exact-structure-smoke.js` — PASS 100%, gồm Test 6 xác nhận tiểu mục không số “Tính chất của phép nhân” được nhập đúng vào Mục 1 và còn đúng 2 sections.

Không sửa `canvas_soankhbd.html`. Không có vấn đề còn lại trong phạm vi triển khai; cần `/verify` trên Antigravity để kiểm tra trực quan bằng SGK/PDF thật và mở tệp PPTX trên máy người dùng.
