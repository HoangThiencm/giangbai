# IMPLEMENT: Khớp YCCĐ chính xác và chuẩn hóa xuất Word Phụ lục 5512

## Phạm vi đã triển khai

- Bổ sung chuẩn hóa tên/chủ đề, từ khóa toán học cốt lõi và ngữ cảnh bài trước cho `findOfficialYccdRows`. Bài luyện tập, ôn tập và thực hành lấy YCCĐ của chủ đề gần nhất thay vì rơi về bài đầu tiên.
- Loại bỏ hoàn toàn fallback theo chỉ số `generatedRows[normal]` trong Phụ lục 1. Tên bài được khớp mờ theo tên đã làm sạch và từ khóa chủ đề.
- Áp dụng chuỗi dự phòng YCCĐ: CSDL CTGDPT 2018, trích xuất mục tiêu từ ngữ cảnh SGK, AI đã qua kiểm tra ngữ nghĩa, rồi khung sư phạm theo loại bài. Các tên bài lạ không còn nhận nội dung của bài khác.
- Thêm khung `generatePedagogicalOutcome` cho bài lý thuyết, luyện tập/ôn tập, kiểm tra đánh giá và STEM/trải nghiệm.
- Cho phép sửa trực tiếp ô Yêu cầu cần đạt trong bảng xem trước Phụ lục 1; thay đổi được lưu vào mô hình bảng và dùng cho xuất Word.
- Chuẩn hóa độ rộng cột của bảng Phụ lục 1, thiết bị, phòng học, kiểm tra đánh giá, Phụ lục 2 và Phụ lục 3; hàng tiêu đề có `tableHeader: true` và tất cả hàng dữ liệu bảng có `cantSplit: true`.

## File đã sửa

- `js/khbd-yccd.js`
- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

Không có bộ kiểm thử xuất `.docx` độc lập trong dự án; smoke test kiểm tra các cấu hình chiều rộng, header, ngắt hàng và trang A4 ngang trong mã xuất.

## Vấn đề còn lại

- Chưa thực hiện kiểm tra hiển thị thủ công trong Microsoft Word.
- Chưa commit hoặc push theo yêu cầu.
