# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Mở rộng giao diện hiển thị toàn màn hình (`w-full max-w-[98%] 2xl:max-w-[1750px]`), loại bỏ hiện tượng co cụm chữ trong bảng PPCT và Bảng chọn tiết AI.
- [x] Chuẩn hóa duy nhất 1 cột "Mã NLS & AI (CV 3456 & QĐ 2422)" qua adapter `normalizeIntegrationTable`, loại bỏ triệt để lỗi nhân đôi cột khi xem trước và khi xuất DOCX.
- [x] Thiết lập quy trình 4 bước chuẩn hóa:
  * Bước 1: Chọn file PPCT -> Bấm nút "🔍 Nhận diện PPCT" (`recognizeStagedPpct`) -> Bóc tách và hiển thị ngay bảng PPCT ở Mục 3 và Mục 7.
  * Bước 2: Chọn file SGK -> Bấm nút "📖 Đọc SGK" (`readStagedSgk`) -> Gửi AI phân tích ngữ cảnh SGK và xuất thông báo nổi bật "✓ Đã hiểu thông tin SGK".
  * Bước 3: Người dùng tick chọn tiết tích hợp Khung AI (tối đa 12 tiết chuẩn) trên bảng mở rộng.
  * Bước 4: Bấm sinh phụ lục (1, 2, 3) với hệ thống mã NLS chuẩn (TT 02 / CV 3456: `.TC1a` / `.TC2a`) và mã Khung AI chuẩn (QĐ 2422: `6.A1.1`, `7.A1.1`...) từ `js/khbd-standards.js` và YCCĐ chuẩn từ `js/khbd-yccd.js`.
- [x] Tự động nạp "Yêu cầu cần đạt" từ dữ liệu chuẩn CT GDPT 2018 cho Phụ lục 1.
- [x] Dọn dẹp mã nguồn, không còn hàm trùng lặp trong thẻ `<script>`.

## Test đã chạy
1. `node tests/xaydungphuluc-smoke.js` — PASS 100%
2. `node tests/xaydungphuluc-integration-smoke.js` — PASS 100%

## Pass / Fail từng tiêu chí
- [x] Giao diện mở rộng toàn màn hình không bị bóp nghẹt: PASS
- [x] Bảng kết quả Phụ lục 1, Phụ lục 3 chỉ có duy nhất 1 cột NLS & AI: PASS
- [x] Nút "🔍 Nhận diện PPCT" và nút "📖 Đọc SGK" hoạt động độc lập, có trạng thái "Đã hiểu thông tin SGK": PASS
- [x] Tích hợp `js/khbd-standards.js` và `js/khbd-yccd.js`, sinh mã chuẩn xác theo từng bài học: PASS
- [x] Phụ lục 1 tự động điền YCCĐ chuẩn: PASS
- [x] Bộ test tự động smoke & integration: PASS

## Bug
- Không phát hiện lỗi mới.