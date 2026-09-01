# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Tái cấu trúc thành công luồng sinh YCCĐ Phụ lục 1 theo mô hình RAG Sư phạm: truyền đầy đủ danh sách PPCT nguồn và ngữ cảnh CTGDPT 2018 vào prompt để AI ghép 1-kèm-1 cho từng bài học.
- [x] `cleanAppendixOutcome` giữ nguyên vẹn kết quả YCCĐ chất lượng cao, đúng trọng tâm của AI cho từng bài; không còn bị CSDL tĩnh theo chủ đề lớn đè bẹp.
- [x] Cơ chế ghép bài `lessonsMatch` tổng quát hóa qua số bài (`lessonOrdinal`), tên bài làm sạch và độ chồng khớp từ khóa động, áp dụng tốt cho mọi môn học (Toán, Văn, KHTN, Sử, Địa...).
- [x] Bảo đảm tính duy nhất trong ghép nối bằng `usedGenerated`, loại bỏ hoàn toàn hiện tượng dồn toa hoặc trùng lặp.
- [x] Cột NLS/AI và xuất Word (.docx) A4 ngang hoạt động chuẩn xác, sạch sẽ không có `[object Object]`.
- [x] Mục 4 tách 3 ô input thống kê (`Số lớp`, `Số học sinh`, `Số giáo viên`) và đồng bộ lên bản nháp/xuất Word.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Pass / Fail từng tiêu chí
- [x] PASS: Phụ lục 1 sinh YCCĐ riêng biệt, đúng 1–3 gạch đầu dòng trọng tâm cho từng bài học.
- [x] PASS: Áp dụng đa môn và đa bộ sách không cần hardcode thủ công từng bài.
- [x] PASS: Cột NLS/AI bóc tách chuỗi an toàn 100%.
- [x] PASS: Xuất Word A4 ngang, lề 20mm, tỉ lệ cột riêng biệt cho từng bảng.

## Bug
- Không có.
