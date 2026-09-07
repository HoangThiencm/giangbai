# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đạt: **Chuẩn hóa Phụ lục 2 theo CV 5512**: Đổi bản chất từ danh sách bài học lý thuyết sang Kế hoạch tổ chức các hoạt động giáo dục (Hoạt động thực hành trải nghiệm, chuyên đề STEM, CLB môn học, AI Day). Bảng 10 cột có cột `STT`, khối tiêu đề hành chính Quốc hiệu/Tên trường/Tổ, khối chữ ký bên trái `TỔ TRƯỞNG` và bên phải `HIỆU TRƯỞNG` chuẩn xác 100%.
- Đạt: **Đồng bộ 100% NLS & AI giữa Phụ lục 1 và Phụ lục 3**: Phụ lục 1 là Single Source of Truth; Phụ lục 3 tự động kế thừa 100% mã và mô tả tích hợp từ Phụ lục 1; sửa ô tích hợp ở Phụ lục 1 tự động cập nhật sang Phụ lục 3 ngay lập tức.
- Đạt: **Khắc phục triệt để gán ghép NLS gượng ép môn Toán**: Loại bỏ hoàn toàn mã Miền 6 (AI) khỏi danh mục đề xuất NLS môn Toán; ưu tiên tuyệt đối các công cụ số toán học cốt lõi (Máy tính cầm tay, GeoGebra/Desmos, Bảng tính điện tử) theo chuẩn CTGDPT 2018.
- Đạt: **Khắc phục dứt điểm lỗi cụt mô tả cột AI (QĐ 2422)**: 100% các ô AI luôn có đầy đủ mã chuẩn, câu mô tả hành động sư phạm gắn với bài học và trách nhiệm kiểm chứng theo 4 nhóm A, B, C, D của QĐ 2422, kèm phạm vi tiết `(Áp dụng: tiết X, Y)`.
- Đạt: **Đồng bộ song song 1-1** trên cả `xaydungphuluc.html` và `canvas_xaydungphuluc.html` (kèm mirror `backupcode viettailieu/canvas_xaydungphuluc.html`).
- Đạt: Toàn bộ 58 test suite trong toàn dự án và kiểm tra cú pháp JS inline đều thành công 100%.

## Test đã chạy
1. `node tests/run-all-tests.js`: **ALL 58 TEST SUITES PASSED 100%!**
2. `node tests/xaydungphuluc-smoke.js`: PASS 100% (bao gồm ca kiểm thử làm giàu mã AI cụt `9.B2.1`, khử bỏ chatbot lịch sử NLS, ưu tiên 5.3.TC2a cho Đại số 9).
3. `node tests/canvas-xaydungphuluc-smoke.js`: PASS 100% (bao gồm kiểm tra Canvas với `cleanLessonDescription`, `lessonAppliedNlsDescription`, `lessonAppliedAiDescription`).
4. `node tests/xaydungphuluc-integration-smoke.js`: PASS 100%.
5. `node tests/canvas-soankhbd-smoke.js`: PASS 100%.
6. `node tests/soankhbd-ppct-standards-smoke.js`: PASS 100%.
7. `node tests/khbd-ppct-integration-smoke.js`: PASS 100%.
8. `node tests/khbd-ai-catalog-smoke.js`: PASS 100%.
9. `node tests/khbd-ai-integration-gate.test.js`: PASS 100%.
10. `node tests/khbd-4steps-workflow-smoke.js`: PASS 100%.
11. Kiểm tra cú pháp toàn bộ JavaScript inline Canvas bằng Node `vm.Script`: PASS.

## Pass / Fail từng tiêu chí
- [PASS] Loại bỏ hoàn toàn mã Miền 6 (AI) khỏi Năng lực số môn Toán: `recommendOfficialStandards('digital', ...)` cho Toán 9 phương trình 100% không đề xuất mã 6.x, ưu tiên `5.3.TC2a` ("Sử dụng sáng tạo công nghệ số - máy tính cầm tay, GeoGebra") và `5.2.TC2a`, `1.1.TC2a`.
- [PASS] Khắc phục triệt để lỗi cụt mô tả cột AI: `cleanAiColumnText('9.B2.1 - (Áp dụng: tiết 1, 2).', ...)` tự động bổ sung mô tả hành động sư phạm và trách nhiệm kiểm chứng chuẩn QĐ 2422, giữ nguyên vẹn phạm vi tiết.
- [PASS] Lọc bỏ triệt để các câu NLS đối phó "dùng chatbot tìm hiểu lịch sử ra đời": `cleanNlsColumnText` tự động chuyển hóa thành mô tả thực hành công cụ số trực quan.
- [PASS] Chuẩn hóa toàn diện Phụ lục 2: dữ liệu mẫu 6 hoạt động trải nghiệm/STEM/AI Day, prompt chỉ thị đúng bản chất, bảng 10 cột có cột STT, khối tiêu đề hành chính Quốc hiệu/Tên trường/Tổ, chữ ký Tổ trưởng (bên trái) và Hiệu trưởng (bên phải).
- [PASS] Đồng bộ 100% NLS & AI giữa Phụ lục 1 và Phụ lục 3: Kế thừa chính xác từ Phụ lục 1 (Single Source of Truth), cập nhật realtime 2 chiều khi chỉnh sửa ô NLS/AI.
- [PASS] Toàn bộ 58/58 bài test của hệ thống chạy PASS 100%.

## Bug
- Lỗi: Không có
- Tái hiện: Không có
- File liên quan: Không có
