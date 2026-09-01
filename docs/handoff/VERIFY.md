# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Định dạng Yêu cầu cần đạt luôn được tách thành các dòng gạch đầu dòng `- ` rõ ràng, loại bỏ hoàn toàn hiện tượng dính dấu phẩy thành một dòng dài.
- [x] Phân rã chi tiết 100% YCCĐ cho toàn bộ 43 bài học Toán 6 (Bài 1–43); các bài liền kề như Bài 13, 14, 15, 16, 17 và Bài 18, 19, 20 đều nhận đúng YCCĐ trọng tâm riêng biệt.
- [x] Cơ chế theo dõi tiêu đề chương (Chapter Context Tracker) giúp các bài Luyện tập chung, Ôn tập chương nhận đúng YCCĐ củng cố của chương hiện hành (Số tự nhiên, Số nguyên, Phân số, Hình học phẳng hay Thống kê).
- [x] Tách 3 ô input thống kê và chuẩn hóa xuất Word A4 ngang có tỉ lệ cột riêng biệt cho từng bảng.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Pass / Fail từng tiêu chí
- [x] PASS: `formatOutcomeLines` bẻ câu dính dấu phẩy trước động từ hành vi thành các gạch đầu dòng `- `.
- [x] PASS: Toàn bộ 43 bài học Toán 6 có YCCĐ riêng biệt, không bị trùng lặp nguyên khối.
- [x] PASS: Bài Ôn tập chương I / III nhận đúng mạch Số học; Ôn tập hình học nhận đúng mạch Hình học.
- [x] PASS: 100% các bài kiểm thử tự động chạy đạt PASS.

## Bug
- Không có.
