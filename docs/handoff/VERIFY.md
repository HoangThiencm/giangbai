# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Tách riêng ứng dụng độc lập `canvas_soanbaigiang.html`: ĐẠT (nhân bản thành công từ Canvas KHBD, giao diện chuyên biệt cho soạn bài giảng trình chiếu).
- Bảo toàn tuyệt đối `canvas_soankhbd.html`, `soankhbd.html`, `js/khbd-app.js`, `js/khbd-docx.js`: ĐẠT (không bị sửa đổi bất kỳ dòng nào, chức năng soạn giáo án KHBD giữ nguyên 100%).
- Module `js/khbd-slides.js`: ĐẠT (phân rã đơn vị kiến thức SGK thành chuỗi Khám phá -> Kiến thức đóng khung -> Ví dụ mẫu từng bước -> Luyện tập tại chỗ, đạt quy mô 15–25 slide).
- Hiệu ứng sư phạm (Step-by-step reveal): ĐẠT (gán cơ chế reveal cho các bước giải, kịch bản click chuột).
- Công thức Toán & Trình chiếu Web / Xuất PPTX: ĐẠT (hỗ trợ KaTeX mượt mà trên Web, layout 16:9, nút Trình chiếu F5 và nút tải file `.pptx` qua PptxGenJS).
- Sao lưu và Test tự động: ĐẠT (bản sao lưu trong `backupcode viettailieu/canvas_soanbaigiang.html` và bài test `tests/canvas-soanbaigiang-smoke.js`).

## Test đã chạy
1. `tests/canvas-soanbaigiang-smoke.js`: PASS.
2. `tests/canvas-soankhbd-smoke.js`: PASS.
3. `tests/khbd-activity-e-smoke.js`: PASS.
4. `tests/khbd-pedagogy-rate-smoke.js`: PASS.
5. `tests/khbd-time-budgets-smoke.js`: PASS.
6. `tests/khbd-docx-format-smoke.js`: PASS.
7. `tests/sodiem-smoke.js`: PASS.

## Pass / Fail từng tiêu chí
1. Tiêu chí 1: Toàn bộ chức năng KHBD (`canvas_soankhbd.html`, `soankhbd.html`, `js/khbd-app.js`) không bị đụng chạm -> PASS.
2. Tiêu chí 2: Ứng dụng mới `canvas_soanbaigiang.html` hoạt động độc lập, kế thừa đầy đủ OCR/Vision và PPCT -> PASS.
3. Tiêu chí 3: Phân rã Hoạt động Kiến thức SGK thành chuỗi slide hoàn chỉnh (15–25 slide cho toàn bài) -> PASS.
4. Tiêu chí 4: Có cơ chế hiệu ứng sư phạm từng bước (step-by-step reveal) -> PASS.
5. Tiêu chí 5: Trình chiếu 16:9, KaTeX Toán học, xuất PowerPoint `.pptx` -> PASS.
6. Tiêu chí 6: 100% bài kiểm thử tự động đạt PASS -> PASS.

## Bug
(Không có bug)
