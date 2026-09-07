# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đạt: Khắc phục triệt để việc sót lại dấu `]` ở cuối câu mô tả NLS và AI khi có dấu chấm `.`, phẩy `,`, chấm phẩy `;` hoặc đứng trước cụm `(Áp dụng: tiết …)`.
- Đạt: Bộ điều khiển phân bổ NLS thông minh theo số tiết & AI (1 tiết: 2 mã; ≥2 tiết có AI: 2 mã; ≥2 tiết không AI: tùy chọn 2–3 mã) trên UI Mục 4 của cả hai giao diện.
- Đạt: Cột AI trong Phụ lục 1 để ô trống hoàn toàn (chuỗi rỗng `''`) đối với bài không có tích hợp AI; xuất Word DOCX để ô trống.
- Đạt: Timeout client/proxy đồng nhất 120s cho tài liệu cả năm học.
- Đạt: Bảo toàn định dạng Phụ lục 3 và không tác động ngoài scope.

## Test đã chạy
1. `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
2. `node tests/xaydungphuluc-smoke.js`: PASS.
3. `node tests/xaydungphuluc-integration-smoke.js`: PASS.
4. Kiểm thử hồi quy regex làm sạch:
   - `cleanNlsColumnText('[NLS: 5.3.TC2a - Sử dụng phần mềm GeoGebra].')` -> `"5.3.TC2a - Sử dụng phần mềm GeoGebra."` (PASS: sạch dấu `]`).
   - `cleanNlsColumnText('[NLS: 5.3.TC2a - Sử dụng phần mềm GeoGebra],')` -> `"5.3.TC2a - Sử dụng phần mềm GeoGebra"` (PASS).
   - `cleanNlsColumnText('[NLS: 5.3.TC2a - Sử dụng phần mềm GeoGebra] .')` -> `"5.3.TC2a - Sử dụng phần mềm GeoGebra."` (PASS).
   - `cleanAiColumnText('[AI: 8.A1.1 - Học sinh sử dụng AI]. (Áp dụng: tiết 1).')` -> `"8.A1.1 - Học sinh sử dụng AI. (Áp dụng: tiết 1)."` (PASS: sạch dấu `]`).
   - `cleanAiColumnText('[AI: 8.A1.1 - Học sinh sử dụng AI] (Áp dụng: tiết 1).')` -> `"8.A1.1 - Học sinh sử dụng AI (Áp dụng: tiết 1)."` (PASS).
   - `cleanAiColumnText('[AI: 8.A1.1 - Học sinh sử dụng AI].')` -> `"8.A1.1 - Học sinh sử dụng AI."` (PASS).
   - `cleanAiColumnText('8.A1.1 - Học sinh sử dụng AI]')` -> `"8.A1.1 - Học sinh sử dụng AI"` (PASS).
   - `cleanAiColumnText('')` -> `""` (PASS: ô rỗng).
5. Kiểm thử phân bổ NLS: bài 1 tiết -> 2 mã; bài ≥2 tiết có AI -> 2 mã; bài ≥2 tiết không AI -> 2-3 mã: PASS.

## Pass / Fail từng tiêu chí
- [PASS] Loại bỏ triệt để dấu `]` ở cuối câu mô tả NLS kể cả khi có dấu chấm `].` hoặc `] .`.
- [PASS] Loại bỏ triệt để dấu `]` trong mô tả AI khi nằm trước dấu chấm hoặc trước cụm `(Áp dụng: tiết X)`.
- [PASS] Giao diện Mục 4 có bộ chọn phân bổ NLS theo tiết & AI trực quan và đồng bộ cấu hình.
- [PASS] Cột AI để trống hoàn toàn (chuỗi rỗng `''`) khi không chọn AI.
- [PASS] Toàn bộ 3 bộ smoke tests chạy thành công.

## Bug
Không có.
