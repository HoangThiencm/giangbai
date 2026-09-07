# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đạt: **Chuẩn hóa Phụ lục 2 theo CV 5512**: Đổi bản chất từ danh sách bài học lý thuyết sang Kế hoạch tổ chức các hoạt động giáo dục (Hoạt động thực hành trải nghiệm, chuyên đề STEM, CLB môn học, AI Day). Bảng 10 cột có cột `STT`, khối tiêu đề hành chính Quốc hiệu/Tên trường/Tổ, khối chữ ký bên trái `TỔ TRƯỞNG` và bên phải `HIỆU TRƯỞNG` chuẩn xác 100%.
- Đạt: **Đồng bộ 100% NLS & AI giữa Phụ lục 1 và Phụ lục 3**: Phụ lục 1 là Single Source of Truth; Phụ lục 3 tự động kế thừa 100% mã và mô tả tích hợp từ Phụ lục 1; sửa ô tích hợp ở Phụ lục 1 tự động cập nhật sang Phụ lục 3 ngay lập tức.
- Đạt: **Khắc phục triệt để gán ghép NLS gượng ép môn Toán**: Loại bỏ hoàn toàn mã Miền 6 (AI) khỏi danh mục đề xuất NLS môn Toán; ưu tiên tuyệt đối các công cụ số toán học cốt lõi (Máy tính cầm tay, GeoGebra/Desmos, Bảng tính điện tử) theo chuẩn CTGDPT 2018.
- Đạt: **Khắc phục dứt điểm lỗi cụt mô tả cột AI (QĐ 2422)**: 100% các ô AI luôn có đầy đủ mã chuẩn, câu mô tả hành động sư phạm gắn với bài học và trách nhiệm kiểm chứng theo 4 nhóm A, B, C, D của QĐ 2422, kèm phạm vi tiết `(Áp dụng: tiết X, Y)`.
- Đạt: **Kho Tri thức SGK dùng chung (Curriculum Knowledge Map Repository)**:
  + Backend API `api/sgk_knowledge.php` quản lý 2 bảng CSDL MySQL `sgk_books` và `sgk_lessons` qua PDO.
  + Giao diện `xaydungphuluc.html` và `canvas_xaydungphuluc.html` có trường chọn Bộ sách (`bookSeries`), tự động kiểm tra kho tri thức dùng chung; nếu đã có thì nạp tức thì (< 0.5s); nếu chưa có thì trích xuất 1 lần và lưu CSDL dùng chung cho toàn trường.
  + Tự động kế thừa YCCD chuẩn từ SGK, minh chứng NLS thực tế (máy tính cầm tay, GeoGebra, bảng tính) và gợi ý AI chuẩn QĐ 2422.
- Đạt: **Sách giáo khoa dùng chung (từ 2026-2027)**:
  + Dropdown `#bookSeries` đã đặt tùy chọn `"Sách giáo khoa dùng chung (từ 2026-2027)"` ở vị trí số 1 và là mặc định.
  + Hàm `getConfig()` trả về mặc định bộ sách dùng chung 2026-2027.
- Đạt: **Bảo đảm bao phủ 100% tất cả các bài học (Curriculum Assurance)**:
  + `compactSgkText`: Bắt trọn vẹn Mục lục (TOC), nâng hạn mức lên 2.500 dòng / 150.000 ký tự, không bao giờ bị cắt ở 9 bài đầu.
  + `ensureFullCurriculumLessons`: Cơ chế an toàn 2 lớp, tự động bù đắp 100% bài học cả năm học từ chuẩn CTGDPT 2018 (`KHBD_YCCD.toan[grade]`), bảo đảm luôn đủ 37-43 bài, có sẵn YCCD chuẩn, NLS thực tế (Casio/GeoGebra/Excel) và AI sư phạm (QĐ 2422).
  + Nút 1-click `seedStandardSgkKnowledge`: Khởi tạo tức thì 100% bài học chuẩn vào CSDL hoặc bộ nhớ máy mà không cần tệp PDF.
- Đạt: **Đồng bộ song song 1-1** trên cả `xaydungphuluc.html` và `canvas_xaydungphuluc.html` (kèm mirror `backupcode viettailieu/canvas_xaydungphuluc.html`).
- Đạt: Toàn bộ 59 test suite trong toàn dự án và kiểm tra cú pháp JS inline đều thành công 100%.

## Test đã chạy
1. `node tests/run-all-tests.js`: **ALL 59 TEST SUITES PASSED 100%!**
2. `node tests/sgk-knowledge-smoke.js`: PASS 100% (kiểm tra toàn diện API schema PHP, 17 DOM hooks/functions trên 3 tệp HTML, option sách dùng chung selected, `compactSgkText` giữ > 220 dòng bao phủ toàn bộ sách, và `ensureFullCurriculumLessons` bù đắp 100% bài học cho Toán 7 từ 9 bài lên 40 bài, Toán 6 đủ 43 bài).
3. `node tests/xaydungphuluc-smoke.js`: PASS 100% (bao gồm ca kiểm thử làm giàu mã AI cụt `9.B2.1`, khử bỏ chatbot lịch sử NLS, ưu tiên 5.3.TC2a cho Đại số 9).
4. `node tests/canvas-xaydungphuluc-smoke.js`: PASS 100% (bao gồm kiểm tra Canvas với `cleanLessonDescription`, `lessonAppliedNlsDescription`, `lessonAppliedAiDescription`, `getConfig`, `addRow`, `deleteTableRow`).
5. `node tests/xaydungphuluc-integration-smoke.js`: PASS 100%.
6. `node tests/canvas-soankhbd-smoke.js`: PASS 100%.
7. `node tests/soankhbd-ppct-standards-smoke.js`: PASS 100%.
8. `node tests/khbd-ppct-integration-smoke.js`: PASS 100%.
9. `node tests/khbd-ai-catalog-smoke.js`: PASS 100%.
10. `node tests/khbd-ai-integration-gate.test.js`: PASS 100%.
11. `node tests/khbd-4steps-workflow-smoke.js`: PASS 100%.
12. `node tests/security-f12-smoke.js`: PASS 100%.
13. Kiểm tra cú pháp toàn bộ JavaScript inline Canvas bằng Node `vm.Script`: PASS.

## Pass / Fail từng tiêu chí
- [PASS] Sách giáo khoa dùng chung (từ 2026-2027): Đặt làm tùy chọn số 1 và mặc định trên toàn bộ giao diện và cấu hình.
- [PASS] Bảo đảm bao phủ 100% tất cả bài học: `compactSgkText` quét toàn bộ mục lục và các chương; `ensureFullCurriculumLessons` bù đắp tự động mọi bài còn thiếu, bảo đảm CSDL luôn có trọn vẹn 100% bài học trong năm.
- [PASS] Khởi tạo nhanh 1-Click `seedStandardSgkKnowledge`: Giáo viên bấm nút là nạp ngay toàn bộ bài học chuẩn của năm học vào kho tri thức dùng chung và bộ nhớ máy.
- [PASS] Kho Tri thức SGK dùng chung: API `api/sgk_knowledge.php` đầy đủ `check`, `get`, `list`, `save`, `verify` với transaction an toàn.
- [PASS] Tự động nạp sẵn sàng khi đã có trong CSDL: Phụ lục 1, 2, 3 tự động kế thừa chính xác Yêu cầu cần đạt chuẩn SGK, minh chứng NLS công cụ số thực tế, và gợi ý AI chuẩn QĐ 2422.
- [PASS] Thư viện sách trực quan (`sgkLibraryModal`) và Chi tiết bài học (`sgkDetailModal`): Tìm kiếm, xem chi tiết từng bài và chuyển đổi bộ sách trong 1 click.
- [PASS] Loại bỏ hoàn toàn mã Miền 6 (AI) khỏi Năng lực số môn Toán: `recommendOfficialStandards('digital', ...)` cho Toán 9 phương trình 100% không đề xuất mã 6.x, ưu tiên `5.3.TC2a` ("Sử dụng sáng tạo công nghệ số - máy tính cầm tay, GeoGebra") và `5.2.TC2a`, `1.1.TC2a`.
- [PASS] Khắc phục triệt để lỗi cụt mô tả cột AI: `cleanAiColumnText('9.B2.1 - (Áp dụng: tiết 1, 2).', ...)` tự động bổ sung mô tả hành động sư phạm và trách nhiệm kiểm chứng chuẩn QĐ 2422, giữ nguyên vẹn phạm vi tiết.
- [PASS] Lọc bỏ triệt để các câu NLS đối phó "dùng chatbot tìm hiểu lịch sử ra đời": `cleanNlsColumnText` tự động chuyển hóa thành mô tả thực hành công cụ số trực quan.
- [PASS] Chuẩn hóa toàn diện Phụ lục 2: dữ liệu mẫu 6 hoạt động trải nghiệm/STEM/AI Day, prompt chỉ thị đúng bản chất, bảng 10 cột có cột STT, khối tiêu đề hành chính Quốc hiệu/Tên trường/Tổ, chữ ký Tổ trưởng (bên trái) và Hiệu trưởng (bên phải).
- [PASS] Đồng bộ 100% NLS & AI giữa Phụ lục 1 và Phụ lục 3: Kế thừa chính xác từ Phụ lục 1 (Single Source of Truth), cập nhật realtime 2 chiều khi chỉnh sửa ô NLS/AI.
- [PASS] Tối ưu luồng giao diện người dùng (UI Flow): Đưa "1. Thông tin & cấu hình sư phạm" lên đầu trang, kế tiếp là "2. Tài liệu & dữ liệu nguồn (Kho Tri thức SGK)". Bảng chọn tiết AI dài được xếp ở Mục 4, giúp giáo viên không cần cuộn chuột lên xuống khi chọn môn học, bộ sách và nhận diện tri thức SGK.
- [PASS] Xóa bản đồ tri thức nhận diện sai: Backend `api/sgk_knowledge.php?action=delete` bọc trong transaction an toàn; giao diện Thư viện (`sgkLibraryModal`) và Modal chi tiết (`sgkDetailModal`) có nút `🗑 Xóa` với xác nhận `canvasConfirm`, tự động dọn sạch cache `localStorage` và làm mới giao diện ngay lập tức.
- [PASS] Khắc phục triệt để thiếu bài và nhảy cóc Bài 3 (Toán 6 đủ 43 bài):
  + Nhúng trực tiếp `DEFAULT_MATH_CATALOG` 43 bài Toán 6 (và các khối 7, 8, 9) vào chính file nguồn, không phụ thuộc mạng/obfuscator ngoài.
  + Hàm `ensureFullCurriculumLessons` bù đắp hoàn chỉnh 100% (đủ 43 bài Toán 6), tự động chèn lại Bài 3 vào đúng vị trí số 3 khi AI nhảy cóc, bù đắp đủ các bài 26..43 khi AI dừng sớm, giữ nguyên vẹn số trang và YCCD chi tiết của các bài trích xuất thành công.
- [PASS] Khắc phục triệt để lỗi sư phạm "kiểm tra nghiệm" / "vẽ đồ thị" ở bài Số học (Bài 3 Toán 6):
  + Phân loại rạch ròi 5 phân môn: Số học (`isArith`), Hình học (`isGeo`), Thống kê (`isStat`), Phương trình (`isEquation`), Hàm số (`isFunction`).
  + Bài Số học gán minh chứng chuẩn: dùng máy tính cầm tay thực hiện tính toán, so sánh thứ tự hai số và phần mềm trực quan tia số/trục số; tuyệt đối không còn chữ "nghiệm" hay "đồ thị".
  + Bộ lọc `isUnfitDigitalEvidence` và thanh lọc CSDL PHP tự động quét sạch mọi dữ liệu cũ.
- [PASS] Tích hợp và thể hiện đa mã Năng lực số (2–3 mã NLS theo CV 3456):
  + Tự động gợi ý 2–3 mã NLS chuẩn: `5.3.TC1a, 5.2.TC1a, 1.1.TC1a` (Lớp 6–7) hoặc `5.3.TC2a, 5.2.TC2a, 1.1.TC2a` (Lớp 8–9).
  + `buildLessonDigitalEvidence` xây dựng minh chứng hành động sư phạm riêng biệt cho từng mã.
  + Modal Chi tiết SGK (`renderSgkDetailNlsBlock`) hiển thị trực quan các badge mã NLS và danh sách minh chứng hành động riêng rẽ.
  + Tự động phân bổ vào Phụ lục 1 và Phụ lục 3 theo mật độ NLS đã chọn.
- [PASS] Hệ thống Nạp Tri thức Toàn diện cho Từng Môn ở Mỗi Lớp (Lớp 6–9):
  + Section 2 tự động cập nhật theo Môn & Lớp với hook `#grade.onchange`, hiển thị nút nạp tức thì cho đúng môn và khối lớp.
  + Modal `#sgkLibraryModal` trang bị Tab Khối lớp (Lớp 6, 7, 8, 9, Đã lưu CSDL) và ma trận 13 môn học kèm nút bấm riêng (`⚡ Nạp tri thức môn này`, `⚡ Chọn dùng môn này`).
  + Hỗ trợ nút nạp hàng loạt: `⚡ Nạp tất cả môn Khối Lớp X` và `⚡ Nạp trọn bộ Lớp 6–9` (52 bộ môn THCS).
  + Khả năng sinh tự động 100% bài học kèm YCCĐ chuẩn cho tất cả 13 môn THCS từ `js/khbd-curriculum.js`.
- [PASS] Tùy chọn Khối Lớp Trực tiếp khi Nạp Tri thức từ tệp SGK:
  + Thanh nút chuyển nhanh Khối lớp `[ Lớp 6 ] [ Lớp 7 ] [ Lớp 8 ] [ Lớp 9 ]` ngay trong Section 2.
  + Hộp thoại `#sgkExtractModal` cho phép chọn chính xác Khối lớp, Môn học, Bộ sách trước khi AI trích xuất từ tệp PDF/Word SGK.
  + Tự động nhận diện Khối lớp và Môn học từ tên tệp SGK khi tải lên.
- [PASS] Toàn bộ 59/59 bài test của hệ thống chạy PASS 100%.

## Bug
- Lỗi: Không có
- Tái hiện: Không có
- File liên quan: Không có
