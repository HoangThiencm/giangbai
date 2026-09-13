# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- **Khóa chặn & Popup số tiết khi chọn thủ công NLS/AI**:
  - Khi tick chọn thủ công từng bài NLS (`toggleNlsLesson`) hoặc từng tiết/cả bài AI (`toggleAiLesson`, `toggleAiLessonRow`): hệ thống hiển thị thông báo (toast/popup) tức thì số tiết đã chọn, số tiết mục tiêu và số tiết còn lại (`Đã chọn X/Y tiết. Còn lại: Z tiết`).
  - Khi chọn vượt quá hạn mức mục tiêu (`current + periods > target`): hệ thống tự động hoàn tác checkbox (`el.checked = false`), chặn không cho chọn thêm và hiển thị cảnh báo giới hạn rõ ràng kèm số tiết còn lại.
  - Hạn mức mục tiêu (`manualAllocationTargets`) được bảo toàn độc lập, không bị thao tác chọn/bỏ từng bài ghi đè mất giá trị cài đặt ban đầu.
- **Quy ước bài 1 tiết chỉ có NLS hoặc AI (Mutual Exclusion)**:
  - Khi bài 1 tiết được chọn NLS, AI của bài đó tự động bị hủy/loại bỏ.
  - Khi tick chọn AI cho bài 1 tiết, NLS của bài đó tự động bị hủy.
  - Loại bỏ hoàn toàn trường hợp một bài 1 tiết vừa có NLS vừa có AI.
- **Gợi ý AI theo đúng định mức / tỉ lệ**:
  - `suggestAiLessons` tuân thủ đúng số tiết nhập tại `#aiCountInput` hoặc tỉ lệ `%` thiết lập (mặc định 30%), không quét toàn bộ 140 tiết PPCT.
- **Bảo toàn mã NLS trong cột Ghi chú Phụ lục 1**:
  - Cột Ghi chú giữ đầy đủ mã NLS cho các bài tích hợp NLS, tiêu chí thẩm định NLS đạt chuẩn 100%.
- **Bảng Thiết bị & Phòng học Phụ lục 1**:
  - Khi tệp PPCT tải lên thiếu bảng thiết bị/phòng học riêng, hệ thống tự động nạp danh mục chuẩn Thông tư 38 / CV 5512 từ `fallback('1', c)`, đảm bảo 100% dòng bài có thiết bị và địa điểm.
- **Phụ lục 3 bảo toàn cấu trúc PPCT nguồn**:
  - Giữ nguyên các dòng tiêu đề (Học kì, Chương/Chủ đề), cột Tiết CT và cột Tuần theo đúng 7 cột chuẩn CV 5512.
- **Đồng bộ mã nguồn**:
  - Đồng bộ logic trên cả 3 tệp: `canvas_xaydungphuluc.html`, `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.

## Test đã chạy
- `node tests/canvas-xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-smoke.js` — PASS.
- `node tests/backupcode-canvas-smoke.js` — PASS.

## Pass / Fail từng tiêu chí
1. **Popup & Chặn chọn thủ công vượt hạn mức**: PASS — Hiển thị số tiết đã chọn/còn lại, chặn và hoàn tác checkbox khi vượt hạn mức.
2. **Quy ước bài 1 tiết (NLS/AI loại trừ lẫn nhau)**: PASS — Không trùng lặp NLS và AI trên bài 1 tiết.
3. **Gợi ý AI theo định mức**: PASS — Không chọn tràn 140 tiết, tuân thủ đúng mục tiêu.
4. **Mã NLS cột Ghi chú Phụ lục 1**: PASS — Đầy đủ mã NLS, thẩm định đạt chuẩn.
5. **Bảng Thiết bị & Phòng học Phụ lục 1**: PASS — Nạp fallback chuẩn TT 38 / CV 5512.
6. **Phụ lục 3 bảo toàn Tiết CT, Tuần, Tiêu đề**: PASS — Giữ nguyên bảng 7 cột chuẩn.

## Bug


