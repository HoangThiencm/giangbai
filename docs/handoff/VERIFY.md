# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] `js/khbd-standards.js`: Đã xóa bỏ hoàn toàn 3 mục Miền 6 (`6.1`, `6.2`, `6.3`) khỏi `KHBD_STANDARDS.digital.entries`.
- [x] `js/khbd-standards.js`: NLS thu gọn chuẩn xác còn đúng 21 mục cho Lớp 6–7 (`TC1a`) và 21 mục cho Lớp 8–9 (`TC2a`) thuộc 5 Miền nền tảng (CV 3456).
- [x] `js/khbd-standards.js`: Đã loại bỏ logic cấm cứng `isMath && /^6\./` trong `isUnnaturalOfficialStandard` và nhánh chấm điểm `Ứng dụng trí tuệ nhân tạo` của NLS.
- [x] `js/khbd-standards.js`: Bảo toàn 100% danh mục 88 YCCĐ chuẩn QĐ 2422 (4 Miền A, B, C, D) cho các khối lớp 6, 7, 8, 9.
- [x] `soankhbd.html` & `canvas_soankhbd.html`: Cập nhật tiêu đề Khối 3: "Phương pháp dạy học & Năng lực số (TT 02 / CV 3456 - 5 Miền nền tảng)"; mô tả và nhãn checkbox ghi rõ 5 Miền; panel NLS chỉ hiển thị 5 Miền.
- [x] `soankhbd.html` & `canvas_soankhbd.html`: Khối AI đứng độc lập là "✨ Tích hợp Khung Năng lực AI (QĐ 2422/QĐ-BGDĐT)", giải thích rõ 4 Miền A–D theo lớp.
- [x] `js/khbd-app.js`: `standardsOfKind("digital")` lọc sạch mã `6.x.TC` và ID `tt02-*-6-*` cũ; phân định rạch ròi giữa NLS và AI.
- [x] `js/khbd-prompts.js`: `SYSTEM_ROLE` và `GENERATE_OBJECTIVES` khẳng định NLS gồm 5 Miền (CV 3456) và AI gồm 4 Miền (QĐ 2422), cấm lẫn lộn mã AI vào NLS.
- [x] `canvas_xaydungphuluc.html` & `xaydungphuluc.html`: Đồng bộ quy chuẩn NLS Miền 1–5 và AI QĐ 2422.
- [x] `tests/khbd-ai-catalog-smoke.js`: Đã cập nhật chỉ số kiểm thử 21 mục NLS cho cả 2 dải lớp và khẳng định NLS không chứa mã Miền 6.

## Test đã chạy
- `node tests/khbd-ai-catalog-smoke.js`: PASS (21 mục NLS L6–7, 21 mục NLS L8–9, 88 mục AI QĐ 2422)
- `node tests/khbd-4steps-workflow-smoke.js`: PASS (Kiểm thử quy trình 4 bước và khung mã NLS 5 Miền & AI QĐ 2422)
- `node tests/khbd-integrations-smoke.js`: PASS (Khóa gate tích hợp NLS và AI)
- `node tests/khbd-competencies-smoke.js`: PASS (Khung năng lực chung và đặc thù)
- `node tests/khbd-subject-integrations-smoke.js`: PASS (Tích hợp bối cảnh theo môn)
- `node tests/khbd-recommendation-flow-smoke.js`: PASS (Luồng đề xuất PPDH / NLS / AI)
- `node tests/soankhbd-ppct-standards-smoke.js`: PASS (Chuẩn hóa chuẩn tích hợp từ PPCT)
- `node tests/khbd-ai-integration-gate.test.js`: PASS (Gate bật/tắt AI tích hợp)
- `node tests/xaydungphuluc-smoke.js`: PASS (Đồng bộ Phụ lục 1, 2, 3)
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS (Đồng bộ Phụ lục bản Canvas)
- `node tests/canvas-soankhbd-smoke.js`: PASS (Đồng bộ Canvas Soạn KHBD 1-1)

## Pass / Fail từng tiêu chí
- **Tiêu chí 1**: Miền 6 (AI) được loại bỏ hoàn toàn khỏi danh mục Năng lực số (CV 3456) -> PASS
- **Tiêu chí 2**: NLS chuẩn hóa đúng 5 Miền nền tảng với 21 năng lực thành phần cho Lớp 6–7 và 21 năng lực thành phần cho Lớp 8–9 -> PASS
- **Tiêu chí 3**: Khung Năng lực AI hoạt động độc lập theo chuẩn QĐ 2422 với 4 Miền (A, B, C, D) và đủ 88 YCCĐ -> PASS
- **Tiêu chí 4**: Giao diện `soankhbd.html` và `canvas_soankhbd.html` phân định rạch ròi giữa Khối 3 (NLS 5 Miền) và Khối AI (QĐ 2422) -> PASS
- **Tiêu chí 5**: Prompt Gemini và Kế hoạch bài dạy sinh ra không còn tình trạng trùng lặp mục tiêu AI trong NLS -> PASS
- **Tiêu chí 6**: Các tệp Phụ lục 5512 giữ vững tính đồng bộ cột NLS và cột AI -> PASS
- **Tiêu chí 7**: Toàn bộ các bộ smoke tests liên quan chạy thành công 100% -> PASS

## Bug
Không phát hiện lỗi.
