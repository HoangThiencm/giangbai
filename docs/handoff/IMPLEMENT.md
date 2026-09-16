# IMPLEMENT: Bài giảng trình chiếu AI từ SGK

## Trạng thái
Đã triển khai source theo docs/handoff/PLAN.md. Kiểm thử riêng bài giảng PASS.
Chưa đạt tiêu chí toàn bộ test suites PASS: 86/96 suite được chạy PASS, 10 FAIL ngoài phần bài giảng.
Chờ Antigravity /verify và kiểm tra trực tiếp trên Gemini Canvas. Không commit/push.

## File thay đổi
- canvas_soanbaigiang.html
- backupcode viettailieu/canvas_soanbaigiang.html (đồng bộ nguyên nội dung)
- js/khbd-slides.js
- tests/canvas-soanbaigiang-smoke.js
- docs/handoff/IMPLEMENT.md

Không sửa canvas_soankhbd.html hoặc js/khbd-app.js. docs/handoff/.lock vẫn giữ LOCK.

## Nội dung triển khai
- Nhúng đầy đủ module js/khbd-slides.js vào hai HTML, không tải module slide bằng đường dẫn tương đối.
- 1-click tự đọc SGK chưa có OCR đúng phiên bản bằng handleAnalyzeSourceMaterials({internal:true}); sau đó gọi generateAiLessonSlides qua buildFromApp với nguồn SGK thực, model gemini-3-flash-preview và kịch bản 15–25 slide.
- Loại bỏ chuỗi gọi 7 bước giáo án Word khỏi handler 1-click. Không yêu cầu nhập tên bài trước khi đọc ảnh/PDF.
- Đồng bộ tên bài, môn/lớp từ kết quả phân tích vào state/UI; wrapper cục bộ trên trang slide cũng áp dụng khi bấm Phân tích SGK riêng.
- Đọc được appState/geminiAPI khai báo const ở global lexical scope. Không ghép nội dung giáo án cũ vào ngữ cảnh SGK.
- Sau sinh slide: chuyển tab trình chiếu, bật xuất PPTX, render KaTeX, thêm khung quy tắc, sửa click toàn màn hình để cập nhật host.
- Hủy hoặc đổi nguồn khi AI đang chạy không ghi đè deck đã hợp lệ. Lỗi OCR không gọi sinh slide.
- Các thư viện khác (core app, KaTeX, PptxGenJS) vẫn dùng cơ chế hiện có; chỉ module slide được inline theo plan.

## Kiểm thử
- node tests/canvas-soanbaigiang-smoke.js — PASS.
- Test chạy inline module và handler thật trong Node VM với DOM/Gemini/OCR giả lập; kiểm tra metadata, lexical globals, OCR mới/cũ, đúng 1 lần gọi sinh slide, 15 slide, chuyển tab, KaTeX, click toàn màn hình, lỗi JSON, hủy, đổi nguồn.
- PPTX: kiểm tra truyền đủ nội dung deck 15 slide, layout 16:9, tên .pptx vào PptxGenJS giả lập.
- Kiểm tra cú pháp script HTML và đồng bộ module inline/backup — PASS.
- Hồi quy: 86/96 suite PASS. Bỏ tests/_tmp-*.js và khbd-navigation-tabs-smoke.js vì có thao tác sửa source ngoài phạm vi. Không chạy run-all-tests.js vì runner gọi cả những script này.
- Không có Git khả dụng trong PATH của ChatCode, không kiểm tra được git diff/status.
- Thử xác minh PPTX thật bằng thư viện CDN bị automatic approval review từ chối: tải và chạy JS CDN với quyền Node process/require gây rủi ro thực thi mã. Không thực hiện thao tác đó. Máy chưa có package pptxgenjs cục bộ; chưa xác minh file PPTX nhị phân hoặc tải file trong trình duyệt.
- Chưa thử API Gemini trực tiếp, giao diện Gemini Canvas thật hoặc chất lượng nội dung AI trên SGK thực. Không khẳng định các nghiệm thu này PASS.

## 10 suite FAIL ngoài phần bài giảng
Các test sau không tham chiếu canvas_soanbaigiang hoặc khbd-slides; không sửa ngoài plan:
- backupcode-canvas-smoke.js: backup taobaitap thiếu banner Gemini Canvas.
- canvas-module-fallback-smoke.js: thiếu Canvas core bootstrap.
- game-quiz-importer-smoke.js: isGeoGebraCoordinateRequested chưa định nghĩa.
- khbd-activity-d-dedupe-smoke.js: không khớp heading hoạt động E (0 phút).
- khbd-activity-e-dedupe-smoke.js: không khớp thời lượng 4 phút.
- khbd-mistral-ocr-smoke.js: test yêu cầu Mistral trước.
- khbd-nls-rate-smoke.js: không khớp nhãn gợi ý NLS theo tỉ trọng.
- khbd-pedagogy-script-smoke.js: độ rộng bảng Word không khớp 4819/4820 dxa.
- khbd-vision-batching-smoke.js: test yêu cầu mỗi lô 1 trang/ảnh.
- kttx-smoke.js: thiếu đồng bộ key khi React mount.

## Bàn giao Tester
Mở Gemini Canvas, tải ảnh/PDF SGK thực rồi bấm 1-click khi tên bài trống; kiểm tra môn/lớp/tên bài, nội dung 15–25 slide, công thức, F5/click/Previous/Next và tải PowerPoint thật. Thử Phân tích SGK riêng, lỗi API, hủy và thay nguồn lúc đang chạy. Đối chiếu các FAIL ngoài scope trước khi kết luận VERIFY.md.
