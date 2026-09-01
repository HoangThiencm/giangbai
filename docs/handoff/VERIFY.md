# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Làm sạch 100% cột "Yêu cầu cần đạt" ở Phụ lục 1: Loại bỏ toàn bộ các câu dẫn quy chuẩn/boilerplate ("Nguồn bắt buộc...", "Căn cứ pháp lý...", "Bài SGK:", "Nội dung CTGDPT 2018 tham chiếu:"), chỉ giữ lại các gạch đầu dòng mục tiêu hành vi chuẩn của học sinh.
- [x] Nâng cấp thuật toán so khớp bài học trong `js/khbd-yccd.js`: Ưu tiên tuyệt đối theo số hiệu bài học (`Bài <số>`), tên bài học chuẩn hóa rồi mới đến tính điểm từ khóa. Bài 14 Số nguyên ("Phép cộng và phép trừ số nguyên") khớp chính xác 100% YCCĐ của số nguyên, không còn bị gán nhầm sang Bài 11 ("Ước chung. Ước chung lớn nhất").
- [x] Sinh mã NLS đa dạng bám sát mật độ `nlsDensity` cấu hình (`1–2` -> 1 mã, `2–3` -> 2 mã, `3–4` -> 3 mã).
- [x] Chuyển đổi toàn bộ file Word xuất ra (.docx) của Phụ lục 1, Phụ lục 2, Phụ lục 3 sang khổ **Nằm ngang (Landscape)** với kích thước `16838 x 11906` và lề cân đối 1134 twips (2cm), giúp bảng 7-8 cột hiển thị rộng rãi, không bị bó hẹp.
- [x] Bộ test tự động `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đạt 100% PASS.

## Test đã chạy
1. `node tests/xaydungphuluc-smoke.js` — PASS 100%
2. `node tests/xaydungphuluc-integration-smoke.js` — PASS 100%

## Pass / Fail từng tiêu chí
- [x] Yêu cầu cần đạt sạch, không chứa metadata quy chuẩn: PASS
- [x] Khớp chính xác bài học và YCCĐ (Bài 14 khớp đúng số nguyên): PASS
- [x] Mã NLS sinh đa dạng theo đúng mật độ: PASS
- [x] Xuất file Word (.docx) khổ nằm ngang Landscape: PASS
- [x] Test tự động smoke & integration: PASS

## Bug
- Không phát hiện lỗi.