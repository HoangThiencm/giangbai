# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đạt: **Khắc phục triệt để lỗi sót `$..$` trong Word DOCX (Phụ lục 3 & Toàn bộ Phụ lục)**:
  + Chuyển đổi 100% công thức toán học thành đối tượng Microsoft Word Equation native (`<m:oMath>`, `<m:f>`, `<m:rad>`, `<m:sSup>`, `<m:eqArr>`).
  + Bổ sung `pushMarkerWithMath` trong `parseInlineTextToRuns` (`js/khbd-docx.js`): Giải mã toàn bộ công thức toán học nằm trong các badge `[NLS: ...]` và `[AI: ...]` thành Word Equation, giữ nguyên định dạng màu sắc/shading của nhãn.
  + Nâng cấp `autoWrapMathInDelimiters`: Tiền chuẩn hóa số mũ Unicode (`²`, `³` -> `^2`, `^3`), ký hiệu Hy Lạp (`Δ`, `π`, `α`), hỗ trợ ngoặc nhọn lồng nhau `\{(?:[^{}]|\{[^{}]*\})*\}` cho phân số/căn thức.
  + Xác minh tệp Word XML: 100% không còn bất kỳ ký tự `$..$` thô nào.
- Đạt: **Rà soát Chuẩn hóa Phụ lục 2 theo Công văn 5512**:
  + Đầy đủ **10 cột dữ liệu**: `STT | Chủ đề (1) | Yêu cầu cần đạt (2) | Số tiết (3) | Thời điểm (4) | Địa điểm (5) | Chủ trì (6) | Phối hợp (7) | Điều kiện thực hiện (8) | Mã NLS & AI (CV 3456 & QĐ 2422)`.
  + Gồm **6 hoạt động thực hành trải nghiệm, chuyên đề STEM và ngày hội AI Day** rải đều 2 học kỳ.
  + Thể thức hành chính chuẩn (Quốc hiệu, Tiêu ngữ, Trường/Tổ, căn cứ CV 5512) và chữ ký đúng thẩm quyền: bên trái `TỔ TRƯỞNG`, bên phải `HIỆU TRƯỞNG`.
- Đạt: **Khắc phục triệt để lỗi so khớp bài học trong `lessonsMatch` & Đồng bộ 100% NLS & AI giữa Phụ lục 1 và Phụ lục 3**:
  + Ưu tiên kiểm tra `lessonOrdinal` trước: Không cho phép nhận nhầm Bài 1 ("Bài 1. Khái niệm...") và Bài 2 ("Bài 2. Giải hệ...").
  + Phụ lục 3 kế thừa 100% mã NLS, mã AI, mô tả hành động sư phạm và phạm vi tiết `(Áp dụng: tiết ...)` từ Phụ lục 1 (Single Source of Truth).
  + Chỉnh sửa trực tiếp tại Phụ lục 1 tự động đồng bộ sang Phụ lục 3 ngay lập tức.
- Đạt: **Hỗ trợ Đa mã Năng lực AI (Multi-Code AI theo QĐ 2422)**:
  + Trang bị cặp đôi mã AI kết hợp Miền A (Làm chủ kỹ thuật) và Miền B/D (Đạo đức, Trách nhiệm, Phản biện) cho từng bài học.
  + Tự động cấp 2 mã AI khi chọn mật độ `2–3 mã/bài` hoặc bài học có từ 2 tiết AI trở lên.
  + Modal Chi tiết bài học SGK hiển thị Badge màu tím riêng biệt và danh sách hành động sư phạm tương ứng.
- Đạt: **Phân hóa Triệt để Năng lực số (NLS) và Trợ lý AI theo Cấp độ Nhận thức từng Bài học**:
  + Bài 1 (Khái niệm): NLS `1.1.TC2a, 5.3.TC2a, 3.1.TC2a`, MTCT (CALC) kiểm tra $(x_0; y_0)$ có là nghiệm không; AI tạo ví dụ kiểm tra định nghĩa. Tuyệt đối không còn "các bước giải" hay "vẽ đồ thị nghiệm".
  + Bài 2 (Giải hệ): NLS `5.3.TC2a, 5.1.TC2a, 5.2.TC2a`, MTCT chức năng giải hệ EQUATION/SIMULT đối chiếu phương pháp thế/cộng đại số, GeoGebra minh họa nghiệm giao điểm 2 đường thẳng, AI định hướng giải tối ưu.
  + Bài 3 (Toán thực tế): NLS `3.1.TC2a, 5.3.TC2a, 1.2.TC2a`, Excel/Sheets lập bảng phân tích đại lượng, MTCT giải hệ và đối chiếu điều kiện thực tế, AI phản biện bước chọn ẩn số.
- Đạt: **Sách giáo khoa dùng chung (từ 2026-2027)** và **Kho Tri thức SGK dùng chung**:
  + Mặc định số 1 trên toàn bộ giao diện, backend PDO MySQL với transaction an toàn.
  + Bao phủ 100% bài học (Toán 6 đủ 43 bài, Toán 7 đủ 37 bài, Toán 8 đủ 39 bài, Toán 9 đủ 32 bài).
- Đạt: **Đồng bộ 1-1 Tuyệt đối**:
  + `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` đạt **100% BYTE-IDENTICAL** (334,526 bytes).
- Đạt: **Toàn bộ 61 test suites trong toàn dự án PASS 100%**.

## Test đã chạy
1. `node tests/run-all-tests.js`: **ALL 61 TEST SUITES PASSED 100%!**
2. `node tests/xaydungphuluc-math-smoke.js`: **PASS 100%** (6/6 mục kiểm tra: Equation OMML trong Word, Phụ lục 3 sạch 100% dấu `$`, Phụ lục 2 đủ 10 cột, PL1 và PL3 đồng bộ 100% NLS/AI).
3. `node tests/sgk-knowledge-smoke.js`: **PASS 100%** (10/10 mục kiểm tra: API schema PHP, 17 DOM hooks, compactSgkText, ensureFullCurriculumLessons đủ 43 bài Toán 6, phân hóa YCCĐ Toán 7-9, phân hóa NLS & AI Toán 9 Bài 1-3, Multi-Code AI QĐ 2422).
4. `node tests/xaydungphuluc-smoke.js`: PASS 100%.
5. `node tests/canvas-xaydungphuluc-smoke.js`: PASS 100%.
6. `node tests/xaydungphuluc-integration-smoke.js`: PASS 100%.
7. `node tests/canvas-soankhbd-smoke.js`: PASS 100%.
8. `node tests/soankhbd-ppct-standards-smoke.js`: PASS 100%.
9. `node tests/khbd-ppct-integration-smoke.js`: PASS 100%.
10. `node tests/khbd-ai-catalog-smoke.js`: PASS 100%.
11. `node tests/khbd-ai-integration-gate.test.js`: PASS 100%.
12. `node tests/khbd-4steps-workflow-smoke.js`: PASS 100%.
13. `node tests/security-f12-smoke.js`: PASS 100%.
14. Kiểm tra cú pháp toàn bộ JavaScript inline Canvas bằng Node `vm.Script`: PASS.

## Pass / Fail từng tiêu chí
- [PASS] Xuất Word Phụ lục 3 & Các phụ lục sạch 100% dấu `$`: Mọi biểu thức toán học đều là Microsoft Word Equation (`<m:oMath>`), không còn ký tự LaTeX `$..$` thô.
- [PASS] Rà soát Phụ lục 2 đảm bảo 100% chuẩn CV 5512: Đủ 10 cột dữ liệu, 6 hoạt động trải nghiệm/STEM/AI Day, tích hợp NLS và AI, khối hành chính và chữ ký đúng thẩm quyền (Tổ trưởng & Hiệu trưởng).
- [PASS] Đồng bộ 100% NLS và AI giữa Phụ lục 1 và Phụ lục 3: Kế thừa 100% từ Phụ lục 1 (Single Source of Truth), khắc phục triệt để lỗi `lessonsMatch` nhận nhầm Bài 1 và Bài 2.
- [PASS] Hỗ trợ Đa mã Năng lực AI (Multi-Code AI theo QĐ 2422): Cặp đôi mã Miền A + Miền B/D, hỗ trợ mật độ 2–3 mã/bài, Modal chi tiết hiển thị badge tím trực quan.
- [PASS] Phân hóa Triệt để NLS & AI theo Cấp độ Nhận thức: Bài 1 (Khái niệm), Bài 2 (Giải hệ), Bài 3 (Toán thực tế) phân hóa hoàn toàn, xóa bỏ dập khuôn.
- [PASS] Bao phủ 100% bài học trong năm học: Toán 6 (43 bài), Toán 7 (37 bài), Toán 8 (39 bài), Toán 9 (32 bài) có sẵn YCCĐ riêng biệt, NLS thực tế và AI sư phạm.
- [PASS] Sách giáo khoa dùng chung (từ 2026-2027): Đặt làm mặc định số 1.
- [PASS] Đồng bộ 100% byte-identical cho Canvas: `canvas_xaydungphuluc.html` và bản mirror `backupcode viettailieu/canvas_xaydungphuluc.html` (334,526 bytes).
- [PASS] Toàn bộ 61/61 test suites chạy PASS 100%.

## Bug
- Lỗi: Không có
- Tái hiện: Không có
- File liên quan: Không có


