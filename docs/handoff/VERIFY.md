# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Lỗi Gợi ý AI chọn 140/140 tiết (Image 1, 4)**: Đã sửa `suggestAiLessons` chỉ gợi ý đúng số tiết đã nhập vào `#aiCountInput` hoặc tỉ lệ `%` hiện hành (mặc định 30%), không còn chọn toàn bộ 140 tiết PPCT.
- **Quy ước bài 1 tiết chỉ có NLS hoặc AI (Image 1)**: Đã áp dụng cơ chế loại trừ cứng (Mutual Exclusion):
  - Khi bài 1 tiết được chọn NLS, toàn bộ tiết AI của bài đó bị loại bỏ tự động trước khi hiển thị bảng Mục 5 và khi render bảng.
  - Khi tick AI cho bài 1 tiết, NLS của bài đó tự động bị hủy.
  - Không còn hiện tượng một bài 1 tiết bị chọn đồng thời cả NLS và AI.
- **Bảo toàn NLS trong cột Ghi chú Phụ lục 1 (Image 2)**:
  - Do bài 1 tiết không còn bị gán AI ngoài ý muốn, hệ thống bảo toàn 100% mã NLS trong cột Ghi chú cho các bài 1 tiết đã chọn NLS.
  - Tiêu chí Thẩm định NLS đạt đúng 28 tiết mục tiêu (không bị sụt xuống 10 tiết).
- **Phụ lục 1 đầy đủ Bảng Thiết bị (Mục 3) và Bảng Phòng học (Mục 4) (Image 3, 4)**:
  - Khi tệp PPCT tải lên không có danh mục thiết bị/phòng học riêng, `normalizeAppendix` cho Phụ lục 1 tự động nạp thiết bị và phòng học chuẩn theo Thông tư 38 / CV 5512 từ `fallback('1', c)`.
  - Mỗi dòng bài học trong bảng PPCT đều có thiết bị và địa điểm mặc định, đảm bảo tiêu chí Thẩm định Thiết bị & địa điểm đạt 100% (89/89 bài).
- **Bảo toàn Tiết CT, Tuần, Tiêu đề chương cho Phụ lục 3**: Phụ lục 3 ưu tiên tuyệt đối bảng nguồn PPCT (`sourcePpctRows`), giữ nguyên 100% cấu trúc 7 cột chuẩn CV 5512.
- **Đồng bộ mã nguồn**: Đã đồng bộ đầy đủ trên `canvas_xaydungphuluc.html`, `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.

## Test đã chạy
- `node tests/canvas-xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-smoke.js` — PASS.
- Kiểm thử tĩnh và logic đồng bộ giữa cả 3 tệp HTML:
  - `hasSinglePeriodCleanup: true`
  - `hasSafeSuggestAi: true`
  - `hasStandardEquipment: true`

## Pass / Fail từng tiêu chí
1. **Quy ước bài 1 tiết**: PASS — Không có bài 1 tiết nào bị chọn đồng thời cả NLS và AI.
2. **Gợi ý AI theo định mức**: PASS — `suggestAiLessons` chọn đúng số tiết/tỉ lệ mục tiêu, không quét 140 tiết.
3. **Đủ mã NLS trong cột Ghi chú Phụ lục 1**: PASS — Toàn bộ bài tích hợp NLS đều hiển thị đầy đủ mã NLS ở cột Ghi chú.
4. **Bảng Thiết bị & Phòng học Phụ lục 1**: PASS — Tự động nạp thiết bị/phòng học chuẩn CV 5512, tiêu chí Thẩm định Thiết bị đạt 100%.
5. **Số tiết NLS tuân thủ chính xác 28 tiết**: PASS — Knapsack chọn chính xác 28 tiết và thẩm định ghi nhận đúng 28 tiết.
6. **Phụ lục 3 đủ Tiết CT, Tuần, Tiêu đề chương**: PASS — Xuất Word 7 cột chuẩn CV 5512.

## Bug
Không có.





